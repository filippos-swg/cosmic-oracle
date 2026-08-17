/* Exhaustive orphan sweep.

   typography_audit.mjs walks real ceremonies, which only proves the lines that
   happened to be drawn — an orphan surfaced only after a corpus change caused a
   different verb to be selected. This renders EVERY string the reading screens
   can print, in the class it will be printed in, at the real column width, and
   reports any that would leave a line holding a single word.

   Run tools/dump_corpus.py first to refresh corpus_dump.json. */
import { readFileSync } from 'node:fs';
import { launchChromium } from './browser.mjs';

const PAGE = new URL('../visual/preview.html', import.meta.url).href;
const corpus = JSON.parse(readFileSync(new URL('./corpus_dump.json', import.meta.url), 'utf8'));

const browser = await launchChromium();
const page = await browser.newPage({ viewport: { width: 1300, height: 731 } });
await page.goto(PAGE);
await page.waitForTimeout(1200);
// get onto a reading screen so #r-body inherits the same cascade it will have
await page.keyboard.press('Enter'); await page.waitForTimeout(300);
for (const c of '04111979') { await page.keyboard.press(c); await page.waitForTimeout(50); }
await page.waitForFunction(() => state === 'reading', null, { timeout: 20000 });
await page.waitForTimeout(500);

const findings = await page.evaluate((corpus) => {
  const body = document.getElementById('r-body');
  const note = document.getElementById('r-note');
  const range = document.createRange();

  const linesOf = (node) => {
    const out = [];
    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    let t;
    while ((t = walker.nextNode())) {
      if (!t.data.trim()) continue;
      let top = null, cur = '';
      for (let i = 0; i < t.data.length; i++) {
        range.setStart(t, i); range.setEnd(t, i + 1);
        const r = range.getClientRects();
        if (!r.length) { cur += t.data[i]; continue; }
        const y = Math.round(r[0].top);
        if (top === null) top = y;
        if (y !== top) { out.push(cur); cur = ''; top = y; }
        cur += t.data[i];
      }
      if (cur.trim()) out.push(cur);
    }
    return out.map(l => l.trim()).filter(Boolean);
  };

  const out = [];
  const cases = [
    ['body', body, 'r-body fadeable', corpus.body],
    ['observation', body, 'r-body fadeable small', corpus.body],
    ['verdict', body, 'r-body fadeable verdict', corpus.verdict],
    ['found item', body, 'r-body fadeable poem', corpus.poem],
    ['note', note, null, corpus.note],
  ];

  for (const [label, el, cls, list] of cases) {
    const prevCls = el.className, prevTxt = el.textContent;
    if (cls) el.className = cls;
    for (const line of list) {
      el.textContent = line;
      const rendered = linesOf(el);
      if (rendered.length < 2) continue;
      const authored = line.split(String.fromCharCode(10)).filter(x => x.trim()).length;
      if (authored > 1) {
        if (rendered.length > authored)
          out.push({ label, line, why: `verse wrapped: ${rendered.length} rendered vs ${authored} authored` });
        continue;
      }
      const orphan = rendered.findIndex(l => l.split(/\s+/).filter(Boolean).length === 1);
      if (orphan !== -1)
        out.push({ label, line, why: `"${rendered[orphan]}" alone on line ${orphan + 1}/${rendered.length}` });
    }
    el.className = prevCls; el.textContent = prevTxt;
  }
  return out;
}, corpus);

const total = Object.values(corpus).reduce((n, a) => n + a.length, 0);
console.log(`\n=== EXHAUSTIVE ORPHAN SWEEP ===\n`);
console.log(`  ${total} distinct strings rendered at the real column width\n`);
if (findings.length) {
  const byLabel = {};
  for (const f of findings) (byLabel[f.label] ||= []).push(f);
  for (const [label, list] of Object.entries(byLabel)) {
    console.log(`  ${label}: ${list.length}`);
    for (const f of list.slice(0, 8))
      console.log(`    FAIL ${f.why}\n         "${f.line.slice(0, 78)}"`);
    if (list.length > 8) console.log(`    ... and ${list.length - 8} more`);
  }
} else {
  console.log('  no string in the corpus can leave a line holding one word');
}
await browser.close();
process.exit(findings.length ? 1 : 0);
