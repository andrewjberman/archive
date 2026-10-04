/**
 * payload35.cjs -- DSGN_AMGTV1 round 35 (issuer 2.0.0_SA_COO~D): NO SYSTEM WORD ON THE FACE.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-92): node <this file>
 *   A worker runs it from its worktree root: cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/
 *   deliverables/2.0.0_SA_COO~D/round35/checks/words/payload35.cjs". Fixtures resolve from this file's own location; the portal
 *   resolves from the cwd (cwd/portal).
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see round15/checks/_load.cjs) is honoured for every source read here (renders AND the
 *   census), and the KEEP checks are spawned with the same env. A worker never sets it.
 * Why: the page's designed empty-state sentences print the system word "payload" to a PM. At portal 055ba370:
 *   GenerationCaption.tsx:35 "generation: not carried on this payload"; LeadPanel.tsx:302 and SecurityOverlay.tsx:193 "Posture: not
 *   carried on this payload."; SecurityOverlay.tsx:427 "sector/country not carried on this payload"; StatTile.tsx:172 "not carried
 *   on this payload"; ExecManagementTab.tsx:376 "<The research team on management>: not carried on this payload.", :410 and
 *   ThesisTab.tsx:163 "Source: the report is not named on this payload", :455 "Exec Management: not carried on this payload.";
 *   PostureTab.tsx:513 "Posture: not carried on this payload.", :564 "Fund of record and last stated position: not carried on this
 *   payload."; ThesisTab.tsx:113 "<The research team's thesis pillars>: not carried on this payload.". The repair says each in
 *   plain words of the form "<the missing thing> is not in this security's data"; the exact wording is the worker's.
 * Render: round15/checks/_load.cjs (the REAL page sources, page hooks stubbed per hook). Each surface is driven into its empty
 *   state by a minimal plant on the served BA bundle (round35/fixtures/thesis.BA_US_Equity.json; for the identity header,
 *   round15/fixtures/r15c.overlay.BA_US_Equity.json, with TimelinePanel and HeaderBrief drawn as markers as round34 repairs34.cjs
 *   does). THE SENTENCE of a surface is read from the element its own hook names (wording-free):
 *     GEN            GenerationCaption with fields {ranking_status: SERVED} (no generation_id key): its data-generation-detail value
 *                    (the line generationCaptionText returns; at the base it reaches no visible text, only this attribute)
 *     LEAD_POSTURE   LeadPanel PostureHeaderLine, posture null: [data-header-posture="NOT_READ"]
 *     HEADER_POSTURE IdentityHeader, bundle.posture removed: [data-header-posture="NOT_READ"]
 *     HEADER_SECTOR  IdentityHeader, GICS_SECTOR_NAME and CNTRY_OF_DOMICILE removed: the element carrying data-identity-currency
 *     STAT_TILE      each StatTile of constants STAT_TILE_DEFS with no figure: [data-stat-state="ABSENT"] less its first <span> (the label)
 *     EXEC_MGMT      ExecManagementTab, dossier_fields removed: [data-dossier-management="NOT_CARRIED"]
 *     EXEC_SOURCE    ExecManagementTab, dossier management SERVED with a citation naming no report_key: the last <p> of
 *                    [data-dossier-management="SERVED"]
 *     EXEC_NOT_READ  ExecManagementTab, management removed: [data-exec-status="NOT_READ"]
 *     POSTURE_TAB    PostureTab, posture removed: [data-posture-status="NOT_READ"]
 *     POSTURE_FUND   PostureTab, dossier_fields removed: [data-dossier-position="NOT_CARRIED"]
 *     THESIS_PILLARS ThesisTab, dossier_fields removed: [data-dossier-pillars="NOT_CARRIED"]
 *     THESIS_SOURCE  ThesisTab, one served pillar whose citation names no report_key: the last <p> of [data-dossier-pillar="1"]
 *   NAMES ITS MISSING THING (case-insensitive, word-bounded): GEN "generation"; *_POSTURE / POSTURE_TAB "posture"; HEADER_SECTOR
 *   "sector" and "country"; STAT_TILE the tile's own label; EXEC_MGMT and EXEC_NOT_READ "management"; *_SOURCE "source" and
 *   "report"; POSTURE_FUND "fund" and "position"; THESIS_PILLARS "pillar(s)". An empty sentence names nothing.
 * CENSUS (arm 2): every .ts/.tsx under portal/src/pages/SecurityAnalysis/ except __harness__/ and __rendercheck__/ (and .d.ts),
 *   parsed with the INSTALLED typescript (ts.createSourceFile, the scanner's tokens as AST nodes; comments and identifiers are not
 *   nodes of the graded kinds): StringLiteral, NoSubstitutionTemplateLiteral, TemplateHead / Middle / Tail and JsxText whose text
 *   matches /payload/i. NOT GRADED, printed: a string literal that is the direct value of a data-* JSX attribute (a machine hook,
 *   never visible text; at 055ba370 RankedChart.tsx:156 data-completeness-state="NO_PAYLOAD").
 * Arms:
 *   1  RENDERED: on each of the 12 surfaces (18 renders: STAT_TILE once per STAT_TILE_DEFS entry, 7 at 055ba370) the visible text
 *      of the render and the sentence hold 0 /payload/i, and the sentence names its missing thing; graded per render, each
 *      sentence printed on a "  SENTENCE" line before the arm lines.
 *   2  CENSUS: 0 graded literals or JSX text nodes match /payload/i; each hit printed file:line.
 *   3  KEEP: round32 repairs/words32.cjs, round34 repairs/repairs34.cjs and round29 header/face.cjs exit 0 on the same tree.
 *   4  PLANTED: the sentence grader flags a sentence carrying "payload", an empty sentence and a sentence that names nothing, and
 *      accepts "Posture is not in this security's data."; the census grader flags a JSX text, a string literal and a template tail
 *      carrying "payload" and passes a comment, an identifier and a data-* attribute value.
 * Blind spots: one empty state per surface (a sentence reached only through another state is not rendered here, though the census
 *   still sees its literal); a sentence computed at run time from served text is not in the census; "names its missing thing" is a
 *   word test, not a meaning test.
 * Prints one line per arm and "NO SYSTEM WORD ON THE FACE: <k> of 4 arms"; exit 0 only at 4 of 4. Static renders only; no network,
 * no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { createRequire } = require('module');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const FXDIR = path.join(__dirname, '..', '..', 'fixtures');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const ts = createRequire(path.join(L.base, 'package.json'))('typescript');
const h = L.React.createElement;
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const norm = (s) => String(s === null || s === undefined ? '' : s).replace(/\s+/g, ' ').trim();
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const clone = (x) => JSON.parse(JSON.stringify(x));
const dec = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const OVR = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) { const i = pair.indexOf('='); OVR[pair.slice(0, i)] = pair.slice(i + 1); }

const THESIS = pay(JSON.parse(fs.readFileSync(path.join(FXDIR, 'thesis.BA_US_Equity.json'), 'utf8')));
const OVERLAY = pay(JSON.parse(fs.readFileSync(path.join(DROOT, 'round15', 'fixtures', 'r15c.overlay.BA_US_Equity.json'), 'utf8')));
const PAYLOAD = /payload/i;

// ---- graders (pure; arm 4 feeds them planted input) -----------------------------------------------------------------------
/** One surface: its sentence and its visible text against its naming rules. */
function sentenceFaults(sentence, visibleText, names) {
  const f = [];
  const s = norm(sentence);
  if (PAYLOAD.test(s)) f.push(`the sentence "${s}" says "${s.match(PAYLOAD)[0]}"`);
  if (visibleText !== null && visibleText !== undefined && PAYLOAD.test(visibleText)) {
    const t = norm(visibleText);
    const at = t.search(PAYLOAD);
    f.push(`the visible text says "${t.slice(Math.max(0, at - 40), at + 10)}"`);
  }
  if (!s) f.push('the sentence is empty');
  else {
    const missing = names.filter((n) => !n.re.test(s)).map((n) => n.word);
    if (missing.length) f.push(`the sentence "${s}" does not name ${missing.map((w) => `"${w}"`).join(' and ')}`);
  }
  return f;
}
const W = (word, re) => ({ word, re: re || new RegExp(`\\b${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i') });

/** The census of one source text: graded hits and excluded data-* attribute values. */
function censusOf(text, file) {
  const sf = ts.createSourceFile(file, text, ts.ScriptTarget.Latest, true, /x$/.test(file) ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
  const K = ts.SyntaxKind;
  const KINDS = new Set([K.StringLiteral, K.NoSubstitutionTemplateLiteral, K.TemplateHead, K.TemplateMiddle, K.TemplateTail, K.JsxText]);
  const hits = [];
  const excluded = [];
  (function visit(node) {
    if (KINDS.has(node.kind) && PAYLOAD.test(node.text)) {
      const line = sf.getLineAndCharacterOfPosition(node.getStart(sf)).line + 1;
      const rec = { file, line, kind: K[node.kind], text: norm(node.text).slice(0, 90) };
      const p = node.parent;
      if (node.kind === K.StringLiteral && p && p.kind === K.JsxAttribute && /^data-/.test(p.name.getText(sf))) excluded.push(rec);
      else hits.push(rec);
    }
    ts.forEachChild(node, visit);
  })(sf);
  return { hits, excluded };
}

// ---- the renders --------------------------------------------------------------------------------------------------------
let setupError = null;
try {
  L.stubSource(SA + 'components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: () => h('div', { 'data-check-stub': 'TimelinePanel' }) });
  const realBrief = L.source(SA + 'components/HeaderBrief.tsx');
  L.stubSource(SA + 'components/HeaderBrief.tsx', Object.assign({}, realBrief, { HeaderBrief: () => h('div', { 'data-check-stub': 'HeaderBrief' }) }));
} catch (e) { setupError = 'STUB SETUP: ' + first(e); }

const bundleHooks = (bundle) => {
  L.hookState.data = undefined;
  L.hookState.impl = { useThesisBundle: () => bundle, usePeerSet: () => undefined, useCollectedChatter: () => undefined, useManagement: () => undefined };
};
const header = (ov) => {
  bundleHooks(undefined);
  const m = L.source(SA + 'components/SecurityOverlay.tsx');
  return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} });
};
const tab = (file, exp, bundle) => { bundleHooks(bundle); return L.render(L.source(SA + file)[exp], { securityKey: 'BA_US_Equity' }); };
const without = (obj, ...keys) => { const x = clone(obj); for (const k of keys) delete x[k]; return x; };
/** The visible text of the first element carrying attr="value" (or attr= when value is undefined); null when none renders. */
const elementText = (html, attr, value) => { const x = L.innerOf(html, attr, value); return x === null ? null : L.textOf(x); };
const lastP = (inner) => { if (inner === null) return null; const ps = [...inner.matchAll(/<p\b[^>]*>([\s\S]*?)<\/p>/g)]; return ps.length ? L.textOf(ps[ps.length - 1][1]) : null; };

function surfaces() {
  const out = [];
  const add = (id, at, names, fn) => out.push({ id, at, names, fn });
  add('GEN', 'GenerationCaption.tsx:35', [W('generation')], () => {
    const html = L.render(L.source(SA + 'components/GenerationCaption.tsx').GenerationCaption, { fields: { ranking_status: 'SERVED' } });
    const m = /\sdata-generation-detail="([^"]*)"/.exec(html);
    return { html, sentence: m ? dec(m[1]) : null };
  });
  add('LEAD_POSTURE', 'LeadPanel.tsx:302', [W('posture')], () => {
    const html = L.render(L.source(SA + 'components/LeadPanel.tsx').PostureHeaderLine, { posture: null, subjectIdentity: THESIS.identity });
    return { html, sentence: elementText(html, 'data-header-posture', 'NOT_READ') };
  });
  add('HEADER_POSTURE', 'SecurityOverlay.tsx:193', [W('posture')], () => {
    const html = header(without(OVERLAY, 'posture'));
    return { html, sentence: elementText(html, 'data-header-posture', 'NOT_READ') };
  });
  add('HEADER_SECTOR', 'SecurityOverlay.tsx:427', [W('sector'), W('country')], () => {
    const ov = clone(OVERLAY);
    ov.header_figures = (ov.header_figures || []).filter((f) => f.mnemonic !== 'GICS_SECTOR_NAME' && f.mnemonic !== 'CNTRY_OF_DOMICILE');
    const html = header(ov);
    return { html, sentence: elementText(html, 'data-identity-currency') };
  });
  const C = L.source(SA + 'constants.ts');
  for (const def of C.STAT_TILE_DEFS) {
    add(`STAT_TILE ${def.label}`, 'StatTile.tsx:172', [W(def.label, new RegExp(def.label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'))], () => {
      const html = L.render(L.source(SA + 'components/StatTile.tsx').StatTile, { mnemonic: def.mnemonic, label: def.label, format: def.format, figure: undefined, currency: 'USD' });
      const tile = L.innerOf(html, 'data-stat-state', 'ABSENT');
      return { html, sentence: tile === null ? null : L.textOf(tile.replace(/<span\b[^>]*>[\s\S]*?<\/span>/, ' ')) };
    });
  }
  add('EXEC_MGMT', 'ExecManagementTab.tsx:376', [W('management')], () => {
    const html = tab('tabs/ExecManagementTab.tsx', 'ExecManagementTab', without(THESIS, 'dossier_fields'));
    return { html, sentence: elementText(html, 'data-dossier-management', 'NOT_CARRIED') };
  });
  add('EXEC_SOURCE', 'ExecManagementTab.tsx:410', [W('source'), W('report')], () => {
    const b = clone(THESIS);
    b.dossier_fields = Object.assign({}, b.dossier_fields, { management: { status: 'SERVED', value: 'PLANTED management passage for the empty-source state.', reason: null, citation: { locator: 'p. 1' } } });
    const html = tab('tabs/ExecManagementTab.tsx', 'ExecManagementTab', b);
    return { html, sentence: lastP(L.innerOf(html, 'data-dossier-management', 'SERVED')) };
  });
  add('EXEC_NOT_READ', 'ExecManagementTab.tsx:455', [W('management')], () => {
    const html = tab('tabs/ExecManagementTab.tsx', 'ExecManagementTab', without(THESIS, 'management'));
    return { html, sentence: elementText(html, 'data-exec-status', 'NOT_READ') };
  });
  add('POSTURE_TAB', 'PostureTab.tsx:513', [W('posture')], () => {
    const html = tab('tabs/PostureTab.tsx', 'PostureTab', without(THESIS, 'posture'));
    return { html, sentence: elementText(html, 'data-posture-status', 'NOT_READ') };
  });
  add('POSTURE_FUND', 'PostureTab.tsx:564', [W('fund'), W('position')], () => {
    const html = tab('tabs/PostureTab.tsx', 'PostureTab', without(THESIS, 'dossier_fields'));
    return { html, sentence: elementText(html, 'data-dossier-position', 'NOT_CARRIED') };
  });
  add('THESIS_PILLARS', 'ThesisTab.tsx:113', [W('pillars', /\bpillars?\b/i)], () => {
    const html = tab('tabs/ThesisTab.tsx', 'ThesisTab', without(THESIS, 'dossier_fields'));
    return { html, sentence: elementText(html, 'data-dossier-pillars', 'NOT_CARRIED') };
  });
  add('THESIS_SOURCE', 'ThesisTab.tsx:163', [W('source'), W('report')], () => {
    const b = clone(THESIS);
    b.dossier_fields = Object.assign({}, b.dossier_fields, { thesis_pillars: [{ pillar: 'PLANTED pillar', text: 'PLANTED pillar text for the empty-source state.', terms: [], citation: { locator: 'p. 2' } }] });
    const html = tab('tabs/ThesisTab.tsx', 'ThesisTab', b);
    return { html, sentence: lastP(L.innerOf(html, 'data-dossier-pillar', '1')) };
  });
  return out;
}

const arms = [];
// ---- arm 1 ----
{
  const f = [];
  const read = [];
  let list = [];
  if (setupError) f.push(setupError);
  try { list = surfaces(); } catch (e) { f.push('SURFACES: ' + first(e)); }
  let clean = 0;
  for (const s of list) {
    let r;
    try { r = s.fn(); } catch (e) { f.push(`${s.id} (${s.at}): RENDER ${first(e)}`); continue; }
    if (r.sentence === null) { f.push(`${s.id} (${s.at}): the empty-state element is not rendered`); continue; }
    const x = sentenceFaults(r.sentence, L.textOf(r.html), s.names);
    if (x.length) f.push(...x.map((y) => `${s.id} (${s.at}): ${y}`));
    else clean += 1;
    read.push(`${s.id} "${norm(r.sentence)}"`);
  }
  for (const line of read) console.log(`  SENTENCE ${line}`);
  arms.push([`RENDERED: each designed empty state (${list.length} surfaces) prints no "payload" and its sentence names its missing thing`, f.length === 0,
    f.length ? `${clean} of ${list.length} surfaces clean; ${f.length} fault(s): ${f.join(' | ')}` : `${clean} of ${list.length} surfaces clean`]);
}
// ---- arm 2 ----
{
  const f = [];
  const root = path.join(L.base, SA);
  const files = [];
  (function walk(dir, rel) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.isDirectory()) { if (e.name !== '__harness__' && e.name !== '__rendercheck__') walk(path.join(dir, e.name), rel + e.name + '/'); }
      else if (/\.tsx?$/.test(e.name) && !/\.d\.ts$/.test(e.name)) files.push(rel + e.name);
    }
  })(root, '');
  const hits = [];
  const excluded = [];
  for (const rel of files) {
    const portalRel = SA + rel;
    const text = fs.readFileSync(OVR[portalRel] || path.join(root, rel), 'utf8');
    const c = censusOf(text, rel);
    hits.push(...c.hits);
    excluded.push(...c.excluded);
  }
  for (const x of hits) f.push(`${x.file}:${x.line} ${x.kind} "${x.text}"`);
  const ex = excluded.map((x) => `${x.file}:${x.line} "${x.text}"`).join('; ');
  arms.push(['CENSUS: 0 string literals or JSX text nodes under SecurityAnalysis (harness and rendercheck excluded) say "payload"', f.length === 0,
    `${hits.length} graded hit(s) across ${files.length} files${f.length ? ': ' + f.join(' | ') : ''}; not graded (data-* attribute values): ${excluded.length}${ex ? ' (' + ex + ')' : ''}`]);
}
// ---- arm 3 ----
{
  const KEEP = ['round32/checks/repairs/words32.cjs', 'round34/checks/repairs/repairs34.cjs', 'round29/checks/header/face.cjs'];
  const f = [];
  for (const rel of KEEP) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 900000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) f.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  arms.push(['KEEP: round32 words32.cjs, round34 repairs34.cjs and round29 face.cjs exit 0 on the same tree', f.length === 0,
    f.length ? f.join(' | ') : `${KEEP.length} of ${KEEP.length} exit 0`]);
}
// ---- arm 4: PLANTED ----
{
  const f = [];
  const posture = [W('posture')];
  const flagged = (name, faults, why) => { if (!faults.some((x) => why.test(x))) f.push(`"${name}" not flagged for its reason (${faults[0] || 'accepted'})`); };
  flagged('a sentence carrying "payload"', sentenceFaults('Posture: not carried on this payload.', 'Posture: not carried on this payload.', posture), /says "payload"/);
  flagged('an empty sentence', sentenceFaults('', '', posture), /the sentence is empty/);
  flagged('a sentence that names nothing', sentenceFaults("Not in this security's data.", "Not in this security's data.", posture), /does not name "posture"/);
  flagged('"payload" elsewhere on the face', sentenceFaults("Posture is not in this security's data.", "Posture is not in this security's data. Read from the payload.", posture), /the visible text says/);
  const good = sentenceFaults("Posture is not in this security's data.", "Posture is not in this security's data.", posture);
  if (good.length) f.push(`a good sentence rejected: ${good[0]}`);
  const src = [
    '// a comment that says payload',
    'const payloadShape = 1',
    "const a = 'Source: the report is not named on this payload'",
    'const b = `${HEADING}: not carried on this payload.`',
    'export const T = () => <div data-completeness-state="NO_PAYLOAD"><p>Posture: not carried on this payload.</p></div>',
  ].join('\n');
  const c = censusOf(src, 'planted.tsx');
  const kinds = c.hits.map((x) => x.kind).sort().join(',');
  if (c.hits.length !== 3 || !/JsxText/.test(kinds) || !/StringLiteral/.test(kinds) || !/(TemplateTail|LastTemplateToken)/.test(kinds)) f.push(`census flagged ${c.hits.length} of 3 planted literals (${kinds || 'none'})`);
  if (c.hits.some((x) => x.line === 1 || x.line === 2)) f.push('census flagged a comment or an identifier');
  if (c.excluded.length !== 1 || c.excluded[0].line !== 5) f.push(`census did not set the data-* attribute value aside (${c.excluded.length})`);
  arms.push(['PLANTED: the sentence grader flags "payload", an empty sentence, a sentence naming nothing and "payload" elsewhere on the face; the census flags JSX text, a string and a template carrying "payload" and passes a comment, an identifier and a data-* value', f.length === 0,
    f.length ? f.join(' | ') : '4 of 4 sentence plants flagged, 1 good sentence accepted; census 3 of 3 flagged, comment and identifier passed, 1 data-* value set aside']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`NO SYSTEM WORD ON THE FACE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
