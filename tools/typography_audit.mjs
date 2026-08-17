/* Typographic audit of the reading screens.

   The reported problem was a rendered line holding a single word — "bend",
   "owner.", "6-M." — which a corpus check cannot catch, because the corpus is
   fine and the LAYOUT is what breaks it. So this measures actual rendered line
   boxes: it walks every text node, groups characters by their vertical
   position, reconstructs each visual line, and flags any line that holds one
   word while its block holds more than one line.

   Runs the ceremony across several birthdates and all three domains, so it
   sees the real spread of corpus lengths rather than one lucky reading. */
import { chromium } from 'playwright';

// resolve the preview next to the repo, not an absolute path from whichever
// machine built this. ASTRA_URL overrides (e.g. http://localhost:8000/tv.html
// to audit the served page instead of the preview build).
const URL = process.env.ASTRA_URL ||
  new global.URL('../visual/preview.html', import.meta.url).href;
const DATES = [[4, 11, 1979], [23, 2, 1991], [1, 7, 1966], [30, 6, 1995], [12, 3, 1988]];
const DOMAINS = ['1', '2', '3'];

const MEASURE_LINE = `
(root) => {
  // Measure per BLOCK, not per element tree. FOR THE RECORD renders each
  // label and value as its own display:block span — one deliberate line each,
  // which is not the same thing as a wrapped line left holding one word.
  // Treating the whole card as one run reported six false orphans.
  const blocks = [];
  const kids = [...root.children].filter(el => getComputedStyle(el).display !== 'inline');
  const targets = kids.length
    ? kids.flatMap(k => [...k.children].length ? [...k.children] : [k])
    : [root];

  const range = document.createRange();
  for (const node of targets) {
    if (!node.textContent.trim()) continue;
    const lines = [];
    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    let t;
    while ((t = walker.nextNode())) {
      if (!t.data.trim()) continue;
      let curTop = null, cur = '';
      for (let i = 0; i < t.data.length; i++) {
        range.setStart(t, i); range.setEnd(t, i + 1);
        const rects = range.getClientRects();
        if (!rects.length) { cur += t.data[i]; continue; }
        const top = Math.round(rects[0].top);
        if (curTop === null) curTop = top;
        if (top !== curTop) { lines.push(cur); cur = ''; curTop = top; }
        cur += t.data[i];
      }
      if (cur.trim()) lines.push(cur);
    }
    const pre = getComputedStyle(node).whiteSpace.startsWith('pre');
    blocks.push({
      lines: lines.map(l => l.trim()).filter(Boolean),
      authored: pre ? node.textContent.trim().split(String.fromCharCode(10)).filter(x => x.trim()).length : null,
    });
  }
  return blocks;
}`;

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1300, height: 731 } });
const orphans = [], overlong = [], errs = [];
page.on('pageerror', e => errs.push(e.message));
let screensChecked = 0;

for (const dob of DATES) {
  for (const domain of DOMAINS) {
    await page.goto(URL);
    await page.waitForTimeout(1100);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(350);
    for (const c of dob.map(n => String(n).padStart(2, '0')).join('').replace(/^(\d\d)(\d\d)(\d+)$/, '$1$2$3')) {
      await page.keyboard.press(c); await page.waitForTimeout(55);
    }
    await page.waitForFunction(() => state === 'reading', null, { timeout: 20000 });
    await page.waitForTimeout(600);
    await page.keyboard.press('Enter');
    await page.waitForSelector('#s-clarify.on', { timeout: 8000 });
    await page.waitForTimeout(300);
    await page.keyboard.press(domain);
    await page.waitForTimeout(800);

    for (let i = 0; i < 13; i++) {
      await page.waitForTimeout(760);
      const s = await page.evaluate(([fnSrc]) => {
        const measure = eval(fnSrc);
        if (state !== 'reading') return { done: true };
        return {
          k: document.getElementById('r-kicker').textContent.trim(),
          body: measure(document.getElementById('r-body')),
          note: measure(document.getElementById('r-note')),
        };
      }, [MEASURE_LINE]);
      if (s.done) break;
      screensChecked++;
      for (const [where, blocks] of [['body', s.body], ['note', s.note]]) {
        for (const blk of blocks) {
          const lines = blk.lines;
          // pre-line blocks (the found item) carry authored breaks: any line
          // beyond the authored count means the layout wrapped one of them
          if (blk.authored !== null) {
            if (lines.length > blk.authored)
              orphans.push({ screen: s.k, where, of: lines.length,
                             line: `wrapped: ${lines.length} rendered vs ${blk.authored} authored` });
            continue;
          }
          if (lines.length < 2) continue;
          lines.forEach((line, idx) => {
            if (line.split(/\s+/).filter(Boolean).length === 1)
              orphans.push({ screen: s.k, where, line, of: lines.length, at: idx + 1 });
          });
          const longest = Math.max(...lines.map(l => l.length));
          if (longest > 78) overlong.push({ screen: s.k, where, chars: longest });
        }
      }
      await page.keyboard.press('Enter');
    }
  }
}

console.log(`\n=== TYPOGRAPHY AUDIT ===\n`);
console.log(`  ${DATES.length} birthdates x ${DOMAINS.length} domains — ${screensChecked} screens measured\n`);

if (orphans.length) {
  console.log(`  ORPHANS — a rendered line holding one word:\n`);
  for (const o of orphans)
    console.log(`    FAIL [${o.screen}] ${o.where} ${o.at ? `line ${o.at}/${o.of}: ` : ''}"${o.line}"`);
} else {
  console.log('  orphans: none — no rendered line holds a single word');
}
console.log(overlong.length
  ? `\n  measure: ${overlong.length} block(s) past 78 characters`
  : '\n  measure: every block within 78 characters');
console.log(`  js errors: ${errs.length ? errs.join('; ') : 'none'}`);

await browser.close();
process.exit(orphans.length || errs.length ? 1 : 0);
