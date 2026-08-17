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

    # --- added 2026-08-14 (language expansion) -----------------------------
    # Keys must follow sky.py's PLANETS declaration order — Sun, Moon,
    # Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto — because
    # build_signature() always emits the earlier planet first. A key written
    # the other way round (VEN_CON_SUN) never matches and dies silently.

    "SUN_CON_VEN": {
        "headline": "Being liked and being oneself have been filed under the same heading today.",
        "omens": [
            "What you want and what you will admit to wanting have stopped arguing.",
            "Charm is unusually available. Its uses are noted and not judged.",
            "Something you made is about to be seen. The archive saw it earlier and said nothing.",
        ],
        "constraint": "Being agreeable is a service, not an identity. The archive keeps files on the difference.",
    },

    "SUN_SQR_SAT": {
        "headline": "The self has been asked for its paperwork.",
        "omens": [
            "An old limit presents itself for renewal. It has not aged.",
            "What you intended and what is permitted are in different buildings today.",
            "Effort is required and will not be publicly credited. It is credited privately, which helps nobody.",
        ],
        "constraint": "Resistance of this grade is not opposition. It is the load test.",
    },

    "SUN_OPP_SAT": {
        "headline": "The self and the structural engineer have taken opposite ends of a long table.",
        "omens": [
            "Something you built is being inspected from the far end.",
            "The authority you are arguing with may have your signature on it.",
            "A decision made years ago has arrived to collect.",
        ],
        "constraint": "The archive does not recommend winning arguments with load-bearing walls.",
    },

    "SUN_SXT_MAR": {
        "headline": "The engine room has left a note for the self. It is short.",
        "omens": [
            "Energy is available in a modest, well-labelled quantity.",
            "A small act done today counts as a larger one, by an accounting nobody explains.",
            "Courage of the ordinary kind is in stock. The archive keeps it near the door.",
        ],
        "constraint": "Small applications of force are how large objects are actually moved. The archive holds the diagrams.",
    },

    "MOO_SXT_MER": {
        "headline": "The emotional record and the correspondence desk are, for once, using the same vocabulary.",
        "omens": [
            "A feeling finds its exact word today. This is rarer than the literature suggests.",
            "What you say about how you are will be nearly accurate.",
            "Something long felt becomes briefly sayable. The window is not wide.",
        ],
        "constraint": "Naming a thing does not dispose of it. It moves it to a shelf you can reach.",
    },

    "MOO_CON_VEN": {
        "headline": "The emotional record and the department of affection are sharing a chair, comfortably, which is unusual.",
        "omens": [
            "What comforts you and what attracts you have stopped being separate questions.",
            "Softness is operationally available. Use is discretionary.",
            "Something you like will like you back today, and say so awkwardly.",
        ],
        "constraint": "Pleasantness is not evidence. The archive requires more, and receives it later.",
    },

    "MOO_CON_SAT": {
        "headline": "The emotional record has been moved into the structural engineer's office. Neither was consulted.",
        "omens": [
            "Feeling arrives today wearing a coat and carrying a form.",
            "What is felt is also, unhelpfully, true.",
            "The mood has a reason, a date and a filing number.",
        ],
        "constraint": "Heaviness is not always sorrow. Sometimes it is mass, correctly reported.",
    },

    "MOO_SQR_MAR": {
        "headline": "The emotional record and the engine room are disputing the same corridor.",
        "omens": [
            "Irritation arrives early and stays for the meeting.",
            "What you feel wants doing immediately. The archive counsels an hour.",
            "The reaction is faster than the reason today. Both will be filed.",
        ],
        "constraint": "Heat is information. It is rarely also a plan.",
    },

    "MER_CON_VEN": {
        "headline": "The correspondence desk and the department of affection are drafting together. The results are legible and slightly warm.",
        "omens": [
            "What is said today lands softer than it looks on paper.",
            "A difficult message becomes possible if written now.",
            "Agreement is easier to reach than usual, and easier to mean.",
        ],
        "constraint": "Charm in writing is still writing. It keeps.",
    },

    "MER_SQR_SAT": {
        "headline": "The correspondence desk has been sent back for corrections.",
        "omens": [
            "A sentence written today will be read more carefully than intended.",
            "Thinking is slower and better. The archive prefers the second of these.",
            "Somebody senior disagrees on a technicality. The technicality is correct.",
        ],
        "constraint": "Precision is expensive, and always cheaper than the alternative.",
    },

    "MER_OPP_JUP": {
        "headline": "The correspondence desk and the office of expansion are exchanging documents of very different lengths.",
        "omens": [
            "The detail and the large picture have both been submitted. Only one of them fits.",
            "Something is being overstated today, sincerely and at length.",
            "A small correction improves a large claim. Nobody enjoys this.",
        ],
        "constraint": "Scale is not a substitute for accuracy. The archive has both departments on record.",
    },

    "VEN_SQR_MAR": {
        "headline": "The department of affection and the engine room have both requisitioned the evening.",
        "omens": [
            "Wanting and pursuing are out of step by a few hours today.",
            "Attraction arrives with a complaint attached.",
            "The disagreement is about pace. It always was.",
        ],
        "constraint": "Desire and haste are neighbours. The archive keeps them in separate drawers for a reason.",
    },

    "VEN_TRI_JUP": {
        "headline": "The department of affection and the office of expansion have approved each other without a meeting.",
        "omens": [
            "Generosity is inexpensive today, and does not feel like generosity.",
            "Something offered will be accepted, possibly too quickly.",
            "The pleasant thing is also, unusually, the correct thing.",
        ],
        "constraint": "Abundance has an end date. It is not printed on the abundance.",
    },

    "MAR_SQR_SAT": {
        "headline": "The engine room has been issued a stop notice by the structural engineer.",
        "omens": [
            "Effort meets a wall built specifically to be met.",
            "Progress today is measured in millimetres, and counts.",
            "Frustration is on schedule. It was in the plans.",
        ],
        "constraint": "Force applied to structure produces either a door or a lesson. The archive stocks paperwork for both.",
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
            "has annexed the in-tray of",
            "is finishing the sentences of",
            "has taken the only chair in the office of",
            "is signing the correspondence of",
            "has moved its filing cabinet against the door of",
            "is wearing the lanyard of",
        ],
        "verbs": [
            "are sharing a desk today",
            "have merged for the day, pending review",
            "are occupying the same office and pretending this is normal",
            "have been issued a single chair between them",
            "have adopted a single letterhead, provisionally",
            "are answering to one bell today",
            "have been assigned one telephone between them",
            "are initialling each other's memos",
            "have combined their in-trays, without asking",
            "are being invoiced as a single department",
        ],
        "omens": [
            "Two departments have merged for the day. Their filing systems have not.",
            "What you want and what you notice have become indistinguishable today. The archive has stapled the two reports together and hopes nobody asks which is which.",
            "There is one chair. Both departments believe it is theirs. Minutes are being kept.",
            "The merger was not announced. They never are. You simply arrive to find the nameplates changed.",
            "Expect the day's business to arrive pre-combined, like a form printed on both sides without warning.",
            "The two dockets have been fastened with the same clip. The clip is under strain. Clips of this class usually are.",
            "Nothing stands between what you intend and what follows from it today. The arrangement is efficient, and the archive distrusts it.",
            "For the duration, both matters answer to one bell. If you ring it, mean it.",
            "The two matters have been bound into one volume. The binding is new and slightly tight.",
            "A single stamp now covers both departments. Nobody has established whose it was.",
            "What arrives today arrives twice, in one envelope.",
            "The archive has stopped distinguishing between your two files. It is not certain it ever could.",
            "One desk, two nameplates, and a growing silence about which is on top.",
            "The proximity is total and nobody has mentioned it. Mentioning it is your department.",
        ],
        "constraints": [
            "Proximity is not the same as agreement. The sky files them separately.",
            "What has merged today will unmerge on schedule. The schedule is not published.",
            "Shared desks produce either partnerships or incidents. The archive stocks forms for both.",
            "What has joined you today is temporary. Temporary is not the same as insincere.",
            "A shared desk has one set of drawers. You will be sharing those too.",
            "A merger is not a marriage. The archive files them on different floors.",
            "What arrives with you today may still leave without you. Departures are not scheduled here.",
            "Whatever you put in one drawer today is found together later, whether or not it belongs together.",
        ],
    },
    "Opposition": {
        "verbs_one": [
            "is negotiating across a long table with",
            "has taken the seat directly opposite",
            "is maintaining formal correspondence with",
            "has tabled a counter-proposal against",
            "has opened proceedings against",
            "is holding the other end of the rope with",
            "has requested a hearing with",
            "is mirroring, badly, the position of",
            "has served notice on",
            "is standing at the far window from",
        ],
        "verbs": [
            "are negotiating across a long table",
            "have taken opposite ends of a very long table",
            "are in formal correspondence, copies filed",
            "have agreed to disagree, in writing, in triplicate",
            "are holding opposite ends of the same rope, politely",
            "have exchanged dossiers at dawn",
            "have booked the same room for opposing purposes",
            "are conducting a correspondence neither will read aloud",
            "have each appointed a representative, then attended anyway",
            "are keeping identical minutes of different meetings",
        ],
        "omens": [
            "Both parties are correct. This is the inconvenient kind of correct.",
            "The table between them is long, polished, and older than either position. It has heard worse.",
            "Negotiations continue. Refreshments were requested in 1997. They are expected shortly.",
            "The distance between the two positions is the actual subject. Nobody will say so. You already know.",
            "Correspondence is being exchanged at great speed and enormous length. The archive summarizes: both of them miss the point, beautifully.",
            "Each party has prepared a dossier on the other. The dossiers are, page for page, identical. Neither has noticed.",
            "A message crosses the table to you today and is read upside down. Your reply will be composed the same way. Progress, of a kind.",
            "The standoff is fully staffed and adequately funded. It could continue indefinitely. It usually declines to.",
            "The gap has been measured. It is exactly as wide as both parties need in order to be right.",
            "A concession was offered to you this morning and misfiled as an attack.",
            "Your position and theirs have begun to resemble each other. Neither of you would survive being told.",
            "There is a chair between them that nobody has sat in. It has been there since 1958.",
            "Both sides have asked the archive to adjudicate. The archive has taken minutes instead.",
            "You have achieved symmetry, which is regularly mistaken for progress.",
        ],
        "constraints": [
            "A tension held properly is load-bearing. Dropped, it is only noise.",
            "The archive does not resolve oppositions. It seats them facing each other and takes minutes.",
            "Neither end of the table will move. You can walk around it. This is mentioned in no manual.",
            "Perfect balance is not peace. It is two pressures agreeing to differ.",
            "The archive notes that long tables make honest mirrors.",
            "A table has two ends. It does not have two truths.",
            "Do not declare victory in a room with a mirror. You are standing in one.",
            "Hold it honestly and it is a structure. Hold it dishonestly and you are moving furniture.",
        ],
    },
    "Trine": {
        "verbs_one": [
            "is cooperating, unprompted, with",
            "has quietly done a favor for",
            "is on unexpectedly good terms with",
            "has waved through the paperwork of",
            "has pre-approved the requests of",
            "is smoothing the path of",
            "has countersigned everything belonging to",
            "is quietly covering the shift of",
            "has removed an obstacle from the corridor of",
            "is lending its stamp to",
        ],
        "verbs": [
            "are cooperating without being asked",
            "are on suspiciously good terms today",
            "have waved each other through without inspection",
            "are, for once, not the problem",
            "have synchronized without a meeting",
            "are passing each other the correct files, first time",
            "have arranged matters between themselves and told nobody",
            "are covering for each other, competently",
            "have agreed without correspondence",
            "are running ahead of their own paperwork",
        ],
        "omens": [
            "Something works today that usually requires supervision.",
            "No memo was sent. The thing happened anyway. Several supervisors are quietly unsettled by this.",
            "The gears have aligned. The archive wishes to note that nobody oiled them. They simply chose to.",
            "A door that normally sticks has opened at a touch. Do not stand there admiring the hinge.",
            "Approvals are moving through the system faster than the system was designed to allow. Enjoy this. Do not audit it.",
            "Traffic is flowing in the corridor that is normally a negotiation. No one is directing it. Do not look for the director.",
            "Whatever you send out today comes back approved, stamped and slightly warm. Spend it before somebody checks.",
            "Help reaches you before you ask for it, which is against procedure and extremely welcome.",
            "A form has arrived on your desk already completed. Enquiries as to by whom are discouraged.",
            "The corridor is clear in both directions. This has not happened since the renovation.",
            "Something is being done well by nobody in particular.",
            "The archive has nothing to report and finds itself, unusually, at ease.",
            "A window that sticks has opened. The building is old and occasionally generous.",
            "Consent has been given in advance for something you have not asked for yet.",
        ],
        "constraints": [
            "Ease is pleasant and teaches nothing. Enjoy it anyway.",
            "Days like this are not owed to you. They are lent. See the standard terms.",
            "When the machine runs smoothly, the temptation is to add more machine. Resist this.",
            "A favourable current is still water. It has its own opinion about where you are going.",
            "What flows easily today will be billed later at the ordinary rate. This is not a complaint. It is arithmetic.",
            "Grace is not a policy. It is a mood the building is in.",
            "Nothing you borrow this easily is remembered as borrowed. The archive remembers.",
            "An open door is an invitation, not an address. You still have to decide where you are going.",
        ],
    },
    "Square": {
        "verbs_one": [
            "is filing complaints about",
            "has raised a structural objection to",
            "is disputing the corridor rights of",
            "has scheduled a grievance hearing with",
            "has wedged its cabinet into the doorway of",
            "is contesting the budget of",
            "has withheld the signature of",
            "is auditing, with enthusiasm, the accounts of",
            "has scheduled roadworks outside the office of",
            "keeps returning the forms of",
        ],
        "verbs": [
            "are filing complaints about each other",
            "have raised structural objections, each about the other",
            "are disputing the same corridor",
            "have escalated the matter to a committee that does not exist",
            "are redrafting each other's conclusions",
            "have both requisitioned the same corridor, in ink",
            "have each declared the other out of order",
            "are investigating each other, in parallel",
            "have jammed the same door from opposite sides",
            "are drafting rival memoranda at speed",
        ],
        "omens": [
            "The friction is structural, not personal. It may still feel personal. Structures are like that.",
            "Two departments want the same corridor today. Neither will use it once they have it. This is standard.",
            "A structural objection has been raised. It has been logged with the other four thousand.",
            "Neither party will yield, and something useful is being machined between them. Machining is loud. Wear what protection you have.",
            "The grievance is genuine, ancient, and procedurally perfect. Nobody remembers the original incident. The complaint form remembers.",
            "The blockage has been inspected. It is genuine, well-made, and in precisely the wrong place — which is to say, precisely where it was designed to be.",
            "Both departments have submitted the same complaint about each other, word for word. The clerk filed them face to face, for symmetry.",
            "You will work against resistance today. It is the only kind of work the archive has seen produce anything with edges.",
            "The friction has been logged, quantified and left exactly where you found it. It is doing something.",
            "Two correct procedures are in collision. The archive finds this the worst kind.",
            "You will be refused today for reasons entirely proper and entirely unhelpful.",
            "The obstacle in front of you has been inspected and found to be original to the building.",
            "A complaint you filed years ago has finally reached the top of a pile.",
            "You are making progress at right angles. It counts, and it is slower.",
        ],
        "constraints": [
            "What grinds today is being shaped into something. The sky has not said what.",
            "Friction is the archive's oldest supplier. Its invoices are always paid, eventually, by someone.",
            "You may pick a side if you like. The corridor does not care. The corridor has seen committees come and go.",
            "Pressure of this grade is not punishment. It is specification.",
            "The wall is real. So is the door in it, eventually. Doors begin their careers as walls.",
            "The archive does not remove obstructions. It records their dimensions and sends you the copy.",
            "What you are resisting is not always what is in your way.",
            "That grinding is the sound of specification. It is not the sound of you failing.",
        ],
    },
    "Sextile": {
        "verbs_one": [
            "is exchanging polite memos with",
            "has extended a modest invitation to",
            "is holding a door, pointedly, for",
            "has left a note in the pigeonhole of",
            "has slid a note under the door of",
            "is holding the lift for",
            "has left the light on for",
            "is holding a form half-completed for",
            "has mentioned, in passing, the availability of",
            "keeps a spare key belonging to",
        ],
        "verbs": [
            "are exchanging polite memos",
            "are circulating a modest proposal",
            "have opened a side door and are standing near it meaningfully",
            "are being courteous in a way that implies homework",
            "are leaving doors ajar with intent",
            "have exchanged courtesies of the binding kind",
            "are conducting a small and deniable cooperation",
            "have left the connecting door unlocked",
            "are being useful to each other by accident",
            "have exchanged a nod across the department",
        ],
        "omens": [
            "An opportunity exists. It is small, well-labeled, and easily ignored. Most are.",
            "The door is not locked. The archive would like to know who keeps suggesting it should be.",
            "A note has been left where you will find it. Finding it is, technically, your department.",
            "The invitation is real but modest, like a biscuit offered at a serious meeting. Take the biscuit.",
            "Somewhere, a small door has been propped open with a wedge of folded paper. The paper is a form. The form was always going to end up doing this.",
            "A courtesy has been extended to you. Courtesies of this size are how the archive tests reflexes.",
            "There is a gap in today's fence at roughly your shoulder width. Fences with gaps are called gates by the observant.",
            "The offer expires quietly. Quiet expiry is the archive's least favorite sound.",
            "A minor door has been unlocked for you, and not advertised.",
            "An offer is on the table, written small, at the bottom, where offers go to be missed.",
            "Something is available to you today that you will merely remember tomorrow.",
            "The archive has left a form where you will see it. This is as close as the archive comes to encouragement.",
            "A small kindness is being extended by a department not known for them.",
            "The opening is modest and cut to your size. Most are not.",
        ],
        "constraints": [
            "Doors that open quietly still require you to walk through them.",
            "Opportunities of this size are not announced twice. The second announcement is called regret.",
            "The archive files unclaimed invitations under 'evidence.' Evidence of what is a question for later.",
            "Small doors are still doors. The archive has watched empires enter through them, stooping slightly.",
            "An invitation you leave unanswered becomes, in time, an exhibit.",
            "An opportunity refused is not lost. It is reclassified, and the new classification is worse.",
            "The archive does not chase. It leaves things where you can find them.",
            "Small doors demand your attention, not your effort. Attention is the scarcer resource.",
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
    "The reading lamp above your shelf flickers at this configuration. Maintenance has been informed. Maintenance was informed in 1988.",
    "A previous holder of your coordinates left a paperclip in the file. The archive has not removed it. Removal requires a reason.",
    "Today's sky was predicted, in outline, by a junior clerk in 1931. She was not believed. Her pencil is in a display case.",
    "The card catalogue offers three cross-references for today. One is sensible. One is alarming. One is a recipe, misfiled.",
    "The archive's clock runs four minutes fast, by policy. It prefers to be waiting.",
    "Your file was requested once by another party. The request was denied. Files are read by their owners and the sky, in that order.",
    "There is a smudge on today's ledger entry at exactly the point of interest. The archive does not consider this symbolic. The archive considers it Tuesday.",
    "Shelf 9 is reserved for configurations the librarian finds personally amusing. Yours passed close to Shelf 9 today.",
    "A moth has taken residence in the O section of the atlas. Attempts at relocation are suspended by mutual agreement.",
    "Nothing in your file is written in red. This is rarer than you might hope.",
    "The previous librarian annotated this configuration with a single word. The word is illegible and appears to be angry.",
    "Your file has been reshelved twice this year for reasons of space. Space is the archive's oldest adversary.",
    "There is a coffee ring on the 1974 ledger at precisely this entry. The archive does not name the responsible party.",
    "The index card for today's configuration is in the wrong hand. Three librarians have declined to correct it.",
    "A request to simplify the filing system was submitted in 1963. It is being considered.",
    "The archive's second-floor window has not opened since the war. Which war is a matter of some internal debate.",
    "Someone has underlined a passage in your file. Underlining is not permitted. The underlining is correct.",
    "Today's configuration was assigned to a junior clerk, who filed it under 'weather.' It has not been moved.",
    "The stamp for 'noted without concern' has run dry. The archive is using 'noted' and hoping.",
    "There is a second copy of your file. The archive would prefer not to discuss the second copy.",
    "A cross-reference in your file leads to a shelf removed in 1981. The reference remains.",
    "The librarian has been asked not to editorialize. This note is the compromise.",
    "The reading room's clock and the ledger's clock disagree by eleven minutes. Both are considered official.",
    "Your coordinates share a drawer with an unsolved matter from 1952. Proximity is not implication.",
    "The archive received a complaint about this configuration in 1996. The complainant did not specify its nature.",
    "A pressed flower was found in the file adjacent to yours. It has been left where it was.",
    "The catalogue card for this aspect has been corrected four times, each in a different hand.",
    "Today's entry was written in haste. The archive has verified it twice since and stands by the haste.",
    "There is a knock in the pipes at this hour that the archive has learned to read as punctuation.",
    "The Department of Second Opinions was closed in 1969. Its correspondence is still delivered.",
    "The librarian's predecessor believed this configuration meant rain. It occasionally does.",
    "Your file carries an odd smell that the archive has classified as 'previous ownership.'",
    "The seal on today's ledger entry was applied crookedly. Straightening it would require reopening the ledger.",
    "A note in the margin reads 'see also.' It does not say what.",
    "The archive's ladder reaches the eighth shelf. Your file is on the eighth shelf. This is not thought to be significant.",
]

# Used when a sign's ruling planet has no aspect at all today. Without these
# such signs fell back to the three shared base omens, which is exactly where
# the same-day cross-sign repetition was coming from: several signs quoting
# the same STACK line on one date.
QUIET_OMENS = [
    "The ruling department has filed a nil return. Nil returns are still returns.",
    "Nothing is being asked of this file today. The archive finds that suspicious and files it anyway.",
    "Your governing desk is unoccupied this afternoon. A note says 'back shortly', in handwriting from 1970.",
    "No business has been raised in your name. Enjoy the absence of correspondence.",
    "The relevant department is between engagements. It is tidying, which it does when uneasy.",
    "There is no entry against your governor today. The blank space has been initialled, as required.",
    "Your file was carried to the reading room and carried back unopened.",
    "The sky has nothing scheduled for this shelf. Scheduling is not the same as intention.",
    "A quiet day in your section. The dust is undisturbed and the archive is watching it.",
    "Your governing planet is present, accounted for, and doing nothing anyone can put in writing.",
    "The department responsible for you has closed early. This is permitted twice a year.",
    "No aspect, no meeting, no minutes. The archive has written 'as before' and moved on.",
    # Sized for the worst case: if every one of the twelve signs falls back
    # here on the same date, the day allocator needs ~28 lines to serve them
    # all without repeating. Twelve was not enough and failed silently.
    "The shelf bearing your governor has been dusted, and nothing else.",
    "No memorandum has been issued in your direction. The archive has issued one about that.",
    "Your governing department submitted a blank sheet, correctly dated and signed.",
    "Nothing is pending. The archive has read the word 'nothing' several times and stands by it.",
    "There is no traffic in your corridor today. The corridor remains a corridor.",
    "Your governor was observed at its desk, reading something unrelated.",
    "The day's business passed your section without stopping. It waved.",
    "An absence of aspect is not an absence of position. Your governor is exactly where it should be.",
    "The file was pulled, checked against the ledger, and returned to the same millimetre.",
    "Nobody has asked after your governing planet since Tuesday. It has noticed.",
    "The archive records 'no change' for your section, in the same ink as everything else.",
    "Your governor has taken the quiet shift. There is always a quiet shift, and someone must take it.",
    "Nothing has been scheduled against you. Scheduling clerks are, as a rule, thorough.",
    "The correspondence tray for your section is empty, and has been polished.",
    "A day without incident has been entered in your file. These are counted, and rarely.",
    "Your section is at rest. The archive does not use the word 'peace' in official records.",
]

# Headlines for the same case. Without these, every sign whose ruler was
# unaspected fell back to the SAME day headline — measured at Cancer and Leo
# sharing a headline on 366 days out of 366, because neither Sun nor Moon was
# aspected in the test sky. Item 12 covered omens; this is the same defect one
# field over.
QUIET_HEADLINES = [
    "The department that keeps your file has nothing to declare.",
    "Your governing planet is holding no meetings today.",
    "The relevant desk is occupied, and idle.",
    "No business has been entered against your section of the sky.",
    "The sky is present in your file and taking no action.",
    "Your governor is unaspected today, which the archive records without alarm.",
    "The shelf that answers for you has not been disturbed.",
    "Nothing has been scheduled in your name. The schedule is otherwise full.",
    "Your section of the sky is between engagements.",
    "The planet responsible for you is at its post, and unbothered.",
    "There is no correspondence today from the department that governs you.",
    "The archive has entered 'as before' against your coordinates.",
    "Your governing desk has closed its ledger early.",
    "No aspect touches your ruler today. The ruler is aware, and untroubled.",
]


def _idx(seed, salt, n):
    """Salted integer hash — the index for one pool, decorrelated from every
    other pool drawn with the same seed.

    The previous form, (seed * 31 + salt * 7) % n, could not do that. With a
    pool of 10 it reduces to (seed + constant) % 10, so the verb index and the
    note index moved in lockstep: measured at 10 distinct (verb, note) pairs
    out of a possible 100, and any two visitors whose dates differ by a
    multiple of ten received an identical transit line AND note. Same defect
    as the tv.html pools in batch 1, one file over."""
    if n <= 0:
        return 0
    h = ((int(seed) & 0x7fffffff) * 2654435761) ^ ((int(salt) + 1) * 2246822519)
    h &= 0xffffffff
    h ^= h >> 15
    h = (h * 2246822507) & 0xffffffff
    h ^= h >> 13
    return h % n


def _pick(pool, seed, salt=0):
    if not pool:
        return None
    return pool[_idx(seed, salt, len(pool))]


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _order(pool, seed):
    """A deterministic full permutation of pool, keyed by seed.

    Used instead of a single modulo pick so the day allocator can walk a
    sign's preferences in order and take the first line no other sign has
    claimed today. The stride is forced coprime to the length — otherwise the
    walk revisits a subset and starves the rest of the pool."""
    n = len(pool)
    if n == 0:
        return []
    if n == 1:
        return list(pool)
    step = 1 + (abs(seed) % (n - 1))
    while _gcd(step, n) != 1:
        step += 1
    start = abs(seed) % n
    return [pool[(start + k * step) % n] for k in range(n)]


class _DayAllocator:
    """Hands out corpus lines without replacement, for one date.

    TASK item 12: two signs must not carry the same omen or marginal note on
    the same day. Visitors compare readings in the room — a shared line is the
    most legible way for the archive to look like a random line generator.
    Each sign asks in its own seeded order; the allocator returns the first
    lines nobody has claimed yet.

    If a pool genuinely runs short it repeats rather than returning nothing,
    and records which pool in .exhausted, so the harness reports it instead of
    the shortfall passing silently."""

    def __init__(self):
        self.used = set()
        self.exhausted = []

    def take(self, pool, seed, count=1, label="", avoid=()):
        """Take `count` lines nobody has claimed today.

        `avoid` is the caller's own current selection. Without it the
        exhaustion fallback could hand a sign a line it had already been given
        moments earlier in the same reading — one sign, the same sentence
        twice, which is worse than two signs sharing one."""
        if not pool:
            return []
        avoid = set(avoid)
        out = []
        for line in _order(pool, seed):
            if line not in self.used and line not in avoid:
                out.append(line)
                self.used.add(line)
                if len(out) == count:
                    return out
        # pool exhausted for today. Degrade in order: reuse a line another sign
        # has, before ever repeating one of this sign's own.
        self.exhausted.append(label or "unlabelled")
        for line in _order(pool, seed):
            if line not in out and line not in avoid:
                out.append(line)
                if len(out) == count:
                    return out
        for line in _order(pool, seed):
            if line not in out:
                out.append(line)
                if len(out) == count:
                    break
        return out

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
    # Every phrasing this aspect could take, in seeded order. build_sign_readings
    # allocates from this so two signs whose rulers share ONE aspect (Taurus and
    # Gemini on a Mercury-Venus sextile) cannot end up with the same sentence.
    # The old arithmetic pick made that impossible by accident — adjacent signs
    # always landed one verb apart — and the accident died with it.
    variants = [f"{d1[0].upper()}{d1[1:]} and {d2} {v}."
                for v in _order(mode["verbs"], seed)]
    # Return an ordered CANDIDATE list, not a fixed two. build_reading still
    # takes the first three; build_sign_readings needs the depth so its day
    # allocator can skip lines another sign already claimed today.
    # the FULL mode pool in seeded order, not a slice of it. Six candidates was
    # enough for the signs served early in the day and starved the ones served
    # last — Aquarius, on a day when several signs led with the same aspect.
    omens = _order(mode["omens"], seed)
    constraint = _pick(mode["constraints"], seed, 4)
    return headline, omens, constraint, variants

# ---------------------------------------------------------------------------
# Sign temperament layer — the visitor's natal sun sign as a filter.
# Per the brief's interpretation hierarchy, temperament outweighs all:
# it does not change what the sky says, it changes how the visitor
# should hold it. `address` opens their file; `lens` closes the reading.
# ---------------------------------------------------------------------------

# Two variants per sign as of 2026-08-14 — address and lens are now LISTS,
# selected by the day/sign seed. Anything reading these must index, not
# concatenate: t["address"][i], not t["address"].
SIGN_TEMPERAMENT = {
    "Aries": {
        "address": [
            "Filed under ARIES. The folder is slightly singed.",
            "Filed under ARIES. The folder was returned before it was finished.",
        ],
        "lens": [
            "You will want to act on this immediately. The sky suggests reading to the end first.",
            "You will decide what this means within four seconds. The archive asks for six.",
        ],
    },
    "Taurus": {
        "address": [
            "Filed under TAURUS. The folder has not moved in some time.",
            "Filed under TAURUS. The folder is heavier than its contents explain.",
        ],
        "lens": [
            "You will want this to stay as it is. The sky declines to promise that.",
            "You will file this away for later. Later has been notified.",
        ],
    },
    "Gemini": {
        "address": [
            "Filed under GEMINI. The folder is cross-referenced with everything.",
            "Filed under GEMINI. The folder has been found in two places today.",
        ],
        "lens": [
            "You will want to discuss this with someone. Possibly several someones. Possibly at once.",
            "You will have two readings of this by evening. Both are yours. Only one is load-bearing.",
        ],
    },
    "Cancer": {
        "address": [
            "Filed under CANCER. The folder is kept close to the chest.",
            "Filed under CANCER. The folder has been repaired more than once, carefully.",
        ],
        "lens": [
            "You will feel this before you understand it. For you, that is the correct order.",
            "You will take this personally. That is not a flaw in you, or in the reading.",
        ],
    },
    "Leo": {
        "address": [
            "Filed under LEO. The folder has requested better lighting.",
            "Filed under LEO. The folder is kept at the front, where it insists on being.",
        ],
        "lens": [
            "You will want to be seen handling this well. Handling it well is the part that matters.",
            "You will want a witness for this. Choose one who is not impressed by you.",
        ],
    },
    "Virgo": {
        "address": [
            "Filed under VIRGO. The folder has been annotated. Twice.",
            "Filed under VIRGO. The folder is correct in every particular and still unsatisfied.",
        ],
        "lens": [
            "You will notice the flaw in this reading. Noted. The flaw is load-bearing.",
            "You will improve this reading before the end of the day. The archive expects the amendment.",
        ],
    },
    "Libra": {
        "address": [
            "Filed under LIBRA. The folder sits exactly between two shelves.",
            "Filed under LIBRA. The folder has been balanced on the edge of the desk for some time.",
        ],
        "lens": [
            "You will want to weigh both sides. At some point, the scale must be read.",
            "You will ask what someone else would do. Ask, then do the other thing.",
        ],
    },
    "Scorpio": {
        "address": [
            "Filed under SCORPIO. The folder is sealed. You sealed it.",
            "Filed under SCORPIO. The folder was opened once, briefly, and closed with force.",
        ],
        "lens": [
            "You will suspect there is more beneath this. There is. There always is.",
            "You will look for what the archive is not saying. The archive respects this and says nothing.",
        ],
    },
    "Sagittarius": {
        "address": [
            "Filed under SAGITTARIUS. The folder was found some distance from its shelf.",
            "Filed under SAGITTARIUS. The folder carries stamps from three other archives.",
        ],
        "lens": [
            "You will want the larger meaning. Fine. Today's paperwork still applies.",
            "You will want to leave before the end of this. The end is where the useful part is kept.",
        ],
    },
    "Capricorn": {
        "address": [
            "Filed under CAPRICORN. The folder is structurally sound.",
            "Filed under CAPRICORN. The folder has been in continuous use since it was opened.",
        ],
        "lens": [
            "You will ask what this is useful for. Not everything is. Some of it is anyway.",
            "You will convert this into a plan. The archive notes that some things are only weather.",
        ],
    },
    "Aquarius": {
        "address": [
            "Filed under AQUARIUS. The folder is filed under a system of its own devising.",
            "Filed under AQUARIUS. The folder is where it should be, by an argument only it understands.",
        ],
        "lens": [
            "You will want to improve the premise. The premise thanks you, and remains.",
            "You will find the reading's assumptions before its conclusions. Both are available.",
        ],
    },
    "Pisces": {
        "address": [
            "Filed under PISCES. The folder's edges are soft from handling.",
            "Filed under PISCES. The folder has absorbed something from its neighbours.",
        ],
        "lens": [
            "You will absorb more of this than intended. Please return what is not yours.",
            "You will take on more of this than was addressed to you. Return the excess at the desk.",
        ],
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
        "For today, do not ask where the mood came from. It came with furniture.",
        "The subject will follow you between rooms. Feeding it is optional. It has already eaten.",
        "Whatever this is, it has your address and a key. It let itself in before you woke.",
        "You will not get distance from this today. Distance is a service the sky is not offering.",
        "It knows your habits by heart already. Assume you are being finished, sentence by sentence.",
        "The thing and you are, for the day, one item. File under whichever name you prefer.",
    ],
    "Opposition": [
        "The pull you feel is not indecision. It is geometry.",
        "Someone across the table holds the other half of this. Possibly it is also you.",
        "You have been seated at one end of a very long table. The correct posture is upright and amused.",
        "Whatever stands opposite you today is not an enemy. It is a counterweight, and you are the other one.",
        "Today the far side of the argument has your handwriting. Study it before objecting.",
        "The tension is symmetrical, which means you are holding half. Set your half down slowly, if at all.",
        "You will be asked to hold a position you no longer entirely believe. Hold it honestly, or set it down.",
        "Something is standing precisely where you would have to stand to see yourself.",
        "The other party has a case. So do you. The archive declines to referee and takes notes.",
        "You are one end of today. Somebody, somewhere, is the other, and has no idea.",
    ],
    "Trine": [
        "The door is already open. Your only task is to notice.",
        "Today, competence will look suspiciously like luck. Accept the accounting error.",
        "The paperwork has gone through before you finished filling it in. Do not report this. Use it.",
        "Something in your vicinity is working on your behalf without being asked. The archive suggests gratitude, silently performed.",
        "What you attempt before noon will cooperate. The archive suggests attempting the difficult thing first, quietly.",
        "Someone has cleared the corridor ahead of you. Walk it as if you had planned to all along.",
        "Ease is being extended to you specifically. The archive suggests noticing by whom.",
        "You will do something difficult today and not remember it as difficult. That is not amnesia. It is fit.",
        "Nothing will be in your way. The archive asks only that you have somewhere to go.",
        "You are being helped by circumstances that will deny it afterwards.",
    ],
    "Square": [
        "The resistance is precisely fitted to you. Treat it as tailoring.",
        "What blocks you today is load-bearing. Lean on it; do not kick it.",
        "The obstacle has your name on it — spelled correctly, which should tell you how long it has been planned.",
        "You will want to file a complaint. The complaint window is, today, the mirror. This is noted without cruelty.",
        "Today's difficulty is addressed to you personally and marked 'builds character.' The archive did not choose the wording.",
        "You will meet the same obstacle twice. The second meeting is the appointment; the first was the rehearsal.",
        "The thing in your way has been in your way before, in a different coat.",
        "You will want to go around it. Around is longer. The archive holds the survey.",
        "This one is measured to you exactly, which is either flattering or ominous. It is both.",
        "You are being worked on today, in the way a stone is worked on. Loudly, and to a purpose.",
    ],
    "Sextile": [
        "A modest opening, addressed to you by name. RSVP optional.",
        "The sky is offering. It will not offer twice in the same tone.",
        "A side door stands open at roughly your height. Coincidences of this kind are rarely coincidences and never doors.",
        "The invitation is small enough to fit in a coat pocket, which is where such things are usually lost. Check the pocket.",
        "The chance is minor, exact, and time-stamped. Minor exact time-stamped things are how archives begin.",
        "If something small presents itself today, measure it twice. Small is a disguise the useful wear.",
        "A small thing is being offered to you and to nobody else. It is not gift-wrapped.",
        "You will be busy at the moment it appears. That is the design, and the test.",
        "Something modest is holding a place for you until roughly this evening.",
        "The opening is your size. The archive measured, which it does not do often.",
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
    # salt 6, distinct from the verb's salt 3: the line and its note must not
    # move together, or the pair collapses to len(notes) combinations
    return {"line": line, "note": _pick(notes, variant, 6)}


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


# Reverse maps for curated tokens: MOO_OPP_SAT -> (Moon, Saturn, "Opposition").
# Needed because a curated token's own writing is only three omens and one
# headline — not enough depth for the day allocator when two signs are led by
# the same token (Cancer and Capricorn both land on MOO_OPP_SAT). Without a
# wider pool the allocator exhausts and repeats, which is the exact thing
# TASK item 12 exists to prevent.
_TOK_TO_PLANET = {p.upper()[:3]: p for p in PLANET_DESK}
_CODE_TO_MODE = {"CON": "Conjunction", "OPP": "Opposition", "TRI": "Trine",
                 "SQR": "Square", "SXT": "Sextile"}


def _token_parts(tok):
    """(planet1, planet2, mode) for a curated token, or (None, None, None)."""
    parts = tok.split("_")
    if len(parts) != 3:
        return None, None, None
    return (_TOK_TO_PLANET.get(parts[0]), _TOK_TO_PLANET.get(parts[2]),
            _CODE_TO_MODE.get(parts[1]))


def _curated_depth(tok, m, seed):
    """A curated lead, widened: its own writing first, then the composed
    phrasings and omens for the same aspect so the allocator has somewhere to
    go. Returns (omens, headline_variants)."""
    p1, p2, mode_name = _token_parts(tok)
    mode = ASPECT_MODES.get(mode_name)
    omens = list(m["omens"])
    variants = [m["headline"]]
    if mode and p1 and p2:
        d1, d2 = PLANET_DESK.get(p1), PLANET_DESK.get(p2)
        omens += _order(mode["omens"], seed)[:6]
        if d1 and d2:
            variants += [f"{d1[0].upper()}{d1[1:]} and {d2} {v}."
                         for v in _order(mode["verbs"], seed)]
    omens += _order(QUIET_OMENS, seed)[:4]   # last-resort tail, never empty
    return uniq(omens), variants


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
                c_omens, c_variants = _curated_depth(tok_name, m, seed)
                cands.append(((m["headline"], c_omens, m["constraint"],
                               c_variants), r))
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

    # One allocator for the whole day: whatever a sign takes, the eleven
    # others can no longer take (TASK item 12). Signs are served in a
    # day-rotated order so Aries is not permanently first in the queue for
    # every shared pool — the readings would then be reliably better at the
    # start of the zodiac, which is not a property anyone asked for.
    alloc = _DayAllocator()
    serve_order = [sign_order[(day_seed + k) % 12] for k in range(12)]

    out = {}
    for sign in serve_order:
        t = SIGN_TEMPERAMENT[sign]
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
            # allocate the phrasing, not just the omens: the headline is a line
            # like any other and two signs must not share it on one date
            headline = alloc.take(lead[3], s_seed, 1, f"headline:{sign}")[0]
            # quiet lines as a tail on every lead, not just curated ones: they
            # are the depth that keeps the last sign served from repeating
            pool = uniq(list(lead[1]) + base_omens + _order(QUIET_OMENS, s_seed)[:6])
            omens = alloc.take(pool, s_seed, 2, f"omens:{sign}")
            constraint = lead[2]
        else:
            # The "reports nothing unusual" suffix used to live on the
            # governor line; the quiet headline now says it, per sign, in
            # words no other sign is using today.
            headline = (alloc.take(QUIET_HEADLINES, s_seed, 1,
                                   f"quiet-headline:{sign}") or [base_headline])[0]
            omens = alloc.take(uniq(QUIET_OMENS + base_omens), s_seed, 2,
                               f"quiet:{sign}")

        # the librarian's marginal note — most readings carry one.
        # avoid= is what this sign already holds: the third line must not
        # repeat either of the first two.
        if s_seed % 3 != 0:
            omens = omens + alloc.take(MARGINALIA, s_seed + 9, 1,
                                       f"marginalia:{sign}", avoid=omens)
        else:
            omens = omens + alloc.take(
                uniq(list(lead[1]) + base_omens) if lead
                else uniq(QUIET_OMENS + base_omens),
                s_seed + 5, 1, f"omens:{sign}", avoid=omens)

        # second address/lens variant, rotating by day and by sign
        v = (day_seed + sign_idx) % 2

        out[sign] = {
            "address":    t["address"][v % len(t["address"])],
            "governor":   governor,
            "headline":   headline,
            "omens":      omens,
            "constraint": constraint,
            "lens":       t["lens"][v % len(t["lens"])],
            "aside":      aside,
        }

    # emit in canonical zodiac order, whatever order they were served in
    return {s: out[s] for s in sign_order}

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
    "The archive closes at dusk, in principle. In practice the sky refuses to.",
    "Lost certainty may be reclaimed at the desk, upon description. Descriptions are rarely adequate.",
    "Kindly do not reshelve yourself. Staff will do this for you.",
    "Today's entries will be bound at the end of the era. Errata sheets are anticipated.",
    "The suggestion box was sealed by order in 1954. Suggestions may still be made to the night sky, which keeps its own box.",
    "The archive thanks you for your coordinates and returns them, slightly used.",
    "Your visit has been recorded in the day-book, between two other visits and a note about the heating.",
    "The stacks will be swept tonight. Anything left will be shelved without ceremony.",
    "This reading is issued in one copy. The archive keeps the carbon.",
    "Please do not thank the sky. It has been known to interpret gratitude as a request.",
    "The librarian returns to the shelves. There is a backlog. There is always a backlog.",
    "The file closes. It closes the way files do — most of the way.",
    "Further enquiries may be submitted in writing, and will join the others.",
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
                    c_head, c_omens, c_constraint, _variants = composed
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
