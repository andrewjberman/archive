# NFRA_OPLGTW.TO-OG-v-2 -- local integrated acceptance run: result (RE-HAND)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~6` | **Worktree:** `C:/tmp/wk-oplgtw-6f` (branch `wk-nfra_oplgtw-6f`, HEAD @5eb4945331)
**Proof:** `NFRA_OPLGTW.TO-OG-v-2.local-acceptance-run.proof_of_spec.json` (this folder) -- validate with
`py -3.12 .tools/proof-of-spec-check.py <instance> OGV2-AC1,OGV2-AC2,OGV2-AC3,OGV2-AC4,OGV2-AC5`.
**Order `<status>`: left `pending`** -- OGV2-AC2 FAILS by output (two real defects in the code under test, not
in this harness or fixture); BOUNDS: "Flip `complete` only when every MECHANICAL criterion PASSES by output."

## What this re-hand did

1. **Re-keyed `conftest.py`'s `READER_ARN`/`CATALOG_ARN`** (and the moto IAM role names) from
   `org/standards/NFRA_OPLGTW_CONTRACT.json`'s `reader_role`/`catalog_role`, instead of the two hardcoded
   pre-rename literals OG-i-3's R-OG-7 left behind (`gateway-schwab-read-role` /
   `gateway-schwab-catalog-read-role`, matching `tests/test_schwab_catalog.py`'s own `ROLE_ENV` read of the
   same contract, for the same reason). This alone took the harness from `5 failed, 2 passed` back to green
   on the previously-existing 7 tests.
2. **Built the 7 machine-and-local A-rows the prior round left unbuilt** (row `NFRA_OPLGTW-W6-S7`'s own
   denominator): `test_ogv2_a03`, `a06`, `a09`, `a10`, `a12`, `a17`, `a18`.
3. **Re-graded OGV2-AC2** with the full, now-whole denominator.

## The harness (three disclosed seams; `conftest.py`'s own module docstring is authoritative)

Unchanged from the prior round except item 1 above: the REAL `app.server` Starlette app in process, moto
`mock_aws()` (S3 versioned/DynamoDB/STS/IAM), `ENABLED_INTEGRATIONS=schwab`, `LocalEntra` upstream issuer
(imported from `tests/test_principal_cutover.py`), OG-v-1's fixture MANIFEST uploaded and restamped. Seam 1
(in-process query engine), seam 2 (fixed account-reference `Keyring`) and seam 3 (`asset_policy` sentinel,
found last round) are all still exactly as documented there.

## Criteria

| id | invocation (relative to `<WS>`) | result |
|---|---|---|
| OGV2-AC1 | `pytest .../test_local_acceptance.py::test_ogv2_ac01` | **PASS** -- `1 passed` |
| OGV2-AC2 | `pytest .../test_local_acceptance.py -k "test_ogv2_a"` | **FAIL** -- `2 failed, 12 passed` (see below) |
| OGV2-AC3 | `pytest .../test_local_acceptance.py::test_ogv2_ac03` | **PASS** -- `1 passed` |
| OGV2-AC4 | per-module loop over `tests/test_*.py` (21 modules) | **PASS** (recorded run) -- `MODULES: 21 FAILED-MODULES: 0`; see the flakiness note below |
| OGV2-AC5 | `pytest .../test_local_acceptance.py::test_ogv2_ac05` | **PASS** -- `1 passed`, 56 S3 calls, 0 violations |

### OGV2-AC2 -- the A-row census, denominator now whole

