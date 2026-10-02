/**
 * whatchanged.cjs -- DSGN_AMGTV1 round 29, AV-zg-5 MODEL (issuer 2.0.0_SA_COO~D): WHAT CHANGED LEADS THE MODEL TAB.
 *
 * Usage (from the worktree root whose portal/ is the checkout under test):  node <this file>
 * Grades PRD v0.10 FWD-25 (prd/DSGN_AMGTV1_PRD.md ~363-373) and the register rows SAUX-23 and SAUX-34 (Model what-changed cap)
 * (docs/briefs/amgt-security-analysis-ui-findings-20261002.json):
 *   FWD-25 "'What changed' is a panel with a header at the TOP of the Model tab: count tiles (added, changed), then a table of the
 *   changed figures with before, after, signed change and percent change, then per-line detail on demand; it defaults to the latest
 *   two versions that differ; the version list collapses into the picker".  SAUX-34: "Each market-cap figure prints its as-of date
 *   beside it".  TODAY (dcdc89b1): 'WHAT MOVED BETWEEN TWO VERSIONS' sits at the bottom under a plain list of version timestamps,
 *   as text lines with no signed change and no percentage, defaulting to the OLDEST version against the newest.
 * THE CONTRACT (the hooks the worker face names):
 *   [data-what-changed]  exactly ONE panel in the Model tab, before the fiscal table (table[data-model-sheet]) and before the
 *     currency line ([data-model-currency]); attributes data-what-changed-from / data-what-changed-to = the SERVED stamps of the pair
 *     it shows. It carries none of the sheet's hooks (data-model-sheet, -cell, -row, -refused, -absent-footnote, -fiscal-cells).
 *   [data-what-changed-header]  its header, whose text reads "What changed".
 *   [data-what-changed-count="added"] / [data-what-changed-count="changed"]  the count tiles: the served compare denominators
 *     (`denominators.added`, `denominators.changed`) as figures, with the word "added" / "changed".
 *   [data-what-changed-table]  the table; one row [data-what-changed-row="<served compared.changed[].figure>"] per served changed
 *     figure; in each row the cells [data-what-changed-cell="before"|"after"|"change"|"pct"] and ONE per-line detail control
 *     [data-what-changed-detail] that is closed at rest (a <details> with no `open`, or a <button aria-expanded="false">).
 *     "change" opens with a sign (+ for up, - or U+2212 for down; a currency code may stand before or after the sign);
 *     "pct" is a signed percentage "<sign><figure>%" equal to (to - from) / |from| x 100 at the precision shown.
 *     The market-cap row's as-of dates (the two versions' ET days) print in that row or in the table's <thead>.
 *   The picker: the panel's <select> elements offer one <option value="<served stamp>"> per served version, and the pair shown is
 *     the selected options. At rest (outside <select> and outside a closed <details>) no version time other than the pair's prints.
 * The instrument renders the REAL tabs/ModelTab.tsx with the issuer loader (round15/checks/_load.cjs: page hooks stubbed per hook;
 * renderToStaticMarkup, so the default pair must be resolved within one render -- no effect-driven stepping).
 * Inputs: round29/fixtures/model/served.BA_US_Equity.json (the portal's own served BA /thesis, /versions (16 stamps), /compare
 *   (oldest -> newest, 7 changed header figures) and /ledger, copied verbatim). PLANTED in memory (labelled): the /compare answer
 *   for EVERY pair the page asks for -- the served 7 changed figures, removed 0, and added = 100 + the index of the earlier stamp
 *   (so a tile names its pair); a pair inside one content group answers 0 added / 0 removed / 0 changed. Two scenarios:
 *   A  every version differs from every other -> the default pair is 20260930T093755Z -> 20260930T123948Z;
 *   B  the newest three versions (20260930T083927Z, T093755Z, T123948Z) are identical -> the latest two versions that differ are
 *      20260929T024521Z (ET: September 28th, 2026, 10:45p; its UTC day is the 29th) -> 20260930T123948Z.
 * Arms:
 *   1  TOP AND SHAPE (A): one panel above the fiscal table with its header, the two count tiles reading the served counts, one table
 *      row per served changed figure with the four cells and one closed per-line detail; no sheet hook and no code token in it.
 *   2  FIGURES (B): every row's change is signed in the served direction and its percent is the served move; the market-cap row
 *      carries "USD" both sides and names both as-of days in ET (September 28th and 30th; never the UTC 29th); no "$" in the panel.
 *   3  DEFAULT PAIR AND PICKER: A defaults to the newest two; B defaults to the latest two that differ and its added tile reads B's
 *      pair; in A every served stamp is an option, the pair is the selected options, and no other version time prints at rest.
 *   4  PLANTED: the arms' own predicates accept a good synthetic panel and reject 8 mutants (unsigned change, wrong percent,
 *      unsigned percent, detail open at rest, as-of day missing, UTC as-of day, a version list at rest, the panel below the table).
 * Prints one line per arm and "WHAT CHANGED LEADS THE MODEL TAB: <k> of 4 arms"; exit 0 only at 4 of 4. Writes no file.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const D = path.join(__dirname, '..', '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const FX = JSON.parse(fs.readFileSync(path.join(D, 'round29', 'fixtures', 'model', 'served.BA_US_Equity.json'), 'utf8'));
const KEY = 'BA_US_Equity';
const STAMPS = FX.versions.versions.map((v) => v.stamp);
const LATEST = STAMPS[STAMPS.length - 1];
const CHANGED = FX.compare.compared.changed;
const MCAP = CHANGED.find((c) => c.mnemonic === 'CUR_MKT_CAP');

// ---- the estate's own ET form (src/lib/dateUtils.ts formatPanelTimestamp), with its positive control -------------------------
const DU = L.source('src/lib/dateUtils.ts');
const isoOf = (s) => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}T${s.slice(9, 11)}:${s.slice(11, 13)}:${s.slice(13, 15)}Z`;
const CLOCK_ET = /,\s*\d{1,2}:\d{2}[ap] ET$/;
const etLabel = (s) => DU.formatPanelTimestamp(isoOf(s));
const etDay = (s) => etLabel(s).replace(CLOCK_ET, '');
const utcDay = (s) => DU.formatPanelTimestamp(null, `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`).replace(CLOCK_ET, '');
if (etLabel('20261002T154900Z') !== 'October 2nd, 2026, 11:49a ET' || etLabel('20260929T024521Z') !== 'September 28th, 2026, 10:45p ET') {
  console.log(`INSTRUMENT ERROR: the estate ET formatter reads "${etLabel('20261002T154900Z')}" (want "October 2nd, 2026, 11:49a ET")`);
  process.exit(3);
}

// ---- planted /compare answers ---------------------------------------------------------------------------------------------
const GROUP_A = (s) => s;
const GROUP_B = (s) => (STAMPS.indexOf(s) >= STAMPS.length - 3 ? 'NEWEST-THREE' : s);
function compareFor(groupOf) {
  return (key, from, to) => {
    if (!key || !from || !to) return undefined;
    const fi = STAMPS.indexOf(from);
    const ti = STAMPS.indexOf(to);
    if (fi < 0 || ti < 0) return { security_key: KEY, available_stamps: STAMPS.slice(), read: FX.compare.read, compared: null, reason: 'That version is not listed.' };
    const same = groupOf(from) === groupOf(to);
    const added = same ? 0 : 100 + Math.min(fi, ti);
    const changed = same ? [] : CHANGED.map((c) => (fi <= ti ? { ...c } : { ...c, from: c.to, to: c.from }));
    return {
      security_key: KEY,
      available_stamps: STAMPS.slice(),
      read: FX.compare.read,
      reason: null,
      denominators: { versions: STAMPS.length, figures_from: 179, figures_to: 179 + added, added, removed: 0, changed: changed.length, unchanged: 172 },
      compared: { from_stamp: from, to_stamp: to, added: FX.compare.compared.added.slice(0, added), removed: [], changed },
    };
  };
}
const PAIR_A = [STAMPS[STAMPS.length - 2], LATEST];
const PAIR_B = [STAMPS[STAMPS.length - 4], LATEST];

let MT = null;
let loadError = '';
try { MT = L.source(SA + 'tabs/ModelTab.tsx'); } catch (e) { loadError = String(e.message).split('\n')[0]; }
function renderTab(groupOf) {
  L.hookState.impl = {
    useThesisBundle: () => FX.thesis,
    useModelVersions: () => FX.versions,
    useModelCompare: compareFor(groupOf),
    useInputLedger: () => FX.ledger,
  };
  if (!MT) return { html: '', err: 'LOAD: ' + loadError };
  try { return { html: L.render(MT.ModelTab, { securityKey: KEY }), err: '' }; } catch (e) { return { html: '', err: 'RENDER: ' + String(e.message).split('\n')[0] }; }
}

// ---- predicates (pure over HTML; arm 4 feeds them planted HTML) ----------------------------------------------------------------
const dec = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (h) => L.textOf(h || '');
const CODE = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|\|None\|/;
const SHEET_HOOKS = ['data-model-sheet', 'data-model-cell', 'data-model-row', 'data-model-refused', 'data-model-absent-footnote', 'data-model-fiscal-cells'];

/** The HTML with every CLOSED <details> body removed (its <summary> kept): what a reader sees before opening anything. */
function atRest(html) {
  let out = '';
  let i = 0;
  const open = /<details\b[^>]*>/g;
  for (;;) {
    open.lastIndex = i;
    const hit = open.exec(html);
    if (!hit) { out += html.slice(i); break; }
    if (/\sopen(?=[\s=>/])/.test(hit[0])) { out += html.slice(i, open.lastIndex); i = open.lastIndex; continue; }
    const pair = /<(\/?)details\b[^>]*>/g;
    pair.lastIndex = open.lastIndex;
    let depth = 1;
    let end = html.length;
    let m;
    while ((m = pair.exec(html)) !== null) { depth += m[1] ? -1 : 1; if (depth === 0) { end = m.index; break; } }
    const summary = /<summary\b[^>]*>[\s\S]*?<\/summary>/.exec(html.slice(open.lastIndex, end));
    out += html.slice(i, hit.index) + (summary ? summary[0] : '');
    i = Math.min(html.length, end + '</details>'.length);
  }
  return out;
}
function openTag(html, needle) {
  const at = html.indexOf(needle);
  if (at < 0) return null;
  const start = html.lastIndexOf('<', at);
  return { tag: html.slice(start, html.indexOf('>', at) + 1), index: start };
}
const attrOf = (tag, name) => { const m = new RegExp('\\s' + name + '="([^"]*)"').exec(tag || ''); return m ? dec(m[1]) : null; };
const rowsOf = (inner) => L.attrValues(inner, 'data-what-changed-row').map((v) => dec(v.value));
const rowInner = (inner, figure) => L.innerOf(inner, 'data-what-changed-row', figure.replace(/&/g, '&amp;').replace(/"/g, '&quot;'));

function shapeFaults(html, want) {
  const f = [];
  const n = (html.match(/\sdata-what-changed="/g) || []).length;
  if (n !== 1) { f.push(`${n} [data-what-changed] panels in the Model tab (want 1)`); if (n === 0) return f; }
  const panel = openTag(html, 'data-what-changed="');
  const inner = L.innerOf(html, 'data-what-changed');
  const head = L.innerOf(inner, 'data-what-changed-header');
  if (head === null) f.push('no [data-what-changed-header]');
  else if (!/what changed/i.test(text(head))) f.push(`the header reads "${text(head).slice(0, 60)}", not "What changed"`);
  const sheetAt = html.indexOf('data-model-sheet');
  const currencyAt = html.indexOf('data-model-currency=');
  if (sheetAt < 0) f.push('no table[data-model-sheet] rendered (the positive control: the sheet must still render)');
  else if (panel.index > sheetAt) f.push('the panel sits BELOW the fiscal table');
  if (currencyAt >= 0 && panel.index > currencyAt) f.push('the panel sits below the "Figures in" currency line');
  for (const [kind, num] of [['added', want.added], ['changed', want.changed]]) {
    const tile = L.innerOf(inner, 'data-what-changed-count', kind);
    if (tile === null) { f.push(`no [data-what-changed-count="${kind}"] tile`); continue; }
    const nums = (text(tile).match(/\d[\d,]*/g) || []).map((x) => Number(x.replace(/,/g, '')));
    if (!nums.includes(num)) f.push(`the ${kind} tile reads "${text(tile)}" (want the served ${num})`);
    if (!new RegExp(kind, 'i').test(text(tile))) f.push(`the ${kind} tile does not say "${kind}"`);
  }
  if (L.innerOf(inner, 'data-what-changed-table') === null) f.push('no [data-what-changed-table]');
  const rows = rowsOf(inner);
  const missing = want.figures.filter((x) => !rows.includes(x));
  const extra = rows.filter((x) => !want.figures.includes(x));
  if (missing.length || extra.length) f.push(`${rows.length} rows against ${want.figures.length} served changed figures (missing ${missing.length}, extra ${extra.length})`);
  for (const fig of rows) {
    const r = rowInner(inner, fig) || '';
    for (const k of ['before', 'after', 'change', 'pct']) if (L.innerOf(r, 'data-what-changed-cell', k) === null) { f.push(`${fig}: no ${k} cell`); break; }
    f.push(...detailFaults(r).map((x) => `${fig}: ${x}`));
  }
  for (const h of SHEET_HOOKS) if (inner.includes(h + '=')) f.push(`the panel carries the sheet hook ${h}`);
  const restText = text(atRest(inner));
  if (CODE.test(restText)) f.push(`a code token at rest in the panel: "${restText.match(CODE)[0]}"`);
  return f;
}
function detailFaults(r) {
  const det = [...r.matchAll(/<(details|button)\b[^>]*\sdata-what-changed-detail\b[^>]*>/g)];
  if (det.length !== 1) return [`${det.length} per-line detail controls (want 1: a <details> or a <button>)`];
  const tag = det[0][0];
  if (det[0][1] === 'details' ? /\sopen(?=[\s=>/])/.test(tag) : !/\saria-expanded="false"/.test(tag)) return ['the per-line detail is open at rest'];
  return [];
}
function rowFaults(r, change) {
  const f = [];
  const cell = (k) => L.innerOf(r, 'data-what-changed-cell', k);
  for (const k of ['before', 'after', 'change', 'pct']) if (cell(k) === null) f.push(`no ${k} cell`);
  if (f.length) return f;
  const from = Number(change.from);
  const to = Number(change.to);
  const dir = to > from ? '+' : to < from ? '-' : '0';
  for (const k of ['before', 'after']) if (!/\d/.test(text(cell(k)))) f.push(`the ${k} cell "${text(cell(k))}" carries no figure`);
  const changeText = text(cell('change'));
  const cm = /^([+\-\u2212])\s?\d/.exec(changeText.replace(/\b[A-Z]{3}\b\s?/g, '').trim());
  if (!cm) f.push(`the change "${changeText}" carries no sign`);
  else if ((cm[1] === '+' ? '+' : '-') !== dir) f.push(`the change "${changeText}" is signed ${cm[1]} but the served move is ${dir}`);
  const pctText = text(cell('pct'));
  const pm = /^([+\-\u2212])\s?(\d[\d,]*)(?:\.(\d+))?\s?%$/.exec(pctText);
  if (!pm) f.push(`the percent "${pctText}" is not a signed percentage`);
  else {
    const want = ((to - from) / Math.abs(from)) * 100;
    const shown = Number(pm[2].replace(/,/g, '') + (pm[3] ? '.' + pm[3] : '')) * (pm[1] === '+' ? 1 : -1);
    if (Math.abs(shown - want) > 0.5 * Math.pow(10, -(pm[3] ? pm[3].length : 0)) + 1e-9) f.push(`the percent "${pctText}" but the served move is ${want.toFixed(3)}%`);
  }
  return f;
}
function asOfFaults(inner, figure, fromStamp, toStamp) {
  const f = [];
  const table = L.innerOf(inner, 'data-what-changed-table') || '';
  const thead = /<thead\b[\s\S]*?<\/thead>/.exec(table);
  const beside = text(rowInner(inner, figure) || '') + ' | ' + (thead ? text(thead[0]) : '');
  for (const [which, s] of [['earlier', fromStamp], ['later', toStamp]]) {
    if (!beside.includes(etDay(s))) f.push(`the ${which} as-of day "${etDay(s)}" is not beside the market cap`);
    if (utcDay(s) !== etDay(s) && beside.includes(utcDay(s))) f.push(`the ${which} version's UTC day "${utcDay(s)}" is beside the market cap`);
  }
  return f;
}
function restListFaults(html, pair) {
  const rest = text(atRest(html).replace(/<select\b[\s\S]*?<\/select>/g, ' '));
  const listed = STAMPS.filter((s) => {
    if (pair.includes(s)) return false;
    const hm = `${s.slice(9, 11)}:${s.slice(11, 13)}`;
    return rest.includes(etLabel(s)) || rest.includes(`${hm} UTC`) || rest.includes(`${hm}:${s.slice(13, 15)} UTC`);
  });
  return listed.length ? [`${listed.length} version times outside the pair print at rest (a plain list; first ${listed[0]})`] : [];
}
function pickerFaults(inner, pair) {
  const f = [];
  const selects = [...inner.matchAll(/<select\b[\s\S]*?<\/select>/g)].map((m) => m[0]);
  if (selects.length === 0) return ['no <select> picker in the panel'];
  const opts = selects.flatMap((s) => [...s.matchAll(/<option\b([^>]*)>/g)].map((m) => ({ value: attrOf(m[0], 'value'), selected: /\sselected=""/.test(m[1]) })));
  const missing = STAMPS.filter((s) => !opts.some((o) => o.value === s));
  if (missing.length) f.push(`${missing.length} of ${STAMPS.length} served versions are not an option value in the picker (first ${missing[0]})`);
  const selected = opts.filter((o) => o.selected).map((o) => o.value);
  for (const s of pair) if (!selected.includes(s)) f.push(`the picker does not show ${s} selected (selected: ${selected.join(', ') || 'none'})`);
  return f;
}
function pairFaults(html, pair, added) {
  const f = [];
  const panel = openTag(html, 'data-what-changed="');
  if (!panel) return ['no [data-what-changed] panel'];
  const got = [attrOf(panel.tag, 'data-what-changed-from'), attrOf(panel.tag, 'data-what-changed-to')];
  if (got[0] !== pair[0] || got[1] !== pair[1]) f.push(`the default pair is ${got[0]} -> ${got[1]} (want ${pair[0]} -> ${pair[1]})`);
  const tile = L.innerOf(L.innerOf(html, 'data-what-changed') || '', 'data-what-changed-count', 'added');
  const nums = (text(tile).match(/\d[\d,]*/g) || []).map((x) => Number(x.replace(/,/g, '')));
  if (!nums.includes(added)) f.push(`the added tile reads "${text(tile)}" (the shown pair serves ${added})`);
  return f;
}

const arms = [];
const A = renderTab(GROUP_A);
const B = renderTab(GROUP_B);
const innerA = L.innerOf(A.html, 'data-what-changed') || '';
const innerB = L.innerOf(B.html, 'data-what-changed') || '';
const addedFor = (pair) => 100 + STAMPS.indexOf(pair[0]);

// Arm 1 -- top and shape (scenario A).
{
  const f = A.err ? [A.err] : shapeFaults(A.html, { added: addedFor(PAIR_A), changed: CHANGED.length, figures: CHANGED.map((c) => c.figure) });
  arms.push(['TOP AND SHAPE: one What-changed panel above the fiscal table, its header, the added and changed tiles, one row per served changed figure with before/after/change/percent and one closed detail', f.length === 0,
    f.length ? `${f.length} faults: ${f.slice(0, 4).join(' | ')}` : `1 panel above the sheet; tiles ${addedFor(PAIR_A)} added / ${CHANGED.length} changed; ${CHANGED.length} of ${CHANGED.length} rows`]);
}
// Arm 2 -- figures (scenario B).
{
  const f = [];
  if (B.err) f.push(B.err);
  else if (!innerB) f.push('no [data-what-changed] panel');
  else {
    for (const c of CHANGED) {
      const r = rowInner(innerB, c.figure);
      if (r === null) { f.push(`${c.mnemonic}: no row`); continue; }
      f.push(...rowFaults(r, c).map((x) => `${c.mnemonic}: ${x}`));
    }
    const mr = rowInner(innerB, MCAP.figure);
    if (mr !== null) {
      for (const k of ['before', 'after']) if (!/\bUSD\b/.test(text(L.innerOf(mr, 'data-what-changed-cell', k)))) f.push(`market cap ${k} does not carry the served currency USD`);
      f.push(...asOfFaults(innerB, MCAP.figure, PAIR_B[0], PAIR_B[1]));
    }
    if (/\$/.test(text(innerB))) f.push('a "$" sign in the panel (ruling a: "<code> <figure>")');
  }
  arms.push(['FIGURES: each change signed in the served direction, each percent the served move, the market cap in USD with both as-of days in ET', f.length === 0,
    f.length ? `${f.length} faults: ${f.slice(0, 4).join(' | ')}` : `${CHANGED.length} of ${CHANGED.length} rows signed and exact; market cap names ${etDay(PAIR_B[0])} and ${etDay(PAIR_B[1])}`]);
}
// Arm 3 -- default pair and picker.
{
  const f = [];
  if (A.err) f.push('A ' + A.err);
  else f.push(...pairFaults(A.html, PAIR_A, addedFor(PAIR_A)).map((x) => 'A: ' + x), ...pickerFaults(innerA, PAIR_A).map((x) => 'A: ' + x), ...restListFaults(A.html, PAIR_A).map((x) => 'A: ' + x));
  if (B.err) f.push('B ' + B.err);
  else f.push(...pairFaults(B.html, PAIR_B, addedFor(PAIR_B)).map((x) => 'B: ' + x));
  arms.push(['DEFAULT PAIR AND PICKER: the latest two versions that differ by default, every version in the picker, no version list at rest', f.length === 0,
    f.length ? `${f.length} faults: ${f.slice(0, 4).join(' | ')}` : `A ${PAIR_A.join(' -> ')}; B ${PAIR_B.join(' -> ')} (3 identical skipped); ${STAMPS.length} options; 0 version times at rest outside the pair`]);
}
// Arm 4 -- planted.
{
  const f = [];
  const [pf, pt] = PAIR_B;
  const opt = (sel) => STAMPS.map((s) => `<option value="${s}"${s === sel ? ' selected=""' : ''}>${etLabel(s)}</option>`).join('');
  const panel = `<section data-what-changed="" data-what-changed-from="${pf}" data-what-changed-to="${pt}"><h3 data-what-changed-header="">What changed</h3>`
    + `<div data-what-changed-count="added">112 added</div><div data-what-changed-count="changed">1 changed</div>`
    + `<label>Earlier <select>${opt(pf)}</select></label><label>Later <select>${opt(pt)}</select></label>`
    + `<table data-what-changed-table=""><thead><tr><th>Figure</th><th>Before, ${etDay(pf)}</th><th>After, ${etDay(pt)}</th><th>Change</th><th>Change, %</th><th></th></tr></thead>`
    + `<tbody><tr data-what-changed-row="${MCAP.figure}"><td>Market cap</td><td data-what-changed-cell="before">USD 162B</td><td data-what-changed-cell="after">USD 156B</td>`
    + `<td data-what-changed-cell="change">-USD 6.3B</td><td data-what-changed-cell="pct">-3.9%</td>`
    + `<td><details data-what-changed-detail=""><summary>Detail</summary>Market cap, full figures</details></td></tr></tbody></table></section>`;
  const sheet = '<p data-model-currency="USD">Figures in USD</p><table data-model-sheet=""></table>';
  const good = `<div data-tab-panel="model">${panel}${sheet}</div>`;
  const want = { added: 112, changed: 1, figures: [MCAP.figure] };
  const judge = (html) => {
    const inner = L.innerOf(html, 'data-what-changed') || '';
    return [...shapeFaults(html, want), ...rowFaults(rowInner(inner, MCAP.figure) || '', MCAP), ...asOfFaults(inner, MCAP.figure, pf, pt),
      ...restListFaults(html, PAIR_B), ...pickerFaults(inner, PAIR_B), ...pairFaults(html, PAIR_B, 112)];
  };
  const g = judge(good);
  if (g.length) f.push(`the good panel is rejected: ${g[0]}`);
  const mutants = [
    ['unsigned change', good.replace('>-USD 6.3B<', '>USD 6.3B<')],
    ['wrong percent', good.replace('>-3.9%<', '>-3.1%<')],
    ['unsigned percent', good.replace('>-3.9%<', '>3.9%<')],
    ['detail open at rest', good.replace('<details data-what-changed-detail="">', '<details data-what-changed-detail="" open="">')],
    ['as-of day missing', good.replace(`<th>Before, ${etDay(pf)}</th>`, '<th>Before</th>')],
    ['UTC as-of day', good.split(etDay(pf)).join(utcDay(pf))],
    ['a version list at rest', good.replace(sheet, `<ul><li>The version of ${etLabel(STAMPS[3])}</li></ul>${sheet}`)],
    ['panel below the table', `<div data-tab-panel="model">${sheet}${panel}</div>`],
  ];
  let caught = 0;
  for (const [name, html] of mutants) { if (judge(html).length) caught += 1; else f.push(`mutant "${name}" accepted`); }
  arms.push(['PLANTED: the predicates accept a good synthetic panel and reject 8 mutants', f.length === 0, f.length ? f.join(' | ') : `good accepted; ${caught} of ${mutants.length} mutants rejected`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`WHAT CHANGED LEADS THE MODEL TAB: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
