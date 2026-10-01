/**
 * dossier.cjs -- DSGN_AMGTV1 round 13, AV-l-1: THE PAGE READS THE SERVED PER-FIELD DOSSIER REASON, AND NEVER CLAIMS A RESEARCH PACK
 * THAT DOES NOT EXIST; THE CONTRACT FIXTURES ARE THE LIVE SHAPES (round-12 analysis ruling 1; FWD-11; AMGT_CORPUS's six).
 *
 * Usage (repo root): node <this file>
 * Ruling 1: AMGT_RESAPP ab-2 (ratified) serves a no-dossier name as the full `dossier_fields` block, each field ABSENT with its
 * reason (`thesis_pillars_absent: {status: ABSENT, reason}`, and `{status: ABSENT, value: null, reason}` on fund_of_record,
 * last_stated_position, management, pack_shape); a top-level `{status, reason}` appears only on a failed read. The page keyed its
 * sentences on the top-level `dossier.status`, so every no-dossier name read "none are stated in the research team's pack" --
 * asserting a pack that does not exist. "none are stated in the research team's pack" is reachable ONLY when a dossier exists and
 * states none. And the ui-contract fixture set is refreshed from the LIVE served shapes, so the next shape move fails a test.
 * Fixtures (round13/fixtures, SERVED, captured at the cut by capture_r13.py; scoped API CodeSha256 nKWCfQRQ..., LastModified
 * 2026-09-30T11:43:22Z): /thesis for 6501 JP (no dossier: every field "no research dossier exists for this name"), BA US (a
 * dossier, no class-A report: pillars "no class A report for this security"), IMB LN (6 served pillars, fund IDVZ); the BA routes
 * the contract fixture set keys. ISSUER VARIANTS (labelled, in memory): a top-level READ_FAILED dossier; a dossier that exists
 * (pack_shape SERVED) and states no pillars.
 * Arms:
 *   1  the live no-dossier name (6501 JP): its Thesis pillars line, the header's fund line, the Posture fund line and the Exec
 *      management line each say there is no research dossier for the name (the served reason, in words), and none of the four
 *      surfaces says "research team's pack"
 *   2  every served shape reads right: IMB's 6 served pillars are listed; BA's ABSENT pillars read their served reason; a planted
 *      top-level READ_FAILED reads a designed sentence with its reason and no status token; and "none are stated in the research
 *      team's pack" appears for the planted dossier that exists and states none -- and only there
 *   3  the contract fixtures are the live shapes: each of the 10 keyed routes in
 *      portal/src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json deep-equals the issuer's live capture, and the
 *      Thesis tab rendered from the fixture's own BA /thesis reads BA's served pillars reason
 * Prints one line per arm and "THE PAGE READS THE SERVED DOSSIER REASON: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const SA = 'src/pages/SecurityAnalysis/';
const K6501 = '6501_JP_Equity';
const PACK = /research team.s pack/i;
const NONE_STATED = /none are stated in the research team.s pack/i;
const NO_DOSSIER = /no research dossier/i;

const live = {};
for (const k of [K6501, 'BA_US_Equity', 'IMB_LN_Equity']) live[k] = S.unwrap(L.fixture(`thesisBundle.${k}.json`));
const liveOverlay6501 = S.unwrap(L.fixture('overlay.6501_JP_Equity.json'));
const text = (html) => unesc(L.textOf(html));
const attrText = (html, attr) => text(L.innerOf(html, attr) || '');
function surfaces(key, bundle, overlay) {
  const saved = S.bundles[key];
  S.bundles[key] = bundle;
  const r = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + e.message; } };
  const out = {
    thesis: r(() => L.render(L.source(SA + 'tabs/ThesisTab.tsx').ThesisTab, { securityKey: key })),
    posture: r(() => L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: key })),
    exec: r(() => L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: key })),
    header: overlay ? r(() => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: overlay, onBack: () => {}, onRefresh: () => {} }); }) : '',
  };
  S.bundles[key] = saved;
  return out;
}
const pillarsLine = (html) => attrText(html, 'data-dossier-pillars');

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const s1 = surfaces(K6501, live[K6501], liveOverlay6501);
if (!NO_DOSSIER.test(pillarsLine(s1.thesis))) f1.push(`6501 Thesis pillars line reads "${pillarsLine(s1.thesis).slice(0, 120)}"`);
const fundLine = (html) => (/[^.]*fund of record[^.]*\./i.exec(text(html)) || [''])[0];
if (!NO_DOSSIER.test(fundLine(s1.header))) f1.push(`6501 header fund line reads "${fundLine(s1.header).slice(0, 120)}"`);
if (!NO_DOSSIER.test(fundLine(s1.posture))) f1.push(`6501 Posture fund line reads "${fundLine(s1.posture).slice(0, 120)}"`);
const mgmt = attrText(s1.exec, 'data-dossier-management');
if (!NO_DOSSIER.test(mgmt)) f1.push(`6501 Exec management line reads "${mgmt.slice(0, 120)}"`);
for (const [n, h] of Object.entries(s1)) if (PACK.test(text(h))) f1.push(`6501 ${n}: "${(/[^.]*research team.s pack[^.]*/i.exec(text(h)) || [''])[0].trim().slice(0, 110)}"`);
const a1 = f1.length === 0;
const a1d = a1 ? `6501's Thesis, header, Posture and Exec each say there is no research dossier; 0 "research team's pack" claims` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const imb = surfaces('IMB_LN_Equity', live.IMB_LN_Equity, null);
const imbPillars = live.IMB_LN_Equity.dossier_fields.thesis_pillars;
const imbItems = (L.innerOf(imb.thesis, 'data-dossier-pillars') || '').match(/<li\b/g) || [];
if (!/data-dossier-pillars="SERVED"/.test(imb.thesis) || imbItems.length < imbPillars.length) f2.push(`IMB: ${imbItems.length} pillar items rendered, want ${imbPillars.length} (SERVED)`);
const ba = surfaces('BA_US_Equity', live.BA_US_Equity, null);
const baReason = live.BA_US_Equity.dossier_fields.thesis_pillars_absent.reason;
if (!pillarsLine(ba.thesis).toLowerCase().includes(baReason.toLowerCase())) f2.push(`BA pillars line "${pillarsLine(ba.thesis).slice(0, 120)}" does not carry its served reason "${baReason}"`);
if (NONE_STATED.test(text(ba.thesis))) f2.push('BA (no class-A report) reads "none are stated in the research team\'s pack"');
const failed = clone(live[K6501]); failed.dossier_fields = { status: 'READ_FAILED', reason: 'the dossier read did not complete' };
const sf = surfaces(K6501, failed, null);
if (!/did not complete/i.test(pillarsLine(sf.thesis))) f2.push(`READ_FAILED pillars line reads "${pillarsLine(sf.thesis).slice(0, 120)}"`);
for (const [n, h] of Object.entries(sf)) if (/READ_FAILED/.test(text(h))) f2.push(`READ_FAILED ${n}: a raw status token in visible text`);
if (NONE_STATED.test(text(sf.thesis))) f2.push('READ_FAILED reads "none are stated in the research team\'s pack"');
const stated = clone(live.IMB_LN_Equity); stated.dossier_fields.thesis_pillars = []; delete stated.dossier_fields.thesis_pillars_absent;
const ss = surfaces('IMB_LN_Equity', stated, null);
if (!NONE_STATED.test(pillarsLine(ss.thesis))) f2.push(`a dossier that states no pillars reads "${pillarsLine(ss.thesis).slice(0, 120)}" (want "none are stated in the research team's pack")`);
const a2 = f2.length === 0;
const a2d = a2 ? `IMB's ${imbPillars.length} pillars listed; BA reads "${baReason}"; READ_FAILED reads its reason, no token; "none are stated" only for the dossier that states none` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const FIX = path.join(process.cwd(), 'portal', SA, '__harness__/tests/uiContractFixtures.json');
let fix = null;
try { fix = JSON.parse(fs.readFileSync(FIX, 'utf8')); } catch (e) { f3.push('uiContractFixtures.json unreadable: ' + e.message); }
const P = '/api/scoped/amgt';
const MAP = {
  [`${P}/security/BA_US_Equity/thesis`]: 'thesisBundle.BA_US_Equity.json',
  [`${P}/security/BA_US_Equity/overlay`]: 'overlay.BA_US_Equity.json',
  [`${P}/security/BA_US_Equity/peers`]: 'peers.BA_US_Equity.json',
  [`${P}/security/BA_US_Equity/versions`]: 'versions.BA_US_Equity.json',
  [`${P}/security/BA_US_Equity/compare`]: 'compare.BA_US_Equity.oldest-latest.json',
  [`${P}/security/BA_US_Equity/ledger`]: 'ledger.BA_US_Equity.json',
  [`${P}/security/BA_US_Equity/timeline`]: 'timeline.BA_US_Equity.json',
  [`${P}/watchlist`]: 'watchlist.json',
  [`${P}/lead-panel/rankings/trending/chatter`]: 'rankings.trending.chatter.json',
  [`${P}/lead-panel/timeseries/trending/chatter`]: 'timeseries.trending.chatter.json',
};
let equal = 0;
if (fix) {
  for (const [key, file] of Object.entries(MAP)) {
    const want = S.unwrap(L.fixture(file));
    if (!(key in fix)) f3.push(`the fixture set has no key ${key}`);
    else if (JSON.stringify(fix[key]) !== JSON.stringify(want)) f3.push(`${key} differs from the live capture ${file}`);
    else equal += 1;
  }
  const fb = fix[`${P}/security/BA_US_Equity/thesis`];
  if (fb && fb.dossier_fields) {
    const sb = surfaces('BA_US_Equity', fb, null);
    const r = (fb.dossier_fields.thesis_pillars_absent || {}).reason || '';
    if (!r || !pillarsLine(sb.thesis).toLowerCase().includes(r.toLowerCase())) f3.push(`the Thesis tab from the fixture's BA /thesis reads "${pillarsLine(sb.thesis).slice(0, 100)}"`);
  } else f3.push("the fixture's BA /thesis carries no dossier_fields");
}
const a3 = f3.length === 0;
const a3d = a3 ? `${equal} of ${Object.keys(MAP).length} keyed routes equal the live captures; the Thesis tab from the fixture's BA /thesis reads its served reason` : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['the live no-dossier name says so on all four surfaces, never a pack', a1, a1d],
  ['every served shape reads right; "none are stated" only where a dossier states none', a2, a2d],
  ['the contract fixtures are the live shapes, and the reader reads them', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`THE PAGE READS THE SERVED DOSSIER REASON: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
