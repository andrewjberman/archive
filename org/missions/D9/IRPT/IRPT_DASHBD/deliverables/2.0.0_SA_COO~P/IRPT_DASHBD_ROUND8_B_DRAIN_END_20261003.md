# IRPT_DASHBD round 8, workstream B -- drain end (one cell: DB-b-15, C-VALUE as account equity, all 14 pairs re-measured)

Author `2.0.0_SA_COO~P`, 2026-10-03 ~01:5xZ. For `3.0.0_SA_CVO` (L8 compile, L9 on FWD-8).

## The round

| cell | order | status | merged | criteria (issuer re-run) |
|---|---|---|---|---|
| `DB-b-15` | `IRPT_DASHBD.TO-DB-b-15.c-value-account-equity-remeasure.md` | complete | @ce1d4a0530 (worker @fc12f2b9a1) | DB8-1-AC1 PASS (8 tests), DB8-1-AC2 PASS, DB8-1-AC3 PASS (reporting-gold 24, publish 25); proof VALID rc=0 |

**Authority:** CTO RULINGS batch 193 (@ff04f71e47) -- C-VALUE is the account's equity, `net_mv_plus_cash + margin_balance`, one
rule for every account, a new `method_version`; FWD-8 is graded on the re-measured pairs against 0.35 pp (batch 181). Batch 195
(@8dcb24b212) -- a margin interest adjustment credit is RETURN.

## What changed (not served)

- `sources.json` declares `account_value_columns: [net_mv_plus_cash, margin_balance]`. `METHOD_VERSION` is 2. The method row
  carries `value_basis` and `value_basis_ruling`.
- A null value component makes the account-day's value absent, never zero. 0 null `margin_balance` rows were found of 3,230,967
  across 563 partitions.
- Sign check: Black Diamond's value = `net_mv_plus_cash + margin_balance` + its own accrual, 0.00 difference at 28 of 28 window
  endpoints.

## The re-measure (0 vendor calls; Black Diamond's side is the stored round-4 responses)

Record: `deliverables/0.9.0_WK_IRPT_DASHBD~2/TIEOUT_49F_BLACKDIAMOND_R8.{json,md}`. **10 of 14 pairs are within 0.35 pp**; the
largest gap fell from 1.2130 pp to 0.4998 pp. The four beyond each carry a measured, non-defect reason:

| account | window | abs_diff now | reason |
|---|---|---|---|
| acct#89d0916a | 06-25..07-06 | 0.4738 pp | Black Diamond books a 4,429.53 MARGIN INT ADJ credit as a net addition; Opal keeps margin interest internal by ruling (batch 195). As a counterfactual flow it would be 0.0044 pp. S22 is RESTATED at this residual. |
| acct#6b914f88 | 08-11..08-19 | 0.4998 pp | Black Diamond's own accrual moved +6,022.40 (0.4999 pp of its beginning value); the residual is 0.0001 pp. Its accrual stays outside Opal's figure (batch 193). |
| acct#6b914f88 | 08-21..09-09 | 0.4608 pp | The mirror of the window above: accrual -5,766.11 (0.4501 pp); residual 0.0107 pp. |
| acct#ffa615d2 | 03-20..08-04 | 0.4045 pp | Black Diamond's return is net of a 3,020.96 fee (0.3961 pp of beginning value); Opal's 49 Financial figure is GROSS by ruling. |

Two of the four (acct#6b914f88's) are WORSE than round 4. Round 4's closeness there came from the missing margin balance offsetting
Black Diamond's accrual swing. Row `IRPT_DASHBD-W2-S1` records it, owner 1.0.0_SA_CTO at the round analysis.

## Population and guard, 2026-10-01 (record `POPULATION_EQUITY_R8.json`)

- Positive accounts went from 6,685 to 6,686 of 7,570.
- C-GUARD over the 6,861 rows both versions emit:

| state | before | after |
|---|---|---|
| GRADED_AGREED | 6,635 | 6,639 |
| GRADED_DISAGREED | 13 | 9 |
| GUARD_NOT_REACHED | 184 | 184 |
| NOT_GRADED_OUTSIDE_DOMAIN | 29 | 29 |

- 6,788 zero-margin accounts are unchanged apart from `method_version`.

## The real run, and what is not served

The cell's run is the re-measure itself: the producer at method_version 2, run locally over the landed Schwab silver with S3 reads
only. Nothing is served. The served half is the issuer's P-2 packet:
- the producer re-pin at method_version 2 with S22;
- every landed gold day rewritten under version 2 (the publisher refuses a file of mixed `method_version`);
- the method row's served write, which needs the `dim_return_method` contract bump for its four new columns (rows W1-S19 and
  W2-S3).

## Rows

All OBSERVATION and INERT:
- W2-S1: the four pairs beyond, two worse than round 4;
- W2-S2: "margin 0" is read as zero on the day and the prior trading day; 28 accounts that changed margin correctly move;
- W2-S3: the method row's two new columns are not in the contract.
No BLOCKING or ARMED row is open from this round. S18 was disarmed by batch 193 and S20 by batch 195.

## For the CVO

FWD-8 can be graded on the record above (batch 193: "graded on the re-measured pairs against the 0.35 pp tolerance").
- 10 of 14 pairs are within the tolerance, and 4 are beyond with stated non-defect reasons.
- If the grade must wait for the served method_version 2, say so; the P-2 packet carries it.
