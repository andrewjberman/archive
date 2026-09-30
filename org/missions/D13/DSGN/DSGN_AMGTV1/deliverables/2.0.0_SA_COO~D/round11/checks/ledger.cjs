/**
 * ledger.cjs -- DSGN_AMGTV1 round 11, AV-n-6: THE MODEL TAB SHOWS WHERE EACH INPUT CAME FROM, WHEN IT LAST RAN AND WHETHER THAT RUN
 * WORKED (round-10 analysis s.2 cell 6, routed from AMGT_RESAPP round-51 ruling 1; RESAPP FWD-12).
 *
 * Usage (repo root): node <this file>
 * RESAPP FWD-12 (AMGT_RESAPP_PRD.md:520-528): "For each kind of input -- market data, filings, news, social, web -- the page shows
 * where it came from, when it last ran, and whether that run worked; and any one can be re-run on its own." The deployed scoped API
 * serves `GET /security/{key}/ledger` (classes{name: {source, stage_registered}} for six classes -- market_data, filings, news,
 * social, web, sa; latest_by_class{class: {input_class, source, outcome OK|FAILED|SKIPPED, stamp, detail}}; denominators{classes,
 * classes_with_a_run, classes_with_a_stage}; read); the portal has no caller, and NO served route re-runs one input alone. The
 * contract (AV-n-6's face): hook `useInputLedger(key)` in hooks/useLeadPanelApi.ts; the Model tab renders `[data-input-ledger]`
 * with one `[data-ledger-class="<class>"]` per served class. Fixtures (round11/fixtures, SERVED): BA US /ledger (market_data OK at
 * 20260925T042544Z from bloomberg; five classes with no run). ISSUER VARIANTS (labelled): a FAILED market_data run; a read ABSENT with
 * its served reason ("no ledger object at <key>").
 * Arms:
 *   1  every input a row, in words: 6 `[data-ledger-class]` rows in the served order; each class named in words ("Market data",
 *      "Filings", "News", "Social", "Web", "Seeking Alpha" -- no "market_data" / "sa" token); market data reads its source
 *      "Bloomberg", its last run's date in the long form ("September 25th, 2026") and "worked"; each class with no run reads that
 *      it has not run yet
 *   2  the count and the re-run are honest: the section states "1 of 6" inputs has run (the served denominators); it says in words
 *      that re-running one input on its own is not available on this page yet (no served route does it); the run's `detail`
 *      (storage paths) is not in visible text -- no "bronze/", "harvest/", ".json" or "s3://"
 *   3  a run that failed or a read that did not answer says so: the FAILED variant's market data row reads "failed"; the ABSENT
 *      variant shows a designed sentence that the input ledger is not there for this name yet, and no storage key or status token
 * Prints one line per arm and "WHERE EACH INPUT CAME FROM: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const DU = (() => { try { return L.source('src/lib/dateUtils.ts'); } catch (e) { return {}; } })();
const longDate = (d) => String(DU.formatPanelTimestamp(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '');

const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const ledger = S.unwrap(L.fixture('ledger.BA_US_Equity.json'));
let LG = ledger;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === 'BA_US_Equity' ? thesis : (S.bundles[k] || undefined)),
  useModelVersions: () => S.unwrap(L.fixture('versions.BA_US_Equity.json')),
  useModelCompare: () => S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json')),
  useInputLedger: () => LG,
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = () => { try { return MT ? L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };
const WORDS = { market_data: 'Market data', filings: 'Filings', news: 'News', social: 'Social', web: 'Web', sa: 'Seeking Alpha' };

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const html = render();
const sec = L.innerOf(html, 'data-input-ledger') || '';
const rows = [...sec.matchAll(/data-ledger-class="([^"]+)"/g)].map((m) => m[1]);
const order = Object.keys(ledger.classes);
if (JSON.stringify(rows) !== JSON.stringify(order)) f1.push(`rows ${JSON.stringify(rows)}, want ${JSON.stringify(order)}`);
const rowText = (c) => unesc(L.textOf(L.innerOf(sec, 'data-ledger-class', c) || ''));
for (const c of order) {
  const t = rowText(c);
  if (!new RegExp(WORDS[c], 'i').test(t)) f1.push(`${c}: not named "${WORDS[c]}"`);
  const run = (ledger.latest_by_class || {})[c];
  if (run) {
    const day = `${run.stamp.slice(0, 4)}-${run.stamp.slice(4, 6)}-${run.stamp.slice(6, 8)}`;
    if (!/Bloomberg/.test(t)) f1.push(`${c}: its source "Bloomberg" is not shown`);
    if (!t.includes(longDate(day))) f1.push(`${c}: its last run "${longDate(day)}" is not shown`);
    if (!/worked/i.test(t)) f1.push(`${c}: "worked" is not shown for an OK run`);
  } else if (!/not run yet|has not run/i.test(t)) f1.push(`${c}: does not say it has not run yet ("${t.slice(0, 80)}")`);
}
if (/\bmarket_data\b|\bsa\b(?! [a-z])/.test(unesc(L.textOf(sec)).replace(/Seeking Alpha/g, ''))) f1.push('a raw class token in visible text');
const a1 = f1.length === 0 && rows.length === 6;
const a1d = a1 ? '6 inputs listed in the served order, named in words; market data from Bloomberg, last run dated, "worked"; the rest "not run yet"' : `${f1.length || 'rows'} failing; first: ${f1[0] || rows.length + ' rows'}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const st = unesc(L.textOf(sec));
const dn = ledger.denominators;
if (!new RegExp(`\\b${dn.classes_with_a_run} of ${dn.classes}\\b`).test(st)) f2.push(`"${dn.classes_with_a_run} of ${dn.classes}" is not stated`);
if (!/re-?run/i.test(st) || !/not available/i.test(st)) f2.push('no sentence that re-running one input alone is not available here yet');
if (/bronze\/|harvest\/|\.json\b|s3:\/\//.test(unesc(L.textOf(html)))) f2.push('a storage path in visible text');
const a2 = f2.length === 0;
const a2d = a2 ? `"${dn.classes_with_a_run} of ${dn.classes}" inputs run stated; re-run said to be unavailable; no storage path visible` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
LG = clone(ledger); LG.latest_by_class.market_data.outcome = 'FAILED';
const tf = unesc(L.textOf(L.innerOf(L.innerOf(render(), 'data-input-ledger') || '', 'data-ledger-class', 'market_data') || ''));
if (!/failed/i.test(tf)) f3.push(`the FAILED run reads "${tf.slice(0, 80)}"`);
LG = clone(ledger); LG.latest_by_class = {}; LG.read = Object.assign({}, LG.read, { status: 'ABSENT', reason: 'no ledger object at ledger/security_key=BA_US_Equity/input_ledger.json' });
const ta = unesc(L.textOf(render()));
if (!/ledger|where each input came from|inputs?/i.test(unesc(L.textOf(L.innerOf(render(), 'data-input-ledger') || '')))) f3.push('the ABSENT variant renders no designed sentence');
if (/ledger\/security_key|input_ledger\.json|\bABSENT\b/.test(ta)) f3.push('a storage key or status token in visible text for the ABSENT variant');
LG = ledger;
const a3 = f3.length === 0;
const a3d = a3 ? 'a FAILED run reads "failed"; an ABSENT ledger reads a designed sentence with no key or status token' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['every input a row, in words', a1, a1d],
  ['the count and the re-run are honest; no storage path', a2, a2d],
  ['a failed run or an absent ledger says so', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`WHERE EACH INPUT CAME FROM: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
