# RESULT -- `IRPT_BCKEND.TO-IB-rtk-1`: the capture tool, third repair -- one session-lifetime navigation observer, a terminal sticky refusal latch

**Worker:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtk-1.the-capture-tool-complete-lifecycle-observer-and-sticky-refusal.md`.
Design direction is `1.0.0_SA_CTO`'s own (round-10 analysis @`703efac869`), executed verbatim as this cell's
arms (a)-(g), not re-derived.

## Arm (a) -- C-S160, metadata only

`IB-rtj-1`'s proof instance's `result.md` artifact row was pinned to the FIRST-pass blob
`35aac8b8bc7025024926b1c2eb61910009718366` (commit `7f5c2dad5a`); the true delivered bytes at HEAD are
blob `b7eea3aeb2817e4e436ce536feb833a1d4a9ee37` (commit `4a65336eb44dc4cf908888a590dbb5acb92a29a4`, the
second pass). Verified both blobs via `git rev-parse HEAD:<path>` and `git rev-parse <commit>:<path>`
before editing (never asserted). Corrected the row's `commit_or_etag`/`deploy_evidence` only, changed no
criterion verdict, re-ran `proof-of-spec-check`: VALID rc=0. Committed separately at `bdf01c0005`.

## Arms (b)-(f) -- the repair

**Baseline (arm (b)), captured BEFORE any source edit:** `IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs`
run unmodified against the then-unchanged source reproduced both residuals exactly as the order states --
case 1 ("interactive foreign hop returns to portal") and case 4 ("verification foreign first attempt then
clean") both showed `writes=1, success=true`; the two controls (case 2, case 3) and the HTTP-500 control
(case 5) already refused. The R9 and R8 diagnostics, run unmodified, matched `IB-rtj-1`'s own post-repair
baseline byte-for-byte. Saved as `IB-rtk-1_baseline_r{10,9,8}_*.json`.

**The repair (arms (c)-(e)), `infra/aws/ec2/investor-reporting-export/capture-session.cjs`:**

- **(c) One session-lifetime observer** -- `createLifetimeObserver(origin)` (capture-session.cjs:184-230),
  installed via `lifetimeObserver.attach(page, context)` at capture-session.cjs:287-288, immediately after
  `page` is created and BEFORE the first `page.goto` call (:305). It registers `page.on('response', ...)`,
  `page.on('request', ...)` and `page.on('framenavigated', ...)` (:219-223), plus the same on `context` when
  exposed (:224-227), filtered to the main frame via `page.mainFrame()` (:198, :199-203). These listeners are
  never removed anywhere in the file, so the observer stays live through the initial navigation, the entire
  interactive human-wait interval, and every verification navigation -- not only the navigations `main()`
  itself awaits.
- **(d) Refusal is terminal and sticky** -- `noteUrl` (:187-196) sets a closure-scope `latched` boolean
  (declared :185) the FIRST time any observed URL's origin does not equal the configured origin, and
  `if (latched) return;` at :188 is the only guard on it -- no line anywhere in this file ever assigns
  `latched` back to `false`. `refuseIfLatched()` (:295-299, a closure over `lifetimeObserver`) is the sole
  reader and is called at five points in `main()`: immediately after the initial navigation (:307),
  immediately after the human-interaction wait (:332), immediately after the verification `page.goto`
  resolves (:338), immediately after `readinessRefusal` returns (:351), and once more immediately before the
  session-state write (:364, defense in depth). Once latched, every one of these throws before any further
  output or write.
- **(e) The retry path narrows, it never widens** -- the ONE behavior change to the retry loop is that a
  foreign-origin hop, wherever the observer sees it, is now checked via `refuseIfLatched()` BEFORE the
  existing `readinessRefusal` reason is ever treated as retryable (:341-351, comment there states the
  reasoning). Every other existing readiness-refusal reason (still-showing sign-in / password present, HTTP
  5xx, marker absent) is untouched and continues to retry exactly as before -- confirmed by the R8/R9
  byte-identical regression check below, which would have caught any change to that behavior. S125
  (instance-id validation), S126 (positive readiness), S127 (origin allowlist, vendor-host refusal, scoped
  storageState) and the C-S153 initial-navigation hop walk are all unweakened: none of their code paths were
  touched.

  **Judgment call, filed as a row (see BOUNDS section below):** arm (e)'s prose names three specific
  causes ("a timeout, a 5xx response, a missing readiness marker") as what survives retry. Read literally as
  an enumerated allow-list, that would also exclude "password field still present" and "still on a sign-in
  path" from ever retrying -- which would break the ordinary human-interactive login flow (those are the
  FIRST couple of readiness-refusal reasons seen on almost every real attempt while a human is mid-login/MFA)
  and would silently change R8's/R9's regression shape. This worker read arm (e) as identifying the ONE
  behavior that must change (a foreign hop must never be retryable, which was the actual C-S159 hole) rather
  than as a literal enumerated allow-list replacing every other existing retryable reason, per the order's
  own "do not weaken or remove any existing check" and "this arm only closes the two holes the lifecycle
  diagnostic found." The conservative-for-security direction (a foreign hop is never retryable, under any
  framing) is fully implemented either way; the conservative-for-scope direction (do not invent a new
  restriction the two named defects do not require) governs which reading was taken.

**The regression and the two discriminating pairs (arm (f)):**

- `IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs`, unmodified, against the repaired source: both residual
  cases now REFUSE (0 writes each); the other four cases hold their intended shape (same-origin positive
  still writes 1; both controls and the HTTP-500 case still refuse). The diagnostic's own `reproduced` flag
  is now `false` (it was `true` at baseline) -- exit code 1, which is the diagnostic's own "defects no longer
  reproduce" signal.
- R9 and R8, unmodified, against the repaired source: byte-identical to the pre-repair baseline (`results`
  array equality, not just the pass/fail summary).
- **Pair (i), interval:** already inherent in the R10 diagnostic's own cases 0/1 -- same-origin interval
  positive (writes=1, success=true) vs. a foreign hop occurring and returning to the portal during the
  interactive wait, all else identical (now writes=0, success=false). The one property that differs is the
  interval array's middle hop.
- **Pair (ii), retry:** built by this worker's own `harness_ib_rtk_1.cjs` (same EventEmitter-based mock
  shape as the R10 diagnostic, so `page.on`/`context.on` exist) since none of CVO~B's diagnostics model a
  same-origin-transient-then-clean positive control. A same-origin HTTP 500 on the first verification attempt
  followed by a clean second attempt still succeeds (writes=1) -- transient retry is preserved. A foreign
  hop on the first verification attempt followed by a clean second attempt now refuses (writes=0) -- this is
  CVO~B's own case 4 shape, reproduced here for the side-by-side pair. The one property that differs is
  whether the first attempt's failure was a foreign-origin hop or a same-origin transient one.

All of the above is reproduced by `battery_ib_rtk_1.py --arm lifecycle`, output committed as
`R107-AC1_final_output.txt`, token `IBR107-LIFECYCLE-DIAGNOSTIC-BOTH-RESIDUALS-REFUSE`.
`battery_ib_rtk_1.py --arm c160`, output committed as `R107-AC2_final_output.txt`, token
`IBR107-C160-METADATA-PIN-CORRECTED-PROOF-STILL-VALID`.

## Arm (g) -- the packet, then the publish: STOPPED in the third pass, COMPLETED in the fourth (this worker, same serial)

**Third pass:** a new never-widen packet was written and committed (`IB-rtk-1_NEVER_WIDEN_PACKET.md`, blob
`ded605028b2210b589735927868aacf92ceb852d`, originally stated with a WRONG sha256 `fffef738...`). Neither
half existed yet, so this worker did NOT open the deploy ledger, publish, or touch the README's expected-
hash lines. The issuer (`2.0.0_SA_COO~B`) caught and corrected the packet's sha256 (@`2505e2c00a`,
corrected packet blob `5d30a76a4e851064e9f5ff0e4a3b742fdd740e6b`, corrected sha256
`f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d`) before signing anything.

**Fourth pass:** both never-widen halves confirmed at HEAD naming the corrected packet blob --
`2.0.0_SA_COO~B` @`cf4da2c5b3`, `1.0.0_SA_CTO` (file present, re-derived independently). Re-verified myself
before proceeding: packet blob at HEAD == `5d30a76a4e851064e9f5ff0e4a3b742fdd740e6b`; source blob ==
`ded605028b2210b589735927868aacf92ceb852d`; its git-blob-bytes sha256 re-derived twice (`git cat-file -p |
sha256sum` and `git show HEAD:<path> | sha256sum`) == `f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d`,
agreeing with both halves and the corrected packet.

Executed: (1) pre-publish live-object readback (sha256 `defcb585...`, VersionId `llAMqS_QPopRTb3T9KWyHLX8jJvoQWS4`,
matching `IB-rtj-1`'s own close record -- positive control before touching anything); (2) deploy-ledger
entry opened BEFORE the S3 act (`.tools/deploy_ledger.py open`, slug `irpt-rtk-1-capture-tool-publish`,
committed as its own sentinel); (3) publish via `aws s3api put-object` of the git-blob bytes (new VersionId
`Angbnvkw2YIyOfdMmVGo11vs3dVfJxBM`, prior version retained for rollback); (4) readback via `aws s3api
get-object`, sha256 `f03666ef...` -- equals the corrected packet's table exactly; (5) `capture-session.sh`
confirmed NOT republished (its VersionId and `LastModified` unmoved); (6) README.md's step-2 expected-hash
line updated to `f03666ef...` (and its commit/cell citation) in the SAME commit as the ledger close, once
the bytes were actually live, per the packet's own stated design; (7) ledger leg closed with the readback
proof, entry closed, sentinel removed.

**Two mid-pass surprises surfaced and were resolved without stopping:**

1. **A mechanical lane-gate collision (`IRPT_BCKEND-W13-S2`).** The order's own `<paths>` names
   `infra/aws/ec2/investor-reporting-export/` (line 56), but `owned-paths-validate.py`'s ADHC_OWNPTH.005
   worker-grant clause reads this order as TERMINAL at HEAD (`<status>` already `complete` from the third
   pass, before either never-widen half existed) and grants nothing under it -- even for this
   order-anticipated fourth pass. Resolved via the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL`
   escape, which `owned-paths-validate.py`'s own comment (`:121-122`) names as the sanctioned remedy for
   exactly this class; the override row is confirmed in the main-root audit log.
