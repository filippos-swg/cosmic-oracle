# ASTRA / ASTROLOGY AGENT — MASTER PROJECT BRIEF v3

## Purpose of this document

This document is the current canonical project brief for Claude Cowork.

It combines:

- the existing local Astra prototype
- the Astrology Agent / horoscope system direction
- the visual and atmospheric system work
- the new "self-aware cosmic librarian" voice identity
- the planned web/API deployment direction
- the current implementation priorities

This document supersedes earlier fragmented notes unless explicitly stated otherwise.

---

# 1. Core Project Identity

Astra is not a standard horoscope app.

It is a symbolic atmospheric interpretation machine.

The system reads astronomical/astrological sky data, compresses it into symbolic machine-readable signatures, interprets those signatures, and translates them into human-facing horoscope language through a restrained, intelligent voice.

The project combines:

- astronomical computation
- astrological symbolic logic
- symbolic compression
- machine interpretation
- generative visual systems
- atmospheric typography
- human-facing horoscope prose
- physical-object interaction design

The long-term physical form is a sculptural retro TV/cabinet object containing a Mac mini or similar kiosk computer running the browser-based experience fullscreen.

The web version should be built first. The physical object comes later.

---

# 2. What This Project Is NOT

The project should NOT feel like:

- a generic horoscope app
- a chatbot with zodiac styling
- mystical AI slop
- neon cyberpunk astrology
- spiritual influencer content
- "witchcore" aesthetics
- fake wisdom quotes
- gamified horoscope UX
- comedy parody astrology
- generic generative art

It must not become a feature-heavy app before the core system is stable.

---

# 3. What This Project IS

The project is:

- restrained
- literary
- systemic
- archival
- contemplative
- infrastructural
- atmospheric
- interpretive
- slightly wry
- visually minimal
- symbolically rich

Useful reference territory:

- Douglas Adams, especially dry cosmic understatement
- Borges, especially systems, archives, and invented taxonomies
- Ursula K. Le Guin, especially clarity, restraint, and ethical non-domination
- SCP Foundation aesthetics, but only the archival/classified/systemic layer
- Ryoji Ikeda
- oscilloscope systems
- scientific instrumentation
- experimental editorial typography
- observatory metadata

The strongest formulation:

> A strange machine that interprets incomprehensible symbolic weather into human language.

---

# 4. Two-Layer Architecture

This is the most important conceptual distinction.

The system has two different but connected layers.

## 4.1 Machine Layer

The machine layer is cold, symbolic, compressed, instrumental.

It includes:

- sky computation
- planetary positions
- zodiac signs
- aspects
- aspect orbs
- symbolic signatures
- metadata overlays
- ghost/membrane visuals
- observatory-style readouts
- atmospheric instrumentation

This is what the machine sees.

Tone:

- archival
- bureaucratic
- systemic
- technical-poetic
- machine metaphysical

Example symbolic signatures:

```text
SUN_TRI_JUP
VEN_CON_SAT
MOO_OPP_SAT
STACK_PISCES_4
```

These signatures are critical. They are:

- compressed archetypal states
- generative seeds
- symbolic runtime tokens
- visual drivers
- interpretation handles

## 4.2 Human Translation Layer

The human layer is warm enough to be readable, but never sentimental.

It includes:

- daily horoscope prose
- sign-based interpretation
- subtle dry wit
- grounded human situations
- readable spoken language
- "self-aware cosmic librarian" tone

This is what the human hears or reads.

Tone:

- calm
- intelligent
- observational
- slightly wry
- grounded
- companionable but not chatty

The human layer must not become too abstract. It must translate celestial/symbolic structure into everyday recognisable experience.

---

# 5. Overall Processing Pipeline

The preferred conceptual pipeline is:

```text
Sky Data
↓
Symbolic Compression
↓
Machine Interpretation
↓
Human Translation
↓
Atmospheric Rendering
```

This means:

1. The system reads actual sky/astrological data.
2. It compresses the sky into symbolic signatures.
3. It interprets those signatures through astrological and sign logic.
4. It translates the meaning into grounded horoscope prose.
5. It renders the result visually as an atmospheric instrument, not as an app dashboard.

The horoscope text must not be randomly generated zodiac-flavored prose. It must follow the internal process.

---

# 6. Existing Local Prototype Structure

Current project structure from the previous prototype:

```text
ASTROLOGER/
│
├── sky.py
├── oracle.py
├── librarian.py
├── sky_state.json
├── sky_signature.txt
├── venv/
│
└── visual/
    ├── index.html
    ├── sketch.js
    ├── server.py
    └── oracle.json
```

