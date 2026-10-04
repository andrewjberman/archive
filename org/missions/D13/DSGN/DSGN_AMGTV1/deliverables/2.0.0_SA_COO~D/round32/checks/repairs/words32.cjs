/**
 * words32.cjs -- DSGN_AMGTV1 round 32, AV-zj-1 (issuer 2.0.0_SA_COO~D): THE LEAD PANEL SPEAKS ONE DATE FORMAT AND NO SYSTEM WORDS AT
 * EVERY WINDOW (PRD FWD-27; FWD-26's faces).
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-90): node <this file>
 * Why: the round-31 close walk (ROUND31_CLOSE.md section 3, @b742fd0687) read:
 *   - the Chatter footer printing the served as_of raw ("As of 2026-10-02", LeadPanel.tsx) beside long dates (walker format:dates);
 *   - the Price face at 90D / 365D printing "Source: ranking details are not carried on this payload" and a Details line that
 *     repeats it, under the served "not produced yet" reason;
 *   - the Chatter count line saying "this period" when the face shows a rolling window;
 *   - LeadPanel.tsx's header comment saying the controls are `ground="band"` while none passes a ground (row Z-W88-S1).
 *   Served prose stays as served (C-PRESENTATION-ONLY; CTO ruling (b), msg 28836): a bubble hover's served places_moved_reason may
 *   carry a served ISO date, so this check grades the footer element, not the whole face, for dates.
 * Render: ../../../round31/checks/presets/_presets.cjs (the REAL LeadPanel, hooks, ChatterBubbles and PriceBars; each preset
 *   selected through its own onChange) over round31/fixtures/windows.{chatter,price}.{30,90,365}.json.
 * Arms:
 *   1  DATES IN WORDS: at 30, 90 and 365 days the Chatter footer ([data-chatter-footer]) names the served as_of in words (longDate
 *      from dateWords.ts, e.g. "October 2nd, 2026") and holds no YYYY-MM-DD date.
 *   2  NO SYSTEM WORDS: at every window on both faces the Lead Panel prints none of "payload", "ranking details", "this period";
 *      the Chatter count line says "in this window"; on Price at 90 and 365 days (no served list) no [data-source-caption] element
 *      is drawn.
 *   3  THE COMMENT AND THE KEEP: LeadPanel.tsx holds no `ground="band"` (no control passes one), and round31 presets.cjs and
 *      windowread.cjs, round29 leadface.cjs and round30 resolutionwords.cjs still exit 0.
 *   4  PLANTED: the footer predicate rejects an ISO as_of and a footer with no date, and accepts the long date; the words predicate
 *      rejects "payload", "this period", a missing "in this window" and a source caption on an unserved window, and accepts the
 *      good shapes.
 * Prints one line per arm and "ONE DATE FORMAT, NO SYSTEM WORDS, AT EVERY WINDOW: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const P = require(path.join(DROOT, 'round31', 'checks', 'presets', '_presets.cjs'));
const { L, SA, CHATTER, PRICE, textOf } = P;
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
let longDate = (s) => String(s);
try { longDate = L.source(SA + 'dateWords.ts').longDate; } catch (e) { /* the footer arm reports it */ }

const ISO = /\b\d{4}-\d{2}-\d{2}\b/;
/** The Chatter footer: its element, the served as_of in words, no ISO date. */
function footerFaults(html, asOf) {
  const m = /<([a-z]+)[^>]*\sdata-chatter-footer="[^"]*"[^>]*>([\s\S]*?)<\/\1>/.exec(html);
  if (!m) return ['no [data-chatter-footer] element'];
  const t = textOf(m[2]);
  const f = [];
  if (ISO.test(t)) f.push(`the footer prints "${t.match(ISO)[0]}" (want the date in words)`);
  if (!t.includes(longDate(asOf))) f.push(`the footer does not name "${longDate(asOf)}"`);
  return f;
}
const WORDS = [/\bpayload\b/i, /\branking details\b/i, /\bthis period\b/i];
/** The Lead Panel's words at one window: no system words; Chatter says "in this window"; no source caption on an unserved list. */
function wordFaults(html, subject, served) {
  const f = [];
  const t = textOf(html);
  for (const re of WORDS) if (re.test(t)) f.push(`prints "${t.match(re)[0]}"`);
  if (subject === 'CHATTER' && !/\bin this window\b/i.test(t)) f.push('the count line does not say "in this window"');
  if (subject === 'PRICE' && !served && /\sdata-source-caption=/.test(html)) f.push('a [data-source-caption] is drawn on a window with no served list');
  return f;
}

