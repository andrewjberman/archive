# NFRA_CTLPLN round 28 -- FWD-23 reads: each box's seat list, from committed files (2.0.0_SA_COO~C, 2026-10-16 ~11:2xZ)

Read from `origin/box/<box>` (git, not a seat's report). PRD FWD-23 DONE WHEN: one box's seat list read by someone who then names each seat's work without opening a log, and one finished piece of work shown with its grade.

| box | seats.json commit | rows | written (Z) by | committed by | graded finished piece named | call |
|---|---|---|---|---|---|---|
| laptop | stale file, written 2026-10-15T12:37Z by `0.9.0_WK_NFRA_CTLPLN~107` | not re-read | worker | worker | CVO v24 read (earlier round) | none (own box) |
| dell1 | `b83562e324` | 21 | `0.0.0_AB_MSTR~DELL1` 10:22:59Z | `1.0.0_SA_CTO~DELL1` (the lane does not admit MSTR) | NOT YET named (no note read) | `XB-20261016T101128Z-0ff7` ACKED, MSTR record `160c2981e1`; from-side OPEN |
| dell2 | `7464c5847c` | 21 | `0.0.0_AB_MSTR~DELL2` 10:26:22Z | `1.0.0_SA_CTO~DELL2` | `IRPT_DASHBD r147 PUBLISH, graded by CVO~IRPT v131` (`0f32dc96b3`) | `XB-20261016T101128Z-bfaa` to-side CLOSED 10:30:11Z |
| site Z | `653d950a92` | 12 | `0.0.0_AB_MSTR~Z` 10:24:34Z | `1.0.0_SA_CTO~Z` (the lane does not admit MSTR) | NOT YET named (no note read) | `XB-20261016T101129Z-a856` ACKED; from-side OPEN |

Each file's `schema` reads `seat-list/1` and carries `device`, `written_at`, `written_by`, and per seat a serial, kind, live flag, `doing` (WORKING / IDLE / NOTHING / BLOCKED), project and a one-line summary. Three of four boxes now hold a current list; the laptop's own list is 26 hours old and is rewritten by the next `python .tools/seat-list.py write` on this box (not done: this seat's act is the read).

## Not read, and not asserted

- The act the DONE WHEN names, a person reading one box's list and naming each seat's work without opening a log, has NOT been run: a reader (the CVO or Andrew) is owed it. The files above are what that reader reads; `python .tools/seat-list.py show` prints them.
- dell1 and site Z have not named a graded finished piece; the calls stay open from this side until each does (or the CTO rules the piece named in the list's own summaries).
- "One that is doing nothing" (ACCEPT): dell1 `2.0.0_SA_COO~D1` reads `doing=NOTHING`, dell2 `2.0.0_SA_COO~N2` and `~S2` read `NOTHING`; this seat read the flag, not whether it is true.
