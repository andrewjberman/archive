/**
 * check_gr7_wording.cjs -- acceptance arms for the gr-7 WORDING follow-up (CTO 6706): the AI row's count of web blocks reads "1 cites a web search made when it was written" (plural: "N cite web searches made when they were written"), so it no longer sits beside the stored-search line as a contradiction. A copy of round106_aifill_prep/checks/check_gr7_provenance.cjs with the two web-count expectations changed and one arm added for the singular.
 *
 * RUN (from anywhere):  node check_gr7_wording.cjs <portal worktree root>
 * The ACTUAL components/InputProvenance.tsx and dateWords.ts of that tree, transpiled with its installed typescript and rendered by its react-dom/server; no browser, no network, no file written.
 * The CVO's finding (C-S143 item 8): on every page the panel read "web search results stored for this name -- nothing has been read from this input for this name yet" beside blocks labelled
 * "From a web search": the panel described the SERP collection input and said nothing about the AI fill the page was showing. The CTO's 4(d): "ABOUT THIS DATA reads the AI-fill input it renders."
 * PRINTS one `ARM <name> PASS|FAIL <detail>` per arm, then `AIFILL PROVENANCE: YES (N of N)` (exit 0) or `NO (k of N)` (exit 1).
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { createRequire } = require('module');

const base = path.resolve(process.argv[2] || '.');
const req = createRequire(path.join(base, 'package.json'));
const ts = req('typescript');
const React = req('react');
const { renderToStaticMarkup } = req('react-dom/server');
const h = React.createElement;
const SA = 'src/pages/SecurityAnalysis/';

function transpile(text) {
  return ts.transpileModule(text, { compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 } }).outputText;
}
const loaded = {};
function source(rel) {
  if (loaded[rel]) return loaded[rel];
  const file = path.join(base, rel);
  const js = transpile(fs.readFileSync(file, 'utf8'));
  const mod = { exports: {} };
  loaded[rel] = mod.exports;
  function load(name) {
    if (name === 'react') return React;
    if (name.startsWith('.')) {
      const joined = path.posix.normalize(path.posix.join(path.posix.dirname(rel), name));
      for (const c of [joined + '.tsx', joined + '.ts']) {
        if (fs.existsSync(path.join(base, c))) return source(c);
      }
      return {};
    }
    return req(name);
  }
  vm.runInThisContext('(function(require,module,exports){' + js + '\n})', { filename: file })(load, mod, mod.exports);
  loaded[rel] = mod.exports;
  return mod.exports;
}

const { InputProvenance } = source(SA + 'components/InputProvenance.tsx');
const { longDate } = source(SA + 'dateWords.ts');

const ENTRIES = [
  { input: 'bloomberg', source: 'Bloomberg', last_run: 'NEVER', outcome: 'never', reason: 'No Bloomberg read is stored for this name.' },
  { input: 'seekingalpha', source: 'Seeking Alpha', last_run: 'NEVER', outcome: 'never', reason: 'No Seeking Alpha read is stored for this name.' },
  { input: 'serp', source: 'Web search results stored for this name', last_run: 'NEVER', outcome: 'never', reason: 'nothing has been read from this input for this name yet' },
  { input: 'filings', source: 'SEC filings', last_run: 'NEVER', outcome: 'never', reason: 'No filing is stored for this name.' },
  { input: 'pack', source: 'Research team pack', last_run: 'NEVER', outcome: 'never', reason: 'No pack is on file for this name.' },
];
const web = (id) => ({ block_id: id, source_class: 'WEB_SEARCH', machine_written: true, text: 'Some text.', reason: null, citations: [{ source_kind: 'web', url: 'https://example.com/a', title: 'A', quote: null, ref: null }] });
const opal = (id) => ({ block_id: id, source_class: 'OPAL_SOURCE', machine_written: true, text: 'Some text.', reason: null, citations: [{ source_kind: 'opal', url: null, title: null, quote: null, ref: 'Company officer list' }] });
const none = (id) => ({ block_id: id, source_class: 'NONE', machine_written: true, text: null, reason: 'The research team pack already states this.', citations: [] });
const fill = (status, blocks) => ({ status, reason: status === 'SERVED' ? null : 'absent_object s3://x', source: status === 'SERVED' ? 'pool' : 'none', read_completed: true, as_of: '2026-10-14', generated_at: '2026-10-14T03:05:25Z', producer: { version: 'opal-aifill/1.1.0' }, blocks });
const IDS = ['mgmt_bio', 'mgmt_recent', 'mgmt_team_view', 'thesis_pillars', 'identity_description'];
const mixed = fill('SERVED', { mgmt_bio: web('mgmt_bio'), mgmt_recent: web('mgmt_recent'), mgmt_team_view: opal('mgmt_team_view'), thesis_pillars: none('thesis_pillars'), identity_description: none('identity_description') });
const allNone = fill('SERVED', Object.fromEntries(IDS.map((i) => [i, none(i)])));

function render(entries, aiFill) {
  return renderToStaticMarkup(h(InputProvenance, { entries, aiFill }));
}
function decode(s) {
  return s.replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}
function visible(html) {
  return decode(html.replace(/<!--[\s\S]*?-->/g, '').replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
}
function rows(html) {
  return Array.from(html.matchAll(/<li [^>]*data-provenance-row="([^"]*)"[^>]*>([\s\S]*?)<\/li>/g)).map((m) => ({ id: m[1], text: visible(m[2]) }));
}

const results = [];
function arm(name, fn) {
  let ok = false;
  let detail = '';
  try {
    const r = fn();
    ok = !!r.ok;
    detail = String(r.detail || '').slice(0, 220);
  } catch (err) {
    detail = 'threw ' + (err && err.message);
  }
  results.push(ok);
  console.log(`ARM ${name} ${ok ? 'PASS' : 'FAIL'} ${detail}`);
}

const DATE = longDate('2026-10-14');

arm('a SERVED fill adds one row after the five, naming the AI-written blocks, the date and the counts by source', () => {
  const r = rows(render(ENTRIES, mixed));
  const want = `AI-written blocks -- ${DATE} -- 2 cite web searches made when they were written, 1 from Opal sources`;
  return { ok: r.length === 6 && r[5].text === want && r[5].id === 'ai-fill', detail: r.length + ' rows; last=' + (r[5] && r[5].text) };
});

arm('the five served rows are unchanged, in order, with the row numbers they had', () => {
  const a = rows(render(ENTRIES, undefined));
  const b = rows(render(ENTRIES, mixed)).slice(0, 5);
  return { ok: a.length === 5 && JSON.stringify(a) === JSON.stringify(b) && a.map((x) => x.id).join() === '1,2,3,4,5', detail: a.map((x) => x.id).join() };
});

arm('web only: the Opal part is left out; Opal only: the web part is left out', () => {
  const w = fill('SERVED', Object.fromEntries(IDS.map((i) => [i, web(i)])));
  const o = fill('SERVED', Object.fromEntries(IDS.map((i) => [i, opal(i)])));
  const a = rows(render(ENTRIES, w))[5].text;
  const b = rows(render(ENTRIES, o))[5].text;
  return { ok: a === `AI-written blocks -- ${DATE} -- 5 cite web searches made when they were written` && b === `AI-written blocks -- ${DATE} -- 5 from Opal sources`, detail: a + ' | ' + b };
});

arm('ONE web block reads "1 cites a web search made when it was written" (the CTO wording), alone or beside an Opal part', () => {
  const one = fill('SERVED', { mgmt_bio: web('mgmt_bio'), mgmt_recent: none('mgmt_recent'), mgmt_team_view: none('mgmt_team_view'), thesis_pillars: none('thesis_pillars'), identity_description: none('identity_description') });
  const oneOpal = fill('SERVED', { mgmt_bio: web('mgmt_bio'), mgmt_recent: opal('mgmt_recent'), mgmt_team_view: none('mgmt_team_view'), thesis_pillars: none('thesis_pillars'), identity_description: none('identity_description') });
  const a = rows(render(ENTRIES, one))[5].text;
  const b = rows(render(ENTRIES, oneOpal))[5].text;
  return { ok: a === `AI-written blocks -- ${DATE} -- 1 cites a web search made when it was written` && b === `AI-written blocks -- ${DATE} -- 1 cites a web search made when it was written, 1 from Opal sources`, detail: a + ' | ' + b };
});

arm('a SERVED fill with every block NONE says no block was written for this name', () => {
  const r = rows(render(ENTRIES, allNone));
  return { ok: r.length === 6 && r[5].text === `AI-written blocks -- ${DATE} -- no block was written for this name`, detail: r[5] && r[5].text };
});

arm('ABSENT, INVALID, null and undefined add no row and leave the panel as it was', () => {
  const base0 = render(ENTRIES, undefined);
  const bad = [fill('ABSENT', {}), fill('INVALID', {}), null, undefined].map((f) => render(ENTRIES, f));
  const same = bad.every((x) => x === base0);
  const none5 = rows(base0).length === 5;
  return { ok: same && none5, detail: 'identical=' + same };
});

arm('the panel stays closed (a native details) and its summary still reads About this data', () => {
  const html = render(ENTRIES, mixed);
  return { ok: /<details[^>]*data-input-provenance/.test(html) && !/<details[^>]*\sopen/.test(html) && visible(html).includes('About this data'), detail: html.slice(0, 80) };
});

arm('with no served entries and a SERVED fill the panel shows the AI row alone; with neither it renders nothing', () => {
  const a = rows(render(null, mixed));
  const b = render(null, undefined);
  const c = render([], fill('ABSENT', {}));
  return { ok: a.length === 1 && a[0].text.startsWith('AI-written blocks') && b === '' && c === '', detail: a.length + ' rows; b=' + b.length + ' c=' + c.length };
});

arm('no raw code or technical reason reaches the visible text', () => {
  const v = visible(render(ENTRIES, mixed)) + ' ' + visible(render(ENTRIES, fill('INVALID', {})));
  return { ok: !/[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+/.test(v.replace(/nothing has been read from this input for this name yet/g, '')) && !v.includes('s3://') && !v.includes('absent_object'), detail: v.slice(-120) };
});

arm('the web-search collection row still says what it said (it describes the SERP input, not the AI fill)', () => {
  const r = rows(render(ENTRIES, mixed));
  return { ok: r[2].text === 'Web search results stored for this name -- nothing has been read from this input for this name yet', detail: r[2].text };
});

arm('SecurityAnalysis.tsx hands the served fill to the panel', () => {
  const src = fs.readFileSync(path.join(base, SA + 'SecurityAnalysis.tsx'), 'utf8');
  return { ok: /<InputProvenance[^>]*aiFill=\{thesisQuery\.data\?\.ai_fill\}/.test(src), detail: (src.match(/<InputProvenance[^>]*>/) || ['no mount'])[0] };
});

arm('the component and the page file stay ASCII', () => {
  const files = [SA + 'components/InputProvenance.tsx', SA + 'SecurityAnalysis.tsx'];
  const bad = files.filter((f) => fs.readFileSync(path.join(base, f)).some((b) => b > 127));
  return { ok: bad.length === 0, detail: bad.join(',') };
});

const passed = results.filter(Boolean).length;
console.log(`AIFILL PROVENANCE: ${passed === results.length && results.length > 0 ? 'YES' : 'NO'} (${passed} of ${results.length})`);
process.exit(passed === results.length ? 0 : 1);
