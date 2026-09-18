# NFRA_OPLGTW.TO-OG-q-5 -- result (re-hand round, closed)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` **Branch:** `wk-nfra_oplgtw-5e` **Base HEAD (wiring round):** `35377638d7`
**Closing re-measurement HEAD:** `1ca5067f6e2f08e8e0d225e1cdddaa7ee7f87ec3` (fast-forwarded to CLOUD)

## Closing round (this pass) -- AC1..AC6 re-run fresh at ONE vintage, `<status>` flipped `complete`

Neither by this worker: `test_ogv2_a06` and `test_ogv2_a18` were fixed in `OG-v-2`'s last re-hand (drained
`@dcad7a92f1` and `@1ca5067f6e`); `test_ogq2_ac06`/`ac20` (rows W5-S19/W5-S20, both already resolved before
this pass) ride this cell's own `OG-q-6` re-open drain `@e58d9d2b04`. Re-running all six criteria at this
worker's current HEAD (`1ca5067f6e`, fully committed -- `git status --porcelain` shows only untracked
`.scratch/`/`.venv-og/`) measures **all six PASS**:

- `OGQ5-AC1` -- `1 passed` (unchanged).
- `OGQ5-AC2` -- `1 passed` (unchanged).
- `OGQ5-AC3` -- `1 passed` (unchanged).
- `OGQ5-AC4` -- `VERDICT: PASS-OGQ5-AC4`, mutant still discriminates, porcelain unchanged (unchanged).
- `OGQ5-AC5` -- `VERDICT: PASS-OGQ5-AC5`, census re-read not rebuilt, same denominators 34/29/20/5/4 (unchanged).
- `OGQ5-AC6` -- **now PASS** (was FAIL in the prior round): `test_schwab_query.py` 25 passed,
  `test_schwab_semantics.py` 14 passed, `test_schwab_wiring.py` 3 passed,
  `tests/acceptance/test_local_acceptance.py` **14 passed, 0 failed** -- both `test_ogv2_a06` and
  `test_ogv2_a18` are green at this HEAD. All four modules carry 0 failures; denominator 4 printed.

Proof-of-spec instance rebuilt for all six ids; `py -3.12 .tools/proof-of-spec-check.py <instance>
OGQ5-AC1,OGQ5-AC2,OGQ5-AC3,OGQ5-AC4,OGQ5-AC5,OGQ5-AC6` -> `VALID (rc=0)`. Every mechanical criterion PASSES
by output, so `<status>` is flipped `complete` in this pass. No new surprise row filed this pass (the prior
round's rows W5-S13..W5-S18 stand unchanged; W5-S18's own disposition is the CTO's to move, not touched
here).

## Prior round (wiring), unchanged below

## HALF ONE (the dim_asset partial-account CUSIP restriction) -- WIRED this round

The re-hand granted `app/integrations/schwab/integration.py` for HALF ONE's one call site
(`SchwabService.query()`), fixing the issuer's own `<paths>` gap named by row `NFRA_OPLGTW-W5-S13`.

