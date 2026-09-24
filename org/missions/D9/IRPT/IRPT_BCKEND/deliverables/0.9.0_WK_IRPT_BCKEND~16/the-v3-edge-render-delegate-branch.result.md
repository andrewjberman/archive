# IRPT_BCKEND.TO-IB-rtq-3 -- THE V3 EDGE RENDER-DELEGATE BRANCH -- result

**Assignee:** `0.9.0_WK_IRPT_BCKEND~16` | **Round:** 17, cell `IB-rtq-3` | **PRD:** v0.17 @`4f942b7657` items 4 (V3 half), 8.

## What was built

1. **`infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs` (new file, 204 lines).** The render-key
   verification, URI-admission and header-injection logic: `getRenderKeySlots`/`__setRenderKeySlotsForTest`
   (mirrors `jwtPublicKeys.mjs`'s two-slot pattern, read-only import of `parseKeySlots`/`verifyWithSlots` --
   that module is never edited), `verifyRenderTokenWithSlots` (RS256, `aud=irpt-render`,
   `iss=opal-irpt-render`, 60s clock-skew leeway, the JWT library's own `exp` check), `hasForbiddenRenderClaims`
   (role=admin / firmRole=admin / tier=internal / userType=Dev), `isRenderAdmissibleUri` (the print route, the
   SPA static assets under `/investor-reporting/`, and the three API paths), and `applyRenderHeaders`
   (injects `X-User-Email`/`X-User-Role`/`X-Firm-Id`/`X-Render-Delegator`/`X-Render-Bundle`/`X-Render-Revision`,
   overwriting any client-supplied value of the same name, and deletes `X-Advisor-Id`/`X-Advisor-Role`/
   `X-User-Type` unconditionally).

2. **`infra/aws/lambda-edge/auth-validator-edge/index.mjs` (modified).** A `v13` changelog entry; the import
   of the five `render_auth.mjs` exports it needs; a new `evaluateRenderBranch(uri, token)` function
   (`:249-296` at this HEAD); and its call site inside `handler` (`:317-328`), placed immediately after token
   extraction -- **BEFORE** the human JWT verify (`:330`, `getJwtKeySlots()`/`verifyWithSlots`) and therefore
   before the admin-bypass evaluation (`isAdminBypass`, `:358-364`). This placement is deliberate and stated
   in-line: a render token is signed by a different key and would fail the human verify's signature check
   before ever reaching admin-bypass, so running the render branch after the human verify would make it
   unreachable for every genuine render token. `evaluateRenderBranch` returns one of three outcomes
   (`admit`/`refuse`/`not_render`); on `not_render` the handler falls through to the pre-existing code
   completely unchanged, byte-for-byte, from `:330` down.

3. **`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs`
   (new file, 448 lines, 19 tests).** The criterion's own invocation file. Exercises the REAL `handler` from
   `index.mjs` and the REAL `render_auth.mjs` against fixture RSA keypairs and synthetic CloudFront
   viewer-request events; no AWS call is ever reached (`@aws-sdk/client-secrets-manager` intercepted for this
   process via `node:module`'s `registerHooks`, a `data:` URL fake module, for the human-path regression
   tests; the render-key path uses `render_auth.mjs`'s own `__setRenderKeySlotsForTest` seam).

## Criterion R117-AC3

**Invocation (exact, as named in the task order):**
```
cd deliverables/0.9.0_WK_IRPT_BCKEND~16 && node --test test_edge_render_delegate.mjs
```
Run from `org/missions/D9/IRPT/IRPT_BCKEND/` (the task order's own directory), rc=0:
```
ℹ tests 19
ℹ suites 0
ℹ pass 19
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
```
19 of 19 tests PASS, covering every named arm:
- **Three-path admission** (5 tests): print route, a static asset under `/investor-reporting/`, and each of
  the three API paths (performance/sections/narrative) -- all admitted. A sixth test confirms an inadmissible
  URI on an otherwise-valid render token is refused **BY THE BRANCH ITSELF** (`Render token not admitted for
  this resource`), never falling through.
- **Header-injection-overwrites-client-supplied-values arm**: a request carrying spoofed
  `X-Firm-Id`/`X-User-Role`/`X-User-Email`/`X-Render-*` headers still shows the VERIFIED claim values on the
  outgoing request.
- **X-Advisor-* absence arm**: `X-Advisor-Id`/`X-Advisor-Role`/`X-User-Type` are asserted ABSENT (not merely
  unset -- deleted) even when the caller supplied fake values for them.
- **tier-internal/role-admin refusal arm (d)**: four tests (tier=internal, role=admin, firmRole=admin,
  userType=Dev) -- each refused BY THE BRANCH with `Render token carries a forbidden claim`.
- **Expiry (arm (c) first clause)**: an expired render token is refused via the JWT library's own
  `TokenExpiredError` (signature-verified-then-expired, proven distinguishable from "wrong key" by the
  library's own check order, `node_modules/jsonwebtoken/verify.js :162-192` at this HEAD).
- **V1 refusal confirmation (arm (e))**: a render-signed token fails V1's own read verify() parameters
  (issuer/audience/algorithm read from `auth-handler/src/jwt.ts:19-20,251-261`, never guessed) with a
  SIGNATURE-stage `JsonWebTokenError`, proven to precede the audience/issuer checks by reading
  `verify.js` directly. See surprise row `IRPT_BCKEND-W16-S3` for why this is a faithful replication rather
  than a direct TypeScript import.
- **Negative-widening regression control (arm (c) second clause, arm (f))**: 5 tests exercising the
  PRE-EXISTING human path through the REAL, unmodified handler -- a wrong-aud human token falls through and
  is admitted exactly as before (all standard headers, including the human path's own `X-Advisor-Id: ""`
  behaviour, which is the OPPOSITE of the render path's unconditional delete); missing-Authorization refusal;
  wrong-signature refusal; expired-human-token refusal; the pre-existing admin bypass still injects its
  pre-existing header set. See surprise row `IRPT_BCKEND-W16-S1` for why these regression tests live in this
  one file rather than a separate pre-existing suite (none was found).

**Controls (proof-of-spec `controls` object):**
- **Mutant:** `hasForbiddenRenderClaims` temporarily forced to `return false` (nothing else changed). Re-run:
  `pass 15, fail 4` -- exactly the four forbidden-claim tests failed, every other test (including the
  three-path admission, header-injection, expiry, V1 and all five regression tests) still passed. Reverted
  (byte-identical to the pre-mutant file, `diff` clean); re-run: `pass 19, fail 0` again. FIRED-AS-EXPECTED.
- **Determinism:** the exact criterion invocation run 3 times across this session (initial build, from the
  deliverables dir directly, and the exact `cd ... &&` form) plus once more after the mutant revert: every run
  `pass 19, fail 0`, rc=0, no flakiness (all fixtures are in-process RSA keypairs and synthetic events, no
  network or timing dependency). STABLE.

## Surprises filed (non-blocking, kept working per BOUNDS)

- **`IRPT_BCKEND-W16-S1`** -- no pre-existing edge-auth test suite/file exists anywhere in the tracked tree
  (measured: zero `*.test.mjs`/`*.spec.mjs`/`test_*.mjs` under `auth-validator-edge/`, zero `node:test` import
  anywhere in the repo). class OBSERVATION, hazard_standing INERT.
- **`IRPT_BCKEND-W16-S2`** -- the PRD/task-order never pin the SPA's static-asset path shape, and `portal/`
  (a gitlink) is not checked out in this worktree, so the actual build convention cannot be confirmed. A
  documented, conservative interpretation was implemented instead of a guess. class OBSERVATION,
  hazard_standing INERT.
- **`IRPT_BCKEND-W16-S3`** -- V1's real TypeScript module cannot be directly executed without either a live
  AWS call (BOUNDS-prohibited) or populating a directory outside this cell's `<paths>` grant; V1's own read
  verify() parameters were replicated against `jsonwebtoken` directly instead. class OBSERVATION,
  hazard_standing INERT.

All three are non-blocking judgment calls left for `3.0.0_SA_CVO`'s L9 adjudication, not self-graduated, per
the CTO's ruling on row S117 (repeated in this order's BOUNDS).

## BOUNDS discipline

- No Secrets Manager entry, SSM parameter, AWS API call, or Lambda deploy -- code + tests only, fixture
  keypairs, synthetic requests.
- No edit to V1, V4, V5, V6 or V7 -- confirmed: only `infra/aws/lambda-edge/auth-validator-edge/index.mjs`
  (modified) and `render_auth.mjs` (new) touch code; V1 was read-only cited, never imported for edit.
- No edit to any existing test's expected value -- no pre-existing test file was found (row
  `IRPT_BCKEND-W16-S1`); every assertion in `test_edge_render_delegate.mjs` is new.
- No edit to `_scope/resolve.py`, `_authz/enforce.py`, `portal-authorizer/index.mjs`, or the render-key minter
  module -- none touched.
