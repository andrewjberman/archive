/**
 * figures.cjs -- DSGN_AMGTV1 round 29, AV-zg-2 OVERLAY HEADER (issuer 2.0.0_SA_COO~D): THE KEY FIGURES READ ONCE, FORMATTED, DATED, IN READER WORDS.
 *
 * Usage: cd <dir whose portal/ is the checkout under test> && node <this file>
 *   (e.g. cd C:/tmp/wk-dsgn-amgtv1-70). Static renders only; no network, no AWS, writes no file.
 * Grades (PRD v0.10 @175e4081b1, FWD-27 and the register docs/briefs/amgt-security-analysis-ui-findings-20261002.json):
 *   SAUX-03: one key-figures surface where every figure shows at rest, OR each opened detail adds only figures not on the face; no
 *     figure appears twice. Graded as the union: over the header face and every detail body, each of the seven key figures (price,
 *     market cap, enterprise value, net debt, beta, average volume, short interest) is shown exactly once.
 *   SAUX-04: a figure's tooltip shows the formatted value and its source in words ("Bloomberg"); no unformatted number (e.g.
 *     '187187.819936') and no system source id ('bloomberg-dapi').
 *   SAUX-30 (header lines): "Back to universe" and "Export rich text (.md)" do not render; each control stays, in reader words.
 *   SAUX-31 (header lines): a figure with no source prints no line ('<X> is not in the data yet', constants.ts HEADER_CARD_DEFS
 *     emptyLine, HeaderCards.tsx HeaderCardDetail); a key-figures panel with nothing to show renders ONE designed empty state.
 *   SAUX-33 (header): money prints '<served currency code> <figure>' ('USD 196.80', 'USD 187B'), never '$'.
 *   SAUX-34 (header): each market-cap figure prints its as-of date beside it.
 * THE FIGURE UNIT: a shown key figure is the element that is the PARENT of its FigureTooltip -- `[role="tooltip"][data-mnemonic=
 *   "<MNEMONIC>"]` (StatTile.tsx's FigureTooltip contract: "the parent element is `group relative`"). Its FACE TEXT is the parent's
 *   visible text with the tooltip's subtree removed; its TOOLTIP TEXT is the tooltip's visible text. The census counts these
 *   tooltips per mnemonic (short interest = SI_PERCENT_EQUITY_FLOAT or SHORT_INT_RATIO, summed).
 * DETAIL BODIES: a static render never mounts a closed dialog, so a detail body is rendered directly: `HeaderCardDetail({ cardKey,
 *   bundle })` from HeaderCards.tsx for every `HEADER_CARD_DEFS` key in constants.ts, when both exports exist (none = no detail body).
 *   A closed native <details> is in the markup and counts as part of the header.
 * Render: round15/checks/_load.cjs with the REAL DataTooltip (so the tooltip's header and rows are visible text); HeaderBrief and
 *   TimelinePanel (AV-zg-1's files) are empty markers; hooks return the fixtures below.
 * Inputs: round15/fixtures/r15c.overlay.BA_US_Equity.json (the round-14 SERVED /overlay capture of BA: PX_LAST 196.8 USD,
 *   CUR_MKT_CAP 155544819936 USD, CURR_ENTP_VAL 187187.819936 MILLIONS USD, NET_DEBT 26965 MILLIONS USD, EQY_BETA, VOLUME_AVG_30D,
 *   SI_PERCENT_EQUITY_FLOAT; vintage 2026-09-30T12:39:47Z; source bloomberg-dapi) with display_name "The Boeing Company"; NO-NET-DEBT =
 *   the same minus NET_DEBT; NONE = the same minus every key-figure mnemonic (and VOLATILITY_30D, SHORT_INT_RATIO).
 * Arms:
 *   1  ONCE (SAUX-03): over the header plus every detail body, each of the seven key figures shows exactly once.
 *   2  TOOLTIP (SAUX-04): each key figure's tooltip text carries a formatted value equal to the served value at its printed precision,
 *      "Bloomberg" in words, no unformatted number (a digit run of 5+ without grouping, or 3+ decimals), not the served source id,
 *      no UPPER_SNAKE code; the served value rides `data-full-value` verbatim on the tooltip (FWD-13's carrier, never the face).
 *      CONTROL line (issuer ruling, round 29; passes at base by design): StatTile.tsx still exports FigureTooltip (1 parameter,
 *      renders [role=tooltip][data-mnemonic] carrying `attrs`), formatStatValue (4 parameters: value, format, currency, unit;
 *      returns a string) and figureTooltipRows (1 parameter; returns { label, value } string rows) -- tabs/ModelTab.tsx (AV-zg-5)
 *      imports all three. formatStatValue's OUTPUT may change for the money rule; its name and signature may not.
 *   3  WORDS (SAUX-30, 31, 33, 34): (a) 0 "Back to universe", 0 "rich text", 0 ".md" over the header, the detail bodies and
 *      PrintExportAction; [data-header-action="back"] renders with words; PrintExportAction still renders 2 labelled buttons;
 *      (b) on BA (USD) and 6501 (JPY, round15/fixtures/r15c.overlay.6501_JP_Equity.json): 0 "$" in the visible text; each money
 *      figure's face text reads "<its served currency code> <number>" ("USD 196.80", "JPY 5465"), never a fixed "USD";
 *      (c) on both, the market-cap face text carries its served vintage date in words (September 30th, 2026);
 *      (d) full and NO-NET-DEBT renders: 0 "not in the data yet" / "not carried"; NO-NET-DEBT shows no "Net debt" at all;
 *      (e) NONE: exactly one [data-key-figures], holding exactly one designed empty state (`data-stub="PanelEmpty"` or
 *      `data-stub="EmptyState"` from the estate, or [data-empty-state]) and no figure line.
 *   4  PLANTED: the arm 1-3 predicates reject a figure shown twice, '187187.819936', 'bloomberg-dapi', '$196.80', a market cap with
 *      no date, a 'Net debt is not in the data yet' line, "Back to universe", a NONE panel of empty lines, a StatTile module
 *      missing formatStatValue and one whose formatStatValue lost its unit parameter; they accept a correct synthetic set.
 * Prints one line per arm and "THE KEY FIGURES READ ONCE, FORMATTED, DATED, IN READER WORDS: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const h = L.React.createElement;
const readFix = (p) => { const x = JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8')); return x && x.payload && (x._capture_note || x._capture) ? x.payload : x; };

// ---- the HTML tree (same parser as face.cjs) -------------------------------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null, start: -1 };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[0].startsWith('<!--')) continue;
    if (m[5] !== undefined) { cur.children.push({ text: decode(m[5]), parent: cur }); continue; }
    const tag = m[2].toLowerCase();
    if (m[1]) { let n = cur; while (n && n.tag !== tag) n = n.parent; if (n && n.parent) cur = n.parent; continue; }
    const attrs = {};
    const ar = /([^\s=]+)(?:="([^"]*)")?/g;
    let a;
    while ((a = ar.exec(m[3])) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
    const node = { tag, attrs, children: [], parent: cur, start: m.index };
    cur.children.push(node);
    if (!m[4] && !VOID.has(tag)) cur = node;
  }
  return root;
}
function elements(node, out = []) { for (const c of node.children || []) if (c.tag) { out.push(c); elements(c, out); } return out; }
function textNodes(node, out = [], skip = null) { for (const c of node.children || []) { if (c.tag) { if (!skip || !skip(c)) textNodes(c, out, skip); } else out.push(c); } return out; }
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const textOf = (node, skip) => norm(textNodes(node, [], skip).map((t) => t.text).join(' '));
const has = (n, attr, val) => n.attrs && Object.prototype.hasOwnProperty.call(n.attrs, attr) && (val === undefined || n.attrs[attr] === val);

// ---- the key figures --------------------------------------------------------------------------------------------------------
const KEY = [
  { key: 'price', mn: ['PX_LAST'], money: true },
  { key: 'market cap', mn: ['CUR_MKT_CAP'], money: true },
  { key: 'enterprise value', mn: ['CURR_ENTP_VAL'], money: true },
  { key: 'net debt', mn: ['NET_DEBT'], money: true },
  { key: 'beta', mn: ['EQY_BETA'] },
  { key: 'average volume', mn: ['VOLUME_AVG_30D'] },
  { key: 'short interest', mn: ['SI_PERCENT_EQUITY_FLOAT', 'SHORT_INT_RATIO'] },
];
const ALL_MN = KEY.flatMap((k) => k.mn);

/** Every shown key figure over a list of HTML surfaces: { mn, face, tip, fullValue, where }. */
function figuresOf(surfaces) {
  const out = [];
  for (const [where, html] of surfaces) {
    for (const n of elements(parse(html))) {
      if (!(n.attrs.role === 'tooltip' && ALL_MN.includes(n.attrs['data-mnemonic']))) continue;
      const parent = n.parent;
      out.push({ mn: n.attrs['data-mnemonic'], where, tip: textOf(n), fullValue: n.attrs['data-full-value'],
        face: parent ? textOf(parent, (c) => c.attrs && c.attrs.role === 'tooltip') : '' });
    }
  }
  return out;
}
function onceFaults(figs) {
  const f = [];
  const counts = [];
  for (const k of KEY) {
    const n = figs.filter((x) => k.mn.includes(x.mn)).length;
    counts.push(`${k.key} ${n}`);
    if (n !== 1) f.push(`${k.key} shows ${n} time(s)${n > 1 ? ' (' + figs.filter((x) => k.mn.includes(x.mn)).map((x) => x.where).join(', ') + ')' : ''}`);
  }
  return { f, counts };
}

