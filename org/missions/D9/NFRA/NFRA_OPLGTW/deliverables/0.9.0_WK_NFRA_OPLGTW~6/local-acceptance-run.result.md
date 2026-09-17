# NFRA_OPLGTW.TO-OG-v-2 -- local integrated acceptance run: result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~6` | **Worktree:** `C:/tmp/wk-oplgtw-6f` (branch `wk-nfra_oplgtw-6f`, cut @3207f5ea09)
**Proof:** `NFRA_OPLGTW.TO-OG-v-2.local-acceptance-run.proof_of_spec.json` (this folder) -- validated
`py -3.12 .tools/proof-of-spec-check.py <instance> OGV2-AC1,OGV2-AC2,OGV2-AC3,OGV2-AC4,OGV2-AC5` -> `VALID (rc=0)`.
**Order `<status>`: left `pending`** -- OGV2-AC2 FAILS by output (a real defect in the code under test, not in this
harness or fixture); BOUNDS: "Flip `complete` only when every MECHANICAL criterion PASSES by output."

## The harness (two disclosed seams; conftest.py's own module docstring is authoritative)

`infra/aws/ec2/opal-gateway/tests/acceptance/conftest.py` builds the REAL `app.server` Starlette app in
process (Starlette `TestClient`), against:
- moto `mock_aws()` -- one instance shared for the module: DynamoDB (`gateway-access-state-table`), S3
  (`opal-data-assets`, versioning ON, OG-v-1's `fixtures/MANIFEST.json` uploaded in its own stated order
  and every marker restamped to the bucket's real VersionIds via `make_fixtures.restamp`), STS and IAM
  (the two Schwab roles created so `sts:AssumeRole` has a target).
- `ENABLED_INTEGRATIONS=schwab` set before `app.server`'s first import (the integration registers once, at
  that import).
- the upstream identity provider: `tests/test_principal_cutover.py`'s `LocalEntra` (imported, not copied).
- **Seam 1 -- the query-engine process boundary.** `app/integrations/schwab/engine.py`'s real
  `ExecutionEngine` spawns a child process per job; a 120-second budget across many A-row queries cannot
  afford a Windows `spawn` re-import per query. `conftest.InProcessEngine` runs OG-q-1's own
  `validate_plan` / `ExecutionEngine.check_sources` / `_plan_job` synchronously in this process instead --
  the SAME substitution `tests/test_schwab_query.py` (OGQ2) and `tests/test_schwab_export.py` (OGX1) already
  made for this same project, for the same reason. Everything else in the query path (the real
  `app/integrations/schwab/catalog.py` Catalog, `app/integrations/schwab/aws_roles.py` AssumedRole against
  real moto STS, `app/data_entitlement.py`, `app/account_ref.py`, `app/integrations/schwab/envelope.py`,
  `app/schwab_audit.py`) is unmocked.
- **Seam 2 -- the account-reference key.** `app/account_ref.py`'s real key comes from Secrets Manager;
  this harness hands `SchwabService` a fixed literal `Keyring` instead (the same substitution the two
  peer test files above already make). The HMAC mint/resolve code itself is the real module.
- **Seam 3 (found during this run, not anticipated) -- `asset_policy`.** `SchwabService`'s `asset_policy`
  constructor argument gates every `dim_asset` request on mere presence (`is None`); grepping the whole
  repo shows NO caller anywhere -- production wiring or any existing test -- ever passes one. A non-`None`
  sentinel (`object()`) is this harness's only way to reach `dim_asset` at all; disclosed in
  `conftest.py`'s `build_service()`.

## Criteria

| id | invocation (relative to `<WS>`) | result |
|---|---|---|
| OGV2-AC1 | `pytest .../test_local_acceptance.py::test_ogv2_ac01` | **PASS** -- `1 passed` |
| OGV2-AC2 | `pytest .../test_local_acceptance.py -k "test_ogv2_a"` | **FAIL** -- `1 failed, 6 passed` (see below) |
| OGV2-AC3 | `pytest .../test_local_acceptance.py::test_ogv2_ac03` | **PASS** -- `1 passed` |
| OGV2-AC4 | per-module loop over `tests/test_*.py` (21 modules) | **PASS** -- `MODULES: 21 FAILED-MODULES: 0` |
| OGV2-AC5 | `pytest .../test_local_acceptance.py::test_ogv2_ac05` | **PASS** -- `1 passed`, 56 S3 calls, 0 violations |

