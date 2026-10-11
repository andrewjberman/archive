# IB142-1 (IB-pr-445) -- the unmoved-bar guard: the overlap table again under it, three sizings, and what it un-grades

READ ONLY; a SIZING and a TABLE, not a stamp. Nothing built, served, re-graded or admitted in the product. Counts only; no account id, balance, quantity or single account's holding.
Same 85 trading days (2026-06-10 to 2026-10-09). Data: `IB142-1_unmoved_bar_guard.json`. Scripts in this folder: `ib441_fetch_s3.py`, `ib441_fetch_tx.py`, `ib433_fetch.py` (partitions, transactions table), `ib441_prepare.py`, `ib442_phase1.py`, `ib442_prepare.py`, `ib445_tickers.py` (the one list, counted before fetching), `ib441_fetch_yahoo.py` (the one pass), `ib445_measure.py` (the guard, Table 1, the sizings, the control; it imports `ib441_measure.py` and `ib442_measure.py` unchanged).

**The guard.** The reader's (Yahoo Finance unadjusted Close) bar for day t equals its bar for the prior trading day (relative 1e-4) => the second witness gives NO grade for that security on t; a security-day no witness grades is ungradeable. The first witness grades every security it carries, as today.

## The two reproductions (both hold)
- **Guard off = IB-pr-441's Table 1:** 894 securities, 64,536 security-days, equal 63,720, one day off 5, neither 499, no bar 312; every type's row equals IB138-2's too. TRUE.
- **Seven types, no guard = IB-pr-442's sizing:** blank 50.305 percent, never served 357, freed (no other ungradeable kind) 5,666, claims 37,592 / 107 / 25,498 / 13,599, eligible 75,796, served 37,667. TRUE. **Same account-days read: TRUE** (43,310 / 55 / 19,832 / 13,599; present 76,796).

## 1. Table 1 under the guard (894 securities, 64,536 security-days)
Total: equal 62,649; one day off **0**; neither 440; no bar 312; not graded under the guard **1,135** (1.76 percent). Of the 1,135: 1,071 were `equal`, 59 `neither`, 5 `one_day_off`.
`R/B` = Securities Issued by Registered Investment Companies or Business Development Companies; `ETS` = Exchange-Traded Equity Securities.

| type | securities | security-days | equal | one day off | neither | no bar | not graded | equal on moved-close days |
|---|---|---|---|---|---|---|---|---|
| ETS / Not Available | 479 | 36,863 | 36,019 | 0 | 278 | 279 | 287 | 35,933 |
| R/B / ETF | 28 | 2,137 | 2,076 | 0 | 2 | 0 | 59 | 2,072 |
| R/B / A | 6 | 411 | 408 | 0 | 0 | 0 | 3 | 407 |
| R/B / No Load | 10 | 391 | 386 | 0 | 0 | 0 | 5 | 379 |
| R/B / Other | 15 | 857 | 845 | 0 | 0 | 0 | 12 | 834 |
| R/B / Retirement | 4 | 116 | 111 | 0 | 0 | 0 | 5 | 107 |
| R/B / Inv | 2 | 91 | 83 | 0 | 0 | 6 | 2 | 83 |
| R/B / Inst | 31 | 1,474 | 1,283 | **0** (was 2) | 3 | 0 | 188 | 1,264 |
| R/B / Not Available | 123 | 8,596 | 8,126 | **0** (was 3) | 92 | 0 | 378 | 8,098 |
| Cash and Cash Equivalents / Not Available | 1 | 85 | 2 | 0 | 0 | 2 | 81 | 0 |
| Not Available / Not Available | 141 | 9,882 | 9,788 | 0 | 19 | 25 | 50 | 9,734 |
| MIXED | 54 | 3,633 | 3,522 | 0 | 46 | 0 | 65 | 3,505 |

Every type's one-day-off column is empty under the guard, so all 12 types are listed as empty (`one_day_off` 0 and `equal` above 0). That is the table's arithmetic, not an admission: Cash has 0 days equal on which the close moved (listed separately in the json), and this cell admits no class.
**The five earlier one-day-off security-days all land in `not_graded_under_the_guard`:** SHM 2026-06-30, MEIIX 2026-07-02, SHM 2026-07-20, PZA 2026-07-31, MISIX 2026-10-09. On each the reader's bar for t equals its bar for the prior day while the anchor moved (the dangerous direction). **No one-day-off entry remains under the guard.**
`neither` after the guard: 440 (was 499). The guard moved it in one type only: ETS / Not Available (337 to 278, 59 neither-days were on an unmoved reader bar). `equal on days the close moved`: 62,418 to 62,416 (two security-days sit on the 1e-4 tolerance edge: the reader's two bars agree within 1e-4 while the anchor's two closes differ by just over it; INFERRED from the counts).

