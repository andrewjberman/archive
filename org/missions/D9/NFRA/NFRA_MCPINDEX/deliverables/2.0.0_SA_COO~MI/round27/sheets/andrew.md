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

Tested 2026-10-19T18:36:00Z.

## opal-data-assets (bucket)

### client_get_allocation

KNOWN ISSUE: the last test of this tool failed (not_run)

### client_get_fees

KNOWN ISSUE: the last test of this tool failed (not_run)

### client_get_holdings

KNOWN ISSUE: the last test of this tool failed (not_run)

### client_get_transactions

KNOWN ISSUE: the last test of this tool failed (not_run)

### client_resolve_account

KNOWN ISSUE: the last test of this tool failed (not_run)

## opal-data-etfs (bucket)

### etfs_compare_peers

KNOWN ISSUE: the last test of this tool failed (not_run)

### etfs_get_coverage

- How current is the holdings data for the rival fund BIDD

### etfs_get_fund_bloomberg_characteristics

KNOWN ISSUE: the last test of this tool failed (not_run)

### etfs_get_fund_flows

KNOWN ISSUE: the last test of this tool failed (not_run)

### etfs_get_fund_holdings

- What are the holdings of DIVZ on the latest date

### etfs_get_fund_nav_history

- Give me DIVZ daily net assets since July 2026

### etfs_get_fund_snapshot

- What was PFDE's NAV and net assets on the last run

### etfs_get_fund_trades

KNOWN ISSUE: the last test of this tool failed (not_run)

### etfs_get_monthly_report

- Did the September 2026 ETF ownership report go out with all its files

### etfs_get_new_securities

- Which new stocks entered the ETFs on the latest run

### etfs_get_ownership_rollup

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### etfs_get_partner_ownership

- How much DIVZ did 49 Financial hold on 2026-10-12

### etfs_get_peer_group_members

- Who are PFOE's rivals

### etfs_get_research_notes

- What unusual activity did the model flag for TXUE

### etfs_get_rival_fund_holdings

- What does BIDD hold today according to the canonical table

### etfs_get_rival_page_status

- Show me today's rival funds page status
- Show the rival funds page for January 2020

### etfs_get_security_reference

KNOWN ISSUE: the last test of this tool failed (not_run)

### etfs_who_holds

KNOWN ISSUE: the last test of this tool failed (unexpected_empty)

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

- What does each 49 Financial model hold, and at what weights?

## opal-data-portal-v2 (bucket)

### mdpf_get_category_views

- How is 49 Financial AUA split between Models, SMA and Client assets?

### news_market_mood

KNOWN ISSUE: the last test of this tool failed (misrouted)

### opal_asker_query

KNOWN ISSUE: the last test of this tool failed (not_run)

### portal_get_cma_assumptions

- What are the capital-markets assumptions for each asset class?

### portal_get_correlations

- Which correlation windows and tickers does the portal hold?

### portal_get_etf_returns

- What did the ETF benchmarks return this quarter?

### portal_get_factor_tilts

- Show the current factor tilt snapshot for the book.

### portal_get_macro

KNOWN ISSUE: the last test of this tool failed (misrouted)

### portal_get_market_regime

- What market regime are we in and why?

### portal_get_market_returns

- What were the index and sector returns for the year to date?

### portal_get_model_attribution

- What were the QTD, YTD and since-inception attribution totals per model?

### portal_get_model_portfolio_timeseries

- What are the latest daily model and benchmark returns?

### portal_get_model_positioning

- How is each model positioned versus its benchmark today?

### portal_get_peer_performance

- How does each model rank against peers over one year?

### portal_get_pipeline_freshness

- As of what date is the portal model data, and when did the last refresh run?

### portal_get_security_scan

KNOWN ISSUE: the last test of this tool failed (tool_error)

### portal_get_trending

- What are today's top bullish and bearish news themes?

### portal_get_valuation

KNOWN ISSUE: the last test of this tool failed (misrouted)

## Dynamodb (store)

### mdpf_get_security_classification

- What asset class does the classification table give SPY?

### news_keyword_intelligence

