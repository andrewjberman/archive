# Task Order: NFRA_CMTQUE TO-6R -- load-test RUN + phased cutover of the 1338 callers (the WINDOW-gated leg)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cmtque-to-6r</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B + 0.0.0_AB_MSTR (window) + 3.0.0_SA_CVO~B (cert)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_CMTQUE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>GENUINELY-EXTERNAL but NARROW: gates only this RUN leg (11 live agents on the box). MSTR names a specific quiet window (no gold/rebuild/re-serve in flight) -- NOT passive-wait, NOT default-to-tonight.</gate_note>
  </metadata>

  <objective>Run safe-commit-loadtest.sh (N in {10,25}) under a CONFIRMED-QUIET window -> measure queue-vs-mutex p50/p95 + exit-3 storms; then canary a subset of agents on SAFE_COMMIT_USE_QUEUE, then flip the default. The load-test is BUILT+ready; only the RUN needs the window.</objective>

  <requirements>
    <requirement id="1">all commits land, zero exit-3, lower tail-latency than mutex</requirement>
    <requirement id="2">compat matrix passes; one index-writer during burst; no silent drop</requirement>
    <requirement id="3">phased: load-test -> canary subset -> flip default, with documented rollback</requirement>
    <requirement id="4">CVO~B certs the cutover</requirement>
  </requirements>
</task_order>
```

<!-- ZOMBIE-RESOLVED 2026-07-13T08:04Z by 2.0.0_SA_COO.
     This TO was <status>pending</status> -- which means DISPATCHED -- while its assignee was
     NOT REGISTERED. Nobody was there. The board read it as ACTIVE work in flight.
     Flipped pending -> staged: `staged` is the TRUE state (scoped, awaiting a GO when a live
     lane exists). NOT flipped to complete -- THE WORK WAS NEVER DONE.
     Detector: .tools/to-liveness-join.py (e8ed4e1d2) -- the join /to-check and fabric-check
     never made. A dispatch into an unverified lane is a hope, not a drive. -->
