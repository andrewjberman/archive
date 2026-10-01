/**
 * c14.cjs -- DSGN_AMGTV1 round 13, AV-l-3: THE THREE C14 BLOCKS ARE ONE PLAIN SENTENCE OR FOLDED, AND THE RAW TOKENS ARE GONE
 * (round-12 analysis ruling 3; FWD-11, FWD-20's person-read rejections).
 *
 * Usage (repo root): node <this file>
 * Ruling 3 (the CVO's three C14 rejections of AV-m-1's PNGs, cut): (a) the header's "Description: ABSENT -- no description header
 * scalar ..." becomes one plain sentence ("No company description is on file yet") or nothing; (b) Posture's "FILING EVIDENCE,
 * EACH SIDE" count block folds behind an affordance, never a count block at rest; (c) Exec's "CEO public profile ...: unreadable
 * object -- status=ABSENT query=set absence_class=None." becomes one plain sentence; and with them FWD-11's raw tokens: "PASSAGE
 * P0278" (the Thesis driver chart's passage list) and the ISO "as of 2026-09-24T0310Z" (Peers), which reads as a long-form date.
 * The issuer adds the same class on the same Peers line, seen on walk L: "... CSC column(s), as R-1's map says; ... on R-1".
 * ("derived before C-MODEL-WINDOW-AND-ROWS (5)" is on the Model tab: AV-l-2 owns it.)
 * Fixtures (round13/fixtures, SERVED, captured at the cut): BA US /thesis, /overlay and /peers. ISSUER VARIANTS (labelled, in
 * memory): the header and thesis description blocks set ABSENT with the served-shape reason the round-12 render showed.
 * Arms:
 *   1  descriptions: a header description ABSENT with its reason reads no "Description: ABSENT", no "CIE_DES", no "scalar" -- one
 *      plain sentence or nothing -- and the thesis description block the same; the served BA header description still shows
 *      (control)
 *   2  Exec and Peers and the driver chart: BA's Exec tab shows no "unreadable object", "status=", "query=" or "absence_class";
 *      BA's Peers tab shows no raw ISO stamp, no "R-1" and no "CSC", and its as-of reads as a long-form date; BA's Thesis tab
 *      shows no "PASSAGE P####" token
 *   3  Posture: BA's "Filing evidence, each side" counts ("N drafted sentences, N evidence records ...") are not visible at rest
 *      (they sit behind a closed affordance), while the verdict card and the numbered reasons still show (control)
 * Prints one line per arm and "C14 BLOCKS CUT, RAW TOKENS GONE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const SA = 'src/pages/SecurityAnalysis/';
const K = 'BA_US_Equity';
const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const overlay = S.unwrap(L.fixture('overlay.BA_US_Equity.json'));
const peers = S.unwrap(L.fixture('peers.BA_US_Equity.json'));
S.bundles[K] = thesis;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => S.bundles[k],
  usePeerSet: (k) => (k === K ? peers : undefined),
  useManagement: (k) => (S.bundles[k] || {}).management,
  useModelVersions: () => undefined,
  useModelCompare: () => undefined,
  useInputLedger: () => undefined,
});
const r = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + e.message; } };
const atRest = (html) => unesc(L.textOf(String(html).replace(/<details(?![^>]*\bopen\b)[^>]*>[\s\S]*?<\/details>/g, '')));
const header = (ov) => r(() => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} }); });
const tab = (file, name) => r(() => L.render(L.source(SA + file)[name], { securityKey: K }));
const DESC_REASON = "no description header scalar ['CIE_DES', 'CIE_DES_BULK'] on the model block (14 header scalar(s) measured) and no served D-1 company_description sentence passing the describes-the-business test (drafting_status SERVED)";

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const ovAbsent = clone(overlay); ovAbsent.description = { status: 'ABSENT', text: null, reason: DESC_REASON };
const hA = atRest(header(ovAbsent));
for (const bad of [/Description: ABSENT/, /CIE_DES/, /scalar/i, /drafting_status/]) if (bad.test(hA)) { f1.push(`header with an ABSENT description shows ${bad}`); break; }
const thA = clone(thesis);
let thesisPlanted = 0;
const plant = (o) => { if (!o || typeof o !== 'object') return; for (const v of Object.values(o)) { if (v && typeof v === 'object' && 'description_verdict_state' in v) { v.description_verdict_state = 'ABSENT'; v.description_verdict_reason = DESC_REASON; thesisPlanted += 1; } plant(v); } };
plant(thA);
S.bundles[K] = thA;
const tA = atRest(tab('tabs/ThesisTab.tsx', 'ThesisTab'));
S.bundles[K] = thesis;
if (thesisPlanted && /Description: ABSENT|CIE_DES|drafting_status/.test(tA)) f1.push('the Thesis description block with an ABSENT verdict shows the raw reason');
const hS = atRest(header(overlay));
const served = overlay.description && overlay.description.text ? overlay.description.text.slice(0, 40) : null;
if (served && !hS.includes(served)) f1.push('the served BA header description no longer shows (control)');
const a1 = f1.length === 0;
const a1d = a1 ? `an ABSENT description reads as a plain sentence or nothing (header, and ${thesisPlanted} thesis block(s)); the served description still shows` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const ex = atRest(tab('tabs/ExecManagementTab.tsx', 'ExecManagementTab'));
for (const bad of [/unreadable object/i, /status=/, /query=/, /absence_class/]) if (bad.test(ex)) f2.push(`Exec shows ${bad}: "${(new RegExp('[^.]*' + bad.source + '[^.]*', bad.flags).exec(ex) || [''])[0].trim().slice(0, 100)}"`);
const pe = atRest(tab('tabs/PeersTab.tsx', 'PeersTab'));
if (/\b\d{4}-\d{2}-\d{2}T\d{2}:?\d{2}(:?\d{2})?Z\b/.test(pe)) f2.push(`Peers shows a raw ISO stamp: "${/\b\d{4}-\d{2}-\d{2}T[\dZ:]+/.exec(pe)[0]}"`);
if (/\bR-1\b/.test(pe)) f2.push('Peers shows "R-1"');
if (/\bCSC\b/.test(pe)) f2.push('Peers shows "CSC"');
if (peers.as_of && !/\bas of [A-Z][a-z]+ \d{1,2}(st|nd|rd|th), \d{4}/.test(pe)) f2.push('Peers does not read its as-of as a long-form date');
const th = atRest(tab('tabs/ThesisTab.tsx', 'ThesisTab'));
if (/PASSAGE P\d+|\bP\d{4}\b/.test(th)) f2.push(`Thesis shows a passage id: "${/PASSAGE P\d+|\bP\d{4}\b/.exec(th)[0]}"`);
const a2 = f2.length === 0;
const a2d = a2 ? 'Exec shows no reading-machine tokens; Peers no raw stamp, no R-1, no CSC, its as-of in long form; Thesis no passage id' : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const poHtml = tab('tabs/PostureTab.tsx', 'PostureTab');
const po = atRest(poHtml);
if (/\d+ drafted sentences?, \d+ evidence records?/i.test(po)) f3.push(`Posture shows the count block at rest: "${(/[^.]*\d+ drafted sentences?, \d+ evidence records?[^.]*/i.exec(po) || [''])[0].trim().slice(0, 100)}"`);
if (!/\d+ drafted sentences?, \d+ evidence records?/i.test(unesc(L.textOf(poHtml)))) f3.push('the count block is gone entirely (it must fold, not vanish)');
if (!/HOLD|BUY|SELL|NO CALL|TRIM|ADD/.test(po)) f3.push('the verdict card is not visible (control)');
if (!/Reasons, each beside/i.test(po)) f3.push('the numbered reasons are not visible (control)');
const a3 = f3.length === 0;
const a3d = a3 ? "BA's filing-evidence counts sit behind a closed affordance; the verdict card and reasons still show" : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['an absent description is one plain sentence or nothing', a1, a1d],
  ['no reading-machine tokens on Exec, Peers or the driver chart', a2, a2d],
  ['the Posture count block folds, never at rest', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`C14 BLOCKS CUT, RAW TOKENS GONE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
