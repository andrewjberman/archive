# L8 drain end -- ADVI_COTBKF round 25

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~01:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB25y1-AC3, CB25y2-AC3)

Round 25 was cut as one issuance (@c77f7982e4, `fanout: 1 of 1 chains, cap 8`, restated @d71f30aa85) on `1.0.0_SA_CTO~DELL2`'s round-24
analysis @cdf5f13f3f (msg 1957). 2 of 2 orders complete; the chain drained once @052a80dd0f (20 of 20 paths, 0 dropped); proofs VALID;
0 unmerged worker branches; 0 linked worktrees for this project. Risk LOCAL: nothing applied.

| order | item | worker | criteria |
|---|---|---|---|
| CB-y-1 | E1: sourced treatments for the unlisted row types (`method_r25`) | ~47 | AC1 17 passed; AC2 `regressions=0`; AC3 JUDGMENT, yours |
| CB-y-2 | E2: the 39 carried levels traced; E3 grading: the 22 dividend months at pay and ex date | ~47 | AC1 14 passed; AC2 `regressions=0`; AC4 `dividend_both=22/22`; AC3 JUDGMENT, yours |

- **E3, the ex-date filing:** the issuer's record, not an order. The TO gate refused my attempt to cut it as one (Tier-1 assignee,
  born terminal, second issuance), and nothing was committed from that attempt.
  - The request (@c77f7982e4) reached dell1 `2.0.0_SA_COO~Q1` (MDPF_DEMQUE). Ex-dates were served @5a392db104: 39 rows, 16 CUSIPs.
    My request said 17; the table holds 16.
- **CB-y-2 AMENDMENT 1** @43e4871735 added AC4, the both-ways grading. CB-y-2 had not started, so the amended text was placed in the
  worker's worktree before it reached the order.

## The real runs, shared tree, after the drain (own `--data-dir`)

```
A  SWEEP-REGRADE ... months_before=3059/925/78609 months_after=3098/886/78609 control_same=False regressions=0 movers_back=138 year_chain_same=True r22_named=25/25 dividend_both=NA
C  SWEEP-REGRADE ... months_before=3098/886/78609 months_after=3094/890/78609 control_same=True regressions=6 movers_back=136 year_chain_same=True r22_named=25/25 dividend_both=22/22
pytest data/assets/scripts/silver/tests: 626 passed, 11 skipped
```

- A is `method` -> `method_r25`. C is `method_r25b` at pay date -> the same rule at ex date, with the tracked
  `EXDATES_ADVI_COTBKF_20261009.csv`.
- Both match the worker's lines.

## What the round found

- **E1, unlisted types:** MATCH 3,059 -> 3,098, DIFF 925 -> 886, 0 regressions; all 35 unlisted-type months MATCH. The source table
  was fixed in a commit before the real run (@679c3c22b5):
  - `cbf`, `bcf`, `stp`, `term`, `fco` are flows: the delivered descriptions, and the CRO's "every other charge is a withdrawal".
  - `ftax` and `stax` are flows only where they ride a same-day CFNCASH `lo` (pairing: 4,056 of 4,198 `ftax`, 107 of 112 `stax`).
  - `frntax` is internal, as income net of tax (1,086 of 1,086 sit on a same-security same-day `dv`).
  - `ASF` is internal, with no source, and is named as such.
- **E2, carried levels -- the premise did not hold (row W47-S1).**
  - The method's own cash ledger closes to 0.00 on 13 of 13 closed accounts, with 0 unmatched sales. What departs is the OLD
    `conditional` baseline.
  - By kind: 23 first-valued-day postings the baseline never made; 14 `ManAltF` payments for another account; 2 sweep sales funding a
    non-sweep purchase.
  - No fix was needed: `method_r25b` = `method_r25`.
- **E3 graded (round 24 AC4's parked clause, row W47-S2):** 20 of the 22 dividend months do not move between pay and ex date.
  - The 2 XOM months of RGY003587 (2025-06, 2025-09) turn DIFF -> MATCH under ex-dating.
  - But the same XOM dividends turn 6 other MATCH months DIFF (0QF878981, 0QF879181, RGY005018).
  - Net under ex-dating: MATCH 3,098 -> 3,094. Neither date is adopted; the default stays pay date.
- **Default:** `method` stays the default. `method_r25` is selectable and graded; adopting it as the default is the CTO's to rule
  (0 regressions, +39 MATCH).

**Rows this round:** W47-S1 (the carried-level premise), W47-S2 (ex-dating +2/-6). OBSERVATION / INERT. ARMED: 0.

**Round-close check:** REFUSED on two causes, both judgment and yours at L9: CB25y1-AC3 and CB25y2-AC3 UNGRADED.

**Enrichment candidates for the round-25 analysis** (the CTO's to list):
1. **Adopt `method_r25` as the default** (0 regressions, MATCH 3,098).
2. **The remaining 886 DIFF months:** a fresh cause census on the new baseline.
3. **Dividend dating:** pay date stays, on the measured +2/-6.

**Cross-fabric, done this round:** an AMLP consumer read for dell1 MDPF_DEMQUE @14d4fc7049. Living client 0QF880237 was valued on
1,058 days with 0 unpriced; trade prices agree 3 of 4 within 2%. dell1's CTO filed it as their hop 6.

**Parked, owner `~C2`:** the ranked price-need list, un-parked by the dell1 data-queue project's L2.
