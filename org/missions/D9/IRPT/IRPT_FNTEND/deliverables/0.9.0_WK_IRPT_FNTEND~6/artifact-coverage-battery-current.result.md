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

## 2. THE REMEDY -- the battery only (`051379eac7`)

`org/standards/test_artifact_coverage_both_grammars.py`:
- **In-tree instances.** `run()` writes each instance under `<tree>/.scratch/aco_inst_*/`, inside the tree whose
  checker grades it.
- **Named-violation controls.** `judge()`:
  - A PASS arm needs rc=0, zero VIOLATION lines, and a header of `violations=0`.
  - A CONTROL needs rc=1 and at least one named line; every VIOLATION line must start with its named text, and the
    header count must equal the named lines.
  - The named texts are the uncovered artifact for C and D, and the dangling `['WP9-9']` citation for F.
  - Each control prints the lines it matched, tagged `named` or `OTHER`.
- **A real pin.** The artifact row pins the commit that last touched `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`
  (`4707880967`). It is derived with `git log` and checked with `git cat-file -e`, and the battery exits 2 loud if no
  commit carries the path.
- **Real shape, checked by the battery on every run.** The comparison instance is
  `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/IRPT_BCKEND.TO-IB-rt-7.the-holdings-handler-and-the-attribution-holdouts.proof_of_spec.json`,
  read as the committed blob at `b9a3fcc335` (RULING AC). It is BUILD-GENERAL / FABRIC / OTHER; its gold script row
  is `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py @d9c940244a`, and its PASS rows use method
  `command` and carry `expect`.
  - The fixture's keys: 13 of 13 top-level, 6 of 6 artifact-row and 8 of 8 acceptance-row keys are carried by the real
    instance.
  - Its vocabulary: 7 of 7 fields carry only values the real instance carries.
  - The one real key the fixture omits is `decomp_ref`. That is deliberate: `to_id` `FIXTURE.T` resolves no governing
    order, so every order-bound limb announces and the six arms isolate the instance-intrinsic rules.
- **Real exemplars for each route**, from a census of all 373 committed instances (624 script/s3 artifacts):
  - naming route: 12, all id-prefix coincidences. The closest to arm A is
    `NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement`, where token `CCY` of `build_ccy_proof.py` appears in `L3S7B-CCY-AC1`.
  - row-reference route (arm B's): 459.
  - `artifact_covered_by` route (arm E's): 148, IB-rt-7 among them.
  - exclusion-item route: 5.
  - uncovered: 0.
- **The mutant runs every time.** The checker's bytes are copied to `<tree>/.scratch/aco_mutant_*.py`, one level under
  the tree, because the checker derives its tree as `parent.parent`. The per-artifact coverage loop is replaced by
  `for a in []`, at exactly 1 site. All six arms run on the copy, and the copy is unlinked in a `finally`. The line
  reads `yes` only if all three controls go red AND all three positive arms stay green.
- **Exit.** rc 0 only on 6/6, controls 3 of 3, mutant yes and shape yes.

`.tools/proof-of-spec-check.py` is **byte-identical**: blob `7e324c78c2a6cdd92739b341286a77d740b05869` at the base,
at HEAD and in the working copy, and `git diff --stat 4d11c008c2 HEAD -- .tools/proof-of-spec-check.py` is empty.

## 3. RESULTS (run as written, on committed bytes `051379eac7`)

| criterion | deciding line | denominator |
|---|---|---|
| F44-AC1 | `ARTIFACT-COVERAGE BATTERY: 6/6 PASS (denominator 6)`, rc=0 | 6 of 6 arms |
| F44-AC2 | `CONTROLS FAIL FOR THEIR NAMED VIOLATION: 3 of 3`, rc=0 | 3 of 3 controls, 1 named violation each, 0 other |
| F44-AC3 | `WITH THE COVERAGE RULE DISABLED IN A SCRATCH COPY, THE CONTROLS CATCH IT: yes`, rc=0 | 3 of 3 controls red, 3 of 3 positives green, 1 of 1 site; copy removed |
| F44-AC4 | `RESULT: 42 of 42 arm(s) behaved`, rc=0 | 42 of 42 (unchanged; checker untouched, no arm owed) |
| F44-AC5 | `EVERY .tools BATTERY THAT CALLS EITHER TOOL: 12 of 12 green`; `governing-binding battery: 19 of 19 arm(s) as expected (277 s wall)`, rc=0 | 12 of 12 batteries (census domain: 63 .py under .tools/tests/, 13 name either tool, 12 run) |
| F44-AC6 | `[to-pipeline-gate --self-test] RESULT: 0 arm(s) failed of 72`, rc=0 | 72 of 72 |
| F44-AC7 | judgment, recorded for 3.0.0_SA_CVO at L9 | 3 heads |

## 4. CONTROLS

- **The mutant (in-battery, every run)**: `mutant: 3 of 3 controls go red; 3 of 3 positive arms stay green`. The
  copy is removed, which is re-read after the unlink.
- **The defect's own coordinate (negative control, by hand)**: a scratch copy of the NEW battery with `SCRATCH` set to
  the OS temp dir reads `ARTIFACT-COVERAGE BATTERY: 0/6 PASS`, `CONTROLS FAIL FOR THEIR NAMED VIOLATION: 0 of 3`, and
  mutant `no`, rc=1. Each control lists `violation (OTHER): artifact-resolution/CHECKER-SCOPE`. The old battery
  counted exactly this state as 3 control passes. The copy was removed.
- **Determinism**: two runs, one on the working copy before commit and one deciding run on committed bytes. Both
  produced identical verdicts and violation lines.

## 5. ROWS

- **IRPT_FNTEND-W6-S1** (OBSERVATION, INERT), appended to `INVESTIGATION_v2.md`. At the base, the census of record
  read `11 of 12 green`: `test_seeded_limb.py` hit the census's own 560 s per-battery bound (rc=124) while the box was
  shared. Alone on `051379eac7` the same battery ran in 275 s and the census read `12 of 12`, with neither tool
  changed. The census's row shape does not separate load from regression.
- Not re-filed: the gap in the census domain (`org/standards/` lies outside `.tools/tests/`). That is W4-S15 / C-S90,
  the row this cell answers.

## 6. NAMED WEAKNESSES

- The fixture shares the real instance's FIELD SHAPE and VOCABULARY, not its governing order. That is deliberate: a
  resolving `to_id` would bring the alignment, invocation and drives limbs in, and the arms would stop isolating the
  coverage rule.
- The mutant disables the whole per-artifact loop. A narrower mutant, such as dropping only the `:208` exclusion-item
  precision, is not exercised as its own arm. Arm D is the arm that would catch the regression to the old blob match.
- The pin is derived, not frozen. If `dim_mdpf_aum_metrics.py` were ever deleted, `git log -1` would name the deletion
  commit, and the battery exits 2 loud rather than grading.
