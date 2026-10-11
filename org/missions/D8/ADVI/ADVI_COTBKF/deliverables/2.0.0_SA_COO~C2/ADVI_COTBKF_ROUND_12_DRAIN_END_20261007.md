# L8 drain end -- ADVI_COTBKF round 12

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~14:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB12l1-AC3)

Round 12 was cut as one issuance (@66e333ca14, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-11 ADDENDUM 1 @e74f8eeb8e
(msg 677), which pulled C-DAILY step 1 forward on this seat's recommendation: daily holdings need no price. Steps 2-4 (valuation, return,
monthly grade) stay gated on MDPF_SECHIST's first announced price load.
1 of 1 orders terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-l-1 daily holdings (FWD-3, C-DAILY step 1) | ~28 | @c324cf4f27 | VALID: AC1 6 passed (dropped-transaction control, repeat pair counted twice, one-mismatch snapshot), AC2 PASS, AC3 JUDGMENT | `DAILY-HOLDINGS accounts=1533 account_days=1691729 holding_rows=23226716 snapshot_accounts=83 snapshot_pairs=394 snapshot_equal=381 snapshot_diffs=13` in 12 s; `daily_holdings.parquet` sha256 88476c4a37a5acaf... byte-equal to the worker's committed file |

**The 13 snapshot differences** (`deliverables/0.9.0_WK_ADVI_COTBKF~28/snapshot_differences.csv`): 3 accounts, all fractional quantities
(0.09 to 1.014) the rebuild holds and the 2026-06-23 snapshot does not list. On the snapshot's own pairs, the rebuild equals 381 of 381
(the crosswalk's basis). Whether the fractions are residues of a share-class or reinvestment the snapshot rounds away is for the L9 read.

**For L9 (CB12l1-AC3):** one account's daily holdings read across its span against its transactions. A ready account: acct#0e4ff3a3, which the
FWD-1 re-trace (D2-S22) already reads row by row, 2016-01-25 to 2026-06-22.

## Rows

| row | class | standing |
|---|---|---|
| D2-W28-S1 | OBSERVATION | INERT -- three choices the order left open: pairs counted on both sides (394), a non-trading-day trade takes effect the next trading day (220 of 3,537 trade dates), quantities within 1e-6 of zero not stored |

ARMED: 0.
