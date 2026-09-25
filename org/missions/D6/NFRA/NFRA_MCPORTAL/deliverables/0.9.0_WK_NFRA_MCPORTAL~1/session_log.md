# NFRA_MCPORTAL.TO-MP-w-1 -- session log, `0.9.0_WK_NFRA_MCPORTAL~1`

Worktree: `C:/tmp/mp-1`, branch `wk-NFRA_MCPORTAL-1`, based `b99ab96fdf`.

## Sequence

1. Grounded premises: `mcportal` remote reachable (`git ls-remote`), `DEV`=`PROD`=`fa1ff9693b0868c29c8ff421d403449db8a1ee39`
   (matches the task order's stated cut). `portal` and `opal_ai` submodules were uninitialised in this worktree;
   initialised `portal` to read `portal/DESIGN.md`.
2. Read the brief at pin `8d1f5c362b` and copied Andrew's verbatim sidebar order into `src/shell/pages.ts`
   (the sidebar's single source of truth, imported by both the sidebar component and its test):
   Home, Operations Report, User Management, User Analytics, MCP Server, Health Check, Cost Management, Infosec.
3. `.gitmodules`: added the `mcportal` submodule entry beside `opal_ai`/`portal`, byte-unchanged, via
   `git submodule add -b DEV https://github.com/Opal-Capital/mcportal.git mcportal` (landed the gitlink at
   `fa1ff9693b0868c29c8ff421d403449db8a1ee39` as declared).
4. Nested `mcportal`: scaffolded a React 19 + Vite 7 + TypeScript 5.9 shell on bun (package.json `build`/`test`
   scripts), styled from `portal/DESIGN.md`'s C1/C3/C8 clauses (Lato, the four surface roles, the one indigo
   action). `bun install` ran inside `mcportal/` only. Committed on branch `wk-NFRA_MCPORTAL-1-mcportal`
   inside the submodule's own git dir.
5. **Surprise filed** (`NFRA_MCPORTAL-Z-W1-S1`): `.tools/owned-paths-validate.py`'s `--check-agent` CLI resolves
   `resolve_lane()` before ever consulting the ADHC_OWNPTH.005 task-order-paths worker grant, so a path absent
   from `.owned-paths.yaml` (here, the brand-new `mcportal` path this very task order's `<paths>` names) is
   refused `UNDEFINED` and the grant clause never runs -- reproduced live, matches the sibling project's
   `NFRA_OPALAI-Z-W1-S1` finding on the same mechanism. Worked around via the documented, audited
   `GIT_COMMIT_AUTHOR_OVERRIDE` escape hatch (CLAUDE.md 14a), not by editing the gate (out of this order's
   `<paths>`).
6. **Self-caught defect**: `git commit -- mcportal` re-reads the submodule's CURRENT checked-out HEAD before
   committing (a tracked pathspec re-stages from the working tree), so the first parent commit
   (`cdf2292d84`) landed the gitlink at my nested branch's tip (`859c68f5a3`) instead of the required
   `fa1ff9693b`. Fixed in a new commit (`bac884039f`): detached the submodule to `fa1ff9693b`, re-ran
   safe-commit so `git add -f` picked up the correct SHA, then switched the submodule back to
   `wk-NFRA_MCPORTAL-1-mcportal` (a working-directory operation only -- the branch and its commits were
   never at risk). Verified post-fix: `git ls-files -s mcportal` == `160000 fa1ff9693b... mcportal`.
7. AC3 (`bun test`) initially FAILed on `named test lines=0`: bun's default reporter prints a test's name only
   on FAILURE (measured against bun 1.3.14 with a deliberately-failing dummy test); a passing run emits only
   the summary counts. Added a `console.log` of the exact test name inside the test body (nested commit
   `606f032`) so the run self-reports either way; the assertion itself is unchanged.
8. Ran the mutant control on AC3: swapped `Operations Report`/`User Management` in `pages.ts` (uncommitted) --
   AC3 correctly FAILed (`named test lines=4; fail=1`); restored byte-identical (`git status --short` clean)
   and AC3 PASSed again, twice, with identical output both times.
9. All three criteria PASS at HEAD `bac884039f` / nested `606f032`.

## Final state

- Parent gitlink: `mcportal` @ `fa1ff9693b0868c29c8ff421d403449db8a1ee39` (pinned, per the task order's bound;
  the issuer bumps it once the nested branch reaches the remote).
- Nested branch `wk-NFRA_MCPORTAL-1-mcportal` @ `606f032abdbdfbb71669afcde1aa985213acad5e`, 2 commits ahead of
  `fa1ff9693b` (README-only).
