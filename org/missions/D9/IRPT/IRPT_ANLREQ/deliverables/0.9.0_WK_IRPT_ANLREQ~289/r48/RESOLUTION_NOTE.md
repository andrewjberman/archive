# RESOLUTION_NOTE -- AR-y-389 (TO IRPT_ANLREQ.TO-AR-y-389), branch cand/dell2/prod-into-dev-reconcile

Head e5682ec51cbffd1bff95525e0dabb6f4508bc9cc (LOCAL, portal worktree; nothing pushed).
Base origin/DEV 539b1ee70ba1b2a9b0c562a9169d9fcca1b7c18e. Merged origin/PROD 15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8 with --no-ff.
Merge-base fa21a303d872. Both refs read at the values the order names (no move).

## Trial before the merge

`git merge-tree --write-tree --name-only origin/DEV origin/PROD` printed the conflicted files
`src/api/endpoints/tickets.ts` and `src/pages/TicketCenter/TicketCenter.tsx`, and
`src/pages/InvestorReporting/dashboard/DashboardPerformance.tsx` auto-merged. Commit counts: 23 PROD-only (21 non-merge, 2 merges), 102 DEV-only.
After the merge `git diff --name-only --diff-filter=U` listed exactly the two named files (3 conflict hunks and 1 conflict hunk).

## Rule used for every conflicted hunk

For each hunk the PROD side is either the older text of the same member (before a DEV change) or the same change in other
surroundings. The DEV side is a superset in all four hunks, so the DEV side is kept once. No hunk drops a PROD-only change, because
the PROD-only content of these two files is empty (see the PROD-vs-DEV check below).

## src/api/endpoints/tickets.ts (3 hunks)

| hunk | lines (merged file) | DEV side (kept) | PROD side (dropped) | DEV commit carrying the DEV side | PROD commit carrying the PROD side |
|---|---|---|---|---|---|
| H1 | Ticket interface, `attachment` member | `attachment?: TicketAttachment \| TradeFormAttachment \| null` | `attachment?: TicketAttachment \| null` | c05e3dda (Trade Request form upload, DEV only) | f7fa7fb1 (analysis upload door; predates the trade member) |
| H2 | CreateTicketInput `answers`, `attachment` | `answers?: AnalysisRequestAnswers \| MeetingRequestAnswers \| TradeRequestAnswers`; `attachment?: TicketAttachment \| TradeFormAttachment` | `answers?: AnalysisRequestAnswers \| MeetingRequestAnswers`; `attachment?: TicketAttachment` | c05e3dda | PROD text is a strict subset of the DEV text |
| H3 | between recordCommentarySent and recordMeetingOutcome | `requestAttachmentUpload` and `getTicketAttachmentUrl`, with their doc comments (the upload door and the read URL, TCKT_VNEXT R18-tf-4) | nothing (PROD has no such functions) | c05e3dda | none; recordMeetingOutcome (the PROD-side text after the hunk) is on DEV too, identical |

Resolution by hunk: H1, H2 and H3 take the DEV side; the common text and recordMeetingOutcome appear once. The resolved file's tail is DEV's tail, byte for byte.

## src/pages/TicketCenter/TicketCenter.tsx (1 hunk)

| hunk | lines | DEV side (kept) | PROD side (dropped) | DEV commit | PROD commit |
|---|---|---|---|---|---|
| H4 | line 90-94, the TradeRequestParts import | `import { TradeRequestForm, TradeFormOpen } from './TradeRequestParts'` | `import { TradeRequestForm } from './TradeRequestParts'` | c05e3dda | b8fc4628 (mounts the Trade Request form; no TradeFormOpen) |

Resolution: the DEV line is kept, so `TradeFormOpen` stays imported and used on DEV's `<TradeFormOpen ticket={t} />` render.

## Auto-merged hunks (not conflicted)

- `src/pages/InvestorReporting/dashboard/DashboardPerformance.tsx` auto-merged to the DEV blob 288b3bb6e02a. PROD's only change from the base (037b9af3, DB-c-24: MONTH_NAMES, monthDayYearWords, "Returns from" sentence) is already in DEV's blob, carried by 9e0bcb60 (line 82-87 and 168 identical).
- `src/pages/TicketCenter/TicketCenter.tsx` other auto-merged regions: the resolved file equals DEV's blob. The PROD-vs-DEV difference in this file is 6 lines, all DEV-only Trade Request code (`readFirms`, `client`, `internal` props of TradeRequestForm, and `<TradeFormOpen ticket={t} />`). PROD adds nothing here.

