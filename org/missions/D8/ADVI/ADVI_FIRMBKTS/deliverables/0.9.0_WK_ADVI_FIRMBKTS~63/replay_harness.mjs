/*
 * ADVI_FIRMBKTS FB-h-3 -- offline replay of the auth-validator-edge .004c decision on the
 * legacy and the canonical ownership map.
 *
 * Usage: bun run replay_harness.mjs --legacy <file> --canonical <file>
 *
 * Drives the REAL handler (infra/aws/lambda-edge/auth-validator-edge/index.mjs) of the worktree
 * this file lives in. Stubbed at module level, before the handler is imported:
 *   - @aws-sdk/client-s3          : records every GetObject, serves the map file of the run.
 *   - @aws-sdk/client-secrets-manager : refuses (belt); the render key cache is also seeded so
 *                                   the render branch never reaches Secrets Manager.
 *   - lambda/lib/authkeys/jwtPublicKeys.mjs : the JWT key slots are a key this harness generates.
 * No AWS call is made. No production key, secret or token is read or printed. Map files are read
 * from the paths given on the command line and are never copied into the tree. The result file
 * carries no client, advisor or account identifier.
 */
import { mock } from "bun:test";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
import crypto from "node:crypto";
import { createRequire } from "node:module";

const HERE = import.meta.dir;
const ROOT = path.resolve(HERE, "../../../../../../..");
const HANDLER_REL = "infra/aws/lambda-edge/auth-validator-edge/index.mjs";
const VDIR = path.join(ROOT, "infra/aws/lambda-edge/auth-validator-edge");
const AUTHKEYS = path.join(ROOT, "infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs");
const RENDER = path.join(VDIR, "render_auth.mjs");
const OUT = path.join(HERE, "REPLAY_RESULT.json");
const SAMPLE = 2000;
const SEED = 63;
const FIRM = "49financial";
const TTL_STEP_MS = 120000; // larger than the handler's 60 s ownership-map cache TTL
const ABSENT_ADVISOR = "absent-advisor-r5-fb-h3";

function arg(name) {
  const i = process.argv.indexOf(name);
  if (i < 0 || !process.argv[i + 1]) throw new Error("missing argument " + name);
  return process.argv[i + 1];
}
const LEGACY_FILE = arg("--legacy");
const CANON_FILE = arg("--canonical");
if (!fs.existsSync(path.join(ROOT, HANDLER_REL))) throw new Error("handler not found at " + HANDLER_REL);

const requireFromVdir = createRequire(path.join(VDIR, "package.json"));
const jwt = requireFromVdir("jsonwebtoken");

// ---- stubs, installed before the handler is imported ------------------------------------------
const state = { body: "", gets: [], smCalls: 0 };
class StubGetObjectCommand {
  constructor(input) { this.input = input; }
}
class StubS3Client {
  async send(cmd) {
    state.gets.push({ Bucket: cmd.input.Bucket, Key: cmd.input.Key });
    const body = state.body;
    return { Body: { transformToString: async () => body } };
  }
}
class StubSecretsClient {
  async send() {
    state.smCalls++;
    throw new Error("harness: no Secrets Manager read in the offline replay");
  }
}
const S3_ABS = Bun.resolveSync("@aws-sdk/client-s3", VDIR);
const SM_ABS = Bun.resolveSync("@aws-sdk/client-secrets-manager", VDIR);
mock.module(S3_ABS, () => ({ S3Client: StubS3Client, GetObjectCommand: StubGetObjectCommand }));
mock.module(SM_ABS, () => ({ SecretsManagerClient: StubSecretsClient, GetSecretValueCommand: StubGetObjectCommand }));

const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 2048,
  publicKeyEncoding: { type: "spki", format: "pem" },
  privateKeyEncoding: { type: "pkcs8", format: "pem" },
});
const SLOTS = { current: publicKey, previous: null };
mock.module(AUTHKEYS, () => ({
  parseKeySlots: (s) => ({ current: s, previous: null }),
  getJwtKeySlots: async () => SLOTS,
  // Same contract as the real verifyWithSlots: the handler's own options pass through unchanged.
  verifyWithSlots: (jwtLib, token, slots, verifyOptions) => jwtLib.verify(token, slots.current, verifyOptions),
}));

const s3Check = await import(pathToFileURL(S3_ABS).href);
if (s3Check.S3Client !== StubS3Client) throw new Error("S3 stub not bound to the handler's import");
const renderMod = await import(pathToFileURL(RENDER).href);
const { handler } = await import(pathToFileURL(path.join(VDIR, "index.mjs")).href);

