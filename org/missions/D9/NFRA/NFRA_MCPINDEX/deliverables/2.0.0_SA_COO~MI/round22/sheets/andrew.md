# Opal gateway cheat sheet

This sheet is generated from the gateway's own tool list, your current access and a test run of every tool listed. It lists only the tools your sign-in reaches today. If your access changes, ask for a new sheet.

## How to connect

1. Add the Opal gateway to Claude as a custom connector. The address is `https://mcp.opalinvest.dev/mcp/`.
2. When Claude asks you to sign in, use your Opal Microsoft account (your @opalinvest.com address). The first sign-in opens a Microsoft page; approve it once.
3. Ask your question in plain words. Claude picks the tool. If you do not know which tool holds a fact, ask Claude to use `opal_discover` with a short subject such as "harvested news articles"; it names the dataset, how fresh it is and the next tool to call.

## How to tell a refusal from an empty answer

- A refusal carries an `error` and `guard_denied: true`, with a short `code` (for example `harvest_prefix_not_served`). It means the tool did not read anything for you: you are not granted that data, or the request named something the tool does not serve. Do not read a refusal as "no data".
- An empty answer has no `error`. It carries an `as_of` date or an `absent_reason` that says why nothing was found, and a count of zero. Zero rows is not the same as "nothing happened": for example zero articles in a day is not "no chatter" when the answer's `data_status` says the publishers were not all covered.
- Every answer states its as-of date. If the date is older than you expect, say so when you use the figure.

Tested 2026-10-19T15:24:00Z.

## opal-data-assets (bucket)

### client_get_allocation

NOT YET TESTED

### client_get_fees

NOT YET TESTED

### client_get_holdings

NOT YET TESTED

### client_get_transactions

NOT YET TESTED

### client_resolve_account

NOT YET TESTED

## opal-data-etfs (bucket)

### etfs_compare_peers

NOT YET TESTED

### etfs_get_coverage

NOT YET TESTED

### etfs_get_fund_bloomberg_characteristics

NOT YET TESTED

### etfs_get_fund_flows

NOT YET TESTED

### etfs_get_fund_holdings

NOT YET TESTED

### etfs_get_fund_nav_history

NOT YET TESTED

### etfs_get_fund_snapshot

NOT YET TESTED

### etfs_get_fund_trades

NOT YET TESTED

### etfs_get_monthly_report

NOT YET TESTED

### etfs_get_new_securities

NOT YET TESTED

### etfs_get_ownership_rollup

NOT YET TESTED

### etfs_get_partner_ownership

NOT YET TESTED

### etfs_get_peer_group_members

NOT YET TESTED

### etfs_get_research_notes

NOT YET TESTED

### etfs_get_rival_fund_holdings

NOT YET TESTED

### etfs_get_rival_page_status

NOT YET TESTED

### etfs_get_security_reference

NOT YET TESTED

### etfs_who_holds

NOT YET TESTED

## opal-data-harvest (bucket)

### harvest_get_article

- Show one article by its key

### harvest_get_chatter

- How much press chatter was there on Apple in early October

### harvest_get_filing_analysis

- Show the latest analysed filing for Apple

### harvest_get_fundamentals

- Show Apple's reference fundamentals

### harvest_get_peers_and_scores

- Who are Apple's closest peers

### harvest_get_published_analysis

- Show the published overlay for Apple

### harvest_get_research

- Show our research dossier on Apple

### harvest_list

- List the tables the harvest bucket holds in its gold layer

### harvest_query_columns

- Show three daily chatter rows for Apple

### harvest_read

- Read one harvest object by its key

### harvest_resolve_security

- What is the harvest security key for AAPL

### harvest_search_articles

- Show the latest three articles that mention Apple

### harvest_security_coverage

- What does the harvest bucket hold on Apple and how fresh is it

### news_for_security

- Show the last week of news on Apple

## opal-data-mdpf (bucket)

### mdpf_get_model_composition

NOT YET TESTED

## opal-data-portal-v2 (bucket)

### mdpf_get_category_views

NOT YET TESTED

### news_market_mood

NOT YET TESTED

### opal_asker_query

NOT YET TESTED

### portal_get_cma_assumptions

NOT YET TESTED

### portal_get_correlations

NOT YET TESTED

### portal_get_etf_returns

NOT YET TESTED

### portal_get_factor_tilts

NOT YET TESTED

### portal_get_macro

NOT YET TESTED

### portal_get_market_regime

NOT YET TESTED

### portal_get_market_returns

NOT YET TESTED

### portal_get_model_attribution

NOT YET TESTED

### portal_get_model_portfolio_timeseries

NOT YET TESTED

### portal_get_model_positioning

NOT YET TESTED

### portal_get_peer_performance

NOT YET TESTED

### portal_get_pipeline_freshness

NOT YET TESTED

### portal_get_security_scan

NOT YET TESTED

### portal_get_trending

NOT YET TESTED

### portal_get_valuation

NOT YET TESTED

## Dynamodb (store)

### mdpf_get_security_classification

NOT YET TESTED

### news_keyword_intelligence

NOT YET TESTED

### news_search_articles

NOT YET TESTED

### news_trending_topics

NOT YET TESTED

## Microsoft 365 (native)

### copy_site_file_to_s3

NOT YET TESTED

### create_draft

NOT YET TESTED

### find_online_meeting

NOT YET TESTED

### find_sharepoint_site

NOT YET TESTED

### get_item

NOT YET TESTED

### get_site_item

NOT YET TESTED

### inspect_email_attachment

NOT YET TESTED

### list_calendar

NOT YET TESTED

### list_channels

NOT YET TESTED

### list_chats

NOT YET TESTED

### list_email_attachments

NOT YET TESTED

### list_email_filtered

NOT YET TESTED

### list_meeting_transcripts

NOT YET TESTED

### list_onedrive

NOT YET TESTED

### list_recent_email

NOT YET TESTED

### list_shared_folder

NOT YET TESTED

### list_site_drives

NOT YET TESTED

### list_site_files

NOT YET TESTED

### list_teams

NOT YET TESTED

### poll_addressed_teams_messages

NOT YET TESTED

### profile_site_file

NOT YET TESTED

### read_channel_messages

NOT YET TESTED

### read_chat_message_images

NOT YET TESTED

### read_chat_messages

NOT YET TESTED

### read_document

NOT YET TESTED

### read_email

NOT YET TESTED

### read_file

NOT YET TESTED

### read_meeting_transcript

NOT YET TESTED

### read_site_file

NOT YET TESTED

### read_site_workbook

NOT YET TESTED

### read_teams_attachment

NOT YET TESTED

### read_workbook

NOT YET TESTED

### reply_email

NOT YET TESTED

### save_email_attachment_to_site

NOT YET TESTED

### search_email

NOT YET TESTED

### search_files

NOT YET TESTED

### search_site_files

NOT YET TESTED

### send_channel_message

NOT YET TESTED

### send_chat_message

NOT YET TESTED

### send_email

NOT YET TESTED

### upload_text_to_site

NOT YET TESTED

### validate_ssavail_attachment

NOT YET TESTED

### whoami

NOT YET TESTED