2. **A CRLF/LF grain mismatch in the evidence chain (`IRPT_BCKEND-W13-S3`).** The packet's ORIGINAL "wrong"
   sha256 (`fffef738...`) is not an arbitrary typo -- it is the EXACT sha256 of `capture-session.cjs`'s
   CRLF-checked-out WORKING-TREE bytes (21466 bytes, 379 CRLF sequences), while the corrected value
   (`f03666ef...`) is the git BLOB's own LF bytes (21087 bytes; 21466-21087=379, exactly the CRLF count).
   `R107-AC1`'s own committed evidence (the diagnostic tool reads the working-tree path) recorded
   `sourceSha256=fffef738...` throughout, including a fresh re-run of the SAME diagnostic just now. Verified
   this has NO behavioral effect: running the diagnostic explicitly against the git blob (its own documented
   negative-control mode) produces a byte-identical `results`/`reproduced` output to the worktree run,
   differing only in the `source`/`sourceSha256` metadata fields. `R107-AC1`'s PASS verdict is not put in
   doubt by this; it is recorded so a later reader comparing the packet's hash against the committed
   diagnostic evidence's `sourceSha256` does not mistake a checkout-time line-ending artifact for an
   unresolved discrepancy.

**A worktree-and-branch loss mid-pass, recovered without data loss.** After committing the ledger-open,
publish/README/ledger-close and surprise-row commits (`0670ef16cd`, `60bab95e58`, `897171eb53`) on branch
`wk-irpt_bckend-11-13b`, that branch and its worktree were removed from disk and from `git worktree
list`/`git branch -a` mid-session -- the live issuer (`2.0.0_SA_COO~B`) had already merged the branch into
CLOUD and cleaned up (`git merge-base --is-ancestor 897171eb53 CLOUD` = true; CLOUD's own follow-up commit
`82ef626c10` references "IB-rtk-1's publish drained"). No commits were lost (verified via `git cat-file -t`
on each hash before recovery); this worker re-provisioned a fresh worktree (`wk-irpt_bckend-11-13b-recovery`,
off CLOUD HEAD, which already carries all three commits) to finish this result.md and the proof-of-spec
instance, which had not yet been updated to reflect the completed publish when the original worktree
vanished.

**The host is STOPPED throughout every pass of this order and this cell never started it or performed any
on-host verification.** That remains the operator's own runbook step-2 re-read.

## Surprises

Three rows filed. `IRPT_BCKEND-W13-S1` (the arm (e) reading, third pass), class OBSERVATION, hazard_standing
INERT, disposition UNDER_INVESTIGATION -- the CVO grading R107-AC3 can confirm or correct the reading.
`IRPT_BCKEND-W13-S2` (the terminal-order lane-gate collision on arm (g)'s README edit and its audited-override
resolution), class OBSERVATION, hazard_standing INERT, disposition UNDER_INVESTIGATION.
`IRPT_BCKEND-W13-S3` (the CRLF/LF grain mismatch between the tested and published bytes, verified behaviorally
inert), class OBSERVATION, hazard_standing INERT, disposition UNDER_INVESTIGATION. See
`../surprise-channel/investigations/INVESTIGATION_v1.md`.
