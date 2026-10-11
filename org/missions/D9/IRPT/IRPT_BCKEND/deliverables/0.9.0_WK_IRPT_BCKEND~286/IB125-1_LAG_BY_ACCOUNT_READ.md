# IB125-1 -- Cottonwood's lagged closes by account and by source field (read only, counts only)

Author `0.9.0_WK_IRPT_BCKEND~286`, 2026-10-11. For the CTO. Data: `IB125-1_lag_by_account.json`. Instruments: `ib427_fetch.py`, `ib427_by_account.py`
(copied from IB-pr-425's scripts and extended). S3 reads only. No account id, balance or position value is in any file here; accounts appear as counts.

## What was measured

The same 85 graded days (2026-06-10 to 2026-10-09), the same anchor, tolerance (1e-4 relative) and definition of "moved" as IB-pr-425. Every moved ROW is graded
at the own close, the prior close or neither, then grouped by account. 1,000 accounts appear in the graded partitions. 614 have at least one moved row; 386 have none.

Reconciliation with IB-pr-425: exact. Moved rows 583,996 and prior rows 3,278 equal its `rows_priced_moved` and `rows_prior`. Re-applying its security-day rule (prior if
any row is prior, else own, else neither) to these rows gives 37,806 moved, 34,931 own, 2,514 prior, 361 neither, and every one of the 85 days matches its day counts.
Its 2,514 prior security-days are 3,278 prior rows.

## The account split

| class | accounts | moved rows | own | prior | neither |
|---|---|---|---|---|---|
| always_own | 553 | 495,642 | 494,257 | 0 | 1,385 |
| always_prior | 0 | 0 | 0 | 0 | 0 |
| mixed | 61 | 88,354 | 84,558 | 3,278 | 518 |
| no_moved_rows | 386 | 0 | 0 | 0 | 0 |
| all | 1,000 | 583,996 | 578,815 | 3,278 | 1,903 |

3 of the 553 always_own accounts have only "neither" rows (0 own, 0 prior); they meet the always_own definition literally and are counted there.

Share of each account's own-or-prior rows at the prior close (614 accounts, minus 3 with no such row): 0 percent: 550; above 0 to 1: 11; 1 to 10: 37; 10 to 50: 0;
50 to 99: 13; 100: 0. No account is behind on all of its rows. The largest share is under 100.

## The mixing

61 accounts are mixed. By day (behind on some days, current on others, never both in one day): 53. Within a day only (some securities behind, some current, the same day): 2.
Both patterns: 6. Counted by account-day, the mixed accounts are current-only on 3,846, behind-only on 459 and hold both on 8. So the mixing is almost entirely BY DAY.

## Time

An account is "behind" on a day if it has at least one prior row. Per day, 0 to 24 accounts are behind (median 6; 25 days have none). 61 accounts are ever behind;
18 on 2 or more days, 12 on 10 or more, 10 on 20 or more, 5 on 40 or more, none on 60 or more. Day to day the set is sticky: median 83 percent of yesterday's behind
accounts are behind again, and 89 percent of today's were behind yesterday. It is a small set that changes slowly.

The four heavy days are NOT many accounts at once. Accounts behind (of accounts with moved rows): 2026-10-01 6 of 579 (328 prior rows); 2026-09-03 10 of 569 (327);
2026-07-02 24 of 516 (406); 2026-07-31 17 of 550 (226). Those accounts hold 6 to 17 prior rows each at the median. Pairs of heavy days share 2 to 6 behind accounts;
2 accounts are behind on all four.

## The field split

Considered and split: `Account Supervised`, `Holding Supervised`, `_source`, `_feed`, `_schema_version`. Left out: `Relationship ID`, `PortfolioID`, `Account Number`
(account-specific ids, not category labels); `_source_file`, `_source_as_of` (one value per day: the day itself); `Cash Equivalent` and the security descriptors (not custodian,
source, feed or type). `_source` (blackdiamond), `_feed` (holdings) and `_schema_version` (1.0) each hold ONE value on every row: the lag cannot follow them.

`Account Supervised` and `Holding Supervised` are the same on every row and are in the partitions only from 2026-08-20 (36 of 85 days; absent on the other 49).

| value | accounts | moved | own | prior | neither |
|---|---|---|---|---|---|
| Supervised (36 days) | 595 | 318,287 | 317,231 | 769 | 287 |
| Unsupervised (36 days) | 16 | 1,830 | 114 | 1,463 | 253 |
| column absent (49 days) | 563 | 263,879 | 261,470 | 1,046 | 1,363 |

Where the field exists, the lag follows it strongly: 80 percent of Unsupervised moved rows are prior (0.24 percent of Supervised). 16 accounts carry the label; 13 of them
are mixed. But Supervised accounts still carry 769 prior rows, and 48 mixed accounts never carry an Unsupervised row on a present day. So the label marks a heavy part of the
lag, not all of it, and it cannot be read before 2026-08-20.

## The neither rows (1,903 rows; IB-pr-425's 361 security-days)

By account class: 1,385 in always_own accounts (73 percent), 518 in mixed. By field: Supervised 287, Unsupervised 253, column absent 1,363. On the days with the field, 14 percent of
Unsupervised moved rows are neither, against 0.09 percent of Supervised. 72 percent of the neither rows (1,363 of 1,903) are on the 49 days without the field.

## Is the lag a property of the account, a field value, the day, or none?

- The ACCOUNT: yes, in part. All 3,278 prior rows sit in 61 of 614 accounts; 553 accounts never lag. But no account always lags, and the 61 are current most days.
- A FIELD value: in part. `Unsupervised` carries 1,463 of the 2,232 prior rows on the days it can be read (66 percent). No source, feed or schema value varies.
- The DAY: not as a mass event. A heavy day is 6 to 24 accounts each holding many rows.
- Not one of these alone explains it.

## Not measured

- Why an account is behind (a pull's timing, a custodian, a vendor feed). No log or vendor call was read.
- Whether an account's supervised status explains the 49 days where the column is absent.
- Portfolio and relationship grouping (whether the behind accounts share a portfolio or relationship), and the size of the positions behind.
- Rows without a CUSIP or a priced Units and Market Value; securities the anchor does not carry; securities that did not move.
- 2026-06-09 (no prior-day partition) and any date outside 2026-06-09 to 2026-10-09.
- Any basis declaration: this cell measures only.
