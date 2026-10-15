#!/usr/bin/env node
/**
 * q1_harness.mjs -- MDPF_CANON CN-q-1 issuer harness (driven by r9_cn_q_1.py; ASCII only).
 *
 * Drives the REAL auth-validator-edge `handler` (<root>/infra/aws/lambda-edge/auth-validator-edge/index.mjs) with synthetic
 * CloudFront viewer-request events. The JWT verify is replaced in-process by a node:module resolve hook: the shared key
 * module resolves to a stub whose verifyWithSlots returns the claim set registered for the presented token; jsonwebtoken,
 * the S3 client and the Secrets Manager client resolve to stubs that throw if touched (the render branch then reads "not a
 * render token" and falls through, as in production with no render key). Everything else the handler imports is the real
 * file. No AWS call, no network, no secret.
 *
 * NEGATIVE CONTROL (no source surgery): a second instance of the SAME index.mjs (import URL + "?nogate") whose
 * ./mdpf_gate.mjs resolves to an always-pass stub. A harness that cannot see a missing gate fails its arm.
 *
 *   node q1_harness.mjs <handler|seam|control> --root <tree root>
 * Prints "ARM <id> <PASS|FAIL> n=<rows> bad=<mismatches> :: <what>" per arm, up to 6 mismatch rows per failing arm, and
 * a final "TOTAL <passed> of <arms>". Exit 0 always (the python driver decides); exit 2 on a load error.
 */
import { registerHooks } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
const MODE = argv[0];
const rootAt = argv.indexOf("--root");
const ROOT = rootAt === -1 ? process.cwd() : path.resolve(argv[rootAt + 1]);
const EDGE = path.join(ROOT, "infra", "aws", "lambda-edge", "auth-validator-edge");
const PDR = path.join(ROOT, "infra", "aws", "lambda-edge", "public-data-router", "index.mjs");
const INDEX_URL = pathToFileURL(path.join(EDGE, "index.mjs")).href;
const GATE_PATH = path.join(EDGE, "mdpf_gate.mjs");

const data = (src) => "data:text/javascript," + encodeURIComponent(src);
const STUB_JWT = data("export default { verify() { throw new Error('harness: jsonwebtoken.verify must not run'); }, decode() { return null; } };");
const STUB_S3 = data("export class S3Client { send() { throw new Error('harness: no S3'); } }\n" +
  "export class GetObjectCommand { constructor(i) { this.input = i; } }");
const STUB_SM = data("export class SecretsManagerClient { async send() { throw new Error('harness: no Secrets Manager'); } }\n" +
  "export class GetSecretValueCommand { constructor(i) { this.input = i; } }");
const STUB_KEYS = data(
  "export async function getJwtKeySlots() { return { current: 'harness-slot', previous: null }; }\n" +
  "export function parseKeySlots() { throw new Error('harness: parseKeySlots must not run'); }\n" +
  "export function verifyWithSlots(_lib, token) {\n" +
  "  const c = globalThis.__Q1_TOKENS__.get(token);\n" +
  "  if (!c) throw new Error('harness: unknown token');\n" +
  "  return { ...c };\n" +
  "}\n");
const STUB_NOGATE = data("export const MDPF_PASS = 'pass'; export const MDPF_DENY = 'deny';\n" +
  "export function mdpfGate() { return 'pass'; }\n");
globalThis.__Q1_TOKENS__ = new Map();

registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier === "jsonwebtoken") return { url: STUB_JWT, shortCircuit: true };
    if (specifier === "@aws-sdk/client-s3") return { url: STUB_S3, shortCircuit: true };
    if (specifier === "@aws-sdk/client-secrets-manager") return { url: STUB_SM, shortCircuit: true };
    if (specifier.endsWith("lambda/lib/authkeys/jwtPublicKeys.mjs")) return { url: STUB_KEYS, shortCircuit: true };
    if (String(context.parentURL || "").endsWith("?nogate") && /(^|\/)mdpf_gate\.mjs$/.test(specifier)) {
      return { url: STUB_NOGATE, shortCircuit: true };
    }
    return nextResolve(specifier, context);
  },
});

const captured = [];
for (const lvl of ["log", "warn", "error"]) {
  console[lvl] = (...a) => { captured.push({ lvl, msg: a.join(" ") }); };
}
const out = (s) => process.stdout.write(s + "\n");

let gated;
let nogate;
let pdr;
let FC = {};
try {
  FC = await import(pathToFileURL(path.join(ROOT, "infra", "aws", "lambda-edge", "_shared", "firm-config.mjs")).href);
  gated = (await import(INDEX_URL)).handler;
  nogate = (await import(INDEX_URL + "?nogate")).handler;
  pdr = (await import(pathToFileURL(PDR).href)).handler;
} catch (e) {
  out("ERROR: module load failed: " + (e && e.stack));
  process.exit(2);
}

