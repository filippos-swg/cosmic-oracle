/* Batch-1 verification for visual/tv.html corpus + selection mechanics.
   Extracts the corpus blocks, replicates the selection formulas exactly,
   and reports pool sizes, duplicate lines, same-day collision rates across
   synthetic visitor cohorts, and day-to-day rotation for a single visitor. */
import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../visual/tv.html', import.meta.url), 'utf8');

function block(name) {
  const start = html.indexOf(`const ${name} `);
  if (start < 0) throw new Error(`missing ${name}`);
  const eq = html.indexOf('=', start);
  let i = html.indexOf(/[[{]/.test(html[eq + 1]) ? html[eq + 1] : '', eq);
  i = eq + 1;
  while (/\s/.test(html[i])) i++;
  const open = html[i], close = open === '{' ? '}' : ']';
  let depth = 0, j = i, inStr = null;
  for (; j < html.length; j++) {
    const c = html[j];
    if (inStr) {
      if (c === '\\') { j++; continue; }
      if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (!depth) break; }
  }
  return eval(`(${html.slice(i, j + 1)})`);
}

const LANDINGS = block('LANDINGS');
const VERDICTS = block('VERDICTS');
const LANDING_FRAMES = block('LANDING_FRAMES');
const FOUND_ITEMS = block('FOUND_ITEMS');
const RECORD_FORMS = block('RECORD_FORMS');
const RECORD_COLORS = block('RECORD_COLORS');
const RECORD_HOURS = block('RECORD_HOURS');
const RECORD_FORM_NOTES = block('RECORD_FORM_NOTES');

const MODES = ['Conjunction', 'Opposition', 'Trine', 'Square', 'Sextile'];
const DOMAINS = ['work', 'love', 'other'];
let fail = 0;
const bad = (m) => { console.log('  FAIL ' + m); fail++; };

/* ---- 1. pool sizes ---- */
console.log('\n[1] POOL SIZES');
for (const d of DOMAINS) for (const m of MODES) {
  const l = LANDINGS[d][m].length, v = VERDICTS[d][m].length;
  if (l !== 6) bad(`LANDINGS.${d}.${m} = ${l}, expected 6`);
  if (v !== 6) bad(`VERDICTS.${d}.${m} = ${v}, expected 6`);
}
console.log(`  LANDINGS  ${DOMAINS.length}x${MODES.length} pools of 6 = ${DOMAINS.length * MODES.length * 6} lines`);
console.log(`  VERDICTS  ${DOMAINS.length}x${MODES.length} pools of 6 = ${DOMAINS.length * MODES.length * 6} lines`);
console.log(`  LANDING_FRAMES ${LANDING_FRAMES.length}  RECORD_FORMS ${RECORD_FORMS.length}  RECORD_COLORS ${RECORD_COLORS.length}`);
if (LANDING_FRAMES.length !== 8) bad('LANDING_FRAMES expected 8');

let fi = 0;
for (const c of ['letter', 'dream']) for (const m of [...MODES, 'none']) {
  const n = FOUND_ITEMS[c].pieces[m].length;
  fi += n;
  if (n !== 4) bad(`FOUND_ITEMS.${c}.${m} = ${n}, expected 4`);
}
console.log(`  FOUND_ITEMS 2x6 pools of 4 = ${fi} pieces`);

/* ---- 2. duplicates + shape ---- */
console.log('\n[2] DUPLICATES & SHAPE');
const seenAll = new Map();
const collect = (label, arr) => arr.forEach(s => {
  const k = s.trim().toLowerCase();
  if (seenAll.has(k)) bad(`duplicate line in ${label} and ${seenAll.get(k)}: "${s.slice(0, 60)}..."`);
  else seenAll.set(k, label);
});
for (const d of DOMAINS) for (const m of MODES) {
  collect(`LANDINGS.${d}.${m}`, LANDINGS[d][m]);
  collect(`VERDICTS.${d}.${m}`, VERDICTS[d][m]);
}
collect('LANDING_FRAMES', LANDING_FRAMES);
for (const c of ['letter', 'dream']) for (const m of [...MODES, 'none'])
  collect(`FOUND_ITEMS.${c}.${m}`, FOUND_ITEMS[c].pieces[m]);
collect('RECORD_FORMS', RECORD_FORMS);
collect('RECORD_COLORS', RECORD_COLORS);
collect('RECORD_HOURS', RECORD_HOURS);
collect('RECORD_FORM_NOTES', RECORD_FORM_NOTES);

// every FOR THE RECORD line has to mean something to a stranger: a bare form
// number is the archive talking to itself, so each one carries a note
if (RECORD_FORMS.length !== RECORD_FORM_NOTES.length)
  bad('RECORD_FORMS and RECORD_FORM_NOTES are not index-parallel — the wrong note would print');
RECORD_FORMS.forEach((f, i) => {
  const note = RECORD_FORM_NOTES[i] || '';
  const num = f.replace(/ REV\.$/, '');
  if (!note.includes(num)) bad(`RECORD_FORM_NOTES[${i}] does not name form ${f}: "${note}"`);
});
// the card column wraps at roughly 22 characters
const LINE_MAX = 22;
// every value sits on its own line under its label — none may exceed the column
for (const h of RECORD_HOURS)
  if (h.length > LINE_MAX) bad(`hour too long for the column: "${h}"`);
for (const f of RECORD_FORMS)
  if (f.length > 12) bad(`form id too long for the column: "${f}"`);
for (const c of RECORD_COLORS)
  if (c.length > LINE_MAX) bad(`colour too long for the column: "${c}"`);

// one frame and one stamp for the found item, whichever container it came from
for (const name of ['FOUND_FRAME', 'FOUND_STAMP'])
  if (!new RegExp(`const ${name}\\s*=\\s*'`).test(html))
    bad(`${name} is not a single constant — the found item can be framed two ways again`);
for (const c of ['letter', 'dream'])
  if (FOUND_ITEMS[c].frame || FOUND_ITEMS[c].stamp)
    bad(`FOUND_ITEMS.${c} still carries its own frame/stamp`);

// landings are clauses that follow a frame: must start lowercase
for (const d of DOMAINS) for (const m of MODES) for (const s of LANDINGS[d][m])
  if (/^[A-Z]/.test(s)) bad(`LANDINGS.${d}.${m} starts uppercase: "${s.slice(0, 40)}"`);
// verdicts are the plain register: must start uppercase and end in a stop
for (const d of DOMAINS) for (const m of MODES) for (const s of VERDICTS[d][m]) {
  if (!/^[A-Z]/.test(s)) bad(`VERDICTS.${d}.${m} starts lowercase: "${s.slice(0, 40)}"`);
  if (!/[.!?]$/.test(s)) bad(`VERDICTS.${d}.${m} unterminated: "${s.slice(0, 40)}"`);
}
// found items: exactly four lines each
for (const c of ['letter', 'dream']) for (const m of [...MODES, 'none'])
  FOUND_ITEMS[c].pieces[m].forEach(p => {
    const n = p.split('\n').length;
    if (n !== 4) bad(`FOUND_ITEMS.${c}.${m} has ${n} lines, expected 4`);
  });
// dreams witness, they do not address: no second person
for (const m of [...MODES, 'none']) FOUND_ITEMS.dream.pieces[m].forEach(p => {
  const hit = p.match(/\b(you|your|yours)\b/i);
  if (hit) bad(`FOUND_ITEMS.dream.${m} addresses the visitor ("${hit[0]}"): "${p.split('\n')[0]}"`);
});
// letters address
for (const m of [...MODES, 'none']) FOUND_ITEMS.letter.pieces[m].forEach(p => {
  if (!/\b(you|your|yours)\b/i.test(p))
    bad(`FOUND_ITEMS.letter.${m} never addresses the visitor: "${p.split('\n')[0]}"`);
});
if (!fail) console.log('  no duplicates; register and shape hold');

/* ---- 3. selection formulas, verbatim from buildMainScreens ---- */
// mirrors tv.html; the assert below fails loudly if the source drifts
const SEED_SRC = 'const seed = (dob.y || 0) * 372 + (dob.m || 0) * 31 + (dob.d || 0);';
if (!html.includes(SEED_SRC)) bad('seed expression in tv.html no longer matches this harness');
const seedOf = (d, m, y) => y * 372 + m * 31 + d;

/* the seed must be injective over real dates — two different birthdates
   sharing a seed means two visitors receive a byte-identical reading */
{
  const seen = new Map(); let clash = 0, ex = null;
  for (let y = 1935; y <= 2020; y++) for (let m = 1; m <= 12; m++) for (let d = 1; d <= 31; d++) {
    const s = seedOf(d, m, y);
    if (seen.has(s)) { clash++; ex = ex || [seen.get(s), [d, m, y]]; }
    else seen.set(s, [d, m, y]);
  }
  console.log(`\n[0] SEED INJECTIVITY — ${seen.size} distinct seeds over ${86 * 12 * 31} dates`);
  if (clash) bad(`${clash} birthdate pairs share a seed, e.g. ${JSON.stringify(ex)}`);
  else console.log('  no two birthdates share a seed');
}

// pickIdx lifted verbatim out of tv.html — if the source changes, this fails loudly
const pickSrc = html.slice(html.indexOf('function pickIdx'), html.indexOf('const SALT'));
const pickIdx = eval(`(${pickSrc.trim()})`);
const SALT = eval('(' + html.slice(html.indexOf('const SALT = {') + 'const SALT = '.length,
  html.indexOf('};', html.indexOf('const SALT = {')) + 1) + ')');

const sel = (seed, dnum, dk, type) => ({
  frame: LANDING_FRAMES[pickIdx(seed, dnum, SALT.frame, LANDING_FRAMES.length)],
  landing: LANDINGS[dk][type][pickIdx(seed, dnum, SALT.landing, LANDINGS[dk][type].length)],
  verdict: VERDICTS[dk][type][pickIdx(seed, dnum, SALT.verdict, VERDICTS[dk][type].length)],
  form: RECORD_FORMS[pickIdx(seed, dnum, SALT.form, RECORD_FORMS.length)],
  color: RECORD_COLORS[pickIdx(seed, dnum, SALT.color, RECORD_COLORS.length)],
  found: (() => {
    const container = pickIdx(seed, dnum, SALT.container, 2) === 0 ? 'letter' : 'dream';
    const pool = FOUND_ITEMS[container].pieces[type];
    return container + '|' + pool[pickIdx(seed, dnum, SALT.piece, pool.length)];
  })(),
});

/* ---- 4. same-day cohort collisions (the friends-comparing case) ---- */
console.log('\n[3] SAME-DAY COLLISIONS — cohorts of 6 friends, same domain, same lead transit');
const dnum = Math.floor(Date.UTC(2026, 7, 14) / 86400000);
let pairs = 0, cl = 0, cv = 0, cb = 0, cf = 0;
const rnd = (n => () => (n = (n * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff)(42);
for (let trial = 0; trial < 4000; trial++) {
  const dk = DOMAINS[Math.floor(rnd() * 3)], type = MODES[Math.floor(rnd() * 5)];
  const cohort = Array.from({ length: 6 }, () => seedOf(
    1 + Math.floor(rnd() * 28), 1 + Math.floor(rnd() * 12), 1960 + Math.floor(rnd() * 45)));
  for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
    if (cohort[i] === cohort[j]) continue;   // identical dob: identical reading is correct
    const a = sel(cohort[i], dnum, dk, type), b = sel(cohort[j], dnum, dk, type);
    pairs++;
    const l = a.landing === b.landing, v = a.verdict === b.verdict;
    if (l) cl++; if (v) cv++; if (l && v) cb++;
    if (a.found === b.found) cf++;
  }
}
const pc = n => (100 * n / pairs).toFixed(1) + '%';
console.log(`  pairs compared: ${pairs}`);
console.log(`  same landing             ${pc(cl)}   (was 50.0% at pool 2)`);
console.log(`  same verdict             ${pc(cv)}   (was 50.0% at pool 2)`);
console.log(`  same landing AND verdict ${pc(cb)}   (was 25.0% at pool 2; 2.8% if independent)`);
console.log(`  same found item          ${pc(cf)}   (was 25.0% at pool 2)`);
if (cb / pairs > 0.05) bad('landing+verdict collision above 5% — the pools are correlated');
if (cf / pairs > 0.18) bad('found-item collision above 18% — container and piece are correlated');

/* ---- 5. day rotation for one returning visitor ---- */
console.log('\n[4] DAY ROTATION — one visitor, same domain and transit, consecutive days');
// coupon-collector: 6 slots sampled independently need ~15 draws on average to
// cover, so 14 days covering 5/6 is correct behaviour. 40 days must cover all.
for (const [d, m, y] of [[4, 11, 1979], [23, 2, 1991], [1, 7, 1966]]) {
  const s1 = seedOf(d, m, y);
  const at = k => sel(s1, dnum + k, 'work', 'Square');
  const setOf = (n, f) => new Set(Array.from({ length: n }, (_, k) => f(at(k))));
  const L14 = setOf(14, r => r.landing), V14 = setOf(14, r => r.verdict);
  const L40 = setOf(40, r => r.landing), V40 = setOf(40, r => r.verdict),
        F40 = setOf(40, r => r.found);
  console.log(`  ${String(d).padStart(2)}/${String(m).padStart(2)}/${y}` +
    `  14d: landing ${L14.size}/6 verdict ${V14.size}/6` +
    `  |  40d: landing ${L40.size}/6 verdict ${V40.size}/6 found ${F40.size}/8`);
  if (L14.size < 4 || V14.size < 4) bad(`${d}/${m}/${y}: fewer than 4 distinct in a fortnight`);
  if (L40.size < 6 || V40.size < 6) bad(`${d}/${m}/${y}: pool not fully reachable in 40 days`);
}

/* ---- 6. every entry is reachable, and the spread is even ---- */
console.log('\n[5] REACHABILITY — no line may be unreachable for real dialled dates');
const realSeeds = [];
for (let y = 1935; y <= 2020; y++) for (let m = 1; m <= 12; m++) for (let d = 1; d <= 28; d++)
  realSeeds.push(seedOf(d, m, y));
for (const [salt, len, what] of [[SALT.landing, 6, 'landing'], [SALT.verdict, 6, 'verdict'],
[SALT.frame, 8, 'frame'], [SALT.piece, 4, 'found piece'], [SALT.container, 2, 'container'],
[SALT.form, RECORD_FORMS.length, 'form'], [SALT.color, RECORD_COLORS.length, 'color'],
[SALT.shelf, RECORD_HOURS.length, 'hour']]) {
  const hits = new Array(len).fill(0);
  realSeeds.forEach(s => hits[pickIdx(s, dnum, salt, len)]++);
  const min = Math.min(...hits), max = Math.max(...hits), mean = realSeeds.length / len;
  const skew = ((max - min) / mean * 100).toFixed(1);
  console.log(`  ${what.padEnd(12)} all ${String(len).padEnd(2)} reachable, spread ±${skew}% of even`);
  if (min === 0) bad(`${what}: some entries never selected across 28,896 real birthdates`);
  if (max - min > mean * 0.35) bad(`${what}: distribution skewed ${skew}%`);
}

console.log('\n' + (fail ? `${fail} FAILURE(S)` : 'ALL CHECKS PASSED'));
process.exit(fail ? 1 : 0);
