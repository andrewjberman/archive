# d503 receipt -- IRPT_ANLREQ worktrees on dell2, measured then removed (0.0.0_AB_MSTR~DELL2, 2026-10-13 ~15:2xZ)

Authority: laptop 1.0.0_SA_CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_D503_IRPT_ANLREQ_WORKTREES_MERGED_ARE_FORCE_REMOVED_ON_STANDING_WORD_20261013.md`
@8e2b5a0609 (relay: laptop msg 108785), on Andrew's 2026-10-08 standing word for merged worktrees.

Measure per worktree: HEAD contained in the trunk (`merge-base --is-ancestor`; workspace trunk `box/dell2`, portal trunk
`origin/DEV`), tracked changes (`status --porcelain --untracked-files=no`), untracked count. The named top-level folders
wk56/61/64/65/66 are containers; the git worktrees are their sub-folders.

| # | path | HEAD | merged | tracked dirty | untracked | verdict |
|---|---|---|---|---|---|---|
| 1 | C:/dev/wk56-release/holds-only + /patch (detached) | 5d8b0390ed | YES | 1 each | 0 | STAYS (dirty); owner 2.0.0_SA_COO~Y2 |
| 2 | C:/dev/wk61-release/base (detached) | 5d8b0390ed | YES | 0 | 0 | REMOVED (worktree remove --force; empty container rmdir) |
| 3 | C:/dev/wk64-release/base (detached) | 4067c2dd5b | YES | 0 | 0 | REMOVED (same) |
| 4 | C:/dev/wk65-control/base (detached) | c5950e99c6 | YES | 0 | 0 | REMOVED (same) |
| 5 | C:/dev/wk66-release/base (detached) | 5d8b0390ed | YES | 1 | 0 | STAYS (dirty); owner 2.0.0_SA_COO~Y2 |
| 6 | C:/dev/wk-portal-63 (portal, branch wk-IRPT_ANLREQ-63-portal) | f644605182 | YES (origin/DEV) | 0 | 0 | REMOVED; branch -d (was f6446051) |
| 7 | C:/dev/wk-portal-63-base (portal, detached) | e50a1379d6 | YES (origin/DEV) | 0 | 0 | REMOVED |
| 8 | C:/dev/irpt-release-r19 | n/a | n/a | n/a | n/a | STAYS: not a git worktree (release package, install/rollback scripts, extract_check/); owner names what it is (ruling item 4) |

Removed 5 worktrees (3 workspace, 2 portal) and 1 portal branch; 3 workspace worktrees stay dirty for COO~Y2; 1 non-worktree path
stays for its owner. Worker `.scratch` folders: none inside the removed trees beyond what `worktree remove` took with them.
After: `worktree prune` on both repos; each removed path reads GONE.
