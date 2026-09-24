# RESULT -- `IRPT_BCKEND.TO-IB-rtl-1`: the capture tool, fourth repair -- the invariant guarded at the write boundary, not a point in the lifecycle

**Worker:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtl-1.the-capture-tool-invariant-guard-at-the-write-boundary.md`.
Design direction is `1.0.0_SA_CTO`'s own (round-11 analysis @`23d5fe2e6b`), executed verbatim as this
cell's arms (a)-(f), not re-derived.

## Arm (a) -- baseline reproduction, before touching source

`3.0.0_SA_CVO~B`'s round-11 lifecycle diagnostic (`IRPT_BCKEND_R11_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs`), run
UNCHANGED against the UNCHANGED source: `reproduced=true`. By observed writes/success, not name alone:
case "storage wait foreign hop then portal" (C-S170) showed `writes=1, success=true` -- a foreign
navigation during the `storageState()` await still resulted in a write. Case "non-navigation foreign
response" (C-S171) showed `writes=0, success=false, exitCode=1` -- a foreign-origin subresource wrongly
latched a terminal refusal. Also confirmed row `W13-S1`'s carried finding: cases "same-origin HTTP 404 then
clean" and "same-origin non-timeout navigation error then clean" both showed `writes=1, success=true` --
the pre-repair implementation silently retried both, which arm (d) must close. The round-10, round-9 and
round-8 diagnostics, run unchanged, reproduced RESULTS arrays byte-identical to `IB-rtk-1`'s own saved
post-repair baselines -- no drift since that round, no STOP row needed. Saved as
`IB-rtl-1_baseline_r{11,10,9,8}_*.json`, committed at `fd643dfeba`.

## Arms (b)-(d) -- the repair

**`infra/aws/ec2/investor-reporting-export/capture-session.cjs`, committed at `cb6429dc9e`:**

- **(b) The invariant, guarded at the write boundary.** `context.storageState()` (main(), the line reading
  `const rawState = await context.storageState();`) is now called with NO stored latch check preceding it
  and its result captured to MEMORY; `refuseIfLatched()` runs IMMEDIATELY AFTER that await resolves -- the
  first point any navigation admitted during the capture could be seen. The write is now ATOMIC: a temp
  file (`${statePath}.tmp`) via `fs.writeFileSync`, then `fs.renameSync` to the final path (guarded by
  `typeof fs.renameSync === 'function'`, degrading to a direct write ONLY on the minimal two-method `fs`
  stub every upstream read-only diagnostic exposes -- same fail-mode idiom the observer already uses for
  `page.on`; in production, Node's real `fs` module always exposes `renameSync`). Immediately after the
  rename, the latch is checked AGAIN; if set, `fs.unlinkSync` deletes the just-written file (best-effort)
  and the run throws, printing the cause. The timing of any navigation can no longer matter, because the
  check follows the last await that could possibly admit one -- proven at BOTH named timing windows: R11's
  own case 1 (during the `storageState()` await: now refuses, was accepting) and this worker's own
  `harness_ib_rtl_1.cjs` (immediately after the rename: refuses, `unlinks==1`, `deleted==true`).
- **(c) The observer narrowed to main-frame navigations, both paths.** `createLifetimeObserver`'s
  `onResponse` previously had no `isNavigationRequest()` filter (unlike `onRequest`, which already had
  one) -- a foreign-origin subresource response (image/font/analytics/CDN script) wrongly latched a
  terminal refusal even though the page itself never navigated away. `onResponse` now reads the response's
  own `request().isNavigationRequest()` and returns early for a non-navigation event, exactly mirroring the
  request-path filter. Proven by R11's case 3 (foreign subresource: now succeeds, was refused) alongside
  case 4 as the unaffected control (an actual foreign main-frame navigation: still refuses).
- **(d) The retry taxonomy, closed.** `readinessRefusal` (bare reason string, every reason equally
  retryable) replaced by `readinessOutcome` (`{ready, retryable, cause}`), preserving every existing check
  and its ORDER unweakened (status, password, per-hop origin/sign-in-path, final-URL origin/sign-in-path,
  marker) -- only the retry-vs-terminal classification is new. `main()`'s retry loop now retries EXACTLY
  three named causes: a timeout (classified from the `page.goto()` rejection's message via `/timeout/i`),
  an HTTP 5xx, and marker-absent-after-load (one bucket covering every "not yet signed in" symptom -- a
  password field showing, an on-origin sign-in-path redirect, or the marker itself absent -- since all are
  the same underlying condition and all retry the same way, proven by R11's case 10, "same-origin password
  screen then clean": retries once, succeeds, `verificationCalls==2`). An HTTP 4xx, a generic non-timeout
  navigation error, or any origin-hop `readinessOutcome` itself discovers is now a TERMINAL refusal on
  FIRST occurrence -- proven by R11's cases 8 and 9 (404, generic error): both now `success=false,
  writes=0, verificationCalls==1, storageCalls==0` (never retried, was `writes=1, success=true` at
  baseline).

## Arm (e) -- the regression and the two discriminating pairs

All reproduced by `battery_ib_rtl_1.py --arm invariant` (R112-AC1, token
`IBR112-INVARIANT-GUARD-BOTH-DEFECTS-REFUSE-TWINS-SUCCEED`) and `--arm retry` (R112-AC2, token
`IBR112-RETRY-TAXONOMY-CLOSED-CODE-README-AGREE`), both rc=0, output committed as
`R112-AC1_final_output.txt` / `R112-AC2_final_output.txt`.

- R11, unmodified, against the repaired source: `reproduced=false`; all 11 of 11 cases match the
  post-repair intent table (denominator printed by the battery: 11 of 11).
- R10, unmodified: `reproduced=false` (C-S158/C-S159 stay fixed, unaffected by this round); all 6 cases
  match `R10_INTENT`.
- R9, unmodified: externally-visible verdict (`success`, `writes`) unchanged for all 6 cases versus this
  round's own pre-repair baseline; 5 of 6 byte-identical. The sixth case ("verification foreign hop returns
  control") now refuses on the FIRST verification attempt via `readinessOutcome`'s own redirect-hop check
  (terminal, not retryable) instead of exhausting all 5 attempts as `NOT_AUTHENTICATED` -- an intended
  strengthening consistent with BOUNDS ("a foreign-origin hop is NEVER retryable under this taxonomy or any
  other framing"), filed as row `W13-S5` for the grader to confirm.
- R8, unmodified: byte-identical to this round's own pre-repair baseline (its plain-object page mock
  exposes no `.on()`, so the observer never attaches and nothing in this round touches its code paths).
- **Pair (i), invariant-timing:** extracted from R11's own cases 0/1 (during-`storageState()`-await
  timing) PLUS this worker's own `harness_ib_rtl_1.cjs`, built specifically because no upstream diagnostic
  models the post-rename timing window arm (b) also names, with a COMPLETE `fs` mock
  (`mkdirSync`+`writeFileSync`+`renameSync`+`unlinkSync`, unlike every upstream diagnostic's two-method
  stub) so the repaired source's real temp-file-then-rename path actually executes. GOOD (clean, no hop):
  writes+renames, succeeds, zero unlinks. BAD (foreign hop the instant after the rename): writes+renames,
  then caught, unlinked, refused (`unlinks==1, deleted==true, diskFinal==false`).
- **Pair (ii), subresource-scope:** extracted from R11's own cases 2/3 (GOOD: foreign-origin
  non-navigation resource, now succeeds) versus case 4 (BAD: an actual foreign-origin main-frame
  navigation, still refuses, unaffected by arm (c)).
- Retry-taxonomy proof (`--arm retry`): the three named causes (HTTP 500, timeout, missing marker, plus the
  password-screen symptom of the same marker-absent-after-load bucket) each retry once and succeed on a
  clean second attempt (`verificationCalls==2, storageCalls==1`); HTTP 404 and a generic non-timeout
  navigation error each terminally refuse on the FIRST occurrence (`verificationCalls==1, storageCalls==0,
  prompts==1`), cause printed to stderr, never retried. README.md's new prose subsection ("The invariant,
  and the retry taxonomy") names the same three causes verbatim, states the taxonomy is CLOSED at exactly
  three, and states the terminal side (4xx, generic error, foreign hop) is never retryable -- confirmed by
  the battery reading the file directly (3 of 3 causes found verbatim).

## Arm (f) -- the packet, then the publish: STOPPED this pass

`IB-rtl-1_NEVER_WIDEN_PACKET.md` written and committed, documenting the exact blast radius (ONE file,
`capture-session.cjs`), every hash git-object-derived per row `W13-S3`'s hash discipline (re-verified live
this session: a raw working-tree read of the SAME file produces a DIFFERENT, wrong sha256
`b6f266432e9c94002980316a6e97256d43b8ce11117281ade99e53b6bce232e0` versus the correct git-blob value
`b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`), and the rollback path.

**Censused this session, both halves absent:** `Glob` over
`org/tier1_exec/{1.0.0_SA_CTO,2.0.0_SA_COO~B}/deliverables/` for any filename containing `IB-rtl-1` --
0 of 0 found. `git log CLOUD -3` shows the shared branch's current tip is on an unrelated project
(`IRPT_FNTEND` round 12), confirming no cross-seat reference to this packet's blob exists anywhere
reachable from this worktree. Per the order's own arm (f): **"STOP here unless BOTH halves
(`2.0.0_SA_COO~B` and `1.0.0_SA_CTO`) are at HEAD naming this NEW packet's blob."** This worker therefore
does NOT open the deploy-ledger entry, does NOT publish to S3, does NOT update the README's expected-hash
line, and does NOT claim host-side or S3-side verification. **The host is STOPPED and this cell does not
start it -- no on-host readback exists here.**

One judgment call on the README, filed as row `W13-S4`: arm (d) requires the retry-behavior PROSE to exist
and agree with the code NOW (untied to publish state, and R112-AC2's own `<expect>` names it as gradable
this pass); arm (f) separately bundles "the README's retry-behavior and expected-hash lines" as updated
"in the SAME act as the publish." This worker read the two as governing DIFFERENT parts of the file: the
hash line literally asserts a sha256 of published S3 bytes (genuinely cannot be true before publish, left
untouched) while the new prose subsection describes repo code BEHAVIOR (true today; added now, in commit
`6c7713e1df`, ahead of the publish). `R112-AC3`'s grader can confirm or correct this reading; if corrected,
the remedy is a one-line revert of the prose subsection to a later, publish-bundled commit, with no change
to `capture-session.cjs` or the battery's own logic.

## Arm (f) ADDENDUM -- sixth invocation, publish-continuation pass (2026-09-22)

Both never-widen halves landed at HEAD naming this exact packet blob (`3676e2a26e8018c3ba91627f3df8fdd0b4a96cc7`)
-- `2.0.0_SA_COO~B`'s (`NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtl-1_CAPTURE_TOOL_FOURTH_PUBLISH.md`) and
`1.0.0_SA_CTO`'s (`NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtl-1_CAPTURE_TOOL_FOURTH_PUBLISH.md`). Both
re-derived independently this pass, before doing anything else: `git rev-parse HEAD:<packet path>` =
`3676e2a26e8018c3ba91627f3df8fdd0b4a96cc7`; `git rev-parse HEAD:<cjs path>` = `82abe68499ab1d5422f6f73979c3f5b72ed4c583`;
sha256 via both `git cat-file -p <blob> | sha256sum` and `git show cb6429dc9e:<path> | sha256sum` =
`b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`. All four values match both half files
exactly.

Arm (f) then executed in full:
1. **Ledger opened BEFORE the act** (`d31ff772b4`): `deploy_ledger.py open --slug irpt-rtl-1-capture-tool-publish`,
   1 leg (`L1`, s3-prefix), sentinel + `change_management` entry committed together.
2. **Publish**: extracted the git-blob bytes via `git cat-file -p HEAD:<path>` to a scratch file (never a raw
   working-tree read, per row `W13-S3`'s lesson), independently re-hashed BEFORE upload (matched the signed
   value, 28586 bytes), published via `s3api put-object` to
   `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/capture-session.cjs` (new VersionId
   `vLUlxFLiMvDtNnY5rH4Z6pGl4Slp9Man`).
3. **Readback**: `s3api get-object` to a SEPARATE scratch file, independently re-hashed the RETRIEVED bytes
   (not the CLI's own reported ETag/checksum, though those also happened to agree) -- sha256
   `b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`, exactly equal to both signed halves'
   value; `cmp` confirms the readback is byte-for-byte identical to the pre-upload payload.
   `capture-session.sh` confirmed unchanged (`head-object` VersionId `Z3NJuuiIxczhtYxGEsXW8ZqBpqYi1gs7`,
   `LastModified` predating this publish), correctly not republished.
4. **README updated in the SAME commit as the publish** (`acd048314f`): the step-2 "Expected output" hash
   line for `capture-session.cjs` now reads `b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`
   with its commit/cell citation changed to `cb6429dc9e` / `IB-rtl-1`.
5. **Ledger closed** (`acd048314f`): leg `L1` closed with the readback proof, entry `CLOSED`, sentinel removed.

The host (`i-0167fd745ad906a66`) stayed **STOPPED** throughout; this act did not start it and claims **NO
on-host byte verification** -- that remains the operator's own runbook step-2 re-read, unchanged from every
prior pass in this chain.

`R112-AC3` (judgment) is unaffected by this addendum and remains `3.0.0_SA_CVO~B`'s to grade; nothing in
arms (a)-(e)'s evidence above changed. The task order's `<status>` is flipped to `complete` in this same
pass, per the order's own `<proof_of_spec>` instruction, now that arm (f) has actually run.

## Surprises

Two rows filed this pass. `IRPT_BCKEND-W13-S4` (the README-timing reading above), class OBSERVATION,
hazard_standing INERT, disposition UNDER_INVESTIGATION. `IRPT_BCKEND-W13-S5` (R9's one case's internal-path
change under an unchanged external verdict), class OBSERVATION, hazard_standing INERT, disposition
UNDER_INVESTIGATION. See `../surprise-channel/investigations/INVESTIGATION_v1.md`.
