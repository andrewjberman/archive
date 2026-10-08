/**
 * r53b.cjs -- DSGN_AMGTV1 round 53 issuer CHECK (2.0.0_SA_COO~D): THE SEGMENT TABLE AND THE FIVE RESEARCH-NOTE SECTIONS ARE DRAWN.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round53/checks/r53b.cjs"
 *
 * Why: PRD v0.18 SAUX-43 (FWD-4): "Where the function serves a segment table, the page draws it as a table with its period and
 * its citation; where it serves a reason, the page draws that reason." SAUX-42 (FWD-4): "Each of the five has one named place
 * on the Security page, drawn with its citation opener like the pillars; a field absent for a name draws its served reason."
 * Served on /thesis since the AMGT_RESAPP round-79 cc-7 redeploy: `segment_table` (cc-2) and `dossier_sections` (cc-4).
 *
 * Input: LIVE /thesis bodies read by the issuer from the deployed function (round53/served/thesis_<name>.json):
 *   AMD US (table served, 6 rows, first column fiscal year 2025, 5 untied columns; all five sections absent),
 *   ASML NA (table served, 12 rows; all five sections served), NU US (no table; 3 of 5 sections served),
 *   8766 JP (table served, first column untied), HD US (no table; all five sections absent).
 *
 * Arms (each prints its evidence; exit 0 only on all four):
 *   1 THE SEGMENT TABLE: components/SegmentTable.tsx, given each body's served `segment_table`: a served table draws ONE
 *     [data-segment-table="served"] holding a <table data-segment-table-revenue>: a "Segment" head cell then one head cell per
 *     served period carrying its served label verbatim, in served order; one body row per served row, in served order, its
 *     segment first and one cell per value (a number in en-US grouping, a null value an empty cell); the served currency note
 *     and period note once each; each distinct served column note once; a source line naming the served source label and the
 *     pull date in words; no raw storage path. A served operating-income set draws a second table
 *     [data-segment-table-operating]. A body whose status is not served draws [data-segment-table="none"] with the served
 *     reason once and no table. No `segment_table` draws nothing.
 *   2 THE FIVE SECTIONS: components/DossierSections.tsx, given each body's served `dossier_sections`: ONE
 *     [data-dossier-sections] holding five [data-dossier-section="<field>"] in the served order, each carrying
 *     data-dossier-section-state="<status>" and its served heading; a served section prints its text verbatim once and holds
 *     one closed <details data-dossier-section-open> with its served passage; an absent section prints its served reason once
 *     and holds no opener. No `dossier_sections` draws nothing.
 *   3 MOUNTED ON THE THESIS TAB, WHATEVER THE DRAFTING STATE: tabs/ThesisTab.tsx rendered with each live body as the thesis
 *     read draws exactly one [data-segment-table] and exactly one [data-dossier-sections]; and with the drafting state forced
 *     to ABSENT it still draws both.
 *   4 PLANTED: the graders refuse a missing period label, a reordered row, a reason drawn twice, a served section without its
 *     opener and an absent section printing no reason.
 * Renders the REAL components through round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const D = path.join(__dirname, '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const SA = 'src/pages/SecurityAnalysis/';
const NAMES = ['AMD_US_Equity', 'ASML_NA_Equity', 'NU_US_Equity', '8766_JP_Equity', 'HD_US_Equity'];
const BODIES = Object.fromEntries(NAMES.map((n) => [n, JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'served', `thesis_${n}.json`), 'utf8'))]));
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim();
const times = (hay, needle) => (needle ? String(hay).split(needle).length - 1 : 0);
const count = (html, re) => (String(html).match(re) || []).length;
const NUM = new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 });
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

/** Rows of one table: [[cellText, ...], ...] for tbody rows; head = [cellText, ...]. */
function table(html) {
  const head = ((String(html).split('<thead')[1] || '').split('</thead>')[0].match(/<th[^>]*>[\s\S]*?<\/th>/g) || []).map(text);
  const body = (String(html).split('<tbody')[1] || '').split('</tbody>')[0];
  const rows = body.split('<tr').slice(1).map((tr) => (tr.match(/<td[^>]*>[\s\S]*?<\/td>/g) || []).map(text));
  return { head, rows };
}
function segFaults(html, st) {
  const f = [];
  if (st === undefined || st === null) { if (text(html) !== '') f.push('something is drawn where no segment_table is served'); return f; }
  const marks = count(html, /data-segment-table="/g);
  if (marks !== 1) f.push(`${marks} [data-segment-table] element(s) (1 wanted)`);
  if (st.status !== 'served') {
    if (!/data-segment-table="none"/.test(html)) f.push('a reason body is not marked data-segment-table="none"');
    if (/<table/.test(html)) f.push('a table is drawn where a reason is served');
    if (times(text(html), norm(st.reason)) !== 1) f.push(`the served reason is printed ${times(text(html), norm(st.reason))} time(s)`);
    return f;
  }
  if (!/data-segment-table="served"/.test(html)) f.push('a served table is not marked data-segment-table="served"');
  const rev = /<table[^>]*data-segment-table-revenue[\s\S]*?<\/table>/.exec(html);
  if (!rev) { f.push('no <table data-segment-table-revenue>'); return f; }
  const t = table(rev[0]);
  const wantHead = ['Segment', ...st.periods.map((p) => p.label)];
  if (JSON.stringify(t.head) !== JSON.stringify(wantHead)) f.push(`head ${JSON.stringify(t.head)} (wanted ${JSON.stringify(wantHead)})`);
  if (t.rows.length !== st.rows.length) f.push(`${t.rows.length} body row(s) of ${st.rows.length} served`);
  st.rows.forEach((r, i) => {
    const want = [r.segment, ...r.values.map((v) => (v === null || v === undefined ? '' : NUM.format(v)))];
    if (JSON.stringify(t.rows[i]) !== JSON.stringify(want)) f.push(`row ${i + 1} ${JSON.stringify(t.rows[i])} (wanted ${JSON.stringify(want)})`);
  });
  const opRows = (st.operating_income_rows || []).length;
  const op = /<table[^>]*data-segment-table-operating[\s\S]*?<\/table>/.exec(html);
  if (opRows && (!op || table(op[0]).rows.length !== opRows)) f.push(`the operating-income table is ${op ? table(op[0]).rows.length + ' row(s)' : 'absent'} (${opRows} served)`);
  if (!opRows && op) f.push('an operating-income table is drawn where none is served');
  const all = text(html);
  for (const k of ['currency_note', 'period_note']) if (st[k] && times(all, norm(st[k])) !== 1) f.push(`the served ${k} is printed ${times(all, norm(st[k]))} time(s)`);
  for (const n of new Set(st.periods.map((p) => p.note).filter(Boolean))) if (times(all, norm(n)) !== 1) f.push(`a served column note is printed ${times(all, norm(n))} time(s)`);
  const src = /data-segment-table-source[^>]*>([\s\S]*?)<\/(?:p|div|span)>/.exec(html);
  if (!src) f.push('no [data-segment-table-source] line');
  else {
    const s = text(src[1]);
    const day = String(st.source && st.source.pulled_at || '').slice(0, 10);
    const [y, m, d] = day.split('-').map(Number);
    if (st.source && st.source.label && !s.includes(st.source.label)) f.push(`the source line does not name "${st.source.label}": "${s}"`);
    if (day && !(s.includes(MONTHS[m - 1]) && s.includes(String(y)) && new RegExp(`\\b${d}(st|nd|rd|th)?\\b`).test(s))) f.push(`the source line does not give the pull date ${day} in words: "${s}"`);
  }
  if (/s3:\/\/|bronze\/|\.json\b/.test(all)) f.push('a raw storage path is printed');
  if (/\d{4}-\d{2}-\d{2}/.test(all)) f.push('a raw ISO date is printed');
  return f;
}
function dosFaults(html, ds) {
  const f = [];
  if (!Array.isArray(ds) || ds.length === 0) { if (text(html) !== '') f.push('something is drawn where no dossier_sections is served'); return f; }
  if (count(html, /data-dossier-sections[=\s>]/g) !== 1) f.push(`${count(html, /data-dossier-sections[=\s>]/g)} [data-dossier-sections] element(s) (1 wanted)`);
  const fields = [...String(html).matchAll(/data-dossier-section="([^"]+)"/g)].map((m) => m[1]);
  if (JSON.stringify(fields) !== JSON.stringify(ds.map((e) => e.field))) f.push(`sections ${JSON.stringify(fields)} (served ${JSON.stringify(ds.map((e) => e.field))})`);
  for (const e of ds) {
    const at = String(html).indexOf(`data-dossier-section="${e.field}"`);
    if (at < 0) continue;
    const open = String(html).lastIndexOf('<', at);
    const next = String(html).indexOf('data-dossier-section="', at + 10);
    const chunk = String(html).slice(open, next < 0 ? undefined : String(html).lastIndexOf('<', next));
    const st = /data-dossier-section-state="([^"]*)"/.exec(chunk.slice(0, chunk.indexOf('>') + 1));
    if (!st || st[1] !== e.status) f.push(`${e.field}: data-dossier-section-state ${st ? st[1] : 'missing'} (served ${e.status})`);
    const t = text(chunk);
    if (!t.includes(norm(e.heading))) f.push(`${e.field}: the served heading "${e.heading}" is not printed`);
    const openers = count(chunk, /<details[^>]*data-dossier-section-open/g);
    if (e.status === 'served') {
      const bodyText = text(chunk.replace(/<details[\s\S]*?<\/details>/g, ''));
      if (times(bodyText, norm(e.text)) !== 1) f.push(`${e.field}: the served text is printed ${times(bodyText, norm(e.text))} time(s) outside the opener`);
      if (openers !== 1) f.push(`${e.field}: ${openers} opener(s) (1 wanted)`);
      else {
        const det = /<details[^>]*data-dossier-section-open[^>]*>[\s\S]*?<\/details>/.exec(chunk)[0];
        if (/<details[^>]*\sopen[=\s>]/.test(det.slice(0, det.indexOf('>') + 1).replace('data-dossier-section-open', ''))) f.push(`${e.field}: the opener is drawn open`);
        if (e.citation && e.citation.passage && !text(det).includes(norm(e.citation.passage))) f.push(`${e.field}: the opener does not carry the served passage`);
      }
    } else {
      if (times(t, norm(e.reason)) !== 1) f.push(`${e.field}: the served reason is printed ${times(t, norm(e.reason))} time(s)`);
      if (openers) f.push(`${e.field}: an absent section carries an opener`);
    }
  }
  if (/s3:\/\//.test(text(html))) f.push('a raw storage path is printed');
  return f;
}

