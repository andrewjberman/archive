// IRPT_BCKEND.TO-IB-rtr-2 -- BOTH VERIFIERS, THE FORBIDDEN CLAIMS + THE EXPIRY BOUND.
// Criterion R118-AC2. Invocation (task order, verbatim):
//   cd deliverables/0.9.0_WK_IRPT_BCKEND~18 && node --test test_v2_v3_forbidden_claims_and_expiry.mjs
// Run from org/missions/D9/IRPT/IRPT_BCKEND/ (the task order's own directory), matching
// the convention set by the round-15/16 sibling cells' result.md files.
//
// Exercises the REAL `infra/aws/users/lambda/portal-authorizer/index.mjs` (V2) and the
// REAL `infra/aws/lambda-edge/auth-validator-edge/index.mjs` + `render_auth.mjs` (V3)
// against fixture RSA keypairs and synthetic events. No AWS call is ever reached:
//   - V3's render-key path uses `render_auth.mjs`'s own `__setRenderKeySlotsForTest` seam
//     (mirrors round-16's `test_edge_render_delegate.mjs`).
//   - V2's render-key path uses its own `IRPT_RENDER_JWT_PUBLIC_KEY_PEM` env-var fixture
//     injection point (mirrors round-15's `test_edge_render_delegate_v2_authorizer.mjs`).
//   - Both verifiers' HUMAN paths read the shared `infra/aws/lambda/lib/authkeys/
//     jwtPublicKeys.mjs` module, which itself has no `node_modules` anywhere in its own
//     directory ancestry in a fresh worktree (measured: `import('@aws-sdk/client-
//     secrets-manager')` from that module's own location fails ERR_MODULE_NOT_FOUND
//     until intercepted) -- so, unlike round-15's approach of monkeypatching
//     `SecretsManagerClient.prototype.send` post-import (which requires the bare import
//     to resolve to SOMETHING first), this file uses `node:module`'s `registerHooks` to
//     intercept the specifier PROCESS-WIDE regardless of which file requests it, the
//     same mechanism round-16 used for the same reason. See row IRPT_BCKEND-W18-S1.
//
// `jsonwebtoken` itself is loaded by relative path from `auth-validator-edge`'s own
// `node_modules` (this test file's own directory has no node_modules ancestry) --
// the SAME install `index.mjs` itself bare-imports (bare specifiers resolve from the
// IMPORTING FILE's own location, never the test file's).

import { test, before } from "node:test";
import assert from "node:assert/strict";
import { registerHooks } from "node:module";
import crypto from "node:crypto";

// ---------------------------------------------------------------------------
// Fixture keypairs -- throwaway, generated fresh every run (BOUNDS: never
// IB-rtq-1's real minter, never a live secret).
// ---------------------------------------------------------------------------
function genKeyPair() {
  return crypto.generateKeyPairSync("rsa", {
    modulusLength: 2048,
    publicKeyEncoding: { type: "spki", format: "pem" },
    privateKeyEncoding: { type: "pkcs8", format: "pem" },
  });
}

const renderKeys = genKeyPair(); // shared render-token signer for BOTH verifiers' tests
const humanKeys = genKeyPair();  // the ONE shared human key both verifiers' getJwtKeySlots() reads
const ORIGIN_SECRET_VALUE = "test-cloudfront-origin-secret-value";

process.env.IRPT_RENDER_JWT_PUBLIC_KEY_PEM = renderKeys.publicKey; // V2's own fixture seam

// ---------------------------------------------------------------------------
// Intercept @aws-sdk/client-secrets-manager PROCESS-WIDE (row IRPT_BCKEND-W18-S1
// above) so the shared jwtPublicKeys.mjs (human path, both verifiers) and
// originVerify.mjs (V2's origin gate) resolve fixtures instead of a live secret.
// The render-key paths never reach this: V3 seeds via __setRenderKeySlotsForTest,
// V2 via its own env var.
// ---------------------------------------------------------------------------
const JWT_PUBLIC_KEY_SECRET_ID = "opal/auth/jwt-public-key";
const ORIGIN_VERIFY_SECRET_ID = "opal/auth/origin-verify";
const FAKE_SM_SRC = `
export class SecretsManagerClient {
  constructor() {}
  async send(cmd) {
    const id = cmd && cmd.input && cmd.input.SecretId;
    if (id === ${JSON.stringify(JWT_PUBLIC_KEY_SECRET_ID)}) {
      return { SecretString: ${JSON.stringify(humanKeys.publicKey)} };
    }
    if (id === ${JSON.stringify(ORIGIN_VERIFY_SECRET_ID)}) {
      return { SecretString: JSON.stringify({ current: ${JSON.stringify(ORIGIN_SECRET_VALUE)}, previous: null }) };
    }
    throw new Error("test fake SecretsManagerClient: unexpected SecretId " + id);
  }
}
export class GetSecretValueCommand {
  constructor(input) { this.input = input; }
}
`;
const FAKE_SM_URL = "data:text/javascript," + encodeURIComponent(FAKE_SM_SRC);

registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier === "@aws-sdk/client-secrets-manager") {
      return { url: FAKE_SM_URL, shortCircuit: true };
    }
    return nextResolve(specifier, context);
  },
});

// ---------------------------------------------------------------------------
// Load the REAL modules under test (dynamic import -- must happen AFTER the
// hook above is registered).
// ---------------------------------------------------------------------------
const EDGE_DIR = "../../../../../../../infra/aws/lambda-edge/auth-validator-edge";
const V2_DIR = "../../../../../../../infra/aws/users/lambda/portal-authorizer";

const v3 = await import(`${EDGE_DIR}/index.mjs`);
const { __setRenderKeySlotsForTest, RENDER_PRINT_PATH } = await import(`${EDGE_DIR}/render_auth.mjs`);
const v2 = await import(`${V2_DIR}/index.mjs`);
// The SAME jsonwebtoken install index.mjs itself resolves (bare specifier
// "jsonwebtoken" walks up from auth-validator-edge/ to its own node_modules);
// imported here by relative path since this test file has no node_modules
// ancestry of its own (round-16's own pattern, reused verbatim).
const jwtModule = await import(`${EDGE_DIR}/node_modules/jsonwebtoken/index.js`);
const jwt = jwtModule.default;

__setRenderKeySlotsForTest({ current: renderKeys.publicKey, previous: null });

// ---------------------------------------------------------------------------
// Token builders. Claims are fully explicit (iat/exp included by hand) so the
// expiry-bound arms have exact control -- never `options.expiresIn`, which
// would compute exp itself and could not produce a MISSING exp claim.
// ---------------------------------------------------------------------------
const RENDER_ISS = "opal-irpt-render";
const RENDER_AUD = "irpt-render";
const PORTAL_ISS = "opal-portal-auth";
const PORTAL_AUD = "opal-portal-api";

function nowSec() {
  return Math.floor(Date.now() / 1000);
}

function baseRenderClaims(overrides = {}) {
  const t = nowSec();
  return {
    iss: RENDER_ISS,
    aud: RENDER_AUD,
    jti: "rnd_test_001",
    sub: "render:rnd_test_001",
    role: "renderer",
    tier: "render",
    firmId: "49financial",
    bundle: "bundle_abc",
    revision: "rev_1",
    delegator: "advisor@49financial.com",
    accountSetId: "acctset123",
    jobId: "job456",
    reportId: "report789",
    iat: t,
    exp: t + 295,
    ...overrides,
  };
}

function signRenderToken(overrides = {}, key = renderKeys.privateKey) {
  const claims = baseRenderClaims(overrides);
  return jwt.sign(claims, key, { algorithm: "RS256" });
}

/** Same claim set as signRenderToken but with `exp` deleted entirely (not just
 * unset in overrides -- baseRenderClaims always sets one, so this strips it
 * back off after construction). */
function signRenderTokenNoExp(overrides = {}, key = renderKeys.privateKey) {
  const claims = baseRenderClaims(overrides);
  delete claims.exp;
  return jwt.sign(claims, key, { algorithm: "RS256" });
}

function signHumanToken(overrides = {}) {
  const t = nowSec();
  const payload = {
    iss: PORTAL_ISS,
    aud: PORTAL_AUD,
    sub: "user@49financial.com",
    name: "Test User",
    role: "user",
    tier: "advisor",
    firmId: "49financial",
    iat: t,
    exp: t + 900,
    ...overrides,
  };
  return jwt.sign(payload, humanKeys.privateKey, { algorithm: "RS256" });
}

