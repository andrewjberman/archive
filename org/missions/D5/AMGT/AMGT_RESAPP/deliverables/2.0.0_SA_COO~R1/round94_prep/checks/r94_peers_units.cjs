/* AMGT_RESAPP round-94 PREP -- the peers table names the unit its cap values carry, and the Ticker cell says "no ticker held" instead of a company name.
 *
 *   cd <the PORTAL worktree> && node ../org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round94_prep/checks/r94_peers_units.cjs
 *
 * INSTRUMENT: the ACTUAL PeersTab.tsx of the working directory's portal, server-rendered (the loader of peersPattern.harness.cjs, cut at its fixture marker)
 * over the LIVE served peers and header payloads of ASML, ROG and BA (`../fixtures/peers_and_header_figures_ASML_ROG_BA_20261011.json`, read 2026-10-11).
 * The CVO's browser walk (C-S67) read "Mkt Cap (local)" over USD peer values and company names in the Ticker column for Tencent, SK hynix, Samsung and Novo.
 *
 *   H1 the Mkt Cap heading names the codes its figures carry, sorted, comma-separated: ASML (subject EUR, peers USD) reads "Mkt Cap (EUR, USD)", ROG (CHF, USD)
 *      reads "Mkt Cap (CHF, USD)".
 *   H2 control: a page whose figures all carry one code reads "Mkt Cap (USD)" (BA).
 *   T1 every member whose identity is not MEASURED and whose served ticker is empty, all digits or SEDOL-shaped prints "no ticker held" in the Ticker cell
 *      (ASML: Tencent, SK hynix, Samsung x2 where present; ROG: Novo Nordisk): never the company name.
 *   T2 control: a MEASURED member prints its house-form ticker unchanged ("INTC US").
 *   T3 control: the Name cell of every member row still prints the company name.
 * Verdict: R94 PEERS UNITS: YES|NO (exit 0|1). At the base (portal DEV c96efe17 and 11f25102dd) H1 and T1 FAIL, H2, T2, T3 PASS.
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const PORTAL = process.cwd().replace(/\\/g, '/');
const HARNESS = PORTAL + '/src/pages/SecurityAnalysis/__harness__/peersPattern.harness.cjs';
const FIXTURE = path.join(__dirname, '..', 'fixtures', 'peers_and_header_figures_ASML_ROG_BA_20261011.json');
if (!fs.existsSync(HARNESS)) {
  console.log('FAIL no peersPattern harness under the working directory: run this from the portal worktree root');
  process.exit(2);
}
let text = fs.readFileSync(HARNESS, 'utf8');
const marker = text.indexOf('// -- FIXTURE.');
if (marker < 0) throw new Error('fixture marker not found in the harness');
text = text.slice(0, marker)
  .replace("path.resolve(__dirname, '../../../..')", "'" + PORTAL + "'")
  .replace("PanelHeader: box,", "PanelHeader: box, PanelFooter: box,");
const tail = [
  "const pages = JSON.parse(fs.readFileSync(" + JSON.stringify(FIXTURE) + ", 'utf8'));",
  "const strip = (h) => h.replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim();",
  "const render = (key) => {",
  "  const doc = pages[key];",
  "  peer = doc.peers;",
  "  hooks.useSecurityOverlay = () => ({ data: doc.overlay, isLoading: false });",
  "  return renderToStaticMarkup(React.createElement(PeersTab, { securityKey: key }));",
  "};",
  "const heading = (html) => { const m = html.match(/<th[^>]*data-csc-column-code=\"mkt_val_sec\"[^>]*>([\\s\\S]*?)<\\/th>/); return m ? strip(m[1]) : null; };",
  "const memberRows = (html) => [...html.matchAll(/<tr[^>]*data-csc-row=\"member\"[^>]*>([\\s\\S]*?)<\\/tr>/g)].map((m) => {",
  "  const tds = [...m[1].matchAll(/<td[^>]*>([\\s\\S]*?)<\\/td>/g)].map((t) => strip(t[1]));",
  "  return { name: tds[0], ticker: tds[1] };",
  "});",
  "const results = [];",
  "const say = (ok, label, detail) => { console.log((ok ? 'PASS ' : 'FAIL ') + label + (detail ? '  [' + detail + ']' : '')); results.push(ok); };",
  "const html = { ASML_NA_Equity: render('ASML_NA_Equity'), ROG_SW_Equity: render('ROG_SW_Equity'), BA_US_Equity: render('BA_US_Equity') };",
  "const h = { ASML: heading(html.ASML_NA_Equity), ROG: heading(html.ROG_SW_Equity), BA: heading(html.BA_US_Equity) };",
  "say(h.ASML === 'Mkt Cap (EUR, USD)' && h.ROG === 'Mkt Cap (CHF, USD)', 'H1 the Mkt Cap heading names the codes its figures carry', 'ASML ' + JSON.stringify(h.ASML) + ', ROG ' + JSON.stringify(h.ROG));",
  "say(h.BA === 'Mkt Cap (USD)', 'H2 control: one code reads that code', 'BA ' + JSON.stringify(h.BA));",
  "const want = /tencent|hynix|samsung|novo nordisk/i;",
  "let seen = 0, bad = [];",
  "for (const key of ['ASML_NA_Equity', 'ROG_SW_Equity']) {",
  "  for (const r of memberRows(html[key])) {",
  "    if (want.test(r.name || '')) { seen++; if (r.ticker !== 'no ticker held') bad.push(r.name + ' -> ' + r.ticker); }",
  "  }",
  "}",
  "say(seen >= 4 && bad.length === 0, 'T1 a member with no held ticker prints \"no ticker held\", not a company name', seen + ' rows read, wrong: ' + JSON.stringify(bad));",
  "const intel = memberRows(html.ASML_NA_Equity).find((r) => /^Intel/.test(r.name || ''));",
  "say(!!intel && intel.ticker === 'INTC US', 'T2 control: a MEASURED member prints its house-form ticker', intel ? intel.ticker : 'no Intel row');",
  "const served = new Set(pages.ASML_NA_Equity.peers.members.map((m) => strip(String(m.display_name || m.name || ''))));",
  "const rows = memberRows(html.ASML_NA_Equity);",
  "say(rows.length === 12 && rows.every((r) => served.has(r.name)), 'T3 control: the Name cell of every member row still prints the served company name', rows.length + ' rows');",
  "console.log('   arms passed ' + results.filter(Boolean).length + ' of ' + results.length);",
  "const verdict = results.every(Boolean);",
  "console.log('R94 PEERS UNITS: ' + (verdict ? 'YES' : 'NO'));",
  "process.exit(verdict ? 0 : 1);",
].join('\n');
const out = path.join(os.tmpdir(), 'r94_peers_units_gen_' + process.pid + '.cjs');
fs.writeFileSync(out, text + tail);
process.on('exit', () => { try { fs.unlinkSync(out); } catch (e) { /* the temp file stays */ } });
require(out);
