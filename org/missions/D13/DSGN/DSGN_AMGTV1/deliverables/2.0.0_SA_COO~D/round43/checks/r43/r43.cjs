/**
 * r43.cjs -- DSGN_AMGTV1 round 43 issuer CHECK (2.0.0_SA_COO~D): NO BARE NUMBER AS A PEER TICKER; THE PLAIN NAME WHEREVER IT IS SERVED.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round43/checks/r43/r43.cjs"
 *
 * Why: ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND41.md @0bcdb77515 (msg 29884), ROUND 43:
 *   (1) FWD-8: a numeric peer member shows its resolved key or its served ticker_reason, never a bare number. The deployed producer
 *       (2lUlZomo) serves, per member, `ticker` (still the exchange number for 94 members), and either `security_key` (21; e.g.
 *       688910 -> TSM_US_Equity) or a plain `ticker_reason` (73). PeersTab prints CscRow.ticker, which buildCscTable fills with
 *       member.ticker today.
 *   (2) FWD-27: the plain `display_name` wherever a row's `name` is printed and `display_name` is served. Census (issuer, DEV
 *       7d1ea524): components/PriceBars.tsx:191 and components/RankedList.tsx:131 print row.name ("SYNOPSYS INC") on the price
 *       face; cscTable.ts:184 (peer label) and postureCites.ts:298 (peer cite) print member/peer name.
 * Fixtures: ../../fixtures/*.deployed-2lUlZomo.json, read-only invokes of the deployed API (MSFT's peers; the trending price list).
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 NO BARE NUMBER AS A TICKER (FWD-8): buildCscTable on MSFT's deployed peers: 0 member rows whose ticker is all digits; the
 *     resolved member (688910 -> TSM_US_Equity) shows "TSM US"; each of the 3 unresolved numeric members shows its served
 *     ticker_reason verbatim; GOOG and GOOGL are unchanged.
 *   2 THE PRICE FACE PRINTS THE PLAIN NAME (FWD-27): the REAL PriceBars rendered on the deployed price list shows "Synopsys Inc",
 *     "Adobe Inc" and "Cadence Design Sys Inc" and none of "SYNOPSYS INC", "ADOBE INC", "CADENCE DESIGN SYS".
 *   3 EVERY OTHER SERVED-NAME SITE PREFERS display_name (source): RankedList's row name, cscTable's member label and postureCites'
 *     peer cite each read `display_name` before `name`.
 *   4 KEEP: a price row with no display_name still prints its name; a peer member with a letter ticker keeps it; the subject row
 *     keeps its label; no row loses its ticker when nothing better is served.
 *   5 PLANTED: the graders refuse a bare number, a vendor-capitals face and a name-first read, and accept the intended forms.
 * Renders through round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));

const FX = path.join(__dirname, '..', '..', 'fixtures');
const pay = (f) => JSON.parse(fs.readFileSync(path.join(FX, f), 'utf8')).payload;
const PEERS = pay('peers.MSFT_US_Equity.deployed-2lUlZomo.json');
const RANK = pay('rankings.trending.price.deployed-2lUlZomo.json');
const portal = path.join(process.cwd(), 'portal');
const OV = Object.fromEntries((process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]));
const src = (rel) => { const f = OV[rel] || path.join(portal, rel); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : ''; };
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(html.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

const numericMembers = (PEERS.members || []).filter((m) => /^\d+$/.test(String(m.ticker || '')));
function gradeTickers(rows) {
  const f = [];
  const memberRows = rows.filter((r) => !r.isSubject);
  const bare = memberRows.filter((r) => /^\d+$/.test(String(r.ticker || '').trim()));
  if (bare.length) f.push(`${bare.length} member row(s) show a bare number: ${bare.map((r) => r.ticker).join(', ')}`);
  for (const m of numericMembers) {
    const row = memberRows.find((r) => r.label === m.display_name || r.label === m.name);
    if (!row) { f.push(`no row for ${m.name}`); continue; }
    if (m.security_key) {
      const want = m.security_key.replace(/_Equity$/, '').replace(/_/g, ' ');
      if (row.ticker !== want) f.push(`${m.name}: ticker "${row.ticker}" (want "${want}" from ${m.security_key})`);
    } else if (m.ticker_reason) {
      if (row.ticker !== m.ticker_reason) f.push(`${m.name}: ticker cell "${row.ticker}" is not the served ticker_reason`);
    }
  }
  for (const t of ['GOOG', 'GOOGL']) if (!memberRows.some((r) => r.ticker === t)) f.push(`${t} lost its ticker`);
  return f;
}
const PLAIN = ['Synopsys Inc', 'Adobe Inc', 'Cadence Design Sys'];
const CAPS = ['SYNOPSYS INC', 'ADOBE INC', 'CADENCE DESIGN SYS'];
function gradeFace(t) {
  const f = [];
  for (const w of PLAIN) if (!t.includes(w)) f.push(`face lacks "${w}"`);
  for (const w of CAPS) if (t.includes(w)) f.push(`face prints "${w}"`);
  return f;
}
function displayFirst(code, re) {
  const m = re.exec(code);
  if (!m) return 'site not found';
  const seg = code.slice(m.index, m.index + 400);
  const d = seg.indexOf('display_name'); const n = seg.search(/\.name\b/);
  return d >= 0 && (n < 0 || d < n) ? null : 'reads name before display_name';
}

const arms = [];
let csc = null;
try { csc = L.source('src/pages/SecurityAnalysis/cscTable.ts'); } catch (e) { console.log('LOADER ERROR: cscTable.ts :: ' + String(e.message).split('\n')[0]); process.exit(3); }
let rows = [];
try { rows = csc.buildCscTable(PEERS, 'Microsoft Corp').rows; } catch (e) { arms.push(['RENDER', false, 'buildCscTable threw: ' + String(e.message).split('\n')[0]]); }
{
  const f = gradeTickers(rows);
  arms.push(['NO BARE NUMBER AS A PEER TICKER (FWD-8)', f.length === 0, f.length ? f.join(' | ') : `${numericMembers.length} numeric members: resolved -> "TSM US", unresolved -> served reason; GOOG/GOOGL kept`]);
}
let faceText = '';
try {
  const PB = L.source('src/pages/SecurityAnalysis/components/PriceBars.tsx');
  faceText = text(L.render(PB.PriceBars, { rows: RANK.rows, asOfDate: RANK.as_of_date, onSelectSecurity: () => {} }));
} catch (e) { faceText = ''; arms.push(['RENDER', false, 'PriceBars threw: ' + String(e.message).split('\n')[0]]); }
{
  const f = faceText ? gradeFace(faceText) : ['PriceBars rendered nothing'];
  arms.push(['THE PRICE FACE PRINTS THE PLAIN NAME (FWD-27)', f.length === 0, f.length ? f.join(' | ') : 'Synopsys Inc, Adobe Inc, Cadence Design Sys shown; 0 vendor-capitals names']);
}
{
  const f = [];
  const sites = [
    ['components/RankedList.tsx', /function\s+\w*[Nn]ame\w*\s*\(\s*row/],
    ['cscTable.ts', /for \(const member of peers\.members/],
    ['postureCites.ts', /peer: \$\{peer\.ticker\}/],
  ];
  for (const [rel, re] of sites) {
    const code = src('src/pages/SecurityAnalysis/' + rel);
    const citeLine = code.split('\n').find((l) => re.test(l)) || '';
    const r = code ? (rel === 'postureCites.ts' ? (/display_name/.test(citeLine) && citeLine.indexOf('display_name') < citeLine.lastIndexOf('peer.name') ? null : 'peer cite never reads display_name first') : displayFirst(code, re)) : 'file missing';
    if (r) f.push(`${rel}: ${r}`);
  }
  arms.push(['EVERY OTHER SERVED-NAME SITE PREFERS display_name (source)', f.length === 0, f.length ? f.join(' | ') : 'RankedList, cscTable member label, postureCites peer cite read display_name first']);
}
{
  const f = [];
  const noDisp = RANK.rows.slice(0, 3).map((r) => Object.assign({}, r, { display_name: undefined, name: r.name }));
  try {
    const PB = L.source('src/pages/SecurityAnalysis/components/PriceBars.tsx');
    const t = text(L.render(PB.PriceBars, { rows: noDisp, asOfDate: RANK.as_of_date, onSelectSecurity: () => {} }));
    if (!t.includes(noDisp[0].name)) f.push('a row with no display_name lost its name');
  } catch (e) { f.push('PriceBars (no display_name) threw'); }
  const subject = rows.find((r) => r.isSubject);
  if (!subject || !/Microsoft Corp \(subject\)/.test(subject.label)) f.push('subject row label changed');
  const letters = rows.filter((r) => !r.isSubject && /^[A-Z]{1,5}$/.test(String(r.ticker || '')));
  if (letters.length < 8) f.push(`${letters.length} letter tickers kept (8 expected)`);
  arms.push(['KEEP: name fallback, subject label, letter tickers', f.length === 0, f.length ? f.join(' | ') : 'fallback to name; subject unchanged; 8 letter tickers kept']);
}
{
  const f = [];
  const mk = (ticker, label) => ({ label, ticker, isSubject: false });
  const good = [mk('GOOG', 'Alphabet Inc. Class C'), mk('GOOGL', 'Alphabet Inc. Class A')]
    .concat(numericMembers.map((m) => mk(m.security_key ? m.security_key.replace(/_Equity$/, '').replace(/_/g, ' ') : m.ticker_reason, m.display_name || m.name)));
  if (gradeTickers(good).length) f.push('good ticker rows refused: ' + gradeTickers(good).join(';'));
  const bad = good.map((r, i) => (i === 2 ? Object.assign({}, r, { ticker: numericMembers[0].ticker }) : r));
  if (!gradeTickers(bad).length) f.push('a bare number accepted');
  if (!gradeFace('SYNOPSYS INC Adobe Inc Cadence Design Sys').length) f.push('a vendor-capitals face accepted');
  if (gradeFace('Synopsys Inc Adobe Inc Cadence Design Sys Inc').length) f.push('a plain face refused');
  if (!displayFirst('function rowName(row) { return row.name ?? row.display_name }', /function\s+\w*[Nn]ame\w*\s*\(\s*row/)) f.push('a name-first read accepted');
  arms.push(['PLANTED: the graders refuse a bare number, vendor capitals and a name-first read, and accept the intended forms', f.length === 0, f.length ? f.join(' | ') : '3 of 3 faults refused; 2 of 2 good forms accepted']);
}

const TITLE = 'NO BARE NUMBER AS A PEER TICKER; THE PLAIN NAME WHEREVER IT IS SERVED';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 5 ? 0 : 1);
