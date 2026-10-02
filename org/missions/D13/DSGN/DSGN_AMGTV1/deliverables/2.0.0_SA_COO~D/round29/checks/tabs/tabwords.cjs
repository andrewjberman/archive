/**
 * tabwords.cjs -- DSGN_AMGTV1 round 29, AV-zg-6 TABS (issuer 2.0.0_SA_COO~D): THE EXEC AND THESIS TABS READ IN PLAIN WORDS,
 * WITH THE CHIEF EXECUTIVE FIRST.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-70):
 *   node <this file>
 * Grades PRD v0.10 FWD-27 (DSGN_AMGTV1_PRD.md ~387-402): "officers list the chief executive first, then the chief financial
 * officer"; "an unconnected field prints no line"; "0 strings from the register's system-wording list". Register rows
 * (docs/briefs/amgt-security-analysis-ui-findings-20261002.json):
 *   SAUX-32  "Officers list the chief executive first, then the chief financial officer, then the rest by role rank."
 *   SAUX-31  "A field with no source is not printed as a line" -- this cell's line: 'No profile (no match found)'
 *            (tabs/ExecManagementTab.tsx ~126). NOT PRINTED means not in the rendered text at all: a closed <details> does
 *            not excuse it (SAUX-31's acceptance names no details vehicle; SAUX-30's does).
 *   SAUX-30  "None of the listed strings renders; each is replaced by reader words or moved behind a details toggle" -- this
 *            cell's three: 'in a union of <n>' (ExecManagementTab ~158), 'no served drafted sentence carries this passage on
 *            this bundle' (components/ThesisDriverChart.tsx ~162), 'The drafted document does not say how many claims were
 *            held back uncited' (tabs/ThesisTab.tsx ~63). Text inside a CLOSED <details> (no `open`) counts as moved behind
 *            a toggle; its <summary> is still face text.
 * Inputs (issuer-held, frozen from the base checkout's committed harness fixtures; see each file's _note):
 *   round29/fixtures/tabs/thesis.BA_US_Equity.json        served /thesis bundle (12 officers, alphabetical; ABSENT_ON_OBJECT)
 *   round29/fixtures/tabs/thesis.HD_US_Equity.mgmt.json   served management (10 officers; CEO row 6, CFO row 7)
 *   round29/fixtures/tabs/thesis.BABA_US_Equity.mgmt.json served management (7 officers; Chairman row 1, CEO row 2, a
 *                                                          business-group CEO row 7)
 *   round29/fixtures/tabs/mgmt.BA_US_Equity.planted.json  PLANTED: BA reversed (three segment CEOs above the company CEO) and
 *                                                          one officer NOT-ATTEMPTED
 *   round29/fixtures/tabs/driverChart.filing.planted.json PLANTED: a SERVED filing chart, P0111 resolves, P9999 does not
 * The company chief executive is the served `management.ceo_public_profile.ceo_name`; the CFO is the one officer whose served
 * role names "Chief Financial Officer". Rows are read off `data-exec-officer` (the existing row hook) in document order.
 * The driver chart's passage text renders only after a click, so the chart is rendered with React.useState forced open
 * (an initial null -> the planted passage id, an initial false -> true); a positive control proves the force reached the
 * passage. If the force cannot reach it, the arm falls back to the source: the phrase must be gone from every string and JSX
 * text node of ThesisDriverChart.tsx.
 * Arms:
 *   1  ORDER (SAUX-32): on BA, HD, BABA (served) and BA reversed (planted), row 1 is the CEO, row 2 the CFO, no officer dropped.
 *   2  NO-SOURCE PROFILE (SAUX-31): Exec on BA (served) and BA planted prints none of "no profile" / "no match found" /
 *      "not attempted" / "not found" in its rendered text; every MATCHED officer still carries its profile link.
 *   3  SYSTEM WORDS (SAUX-30): 'in a union of' (Exec, BA), 'held back uncited' (Thesis, BA), 'no served drafted sentence
 *      carries' (driver chart, forced open on P9999) are absent from the face text.
 *   4  PLANTED: the order comparator and the two text predicates reject known-bad inputs and accept known-good ones.
 * Prints one line per arm and "THE EXEC AND THESIS TABS READ IN PLAIN WORDS: <k> of 4 arms"; exit 0 only at 4 of 4.
 * No network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const D = path.join(__dirname, '..', '..', '..');
const FX = path.join(D, 'round29', 'fixtures', 'tabs');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const ts = require('module').createRequire(path.join(L.base, 'package.json'))('typescript');
const load = (name) => { const d = JSON.parse(fs.readFileSync(path.join(FX, name), 'utf8')); return d && d.payload ? d.payload : d; };
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');

/** FACE HTML: every CLOSED <details> (no `open` attribute) is replaced by its <summary> only; an open one keeps its body. */
function faceHtml(html) {
  let out = String(html);
  const re = /<details(\s[^>]*)?>((?:(?!<details[\s>])[\s\S])*?)<\/details>/;
  let m;
  let guard = 0;
  while ((m = re.exec(out)) !== null && guard++ < 5000) {
    const isOpen = /(^|\s)open(=|\s|$)/.test(m[1] || '');
    const s = /<summary[^>]*>([\s\S]*?)<\/summary>/.exec(m[2]);
    const repl = isOpen ? '<div>' + m[2] + '</div>' : '<div>' + (s ? s[1] : '') + '</div>';
    out = out.slice(0, m.index) + repl + out.slice(m.index + m[0].length);
  }
  return out;
}
const faceText = (html) => L.textOf(faceHtml(html));

