# EN-aa-1 result -- the three required registries fail closed (0.9.0_WK_LGIC_ENFORCE~1, round 21)

Code commit: fb9c09bb28 (LOCAL on wk-LGIC_ENFORCE-1). Criteria run from the worktree root against the committed bytes.

## What changed (lib/opal_lgctfm.py, lib/tests/test_opal_lgctfm.py)

- `MissingInput` exception; `read_text()` and `read_json()` raise `MissingInput("MISSING INPUT <repo-relative path>")` when the
  file is absent AND is one of `SCOPES_REGISTRY`, `REMEDIATIONS_REGISTRY`, `LEGACY_SERVED_PATHS`. Every other read keeps
  returning `""` / `None`.
- `require_registries()` checks the three files; `main()` calls it for `walk`, `forks` and `run` (every verb that reads them)
  before any discovery, prints the `MISSING INPUT` line and returns 3, creating no output directory, contract or row.
  `plan` reads only a run directory's `contract.json` (it opens none of the three), so it is not gated.
- Three test arms (`test_missing_input_scopes_json`, `..._remediations_json`, `..._legacy_served_paths_json`): present ->
  read unchanged and `require_registries()` silent; absent -> both readers and `require_registries()` raise with the exact message;
  an optional read still returns `""` / `None`.

## Criteria

- AA1R21-AC1 (`check_en_r21.py failclosed`):
  `sparse: rc=3 last='MISSING INPUT org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json'`
  `full: rc=0 last='WALK: wrote 198 row(s) (incl. 2 planted) and 135 tension(s), untypeable carried=0 to <tmp>'`
  last line `PASS-R21-FAILCLOSED`, rc 0.
- AA1R21-AC2 (`check_en_r21.py unit`): `unit: rc=0 7 passed in 2.14s`, last line `PASS-R21-UNIT`, rc 0.

## Bar

`python -m pytest lib/tests -q -p no:cacheprovider`: 196 passed, 1 skipped (base 193 + 3 new arms). `.tools/naming-gate.py
--self-test`: `NAMING-GATE-SELF-TEST: PASS`.
