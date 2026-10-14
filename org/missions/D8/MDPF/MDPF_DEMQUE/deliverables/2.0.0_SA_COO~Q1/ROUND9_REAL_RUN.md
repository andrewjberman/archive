# ROUND 9 REAL RUN -- the L8 packet for 3.0.0_SA_CVO, DRAFT (2.0.0_SA_COO~Q1, MDPF_DEMQUE, drafted 2026-10-14; NOT DELIVERED)

**Status of this file: a DRAFT kept current while round 9 runs. It is not the L8 packet until the section "What is still owed" is empty and the issuer sends it to `3.0.0_SA_CVO` with its blob hash.** Nothing below is a grade; the CVO grades the judgment criterion.

## 1. What round 9 delivered: cell, drain commit, worker, what it did

| cell | drain commit | worker | what it did (issuer's merge subject, shortened) |
|---|---|---|---|
| t-32 | `bd3f71a021` | ~25 | lock_cause + hold_lock_records (dry-run), |
| t-33 | `4def446d78` | ~26 | remaining-cells re-quote, trading-day history cells, COMPLETE, chained re-freeze |
| t-35 | `9ae2f2d054` | ~27 | read-only valuation trace and re-resolve (production bucket opal-data-cot, bridge read, 0 of 15 applied, no candidate at 90) |
| t-36 | `df9aaa34cc` | ~28 | the extension refuses a frontier before the store's latest valid_to |
| t-37 | `8e63ec0a23` | ~29 | the extension refuses a --today after the local date and its tests pin the clock |
| t-38 | `1bb7035580` | ~30 | each lock row states trades_through beside its claim |
| t-39 | `89007f31a2` | ~31 | a name whose pull adds a split row keeps its prior files (CTO half condition) |
| t-40 | `34040149bb` | ~32 | batched incremental pull equal to the per-symbol path on 50 of 50 symbols; HTTP requests measured: one per symbol, verdict BATCH_DOES_NOT_REDUCE |
| t-41 | `dbf7bacc77` | ~33 | the standing extension is tiered (daily 141+ADVI, IRPT 782 rolling in FWD-9 blocks on a 5-trading-day cycle, cap refusal, --plan-week 7 days max 306 a day) |
| t-42 | `e148463ae6` | ~34 | the lag is declared per tier in ENROLMENT_TIERS.json and --lag-report prints each name's trading-day lag against it (real store: 141 indexed, 127 within, 14 over, rolling... |
| t-43 | `b956c6307e` | ~35 | per-security windows in bbg_quote and the CARD-A P1 slice builder (P1 609 names: 607 priced, 2 FDIC placeholders unresolved, 882,024 cells, 330 trading days at the curren... |
| t-44 | `900406e221` | ~36 | the 2012 floor and need-class refusal on the Bloomberg side (ABNB refused by the 365-day rule, held undrawn per CTO msg 4912), the TR remainder by (security,date) identit... |
| t-45 | `6f6a61123b` | ~38 | the Yahoo side of the queue refuses an undeclared or over-window request (demand_queue.validate, --check-declared), the standing extension declares client from 2013-04-08... |
| t-46 | `1d7ad82723` | ~37 | P1 coverage measured on the merged window: Yahoo in store 0, rejected 5, no symbol 601; Black Diamond units and value 11 names and 126 held days; residual 606 names, 467,... |
| t-47 | `2989e78de8` | ~39 | the research-app model block keeps its 2016 history as the named exception research_app_model_history_2016 (non_client, model_block, window_start 2016-01-01 or later), ev... |
| t-48 | `9de742d8f9` | ~40 | the Yahoo incremental path (last 5 trading days, targeted refill on a gap or a split) built and proved cell-equal: 50 of 50 no-split names, one split arm refilled and equ... |
| t-49 | `567a058ddb` | ~41 | the surface B porting test: its Bloomberg request (326 securities, 2,497 cells, at most 10 each, deterministic sha256 intervals, valid under the queue's rule) and the pur... |
| t-50 | `911d2806c8` | ~42 | the B1 Cottonwood request at option C depth: 614 securities (606 priced P1 plus the 8 rejected funds), 37,514 cells, 18 trading days to finish, PX_LAST with the total-ret... |
| t-51 | `adbdc57967` | ~43 | the porting test always draws 5 intervals (a length that does not fit is replaced by a sha256-drawn length, minimum 5 trading days, a window under 10 trading days is UNTE... |
| t-52 | `0294f140f0` | ~44 | the priority gate: former clients (P3) never drawn, a match-open name (P2) waits, P1 only, on CLIENT requests; rank.py refuses P2 and P3, the extension tiers and the dail... |
| t-53 | `2498d1dabc` | ~45 | DEMQUE's half of C-DEMQUE-SECCLASS-SYNC: key AES (cusip 00130H105) printed equal on the request row, the unresolved list (resolved) and the etf-classifications row, one r... |
| t-54 | `8b7c76ad35` | ~46 | a non-trading-day fire's history room is the measured ceiling plus the trading-day cells production left unused, read from the budget ledger at run time; an absent tradin... |
| t-55 | `450bf78800` | ~47 | the surface E intake cap: 10 percent of the measured 5,858-cell history ceiling = 585 cells; a request above it is refused at intake naming the cap and never split; a one... |
| t-56 | `3885d9eef1` | ~48 | the site Z drawer draws CUSIP entries (a /cusip/ form probed with one row first), dates entries by identity, per-entry fields, the reference channel, skips excluded clien... |
| t-57 | `2ff948f093` | ~49 | the B1 request is clipped to dell2's active Cottonwood set (sha256 verified, 769 accounts, 3,357 securities): 608 CUSIPs, 34,223 cells from 37,439; names outside the set ... |
| t-58 | `ea0dd99e4e` | ~50 | the Yahoo incremental path wired into the nightly draw under never-widen pair A: a stored name takes the five-day window and appends only new rows with total-return colum... |
| t-59 | `7ad0fcd178` | ~51 | a porting_verdict column (last) on the Yahoo store index under never-widen pair B: UNVERIFIED by default, PASS/FAIL/UNTESTABLE read per name from ~/.opal/demque/porting_v... |
| t-60 | `a571c06ff9` | ~52 | the B1 builder reads dell2's active Cottonwood set V2 (commit 4d427d3bbb, sha256 5cef7ab0c9e1..., 41,826 rows, 860 accounts, 3,368 securities); the four bond and T-bill C... |
| t-61 | `0288b4fb5c` | ~53 | the B1 builder takes a named CUSIP list and a request id; the 14 Yahoo-lock-failed daily-tier names build to 14 CUSIPs, 7,685 cells at depth c on the V2 active windows, f... |
| t-62 | `e614d1ad2b` | ~54 | a share-class symbol without a dash (BRKB, BRKA) is pulled from Yahoo in its dash form and keyed as given in the three default fetch paths; live probe BRKB status OK rows... |

Not in the table (their drain was not a `drain(MDPF_DEMQUE.TO-DQ-tN)` commit, or the order is not terminal): `DQ-t-30` (complete), `DQ-t-31` (complete), `DQ-t-34` (pending). `DQ-t-34` is the site Z draw: its AC2 waits on the 2026-10-17 non-trading-day fire (owner `~ZQ`).
Counts at the last `round-close-check.py` read (2026-10-14 ~04:45Z): 33 round-9 orders, 32 complete, 1 not complete (`TO-DQ-t34`); 1 JUDGMENT criterion (`DQ9-t35-AC2`), 0 graded.

## 2. The real runs so far (measured, not asserted)

- **The scheduled Yahoo draw of 2026-10-12 and of 2026-10-13 (22:30 ET, `Opal MDPF_DEMQUE daily draw`).** The 10-13 run (rc 0, 81 minutes; the first with the priority gate, the need-class refusal and the tiers): extension DRAWN 535,407 of 581,955 cells; IRPT P1 PARTIAL 29,124 of 81,270; three other jobs 0 (pacer cap);
  398 names processed, 308 LOCKED and written, 90 REJECTED and not written (74 LOW_TRADE_AGREEMENT, 16 PRICE_MISMATCH); the store grew from 326 to 483 names; unresolved 225; the gate skipped 1; lag: daily tier 130 of 144 within cycle, rolling tier 258 of 259. Source: `.git/demque-daily-draw.log`, `unresolved.csv`, `STORE_BASELINE_AFTER_2026-10-13_RUN_VERSIONS.csv` (every store key's S3 version id after that run).
- **Rehearsal of the wired incremental draw (a LOCAL store copy of five names, the real Yahoo fetch, 2026-10-14):** rc 0; one name appended with a lock extension, two held by the combined relock, one appended without a relock, no crash in the unresolved fold.
- **Whole-store relock census (S3 and the client transactions, read only, 483 names):** applicable 165, locked 151, held 14, not applicable 238 (a trade predates the stored window), no trade rows 80, price-mismatch holds 0.
- **Bloomberg:** nothing has been drawn by this round yet. B1 is filed and quoted (613 CUSIPs, 34,437 cells), the porting test (326 CUSIPs, 3,195 cells), the fund-type check (227 cells), the 14-name request (7,685 cells, CTO-approved), D1 to D5 per the queue form; the first draw is the 2026-10-17 fire at site Z.

## 3. What is still owed before this is the packet

1. `DQ-t-34` AC2: the 2026-10-17 site Z fire, then its receipt read on 2026-10-18 (carry-over printed, `bbg_budget` ledger, which requests drew, the not-drawable list).
2. The first nightly run on the WIRED Yahoo path (2026-10-14 22:30 ET): its receipt against the version baseline (names appended, appended without relock, held restatement, keys written).
3. `DQ9-t35-AC2` (JUDGMENT, the CVO's): the chain from the price file to the client page for FTHSX, PFORX and RPIFX. The original trace carried account numbers and was moved out under the containment ruling (`MOVED_ACCOUNT_DATA.md`); the de-identified chain is `VALUATION_TRACE_DEIDENTIFIED_DQ_t35.md` in this folder.
4. ARMED rows: the surprise tool lists rows with `hazard_standing` ARMED; this seat's disarm evidence files are in `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/` (W24-S1, W36-S2, W37-S1/S3, W38-S2, W48-S1, W50-S2/S6/S10). `MDPF_DEMQUE-D1-W35-S3` is MSTR's to disarm.

## 4. Findings for the CTO's round-9 analysis (the enrichment list candidates)

- **Three funds look like a wrong Yahoo series, not noise (CTO msg 5419):** FTHSX 255 of 627 observations agree (41%), PFORX 220 of 513 (43%), RPIFX 255 of 651 (39%), against 77% to 88% for the other eleven names whose lock fails. All 14 are stuck at 2026-06-23 (78 trading days) and now ride the Bloomberg request `MDPF_SECHIST-CARD-A-B1-YAHOO-FAILED-14`.
- **A residual the signed pair A names:** 238 names append without the combined-history relock because a trade predates their stored window; the receipt lists them each night. A periodic full re-pull would close it (round 10 candidate, not built).
- **Share-class symbol forms:** BRKB sent to Yahoo as BRK-B (`DQ-t-62`); of the 22 empty symbols on 10-13 it was the only dash-form case. The other 21 are delisted, merged or money-market names.
- **A stored-rows relock is not the full-history relock** (row `MDPF_DEMQUE-D1-S17`): the store keeps only the held window, so a name with a trade before it reads REJECTED on the stored rows alone.
- **The 2012 floor, per-security windows, need-class refusal, the surface E cap (585 cells), the non-trading-day carry-over, the priority gate and the active-set windows (V2)** are all merged; none has run against Bloomberg yet.
