/**
 * exportCompare.harness.cjs -- AMGT_RESAPP AMGT-rl-10, AC1/AC2.
 *
 * INSTRUMENT. Reuses `tabs.harness.cjs`'s OWN loader (real sources, stubbed boundaries: the
 * ACTUAL `SecurityAnalysis` page, `IdentityHeader`/`StatTile`, `ThesisTab`, `ModelTab`,
 * `PostureTab`, transpiled with the installed typescript, rendered by the ACTUAL
 * react-dom/server) over `tabsFixture.BA_US_Equity.json` (the SAME captured bytes
 * `measure_landed_pack.py` builds the model block from, so the page half and the export half
 * of this comparison read the SAME landed record, never two that have drifted apart).
 *
 * THE THREE SETS, per the task order:
 *   FIGURES   a number with its label -- the identity header's 7 StatTiles (data-stat-tile,
 *             data-stat-state="SERVED") and the Model tab's fiscal-year cells
 *             (data-model-row + data-model-cell, walked against the table's own year headers),
 *             keyed "header|MNEMONIC" / "fiscal|MNEMONIC|YEAR" -- the SAME key shape the export
 *             document is walked with, so "same" means the same (mnemonic, scope) pair reached
 *             BOTH surfaces, never that the two texts happen to match byte for byte.
 *   CITES     a passage's accession line -- the Thesis tab's own evidence-id attribute
 *             (`data-thesis-passage`, `ThesisTab.tsx`'s `EvidenceDisclosure`), deduplicated.
 *   ABSENCES  an "ABSENT ... reason" or "[MACHINE-EMPTY: ...]" line -- the Model tab's
 *             `CasesBlock` ("... cases: ABSENT -- <reason>") and any REFUSED model row's own
 *             sentence (`data-model-refused`), both real, both printed with their denominator.
 *
 * RUN (from the portal root):
 *   node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --pack <path/to/pack_*.txt>
 *   node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --rich <path/to/*.md>
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');
const { createRequire } = require('module');

const base = 'C:/Users/Opal Bloomberg/Desktop/ajb_workspace/portal';  // AE~A ro-7 diagnostic: rebased, copy runs outside portal/
const req = createRequire(path.join(base, 'package.json'));
const ts = req('typescript');
const React = req('react');
const { renderToStaticMarkup } = req('react-dom/server');

const args = process.argv.slice(2);
const modeIdx = args.findIndex((a) => a === '--pack' || a === '--rich');
if (modeIdx === -1 || !args[modeIdx + 1]) {
  console.error('usage: exportCompare.harness.cjs --pack <path> | --rich <path> [--fixture <path>]');
  process.exit(2);
}
const MODE = args[modeIdx].slice(2); // 'pack' | 'rich'
const ARTIFACT_PATH = path.resolve(process.cwd(), args[modeIdx + 1]);

// AMGT-rn-5: --fixture <path> renders the page half from an ALTERNATE fixture (e.g. the SERVED
// plane's captured JSON) instead of the landed tabsFixture.BA_US_Equity.json. Default unchanged.
const fixtureFlagIdx = args.findIndex((a) => a === '--fixture');
const fixturePath = fixtureFlagIdx !== -1 && args[fixtureFlagIdx + 1]
  ? path.resolve(process.cwd(), args[fixtureFlagIdx + 1])
  : path.join(base, 'src/pages/SecurityAnalysis/__harness__', 'tabsFixture.BA_US_Equity.json');
const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));

let current = fixture;
let tabState = 'thesis';

const box = ({ children }) => React.createElement('section', null, children);
const nothing = () => null;
const noop = () => {};
const loaded = {};

// ---------------------------------------------------------------------------
// THE LOADER -- copied verbatim (STUBS/SOURCE_STUBS/source/resolveRelative) from
// `tabs.harness.cjs`, this round's own harness (read-only, not this cell's to edit).
// ---------------------------------------------------------------------------
const STUBS = {
  '@/ui/components/panels': { Panel: box, PanelHeader: box, PanelContent: box, PanelFooter: box },
  '@/ui/components/Select': { Select: nothing },
  '@/ui/components/EmptyState': { EmptyState: ({ title }) => React.createElement('div', null, title) },
  '@/ui/components/states': {
    PanelEmpty: ({ message }) => React.createElement('div', { 'data-panel-state': 'empty' }, message),
    PanelLoading: ({ label }) => React.createElement('div', { 'data-panel-state': 'loading' }, label || 'Loading'),
    PanelError: ({ message, cause }) => React.createElement('div', { 'data-panel-state': 'error' }, [message, cause]),
    PanelNoPermission: () => null,
  },
  '@/ui/components/Controls': {
    buttonClass: () => '',
    Segmented: ({ options, value, ariaLabel }) =>
      React.createElement('div', { role: 'group', 'aria-label': ariaLabel, 'data-segmented-value': value },
        (options || []).map((o) => React.createElement('button', { key: String(o.value), type: 'button' }, o.label))),
  },
  '@/components/HelperTip': { HelperTip: ({ children }) => React.createElement('span', null, children) },
  '@/components/DataTooltip': {
    DataTooltip: ({ header, rows }) =>
      React.createElement('div', { 'data-data-tooltip': header }, (rows || []).map((r) => String(r.value)).join(' | ')),
  },
  '@/hooks/useAuth': { useAuth: () => ({ claims: { firmId: 'RL10-EXPORT-COMPARE' } }) },
  '@/lib/utils': { cn: (...xs) => xs.filter(Boolean).join(' ') },
  'react-router-dom': { useParams: () => ({ securityKey: current ? current.security_key : undefined }) },
  '@/contexts/PageThemeContext': { PageThemeProvider: box },
  '@/components/PageHeaderVariants': {
    PageHeaderCleanBadge: ({ title, actions }) => React.createElement('header', { 'data-page-header': title }, actions),
  },
  '@/hooks/useTabNavigation': {
    useTabNavigation: () => ({ activeTab: tabState, handleTabChange: noop, tabContentRef: null }),
  },
  '@/components/TabNavigation': {
    TabNavigation: ({ tabs }) =>
      React.createElement('nav', null, tabs.map((tab) => React.createElement('span', { key: tab.id, 'data-tab-id': tab.id }, tab.label))),
  },
  recharts: {
    ResponsiveContainer: box, LineChart: box, Line: nothing, XAxis: nothing, YAxis: nothing,
    CartesianGrid: nothing, Tooltip: nothing, Legend: nothing,
  },
};

const SOURCE_STUBS = {
  'src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts': {
    useThesisBundle: () => ({ data: current ? current.thesis : undefined, isLoading: false }),
    usePeerSet: () => ({ data: current ? current.peers : undefined, isLoading: false }),
    useSecurityOverlay: () => ({ data: current ? current.overlay : undefined, isLoading: false }),
    useCoverageSet: () => ({ data: undefined, isLoading: false }),
    useLeadPanelRankings: () => ({ data: undefined, isLoading: false, isError: false }),
    useRankTimeSeries: () => ({}),
    useStarredList: () => ({ data: [], isLoading: false, isError: false }),
    useSetStarred: () => ({ mutate: noop }),
    useRequestRefresh: () => ({ mutate: noop, isPending: false }),
  },
  'src/pages/SecurityAnalysis/components/PrintExportAction.tsx': {
    PrintExportAction: () => React.createElement('button', { 'data-print-action': 'header' }, 'Print'),
  },
};

function resolveRelative(fromRel, name) {
  const joined = path.posix.normalize(path.posix.join(path.posix.dirname(fromRel), name));
  for (const candidate of [joined + '.tsx', joined + '.ts', joined]) {
    if (fs.existsSync(path.join(base, candidate)) && fs.statSync(path.join(base, candidate)).isFile()) return candidate;
  }
  throw new Error(`cannot resolve ${name} from ${fromRel}`);
}

function source(rel) {
  if (loaded[rel]) return loaded[rel];
  const file = path.join(base, rel);
  const bytes = fs.readFileSync(file);
  const js = ts.transpileModule(bytes.toString('utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 },
  }).outputText;
  const mod = { exports: {} };
  loaded[rel] = mod.exports;
  function load(name) {
    if (Object.prototype.hasOwnProperty.call(STUBS, name)) return STUBS[name];
    if (name.startsWith('.')) {
      const target = resolveRelative(rel, name);
      if (SOURCE_STUBS[target]) return SOURCE_STUBS[target];
      return source(target);
    }
    return req(name);
  }
  vm.runInThisContext('(function(require,module,exports){' + js + '\n})', { filename: file })(load, mod, mod.exports);
  loaded[rel] = mod.exports;
  return mod.exports;
}

const { SecurityAnalysis } = source('src/pages/SecurityAnalysis/SecurityAnalysis.tsx');

function renderPage(tab) {
  tabState = tab;
  return renderToStaticMarkup(React.createElement(SecurityAnalysis));
}

// ---------------------------------------------------------------------------
// THE PAGE'S OWN THREE SETS
// ---------------------------------------------------------------------------
const thesisHtml = renderPage('thesis');
const modelHtml = renderPage('model');
// AMGT-ro-1 item 2: FIGURES/CITES stay scoped to Thesis + Model (unchanged -- CITES is
// deliberately thesis-only, per the module header above), but ABSENCES below used to compare
// the export's Peers/Exec-Management-sourced lines (`_peers_markdown`'s ABSENT CSC columns,
// `_management_markdown`'s ceo_bio MACHINE-EMPTY) against a page render that never mounted
// PeersTab or ExecManagementTab at all -- every one of those export lines read as an "extra"
// the page never carries, when in fact PeersTab renders the SAME absent-column reasons (behind
// its own collapsed disclosure -- still present in a static, no-JS-state render) and
// ExecManagementTab renders the SAME ceo_bio object. PostureTab is rendered too, for the same
// reason (`_posture_markdown`'s ABSENT line). Three more real renders, same loader, same stubs
// (verified: all three render clean off the existing STUBS/SOURCE_STUBS with no new stub
// needed).
const execManagementHtml = renderPage('exec_management');
const peersHtml = renderPage('peers');
const postureHtml = renderPage('posture');
const combinedHtml = [thesisHtml, modelHtml, execManagementHtml, peersHtml, postureHtml].join('\n');

// AMGT-ro-1 item 2: the three scalars `IdentityHeader` (`components/SecurityOverlay.tsx`) prints
// as plain text beside the seven Stat tiles -- sector, country (joined "sector -- country") and
// currency (the price tile's own prefix, `StatTile.tsx`'s `formatStatValue` price branch) --
// never behind a `data-stat-tile` attribute, so `pageFigures()` below never saw them. Read the
// SAME mnemonics `constants.ts` names (`IDENTITY_SECTOR_MNEMONIC`/`IDENTITY_COUNTRY_MNEMONIC`/
// `IDENTITY_CURRENCY_MNEMONIC`), transcribed here for the same reason `render_pack.py`'s
// `PAGE_HEADER_MNEMONICS` transcribes them (no import path from a `.cjs` harness that predates
// this cell's own loader wiring for `constants.ts`).
const IDENTITY_LINE_MNEMONICS = ['GICS_SECTOR_NAME', 'CNTRY_OF_DOMICILE', 'CRNCY'];

function pageFigures(html) {
  const out = new Set();
  for (const m of html.matchAll(/data-stat-tile="([^"]+)" data-stat-state="SERVED"/g)) {
    out.add('header|' + m[1]);
  }
  // THE IDENTITY LINE: confirmed PRESENT the same way a stat tile is confirmed SERVED -- not by
  // trusting the fixture, but by checking the mnemonic's OWN value (read off the SAME fixture
  // the page rendered from) actually reached the rendered markup. A mnemonic absent from the
  // payload, or whose value never reaches the DOM, is correctly NOT added.
  const overlayFigures = (current && current.overlay && current.overlay.header_figures) || [];
  for (const mnemonic of IDENTITY_LINE_MNEMONICS) {
    const figure = overlayFigures.find((f) => f.mnemonic === mnemonic);
    const value = figure ? figure.value : undefined;
    if (value !== undefined && value !== null && String(value) !== '' && html.includes(String(value))) {
      out.add('header|' + mnemonic);
    }
  }
  // The Model sheet table: years off the header row, mnemonic off each data-model-row, values
  // off each row's ordered data-model-cell tds -- a REFUSED row (data-model-refused) has no
  // bare value cell and contributes nothing to FIGURES (it is an ABSENCE, below).
  const tableMatch = html.match(/<table data-model-sheet[^>]*>([\s\S]*?)<\/table>/);
  if (tableMatch) {
    const theadMatch = tableMatch[1].match(/<thead>([\s\S]*?)<\/thead>/);
    const years = theadMatch
      ? Array.from(theadMatch[1].matchAll(/<th[^>]*>([^<]*)<\/th>/g)).map((m) => m[1]).slice(1)
      : [];
    const rowRe = /<tr data-model-row="([^"]+)"[^>]*>([\s\S]*?)<\/tr>/g;
    let rowMatch;
    while ((rowMatch = rowRe.exec(tableMatch[1]))) {
      const mnemonic = rowMatch[1];
      const body = rowMatch[2];
      if (body.includes('data-model-refused')) continue; // ABSENCE, not a FIGURE
      // EVERY <td> in the row, IN ORDER -- a null cell (`<td>--</td>`, no `data-model-cell`
      // attribute) still occupies its own array slot, so its POSITION (and every year after
      // it) stays aligned with `years`. Matching data-model-cell tds ONLY would silently
      // shift every later year's index left by one per null cell in between (measured: this
      // exact shift mis-keyed CURRENT_EV_TO_T12M_EBITDA's real 2023/2024/2025 cells onto
      // 2021/2022/2023 the first time this harness ran).
      const cellTags = Array.from(body.matchAll(/<td([^>]*)>([^<]*)<\/td>/g)).slice(1); // drop the label td
      cellTags.forEach(([, attrs, text], idx) => {
        if (attrs.includes('data-model-cell') && text && text !== '--' && years[idx]) {
          out.add('fiscal|' + mnemonic + '|' + years[idx]);
        }
      });
    }
  }
  return out;
}

function pageCites(html) {
  const out = new Set();
  for (const m of html.matchAll(/data-thesis-passage="([^"]+)"/g)) out.add(m[1]);
  return out;
}

// react-dom/server escapes text nodes/attribute values (&amp; &lt; &gt; &quot; &#x27;) -- decode
// before comparing against the rich document's plain-text reasons, or an apostrophe/quote/arrow
// inside a real reason reads as a false "missing".
function decodeEntities(text) {
  return text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'");
}

function pageAbsences(html) {
  const out = new Set();
  for (const m of html.matchAll(/ABSENT\s*--\s*([^<\n]{1,300})/g)) out.add('ABSENT: ' + decodeEntities(m[1].trim()));
  for (const m of html.matchAll(/REFUSED\s*--\s*([^<\n]{1,300})/g)) out.add('REFUSED: ' + decodeEntities(m[1].trim()));
  return out;
}

const PAGE_FIGURES = pageFigures(combinedHtml);
const PAGE_CITES = pageCites(thesisHtml);
const PAGE_ABSENCES = pageAbsences(combinedHtml);

// ---------------------------------------------------------------------------
// THE ARTIFACT'S THREE SETS -- the pack's plain-text render_figure_line lines (heading-aware:
// "Header" / "Fiscal year <fy>"), or the rich document's markdown table rows, both reusing the
// SAME withheld-value convention ("[BLOCKED] [REFUSED: ...]" is never a FIGURE).
// ---------------------------------------------------------------------------
function artifactFiguresAndAbsencesFromPackText(text) {
  const figures = new Set();
  const absences = new Set();
  let section = null; // 'header' | fiscal year string
  const MID_DOT = '·';
  for (const rawLine of text.split('\n')) {
    const line = rawLine.trim();
    if (!line) continue;
    if (line === 'Header') { section = 'header'; continue; }
    const fyMatch = line.match(/^Fiscal year (\S+)$/);
    if (fyMatch) { section = fyMatch[1]; continue; }
    if (line.startsWith('[MACHINE-EMPTY:')) {
      const m = line.match(/^\[MACHINE-EMPTY: (.+)\]$/);
      absences.add('MACHINE-EMPTY: ' + (m ? m[1] : line));
      continue;
    }
    if (section === null || !line.includes(MID_DOT)) continue;
    const segments = line.split(' ' + MID_DOT + ' ');
    if (segments.length < 2) continue;
    const mnemonicMatch = segments[1].match(/^(\S+)\s*\(/);
    if (!mnemonicMatch) continue;
    const mnemonic = mnemonicMatch[1];
    if (segments[0].includes('[REFUSED:')) {
      absences.add('REFUSED: ' + segments[0]);
      continue;
    }
    figures.add(section === 'header' ? 'header|' + mnemonic : 'fiscal|' + mnemonic + '|' + section);
  }
  return { figures, absences };
}

function artifactFiguresAndAbsencesFromRichText(text) {
  const figures = new Set();
  const absences = new Set();
  let section = null;
  const MID_DOT = '·';
  for (const rawLine of text.split('\n')) {
    const line = rawLine.trim();
    if (line === '## Header') { section = 'header'; continue; }
    const fyMatch = line.match(/^## Fiscal year (\S+)$/);
    if (fyMatch) { section = fyMatch[1]; continue; }
    if (line.startsWith('## ')) { section = null; continue; } // left the figures region
    const machineEmpty = line.match(/\[MACHINE-EMPTY: ([^\]]+)\]/);
    if (machineEmpty) { absences.add('MACHINE-EMPTY: ' + machineEmpty[1]); continue; }
    // AMGT-ro-1 item 2: `_refused_figures_markdown`'s own line -- "MNEMONIC: REFUSED --
    // <reason>", bare, inside "## Model Notes" -- one per REFUSED mnemonic, never inside a table
    // row once render_pack.py stopped printing a REFUSED figure as a value row at all. Matched
    // BEFORE the generic ABSENT check (a REFUSED line never starts with the word ABSENT).
    const refusedLine = line.match(/^\S+:\s*REFUSED\s*--\s*(.+)$/);
    if (refusedLine) { absences.add('REFUSED: ' + refusedLine[1].trim()); continue; }
    const absent = line.match(/ABSENT\s*--\s*(.+)$/);
    if (absent) { absences.add('ABSENT: ' + absent[1].trim()); continue; }
    if (section === null) continue;
    const rowMatch = line.match(/^\|\s*(\S+)\s*\|\s*(.+?)\s*\|$/);
    if (!rowMatch) continue;
    const mnemonic = rowMatch[1];
    const rendered = rowMatch[2];
    if (!rendered.includes(MID_DOT)) continue;
    if (rendered.includes('[REFUSED:')) { absences.add('REFUSED: ' + rendered); continue; }
    figures.add(section === 'header' ? 'header|' + mnemonic : 'fiscal|' + mnemonic + '|' + section);
  }
  return { figures, absences };
}

function artifactCites(text) {
  const out = new Set();
  for (const m of text.matchAll(/>?\s*(\S+) -- accession (\d+)/g)) out.add(m[1]);
  return out;
}

if (!fs.existsSync(ARTIFACT_PATH)) {
  console.error('BLOCKED: artifact not found at ' + ARTIFACT_PATH);
  process.exit(2);
}
const artifactText = fs.readFileSync(ARTIFACT_PATH, 'utf8');
const parsed = MODE === 'pack'
  ? artifactFiguresAndAbsencesFromPackText(artifactText)
  : artifactFiguresAndAbsencesFromRichText(artifactText);
const ARTIFACT_FIGURES = parsed.figures;
const ARTIFACT_ABSENCES = parsed.absences;
const ARTIFACT_CITES = artifactCites(artifactText);
const ARTIFACT_LABEL = MODE === 'pack' ? 'pack' : 'rich';

function setDiff(pageSet, otherSet) {
  const same = [...pageSet].filter((x) => otherSet.has(x));
  const missing = [...pageSet].filter((x) => !otherSet.has(x));
  const extra = [...otherSet].filter((x) => !pageSet.has(x));
  return { same, missing, extra };
}

console.log('ARTIFACT: ' + MODE + ' ' + ARTIFACT_PATH);
console.log('ARTIFACT BYTES: ' + Buffer.byteLength(artifactText, 'utf8'));

const figDiff = setDiff(PAGE_FIGURES, ARTIFACT_FIGURES);
console.log(
  'FIGURES page=' + PAGE_FIGURES.size + ' ' + ARTIFACT_LABEL + '=' + ARTIFACT_FIGURES.size +
  ' same=' + figDiff.same.length + ' missing=' + figDiff.missing.length + ' extra=' + figDiff.extra.length
);

const citeDiff = setDiff(PAGE_CITES, ARTIFACT_CITES);
console.log(
  'CITES page=' + PAGE_CITES.size + ' ' + ARTIFACT_LABEL + '=' + ARTIFACT_CITES.size +
  ' same=' + citeDiff.same.length + ' missing=' + citeDiff.missing.length + ' extra=' + citeDiff.extra.length
);

const absDiff = setDiff(PAGE_ABSENCES, ARTIFACT_ABSENCES);
console.log(
  'ABSENCES page=' + PAGE_ABSENCES.size + ' ' + ARTIFACT_LABEL + '=' + ARTIFACT_ABSENCES.size +
  ' same=' + absDiff.same.length + ' missing=' + absDiff.missing.length + ' extra=' + absDiff.extra.length
);

console.log('');
console.log('GAP TABLE (in words):');
console.log(
  '  FIGURES: ' + figDiff.same.length + ' of ' + PAGE_FIGURES.size + ' page figures reach the ' +
  ARTIFACT_LABEL + '; ' + figDiff.missing.length + ' page figure(s) the ' + ARTIFACT_LABEL +
  ' does not carry; ' + figDiff.extra.length + ' ' + ARTIFACT_LABEL + ' figure(s) not shown on the page.'
);
console.log(
  '  CITES: ' + citeDiff.same.length + ' of ' + PAGE_CITES.size + ' page cites reach the ' + ARTIFACT_LABEL +
  '; ' + citeDiff.missing.length + ' page cite(s) missing from the ' + ARTIFACT_LABEL + '.'
);
console.log(
  '  ABSENCES: ' + absDiff.same.length + ' of ' + PAGE_ABSENCES.size + ' page absences read the SAME reason in the ' +
  ARTIFACT_LABEL + '; ' + absDiff.missing.length + ' page absence(s) the ' + ARTIFACT_LABEL +
  ' states differently or not at all; ' + absDiff.extra.length + ' ' + ARTIFACT_LABEL +
  ' absence(s) (e.g. undrafted sections) the page does not carry as an ABSENT/REFUSED line.'
);

if (MODE === 'rich') {
  console.log('');
  console.log('RICH DOC SIZE: ' + Buffer.byteLength(artifactText, 'utf8') + ' bytes (' +
    (Buffer.byteLength(artifactText, 'utf8') > 20 * 1024 ? '>' : '<=') + ' 20 KB)');
  console.log('RICH DOC FIRST 200 CHARS: ' + JSON.stringify(artifactText.slice(0, 200)));

  // Every [MACHINE-EMPTY]/ABSENT line the PAGE carries must be present in the rich doc, with
  // its reason -- AC2's own wording.
  let pageAbsencesCoveredInRich = 0;
  const uncovered = [];
  for (const item of PAGE_ABSENCES) {
    const reason = item.split(/: /).slice(1).join(': ');
    if (reason && artifactText.includes(reason)) pageAbsencesCoveredInRich += 1;
    else uncovered.push({ item: item, reason: reason });
  }
  console.log('DIAG uncovered-by-reason count: ' + uncovered.length);
  for (const u of uncovered) {
    console.log('DIAG   PAGE ITEM : ' + JSON.stringify(u.item));
    console.log('DIAG   REASON    : ' + JSON.stringify(u.reason));
  }
  console.log('DIAG absDiff.missing (' + absDiff.missing.length + '):');
  for (const m of absDiff.missing) console.log('DIAG   MISSING   : ' + JSON.stringify(m));
  console.log('DIAG absDiff.extra (' + absDiff.extra.length + '):');
  for (const e of absDiff.extra) console.log('DIAG   EXTRA     : ' + JSON.stringify(e));
  console.log(
    'PAGE ABSENCE LINES COVERED IN RICH DOC (verbatim reason found): ' + pageAbsencesCoveredInRich +
    ' of ' + PAGE_ABSENCES.size
  );

  // AMGT-ro-1 item 2 (Z-S268, row's own words): "ok also requires 0 figure extras and every
  // rich absence to be a page absence" -- both sets were already COMPUTED above (figDiff.extra,
  // absDiff.extra) and PRINTED, but never fed into the verdict; FWD-30's DONE WHEN reads "NOTHING
  // in the export that is not on the page", which this harness could not see until now.
  const ok =
    figDiff.missing.length === 0 &&
    figDiff.extra.length === 0 &&
    citeDiff.missing.length === 0 &&
    pageAbsencesCoveredInRich === PAGE_ABSENCES.size &&
    absDiff.extra.length === 0 &&
    Buffer.byteLength(artifactText, 'utf8') > 20 * 1024;
  console.log('EXPORT-COMPARE ' + (ok ? 'OK' : 'NOT OK'));
  process.exit(ok ? 0 : 1);
}

process.exit(0);
