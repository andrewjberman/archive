/**
 * oneform.cjs -- DSGN_AMGTV1 round 9, AV-p-3: THE LEAD SOURCE LINE DROPS ITS LONE "Dated" AND THE OLDER-LIST LINE READS IN PLAIN
 * WORDS (round-8 analysis ruling 3; FWD-11).
 *
 * Usage (repo root): node <this file>
 * Walk G read the lead panel footer as "Dated September 28th, 2026 | Source: ranked from Bloomberg prices (32 names); requested for
 * September 30th, 2026" -- the only footer on the page that starts "Dated" (the header card windows and the Positioning footers
 * read "<long date>[, <time> ET] | Source: ...") -- and beneath it "this list is older than the date requested, shown as such
 * rather than silently", a line in the system's voice. Ruled: drop "Dated" so the lead line matches the other footers; rewrite the
 * second line in plain words (for example "This list is from September 28th, 2026, the newest available.").
 * Reads components/LeadPanel.tsx sourceFooterContent / sourceDisclosureText (exported, pure) on the four SERVED lists
 * (round9/fixtures/rankings.*.json) and one labelled ISSUER VARIANT (Trending x Price with as_of_date removed). Expected dates come
 * from the ESTATE'S OWN formatter (src/lib/dateUtils.ts), never typed.
 * Arms:
 *   1  the lead line leads with its date, no "Dated": for every served list the line starts "<long as_of_date> | Source: " with
 *      no "Dated", no ISO date and no invented clock; the dateless variant starts "Source: "; the served count and the requested
 *      day in words are kept where served
 *   2  the older-list line in plain words: for every served list where dated is true and requested_as_of differs, the second
 *      line starts "This list is from <long as_of_date>" and carries none of "older than the date requested", "shown as such",
 *      "silently", nor an ISO date; for every other served list there is no second line (null)
 *   3  one form across the page's footers (the census): the lead stamp, every header card window stamp (served VLO / SAP GY /
 *      992 HK overlays) and the Thesis window stamp (served VLO / 992 HK) each read "<long date>[, <time> ET]" -- none starts
 *      "Dated" -- with a "Source: ..." beside it; prints each footer
 * Prints the census, one line per arm and "ONE FOOTER FORM, PLAIN WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const safe = (f) => { try { return f(); } catch (e) { return { error: String(e.message).split('\n')[0] }; } };
const DU = safe(() => L.source('src/lib/dateUtils.ts'));
const fmt = DU && DU.formatPanelTimestamp;
const longDate = (d) => (fmt ? String(fmt(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '') : null);
const LP = safe(() => L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx'));
const sfc = LP && LP.sourceFooterContent;
const sdt = LP && LP.sourceDisclosureText;
const ISO = /\b\d{4}-\d{2}-\d{2}\b/;
const CLOCK = /\d{1,2}:\d{2}[ap]\s*ET/i;
const SYSTEM = /older than the date requested|shown as such|silently/i;
const LISTS = ['TRENDING_CHATTER', 'TRENDING_PRICE', 'BREAKOUT_CHATTER', 'BREAKOUT_PRICE'];
const lists = Object.fromEntries(LISTS.map((k) => [k, L.fixture(`rankings.${k}.json`)]));
const line = (fields) => (sfc ? safe(() => sfc(fields)) : { error: 'sourceFooterContent not exported' });
const second = (fields) => (sdt ? safe(() => sdt(fields)) : { error: 'sourceDisclosureText not exported' });

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
for (const k of LISTS) {
  const p = lists[k];
  const s = line(p);
  if (typeof s !== 'string') { f1.push(`${k}: ${s.error}`); continue; }
  const want = `${longDate(p.as_of_date)} | Source: `;
  if (!s.startsWith(want)) f1.push(`${k}: "${s}" does not start "${want}"`);
  if (/\bDated\b/.test(s)) f1.push(`${k}: "Dated" in "${s}"`);
  if (ISO.test(s)) f1.push(`${k}: an ISO date in "${s}"`);
  if (CLOCK.test(s)) f1.push(`${k}: an invented clock in "${s}"`);
  if (p.generation_row_count !== null && p.generation_row_count !== undefined && !s.includes(`(${p.generation_row_count} names)`)) f1.push(`${k}: the served count is gone from "${s}"`);
  if (p.requested_as_of && p.requested_as_of !== p.as_of_date && !s.includes(longDate(p.requested_as_of))) f1.push(`${k}: the requested day is not in words in "${s}"`);
}
const nod = clone(lists.TRENDING_PRICE); delete nod.as_of_date;
const sv = line(nod);
if (typeof sv !== 'string' || !sv.startsWith('Source: ') || /Dated/.test(sv) || CLOCK.test(sv)) f1.push(`variant (no as_of_date): "${typeof sv === 'string' ? sv : sv.error}"`);
const a1 = f1.length === 0 && !!fmt;
const a1d = a1 ? `4 of 4 served lists lead with "<long date> | Source: " (no "Dated", no ISO, no clock); count and requested day kept; the dateless variant invents none` : `${f1.length} failing; first: ${f1[0] || 'the estate formatter did not load'}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
let n2 = 0;
for (const k of LISTS) {
  const p = lists[k];
  const d = second(p);
  if (d && typeof d === 'object' && d.error) { f2.push(`${k}: ${d.error}`); continue; }
  const fires = p.dated === true && p.requested_as_of && p.requested_as_of !== p.as_of_date;
  if (!fires) { if (d !== null) f2.push(`${k}: a second line "${d}" where the list is not older than requested`); continue; }
  n2 += 1;
  console.log(`SECOND LINE ${k}: "${d}"`);
  const want = `This list is from ${longDate(p.as_of_date)}`;
  if (typeof d !== 'string' || !d.startsWith(want)) f2.push(`${k}: "${d}" does not start "${want}"`);
  else if (SYSTEM.test(d) || ISO.test(d)) f2.push(`${k}: system words or an ISO date in "${d}"`);
}
const a2 = f2.length === 0 && n2 > 0;
const a2d = a2 ? `${n2} older list(s) say "This list is from <long date>..." in plain words; the others carry no second line` : `${f2.length} failing; first: ${f2[0] || 'no served list fires the line'}`;

// ---- arm 3: one form across the page's footers (the census) -------------------------------------------------------------------
const STAMP = /^[A-Z][a-z]+ \d{1,2}(st|nd|rd|th), \d{4}(, \d{1,2}:\d{2}[ap]\s*ET)?$/;
const HC = safe(() => L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'));
const TC = safe(() => L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
const DEFS = (safe(() => L.source('src/pages/SecurityAnalysis/constants.ts')) || {}).HEADER_CARD_DEFS || [];
const footers = [];
for (const k of LISTS) {
  const s = line(lists[k]);
  if (typeof s !== 'string') { footers.push({ where: `lead ${k}`, stamp: null, source: s.error }); continue; }
  const i = s.indexOf(' | Source: ');
  footers.push({ where: `lead ${k}`, stamp: i < 0 ? s : s.slice(0, i), source: i < 0 ? '' : s.slice(i + 3) });
}
for (const [n, f] of [['VLO', 'overlay.VLO_US_Equity.json'], ['SAP', 'overlay.SAP_GY_Equity.json'], ['992', 'overlay.992_HK_Equity.json']]) {
  const b = L.fixture(f);
  for (const def of DEFS) {
    const r = HC && HC.headerCardStamp ? safe(() => HC.headerCardStamp(b, def.key)) : { error: 'no headerCardStamp' };
    if (r && !r.error && (r.stamp !== null || r.source !== undefined)) footers.push({ where: `card ${n}/${def.key}`, stamp: r.stamp, source: r.source });
  }
}
for (const [n, f] of [['VLO', 'thesisBundle.VLO_US_Equity.json'], ['992', 'thesisBundle.992_HK_Equity.json']]) {
  const r = TC && TC.thesisWindowStamp ? safe(() => TC.thesisWindowStamp(L.fixture(f))) : { error: 'no thesisWindowStamp' };
  if (r && !r.error) footers.push({ where: `thesis ${n}`, stamp: r.stamp, source: r.source });
}
for (const f of footers) console.log(`CENSUS FOOTER ${f.where}: "${f.stamp}" | "${f.source}"`);
const bad3 = footers.filter((f) => !(typeof f.stamp === 'string' && STAMP.test(f.stamp) && /^Source: /.test(f.source || '')));
const a3 = footers.length >= 8 && bad3.length === 0;
const a3d = `${footers.length - bad3.length} of ${footers.length} footers in the one form` + (bad3.length ? `; first failing ${bad3[0].where}: "${bad3[0].stamp}"` : '');

const arms = [
  ['the lead line leads with its date, no "Dated"', a1, a1d],
  ['the older-list line reads in plain words', a2, a2d],
  ['every footer on the page reads in one form (census)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`ONE FOOTER FORM, PLAIN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
