/**
 * unitlead.cjs -- DSGN_AMGTV1 round 11, AV-n-1: AN UNRESOLVED FIGURE LEADS WITH ITS QUALIFIER, AND ITS DIGITS ARE LABELLED A RAW
 * FIGURE (round-10 analysis ruling 1; AMGT_RESAPP FWD-30, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Round 10 showed TSM's enterprise value as "TWD 71,993,494.73 (unit not resolved)", which a reader who stops early takes for
 * about TWD 72 million -- when the served number is very likely in millions. Ruled: the qualifier LEADS and the digits are
 * labelled raw: "unit not resolved -- raw figure 71,993,494.73 (TWD)". A reader who stops early reads "unit not resolved", never
 * an amount. Fixtures (round11/fixtures, SERVED /overlay): the planted six (6501, 9433, 8316, 8035, 8766 JP, TSM US); the
 * controls IMB LN and AZN LN (measured units).
 * Arms:
 *   1  the qualifier leads: every header card figure of the six whose unit starts "UNRESOLVED" and whose value is a number has a
 *      display (HeaderCards `headerCardFigureDisplay`) that STARTS "unit not resolved -- raw figure ", followed by the served
 *      number unscaled and grouped (its integer digits), with the currency code, when served, in brackets AFTER the digits
 *      ("(TWD)"); no K / M / B / T; no "UNRESOLVED-ON" / "field_map"
 *   2  the card face reads the same way: each of the six headers (SecurityOverlay IdentityHeader) shows "Enterprise value" (or the
 *      figure's own label) followed by "unit not resolved" BEFORE any digit of that figure
 *   3  a measured unit is unchanged (the control): every figure whose unit is not UNRESOLVED, over the eight names, formats exactly
 *      as the base formatter did (StatTile `formatStatValue(value, format, currency)`); IMB's and AZN's enterprise value keep their
 *      K / M / B / T
 * Prints one line per unresolved figure, one line per arm and "UNRESOLVED FIGURE LEADS WITH ITS QUALIFIER: <k> of 3 arms"; exit 0
 * only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const safe = (f) => { try { return f(); } catch (e) { return { error: String(e.message).split('\n')[0] }; } };
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const PLANTED = ['6501_JP_Equity', '9433_JP_Equity', '8316_JP_Equity', '8035_JP_Equity', '8766_JP_Equity', 'TSM_US_Equity'];
const CONTROL = ['IMB_LN_Equity', 'AZN_LN_Equity'];
const ov = (k) => S.unwrap(L.fixture(`overlay.${k}.json`));
const HC = safe(() => L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'));
const disp = HC && HC.headerCardFigureDisplay;
const ST = safe(() => L.source('src/pages/SecurityAnalysis/components/StatTile.tsx'));
const DEFS = (safe(() => L.source('src/pages/SecurityAnalysis/constants.ts')) || {}).HEADER_CARD_DEFS || [];
const defOf = (m) => { for (const d of DEFS) for (const f of d.figures || []) if (f.mnemonic === m) return f; return null; };
const SCALED = /\d(?:\.\d+)?\s?[KMBT]\b/;
const face = (k) => { const m = safe(() => L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx')); return unesc(L.textOf(safe(() => L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov(k), onBack: () => {}, onRefresh: () => {} })) || '')); };
const intDigits = (v) => String(Math.trunc(Math.abs(Number(v))));

const f1 = [];
const f2 = [];
let unresolved = 0;
if (!disp) f1.push('HeaderCards.headerCardFigureDisplay is not exported');
for (const k of PLANTED) {
  const b = ov(k);
  const t = face(k);
  for (const fig of b.header_figures || []) {
    const def = defOf(fig.mnemonic);
    if (!def || !/^UNRESOLVED/.test(String(fig.unit || '')) || typeof fig.value !== 'number') continue;
    unresolved += 1;
    const d = disp ? safe(() => disp(b, fig.mnemonic)) : null;
    const s = typeof d === 'string' ? unesc(d) : JSON.stringify(d);
    console.log(`FIGURE ${k} ${fig.mnemonic}: served ${fig.value} (${fig.currency ?? 'no currency'}) -> "${s}"`);
    const cur = def.money && fig.currency ? fig.currency : null;
    const ok = typeof d === 'string' && s.startsWith('unit not resolved -- raw figure ') && !SCALED.test(s)
      && s.replace(/[,\s]/g, '').includes(intDigits(fig.value)) && !/UNRESOLVED-ON|field_map/.test(s)
      && (!cur || s.trimEnd().endsWith(`(${cur})`));
    if (!ok) f1.push(`${k} ${fig.mnemonic}: "${s}"`);
    // arm 2: on the face, the qualifier comes before the figure's digits
    const at = t.indexOf(def.label);
    if (at >= 0 && def.key === ((DEFS.find((c) => (c.figures || []).includes(def)) || {}).figures || [])[0]?.key) {
      const after = t.slice(at + def.label.length, at + def.label.length + 90);
      const q = after.search(/unit not resolved/i);
      const dg = after.search(/\d/);
      if (q < 0 || (dg >= 0 && dg < q)) f2.push(`${k}: the face reads "${def.label}${after.slice(0, 60)}"`);
    }
  }
  if (/UNRESOLVED-ON|field_map/.test(t)) f2.push(`${k}: a raw unit string on the header face`);
}
const a1 = f1.length === 0 && unresolved > 0;
const a1d = a1 ? `${unresolved} unresolved figure(s) over the six read "unit not resolved -- raw figure <digits> (<currency>)"` : `${f1.length} failing of ${unresolved}; first: ${f1[0]}`;
const a2 = f2.length === 0 && unresolved > 0;
const a2d = a2 ? 'on every header face of the six, "unit not resolved" comes before the figure\'s digits' : `${f2.length} failing; first: ${f2[0]}`;

const f3 = [];
let measured = 0;
for (const k of [...CONTROL, ...PLANTED]) {
  const b = ov(k);
  for (const d of DEFS) for (const fd of d.figures || []) {
    const fig = (b.header_figures || []).find((f) => f.mnemonic === fd.mnemonic);
    if (!fig || /^UNRESOLVED/.test(String(fig.unit || ''))) continue;
    const want = ST && ST.formatStatValue ? safe(() => ST.formatStatValue(fig.value, fd.format, fd.money ? (fig.currency ?? null) : undefined)) : null;
    const got = disp ? safe(() => disp(b, fd.mnemonic)) : null;
    measured += 1;
    if (JSON.stringify(got) !== JSON.stringify(want)) f3.push(`${k} ${fd.mnemonic}: "${got}" vs "${want}"`);
  }
  if (CONTROL.includes(k)) {
    const ev = disp ? safe(() => disp(b, 'CURR_ENTP_VAL')) : null;
    if (typeof ev !== 'string' || !SCALED.test(ev)) f3.push(`${k}: the MEASURED enterprise value "${ev}" lost its scale`);
  }
}
const a3 = f3.length === 0 && measured > 0;
const a3d = a3 ? `${measured} measured-unit card figure(s) format exactly as before; IMB and AZN enterprise value keep their scale` : `${f3.length} failing of ${measured}; first: ${f3[0]}`;

const arms = [
  ['the qualifier leads; the digits are labelled raw', a1, a1d],
  ['the card face puts the qualifier before the digits', a2, a2d],
  ['a measured unit is unchanged (control)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`UNRESOLVED FIGURE LEADS WITH ITS QUALIFIER: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