// ---- synthetic claim sets (the claim names are portal_authorizer's: firmId, userType, role, firmRole, tier) -----------
const CLAIMS = {
  internal: { sub: "staff@opal.test", firmId: "opal-capital", role: "admin", userType: "Staff" },
  dev: { sub: "dev@opal.test", firmId: "opal-capital", userType: "Dev", role: "admin" },
  devPartner: { sub: "dev2@opal.test", firmId: "49financial", userType: "Dev" },
  p49: { sub: "a@49.test", firmId: "49financial", role: "user", advisorRole: "architect" },
  p49admin: { sub: "b@49.test", firmId: "49financial", role: "admin", firmRole: "admin", tier: "internal" },
  inf: { sub: "a@inf.test", firmId: "inflection", role: "user" },
  infadmin: { sub: "b@inf.test", firmId: "inflection", role: "admin", firmRole: "admin" },
  cot: { sub: "a@cot.test", firmId: "cottonwood", role: "user" },
  demo: { sub: "a@demo.test", firmId: "demo", role: "user" },
  nofirm: { sub: "a@none.test", role: "user" },
  emptyfirm: { sub: "a@empty.test", firmId: "", role: "user" },
  nullfirm: { sub: "a@null.test", firmId: null, role: "user" },
  mockadv: { sub: "a@mock.test", firmId: "mockadv", role: "user" },
  proto: { sub: "a@p.test", firmId: "__proto__", role: "user" },
  ctor: { sub: "a@c.test", firmId: "constructor", role: "user" },
  bd: { sub: "a@bd.test", firmId: "bd", role: "user" },
  numfirm: { sub: "a@n.test", firmId: 49, role: "user" },
  objfirm: { sub: "a@o.test", firmId: {}, role: "user" },
  spacefirm: { sub: "a@s.test", firmId: " inflection", role: "user" },
  upperfirm: { sub: "a@u.test", firmId: "Inflection", role: "user" },
};
const INTERNAL = new Set(["internal", "dev", "devPartner"]);
// the folder(s) each non-internal claim may read (the order's table; the oracle for every arm)
const OWN = {
  p49: ["49financial"], p49admin: ["49financial"], inf: ["inflection"], infadmin: ["inflection"], cot: ["cottonwood"],
  demo: ["global"], nofirm: ["global"], emptyfirm: ["global"], nullfirm: ["global"],
  mockadv: ["mockadv"], proto: [], ctor: [], bd: [], numfirm: [], objfirm: [], spacefirm: [], upperfirm: [],
};
const FOLDERS = ["49financial", "inflection", "cottonwood", "global"];
const ODD_FOLDERS = ["_manifests", "archive", "mockadv", "demo", "49financial-old", "inflectionx", "globalx"];
const FILES = ["aggregate-aua-timeseries.json", "aum-metrics.json", "category-views.json", "category-views-history.json", "account-distribution.json", "account-units.json", "non-model-assets.json"];
const P = "/api/general/mdpf/";

let seq = 0;
function tokenFor(claims) {
  seq += 1;
  const t = "q1-token-" + seq;
  globalThis.__Q1_TOKENS__.set(t, claims);
  return t;
}
function eventFor(uri, qs, token, method = "GET") {
  const headers = { host: [{ key: "Host", value: "opalinvest.dev" }] };
  if (token) headers.authorization = [{ key: "Authorization", value: "Bearer " + token }];
  return { Records: [{ cf: { request: { clientIp: "203.0.113.7", method, uri, querystring: qs || "", headers } } }] };
}
// verdict: "pass" (request returned unchanged), else the status string
async function drive(handler, claimName, uri, qs = "", method = "GET") {
  const claims = claimName ? CLAIMS[claimName] : null;
  const token = claims ? tokenFor(claims) : null;
  const ev = eventFor(uri, qs, token, method);
  const req = ev.Records[0].cf.request;
  const before = captured.length;
  const r = await handler(ev);
  const logs = captured.slice(before);
  if (r === req) return { v: "pass", req: r, logs, token };
  return { v: String(r.status), res: r, logs, token };
}

const arms = [];
function arm(id, what, rows, extraOk = true) {
  const bad = rows.filter((r) => !r.ok);
  const ok = extraOk && bad.length === 0 && rows.length > 0;
  arms.push({ id, ok });
  out(`ARM ${id} ${ok ? "PASS" : "FAIL"} n=${rows.length} bad=${bad.length} :: ${what}`);
  if (!ok) for (const b of bad.slice(0, 6)) out(`  MISMATCH ${b.name} expect=${b.expect} got=${b.got}`);
  if (!ok && rows.length === 0) out("  (no rows ran)");
}
async function rowOf(handler, claimName, uri, expect, qs = "") {
  const g = await drive(handler, claimName, uri, qs);
  return { name: `${claimName || "notoken"} ${uri}${qs ? "?" + qs : ""}`, expect, got: g.v, ok: g.v === expect, g };
}

