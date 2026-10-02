const path=require('path');
const DSGN=path.join(process.cwd(),'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const L=require(path.join(DSGN,'_load.cjs'));const S=require(path.join(DSGN,'surfaces.cjs'));
const t=S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
console.log(Object.keys(t));
console.log(JSON.stringify((t.header_figures||[]).filter(f=>/CRNCY|CURRENCY/i.test(f.mnemonic)),null,0));
const seen={};
for(const f of t.fiscal_year_figures){const k=f.mnemonic;if(!seen[k])seen[k]={unit:f.unit,cur:f.currency,scope:f.scope,ex:f.value};}
console.log(JSON.stringify(seen,null,1));
const s2={};for(const f of (t.model.forecast_figures||[])){if(!s2[f.mnemonic])s2[f.mnemonic]={unit:f.unit,cur:f.currency,scope:f.scope,ex:f.value}}
console.log(JSON.stringify(s2,null,1));
