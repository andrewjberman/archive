/**
 * sourceline.cjs -- DSGN_AMGTV1 round 8, AV-q-2: THE LEAD-LIST SOURCE LINE READS IN THE ONE FOOTER FORM, DATE ONLY (round-7
 * analysis ruling 4; FWD-11).
 *
 * Usage (repo root): node <this file>
 * The lead panel's source line (components/LeadPanel.tsx sourceFooterContent, rendered as data-source-caption="generation") reads
 * "Source: ranked 2026-09-28 from Bloomberg prices (32 names) (requested 2026-09-29)" -- an ISO date inside the source, where
 * every other footer on the page reads the estate's one form "<date in words>[, <time> ET] | Source: ...". A ranking carries a
 * DATE and no time, so the line is DATE ONLY: "Dated <long date> | Source: ..." -- the round-7 pattern (HeaderCards.tsx
 * footerTime: formatPanelTimestamp(null, date) with its appended clock stripped). EXPECTED values come from the ESTATE'S OWN
 * formatter (src/lib/dateUtils.ts, loaded here), never typed. Fixtures: the four SERVED lead-panel lists (round8/fixtures/
 * rankings.*.json) and one labelled ISSUER VARIANT (Trending x Price with as_of_date removed -- a line never invents a date).
 * Arms:
 *   1  the date leads, in words, with no clock: for every served list, sourceFooterContent starts "Dated <long as_of_date> |
 *      Source: "; the line carries no ISO date and no "h:mm[ap] ET"; the variant with no as_of_date starts "Source: " and
 *      carries no "Dated"
 *   2  the source keeps the served words and the requested day reads in words: the text after "Source: " still carries the
 *      served count ("(N names)") and vendor/noun words where served; when requested_as_of differs from as_of_date the line
 *      carries the requested day as a long date (never ISO)
 *   3  ONE FORM ACROSS THE PAGE'S FOOTERS (the census): the lead line's stamp, every header card window stamp (headerCardStamp,
 *      served VLO / SAP GY / 992 HK overlays) and the Thesis window stamp (thesisWindowStamp, served VLO / 992 HK) each read
 *      "[Dated ]<long date>[, <time> ET]" with a "Source: ..." beside it; prints each footer
 * Prints the census, one line per arm and "LEAD SOURCE LINE IN THE FOOTER FORM: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const safe = (f) => { try { return f(); } catch (e) { return { error: String(e.message).split('\n')[0] }; } };
const DU = safe(() => L.source('src/lib/dateUtils.ts'));
const fmt = DU && DU.formatPanelTimestamp;
const longDate = (d) => (fmt ? String(fmt(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '') : null);
const LP = safe(() => L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx'));
const sfc = LP && LP.sourceFooterContent;
const ISO = /\b\d{4}-\d{2}-\d{2}\b/;
const CLOCK = /\d{1,2}:\d{2}[ap]\s*ET/i;
const LISTS = ['TRENDING_CHATTER', 'TRENDING_PRICE', 'BREAKOUT_CHATTER', 'BREAKOUT_PRICE'];
const lists = Object.fromEntries(LISTS.map((k) => [k, L.fixture(`rankings.${k}.json`)]));
const line = (fields) => (sfc ? safe(() => sfc(fields)) : { error: 'sourceFooterContent not exported' });

// ---- arm 1 ------------------------------------------------------------------------------------------------------------
const f1 = [];
for (const k of LISTS) {
  const p = lists[k];
  const s = line(p);
  if (typeof s !== 'string') { f1.push(`${k}: ${s.error}`); continue; }
  const want = `Dated ${longDate(p.as_of_date)} | Source: `;
  if (!s.startsWith(want)) f1.push(`${k}: "${s}" does not start "${want}"`);
  if (ISO.test(s)) f1.push(`${k}: an ISO date in "${s}"`);
  if (CLOCK.test(s)) f1.push(`${k}: an invented clock in "${s}"`);
}
const nod = clone(lists.TRENDING_PRICE); delete nod.as_of_date;
const sv = line(nod);
if (typeof sv !== 'string' || !sv.startsWith('Source: ') || /Dated/.test(sv) || CLOCK.test(sv)) f1.push(`variant (no as_of_date): "${typeof sv === 'string' ? sv : sv.error}"`);
const a1 = f1.length === 0 && !!fmt;
const a1d = a1 ? `4 of 4 served lists lead with "Dated <long date> | Source: " (no ISO, no clock); the dateless variant invents none` : `${f1.length} failing; first: ${f1[0] || 'the estate formatter did not load'}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------
const f2 = [];
for (const k of LISTS) {
  const p = lists[k];
  const s = line(p);
  if (typeof s !== 'string') { f2.push(`${k}: ${s.error}`); continue; }
  const src = s.slice(s.indexOf('Source: ') + 8);
  if (p.generation_row_count !== null && p.generation_row_count !== undefined && !src.includes(`(${p.generation_row_count} names)`)) f2.push(`${k}: the served count is gone from "${src}"`);
  if (/^bloomberg/i.test(p.coverage_vintage || '') && !/Bloomberg/.test(src)) f2.push(`${k}: the served vendor is gone from "${src}"`);
  if (p.requested_as_of && p.requested_as_of !== p.as_of_date && !s.includes(longDate(p.requested_as_of))) f2.push(`${k}: the requested day ${p.requested_as_of} is not in words in "${s}"`);
}
const a2 = f2.length === 0;
const a2d = a2 ? 'the served count and vendor are kept; a requested day that differs reads as a long date' : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3: one form across the page's footers (the census) ---------------------------------------------------------------
const STAMP = /^(Dated )?[A-Z][a-z]+ \d{1,2}(st|nd|rd|th), \d{4}(, \d{1,2}:\d{2}[ap]\s*ET)?$/;
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
  ['the lead source line leads with its date in words, date only', a1, a1d],
  ['the source keeps its served words; the requested day reads in words', a2, a2d],
  ['every footer on the page reads in one form (census)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`LEAD SOURCE LINE IN THE FOOTER FORM: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