// A number token: optional grouping, optional decimals, optional magnitude suffix, optional percent.
const NUM = /(-?\d{1,3}(?:,\d{3})+|-?\d+)(?:\.(\d+))?\s*(T|B|M|K|bn|mm)?\b(\s*%)?/g;
const MULT = { T: 1e12, B: 1e9, bn: 1e9, M: 1e6, mm: 1e6, K: 1e3 };
const UNFORMATTED = /(?<![\d,.])(\d{5,}(?:\.\d+)?|\d+\.\d{3,})(?![\d,])/;
const CODE = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
function servedAbs(fig) { const v = Number(fig.value); return /^MILLIONS/i.test(String(fig.unit || '')) ? v * 1e6 : v; }
function formattedMatch(text, fig) {
  const want = servedAbs(fig);
  let m;
  NUM.lastIndex = 0;
  while ((m = NUM.exec(text)) !== null) {
    const n = Number(m[1].replace(/,/g, '') + (m[2] ? '.' + m[2] : ''));
    const dec = (m[2] || '').length;
    const mult = m[3] ? MULT[m[3]] : 1;
    const tol = 0.5000001 * Math.pow(10, -dec) * mult + 1e-9;
    if (Math.abs(n * mult - want) <= tol) return m[0];
  }
  return null;
}
function tipFaults(fig, served) {
  const f = [];
  const t = fig.tip;
  const u = UNFORMATTED.exec(t);
  if (u) f.push(`UNFORMATTED: "${u[0]}"`);
  if (!formattedMatch(t, served)) f.push(`FORMATTED: no formatted value equal to the served ${served.value} (${served.unit})`);
  if (!/\bBloomberg\b/.test(t)) f.push('SOURCE: "Bloomberg" is not said in words');
  if (served.source && served.source !== 'Bloomberg' && t.toLowerCase().includes(String(served.source).toLowerCase())) f.push(`SOURCE-ID: "${served.source}" on the face`);
  const c = CODE.exec(t);
  if (c) f.push(`CODE: "${c[0]}"`);
  if (fig.fullValue !== String(served.value)) f.push(`CARRIER: data-full-value is "${fig.fullValue}", not the served ${String(served.value)}`);
  return f;
}

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function vintageWords(vintage) {
  const days = new Set([String(vintage).slice(0, 10)]);
  const d = new Date(vintage);
  if (!Number.isNaN(d.getTime())) days.add(new Date(d.getTime() - 4 * 3600 * 1000).toISOString().slice(0, 10)); // ET (EDT) date
  return Array.from(days).map((iso) => { const [y, mo, dd] = iso.split('-').map(Number); return new RegExp(`\\b(${MONTHS[mo - 1]}|${MONTHS[mo - 1].slice(0, 3)}) ${dd}(st|nd|rd|th)?,? ${y}\\b`); });
}
/** Arm 3 (b)(c) on the shown figures. */
function moneyDateFaults(figs, ov) {
  const f = [];
  for (const x of figs) {
    const k = KEY.find((kk) => kk.mn.includes(x.mn));
    const served = (ov.header_figures || []).find((g) => g.mnemonic === x.mn) || {};
    if (k && k.money) {
      const code = served.currency;
      if (code && !new RegExp(`\\b${code}\\s+-?\\d`).test(x.face)) f.push(`MONEY: ${k.key} reads "${x.face.slice(0, 60)}", not "${code} <figure>"`);
      if (/\$/.test(x.face)) f.push(`MONEY: ${k.key} prints "$"`);
    }
    if (x.mn === 'CUR_MKT_CAP' && served.vintage && !vintageWords(served.vintage).some((re) => re.test(x.face))) f.push(`AS-OF: market cap reads "${x.face.slice(0, 60)}" with no as-of date beside it`);
  }
  return f;
}
const NO_LINE = /not in the data yet|not carried/i;

