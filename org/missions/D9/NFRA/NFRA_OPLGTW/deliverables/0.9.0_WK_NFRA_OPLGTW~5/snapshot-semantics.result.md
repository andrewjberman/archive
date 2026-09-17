# NFRA_OPLGTW.TO-OG-q-3.snapshot-semantics -- session log

Worker `0.9.0_WK_NFRA_OPLGTW~5`, worktree `C:/tmp/wk-oplgtw-5e` (branch `wk-nfra_oplgtw-5e`), cut from
`CLOUD @4c179f1826`.

## What was built

- `infra/aws/ec2/opal-gateway/app/integrations/schwab/datasets.json` -- dataset field descriptions (grain,
  type, unit, sign, null semantics, source citation) for `dim_position`/`dim_balance`/`dim_asset`, plus
  `additive_fields` and `quantity_sum_required_groups`, cross-checked at import against
  `query.py`'s own `DATASET_SCHEMAS`/`DATASET_GRAINS` (`semantics._validate_datasets`, refuses loudly on
  any drift between the two files).
- `infra/aws/ec2/opal-gateway/app/integrations/schwab/semantics.py` -- the semantic validation layer above
  `query.py`'s closed grammar: grouping/identity (AC1), same-date sums and cross-date deltas via
  `SnapshotValue`/`sum_snapshot_values`/`snapshot_delta` (AC2, AC4), separate per-master results (AC3),
  which sums are meaningful (`assert_field_summable`/`assert_quantity_sum_grouped`/
  `assert_single_balance_metric`/`assert_sum_allowed`, AC5-AC8), duplicate/conflicting grain refusal
  (`assert_unique_grain`, AC9), dataset descriptions (`describe_field`/`describe_dataset`, AC10), the
  partial-account asset qualification (`qualify_asset_plan`, AC11-AC13), and a small closed metric catalog
  (`resolve_metric`, AC14).
- `infra/aws/ec2/opal-gateway/tests/test_schwab_semantics.py` -- one test per criterion, `test_ogq3_ac01`
  through `test_ogq3_ac14`, run against the real `engine._plan_job`/`ExecutionEngine` code path (synthetic
  Parquet fixtures written in-test; no Schwab object read; `query.py`/`engine.py` left untouched).

## query.py/engine.py

Read, per the order, and left byte-for-byte unmodified (`git status --porcelain` on both paths is empty at
every check in this session). `semantics.py` imports both as read-only dependencies (`query.DATASET_SCHEMAS`,
`query.DATASET_GRAINS`, `query.exposed_name`, `engine.QueryPlan`/`PolicyFilter`/`SourceObject`/
`ExecutionEngine`), never re-implementing what they already validate.

## Runs

- `py -3.12 -m venv --system-site-packages .venv-og` at `<WS>` (the venv did not exist for this worker; the
  worktree-root location matches the order's `cd <WS> && ... -m venv ... .venv-og` literally -- an earlier
  attempt inside `infra/aws/ec2/opal-gateway/.venv-og` was recreated at the correct root once the
  criterion's own `cd <WS> && .venv-og/Scripts/python ...` invocation showed the mismatch).
- `.venv-og/Scripts/python -m pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest`
  -- installed clean (two pre-existing, unrelated system-site version notices: awscli/botocore,
  mitmproxy/typing-extensions; neither package this order touches).
- Each of the 14 criteria run individually (`pytest ... ::test_ogq3_ac<nn> -q -p no:cacheprovider
  --color=no`), twice (once mid-build, once at the committed bytes) -- identical `1 passed` both times, see
  `proof_of_spec.json`.
- Full new file, `pytest infra/aws/ec2/opal-gateway/tests/test_schwab_semantics.py -q ...`: `14 passed in
  1.71s` / `2.17s` across runs (both clean).
- Regression check (not a criterion; the order's own read list): the pre-existing
  `tests/test_schwab_query.py` (OG-q-2's 24 tests) still passes in full, `24 passed in 10.99s` --
  `semantics.py`/`datasets.json` are additive and touch no shared module.
- `bash .tools/commit-gate.sh` on the two `.py` files: `OK: pre-commit gate clean for 2 of 2 file(s)`
  (mid-build) and again with `datasets.json` alongside: `OK: pre-commit gate clean for 2 of 3 file(s)`
  (the JSON file is outside the gate's `.py` scope, per Rule 14; both `.py` files clean both times).

## Mutant control

Single-edit mutant in `semantics.py`: `assert_single_balance_metric`'s refusal condition changed from
`if len(distinct) > 1:` to `if False and len(distinct) > 1:` (disarming AC6's refusal). Expected:
`test_ogq3_ac06` fails (`DID NOT RAISE SemanticError`). Observed: `1 failed in 1.19s`,
`Failed: DID NOT RAISE <class 'app.integrations.schwab.semantics.SemanticError'>` -- FIRED AS EXPECTED.
Restored verbatim; `sha256sum` before mutation and after restoration both
`198691744b790f4650cfc6360730a1475e0d468aca1b2bee10efddbe837d9019`; the full 14-test file re-passed after
restoration (`14 passed in 2.17s`).

## Declared exclusions / epistemic notes

- The `sign` values recorded in `datasets.json` as `signed_measured` for `dim_balance` fields other than
  `mkt_value_long` (i.e. `mkt_value_short`, `net_mv_positions`, `net_mv_plus_cash`,
  `cash_balance_settled_only`) are business-logic inference plus this pass's own synthetic fixtures, not an
  independently confirmed live-vendor sign convention -- the order's own bound is synthetic fixtures only,
  no Schwab object read, so no stronger claim is possible in this pass. `dim_position.market_value_settled_
  unsettled`'s `signed_measured` IS corroborated by an existing fixture already in the merged codebase
  (`test_schwab_query.py`'s `POSITIONS`, row A2/CCC000003, `-30.3000`), cited in `datasets.json`.
- The "cash/AUA total" refusal (AC6) is implemented as: at most one distinct `dim_balance` additive field
  may be summed per request (`assert_single_balance_metric`). `query.py`'s own closed aggregate grammar
  already forbids an expression that adds two columns in one aggregate; this is the one remaining shape
  that could let a caller approximate a combined total (two single-field sums returned in one response,
  added back together outside the Gateway), and it is refused here.

## No surprises filed

Every named criterion was met as written; no premise failed, no named path was elsewhere, no invocation
failed to produce its named result, and no capability named in the order was missing. `query.py`/`engine.py`
were read exactly as directed and required no edit.