const NO_SOURCE = /\bno profile\b|no match found|\bnot attempted\b|\bnot found\b/i; // SAUX-31: graded on ALL rendered text
const SYSTEM_WORDS = [
  ['in a union of', /in a union of/i],
  ['held back uncited', /held back uncited/i],
  ['no served drafted sentence carries', /no served drafted sentence carries/i],
];

function rowNames(html) { return L.attrValues(html, 'data-exec-officer').map((a) => decode(a.value)); }
function orderFaults(names, management) {
  const f = [];
  const served = (management.officers || []).map((o) => o.name);
  const ceo = management.ceo_public_profile && management.ceo_public_profile.ceo_name;
  const cfos = (management.officers || []).filter((o) => /chief financial officer/i.test(o.role || '')).map((o) => o.name);
  if (!ceo) f.push('INPUT: no served ceo_name');
  if (cfos.length !== 1) f.push('INPUT: ' + cfos.length + ' officers name Chief Financial Officer');
  if (names.length !== served.length || [...names].sort().join('|') !== [...served].sort().join('|')) {
    f.push('SET: rendered ' + names.length + ' of ' + served.length + ' served officers');
  }
  if (names[0] !== ceo) f.push('ROW 1 is "' + names[0] + '", not the chief executive "' + ceo + '" (CEO at row ' + (names.indexOf(ceo) + 1) + ')');
  if (cfos.length === 1 && names[1] !== cfos[0]) f.push('ROW 2 is "' + names[1] + '", not the CFO "' + cfos[0] + '" (CFO at row ' + (names.indexOf(cfos[0]) + 1) + ')');
  return f;
}

function renderExec(bundle) {
  L.hookState.impl = { useThesisBundle: () => bundle };
  const m = L.source(SA + 'tabs/ExecManagementTab.tsx');
  return L.render(m.ExecManagementTab, { securityKey: bundle.security_key || 'BA_US_Equity' });
}
function renderThesis(bundle) {
  L.hookState.impl = { useThesisBundle: () => bundle };
  const m = L.source(SA + 'tabs/ThesisTab.tsx');
  return L.render(m.ThesisTab, { securityKey: bundle.security_key || 'BA_US_Equity' });
}
/** Render the driver chart with every initial-null state forced to `id` and every initial-false state forced to true. */
function renderChartForced(props, id) {
  const React = L.React;
  const orig = React.useState;
  React.useState = function forced(init) {
    const r = orig(init);
    const v = typeof init === 'function' ? init() : init;
    if (v === null || v === undefined) return [id, r[1]];
    if (v === false) return [true, r[1]];
    return r;
  };
  try {
    const m = L.source(SA + 'components/ThesisDriverChart.tsx');
    return L.render(m.ThesisDriverChart, props);
  } finally {
    React.useState = orig;
  }
}
/** Every string-literal, template and JSX-text node of a source file (comments excluded). */
function sourceStrings(rel) {
  // Honours the loader's ISSUER GREEN ARM override (CHECK_SRC_OVERRIDE), so a scratch reference proves the arm CAN pass.
  const over = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]);
  const hit = over.find(([k]) => k === rel);
  const file = hit ? hit[1] : path.join(L.base, rel);
  const sf = ts.createSourceFile(rel, fs.readFileSync(file, 'utf8'), ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const out = [];
  (function walk(n) {
    if (ts.isStringLiteral(n) || ts.isNoSubstitutionTemplateLiteral(n) || ts.isJsxText(n)) out.push(n.text);
    else if (ts.isTemplateExpression(n)) out.push(n.getText(sf));
    ts.forEachChild(n, walk);
  })(sf);
  return out.join('\n');
}

