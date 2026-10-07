/**
 * r49.cjs -- DSGN_AMGTV1 round 49 issuer CHECK (2.0.0_SA_COO~D): THE MODEL TAB'S FOOT PRINTS MONEY IN THE PAGE'S ONE MONEY FORMAT.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round49/checks/r49/r49.cjs"
 *
 * Why: 3.0.0_SA_CVO~Z's FWD-27 re-grade (DSGN_AMGTV1_FWD20_CLAUSE_COUNT_AND_FWD27_REGRADE_20261007.md @7ca923a956, ground 1) and the
 * CTO's ruling msg 30869: the foot prints "Market capitalisation: USD 152,320 million" and "Average daily value traded (three
 * months): USD 1,356,158,848" on a page whose header prints market cap as "USD 152B". That is three money formats on one tab for
 * figures the PAGE formats. Read first (issuer): both foot figures are formatted by the page, in tabs/ModelTab.tsx `v3FactValue`
 * (toLocaleString plus " million"); the header's short form comes from components/StatTile.tsx `formatStatValue`.
 *
 * The expected strings are NOT typed here: they are computed by calling the page's own `formatStatValue` on the same served values,
 * so the arm reads "the foot uses the header's formatter", whatever that formatter prints.
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 THE FOOT USES THE HEADER'S MONEY FORMAT: the foot fact for market capitalisation (served 152320, MILLIONS, USD) reads
 *     formatStatValue(152320, 'currency-millions', 'USD', unit); average daily value traded (served 1356158848, ABSOLUTE, USD) reads
 *     formatStatValue(1356158848, 'currency-abs', 'USD', unit); the foot holds no "million" and no figure with two or more comma groups.
 *   2 KEEP: Country still prints its served value; the labels are unchanged; a money fact served with NO currency does not print a
 *     currency code it was not given (it says the currency is not stated).
 *   3 PLANTED: the grader refuses the two long forms and admits the short ones.
 * Renders the REAL ModelTab.tsx through round11/checks/_load.cjs on round-11 fixtures; no network; writes nothing.
 */
'use strict';
const path = require('path');
const R11 = path.join(__dirname, '..', '..', '..', 'round11', 'checks');
const L = require(path.join(R11, '_load.cjs'));
const S = require(path.join(R11, 'surfaces.cjs'));
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");

