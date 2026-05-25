import json
from pathlib import Path
from datetime import datetime

# Voice: self-aware cosmic librarian
# Tone: dry, observational, archival — Douglas Adams as restraint, not imitation
# Rules: implication over instruction, observation over advice, no imperatives, no coaching

# ---------------------------------------------------------------------------
# Token interpretation table
# ---------------------------------------------------------------------------

TOKEN_MEANINGS = {

    "SUN_TRI_JUP": {
        "headline": "The sky is in an unusually cooperative mood.",
        "omens": [
            "Green lights appear where you expected bureaucracy.",
            "Confidence arrives without the usual paperwork.",
            "The gap between intention and consequence has narrowed slightly.",
        ],
        "constraint": "Luck and immortality remain separate categories. The numbers still apply.",
    },

    "VEN_CON_SAT": {
        "headline": "Affection is wearing sensible shoes today.",
        "omens": [
            "What seemed provisional now appears to be load-bearing.",
            "Boundaries feel attractive for all the wrong reasons.",
            "The romantic and the practical are sharing an office. Neither is thrilled.",
        ],
        "constraint": "If it is not sustainable, it is not love. It is a subscription.",
    },

    "MER_TRI_JUP": {
        "headline": "Ideas are moving through the atmosphere with unusual ease.",
        "omens": [
            "The gap between thinking and saying seems narrower than usual.",
            "A broader frame is available, should you require one.",
            "The system appears to reward precision today. The system's motives remain unclear.",
        ],
        "constraint": "Large ideas still require small, careful acts. The sky does not do the footnotes.",
    },

    "SUN_CON_MER": {
        "headline": "Thinking and being are currently sharing the same frequency.",
        "omens": [
            "Whatever is said today lands further than intended, in most directions.",
            "Articulation is possible. This is rarer than the literature suggests.",
            "The thing that has not been named is waiting.",
        ],
        "constraint": "What is said today tends to persist. The sky has noted this without comment.",
    },

    "MOO_SQR_JUP": {
        "headline": "Feelings want more than reality can sensibly provide.",
        "omens": [
            "Indulgence has a persuasive PR team today.",
            "The scale of things may be slightly off. The error is on the generous side.",
            "Enthusiasm and accuracy are not the same variable.",
        ],
        "constraint": "The appetite is rarely wrong about what it wants. It is occasionally wrong about quantities.",
    },

    "MOO_OPP_SAT": {
        "headline": "Emotion and responsibility are negotiating across a long table.",
        "omens": [
            "What feels like resistance may simply be architecture.",
            "The structure was always there. Today it is more visible.",
            "Warmth and form are not natural allies. Today they are in the same room.",
        ],
        "constraint": "The sky does not apologize for its load-bearing walls.",
    },

}

# ---------------------------------------------------------------------------
# Planetary stack: element-aware prose
# ---------------------------------------------------------------------------

# Signs grouped by element — used to select appropriate stack language
ELEMENTS = {
    "fire":  {"Aries", "Leo", "Sagittarius"},
    "earth": {"Taurus", "Virgo", "Capricorn"},
    "air":   {"Gemini", "Libra", "Aquarius"},
    "water": {"Cancer", "Scorpio", "Pisces"},
}

STACK_BY_ELEMENT = {
    "fire": {
        "headline": "The sky is running warm. Momentum is available; direction is the open question.",
        "omens": [
            "Something that has been waiting gains speed. Whether it was ready is a separate matter.",
            "Decisiveness arrives in quantity. The accuracy of the decisions varies.",
            "The system is running hot. This is either very useful or the beginning of a maintenance issue.",
        ],
        "constraint": "The fire does not ask permission. It does, however, appreciate containment.",
    },
    "earth": {
        "headline": "The material world has arranged itself into a clear argument.",
        "omens": [
            "Practicality and its associates are running the meeting.",
            "What can be touched, measured, or verified feels more real. The rest feels like weather.",
            "The ground is more present than usual. Whether this is reassuring depends on the ground.",
        ],
        "constraint": "Stability is not the same as permanence. The rock was once something else.",
    },
    "air": {
        "headline": "The atmosphere is full of ideas. Most of them are looking for a surface to land on.",
        "omens": [
            "Communication moves quickly and arrives everywhere, including places not intended.",
            "Several good ideas are in circulation. Several less good ones are in the same circulation.",
            "The system is processing. Output is pending.",
        ],
        "constraint": "An idea that has not been tested is, technically, still a theory.",
    },
    "water": {
        "headline": "The emotional weather is unusually specific. Take notes.",
        "omens": [
            "Intuition is louder than evidence. This is sometimes the correct configuration.",
            "The boundary between yours and not-yours requires inspection.",
            "What surfaces today has been waiting some time to do so.",
        ],
        "constraint": "Depth is a quality. It is not, by itself, a plan.",
    },
}

