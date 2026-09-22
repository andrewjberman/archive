// IRPT_BCKEND.TO-IB-rtr-4 -- THE V1 HARNESS.
// Criterion R118-AC4, third leg. Invocation (task order, verbatim):
//   cd deliverables/0.9.0_WK_IRPT_BCKEND~20 && ... && node --test test_v1_actual_module_harness.mjs
//
// CELL (c): "Build a NEW offline test harness that invokes V1's ACTUAL
// `verifyAccessToken` function (infra/aws/opalinvest_dev/lambda/auth-handler
// /src/jwt.ts) directly -- import and call the real function, with its
// key-retrieval dependency faked ... This is genuinely NEW work, not a
// relabeling of IB-rtq-3's own replication test (which read V1's parameters
// and called jsonwebtoken.verify() directly, never V1's own function) --
// this harness calls V1's OWN CODE."
//
// WHAT "V1's OWN CODE" MEANS HERE, MEASURED THIS SESSION. `jwt.ts` cannot be
// run as raw TypeScript source through Node's native --experimental-strip-types
// (default-on, this Node): it is plain type-stripping (erasure), not full
// type-checking, so `import { AccessTokenPayload, RefreshTokenPayload, User }
// from './types'` (no `import type`) is left as a VALUE import once stripped,
// and `./types` (an interfaces-only file, zero runtime exports) then throws
// "does not provide an export named 'AccessTokenPayload'" -- reproducible
// with `node --experimental-strip-types` directly on jwt.ts. V1's own
// package.json ("build": "tsc", tsconfig.json "module": "commonjs") settles
// what "V1's own code" actually means at runtime: V1 is a Lambda that ships
// COMPILED CommonJS (`dist/`), never raw .ts. So this harness imports the
// SAME compiled artifact the deployed Lambda runs -- `tsc` elides the
// type-only `./types` import entirely in commonjs output (verified: `grep
// types dist/jwt.js` finds nothing), which is exactly why the real build
// succeeds where a bare strip-types run does not. This is `verifyAccessToken`
// itself, unedited, compiled by the project's own unmodified tsconfig.json --
// never a hand-written stand-in.
//
// TWO PREREQUISITES, NEITHER COMMITTED, BOTH GITIGNORED, NEITHER TOUCHED BY
// THIS CELL'S <paths> GRANT (auth-handler/ is outside it; SURPRISE filed,
// IRPT_BCKEND-W20-S1, non-blocking, kept working per BOUNDS):
//   1. `infra/aws/opalinvest_dev/lambda/auth-handler/src/lib/` -- the
//      BUILD-TIME MIRROR of `infra/aws/lambda/lib/` that jwt.ts's own
//      `./lib/authkeys/jwtPublicKeys.mjs` import needs (build-nodejs-
//      lambda.sh:137-158 per that file's own docstring; auth-handler's own
//      .gitignore:1-7 names this exact mechanism and gitignores it for
//      exactly this reason -- "a tracked copy is a SECOND CARRIER").
//   2. `dist/` -- the project's own `tsc` output (package.json "build":
//      "tsc", unmodified tsconfig.json), plus `dist/lib/authkeys/
//      jwtPublicKeys.mjs` copied alongside (tsc's `include` is `src/**/*`,
//      which does not copy a non-.ts file; the real Lambda package step
//      does this copy as part of packaging, outside this cell's <paths>).
// Reproduction, run once before this file (see result.md for the exact
// commands used this session): `bun install` in both
// auth-validator-edge/ (needed by the second leg of this criterion,
// already-established precedent) and auth-handler/ (needed by this leg);
// mirror `infra/aws/lambda/lib/` into `auth-handler/src/lib/`; `tsc` in
// auth-handler/; copy the mirrored `authkeys/jwtPublicKeys.mjs` into
// `dist/lib/authkeys/`. All four steps are local-only, offline, no AWS call,
// no deploy, no Terraform -- BOUNDS-compliant, same class as the ephemeral
// `node_modules` install row IRPT_BCKEND-W15-S4 already established as
// non-blocking.
//
// THE KEY-RETRIEVAL DEPENDENCY IS FAKED, NEVER V1'S CODE. `verifyAccessToken`
// -> `getJwtVerifySlots()` -> the shared `getJwtKeySlots()` (jwtPublicKeys.mjs,
// read-only import, outside this cell's <paths>, NEVER edited) which calls
// AWS Secrets Manager for `opal/auth/jwt-public-key`. This harness intercepts
// the `@aws-sdk/client-secrets-manager` module specifier for this process via
// `node:module`'s `registerHooks` (the SAME technique IB-rtq-3's own
// `test_edge_render_delegate.mjs` uses for its human-path regression tests),
// so the SecretsManager call resolves a fixture RSA public key instead of a
// live secret -- no AWS API call is ever reached.