// ---------------------------------------------------------------------------
// V2 event helpers (API Gateway HTTP API v2 authorizer shape).
// ---------------------------------------------------------------------------
const V2_ROUTE = "GET /api/scoped/investor-reporting/performance/{accountSetId}";
const V2_ROUTE_CLAIM = "accountSetId";
const V2_ROUTE_CLAIM_VALUE = "acctset123";

function v2Event(token, { routeKey = V2_ROUTE, pathParameters = { [V2_ROUTE_CLAIM]: V2_ROUTE_CLAIM_VALUE } } = {}) {
  return {
    routeKey,
    path: routeKey.split(" ")[1],
    httpMethod: "GET",
    pathParameters,
    headers: { Authorization: "Bearer " + token, "x-opal-origin-verify": ORIGIN_SECRET_VALUE },
  };
}

// ---------------------------------------------------------------------------
// V3 event helpers (CloudFront viewer-request shape).
// ---------------------------------------------------------------------------
function v3Event({ uri = RENDER_PRINT_PATH, token, extraHeaders = {}, method = "GET" } = {}) {
  const headers = { ...extraHeaders };
  if (token !== undefined) {
    headers["authorization"] = [{ key: "Authorization", value: `Bearer ${token}` }];
  }
  return { Records: [{ cf: { request: { method, uri, querystring: "", headers } } }] };
}

function v3IsRefusal(result) {
  return typeof result === "object" && result !== null && typeof result.status === "string";
}

function v3HeaderValue(result, name) {
  const h = result && result.headers && result.headers[name];
  return h && h[0] && h[0].value;
}

// ===========================================================================
// (a) V2: REJECT THE FOUR FORBIDDEN CLAIMS -- 4 negative + 1 positive control.
// ===========================================================================

test("V2 forbidden claim: role=admin is refused on an otherwise-admissible route", () => {
  const token = signRenderToken({ role: "admin" });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V2 forbidden claim: firmRole=admin is refused on an otherwise-admissible route", () => {
  const token = signRenderToken({ firmRole: "admin" });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V2 forbidden claim: tier=internal is refused on an otherwise-admissible route", () => {
  const token = signRenderToken({ tier: "internal" });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V2 forbidden claim: userType=Dev is refused on an otherwise-admissible route", () => {
  const token = signRenderToken({ userType: "Dev" });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V2 positive control: a clean render token (none of the four claims) on the same route is admitted", () => {
  const token = signRenderToken();
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, true);
  assert.equal(result.context.renderDelegate, "true");
});

// ===========================================================================
// (b) BOTH VERIFIERS: THE EXPIRY BOUND -- 4 controls x 2 verifiers = 8 arms.
// Each control isolates ONE thing: the TTL-bound check (exp-iat<=300) is kept
// satisfied in the skew-edge arms (iat chosen so exp-iat=200<=300), and the
// oversized-exp arm is NOT naturally expired by the clock (iat=now,
// exp=now+3600), so a pass there would prove only the runtime clock check
// fired, never the static bound -- which is exactly what this arm rules out.
// ===========================================================================

test("V2 expiry bound: a token with NO exp claim is refused, never treated as non-expiring", () => {
  const token = signRenderTokenNoExp();
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V3 expiry bound: a token with NO exp claim is refused, never treated as non-expiring", async () => {
  const token = signRenderTokenNoExp();
  const result = await v3.handler(v3Event({ token }));
  assert.equal(v3IsRefusal(result), true);
});

test("V2 expiry bound: an oversized exp (1 hour out) is refused even though not yet expired by the clock", () => {
  const t = nowSec();
  const token = signRenderToken({ iat: t, exp: t + 3600 });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V3 expiry bound: an oversized exp (1 hour out) is refused even though not yet expired by the clock", async () => {
  const t = nowSec();
  const token = signRenderToken({ iat: t, exp: t + 3600 });
  const result = await v3.handler(v3Event({ token }));
  assert.equal(v3IsRefusal(result), true);
});

test("V2 skew edge: exp 55s in the past (inside the 60s leeway) is ACCEPTED", () => {
  const exp = nowSec() - 55;
  const token = signRenderToken({ iat: exp - 200, exp });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, true);
});

