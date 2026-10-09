# Ex-date request -- ADVI_COTBKF to dell1's backfill data-queue project (filed 2026-10-09 ~00:2xZ)

**Owner:** `2.0.0_SA_COO~C2` (dell2) | **Ruling:** `1.0.0_SA_CTO~DELL2` round-24 analysis @cdf5f13f3f (msg 1957), E3 | **Row:** D2-W46-S2

**What is asked.** The EX-DATE of each dividend below. Key namespace: CUSIP (9 characters, as Commonwealth delivers it), with the
ticker as delivered beside it for resolution. One ex-date per (CUSIP, pay date). The delivered transactions carry the pay date only.

**What it un-parks.** CB24x1-AC4's clause "every cross-month dividend month graded both ways". When ex-dates land, the 22 months are
graded at pay date and at ex-date with the swing printed (runner option `--dividend-date pay|ex`, input `--ex-dates` with columns
cusip, pay_date, ex_date; built and tested in round 24). Until then the clause stays NOT MET, parked as one hop (NO-STOP RULE).

**Priority within the queue.** These are 22 account-months on 17 securities, a small, exact request; their tier on the queue's
ranking (living client / match open / gone) is not measured here. It travels with, and does not wait for, this project's ranked price-need list (parked on the queue's L2).

## The 22 months (from `deliverables/0.9.0_WK_ADVI_COTBKF~46/sweep_regrade.md`, cause `dividend_row`)

| account | month | pay date | dividend (account) | CUSIP(s) paying that day | ticker(s) |
|---|---|---|---|---|---|
| acct#04ebe1d1 | 2022-08 | 2022-08-11 | 12.88 | 037833100 | AAPL |
| acct#04ebe1d1 | 2022-11 | 2022-11-10 | 12.88 | 037833100 | AAPL |
| acct#04ebe1d1 | 2023-02 | 2023-02-16 | 12.88 | 037833100 | AAPL |
| acct#04ebe1d1 | 2023-05 | 2023-05-18 | 13.44 | 037833100 | AAPL |
| acct#04ebe1d1 | 2023-11 | 2023-11-16 | 13.44 | 037833100 | AAPL |
| acct#04ebe1d1 | 2024-02 | 2024-02-15 | 13.44 | 037833100 | AAPL |
| acct#04ebe1d1 | 2024-08 | 2024-08-15 | 14.00 | 037833100 | AAPL |
| acct#04ebe1d1 | 2024-11 | 2024-11-14 | 14.00 | 037833100 | AAPL |
| acct#04ebe1d1 | 2025-05 | 2025-05-15 | 14.56 | 037833100 | AAPL |
| acct#04ebe1d1 | 2025-08 | 2025-08-14 | 14.56 | 037833100 | AAPL |
| acct#04ebe1d1 | 2025-11 | 2025-11-13 | 14.56 | 037833100 | AAPL |
| acct#04ebe1d1 | 2026-02 | 2026-02-12 | 14.56 | 037833100 | AAPL |
| acct#1f02bee1 | 2022-12 | 2022-12-28 | 77.52 | 654106103 | NKE |
| acct#16f4eae3 | 2024-08 | 2024-08-06 | 50.97 | 464288414; 78468R739 | MUB; SHM |
| acct#16f4eae3 | 2024-09 | 2024-09-06 | 51.93 | 464288414; 78468R739 | MUB; SHM |
| acct#16f4eae3 | 2024-12 | 2024-12-20 | 126.17 | 464286525; 46432F339; 46434G103; 46434G848; 46434V449; 46434V456; 46435G409 | ACWV; IEMG; IMTM; IQLT; IVLU; PICK; QUAL |
| acct#16f4eae3 | 2025-02 | 2025-02-06 | 53.04 | 464288414; 78468R739 | MUB; SHM |
| acct#16f4eae3 | 2025-12 | 2025-12-19 | 152.29 | 464286525; 46432F339; 46434G103; 46434G848; 46434V449; 46434V456; 46435G409 | ACWV; IEMG; IMTM; IQLT; IVLU; PICK; QUAL |
| acct#83c764b4 | 2025-06 | 2025-06-10 | 268.29 | 30231G102 | XOM |
| acct#83c764b4 | 2025-09 | 2025-09-10 | 268.29 | 30231G102 | XOM |
| acct#ed5f47fe | 2025-12 | 2025-12-23 | 96.45 | 921943858; 922042858 | VEA; VWO |
| acct#ed5f47fe | 2026-03 | 2026-03-20 | 34.74 | 464287663; 464287671 | IUSG; IUSV |

Distinct securities: 17. CUSIP / ticker read from `.scratch/advi_cotbkf/cache/transactions.parquet` (the projected silver
transactions), rows of type dv/dvr/dvlt/dvst on the account and pay date; the dollar figure is the arms' value step from the round-24
report. The "dividend (account)" column is that step, not a per-share rate.
