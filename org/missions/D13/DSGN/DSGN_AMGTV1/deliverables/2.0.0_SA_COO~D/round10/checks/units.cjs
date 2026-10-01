/**
 * units.cjs -- DSGN_AMGTV1 round 10, AV-o-4: NEVER SCALE AN UNRESOLVED UNIT -- a figure whose served unit is UNRESOLVED shows raw,
 * with its unresolved label in words, and never carries a K / M / B / T (round-9 analysis ruling 3; AMGT_RESAPP FWD-30).
 *
 * Usage (repo root): node <this file>
 * The header figures carry `unit`; on six names the enterprise value (and 8316's net debt) is served with a unit reading
 * "UNRESOLVED-ON-<name>: sampled magnitude ... does not discriminate absolute vs millions". The page's one formatter
 * (components/StatTile.tsx formatStatValue) scales every money figure by magnitude, so 6501's 24154022.78 prints as a
 * "24.15M" the unit never claimed. Fixtures (round10/fixtures, SERVED /overlay): the planted population 6501, 9433, 8316, 8035,
 * 8766 JP and TSM US; the controls IMB LN and AZN LN (enterprise value MEASURED: "ABSOLUTE (full currency units)" / "MILLIONS").
 * The header card face is rendered through the page (SecurityOverlay IdentityHeader); every header card figure is also formatted
 * through the page's own path (HeaderCards `headerCardFigureDisplay(bundle, mnemonic)`, exported by this cell).
 * Arms:
 *   1  no scale on an unresolved unit: for every header card figure of the six whose served unit starts "UNRESOLVED" and whose
 *      value is a number, the display carries no K / M / B / T after its digits and shows the served number unscaled (its
 *      integer digits, grouped or not); the card face of each of the six shows the enterprise value that way
 *   2  the unresolved label in words: each such display says "unit not resolved" and carries no "UNRESOLVED-ON" or "field_map"
 *      text; no header face of the six shows "UNRESOLVED-ON" or "field_map"
 *   3  a MEASURED unit still shows its scale (the control): IMB's and AZN's enterprise value still read with a K / M / B / T
 *      suffix, exactly as the base formatter printed them, and every figure whose unit is not UNRESOLVED formats as before
 * Prints one line per figure, one line per arm and "NO SCALE ON AN UNRESOLVED UNIT: <k> of 3 arms"; exit 0 only at 3 of 3.
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
const DEFS = (safe(() => L.source('src/pages/SecurityAnalysis/constants.ts')) || {}).HEADER_CARD_DEFS || [];
const cardMnemonics = [...new Set(DEFS.flatMap((d) => (d.figures || []).map((f) => f.mnemonic)).filter(Boolean))];
const SCALED = /\d(?:\.\d+)?\s?[KMBT]\b/;
const face = (k) => { const m = safe(() => L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx')); return unesc(L.textOf(safe(() => L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov(k), onBack: () => {}, onRefresh: () => {} })) || '')); };
const intDigits = (v) => String(Math.trunc(Math.abs(Number(v))));

// ---- arms 1 and 2 -------------------------------------------------------------------------------------------------------------
const f1 = [];
const f2 = [];
let unresolved = 0;
if (!disp) { f1.push('HeaderCards.headerCardFigureDisplay is not exported'); f2.push('HeaderCards.headerCardFigureDisplay is not exported'); }
for (const k of PLANTED) {
  const b = ov(k);
  for (const fig of b.header_figures || []) {
    if (!cardMnemonics.includes(fig.mnemonic)) continue;
    if (!/^UNRESOLVED/.test(String(fig.unit || '')) || typeof fig.value !== 'number') continue;
    unresolved += 1;
    const d = disp ? safe(() => disp(b, fig.mnemonic)) : null;
    const s = typeof d === 'string' ? unesc(d) : JSON.stringify(d);
    console.log(`FIGURE ${k} ${fig.mnemonic}: served ${fig.value} -> "${s}"`);
    if (typeof d !== 'string' || SCALED.test(s) || !s.replace(/[,\s]/g, '').includes(intDigits(fig.value))) f1.push(`${k} ${fig.mnemonic}: "${s}"`);
    if (typeof d !== 'string' || !/unit not resolved/i.test(s) || /UNRESOLVED-ON|field_map/.test(s)) f2.push(`${k} ${fig.mnemonic}: "${s}"`);
  }
  const t = face(k);
  const m = /Enterprise value\s+(.{0,60})/.exec(t);
  if (m && SCALED.test(m[1].split(/unit not resolved/i)[0])) f1.push(`${k}: the card face reads "Enterprise value ${m[1]}"`);
  if (/UNRESOLVED-ON|field_map/.test(t)) f2.push(`${k}: a raw unit string on the header face`);
}
const a1 = f1.length === 0 && unresolved > 0;
const a1d = a1 ? `${unresolved} unresolved-unit header figure(s) over the six names show unscaled, with no K/M/B/T; each face's enterprise value too` : `${f1.length} failing of ${unresolved}; first: ${f1[0]}`;
const a2 = f2.length === 0 && unresolved > 0;
const a2d = a2 ? 'each says "unit not resolved" in words; no raw UNRESOLVED-ON / field_map string on any face' : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const ST = safe(() => L.source('src/pages/SecurityAnalysis/components/StatTile.tsx'));
let measured = 0;
for (const k of [...CONTROL, ...PLANTED]) {
  const b = ov(k);
  const own = ((b.header_figures || []).find((f) => f.mnemonic === 'CRNCY') || {}).value;
  for (const def of DEFS) {
    for (const fd of def.figures || []) {
      const fig = (b.header_figures || []).find((f) => f.mnemonic === fd.mnemonic);
      if (!fig || /^UNRESOLVED/.test(String(fig.unit || ''))) continue;
      const want = ST && ST.formatStatValue ? safe(() => ST.formatStatValue(fig.value, fd.format, fd.money ? (fig.currency ?? null) : undefined)) : null;
      const got = disp ? safe(() => disp(b, fd.mnemonic)) : null;
      measured += 1;
      if (JSON.stringify(got) !== JSON.stringify(want)) f3.push(`${k} ${fd.mnemonic}: "${got}" vs the base form "${want}"`);
    }
  }
  if (CONTROL.includes(k)) {
    const ev = disp ? safe(() => disp(b, 'CURR_ENTP_VAL')) : null;
    console.log(`CONTROL ${k} CURR_ENTP_VAL -> "${ev}"`);
    if (typeof ev !== 'string' || !SCALED.test(ev)) f3.push(`${k}: the MEASURED enterprise value "${ev}" lost its scale`);
  }
}
const a3 = f3.length === 0 && measured > 0;
const a3d = a3 ? `${measured} measured-unit card figure(s) format exactly as before; IMB and AZN enterprise value keep their scale` : `${f3.length} failing of ${measured}; first: ${f3[0]}`;

const arms = [
  ['no K/M/B/T on an unresolved unit', a1, a1d],
  ['the unresolved label in words', a2, a2d],
  ['a measured unit still shows its scale (control)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`NO SCALE ON AN UNRESOLVED UNIT: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
