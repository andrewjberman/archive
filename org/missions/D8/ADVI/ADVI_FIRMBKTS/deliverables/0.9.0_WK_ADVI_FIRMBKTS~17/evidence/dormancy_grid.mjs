// Dormancy grid: base (576e574de4) vs the new router and guard over every (firmId, tenant dir, path class) decision.
// The base copies are built HERE from git (git show 576e574de4:<path>) into <worktree>/.scratch/base, mirroring the
// repo layout so the relative imports (../_shared/firm-config.mjs, ./tier_policy.mjs) resolve exactly as at base.
// Usage: bun dormancy_grid.mjs <worktree root>
import { pathToFileURL } from "node:url";
import { resolve, dirname } from "node:path";
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, existsSync, symlinkSync } from "node:fs";

const BASE_REF = "576e574de4";
const W = resolve(process.argv[2]);   // worktree root
const B = resolve(W, ".scratch/base");
const BASE_FILES = [
  "infra/aws/lambda-edge/shared-advisor-router/index.mjs",
  "infra/aws/lambda-edge/shared-advisor-router/tier_policy.mjs",
  "infra/aws/lambda-edge/_shared/firm-config.mjs",
  "infra/aws/lambda-edge/shared-advisor-router-response/index.mjs",
];
for (const p of BASE_FILES) {
  const bytes = execFileSync("git", ["show", `${BASE_REF}:${p}`], { cwd: W, maxBuffer: 16 * 1024 * 1024 });
  const out = resolve(B, p);
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, bytes);
}
// The base guard imports @aws-sdk/client-sns; resolve it from the worktree's installed packages.
const guardNm = resolve(W, "infra/aws/lambda-edge/shared-advisor-router-response/node_modules");
const guardNmBase = resolve(B, "infra/aws/lambda-edge/shared-advisor-router-response/node_modules");
if (!existsSync(guardNmBase)) symlinkSync(guardNm, guardNmBase, "junction");

const base = await import(pathToFileURL(resolve(B, "infra/aws/lambda-edge/shared-advisor-router/index.mjs")).href);
const neu = await import(pathToFileURL(resolve(W, "infra/aws/lambda-edge/shared-advisor-router/index.mjs")).href);
const cfg = (await import(pathToFileURL(resolve(W, "infra/aws/lambda-edge/_shared/firm-config.mjs")).href)).FIRM_CONFIG;
const gBase = await import(pathToFileURL(resolve(B, "infra/aws/lambda-edge/shared-advisor-router-response/index.mjs")).href);
const gNew = await import(pathToFileURL(resolve(W, "infra/aws/lambda-edge/shared-advisor-router-response/index.mjs")).href);
const map = Object.fromEntries(Object.entries(cfg).map(([k, v]) => [k, v.bucket]));
const A = "/api/scoped/advisor-intelligence/";
const firms = [...Object.keys(cfg), "opal-capital", "unmapped-x"];
const slugs = [...new Set(Object.values(cfg).map((v) => v.bucket.replace(/^opal-data-/, "")))].concat(["none-x"]);
const dirs = [...Object.keys(cfg), "not-a-firm"];
const paths = dirs.map((d) => `platinum/advi/${d}/mix_summary.json`).concat(["platinum/firm/h.json", "views/v.json"]);
const quiet = async (fn) => { const l = console.log, w = console.warn, e = console.error; console.log = () => {}; console.warn = () => {}; console.error = () => {};
  try { return await fn(); } finally { console.log = l; console.warn = w; console.error = e; } };
const ev = (firmId, uri, qs) => { const h = {}; if (firmId) h["x-firm-id"] = [{ key: "X-Firm-Id", value: firmId }];
  h["x-user-tier"] = [{ key: "X-User-Tier", value: "internal" }];
  return { Records: [{ cf: { request: { method: "GET", uri: A + uri, querystring: qs, headers: h,
    origin: { s3: { domainName: "opal-data-bd.s3.us-east-1.amazonaws.com", region: "us-east-1", authMethod: "origin-access-identity", customHeaders: {} } } } } }] }; };
const gev = (firmId, uri, qs, served) => ({ Records: [{ cf: { request: { uri, querystring: qs,
  headers: firmId ? { "x-firm-id": [{ key: "X-Firm-Id", value: firmId }] } : {},
  origin: { s3: { domainName: `${served}.s3.us-east-1.amazonaws.com`, region: "us-east-1" } } },
  response: { status: "200", statusDescription: "OK", headers: { "x-amz-cf-id": [{ key: "X-Amz-Cf-Id", value: "t" }] }, body: "{}" } } }] });
const cases = [];
for (const f of firms) for (const p of paths) for (const qs of (f === "opal-capital" ? slugs.map((s) => "firm=" + s) : [""])) cases.push({ f, p, qs });
let same = 0, diffs = [];
for (const c of cases) {
  const a = await quiet(() => base.handleWithMap(ev(c.f, c.p, c.qs), map));
  const b = await quiet(() => neu.handleWithMap(ev(c.f, c.p, c.qs), map));
  const ka = JSON.stringify({ s: a.status, u: a.uri, d: a.origin?.s3?.domainName, b: a.body });
  const kb = JSON.stringify({ s: b.status, u: b.uri, d: b.origin?.s3?.domainName, b: b.body });
  if (ka === kb) same++; else diffs.push({ f: c.f, qs: c.qs, p: c.p, base: ka, neu: kb });
}
console.log(`ROUTER GRID: identical ${same} of ${cases.length} (firmId x tenant-dir x path x ?firm); differing ${diffs.length}`);
for (const d of diffs) console.log("  DIFF " + JSON.stringify({ f: d.f, qs: d.qs, p: d.p }) + "\n     base " + d.base + "\n     new  " + d.neu);
// guard: served from the bucket the base router would route to vs CANONICAL, for platinum/advi paths
let gsame = 0, gdiff = [];
const gcases = [];
for (const f of firms) for (const p of dirs.map((d) => `/platinum/advi/${d}/mix_summary.json`)) for (const qs of (f === "opal-capital" ? slugs.map((s) => "firm=" + s) : [""])) for (const served of ["opal-data-portal-v2", ...Object.values(map)]) gcases.push({ f, p, qs, served });
for (const c of gcases) {
  const a = await quiet(() => gBase.handler(gev(c.f, c.p, c.qs, c.served)));
  const b = await quiet(() => gNew.handler(gev(c.f, c.p, c.qs, c.served)));
  const sa = a.status, sb = b.status;
  if (sa === sb) gsame++; else gdiff.push({ ...c, base: sa, neu: sb });
}
console.log(`GUARD GRID: identical ${gsame} of ${gcases.length} (firmId x tenant-dir x ?firm x served bucket); differing ${gdiff.length}`);
for (const d of gdiff) console.log("  GDIFF " + JSON.stringify(d));
console.log(`DORMANCY: router differing ${diffs.length}, guard differing ${gdiff.length}`);