- Why is sentiment on the tariff story bearish?

### news_search_articles

KNOWN ISSUE: the last test of this tool failed (not_run)

### news_trending_topics

- What themes were trending in the news on October 16?

## Black Diamond silver (fees) (integration)

### blackdiamond_list_fees

KNOWN ISSUE: the last test of this tool failed (misrouted)

## Estate graph (Kuzu projection) (integration)

### graph_cypher

KNOWN ISSUE: the last test of this tool failed (misrouted)

### graph_status

- How old is the estate graph answer I am about to quote?

## Opal data discovery (the ONE catalog) (integration)

### opal_describe

KNOWN ISSUE: the last test of this tool failed (source_disagrees)

### opal_discover

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

## Opal Portal Data Refresh (integration)

### opal_data_refresh_status

- Has the last data refresh run finished yet?

### opal_data_refresh_upload

KNOWN ISSUE: the last test of this tool failed (not_run)

## Portal precomputed objects (mdpf, model benchmarks, etf positioning) (integration)

### etfs_get_positioning

KNOWN ISSUE: the last test of this tool failed (not_run)

### gateway_query_catalog

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_account_distribution

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_aggregate_aua

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_aum_metrics

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_model_benchmarks

KNOWN ISSUE: the last test of this tool failed (misrouted)

## Schwab (Opal silver) (integration)

### schwab_describe_dataset

- What fields and units does the Schwab position dataset have

### schwab_get_access

- Which Schwab dates can I download right now

### schwab_list_files

- Which Schwab security files exist for early October

### schwab_prepare_download

PREVIEW-ONLY: the send leg is not exercised

### schwab_query

KNOWN ISSUE: the last test of this tool failed (misrouted)

## YCharts (integration)

### ycharts_freshness

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### ycharts_fund_series

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### ycharts_risk_return_scatter

KNOWN ISSUE: the last test of this tool failed (tool_error)

### ycharts_search

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### ycharts_snapshot_metrics

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### ycharts_time_series

KNOWN ISSUE: the last test of this tool failed (tool_error)

## Microsoft 365 (native)

### copy_site_file_to_s3

KNOWN ISSUE: the last test of this tool failed (not_run)

### create_draft

- Draft an email with no recipients named

### find_online_meeting

KNOWN ISSUE: the last test of this tool failed (tool_error)

### find_sharepoint_site

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### get_item

- Show the type and size of the first OneDrive file found

### get_site_item

- Show the metadata of a file on the first Opal site

### inspect_email_attachment

KNOWN ISSUE: the last test of this tool failed (source_disagrees)

### list_calendar

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_channels

- Which channels does my first team have

### list_chats

- Show my three most recently active Teams chats

### list_email_attachments

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_email_filtered

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_meeting_transcripts

- List every transcript of the first Teams meeting found

### list_onedrive

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_recent_email

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_shared_folder

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_site_drives

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_site_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### list_teams

- Which Microsoft Teams am I a member of

### poll_addressed_teams_messages

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### profile_site_file

- Profile the layout of a file on the first Opal site

### read_channel_messages

- Show the three newest messages in the first channel

### read_chat_message_images

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### read_chat_messages

- Read the three newest messages in my most active chat

### read_document

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### read_email

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### read_file

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### read_meeting_transcript

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### read_site_file

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### read_site_workbook

KNOWN ISSUE: the last test of this tool failed (not_run)

### read_teams_attachment

KNOWN ISSUE: the last test of this tool failed (not_run)

### read_workbook

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### reply_email

KNOWN ISSUE: the last test of this tool failed (not_run)

### save_email_attachment_to_site

KNOWN ISSUE: the last test of this tool failed (not_run)

### search_email

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### search_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### search_site_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### send_channel_message

KNOWN ISSUE: the last test of this tool failed (not_run)

### send_chat_message

PREVIEW-ONLY: the send leg is not exercised

### send_email

- Send an email with no recipient named

### upload_text_to_site

KNOWN ISSUE: the last test of this tool failed (not_run)

### validate_ssavail_attachment

KNOWN ISSUE: the last test of this tool failed (source_disagrees)

