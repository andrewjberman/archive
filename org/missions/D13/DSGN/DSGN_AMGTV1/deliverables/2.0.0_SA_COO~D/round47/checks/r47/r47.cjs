/**
 * r47.cjs -- DSGN_AMGTV1 round 47 issuer CHECK (2.0.0_SA_COO~D): THE MODEL TAB HAS NO TEXT UNDER 11 PX, NO VENDOR SHORT-NAME LINE,
 * AND ITS INPUT LEDGER READS IN PLAIN WORDS.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round47/checks/r47/r47.cjs"
 *
 * Why: ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md @43d2e5eb3c, ROUND 47 items 1 and 2 (rulings 6 and 7):
 *   1 FWD-20: the Model tab's 10 px text is raised to the contract floor of 11 px (tabs/ModelTab.tsx, the gap-mark <sup>).
 *   2 FWD-27: the Model tab's foot prints "Company short name: BOEING CO/THE" beside the display name "The Boeing Co", and two
 *     system-wording lines: "2 of 6 inputs have run." and "News: a source this page has no name for yet". All three are PAGE text
 *     (modelSheet.ts V3_HEADER_LABELS.SHORT_NAME; ModelTab.tsx ledgerSourceWords and the data-input-ledger-count line). The news
 *     class is served with source "harvested news (the overlay feed, gold article_security_mention)" (lib/research/api/scoped_amgt.py).
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 NO TEXT UNDER 11 PX: the rendered Model tab carries no text-[Npx] class with N < 11, and ModelTab.tsx carries no fontSize
 *     literal under 11.
 *   2 NO VENDOR SHORT-NAME LINE: the rendered Model tab does not print "Company short name" or the served SHORT_NAME value; the
 *     other three header facts (Country, Average daily value traded, Market capitalisation) are still printed.
 *   3 THE INPUT LEDGER IN PLAIN WORDS: with 2 of 6 classes run, the section states "2 of 6", does not say "inputs have run", and
 *     says the count in a sentence a reader understands; the News row names its source "Articles we collect" and prints none of
 *     the served storage words; a class served with a source the page does not know reads "source not named" and never the raw
 *     token or "this page has no name for".
 *   4 PLANTED: the graders refuse a 10 px class, a short-name line, "inputs have run" and the unnamed-source phrase.
 * Renders the REAL ModelTab.tsx through round11/checks/_load.cjs on round11 fixtures; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const R11 = path.join(__dirname, '..', '..', '..', 'round11', 'checks');
const L = require(path.join(R11, '_load.cjs'));
const S = require(path.join(R11, 'surfaces.cjs'));
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");

const SERVED_NEWS_SOURCE = 'harvested news (the overlay feed, gold article_security_mention)';
const SHORT_NAME_VALUE = 'BOEING CO/THE';
const VINT = '2026-10-06T13:30:00Z';

const thesis = clone(S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json')));
// The four V3 header facts as the deployed producer serves them (walk read-20261007T093016Z, BA US Model tab).
const hf = Array.isArray(thesis.header_figures) ? thesis.header_figures : (thesis.header_figures = []);
const put = (mnemonic, value, unit, currency) => {
  const at = hf.findIndex((f) => f && f.mnemonic === mnemonic);
  const row = { scope: 'HEADER', fiscal_year: null, mnemonic, value, unit, sign: null, basis: { mnemonic, definition: '' }, vintage: VINT, source: 'bloomberg', currency };
  if (at >= 0) hf[at] = Object.assign({}, hf[at], row); else hf.push(row);
};
put('SHORT_NAME', SHORT_NAME_VALUE, 'TEXT (string field)', null);
put('COUNTRY_FULL_NAME', 'UNITED STATES', 'TEXT (string field)', null);
put('AVG_DAILY_VALUE_TRADED_3M', 1356158848, 'ABSOLUTE (full currency units)', 'USD');
put('CRNCY_ADJ_MKT_CAP', 152320, 'MILLIONS', 'USD');

const ledger = clone(S.unwrap(L.fixture('ledger.BA_US_Equity.json')));
ledger.classes.news = Object.assign({}, ledger.classes.news, { source: SERVED_NEWS_SOURCE });
ledger.latest_by_class.news = { input_class: 'news', source: SERVED_NEWS_SOURCE, outcome: 'OK', stamp: '20261005T120000Z', detail: null };
ledger.denominators = Object.assign({}, ledger.denominators, { classes: 6, classes_with_a_run: 2 });
let LG = ledger;

L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === 'BA_US_Equity' ? thesis : (S.bundles[k] || undefined)),
  useModelVersions: () => S.unwrap(L.fixture('versions.BA_US_Equity.json')),
  useModelCompare: () => S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json')),
  useInputLedger: () => LG,
});
const MT_PATH = 'src/pages/SecurityAnalysis/tabs/ModelTab.tsx';
const MT = (() => { try { return L.source(MT_PATH); } catch (e) { return null; } })();
const render = () => { try { return MT ? L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' }) : 'RENDER FAILED no module'; } catch (e) { return 'RENDER FAILED ' + e.message; } };

// ---- graders (pure, so the PLANTED arm can exercise them) -------------------------------------------------------------------
const smallClasses = (html) => [...String(html).matchAll(/text-\[(\d+(?:\.\d+)?)px\]/g)].map((m) => Number(m[1])).filter((n) => n < 11);
const smallLiterals = (src) => [...String(src).matchAll(/fontSize\s*[:=]\s*\{?\s*['"]?(\d+(?:\.\d+)?)/g)].map((m) => Number(m[1])).filter((n) => n < 11);
const shortNameFaults = (text) => {
  const f = [];
  if (/Company short name/i.test(text)) f.push('"Company short name" is printed');
  if (text.includes(SHORT_NAME_VALUE)) f.push(`the served short name "${SHORT_NAME_VALUE}" is printed`);
  return f;
};
const ledgerFaults = (text) => {
  const f = [];
  if (/inputs have run/i.test(text)) f.push('"inputs have run" survives');
  if (/this page has no name for/i.test(text)) f.push('"this page has no name for" survives');
  if (/article_security_mention|\bgold\b|overlay feed|harvested news \(/i.test(text)) f.push('a served storage word is printed');
  return f;
};

const html = render();
const text = unesc(L.textOf(html));
const failedRender = /^RENDER FAILED/.test(html);

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
if (failedRender) f1.push(html);
const sc = smallClasses(html);
if (sc.length) f1.push(`${sc.length} rendered text-[Npx] class(es) under 11: ${JSON.stringify([...new Set(sc)])}`);
const srcFile = path.join(process.cwd(), 'portal', MT_PATH);
const src = fs.existsSync(srcFile) ? fs.readFileSync(srcFile, 'utf8') : null;
if (src === null) f1.push(`cannot read ${srcFile}`);
else { const sl = smallLiterals(src); if (sl.length) f1.push(`fontSize literal(s) under 11 in ModelTab.tsx: ${JSON.stringify(sl)}`); }
if (!/data-model-gap-mark/.test(html)) f1.push('no [data-model-gap-mark] rendered, so the mark this arm exists for was not exercised');
const a1 = f1.length === 0;
const a1d = a1 ? `0 text sizes under 11 px over ${[...html.matchAll(/text-\[(\d+)px\]/g)].length} sized nodes; gap marks rendered` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = failedRender ? [html] : shortNameFaults(text);
for (const keep of ['Country', 'UNITED STATES', 'Average daily value traded', 'Market capitalisation']) {
  if (!text.includes(keep)) f2.push(`KEEP: "${keep}" is no longer printed`);
}
const a2 = f2.length === 0;
const a2d = a2 ? 'no short-name line; Country, Average daily value traded and Market capitalisation still printed' : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const sec = L.innerOf(html, 'data-input-ledger') || '';
const st = unesc(L.textOf(sec));
if (!sec) f3.push('no [data-input-ledger] section rendered');
f3.push(...ledgerFaults(st));
if (!/\b2 of 6\b/.test(st)) f3.push('"2 of 6" is not stated');
const newsRow = unesc(L.textOf(L.innerOf(sec, 'data-ledger-class', 'news') || ''));
if (!/Articles we collect/.test(newsRow)) f3.push(`the News row does not name its source "Articles we collect" ("${newsRow.slice(0, 90)}")`);
if (!/worked/i.test(newsRow)) f3.push('the News row no longer says its run worked');
LG = clone(ledger); LG.classes.web = Object.assign({}, LG.classes.web, { source: 'zzz_vendor_feed' });
const webRow = unesc(L.textOf(L.innerOf(L.innerOf(render(), 'data-input-ledger') || '', 'data-ledger-class', 'web') || ''));
LG = ledger;
if (!/source not named/i.test(webRow)) f3.push(`an unknown source does not read "source not named" ("${webRow.slice(0, 90)}")`);
if (/zzz_vendor_feed/.test(webRow)) f3.push('an unknown source prints its raw token');
const mdRow = unesc(L.textOf(L.innerOf(sec, 'data-ledger-class', 'market_data') || ''));
if (!/Bloomberg/.test(mdRow)) f3.push('KEEP: the market data row no longer names Bloomberg');
const a3 = f3.length === 0;
const a3d = a3 ? '"2 of 6" stated in plain words; News from "Articles we collect"; an unknown source reads "source not named"; Bloomberg kept' : `${f3.length} failing; first: ${f3[0]}`;

// ---- arm 4 PLANTED ----------------------------------------------------------------------------------------------------------
const f4 = [];
if (smallClasses('<sup class="ml-0.5 text-[10px] font-bold">1</sup>').length !== 1) f4.push('a planted text-[10px] is not refused');
if (smallClasses('<p class="text-[11px]">x</p>').length !== 0) f4.push('a clean text-[11px] control is refused');
if (smallLiterals("tick={{ fontSize: 10 }}").length !== 1) f4.push('a planted fontSize: 10 is not refused');
if (shortNameFaults('Company short name: BOEING CO/THE; Country: UNITED STATES').length !== 2) f4.push('a planted short-name line is not refused twice');
if (shortNameFaults('Country: UNITED STATES').length !== 0) f4.push('a clean header-facts control is refused');
if (ledgerFaults('2 of 6 inputs have run.').length !== 1) f4.push('a planted "inputs have run" is not refused');
if (ledgerFaults('News: a source this page has no name for yet').length !== 1) f4.push('a planted unnamed-source phrase is not refused');
if (ledgerFaults(`News: ${SERVED_NEWS_SOURCE}`).length !== 1) f4.push('a planted served storage string is not refused');
if (ledgerFaults('2 of 6 kinds of input have been collected for this name.').length !== 0) f4.push('a clean ledger control is refused');
const a4 = f4.length === 0;
const a4d = a4 ? '5 planted faults refused, 3 clean controls admitted' : `${f4.length} failing; first: ${f4[0]}`;

const arms = [
  ['NO TEXT UNDER 11 PX', a1, a1d],
  ['NO VENDOR SHORT-NAME LINE', a2, a2d],
  ['THE INPUT LEDGER IN PLAIN WORDS', a3, a3d],
  ['PLANTED', a4, a4d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`THE MODEL TAB HAS NO SMALL TEXT, NO VENDOR SHORT NAME AND A PLAIN-WORDS LEDGER: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