const arms = [];
const at = {};
const stops = [];
for (const s of ['CHATTER', 'PRICE']) for (const d of P.WINDOWS) {
  try { const r = P.renderAt(s, d); if (r.stop) stops.push(`${s} ${d}: ${r.stop}`); at[`${s}:${d}`] = r.at; } catch (e) { stops.push(`${s} ${d}: RENDER ${first(e)}`); }
}
// Arm 1 -- dates in words.
{
  const f = [...stops.filter((x) => x.startsWith('CHATTER'))];
  for (const d of P.WINDOWS) {
    const r = at[`CHATTER:${d}`];
    if (r) f.push(...footerFaults(r.html, CHATTER[d].as_of).map((x) => `${d}: ${x}`));
  }
  arms.push(['DATES IN WORDS: the Chatter footer names the served as_of in words at every window, no YYYY-MM-DD', f.length === 0,
    f.length ? [...new Set(f)].slice(0, 5).join(' | ') : `footer names "${longDate(CHATTER[30].as_of)}" at 30, 90 and 365 days`]);
}
// Arm 2 -- no system words.
{
  const f = [...stops];
  for (const s of ['CHATTER', 'PRICE']) for (const d of P.WINDOWS) {
    const r = at[`${s}:${d}`];
    if (r) f.push(...wordFaults(r.html, s, s === 'PRICE' ? (PRICE[d].rows || []).length > 0 : true).map((x) => `${s.toLowerCase()} ${d}: ${x}`));
  }
  arms.push(['NO SYSTEM WORDS: no "payload" / "ranking details" / "this period" at any window; "in this window"; no source caption on an unserved list', f.length === 0,
    f.length ? [...new Set(f)].slice(0, 6).join(' | ') : '6 of 6 renders clean']);
}
// Arm 3 -- the comment and the keep.
{
  const f = [];
  let lp = null;
  try { lp = fs.readFileSync(path.join(process.cwd(), 'portal', SA, 'components', 'LeadPanel.tsx'), 'utf8'); } catch (e) { f.push('READ LeadPanel.tsx: ' + first(e)); }
  if (lp !== null && /ground="band"/.test(lp)) f.push(`LeadPanel.tsx holds ${lp.match(/ground="band"/g).length} \`ground="band"\` (no control passes one)`);
  const KEEP = ['round31/checks/presets/presets.cjs', 'round31/checks/presets/windowread.cjs', 'round29/checks/leadprice/leadface.cjs',
    'round30/checks/universe/resolutionwords.cjs'];
  for (const rel of KEEP) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 900000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) f.push(`${rel} rc=${r.status} ("${last.slice(0, 80)}")`);
  }
  arms.push(['THE COMMENT AND THE KEEP: no `ground="band"` in LeadPanel.tsx; presets, windowread, leadface and resolutionwords exit 0', f.length === 0,
    f.length ? f.join(' | ') : `0 \`ground="band"\`; ${KEEP.length} of ${KEEP.length} exit 0`]);
}
// Arm 4 -- planted.
{
  const f = [];
  const foot = (t) => `<div><p data-chatter-footer="">${t}</p></div>`;
  if (footerFaults(foot('Articles collected, from the harvest. As of October 2nd, 2026.'), '2026-10-02').length) f.push('good footer rejected');
  for (const [n, h] of [['an ISO as_of', foot('Articles collected, from the harvest. As of 2026-10-02.')], ['no date', foot('Articles collected, from the harvest.')], ['no footer', '<div><p>As of October 2nd, 2026</p></div>']])
    if (footerFaults(h, '2026-10-02').length === 0) f.push(`footer: ${n} accepted`);
  const chatGood = '<p>55 of 95 covered names have collected articles in this window</p>';
  if (wordFaults(chatGood, 'CHATTER', true).length) f.push('good chatter words rejected');
  if (wordFaults('<p>the 90- and 365-day price windows are not produced yet</p>', 'PRICE', false).length) f.push('good unserved price rejected');
  if (wordFaults('<p>Change over the last 30 days</p><div data-source-caption="detail">Bloomberg</div>', 'PRICE', true).length) f.push('a served price caption rejected');
  for (const [n, h, s, sv] of [
    ['"payload"', '<p>Source: ranking details are not carried on this payload</p>', 'PRICE', false],
    ['"this period"', '<p>55 of 95 covered names have collected articles this period</p>', 'CHATTER', true],
    ['no "in this window"', '<p>55 of 95 covered names have collected articles</p>', 'CHATTER', true],
    ['a source caption on an unserved window', '<p>not produced yet</p><div data-source-caption="generation">Source: Bloomberg</div>', 'PRICE', false],
  ]) if (wordFaults(h, s, sv).length === 0) f.push(`words: ${n} accepted`);
  arms.push(['PLANTED: the footer and words predicates reject their planted faults and accept the good shapes', f.length === 0,
    f.length ? f.join(' | ') : '3 + 4 rejected, 4 good accepted']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`ONE DATE FORMAT, NO SYSTEM WORDS, AT EVERY WINDOW: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