Wiring: inside `query()`'s cache-miss branch, when `q.dataset == sem.ASSET_DATASET`, the code now (1)
fetches a qualified `dim_position` snapshot for the same master/date, reusing the SAME authorized `check`
already built for the dim_asset request itself (the grant may carry no separate `dim_position`
authorization at all -- exactly the AC1 fixture's shape: `datasets=("dim_asset",)`); (2) runs a small
internal engine job (`mode="rows"`, `PolicyFilter(ACCOUNT_SOURCE, scope.accounts[master])`, projecting
`cusip`) to resolve `position_cusips`; (3) calls `semantics.qualify_asset_plan(plan, position_sources,
position_cusips)`, which appends the CUSIP `PolicyFilter` to the dim_asset plan and re-tags the position
source objects `role="policy"` for the same object/byte/deadline accounting; (4) runs the qualified plan
with both source sets. Nothing else in `integration.py` changed; `prepare_download()`/`export_query()`'s
own `dim_asset` gates are untouched (not this order's named call site).

`OGQ5-AC1`, `AC2` and `AC3` now measure **PASS** through the registered `schwab_query` tool on OG-v-2's
live-app harness. `OGQ5-AC4`'s mutant control now genuinely fires (neuters the wiring branch in a scratch
copy; AC1/AC2/AC3 all FAIL there; tracked files unchanged) -- **PASS**.

## HALF TWO (the C3 census) -- unchanged, re-measured at this HEAD

`C3_CALL_PATH_CENSUS.md` not rebuilt (per this order's own re-hand instruction). `OGQ5-AC5` re-run once at
this HEAD: **PASS**, same denominators as the prior drain (34 sentences / 29 rules / 20 ENFORCED / 5
NOT-ENFORCED / 4 NOT-A-CALL-PATH-RULE, 20+5+4=29). Rows `NFRA_OPLGTW-W5-S14`..`S17` (the four further
NOT-ENFORCED C3 rules the census found beyond HALF ONE) are unchanged this round.

## OGQ5-AC6 -- measured FAIL, and why it is not "only test_ogv2_a18"

`test_schwab_query.py` (25 passed), `test_schwab_semantics.py` (14 passed) and `test_schwab_wiring.py` (3
passed) are clean. `tests/acceptance/test_local_acceptance.py` carries **2** failures, not 1:

- `test_ogv2_a18` -- issuer-disclaimed (row `NFRA_OPLGTW-S26`, rides `OG-v-2`'s own re-hand); unrelated to
  HALF ONE (`quantity_sum_ungrouped` on a `dim_position` aggregate).
- `test_ogv2_a06` -- **this cell's own arm.** Its dim_asset partial-account CUSIP assertion (`:477`) now
  measurably **PASSES** (`'OGV2-AC2/A6/partial-grant-asset-cusips: got ['SYN000001', 'SYN000002'],
  EXPECTED ['SYN000001', 'SYN000002'] (MATCH)'`), confirming HALF ONE's wiring on a SECOND, independent
  harness beyond this cell's own dedicated test file. But that same test's LAST assertion (`:488`, a
  post-revocation guard-denial response-shape check) was previously **masked** by the `:477` failure
  (Python's assert-stops-at-first-failure) and is now exposed: a revoked principal's `schwab_query` denial
  arrives as `app/data_entitlement.py`'s raw `guard_denied` dict with the MCP `isError` flag left falsy
  (traced to `app/tools.py`'s `_PolicyGuardedMCP.call_tool()`, which returns that dict directly rather than
  wrapping it in a `CallToolResult(isError=True, ...)` the way `SchwabIntegration._call()`'s own
  `_admit()`/`_denied()` does). This is a genuine defect this cell's fix **exposed, not caused**, in files
  (`app/tools.py`, `app/data_entitlement.py`) neither in this cell's `<paths>` nor this cell's task. Filed
  as surprise row `NFRA_OPLGTW-W5-S18` (OBSERVATION, ARMED, disarm_owner `1.0.0_SA_CTO`), not repaired.

Per the order's own hand-off text ("if it is the only failure ... report that measurement plainly"): it is
**not** the only failure, so this is reported as the measured `FAIL-OGQ5-AC6` it is, not silently narrowed.

## Criteria

| id | verdict | measured |
|---|---|---|
| OGQ5-AC1 | **PASS** | live tool returns exactly the granted account's 2 CUSIPs |
| OGQ5-AC2 | **PASS** | ungranted-account CUSIP absent under the narrow grant, present under the wide grant |
| OGQ5-AC3 | **PASS** | zero-holding grant denied, `ENTITLEMENT_DENIED`/`asset_read_denied_unqualified` |
| OGQ5-AC4 | **PASS** | mutant discriminates (AC1/AC2/AC3 all FAIL on the neutered copy); tracked files unchanged |
| OGQ5-AC5 | **PASS** | census denominators printed and consistent (34/29/20/5/4), re-run not rebuilt |
| OGQ5-AC6 | FAIL | acceptance module carries 2 failures: `test_ogv2_a06` (newly-exposed, unrelated `:488` defect -- row S18) and `test_ogv2_a18` (issuer-disclaimed, row S26) |

## Proof of spec

`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/NFRA_OPLGTW.TO-OG-q-5.asset-policy-and-c3-census.proof_of_spec.json`,
validated with `.tools/proof-of-spec-check.py`. **The task order's `<status>` stays `pending`**: one of six
mechanical criteria (`OGQ5-AC6`) FAILS by measured output; a VALID proof-of-spec instance is not a met
order.
