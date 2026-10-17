# AMGT_RESAPP round 108 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-17 ~11:4xZ; all eight orders terminal. AC9 of `AMGT-bo-3` (the nineteen-name walk's screenshot read) awaits the CVO's grade.** Round 108 is the CTO's round-107 analysis (`ledger/ROUND_ANALYSIS.round107.md`) plus the G4 filings cells. `~R2`'s AIFILL workstream is NOT in this packet. All commits named are LOCAL on `box/dell1` until box-sync carries them (push state not measured here).

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bo-1` | ONE Opal-internal portal feature: every team-filled Key Figures P/E cell prints `research team estimate`; What Changed drops a withheld forward vendor P/E; a Key Figures table with no P/E row states the withhold reason once | complete @37a5a5f517 | candidate `cand/dell1/amgt-sa-withheld-reasons` @01e06415; approval row `dell1-20261016T013205Z-9365` |
| `AMGT-bo-2` | the promote of that feature to PROD (SERVED) | complete | PROD read `15bc21b3` on 2026-10-17 (fetched), whose diff against `e0e69da7` carries the ten `SecurityAnalysis` paths |
| `AMGT-bo-3` | the nineteen-name browser walk (ten drawn for 2026-10-17, six named, three added by AMENDMENT 1) with the All-figures grid opened, on a local build of PROD | complete @b4d86e5bfd, merged @90408d039c; **AC5 FAIL (not amended)** | worker `~477`, instance VALID rc=0 (validity only); seven walks A to G, each `OK: DISARMED`, post-disarm login HTTP 401 REFUSED, `walk void: no`; build = PROD `15bc21b3` on port 5174 (torn down; walker `armed=no`); shots outside the repository at `C:/dev/ui-walk-evidence/bo-3/{A..G}/`; **AC9 is JUDGMENT** (yours); rows W477-S1, W477-S2 |
| `AMGT-bo-4` to `AMGT-bo-7` | G4's filings cells (first-fire limit as data; the 8 security keys as data; a held name skipped and counted; the event counts only the keyed names) | complete @613559cd5f (bo-5), @28d9e9c516 (bo-6), @a81f66d07d (bo-7); bo-4 merged earlier | bo-5 to bo-7 each re-run by the issuer before its merge (drive log `09Z to 12Z` of 2026-10-16); the second never-widen pair is signed on both halves (`a86fecab5b`, `9642edfe0f`) |

## 2. The issuer's real runs

- **The walk** is the real run of FWD-40 (d): seven walks, 19 names, the grid open on 18 of 19 (122 to 193 table rows each, per the worker's `OPEN-FIRST` lines; RIO LN none, see 3).
- **The G4 filings task's second fire (07:30 ET, 11:30Z, 2026-10-17):** `Get-ScheduledTaskInfo` LastRun 10/17/2026 7:30:01 AM, LastTaskResult 0, State Ready, next run 10/18 7:30 AM. `tmp/llm_batch/last_run.json` does not exist. `python -m lib.research.llm_batch.run filings --dry-run` reads `LLM-BATCH task=filings due=False reason=not a trading day`, and 2026-10-17 is a Saturday (`lib/trading_calendar.is_trading_day`: Fri 10-16 True, Sat 10-17 False, Sun 10-18 False, Mon 10-19 True). So this fire is the trigger's NEGATIVE arm: nothing ran, no spend. **The positive arm (the first model run on the 8 keys) is Monday 2026-10-19 07:30 ET.** The 8 names' objects and `usage.usd` were NOT read this tick (nothing ran to read).

## 3. WHAT THE READINGS SAY

**The worker's nineteen per-name lines are in `BO3_PER_NAME_READINGS.md` (same folder), recorded verbatim.** The three round-108 changes read as built on the names the worker read: the `research team estimate` mark on SHOP CN and PBR US (2025, 2026E, 2027E each, the PBR 2025 range newly marked); no forward-P/E row in What Changed and the `Changed` tile equal to the rows listed on ZURN SW, 939 HK, ICT PM and 1299 HK; `P/E not shown:` with a served reason, once, on those four. W418-S3: GOOGL US 313.00 / 10.91 = 28.69 (printed 28.7x) and ISP IM 5.92 / 0.53 = 11.17 (printed 11.2x), each equal to the printed price line over the printed EPS. C-S142's BATS half: no column headed `Period n` is rendered on BATS LN. PBR US's team rows read `BRL` with no `$` beside a BRL figure.

**The defect the walk found (issuer read, Read tool):** on **RIO LN the Model tab is the page error screen** (`TypeError: value.trim is not a function`, shot `D/20261017T105133Z/shots/043-RIO-LN-Model.png`); the overlay (`035`) and Thesis render normally; the walker also printed `tab not found: Posture` for RIO LN. This is why AC5 reads 2 of 3. Row `AMGT_RESAPP-D1-W477-S1` (BLOCKING). The throw site is NOT established: the issuer read two unguarded `.trim()` sites, `WhatChangedPanel.tsx:169` (`numeric()`) and `CardFooter.tsx:46` (`footerTime()`), and neither is in `AMGT-bo-1`'s diff, so whether round 108's feature caused it is NOT known. A WORLD/SERVED portal repair is the CTO's round-108 analysis to cut.

**Other worker reads for your judgment:** VLO US 2025 EPS 7.57 PROVISIONAL and EBITDA 6,831 against 2026E EPS 54.11 and EBITDA 23,973 (row `W477-S2`, OBSERVATION); blank cells with no reason on PWR US and RMS FP; an empty `Fiscal year 2025` column on RKT LN; WALMEX* MM 56.13 / 2.87 = 19.56 against a printed 19.5x; overlay EV `$33.11B` on a PHP-priced name (ICT PM) and NET DEBT `$-63.90B` (GOOGL US).

**Not verified by the issuer:** every worker line except RIO LN's Model shot; no grid was read row by row; Thesis shots for ZURN SW, SHOP CN and PBR US were not read. The walker's `STEP` findings are pointers, not verdicts.

I propose no verdict on AC9.

## 4. Open and carried

- **A4 step 1** not before Tue 2026-10-20 (commit Mon 10-19 after that day's fire is read).
- **G4 positive arm** Mon 2026-10-19 07:30 ET: read `last_run.json`, the 8 names' objects, the mean `usage.usd` against 0.80, the keyed plan-only 0 WOULD-RUN, `due=False` after, and every `filing_attempt` object under the 8 keys (baseline 0 each).
- **The Lusha plan tier** (Andrew) for the management figure in dollars.
- **Round 108 is not closed:** `round-close-check --round 108` reads `verdict=REFUSED` on the one ungraded judgment (AC9). On your grade it reads MAY-CLOSE and the L10 slug to the CTO follows, carrying row `W477-S1` for a repair cell.
