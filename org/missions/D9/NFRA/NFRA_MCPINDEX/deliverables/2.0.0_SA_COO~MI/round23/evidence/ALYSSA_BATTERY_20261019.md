# Alyssa 19:00Z battery - verdict table (2.0.0_SA_COO~MI, 2026-10-19 18:36Z-18:50Z)

Scope: schwab, portal, etfs channels she reaches. Two sequential runners, one call at a time, read-only, stopped at 18:50Z.
RESULT: 15 of 61 planned tools run, 15 ok, 0 error, 0 refused, 46 NOT RUN (cutoff). No gateway FAIL; host stayed up (health 200 at 18:35Z).
Not run is not pass. Large answers (compare_peers 58k, positioning 76k chars, schwab_get_access) consumed the window.

| tool | status | rows | as_of | source_check |
|---|---|---|---|---|
| schwab_get_access | ok | 8 | 2026-10-16 | null |
| schwab_list_files | ok | 10 | 2026-10-16 | agrees=True |
| schwab_describe_dataset | ok | 11 | None | agrees=True |
| schwab_query | ok | 3 | 2026-10-16 | null |
| etfs_get_positioning | ok | 1 | 2026-10-16 | null |
| etfs_compare_peers | ok | 30 | 2026-10-19 | null |
| etfs_get_coverage | ok | 1 | 2026-10-16 | agrees=True |
| etfs_get_fund_bloomberg_characteristics | ok | 1 | 2026-10-16 | null |
| etfs_get_fund_flows | ok | 5 | 2026-10-13 | null |
| etfs_get_fund_holdings | ok | 31 | 2026-10-16 | agrees=True |
| etfs_get_fund_nav_history | ok | 97 | 2026-10-13 | agrees=True |
| etfs_get_fund_snapshot | ok | 1 | 2026-10-18 | null |
| etfs_get_peer_group_members | ok | 6 | 2026-10-19 | agrees=True |
| etfs_get_new_securities | ok | 1 | 2026-10-19 | agrees=True |
| etfs_get_ownership_rollup | ok | 1 | 2026-10-19 | null |

NOT RUN (46): mdpf_get_account_distribution, mdpf_get_aggregate_aua, mdpf_get_aum_metrics, mdpf_get_model_benchmarks, gateway_query_catalog, mdpf_get_model_composition, mdpf_get_category_views, news_market_mood, portal_get_cma_assumptions, portal_get_correlations, portal_get_etf_returns, portal_get_factor_tilts, portal_get_macro, portal_get_market_regime, portal_get_market_returns, portal_get_model_attribution, portal_get_model_portfolio_timeseries, portal_get_model_positioning, portal_get_peer_performance, portal_get_pipeline_freshness, portal_get_security_scan, portal_get_trending, portal_get_valuation, etfs_get_fund_trades, etfs_get_monthly_report, etfs_get_partner_ownership, etfs_get_research_notes, etfs_get_rival_fund_holdings, etfs_get_rival_page_status, etfs_get_security_reference, etfs_who_holds, mdpf_get_security_classification, news_keyword_intelligence, news_search_articles, news_trending_topics, graph_status, graph_cypher, opal_describe, opal_discover, opal_data_refresh_status, ycharts_freshness, ycharts_fund_series, ycharts_risk_return_scatter, ycharts_search, ycharts_snapshot_metrics, ycharts_time_series

Not attempted at all: m365 (40 tools; senders preview-only per c5c2), dynamodb, globgrph, opal_portal, opal-data-harvest, mdpf (1), opal_discover (listed above), schwab_prepare_download.
Raw rows: scratchpad alyssa/run1.json, run2.json (session ca6a9190).