/** CONTROL (issuer ruling, round 29): StatTile.tsx's FigureTooltip, formatStatValue and figureTooltipRows are imported by
 * tabs/ModelTab.tsx (AV-zg-5); their names and signatures do not change (formatStatValue's OUTPUT may change for the money rule). */
function exportFaults(st) {
  const c = [];
  for (const [name, arity] of [['FigureTooltip', 1], ['formatStatValue', 4], ['figureTooltipRows', 1]]) {
    if (!st || typeof st[name] !== 'function') c.push(`${name} is not exported`);
    else if (st[name].length !== arity) c.push(`${name} takes ${st[name].length} parameter(s), not ${arity}`);
  }
  if (c.length) return c;
  try {
    const fig = { mnemonic: 'CURR_ENTP_VAL', value: 187187.819936, unit: 'MILLIONS', basis: { definition: 'Current enterprise value.' }, vintage: '2026-09-30T12:39:47Z', source: 'bloomberg-dapi' };
    if (typeof st.formatStatValue(fig.value, 'currency-millions', 'USD', fig.unit) !== 'string') c.push('formatStatValue(value, format, currency, unit) does not return a string');
    const rows = st.figureTooltipRows(fig);
    if (!Array.isArray(rows) || !rows.length || rows.some((r) => typeof r.label !== 'string' || typeof r.value !== 'string')) c.push('figureTooltipRows(figure) does not return { label, value } string rows');
    const th = L.render(st.FigureTooltip, { mnemonic: 'CURR_ENTP_VAL', label: 'Enterprise value', rows: [{ label: 'later', value: '1' }], attrs: { 'data-full-from': '1' } });
    if (!/role="tooltip"/.test(th) || !/data-mnemonic="CURR_ENTP_VAL"/.test(th) || !/data-full-from="1"/.test(th)) c.push('FigureTooltip({ mnemonic, label, rows, attrs }) no longer renders [role=tooltip][data-mnemonic] carrying the attrs');
  } catch (e) { c.push('a call threw: ' + String(e.message).split('\n')[0]); }
  return c;
}

