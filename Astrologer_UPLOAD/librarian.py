import json
from pathlib import Path
from datetime import datetime

# Tone: dry, witty, self-aware cosmic librarian (Douglas Adams-ish, not parody)
# Output: headline, omens, constraint, aside

TOKEN_MEANINGS = {
    "SUN_TRI_JUP": {
        "headline": "Optimism and purpose are unusually aligned.",
        "omens": [
            "Green lights appear where you expected bureaucracy.",
            "Confidence is earned, not inflated.",
            "Plans expand—but in a useful way."
        ],
        "constraint": "Don’t confuse luck with immortality. Still check the numbers."
    },
    "VEN_CON_SAT": {
        "headline": "Affection is wearing sensible shoes today.",
        "omens": [
            "Commitments become clearer (and less romantic, but more real).",
            "Boundaries feel attractive for all the wrong reasons.",
            "Quality beats quantity—especially in people and purchases."
        ],
        "constraint": "If it’s not sustainable, it’s not love; it’s a subscription."
    },
    "MER_TRI_JUP": {
        "headline": "Good thinking travels farther than usual.",
        "omens": [
            "Write the email. Make the call. Ask the smarter question.",
            "Learning is efficient; arrogance is not.",
            "If you teach, you’ll understand it twice."
        ],
        "constraint": "Don’t oversimplify. Big ideas still need footnotes."
    },
    "SUN_CON_MER": {
        "headline": "The mind is loud; the world is listening.",
        "omens": [
            "Your words land with extra weight—choose them carefully.",
            "Clarity is available if you stop multitasking for 90 seconds.",
            "Naming the thing makes it manageable."
        ],
        "constraint": "Avoid reactive hot takes. Precision beats velocity."
    },
    "MOO_SQR_JUP": {
        "headline": "Feelings want more than reality can sensibly provide.",
        "omens": [
            "Overpromising is emotionally tempting and strategically stupid.",
            "Indulgence has a persuasive PR team today.",
            "Your appetite may be symbolic; feed the right thing."
        ],
        "constraint": "Don’t solve discomfort with excess. It won’t stay solved."
    },
    "MOO_OPP_SAT": {
        "headline": "Emotion and responsibility are negotiating across a long table.",
        "omens": [
            "If you feel blocked, it may be timing—not failure.",
            "A firm ‘no’ can be a form of care.",
            "Structure helps the mood, even if the mood objects."
        ],
        "constraint": "Don’t punish yourself for having needs. Schedule them like meetings."
    },
}

def read_sky_state(path="sky_state.json"):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Can't find {path}. Run: python sky.py first.")
    return json.loads(p.read_text(encoding="utf-8"))

def uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out

def build_reading(sky):
    sig = sky.get("signature", [])
    planets = sky.get("planets", {})
    utc = sky.get("utc", "")

    # Collect candidate lines from tokens, in order.
    headlines = []
    omens = []
    constraints = []

    for t in sig:
        if t in TOKEN_MEANINGS:
            m = TOKEN_MEANINGS[t]
            headlines.append(m["headline"])
            omens.extend(m["omens"])
            constraints.append(m["constraint"])

    # Pisces stack special handling (your current sky)
    for t in sig:
        if t.startswith("STACK_"):
            # e.g. STACK_PISCES_4
            parts = t.split("_")
            if len(parts) >= 3:
                sign = parts[1].capitalize()
                count = parts[2]
                headlines.append(f"A noticeable {sign} concentration ({count} bodies): intuition up, boundaries negotiable.")
                omens.extend([
                    "Dream logic is persuasive; write things down before they evaporate.",
                    "Art and empathy spike; so does avoidance.",
                    "If you must escape, escape into craft."
                ])
                constraints.append("Don’t let ‘vibes’ run payroll. Translate feelings into actions.")

    headline = " ".join(uniq(headlines)[:2]) if headlines else "The sky is quiet in the way a library is quiet: full of opinions, none of them shouted."

    # pick 3 unique omens
    omens = uniq(omens)[:3] if omens else [
        "Small rituals beat grand resolutions.",
        "Be kind, but be specific.",
        "One useful action is worth ten symbolic ones."
    ]

    # pick strongest constraint
    constraint = uniq(constraints)[0] if constraints else "Do one thing properly. The universe respects craftsmanship."

    # Douglas-esque aside: tie to planets/signs for flavor
    sun = planets.get("Sun", {})
    moon = planets.get("Moon", {})
    aside = (
        f"Administrative note from the stacks: Sun in {sun.get('sign','?')} at {sun.get('degree','?')}° "
        f"and Moon in {moon.get('sign','?')} at {moon.get('degree','?')}°. "
        "Please return borrowed certainty by closing time."
    )

    # pretty timestamp
    try:
        dt = datetime.fromisoformat(utc.replace("Z", "+00:00"))
        stamp = dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        stamp = utc or "unknown time"

    return stamp, headline, omens, constraint, aside

def main():
    sky = read_sky_state()
    stamp, headline, omens, constraint, aside = build_reading(sky)

    print("\nCOSMIC LIBRARIAN — SKY READING")
    print(stamp)
    print("\nHeadline:")
    print(headline)
    print("\nOmens:")
    for o in omens:
        print(f"- {o}")
    print("\nConstraint:")
    print(constraint)
    print("\nAside:")
    print(aside)
    print("")

if __name__ == "__main__":
    main()