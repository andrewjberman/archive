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

## opal-data-mdpf (bucket)

### mdpf_get_model_composition

- What does each 49 Financial model hold, and at what weights?

## opal-data-portal-v2 (bucket)

### mdpf_get_category_views

- How is 49 Financial AUA split between Models, SMA and Client assets?

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

## Microsoft 365 (native)

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

### search_email

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### search_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### search_site_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### validate_ssavail_attachment

KNOWN ISSUE: the last test of this tool failed (source_disagrees)

### whoami

KNOWN ISSUE: the last test of this tool failed (source_unchecked)
