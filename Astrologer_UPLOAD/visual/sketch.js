// ------------------- CONFIG -------------------
const ORACLE_URL = "/oracle.json";
const UPDATE_MS = 1000;
const MODE = "both"; // "rings" | "ghost" | "both"

// ------------------- STATE -------------------
let oracle = null;
let lastError = "";

// ------------------- FETCH -------------------
async function loadOracle() {
  try {
    lastError = "";
    const res = await fetch(`${ORACLE_URL}?ts=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    oracle = await res.json();
  } catch (e) {
    lastError = String(e);
    // keep old oracle so visuals don't die when fetch hiccups
  }
}

// ------------------- P5 -------------------
function setup() {
  createCanvas(windowWidth, windowHeight);
  frameRate(60);
  textFont("monospace");

  loadOracle();
  setInterval(loadOracle, UPDATE_MS);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function draw() {
  background(0, 25);

  // Debug overlay so it never looks "dead"
  resetMatrix();
  noStroke();
  fill(255);
  textSize(14);
  text("p5 running ✓", 16, 18);

  if (lastError) {
    fill(255);
    text("fetch error: " + lastError, 16, 38);
  }

  if (!oracle) {
    fill(255);
    text("loading oracle.json…", 16, 58);
    return;
  }

  // oracle.json contains full sky in oracle.sky
  const sky = oracle.sky || {};
  const sig = Array.isArray(oracle.signature) ? oracle.signature : [];
  const planets = sky.planets || {};
  const aspects = sky.aspects || [];

  // Signature-driven intensity
  let chaos = 0.35 + sig.length * 0.08;
  if (sig.includes("STACK_PISCES_4")) chaos += 0.9;
  if (sig.includes("SUN_TRI_JUP")) chaos += 0.4;
  if (sig.includes("MOO_OPP_SAT")) chaos += 0.6;
  if (sig.includes("VEN_CON_SAT")) chaos += 0.3;

  // Scene
  translate(width / 2, height / 2);
  const t = millis() * 0.001;
  const base = min(width, height);

  if (MODE === "ghost" || MODE === "both") {
    drawGhost(base, t, chaos, sig);
  }

  if (MODE === "rings" || MODE === "both") {
    drawRings(base, t, chaos, planets, aspects);
  }

  // Overlay readout
  resetMatrix();
  noStroke();
  fill(255, 160);
  textSize(12);
  text(`Oracle UTC: ${oracle.utc || "missing"}`, 16, 22);
  fill(255, 110);
  text(`Sky UTC: ${oracle.sky_utc || "missing"}`, 16, 40);
  fill(255, 90);
  text(sig.join("  "), 16, 58);

  // Reading text
  fill(255, 140);
  textSize(13);
  const reading = (oracle.reading || "").trim();
  if (reading) {
    text(reading, 16, height - 120, width - 32, 110);
  }
}

// ------------------- VISUALS -------------------
function drawGhost(base, t, chaos, sig) {
  noFill();
  stroke(255, 120);
  strokeWeight(1.2);

  const baseRadius = base * 0.18;
  const pulse = 1 + 0.08 * sin(t * 1.7) + 0.03 * sin(t * 4.1);
  const piscesBoost = sig.includes("STACK_PISCES_4") ? 1.8 : 1.0;

  beginShape();
  for (let a = 0; a < TWO_PI; a += 0.035) {
    const nx = cos(a) + t * 0.25;
    const ny = sin(a) + t * 0.22;

    const n = noise(nx, ny);
    const warp =
      (n - 0.5) * 2.0 * 140 * chaos * piscesBoost +
      sin(a * 6 + t * 2) * 18 * chaos +
      sin(a * 13 - t * 1.3) * 9;

    const r = baseRadius * pulse + warp;
    vertex(cos(a) * r, sin(a) * r);
  }
  endShape(CLOSE);

  // orbit dust
  stroke(255, 40);
  for (let i = 0; i < 140; i++) {
    const a = i * 0.045 + t * 0.25;
    const r = baseRadius * 1.9 + sin(i + t) * 28 * chaos;
    point(cos(a) * r, sin(a) * r);
  }
}

function drawRings(base, t, chaos, planets, aspects) {
  const pnames = Object.keys(planets);
  const degrees = pnames.map(n => (planets[n]?.degree ?? 0));

  noFill();
  stroke(255, 70);
  strokeWeight(1);

  const rings = 5;
  for (let i = 0; i < rings; i++) {
    const r = base * (0.10 + i * 0.075);
    const phase = t * (0.45 + i * 0.12);

    beginShape();
    const steps = 220;
    for (let k = 0; k <= steps; k++) {
      const a = (TWO_PI * k) / steps;
      const d = degrees[i % max(1, degrees.length)];
      const mod = 0.03 + (d / 30.0) * 0.10 * chaos;

      const nr =
        r *
        (1 +
          mod * sin(a * (2 + i) + phase) +
          0.02 * sin(a * 11 + phase * 2));

      vertex(nr * cos(a), nr * sin(a));
    }
    endShape();
  }

  // aspect chords
  const planetAngles = {};
  for (const name of pnames) {
    const sign = planets[name]?.sign || "Aries";
    const deg = planets[name]?.degree ?? 0;
    planetAngles[name] = radians(signDegToLon(sign, deg));
  }

  const R = base * 0.32;
  strokeWeight(1);

  for (const asp of (aspects || []).slice(0, 12)) {
    const a = planetAngles[asp.planet1];
    const b = planetAngles[asp.planet2];
    if (a == null || b == null) continue;

    const orb = asp.orb ?? 10;
    const alpha = constrain(map(orb, 0, 8, 140, 10), 10, 140);
    stroke(255, alpha);
    line(R * cos(a), R * sin(a), R * cos(b), R * sin(b));
  }
}

// ------------------- HELPERS -------------------
function signIndex(sign) {
  const signs = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
  ];
  const idx = signs.indexOf(sign);
  return idx >= 0 ? idx : 0;
}

function signDegToLon(sign, deg) {
  return signIndex(sign) * 30 + deg;
}