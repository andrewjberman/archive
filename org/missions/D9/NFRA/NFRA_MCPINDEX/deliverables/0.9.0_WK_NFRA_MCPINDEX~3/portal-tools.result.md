# NFRA_MCPINDEX.TO-MX-t-8 -- the portal tools: result

`0.9.0_WK_NFRA_MCPINDEX~3`, branch `wk-NFRA_MCPINDEX-3`, base `d59217f5a8`. Tests:
`infra/aws/ec2/opal-gateway/tests/test_portal_index.py`.

**The integration module is NOT in the gateway tree.** The naming commit gate (ENFORCE) refuses it, because every
exact key the portal serves today is a legacy-layout literal that `address()` cannot produce (row
`NFRA_MCPINDEX-Z-W3-S6`, BLOCKING). The refused bytes are kept, unexecuted, at
`deliverables/0.9.0_WK_NFRA_MCPINDEX~3/candidate/portal_index/{__init__,integration}.py`. They belong at
`app/integrations/portal_index/` once the naming remedy lands. Everything below describes that module.

## The ten tools

Bucket: `opal-data-portal-v2`. Each tool reads ONE whole object by exact key, and `read_object` fences it
before any S3 call. Every tool declares class `SAFE` on `SPEC.tool_classifications` (one GetObject each, no write).

| tool | exact keys (fence prefix) | as-of field | catalog ref |
|---|---|---|---|
| `mdpf_get_aum_metrics(scope)` | `platinum/mdpf/{49financial,cottonwood,global,inflection}/aum-metrics.json` | `period` | `portal_mdpf_aum_metrics` |
| `mdpf_get_account_distribution(scope)` | `platinum/mdpf/{4 scopes}/account-distribution.json` | `period` | `portal_mdpf_account_distribution` |
| `mdpf_get_aggregate_aua(scope)` | `platinum/mdpf/{4 scopes}/aggregate-aua-timeseries.json` | `as_of_last` | `portal_mdpf_aggregate_aua` |
| `mdpf_get_category_views(scope)` | `platinum/mdpf/{4 scopes}/category-views.json` | `as_of` | `portal_mdpf_category_views` |
| `mdpf_get_non_model_assets()` | `platinum/mdpf/global/non-model-assets.json` | `latest.date` | `portal_mdpf_non_model_assets` |
| `etfs_get_positioning(fund)` | `platinum/etfs/positioning_data.json`; answers `portfolios.{fund}` | `portfolios.{fund}.data_as_of` | `portal_etfs_positioning` |
| `advi_get_leaderboard(scope)` | `platinum/advi/49financial/leaderboard.json` | `data_as_of` | `portal_advi_leaderboard` |
| `advi_get_mix_summary(scope)` | `platinum/advi/49financial/mix_summary.json` | `data_as_of` | `portal_advi_mix_summary` |
| `advi_get_partner_analytics(scope, period)` | `platinum/advi/49financial/partner_analytics_{annual,quarterly}.json` | `data_as_of` | `portal_advi_partner_analytics` |
| `advi_get_growth_chart(scope, chart)` | `platinum/advi/49financial/{cumulative_chart,timeseries_chart,timeseries_overview}.json` | `data_as_of` | `portal_advi_growth_chart` |

Excluded inside the fence (analysis AC8): `platinum/mdpf/archive/`, `platinum/mdpf/_manifests/`,
`platinum/etfs/_manifests/`, `platinum/advi/49financial/_manifests/`. The Inflection/Cottonwood firm buckets are
out of scope. Every as-of field was confirmed by a read-only `s3api get-object` of the 13 live keys on
2026-09-25. Only key names and date fields were printed, and nothing was committed.

Every tool takes an optional `as_of` (YYYY-MM-DD). An absent or empty object answers
`"no data for that date"` with no figure. So does an object whose own as-of differs from the one asked for, and
that answer reports both dates.

## R-7 -- model composition and weights: UNANSWERABLE from the portal's objects

No tool answers which holdings, at what weights, make up a model. None of the 13 objects inside this fence carries
a per-model holdings list with weights:
- `aum-metrics.json` `by_model[]` carries `model_name, aum, account_count, q0..q3`.
- `aggregate-aua-timeseries.json` `by_model.*` carries `display_name, model_value, account_count, cohort_class`.
- `category-views.json` `nodes.Models` carries `aum, display_label, members, children` (each child: `aum, display_label, members`).
- `account-distribution.json` `by_model.*` carries size statistics only.
- `positioning_data.json` carries holdings for the four ETFs, which are funds, not models.
- `mix_summary.json` carries firm-level top holdings, not per-model ones.

The portal objects that might carry model holdings sit under `json/positioning/` (`model.json`,
`holdings_attribution_data.json`). The round-1 analysis excluded them from the fence as a different property
(AC1/AC8), so this cell does not read them.

## Criteria

On the committed tree, AC1, AC2 and AC3 all fail: the six tests cannot import `app.integrations.portal_index`
(row `-Z-W3-S6`).

Before the commit, with the module in place, the module read 4 passed and 2 failed. AC2's three tests and AC3's
one test passed. AC1's two tests failed on limbs this order cannot reach (BLOCKING/INERT):
- `-Z-W3-S1`: `data_entitlement.classify` returns None for 10 of 10 tools, because `app/data_entitlement.py` is outside `<paths>`.
- `-Z-W3-S2`: `DATA_CATALOG.yaml` cannot be regenerated here. `emit_catalog_v02.py` refuses because `portal/src/api` is absent, while the 10 source entries validate.

Rows `-S3` (registry wiring), `-S4` (catalog_entries is the silver mechanism) and `-S5` (single `tool_prefix`) are
OBSERVATION/INERT.
