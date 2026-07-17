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
# Composed readings — fallback layer
#
# The curated TOKEN_MEANINGS table covers a handful of aspects. Most days,
# none of them are exact. Rather than falling through to the generic
# "quiet library" reading every time, this layer composes a reading from
# the tightest aspect involving a fast-moving planet. Same voice, assembled
# from parts: each planet is a department of the archive; each aspect type
# is a mode of inter-departmental relations.
# ---------------------------------------------------------------------------

PERSONAL_PLANETS = ["Moon", "Sun", "Mercury", "Venus", "Mars"]

PLANET_DESK = {
    "Sun":     "the self",
    "Moon":    "the emotional record",
    "Mercury": "the correspondence desk",
    "Venus":   "the department of affection",
    "Mars":    "the engine room",
    "Jupiter": "the office of expansion",
    "Saturn":  "the structural engineer",
    "Uranus":  "the department of surprises",
    "Neptune": "the fog archive",
    "Pluto":   "deep storage",
}

ASPECT_MODES = {
    "Conjunction": {
        "verb_one": "is sharing a desk with",
        "verb": "are sharing a desk today",
        "omens": [
            "Two departments have merged for the day. Their filing systems have not.",
            "What one wants and what the other notices are currently indistinguishable.",
        ],
        "constraint": "Proximity is not the same as agreement. The sky files them separately.",
    },
    "Opposition": {
        "verb_one": "is negotiating across a long table with",
        "verb": "are negotiating across a long table",
        "omens": [
            "Both parties are correct. This is the inconvenient kind of correct.",
            "The distance between the two positions is the actual subject of the meeting.",
        ],
        "constraint": "A tension held properly is load-bearing. Dropped, it is only noise.",
    },
    "Trine": {
        "verb_one": "is cooperating, unprompted, with",
        "verb": "are cooperating without being asked",
        "omens": [
            "Something works today that usually requires supervision.",
            "No memo was sent. The thing happened anyway.",
        ],
        "constraint": "Ease is pleasant and teaches nothing. Enjoy it anyway.",
    },
    "Square": {
        "verb_one": "is filing complaints about",
        "verb": "are filing complaints about each other",
        "omens": [
            "The friction is structural, not personal. It may still feel personal.",
            "Neither party will yield today. Something useful is being machined between them.",
        ],
        "constraint": "What grinds today is being shaped into something. The sky has not said what.",
    },
    "Sextile": {
        "verb_one": "is exchanging polite memos with",
        "verb": "are exchanging polite memos",
        "omens": [
            "An opportunity exists. It is small, well-labeled, and easily ignored.",
            "The door is not locked. It is, however, closed, and someone must still open it.",
        ],
        "constraint": "Doors that open quietly still require walking through.",
    },
}

def compose_from_aspect(aspect: dict):
    """Build a reading fragment from a single aspect dict (sky_state format)."""
    mode = ASPECT_MODES.get(aspect.get("type"))
    if not mode:
        return None
    p1, p2 = aspect.get("planet1"), aspect.get("planet2")
    d1, d2 = PLANET_DESK.get(p1), PLANET_DESK.get(p2)
    if not d1 or not d2:
        return None
    headline = f"{d1[0].upper()}{d1[1:]} and {d2} {mode['verb']}."
    return headline, list(mode["omens"]), mode["constraint"]

# ---------------------------------------------------------------------------
# Sign temperament layer — the visitor's natal sun sign as a filter.
# Per the brief's interpretation hierarchy, temperament outweighs all:
# it does not change what the sky says, it changes how the visitor
# should hold it. `address` opens their file; `lens` closes the reading.
# ---------------------------------------------------------------------------

