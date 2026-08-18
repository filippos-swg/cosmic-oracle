# RUNBOOK — ASTRA

For whoever opens the room. Assume that person is not Filippos, is not
technical, and has four minutes.

**The working principle, which is also the acceptance criterion:** power on
the object; the sky is already being observed; ASTRA appears. No keyboard, no
mouse, no desktop, no terminal, ever visible to a visitor.

---

## OPEN

1. Wall socket / power strip **on**. Order does not matter; everything is on
   KeepAlive and comes back on its own.
2. Open the cabinet doors.
3. Wait. The tube takes 20–40 seconds to warm; the Mac takes about a minute
   to reach the ceremony. **Do not touch anything during this.**
4. You should see: the boot calibration ritual, then IDLE — the figure, a
   slow rotating line about the sky, and the invitation to dial.
5. Lift the handset off the phone and put it back. Nothing should happen —
   the hook switch is unwired. This is the daily check that nobody has
   "helpfully" rewired anything.
6. Dial **one digit**. A digit should appear. Then dial `0` `0` `0` to clear
   the slate. Leave it at IDLE.

Doors stay open while the room is open. Cabinet top must stay clear —
nothing placed on it, ever. It is the set's air exit.

## CLOSE

1. Leave the piece at IDLE. If somebody left it mid-ceremony, dial `0` `0` `0`
   and let it time out, or press `Esc` on the hidden keyboard.
2. Close the doors.
3. Power strip **off** at the wall.

Do **not** shut the Mac down from the menu. Do not close the lid. The whole
appliance is built to be cut at the wall and to come back by itself; the
menu route breaks auto-login on some restarts and needs a keyboard to fix.

---

## TRIAGE

Work down each list. Stop at the first thing that fixes it.

### Black screen, no sound, nothing

1. Is the power strip on? Is the TV's own switch on?
2. Give it two full minutes. A cold Mac plus a cold tube is slower than you
   think it is.
3. Cut power at the wall, wait ten seconds, restore. This fixes most of it.
4. If the TV shows **snow or a rolling picture**, the Mac is probably fine
   and the picture chain is not — go to *Snow / rolling picture*.
5. If the TV is dark but you can hear the drone from its speaker, the tube or
   the set is the problem, not the computer. Close the doors, put the "not
   today" card up, call Filippos.

### Snow / rolling picture / no picture but sound is fine

1. Check the TV's channel knob has not been knocked. It should sit on the
   channel written on the tape inside the cabinet door.
2. Check the modulator's power LED, and the coax at both ends.
3. Check the small converter box between the Mac and the modulator — if it
   was power-cycled it can come back in the wrong TV standard. Its switch
   must read **PAL**, not NTSC. Power-cycle just that box.
4. Spare converter is in the drawer. Swap it, same cables, same switch
   position.

### Picture is there, but it never leaves IDLE / the dial does nothing

1. Dial slowly and let the dial return all the way home each time. A hand
   held against the returning dial will drop the digit.
2. Try `0` `0` `0` — three clears in a row is the most forgiving thing to
   dial.
3. Under the phone base: the USB cable to the Mac. Unplug and replug it. The
   board re-enumerates in a second; a small LED inside the base blinks three
   times when it does.
4. Still nothing: the spare board is in the drawer, pre-flashed, with the
   same two-connector plug. Swap it.
5. Piece still works without the dial — it holds IDLE and shows the day's
   sky. That is an acceptable half-open state for a few hours. It is not
   acceptable overnight.

### Digits appear but they are the wrong digits

Stop. This is the Swedish pulse mapping (`digit = pulses − 1`) and it means
somebody re-flashed the board. Do not attempt to fix it in the room. Put the
"not today" card up and call Filippos.

### The screen is frozen on one image

The particle figure always moves. If it is truly static, Chrome has died.
Cut power at the wall and restore.

### A desktop, a menu bar, a Finder window, or a dialog is visible

The illusion is broken and there is a real fault behind it. Cut power at the
wall and restore. If it comes back a second time, close the doors and call —
a mounted USB drive or a software-update prompt is the usual cause and both
need fixing properly.

---

## Things that are NOT faults

- The picture is soft and a little grey. It is a 1950s tube fed through its
  own tuner. That is the piece.
- The picture takes half a minute to bloom to full size and brightness.
- The reading is different for two people born on the same day. That is
  deliberate.
- Faint hum from the cabinet. Valves and a mains transformer.
- The tube clicks and ticks as it warms and cools.

## Things that ARE faults, even if the piece looks fine

- Cabinet top hot enough to be uncomfortable to rest a hand on at close.
- Burning or hot-dust smell. **Power off at the wall immediately and do not
  restore it.**
- Any visible smoke or arcing sound. Same. Call.
- A digit appearing on screen without anybody touching the dial.

---

## Weekly, for a long run

- Monday morning before opening: full cold-boot test — power off at the wall,
  restore, watch it reach IDLE without a keyboard.
- Dial one full known birthdate and confirm it reads back correctly on the
  IDENTIFY screen. This catches a drifting dial before a visitor does.
- Wipe the tube glass with a dry microfibre cloth. Nothing wet, nothing
  near the vents.
- Confirm the automatic weekly restart happened (`pmset repeat restart` is
  set for 05:00; the piece should simply be running).

---

## For Filippos — the technical shelf

Only for someone with the hidden keyboard and a reason.

```
status   launchctl list | grep astra
logs     tail -f /tmp/astra_oracle.log /tmp/astra_server.log
restart  bash kiosk/install.sh
remove   bash kiosk/install.sh uninstall
check    npm run check          # harness suite, before touching corpus
```

Dev keys on `tv.html`: digits dial · `000` resets the date · `Enter`/`Space`
advances · `Esc` abandons · `M` mutes · `P` previews the ending · `Enter`
during boot skips it.

The nine machine settings launchd cannot do are printed by
`kiosk/install.sh` at the end of every install. Auto-login, no sleep, Do Not
Disturb, no automatic updates, Spotlight exclusion, display resolution,
`ENTITY_COUNT` 40–60k, weekly reboot, Wi-Fi verified off.

## Contacts

| | |
|---|---|
| Artist | Filippos Arvanitakis — filippos@southnorth.se |
| TV technician | *(fill in after the recap — name, phone, and what they did)* |
| Venue technical | *(fill in per exhibition)* |

Repo: `~/Projects/cosmic-oracle` on the appliance Mac (user `astrologer`,
host `Astrologer-Core`). Mirror: `github.com/filippos-swg/cosmic-oracle`.

---

## Opening-night acceptance test

Not done until every line passes, in this order, on the real object.

- [ ] Cold boot from a dead wall socket → IDLE, untouched, nothing visible
      that is not the piece.
- [ ] Repeated ten times. Ten out of ten.
- [ ] One full ceremony dialled on the real dial with a **known** birthdate;
      the date reads back correctly on IDENTIFY.
- [ ] Each of `1` / `2` / `3` at CLARIFY reaches its domain.
- [ ] 24 h connected and powered beside the running TV: zero phantom digits.
- [ ] Sound judged through the TV's own speaker, levels committed.
- [ ] `CONFIG.SAFE` and `CONFIG.TYPE_SCALE` measured on this tube and
      committed, with a note saying which set they were measured on.
- [ ] Wall label printed and mounted; instruction panel at the phone.
- [ ] Doors-open ritual decided and written into OPEN above.
