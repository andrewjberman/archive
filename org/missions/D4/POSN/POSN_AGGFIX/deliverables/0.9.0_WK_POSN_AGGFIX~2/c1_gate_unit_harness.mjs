#!/usr/bin/env node
/**
 * GATE_UNIT_HARNESS_C1 -- POSN_AGGFIX.TO-C1-1, criterion C1-AC4 (cell AF1-s-11).
 *
 * Drives the REAL auth-validator-edge `handler` (infra/aws/lambda-edge/auth-validator-edge/index.mjs in
 * this worktree) with synthetic CloudFront viewer-request events. The JWT verify is replaced IN-PROCESS by
 * a node:module resolve hook: `../../lambda/lib/authkeys/jwtPublicKeys.mjs` resolves to a stub whose
 * verifyWithSlots returns the claim set registered for the presented token, `jsonwebtoken` and
 * `@aws-sdk/client-s3` resolve to stubs that throw if touched. Everything else the handler imports
 * (tier_policy.mjs, aggregate_gate.mjs, ../_shared/firm-config.mjs) is the real file.
 *
 * NEGATIVE CONTROL: a scratch copy of index.mjs with the gate call block removed (the lines from
 * `// --- POSN_AGGFIX AF1-s-11` through `// --- end POSN_AGGFIX AF1-s-11 ---`, asserted present exactly
 * once), its relative imports resolved against the real directory. It must let advisor and client
 * through on the aggregate URLs and on the three encoded forms -- so a harness that could not see a
 * missing gate fails here.
 *
 * FORWARDED-URI RESOLUTION: for a PASS-THROUGH the forwarded request is run through the REAL
 * public-data-router handler and the rewritten path is percent-decoded the way S3 decodes a request path,
 * giving the key the origin would resolve; it is printed beside every row.
 *
 * Exit 0 only when every row matches its expectation.
 */
import { registerHooks } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  AGG_URLS, AMENDMENT_URLS, CLASS_ORDER, ADMITTED, CONTROL_URL, ENCODED_URLS, KEY, claimsFor, splitUrl,
} from "./c1_classes.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = execFileSync("git", ["rev-parse", "--show-toplevel"], { cwd: HERE, encoding: "utf8" }).trim();
const EDGE_DIR = path.join(ROOT, "infra", "aws", "lambda-edge", "auth-validator-edge");
const REAL_INDEX = path.join(EDGE_DIR, "index.mjs");
const PDR_INDEX = path.join(ROOT, "infra", "aws", "lambda-edge", "public-data-router", "index.mjs");
const SCRATCH = path.join(ROOT, ".scratch", "c1_harness");
const NEG_PATH = path.join(SCRATCH, "index.nogate.mjs");
const REAL_URL = pathToFileURL(REAL_INDEX).href;
const NEG_URL = pathToFileURL(NEG_PATH).href;

const data = (src) => "data:text/javascript," + encodeURIComponent(src);
const STUB_JWT = data("export default { verify() { throw new Error('harness: jsonwebtoken.verify must not run'); } };");
const STUB_S3 = data("export class S3Client { send() { throw new Error('harness: no S3'); } }\n" +
  "export class GetObjectCommand { constructor(i) { this.input = i; } }");
const STUB_KEYS = data(
  "export async function getJwtKeySlots() { return { current: 'harness-slot', previous: null }; }\n" +
  "export function verifyWithSlots(_lib, token) {\n" +
  "  const c = globalThis.__C1_HARNESS_TOKENS__.get(token);\n" +
  "  if (!c) throw new Error('harness: unknown token');\n" +
  "  globalThis.__C1_HARNESS_VERIFY_CALLS__ += 1;\n" +
  "  return { ...c };\n" +
  "}\n");

globalThis.__C1_HARNESS_TOKENS__ = new Map();
globalThis.__C1_HARNESS_VERIFY_CALLS__ = 0;

registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier === "jsonwebtoken") return { url: STUB_JWT, shortCircuit: true };
    if (specifier === "@aws-sdk/client-s3") return { url: STUB_S3, shortCircuit: true };
    if (specifier.endsWith("lambda/lib/authkeys/jwtPublicKeys.mjs")) return { url: STUB_KEYS, shortCircuit: true };
    if (context.parentURL === NEG_URL && (specifier.startsWith("./") || specifier.startsWith("../"))) {
      return nextResolve(specifier, { ...context, parentURL: REAL_URL });
    }
    return nextResolve(specifier, context);
  },
});

// ---- the negative-control copy -------------------------------------------------------------------
const realSrc = readFileSync(REAL_INDEX, "utf8");
const lines = realSrc.split("\n");
const startIdx = lines.findIndex((l) => l.includes("// --- POSN_AGGFIX AF1-s-11:"));
const endIdx = lines.findIndex((l) => l.includes("// --- end POSN_AGGFIX AF1-s-11 ---"));
const starts = lines.filter((l) => l.includes("// --- POSN_AGGFIX AF1-s-11:")).length;
const ends = lines.filter((l) => l.includes("// --- end POSN_AGGFIX AF1-s-11 ---")).length;
if (starts !== 1 || ends !== 1 || endIdx <= startIdx) {
  console.log(`ERROR: gate call markers start=${starts} end=${ends}; cannot build the negative control`);
  process.exit(2);
}
const negLines = lines.slice(0, startIdx).concat(lines.slice(endIdx + 1));
if (negLines.join("\n").includes("aggregateGate(")) {
  console.log("ERROR: the negative-control copy still calls aggregateGate");
  process.exit(2);
}
mkdirSync(SCRATCH, { recursive: true });
writeFileSync(NEG_PATH, negLines.join("\n"));

// ---- capture the handler's log lines ------------------------------------------------------------
const captured = [];
for (const lvl of ["log", "warn", "error"]) {
  const orig = console[lvl].bind(console);
  console[lvl] = (...a) => { captured.push({ lvl, msg: a.join(" ") }); };
  console[`_${lvl}`] = orig;
}
const out = (...a) => console._log(...a);

let gated;
let nogate;
let pdr;
try {
  gated = (await import(REAL_URL)).handler;
  nogate = (await import(NEG_URL)).handler;
  pdr = (await import(pathToFileURL(PDR_INDEX).href)).handler;
} catch (e) {
  out(`ERROR: module load failed: ${e && e.stack}`);
  process.exit(2);
}

let tokenSeq = 0;
function tokenFor(claims) {
  tokenSeq += 1;
  const t = `harness-token-${tokenSeq}`;
  globalThis.__C1_HARNESS_TOKENS__.set(t, claims);
  return t;
}

function eventFor(url, token, shape = "cloudfront") {
  const { uri, querystring } = shape === "cloudfront" ? splitUrl(url) : { uri: url, querystring: "" };
  const headers = { host: [{ key: "Host", value: "opalinvest.dev" }] };
  if (token) headers.authorization = [{ key: "Authorization", value: `Bearer ${token}` }];
  return { Records: [{ cf: { request: { clientIp: "203.0.113.7", method: "GET", uri, querystring, headers } } }] };
}

