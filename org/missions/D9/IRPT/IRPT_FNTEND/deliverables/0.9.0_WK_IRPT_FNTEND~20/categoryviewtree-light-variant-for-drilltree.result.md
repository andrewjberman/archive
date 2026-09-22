# FE-s-70 result -- CategoryViewTree additive light variant for DrillTree

**These captures are FIXTURE-FED**: every `ui-smoke.mjs` invocation below drove the real route
(`/investor-reporting`, `/portfolios`) with fixtures answered at the network layer (`--fixtures`);
no live backend or route was reached. That is the right evidence for FWD-12's DONE WHEN here
("the Investor Reporting screens look and behave like the rest of the Opal portal") -- the
question is purely about rendered visual state against portal/DESIGN.md, which a fixture-fed
capture answers completely; it needs no live-wire counterpart the way a data-correctness cell
would.

## What changed

`portal/src/components/CategoryViewTree.tsx` gained an additive `ground?: 'dark' | 'light'` prop
(default `'dark'`), threaded through `TreeBody` -> `CategoryOverview` -> `CategoryTile` ->
`SegmentBar`. When `'light'`:
- The ready-state card (`CategoryOverview`) drops the dark-gradient `GraphicPanel` wrapper for a
  plain white surface with the same outer `border-black`/`rounded-[4px]` frame, an indigo top rule
  kept as the one accent, and `Eyebrow` (black-on-white) instead of `PanelEyebrow` (lilac-on-navy).