## What the merge adds to DEV (the proof the order asks for)

- `git diff origin/DEV cand/dell2/prod-into-dev-reconcile -- src/api/endpoints/tickets.ts`: empty.
- `git diff origin/DEV cand/dell2/prod-into-dev-reconcile -- src/pages/TicketCenter/TicketCenter.tsx`: empty.
- `git diff --name-only origin/DEV cand/dell2/prod-into-dev-reconcile`: empty. The merge's tree equals origin/DEV's tree (d445d9c8b793 on both).
  So no hunk is PROD-only in the merge result, and every hunk of `git diff origin/DEV <branch>` is zero; there is no PROD commit to name.
- `git cherry origin/DEV origin/PROD` gives 16 `-` (patch-equal to a DEV commit) and 5 `+` (patch not on DEV). The five `+` commits have their content on DEV already, carried by DEV commits:

| PROD commit (not a DEV ancestor) | subject, short | DEV carrier of the same content |
|---|---|---|
| 037b9af3 | DB-c-24 partial-history sentence (DashboardPerformance, two tests) | 9e0bcb60 |
| b4c219c8 | DB-c-26 page mirror; an EMPTY commit (tree equal to its parent 037b9af3) | a8d5dafc / a020da0b (DB-c-26 on DEV) |
| c7a63531 | meeting outcome line in every status, coordinator controls (TicketCenter, MeetingRequestParts, tests) | 8e4f0885 |
| 2cf8ec35 | AR-v-31 hop failure read through the status route (AnalysisRequestParts, TicketCenter, test) | c748b8fe |
| 8623c829 | AR-v-31 AMENDMENT 1: hop failure for a ticket with neither draft nor package | 7d5f953c |

The two PROD merge commits among the 23 are not counted by `git cherry`; their effect is covered by the tree equality above.

## Trade Request code

- `git diff --name-only origin/DEV <branch>`: empty, so no path matches `trade`.
- The `trade`/`Trade` lines of `src/pages/TicketCenter/TicketCenter.tsx`: 10 lines on the branch; the same 10 as origin/DEV (set equal, gates_check.py).
- No Trade Request line was added, moved or removed. The Trade Request code was not edited by the worker: the resolved files are DEV's bytes.

## Checks (the record; the verdicts are in the checkers' output)

- ancestry_check.py: ANCESTRY-OK head e5682ec51cbf, 24 commits over DEV (23 PROD commits plus the merge), no conflict markers under src.
- gates_check.py: GATES-OK; typecheck 0 errors; eslint 0 errors (2 warnings, identical on DEV); failing test lines 55 on the branch and 55 at origin/DEV at the same path (multiset equal); new load errors 0; AMENDMENT-1 name subset 51 of 51 and trade lines equal.
- once_check.py: ONCE-OK 44 exports and 86 imports in the two files, none repeated; control: a duplicated export is rejected in each file (CONTROL-FIRES).

## Deviations from the order, recorded

- `git merge` has no `--author` option (surprise row IRPT_ANLREQ-D2-W289-S1). The merge ran with `--no-commit` and the identity in env vars; the commit was made with `git commit --author` and the same env.
- The merge commit was made with `--no-verify` (IRPT_ANLREQ-D2-W289-S2). The portal commit-msg hook only appends a SURFACE_ACK line when SURFACE_ACK is set; it was unset.
- The first DEV baseline ran in a detached worktree at another depth (.scratch/portal-dev-ref). It showed a false difference of one failing line (superseded; IRPT_ANLREQ-D2-W289-S3). The baseline used for every equality claim is the same tree at the portal path (git switch --detach origin/DEV, then back to the branch; status clean both times).
- `git switch -c` at creation set the branch's upstream tracking to origin/DEV (git's own config write on branch creation). Nothing was pushed.

## Not read by this worker

The rendered pages, the vite build, any server, any live call. Judgment (AR389-y-AC4J) is for 3.0.0_SA_CVO at L9. The full bun test suite was not run: only `src/pages/TicketCenter` and `src/pages/InvestorReporting`, as the order names. Eslint covered the two conflicted files only, the only files the merge touched.
