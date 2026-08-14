# Rotary dial hardware — notes for the build session

**Chosen hardware (Tradera, 2026-08):**
- Stage phone: LM Ericsson DBH 1001 bakelite, "modell 1947" (1947–1962) —
  period-matched to the DUX TV. Dial contacts accessed inside the base;
  original wiring untouched (reversible).
- Bench unit: Försvaret surplus dial, Fingerskiva M 3926-990019 — exposed
  screw terminals; develop and debounce the firmware on this one, keep as
  spare.
- Rejected: Ericofon (dial on the underside — wrong ergonomics for a
  planted public dial; hook-switch button inside the dial face).

## ⚠ SWEDISH PULSE MAPPING — DO NOT SKIP

Swedish rotary dials are shifted relative to the international standard:

    0 → 1 pulse, 1 → 2 pulses, ... 9 → 10 pulses
    firmware: digit = pulse_count - 1

(International/ABC standard is 1→1 ... 0→10. The faceplate tell: Swedish
dials print 0 next to 1 at the fingerstop.) Getting this wrong shifts
every birthdate by one digit — test with a known date end-to-end.

## Firmware plan (ESP32-S2/S3 or Pi Pico, USB HID keyboard)

1. Dial pulse contacts → GPIO with internal pull-up; contacts open/close
   at ~10 pulses/sec, ~60/40 duty.
2. Debounce ~15-25 ms; count pulses; a gap > ~250 ms ends the digit.
3. digit = count - 1 (Swedish mapping above).
4. Send as USB HID keypress '0'-'9'. Nothing else. The page already
   treats plain digits as the whole interface (000 = reset, 1/2/3 =
   clarify choice).
5. Optional later: hook switch on a second GPIO (the bakelite handset) —
   reserved for a future interaction; do not wire for v1.

## Bench test checklist

- Dial each digit 0-9 twenty times: 100% correct, no doubles.
- Dial a full birthdate fast and sloppy; verify on tv.html IDENTIFY.
- Dial 000 mid-entry: slate clears.
- Leave connected 24h: no phantom keypresses (mind mains hum near the
  TV — twist the contact pair, keep leads short).
