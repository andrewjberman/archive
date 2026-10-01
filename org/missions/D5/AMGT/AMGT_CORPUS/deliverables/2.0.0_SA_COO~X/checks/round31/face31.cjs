/**
 * face31.cjs -- AMGT_CORPUS round 31, CRPS-ag-1 (issuer direct act): NOTHING ON THE MODEL TAB PRESUPPOSES A RESEARCH PACK
 * (round-30 analysis @500c40ecb2 ruling 1; the round-30 footer treatment).
 *
 * Usage (repo root): node <this file>
 * Method: STATIC, DSGN's read-only loader on BA's served /thesis capture (in which BA's DPS still reads refused, so the
 * refused-row sentence is on the face) and in-memory variants. "pack" may appear only inside a SERVED team case
 * (data-model-team-case-state="SERVED": the team's own workbook is then real and cited). Arms:
 *   1  BA SERVED face: no "pack" outside a served team case; the growth-rows line still says the page computes no growth rows
 *   2  BA ABSENT face (model_status ABSENT): no "pack" outside a served team case
 *   3  REGRESSION: round 30's face30.cjs reads 4 of 4
 *   4  HISTORY: an ABSENT model with history served heads the compare block as history and says no "pack" (k-5, re-anchored)
 * Prints one line per arm and "NOTHING PRESUPPOSES A PACK: <k> of 4 arms"; exit 0 only at 4 of 4. No network, writes nothing.
 */
const path = require('path');
const { spawnSync } = require('child_process');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const R30 = path.join(process.cwd(), 'org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round30/face30.cjs');
const L = require(path.join(DSGN, '_load.cjs'));
const S = require(path.join(DSGN, 'surfaces.cjs'));
const K = 'BA_US_Equity';
const clone = (x) => JSON.parse(JSON.stringify(x));
const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
let T = thesis;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === K ? T : (S.bundles[k] || undefined)),
  useModelVersions: () => undefined,
  useModelCompare: () => undefined,
  useInputLedger: () => undefined,
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = (b) => { T = b; try { return MT ? L.render(MT.ModelTab, { securityKey: K }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };
// strip every served team-case section (the team's pack is real there), then look for "pack"
const outsideServedTeamCases = (h) => h.replace(/<section[^>]*data-model-team-case-state="SERVED"[\s\S]*?<\/section>/g, '');
const results = [];
const arm = (n, name, fails) => { results.push(fails.length === 0); console.log(`ARM ${n} ${name}: ${fails.length === 0 ? 'PASS' : 'FAIL -- ' + fails.join('; ')}`); };
const packHits = (h) => (L.textOf(outsideServedTeamCases(h)).match(/[^.]{0,40}\bpacks?\b[^.]{0,30}/gi) || []);

{
  const f = [];
  const h = render(clone(thesis));
  if (!h || /^RENDER FAILED/.test(h)) f.push('did not render');
  else {
    const hits = packHits(h);
    if (hits.length) f.push(`${hits.length} "pack" phrase(s): ${hits.slice(0, 3).map((x) => `"${x.trim()}"`).join(' | ')}`);
    if (!/computes none|no year-on-year growth/i.test(L.textOf(h))) f.push('the growth-rows line no longer says the page computes no growth rows');
  }
  arm(1, 'BA served face presupposes no pack', f);
}
{
  const f = [];
  const h = render(Object.assign(clone(thesis), { model_status: 'ABSENT' }));
  const hits = packHits(h);
  if (hits.length) f.push(`${hits.length} "pack" phrase(s): ${hits.slice(0, 3).map((x) => `"${x.trim()}"`).join(' | ')}`);
  arm(2, 'BA absent face presupposes no pack', f);
}
{
  const f = [];
  const r = spawnSync(process.execPath, [R30], { encoding: 'utf8', cwd: process.cwd() });
  if (r.status !== 0 || !(r.stdout || '').includes('THE MODEL FOOTER READS NEUTRAL: 4 of 4 arms')) f.push(`face30.cjs reads "${((r.stdout || '').trim().split('\n').pop() || '').slice(0, 80)}"`);
  arm(3, "round 30's check still passes", f);
}
// 4 HISTORY (k-5's agreement, re-anchored here: DSGN's frozen round-14 modelhistory.cjs anchors the pre-round-28 empty sentence
// "No model in the research pack ...", which CRPS-ad-3 replaced): latest ABSENT with history served -> the compare block is
// headed as history, and no "pack" on the face
{
  const f = [];
  const versions = S.unwrap(L.fixture('versions.BA_US_Equity.json'));
  const compare = S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json'));
  L.hookState.impl = Object.assign({}, L.hookState.impl, { useModelVersions: () => versions, useModelCompare: () => compare });
  const h = render(Object.assign(clone(thesis), { model_status: 'ABSENT' }));
  const inner = L.innerOf(h, 'data-model-compare', '');
  if (inner === null) f.push('no compare block on the ABSENT face with history served');
  else {
    const head = L.textOf((/<p[^>]*>([\s\S]*?)<\/p>/.exec(inner) || [, ''])[1]);
    if (!/\b(earlier|previous|prior|past|older)\b[^.]*\bversions?\b|\bhistory\b|\bhistorical\b/i.test(head)) f.push(`the compare block is headed "${head}", not as history`);
  }
  const hits = packHits(h);
  if (hits.length) f.push(`${hits.length} "pack" phrase(s): ${hits.slice(0, 3).map((x) => `"${x.trim()}"`).join(' | ')}`);
  arm(4, 'absent model with history: headed as history, no pack', f);
}
const k = results.filter(Boolean).length;
console.log(`NOTHING PRESUPPOSES A PACK: ${k} of 4 arms`);
process.exit(k === 4 ? 0 : 1);