SIGN_TEMPERAMENT = {
    "Aries": {
        "address": "Filed under ARIES. The folder is slightly singed.",
        "lens": "You will want to act on this immediately. The sky suggests reading to the end first.",
    },
    "Taurus": {
        "address": "Filed under TAURUS. The folder has not moved in some time.",
        "lens": "You will want this to stay as it is. The sky declines to promise that.",
    },
    "Gemini": {
        "address": "Filed under GEMINI. The folder is cross-referenced with everything.",
        "lens": "You will want to discuss this with someone. Possibly several someones. Possibly at once.",
    },
    "Cancer": {
        "address": "Filed under CANCER. The folder is kept close to the chest.",
        "lens": "You will feel this before you understand it. For you, that is the correct order.",
    },
    "Leo": {
        "address": "Filed under LEO. The folder has requested better lighting.",
        "lens": "You will want to be seen handling this well. Handling it well is the part that matters.",
    },
    "Virgo": {
        "address": "Filed under VIRGO. The folder has been annotated. Twice.",
        "lens": "You will notice the flaw in this reading. Noted. The flaw is load-bearing.",
    },
    "Libra": {
        "address": "Filed under LIBRA. The folder sits exactly between two shelves.",
        "lens": "You will want to weigh both sides. At some point, the scale must be read.",
    },
    "Scorpio": {
        "address": "Filed under SCORPIO. The folder is sealed. You sealed it.",
        "lens": "You will suspect there is more beneath this. There is. There always is.",
    },
    "Sagittarius": {
        "address": "Filed under SAGITTARIUS. The folder was found some distance from its shelf.",
        "lens": "You will want the larger meaning. Fine. Today's paperwork still applies.",
    },
    "Capricorn": {
        "address": "Filed under CAPRICORN. The folder is structurally sound.",
        "lens": "You will ask what this is useful for. Not everything is. Some of it is anyway.",
    },
    "Aquarius": {
        "address": "Filed under AQUARIUS. The folder is filed under a system of its own devising.",
        "lens": "You will want to improve the premise. The premise thanks you, and remains.",
    },
    "Pisces": {
        "address": "Filed under PISCES. The folder's edges are soft from handling.",
        "lens": "You will absorb more of this than intended. Please return what is not yours.",
    },
}

def compose_transit(planet, aspect_type, target="Sun"):
    """One personal line about a current planet aspecting the visitor's
    natal Sun or Moon. Same voice, same parts bin as the composed layer."""
    mode = ASPECT_MODES.get(aspect_type)
    desk = PLANET_DESK.get(planet)
    if not mode or not desk:
        return None
    line = f"{desk[0].upper()}{desk[1:]} {mode['verb_one']} your natal {target}."
    return {"line": line, "note": mode["omens"][0]}


# Rulerships (modern primary, traditional fallback where they differ).
# A sign's reading leads with what its ruling planet is doing today —
# real astrological logic, and it guarantees the twelve signs disperse
# across the day's sky instead of all hearing the same report.
SIGN_RULERS = {
    "Aries":       ["Mars"],
    "Taurus":      ["Venus"],
    "Gemini":      ["Mercury"],
    "Cancer":      ["Moon"],
    "Leo":         ["Sun"],
    "Virgo":       ["Mercury"],
    "Libra":       ["Venus"],
    "Scorpio":     ["Pluto", "Mars"],
    "Sagittarius": ["Jupiter"],
    "Capricorn":   ["Saturn"],
    "Aquarius":    ["Uranus", "Saturn"],
    "Pisces":      ["Neptune", "Jupiter"],
}

# For picking the FRESHEST aspect involving a ruler: prefer the hit whose
# other planet moves fastest (a Moon contact is news; Pluto-Neptune is
# geology). Lower rank = faster.
SPEED_RANK = {
    "Moon": 0, "Mercury": 1, "Venus": 2, "Sun": 3, "Mars": 4,
    "Jupiter": 5, "Saturn": 6, "Uranus": 7, "Neptune": 8, "Pluto": 9,
}

def _tok(planet):
    return planet.upper()[:3]

# Position of each sign within its shared-ruler group (Taurus 0 / Libra 1
# under Venus; Gemini 0 / Virgo 1 under Mercury; everyone else 0). Twins
# draw DIFFERENT stories from the same ruler's aspect list.
_GROUP_POS = {}
_seen_rulers = {}
for _s, _rl in SIGN_RULERS.items():
    _p = _rl[0]
    _GROUP_POS[_s] = _seen_rulers.get(_p, 0)
    _seen_rulers[_p] = _seen_rulers.get(_p, 0) + 1


