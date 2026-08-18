# BUILD GUIDE — ASTRA, for one person, alone

The other hardware documents are written for someone who already knows this
stuff. This one is not. It assumes you own a screwdriver, can follow a
recipe, and have never wired a microcontroller. Nothing here requires
soldering.

Read `exhibition/PICTURE_CHAIN.md` only if you want the reasoning. Everything
you have to *do* is in this file.

---

## What you already have

| | |
|---|---|
| Television | DUX V6397, 1950s, Swedish. **Not yet powered on. Do not power it on.** |
| Computer | MacBook Pro 15", 2016–2018 |
| Phone | LM Ericsson DBH 1001 bakelite — the one on show |
| Bench dial | Försvaret surplus dial, screw terminals — the one you practise on |
| Converter | Mini HDMI2AV box (HDMI in, three RCA plugs out) |
| Cable | 100 W USB-C charging cable — that is **power only**, it carries no video |

## What the whole thing has to become

```
   MacBook  ──USB-C→HDMI adapter──  HDMI2AV box  ──yellow RCA──  TV picture
        │                                        └─red+white──  TV sound
        └──USB──  the phone dial
```

Three cables. That is the entire machine. Everything below is about making
each of those three arrows real.

---

# STEP 0 — Do not plug the television in

Not once, not "just to see". A set that has been switched off for decades
can destroy itself or start a fire on the first power-up, because the
capacitors inside have degraded and nobody has re-formed them slowly. And
the tube stores a lethal charge for a long time after it is unplugged, so
the back does not come off either — not by you, not ever.

**The television goes to a technician before it does anything else.** This
is the one job in the project you should not do yourself, and it is also the
job that decides whether the rest is worth doing. Everything else in this
guide can be done while the set is at the shop.

### Finding one

Search Swedish terms, not English: **"renovering rörradio"**, **"reparation
gammal TV"**, **"radiomuseum"**, **"antikradio"**. Vintage-radio collectors'
clubs will know who is still doing this — there are perhaps a few dozen
people in Sweden who can, and they are findable. Radiomuseum's Swedish
section and local *radiohistoriska* clubs are the way in.

### What to ask them for — copy this

> This is a DUX V6397 from the 1950s. It has not been powered on. I want to
> run it eight hours a day in a gallery, fed from a laptop, for several
> weeks.
>
> 1. Please recap it and bring it up slowly, so it is safe to leave running
>    unattended.
> 2. Is the chassis isolated from the mains? (The plate says *växelström*,
>    so I think there is a transformer, but please confirm with a meter.)
> 3. **Can you add a composite video input — a phono socket on the back that
>    goes straight into the video amplifier?** And an audio input to the
>    sound stage at the same time, if that is possible.
> 4. How is the picture tube's emission — how much life is in it?

Question 3 is the important one. Ask it early, because the answer changes
what you buy.

### Why question 3 changes everything — I am revising my own advice here

I first recommended keeping the set completely unmodified and feeding it
through its aerial socket with a professional modulator. That is the
purist's answer and I still think it is the right answer **for someone with
a workbench and RF experience**. You told me you are doing this alone and
are not technical, and that genuinely changes the recommendation.

|  | Aerial route (modulator) | AV input added by the technician |
|---|---|---|
| Cost | ~3 000 SEK box, plus balun and adapters | technician's time, on top of a recap you are paying for anyway |
| What you do | configure a headend modulator's menus, pick a VHF channel, set System B/G and 5.5 MHz sound, tune the TV's knob to find it, trim the level | plug the yellow plug in |
| Picture | soft — through a 70-year-old tuner | sharper, straight into the amplifier |
| Failure modes | drift, retuning, a wrong-standard purchase | none, really |
| The set | untouched, fully reversible | permanently modified |

**Take the AV input if the technician will do it.** You will be alone in a
gallery at eight in the morning with a picture that will not come up, and
the difference between one plug and a menu-driven RF box is the difference
between fixing it and closing the room. The cost of reversibility here is
paid in nights.

If the technician says no — some will, out of respect for the object — then
go back to `PICTURE_CHAIN.md` and buy the modulator, and budget a day to
learn it.

---

# STEP 1 — The three cables

## 1a. MacBook to HDMI

