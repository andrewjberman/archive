#!/usr/bin/env node
/**
 * SERVED_TIER_BODIES_B3 -- POSN_AGGFIX.TO-B3-1, criterion B3-AC6 (AMENDMENT 1, issuer, at the partial
 * drain 6ff556ed39). Lives in THIS worker's deliverables because no worker edits another's file: the
 * reading below is one c1_live_tier_arms.mjs does not produce (its only current_holdings.AGG predicate
 * is scoped to the aggregate URLs and is never applied to the control URL -- row POSN_AGGFIX-Z-W3-S5).
 *
 * WHAT IT MEASURES -- what a session OUTSIDE Opal actually RECEIVES, on the live distribution:
 *   - advisor class and client class on /api/general/positioning/positioning_data.json: 200, and the
 *     PARSED body carries no current_holdings.AGG (the current_holdings key set is printed per row);
 *   - the same two classes on BOTH aggregate URL forms: 401;
 *   - Opal staff and Dev on /api/general/positioning/opal_aggregate.json: 200 with body status OK;
 *   - POSITIVE CONTROL: the SAME parsed check, run against TO-A3-1's PRIOR shared-file version fetched
 *     BY VERSIONID (b3_ac6_prior_fetch.py), must report AGG PRESENT. Without it an AGG-absence check
 *     that can only ever say ABSENT is indistinguishable from one that works.
 *
 * ONE DEFINITION OF THE CLASSES: the four viewer classes and the URL forms are IMPORTED from TO-C1-1's
 * c1_classes.mjs (read, never edited), so these rows and C1's live rows are driven by the same claim
 * shapes; the module's path and sha256 are printed.
 *
 * SECRETS (this order's rule, identical to the one c1_live_tier_arms.mjs applies): the ONLY secret read
 * is opal/auth/jwt-private-key, through `comp-secrets get opal/auth/jwt-private-key --reveal`, captured
 * from the child's stdout INSIDE this process -- the process that signs. The key and every token are
 * never printed, never written to a file, never placed in argv and never committed; argv carries the
 * secret's NAME only. Tokens: RS256, no keyid, exp = iat + 300, sub = qa-posn-aggfix-<class>. If the key
 * cannot be read that way, the token arms are REFUSED (exit 3).
 *
 * Read-only toward the cloud: HTTPS GETs and read-only S3 reads by VersionId. Nothing deploys or serves.
 */
import { spawnSync } from "node:child_process";
import { createHash, createPrivateKey, createPublicKey, sign, verify } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { AGG_URLS, CLASS_ORDER, CONTROL_URL, claimsFor } from "../0.9.0_WK_POSN_AGGFIX~2/c1_classes.mjs";

const BASE = "https://opalinvest.dev";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const CLASSES_MODULE = path.join(HERE, "..", "0.9.0_WK_POSN_AGGFIX~2", "c1_classes.mjs");
const PRIOR_FETCH = path.join(HERE, "b3_ac6_prior_fetch.py");
const OUTSIDE = ["advisor", "client"];
const ADMITTED = ["opal", "dev"];

// ---- key read (in-process) and minting ----------------------------------------------------------
function readSigningKey() {
  const r = spawnSync("bash", ["-c", "comp-secrets get opal/auth/jwt-private-key --reveal"],
    { encoding: "utf8", maxBuffer: 1 << 20, timeout: 60000 });
  const raw = r.stdout || "";
  let pem = null;
  const t = raw.trim();
  if (t.startsWith("{")) {
    try {
      const j = JSON.parse(t);
      pem = typeof j.current === "string" ? j.current : null;
    } catch {
      pem = null;
    }
  }
  if (!pem) {
    const m = raw.match(/-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----/);
    pem = m ? m[0] : null;
  }
  if (r.status !== 0 || !pem) {
    console.log(`KEY READ: REFUSED -- comp-secrets rc=${r.status}, PEM block found=${Boolean(pem)} (value not printed)`);
    process.exit(3);
  }
  const key = createPrivateKey(pem);
  const probe = Buffer.from("b3-ac6-self-check");
  const ok = verify("RSA-SHA256", probe, createPublicKey(key), sign("RSA-SHA256", probe, key));
  const bits = key.asymmetricKeyDetails ? key.asymmetricKeyDetails.modulusLength : "?";
  console.log(`KEY READ: comp-secrets get opal/auth/jwt-private-key --reveal rc=0; shape=${t.startsWith("{") ? "envelope.current" : "PEM"}; ` +
    `type=${key.asymmetricKeyType}; modulus=${bits} bits; sign/verify self-check=${ok ? "OK" : "FAILED"}; value REDACTED`);
  if (!ok) process.exit(3);
  return key;
}

