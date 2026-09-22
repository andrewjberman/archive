// IRPT_BCKEND.TO-IB-rtr-1 -- V3, THE ORIGIN MARKER + THE REAL ASSET ALLOWLIST.
// Criterion R118-AC1. Invocation (task order, verbatim):
//   cd deliverables/0.9.0_WK_IRPT_BCKEND~17 && node --test test_v3_origin_marker_and_assets.mjs
//   && node --test ../0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs
//
// Exercises the REAL `auth-validator-edge/render_auth.mjs` and `index.mjs`
// (unedited import, no test-only branch in production code) against fixture
// RSA keypairs and synthetic CloudFront viewer-request events, mirroring
// IB-rtq-3's own test harness shape (test_edge_render_delegate.mjs) so both
// suites share one proven pattern rather than inventing a second one.
//
// CELL (a)/(b): the origin-marker fix and its two controls.
// CELL (c): the GET-only check and its POST control.
// CELL (d): the real, config-derived asset allowlist and its controls.
//
// SURPRISE (filed IRPT_BCKEND-W17-S1, non-blocking, kept working): CELL's
// own suggested method ("git submodule update --init portal from the
// worktree root") FAILS in this worktree -- .gitmodules is a TRACKED,
// EMPTY (0-byte) file, so git reports "no submodule mapping found in
// .gitmodules for path 'portal'" (rc=128). This worker instead read
// portal/vite.config.ts at the gitlink's OWN pinned commit
// (15ceef793bda03c102539c209dde25cb18ab2eba, `git ls-files -s portal`)
// directly from the main workspace's independent portal checkout
// (`ajb_workspace/portal/.git`, which already holds that exact commit
// object -- confirmed via `git cat-file -e` before reading), via
// `git -C <main-workspace>/portal show <pin>:vite.config.ts` -- read-only,
// no write to any portal path, no submodule state created in this
// worktree. See that row for the full grounding.
//
// SURPRISE (filed IRPT_BCKEND-W17-S2, non-blocking, kept working): CELL (d)
// instructs deriving the allowlist from the config and CELL (e) plus
// BOUNDS both require IB-rtq-3's pre-existing 19-test suite to pass
// UNMODIFIED. `portal/vite.config.ts` at its pinned commit sets neither
// `base` nor `build.assetsDir` (Vite defaults apply, confirmed: exactly one
// vite.config* file in the tree, no `--base` flag in package.json's build
// script, and `infra/aws/terraform/portal-auth/cloudfront-distribution.tf`
// has NO path_pattern behaviour for `/investor-reporting/*` or `/assets/*`
// static files -- both fall through to the single DEFAULT "SPA static
// assets" cache behaviour, i.e. assets are served at Vite's own default
// public URL `/assets/*`, never under an `/investor-reporting/` prefix).
// So the REAL, narrowest, config-sourced allowlist is `/assets/*`, which
// is a DIFFERENT shape than IB-rtq-3's own test
// ("three-path admission: a static asset under /investor-reporting/ is
// admitted", uri `/investor-reporting/assets/app-9f3c1a.js`) assumed under
// W16-S2's own disclosed guess. Fixing CELL's own root-cause defect (an
// allowlist "assuming a URL prefix the real portal build does not use",
// this order's own one-line summary) NECESSARILY changes that guessed
// shape from admitted to refused. This worker cannot edit that file
// (BOUNDS: "NO edit to any EXISTING test's expected value ... only NEW
// test functions are added"; also outside this cell's <paths> grant,
// which names only `deliverables/0.9.0_WK_IRPT_BCKEND~17/`, never `~16/`).
// So R118-AC1's second invocation (`node --test
// ../0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs`) is measured,
// reported and graded HONESTLY below at 18 of 19 passing, rc=1 -- not
// forced green. This worker chose the REAL, config-derived fix over
// keeping the guessed-wrong test passing, because BOTH cannot be true at
// once once the real config is read, and CELL (d) is this cell's entire
// reason for existing (CVO C-S203 V3 half / W16-S2). The remedy for the
// stale test is a follow-on cell with write access to
// `deliverables/0.9.0_WK_IRPT_BCKEND~16/`.

import { test } from "node:test";
import assert from "node:assert/strict";
import { registerHooks } from "node:module";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

function genKeyPair() {
  return crypto.generateKeyPairSync("rsa", {
    modulusLength: 2048,
    publicKeyEncoding: { type: "spki", format: "pem" },
    privateKeyEncoding: { type: "pkcs8", format: "pem" },
  });
}

const renderKeys = genKeyPair();

