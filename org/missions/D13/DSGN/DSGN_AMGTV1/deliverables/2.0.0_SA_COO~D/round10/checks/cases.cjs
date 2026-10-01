/**
 * cases.cjs -- DSGN_AMGTV1 round 10, AV-o-3: THE RESEARCH TEAM'S UPSIDE AND DOWNSIDE ON THE MODEL TAB, AND OPAL'S RULE CASES
 * LABELLED AS OPAL'S (round-9 analysis ruling 2; AMGT_CORPUS FWD-12).
 *
 * Usage (repo root): node <this file>
 * `/thesis` serves `model.team_cases` = { base, upside, downside }, each { status: SERVED, table: row -> period -> text, citation,
 * currency, unit_as_written } or { status: ABSENT, reason }, and `model_cases` (Opal's rule) = { base, upside, downside }, each
 * with its own status, label and reason. Today the Model tab shows only the team's Base and prints the rule's upside as "Upside
 * case: not in the pack yet -- the method is to be agreed" -- beside nothing on AZN, whose team Upside and Downside ARE served.
 * Fixtures (round10/fixtures, SERVED): AZN LN (team base / upside / downside all SERVED; rule base ABSENT with its label, rule
 * upside / downside ABSENT "methodology to be discussed with Andrew"), IMB LN (team cases ABSENT; the rule base SERVED as "Opal's
 * historical-multiple reference"), VLO US (team cases ABSENT with reasons; round-9 fixture).
 * Arms:
 *   1  the team's Upside and Downside rendered: for AZN an element [data-model-team-case="upside"] and one for "downside", each
 *      with data-model-team-case-state="SERVED", labelled the research team's in words, carrying every served table cell's text
 *      (e.g. the 2030E Price) as written; the team's Base still renders as before
 *   2  Opal's rule cases labelled as Opal's: on AZN, IMB and VLO every rule-case line ([data-model-case]) reads with "Opal's" at
 *      its head (e.g. "Opal's rule-based upside: the method is to be agreed.", or the served label such as "Opal's
 *      historical-multiple reference: ..."); no visible "Upside case:" / "Downside case:" / "Base case:" without "Opal's" or "the
 *      research team's" before it
 *   3  no bare absence beside a served team case: on AZN no visible "not in the pack yet" line names the Upside or Downside while
 *      the team's served Upside / Downside is on the tab unless it is labelled Opal's; on IMB / VLO (team cases ABSENT) the team
 *      Upside and Downside each read one plain sentence that the research team's case is not in this pack, with no figure
 * Prints one line per arm and "TEAM CASES AND OPAL'S RULE CASES: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');

const html = (n) => (S.renderAll([`model-${n}`])[0] || {}).html || '';
const unesc = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const vis = (h) => unesc(L.textOf(h));
const H = { AZN: html('AZN'), IMB: html('IMB'), VLO: html('VLO') };
const inner = (h, attr, v) => unesc(L.textOf(L.innerOf(h, attr, v) || ''));
const openTag = (h, attr, v) => { const i = h.indexOf(`${attr}="${v}"`); return i < 0 ? '' : h.slice(h.lastIndexOf('<', i), h.indexOf('>', i) + 1); };

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const azn = S.bundles.AZN_LN_Equity;
let cells = 0;
for (const side of ['upside', 'downside', 'base']) {
  const tc = azn.model.team_cases[side];
  const tag = openTag(H.AZN, 'data-model-team-case', side);
  if (!tag) { f1.push(`AZN: no [data-model-team-case="${side}"]`); continue; }
  if (!/data-model-team-case-state="SERVED"/.test(tag)) f1.push(`AZN ${side}: state is not SERVED (${tag.slice(0, 120)})`);
  const t = inner(H.AZN, 'data-model-team-case', side);
  if (!/research team/i.test(t)) f1.push(`AZN ${side}: not labelled the research team's`);
  for (const row of Object.values(tc.table || {})) for (const v of Object.values(row)) { cells += 1; if (!t.includes(v)) f1.push(`AZN ${side}: served "${v}" not shown`); }
}
const a1 = f1.length === 0 && cells > 0;
const a1d = a1 ? `AZN's team Base, Upside and Downside are SERVED on the tab, ${cells} table cell(s) shown as written` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
let lines = 0;
for (const [n, h] of Object.entries(H)) {
  for (const m of h.matchAll(/data-model-case="([^"]+)"/g)) {
    lines += 1;
    const t = inner(h, 'data-model-case', m[1]).trim();
    if (!/^Opal's\b/.test(t)) f2.push(`${n} rule ${m[1]}: "${t.slice(0, 80)}"`);
  }
  const text = vis(h);
  for (const bare of text.match(/(?:^|[.!?]\s+|\s)(?:Upside|Downside|Base) case:/g) || []) f2.push(`${n}: a bare "${bare.trim()}" on the tab`);
}
const a2 = f2.length === 0 && lines > 0;
const a2d = a2 ? `${lines} rule-case line(s) over AZN / IMB / VLO all read with "Opal's" at their head; no bare "<Name> case:"` : `${f2.length} failing of ${lines}; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
for (const m of vis(H.AZN).matchAll(/([^.]*?)(Upside|Downside)[^.]*not in the pack yet/gi)) {
  if (!/Opal's/.test(m[0])) f3.push(`AZN: a bare absence "${m[0].trim().slice(0, 90)}" beside the team's served ${m[2]}`);
}
for (const n of ['IMB', 'VLO']) {
  for (const side of ['upside', 'downside']) {
    const tag = openTag(H[n], 'data-model-team-case', side);
    const t = inner(H[n], 'data-model-team-case', side);
    if (!tag) { f3.push(`${n}: no [data-model-team-case="${side}"] sentence`); continue; }
    if (/data-model-team-case-state="SERVED"/.test(tag)) f3.push(`${n} ${side}: SERVED where the fixture is ABSENT`);
    if (!/research team/i.test(t) || !/not in this pack/i.test(t)) f3.push(`${n} ${side}: reads "${t.slice(0, 90)}"`);
    if (/\d+\.\d+/.test(t)) f3.push(`${n} ${side}: a figure in the absence sentence`);
  }
}
const a3 = f3.length === 0;
const a3d = a3 ? "no bare Upside/Downside absence beside AZN's served team cases; IMB and VLO say the team's Upside and Downside are not in this pack, with no figure" : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ["the research team's Upside and Downside rendered as written", a1, a1d],
  ["Opal's rule cases labelled as Opal's", a2, a2d],
  ['no bare absence beside a served team case', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`TEAM CASES AND OPAL'S RULE CASES: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