import { test } from "node:test";
import assert from "node:assert/strict";
import { registerHooks } from "node:module";
import crypto from "node:crypto";

// ---------------------------------------------------------------------------
// Fixture keypairs -- this cell's own throwaway RSA keys, never IB-rtq-1's or
// IB-rtq-3's actual key material, same convention as test_edge_render_
// delegate.mjs's own fixtures.
// ---------------------------------------------------------------------------
function genKeyPair() {
  return crypto.generateKeyPairSync("rsa", {
    modulusLength: 2048,
    publicKeyEncoding: { type: "spki", format: "pem" },
    privateKeyEncoding: { type: "pkcs8", format: "pem" },
  });
}

const portalKeys = genKeyPair();   // stands in for the LIVE opal/auth/jwt-public-key
const renderKeys = genKeyPair();   // the render-key signer -- V1 must never trust this key
const strangerKeys = genKeyPair(); // signed by nobody V1 trusts, at either key

// ---------------------------------------------------------------------------
// Intercept @aws-sdk/client-secrets-manager for this process so V1's REAL,
// UNEDITED getJwtVerifySlots() -> getJwtKeySlots() (jwtPublicKeys.mjs,
// outside this cell's <paths>) resolves a fixture instead of a live secret.
// ---------------------------------------------------------------------------
const PORTAL_SECRET_ID = "opal/auth/jwt-public-key"; // jwtPublicKeys.mjs JWT_PUBLIC_KEY_SECRET_ID
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
// Load V1's REAL compiled module (dynamic import -- must happen AFTER the
// hook above is registered, since jwt.js's module graph transitively
// require()s jwtPublicKeys.mjs, which statically imports the AWS SDK
// package; Node's synchronous require(esm) support routes that require
// through the same ESM resolver these hooks patch -- verified this session).
// ---------------------------------------------------------------------------
const V1_DIR = "../../../../../../../infra/aws/opalinvest_dev/lambda/auth-handler";
const { verifyAccessToken } = await import(`${V1_DIR}/dist/jwt.js`);

// The SAME jsonwebtoken install V1 itself resolves (bare specifier
// "jsonwebtoken" walks up from auth-handler/ to its own node_modules);
// imported here by relative path since this test file has no node_modules
// ancestry of its own -- same convention as test_edge_render_delegate.mjs.
const jwtModule = await import(`${V1_DIR}/node_modules/jsonwebtoken/index.js`);
const jwt = jwtModule.default;

// V1 constants read directly from source (auth-handler/src/jwt.ts :19-20),
// never guessed.
const PORTAL_ISS = "opal-portal-auth";
const PORTAL_AUD = "opal-portal-api";

function signHumanToken(overrides = {}) {
  const payload = {
    sub: "user@49financial.com",
    name: "Test User",
    role: "user",
    tier: "advisor",
    firmId: "49financial",
    iss: PORTAL_ISS,
    aud: PORTAL_AUD,
    ...overrides,
  };
  const options = { algorithm: "RS256" };
  if (payload.exp === undefined) options.expiresIn = "15m";
  return jwt.sign(payload, portalKeys.privateKey, options);
}