async function handlerMode() {
  // A1 no token / malformed token: 401 (control)
  {
    const rows = [];
    for (const f of FOLDERS) rows.push(await rowOf(gated, null, `${P}${f}/aum-metrics.json`, "401"));
    // a token the stub does not know -> verify throws -> 401
    const ev = eventFor(`${P}49financial/aum-metrics.json`, "", "not-a-registered-token");
    const r = await gated(ev);
    rows.push({ name: "unknown bearer", expect: "401", got: String(r.status), ok: String(r.status) === "401" });
    arm("A1", "no token and an unverifiable token -> 401 on a MDPF leaf (control)", rows);
  }
  // A2 own leaf passes, every file (control)
  {
    const rows = [];
    for (const c of ["p49", "inf", "cot"]) {
      for (const f of FILES) rows.push(await rowOf(gated, c, `${P}${OWN[c][0]}/${f}`, "pass"));
    }
    for (const c of ["demo", "nofirm", "emptyfirm", "nullfirm"]) {
      for (const f of FILES) rows.push(await rowOf(gated, c, `${P}global/${f}`, "pass"));
    }
    // mockadv is a key of the generated firm map, so it reads the folder of its own name (none exists in the bucket; harmless) and not global
    rows.push(await rowOf(gated, "mockadv", `${P}mockadv/aum-metrics.json`, "pass"));
    arm("A2", "own-folder leaf passes: three partners on their folder, demo and no-firm on global, mockadv on its own name (control)", rows);
  }
  // A3 foreign leaf 403 (build)
  {
    const rows = [];
    for (const c of ["p49", "inf", "cot", "p49admin", "infadmin"]) {
      for (const t of [...FOLDERS, ...ODD_FOLDERS]) {
        if (OWN[c].includes(t)) continue;
        for (const f of ["aggregate-aua-timeseries.json", "category-views-history.json"]) rows.push(await rowOf(gated, c, `${P}${t}/${f}`, "403"));
      }
    }
    arm("A3", "a partner reading any other folder (incl. global, _manifests, archive) -> 403", rows);
  }
  // A4 internal passes every folder, odd shapes too (control)
  {
    const rows = [];
    for (const c of ["internal", "dev", "devPartner"]) {
      for (const t of [...FOLDERS, ...ODD_FOLDERS]) rows.push(await rowOf(gated, c, `${P}${t}/aum-metrics.json`, "pass"));
      rows.push(await rowOf(gated, c, `${P}global/category-views-history.json`, "pass"));
      rows.push(await rowOf(gated, c, "/api/general/mdpf", "pass"));
    }
    arm("A4", "opal-capital and a Dev claim pass every folder under the prefix (control)", rows);
  }
  // A5 demo: global only (build)
  {
    const rows = [];
    for (const t of ["49financial", "inflection", "cottonwood", "demo", "_manifests", "archive"]) rows.push(await rowOf(gated, "demo", `${P}${t}/aum-metrics.json`, "403"));
    arm("A5", "the demo tenant is refused every folder but global", rows);
  }
  // A6 no firm: global only (build)
  {
    const rows = [];
    for (const c of ["nofirm", "emptyfirm", "nullfirm"]) {
      for (const t of ["49financial", "inflection", "cottonwood", "demo", "_manifests", "archive"]) rows.push(await rowOf(gated, c, `${P}${t}/aum-metrics.json`, "403"));
    }
    arm("A6", "a claim with no firm (absent, empty, null) is refused every folder but global", rows);
  }
  // A7 unknown firm: nothing (build)
  {
    const rows = [];
    for (const c of ["proto", "ctor", "bd", "numfirm", "objfirm", "spacefirm", "upperfirm"]) {
      for (const t of ["global", "49financial", "inflection", "mockadv", "__proto__", "constructor"]) rows.push(await rowOf(gated, c, `${P}${t}/aum-metrics.json`, "403"));
    }
    // mockadv is a map key, so it reads its own name only: not global, not a partner folder
    for (const t of ["global", "49financial", "inflection", "cottonwood", "demo", "_manifests"]) rows.push(await rowOf(gated, "mockadv", `${P}${t}/aum-metrics.json`, "403"));
    arm("A7", "an unknown, prototype-key, non-string or case-variant firmId is refused every folder, global included; mockadv reads its own name only", rows);
  }
  // A8 role/tier admin does not bypass (build)
  {
    const rows = [];
    for (const c of ["p49admin", "infadmin"]) {
      for (const t of ["global", "cottonwood", "inflection", "49financial"]) {
        if (OWN[c].includes(t)) continue;
        rows.push(await rowOf(gated, c, `${P}${t}/aum-metrics.json`, "403"));
      }
    }
    arm("A8", "a partner-firm admin (role admin, firmRole admin, tier internal) is held to its own folder", rows);
  }
  // A9 non-leaf shapes (build)
  {
    const rows = [];
    for (const c of ["p49", "demo", "nofirm"]) {
      for (const u of ["/api/general/mdpf", "/api/general/mdpf/", "/api/general/mdpf//", "/api/general/mdpf/_manifests/2026-10-14/x.json", "/api/general/mdpf/archive/aggregate_aua/x.json"]) {
        rows.push(await rowOf(gated, c, u, "403"));
      }
    }
    arm("A9", "the bare prefix and the non-firm folders (_manifests, archive) are refused to every non-internal claim", rows);
  }
  // A10 path tricks, all as the 49financial claim reaching for inflection or escaping its folder (build)
  {
    const own = "49financial";
    const tricks = [
      `${P}${own}/../inflection/aum-metrics.json`, `${P}./inflection/aum-metrics.json`, `${P}${own}/./../inflection/aum-metrics.json`,
      `${P}/inflection/aum-metrics.json`, `${P}${own}//../inflection/aum-metrics.json`,
      `${P}${own}/%2e%2e/inflection/aum-metrics.json`, `${P}${own}/%2E%2E/inflection/aum-metrics.json`, `${P}${own}/.%2e/inflection/aum-metrics.json`,
      `${P}${own}%2f..%2finflection%2faum-metrics.json`, `${P}${own}%2F..%2Finflection%2Faum-metrics.json`,
      `${P}%69nflection/aum-metrics.json`, `${P}%2569nflection/aum-metrics.json`, `${P}%252569nflection/aum-metrics.json`,
      `${P}${own}/%252e%252e/inflection/aum-metrics.json`,
      `${P}${own}%5c..%5cinflection/aum-metrics.json`, `${P}${own}\\..\\inflection/aum-metrics.json`,
      `${P}Inflection/aum-metrics.json`, `${P}INFLECTION/aum-metrics.json`, `${P}iNfLeCtIoN/aum-metrics.json`,
      `${P}49Financial/aum-metrics.json`, `${P}49FINANCIAL/aum-metrics.json`,
      "/API/general/mdpf/49financial/aum-metrics.json", "/api/general/MDPF/49financial/aum-metrics.json", "/api/GENERAL/mdpf/inflection/aum-metrics.json",
      "/api/general/%6Ddpf/inflection/aum-metrics.json", "/api/general/%6ddpf/49financial/aum-metrics.json",
      "/api/general/json/mdpf/inflection/aum-metrics.json", "/api/general/json/%6Ddpf/inflection/aum-metrics.json",
      `${P}inflection/`, `${P}inflection`, `${P}inflection/.`, `${P}inflection/..`,
      `${P}${own}/aum-metrics.json%00.png`, `${P}${own}%00/../inflection/aum-metrics.json`, `${P}inflection%00/aum-metrics.json`,
      `${P}inflection%20/aum-metrics.json`, `${P}%20inflection/aum-metrics.json`, `${P}inflection./aum-metrics.json`, `${P}inflection%09/aum-metrics.json`,
      `${P}%E0%A4%A/inflection/aum-metrics.json`, `${P}${own}/%E0%A4%A/../inflection/x.json`, `${P}%/inflection/x.json`,
      `${P}${own};/..;/inflection/aum-metrics.json`, `${P}${own}%3b/inflection/x.json`,
      `${P}%EF%BC%8Finflection/aum-metrics.json`, `${P}${own}%EF%BC%8F..%EF%BC%8Finflection/x.json`,
      `${P}${own}/aum-metrics.json/../../inflection/aum-metrics.json`, `${P}${own}/aum-metrics.json/%2e%2e/%2e%2e/inflection/aum-metrics.json`,
      `${P}${own}//aum-metrics.json`, `${P}${own}/sub//aum-metrics.json`, `${P}${own}/aum-metrics.json//`,
      `${P}${own}%3Fx/../inflection/x.json`, `${P}${own}%23/../inflection/x.json`,
    ];
    const rows = [];
    for (const u of tricks) rows.push(await rowOf(gated, "p49", u, "403"));
    rows.push(await rowOf(gated, "p49", `${P}inflection/aum-metrics.json`, "403", "folder=49financial"));
    rows.push(await rowOf(gated, "p49", `${P}inflection/aum-metrics.json`, "403", "x=/49financial/aum-metrics.json"));
    arm("A10", `path tricks as the 49financial claim (traversal, encoded and double-encoded, case, backslash, NUL, space, unicode slash, query): all ${tricks.length + 2} refused`, rows);
  }
  // A11 own-folder variants that must keep working (control)
  {
    const rows = [];
    rows.push(await rowOf(gated, "p49", `${P}49financial/aum-metrics.json`, "pass", "v=2"));
    rows.push(await rowOf(gated, "p49", `${P}49financial/aum-metrics.json`, "pass", "folder=inflection"));
    rows.push(await rowOf(gated, "inf", `${P}inflection/category-views.json`, "pass", "cb=1&x=%2e%2e"));
    for (const m of ["HEAD"]) {
      const g = await drive(gated, "cot", `${P}cottonwood/account-units.json`, "", m);
      rows.push({ name: `cot ${m} own`, expect: "pass", got: g.v, ok: g.v === "pass" });
    }
    arm("A11", "own-folder leaf with a query string, and HEAD, keeps passing (control)", rows);
  }
  // A12 the denial's shape: status, JSON body, no echo, one log event, no token in any log (build)
  {
    const rows = [];
    const g = await drive(gated, "p49", `${P}inflection/aum-metrics.json`);
    const ok403 = g.v === "403";
    rows.push({ name: "status 403", expect: "403", got: g.v, ok: ok403 });
    if (ok403) {
      let body = null;
      try { body = JSON.parse(g.res.body); } catch { body = null; }
      rows.push({ name: "JSON body with an error string", expect: "string", got: body && typeof body.error, ok: !!body && typeof body.error === "string" && body.error.length > 0 });
      const text = JSON.stringify(g.res);
      for (const w of ["inflection", "49financial", "cottonwood", "global", g.token]) {
        rows.push({ name: `denial response does not echo ${w === g.token ? "the token" : w}`, expect: "absent", got: text.includes(w) ? "echoed" : "absent", ok: !text.includes(w) });
      }
      const ct = g.res.headers && g.res.headers["content-type"] && g.res.headers["content-type"][0] && g.res.headers["content-type"][0].value;
      rows.push({ name: "content-type application/json", expect: "application/json", got: String(ct), ok: ct === "application/json" });
      rows.push({ name: "no injected X-User-* header on a denial", expect: "none", got: Object.keys(g.res.headers || {}).filter((k) => k.startsWith("x-user")).join(",") || "none", ok: !Object.keys(g.res.headers || {}).some((k) => k.startsWith("x-user")) });
      const ev = g.logs.filter((l) => l.msg.includes("mdpf_scope_denied"));
      rows.push({ name: "exactly one mdpf_scope_denied log event", expect: "1", got: String(ev.length), ok: ev.length === 1 });
      let parsed = null;
      try { parsed = JSON.parse(ev[0].msg); } catch { parsed = null; }
      rows.push({ name: "the event names the claim firm and the path", expect: "jwtFirmId=49financial and path", got: parsed ? `${parsed.jwtFirmId} ${typeof parsed.path}` : "unparsed", ok: !!parsed && parsed.jwtFirmId === "49financial" && typeof parsed.path === "string" && parsed.path.includes("inflection") });
      rows.push({ name: "no log line carries the token", expect: "none", got: g.logs.some((l) => l.msg.includes(g.token)) ? "leaked" : "none", ok: !g.logs.some((l) => l.msg.includes(g.token)) });
    }
    arm("A12", "a denial is a 403 JSON body that echoes nothing, injects no header, logs one mdpf_scope_denied event, leaks no token", rows);
  }
  // A13 negative control: the harness sees a missing gate (control)
  {
    const rows = [];
    for (const c of ["p49", "inf", "demo"]) {
      for (const t of ["inflection", "49financial", "cottonwood"]) {
        if (OWN[c].includes(t)) continue;
        const g = await drive(nogate, c, `${P}${t}/aum-metrics.json`);
        rows.push({ name: `nogate ${c} ${t}`, expect: "pass", got: g.v, ok: g.v === "pass" });
      }
    }
    arm("A13", "with the gate replaced by an always-pass stub the same foreign reads are forwarded (the harness can see a missing gate; control)", rows);
  }
  // A14 an admitted request is forwarded with the existing identity headers (control)
  {
    const rows = [];
    const g = await drive(gated, "inf", `${P}inflection/aum-metrics.json`);
    const h = g.req ? g.req.headers : {};
    const val = (k) => h[k] && h[k][0] && h[k][0].value;
    rows.push({ name: "x-firm-id is the claim firm", expect: "inflection", got: String(val("x-firm-id")), ok: val("x-firm-id") === "inflection" });
    rows.push({ name: "x-origin-verify is set", expect: "cloudfront", got: String(val("x-origin-verify")), ok: val("x-origin-verify") === "cloudfront" });
    rows.push({ name: "x-user-email is the subject", expect: "a@inf.test", got: String(val("x-user-email")), ok: val("x-user-email") === "a@inf.test" });
    arm("A14", "an admitted request still carries the injected identity headers (control)", rows);
  }
}

