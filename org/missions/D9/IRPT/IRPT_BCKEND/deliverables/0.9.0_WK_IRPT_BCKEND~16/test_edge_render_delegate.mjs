// IRPT_BCKEND.TO-IB-rtq-3 -- THE V3 EDGE RENDER-DELEGATE BRANCH.
// Criterion R117-AC3. Invocation (task order, verbatim):
//   cd deliverables/0.9.0_WK_IRPT_BCKEND~16 && node --test test_edge_render_delegate.mjs
//
// Exercises the REAL `auth-validator-edge/index.mjs` handler (unedited
// import, no test-only branch in production code) and the REAL
// `render_auth.mjs` module this cell adds, against fixture RSA keypairs and
// synthetic CloudFront viewer-request events. No AWS call is ever reached
// (BOUNDS: "NO AWS API call ... against a fixture keypair and synthetic
// requests"): the render key path uses `render_auth.mjs`'s own
// `__setRenderKeySlotsForTest` seam; the HUMAN key path (needed so the
// pre-existing behaviour can be regression-tested through the real handler)
// is served by intercepting the `@aws-sdk/client-secrets-manager` module
// specifier for this process via `node:module`'s `registerHooks`, so
// `infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs` (read-only import,
// outside this cell's <paths>, NEVER edited) resolves a fixture PEM instead
// of a live secret.
//
// SURPRISE (filed IRPT_BCKEND-W16-S1, non-blocking, kept working per
// BOUNDS): the CELL's arm (c) says "run the existing edge-auth test file
// (find it, confirm its current pass state before your change...)" -- no
// such file exists anywhere in the tracked tree at this HEAD (comp-find
// across the whole estate: zero hits for any *.test.mjs / *.spec.mjs /
// test_*.mjs under infra/aws/lambda-edge/auth-validator-edge/, and zero
// `node:test` import anywhere in the repo). The nearest prior work on this
// same handler (POSN_AGGFIX AF1-s-11, C1-1) built a Python-driven harness
// under its own deliverables/ rather than a persistent .mjs suite. So this
// ONE file (the only file the criterion's invocation names) carries BOTH
// the new render-branch tests AND a self-built regression suite standing in
// for "the pre-existing edge-auth suite" -- every regression test below
// exercises HUMAN-path behaviour that existed before this cell's diff and
// is unchanged by it (arm (f), the negative-widening control). Nothing
// pre-existing was modified because nothing pre-existing was found.
//
// SURPRISE (filed IRPT_BCKEND-W16-S2, non-blocking): the PRD (item 4, V3
// half) never pins the exact shape of "the SPA's static asset paths", and
// `portal/` is a git submodule not checked out in this worktree, so the
// built asset path cannot be read to confirm. `render_auth.mjs` documents
// the conservative interpretation used (see its own comment); this test
// file exercises exactly that interpretation, not a guessed alternative.
//
// SURPRISE (filed IRPT_BCKEND-W16-S3, non-blocking): CELL arm (e) asks for
// a test "running [a render-key token] through V1's existing verification
// path (read-only use of V1's code, no edit)". V1
// (infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts) is TypeScript
// whose own key retrieval (`getJwtVerifySlots` -> `getJwtKeySlots`) needs
// EITHER a live Secrets Manager call (BOUNDS: none this round) OR that
// directory's OWN `node_modules` (jsonwebtoken, etc.), which is not
// populated in this worktree and sits outside IB-rtq-3's <paths> grant
// (infra/aws/lambda-edge/auth-validator-edge/ only) -- populating it would
// be a write outside the grant. The V1 test below instead reads V1's own
// verify() parameters directly from its source (cited by line, never
// guessed) and calls `jsonwebtoken.verify()` -- the SAME library V1 itself
// calls -- with those exact parameters against a portal-key fixture. CVO
// adjudicates at L9 whether this satisfies the letter of "running it
// through V1's existing verification path".

import { test } from "node:test";
import assert from "node:assert/strict";
import { registerHooks } from "node:module";
import crypto from "node:crypto";

