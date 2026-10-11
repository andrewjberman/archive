# CB-bo-2 -- the splits the grown split-history store added (round 67, 0.9.0_WK_ADVI_COTBKF~100)

Read-only measurement. No code, config or manifest changed; no S3 write of any kind (version listings and gets of the store only).
Record: `ADDED_SPLITS.json`; per-added-CUSIP table: `ADDED_CUSIPS.csv`; the 30 account-days by date: `DRIFT_DATES.csv`.
Store: `s3://opal-data-assets/yahoo/global/silver/price_history/cusip=<CUSIP>/splits.parquet` (address from `lib/opal_naming` as `load_store_splits` builds it).

## 1. What was added, and when
- Served run (round 34, data dir r34): 2026-10-09, between 11:48:25Z and 12:01:11Z, bounded from file times; its log line is `SPLIT-STORE listed=32 held_by_the_accounts=32`.
- Version listing (648 object versions under the prefix, no delete markers; 159 `splits.parquet` versions over 141 partitions): 32 partitions landed 2026-10-09T01:28:12Z (1) and 02:38:19Z..02:39:06Z (31); the count stays 32 until 2026-10-10T02:33:18Z; 109 more landed 2026-10-10T02:33:18Z..03:00:42Z; 141 since. So 32 at the served run, 141 now, 109 added.
- Held = in the build's universe (`universe_from_tx` over the transactions cache, 4,634 CUSIPs); all 141 store partitions are held (the served table's 4,614 give the same 32 / 141).
- Among the original 32: 0 changed content. 18 were rewritten once on 2026-10-11T05:31:44Z..05:32:00Z with the identical date/ratio events; 14 never rewritten.
- The 109 added carry 205 store events in 45 partitions (64 hold none). Only 26 are dated after the CUSIP's first transaction, which is what `split_plan` reads.

## 2. Which of them move anything
Plan of today's control (`method_r28`) against the served plan, added CUSIPs only: 26 store lines. Applied 8 (4 with the account rows agreeing, no price change; 4 DISAGREE, store only), not applied 18 (15 CUSIPs; stored close not continuous across the day), disagreements 4. The 3,034 changed price points (of 2,124,908) are exactly the 4 DISAGREE lines: 00206R102 (649 points), 438516106 (1,876), 460146103 (392), 717081103 (117). Every moved point is the served price x the store ratio, exactly.

## 3. Real, and dated before the days they move
| CUSIP | split date | ratio | first..last moved | class |
|---|---|---|---|---|
| 00206R102 | 2022-04-11 | 1.324 | 2020-07-01..2022-04-10 | REAL_AND_BEFORE |
| 438516106 | 2025-10-30 | 1.061 | 2020-09-10..2025-10-29 | REAL_AND_BEFORE |
| 460146103 | 2021-10-01 | 1.056 | 2020-09-04..2021-09-30 | REAL_AND_BEFORE |
| 717081103 | 2020-11-17 | 1.054 | 2020-07-23..2020-11-16 | REAL_AND_BEFORE |

All moved points lie strictly BEFORE the split date (last moved = the calendar day before), contiguous from the CUSIP's first price date; that is the side a correct as-traded adjustment moves.
Independent evidence: (a) the custodian posts `acca` (Adjust Cost Corporate Action) on exactly that date for the CUSIP and `lica` (Corporate Action Contribution) of a second security the same day (Warner Bros. Discovery, Solstice Advanced Materials, Sylvamo, Viatris); (b) own quantity is unchanged across the date (ratio 1.0000 in every account holding on adjacent days), so these are NOT share splits but spin-offs, and the ratio is a price factor; (c) the cottonwood store (a separate price store) steps down across the date by 0.8132 / 0.9400 / 0.9524 / 0.9654 where the unrepaired Yahoo close is continuous (1.0766 / 0.9973 / 1.0058 / 1.0176); Yahoo ratio over cottonwood ratio gives the factor 1.3239 / 1.0610 / 1.0561 / 1.0541 against the store's 1.324 / 1.061 / 1.056 / 1.054; cottonwood against the repaired series has no step at the date. Surprise row ADVI_COTBKF-D2-W100-S1 records that they are spin-offs. The class is the worker's reading; the judgment criterion is not self-graded.

## 4. The 30 account-days
28 returns, one account, 2020-10-12..2020-11-18: all rest on 00206R102. 2 blank reasons (UNPRICED -> INKIND_UNDERSTATED), 2020-10-13 and 2024-09-24, two accounts, each with an in-kind li row of 438516106 whose value changed. All 30 are in class REAL_AND_BEFORE; 0 in the other three classes.

## Not established
See `not_established` in the record: the run's instant is bounded not stamped; the store bytes served then are rebuilt from object versions; cottonwood's independence from Yahoo upstream is not proven; whether spin-off factors belong in the rule is for the CTO; 00206R102's one-day ratio (0.8132) is 7.7 percent away from 1/1.324.