// ---------------------------------------------------------------------------
// Intercept @aws-sdk/client-secrets-manager for this process, mirroring
// IB-rtq-3's own harness, so no test in this file can ever reach the
// network even incidentally via the human-path module graph.
// ---------------------------------------------------------------------------
const FAKE_SM_SRC = `
export class SecretsManagerClient {
  constructor() {}
  async send() { throw new Error("test fake SecretsManagerClient: no call expected in this suite"); }
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

const EDGE_DIR = "../../../../../../../infra/aws/lambda-edge/auth-validator-edge";
const EDGE_ABS_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), EDGE_DIR);

const { handler } = await import(`${EDGE_DIR}/index.mjs`);
const {
  __setRenderKeySlotsForTest,
  RENDER_PRINT_PATH,
  RENDER_STATIC_ASSET_PREFIX,
  isRenderStaticAssetUri,
  applyRenderHeaders,
} = await import(`${EDGE_DIR}/render_auth.mjs`);
const jwtModule = await import(`${EDGE_DIR}/node_modules/jsonwebtoken/index.js`);
const jwt = jwtModule.default;

__setRenderKeySlotsForTest({ current: renderKeys.publicKey, previous: null });

const RENDER_ISS = "opal-irpt-render";
const RENDER_AUD = "irpt-render";

function signRenderToken(overrides = {}) {
  const payload = {
    iss: RENDER_ISS,
    aud: RENDER_AUD,
    jti: "rnd_marker_001",
    sub: "render:rnd_marker_001",
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

// ===========================================================================
// (a)/(b) THE ORIGIN MARKER, THE ROOT CAUSE + ITS TWO CONTROLS
// ===========================================================================

test("MISSING-marker control: the PRE-FIX render_auth.mjs (this order's own parent commit, 7a55a7327d) never injects X-Origin-Verify -- reproduces the ORIGINAL bug", async () => {
  // Read the PRE-FIX blob straight from git (the commit this worktree was
  // cut from, per this order's own IDENTITY AND WORKTREE section), write it
  // to a throwaway file OUTSIDE the repo tree, and dynamically import it --
  // a genuine before/after comparison, not a re-assertion of the fix alone.
  const preFixSrc = execFileSync(
    "git",
    ["show", "7a55a7327d:infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs"],
    { cwd: path.resolve(EDGE_ABS_DIR, "../../../.."), encoding: "utf8" }
  );
  assert.ok(!preFixSrc.includes("x-origin-verify"), "sanity: the pre-fix blob must not already contain the fix");

  // Written INSIDE the real edge directory (same depth as the live file, not
  // an unrelated tmp dir) so its own relative import
  // ("../../lambda/lib/authkeys/jwtPublicKeys.mjs") resolves exactly as it
  // did for the real pre-fix commit; deleted in `finally` so nothing
  // untracked survives this test run.
  const tmpFile = path.join(EDGE_ABS_DIR, `.render_auth_prefix_${process.pid}.mjs`);
  fs.writeFileSync(tmpFile, preFixSrc, "utf8");
  try {
    const preFix = await import(pathToFileURL(tmpFile).href);
    const request = { headers: {} };
    preFix.applyRenderHeaders(request, { jti: "x", firmId: "f", delegator: "d", bundle: "b", revision: "r" }, {
      userRoleKey: "x-user-role", userRoleName: "X-User-Role", advisorRoleKey: "x-advisor-role",
    });
    assert.equal(request.headers["x-origin-verify"], undefined, "PRE-FIX code must NOT inject X-Origin-Verify (reproduces the original bug)");
  } finally {
    fs.rmSync(tmpFile, { force: true });
  }
});

test("MISSING-marker control, live code: the FIXED applyRenderHeaders DOES inject X-Origin-Verify=cloudfront, in the human path's own shape", () => {
  const request = { headers: {} };
  applyRenderHeaders(request, { jti: "x", firmId: "f", delegator: "d", bundle: "b", revision: "r" }, {
    userRoleKey: "x-user-role", userRoleName: "X-User-Role", advisorRoleKey: "x-advisor-role",
  });
  assert.deepEqual(request.headers["x-origin-verify"], [{ key: "X-Origin-Verify", value: "cloudfront" }]);
});

test("MISSING-marker control, full handler: a genuine render-admit request now carries X-Origin-Verify on the forwarded request", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-origin-verify"), "cloudfront");
});

test("SPOOFED-marker control: a client-supplied X-Origin-Verify (wrong value) is OVERWRITTEN by the verified constant, never passed through", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({
    uri: RENDER_PRINT_PATH,
    token,
    extraHeaders: {
      "x-origin-verify": [{ key: "X-Origin-Verify", value: "SPOOFED-NOT-CLOUDFRONT" }],
    },
  }));
  assert.equal(isRefusal(result), false);
  assert.equal(headerValue(result, "x-origin-verify"), "cloudfront", "the verified constant must win over any client-supplied value");
});

test("SPOOFED-marker control, unit-level: applyRenderHeaders overwrites a pre-existing x-origin-verify key on the request object", () => {
  const request = { headers: { "x-origin-verify": [{ key: "X-Origin-Verify", value: "SPOOFED" }] } };
  applyRenderHeaders(request, { jti: "x", firmId: "f", delegator: "d", bundle: "b", revision: "r" }, {
    userRoleKey: "x-user-role", userRoleName: "X-User-Role", advisorRoleKey: "x-advisor-role",
  });
  assert.equal(headerValue(request, "x-origin-verify"), "cloudfront");
});

// ===========================================================================
// (c) GET-ONLY, WITH A POST CONTROL
// ===========================================================================

test("GET-only: a GET to the print route with a valid render token is admitted (positive control)", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token, method: "GET" }));
  assert.equal(isRefusal(result), false);
});

test("GET-only: a POST to an otherwise-admissible render URI, with an otherwise-valid render token, is refused BY THE BRANCH", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token, method: "POST" }));
  assert.equal(isRefusal(result), true, "a POST on the render branch must be refused, not forwarded");
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token only admits GET");
});

test("GET-only: a POST to one of the three admissible render API URIs is also refused", async () => {
  const token = signRenderToken();
  const uri = "/api/scoped/investor-reporting/performance/acctset123";
  const result = await handler(makeEvent({ uri, token, method: "POST" }));
  assert.equal(isRefusal(result), true);
  assert.equal(result.status, "401");
  const body = JSON.parse(result.body);
  assert.equal(body.error, "Render token only admits GET");
});

// ===========================================================================
// (d) THE REAL ASSET ALLOWLIST, DERIVED FROM portal/vite.config.ts
// ===========================================================================
// portal/vite.config.ts (pinned commit 15ceef793bda03c102539c209dde25cb18ab2eba,
// read via `git -C <main-workspace>/portal show <pin>:vite.config.ts`, since
// .gitmodules carries no mapping for 'portal' in this worktree -- see the
// filed surprise row): `defineConfig({ plugins: [react()], cacheDir: ...,
// resolve: { alias: {...} }, build: { rollupOptions: {...},
// chunkSizeWarningLimit: 600 }, server: {...} })` -- NEITHER `base` NOR
// `build.assetsDir` is set anywhere in that object, and no second
// `vite.config*` file exists in the tree (`git ls-tree -r --name-only
// <pin> | grep vite.config` -> exactly one hit: vite.config.ts).
// package.json's build script ("tsc -b && vite build --configLoader
// runner") passes no `--base` override. Vite's own default public URL for
// a built asset is therefore `<base>` + `<assetsDir>/` = `/` + `assets/` =
// `/assets/` (https://vite.dev/config/build-options.html#build-assetsdir).
// Corroborated independently:
// infra/aws/terraform/portal-auth/cloudfront-distribution.tf carries no
// path_pattern behaviour for `/investor-reporting/*` or `/assets/*`
// static files -- both fall through to the single DEFAULT "SPA static
// assets" cache behaviour (comment ":270"), so nothing in the CloudFront
// config scopes a build's assets to any route-specific prefix either.

test("real asset allowlist: the print route itself is still admitted", async () => {
  const token = signRenderToken();
  const result = await handler(makeEvent({ uri: RENDER_PRINT_PATH, token }));
  assert.equal(isRefusal(result), false);
});

test("real asset allowlist: the DERIVED real asset path shape (/assets/<hash>.<ext>, Vite's own default) is admitted", async () => {
  const token = signRenderToken();
  const uri = "/assets/index-49a2f1c8.js";
  assert.equal(isRenderStaticAssetUri(uri), true, "unit check: matches the config-derived prefix+extension rule");
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), false, "a real Vite-built asset path must be admitted, not refused");
  assert.equal(headerValue(result, "x-user-role"), "renderer");
});