### OGV2-AC2 -- the A-row census

**Denominator: 6 of 13** OG-v-1 census rows marked `operated_by: machine` whose instrument is `OG-v-2` are
built as tests here (A2 is `OGV2-AC3`, counted separately by this order's own text; the other five --
A4, A5, A8, A11 -- are `test_ogv2_a04/a05/a08/a11`). **7 of 13 are not built**: A3, A6, A9, A10, A12, A14,
A17, A18 (row `NFRA_OPLGTW-W6-S7`, filed as a surprise, not silently dropped).

Of the 6 built:

| row | test | result | compared against |
|---|---|---|---|
| A4 | `test_ogv2_a04` | PASS | discovery hides ungranted Schwab tools; direct `tools/call` denied, 0 new S3 calls |
| A5 | `test_ogv2_a05` | PASS | `expected/EXPECTED.json` `A5-shared-account-two-masters` (distinct aliases, cross-master refusal, no raw id in any response) |
| A8 | `test_ogv2_a08` | **FAIL** (partial) | `A8-balance-field-totals`, `A8-position-quantity-by-cusip-ls`, `A8-position-market-value-total`, `A8-date-deltas`: **all four match `expected/EXPECTED.json` exactly.** `A8-refusals`: **2 of 5 listed refusals exercised, 0 of 2 pass** -- see row `NFRA_OPLGTW-W6-S6` below. |
| A11 | `test_ogv2_a11` | PASS | a raw silver key as `catalog_id` refuses (`INVALID_REQUEST`); no S3 presigned-URL pattern in the response |
| A2 (machine) | `test_ogv2_ac03` | PASS | a legacy refresh token -> `invalid_grant`; a fresh loopback client's refresh survives a new `TestClient` on the same durable store |

### The real defect this run found (`NFRA_OPLGTW-W6-S6`, filed to the surprise channel, ARMED, disarm_owner `1.0.0_SA_CTO`)

`schwab_query` in aggregate mode does **not** refuse either request `A8-refusals` names:
- `SUM(closing_price)` on `dim_asset` (closing_price is NOT in the contract's `additive_fields` -- price is
  nonadditive) -- the live app answers 200 with a computed sum instead of `INVALID_REQUEST`.
- `SUM(quantity_settled_unsettled)` on `dim_position` with no `group_by cusip, l_s` (the contract's
  `quantity_sum_required_groups`) -- the live app answers 200 with a single ungrouped total instead of
  `INVALID_REQUEST`.

Root cause (grading only -- **not fixed**; `app/integrations/schwab/query.py` and `integration.py` are
outside this order's `<paths>` grant): `app/integrations/schwab/semantics.py` declares
`assert_field_summable` / `assert_quantity_sum_grouped` / `assert_single_balance_metric` (composed in
`assert_sum_allowed`), and they are correct and tested in isolation
(`tests/test_schwab_semantics.py`), but neither `query.py`'s `check_against_grant` nor
`integration.py`'s `SchwabService.query` ever imports or calls them. This is why OGV2-AC2 is graded
**FAIL** here rather than silently passed: the independent fixture (`expect_independent.py`, never
re-derived from the code under test) is exactly what caught it.

## Surprise rows filed this order

- `NFRA_OPLGTW-W6-S6` -- the semantics-wiring gap above. OBSERVATION, **ARMED**, disarm_owner `1.0.0_SA_CTO`.
- `NFRA_OPLGTW-W6-S7` -- the reduced OGV2-AC2 row coverage (6 of 13 built). OBSERVATION, INERT.

## Mutant / determinism controls

See `controls` in the proof-of-spec instance: a single-edit mutant on `test_ogv2_ac01`'s own assertion
fired as expected and the file was restored byte-identical (sha256
`75ce95163b592c42f3bc326be11eb1fbd0efc907764ad13590a5f83611fcb1e5` before and after); OGV2-AC1/AC3/AC5 are
stable across repeated standalone runs, and OGV2-AC2 fails the same one test every time across three runs
this session.
