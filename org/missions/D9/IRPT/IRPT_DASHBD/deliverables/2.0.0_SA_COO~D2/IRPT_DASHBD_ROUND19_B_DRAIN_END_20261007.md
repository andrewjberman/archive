# L8 drain end -- IRPT_DASHBD round 19, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~11:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @09dde1b9a1

Both orders are terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer before each drain).
0 JUDGMENT criteria. Both cells are LOCAL; no served byte moved, no vendor call. Both worktrees and branches were removed after their
drains. On: `1.0.0_SA_CTO~DELL2`'s round-18 analysis @62026ca511 as ruled in msg 308. E1 was handed back (msg 307) and replaced by E1'.

## Orders

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-29 (E1': Opal recomputed with 2025-01-09 held, over the 2,299 closure segments) | @33949e002d (worker ~14: 40a7390d39, 253c4cbf38, 04d545b951) | DB19-1-AC1..AC3 PASS | **0 of 2,299 within 0.35 pp.** The served `opal_return` is unchanged; the recomputation lives only in `*_bd_convention`. Accrual: the mean daily `income_return` over the segment's linked days (the issuer accepted that rule). 564 gold partitions read on dell2 |
| DB-b-30 (E2: the 980 non-closure UNEXPLAINED segments) | @5831f348b8 (worker ~15: a5e3325b4b) | DB19-2-AC1..AC3 PASS | FLOW_TIMING 226, UNEXPLAINED 754 (8.31% of 9,078); MISSING_PRICE, INCOME_DATE and COVERAGE_DAYS 0 |

## Read before grading

- **DB-b-29 refutes the day-count hypothesis on Opal's side.** The issuer read the record: holding 2025-01-09 moves Opal's figure by a
  median 0.013 pp (largest 0.53 pp) against a median gap of 0.79 pp; 182 of 2,299 move closer; the smallest gap left is 0.361 pp.
  Under msg 308 ("If E1' leaves most of the 2,299 unexplained, the split-range BD pull goes on Andrew's list as a per-use vendor act"),
  that listing is now owed by `1.0.0_SA_CTO~DELL2`.
- **DB-b-30's 226 FLOW_TIMING are INFERRED, not measured.** The record says `claim: inferred`. The rule: BD's Account-level point shows
  a net flow of at least 25% of the larger market value, and both Opal's and BD's gross returns fall inside the Modified Dietz envelope
  of that flow placed at segment start versus end (plus or minus 0.35 pp). The flow day alone could carry the gap, but this is not
  shown. INCOME_DATE could not be tested: BD gives income totals, not dates.
- **How DB-b-29 got its read:** the 49F gold was fenced from dell2 (row W14-S1) until the fence join applied (TO-APPLY-4 amendment 1
  @aefcf32c11). The issuer probed it at 10:44Z, withdrew the laptop relay (ids 356/357), and the worker ran on dell2.

## Where FWD-8 stands after round 19

On the gross basis, 9,078 graded segments: 5,416 within; 3,662 outside. Of the outside: FLOW_TIMING 333 + 226 (the second figure is
inferred), INCOME_DATE 44, COVERAGE_DAYS 5, MISSING_PRICE 1; UNEXPLAINED 754 (non-closure) + 2,299 (closure) = 3,053, which is 33.6% of
9,078. FWD-8's ACCEPT ("every day they disagree carries a stated reason") still fails.

## Rows in the round

| row | class | standing |
|---|---|---|
| W14-S1 | BLOCKING, INERT | resolved by S28 (@09dde1b9a1): the fence opened and the read ran on dell2 |
| W14-S2 | OBSERVATION, INERT | DISMISSED (the worker's record of the dell2 run) |
| S28 | OBSERVATION, INERT | the issuer's `adjudicates` row for W14-S1 |

OPEN 0, ARMED 0 (comp-surprise after S28).

## Not done this round

- E3 (`account_class_daily`, FWD-3) still waits on the six-class values in `_shared/etf_classification.py`.
- The live thread trace (FWD-1 hop 5) was not re-run: both cells were offline measurements and dell2 holds no signed-in portal
  session. Its last exercised run stays 2026-10-02 (STATUS~D).
