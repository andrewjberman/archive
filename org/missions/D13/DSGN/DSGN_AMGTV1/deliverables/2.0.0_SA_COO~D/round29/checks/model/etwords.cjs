/**
 * etwords.cjs -- DSGN_AMGTV1 round 29, AV-zg-5 MODEL (issuer 2.0.0_SA_COO~D): THE MODEL TAB READS IN ET AND IN READER WORDS.
 *
 * Usage (from the worktree root whose portal/ is the checkout under test):  node <this file>
 * Grades PRD v0.10 FWD-25 ("every version time prints in ET") and FWD-27 on the Model tab (prd/DSGN_AMGTV1_PRD.md ~363-402), with
 * the register rows (docs/briefs/amgt-security-analysis-ui-findings-20261002.json):
 *   SAUX-24 "Every time on the page prints in ET in one format." TODAY: "The version of October 2nd, 2026, 15:49 UTC".
 *   SAUX-26 "None of these sentences renders at rest; any that remains sits behind a details toggle in reader words." -- 'Showing
 *     <n> fiscal figures from the model block', 'No year-on-year growth rows: the model block serves none and this page computes
 *     none', '<n> versions have landed; a refresh adds a version and never overwrites an earlier one', 'Re-running one input on its
 *     own is not available on this page yet'.
 *   Issuer ruling (b) (decomposition v29): every time prints in ET through dateWords.ts (owned by AV-zg-5); other cells call its
 *     helpers and do not format times.
 * THE HOUSE ET FORM is the estate formatter's own (src/lib/dateUtils.ts formatPanelTimestamp, already behind dateWords.longStamp):
 *   "September 28th, 2026, 10:45p ET". A version stamp is served compact ("20260929T024521Z"); its ET day can differ from its UTC
 *   day. AT REST = the rendered HTML with every closed <details> body removed (its <summary> kept); text inside an `sr-only` span
 *   or an open <details> is at rest.
 * Inputs: round29/fixtures/model/served.BA_US_Equity.json (the portal's own served BA /thesis, /versions (16 stamps), /compare,
 *   /ledger, verbatim). PLANTED in memory (labelled): the /compare answer for every pair (the served 7 changed figures; the newest
 *   three versions identical, as whatchanged.cjs scenario B); arm 1 also plants the bundle's generated_at = 2026-10-02T02:30Z and the
 *   ledger's market-data run stamp = 20261002T020000Z -- both on UTC day October 2nd and ET day October 1st.
 * Arms:
 *   1  ET ON THE FACE: every <option> whose value is a served stamp carries that stamp's house ET label (16 of 16; 20260929T024521Z
 *      reads "September 28th, 2026, 10:45p ET"); every clock time in the Model tab's text is "<h>:<mm>[:<ss>]<a|p> ET"; no "UTC"
 *      and no raw stamp prints; the panel header's Updated day and the ledger's run day read the ET day (October 1st), never the
 *      UTC day (October 2nd); the ledger ([data-input-ledger]) is still in the tab's HTML.
 *   2  ONE FORMATTER: dateWords.ts exports a function that maps the served compact stamp to the house ET label (2 probes); its three
 *      existing helpers (longDate, longStamp, chartTick) answer as at the base (the other cells' contract); tabs/ModelTab.tsx and
 *      components/model/** (comments stripped) format no time themselves: no UTC, toISOString, getUTC*, Intl.DateTimeFormat,
 *      toLocaleDateString, toLocaleTimeString or timeZone.
 *   3  SYSTEM FACTS: none of the four sentences (or a light rewording of each) is at rest; none prints verbatim even behind a toggle;
 *      the sheet's data-model-fiscal-cells count still rides the tab (tabs.harness.cjs reads it).
 *   4  PLANTED: the arms' predicates accept good synthetic HTML and reject 7 mutants.
 * Prints one line per arm and "THE MODEL TAB READS IN ET AND IN READER WORDS: <k> of 4 arms"; exit 0 only at 4 of 4. Writes no file.
 */
