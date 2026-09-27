# DSGN_IRPTV1.TO-IV-e-45.face-batch -- result summary (0.9.0_WK_DSGN_IRPTV1~29)

## Per-row disposition

- **UIR-17** (Over what opens each account's Performance) -- IMPLEMENTED. `IdentityCard`'s Over
  What accounts (single and multi) render as real `<button data-account-ref="...">` elements when
  `onOpenAccountPerformance` is supplied (inert as before when it is not); `index.tsx` relays the
  click into a `requestedFocus` state passed to `TabShell`, which switches the active tab to
  `reporting` and seeds `ReportingTab`'s tab-local `initialFocusedAccountId` with the same account
  id (forcing a remount via its own mount key even if Performance is already active).
- **UIR-20** (Export disabled with no answer-bearing report) -- IMPLEMENTED. `ReportingTab`'s
  `onExportTarget` effect and `index.tsx`'s `exportGateOk` both now require
  `isAnswerBearing(report.availability)` before a target is published / the control is enabled.
- **UIR-27** (Supervision/Advisory one click away, or hidden when withheld) -- PARTIALLY
  IMPLEMENTED. The "hidden when withheld on every row" half is implemented (`hideClassification`);
  the "one click away" half for the ordinary case collides with `fe-s-39/adapter-plane.test.ts`'s
  F39-AC7 byte-exact golden (out of this cell's `<paths>` grant) and is left as the pre-existing
  always-visible columns. Surprise row `DSGN_IRPTV1-W29-S2`.
- **UIR-28** (client facts on the face; source dates + coverage one click away, one date format)
  -- IMPLEMENTED. `HoldingsSummary` moves Source dates and Model coverage behind a `<details>`
  disclosure; both dates render through `formatPanelTimestamp`.
- **UIR-29** (one money format; client total once) -- PARTIALLY IMPLEMENTED. A new
  `tabs/holdings/format.ts` unifies `SliceTable`/`AllocationBars`/`HoldingsTreemap`/`SecurityList`'s
  four duplicate formatters into one. Full page-wide unification (with `IdentityCard`'s own
  `$`-symbol format) and "the client total appears once" (removing `HoldingsSummary`'s "Current
  value") each collide with a different out-of-grant pinned test; both attempted and reverted.
  Surprise row `DSGN_IRPTV1-W29-S3`.
- **UIR-35** (no amount wraps at 1440px) -- IMPLEMENTED. `whitespace-nowrap` on the Amount header
  and cell in `SliceTable`.
- **UIR-38** (no classification chip / client-language chips never wrap) -- CONFIRMED + hardened.
  The existing badges are already client language (never a raw token); `whitespace-nowrap` added.
- **UIR-40** (one band per page) -- CONFIRMED. `AllocationBars`/`HoldingsTreemap`/`SecurityList`
  all mount `variant="nested"` (never a band); the page-wide invariant is `iv-e-20.bands.test.ts`'s
  own live-server census (out of this cell's grant, unaffected).
- **UIR-45** (one date format; source line names the actual source) -- IMPLEMENTED.
  `HoldingsSummary` and `IdentityCard` both render through `formatPanelTimestamp`, verified to
  produce IDENTICAL text for the same raw date.

## Amendment 1 (disarms W29-S1)

The three IV-e-12 tests (`iv-e-12.cash-green.test.ts`, `iv-e-12.positioning-reader.test.ts`,
`iv-e-12.unclassified.test.ts`) are re-scoped: each retired pin (the commodities base-hex assertion,
retired by CTO 101649/101681) is dropped while every other intent (cash's own distinct green, the
Positioning reader's parity over every OTHER key, the unclassified/never-borrows-another-class rule)
stays asserted -- the unclassified test now reads the page-local `ASSET_CLASS_COLOR` (the actual
paint source, per IV-e-43/UIR-37) instead of the shared `lib/chartColors.ts` registry the component
no longer paints from. All three pass: 3 pass / 0 fail.

## New surprise rows filed

- `DSGN_IRPTV1-W29-S2` -- UIR-27's "one click away" half vs. F39-AC7's byte-exact golden.
- `DSGN_IRPTV1-W29-S3` -- UIR-29's "one format"/"once" halves vs. two out-of-grant test sets.
- `DSGN_IRPTV1-W29-S4` -- a fresh, printed denominator for the suite's 17 pre-existing, unrelated
  failures at this worker's tip.

## Regression

`bun test src/pages/InvestorReporting` at this worker's tip: 860 pass / 27 skip / 17 fail (all 17 in
fe-s-1/14/15/19/25/30/45/55/57, pre-existing, unrelated to this cell -- see `DSGN_IRPTV1-W29-S4`).
The whole `dsgn-irptv1` suite (94 files, including this cell's own new/amended tests): 0 fail.
`bun run typecheck`: rc=0, 0 diagnostics.