### whoami

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

## Platform labels

- client_get_allocation [bd49f]: platform: A platform value is accepted only when, lower-cased with surrounding spaces stripped, it reads blackdiamond or black diamond. The check is a constant comparison and reads no column, and any other non-null value is refused platform_not_source_label. | omit: When platform is omitted the check returns at once with no label filter, and the allocation is read for the account as if the argument were not sent.
- client_get_allocation [bdcottonwood]: platform: A platform value must equal a Custodian value present in the newest fact_allocations partition, and also one of the Custodian values of this account's own allocation rows. The match is exact and case-sensitive. Otherwise it is refused platform_not_source_label, and the value is used for nothing else on this path. | omit: When platform is omitted no label check runs and the account's model assignment and target weights are read from the newest partitions of each table.
- client_get_allocation [commonwealth]: platform: The only accepted platform value is the constant commonwealth, compared lower-cased to the adapter's PLATFORM_LABEL. Any other non-null value is refused platform_not_source_label before the account reference is read, and no label is read from data. | omit: When platform is omitted the call goes on after the account reference parses and refuses no_allocation_source with no read, since the closed delivery has no allocation table.
- client_get_allocation [eclipse]: platform: The platform argument is never read on this path, so no value of platform is refused platform_not_source_label. With no model key the call refuses account_not_resolved first, and with a model key it returns the model allocation, which carries no custodian label. | omit: When platform is omitted the call behaves the same as with any value: no model key refuses account_not_resolved, and a model key returns the model allocation with a null platform label.
- client_get_allocation [orion]: platform: A platform value must be an exact custodian label that the newest fact_positions partition holds, else platform_not_source_label. The account rows are then kept only when they carry that custodian, so the allocation is the one custodian's rows. | omit: When platform is omitted every row of the account in the newest fact_positions partition is used, with no custodian filter.
- client_get_allocation [schwab]: platform: Only an omitted platform passes: any non-null value is refused, the contract labels SmartX and BlackDiamond with platform_not_source_label and every other value with platform_enum_open, because the platform enum is open. | omit: When platform is omitted the check returns at once and the allocation is derived from one partition each of dim_position and dim_balance, with no model.
- client_get_allocation [smartx]: platform: The only accepted platform value is the exact string smartx, the adapter's own PLATFORM_LABEL. Any other non-null value, including a case variant, is refused platform_not_source_label before any read. | omit: When platform is omitted the check returns at once and the model assignment, targets and weights are read for the account with no label filter.
- client_get_fees [bd49f]: platform: A platform value is accepted only when, lower-cased with surrounding spaces stripped, it reads blackdiamond or black diamond. The check is a constant comparison and reads no column, and any other non-null value is refused platform_not_source_label. | omit: When platform is omitted the check returns at once with no label filter, and the fee rows of the account are read from the live fees table in the window.
- client_get_fees [bdcottonwood]: platform: A platform value must equal a Custodian value present in the newest fact_transactions partition, else platform_not_source_label. The Management Fee rows are then kept only when their Custodian equals it, so a value naming another custodian returns no fee rows and no refusal. | omit: When platform is omitted no label check runs and every Management Fee row of the account in the window of the newest partition is kept, deduplicated on TransactionID.
- client_get_fees [commonwealth]: platform: The only accepted platform value is the constant commonwealth, compared lower-cased to the adapter's PLATFORM_LABEL. Any other non-null value is refused platform_not_source_label before the account reference is read, and no label is read from data. | omit: When platform is omitted the call goes on after the account reference parses and the window check, then refuses no_fee_source with no read, since there is no fee table.
- client_get_fees [eclipse]: platform: The platform argument is never read on this path, so no value of platform is refused platform_not_source_label. The call refuses no_fee_source at once with zero reads, since there is no Eclipse silver fee table. | omit: When platform is omitted the call refuses no_fee_source at once with zero reads, exactly as it does for any other platform value.
- client_get_fees [orion]: platform: A platform value must be an exact custodian label that the newest fact_transactions partition holds, else platform_not_source_label. The fee rows are then kept only when their own custodian equals it. | omit: When platform is omitted the account's fee rows of the window are read from the newest fact_transactions partition with no custodian filter.
- client_get_fees [schwab]: platform: Only an omitted platform passes: any non-null value is refused, the contract labels SmartX and BlackDiamond with platform_not_source_label and every other value with platform_enum_open, because the platform enum is open. | omit: When platform is omitted the check returns at once and the call goes on to the window check, then refuses no_fee_source with zero reads, since Schwab has no fee table.
- client_get_fees [smartx]: platform: The only accepted platform value is the exact string smartx, the adapter's own PLATFORM_LABEL. Any other non-null value, including a case variant, is refused platform_not_source_label before any read. | omit: When platform is omitted the check returns at once, the window check runs, and the call refuses no_fee_source with zero reads, since SmartX has no fee-row table.
- client_get_holdings [bd49f]: platform: A platform value is accepted only when, lower-cased with surrounding spaces stripped, it reads blackdiamond or black diamond. The check is a constant comparison and reads no column, and any other non-null value is refused platform_not_source_label. | omit: When platform is omitted the check returns at once with no label filter, and the lots of the account are read from the live unrealized table.
- client_get_holdings [bdcottonwood]: platform: A platform value must equal a Custodian value present in the newest fact_allocations partition, and also one of the Custodian values of this account's own allocation rows. The match is exact and case-sensitive. Otherwise it is refused platform_not_source_label, and the holdings rows are not filtered by the value. | omit: When platform is omitted no label check runs and the account's positions and cash are read from the newest holdings partition with every custodian.
- client_get_holdings [commonwealth]: platform: The only accepted platform value is the constant commonwealth, compared lower-cased to the adapter's PLATFORM_LABEL. Any other non-null value is refused platform_not_source_label before the account is read, and no label is read from data. | omit: When platform is omitted no label check runs and the account positions and valuation rows are read from the newest partitions of their tables.
- client_get_holdings [eclipse]: platform: The platform argument is never read on this path, so no value of platform is refused platform_not_source_label. The call refuses vendor_no_holdings at once with zero reads, since Eclipse has no holdings table. | omit: When platform is omitted the call refuses vendor_no_holdings at once with zero reads, exactly as it does for any other platform value.
- client_get_holdings [orion]: platform: A platform value must be an exact custodian label that the newest fact_positions partition holds, else platform_not_source_label. The account rows are then kept only when they carry that custodian, and an account with no row under it is refused account_not_resolved. | omit: When platform is omitted every row of the account in the newest fact_positions partition is used, with no custodian filter.
- client_get_holdings [schwab]: platform: Only an omitted platform passes: any non-null value is refused, the contract labels SmartX and BlackDiamond with platform_not_source_label and every other value with platform_enum_open, because the platform enum is open. | omit: When platform is omitted the check returns at once and the account view is read from one partition each of dim_position and dim_balance.
- client_get_holdings [smartx]: platform: The only accepted platform value is the exact string smartx, the adapter's own PLATFORM_LABEL. Any other non-null value, including a case variant, is refused platform_not_source_label before any read. | omit: When platform is omitted the check returns at once and the positions and cash of the account are read with no label filter.
- client_get_transactions [bd49f]: platform: A platform value is accepted only when, lower-cased with surrounding spaces stripped, it reads blackdiamond or black diamond. The check is a constant comparison and reads no column, and any other non-null value is refused platform_not_source_label. | omit: When platform is omitted the check returns at once with no label filter, and the account transactions of the window are read from the live transactions table.
- client_get_transactions [bdcottonwood]: platform: A platform value must equal a Custodian value present in the newest fact_transactions partition, else platform_not_source_label. The account rows of the window are then kept only when their Custodian equals it, so a value naming another custodian returns an empty window and no refusal. | omit: When platform is omitted no label check runs and every account row of the window in the newest transactions partition is kept, deduplicated on TransactionID.
- client_get_transactions [commonwealth]: platform: The only accepted platform value is the constant commonwealth, compared lower-cased to the adapter's PLATFORM_LABEL. Any other non-null value is refused platform_not_source_label before the window is read, and no label is read from data. | omit: When platform is omitted no label check runs and the account rows of the window are read from the newest transactions partition.
- client_get_transactions [eclipse]: platform: The platform argument is never read on this path, so no value of platform is refused platform_not_source_label. The call refuses vendor_no_transactions at once with zero reads, since no Eclipse silver table carries account transactions. | omit: When platform is omitted the call refuses vendor_no_transactions at once with zero reads, exactly as it does for any other platform value.
- client_get_transactions [orion]: platform: A platform value must be an exact custodian label that the newest fact_transactions partition holds, else platform_not_source_label. The account rows are then kept only when their own custodian equals it, and a label with no row of the account returns an empty window rather than a refusal. | omit: When platform is omitted the account's Complete rows of the window are read from the newest fact_transactions partition with no custodian filter.
- client_get_transactions [schwab]: platform: Only an omitted platform passes: any non-null value is refused, the contract labels SmartX and BlackDiamond with platform_not_source_label and every other value with platform_enum_open, because the platform enum is open. | omit: When platform is omitted the check returns at once and the account dim_transaction rows of the window are read, summed across the partitions in range.
- client_get_transactions [smartx]: platform: The only accepted platform value is the exact string smartx, the adapter's own PLATFORM_LABEL. Any other non-null value, including a case variant, is refused platform_not_source_label before any read. | omit: When platform is omitted the check returns at once, the window check runs, and the call refuses vendor_no_transactions with zero reads, since SmartX has no account-transaction table.
- client_resolve_account [bd49f]: platform: A platform value is accepted only when, lower-cased with surrounding spaces stripped, it reads blackdiamond or black diamond. The check is a constant comparison and reads no column, and any other non-null value is refused platform_not_source_label before the crosswalk is read. | omit: When platform is omitted the check returns at once with no label filter, and every account of the cross-reference whose number ends in the last-4 becomes a candidate.
- client_resolve_account [bdcottonwood]: platform: A platform value must be a Custodian value present in the newest fact_allocations partition for some account, else platform_not_source_label. A candidate is then kept only when the value is one of its own Custodian values, so a passing value can yield no candidate without a refusal. | omit: When platform is omitted no label check runs and every account of the partition whose number ends in the last-4 becomes a candidate, with its own Custodian labels.
- client_resolve_account [commonwealth]: platform: The only accepted platform value is the constant commonwealth, compared lower-cased to the adapter's PLATFORM_LABEL. Any other non-null value is refused platform_not_source_label before the crosswalk is read, and no label is read from data. | omit: When platform is omitted no label check runs and every crosswalk account whose number ends in the last-4 becomes a candidate, each stamped with the constant commonwealth.
- client_resolve_account [eclipse]: platform: A platform value must be a custodian label that the newest Orion fact_positions partition holds, else platform_not_source_label. A candidate is kept only when its custodian equals the value, and a label that matches no candidate is refused no_account_match. | omit: When platform is omitted no label check runs and every row of the newest Orion fact_positions partition ending in the last-4 becomes a candidate.
- client_resolve_account [orion]: platform: A platform value must be an exact custodian label that the newest fact_positions partition holds, else platform_not_source_label. Candidates are then kept only when their own custodian equals it, and a label that matches no account of the last-4 is refused no_account_match. | omit: When platform is omitted no label check runs and every account row of the partition ending in the last-4 becomes a candidate, labelled with its own custodian.
- client_resolve_account [schwab]: platform: Only an omitted platform passes: any non-null value is refused, the contract labels SmartX and BlackDiamond with platform_not_source_label and every other value with platform_enum_open, because the platform enum is open. | omit: When platform is omitted the check returns at once and the call refuses no_resolve_source with zero reads, since Schwab has no resolve source in the gateway.
- client_resolve_account [smartx]: platform: The only accepted platform value is the exact string smartx, the adapter's own PLATFORM_LABEL. Any other non-null value, including a case variant, is refused platform_not_source_label before any read. | omit: When platform is omitted the check returns at once and every firm account whose custodian number ends in the last-4 becomes a candidate, stamped with the constant smartx.
