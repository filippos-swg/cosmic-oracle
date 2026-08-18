# ASTRA — rotary dial to USB keyboard digits
# Raspberry Pi Pico (RP2040) + CircuitPython 9.x + adafruit_hid
#
# Reads the pulse contacts of a Swedish rotary dial and types 0-9.
# Nothing else is ever sent. tv.html treats plain digits as the whole
# interface (date entry, 000 = reset, 1/2/3 = the clarify choice).
#
# ─────────────────────────────────────────────────────────────────────
# THE SWEDISH MAPPING — the one thing that must not be got wrong
#
#   0 sends 1 pulse, 1 sends 2, ... 9 sends 10   →   digit = pulses - 1
#
# The international/ABC standard is the other way round (1→1 ... 0→10).
# Faceplate tell: a Swedish dial prints 0 beside 1 at the fingerstop.
# Get this backwards and every birthdate in the exhibition is shifted by
# one digit — and it will look like a content bug, not a wiring bug.
# ─────────────────────────────────────────────────────────────────────
#
# WIRING (see ../README.md for how to find the contacts with a meter)
#
#   PULSE_PIN      → one side of the dial's IMPULSE contact pair
#   GND            → the other side
#   OFF_NORMAL_PIN → one side of the OFF-NORMAL contact pair  (optional,
#   GND              strongly recommended — see below)
#
# The off-normal contact is closed only while the dial is away from rest.
# Wiring it turns "a digit ended because nothing happened for 250 ms" into
# "a digit ended because the dial physically returned", and it makes a
# stray pulse arriving while the dial is AT REST impossible to mistake for
# a dialled 0. One spurious pulse without it types a '0' into somebody's
# birthdate. Two extra wires buy the whole phantom-input class.

import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ── CONFIG ───────────────────────────────────────────────────────────
# These are the only numbers to touch on the bench.

PULSE_PIN = board.GP2
OFF_NORMAL_PIN = board.GP3      # set to None if you wired only the pair
LED_PIN = board.LED             # blinks once per digit sent; None to disable

DEBOUNCE_MS = 20                # contact settle; dial pulses are ~40-60 ms
DIGIT_GAP_MS = 250              # silence that ends a digit (no-off-normal mode)
POST_DIGIT_LOCKOUT_MS = 120     # ignore contacts right after sending
MIN_PULSE_MS = 15               # a "pulse" shorter than this is noise
MAX_PULSE_MS = 200              # ...and longer than this is a stuck contact

PULSE_ACTIVE_LOW = True         # contact closed to GND == pulse asserted
OFF_NORMAL_ACTIVE_LOW = True    # contact closed to GND == dial off rest

KEY_PRESS_MS = 15               # HID press duration
# ─────────────────────────────────────────────────────────────────────

DIGIT_KEYCODES = (
    Keycode.ZERO, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR,
    Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE,
)


def _now_ms():
    return time.monotonic_ns() // 1_000_000


def _make_input(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return io


class Debounced:
    """A contact, read as a settled boolean. True == asserted (closed)."""

    def __init__(self, pin, active_low, debounce_ms):
        self._io = _make_input(pin)
        self._active_low = active_low
        self._debounce_ms = debounce_ms
        self.state = self._raw()
        self._candidate = self.state
        self._since = _now_ms()

    def _raw(self):
        v = self._io.value
        return (not v) if self._active_low else v

    def update(self, now):
        """Returns True if the settled state changed on this call."""
        raw = self._raw()
        if raw != self._candidate:
            self._candidate = raw
            self._since = now
            return False
        if raw != self.state and (now - self._since) >= self._debounce_ms:
            self.state = raw
            return True
        return False


class Dial:
    def __init__(self, keyboard, led=None):
        self.kbd = keyboard
        self.led = led
        self.pulse = Debounced(PULSE_PIN, PULSE_ACTIVE_LOW, DEBOUNCE_MS)
        self.off_normal = (
            Debounced(OFF_NORMAL_PIN, OFF_NORMAL_ACTIVE_LOW, DEBOUNCE_MS)
            if OFF_NORMAL_PIN is not None
            else None
        )
        self.count = 0
        self.rejected = False        # this digit saw something implausible
        self.last_edge = 0
        self.pulse_started = 0
        self.lockout_until = 0

    # ── pulse accounting ──
    def _begin_pulse(self, now):
        self.pulse_started = now
        self.last_edge = now

    def _end_pulse(self, now):
        width = now - self.pulse_started
        self.last_edge = now
        if width < MIN_PULSE_MS or width > MAX_PULSE_MS:
            # Too short to be a dial, or a contact that stuck. Poison the
            # digit rather than let a wrong number into a birthdate.
            self.rejected = True
            return
        self.count += 1
        if self.count > 10:
            self.rejected = True

    def _reset(self):
        self.count = 0
        self.rejected = False

    def _emit(self, now):
        count, rejected = self.count, self.rejected
        self._reset()
        self.lockout_until = now + POST_DIGIT_LOCKOUT_MS
        if rejected or not (1 <= count <= 10):
            return None
        digit = count - 1                      # ← the Swedish mapping
        self.kbd.press(DIGIT_KEYCODES[digit])
        time.sleep(KEY_PRESS_MS / 1000)
        self.kbd.release_all()
        if self.led is not None:
            self.led.value = True
            time.sleep(0.02)
            self.led.value = False
        return digit

    # ── main step ──
    def step(self, now):
        if self.off_normal is not None:
            was_off_rest = self.off_normal.state
            if self.off_normal.update(now):
                if self.off_normal.state and not was_off_rest:
                    self._reset()             # dial has left rest: new digit
                elif was_off_rest and not self.off_normal.state:
                    return self._emit(now)    # dial is home: digit complete

            # At rest, contacts are not the visitor. Ignore them entirely —
            # this is what kills phantom input from mains hum near the TV.
            if not self.off_normal.state:
                self.pulse.update(now)
                return None

        if now < self.lockout_until:
            self.pulse.update(now)
            return None

        if self.pulse.update(now):
            if self.pulse.state:
                self._begin_pulse(now)
            else:
                self._end_pulse(now)

        # No off-normal contact wired: fall back to the silence timeout.
        if (
            self.off_normal is None
            and self.count
            and not self.pulse.state
            and (now - self.last_edge) >= DIGIT_GAP_MS
        ):
            return self._emit(now)

        return None


def main():
    kbd = Keyboard(usb_hid.devices)

    led = None
    if LED_PIN is not None:
        led = digitalio.DigitalInOut(LED_PIN)
        led.direction = digitalio.Direction.OUTPUT
        led.value = False

    dial = Dial(kbd, led)

    # Three slow blinks: firmware is alive and the host enumerated it.
    if led is not None:
        for _ in range(3):
            led.value = True
            time.sleep(0.12)
            led.value = False
            time.sleep(0.12)

    while True:
        dial.step(_now_ms())
        time.sleep(0.001)


main()
