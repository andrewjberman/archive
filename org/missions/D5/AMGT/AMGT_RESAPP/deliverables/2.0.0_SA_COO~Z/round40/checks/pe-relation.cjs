// AMGT_RESAPP round 39, AMGT-rn-2 AC2 -- THE MAGNITUDE CRITERION (round-38 analysis s.4): every P/E value the
// portal's own table builder produces for the BA fixture's members lies in the plausibility band [0.5, 200], or is
// null (an absent value renders as absent, never as a number). Loads the REAL cscTable.ts through the harness's own
// transpile-and-require path, so what is graded is the builder the page runs.
// usage (from the portal root): node <this> [--fixture <uiContractFixtures-shaped JSON>] [--route <peers route key>] [--lo 0.5] [--hi 200]
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { createRequire } = require('node:module');
const base = path.resolve(process.cwd());
const req = createRequire(path.join(base, 'package.json'));
const ts = req('typescript');
const args = process.argv.slice(2);
const arg = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const fixturePath = arg('--fixture', 'src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json');
const routeKey = arg('--route', '/api/scoped/amgt/security/BA_US_Equity/peers');
const lo = Number(arg('--lo', '0.5')); const hi = Number(arg('--hi', '200'));
const cache = new Map();
function load(rel) {
  if (cache.has(rel)) return cache.get(rel);
  const file = path.join(base, rel);
  const js = ts.transpileModule(fs.readFileSync(file, 'utf8'), { compilerOptions: {
    module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, jsx: ts.JsxEmit.ReactJSX } }).outputText;
  const mod = { exports: {} };
  const localRequire = (spec) => {
    if (spec.startsWith('.')) {
      const dir = path.dirname(rel); let p = path.join(dir, spec).replace(/\\/g, '/');
      for (const cand of [p + '.ts', p + '.tsx', p + '/index.ts', p]) if (fs.existsSync(path.join(base, cand)) && fs.statSync(path.join(base, cand)).isFile()) return load(cand);
      throw new Error('unresolved relative import ' + spec + ' from ' + rel);
    }
    if (spec.startsWith('@/')) return load('src/' + spec.slice(2) + (fs.existsSync(path.join(base, 'src/' + spec.slice(2) + '.ts')) ? '.ts' : '.tsx'));
    return req(spec);
  };
  vm.runInThisContext('(function (require, module, exports) {' + js + '\n})')(localRequire, mod, mod.exports);
  cache.set(rel, mod.exports); return mod.exports;
}
const { buildCscTable } = load('src/pages/SecurityAnalysis/cscTable.ts');
// AMGT_RESAPP round 40 -- THE RELATION CRITERION: every member's rendered P/E equals 100 / (its percent earnings yield)
// within 1%. A magnitude band cannot tell a raw percent yield (2-5) from a P/E; the product can. Reads the member's
// own yield from the same document the table is built from.
const doc = JSON.parse(fs.readFileSync(path.join(base, fixturePath), 'utf8'));
const peers = doc[routeKey] || doc.peers || doc;
const table = buildCscTable(peers);
const cols = table.columns.map((c, i) => ({ c, i })).filter(({ c }) => c.code === 'ey' || c.code === 'ey_ntm');
const members = peers.members || [];
let ok = 0, bad = 0, nul = 0; const samples = [];
table.rows.filter((r) => !r.isSubject).forEach((row, m) => {
  const src = members[m] || {};
  for (const { c, i } of cols) {
    const y = c.code === 'ey' ? src.ey : (src.factors || {}).ey_ntm;
    const v = row.values[i];
    if (v === null || v === undefined) { nul++; if (samples.length < 4) samples.push(`${row.ticker} ${c.column}=null (yield ${y})`); continue; }
    const prod = v * y;
    if (Math.abs(prod - 100) <= 1) ok++; else { bad++; if (samples.length < 4) samples.push(`${row.ticker} ${c.column}=${v} x yield ${y} = ${prod.toFixed(3)}`); }
  }
});
console.log(`P/E x percent yield == 100 (+/-1): ${ok} of ${ok + bad + nul}; off-relation ${bad}; null ${nul}; samples: ${samples.join(' | ') || 'none'}`);
process.exit(cols.length === 2 && ok > 0 && bad === 0 && nul === 0 ? 0 : 1);
