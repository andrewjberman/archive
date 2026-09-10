# IRPT_FNTEND.TO-FE-s-2 -- result (0.9.0_WK_IRPT_FNTEND~1)

**Cell `FE-s-2`: the route, the page shell, the header with the firm dropdown and the client search.**
Nine criteria: eight mechanical, all PASS by output; one (`F2-AC7`) is judgment and is RECORDED with no
verdict for `3.0.0_SA_CVO` at L9.

- Portal commit **75fbfc982e8cb81da5a338cc39b666283763a364** -- LOCAL on branch `wk-irpt_fntend-1-2-fe-s-2`
  of the PORTAL repo (13 files, +1301 / -6). Never pushed.
- Workspace commit **44887f7b93** (the two surprise rows) -- LOCAL on the same branch name in the
  WORKSPACE repo. The proof, the three PNGs and the `<status>` flip ride the workspace commit after it.
- Proof of spec: `IRPT_FNTEND.TO-FE-s-2.route-shell-header-search.proof_of_spec.json`,
  `proof-of-spec-check.py` **rc=0 (VALID)**.

---

## WHAT WAS BUILT

| Path (portal repo) | What it is |
|---|---|
| `src/App.tsx` | three added lines, zero removed: lazy import, nav entry, route |
| `src/pages/InvestorReporting/index.tsx` | the page shell; one react-query query (`resolve-scope`), key built by `irKey` |
| `src/pages/InvestorReporting/header/search.ts` | the pure search + selection logic and the debounce, no React |
| `src/pages/InvestorReporting/header/firm.ts` | the pure firm-catalogue logic, no React |
| `src/pages/InvestorReporting/header/FirmDropdown.tsx` | `PageSurfaceControl as="dropdown"`, hidden below two firms |
| `src/pages/InvestorReporting/header/ClientSearch.tsx` | the catalyst `Combobox` over the shaped rows |
| `src/pages/InvestorReporting/header/ScopeSummary.tsx` | selection, permitted-account count with its denominator, dates, cohort controls |
| `src/pages/InvestorReporting/fixtures/smoke/fe-s-2-{default,one-firm}.json` | the two ui-smoke fixture maps |
| `src/pages/InvestorReporting/__tests__/fe-s-2/{search,dropdown,app-diff}.test.ts` | 13 tests, 0 fail |
| `src/pages/InvestorReporting/__tests__/fe-s-1/node-builtins.d.ts` | the ordered shim collision removal |

### Three decisions worth reading

1. **The nav entry reuses the already-imported `FileText` icon.** Importing a new lucide glyph would
   have made the icon import block a FOURTH changed hunk in `App.tsx`, which `F2-AC6` refuses and the
   cell forbids ("no other line of `App.tsx` changes"). `NAV_ICONS` is a path-to-icon map, so two entries
   may share a glyph; the labels are what distinguish them.
2. **The pure logic is split into two modules, `search.ts` and `firm.ts`.** The order names `search.ts`
   by path; `firm.ts` is the same move applied to the dropdown, so `F2-AC3` grades the OPTION LIST
   rather than a rendered `<select>`. `FirmDropdown.tsx` is still the control the order names -- it
   renders `PageSurfaceControl` and delegates the list.