// ---- stubs + fixtures -----------------------------------------------------------------------------------------------------
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);
L.stubSource('@tanstack/react-query', { __esModule: true,
  useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }) });
let setupError = null;
try {
  L.stubSource('src/components/DataTooltip.tsx', L.source('src/components/DataTooltip.tsx'));
  L.stubSource(SA + 'components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: () => h('div', { 'data-check-stub': 'TimelinePanel' }) });
  const realBrief = L.source(SA + 'components/HeaderBrief.tsx');
  L.stubSource(SA + 'components/HeaderBrief.tsx', Object.assign({}, realBrief, { HeaderBrief: () => h('div', { 'data-check-stub': 'HeaderBrief' }) }));
} catch (e) { setupError = 'STUB SETUP: ' + String(e.message).split('\n')[0]; }

const BA = Object.assign({}, readFix('round15/fixtures/r15c.overlay.BA_US_Equity.json'), { display_name: 'The Boeing Company', display_name_source: 'crosswalk' });
const NO_ND = Object.assign({}, BA, { header_figures: BA.header_figures.filter((g) => g.mnemonic !== 'NET_DEBT') });
const NONE = Object.assign({}, BA, { header_figures: BA.header_figures.filter((g) => !ALL_MN.includes(g.mnemonic) && g.mnemonic !== 'VOLATILITY_30D') });
const J6501 = readFix('round15/fixtures/r15c.overlay.6501_JP_Equity.json');
L.hookState.impl = { useThesisBundle: () => undefined, useCollectedChatter: () => undefined, usePeerSet: () => undefined, useManagement: () => undefined };

const safe = (fn) => { try { return fn(); } catch (e) { return `<p data-render-failed="1">RENDER FAILED ${String(e.message).split('\n')[0].replace(/</g, '&lt;')}</p>`; } };
function surfaces(ov) {
  const out = [['header', safe(() => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} }); })]];
  let hc = {};
  let defs = null;
  try { hc = L.source(SA + 'components/HeaderCards.tsx'); } catch (e) { hc = {}; }
  try { defs = L.source(SA + 'constants.ts').HEADER_CARD_DEFS; } catch (e) { defs = null; }
  if (typeof hc.HeaderCardDetail === 'function' && Array.isArray(defs)) {
    for (const c of defs) out.push([`detail:${c.key}`, safe(() => L.render(hc.HeaderCardDetail, { cardKey: c.key, bundle: ov }))]);
  }
  return out;
}
const failedAny = (ss) => ss.filter(([, html]) => /data-render-failed/.test(html)).map(([w, html]) => `${w}: ${textOf(parse(html)).slice(0, 90)}`);
const fullText = (ss) => ss.map(([, html]) => textOf(parse(html))).join(' ');

