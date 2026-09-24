# IRPT_BCKEND.TO-IB-rtr-2 -- BOTH VERIFIERS, THE FORBIDDEN CLAIMS + THE EXPIRY BOUND -- result

**Assignee:** `0.9.0_WK_IRPT_BCKEND~18` | **Round:** 18, cell `IB-rtr-2` (file suffix `IB-rtr-b`) | **PRD:** v0.17 @`4f942b7657` | **Rows:** `IRPT_BCKEND-C-S201`, `IRPT_BCKEND-C-S210`.

## What was built

1. **`infra/aws/users/lambda/portal-authorizer/index.mjs` (V2, modified).** CELL arm (a): a new
   `hasForbiddenRenderClaims(payload)` mirroring `render_auth.mjs`'s function exactly (`role==='admin' ||
   firmRole==='admin' || tier==='internal' || userType==='Dev'`), checked on the VERIFIED payload right
   after `jwt.verify` succeeds, before the route/path-id match. Not imported cross-package -- `portal-
   authorizer` and `auth-validator-edge` are separate Lambda deploy units with separate `node_modules` and
   separate build pipelines, so the shape is duplicated rather than adding a cross-package dependency (the
   task order's own instruction: "read `render_auth.mjs` for the exact shape, mirror it, do not diverge").
   CELL arm (b): `RENDER_MAX_TTL_SECONDS` (300) and `RENDER_SKEW_LEEWAY_SECONDS` (60) constants; a new
   `assertBoundedRenderExpiry(payload)` -- refuses a payload with no `exp` claim, and refuses an `exp` more
   than 300s past `iat`, both as STATIC checks on the claims themselves (never a runtime "has it exceeded
   now" check) -- called immediately after `jwt.verify` inside the same try block; `clockTolerance:
   RENDER_SKEW_LEEWAY_SECONDS` added to the `jwt.verify` call itself (previously unset, defaulting to 0,
   which would have made V2's skew behaviour diverge from V3's existing 60s). CELL arm (c): `jti` and
   `renderId` (identical values, per the minter's own `sub`/`jti` grammar -- confirmed by reading
   `infra/aws/lambda/investor-reporting/_render_identity/mint.py:110-111,170`) added to BOTH the accept log
   line ("Render token authorized") and the refusal log line ("Render token path id does not match its
   claim"), plus the two new refusal log lines (forbidden-claim, expiry-bound). CELL arm (d): no edit to the
   human JWT verification path (`getKeySlots`/`computeAllowedFirms`/`handler`'s try block) -- confirmed by
   `git show` on the commit: only `authorizeRenderToken` and its two new helper functions changed.

2. **`infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs` (V3, modified).** CELL arm (b): a new
   exported `RENDER_MAX_TTL_SEC` (300), `RenderExpiryBoundError` class (carries `.name` and `.jti`), and
   `assertBoundedRenderExpiry(payload, {maxTtlSec})` -- same two checks as V2's local function, called from
   inside `verifyRenderTokenWithSlots` immediately after `verifyWithSlots` succeeds, so the same 60s
   `clockTolerance` V3 already had is untouched (no widening) and the new bound runs on top of it. Arm (a)
   needed no change at V3: `hasForbiddenRenderClaims` already existed and was already wired into
   `evaluateRenderBranch` before this round's CVO finding (C-S201/C-S210 named ONLY V2 as accepting the four
   claims).

3. **`infra/aws/lambda-edge/auth-validator-edge/index.mjs` (V3, modified).** CELL arm (c): reading this
   file's CURRENT logging first (per the task order's explicit instruction, "do not assume") found the SAME
   gap the order named at V2, one level over: the `TokenExpiredError` refusal log line ("render_denied",
   reason "expired") carried `path` only, no `jti` -- every OTHER `render_denied`/`render_accepted` line in
   this file already carried `jti`. Fixed by an unverified `jwt.decode(token)` peek inside that catch arm
   (safe: the comment two lines above already establishes the signature verified against the render key
   before a `TokenExpiredError` can be thrown, so this is a faithful read, never a new trust decision). Also
   added a new catch arm for `e.name === "RenderExpiryBoundError"`, refusing with `reason: "expiry_bound"`
   and `jti: e.jti`, structurally parallel to the `TokenExpiredError` arm beside it. No edit to
   `_scope/resolve.py`, `_authz/enforce.py`, or the asset-allowlist/origin-marker logic (BOUNDS) -- confirmed
   by `git show`: only the two `catch` arms inside `evaluateRenderBranch` changed in this file.

4. **`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~18/
   test_v2_v3_forbidden_claims_and_expiry.mjs` (new file, 20 tests).** The criterion's own invocation file.
   Exercises the REAL `portal-authorizer/index.mjs` and REAL `auth-validator-edge/index.mjs` +
   `render_auth.mjs` against fixture RSA keypairs and synthetic events; no AWS call reached (V3's render-key
   path via `__setRenderKeySlotsForTest`; V2's via its own `IRPT_RENDER_JWT_PUBLIC_KEY_PEM` env-var seam;
   both verifiers' shared human-path `@aws-sdk/client-secrets-manager` dependency intercepted process-wide
   via `node:module`'s `registerHooks`, needed because the shared `jwtPublicKeys.mjs` has no `node_modules`
   anywhere in its own directory ancestry in a fresh worktree -- row `IRPT_BCKEND-W18-S1`, same underlying
   friction `IRPT_BCKEND-W15-S4` already documented).

## Criterion R118-AC2

**Invocation (exact, as named in the task order):**
```
cd deliverables/0.9.0_WK_IRPT_BCKEND~18 && node --test test_v2_v3_forbidden_claims_and_expiry.mjs
```
Run from `org/missions/D9/IRPT/IRPT_BCKEND/` (the task order's own directory), rc=0:

```
Render token carries a forbidden claim: {
  route: 'GET /api/scoped/investor-reporting/performance/{accountSetId}',
  jti: 'rnd_test_001',
  renderId: 'rnd_test_001'
}
... (4 forbidden-claim refusal logs, 1 accept log, 2 expiry-bound refusal logs with reason "expiry_bound",
    1 accept log, 1 "jwt expired" TokenExpiredError refusal log, then the human-path handler logs for the
    two V2 regression tests) ...
