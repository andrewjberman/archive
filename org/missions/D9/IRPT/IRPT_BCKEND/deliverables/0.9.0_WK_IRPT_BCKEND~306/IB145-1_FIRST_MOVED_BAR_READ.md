# IB145-1 (IB-pr-449) -- the reader's first moved bar after a repeated run, the six's moved days, and the no-prior-bar count

READ ONLY; counts only; nothing built, served, re-graded or admitted in the product; no class is admitted and none recommended. Same 85 trading days (2026-06-10 to 2026-10-09). Data: `IB145-1_first_moved_bar.json`; script `ib449_measure.py` (imports IB-pr-445's `ib441_measure.py` / `ib445_measure.py` classifiers unchanged; the S3, transactions, prepare and Yahoo scripts are copies of the earlier cells').

**Reproduction (holds).** The overlap table under the guard was rebuilt from the same S3 objects: 894 securities, 64,536 security-days, and every one of the twelve types equals IB-pr-445's row. The two pairs: Inst 1,283 equal / 0 one day off / 3 neither / 0 no bar / 188 not graded under the guard; Not Available 8,126 / 0 / 92 / 0 / 378. Both equal the ~303 record.

**Rules.** A repeated run is a maximal sequence of consecutive trading days on each of which the reader's bar exists and equals the prior trading day's bar (relative 1e-4); a day with no bar ends a run. The first moved day is the first later day in the window on which the reader has a bar and a prior bar that differ; it is placed against the anchor as no anchor that day, else equal to the anchor's close that day, else equal to the anchor's close for the prior trading day (a late bar), else neither.

## Table A -- the runs and the first moved day (overlap securities of the two pairs)
| | R/B / Inst | R/B / Not Available |
|---|---|---|
| securities | 31 | 123 |
| securities with a repeated run | 25 | 67 |
| repeated runs | 181 | 368 |
| days in runs | 268 | 480 |
| run lengths (length: runs) | 1: 145, 2: 18, 3: 4, 4: 6, 5: 3, 6: 2, 8: 3 | 1: 293, 2: 51, 3: 13, 4: 9, 5: 2 |
| first moved day equals the anchor, same day | 121 | 295 |
| equals the anchor, prior day (a late bar) | **0** | **0** |
| equals neither | **0** | **0** |
| no anchor that day | 54 | 72 |
| no moved day in the window | 6 | 1 |
| side: neither-runs whose bar equals an anchor close inside the run | 0 | 0 |
| side: run days the anchor moved while the reader did not | 2 | 5 |
| side: run days the anchor also did not move | 184 | 373 |
| side: run days with no anchor | 82 | 102 |
| no-prior-bar sentence: security-days un-graded | 0 | 0 |

In both pairs every first moved bar that has an anchor close that day equals it (121 of 121, 295 of 295); no run's first moved bar is a late bar or matches neither. Every first moved day is the day right after its run (0 exceptions). The no-anchor outcomes (54, 72) are not graded.

## Table B -- the six (outside the first witness except as noted); days of the 85
| ticker | days with a bar | unmoved | moved | no prior bar | moved under 0.1 percent | anchor carries it | rows held on moved days | same day / prior day / neither |
|---|---|---|---|---|---|---|---|---|
| ADLYX | 85 | 49 | 36 | 0 | 0 | no | 8 | 8 / 0 / 0 |
| BISOX | 85 | 79 | 6 | 0 | 6 | no | 6 | 6 / 0 / 0 |
| EIBLX | 85 | 60 | 25 | 0 | 0 | no | 7 | 7 / 0 / 0 |
| GPPIX | 85 | 78 | 7 | 0 | 7 | no | 12 | 12 / 0 / 0 |
| JSOSX | 85 | 67 | 18 | 0 | 14 | **yes, 75 of 87 axis days** | 23 | 23 / 0 / 0 |
| OLCYX | 85 | 57 | 28 | 0 | 0 | no | 125 | 125 / 0 / 0 |

They are the six IB-pr-445 named. On every moved day, every priced held row of each of the six equals the reader's bar for that day, none the prior day's. Rows of the security on those days with no price (not graded, outside the three outcomes): ADLYX 28, BISOX 0, EIBLX 18, GPPIX 28, JSOSX 13, OLCYX 22. JSOSX is carried by the anchor on most days (the same security is in the overlap table); the 23 rows include days the anchor carries it, where IB-pr-445's sizing held only 2 as outside the first witness. Kind of fund: for each, the holdings rows give only a name (American Beacon DoubleLine Floating Rate Y; BlackRock Short Obligations Instl; Eaton Vance Floating Rate I; Goldman Sachs Short-Term Conservative Income Instl; JPMorgan Strategic Income Opportunities I; Invesco Limited Term California Municipal Y) and the transactions table types all six Inst; neither says a money-market or stable-value fund or a constant price, so that is not told.

## Table C -- AMENDMENT 1: the no-prior-bar sentence (PRD v0.41), all twelve types of the overlap table
Where the reader has no bar for the trading day before t, it gives no grade on t. Over the 64,536 security-days, this sentence un-grades **6** that IB-pr-445's guard graded, **all 6 of them `equal`**: Exchange-Traded Equity Securities / Not Available 3, Cash and Cash Equivalents / Not Available 2, Not Available / Not Available 1; the other nine types 0 (the two pairs 0 and 0). The prior trading day of 2026-06-10 is 2026-06-09, inside the fetch window (from 2026-06-05), so the first day is graded like any other and counted if its prior bar is missing.

## The pass and the control
Yahoo Finance only, `fetch_yahoo` / `read_yahoo_close` unedited, window 2026-06-05 to 2026-10-13. Counted BEFORE fetching: 895 distinct tickers (the overlap's 890 plus the five of the six not in it), above the order's 400, so under AMENDMENT 1's 1,100 for the all-types count. 18 calls (17 of 50, one of 45), each ticker asked once, 891 with bars, 4 with none (recorded, never re-asked), none rate-limited, paced 8 s, none parallel. No YCharts, no Bloomberg; S3 reads only.
**Control (planted equals read):** a five-day series whose bar repeats on days 2 and 3 and moves on day 4 to the anchor's day-4 close reads `equals_the_anchor_same_day`; one whose day-4 bar is the anchor's day-3 close reads `equals_the_anchor_prior_day`. `ib449_measure.py --control` prints EQUAL: True.

## Not established
Whether to admit or refuse the class (none recommended); why the bar repeats; the bar on a moved day with no anchor close (54 + 72 runs, ungraded); anything about the other ten types beyond the count of Table C; days after 2026-10-09; any grade of the six other than against the reader's own bar; rows with no price; the size of an error (none was found in the two pairs, so none is sized).
