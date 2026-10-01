/**
 * packwords.cjs -- DSGN_AMGTV1 round 15, the BA pack split: THE PACK SENTENCES READ THEIR OWN REASON
 * (round-14 analysis section 3 row 5, ruling 2, as narrowed by the issuer after CONTRACT amendment 1 @c7f9fa44fa: the Model
 * face -- ModelTab.tsx, k-5 -- belongs to AMGT_CORPUS until the Friday freeze and is NOT graded here; L9 record
 * ADJUDICATION_v16.md section 2; FWD-11).
 *
 * Usage (repo root): cd "$(git rev-parse --show-toplevel)" && node <this file>
 * `portal/` under the working directory is the checkout under test. The BASE negative is a PINNED BASE RENDER: the same
 * invocation from the shared repo root, whose portal/ is DEV b336b141 with a clean tree; the header line prints the checkout's
 * HEAD and its count of modified files under src/pages/SecurityAnalysis, so every run line names the bytes it graded.
 *
 * WHAT WAS MEASURED (served BA /thesis, round14/fixtures/thesisBundle.BA_US_Equity.json, and the producer):
 *   - Thesis  served dossier_fields.thesis_pillars_absent.reason "no class A report for this security"
 *             page "The research team's thesis pillars: no research pack for this security." -- reasonWords.ts maps
 *             "class A report" -> "research pack": the served fact re-worded, no presupposition added (page word: "research
 *             pack" for "class A report"; heading "The research team's thesis pillars" is the page's)
 *   - Exec    served dossier_fields.management.reason "no MANAGEMENT section in class A missing or class B missing"
 *             (lib/research/corpus/dossier.py:381 `"no %s section in class A %s or class B %s" % (label, label_a, label_b)`,
 *             each label = the picked report's date or "missing": here BOTH reports are missing)
 *             page "The research team on management: no management section in the research pack or the earnings update."
 *             -- reasonWords.ts:26 rewrites "in class A missing or class B missing" to "in the research pack or the earnings
 *             update", DROPPING both "missing" words: the PAGE adds a pack the served reason says is missing
 *   The served pack reasons AGREE (thesis_pillars_absent, management, pack_shape and the three model.team_cases reasons all say
 *   no class-A report); arm 3 prints that tally on every run, so a disagreement surfaces as a row to the writer, never as a
 *   page-side reconciliation.
 *
 * Method: STATIC -- the real ThesisTab / ExecManagementTab sources rendered with the installed react-dom/server (loader
 * _load.cjs; recharts, react-query and the api client stubbed as round14/checks/surfaces.cjs does). Page hooks:
 * useThesisBundle -> the bundle the arm sets; useManagement -> its `management`; useModelVersions/useModelCompare/
 * useInputLedger/usePeerSet -> undefined.
 * Inputs (round14/fixtures, SERVED read-only captures): thesisBundle for BA_US_Equity, VLO_US_Equity, 992_HK_Equity (the same
 * pack-absent reasons as BA) and 6501_JP_Equity (a reason naming no pack: "no research dossier exists for this name").
 * ISSUER PLANTS (in memory, labelled): pack-PRESENT reasons on a copy of BA (see arm 2).
 *
 * DEFINITIONS:
 *   PACK SENTENCE  Thesis: visible text of [data-dossier-pillars]; Exec: visible text of [data-dossier-management]
 *   OWN REASON     Thesis: dossier_fields.thesis_pillars_absent.reason; Exec: dossier_fields.management.reason
 *   PACK-ABSENT    an own reason matching PACK_ABSENT_RE ("no class A ...", "class A missing")
 *   NAMES NO PACK  an own reason matching neither "class A" nor "pack"
 *   PRESUPPOSES    PRESUPPOSE_RE: "in/from/of/on the|this|a (research) pack", "the pack carries/holds/has", "<x>'s pack"
 *   SAYS NONE      SAYS_NONE_RE: a negation (no / neither / nor / without) before "research pack" in the same sentence
 *   A sentence READS ITS OWN REASON when: PACK-ABSENT -> it does not PRESUPPOSE and it SAYS NONE; NAMES NO PACK -> it carries
 *   no "pack" word at all; otherwise (a pack-present reason) no constraint beyond arm 2's function test.
 * Arms:
 *   1  BA: the Thesis and Exec pack sentences each read their own served reason
 *   2  FUNCTION + CONTROLS: a pack-present plant of each own reason moves each sentence (the sentence is a function of its own
 *      reason, not a constant); VLO and 992 HK (served, the same pack-absent reasons) read their own reasons; 6501 JP (served,
 *      a reason naming no pack) prints no pack word on either sentence
 *   3  DETECTOR + AGREEMENT: the predicate REJECTS the base Exec wording and a planted presupposing Thesis sentence spliced
 *      into BA's rendered face, and ACCEPTS the served Thesis wording; prints the served-reason agreement tally (6 BA reasons)
 * Prints one line per arm and "THE PACK SENTENCES READ THEIR OWN REASON: <k> of 3 arms"; exit 0 only at 3 of 3.
 * Measured wall time: 0.7 s at the base, 0.6 s on the green arm (in-process; ~1 s with node start-up; site Z).
 * No network, no AWS, writes no file (git is read once for the header line).
 */
