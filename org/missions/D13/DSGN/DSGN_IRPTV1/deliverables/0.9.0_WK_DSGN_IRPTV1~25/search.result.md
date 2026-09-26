# DSGN_IRPTV1.TO-IV-e-37.search -- result log (0.9.0_WK_DSGN_IRPTV1~25)

Cell `IV-e-37`, O1 search: UIR-01, 02, 04, 06, 07r, 08, 09, 10, 11.

## What changed (portal, commit d6e6eda3 on `wk-DSGN_IRPTV1-25-portal`, base DEV `fdccc6e6`)

- `src/components/ui/SearchSelect.tsx`
  - New exported pure function `searchSelectShouldOpen(query)` -- the list opens only for
    non-empty (trimmed) typed text. `onFocus` and `handleInput` both gate on it (UIR-01); an
    ArrowDown/ArrowUp on an empty box no longer opens either.
  - The option list's z-index moved from a raw `z-10` to `Z_INDEX.dropdown` (`z-50`, imported
    from `@/lib/designTokens`), above `TabNavigation`'s own `Z_INDEX.navigation` (`z-40`)
    (UIR-02/UIR-08).
  - The option row layout split into a stable two-line slot: the label owns its own
    full-width line (free to wrap), and a new `data-slot="search-select-option-meta"` wrapper
    holds detail+tag in a FIXED slot present on every row (UIR-04's "laid out the same on
    every row").
  - `spellCheck={false}` added to the input (UIR-09).
  - New optional `resultSummary` prop, rendered as a caption above the rows when supplied
    (UIR-10).
- `src/pages/InvestorReporting/header/ClientSearch.tsx`
  - `toSearchSelectOption`'s `tag` is never omitted: `row.firmName ?? FIRM_TAG_FALLBACK`
    (`'Firm unavailable'`) -- every option now carries a firm marker (UIR-04).
  - New exported `globalResultSummary(scopeCount, query, rowCount)` -- a matched-count
    caption in Global mode (more than one resolved firm scope) once text is typed and at
    least one row matched; wired into `SearchSelect`'s new `resultSummary` prop (UIR-10).
  - `onQuery` no longer calls `onSelectionChange?.(null, null)` on every keystroke -- ROOT
    CAUSE of UIR-11: that call told `index.tsx`'s `select()` to drop an already-accepted
    selection the instant a viewer began typing a NEW search, which swapped
    Performance/Holdings straight into `SampleView`'s pre-selection Sample content
    (`TabShell.tsx`'s own `!scopeRef` gate, unchanged) while a real client's report was
    already on screen. The header now holds the last ACCEPTED selection until a new option
    is actually picked (`handleSelect`, unchanged).
- New test: `src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-37.search.test.tsx` --
  one named arm per UIR row, `VERDICT: SEARCH-OK`.

Not touched: `header/search.ts`, `header/BrowseDrawer.tsx`, `tabs/SampleView.tsx`,
`tabs/TabShell.tsx` (all in-grant, read for context; no code change needed in any of them --
`toOptions`/`toOptionRow` already preserve served order (UIR-07r) and never sort; `SampleView`
already marks every number Sample + disclosed (UIR-06); `TabShell`'s own `!scopeRef` gate was
already correct once the ROOT-CAUSE keystroke bug in `ClientSearch.tsx` stopped tripping it).

## Verification

- `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-37.search.test.tsx`:
  1 pass / 0 fail, `VERDICT: SEARCH-OK` (run twice, identical).
- Mutant: `searchSelectShouldOpen` body replaced with `return true` (python edit) -- re-ran
  the same invocation: `VERDICT: SEARCH-FAIL UIR-01: searchSelectShouldOpen opens for an
  empty/whitespace query`. File restored from a saved copy; `git diff --stat` printed nothing
  afterward; re-ran clean, twice, identical `VERDICT: SEARCH-OK`.
- `bun run typecheck` (tsc -b --noEmit, whole portal): 0 errors.
- `bunx eslint` on the three touched files: 0 errors, 8 pre-existing-class warnings (the
  `react-refresh/only-export-components` warning already applied to `SearchSelect.tsx`
  before this cell, which already exported `filterSearchOptions`/`emitSelection`/
  `handleSearchSelectKeyDown` alongside the component; one pre-existing
  `react-hooks/set-state-in-effect` warning at `ClientSearch.tsx:100`, unrelated to and
  predating this cell's edits).
- No-regression sweep: `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` --
  96 pass / 0 fail, 487 expect() calls, 96 tests across 82 files (one run showed a transient
  95/1 flake unrelated to the files this cell touches, not reproduced on a clean re-run;
  not filed as a surprise since it never implicated SearchSelect.tsx/ClientSearch.tsx and did
  not reproduce).

## Surprise row filed

`DSGN_IRPTV1-W25-S1` (INVESTIGATION_v1.md): the cell's own "Where it lives" map names only
`tabs/SampleView.tsx`/`tabs/TabShell.tsx` for UIR-06/UIR-11, but UIR-11's actual root cause is
`ClientSearch.tsx`'s `onQuery` handler (in-grant, no BOUNDS issue); and UIR-10 was satisfied by
a new `resultSummary` caption rather than by literally reusing `BrowseDrawer`'s group-by-firm
functions (which operate over a materially different, paginated-groups shape). Both dismissed
with reason -- the deviation is documentation, not defect; criterion passes mechanically.
