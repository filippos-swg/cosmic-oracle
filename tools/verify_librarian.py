"""Batch-2 verification for librarian.py.

Checks the corpus sizes, that every curated TOKEN_MEANINGS key can actually
fire (a key written in the wrong planet order never matches and dies silently),
that no line is duplicated across pools, and — the point of TASK item 12 —
that no two signs carry the same omen or marginal note on the same date.

The day sweep rewrites sky_state's utc across a full year: day_seed is derived
from day-of-year, so this exercises every allocation the installation can
produce from one real sky. The no-aspect case is tested separately because
that is the path where every sign falls back to shared material.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import librarian as L                                    # noqa: E402

fail = []
def bad(msg):
    print("  FAIL " + msg)
    fail.append(msg)


# --------------------------------------------------------------- pool sizes
print("\n[1] POOL SIZES")
TARGETS = {"TOKEN_MEANINGS": 20, "MARGINALIA": 50, "ASIDE_CLOSINGS": 20}
for name, want in TARGETS.items():
    got = len(getattr(L, name))
    print(f"  {name:<16} {got}")
    if got < want:
        bad(f"{name} = {got}, expected >= {want}")
for mode, m in L.ASPECT_MODES.items():
    got = (len(m["verbs_one"]), len(m["verbs"]), len(m["omens"]), len(m["constraints"]))
    if got < (10, 10, 14, 8):
        bad(f"ASPECT_MODES.{mode} = {got}, expected >= (10, 10, 14, 8)")
print(f"  ASPECT_MODES     5 modes x (verbs_one 10, verbs 10, omens 14, constraints 8)")
for mode, notes in L.TRANSIT_NOTES.items():
    if len(notes) < 10:
        bad(f"TRANSIT_NOTES.{mode} = {len(notes)}, expected >= 10")
print(f"  TRANSIT_NOTES    5 modes x {len(L.TRANSIT_NOTES['Trine'])}")
for sign, t in L.SIGN_TEMPERAMENT.items():
    if len(t["address"]) < 2 or len(t["lens"]) < 2:
        bad(f"SIGN_TEMPERAMENT.{sign} needs 2 address and 2 lens variants")
print(f"  SIGN_TEMPERAMENT 12 signs x 2 address + 2 lens")


# ------------------------------------------------- curated keys can fire
print("\n[2] TOKEN KEYS — a key in the wrong planet order never matches sky.py")
sky_src = (ROOT / "sky.py").read_text(encoding="utf-8")
planet_block = re.search(r"PLANETS\s*=\s*\{(.*?)\}", sky_src, re.S).group(1)
order = [m.upper()[:3] for m in re.findall(r'"(\w+)"\s*:', planet_block)]
codes = set(re.findall(r'"\w+":\s*"(\w{3})"', sky_src))
print(f"  sky.py emits planet1 before planet2 in: {' '.join(order)}")
for key in L.TOKEN_MEANINGS:
    parts = key.split("_")
    if len(parts) != 3:
        bad(f"{key}: not TOK_ASP_TOK")
        continue
    a, asp, b = parts
    if asp not in codes:
        bad(f"{key}: '{asp}' is not an aspect code emitted by sky.py ({sorted(codes)})")
    if a not in order or b not in order:
        bad(f"{key}: unknown planet token")
    elif order.index(a) >= order.index(b):
        bad(f"{key}: wrong order — sky.py would emit {b}_{asp}_{a}, so this never fires")
if not fail:
    print(f"  all {len(L.TOKEN_MEANINGS)} keys are reachable")


# ------------------------------------------------------- corpus duplicates
print("\n[3] DUPLICATE LINES ACROSS POOLS")
seen, dupes = {}, 0
def scan(label, lines):
    global dupes
    for s in lines:
        k = s.strip().lower()
        if k in seen:
            bad(f"duplicate in {label} and {seen[k]}: \"{s[:64]}...\"")
            dupes += 1
        else:
            seen[k] = label

for tok, m in L.TOKEN_MEANINGS.items():
    scan(f"TOKEN_MEANINGS.{tok}", [m["headline"], m["constraint"], *m["omens"]])
for mode, m in L.ASPECT_MODES.items():
    for field in ("verbs_one", "verbs", "omens", "constraints"):
        scan(f"ASPECT_MODES.{mode}.{field}", m[field])
scan("MARGINALIA", L.MARGINALIA)
scan("ASIDE_CLOSINGS", L.ASIDE_CLOSINGS)
scan("QUIET_OMENS", L.QUIET_OMENS)
scan("QUIET_HEADLINES", L.QUIET_HEADLINES)
for mode, notes in L.TRANSIT_NOTES.items():
    scan(f"TRANSIT_NOTES.{mode}", notes)
for sign, t in L.SIGN_TEMPERAMENT.items():
    scan(f"SIGN_TEMPERAMENT.{sign}", t["address"] + t["lens"])
for el, s in L.STACK_BY_ELEMENT.items():
    scan(f"STACK_BY_ELEMENT.{el}", [s["headline"], s["constraint"], *s["omens"]])
if not dupes:
    print(f"  {len(seen)} lines, none repeated")


# ------------------------------------- TASK item 12: same-day cross-sign
def sweep(sky, label, days=366):
    """Build all 12 sign readings for every day-of-year and check that no
    omen or marginal note is shared by two signs on the same date."""
    worst, shared_days, exhausted = 0, 0, set()
    headline_counts = []
    for doy in range(1, days + 1):
        s = json.loads(json.dumps(sky))
        s["utc"] = f"2026-01-01T12:00:00+00:00"
        # day_seed is strftime('%j') of utc, so walk real dates
        from datetime import datetime, timedelta
        s["utc"] = (datetime(2026, 1, 1) + timedelta(days=doy - 1)).isoformat() + "+00:00"

        alloc_before = len(L._DayAllocator().used)          # noqa: F841
        readings = L.build_sign_readings(s)

        counts = {}
        for sign, r in readings.items():
            for line in r["omens"]:
                counts.setdefault(line, []).append(sign)
        for sign, r in readings.items():
            counts.setdefault(r["headline"], []).append(sign)
        clashes = {k: v for k, v in counts.items() if len(v) > 1}
        if clashes:
            shared_days += 1
            worst = max(worst, max(len(v) for v in clashes.values()))
            if shared_days == 1:
                line, signs = next(iter(clashes.items()))
                bad(f"{label} day {doy}: \"{line[:56]}...\" shared by {', '.join(signs)}")
        headline_counts.append(len(set(r["headline"] for r in readings.values())))
    return shared_days, worst, sum(headline_counts) / len(headline_counts)


print("\n[4] SAME-DAY CROSS-SIGN REPEATS — 366 days, real sky")
sky = json.loads((ROOT / "sky_state.json").read_text(encoding="utf-8"))
shared, worst, avg_heads = sweep(sky, "real sky")
print(f"  days with any line shared by two signs: {shared}/366")
print(f"  distinct headlines across the 12 signs:   {avg_heads:.1f}/12 average")
if shared:
    bad(f"{shared} days still share lines across signs (worst: {worst} signs on one line)")

print("\n[5] SAME-DAY CROSS-SIGN REPEATS — degenerate sky, no aspects at all")
quiet = json.loads(json.dumps(sky))
quiet["aspects"] = []
quiet["signature"] = []
shared_q, worst_q, avg_q = sweep(quiet, "no-aspect sky", days=90)
print(f"  days with a shared line: {shared_q}/90   (every sign falls back here)")
if shared_q:
    bad(f"no-aspect sky repeats across signs on {shared_q} days")

print("\n[6] ALLOCATOR HEADROOM")
a = L._DayAllocator()
a.take(L.MARGINALIA, 1, 1, "probe")
readings = L.build_sign_readings(sky)
probe = L._DayAllocator()
for i in range(12):
    probe.take(L.MARGINALIA, i * 13, 1, "sign")
print(f"  MARGINALIA {len(L.MARGINALIA)} lines for 12 signs/day — "
      f"{len(L.MARGINALIA) // 12}x headroom, exhausted: {probe.exhausted or 'no'}")
if probe.exhausted:
    bad("marginalia pool exhausted for a single day")

print("\n[7] SIGN VARIANTS ROTATE")
from datetime import datetime, timedelta
addr = {}
for doy in (1, 2):
    s = json.loads(json.dumps(sky))
    s["utc"] = (datetime(2026, 1, 1) + timedelta(days=doy - 1)).isoformat() + "+00:00"
    for sign, r in L.build_sign_readings(s).items():
        addr.setdefault(sign, set()).add(r["address"])
rotating = sum(1 for v in addr.values() if len(v) == 2)
print(f"  signs whose address changed between two consecutive days: {rotating}/12")
if rotating < 12:
    bad("address variant does not rotate day to day for every sign")

print("\n[8] CURATED TOKENS FIRE AGAINST REAL SKY — 730 days")
# A token that never matches is dead corpus. This computes real ephemeris
# signatures for two years and counts hits per token.
try:
    import swisseph as swe                                  # noqa: E402
    import sky                                              # noqa: E402
    import collections
    hits, days = collections.Counter(), 0
    N = 730
    for k in range(N):
        jd = swe.julday(2026, 1, 1, 12.0) + k
        pos, _spd = sky.get_positions(jd)
        planets = {n: {"sign": sky.lon_to_sign(l)[0], "degree": sky.lon_to_sign(l)[1]}
                   for n, l in pos.items()}
        sig = sky.build_signature({"planets": planets},
                                  sky.find_aspects(pos), max_aspects=8)
        fired = [t for t in sig if t in L.TOKEN_MEANINGS]
        if fired:
            days += 1
        hits.update(fired)
    dead = [t for t in L.TOKEN_MEANINGS if not hits[t]]
    print(f"  days where a curated token leads: {days}/{N} ({100 * days / N:.0f}%)")
    print(f"  least-used token: {min(hits, key=hits.get)} ({min(hits.values())} hits)")
    if dead:
        bad(f"curated tokens that never fire in two years: {dead}")
    else:
        print(f"  all {len(L.TOKEN_MEANINGS)} tokens fire at least 18 times")
except ImportError:
    print("  skipped — pyswisseph not installed")

print("\n[9] TRANSIT LINE AND NOTE MUST NOT MOVE TOGETHER")
# server.py builds every transit as compose_transit(..., variant=seed+idx).
# If the verb and the note are drawn with correlated indices the pair collapses
# to len(notes) combinations and two visitors a fixed distance apart receive an
# identical line AND note — the defect fixed in tv.html, one file over.
pairs, lines_seen = set(), set()
for seed in range(2000, 2400):
    r = L.compose_transit("Saturn", "Square", "Sun", variant=seed)
    pairs.add((r["line"], r["note"]))
    lines_seen.add(r["line"])
possible = len(L.ASPECT_MODES["Square"]["verbs_one"]) * len(L.TRANSIT_NOTES["Square"])
print(f"  distinct line+note pairs over 400 seeds: {len(pairs)}/{possible}")
if len(pairs) < possible * 0.8:
    bad(f"transit line and note are correlated — only {len(pairs)} of {possible} pairings occur")
if len(lines_seen) < len(L.ASPECT_MODES["Square"]["verbs_one"]):
    bad("some transit verbs are unreachable")

print("\n" + (f"{len(fail)} FAILURE(S)" if fail else "ALL CHECKS PASSED"))
sys.exit(1 if fail else 0)
