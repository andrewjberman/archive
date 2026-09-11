# IRPT_FNTEND.TO-FE-s-10 -- the Global view -- result

Worker: `0.9.0_WK_IRPT_FNTEND~1`. Branches: workspace
`wk-irpt_fntend-1-6-fe-s-10` (HEAD at TO start `d1479bc5f0`); portal
`wk-irpt_fntend-1-6-fe-s-10` (HEAD at TO start `164c1b1a`, committed to
`3f055080` in this session).

## What was built

- `global/firms.ts` -- pure catalogue validation: `resolveFirmSelection` (the
  ONE rule a URL parameter, a persisted selection or a forced selector value
  all resolve through -- a one-firm catalogue can never yield `global`),
  `admitsGlobal`, `catalogueFirmIds`, `findPermittedFirm`, `firmDisplayName`.
  `GLOBAL_FIRM_OPTION` / `DEFAULT_FIRM_ID` are imported from `header/firm.ts`
  (FE-s-2), never redefined.
- `global/useFirmContext.ts` -- validates the dropdown's `value`/`onChange`
  pair against `resolveFirmSelection` on load (URL param, then persisted
  selection, then the caller's own value) and on every `scope` change.
- `global/FirmAttribution.tsx` -- a pure presentational lookup: a result's
  own `scope.firmId`/`tenant` against `ResolvedScope.permittedFirms`, never
  the header's current selection.
- `header/FirmDropdown.tsx` -- writes the selection through `useFirmContext`.
- `header/search.ts` / `header/ClientSearch.tsx` -- `toOptionRow`/`toOptions`/
  `DirectorySearchRunner` gain an OPTIONAL `permittedFirms` parameter; every
  `SearchOptionRow` carries `firmName` (null when no catalogue is supplied).
  No second `directory-search` call is added -- the existing single-call
  architecture already spans the catalogue whenever the resolved scope is
  Global; this only adds the display lookup.
- `state/selection.ts` -- `switchFirm(next)`, sharing `switchScope`'s
  synchronous clear-then-adopt implementation (extracted into one internal
  `adopt()`).
- `state/hooks.ts` -- SURPRISE FIX (row `IRPT_FNTEND-W1-S9`): all three
  `useSyncExternalStore` calls gained a third (server-snapshot) argument
  identical to the client one, so `TabShell` can be rendered via
  `renderToStaticMarkup` at all.
- `tabs/TabShell.tsx` -- `analysis` now mounts `AnalysisTab`, `holdings` now
  mounts `HoldingsTab` (amended at the FE-s-6 drain, row
  `IRPT_FNTEND-W3-S1`); `reporting` unchanged. Test-only seeds `initialTab` /
  `initialHoldingsSnapshot` / `initialHoldingsEnvelope` /
  `initialAnalysisRequests` / `initialAnalysisReport`.
- `tabs/analysis/AnalysisTab.tsx`, `tabs/holdings/HoldingsTab.tsx`,
  `tabs/reporting/ReportingTab.tsx`, `export/Preview.tsx` -- each mounts
  `FirmAttribution` beside its own result header (`AnalysisTab` also beside
  `InputReview`, the review panel); each gains the optional `scope` prop (or,
  for `AnalysisTab`, already had it) needed for the catalogue lookup.
- `fixtures/fe-s-10/` -- `scope.two-firms.json` (49financial + cottonwood,
  Global/unnarrowed), `scope.one-firm.json` (49financial only, DELIBERATELY
  carrying a different displayName for 49financial than the two-firm scope,
  so the parity test's stripping logic is actually exercised),
  `directory.two-firms.json` (3 entries spanning both firms, including
  client X), `performance.clientX.rev7.json` (rev-7).
- `fixtures/smoke/fe-s-10-{global,one-firm}.json`; six test files under
  `__tests__/fe-s-10/`.
- `__tests__/fe-s-4/analysis-no-narrative.test.ts` -- the FE-s-9-drain
  amendment: the positive-control case now spreads
  `renderOptions: { ...bundle.renderOptions, includeNarrative: true }`.

## Two surprises

- `IRPT_FNTEND-W1-S9` (INERT): F10-AC10 required rendering `TabShell` via
  `renderToStaticMarkup`; `state/hooks.ts`'s `useSyncExternalStore` calls
  (FE-s-3) had no server-snapshot argument, which React THROWS on under any
  SSR-style render. Fixed inside `state/` (granted) but beyond the one named
  seam (`state/selection.ts`'s `switchFirm`) -- the fix is additive and
  backward-compatible; the full suite is unaffected on the client plane.
- `IRPT_FNTEND-W1-S10` (INERT): F10-AC8's ui-smoke run for a firm session
  prints `LOC /market`, matching the WORKER FACE's anticipated
  "DID NOT LAND" but not its stated cause (a query-string artifact).
  Reproduced identically with the query string removed, isolating the real
  cause to `portal/src/lib/firmAccess.ts`'s `FIRM_ALLOWED_PATHS` matrix,
  which lists `/investor-reporting` for no partner firm yet -- outside every
  IRPT_FNTEND cell's `<paths>` to date, independent of Global mode. The
  criterion's mechanical bar (`rc=0`) is met; the PNG is exactly what a firm
  session gets today.

## Verification

- `bun run typecheck`: rc=0, twice.
- `bun test src/pages/InvestorReporting/__tests__/fe-s-10/catalogue.test.ts`:
  15 pass, 0 fail.
- `.../search.test.ts`: 4 pass, 0 fail (`SEARCH ROWS: 3 of 3 entries, firms
  present: 49 Financial, Cottonwood`).
- `.../switch.test.ts`: 3 pass, 0 fail (`ADAPTER CALL LOG (switchFirm): 1
  entry, logged AFTER the synchronous clear`).
- `.../parity.test.ts`: 2 pass, 0 fail (`PARITY: identical`).
- `.../source-bounds.test.ts`: 6 pass, 0 fail (arithmetic scan and firmId
  assignment scan both 12 of 12 files clean).
- `.../tabs-mounted.test.ts`: 5 pass, 0 fail (`ANALYSIS MOUNT: AnalysisTab
  root present`, `HOLDINGS MOUNT: HoldingsTab root present`).
- Full `bun test src/pages/InvestorReporting`: 236 pass, 1 skip
  (pre-existing, unrelated), 0 fail, 1137 `expect()` calls, 237 tests across
  46 files -- re-run twice, byte-identical.
- Mutation control: `global/firms.ts`'s one-firm-catalogue branch disabled;
  `catalogue.test.ts` failed 4 of 15 as expected (`Received: "global"` where
  `"49financial"` was required); reverted from a pre-mutation copy, `diff`
  confirmed byte-identical; full suite re-passed 236/1/0.
- `node scripts/ui-smoke.mjs investor-reporting ... --fixtures
  fe-s-10-global.json`: rc=0, `LOC: /investor-reporting`, `FIXTURES: 4
  declared; 4 matched`. PNG shows the two-firm dropdown and a `49 Financial`
  attribution chip.
- `node scripts/ui-smoke.mjs "investor-reporting?firm=global" ... --firm
  49financial --fixtures fe-s-10-one-firm.json`: rc=0, `LOC: /market`
  (diagnosed as row `IRPT_FNTEND-W1-S10`, not a defect in this cell's own
  code).

## Commits

- Portal repo: `3f055080` (26 files, 2636 insertions, 63 deletions) on
  branch `wk-irpt_fntend-1-6-fe-s-10`, LOCAL (not pushed).
- Workspace repo: this instance, this result file, both PNGs, the two
  surprise rows and the task order's `<status>` flip, committed together,
  LOCAL (not pushed).
