/**
 * served.cjs -- DSGN_AMGTV1 round 30, AV-zh-2 REPAIRS, check 2 of 2 (issuer 2.0.0_SA_COO~D): A SERVED VALUE PRINTS AS SERVED --
 * A LINK ONLY WHERE A URL IS SERVED, A FIGURE AT ITS DISPLAY PRECISION.
 *
 * Usage: cd <dir whose portal/ is the checkout under test> && node <this file>
 *   (e.g. cd C:/tmp/wk-dsgn-amgtv1-82). Static renders only; no network, no AWS, writes no file.
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see round15/checks/_load.cjs) is honoured for every source read here.
 * Grades:
 *   COO~Z msg 28802 (RESAPP row Z-W212-S2): after RESAPP's next redeploy the overlay feed serves `url: null` (harvested gold carries
 *     no url); components/HeaderBrief.tsx (~:89 at e370eb7c) wraps every title in <a href={item.url}>, so a null url draws an
 *     anchor with no href. PRD FWD-27 (prd/DSGN_AMGTV1_PRD.md ~407): "an unconnected field prints no line" -- a link with no
 *     target is not drawn.
 *   CTO msg 28833 (from CVO~Z v33), FWD-27 rounding: components/model/WhatChangedPanel.tsx prints served compare values
 *     unrounded ("2.9039" -> "3.036", round11/fixtures/compare.BA_US_Equity.oldest-latest.json, SHORT_INT_RATIO). Each before /
 *     after value prints at the figure's display precision through the page's existing formatter, never raw.
 * THE DISPLAY PRECISION (what arm 2 reads; every function is the page's own, loaded from the checkout):
 *   (a) a mnemonic the header maps format (constants.ts HEADER_CARD_DEFS, then STAT_TILE_DEFS -- WhatChangedPanel's own
 *       HEADER_FORMATS precedence): StatTile.formatStatValue(value, format, money ? figure.currency : undefined, figure.unit),
 *       the figure being the served header_figures entry for a header-scope change;
 *   (b) else a Model sheet line (modelSheet.ts FINANCIAL_SUMMARY_ROWS / MARGIN_HISTORY_ROWS by mnemonic, or the row whose label
 *       FORECAST_MNEMONICS maps to it): modelSheet.formatSheetValue(<that row's type>, value);
 *   (c) else any other numeric line: modelSheet.formatSheetValue(undefined, value) (the sheet's untyped format: 2 places,
 *       grouped). A non-numeric served value is not graded.
 * Inputs: round30/fixtures/repairs/overlay.BA_US_Equity.urlnull.PLANTED.json (built by r30r.build.cjs: 5 feed items, 3 with url
 *   null across the open three and the "Expand" details); round14/fixtures/overlay.BA_US_Equity.json (SERVED: 1 item, url served);
 *   round29/fixtures/model/served.BA_US_Equity.json (SERVED /thesis, /versions and the 7 changed header figures of /compare).
 *   PLANTED in memory (labelled): 6 sheet-scope changed lines with long fractions (IS_EPS perShare, PE_RATIO multiple,
 *   EBITDA_MARGIN percent, EBITDA amount, BEST_EPS forecast of the EPS row, BS_CASH_NEAR_CASH_ITEM untyped), answered with the 7
 *   served ones by a stubbed useModelCompare for every pair.
 * Arms:
 *   1  FEED LINKS: HeaderBrief alone, on the planted feed and on the served BA feed: each served item has one [data-feed-item]
 *      row holding its title; a row whose url is served holds an <a href="<url>">; a row whose url is null holds no <a>; the
 *      card holds no <a> without an href; and round29/checks/timeline/dayopen.cjs (as AMENDED this round) still exits 0.
 *   2  ROUNDING: WhatChangedPanel on the 7 served + 6 planted changed lines: every [data-what-changed-cell="before"|"after"]
 *      reads exactly the display-precision text above (13 rows x 2 cells); and round29/checks/model/whatchanged.cjs and
 *      etwords.cjs still exit 0 (battery29.sh runs none of the three).
 *   3  PLANTED: the feed-link predicate rejects 4 bad lists and accepts 1 good one; the rounding predicate rejects 4 bad cells
 *      (4-place SHORT_INT_RATIO, 4-place EPS, an EPS rounded to a whole number, a 2-place P/E) and accepts the display texts.
 * Prints one line per arm and "A SERVED VALUE PRINTS AS SERVED: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8'));
const pay = (x) => (x && x.payload ? x.payload : x);
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const { spawnSync } = require('child_process');
/** The round-29 checks over the same files must still exit 0 (same cwd, same env -- so the same CHECK_SRC_OVERRIDE). */
function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 300000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 90)}")`);
  }
  return faults;
}

