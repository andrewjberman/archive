# 0.0.0_AB_MSTR handoff before the box reboot -- 2026-09-21 ~10:00Z (Mon ~6:00 AM ET)

Andrew at the `1.0.0_SA_CTO` terminal, relayed VERBATIM in msg 99025: *"I am about to wind down this computer going
into a reboot."* Every session dies with the box. This file is what the next `0.0.0_AB_MSTR` session reads first.

## State at write time, measured

- `origin/CLOUD` = local HEAD = `d7904401ad` (ls-remote read after the push). All 8 commits 1.0.0_SA_CTO listed as
  local in 99025 are ON ORIGIN (is-ancestor, 8 of 8).
- `origin/SITEZ` = `047aee5478`, unmoved since 2026-09-18 19:45 ET. Site Z is usage-limited per Andrew; FIVE bus
  frames from this seat sit unread in the laptop-to-sitez queue: 4209a2fd, 0a21daf1 (WRONG, superseded by b7fb74f9),
  b7fb74f9, 465d4a3a (Andrew's ask: a whole-fabric /outcome-check for Fri 09-18 through Sun 09-20 12:00 PM ET plus a
  push of SITEZ), 60982373 (the Opal_Bloomberg elevated firewall read + a status frame). No /integrate is possible
  until a Site Z seat is live.
- Live seats before the reboot: 1.0.0_SA_CTO, 2.0.0_SA_COO~B (IRPT_BCKEND round 8), ~T (MDPF_TAXSMA), ~M
  (NFRA_MCPINDEX), 3.0.0_SA_CVO. Closed by Andrew earlier: ~G, ~O, 0.7.0_AE_CloudOps~V, 4.0.0_SA_CRO.
- Disk 34 GB free. RAM 80%, of which ~10.4 GB was resident KERNEL PAGED POOL after 5+ days of uptime -- the reboot
  is the only thing that returns it. After the reboot, read the pool early (`Get-Counter '\Memory\Pool Paged
  Resident Bytes'`) and again a few hours in: the growth RATE is what would identify the cause. No pool-tag tool is
  installed.

## Andrew's standing words to this seat (2026-09-21, verbatim in the two records named below)

- MSTR manages the FABRIC ONLY: unstick, spawn/kill, push/merge with Site Z. No opinions on project work.
- A paused or stuck seat is MSTR's to clear with /unstick WITHOUT asking. `/govern` on a 2-hour loop -- the cron was
  session-only (id edb1e2fa) and DIES with this session: RE-ARM IT (`17 */2 * * *`, prompt in LD-0596's record).
- No new COO seats "for the remainder of the session"; that session ends with this reboot -- ask nothing, but do
  not assume the hold carries over either: the 3-COO cap and SEQUENCE.yaml govern, and 1.0.0_SA_CTO is conferred
  with on which lane.
- Records: `ANDREW_DIRECT_20260921_005xZ_SEVEN_OPEN_CALLS_ANSWERED.md` (this folder), LD-0596 .. LD-0599.

## What a fresh MSTR does first

1. /watcher (the inbox watcher now prints `[WATCHER-EXPIRED]` at 1770 s and exits -- re-run /watcher that turn),
   then /agentbus (its Monitor has the same 30-minute death and NO alert yet).
2. Census live claude.exe seats; peek any that look idle at a prompt after relaunch (post-restart seats sit at
   their first prompt until nudged).
3. Re-arm /govern every 2 hours.
4. `git fetch`, push CLOUD if ahead; read the five unread Site Z frames' state.

## Still with Andrew (not MSTR's to decide)

Developer Mode toggle (needs elevation; this user cannot create symlinks, which is why terraform COPIES its
provider per root -- measured); TOTP MFA device for Andrew_Berman_Console (deferred by him); at 1.0.0_SA_CTO's
queue: the five Schwab tools, the Gateway rollback-repair owner, the naming-backlog seat, ADVI_FIRMBKTS seating.

## Open fabric-hygiene items

- Shared box MEMORY.md is at its size ceiling with concurrent writers: Edit tool ONLY (it refuses on a changed
  file); a compaction to <17.1 KB is owed in a QUIET window.
- `/cleanup` has a fifth pool, `terraform-provider-cache`; its removal arm has not yet run through the engine.
- `C:\tmp\_reaped_scratch_20260921\` (148 MB) holds the archived scratch of nine removed worktrees.
- Six worktree heads are backed up on origin as tags `backup-20260920/*`; none of those six is removable
  (3.0.0_SA_CVO verdict @29fce296c2).

## A BRANCH THAT MUST NOT BE MERGED -- added 10:4xZ, 1.0.0_SA_CTO ruling @5f3b4a20c6 (msg 99036)

`wk-nfra_mcpindex-1-1d` (head `119a49eef0`, ONE commit not on origin/CLOUD, its worktree already removed) is HELD
by ruling: it changes what the live Gateway serves (`read_teams_attachment`) ahead of both its gates, and a release
cut from CLOUD carries everything on CLOUD. **Do NOT drain, merge or "clean up" this branch to make a count look
clean.** Its commit is preserved on origin as tag `backup-20260921/wk-nfra_mcpindex-1-1d` (a tag lands nothing on
CLOUD; verified NOT an ancestor of origin/CLOUD). /cleanup's merged-worktree pool will not touch it (no worktree,
and it is unmerged); the hazard is a hand merge. It is released only by 1.0.0_SA_CTO or Andrew.
