/**
 * precision.cjs -- DSGN_AMGTV1 round 18, AV-i-1 (issuer 2.0.0_SA_COO~D): THE PRICE BARS PRINT ONE DECIMAL, THE WHOLE VALUE IN AN ATTRIBUTE.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO ruling msg 27760 = CONTRACT amendment 3 @b9d096f6dd: "the bars print *_pct to ONE decimal with sign and '%', and the whole
 * served value stays in a data attribute on the bar (e.g. data-price-value). Rounding never rescales." The acceptance walk
 * (tmp/ui-walk/20261001T101104Z, 004-lead-Trending-Price.png) printed "-25.40217088783747%" and the values clipped at the panel edge.
 * Input: round15/fixtures/r15a.rankings.TRENDING_PRICE.return30d.json with every return_30d_pct given live-like float precision
 * here (v + sign(v) * 0.0123456789012, so each value carries 13+ decimals; the |value| order is unchanged).
 * Render: round15/checks/_load.cjs with round15 pricebars.cjs's stubs (LeadPanel on PRICE; the rankings hook returns the fixture).
 * Arms:
 *   1  THE CHECKOUT: one data-price-bar per row; each bar's visible text holds EXACTLY ONE percent token of the form
 *      <sign><digits>.<one digit>% equal to the served value rounded to one decimal (Number(v.toFixed(1)), an explicit "+" for a
 *      positive, "-" or U+2212 for a negative; "-0.0" never printed for a value that rounds to zero is not required); the bar element
 *      (or a descendant) carries data-price-value whose value parses to EXACTLY the served value (no rounding); every printed token
 *      is at most 7 characters (the clip proxy -- the live PNG is the real read); the order stays descending by |value|.
 *   2  NEGATIVE: the pinned base source (portal 788afb2e: components/PriceBars.tsx) prints the value without one-decimal rounding
 *      and carries no data-price-value -- read from `git -C portal show 788afb2e:<path>`; PRECISION_BASE overrides the pin.
 *   3  PLANTED: synthetic bar markups -- two decimals printed (DECIMALS), the attribute missing (ATTR), the attribute rounded
 *      (ATTR), the printed value x100 (VALUE) -- are each rejected; a correct markup passes.
 * Prints one line per arm and "THE PRICE BARS PRINT ONE DECIMAL: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const R15 = path.join(__dirname, '..', '..', 'round15');
const PIN = process.env.PRECISION_BASE || '788afb2e';
const PB = 'src/pages/SecurityAnalysis/components/PriceBars.tsx';
const LP = 'src/pages/SecurityAnalysis/components/LeadPanel.tsx';

const raw = JSON.parse(fs.readFileSync(path.join(R15, 'fixtures', 'r15a.rankings.TRENDING_PRICE.return30d.json'), 'utf8'));
const priceSet = raw && raw.payload && raw._capture_note ? raw.payload : raw;
for (const r of priceSet.rows) if (typeof r.return_30d_pct === 'number') r.return_30d_pct = r.return_30d_pct + Math.sign(r.return_30d_pct || 1) * 0.0123456789012;
const ROWS = priceSet.rows;
const keyOf = (r) => (r.security_key === null || r.security_key === undefined ? r.ticker : r.security_key);
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const textOf = (h) => h.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/\s+/g, ' ').trim();

/** Split the markup into one chunk per data-price-bar element: from its attribute to the next bar's (enough for a row's text). */
function barChunks(html) {
  const idx = [];
  const re = /data-price-bar="([^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) idx.push([m.index, unesc(m[1])]);
  return idx.map(([at, key], i) => {
    const open = html.lastIndexOf('<', at);
    const end = i + 1 < idx.length ? html.lastIndexOf('<', idx[i + 1][0]) : html.length;
    return { key, chunk: html.slice(open, end) };
  });
}

function faults(html, rows) {
  const f = [];
  const byKey = new Map(rows.map((r) => [keyOf(r), r]));
  const bars = barChunks(html);
  if (bars.length !== rows.length) f.push(`COUNT: ${bars.length} bars for ${rows.length} rows`);
  let prev = Infinity;
  for (const { key, chunk } of bars) {
    const r = byKey.get(key);
    if (!r) { f.push(`COUNT: a bar for an unserved key ${key}`); continue; }
    const v = r.return_30d_pct;
    if (Math.abs(v) > prev + 1e-12) f.push(`ORDER: ${key} out of |value| order`);
    prev = Math.abs(v);
    const text = textOf(chunk);
    const toks = [...text.matchAll(/([+\-−]?)(\d+(?:\.\d+)?)%/g)];
    if (toks.length !== 1) { f.push(`VALUE: ${key} prints ${toks.length} percent tokens ("${text.slice(0, 70)}")`); continue; }
    const [tok, sign, num] = toks[0];
    if (!/^\d+\.\d$/.test(num)) f.push(`DECIMALS: ${key} prints "${tok}" -- not one decimal`);
    const printed = sign === '' ? NaN : (sign === '+' ? 1 : -1) * Number(num);
    const want = Number(v.toFixed(1));
    if (!(Math.abs(printed - want) < 1e-9) && !(want === 0 && Number(num) === 0)) f.push(`VALUE: ${key} prints "${tok}" for served ${v} (want ${want.toFixed(1)})`);
    if (tok.length > 7) f.push(`CLIP: ${key} prints a ${tok.length}-character value "${tok}"`);
    const attr = (/data-price-value="([^"]*)"/.exec(chunk) || [])[1];
    if (attr === undefined) f.push(`ATTR: ${key} carries no data-price-value`);
    else if (Number(unesc(attr)) !== v) f.push(`ATTR: ${key} data-price-value="${attr}" is not the whole served value ${v}`);
  }
  return f;
}

