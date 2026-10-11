// ADVI_FIRMBKTS round 2 check for cell FB-e-6 (F6: the router's canonical platinum key path), issuer 2.0.0_SA_COO~B1.
//
//   bun <this file> diff [--router DIR]   the difference control: for the registry's CURRENT firm map, the new router's
//                                         handleWithMap() equals the pre-change router (git blob BASE_BLOB) on every
//                                         event of the corpus, byte for byte.
//   bun <this file> seam [--router DIR]   the seam to the table: with the map overridden so 49financial and mockadv
//                                         resolve to opal-data-49financial AND that bucket named in the canonical list
//                                         (the router ships it EMPTY), every router-reachable served class's
//                                         rewritten key equals the key the round-1 table (mapping.json) gives it;
//                                         unplaced classes are refused; the other firms, the twin class and the
//                                         satellites branch are unchanged.
//
// --router DIR is the directory holding the router's index.mjs (default <cwd>/infra/aws/lambda-edge/shared-advisor-router);
// its `../_shared/firm-config.mjs` is the registry's view. Run from the repository root. Never edit this file.
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, unlinkSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const BASE_COMMIT = "fda1c4f0cc";   // the router as it stood at the round-2 cut
const ROUTER_REL = "infra/aws/lambda-edge/shared-advisor-router";
const MAPPING = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/mapping.json";
const DOMAIN = (b) => `${b}.s3.us-east-1.amazonaws.com`;

const argv = process.argv.slice(2);
const arm = argv[0];
const ri = argv.indexOf("--router");
const root = process.cwd();
const routerDir = resolve(ri >= 0 ? argv[ri + 1] : join(root, ROUTER_REL));

function quiet(fn) {
  const l = console.log, w = console.warn;
  console.log = () => {}; console.warn = () => {};
  return fn().finally(() => { console.log = l; console.warn = w; });
}

function event({ firmId, uri, qs = "", method = "GET", tier = "internal" }) {
  const headers = {};
  if (firmId !== undefined) headers["x-firm-id"] = [{ key: "X-Firm-Id", value: firmId }];
  if (tier) headers["x-user-tier"] = [{ key: "X-User-Tier", value: tier }];
  return { Records: [{ cf: { request: {
    method, uri, querystring: qs, headers,
    origin: { s3: { domainName: DOMAIN("opal-data-bd"), region: "us-east-1", authMethod: "origin-access-identity", customHeaders: {} } },
  } } }] };
}
const clone = (o) => JSON.parse(JSON.stringify(o));
const A = "/api/scoped/advisor-intelligence/";
const SUFFIXES = [
  "artifacts/implementor_leaderboard.json", "artifacts/snapshots/aua_by_region.json",
  "entities/accounts/z0823828141/aua_timeseries.json", "entities/advisors/wills_crenshaw/timeseries.json",
  "entities/clients/z0893800/aua_timeseries.json", "advisors/dean_herndon/mix_timeseries.json",
  "client_timeseries/z0880342.json", "views/firm_composition.json", "timeseries/synthetic_positions_index.json",
  "platinum/firm/advisor_nna_canonical.json", "platinum/accounts/z0823699811/summary.json",
  "platinum/clients/z0893649/mix_timeseries.json", "platinum/advisors/zach_hawkins/positions.json",
  "platinum/advisors/zach_hawkins/summary.json", "platinum/clients/z0893649/summary.json",
  "platinum/49financial/ownership_map.json", "platinum/advi/49financial/mix_summary.json",
  "platinum/advi/inflection/mix_summary.json", "firm_composition.json", "summary/header_metrics.json",
];
const SAT = ["registry.json", "holdings.json", "characteristics.json", "nope.json"].map((s) => "/api/scoped/satellites/" + s);

function corpus() {
  const evs = [];
  for (const firmId of ["49financial", "inflection", "cottonwood", "mockadv", "demo", "acme"]) {
    for (const s of SUFFIXES) evs.push({ firmId, uri: A + s });
    for (const u of SAT) evs.push({ firmId, uri: u });
    evs.push({ firmId, uri: A + "views/firm_composition.json", method: "OPTIONS" });
  }
  for (const f of ["49financial", "inf", "cot", "bd"]) {
    for (const s of SUFFIXES.slice(0, 10)) evs.push({ firmId: "opal-capital", uri: A + s, qs: "firm=" + f });
  }
  evs.push({ firmId: "opal-capital", uri: A + SUFFIXES[0] });
  evs.push({ firmId: undefined, uri: A + SUFFIXES[0] });
  evs.push({ firmId: "49financial", uri: A + SUFFIXES[2], tier: "" });
  return evs;
}

