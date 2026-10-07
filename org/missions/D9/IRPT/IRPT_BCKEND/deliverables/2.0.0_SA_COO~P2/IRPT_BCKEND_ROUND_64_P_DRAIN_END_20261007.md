# L8 drain end -- IRPT_BCKEND round 64, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~11:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

**Cut from:** the IRPT_CUSTDY round-3 analysis @ec25e39844, S8(b) (msg 383), as one read-only measurement cell. Issuance @f3d1ef5587,
decomposition section 57.

## The order

**IB-pr-342, the directory-coverage census.**
- **Drain:** @9b933b3f15.
- **Criteria:** IB64-1-AC1 and the guard PASS; proof VALID; the issuer re-ran AC1.
- **Judgment criteria:** 0.
- **Result:** `deliverables/0.9.0_WK_IRPT_BCKEND~144/IB64-1_directory_coverage.json`, with the per-reason build change in the
  `.result.md` beside it. The worker recomputed it from the sources rather than reading IRPT_CUSTDY's files.

**Denominators.**

| firm | granted | in directory | not in directory |
|---|---|---|---|
| 49 Financial | 7,022 | 5,061 | 1,961 |
| Inflection | 0 (no ownership map object) | 0 | 0 |
| Cottonwood | 0 (the map at opal-data-cot holds 0 advisors) | 0 | 0 |

**Why each account is absent.** UNEXPLAINED is 0.

| count | reason |
|---|---|
| 1,447 | `BD_KEY_ABSENT_FROM_EVERY_BRIDGE_SOURCE`: no path to a Schwab id in 53 xref partitions, 53 fee-role partitions, `fact_bd_allocation` or `fact_taxsma_report` |
| 343 | `XREF_UNRESOLVED_NO_SCHWAB_MATCH`: the xref row exists but its Schwab id is null |
| 139 | `XREF_UNRESOLVED_NUMBER_IN_DIM_ACCOUNT_ONLY`: as above, and the account number matches a `dim_account` row that `dim_relationship` lacks |
| 32 | `ACCOUNT_CARRIED_ABSENT_FROM_FEED_NOT_IN_RELATIONSHIP`: open accounts carried absent-from-feed since June-August 2026; `a01_dim_relationship.py:228` builds the universe from today's feed, so they never reach `dim_relationship`, the directory's source |

The 482 xref-unresolved accounts are the same population as IRPT_CUSTDY W5-S1 (the 826 'None' seam values).

## Row filed

**W144-S1** (OBSERVATION): the order named the buckets opal-data-49financial / -inflection / -cottonwood, but the directory registry
reads opal-data-bd / -inf / -cot. The issuer's face was wrong; the worker read the right buckets and widened no fence.
