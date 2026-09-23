# FE-s-89 -- fixture-key grammar reconciliation (C-S147) -- result

**DISCLOSURE FIRST.** Three mechanical criteria were run exactly as the task order names them.
F89-AC1 and F89-AC3 PASS. **F89-AC2 FAILS as literally invoked**: the order's own invocation
(`cd WS/portal && bun __tests__/fe-s-89/verify-key-validity.mjs`) names a path relative to the
PORTAL ROOT, but this order's own BOUNDS Grant lists only the nested
`portal/src/pages/InvestorReporting/__tests__/fe-s-89/` -- no top-level `portal/__tests__/` entry
anywhere, and no such directory has ever existed in this repo (0 of 220 tracked
`__tests__/` files sit at portal root; `git log --all -- '__tests__/*'` is empty). Writing a
second copy of the checker at the literal path to make the invocation resolve would be a write
outside this order's own Grant, which the order elsewhere forbids in the same breath ("Never edit
outside the task order's `<paths>`"). Per instruction I did not paraphrase the invocation and did
not widen my write grant to make it pass; I built the substantively correct checker at the
GRANTED path (byte-identical logic, same file), ran BOTH the granted-path invocation (PASS, exact
target denominators) and the literal ordered invocation (FAIL, `Module not found`), and filed
`IRPT_FNTEND-W39-S1` documenting the conflict. **This order's `<status>` is therefore NOT flipped
to `complete`** -- not every mechanical criterion is PASS-by-output. A second surprise row,
`IRPT_FNTEND-W39-S2`, documents that the C-S147 bare-prefix-key defect this order names on four
files also exists, unrepaired, on 23 OTHER committed fixture files entirely outside this order's
grant -- found while reading every consumer per the order's own HOW step 1, not touched.

## What was done

**Four fixture files, two remedy shapes, all choosing remedy (a) (concrete migration)** -- verified
safe per-file by reading every real consumer before choosing, per the order's own mandate.

1. **`fixtures/smoke/reporting-answer-bearing.json`** and
   **`__tests__/fe-s-84/fixtures/reporting-qualified.json`** (hand-edited, not generator-owned):
   the `performance/` and `holdings/` bare-prefix keys became concrete --
   `performance/3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b` and
   `holdings/3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b`. That value is the
   SAME `permitted_account_set_fingerprint` both files' own `directory/resolve` entry already
   carries. **Verified this is not a guess:** `portal/src/api/endpoints/investor-reporting.ts`
   (`getPerformanceReport`/`getHoldingsSnapshot`, `:995-1057`) binds `accountSetId` to
   `req.scopeFingerprint`, and `contracts/adapt.ts:718,735` binds `scopeFingerprint` to
   `wire.permitted_account_set_fingerprint` off the `directory/resolve` response -- so for any real
   consumer of these two files, the app's own performance/holdings request necessarily targets
   this exact fingerprint, matching `default.json`'s own already-migrated pattern (the task
   order's named model). The only real consumer of `reporting-answer-bearing.json` outside
   ad-hoc CVO probes is `__tests__/fe-s-84/report-scroll-exercise.test.ts` (a real-browser
   dev-server exercise, gated ABSENT->SKIP, not touched by this change's shape); `reporting-qualified.json`'s
   only committed reference is inside the round-14 CVO's own probe scripts (not a `*.test.ts`
   consumer). Neither depends on any OTHER concrete account id.

2. **`fixtures/smoke/fe-s-13-wire.json`** (9 keys) and **`fixtures/smoke/fe-s-14-print-v1.json`**
   (2 keys) -- **generator-owned, fixed at the source** per the order's stated preference.
   `__tests__/fe-s-13/gen-corpus.ts`'s `generateSmokeMap()` and `generatePrintMap()` built their
   keys as hand-typed bare prefixes (`` `${base}/performance/` ``, etc.); `generatePublishedMap()`
   (which writes `default.json`, untouched, read-only) already built CONCRETE, bound keys via
   `irBuildRequest(operation, { pathParams })`. Added one shared helper, `boundKeyFor(operation)`,
   using the exact same binding, and switched both functions to it -- so the generator can never
   again regenerate a truncated-prefix key for these two files.

## Proving the regenerated output (the generator-owned pair)

Built `__tests__/fe-s-89/regen-generator-owned-fixtures.mjs`: intercepts the REAL, now-fixed
`gen-corpus.ts`'s filesystem writes (same write-interception technique the round-14 CVO's own
`IRPT_FNTEND_ROUND14_OBJECT_PROBE_20260922.mjs` used) so the run touches NOTHING on disk except
the two files this cell owns. Result (`f89_ac2...` logs and the run below):

- `default.json` (READ-ONLY to this cell): the generator's captured, in-memory output for it is
  **byte-identical to the git blob at HEAD** (`git show HEAD:.../default.json`) -- 16465 bytes,
  exact match. (A raw disk-bytes comparison first read as MISMATCHED, 594 bytes longer on disk --
  `core.autocrlf=true` means the working-tree copy carries CRLF while the generator and the git
  blob both carry LF, one `\r` per line, nothing else different; comparing against the git blob
  resolved this.) **default.json was NEVER written by this run; the check is diagnostic only, per
  the order's explicit "do not regenerate over it."**
- `fe-s-13-wire.json` and `fe-s-14-print-v1.json`: the captured in-memory bytes from the real,
  fixed generator were written verbatim to those two files (no hand-transcription) --
  `f89_ac2_key_validity_granted_path.log` shows the resulting key-validity read.
