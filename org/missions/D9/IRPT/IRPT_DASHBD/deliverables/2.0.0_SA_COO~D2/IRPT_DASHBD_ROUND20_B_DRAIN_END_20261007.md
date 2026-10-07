# L8 drain end -- IRPT_DASHBD round 20, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~11:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @8e4c07ce7e

Both orders are terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer before each drain).
0 JUDGMENT criteria. Both cells are LOCAL: S3 reads only, no served byte moved, no vendor call. Both worktrees and branches were removed.
On: `1.0.0_SA_CTO~DELL2`'s round-19 analysis @b402b7b2e3 with its E1 method ruling (msg 400). The split-at-2025-01-09 BD pull stays
listed for Andrew (2,299 accounts, 2,299 calls, 4,598 ranges) and was not cut.

## Orders

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-31 (E1: measure the 226 inferred FLOW_TIMING) | @8e4c07ce7e (worker ~16: 747fb92c4e, e6da5fdc9e) | DB20-1-AC1..AC3 PASS | **22 measured, 204 returned to UNEXPLAINED.** All 226 pass the flow-totals guard (Opal's `external_flow` sum equals BD's netAdditions), so every return is on the Dietz gap. Negative control: 19 of 226 within with flows at the midpoint |
| DB-b-32 (E2: the 754 non-closure residue, Opal's side) | @00d950283a (worker ~17: 4be6241e38, e4d5a17534) | DB20-2-AC1..AC3 PASS | **0 of 754 gain a reason.** Every segment was read with Opal's served days |

## Read before grading

- **The midpoint control nearly matches the measured count, and the two sets barely overlap.** The issuer read the record: 22 measured,
  19 within at the midpoint, 3 in both (19 measured only, 16 midpoint only). A wrong flow placement fits about as many segments as
  Opal's actual dates. On the CTO's own test ("a method that explains everything explains nothing"), the 22 are weak evidence for flow
  timing. They are marked MEASURED by the rule as ruled; whether that rule discriminates is the CTO's call.
- **DB-b-32 adds no reason, as expected in hindsight.** Round 18's gross re-grade already applied the round-17 rules against Opal's
  served series for these segments, so a re-read under the same rules reproduces UNEXPLAINED. What is new is that all 754 were read with
  served days, so none is unexplained for lack of data.

## Where FWD-8 stands after round 20 (measured basis)

9,078 graded: 5,416 within; 3,662 outside = FLOW_TIMING 333 (round 18, re-link rule) + 22 (round 20, Dietz rule), INCOME_DATE 44,
COVERAGE_DAYS 5, MISSING_PRICE 1, **UNEXPLAINED 3,257 (35.9%)** = 2,299 closure + 754 non-closure + 204 returned. FWD-8's ACCEPT still
fails. The one listed act that can still move the closure share is the split BD pull, which waits on Andrew's word.

## Rows in the round

None filed. OPEN 0, ARMED 0 (comp-surprise after both drains).

## Not done this round

- E3 (`account_class_daily`, FWD-3) still waits on the six-class values in `_shared/etf_classification.py`.
- The live thread trace (FWD-1 hop 5) was not re-run: both cells were offline measurements and dell2 holds no signed-in portal session.
  Its last exercised run stays 2026-10-02 (STATUS~D).
