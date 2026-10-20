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

PLACEHOLDER SHEET: your role is not recorded yet, so this sheet shows the tools of these buckets: m365.

## Dynamodb (store)

### mdpf_get_security_classification

KNOWN ISSUE: the last test of this tool failed (not_run)

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