- The request-corpus directory (`fixtures/wire/requests/*.request.json`, outside this cell's
  grant) was never written -- writes intercepted, captured, discarded.

## Criteria

**F89-AC1** -- `cd WS/portal && timeout 180 bun run typecheck; echo rc=$?` -> `rc=0`. PASS.
(`f89_ac1_typecheck.log`)

**F89-AC2** -- ordered invocation FAILS (see disclosure); substantively-correct checker at the
granted path reads:
```
default.json: 12 of 12
reporting-answer-bearing.json: 3 of 3
reporting-qualified.json: 3 of 3
fe-s-13-wire.json: 9 of 9
fe-s-14-print-v1.json: 2 of 2
```
All five files hit their target denominators exactly (see `f89_ac2_key_validity_granted_path.log`).
The checker extracts the REAL, unmodified `checkKeyValidity`/`routeKeyCandidates` source out of
`scripts/ui-smoke.mjs` (read-only, round 14's classifier, untouched) and evaluates it -- same
technique as the CVO's own round-14 classifier probe -- so it cannot silently diverge from the
production instrument.

**F89-AC3** -- `cd WS/portal && timeout 600 bun test src/pages/InvestorReporting` ->
`661 pass / 27 skip / 0 fail`, rc=0. PASS. (`f89_ac3_whole_suite.log`) No currently-passing test
that consumes any of the five fixture files stopped passing.

**F89-AC4** (judgment, RECORDED, no verdict given):

- **Classifier strictness unweakened.** `checkKeyValidity`/`routeKeyCandidates` in
  `scripts/ui-smoke.mjs` were never touched (git diff on that file for this cell: empty).
- **Declared-key validity vs. exercised request fulfilment, kept as two separate figures, never
  conflated.** F89-AC2's numbers are pure KEY-VALIDITY (static, per the segment matcher). A LIVE
  render was separately exercised, against the real dev server (port 6011, this worktree,
  verified with curl before trusting it; stopped before F89-AC3, port verified closed at 000
  afterward):
  - **Positive control** (`f89_answer_bearing_after_positive_control.png`,
    `scripts/ui-smoke.mjs investor-reporting ... --fixtures .../reporting-answer-bearing.json
    --expect-text '[data-slot="answer-state"]::Ready'`): `EXPECT-TEXT: PASS`,
    `FIXTURES-MATCH: matched 3 of 3`, `KEY-VALIDITY: 3 of 3 valid consumed.ts operation keys` --
    the Reporting tab genuinely renders "Ready" from the real network fetch, not merely from a
    classifier count.
  - **Negative control, proving the fix is discriminating, not coincidental**
    (`f89_wrong_account_negative_control.png`): the SAME fixture with `performance/` pointed at a
    deliberately WRONG account id (`WRONG-ACCOUNT-ID-NOT-THE-FINGERPRINT` instead of the real
    fingerprint) -> `EXPECT-TEXT: FAIL`, `FIXTURES-MATCH: matched 2 of 3`,
    `FIXTURE-DEAD (declared, NEVER matched): /api/scoped/investor-reporting/performance/WRONG-ACCOUNT-ID-NOT-THE-FINGERPRINT`.
    This is exactly the risk the order named explicitly ("a test that requests a DIFFERENT
    account ... will stop matching") -- reproduced deliberately here to prove the chosen concrete
    value is the one the real app actually requests, not a lucky guess.
  - **Print-route finding (recorded, not a regression):** probed `fe-s-14-print-v1.json` against
    the real `/investor-reporting/print` route with a synthetic render-claim token (same technique
    as the CVO's round-14 browser probe). `PrintEntry.tsx:107-108` reads `scopeFingerprint =
    params.get('scope')` -- the print route's accountSetId is the CALLER-SUPPLIED `?scope=` query
    value, not the `directory/resolve` fingerprint the reporting tab uses. My concrete key
    (bound to the fingerprint, matching `default.json`'s own model) therefore did not match a
    synthetic probe using an arbitrary `?scope=scope-1` -- exactly the substring-match risk the
    order names, and NOT a regression: no currently-committed automated test exercises
    `fe-s-14-print-v1.json`'s URL-matching behaviour at all (its only committed consumers are
    `gen-corpus.ts` itself, `fe-s-85/verify-git-object.mjs`, and `fe-s-81/...test.ts`, all of which
    check data SHAPE, never URL matching -- confirmed by reading each; F89-AC3's 0 fail already
    proves this). No single concrete value is canonically "correct" for this file under the
    print route's caller-supplied-scope design; the generator's own binding convention
    (the fingerprint, matching every other route table entry) is the least-arbitrary choice and
    is what this fix applies, consistent with the order's instruction to model `default.json`'s
    already-migrated pattern.
- **Generator-owned regeneration survives a re-run** (the order's own CVO-sourced requirement):
  proved above, with `default.json` provably untouched.

## Surprises filed

- `IRPT_FNTEND-W39-S1` (BLOCKING, INERT) -- F89-AC2's invocation path lies outside this order's
  own BOUNDS Grant; order defect, not a code defect. Order's `<status>` stays open on this
  criterion.
- `IRPT_FNTEND-W39-S2` (OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~F`) -- 23 OTHER committed
  InvestorReporting fixture files, entirely outside this order's grant, carry the identical
  bare-prefix-key defect this order names on 4 files. Not touched (out of grant); named so the
  class, not just this order's subset, is visible to whoever owns the next C-S147 remedy.

## Push state

LOCAL only. Workspace and portal commits are both on this worker's own branches; nothing pushed.
