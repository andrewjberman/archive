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

PLACEHOLDER SHEET: your role is not recorded yet, so this sheet shows the tools of these buckets: portal, news.

## opal-data-harvest (bucket)

### news_for_security

- Show the last week of news on Apple

## opal-data-mdpf (bucket)

### mdpf_get_model_composition

KNOWN ISSUE: the last test of this tool failed (not_run)

## opal-data-portal-v2 (bucket)

### mdpf_get_category_views

KNOWN ISSUE: the last test of this tool failed (not_run)

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

KNOWN ISSUE: the last test of this tool failed (not_run)

### news_keyword_intelligence

KNOWN ISSUE: the last test of this tool failed (misrouted)

### news_search_articles

KNOWN ISSUE: the last test of this tool failed (misrouted)

### news_trending_topics

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

KNOWN ISSUE: the last test of this tool failed (not_run)

## Portal precomputed objects (mdpf, model benchmarks, etf positioning) (integration)

### etfs_get_positioning

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### gateway_query_catalog

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_account_distribution

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### mdpf_get_aggregate_aua

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_aum_metrics

KNOWN ISSUE: the last test of this tool failed (misrouted)

### mdpf_get_model_benchmarks

KNOWN ISSUE: the last test of this tool failed (misrouted)

## Microsoft 365 (native)

### find_online_meeting

KNOWN ISSUE: the last test of this tool failed (not_run)

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

KNOWN ISSUE: the last test of this tool failed (not_run)

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

KNOWN ISSUE: the last test of this tool failed (not_run)

### search_email

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### search_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### search_site_files

KNOWN ISSUE: the last test of this tool failed (source_unchecked)

### validate_ssavail_attachment

KNOWN ISSUE: the last test of this tool failed (not_run)

### whoami

KNOWN ISSUE: the last test of this tool failed (source_unchecked)