test("V3 skew edge: exp 55s in the past (inside the 60s leeway) is ACCEPTED", async () => {
  const exp = nowSec() - 55;
  const token = signRenderToken({ iat: exp - 200, exp });
  const result = await v3.handler(v3Event({ token }));
  assert.equal(v3IsRefusal(result), false);
});

test("V2 skew edge: exp 65s in the past (outside the 60s leeway) is REFUSED", () => {
  const exp = nowSec() - 65;
  const token = signRenderToken({ iat: exp - 200, exp });
  const result = v2.authorizeRenderToken(token, v2Event(token));
  assert.equal(result.isAuthorized, false);
});

test("V3 skew edge: exp 65s in the past (outside the 60s leeway) is REFUSED", async () => {
  const exp = nowSec() - 65;
  const token = signRenderToken({ iat: exp - 200, exp });
  const result = await v3.handler(v3Event({ token }));
  assert.equal(v3IsRefusal(result), true);
});

// ===========================================================================
// (c) LOGGING -- jti/render id on accept AND refusal, at BOTH verifiers; and
// the no-secret-leak assertion (raw token / PEM content never appears).
// ===========================================================================

// Object args must be JSON-stringified, not `String()`ed -- `String({...})`
// collapses to the literal text "[object Object]", which would make every
// structured log line (every one of them, at both verifiers) invisible to
// this capture regardless of its real content and give a false negative on
// the render-identity assertion below rather than a true one.
function stringifyArg(a) {
  if (typeof a === "string") return a;
  try {
    return JSON.stringify(a);
  } catch {
    return String(a);
  }
}

function captureConsole(fn) {
  const lines = [];
  const orig = { log: console.log, warn: console.warn, error: console.error };
  console.log = (...args) => lines.push(args.map(stringifyArg).join(" "));
  console.warn = (...args) => lines.push(args.map(stringifyArg).join(" "));
  console.error = (...args) => lines.push(args.map(stringifyArg).join(" "));
  try {
    fn();
  } finally {
    console.log = orig.log;
    console.warn = orig.warn;
    console.error = orig.error;
  }
  return lines.join("\n");
}

async function captureConsoleAsync(fn) {
  const lines = [];
  const orig = { log: console.log, warn: console.warn, error: console.error };
  console.log = (...args) => lines.push(args.map(stringifyArg).join(" "));
  console.warn = (...args) => lines.push(args.map(stringifyArg).join(" "));
  console.error = (...args) => lines.push(args.map(stringifyArg).join(" "));
  try {
    await fn();
  } finally {
    console.log = orig.log;
    console.warn = orig.warn;
    console.error = orig.error;
  }
  return lines.join("\n");
}

