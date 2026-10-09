/**
 * r58a.cjs -- DSGN_AMGTV1 round 58 issuer CHECK (2.0.0_SA_COO~D1), prepared ahead of the round-57 analysis:
 * THE FILING PANEL DOES NOT SAY A BREAKDOWN IS ABSENT BESIDE A DRAWN SEGMENT TABLE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round58/checks/r58a.cjs"
 *
 * Why (AMGT_RESAPP round-80 analysis R4, org/missions/D5/AMGT/AMGT_RESAPP/ledger/ROUND_ANALYSIS.round80.md, msg 1684): on AMD the Thesis
 * draws the served segment_table (SegmentTable, status "served"), and SegmentBreakdown beneath it, having no filing rows, prints the
 * served reason "No filing analysis is stored for this name yet, so no segment breakdown is shown. ..." -- a sentence that contradicts
 * the table just above it. Where a served segment_table is drawn, the filing panel does not say the breakdown is absent.
 *
 * Arms (each prints its evidence; exit 0 only on all four):
 *   1 BESIDE A DRAWN TABLE: SegmentBreakdown with no rows, the served reason, and tableServed=true prints neither the served reason nor
 *     "no segment breakdown"; it still renders its section (data-segment-breakdown) with the heading.
 *   2 CONTROL, NO TABLE: the same breakdown with tableServed=false (and with the prop absent) still prints the served reason verbatim,
 *     and a breakdown WITH rows prints its rows either way.
 *   3 THE TAB WIRES IT: ThesisTab.tsx passes tableServed derived from the served segment_table status ("served") to SegmentBreakdown
 *     (source read; behaviour is arms 1-2).
 *   4 PLANTED: the graders refuse a panel that prints the absence sentence beside a table, a panel that drops the served reason with no
 *     table, and a tab that does not wire the prop.
 * Renders the REAL SegmentBreakdown through D's round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

const REASON = 'No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull.';
const EMPTY = { rows: [], reason: REASON, source: null };
const WITH_ROWS = { rows: [{ segment: 'Data Center', text: 'Revenue grew.', cite: 'Item 7, p. 41' }], reason: null, source: 'the 10-K' };

function besideTableFaults(html) {
  const f = []; const t = text(html);
  if (t.includes(REASON) || /no segment breakdown/i.test(t)) f.push(`beside a drawn table the panel says: "${t.slice(0, 160)}"`);
  if (!/data-segment-breakdown/.test(String(html))) f.push('the panel section is not drawn');
  return f;
}
function controlFaults(htmlFalse, htmlAbsent, htmlRows) {
  const f = [];
  if (!text(htmlFalse).includes(REASON)) f.push('with tableServed=false the served reason is not printed');
  if (!text(htmlAbsent).includes(REASON)) f.push('with no tableServed prop the served reason is not printed');
  if (!text(htmlRows).includes('Revenue grew.')) f.push('a breakdown with rows does not print its rows beside a table');
  return f;
}
function wiringFaults(src) {
  return /<SegmentBreakdown[^>]*tableServed=\{[^}]*segment_table[^}]*['"]served['"][^}]*\}/.test(src) ? [] : ['ThesisTab.tsx does not pass tableServed from segment_table status "served"'];
}

const arms = []; const load = [];
let SB = null;
L.stubSource('src/ui/components/states', { PanelEmpty: (p) => `${p.message || ''} ${p.detail || ''}` });
try { SB = L.source('src/pages/SecurityAnalysis/components/SegmentBreakdown.tsx').SegmentBreakdown; } catch (e) { load.push('LOADER: SegmentBreakdown.tsx ' + String(e.message).split('\n')[0]); }
const r = (props) => L.render(SB, props);
{
  let f;
  if (!SB) f = load.slice(); else { try { f = besideTableFaults(r({ breakdown: EMPTY, tableServed: true })); } catch (e) { f = ['RENDER FAILED ' + String(e.message).split('\n')[0]]; } }
  arms.push(['BESIDE A DRAWN TABLE', f.length === 0, f.length ? f.join(' | ') : 'no absence sentence beside a drawn table; the section and heading stand']);
}
{
  let f;
  if (!SB) f = load.slice(); else { try { f = controlFaults(r({ breakdown: EMPTY, tableServed: false }), r({ breakdown: EMPTY }), r({ breakdown: WITH_ROWS, tableServed: true })); } catch (e) { f = ['RENDER FAILED ' + String(e.message).split('\n')[0]]; } }
  arms.push(['CONTROL, NO TABLE', f.length === 0, f.length ? f.join(' | ') : 'with no drawn table the served reason prints verbatim; served rows print beside a table']);
}
{
  let src = null; try { src = fs.readFileSync(path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis', 'tabs', 'ThesisTab.tsx'), 'utf8'); } catch (e) { /* below */ }
  const f = src === null ? ['cannot read ThesisTab.tsx'] : wiringFaults(src);
  arms.push(['THE TAB WIRES IT', f.length === 0, f.length ? f.join(' | ') : 'ThesisTab passes tableServed from segment_table status "served"']);
}
{
  const f = [];
  const sec = (body) => `<section data-segment-breakdown=""><h4>Business segments</h4>${body}</section>`;
  if (besideTableFaults(sec('')).length) f.push('the clean panel refused');
  if (!besideTableFaults(sec(REASON)).length) f.push('an absence sentence beside a table accepted');
  if (!controlFaults(sec(''), sec(REASON), sec('Revenue grew.')).length) f.push('a dropped served reason accepted');
  if (!wiringFaults('<SegmentBreakdown breakdown={data.segment_breakdown} />').length) f.push('an unwired tab accepted');
  if (wiringFaults("<SegmentBreakdown breakdown={data.segment_breakdown} tableServed={data.segment_table?.status === 'served'} />").length) f.push('the clean tab refused');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '3 of 3 faults refused; the clean forms admitted']);
}

const TITLE = 'THE FILING PANEL DOES NOT SAY A BREAKDOWN IS ABSENT BESIDE A DRAWN TABLE';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