// ---------------------------------------------------------------------------
// Fixture keypairs. CELL (a): "a fixture key you generate for this cell's
// own test -- do not depend on IB-rtq-1's actual module; generate your own
// throwaway keypair so this cell is independently testable."
// ---------------------------------------------------------------------------
function genKeyPair() {
  return crypto.generateKeyPairSync("rsa", {
    modulusLength: 2048,
    publicKeyEncoding: { type: "spki", format: "pem" },
    privateKeyEncoding: { type: "pkcs8", format: "pem" },
  });
}

const renderKeys = genKeyPair(); // the render token signer (throwaway, this cell's own)
const portalKeys = genKeyPair(); // stands in for the LIVE opal/auth/jwt-public-key
const strangerKeys = genKeyPair(); // signs neither correctly -- "signed by nobody we trust"

// ---------------------------------------------------------------------------
// Intercept @aws-sdk/client-secrets-manager for this process so the human
// path's REAL, UNEDITED getJwtKeySlots() (jwtPublicKeys.mjs, outside this
// cell's <paths>) resolves a fixture instead of a live secret. The render
// key path never reaches this -- it is seeded directly via render_auth.mjs's
// own `__setRenderKeySlotsForTest` test seam below.
// ---------------------------------------------------------------------------
const PORTAL_SECRET_ID = "opal/auth/jwt-public-key";
const FAKE_SM_SRC = `
export class SecretsManagerClient {
  constructor() {}
  async send(cmd) {
    const id = cmd && cmd.input && cmd.input.SecretId;
    if (id === ${JSON.stringify(PORTAL_SECRET_ID)}) {
      return { SecretString: ${JSON.stringify(portalKeys.publicKey)} };
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
// hook above is registered, since index.mjs's module graph statically
// imports jwtPublicKeys.mjs, which statically imports the AWS SDK package).
// ---------------------------------------------------------------------------
const EDGE_DIR = "../../../../../../../infra/aws/lambda-edge/auth-validator-edge";

const { handler } = await import(`${EDGE_DIR}/index.mjs`);
const { __setRenderKeySlotsForTest, RENDER_PRINT_PATH } = await import(`${EDGE_DIR}/render_auth.mjs`);
// The SAME jsonwebtoken install index.mjs itself resolves (bare specifier
// "jsonwebtoken" walks up from auth-validator-edge/ to its own
// node_modules); imported here by relative path since this test file has
// no node_modules ancestry of its own.
const jwtModule = await import(`${EDGE_DIR}/node_modules/jsonwebtoken/index.js`);
const jwt = jwtModule.default;

__setRenderKeySlotsForTest({ current: renderKeys.publicKey, previous: null });

// ---------------------------------------------------------------------------
// Token builders
// ---------------------------------------------------------------------------
const RENDER_ISS = "opal-irpt-render";
const RENDER_AUD = "irpt-render";

function signRenderToken(overrides = {}) {
  const payload = {
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
    ...overrides,
  };
  const options = { algorithm: "RS256" };
  if (payload.exp === undefined) options.expiresIn = "5m";
  return jwt.sign(payload, renderKeys.privateKey, options);
}

// V1 constants read from source (auth-handler/src/jwt.ts :19-20), never
// guessed -- reused here for both the human-token fixture and the V1
// replication test below.
const PORTAL_ISS = "opal-portal-auth";
const PORTAL_AUD = "opal-portal-api";

function signHumanToken(overrides = {}) {
  const payload = {
    iss: PORTAL_ISS,
    aud: PORTAL_AUD,
    sub: "user@49financial.com",
    name: "Test User",
    role: "user",
    tier: "advisor",
    firmId: "49financial",
    ...overrides,
  };
  const options = { algorithm: "RS256" };
  if (payload.exp === undefined) options.expiresIn = "15m";
  return jwt.sign(payload, portalKeys.privateKey, options);
}

// ---------------------------------------------------------------------------
// CloudFront viewer-request event + response helpers
// ---------------------------------------------------------------------------
function makeEvent({ uri, token, extraHeaders = {}, method = "GET" }) {
  const headers = { ...extraHeaders };
  if (token !== undefined) {
    headers["authorization"] = [{ key: "Authorization", value: `Bearer ${token}` }];
  }
  return { Records: [{ cf: { request: { method, uri, querystring: "", headers } } }] };
}

function headerValue(result, name) {
  const h = result && result.headers && result.headers[name];
  return h && h[0] && h[0].value;
}

function isRefusal(result) {
  return typeof result === "object" && result !== null && typeof result.status === "string";
}

// A benign human-path URI that trips NONE of the existing branches needing
// extra I/O or a non-admin-bypass role: not an aggregate path
// (aggregate_gate.mjs AGGREGATE_PATHS), not under /api/scoped/advisor-
// intelligence/ (tier_policy.mjs requiredTierForUri), not an advisor/
// account/relationship scoping path (index.mjs matchAdvisorScopingPath /
// matchResourceScopingPath). Reaches the final header-injection line by the
// same path it always did.
const BENIGN_HUMAN_URI = "/api/scoped/investor-reporting/directory";

// A URI outside every render-admitted shape, but plausible (the PRD's own
// PrintRoute default is "/investor-reporting/print" -- this is its sibling
// "status" route, referenced in infra/aws/terraform/investor-reporting/
// export/ssm.tf, never in the render's own admit list).
const RENDER_INADMISSIBLE_URI = "/investor-reporting/status";

// ===========================================================================
// (a) THE THREE-PATH ADMISSION
// ===========================================================================

test("three-path admission: /investor-reporting/print is admitted", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), false, "print route must be admitted, not refused");
  assert.equal(result.uri, RENDER_PRINT_PATH);
  assert.equal(headerValue(result, "x-user-role"), "renderer");
});

// RE-PINNED (round 18, 2.0.0_SA_COO~B, COO ruling on a genuine conflict between IB-rtr-1's
// BOUNDS and IB-rtr-4's "durable baseline, unedited" instruction -- neither cell's own
// <paths> granted this file, so neither could fix it itself under its own BOUNDS). This
// assertion originally asserted a DISCLOSED GUESS (row IRPT_BCKEND-W16-S2, filed because
// `portal/` was not checked out in that worker's worktree): a static asset path prefixed
// `/investor-reporting/`. Round 18's IB-rtr-1 read the SPA's real, pinned `vite.config.ts`
// (neither `base` nor `build.assetsDir` overridden -- confirmed independently by the COO,
// not just cited) and found the real Vite-default public asset path is root `/assets/`,
// never `/investor-reporting/assets/`. Re-pinning this ONE assertion to the real, verified
// path -- this is a correction of a labeled guess with the now-known real answer, never a
// weakening of what the test checks (a static asset must still be admitted, not refused).
test("three-path admission: a static asset under the real /assets/ prefix is admitted", async () => {
  const token = signRenderToken();
  const uri = "/assets/app-9f3c1a.js";
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), false, "SPA static asset must be admitted, not refused");
  assert.equal(headerValue(result, "x-user-role"), "renderer");
});

test("three-path admission: GET performance API is admitted", async () => {
  const token = signRenderToken();
  const uri = "/api/scoped/investor-reporting/performance/acctset123";
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-user-role"), "renderer");
});

test("three-path admission: GET analysis sections API is admitted", async () => {
  const token = signRenderToken();
  const uri = "/api/scoped/investor-reporting/analysis/job456/sections";
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-user-role"), "renderer");
});

test("three-path admission: GET narrative API is admitted", async () => {
  const token = signRenderToken();
  const uri = "/api/scoped/investor-reporting/narrative/report789";
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-user-role"), "renderer");
});

test("any other URI is refused BY THE BRANCH itself, never falls through to the human path", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({ uri: RENDER_INADMISSIBLE_URI, token }));
  assert.equal(isRefusal(result), true, "an inadmissible URI on a valid render token must be refused");
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token not admitted for this resource");
});

// ===========================================================================
// (b) THE INJECTION, MIRRORING THE EXISTING SHAPE
// ===========================================================================

test("header injection OVERWRITES client-supplied values of the same names", async () => {
  const token = signRenderToken({ firmId: "inflection", jti: "rnd_overwrite_001", delegator: "d1", bundle: "b1", revision: "r1" });
  const result = await handler(makeEvent({
    uri: RENDER_PRINT_PATH,
    token,
    extraHeaders: {
      "x-firm-id": [{ key: "X-Firm-Id", value: "SPOOFED-FIRM" }],
      "x-user-role": [{ key: "X-User-Role", value: "admin" }],
      "x-user-email": [{ key: "X-User-Email", value: "attacker@evil.example" }],
      "x-render-delegator": [{ key: "X-Render-Delegator", value: "SPOOFED-DELEGATOR" }],
      "x-render-bundle": [{ key: "X-Render-Bundle", value: "SPOOFED-BUNDLE" }],
      "x-render-revision": [{ key: "X-Render-Revision", value: "SPOOFED-REVISION" }],
    },
  }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-firm-id"), "inflection", "verified claim must win over client-supplied X-Firm-Id");
  assert.equal(headerValue(result, "x-user-role"), "renderer", "verified role must win over client-supplied X-User-Role");
  assert.equal(headerValue(result, "x-user-email"), "render:rnd_overwrite_001", "verified render id must win over client-supplied X-User-Email");
  assert.equal(headerValue(result, "x-render-delegator"), "d1");
  assert.equal(headerValue(result, "x-render-bundle"), "b1");
  assert.equal(headerValue(result, "x-render-revision"), "r1");
});

test("X-Advisor-Id / X-Advisor-Role / X-User-Type are ABSENT on every render-token admit path, even when the caller supplied fake values", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({
    uri: RENDER_PRINT_PATH,
    token,
    extraHeaders: {
      "x-advisor-id": [{ key: "X-Advisor-Id", value: "adv_fake_123" }],
      "x-advisor-role": [{ key: "X-Advisor-Role", value: "architect" }],
      "x-user-type": [{ key: "X-User-Type", value: "Dev" }],
    },
  }));
  assert.equal(isRefusal(result), false);
  assert.equal(result.headers["x-advisor-id"], undefined, "X-Advisor-Id must never reach the origin on a render path");
  assert.equal(result.headers["x-advisor-role"], undefined, "X-Advisor-Role must never reach the origin on a render path");
  assert.equal(result.headers["x-user-type"], undefined, "X-User-Type must never reach the origin on a render path");
});

// ===========================================================================
// (c) / (d) REFUSAL ARMS
// ===========================================================================

test("a render token carrying tier=internal is refused BY THIS BRANCH, not merely unused downstream", async () => {
  const token = signRenderToken({ tier: "internal" });
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), true);
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token carries a forbidden claim");
});

test("a render token carrying role=admin is refused BY THIS BRANCH", async () => {
  const token = signRenderToken({ role: "admin" });
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), true);
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token carries a forbidden claim");
});

test("a render token carrying firmRole=admin is refused BY THIS BRANCH", async () => {
  const token = signRenderToken({ firmRole: "admin" });
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), true);
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token carries a forbidden claim");
});

test("a render token carrying userType=Dev is refused BY THIS BRANCH", async () => {
  const token = signRenderToken({ userType: "Dev" });
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), true);
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token carries a forbidden claim");
});

test("a render token past its exp is refused, using the JWT library's own expiry check", async () => {
  const nowSeconds = Math.floor(Date.now() / 1000);
  const token = signRenderToken({ exp: nowSeconds - 600, iat: nowSeconds - 900 });
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), true);
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token expired");
});

// ===========================================================================
// (c) arm (f) -- NEGATIVE-WIDENING REGRESSION CONTROL: the pre-existing
// human-path evaluation is UNCHANGED. See file header for why this suite
// (rather than a separate pre-existing file) carries these tests.
// ===========================================================================

test("a token for the wrong aud (a human portal token) falls through to the EXISTING human-path evaluation, completely unchanged", async () => {
  const token = signHumanToken({ role: "user", tier: "advisor", firmId: "49financial", sub: "advisor1@49financial.com" });
  const result = await handler(makeEvent({ uri: BENIGN_HUMAN_URI, token }));
  assert.equal(isRefusal(result), false, "a valid human token on a benign path must still be admitted");
  assert.equal(headerValue(result, "x-user-email"), "advisor1@49financial.com");
  assert.equal(headerValue(result, "x-user-role"), "user");
  assert.equal(headerValue(result, "x-user-tier"), "advisor");
  assert.equal(headerValue(result, "x-firm-id"), "49financial");
  // Pre-existing behaviour: the human path injects X-Advisor-Id as an EMPTY
  // STRING when absent (present, not deleted) -- the OPPOSITE of the render
  // path's unconditional delete, proving the two paths are genuinely
  // distinct and the human path's own shape was not touched.
  assert.equal(headerValue(result, "x-advisor-id"), "");
});

test("regression: missing Authorization header is still refused exactly as before", async () => {
  const result = await handler(makeEvent({ uri: BENIGN_HUMAN_URI }));
  assert.equal(isRefusal(result), true);
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Missing or invalid Authorization header");
});

test("regression: a token signed by neither key is still refused via the existing catch-all", async () => {
  const token = jwt.sign(
    { iss: PORTAL_ISS, aud: PORTAL_AUD, sub: "nobody@nowhere.example", role: "user", tier: "advisor", firmId: "49financial" },
    strangerKeys.privateKey,
    { algorithm: "RS256", expiresIn: "15m" }
  );
  const result = await handler(makeEvent({ uri: BENIGN_HUMAN_URI, token }));
  assert.equal(isRefusal(result), true);
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Invalid or expired token");
});

test("regression: an expired HUMAN token is still refused exactly as before", async () => {
  const nowSeconds = Math.floor(Date.now() / 1000);
  const token = signHumanToken({ exp: nowSeconds - 600, iat: nowSeconds - 1500 });
  const result = await handler(makeEvent({ uri: BENIGN_HUMAN_URI, token }));
  assert.equal(isRefusal(result), true);
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Invalid or expired token");
});

test("regression: the pre-existing admin bypass still injects the pre-existing header set", async () => {
  const token = signHumanToken({ role: "admin", tier: "internal", sub: "admin1@opal-capital.com", firmId: "opal-capital" });
  const result = await handler(makeEvent({ uri: BENIGN_HUMAN_URI, token }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-user-role"), "admin");
  assert.equal(headerValue(result, "x-user-tier"), "internal");
  assert.equal(headerValue(result, "x-firm-id"), "opal-capital");
});

// ===========================================================================
// (e) V1 REFUSAL CONFIRMATION (see file header SURPRISE note for why this is
// a faithful REPLICATION of V1's own read parameters rather than a direct
// import of V1's TypeScript module).
// ===========================================================================

test("V1 refusal confirmation: a render-signed token fails V1's own verify() parameters with a SIGNATURE error (wrong key), before aud/iss are ever checked", () => {
  // V1 = infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts
  // verifyAccessToken (:251-261) calls verifyWithSlots(jwt, token, slots,
  // { algorithms: ['RS256'], issuer: JWT_ISSUER, audience: JWT_AUDIENCE })
  // where JWT_ISSUER = 'opal-portal-auth' (:19) and
  // JWT_AUDIENCE = 'opal-portal-api' (:20) -- read directly from source,
  // reproduced here verbatim as PORTAL_ISS / PORTAL_AUD.
  const renderToken = signRenderToken();
  assert.throws(
    () => jwt.verify(renderToken, portalKeys.publicKey, {
      algorithms: ["RS256"],
      issuer: PORTAL_ISS,
      audience: PORTAL_AUD,
    }),
    (err) => {
      assert.equal(err.name, "JsonWebTokenError", `expected a signature-stage JsonWebTokenError, got ${err.name}: ${err.message}`);
      assert.match(err.message, /invalid signature/);
      return true;
    }
  );
});
