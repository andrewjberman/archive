# NFRA_TRNSPT FWD-2 -- first read of the Research Meeting SharePoint source (2026-10-11 ~02:3xZ)

Seat: 2.0.0_SA_COO~T2 (dell2). Ask: 1.0.0_SA_CTO~DELL2 msg 3884, on Andrew's answer row 13 of
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261010_133xZ_FIFTEEN_OPEN_ITEMS_ANSWERED.md`
("Lauren added me to some share point folder where they collect anyway"). The record names no site, folder or link.

Identity of the gateway session (measured, `whoami`): Andrew@opalinvest.com.

## Verdict

NOT LOCATED. The gateway's site-file tools did not return a Research Meeting transcript folder. This is a failed
retrieval, NOT an absence: the tools search sites by NAME and each site's DEFAULT library only, and they have no
"shared with me" read. A folder shared by link, or one inside another person's OneDrive (where Teams stores a
meeting's recording and transcript), is out of their reach by construction.

## What was read (denominators printed)

| read | result |
|---|---|
| `find_sharepoint_site` name = Research, Meeting, Investment, Transcript | 0 sites each |
| `find_sharepoint_site` name = Opal | 6 sites: OpalOCIO, OpalCapital, OpalConsulting, OpalTradeSubmissionsandApprovals501, OpalCIOOfficefor49Financial, 49Financial |
| `find_sharepoint_site` name = Team | 1 site: smarshteamsarchive (the Smarsh archiving group; not searched) |
| `list_site_drives` OpalCapital | 1 library (Documents) |
| `list_site_files` OpalCapital root | 13 folders: Alongside, Andrew-scratch, Ausdal, claude-staging, ClaudeTemp, End of Day Updates, End-of-Day Updates, General, Holdings, Market Update, Model Update Checklist, Opal Client Tickets, Website. None is a research or meeting folder |
| `list_site_files` OpalCapital /General | 5 files, none a transcript |
| `search_site_files` "Research Team Meeting" / "transcript" on OpalCapital | 1 unrelated hit (an earnings brief PDF) / 0 |
| `search_site_files` "Research" on OpalOCIO, OpalConsulting, 49Financial, OpalCIOOfficefor49Financial | 1 unrelated, 0, 0, 3 unrelated (2024 benchmark PDFs) |
| `search_files` (Andrew's OneDrive) "Research Team Meeting transcript", "Research Team Meeting", "Research Meeting" | no transcript item; hits are workspace files synced from a Desktop |
| `search_files` "transcript" | 64,488 characters returned; a name filter for Research, Meeting, Recording, .vtt, .docx matched 0 rows |

Sites searched by content: 5 of the 7 named sites found (not searched: OpalTradeSubmissionsandApprovals501,
smarshteamsarchive). No file body was opened; names and sizes only.

## What un-blocks it

ONE of:
1. The folder's link, or its site name plus path, from Andrew. With a site name the existing tools can list it.
2. A gateway capability to read "shared with me" items or a drive by id (owner NFRA_OPLGTW, site Z), if the folder
   lives in a personal OneDrive.

Queued as an open call on this box (`python .tools/open-calls.py list`). FWD-2 stays 1 of 4 on the Graph route until
then; nothing else in round 22 waits on it.
