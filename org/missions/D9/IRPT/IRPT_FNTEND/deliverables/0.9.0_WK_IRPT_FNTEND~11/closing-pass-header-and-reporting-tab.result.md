# FE-s-61 result -- header and Reporting tab, real route, read against DESIGN.md

**These captures are FIXTURE-FED**: the real route `investor-reporting` with fixtures answered at the network layer by `scripts/ui-smoke.mjs`; no live route was reached. That is the right kind of evidence for THIS card (FWD-12's DONE WHEN is about an advisor's familiarity with the real page, which needs no counterpart half) and not for the other seven cards, whose outcomes depend on what a live producer returns. **Two limits, both filed as rows:** the fixture the order names (`fe-s-10-global.json`) matched 0 of 4 URLs, so the two ordered captures show the scope-failed state (W11-S1); and no fixture reaches an answer-bearing report, so the summary cards, chart, period results and account detail were not on screen in any capture (W11-S2).

Vintage: workspace base CLOUD fcf38f866b, portal base DEV ddb172bf, fix commit on portal branch `wk-irpt_fntend-10-61-fe-s-61-portal`. DESIGN.md and portal CLAUDE.md read in full first.

## The discriminator

FE-s-11's recorded capture printed `CANVAS: rgb(195, 202, 218)` (retired silver). This pass prints, at both widths, `CANVAS: rgb(244, 246, 250) (the page field; ...)`. The value itself was read, not the parenthetical.

## Captures (file / viewport / CANVAS line / clauses / what the capture shows)

| file | vp | CANVAS line (verbatim) |
|---|---|---|
| `fe-s-61_reporting_1440.png` | 1440 | `CANVAS: rgb(244, 246, 250) (the page field; contract portal/DESIGN.md C3 = #F4F6FA = rgb(244, 246, 250) -- light fg on this is the footgun)` |
| `fe-s-61_reporting_390.png` | 390 | same line |
| `fe-s-61_reporting_{1440,390}_live-fixture.png` (BEFORE) and `..._live-fixture_AFTER.png` | 1440, 390 | same line, each |

NOTE: the two ordered PNGs were re-captured after the fix, so they show the AFTER preset styling; the pre-fix look of the same scope-failed state is unchanged apart from the YTD chip and is preserved by the `_live-fixture` BEFORE pair. `smoke_*.txt` hold the full printed output of each run.

**Ordered captures (fe-s-10-global.json, scope-failed state), read:** page field light (C3); page title black with the indigo rule and indigo subtext (C8); the firm dropdown is absent (catalogue not resolved) and the client search is a white input with a grey hairline border; below the header a dark-red sentence "Scope could not be resolved..." with no icon (C12 says status.danger icon beside navy text, finding W11-S3); tabs with the active label and underline in indigo (C8); Reporting panel white with hairline (C3); a filled-indigo YTD chip, Refresh plain, Export filled indigo; a StatusPanel "Failed" card with a filled-indigo Retry (C8: a second filled action, W11-S3).

**Supplementary captures (fe-s-14-global.json, UNCERTAIN report), read:** firm dropdown "Global (All)" is an indigo-outlined control with a chevron (a byte copy of the Model Portfolios className; source imports the same `PageSurfaceControl` in both files -- read in source: `FirmDropdown.tsx` imports `@/components/ui/PageSurfaceControl`, `ModelPortfolios.tsx:49` imports the same); it carries rounded-lg and a shadow-sm class (C11) and font-semibold (C1) inherited from that copy (W11-S4). ScopeSummary is a white hairline panel of five label/value facts with small uppercase labels (C1 allows tracking under 14px); the partial-disclosure fact (FE-s-59) did not render because the fixture carries no unprojected grant. At 390 the strip wraps into two rows and nothing overflows; the date inputs wrap under "Custom" and the three date statements stack (FE-s-18 layout).

## Fix (one finding, one fix)

Finding: the active period preset is a solid filled indigo chip. DESIGN.md C8: "A segmented control or toggle never gets a filled purple chip per option; its active state is weight and rule." Also C1 (the buttons used font-medium, weight 500) and C11 (buttons 3px, panel 4px; they used 6px and 8px).
BEFORE: `fe-s-61_reporting_1440_live-fixture.png` / `_390_live-fixture.png` (YTD filled indigo, white label).
AFTER: `..._live-fixture_AFTER.png` (YTD white, 2px navy rule, bold navy label; all buttons 3px; panel 4px). Export stays the one filled-indigo action. Edit is confined to `tabs/reporting/PeriodControls.tsx`, portal commit `3a63d523`; the whole InvestorReporting suite stayed at 0 fail.

## Unfixed findings -> rows

W11-S1 dead named fixture; W11-S2 answer body not reachable in any capture; W11-S3 red error text (index.tsx) and filled Retry/Reload (StatusPanel.tsx), both outside the grant; W11-S4 firm-dropdown and cohort-chip styling pinned by tests outside the grant, plus slate ink.

## Criteria

F61-AC1 typecheck rc=0. F61-AC2 / F61-AC3 canvas printed `rgb(244, 246, 250)` at 1440 / 390. F61-AC4 `0 fail` (612 pass, 22 skip, 634 tests across 114 files) with the dev server stopped and port 5471 verified closed. F61-AC5 judgment: evidence above, NO verdict.
