# R32 M multi-relationship grade (0.9.0_WK_IRPT_BCKEND~154, TO IRPT_BCKEND.TO-IB-m32-321)

Read-only grade of the delivered file. No AWS call, no reader re-run, no bun. All three invocations rc=0.

## IBM32-321-AC1 -- `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R32_CHECKS/r32_delivered_read.py m1`

```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R32M_MULTI_RELATIONSHIP_READ.json@09e0d7c89c sha256 e2606081349ee91aef56ede3fac5c368f57cbcff057bae23922e92de1595f56a (pinned e2606081349ee91aef56ede3fac5c368f57cbcff057bae23922e92de1595f56a)
m1: account acc_0f1e215e521798954f80f291 in relationships ['z09305591', 'z09326136']; 3 account(s) hold more than one Relationship ID of 860 with relationship rows
M1-MULTI-RELATIONSHIP-NAMED
```

## IBM32-321-AC2 -- `... r32_delivered_read.py m2`

```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R32M_MULTI_RELATIONSHIP_READ.json@09e0d7c89c sha256 e2606081349ee91aef56ede3fac5c368f57cbcff057bae23922e92de1595f56a (pinned e2606081349ee91aef56ede3fac5c368f57cbcff057bae23922e92de1595f56a)
m2: 58 raw rows -> 29 unique positions (29 duplicate relationship rows collapsed); subtree ties True over 4 partitions, 0 unbalanced; rebuilt 462857.7422 vs served 462857.7422 (2026-10-05 2026-10-05 rev bb51912332f6)
M2-RECONCILES
```

## IBM32-321-AC3 -- `... r32_delivered_read.py m3`

```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R32M_MULTI_RELATIONSHIP_READ.json@09e0d7c89c sha256 e2606081349ee91aef56ede3fac5c368f57cbcff057bae23922e92de1595f56a (pinned e2606081349ee91aef56ede3fac5c368f57cbcff057bae23922e92de1595f56a)
m3: of 860 accounts -- both 1, multi-model only 180, multi-relationship only 2, neither 677
M3-OVERLAP-MEASURED
```

2x2 sum: 1 + 180 + 2 + 677 = 860 = account denominator.
