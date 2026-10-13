# CB-cc-3 -- date-bound re-read (round 81), 0.9.0_WK_ADVI_COTBKF~160

Record: `DATE_BOUNDS.json` (same folder). Law: Andrew's backfill law, record `ANDREW_DIRECT_20261013_141xZ_BACKFILL_FLOOR_2012_AND_EARLIEST_CLIENT_RECORD.md` @82c7c92449, read by `git show origin/box/dell1:...` (resolved; not in worktree HEAD b1845759b7).

## Law (quoted from the record)
- Floor: "no backfill request reaches before 2012-01-01, whatever a record says."
- Client history: the window starts at the EARLIEST CLIENT RECORD for the security or account, not earlier.
- Non-client need: "365 days back from the point of the need" (ADDENDUM 1); the 2012 floor binds both.

## Earliest client record
- 2013-04-03 (firm minimum of `Trade_Date`, 14 parquet files, 1,416,497 rows, tx_cache copy).
- Accounts (1,533): before 2012 = 0; 2012 to 2019 = 1,026; in 2020 = 97; after 2020 = 410.
- Per security (4,634 CUSIPs): one CUSIP's first record is 2013-04-03; 4,633 start later. The first-record years run 2013 (1,131) to 2026 (45).
- `Cost_Date` was not used: 2 rows hold 1901-01-01 and 389 rows precede 2000-01-01 (placeholder dates; see the channel row).

## Windows (4 determined, 1 moves)
| where | kind | start | end | moves | new_start | rule |
|---|---|---|---|---|---|---|
| decomp round12 l14, silver transactions | build_range | 2013-04-03 | 2026-06-22 | false | 2013-04-03 | none |
| decomp round12 l15, positions snapshot | build_range | 2026-06-23 | 2026-06-23 | false | 2026-06-23 | none |
| PRICE_NEED_20261007.json (days_held per security from its first Trade_Date) | client | 2013-04-03 (span) | 2026-06-22 | false | per security = its first record | none |
| decomp round33 l25, canonical price store | build_range | 2006-01-02 | 2026-06-09 | true | 2012-01-01 | floor_2012 |

The price need's span start is the firm minimum; each security's window starts at its own first Trade_Date, which is its earliest client record, so the law does not move it.

## Built before its bound
- Canonical price store: first date 2006-01-02, 2,190 days before 2012-01-01. Nothing is deleted or rebuilt here; the narrowing happens at the next cut.

## Not established (8)
Request file window 2020-07-06 to 2026-06-22 (security fields outside the read grant); account_return_daily backfill start (not stated); 47 early holdings partitions (account-level contents unread; 3 accounts have a first record after 2026-04-22); custodian mark store 2026-06-08 to 2026-10-06 (not read by the issuer); single-day fetch 2022-10-12 (two CUSIPs not computed); served APH/CTVA account-days 2025-02-11 to 2025-04-21 (account not identified); build series after 2026-06-05 (open-ended); minted table range (not located on disk).

## Notes
- No non-client need window is declared in this project's decompositions, PRD or open order; the 365-day rule therefore moves no window here.
- The 2024-01-01 landing gate (round 5, RULING B) is a block on landing and grading, not a read window; it is not in the windows list.
- Nothing was deleted, narrowed, rebuilt, re-run, fetched or served. No account id or account value is printed.
