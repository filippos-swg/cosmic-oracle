import json
import sys
import time
import subprocess
from datetime import datetime, timezone
UTC = timezone.utc
from pathlib import Path

UPDATE_SECONDS = 60        # re-run sky + write oracle.json every 60s
PRINT_LOGS     = True

HERE       = Path(__file__).resolve().parent
SKY_PY     = HERE / "sky.py"
SKY_JSON   = HERE / "sky_state.json"
SIG_TXT    = HERE / "sky_signature.txt"
VISUAL_DIR = HERE / "visual"
ORACLE_JSON = VISUAL_DIR / "oracle.json"

# librarian.py lives alongside this file
sys.path.insert(0, str(HERE))
import librarian   # FIX: was never imported — reading generation was bypassed entirely

def log(msg: str):
    if PRINT_LOGS:
        print(msg, flush=True)

def run_sky():
    subprocess.run(["python3", str(SKY_PY)], cwd=HERE, check=True)

def read_sky_state() -> dict:
    if not SKY_JSON.exists():
        return {}
    return json.loads(SKY_JSON.read_text(encoding="utf-8"))

def write_oracle_json(sky_state: dict):
    # FIX: was calling a hardcoded make_reading() stub; now calls librarian properly
    _stamp, headline, omens, constraint, aside = librarian.build_reading(sky_state)

    payload = {
        "utc":     datetime.now(UTC).isoformat(),
        "sky_utc": sky_state.get("utc"),
        "signature": sky_state.get("signature", []),

        # FIX: field was "reading" (string); frontend expects "reading_structured" (object)
        "reading_structured": {
            "headline":   headline,
            "omens":      omens,
            "constraint": constraint,
            "aside":      aside,
        },

        # Pass full sky data through for Celestial Log, Transits, Moon strip, etc.
        "sky": {
            "planets": sky_state.get("planets", {}),
            "aspects": sky_state.get("aspects", []),
        },
    }

    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    ORACLE_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def main():
    log("\n==============================")
    log("  ASTRA — ORACLE RUNNING")
    log("==============================\n")

    while True:
        try:
            run_sky()
            sky_state = read_sky_state()
            write_oracle_json(sky_state)
            sig_count = len(sky_state.get("signature", []))
            log(f"✅  wrote: visual/oracle.json  (tokens={sig_count})  [{datetime.now(UTC).strftime('%H:%M:%S')} UTC]")
            time.sleep(UPDATE_SECONDS)

        except KeyboardInterrupt:
            log("\n⏹  stopped (Ctrl+C)")
            break
        except Exception as e:
            log(f"\n⚠️  error: {e}\n   retrying in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
