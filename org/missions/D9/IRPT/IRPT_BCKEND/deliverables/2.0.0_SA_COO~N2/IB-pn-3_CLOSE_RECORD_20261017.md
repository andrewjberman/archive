# IB-pn-3 close record -- the one real run (2.0.0_SA_COO~N2, 2026-10-17 ~12:5xZ)

Order `IRPT_BCKEND.TO-IB-pn-3` (workstream ~PN round 5), worker `0.9.0_WK_IRPT_BCKEND~481`, merged as `3b3d3e9f94` (LOCAL on box/dell2) through `.tools/safe-merge.sh`: fast lane, 7 of 7 merged paths present at HEAD, 0 dropped, 0 foreign.

Run on the MERGED main tree from the repository root:

| invocation | output |
|---|---|
| `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/checks/r3/pn_region_cells.py . IBN3-AC1` | `IBN3-AC1 PASS` |
| the same file, `IBN3-AC2` | `IBN3-AC2 PASS` |
| the same file, `IBN3-AC3` | `IBN3-AC3 PASS` |

Base controls (151e71f132, before the worker): AC1 `NoRegionError`, AC2 `line 327 boto3.client` without `region_name`, AC3 `new test file absent`. The worker's own run of the criteria in its tree and its proof instance (`proof-of-spec-check.py` VALID rc=0) were re-run by this seat before the merge.

Drain checks, once: `py_compile` of the feed script OK; `ruff check --target-version py39` on the script and the new test file: all checks passed.

Limits: the end-to-end test fakes the Orion transport below the real `OrionPost` and supplies a synthetic sidecar; the flat directory the checks build is made from the repository folders, not the deployed S3 objects. The worker filed three OBSERVATION rows (W481-S3 to S5, all INERT). Slot ~481 had already been used earlier on this project by another seat's workers (TO-IB-pr-617 and 619); the row ids W481-S1 and S2 are theirs, the folder `deliverables/0.9.0_WK_IRPT_BCKEND~481/` holds both seats' files under distinct names, and no id collided at the merge. Future slots from this seat: ~490 and up.

New script bytes: blob `e2ed945d2e920673231e0848a5e51784aefc4db8`, sha256 `a92589d697bac504d5338b434d49c5cb1ccb09926c6fe8720fc6a72c5de8dfae`. Worktree `C:/dev/wk-IRPT_BCKEND-481` and its branch removed.
