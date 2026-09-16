#!/usr/bin/env node
/**
 * LIVE_TIER_ARMS_C1 -- POSN_AGGFIX.TO-C1-1, criteria C1-AC3 (--phase pre), C1-AC17 (--phase families-before)
 * and C1-AC13 (--phase post). Live GETs against https://opalinvest.dev (distribution EVTSA9VEHNZVH).
 *
 * SECRETS: the ONLY secret read is opal/auth/jwt-private-key, through `comp-secrets get
 * opal/auth/jwt-private-key --reveal`, captured from the child's stdout INSIDE this process (the process
 * that signs). The key and every token are never printed, written to a file or placed in argv; the argv
 * carries the secret's NAME only. Tokens: RS256, no keyid (the signer sets none), exp = iat + 300,
 * sub = qa-posn-aggfix-<class>. If the key cannot be read that way the token arms are REFUSED (exit 3).
 *
 * Bodies of partner-scoped families are never printed: status, length and sha256 only.
 */
import { spawnSync } from "node:child_process";
import { createHash, createPrivateKey, createPublicKey, sign, verify } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  AGG_URLS, AMENDMENT_URLS, CLASS_ORDER, CONTROL_URL, MODEL_URL, claimsFor,
} from "./c1_classes.mjs";

const BASE = "https://opalinvest.dev";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = spawnSync("git", ["rev-parse", "--show-toplevel"], { cwd: HERE, encoding: "utf8" }).stdout.trim();
const FAMILIES_FILE = path.join(ROOT, ".scratch", "c1_families_before.json");
const GATE_MESSAGE = "Opal-only resource: not authorized for this viewer";
const FAMILIES = [
  { family: "S3-backed /api/scoped/advisor-intelligence/*",
    url: "/api/scoped/advisor-intelligence/artifacts/firm_composition.json?firm=bd" },
  { family: "API-Gateway-backed /v1/*", url: "/v1/metadata/yang" },
  { family: "/api/scoped/satellites/*", url: "/api/scoped/satellites/registry.json?firm=bd" },
];

const phaseIdx = process.argv.indexOf("--phase");
const phase = phaseIdx === -1 ? "" : process.argv[phaseIdx + 1];
if (!["pre", "families-before", "post"].includes(phase)) {
  console.log("usage: node c1_live_tier_arms.mjs --phase pre|families-before|post");
  process.exit(2);
}

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
  const probe = Buffer.from("c1-self-check");
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

// ---- HTTP --------------------------------------------------------------------------------------
const printable = (buf) => buf.subarray(0, 120).toString("latin1").replace(/[^\x20-\x7e]/g, ".");
async function get(url, token) {
  const headers = { "user-agent": "qa-posn-aggfix-c1/1" };
  if (token) headers.authorization = `Bearer ${token}`;
  const res = await fetch(BASE + url, { headers, redirect: "manual" });
  const buf = Buffer.from(await res.arrayBuffer());
  return {
    status: res.status, len: buf.length, sha: createHash("sha256").update(buf).digest("hex"),
    head: printable(buf), ctype: res.headers.get("content-type") || "", buf,
  };
}

function claimLine(cls, claims) {
  return `  CLAIMS ${cls}: ${JSON.stringify(claims)} (token REDACTED)`;
}

function s3Head(key) {
  const r = spawnSync("bash", ["-c", `aws s3api head-object --bucket opal-data-portal-v2 --key ${key} --query "{LastModified:LastModified,Len:ContentLength,VersionId:VersionId}" --output text`],
    { encoding: "utf8", timeout: 60000 });
  return `rc=${r.status} ${(r.stdout || "").trim()} ${(r.stderr || "").trim().split("\n").pop()}`;
}

const key = readSigningKey();
const tokens = {};
const iat = Math.floor(Date.now() / 1000);
console.log(`PHASE ${phase} at ${new Date().toISOString()} against ${BASE}; iat=${iat} exp=${iat + 300}`);
for (const cls of CLASS_ORDER) {
  const c = claimsFor(cls, iat);
  tokens[cls] = mint(key, c);
  console.log(claimLine(cls, c));
}