test("real asset allowlist: a non-JS/CSS/etc file directly under /assets/ (wrong extension) is still refused", async () => {
  const token = signRenderToken();
  const uri = "/assets/README.md";
  assert.equal(isRenderStaticAssetUri(uri), false);
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), true);
});

test("real asset allowlist: an UNRELATED URI outside the assets prefix entirely is refused (negative control)", async () => {
  const token = signRenderToken();
  const uri = "/unrelated/nothing-here.js";
  assert.equal(isRenderStaticAssetUri(uri), false);
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), true, "an unrelated root path must never be admitted");
  assert.equal(result.status, "401");
});

test("real asset allowlist: the OLD guessed shape (/investor-reporting/assets/*) is now correctly REFUSED -- it is not a real Vite build output path", async () => {
  const token = signRenderToken();
  const uri = "/investor-reporting/assets/app-9f3c1a.js";
  assert.equal(isRenderStaticAssetUri(uri), false, "the pre-round-18 guessed prefix must no longer be admitted -- it is not derivable from portal/vite.config.ts");
  const result = await handler(makeEvent({ uri, token }));
  assert.equal(isRefusal(result), true);
});

test("RENDER_STATIC_ASSET_PREFIX exports the exact derived value", () => {
  assert.equal(RENDER_STATIC_ASSET_PREFIX, "/assets/");
});
