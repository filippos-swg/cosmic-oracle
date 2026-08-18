# firmware — the rotary dial

The dial is the whole interface. This folder turns its contact pulses into
USB keystrokes `0`–`9` and sends nothing else, ever. `tv.html` already
treats plain digits as the entire interaction: eight digits are a birthdate,
`000` mid-entry clears the slate, `1`/`2`/`3` answer the CLARIFY question.

| | |
|---|---|
| Primary board | Raspberry Pi Pico (RP2040), CircuitPython 9.x — `pico-circuitpython/` |
| Spare board | Arduino Pro Micro / Leonardo (32U4) — `pro-micro-arduino/` |
| Bench dial | Försvaret surplus Fingerskiva M 3926-990019 (exposed screw terminals) |
| Stage dial | LM Ericsson DBH 1001 bakelite, "modell 1947" |

Both firmwares implement the same state machine with the same constants.
Change a timing number in one, change it in the other — otherwise the spare
board behaves differently from the one in the phone on the night it matters.

---

## ⚠ The Swedish mapping

```
0 → 1 pulse    1 → 2 pulses    …    9 → 10 pulses
firmware:  digit = pulse_count - 1
```

International/ABC dials are the other way round (1→1 … 0→10). The faceplate
tell: a Swedish dial prints **0 beside 1 at the fingerstop** — visible on the
purchased Ericsson.

Get this backwards and every birthdate in the exhibition is shifted by one
digit. It will not look like a wiring bug. It will look like the readings are
wrong, and you will go hunting in `librarian.py` for two days.

**Test it end to end with a known date before anything is closed up.**

---

## Wiring

A rotary dial has two contact sets that matter. Find them with a continuity
meter — do not trust wire colours, they vary by decade and by whoever was
last inside the phone.

| Contact | Behaviour at the meter | Goes to |
|---|---|---|
| **IMPULSE** | opens and closes *n* times as the dial returns | `GP2` (Pico) / `D2` (Pro Micro), other side to GND |
| **OFF-NORMAL** | closed the whole time the dial is away from rest, open at rest | `GP3` (Pico) / `D3` (Pro Micro), other side to GND |

Both contacts are dry — no polarity, no supply, internal pull-ups do the
rest. Twist each pair, keep the leads short: they will live inside a wooden
box beside a 170 W valve television with a mains transformer in it.

### Wire the off-normal contact. It is not optional in practice.

The old notes assumed two wires and a 250 ms silence timeout. That works on
the bench and fails in a gallery, for one specific reason:

> In the Swedish mapping, **a single pulse is a legitimate `0`**.

So one spurious pulse — a dirty contact settling, hum coupling into a long
unshielded lead, somebody knocking the table — types a `0` into a visitor's
birthdate, and the machine gives them a reading for the wrong day with total
confidence. The off-normal contact makes that impossible: at rest the
firmware ignores the impulse line completely, and a digit is emitted because
the dial physically came home, not because nothing happened for a quarter
second.

The test suite proves the difference rather than asserting it:

```
[off-normal wired]   spurious 40 ms pulse at rest → nothing
[pulse pair only]    spurious 40 ms pulse at rest → types "0"
```

Set `OFF_NORMAL_PIN = None` (Pico) or `PIN_OFF_NORMAL = -1` (Pro Micro) only
if the stage phone turns out to have no accessible off-normal spring — and
if so, budget an extra day for the 24 h phantom soak.

### Into the Ericsson

Develop and debounce on the surplus bench dial. Only when it passes the
checklist below, migrate into the DBH 1001: the board sits in the base, taps
the dial's existing contact springs, and the phone's **original wiring stays
untouched and reconnected** — the piece must be able to go back to being a
telephone. Bring the USB cable out through the existing cord exit; no new
holes in bakelite.

The hook switch stays unwired for v1 (decision carried from
`exhibition/HARDWARE_DIAL.md`). The handset is scenery for now.

---

## Install — Pi Pico

1. Flash CircuitPython 9.x (`.uf2`, drag and drop while holding BOOTSEL).
2. Copy `adafruit_hid/` from the CircuitPython bundle into `CIRCUITPY/lib/`.
3. Copy `pico-circuitpython/code.py` and `pico-circuitpython/boot.py` to the
   root of `CIRCUITPY`.
4. Unplug, replug. Three slow blinks on the onboard LED = alive and
   enumerated. One short blink per digit sent.

`boot.py` hides the `CIRCUITPY` drive and the serial console. This matters
more than it looks: if the drive mounts, the appliance Mac opens a Finder
window at login, over a 1950s television, and launchd cannot undo it.

**To get back in:** ground `GP15` while plugging the board in. The drive and
REPL return for that session.

## Install — Pro Micro

Arduino IDE, board *Arduino Leonardo*, open `pro-micro-arduino/astra_dial/`,
upload. Nothing to install — `Keyboard.h` is core, and nothing else is
included on purpose.

---

## Testing without hardware

Both implementations are driven through the same synthesized waveforms —
clean dialling, sloppy dialling, contact bounce, a welded contact, and the
phantom pulse:

```bash
python3 firmware/test_dial_logic.py

g++ -std=c++17 -O1 -Ifirmware/test-shim -o /tmp/dialtest \
    firmware/test_dial_logic.cpp && /tmp/dialtest
```

Both should print `all checks passed`. Run them after any timing change,
before you touch a screwdriver.

---

## Bench checklist (carried from HARDWARE_DIAL.md, still binding)

- [ ] Each digit 0–9, twenty times: 100 % correct, no doubles, no drops.
- [ ] A full birthdate dialled fast and sloppy → correct on `tv.html` IDENTIFY.
- [ ] `000` mid-entry → the slate clears.
- [ ] `1` / `2` / `3` at CLARIFY select the right domain.
- [ ] Connected 24 h beside the powered TV: **zero** phantom keypresses.
- [ ] Unplug/replug the USB: the board re-enumerates and still types.
- [ ] Cold boot of the Mac with the dial already connected: no Finder window,
      no drive on the desktop, ASTRA reaches IDLE untouched.