// ---- a small HTML tree (react-dom/server markup is well formed) -------------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:-]*)\s*>|<([a-zA-Z][\w:-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1]) { let n = cur; while (n && n.tag !== m[1].toLowerCase()) n = n.parent; if (n && n.parent) cur = n.parent; }
    else if (m[2]) {
      const attrs = {};
      const ar = /([^\s=>\/]+)(?:="([^"]*)")?/g;
      let a;
      while ((a = ar.exec(m[3] || '')) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
      const node = { tag: m[2].toLowerCase(), attrs, children: [], parent: cur };
      cur.children.push(node);
      if (!m[4] && !VOID.has(node.tag)) cur = node;
    } else if (m[5]) cur.children.push({ text: decode(m[5]), parent: cur });
  }
  return root;
}
function all(node, pred, out = []) { for (const c of node.children || []) if (c.tag) { if (pred(c)) out.push(c); all(c, pred, out); } return out; }
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const text = (n) => (n.text !== undefined ? n.text : (n.children || []).map(text).join(' '));
const visible = (n) => norm(text(n));
const byAttr = (tree, attr, value) => all(tree, (n) => n.attrs[attr] !== undefined && (value === undefined || n.attrs[attr] === value));

// ---- arm 1 predicate: feed links ---------------------------------------------------------------------------------------------
/** A row links ONLY where a url is served; a null url renders the title as plain text; no <a> without an href in the card. */
function feedLinkFaults(tree, items) {
  const f = [];
  const bare = all(tree, (n) => n.tag === 'a' && !String(n.attrs.href || '').trim());
  if (bare.length) f.push(`${bare.length} <a> without an href (first "${visible(bare[0]).slice(0, 50)}")`);
  for (const it of items || []) {
    const k = String(it.article_key).slice(0, 34);
    const rows = byAttr(tree, 'data-feed-item', it.article_key);
    if (rows.length !== 1) { f.push(`${k}: ${rows.length} [data-feed-item] rows (want 1)`); continue; }
    const links = all(rows[0], (n) => n.tag === 'a');
    const served = typeof it.url === 'string' && it.url.trim() !== '';
    if (served && !links.some((a) => a.attrs.href === it.url)) f.push(`${k}: a url is served and the row has no <a href="<url>"> (${links.length} link(s))`);
    if (!served && links.length) f.push(`${k}: no url is served and the row draws ${links.length} <a>${links[0].attrs.href === undefined ? ' with no href' : ''}`);
    const title = norm(it.title || '');
    if (title && !visible(rows[0]).includes(title)) f.push(`${k}: the title "${title.slice(0, 40)}" is not in the row`);
  }
  return f;
}

