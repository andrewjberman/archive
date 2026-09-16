# RESULT -- LGIC_ENFORCE.TO-EN-p-1 (FWD-6 on a practice copy) -- RE-RUN

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Slot branch:** `wk-lgic-enforce-1-2-p1r`, cut from `CLOUD` @9a05002d39 | **Scratch
branch:** `prac-lgic-enforce-p1` @6640c8153d (never pushed, not touched by this run) | **Record:**
`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD6.md` @89664b0829

**Verdict: all four criteria PASS by output.** P1-AC1, P1-AC2, P1-AC3 and P1-AC4 each print their expected verdict with
rc=0. The order flips to `complete`.

## 1. What this run is

This is a re-run. The cell's work was done by the prior slot-2 run on `wk-lgic-enforce-1-2-p1` (record @89664b0829, proof
and result @0bbb96676c) and merged at the drain @38691b5c74. That run read P1-AC1 as FAIL-NOT-EVALUABLE because
`check_en.py p1-surface` stopped on a carrier whose grade RAISES (row `LGIC_ENFORCE-W2-S7`). The issuer fixed the checker
@c30637c49c (issuer row `LGIC_ENFORCE-S12`). This run did not redo the exercise. It made no practice copy, did not touch
the scratch branch, and wrote no new surprise rows. It re-ran the four criteria and re-recorded them.

## 2. The bar

- `git rev-parse --abbrev-ref HEAD` read `wk-lgic-enforce-1-2-p1r`, HEAD 9a05002d39, and `TREE-OK` printed.
- **Premises re-grounded at base:**
  - 89664b0829 (EXERCISE_FWD6.md and rows W2-S7..S9), 0bbb96676c, c30637c49c and 38691b5c74 are each ancestors of HEAD
    (`git merge-base --is-ancestor`).
  - EXERCISE_FWD6.md's last touching commit is 89664b0829.
  - `check_en.py`'s last touching commit is c30637c49c.
  - The plant commit 6640c8153d is NOT on HEAD. That is expected: it lives only on the scratch branch.

## 3. Verdicts (each run under `timeout 120`, from `<WS>` = `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-1-2-p1r`)

| criterion | subcommand | deciding output | rc |
|---|---|---|---|
| P1-AC1 | p1-surface | `RECORD: .claude/skills/mdpf-refresh/mdpf_refresh.py  BY RULE: .claude/skills/mdpf-refresh/mdpf_refresh.py  (carriers read: 23 of 12953, passed over on a RAISE: 18)` / `VERDICT: PASS-SURFACE-BY-RULE` | 0 |
| P1-AC2 | p1-refused | `NAMING REFUSE .claude/skills/mdpf-refresh/mdpf_refresh.py:292 ... the live remediation PRAC_FWD6REM` / `VERDICT: PASS-REFUSED` | 0 |
| P1-AC3 | p1-passed | `NAMING-GATE: PASS 0 graded` / `VERDICT: PASS-REMOVAL-PASSES` | 0 |
| P1-AC4 | p1-branch | `BRANCH: prac-lgic-enforce-p1  PLANTED-ROW COMMIT 6640c8153d4367520e8c1ea52f000d2f74f3d6fd ON IT: True` / `VERDICT: PASS-EVIDENCE-ON-BRANCH` | 0 |

## 4. Limits

- **Same instrument.** P1-AC2, AC3 and AC4 were re-run with the same checker the prior run used. That is repetition, not
  corroboration. Only P1-AC1's reading changed, and it changed because the instrument changed @c30637c49c.
- **Limits carried from the exercise:**
  - Arm 2 grades 0 strings, because the replacement sits in a permitted `key()` context.
  - The surface was already owned by MDPF_CANON before the plant (row W2-S8).
  - `validate` refuses the fictitious row (row W2-S9).
- **Nothing live moved.** No AWS read or write, and no Terraform.
