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

# Corpus per ASTRA_MIND_v0.1: each mode carries multiple verbs, omens built
# on the Adams operations (bathos, specificity, escalation, swerve,
# understatement, institutional pathos), and several constraints. Selection
# is seeded — stable for a given visitor-day, different across them.

ASPECT_MODES = {
    "Conjunction": {
        "verbs_one": [
            "is sharing a desk with",
            "has moved its things onto the desk of",
            "is standing unreasonably close to",
            "has merged, without consultation, with",
        ],
        "verbs": [
            "are sharing a desk today",
            "have merged for the day, pending review",
            "are occupying the same office and pretending this is normal",
            "have been issued a single chair between them",
        ],
        "omens": [
            "Two departments have merged for the day. Their filing systems have not.",
            "What one wants and what the other notices are currently indistinguishable. The archive has stapled the two reports together and hopes no one asks which is which.",
            "There is one chair. Both departments believe it is theirs. Minutes are being kept.",
            "The merger was not announced. Mergers of this kind never are. One simply arrives to find the nameplates changed.",
            "Expect the day's business to arrive pre-combined, like a form printed on both sides without warning.",
        ],
        "constraints": [
            "Proximity is not the same as agreement. The sky files them separately.",
            "What has merged today will unmerge on schedule. The schedule is not published.",
            "Shared desks produce either partnerships or incidents. The archive stocks forms for both.",
        ],
    },
    "Opposition": {
        "verbs_one": [
            "is negotiating across a long table with",
            "has taken the seat directly opposite",
            "is maintaining formal correspondence with",
            "has tabled a counter-proposal against",
        ],
        "verbs": [
            "are negotiating across a long table",
            "have taken opposite ends of a very long table",
            "are in formal correspondence, copies filed",
            "have agreed to disagree, in writing, in triplicate",
        ],
        "omens": [
            "Both parties are correct. This is the inconvenient kind of correct.",
            "The table between them is long, polished, and older than either position. It has heard worse.",
            "Negotiations continue. Refreshments were requested in 1997. They are expected shortly.",
            "The distance between the two positions is the actual subject of the meeting. Nobody has said this aloud. Everybody knows.",
            "Correspondence is being exchanged at great speed and enormous length. The archive summarizes: both of them miss the point, beautifully.",
        ],
        "constraints": [
            "A tension held properly is load-bearing. Dropped, it is only noise.",
            "The archive does not resolve oppositions. It seats them facing each other and takes minutes.",
            "Neither end of the table is going to move. The table, however, can be walked around. This is mentioned in no manual.",
        ],
    },
    "Trine": {
        "verbs_one": [
            "is cooperating, unprompted, with",
            "has quietly done a favor for",
            "is on unexpectedly good terms with",
            "has waved through the paperwork of",
        ],
        "verbs": [
            "are cooperating without being asked",
            "are on suspiciously good terms today",
            "have waved each other through without inspection",
            "are, for once, not the problem",
        ],
        "omens": [
            "Something works today that usually requires supervision.",
            "No memo was sent. The thing happened anyway. Several supervisors are quietly unsettled by this.",
            "The gears have aligned. The archive wishes to note that nobody oiled them. They simply chose to.",
            "A door that normally sticks has opened at a touch. Do not stand there admiring the hinge.",
            "Approvals are moving through the system faster than the system was designed to allow. Enjoy this. Do not audit it.",
        ],
        "constraints": [
            "Ease is pleasant and teaches nothing. Enjoy it anyway.",
            "Days like this are not owed to you. They are lent. See the standard terms.",
            "When the machine runs smoothly, the temptation is to add more machine. Resist this.",
        ],
    },
    "Square": {
        "verbs_one": [
            "is filing complaints about",
            "has raised a structural objection to",
            "is disputing the corridor rights of",
            "has scheduled a grievance hearing with",
        ],
        "verbs": [
            "are filing complaints about each other",
            "have raised structural objections, each about the other",
            "are disputing the same corridor",
            "have escalated the matter to a committee that does not exist",
        ],
        "omens": [
            "The friction is structural, not personal. It may still feel personal. Structures are like that.",
            "Two departments want the same corridor today. Neither will use it once they have it. This is standard.",
            "A structural objection has been raised. It has been logged with the other four thousand.",
            "Neither party will yield, and something useful is being machined between them. Machining is loud. Wear what protection you have.",
            "The grievance is genuine, ancient, and procedurally perfect. Nobody remembers the original incident. The complaint form remembers.",
        ],
        "constraints": [
            "What grinds today is being shaped into something. The sky has not said what.",
            "Friction is the archive's oldest supplier. Its invoices are always paid, eventually, by someone.",
            "You may pick a side if you like. The corridor does not care. The corridor has seen committees come and go.",
        ],
    },
    "Sextile": {
        "verbs_one": [
            "is exchanging polite memos with",
            "has extended a modest invitation to",
            "is holding a door, pointedly, for",
            "has left a note in the pigeonhole of",
        ],
        "verbs": [
            "are exchanging polite memos",
            "are circulating a modest proposal",
            "have opened a side door and are standing near it meaningfully",
            "are being courteous in a way that implies homework",
        ],
        "omens": [
            "An opportunity exists. It is small, well-labeled, and easily ignored. Most are.",
            "The door is not locked. The archive would like to know who keeps suggesting it should be.",
            "A note has been left where you will find it. Finding it is, technically, your department.",
            "The invitation is real but modest, like a biscuit offered at a serious meeting. Take the biscuit.",
            "Somewhere, a small door has been propped open with a wedge of folded paper. The paper is a form. The form was always going to end up doing this.",
        ],
        "constraints": [
            "Doors that open quietly still require walking through.",
            "Opportunities of this size are not announced twice. The second announcement is called regret.",
            "The archive files unclaimed invitations under 'evidence.' Evidence of what is a question for later.",
        ],
    },
}

