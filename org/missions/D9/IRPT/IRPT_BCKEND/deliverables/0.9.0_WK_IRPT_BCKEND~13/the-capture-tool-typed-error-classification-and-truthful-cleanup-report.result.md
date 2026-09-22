# RESULT -- `IRPT_BCKEND.TO-IB-rtm-1`: the capture tool, fifth repair -- typed error classification and truthful cleanup reporting

**Worker:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtm-1.the-capture-tool-typed-error-classification-and-truthful-cleanup-report.md`.
Design direction is `1.0.0_SA_CTO`'s own (round-12 analysis @`a8d306eb71`), stated as this cell's
arms (a)-(g), the bar restated as four finite invariants rather than re-derived.

## Arm (c) -- baseline reproduction, before touching source

All five diagnostics (R12, R11, R10, R9, R8) run UNCHANGED against the UNCHANGED
IB-rtl-1-repaired source (blob `82abe68499ab1d5422f6f73979c3f5b72ed4c583`, HEAD before this
cell's edits). R12's own two counterexamples reproduced exactly as the order states: case "same
non-timeout certificate error, timeout substring in URL text" showed `writes=1, success=true`
(C-S179: a certificate error wrongly retried because its message contains "timeout"); cleanup
case "same latched rename, deletion fails EPERM" showed `deleted=false, diskFinal=true` but the
printed message still claimed "the file ... was deleted" (C-S180: untruthful). R11, R10, R9, R8
diagnostics, run unchanged, produced results arrays BYTE-IDENTICAL to `IB-rtl-1`'s own saved
post-repair baselines -- no drift, no STOP row needed. Saved as `IB-rtm-1_baseline_r{12,11,10,9,8}_*.json`.

## Arms (a)-(b) -- the repair

**`infra/aws/ec2/investor-reporting-export/capture-session.cjs`, committed at `227763d734` then
`b809df14d5`:**

- **(a) Typed classification, C-S179.** The verification `page.goto()` catch block's
  `/timeout/i.test(msg)` (a substring search over the error's message text, matching "timeout"
  ANYWHERE) is replaced by `error.name === 'TimeoutError'` (Playwright's own error class) OR
  `isOwnDeadlineMessage(msg)` -- an EXACT-STRING equality check against the one deterministic
  message Node/Playwright's own internal deadline mechanism produces for THIS tool's OWN
  configured `GOTO_TIMEOUT_MS` (60000, now a named constant shared by both `page.goto()` calls).
  Neither a regular expression nor a substring search over free text: a message merely
  CONTAINING "timeout" (e.g. a certificate failure on a URL carrying `?timeout=1`) can never
  equal the fixed deadline string. Proven by R12's own counterexample case, now terminal
  (`writes=0`, was `writes=1`), and this worker's own `harness_ib_rtm_1.cjs` pair (i).

  **Judgment call, filed as row `IRPT_BCKEND-W13-S6`, not self-graduated:** arm (a) names TWO
  paths to a timeout classification -- `error.name === 'TimeoutError'` OR "the tool's own
  deadline firing" -- and this worker MEASURED that implementing ONLY the first (name-only)
  regresses two long-standing reference diagnostics' own genuine-timeout positive controls (R11's
  "same-origin timeout then clean" case and R12's "actual timeout positive control"), because
  every upstream CVO diagnostic's mock (read-only, inherited across four prior repair rounds)
  throws a plain `Error()` for a simulated timeout and never sets `.name` -- unlike real
  Playwright. This worker's resolution implements arm (a)'s own second named clause as an EXACT
  match against this tool's own configured deadline message, which closes C-S179's counterexample
  AND avoids the regression (both empirically verified, see arm (d) below). The CVO's R113-AC3
  judgment is the oracle for whether this reading of "the tool's own deadline firing" holds the
  four-invariant bar's third item.

- **(b) Truthful cleanup reporting, C-S180.** The post-rename latch recheck's cleanup path
  previously swallowed an `unlinkSync` throw (`catch (e) { /* best-effort */ }`) and always
  printed the SAME "was deleted" message regardless of whether deletion actually succeeded. Now
  the deletion outcome is tracked: a genuine `unlinkSync` failure prints `ERROR: session file
  could NOT be removed: <path> (<errno>) -- delete it manually before any use`, exits the new
  `CLEANUP_FAILURE_EXIT_CODE` (4, distinct from the generic refusal's exit 1), and the file
  REMAINS on disk -- never claims deletion that did not happen. Proven by R12's own EPERM
  counterexample case, now truthful (`deleted=false, diskFinal=true, exitCode=4`, message names
  removal failure), and this worker's own `harness_ib_rtm_1.cjs` pair (ii). No reading ambiguity
  here -- the CVO's own diagnostic mock fully and faithfully exercises this fix.

Neither change touches any existing S125/S126/S127/C-S153/C-S158/C-S159/C-S170/C-S171 check.
README.md updated (commit `1473f3ec4a`) to name the new exit code, the required manual step, and
the typed-classification behavior -- prose describing repo code BEHAVIOR (true today), the same
reasoning `IB-rtl-1`'s row `W13-S4` established; the step-2 expected-hash line was left untouched
at that commit, deliberately (arm (g)'s own design: the line must not assert bytes S3 does not yet
hold). **It was updated in the SAME commit as the publish once arm (g) completed** -- see below.

## Arm (d) -- acceptance: all five diagnostics post-repair, both single-difference pairs

Reproduced by `battery_ib_rtm_1.py --arm classify` (R113-AC1, token
`IBR113-TYPED-CLASSIFICATION-BOTH-DEFECTS-REFUSE-TWINS-SUCCEED`), rc=0, output committed as
`R113-AC1_final_output.txt`.

- R12, unmodified, against the CURRENT COMMITTED blob (`058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae`,
  git-object-derived via `git rev-parse HEAD:<path>`, cross-checked `git cat-file -p | sha256sum`
  vs `git show HEAD:<path> | sha256sum`, agreeing): the C-S179 counterexample now TERMINAL
  (`writes=0, success=false, verificationCalls=1`); the actual-timeout positive STILL RECOVERS
  (`writes=1, success=true, verificationCalls=2`); the HTTP 404 control stays terminal; the
  C-S180 counterexample now TRUTHFUL (`deleted=false, diskFinal=true, exitCode=4`, message names
  the removal failure, never claims deletion); the clean positive controls for both arms
  unaffected.
- R11, unmodified, against the same blob: ALL 11 cases' externally-visible verdict
  (success/writes/exitCode/verificationCalls/prompts/storageCalls) UNCHANGED from this round's
  own pre-repair baseline -- zero behavioral regression. The ONE byte-level difference (10 of 11
  cases byte-identical) is a COSMETIC addition of an `(error.name=...)` annotation to an
  already-terminal case's error message text, not a behavioral change.
- R10, R9, R8, unmodified: results arrays BYTE-IDENTICAL to this round's own pre-repair baseline
  -- zero drift.
- **Pair (i), typed classification:** this worker's own `harness_ib_rtm_1.cjs`, since neither
  upstream diagnostic isolates a single-difference pair with the discriminating property named.
  GOOD (genuine `TimeoutError`, message "Timeout 60000ms exceeded"): retries once, recovers
  (`writes=1, success=true, verificationCalls=2`). BAD twin (SAME general shape -- a message that
  ALSO contains the substring "timeout", specifically a certificate failure on a URL carrying
  `?timeout=1` -- but `error.name` is NOT `TimeoutError` and the message does not exactly match
  the tool's own deadline format): terminally refuses (`writes=0, success=false,
  verificationCalls=1`). Discriminating property: error TYPE (name, or an exact match against
  this tool's own configured deadline message), never a keyword search anywhere in the message.
  Verified as a NEGATIVE CONTROL against the pre-repair blob (`82abe68499ab1d5422f6f73979c3f5b72ed4c583`):
  the pair correctly reports `pairIOk=false` (the BAD twin wrongly retries under the old
  `/timeout/i` regex), proving the pair genuinely discriminates.
- **Pair (ii), truthful cleanup:** this worker's own `harness_ib_rtm_1.cjs`, same narrowest
  post-rename timing window `IB-rtl-1`'s own harness modeled. GOOD (unlink succeeds): file
  removed, old-style refusal message, exit 1. BAD twin (SAME hop, unlink mocked to throw EPERM):
  file REMAINS on disk, new truthful-failure message, exit code 4. Discriminating property:
  whether the delete call itself succeeded. Also verified as a negative control (`pairIIOk=false`
  against the pre-repair blob: the old code's untruthful "was deleted" message and generic exit
  code).

## Arm (e) -- the four-invariant bar, restated for this proof

(i) No bytes on disk unless the latch is clear after the in-memory capture -- UNCHANGED from
`IB-rtl-1`, re-verified not regressed (R11's cases 0/1, R10/R9/R8 byte-identical, this worker's
own harness pair (ii) proving the post-rename window still guards correctly). (ii) Only
main-frame navigation to a foreign origin latches -- UNCHANGED from `IB-rtl-1`, re-verified not
regressed (R11's cases 2/3/4 unchanged). (iii) Retry only the three TYPED causes, classified by
type never by message text -- this cell's arm (a), `error.name === 'TimeoutError'` or an exact
match against this tool's own configured deadline message; HTTP 5xx read structurally from the
response status (unchanged, `readinessOutcome`); marker-absent-after-load is the tool's own
readiness result (unchanged). (iv) Every failure is truthfully reported -- this cell's arm (b),
the cleanup path now tracks and reports the true deletion outcome.

## Arm (f) -- metadata fixes, no publish replay

**C-S174** (`IRPT_BCKEND.TO-IB-rtk-1`'s proof instance, `controls.mutant.observed`): the text
called the packet's original stated value `fffef738...` "a transcription error in the packet
only", which understated what actually happened. Corrected: `fffef738e90cf03fbb20cdfbeb8cbb310e3a44c6eee657974f8a3eeb92e8e35b`
is the EXACT, correctly-computed sha256 of `capture-session.cjs`'s CRLF/checkout-grain
WORKING-TREE bytes on this box (row `W13-S3`); `f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d`
is the git-object's own LF-bytes sha256, the PUBLISHED value. Both are real, correctly-computed
sha256 values of two DIFFERENT byte sequences of the same logical file; neither is a typo.
Committed at `1914e80595` then `f9c83f851f` (battery check refinement). `proof-of-spec-check`
re-run: VALID rc=0, no criterion verdict changed.

**C-S187** (`IRPT_BCKEND.TO-IB-rtl-1`'s proof instance): the `result.md` artifact row was still
pinned to commit `c33e9f3d38` (blob `0d19277bfd64bf63fbd79d1be1b5a41867c3d435`) -- the PRE-PUBLISH
snapshot. Re-pinned to the true HEAD blob `4c5a60d2c063209de915d7ca142f9f8877f3cc95` at commit
`d8bac06b89` (the commit that added the sixth-invocation publish-continuation addendum), verified
via `git rev-parse HEAD:<path>`. The `declared_exclusions` entry that blanket-claimed "any real
host/SSM/S3 action" never occurred was narrowed to "host start/stop, live login, credential, MFA
automation" for arms (a)-(e)'s fifth-pass code-only work, since arm (f)'s sixth pass DID perform
a real S3 `put-object`/`get-object` (documented in the `capture-session.cjs` artifact row's
`DEPLOYED-VERIFIED` state). Committed at `1914e80595`. `proof-of-spec-check` re-run: VALID rc=0,
no criterion verdict changed.

`battery_ib_rtm_1.py --arm metadata` (R113-AC2, token `IBR113-METADATA-C174-C187-CORRECTED`),
rc=0, output committed as `R113-AC2_final_output.txt`.

## Arm (g) -- the packet, then the publish: COMPLETED this pass (continuation)

`IB-rtm-1_NEVER_WIDEN_PACKET.md` written and committed (blob `db092cbd5124d61e1fc633d75e0ce07f6a4c9aae`),
documenting the exact blast radius (ONE file, `capture-session.cjs`), every hash git-object-derived
(`git cat-file -p <blob> | sha256sum`, cross-checked with `git show HEAD:<path> | sha256sum`, agreeing),
and the rollback path. A prior pass STOPPED here because both never-widen halves were absent (censused
via `Glob`, 0 of 0 found).

**This continuation pass:** both halves confirmed at HEAD naming this exact packet blob
(`org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtm-1_CAPTURE_TOOL_FIFTH_PUBLISH.md`,
`org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtm-1_CAPTURE_TOOL_FIFTH_PUBLISH.md`),
both independently re-derived by this worker this pass (`git rev-parse`/`cat-file`/`show`, matching each
half's own quoted values and each other exactly: packet `db092cbd5124d61e1fc633d75e0ce07f6a4c9aae`; cjs
blob `058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae`, sha256
`3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2`).

Deploy ledger `irpt-rtm-1-capture-tool-publish` opened BEFORE the S3 act (commit `65e015dd8a`), single
leg L1 (`s3-prefix`). Payload extracted via `git cat-file -p HEAD:<path>` to a scratch file and hashed
BEFORE upload (34785 bytes, sha256 matched the packet's table). Published via `s3api put-object` (new
VersionId `urBPlR5pfitAb30A8jGT_k4ivtjSAnFN`; prior IB-rtl-1 VersionId `vLUlxFLiMvDtNnY5rH4Z6pGl4Slp9Man`
retained, versioned bucket). Read back via `s3api get-object` to a SEPARATE scratch file and independently
re-hashed (NOT the CLI's own reported ETag/checksum, per the order's hash-instrument discipline) -- readback
sha256 `3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2` equals both signed halves' table
exactly and is byte-for-byte identical (`cmp`) to the pre-upload payload. `capture-session.sh` confirmed
unchanged via `head-object` (VersionId `Z3NJuuiIxczhtYxGEsXW8ZqBpqYi1gs7`, unmoved since `IB-rti-1`), not
republished. README.md's step-2 "Expected output" hash line updated to the new sha256 (and its commit/cell
citation to `b809df14d5` / `IB-rtm-1`) in the SAME commit as the publish (`14a8b2ab58`). Ledger leg closed
with the readback proof and the entry closed (`org/critical_paths/change_management/20260922T0811Z_irpt-rtm-1-capture-tool-publish_deploy_completion.md`
now reads CLOSED, all 1 leg proven). **The host (`i-0167fd745ad906a66`) is STOPPED throughout -- this act
does not start it and claims NO on-host byte verification**, exactly as the order's arm (g) anticipates;
that remains the operator's own runbook step-2 re-read.

`<status>` flipped to `complete` (commit `a442c9dc16`), per the order's own `<proof_of_spec>` instruction
(rc 0 AND R113-AC1 AND R113-AC2 PASS-by-output, in the same pass that completes the publish). `R113-AC3`
remains a JUDGMENT row, `UNVERIFIABLE-BY-INSTRUMENT`, left for `3.0.0_SA_CVO~B` -- not self-graded.

## Surprises

One row filed this pass. `IRPT_BCKEND-W13-S6` (the arm (a) error.name-only-vs-regression tension
and its resolution via arm (a)'s own "tool's own deadline firing" clause), class OBSERVATION,
hazard_standing INERT, disposition UNDER_INVESTIGATION, NOT self-graduated per the CTO's ruling
on row `S117` (repeated in this order's BOUNDS). See
`../surprise-channel/investigations/INVESTIGATION_v1.md`.