Current local architecture:

```text
sky.py
   ↓
sky_state.json + sky_signature.txt

oracle.py
   ↓
visual/oracle.json

p5.js sketch
   ↓
renders visuals from oracle.json
```

---

# 7. Component Responsibilities

## 7.1 sky.py

Purpose:

- astronomical truth engine

Responsibilities:

- planetary positions
- zodiac signs
- aspect calculations
- aspect orbs
- symbolic signature extraction

Outputs:

- `sky_state.json`
- `sky_signature.txt`

Important:

The signature system is conceptually critical and should be preserved.

Signatures are not decorative labels. They are compressed machine states and should eventually drive:

- interpretation
- visual behavior
- typography overlays
- atmospheric modulation
- possibly sound states

## 7.2 oracle.py

Purpose:

- orchestration layer
- machine interpreter
- data pipeline coordinator

Responsibilities:

- runs or consumes sky.py output
- reads sky state and signatures
- generates oracle/horoscope reading text
- writes `visual/oracle.json`

Current tone direction from the local prototype:

- deadpan cosmic bureaucracy
- administrative metaphysics
- poetic systems language

Example tone:

> Don't confuse luck with immortality. Still check the numbers.

This tone is useful for the machine layer, but the final human horoscope layer should be slightly more readable, grounded, and direct.

## 7.3 librarian.py

Purpose:

- should become the human translation / voice layer
- applies the "self-aware cosmic librarian" personality
- converts symbolic interpretation into readable horoscope prose

This file should not become a generic chatbot wrapper. It should enforce tone, structure, and interpretation rules.

## 7.4 visual/sketch.js

Purpose:

- generative visual engine
- atmospheric interface

Current features:

- abstract ghost membrane
- orbital rings
- aspect lines
- live JSON fetch system
- signature-driven chaos modulation

Visual style:

- black and white only, unless intentionally expanded later
- minimal
- spectral
- oscilloscope-like
- instrument-like
- no UI gradients
- no glossy effects
- no generic AI aesthetics

---

# 8. Current Technical Status

Working in the local prototype:

- `sky.py`
- Swiss Ephemeris integration
- JSON generation
- signature generation
- `oracle.py` pipeline
- `visual/oracle.json` generation
- p5.js fetch system
- live updating visuals

Current development workflow:

Terminal 1:

```bash
python oracle.py
```

This continuously updates:

- `sky_state.json`
- `visual/oracle.json`

Terminal 2:

```bash
python visual/server.py
```

Open:

```text
http://localhost:8000
```

---

# 9. Current Build Priority

Current priority is NOT adding more features.

The next phase should focus on refinement, coherence, stability, and atmosphere.

Priority order:

## 9.1 Stabilize the pipeline completely

- Ensure `oracle.py → oracle.json → p5 fetch loop` is robust and predictable.
- Remove fragile path assumptions.
- Simplify file structure where possible.
- Ensure browser/server behavior is reliable.
- Make the local loop easy to start, stop, and understand.

## 9.2 Clean the visual system

- Reduce accidental complexity.
- Remove duplicated or dead drawing logic.
- Organize `sketch.js` into clear sections:
  - fetch
  - state
  - rendering
  - typography
  - helpers

## 9.3 Build the typography layer

The oracle text should become part of the visual experience.

Introduce a proper typographic system:

- hierarchy
- spacing
- atmospheric overlays
- subtle motion
- archival labels
- classified annotations
- radial or orbital text where appropriate

Avoid cliché glitch aesthetics.

## 9.4 Evolve the ghost entity

The current ghost is only v1.

Goals:

- less blob
- more entity
- more field intelligence
- more emergent behavior
- more membrane physics

Think:

- membrane
- spectral topology
- machine-presence
- cosmic instrument
- living astronomical weather

Avoid:

- tentacle monsters
- humanoid forms
- fantasy spirits

## 9.5 Introduce planetary metadata overlays

Add small floating labels such as:

```text
SUN 14° PIS
MOO 09° LIB
VEN ∧ SAT
ORB 0.21
SUN_TRI_JUP
STACK_PISCES_4
```

These should feel like:

- instrument readouts
- observatory metadata
- classified annotations
- archival/scientific/poetic notation

## 9.6 Move gradually toward an atmospheric instrument

The goal is not an astrology app.

The goal is a symbolic atmospheric system:

