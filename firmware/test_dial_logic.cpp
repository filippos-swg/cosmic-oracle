// Compile-and-run check for the Pro Micro sketch.
// Stubs the Arduino API, drives a synthetic clock, and runs the SAME
// waveforms as test_dial_logic.py so both boards are proven to agree.
//
//   g++ -std=c++17 -O1 -o /tmp/dialtest firmware/test_dial_logic.cpp && /tmp/dialtest

#include <cstdio>
#include <string>
#include <vector>

// ── Arduino API stubs ────────────────────────────────────────────────
static const int HIGH = 1, LOW = 0, INPUT_PULLUP = 2, OUTPUT = 1;
static const int LED_BUILTIN = 13;

static unsigned long g_ms = 0;
static bool g_pinHigh[32];
static std::string g_sent;

unsigned long millis() { return g_ms; }
void pinMode(int, int) {}
int digitalRead(int pin) { return g_pinHigh[pin] ? HIGH : LOW; }
void digitalWrite(int, int) {}
void delay(unsigned long) {}   // time is advanced by the bench, not the sketch

struct KeyboardStub {
  void begin() {}
  void press(char c) { g_sent.push_back(c); }
  void releaseAll() {}
};
static KeyboardStub Keyboard;

#define ASTRA_TEST_NO_KEYBOARD_H 1
#include "pro-micro-arduino/astra_dial/astra_dial.ino"

// ── bench ────────────────────────────────────────────────────────────
static void tick(int ms) {
  for (int i = 0; i < ms; i++) { g_ms++; loop(); }
}
static void setPulse(bool closed)  { g_pinHigh[PIN_PULSE] = !closed; }
static void setOffRest(bool off)   { if (PIN_OFF_NORMAL >= 0) g_pinHigh[PIN_OFF_NORMAL] = !off; }

static void reset() {
  g_ms = 0;
  for (int i = 0; i < 32; i++) g_pinHigh[i] = true;  // all contacts open
  g_sent.clear();
  pulseCount = 0; digitRejected = false;
  lastEdge = 0; pulseStarted = 0; lockoutUntil = 0;
  setup();
}

static void dialDigit(int digit, int closedMs = 40, int openMs = 60, bool bounce = false) {
  int pulses = digit + 1;               // the Swedish mapping, from the visitor's side
  setOffRest(true);
  tick(40);
  for (int p = 0; p < pulses; p++) {
    setPulse(true);
    if (bounce) { tick(1); setPulse(false); tick(1); setPulse(true); }
    tick(closedMs);
    setPulse(false);
    tick(openMs);
  }
  setOffRest(false);
  tick(300);
}

static int failures = 0;
static void check(const char* label, const std::string& got, const std::string& want) {
  bool ok = got == want;
  if (!ok) failures++;
  printf("  %s  %-30s got=\"%s\" want=\"%s\"\n", ok ? "PASS" : "FAIL", label,
         got.c_str(), want.c_str());
}

int main() {
  printf("\n[pro micro / off-normal wired]\n");

  reset();
  for (int d = 0; d < 10; d++) dialDigit(d);
  check("every digit 0-9", g_sent, "0123456789");

  reset();
  for (int d : {1, 9, 0, 5}) dialDigit(d, 55, 45);
  check("slow sloppy dialling", g_sent, "1905");

  reset();
  for (int d : {2, 4, 0}) dialDigit(d, 30, 35);
  check("fast dialling", g_sent, "240");

  reset();
  for (int d : {3, 0, 7}) dialDigit(d, 40, 60, true);
  check("dirty contacts (bounce)", g_sent, "307");

  reset();
  for (int d : {1, 8, 0, 8, 1, 9, 7, 5}) dialDigit(d);
  check("full birthdate", g_sent, "18081975");

  reset();
  for (int i = 0; i < 3; i++) dialDigit(0);
  check("000 reset sequence", g_sent, "000");

  reset();
  tick(200); setPulse(true); tick(3); setPulse(false); tick(600);
  check("phantom glitch at rest", g_sent, "");

  reset();
  tick(200); setPulse(true); tick(40); setPulse(false); tick(600);
  check("spurious 40ms pulse at rest", g_sent, "");

  reset();
  setOffRest(true); tick(40);
  setPulse(true); tick(400); setPulse(false); tick(100);
  setOffRest(false); tick(300);
  check("stuck contact rejected", g_sent, "");

  printf(failures ? "\nFAILED: %d\n" : "\nall checks passed\n", failures);
  return failures ? 1 : 0;
}
