# MDPF_DEMQUE round 9 -- the 14 lock-rejected names, cause classed (2.0.0_SA_COO~Q1)

Run 2026-10-11T16:00:23Z on dell1: `lock_cause.py` (TO-DQ-t32 @bd3f71a021) over every name still on the original three columns (14), each with a fresh paced Yahoo pull (14 of 14 `pull_status` OK) against the served file and the client's trade prices (transactions `date=2026-06-23`, trades through 2026-06-22). Then `hold_lock_records.py --apply`: 14 lock.json written, second apply skipped 14 (idempotent); claim `held` with the stated reason; versioning on (bucket Enabled), pre-write bodies and version ids saved.

| symbol | cusip | type | agreement old | agreement new | dates | first lock before the floor | cause |
|---|---|---|---|---|---|---|---|
| RPIFX | 77958B402 | Mutual Fund | 39.2 | 39.2 | 651 | True | wrong-symbol |
| FTHSX | 14064D865 | Mutual Fund | 40.7 | 40.7 | 627 | True | wrong-symbol |
| PFORX | 693390882 | Mutual Fund | 42.9 | 42.9 | 513 | True | wrong-symbol |
| VSEIX | 4812A1373 | Mutual Fund | 77.2 | 77.2 | 329 | True | never-met-floor |
| IWO | 464287648 | ETF | 79.2 | 79.2 | 240 | True | never-met-floor |
| VSS | 922042718 | ETF | 79.3 | 79.3 | 193 | True | never-met-floor |
| IWP | 464287481 | ETF | 80.6 | 80.6 | 242 | True | never-met-floor |
| MISIX | 92647K309 | Mutual Fund | 82.0 | 82.0 | 748 | True | never-met-floor |
| HLMEX | 412295701 | Mutual Fund | 82.3 | 82.3 | 141 | True | never-met-floor |
| IWN | 464287630 | ETF | 83.2 | 83.2 | 244 | True | never-met-floor |
| IWS | 464287473 | ETF | 83.3 | 83.3 | 240 | True | never-met-floor |
| LCEYX | 00141B204 | Mutual Fund | 87.2 | 87.2 | 211 | True | never-met-floor |
| VWO | 922042858 | ETF | 87.2 | 87.2 | 313 | True | never-met-floor |
| PIMSX | 92828R610 | Mutual Fund | 87.6 | 87.6 | 275 | True | never-met-floor |

## Reading

- **No draw-column defect:** all 14 have `agreement_old_pct == agreement_new_pct`. The served file and the fresh draw agree with the trades to the same percentage, so the re-draw did not change the price column.
- **11 never-met-floor** (agreement 77.2 to 87.6): each name's first lock (2026-10-09 02:38Z) pre-dates the 90 pct floor (`52b8a3cca2`, 2026-10-09T03:35Z); the file was locked without meeting it. Serve claim `held`, as ruled.
- **3 wrong-symbol by the rule (both below 60): RPIFX 39.2, FTHSX 40.7, PFORX 42.9.** The CTO's ruling named two names near 40; the table reads three. All three are Mutual Funds.
- **Client-page use, read from the positions snapshot** (`silver/positions/date=2026-06-23`, one partition, AsOfDate 2026-06-23): FTHSX held by 4 accounts (Account_Status 0), PFORX by 11 (status 0), RPIFX by 0 (no position row). That the pages value those holdings with these price files was NOT traced here.
- **Not claimed:** that FTHSX, PFORX or RPIFX is the wrong security (the rule classes agreement below 60 on both sides; the symbol was not re-resolved), or why the 10-09 lock passed (its floor-less rule was in force at the time).
