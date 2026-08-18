/*
 * ASTRA — rotary dial to USB keyboard digits
 * Arduino Pro Micro / Leonardo (ATmega32U4) — the spare-board variant.
 *
 * Same state machine as firmware/pico-circuitpython/code.py, same numbers.
 * If you change a timing constant, change it in both, or the spare board
 * will behave differently from the one in the phone on the one night it
 * matters.
 *
 * ─────────────────────────────────────────────────────────────────────
 * THE SWEDISH MAPPING
 *
 *   0 sends 1 pulse, 1 sends 2, ... 9 sends 10   →   digit = pulses - 1
 *
 * International/ABC dials are the other way round. Faceplate tell: a
 * Swedish dial prints 0 beside 1 at the fingerstop. Backwards here and
 * every birthdate in the room is shifted by one digit.
 * ─────────────────────────────────────────────────────────────────────
 *
 * WIRING
 *   PIN_PULSE      → dial IMPULSE contact, other side to GND
 *   PIN_OFF_NORMAL → dial OFF-NORMAL contact, other side to GND
 *                    (set to -1 to run on the pulse pair alone — but read
 *                     the note in ../../README.md first: without it, one
 *                     spurious pulse types a 0 into a birthdate)
 *
 * Board: Arduino Leonardo / SparkFun Pro Micro (32U4). Needs Keyboard.h,
 * which is core. Nothing else is installed, on purpose.
 */

#include <Keyboard.h>

// ── CONFIG ───────────────────────────────────────────────────────────
static const int  PIN_PULSE              = 2;
static const int  PIN_OFF_NORMAL         = 3;    // -1 to disable
static const int  PIN_LED                = LED_BUILTIN;  // -1 to disable

static const unsigned long DEBOUNCE_MS            = 20;
static const unsigned long DIGIT_GAP_MS           = 250;
static const unsigned long POST_DIGIT_LOCKOUT_MS  = 120;
static const unsigned long MIN_PULSE_MS           = 15;
static const unsigned long MAX_PULSE_MS           = 200;
static const unsigned long KEY_PRESS_MS           = 15;

static const bool PULSE_ACTIVE_LOW      = true;
static const bool OFF_NORMAL_ACTIVE_LOW = true;
// ─────────────────────────────────────────────────────────────────────

struct Debounced {
  int pin;
  bool activeLow;
  bool state;
  bool candidate;
  unsigned long since;

  void begin(int p, bool al, unsigned long now) {
    pin = p;
    activeLow = al;
    pinMode(pin, INPUT_PULLUP);
    state = raw();
    candidate = state;
    since = now;
  }

  bool raw() const {
    bool v = digitalRead(pin) == HIGH;
    return activeLow ? !v : v;
  }

  // true when the settled state changed on this call
  bool update(unsigned long now) {
    bool r = raw();
    if (r != candidate) {
      candidate = r;
      since = now;
      return false;
    }
    if (r != state && (now - since) >= DEBOUNCE_MS) {
      state = r;
      return true;
    }
    return false;
  }
};

static Debounced pulse;
static Debounced offNormal;
static bool haveOffNormal = false;

static int  pulseCount     = 0;
static bool digitRejected  = false;
static unsigned long lastEdge      = 0;
static unsigned long pulseStarted  = 0;
static unsigned long lockoutUntil  = 0;

static void resetDigit() {
  pulseCount = 0;
  digitRejected = false;
}

static void beginPulse(unsigned long now) {
  pulseStarted = now;
  lastEdge = now;
}

static void endPulse(unsigned long now) {
  unsigned long width = now - pulseStarted;
  lastEdge = now;
  if (width < MIN_PULSE_MS || width > MAX_PULSE_MS) {
    // too short to be a dial, or a contact that stuck: poison the digit
    // rather than let a wrong number into somebody's birthdate
    digitRejected = true;
    return;
  }
  pulseCount++;
  if (pulseCount > 10) digitRejected = true;
}

static void emitDigit(unsigned long now) {
  int count = pulseCount;
  bool rejected = digitRejected;
  resetDigit();
  lockoutUntil = now + POST_DIGIT_LOCKOUT_MS;

  if (rejected || count < 1 || count > 10) return;

  char c = (char)('0' + (count - 1));   // ← the Swedish mapping
  Keyboard.press(c);
  delay(KEY_PRESS_MS);
  Keyboard.releaseAll();

  if (PIN_LED >= 0) {
    digitalWrite(PIN_LED, HIGH);
    delay(20);
    digitalWrite(PIN_LED, LOW);
  }
}

void setup() {
  unsigned long now = millis();
  pulse.begin(PIN_PULSE, PULSE_ACTIVE_LOW, now);
  haveOffNormal = (PIN_OFF_NORMAL >= 0);
  if (haveOffNormal) offNormal.begin(PIN_OFF_NORMAL, OFF_NORMAL_ACTIVE_LOW, now);

  if (PIN_LED >= 0) pinMode(PIN_LED, OUTPUT);

  Keyboard.begin();

  // three slow blinks: firmware alive, host enumerated it
  if (PIN_LED >= 0) {
    for (int i = 0; i < 3; i++) {
      digitalWrite(PIN_LED, HIGH); delay(120);
      digitalWrite(PIN_LED, LOW);  delay(120);
    }
  }
}

void loop() {
  unsigned long now = millis();

  if (haveOffNormal) {
    bool wasOffRest = offNormal.state;
    if (offNormal.update(now)) {
      if (offNormal.state && !wasOffRest) {
        resetDigit();            // dial has left rest: a new digit begins
      } else if (wasOffRest && !offNormal.state) {
        emitDigit(now);          // dial is home: the digit is complete
        return;
      }
    }
    // At rest, the contacts are not the visitor. Ignore them — this is
    // what kills phantom input from mains hum beside the television.
    if (!offNormal.state) {
      pulse.update(now);
      return;
    }
  }

  if (now < lockoutUntil) {
    pulse.update(now);
    return;
  }

  if (pulse.update(now)) {
    if (pulse.state) beginPulse(now);
    else             endPulse(now);
  }

  // No off-normal contact wired: fall back to the silence timeout.
  if (!haveOffNormal && pulseCount > 0 && !pulse.state &&
      (now - lastEdge) >= DIGIT_GAP_MS) {
    emitDigit(now);
  }
}
