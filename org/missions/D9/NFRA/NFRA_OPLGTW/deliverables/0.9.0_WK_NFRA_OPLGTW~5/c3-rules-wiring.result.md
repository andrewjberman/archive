# NFRA_OPLGTW.TO-OG-q-6 -- result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` **Branch:** `wk-nfra_oplgtw-5e` **Cut HEAD:** `a96788f138`

## The four rules, by call site

Two call sites, not one, because R25 reaches through a different tool than R20/R22/R24:

- **`app/integrations/schwab/query.py` `check_against_grant()`** (query.py:438-506) -- the same site
  OG-q-4 (R-OG-13) and OG-q-5 already extend:
  - **R20**: `sem.assert_grouping_preserves_identity(query.group_by)`, called once at the top of the
    function on the raw `group_by` tuple, independent of the grant (a request-shape rule).
  - **R22 (negative half)**: after the aggregate loop, `summed_fields` collects every `agg.field` of every
    `sum` aggregate across the WHOLE request, then `sem.assert_single_balance_metric(query.dataset,
    summed_fields)` runs once -- catching two distinct `dim_balance` fields summed in TWO SEPARATE
    aggregate entries, not only two fields inside one aggregate expression (query.py's own grammar already
    forbids the latter).
- **`app/integrations/schwab/integration.py`** -- unreachable from query.py because each needs state
  query.py's validation stage never has:
  - **R24**: `SchwabService.query()`, after the job returns rows, for a "rows"-mode request whose own
    requested columns already carry every one of the dataset's grain fields (the shape in which grain
    identity is OBSERVABLE from this call's own output without a second engine query):
    `sem.assert_unique_grain(q.dataset, grain_rows)`. Scoped this way and disclosed as such in the code
    comment -- an aggregate-mode request, or a rows-mode request that omits a grain column, is NOT covered
    by this wiring.
  - **R25**: `SchwabService.describe_dataset()`, per visible field: `sem.describe_field(d, name)` supplies
    `sign`/`null_semantics`, added beside the pre-existing `name`/`type`/`unit`/`grain` the tool already
    served.

`semantics.py` and `datasets.json` are untouched (git status clean on both throughout).

## AC1..AC4 -- new test file, live-app harness

