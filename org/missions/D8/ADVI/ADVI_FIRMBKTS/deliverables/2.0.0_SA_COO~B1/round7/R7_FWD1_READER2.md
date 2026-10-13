# ADVI_FIRMBKTS round 7 -- FWD-1: the second fresh blind reader (cell FB-j-1), the issuer's real run

Issuer `2.0.0_SA_COO~B1`, 2026-10-13 ~23:3xZ. The reader was worker `0.9.0_WK_ADVI_FIRMBKTS~68`; its directory is the detached worktree `C:/dev/wk-firmbkts-r7-reader`.

| read | command (issuer) | result |
|---|---|---|
| construction | `r6_fwd1.py reader --dir C:/dev/wk-firmbkts-r7-reader --root C:/dev/ajb_workspace` | `ROUND 6 READER: 4 of 4 arms` (the index is LOCATIONS.json alone, one parentless commit, the cut's bytes, answers complete) |
| agreement with the key | `r6_fwd1.py agree --dir C:/dev/wk-firmbkts-r7-reader` | reader=`0.9.0_WK_ADVI_FIRMBKTS~68`; locations 150; key 150; system, firm, tier and table each equal the key 150 of 150 (unknown 0); **all four equal the key 150 of 150**; no NOT-EQUAL line |
| ingest | `cmp` of the reader directory's `ANSWERS.json` with the issuer's copy `org/tier1_exec/2.0.0_SA_COO~B1/round7/blind/ANSWERS.json` | identical |

Reader 1 (round 6) read the same 150 against the same key and agreed 150 of 150 (`deliverables/2.0.0_SA_COO~B1/round6/R6_CLOSE.md`). Two fresh blind readers, each given only the location list, therefore
each placed all 150 canonical locations as the key does. That is the evidence for FWD-1 on the reading side; the grade (REALIZED or not) is the CVO's at L9, and no verdict is stated here.

What this does not show: the key is the mapping's own destination table, so the readers agreed with the mapping, not with any independent oracle beyond it; the 150 are the canonical-arm locations only.
