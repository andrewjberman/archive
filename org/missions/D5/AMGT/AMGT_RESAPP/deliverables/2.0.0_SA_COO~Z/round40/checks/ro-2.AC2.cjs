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
// AMGT_RESAPP round 40, AMGT-ro-2 AC2 -- THE GUARD: a map entry whose relation is RECIPROCAL but which states no
// transform/units (every peers/v1 pool object written before rn-2 is shaped this way) renders ABSENT, never the raw
// yield under a P/E label. Strips the two fields from the fixture's ey/ey_ntm entries and reads the P/E cells.
const doc = JSON.parse(fs.readFileSync(path.join(base, fixturePath), 'utf8'));
const peers = JSON.parse(JSON.stringify(doc[routeKey] || doc.peers || doc));
let stripped = 0;
for (const e of (peers.csc_columns && peers.csc_columns.present) || []) {
  if (e.code === 'ey' || e.code === 'ey_ntm') { if ('transform' in e || 'units' in e) stripped++; delete e.transform; delete e.units; }
}
const table = buildCscTable(peers);
const idx = table.columns.map((c, i) => ({ c, i })).filter(({ c }) => c.code === 'ey' || c.code === 'ey_ntm');
let nulls = 0, numbers = 0; const samples = [];
for (const row of table.rows.filter((r) => !r.isSubject)) for (const { c, i } of idx) {
  const v = row.values[i]; if (v === null || v === undefined) nulls++; else { numbers++; if (samples.length < 3) samples.push(`${row.ticker} ${c.column}=${v}`); }
}
console.log(`entries stripped: ${stripped}; P/E cells with no stated unit: ${nulls} absent, ${numbers} numeric; samples: ${samples.join(' | ') || 'none'}`);
process.exit(idx.length === 2 && numbers === 0 && nulls > 0 ? 0 : 1);
