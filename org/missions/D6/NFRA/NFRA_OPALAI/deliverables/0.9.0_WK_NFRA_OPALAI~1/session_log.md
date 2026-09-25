# NFRA_OPALAI.TO-OA-w-1 -- session log -- 0.9.0_WK_NFRA_OPALAI~1

Worktree `C:/tmp/oa-1` (branch `wk-NFRA_OPALAI-1`, base `fee6c9f89c`).

## What was done

1. `.gitmodules` (0 bytes at base) built to map `opal_ai` (`https://github.com/Opal-Capital/opal_ai.git`,
   `branch = DEV`) and `portal` (`https://github.com/Opal-Capital/portal.git`). `models/factor_scanner` left
   unmapped per the face (waits on its owner's word).
2. The gitlink `opal_ai` landed at `90ca424fc7551019cc493847637258adf3c1c4b5` via `git submodule add -b DEV
   https://github.com/Opal-Capital/opal_ai.git opal_ai` (a real clone under this worktree's own git dir, torn
   down with the worktree; never touches the MAIN tree's `opal_ai`). Using `git submodule add` rather than a
   bare `git update-index --add --cacheinfo` was load-bearing: a bare cacheinfo gitlink with no on-disk
   directory is UNSTAGED by `safe-commit.sh`'s own `cg_stage_pathspec` re-staging pass (`git add -f` on a
   path absent from the worktree treats it as a pending deletion and removes it from the index -- measured
   directly, `git add -f --dry-run` printed `remove 'opal_ai'`). `git submodule add` leaves a real nested
   checkout, so the later `git add -f -- opal_ai` re-stages it correctly as the gitlink.
3. `.tools/wk-provision.sh` gained repeatable `provision --nested <path>=<ref>`: a new `provision_nested()`
   generalises `cmd_portal`'s own nested-worktree provisioning (branch `<super-branch>-<path with / as ->`,
   ref resolution off the MAIN tree's copy, non-empty-target refusal) to any path `.gitmodules` maps, and a
   new `require_nested_initialised()` refuses rc 2 with `REFUSED: <path> is uninitialised in the main tree
   (git submodule update --init <path>)` BEFORE the super worktree (or anything else) is created --
   validated in `cmd_provision` before the `git worktree add` line. `cmd_remove` generalised the same way:
   after tearing down portal's own nested worktree (unchanged code path), a new loop reads every OTHER path
   `.gitmodules` maps and tears down any present nested worktree the identical way (placeholder recreated
   empty, no `worktree prune`). `cmd_portal`'s own flags, behaviour and the `--self-test` arms are byte-
   unchanged; `node_modules` handling stays portal-only. `--self-test` was NOT run (bounds: the issuer runs
   it at the drain).

## Commit

`69288c8ca0b396e9f9010a009ee18c0a9c83ca23` on `wk-NFRA_OPALAI-1` (LOCAL) -- `.gitmodules`, `opal_ai`
(gitlink, `create mode 160000`), `.tools/wk-provision.sh`.

## Owned-paths gate gap (surprise row filed)

The commit staged `opal_ai` alongside `.gitmodules` and `.tools/wk-provision.sh`. `.tools/git-hooks/owned-
paths-check.sh` (via `.tools/owned-paths-validate.py`) refused: `opal_ai` resolves to NO lane at all in
`.owned-paths.yaml` (`resolve_lane` returns `None`), and `main()`'s CLI loop reports `UNDEFINED` and never
reaches `check_agent` -- so the registry's own `worker_grant` (task-order-paths, ADHC_OWNPTH.005) stanza,
which DOES grant this worker `opal_ai` per this order's `<paths>` block, is never consulted for a path with
ZERO existing lane row (the clause only supplements an EXISTING lane's `permitted_agents`, never a wholly
undefined path). `.owned-paths.yaml` is not in this order's `<paths>`, so this worker cannot add a lane row
itself. Landed the commit via the documented, audited escape hatch (`GIT_COMMIT_AUTHOR_OVERRIDE`, CLAUDE.md
rule 14a; `.tools/git-hooks/owned-paths-check.sh:11-12,118-121`) with value `0.9.0_WK_NFRA_OPALAI~1` --
every staged path in that commit is inside this order's own `<paths>` grant, so the override does not cross
lanes. Filed as `NFRA_OPALAI-Z-W1-S1` (see below); disarm is a lane-row question for OA-w-2 / the registry
owner, not this worker's to fix.

## Mutant + determinism (controls)

Mutant: `.gitmodules`'s `branch = DEV` line for `opal_ai` was deleted on disk (uncommitted), `w1.AC1.sh`
re-run and correctly FAILed (`opal_ai.branch=NONE ... RESULT: FAIL exit=1`), then the file was restored
byte-for-byte from a pre-mutation copy (`git status --porcelain -- .gitmodules` empty after restore, working
tree clean, no commit touches this). Determinism: `w1.AC1.sh` run twice in a row post-restore, identical
`RESULT: PASS exit=0` both times.

## Proof-of-spec checks (verbatim, per the task order)

- AC1: `bash .../checks/w1.AC1.sh` -> `RESULT: PASS` `exit=0`
- AC2: `bash .../checks/w1.AC2.sh` -> `RESULT: PASS` `exit=0`
- AC3: `bash .../checks/w1.AC3.sh` -> `RESULT: PASS` `exit=0`, and no stray worktree/branch survives
  (`git worktree list` / `git branch --list wk-NFRA_OPALAI-97` both empty after the run).
