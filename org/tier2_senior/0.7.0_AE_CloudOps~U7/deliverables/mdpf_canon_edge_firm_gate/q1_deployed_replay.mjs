#!/usr/bin/env node
/**
 * q1_deployed_replay.mjs -- L5d of ADHOC.canon-q1-edge-firm-gate-deploy (0.7.0_AE_CloudOps~U7; ASCII only).
 *
 * Replays the issuer's q1_harness.mjs handler arms A1-A12 and A14 (rows copied verbatim) against the DEPLOYED BUNDLE of the
 * published version (index.mjs unzipped from get-function --qualifier N), with the REAL jsonwebtoken verify inlined in that
 * bundle. Only @aws-sdk/client-secrets-manager and @aws-sdk/client-s3 are stubbed by a node:module resolve hook: the fake
 * Secrets Manager returns the PEM public half of a throwaway RSA key (generated in memory, never written) for SecretId
 * opal/auth/jwt-public-key and throws for any other id; the fake S3 throws if touched. Tokens are signed RS256 with the
 * matching private key. EXTRA control rows: a token signed by a DIFFERENT throwaway key must read 401 (proves the real verify
 * runs), and an expired token must read 401.
 *
 *   node q1_deployed_replay.mjs <dir holding the unzipped index.mjs>
 * Prints ARM lines as the harness does and "TOTAL <passed> of <arms>". Exit 0 always; exit 2 on a load error.
 * LIMIT: this proves the DEPLOYED BYTES answer the matrix; a live 403 for a real partner login is not provable (none exists).
 */
import { registerHooks } from "node:module";
import crypto from "node:crypto";
import path from "node:path";
import { pathToFileURL } from "node:url";

const DIR = path.resolve(process.argv[2]);
const INDEX_URL = pathToFileURL(path.join(DIR, "index.mjs")).href;
const KEYS = {
  good: crypto.generateKeyPairSync("rsa", { modulusLength: 2048 }),
  other: crypto.generateKeyPairSync("rsa", { modulusLength: 2048 }),
};
const PEM = KEYS.good.publicKey.export({ type: "spki", format: "pem" });
const data = (s) => "data:text/javascript," + encodeURIComponent(s);
globalThis.__PEM__ = PEM;
globalThis.__SM_CALLS__ = [];
const STUB_S3 = data("export class S3Client { send() { throw new Error('replay: no S3'); } }\n" +
  "export class GetObjectCommand { constructor(i) { this.input = i; } }");
const STUB_SM = data("export class SecretsManagerClient { async send(c) { globalThis.__SM_CALLS__.push(c.input.SecretId); " +
  "if (c.input.SecretId === 'opal/auth/jwt-public-key') return { SecretString: globalThis.__PEM__ }; throw new Error('replay: no such secret'); } }\n" +
  "export class GetSecretValueCommand { constructor(i) { this.input = i; } }");
registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier === "@aws-sdk/client-s3") return { url: STUB_S3, shortCircuit: true };
    if (specifier === "@aws-sdk/client-secrets-manager") return { url: STUB_SM, shortCircuit: true };
    return nextResolve(specifier, context);
  },
});

const captured = [];
for (const lvl of ["log", "warn", "error"]) {
  console[lvl] = (...a) => { captured.push({ lvl, msg: a.join(" ") }); };
}
const out = (s) => process.stdout.write(s + "\n");

let gated;
try {
  gated = (await import(INDEX_URL)).handler;
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
const b64u = (b) => Buffer.from(b).toString("base64url");
function signRS256(claims, key) {
  const head = b64u(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const pay = b64u(JSON.stringify({ ...claims, iat: Math.floor(Date.now() / 1000) - 5, exp: Math.floor(Date.now() / 1000) + 600 }));
  const sig = crypto.sign("RSA-SHA256", Buffer.from(head + "." + pay), key).toString("base64url");
  return head + "." + pay + "." + sig;
}
function tokenFor(claims) { seq += 1; return signRS256({ ...claims, jti: "q1-replay-" + seq }, KEYS.good.privateKey); }
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

// ---- extra controls: the real verify is running ----
async function extraControls() {
  const rows = [];
  const bad = signRS256({ sub: "x@opal.test", firmId: "opal-capital", userType: "Dev", jti: "wrongkey" }, KEYS.other.privateKey);
  let r = await gated(eventFor(`${P}inflection/aum-metrics.json`, "", bad));
  rows.push({ name: "internal claim signed by a DIFFERENT key", expect: "401", got: String(r.status), ok: String(r.status) === "401" });
  const head = b64u(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const pay = b64u(JSON.stringify({ sub: "x", firmId: "opal-capital", iat: 1, exp: 2 }));
  const exp = head + "." + pay + "." + crypto.sign("RSA-SHA256", Buffer.from(head + "." + pay), KEYS.good.privateKey).toString("base64url");
  r = await gated(eventFor(`${P}inflection/aum-metrics.json`, "", exp));
  rows.push({ name: "validly signed but expired internal token", expect: "401", got: String(r.status), ok: String(r.status) === "401" });
  const none = head.replace(/./, "e") && b64u(JSON.stringify({ alg: "none", typ: "JWT" })) + "." + b64u(JSON.stringify({ sub: "x", firmId: "opal-capital" })) + ".";
  r = await gated(eventFor(`${P}inflection/aum-metrics.json`, "", none));
  rows.push({ name: "alg none token claiming opal-capital", expect: "401", got: String(r.status), ok: String(r.status) === "401" });
  rows.push({ name: "secret ids requested (only opal/auth/jwt-public-key and at most the render key lookup)", expect: "jwt key read", got: [...new Set(globalThis.__SM_CALLS__)].join(","), ok: globalThis.__SM_CALLS__.includes("opal/auth/jwt-public-key") });
  arm("X1", "real verify runs in the deployed bundle: wrong key, expired, alg none all 401; the fake Secrets Manager was asked for the JWT key (control)", rows);
}

await handlerMode();
await extraControls();
out(`TOTAL ${arms.filter((a) => a.ok).length} of ${arms.length}`);