async function load(dir, label) {
  const mod = await import(pathToFileURL(join(dir, "index.mjs")).href);
  const cfg = await import(pathToFileURL(join(dir, "..", "_shared", "firm-config.mjs")).href);
  return { mod, cfg, label };
}

async function baseRouter(dirOfNew) {
  const blob = execFileSync("git", ["show", `${BASE_COMMIT}:${ROUTER_REL}/index.mjs`], { cwd: root, maxBuffer: 1 << 26 }).toString("utf8");
  const tmp = join(dirOfNew, ".r2_base_index.mjs");
  writeFileSync(tmp, blob);
  try {
    const mod = await import(pathToFileURL(tmp).href + "?base=" + Date.now());
    return mod;
  } finally {
    try { unlinkSync(tmp); } catch (_e) { /* the module is already loaded */ }
  }
}

async function run(handler, ev) {
  try { return JSON.stringify(await handler(clone(ev))); } catch (e) { return "THROW " + String(e).slice(0, 80); }
}

async function diff() {
  const { mod, cfg } = await load(routerDir, "new");
  if (typeof mod.handleWithMap !== "function") {
    console.log("F6 DIFF: NOT RUN -- index.mjs does not export handleWithMap(event, firmBucketMap)");
    return 1;
  }
  const base = await baseRouter(routerDir);
  const evs = corpus();
  let same = 0, viaHandler = 0;
  const bad = [];
  await quiet(async () => {
    for (const d of evs) {
      const ev = event(d);
      const want = await run(base.handler, ev);
      const got = await run((e) => mod.handleWithMap(e, cfg.FIRM_BUCKET_MAP), ev);
      const got2 = await run(mod.handler, ev);
      if (want.startsWith("THROW") || got.startsWith("THROW")) bad.push(d);
      else if (want === got) same++; else bad.push(d);
      if (want === got2) viaHandler++;
    }
  });
  console.log(`F6 DIFF: identical ${same} of ${evs.length} events through handleWithMap; ${viaHandler} of ${evs.length} through handler`);
  for (const b of bad.slice(0, 3)) console.log("  DIFFERS " + JSON.stringify(b));
  return same === evs.length && viaHandler === evs.length ? 0 : 1;
}