const arms = [];
const S_BA = surfaces(BA);
const FIGS = figuresOf(S_BA);
// ---- arm 1 -----------------------------------------------------------------------------------------------------------------
{
  const f = [];
  if (setupError) f.push(setupError);
  f.push(...failedAny(S_BA));
  const { f: of, counts } = onceFaults(FIGS);
  f.push(...of);
  arms.push(['ONCE: over the header and every detail body, each of the seven key figures shows exactly once (SAUX-03)', f.length === 0,
    (f.length === 0 ? '' : `${f.length} fault(s): ${f.join(' | ')} :: `) + `census ${counts.join(', ')} over ${S_BA.length} surface(s)`]);
}
// ---- arm 2 -----------------------------------------------------------------------------------------------------------------
{
  const f = [];
  let n = 0;
  for (const x of FIGS) {
    const served = (BA.header_figures || []).find((g) => g.mnemonic === x.mn);
    if (!served) continue;
    n += 1;
    for (const e of tipFaults(x, served)) f.push(`${x.mn}@${x.where} ${e}`);
  }
  if (n === 0) f.push('no key-figure tooltip rendered');
  // CONTROL (issuer ruling, round 29): StatTile.tsx's FigureTooltip, formatStatValue and figureTooltipRows are imported by
  // tabs/ModelTab.tsx (AV-zg-5); their names and signatures do not change (formatStatValue's OUTPUT may, for the money rule).
  let ctl = [];
  try { ctl = exportFaults(L.source(SA + 'components/StatTile.tsx')); } catch (e) { ctl.push('StatTile.tsx LOAD: ' + String(e.message).split('\n')[0]); }
  f.push(...ctl.map((x) => `CONTROL-EXPORTS: ${x}`));
  const classes = Array.from(new Set(f.map((x) => (/ ([A-Z-]+):/.exec(x) || /^([A-Z-]+):/.exec(x) || [])[1]).filter(Boolean)));
  arms.push(['TOOLTIP: formatted value, "Bloomberg" in words, no raw number, no source id, the served value carried in data-full-value (SAUX-04); CONTROL: StatTile.tsx exports FigureTooltip / formatStatValue / figureTooltipRows unchanged', f.length === 0,
    (f.length === 0 ? `${n} tooltip(s) clean` : `${f.length} fault(s) over ${n} tooltip(s), classes ${classes.join('/')}; first: ${f.slice(0, 3).join(' | ')}`) +
    ` :: control ${ctl.length === 0 ? 'OK (3 of 3 exports, arity 1/4/1, call shapes hold)' : 'FAIL ' + ctl.join('; ')}`]);
}
// ---- arm 3 -----------------------------------------------------------------------------------------------------------------
{
  const f = [];
  // (a) SAUX-30
  let pea = '';
  try { pea = L.render(L.source(SA + 'components/PrintExportAction.tsx').PrintExportAction, { securityKey: 'BA_US_Equity' }); } catch (e) { f.push('PrintExportAction RENDER: ' + String(e.message).split('\n')[0]); }
  const words = `${fullText(S_BA)} ${textOf(parse(pea))}`;
  for (const [name, re] of [['"Back to universe"', /back to universe/i], ['"rich text"', /rich text/i], ['".md"', /\.md\b/i]]) if (re.test(words)) f.push(`WORDS: ${name} renders`);
  const back = elements(parse(S_BA[0][1])).filter((n) => n.attrs['data-header-action'] === 'back');
  if (back.length !== 1 || !textOf(back[0])) f.push(`WORDS: ${back.length} [data-header-action="back"] control(s) with words (want 1)`);
  const buttons = elements(parse(pea)).filter((n) => n.tag === 'button' && textOf(n));
  if (buttons.length !== 2) f.push(`WORDS: PrintExportAction renders ${buttons.length} labelled button(s) (want 2)`);
  // (b)(c) SAUX-33, SAUX-34 -- BA (USD) and 6501 (JPY: the code is the served one, never a fixed "USD")
  for (const [name, ov, ss] of [['BA', BA, S_BA], ['6501', J6501, surfaces(J6501)]]) {
    f.push(...failedAny(ss).map((x) => `${name} ${x}`));
    if (/\$/.test(fullText(ss))) f.push(`MONEY (${name}): a "$" in the header text`);
    f.push(...moneyDateFaults(figuresOf(ss), ov).map((x) => `${x} (${name})`));
  }
  // (d) SAUX-31 lines
  for (const [name, ov, ss] of [['full', BA, S_BA], ['no-net-debt', NO_ND, surfaces(NO_ND)]]) {
    const t = fullText(ss);
    const hit = NO_LINE.exec(t);
    if (hit) f.push(`LINE (${name}): "${t.slice(Math.max(0, hit.index - 40), hit.index + 30)}"`);
    if (name === 'no-net-debt' && /net debt/i.test(t)) f.push('LINE (no-net-debt): "Net debt" still prints for a figure with no source');
  }
  // (e) SAUX-31 empty panel
  const sn = surfaces(NONE);
  const tn = fullText(sn);
  if (NO_LINE.test(tn)) f.push(`EMPTY: a no-source line renders in NONE ("${(NO_LINE.exec(tn) || [''])[0]}")`);
  const kf = elements(parse(sn[0][1])).filter((n) => has(n, 'data-key-figures'));
  if (kf.length !== 1) f.push(`EMPTY: ${kf.length} [data-key-figures] in NONE (want exactly 1)`);
  else {
    const empties = elements(kf[0]).filter((n) => n.attrs['data-stub'] === 'PanelEmpty' || n.attrs['data-stub'] === 'EmptyState' || has(n, 'data-empty-state'));
    if (empties.length !== 1) f.push(`EMPTY: ${empties.length} designed empty state(s) in the NONE key figures (want exactly 1)`);
    if (figuresOf([['none', sn[0][1]]]).length) f.push('EMPTY: a figure renders in NONE');
  }
  arms.push(['WORDS: no "Back to universe" / "Export rich text (.md)", one money format, market cap dated, no no-source line, one designed empty state (SAUX-30, 31, 33, 34)', f.length === 0,
    f.length === 0 ? 'back + 2 export buttons in reader words; served code on every money figure (USD / JPY), 0 "$"; market cap dated on both; 0 no-source lines; NONE = 1 empty state' : `${f.length} fault(s): ${f.slice(0, 6).join(' | ')}`]);
}
// ---- arm 4 (PLANTED) -------------------------------------------------------------------------------------------------------
{
  const f = [];
  const caught = [];
  const ev = BA.header_figures.find((g) => g.mnemonic === 'CURR_ENTP_VAL');
  const mc = BA.header_figures.find((g) => g.mnemonic === 'CUR_MKT_CAP');
  const tip = (mn, full, body) => `<div role="tooltip" data-mnemonic="${mn}" data-full-value="${full}">${body}</div>`;
  const goodEv = `<li><span>Enterprise value</span><span>USD 187B</span>${tip('CURR_ENTP_VAL', ev.value, '<div>Enterprise value</div><div>USD 187.19B, as of September 30th, 2026; source: Bloomberg</div>')}</li>`;
  const goodMc = `<li><span>Market cap</span><span>USD 156B</span><span>as of September 30th, 2026</span>${tip('CUR_MKT_CAP', mc.value, '<div>Market cap</div><div>USD 155.54B; source: Bloomberg</div>')}</li>`;
  const g = figuresOf([['planted', `<ul>${goodEv}${goodMc}</ul>`]]);
  const gEv = g.find((x) => x.mn === 'CURR_ENTP_VAL');
  if (!gEv || tipFaults(gEv, ev).length) f.push(`a correct tooltip is rejected: ${gEv ? tipFaults(gEv, ev)[0] : 'not found'}`);
  if (moneyDateFaults(g, BA).length) f.push(`a correct money/date face is rejected: ${moneyDateFaults(g, BA)[0]}`);
  const T = [
    ['187187.819936 in the tooltip', goodEv.replace('USD 187.19B,', '187187.819936,'), /UNFORMATTED/],
    ['bloomberg-dapi in the tooltip', goodEv.replace('source: Bloomberg', 'source: bloomberg-dapi'), /SOURCE/],
  ];
  for (const [n, html, want] of T) { const x = figuresOf([['p', html]])[0]; if (x && tipFaults(x, ev).some((e) => want.test(e))) caught.push(n); else f.push(`"${n}" not rejected`); }
  const D = [
    ['$196.80', `<li><span>Price</span><span>$196.80</span>${tip('PX_LAST', '196.8', '<div>USD 196.80; source: Bloomberg</div>')}</li>`, /MONEY/],
    ['a market cap with no date', goodMc.replace('<span>as of September 30th, 2026</span>', ''), /AS-OF/],
  ];
  for (const [n, html, want] of D) { if (moneyDateFaults(figuresOf([['p', html]]), BA).some((e) => want.test(e))) caught.push(n); else f.push(`"${n}" not rejected`); }
  const dup = figuresOf([['face', goodEv], ['detail', goodEv]]);
  if (onceFaults(dup).f.some((e) => /enterprise value shows 2/.test(e))) caught.push('a figure shown twice'); else f.push('"a figure shown twice" not rejected');
  if (NO_LINE.test('Net debt Net debt is not in the data yet')) caught.push('a no-source line'); else f.push('"a no-source line" not rejected');
  if (/back to universe/i.test('Back to universe Refresh')) caught.push('"Back to universe"'); else f.push('"Back to universe" not rejected');
  const fourLines = '<div data-key-figures=""><div>Price is not in the data yet</div><div>Enterprise value and net debt are not in the data yet</div></div>';
  const kfp = elements(parse(fourLines)).find((n) => has(n, 'data-key-figures'));
  const emp = elements(kfp).filter((n) => n.attrs['data-stub'] === 'PanelEmpty' || has(n, 'data-empty-state')).length;
  if (emp !== 1 && NO_LINE.test(textOf(kfp))) caught.push('an empty panel of lines'); else f.push('"an empty panel of lines" not rejected');
  const oneEmpty = '<div data-key-figures=""><div data-stub="PanelEmpty"><span>No key figures are available for this name yet.</span></div></div>';
  const kfo = elements(parse(oneEmpty)).find((n) => has(n, 'data-key-figures'));
  if (elements(kfo).filter((n) => n.attrs['data-stub'] === 'PanelEmpty').length !== 1 || NO_LINE.test(textOf(kfo))) f.push('a correct designed empty state is rejected');
  // The export control: the checkout's own StatTile module passes; a module missing formatStatValue, and one whose
  // formatStatValue dropped its unit parameter, are rejected.
  try {
    const st = L.source(SA + 'components/StatTile.tsx');
    const okNow = exportFaults(st);
    const noFmt = Object.assign({}, st); delete noFmt.formatStatValue;
    const shrunk = Object.assign({}, st, { formatStatValue: (value, format, currency) => String(value) + format + currency });
    if (exportFaults(noFmt).some((e) => /formatStatValue is not exported/.test(e))) caught.push('a missing export'); else f.push('"a missing export" not rejected');
    if (exportFaults(shrunk).some((e) => /takes 3 parameter/.test(e))) caught.push('a changed signature'); else f.push('"a changed signature" not rejected');
    if (okNow.length && !/is not exported|parameter/.test(okNow[0])) f.push(`the export control rejects the module for another reason: ${okNow[0]}`);
  } catch (e) { f.push('export plant: ' + String(e.message).split('\n')[0]); }
  arms.push(['PLANTED: a raw number, a source id, "$", an undated market cap, a duplicate, a no-source line, "Back to universe", an empty panel of lines, a missing StatTile export and a changed signature are rejected; correct faces pass', f.length === 0,
    f.length === 0 ? `${caught.length} of 10 plants rejected; correct tooltip, money/date face and empty state accepted` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE KEY FIGURES READ ONCE, FORMATTED, DATED, IN READER WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
