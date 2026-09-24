# DSGN_IRPTV1.TO-IV-t-4 (security-list) -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~3`. Portal branch `wk-DSGN_IRPTV1-3-portal`, commit
`287acb896ffcb89fb992b29fb7360b7a53712a27` (LOCAL). Workspace branch `wk-DSGN_IRPTV1-3`.

## What changed

New `portal/src/pages/InvestorReporting/tabs/holdings/SecurityList.tsx` -- a `Panel
variant="nested"` with `PanelHeader`/`PanelContent`/`PanelFooter`: one row per `kind ===
'security'` leaf node of `snapshot.nodes`, columns Ticker / Name / Sleeve / Weight / Value,
sortable by any column (default weight descending), filterable by sleeve and by account.
Asset class and Sector columns are absent. The footer carries basis, denominator, position
count and source coordinate/revision -- never a table cell. Mounted in `HoldingsTab.tsx` as
one line (`<SecurityList snapshot={snapshot} />`, plus its one import line) immediately after
`<DrillTree snapshot={snapshot} />`; `SliceTable.tsx` untouched.

## IV4-AC1 -- SECURITY-LIST-OK

`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-t-4.security-list.test.ts` --
PASS (1 pass / 0 fail, 1 `expect()` call covering all 9 fixtures). Over the task order's two
named `fe-s-7` fixtures plus every sibling `fe-s-7/holdings.*.json` (discovered from disk --
row `DSGN_IRPTV1-W3-S2`) and `holdingsSnapshot.success.json`: `ROWS: n of n leaves` for every
fixture (exact match, including the three fixtures with zero leaves), every row's NAME text
independently checked against `display.label`/`displayName`, WEIGHT/VALUE text checked
against the component's own exported formatters run on the node's `pctOfTotal`/`amount`, no
ticker cell containing a full `securityId`, and rows weight-descending by default (checked on
the actual rendered `data-node-ref` order, not the source array order).

## IV4-AC2 -- COLUMNS-AND-VOCAB-OK

`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-t-4.columns-and-vocabulary.test.ts`
-- PASS (1 pass / 0 fail, 2 `expect()` calls). Header row exactly `Ticker, Name, Sleeve,
Weight, Value` (the sort-direction glyph on the active column is stripped before comparison
-- an affordance, not the column's name) on every fixture that renders a table; zero of
`sourceCoordinate`/`sourceRevision`/`observed-custody`/`observed-allocation`/`src-`/`holdings/`
found in any `<td>` cell across all 9 fixtures; the footer positive control genuinely fires
(verified by direct inspection: the footer for `holdings.smartx-observed.json` reads `Basis:
observed-custody | Denominator: 5,000,000 | Positions: 4 | Source:
holdings/tenant-a1/2026-09-09 (src-2026-09-09-smartx-01)` -- three of the six forbidden
tokens genuinely present, confined to the footer, never a cell).

## IV4-AC3 -- ONE-LINE-MOUNT

`git diff --numstat 7c542fd23ec70c88bade4e3270f4c87f267a275a -- HoldingsTab.tsx SliceTable.tsx`:
`['2\t0\tsrc/pages/InvestorReporting/tabs/holdings/HoldingsTab.tsx']` -- 2 lines added (the
import + the mount), 0 removed, `SliceTable.tsx` absent from the diff entirely. `VERDICT:
ONE-LINE-MOUNT` -- PASS. (`DrillTree.tsx` differs from the base too, but is out of this
criterion's pathspec by design -- it is IV-t-3's change, landed earlier in this same
worktree.)

## Seam check (not an acceptance criterion, recorded as evidence)

`bun test src/pages/InvestorReporting/__tests__/fe-s-10/` (the `TabShell`/`HoldingsTab`
mounting suite): 31 pass / 4 fail both BEFORE and AFTER this cell's `HoldingsTab.tsx` change
(verified by temporarily reverting `HoldingsTab.tsx` to `7c542fd2`'s bytes and re-running --
identical 4 failures, all in `tabs-mounted.test.ts`'s `reporting tab is unaffected` block,
unrelated to Holdings). Pre-existing, out of this order's grant to fix.

## IV4-AC4 -- RECORD, no verdict (judgment, CVO at L9)

- `iv-t-4.security-list.html` (5017 bytes): `renderToStaticMarkup(createElement(SecurityList,
  { snapshot }))` over `holdings.smartx-observed.json` (4 leaves, richer ancestor chain than
  the Cottonwood fixture -- account > model > security and account > sleeve > security both
  exercised).
- `iv-t-4.png`: attempted (own dev server, port 5417, stopped after use -- never 5174). RAN,
  but shows the same "Scope could not be resolved" state as IV-t-3's PNG -- the smoke
  script's directory-search fixture stub does not carry enough to auto-select a client scope,
  so `HoldingsTab` (and this cell's `SecurityList`) never mounted in the screenshot.
  `iv-t-4.security-list.html` is the substantive AC4 artifact.

## Surprise rows

None new for this cell -- `DSGN_IRPTV1-W3-S2` (already filed against IV-t-3) is cited, not
duplicated, per the order's own instruction.
