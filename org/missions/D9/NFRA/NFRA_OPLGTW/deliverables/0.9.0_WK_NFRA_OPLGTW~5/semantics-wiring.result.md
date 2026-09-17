# NFRA_OPLGTW.TO-OG-q-4.semantics-wiring -- session log

Worker `0.9.0_WK_NFRA_OPLGTW~5`, worktree `C:/tmp/wk-oplgtw-5e` (branch `wk-nfra_oplgtw-5e`), fast-forwarded
to `CLOUD @6a4df76f02`.

## Call site

`infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py:check_against_grant` -- every one of
`integration.py`'s three `qry.check_against_grant(...)` call sites (`query`, the export-ticket path, and a
third read path) already funnel through this one function, so wiring the checks there covers all three
without touching `integration.py`. Inside the aggregates loop, right after the existing
`aggregate_function_type` check, `check_against_grant` now calls (local import, avoiding the
`query.py` <-> `semantics.py` circular-import-at-load hazard both directions were measured against):

```python
if agg.function == "sum":
    try:
        sem.assert_field_summable(query.dataset, agg.field)
        sem.assert_quantity_sum_grouped(query.dataset, agg.field, query.group_by)
    except sem.SemanticError as exc:
        raise QueryError(exc.code, exc.reason, where + ".field") from None
```

`semantics.SemanticError` is translated to `query.QueryError` at the call site itself, so
`integration.py`'s existing `except qry.QueryError as err:` handler in `_run` (already present, unedited)
reports the contract error code/reason/where without any change to `integration.py`.

`semantics.py` and `datasets.json` are OG-q-3's and are byte-for-byte unchanged this session
(`git status --porcelain` on both paths empty throughout).

## Tests built

