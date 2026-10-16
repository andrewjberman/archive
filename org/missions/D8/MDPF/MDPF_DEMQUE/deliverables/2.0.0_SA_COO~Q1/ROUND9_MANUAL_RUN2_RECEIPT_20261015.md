# The first run on the 600-request cap: receipt (2.0.0_SA_COO~Q1, 2026-10-15 ~10:55 PM ET)

Run: scheduled task `Opal MDPF_DEMQUE daily draw`, started BY HAND at 10:13:55 PM ET (02:13:55Z 2026-10-16) on Andrew's "just run it manual"; same wrapper, same log (from line 284). It ended at about 10:52 PM ET with `OK: daily draw complete`. The cap was 600 (DQ-t-71 @a35132030f, CTO ruling msg 6379); the pacer day (local 2026-10-15) already held 400, so the run drew the 200 the new cap added. The task's `Last Result` reads -2147020576 afterwards: the 10:30 PM trigger fired while this run held the task and was ignored (`MultipleInstancesPolicy` IgnoreNew), as read before the run; it is not a failure of this run.
Read AFTER it ended, read-only: the log summary line, `pacer.json`, S3 `list_object_versions` against `STORE_BASELINE_AFTER_2026-10-15_RUN_VERSIONS.csv` (696 names). Next base: `STORE_BASELINE_AFTER_2026-10-15_RUN2_VERSIONS.csv` (711 names). Covered by the signed never-widen pair; the stop (a non-zero exit or a write outside its table) did not fire.

## 1. The pushback read the CTO asked for (before any further step)

| signal | value |
|---|---|
| requests | 600 of 600 (400 earlier that pacer day, 200 in this run) |
| pacer `pushback` flag, `factor` | false, 1.0 |
| `429` or "Too Many" in the run's log lines | 0 |
| "timed out", "Timeout", connection errors | 0 |
| rate-limit text | 0 |
| HTTP 404 (unknown symbol) | 2 |
| "possibly delisted" (an empty frame; the symbol has no data) | 139 |

No pushback sign. The CTO's rule (hold at the last clean step on the first sign of pushback) does not fire. The empties are not pushback; they are symbols Yahoo has no data for.

## 2. The run's claim against the store

| check | result |
|---|---|
| keys the run says it wrote (incremental) | 72: 38 `prices.parquet`, 33 `lock.json`, 1 `dividends.parquet`; actual changes on the 696 baseline names equal that exactly, each on a name in the run's appended list; 0 outside it |
| new names | 15, each with all four files (60 keys); equals the run's 15 `ok` |
| keys outside the pair's table | none: the only other changed keys are `index/index.parquet` and `index/index.csv` |
| V2-held names touched | 0 among the baseline names; 0 among the new names |
| index | 711 rows (was 696) |
| rejected by the identity lock, not written | 7 (5 `PRICE_MISMATCH`, 2 `LOW_TRADE_AGREEMENT`) |
| unresolved rows | 520 (was 508) |

## 3. What the extra 200 requests bought, and why: 15 new names, not 200 requests of progress

The pacer holds 158 symbols as `FAILED_EMPTY` (real tickers of delisted or acquired securities: AEPI, AKS, ANR and the like; only 2 look like a CUSIP). `Pacer.done` skips an `OK` symbol only, so a known-empty symbol is asked again on every run: **138 of this run's 200 added requests went to symbols already known empty**, 38 to incremental appends, 15 to new names, 7 to rejects. A cap step alone is therefore mostly spent on retries. Cell `DQ-t-72` (decomposition amendment 31) makes a symbol that returned empty within 7 days cost no request; a transient failure is `FAILED_REFUSED`, not `FAILED_EMPTY`, so it is not hidden.

Push state: LOCAL (box/dell1), not pushed by this seat.