3. **The client search does NOT go through react-query.** Its input is a human-typed name and a name
   never enters a cache key (FE-s-1's `irKey` rule). It calls the typed client directly through
   `DirectorySearchRunner`, whose clock is an ARGUMENT -- which is what lets the 25-keystroke arm run
   with no timers and no flake.

---

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| F2-AC1 | PASS-by-output | `rc=0` (and `FORCED rc=0` on a cache-defeating second run) | 1 of 1 project, 0 diagnostics |
| F2-AC2 | PASS-by-output | `7 pass / 0 fail` | 7 of 7 tests, 97 expects; call log 26 of 26 on `directory-search`, 0 of 26 on the other 10 operations |
| F2-AC3 | PASS-by-output | `5 pass / 0 fail` | 5 of 5 tests; options 3 of 3; visibility 4 of 4 cases |
| F2-AC4 | PASS-by-output | `LOC : /investor-reporting`, `rc=0` | 1 of 1 capture, 1 of 1 fixture matched, 0 crashes |
| F2-AC5 | PASS-by-output | `LOC : /investor-reporting`, `rc=0` | 1 of 1 capture at 390 |
| F2-AC6 | PASS-by-output | `1 file(s), 3 hunk(s), 3 added line(s), 0 removed line(s)` | 3 of 3 hunks, each matched to the clause that ordered it |
| F2-AC7 | RECORDED (judgment) | see below -- NO VERDICT TAKEN | 3 of 3 captures read; 4 of 4 controls measured by computed style |
| F2-AC8 | PASS-by-output | `DIRENT_NAME=False` (parent blob: `PARENT_BLOB_BYTES=967 DIRENT_NAME=True`) | 1 of 1 shim file |
| F2-AC9 | PASS-by-output | `46 pass / 0 fail` | 46 of 46 tests across 5 of 5 fe-s-1 files -- the same 46 FE-s-1 recorded |

### F2-AC7 -- recorded, not graded

The two PNGs the CVO grades are in this folder. What they show, and one thing measured rather than
eyeballed:

- **1440.** The portal's own header (split-weight title, indigo accent bar), the actions slot carrying
  `Firm: Global (All)` and the search box, the scope strip as a light `Panel` with dark text, and
  `Investor Reporting` in the Insights nav. The tab area is empty by design (FE-s-3's).
- **390.** Title, description and scope strip re-flow. The header ACTIONS do not: `PageHeaderCleanBadge`
  lays actions out as a `shrink-0` flex item beside the title, so the firm control is clipped at the
  right edge and the search box is off-screen. That component is IMPORTED-never-edited by this order and
  the criterion asks only that the route render, so nothing was worked around -- it is stated here so the
  grader does not have to discover it.
- **Colour law, MEASURED.** Canvas `rgb(195, 202, 218)`. The `<select>` the order specifies computes
  `background-color: rgba(0, 0, 0, 0)` with `color: rgb(255, 255, 255)` -- white on silver, ~1.35:1.
  The same control computes the identical pair on its OWN demo route `/dev/page-surface-control`, which
  this cell does not touch, while the button and toggle-group branches compute `rgb(96, 60, 226)`.
  Filed as **IRPT_FNTEND-W1-S4**, ARMED, `disarm_owner 2.0.0_SA_COO~F`. Everything this cell authored is
  dark-on-light on the canvas.

---

## CONTROLS

**Mutants -- three, one per mechanically-graded family, each restored from a byte copy.**

| # | mutation | expected | observed |
|---|---|---|---|
| 1 | deleted the nav-entry line from `App.tsx` and regenerated `.scratch/app.diff` | `app-diff` fails on the count | `0 pass / 1 fail`, `Expected length: 3 / Received length: 2` |
| 2 | removed `GLOBAL_FIRM_OPTION` from `firmOptions()` | `dropdown` fails the list arms | `3 pass / 2 fail` (option-list and locked-firm arms) |
| 3 | made `toOptions()` filter out terminated and unmapped rows | `search` fails the terminated and unmapped arms | `5 pass / 2 fail`, with `CALL-LOG: 26 ... 0 outside` still printed |

Three mutants, three DIFFERENT failing arms -- not one shared assertion. After restoration:
`git status --porcelain` in the portal worktree prints nothing, `bun test .../fe-s-2` is `13 pass / 0 fail`,
`bun run typecheck` is `rc=0`.

**Determinism.** Each fe-s-2 file run twice: 3 of 3 IDENTICAL apart from the wall-clock duration line
(the raw diff showed exactly that one line per file). ui-smoke printed the same `LOC`, `CANVAS` and
`FIXTURES` lines on both runs at both widths. No test reads a clock it does not control.

---

## SURPRISES

- **IRPT_FNTEND-W1-S3** (OBSERVATION, INERT) -- the order names `PageThemeProvider` as an export of
  `portal/src/components/PageHeaderVariants.tsx`; it is defined in `portal/src/contexts/PageThemeContext.tsx:12`
  and imported from there by all 15 portal pages that use it, including this one. Form only.
- **IRPT_FNTEND-W1-S4** (OBSERVATION, ARMED, `disarm_owner 2.0.0_SA_COO~F`) -- `PageSurfaceControl`'s
  `as="dropdown"` shape renders white text on a transparent background on the silver canvas, on its own
  demo route as well as here. The control is on this order's do-not-edit list; no local override was
  taken, because one would have hidden the defect on the page that measured it.

Both rows are appends: the three pre-existing rows are byte-identical and the row gate confirmed it
(`2 new row(s) of 5 total checked (3 pre-existing, NOT re-graded)`).

## WHAT THIS CELL DID NOT DO

The tab shell and every tab (FE-s-3's); any live call to `/api/scoped/investor-reporting/*` (the routes
do not exist -- IRPT_BCKEND B15); any edit to a reused component; any change to `tsconfig.app.json`; any
push, merge or rebase. Full list with reasons in `declared_exclusions` of the proof instance.
