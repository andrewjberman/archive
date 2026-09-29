/**
 * attrs.cjs -- DSGN_AMGTV1 round 6, AV-u-5: THE DATA ATTRIBUTES FWD-30 NEEDS (AMGT_RESAPP round-49 ask, msg 26753 from
 * 2.0.0_SA_COO~Z; rows AMGT_RESAPP-Z-W173-S1..S4). FWD-30's grade (AMGT_RESAPP round45/checks/sweep.py, merged @525e045932)
 * reads the page ONLY through data attributes; seven facts the page shows carry none, so the grade matches them on identity,
 * not value. Each gains ONE attribute carrying the served value or reason. NO VISIBLE CHANGE.
 *
 * Usage (repo root): node <this file>        (issuer only, at the cut: ATTRS_SNAPSHOT=1 node <this file> writes the base
 *                                             visible-text snapshot round6/fixtures/attrs.visible.base.json)
 * THE CONTRACT (attribute -> the served value it must equal):
 *   M1 every sheet figure cell `[data-model-cell]` inside a `[data-model-row=<mnemonic>]` row carries data-model-cell="<served
 *      value>" and data-model-year="<fiscal year>"  -> fiscal_year_figures[mnemonic, year].value
 *   M2 a SERVED case line `[data-model-case]` carries data-model-case-value="<served value>" and data-model-case-currency="<the
 *      currency the line prints, '' when none>"      -> model_cases.<case>.value ; the page's own caseCurrency
 *   H1 the identity line carries data-identity-sector / data-identity-country / data-identity-currency
 *                                                     -> header figures GICS_SECTOR_NAME / CNTRY_OF_DOMICILE / CRNCY
 *   H2 an ABSENT description `[data-header-description="ABSENT"]` carries data-header-description-reason -> description.reason
 *   H3 an ABSENT driver chart `[data-driver-chart="ABSENT"]` carries data-driver-chart-series -> thesis_driver_chart.driver_series
 *      (the key the export shares: it names the series)
 *   P1 each peers absent column `[data-absent-column]` carries data-absent-column-reason -> that column's served reason (the
 *      reason the line itself prints)
 *   P2 a no-call verdict `[data-posture-verdict="absent"]` carries data-posture-reason -> posture.reason
 * Inputs: SAP GY served fixtures (thesisBundle, overlay), Valero's served peer set. ISSUER VARIANTS (in memory, not served):
 * an overlay whose description is {status: ABSENT, reason} and a posture whose verdict is "absent" with a reason -- no served
 * fixture carries either state today; each variant changes only that one field.
 * Arms:
 *   1  Model (SAP GY): M1 on every sheet cell (>= 100 cells, 0 mismatches) and M2 on the served Base case; ModelTab's visible
 *      text unchanged against the base snapshot
 *   2  Header (SAP GY): H1, H2 (variant), H3; the identity header's and driver chart's visible text unchanged
 *   3  Peers (Valero) and Posture (SAP GY variant): P1 on every absent column (>= 1), P2; visible text unchanged
 * Prints one line per arm and "FWD-30 ATTRIBUTES: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const nothing = () => null;
L.stubSource('src/pages/SecurityAnalysis/components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: nothing });
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);

const SA = 'src/pages/SecurityAnalysis/';
const bundle = L.fixture('thesisBundle.SAP_GY_Equity.json');
const overlay = L.fixture('overlay.SAP_GY_Equity.json');
const peers = L.fixture('peerSet.VLO_US_Equity.json');
const DESC_REASON = 'the vendor returned no description for this name';
const NOCALL_REASON = 'no call was made: the comparable pack carries no figures';
const overlayAbsent = { ...overlay, description: { status: 'ABSENT', source: null, marked: null, text: null, reason: DESC_REASON } };
const bundleNoCall = { ...bundle, posture: { ...bundle.posture, verdict: 'absent', reason: NOCALL_REASON } };

const safe = (fn) => {
  try {
    return fn();
  } catch (e) {
    console.log('render failed: ' + String(e.message).split('\n')[0]);
    return '';
  }
};
const dec = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const attr = (tag, name) => { const m = new RegExp('\\s' + name + '="([^"]*)"').exec(tag); return m ? dec(m[1]) : null; };
const tags = (html, name) => (html.match(new RegExp('<[a-z]+[^>]*\\s' + name + '(="[^"]*")?[^>]*>', 'g')) || []);

// ---- renders -----------------------------------------------------------------------------------------------------------
L.hookState.impl = { useThesisBundle: () => bundle, usePeerSet: () => undefined };
const model = safe(() => L.render(L.source(SA + 'tabs/ModelTab.tsx').ModelTab, { securityKey: 'SAP_GY_Equity' }));
const ident = safe(() => L.render(L.source(SA + 'components/SecurityOverlay.tsx').IdentityHeader, { bundle: overlay }));
const identAbsent = safe(() => L.render(L.source(SA + 'components/SecurityOverlay.tsx').IdentityHeader, { bundle: overlayAbsent }));
const driver = safe(() => L.render(L.source(SA + 'components/ThesisDriverChart.tsx').ThesisDriverChart, { chart: bundle.thesis_driver_chart, driver: bundle.thesis_driver, sections: [] }));
L.hookState.impl = { useThesisBundle: () => bundle, usePeerSet: () => peers };
const peersHtml = safe(() => L.render(L.source(SA + 'tabs/PeersTab.tsx').PeersTab, { securityKey: 'VLO_US_Equity' }));
L.hookState.impl = { useThesisBundle: () => bundleNoCall, usePeerSet: () => undefined };
const posture = safe(() => L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: 'SAP_GY_Equity' }));

const visible = { model: L.textOf(model), ident: L.textOf(ident), identAbsent: L.textOf(identAbsent), driver: L.textOf(driver), peers: L.textOf(peersHtml), posture: L.textOf(posture) };
const SNAP = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round6/fixtures/attrs.visible.base.json');
if (process.env.ATTRS_SNAPSHOT === '1') {
  fs.writeFileSync(SNAP, JSON.stringify(visible, null, 1));
  console.log('SNAPSHOT written: ' + SNAP);
  process.exit(0);
}
const base = JSON.parse(fs.readFileSync(SNAP, 'utf8'));
const same = (...keys) => keys.every((k) => visible[k] === base[k]);
const changed = (...keys) => keys.filter((k) => visible[k] !== base[k]);

// ---- arm 1: Model ---------------------------------------------------------------------------------------------------------
const figs = {};
for (const f of bundle.fiscal_year_figures || []) figs[`${f.mnemonic}|${f.fiscal_year}`] = f.value;
let cells = 0;
let good = 0;
const bad1 = [];
for (const rowm of model.matchAll(/<tr[^>]*data-model-row="([^"]*)"[^>]*>([\s\S]*?)<\/tr>/g)) {
  for (const t of tags(rowm[2], 'data-model-cell')) {
    const year = attr(t, 'data-model-year');
    if (year === null) continue; // a hidden refusal marker carries no year; the sheet cells do
    cells += 1;
    const want = figs[`${rowm[1]}|${year}`];
    const got = attr(t, 'data-model-cell');
    if (want !== undefined && got !== null && got !== '' && Number(got) === Number(want)) good += 1;
    else if (bad1.length < 3) bad1.push(`${rowm[1]} ${year}: attr ${JSON.stringify(got)} vs served ${JSON.stringify(want)}`);
  }
}
const sheetCells = tags(model, 'data-model-cell').length;
const baseCase = (bundle.model_cases || {}).base || {};
const caseTag = tags(model, 'data-model-case').find((t) => attr(t, 'data-model-case') === 'Base' && attr(t, 'data-model-case-status') === 'SERVED') || '';
const caseOk = !!caseTag && Number(attr(caseTag, 'data-model-case-value')) === Number(baseCase.value) && attr(caseTag, 'data-model-case-currency') === 'EUR';
const a1 = cells >= 100 && good === cells && caseOk && same('model');
const a1d = `sheet cells with a year ${cells} (of ${sheetCells} data-model-cell elements), value == served ${good}${bad1.length ? '; ' + bad1.join('; ') : ''}; Base case value/currency ${caseOk ? 'OK' : JSON.stringify([attr(caseTag, 'data-model-case-value'), attr(caseTag, 'data-model-case-currency')])}; visible changed: ${JSON.stringify(changed('model'))}`;

// ---- arm 2: Header ----------------------------------------------------------------------------------------------------------
const hv = (m) => ((overlay.header_figures || []).find((h) => h.mnemonic === m) || {}).value;
const idTag = tags(ident, 'data-identity-sector')[0] || '';
const h1 = !!idTag && attr(idTag, 'data-identity-sector') === hv('GICS_SECTOR_NAME') && attr(idTag, 'data-identity-country') === hv('CNTRY_OF_DOMICILE') && attr(idTag, 'data-identity-currency') === hv('CRNCY');
const dTag = tags(identAbsent, 'data-header-description').find((t) => attr(t, 'data-header-description') === 'ABSENT') || '';
const h2 = attr(dTag, 'data-header-description-reason') === DESC_REASON;
const cTag = tags(driver, 'data-driver-chart').find((t) => attr(t, 'data-driver-chart') === 'ABSENT') || '';
const h3 = !!cTag && attr(cTag, 'data-driver-chart-series') === (bundle.thesis_driver_chart || {}).driver_series;
const a2 = h1 && h2 && h3 && same('ident', 'identAbsent', 'driver');
const a2d = `identity attrs ${h1 ? 'OK' : JSON.stringify(idTag ? [attr(idTag, 'data-identity-sector'), attr(idTag, 'data-identity-country'), attr(idTag, 'data-identity-currency')] : 'absent')}; description reason ${h2 ? 'OK' : JSON.stringify(attr(dTag, 'data-header-description-reason'))}; driver series ${h3 ? 'OK' : JSON.stringify(attr(cTag, 'data-driver-chart-series'))}; visible changed: ${JSON.stringify(changed('ident', 'identAbsent', 'driver'))}`;

// ---- arm 3: Peers + Posture ----------------------------------------------------------------------------------------------
const cols = [...peersHtml.matchAll(/<li([^>]*data-absent-column="[^"]*"[^>]*)>([\s\S]*?)<\/li>/g)].map((m) => {
  const shown = L.textOf(m[2]);
  const reason = shown.includes(' -- ') ? shown.slice(shown.indexOf(' -- ') + 4) : null;
  return { col: attr(m[1], 'data-absent-column'), got: attr(m[1], 'data-absent-column-reason'), reason };
});
const p1 = cols.length >= 1 && cols.every((c) => c.got !== null && c.got === c.reason);
const vTag = tags(posture, 'data-posture-verdict').find((t) => attr(t, 'data-posture-verdict') === 'absent') || '';
const p2 = attr(vTag, 'data-posture-reason') === NOCALL_REASON;
const a3 = p1 && p2 && same('peers', 'posture');
const bc = cols.find((c) => !(c.got !== null && c.got === c.reason));
const a3d = `absent columns ${cols.length}, reason attr == shown reason ${cols.filter((c) => c.got !== null && c.got === c.reason).length}${bc ? ` (first miss ${bc.col}: ${JSON.stringify(bc.got)})` : ''}; no-call reason ${p2 ? 'OK' : JSON.stringify(attr(vTag, 'data-posture-reason'))}; visible changed: ${JSON.stringify(changed('peers', 'posture'))}`;

const arms = [
  ['Model: every figure cell and the served case carry their served value', a1, a1d],
  ['Header: identity line, description absence, driver-chart absence carry their served fact', a2, a2d],
  ['Peers and Posture: absent-column reasons and the no-call reason ride attributes', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`FWD-30 ATTRIBUTES: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
