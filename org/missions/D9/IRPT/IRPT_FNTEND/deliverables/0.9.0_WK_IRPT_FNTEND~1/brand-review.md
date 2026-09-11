# FE-s-11 brand review

## Sources actually used, and why they differ from the WORKER FACE's two named files

The WORKER FACE names `deck_generation/brand_spec/brand.json` and
`deck_generation/brand/opal_brand_guidelines.pdf` as the brand sources. **Neither
exists in this worktree** (confirmed: `comp-find --name brand.json --corpus raw`
and `comp-find --name "opal_brand_guidelines*" --corpus raw` both return `0
hit(s) across 76056 file(s) scanned` -- every file, tracked and untracked and
gitignored, in the whole repo). `deck_generation/.gitignore:14-15` ignores
`brand_spec/` and `brand/` outright, so both directories exist ONLY in the
primary checkout (`C:/Users/AndrewBerman/Desktop/ajb_workspace/deck_generation/`)
and in **no** worktree. This is not a new finding: `0.9.0_WK_IRPT_FNTEND~2`
already surfaced and grounded it as row `IRPT_FNTEND-W2-S1` while building
FE-s-4's render package, and copied both the token file and the logo verbatim
into the package so it would be self-contained in any checkout. This review
cites that row rather than re-filing it (a duplicate finding is not a new
surprise) and uses the substitutes the codebase already provides for exactly
this reason:

- `portal/src/pages/InvestorReporting/render/brand.tokens.json` -- a **byte
  copy** of `deck_generation/brand_spec/brand.json` (per `render/brand.ts`'s
  own header, "Both were copied from those paths into this package
  unmodified").
- `portal/src/pages/InvestorReporting/render/brand.ts` -- the same values as
  typed constants, with the workspace-relative source path recorded in
  `BRAND_TOKENS_SOURCE`.
- `deck_generation/DESIGN_BIBLE.md` (present, MANDATORY-status, independent of
  the missing files) -- corroborates the same hex values by an entirely
  different route: its own "A. Brand tokens (locked)" section lists
  `navy #163372 · midnight #0A1733 · medium-blue #174A7C · muted #395085 ·
  cool-grey #C4CBDB · electric-purple #5F3BE3 · white #FFFFFF · charcoal
  #595959` and `Type is Lato only`, which match `brand.tokens.json`'s
  `colors`/`extended_palette`/`typography` verbatim (DESIGN_BIBLE calls
  `#0A1733` "midnight" where brand.tokens.json/render code calls it
  "midnight_blue" -- same hex, a naming variance only).
- `portal/design/themes/opal-capital.css` -- the portal's own live theme
  tokens (`--semantic-action-primary: 253 74% 56%`), which resolve
  (HSL->RGB) to approximately `#603CE2` -- within HSL-rounding distance of
  brand's `electric-purple #5F3BE3` (RGB 95/59/227 vs. computed ~96/60/226).
  The portal's `--primary`/`--primary-purple` IS the brand's electric-purple.

## Screens reviewed

Six of the seven named screens were captured fresh this cell (`fe-s-11_*_390.png`,
this folder); three of those six landed on the intended content, three landed
on the portal's global error boundary instead of the named screen (see
`design-conformity-census.result.md` and surprise row
`IRPT_FNTEND-W1-S12` for why -- a genuine, reproducible crash this order's own
named fixtures trigger, not a brand defect). Where a fresh capture is an error
screen, this review ALSO cites the same screen's working capture from an
EARLIER cell's own committed deliverable (read-only, for informational
context; not edited, not this order's own evidence for its acceptance rows):

