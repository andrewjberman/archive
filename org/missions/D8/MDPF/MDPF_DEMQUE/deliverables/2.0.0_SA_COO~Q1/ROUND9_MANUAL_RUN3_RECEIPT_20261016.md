# The third Yahoo pass, on the 600 cap with the empty cooldown: receipt (2.0.0_SA_COO~Q1, 2026-10-16 ~2:00 AM ET)

Run: scheduled task `Opal MDPF_DEMQUE daily draw`, started BY HAND at 12:08:01 AM ET (04:08:01Z) by this seat's own one-shot cron (the second pass Andrew's "do yahoo runs now" authorised); same wrapper, same log (from line 432). It ended at about 1:57 AM ET with `OK: daily draw complete`. Cap 600 (DQ-t-71 @a35132030f), empty-symbol cooldown of 7 days (DQ-t-72 @99d9ef63b2). The pacer day rolled to 2026-10-16 at the first request (the state file's `day` field is only rewritten then; the roll was tested on a copy of the file before the start).
Read AFTER it ended, read-only: the log summary line, `pacer.json`, S3 `list_object_versions` against `STORE_BASELINE_AFTER_2026-10-15_RUN2_VERSIONS.csv` (711 names; the older RUN file the cron prompt names predates run 2), and the stored index object. Next base: `STORE_BASELINE_AFTER_2026-10-16_RUN3_VERSIONS.csv` (937 names). Covered by the signed never-widen pair; the stop (a non-zero exit or a write outside its table) did not fire.

## 1. Pushback (the CTO's read before any further step)

| signal | value |
|---|---|
| requests | 600 of 600 on pacer day 2026-10-16; pacer `pushback` false, `factor` 1.0 |
| 429 as a rate-limit response, "Too Many", "timed out", "Timeout", connection errors | 0 (the two text hits for "429" are digits inside the run's one summary line, CUSIP numbers) |
| HTTP 404 (unknown symbol) | 2 (LAYN, LVNTA) |

No pushback sign at 600. The cap holds at 600; no further step is taken in this receipt.

## 2. The run's claim against the store

| check | result |
|---|---|
| keys the run says it wrote (incremental) | 71; actual changes on the 711 baseline names: 35 `prices.parquet`, 35 `lock.json`, 1 `dividends.parquet` = 71, each on a name in the run's appended list; 0 outside it |
| new names | 226, each with all four files (904 keys); equals the run's 226 `ok` |
| keys outside the pair's table | none: the only other changed keys are the two index files |
| V2-held names touched | 0 among the baseline names; 0 among the new names |
| index | 937 rows (was 711): 528 `NOT_FOR_ACTIVE` (the V2-held names) and 409 `INACTIVE_USE`; 0 rows whose label disagrees with V2 membership |

## 3. What the 600 requests did, with the cooldown

| outcome | names |
|---|---|
| new names written | 226 |
| incremental appends | 35 |
| rejected by the identity lock, not written | 131 (98 `PRICE_MISMATCH`, 33 `LOW_TRADE_AGREEMENT`) |
| unchanged | 9 |
| returned empty (first time asked) | about 200 ("possibly delisted" 201 lines) |

Run 2 spent 138 of its 200 added requests on symbols already known empty and bought 15 new names. This run asked none of the 158 known-empty symbols again (the pacer's `FAILED_EMPTY` rose from 158 to 362, all first attempts) and wrote 226 new names. The cooldown did what it was built for.

## 4. Where the 1,071-name backfill stands

Of the 1,071 symbolled inactive-only names: 675 pulled OK (those that passed the lock are stored, the rest rejected), 346 returned empty, 50 not yet tried. The next run takes the last 50. After it, the symbolled set has been tried once: **409 inactive names stored of 1,705 outside V2** (the other 1,296 are 634 with no symbol in any source, the empties, and the lock rejections). Yahoo cannot fill the rest: the empties are delisted tickers, and the identity lock rejects about 37 to 39 percent of the new names it evaluates (102 of 260 on run 1, 131 of 357 on run 3; no looser rule, CTO msg 5411). Former clients are barred from Bloomberg's quota (Andrew-direct 2026-10-13). What prices those names is a decision for Andrew, not a cap.

Push state: LOCAL (box/dell1), not pushed by this seat.
