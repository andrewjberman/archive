/**
 * bound.cjs -- DSGN_AMGTV1 round-2 BOUND check: the page's own harnesses that load a cell's
 * surface and read green at the base stay green. Usage (from the repository root):
 *   node <this file> <LABEL> <harness file> [<harness file> ...]
 * Prints one line per harness and "<LABEL> BOUND: k of n harnesses green"; exit 0 only when k == n.
 * A harness is green when it exits 0 AND prints CHECKS-OK N of N, an "OK:" line, or a PASS result.
 */
const L = require('./_load.cjs');
const [label, ...files] = process.argv.slice(2);
if (!label || files.length === 0) {
  console.log('usage: bound.cjs <LABEL> <harness> [...]');
  process.exit(3);
}
// "<file>:<min>" also requires CHECKS-OK N of N with N >= min -- a re-scoped harness may not
// shrink below the number of checks it ran at the base.
let green = 0;
for (const spec of files) {
  const [f, minRaw] = spec.split(':');
  const min = minRaw ? Number(minRaw) : 0;
  const r = L.runHarness(f);
  const n = Number((/CHECKS-OK (\d+) of/.exec(r.tally) || [])[1] || 0);
  const ok = r.green && (min === 0 || n >= min);
  console.log(`HARNESS ${ok ? 'GREEN' : 'RED'} ${f} :: ${r.tally}${min ? ` (floor ${min})` : ''}`);
  if (ok) green += 1;
}
console.log(`${label} BOUND: ${green} of ${files.length} harnesses green`);
process.exit(green === files.length ? 0 : 1);
