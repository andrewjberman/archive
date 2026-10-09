# L8 drain end -- ADVI_COTBKF round 30

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~09:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB30ad1-AC2)

Round 30 was cut as one issuance @9a2399d831 (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 5 @abbf204c7e (msg
2921).
- Enrichment item 2 was drained in round 29.
- Item 3 waits on a price fill: the store index still reads rows 32, as_of 2026-06-23.

| order | item | worker | state |
|---|---|---|---|
| CB-ad-1 | read-only trace of D2-S45's r28/r26 factor on B3S728504 and B3S728506 | ~57 | complete @816400901c, drained @abe8a94a17 |

## The real run, shared tree, after the drain

```
SCALE-TRACE accounts=2 split_double_applied=0 split_missing_r26=0 cash_leg=0 other=0 untraced=2
```

The issuer's run matches the worker's.

## What the round found

**The factor is located.** On both accounts it is carried by two CUSIPs and nothing else (scale_trace.md, ~57):

| CUSIP | close r28 / close r26 | split applied by r28 | date | source |
|---|---|---|---|---|
| 808524102 | 3.0000 on every scaled sample day | x3 | 2024-10-11 | rows |
| 808524839 | 2.0000 on every scaled sample day | x2 | 2024-10-11 | rows |

- After 2024-10-11 the ratio is 1.0000.
- Cash is identical under both methods.
- Example, B3S728504 on 2022-10-12: 426 sh of 808524102 at 13.3302 (r26) vs 39.9906 (r28).

**Which level is right is still unmeasured.** Both accounts are classed `untraced` by the pre-written rule:
- The delivery carries no market value and no trade price for these CUSIPs. They enter only as li/trfi/QA/dv/lo rows: 0 of 10
  carrier-days per account have an outside price.
- Under `method_r28`'s own test, each split was applied because the chain close was continuous across the split day. That means r26
  holds split-adjusted closes and r28's as-traded level is right. This is an INFERENCE (row W57-S1), not an outside value.

**The measurement that would settle it (proposed for round 31):** the as-traded (unadjusted) close of 808524102 and 808524839 on one
pre-split day.
- Sources: dell1 MDPF_DEMQUE's `as_traded_close` once it holds these CUSIPs, or a direct Yahoo read. Egress is open except Bloomberg.
- If it reads ~39.99 / ~39.44 on 2022-10-12, r28 is right and FWD-3's PARTIAL lifts with no re-mint.
- If it reads ~13.33 / ~19.72, r28 double-scales. The two accounts' served levels are then repaired, or blanked under a pair.

**Rows:** W57-S1 (OBSERVATION, INERT). The worker disclosed one non-threshold fix after its first run: a date-type conversion, in its
commit and its row. ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB30ad1-AC2. Orders 1/1 complete.
