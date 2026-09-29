/**
 * money.cjs -- DSGN_AMGTV1 round 3: NO PAGE-SIDE FORMATTER PRINTS A "$" IT WAS NOT SERVED (FWD-4).
 *
 * Usage (repo root): node <this file>
 * The only page-side builder of a "$" left after round 2 is formatStatValue's legacy path in components/StatTile.tsx: a call
 * with NO currency argument returns "$<amount>". Served prose ("$2,078 million" in a drafted reason) is the served text and
 * is never rewritten; this check reads the formatter only.
 * Arms, all must hold:
 *   A  formatStatValue(382.86, 'price'), formatStatValue(110235907718.46, 'currency-abs') and
 *      formatStatValue(116977.9, 'currency-millions') with NO currency argument carry no "$" and read "currency not stated".
 *   B  with currency 'EUR' they read "EUR <amount>" (the served code, unchanged from round 2).
 *   C  non-money formats are unchanged: formatStatValue(0.72, 'ratio') has no currency word and no "$".
 * Prints "NO UNSERVED DOLLAR: k of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const { formatStatValue } = L.source('src/pages/SecurityAnalysis/components/StatTile.tsx');
const results = [];
const cases = [[382.86, 'price'], [110235907718.46, 'currency-abs'], [116977.9, 'currency-millions']];
{
  const out = cases.map(([v, f]) => String(formatStatValue(v, f)));
  const ok = out.every((s) => !s.includes('$') && /currency not stated/i.test(s));
  results.push(['A no currency argument -> no "$", "currency not stated"', ok, JSON.stringify(out)]);
}
{
  const out = cases.map(([v, f]) => String(formatStatValue(v, f, 'EUR')));
  const ok = out.every((s) => /^EUR\s/.test(s) && !s.includes('$'));
  results.push(['B served code prints first', ok, JSON.stringify(out)]);
}
{
  const s = String(formatStatValue(0.72, 'ratio'));
  const ok = !s.includes('$') && !/currency/i.test(s);
  results.push(['C non-money unchanged', ok, JSON.stringify(s)]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`NO UNSERVED DOLLAR: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
