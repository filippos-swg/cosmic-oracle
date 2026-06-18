import json
import sys
import time
import subprocess
from datetime import datetime, timezone
from pathlib import Path

UPDATE_SECONDS = 60  # planets move on minutes/hours, not seconds

PRINT_LOGS = True

HERE = Path(__file__).resolve().parent

# Ensure librarian.py is importable regardless of working directory
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from librarian import build_reading  # noqa: E402 (import after sys.path)

SKY_PY    = HERE / "sky.py"
SKY_JSON  = HERE / "sky_state.json"
VISUAL_DIR = HERE / "visual"
ORACLE_JSON = VISUAL_DIR / "oracle.json"


def log(msg: str):
    if PRINT_LOGS:
        print(msg, flush=True)


def run_sky():
    subprocess.run([sys.executable, str(SKY_PY)], cwd=HERE, check=True)


def read_sky_state():
    if not SKY_JSON.exists():
        return {}
    return json.loads(SKY_JSON.read_text(encoding="utf-8"))


def write_oracle_json(sky_state, stamp, headline, omens, constraint, aside):
    # reading: single string — backward compatible with current p5 visual
    reading_text = "\n\n".join([
        headline,
        "\n".join(f"- {o}" for o in omens),
        constraint,
        aside,
    ])

    payload = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "sky_utc": sky_state.get("utc"),
        "signature": sky_state.get("signature", []),
        "reading": reading_text,
        "reading_structured": {
            "stamp": stamp,
            "headline": headline,
            "omens": omens,
            "constraint": constraint,
            "aside": aside,
        },
        "sky": sky_state,
    }

    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    ORACLE_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    log("\n==============================")
    log(" ASTRA — RUNNING")
    log("==============================\n")

    while True:
        try:
            run_sky()
            sky_state = read_sky_state()
            stamp, headline, omens, constraint, aside = build_reading(sky_state)
            write_oracle_json(sky_state, stamp, headline, omens, constraint, aside)
            log(f"✅ wrote: visual/oracle.json  tokens={len(sky_state.get('signature', []))}")
            time.sleep(UPDATE_SECONDS)

        except KeyboardInterrupt:
            log("\n🛑 stopped (Ctrl+C)")
            break

        except Exception as e:
            log(f"\n⚠️ error: {e}\nretrying in 10s...")
            time.sleep(10)


if __name__ == "__main__":
    main()
