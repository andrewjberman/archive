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

## Arm (g) -- the packet, then the publish: STOPPED as the order specifies

A new never-widen packet was written and committed
(`IB-rtk-1_NEVER_WIDEN_PACKET.md`), naming this repair's new blob. **As of this pass, NEITHER half exists
for this new packet** (censused: no file under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` or
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` names `IB-rtk-1` together with `CTO_HALF`/`COO_HALF`). Per the
order's own text -- "STOP here unless BOTH halves ... are at HEAD naming this NEW packet's blob" -- this
worker does NOT open the deploy ledger, does NOT publish to S3, and does NOT touch the README's expected-
hash lines under a claim of having published (the packet documents what those lines WOULD become once the
publish runs). **The host is STOPPED throughout this pass and this cell does not start it.** This is the
expected, specified stopping point for this pass -- the order says so explicitly.

## Surprises

One row filed, `IRPT_BCKEND-W13-S1` (the arm (e) reading above), class judgment-call / scope-ambiguity,
disposition UNDER_INVESTIGATION, `disarm_owner: 3.0.0_SA_CVO~B` (the seat that grades R107-AC3 and can
confirm or correct the reading). See
`../surprise-channel/investigations/INVESTIGATION_v1.md`.
