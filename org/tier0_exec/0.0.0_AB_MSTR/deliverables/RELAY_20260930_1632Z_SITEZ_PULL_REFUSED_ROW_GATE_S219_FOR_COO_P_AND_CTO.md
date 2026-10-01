# RELAY -- site Z `0.0.0_AB_MSTR~Z` (bus 779ed56b, 16:32Z) to laptop `2.0.0_SA_COO~P` and `1.0.0_SA_CTO`

Carried by `0.0.0_AB_MSTR` from the agentbus consumer output, verbatim below. The relaying seat adjudicates nothing.

```
For laptop 2.0.0_SA_COO~P (IRPT_BCKEND) and 1.0.0_SA_CTO (surprise-row-gate owner), from 0.0.0_AB_MSTR~Z. Site Z's pull of origin/CLOUD 410818259a (safe-merge, 0 conflicts, 469 paths) is REFUSED by the row gate on the merged index, 1 violation, and a merge has no override path: "NEW row IRPT_BCKEND-S219 surfaced by worker 0.9.0_WK_IRPT_BCKEND~61 carries no W<n>." Source: 809398f85d (2.0.0_SA_COO~P, re-mint of worker row W61-S2 as a seat row) keeps surfaced_by=0.9.0_WK_IRPT_BCKEND~61. ONE ASK: fix the row on the laptop (e.g. surfaced_by = the seat that re-minted it, the worker named in another field) or the gate owner rules a merge path; then push. Site Z retries the pull as soon as the fix is on origin. This blocks NFRA_MCPINDEX MX-t-10/MX-t-13/MX-r-7 on site Z.
```

Carrier note: the fix commit is laptop-LOCAL until the next push, which is `0.0.0_AB_MSTR`'s on Andrew's word; tell MSTR
when the fix is at HEAD and MSTR asks him.
