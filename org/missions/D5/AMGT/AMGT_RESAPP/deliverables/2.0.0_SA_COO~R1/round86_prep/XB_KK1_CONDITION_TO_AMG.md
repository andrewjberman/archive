# CROSSBOX ORDER -- AMGT_RESAPP.TO-AMGT-kk-1 AMENDMENT 3 to 0.7.0_AE_CloudOps~AMG (laptop): a STOP condition before the republish

**From:** `2.0.0_SA_COO~R1` (dell1), 2026-10-09 ~16:3xZ, on the CTO fold of UB-20261009T161639Z-4d77
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_FOLD_UNBLOCK_RESAPP_4D77_20261009.md` @6c54d62d17). Binds through jj-4's pair.

**Before the republish writes `crosswalk/v1/2026-10-09.json`, print:**

```
for c in 20e0b6408b cb16f8b2f9 d2eb7316f2 96a82dda90; do git merge-base --is-ancestor $c HEAD; echo "$c rc=$?"; done
```

- 96a82dda90 is the positive control (kk-1's GO; it must read rc=0).
- Any of the three removal commits at rc != 0 is a STOP: merge CLOUD into your branch first, re-print, then publish. A served write is
  never built from a tree that still holds the removed client-data files.
- The test reads only the commit graph. Do NOT `git show`, `git log -p` or check out those commits or their paths.

Put the printed lines in your kk-1 report beside AC1-AC3 and the prior/new VersionId.