const b64u = (buf) => Buffer.from(buf).toString("base64").replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_");
function mint(key, claims) {
  const head = b64u(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const body = b64u(JSON.stringify(claims));
  return `${head}.${body}.${b64u(sign("RSA-SHA256", Buffer.from(`${head}.${body}`), key))}`;
}

// ---- HTTP ---------------------------------------------------------------------------------------
async function get(url, token) {
  const headers = { "user-agent": "qa-posn-aggfix-b3/1" };
  if (token) headers.authorization = `Bearer ${token}`;
  const res = await fetch(BASE + url, { headers, redirect: "manual" });
  const buf = Buffer.from(await res.arrayBuffer());
  return { status: res.status, len: buf.length, sha: createHash("sha256").update(buf).digest("hex"), buf };
}

// ---- THE ONE PARSED CHECK, used on the served bodies AND on the prior version --------------------
function aggReading(buf) {
  let doc;
  try {
    doc = JSON.parse(buf.toString("utf8"));
  } catch (e) {
    return { parsed: false, keys: null, agg: null, status: null, note: `not JSON: ${String(e.message).slice(0, 60)}` };
  }
  if (!doc || typeof doc !== "object" || Array.isArray(doc)) {
    return { parsed: true, keys: null, agg: null, status: null, note: "JSON but not an object" };
  }
  const ch = doc.current_holdings;
  const isObj = ch && typeof ch === "object" && !Array.isArray(ch);
  const keys = isObj ? Object.keys(ch) : null;
  return {
    parsed: true,
    keys,
    agg: isObj ? Object.prototype.hasOwnProperty.call(ch, "AGG") : null,
    status: typeof doc.status === "string" ? doc.status : null,
    note: isObj ? "" : "no current_holdings object",
  };
}

const fmtKeys = (rd) => (rd.keys ? `[${rd.keys.join(" ")}]` : `(none: ${rd.note})`);
const fmtAgg = (rd) => (rd.agg === null ? "n/a" : rd.agg ? "PRESENT" : "ABSENT");

// ---- run ------------------------------------------------------------------------------------------
const modSha = createHash("sha256").update(readFileSync(CLASSES_MODULE)).digest("hex");
console.log(`SERVED_TIER_BODIES_B3 -- B3-AC6 (AMENDMENT 1) at ${new Date().toISOString()} against ${BASE}`);
const REPO_ROOT = spawnSync("git", ["rev-parse", "--show-toplevel"], { cwd: HERE, encoding: "utf8" }).stdout.trim();
console.log(`CLASS DEFINITIONS imported from ${path.relative(REPO_ROOT, CLASSES_MODULE).replace(/\\/g, "/")} sha256=${modSha.slice(0, 16)} (read, never edited)`);

const key = readSigningKey();
const iat = Math.floor(Date.now() / 1000);
const tokens = {};
console.log(`TOKENS iat=${iat} exp=${iat + 300} (lifetime 300 s, the order's bound)`);
for (const cls of CLASS_ORDER) {
  const c = claimsFor(cls, iat);
  tokens[cls] = mint(key, c);
  console.log(`  CLAIMS ${cls}: ${JSON.stringify(c)} (token REDACTED)`);
}

let n = 0;
const table = [];
function row(who, url, r, rd, expectText, ok) {
  n += 1;
  table.push(ok);
  console.log(`  ${String(n).padStart(2)} ${ok ? "MATCH   " : "MISMATCH"} ${who.padEnd(8)} ${url.padEnd(50)} ${String(r.status).padEnd(4)} ` +
    `len=${String(r.len).padEnd(7)} sha256=${r.sha.slice(0, 16)} body.status=${String(rd.status).padEnd(5)} ` +
    `current_holdings=${fmtKeys(rd)} AGG=${fmtAgg(rd)}   [expect ${expectText}]`);
}

console.log("");
console.log("B3-AC6 -- one row per (class, URL): what the session RECEIVES, parsed");
// 1. the two classes outside Opal, on the control URL: 200 and no current_holdings.AGG
for (const cls of OUTSIDE) {
  const r = await get(CONTROL_URL, tokens[cls]);
  const rd = aggReading(r.buf);
  row(cls, CONTROL_URL, r, rd, "200 and current_holdings WITHOUT AGG", r.status === 200 && rd.parsed && rd.agg === false);
}
// 2. the same two classes, on BOTH aggregate URL forms: 401
for (const cls of OUTSIDE) {
  for (const url of AGG_URLS) {
    const r = await get(url, tokens[cls]);
    const rd = aggReading(r.buf);
    row(cls, url, r, rd, "401", r.status === 401);
  }
}
// 3. Opal staff and Dev, on the aggregate: 200 with body status OK
for (const cls of ADMITTED) {
  const r = await get(AGG_URLS[0], tokens[cls]);
  const rd = aggReading(r.buf);
  row(cls, AGG_URLS[0], r, rd, "200 with body status OK", r.status === 200 && rd.status === "OK");
}

// ---- THE POSITIVE CONTROL -------------------------------------------------------------------------
console.log("");
console.log("POSITIVE CONTROL -- the SAME parsed check against TO-A3-1's PRIOR shared-file version, by VersionId");
let pf = spawnSync("python", [PRIOR_FETCH], { encoding: "utf8", maxBuffer: 1 << 24, timeout: 300000 });
let how = "python <script>";
if (pf.status !== 0 || !(pf.stdout || "").includes("PRIOR_FETCH_JSON ")) {
  const posix = PRIOR_FETCH.replace(/^([A-Za-z]):/, (m, d) => `/${d.toLowerCase()}`).replace(/\\/g, "/");
  console.log(`  direct spawn rc=${pf.status}; retrying through bash`);
  pf = spawnSync("bash", ["-c", `python "${posix}"`], { encoding: "utf8", maxBuffer: 1 << 24, timeout: 300000 });
  how = "bash -c python <script>";
}
for (const ln of (pf.stdout || "").split("\n")) {
  if (ln.trim() && !ln.startsWith("PRIOR_FETCH_JSON ")) console.log(`  ${ln.trimEnd()}`);
}
const jsonLine = (pf.stdout || "").split("\n").find((l) => l.startsWith("PRIOR_FETCH_JSON "));
let controlFires = false;
if (!jsonLine) {
  console.log(`  PRIOR FETCH FAILED (${how}) rc=${pf.status}; stderr tail: ${(pf.stderr || "").trim().split("\n").pop()}`);
} else {
  const meta = JSON.parse(jsonLine.slice("PRIOR_FETCH_JSON ".length));
  const raw = readFileSync(meta.path);
  const rd = aggReading(raw);
  const shaOk = createHash("sha256").update(raw).digest("hex") === meta.decompressed_sha256;
  console.log(`  fetched ${meta.key} @VersionId ${meta.version_id} (from ${meta.source_instance_commit}, loci agree ${meta.loci_agree})`);
  console.log(`  LastModified ${meta.last_modified}  ContentLength ${meta.content_length}  ContentEncoding ${meta.content_encoding}  ` +
    `stored md5 ${meta.stored_md5}  decompressed ${meta.decompressed_bytes} bytes sha256=${meta.decompressed_sha256.slice(0, 16)} (read back equal: ${shaOk})`);
  console.log(`  PARSED by the SAME aggReading(): current_holdings=${fmtKeys(rd)} AGG=${fmtAgg(rd)} body.status=${rd.status}`);
  controlFires = rd.parsed && rd.agg === true && shaOk;
  console.log(`  CONTROL: the AGG check reports ${fmtAgg(rd)} on the prior version -- ${controlFires ? "FIRED-AS-EXPECTED (the check can fail)" : "DID NOT FIRE"}`);
}

const matched = table.filter(Boolean).length;
console.log("");
console.log(`TABLE ROWS ${table.length}; MATCH ${matched} of ${table.length}`);
console.log(`POSITIVE CONTROL AGG PRESENT ON THE PRIOR VERSION: ${controlFires ? "TRUE" : "FALSE"}`);
process.exit(matched === table.length && controlFires ? 0 : 1);