function render() {
  const L = require(path.join(R15, 'checks', '_load.cjs'));
  const React = L.React;
  const icons = {};
  L.stubSource('lucide-react', new Proxy({}, { get(_t, k) { if (k === '__esModule') return true; if (typeof k !== 'string') return undefined; if (!icons[k]) icons[k] = () => React.createElement('svg', { 'data-icon': k }); return icons[k]; } }));
  const Segmented = (p) => React.createElement('div', { role: 'group', 'aria-label': p.ariaLabel }, ...(p.options || []).map((o, i) => React.createElement('button', { key: i }, o.label)));
  const ctl = {};
  const controls = new Proxy({}, { get(_t, k) { if (k === '__esModule') return true; if (typeof k !== 'string') return undefined; if (k === 'Segmented') return Segmented; if (!ctl[k]) ctl[k] = (p) => React.createElement('div', { 'data-stub': k }, (p || {}).children); return ctl[k]; } });
  for (const k of ['src/ui/components/Controls', 'src/ui/components/Controls.tsx', 'src/ui/components/Controls.ts']) L.stubSource(k, controls);
  for (const k of ['src/hooks/useAuth', 'src/hooks/useAuth.ts', 'src/hooks/useAuth.tsx']) L.stubSource(k, { useAuth: () => ({ claims: { firmId: 'opal' } }) });
  L.hookState.impl = {
    useLeadPanelRankings: (_m, s) => (String(s).toUpperCase() === 'PRICE' ? priceSet : undefined),
    useRankTimeSeries: () => undefined, useStarredList: () => [], useSetStarred: () => undefined, useCollectedChatter: () => undefined,
  };
  const noop = () => {};
  const { LeadPanel } = L.source(LP);
  return L.render(LeadPanel, { movement: 'TRENDING', setMovement: noop, subject: 'PRICE', setSubject: noop, starredOnly: false, setStarredOnly: noop,
    view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop, searchInput: '', setSearchInput: noop });
}

// arm 1
let f1 = [];
try { f1 = faults(render(), ROWS); } catch (e) { f1 = ['RENDER: ' + String(e.message).split('\n')[0]]; }
const a1 = f1.length === 0;

// arm 2
const f2 = [];
const b = spawnSync('git', ['-C', path.join(ROOT, 'portal'), 'show', `${PIN}:${PB}`], { encoding: 'utf8', maxBuffer: 1 << 24 });
if (b.status !== 0 || !b.stdout) f2.push(`INPUT MISSING: git show ${PIN}:${PB} rc=${b.status}`);
else {
  const s = b.stdout;
  const hasAttr = /data-price-value/.test(s);
  const rounds = /toFixed\(\s*1\s*\)/.test(s);
  if (hasAttr && rounds) f2.push(`the base PriceBars.tsx at ${PIN} already rounds to one decimal and carries data-price-value -- the check cannot tell base from fix`);
}
const a2 = f2.length === 0;

// arm 3
const r0 = ROWS[0];
const k0 = keyOf(r0);
const sgn = (x) => (x >= 0 ? '+' : '-');
const bar = (txt, attr) => `<div><div data-price-bar="${k0}"${attr === null ? '' : ` data-price-value="${attr}"`}><span>${r0.name || k0}</span><span>${txt}</span></div></div>`;
const good = bar(`${sgn(r0.return_30d_pct)}${Math.abs(r0.return_30d_pct).toFixed(1)}%`, String(r0.return_30d_pct));
const one = [r0];
const f3 = [];
if (faults(good, one).length) f3.push(`the correct markup is rejected: ${faults(good, one)[0]}`);
const M = [
  ['two decimals', bar(`${sgn(r0.return_30d_pct)}${Math.abs(r0.return_30d_pct).toFixed(2)}%`, String(r0.return_30d_pct)), 'DECIMALS'],
  ['no attribute', bar(`${sgn(r0.return_30d_pct)}${Math.abs(r0.return_30d_pct).toFixed(1)}%`, null), 'ATTR'],
  ['rounded attribute', bar(`${sgn(r0.return_30d_pct)}${Math.abs(r0.return_30d_pct).toFixed(1)}%`, r0.return_30d_pct.toFixed(1)), 'ATTR'],
  ['x100', bar(`${sgn(r0.return_30d_pct)}${Math.abs(r0.return_30d_pct * 100).toFixed(1)}%`, String(r0.return_30d_pct)), 'VALUE'],
];
const caught = [];
for (const [name, html, cls] of M) { if (faults(html, one).some((x) => x.startsWith(cls + ':'))) caught.push(name); else f3.push(`mutant "${name}" not rejected as ${cls}`); }
const a3 = f3.length === 0;

const arms = [
  ['the checkout prints one decimal, the whole value in data-price-value, no long token, |value| order kept', a1, a1 ? `${ROWS.length} bars, 0 faults` : `${f1.length} faults; first: ${f1[0]}`],
  [`NEGATIVE: the base PriceBars.tsx (${PIN}) does not round to one decimal with data-price-value`, a2, a2 ? 'base lacks the rounding and/or the attribute' : f2[0]],
  ['PLANTED: two decimals, a missing or rounded attribute and x100 are rejected; a correct bar passes', a3, a3 ? `${caught.length} of ${M.length} rejected` : f3[0]],
];
let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE PRICE BARS PRINT ONE DECIMAL: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