// ---- arm 2: the page's own formatters --------------------------------------------------------------------------------------
let FMT = null;
let fmtErr = '';
try {
  const ST = L.source(SA + 'components/StatTile.tsx');
  const MS = L.source(SA + 'modelSheet.ts');
  const C = L.source(SA + 'constants.ts');
  const headerFormats = {};
  for (const card of C.HEADER_CARD_DEFS) for (const fig of card.figures) if (fig.mnemonic && !headerFormats[fig.mnemonic]) headerFormats[fig.mnemonic] = { format: fig.format, money: Boolean(fig.money) };
  for (const tile of C.STAT_TILE_DEFS) if (!headerFormats[tile.mnemonic]) headerFormats[tile.mnemonic] = { format: tile.format, money: !['ratio', 'percent', 'shares-abs'].includes(tile.format) };
  const sheetTypes = {};
  for (const row of [...MS.FINANCIAL_SUMMARY_ROWS, ...MS.MARGIN_HISTORY_ROWS]) {
    const type = row.type || 'other';
    if (row.mnemonic && !sheetTypes[row.mnemonic]) sheetTypes[row.mnemonic] = type;
    const fc = MS.FORECAST_MNEMONICS[row.label];
    if (fc && !sheetTypes[fc]) sheetTypes[fc] = type;
  }
  FMT = { formatStatValue: ST.formatStatValue, formatSheetValue: MS.formatSheetValue, headerFormats, sheetTypes };
} catch (e) { fmtErr = 'FORMATTERS: ' + first(e); }
const numeric = (v) => { if (v === null || v === undefined) return null; const n = typeof v === 'number' ? v : String(v).trim() === '' ? NaN : Number(v); return Number.isFinite(n) ? n : null; };
/** The display-precision text of one served value of one changed line, or null when the value is not graded. */
function displayText(change, value, headerFigures) {
  if (value === null || value === undefined) return null;
  const known = FMT.headerFormats[change.mnemonic];
  if (known) {
    const fig = change.scope === 'header' ? (headerFigures || []).find((x) => x.mnemonic === change.mnemonic) : undefined;
    const t = FMT.formatStatValue(value, known.format, known.money ? (fig && fig.currency) || null : undefined, fig && fig.unit);
    if (t !== null) return t;
  }
  const n = numeric(value);
  if (n === null) return null;
  return FMT.formatSheetValue(FMT.sheetTypes[change.mnemonic], n);
}
/** rows: [{ change, before, after }] (cell texts). */
function roundingFaults(rows, headerFigures) {
  const f = [];
  for (const r of rows) {
    for (const [k, v] of [['before', r.change.from], ['after', r.change.to]]) {
      const want = displayText(r.change, v, headerFigures);
      if (want === null) continue;
      const got = r[k];
      if (got === null || got === undefined) f.push(`${r.change.mnemonic}: no ${k} cell`);
      else if (norm(got) !== want) f.push(`${r.change.mnemonic} ${k} "${norm(got)}" (served ${v}; display "${want}")`);
    }
  }
  return f;
}

const MODEL = readJson('round29/fixtures/model/served.BA_US_Equity.json');
const STAMPS = MODEL.versions.versions.map((v) => v.stamp);
const SERVED_CHANGED = MODEL.compare.compared.changed;
// PLANTED (labelled): sheet-scope lines with long fractions, one per row type, a forecast mnemonic and an untyped line.
const PLANTED_CHANGED = [
  { figure: 'fiscal_year_line_item|2025|IS_EPS', mnemonic: 'IS_EPS', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 3.456789, to: 3.51234 },
  { figure: 'fiscal_year_line_item|2025|PE_RATIO', mnemonic: 'PE_RATIO', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 23.456789, to: 24.104321 },
  { figure: 'fiscal_year_line_item|2025|EBITDA_MARGIN', mnemonic: 'EBITDA_MARGIN', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 12.345678, to: 11.98765 },
  { figure: 'fiscal_year_line_item|2025|EBITDA', mnemonic: 'EBITDA', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 1234567.891234, to: 1301234.56789 },
  { figure: 'forecast|2027|BEST_EPS', mnemonic: 'BEST_EPS', fiscal_year: 2027, scope: 'forecast', from: 4.123456, to: 4.209871 },
  { figure: 'fiscal_year_line_item|2025|BS_CASH_NEAR_CASH_ITEM', mnemonic: 'BS_CASH_NEAR_CASH_ITEM', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 13801.123456, to: 12345.987654 },
];
const CHANGED = [...SERVED_CHANGED, ...PLANTED_CHANGED];
const COMPARE = {
  security_key: 'BA_US_Equity', available_stamps: STAMPS.slice(), read: MODEL.compare.read, reason: null,
  denominators: { versions: STAMPS.length, figures_from: 179, figures_to: 179, added: 0, removed: 0, changed: CHANGED.length, unchanged: 172 },
  compared: { from_stamp: STAMPS[STAMPS.length - 2], to_stamp: STAMPS[STAMPS.length - 1], added: [], removed: [], changed: CHANGED },
};
const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
const cellsOf = (html, change) => {
  const row = L.innerOf(html, 'data-what-changed-row', esc(change.figure));
  if (row === null) return { change, before: null, after: null };
  const c = (k) => { const x = L.innerOf(row, 'data-what-changed-cell', k); return x === null ? null : L.textOf(x); };
  return { change, before: c('before'), after: c('after') };
};

