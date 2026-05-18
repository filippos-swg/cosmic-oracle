import datetime
import json
from math import fmod

import swisseph as swe


SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}

ASPECTS = [
    ("Conjunction", 0, 8),
    ("Opposition", 180, 8),
    ("Trine", 120, 7),
    ("Square", 90, 6),
    ("Sextile", 60, 5),
]


def norm360(x: float) -> float:
    x = fmod(x, 360.0)
    return x + 360.0 if x < 0 else x


def angle_diff(a: float, b: float) -> float:
    d = abs(norm360(a) - norm360(b))
    return d if d <= 180 else 360 - d


def lon_to_sign(lon: float):
    lon = norm360(lon)
    sign_index = int(lon // 30)
    sign = SIGNS[sign_index]
    deg = lon % 30
    return sign, deg


def get_positions(jd: float):
    pos = {}
    for name, p in PLANETS.items():
        lon = swe.calc_ut(jd, p)[0][0]  # longitude only
        pos[name] = norm360(lon)
    return pos


def find_aspects(positions: dict):
    names = list(positions.keys())
    hits = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]
            ang = angle_diff(positions[a], positions[b])

            for asp_name, asp_angle, orb in ASPECTS:
                off = abs(ang - asp_angle)
                if off <= orb:
                    hits.append((off, asp_name, a, b, ang))
                    break

    hits.sort(key=lambda x: x[0])  # tightest first
    return hits


def build_signature(sky_state: dict, aspects: list, max_aspects: int = 8):
    """
    Produces compact tokens like:
      SUN_TRI_JUP
      VEN_CON_SAT
      STACK_PISCES_4
    """
    def tok(name: str) -> str:
        return name.upper()[:3]

    aspect_code = {
        "Conjunction": "CON",
        "Opposition": "OPP",
        "Trine": "TRI",
        "Square": "SQR",
        "Sextile": "SXT",
    }

    sig = []
    for off, asp, a, b, ang in aspects[:max_aspects]:
        sig.append(f"{tok(a)}_{aspect_code.get(asp, asp[:3].upper())}_{tok(b)}")

    # Add a simple “stack” token if 3+ planets are in the same sign
    sign_counts = {}
    for p, info in sky_state["planets"].items():
        s = info["sign"]
        sign_counts[s] = sign_counts.get(s, 0) + 1

    # pick the strongest stack (if any)
    stacked = [(sign, n) for sign, n in sign_counts.items() if n >= 3]
    stacked.sort(key=lambda x: x[1], reverse=True)

    if stacked:
        sign, n = stacked[0]
        sig.append(f"STACK_{sign.upper()}_{n}")

    return sig


def main():
    now = datetime.datetime.now(datetime.UTC)
    jd = swe.julday(
        now.year,
        now.month,
        now.day,
        now.hour + now.minute / 60 + now.second / 3600
    )

    positions = get_positions(jd)
    aspects = find_aspects(positions)

    # Human-readable output
    print("\nCurrent UTC:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("\nPlanet positions:\n")
    for name, lon in positions.items():
        sign, deg = lon_to_sign(lon)
        print(f"{name:8s} {sign:10s} {deg:05.2f}°")

    print("\nMajor aspects (tightest first):\n")
    if not aspects:
        print("(none within orbs)")
    else:
        for off, asp, a, b, ang in aspects[:20]:
            print(f"{a:8s} {asp:12s} {b:8s}  angle={ang:06.2f}°  orb={off:04.2f}°")

    # JSON output object
    sky_state = {
        "utc": now.isoformat(),
        "planets": {},
        "aspects": []
    }

    for name, lon in positions.items():
        sign, deg = lon_to_sign(lon)
        sky_state["planets"][name] = {"sign": sign, "degree": round(deg, 2)}

    for off, asp, a, b, ang in aspects:
        sky_state["aspects"].append({
            "type": asp,
            "planet1": a,
            "planet2": b,
            "angle": round(ang, 2),
            "orb": round(off, 2)
        })

    # Signature tokens
    signature = build_signature(sky_state, aspects, max_aspects=8)
    sky_state["signature"] = signature

    print("\nSky Signature:\n")
    for s in signature:
        print(s)

    print("\nSky JSON:\n")
    print(json.dumps(sky_state, indent=2))

    # Write JSON to file (source of truth for the rest of the system)
    with open("sky_state.json", "w", encoding="utf-8") as f:
        json.dump(sky_state, f, indent=2)

    # Write signature tokens to a plain text file (easy for visuals to read)
    with open("sky_signature.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(signature) + "\n")

    print("\nWrote: sky_state.json")
    print("Wrote: sky_signature.txt")


if __name__ == "__main__":
    main()