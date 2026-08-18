# PICTURE CHAIN — Mac → DUX V6397

Phase B of `aios/tasks/TASK_hardware_installation.md`. The set is now
identified, so the standing rule ("do not buy conversion hardware before the
set is identified") is discharged.

> **⚠ RECOMMENDATION REVISED 2026-08-18 — read this before buying anything.**
>
> This document originally recommended the aerial route: leave the set
> completely unmodified and feed it through a professional VHF modulator.
> That is still the right answer for someone with a workbench and RF
> experience.
>
> It is **not** the right answer for a solo, non-technical build, which is
> what this is. The set needs a technician for recapping before it can run
> unattended anyway — so **ask that technician to add a composite video
> input, and an audio input, while it is open.** Then the entire chain
> becomes one yellow plug, there is no 3 000 SEK box to configure, no VHF
> channel to find, no System B/G menu, and nothing to drift at eight in the
> morning with a gallery about to open.
>
> The cost is that the set is permanently modified. That is a real loss and
> it is the reason the aerial route was chosen first. It is outweighed here.
>
> **`exhibition/BUILD_GUIDE.md` is now the document to follow.** Everything
> below is the reasoning, plus the fallback if the technician declines to
> modify the set.

---

## The set

**DUX TYP V6397** — Dux Radio AB, Stockholm. Teak cabinet, double doors,
rounded B&W CRT, splayed legs. Rear plate reads:

| | |
|---|---|
| Supply | 220 V **växelström** (AC only), 50 Hz |
| Consumption | 170 W |
| Antenna | **Z = 300 Ω** balanced screw terminals |
| Safety | Swedish "S" mark; `VARNING HÖGSPÄNNING` on the back panel |
| Tuner | multi-position channel selector on the front (right-hand knob) |

Two things follow from the plate, and both are load-bearing:

**"Växelström" means AC only, which means a mains transformer, which means
the chassis is almost certainly isolated** — not the live-chassis AC/DC
design that would make connecting a Mac to it genuinely dangerous. Treat
that as a strong indication, not a certificate. Have the technician confirm
chassis-to-mains isolation with a meter before anything from the Mac side is
bolted to it.

**300 Ω balanced antenna terminals, no AV input of any kind.** Everything
below exists to turn an HDMI signal into something those two screws accept.

## The standard it expects

Sweden broadcast **625-line CCIR System B** on VHF from 1956. So:

| | |
|---|---|
| Lines / field rate | 625 / 50 Hz interlaced |
| Vision modulation | negative |
| Sound | FM, **5.5 MHz** above the vision carrier |
| Channel width | 7 MHz |
| Bands | I (E2 48.25, E3 55.25, E4 62.25 MHz) · III (E5–E12, 175.25–224.25 MHz) |

This is the single most common way to waste money here: most cheap "AV to
RF" boxes are **UHF only** (ch 21–69) or **PAL I** (6.0 MHz sound, UK). This
set has no UHF tuner at all, and a 6.0 MHz box gives a picture with no
sound. **The modulator must cover VHF Band I/III and be set to System B/G
with a 5.5 MHz sound carrier.** Nothing else will do.

---

## The chain

```
MacBook Pro ─HDMI─▶ HDMI→composite (PAL 576i)
                        │ CVBS 1 Vpp / 75 Ω  +  L/R audio
                        ▼
              Terra MT47 agile modulator
              System B/G · 5.5 MHz sound · VHF ch E4 (62.25 MHz)
              output trimmed with its own 0…−20 dB control
                        │ 75 Ω coax
                        ▼
              75 Ω → 300 Ω balun
                        │ twin lead, short
                        ▼
              DUX  ANTENN  ⌷⌷   → tune the front knob to that channel
```

### Parts

| # | Part | Why this one | Approx. |
|---|---|---|---|
| 1 | **Terra MT47** agile DSB TV modulator | The reason the whole plan works: 45–84 MHz + 170–300 MHz + UHF, standards B/G (5.5), D/K (6.5), I (6.0), M/N (4.5) selectable, composite in 1 V/75 Ω, stereo audio in, 85 dBµV out with a 0…−20 dB trim, mains powered. Hotel-headend gear — designed to run for years untouched. | ~2 500–3 500 SEK |
| 2 | HDMI → composite converter, **PAL** | See the two options below. | 300 / 3 800 SEK |
| 3 | 75 Ω coax → 300 Ω balun | Passive, trivial, ~50 SEK. Buy two. | ~50 SEK |
| 4 | Inline 10 dB attenuator (75 Ω) | Insurance. The MT47's own trim should be enough, but a set expecting a rooftop aerial does not need 85 dBµV shoved into it. | ~80 SEK |
| 5 | Isolation transformer, ≥300 VA | For bench work on the TV, and cheap peace of mind in the cabinet. | ~800 SEK |
| 6 | Short 75 Ω patch coax, F/IEC adapters | Match the MT47's connector to the balun. | ~150 SEK |

### The one open choice — converter grade

**Consumer (≈300 SEK).** A Portta-class HDMI→CVBS box with a PAL/NTSC
switch. It works. It is also a €25 plastic box in a piece that must run
unattended for weeks. If you take this route, **buy three** — one in the
cabinet, one in the drawer, one to leave with whoever opens the room — and
verify it comes up in PAL after a power cut rather than defaulting to NTSC.
That last failure mode is the one that will bite: a cold boot after a power
cut, and the DUX shows rolling nothing.

**Broadcast (≈3 800 SEK).** Blackmagic **Mini Converter HDMI to SDI 6G** →
**Mini Converter SDI to Analog**, which outputs composite PAL 625i50 with a
proper HD→SD downconverter. Two boxes instead of one, both metal, both
designed for permanent installation, deterministic on power-up.

Honest read: the picture is going to be soft either way — it is a 70-year-old
B&W tube behind glass, and the tuner and IF strip will take more resolution
off it than any converter will. What you are actually buying with the
Blackmagic is **deterministic behaviour after a power cut**, which is the
thing that decides whether the piece survives a three-week exhibition
without you in the room. Start with the cheap box on the bench; decide after
you have watched it cold-boot twenty times.

### Mac side

- **Confirmed 2026-08-18: the appliance Mac is a 15" MacBook Pro, 2016–2018 —
  four USB-C / Thunderbolt 3 ports and nothing else.** No HDMI socket. A
  **USB-C → HDMI adapter** is required and is not yet owned; the 100 W USB-C
  cable already bought is power only. No hub needed: power, video and the
  dial take one port each and leave one spare.
- **Converter already owned: a Mini HDMI2AV box** (HDMI in, three RCA out).
  Usable *if* it has a PAL/NTSC switch set to PAL — this set is 625/50 and
  will never lock to NTSC's 525/60; the symptom is an endlessly rolling
  picture that looks like a dead television. If the box has no switch, it is
  NTSC-only and useless here: buy ones with PAL in the product title, and buy
  three, because it is the cheapest and most failure-prone link in the chain.
- Set the display to **1024 × 768** (4:3). That is exactly `tv.html`'s design
  space, so the converter's scaler has the simplest possible job and nothing
  gets letterboxed into the tube's already-cropped area.
- Do **not** let the converter or the Mac add overscan compensation. Overscan
  is what `CONFIG.SAFE` is for, and it must be measured on the tube, once.

---

## Bring-up order

Do not skip a step to see a picture sooner. Each step tells you which box is
lying to you.

1. **Service the set first.** 1950s paper and electrolytic capacitors, then
   eight hours a day in a closed cabinet. A recap and a dim-bulb bring-up by
   a technician, before it is ever left running unattended. Ask them at the
   same time for: chassis-to-mains isolation confirmed, which channels the
   tuner actually covers, and the state of the CRT's emission.
2. **Never open the back yourself.** A CRT holds a lethal charge for a long
   time after the plug comes out, and the EHT cap does not care that the set
   is unplugged. This is the one line in the project with a body count.
3. Modulator on the bench into a *modern* TV with an analog tuner, or a
   spectrum analyser if the technician has one. Confirm channel, System B/G,
   5.5 MHz sound. Do this before the DUX is anywhere near it.
4. Then the DUX, tuning the front knob across the band until the carrier
   appears. Trim the modulator's output down until the picture is clean
   without snow and without overload smearing.
5. **First page on the tube: `/testcard.html`.** Not the ceremony. Measure:
   true visible area, the corner mask, the smallest legible type size,
   whether 1 px horizontals shimmer on interlace.
6. Only then edit `CONFIG.SAFE` and `CONFIG.TYPE_SCALE` in `visual/tv.html`.
   Nothing else in that file. Commit the measured values with a note saying
   which set they were measured on.

## Sound

The MT47 carries audio on the 5.5 MHz subcarrier, so the TV's own speaker
plays the breathing bed and the drone — which is the right answer: the sound
should come out of the object, not out of a hidden speaker beside it.

Judge the redesigned bed **through that speaker**, not headphones. A 1950s
elliptical speaker in a wooden cabinet will eat the bottom of the drone and
exaggerate the whistler. The levels are labelled numbers in the AUDIO module
of `tv.html`; expect to move them, and expect the change to be larger than
feels reasonable on a laptop.

Verify `--autoplay-policy=no-user-gesture-required` survives in
`kiosk/astra-kiosk.sh` — without it the hum never starts and the piece is
silent, with no error anywhere to tell you why.

## Heat

170 W of valves plus a MacBook in a closed teak box. The tube chassis runs
hot and vents upward.

- Mac **below** the tube chassis, never above it, never against the back panel.
- Never block the cabinet's own vents, and never close the doors on a
  running set without leaving a rear air path.
- Leave it running for a full exhibition day with the doors as they will be,
  and put a hand on the cabinet top and on the Mac's underside at close.
  If either is uncomfortable, add a slow 120 mm fan on the Mac's intake side
  — quiet enough to lose under the drone.

---

## Sources

- [CCIR System B — Wikipedia](https://en.wikipedia.org/wiki/CCIR_System_B)
- [Television channel frequencies (CCIR Band I / III)](https://en.wikipedia.org/wiki/Television_channel_frequencies)
- [Terra MT47 — product page (B1+B3+UHF)](https://www.terraelectronics.com/product/tv-modulators-and-others/analog-tv-modulators/dsb-tv-modulators/dsb-tv-modulators/mt47/)
- [Terra MT41/MT47/MT57 manual — standards and level specs (PDF)](https://www.terraelectronics.com/uploads/Products/product_189/Manual.pdf)
- [Blackmagic Mini Converter SDI to Analog — composite PAL 625i50](https://www.blackmagicdesign.com/products/miniconverters/techspecs/W-CONM-01)
- [Dux Radio AB model index — Radiomuseum](https://www.radiomuseum.org/dsp_hersteller_detail.cfm?company_id=1979)
