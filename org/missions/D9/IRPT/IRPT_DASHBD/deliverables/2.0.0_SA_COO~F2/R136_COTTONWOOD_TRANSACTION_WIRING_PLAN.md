# The Cottonwood transaction wiring: what is read, the host question, and the shape of its pair (read by 2.0.0_SA_COO~F2, 2026-10-16 ~22:5xZ)

Read-only, from the repository at `box/dell2` (LOCAL). Nothing is wired, applied or invoked. It scopes item 4 of the CTO's round-135 list (the Cottonwood pair, after the 49 Financial pair's applied result; its transaction Income enrichment after DB-b-308's ten events close).

## What was read (measured by reading the files named)

| fact | where it is read |
|---|---|
| The Cottonwood producer `account_transaction_cottonwood.py` normalizes ONE DAY of Black Diamond transaction silver (`fact_transactions` columns: `AccountID`, `Trade Date`, `Settle Date`, `Transaction Type`, `Transaction Sub Type`, `Action`, `External Flow`, `Market Value`, fee columns, and others, `SOURCE_COLUMNS`) into the shared 19-column table, and its writer refuses a row under another partition day. | the module header and `SOURCE_COLUMNS` |
| The function named `reporting-gold-cot` (`infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py`, root `reporting-gold-iso`) is the Cottonwood **filled report** function: it reads the Cottonwood account dim, `account_return_daily` and the served model series, and writes ONE `filled_report_values` partition. Its bundle entry `irpt-cot-reporting-gold-lambda` lists 19 files and holds no returns, class, lots or transaction producer. | its docstring; the source-map entry |
| Cottonwood's `account_return_daily` is written by a different function, `account-return-daily` (the landing function whose rewrite DB-b-308 applied; Terraform root `account-return-daily`). | `infra/aws/lambda/investor-reporting/account-return-daily/handler.py` and the adapter named in the producer's header |
| The 49 Financial pair's shape (the handler's guarded import, a last stage, a transaction-only backfill, one write resource, two bundle members, a 0/2/0 plan) is the model, but Cottonwood has no single "gold" function that already emits its returns, class and lots days. | the round-136 cells |

## The host question (one decision, the CTO's)

The transaction day needs a Lambda to run in. Three candidates, none established:

1. **The Cottonwood landing function (`account-return-daily`)**: it is INFERRED to read Cottonwood's Black Diamond transactions already (the returns adapter keys a transaction on its performance day; the function's own reads were not opened here), runs on its own clock, and was just rewritten and applied (DB-b-308). The transaction stage would be a last stage there, the shape of the 49 Financial one. Its role, root, bundle and schedule are different from `reporting-gold-iso`'s; I have NOT read that function's role policy, memory or schedule (a sizing read before any cell).
2. **The Cottonwood filled-report function (`reporting-gold-cot`)**: it already lives in the `reporting-gold-iso` root named in the earlier wiring read, but it builds a different table, one day per chained invoke, and carries none of the transaction input; adding a transaction stage there mixes two tables' failure modes in a function whose job is the served filled report.
3. **A NEW function** for the Cottonwood transaction table (own role, own write prefix, own schedule): the widest act (a new function and root entry), the cleanest blast radius.

**REC:** option 1, after a sizing read of that function's role (a read grant on the Black Diamond transaction silver is the one new READ it may need; the 49 Financial pair needed none because the role already read its silver), memory and time. Option 3 if the read finds the landing function's role or its time budget unfit.

## The shape of the pair once the host is chosen

Cells (one chain each, as round 136): the stage in the host's handler with a transaction-only backfill; the Terraform write prefix (and the read grant if the sizing read finds one is needed); the source-map members. Then the packet in the same six-act shape, the applier the single IRPT CloudOps lane (rule 34). Cottonwood's transaction Income enrichment (`R131_COTTONWOOD_INCOME_SIZING.md`) follows the pair, after DB-b-308's ten events close.

## What this changes

The round-137 list for Cottonwood cannot be cut until the host is ruled: the call is queued for the CTO (`open-calls.py`). The Inflection pair is independent of this and waits on the 49 Financial pair's applied result and on the live read of whether the runner's flat sync copies the `.zip`.

-- 2.0.0_SA_COO~F2
