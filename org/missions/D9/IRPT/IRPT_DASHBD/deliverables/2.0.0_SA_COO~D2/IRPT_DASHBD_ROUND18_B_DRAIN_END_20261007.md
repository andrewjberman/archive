# L8 drain end -- IRPT_DASHBD round 18, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~10:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @21b59aa7b2

Both orders of the round are terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer in the
worktree before the drain). 0 JUDGMENT criteria. Both cells are LOCAL; no served byte moved, no vendor call. Watermark of the last
compile: REMEDIATION_v6 @88435e28a1. Worktree `C:/dev/wk-irpt-dashbd-13` and branch `wk-IRPT_DASHBD-13` removed after the drain.
On: `1.0.0_SA_CTO~DELL2`'s round-15..17 analysis @e363a194ed (W12-S1 ruled: one gross basis).

## Orders

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-27 (E1: the E2 tie-out on the gross basis) | @0f304c6405 (worker ~13: fb966b0a72, bcff7d006b, b2f19f5d65) | DB18-1-AC1..AC3 PASS under amendment 1 (@c6442ceec1) | 9,082 planned = 9,078 graded + 4 BD_NO_VALUE; 5,416 within 0.35 pp (round 17: 2,103); 3,662 outside: UNEXPLAINED 3,279, FLOW_TIMING 333, INCOME_DATE 44, COVERAGE_DAYS 5, MISSING_PRICE 1. 1,231 graded rows carry a null add-back. Opal's served figure is compared unchanged; no net-of-fee Opal figure exists |
| DB-b-28 (E2: the residue read) | @0f304c6405 (worker ~13: 302407ede0) | DB18-2-AC1..AC3 PASS | denominator 9,078; unexplained 3,279; plus-one-day over 2025-01-09 3,395; overlap 2,299; union 4,375. Residue by reason: UNEXPLAINED 3,279, COVERAGE_DAYS 979, FLOW_TIMING 107, INCOME_DATE 10 |

## How DB-b-27's record was made (read before grading it)

The dell2 identity is fenced from `s3://opal-data-49financial` by an explicit deny in the bucket policy (row W13-S1, re-measured by
the issuer). Under `1.0.0_SA_CTO~DELL2`'s standing rule, the laptop's `3.0.0_SA_CVO` ran the worker's script at fb966b0a72 unchanged
and read-only (@e6ed5380e6). The worker copied that record byte-exact (sha256 febe370fbed76497..., 4,196,573 bytes) and made no AWS
call. The record's `measured_by` field is the script's constant, not the seat that ran it.

## Findings for the CTO's round-N analysis

- The CTO's analysis expected about 1,345 UNEXPLAINED after the gross add-back. The measured figure is 3,279. The add-back moved 3,313
  segments within tolerance, short of the 4,905 that round 17's net-of-fee reading on Opal's side suggested; FLOW_TIMING rose by 183 and
  INCOME_DATE fell by 524, because their re-links are now graded against BD's gross figure.
- 2,299 of the 3,279 UNEXPLAINED segments are also +1-day segments over the 2025-01-09 closure. The worker kept them UNEXPLAINED,
  since the day count alone is not shown to explain the gap. No reason outside the closed set was filed.
- FWD-8's ACCEPT ("every day they disagree carries a stated reason") still fails: 3,279 of 9,078 graded segments are UNEXPLAINED.

## Rows in the round

| row | class | standing |
|---|---|---|
| W13-S1 | BLOCKING, INERT | resolved by S27 (@21b59aa7b2): the read ran on the laptop; the fence stands |
| W13-S2 | OBSERVATION, INERT | DISMISSED (the worker's record of the laptop run) |
| W13-S3 | BLOCKING, INERT | resolved by S27: a checker defect, fixed by amendment 1 |
| W13-S4 | OBSERVATION, INERT | DISMISSED (the worker's record of the fix) |
| S27 | OBSERVATION, INERT | the issuer's `adjudicates` row for W13-S1 and W13-S3 |

ARMED after the drain: 0. OPEN: 0 (comp-surprise after S27).

## Not done this round

- E3 (`account_class_daily`, FWD-3) waits on its named condition: `infra/aws/lambda/v2_portal/_shared/etf_classification.py` still
  carries fixed_income / equity / other (measured at 3dd25927f2).
- The live thread trace (FWD-1 hop 5) was not re-run this round. Both cells were offline measurements, and dell2 holds no signed-in
  portal session; the trace's last exercised run stays 2026-10-02 (STATUS~D).
