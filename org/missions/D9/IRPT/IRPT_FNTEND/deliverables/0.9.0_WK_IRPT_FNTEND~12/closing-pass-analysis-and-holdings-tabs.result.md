# FE-s-62 result -- Analysis and Holdings tabs read against DESIGN.md

These captures are FIXTURE-FED: the real `/investor-reporting` route with responses answered at the network layer by `scripts/ui-smoke.mjs`; no live route was reached. That is the right evidence for THIS card (FWD-12's DONE WHEN is about how the real page looks and behaves to an advisor who knows the portal, and needs no counterpart half) and would not be for the other seven cards, which need IRPT_BCKEND.

**IMPORTANT MEASURED LIMIT (row IRPT_FNTEND-W12-S1).** The order's own fixtures (`fe-s-6-ready.json`, `fe-s-7-smartx.json`) are keyed by operation name, not by the wire URL, so ui-smoke printed `FIXTURES: 4 declared; 0 matched >=1 URL` / `FIXTURE-DEAD` for all four. The four criterion captures (`fe-s-62_*.png`) therefore show the UNFIXTURED state: "Scope could not be resolved" and, on Holdings, a "Failed" panel with Retry. They do not show the radial drilldown, category tree, model colours, table or `withheld` rendering. To read those, I added supplementary captures (`supp_*`) using wire-keyed fixtures already in the tree (`fe-s-18-holdings-observed.json`, `fe-s-18-frozen.json`).

## Canvas discriminator
FE-s-11's recorded capture: `CANVAS: rgb(195, 202, 218)` (the retired silver).
Every capture here (all 8 plus the AFTER pair): `CANVAS: rgb(244, 246, 250) (the page field; contract portal/DESIGN.md C3 = #F4F6FA = rgb(244, 246, 250) -- ...)`.

## Captures (all read with the Read tool)
| file | viewport | CANVAS | clauses read against | what the capture shows |
|---|---|---|---|---|
| fe-s-62_analysis_1440.png | 1440 | rgb(244, 246, 250) | C3 C8 C9 C12 | scope-failed page; Analysis tab underline and label indigo; Generate panel white with hairline; Add button is a black/navy fill; Export is the one indigo button; scope-error line is dark red text with no icon (C12) |
| fe-s-62_analysis_390.png | 390 | rgb(244, 246, 250) | same | same content stacked, no horizontal clipping |
| fe-s-62_holdings_1440.png | 1440 | rgb(244, 246, 250) | C12 | "Failed / IR-REQUEST-FAILED" panel and an indigo Retry button; below it 400px of empty canvas |
| fe-s-62_holdings_390.png | 390 | rgb(244, 246, 250) | C12 | same |
| supp_holdings_observed_1440.png | 1440 | rgb(244, 246, 250) | C3 C8 C10 C12 | READY holdings: summary panel, then a dark navy card (Total Assets, Models, SMAs, Client tiles with model-coloured dots) inside a white panel (C3); purple legend and "A-0001" text (C8); pie plus a slice table; rightmost header clipped "Provenan", Advisory column wraps to six lines (C10) |
| supp_holdings_observed_390.png | 390 | rgb(244, 246, 250) | same | dark card stacked; table scrolls sideways past Denominator |
| supp_analysis_frozen_1440.png (BEFORE) | 1440 | rgb(244, 246, 250) | C1 C2 C12 | account labels A-0001.., snapshot id and idempotency key render in a monospace face (C1, C2); "Needs correction" and "Select a client" lines in red text with no icon (C12) |
| supp_analysis_frozen_390.png (BEFORE) | 390 | rgb(244, 246, 250) | C1 C2 | same |
| supp_analysis_frozen_1440_AFTER.png / _390_AFTER.png | 1440, 390 | rgb(244, 246, 250) | C1 C2 | the same ids now render in Lato with tabular figures; nothing else moved |

Verbatim CANVAS line, all runs: `CANVAS: rgb(244, 246, 250) (the page field; contract portal/DESIGN.md C3 = #F4F6FA = rgb(244, 246, 250) -- light fg on this is the footgun)`.

## Fix made (one finding)
C1/C2: `font-mono` on account labels, snapshot id, comparison keys, idempotency key, job request id (`GenerateComposer.tsx`, 5 places) and RevisionIdentity values (`RevisionIdentity.tsx:62`) -> `tabular-nums`. Portal commit 1319b09f. No test referenced `font-mono` (count 0 elsewhere); full suite 0 fail after the change.

## Unfixed findings (rows)
- W12-S1: order fixtures dead (above).
- W12-S2: dark navy card and purple text from shared `CategoryViewTree` (C3, C8); outside paths.
- W12-S3: slice table clipping (C10); red-only error text with no icon (C12); left alone (SliceTable coupled to FE-s-55 `withheld` rendering, which the order says not to change).

## Source read for the judgment criterion (evidence only)
Holdings reuses the portal `CategoryViewTree` (`DrillTree.tsx:60`, `@/components/CategoryViewTree`) and `getModelColor` / `getCanonicalModelName` (`DrillTree.tsx:62`, `@/lib/modelPortfolioColors`). The slice table is a real `<table>` in `SliceTable.tsx` (7 matches for withheld / table markers in it), present in the supplementary DOM capture as a visible table beside the pie. I did not open the DOM of the Analysis tab for a chart-table equivalent; the Analysis tab has no chart in the captured states. NO VERDICT.
