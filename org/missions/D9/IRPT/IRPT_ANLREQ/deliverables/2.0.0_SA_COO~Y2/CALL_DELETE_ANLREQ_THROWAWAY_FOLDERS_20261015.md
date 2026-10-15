# Call: recursive deletion of IRPT_ANLREQ throwaway folders (2.0.0_SA_COO~Y2, dell2, 2026-10-15)

CLAUDE.md: recursive deletion needs Andrew's word. Nothing below has been deleted. Measured 2026-10-15 ~05:00Z.

## Delete NOW (nothing waits on them)

Registered worktrees, branch merged into box/dell2 (git branch --merged), tree clean:
- C:/dev/wk-irpt-anlreq-120 (branch wk-IRPT_ANLREQ-120)
- C:/dev/wk-irpt-anlreq-122 (branch wk-IRPT_ANLREQ-122)
- C:/dev/wk-irpt-anlreq-74 (branch merged; ONE tracked record modified in the tree: r22/PORTAL_FILE_NAME_CANDIDATE.json, the committed copy is on the branch)

Unregistered plain folders (not worktrees, 139 is 179 MB): C:/dev/wk-irpt-anlreq-139, C:/dev/wk-irpt-anlreq-140.

Release build worktrees, detached heads both contained in box/dell2 (git branch --contains):
- C:/dev/irpt-release-r30 (10901 MB, head 0c0ae5a8f5)
- C:/dev/irpt-release-r29b (head 4279513f95)

Stray tree: C:/c/dev (a mis-rooted path; contents listed by `ls -d /c/c/dev`).

Inside C:/dev/irpt-release-r31s (8992 MB): scratch, build-1, build-2, tmp-control-15a, tmp-control-d398, tmp-control-d398b, tmp-status, wt-control-15a387dd36, wt-control-d39886e4aa, wt-status-e008b6216a, live-read-145.

Each registered worktree is removed with `git worktree remove --force` then the folder; the branch ref stays.

## KEEP (not in this call)

- C:/dev/irpt-release-r31s/irpt-status-r31.zip and C:/dev/irpt-release-r31/ tarball + scripts: until legs L and R are applied.
- C:/dev/irpt-release-r29: rollback for the resident.
- C:/dev/wk-irpt-anlreq-102 (branch wk-IRPT_ANLREQ-102): 6 uncommitted code/test files of the firm-scoped ticket LIST (AR-y-281, rows W108-S3, S6) and commits not in box/dell2. Not mine to delete without a ruling; a separate card.
- C:/dev/rel-anlreq-r4 (branch rel-anlreq-r4): IRPT_YCDGEN seat ~G2's resident build, commit eb72753aad not in box/dell2. Another seat's.

## After the windows

The rest of irpt-release-r31 and r31s (zip, tarball, scripts) once both legs are applied and the FWD-1 run closes.