const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const SA = 'src/pages/SecurityAnalysis/';
const D = path.join(__dirname, '..', '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const ts = createRequire(path.join(L.base, 'package.json'))('typescript');
const FX = JSON.parse(fs.readFileSync(path.join(D, 'round29', 'fixtures', 'model', 'served.BA_US_Equity.json'), 'utf8'));
const KEY = 'BA_US_Equity';
const STAMPS = FX.versions.versions.map((v) => v.stamp);
const CHANGED = FX.compare.compared.changed;
const clone = (x) => JSON.parse(JSON.stringify(x));

const DU = L.source('src/lib/dateUtils.ts');
const isoOf = (s) => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}T${s.slice(9, 11)}:${s.slice(11, 13)}:${s.slice(13, 15)}Z`;
const etLabel = (s) => DU.formatPanelTimestamp(isoOf(s));
const PROBES = [['20261002T154900Z', 'October 2nd, 2026, 11:49a ET'], ['20260929T024521Z', 'September 28th, 2026, 10:45p ET']];
if (!PROBES.every(([s, want]) => etLabel(s) === want)) {
  console.log(`INSTRUMENT ERROR: the estate ET formatter reads "${etLabel(PROBES[0][0])}" (want "${PROBES[0][1]}")`);
  process.exit(3);
}
const PLANT_GENERATED = '2026-10-02T02:30Z';
const PLANT_RUN = '20261002T020000Z';
const ET_DAY = 'October 1st, 2026';
const UTC_DAY = 'October 2nd, 2026';

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
      security_key: KEY, available_stamps: STAMPS.slice(), read: FX.compare.read, reason: null,
      denominators: { versions: STAMPS.length, figures_from: 179, figures_to: 179 + added, added, removed: 0, changed: changed.length, unchanged: 172 },
      compared: { from_stamp: from, to_stamp: to, added: FX.compare.compared.added.slice(0, added), removed: [], changed },
    };
  };
}
const NEWEST_THREE = (s) => (STAMPS.indexOf(s) >= STAMPS.length - 3 ? 'NEWEST-THREE' : s);

let MT = null;
let loadError = '';
try { MT = L.source(SA + 'tabs/ModelTab.tsx'); } catch (e) { loadError = String(e.message).split('\n')[0]; }
function renderTab(thesis, ledger) {
  L.hookState.impl = {
    useThesisBundle: () => thesis,
    useModelVersions: () => FX.versions,
    useModelCompare: compareFor(NEWEST_THREE),
    useInputLedger: () => ledger,
  };
  if (!MT) return { html: '', err: 'LOAD: ' + loadError };
  try { return { html: L.render(MT.ModelTab, { securityKey: KEY }), err: '' }; } catch (e) { return { html: '', err: 'RENDER: ' + String(e.message).split('\n')[0] }; }
}

// ---- predicates (pure over HTML; arm 4 feeds them planted HTML) ----------------------------------------------------------------
const dec = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (h) => L.textOf(h || '');

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

function etFaults(html) {
  const f = [];
  const all = text(html);
  if (/\bUTC\b/.test(all)) f.push(`"UTC" prints ("${(all.match(/.{0,40}\bUTC\b/) || [''])[0].trim()}")`);
  if (/\b\d{8}T\d{6}Z\b/.test(all)) f.push('a raw version stamp prints');
  const clocks = [...all.matchAll(/(?<![\d:])\d{1,2}:\d{2}(?::\d{2})?(?![\d:])/g)];
  const bad = clocks.filter((m) => !/^[ap] ET\b/.test(all.slice(m.index + m[0].length)));
  if (bad.length) f.push(`${bad.length} of ${clocks.length} clock times not in the house ET form (first "${all.slice(Math.max(0, bad[0].index - 22), bad[0].index + 10).trim()}")`);
  const opts = [...html.matchAll(/<option\b([^>]*)>([\s\S]*?)<\/option>/g)].map((m) => ({ value: dec((/\svalue="([^"]*)"/.exec(m[1]) || [])[1] || ''), label: text(m[2]) }));
  const served = opts.filter((o) => STAMPS.includes(o.value));
  const wrong = served.filter((o) => !o.label.includes(etLabel(o.value)));
  const offered = new Set(served.map((o) => o.value));
  if (offered.size < STAMPS.length) f.push(`${offered.size} of ${STAMPS.length} served versions are an option`);
  if (wrong.length) f.push(`${wrong.length} of ${served.length} version options lack the house ET label (first "${wrong[0].label}", want "${etLabel(wrong[0].value)}")`);
  const head = L.innerOf(html, 'data-model-panel-header');
  if (head === null) f.push('no [data-model-panel-header]');
  else {
    if (!text(head).includes(ET_DAY)) f.push(`the header's Updated day is not the ET day "${ET_DAY}" ("${text(head).slice(-40)}")`);
    if (text(head).includes(UTC_DAY)) f.push(`the header prints the UTC day "${UTC_DAY}"`);
  }
  const ledger = L.innerOf(html, 'data-input-ledger');
  if (ledger === null) f.push('no [data-input-ledger] in the tab (keep the ledger; a toggle may hide it)');
  else {
    if (!text(ledger).includes(ET_DAY)) f.push(`the ledger's run day is not the ET day "${ET_DAY}"`);
    if (text(ledger).includes(UTC_DAY)) f.push(`the ledger prints the UTC day "${UTC_DAY}"`);
  }
  return f;
}

