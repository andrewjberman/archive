# DSGN_IRPTV1.TO-IV-e-81 -- search is search only: result

**Base:** portal DEV `7b4f4f83` (previous order TO-IV-e-80, merged). **Commit:** `7689c526`, LOCAL on
`wk-DSGN_IRPTV1-42-portal`.

## Build

`portal/src/pages/InvestorReporting/header/ClientSearch.tsx`: removed the `import { BrowseDrawer } from
'./BrowseDrawer'` line, the `IV-e-8` mount comment, and the `<BrowseDrawer api={api} scope={scope}
contexts={contexts} onSelectionChange={onSelectionChange} />` line. `api` remains used (`api.browseDirectory`
in the debounced fetch effect); `scope`, `contexts`, `onSelectionChange` remain used elsewhere in the same
file. No other edit made to the file.

`portal/src/pages/InvestorReporting/header/BrowseDrawer.tsx`: **left in place and unedited.** Not dead code --
still imported directly (never through `ClientSearch`) by five test files: `iv-e-8.browse-drawer.test.ts`,
`iv-e-8.selection-path.test.ts`, `iv-e-9.picker-adoption.test.ts`, `iv-e-33.client-words.test.tsx`,
`iv-e-56.firm-display.test.tsx`. None of them render it through `ClientSearch`, so removing the mount there
broke none of them (confirmed: not in the five-failure set of two full IR-suite runs, both below).

## Re-goldened tests

**New:** `portal/src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-101.search-only.test.tsx` --
renders the header through `SelectionWorkspace` in its global empty state exactly as
`iv-e-38.header-identity.test.tsx`'s `renderGlobalEmptyState` does, asserts no
`data-slot="browse-trigger"`, no `data-slot="browse-drawer-root"`, no button whose text is `"Browse"`, plus
the CONTROL (`data-slot="search-select-input"` present, `searchSelectShouldOpen('')` and `('   ')` false,
`('an')` true).

**No pre-existing test needed re-goldening.** A denominator search (`comp-find "BrowseDrawer"` /
`"browse-trigger"` / `"browse-drawer-root"` over `src/pages/InvestorReporting`) found `data-slot="browse-
trigger"` and `data-slot="browse-drawer-root"` occur ONLY in `BrowseDrawer.tsx` itself -- no existing test
asserted either slot's presence, and `iv-e-9.picker-adoption.test.ts` (which renders `ClientSearch` via
`renderToStaticMarkup`) asserts only `search-select-root`, never anything Browse-shaped. Both full-suite
runs below confirm: the failing set is identical to, and no larger than, the known five named in the task
order.

## IVE81-AC1

```
cd C:/tmp/wk-dsgn_irptv1-10-42/portal && timeout 120 /c/Users/AndrewBerman/.bun/bin/bun test ./src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-101.search-only.test.tsx 2>&1 | tail -12
```
```
AD-11: no browse-trigger slot=true; no browse-drawer-root slot=true; no button text "Browse"=true
CONTROL: search input present=true; shouldOpen('')=false; shouldOpen('   ')=false; shouldOpen('an')=true
VERDICT: SEARCH-ONLY-OK

 1 pass
 0 fail
 8 expect() calls
Ran 1 test across 1 file.
```

## IVE81-AC2

Two full runs at commit `7689c526` (base `ClientSearch.tsx` state, after mutant revert -- see controls below).
Both: **919 pass / 27 skip / 5 fail**, 951 tests across 282 files, IDENTICAL failing set both times:

- `fixture set > the smoke map covers every scoped route, one entry each` (`fe-s-1/fixtures.test.ts`)
- `source bounds > neither source carries any forbidden token` (`fe-s-1/source-bounds.test.ts`)
- `F25-AC2 -- ABSENT and NULL are two different things on the page > on every no-answer state the two render
  differently, on the path the tabs render` (`fe-s-25/absent-vs-null.test.ts`)
- `F25-AC2 -- ABSENT and NULL are two different things on the page > the two renderings are the RIGHT two,
  and the fact survives on the view document alone` (`fe-s-25/absent-vs-null.test.ts`)
- `F25-AC3 -- \`?? null\` is refused wherever the contract distinguishes > the scan finds none, and the scan
  can fire` (`fe-s-25/absent-vs-null.test.ts`)

These are exactly the "known five" named in the task order -- pre-existing, out of this cell's grant.
No process-spawning test was cut at its time cap under load in either run; no isolated re-run was needed.
`src/pages/InvestorReporting/contracts/wire/*` (rewritten by the run) restored via `git checkout --` after
each run and never committed.

## Controls

**Mutant:** re-inserted the `BrowseDrawer` import + mount into `ClientSearch.tsx` (in-worktree only).
IVE81-AC1 re-run: `VERDICT: SEARCH-ONLY-FAIL -- AD-11: data-slot="browse-trigger" still rendered; AD-11:
data-slot="browse-drawer-root" still rendered; AD-11: a button whose text is "Browse" is still rendered` (1
fail). Reverted from a pre-mutant backup (`cp`); `diff` against the backup came back empty, confirming an
exact restore. Re-ran IVE81-AC1: `VERDICT: SEARCH-ONLY-OK`, identical to the pre-mutant read. FIRED-AS-
EXPECTED.

**Determinism:** IVE81-AC1 run 3 times (base, post-mutant, post-revert) -- stable and mutation-sensitive (OK,
FAIL, OK). IVE81-AC2 (the full IR suite) run twice in immediate succession at the same commit, restoring
`contracts/wire/*` after each -- both runs read 919 pass / 27 skip / 5 fail with the identical five (file,
test) pairs failing both times. STABLE.

## Declared exclusions

- The five pre-existing IR-suite failures (fixture set smoke map, source bounds, F25-AC2 x2, F25-AC3): named
  in the task order itself as "the known five" -- pre-existing, out of this cell's grant, confirmed unchanged
  across two runs.
- No other test file's assertions needed re-goldening (see denominator search above).

## Surprises

None filed for this cell.
