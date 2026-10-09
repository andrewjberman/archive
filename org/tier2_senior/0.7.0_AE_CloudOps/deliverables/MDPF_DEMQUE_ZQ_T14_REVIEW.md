# TO-DQ-t14 candidate and site-Z WORLD act plan

Seat: `0.7.0_AE_CloudOps~ZQ`. Order: `MDPF_DEMQUE.TO-DQ-t14` (round 4).

## Candidate

`data/mdpf/scripts/demque/bbg_ledger_upload.py` reads the existing budget module's ledger directory and calls the naming builder. No producer is imported, run or edited. Field declarations are read as Python AST literals. The five required tests in `test_demque_bbg_ledger_upload.py` use temporary files and stub S3.

Source reading exposed two producers sharing `backfill`: rivalfunds holdings and ETF historical data. `etf_history_backfill_*` selects the ETF `RET` field declaration (two fields); `batch-*` selects the stated 16-column holdings reconstruction. The raw mode and batch_id remain in the output. Unsupported/ambiguous records have null cells and absent claim; an unknown channel is null. Known conversions carry held claim and basis because requested/returned cells do not measure the vendor's capacity meter. `market-range` mixes reference currency requests and history under the same mode/batch. `amgt-model-block` mixes request widths. Neither gets an invented conversion.

## Validation measured before commit

- AC1 `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R4_CHECKS/dq_t14_tests.py`: five named tests PASSED, `UPL-OK`.
- `.tools/commit-gate.sh` on both new Python files: `OK: pre-commit gate clean for 2 of 2 file(s)`.
- Dry run, latest existing UTC ledger `2026-10-08`: four records, 3,729 rows, 17,878 converted cells, all held. Breakdown: holdings 0 + 11,968; ETF history 5,858; names 52.
- Builder target: `s3://opal-data-assets/bloomberg/global/bronze/demand_ledger/dt=2026-10-08/ledger.jsonl`.
- STS caller: `arn:aws:iam::313476888478:user/Andrew_Berman`.
- IAM `simulate-principal-policy` for that principal, `s3:PutObject`, exact object ARN: `allowed`, missing context `[]`. This is an identity policy simulation; apply/read-back proves actual access.
- Sequence check: MDPF_DEMQUE UNPLACED, its directive governs; no sequence hold reported.
- `comp-blast bbg_ledger_upload` and `bbg_budget`: subject absent from served graph, not a no-impact clearance. Source/target read directly.
- `comp-diff` reports no changed files (new untracked files are outside that instrument's view); the two explicit paths pass the commit gate.
- `comp-schedule --owner 0.7.0_AE_CloudOps~ZQ --budget 10`: PARTIAL_OR_BLIND, not a clean gate census. Live Windows task read confirms OPAL_BBGTML_daily_pull enabled daily at 07:00, Interactive user Opal Bloomberg, local timezone Eastern Standard Time.

## Exact proposed WORLD acts (site-Z CTO half required)

1. Open the change-management entry for this order.
2. Apply once for the latest existing UTC ledger (currently October 8). Write only the single builder-derived `ledger.jsonl`; no prefix clearing. Read AC2 for that day and compare served bytes to the local conversion.
3. Register `OPAL_DEMQUE_bbg_ledger_upload` daily at 08:30 Eastern, after the 07:00 pull, under the existing user's interactive context. Run the committed uploader with **previous UTC day**, so the daily upload covers a closed day including later CORPUS/other draws. The one initial latest-day apply is separate. No Bloomberg calls. Use an absolute committed worktree path and Python executable; PowerShell computes UTC yesterday at execution and propagates the Python exit code. Record exact action, enabled state, trigger, principal and source commit.
4. Read back the registered task and finish the ledger. No additional monitor or timer.

Rollback: unregister only the new named task; restore the prior version/bytes of the single initial object if it existed, otherwise remove only that newly written object. Capture prior object state before apply. No producer, auth, or IAM changes. No changes to the 07:00 task.

## Completion and handoff

CTO site-Z half SIGNED at `3607c76017`, message 32558; conditions C1-C5 were applied. The initial upload and the schedule are complete. Change-management entry `org/critical_paths/change_management/20261009T0813Z_mdpf-demque-zq-t14-ledger_deploy_completion.md` is CLOSED, both legs proven.

- C1: task runs the quoted uploader path in the shared workspace, not a worktree. Source remains `492cb5a2f1`.
- C2: task wrapper reads `bbg_budget.ledger_dir()` without a producer import; missing day 1900-01-01 prints `SKIP: no ledger file for 1900-01-01`, exit 0. Other Python errors propagate. A native-command quoting error in the first scratch wrapper probe was fixed before task registration.
- C3: exact target head-object returned 404 ABSENT before apply; prior-state JSON recorded. Rollback is removal of only that new daily object plus unregistration of the new task.
- C4: ledger opened before the first write and closed after task read-back.
- C5: exported `OPAL_BBGTML_daily_pull` XML compared equal before/after; existing task untouched.

AC1 from shared workspace: five tests PASSED, `UPL-OK`. An in-memory mutant changed the holdings multiplier to 15; conversion test failed (`45 != 48`, exit 1). The unmodified suite then passed. No source/deployed file was mutated.

AC2, both explicit day and exact no-argument order invocation: `LEDGER-OK rows=4 cells=17878 under s3://opal-data-assets/bloomberg/global/bronze/demand_ledger/dt=2026-10-08`. All four rows carry held claims. Served 1,040 bytes match local bytes; SHA256 `5ea616b2aaf151a888cbdd05097b0bb3ba375641c11294b9d490a292d023293f`, version `oTKuZIDmQ9me24YkH1uZ73gSF1gm5IU4`.

Task `OPAL_DEMQUE_bbg_ledger_upload`: **Ready, enabled**, daily 08:30 Eastern, previous UTC day; Interactive user Opal Bloomberg, Limited. Next run October 9, 2026 at 08:30 Eastern. First scheduled fire is not yet observed. Its complete encoded/decoded action, trigger, principal and source pin are in `MDPF_DEMQUE_ZQ_T14_task.json` and exported XML; prior and served object evidence are in the adjacent `_prior.json` and `_served.json`.

Candidate `492cb5a2f1` was safely merged locally as `ac9945ffe2`; the merge check found all three expected files present and the index matched HEAD on all three. Signature requested from `1.0.0_SA_CTO~Z` in message `20261009T080551Z_0.7.0_AE_CloudOps_ZQ_TO-DQ-t14__site-Z_WORLD_half_requested_o.md`.

Notebook coverage read is complete: the scheduled tplus1 runner and both named notebook sources contain no `bbg_budget` or `.record(` calls. Claim remains held. Appended observations `MDPF_DEMQUE-Z-W1-S1` (mode ambiguity) and `MDPF_DEMQUE-Z-W1-S2` (notebook coverage) to the project's investigation channel; no producer edited.

Observation commit: `db1544544d`. The row gate rejected the issuer-required `W1` identifiers because this assignee is a named seat, not a numeric worker. Used the gate's documented audited `surprise-row-override` with the exact TO BOUNDS requirement as the reason. The row corpus check found zero new schema failures; both override audit entries were written by safe-commit/the hook.

Push state: **LOCAL**. At the candidate report, `git ls-remote` read origin `box/sitez` at `1ebbf7ecdf1d9d3c9c22f2023a61f27895181075` and origin `CLOUD` at `393790d6ad4d11054e8b916f3d4c69447fca2817`. This seat has not pushed. The completion commit carries the validated proof and terminal order status.
