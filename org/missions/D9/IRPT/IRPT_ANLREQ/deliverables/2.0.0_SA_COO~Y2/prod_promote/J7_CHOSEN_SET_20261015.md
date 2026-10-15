# J7 chosen set for the PROD promote -- 2.0.0_SA_COO~Y2, 2026-10-15 ~14:5xZ (CTO msg 8332)

**The set (`--features`): ONE branch.** `cand/dell2/anlreq-internal-filer-chooses-firm`, one commit `6f4e5f671f09` ("feat(TicketCenter AR-y-325): an Opal staff filer chooses the firm from the served list (PRD ADDENDUM v0.6 J7)"). Approved as call 1f3e (CLOSED; CTO msg 8332: Andrew approved it). EXCLUDED: `cand/dell2/anlreq-commentary-always-requested` (c8c3, commit `406345bce1`), as the CTO ruled.

Claim words: MEASURED = this seat ran it in this session; RECORD = a committed file read; NOT READ = said so.

## Refs read (MEASURED, `git fetch origin PROD DEV` at ~14:45Z)
origin/PROD `c3b21a40e29f`; origin/DEV `ad7c100b5cca`; J7 branch tip `6f4e5f671f09`, an ancestor of origin/DEV (`merge-base --is-ancestor`).

## Why J7 stands alone (the other DEV candidates the CTO named are NOT needed)
- `git log origin/PROD..J7-branch` lists exactly one commit (`6f4e5f67`): J7 was cut on a base already in PROD (merge-base with PROD `6a5926fc11`, in PROD history). It touches five files only: `src/pages/TicketCenter/AnalysisRequestParts.tsx`, `TicketCenter.tsx` and three tests under `__tests__/` (`analysis-firm-c-firm`, `analysis-firm-choice`, `internal-filer-chooses-firm`).
- MEASURED in a scratch worktree at origin/PROD (`C:/dev/j7-promote-check`, a detached checkout, node_modules linked): `git cherry-pick 6f4e5f671f` applied with no conflict (the commit step then failed only for lack of a git identity in that checkout, so the change sits staged, uncommitted); `bun run typecheck` (`tsc -b --noEmit`) rc 0; `bun test src/pages/TicketCenter` 121 pass, 0 fail, 23 files. So 8500 (held-submit words), 7b45 (advisory fee), fde0 (model order) and 7773 (partner-firm stack) are not dependencies of J7 on the PROD tip.
- c8c3 stays out: on PROD plus J7 `commentary_requested` is only an optional type field (`src/pages/InvestorReporting/contracts/wire/AnalysisSubmissionRequest.ts:23`) and the form's "Add commentary" box writes the ticket answer `add_commentary`, not the intake wire field (MEASURED by `git grep` at that tree), so no filing sends it until c8c3 or later code does. The live intake Lambda refuses that member until IB-pr-456 applies (CTO).

## What the promote changes (for the receipt)
Page: Ticket Center, New Analysis Request, for an Opal STAFF caller: the Firm chooser from the served Global list replaces the "staff open requests from the queue rather than file them" sentence, and the catalogue (models, tickers) then loads once a firm is chosen (source read at both refs, row `IRPT_ANLREQ-D2-S119`). The approval row lists the class as client-facing; the CTO's ruling (2402) reads the Ticket Center as Opal-internal. Andrew approved the candidate (1f3e).

## NOT read
The vite build of PROD plus J7 (only typecheck and the Ticket Center tests were run); live behaviour after the promote (the staff form's firms read and the partner-firm catalogue against the live API are source predictions, row S119); whether the PROD tip moves before GO (the set is recomputed against the tip at GO: the cherry-pick and the two checks are cheap to repeat). The scratch worktree `C:/dev/j7-promote-check` holds the staged cherry-pick and is registered in the portal repository: remove it with the standing word for merged worktrees once it is reset (a `git reset --hard` there was refused by the destructive-git guard, so it is left for MSTR).