| screen | this cell's own PNG | working reference (earlier cell) |
|---|---|---|
| page / Reporting tab | `fe-s-11_page_390.png` (LANDED) | -- |
| Analysis tab | `fe-s-11_analysis_390.png` (crashed) | `0.9.0_WK_IRPT_FNTEND~3/fe-s-6_analysis_ready_1440.png` |
| Holdings tab | `fe-s-11_holdings_390.png` (crashed) | `0.9.0_WK_IRPT_FNTEND~4/fe-s-7_holdings_smartx_1440.png` |
| Export modal | `fe-s-11_export_390.png` (crashed) | `0.9.0_WK_IRPT_FNTEND~1/fe-s-9_export_modal_1440.png` (already this worker's own deliverables folder, from the earlier FE-s-9 order) |
| print, performance | `fe-s-11_print_390.png` (bundle-not-renderable message, not a crash) | `0.9.0_WK_IRPT_FNTEND~2/fe-s-4_print_performance_1440.png` |
| print, analysis | not captured -- F11-AC8 names one print invocation (`?bundle=perf-narrative-fixture-1`, a PERFORMANCE bundle); no analysis-print fixture/route is named by this order's acceptance battery | `0.9.0_WK_IRPT_FNTEND~2/fe-s-4_print_analysis_1440.png` |

## Colours

- **Page / Reporting tab (`fe-s-11_page_390.png`)**: canvas is the cool-grey
  silver (`CANVAS: rgb(195, 202, 218)` per the ui-smoke instrument's own probe
  -- close to `#C4CBDB` = rgb(196,203,219), the tiny delta is anti-aliasing at
  the sampled pixel, not a different colour). Every panel on it (ScopeSummary,
  StatusPanel/period-controls surfaces) is a WHITE card with navy/charcoal
  text -- no light text sits directly on the silver, matching brand's
  `contrast_rules` (text on a non-white/grey fill must be white; text on
  white/grey must be navy/charcoal) and `SURFACES` in `render/brand.ts`. The
  Firm dropdown and the YTD preset are the single purple accent
  (`bg-[hsl(var(--primary))]`, i.e. brand's electric-purple), each appearing
  once, never in a multi-segment ramp -- consistent with DESIGN_BIBLE's B2
  ("purple is a single-accent color only... must never appear inside a
  multi-segment ramp").
- **Export modal (`fe-s-9_export_modal_1440.png`, reference)**: the modal body
  is a dark navy band (`Panel variant="chart"`) carrying WHITE text
  throughout ("EXPORT OPTIONS", "Branding", checkbox labels) -- exactly
  brand's contrast rule applied to a non-white/grey fill. The selected
  branding pill ("Opal") is solid electric-purple with white text; the two
  unavailable choices ("Advisor", "Co-branded") are outline-only, dark text,
  correctly greyed/disabled-looking without inventing a new colour.
- **Print templates (`fe-s-4_print_performance_1440.png`,
  `fe-s-4_print_analysis_1440.png`, reference)**: white page sheet on the
  silver canvas (per `render/Page.tsx`'s `<section className="ir-page ...">`
  and `render/print.css`'s own header, "the canvas is the silver cool grey
  #C4CBDB and NOTHING light sits on it"); navy headings and body text; the
  electric-purple appears ONLY as the section-eyebrow label ("PERFORMANCE
  REPORT" / "ANALYSIS REPORT"), the chart line and rule, and `UNAVAILABLE`
  flags -- again single-accent, never a ramp. Both templates -- one landscape,
  one portrait -- share identical logo treatment, colour tokens and footer
  format, which is the intended "one brand, two orientations" property
  `render/Page.tsx`'s own header names as a property of the code rather than
  a reviewer's memory.
- **Colour-law scan (`colour-law.test.ts`, F11-AC3)**: mechanically confirms
  the above for every `.tsx` file in the tree except ONE real exception --
  `export/AppliedBranding.tsx` renders `text-white` with no dark ancestor and
  no self-contained dark background in its own file. See
  `design-conformity-census.result.md` and surprise row `IRPT_FNTEND-W1-S11`.

## Logo clear space

`render/brand.ts`'s `LOGO` constant states the rule from `brand.tokens.json`
verbatim: `orientation: horizontal_only`, `safe_space: "0.5x"` (a clear zone of
0.5x the logo's own height, free of other elements), rendered at `widthPx: 152`
on screen / `widthPt: 114` in the PDF. `render/Page.tsx` applies this as CSS
padding around the mark (`ir-logo-clearspace`, per that file's own comment:
"The logo's clear space is brand.json's own 0.5x rule, applied as padding
around the mark") -- visible in both print captures as consistent whitespace
around the "Opal Capital" wordmark on every page, never crowded by the
eyebrow label or the identity block beside it. The `full_color` variant
(brand's `logo.light_bg_variant`) is used throughout, correct for the white
sheet it sits on; no `ko_white`/black variant is needed anywhere in this
tree because no InvestorReporting surface places the mark on a dark fill.

## Typeface

Brand names Lato (`brand.tokens.json.typography.font_family`, weights
Thin/Light/Regular/Medium/SemiBold/Bold). `render/print.css` (the ONLY
stylesheet governing the rendering package, screen preview and PDF alike)
sets `font-family: 'Lato', 'Segoe UI', Arial, sans-serif` -- but its own
header comment (surprise `IRPT_FNTEND-W2-S3`, already filed, not re-filed
here) states plainly: "no Lato binary exists in this repo, in
deck_generation, or in either font store on this box... the family stack
('Segoe UI', Arial, sans-serif) carries the document" until the packaged
`.woff2` files are committed. The rendered screenshots therefore show a
system sans-serif substitute, not Lato itself, on this box -- a disclosed,
pre-existing, out-of-grant gap, not a new finding. The portal's OWN on-screen
chrome (header, tabs, buttons -- everything outside the print/export
templates) uses `'Inter', -apple-system, ...` (`src/index.css`), which is the
portal's own established UI font, distinct from the document typeface; brand's
Lato rule is scoped to the generated/exported document (DESIGN_BIBLE.md's own
banner: "MANDATORY for any agent generating PowerPoint"), not the web app's
native chrome, so this is not a discrepancy.

## Firm dropdown

Confirmed by import, not by eye: `header/FirmDropdown.tsx` imports
`PageSurfaceControl` from `@/components/ui/PageSurfaceControl` (see
`component-census.json`, row `PageSurfaceControl`, classification `REUSED`)
and renders it `as="dropdown"` -- the same control `ModelPortfolios.tsx` uses
for its own firm dropdown (`ModelPortfolios.tsx` also imports
`PageSurfaceControl` and configures it identically). `FirmDropdown.tsx`'s
`className` is the EXACT string copied verbatim from
`ModelPortfolios.tsx` lines 1268-1275 (portal `5907cbca`) per its own header
comment -- confirmed present, byte for byte, in both files. This satisfies
FWD-12's PROOF ("the Model Portfolios firm dropdown REUSED, not rebuilt") at
the level that is actually reusable: `ModelPortfolios.tsx` composes its
dropdown inline and exports no separate dropdown component, so there is
nothing to import beyond `PageSurfaceControl` itself (already reused, PATHS
row 2) -- the styling is reproduced because there is no shared constant to
import it from, not because a look-alike was built instead. See
`component-census.md`'s PRD row 5 accounting for the full citation.

## Table equivalents for every chart

One chart exists in this tree: `render/performance/CumulativeReturnChart.tsx`
(recharts `LineChart`), and it prints a full `<table>` of every plotted
observation immediately beneath the chart, unconditionally -- not only as a
fallback. Its own header comment states why: "recharts 3.7.0 renders an EMPTY
`.recharts-wrapper` under `renderToStaticMarkup`... The endpoint labels and
the series table are real DOM, so the numbers survive in BOTH planes" (surprise
`IRPT_FNTEND-W2-S4`, already filed). The Holdings tab's donut
(`tabs/holdings/DrillTree.tsx`, recharts `PieChart`) is paired with
`SliceTable` for the SAME rows, and `SliceTable` is also the ONLY view shown
in place of the donut whenever a slice's denominator is invalid (signed, zero
or unknown) -- confirmed by import in `component-census.json` (`SliceTable`,
2 usedIn sites: the alternative-state render and the normal paired render).
Both charts in this tree have a table equivalent; the census's row-count
confirms there is no third chart anywhere under
`pages/InvestorReporting/**` that lacks one.

## Narrow-width (390px) behaviour

Visible in `fe-s-11_page_390.png`: the firm dropdown and client search wrap
onto their own row below the header badge (index.tsx's own documented
amendment from the FE-s-2 drain, rows `IRPT_FNTEND-W1-S4`/`-S3`, "so they
re-flow at narrow widths instead of clipping"); the tab strip's three labels
truncate the row rather than wrapping vertically (browser default overflow,
acceptable at this width, no content is lost -- `HOLDINGS` is simply
off-screen-right, reachable by scroll); the period-preset row wraps into two
lines; the export/preview PNGs (`fe-s-9_export_modal_390.png`, from FE-s-9's
own deliverables, present in this same folder) show the modal's preview
column scrolling horizontally rather than clipping, per `ExportModal.tsx`'s
own `data-slot="preview-scroll"` comment ("a narrow viewport scrolls it
horizontally rather than clipping it").

## Summary

Where this order's own captures succeeded (the page/Reporting tab) and where
an earlier cell's own captures are available as reference (export modal, both
print templates, Analysis/Holdings tabs pre-crash), the Investor Reporting
surfaces consistently use the SAME reused header/tabs/panel/dropdown
components, the SAME brand palette (electric-purple single accent, navy
headings, cool-grey canvas, white cards/sheets), and the SAME logo treatment
as the rest of the portal and the print package -- one brand across the
dashboard and the exported document, as FWD-12 and FWD-8 require. The one
disputable colour-law gap (`AppliedBranding.tsx`, never mounted anywhere) and
the one reproducible crash on a one-firm catalogue (blocking three of this
order's six fresh captures) are both recorded as surprise rows rather than
silently smoothed over by substituting an old screenshot for a new claim.
