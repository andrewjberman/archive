# MDPF_DEMQUE: qualification of every queue item to a two-week Bloomberg budget (2.0.0_SA_COO~Q1, 2026-10-13)

For: `1.0.0_SA_CTO~DELL1` msg 4889 (Andrew-direct law, record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261013_141xZ_BACKFILL_FLOOR_2012_AND_EARLIEST_CLIENT_RECORD.md`,
addenda 1 and 2). Andrew reads this before any new draw.

**Census.** 19 request files read (12 in `requests/`, 7 in the device queue) = **17 distinct request ids**; ADVI and IRPT each also sit as a queue copy.
Sources read: the request files, their quote files, `ledger/BBG_ACTUALS.jsonl` (via `quote_vs_actual.py --all`), the Yahoo ledger
`~/.opal/demque/ledger.jsonl`, and the drawn rows of the TR comparison (`MDPF_DEMQUE_ZQ_T24`, `MDPF_DEMQUE_ZQ_STANDING`). Rank is call 7328's order:
**R1** production daily pulls incl. ETF Positioning, **R2** current clients incl. onboarding, **R3** the rest.

**What is NOT in this table yet, and why.** Cells for the CARD-A P1 slice are computed by DQ-t-43 and DQ-t-44 (worker `~35` is building the window pricing; the
2012 floor, class declaration and refusal rule are the t-44 order). The rows marked *pending* carry no invented number.

## A. Bloomberg items (the budget this table qualifies)

| # | request id | consumer | class | window (old to new) | securities x fields | cells old / new | rank | days of daily quota | decision |
|---|---|---|---|---|---|---|---|---|---|
| 1 | SITEZ-SIGNIN-PREFLIGHT-REFDATA-20261009 | production daily pulls (pre-flight) | production | n/a (reference) | 1 x 1 | 1 / 1 (drawn 10-09) | R1 | 0 | KEEP, done |
| 2 | MDPF_SECHIST-SHT8-TR-FIELD-CONFIRM-20261009 | Positioning page, money-market rule (FWD-9) | production | 2026-10-08 / same | 1 x 1 | 1 / 1 (drawn 10-09) | R1 | 0 | KEEP, done |
| 3 | MDPF_SECHIST-SHT8-TR-FIELD-HISTORY-20261009 | Positioning page, money-market rule | production | 2026-09-28 / same | 2 x 1 | 16 / 16 (drawn 10-09) | R1 | 0 | KEEP, done |
| 4 | MDPF_SECHIST-CARD-A-COT-BBG-HISTORY | client performance (Cottonwood) via MDPF_SECHIST series | client history | 2013-04-03..2026-06-23 / [max(first record, 2012-01-01), frontier] intersected with held dates | 1,319 names x PX_LAST, P1 first | ~2.4M (inferred, never priced) / **pending (t-43/t-44)** | R2 | pending; at 5,900 to 7,300 cells a day ~330+ days for all 1,319, so P1 alone is the number to print | TRIM to the P1 slice, re-price before any draw; if P1 > 30 days the number goes to the CTO (msg 4875) |
| 5 | DEMQUE-TR-COMPARISON-DIVIDEND-PAYERS | the TR comparison (Andrew-direct 2026-10-09; DEMQUE round-5 method; research deliverable, not a served series) -- surface D | non-client | 2021-10-01..2026-10-08 / **2025-10-09..2026-10-08 (251 trading days)** | 6 x 2 (PX_LAST, DAY_TO_DAY_TOT_RETURN_GROSS_DVDS) | 15,120 / **12,720 total**: 11,716 drawn and KEPT, **1,004 still to draw**, 2,400 cancelled | R3 | 1,004 / ~5,900 = 0.2 day | TRIM (Andrew-direct addendum 2; msg 4889): see section C |
| 6 | AMGT_RESAPP-107a-ABNB-MODEL-BLOCK | the research app (AMGT_RESAPP) -- surface D | non-client | producer-defined (HIST_START in the producer) / must be declared; not computed here | 1 x model block | 989 / 989 (not drawn) | R3 | ~0.2 day on its channel | KEEP; its window needs declaring at t-44 |
| 7 | AMGT_RESAPP-493c-ICT-IDENTITY | the research app (AMGT_RESAPP) -- surface D | non-client | n/a (reference) | 1 x 1 | 1 / 1 | R3 | 0 | KEEP |
| 8 | AMGT_RESAPP-S14-CRNCY-SCANNER-US-SLICE1 | the research app (AMGT_RESAPP), scanner currency test -- surface D | non-client | n/a (reference) | 50 x 1 | 50 / 50 | R3 | 1 day | KEEP (filer's first slice, msg 4877) |
| 9 | AMGT_RESAPP-S14-CRNCY-SCANNER-US | the research app (AMGT_RESAPP) -- surface D | non-client | n/a (reference) | 1,038 x 1 | 1,038 / **0 until slice 1 reads a non-USD currency** | R3 | finish 2026-12-04 if drawn | KEEP FILED, UNDRAWN (filer's rule); counts 0 in the two weeks |
| 10 | ETFS_RIVALS-HISTORY-OWED-DAILY | Rival Funds page (ETFS_RIVALS) | non-client | per owed set, none declared / 365 days before need date | owed set (742 securities, 184,600 units on 2026-10-08) x 1 | 184,600 (10-08 owed set) / re-price per run | R3 | at its 20,000-cell cap per run: 9.2 runs | KEEP, class and 365-day start to be declared; owed set averages 249 units a security, already inside 365 days |

## B. Yahoo items (no Bloomberg budget; the shared pacer's 400 requests a day)

| # | request id | consumer | class | window | cells quoted (drawn latest) | decision |
|---|---|---|---|---|---|---|
| 11 | STANDING extension (Z-STANDING-T1-EXTEND, daily) | client performance prices, price store (C-PRICES) | client | 2013-04-08 to T-1 | ~497k a day (461,094 drawn 10-12) | KEEP (production T-1) |
| 12 | DEMQUE-S8-REDRAW-20261011 | price store | client | 2013-04-08.. | 110,304 (105,690 drawn) | KEEP, done |
| 13 | R2-PILOT-50 | advi/cottonwood backfilled holding values | client | 2013-04-08.. | 172,350 (143,104 latest) | KEEP; the rest is on the unresolved list |
| 14 | R2-SCHED-SLICE-1 | same | client | 2013-04-08.. | 10,341 (6,753) | KEEP; same |
| 15 | R4-P1-SLICE-1 | same | client | 2013-04-08.. | 516,900 (314,095) | KEEP; same |
| 16 | IRPT_BCKEND-AS-TRADED-CLOSES-878 | investor reporting date-basis grading (IRPT_BCKEND) | client | 2026-04-14..2026-10-09 | 113,262 (30,570 day 1 of 3) | KEEP |
| 17 | ADVI_COTBKF-TIER2-15-FUNDS-AS-TRADED-20261012 | the Cottonwood 15-fund fill (ADVI_COTBKF; minted table account_return_daily) -- surface B | client | 2020-07-06.. | 23,340 (19,474; 7 of 15 landed, 8 rejected) | KEEP, done; the 8 rejected funds stay unresolved |

## C. The TR comparison, how the trim works

Measured from the drawn rows: 5,858 security-date rows, two fields each = 11,716 cells. KO, JNJ, T, VZ are drawn in full (1,260 days each); MO is drawn to
2025-01-02 (818 days); XOM is not started. The 365-day window is 2025-10-09..2026-10-08 = 251 trading days. Inside it: KO, JNJ, T, VZ are already drawn
(1,004 security-date rows); MO and XOM are not (502 security-date rows = 1,004 cells). So **keep 11,716, draw 1,004, cancel 2,400** (MO 2025-01-03..2025-10-08 and XOM
before 2025-10-09). The drawer counts cells, not identities, so a bare edit of the request's start would make it read "already complete". The
order that lands this (t-44) must make the remainder an identity set. **The drawer's next fire is the first non-trading day (2026-10-17): nothing draws this
request before that.**

## D. Two-week total

Fixed Bloomberg cells to draw in the window: 1,004 (TR) + 989 (ABNB) + 1 (ICT) + 50 (slice 1) = **2,044 cells, under half a day of the history allowance**. The rival-funds
list draws in its own vehicle at up to 20,000 cells a run, about 9 runs for the 10-08 owed set. The one open number is the CARD-A P1 slice. Until it is printed the
two-week total cannot be stated honestly; the CTO's 30-day rule applies to it.

## E. Surface map and the hold (Andrew's form, `deliverables/QUEUE_FORM_ANDREW_20261013.md`; CTO msg 4892)

Order: **A** production daily, **B** client history, **E** Opal ad-hoc (10 percent of the daily Bloomberg allowance, unused part released the same day), **C** product
history, **D** research. "None found" is not a drop: the AMGT_RESAPP items are the research app's needs and are KEPT.

| surface | items above |
|---|---|
| A production daily | 1, 2, 3 (Bloomberg); 11 (Yahoo standing extension) |
| B client history | 4 (CARD-A P1, pending); 12 to 17 (Yahoo) |
| E Opal ad-hoc | none queued today; 10 percent of the allowance is held for it |
| C product history | 10 (rival funds) |
| D research | 5 (TR comparison), 6, 7, 8, 9 (research app) |

**Hold (msg 4892): no NEW Bloomberg draw starts until the form is complete.** Nothing new fires before the standing drawer's next non-trading-day fire (2026-10-17), and this
seat starts none. Already-scheduled production runs and the Yahoo nightly run are not new draws and continue.

