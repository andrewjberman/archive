/**
 * team.cjs -- DSGN_AMGTV1 round 3: THE TEAM-CASE ABSENCE NAMES THE GAP THE PAGE CAN SEE (round-2 analysis, the CVO's decision 1).
 *
 * Usage (repo root): node <this file> <window|model>
 *   window  the Recommendation window body (ThesisCardDetail, sectionId 'recommendation') from components/ThesisCards.tsx
 *   model   the Model tab (ModelTab) from tabs/ModelTab.tsx
 * Fixtures (round3/fixtures, captured at the cut; the adapter now serves model.team_cases): Valero (base ABSENT with the
 * dossier's own reason), INTU (base SERVED).
 * Arms, all must hold:
 *   A  Valero as served (team_cases present, base ABSENT): the team-case element (data-team-case="base" in the window,
 *      data-model-team-case="base" on the Model tab) says the case is "not in the (or this) pack" AND carries the dossier's
 *      served reason -- in its visible text or in a data-team-case-reason attribute on the element (the reason is machine text).
 *   B  Valero with model.team_cases removed (a payload that does not carry the field): the element says "not served on this
 *      page yet" and does NOT say "not in the pack".
 *   C  INTU as served: the element renders the team's Base table as written (23.22, 16.0x, 371) with "as written in the team's
 *      pack".
 * Prints "TEAM CASE GAP (<surface>): k of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const surface = process.argv[2];
const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
const intu = L.fixture('thesisBundle.INTU_US_Equity.json');
const reason = String((((vlo.model || {}).team_cases || {}).base || {}).reason || '');
const bare = JSON.parse(JSON.stringify(vlo));
if (bare.model) delete bare.model.team_cases;
let render;
let attr;
if (surface === 'window') {
  const { ThesisCardDetail } = L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx');
  render = (b) => L.render(ThesisCardDetail, { sectionId: 'recommendation', bundle: b });
  attr = 'data-team-case';
} else if (surface === 'model') {
  const cur = { b: null };
  L.hookState.impl = { useThesisBundle: () => cur.b };
  const { ModelTab } = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx');
  render = (b) => { cur.b = b; return L.render(ModelTab, { securityKey: b.security_key }); };
  attr = 'data-model-team-case';
} else {
  console.log('usage: team.cjs window|model');
  process.exit(3);
}
const teamText = (html) => {
  const at = html.indexOf(`${attr}="base"`);
  if (at < 0) return null;
  return L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), attr, 'base') || '');
};
const results = [];
{
  const h = render(vlo);
  const t = teamText(h);
  const probe = reason.slice(0, 40);
  // The served reason rides ON the element -- visible, or in a data-team-case-reason attribute (it is machine text, and
  // cell 1 keeps machine text off the face); either carries the claim.
  const at = h.indexOf(`${attr}="base"`);
  const openTag = at < 0 ? '' : h.slice(h.lastIndexOf('<', at), h.indexOf('>', at) + 1);
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const carried = probe.length > 0 && ((t || '').includes(probe) || openTag.includes(esc(probe)) || h.includes('data-team-case-reason="' + esc(reason)));
  const ok = t !== null && /not in (the|this) pack/i.test(t) && carried;
  results.push(['A served ABSENT: "not in the/this pack" + the served reason carried', ok, `text=${JSON.stringify((t || '').slice(0, 140))} reason_carried=${carried}`]);
}
{
  const t = teamText(render(bare));
  const ok = t !== null && /not served on this page yet/i.test(t) && !/not in (the|this) pack/i.test(t);
  results.push(['B field not carried: "not served on this page yet"', ok, `text=${JSON.stringify((t || '').slice(0, 160))}`]);
}
{
  const t = teamText(render(intu));
  const miss = ['23.22', '16.0x', '371'].filter((w) => !(t || '').includes(w));
  const ok = t !== null && miss.length === 0 && /as written in the team's pack/i.test(t);
  results.push(['C INTU served: the table as written', ok, `missing=[${miss.join(',')}] as_written=${/as written in the team's pack/i.test(t || '')}`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`TEAM CASE GAP (${surface}): ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
