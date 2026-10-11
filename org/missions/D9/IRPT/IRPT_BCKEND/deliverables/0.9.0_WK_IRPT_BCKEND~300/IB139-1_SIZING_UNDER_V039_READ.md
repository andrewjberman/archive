# IB139-1 (IB-pr-442) -- the sizing under PRD ADDENDUM v0.39: what grading only the admitted types frees

READ ONLY; a SIZING, not a stamp. Nothing built, served or re-graded in the product. Counts only; no account id, balance, quantity or single account's holding.
Same 85 trading days (2026-06-10 to 2026-10-09). Data: `IB139-1_sizing_under_v039.json`. Scripts in this folder: `ib433_fetch.py` (partitions), `ib441_fetch_tx.py` (transactions table),
`ib442_phase1.py`, `ib442_prepare.py`, `ib441_fetch_yahoo.py` (the one pass), `ib442_measure.py` (classes, grades, outcomes, sizing, control).

**Same account-days read: TRUE.** Under the cash rule: UNGRADEABLE 43,310; ACCT_PRIOR_DATE 55; ACCT_OWN_DATE 19,832; NOTHING_TO_GRADE 13,599; present 76,796 (IB-pr-438's figures exactly).

## 1. The seven classes (737 securities the first witness does not carry)
Precedence: no ticker; then type (no type or mixed; Inst; RIC/BDC Not Available; another pair); then, for an admitted type, no bar or with bars.

| class | securities |
|---|---|
| admitted_type_with_bars | 152 |
| left_out_type_inst | 71 |
| left_out_type_ric_not_available | 78 |
| no_type_or_mixed | 38 |
| another_type_not_admitted | 19 (Cash and Cash Equivalents / Not Available 7; Not Available / Not Available 8; RIC/BDC Adv 2, C 1, N 1) |
| no_ticker_to_ask_with | 375 |
| no_bar | 4 (FPNIX, BRK.A, UHALB, JHG: admitted types whose ticker returned nothing) |

Admitted securities with bars, by pair: Exchange-Traded Equity Securities / Not Available 96; RIC/BDC ETF 6; A 7; No Load 8; Other 25; Retirement 10; Inv 0 (its one outside security is FPNIX, no bar).
All seven pair strings were found exactly as written in the transactions table.
**Type join over THIS set** (not IB-pr-441's 894): 667 find one pair, 13 find no row, 57 find more than one pair (of the 362 with a ticker: 324 one pair, 0 no row, 38 mixed).
The 38 of the class no_type_or_mixed all have a ticker and all are mixed (the other 19 mixed and the 13 with no row have no ticker). Of the 38, 22 are one share class under both `Not Available` and `RIC/BDC` as asset type (for example `Not Available / Inst` with `RIC/BDC / Inst`: 14), 5 are `Not Available / Not Available` with `RIC/BDC / Not Available`, and 11 are `Exchange-Traded Equity Securities` or `Cash and Cash Equivalents` with `Not Available / Not Available`; the rule as written leaves them with no type.

## 2. The one pass
232 distinct tickers, 5 calls (50, 50, 50, 50, 32), paced 8 s, none parallel, none rate-limited, none asked twice: 154 tickers of admitted-type securities and 103 fund tickers (25 in both). 228 returned bars, 4 returned none.
Window 2026-06-05 to 2026-10-13. Yahoo Finance only; no YCharts, no Bloomberg.

## 3. The account-days (34,789 hold a security the first witness does not carry)
holds_a_security_no_witness_may_grade 28,903; admitted_but_one_or_more_at_neither 69; admitted_but_one_or_more_at_prior_day_only 80;
**freed_every_security_admitted_and_at_the_day_close 5,737**, of which 5,666 hold no other ungradeable kind (of the 80 at prior-day-only, 52 hold none).

## 4. The sizing (the stated assumption is in the json: every clean freed day reads ACCT_OWN_DATE, a clean prior-day-only day reads ACCT_PRIOR_DATE, the rest keep their claim)
| | today (cash rule) | under v0.39 admitted types | withdrawn v0.37 (reference) |
|---|---|---|---|
| UNGRADEABLE / PRIOR / OWN / NOTHING | 43,310 / 55 / 19,832 / 13,599 | 37,592 / 107 / 25,498 / 13,599 | -- |
| eligible, served, blank | 75,796; 31,715; 44,081 | 75,796; 37,667; 38,129 | -- |
| blank share | 58.157 % | **50.305 %** | 36.989 % |
| accounts never served (of 999) | 382 | **357** | 181 |

So the admitted types free 7.85 points of blank share and 25 accounts. The v0.38 range (37.0 to 58.2) holds.

## 5. What the rest waits on (account-days; "only on" is an UPPER BOUND: freed if that ONE class sat at the day's close, all else unchanged)
| class | holding any | waiting only on |
|---|---|---|
| left_out_type_inst | 23,562 | 6,960 |
| left_out_type_ric_not_available | 6,235 | 2,003 |
| no_ticker_to_ask_with | 4,619 | 1,871 |
| another_type_not_admitted | 2,027 | 319 |
| no_type_or_mixed | 497 | 96 |
| no_bar | 12,248 | 43 |

Largest no-bar fund: **FPNIX, 12,115 account-days** (type RIC/BDC / Inv, admitted, but the reader has no bar). Admitting it would free almost nothing alone (43 account-days waiting only on all no-bar securities).

## 6. The reviewer's two points
**Next day only to the cent: 3 trades (the same 3 as IB-pr-441), all dividend-reinvestment buys, all of an Inst fund, none an admitted pair.**
PFMIX 2026-06-30, price 9.4637, bars prior 9.47 / day 9.47 / next 9.46. VWIUX 2026-06-30, 13.805, bars 13.81 / 13.81 / 13.80. NHMRX 2026-07-01, 14.5263, bars 14.52 / 14.50 / 14.53.
**6,149 priced fund trades by the fund's pair** (trades; funds; same day only / prior / next / more than one / none / no bar), relative 1e-4:
Inst 3,630; 60 funds: 2,692 / 28 / 0 / 771 / 139 / 0. No Load 1,547; 9: 1,282 / 0 / 0 / 265 / 0 / 0. Other 505; 12: 433 / 0 / 0 / 44 / 28 / 0. Inv 285; 2: 1 / 0 / 0 / 0 / 0 / 284.
Retirement 98; 5: 60 / 0 / 0 / 12 / 26 / 0. A 47; 6: 3 / 0 / 0 / 2 / 42 / 0. Adv 25; 1: 10 / 0 / 0 / 8 / 7 / 0. MIXED 12; 8: 9 / 0 / 0 / 0 / 3 / 0. Totals 4,490 / 28 / 0 / 1,102 / 245 / 284 (IB-pr-441's, exactly).
Read: `Inv` rests on 285 trades of which 284 have no bar (one fund) and 1 is same-day, so the fund table supports `Inv` on one trade; `A` has 47 trades of which only 3 are same-day and 42 match no bar; `Retirement` 98 trades, 60 same-day.

## 7. Control (planted equals read)
Three planted account-days through the real class, row, outcome and sizing functions: an admitted-type security at the day's close is freed; the same plus a left-out-type security is not freed; an admitted security at the prior day's close is blocked (prior day only; sizing claim ACCT_PRIOR_DATE).
