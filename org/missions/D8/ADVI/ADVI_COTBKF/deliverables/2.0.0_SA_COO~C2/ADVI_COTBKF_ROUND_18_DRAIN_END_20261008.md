# L8 drain end -- ADVI_COTBKF round 18

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~07:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 18 was cut as one issuance (@3a5cad1cef, `fanout: 3 of 3 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-17 analysis
@0ae2f15e5c (msg 1185). 3 of 3 orders terminal and merged; proofs VALID; 0 unmerged worker branches; 0 linked worktrees for this
project. The SERVED item was applied under a pair and a closed ledger.

| order | item | worker | drain | criteria |
|---|---|---|---|---|
| CB-r-1 | E1 non-positive base reads blank | ~37 | @40d40e22e4 | VALID: AC1 6 passed; AC2 below |
| CB-r-2 | E2 index page counts (SERVED) | ~38 | @e4ab655cf9 | VALID: AC1 3 passed (`-k page_count`); AC2 below; applied, below |
| CB-r-3 | E3 flow-month DIFF classed | ~39 | @afc9554189 | VALID: AC1 4 passed (mutant control fired); AC2 below |

## The real runs, shared tree, after the drains

```
DAILY-RETURNS account_days=1691729 computed=100371 blank=1591358 flow_types=61 of 61 zero_amount=20403 valued=5017 blank_no_price=15386
MONTHLY-GRADE months=82593 match=1685 diff=1931 ungradable=78977 tolerance_pct=0.05
NON-POSITIVE-BASE days_blanked=29603 months_before=1973/2264/78356 months_after=1685/1931/78977
FLOW-DIFF-CLASSES diff_flow_months=703 classes=6 largest=lo/over 10% largest_months=249 examples=3
INDEX-PAGE-DIFF rows=11119 served_version=xS7loply3Eug2dT30ffGOyFgfQt7K8OM only_page_count_differs=True filled=11087 null=32 other_columns_differing=0
```

## What each item found

- **E1, the ruling applied.** 29,603 days now read `NON_POSITIVE_BASE`: 2,578 zero-base and 27,025 negative-base days (27,044
  follow a negative value; 19 were already UNPRICED). MATCH falls 1,973 -> 1,685, because months that contained a computed
  negative-base day now read UNGRADABLE (78,356 -> 78,977) instead of grading on a meaningless ratio.
  - The before arm reproduces round 17 exactly (the control).
  - `commonwealth_flow_timing.py:188` still names `ZERO_BASE` in report prose. It was outside the worker's paths; a one-word repair
    for the next batch cell.
- **E3, where the flow-month DIFF comes from (rows W39-S1, W39-S2).** The largest class is `lo` over 10% of value: 249 of 703 DIFF
  flow months on the new base rule (252 of 857 on the worker's run before E1).
  - **Cause, read against the transactions:** a withdrawal is delivered as an `lo` of CFNCASH plus an `sl` of the FDIC sweep for the
    same amount. The account value falls by TWICE the withdrawal, while the return takes the flow out once.
  - **Evidence:** in 74 of 106 single-`lo` months the drop equals twice the flow (example: acct#05dd4a9d on 2023-07-14, `lo` 455.68 and
    `sl` 455.68, the value drops 911.36, the month computes -32.71% against a reported -0.18%).
  - **No fix in this item.** The repair, for the CTO to list: an `sl` of the sweep fund that pays an `lo` of cash on the same day is
    one withdrawal, not a sale plus a withdrawal.
  - **W39-S2:** the round-17 population (937 / 242) came from the flow-timing comparison, which counts only months graded under BOTH
    conventions. Over the committed grade, months with an external flow are 1,173 (316 MATCH). The class ranking does not depend on
    the gap.
- **E2, page counts SERVED (D2-S26 closed in the served table).**
  - **Pair:** COO half @9dfdce0b3e, CTO half @606b798fc8.
  - **Ledger:** `20261008T0659Z_advi-cotbkf-r18-index-page-counts-20261008`, opened @32c5415 before any write, closed with both legs
    proven.
  - **The apply:** rebuilt with the drained builder, hash-equal to the worker's drained build. Pins re-read unchanged at the apply.
  - **Read-back:** `document_index.parquet` `xS7loply...` -> `0aPGtfdm5pzHbMNqHP3KUHsFHGKYNS4t`: 11,119 rows, `page_count` on 11,087,
    null on 32 (31 not a PDF, 1 encrypted), every other column equal to the pin. `archives.parquet` `mSZeqb29...` ->
    `cjcZtTuUeOzunpowvYpqIVIKvv_.ubge`: 3 rows, same content, row order changed (recorded in the ledger).
  - **Correction:** the COO half swapped the two build hashes. `e60f6ce5...` is the index, `569d4b88...` the archives.

**Rows this round** (OBSERVATION / INERT): W39-S1, W39-S2. ARMED: 0.

**Enrichment candidates for the round-18 analysis** (the CTO's to list):
1. **The sweep-pair repair:** an `lo` of cash with a same-day `sl` of the FDIC sweep for the same amount is one withdrawal; then
   re-grade.
2. **A batch repair:** the `ZERO_BASE` prose in `commonwealth_flow_timing.py`.

**Still external:** MDPF_SECHIST's price load (FWD-3 coverage, 7.8% of account-days priced), the laptop's restricted-statements
apply, and Andrew's CRM landing.