const t0 = Date.now();
const L = require('./_load.cjs');
const React = L.React;
const { spawnSync } = require('child_process');

const SA = 'src/pages/SecurityAnalysis/';
const BA = 'BA_US_Equity';
const clone = (x) => JSON.parse(JSON.stringify(x));
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => unesc(L.textOf(html || ''));

// ---- the checkout under test, named ------------------------------------------------------------------------------------------
const git = (args) => { const r = spawnSync('git', ['-C', L.base, ...args], { encoding: 'utf8' }); return r.status === 0 ? r.stdout.trim() : `git rc=${r.status}`; };
const head = git(['rev-parse', '--short=8', 'HEAD']);
const dirty = git(['status', '--porcelain', '--', 'src/pages/SecurityAnalysis']).split('\n').filter(Boolean).length;
console.log(`CHECKOUT portal@${head}, ${dirty} modified file(s) under src/pages/SecurityAnalysis`);

// ---- stubs (as round14/checks/surfaces.cjs) ----------------------------------------------------------------------------------
const rcCache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!rcCache[k]) { const C = (p) => React.createElement('div', { 'data-rc': k }, (p || {}).children); C.displayName = k; rcCache[k] = C; }
    return rcCache[k];
  },
}));
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }),
});
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);

// ---- fixtures and hooks ------------------------------------------------------------------------------------------------------
const live = {};
for (const k of [BA, 'VLO_US_Equity', '992_HK_Equity', '6501_JP_Equity']) live[k] = unwrap(L.fixture(`thesisBundle.${k}.json`));
let T = null;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: () => T,
  useManagement: () => (T || {}).management,
  useModelVersions: () => undefined,
  useModelCompare: () => undefined,
  useInputLedger: () => undefined,
  usePeerSet: () => undefined,
});
const tab = (file, name) => { try { return L.source(SA + 'tabs/' + file)[name]; } catch (e) { return { error: e.message }; } };
const TABS = { thesis: tab('ThesisTab.tsx', 'ThesisTab'), exec: tab('ExecManagementTab.tsx', 'ExecManagementTab') };
function render(which, key, bundle) {
  const C = TABS[which];
  if (!C || C.error) return 'RENDER FAILED ' + (C && C.error);
  T = bundle;
  try { return L.render(C, { securityKey: key }); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } finally { T = null; }
}

// ---- the predicate -----------------------------------------------------------------------------------------------------------
const PRESUPPOSE_RE = /\b(?:in|from|of|on|inside)\s+(?:the|this|that|its|a)\s+(?:research\s+)?pack\b|\b(?:the|this)\s+(?:research\s+)?pack\s+(?:carries|holds|has|says|states)\b|\b\w+'s\s+pack\b/i;
const SAYS_NONE_RE = /\b(?:no|neither|nor|without)\b[^.]*\bresearch pack\b/i;
const PACK_WORD_RE = /\bpack\b/i;
const NAMES_PACK_RE = /\bclass[- ]?A\b|\bpack\b/i;
const PACK_ABSENT_RE = /\bno class[- ]?A\b|\bclass[- ]A missing\b/i;

const SENT = {
  thesis: { attr: 'data-dossier-pillars', reason: (b) => (b.dossier_fields.thesis_pillars_absent || {}).reason },
  exec: { attr: 'data-dossier-management', reason: (b) => (b.dossier_fields.management || {}).reason },
};
const lineOf = (which, html) => text(L.innerOf(html, SENT[which].attr) || '');

/** Faults for one sentence against its own served reason (empty array = it reads its own reason). */
function readsOwn(label, line, reason) {
  const out = [];
  if (!line) return [`${label}: no sentence rendered`];
  if (!NAMES_PACK_RE.test(reason || '')) {
    if (PACK_WORD_RE.test(line)) out.push(`${label}: "${line}" names a pack; its served reason "${reason}" names none`);
  } else if (PACK_ABSENT_RE.test(reason)) {
    const p = PRESUPPOSE_RE.exec(line);
    if (p) out.push(`${label}: "${line}" presupposes a pack ("${p[0]}"); its served reason "${reason}" says class A is missing`);
    if (!SAYS_NONE_RE.test(line)) out.push(`${label}: "${line}" does not say there is no research pack (served "${reason}")`);
  }
  return out;
}
function gradeName(key, bundle, prefix) {
  const faults = [];
  const lines = {};
  for (const which of Object.keys(SENT)) {
    const h = render(which, key, bundle);
    if (/^RENDER FAILED/.test(h)) { faults.push(`${prefix}${which}: ${h.slice(0, 100)}`); continue; }
    lines[which] = lineOf(which, h);
    faults.push(...readsOwn(`${prefix}${which}`, lines[which], SENT[which].reason(bundle)));
  }
  return { faults, lines };
}