const arms = [];
function comp(rel, name) {
  try { const m = L.source(SA + rel); return typeof m[name] === 'function' ? [m[name], null] : [null, `${rel} does not export ${name}`]; } catch (e) { return [null, `LOADER: ${rel} ` + String(e.message).split('\n')[0]]; }
}
{
  const [ST, err] = comp('components/SegmentTable.tsx', 'SegmentTable');
  const f = err ? [err] : [];
  const seen = [];
  if (ST) {
    for (const n of NAMES) {
      const st = BODIES[n].segment_table;
      try { for (const x of segFaults(L.render(ST, { table: st }), st)) f.push(`${n}: ${x}`); } catch (e) { f.push(`${n}: RENDER FAILED ${String(e.message).split('\n')[0]}`); }
      seen.push(`${n.split('_')[0]} ${st.status}${st.status === 'served' ? ' ' + st.rows.length + 'x' + st.periods.length : ''}`);
    }
    try { for (const x of segFaults(L.render(ST, {}), undefined)) f.push(`no table: ${x}`); } catch (e) { f.push('no table: RENDER FAILED ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['THE SEGMENT TABLE, ITS PERIODS AND ITS CITATION', f.length === 0, f.length ? `${f.length} fault(s): ` + f.slice(0, 6).join(' | ') : `5 of 5 live bodies drawn as served (${seen.join('; ')}); no table draws nothing`]);
}
{
  const [DS, err] = comp('components/DossierSections.tsx', 'DossierSections');
  const f = err ? [err] : [];
  const seen = [];
  if (DS) {
    for (const n of NAMES) {
      const ds = BODIES[n].dossier_sections;
      try { for (const x of dosFaults(L.render(DS, { sections: ds }), ds)) f.push(`${n}: ${x}`); } catch (e) { f.push(`${n}: RENDER FAILED ${String(e.message).split('\n')[0]}`); }
      seen.push(`${n.split('_')[0]} ${ds.filter((e) => e.status === 'served').length}/5`);
    }
    try { for (const x of dosFaults(L.render(DS, {}), undefined)) f.push(`none: ${x}`); } catch (e) { f.push('none: RENDER FAILED ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['THE FIVE RESEARCH-NOTE SECTIONS, EACH WITH ITS OPENER OR ITS REASON', f.length === 0, f.length ? `${f.length} fault(s): ` + f.slice(0, 6).join(' | ') : `5 of 5 live bodies drawn as served (served sections: ${seen.join(', ')}); none served draws nothing`]);
}
{
  const f = [];
  let TT;
  try { TT = L.source(SA + 'tabs/ThesisTab.tsx').ThesisTab; } catch (e) { f.push('LOADER: tabs/ThesisTab.tsx ' + String(e.message).split('\n')[0]); }
  if (TT) {
    for (const n of NAMES) {
      for (const [label, body] of [['as served', BODIES[n]], ['drafting ABSENT', { ...BODIES[n], drafting_status: 'ABSENT', drafted_sections: [] }]]) {
        L.hookState.data = body;
        let html;
        try { html = L.render(TT, { securityKey: n }); } catch (e) { f.push(`${n} ${label}: RENDER FAILED ${String(e.message).split('\n')[0]}`); continue; }
        const a = count(html, /data-segment-table="/g);
        const b = count(html, /data-dossier-sections[=\s>]/g);
        if (a !== 1 || b !== 1) f.push(`${n} ${label}: [data-segment-table] x${a}, [data-dossier-sections] x${b} (1 and 1 wanted)`);
      }
    }
    L.hookState.data = undefined;
  }
  arms.push(['MOUNTED ON THE THESIS TAB, WHATEVER THE DRAFTING STATE', f.length === 0, f.length ? `${f.length} fault(s): ` + f.slice(0, 6).join(' | ') : '5 of 5 live bodies, as served and with drafting ABSENT: one segment place and one sections place each']);
}
{
  const f = [];
  const st = BODIES.AMD_US_Equity.segment_table;
  const th = ['Segment', ...st.periods.map((p) => p.label)].map((h) => `<th>${h}</th>`).join('');
  const tr = (rows) => rows.map((r) => `<tr><td>${r.segment}</td>${r.values.map((v) => `<td>${v === null ? '' : NUM.format(v)}</td>`).join('')}</tr>`).join('');
  const notes = [st.currency_note, st.period_note, ...new Set(st.periods.map((p) => p.note).filter(Boolean))].map((n) => `<p>${n}</p>`).join('');
  const good = `<section data-segment-table="served"><table data-segment-table-revenue><thead><tr>${th}</tr></thead><tbody>${tr(st.rows)}</tbody></table>` +
    `<table data-segment-table-operating><thead><tr>${th}</tr></thead><tbody>${tr(st.operating_income_rows)}</tbody></table>${notes}` +
    `<p data-segment-table-source>Source: ${st.source.label}, pulled October 7th, 2026</p></section>`;
  if (segFaults(good, st).length) f.push('the clean table refused: ' + segFaults(good, st)[0]);
  if (!segFaults(good.replace(`<th>${st.periods[0].label}</th>`, '<th></th>'), st).length) f.push('a missing period label accepted');
  const swapped = [st.rows[1], st.rows[0], ...st.rows.slice(2)];
  if (!segFaults(good.replace(tr(st.rows), tr(swapped)), st).length) f.push('a reordered row accepted');
  const none = BODIES.HD_US_Equity.segment_table;
  if (!segFaults(`<section data-segment-table="none"><p>${none.reason}</p><p>${none.reason}</p></section>`, none).length) f.push('a reason drawn twice accepted');
  const ds = BODIES.NU_US_Equity.dossier_sections;
  const sec = (e, withOpen, withReason) => `<div data-dossier-section="${e.field}" data-dossier-section-state="${e.status}"><p>${e.heading}</p>` +
    (e.status === 'served' ? `<p>${e.text}</p>${withOpen ? `<details data-dossier-section-open><summary>Where this comes from</summary><blockquote>${e.citation.passage}</blockquote></details>` : ''}` : (withReason ? `<p>${e.reason}</p>` : '')) + '</div>';
  const cleanDs = `<section data-dossier-sections>${ds.map((e) => sec(e, true, true)).join('')}</section>`;
  if (dosFaults(cleanDs, ds).length) f.push('the clean sections refused: ' + dosFaults(cleanDs, ds)[0]);
  if (!dosFaults(`<section data-dossier-sections>${ds.map((e) => sec(e, false, true)).join('')}</section>`, ds).length) f.push('a served section without its opener accepted');
  if (!dosFaults(`<section data-dossier-sections>${ds.map((e) => sec(e, true, false)).join('')}</section>`, ds).length) f.push('an absent section with no reason accepted');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '5 of 5 faults refused; 2 clean forms admitted']);
}

const TITLE = 'THE SEGMENT TABLE AND THE FIVE RESEARCH-NOTE SECTIONS ARE DRAWN';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
