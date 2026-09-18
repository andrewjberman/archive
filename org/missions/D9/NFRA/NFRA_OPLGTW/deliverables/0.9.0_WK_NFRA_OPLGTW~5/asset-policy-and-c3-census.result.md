# NFRA_OPLGTW.TO-OG-q-5 -- result (re-hand round)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` **Branch:** `wk-nfra_oplgtw-5e` **Base HEAD:** `35377638d7`

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