Your MacBook Pro (2016–2018, 15") has **four USB-C ports and nothing else**.
No HDMI socket. The cable you photographed is a charging cable — it carries
power, not video, and it will not do this job.

**Buy:** a *USB-C to HDMI adapter*. Any brand, ~200–400 SEK. Search
"USB-C till HDMI adapter". Get one that says **4K 60Hz** — not because you
need 4K, but because it means it is a proper active adapter rather than the
cheapest possible thing.

You do not need a hub. Three of your four ports get used, one each:

```
port 1  ⟶  power
port 2  ⟶  USB-C→HDMI adapter  ⟶  HDMI2AV box
port 3  ⟶  the dial's USB cable
port 4  ⟶  spare
```

## 1b. The HDMI2AV box — check one thing before you rely on it

**Look along the sides and the end of the box for a tiny switch marked
PAL / NTSC.** Take a photo of it and send it to me if you are unsure.

- **If there is a switch: set it to PAL.** European televisions are 50 Hz,
  American ones are 60 Hz, and this set will simply not lock onto NTSC — you
  will get a picture rolling endlessly up the screen and think the TV is
  broken when it is not.
- **If there is no switch anywhere**, the box may be NTSC-only, in which case
  it is no use here. Search "HDMI to AV converter **PAL**" and buy one that
  says PAL explicitly in the title. They are about 250 SEK. **Buy three.**
  They are the cheapest thing in the chain and the most likely to die.

The three plugs coming out are colour-coded: **yellow = picture**, **red and
white = sound**.

## 1c. Sound

You raised this yourself, and your instinct — that it is only a hum, so it
barely matters — is the one thing in your message I want to push back on.

It is not a hum. The bed was redesigned in the launch revision into a
composed drone with a real interval in it, breathing on the figure's cycle,
with falling whistlers through it. More to the point: **where a sound comes
from is part of what the object is**. Sound out of the television is the
television being alive. Sound out of a laptop on the floor is a laptop on
the floor, and every visitor will locate it instantly and stop believing the
set is doing anything.

In order of preference:

1. **Into the TV's own speaker.** Ask the technician for an audio input
   alongside the video one. Then red and white from the HDMI2AV box go
   straight in. This is the answer if you can get it.
2. **A small powered speaker hidden inside the cabinet.** ~500 SEK, a little
   amplifier module with a speaker, red/white RCA in, tucked behind the
   tube. The sound still comes out of the object. Nobody can tell.
3. **The MacBook's own speakers.** Only if the Mac ends up outside the
   cabinet. Inside a closed wooden box, facing down, it will be muffled and
   directionless, and the drone loses exactly the bottom end that makes it
   read as composed rather than as a fault.

Whatever you choose, judge the levels **through the actual speaker in the
actual room** and expect to change them more than feels reasonable. They are
labelled numbers in the AUDIO block of `visual/tv.html`.

---

# STEP 2 — The dial

This is the part you said you have no idea about, so here it is with nothing
assumed. It is also, honestly, the most satisfying afternoon in the project.

## What the parts are, in one line each

- **Raspberry Pi Pico** — a small circuit board, about the size of a stick of
  chewing gum, ~60 SEK. It plugs into the Mac by USB. Once it has the file I
  wrote on it, the Mac believes it is a keyboard. That is all it does: watch
  the dial, type digits.
- **Screw terminal expansion board** — a base plate the Pico sits into. It
  turns the Pico's tiny metal pins into little screw connectors, so wires go
  in with a screwdriver instead of a soldering iron.
- **Arduino Pro Micro** — ignore this for now. It is an alternative board.
  I wrote the same program for it so that if the Pico is out of stock or you
  break one, you are not stuck. You do not need it to start.

## Shopping list — dial

| What | Search for | Why exactly this |
|---|---|---|
| **Raspberry Pi Pico H** | "Raspberry Pi Pico H" — the **H** matters | The H version comes with its pins **already soldered on**. The plain one does not, and that is a soldering iron you do not want to own yet. |
| Screw terminal expansion board for Pico | "Pico screw terminal expansion board" | Pico plugs in, wires screw in. Zero soldering. |
| Micro-USB cable, ~2 m | "micro USB cable 2m" | The Pico uses micro-USB, not USB-C. Check the photos before you buy. |
| Cheap multimeter | "multimeter" (~150 SEK) | Only used on its beeping continuity setting, on a dial that is not plugged into anything. Nothing here is dangerous. |
| Small wire, or jumper wires with bare ends | "kopplingstråd" | Four short lengths. |

Order two Picos. They cost nothing and one lives in the drawer as the spare
the runbook refers to.

## Putting the program on the Pico — fifteen minutes

1. Go to **circuitpython.org/board/raspberry_pi_pico/** and download the
   `.uf2` file. This is the language the program is written in.
2. Hold down the small white **BOOTSEL** button on the Pico while you plug it
   into the Mac. A disk called **RPI-RP2** appears on your desktop, like a
   USB stick.
3. Drag the `.uf2` file onto it. The disk vanishes on its own and comes back
   named **CIRCUITPY**. That is normal — it means it worked.
4. Go to **circuitpython.org/libraries**, download the *Bundle for Version
   9.x*, unzip it, find the folder called **`adafruit_hid`** inside its `lib`
   folder, and copy that whole folder into the `lib` folder on CIRCUITPY.
5. Copy `firmware/pico-circuitpython/code.py` and
   `firmware/pico-circuitpython/boot.py` from this repo onto CIRCUITPY —
   loose in the main area, not in a folder.
6. Unplug the Pico and plug it back in. The little green light should blink
   three times. That is the program saying hello.

The CIRCUITPY disk will now stop appearing, on purpose — if it turned up on
the gallery machine it would open a Finder window over the television. To
get it back later, connect a wire between the pin labelled **GP15** and any
pin labelled **GND** while you plug the Pico in.

## Finding the two contacts on the dial

Use the **bench dial**, not the Ericsson. Its terminals are exposed screws,
which is why it was bought.

Set the multimeter to the setting with the **sound-wave / diode symbol** —
continuity. When you touch its two probes together it beeps. That is the
whole skill.

You are looking for two pairs of screws:

- **IMPULSE** — hold a probe on each of two screws, dial a number, and listen.
  The correct pair goes **beep-beep-beep** as the dial spins back, once per
  click. Dial 9 and you should hear ten beeps.
- **OFF-NORMAL** — a pair that goes **on when you pull the dial round and off
  again when it comes home**. One long beep per dial, not a series.

Write down which screws they were. Take a photo. You will need it again when
you move into the Ericsson.

## Wiring it — four wires, four screws

| From the dial | To the terminal board, screw marked |
|---|---|
| IMPULSE, either screw | **GP2** |
| IMPULSE, other screw | **GND** |
| OFF-NORMAL, either screw | **GP3** |
| OFF-NORMAL, other screw | **GND** |

Neither pair has a right way round — swap them if you like, it makes no
difference. If the board has only one GND screw free, both black wires can go
into it together.

### Do not skip the off-normal pair

Two extra wires, and here is what they buy. On a Swedish dial, **the number
zero is a single pulse**. So without the off-normal pair, any single stray
electrical blip — a dirty contact settling, interference from a television
with a mains transformer in it a metre away — types a **0**. Not an error
message: a zero, silently, into a stranger's birthdate, and the machine then
reads them the wrong day with total confidence and no one ever finds out.

With the off-normal pair wired, the program ignores the dial completely
except while it is actually being turned. The problem stops existing.

## Testing it

Plug the Pico into the Mac. Open TextEdit. Dial numbers. They should appear
in the document, correctly, every time. If they do:

- Dial each of 0 through 9 twenty times and read them back. All correct.
- Dial a birthdate you know, fast and carelessly.
- Then open ASTRA and dial it there.

**If the numbers are all wrong by one** — you dial 5 and get 4 — stop and
tell me. That is the Swedish pulse mapping and it is fixed in one line, but
it must be fixed before anything is screwed shut.

## Moving into the Ericsson — later

Only after the bench dial passes. Inside the phone's base you will find the
same two pairs of contacts, on the back of the dial mechanism. Same
procedure with the meter, same four wires, and **leave the phone's original
wiring connected and untouched** — the Pico just listens alongside it, so
the phone can go back to being a phone.

The USB cable leaves through the hole the telephone cord already uses. No new
holes in bakelite.

The handset does nothing, deliberately. It is scenery for now.

---

# STEP 3 — Putting it together

Only once the TV is back from the technician and the dial passes on the
bench.

1. TV on the floor where it will stand. Doors open.
2. Yellow plug from the HDMI2AV box into the TV's new video input.
3. Red and white into the audio input, or into the hidden speaker.
4. Mac connected: power, HDMI adapter, dial.
5. Set the Mac's screen resolution to **1024 × 768**. That is the shape the
   piece was designed at and it gives the converter the easiest possible job.
6. **First thing on the tube is the test card, not the piece.** Open
   `http://localhost:8000/testcard.html`. Photograph the screen. It tells you
   how much of the picture the tube actually shows and how small text can be
   before it disappears — measurements, instead of guessing.
7. Then, and only then, adjust `CONFIG.SAFE` and `CONFIG.TYPE_SCALE` at the
   top of `visual/tv.html` to match what you measured. Those two settings
   only. Everything else in that file is finished.
8. Heat: the TV draws 170 W and vents upward. The Mac goes **below** the tube
   chassis, never on top of it, never against the back panel, and nothing
   ever sits on the cabinet lid.

Then work through the acceptance test at the end of `exhibition/RUNBOOK.md`.

---

# The order, on one page

- [ ] **1.** Television to the technician. Ask the four questions. Do not
      power it on before then.
- [ ] **2.** While it is away: order the Pico H, the terminal board, the
      micro-USB cable, the multimeter, the USB-C→HDMI adapter.
- [ ] **3.** Check the HDMI2AV box for a PAL switch. Order PAL ones if not.
- [ ] **4.** Put the program on the Pico. Blinks three times.
- [ ] **5.** Find the contacts on the bench dial with the meter.
- [ ] **6.** Wire four wires. Dial into TextEdit. Then into ASTRA.
- [ ] **7.** Move the wiring into the Ericsson.
- [ ] **8.** Television comes back. Video and audio decided by then.
- [ ] **9.** Test card on the tube. Measure. Set the two CONFIG values.
- [ ] **10.** Sound levels judged in the room, through the real speaker.
- [ ] **11.** Ten cold boots. 24 hours with no phantom digits.

Steps 2 and 4–7 can all happen while the television is at the shop. That is
most of the build, and none of it needs the set.
