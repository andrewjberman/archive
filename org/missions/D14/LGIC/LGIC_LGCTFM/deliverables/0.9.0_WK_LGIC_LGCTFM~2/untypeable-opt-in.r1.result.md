# LT-e-4-r1 result -- the untypeable plant becomes opt-in (R-36)

**Worker:** `0.9.0_WK_LGIC_LGCTFM~2` on `LGIC_LGCTFM.TO-LT-e-4-r1`. **Branch:** `wk-lgic-lgctfm-1-2c`
@`a5fca30175`. **PRD** @`459b4a736d`. **Decomp** v1.2 @`60aac06844`, round-1 amendment cell `LT-e-4`.

## What changed, and why (measured, not re-derived here -- see the WORKER FACE for the full chain)

`org/standards/LGCTFM_CONTRACT.schema.json`'s `$defs.node_type.enum` (33 values) equals
`NAMING_SCHEMA.json`'s graded types by subtraction (`LT-s-1`'s own invariant). `LT-e-3`'s untypeable
plant (a `COGNITO_USER_POOL` row) fired UNCONDITIONALLY in `cmd_walk()`, so every contract this
engine wrote failed schema validation on that one row -- all of `LT-x-1`'s `X1R1-AC1` FAIL, filed as
`LGIC_LGCTFM-W2-S2`. R-36 keeps the enum equality (it is what lets the contract say a type is
ungraded at all) and moves the plant behind a new `--plant-untypeable` flag, OFF by default, on both
the `walk` and `run` verbs.

`lib/opal_lgctfm.py` `cmd_walk()`:
- The third plant block is now guarded by `if getattr(args, "plant_untypeable", False):`.
- When it fires, the node is collected into `untypeable_entries` (a list) instead of being appended
  to `rows`. Each entry carries `name`, `node_type`, `verdict: "NOT_COVERED"`, `why` (the raise's own
  text), `desired` (the full `desired_cells()` output) and `cells` (the row's own current-half
  cells, kept for anyone who wants the full planted-row shape without it being a row).
- `PLANT_UNTYPEABLE.json` is now `{"untypeable": untypeable_entries, "count": len(untypeable_entries)}`
  -- empty list + count 0 when the flag is absent.
- `contract.json` gains a required top-level `untypeable` cell:
  `cell(len(untypeable_entries), "MEASURED", <instrument>, <branch-specific blind_spot>)`, printed
  even at zero.
- `cmd_run()` and `main()`'s two new `--plant-untypeable` argparse flags thread the same boolean
  through the `run` verb's self-invoked `walk` call.

## The two real runs (AMENDMENT_RUNS.json)

- `default_off`: `workflows/legacy_transform/blackdiamond-49financial/20260917T233115Z-a89fd61/` --
  `python lib/opal_lgctfm.py run --subject 49financial --run-home-subject blackdiamond-49financial
  --seed opal-data-bd --seed opal-data-49financial --root workflows/legacy_transform`. 184 rows, 0
  `COGNITO_USER_POOL` rows, `untypeable` cell value 0, carrier empty, contract validates 0 errors.
- `flag_on`: `workflows/legacy_transform/blackdiamond-49financial/20260917T233143Z-a89fd61/` -- same
  invocation plus `--plant-untypeable`. 184 rows (still none untypeable -- the node is carried, not
  rowed), `untypeable` cell value 1, carrier holds 1 entry verdict `NOT_COVERED`, contract validates 0
  errors.

## Completing LT-x-1's own run directory (E4R1-AC6)

`workflows/legacy_transform/blackdiamond-49financial/20260917T202556Z-bb29248/` (LT-x-1's first real
run) was missing `contract.json` and `plan.json` on disk -- `.tools/naming-gate.py` refused them
before R-35 landed (per that cell's own `first-run-and-mark.r1.result.md`: "REFUSED `contract.json`,
`plan.json`, `PLANT.json`, `PLANT_UNTYPEABLE.json` and `MARK.json` wholesale"). This worktree, freshly
branched from `CLOUD`, never had those files on disk at all (they lived only in the old worktree's
untracked state). Backfilled here: `walk --subject 49financial --seed opal-data-bd --seed
opal-data-49financial --out <that dir>` (default, flag off) then `plan <that dir>` -- writes
`contract.json` (184 rows, `untypeable` = 0, 0 schema errors) and `plan.json`/`plan.md` (1074
packages, regenerated to match the new contract). `flow.current.md`, `flow.desired.md`,
`VINTAGE.json` and `FWD10.json` (LT-x-1's own artifacts) were not touched. `MARK.json` remains absent
-- out of this cell's scope (`x1-marks` is not one of this order's criteria); the issuer re-opens and
re-grades `LT-x-1` at this cell's drain.

## Criteria, all re-run post-commit (see the proof_of_spec.json `acceptance[]` for full output)

- **E4R1-AC1 (a4-plant-off): PASS.** 0 of 184 rows carry an ungraded node_type; carrier empty; count 0.
- **E4R1-AC2 (a4-flag-on): PASS.** 1 carried entry, NOT_COVERED, absent from rows, count 1 == carrier count 1.
- **E4R1-AC3 (a4-count-typed): PASS.** `untypeable` is a cell: `{value: 0, status: MEASURED, evidence: {instrument, blind_spot}}`.
- **E4R1-AC4 (a4-schema-valid): PASS.** Both named runs validate against `LGCTFM_CONTRACT.schema.json`, 0 errors.
- **E4R1-AC5 (a4-e3-exercised): PASS.** The flag-on carrier's 1 entry reads NOT_COVERED, 0 leaked into rows.
- **E4R1-AC6 (x1-run-dir): PASS.** `runs[0]` (LT-x-1's own run) carries 0 of 6 RUN_FILES missing, 0 schema errors.
- **E4R1-AC7 (e1-stdlib): PASS.** 11 top-level imports, 0 outside stdlib/`lib/`.
- **E4R1-AC8 (d1-pytest): PASS.** 2 passed (negative arm first).
- **E4R1-AC9:** judgment, for `3.0.0_SA_CVO`, no verdict from this worker.

## Controls

**Self-test cross-check:** `check_lt_r1.py`'s own `_selftest_a4()` GREEN/RED fixtures (read, never
edited) assert the exact defect shapes the two real runs must avoid (an ungraded row leaking into
`rows`, a non-zero count beside an empty carrier, a bare-integer count, a count disagreeing with the
entry list, a non-`NOT_COVERED` verdict) -- our two real runs' shapes match the GREEN fixtures'
structure field-for-field.

**Determinism:** all eight mechanical criteria re-run pre-commit and post-commit against the same
committed state; byte-identical VERDICT/denominator lines both times except `x1-run-dir`'s own "runs
under the subject" count (1 -> 3, purely because the two AMENDMENT runs were added in between -- the
graded `runs[0]` and its verdict were unchanged). `d1-pytest` is itself the engine's own determinism
suite (two hash seeds, negative arm first).

## Declared exclusions

- `LGIC_LGCTFM.TO-LT-x-1-r1.md` / `LGIC_LGCTFM.TO-LT-e-3-r1.md` and rows `LGIC_LGCTFM-W2-S1`/`-S2`:
  read-only context, never edited (LT-x-1's run *directory*, not its order file, was completed).
- `org/standards/LGCTFM_CONTRACT.schema.json`, `PLANTED_CONTRACT.json`, `check_lt_r1.py`: fixed
  inputs, read-only, already carrying the required pieces before this cell started.
- `NAMING_SCHEMA.json`'s `$defs.node_type`: untouched per R-36 (the invariant this cell preserves).
- E4R1-AC9: judgment, recorded not verdicted.
