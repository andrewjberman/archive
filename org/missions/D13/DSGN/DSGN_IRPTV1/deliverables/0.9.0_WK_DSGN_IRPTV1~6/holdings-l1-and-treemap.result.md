# DSGN_IRPTV1.TO-IV-e-5 (holdings-l1-and-treemap) -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~6`. Portal branch `wk-DSGN_IRPTV1-6-portal`, commit
`fb4fc3b2ead32b67b49269b3f6556b6f9268d22e` (LOCAL). Workspace branch `wk-DSGN_IRPTV1-6`.

## What changed

New `portal/src/pages/InvestorReporting/tabs/holdings/AllocationBars.tsx` -- a `Panel
variant="nested"` with `PanelHeader`/`PanelContent`/`PanelFooter`: one horizontal bar per L0
category (the snapshot root's own direct children), length/amount read straight off the
node's `pctOfTotal`/`amount`+`currency` ("not supplied" when null). Each bar is a native
`<details>`/`<summary>` disclosure (the same pattern `header/IdentityCard.tsx`'s "About this
scope" panel already uses in this project) that reveals the per-account matrix: one row per
`kind === 'account'` node found anywhere in the snapshot, one column per category, each cell
the account's own `amount` when that account sits at or beneath the category (walking
`parentRef`), else "--". `slices.ts` is out of grant, so `rootOf`/`childrenOf` and the
`display.label`-else-`displayName` label rule are a small deliberate duplicate, matching
`SecurityList.tsx`'s own precedent for the identical reason.

New `portal/src/pages/InvestorReporting/tabs/holdings/HoldingsTreemap.tsx` -- one node per
`kind === 'security'` leaf with a non-null `pctOfTotal` (null leaves excluded and counted);
size = `pctOfTotal`; colour/group = the nearest `model`/`sleeve` ancestor's label via a small
deliberate duplicate of `SecurityList.tsx`'s `nearestAncestorOfKind` (same reason: the file
this cell must not touch is also the file it must not depend on). Hover ticker is
`display.symbol` else "not supplied" -- NEVER a `securityId` parse (narrower than
`SecurityList.tsx`'s own `tickerFor`, per the C-S12 rule this order names explicitly). No
asset class, no sector. `recharts` `Treemap` + `ResponsiveContainer`, a deterministic
hash-based colour keyed by the group label (no `ASSET_CLASS` registry, which this order does
not grant and which would misfire on a sleeve's taxonomy-path label anyway).

Mounted in `HoldingsTab.tsx`: `<AllocationBars snapshot={snapshot} />` directly above
`<DrillTree snapshot={snapshot} />`, `<HoldingsTreemap snapshot={snapshot} />` directly above
`<SecurityList snapshot={snapshot} />`, plus their two import lines -- 4 lines added, 0
removed, nothing else touched.

## IVE5-AC1 -- BARS-AND-MATRIX-OK

`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-5.allocation-bars.test.ts` --
PASS (1 pass / 0 fail, 1 `expect()` call covering all 9 fixtures: the task order's `fe-s-7/*`
set discovered from disk, row `DSGN_IRPTV1-W3-S2`'s workaround, plus
`holdingsSnapshot.success.json`). Every fixture: `BARS: n of n` exact; every bar's rendered
pct/amount text equals the category's own field run through the exported formatter (0
computed values, printed); the per-account matrix's row/column count and every cell (`filled`
vs `dashes`) independently verified against a fresh `accountMatrixFrom` read, not the
component's own arithmetic; no leaked `basis`/`denominator`/`provenance` token in any bar or
matrix cell across all 9 fixtures, with the footer's own inclusion of those facts as the
positive control (verified present on every fixture).

## IVE5-AC2 -- TREEMAP-OK

