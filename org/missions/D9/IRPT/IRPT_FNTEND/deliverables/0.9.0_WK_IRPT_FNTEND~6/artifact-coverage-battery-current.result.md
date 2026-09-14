# FE-s-44 -- the red artifact-coverage battery, diagnosed (0.9.0_WK_IRPT_FNTEND~6)

Order: `org/missions/D9/IRPT/IRPT_FNTEND/task-orders/IRPT_FNTEND.TO-FE-s-44.artifact-coverage-battery-current.md`.
Worktree `C:/tmp/wk-irpt_fntend-7-6-fe-s-44`, branch `wk-irpt_fntend-7-6-fe-s-44`, base `4d11c008c2`.
The checker's bytes at the base were last changed by `da3e61889d`, and no commit in `8f4106a7f2..4d11c008c2` touches
`.tools/proof-of-spec-check.py`. So the issuer's cut and this base grade with the same checker bytes.

## 1. DIAGNOSIS (written before any fix)

### 1.1 The battery at the base, as committed

`python org/standards/test_artifact_coverage_both_grammars.py` at `4d11c008c2` gave `ARTIFACT-COVERAGE BATTERY: 3/6 PASS (denominator 6)`, rc=1.
This matches the issuer's cut: A, B and E FAIL, and C, D and F "PASS".

### 1.2 The violation lines that refuse A, B and E

I ran the checker on each arm's instance exactly as the battery builds it (`base()` `:39-60`, written by `run()` `:63-69`
into `tempfile.TemporaryDirectory()`, which is the OS temp dir). Each of A, B and E carries exactly ONE violation, and it
is the same violation (`violations=1` in each header):

- **A** (`MDPF-A-AUMMETRICS-01`), rc=1:
  `VIOLATION: artifact-resolution/CHECKER-SCOPE: this proof-of-spec-check lives in C:\tmp\wk-irpt_fntend-7-6-fe-s-44 but the instance is at C:\Users\AndrewBerman\AppData\Local\Temp\tmpudxjsovi\i.json, OUTSIDE that tree -- it cannot resolve the instance's commit and CANNOT GRADE IT. This is NOT a finding against the instance or its author. Run the WORKTREE'S OWN .tools/proof-of-spec-check.py from inside that worktree.`
- **B** (`WP1-1`, the row invokes the artifact), rc=1:
  `VIOLATION: artifact-resolution/CHECKER-SCOPE: this proof-of-spec-check lives in C:\tmp\wk-irpt_fntend-7-6-fe-s-44 but the instance is at C:\Users\AndrewBerman\AppData\Local\Temp\tmp57k0b826\i.json, OUTSIDE that tree -- it cannot resolve the instance's commit and CANNOT GRADE IT. ...`
- **E** (`artifact_covered_by: ["WP1-1"]`), rc=1:
  `VIOLATION: artifact-resolution/CHECKER-SCOPE: this proof-of-spec-check lives in C:\tmp\wk-irpt_fntend-7-6-fe-s-44 but the instance is at C:\Users\AndrewBerman\AppData\Local\Temp\tmpz_w6btbi\i.json, OUTSIDE that tree -- it cannot resolve the instance's commit and CANNOT GRADE IT. ...`

C, D and F each carry TWO violations: their named one, plus the same CHECKER-SCOPE line. So their "PASS" was never
evidence of anything. The same line would have refused them even with the coverage rule gone.

### 1.3 The limb

`artifact_resolution_check`, the CHECKER-SCOPE branch: `.tools/proof-of-spec-check.py:322-342 @4d11c008c2`.
- `:323-325` resolves the instance path relative to `_REPO_ROOT`, which is defined at `:222` as `Path(__file__).resolve().parent.parent`.
- On `ValueError` (the path is outside the tree), `:333-334` record `_foreign_tree`.
- `:335-342` then RETURN the single CHECKER-SCOPE violation before any artifact row is read.

The limb landed in `709b9556a3` (2026-09-10T10:37:30-04:00, `1.0.0_SA_CTO~Z`, on row NFRA_IAMROLES202609-Z-S10). The
battery was written 22 days earlier, in `ba59c67ada` (2026-08-19T19:54:38-04:00, `0.8.0_AE_CloudComp`).
`709b9556a3` is an ancestor of the base.

### 1.4 Discrimination: the limb alone flips A, B and E

The same six instances were run three times, changing one variable each time. The runner is `.scratch/diag2.py`: it
builds `base()` byte-for-byte as committed, keeps the pin `abc1234`, and prints every VIOLATION line.

| checker bytes | instances written to | A | B | E | C | D | F |
|---|---|---|---|---|---|---|---|
| `709b9556a3~1` (the limb absent) | OS temp | rc=0, 0 viol | rc=0, 0 | rc=0, 0 | rc=1, coverage only | rc=1, coverage only | rc=1, dangling-citation only |
| `709b9556a3` (the limb lands) | OS temp | rc=1, SCOPE | rc=1, SCOPE | rc=1, SCOPE | rc=1, coverage + SCOPE | rc=1, coverage + SCOPE | rc=1, dangling + SCOPE |
| `da3e61889d` (the base, unchanged) | inside the worktree (`.scratch/`) | rc=0, 0 viol | rc=0, 0 | rc=0, 0 | rc=1, coverage only | rc=1, coverage only | rc=1, dangling only |

- Row 1 against row 2 isolates the limb. Between them only the checker's bytes change, and the ONLY new violation is CHECKER-SCOPE.
- Row 3 shows that nothing ELSE in the 29+ checker commits since `709b9556a3` refuses these instances. It is the current
  checker, and moving the instance into the tree is the only change.
- FE-s-29's limbs (count-bar, drives, placeholders), FE-s-36's output vocabulary, FE-s-37's binding and the
  alignment/resolution frames all run on these instances and raise nothing: `to_id` `FIXTURE.T` resolves no governing
  order, so every order-bound limb ANNOUNCES.

### 1.5 Which side is wrong, and why

**The battery is the wrong side.** The limb is right for these instances. It refuses a pair it cannot see rather than
grade it, and says so without blaming the instance. Its docstring (`:326-338`) records the prior behaviour: that
behaviour blamed the honest party when the instance lay outside the tree. A checker can resolve an instance's commit
and its (commit, path) pairs only inside the tree it lives in. An OS-temp instance is outside every worktree by
construction, so the refusal is the correct verdict and loosening it would re-open Z-S10.

The battery went stale at `709b9556a3`. It has written its instances into the OS temp dir since `ba59c67ada`, and
from 2026-09-10 on every arm has been refused before the coverage rule was reached. That is why C, D and F kept
"passing": their assertion (`rc != 0 and "artifact-coverage" in out`) is satisfied by ANY refusal that also carries a
coverage line. It never asked whether the coverage line was the only thing refusing.

**Remedy class: the battery only.** `.tools/proof-of-spec-check.py` stays byte-identical. The battery must:
- (a) write its instances inside the tree it grades;
- (b) assert that each control fails on its NAMED violation and nothing else;
- (c) prove, with a scratch mutant, that it can fail on the case it exists for.

A second staleness, not a refusal: the fixture pin `abc1234` does not resolve, so the resolution limb reads the row as
UNRESOLVED-HERE (announced), and the artifact row is never resolved at all. Real committed instances pin a commit that
carries the path. The remedy uses one.
