# RESULT -- LGIC_ENFORCE.TO-EN-p-1 (FWD-6 on a practice copy)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Slot branch:** `wk-lgic-enforce-1-2-p1`, cut from `CLOUD` @39aae459ed | **Scratch branch:**
`prac-lgic-enforce-p1` (never pushed) | **Record:** `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD6.md` @89664b0829

**Verdict: THE ORDER STAYS OPEN.** P1-AC2, P1-AC3 and P1-AC4 PASS by output. P1-AC1 is FAIL by output, because its
instrument cannot evaluate the rule (row `LGIC_ENFORCE-W2-S7`, BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~G`). No
`complete` flip.

## 1. The bar

- `git rev-parse --abbrev-ref HEAD` read `wk-lgic-enforce-1-2-p1` at 39aae459ed, and `TREE-OK` printed. Every path the order
  names was present: CARRIER_CENSUS.md, check_en.py, `.tools/naming-gate.py`, `lib/opal_naming.py`, and the five registry
  files.

## 2. Premises re-grounded

- **EN-g-1 and EN-r-1 are merged at base.** `.tools/naming-gate.py` and `infra/logic/registry/remediations.json` exist at
  39aae459ed. The registry validates at base: `VALIDATE: OK 16 system row(s), 9 scope row(s), 9 warning(s) at
  registry@50e4fabd1cb6a150`.
- **The rule's surface.** Sorted by (path, line), there are 12,953 carriers. Carriers 1-22 are 18 RaiseDefect and 4
  CONFORMANT. Carrier 23 is `.claude/skills/mdpf-refresh/mdpf_refresh.py:292`, token
  `platinum/mdpf/inflection/aggregate-aua-timeseries.json`, OUT-OF-PATTERN. The file is tracked and not ignored.
- **The premise that failed.** The order implies a row has to be planted before the touching diff is refused. At base,
  MDPF_CANON (status `active`) already owns the key through `s3-prefix platinum/mdpf/`, and the pre-plant control refuses
  (row `LGIC_ENFORCE-W2-S8`).
- **The instrument.** `check_en.py p1-surface` raises on carrier 1 before it reaches carrier 23 (row `LGIC_ENFORCE-W2-S7`).
  Fixed inputs are read-only, so the worker did not touch it.

## 3. What was done

1. Created the practice copy: `git worktree add -b prac-lgic-enforce-p1 <WS>/../prac-lgic-enforce-p1 HEAD`.
2. **Arm 0, the pre-plant control.** The touching edit's diff was refused, naming MDPF_CANON, rc=1.
3. **Planted ONE row**, `PRAC_FWD6REM`, owning `s3-prefix opal-data-portal-v2 platinum/mdpf/inflection/`, placed FIRST in the
   array so the limb names it. Committed as `plant` = `6640c8153d4367520e8c1ea52f000d2f74f3d6fd`, with every safe-commit
   stage clean (`[naming-gate] NAMING-GATE: PASS 0 graded`). Post-plant, `validate` refuses the row (row
   `LGIC_ENFORCE-W2-S9`).
4. **Arm 1, touching.** A trailing comment on line 292, with the string kept. `NAMING-GATE: REFUSE 1 graded`, naming the
   surface and `PRAC_FWD6REM`, rc=1. Discarded.
5. **Arm 2, removing.** The literal was replaced by a `key()` call. `NAMING-GATE: PASS 0 graded`, rc=0. Discarded.
6. `git worktree remove` on the clean practice copy (0 porcelain lines; rc=0; the directory is gone). The branch was left in
   place at 6640c8153d.
7. Wrote EXERCISE_FWD6.md and rows W2-S7..S9, committed as 89664b0829.

## 4. Verdicts (each run under `timeout 120`, from `<WS>`)

| criterion | subcommand | verdict line | rc |
|---|---|---|---|
| P1-AC1 | p1-surface | `VERDICT: FAIL-NOT-EVALUABLE` (after `RaiseDefect: K1: segment 1 '\\"' is neither a source nor a tier`) | 1 |
| P1-AC2 | p1-refused | `VERDICT: PASS-REFUSED` | 0 |
| P1-AC3 | p1-passed | `VERDICT: PASS-REMOVAL-PASSES` | 0 |
| P1-AC4 | p1-branch | `VERDICT: PASS-EVIDENCE-ON-BRANCH` | 0 |

## 5. Limits

- **Arm 2 grades 0 strings.** The replacement sits inside `key()`, which is a permitted context. The pass means the string
  left the post-image. Arm 1 on the same line is the control that shows the line is graded.
- **The planted row is fictitious**, so the registry at `plant` is REFUSED by `validate`. The limb does not validate, and it
  honoured the row.
- **Nothing live moved.** No AWS read or write, and no Terraform.
