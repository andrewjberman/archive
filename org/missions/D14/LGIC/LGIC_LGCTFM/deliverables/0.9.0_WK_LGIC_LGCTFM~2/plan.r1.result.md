# LT-p-1 round 1 result -- `0.9.0_WK_LGIC_LGCTFM~2` on `LGIC_LGCTFM.TO-LT-p-1-r1`

**Cell:** `LT-p-1`. **Artifacts:** `lib/opal_lgctfm.py` (edited -- the engine's fourth and last round-1
writer, after slot ~1's `LT-e-1`/`LT-e-2`/`LT-e-3`), plus the GRADED RUN's own output
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~2/plan_r1/{contract.json,plan.json,plan.md}`
(`contract.json` is slot ~1's committed `walk/contract.json`, copied byte-for-byte per the WORKER FACE's own
instruction, never re-walked).

## What this cell adds

Two new verbs on `lib/opal_lgctfm.py` (WORKER FACE "TWO VERBS"; decomposition v1.1 s.10: "`LT-p-1` also
carries the `run` verb that assembles a run directory, so `LT-x-1` and `LT-x-3` ... need no further engine
edits"):

- **`plan <run dir>`** (`cmd_plan()`/`build_packages()`, graded this round). Reads `<run dir>/contract.json`,
  builds one ATOM_DECOMP package (`objective`, `dependencies`, `reads`, `writes`, `acceptance_proof`,
  `rollback`, `owner`, `replacement_obligation` -- `PACKAGE_FIELDS`, ATOM_DECOMP SKILL.md "Decompose
  migration") per `(tension, R19 step)`, emitted grouped by step in R19's fixed order `MAP -> CLASSIFY ->
  RULE -> PORT -> REPOINT -> PROVE` (`R19_STEPS`, PRD DEC-8 / `02_DOCTRINE.md` R19), each step's packages in
  the tension list's own already-rank-ordered position (`build_tensions()`, LT-e-3, never re-sorted here).
  Only `PORT` and `REPOINT` (`WRITING_STEPS`) `writes` the row -- every other step reads and reasons, writes
  nothing (DEC-8: "the plan ... signs nothing"; WORKER FACE: "no package is executed; the plan signs
  nothing"). A package whose `writes` names a row whose `current.client_facing` is `True` carries
  `never_widen_signoff_owed: true` and `signoff_owners: ["1.0.0_SA_CTO", "2.0.0_SA_COO"]` (`SIGNOFF_OWNERS`,
  DEC-8: "the package carries `never_widen_signoff_owed: true` and names the owners (CTO and COO, NEVER#1)").
  Writes `plan.json` (`{"executed": false, "packages": [...]}`) and a deterministic `plan.md`
  (`render_plan_md()`) -- no wall clock, no absolute path in either file, so a re-run on a copy is byte-equal
  (p1-regenerates).
- **`run --subject <key> --run-home-subject <dir> --seed <bucket> [...] --root <dir>`** (`cmd_run()`, NOT
  graded by this round's criteria -- decomposition v1.1 s.10 names it as this cell's scope so `LT-x-1`/
  `LT-x-3` need no further engine edits, but no `P1R1-AC*` criterion reads its output). Allocates the run
  directory through `workflows/legacy_transform/run_home.py new` (a `PENDING` `graph_built` placeholder,
  since the true value is only known after the walk; `VINTAGE.json` is patched in place once it is), self-
  invokes this same engine's `walk` verb into that directory (byte-identical to a standalone walk run),
  optionally folds in a `forks` pass via an additive `--seed-loc` flag (`_renumber_forks_rows()` --
  renumbers the forks run's own `R-####`/`F-####` ids past the walk's own maximum, since both runs number
  independently and a bare merge would collide; `contract["tensions"]` is rebuilt from the merged rows via
  the unchanged `build_tensions()`), calls `plan` on the assembled `contract.json`, renders through
  `lib/lgctfm_render.py render`, and refreshes `MANIFEST.md` through `run_home.py manifest`. Writes nothing
  outside the run directory and `MANIFEST.md` (the optional forks pass writes into a `.forks_scratch/`
  subdirectory of the run directory itself, removed once merged).

Both verbs are additive: no existing function (`cmd_walk`, `cmd_forks`, `build_tensions`, `desired_cells`,
etc.) is edited, so `LT-e-1`/`LT-e-2`/`LT-e-3`'s already-drained criteria re-run PASS unchanged (checked
below).

