/**
 * posturewords.cjs -- DSGN_AMGTV1 round 6, AV-u-2: POSTURE'S LAST MACHINE PHRASING (round-5 analysis s.4 item 2, ruling 5;
 * FWD-10).
 *
 * Usage (repo root): node <this file>
 * Renders the Posture tab on SAP GY (comparable ANET US) and Valero (comparable WMB), served fixtures under round6/fixtures.
 * Visible text includes collapsed <details> content (the cites sit in a drawer). Measured at the cut on SAP GY: "comparability
 * log cap distance: 0.1047 (the object's comparable selection)", "cite not resolved -- no rung name for the comparable on this
 * name's peer set or on the object's comparable selection", "... no industry group for the comparable ... on the object's
 * comparable selection", and the footer "10 of 18 cite(s) resolved on the bundles this page reads (the object validated 18 of
 * 18 against its packs)".
 * THE PHRASE CLASS (what round 5's census missed): "the object", "comparable selection", "rung", "log cap", "cite(s)",
 * "bundles this page reads", a served field name printed with its underscores turned to spaces ("rung name", "industry
 * group" beside "on this name's peer set"), and "validated N of N against its packs".
 * Arms:
 *   1  SAP GY: 0 phrase-class hits on the cite lines and the footer
 *   2  Valero: 0 phrase-class hits on the cite lines and the footer
 *   3  nothing dropped: every cite still renders (SAP GY 18, Valero 20 cite lines -- the counts at the cut), and the footer
 *      still states both served counts (its resolved count and the served cites_total) as numbers, now in words around them
 * Prints one line per arm and "POSTURE PHRASING IN WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const bundles = {};
for (const k of ['VLO_US_Equity', 'SAP_GY_Equity', 'WMB_US_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: () => undefined };

const PHRASE = /\bthe object\b|comparable selection|\brung\b|\blog cap\b|\bcite\(s\)|bundles this page reads|on this name's peer set|validated \d+ of \d+ against its packs|comparability [a-z]+ [a-z]+ [a-z]+:/gi;
function render(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
function citeLines(html) {
  const out = [];
  const re = /<li[^>]*data-posture-cite="[^"]*"[^>]*>([\s\S]*?)<\/li>/g;
  let m;
  while ((m = re.exec(html)) !== null) out.push(L.textOf(m[1]));
  return out;
}
function footer(html) {
  const m = /<p[^>]*data-posture-cites-resolved="([^"]*)"[^>]*data-posture-cites-total="([^"]*)"[^>]*>([\s\S]*?)<\/p>/.exec(html);
  return m ? { resolved: m[1], total: m[2], text: L.textOf(m[3]) } : null;
}
const read = (key) => {
  const h = render(key);
  const cites = citeLines(h);
  const f = footer(h);
  const hits = [...cites, f ? f.text : ''].join(' | ').match(PHRASE) || [];
  return { h, cites, f, hits };
};
const sap = read('SAP_GY_Equity');
const vlo = read('VLO_US_Equity');
const served = (key) => (bundles[key].posture || {}).cites_total;
const footerOk = (r, key) =>
  !!r.f && r.f.text.includes(String(r.f.resolved)) && (served(key) === null || served(key) === undefined || r.f.text.includes(String(served(key))));
const arms = [
  ['SAP GY: no machine phrasing on the cites or the footer', sap.h.length > 0 && sap.hits.length === 0, `${sap.hits.length} hit(s) ${JSON.stringify(sap.hits.slice(0, 6))}`],
  ['Valero: no machine phrasing on the cites or the footer', vlo.h.length > 0 && vlo.hits.length === 0, `${vlo.hits.length} hit(s) ${JSON.stringify(vlo.hits.slice(0, 6))}`],
  ['nothing dropped: every cite renders, the footer keeps both counts',
    sap.cites.length >= 18 && vlo.cites.length >= 20 && footerOk(sap, 'SAP_GY_Equity') && footerOk(vlo, 'VLO_US_Equity'),
    `cite lines SAP ${sap.cites.length}/18, Valero ${vlo.cites.length}/20; footer SAP "${sap.f ? sap.f.text.slice(0, 90) : 'absent'}"`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`POSTURE PHRASING IN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