# Marginalia — the librarian's own notes, precedents, and incidents. One is
# folded into most readings; this is where the archive's history and mild
# suffering show through (institutional pathos, per ASTRA_MIND).
MARGINALIA = [
    "A similar configuration occurred in October 1962. The archive prefers not to elaborate.",
    "Precedent exists. Precedent always exists. That is the trouble with precedent.",
    "Form 30-B (Request for Clarity) remains available at the front desk. None has ever been approved.",
    "The margin of your file contains a note in pencil. It says: 'again?'",
    "An asterisk has followed this entry since 1994. Its referent has been lost. The asterisk remains vigilant.",
    "Regulation 7 forbids the archive from saying 'we told you so.' Regulation 7 is tested daily.",
    "Three previous visitors asked the sky to be more specific. Their requests were filed under 'optimism.'",
    "The relevant drawer sticks in humid weather. Today it opened at once. Draw what conclusions you must.",
    "The Department of Outcomes has declined to comment. This is itself a comment, and has been filed as one.",
    "Your file was consulted once before. The date stamp is smudged. The archive apologizes for the previous librarian, in general.",
    "A biro has gone missing from the annotations desk. This has no bearing on your reading. It is simply where the archive's attention is.",
    "The catalogue lists today's configuration as 'seen previously.' The catalogue lists everything as 'seen previously.' It has been right so far.",
    "Someone has dog-eared a page of your file. It was not the librarian. The librarian uses bookmarks.",
    "The ledger for days like this is kept on the high shelf, which is understood to be a statement.",
    "There was an incident in 1977 involving a comparable sky and a dinner party. The file is sealed. The tablecloth was not recovered.",
]

def _pick(pool, seed, salt=0):
    if not pool:
        return None
    return pool[(seed * 31 + salt * 7) % len(pool)]

def compose_from_aspect(aspect: dict, seed: int = 0):
    """Build a reading fragment from a single aspect dict (sky_state format).
    The seed selects among verb/omen/constraint variants — stable for a
    given day/sign/visitor, different across them."""
    mode = ASPECT_MODES.get(aspect.get("type"))
    if not mode:
        return None
    p1, p2 = aspect.get("planet1"), aspect.get("planet2")
    d1, d2 = PLANET_DESK.get(p1), PLANET_DESK.get(p2)
    if not d1 or not d2:
        return None
    verb = _pick(mode["verbs"], seed, 1)
    headline = f"{d1[0].upper()}{d1[1:]} and {d2} {verb}."
    n = len(mode["omens"])
    i = (seed * 31 + 14) % n
    j = (i + 1 + (seed % max(1, n - 1))) % n
    if j == i:
        j = (i + 1) % n
    omens = [mode["omens"][i], mode["omens"][j]]
    constraint = _pick(mode["constraints"], seed, 4)
    return headline, omens, constraint

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

