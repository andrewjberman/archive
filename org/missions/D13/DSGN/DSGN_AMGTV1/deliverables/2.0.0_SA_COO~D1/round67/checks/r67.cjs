/**
 * r67.cjs -- DSGN_AMGTV1 round 67 issuer CHECK (2.0.0_SA_COO~D1): THE PEER TABLE READS CLEAN (FWD-8), AND ONE MEASURE READS ONE WAY
 * ACROSS TILE AND TABLE (FWD-27).
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round67/checks/r67.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round66.md @f16252a512; round-66 walk tmp/ui-walk/20261009T142010Z shot 131): on ASML's peers
 *   - the ticker cells read "BMMV2K" (a served id) and "This listing has only an exchange number; ..." (the served ticker_reason);
 *   - the peer prices print with no currency, because the page reads `currency` while the payload serves `price_currency`;
 *   - "Mkt Cap (USD mm)" / "EV (USD mm)" head columns whose subject cells are EUR;
 *   - the subject price reads "EUR 1626.20" in its tile (StatTile formatStatValue 'price': toFixed(2), no separator) and "EUR 1,626" in
 *     the table (PeersTab formatValue);
 *   - the subject cap reads "EUR 631B" in its tile (CUR_MKT_CAP) and "EUR 541,932" mm in the table (market_cap_musd).
 * Arms (exit 0 only on all six):
 *   1 ONE PRICE FORMAT: StatTile.tsx formatStatValue(v, 'price', code) prints two decimals WITH a thousands separator ("EUR 1,626.20",
 *     "USD 99.81", "1,495,000.00 currency not stated" with no code) -- loaded through the real module.
 *   2 READABLE TICKERS: cscTable.ts exports memberTicker(member). A member whose identity resolution is MEASURED with a security_key prints
 *     the key in house form ("700_HK_Equity" -> "700 HK"); any other member prints its company name (display_name, else name) -- never a
 *     served id or a sentence -- loaded through the real module.
 *   3 HONEST HEADINGS: cscTable.ts exports columnHeading(displayLabel, codes). It strips the served parenthetical ("Mkt Cap (USD mm)" ->
 *     "Mkt Cap") and appends "(<code>)" only when every code (subject and members) is the same served code, else "(local)".
 *   4 PRICE CURRENCY READ: the peer price's currency is read from the served `price_currency` (cscTable.ts or PeersTab.tsx).
 *   5 ONE FORMAT IN THE TABLE: PeersTab.tsx formats the price and money cells through formatStatValue ('price', 'currency-millions'),
 *     and the subject's Mkt Cap reads the header's CUR_MKT_CAP (the same served figure as the tile).
 *   6 PLANTED.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

const G = {
  price: (fmt) => {
    if (typeof fmt !== 'function') return ['StatTile.tsx exports no formatStatValue'];
    const f = [];
    const cases = [[[1626.2, 'price', 'EUR'], 'EUR 1,626.20'], [[99.81, 'price', 'USD'], 'USD 99.81'], [[1495000, 'price', null], '1,495,000.00 currency not stated']];
    for (const [args, want] of cases) {
      let got; try { got = fmt(...args); } catch (e) { got = 'THREW ' + e.message; }
      if (got !== want) f.push(`formatStatValue(${JSON.stringify(args)}) = ${JSON.stringify(got)} (wanted ${JSON.stringify(want)})`);
    }
    return f;
  },
  ticker: (fn) => {
    if (typeof fn !== 'function') return ['cscTable.ts exports no memberTicker'];
    const f = [];
    const cases = [
      [{ ticker: 'BMMV2K', name: 'Tencent Holdings Ltd', identity: { resolution: 'UNRESOLVED' } }, 'Tencent Holdings Ltd'],
      [{ ticker: '000660', name: 'SK hynix Inc.', ticker_reason: 'This listing has only an exchange number; we have no company match for it yet.', identity: { resolution: 'UNRESOLVED' } }, 'SK hynix Inc.'],
      [{ ticker: '0700', name: 'Tencent Holdings Ltd', security_key: '700_HK_Equity', identity: { resolution: 'MEASURED', security_key: '700_HK_Equity' } }, '700 HK'],
      [{ ticker: 'INTC', name: 'Intel Corporation', display_name: 'Intel Corporation', identity: { resolution: 'MEASURED', security_key: 'INTC_US_Equity' } }, 'INTC US'],
      [{ ticker: 'XYZ', name: 'Plain Co', display_name: 'Plain Company', identity: null }, 'Plain Company'],
    ];
    for (const [m, want] of cases) {
      let got; try { got = fn(m); } catch (e) { got = 'THREW ' + e.message; }
      if (got !== want) f.push(`memberTicker(${m.ticker}) = ${JSON.stringify(got)} (wanted ${JSON.stringify(want)})`);
    }
    return f;
  },
  heading: (fn) => {
    if (typeof fn !== 'function') return ['cscTable.ts exports no columnHeading'];
    const f = [];
    const cases = [
      [['Mkt Cap (USD mm)', ['USD', 'USD', 'USD']], 'Mkt Cap (USD)'],
      [['Mkt Cap (USD mm)', ['EUR', 'USD', 'USD']], 'Mkt Cap (local)'],
      [['EV (USD mm)', ['USD', null]], 'EV (local)'],
      [['Price (last)', ['EUR', 'USD']], 'Price (local)'],
      [['Price (last)', ['USD', 'USD']], 'Price (USD)'],
    ];
    for (const [args, want] of cases) {
      let got; try { got = fn(...args); } catch (e) { got = 'THREW ' + e.message; }
      if (got !== want) f.push(`columnHeading(${JSON.stringify(args)}) = ${JSON.stringify(got)} (wanted ${JSON.stringify(want)})`);
    }
    return f;
  },
  priceCurrency: (csc, peers) => (/price_currency/.test(`${csc || ''}\n${peers || ''}`) ? [] : ['the served price_currency is never read']),
  oneFormat: (peers) => {
    if (peers === null) return ['PeersTab.tsx missing'];
    const f = [];
    if (!/formatStatValue\s*\(/.test(peers)) f.push('PeersTab does not format cells through formatStatValue');
    if (!/'currency-millions'/.test(peers)) f.push("PeersTab does not format the money (mm) columns as 'currency-millions'");
    if (!/mkt_val_sec\s*:\s*'CUR_MKT_CAP'/.test(peers)) f.push("the subject's Mkt Cap does not read the header's CUR_MKT_CAP");
    return f;
  },
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
let L = null; let lerr = null;
try { L = require(path.join(DD, 'round15', 'checks', '_load.cjs')); } catch (e) { lerr = 'LOADER: ' + String(e.message).split('\n')[0]; }
const mod = (rel) => { try { return L.source(`src/pages/SecurityAnalysis/${rel}`); } catch (e) { return { __err: 'LOADER: ' + String(e.message).split('\n')[0] }; } };
const st = lerr ? { __err: lerr } : mod('components/StatTile.tsx');
const cs = lerr ? { __err: lerr } : mod('cscTable.ts');
push('ONE PRICE FORMAT', st.__err ? [st.__err] : G.price(st.formatStatValue));
push('READABLE TICKERS', cs.__err ? [cs.__err] : G.ticker(cs.memberTicker));
push('HONEST HEADINGS', cs.__err ? [cs.__err] : G.heading(cs.columnHeading));
push('PRICE CURRENCY READ', G.priceCurrency(read('cscTable.ts'), read('tabs/PeersTab.tsx')));
push('ONE FORMAT IN THE TABLE', G.oneFormat(read('tabs/PeersTab.tsx')));
{
  const p = [];
  const okPrice = (v, fmt, c) => { const s = v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); return c ? `${c} ${s}` : `${s} currency not stated`; };
  if (G.price(okPrice).length) p.push('the clean price formatter refused');
  if (!G.price((v, fmt, c) => `${c} ${v.toFixed(2)}`).length) p.push('the round-66 price formatter admitted');
  const okTicker = (m) => { const id = m.identity || {}; const key = m.security_key || id.security_key; return id.resolution === 'MEASURED' && key ? key.replace(/_Equity$/, '').replace(/_/g, ' ') : (m.display_name || m.name); };
  if (G.ticker(okTicker).length) p.push('the clean ticker rule refused');
  if (!G.ticker((m) => (/^\d+$/.test(m.ticker) ? m.ticker_reason : m.ticker)).length) p.push('the round-66 ticker rule admitted');
  const okHead = (label, codes) => { const m = String(label).replace(/\s*\([^)]*\)\s*$/, ''); const set = new Set(codes); return set.size === 1 && !set.has(null) ? `${m} (${codes[0]})` : `${m} (local)`; };
  if (G.heading(okHead).length) p.push('the clean heading refused');
  if (!G.heading((label) => label).length) p.push('the served heading admitted');
  if (!G.oneFormat("const SUBJECT_HEADER_MNEMONIC = { price: 'PX_LAST' }\nformatValue(v)").length) p.push('the round-66 table admitted');
  if (G.oneFormat("formatStatValue(v, 'currency-millions', c)\nconst SUBJECT_HEADER_MNEMONIC = { mkt_val_sec: 'CUR_MKT_CAP' }").length) p.push('the clean table refused');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 67 PEERS AND FORMATS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
