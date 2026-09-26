# NFRA_MCPINDEX.TO-MX-t-8 -- the portal tools: result

`0.9.0_WK_NFRA_MCPINDEX~3`, branch `wk-NFRA_MCPINDEX-3`, build commit `bc0cde67f0`. Module:
`infra/aws/ec2/opal-gateway/app/integrations/portal_index/integration.py`. Tests:
`infra/aws/ec2/opal-gateway/tests/test_portal_index.py`.

This supersedes the earlier text of this file, which described a ten-tool module kept outside the tree.

## The three tools (order item 13)

Row `-Z-W3-S11`, disarmed by the issuer's seat row `-Z-S2`, cut the cell to the tools whose key catalog_gate resolves
today. Bucket: the runtime catalog's own `bucket` (`opal-data-portal-v2`). Each tool's key is the `key` of the ONE
catalog row whose `accessors` names the tool's portal accessor, read at one `{scope}` member and admitted by
`catalog_gate.gate()` with the caller's principal (ruling D-5 = (c)). The module holds no key literal.

| tool | portal accessor | exact keys (fence prefix `platinum/mdpf/`) | class | as-of field | catalog ref |
|---|---|---|---|---|---|
| `mdpf_get_aum_metrics(scope)` | `getAUMMetricsByFirm` | `platinum/mdpf/{scope}/aum-metrics.json` | SAFE | `period` | `portal_mdpf_aum_metrics` |
| `mdpf_get_account_distribution(scope)` | `getAccountDistributionByFirm` | `platinum/mdpf/{scope}/account-distribution.json` | SAFE | `period` | `portal_mdpf_account_distribution` |
| `mdpf_get_aggregate_aua(scope)` | `getMdpfAggregateAUATimeSeriesByFirm` | `platinum/mdpf/{scope}/aggregate-aua-timeseries.json` | SAFE | `as_of_last` | `portal_mdpf_aggregate_aua` |

- `{scope}` is one of the members the gate indexes for the row: 49financial, cottonwood, global, inflection. A firm
  principal reads only its own member.
- Excluded inside the fence (analysis AC8): `platinum/mdpf/archive/` and `platinum/mdpf/_manifests/`.
- Every tool takes an optional `as_of` (YYYY-MM-DD). An absent or empty object answers `"no data for that date"`
  with no figure. So does an object whose own as-of differs from the one asked for, and that answer reports both
  dates.
- The data_entitlement class of all three is `legacy`, beside `opal_discover` and `opal_describe`. Both factories
  are wired in `registry.py`, and both integrations stay dormant.

The other seven tools of the analysis's AC7 left this cell for round 3's catalog-row cell: mdpf category-views and
non-model-assets (its catalog verdict is deny), etfs positioning, and the four advi tools. No catalog row was added
for them. Their seven `catalog_entries/portal_*` sources were removed from this branch (row `-Z-W3-S13`).

## R-7 -- model composition and weights: UNANSWERABLE from the portal's objects

No tool answers which holdings, at what weights, make up a model. None of the 13 objects inside the round-1 fence
carries a per-model holdings list with weights:
- `aum-metrics.json` `by_model[]` carries `model_name, aum, account_count, q0..q3`.
- `aggregate-aua-timeseries.json` `by_model.*` carries `display_name, model_value, account_count, cohort_class`.
- `category-views.json` `nodes.Models` carries `aum, display_label, members, children` (each child: `aum, display_label, members`).
- `account-distribution.json` `by_model.*` carries size statistics only.
- `positioning_data.json` carries holdings for the four ETFs, which are funds, not models.
- `mix_summary.json` carries firm-level top holdings, not per-model ones.

The portal objects that might carry model holdings sit under `json/positioning/` (`model.json`,
`holdings_attribution_data.json`). The round-1 analysis excluded them from the fence as a different property
(AC1/AC8), so this cell does not read them. After the item-13 cut, the three tools this cell registers read
`aum-metrics.json`, `account-distribution.json` and `aggregate-aua-timeseries.json` only, and none of them carries
weights.

## Criteria at `bc0cde67f0`

- AC1: `pytest rc=0; named tests passed 2 of 2; failed/error lines 0` -- RESULT: PASS -- exit=0
- AC2: `pytest rc=0; named tests passed 4 of 4; failed/error lines 0` -- RESULT: PASS -- exit=0
- AC3: `pytest rc=0; named tests passed 1 of 1; failed/error lines 0` -- RESULT: PASS -- exit=0

`test_entitlement_admin.py::test_ogz2_ac08` pins portal_index (3) and opal_discover (2), and the total 49
(44 + 3 + 2). It was not run: the file does not collect here (`ModuleNotFoundError: No module named 'moto'`), and
`app/integrations/opal_discover` is not on this tree. Row `-Z-W3-S10` stands.
