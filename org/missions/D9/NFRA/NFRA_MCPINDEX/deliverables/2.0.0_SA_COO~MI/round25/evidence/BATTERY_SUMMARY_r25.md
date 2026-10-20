# FWD-24 battery - round 25 re-grade, 2026-10-20 (2.0.0_SA_COO~MI)

GRADE tools=127: PASS=51 EMPTY-CORRECT=4 PREVIEW-ONLY=2 FAIL=70 (round 24 re-grade: PASS 49, FAIL 73; round 23: PASS 38, FAIL 85).
Grader: the merged MX-y-2 (a sent result is PASS on the tester's own read-back, else FAIL send_unconfirmed; send_chat_message PREVIEW-ONLY). Routing: ROUTING_TABLE_20261020b.json (the round-25 link rule is NOT yet in this table; it was emitted before MX-y-4 merged).
Source compare (MX-y-1 by-key rule, list-only): 106 tools with an ok result: agrees 30, disagrees 1 (harvest_query_columns), unreadable 75 (graph 33, s3 undated 29, integration 9, store 4). Independent probes for graph, integration and store need a read route outside the gateway; none exists in this session, so those 46 stay source_unchecked with their reasons.
Test sends (open call c5c2) by the issuer, once each, read back from the owner's own mailbox: send_email (one send, Sent Items and Inbox copies) and create_draft (one draft); both PASS. send_chat_message NOT sent (no self-chat).

| class | n | tools |
|---|---|---|
| PASS | 51 | create_draft, etfs_get_coverage, etfs_get_fund_holdings, etfs_get_fund_nav_history, etfs_get_fund_snapshot, etfs_get_monthly_report, etfs_get_new_securities, etfs_get_partner_ownership, etfs_get_peer_group_members, etfs_get_research_notes, etfs_get_rival_fund_holdings, etfs_get_rival_page_status, get_item, get_site_item, ... |
| source_unchecked | 27 | etfs_get_ownership_rollup, find_sharepoint_site, list_calendar, list_email_attachments, list_email_filtered, list_onedrive, list_recent_email, list_shared_folder, list_site_drives, list_site_files, opal_discover, poll_addressed_teams_messages, read_chat_message_images, read_document, ... |
| not_run | 20 | client_get_allocation, client_get_fees, client_get_holdings, client_get_transactions, client_resolve_account, copy_site_file_to_s3, etfs_compare_peers, etfs_get_fund_bloomberg_characteristics, etfs_get_fund_flows, etfs_get_fund_trades, etfs_get_positioning, etfs_get_security_reference, opal_asker_query, opal_data_refresh_upload, ... |
| misrouted | 14 | blackdiamond_list_fees, gateway_query_catalog, graph_cypher, mdpf_get_account_distribution, mdpf_get_aggregate_aua, mdpf_get_aum_metrics, mdpf_get_model_benchmarks, news_keyword_intelligence, news_market_mood, news_search_articles, news_trending_topics, portal_get_macro, portal_get_valuation, schwab_query |
| tool_error | 4 | find_online_meeting, portal_get_security_scan, ycharts_risk_return_scatter, ycharts_time_series |
| EMPTY-CORRECT | 4 | harvest_get_filing_analysis, harvest_get_fundamentals, harvest_get_research, news_for_security |
| source_disagrees | 3 | inspect_email_attachment, opal_describe, validate_ssavail_attachment |
| PREVIEW-ONLY | 2 | schwab_prepare_download, send_chat_message |
| unexpected_empty | 1 | etfs_who_holds |
| route_unproven | 1 | harvest_get_published_analysis |