const arms = [];
// ---- arm 1: FEED LINKS ---------------------------------------------------------------------------------------------------------
{
  const f = [];
  const counts = [];
  let HB = null;
  try { HB = L.source(SA + 'components/HeaderBrief.tsx').HeaderBrief; if (typeof HB !== 'function') throw new Error('HeaderBrief.tsx exports no HeaderBrief'); } catch (e) { f.push('LOAD: ' + first(e)); }
  if (HB) {
    for (const [name, file] of [['planted url-null feed', 'round30/fixtures/repairs/overlay.BA_US_Equity.urlnull.PLANTED.json'], ['served BA feed', 'round14/fixtures/overlay.BA_US_Equity.json']]) {
      const bundle = pay(readJson(file));
      let html = '';
      try { html = L.render(HB, { bundle }); } catch (e) { f.push(`${name}: RENDER ${first(e)}`); continue; }
      const items = bundle.feed.items;
      f.push(...feedLinkFaults(parse(html), items).map((x) => `${name}: ${x}`));
      const nul = items.filter((i) => !(typeof i.url === 'string' && i.url.trim())).length;
      counts.push(`${name} ${items.length} items (${nul} url null)`);
    }
  }
  f.push(...keepsPassing(['round29/checks/timeline/dayopen.cjs']));
  arms.push(['FEED LINKS: a feed item links only where a url is served; a null url prints its title as plain text; no <a> without an href (msg 28802, Z-W212-S2)', f.length === 0,
    f.length === 0 ? `${counts.join('; ')}: every served url linked, every null url plain, 0 bare <a>; round-29 dayopen.cjs (amended) exits 0` : `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}`]);
}
// ---- arm 2: ROUNDING -----------------------------------------------------------------------------------------------------------
{
  const f = [];
  let n = 0;
  if (!FMT) f.push(fmtErr);
  else {
    L.hookState.impl = { useModelCompare: () => COMPARE, useThesisBundle: () => MODEL.thesis, useModelVersions: () => MODEL.versions, useInputLedger: () => MODEL.ledger };
    let html = '';
    try {
      const W = L.source(SA + 'components/model/WhatChangedPanel.tsx').WhatChangedPanel;
      html = L.render(W, { securityKey: 'BA_US_Equity', stamps: STAMPS, data: MODEL.thesis, latestAbsent: false });
    } catch (e) { f.push('RENDER: ' + first(e)); }
    if (html) {
      const rows = CHANGED.map((c) => cellsOf(html, c));
      const missing = rows.filter((r) => r.before === null && r.after === null);
      if (missing.length) f.push(`${missing.length} of ${CHANGED.length} changed lines have no row (first ${missing[0].change.figure})`);
      f.push(...roundingFaults(rows.filter((r) => !missing.includes(r)), MODEL.thesis.header_figures));
      n = rows.length - missing.length;
    }
  }
  f.push(...keepsPassing(['round29/checks/model/whatchanged.cjs', 'round29/checks/model/etwords.cjs']));
  const sir = SERVED_CHANGED.find((c) => c.mnemonic === 'SHORT_INT_RATIO');
  arms.push(['ROUNDING: every What-changed before/after value prints at its display precision through the page\'s own formatter, never raw (FWD-27, CTO msg 28833)', f.length === 0,
    f.length === 0 ? `${n} of ${CHANGED.length} lines (7 served + 6 planted) x 2 cells at display precision${sir ? `, e.g. SHORT_INT_RATIO ${displayText(sir, sir.from, [])} -> ${displayText(sir, sir.to, [])}` : ''}; round-29 whatchanged.cjs and etwords.cjs exit 0` : `${f.length} fault(s): ${f.slice(0, 5).join(' | ')}`]);
}
// ---- arm 3: PLANTED ------------------------------------------------------------------------------------------------------------
{
  const f = [];
  let bad = 0; let rejected = 0; let good = 0; let accepted = 0;
  const rej = (name, faults) => { bad += 1; if (faults.length) rejected += 1; else f.push(`"${name}" accepted`); };
  const acc = (name, faults) => { good += 1; if (!faults.length) accepted += 1; else f.push(`"${name}" rejected: ${faults[0]}`); };
  const ITEMS = [{ article_key: 'k:served', url: 'https://example.com/a?x=1&y=2', title: 'Served headline' }, { article_key: 'k:null', url: null, title: 'Harvested headline' }];
  const list = (rs, rn) => parse(`<div data-header-feed="SERVED"><ul><li data-feed-item="k:served">${rs}</li></ul><details data-feed-expand=""><summary>Expand (1 more)</summary><ul><li data-feed-item="k:null">${rn}</li></ul></details></div>`);
  const LINKED = '<a href="https://example.com/a?x=1&amp;y=2" target="_blank" rel="noreferrer">Served headline</a><div>Reuters -- September 24th, 2026</div>';
  const PLAIN = '<span>Harvested headline</span><div>Reuters -- September 29th, 2026</div>';
  acc('a correct mixed list', feedLinkFaults(list(LINKED, PLAIN), ITEMS));
  rej('a null url drawn as an <a> with no href', feedLinkFaults(list(LINKED, '<a target="_blank" rel="noreferrer">Harvested headline</a>'), ITEMS));
  rej('a null url drawn as <a href="">', feedLinkFaults(list(LINKED, '<a href="">Harvested headline</a>'), ITEMS));
  rej('a served url with its link dropped', feedLinkFaults(list('<span>Served headline</span>', PLAIN), ITEMS));
  rej('a null-url row with its title dropped', feedLinkFaults(list(LINKED, '<span></span><div>Reuters</div>'), ITEMS));
  if (FMT) {
    const sir = SERVED_CHANGED.find((c) => c.mnemonic === 'SHORT_INT_RATIO');
    const eps = PLANTED_CHANGED[0];
    const pe = PLANTED_CHANGED[1];
    const HF = MODEL.thesis.header_figures;
    const ok = (c) => ({ change: c, before: displayText(c, c.from, HF), after: displayText(c, c.to, HF) });
    if (sir) rej('SHORT_INT_RATIO at 4 places', roundingFaults([{ change: sir, before: '2.9039', after: '3.036' }], HF));
    else f.push('the served compare carries no SHORT_INT_RATIO line');
    rej('EPS at 4 places', roundingFaults([{ change: eps, before: '3.4568', after: '3.5123' }], HF));
    rej('EPS rounded to a whole number', roundingFaults([{ change: eps, before: '3', after: '4' }], HF));
    rej('P/E at 2 places', roundingFaults([{ change: pe, before: '23.46x', after: '24.10x' }], HF));
    acc('every line at its display text', roundingFaults(CHANGED.map(ok), HF));
  } else f.push(fmtErr);
  arms.push(['PLANTED: the feed-link predicate rejects 4 bad lists and accepts a good one; the rounding predicate rejects raw and mis-rounded cells and accepts the display texts', f.length === 0,
    f.length === 0 ? `${rejected} of ${bad} bad inputs rejected; ${accepted} of ${good} good inputs accepted` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`A SERVED VALUE PRINTS AS SERVED: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