## 2. Three sizings (the same 76,796 account-days; assumption in the json)
| | seven, no guard | seven, under the guard | seven + Inst, under the guard |
|---|---|---|---|
| UNGRADEABLE / PRIOR / OWN / NOTHING | 37,592 / 107 / 25,498 / 13,599 | 38,147 / 104 / 24,946 / 13,599 | 33,040 / 161 / 29,996 / 13,599 |
| eligible, served, blank | 75,796; 37,667; 38,129 | 75,796; 36,569; 39,227 | 75,796; 40,704; 35,092 |
| blank share | 50.305 % | **51.753 %** | **46.298 %** |
| accounts never served (of 999) | 357 | 357 | **283** |
| freed, no other ungradeable kind | 5,666 | 5,114 | 10,164 |
These are sizings, not stamps.

## 3. What the guard costs in the seven admitted types
**552 account-days no longer freed** (5,666 to 5,114; 5,737 to 5,185 of every kind). 4,649 row-days not graded (of 104,247 rows of admitted-type securities outside the first witness); 367 security-days (of 12,832 with both bars, 85-day basis; 306 on days an account holds it), on 68 securities. Blank share +1.45 points; never served unchanged at 357.
Carrying most (row-days; days unmoved of 85): FXNAX 1,813 (11), FLCOX 808 (4), FFBOX 440 (13), FSGGX 385 (3), FSPGX 285 (2), FSMAX 266 (2), FCSTX 198 (41), ACTSX 104 (26), FNFWX 72 (2), RPMT 35 (11). **No admitted-type security outside the first witness is un-graded on more than half its days.** Among the overlap securities: SWVXX (Cash) 81 of 81 days, CMRF (ETS) 59 of 85, CLIP (R/B Not Available) 48 of 85, SGOV (R/B Not Available) 11 of 16, JSOSX (R/B Inst) 58 of 75.
**Inst under the guard:** 71 securities outside the first witness (all 71 have bars); 102,812 row-days, 93,122 graded, **9,690 left ungraded** by the guard; 927 of 6,035 security-days unmoved; six Inst securities un-graded on more than half their days (BISOX 79 of 85, GPPIX 78, JSOSX 67, EIBLX 60, OLCYX 57, ADLYX 49). **Adding the class frees 5,050 account-days** (5,114 to 10,164).

## 4. To the cent
Equal-to-the-cent is not a stricter reading than 1e-4: for prices above about 50 a cent is inside 1e-4. Overlap table: 943 security-days un-graded to the cent against 1,135 relative (30 only by the cent reading, 222 only by the relative one: 192 fewer net); one-day-off still 0. Seven types outside the first witness: 447 security-days to the cent against 367 (102 and 22: 80 more), row-days 4,449 against 4,649 (200 fewer); freed 5,113 against 5,114; with Inst freed 10,180, blank 46.257 percent.

## 5. The one pass, the control
Yahoo Finance only, via `fetch_yahoo` / `read_yahoo_close` (unedited), window 2026-06-05 to 2026-10-13: counted BEFORE fetching 1,024 distinct tickers (890 overlap + 154 admitted-type outside + 71 Inst outside; 73 and 18 also in the overlap) against the 1,500 stop; **21 calls (20 of 50, one of 24), each ticker asked once**, 1,018 with bars, 6 with none, none rate-limited, paced 8 s, none parallel. No YCharts, no Bloomberg.
**Control (planted equals read):** one security over five days whose reader bar repeats on day 3: day 3 reads `not_graded_under_the_guard`, days 1, 2, 4, 5 `equal`; with the guard off all five read `equal`; where the anchor moves on day 3 the guard-off reading is `one_day_off` and the guarded one not graded; an account-day holding it on day 3 is not freed, on days 2 and 4 it is. `ib445_measure.py --control` prints EQUAL: True.
