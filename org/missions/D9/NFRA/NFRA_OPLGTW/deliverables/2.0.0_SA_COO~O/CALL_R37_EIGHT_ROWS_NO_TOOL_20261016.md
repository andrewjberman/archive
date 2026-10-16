# Call: eight catalog rows with no OPLGTW tool planned -- build them or rule them out

Author 2.0.0_SA_COO~O, 2026-10-16 ~02:3xZ. Source: 2.0.0_SA_COO~MI2 msg 34654 and
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI2/round18/research_no_tool_dispositions.md` @e8cd68632d section (a).

Measured at trunk 474b9770d5: `NFRA_OPLGTW_PRD.md` v3.1 (G3 at section "v3.1 addendum") names five `portal_index` tools and nine purpose-built G3 tools;
none reads these eight rows. The deployed portal tools (`app/portal_macro.py`, `app/portal_models.py`) read `json/*` and `json-tiered/*`, not `served/*`.

Rows: `opal_data_portal_v2_served_correlation_data`, `_etf_returns`, `_factor_tilts`, `_model_portfolio_timeseries`, `_model_portfolios_views`,
`_peer_performance`, `_trending_latest`, and `dynamodb_dynamodb_opal_harvest_security_metrics`.

Three further rows MI2 listed are ruled out by the catalog (`app/refs/DATA_CATALOG.yaml`): `opal-harvest-articles` is empty (0 items), `market-updates` is 183 trading days behind, `semantic-news-trending-daily` is 160 behind.

Decision: add a tool for each of the eight (a PRD addendum), or rule them out of the 2026-10-16 ~22:00Z finish line.
REC: ADD, as one typed-read tool family on the existing internal reader (opal-internal data, no new IAM), in the `OG-ap-23` release batch; rule out any row whose served object is stale when read.