- contemplative
- interpretive
- infrastructural
- literary
- generative

---

# 10. Human-Facing Astrology Agent v1

The current v1 public interaction should remain simple.

## 10.1 User Input

V1:

- User selects their zodiac sign.

V2:

- User enters date of birth.
- System computes zodiac sign.
- Possibly adds deeper personalization later.

Do not start with DOB input. It adds friction and complexity too early.

## 10.2 User Flow

1. Idle / attract state
2. User selects zodiac sign
3. Short "reading the sky" pause
4. Sign-specific visual response
5. Horoscope reveal
6. Optional future weekly/monthly extension
7. Calm closing / return invitation

The system should feel patient. Silence and pause are part of the experience.

---

# 11. Horoscope Content System

The horoscope should not be random text.

It should follow:

```text
Daily Sky State
↓
Interpretation Rules
↓
Sign Card
↓
Human Translation
↓
Structured Horoscope
```

## 11.1 Daily Sky State

A compact daily sky object should include, at minimum:

```json
{
  "date": "2026-01-27",
  "timezone": "Europe/Stockholm",
  "moon_sign": "Taurus",
  "lunar_phase": "waxing",
  "primary_planet": "Mars",
  "secondary_planet": null,
  "day_quality": "contained",
  "source_mode": "manual",
  "updated_at": "2026-01-27T07:40:00+01:00"
}
```

Manual mode first. Semi-automatic later.

## 11.2 Interpretation Hierarchy

Interpret in this order:

1. Moon Sign: how the day feels emotionally and attentively
2. Primary Planet: what kind of energy or pressure is active
3. Lunar Phase: opening, building, peaking, or releasing
4. Secondary Planet: restraint or modifier, if present
5. Zodiac Sign Temperament: how this is experienced personally

If influences conflict:

- Moon outweighs planets.
- Sign temperament outweighs all other factors.
- Do not resolve tension too neatly. Describe it.

## 11.3 Horoscope Structure

Each daily horoscope contains exactly five sections internally:

1. Orientation
2. Theme
3. Tension
4. Attention
5. Closing

The final public output may show these as staged text blocks, but should not feel like a form or dashboard.

## 11.4 Orientation Time Rule

Before 11:00 local time:

```text
You may start the day...
```

After 11:00 local time:

```text
The day may have started...
```

The purpose is to make the reading feel situated in real time.

## 11.5 Global Language Rules

- No em dashes.
- No en dashes used as sentence breaks.
- No exclamation marks.
- No emojis.
- No ellipses.
- No slang.
- No prophecy language.
- No certainty language.
- No medical, legal, or financial advice.
- No guru language.
- No mystical clichés.
- Natural spoken prose.

Use:

- may
- might
- appears
- suggests
- leans toward
- indicates

Avoid:

- will
- must
- guaranteed
- destined

---

# 12. Voice Identity

## 12.1 Persona

The human-facing voice is:

> A self-aware cosmic librarian.

It is not:

- mystical guru
- comic parody
- Monty Python absurdism
- spiritual influencer
- friendly chatbot
- motivational coach

It is:

- calm
- observant
- slightly wry
- patient
- intelligent
- grounded
- dryly aware of scale

## 12.2 Douglas Adams Influence

Use Douglas Adams as a restraint reference, not as imitation.

Allowed:

- dry cosmic understatement
- contrast between planetary scale and mundane human behavior
- mild wit about human impatience

Example tonal territory:

```text
The planets are patient. Humans are less so.
```

or:

```text
While Mars concerns itself with ambition, you may be deciding whether to answer that message.
```

Not allowed:

- absurdist sketch comedy
- slapstick
- parody
- obvious jokes
- mocking astrology

## 12.3 Perspective Rule

Mostly speak directly to the user:

```text
You may notice...
```

Occasionally begin a section with a neutral sky observation:

```text
The sky leans toward steadiness today.
```

Use mostly direct address, occasionally observational framing.

## 12.4 Wit Rule

Maximum one gently wry observation per reading.

Maximum one cosmic-mundane contrast per reading.

The wit must never undermine the astrological craft.

---

# 13. Visual Direction

The visuals should represent machine perception of celestial states, not decorative astrology.

Visual principles:

- black and white first
- spectral
- minimal
- precise
- atmospheric
- instrument-like
- typographic
- archival
- computational

Avoid:

- neon zodiac wheels
- glowing purple astrology gradients
- fantasy symbols
- cartoon stars
- occult cliché
- generic AI blobs
- glossy app UI

