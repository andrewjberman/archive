/**
 * codeface.cjs -- DSGN_AMGTV1 round 22, AV-z-1 (issuer 2.0.0_SA_COO~D): NO CODE-SHAPED TOKEN ON THE EXEC, POSTURE OR PEERS FACE.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-21 analysis @e14de1769c section 3A row A1 (FWD-11): Exec, Posture and Peers render a plain reason whenever the served
 * string carries a code, an id, `_US_Equity` or a file name. The page keeps ONE guard: it never prints a code-shaped token and falls
 * back to a plain generic reason; the served string may ride a data- attribute.
 * Census classes (visible text only; attributes are not text):
 *   snake      [a-z]+_[a-z0-9_]+          (a field code: ey_ntm, cash_mv, debt_assets)
 *   equity     _Equity                    (a security key)
 *   json       \.json                     (a file name)
 *   absent     ABSENT | UNMAPPED          (a machine state word)
 *   upper      [A-Z][A-Z0-9]*_[A-Z0-9_]+  (a vendor mnemonic or a state code such as PRESENT_NOT_CARRIED)
 * Inputs: portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json (thesis, peers), with the served strings
 * PLANTED that the analysis names: the Lusha skip reason "no declared domain for VLO_US_Equity in domains.json", an absent-column
 * reason naming `ey_ntm` and `factor_metadata_registry.json`, and the fixture's own posture claim "fit scores are ABSENT".
 * Render: round15/checks/_load.cjs (the real tab sources; estate chrome stubbed; hooks return the fixture).
 * Arms:
 *   1  THE CHECKOUT: ExecManagementTab, PostureTab and PeersTab (absent-column disclosure open in the markup) render with the
 *      plants; the visible-text census reads 0 tokens over the three faces.
 *   2  POSITIVE CONTROL: the census reads >= 1 on each planted served string set as visible text (5 of 5 classes caught), and 0 on
 *      a plain sentence whose code rides only a data- attribute.
 *   3  PLAIN SERVED WORDS STAY: with a PLAIN Lusha skip reason and the fixture's plain absent-column reasons, the visible text still
 *      carries each plain reason verbatim (the guard does not blank served words that carry no code).
 * Prints one line per arm and "NO CODE ON THE EXEC, POSTURE OR PEERS FACE: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const FIX = JSON.parse(fs.readFileSync(path.join(L.base, SA + '__harness__/tabsFixture.BA_US_Equity.json'), 'utf8'));
const KEY = FIX.security_key;

const CLASSES = {
  snake: /\b[a-z]+_[a-z0-9_]+\b/g,
  equity: /_Equity\b/g,
  json: /\.json\b/g,
  absent: /\b(ABSENT|UNMAPPED)\b/g,
  upper: /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/g,
};
function census(html) {
  const text = L.textOf(html);
  const out = { total: 0, hits: [] };
  for (const [k, re] of Object.entries(CLASSES)) {
    const m = text.match(re) || [];
    out[k] = m.length;
    out.total += m.length;
    for (const h of m.slice(0, 3)) out.hits.push(`${k}:${h}`);
  }
  return out;
}

const PLANT_LUSHA = 'no declared domain for VLO_US_Equity in domains.json';
const PLANT_COLUMN = 'no ey_ntm factor in factor_metadata_registry.json';
const PLAIN_LUSHA = 'the issuer has no web domain on file';

function clone(x) { return JSON.parse(JSON.stringify(x)); }
function fixtureWith(lushaReason, plantColumn) {
  const f = clone(FIX);
  const m = f.thesis.management || (f.thesis.management = {});
  m.lusha_enrichment = { status: 'SKIPPED', reason: lushaReason };
  if (plantColumn && f.peers.csc_columns && Array.isArray(f.peers.csc_columns.absent) && f.peers.csc_columns.absent[0]) {
    f.peers.csc_columns.absent[0].reason = PLANT_COLUMN;
  }
  return f;
}

function renderTabs(f) {
  L.hookState.impl = {
    useThesisBundle: (k) => (k === undefined || k === null || k === KEY ? f.thesis : undefined),
    usePeerSet: (k) => (k === undefined || k === null || k === KEY ? f.peers : undefined),
    useSecurityOverlay: (k) => (k === undefined || k === null || k === KEY ? f.overlay : undefined),
    useManagement: () => f.thesis.management,
    useCollectedChatter: () => undefined,
  };
  const out = {};
  const tabs = [
    ['exec', 'tabs/ExecManagementTab.tsx', 'ExecManagementTab'],
    ['posture', 'tabs/PostureTab.tsx', 'PostureTab'],
    ['peers', 'tabs/PeersTab.tsx', 'PeersTab'],
  ];
  for (const [id, rel, name] of tabs) {
    const m = L.source(SA + rel);
    out[id] = L.render(m[name], { securityKey: KEY });
  }
  return out;
}

const arms = [];

// Arm 1 -- the checkout with the plants.
{
  const f = [];
  let html;
  try { html = renderTabs(fixtureWith(PLANT_LUSHA, true)); } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  if (html) {
    for (const [id, h] of Object.entries(html)) {
      if (!h || L.textOf(h).length < 20) f.push(`${id}: the face rendered no text`);
      const c = census(h);
      if (c.total > 0) f.push(`${id}: ${c.total} token(s) [${c.hits.join(', ')}]`);
    }
  }
  arms.push(['the checkout: Exec, Posture and Peers print no code-shaped token with the planted served strings', f.length === 0,
    f.length === 0 ? '0 tokens over 3 faces' : `${f.length} fault(s): ${f.join(' | ')}`]);
}

// Arm 2 -- the instrument catches each class; attributes are not text.
{
  const f = [];
  const planted = [
    ['snake', `<p>Lusha enrichment: ${PLANT_COLUMN}</p>`],
    ['equity', `<p>${PLANT_LUSHA}</p>`],
    ['json', '<p>read from domains.json</p>'],
    ['absent', '<li>Shares: ABSENT -- no share-count factor code</li>'],
    ['upper', '<td>PRESENT_NOT_CARRIED</td>'],
  ];
  let caught = 0;
  for (const [cls, h] of planted) {
    const c = census(h);
    if (c[cls] >= 1) caught += 1; else f.push(`class ${cls} not caught in ${h}`);
  }
  const clean = census('<p data-reason="ey_ntm in factor_metadata_registry.json" data-key="VLO_US_Equity">Forward earnings yield is not in the comparison map.</p>');
  if (clean.total !== 0) f.push(`a plain sentence with its code in attributes read ${clean.total} [${clean.hits.join(', ')}]`);
  arms.push(['POSITIVE CONTROL: each planted served code string reads >= 1; a plain sentence with attribute-only codes reads 0', f.length === 0,
    f.length === 0 ? `${caught} of ${planted.length} classes caught; clean sentence 0` : f.join(' | ')]);
}

// Arm 3 -- plain served words still print verbatim.
{
  const f = [];
  let html;
  try { html = renderTabs(fixtureWith(PLAIN_LUSHA, false)); } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  if (html) {
    const execText = L.textOf(html.exec);
    if (!execText.includes(PLAIN_LUSHA)) f.push(`exec: the plain Lusha skip reason "${PLAIN_LUSHA}" is not on the face`);
    // AMENDMENT 1 (issuer, round 23, 2026-10-02 ~08:5xZ; row DSGN_AMGTV1-Z-W71-S1): CTO round-22 ruling 1 (@eee9380be7) puts the
    // Peers absent-column reason on the face in PAGE-composed reader words and keeps R-1's served reason in
    // `data-absent-column-reason`, so a plain served reason is PRESERVED when it is on the face OR carried verbatim in that
    // attribute. The Exec clause (the plain Lusha reason prints verbatim) is unchanged.
    const peersText = L.textOf(html.peers);
    const decodeAttr = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    const carried = new Set(Array.from(html.peers.matchAll(/data-absent-column-reason="([^"]*)"/g)).map((m) => decodeAttr(m[1])));
    const plainReasons = (FIX.peers.csc_columns.absent || [])
      .map((c) => c.reason)
      .filter((r) => typeof r === 'string' && r && census(`<p>${r}</p>`).total === 0);
    let shown = 0;
    for (const r of plainReasons) { if (peersText.includes(r) || carried.has(r)) shown += 1; else f.push(`peers: plain reason neither on the face nor carried: "${r.slice(0, 60)}"`); }
    if (plainReasons.length === 0) f.push('INPUT: the fixture carries no plain absent-column reason to read');
    arms.push(['PLAIN SERVED WORDS STAY: a plain Lusha reason prints verbatim; each plain absent-column reason is on the face or carried', f.length === 0,
      f.length === 0 ? `exec 1 of 1, peers ${shown} of ${plainReasons.length}` : `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}`]);
  } else {
    arms.push(['PLAIN SERVED WORDS STAY: a plain Lusha reason prints verbatim; each plain absent-column reason is on the face or carried', false, f.join(' | ')]);
  }
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`NO CODE ON THE EXEC, POSTURE OR PEERS FACE: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