// ---- clock: the handler's ownership-map cache expires on Date.now(); step past it per run -----
const realNow = Date.now;
let offsetMs = 0;
Date.now = () => realNow.call(Date) + offsetMs;

function sign(claims) {
  return jwt.sign(claims, privateKey, { algorithm: "RS256", expiresIn: "2h" });
}
function uriFor(type, id) {
  return type === "account"
    ? `/api/scoped/advisor-intelligence/platinum/accounts/${id}/summary.json`
    : `/api/scoped/partners/books/relationship/${id}/summary`;
}

async function decide(req) {
  // Seed the render key cache (no Secrets Manager call); a human token fails the render audience
  // check and falls through to the human path, exactly as the handler's own comment describes.
  renderMod.__setRenderKeySlotsForTest({ current: publicKey, previous: null });
  const claims = req.kind === "admin"
    ? { sub: "replay-admin", role: "admin", firmRole: "user", firmId: FIRM }
    : { sub: "replay-user", role: "user", firmRole: "user", firmId: FIRM, advisorId: req.requester };
  const token = sign(claims);
  const ev = {
    Records: [{ cf: { request: {
      uri: uriFor(req.type, req.id), method: "GET",
      headers: { authorization: [{ key: "Authorization", value: "Bearer " + token }] },
    } } }],
  };
  const logs = [];
  const saved = { log: console.log, warn: console.warn, error: console.error, info: console.info };
  for (const k of Object.keys(saved)) console[k] = (...a) => logs.push(a.map(String).join(" "));
  let res;
  try {
    res = await handler(ev);
  } finally {
    Object.assign(console, saved);
  }
  let event = "";
  for (const line of logs) {
    if (line.startsWith("{")) {
      try { const o = JSON.parse(line); if (o.event) event = o.event; } catch { /* not a log event */ }
    }
  }
  const status = res && res.status ? String(res.status) : "pass";
  if (status === "pass" && !event) event = "auth_ok";
  return `${status}:${event || "none"}`;
}

async function runMap(text, requests) {
  state.body = text;
  state.gets = [];
  const decisions = [];
  for (const req of requests) {
    const before = state.gets.length;
    decisions.push(await decide(req));
    if (req.kind === "admin" && state.gets.length !== before) throw new Error("admin request read S3");
  }
  return { decisions, gets: state.gets.slice() };
}

function histogram(list) {
  const h = {};
  for (const d of list) h[d] = (h[d] || 0) + 1;
  return h;
}

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---- build the request set from the LEGACY map ------------------------------------------------
const legacyBuf = fs.readFileSync(LEGACY_FILE);
const canonBuf = fs.readFileSync(CANON_FILE);
const legacyText = legacyBuf.toString("utf8");
const canonText = canonBuf.toString("utf8");
const legacy = JSON.parse(legacyText);
const canonObj = JSON.parse(canonText);
const legacyAdvisorIds = Object.keys(legacy.advisors).sort();
if (legacyAdvisorIds.includes(ABSENT_ADVISOR)) throw new Error("absent advisor id is in the map");

const owned = new Map();
const allPairs = [];
for (const a of legacyAdvisorIds) {
  const e = legacy.advisors[a] || {};
  const acc = Array.isArray(e.accounts) ? e.accounts : [];
  const rel = Array.isArray(e.relationships) ? e.relationships : [];
  owned.set(a, { account: new Set(acc), relationship: new Set(rel) });
  for (const id of acc) allPairs.push({ type: "account", id, advisor: a });
  for (const id of rel) allPairs.push({ type: "relationship", id, advisor: a });
}

// Control target: the first account of the first advisor of the CANONICAL map (removed in memory later).
const canonFirstAdvisor = Object.keys(canonObj.advisors)[0];
const canonFirstAccounts = canonObj.advisors[canonFirstAdvisor].accounts;
if (!Array.isArray(canonFirstAccounts) || canonFirstAccounts.length === 0) throw new Error("first advisor has no account");
const ctrl = { type: "account", id: canonFirstAccounts[0], advisor: canonFirstAdvisor };
if (!owned.get(ctrl.advisor) || !owned.get(ctrl.advisor).account.has(ctrl.id)) {
  throw new Error("control target is not owned in the legacy map");
}