V ok forbidden-claim x4, positive control x1, expiry-bound x4 (missing exp, oversized exp, skew-inside,
  skew-outside) x2 verifiers = 8, logging x2, human-path regression x5

tests 20
suites 0
pass 20
fail 0
cancelled 0
skipped 0
todo 0
duration_ms 869.2132
```

**20 of 20 tests PASS, rc=0**, covering every named arm:
- **(a) V2 forbidden-claims -- 5 controls**: role=admin, firmRole=admin, tier=internal, userType=Dev each
  individually refused on an otherwise-admissible route; a clean token on the same route admitted (positive
  control).
- **(b) Expiry bound -- 8 arms (4 controls x 2 verifiers)**: no `exp` claim at all (refused, both); an
  oversized `exp` (1 hour from `iat`, NOT naturally expired by the clock -- proves the STATIC bound fired,
  not the runtime expiry check) (refused, both); `exp` 55s in the past (inside the 60s skew leeway, accepted,
  both); `exp` 65s in the past (outside the 60s leeway, refused, both).
- **(c) Logging**: V2's accept and refusal lines carry `jti`/`renderId`, never the raw JWT string or PEM
  content (regex-escaped exact-match assertion against the actual signed token and key text); V3's accept
  line and its (newly-fixed) expired-refusal line both carry `jti`, same no-leak assertion, plus the new
  expiry-bound refusal line.
- **(d) Human-path regression**: a human token is never classified as render-audience (V2); the full V2
  handler still authorizes an ordinary human token with byte-identical context fields; V2's admin bypass
  still computes `allowedFirmIds: 'ALL'`, unaffected by the render forbidden-claims check; V3's full handler
  still admits an ordinary human token on a benign path with the pre-existing header set; V3's admin bypass
  still injects its pre-existing headers.

**Controls (proof-of-spec `controls` object):**
- **Mutant 1:** V2's `hasForbiddenRenderClaims` temporarily forced to `return false` (nothing else changed).
  Re-run: `tests 20 / pass 16 / fail 4` -- exactly, and only, the four V2 forbidden-claim tests failed;
  every other test (V2 positive control, all 8 expiry arms, both logging tests, all 5 regression tests)
  still passed. Reverted (`git diff --stat` byte-identical to pre-mutant: 130 insertions/10 deletions across
  the three source files, matching the pre-mutant baseline exactly); re-run: `pass 20 / fail 0` again.
  FIRED-AS-EXPECTED.
- **Mutant 2:** V3's `assertBoundedRenderExpiry` temporarily replaced with a no-op `return;` (nothing else
  changed). Re-run: `tests 20 / pass 18 / fail 2` -- exactly, and only, the two V3 expiry-bound tests
  ("missing exp claim" and "oversized exp") failed; the two V3 skew-edge tests still passed (they depend on
  `jwt.verify`'s own `clockTolerance`, untouched by this mutant) and every other test still passed. Reverted
  (`git diff --stat` byte-identical again); re-run: `pass 20 / fail 0` again. FIRED-AS-EXPECTED.
- **Determinism:** the exact criterion invocation run 5+ times across this session (initial build; after
  fixing a console-capture serialization bug; the exact `cd deliverables/... && node --test ...` form from
  the task order's own directory; after each mutant revert; the final run after both commits landed, cited
  above). Every run: `tests 20 / pass 20 / fail 0`, rc=0. No flakiness: every fixture is an in-process RSA
  keypair (`crypto.generateKeyPairSync`) or a synthetic event object; the skew-edge tests use fixed
  `Date.now()`-relative offsets (55s/65s, not a sleep), with a comfortable margin either side of the exact
  60s boundary. STABLE.

## Surprises filed (non-blocking, kept working per BOUNDS)

- **`IRPT_BCKEND-W18-S1`** -- a fresh worktree carries no `node_modules` anywhere in the shared
  `jwtPublicKeys.mjs`'s own directory ancestry, so its bare `import('@aws-sdk/client-secrets-manager')`
  fails before any fixture can run; the SAME underlying gap row `IRPT_BCKEND-W15-S4` already documented on
  this project (there resolved via a repo-root `bun install`; here via a `cp -r` of the same package's
  already-installed `node_modules` from the main workspace checkout, LOCAL TEST EXECUTION ONLY, nothing
  committed). class OBSERVATION, hazard_standing INERT, not self-graduated.

## BOUNDS discipline

- No Secrets Manager entry, SSM parameter, AWS API call, or Lambda deploy -- code + tests only, fixture
  keypairs, synthetic requests.
- No edit to the human `aud`/`iss` verification path at either verifier -- confirmed by `git show` on both
  commits: only each verifier's render-only branch and its own new helper functions changed.
- No edit to any existing test's expected value -- no pre-existing test file exists for either verifier in
  the tracked tree at cells IB-rtr-1/IB-rtr-2/IB-rtr-3's shared surface; every assertion in this cell's new
  test file is new.
- No edit to `_scope/resolve.py`, `_authz/enforce.py`, or the asset-allowlist/origin-marker logic in
  `render_auth.mjs` -- confirmed by `git show`: this cell's `render_auth.mjs` diff touches only the new
  expiry-bound block (arm (b)); `isRenderAdmissibleUri`, `RENDER_API_PATH_PATTERNS`, `applyRenderHeaders` and
  every URI-admission/header-injection line are untouched.