# ---------------------------------------------------------------------------
# Aside: rotating daily closings
# ---------------------------------------------------------------------------

ASIDE_CLOSINGS = [
    "Please return borrowed certainty by closing time.",
    "The catalogue has been updated. Proceed accordingly.",
    "Your reading is complete. The sky will continue without you.",
    "This concludes today's atmospheric report. The sky has returned to its standard opacity.",
    "Filed under: today. Cross-referenced with everything else.",
    "The stacks remain open. The librarian has noted your visit.",
    "All readings are approximate. The sky accepts no liability.",
]

# ---------------------------------------------------------------------------
# Core reading assembly
# ---------------------------------------------------------------------------

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
    sig     = sky.get("signature", [])
    planets = sky.get("planets", {})
    utc     = sky.get("utc", "")

    headlines   = []
    omens       = []
    constraints = []

    # Named token meanings
    for t in sig:
        if t in TOKEN_MEANINGS:
            m = TOKEN_MEANINGS[t]
            headlines.append(m["headline"])
            omens.extend(m["omens"])
            constraints.append(m["constraint"])

    # Planetary stack: element-aware
    for t in sig:
        if t.startswith("STACK_"):
            parts = t.split("_")
            if len(parts) >= 3:
                sign  = parts[1].capitalize()
                element = next(
                    (e for e, signs in ELEMENTS.items() if sign in signs),
                    "fire"  # fallback — should not occur with valid sign names
                )
                stack = STACK_BY_ELEMENT[element]
                headlines.append(stack["headline"])
                omens.extend(stack["omens"])
                constraints.append(stack["constraint"])

    # Fallbacks — used when no tokens match
    headline = (
        " ".join(uniq(headlines)[:2])
        if headlines
        else "The sky is quiet in the way a library is quiet: full of opinions, none of them shouted."
    )
    omens = uniq(omens)[:3] if omens else [
        "Nothing of note is being announced. This is not the same as nothing happening.",
        "The sky has filed its report. The contents are available on request.",
        "Ordinary time has its own texture, if you are patient enough to notice it.",
    ]
    constraint = (
        uniq(constraints)[0]
        if constraints
        else "The universe maintains its records regardless."
    )

    # Timestamp and rotating aside closing
    try:
        dt         = datetime.fromisoformat(utc.replace("Z", "+00:00"))
        stamp      = dt.strftime("%Y-%m-%d %H:%M UTC")
        day_index  = int(dt.strftime("%j"))
        aside_close = ASIDE_CLOSINGS[day_index % len(ASIDE_CLOSINGS)]
    except Exception:
        stamp       = utc or "unknown time"
        aside_close = ASIDE_CLOSINGS[0]

    sun  = planets.get("Sun", {})
    moon = planets.get("Moon", {})
    def fmt_deg(p):
        d = p.get("degree", None)
        return f"{d:.2f}" if isinstance(d, (int, float)) else "?"
    aside = (
        f"Sun in {sun.get('sign', '?')} at {fmt_deg(sun)}°. "
        f"Moon in {moon.get('sign', '?')} at {fmt_deg(moon)}°. "
        f"{aside_close}"
    )

    return stamp, headline, omens, constraint, aside


# ---------------------------------------------------------------------------
# Standalone runner — reads sky_state.json directly
# ---------------------------------------------------------------------------

def main():
    sky = read_sky_state()
    stamp, headline, omens, constraint, aside = build_reading(sky)

    print("\nASTRA — SKY READING")
    print(stamp)
    print("\nHeadline:")
    print(headline)
    print("\nObservations:")
    for o in omens:
        print(f"- {o}")
    print("\nConstraint:")
    print(constraint)
    print("\nAside:")
    print(aside)
    print("")


if __name__ == "__main__":
    main()