const rnd = mulberry32(SEED);
const shuffled = allPairs.slice();
for (let i = shuffled.length - 1; i > 0; i--) {
  const j = Math.floor(rnd() * (i + 1));
  [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
}
let sample = shuffled.slice(0, SAMPLE);
if (!sample.some((p) => p.type === ctrl.type && p.id === ctrl.id && p.advisor === ctrl.advisor)) {
  sample = [ctrl, ...sample.slice(0, SAMPLE - 1)];
}

const requests = sample.map((p) => ({ type: p.type, id: p.id, requester: p.advisor, kind: "user" }));

// For each sampled advisor: one id of the same type owned by ANOTHER advisor (expected deny).
const sampledAdvisors = [...new Set(sample.map((p) => p.advisor))];
for (const a of sampledAdvisors) {
  let found = null;
  for (let t = 0; t < 100000 && !found; t++) {
    const p = allPairs[Math.floor(rnd() * allPairs.length)];
    if (p.advisor === a) continue;
    if (owned.get(a)[p.type].has(p.id)) continue;
    found = p;
  }
  if (!found) throw new Error("no cross-owned id found");
  requests.push({ type: found.type, id: found.id, requester: a, kind: "user" });
}
// One advisor id absent from the map.
requests.push({ type: ctrl.type, id: ctrl.id, requester: ABSENT_ADVISOR, kind: "user" });
// One admin token (expected bypass, no S3 read).
requests.push({ type: ctrl.type, id: ctrl.id, requester: null, kind: "admin" });

for (const r of requests) {
  if (!/^[A-Za-z0-9_-]+$/.test(String(r.id))) throw new Error("id outside the path-safe alphabet");
}

const accountsN = requests.filter((r) => r.type === "account").length;
const relationshipsN = requests.filter((r) => r.type === "relationship").length;
if (accountsN < 1 || relationshipsN < 1) throw new Error("both path types must be replayed");

// ---- the three runs ---------------------------------------------------------------------------
offsetMs = 0;
const legacyRun = await runMap(legacyText, requests);

offsetMs += TTL_STEP_MS;
const canonRun = await runMap(canonText, requests);
if (canonRun.gets.length < 1) throw new Error("canonical run made no ownership-map read");
const canonKeys = new Set(canonRun.gets.map((g) => g.Bucket + "\u0000" + g.Key));
if (canonKeys.size !== 1) throw new Error("canonical run requested more than one Bucket/Key");
const reqBucket = canonRun.gets[0].Bucket;
const reqKey = canonRun.gets[0].Key;

const controlObj = JSON.parse(canonText);
const removed = controlObj.advisors[ctrl.advisor].accounts.shift();
if (removed !== ctrl.id) throw new Error("control removal did not remove the control target");
offsetMs += TTL_STEP_MS;
const controlRun = await runMap(JSON.stringify(controlObj), requests);
if (controlRun.gets.length < 1) throw new Error("control run made no ownership-map read");

let mismatches = 0;
let controlMismatches = 0;
const pairSeen = {};
for (let i = 0; i < requests.length; i++) {
  if (legacyRun.decisions[i] !== canonRun.decisions[i]) {
    mismatches++;
    const k = legacyRun.decisions[i] + " -> " + canonRun.decisions[i];
    pairSeen[k] = (pairSeen[k] || 0) + 1;
  }
  if (legacyRun.decisions[i] !== controlRun.decisions[i]) controlMismatches++;
}
if (Object.keys(pairSeen).length) console.error("MISMATCH decision pairs (count): " + JSON.stringify(pairSeen));

const legacySha = crypto.createHash("sha256").update(legacyBuf).digest("hex");
const canonSha = crypto.createHash("sha256").update(canonBuf).digest("hex");

const result = {
  handler: HANDLER_REL,
  canonical_request_bucket: reqBucket,
  canonical_request_key: reqKey,
  legacy_sha256: legacySha,
  canonical_sha256: canonSha,
  bytes_equal: legacySha === canonSha,
  pairs: requests.length,
  mismatches,
  control_mismatches: controlMismatches,
  accounts: accountsN,
  relationships: relationshipsN,
  advisors: legacyAdvisorIds.length,
  decisions: histogram(canonRun.decisions),
};
fs.writeFileSync(OUT, JSON.stringify(result, null, 2) + "\n");
console.log(`REPLAY pairs=${requests.length} mismatches=${mismatches} control_mismatches=${controlMismatches} accounts=${accountsN} relationships=${relationshipsN}`);