// ---- seam: the gate against the REAL origin-request router ---------------------------------------------------------
function keyOf(uriAfterRouter) {
  let p = uriAfterRouter;
  try { p = decodeURIComponent(p); } catch { /* S3 would refuse a malformed escape; keep raw */ }
  return p.replace(/^\//, "");
}
async function routed(uri) {
  const ev = { Records: [{ cf: { request: { method: "GET", uri, querystring: "", headers: {} } } }] };
  const r = await pdr(ev);
  return keyOf(r.uri);
}
// a key is inside an admitted folder iff, wherever it names an "mdpf" segment, it is platinum|json / mdpf / <admitted> / clean rest
const hasMdpf = (k) => k.split("/").some((s) => s.toLowerCase() === "mdpf");
// the most permissive reading of a key: dot segments resolved and empty segments collapsed
function normalizedKey(key) {
  const out = [];
  for (const s of key.split("/")) {
    if (s === "." || s === "") continue;
    if (s === "..") { out.pop(); continue; }
    out.push(s);
  }
  return out.join("/");
}
function shapeBad(key, allowed) {
  const segs = key.split("/");
  if (!hasMdpf(key)) return false;
  if (!((segs[0] === "platinum" || segs[0] === "json") && segs[1] === "mdpf")) return true;
  if (!allowed.includes(segs[2])) return true;
  const rest = segs.slice(3);
  return rest.some((s, i) => s === "." || s === ".." || (s === "" && i !== rest.length - 1));
}
// a key violates iff it can reach MDPF data under some reading and is not exactly a canonical key inside an admitted folder.
// A key that no normalisation brings into mdpf (a nonexistent literal key) is harmless and is not counted.
function keyViolates(key, allowed) {
  const nk = normalizedKey(key);
  if (!hasMdpf(nk)) return false;
  return shapeBad(key, allowed) || shapeBad(nk, allowed);
}
function corpus(own) {
  const prefixes = ["/api/general/mdpf/", "/api/general/json/mdpf/", "/API/general/mdpf/", "/api/general/MDPF/", "/api/general/%6Ddpf/", "/api/general/mdpf//", "/api/general/./mdpf/", "/api/general/mdpf"];
  const targets = ["49financial", "inflection", "cottonwood", "global", "_manifests", "archive", "mockadv", "demo", "49financial-old", "inflectionx", "", "..", "."];
  const mkOwn = own || "global";
  const up = (s) => s.toUpperCase();
  const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
  const pct1 = (s) => (s ? "%" + s.charCodeAt(0).toString(16).toUpperCase().padStart(2, "0") + s.slice(1) : s);
  const dbl1 = (s) => (s ? "%25" + s.charCodeAt(0).toString(16).toUpperCase().padStart(2, "0") + s.slice(1) : s);
  const f = "aum-metrics.json";
  const out = [];
  for (const p of prefixes) {
    for (const t of targets) {
      for (const tail of [
        `${t}/${f}`, `${mkOwn}/../${t}/${f}`, `${mkOwn}/%2e%2e/${t}/${f}`, `${mkOwn}%2f..%2f${t}/${f}`, `${pct1(t)}/${f}`, `${dbl1(t)}/${f}`,
        `${up(t)}/${f}`, `${cap(t)}/${f}`, `${t}./${f}`, `${t}%00/${f}`, `${t}%20/${f}`, `${t}\\${f}`, `${t};/${f}`,
        `${mkOwn}//${t}/${f}`, `${mkOwn}/./${t}/${f}`, `${mkOwn}/${f}/../../${t}/${f}`, `${t}/`, `${t}`, ``,
      ]) out.push(p + tail);
    }
  }
  return [...new Set(out)];
}
async function seamMode() {
  const claimsForSeam = [["p49", "49financial"], ["inf", "inflection"], ["cot", "cottonwood"], ["demo", "global"], ["nofirm", "global"], ["mockadv", "mockadv"]];
  // S1 the property: nothing a non-internal claim is admitted on resolves outside its folders
  {
    const rows = [];
    let admitted = 0;
    let total = 0;
    for (const [c, own] of claimsForSeam) {
      for (const u of corpus(own)) {
        total += 1;
        const g = await drive(gated, c, u);
        if (g.v !== "pass") continue;
        admitted += 1;
        const key = await routed(g.req.uri);
        const bad = keyViolates(key, OWN[c]);
        rows.push({ name: `${c} ${u} -> ${key}`, expect: "inside", got: bad ? "OUTSIDE" : "inside", ok: !bad });
      }
    }
    out(`  corpus ${total} requests x claims, ${admitted} admitted`);
    arm("S1", "every request a non-internal claim is ADMITTED on resolves, through the real router and S3 decoding, to a key inside that claim's folders", rows);
  }
  // S2 the gate is not just denying everything: each claim's own-folder leaf is admitted and resolves where expected (control)
  {
    const rows = [];
    for (const [c, own] of claimsForSeam) {
      const g = await drive(gated, c, `${P}${own}/aum-metrics.json`);
      const key = g.v === "pass" ? await routed(g.req.uri) : "-";
      const want = `platinum/mdpf/${own}/aum-metrics.json`;
      rows.push({ name: `${c} own`, expect: want, got: key, ok: key === want });
    }
    arm("S2", "each claim's own-folder leaf is admitted and the router resolves it to platinum/mdpf/<folder>/ (control)", rows);
  }
  // S3 internal is never denied on the corpus (control)
  {
    const rows = [];
    for (const c of ["internal", "dev"]) {
      for (const u of corpus("global")) {
        const g = await drive(gated, c, u);
        rows.push({ name: `${c} ${u}`, expect: "pass", got: g.v, ok: g.v === "pass" });
      }
    }
    arm("S3", "an internal claim is admitted on the whole corpus (control)", rows);
  }
  // S4 the router instrument is live: the rewrite to platinum/mdpf/ still happens (control)
  {
    const k = await routed("/api/general/mdpf/inflection/aum-metrics.json");
    arm("S4", "the real public-data-router rewrites /api/general/mdpf/ to platinum/mdpf/ (the instrument is live; control)", [{ name: "rewrite", expect: "platinum/mdpf/inflection/aum-metrics.json", got: k, ok: k === "platinum/mdpf/inflection/aum-metrics.json" }]);
  }
  // S5 the property can fail: with the gate stubbed out, the same corpus yields violations (control)
  {
    let violations = 0;
    for (const u of corpus("49financial")) {
      const g = await drive(nogate, "p49", u);
      if (g.v !== "pass") continue;
      if (keyViolates(await routed(g.req.uri), OWN.p49)) violations += 1;
    }
    arm("S5", `with the gate stubbed out the S1 property finds ${violations} violations (it can fail; control)`, [{ name: "nogate violations", expect: ">0", got: String(violations), ok: violations > 0 }]);
  }
}

// ---- control: behaviour the cell must not move, and the pure function's robustness ---------------------------------
async function controlMode() {
  // K1 existing behaviours through the handler (control)
  {
    const rows = [];
    rows.push(await rowOf(gated, "p49", "/api/general/positioning/opal_aggregate.json", "401"));
    rows.push(await rowOf(gated, "internal", "/api/general/positioning/opal_aggregate.json", "pass"));
    rows.push(await rowOf(gated, "dev", "/api/general/json/positioning/opal_aggregate.json", "pass"));
    rows.push(await rowOf(gated, "p49", "/api/general/positioning/other.json", "pass"));
    rows.push(await rowOf(gated, "demo", "/api/general/json/market-overview/rsi-summary.json", "pass"));
    rows.push(await rowOf(gated, "p49", "/api/general/etfs/positioning/x.json", "pass"));
    rows.push(await rowOf(gated, "cot", "/api/general/mdpfx/inflection/x.json", "pass"));
    rows.push(await rowOf(gated, "cot", "/api/general/mdpf-other/inflection/x.json", "pass"));
    rows.push(await rowOf(gated, "p49", "/api/scoped/partners/books/advisor/adv-other/x.json", "403"));
    rows.push(await rowOf(gated, null, "/api/general/positioning/other.json", "401"));
    {
      const g = await drive(gated, null, "/auth/login");
      rows.push({ name: "auth login passes without a token", expect: "pass", got: g.v, ok: g.v === "pass" });
      const o = await drive(gated, null, `${P}inflection/aum-metrics.json`, "", "OPTIONS");
      rows.push({ name: "OPTIONS preflight passes without a token", expect: "pass", got: o.v, ok: o.v === "pass" });
    }
    arm("K1", "existing edge behaviour unchanged: aggregate gate, advisor scoping, other /api/general paths, a near-miss prefix (mdpfx), /auth/, OPTIONS, no token (control)", rows);
  }
  // K2 the pure module: present, the three exports, no throw on any input, deny on a malformed payload (build)
  {
    const rows = [];
    let mod = null;
    try { mod = await import(pathToFileURL(GATE_PATH).href); } catch (e) { rows.push({ name: "import mdpf_gate.mjs", expect: "loads", got: String(e && e.code || e), ok: false }); }
    if (mod) {
      const has = (n) => typeof mod[n] !== "undefined";
      rows.push({ name: "exports MDPF_PASS, MDPF_DENY, mdpfGate", expect: "present", got: has("MDPF_PASS") && has("MDPF_DENY") && typeof mod.mdpfGate === "function" ? "present" : "missing", ok: has("MDPF_PASS") && has("MDPF_DENY") && typeof mod.mdpfGate === "function" });
      rows.push({ name: "MDPF_PASS !== MDPF_DENY", expect: "distinct", got: mod.MDPF_PASS === mod.MDPF_DENY ? "same" : "distinct", ok: mod.MDPF_PASS !== mod.MDPF_DENY });
      const MAP = FC.FIRM_BUCKET_MAP;
      const GV = FC.MDPF_GLOBAL_VIEW_FIRMS;
      rows.push({ name: "firm-config.mjs exports FIRM_BUCKET_MAP and MDPF_GLOBAL_VIEW_FIRMS (the generated carriers)", expect: "present", got: MAP && GV ? "present" : "missing", ok: !!MAP && !!GV });
      const U = "/api/general/mdpf/";
      // every caller states BOTH carriers (a JS default parameter would turn an explicit undefined back into the real one)
      const call = (u, pl, m, g) => { try { return mod.mdpfGate(u, pl, m, g); } catch (e) { return "THROW"; } };
      const bad = [undefined, null, "str", 7, [], true];
      const inputs = [[undefined, {}], [null, null], [123, {}], [{}, {}], ["", {}], [U + "global/x.json", undefined], [U + "global/x.json", null],
        [U + "global/x.json", "str"], [U + "global/x.json", []], [U + "global/x.json", 7], ["%", {}], [U + "%", { firmId: "demo" }]];
      for (const [u, pl] of inputs) {
        const got = call(u, pl, MAP, GV);
        rows.push({ name: `mdpfGate(${JSON.stringify(u)}, ${JSON.stringify(pl)}) returns pass|deny`, expect: "pass|deny", got: String(got), ok: got === mod.MDPF_PASS || got === mod.MDPF_DENY });
      }
      rows.push({ name: "a MDPF uri with a non-object payload is denied", expect: "deny", got: call(U + "global/x.json", "str", MAP, GV), ok: call(U + "global/x.json", "str", MAP, GV) === mod.MDPF_DENY });
      rows.push({ name: "a non-MDPF uri passes whatever the payload", expect: "pass", got: call("/api/general/etfs/x.json", null, MAP, GV), ok: call("/api/general/etfs/x.json", null, MAP, GV) === mod.MDPF_PASS });
      // the firm map is consulted, not remembered: a missing, non-object or array map FAILS CLOSED for every non-internal claim
      for (const m of bad) {
        for (const [c, f] of [["p49", "49financial"], ["demo", "global"], ["nofirm", "global"], ["mockadv", "mockadv"]]) {
          const got = call(U + f + "/x.json", CLAIMS[c], m, GV);
          rows.push({ name: `map=${JSON.stringify(m)}: ${c} on ${f} is denied (fail closed)`, expect: "deny", got: String(got), ok: got === mod.MDPF_DENY });
        }
        const gi = call(U + "inflection/x.json", CLAIMS.internal, m, GV);
        rows.push({ name: `map=${JSON.stringify(m)}: the internal claim still passes`, expect: "pass", got: String(gi), ok: gi === mod.MDPF_PASS });
        const gn = call("/api/general/etfs/x.json", CLAIMS.p49, m, GV);
        rows.push({ name: `map=${JSON.stringify(m)}: a non-MDPF path still passes`, expect: "pass", got: String(gn), ok: gn === mod.MDPF_PASS });
      }
      // a missing or unusable global-view list means no firm views global (the demo tenant reads nothing), never a throw
      for (const g of [undefined, null, "demo", 7, {}]) {
        const got = call(U + "global/x.json", CLAIMS.demo, MAP, g);
        rows.push({ name: `globalViewFirms=${JSON.stringify(g)}: demo on global is denied`, expect: "deny", got: String(got), ok: got === mod.MDPF_DENY });
      }
      rows.push({ name: "globalViewFirms as a Set of the same ids behaves as the array", expect: "pass", got: call(U + "global/x.json", CLAIMS.demo, MAP, new Set(GV || [])), ok: call(U + "global/x.json", CLAIMS.demo, MAP, new Set(GV || [])) === mod.MDPF_PASS });
      // the map is the source of the partner folders: a synthetic map admits ITS keys and no other (no slug is remembered)
      const syn = Object.freeze({ acme: 1 });
      const sy = (id, f) => call(U + f + "/x.json", { sub: "u", firmId: id }, syn, []);
      rows.push({ name: "synthetic map: acme reads acme", expect: "pass", got: sy("acme", "acme"), ok: sy("acme", "acme") === mod.MDPF_PASS });
      rows.push({ name: "synthetic map: a real partner id that is not a key reads nothing", expect: "deny", got: sy("49financial", "49financial"), ok: sy("49financial", "49financial") === mod.MDPF_DENY });
      const np = Object.create(null); np.acme = 1;
      const npa = call(U + "acme/x.json", { sub: "u", firmId: "acme" }, np, []);
      const npc = call(U + "constructor/x.json", { sub: "u", firmId: "constructor" }, np, []);
      rows.push({ name: "null-prototype map: acme reads acme, constructor reads nothing", expect: "pass,deny", got: npa + "," + npc, ok: npa === mod.MDPF_PASS && npc === mod.MDPF_DENY });
      const g1 = call(U + "49financial/x.json", CLAIMS.p49, MAP, GV);
      const g2 = call(U + "inflection/x.json", CLAIMS.p49, MAP, GV);
      rows.push({ name: "the generated map and a real partner: 49financial reads 49financial, not inflection", expect: "pass,deny", got: g1 + "," + g2, ok: g1 === mod.MDPF_PASS && g2 === mod.MDPF_DENY });
    }
    arm("K2", "mdpf_gate.mjs: the three exports, never throws, denies a MDPF uri on a malformed payload, FAILS CLOSED on a missing or unusable firm map, reads the partner folders from the map it is given", rows);
  }
}

if (MODE === "handler") await handlerMode();
else if (MODE === "seam") await seamMode();
else if (MODE === "control") await controlMode();
else { out("ERROR: mode must be handler|seam|control"); process.exit(2); }
out(`TOTAL ${arms.filter((a) => a.ok).length} of ${arms.length}`);