const FACTS = [
  ['fiscal-figure count', [/Showing\s+\d[\d,]*\s+fiscal figures/i], /Showing \d[\d,]* fiscal figures from the model block/],
  ['no year-on-year rows', [/year-on-year growth rows/i, /this page computes none/i], /the model block serves none and this page computes none/],
  ['versions landed', [/versions?\s+(?:has|have)\s+landed/i, /never overwrites an earlier/i], /a refresh adds a version and never overwrites an earlier one/],
  ['re-running unavailable', [/Re-running one input/i], /Re-running one input on its own is not available on this page yet/],
];
function factFaults(html) {
  const f = [];
  const rest = text(atRest(html));
  const all = text(html);
  for (const [name, loose, verbatim] of FACTS) {
    const hit = loose.find((re) => re.test(rest));
    if (hit) f.push(`at rest: ${name} ("${rest.match(hit)[0]}")`);
    else if (verbatim.test(all)) f.push(`verbatim behind a toggle: ${name}`);
  }
  return f;
}

function sourceFaults() {
  const f = [];
  const files = [SA + 'tabs/ModelTab.tsx'];
  const walk = (rel) => {
    const abs = path.join(L.base, rel);
    if (!fs.existsSync(abs)) return;
    for (const e of fs.readdirSync(abs, { withFileTypes: true })) {
      if (e.isDirectory()) walk(rel + '/' + e.name);
      else if (/\.tsx?$/.test(e.name)) files.push(rel + '/' + e.name);
    }
  };
  walk(SA + 'components/model');
  const BANNED = /\bUTC\b|toISOString|getUTC[A-Za-z]*|Intl\s*\.\s*DateTimeFormat|toLocaleDateString|toLocaleTimeString|\btimeZone\b/;
  // ISSUER GREEN ARM ONLY: honour the loader's CHECK_SRC_OVERRIDE (a worker never sets it), so a scratch reference is read here too.
  const overrides = {};
  for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) overrides[pair.slice(0, pair.indexOf('='))] = pair.slice(pair.indexOf('=') + 1);
  for (const rel of files) {
    const src = fs.readFileSync(overrides[rel] || path.join(L.base, rel), 'utf8');
    const out = ts.transpileModule(src, { compilerOptions: { removeComments: true, jsx: ts.JsxEmit.Preserve, target: ts.ScriptTarget.ESNext } }).outputText;
    const m = out.match(BANNED);
    if (m) f.push(`${rel.replace(SA, '')} formats a time itself ("${m[0]}")`);
  }
  return { faults: f, files: files.length };
}

