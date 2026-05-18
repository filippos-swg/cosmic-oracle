import json
import time
import subprocess
from datetime import datetime, UTC
from pathlib import Path

UPDATE_SECONDS = 1
PRINT_LOGS = True

HERE = Path(__file__).resolve().parent

SKY_PY = HERE / "sky.py"
SKY_JSON = HERE / "sky_state.json"          # <-- matches your file tree
SIG_TXT = HERE / "sky_signature.txt"        # <-- matches your file tree

VISUAL_DIR = HERE / "visual"
ORACLE_JSON = VISUAL_DIR / "oracle.json"    # <-- IMPORTANT: goes into visual/


def log(msg: str):
    if PRINT_LOGS:
        print(msg, flush=True)


def run_sky():
    # Ensure it runs in the project root where sky.py + venv live
    subprocess.run(["python", str(SKY_PY)], cwd=HERE, check=True)


def read_signature_tokens():
    if not SIG_TXT.exists():
        return []
    tokens = [line.strip() for line in SIG_TXT.read_text(encoding="utf-8").splitlines()]
    return [t for t in tokens if t]


def read_sky_state():
    if not SKY_JSON.exists():
        return {}
    return json.loads(SKY_JSON.read_text(encoding="utf-8"))


def make_reading(signature_tokens, sky_state):
    sun = (sky_state.get("planets") or {}).get("Sun") or {}
    moon = (sky_state.get("planets") or {}).get("Moon") or {}

    sun_txt = f"Sun in {sun.get('sign','?')} at {sun.get('degree','?')}°"
    moon_txt = f"Moon in {moon.get('sign','?')} at {moon.get('degree','?')}°"

    return (
        "Don’t confuse luck with immortality. Still check the numbers.\n\n"
        f"Aside: Administrative note from the stacks: {sun_txt} and {moon_txt}."
    )


def write_oracle_json(signature_tokens, sky_state, reading_text):
    payload = {
        "utc": datetime.now(UTC).isoformat(),
        "sky_utc": sky_state.get("utc"),
        "signature": signature_tokens,
        "reading": reading_text,
        "sky": sky_state,  # keep full sky here for p5
    }

    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    ORACLE_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    log("\n==============================")
    log("   COSMIC ORACLE — RUNNING")
    log("==============================\n")

    while True:
        try:
            run_sky()

            sig = read_signature_tokens()
            sky_state = read_sky_state()
            reading = make_reading(sig, sky_state)

            write_oracle_json(sig, sky_state, reading)

            log(f"✅ wrote: visual/oracle.json   (tokens={len(sig)})")
            time.sleep(UPDATE_SECONDS)

        except KeyboardInterrupt:
            log("\n🛑 stopped (Ctrl+C)")
            break
        except Exception as e:
            log(f"\n⚠️ error: {e}\nretrying in 3s...")
            time.sleep(3)


if __name__ == "__main__":
    main()