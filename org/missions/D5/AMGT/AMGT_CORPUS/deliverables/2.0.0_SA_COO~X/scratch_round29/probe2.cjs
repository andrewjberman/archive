const path = require('path');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const L = require(path.join(DSGN, '_load.cjs')); const S = require(path.join(DSGN, 'surfaces.cjs'));
const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
L.hookState.impl = Object.assign({}, L.hookState.impl, { useThesisBundle: () => thesis, useModelVersions: () => undefined, useModelCompare: () => undefined, useInputLedger: () => undefined });
const MT = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx');
const html = L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' });
for (const m of html.matchAll(/<tr[^>]*data-model-row="(EQY_DVD_YLD_IND|EBITDA|REVENUE_PER_SH)"[^>]*>([\s\S]*?)<\/tr>/g)) {
  console.log(m[1], [...m[2].matchAll(/<td[^>]*>([^<]*)/g)].map((x) => x[1]).join(' | '));
}
