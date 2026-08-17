/* Input and recovery paths for the kiosk — everything the happy-path
   walkthrough does not touch. A rotary dial is the only input this
   installation has and nobody is standing next to it, so every one of these
   has to end with the machine back at IDLE, ready for the next visitor. */
import { chromium } from 'playwright';

const URL = 'http://localhost:8000/tv.html';
let fail = 0, ran = 0;
const results = [];

function check(name, ok, detail = '') {
  ran++;
  if (!ok) fail++;
  results.push(`  ${ok ? 'pass' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
}

const wait = (p, ms) => p.waitForTimeout(ms);
const state = p => p.evaluate(() => (typeof state !== 'undefined' ? state : '?'));
const err = p => p.evaluate(() => document.getElementById('h-error')?.textContent.trim() || '');
const slots = p => p.evaluate(() =>
  [...document.querySelectorAll('#slots .slot')].map(s => s.textContent).join('') || '');

async function fresh(browser, opts = {}) {
  const page = await browser.newPage({ viewport: { width: 1024, height: 768 } });
  page.on('pageerror', e => { console.log('    pageerror: ' + e.message); fail++; });
  if (opts.route) await page.route(...opts.route);
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.keyboard.press('Enter');            // skip boot
  await wait(page, 400);
  if (opts.config) await page.evaluate(c => Object.assign(CONFIG, c), opts.config);
  return page;
}

async function dial(page, digits, gap = 80) {
  for (const c of String(digits)) { await page.keyboard.press(c); await wait(page, gap); }
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

/* 1 — an impossible date must be refused and recoverable */
{
  const p = await fresh(browser);
  await dial(p, '31021990');
  await wait(p, 1200);
  check('invalid date (31 Feb) is refused', /DOES NOT RECOGNIZE/.test(await err(p)), await err(p));
  await wait(p, 2500);
  await dial(p, '04111979');
  await p.waitForFunction(() => state === 'consult' || state === 'reading', null, { timeout: 15000 })
    .then(() => check('can dial a valid date after a refusal', true))
    .catch(() => check('can dial a valid date after a refusal', false, 'stuck in ' + '?'));
  await p.close();
}

/* 2 — redialling DURING the error message must not be wiped by it.
       A rotary dial takes ~1.5s per digit; the 2.2s reset lands mid-dial. */
{
  const p = await fresh(browser);
  await dial(p, '31021990');
  await wait(p, 600);                       // error is showing, reset pending
  await dial(p, '0411', 250);               // visitor starts redialling immediately
  await wait(p, 2200);                      // the pending reset fires here
  const s = await slots(p);
  check('redial during the error window survives the reset', s.startsWith('0411'),
        `slots read "${s}" — the visitor's digits were erased mid-dial`);
  await p.close();
}

/* 3 — 000 mid-entry clears the slate (the dial has no backspace) */
{
  const p = await fresh(browser);
  await dial(p, '12000');
  await wait(p, 400);
  check('000 mid-entry clears the slate', /SLATE IS CLEARED/.test(await err(p)), await err(p));
  check('000 reset empties the slots', (await slots(p)) === '');
  await p.close();
}

/* 4 — but a birthdate ENDING in 000 must pass through untouched */
{
  const p = await fresh(browser);
  await dial(p, '01012000');
  const ok = await p.waitForFunction(() => state === 'consult' || state === 'reading',
    null, { timeout: 15000 }).then(() => true).catch(() => false);
  check('born in 2000 is not eaten by the 000 reset', ok);
  await p.close();
}

/* 5 — a visitor who walks away mid-entry returns the machine to IDLE */
{
  const p = await fresh(browser, { config: { IDENTIFY_TIMEOUT_MS: 2000 } });
  await dial(p, '0411');
  await wait(p, 3200);
  check('abandoned entry times out to IDLE', (await state(p)) === 'idle', await state(p));
  await p.close();
}

/* 6 — Escape abandons cleanly from IDENTIFY */
{
  const p = await fresh(browser);
  await dial(p, '0411');
  await p.keyboard.press('Escape');
  await wait(p, 500);
  check('Escape abandons entry', (await state(p)) === 'idle', await state(p));
  await p.close();
}

/* 7 — letters and punctuation from a stray keyboard are ignored */
{
  const p = await fresh(browser);
  await dial(p, '04');
  for (const k of ['a', 'z', 'Tab', 'Shift', '-', '/']) { await p.keyboard.press(k); }
  await wait(p, 300);
  check('non-digits are ignored during entry', (await slots(p)) === '04', await slots(p));
  await p.close();
}

/* 8 — THE KIOSK KILLER: /natal accepted but never answered.
       enterConsult polls every 250ms for natalResult and CONSULT takes no
       input at all, so if the fetch never settles the machine is bricked
       until someone power-cycles it. */
{
  const p = await fresh(browser, {
    route: ['**/natal**', route => { /* accept and never respond */ }],
  });
  await dial(p, '04111979');
  const escaped = await p.waitForFunction(() => state === 'reading', null, { timeout: 30000 })
    .then(() => true).catch(() => false);
  check('hung /natal still reaches the reading', escaped,
        escaped ? '' : 'stuck in CONSULT for 30s with no input accepted — needs a power cycle');
  await p.close();
}

/* 9 — /natal erroring is fine: there is an offline sign table */
{
  const p = await fresh(browser, {
    route: ['**/natal**', route => route.fulfill({ status: 500, body: 'nope' })],
  });
  await dial(p, '04111979');
  const ok = await p.waitForFunction(() => state === 'reading', null, { timeout: 20000 })
    .then(() => true).catch(() => false);
  check('/natal 500 falls back to the offline sign table', ok);
  await p.close();
}

/* 10 — oracle.json unreachable: say so, and still give the visitor a reading */
{
  const p = await fresh(browser, {
    route: ['**/oracle.json**', route => route.fulfill({ status: 503, body: '' })],
  });
  await wait(p, 1200);
  const banner = await p.evaluate(() => {
    const el = document.getElementById('signal-lost');
    return el && el.style.display !== 'none' ? el.textContent : '';
  });
  check('stale sky shows SIGNAL LOST', /SIGNAL LOST/.test(banner), banner);
  await dial(p, '04111979');
  const ok = await p.waitForFunction(() => state === 'reading', null, { timeout: 20000 })
    .then(() => true).catch(() => false);
  check('ceremony still runs with no oracle.json', ok);
  await p.close();
}

/* 11 — mashing the dial does not desync the slots */
{
  const p = await fresh(browser);
  await dial(p, '0411197904111979', 15);
  await wait(p, 800);
  const s = await slots(p);
  check('input beyond 8 digits is dropped', s.length <= 8, `slots read "${s}"`);
  await p.close();
}

console.log('\n=== KIOSK EDGE CASES ===\n');
console.log(results.join('\n'));
console.log(`\n  ${ran - fail}/${ran} passed`);
await browser.close();
process.exit(fail ? 1 : 0);
