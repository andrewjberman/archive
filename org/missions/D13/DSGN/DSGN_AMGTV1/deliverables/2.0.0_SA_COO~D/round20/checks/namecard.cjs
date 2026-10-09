/**
 * namecard.cjs -- DSGN_AMGTV1 round 20, AV-x-1 (issuer 2.0.0_SA_COO~D): THE IDENTITY CARD SHOWS THE SERVED COMPANY NAME.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO ruling msg 27874 (on COO~Z 27871: the overlay serves top-level `display_name`, never empty, never the raw key): "In
 * SecurityOverlay.tsx, show the served display_name above the ticker ... If the served name is absent, keep the ticker only, never a
 * placeholder. It stays presentation only, with no fetch change."
 * THE CONTRACT: in IdentityHeader's identity card, an element carrying `data-identity-name` holds exactly the served top-level
 * `display_name` (whitespace-trimmed), placed BEFORE the ticker in the markup; the ticker still renders. When the overlay carries no
 * display_name (absent, null or empty), there is NO data-identity-name element and no placeholder text ("Unknown", "N/A", "--",
 * "null", "undefined", "Name not available") -- the ticker only.
 * Inputs: round15/fixtures/r15c.overlay.BA_US_Equity.json with display_name "The Boeing Company" added (arm 1a) and removed (arm 1b).
 * Render: round15/checks/_load.cjs with round15 headerread.cjs's stubs (the api client, react-query).
 * Arms:
 *   1  THE CHECKOUT: (a) data-identity-name reads "The Boeing Company" and precedes "BA US"; (b) no data-identity-name, no placeholder,
 *      "BA US" still renders.
 *   2  NEGATIVE: the pinned base SecurityOverlay.tsx (portal f73cd009; NAMECARD_BASE overrides) carries no data-identity-name.
 *   3  PLANTED: a placeholder name (PLACEHOLDER), a name after the ticker (ORDER), the raw key as the name (VALUE) -- each rejected; a
 *      correct card passes.
 * Prints one line per arm and "THE IDENTITY CARD SHOWS THE SERVED COMPANY NAME: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const R15 = path.join(__dirname, '..', '..', 'round15');
const PIN = process.env.NAMECARD_BASE || 'f73cd009';
const SA = 'src/pages/SecurityAnalysis/';
const raw = JSON.parse(fs.readFileSync(path.join(R15, 'fixtures', 'r15c.overlay.BA_US_Equity.json'), 'utf8'));
const OV0 = raw && raw.payload && raw._capture_note ? raw.payload : raw;
const NAME = 'The Boeing Company';
const TICKER = 'BA US';
// Not "--": the served sector line reads "Industrials -- US".
const PLACEHOLDER = /\b(unknown|n\/a|null|undefined|name not available)\b/i;
const textOf = (h) => h.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();
function nameEl(html) {
  const at = html.indexOf('data-identity-name');
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const start = html.indexOf('>', at) + 1;
  const end = html.indexOf('</' + tag, start);
  return { text: textOf(html.slice(start, end)), at };
}
function faults(html, served) {
  const f = [];
  const t = textOf(html);
  const el = nameEl(html);
  const tickAt = html.indexOf(TICKER);
  if (tickAt < 0) f.push('TICKER: the ticker "BA US" does not render');
  if (served) {
    if (!el) f.push('MISSING: no data-identity-name element');
    else {
      if (el.text !== served) f.push(`VALUE: data-identity-name reads "${el.text}" for served "${served}"`);
      if (tickAt >= 0 && el.at > tickAt) f.push('ORDER: the name sits after the ticker');
      if (PLACEHOLDER.test(el.text)) f.push(`PLACEHOLDER: "${el.text}"`);
    }
  } else {
    if (el) f.push(`PLACEHOLDER: a data-identity-name element renders with no served name ("${el.text}")`);
    const head = t.slice(0, 200);
    if (PLACEHOLDER.test(head)) f.push(`PLACEHOLDER: placeholder text in the header ("${head.slice(0, 80)}")`);
  }
  return f;
}

let L;
function render(ov) {
  if (!L) {
    L = require(path.join(R15, 'checks', '_load.cjs'));
    const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
    L.stubSource('src/api/api-client.ts', api);
    L.stubSource('src/api/api-client', api);
    L.stubSource('@tanstack/react-query', { __esModule: true,
      useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
      useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }) });
  }
  // DSGN_AMGTV1 round 60 RE-ANCHOR (the checkout arm, "the ticker still renders"): since round 28 the ticker is drawn on the identity card's
  // `panel` prop, which the loader's generic stub (children only) drops. This check supplies a GraphicCard stub that draws the panel and the
  // body, so the ticker is read where the page puts it. The claim is unchanged: the name above the ticker, the ticker still renders.
  L.stubSource('src/ui/components/graphic/GraphicCard.tsx', { __esModule: true,
    GraphicCard: ({ panel, children, as, flat, panelClassName, bodyClassName, ...rest }) => L.React.createElement('div', rest, panel, children) });
  L.hookState.impl = { useCollectedChatter: () => undefined, useThesisBundle: () => undefined, usePeerSet: () => undefined, useManagement: () => undefined };
  const m = L.source(SA + 'components/SecurityOverlay.tsx');
  return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} });
}

const withName = { ...OV0, name: NAME, name_source: 'crosswalk', display_name: NAME, display_name_source: 'crosswalk' };
const noName = { ...OV0 }; delete noName.display_name; delete noName.name;
const f1 = [];
try {
  f1.push(...faults(render(withName), NAME).map((x) => 'A ' + x));
  f1.push(...faults(render(noName), null).map((x) => 'B ' + x));
} catch (e) { f1.push('RENDER: ' + String(e.message).split('\n')[0]); }
const a1 = f1.length === 0;

const f2 = [];
const s = spawnSync('git', ['-C', path.join(ROOT, 'portal'), 'show', `${PIN}:${SA}components/SecurityOverlay.tsx`], { encoding: 'utf8', maxBuffer: 1 << 24 });
if (s.status !== 0 || !s.stdout) f2.push(`INPUT MISSING: git show ${PIN} rc=${s.status}`);
else if (/data-identity-name/.test(s.stdout)) f2.push(`the base at ${PIN} already carries data-identity-name -- the check cannot tell base from fix`);
const a2 = f2.length === 0;

const f3 = [];
const card = (name, before = true) => {
  const n = name === null ? '' : `<div data-identity-name="">${name}</div>`;
  return `<div>${before ? n : ''}<div>${TICKER}</div>${before ? '' : n}</div>`;
};
if (faults(card(NAME), NAME).length) f3.push(`a correct card is rejected: ${faults(card(NAME), NAME)[0]}`);
if (faults(card(null), null).length) f3.push(`a correct ticker-only card is rejected: ${faults(card(null), null)[0]}`);
const M = [['placeholder', card('Unknown'), NAME, 'PLACEHOLDER'], ['after the ticker', card(NAME, false), NAME, 'ORDER'], ['raw key', card('BA_US_Equity'), NAME, 'VALUE']];
const caught = [];
for (const [n, h, served, cls] of M) { if (faults(h, served).some((x) => x.startsWith(cls + ':'))) caught.push(n); else f3.push(`mutant "${n}" not rejected as ${cls}`); }
const a3 = f3.length === 0;

const arms = [
  ['the checkout: the served display_name above the ticker; no name served -> the ticker only, no placeholder', a1, a1 ? '0 faults (named, unnamed)' : `${f1.length} faults: ${f1.join(' | ')}`],
  [`NEGATIVE: the base SecurityOverlay.tsx (${PIN}) has no data-identity-name`, a2, a2 ? 'base lacks the name element' : f2[0]],
  ['PLANTED: a placeholder, a name after the ticker and the raw key are rejected; correct cards pass', a3, a3 ? `${caught.length} of ${M.length} rejected` : f3[0]],
];
let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE IDENTITY CARD SHOWS THE SERVED COMPANY NAME: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
