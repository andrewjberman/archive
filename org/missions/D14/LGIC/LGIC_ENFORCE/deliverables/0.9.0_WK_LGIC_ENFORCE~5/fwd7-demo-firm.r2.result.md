# LGIC_ENFORCE.TO-EN-d-1-r2 -- result

Worker `0.9.0_WK_LGIC_ENFORCE~5`, cell `EN-d-1`, round 2. Worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-2d-5`, branch
`wk-lgic-enforce-2d-5`, base CLOUD @`2a2b853f79`.

## What landed

| path | commit |
|---|---|
| `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD7_R2.md` | `1091a6cd3e` |
| `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~5/expected_diff.r2.txt` | `1091a6cd3e` (and `529b5c39fb` on the scratch branch, where it is the `expected_set` commit) |
| the six saved outputs and the two patches | `1091a6cd3e` |

On scratch branch `prac-lgic-enforce-d1-r2` (never pushed, never merged, worktree removed clean):

| commit | what |
|---|---|
| `529b5c39fb` | **expected_set** -- the 10 paths, derived and committed before the row existed |
| `ed8771f9e8` | **generated** -- one 17-line `scopes.json` row, then `generate --out .` committed unedited |

## Criteria -- 6 of 6 MECHANICAL, 6 PASS by output, 0 JUDGMENT

Every invocation ran as `cd <WS> && timeout 120 python
org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_en_r2.py <sub>`.

| id | sub | deciding line | rc |
|---|---|---|---|
| D1R-AC1 | `d1r-firm` | `VERDICT: PASS-R2-FIXED-FIRM` | 0 |
| D1R-AC2 | `d1r-order` | `VERDICT: PASS-R2-EXPECTED-FIRST` | 0 |
| D1R-AC3 | `d1r-diff-equal` | `VERDICT: PASS-R2-DIFF-EQUALS-EXPECTED` | 0 |
| D1R-AC4 | `d1r-zero-warnings` | `VERDICT: PASS-NEW-FIRM-DRAWS-NO-WARNING` | 0 |
| D1R-AC5 | `d1r-address-refused` | `VERDICT: PASS-R2-ADDRESS-REFUSED` | 0 |
| D1R-AC6 | `d1r-name-refused` | `VERDICT: PASS-R2-NAME-REFUSED` | 0 |

Denominators: AC3 `EXPECTED: 10  ACTUAL (minus the registry): 10  ONLY EXPECTED: []  ONLY ACTUAL: []`;
AC4 `validate AT expected_set: rc=0, 16 warning(s)  AT generated: rc=0, 0 refusal(s), 16 warning(s)` and
`WARNINGS NAMING quillwater OR qwt: []`.

## Controls

**The discriminator for AC5/AC6.** The same two patches run in the slot worktree, whose registry has NO
`quillwater` row: the address grades `NAMING-GATE: WARN 1 graded` at rc 0 (a RAISE, not a refusal) and the
name file grades `NAMING-GATE: PASS 0 graded` at rc 0. With the row, rc 1 and `REFUSE 1` / `REFUSE 2`. The
refusals are produced by the one row and by nothing else.

**The control for AC3.** Before the row, `generate --out .` in the practice copy wrote 10 files and
`git diff --name-only` printed 0 paths -- so the 10 paths in the actual diff are the row's effect, not
pre-existing drift. Corroborated on a second instrument: each `git cat-file -p HEAD:<path>` blob compared
byte-for-byte to the worktree file, 10 of 10 equal, 0 CR bytes on either side.

**Determinism.** All six criteria ran twice on the same bytes -- once with the practice worktree still
present, once after `git worktree remove` -- and printed the same six PASS verdicts at rc 0 each. The
checker reads the two commits from the object database, so removing the worktree does not move it.

## What is NOT claimed

- Nothing was written to AWS and no Terraform command ran.
- The scratch branch is not merged and is not proposed for merging. `git ls-remote --heads origin
  prac-lgic-enforce-d1-r2` printed 0 lines.
- `quillwater` is fictitious. No real firm was added, and the slot branch carries no registry or carrier
  change -- `git diff --name-only` against the base lists only this worker's records.
- AC4's reading is that a scopes row has **no reachable warning site** in `validate()` (the one
  `warnings.append` is `lib/opal_naming.py:425`, inside the `systems.json` loop). That is a property of the
  code at `2a2b853f79`, not a guarantee about a future validator.

## Surprises

None filed. No premise of the order failed, no path was missing, every named invocation produced its named
result, and no tracked file outside `<paths>` was modified (`git diff --name-only` on the slot worktree
prints 0 paths).
