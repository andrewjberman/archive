# NFRA_TRNSPT TR-om-23 -- the four Monday meetings by another route: NOT FOUND, and this route cannot answer (2026-10-11 ~07:0xZ)

Seat: 2.0.0_SA_COO~T2 (issuer read; cell TR-om-23, CTO round-23 analysis item 3). Gateway identity: Andrew@opalinvest.com. Read-only.
File names, folders, sizes and dates only; no file was opened. No landing.

## Verdict, per date

| meeting created | found by another route? | what answered |
|---|---|---|
| 2026-04-10 | NOT FOUND | every read below |
| 2026-04-13 | NOT FOUND | every read below |
| 2026-05-04 | NOT FOUND | every read below |
| 2026-06-01 | NOT FOUND | every read below |

**This is a FAILED RETRIEVAL, not an absence.** The series (`Morning Meeting`, `data/transcripts/scripts/teams/series.json`) is organized
by another person, so its recordings and transcripts, if kept, sit in the ORGANIZER'S OneDrive. The gateway's file tools read the
signed-in user's OneDrive and the default library of a named SharePoint site. None of them reads another user's drive. So the place
the analysis names first, "the organizer's OneDrive", was not read by any tool: 0 of 1.

## What was read (denominators printed)

| read | result |
|---|---|
| `list_onedrive` `Recordings` (Andrew's own) | 5 files, all `...-Meeting Recording.mp4`, dated 2026-07-07 to 2026-08-19; none is a Morning Meeting and none falls on the four dates. No `.vtt` or transcript file in the folder |
| `search_files` (Andrew's OneDrive) `Morning Meeting` | 2 hits, both unrelated (a zip and a csv) |
| `search_files` `Morning Meeting Transcript` | 0 |
| `search_files` `Meeting Recording` | 4 hits, all unrelated workspace files |
| `list_teams` | 5 teams: Opal OCIO, Opal CIO Office for 49 Financial, 49 Financial Internal Channel, Opal Consulting, Opal Capital. None is named for the meeting |
| `search_site_files` `Morning Meeting` on OpalCapital | 0 |
| `search_site_files` `Meeting Recording` on OpalCapital, OpalOCIO, OpalConsulting | 1 unrelated docx, 0, 0 |
| `list_site_files` OpalCapital root and `General` (read 02:3xZ, `R22_RESEARCH_SHAREPOINT_READ_20261011.md`) | 13 folders, none `Recordings`; `General` holds 5 PDFs |

Sites searched: 3 of the 7 found by name (not searched this time: 49Financial, OpalCIOOfficefor49Financial,
OpalTradeSubmissionsandApprovals501, smarshteamsarchive).

**The search tool's zero is not a zero.** Positive control: `list_onedrive` shows five files named `...Meeting Recording.mp4` in Andrew's
own `Recordings` folder, and `search_files` for `Meeting Recording` returned NONE of them. The search does not see files a listing
proves are there, so every `0` in the table above is "the search returned nothing", never "no such file".

**A second structural limit.** The five recordings that are visible are `.mp4` files with no separate transcript beside them. A Teams
transcript is normally not a file in the drive at all; it is held with the meeting and served by the meeting route, which is the route
that already refuses these four. A recording, where one exists, would need its own speech-to-text to become a transcript, which is a
different pipeline from anything this project runs.

## What would answer it

ONE of:
1. The organizer looks in their own OneDrive `Recordings` folder for the four dates and says what is there (a person's act, minutes).
2. A gateway capability to list another user's drive (owner NFRA_OPLGTW, site Z), which is a wider permission and its own decision.
3. Smarsh, the firm's Teams archive (`smarshteamsarchive` is a site in the tenant): whether it archives meeting transcripts is unknown here.

## For the CTO's ruling on row D2-S15

The analysis said: not found means a PRD addendum naming the four as lost to every route read. Stated exactly, the routes READ are the
meeting route (refused, 502) and Andrew's own drive and three team sites (nothing). The organizer's drive, the route most likely to hold
anything, is UNREAD. So "lost to every route read" would be true and would still leave the likeliest place unopened; item 1 above is
cheap and is the issuer's recommendation before the addendum is written.
