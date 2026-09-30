# session log -- 0.9.0_WK_NFRA_OPALAI~17 on OA-e-11
- Resolution: committing worktree's `git rev-parse --git-common-dir` (absolute) must sit under `.git/modules/` or `.git/worktrees/*/modules/`; the superproject is asked of that gitdir's `core.worktree` checkout (`--show-superproject-working-tree`). Never `git worktree list`.
- No superproject for a submodule: exit 1, message "superproject could not be resolved -- refusing the commit (fail closed; the lane check is never skipped)".
- Negative control: the test run against HEAD~ bytes of both scripts: 5 passed, 4 failed (arm1 landed, arm6 landed).
- Row NFRA_OPALAI-Z-W17-S1 (ARMED, disarm_owner 2.0.0_SA_COO~AI): installer is a no-op against the already-installed old wrapper.