async function seam() {
  const { mod, cfg } = await load(routerDir, "new");
  if (typeof mod.handleWithMap !== "function") {
    console.log("F6 SEAM: NOT RUN -- index.mjs does not export handleWithMap(event, firmBucketMap)");
    return 1;
  }
  const rows = JSON.parse(readFileSync(join(root, MAPPING), "utf8")).rows
    .filter((r) => r.bucket === "opal-data-bd" && r.disposition === "MOVE" && r.dest && r.dest.tier === "platinum");
  const census = JSON.parse(readFileSync(join(root, "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/census.json"), "utf8"));
  const sample = Object.fromEntries(census.buckets["opal-data-bd"].classes.map((c) => [c.prefix, c.sample_key]));
  const ROUTE = {   // the served class -> the advisor-intelligence suffix that reaches it today
    "gold/artifacts/": "artifacts/", "gold/entities/accounts/": "entities/accounts/",
    "gold/entities/advisors/": "entities/advisors/", "gold/entities/clients/": "entities/clients/",
    "gold/views/": "views/", "platinum/accounts/": "platinum/accounts/", "platinum/advisors/": "platinum/advisors/",
    "platinum/clients/": "platinum/clients/", "platinum/firm/": "platinum/firm/", "platinum/49financial/": "platinum/49financial/",
  };
  const map = { ...cfg.FIRM_BUCKET_MAP, "49financial": "opal-data-49financial", mockadv: "opal-data-49financial" };
  const CANON = ["opal-data-49financial"];
  let ok = 0, n = 0;
  const bad = [];
  const unreachable = [];
  await quiet(async () => {
    for (const r of rows) {
      const route = ROUTE[r.prefix];
      if (route === undefined) { unreachable.push(r.prefix); continue; }
      const tail = sample[r.prefix].slice(r.prefix.length);
      const want = "/" + r.dest_pattern.replace("{firm}", "49financial").replace("{tail}", tail);
      for (const firmId of ["49financial", "mockadv"]) {
        n++;
        const out = await mod.handleWithMap(clone(event({ firmId, uri: A + route + tail })), map, CANON);
        const got = out && out.uri;
        if (got === want && out.origin.s3.domainName === DOMAIN("opal-data-49financial")) ok++;
        else bad.push(`${firmId} ${route + tail} -> ${got} (${out && out.origin && out.origin.s3.domainName}) want ${want}`);
      }
    }
  });
  console.log(`F6 SEAM: ${ok} of ${n} served-class requests rewrite to the key the table gives (router-reachable classes ${rows.length - unreachable.length} of ${rows.length}; not reachable by any route: ${unreachable.join(", ") || "none"})`);
  for (const b of bad.slice(0, 5)) console.log("  MISS " + b);

  let ctl = 0, nctl = 0;
  const check = async (label, ev, pred) => {
    nctl++;
    const out = await quiet(async () => mod.handleWithMap(clone(ev), map, CANON));
    if (pred(out)) ctl++; else console.log("  CONTROL FAILED: " + label + " -> " + JSON.stringify(out).slice(0, 160));
  };
  nctl++;
  {
    const out = await quiet(async () => mod.handleWithMap(clone(event({ firmId: "49financial", uri: A + "views/firm_composition.json" })), map));
    if (out.uri === "/gold/views/firm_composition.json") ctl++;
    else console.log("  CONTROL FAILED: the shipped (empty) list must change nothing even under the cutover map -> " + JSON.stringify(out).slice(0, 160));
  }
  await check("unplaced class refused", event({ firmId: "49financial", uri: A + "timeseries/synthetic_positions_index.json" }),
    (o) => o.status === "404" && JSON.parse(o.body).error === "unplaced_canonical_resource");
  await check("flat legacy path unplaced", event({ firmId: "49financial", uri: A + "summary/header_metrics.json" }),
    (o) => o.status === "404" || (o.uri && o.uri.startsWith("/advi/49financial/platinum/artifacts/")));
  await check("inflection stays legacy", event({ firmId: "inflection", uri: A + "views/firm_composition.json" }),
    (o) => o.uri === "/gold/views/firm_composition.json" && o.origin.s3.domainName === DOMAIN("opal-data-inf"));
  await check("cottonwood stays legacy", event({ firmId: "cottonwood", uri: A + "views/firm_composition.json" }),
    (o) => o.uri === "/gold/views/firm_composition.json" && o.origin.s3.domainName === DOMAIN("opal-data-cot"));
  await check("twin class untouched", event({ firmId: "49financial", uri: A + "platinum/advi/49financial/mix_summary.json" }),
    (o) => o.uri === "/platinum/advi/49financial/mix_summary.json" && o.origin.s3.domainName === DOMAIN("opal-data-portal-v2"));
  await check("twin class cross-firm refused", event({ firmId: "49financial", uri: A + "platinum/advi/inflection/mix_summary.json" }),
    (o) => o.status === "401");
  await check("PII-blocked summary still refused", event({ firmId: "49financial", uri: A + "platinum/clients/z0893649/summary.json" }),
    (o) => o.status === "401");
  await check("satellites branch untouched", event({ firmId: "49financial", uri: "/api/scoped/satellites/registry.json" }),
    (o) => o.uri === "/platinum/satellites/registry.json");
  await check("satellites unknown leaf still 404", event({ firmId: "49financial", uri: "/api/scoped/satellites/nope.json" }),
    (o) => o.status === "404" && JSON.parse(o.body).error === "unknown_satellites_resource");
  console.log(`F6 SEAM CONTROLS: ${ctl} of ${nctl} (empty list inert; unplaced refused; other firms, twin class, PII block, satellites unchanged)`);
  return ok === n && n > 0 && ctl === nctl && bad.length === 0 ? 0 : 1;
}

const code = arm === "diff" ? await diff() : arm === "seam" ? await seam() : (console.log("usage: diff|seam"), 2);
process.exit(code);
