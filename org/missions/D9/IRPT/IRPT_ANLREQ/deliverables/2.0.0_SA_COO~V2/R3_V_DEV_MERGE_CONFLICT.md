# AR-v-31's approved portal candidate does not merge into DEV: the facts, and the two ways forward (read 2026-10-16 ~07:3xZ)

**Candidate:** `cand/dell2/ticket-hop-failure-read` at `ac828834e433` (on origin, ls-remote read), approved by the CTO as row `dell2-20261016T071559Z-d870` (msg 9163, Opal-internal, "merge it forward to DEV").

## What happened

`bash .tools/portal-merge-forward.sh cand/dell2/ticket-hop-failure-read` (no `--push`) refused: `result=REFUSED reason=conflict`, DEV unchanged (`dev_before` = `dev_after` = `34a6baf8`), nothing pushed.
**Two readings of that line, because the first was wrong:** the first run said `conflict` but its own output showed `Committer identity unknown` (the portal repository has no committer identity here, and the script relies on an ambient one); the script reports ANY failed merge as `conflict`. Re-run with a committer identity supplied through the environment for that one run (my serial; nothing written to any config), the refusal is a GENUINE conflict: `AnalysisRequestParts.tsx` and `TicketCenter.tsx` (`git merge-tree --write-tree origin/DEV <candidate>` agrees).

## Why: five unreleased DEV commits overlap the same two files

The candidate is cut from the PROD release (CONTRIBUTING-BOXES step 1, as ruled) and DEV carries approved but unpromoted work in the same hunks. DEV-only commits touching these two files (`git log origin/PROD..origin/DEV --no-merges`): `0ba0cb13` (AR-y-365, the door's not-covered notice), `9b20efde` (AR-y-363, the unknown-ticker decision tree), `284e54d2` (AR-y-332, the commentary PDF opener), and `c05e3dda` and `12c164a0` (round 18's Trade Request upload and Meeting Request: this project's own candidate, on DEV, not yet on PROD). The conflicts are the same two hunks resolved by hand when the candidate was re-cut onto PROD: the `PackageReaders` interface (DEV carries one more line) and the board row in `TicketCenter.tsx` (DEV carries the meeting block after it).
**No hand resolution is possible by design:** the script's last check requires the merge commit's parents to be exactly DEV and the approved tip, so a conflict can only be removed by changing what is approved.

## Option A: a DEV-based re-cut (a new head, a waiver, a promote-order constraint)

The worker's five portal commits applied to the current DEV tip (`34a6baf8`) WITHOUT conflict. Measured on that tree (scratch worktree, never pushed): `tsc -b` rc 0; `bun test src/pages/TicketCenter` 196 pass, 0 fail across 31 files; the cell's check `V31-FAILURE-OK pass=13`.
**But the registration tool refuses it:** `open-calls.py add --kind approval ... --check-only` on a local branch of that tree prints `APPROVAL-REGISTER result=REFUSED reason=dev-overlap overlap=38 commits=43` (38 of its 43 commits are already on DEV). The tool has `--waive-overlap` and `--waiver-ref`; a waiver is the CTO's. If waived and landed, the feature depends on the four overlapping features above, so a PROD promote list must carry them in front of it (a promote of this feature alone would conflict the same way).

## Option B: hold the PROD-based approved head

It merges cleanly once the overlapping features are on PROD and the candidate is re-cut onto that PROD (PROD has already moved from `a062c56e` to `8012cd1a`; the old base is an ancestor, so a re-cut is a rebase of the same five commits). No coupling and no waiver, but the landing waits on the promotion of features that may include client-facing ones (earlier approval rows on these two files were classed client-facing; I have not re-read each overlapping feature's class), which waits on Andrew's word, so DEV would not carry the page read until then.

## Recommendation

**Option A with the waiver, and the promote list ordered (the four overlapping features first).** FWD-4's run needs the page on DEV when the resident writers (r34) and the commentary writer land, and the promotion of the overlapping features is not under this seat's control. The PROD-based head stays on origin as the fallback, so choosing B later costs nothing. Either way, nothing waits on this except FWD-4's live run; no client sees the page.
