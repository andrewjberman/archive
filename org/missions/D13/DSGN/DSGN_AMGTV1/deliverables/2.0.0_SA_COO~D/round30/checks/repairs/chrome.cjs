/**
 * chrome.cjs -- DSGN_AMGTV1 round 30, AV-zh-2 REPAIRS, check 1 of 2 (issuer 2.0.0_SA_COO~D): THE PAGE WEARS THE ESTATE'S OWN
 * TOKENS AND CONTROLS.
 *
 * Usage: cd <dir whose portal/ is the checkout under test> && node <this file>
 *   (e.g. cd C:/tmp/wk-dsgn-amgtv1-82). Static renders and source reads only; no network, no AWS, writes no file.
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see round15/checks/_load.cjs) is honoured for every source read here.
 * Grades:
 *   FWD-23 (prd/DSGN_AMGTV1_PRD.md ~347-353; CTO msg 28820): "its colours come from lib/chartColors.ts (0 hard-coded hex in the
 *     panel's chart files)" -- components/ChatterBubbles.tsx:75 holds NO_TONE_FILL = '#cbd5e1' (the no-tone bubble fill and the
 *     legend swatch at ~:537). The ramp colours reach the file through lib/sentimentColor.ts and are not graded here.
 *   Row DSGN_AMGTV1-Z-W81-S1: SecurityOverlay.tsx's Refresh is buttonClass('primary', 'canvas', 'sm', 'text-[hsl(0_0%_100%)]'),
 *     its white ink re-spelled so the round-29 face.cjs would not read it as white-on-white (face.cjs is amended in place this
 *     round to judge a primary's ink against its own fill). The repair restores the canonical estate class (PRD FWD-18: Refresh
 *     stays the ONE purple fill).
 *   Row DSGN_AMGTV1-Z-W81-S3 / SAUX-30: __rendercheck__/renderCheck.tsx:439 still reads the Security-mode header by the retired
 *     words 'Back to universe'; the back control is [data-header-action="back"] reading "Back to all names".
 * Render: round15/checks/_load.cjs (the real page sources) with the round-29 face.cjs stubs: the REAL Panel, buttonClass
 *   (Controls.tsx), GraphicCard and DataTooltip; HeaderBrief and TimelinePanel as markers. ChatterBubbles renders as tone.cjs does.
 * Inputs: round29/fixtures/collage/r29c.chatter.toned.json (17 names collected in 2026-09: 14 toned, 1 tone null, 2 no tone
 *   field); round15/fixtures/r15c.overlay.BA_US_Equity.json (the served BA overlay); round30/fixtures/repairs/
 *   chartColors.base.exports.json (the BASE e370eb7c census of lib/chartColors.ts, built by r30r.build.cjs).
 * Arms:
 *   1  NO-TONE TOKEN (FWD-23): ChatterBubbles.tsx holds 0 colour literals in code (hex #rgb/#rrggbb/#rrggbbaa, or rgb()/hsl() with
 *      numeric channels, in any string, template or JSX text; comments are not code) and imports from lib/chartColors;
 *      lib/chartColors.ts keeps all 44 BASE exports (none removed, none changing kind) and holds the no-tone token
 *      CHATTER_NO_TONE_FILL; every no-tone bubble's fill is that token's value, and the tone legend carries the same value as its
 *      no-tone swatch; and the round-29
 *      ISSUER AMENDMENT 1 (round 31, 2026-10-03): this arm graded "BASE exports value-identical + exactly ONE new export". That
 *      was the round-30 cell's own diff, graded 4/4 at its drain (@8b73dd0f5b). On a later candidate merged with remote DEV,
 *      other projects' landed edits are legitimate (DSGN_REBRND's PALETTE.pink400 and getAssetClassInkOnDark). So a BASE value
 *      changed by other work is now a printed NOTE, not a fault. A removed BASE export, a changed kind, or a missing token is
 *      still a fault.
 *      collage checks over the same file still exit 0 (round29/checks/collage/tone.cjs, collage.cjs -- battery29.sh runs neither).
 *   2  CANONICAL PRIMARY (Z-W81-S1): the loaded header's [data-header-action="refresh"] wears buttonClass('primary', 'canvas',
 *      'sm' | 'md') -- every token of it, and no other paint token (text-/bg-/border-/fill-/stroke-, variant prefixes ignored);
 *      SecurityOverlay.tsx spells no white ink by value (hsl(0 0% 100%) in any separator, or text-[#fff | #ffffff | white |
 *      rgb(255 255 255)]) anywhere in the file; and the round-29 header checks still exit 0 (round29/checks/header/face.cjs as
 *      AMENDED this round, figures.cjs).
 *   3  BACK CONTROL (Z-W81-S3): renderCheck.tsx's own readRoute(), lifted from the source and run here, reads
 *      persistentPanelPresent TRUE on the live loaded header, FALSE on the same header with its data-header-action="back" hook
 *      removed, FALSE on a page reading only the words "Back to universe", and TRUE on a Universe page reading "Lead Panel"
 *      (control); no string literal in renderCheck.tsx reads "Back to universe"; the live header renders exactly one
 *      [data-header-action="back"] whose text is "Back to all names" (control).
 *   4  PLANTED: each predicate rejects its known-bad inputs and accepts a known-good one (colour literal x5 / clean source;
 *      chartColors census x3 / two good (AMENDMENT 1: token added; token + other landed work); no-tone fill x2 / matching; primary class x2 / canonical x2; readRoute x2 /
 *      hook-based).
 * Prints one line per arm and "THE PAGE WEARS THE ESTATE'S OWN TOKENS AND CONTROLS: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { createRequire } = require('module');

const SA = 'src/pages/SecurityAnalysis/';
const CB = SA + 'components/ChatterBubbles.tsx';
const CC = 'src/lib/chartColors.ts';
const SO = SA + 'components/SecurityOverlay.tsx';
const RC = SA + '__rendercheck__/renderCheck.tsx';
const DROOT = path.join(__dirname, '..', '..', '..');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const h = L.React.createElement;
const ts = createRequire(path.join(L.base, 'package.json'))('typescript');
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8'));
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const OVR = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) { const i = pair.indexOf('='); OVR[pair.slice(0, i)] = pair.slice(i + 1); }
const srcText = (rel) => { const f = OVR[rel] || path.join(L.base, rel); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8').replace(/\r\n/g, '\n') : null; };
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex');
const decode = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
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

// ---- predicates ----------------------------------------------------------------------------------------------------------
const HEX = /#(?:[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{3,4})(?![0-9a-z])/i;
const NUMERIC_COLOUR = /\b(?:rgba?|hsla?)\(\s*-?[\d.]/i;
/** Every colour literal in CODE: string literals, template parts and JSX text (comments are trivia and never read). */
function colourLiterals(src) {
  const sf = ts.createSourceFile('x.tsx', src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TSX);
  const hits = [];
  const K = ts.SyntaxKind;
  const visit = (n) => {
    let t = null;
    if (ts.isStringLiteral(n) || ts.isNoSubstitutionTemplateLiteral(n) || n.kind === K.TemplateHead || n.kind === K.TemplateMiddle || n.kind === K.TemplateTail || ts.isJsxText(n)) t = n.text;
    if (t !== null) {
      const m = HEX.exec(t) || NUMERIC_COLOUR.exec(t);
      if (m) hits.push(`line ${sf.getLineAndCharacterOfPosition(n.getStart(sf)).line + 1} "${m[0]}"`);
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
  return hits;
}
const IMPORTS_CHART_COLORS = /^import\s*\{[^}]+\}\s*from\s*['"](?:@\/lib\/chartColors|(?:\.\.\/)+lib\/chartColors)['"]/m;

/** The top-level export census of a chartColors.ts text: kind + sha256 (r30r.build.cjs computes the BASE one the same way). */
function exportCensus(text, mod) {
  const sf = ts.createSourceFile('chartColors.ts', text, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  const out = {};
  const exported = (n) => (n.modifiers || []).some((m) => m.kind === ts.SyntaxKind.ExportKeyword);
  const collapse = (s) => s.replace(/\s+/g, ' ').trim();
  for (const st of sf.statements) {
    if (!exported(st)) continue;
    if (ts.isFunctionDeclaration(st) && st.name) out[st.name.text] = { kind: 'function', sha256: sha(collapse(st.getText(sf))) };
    else if (ts.isVariableStatement(st)) {
      for (const d of st.declarationList.declarations) {
        const name = d.name.getText(sf);
        const v = mod ? mod[name] : undefined;
        out[name] = typeof v === 'function' ? { kind: 'function', sha256: sha(collapse(d.getText(sf))) } : { kind: 'value', sha256: sha(JSON.stringify(v)) };
      }
    }
  }
  return out;
}
const NO_TONE_TOKEN = 'CHATTER_NO_TONE_FILL';
/** AMENDMENT 1: no BASE export removed or changing kind, and the no-tone token present. A BASE value changed by other landed work
 * is listed in `changedElsewhere` (a note, not a fault). Returns { faults, added, changedElsewhere }. */
function censusFaults(base, cand) {
  const f = [];
  const removed = Object.keys(base).filter((k) => !cand[k]);
  const rekinded = Object.keys(base).filter((k) => cand[k] && cand[k].kind !== base[k].kind);
  const changedElsewhere = Object.keys(base).filter((k) => cand[k] && cand[k].kind === base[k].kind && cand[k].sha256 !== base[k].sha256);
  const added = Object.keys(cand).filter((k) => !base[k]);
  if (removed.length) f.push(`CHARTCOLORS: ${removed.length} BASE export(s) removed (${removed.slice(0, 4).join(', ')})`);
  if (rekinded.length) f.push(`CHARTCOLORS: ${rekinded.length} BASE export(s) changed kind (${rekinded.slice(0, 4).join(', ')})`);
  if (!added.includes(NO_TONE_TOKEN)) f.push(`CHARTCOLORS: no ${NO_TONE_TOKEN} export (new exports: ${added.join(', ') || 'none'})`);
  return { faults: f, added, changedElsewhere };
}
const leaves = (v, out = []) => { if (typeof v === 'string') out.push(v.toLowerCase()); else if (v && typeof v === 'object') Object.values(v).forEach((x) => leaves(x, out)); return out; };
/** The no-tone bubbles' fill is the new token's value, and the legend carries it. */
function fillFaults(noToneFills, legendHtml, tokenValue) {
  const f = [];
  const want = leaves(tokenValue);
  if (!noToneFills.length) return ['FILL: no no-tone bubble rendered'];
  const fills = [...new Set(noToneFills.map((x) => String(x || '').toLowerCase()))];
  if (fills.length !== 1) f.push(`FILL: ${fills.length} different no-tone fills (${fills.join(', ')})`);
  for (const x of fills) if (!want.includes(x)) f.push(`FILL: the no-tone fill "${x}" is not the new chartColors token's value (${want.join(', ') || 'no string value'})`);
  if (legendHtml === null) f.push('LEGEND: no [data-tone-legend]');
  else if (fills.length === 1 && !decode(legendHtml).toLowerCase().includes(fills[0])) f.push(`LEGEND: the no-tone swatch does not carry ${fills[0]}`);
  return f;
}

const PAINT = /^(text|bg|border|fill|stroke)-/;
const toks = (cls) => String(cls || '').split(/\s+/).filter(Boolean);
/** The Refresh button's class is the canonical primary for one size, with no other paint token. */
function primaryFaults(cls, canonBySize) {
  const have = toks(cls);
  const bare = (t) => t.split(':').pop();
  const verdicts = Object.entries(canonBySize).map(([size, canon]) => {
    const want = toks(canon);
    const missing = want.filter((t) => !have.includes(t));
    const extra = have.filter((t) => !want.includes(t) && PAINT.test(bare(t)));
    return { size, missing, extra };
  });
  if (verdicts.some((v) => !v.missing.length && !v.extra.length)) return [];
  const v = verdicts[0];
  return [`REFRESH: class is not buttonClass('primary', 'canvas', '${v.size}') -- missing [${v.missing.join(' ')}], extra paint [${v.extra.join(' ')}]`];
}
const WHITE_SPELLING = /hsla?\(\s*0(?:deg)?[\s_,]+0%[\s_,]+100%|text-\[(?:color:)?(?:#fff(?:fff)?(?:[0-9a-f]{2})?|white|rgba?\(\s*255[\s_,]+255[\s_,]+255)/i;

/** Lift readRoute (and the file's top-level string/regex constants) out of renderCheck.tsx and run it here. */
function liftReadRoute(src) {
  const sf = ts.createSourceFile('renderCheck.tsx', src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TSX);
  const consts = [];
  let fn = null;
  const lit = (e) => e && (ts.isStringLiteral(e) || ts.isNoSubstitutionTemplateLiteral(e) || ts.isRegularExpressionLiteral(e));
  for (const st of sf.statements) {
    if (ts.isFunctionDeclaration(st) && st.name && st.name.text === 'readRoute') fn = st;
    else if (ts.isVariableStatement(st) && st.declarationList.declarations.every((d) => lit(d.initializer))) consts.push(st.getText(sf).replace(/^export\s+/, ''));
  }
  if (!fn) throw new Error('renderCheck.tsx declares no top-level function readRoute');
  const code = consts.join('\n') + '\n' + fn.getText(sf).replace(/^export\s+/, '') + '\nmodule.exports = readRoute;\n';
  const js = ts.transpileModule(code, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 } }).outputText;
  const mod = { exports: {} };
  new Function('module', 'exports', js)(mod, mod.exports);
  return mod.exports;
}
const SEC_PATH = '/security-analysis/BA_US_Equity';
const UNI_PATH = '/security-analysis';
const STALE_ONLY = '<div><h2>The Boeing Co</h2><button type="button">Back to universe</button><div>Thesis</div></div>';
const UNIVERSE = '<section><h2>Lead Panel</h2><div>Thesis</div></section>';
/** readRoute's persistentPanelPresent on the four pages (arm 3), given the live loaded header markup. */
function readRouteFaults(readRoute, liveHtml) {
  const f = [];
  const pp = (p, html) => { const r = readRoute(p, html); return r && r.persistentPanelPresent; };
  const noHook = liveHtml.split('data-header-action="back"').join('');
  if (pp(SEC_PATH, liveHtml) !== true) f.push('READROUTE: persistentPanelPresent is not true on the live header (its back control is [data-header-action="back"])');
  if (pp(SEC_PATH, noHook) !== false) f.push('READROUTE: persistentPanelPresent is true on the header with the back hook removed (it reads words, not the control)');
  if (pp(SEC_PATH, STALE_ONLY) !== false) f.push('READROUTE: persistentPanelPresent is true on a page reading only "Back to universe" (the retired words)');
  if (pp(UNI_PATH, UNIVERSE) !== true) f.push('READROUTE CONTROL: persistentPanelPresent is not true on a Universe page reading "Lead Panel"');
  return f;
}
function stringLiterals(src) {
  const sf = ts.createSourceFile('x.tsx', src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TSX);
  const out = [];
  const K = ts.SyntaxKind;
  const visit = (n) => {
    if (ts.isStringLiteral(n) || ts.isNoSubstitutionTemplateLiteral(n) || n.kind === K.TemplateHead || n.kind === K.TemplateMiddle || n.kind === K.TemplateTail || ts.isJsxText(n)) out.push(n.text);
    ts.forEachChild(n, visit);
  };
  visit(sf);
  return out;
}

// ---- stubs (round29 face.cjs) + renders ------------------------------------------------------------------------------------
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);
L.stubSource('@tanstack/react-query', { __esModule: true,
  useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }) });
let setupError = null;
let Controls = null;
try {
  Controls = L.source('src/ui/components/Controls.tsx');
  L.stubSource('src/ui/components/Controls.tsx', Controls);
  const realPanel = L.source('src/ui/components/panels/Panel.tsx').Panel;
  const stubCache = {};
  const panels = new Proxy({}, { get(_t, k) {
    if (k === '__esModule') return true;
    if (k === 'Panel') return realPanel;
    if (typeof k !== 'string') return undefined;
    if (!stubCache[k]) { const C = (p) => h('div', { 'data-stub': k }, (p || {}).children); C.displayName = k; stubCache[k] = C; }
    return stubCache[k];
  } });
  for (const k of ['src/ui/components/panels/index.ts', 'src/ui/components/panels']) L.stubSource(k, panels);
  L.stubSource('src/ui/components/graphic/GraphicCard.tsx', L.source('src/ui/components/graphic/GraphicCard.tsx'));
  L.stubSource('src/components/DataTooltip.tsx', L.source('src/components/DataTooltip.tsx'));
  L.stubSource(SA + 'components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: (p) => h('div', { 'data-check-stub': 'TimelinePanel', 'data-security-key': (p || {}).securityKey || '' }) });
  const realBrief = L.source(SA + 'components/HeaderBrief.tsx');
  L.stubSource(SA + 'components/HeaderBrief.tsx', Object.assign({}, realBrief, { HeaderBrief: () => h('div', { 'data-check-stub': 'HeaderBrief' }) }));
} catch (e) { setupError = 'STUB SETUP: ' + first(e); }
L.hookState.impl = { useThesisBundle: () => undefined, useCollectedChatter: () => undefined, usePeerSet: () => undefined, useManagement: () => undefined };
const BA = Object.assign({}, unwrap(readJson('round15/fixtures/r15c.overlay.BA_US_Equity.json')), { display_name: 'The Boeing Company', display_name_source: 'crosswalk' });
let headerHtml = '';
let headerErr = setupError;
if (!headerErr) {
  try { const m = L.source(SO); headerHtml = L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: BA, onBack: () => {}, onRefresh: () => {} }); } catch (e) { headerErr = 'HEADER RENDER: ' + first(e); }
}
/** The opening tag of the (first) element carrying attr="value"; null if none. */
function openTag(html, attr, value) {
  const at = html.indexOf(`${attr}="${value}"`);
  if (at < 0) return null;
  const s = html.lastIndexOf('<', at);
  return html.slice(s, html.indexOf('>', at) + 1);
}
const classOf = (tag) => { const m = /\sclass="([^"]*)"/.exec(tag || ''); return m ? decode(m[1]) : ''; };
const canon = () => ({ sm: Controls.buttonClass('primary', 'canvas', 'sm'), md: Controls.buttonClass('primary', 'canvas', 'md') });