`infra/aws/ec2/opal-gateway/tests/test_schwab_c3_rules.py` (new, this cell's `<paths>`), following
`test_schwab_asset_policy.py`'s own importlib pattern to reach `tests/acceptance/conftest.py`'s `og_v2`
fixture. R24's fixture is OG-v-1's own pre-built `duplicate_grain` variant
(`make_fixtures.VARIANT_DATES["duplicate_grain"]` = 2026-07-07, M_SMARTX), read through `dim_balance` (the
dataset with the simplest grain, `(account_ref,)`) rather than through `dim_position`/`dim_asset` (other
cells' datasets). All four PASS, individually and together in one process.

## AC5 -- the one mutant, and why it removes TWO call sites, not one

The ruling's "one call site" is this cell's own diff, not a single textual line: `og_q6.py AC5` extracts
`infra/aws/ec2/opal-gateway` from `git archive HEAD` (this worktree's uncommitted wiring is therefore
absent by construction -- exactly the state the original census measured NOT-ENFORCED for all four rules),
copies in this cell's own untracked test file, and runs AC1..AC4 against that mutant. **All four FAIL**
there (verified: `wiring_absent=True`, all four outcomes FAIL, `git status --porcelain` before/after
identical). The one-cell premise holds for this wiring.

## AC6 -- fresh re-derivation, never inherited

`og_q6.py AC6` re-splits C3 from the PRD at HEAD (byte-identical to the cited pin `e09219470f`, verified by
`git diff --quiet`) into sentences FRESH this run: **34 sentences**, same paragraph shape (7+7+7+8+5) as the
first census but RE-COUNTED, not copied. Exclusions (2 descriptive + 1 "Thus..." consequence) and the P5
fold (3 sentences -> 1 row) are re-identified by matching the same sentence text the original census
named, not assumed present: **3 excluded, 2 folded, rule count = 34 - 3 - 2 = 29**, matching the earlier
vintage because the PRD is unchanged, not because the number was carried forward. The five functions the
original census measured at zero production callers (`assert_grouping_preserves_identity`,
`assert_single_balance_metric`, `assert_unique_grain`, `describe_field`, `qualify_asset_plan`) are
independently re-measured by this probe's own regex scan (a different instrument than the original
census's `comp-find` run): each now shows exactly 1 caller outside `semantics.py`. **NOT-ENFORCED = 0.**
No rule newly appears in C3 since the pin (PRD content identical). `VERDICT: PASS-OGQ6-AC6`.

## Informational regression run, and two new surprise rows

AC6's own text asks for the census re-read only, not a regression-suite run (unlike OG-q-5's differently
worded AC6) -- but the probe runs one anyway as due diligence on a production change. Six modules re-run,
one pytest process each: `test_schwab_semantics.py`, `test_schwab_wiring.py`, `test_schwab_asset_policy.py`
and this cell's own `test_schwab_c3_rules.py` are clean. Two modules carry failures, both **disclosed, not
fixed, not gating any of this cell's own criteria**:

- `tests/acceptance/test_local_acceptance.py` -- `test_ogv2_a18` (row `NFRA_OPLGTW-S26`) and
  `test_ogv2_a06`'s `isError` arm (row `NFRA_OPLGTW-W5-S18`) -- both OTHER cells' pre-existing, disclaimed
  defects per this order's own BOUNDS text, unaffected by this cell's edits.
- `tests/test_schwab_query.py` -- **two NEW failures this cell's own correct wiring causes**, in a file
  explicitly outside this cell's `<paths>` ("A needed change there is a BLOCKING row"):
  - `test_ogq2_ac06` -- its "at_limit" `group_fields` case groups by `ALL_POSITION[:10]`
    (`dim_position`'s contract-field order), and `business_date` sits at index 1 -- always inside the
    10-field "should succeed" arm. R20 now correctly refuses it.
  - `test_ogq2_ac20` -- its one-page duplicate-grain case asserts SUCCESS once `page_size` is large enough
    to avoid pagination. R24 requires UNAVAILABLE regardless of page size; C3's text names no page-size
    exception.

  Filed as `NFRA_OPLGTW-W5-S19` and `NFRA_OPLGTW-W5-S20` (OBSERVATION, ARMED, disarm_owner
  `2.0.0_SA_COO~O`) -- real, committed test-suite regressions, not dormant-feature latent risk like this
  cell's other C3 rows, but genuinely unfixable inside this cell's grant.

## Criteria

| id | verdict | measured |
|---|---|---|
| OGQ6-AC1 | **PASS** | `group_by=["business_date"]` refused, `INVALID_REQUEST`/`group_removes_date_identity` |
| OGQ6-AC2 | **PASS** | two distinct `dim_balance` SUMs refused (`combined_balance_total_refused`); one named field's SUM still succeeds |
| OGQ6-AC3 | **PASS** | duplicate-grain date refused `UNAVAILABLE`/`duplicate_source_grain`; control date (3 rows) succeeds |
| OGQ6-AC4 | **PASS** | all 9 `dim_balance` fields carry `sign` and `null_semantics`, denominator printed |
| OGQ6-AC5 | **PASS** | mutant (HEAD, pre-wiring) fails all four; porcelain unchanged |
| OGQ6-AC6 | **PASS** | fresh 34/29/0-NOT-ENFORCED re-derivation; regression finding informational, filed as surprises |

## Proof of spec

`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/NFRA_OPLGTW.TO-OG-q-6.c3-rules-wiring.proof_of_spec.json`,
validated with `.tools/proof-of-spec-check.py`. All six mechanical criteria PASS by measured output; the
task order's `<status>` flips to `complete`.
