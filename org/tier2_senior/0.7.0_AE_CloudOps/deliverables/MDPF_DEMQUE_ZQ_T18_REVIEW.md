# TO-DQ-t18 site-Z notebook meter completion

**Seat:** 0.7.0_AE_CloudOps~ZQ. **State:** implementation activated and verified under amended order ebdd71e8ed.
**archetype:** DEPLOY

COO~Q1 amendment 5622357580 resolved BLOCKING row MDPF_DEMQUE-Z-W1-S3 by granting the old tests' sentinel-only cardinality
updates. Amendment ebdd71e8ed assigns first metered scheduled-run evidence to the issuer's round 6 and permits this order's
completion after today's baseline read, merge, RUNNER activation, and AC1/AC2. No criterion was weakened.

## Final implementation

Candidate source e465eabe7b was merged into the live workspace by safe-merge as 04124013f9. All five changed source/test files
were compared to the signed candidate after merge: no differences. `scheduled_daily_pull.cmd` changes exactly its RUNNER
assignment to `data/mdpf/scripts/demque/bbgtml_meter.py`; no other pipeline leg or task definition is changed.

The meter imports the original tplus1 runner by file path, wraps only `run_notebook`, and delegates `main` unchanged.
Original CLI options, project resolution, guards, notebook order/kernel configuration, tripwire, return code and SystemExit
remain the runner's. One record is attempted in finally per attempted notebook, including a failed notebook; notebooks never
reached after a failure get no record. Ledger failures are contained and cannot replace the pull outcome.

The production runner returns None, not kernel data frames or row counts. The meter therefore records rows=0 and a UTC batch
identifier ending in `-rows-unreadable`. Zero here means an unknown count, not measured zero demand. Nonnegative integer returns
are readable, but the current runner exposes none. The uploader keeps unreadable records null/absent; notebook aggregates also
lack one applicable field multiplier (market dc_fields_return/all/price: 2/13/1, regression dc_return/dc_characteristic).
No conversion is invented. One TO-named `bbgtml-unmetered` row is appended on a nonempty day without notebook records. Empty or
missing ledgers retain the existing upload refusal. Original source rows, conversions, dry-run and replacement semantics remain.

Changed files: `bbgtml_meter.py`, `bbg_ledger_upload.py`, `test_demque_bbgtml_meter.py`, and `test_demque_bbg_ledger_upload.py`
under `data/mdpf/scripts/demque/`, plus `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd`.
No notebook, scheduled-task definition, IAM, auth or vendor-call behavior was edited. No ad-hoc Bloomberg call or AWS write was made.

## CTO condition and baseline evidence

CTO~Z signature 3ccf1f560f:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_DEMQUE_DQ_T18_BBGTML_METER_20261009.md`.
C1 required today's 07:00 Eastern run on the original runner and its log read before merging. This was discharged before activation.

The actual task started Oct9 07:00:13 Eastern and was Ready with LastTaskResult=0 when inspected after completion. Full log
`C:/Users/Opal Bloomberg/opal_bbg_logs/bbg_tplus1_20261009_070014.log` was read (last write07:08:47) and retained as
`MDPF_DEMQUE_ZQ_T18_baseline_20261009.txt`. It records DAPI PASS, market notebook141s, regression95s, tripwire PASS, pull exit0,
publish exit0 and served-content comparison for vintage20261008. The other legs' output is preserved in the same log; its statements
are baseline log evidence, not an independent verification of their served data by this seat.

Actual local Oct9 ledger lines read after the baseline:

```json
{"at":"2026-10-09T11:07:22Z","mode":"backfill","rows":514,"batch_id":"etf_history_backfill_2026-10-08"}
{"at":"2026-10-09T11:08:08Z","mode":"daily","rows":752,"batch_id":"batch-20261009T110739Z"}
{"at":"2026-10-09T11:08:47Z","mode":"names","rows":8,"batch_id":"names-20261009T110846Z"}
```

No notebook meter lines exist for today's original-runner baseline, as expected. First metered run is scheduled Oct10 07:00 Eastern,
not yet observed; issuer round6 owns that read under ebdd71e8ed. Tests are not represented as scheduled-run evidence.

## Activation verification and checks

Live `RUNNER` reads `%REPO%\data\mdpf\scripts\demque\bbgtml_meter.py`. Export-ScheduledTask XML exactly equals the preactivation
`MDPF_DEMQUE_ZQ_T18_task_before.xml` (TASK-UNCHANGED). `MDPF_DEMQUE_ZQ_T18_live.json` captures task state/times and source pins.

| Check | Output |
|---|---|
| `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R5_CHECKS/dq_t18_tests.py` on live workspace | 5 passed in0.25s; METER-OK; rc0 |
| `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R5_CHECKS/dq_t18_ledger.py` on live workspace | BBGTML-OK day=2026-10-09 bbgtml_rows=1 of4; rc0 |
| Old uploader suite on live workspace | 5 passed in0.40s; rc0 |
| Initial combined suites in isolated candidate | 10 passed in0.62s; rc0 |
| Python commit gate for four edited Python files | 4 of4 clean; rc0 |
| cma Python3.13.2 meter `--help` | Original tplus1 options; rc0, no pull |
| In-memory mutant disabling meter record, separate process | Required per-notebook test fails: zero records versus two expected modes; rc1 |

AC2 dry output contains the three actual records with held cells1028,12032,8 plus exactly one `bbgtml-unmetered` null/absent sentinel
whose basis names TO-DQ-t18. It writes nothing to AWS. Tests use temporary ledgers and S3 stubs. Bound proof validation returned
VALID rc0, 2 of2 criteria,0 violations before the order status flip; checker72a2636203. No code changed after candidate validation/signing.
The first completion commit was refused because the gate discovers only mission-tree deliverables for a tree order, while this
order named the seat deliverables path. The same validated proof is also filed under the mission's `deliverables/0.7.0_AE_CloudOps~ZQ/`
with the same basename; the order names both locations. No gate or criterion was bypassed.

## Deployment record and rollback

`org/critical_paths/change_management/20261009T1002Z_mdpf-demque-zq-t18-meter_deploy_completion.md` opened at start (bc9c3fc320)
and is CLOSED, all one activation leg proven, sentinel removed, closure commit856117665b. Nothing is half-landed.
Rollback restores the old RUNNER assignment and premerge uploader bytes; the original runner is still present. No pull should be
rerun merely for rollback. Task/IAM/auth are unchanged. One assignment writes RUNNER; both success/failure paths were covered by
the signed wrapper scope.

## Compiler tools, commits and publication

comp-which/known-path reads grounded the exact dispatch, source and logs; comp-to bound the order to this session.
sequence-check: UNPLACED, not sequenced. comp-blast scheduled_daily_pull: SUBJECT_ABSENT_FROM_CORPUS, not impact clearance.
comp-schedule:30s partial;90s reached C1; continuation timed out at C2 with0 of27 entries. This is not a clean gate census.
Live task XML, source comparison and full baseline-log read provide the concrete act evidence. Normal commit gates passed;
safe-merge verified10 of10 needed paths carried, dropped0, foreign0, index differences0.

Source e465eabe7b; activation04124013f9; closed deployment856117665b. Push state LOCAL (this seat made no push).
Latest measured origin box/sitez04124013f99233ab882c0dc0e2087952bc5afd6b; CLOUD f7ed4423255884e0240705bcfc407d6b381683f7.
The scheduled sync may advance origin independently; local completion records carry their own commit pins.
