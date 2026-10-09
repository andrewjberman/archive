# TIEOUT_49F_BLACKDIAMOND_R6 -- the three like-day pairs beyond 0.35 pp (TO-DB-b-13, FWD-8)

Tolerance 0.0035 (0.35 pp, CTO RULINGS batch 181, corrected by batch 182). Vendor calls: 0. Black Diamond's side is the stored round-4
response per account; Opal's side is the producer in this worktree run locally over the Schwab silver (reads only). Ids only.

| account | window | R4 abs_diff | now abs_diff | defect | fixed |
|---|---|---|---|---|---|
| acct#e7ab8585 | 2026-06-25..07-06 | 1.2130 pp | 1.2130 pp | yes (income sign) | yes |
| 0084073310 | 2026-08-21..10-01 | 0.7078 pp | 0.7078 pp | no (value basis) | n/a |
| acct#e7ab8585 | 2026-04-09..04-30 | 0.4555 pp | 0.4555 pp | no (value basis) | n/a |

## What the S22 fix did, and did not do

Fix: the income term of `classify_and_sum` now admits the DEBIT leg of the plain dividend keys (QDV, NDV, PDV on FC/DV), as negative
income, read from the transaction key and never the account. Measured over the 188 transaction partitions of 2026: 614 rows newly
admitted (16,116.12 absolute), 614 of 614 with a negative share quantity, 613 of 614 on an account-day with a short market value,
0 with neither signal. Adjustment keys (DIVAJ etc.), margin interest (INTR) and foreign-tax withholding stay out as before.

Result: window income_received for acct#e7ab8585 moves 4,769.03 -> 4,312.61. **The pair's total return does not move**, because the
daily total return is (V_t - F_t) / V_(t-1) - 1 and income is not an input of it; income feeds `income_return` and the guard
cross-check only. So the largest pair is fixed as a defect and still stands at 1.2130 pp for the reasons below.

## The measured reasons

Black Diamond's beginning and ending values equal Opal's value + the Schwab `margin_balance` + Black Diamond's own accrual, to the cent,
at all 6 window endpoints (0.00 difference each). Opal's value is `net_mv_plus_cash` (the ratified C-VALUE); it leaves out
`margin_balance`.

- 0084073310 2026-08-21..10-01: adding margin_balance moves 0.7078 -> 0.0264 pp.
- acct#e7ab8585 2026-04-09..04-30: adding margin_balance moves 0.4555 -> 0.0493 pp.
- acct#e7ab8585 2026-06-25..07-06: adding margin_balance moves 1.2130 -> 0.4738 pp (0.7392 pp); then treating the 4,429.53 credit
  coded INTRA/FC/IN "MARGIN INT ADJ" on 06-25 as a flow, as Black Diamond does (netAdditions 4,402.22), moves 0.4738 -> 0.0044 pp.

These are counterfactuals replayed on the Schwab balances; none is applied to the producer or written anywhere.

## Not measured

Black Diamond's reported window income (-2,470.31 here) is not reproducible from the Schwab silver: Black Diamond's accrual
convention for margin interest is its own, and its source is not in the stored response. Said, not guessed.

Rows: IRPT_DASHBD-W1-S17 (DIV key left out), -S18 (value basis, ruling owed), -S19 (method-row columns vs contract), -S20
(margin-interest adjustment classification).
