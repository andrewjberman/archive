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

## AMENDMENT (R-OG-15, second hand-off) -- OGQ4-AC6/AC7 built, AC1-AC4 newly BLOCKED

Re-handed after the issuer merged `CLOUD` into this branch to deliver the R-OG-15 amendment. HEAD at the
start of this hand-off is `2392d6f9fb`, a merge commit whose two parents are `881b1a5445` (this seat's own
prior work above) and `d91629cfd8` (the `CLOUD` tip the issuer merged in).

### Cut base for AC6/AC7

`_CUT_BASE = d91629cfd8e7693c65ac3b06d945fa584be44adf` in `probes/og_q4.py`, i.e. `merge-base(HEAD, CLOUD)`
at this hand-off's starting HEAD -- which is `d91629cfd8` itself, since it is a direct parent of the merge
commit. It is PINNED to that literal hash rather than re-derived from `git merge-base HEAD CLOUD` at probe
run time: `CLOUD` is a shared branch that can move on independently of this worktree, and the question
AC6/AC7 ask ("what did this hand-off change against the file it started from") is about that ONE historical
merge, not whatever `CLOUD` happens to point to whenever the probe next runs. Verified `git show --stat
d91629cfd8` touches exactly one path (the task order's own `.md`), so `test_schwab_query.py` at that pin is
the original, pre-correction OG-q-2 file -- confirmed by running the two named tests against it before any
edit (`2 failed, 23 passed`, both failures on `quantity_sum_ungrouped` where the file's own code expected
success).

### R-OG-15 correction (OGQ4-AC6, AC7)

`test_ogq2_ac07` (`:470-516`) -- its final "control" case summed `quantity_settled` (a quantity field) with
no `group_by` and asserted success; flipped to `err(...)` expecting `INVALID_REQUEST`/`quantity_sum_ungrouped`,
with a comment citing PRD C3 verbatim (`NFRA_OPLGTW_PRD.md@f0aa50dbc0:161-163`, "Quantity sums require
grouping by CUSIP and long/short indicator").

`test_ogq2_ac15` (`:739-767`) -- its "killed" case summed `quantity_settled` ungrouped to reach the engine
and be cut off at `engine.fail`'s simulated deadline (`LIMIT_EXCEEDED`/`aggregate_scan_incomplete`); flipped
to expect `INVALID_REQUEST`/`quantity_sum_ungrouped` instead, with the same PRD C3 citation, noting the
`world.engine.fail` deadline it used to exercise is now never reached (the semantic check runs before
`build_plan`/any object read).

`probes/og_q4.py AC6` diffs `test_schwab_query.py` against the pinned cut base (`git diff -U0`), computes
each of `test_ogq2_ac07`'s and `test_ogq2_ac15`'s own `[start,end]` line range independently (via a
`^def name(` scan, never trusting the diff's own function-context trailer alone), and checks every changed
hunk's old and new ranges fall entirely inside one of those two ranges: 3 of 3 hunks do. `AC7` runs
`--collect-only` on the corrected file (25 tests) and, for the "before" count, copies the whole gateway tree
to `.scratch/` and swaps in the cut-base's `test_schwab_query.py` bytes only (same technique as AC4's mutant),
runs `--collect-only` there too (25 tests, with `NFRA_OPLGTW_CONTRACT_PATH` set for the scratch depth), and
checks both corrected functions' source text contains the PRD C3 citation verbatim (initially FAILED on
`test_ogq2_ac15` because the quoted phrase was wrapped across two comment lines by this worker's own
formatting; rewritten onto one line and re-verified). Both PASS: `VERDICT: PASS-OGQ4-AC6`,
`VERDICT: PASS-OGQ4-AC7`.

### NEW surprise: AC1/AC2/AC3/AC4 now FAIL (row `NFRA_OPLGTW-W5-S11`, BLOCKING)

Re-running the unchanged `test_ogq4_ac01/02/03` (no edit to `query.py`, `integration.py` or
`test_schwab_wiring.py` this round) now FAILs all three: every one returns `UNAVAILABLE`/
`schwab_integration_unavailable` instead of the expected refusal/success. Traced to
`tests/acceptance/conftest.py:88-91` (`READER_ARN`/`CATALOG_ARN`, NOT in this order's `<paths>` grant):
these hardcode the PRE-rename role names (`opal-mcp-emp-menachem-schwab-read` /
`opal-mcp-schwab-catalog-read`), while `org/standards/NFRA_OPLGTW_CONTRACT.json`'s `reader_role`/
`catalog_role` were renamed to `gateway-schwab-read-role`/`gateway-schwab-catalog-read-role` by commit
`b2e4a10678` (R-OG-7, `NFRA_OPLGTW.TO-OG-i-3`) -- landed on this branch via the issuer's `CLOUD` merge
(`881b1a5445..d91629cfd8` contains exactly that one commit touching the contract; the same range for
`tests/acceptance/conftest.py` is empty). `app/integrations/schwab/aws_roles.py:116-135`'s
`role_config()` (unchanged code, verified by diff) now refuses the fixture's own ARN at construction
(`RoleConfigError`, reproduced directly by calling `aws_roles.role_configs` with the fixture's exact env);
`app/integrations/schwab/integration.py:917-920` swallows this as a bare `Exception` and returns the
generic `UNAVAILABLE`/`schwab_integration_unavailable` every failing test measures. `AC4`'s mutant control
was ALSO rewritten this round (its old `git show HEAD:query.py` pin now returns the WIRED bytes, since
881b1a5445 committed the wiring -- see `_pre_wiring_query_bytes` in `probes/og_q4.py`, which walks
`query.py`'s own history to a content-verified pre-wiring commit, `c3728d6b...`); with that fix the mutant
correctly makes AC1/AC2 FAIL, but AC3 also FAILs against the mutant copy (which carries the same stale
`conftest.py`), so `VERDICT: FAIL-OGQ4-AC4`.

Filed as surprise row `NFRA_OPLGTW-W5-S11` (class `BLOCKING`, `hazard_standing: INERT`) in
`INVESTIGATION_v1.md`. `tests/acceptance/conftest.py` is not in this order's `<paths>` grant (OG-v-2's
harness, not this cell's), so it is not edited here -- reported FAIL by measurement on all four criteria,
never patched around.

### This round's net proof state

AC1 FAIL, AC2 FAIL, AC3 FAIL, AC4 FAIL (all four blocked by `NFRA_OPLGTW-W5-S11`, a harness fixture defect
outside this order's grant, introduced by the issuer's `CLOUD` merge and not by this cell's own wiring);
AC5 PASS (25+14+27, R-OG-15's correction now makes the module clean); AC6 PASS; AC7 PASS. `<status>` stays
`pending`; `proof_of_spec.json` rebuilt for all 7 ids with these results.
