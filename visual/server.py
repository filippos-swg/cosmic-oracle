from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json
import os
import sys

PORT = 8000
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import librarian  # transit line composition (same voice as the readings)

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

try:
    import swisseph as swe
    HAVE_SWE = True
except ImportError:
    HAVE_SWE = False


ASPECTS = [
    ("Conjunction", 0,   8),
    ("Opposition",  180, 8),
    ("Trine",       120, 7),
    ("Square",      90,  6),
    ("Sextile",     60,  5),
]


def natal(day: int, month: int, year: int) -> dict:
    """Natal sun and moon from a date of birth, computed at 12:00 UT.
    Sun sign is exact except within ~hours of a cusp; moon sign is correct
    ~93% of the time without a birth time (the moon moves ~13°/day)."""
    jd = swe.julday(year, month, day, 12.0)
    sun = swe.calc_ut(jd, swe.SUN)[0][0] % 360.0
    moon = swe.calc_ut(jd, swe.MOON)[0][0] % 360.0
    result = {
        "sun_sign":  SIGNS[int(sun // 30)],
        "sun_deg":   round(sun % 30, 2),
        "moon_sign": SIGNS[int(moon // 30)],
        "moon_deg":  round(moon % 30, 2),
        "moon_confidence": "approximate (noon UT assumed)",
        "transits":  find_transits(sun, moon),
    }
    return result


def find_transits(natal_sun_lon: float, natal_moon_lon: float, max_hits: int = 2):
    """Aspects from the CURRENT sky (sky_state.json, written by oracle.py)
    to the visitor's natal Sun and Moon — this is what makes two birthdates
    genuinely different readings on the same day. Tightest orbs first."""
    try:
        sky = json.loads((ROOT / "sky_state.json").read_text(encoding="utf-8"))
    except Exception:
        return []
    hits = []
    for name, info in sky.get("planets", {}).items():
        try:
            lon = SIGNS.index(info["sign"]) * 30 + info["degree"]
        except (ValueError, KeyError):
            continue
        for target, tlon in (("Sun", natal_sun_lon), ("Moon", natal_moon_lon)):
            d = abs(lon - tlon) % 360.0
            if d > 180.0:
                d = 360.0 - d
            for asp_name, asp_angle, orb in ASPECTS:
                off = abs(d - asp_angle)
                if off <= orb:
                    hits.append((off, name, asp_name, target))
                    break
    hits.sort(key=lambda h: h[0])
    # prefer diverse hits: skip a repeat of the same planet+aspect pair
    seen, picked = set(), []
    for h in hits:
        key = (h[1], h[2])
        if key in seen:
            continue
        seen.add(key)
        picked.append(h)
        if len(picked) == max_hits:
            break
    out = []
    for off, name, asp_name, target in picked:
        composed = librarian.compose_transit(name, asp_name, target) or {}
        out.append({
            "planet": name, "type": asp_name, "target": target,
            "orb": round(off, 2),
            "approx": target == "Moon",   # natal moon assumes noon birth
            "line": composed.get("line", ""),
            "note": composed.get("note", ""),
        })
    return out


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path == "/natal":
            return self.handle_natal()
        return super().do_GET()

    def handle_natal(self):
        try:
            qs = parse_qs(urlparse(self.path).query)
            d = int(qs["d"][0]); m = int(qs["m"][0]); y = int(qs["y"][0])
            if not (1 <= d <= 31 and 1 <= m <= 12 and 1900 <= y <= 2100):
                raise ValueError("out of range")
            if not HAVE_SWE:
                raise RuntimeError("swisseph not installed")
            payload = natal(d, m, y)
            body = json.dumps(payload).encode()
            self.send_response(200)
        except Exception as e:
            body = json.dumps({"error": str(e)}).encode()
            self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # quiet kiosk logs


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"ASTRA local server: http://localhost:{PORT}/")
    print(f"  dashboard: /index.html   installation: /tv.html   calibration: /testcard.html")
    print(f"  natal API: /natal?d=21&m=3&y=1985   (swisseph: {'ok' if HAVE_SWE else 'MISSING'})")
    ThreadingHTTPServer(("localhost", PORT), Handler).serve_forever()
