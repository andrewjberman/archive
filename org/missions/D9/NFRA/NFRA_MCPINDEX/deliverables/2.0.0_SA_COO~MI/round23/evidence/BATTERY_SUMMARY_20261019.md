# FWD-24 battery over every channel - 2026-10-19 (2.0.0_SA_COO~MI)

GRADE tools=127: PASS=38 EMPTY-CORRECT=4 FAIL=85. Case counts: {'PASS': 52, 'EMPTY-CORRECT': 4, 'REFUSED-CORRECT': 2, 'PREVIEW-ONLY': 0, 'FAIL': 104}.
Inputs: cases_all_20261019.json (162 cases), results_all_20261019.json (113 results; runs 1-4 at 18:36Z-20:19Z, harvest 15:24Z), routing ROUTING_TABLE_20261019.json.
Senders were preview only; no send, write, upload or mint was called. Not run is FAIL not_run, never pass.

| class | n | tools |
|---|---|---|
| PASS | 38 | etfs_get_new_securities, etfs_get_peer_group_members, etfs_get_research_notes, etfs_get_rival_fund_holdings, get_item, get_site_item, graph_status, harvest_get_article, harvest_get_chatter, harvest_get_peers_and_scores, harvest_get_published_analysis, harvest_list, harvest_query_columns, harvest_read, ... |
| source_unchecked | 35 | blackdiamond_list_fees, etfs_compare_peers, etfs_get_fund_bloomberg_characteristics, etfs_get_fund_flows, etfs_get_fund_snapshot, etfs_get_fund_trades, etfs_get_ownership_rollup, etfs_get_positioning, etfs_get_security_reference, find_sharepoint_site, list_calendar, list_email_attachments, list_email_filtered, list_onedrive, ... |
| not_run | 32 | client_get_allocation, client_get_fees, client_get_holdings, client_get_transactions, client_resolve_account, copy_site_file_to_s3, create_draft, etfs_get_coverage, etfs_get_fund_holdings, etfs_get_fund_nav_history, etfs_get_monthly_report, etfs_get_partner_ownership, etfs_get_rival_page_status, find_online_meeting, ... |
| misrouted | 11 | gateway_query_catalog, graph_cypher, mdpf_get_aggregate_aua, mdpf_get_aum_metrics, mdpf_get_model_benchmarks, news_keyword_intelligence, news_market_mood, news_search_articles, news_trending_topics, portal_get_macro, portal_get_valuation |
| EMPTY-CORRECT | 4 | harvest_get_filing_analysis, harvest_get_fundamentals, harvest_get_research, news_for_security |
| tool_error | 3 | portal_get_security_scan, ycharts_risk_return_scatter, ycharts_time_series |
| source_disagrees | 2 | inspect_email_attachment, opal_describe |
| unexpected_empty | 1 | etfs_who_holds |
| route_unproven | 1 | harvest_resolve_security |

Gateway-code or data defects for COO~O: tool_error (portal_get_security_scan AccessDenied s3:ListBucket for the reader role; ycharts_time_series and ycharts_risk_return_scatter upstream 403), unexpected_empty etfs_who_holds (newest date only), source_disagrees (opal_describe ItemCount 386383 vs catalog 381261; inspect_email_attachment), stale as-of 2026-09-30 on portal_get_model_attribution / peer_performance / pipeline_freshness, portal_get_macro null.
Not gateway defects: source_unchecked (35) means the answer came back and the second instrument was not run; not_run (32) are tools whose inputs the runner could not supply (client_* need a staff-typed last-four), or were never attempted.

Note on not_run: a tool is graded not_run when ANY of its planned cases has no result; the runners ran each tool's first case only, so a tool whose first case passed still reads not_run while its later cases wait. Case level: 52 PASS, 4 EMPTY-CORRECT, 2 REFUSED-CORRECT, 104 FAIL of 162 planned cases; 113 cases have a result.
