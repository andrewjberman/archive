# TIEOUT_COMPOUND_E1 -- the 49F tie-out re-graded on the compounded fee basis (TO-DB-b-53, 0.9.0_WK_IRPT_DASHBD~34)

Counts only. Record: `TIEOUT_COMPOUND_E1.json`. Reader: `tieout_compound.py` (imports round 18's `tieout_e2_gross.py`; overrides only the gross formation).

Basis: BD gross = (1 + BD net TWR) * (1 + fees / ((bmv + emv) / 2)) - 1. Round 18: BD net TWR + the same add-back. Tolerance 0.35 pp. S3 reads only; zero vendor calls.

Population: 9,082 planned, 9,078 graded (4 not gradable, as in round 18). Round 18's counts were re-derived from the same inputs before the override: 5,416 within / 3,662 outside (MATCH with its record).

| | within 0.35 pp | outside | share within |
|---|---|---|---|
| before (round 18, additive) | 5,416 | 3,662 | 59.66% |
| after (compounded) | 7,459 | 1,619 | 82.17% |

Verdict moves, per segment, against round 18: unchanged (MATCH) 6,673; OUTSIDE to WITHIN 2,224; WITHIN to OUTSIDE 181 (DIFF 2,405 in all).

Outside by reason (closed set):

| reason | before | after |
|---|---|---|
| FLOW_TIMING | 333 | 370 |
| MISSING_PRICE | 1 | 1 |
| INCOME_DATE | 44 | 40 |
| COVERAGE_DAYS | 5 | 5 |
| UNEXPLAINED | 3,279 | 1,203 |
| total | 3,662 | 1,619 |

Inputs: plan `BD_POPULATION_PLAN_E3.json`; BD pull=20261004 (5,252 objects); served gold `account_return_daily` (566 partitions, 6,898 accounts).
Rows filed: IRPT_DASHBD-W34-S1 (chain test needs the compounded fee drag), IRPT_DASHBD-W34-S2 (181 reversals).
