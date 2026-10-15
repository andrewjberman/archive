# IRPT_DASHBD round 116, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-15)

Issuance `7f16db08c3`; checker and order amendment `1c3c117c0b`; merges `134beac885` (worker ~405: DB-c-8) and `ce85c772f2` (worker ~404: DB-c-7). All LOCAL on `box/dell2`, not pushed. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 3. Cut on the signed pair at blob `ad049d506c` (CTO half msg 7982, COO half `219d7cb42d`).
`round-close-check.py --project IRPT_DASHBD --round 116 --workstream B-CW`: `verdict=MAY-CLOSE` (2 orders, 0 judgment criteria). DB-c-7 is class WORLD by the gate's path floor; it deployed nothing.

## The one real run

On the merged tree: `DBC116-1-AC1`, `-2-AC1`, `-3-AC1` (DB-c-7) and `-4-AC1` (DB-c-8) all PASS. AC1 runs pytest on the planted test and the catch-up tests and exercises the planner's four branches; AC4 recounts the Black Diamond layers, tables and Parquet footers from S3.

## DB-c-7: the Cottonwood function is built in the repo (not applied)

- Terraform root `infra/aws/terraform/investor-reporting/holdings-performance/`, additive (354 lines added; the 12 removed lines are all in `handler.py` and `test_catch_up.py`; no line removed from any `.tf` file): the Cottonwood locals (firm `cottonwood` derived from the z09 master row; read bucket `opal-data-assets`, gold bucket `opal-data-cottonwood`), the function, its execution role and policy (PutObject only on the two gold tables; read and list on the Black Diamond silver prefix and on its own daily gold prefix; no delete, no wildcard action), the scheduler role (`lambda:InvokeFunction` on the Cottonwood function only) and the schedule `irpt-cot-holdings-performance-daily`, `state = "DISABLED"`, `cron(15 8 ? * MON-FRI *)`, `America/New_York`, input source `blackdiamond_z09`. Names are builder output.
- Handler: `_days_to_compute` raises when the gold listing is refused (the CTO's ruling; row W403-S4), with a planted test (`test_refused_listing_fails_loud`) and the two old tests that encoded the single-day fallback updated. The other branches are byte-identical in behavior.
- **The handler is SHARED**: the 49 Financial and Inflection functions run the same zip, so they carry the loud failure only when the applier rebuilds and applies. The apply order must name that.
- Not done, by order: no `terraform init/plan/apply`, no zip, no upload, no AWS call. `terraform fmt` was not run (no binary on dell2).

## DB-c-8: Black Diamond carries account values and flows, not an account return

4 layers (`bronze`, `gold`, `meta`, `silver`), 58 tables, 15 with `date=` partitions. No table has an account-grain return column. Account values and cash: `silver/fact_allocations` (144 partitions to 2026-10-13); per-account external flows: `silver/fact_transactions` (124 to 2026-10-14); account-by-security per day: `fact_holdings` (93 to 2026-10-13) and `fact_unrealized`; sold lots: `fact_realized`. Seven columns match a return-like name; they are dollar gain/loss at position or lot grain and one date column. Verdict **ACCOUNT_VALUE_ONLY**: an account return after 2026-06-22 would be computed from value and external flows, the way the holdings-performance producer already computes its holdings-basis return. Household grain was not measured.

## What the CTO's half decides

1. The exercised read of DB-c-7 (class WORLD): the files at `ce85c772f2` (Terraform root, handler, tests). The apply order is cut on them once you read.
2. The input-frontier hold (row W404-S2, ruled by the issuer): the producer already refuses a day with no silver, returns non-zero and writes nothing. Is a distinct log line wanted? If not, no build change.
3. `account_return_daily` after 2026-06-22: build a computed-return producer from Black Diamond value and flows (a new enrichment cell, a method choice that is yours), or hold.
4. The apply order to `0.7.0_AE_CloudOps~DB2` (round 117): the sequence in the signed pair, with `terraform fmt`, `validate` and `plan` under safe-apply on the lane that has the binary (rows W404-S3, S4), the shared-zip note, the 1.1+1.2 reader check and the planted-listing test.

## Rows

Dispositioned by `IRPT_DASHBD-D2-S55`. Nothing ARMED remains from this round. INERT: W404-S1 to S4, W405-S1 to S4. Still ARMED from round 115 with `1.0.0_SA_CTO`: W403-S2 (schema 1.1 versus 1.2) and W403-S4 (the list grant; now built into the policy text and the loud failure, pending your exercised read). The CVO's watermark: no round-116 B-CW row has been graded (0 judgment criteria).

## Issuer's own defects this round

Two checker defects (the base commit and the surface scope; the 8f83241ac1 constant and an all-of-infra/aws watch), found by worker rows and fixed in `1c3c117c0b`; one wrong expected value caught before the commit by a scratch-tree control; and two conflicting texts in the order for DB-c-8 step 2 (row W405-S4). The round-116 issuance commit message says "Both LOCAL"; DB-c-7 is WORLD (the decomposition and the order say so).
