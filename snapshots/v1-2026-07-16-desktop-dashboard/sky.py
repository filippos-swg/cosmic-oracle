import datetime
from datetime import timezone
import json
from math import fmod
import swisseph as swe

# Python 3.9 compat
datetime.UTC = timezone.utc

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = {
    "Sun":     swe.SUN,
    "Moon":    swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus":   swe.VENUS,
    "Mars":    swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn":  swe.SATURN,
    "Uranus":  swe.URANUS,    # FIX: was missing
    "Neptune": swe.NEPTUNE,   # FIX: was missing
    "Pluto":   swe.PLUTO,     # FIX: was missing
}

ASPECTS = [
    ("Conjunction", 0,   8),
    ("Opposition",  180, 8),
    ("Trine",       120, 7),
    ("Square",      90,  6),
    ("Sextile",     60,  5),
]

# Speed rank: lower = faster-moving. Used to prioritise the signature so
# slow outer-planet aspects (which hold near-exact orbs for months) don't
# permanently crowd out the fast, day-defining aspects. Per the brief:
# Moon outweighs planets.
SPEED_RANK = {
    "Moon": 0, "Mercury": 1, "Venus": 2, "Sun": 3, "Mars": 4,
    "Jupiter": 5, "Saturn": 6, "Uranus": 7, "Neptune": 8, "Pluto": 9,
}

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
    """Returns (positions, speeds) — longitude in degrees, speed in deg/day."""
    pos = {}
    spd = {}
    for name, p in PLANETS.items():
        xx = swe.calc_ut(jd, p)[0]
        pos[name] = norm360(xx[0])
        spd[name] = xx[3]  # longitudinal speed, negative = retrograde
    return pos, spd

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
    hits.sort(key=lambda x: x[0])
    return hits

def is_applying(hit, positions_later):
    """True if the aspect's orb is shrinking (applying), False if separating."""
    off, asp_name, a, b, ang = hit
    asp_angle = next(x[1] for x in ASPECTS if x[0] == asp_name)
    ang_later = angle_diff(positions_later[a], positions_later[b])
    return abs(ang_later - asp_angle) < off

def build_signature(sky_state: dict, aspects: list, max_aspects: int = 8):
    def tok(name: str) -> str:
        return name.upper()[:3]

    aspect_code = {
        "Conjunction": "CON",
        "Opposition":  "OPP",
        "Trine":       "TRI",
        "Square":      "SQR",
        "Sextile":     "SXT",
    }

    # Prioritise aspects involving fast-moving planets, then tightness.
    # Otherwise Uranus/Neptune/Pluto aspects (near-exact for months) would
    # occupy the token budget permanently and the signature would freeze.
    ordered = sorted(
        aspects,
        key=lambda h: (min(SPEED_RANK.get(h[2], 9), SPEED_RANK.get(h[3], 9)), h[0]),
    )

    sig = []
    for off, asp, a, b, ang in ordered[:max_aspects]:
        sig.append(f"{tok(a)}_{aspect_code.get(asp, asp[:3].upper())}_{tok(b)}")

    sign_counts = {}
    for p, info in sky_state["planets"].items():
        s = info["sign"]
        sign_counts[s] = sign_counts.get(s, 0) + 1

    stacked = [(sign, n) for sign, n in sign_counts.items() if n >= 3]
    stacked.sort(key=lambda x: x[1], reverse=True)
    if stacked:
        sign, n = stacked[0]
        sig.append(f"STACK_{sign.upper()}_{n}")

    return sig

def main():
    now = datetime.datetime.now(datetime.UTC)
    jd = swe.julday(
        now.year, now.month, now.day,
        now.hour + now.minute / 60 + now.second / 3600
    )

    positions, speeds = get_positions(jd)
    aspects   = find_aspects(positions)

    # Positions a half-hour ahead — used to tell applying from separating
    positions_later, _ = get_positions(jd + 0.02)

    print("\nCurrent UTC:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("\nPlanet positions:\n")
    for name, lon in positions.items():
        sign, deg = lon_to_sign(lon)
        print(f"  {name:8s}  {sign:12s}  {deg:05.2f}°")

    print("\nMajor aspects (tightest first):\n")
    if not aspects:
        print("  (none within orbs)")
    else:
        for off, asp, a, b, ang in aspects[:20]:
            print(f"  {a:8s}  {asp:12s}  {b:8s}  angle={ang:06.2f}°  orb={off:04.2f}°")

    sky_state = {
        "utc":      now.isoformat(),
        "planets":  {},
        "aspects":  [],
    }

    for name, lon in positions.items():
        sign, deg = lon_to_sign(lon)
        sky_state["planets"][name] = {
            "sign":       sign,
            "degree":     round(deg, 2),
            "speed":      round(speeds[name], 4),
            "retrograde": speeds[name] < 0,
        }

    for hit in aspects:
        off, asp, a, b, ang = hit
        sky_state["aspects"].append({
            "type":     asp,
            "planet1":  a,
            "planet2":  b,
            "angle":    round(ang, 2),
            "orb":      round(off, 2),
            "applying": is_applying(hit, positions_later),
        })

    signature = build_signature(sky_state, aspects, max_aspects=8)
    sky_state["signature"] = signature

    print("\nSky Signature:\n")
    for s in signature:
        print(f"  {s}")

    with open("sky_state.json", "w", encoding="utf-8") as f:
        json.dump(sky_state, f, indent=2)

    with open("sky_signature.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(signature) + "\n")

    print("\nWrote: sky_state.json")
    print("Wrote: sky_signature.txt\n")

if __name__ == "__main__":
    main()
