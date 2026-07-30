# Experiment: ambient sound

**Status:** sandbox — includes found-items + ceremonial mono type.
Production tv.html untouched.

Sound design, not soundtrack. Everything is synthesized live with WebAudio:
nothing loads, nothing loops audibly, works fully offline.

## The design

- **Carrier hum** (55/110 Hz) + **shortwave drift** (brown noise through a
  slowly wandering bandpass) — the set is alive. Intensity follows the
  ceremony: full in IDLE, dimmed during IDENTIFY, swelling in CONSULT,
  calm under the READING.
- **Dial clunks** — a mechanical thunk per digit; a double-clunk on the
  0·0·0 reset.
- **Text ticks** — a papery tick as each reading screen lands.
- **Numbers-station murmur** — quiet filtered blips under CONSULT only.
- **The held breath** — on "ONE ITEM REMAINS," the bed fades to true
  silence. The letter/dream plays in a silent room. This is the whole
  point; resist the urge to fill it.

## Try it

    http://localhost:8000/experiments/sound/tv.html

Click/keypress once to unlock audio (browser autoplay policy), then dial.
**M** mutes. **P** previews the ending (note the silence drop).

## Levels

All in the AUDIO module's CFG + SCENES table at the top of the script:
CFG.master (overall, default 0.35), per-scene bed multipliers, and the
clunk/tick/blip volumes inline. The TV's own volume knob is the intended
gallery control.

## Kiosk note

For sound to start on boot without a keypress, launch Chrome with
--autoplay-policy=no-user-gesture-required (add to the kiosk flags in the
appliance setup). Audio output must be routed with video through the
converter to the TV speaker, or via a separate small amp — decide during
the hardware session.
