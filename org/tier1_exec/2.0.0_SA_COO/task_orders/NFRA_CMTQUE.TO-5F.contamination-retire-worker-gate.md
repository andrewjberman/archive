# Task Order: NFRA_CMTQUE TO-5F -- contamination-guard retire + worker-side ds-gate re-assert

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cmtque-to-5f</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07 (post-reboot Wave-1). CLOSED 2026-07-07T16:33Z, all 4 requirements live-exercised against the real worker + real repo.</dispatch_state>
    <gate_note>COO-RESOLVABLE now, no window. Owner 0.7.0~B.</gate_note>
  </metadata>

  <evidence>
    Commit fce73ef08 (+ cleanup e0f9e5b4b for a self-caught mid-exercise mistake -- see below). Session log: org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-07/nfra_cmtque_to5f_worker_gate_reassert.md (10acd3e41).
    Req 1: --selftest green before and after.
    Req 2: owned-paths rejection exercised live -- enqueued a .github/workflows/ file as AE, the real git pre-commit hook blocked it (lane=BASE_EXEC).
    Req 3: non-compiling .py rejection exercised live -- enqueued a broken file directly. Caught + fixed 2 real bugs in the process: (a) the running daemon was pre-edit code (no hot-reload), so the FIRST attempt actually committed the broken file (63b98eda1) before the restart was caught -- cleaned up in e0f9e5b4b, re-verified clean; (b) a rejected file stayed staged (no unstage-on-reject) -- fixed using the same git-reset pattern the sensitive-leak gate already uses.
    Req 4: confirmed (per COO's scope ruling this session) the worker's own commit logic never ported the mkdir-mutex/contamination apparatus (D5, already retired) -- did NOT touch safe-commit.sh's still-active legacy path, correctly scoped per the TO-5F scope-fork ruling.
    Bonus: exercised the objective's workflows/-class near-miss directly -- a session.har under workflows/**/sources/ correctly fail-closed (sensitive-leak blocked) in the worker.
  </evidence>

  <objective>Remove the commit-mutex v2 baseline/contamination apparatus (safe-commit.sh:196-339) from the queue path; worker re-asserts ds-gate; prove the workflows/-class sensitive leak still fail-closes IN THE WORKER (the 07-02 near-miss).</objective>

  <requirements>
    <requirement id="1">selftest case-2 green (already)</requirement>
    <requirement id="2">owned-paths-lane rejection exercised in the worker path</requirement>
    <requirement id="3">non-compiling .py rejection exercised in the worker path</requirement>
    <requirement id="4">legacy apparatus removed from the queue path</requirement>
  </requirements>
</task_order>
```
