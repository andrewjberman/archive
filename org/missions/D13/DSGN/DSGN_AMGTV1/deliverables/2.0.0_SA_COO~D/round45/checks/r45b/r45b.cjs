/**
 * r45b.cjs -- DSGN_AMGTV1 round 45 AMENDMENT check (2.0.0_SA_COO~D): NO FIGURE SITS UNDER THE WRONG COLUMN HEADER.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round45/checks/r45b/r45b.cjs"
 *
 * Why: CTO render review `ledger/CTO_RENDER_REVIEW_ROUND45_0aa353a6.md` @e3d1e62b06 Amendment 1 (msg 30533). On candidate 0aa353a6
 * BA's "Deliveries" row holds 8 figures under 6 headers, so 26 is drawn under "Total" and the real total hangs past the last
 * column. The rule: a row whose figure count differs from the header count is NOT drawn in the header grid. It renders as its own
 * unaligned line (label, then its figures in printed order). Only a row that matches the headers is drawn under them.
 * Fixture: AMGT_RESAPP deliverables/2.0.0_SA_COO~Z/round77/checks/r77_groupB_fixture.json (the deployed /thesis bytes). BA's three
 * points each serve columns [737, 747, 767, 777, 787, Total] and two rows of 5 and 8 (or 7) figures: NEITHER matches.
 *
 * The contract (components/PassageTable.tsx):
 *   - `<table data-driver-chart-passage-table>` keeps its header row, one `<th scope="col">` per served column label;
 *   - a row with exactly as many figures as there are columns is a `<tr>` in the table body, as today;
 *   - any other row is an element carrying `data-driver-chart-passage-row-unaligned`, OUTSIDE the table, holding the row's label and
 *     every figure in served order;
 *   - the served note is shown once.
 *
 * Arms (exit 0 only on all of them):
 *   1 BA: no served figure of a mismatched row is inside the table; each mismatched row is an unaligned line with its label and all
 *     its figures in order; the six column labels are still printed; the note is shown.
 *   2 A MATCHING ROW STAYS IN THE GRID (planted: BA's columns with one 6-figure row and one 8-figure row): the 6-figure row is a table
 *     row with its figures; the 8-figure row is an unaligned line.
 *   3 ALL ROWS MATCH (planted): no unaligned line is drawn.
 *   4 PLANTED: the grader refuses a mismatched row left in the grid and a dropped figure, and accepts the intended form.
 */
const fs = require('fs');
const path = require('path');
const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));

