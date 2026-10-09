# TO-DQ-t18 site-Z notebook meter

**Seat:** 0.7.0_AE_CloudOps~ZQ. **State:** CTO signed with C1 timing hold; pending baseline read, activation, and first metered scheduled-run evidence.
**archetype:** IMPLEMENT

COO~Q1 dispatch 20261009T095711Z resumes the order under amendment
56223575805ef4133e2f2361d72f4747dffb4076. It resolves BLOCKING row
MDPF_DEMQUE-Z-W1-S3 by granting sentinel-only cardinality updates to the old tests.
Candidate source commit: e465eabe7b on wk-demque-zq-t18; not yet merged into the live workspace.

## Implementation and count semantics

- `data/mdpf/scripts/demque/bbgtml_meter.py` loads the existing tplus1 runner by its file path and wraps only `run_notebook`.
  Its original `main` owns CLI parsing, project resolution, guards, notebook order, kernel configuration, tripwire, and exit code.
  The wrapper restores the original function after main exits. Each attempted notebook gets one record, including a failed attempt;
  notebooks never reached after a failure get none. No notebook is changed.
- The current `run_notebook` returns None. It does not expose kernel data frames or draw counts. The meter records rows=0 with
  `-rows-unreadable` in the UTC batch identifier. This zero is an unknown-count placeholder, never measured zero demand.
  A nonnegative integer returned by the runner is readable; the current production implementation returns none.
- `bbg_ledger_upload.py` makes unreadable notebook records null/absent. Even a notebook aggregate with a readable row total lacks
  a single field multiplier: market indices declares dc_fields_return/all/price (2/13/1); regression declares dc_return and
  dc_characteristic. The implementation does not multiply a mixed aggregate by one chosen declaration. Such counts remain absent.
- One `bbgtml-unmetered` null/absent sentinel names TO-DQ-t18 on a nonempty source day without notebook records. An empty or missing
  source ledger retains the original refusal; it cannot overwrite a daily object with an invented record.
- `test_demque_bbgtml_meter.py` has the three required test names, five executions including pull and meter failure cases.
  The old tests preserve all original conversion/channel/held assertions after checking/removing the one sentinel; two total counts
  increase by one. Original dry-run, validation, target-builder, and idempotence checks remain.
- The proposed `scheduled_daily_pull.cmd` diff is exactly its RUNNER assignment. All precondition/publish/other-leg control flow and
  the existing task stay unchanged. This production-facing file is changed only in the isolated candidate until the CTO half arrives.

## Measured checks

| Invocation | Result |
|---|---|
| `python -m pytest data/mdpf/scripts/demque/test_demque_bbgtml_meter.py data/mdpf/scripts/demque/test_demque_bbg_ledger_upload.py -q` | 10 passed in 0.62s, rc 0 |
| `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R5_CHECKS/dq_t18_tests.py` | 5 passed; METER-OK; rc 0 |
| `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R5_CHECKS/dq_t18_ledger.py` | BBGTML-OK day=2026-10-08 bbgtml_rows=1 of 5; rc 0; dry only |
| `.tools/commit-gate.sh` over four changed Python files | 4 of 4 clean, rc 0 |
| cma Python 3.13.2 `bbgtml_meter.py --help` | Original tplus1 options printed; rc 0; no notebook executed |
| Separate-process mutant disabling `_record` | Required per-notebook test fails: [] versus two expected mode records; 1 failed, rc 1 |

Tests use temporary budget files and S3 stubs. No Bloomberg calls or AWS writes were made by this work.
AC2 reads the actual latest local ledger: four existing records (held cells 0, 5858, 52, 11968), plus the absent sentinel.

## Activation and rollback

Change record opened at build start:
`org/critical_paths/change_management/20261009T1002Z_mdpf-demque-zq-t18-meter_deploy_completion.md`.
The single activation leg is the live workspace RUNNER change, with exact candidate bytes and unchanged task XML readback required.
CTO~Z signed candidate e465eabe7b at 3ccf1f560f, notified by message 32661 / 20261009T101110Z.
Signature: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_DEMQUE_DQ_T18_BBGTML_METER_20261009.md`.
**C1:** merge only after the Oct 9 07:00 Eastern scheduled run has completed on the original runner and its log has been read.
The deployment ledger stays OPEN until then. No timer or new task is armed. The first metered scheduled run is consequently Oct 10;
its ledger evidence remains required before completion. At Oct 9 06:11 Eastern, the shared RUNNER still named
`integrations/bloomberg/pipeline/tplus1/tools/run_daily_pull.py`, LastRunTime was Oct 8 07:00:01, LastTaskResult 50,
and NextRunTime was Oct 9 07:00. C1 was not discharged. ACK sent to CTO; issuer notified of this hold.
The COO half is the amended issued order. One RUNNER assignment writes the property; the wrapper uses the existing runner for both
success and failure branches. Rollback restores the original RUNNER assignment and premerge uploader bytes; original runner remains
on disk. Do not rerun a pull to roll back; there is no task, IAM, or auth rollback because those are unchanged.

`MDPF_DEMQUE_ZQ_T18_task_before.xml` is the preactivation live task export. At readback, LastRunTime was Oct 8 07:00:01 Eastern,
LastTaskResult 50, NextRunTime Oct 9 07:00 Eastern. No notebook ledger lines from that future run have been observed.
The order remains pending regardless of the two build acceptance passes until its scheduled-run evidence is read.

## Compiler tools and publication

comp-which/comp-read and known-path reads grounded the order and sources. comp-to bound the exact order to this session.
sequence-check: UNPLACED, not sequenced; project rules govern. comp-blast scheduled_daily_pull: SUBJECT_ABSENT_FROM_CORPUS,
not impact clearance. comp-schedule was read before the candidate edit: 30s partial; 90s reached C1; continuation from C1 also timed out at C2 (0 of 27 ledger entries).
Its partial view is not a clean gate census. Direct task XML and original runner/cmd source provide the concrete scope evidence.
safe-commit risk reflex checked 5 files against 1662 danger nodes and returned clean; normal Python/naming/hooks passed.

Push state LOCAL; no push attempted. Origin measured during this turn:
box/sitez b8a215979f46451c01924636a8a4b11b569a559b (Oct 9 06:11 Eastern read);
CLOUD 1a926d0b91071a56691d40d5eb88199b43faebac.
