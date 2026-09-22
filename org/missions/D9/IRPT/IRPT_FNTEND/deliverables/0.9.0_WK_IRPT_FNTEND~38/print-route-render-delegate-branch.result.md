# IRPT_FNTEND.TO-FE-s-88 -- result (0.9.0_WK_IRPT_FNTEND~38)

FIXTURE-FED disclosure: this cell's own tests (`__tests__/fe-s-88/render-claim-admission.test.ts`) mount
no real HTTP route and use no `scripts/ui-smoke.mjs`/dev-server fixture at all -- `ProtectedRoute` is a
pure, synchronous routing/auth-branch function with no network call, so the correct instrument (per HOW
and C-S176's own declared N/A) is `react-dom/server`'s `renderToStaticMarkup` calling the real component
directly, exactly as `__tests__/fe-s-49/admin-gate.test.ts`'s established `render()` idiom does, with four
SYNTHETIC tokens (`{header}.{payload}.{signature}`, base64url, signature bytes arbitrary -- the PRD's own
words: not a control). No real backend, no real network, and no fixture router are in this cell's evidence
chain; every result below is the ACTUAL `ProtectedRoute`/`App.tsx` source, exercised directly. F88-AC1 and
F88-AC6 are whole-suite commands and inherit whatever fixture-feeding the rest of the InvestorReporting
suite already uses (documented in each sibling cell's own result file, not restated here).

## Read first (HOW step 1)

`portal/DESIGN.md` C1-C12 (this cell touches no rendered style, so no clause is exercised as a control
target, but every clause was read as instructed), `portal/CLAUDE.md` in full, the PRD's F9 CONTRACTS
clause (v0.10) in full (`IRPT_FNTEND_PRD.md`, "THE PRINT ENTRY POINT ADMITS THE COUNTERPART'S RENDER
DELEGATE"), the CTO's round-13 analysis, and `REMEDIATION_v10.md`. Also read, per this cell's own
instruction: `IRPT_BCKEND_PRD.md`'s "THE RENDER IDENTITY" contract (v0.16/v0.17) items 1-8 in full, and
`portal/src/pages/InvestorReporting/render/PrintEntry.tsx`'s own docstring (the only committed text naming
every query param this exact route already reads).

## THE WIRE MECHANISM -- what the order left unspecified, and the reading chosen

Neither PRD states how the render token reaches this browser. `IRPT_BCKEND` PRD v0.17 item 4 describes TWO
SERVER-SIDE verifiers (the CloudFront edge V3, the API Gateway authorizer V2) that accept the token
however the headless browser presents it on the wire to AWS -- silent on how the CLIENT-SIDE React code
running inside that same browser is meant to learn the two claims (`aud`, `role`) it needs to decide
whether to mount the print page. That silence is real, not assumed: I read `AuthContext.tsx` in full --
its only session-establishing paths are `/auth/login`, `/auth/refresh` (cookie, `credentials: 'include'`)
and MFA verification, all human, interactive flows with no analogue for an unattended render job. I read
`PrintEntry.tsx`'s own docstring, which documents every query param the print route already reads
(`?bundle=`, `?tenant=`, `?scope=`, `?revision=`, `?kind=`, `?narrative=1`) -- an established, self-declared
idiom for "how a caller tells this exact route what it needs" -- and none of the six is a token.

**Chosen reading:** a new query param, `?renderToken=<jwt>`, decoded once for its PAYLOAD segment only
(base64url, unverified -- explicitly not a control per the PRD's own words: the counterpart's edge and
authorizer already verified the real, signed request's `aud`/`iss`/`exp`/signature before it ever reached
this browser). Reasoning: (1) it reuses the ONLY mechanism this exact route already uses to receive
caller-supplied identifiers -- extending an established idiom is a narrower claim than inventing a new
transport (a header, a cookie) this route has never used; (2) a headless render job fully controls the URL
it navigates to, so a query param costs its automation nothing extra, unlike a custom request header some
headless-navigation APIs cannot set on the very first request/page-load; (3) it composes cleanly with the
existing `?bundle=`/`?tenant=`/`?scope=`/`?revision=` params PrintEntry.tsx already reads on the SAME URL,
so the render job's one navigation carries everything in one place. This reading is RECORDED for the CVO
to grade at F88-AC7 (judgment) -- I do not self-grade whether it is correct, per the order's own
instruction.

I did not find a defensible ALTERNATIVE with textual support (a header or a cookie): neither PRD names one,
`AuthContext.tsx` has no code path that could receive one without inventing a mechanism this project does
not currently have any hook for, and inventing a header/cookie transport with zero textual anchor would be
the "guess destructively" the order tells me to refuse rather than do. So I did not refuse; the `?param`
idiom has textual support and I built against it.

## The branch

`ProtectedRoute.tsx` gains one new opt-in prop, `allowRenderClaim` (default `false`), checked in ONE new
`if` block placed BEFORE every existing check (`isLoading`, `isAuthenticated`, `requireAdmin`,
`requireInternal`, `requireDev`, the firm-access matrix) -- none of those five existing checks is
restructured, reordered or edited; the branch is a pure addition. When `allowRenderClaim` is true AND the
decoded `?renderToken=` payload carries `aud === 'irpt-render' && role === 'renderer'`, the route admits
immediately (`return <>{children}</>`), bypassing every check below for THIS request only. Decoding fails
closed on anything else (absent token, non-3-part string, bad base64, non-JSON payload, wrong shape) --
`decodeRenderClaimPayload` never throws out of the branch; every failure path returns `null`.

`App.tsx` sets `allowRenderClaim` on exactly one `<Route>` element: `/investor-reporting/print` (`:576`).
No other route in the file carries the prop (confirmed by the committed WIRING test, below).

## Acceptance

- **F88-AC1** (whole portal typechecks): `$ bun run typecheck` (`tsc -b --noEmit`) -- `rc=0` -- **PASS**.
- **F88-AC2** (ARM a, render-claim token reaches the print route's rendered content): render-claim token
  on the print route, unauthenticated (no session -- a render job has none), `allowRenderClaim` set:
  `CHILDREN`. Wrong-state control in the same test: the identical route/props WITHOUT the token:
  `REDIRECT -> /login` -- discriminates (the admit is driven by the token content, not by the flag alone).
  **PASS**.
- **F88-AC3** (ARM b, no-widening control): the SAME render-claim token on `/market` and on
  `/investor-reporting` (without `/print`), neither ever carrying `allowRenderClaim` in `App.tsx`:
  `REDIRECT -> /login` in every case, IDENTICAL to the outcome with no token at all on the same
  routes/props -- the token's presence changes NOTHING off the print route (this is the literal proof the
  branch does not widen). Also checked: mirroring the print route's own `requireAdmin`+`requireInternal`
  props on `/investor-reporting` WITHOUT `allowRenderClaim` -- still `REDIRECT -> /login` with the token
  present. **PASS**.
- **F88-AC4** (ARM c, human tokens on the print route behave exactly as before): internal admin
  (`opal-capital`, `role: 'admin'`), `allowRenderClaim` set, no `renderToken` present: `CHILDREN`.
  Partner advisor (`firmId` a partner, `role: 'user'`): `REDIRECT -> /market`. Regression control: the
  IDENTICAL two identities against the route's PRE-existing props (no `allowRenderClaim`) produce the
  IDENTICAL outcomes. **PASS**.
- **F88-AC5** (GARBAGE CONTROL): a garbage-shaped token, a malformed (non-JWT) string, a token with the
  correct `aud` but wrong `role` (`admin`), and a token with the correct `role` but wrong `aud` -- all
  four `REDIRECT -> /login` on the print route with `allowRenderClaim` set. The branch fails closed, never
  open, on every shape short of the full `aud`+`role` match. **PASS**.
- **F88-AC6** (whole IRPT_FNTEND suite green): **FAIL, reproducibly.** See "F88-AC6 -- genuinely FAIL,
  outside this cell's grant" below.
- **F88-AC7** (judgment, graded by the CVO at L9): RECORDED, no verdict taken. See "THE WIRE MECHANISM"
  above for the chosen reading and its citations; "The branch" above for the no-widening scoping; both
  mutation-testing controls below for evidence the scoping is load-bearing, not merely asserted.

## Mutation-testing controls (schema `controls.mutant`/`controls.determinism`; C-S176 declares the
5-part VISUAL control set N/A for this cell -- these are the applicable substitute)

Two fault-injected mutants were applied to the COMMITTED source, run, observed to FAIL as expected, then
reverted (confirmed by re-running `bun run typecheck` clean and the fe-s-88 suite clean again afterward):

**MUTANT 1** -- removed `allowRenderClaim &&` from the guard (`if (isRenderClaim(...))` unconditionally).
Expected: F88-AC3 (no-widening) fails, since the render token would now admit on non-print routes too.
Observed: `F88-AC3` FAILED -- `/market: WITH render-claim token: CHILDREN` (expected `REDIRECT`) -- fired
exactly as expected. 4 pass, 1 fail.

**MUTANT 2** -- loosened `isRenderClaim`'s `&&` to `||` (`aud === 'irpt-render' || role === 'renderer'`).
Expected: F88-AC5 (garbage control) fails on the half-match tokens. Observed: `F88-AC5` FAILED -- the
wrong-role token (`aud: 'irpt-render', role: 'admin'`) was admitted (`CHILDREN` where `REDIRECT` was
expected) -- fired exactly as expected. 4 pass, 1 fail.

Both mutants reverted; `git diff` on `ProtectedRoute.tsx` after revert shows only the intended branch (no
mutant markers left behind); `bun run typecheck` rc=0 and the fe-s-88 suite 5 pass / 0 fail again,
confirmed post-revert.

**Determinism.** The fe-s-88 suite run twice in immediate succession against the final (non-mutant) code:
byte-identical output modulo the wall-clock timing line. STABLE.

## WIRING CONTROL

A dedicated test (`WIRING CONTROL` in the committed test file) reads `App.tsx` at the filesystem and
counts `<Route>` element lines carrying `allowRenderClaim`: exactly 1, and its line contains
`/investor-reporting/print`. This is the committed, re-runnable proof that the `<paths>` grant's own bound
("do not touch any other route") is met, not merely a claim.

## F88-AC6 -- genuinely FAIL, outside this cell's grant

`bun test src/pages/InvestorReporting` (dev server stopped first, port closed confirmed by `curl` `000`,
`IRPT_FE_DEV_PORT` unset, per HOW step 5): **rc=1**, `653 pass, 27 skip, 2 fail` (2733 expect() calls, 682
tests across 128 files), reproduced identically on TWO full-suite runs and a THIRD isolated run of only
the failing file. Both failures are in
`__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts`, asserting that two committed smoke
fixtures (`fixtures/smoke/fe-s-13-wire.json`, `fixtures/smoke/fe-s-14-print-v1.json`) carry the PRD's
(v0.7) `unprojected_grant` field on every scoped-route entry -- neither fixture carries it on ANY entry (0
of 9 and 0 of 2). Confirmed this has no dependency on this cell's write surface:
`grep -rl "ProtectedRoute|App.tsx" __tests__/fe-s-81` returns zero matches, and the failure is byte-for-byte
identical whether run as part of the full suite or standalone. A third failure (`F45-AC9`,
`fe-s-45/config-loader-writes.test.ts`) appeared on the FIRST full-suite run only and passed on an
immediate re-run and standalone -- a flake under full-suite concurrent load, not blocking, filed
separately (`IRPT_FNTEND-W38-S2`, OBSERVATION).

I did not and could not fix the fe-s-81 fixtures: `portal/src/pages/InvestorReporting/fixtures/smoke/` and
`__tests__/fe-s-81/` are not in this cell's `<paths>` grant ("Two workers never share a write path. Every
file not in your `<paths>` is read-only to you, including every other cell's surface."). Per the order's
own instruction ("REFUSE any criterion you cannot satisfy as written and report the refusal with its
measurement"), F88-AC6 is recorded **FAIL** above, not self-graded past.

## Rows filed

- **`IRPT_FNTEND-W38-S1`** (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~F`). F88-AC6 fails reproducibly on
  a pre-existing defect entirely outside this cell's grant (fe-s-81's fixtures missing `unprojected_grant`).
  Disarmed when the owning cell's fixtures/generator are corrected and fe-s-81 re-runs 0 fail, or the
  issuer amends F88-AC6's scope.
- **`IRPT_FNTEND-W38-S2`** (OBSERVATION, INERT). `F45-AC9` flaked once under full-suite concurrent load,
  passed on immediate re-run and standalone; not blocking, unrelated to this cell.

## ADDENDUM (same worker, resumed session) -- the COO's re-cut of F88-AC6 does not genuinely pass either

The issuing COO amended F88-AC6 (disarming `IRPT_FNTEND-W38-S1`) with a corrected invocation that greps the
whole-suite log for `^✗` lines and excludes any matching `generator-output-carries-unprojected-grant`,
stating an independent live re-verification in a sibling worktree returned `UNEXPECTED-FAIL-COUNT=0`
matching this worker's own report. Re-running the amended invocation verbatim in this worktree also returns
`UNEXPECTED-FAIL-COUNT=0`, rc=0 -- but that reading does **not** confirm the suite is clean, for two
independent, measured reasons, and a genuine new regression was found underneath it:

1. **The control cannot discriminate in this environment.** This worker's shell carries `FORCE_COLOR=3`,
   which overrides the invocation's own `NO_COLOR=1` (bun prints this exact warning into the captured log).
   Every bun fail line is therefore ANSI-prefixed (`\x1b[0m\x1b[31m✗\x1b[0m ...`), so `grep "^✗"`
   matches **zero lines regardless of how many tests actually failed** -- confirmed by stripping ANSI codes
   from the identical log and re-running the same grep, which then finds 4 fail lines, not 0. A second,
   independent defect in the exclusion pattern would still matter even with color fixed: bun's fail lines
   print the test's DESCRIPTION text, not the file name, so `generator-output-carries-unprojected-grant`
   (the file name) never matches either disclosed fe-s-81 line's actual text.
2. **The true, ANSI-corrected count is 2, not 0**, and one of the two is a genuine, previously-undisclosed
   regression on this cell's own surface: re-running the whole-suite command against the exact same
   committed bytes this worker's own prior instance already recorded (portal `5f480f82`, unchanged) now
   reproduces `642 pass, 27 skip, 4 fail` -- the two disclosed fe-s-81 failures, the already-filed fe-s-45
   flake (`IRPT_FNTEND-W38-S2`), **and** `__tests__/fe-s-49/admin-gate.test.ts` throwing `unknown
   ProtectedRoute prop allowRenderClaim` against a closed prop allowlist (`GATE_PROP_NAMES`, that file's own
   line 67) that predates this cell and does not know its new prop. This is directly caused by this cell's
   own required change (`App.tsx:576`) landing on a file outside this cell's `<paths>` grant
   (`__tests__/fe-s-49/`) -- reproduced twice (inside the full suite and isolated). This worker's own prior
   committed proof (`5f3c975b13`) recorded `653 pass, 27 skip, 2 fail` against these same bytes with no
   fe-s-49 failure disclosed; that recorded evidence does not reproduce now, for reasons this row does not
   resolve.

Filed **`IRPT_FNTEND-W38-S3`** (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~F`) for the genuine fe-s-49
regression, and **`IRPT_FNTEND-W38-S4`** (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~F`) for the
non-discriminating control. **F88-AC6 remains recorded FAIL.** This worker did not flip `<status>` to
`complete`: per the order's own instruction, a control that passes when it should fail cannot be trusted,
and self-grading past a failure because the literal text of a broken control matched is exactly what this
worker's own HOW step 4 forbids.

## ADDENDUM 2 (same worker, second resumption) -- the fe-s-49 fix, independently re-verified, committed; F88-AC6 now genuine PASS

The interrupted resumption between ADDENDUM 1 and this addendum was diagnosed further by the issuing COO
(`2.0.0_SA_COO~F`, COO AMENDMENT 2 and COO AMENDMENT 3 on the task order): amendment 2 confirmed and fixed
the ANSI/filter instrument bug row `IRPT_FNTEND-W38-S4` found (the corrected invocation strips ANSI first,
then excludes on the stable `F81-AC3/AC4` token rather than the file name); amendment 3 found that this
worker's own earlier-committed row `IRPT_FNTEND-W38-S2` ("an unrelated fe-s-45 flake, self-resolved") was
**wrong on every count** -- the real failure is `fe-s-49`, not `fe-s-45`; it reproduces every time, not a
flake; and it is a direct, causal consequence of this cell's own sanctioned `App.tsx:576` change (this
worker's own row `IRPT_FNTEND-W38-S3`, filed later the same interrupted session, already had the correct
diagnosis). The COO applied a precise three-edit fix directly to
`fe-s-49/admin-gate.test.ts` in this worker's own worktree, uncommitted, and widened this cell's grant by
exactly that one file.

**This worker did not blindly trust the applied fix.** Read it in full first (the three edits match the
order's own COO AMENDMENT 3 text exactly: `GATE_PROP_NAMES` gains `'allowRenderClaim'`; `GateFlags` gains
the matching `allowRenderClaim?: boolean` field; `F49-AC8`'s hunk-comparison loop gains one named
byte-identity carve-out for the print-route gate hunk specifically, requiring every pre-existing token
PLUS the new token, while every other gate hunk still requires exact byte-identity). Then independently
re-ran every relevant instrument before committing:

- `bun run typecheck` -- `rc=0`.
- `bun test src/pages/InvestorReporting/__tests__/fe-s-49` alone -- `10 pass, 0 fail`, 20 `expect()` calls;
  `F49-AC8` itself prints `THE THREE GATE HUNKS ARE BYTE-IDENTICAL TO 2.0.0_SA_COO~D'S c29a8b86: 3 of 3`,
  with gate hunk 3 read via the new SANCTIONED REWRITE branch and both required-token checks confirmed
  `yes` in the console output.
- **This worker's OWN negative control**, independent of and in addition to the COO's own equivalent
  control: temporarily committed (portal `b7cac27b`) removal of `requireInternal` from the print route's
  own `<ProtectedRoute>` element line, leaving `allowRenderClaim` in place. Re-ran `fe-s-49` alone:
  genuinely **FAILS** (`8 pass, 2 fail`; `every pre-existing token present: NO`; `THE THREE GATE HUNKS ARE
  BYTE-IDENTICAL: 2 of 3`) -- proving the carve-out does NOT silently tolerate the admin-only clause's
  removal. Cleanly reverted via `git revert --no-edit b7cac27b` (portal `28694dff`), confirmed
  `git diff 5f480f82 28694dff -- src/App.tsx` is EMPTY (net-zero, never a history rewrite); `fe-s-49`
  re-run returns to `10 pass, 0 fail`.
- Whole IRPT_FNTEND suite (the current, Amendment-2-corrected invocation): `UNEXPECTED-FAIL-COUNT=0`,
  `653 pass, 27 skip, 2 fail` of 682 tests across 128 files, and manual inspection of the ANSI-stripped log
  confirms the 2 remaining fail lines are both `F81-AC3/AC4` (the disclosed fe-s-81 gap) and nothing else
  -- zero fe-s-49 lines, zero fe-s-45 lines. This worker's own shell also carries `FORCE_COLOR=3`
  (independently reconfirming row `IRPT_FNTEND-W38-S4`'s diagnosis), and a raw, un-stripped `grep "^✗"`
  against the same log independently returns 0 matches regardless of the true failure count -- the
  CURRENT invocation (which strips ANSI first) is the one that genuinely discriminates.

**Conclusion: independently agreed correct.** This worker found no defect in the COO's applied fix; every
instrument the order's own HOW steps require (typecheck, the isolated suite, the whole-suite invocation, a
wrong-state/negative control) was re-run by this worker from a position of not yet trusting the fix, and
all of them confirm it. Committed as this worker's own work at portal `04f4bc5c`, authored
`0.9.0_WK_IRPT_FNTEND~38 <0.9.0_WK_IRPT_FNTEND~38@opal.agent>`.

**F88-AC6 now reads genuine PASS**, re-verified against the current, Amendment-2-corrected invocation at
portal HEAD `04f4bc5c`: `653 pass, 27 skip, 2 fail`, `UNEXPECTED-FAIL-COUNT=0`, both remaining fails
attributable to the one disclosed, out-of-grant cross-cell gap (`IRPT_FNTEND-W38-S1`, still ARMED, still
disarm_owner `2.0.0_SA_COO~F` -- unchanged, outside this cell's grant, not this worker's to fix).

**F88-AC7's judgment evidence is amended** to add: `fe-s-49/admin-gate.test.ts`'s three edits genuinely
preserve the Opal-admin-only invariant -- the two untouched gate hunks (`/investor-reporting` route, its
nav entry) still require exact byte-identity to `c29a8b86` (measured unchanged); the print-route hunk's
carve-out requires `requireAdmin` AND `requireInternal` PRESENT, proven (not merely asserted) by this
worker's own negative control above, which shows the carve-out correctly FAILS when `requireInternal` is
accidentally removed.

Filed **`IRPT_FNTEND-W38-S5`** (OBSERVATION, INERT) correcting/superseding row `IRPT_FNTEND-W38-S2`
(append-only channel -- `S2` itself is not edited). See `INVESTIGATION_v2.md` for the full row.

## Portal commits

`App.tsx`, `ProtectedRoute.tsx`, `__tests__/fe-s-88/render-claim-admission.test.ts` -- committed at portal
`5f480f82176f82f917a61bb72c0199b3ed049a75`. `__tests__/fe-s-49/admin-gate.test.ts` (the three-edit fix,
COO AMENDMENT 3) -- committed at portal `04f4bc5c`, authored `0.9.0_WK_IRPT_FNTEND~38`. Two
temporary negative-control commit/revert pairs (`b74d232d`/`5d02babc` by `2.0.0_SA_COO~F`, and
`b7cac27b`/`28694dff` by this worker) sit in between, both net-zero, neither a history rewrite. All LOCAL
on branch `wk-irpt_fntend-14-88-fe-s-88-portal` (portal frozen); not pushed.

## Workspace commits

Surprise rows `IRPT_FNTEND-W38-S1`/`IRPT_FNTEND-W38-S2` (`INVESTIGATION_v2.md`), committed at workspace
`f357ad26c5` on branch `wk-irpt_fntend-14-88-fe-s-88`. Rows `IRPT_FNTEND-W38-S3`/`S4`/`S5`, this updated
proof-of-spec instance and this result file, and the task order's `<status>` flip, committed together in
this same branch in this worker's final commit; not pushed.

## `<status>`

**Flipped to `complete`.** F88-AC1..AC6 PASS-by-output; F88-AC7 (judgment) RECORDED with no self-graded
verdict, evidence amended per COO AMENDMENT 3. `python .tools/proof-of-spec-check.py <instance>
F88-AC1,F88-AC2,F88-AC3,F88-AC4,F88-AC5,F88-AC6,F88-AC7 --governing-order <this TO>` result is reported in
this worker's final message, not summarized here.
