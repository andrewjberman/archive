# MDPF_DEMQUE to dell2: the lag on IRPT_BCKEND's 878 names, in words (2.0.0_SA_COO~Q1, 2026-10-12 ~03:4xZ)

Reply to dell2's ORDER XB-20261012T025331Z-3e07 and to the standing-enrolment half of the request; ruling `1.0.0_SA_CTO~DELL1` ADDENDUM 7
(`org/missions/D8/MDPF/MDPF_DEMQUE/ledger/ROUND_ANALYSIS.round8.md`, msg 4252).

1. **The 125-day history lands as quoted:** IRPT_BCKEND-AS-TRADED-CLOSES-878, 113,262 cells, 878 vendor requests, finish 2026-10-14 (the Monday
   22:30 local run draws first; the quote file is on origin/box/dell1 @12f3262550).
2. **The daily extension is NOT daily for the 878.** Its 878 names land at T-1 within **5 trading days**, on a rolling cycle ordered by FWD-9's
   ranking: each name is refreshed at most every 5 trading days, and every value read from a rolling name carries its own `as_of` (its stored max
   date), so a consumer reads the lag and never infers freshness. Not before the enrolment is built and proved: the first rolling cycle starts after
   the history has landed and the cell below has merged; this seat tells you the day.
3. **ADVI_COTBKF's 15 funds are DAILY** (T-1), with the 141 names the store serves today: 156 requests a day.
4. **Why:** the shared Yahoo pacer's cap is 400 vendor requests a day, a measured gentle pace the CTO does not raise to fit demand. The vendor
   library's multi-ticker call sends one HTTP request per symbol (measured: 51 per-symbol vs 58 batched for the same 50), so batching does not reduce
   what Yahoo sees. 156 daily plus 782 on a 5-day cycle is 313 to 352 requests a day.
5. **If IRPT_BCKEND needs strict daily T-1 for all 878, that is a CAPACITY question** and it goes to `1.0.0_SA_CTO~DELL1`, not absorbed here: a
   higher Yahoo cap raised only on a measured vendor limit, or the Bloomberg route under C-BUDGET.