function signRenderToken(overrides = {}) {
  const payload = {
    iss: "opal-irpt-render",
    aud: "irpt-render",
    jti: "rnd_test_001",
    sub: "render:rnd_test_001",
    role: "renderer",
    firmId: "49financial",
    bundle: "bundle_abc",
    revision: "rev_1",
    delegator: "advisor@49financial.com",
    ...overrides,
  };
  const options = { algorithm: "RS256" };
  if (payload.exp === undefined) options.expiresIn = "5m";
  return jwt.sign(payload, renderKeys.privateKey, options);
}

// ===========================================================================
// POSITIVE CONTROL -- proves the harness itself works, not just that
// everything gets refused (CELL (c)'s own requirement).
// ===========================================================================

test("V1 ACTUAL verifyAccessToken: a valid human token, through V1's REAL function, is accepted", async () => {
  const token = signHumanToken();
  const payload = await verifyAccessToken(token);
  assert.equal(payload.sub, "user@49financial.com");
  assert.equal(payload.role, "user");
  assert.equal(payload.tier, "advisor");
  assert.equal(payload.firmId, "49financial");
});

test("V1 ACTUAL verifyAccessToken: a wrong-key human-shaped token is still refused (negative control on the positive control's own fixture)", async () => {
  const forged = jwt.sign(
    { sub: "nobody@nowhere.example", role: "user", tier: "advisor", firmId: "49financial",
      iss: PORTAL_ISS, aud: PORTAL_AUD },
    strangerKeys.privateKey,
    { algorithm: "RS256", expiresIn: "15m" }
  );
  await assert.rejects(() => verifyAccessToken(forged), (err) => {
    assert.equal(err.name, "JsonWebTokenError");
    assert.match(err.message, /invalid signature/);
    return true;
  });
});

// ===========================================================================
// REFUSAL ARM -- CELL (c): "a render-key-signed token, run through V1's
// actual verifyAccessToken, is refused (same expectation as before)".
// ===========================================================================

test("V1 ACTUAL verifyAccessToken: a render-key-signed token is refused BY V1's REAL FUNCTION, through its own key-verification path", async () => {
  const token = signRenderToken();
  await assert.rejects(() => verifyAccessToken(token), (err) => {
    // Signed by renderKeys, verified against portalKeys (the fixture the
    // faked SecretsManager returns) -- fails at the SIGNATURE stage, before
    // V1's own issuer/audience checks ever run, exactly as
    // test_edge_render_delegate.mjs's replication test found reading
    // jsonwebtoken's own verify.js check order (that test's own comment,
    // W16-S3's context) -- reproduced here against V1's OWN CODE rather than
    // a replicated call, which is the entire point of this new harness.
    assert.equal(err.name, "JsonWebTokenError", `expected a signature-stage JsonWebTokenError, got ${err.name}: ${err.message}`);
    assert.match(err.message, /invalid signature/);
    return true;
  });
});

test("V1 ACTUAL verifyAccessToken: a render token also carrying the WRONG issuer/audience is still refused (never a false accept via a laxer path)", async () => {
  // A render token would also fail V1's iss/aud check even if it were
  // somehow signed by the portal key -- both defenses hold independently.
  const wrongClaims = jwt.sign(
    { sub: "render:rnd_test_002", role: "renderer", iss: "opal-irpt-render", aud: "irpt-render" },
    portalKeys.privateKey,
    { algorithm: "RS256", expiresIn: "5m" }
  );
  await assert.rejects(() => verifyAccessToken(wrongClaims), (err) => {
    assert.equal(err.name, "JsonWebTokenError");
    assert.match(err.message, /(audience|issuer)/i);
    return true;
  });
});
