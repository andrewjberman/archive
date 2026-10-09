/**
 * r56.cjs -- DSGN_AMGTV1 round 56 issuer CHECK (2.0.0_SA_COO~D1): ONE DATE FORM ON THE FRESHNESS PAGE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round56/checks/r56.cjs"
 *
 * Why (the CTO's round-55 analysis, ruling R1, ledger/ROUND_ANALYSIS.round55.md): the signed-in walk read two date forms on
 * /freshness -- ISO days in the cells ("2026-09-22") and the house long form in the page end ("October 8th, 2026"). The house
 * form is the estate's formatPanelTimestamp long date (PageEnd, portal/src/ui/components/PageEnd.tsx; Security Analysis
 * round-9 ruling 1, SecurityAnalysis/dateWords.ts longDate). The page-drawn days take it; the ISO day stays on data-day.
 * Served sentences (the Seeking Alpha sentence, the lists' out_of_date line) are the producer's words and print verbatim.
 * Input: the LIVE /freshness?view=page body of round 53 (D's round53/served/freshness_page.json, 95 covered rows).
 *
 * Arms (each prints its evidence; exit 0 only on all five):
 *   1 PAGE DAYS IN THE HOUSE FORM: every keyed-date cell and every input cell without served words that has a day prints
 *     longDate(day) exactly, carries data-day = the ISO day, and keeps whitespace-nowrap.
 *   2 THE STALE WORDS: a planted stale build (2026-08-01) reads "Built analysis last read August 1st, 2026"; with the served
 *     sentences removed, the rendered view prints no YYYY-MM-DD anywhere.
 *   3 THE PAGE END AND THE CELLS AGREE: PageEnd's as-of for the body's day, clock removed, equals longDate of that day, and
 *     the cells use that same form.
 *   4 CONTROLS: the Seeking Alpha cell keeps the served data-state and prints the served sentence verbatim; the head reads
 *     "Built analysis".
 *   5 PLANTED: the graders refuse an ISO day cell, a day cell without data-day, a page-composed ISO in the stale words, and a
 *     footer in another form; the clean form is admitted.
 * longDate is loaded from the estate (SecurityAnalysis/dateWords.ts over lib/dateUtils formatPanelTimestamp), never re-typed.
 * Renders the REAL FreshnessView through D's round15/checks/_load.cjs (the API module stubbed); no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
const BODY = JSON.parse(fs.readFileSync(path.join(DD, 'round53', 'served', 'freshness_page.json'), 'utf8'));
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const attr = (attrs, name) => { const m = new RegExp(name + '="([^"]*)"').exec(attrs || ''); return m ? m[1] : null; };
const ISO = /\d{4}-\d{2}-\d{2}/;
const CLOCK = /,\s*\d{1,2}:\d{2}[ap]\s*ET$/i;

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
const NO_DAY = new Set(['Never', 'Not collected', 'Nothing collected']);

function dayCellFaults(html, longDate) {
  const f = []; let n = 0;
  for (const l of cells(html)) {
    for (const t of l.tds) {
      const keyed = attr(t.attrs, 'data-slot') === 'keyed-date';
      const input = attr(t.attrs, 'data-input');
      if (!keyed && !(input && attr(t.attrs, 'data-sa-state') === null)) continue;
      if (NO_DAY.has(t.text)) continue;
      n += 1;
      const iso = attr(t.attrs, 'data-day');
      if (!iso || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) { f.push(`${l.name}: "${t.text}" cell without data-day`); continue; }
      if (t.text !== longDate(iso)) f.push(`${l.name}: "${t.text}" (wanted "${longDate(iso)}")`);
      if (!/\bwhitespace-nowrap\b/.test(attr(t.attrs, 'class') || '')) f.push(`${l.name}: "${t.text}" cell without whitespace-nowrap`);
    }
  }
  return { f, n };
}
function servedWords(rows, lists) {
  const w = [];
  for (const r of rows) if (r.seeking_alpha && typeof r.seeking_alpha.sentence === 'string') w.push(r.seeking_alpha.sentence);
  if (lists) for (const k of ['owner_line', 'out_of_date']) if (typeof lists[k] === 'string') w.push(lists[k]);
  return w;
}
function composedIsoFaults(html, rows, lists) {
  let t = text(html);
  for (const s of servedWords(rows, lists).sort((a, b) => b.length - a.length)) t = t.split(text(s)).join(' ');
  const m = t.match(new RegExp('.{0,40}' + ISO.source + '.{0,20}', 'g')) || [];
  return m.map((x) => `page-composed ISO: "${x.trim()}"`);
}
function footerFaults(footerHtml, day, longDate) {
  const words = (text(footerHtml).match(/Data as of (.*)\.$/) || [])[1];
  if (!words) return [`no "Data as of" in the page end: "${text(footerHtml)}"`];
  const bare = words.replace(CLOCK, '');
  return bare === longDate(day) ? [] : [`page end reads "${bare}", the cells' form is "${longDate(day)}"`];
}

const arms = [];
let FV; let PageEnd; let longDate; let live = null; const load = [];
try { longDate = L.source('src/pages/SecurityAnalysis/dateWords.ts').longDate; } catch (e) { load.push('LOADER: dateWords.ts ' + String(e.message).split('\n')[0]); }
try { FV = L.source('src/pages/Freshness/Freshness.tsx').FreshnessView; } catch (e) { load.push('LOADER: Freshness.tsx ' + String(e.message).split('\n')[0]); }
try { PageEnd = L.source('src/ui/components/PageEnd.tsx').PageEnd; } catch (e) { load.push('LOADER: PageEnd.tsx ' + String(e.message).split('\n')[0]); }
const render = (rows) => L.render(FV, { rows, lists: BODY.lists, initialSort: 'name' });
if (FV && longDate) { try { live = render(BODY.rows); } catch (e) { load.push('RENDER FAILED ' + String(e.message).split('\n')[0]); } }
const DAY = String(BODY.generated_at).slice(0, 10);

{
  const { f, n } = live ? dayCellFaults(live, longDate) : { f: load.slice(), n: 0 };
  if (live && n === 0) f.push('no day cell was read (denominator 0)');
  arms.push(['PAGE DAYS IN THE HOUSE FORM', f.length === 0, f.length ? `${f.length} fault(s) over ${n} day cell(s): ` + f.slice(0, 4).join(' | ') : `${n} of ${n} day cells print the long form, carry data-day and nowrap`]);
}
{
  const f = live ? composedIsoFaults(live, BODY.rows, BODY.lists) : load.slice();
  if (live) {
    const row = JSON.parse(JSON.stringify(covered[0]));
    row.name = 'Planted Old Build'; row.pack = '20260801T000000Z'; row.per_input = { ...row.per_input, pack: '20260801T000000Z' };
    row.inputs = { ...row.inputs, pack: { state: 'stale', day: '2026-08-01', age_trading_days: 48 } };
    row.stale = true; row.stale_inputs = ['pack'];
    try {
      const html = render([row]);
      const want = `Built analysis last read ${longDate('2026-08-01')}`;
      if (!text(html).includes(want)) f.push(`a stale built analysis does not read "${want}": "${text(html).slice(-200)}"`);
      for (const x of composedIsoFaults(html, [row], BODY.lists)) f.push('stale row: ' + x);
    } catch (e) { f.push('stale row RENDER FAILED ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['THE STALE WORDS', f.length === 0, f.length ? f.slice(0, 4).join(' | ') : `the planted stale build reads "Built analysis last read ${longDate ? longDate('2026-08-01') : '?'}"; no page-composed ISO on the 95-row view`]);
}
{
  const f = [];
  if (!PageEnd || !longDate) f.push(...load);
  else {
    try {
      const html = L.render(PageEnd, { pageName: 'Freshness', dataAsOf: DAY });
      f.push(...footerFaults(html, DAY, longDate));
      if (live && !cells(live).some((l) => l.tds.some((t) => /^[A-Z][a-z]+ \d{1,2}(st|nd|rd|th), \d{4}$/.test(t.text)))) f.push('no cell prints the long form');
    } catch (e) { f.push('PageEnd RENDER FAILED ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['THE PAGE END AND THE CELLS AGREE', f.length === 0, f.length ? f.join(' | ') : `the page end's as-of for ${DAY} reads "${longDate(DAY)}" (clock aside), the cells' form`]);
}
{
  const f = live ? [] : load.slice();
  if (live) {
    const byName = new Map(cells(live).map((l) => [l.name, l]));
    for (const r of covered) {
      const l = byName.get(servedName(r));
      const td = l && l.tds.find((t) => attr(t.attrs, 'data-input') === 'seekingalpha');
      if (!td) { f.push(`${servedName(r)}: no Seeking Alpha cell`); continue; }
      const stale = r.inputs && r.inputs.seekingalpha && r.inputs.seekingalpha.state === 'stale';
      const want = stale ? 'stale' : r.seeking_alpha.state;
      if (attr(td.attrs, 'data-state') !== want) f.push(`${servedName(r)}: data-state ${attr(td.attrs, 'data-state')} (wanted ${want})`);
      if (r.seeking_alpha.sentence && td.text !== text(r.seeking_alpha.sentence)) f.push(`${servedName(r)}: sentence not verbatim`);
    }
    const heads = (String(live).match(/<th[^>]*>[\s\S]*?<\/th>/g) || []).map(text);
    if (!heads.includes('Built analysis')) f.push(`no "Built analysis" head (${JSON.stringify(heads)})`);
  }
  arms.push(['CONTROLS', f.length === 0, f.length ? `${f.length} fault(s): ` + f.slice(0, 4).join(' | ') : `${covered.length} of ${covered.length} Seeking Alpha cells keep the served state and sentence; the head reads "Built analysis"`]);
}
{
  const f = [];
  if (!longDate) f.push(...load);
  else {
    const L8 = longDate('2026-10-08');
    const tbl = (cell) => `<table><tbody><tr><td>A</td>${cell}</tr></tbody></table>`;
    const clean = tbl(`<td class="py-2 whitespace-nowrap" data-slot="keyed-date" data-day="2026-10-08">${L8}</td>`);
    if (dayCellFaults(clean, longDate).f.length) f.push('the clean day cell refused');
    if (!dayCellFaults(tbl('<td class="whitespace-nowrap" data-slot="keyed-date" data-day="2026-10-08">2026-10-08</td>'), longDate).f.length) f.push('an ISO day cell accepted');
    if (!dayCellFaults(tbl(`<td class="whitespace-nowrap" data-slot="keyed-date">${L8}</td>`), longDate).f.length) f.push('a day cell without data-day accepted');
    if (!composedIsoFaults('<p>Built analysis last read 2026-08-01</p>', [], null).length) f.push('a page-composed ISO accepted');
    if (composedIsoFaults('<p>served 2026-09-10 words</p>', [], { out_of_date: 'served 2026-09-10 words' }).length) f.push('a served sentence refused');
    if (!footerFaults('<div>End of Freshness. Data as of 2026-10-08.</div>', '2026-10-08', longDate).length) f.push('an ISO page end accepted');
    if (footerFaults(`<div>End of Freshness. Data as of ${L8}, 5:00p ET.</div>`, '2026-10-08', longDate).length) f.push('the house page end refused');
  }
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '4 of 4 faults refused; the clean forms admitted']);
}

const TITLE = 'THE FRESHNESS PAGE READS ONE DATE FORM';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 5 ? 0 : 1);
