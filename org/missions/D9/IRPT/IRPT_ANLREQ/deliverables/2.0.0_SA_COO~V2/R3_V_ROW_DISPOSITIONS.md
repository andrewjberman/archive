# IRPT_ANLREQ round 3, workstream TICKET (`2.0.0_SA_COO~V2`) -- AR-v-31: dispositions, the issuer's own misses, and how the portal candidate was made

**Issuer:** `2.0.0_SA_COO~V2`, 2026-10-16. Cell `AR-v-31` (the ticket page reads a hop failure, FWD-4, C-HOP-FAILURE v0.21), worker `0.9.0_WK_IRPT_ANLREQ~270`, order `TO-AR-v31` at three amendments, merged on the workspace side at `7c5a823480` (LOCAL; push not read). Everything below is for the CVO's L8/L9 read; nothing here is a verdict.

## A. The worker's rows

| row | class | what | proposed disposition |
|---|---|---|---|
| `IRPT_ANLREQ-D2-W270-S1` | BLOCKING, ARMED (`disarm_owner` this seat) | a ticket with a request id and neither a draft nor a package was never read: `TicketCenter.tsx` mounted the block only when a draft or package existed, so three of the five hop codes could not show | DISARMED by the issuer's AMENDMENT 1 (the same gap, found by the issuer in review before the worker reported). Evidence: tests `shows the failure on a ticket with neither a draft nor a package` and `leaves no blank row ...` pass (10 of 10); `AnalysisPackageRow` replaces the guarded row in `TicketCenter.tsx` |
| `IRPT_ANLREQ-D2-W270-S2` | OBSERVATION | the order said "the requester firm", the file reads `ticket.answers.firm` | `NOT_A_DEFECT`: the existing `PackageFiles` code in the same file (the package-open path, before this cell) already uses `ticket.answers?.firm` as the tenant for its owned reads; the order's wording was imprecise and the worker followed the file |
| `IRPT_ANLREQ-D2-W270-S3` | OBSERVATION | the portal adapter maps the wire actions `WAIT` and `NONE` to the same `'none'` | `NOT_A_DEFECT` for this cell: `hopFailureWords` also requires a hop `publicReasonCode`, and `~G2`'s producer appends a `NONE` action last for a hop failure (msg 9053), so no live path shows a `WAIT` as words. Carried to the CVO's reading of `AR31-v-AC4J` |
| `IRPT_ANLREQ-D2-W270-S4` | BLOCKING, INERT | `AR31-v-AC3`'s mutant (remove the display guard) could not fire after AMENDMENT 2 | dispositioned by the issuer's AMENDMENT 3: the mutant is now the call gate's package condition, which the worker had measured as its control; the issuer re-ran it: `MUTANT-FIRES` (9 pass, 1 fail on `makes no status call for a ticket whose package is attached`), file restored byte for byte |

## B. The issuer's own misses in this cell (stated, not softened)

1. **The cut omitted the draft axis.** The first Rule 24 record listed request id, package and status, not draft. All six first tests rendered a ticket that had a draft, so they passed while the page could not show the failure for a ticket without one. Found by reading the worker's first commits against the contract; AMENDMENT 1 and a corrected record.
2. **The first version made a status call for every ticket on the board**, including a finished request whose answer clause 5 hides. Found by running the worker's checks and reading its diff; AMENDMENT 2.
3. **The mutant I named went stale with my own amendment** (AMENDMENT 3).
4. **I misread "this seat approves the portal candidate".** In the CTO's ruling (msg 8908) "this seat" is the CTO. The approval is the CTO's lane (portal law: `opal-internal` waits for the building box's CTO lane); the issuer registers the candidate and asks. Earlier drive-log lines that say the issuer approves are wrong on this point.

## C. The portal candidate: how it was made and where it differs from the worker's commits

`cand/dell2/ticket-hop-failure-read` on origin at `e564a543882d` (ls-remote read 2026-10-16), registered as call `dell2-20261016T064045Z-0633`, class `opal-internal`. The worker's four portal commits (`e24facfa`, `eafc9aee`, `f4e5cc18`, `f488e20a`) were cut from DEV; the portal procedure (CONTRIBUTING-BOXES step 2) wants a branch cut from the last PROD release, so the issuer re-cut them onto `a062c56e` (`origin/PROD`) by cherry-pick. DEV carries approved, unreleased work in the same two files, which produced two conflicts, resolved by hand, each keeping ONLY this cell's lines:

1. `AnalysisRequestParts.tsx`, the `PackageReaders` interface: the incoming side also carried the `getAnalysisRequestCommentaryPdf` line, which belongs to another DEV-only feature. Kept: the `getJobStatus` comment and signature only.
2. `TicketCenter.tsx`, the board row: the incoming side carried the `meeting_request` block lines of round 18's DEV-only candidate as diff context. Resolved to the single `<AnalysisPackageRow .../>` line in place of the old analysis row and its two closing lines (`</tr>`, `)}`), which close that old block on the PROD structure.

A first attempt of this cherry-pick went wrong (a scripted edit failed to open its path while the next command ran anyway, so a commit with conflict markers was made on the local, never-pushed branch). It was aborted back to the PROD release before any push, and redone one commit at a time with each resolution refusing to stage on a remaining marker.

**Measured on the PROD-based candidate (not on the worker's DEV-based tree):** diff against PROD is the three files only (`AnalysisRequestParts.tsx`, `TicketCenter.tsx`, the new test); `tsc -b` rc 0; `bun test src/pages/TicketCenter` 138 pass, 0 fail across 25 files (DEV's tree has 31 files because of DEV-only features); the cell's `v31-failure` check prints `V31-FAILURE-OK pass=10`. The worker's own DEV-based numbers (193 pass, 0 fail, 31 files; the mutant firing) are in its record.

**Why the class is `opal-internal`, measured:** `TicketCenter.tsx` computes `internal = auth.isInternal() || auth.isDev()` and `partner = !internal`; the partner branch (`if (partner) {` and its `return`) returns before the board and its own comment says "No other ticket type, metric, board or claim/complete control is rendered"; the new row component is used only in the internal render after it (measured in the worker's tree, where the branch ran from line 579 to 690; the line numbers on the PROD-based candidate differ). The two files also carry the partner view, which this change does not touch.

## D. What is not done

- **The live arm** (each failure driven on purpose against the released status route) is FWD-4's run. `irpt-status` carries the reader live (`~G2`, msg 9134, CodeSha `+TcZDWmw...`), but no live job row carries `hop_failure` yet: the resident writers ship in the r34 re-apply and the commentary writer is `~T2`'s.
- **Not looked at as a real screenshot:** the worker rendered the block in a DOM test (markup saved in its `render_markup.txt`); `scripts/ui-smoke.mjs` was not run because it needs fixtures no one has validated for this state. `AR31-v-AC4J` is the CVO's judgment on that evidence.
