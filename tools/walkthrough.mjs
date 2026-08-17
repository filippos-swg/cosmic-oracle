/* Playwright walkthrough of the ASTRA ceremony against a live server.
   Dials a birthdate, chooses a domain, steps every reading screen and reads
   kicker/body/note off the DOM. Then runs a cohort of friends on the same
   day to confirm they no longer receive matching landings and verdicts. */
import { chromium } from 'playwright';

const URL = 'http://localhost:8000/tv.html';
const wait = (p, ms) => p.waitForTimeout(ms);

async function ceremony(page, [d, m, y], domainDigit) {
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.keyboard.press('Enter');                 // skip boot
  await wait(page, 500);
  const digits = String(d).padStart(2, '0') + String(m).padStart(2, '0') + String(y);
  for (const c of digits) { await page.keyboard.press(c); await wait(page, 90); }

  // CONSULT theatre + /natal fetch, then the FILE card
  await page.waitForFunction(() => state === 'reading', null, { timeout: 20000 });
  await wait(page, 600);
  await page.keyboard.press('Enter');                 // FILE card -> CLARIFY
  await page.waitForSelector('#s-clarify.on', { timeout: 8000 });
  await wait(page, 400);
  await page.keyboard.press(domainDigit);
  await wait(page, 700);

  // renderReadingScreen paints 650ms after the fade starts — read after that,
  // or every screen comes back blank and the walkthrough silently proves nothing
  const screens = [];
  for (let i = 0; i < 14; i++) {
    await wait(page, 780);
    const s = await page.evaluate(() => ({
      k: document.getElementById('r-kicker').textContent.trim(),
      b: document.getElementById('r-body').innerText.trim(),
      n: document.getElementById('r-note').textContent.trim(),
      done: typeof state !== 'undefined' && state !== 'reading',
    }));
    if (s.done) break;
    const key = s.k + '|' + s.b;
    if (s.k && key !== (screens.at(-1) || {}).key) screens.push({ ...s, key });
    await page.keyboard.press('Enter');
  }
  return screens;
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1024, height: 768 } });
const errors = [];
page.on('pageerror', e => errors.push('pageerror: ' + e.message));
page.on('requestfailed', r => errors.push('requestfailed: ' + r.url()));
page.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) errors.push('http ' + r.status() + ': ' + r.url()); });
page.on('console', m => {
  const t = m.text();
  if (m.type() === "error" && !/favicon|Failed to load resource/i.test(t)) errors.push('console: ' + t);
});

console.log('=== FULL CEREMONY — 04/11/1979 · domain 1 (WORK) ===\n');
for (const s of await ceremony(page, [4, 11, 1979], '1')) {
  console.log(`[${s.k}]`);
  console.log(s.b.split('\n').map(l => '  ' + l).join('\n'));
  if (s.n) console.log('  ~ ' + s.n);
  console.log('');
}

console.log('=== COHORT — five visitors, same day, same domain, same sky ===\n');
const cohort = [[4, 11, 1979], [5, 11, 1979], [12, 3, 1988], [30, 6, 1995], [1, 1, 2000]];
const rows = [];
for (const dob of cohort) {
  const s = await ceremony(page, dob, '1');
  const find = k => (s.find(x => x.k.includes(k)) || {});
  const lead = s[0] || {};
  rows.push({
    dob: dob.map(n => String(n).padStart(2, '0')).join('/'),
    landing: (lead.n || '(none)').slice(0, 72),
    verdict: (find('VERDICT').b || '(none)').replace(/\n/g, ' ').slice(0, 60),
    found: (s.at(-1)?.b || '(none)').split('\n')[0].slice(0, 46),
  });
}
for (const r of rows)
  console.log(`  ${r.dob}\n    landing: ${r.landing}\n    verdict: ${r.verdict}\n    found:   ${r.found}`);

let fail = 0;
for (const [field, label] of [['landing', 'landings'], ['verdict', 'verdicts'], ['found', 'found items']]) {
  const vals = rows.map(r => r[field]);
  const n = new Set(vals).size;
  console.log(`\n  distinct ${label}: ${n}/${vals.length}`);
  if (n < 4) { console.log(`  FAIL — ${label} still collapsing across visitors`); fail++; }
}

console.log('\n=== JS ERRORS ===');
console.log(errors.length ? errors.join('\n') : '  none');
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
