const path = require('path');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const L = require(path.join(DSGN, '_load.cjs')); const S = require(path.join(DSGN, 'surfaces.cjs'));
const t = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
console.log(t.model.forecast_figures.filter((f) => f.mnemonic === 'BEST_DIV_YLD').map((f) => f.fiscal_year + ':' + f.value).join(' '));
