# FWD-24 battery over every channel - round 24 re-grade, 2026-10-20 (2.0.0_SA_COO~MI)

GRADE tools=127: PASS=49 EMPTY-CORRECT=4 PREVIEW-ONLY=1 FAIL=73 (round 23: PASS 38, EMPTY-CORRECT 4, FAIL 85). Cases: 162 planned, results for 130.
Inputs: cases_all_20261019.json, results_all_20261020.json (runs 1-7 plus the 15:24Z harvest run; source_check set from SOURCE_COMPARE_20261020.json on 10 results), routing ROUTING_TABLE_20261020b.json (post-emit: link 7, code 3).
Senders: no send, write, upload or mint ran in a runner. Test sends under open call c5c2 were made by the issuer, once each, to the owner's own mailbox (send_email, create_draft); send_chat_message NOT sent (no self-chat). They are recorded in round24/evidence/TEST_SENDS_20261020.json and are not in the graded results: tool_battery.py grades any `sent` result FAIL, so it has no verdict for a test send.

| class | n | tools |
|---|---|---|
| PASS | 49 | etfs_get_coverage, etfs_get_fund_holdings, etfs_get_fund_nav_history, etfs_get_fund_snapshot, etfs_get_monthly_report, etfs_get_new_securities, etfs_get_partner_ownership, etfs_get_peer_group_members, etfs_get_research_notes, etfs_get_rival_fund_holdings, etfs_get_rival_page_status, get_item, get_site_item, graph_status, ... |
| source_unchecked | 29 | etfs_get_ownership_rollup, etfs_get_positioning, find_sharepoint_site, list_calendar, list_email_attachments, list_email_filtered, list_onedrive, list_recent_email, list_shared_folder, list_site_drives, list_site_files, mdpf_get_account_distribution, opal_discover, poll_addressed_teams_messages, ... |
| not_run | 22 | client_get_allocation, client_get_fees, client_get_holdings, client_get_transactions, client_resolve_account, copy_site_file_to_s3, create_draft, etfs_compare_peers, etfs_get_fund_bloomberg_characteristics, etfs_get_fund_flows, etfs_get_fund_trades, etfs_get_security_reference, opal_asker_query, opal_data_refresh_upload, ... |
| misrouted | 13 | blackdiamond_list_fees, gateway_query_catalog, graph_cypher, mdpf_get_aggregate_aua, mdpf_get_aum_metrics, mdpf_get_model_benchmarks, news_keyword_intelligence, news_market_mood, news_search_articles, news_trending_topics, portal_get_macro, portal_get_valuation, schwab_query |
| tool_error | 4 | find_online_meeting, portal_get_security_scan, ycharts_risk_return_scatter, ycharts_time_series |
| EMPTY-CORRECT | 4 | harvest_get_filing_analysis, harvest_get_fundamentals, harvest_get_research, news_for_security |
| source_disagrees | 3 | inspect_email_attachment, opal_describe, validate_ssavail_attachment |
| unexpected_empty | 1 | etfs_who_holds |
| route_unproven | 1 | harvest_get_published_analysis |
| PREVIEW-ONLY | 1 | schwab_prepare_download |

A tool reads not_run until every planned case has a result; the first case of most tools ran. The source instrument verified 26 of 104 tools with an ok result (25 agree, 1 disagrees); 78 are unreadable by it (graph 31, integration 9, store 4, s3 without a date token 34).