let failures = 0;
const table = [];
function row(n, who, url, r, expectText, ok) {
  table.push(ok);
  if (!ok) failures += 1;
  console.log(`  ${String(n).padStart(2)} ${ok ? "MATCH   " : "MISMATCH"} ${who.padEnd(8)} ${url.padEnd(56)} ${String(r.status).padEnd(4)} ` +
    `len=${String(r.len).padEnd(8)} sha256=${r.sha.slice(0, 16)} first120="${r.head}"   [expect ${expectText}]`);
}

if (phase === "pre") {
  console.log("");
  console.log("C1-AC3 -- the proxy docstring's 'blocks client tier' on /api/general/positioning/model.json, exercised");
  console.log(`  s3 head-object json/positioning/model.json: ${s3Head("json/positioning/model.json")}`);
  const unauth = await get(MODEL_URL, null);
  row(1, "unauth", MODEL_URL, unauth, "401 (reachability control)", unauth.status === 401);
  const client = await get(MODEL_URL, tokens.client);
  row(2, "client", MODEL_URL, client, "status recorded", true);
  const opal = await get(MODEL_URL, tokens.opal);
  row(3, "opal", MODEL_URL, opal, "status recorded (discriminator: Opal staff on the same URL)", true);
  // A refusal is an answer the EDGE or a function gives. S3's own XML <Error> is the ORIGIN answering, i.e. the
  // request was NOT refused on the way -- a 403 AccessDenied for an absent key is not a tier refusal.
  const originAnswer = (r) => /^<\?xml[^>]*\?>\s*<Error><Code>/.test(r.buf.toString("utf8"));
  const edgeRefusal = (client.status === 401 || client.status === 403) && !originAnswer(client);
  console.log(`  client answer is the S3 origin's own error document: ${originAnswer(client)}; ` +
    `same status and shape as Opal staff's answer: ${client.status === opal.status && originAnswer(client) === originAnswer(opal)}`);
  console.log(`MODEL-ROUTE CLIENT REFUSAL: ${edgeRefusal ? "TRUE" : "FALSE"}`);
  console.log("");
  console.log("SUPPLEMENTARY (pre-gate state, not graded by C1-AC3)");
  console.log(`  s3 head-object ${"json/positioning/opal_aggregate.json"}: ${s3Head("json/positioning/opal_aggregate.json")}`);
  let n = 4;
  for (const cls of ["client", "advisor"]) {
    for (const url of [AGG_URLS[0], CONTROL_URL]) {
      row(n++, cls, url, await get(url, tokens[cls]), "status recorded", true);
    }
  }
  const plain = await get(CONTROL_URL, tokens.client);
  const enc = await get("/api/general/positioning/positioning%5Fdata.json", tokens.client);
  row(n++, "client", "/api/general/positioning/positioning%5Fdata.json", enc, "status recorded", true);
  const same = plain.status === 200 && enc.status === 200 && plain.sha === enc.sha;
  console.log(`  EDGE+ORIGIN RESOLVE %5F TO THE SAME OBJECT AS THE PLAIN CONTROL: ${same ? "TRUE" : "FALSE"} ` +
    `(plain ${plain.status} ${plain.sha.slice(0, 16)}, encoded ${enc.status} ${enc.sha.slice(0, 16)})`);
  process.exit(unauth.status === 401 ? 0 : 1);
}