const VINT = '2026-10-06T13:30:00Z';
const U_ABS = 'ABSOLUTE (full currency units)';
const U_MM = 'MILLIONS';
const base = clone(S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json')));
function withFacts(currency) {
  const b = clone(base);
  const hf = Array.isArray(b.header_figures) ? b.header_figures : (b.header_figures = []);
  const put = (mnemonic, value, unit, cur) => {
    const at = hf.findIndex((f) => f && f.mnemonic === mnemonic);
    const row = { scope: 'HEADER', fiscal_year: null, mnemonic, value, unit, sign: null, basis: { mnemonic, definition: '' }, vintage: VINT, source: 'bloomberg', currency: cur };
    if (at >= 0) hf[at] = Object.assign({}, hf[at], row); else hf.push(row);
  };
  put('COUNTRY_FULL_NAME', 'UNITED STATES', 'TEXT (string field)', null);
  put('AVG_DAILY_VALUE_TRADED_3M', 1356158848, U_ABS, currency);
  put('CRNCY_ADJ_MKT_CAP', 152320, U_MM, currency);
  return b;
}
let BUNDLE = withFacts('USD');
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === 'BA_US_Equity' ? BUNDLE : (S.bundles[k] || undefined)),
  useModelVersions: () => S.unwrap(L.fixture('versions.BA_US_Equity.json')),
  useModelCompare: () => S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json')),
  useInputLedger: () => S.unwrap(L.fixture('ledger.BA_US_Equity.json')),
});
let MT = null; let ST = null; let loadErr = null;
try { MT = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); ST = L.source('src/pages/SecurityAnalysis/components/StatTile.tsx'); } catch (e) { loadErr = String(e && e.message).split('\n')[0]; }
const render = () => { try { return L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' }); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
// textOf puts a space where a tag closed, so "label</span>: value" reads "label : value"; close that gap before grading.
const tidy = (s) => unesc(s).replace(/\s+/g, ' ').replace(/ ([:;.])/g, '$1').trim();
const factText = (html, mnemonic) => tidy(L.textOf(L.innerOf(html, 'data-model-v3-fact', mnemonic) || ''));
const footText = (html) => tidy(L.textOf(L.innerOf(html, 'data-model-v3-facts') || ''));

// pure grader, so PLANTED can exercise it
function gradeFoot(foot, capFact, advFact, wantCap, wantAdv) {
  const f = [];
  if (!foot) return ['no [data-model-v3-facts] line rendered'];
  if (!capFact.includes(wantCap)) f.push(`market capitalisation reads "${capFact}", want it to hold "${wantCap}"`);
  if (!advFact.includes(wantAdv)) f.push(`average daily value traded reads "${advFact}", want it to hold "${wantAdv}"`);
  if (/\bmillion\b/i.test(foot)) f.push('the foot still prints "million"');
  if (/\d{1,3}(,\d{3}){2,}/.test(foot)) f.push('the foot still prints a figure written out in full (two or more comma groups)');
  return f;
}

// A non-money numeric fact (served 1234567): the plain grouped number, no currency words, no magnitude letter.
function nonMoneyFaults(fact) {
  const f = [];
  if (!fact) return ['the non-money fact is not rendered'];
  if (!fact.includes('1,234,567')) f.push(`a non-money number does not print as the plain grouped number "1,234,567" ("${fact}")`);
  if (/currency|USD|EUR|CHF/i.test(fact)) f.push(`a non-money number carries currency words ("${fact}")`);
  if (/\d(\.\d+)?[KMBT]\b/.test(fact)) f.push(`a non-money number carries a magnitude letter ("${fact}")`);
  return f;
}

const arms = [];
if (loadErr || !MT || !ST || typeof ST.formatStatValue !== 'function') {
  arms.push(['LOAD', false, loadErr || 'ModelTab or StatTile.formatStatValue did not load']);
} else {
  const wantCap = ST.formatStatValue(152320, 'currency-millions', 'USD', U_MM);
  const wantAdv = ST.formatStatValue(1356158848, 'currency-abs', 'USD', U_ABS);
  const html = render();
  {
    const f = /^RENDER FAILED/.test(html) ? [html] : gradeFoot(footText(html), factText(html, 'CRNCY_ADJ_MKT_CAP'), factText(html, 'AVG_DAILY_VALUE_TRADED_3M'), wantCap, wantAdv);
    if (!wantCap || !wantAdv) f.push('the header formatter returned nothing for the two served values');
    arms.push(["THE FOOT USES THE HEADER'S MONEY FORMAT", f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : `market capitalisation "${wantCap}"; average daily value traded "${wantAdv}"; no "million", no full-length figure`]);
  }
  {
    const f = [];
    const foot = footText(html);
    if (!/Country: UNITED STATES/.test(foot)) f.push(`Country no longer prints its served value ("${foot.slice(0, 80)}")`);
    for (const label of ['Average daily value traded (three months)', 'Market capitalisation']) if (!foot.includes(label)) f.push(`the label "${label}" is gone`);
    BUNDLE = withFacts(null);
    const bare = render();
    BUNDLE = withFacts('USD');
    const bareFoot = footText(bare);
    if (/USD|EUR|CHF|GBP|JPY/.test(bareFoot)) f.push(`a currency code is printed for a fact served with none ("${bareFoot.slice(0, 120)}")`);
    if (!/currency not stated/i.test(bareFoot)) f.push(`a money fact with no currency does not say the currency is not stated ("${bareFoot.slice(0, 120)}")`);
    arms.push(['KEEP: country, labels, and no invented currency', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : 'Country: UNITED STATES; both labels; a fact with no currency says so']);
  }
  {
    // AMENDMENT 1 (CTO review msg 30881): only a DECLARED money fact takes the money format. V3_HEADER_LABELS is an open list, so a
    // numeric fact that is not money must print as a plain grouped number. COUNTRY_FULL_NAME is the one non-money mnemonic the list
    // holds today; here it is served as a NUMBER (an issuer variant) to exercise that branch.
    const f = [];
    const b = withFacts('USD');
    const row = b.header_figures.find((x) => x && x.mnemonic === 'COUNTRY_FULL_NAME');
    row.value = 1234567; row.unit = null; row.currency = null;
    BUNDLE = b;
    const h = render();
    BUNDLE = withFacts('USD');
    const fact = factText(h, 'COUNTRY_FULL_NAME');
    f.push(...nonMoneyFaults(fact));
    const cap = factText(h, 'CRNCY_ADJ_MKT_CAP');
    if (!cap.includes(ST.formatStatValue(152320, 'currency-millions', 'USD', U_MM))) f.push(`with a non-money number beside it, market capitalisation lost the money format ("${cap}")`);
    arms.push(['A NUMBER THAT IS NOT MONEY IS NOT FORMATTED AS MONEY', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : `a non-money numeric fact reads "${fact}"; the money facts keep the money format`]);
  }
}
{
  const f = [];
  const longFoot = 'Country: UNITED STATES; Average daily value traded (three months): USD 1,356,158,848; Market capitalisation: USD 152,320 million.';
  const shortFoot = 'Country: UNITED STATES; Average daily value traded (three months): USD 1.36B; Market capitalisation: USD 152B.';
  if (gradeFoot(longFoot, 'Market capitalisation: USD 152,320 million', 'Average daily value traded (three months): USD 1,356,158,848', 'USD 152B', 'USD 1.36B').length < 4) f.push('the long forms are not refused on all four counts');
  if (gradeFoot(shortFoot, 'Market capitalisation: USD 152B', 'Average daily value traded (three months): USD 1.36B', 'USD 152B', 'USD 1.36B').length) f.push('the short forms are refused');
  if (!gradeFoot('', '', '', 'x', 'y').length) f.push('a missing foot is admitted');
  if (!nonMoneyFaults('Country: 1.23M currency not stated').length) f.push('a non-money number in the money format is admitted');
  if (nonMoneyFaults('Country: 1,234,567').length) f.push('a plain grouped non-money number is refused');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : 'the long forms refused on 4 counts, a missing foot refused, a money-formatted non-money number refused; the clean forms admitted']);
}

const TITLE = "THE MODEL TAB'S FOOT PRINTS MONEY IN THE PAGE'S ONE MONEY FORMAT";
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