def _leads_for_rulers(rulers, sig, aspects):
    """Ordered candidate leads for a sign's ruler(s): curated tokens first
    (best writing), then composed aspects freshest-first. Only falls through
    to the traditional ruler if the modern one has nothing at all."""
    for r in rulers:
        cands = []
        curated_pairs = set()
        for tok_name in sig:
            if tok_name in TOKEN_MEANINGS and _tok(r) in tok_name:
                m = TOKEN_MEANINGS[tok_name]
                cands.append(((m["headline"], list(m["omens"]), m["constraint"]), r))
                parts = tok_name.split("_")
                if len(parts) == 3:
                    curated_pairs.add(frozenset((parts[0], parts[2])))
        hits = []
        for a in aspects:
            p1, p2 = a.get("planet1"), a.get("planet2")
            if r in (p1, p2):
                if frozenset((_tok(p1), _tok(p2))) in curated_pairs:
                    continue  # already covered by a curated token
                other = p2 if p1 == r else p1
                hits.append((SPEED_RANK.get(other, 9), a.get("orb", 99), a))
        hits.sort(key=lambda h: (h[0], h[1]))
        for _, _, a in hits:
            c = compose_from_aspect(a)
            if c:
                cands.append((c, r))
        if cands:
            return cands
    return []


def build_sign_readings(sky):
    """One reading per sign, led by the sign's ruling planet.

    Per sign: (1) if a curated token involving the ruler matched today,
    its writing leads; (2) otherwise compose from the freshest aspect
    involving the ruler; (3) if the ruler is unaspected today, fall back
    to the shared day reading and say so. Temperament closes as before.
    Returns {sign: {address, governor, headline, omens, constraint,
    lens, aside}}."""
    stamp, base_headline, base_omens, base_constraint, aside = build_reading(sky)
    aspects = sky.get("aspects", [])
    sig = sky.get("signature", [])
    sign_order = list(SIGN_TEMPERAMENT.keys())

    out = {}
    for sign, t in SIGN_TEMPERAMENT.items():
        rulers = SIGN_RULERS[sign]
        sign_idx = sign_order.index(sign)
        headline, omens, constraint = base_headline, list(base_omens), base_constraint

        # Candidate stories from the ruler's day, best-first. Ruler-twins
        # (Taurus/Libra, Gemini/Virgo) take DIFFERENT candidates from the
        # same list, so they only converge when the ruler has exactly one
        # aspect all day.
        cands = _leads_for_rulers(rulers, sig, aspects)
        lead, used_ruler = (cands[_GROUP_POS[sign] % len(cands)]
                            if cands else (None, rulers[0]))

        desk = PLANET_DESK[used_ruler]
        governor = f"Your file is kept by {desk}."

        if lead:
            headline = lead[0]
            pool = uniq(list(lead[1]) + base_omens)
            n = len(pool)
            off = (sign_idx + _GROUP_POS[sign] * 2) % n if n else 0
            omens = [pool[(off + k) % n] for k in range(min(3, n))]
            constraint = lead[2]
        else:
            governor += f" {used_ruler} reports nothing unusual today."

        out[sign] = {
            "address":    t["address"],
            "governor":   governor,
            "headline":   headline,
            "omens":      omens,
            "constraint": constraint,
            "lens":       t["lens"],
            "aside":      aside,
        }
    return out

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

    # Composed layer — when no curated token matched, build a reading from
    # the tightest aspect involving a personal planet (aspects arrive
    # orb-sorted from sky.py, so the first match is the tightest).
    if not headlines:
        for a in sky.get("aspects", []):
            if a.get("planet1") in PERSONAL_PLANETS or a.get("planet2") in PERSONAL_PLANETS:
                composed = compose_from_aspect(a)
                if composed:
                    c_head, c_omens, c_constraint = composed
                    headlines.append(c_head)
                    omens.extend(c_omens)
                    constraints.append(c_constraint)
                break

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