## The graded plan

Per the WORKER FACE: `deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk/contract.json` copied to
`deliverables/0.9.0_WK_LGIC_LGCTFM~2/plan_r1/contract.json`, then `python lib/opal_lgctfm.py plan
.../plan_r1`. **1626 packages** (271 tensions x 6 R19 steps), **executed: false**, every package `status:
PLANNED`. Served-key packages: 4 client-facing rows in the walk contract, 6 packages (PORT+REPOINT across
rows whose `writes` names one of them) carry `never_widen_signoff_owed: true` with both owners.

## Criterion-by-criterion

- **P1R1-AC1** `p1-fields`: 1626 packages, 0 missing any of the eight `PACKAGE_FIELDS`. PASS.
- **P1R1-AC2** `p1-r19`: package `step` sequence non-decreasing under `R19_STEPS` order (all `MAP` first,
  ... all `PROVE` last). PASS.
- **P1R1-AC3** `p1-served`: 4 client-facing rows in the walk contract; 6 packages write one of them; 0
  missing the flag or an owner (`need > 0 and bad == 0`). PASS.
- **P1R1-AC4** `p1-not-executed`: `plan.executed == False`; all 1626 packages `status == "PLANNED"`. PASS.
- **P1R1-AC5** `p1-regenerates`: `plan <copy>` on a fresh temp copy of the committed `contract.json`
  reproduces `plan.json` and `plan.md` byte-for-byte (2 of 2 files). PASS.
- **P1R1-AC6**: judgment, for `3.0.0_SA_CVO` at L9 -- recorded `UNVERIFIABLE-BY-INSTRUMENT` below, no
  self-graded verdict.

## Regression sweep (not this round's own criteria, re-run to confirm no edit-shared-file regression)

`e1-stdlib` (top-level imports: `argparse, hashlib, json, opal_naming, os, re, shlex, shutil, subprocess,
sys, __future__` -- all stdlib or `lib/`), `e1-ascii` (0 non-ASCII of 85791 bytes), `d1-pytest` (2 passed),
`e2-reproduce`, `e2-forks`, `e2-negative`, `e2-raise`, `e3-rule`, `e3-factors`, `e3-order`, `e3-types`,
`e3-untypeable`, `e1-control`, `e1-triggers`, `e1-cells`, `e1-plant`, `e1-method`, `e1-skill`: all PASS,
unchanged from their own drained rounds. `selftest-arms`: 51 of 51 arms discriminate (`p1-fields`/`p1-r19`/
`p1-served`/`p1-not-executed` included), `PASS-ARMS-DISCRIMINATE`.

## Smoke test of the `run` verb (not graded; confidence for the next cell, `LT-x-1`)

`python lib/opal_lgctfm.py run --subject 49financial --run-home-subject smoke-test-lt-p-1 --seed
opal-data-bd --root .scratch/run_smoke` completed rc=0: allocated
`.scratch/run_smoke/smoke-test-lt-p-1/20260917T194050Z-56dbaee/`, wrote `contract.json` (182 rows, 179
tensions), `plan.json`/`plan.md` (1074 packages), `flow.current.md`/`flow.desired.md`, patched
`VINTAGE.json`'s `graph_built` from `PENDING` to the walk's own measured vintage, and refreshed
`MANIFEST.md` (1 run listed). Scratch directory deleted before this report (outside `<paths>`, never
committed -- CLAUDE.md: "Disk on this box is tight").

## Declared exclusions

- **The `forks` merge inside `run`.** `--seed-loc` is additive to the WORKER FACE's own `--seed` list, not
  named there; a bare `--seed <bucket>` cannot supply `forks`' own `bucket:prefix[:mode]` grammar, so a
  `run` invocation using only `--seed` (the WORKER FACE's own shown form) produces a walk-only contract with
  zero `FORK` rows -- a legitimate empty result, never a broken one. Named as a design choice for a verb
  this round's criteria do not grade, not hidden.
- **`P1R1-AC6`** (judgment) -- recorded, not verdicted, per the WORKER FACE's own instruction.

## Commit

Artifact committed on branch `wk-lgic-lgctfm-1-2` before grading (see the commit hash in this deliverable's
proof-of-spec `artifacts_produced[].commit_or_etag`).
