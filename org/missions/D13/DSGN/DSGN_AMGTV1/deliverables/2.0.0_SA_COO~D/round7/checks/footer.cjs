/**
 * footer.cjs -- DSGN_AMGTV1 round 7, AV-s-2: EVERY WINDOW FOOTER READS IN THE ESTATE'S ONE FOOTER FORM (round-6 analysis
 * ruling 2; FWD-11).
 *
 * Usage (repo root): node <this file>
 * The reference pages (Market, Positioning, Philosophy) stamp a footer through the estate's DialogStamp / PanelFooter with
 * `@/lib/dateUtils` formatPanelTimestamp: "September 28th, 2026, 5:00p ET | Source: Bloomberg". Security Analysis's two window
 * footers -- the header card windows (components/HeaderCards.tsx) and the Thesis windows (components/ThesisCards.tsx) -- print
 * "2026-09-29 | Source: Bloomberg" and "Pack read 2026-09-29 | Machine draft from ...". The cell exports the two pure stamp
 * builders the windows use -- headerCardStamp(bundle, cardKey) and thesisWindowStamp(bundle), each -> {stamp, source} -- so
 * this check reads exactly what the footer prints (the header window is lazy-loaded, which a static render cannot open).
 * EXPECTED values are computed by the ESTATE'S OWN formatter (src/lib/dateUtils.ts, loaded here), never typed.
 * Arms:
 *   1  header card windows, served overlays VLO / SAP GY / 992 HK, every card of HEADER_CARD_DEFS: a non-null stamp equals
 *      formatPanelTimestamp(v) for one of that card's served, time-carrying vintages (so: the estate's long form with its
 *      time), carries no ISO date, and the source begins "Source: "
 *   2  Thesis windows, served /thesis VLO / 992 HK: the stamp equals formatPanelTimestamp(generated_at) and the source begins
 *      "Source: "; no "Pack read" and no ISO date in the stamp
 *   3  a served value with NO time prints the long date WITHOUT an invented clock and says it is a date (ISSUER VARIANTS,
 *      labelled: the VLO overlay with every vintage cut to its date, and the VLO /thesis with generated_at cut to its date):
 *      the stamp carries the estate's long date ("September 28th, 2026"), no "h:mm[ap] ET", the word "date"/"Dated", no ISO
 * Prints one line per arm and "ONE FOOTER FORM: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const safe = (f) => { try { return f(); } catch (e) { return { error: String(e.message).split('\n')[0] }; } };
const DU = safe(() => L.source('src/lib/dateUtils.ts'));
const fmt = DU && DU.formatPanelTimestamp;
const HC = safe(() => L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'));
const TC = safe(() => L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
const DEFS = (safe(() => L.source('src/pages/SecurityAnalysis/constants.ts')) || {}).HEADER_CARD_DEFS || [];
const ISO = /\b\d{4}-\d{2}-\d{2}\b/;
const LONG = /\b[A-Z][a-z]+ \d{1,2}(st|nd|rd|th), \d{4}\b/;
const CLOCK = /\d{1,2}:\d{2}[ap]\s*ET/i;

const ov = { VLO: L.fixture('overlay.VLO_US_Equity.json'), SAP: L.fixture('overlay.SAP_GY_Equity.json'), HK: L.fixture('overlay.992_HK_Equity.json') };
const th = { VLO: L.fixture('thesisBundle.VLO_US_Equity.json'), HK: L.fixture('thesisBundle.992_HK_Equity.json') };
const vintagesOf = (bundle) => {
  const out = new Set();
  const walk = (o) => { if (o && typeof o === 'object') { if (typeof o.vintage === 'string') out.add(o.vintage); for (const v of Object.values(o)) walk(v); } };
  walk(bundle.header_figures);
  return [...out];
};

// ---- arm 1 ------------------------------------------------------------------------------------------------------------
const c1 = [];
const hcs = HC && HC.headerCardStamp;
for (const [name, bundle] of Object.entries(ov)) {
  const allowed = new Set(vintagesOf(bundle).filter((v) => !/^\d{4}-\d{2}-\d{2}$/.test(v)).map((v) => fmt && fmt(v)));
  for (const def of DEFS) {
    const r = hcs ? safe(() => hcs(bundle, def.key)) : { error: 'headerCardStamp not exported' };
    if (r.error) { c1.push({ where: `${name}/${def.key}`, ok: false, why: r.error }); continue; }
    if (r.stamp === null && r.source === undefined) continue; // a card with no carried figure has no footer
    const ok = typeof r.stamp === 'string' && allowed.has(r.stamp) && !ISO.test(r.stamp) && /^Source: /.test(r.source || '');
    c1.push({ where: `${name}/${def.key}`, ok, why: `stamp "${r.stamp}", source "${r.source}"` });
  }
}
const a1 = c1.length >= 6 && c1.every((c) => c.ok);
const bad1 = c1.filter((c) => !c.ok);
const a1d = `${c1.length - bad1.length} of ${c1.length} card footers in the estate form` + (bad1.length ? `; first failing ${bad1[0].where}: ${bad1[0].why}` : '');

// ---- arm 2 ------------------------------------------------------------------------------------------------------------
const tws = TC && TC.thesisWindowStamp;
const c2 = Object.entries(th).map(([name, bundle]) => {
  const r = tws ? safe(() => tws(bundle)) : { error: 'thesisWindowStamp not exported' };
  if (r.error) return { where: name, ok: false, why: r.error };
  const want = fmt && fmt(bundle.generated_at);
  const ok = r.stamp === want && /^Source: /.test(r.source || '') && !/Pack read/.test(r.stamp || '') && !ISO.test(r.stamp || '');
  return { where: name, ok, why: `stamp "${r.stamp}" (want "${want}"), source "${String(r.source).slice(0, 60)}"` };
});
const a2 = c2.every((c) => c.ok);
const a2d = c2.map((c) => `${c.where}: ${c.why}`).join(' | ');

// ---- arm 3: date-only values (ISSUER VARIANTS) ------------------------------------------------------------------------
const dateOnlyOv = clone(ov.VLO);
const cut = (o) => { if (o && typeof o === 'object') { if (typeof o.vintage === 'string') o.vintage = o.vintage.slice(0, 10); for (const v of Object.values(o)) cut(v); } };
cut(dateOnlyOv.header_figures);
const dateOnlyTh = clone(th.VLO);
dateOnlyTh.generated_at = String(th.VLO.generated_at).slice(0, 10);
const reads = [];
for (const def of DEFS) {
  const r = hcs ? safe(() => hcs(dateOnlyOv, def.key)) : { error: 'headerCardStamp not exported' };
  if (!r.error && r.stamp === null && r.source === undefined) continue;
  reads.push({ where: `card ${def.key}`, s: r.error ? `ERROR ${r.error}` : r.stamp });
}
{
  const r = tws ? safe(() => tws(dateOnlyTh)) : { error: 'thesisWindowStamp not exported' };
  reads.push({ where: 'thesis', s: r.error ? `ERROR ${r.error}` : r.stamp });
}
const okDate = (s) => typeof s === 'string' && LONG.test(s) && !CLOCK.test(s) && /\bdate/i.test(s) && !ISO.test(s);
const a3 = reads.length >= 3 && reads.every((r) => okDate(r.s));
const bad3 = reads.filter((r) => !okDate(r.s));
const a3d = `${reads.length - bad3.length} of ${reads.length} date-only footers read as a long date, no clock, said to be a date` + (bad3.length ? `; first failing ${bad3[0].where}: "${bad3[0].s}"` : '');

const arms = [
  ['header card window footers read in the estate form (time | Source)', a1, a1d],
  ['Thesis window footers read in the estate form (time | Source)', a2, a2d],
  ['a date with no time prints the long date, no invented clock, and says it is a date', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`ONE FOOTER FORM: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
