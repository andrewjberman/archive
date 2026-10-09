# MDPF_CANON round 1 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~21:3xZ)

## Round 1 = THE THREAD for FWD-1

The outcome to exercise is FWD-1: *"asked what did 49 Financial's total assets read on a particular day last month, someone answers from the name of the stored file alone"*. It also requires that every stored figure of this kind sits where the one naming rule puts it.

| item | value |
|---|---|
| PRD | v2.9 @12adb87963, ADMITTED. The CTO's L5 ruling (a), msg 2995, added the per-firm gold writer; the CVO's L6 condition is msg 3000. |
| issuance | @155ac2ce67: decomposition v1, 3 cells, fan-out 2 of 2 chains, risk WORLD |
| `CN-a-1` per-firm gold writers (IAM) | ~1, `1f1360cbfb`, drained @c57820d3b9. `r1_iam.py` 6/6, fmt clean, proof VALID |
| `CN-a-2` the one parquet writer | ~2, `4fc14f14cd` + `0c547143bd`, drained @c45bce257c. `r1_emit.py` 7/7, gold tests 114 passed (3 known-red deselected, row S1), proof VALID |
| `CN-a-3` the backfill (+ AMENDMENT 1: a 403 read is "absent") | ~3, `546b4e60c6` + `aeb22e30a1`, drained @55c3cc4642. `r1_backfill.py` 7/7, `r1_emit.py` 8/8, 126 passed, proof VALID |
| deploy, order 1 | CloudOps ~DELL1 `ADHOC.canon-r1-gold-writer-iam`: 7 added, ledger CLOSED. C4 simulate on 49f: own gold allowed; own platinum and other firm's gold implicitDeny |
| deploy, order 2 | CloudOps ~DELL1 `ADHOC.canon-r1-gold-redeploy-backfill`, amended 4 times in flight; COMPLETE @1785cdcddf, C1-C7 PASS. Live pin `79e30151a6` (MDPF_STRATID's fixes rebuilt on this round's code) |

## The real run

### The writer, live

- `mdpf-gold-lambda` assumes `mdpf-{49f,inf,cot}-gold-writer-role`. These are `name()` output, admitted by the live
  `DenyForeignFirmPrincipals` with no edit: the CVO's L6 condition.
- It writes `address()`'s firm gold for the firm scopes and `opal-data-mdpf`'s composite gold for `global`.
- The `qa_local` read on the live build (C3): green, errors [], 16 of 16 objects, L-1 key-set PASS on all four types, zero writes.
- The scheduled 13:30Z floor on 2026-10-10 writes the daily path's first real partitions. That is the confirmation, never the proof.

### The history, written on demand

`run_class=backfill` wrote 537 partitions, then 3 more after the fixtures were deleted: **540**. The issuer's own count
compares each new prefix with its legacy dated source (`portal/gold/mdpf/{scope}/{type}/{date}.json`):

| scope | aum_metrics | account_distribution | aggregate_aua_timeseries | account_units |
|---|---|---|---|---|
| 49financial (`opal-data-49financial`) | 42 = 42 | 44 = 44 | 51 = 51 | 0 = 0 (no standalone source) |
| inflection (`opal-data-inflection`) | 41 = 41 | 58 = 58 | 50 = 50 | 0 = 0 |
| cottonwood (`opal-data-cottonwood`) | 34 = 34 | 34 = 34 | 42 = 42 | 32 = 32 |
| global (`opal-data-mdpf`) | 33 = 33 | 37 = 37 | 42 = 42 | 0 = 0 |

The global 10-08 cells read 32/36/41 at 21:13Z, before the last backfill pass. CloudOps' final read (C5/C6) is 16 of 16 series
equal, 0 mismatches.

### The reader hop (FWD-1's question, asked by the issuer)

1. **Asked:** "what did 49 Financial's total assets read on 2026-09-15?"
2. **The prefix:** `address("mdpf","49financial","gold","aum_metrics","date=2026-09-15")` gives
   `s3://opal-data-49financial/mdpf/49financial/gold/aum_metrics/`. Its listing holds 42 partitions, 2026-07-30..2026-10-08, with 16 September
   trading days.
3. **The answer, from the name alone:** `mdpf/49financial/gold/aum_metrics/date=2026-09-15/data.parquet`.
4. **The control (opened once, no figure printed):** the file's own `period` and `meta.count_as_of` read 2026-09-15, and `total.aum` is present
   among its 113 rows. The name tells the truth about the vintage.

## Rows

- **S1** (OBSERVATION): three `test_global_fold_flag2.py` cases already red at base. Not this project's.
- **W1-S1** (OBSERVATION): the Terraform `opal_name` module's `scope_bucket["global"]` is `opal-data-portal-v2`, while `address()`'s composite gold
  is `opal-data-mdpf`. The grant uses the existing `local.mdpf_bucket`. The builder map is tier-blind, so this is for the CTO.
- **S2** (OBSERVATION, CloudOps): `iam:SimulatePrincipalPolicy` is denied to the dell1 CloudOps principal for most policy sources. CloudOps graded C4
  another way.
- **S3, S5** (BLOCKING): MDPF_STRATID's package omission and L-1 key-set defect, which the first exercise of its 18:00Z deploy uncovered. Fixed by MDPF_STRATID
  (@79e30151a6, @88e974ca10), live.
- **S4** (BLOCKING): four 2-row synthetic composite partitions written at 19:10Z by ~2's test, in breach of its no-AWS-write bound. Deleted on
  Andrew's word (@991c4cae64; call -113f CLOSED); the real 10-08 figures then backfilled.
- **S6** (BLOCKING): the composite ListBucket CN-a-1 omitted. AMENDMENT 4, applied.
- **S7:** disarms S3-S6.

## Carried to round 2 (not this round's)

- **M1** (the census) and **M7** (the global basis) wait on nothing.
- The longer aggregate history (2024-11-01..) inside the single-object time series and `_aggregate_aua/`. M3's full-history clause is
  enrichment; round 1 backfilled the dated tree.
- `account_units` for 49financial, inflection and global: the backfill has no standalone source for them. The daily path writes them from
  the folded figure, forward from the next fire.
- **M5** (the publisher): python3.12 with no pyarrow layer (L5_FACTS section 4). M4/M6/M8/M11-M17 follow the PRD's arc. M9/M10 wait on ADVI_FIRMBKTS.
