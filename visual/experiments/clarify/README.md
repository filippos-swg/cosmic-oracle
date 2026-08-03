# Experiment: the clarification dial

**Status:** sandbox tip — includes found-items + mono type + sound.
Production tv.html untouched. Response to the friends-feedback round
(too abstract / repetitive / "not an actual horoscope").

## What changed in the ceremony

After the FILE card, the archive asks its question:

    ONE CLARIFICATION IS REQUIRED
    DIAL 1 — THE MATTER OF WORK
    DIAL 2 — THE MATTER OF LOVE
    DIAL 3 — THE OTHER THING

The choice shapes everything after it: transits are re-ranked so planets
governing the chosen domain lead (Saturn/Mars/Jupiter/Mercury for work,
Venus/Moon/Mars/Neptune for love, Moon/Neptune/Pluto/Uranus for the other
thing); the lead transit's note becomes a LANDING sentence that translates
the metaphor into the visitor's life exactly once ("In practical terms —
the archive apologizes for practical terms — ..."); and the reading closes
with THE VERDICT: one plain, takeable sentence, time-bounded by real
astronomy ("This holds until the Moon leaves Virgo — Wednesday, in the
afternoon." — computed from the Moon's live position and speed), followed
by FOR THE RECORD (auspicious shelf / unfavorable form / color of the day).
An undecided visitor is decided for after 25s: "THE ARCHIVE HAS CHOSEN FOR
YOU. IT USUALLY DOES."

The balance rule (per discussion): the body stays enigmatic; every unit
touches "you"; ONE landing sentence per unit names the domain; the verdict
closes plainly. Roughly 70% visitor-directed, up from ~40%.

## Server change

/natal now returns up to 6 transits (was 3) so domain filtering has
material. Panels display the top 3.

## Try it

    http://localhost:8000/experiments/clarify/tv.html

Dial a date, advance past the FILE card (or wait), dial 1/2/3.
M mutes, P previews the ending, Esc abandons.

## Content locations (for editing/expansion)

All in this file's script, clearly labeled: DOMAINS, LANDING_FRAMES,
LANDINGS (domain x aspect-mode x 2), VERDICTS (domain x aspect-mode x 2),
RECORD_FORMS/RECORD_COLORS, moonDeadline(). Next session's planned work:
batch-expand LANDINGS/VERDICTS pools and add day-level no-repeat
allocation across signs.
