/**
 * evidence.cjs -- DSGN_AMGTV1 round 11, AV-n-2: THE POSTURE TAB'S EVIDENCE WORDING NAMES WHICH EVIDENCE IT MEANS AND WHICH IS
 * ABSENT (round-10 analysis ruling 3; FWD-11).
 *
 * Usage (repo root): node <this file>
 * IMB's Posture tab (walk J shot 169) put two "packs" side by side: the evidence-coverage lines read "IMB LN (subject): no pack for
 * IMB_LN_Equity is carried in packs on this object", while the position line above reads the research team's pack. Ruled: the
 * evidence-coverage lines refer to AMGT_RESAPP's FILING EVIDENCE and say so; the position line keeps "the research team's pack";
 * "no pack is carried in packs on this object" becomes a sentence a PM can read, naming which evidence is absent. Renders
 * tabs/PostureTab.tsx (surfaces.cjs) on the SERVED /thesis of VLO, INTU and SAP GY (filing evidence carried), 992 HK and IMB LN (none
 * carried) and AZN LN.
 * Arms:
 *   1  the evidence section names the filing evidence: on every Posture tab that renders an evidence-coverage section, the section
 *      (from its heading to the "Reasons" heading) and the citation footer name "filing evidence" (or "filings"), and carry no
 *      "pack" / "packs" / "research pack" / "research team's pack" -- the research team's pack is not this evidence
 *   2  no machine words: no Posture tab of the walked names shows "on this object", "carried in packs", or a raw security key
 *      (`<CODE>_<XX>_Equity`) in visible text; an absent side (992 HK, IMB LN) reads in words that no filing evidence is carried
 *      for that name
 *   3  nothing else moves (the control): VLO's coverage still shows its served counts ("39 drafted sentences", "95 evidence
 *      records"); the footer still shows the served citation counts ("20 citations", "20 of 20"); IMB's research-team position line
 *      still reads "Fund of record: IDVZ" with its source "Imperial Brands Research Pack"
 * Prints one line per surface, one line per arm and "EVIDENCE WORDING NAMES THE FILING EVIDENCE: <k> of 3 arms"; exit 0 only at 3
 * of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const NAMES = ['VLO', 'INTU', 'SAP', 'HK', 'IMB', 'AZN', 'TSM'];
const tabs = Object.fromEntries(S.renderAll(NAMES.map((n) => `posture-${n}`)).map((r) => [r.surface.replace('posture-', ''), r.html]));

function section(text) {
  const a = text.search(/evidence coverage|filing evidence, each side|evidence, each side/i);
  if (a < 0) return null;
  const b = text.indexOf('Reasons, each beside', a);
  return text.slice(a, b > a ? b : a + 1200);
}
function footer(html) {
  return unesc(L.textOf(L.innerOf(html, 'data-posture-cites-total') || ''));
}

const f1 = [];
const f2 = [];
const f3 = [];
let sections = 0;
for (const n of NAMES) {
  const html = tabs[n] || '';
  const text = unesc(L.textOf(html));
  const sec = section(text);
  const foot = footer(html);
  console.log(`SURFACE posture-${n}: section ${sec ? `"${sec.slice(0, 150)}..."` : 'none'} | footer "${foot.slice(0, 120)}"`);
  if (sec) {
    sections += 1;
    if (!/filing evidence|filings/i.test(sec)) f1.push(`${n}: the evidence section does not name the filing evidence`);
    if (/\bpacks?\b|research pack|research team's pack/i.test(sec)) f1.push(`${n}: the evidence section says "${(/[^.]*\b(packs?|research pack)\b[^.]*/i.exec(sec) || [''])[0].trim().slice(0, 90)}"`);
  }
  if (foot && /research pack|\bpacks?\b/i.test(foot)) f1.push(`${n}: the footer says "${foot.slice(0, 100)}"`);
  if (foot && sec && !/filing/i.test(foot)) f1.push(`${n}: the footer does not name the filings`);
  if (/on this object|carried in packs/i.test(text)) f2.push(`${n}: "${(/[^.]*(on this object|carried in packs)[^.]*/i.exec(text) || [''])[0].trim().slice(0, 90)}"`);
  const key = /\b[A-Z0-9]+_[A-Z]{2}_Equity\b/.exec(text);
  if (key) f2.push(`${n}: a raw key "${key[0]}" in visible text`);
}
for (const n of ['HK', 'IMB']) {
  const sec = section(unesc(L.textOf(tabs[n] || ''))) || '';
  if (!/no filing evidence/i.test(sec)) f2.push(`${n}: the absent side does not say that no filing evidence is carried`);
}
const vlo = unesc(L.textOf(tabs.VLO || ''));
for (const w of ['39 drafted sentences', '95 evidence records']) if (!vlo.includes(w)) f3.push(`VLO: "${w}" is gone`);
const vf = footer(tabs.VLO || '');
if (!/\b20\b.*citations/.test(vf) || !/20 of 20/.test(vf)) f3.push(`VLO footer: served counts changed ("${vf.slice(0, 100)}")`);
const imb = unesc(L.textOf(tabs.IMB || ''));
if (!imb.includes('Fund of record: IDVZ') || !imb.includes('Imperial Brands Research Pack')) f3.push("IMB: the research team's position line changed");

const a1 = f1.length === 0 && sections > 0;
const a1d = a1 ? `${sections} evidence section(s) and their footers name the filing evidence; no "pack" in them` : `${f1.length} failing; first: ${f1[0]}`;
const a2 = f2.length === 0;
const a2d = a2 ? 'no "on this object", "carried in packs" or raw key on any Posture tab; 992 HK and IMB say no filing evidence is carried' : `${f2.length} failing; first: ${f2[0]}`;
const a3 = f3.length === 0;
const a3d = a3 ? "served counts and the research team's position line unchanged" : `${f3.length} failing; first: ${f3[0]}`;
const arms = [
  ['the evidence section names the filing evidence', a1, a1d],
  ['no machine words; an absent side says which evidence is absent', a2, a2d],
  ['nothing else moves (control)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`EVIDENCE WORDING NAMES THE FILING EVIDENCE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
