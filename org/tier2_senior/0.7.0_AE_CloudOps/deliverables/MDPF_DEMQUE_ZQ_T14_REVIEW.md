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

## Outstanding

Awaiting site-Z CTO signature on the committed candidate/act pair. AC2 and schedule are unperformed. Notebook ledger coverage is being checked by source text; no notebook will be executed.