**Denominator: 12 of 12** OG-v-1 census rows marked `operated_by: machine` whose instrument is `OG-v-2` are
built as tests (A2 is `OGV2-AC3`, counted separately by this order's own text). **A14 is correctly out of
scope**: its machine half is graded_by BOTH `OG-v-2` AND `OG-r-2` (concurrent-job memory/latency, a host
measurement `OG-v-2` alone cannot make) -- listed here, not silently dropped, per the WORKER FACE's own
routing rule.

| row | test | result | compared against |
|---|---|---|---|
| A2 (machine) | `test_ogv2_ac03` | PASS | legacy refresh -> `invalid_grant`; fresh loopback refresh survives a restart |
| A3 | `test_ogv2_a03` | PASS | unknown/revoked/null-tid/null-oid principals denied and hidden from discovery; forged headers change nothing; same email + different oid denied |
| A4 | `test_ogv2_a04` | PASS | discovery hides ungranted tools; direct call denied, 0 new S3 calls |
| A5 | `test_ogv2_a05` | PASS | `A5-shared-account-two-masters` (distinct aliases, cross-master refusal, no raw id) |
| A6 | `test_ogv2_a06` | **FAIL** (partial) | `A6-account-grant-before-aggregate` (narrow grant after a broader-grant warm): **matches EXPECTED exactly**. 4 hidden-field refusals + the SQL-injection-shaped-value case + post-revocation refusal: **all pass**. `A6-partial-grant-asset-cusips`: **FAILS** -- see `NFRA_OPLGTW-W6-S8` below. |
| A8 | `test_ogv2_a08` | **FAIL** (partial) | balance totals, position quantity-by-cusip-ls, market-value totals, date deltas: **all four match exactly**. `A8-refusals`: **FAILS** -- see `NFRA_OPLGTW-W6-S6` (carried, unchanged this round). |
| A9 | `test_ogv2_a09` | PASS | all 12 closure variants + 2 anchor dates, under a FIXED grant naming every date, behave per `A9-closure-variants` |
| A10 | `test_ogv2_a10` | PASS | ticket mint -> exchange once (200) -> replay refused -> cross-principal refused -> owner still redeems -> post-revocation refused; ticket only in the URL fragment. (Reduced: no fake-clock hook for the 300s expiry sub-case; no log-scan instrument -- declared exclusions.) |
| A11 | `test_ogv2_a11` | PASS | raw silver key refused; no presigned-URL pattern |
| A12 | `test_ogv2_a12` | PASS | prompt-like text returned verbatim, grant revision unchanged; CSV formula-escaping matches `A12-csv-formula-escaping` exactly (6 escaped cells, 1 unescaped negative numeric, correct row count) |
| A17 | `test_ogv2_a17` | PASS | reuse revokes the family (successor also dead); wrong client_id/resource/broader-scope each rejected; survives a restart. (Reduced: a true two-thread race not separately built -- declared exclusion.) |
| A18 | `test_ogv2_a18` | PASS | Unicode codepoint/UTF-8/JSON-escape counts match exactly; rows paging (page_size 2) covers the match with no repeat; paged (page_size 1) and un-paged aggregate group totals agree; empty match -> 0 rows, null sum |

### The two real defects OGV2-AC2 finds (both ARMED, disarm_owner `1.0.0_SA_CTO`, neither fixed here)

**`NFRA_OPLGTW-W6-S6` (carried from the prior round, re-confirmed at this HEAD -- see note below):**
`schwab_query` aggregate mode does not refuse `SUM(closing_price)` (nonadditive) or an ungrouped
`SUM(quantity_settled_unsettled)`, because `semantics.py`'s `assert_sum_allowed` family is never called
from `query.py`/`integration.py`. **Re-grounded this round:** the issuer's hand-off said OG-q-4 had wired
this in ("now genuinely enforced on the live path") -- at this worker's own HEAD (`5eb4945331`), that wiring
commit (`80fba29f34`/`881b1a5445`) is **not an ancestor**: `git merge-base --is-ancestor 80fba29f34 HEAD`
answers false, and it lives on a sibling worker's branch `wk-nfra_oplgtw-5e`, unmerged. The gap is exactly
as `NFRA_OPLGTW-W6-S6` already described; this is a premise check, not a new finding, and no new row is
filed for it.

**`NFRA_OPLGTW-W6-S8` (new this round):** a partial-account grant on `dim_asset` (accounts = `{99000002}`)
returns all four fixture CUSIPs instead of the two that account holds. `integration.py`'s `asset_policy`
constructor argument gates `dim_asset` on mere presence (`is None`); its VALUE is never read anywhere, and
no CUSIP-restriction/qualified-position-snapshot code exists on the `dim_asset` path at all -- the same
class of gap as `S6`, one level over. `query.py`/`integration.py` are outside this order's `<paths>` grant.

### OGV2-AC4's flakiness (`NFRA_OPLGTW-W6-S9`, new this round, INERT)

The per-module loop was run three times this session: `FAILED-MODULES:1` (`test_schwab_engine.py`'s
`test_ogq1_ac02`, a hardcoded 0.25s event-loop-lag threshold, measured 0.446s under box load -- a standalone
re-run passed clean), `FAILED-MODULES:1` (`test_schwab_export.py`'s `test_ogx1_ac01`, asserting `'s3'`/
`'amazonaws'`/`'?'` are absent from a `secrets.token_urlsafe(32)` ticket -- a rare, pure-chance substring
collision), then `FAILED-MODULES:0` (clean). Neither failing test imports `conftest.py` or
`test_local_acceptance.py`. **The third (clean) run is the one recorded** in the proof instance; the
flakiness itself is disclosed so a future FAIL on this literal invocation is not misread as an OG-v-2
regression.

## Surprise rows filed this order

- `NFRA_OPLGTW-W6-S8` -- the `dim_asset` partial-account CUSIP-restriction gap. OBSERVATION, **ARMED**,
  disarm_owner `1.0.0_SA_CTO`.
- `NFRA_OPLGTW-W6-S9` -- OGV2-AC4's non-determinism on two unrelated pre-existing flaky modules.
  OBSERVATION, INERT.
- (Carried, not re-filed: `NFRA_OPLGTW-W6-S6`, `NFRA_OPLGTW-S24`/`NFRA_OPLGTW-W5-S11` -- the pre-rename ARN
  defect this round's conftest.py fix disarms; `NFRA_OPLGTW-W6-S7` -- this round's denominator now closes it.)

## Mutant / determinism controls

See `controls` in the proof-of-spec instance: the single-edit mutant on `test_ogv2_ac01` (carried from the
prior round, file unchanged at that point) still fires and restores byte-identical
(sha256 `75ce95163b592c42f3bc326be11eb1fbd0efc907764ad13590a5f83611fcb1e5`). This round's independent-fixture
control: `test_ogv2_a06` and `test_ogv2_a08` each assert several `EXPECTED` cases per test body and each
fails on exactly one real-gap sub-case while passing every other sub-case in the same body against the same
`EXPECTED.json` -- the harness discriminates both ways on the same run.
