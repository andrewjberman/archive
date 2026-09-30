/**
 * dates.cjs -- DSGN_AMGTV1 round 10, AV-o-1: ONE HOUSE DATE FORM ACROSS THE PAGE -- every date a person reads is the reference
 * pages' long form ("September 28th, 2026", with ", 10:47p ET" where a time is served); ISO stays only where no one reads it
 * (data- attributes, URLs, export fields) (round-9 analysis ruling 1; FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders every walked surface (surfaces.cjs: the lead lists and footers, the lead chart, the identity header of eight names, the
 * mention timeline and 992 HK's served day, and the Thesis / Model / Posture / Exec Management tabs of eight names) on SERVED
 * fixtures. Expected long dates come from the ESTATE'S OWN formatter (src/lib/dateUtils.ts formatPanelTimestamp, with its
 * appended clock stripped for a bare date), never typed. ISSUER VARIANTS (labelled, in memory): a header figure and a Thesis bundle
 * whose vintage is a BARE date, to reach the HeaderCards / ThesisCards bare-date stamp paths.
 * Arms:
 *   1  no ISO date a person reads: 0 matches of YYYY-MM-DD (with or without a time) in the visible text of every surface,
 *      collapsed <details> included (text behind a drawer is still read); prints each surface's count
 *   2  the ISO values stay where no one reads them (the control): every surface renders (no RENDER FAILED), and the served ISO
 *      dates are still carried in data- attributes somewhere on the page (a count > 0), so the dates were re-worded, not dropped
 *   3  the long form, read from the estate formatter: each header's identity as-of reads the long form of identity
 *      .crosswalk_vintage; each served posture as_of on the header reads its long form; the 992 HK timeline shows each served
 *      event's start date in the long form; the bare-date header card stamp and Thesis window stamp read "<long date>" with no
 *      "Dated"
 * Prints the census, one line per arm and "ONE HOUSE DATE FORM: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const safe = (f) => { try { return f(); } catch (e) { return { error: String(e.message).split('\n')[0] }; } };
const DU = safe(() => L.source('src/lib/dateUtils.ts'));
const fmt = DU && DU.formatPanelTimestamp;
const longDate = (d) => (fmt ? String(fmt(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '') : null);
const ISO = /\b\d{4}-\d{2}-\d{2}(?:T[\d:.]+(?:Z|[+-]\d{2}:\d{2})?)?\b/g;

const rendered = S.renderAll();
const bySurface = Object.fromEntries(rendered.map((r) => [r.surface, r.html]));

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
let total = 0;
for (const { surface, html } of rendered) {
  const text = L.textOf(html);
  const hits = text.match(ISO) || [];
  total += hits.length;
  const first = hits.length ? (() => { const i = text.indexOf(hits[0]); return text.slice(Math.max(0, i - 40), i + hits[0].length + 5); })() : '';
  console.log(`CENSUS ${surface}: ${hits.length} visible ISO date(s)${first ? ` -- first: "${first}"` : ''}`);
  if (hits.length) f1.push(`${surface}: ${hits.length} (first "${first}")`);
}
const a1 = f1.length === 0 && rendered.length > 0;
const a1d = a1 ? `0 visible ISO dates over ${rendered.length} surfaces` : `${total} visible ISO date(s) on ${f1.length} of ${rendered.length} surfaces; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const failed = rendered.filter((r) => /RENDER FAILED/.test(r.html)).map((r) => r.surface);
let attrIso = 0;
for (const { html } of rendered) attrIso += (html.match(/\sdata-[a-z0-9-]+="[^"]*\d{4}-\d{2}-\d{2}/g) || []).length;
const a2 = failed.length === 0 && attrIso > 0;
const a2d = a2 ? `${rendered.length} surfaces render; ${attrIso} data- attribute(s) still carry an ISO date` : `render failed on ${JSON.stringify(failed)}; data- attributes with an ISO date: ${attrIso}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
if (!fmt) f3.push('estate formatter not loaded');
for (const [n, k] of Object.entries(S.NAMES)) {
  const ov = S.overlays[k];
  const html = bySurface[`header-${n}`];
  if (!ov || !html) continue;
  const text = L.textOf(html);
  const cv = ov.identity && ov.identity.crosswalk_vintage;
  if (cv && !text.includes(longDate(String(cv).slice(0, 10)))) f3.push(`header-${n}: identity as-of "${cv}" not in the long form`);
  const pa = ov.posture && ov.posture.as_of;
  if (pa && !text.includes(longDate(String(pa).slice(0, 10)))) f3.push(`header-${n}: posture as-of "${pa}" not in the long form`);
}
const tl = S.unwrap(L.fixture('timeline.992_HK_Equity.json'));
const tlText = L.textOf(bySurface['timeline-HK'] || '');
for (const ev of tl.events || []) {
  const d = ev.first_day;
  if (d && !tlText.includes(longDate(String(d).slice(0, 10)))) f3.push(`timeline-HK: event date ${d} not in the long form`);
}
const HC = safe(() => L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'));
const TC = safe(() => L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
const DEFS = (safe(() => L.source('src/pages/SecurityAnalysis/constants.ts')) || {}).HEADER_CARD_DEFS || [];
const bareOv = JSON.parse(JSON.stringify(S.overlays.VLO_US_Equity));
for (const f of bareOv.header_figures || []) f.vintage = '2026-09-25';
const hs = HC && HC.headerCardStamp && DEFS[0] ? safe(() => HC.headerCardStamp(bareOv, DEFS[0].key)) : { error: 'no headerCardStamp' };
if (!hs || hs.error || hs.stamp !== longDate('2026-09-25')) f3.push(`bare-date header card stamp reads "${hs && (hs.stamp || hs.error)}" (want "${longDate('2026-09-25')}")`);
const bareTb = Object.assign({}, S.bundles.VLO_US_Equity, { generated_at: '2026-09-29' });
const ts = TC && TC.thesisWindowStamp ? safe(() => TC.thesisWindowStamp(bareTb)) : { error: 'no thesisWindowStamp' };
if (!ts || ts.error || ts.stamp !== longDate('2026-09-29')) f3.push(`bare-date Thesis window stamp reads "${ts && (ts.stamp || ts.error)}" (want "${longDate('2026-09-29')}")`);
const a3 = f3.length === 0;
const a3d = a3 ? 'identity and posture as-of on every header, the 992 HK event dates and both bare-date stamps read the long form' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['no ISO date a person reads, on any walked surface', a1, a1d],
  ['the ISO values stay in data- attributes (control)', a2, a2d],
  ['the long form, from the estate formatter', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`ONE HOUSE DATE FORM: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
