# Experiment: ceremonial typography

**Status:** sandbox — includes the found-items experiment, plus new type.
Production tv.html untouched.

Per the "Constant Mistakes" reference: the central voice splits into two
registers over the mono machine layer —

- **Cormorant** (light, engraved, letterspaced caps): kickers, headlines,
  observations, constraints — the librarian's pronouncements.
- **Great Vibes** (copperplate script): notes, stamps, and the found
  letters/dreams — the hand of the unknown author.
- **Courier Prime** (unchanged): everything instrumental — celestial log,
  natal panel, digits, data, badges. The machine stays a machine.

## Try it

    http://localhost:8000/experiments/type/tv.html

P previews the ending. Compare against /experiments/poet/tv.html (same
content, mono type) and /tv.html (production).

## Important: fonts are now SELF-HOSTED

visual/fonts/ contains woff2 files (from @fontsource, OFL license) served
locally — discovered during this experiment that the production page still
loads fonts from Google's CDN, which will FAIL on the offline gallery
MacBook. When merging (or regardless), swap production tv.html's Google
Fonts <link> for the @font-face block at the top of this file. The
testcard + dashboard should get the same treatment before install day.

## CRT note

Cormorant's hairline serifs at small sizes will suffer on the tube more
than Courier does — the big headline sizes here should survive, but judge
the .small (44px) observations on the real DUX via the test card before
committing to sizes.