- Every non-data ink (`headline`, subtext, tile name/figures/copy, the pie's slice stroke, the
  segment-bar track, the hover/rest tile fill and ring) re-derives per DESIGN.md C5 (preserve the
  ROLE and the ratio, re-hue the value): navy `#163372` for primary text/figures, `darkGray
  #6B7280` for secondary copy (legal on a panel per C3's ink table), the hairline `#C4CBDB` for
  boundaries, the canvas `#F4F6FA` step for hover, and the site indigo `#5F3BE3` for the one
  "View breakdown" text link (C8's one-accent-link allowance).
- `l0ColorOf`/`l1ColorOf`/`memberColor` (the L0/L1/L2 legend, the pie slices, the bar segments) are
  called identically on both grounds -- **zero data colours moved.**

`portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx:223` -- the ONE line -- now reads
`<CategoryViewTree result={mdpfResult} ground="light" />`. Nothing else in that file changed.

`CategoryBreakdownDialog` (the L2 modal) and `SegmentBar`'s own default caller inside it are
untouched: `SegmentBar` takes `ground` as an OPTIONAL prop defaulting to `'dark'`, and the dialog
never passes it, so its render is byte-identical to before this cell.

## Criteria

**F70-AC1** -- `bun run typecheck`. `rc=0`, clean `tsc -b --noEmit` with no diagnostics.
PASS-by-output.

**F70-AC2** -- Holdings, 1440px, light variant, WHITE ground (C3). Fixture
`fe-s-18-holdings-observed.json` (no separate `category-views.json` key needed -- `DrillTree.tsx`'s
`mdpfResultFromSnapshot` derives the tree from the `holdings/` snapshot alone, confirmed by the
capture below actually reaching the ready state).
```
EXPECT[[data-slot="holdings-drill-tree"] section[aria-labelledby="asset-category-views"]]: PASS (1 visible)
EXPECT-GROUND[[data-slot="holdings-drill-tree"] section[aria-labelledby="asset-category-views"] > div]: PASS rgb(255, 255, 255)
ASSERT-CONTENT: 1 of 1 met
ASSERT-GROUND: 1 of 1 met
```
Read `f70_irpt_1440.png` directly: the "Asset Category Views" card is a real white panel with an
indigo top rule, navy "Total Assets" headline and figure, and three white/hairline tiles (Models
lilac, SMAs teal, Client amber top-strips and dots -- unchanged data colours) with navy text.
Clause read against: C3 (panel role, white surface, hairline boundary), C5 (ink re-hued
navy-on-white, ratio preserved). PASS-by-output; PNG read confirms the visual claim.
**Control discipline (HOW item 4):** this assertion's OWN discriminating power was checked and
found weak on this specific selector -- see row `IRPT_FNTEND-W20-S1` below; the criterion's literal
invocation still ran unmodified and its output matches `<expect>` verbatim, so it is reported
PASS-by-output per BOUNDS ("do not edit a criterion's expectation").

**F70-AC3** -- same, at 390px.
```
EXPECT[...]: PASS (1 visible)
EXPECT-GROUND[...]: PASS rgb(255, 255, 255)
ASSERT-CONTENT: 1 of 1 met
ASSERT-GROUND: 1 of 1 met
```
Read `f70_irpt_390.png` directly: same white card, single-column tile stack, legible at the narrow
viewport, no clipping. PASS-by-output.

**F70-AC4** -- THE GROUND CONTROL. `--inject-css` paints the section's first `> div` match silver
(`#c4cbdb`) and removes any background-image, then re-runs the SAME ground assertion.
```
INJECT-CSS: [data-slot="holdings-drill-tree"] section[aria-labelledby="asset-category-views"] > div{background:#c4cbdb !important; background-image:none !important}
EXPECT-GROUND[...]: FAIL rgb(196, 203, 219)
ASSERT-GROUND: 0 of 1 met
```
Matches `<expect>` exactly. PASS-by-output. This control DOES discriminate (see the row below for
why AC2/AC3's own bare ground read does not, on this specific selector).

**F70-AC5** -- Model Portfolios BEFORE capture, current HEAD, `__tests__/fe-s-69/fixtures/mp.json`
(landed by FE-s-69, present in this worktree's base -- no fallback fixture needed).
```
SAVED : .../f70_mp_before_1440.png
```
PASS-by-output. Read `f70_mp_before_1440.png`: the dark "All Categories" hero card, `$0` total (this
fixture's `sums.view_plane` is 0 and no peer AUM is present so no pie/tiles render -- the same
no-peers state on both captures, see AC6).

**F70-AC6** -- Model Portfolios AFTER capture, same fixture, asserting the sibling is unbroken
(`ground` defaults to `'dark'`).
```
EXPECT[section[aria-labelledby="asset-category-views"]]: PASS (1 visible)
EXPECT-STYLE[section[aria-labelledby="asset-category-views"] .relative::background-image]: PASS radial-gradient(90% 85% at 80% 85%, rgba(95, 59, 227, 0.55), rgba(0, 0, 0, 0) 65%), linear-gradient(rgba(255, 255, 255, 0.05) 1px, rgba(0, 0, 0, 0) 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, rgba(0, 0, 0, 0) 1px), linear-gradient(160deg, rgb(8, 19, 43), rgb(21, 37, 81))
ASSERT-CONTENT: 1 of 1 met
ASSERT-STYLE: 1 of 1 met
```
Read `f70_mp_before_1440.png` and `f70_mp_after_1440.png` side by side: pixel-identical dark hero
card, same "$0" headline, same AUA-by-model / Client Holdings panels below. Model Portfolios' own
use of `CategoryViewTree` is untouched. PASS-by-output, confirmed by direct visual comparison.

**F70-AC7** -- `bun test src/pages/InvestorReporting/__tests__/fe-s-7` (also picks up fe-s-72/fe-s-73
by substring match, per bun's own path matching). `37 pass, 0 fail, 180 expect() calls`. Read both
named files (`slices.test.ts`, `drill.test.ts`) first, per instruction: neither pins CategoryViewTree's
rendered classes -- both exercise `slices.ts`'s pure decision functions directly (drill destinations,
revision mismatches, sum-preservation), bypassing the `@/`-aliased render path entirely (their own
header explains why: `bun test` cannot resolve `@/` in this worktree). No update needed; nothing
pinned the old dark-card classes. PASS-by-output.

**F70-AC8** -- whole IRPT_FNTEND suite, dev server stopped (PID killed via `Stop-Process`, port 5951
verified closed via `curl` returning `000`/rc=28 before this run), `IRPT_FE_DEV_PORT` unset.
`620 pass, 22 skip, 0 fail, 2618 expect() calls, 642 tests across 117 files`. PASS-by-output.

**F70-AC9** -- judgment, RECORDED, no verdict:
- Chart legend / data colours (percent labels, donut/pie segments, per-model L1/L2 dots and bar
  segments): `l0ColorOf`, `l1ColorOf`, `memberColor` are called with the exact same arguments on
  both grounds; the only ground-conditional value touching the pie is the SLICE STROKE (the ring
  between slices), which is the panel's own background colour (white vs the band's ink), never a
  data hue. Read `f70_irpt_1440.png`/`f70_irpt_390.png`: Models lilac, SMAs teal, Client amber --
  identical hues to `f70_mp_before_1440.png`/`f70_mp_after_1440.png`'s dark card.
- Additive: `ground` is a new, optional prop; every caller that does not pass it (Model Portfolios,
  and `CategoryBreakdownDialog`'s own internal `SegmentBar` call) gets `'dark'`, the pre-existing
  render -- confirmed identical before/after in AC6's PNGs.
- `DrillTree.tsx` changed exactly one line (`ground="light"` on its existing `<CategoryViewTree>`
  call); no other render in that file moved.

## Surprise row filed

`IRPT_FNTEND-W20-S1` (INVESTIGATION_v2.md): F70-AC2/AC3's `--expect-ground` selector resolves, via
`document.querySelector`, to the section's Eyebrow wrapper `<div>` (the FIRST `> div` in document
order) rather than `CategoryOverview`'s own card div (the second child) -- and because that Eyebrow
div carries no background of its own, `groundColor()`'s ancestor walk passes straight through it and
the (also transparent) `<section>` to `DrillTree.tsx`'s own ambient `bg-white` wrapper. Verified by
temporarily reverting `DrillTree.tsx` to `ground="dark"` (no fix applied) and re-running AC2's exact
invocation: it printed the IDENTICAL `PASS rgb(255, 255, 255)` / `ASSERT-GROUND: 1 of 1 met`. F70-AC4
(which paints that same first-match div directly via `--inject-css`, rather than relying on an
ancestor) correctly discriminates. This cell's actual, committed implementation is independently
confirmed correct by reading the PNGs; the row is about the bare ground assertion's discriminating
power on this selector, filed per the criterion rule's own control discipline (HOW item 4) without
editing AC2/AC3's expectation.
