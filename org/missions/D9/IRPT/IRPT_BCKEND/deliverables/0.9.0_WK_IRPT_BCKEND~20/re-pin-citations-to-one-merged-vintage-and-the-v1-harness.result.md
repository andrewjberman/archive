# IRPT_BCKEND.TO-IB-rtr-4 -- RE-PIN CITATIONS + THE V1 HARNESS -- result

**Assignee:** `0.9.0_WK_IRPT_BCKEND~20` | **Round:** 18, cell `IB-rtr-4` | **PRD:** v0.17 @`4f942b7657` | **Base commit:** `7a55a7327d`.

## (a) Every `resolve.py` citation re-pinned, confirmed at the CURRENT merged tree

`infra/aws/lambda/investor-reporting/_scope/resolve.py`'s line-number citations into
`infra/aws/lambda-edge/auth-validator-edge/index.mjs` had drifted a SECOND time since round 17's
own "fix": `index.mjs` grew again (v13, IB-rtq-3's THE RENDER IDENTITY V3 edge branch landing as
part of round 18's `IB-rtr-1`/`IB-rtr-2`), a clean +110 lines above the injection block
(`400-408` -> `510-518`). Re-confirmed at THIS session's actual merged HEAD (never carried
forward from round 17's own citation, which the CVO already found wrong the same day it landed):

- `TRUSTED_HEADERS` (all nine): re-pinned to `index.mjs:510-518` (was `400-408`).
- `RENDER_TRUSTED_HEADERS` (all three render markers): IB-rtq-3's edge branch has now LANDED in
  this worktree (it had not at `IB-rtq-2`'s cut, row `IRPT_BCKEND-W15-S1`) -- measured this
  session: `applyRenderHeaders` in the NEW `render_auth.mjs` (a sibling cell's surface, read-only
  citation only, never edited) sets all three names at lines 210-212; `index.mjs` itself only
  calls it (`index.mjs:327`). Re-pinned to cite `render_auth.mjs:210/211/212`, replacing the
  PRD-paragraph fallback that table carried while the branch was unlanded.
- Every OTHER numbered citation in the module (the docstring's `index.mjs:135-136,:153-154,:162-163`
  for the ownership-map path/schema_version/advisors-claim sentence; `:186-187`/`:205` for the
  role='admin'-vs-firmRole passage, in BOTH the module docstring and `classify_principal`'s own
  docstring and return-value reason strings; `:188` for the "validator refuses these callers"
  reason string; `:161-171` for the schema-mismatch stop-the-line citation in `advisor_grant`)
  was independently re-verified against the current merged `index.mjs` and re-pinned where stale
  (`:155/:180/:419`, `:204-205`/`:225`, `:226`, `:180-191` respectively) -- the DELIVERABLE line
  says "every `resolve.py` citation re-pinned", not only the two allow-list tables, and this
  cell's `<paths>` grant is stated as "CITATION EDITS ONLY, never its logic": every edit made is a
  line-number correction inside a comment or an embedded reason string, never a change to any
  function's control flow or return TYPE/CLASS. Full before/after diff is in this cell's commit.

**Test reproduced BEFORE the fix** (citation drift, exactly the tripwire the test's own docstring
describes):
```
FAILED infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py::test_every_trusted_header_is_actually_injected_at_the_line_it_claims
AssertionError: ('x-user-email', 400, '        console.warn(JSON.stringify({')
```
**AFTER the fix, the full pre-existing `_scope` suite (29 tests, citation-drift test included)
passes in full** -- see criterion output below.

## (b) The durable 19-test baseline -- confirmed, unmodified

`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs`
(IB-rtq-3's 19 worker-authored tests, PINNED AT ITS MERGED COMMIT) was NOT touched by this cell
(confirmed: `git status --porcelain` on that path is empty throughout this session) and was run,
unmodified, against the CURRENT merged tree: **19 of 19 PASS**, rc=0 (output below). This is a
CONFIRMATION, not a new artifact, per the CELL's own text.

## (c) The V1 harness -- genuinely new, calls V1's OWN compiled code

`test_v1_actual_module_harness.mjs` (this cell's own deliverable, new file) imports
`infra/aws/opalinvest_dev/lambda/auth-handler`'s **compiled** `verifyAccessToken`
(`dist/jwt.js`, `tsc`-built from the project's own unmodified `tsconfig.json`) and calls it
directly -- never a re-implementation, never `jsonwebtoken.verify()` called directly (that was
`IB-rtq-3`'s own row `W16-S3` replication, which this cell is explicitly NOT repeating). Its
`getJwtVerifySlots()` -> `getJwtKeySlots()` key-retrieval dependency (Secrets Manager) is faked via
the SAME `node:module` `registerHooks` + `data:` URL technique `IB-rtq-3`'s own
`test_edge_render_delegate.mjs` already uses for its human-path regression tests -- no AWS API
call is ever reached.

**Why "V1's own code" means the COMPILED artifact, not raw `.ts` source** (measured this session,
filed as row `IRPT_BCKEND-W20-S2`, non-blocking): Node's native `--experimental-strip-types`
(default-on) is pure syntactic erasure, not type-checking. `jwt.ts` imports
`{ AccessTokenPayload, RefreshTokenPayload, User }` from `./types` WITHOUT `import type`, so a
bare strip-types run leaves that as a value import; `types.ts` is interfaces-only (zero runtime
exports), so the import throws `SyntaxError: does not provide an export named 'AccessTokenPayload'`
-- reproduced directly, is not fixable without editing `jwt.ts` (forbidden, read-only reference).
V1's own `package.json` (`"build": "tsc"`) and `tsconfig.json` (`"module": "commonjs"`) settle
what V1 actually ships: compiled CommonJS. `tsc` elides a type-only import entirely in commonjs
output (confirmed: `grep -c types dist/jwt.js` == 0), which is exactly why the compiled artifact
resolves where the raw source cannot. This harness therefore imports `dist/jwt.js` -- the SAME
bytes the deployed Lambda runs, unedited, compiled by the project's own unmodified build config.

**Four tests**, two arms plus two extra negative controls proving the harness discriminates
rather than refusing everything:
- **Positive control** (CELL (c)'s own requirement): a valid human token (portal-key-signed,
  correct `iss`/`aud`/algorithm) through the REAL `verifyAccessToken` is ACCEPTED, payload fields
  confirmed.
- **Negative control on the positive control's own fixture**: the SAME human-shaped payload signed
  by a THIRD, untrusted key is refused (`JsonWebTokenError`, "invalid signature") -- proves the
  positive control's acceptance is not vacuous (a function that accepts everything would also pass
  the positive-control assertion alone).
- **Refusal arm** (CELL (c)'s own requirement): a render-key-signed token through the REAL
  `verifyAccessToken` is REFUSED -- signature-stage `JsonWebTokenError`, "invalid signature",
  because it is verified against the (faked) portal public key, never the render key. This is
  `verifyAccessToken`'s OWN key-verification path rejecting it, not a replicated call.
- **A render-shaped token that ALSO carries the wrong `iss`/`aud`** (signed by the portal key, so
  it clears the signature check) is still refused, on the issuer/audience check -- confirms V1's
  defenses are independent, never a single point that a signature-only replication could miss.

**Two gitignored, uncommitted, out-of-`<paths>`-grant build prerequisites were needed to make V1's
source importable at all** (filed as row `IRPT_BCKEND-W20-S2`, non-blocking, same class as the
already-established ephemeral-`node_modules` precedent `IRPT_BCKEND-W15-S4`): auth-handler's own
build-time `src/lib/` mirror of `infra/aws/lambda/lib/` (its own `.gitignore` names this exact
mechanism, `build-nodejs-lambda.sh` rsyncs it in on every real build) and its `tsc` output
(`dist/`), plus the mirrored `.mjs` copied into `dist/lib/authkeys/` (`tsc`'s own
`include: src/**/*` does not copy a non-`.ts` file; the real Lambda packaging step does, outside
this cell's `<paths>`). Reproduction, run once, local-only, no AWS call, no deploy, no Terraform:

```
cd infra/aws/lambda-edge/auth-validator-edge && bun install
cd infra/aws/opalinvest_dev/lambda/auth-handler && bun install
mkdir -p infra/aws/opalinvest_dev/lambda/auth-handler/src/lib
cp -r infra/aws/lambda/lib/* infra/aws/opalinvest_dev/lambda/auth-handler/src/lib/
cd infra/aws/opalinvest_dev/lambda/auth-handler && ./node_modules/.bin/tsc.exe
mkdir -p infra/aws/opalinvest_dev/lambda/auth-handler/dist/lib/authkeys
cp infra/aws/opalinvest_dev/lambda/auth-handler/src/lib/authkeys/jwtPublicKeys.mjs \
   infra/aws/opalinvest_dev/lambda/auth-handler/dist/lib/authkeys/jwtPublicKeys.mjs
```
All four artifacts (`node_modules` x2, `src/lib/`, `dist/`) are `git status --porcelain
--ignored=matching`-confirmed `!!` (gitignored) and none is committed by this cell.

## (d) Isolated vs merged evidence, separated explicitly

- **`IB-rtq-2`/`IB-rtq-3`'s OWN isolated-worktree numbers** (their own result.md files, not
  re-quoted verbatim here) are their own SNAPSHOTS at their own cells' cuts and are now KNOWN
  STALE for the citation lines specifically (round 17's own "fix" of `400-408` was itself wrong by
  the time the CVO checked it the same day, per this order's own intro). They are not treated as
  current evidence anywhere in this result.
- **Everything reported above and in the criterion output below is measured by THIS cell, THIS
  session, against the CURRENT merged tree at branch tip** (see COMMITS in the worker report) --
  the only evidence this result treats as authoritative going forward.

## Criterion R118-AC4

**Invocation as named in the task order** (six `../` segments in the first leg):
```
cd deliverables/0.9.0_WK_IRPT_BCKEND~20 && py -3.12 -m pytest ../../../../../../infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py -v && node --test ../0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs && node --test test_v1_actual_module_harness.mjs
```
**Measured this session: that literal 6-dot path does not resolve** (`org/` has no `infra/`
child) -- `ERROR: file or directory not found`, pytest rc=4, collected 0 items. Filed as row
`IRPT_BCKEND-W20-S1` (non-blocking): the directory `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
0.9.0_WK_IRPT_BCKEND~20/` is measured 7 levels below the worktree root (confirmed by seven
sequential `cd ..`), not 6, so the invocation's first leg needs a SEVENTH `../`. The other two
legs (relative to the same starting directory, shallower) are unaffected.

**Corrected invocation, run from `org/missions/D9/IRPT/IRPT_BCKEND/` (this order's own directory,
same convention `IB-rtq-3`'s own result.md states for the same starting point):**
```
cd deliverables/0.9.0_WK_IRPT_BCKEND~20 && py -3.12 -m pytest ../../../../../../../infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py -v && node --test ../0.9.0_WK_IRPT_BCKEND~16/test_edge_render_delegate.mjs && node --test test_v1_actual_module_harness.mjs
```

**rc=0. Output (verbatim excerpt, each leg's summary line):**
```
Leg 1 (pytest, the real pre-existing _scope suite, citation-drift test included):
============================= 29 passed in 0.55s ==============================

Leg 2 (node --test, the 19-test durable baseline, IB-rtq-3's file, unmodified):
tests 19
pass 19
fail 0

Leg 3 (node --test, the new V1 harness, this cell's own file):
tests 4
pass 4
fail 0
```
**Denominator: 29 of 29 (pytest, including the re-pinned-citation test) + 19 of 19 (durable
baseline, unmodified) + 4 of 4 (new V1 harness) = 52 of 52 tests PASS across all three legs, rc=0
on the corrected chained invocation.** Re-run twice more this session (determinism control below)
-- stable both times.

## Controls (proof-of-spec `controls` object)

- **Mutant:** `TRUSTED_HEADERS["x-user-email"]`'s re-pinned citation temporarily reverted from
  `510` back to the stale `400` (nothing else changed). Re-run of
  `test_every_trusted_header_is_actually_injected_at_the_line_it_claims` alone:
  `AssertionError: ('x-user-email', 400, '        console.warn(JSON.stringify({')` -- FAILED, as
  expected (the exact same failure this cell reproduced before its fix). Reverted (diff confirmed
  clean against the intended state via `git diff --stat`, no stray change); re-run: PASSED again.
  **FIRED-AS-EXPECTED.**
- **Determinism:** the corrected full three-leg criterion invocation run 3 times total this
  session (once to establish the fix, once immediately after, once as an explicit determinism
  re-run) -- every run rc=0, 29/19/4 pass, 0/0/0 fail, no flakiness (fixture RSA keypairs and
  synthetic requests only, no network or timing dependency in any of the three legs). **STABLE.**

## Surprises filed (non-blocking, kept working per BOUNDS)

- **`IRPT_BCKEND-W20-S1`** -- R118-AC4's own invocation's first leg is one `../` short of repo
  root from the stated starting directory; the corrected 7-dot path is what this result and the
  proof_of_spec instance record and run. class OBSERVATION, hazard_standing INERT.
- **`IRPT_BCKEND-W20-S2`** -- V1's `verifyAccessToken` cannot be imported at all without two
  gitignored, uncommitted, out-of-`<paths>` build prerequisites (the `src/lib/` mirror and the
  `tsc` `dist/` build); neither exists in a fresh worktree; both were built locally, offline, and
  are not committed. class OBSERVATION, hazard_standing INERT.

Both are left for `3.0.0_SA_CVO`'s L9 adjudication, not self-graduated, per this order's own
BOUNDS instruction ("Do NOT self-graduate your own filed row").

## BOUNDS discipline

- No Secrets Manager entry, SSM parameter, AWS API call, or Lambda deploy -- code + tests only;
  the V1 harness's key-retrieval dependency is faked exactly as BOUNDS requires; the two build
  prerequisites (mirror copy, `tsc` compile) are local-only, offline, and touch no AWS surface.
- No edit to any existing test's expected value anywhere -- confirmed: `test_resolve.py` and
  `test_edge_render_delegate.mjs` are both byte-unmodified by this cell (`git status --porcelain`
  clean on both throughout); every assertion in `test_v1_actual_module_harness.mjs` is new.
- No edit to `render_auth.mjs`, `index.mjs`, `_authz/enforce.py`, or `portal-authorizer/index.mjs`
  -- confirmed: none touched. `render_auth.mjs` and `index.mjs` were read-only cited (for the
  re-pinned line numbers) and never edited.
- `resolve.py`'s only edits are line-number citations inside comments and embedded reason
  strings -- no function's control flow, return type, or return CLASS changed; every existing
  test that exercised those functions before this cell still exercises them identically after.
