# NFRA_MCPORTAL -- session log, `0.9.0_WK_NFRA_MCPORTAL~1`

## NFRA_MCPORTAL.TO-MP-t-5 (round 1, entitlements + recent-changes pages)

Worktree: `C:/tmp/mp-1`, branch `wk-NFRA_MCPORTAL-1`, HEAD `6267ae1aca`. Nested `mcportal` worktree provisioned at
`--nested mcportal=r1-drain`, branch `wk-NFRA_MCPORTAL-1-mcportal` @ `606f032` (MP-w-1's merged shell), `node_modules`
absent.

### Sequence

1. `bun install` inside `mcportal/` (77 packages, node_modules had not been installed on this fresh nested worktree).
2. Read `infra/aws/ec2/opal-gateway/app/data_entitlement.py:1-90` for the `Scope` shape (masters, datasets, accounts,
   dates, columns, operations) and `portal/DESIGN.md` (C1-C13) for the markup law.
3. `src/api/admin.ts`: typed client for exactly the four fixed routes, same-origin, `credentials: 'include'`; every
   write resolves `{"verdict": "WRITTEN"|"REFUSED", "reason"}`.
4. `src/pages/mcp-server/entitlements/`: split into a fetching container (`Entitlements.tsx`) and a presentational
   view (`EntitlementsView.tsx`) so the view is testable without a DOM -- **no jsdom/happy-dom is installed in this
   shell** (`bun.lock` carries neither; adding one is a `package.json` edit outside this order's `<paths>`), so the
   three named tests are met via `react-dom/server`'s `renderToStaticMarkup` (a string-render, no DOM needed) plus
   the `admin.ts` client directly against a mocked `globalThis.fetch`, rather than a full render+interact cycle.
   Same split for `src/pages/recent-changes/` (`RecentChangesView.tsx` exports `sortNewestFirst`).
5. Tests (`bun test src/pages`): 3 pass, 0 fail, 15 `expect()` calls across 2 files.
6. `git -C mcportal` had no committer identity in this fresh nested worktree (`Committer identity unknown`); set
   `user.email`/`user.name` locally to the worker's own serial (not a `--global` change) before the commit named in
   the Bounds section, which assumes an identity already exists.
7. Committed on `wk-NFRA_MCPORTAL-1-mcportal`: `1eb686a7b95e677f0d813e8029bac912d4aa5ba1` (11 files).
8. Mutant control (AC2, `t5.AC2.sh`): (a) appended `fetch("/api/other/probe")` to `admin.ts` (uncommitted) -- FAILed
   `routes outside /api/admin/=1`, reverted clean (`git checkout -- src/api/admin.ts`); (b) renamed every `widen`
   token to `expand` (uncommitted) -- FAILed `fixed route fragments present 3 of 4`, reverted clean. Both mutants
   confirmed FAIL as expected; restore confirmed PASS both times.
9. Determinism: `t5.AC1.sh` and `t5.AC2.sh` each re-run twice post-restore, byte-identical deciding lines both times
   (only the reporter's timing suffix differs, not read by either checker).
10. `bun run typecheck` (`tsc -b --noEmit`) rc=0; `bun run build` (`tsc -b && vite build`) rc=0, `dist/` gitignored.
11. **Surprise filed** (`NFRA_MCPORTAL-Z-W1-S2`): the task face gives entitlements an explicit sidebar home ("under
    the sidebar's MCP Server entry") but gives recent-changes none, and `src/shell/pages.ts` (the brief's one order
    of truth, read-only per this order's Bounds) enumerates exactly the brief's eight entries with no member for it
    -- the issuer's router hookup has to pick a placement this cell's face and `<paths>` do not decide.
12. Status flip to `complete` is left to the issuer's drain, per the `NFRA_MCPORTAL.TO-MP-w-1` precedent on this
    same slot: this order's own `<paths>` grant does not include `task-orders/`.

### Router hookup owed to the issuer (not in this worker's `<paths>`)

```
import { Entitlements } from './pages/mcp-server/entitlements'
import { RecentChanges } from './pages/recent-changes'
...
<Route path="/mcp-server" element={<Entitlements />} />
<Route path="/recent-changes" element={<RecentChanges />} />
```

`recent-changes` is not a `PAGES` id in `src/shell/pages.ts` (see row `NFRA_MCPORTAL-Z-W1-S2`) -- the issuer decides
whether it gets a new sidebar entry, nests under MCP Server, or stays route-only.

---

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