`infra/aws/ec2/opal-gateway/tests/test_schwab_wiring.py` -- `test_ogq4_ac01/02/03`, each driving the real
`schwab_query` tool through OG-v-2's own acceptance harness (`tests/acceptance/conftest.py`'s `og_v2` /
`served_app` / `moto_world` fixtures, real `app.server`, real Starlette `TestClient`, moto S3/DynamoDB/STS,
the harness's two disclosed seams unchanged). This file lives one level above `tests/acceptance/`, so
pytest's ancestor-conftest walk never reaches `tests/acceptance/conftest.py` on its own, and a plain
`import conftest` would silently bind to `tests/conftest.py` (already cached in `sys.modules["conftest"]`
by pytest's own ancestor-conftest load) instead. Both `tests/` and `tests/acceptance/` are added to
`sys.path` and the acceptance conftest is imported as the namespace-package module `acceptance.conftest`
(no `__init__.py` in either directory -- PEP 420 implicit namespace package), which lands under its own
distinct `sys.modules` key and sidesteps the collision; measured directly (`.scratch/.scratch_import_test.py`,
not committed) before writing the tests.

- `test_ogq4_ac01`: `sum(dim_asset.closing_price)` (nonadditive; `datasets.json` additive_fields.dim_asset
  is `[]`) -> `INVALID_REQUEST`.
- `test_ogq4_ac02`: `sum(dim_position.quantity_settled_unsettled)` with no `group_by` -> `INVALID_REQUEST`
  (`quantity_sum_ungrouped`).
- `test_ogq4_ac03`: `sum(dim_balance.mkt_value_long)` (additive, no grouping requirement) -> succeeds,
  total in the envelope.

## Runs

- `test_ogq4_ac01/02/03` each run individually twice (initial build, then a final confirmation pass after
  the probe and surprise row were added): identical `1 passed` both times -- see `proof_of_spec.json`.
- `bash .tools/commit-gate.sh` on `query.py`, `test_schwab_wiring.py` and the probe: `OK: pre-commit gate
  clean for 3 of 3 file(s)`.

## Mutant control (OGQ4-AC4)

The probe (`probes/og_q4.py AC4`) copies the whole `infra/aws/ec2/opal-gateway` tree into
`.scratch/og_q4_mutant_<ts>/opal-gateway`, then overwrites the copy's `query.py` with
`git show HEAD:infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py` -- HEAD is this cell's own
starting point (before the wiring above), so this removes exactly the two call sites and nothing else
(`semantics.py`, `datasets.json` and every other file in the copy are the current worktree's bytes). Runs
`test_ogq4_ac01/02/03` against that copy as three separate subprocesses.

The copy's `catalog.default_contract_path()` derives the contract path from `Path(__file__).parents[7]`,
which is correct at the real repo's fixed depth but wrong once the tree is re-parented under
`.scratch/<name>/opal-gateway/...` (three fewer directory levels than `infra/aws/ec2/`) -- a path-depth fact
about the scratch location, not a call-site change -- so the mutant subprocess runs with
`NFRA_OPLGTW_CONTRACT_PATH` set to the real, unmutated contract file's absolute path (the loader's own
documented override).

Observed: mutant `test_ogq4_ac01` -> `1 failed in 4.47s`; mutant `test_ogq4_ac02` -> `1 failed in 4.14s`;
mutant `test_ogq4_ac03` -> `1 passed in 8.66s` -- FIRED AS EXPECTED (AC1/AC2 fail, AC3 still passes).
`git status --porcelain` before and after the whole AC4 run: identical, 6 lines, same content -- the probe
never wrote a tracked file. `VERDICT: PASS-OGQ4-AC4`.

## Surrounding-module regression (OGQ4-AC5) -- FAIL, measured

`probes/og_q4.py AC5` runs `test_schwab_query.py`, `test_schwab_semantics.py` and `test_schwab_export.py`,
one pytest process per module, against the real (unmutated) worktree:

- `test_schwab_semantics.py` -> `14 passed in 1.08s`
- `test_schwab_export.py` -> `27 passed in 8.20s`
- `test_schwab_query.py` -> `2 failed, 23 passed in 7.41s`

`test_schwab_query.py::test_ogq2_ac07` (its own "control" case, `:491-497`) and `::test_ogq2_ac15`
(`:743-750`) each sum `quantity_settled` (a quantity field per `datasets.json`'s `quantity_fields.dim_position`)
with no `group_by`, and assert success -- both were written and merged before any caller enforced the
contract's quantity-grouping rule (C3), so they encode exactly the shape this cell's own OGQ4-AC2 requires
to be refused. Wiring the call site correctly therefore breaks them. `test_schwab_query.py` is not in this
order's `<paths>` grant (only `query.py`, `integration.py`, `test_schwab_wiring.py` and the surprise-channel
file are), and OG-q-2's cell is merged and closed, so this worker does not edit it (never widen the order or
fix a neighbouring defect; a path not granted is a BLOCKING surprise row, never an override).

Filed as surprise row `NFRA_OPLGTW-W5-S10` (class `BLOCKING`, `hazard_standing: INERT`) in
`org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md`. `VERDICT:
FAIL-OGQ4-AC5 2 of 3 module(s) passed` -- reported as measured, not repaired or routed around. This order's
`<status>` therefore stays `pending`; `proof_of_spec.json`'s OGQ4-AC5 row is `status: FAIL` with
`status_reason` naming the row.

## Gates run

- `.tools/commit-gate.sh` -- `query.py`, `test_schwab_wiring.py`, `probes/og_q4.py`: clean, 3 of 3.
- `.tools/surprise-row-gate.py` (staged) -- `1 new row(s) of 94 total checked ... all new rows carry their
  step-7/step-10 fields`, rc=0.
- `.tools/proof-of-spec-check.py` -- see the WORKER REPORT for its exact invocation and rc; per the order's
  own text, a FAIL row on a mechanical criterion means the checker's overall rc is non-zero and the order's
  `<status>` is NOT flipped to `complete`.