const REPO = path.join(__dirname, '..', '..', '..', '..', '..', '..', '..', '..', '..', '..');
const FXP = path.join(REPO, 'org', 'missions', 'D5', 'AMGT', 'AMGT_RESAPP', 'deliverables', '2.0.0_SA_COO~Z', 'round77', 'checks', 'r77_groupB_fixture.json');
const FX = JSON.parse(fs.readFileSync(FXP, 'utf8'));
const BA = FX.names.BA_US_Equity.thesis_driver_chart.points[0].passage_table;
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(html.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

function grade(html, table) {
  const f = [];
  const tm = /<table[^>]*data-driver-chart-passage-table[^>]*>([\s\S]*?)<\/table>/.exec(html);
  if (!tm) return ['no table[data-driver-chart-passage-table]'];
  const inside = tm[1];
  const outside = html.replace(tm[0], ' ');
  const ths = (inside.match(/<th[^>]*scope="col"[^>]*>[\s\S]*?<\/th>/g) || []).map((x) => text(x));
  if (ths.join('|') !== table.columns.map(String).join('|')) f.push(`column labels ${JSON.stringify(ths)}`);
  const trs = (/<tbody[^>]*>([\s\S]*?)<\/tbody>/.exec(inside) || [null, ''])[1].split(/(?=<tr[\s>])/).filter((x) => /<tr[\s>]/.test(x));
  const lines = outside.split(/(?=<[a-z0-9]+[^>]*data-driver-chart-passage-row-unaligned[\s>=])/).slice(1).map((x) => text(x.replace(/<[a-z0-9]+[^>]*data-driver-chart-passage-table-note[\s\S]*$/, '')));
  const match = table.rows.filter((r) => r.values.length === table.columns.length);
  const odd = table.rows.filter((r) => r.values.length !== table.columns.length);
  if (trs.length !== match.length) f.push(`${trs.length} row(s) in the grid (${match.length} served row(s) match the headers)`);
  if (lines.length !== odd.length) f.push(`${lines.length} unaligned line(s) (${odd.length} served row(s) do not match)`);
  match.forEach((r, i) => {
    const cells = ((trs[i] || '').match(/<td[^>]*>[\s\S]*?<\/td>/g) || []).map((x) => text(x));
    if (!text(trs[i] || '').includes(r.label)) f.push(`grid row ${i + 1}: label "${r.label}" missing`);
    if (cells.join('|') !== r.values.map(String).join('|')) f.push(`grid row ${i + 1}: figures ${JSON.stringify(cells)}`);
  });
  odd.forEach((r, i) => {
    const line = lines[i] || '';
    if (!line.includes(r.label)) f.push(`unaligned line ${i + 1}: label "${r.label}" missing`);
    let at = line.indexOf(r.label) + r.label.length; let lost = null;
    for (const v of r.values.map(String)) { const k = line.indexOf(v, at); if (k < 0) { lost = v; break; } at = k + v.length; }
    if (lost !== null) f.push(`unaligned line ${i + 1}: figure "${lost}" missing or out of order`);
    if (text(trs.join(' ')).includes(r.label)) f.push(`"${r.label}" is still drawn in the header grid`);
  });
  if (table.note) {
    const n = html.split(table.note.slice(0, 40)).length - 1;
    if (n !== 1) f.push(`the note is shown ${n} time(s)`);
  }
  return f;
}

let PT = null;
try { PT = L.source('src/pages/SecurityAnalysis/components/PassageTable.tsx'); } catch (e) { console.log('LOADER ERROR: PassageTable.tsx :: ' + String(e.message).split('\n')[0]); process.exit(3); }
const safe = (fn) => { try { return fn(); } catch (e) { return ['threw: ' + String(e.message).split('\n')[0]]; } };
const six = { label: 'PLANTED six', values: ['1', '2', '3', '4', '5', '6'] };
const arms = [];
{
  const f = safe(() => grade(L.render(PT.PassageTable, { table: BA }), BA));
  arms.push(['BA: NO MISMATCHED ROW IS DRAWN UNDER THE HEADERS', f.length === 0, f.length ? f.join(' | ') : `${BA.rows.map((r) => `${r.label} (${r.values.length} figures)`).join(', ')}: both are unaligned lines; 6 column labels printed; note once`]);
}
{
  const t = Object.assign({}, BA, { rows: [six, BA.rows[1]] });
  const f = safe(() => grade(L.render(PT.PassageTable, { table: t }), t));
  arms.push(['A MATCHING ROW STAYS IN THE GRID (PLANTED six-figure row)', f.length === 0, f.length ? f.join(' | ') : 'the 6-figure row is a grid row; the 8-figure row is an unaligned line']);
}
{
  const t = Object.assign({}, BA, { rows: [six, Object.assign({}, six, { label: 'PLANTED second' })], note: null });
  const f = safe(() => grade(L.render(PT.PassageTable, { table: t }), t));
  arms.push(['ALL ROWS MATCH (PLANTED): NO UNALIGNED LINE', f.length === 0, f.length ? f.join(' | ') : '2 grid rows, 0 unaligned lines']);
}
{
  const f = [];
  const head = `<table data-driver-chart-passage-table><thead><tr><td></td>${BA.columns.map((c) => `<th scope="col">${c}</th>`).join('')}</tr></thead><tbody>`;
  const line = (r) => `<p data-driver-chart-passage-row-unaligned><span>${r.label}</span> ${r.values.join(' ')}</p>`;
  const note = `<p data-driver-chart-passage-table-note>${BA.note}</p>`;
  const good = `<div>${head}</tbody></table>${BA.rows.map(line).join('')}${note}</div>`;
  if (grade(good, BA).length) f.push('a good form refused: ' + grade(good, BA).join(';'));
  const inGrid = `<div>${head}${BA.rows.map((r) => `<tr><th scope="row">${r.label}</th>${r.values.map((v) => `<td>${v}</td>`).join('')}</tr>`).join('')}</tbody></table>${note}</div>`;
  if (!grade(inGrid, BA).length) f.push('mismatched rows left in the grid accepted');
  const dropped = good.replace(' 528</p>', '</p>');
  if (!grade(dropped, BA).length) f.push('a dropped figure accepted');
  arms.push(['PLANTED: the grader refuses a mismatched row in the grid and a dropped figure', f.length === 0, f.length ? f.join(' | ') : '2 of 2 faults refused; 1 of 1 good form accepted']);
}
let ok = 0;
for (const [name, pass, ev] of arms) { console.log(`ARM ${pass ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); if (pass) ok += 1; }
console.log(`NO FIGURE SITS UNDER THE WRONG COLUMN HEADER: ${ok} of ${arms.length} arms`);
process.exit(ok === arms.length ? 0 : 1);
