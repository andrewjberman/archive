# TIEOUT_49F_BD_POPULATION_E2_GROSS -- counts only

Task order IRPT_DASHBD.TO-DB-b-27. Basis GROSS, tolerance 0.35 pp, vendor calls 0. Record: `TIEOUT_49F_BD_POPULATION_E2_GROSS.json` (4,196,573 bytes, sha256 febe370fbed76497...).

| count | round 18 (gross) | round 17 | change |
|---|---|---|---|
| segments_planned | 9082 | 9082 | 0 |
| graded | 9078 | 9078 | 0 |
| not_gradable (BD_NO_VALUE) | 4 | 4 | 0 |
| within_tolerance | 5416 | 2103 | +3313 |
| outside_tolerance | 3662 | 6975 | -3313 |
| outside: FLOW_TIMING | 333 | 150 | +183 |
| outside: MISSING_PRICE | 1 | 2 | -1 |
| outside: INCOME_DATE | 44 | 568 | -524 |
| outside: COVERAGE_DAYS | 5 | 5 | 0 |
| outside: UNEXPLAINED | 3279 | 6250 | -2971 |

Graded rows with a null bd_fee_addback: 1231 of 9078 (1151 within, 80 outside); the 4 not-gradable rows are also null.

Provenance: 3.0.0_SA_CVO ran it on the laptop @e6ed5380e6 because the dell2 identity is fenced from opal-data-49financial (row IRPT_DASHBD-W13-S1); the record's measured_by field is the script's constant.
