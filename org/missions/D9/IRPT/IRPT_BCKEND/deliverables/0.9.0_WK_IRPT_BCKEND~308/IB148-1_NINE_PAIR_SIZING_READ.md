# IB148-1 (IB-pr-452) -- nine admitted pairs under both guard sentences, the same with five securities not graded, and the securities that mostly repeat

READ ONLY; counts only; nothing built, served, re-graded, admitted or excluded in the product. This cell sizes and recommends nothing on the exclusion. Same 85 trading days (2026-06-10 to 2026-10-09). Data: `IB148-1_nine_pair_sizing.json`; script `ib452_measure.py` (IB-pr-445's sizing code generalised to a set of admitted classes, a guard mode and a not-graded list; the product guard `second_witness_grades` is imported and called, not reproduced).

## The three numbers the CTO asked for
1. **Nine pairs, both guard sentences:** blank share **43.92 percent** (33,291 of 75,796 eligible), **247** accounts never served, **12,482** account-days freed (holding no other ungradeable kind).
2. **The same with ADLYX, BISOX, EIBLX, GPPIX, OLCYX not graded:** blank **43.92 percent** (33,292), **248** accounts never served, **12,472** freed. The five's cost: **10** account-days no longer freed, **1** account no longer ever served, **787** row-days held across the five.
3. **Securities repeating on more than half their days: 7.** Six are Inst (BISOX, GPPIX, JSOSX, EIBLX, OLCYX, ADLYX), one is Not Available (SGOV). All five of the CTO's names are in the list.

## Reproduction (holds)
Seven pairs plus Inst under guard sentence (1) alone: blank 46.298 percent, never served 283, freed 10,164; the four claims (UNGRADEABLE 33,040; ACCT_PRIOR_DATE 161; ACCT_OWN_DATE 29,996; NOTHING_TO_GRADE 13,599; present 76,796) equal IB-pr-445's member for member.

## Sizing
| | UNGRADEABLE | ACCT_PRIOR_DATE | ACCT_OWN_DATE | NOTHING_TO_GRADE | blank % | never served | freed |
|---|---|---|---|---|---|---|---|
| seven + Inst, sentence (1) alone (IB-pr-445) | 33,040 | 161 | 29,996 | 13,599 | 46.298 | 283 | 10,164 |
| nine pairs, sentence (1) alone | 30,661 | 222 | 32,314 | 13,599 | 43.9218 | 247 | 12,482 |
| nine pairs, both sentences | 30,661 | 222 | 32,314 | 13,599 | 43.9218 | 247 | 12,482 |
| nine pairs, both, the five not graded | 30,671 | 222 | 32,304 | 13,599 | 43.9232 | 248 | 12,472 |

**The second sentence's cost is 0 freed account-days** (12,482 under sentence (1) alone, 12,482 under both). The sizing's row grade already treats a missing prior-day bar as no grade, so the sentence was in force in every earlier sizing of this chain (row IRPT_BCKEND-D2-W308-S1).

## The five's cost by ticker (counts only)
| ticker | row-days | accounts holding it | row-days the guard grades |
|---|---|---|---|
| ADLYX | 16 | 1 | 8 |
| BISOX | 85 | 1 | 6 |
| EIBLX | 30 | 1 | 7 |
| GPPIX | 252 | 6 | 12 |
| OLCYX | 404 | 6 | 125 |

## Securities outside the first witness that repeat on more than half their days
Rule: for a security of the nine pairs outside the first witness with bars, days with a bar over the 85 graded days; days not graded = days the product guard (both sentences) gives no grade; it repeats when 2 x not graded > with a bar.

| pair | outside, with bars | repeating |
|---|---|---|
| Exchange-Traded Equity Securities / Not Available | 96 | 0 |
| RIC or BDC / A | 7 | 0 |
| RIC or BDC / ETF | 6 | 0 |
| RIC or BDC / Inv | 0 | 0 |
| RIC or BDC / No Load | 8 | 0 |
| RIC or BDC / Other | 25 | 0 |
| RIC or BDC / Retirement | 10 | 0 |
| RIC or BDC / Inst | 71 | 6 |
| RIC or BDC / Not Available | 77 | 1 |

Listed (days not graded of days with a bar; row-days): BISOX 79 of 85 (85); GPPIX 78 of 85 (252); JSOSX 67 of 85 (22); EIBLX 60 of 85 (30); OLCYX 57 of 85 (404); SGOV 53 of 85 (145); ADLYX 49 of 85 (16). **JSOSX** counts as outside the first witness on this cell's rule (an OUTSIDE_ANCHOR row on some graded day, 22 row-days) although the anchor carries it on most days (row IRPT_BCKEND-D2-W306-S1); it is in the list.

## The pass and the control
Yahoo Finance only (`fetch_yahoo` / `read_yahoo_close`, unedited), window 2026-06-05 to 2026-10-13. Counted BEFORE fetching: 303 distinct tickers (154 admitted-type, 71 Inst, 78 Not Available, outside the first witness), under the 1,500 stop. 7 calls (six of 50, one of 3), each ticker asked once, 298 with bars, 5 with none (recorded, never re-asked), none rate-limited, paced 8 s, none parallel. No YCharts, no Bloomberg; S3 reads only.
**Control (planted equals read):** a planted security of an admitted pair whose bar moves, repeats, moves again, with a gap: an account-day holding it on a moved day is freed with the security graded and not freed when it is in the not-graded list; on the repeated day and the day after a missing bar it is not freed. `ib452_measure.py --control` prints EQUAL: True.

## Assumed and not established
Assumed: these are sizings, not stamps (see `what_is_assumed`). Not established: whether to admit any pair or exclude any security; whether the five's moved days are dated right (no anchor close exists for them); why the bar repeats; that a freed account-day's claim would be correct; anything outside the 85 days, the 303 tickers, or the securities with no ticker, no type, mixed or another type; the five tickers with no bars (their rows block).
