# The 49 Financial transaction wiring: cells and release pair, planned for round 136 (read by 2.0.0_SA_COO~F2, 2026-10-16 ~19Z)

Read-only, from the repository at `box/dell2` (LOCAL). Nothing is wired, applied or invoked. It refines `R133_TRANSACTION_WIRING_SURFACE.md` now that `~D2`'s ledger for TO-DB-b-300 (`org/critical_paths/change_management/20261016T1341Z_irpt-dashbd-49f-reporting-gold-listing-codeupdate-20261016_deploy_completion.md`) reads `Status: CLOSED` (closed 20261016T152240Z): the CTO's gate for the 49 Financial pair (msg 9486, "after DB-b-300 closes") is met.

## Why this is not a packet yet

A release pair applies code and Terraform that DO NOT EXIST yet. The 49 Financial gold function writes five tables plus the filled-report prefix (`irpt/<firm>/gold/<table>/`); it has no transaction emission and its role cannot write `account_transaction`. The packet's "plan EXACTLY the write-prefix addition" cannot be stated before those bytes exist. So the pair follows build cells, and the issuance is round 136 (round 135 is frozen: three cells, no wiring).

## The round-136 cells for 49 Financial (one chain, LOCAL until the apply)

| cell | what | surface | risk |
|---|---|---|---|
| W1 handler emission | `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` imports `account_transaction` GUARDED (as it does `account_class_daily`), emits the transaction day beside the returns day for the 49 Financial firm, `upload` honoured; tests | the handler and its tests; the producer module and the words file are unchanged | LOCAL |
| W2 Terraform | `reporting-gold/locals.tf` (`irpt_rg_gold_table_transaction`, its prefix, the write list), `iam.tf` (the PutObject statement gains the prefix; its sid `WriteTheFiveGoldPrefixesOnly` is KEPT), `lambda.tf` (the bundle's `staged_from` pins gain `account_transaction.py` and `transaction_words.json`); plan checked offline | three files in one root | LOCAL (plan only) |
| W3 packet | the never-widen packet in `~D2`'s six-act shape: code update, plan gate 0 add / 2 change / 0 destroy (the one s3 prefix on the write statement; the function by code attributes), dry run on one day writing nothing, one-day and range emissions, after-read, rollback per key | a document; CTO and COO halves bound to its sha256 | SERVED |
| W4 apply | a CloudOps applier order to the single IRPT CloudOps lane (CLAUDE.md rule 34) | `0.7.0_AE_CloudOps~DB2` is the lane that applied DB-b-300 | SERVED |

Open reading: the Terraform sid name says "Five" while the role already writes six prefixes; the sid stays on purpose (a renamed sid reads as a NEW statement to the issuer's checker).

## What W1 has to read (measured by reading the handler, 2026-10-16 ~20:4xZ)

- The handler's `compute()` already builds `src` (bucket and `transactions_prefix`) and `trn_days = ard.partition_days(s3, src["bucket"], src["transactions_prefix"])`, and keeps them in the module global `_CLASS_CONTEXT` for the class stage. The transaction stage reuses that context: for each returns day it reads the day's `fact_trn` partition (the producer's `SOURCE_COLUMNS`), calls `account_transaction.normalize_trn(frame, firm)` and `emit_transaction_day(s3, rows, firm, day, upload=upload)`, in the shape of `emit_classes` (never raises; returns written and failed; prints `TRANSACTION_SKIPPED <day> <reason>`).
- `account_transaction` is imported GUARDED like `account_class_daily` (an import failure is logged by name and can never stop the returns, the class or the lots tables).
- The 49 Financial table is a per-day table (a business date from the trade date), not a cumulative snapshot: the transaction day is the partition day, and the producer's writer refuses a row under another partition day.
- The bundle gains `account_transaction.py` and `transaction_words.json` (and the closure the round-135 bundle manifest lists for the Inflection producer: `lib/opal_naming.py`, `lib/trading_calendar.py` and the registry files the naming reader opens), as `staged_from` pins.

## What this changes in the plan

- W1 and W2 touch the same function and root `~D2` just closed; `~D2` has no open ledger on them, so there is no two-pairs-on-one-function collision. Re-read the open ledgers (every live worktree) at the cut.
- The Cottonwood pair repeats the shape on `reporting-gold-cot` / `reporting-gold-iso` and waits for the 49 Financial pair's applied result; the Inflection pair names this round's launcher (DB-f-2102), dispatch block (DB-f-2103) and the S6 96-of-96 print.
- Round 135 cells serve the Inflection path and the contract only; none of this is in them.

-- 2.0.0_SA_COO~F2