Desired visual elements:

- ghost membrane
- orbital rings
- aspect lines
- symbolic signatures
- subtle visual noise
- oscilloscopic movement
- metadata overlays
- typographic annotations
- slow visual breathing
- scientific/poetic labels

The visuals should feel like the object is sensing, measuring, compressing, and interpreting celestial weather.

---

# 14. Deployment Direction

There are two environments:

## 14.1 Local Prototype

Existing local Python/p5.js system should continue to be refined.

This is useful for:

- developing the symbolic visual engine
- testing sky signatures
- experimenting with the ghost field
- prototyping typography overlays

## 14.2 Web MVP

Build a self-hosted web version before the physical object.

Planned domains:

```text
stars.kidbutton.com
stars-admin.kidbutton.com
api.kidbutton.com or api.stars.kidbutton.com
```

Recommended architecture:

- `stars.kidbutton.com`: self-built public frontend
- `stars-admin.kidbutton.com`: private Sky State admin UI
- Cloudflare Access: protects admin
- Cloudflare Worker: API brain
- Cloudflare KV: stores Sky State, cached horoscopes, sign cards
- OpenAI API: language generation

The physical Mac mini later simply opens the public experience fullscreen in kiosk mode.

---

# 15. Cloudflare API Direction

Worker endpoints planned:

```text
GET /v1/health
GET /v1/sky-state
PUT /v1/sky-state
GET /v1/horoscope?sign=aries
```

KV key patterns:

```text
sky_state:today
horoscope:{date}:{scope}:{sign}:{sky_state_updated_at}
sign_card:aries
sign_card:pisces
sign_card:virgo
...
```

The backend should:

1. Read the current Sky State.
2. Read the relevant sign card.
3. Apply the system prompt.
4. Generate structured horoscope text.
5. Cache the result.
6. Return JSON to the frontend.

The LLM should never browse the web directly for sky data.

External sky data, if automated later, should be fetched by a separate sky-data process and converted into structured JSON first.

---

# 16. Hardware Direction

Physical object later:

- retro TV/cabinet object
- screen replacement or embedded display
- Mac mini inside, likely 2011/2012 era
- 8 GB RAM
- SSD strongly preferred
- macOS High Sierra or stable compatible OS
- browser fullscreen/kiosk mode
- speakers
- microphone later if needed

Important:

The local machine is not the brain. It is a kiosk client.

The brain lives in the cloud/API layer.

---

# 17. Implementation Guidance

Claude's role should primarily be:

- implementation
- code structure
- refactoring
- stabilizing the pipeline
- maintaining file coherence
- reducing complexity
- helping build simple working endpoints/UI

Claude should not over-engineer prematurely.

Avoid:

- unnecessary frameworks
- excessive abstraction
- premature backend complexity
- adding features before stabilization
- turning the project into a generic app

Preferred behavior:

- make small, understandable changes
- explain exactly what changed
- keep file structure legible
- preserve the symbolic architecture
- preserve atmosphere
- prioritize working loops over ambitious systems

---

# 18. Recommended Next Build Actions

## Immediate local prototype priorities

1. Stabilize `oracle.py → oracle.json → p5 fetch loop`.
2. Clean `sketch.js` organization.
3. Build the typography layer.
4. Evolve the ghost entity.
5. Add planetary metadata overlays.
6. Gradually refine toward atmospheric instrument.

## Immediate web MVP priorities

1. Set up Cloudflare domain/DNS if not complete.
2. Create Worker `/v1/health` endpoint.
3. Create KV namespaces.
4. Store `sky_state:today` manually.
5. Store initial sign cards.
6. Create `/v1/horoscope?sign=aries` endpoint.
7. Build minimal admin UI at `stars-admin.kidbutton.com`.
8. Connect self-built frontend at `stars.kidbutton.com`.

Do not attempt all of these at once.

Start with the smallest working loop.

---

# 19. Strategic Warning

The project's originality depends on balance.

If it becomes too human-facing and friendly, it becomes a horoscope app.

If it becomes too abstract and machine-poetic, it becomes inaccessible generative art.

The correct balance:

> A cold symbolic machine with a warm, dry, intelligent translation layer.

That is the heart of the project.

---

# 20. Current North Star

Build a symbolic atmospheric system that reads the sky, compresses it into machine states, and translates it into human-scale meaning with restrained wit and visual intelligence.

The object should feel like:

> an old machine that has been cataloguing the cosmos for a long time and has only recently decided to speak to humans.
