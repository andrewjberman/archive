# IB-pn-1 close record -- the one real run (2.0.0_SA_COO~N2, 2026-10-16 ~14:0xZ)

Order `IRPT_BCKEND.TO-IB-pn-1` (workstream ~PN round 4), worker `0.9.0_WK_IRPT_BCKEND~480`, merged as `7b47813ad1` (LOCAL on box/dell2) through `.tools/safe-merge.sh`: fast lane, 6 of 6 merged paths present at HEAD, 0 dropped, 0 foreign.

Run on the MERGED main tree, not the worker's tree, from the repository root:

| invocation | output |
|---|---|
| `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/checks/r1/pn1_cells.py . IBN1-AC1` | `IBN1-AC1 PASS` |
| the same file, `IBN1-AC2` | `IBN1-AC2 PASS` |
| the same file, `IBN1-AC3` | `IBN1-AC3 PASS` |

Base controls (a9c3f46a3d, before the worker): AC1 `IndexError: 2`, AC2 `FileNotFoundError` on the sibling `scripts/gold/` builder path, AC3 `new test file absent`.

Drain checks, once: `py_compile` of the feed script OK; `ruff check --target-version py39` on the script and the new test file: all checks passed. The worker's order flip to complete and its proof instance (`python .tools/proof-of-spec-check.py`: VALID rc=0) were re-run by this seat in the worker's worktree before the merge.

Limits: the flat directory the checks build is made from the repository folders the runner's sync names, not from the deployed S3 objects; the deployed script object's bytes were not read. The worker's report noted the naming gate printed two WARN verdicts (not enforced) on literals in the new test file, and that the hashed account-id client-data check did not run on this box (the new test file uses no literal ids). No row was filed by the worker; row `IRPT_BCKEND-D2-S221` (IB2) is the finding this cell answers.

Worktree `C:/dev/wk-IRPT_BCKEND-480` and branch removed. Corrected script: blob `233cf1e604751619ef2b1132c8c6bdb863f2bc13`, sha256 `4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32`.