# Second-person notes per aspect mode — used when a transit addresses the
# visitor directly. Two variants each; selection is seeded by birthdate so
# two visitors with the same transit type still hear different sentences.
TRANSIT_NOTES = {
    "Conjunction": [
        "Expect the theme to sit unusually close today. It has taken your chair.",
        "It will be difficult to tell where the day ends and you begin. File carefully.",
        "This is not a visit. The department has brought its own nameplate and a small plant. Plan accordingly.",
        "You are, for the duration, the office in question. The archive recommends tidying the desk you actually are.",
    ],
    "Opposition": [
        "The pull you feel is not indecision. It is geometry.",
        "Someone across the table holds the other half of this. Possibly it is also you.",
        "You have been seated at one end of a very long table. The correct posture is upright and amused.",
        "Whatever stands opposite you today is not an enemy. It is a counterweight, and you are the other one.",
    ],
    "Trine": [
        "The door is already open. Your only task is to notice.",
        "Today, competence will look suspiciously like luck. Accept the accounting error.",
        "The paperwork has gone through before you finished filling it in. Do not report this. Use it.",
        "Something in your vicinity is working on your behalf without being asked. The archive suggests gratitude, silently performed.",
    ],
    "Square": [
        "The resistance is precisely fitted to you. Treat it as tailoring.",
        "What blocks you today is load-bearing. Lean on it; do not kick it.",
        "The obstacle has your name on it — spelled correctly, which should tell you how long it has been planned.",
        "You will want to file a complaint. The complaint window is, today, the mirror. This is noted without cruelty.",
    ],
    "Sextile": [
        "A modest opening, addressed to you by name. RSVP optional.",
        "The sky is offering. It will not offer twice in the same tone.",
        "A side door stands open at roughly your height. Coincidences of this kind are rarely coincidences and never doors.",
        "The invitation is small enough to fit in a coat pocket, which is where such things are usually lost. Check the pocket.",
    ],
}

def compose_transit(planet, aspect_type, target="Sun", variant=0):
    """One personal line about a current planet aspecting the visitor's
    natal Sun or Moon. Same voice, same parts bin as the composed layer."""
    mode = ASPECT_MODES.get(aspect_type)
    desk = PLANET_DESK.get(planet)
    if not mode or not desk:
        return None
    verb = _pick(mode["verbs_one"], variant, 3)
    line = f"{desk[0].upper()}{desk[1:]} {verb} your natal {target}."
    notes = TRANSIT_NOTES.get(aspect_type, mode["omens"])
    return {"line": line, "note": notes[variant % len(notes)]}


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


def _leads_for_rulers(rulers, sig, aspects, seed=0):
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
            c = compose_from_aspect(a, seed=seed)
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
    try:
        day_seed = int(datetime.fromisoformat(
            sky.get("utc", "").replace("Z", "+00:00")).strftime("%j"))
    except Exception:
        day_seed = 0

    out = {}
    for sign, t in SIGN_TEMPERAMENT.items():
        rulers = SIGN_RULERS[sign]
        sign_idx = sign_order.index(sign)
        headline, omens, constraint = base_headline, list(base_omens), base_constraint

        # Candidate stories from the ruler's day, best-first. Ruler-twins
        # (Taurus/Libra, Gemini/Virgo) take DIFFERENT candidates from the
        # same list, so they only converge when the ruler has exactly one
        # aspect all day.
        # per-sign, per-day seed: variants rotate daily AND differ by sign
        s_seed = day_seed * 13 + sign_idx
        cands = _leads_for_rulers(rulers, sig, aspects, seed=s_seed)
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
            # the librarian's marginal note — most readings carry one
            if n and s_seed % 3 != 0:
                omens = omens[:2] + [_pick(MARGINALIA, s_seed, 9)]
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

    try:
        day_seed = int(datetime.fromisoformat(utc.replace("Z", "+00:00")).strftime("%j"))
    except Exception:
        day_seed = 0

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
                composed = compose_from_aspect(a, seed=day_seed)
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