if (phase === "families-before") {
  console.log("");
  console.log("C1-AC17 -- three behaviour families other than /api/general/*, captured BEFORE the apply (each read twice)");
  const cap = { captured_at: new Date().toISOString(), base: BASE, rows: [] };
  let n = 1;
  for (const cls of ["advisor", "opal"]) {
    for (const f of FAMILIES) {
      const a = await get(f.url, tokens[cls]);
      const b = await get(f.url, tokens[cls]);
      const stable = a.status === b.status && a.sha === b.sha;
      cap.rows.push({ class: cls, family: f.family, url: f.url, status: a.status, len: a.len, sha256: a.sha, stable_across_two_reads: stable });
      row(n++, cls, f.url, a, `captured; second read ${b.status} sha256=${b.sha.slice(0, 16)} stable=${stable}`, true);
      console.log(`       family: ${f.family}; content-type ${a.ctype}`);
    }
  }
  mkdirSync(path.dirname(FAMILIES_FILE), { recursive: true });
  writeFileSync(FAMILIES_FILE, JSON.stringify(cap, null, 2) + "\n");
  const unstable = cap.rows.filter((r) => !r.stable_across_two_reads).length;
  console.log(`  written: ${FAMILIES_FILE}`);
  console.log(`FAMILIES CAPTURED ${cap.rows.length} of 6 (unstable across two reads: ${unstable})`);
  process.exit(cap.rows.length === 6 ? 0 : 1);
}

// ---- post -----------------------------------------------------------------------------------------
console.log("");
console.log("C1-AC13 -- after Deployed: the live refusal, the live allowance, AMENDMENT 1 forms, and the families");
let n = 1;
for (const url of AGG_URLS) {
  const r = await get(url, null);
  row(n++, "unauth", url, r, "401", r.status === 401);
}
const opalAgg = {};
for (const cls of CLASS_ORDER) {
  for (const url of AGG_URLS) {
    const r = await get(url, tokens[cls]);
    if (cls === "advisor" || cls === "client") {
      row(n++, cls, url, r, "401 with the gate's message", r.status === 401 && r.buf.toString("utf8").includes(GATE_MESSAGE));
    } else {
      if (cls === "opal") opalAgg[url] = r;
      row(n++, cls, url, r, "NOT 401", r.status !== 401);
    }
  }
}
for (const cls of CLASS_ORDER) {
  const r = await get(CONTROL_URL, tokens[cls]);
  row(n++, cls, CONTROL_URL, r, "200", r.status === 200);
}
const aggServed = Object.values(opalAgg).some((r) => r.status === 200 && r.ctype.includes("json"));
const aggShas = new Set(Object.values(opalAgg).filter((r) => r.status === 200 && r.ctype.includes("json")).map((r) => r.sha));
console.log(`  aggregate bytes as served to Opal staff: ${aggServed ? "served, sha256 " + [...aggShas].map((s) => s.slice(0, 16)).join(",") : "NOT served (S3 answer for an absent key)"}`);
for (const cls of ["advisor", "client"]) {
  for (const url of AMENDMENT_URLS) {
    const r = await get(url, tokens[cls]);
    const looksAgg = aggShas.has(r.sha) || (r.status === 200 && /"current_holdings"\s*:\s*\{\s*"AGG"/.test(r.buf.toString("utf8")));
    row(n++, cls, url, r, "401, or a body that is not the aggregate's bytes", r.status === 401 || !looksAgg);
  }
}
if (!existsSync(FAMILIES_FILE)) {
  console.log(`  FAMILIES: ${FAMILIES_FILE} ABSENT -- C1-AC17 was not captured`);
  failures += 1;
} else {
  const before = JSON.parse(readFileSync(FAMILIES_FILE, "utf8"));
  console.log(`  families captured before at ${before.captured_at}`);
  let unmoved = 0;
  for (const b of before.rows) {
    const r = await get(b.url, tokens[b.class]);
    const eq = r.status === b.status && r.sha === b.sha256;
    if (eq) unmoved += 1;
    row(n++, b.class, b.url, r, `status ${b.status} and sha256 ${b.sha256.slice(0, 16)} as captured before`, eq);
  }
  console.log(`FAMILIES UNMOVED ${unmoved} of ${before.rows.length}`);
}
console.log(`TABLE ROWS ${table.length}; MATCH ${table.filter(Boolean).length} of ${table.length}`);
process.exit(failures === 0 ? 0 : 1);
