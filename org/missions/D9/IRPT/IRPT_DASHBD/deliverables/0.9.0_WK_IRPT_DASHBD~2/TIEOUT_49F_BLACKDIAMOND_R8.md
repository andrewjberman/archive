# TIEOUT_49F_BLACKDIAMOND_R8 -- all 14 like-day pairs under the EQUITY basis (TO-DB-b-15, FWD-8)

C-VALUE is the account's equity, `net_mv_plus_cash + margin_balance`, margin signed as the custodian stores it (CTO RULINGS batch 193).
It is one rule for every account and `method_version` 2. Tolerance 0.0035 (0.35 pp, batch 181/182). Vendor calls: 0. Black Diamond's side is
the stored round-4 response per account; Opal's side is the producer in this worktree run locally over the Schwab silver (reads only). Ids only.

Sign check: Black Diamond's value minus (`net_mv_plus_cash` + `margin_balance` + its own accrual) is 0.00 at 28 of 28 window endpoints
(14 pairs x 2), so the stored sign is the one to add.

| account | window | R4 abs_diff | now abs_diff | BD accrual over window | within |
|---|---|---|---|---|---|
| acct#e7ab8585 | 03-17..03-26 | 0.1714 pp | 0.1707 pp | 0.00 | yes |
| acct#e7ab8585 | 04-09..04-30 | 0.4555 pp | 0.0493 pp | +537.48 | yes |
| acct#e7ab8585 | 05-08..06-23 | 0.0157 pp | 0.0055 pp | -101.46 | yes |
| acct#e7ab8585 | 06-25..07-06 | 1.2130 pp | 0.4738 pp | -81.72 | NO (S22) |
| acct#e7ab8585 | 07-08..08-04 | 0.1561 pp | 0.0107 pp | +108.16 | yes |
| acct#e7ab8585 | 08-06..08-19 | 0.0042 pp | 0.0325 pp | -325.85 | yes |
| acct#e7ab8585 | 08-21..10-01 | 0.1954 pp | 0.0223 pp | -248.23 | yes |
| 0076459710 | 07-09..08-04 | 0.0000 pp | 0.0000 pp | 0.00 | yes |
| 0076459710 | 08-11..08-19 | 0.3307 pp | 0.4998 pp | +6,022.40 | NO |
| 0076459710 | 08-21..09-09 | 0.0076 pp | 0.4608 pp | -5,766.11 | NO |
| 0076459710 | 09-16..10-01 | 0.1297 pp | 0.0233 pp | -332.99 | yes |
| 0084073310 | 03-20..08-04 | 0.2606 pp | 0.4045 pp | 0.00 | NO |
| 0084073310 | 08-06..08-19 | 0.1124 pp | 0.0219 pp | +208.13 | yes |
| 0084073310 | 08-21..10-01 | 0.7078 pp | 0.0264 pp | -234.65 | yes |

10 of 14 within; max abs diff 1.2130 pp -> 0.4998 pp. `bd_accrual` is Black Diamond's ending accrual minus its beginning accrual over
the window; both ends are in the JSON. Black Diamond's accrual stays outside Opal's figure because Opal books income on receipt.

## The four beyond 0.35 pp, each with a measured reason

- **acct#e7ab8585 06-25..07-06, 0.4738 pp (S22).** RESTATED, not DISARMED. Black Diamond books the 4,429.53 INTRA/FC/IN "MARGIN INT ADJ" credit as a net
  addition (netAdditions 4,402.22); Opal keeps margin interest internal by ruling (batch 195). Treated as a flow, the pair would be 0.0044 pp
  (counterfactual, never applied; the credit is not re-classed).
- **0076459710 08-11..08-19, 0.4998 pp, and 08-21..09-09, 0.4608 pp.** Black Diamond's value carries its accrual (+6,022.40 then -5,766.11), which
  alone is 0.4999 pp and 0.4501 pp of its beginning value; the residuals after that effect are 0.0001 pp and 0.0107 pp. The two windows mirror
  each other. The first of these was 0.3307 pp and the second 0.0076 pp at round 4: they moved because the basis now matches Black Diamond's
  endpoints to the cent and its accrual is the whole of the rest.
- **0084073310 03-20..08-04, 0.4045 pp.** Black Diamond's return equals ending value / beginning value - 1, so its 3,020.96 fee stays inside its
  return (0.3961 pp of beginning value); Opal is gross of fee (GROSS_ONLY, C-FEERAIL). Opal's own window fee flow was inferred from its return
  (within 0.0083 pp of the fee-added-back endpoint form), not read as a flow: said, not guessed.

## Population (POPULATION_EQUITY_R8.json, 2026-10-01)

Positive accounts 6,685 -> 6,686 of 7,570 (the before figure is re-derived at 6,685 as a control). Guard over the 6,861 rows both versions emit:
GRADED_AGREED 6,635 -> 6,639; GRADED_DISAGREED 13 -> 9; GUARD_NOT_REACHED 184 -> 184; NOT_GRADED_OUTSIDE_DOMAIN 29 -> 29. Two accounts emit a row only
under equity. 6,788 accounts with margin_balance 0 on the day and the prior trading day: 0 rows changed apart from method_version. Null margin_balance:
0 rows on the day and 0 of 3,230,967 across 563 partitions.

Rows: IRPT_DASHBD-W2-S1 (4 pairs beyond), -S2 (zero-margin definition, null handling, row set), -S3 (method-row columns vs contract).
