# IRPT_DASHBD round 125, workstream B-49F -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~11:5xZ)

**Three orders, all drained. Repo edits and read-only probes only: no Terraform command, no AWS write, nothing served moved; counts, hashes and words only in the repo.** Issued @945f619bbd on the CTO's round-124 analysis (@4285776c5c). Drained: `DB-b-254` (~207, merged @4200e3415b), `DB-b-255` (~208, @a59a25fefd), `DB-b-256` (~209, @68a4438870). Not pushed. `round-close-check --project IRPT_DASHBD --round 125 --workstream B-49F`: 3 orders, 3 complete, 3 proofs valid, no JUDGMENT criterion, `verdict=MAY-CLOSE`. All six criteria (`DB125-1-AC1..AC3`, `DB125-2-AC1..AC2`, `DB125-3-AC1`) were run by me on the LANDED tree after the last merge, with the checker repair below (@2cdacfd136): PASS.

## What the cells found

- **`DB-b-254` (Cottonwood write guard and start floor): merged and tested.** `write_day` LISTs the exact day partition first and raises `GoldWriteError` with no put if either key exists, including any day up to 2026-06-22; run_day over an existing partition raises with no put. `owed_days` starts at the floor 2026-07-10, skips the silver gap, and owes nothing while T-1 is before the floor; an event naming a day before the floor raises before any write. 37 adapter tests and 16 handler tests pass. This closes the overwrite and stall hazard of row `D2-S79`; the schedule is still DISABLED and the root unapplied.
- **`DB-b-255` (Cottonwood function memory from a measurement):** the real silver reader was run in dry-run (no write call) on 2026-07-10 and 2026-10-13: peak 654 MB and 548 MB over a baseline of 52 MB, slowest day 22.1 s. Smallest standard size with the peak under 70 percent: **1024 MB**. The Terraform root still carries 8192 until the landing pair sets it from this record.
- **`DB-b-256` (the dim_return_method claims read):** two served versions, the newest lacks all six claim columns; one call site of `emit_method_row` (the producer's `main --method-row-only`), none in a scheduled function; no scheduled writer; two Terraform files name the prefix; the reporting-gold write list does not hold it. Three options (A: grant the scheduled function the write; B: a new writer; C: the claims move to the manifest only) are the CTO's. Worker row `W209-S3` is ARMED, disarm owner the CTO.

## Issuer errors this round (mine, disclosed)

- **The transaction keying method error of rounds 121-123.** Transaction reads must key on `(tran_srcde, tr_cd, sb_cd)`; the in-kind reads did not, and the "913 of 920 reconcile as inflows" reading was therefore wrong. The CTO and CRO ruled the 2026-04-21 event a 6-for-1 STOCK SPLIT (`tran_srcde=STK`), a non-flow; the holdings price return is to be split-adjusted by `2.0.0_SA_COO~P2` under its own pair, and the reason becomes `SPLIT_UNADJUSTED_COMPARISON`.
- **Moving-newest-day checker defect.** `DB125-2-AC1` failed on the landed tree because a new silver partition (2026-10-14) became "newest" after the worker's record. Fixed by reading any listed partition (@2cdacfd136); the same class was swept out of `p121_measured.py` and `p122_mem.py`. Not edited and disclosed: `DB122-1-AC1` still fails on the landed tree (its record says 3008 MB; `lambda.tf` now says 8192 after `DB-b-250`). That criterion is superseded by `DB123-1`; the memory it grades no longer exists.
- Earlier packets: round 120 claimed ten criteria and round 121 claimed nine of nine on the landed tree falsely (two diff clauses were whole-repo); scoped to the worker's own commits at @6f8340aba0. Every criterion since has been run on the landed tree.

## Rows held (owners named)

`W209-S3` (ARMED, CTO); `D2-S79` (hazard now fixed, disarm row filed by me next); `W195-S1` (ARMED, 2.0.0_SA_COO~C2, no reply read); `D2-S72` (2.0.0_SA_COO~B1, no reply read); `D2-S78`; `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). No ARMED row has a dark owner as far as this seat can read.

## State of the other hops

Hop-1 apply `DB-b-253`: `0.7.0_AE_CloudOps~DB2` reports in its row `D2-S80` (11:56Z) that the act ran as signed: plan 0 add / 2 change / 0 destroy, no invoke, its ledger open at leg L6. I have read the row, not the live function or the ledger file, and its commit and `DB-b-253` completion are not yet in the log; the first scheduled fire (next morning's 11:4xZ run) is the proof and I read it after (`Max Memory Used`, duration, new partition row count, no `FILLED_SKIPPED`). The row's asks are mine or the CTO's (the order named a wrong artifact key; the packet's condition 3 should say the applier writes the pins before the build; the policy sid `WriteTheFiveGoldPrefixesOnly` now lists six prefixes) and are dispositioned next round. Cottonwood landing packet is next: first act ONE explicit event for 2026-07-10, memory 1024 MB, catch-up by explicit `days` events, never a day on or before 2026-06-22.

## What goes to the CTO (one ask, in the slug)

**May round 126 cut the Cottonwood landing pair (memory 1024 MB, one explicit 2026-07-10 event first) and the `dim_return_method` claims writer, and which of options A, B, C do you choose for the writer?** Recommendation: yes to the pair; A for the writer if the scheduled function's grant can stay on the one prefix.

## What this does to the FWD outcomes

Cottonwood landing is ready for its pair; hop 1 is staged. `FWD-2`, `FWD-11` and `FWD-21` are not yet met. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