const BA = load('thesis.BA_US_Equity.json');
const HD = load('thesis.HD_US_Equity.mgmt.json');
const BABA = load('thesis.BABA_US_Equity.mgmt.json');
const BA_PLANT = load('mgmt.BA_US_Equity.planted.json');
const CHART = JSON.parse(fs.readFileSync(path.join(FX, 'driverChart.filing.planted.json'), 'utf8'));
const arms = [];

// Arm 1 -- ORDER.
{
  const f = [];
  const cases = [['BA', BA], ['HD', HD], ['BABA', BABA], ['BA-reversed (planted)', Object.assign({}, BA, { management: BA_PLANT })]];
  for (const [label, bundle] of cases) {
    try {
      const h = renderExec(bundle);
      f.push(...orderFaults(rowNames(h), bundle.management).map((x) => label + ': ' + x));
    } catch (e) { f.push(label + ': RENDER: ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['ORDER: the chief executive is row 1 and the CFO row 2 on 3 served rosters and 1 planted reversal, none dropped', f.length === 0,
    f.length === 0 ? '4 of 4 rosters' : f.slice(0, 8).join(' | ')]);
}

// Arm 2 -- NO-SOURCE PROFILE.
{
  const f = [];
  for (const [label, bundle] of [['BA', BA], ['BA planted', Object.assign({}, BA, { management: BA_PLANT })]]) {
    try {
      const h = renderExec(bundle);
      const text = L.textOf(h); // ALL rendered text, closed <details> included: not printed means not printed
      const hits = text.match(/\bno profile\b(?: \((?:no match found|not attempted)\))?|no match found|\bnot attempted\b|\bnot found\b/gi) || [];
      if (hits.length || NO_SOURCE.test(text)) f.push(label + ': ' + hits.length + ' no-source line(s) printed, first "' + hits[0] + '"');
      const matched = (bundle.management.officers || []).filter((o) => o.enrichment === 'MATCHED' && o.profile_url);
      const linked = matched.filter((o) => h.includes('href="' + o.profile_url.replace(/&/g, '&amp;') + '"'));
      if (linked.length !== matched.length) f.push(label + ': ' + linked.length + ' of ' + matched.length + ' MATCHED officers keep their profile link');
    } catch (e) { f.push(label + ': RENDER: ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['NO-SOURCE PROFILE: an officer with no profile prints no line; a matched officer keeps its link', f.length === 0,
    f.length === 0 ? 'BA + BA planted: 0 phrases, links kept' : f.slice(0, 4).join(' | ')]);
}

// Arm 3 -- SYSTEM WORDS.
{
  const f = [];
  try {
    const t = faceText(renderExec(BA));
    if (SYSTEM_WORDS[0][1].test(t)) f.push('Exec: "' + t.match(/[^.]{0,60}in a union of[^.]{0,20}/i)[0].trim() + '"');
  } catch (e) { f.push('Exec RENDER: ' + String(e.message).split('\n')[0]); }
  try {
    const t = faceText(renderThesis(BA));
    if (BA.held_uncited_basis !== 'ABSENT_ON_OBJECT') f.push('INPUT: BA basis is not ABSENT_ON_OBJECT');
    if (SYSTEM_WORDS[1][1].test(t)) f.push('Thesis: "' + t.match(/[^.]{0,60}held back uncited[^.]{0,10}/i)[0].trim() + '"');
  } catch (e) { f.push('Thesis RENDER: ' + String(e.message).split('\n')[0]); }
  try {
    const props = { chart: CHART.chart, driver: CHART.driver, sections: BA.drafted_sections || [] };
    const resolved = (BA.drafted_sections || []).flatMap((s) => (s.sentences || []).flatMap((x) => x.evidence || [])).find((e) => e.id === CHART.resolved_passage_id);
    const control = renderChartForced(props, CHART.resolved_passage_id);
    const reached = !!resolved && L.textOf(control).includes(String(resolved.passage).replace(/\s+/g, ' ').trim().slice(0, 40));
    const inSource = SYSTEM_WORDS[2][1].test(sourceStrings(SA + 'components/ThesisDriverChart.tsx'));
    if (reached) {
      const h = renderChartForced(props, CHART.unresolved_passage_id);
      if (SYSTEM_WORDS[2][1].test(faceText(h))) f.push('Chart: the unresolved passage prints "no served drafted sentence carries this passage..."');
      else if (inSource && !SYSTEM_WORDS[2][1].test(L.textOf(h))) f.push('Chart: UNPROVEN -- the phrase is still in the source but the forced-open render did not reach it');
    } else if (inSource) {
      f.push('Chart: UNPROVEN -- the forced-open control did not reach the passage and the phrase is still in the source');
    }
  } catch (e) { f.push('Chart RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['SYSTEM WORDS: "in a union of", "held back uncited" and "no served drafted sentence carries" are off the face', f.length === 0,
    f.length === 0 ? '3 of 3 strings off the face' : f.join(' | ')]);
}

// Arm 4 -- PLANTED.
{
  const f = [];
  const m = BA.management;
  const alpha = m.officers.map((o) => o.name);
  const good = ['Robert K. Ortberg', 'Jesus Malave, Jr.', ...alpha.filter((n) => n !== 'Robert K. Ortberg' && n !== 'Jesus Malave, Jr.')];
  const segmentFirst = ['D. Christopher Raymond', 'Robert K. Ortberg', 'Jesus Malave, Jr.', ...alpha.filter((n) => !['D. Christopher Raymond', 'Robert K. Ortberg', 'Jesus Malave, Jr.'].includes(n))];
  const cfoLate = ['Robert K. Ortberg', ...alpha.filter((n) => n !== 'Robert K. Ortberg')];
  const dropped = good.slice(0, -1);
  if (orderFaults(good, m).length) f.push('order: a correct order is rejected: ' + orderFaults(good, m)[0]);
  for (const [n, names] of [['alphabetical', alpha], ['segment CEO first', segmentFirst], ['CFO not second', cfoLate], ['one dropped', dropped]]) {
    if (!orderFaults(names, m).length) f.push('order mutant "' + n + '" accepted');
  }
  // SAUX-31 predicate: any rendered occurrence fails, a closed <details> included.
  const td = (x) => '<table><tbody><tr><td>Ann</td><td>' + x + '</td></tr></tbody></table>';
  if (NO_SOURCE.test(L.textOf(td(''))) || NO_SOURCE.test(L.textOf(td('<a href="x">Profile</a>')))) f.push('no-source: a blank or linked cell is rejected');
  for (const [n, x] of [['plain', 'No profile (no match found)'], ['reworded', 'Profile not found'], ['in closed details', '<details><summary>Profile</summary>no match found</details>']]) {
    if (!NO_SOURCE.test(L.textOf(td(x)))) f.push('no-source mutant "' + n + '" accepted');
  }
  // SAUX-30 face predicate: a closed <details> hides its body, an open one does not, its summary is face text.
  const re = SYSTEM_WORDS[0][1];
  if (re.test(faceText('<p>Pool</p><details><summary>How the pool is built</summary><p>in a union of 256</p></details>'))) f.push('face: a closed details body is counted');
  if (!re.test(faceText('<p>the pool 4.08 years in a union of 256.</p>'))) f.push('face mutant "plain line" accepted');
  if (!re.test(faceText('<details open=""><summary>More</summary>in a union of 256</details>'))) f.push('face mutant "open details" accepted');
  if (!re.test(faceText('<details><summary>in a union of 256</summary>x</details>'))) f.push('face mutant "in the summary" accepted');
  arms.push(['PLANTED: 4 order mutants, 3 no-source mutants and 3 face mutants are rejected; the good inputs pass', f.length === 0,
    f.length === 0 ? '10 of 10 mutants rejected, 4 good inputs accepted' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log((ok ? 'ARM PASS' : 'ARM FAIL') + ' ' + n + ' :: ' + d); }
console.log('THE EXEC AND THESIS TABS READ IN PLAIN WORDS: ' + pass + ' of ' + arms.length + ' arms');
process.exit(pass === arms.length ? 0 : 1);