const arms = [];
// Arm 1 -- ET on the face.
{
  const thesis = { ...FX.thesis, generated_at: PLANT_GENERATED };
  const ledger = clone(FX.ledger);
  ledger.latest_by_class.market_data.stamp = PLANT_RUN;
  const r = renderTab(thesis, ledger);
  const f = r.err ? [r.err] : etFaults(r.html);
  arms.push(['ET ON THE FACE: every version option in the house ET form, every clock in ET, no UTC, the Updated and ledger days on the ET day', f.length === 0,
    f.length ? `${f.length} faults: ${f.slice(0, 4).join(' | ')}` : `${STAMPS.length} of ${STAMPS.length} options in ET (${etLabel(STAMPS[12])}); 0 UTC; header and ledger read ${ET_DAY}`]);
}
// Arm 2 -- one formatter.
{
  const f = [];
  let DW = null;
  let hitNames = [];
  try { DW = L.source(SA + 'dateWords.ts'); } catch (e) { f.push('LOAD dateWords.ts: ' + String(e.message).split('\n')[0]); }
  if (DW) {
    const fns = Object.entries(DW).filter(([, v]) => typeof v === 'function');
    const hits = fns.filter(([, fn]) => PROBES.every(([s, want]) => { try { return fn(s) === want; } catch (e) { return false; } }));
    if (hits.length === 0) f.push(`no dateWords export maps "${PROBES[0][0]}" to "${PROBES[0][1]}" (exports: ${fns.map(([n]) => n).join(', ')}; longStamp gives "${DW.longStamp ? DW.longStamp(PROBES[0][0]) : 'n/a'}")`);
    const KEEP = [['longDate', '2026-09-28', 'September 28th, 2026'], ['longStamp', '2026-09-28T22:47:00Z', 'September 28th, 2026, 6:47p ET'], ['longStamp', '2026-09-28', 'September 28th, 2026'], ['chartTick', '2026-09-28', '9/28']];
    for (const [name, input, want] of KEEP) {
      let got;
      try { got = typeof DW[name] === 'function' ? DW[name](input) : 'NOT EXPORTED'; } catch (e) { got = 'THREW'; }
      if (got !== want) f.push(`${name}("${input}") reads "${got}" (the base and the other cells read "${want}")`);
    }
    hitNames = hits.map(([n]) => n);
  }
  const s = sourceFaults();
  f.push(...s.faults);
  arms.push(['ONE FORMATTER: dateWords.ts maps the served stamp to the house ET label; its three helpers unchanged; the Model sources format no time themselves', f.length === 0,
    f.length ? `${f.length} faults: ${f.slice(0, 4).join(' | ')}` : `dateWords export(s) ${hitNames.join(', ')} give the ET label; longDate/longStamp/chartTick unchanged; ${s.files} Model source(s) clean`]);
}
// Arm 3 -- system facts.
{
  const r = renderTab(FX.thesis, FX.ledger);
  const f = r.err ? [r.err] : factFaults(r.html);
  if (!r.err) {
    const sheet = L.source(SA + 'modelSheet.ts');
    const want = sheet.buildModelSheet(FX.thesis.fiscal_year_figures, FX.thesis.fiscal_years, FX.thesis.model && FX.thesis.model.line_names).renderedFigureCount;
    const got = L.attrValues(r.html, 'data-model-fiscal-cells').map((v) => Number(v.value));
    if (got.length !== 1 || got[0] !== want) f.push(`data-model-fiscal-cells reads ${JSON.stringify(got)} (want one attribute = ${want}; tabs.harness.cjs reads it)`);
  }
  arms.push(['SYSTEM FACTS: none of the four system sentences at rest, none verbatim behind a toggle, the fiscal-cell count still on the tab', f.length === 0,
    f.length ? `${f.length} faults: ${f.slice(0, 4).join(' | ')}` : '0 of 4 sentences at rest; 0 verbatim; data-model-fiscal-cells kept']);
}
// Arm 4 -- planted.
{
  const f = [];
  const opts = STAMPS.map((s) => `<option value="${s}">${etLabel(s)}</option>`).join('');
  const goodEt = `<div data-model-panel-header=""><h3>Model</h3><span>Updated ${ET_DAY}</span></div><section data-what-changed=""><select>${opts}</select></section>`
    + `<details><summary>Where each input came from</summary><section data-input-ledger="">Market data: Bloomberg; last ran ${ET_DAY} and worked.</section></details>`;
  const goodFacts = '<div data-tab-panel="model"><p>Figures in USD</p><details><summary>About these figures</summary><p>147 yearly figures are shown from the research model.</p></details></div>';
  if (etFaults(goodEt).length) f.push(`the good ET face is rejected: ${etFaults(goodEt)[0]}`);
  if (factFaults(goodFacts).length) f.push(`the good facts face is rejected: ${factFaults(goodFacts)[0]}`);
  const s0 = STAMPS[STAMPS.length - 1];
  const mutants = [
    ['an option in UTC', etFaults, goodEt.replace(`>${etLabel(s0)}<`, '>September 30th, 2026, 12:39 UTC<')],
    ['a 24-hour clock with ET', etFaults, goodEt.replace(`>${etLabel(s0)}<`, '>September 30th, 2026, 08:39 ET<')],
    ['the header on the UTC day', etFaults, goodEt.replace(`Updated ${ET_DAY}`, `Updated ${UTC_DAY}`)],
    ['a system sentence at rest', factFaults, goodFacts.replace('<p>Figures in USD</p>', '<p>Showing 147 fiscal figures from the model block</p>')],
    ['a system sentence in an open details', factFaults, goodFacts.replace('<details>', '<details open="">').replace('147 yearly figures are shown from the research model.', 'Re-running one input on its own is not available on this page yet.')],
    ['a system sentence in an sr-only span', factFaults, goodFacts.replace('<p>Figures in USD</p>', '<p>Figures in USD<span class="sr-only">16 versions have landed; a refresh adds a version and never overwrites an earlier one.</span></p>')],
    ['a system sentence verbatim behind the toggle', factFaults, goodFacts.replace('147 yearly figures are shown from the research model.', 'No year-on-year growth rows: the model block serves none and this page computes none.')],
  ];
  let caught = 0;
  for (const [name, judge, html] of mutants) { if (judge(html).length) caught += 1; else f.push(`mutant "${name}" accepted`); }
  arms.push(['PLANTED: the predicates accept good synthetic faces and reject 7 mutants', f.length === 0, f.length ? f.join(' | ') : `2 good faces accepted; ${caught} of ${mutants.length} mutants rejected`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE MODEL TAB READS IN ET AND IN READER WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
