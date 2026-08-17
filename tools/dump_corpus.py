"""Emit every string the reading screens can print, tagged with the CSS class
it will be printed in. Feeds tools/typography_audit.mjs --exhaustive.

Sampling ceremonies only proves the lines that happened to be drawn. This
enumerates the whole space: every transit sentence the composer can build,
every headline variant, every omen, constraint, landing, verdict and verse.
"""
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import librarian as L                                        # noqa: E402

tv = (ROOT / "visual" / "tv.html").read_text(encoding="utf-8")


def js_block(name):
    """Pull a const literal out of tv.html and JSON-ify it via node."""
    import subprocess
    script = (
        "const fs=require('fs');const h=fs.readFileSync(process.argv[1],'utf8');"
        "const n=process.argv[2];"
        "const s=h.indexOf('const '+n+' ');let i=h.indexOf('=',s)+1;"
        "while(/\\s/.test(h[i]))i++;const o=h[i],c=o==='{'?'}':']';"
        "let d=0,j=i,q=null;for(;j<h.length;j++){const ch=h[j];"
        "if(q){if(ch==='\\\\'){j++;continue}if(ch===q)q=null;continue}"
        "if(ch==='\"'||ch===\"'\"||ch==='`'){q=ch;continue}"
        "if(ch===o)d++;else if(ch===c&&!--d)break}"
        "process.stdout.write(JSON.stringify(eval('('+h.slice(i,j+1)+')')));"
    )
    out = subprocess.run(["node", "-e", script, str(ROOT / "visual" / "tv.html"), name],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


LANDINGS = js_block("LANDINGS")
VERDICTS = js_block("VERDICTS")
FRAMES = js_block("LANDING_FRAMES")
FOUND = js_block("FOUND_ITEMS")
FORM_NOTES = js_block("RECORD_FORM_NOTES")

body, note, poem, verdict = [], [], [], []

# --- transit sentences: every desk x every verb x each target -------------
for mode in L.ASPECT_MODES.values():
    for verb in mode["verbs_one"]:
        for desk in L.PLANET_DESK.values():
            for target in ("Sun", "Moon"):
                body.append(f"{desk[0].upper()}{desk[1:]} {verb} your natal {target}.")

# --- sign headlines: composed variants, curated, quiet --------------------
for mode in L.ASPECT_MODES.values():
    for verb in mode["verbs"]:
        for d1, d2 in itertools.islice(
                itertools.permutations(L.PLANET_DESK.values(), 2), 0, None, 3):
            body.append(f"{d1[0].upper()}{d1[1:]} and {d2} {verb}.")
body += [m["headline"] for m in L.TOKEN_MEANINGS.values()]
body += list(L.QUIET_HEADLINES)
body += [s["headline"] for s in L.STACK_BY_ELEMENT.values()]

# --- observations and constraints ----------------------------------------
for mode in L.ASPECT_MODES.values():
    body += mode["omens"] + mode["constraints"]
for m in L.TOKEN_MEANINGS.values():
    body += m["omens"] + [m["constraint"]]
for s in L.STACK_BY_ELEMENT.values():
    body += s["omens"] + [s["constraint"]]
body += L.MARGINALIA + L.QUIET_OMENS

# --- the visitor's own lines ---------------------------------------------
for t in L.SIGN_TEMPERAMENT.values():
    body += t["address"] + t["lens"]

# --- notes ---------------------------------------------------------------
for dk in LANDINGS:
    for mode in LANDINGS[dk]:
        for frame in FRAMES:
            note += [frame + line for line in LANDINGS[dk][mode]]
for dk in VERDICTS:
    for mode in VERDICTS[dk]:
        verdict += VERDICTS[dk][mode]
for mode, notes in L.TRANSIT_NOTES.items():
    note += notes
note += FORM_NOTES
note += [f"Your file is kept by {d}." for d in L.PLANET_DESK.values()]
note += list(L.ASIDE_CLOSINGS)

# --- the found item ------------------------------------------------------
for container in FOUND.values():
    for pieces in container["pieces"].values():
        poem += pieces

out = {
    "body": sorted(set(body)),
    "note": sorted(set(note)),
    "poem": sorted(set(poem)),
    "verdict": sorted(set(verdict)),
}
dest = ROOT / "tools" / "corpus_dump.json"
dest.write_text(json.dumps(out), encoding="utf-8")
print(f"wrote {dest.name}: " + "  ".join(f"{k} {len(v)}" for k, v in out.items()))
