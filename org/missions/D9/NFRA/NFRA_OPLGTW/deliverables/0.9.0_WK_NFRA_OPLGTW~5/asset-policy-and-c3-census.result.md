# NFRA_OPLGTW.TO-OG-q-5 -- result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` **Branch:** `wk-nfra_oplgtw-5e` **HEAD:** `eeb80016e3`

## HALF ONE (the dim_asset partial-account CUSIP restriction) -- BLOCKED, not repaired

The restriction cannot be wired inside this cell's `<paths>` grant. Traced fully:
`semantics.py`'s `qualify_asset_plan()` (`:330-360`) is already built to implement PRD C3's mechanism
(appends `eng.PolicyFilter("cusip", sorted(position_cusips))`, re-tags position `SourceObject`s
`role="policy"` for budget accounting, raises `ENTITLEMENT_DENIED`/`asset_read_denied_unqualified` when
unqualified) and is unit-tested in isolation (`tests/test_schwab_semantics.py::test_ogq3_ac11/12/13`), but
it has **zero production callers**. The only call site that could supply its `position_sources`/
`position_cusips` arguments -- fetching the qualified position snapshot via the catalog, running a small
engine job filtered to the caller's own granted accounts, then calling `qualify_asset_plan` before the main
`dim_asset` job runs -- is `app/integrations/schwab/integration.py`'s `SchwabService.query()` (and, for
parity, `prepare_download()`/`export_query()`). **That file is not in this task order's `<paths>` grant.**

Filed as BLOCKING surprise row `NFRA_OPLGTW-W5-S13` (full grounding, citations and traced call graph in the
row itself). `OGQ5-AC1`, `AC2`, `AC3` and `AC4` are measured **FAIL** against the real, unwired live path
through the registered `schwab_query` tool on OG-v-2's harness (`tests/test_schwab_asset_policy.py`, this
cell's own deliverable) -- not repaired, not worked around.

`call site by file:line`: `app/integrations/schwab/integration.py:535-536,717-718,790-791` (the
`self._asset_policy is None` gate, never reading the value) and `app/integrations/schwab/semantics.py:330`
(`qualify_asset_plan`, the built-and-uncalled implementation).

## HALF TWO (the C3 census) -- complete, `OGQ5-AC5` PASS

`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/C3_CALL_PATH_CENSUS.md`. Built by
subtraction from C3's own sentence count (34 sentences, PRD v0.9 @`e09219470f`), never from a remembered
list. **29 rules; 20 ENFORCED-ON-CALL-PATH, 5 NOT-ENFORCED, 4 NOT-A-CALL-PATH-RULE; 20+5+4=29.**

Beyond HALF ONE's own row (R28), the census found **four further NOT-ENFORCED rules** -- the same shape
ruling R-OG-17 names (a criterion, already built and unit-tested in `semantics.py`, proven only where
nothing calls it):

- **R20** `assert_grouping_preserves_identity()` -- zero callers; `group_by=["business_date"]` is accepted,
  unrefused (measured directly against the shipped module with the real contract).
- **R22** `assert_single_balance_metric()`/`assert_sum_allowed()` -- zero callers; summing two distinct
  `dim_balance` fields in one aggregate is accepted, unrefused (measured directly).
- **R24** `assert_unique_grain()` -- zero callers, and `engine.py`'s own execution has no grain-uniqueness
  check either; a duplicate/conflicting grain is served or silently folded into a SUM.
- **R25** `describe_field()`/`describe_dataset()` -- zero callers; the live `schwab_describe_dataset` tool
  builds its response from `qry.DATASET_SCHEMAS` directly and never exposes a field's `sign` or
  `null_semantics`, even though `datasets.json` carries both.

Each filed as its own surprise row (`NFRA_OPLGTW-W5-S14` .. `S17`), OBSERVATION class, INERT (nothing is
deployed). Not repaired here, per this cell's own bound: "the census FINDS; it does not FIX."

## Criteria

| id | verdict | measured |
|---|---|---|
| OGQ5-AC1 | FAIL | live tool returns all 4 CUSIPs, wants 2 |
| OGQ5-AC2 | FAIL | ungranted-account CUSIP present under both narrow and wide grant |
| OGQ5-AC3 | FAIL | zero-holding grant still served, `is_error=False` |
| OGQ5-AC4 | FAIL | no call site exists to remove; mutant cannot discriminate |
| OGQ5-AC5 | **PASS** | census denominators printed and consistent (34/29/20/5/4) |
| OGQ5-AC6 | FAIL | acceptance module carries 2 failures (`test_ogv2_a06` -- this cell's own arm; `test_ogv2_a18` -- not this cell's, per issuer context) |

## Proof of spec

`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/NFRA_OPLGTW.TO-OG-q-5.asset-policy-and-c3-census.proof_of_spec.json`,
validated with `.tools/proof-of-spec-check.py`. **The task order's `<status>` stays `pending`**: five of six
mechanical criteria FAIL by measured output; a VALID proof-of-spec instance is not a met order.
