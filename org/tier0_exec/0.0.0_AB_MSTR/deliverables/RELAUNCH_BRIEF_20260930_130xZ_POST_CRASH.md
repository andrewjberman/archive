# RELAUNCH BRIEF -- post-crash, 2026-09-30 ~13:0xZ (laptop)

Issued by `0.0.0_AB_MSTR` on Andrew's word (record
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20260930_130xZ_POST_CRASH_RELAUNCH_CTO_AND_COO_FABRIC_CANONICAL_DRIVE.md`).
Read this, then `org/XXX.md`. This file is a pointer set, not a state report.

## What happened (measured)

- The laptop REBOOTED at 2026-09-30 07:52Z (`systeminfo` boot time 03:52 ET). Every seat, every worker
  subagent, every Monitor and every cron died with it. Nothing was wound down; nothing was handed off.
- Last commits before the reboot landed at 07:49Z (`a7a6d286f2`, 1.0.0_SA_CTO). Local `CLOUD` is 14 commits
  ahead of `origin/CLOUD` (`9e4997d618`), 0 behind, merge-tree clean, deploy ceiling 0. The push waits on
  Andrew's word to `0.0.0_AB_MSTR`; no other seat pushes a shared branch.
- The broker (`org/mcp/liveness.json`) held only `0.0.0_AB_MSTR` at 12:57Z. Every other registration is gone,
  so a `get_agent_status` of a peer reads OFFLINE until that peer relaunches.

## The disclaimer (Andrew's word, relayed verbatim in scope)

> Launch them with a disclaimer about how they need to assess state based on last logs/commits/etc., clean up
> any residue, and continue /canonical-drive on their various projects.

So, in order, before any new act:

1. **ASSESS YOUR OWN STATE FROM ARTIFACTS, NEVER FROM STATUS PROSE.** Your last session log, your last
   commits (`git log --author="^<your serial> <" -20`), your open task orders
   (`python .tools/to-check.py --all --assignee <your full serial>`), your project's surprise channel and
   `.open_deploys/` entries, and your delivery ledger (`get_delivery_state(<serial>, since=2026-09-30T05:00Z)`).
   A `<status>` is a claim; a commit is evidence. Anything you "remember" is from a dead context.
2. **CLEAN UP YOUR RESIDUE.** Worker worktrees left by the crash (`git worktree list --porcelain`; the ten
   present at 13:0xZ are listed below), an `index.lock` in the shared tree or in `portal/`, a half-open
   `org/critical_paths/.open_deploys/` entry (measure the artifact first; world-done closes SUPERSEDED, never
   re-executes), unacked mail, an armed FAST lease that has lapsed (`org/mcp/drive-mode.log`). A worker that
   died mid-order is re-cut by its issuer; its branch is drained or deleted by that issuer, nobody else.
3. **CONTINUE `/canonical-drive` ON YOUR OWN PROJECT** under the DIRECTED row already in `org/ref/LIVE_ARMS.md`.
   This relaunch re-authorizes the continuation of those rows; it adds no new arm and lifts no hold. A row absent
   there arms nothing. The CTO continues its `/self-drive 30m laptop directives` row on the same basis.

## Seating (unchanged from before the crash; one project per Tier-2 instance, Tier-1 lanes as before)

| Serial | Project(s) | Loop |
|---|---|---|
| `1.0.0_SA_CTO` | laptop directives (L2/L3/L4/L10 owner for every row below) | `/self-drive 30m laptop directives` |
| `2.0.0_SA_COO~P` | IRPT_BCKEND workstream P | `/canonical-drive 10m` |
| `2.0.0_SA_COO~M` | IRPT_BCKEND workstream M + MDPF_SECCLASS | `/canonical-drive 10m` |
| `2.0.0_SA_COO~Y` | IRPT_BCKEND workstream Y | `/canonical-drive 10m` |
| `2.0.0_SA_COO~D` | DSGN_IRPTV1 (FAST lease routes ticks to `/closer-drive` only while a lease is live) | `/canonical-drive 10m` |
| `2.0.0_SA_COO~T` | NFRA_TRNSPT (Andrew-direct seating, `ff522abbed`); MDPF_TAXSMA parked | `/canonical-drive` per its L6 state |

Not relaunched by this word (Andrew named the CTO and the COO fabric): `3.0.0_SA_CVO`, `4.0.0_SA_CRO`,
`4.0.0_SA_CRO~T`, `0.7.0_AE_CloudOps`, the `~O` fabric (`1.0.0_SA_CTO~O`, `2.0.0_SA_COO~O/~MI/~MP/~AI`). MSTR has
asked Andrew. Until they are back, an L8/L9 hand-off to the CVO is a FILE on the record, not a message; nothing
waits on a dead seat, and a slug is written to the record for the CVO to compile when it relaunches.

## Worktrees present at 13:0xZ (owner cleans its own)

```
C:/Users/AndrewBerman/Desktop/wk-nfra-oplgtw-og-v-4-p1 c4054b7c6c [wk-nfra_oplgtw-og-v-4-p1]   ~O fabric
C:/Users/AndrewBerman/Desktop/wk_irpt_bckend_84        00b88da890 [wk-IRPT_BCKEND-84]          IRPT_BCKEND issuer
C:/Users/AndrewBerman/Desktop/wk_irpt_bckend_93        571d032b98 [wk-IRPT_BCKEND-93]          IRPT_BCKEND issuer (~M, round 29)
C:/Users/AndrewBerman/Desktop/wk_mdpf_secclass_8       275797b529 [wk-MDPF_SECCLASS-8]         ~M
C:/Users/AndrewBerman/Desktop/wt-cro-t-transcripts     7e31cce92f [cro-t-transcripts]          4.0.0_SA_CRO~T
C:/Users/AndrewBerman/Desktop/wt-gw-f1 / f2 / f3 / int                                          gateway mail tools (CRO~T / CloudOps)
```

## Mechanics reminders

- Register your FULL serial, write the session serial file, run `/watcher` once. Zero crons at launch except the
  LIVE_ARMS row you hold.
- Commit via `.tools/safe-commit.sh -F <msgfile>`; never push. Push state in a report is a MEASURED value.
- Rule 31: one ask per message, under 150 words; the broker refuses over the cap.
- The rail is on: `comp-which` / `comp-find` / `comp-read`, never a raw recursive grep.