async function resolvedKey(uri) {
  const ev = { Records: [{ cf: { request: { method: "GET", uri, querystring: "", headers: {} } } }] };
  const r = await pdr(ev);
  let p = r.uri;
  try {
    p = decodeURIComponent(p);
  } catch {
    // S3 would reject a malformed escape; keep it raw
  }
  return p.replace(/^\//, "");
}

async function drive(handler, cls, url, shape = "cloudfront") {
  const iat = Math.floor(Date.now() / 1000);
  const claims = cls ? claimsFor(cls, iat) : null;
  const ev = eventFor(url, claims ? tokenFor(claims) : null, shape);
  const req = ev.Records[0].cf.request;
  const before = captured.length;
  const r = await handler(ev);
  const logs = captured.slice(before);
  if (r === req) {
    return { result: "PASS-THROUGH", forwarded: r.uri, key: await resolvedKey(r.uri), logs, raw: r };
  }
  let body = "";
  try {
    body = JSON.parse(r.body).error;
  } catch {
    body = String(r.body);
  }
  return { result: String(r.status), forwarded: "-", key: "-", body, logs, raw: r };
}

const rows = [];
function record(section, cls, url, got, expectText, ok) {
  rows.push({ section, ok });
  const tail = got.result === "PASS-THROUGH" ? `forwarded ${got.forwarded} -> key ${got.key}` : `body "${got.body}"`;
  out(`  ${ok ? "MATCH   " : "MISMATCH"} ${cls.padEnd(8)} ${url.padEnd(54)} ${got.result.padEnd(13)} ${tail}   [expect ${expectText}]`);
}

out("C1-AC4 GATE_UNIT_HARNESS_C1");
out(`  real handler: ${REAL_INDEX}`);
out(`  negative control: ${NEG_PATH} (removed lines ${startIdx + 1}-${endIdx + 1} of ${lines.length}, ${endIdx - startIdx + 1} lines)`);
out(`  JWT verify: replaced in-process (resolve hook on ../../lambda/lib/authkeys/jwtPublicKeys.mjs); jsonwebtoken and @aws-sdk/client-s3 stubbed to throw if touched`);
out(`  forwarded-URI resolution: real public-data-router ${PDR_INDEX}, then S3-style percent-decoding`);

out("");
out("PART A -- 4 classes x (2 aggregate URLs + control), gated handler");
for (const cls of CLASS_ORDER) {
  for (const url of [...AGG_URLS, CONTROL_URL]) {
    const got = await drive(gated, cls, url);
    const isAgg = url !== CONTROL_URL;
    const expectDeny = isAgg && !ADMITTED.has(cls);
    const ok = expectDeny ? got.result === "401" : got.result === "PASS-THROUGH";
    record("A", cls, url, got, expectDeny ? "401" : "PASS-THROUGH", ok);
  }
}

out("");
out("PART B -- NEGATIVE CONTROL: advisor and client on both aggregate URLs, handler WITHOUT the gate call");
for (const cls of ["advisor", "client"]) {
  for (const url of AGG_URLS) {
    const got = await drive(nogate, cls, url);
    record("B", cls, url, got, "PASS-THROUGH", got.result === "PASS-THROUGH" && got.key === KEY);
  }
}

out("");
out("PART C -- AMENDMENT 1: encoded, query and double-slash forms x 4 classes, gated handler (CloudFront event shape: query in querystring)");
for (const cls of CLASS_ORDER) {
  for (const url of AMENDMENT_URLS) {
    const got = await drive(gated, cls, url);
    let ok;
    let expectText;
    if (ADMITTED.has(cls)) {
      ok = got.result === "PASS-THROUGH";
      expectText = "PASS-THROUGH";
    } else {
      ok = got.result === "401" || (got.result === "PASS-THROUGH" && got.key !== KEY);
      expectText = "401, or PASS-THROUGH to a key other than " + KEY;
    }
    record("C", cls, url, got, expectText, ok);
  }
}

out("");
out("PART D -- AMENDMENT 1 NEGATIVE CONTROL: advisor and client on the three encoded forms, handler WITHOUT the gate call");
for (const cls of ["advisor", "client"]) {
  for (const url of ENCODED_URLS) {
    const got = await drive(nogate, cls, url);
    record("D", cls, url, got, "PASS-THROUGH to " + KEY, got.result === "PASS-THROUGH" && got.key === KEY);
  }
}

out("");
out("SUPPLEMENTARY (not counted in A-D): readings for C1-AC16 and the gate's query strip on a raw URI");
const supp = [
  ["advisor", "/api/general/positioning/opal_aggregate.json?v=1", "raw", "401"],
  ["partner-admin", AGG_URLS[0], "cloudfront", "401"],
  ["forged-internal-tier", AGG_URLS[0], "cloudfront", "401"],
  ["unauthenticated", AGG_URLS[0], "cloudfront", "401"],
];
const extraClaims = {
  "partner-admin": { sub: "qa-posn-aggfix-partner-admin", role: "admin", firmRole: "admin", tier: "advisor", firmId: "49financial" },
  "forged-internal-tier": { sub: "qa-posn-aggfix-internal-tier", role: "user", tier: "internal", firmId: "49financial" },
};
for (const [name, url, shape, want] of supp) {
  let got;
  if (name === "unauthenticated") {
    got = await drive(gated, null, url, shape);
  } else if (extraClaims[name]) {
    const iat = Math.floor(Date.now() / 1000);
    const ev = eventFor(url, tokenFor({ ...extraClaims[name], iat, exp: iat + 300 }), shape);
    const r = await gated(ev);
    got = r === ev.Records[0].cf.request
      ? { result: "PASS-THROUGH", forwarded: r.uri, key: await resolvedKey(r.uri) }
      : { result: String(r.status), body: JSON.parse(r.body).error };
  } else {
    got = await drive(gated, name, url, shape);
  }
  const tail = got.result === "PASS-THROUGH" ? `forwarded ${got.forwarded} -> key ${got.key}` : `body "${got.body}"`;
  out(`  ${got.result === want ? "as-read " : "DIFFERS "} ${name.padEnd(21)} ${url.padEnd(52)} shape=${shape.padEnd(10)} ${got.result} ${tail}`);
}

out("");
out("SUPPLEMENTARY: non-aggregate URIs on other behaviour families -- gated vs no-gate handler output deep-equal");
const others = [
  "/api/scoped/advisor-intelligence/artifacts/firm_composition.json",
  "/api/scoped/advisor-intelligence/clients/abc/detail",
  "/api/scoped/advisor-intelligence/platinum/advisors/qa-posn-aggfix-advisor/book.json",
  "/api/scoped/satellites/registry.json",
  "/api/private/portfolio/summary",
  "/v1/health",
  "/api/general/positioning/positioning_data.json",
  "/api/general/json-tiered/positioning/tier.json",
  "/api/general/positioning/opal_aggregate.jsonx",
  "/api/general/positioning/opal_aggregate.json/",
];
let same = 0;
let total = 0;
const strip = (r, req) => JSON.stringify(r === req ? { pass: true, uri: r.uri, headers: r.headers } : r);
for (const cls of CLASS_ORDER) {
  for (const url of others) {
    const iat = Math.floor(Date.now() / 1000);
    const claims = claimsFor(cls, iat);
    const t1 = tokenFor(claims);
    const e1 = eventFor(url, t1);
    const e2 = eventFor(url, t1);
    const r1 = await gated(e1);
    const r2 = await nogate(e2);
    total += 1;
    if (strip(r1, e1.Records[0].cf.request) === strip(r2, e2.Records[0].cf.request)) same += 1;
    else out(`  DIFFERS ${cls} ${url}`);
  }
}
out(`  NON-AGGREGATE URIS IDENTICAL gated vs no-gate: ${same} of ${total}`);

const denied = captured.filter((c) => c.msg.includes('"event":"aggregate_denied"'));
out("");
out(`LOG: aggregate_denied lines ${denied.length}; sample: ${denied[0] ? denied[0].msg : "(none)"}`);
out(`VERIFY STUB CALLS: ${globalThis.__C1_HARNESS_VERIFY_CALLS__}`);

const by = (s) => rows.filter((r) => r.section === s);
const cnt = (s) => `${by(s).filter((r) => r.ok).length} of ${by(s).length}`;
out("");
out(`PART A (12 rows): ${cnt("A")} MATCH`);
out(`PART B NEGATIVE CONTROL: ${cnt("B")} MATCH`);
out(`PART C AMENDMENT 1 GATED: ${cnt("C")} MATCH`);
out(`PART D AMENDMENT 1 NEGATIVE CONTROL: ${cnt("D")} MATCH`);
const all = rows.every((r) => r.ok) && same === total;
out(`C1-AC4 HARNESS VERDICT: ${all ? "ALL ROWS MATCH" : "MISMATCH PRESENT"} (${rows.filter((r) => r.ok).length} of ${rows.length} rows)`);
process.exit(all ? 0 : 1);