// ---- arm 1: BA -------------------------------------------------------------------------------------------------------------
const g1 = gradeName(BA, live[BA], 'BA ');
const a1 = g1.faults.length === 0;
const a1d = a1
  ? `Thesis "${g1.lines.thesis}" | Exec "${g1.lines.exec}" -- 2 of 2 read their own served reason`
  : `${g1.faults.length} failing; ${g1.faults.join(' | ')}`;

// ---- arm 2: function of the own reason + served controls ---------------------------------------------------------------------
const f2 = [];
const B = clone(live[BA]);
B.dossier_fields.thesis_pillars_absent.reason = 'no THESIS PILLARS section in class A 2026-05-01'; // ISSUER PLANT (pack present)
B.dossier_fields.management.reason = 'no MANAGEMENT section in class A 2026-05-01 or class B missing'; // lib/research/corpus/tests/test_dossier.py:201
for (const which of Object.keys(SENT)) {
  const lb = lineOf(which, render(which, BA, B));
  if (!lb) f2.push(`plant ${which}: no sentence`);
  else if (lb === g1.lines[which]) f2.push(`plant ${which}: the sentence did not move when its served reason did ("${lb}")`);
}
const ctl = {};
for (const k of ['VLO_US_Equity', '992_HK_Equity', '6501_JP_Equity']) {
  const g = gradeName(k, live[k], k.split('_')[0] + ' ');
  ctl[k] = g.lines;
  f2.push(...g.faults);
}
const a2 = f2.length === 0;
const a2d = a2
  ? `pack-present plants move 2 of 2 sentences; VLO and 992 HK read their own pack-absent reasons on 4 of 4 sentences; 6501 Thesis "${ctl['6501_JP_Equity'].thesis}" / Exec "${ctl['6501_JP_Equity'].exec}" name no pack`
  : `${f2.length} failing; ${f2.slice(0, 3).join(' | ')}`;

// ---- arm 3: detector + served agreement ----------------------------------------------------------------------------------------
const f3 = [];
const execReason = live[BA].dossier_fields.management.reason;
const thesisReason = live[BA].dossier_fields.thesis_pillars_absent.reason;
const BASE_EXEC = 'The research team on management: no management section in the research pack or the earnings update.';
if (readsOwn('probe', BASE_EXEC, execReason).length === 0) f3.push('the base Exec wording is ACCEPTED');
if (readsOwn('probe', "The research team's thesis pillars: no research pack for this security.", thesisReason).length !== 0) f3.push('the served Thesis wording is REJECTED');
const hThesis = render('thesis', BA, live[BA]);
const inner = L.innerOf(hThesis, 'data-dossier-pillars');
if (inner === null) f3.push('no Thesis pillars element to splice into');
else {
  const spliced = hThesis.replace(inner, "The research team's thesis pillars: none are stated in the research team's pack.");
  if (readsOwn('splice', lineOf('thesis', spliced), thesisReason).length === 0) f3.push('a planted presupposing Thesis sentence spliced into the face is ACCEPTED');
}
const d = live[BA].dossier_fields;
const tc = (live[BA].model && live[BA].model.team_cases) || {};
const packReasons = [
  ['thesis_pillars_absent', d.thesis_pillars_absent && d.thesis_pillars_absent.reason],
  ['management', d.management && d.management.reason],
  ['pack_shape', d.pack_shape && d.pack_shape.reason],
  ...['base', 'upside', 'downside'].map((s) => [`model.team_cases.${s}`, tc[s] && tc[s].reason]),
].filter(([, r]) => r);
const PACK_NONE_RE = /\bno class[- ]?A\b|\bclass[- ]A missing\b|\bno class-A or class-B report\b/i;
const agree = packReasons.filter(([, r]) => PACK_NONE_RE.test(r)).length;
const agreement = agree === packReasons.length
  ? `served BA pack reasons AGREE: ${agree} of ${packReasons.length} say no class-A report`
  : `served BA pack reasons DISAGREE: ${agree} of ${packReasons.length} say no class-A report (${packReasons.filter(([, r]) => !PACK_NONE_RE.test(r)).map(([k]) => k).join(', ')} do not) -> a row to the writer`;
const a3 = f3.length === 0;
const a3d = a3
  ? `base Exec wording REJECTED, spliced presupposing Thesis sentence REJECTED, served Thesis wording ACCEPTED; ${agreement}`
  : `${f3.length} failing; ${f3.join(' | ')}; ${agreement}`;

const arms = [
  ["BA's Thesis and Exec pack sentences read their own served reason", a1, a1d],
  ['each sentence is a function of its own reason; served controls', a2, a2d],
  ['the detector rejects the base wording; served-reason agreement', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`wall ${((Date.now() - t0) / 1000).toFixed(1)} s`);
console.log(`THE PACK SENTENCES READ THEIR OWN REASON: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
