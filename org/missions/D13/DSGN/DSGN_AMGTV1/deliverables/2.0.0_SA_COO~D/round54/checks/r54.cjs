/**
 * r54.cjs -- DSGN_AMGTV1 round 54 issuer CHECK (2.0.0_SA_COO~D): THE FRESHNESS PAGE'S THREE REPAIRS.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round54/checks/r54.cjs"
 *
 * Why (the CTO's round-53 verdict, msg 32088, and rows DSGN_AMGTV1-Z-S25, Z-S26):
 *   - a Seeking Alpha cell whose served state is no_record still carries data-state="collected"; it should carry the served state;
 *   - the day cells wrap onto two lines once the Seeking Alpha cell carries a sentence (Z-S25);
 *   - the column header "Research pack" names the analysis the system builds (Z-S26); the issuer's ruling: "Built analysis".
 * Input: the LIVE /freshness?view=page body of round 53 (round53/served/freshness_page.json, 95 covered rows).
 *
 * Arms (each prints its evidence; exit 0 only on all four):
 *   1 THE SERVED STATE ON THE CELL: every covered row's Seeking Alpha cell carries data-state = "stale" where the served rule
 *     marks Seeking Alpha stale, and otherwise the served seeking_alpha.state (read / checked / no_record).
 *   2 THE BUILT ANALYSIS'S NAME: the rendered view says "Research pack" nowhere; the column head reads "Built analysis"; a row
 *     whose built analysis is served stale reads "Built analysis last read <day>".
 *   3 A DAY READS ON ONE LINE: the Oldest input cell and every cell that prints a bare day carry the class whitespace-nowrap.
 *   4 PLANTED: the graders refuse a no_record cell marked collected, a "Research pack" head and a day cell without nowrap.
 * Renders the REAL FreshnessView through round15/checks/_load.cjs (the API module stubbed); no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const D = path.join(__dirname, '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const BODY = JSON.parse(fs.readFileSync(path.join(D, 'round53', 'served', 'freshness_page.json'), 'utf8'));
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const attr = (attrs, name) => { const m = new RegExp(name + '="([^"]*)"').exec(attrs || ''); return m ? m[1] : null; };

L.stubSource('src/api/endpoints/amgt-lead-panel', { getCoverageFreshness: () => null });
L.stubSource('src/api/endpoints/amgt-lead-panel.ts', { getCoverageFreshness: () => null });

function cells(html) {
  const body = String(html).split('<tbody>')[1] || '';
  return body.split('<tr').slice(1).map((tr) => {
    const tds = tr.split('<td').slice(1).map((td) => ({ attrs: td.slice(0, td.indexOf('>')), text: text(td.slice(td.indexOf('>') + 1).split('</td>')[0]) }));
    return { name: tds.length ? tds[0].text : '', tds };
  });
}
const covered = BODY.rows.filter((r) => r.covered === true);
const servedName = (r) => r.name || r.security_key || 'Unnamed company';

function stateFaults(html, rows) {
  const f = [];
  const byName = new Map(cells(html).map((l) => [l.name, l]));
  for (const r of rows) {
    const l = byName.get(servedName(r));
    const td = l && l.tds.find((t) => attr(t.attrs, 'data-input') === 'seekingalpha');
    if (!td) { f.push(`${servedName(r)}: no Seeking Alpha cell`); continue; }
    const stale = r.inputs && r.inputs.seekingalpha && r.inputs.seekingalpha.state === 'stale';
    const want = stale ? 'stale' : r.seeking_alpha.state;
    if (attr(td.attrs, 'data-state') !== want) f.push(`${servedName(r)}: data-state ${attr(td.attrs, 'data-state')} (wanted ${want})`);
  }
  return f;
}
function nameFaults(html) {
  const f = [];
  if (/research pack/i.test(text(html))) f.push(`"Research pack" is printed: ${(text(html).match(/.{0,40}research pack.{0,40}/i) || [''])[0]}`);
  const heads = (String(html).match(/<th[^>]*>[\s\S]*?<\/th>/g) || []).map(text);
  if (!heads.includes('Built analysis')) f.push(`no "Built analysis" column head (heads: ${JSON.stringify(heads)})`);
  return f;
}
function nowrapFaults(html) {
  const f = [];
  for (const l of cells(html)) {
    for (const t of l.tds) {
      const isDay = /^\d{4}-\d{2}-\d{2}$/.test(t.text) || attr(t.attrs, 'data-slot') === 'keyed-date';
      if (isDay && !/\bwhitespace-nowrap\b/.test(attr(t.attrs, 'class') || '')) f.push(`${l.name}: "${t.text}" cell without whitespace-nowrap`);
    }
  }
  return f;
}

const arms = [];
let FV; let live = null; const load = [];
try { FV = L.source('src/pages/Freshness/Freshness.tsx').FreshnessView; } catch (e) { load.push('LOADER: Freshness.tsx ' + String(e.message).split('\n')[0]); }
const render = (rows) => L.render(FV, { rows, lists: BODY.lists, initialSort: 'name' });
if (FV) { try { live = render(BODY.rows); } catch (e) { load.push('RENDER FAILED ' + String(e.message).split('\n')[0]); } }
{
  const f = live ? stateFaults(live, covered) : load.slice();
  const tally = {};
  for (const r of covered) { const s = r.inputs.seekingalpha.state === 'stale' ? 'stale' : r.seeking_alpha.state; tally[s] = (tally[s] || 0) + 1; }
  arms.push(['THE SERVED STATE ON THE SEEKING ALPHA CELL', f.length === 0, f.length ? `${f.length} fault(s): ` + f.slice(0, 5).join(' | ') : `${covered.length} of ${covered.length} cells carry it (${JSON.stringify(tally)})`]);
}
{
  const f = live ? nameFaults(live) : load.slice();
  if (live) {
    const row = JSON.parse(JSON.stringify(covered[0]));
    row.name = 'Planted Old Build'; row.pack = '20260801T000000Z'; row.per_input = { ...row.per_input, pack: '20260801T000000Z' };
    row.inputs = { ...row.inputs, pack: { state: 'stale', day: '2026-08-01', age_trading_days: 48 } };
    row.stale = true; row.stale_inputs = ['pack'];
    try {
      const html = render([row]);
      if (!text(html).includes('Built analysis last read 2026-08-01')) f.push(`a stale built analysis does not read "Built analysis last read 2026-08-01": "${text(html).slice(-200)}"`);
      for (const x of nameFaults(html)) f.push('stale row: ' + x);
    } catch (e) { f.push('stale row RENDER FAILED ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['THE BUILT ANALYSIS IS NAMED "BUILT ANALYSIS"', f.length === 0, f.length ? f.join(' | ') : 'no "Research pack" on the 95-row view; the head reads "Built analysis"; a stale build reads "Built analysis last read 2026-08-01"']);
}
{
  const f = live ? nowrapFaults(live) : load.slice();
  const n = live ? cells(live).reduce((s, l) => s + l.tds.filter((t) => /^\d{4}-\d{2}-\d{2}$/.test(t.text) || attr(t.attrs, 'data-slot') === 'keyed-date').length, 0) : 0;
  arms.push(['A DAY READS ON ONE LINE', f.length === 0, f.length ? `${f.length} of ${n} day cell(s) without nowrap: ` + f.slice(0, 4).join(' | ') : `${n} of ${n} day cells carry whitespace-nowrap`]);
}
{
  const f = [];
  const r = { name: 'A', covered: true, seeking_alpha: { state: 'no_record' }, inputs: { seekingalpha: { state: 'not_collected' } } };
  const row = (st, cls) => `<table><thead><tr><th>Company</th><th>Built analysis</th></tr></thead><tbody><tr><td>A</td><td class="${cls}" data-slot="keyed-date">2026-10-08</td><td data-input="seekingalpha" data-state="${st}">x</td></tr></tbody></table>`;
  const clean = row('no_record', 'py-2 whitespace-nowrap');
  if (stateFaults(clean, [r]).length || nameFaults(clean).length || nowrapFaults(clean).length) f.push('the clean form refused');
  if (!stateFaults(row('collected', 'whitespace-nowrap'), [r]).length) f.push('a no_record cell marked collected accepted');
  if (!nameFaults(clean.replace('Built analysis', 'Research pack')).length) f.push('a "Research pack" head accepted');
  if (!nowrapFaults(row('no_record', 'py-2')).length) f.push('a day cell without nowrap accepted');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '3 of 3 faults refused; the clean form admitted']);
}

const TITLE = 'THE FRESHNESS PAGE: SERVED STATE ON THE CELL, THE BUILT ANALYSIS NAMED, DAYS ON ONE LINE';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
