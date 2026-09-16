# RESULT -- LGIC_CANON.TO-CN-r-2 (FWD-3 graded from the record), round 1

**Worker:** `0.9.0_WK_LGIC_CANON~3` (slot ~3, queue position 2; cold start) | **Branch:** `wk-lgic-canon-1-3`
**Worktree HEAD at work:** `83afab6973` (cut from `CLOUD` @`f95470f384`, carrying CN-r-1's two commits)
**Deliverable:** `org/missions/D14/LGIC/LGIC_CANON/deliverables/FWD3_FROM_RECORD.md`

## 1. The bar

- `git rev-parse --abbrev-ref HEAD` -> `wk-lgic-canon-1-3`; `test -d org && test -d .tools` -> `TREE-OK`.
- Every path the order names exists in the worktree: the task order, the fixed checker, both contradiction reports,
  both IRPT PRDs, the LGIC_CANON PRD (DEC-4 at `:186-194`) and the nine-calls record.

## 2. Premises re-grounded at HEAD

| premise (from the order) | measured | instrument |
|---|---|---|
| The nine-calls record at `@c6be748be7`, card 1, lifts the pause for both IRPT projects by name | holds: `:32` reads "(a) BOTH IRPT projects. THE PAUSE IS LIFTED, by his word, by name." `c6be748be7` is the only commit on the file; `git diff --stat c6be748be7 HEAD` is empty | `git cat-file -e`, `git log`, `git diff --stat`, `git show c6be748be7:<path>` line 32 |
| IRPT_FNTEND's grade is derived from IRPT_BCKEND | holds: `IRPT_FNTEND.md` v2.1 `:15-16`, `:33-34` | Read at HEAD; `a4cc0cb681` is the last commit on the file and the diff to HEAD is empty |
| IRPT_BCKEND carries three CONTRADICTS: `platinum/` (R1), gold parquet (R11, R14), vendor PDFs' home (R4 partial) | holds: `IRPT_BCKEND.md` v2.1 `:18`, rows `:35`, `:36`, `:37` | Read at HEAD; `a4cc0cb681` last commit, diff to HEAD empty |
| DEC-4: the PRD is still v0.14 @`b8e98d5a4d` and carries none of the three | holds, RE-MEASURED rather than copied: `"prd_version": "v0.14"` at `:8`; `b8e98d5a4d` is the last commit on the file; `git diff --stat b8e98d5a4d HEAD` is empty; the `CLOUD` tip `5061a43a46` has the same bytes (`git diff --stat HEAD CLOUD` empty). Token census, 322 lines: `platinum/` 0; `parquet` (-i) 2, both input evidence (`:125`, `:216`); `opal-data-assets` 0; `R20` 0. Destinations unchanged at `:196`, `:199`, `:311-313` | `grep -c` / `grep -ni` on the file at HEAD; `git log`; `git diff --stat` (two instruments: byte diff and token census) |

No premise failed, and no surprise row was filed on this order.

## 3. What was written

`FWD3_FROM_RECORD.md`, 5,727 bytes, 60 lines, 0 non-ASCII bytes, LF endings:
- `PROJECT IRPT_FNTEND: branch derived`: card 1 cited `...NINE_CALLS...md@c6be748be7 :32`; the deciding project
  cited `infra/logic/03_CONTRADICTION_REPORTS/IRPT_FNTEND.md@a4cc0cb681 :15-16, :33-34`.
- `PROJECT IRPT_BCKEND: branch list-of-changes`: card 1 cited `@c6be748be7 :32`; the list cited
  `infra/logic/03_CONTRADICTION_REPORTS/IRPT_BCKEND.md@a4cc0cb681 :18, :35, :36, :37`.
- `IRPT_BCKEND PRD AT HEAD: v0.14 (MEASURED)`, with the instrument stated.
- `CONTRADICTS ABSORBED: 0 of 3 (MEASURED)`, followed by a per-CONTRADICTS table that marks all three **OPEN**
  and owed at the PRD's next L4 re-entry, plus the census's limit and the byte diff that bounds it.

## 4. Criteria

| id | invocation | output (verbatim) | rc | denominator | status |
|---|---|---|---|---|---|
| R2-AC1 | `cd /c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-3 && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py r2-branches` | `PROJECTS: 2  BRANCH CITED: 2` / `VERDICT: PASS-R2-BRANCHES-CITED` | 0 | 2 of 2 projects with a branch line carrying a resolvable path@commit | PASS-by-output |
| R2-AC2 | `cd /c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-3 && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py r2-bckend` | `PRD version at HEAD: v0.14  RECORD STATES: v0.14  ABSORPTION LINE: CONTRADICTS ABSORBED: 0 of 3 (MEASURED)` / `VERDICT: PASS-R2-BCKEND-MEASURED` | 0 | 1 PRD version compared with the live field; 1 absorption line over 3 CONTRADICTS | PASS-by-output |
| R2-J1 | read `FWD3_FROM_RECORD.md` against FWD-3's ACCEPT | RECORDED, no verdict | -- | 2 projects, each with a branch and its cited row | UNVERIFIABLE-BY-INSTRUMENT (graded at L9 by `3.0.0_SA_CVO`) |

No stderr on either run. The cp1252 decode defect (row `LGIC_CANON-W3-S1`) is not reached by `r2-*`, because those
subcommands resolve citations with `git cat-file -e` and never decode `git show` output.

## 5. Controls

- **Mutants** (`.scratch/r2mut/run_mutants.py`). Each mutant is a doctored copy in a mini-root under `.scratch/r2mut/`,
  never the tracked file, run through the unmodified checker:
  - M1: every commit on the FNTEND line set to `@0000000000`. Result: `BRANCH CITED: 1`, `FAIL-R2-BRANCH-UNCITED`.
  - M2: the BCKEND branch set to `resumed`. Result: `FAIL-R2-BRANCH-UNCITED`.
  - M3: the version stated as `v0.13`. Result: `RECORD STATES: v0.13`, `FAIL-R2-BCKEND-UNMEASURED`.
  - M4: the absorption line removed. Result: `ABSORPTION LINE: None`, `FAIL-R2-BCKEND-UNMEASURED`.
  - M0: the clean copy, run through both subcommands. Result: PASS on both.
  - **6 of 6 as expected.**
- **Determinism:** both criteria were run again on the committed bytes (recorded in the proof instance).
- **What the checker cannot see:** R2-AC2 grades that the absorption line EXISTS and names 0-3. It does not grade that
  the number is right. The number here comes from the two instruments in section 2, and a reader should weigh it
  against them, not against the PASS.

## 6. Declared limits

- Whether the record supports each branch is R2-J1, and it is not graded here.
- The contradiction reports' channel denominators (188/71, 138/41) are marked perishable by their author and were
  not re-taken. Nothing in this cell depends on them.
- `CLOUD` tip `5061a43a46` was read once, at work time. Push state of this branch: LOCAL (never pushed; the COO drains).