const MONTH = '2026-09';
const TONED = ((x) => (x && x.payload ? x.payload : x))(readJson('round29/fixtures/collage/r29c.chatter.toned.json')); // tone.cjs's unwrap
function chatterModel() {
  const html = L.render(L.source(CB).ChatterBubbles, { data: TONED, month: MONTH, onMonthChange: () => {}, onSelectSecurity: () => {} });
  const fills = [];
  for (const r of TONED.rows) {
    const e = r.by_month[MONTH];
    if (!e || !(e.collected > 0) || (typeof r.tone === 'number' && Number.isFinite(r.tone))) continue;
    const tag = openTag(html, 'data-bubble', r.security_key);
    fills.push(tag ? ((/\sfill="([^"]*)"/.exec(tag) || [])[1] || '') : '');
  }
  return { fills, legendHtml: L.innerOf(html, 'data-tone-legend') };
}

const arms = [];
// ---- arm 1: NO-TONE TOKEN ----------------------------------------------------------------------------------------------------
{
  const f = [];
  let note = '';
  const cb = srcText(CB);
  const ccText = srcText(CC);
  if (cb === null) f.push('NO FILE: ChatterBubbles.tsx');
  else {
    const lits = colourLiterals(cb);
    if (lits.length) f.push(`HEX: ${lits.length} colour literal(s) in ChatterBubbles.tsx code (${lits.slice(0, 3).join('; ')})`);
    if (!IMPORTS_CHART_COLORS.test(cb)) f.push('IMPORT: ChatterBubbles.tsx imports nothing from lib/chartColors');
  }
  let added = [];
  let elsewhere = [];
  let ccMod = null;
  try { ccMod = L.source(CC); } catch (e) { f.push('CHARTCOLORS LOAD: ' + first(e)); }
  if (ccText !== null && ccMod) {
    const base = readJson('round30/fixtures/repairs/chartColors.base.exports.json').exports;
    const r = censusFaults(base, exportCensus(ccText, ccMod));
    f.push(...r.faults);
    added = r.added;
    elsewhere = r.changedElsewhere;
  }
  if (added.includes(NO_TONE_TOKEN) && ccMod) {
    try {
      const m = chatterModel();
      f.push(...fillFaults(m.fills, m.legendHtml, ccMod[NO_TONE_TOKEN]));
      note = `0 colour literals; chartColors 44 BASE exports kept (${elsewhere.length} value(s) changed by other landed work${elsewhere.length ? ': ' + elsewhere.join(', ') : ''}; other new exports: ${added.filter((k) => k !== NO_TONE_TOKEN).join(', ') || 'none'}) + "${NO_TONE_TOKEN}"; ${m.fills.length} no-tone bubbles and the legend swatch wear it`;
    } catch (e) { f.push('CHATTER RENDER: ' + first(e)); }
  }
  f.push(...keepsPassing(['round29/checks/collage/tone.cjs', 'round29/checks/collage/collage.cjs']));
  if (note) note += '; round-29 tone.cjs and collage.cjs exit 0';
  arms.push(['NO-TONE TOKEN: ChatterBubbles.tsx holds no hard-coded colour; its no-tone fill is ONE new lib/chartColors.ts token, the file otherwise unchanged (FWD-23)', f.length === 0,
    f.length === 0 ? note : `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}`]);
}
// ---- arm 2: CANONICAL PRIMARY ------------------------------------------------------------------------------------------------
{
  const f = [];
  let cls = '';
  if (headerErr) f.push(headerErr);
  else {
    const tag = openTag(headerHtml, 'data-header-action', 'refresh');
    if (!tag) f.push('REFRESH: no [data-header-action="refresh"] in the loaded header');
    else { cls = classOf(tag); f.push(...primaryFaults(cls, canon())); }
  }
  const so = srcText(SO) || '';
  const lines = so.split('\n').map((l, i) => [i + 1, l]).filter(([, l]) => WHITE_SPELLING.test(l));
  if (lines.length) f.push(`WHITE SPELLED BY VALUE: ${lines.length} line(s) of SecurityOverlay.tsx (line ${lines.map((x) => x[0]).join(', ')}: "${lines[0][1].trim().slice(0, 80)}")`);
  f.push(...keepsPassing(['round29/checks/header/face.cjs', 'round29/checks/header/figures.cjs']));
  arms.push(['CANONICAL PRIMARY: Refresh wears buttonClass(\'primary\', \'canvas\', size) and its own ink; SecurityOverlay.tsx spells no white by value (row Z-W81-S1)', f.length === 0,
    f.length === 0 ? `Refresh class = the canonical primary (${toks(cls).filter((t) => PAINT.test(t)).join(' ')}); 0 white spellings; round-29 face.cjs (amended) and figures.cjs exit 0` : `${f.length} fault(s): ${f.slice(0, 3).join(' | ')}`]);
}
// ---- arm 3: BACK CONTROL -----------------------------------------------------------------------------------------------------
{
  const f = [];
  const rc = srcText(RC);
  if (rc === null) f.push('NO FILE: __rendercheck__/renderCheck.tsx');
  else {
    if (headerErr) f.push(headerErr);
    else {
      try { f.push(...readRouteFaults(liftReadRoute(rc), headerHtml)); } catch (e) { f.push('READROUTE: ' + first(e)); }
      const backs = (headerHtml.match(/data-header-action="back"/g) || []).length;
      const backText = backs ? L.textOf(L.innerOf(headerHtml, 'data-header-action', 'back') || '') : '';
      if (backs !== 1 || backText !== 'Back to all names') f.push(`CONTROL: the live header renders ${backs} [data-header-action="back"] reading "${backText}" (want 1 reading "Back to all names")`);
    }
    const stale = stringLiterals(rc).filter((s) => /Back to universe/i.test(s));
    if (stale.length) f.push(`STALE: ${stale.length} string literal(s) in renderCheck.tsx still read "Back to universe"`);
  }
  arms.push(['BACK CONTROL: renderCheck.tsx\'s readRoute reads the Security header by [data-header-action="back"], never by "Back to universe" (row Z-W81-S3, SAUX-30)', f.length === 0,
    f.length === 0 ? 'readRoute: live header true, hook removed false, "Back to universe" alone false, Lead Panel true; 0 stale literals; 1 back control "Back to all names"' : `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}`]);
}
// ---- arm 4: PLANTED ----------------------------------------------------------------------------------------------------------
{
  const f = [];
  let rejected = 0;
  let accepted = 0;
  let bad = 0;
  let good = 0;
  const rej = (name, faults) => { bad += 1; if (faults.length) rejected += 1; else f.push(`"${name}" accepted`); };
  const acc = (name, faults) => { good += 1; if (!faults.length) accepted += 1; else f.push(`"${name}" rejected: ${faults[0]}`); };
  // colour literals
  rej('a hex const', colourLiterals("const NO_TONE_FILL = '#cbd5e1'\n"));
  rej('an upper-case hex', colourLiterals('const X = "#CBD5E1"\n'));
  rej('a hex in a template', colourLiterals('const X = `${a} #fff`\n'));
  rej('a hex JSX attribute', colourLiterals('const C = () => <circle fill="#abc" />\n'));
  rej('a numeric rgb()', colourLiterals("const X = 'rgb(203, 213, 225)'\n"));
  acc('a clean source', colourLiterals("import { CHATTER_NO_TONE_FILL } from '../../../lib/chartColors'\n// was '#cbd5e1'\nconst INK = 'fill-[hsl(var(--palette-navy))]'\nconst C = () => <p>#4 in the ranks</p>\n"));
  // chartColors census
  const B = { A: { kind: 'value', sha256: 'a' }, F: { kind: 'function', sha256: 'f' } };
  const T = { [NO_TONE_TOKEN]: { kind: 'value', sha256: 't' } };
  rej('no token', censusFaults(B, { ...B }).faults);
  rej('a BASE export removed', censusFaults(B, { F: B.F, ...T }).faults);
  rej('a BASE export changing kind', censusFaults(B, { ...B, A: { kind: 'function', sha256: 'a' }, ...T }).faults);
  acc('the token added', censusFaults(B, { ...B, ...T }).faults);
  acc('the token + another landed export + a value changed elsewhere (AMENDMENT 1)', censusFaults(B, { ...B, A: { kind: 'value', sha256: 'a2' }, M: { kind: 'function', sha256: 'm' }, ...T }).faults);
  // no-tone fill
  const LEG = (x) => `<span>no clear tone</span><span style="background-color:${x}"></span>`;
  rej('a fill that is not the token', fillFaults(['#cbd5e1', '#cbd5e1'], LEG('#cbd5e1'), '#d1d5db'));
  rej('a legend without the swatch', fillFaults(['#d1d5db', '#d1d5db'], '<span>no clear tone</span>', '#d1d5db'));
  acc('the token on both bubbles and the legend', fillFaults(['#D1D5DB', '#d1d5db'], LEG('#d1d5db'), '#d1d5db'));
  // primary class
  if (Controls) {
    rej('the canonical primary with a white re-spelled', primaryFaults(Controls.buttonClass('primary', 'canvas', 'sm', 'text-[hsl(0_0%_100%)]'), canon()));
    rej('a secondary Refresh', primaryFaults(Controls.buttonClass('secondary', 'canvas', 'sm'), canon()));
    acc('the canonical primary sm', primaryFaults(Controls.buttonClass('primary', 'canvas', 'sm'), canon()));
    acc('the canonical primary sm plus a layout token', primaryFaults(Controls.buttonClass('primary', 'canvas', 'sm', 'ml-auto'), canon()));
    rej('a line spelling white as hsl(0_0%_100%)', WHITE_SPELLING.test("className={buttonClass('primary', 'canvas', 'sm', 'text-[hsl(0_0%_100%)]')}") ? ['caught'] : []);
    rej('a line spelling white as text-[#ffffff]', WHITE_SPELLING.test("className=\"text-[#ffffff]\"") ? ['caught'] : []);
    acc('the canonical call line', WHITE_SPELLING.test("className={buttonClass('primary', 'canvas', 'sm')}") ? ['caught'] : []);
  } else f.push('no Controls module to plant against');
  // readRoute
  const live = '<div><button data-header-action="back" class="x">Back to all names</button><button data-header-action="refresh">Refresh</button></div>';
  const fakeRoute = (body) => liftReadRoute(`const PRINT_BUTTON_MARKER = 'p'\nfunction readRoute(path: string, html: string) {\n  return { path, persistentPanelPresent: ${body} }\n}\n`);
  rej('readRoute on the retired words', readRouteFaults(fakeRoute("html.includes('Lead Panel') || html.includes('Back to universe')"), live));
  rej('readRoute on the new words only', readRouteFaults(fakeRoute("html.includes('Lead Panel') || html.includes('Back to all names')"), live));
  acc('readRoute on the back hook', readRouteFaults(fakeRoute("html.includes('Lead Panel') || html.includes('data-header-action=\"back\"')"), live));
  arms.push(['PLANTED: the colour-literal, chartColors-census, no-tone-fill, primary-class and readRoute predicates reject known-bad inputs and accept known-good ones', f.length === 0,
    f.length === 0 ? `${rejected} of ${bad} bad inputs rejected; ${accepted} of ${good} good inputs accepted` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE PAGE WEARS THE ESTATE'S OWN TOKENS AND CONTROLS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