`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-5.treemap.test.ts` -- PASS (1
pass / 0 fail, 1 `expect()` call). `treemapLeavesFrom` exercised directly (no chart rendering)
over all 9 fixtures: `NODES: n of n leaves` exact on every fixture including the three with
zero leaves; `EXCLUDED-NULL-WEIGHT: 0` on all 9 (none of this set's security leaves carry a
null `pctOfTotal` -- the exclusion branch exists and is unit-reachable but this fixture set
never trips it); every node's `size`/`amount`/`currency`/`name`/`group` checked against an
independent, test-side re-derivation of the ancestor walk (not the cell's own function); the
C-S12 negative arm (ticker never a `securityId` substring) holds on all 9 fixtures, none of
which carry a `display` block at all -- so the POSITIVE control (a planted `display.symbol`)
had to be built as a small in-memory synthetic snapshot rather than read off a real fixture
(filed as `DSGN_IRPTV1-W6-S2`); that control fires correctly (`ticker: PLANTED-XYZ`,
`PLANTED-OK: true`) and a mutation that reintroduces the `securityId` fallback breaks it (see
Controls).

## IVE5-AC3 -- TWO-MOUNTS-ONLY

`git diff --numstat 895752676a -- HoldingsTab.tsx DrillTree.tsx SecurityList.tsx
HoldingsSummary.tsx`: `['4\t0\t...HoldingsTab.tsx']` -- 4 lines added (2 imports + 2 mounts), 0
removed, every changed line matches the import/mount allow-list, the other three files absent
from the diff entirely. `VERDICT: TWO-MOUNTS-ONLY` -- PASS.

## IVE5-AC4 -- RECORD, no verdict (judgment, CVO at L9)

- `iv-e-5.allocation.html` (11707 bytes): full bar+matrix render over
  `holdings.smartx-observed.json` (3 categories: Models/SMA/Client, 3 accounts, richer than
  the two-account success fixture).
- `iv-e-5.treemap.html` (1103 bytes): panel chrome renders correctly; the chart body itself is
  an empty `recharts-responsive-container` div because `renderToStaticMarkup` cannot give
  `ResponsiveContainer` a real layout box to measure -- the identical structural limitation
  `DrillTree.tsx`'s own donut has under static markup, not a defect specific to this cell. The
  pure data derivation (IVE5-AC2, exercised with no chart rendering at all) is the substitute
  evidence for correctness.
- No smoke PNG attempted: no IV-e-2 fixture exists in this worktree (a parallel chain, not yet
  merged here), and `scripts/ui-smoke.mjs`/`fixtures/smoke/**` are outside this order's
  `<paths>` grant regardless (same limitation round 1's IV-t-3/IV-t-4 AC4 rows recorded).

## Controls

Two mutants (one per cell), both restored byte-identical afterward (diff confirmed):
1. `AllocationBars.tsx`: appended a leaked `observed-custody` token into a bar's amount span
   -- IVE5-AC1 failed (leak check), as expected.
2. `HoldingsTreemap.tsx`: made `tickerFor` fall back to the raw `securityId` (the C-S12 rule's
   exact violation) -- IVE5-AC2 failed at the planted-symbol positive control, as expected.

Determinism: both suites run three times each (pre-mutation, post-restore, post-commit) --
identical per-fixture and VERDICT lines every time.

## Surprise rows

- `DSGN_IRPTV1-W3-S2`: cited, not duplicated (naming-gate workaround, already filed).
- `DSGN_IRPTV1-W6-S1`: the "expand affordance per bar" / "the matrix" (singular) tension --
  resolved as N identical per-bar `<details>` disclosures rather than one shared toggle
  (native HTML has no primitive for the latter without added script).
- `DSGN_IRPTV1-W6-S2`: no fixture in this worktree's grant carries a `display` block, so
  IVE5-AC2's positive control is a synthetic in-memory snapshot, not a checked-in fixture.

Both filed OBSERVATION/INERT -- neither blocks IVE5-AC1/AC2/AC3, all three of which PASS.
