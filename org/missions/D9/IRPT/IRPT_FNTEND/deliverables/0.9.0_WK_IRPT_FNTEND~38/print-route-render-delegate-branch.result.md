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

## Portal commits

`App.tsx`, `ProtectedRoute.tsx`, `__tests__/fe-s-88/render-claim-admission.test.ts`. Committed at portal
`5f480f82176f82f917a61bb72c0199b3ed049a75`, LOCAL on branch `wk-irpt_fntend-14-88-fe-s-88-portal` (portal
frozen); not pushed.

## Workspace commits

Surprise rows `IRPT_FNTEND-W38-S1`/`IRPT_FNTEND-W38-S2` (`INVESTIGATION_v2.md`), committed at workspace
`f357ad26c5` on branch `wk-irpt_fntend-14-88-fe-s-88`. This proof-of-spec instance and this result file
committed in the same branch, not pushed.

## `<status>`

**Left `pending`.** F88-AC1..AC5 PASS-by-output; F88-AC6 is a genuine, reproducible FAIL, caused by a
pre-existing defect entirely outside this cell's `<paths>` grant; F88-AC7 (judgment) RECORDED with no
self-graded verdict. Per the standing bar, a FAIL row leaves the order open -- a schema-VALID proof
instance is not a met order. `python .tools/proof-of-spec-check.py <instance>
F88-AC1,F88-AC2,F88-AC3,F88-AC4,F88-AC5,F88-AC6,F88-AC7 --governing-order <this TO>` result is reported in
this worker's final message, not summarized here.
