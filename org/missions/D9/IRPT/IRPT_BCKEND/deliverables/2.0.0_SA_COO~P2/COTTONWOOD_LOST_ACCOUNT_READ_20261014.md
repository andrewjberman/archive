# Cottonwood's lost account: the read the CTO ruled first (ruling call 3, step 1)

Reader: `2.0.0_SA_COO~P2` on dell2, 2026-10-14 ~02:5xZ. LOCAL read; the DIRECT-ACT path (under the size floor). Every value below is a count, a date, a boolean or a hash prefix. The raw account key was read in memory only and is in no file: the lost account is named by the sha256 prefix `61cb0a951f` of its opaque id. Scratch copies were deleted after each read.

## What the guard says (read, not inferred)

The holdings publish gate refused Cottonwood's candidate (business date 2026-10-12, 867 accounts, 17,966 nodes) at 2026-10-13T14:17:42Z on ONE condition, `account_lost`, count 1; the served publication is business date 2026-10-08. By the trading calendar (`lib/trading_calendar.py`, fallback NYSE table; frontier read 2026-10-14) the served publication is **4 trading days behind** the frontier and the candidate is 2 behind.

## The state of the one account at the source

| source (Cottonwood, Black Diamond silver and the landed directory) | 2026-10-08 | 2026-10-09 | 2026-10-12 |
|---|---|---|---|
| `fact_allocations` (the independent totals) holds the account | yes | **no** | **no** |
| `fact_holdings` holds the account | yes, 2 rows | yes, 2 rows | yes, 2 rows, value zero |
| `fact_model_assignment` holds the account | yes (Rebalancer, Taxable) | yes | yes |
| `fact_transactions` rows for the account | 2 (a cash deposit, an expense) | 2 | 3 (the third trade-dated 2026-10-08) |
| landed directory entry holds the account | yes, termination UNKNOWN | no | no |

- The directory entry is a RELATIONSHIP of four accounts. From 2026-10-09 the same relationship stays in the directory with the other **3** accounts (all 3 still in the silver tables); no new account id appears in it.
- The identity instrument was positive-controlled: the three sibling accounts of the same relationship are found in every silver table by the same mapping (3 of 3). An earlier raw-string search of the silver tables found nothing for the lost account or its siblings, which showed that the directory's ids are opaque; it is retired and proves nothing.
- Cottonwood's source holds **no account status column** (`fact_allocations` and the others carry none; the directory builder says so and emits UNKNOWN). No `Relationship Termination Date` is set for the account's transactions. **No source field says the account is closed or transferred out, and no date is available for either.**

## The reading

The account is **not closed or transferred out by any source field, and not re-keyed** (the same key still holds its positions, assignment and transactions). It is **missing from the allocations feed since 2026-10-09 while its holdings, assignment and transactions persist**; its positions are two rows of negligible value, zero on 2026-10-12. The candidate drops it because the build needs both the holdings and the independent totals.

By the CTO's ruling this is branch 3 (missing from the feed): the guard is right as written and Cottonwood stays served at 2026-10-08, named stale.

## A second finding the read produced (the guard's own exemption)

PRD v0.33 (the `directory_marks_no_closures` rule, `holdings_snapshot.py` `evaluate_publish_gate`) lists a lost account instead of refusing when the firm's directory marks EVERY entry UNKNOWN, which is Cottonwood's shape. The landed directories of 2026-10-09 and 2026-10-12 carry **10 and 2 TERMINATED entries** (clients carried forward as removed from the source, effective 2026-10-08; the directory's `carried_forward.terminated` counts them). One TERMINATED entry makes `all UNKNOWN` false, so the exemption does not apply and the gate refuses. The accounts of those removed clients are exempted as closed; this account is not among them. Without those carried-forward entries the gate would have LISTED this account and published.

## What this read does not settle (put to the CTO)

Whether to treat a zero-value account dropped from the allocations feed as left (a branch-2 never-widen pair removing that one account, rollback to the 2026-10-08 snapshot) or to wait for the feed. Whether the all-UNKNOWN exemption should ignore carried-forward TERMINATED entries. Neither is mine; row D2-S160.