test("V2 logging: accept and refusal log lines carry jti/renderId; no raw token or PEM leaks", () => {
  const acceptToken = signRenderToken({ jti: "rnd_log_accept", sub: "render:rnd_log_accept" });
  const acceptLog = captureConsole(() => v2.authorizeRenderToken(acceptToken, v2Event(acceptToken)));
  assert.match(acceptLog, /rnd_log_accept/, "accept log must carry the render identity");
  assert.doesNotMatch(acceptLog, new RegExp(acceptToken.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
    "accept log must never carry the raw JWT string");
  assert.doesNotMatch(acceptLog, /BEGIN (RSA )?(PUBLIC|PRIVATE) KEY/, "accept log must never carry key material");

  const refuseToken = signRenderToken({ jti: "rnd_log_refuse", sub: "render:rnd_log_refuse", role: "admin" });
  const refuseLog = captureConsole(() => v2.authorizeRenderToken(refuseToken, v2Event(refuseToken)));
  assert.match(refuseLog, /rnd_log_refuse/, "refusal log must carry the render identity");
  assert.doesNotMatch(refuseLog, new RegExp(refuseToken.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
    "refusal log must never carry the raw JWT string");
  assert.doesNotMatch(refuseLog, /BEGIN (RSA )?(PUBLIC|PRIVATE) KEY/, "refusal log must never carry key material");
});

test("V3 logging: accept and the expired-refusal log line carry jti; no raw token or PEM leaks", async () => {
  const acceptToken = signRenderToken({ jti: "rnd_v3_log_accept", sub: "render:rnd_v3_log_accept" });
  const acceptLog = await captureConsoleAsync(() => v3.handler(v3Event({ token: acceptToken })));
  assert.match(acceptLog, /rnd_v3_log_accept/, "V3 accept log must carry the render identity");
  assert.doesNotMatch(acceptLog, new RegExp(acceptToken.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
    "V3 accept log must never carry the raw JWT string");

  const t = nowSec();
  const expiredToken = signRenderToken({ jti: "rnd_v3_log_expired", sub: "render:rnd_v3_log_expired", iat: t - 900, exp: t - 600 });
  const expiredLog = await captureConsoleAsync(() => v3.handler(v3Event({ token: expiredToken })));
  assert.match(expiredLog, /rnd_v3_log_expired/,
    "V3's expired-refusal log line was found missing render identity (the same gap named at V2) and fixed here");
  assert.doesNotMatch(expiredLog, new RegExp(expiredToken.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
    "V3 expired-refusal log must never carry the raw JWT string");

  const boundToken = signRenderTokenNoExp({ jti: "rnd_v3_log_bound", sub: "render:rnd_v3_log_bound" });
  const boundLog = await captureConsoleAsync(() => v3.handler(v3Event({ token: boundToken })));
  assert.match(boundLog, /rnd_v3_log_bound/, "V3's expiry-bound refusal log line must carry the render identity");
  assert.doesNotMatch(boundLog, new RegExp(boundToken.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
    "V3 expiry-bound refusal log must never carry the raw JWT string");
});

// ===========================================================================
// (d) THE HUMAN PATH IS UNTOUCHED -- regression confirmation at both verifiers.
// ===========================================================================

test("V2 human-path regression: a human token is never classified as a render-audience token, so it never reaches authorizeRenderToken", () => {
  const token = signHumanToken({ sub: "advisor.a@49financial.com", role: "user", tier: "advisor", firmId: "49financial" });
  assert.equal(v2.isRenderAudienceToken(token), false, "a human token must never be classified as a render-audience token");
});

test("V2 human-path regression: the full handler still authorizes an ordinary human token, byte-identical context shape", async () => {
  const token = signHumanToken({ sub: "advisor.a@49financial.com", role: "user", tier: "advisor", firmId: "49financial", advisorId: "ADV-A-0001" });
  const event = v2Event(token);
  const result = await v2.handler(event);
  assert.equal(result.isAuthorized, true);
  assert.equal(result.context.email, "advisor.a@49financial.com");
  assert.equal(result.context.role, "user");
  assert.equal(result.context.tier, "advisor");
  assert.equal(Object.prototype.hasOwnProperty.call(result.context, "renderDelegate"), false,
    "a human context must never carry a render-delegate marker");
});

test("V2 human-path regression: the pre-existing admin bypass still computes ALL access, unaffected by the render forbidden-claims check", async () => {
  const token = signHumanToken({ sub: "admin1@opal-capital.com", role: "admin", tier: "internal", firmId: "opal-capital", userType: "Dev" });
  const result = await v2.handler(v2Event(token));
  assert.equal(result.isAuthorized, true);
  assert.equal(result.context.allowedFirmIds, "ALL");
});

test("V3 human-path regression: an ordinary human token falls through to the unchanged human-path evaluation", async () => {
  const token = signHumanToken({ sub: "advisor.a@49financial.com", role: "user", tier: "advisor", firmId: "49financial" });
  const uri = "/api/scoped/investor-reporting/directory";
  const result = await v3.handler(v3Event({ uri, token }));
  assert.equal(v3IsRefusal(result), false, "a valid human token on a benign path must still be admitted");
  assert.equal(v3HeaderValue(result, "x-user-email"), "advisor.a@49financial.com");
  assert.equal(v3HeaderValue(result, "x-user-role"), "user");
  assert.equal(v3HeaderValue(result, "x-user-tier"), "advisor");
});

test("V3 human-path regression: the pre-existing admin bypass still injects the pre-existing header set", async () => {
  const token = signHumanToken({ sub: "admin1@opal-capital.com", role: "admin", tier: "internal", firmId: "opal-capital" });
  const uri = "/api/scoped/investor-reporting/directory";
  const result = await v3.handler(v3Event({ uri, token }));
  assert.equal(v3IsRefusal(result), false);
  assert.equal(v3HeaderValue(result, "x-user-role"), "admin");
  assert.equal(v3HeaderValue(result, "x-user-tier"), "internal");
});
