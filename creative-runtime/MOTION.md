# ASTRA — MOTION.md
Status: Creative Runtime pilot.

## Proposition
Motion implies physical laws. ASTRA does not animate to entertain; it behaves as though the machine and the phenomenon continue to exist between visitor actions.

## Motion classes
### Environmental
Slow, continuous, nearly autonomous. Orbital drift, membrane behaviour, signal fluctuation. It should not appear to wait for the user.

### Machine
Precise and procedural. State changes, acquisition, filing, cross-reference, reveal. Timing may feel administrative or ceremonial.

### Human feedback
Immediate enough to confirm input, quiet enough not to become conventional UI feedback.

## Timing character
- Slow is allowed.
- Stillness is allowed.
- Unequal pauses are allowed when they create ceremony.
- Reveals should feel received, developed, resolved or filed, not "animated in."
- Prefer fades, accumulation, drawing, scanning, phase changes and signal emergence over slides and pops.

## Prohibitions
- no bounce
- no springy product-UI motion
- no gratuitous parallax
- no hover theatre
- no constant movement everywhere
- no loading-spinner language unless the machine genuinely needs it
- no animation whose only rationale is that the library makes it easy

## Implementation
The installation currently ships dependency-free. Do not add Motion or another animation framework merely because this Runtime references Motion as a general SWG capability. Native CSS/canvas timing is preferred until a concrete need justifies a dependency.

## Test
Mute all copy and watch the ceremony. Does the timing alone suggest observation → acquisition → interpretation → release?
