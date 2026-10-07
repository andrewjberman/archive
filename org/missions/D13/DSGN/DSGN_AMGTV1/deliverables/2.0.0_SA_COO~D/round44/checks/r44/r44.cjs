/**
 * r44.cjs -- DSGN_AMGTV1 round 44 issuer CHECK (2.0.0_SA_COO~D): A DRIVER-CHART POINT OPENS ITS SERVED PASSAGE; THE SEGMENT BREAKDOWN
 * IS ON THE PAGE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round44/checks/r44/r44.cjs"
 *
 * Why: AMGT_RESAPP ledger/ROUND_ANALYSIS.round73.md @cf0d03deb2 item 1 (msg 29921), rows Z-W251-S1 / Z-W251-S2:
 *   (a) FWD-18: a driver-chart click opens the served `passage_text` with its filing cite. The deployed producer (satkY3HX) serves
 *       on each `thesis_driver_chart.points[]` entry `passage_id`, `passage_text` and `passage_cite {accession, location}`;
 *       components/ThesisDriverChart.tsx resolves the id only against `drafted_sections` and so prints "The filing passage for this
 *       point is not shown on this page." for every BA point.
 *   (b) FWD-1: the served `segment_breakdown {rows[{segment, text, cite}], reason, source}` is drawn on the company's page with its
 *       cites; a plain served reason shows where there are no rows. 12 covered names serve rows (BA 11); MSFT serves rows [] + reason.
 * Fixtures: ../../fixtures/thesis.{BA,MSFT}_US_Equity.deployed-satkY3HX.json (read-only invokes of the deployed /thesis route).
 *
 * The contract a cell builds to (from the task order): a NEW `src/pages/SecurityAnalysis/components/SegmentBreakdown.tsx` exporting
 * `SegmentBreakdown: FC<{ breakdown?: SegmentBreakdownBlock | null }>`; its root carries `data-segment-breakdown` and
 * `data-segment-state="SERVED"|"REASON"`; each row is an element with `data-segment-row`; each row's cite sits in a CLOSED
 * `<details data-segment-cite>` (FWD-11 v0.8: the served cite names a passage id). ThesisTab mounts it with the bundle's
 * `segment_breakdown`.
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 A CLICKED DRIVER POINT SHOWS ITS SERVED PASSAGE (FWD-18): ThesisDriverChart on BA's served bundle, with the point opened, shows
 *     that point's served passage_text and its passage_cite location, and not "is not shown on this page".
 *   2 THE SEGMENTS ARE DRAWN WITH THEIR CITES (FWD-1): SegmentBreakdown on BA renders state SERVED, 11 rows, each with its segment and
 *     text at rest and its cite verbatim inside a closed details block; the source is named in words (10-K, filed date).
 *   3 NO ROWS READS AS THE SERVED REASON: on MSFT it renders state REASON with the served reason and 0 rows; with no block it renders
 *     nothing.
 *   4 MOUNT + KEEP: ThesisTab mounts SegmentBreakdown with data.segment_breakdown; a point with no passage_text but a passage_id the
 *     sections carry still opens the sections' passage; a point with no passage_id still reads "no passage carried".
 *   5 PLANTED: the graders refuse the old sentence, a missing cite, a cite on the face and an empty reason, and accept the intended forms.
 * Renders through round15/checks/_load.cjs (React.useState stubbed to open one point); no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));

const React = L.React;
const FX = path.join(__dirname, '..', '..', 'fixtures');
const pay = (f) => JSON.parse(fs.readFileSync(path.join(FX, f), 'utf8')).payload;
const BA = pay('thesis.BA_US_Equity.deployed-satkY3HX.json');
const MSFT = pay('thesis.MSFT_US_Equity.deployed-satkY3HX.json');
const portal = path.join(process.cwd(), 'portal');
const OV = Object.fromEntries((process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]));
const src = (rel) => { const f = OV[rel] || path.join(portal, rel); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : ''; };
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(html.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();

function renderOpen(Component, props, openId) {
  const real = React.useState;
  React.useState = (init) => (init === null ? [openId, () => {}] : real(init));
  try { return L.render(Component, props); } finally { React.useState = real; }
}

const NOT_SHOWN = 'is not shown on this page';
function gradePassage(t, point) {
  const f = [];
  if (t.includes(NOT_SHOWN)) f.push('prints "' + NOT_SHOWN + '"');
  if (!t.includes(norm(point.passage_text).slice(0, 60))) f.push('the served passage_text is not shown');
  if (point.passage_cite && point.passage_cite.location && !t.includes(norm(point.passage_cite.location))) f.push('the passage_cite location is not shown');
  return f;
}
function gradeSegments(html, block) {
  const f = [];
  if (!/data-segment-breakdown/.test(html)) return ['no data-segment-breakdown root'];
  if (!/data-segment-state="SERVED"/.test(html)) f.push('state is not SERVED');
  const rows = html.split(/(?=<[a-z]+[^>]*data-segment-row)/).slice(1);
  if (rows.length !== block.rows.length) f.push(`${rows.length} rows (${block.rows.length} served)`);
  // ROUND 45 RE-ANCHOR (AV-zw-2, CTO round-76 ruling 6): rows sit under ONE heading per segment, so a served row is matched to its
  // drawn row by its text (not by position) and its segment name is read from a data-segment-heading.
  const heads = (html.match(/<[a-z0-9]+[^>]*data-segment-heading[^>]*>[\s\S]*?<\/[a-z0-9]+>/g) || []).map((h) => text(h));
  block.rows.forEach((r, i) => {
    const key = norm(r.text).slice(0, 50);
    const same = rows.filter((x) => text(x.replace(/<details[\s\S]*?<\/details>/g, '')).includes(key));
    const row = same.find((x) => text(x).includes(norm(r.cite))) || same[0] || '';   // two rows may open with the same words
    const face = text(row.replace(/<details[\s\S]*?<\/details>/g, ''));
    if (!heads.includes(norm(r.segment))) f.push(`row ${i + 1}: segment "${r.segment}" is not a heading`);
    if (!row) f.push(`row ${i + 1}: text not at rest`);
    const det = /<details([^>]*)data-segment-cite([^>]*)>([\s\S]*?)<\/details>/.exec(row);
    if (!det) f.push(`row ${i + 1}: no details[data-segment-cite]`);
    else {
      if (/open/.test(det[1] + det[2])) f.push(`row ${i + 1}: cite open by default`);
      if (!text(det[3]).includes(norm(r.cite))) f.push(`row ${i + 1}: cite not verbatim`);
    }
    if (face.includes('(passage P')) f.push(`row ${i + 1}: a passage id on the face`);
  });
  const t = text(html.replace(/<details[\s\S]*?<\/details>/g, ''));
  if (block.source && !(t.includes(block.source.form) && /January 30th, 2026/.test(t))) f.push('source not named in words (form + filed date)');
  return f;
}
function gradeReason(html, block) {
  const f = [];
  if (!/data-segment-state="REASON"/.test(html)) f.push('state is not REASON');
  if (!text(html).includes(norm(block.reason))) f.push('the served reason is not shown');
  if (/data-segment-row/.test(html)) f.push('rows drawn where none are served');
  return f;
}

const arms = [];
let TDC = null; let SB = null;
try { TDC = L.source('src/pages/SecurityAnalysis/components/ThesisDriverChart.tsx'); } catch (e) { console.log('LOADER ERROR: ThesisDriverChart.tsx :: ' + String(e.message).split('\n')[0]); process.exit(3); }
try { SB = L.source('src/pages/SecurityAnalysis/components/SegmentBreakdown.tsx'); } catch (e) { SB = null; }

const p0 = BA.thesis_driver_chart.points[0];
{
  let f;
  try { f = gradePassage(text(renderOpen(TDC.ThesisDriverChart, { chart: BA.thesis_driver_chart, driver: BA.thesis_driver, sections: BA.drafted_sections || [] }, 0)), p0); }
  catch (e) { f = ['ThesisDriverChart threw: ' + String(e.message).split('\n')[0]]; }
  arms.push(['A CLICKED DRIVER POINT SHOWS ITS SERVED PASSAGE (FWD-18)', f.length === 0, f.length ? f.join(' | ') : `${p0.period}: served passage_text + "${p0.passage_cite.location}"`]);
}
{
  let f;
  if (!SB || !SB.SegmentBreakdown) f = ['no components/SegmentBreakdown.tsx exporting SegmentBreakdown'];
  else { try { f = gradeSegments(L.render(SB.SegmentBreakdown, { breakdown: BA.segment_breakdown }), BA.segment_breakdown); } catch (e) { f = ['SegmentBreakdown threw: ' + String(e.message).split('\n')[0]]; } }
  arms.push(['THE SEGMENTS ARE DRAWN WITH THEIR CITES (FWD-1)', f.length === 0, f.length ? f.join(' | ') : `${BA.segment_breakdown.rows.length} rows at rest, cites folded verbatim, source in words`]);
}
{
  let f;
  if (!SB || !SB.SegmentBreakdown) f = ['no SegmentBreakdown'];
  else {
    try {
      f = gradeReason(L.render(SB.SegmentBreakdown, { breakdown: MSFT.segment_breakdown }), MSFT.segment_breakdown);
      if (L.render(SB.SegmentBreakdown, { breakdown: undefined }) !== '') f.push('renders something with no block');
    } catch (e) { f = ['SegmentBreakdown threw: ' + String(e.message).split('\n')[0]]; }
  }
  arms.push(['NO ROWS READS AS THE SERVED REASON; NO BLOCK RENDERS NOTHING', f.length === 0, f.length ? f.join(' | ') : 'MSFT: REASON with the served sentence; no block: empty']);
}
{
  const f = [];
  const tab = src('src/pages/SecurityAnalysis/tabs/ThesisTab.tsx');
  const tabLines = tab.split(/\r?\n/);
  const mountAt = tabLines.findIndex((l) => /<SegmentBreakdown[^>]*breakdown=\{data\.segment_breakdown\}/.test(l));
  if (mountAt < 0) f.push('ThesisTab does not mount <SegmentBreakdown breakdown={data.segment_breakdown}>');
  else {
    // AMENDMENT 2: the segments are not part of the drafted thesis -- the mount must not sit under the `served` (drafting_status
    // SERVED) branch, or a name with no drafted thesis (MSFT) never shows its served segment reason.
    let gate = '';
    for (let i = mountAt; i >= 0; i -= 1) { if (/\{!isLoading && !isError && data\b/.test(tabLines[i]) || /\{\s*data\s*&&/.test(tabLines[i])) { gate = tabLines[i]; break; } }
    if (/served\s*&&/.test(gate) || /&&\s*served\b/.test(gate)) f.push('the SegmentBreakdown mount sits under the drafted-thesis (served) branch');
  }
  const ev = (BA.drafted_sections || []).flatMap((s) => (s.sentences || []).flatMap((x) => x.evidence || []))[0];
  if (ev) {
    const pt = { period: '2099', value: 1, unit: p0.unit, passage_id: ev.id };
    const chart = Object.assign({}, BA.thesis_driver_chart, { points: [pt] });
    try {
      const t = text(renderOpen(TDC.ThesisDriverChart, { chart, driver: BA.thesis_driver, sections: BA.drafted_sections }, 0));
      if (!t.includes(norm(ev.passage).slice(0, 40))) f.push('a point resolved through sections lost its passage');
    } catch (e) { f.push('keep render threw'); }
  }
  try {
    const chart = Object.assign({}, BA.thesis_driver_chart, { points: [{ period: '2098', value: 2, unit: p0.unit }] });
    const t = text(L.render(TDC.ThesisDriverChart, { chart, driver: BA.thesis_driver, sections: [] }));
    if (!/no passage carried/.test(t)) f.push('a point with no passage_id lost "no passage carried"');
  } catch (e) { f.push('no-id render threw'); }
  arms.push(['MOUNT + KEEP: ThesisTab mounts it; sections resolution and "no passage carried" kept', f.length === 0, f.length ? f.join(' | ') : 'mounted; sections fallback and no-id line kept']);
}
{
  const f = [];
  if (!gradePassage('2023 ... The filing passage for this point is not shown on this page.', p0).length) f.push('the old sentence accepted');
  if (gradePassage(`${norm(p0.passage_text)} ${p0.passage_cite.location}`, p0).length) f.push('a served passage refused');
  const r = BA.segment_breakdown.rows[0];
  const good = `<div data-segment-breakdown data-segment-state="SERVED"><h5 data-segment-heading>${r.segment}</h5><li data-segment-row>${r.text}<details data-segment-cite><summary>Source</summary>${r.cite}</details></li></div><p>10-K filed January 30th, 2026</p>`;
  const one = { rows: [r], reason: null, source: BA.segment_breakdown.source };
  if (gradeSegments(good, one).length) f.push('a good segment row refused: ' + gradeSegments(good, one).join(';'));
  if (!gradeSegments(good.replace(/<details[\s\S]*?<\/details>/, ''), one).length) f.push('a missing cite accepted');
  if (!gradeSegments(good.replace('<details data-segment-cite><summary>Source</summary>' + r.cite + '</details>', r.cite), one).length) f.push('a cite on the face accepted');
  if (!gradeReason('<div data-segment-breakdown data-segment-state="REASON"></div>', MSFT.segment_breakdown).length) f.push('an empty reason accepted');
  arms.push(['PLANTED: the graders refuse the old sentence, a missing cite, a cite on the face and an empty reason', f.length === 0, f.length ? f.join(' | ') : '4 of 4 faults refused; 2 of 2 good forms accepted']);
}

const TITLE = 'A DRIVER-CHART POINT OPENS ITS SERVED PASSAGE; THE SEGMENT BREAKDOWN IS ON THE PAGE';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 5 ? 0 : 1);
