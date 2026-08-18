"""Bench-free verification of the dial state machine.

Runs the ACTUAL code.py logic (with CircuitPython's board/digitalio/usb_hid
stubbed out and time driven by hand) against synthesized pulse trains:
clean dialling, sloppy dialling, contact bounce, and the mains-hum phantom
that would otherwise type a '0' into somebody's birthdate.

    python3 firmware/test_dial_logic.py
"""

import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "pico-circuitpython", "code.py")

# ── clock we control ──────────────────────────────────────────────────
CLOCK_MS = [0]


def fake_monotonic_ns():
    return CLOCK_MS[0] * 1_000_000


def fake_sleep(_seconds):
    return None


# ── pin fakes ─────────────────────────────────────────────────────────
PIN_STATE = {}  # pin name -> raw electrical level (True = high/open)


class _Direction:
    INPUT = "in"
    OUTPUT = "out"


class _Pull:
    UP = "up"
    DOWN = "down"


class _DigitalInOut:
    def __init__(self, pin):
        self.pin = pin
        self.direction = None
        self.pull = None
        self._out = False

    @property
    def value(self):
        if self.direction == _Direction.OUTPUT:
            return self._out
        return PIN_STATE.get(self.pin, True)

    @value.setter
    def value(self, v):
        self._out = v

    def deinit(self):
        pass


SENT = []


class _Keyboard:
    def __init__(self, _devices):
        pass

    def press(self, code):
        SENT.append(code)

    def release_all(self):
        pass


def install_stubs():
    board = types.ModuleType("board")
    for name in ("GP2", "GP3", "GP15", "LED"):
        setattr(board, name, name)
    sys.modules["board"] = board

    digitalio = types.ModuleType("digitalio")
    digitalio.DigitalInOut = _DigitalInOut
    digitalio.Direction = _Direction
    digitalio.Pull = _Pull
    sys.modules["digitalio"] = digitalio

    usb_hid = types.ModuleType("usb_hid")
    usb_hid.devices = []
    sys.modules["usb_hid"] = usb_hid

    hid_pkg = types.ModuleType("adafruit_hid")
    sys.modules["adafruit_hid"] = hid_pkg

    kb_mod = types.ModuleType("adafruit_hid.keyboard")
    kb_mod.Keyboard = _Keyboard
    sys.modules["adafruit_hid.keyboard"] = kb_mod

    kc_mod = types.ModuleType("adafruit_hid.keycode")

    class Keycode:
        ZERO, ONE, TWO, THREE, FOUR = 0, 1, 2, 3, 4
        FIVE, SIX, SEVEN, EIGHT, NINE = 5, 6, 7, 8, 9

    kc_mod.Keycode = Keycode
    sys.modules["adafruit_hid.keycode"] = kc_mod


def load_module():
    """Exec code.py without its trailing main() call."""
    with open(SRC) as fh:
        src = fh.read()
    src = src.replace("\nmain()\n", "\n")
    module = types.ModuleType("astra_dial_under_test")
    ns = module.__dict__
    exec(compile(src, SRC, "exec"), ns)

    # Drive the module's clock from CLOCK_MS instead of the wall.
    fake_time = types.ModuleType("time")
    fake_time.monotonic_ns = fake_monotonic_ns
    fake_time.sleep = fake_sleep
    ns["time"] = fake_time
    return module


# ── waveform driver ───────────────────────────────────────────────────
class Bench:
    """Drives the fake pins forward in 1 ms ticks and collects emissions."""

    def __init__(self, mod, use_off_normal):
        self.mod = mod
        mod.OFF_NORMAL_PIN = "GP3" if use_off_normal else None
        mod.LED_PIN = None
        PIN_STATE["GP2"] = True   # pulse contact open
        PIN_STATE["GP3"] = True   # dial at rest
        SENT.clear()
        self.dial = mod.Dial(_Keyboard(None), None)
        self.emitted = []

    def advance(self, ms):
        for _ in range(ms):
            CLOCK_MS[0] += 1
            out = self.dial.step(CLOCK_MS[0])
            if out is not None:
                self.emitted.append(out)

    def set_pulse(self, closed):
        PIN_STATE["GP2"] = not closed

    def set_off_rest(self, off_rest):
        PIN_STATE["GP3"] = not off_rest

    def dial_digit(self, digit, closed_ms=40, open_ms=60, bounce=False):
        """Dial `digit` the Swedish way: digit + 1 pulses."""
        pulses = digit + 1
        self.set_off_rest(True)
        self.advance(40)
        for _ in range(pulses):
            self.set_pulse(True)
            if bounce:
                self.advance(1)
                self.set_pulse(False)
                self.advance(1)
                self.set_pulse(True)
            self.advance(closed_ms)
            self.set_pulse(False)
            self.advance(open_ms)
        self.set_off_rest(False)
        self.advance(300)


# ── the checks ────────────────────────────────────────────────────────
def run():
    install_stubs()
    mod = load_module()
    failures = []

    def check(label, got, want):
        ok = got == want
        print(("  PASS  " if ok else "  FAIL  ") + label + f"   got={got} want={want}")
        if not ok:
            failures.append(label)

    for use_on in (True, False):
        mode = "off-normal wired" if use_on else "pulse pair only"
        print(f"\n[{mode}]")

        b = Bench(mod, use_on)
        for d in range(10):
            b.dial_digit(d)
        check("every digit 0-9, clean", b.emitted, list(range(10)))

        b = Bench(mod, use_on)
        for d in (1, 9, 0, 5):
            b.dial_digit(d, closed_ms=55, open_ms=45)
        check("slow sloppy dialling", b.emitted, [1, 9, 0, 5])

        b = Bench(mod, use_on)
        for d in (2, 4, 0):
            b.dial_digit(d, closed_ms=30, open_ms=35)
        check("fast dialling", b.emitted, [2, 4, 0])

        b = Bench(mod, use_on)
        for d in (3, 0, 7):
            b.dial_digit(d, bounce=True)
        check("dirty contacts (bounce)", b.emitted, [3, 0, 7])

        b = Bench(mod, use_on)
        for d in (1, 8, 0, 8, 1, 9, 7, 5):   # 18-08-1975
            b.dial_digit(d)
        check("full birthdate 18081975", b.emitted, [1, 8, 0, 8, 1, 9, 7, 5])

        b = Bench(mod, use_on)
        for _ in range(3):
            b.dial_digit(0)
        check("000 reset sequence", b.emitted, [0, 0, 0])

        # a 3 ms glitch, dial at rest — the mains-hum phantom
        b = Bench(mod, use_on)
        b.advance(200)
        b.set_pulse(True)
        b.advance(3)
        b.set_pulse(False)
        b.advance(600)
        check("phantom glitch at rest", b.emitted, [])

        # a full-width spurious pulse while at rest: only off-normal saves us
        b = Bench(mod, use_on)
        b.advance(200)
        b.set_pulse(True)
        b.advance(40)
        b.set_pulse(False)
        b.advance(600)
        check(
            "spurious 40 ms pulse at rest",
            b.emitted,
            [] if use_on else [0],   # ← documented: pulse-pair-only types a 0
        )

        # contact welds shut mid-digit
        b = Bench(mod, use_on)
        b.set_off_rest(True)
        b.advance(40)
        b.set_pulse(True)
        b.advance(400)
        b.set_pulse(False)
        b.advance(100)
        b.set_off_rest(False)
        b.advance(300)
        check("stuck contact rejected", b.emitted, [])

    print()
    if failures:
        print(f"FAILED: {len(failures)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(run())
