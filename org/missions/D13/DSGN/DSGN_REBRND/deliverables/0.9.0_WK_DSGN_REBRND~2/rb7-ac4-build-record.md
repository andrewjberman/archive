# RB7-AC4 build record -- "Model Portfolio Summary" from the contract alone

Builder: `0.9.0_WK_DSGN_REBRND~2`, a FRESH instance of slot ~2 seated under TO-RB-s-7 Amendment 2,
with no prior context. Branch `wk-dsgn_rebrnd-2b` (workspace @c8ccbdb4f2, portal @63345fac).

**Sole design input:** `portal/DESIGN.md` at portal commit `000478c9` (read with
`git show 000478c9:DESIGN.md`; the worktree copy has not changed since that commit, because
`git diff --stat 000478c9 HEAD -- DESIGN.md` was empty). I read nothing under `portal/src/`,
`portal/design/`, `design/brand/`, `deck_generation/`, no other DESIGN.md revision, no portal
screenshot and no opalinvest.com page. I read the build kit only in the verbatim "THE BRIEF" section
my issuer inlined. I read the proof instance only after the page was built and captured, because
Amendment 2 orders that update.

Deliverables (this folder):
- `rb7-ac4-page.html` -- the page: inline CSS, no script, no external request, nothing vendored.
- `rb7-ac4-page_1440.png` -- a full-page capture at 1440 px wide (1440 x 1204). I read it before
  finishing.
- `rb7-ac4-build-record.md` -- this file.

## What rendered, as measured

- **Font: ARIAL, not Lato.** Lato is not installed on this machine: no `lato` entry is present in
  `C:/Windows/Fonts` or in the per-user font folder. The brief fixes the stack at
  `Lato, sans-serif` and forbids vendoring, so the generic `sans-serif` resolved. The measurement
  was made with CDP `CSS.getPlatformFontsForNode` over six probes (h1, description, band figure,
  table figure, table header, primary button), and all six returned `Arial` (`ArialMT` /
  `Arial-BoldMT`, `isCustomFont: false`). **The capture therefore shows Arial's metrics and
  Arial's tabular figures, not Lato's.**
  - Instrument trap: `document.fonts.check('16px Lato')` returned **true** on the same page. It
    returns true when no font face needs loading, so it cannot tell whether Lato rendered and it
    is not evidence either way.
- **Network:** 1 request total (the `file:` URL of the page) and 0 aborted. Every non-file request
  was routed to abort and logged, and none occurred.
- **Capture instrument:** Playwright 1.60.0 (`portal/node_modules`, a junction, with no install)
  driving system Chrome 153.0.8010.37 headless, viewport 1440 x 900, deviceScaleFactor 1, full page.
- **Computed checks on the rendered DOM:** exactly 1 element with an `#5F3BE3` background (the
  primary button, per C8); 0 elements carrying a `box-shadow` at rest (per C11); the split panels
  measure 546.6 px and 819.9 px wide, which is 40.0 / 60.0 (per C12).
- **Keyboard focus walk (Tab from the top):** 3 of 3 interactive elements reached
  (Download factsheet, the search input, Schedule a delivery), each matching `:focus-visible` with
  computed `box-shadow: rgb(255,255,255) 0 0 0 2px, rgb(95,59,227) 0 0 0 4px`. I read each crop,
  and the ring is visible on all three. A fourth Tab leaves the page. The crops are scratch only
  and are not deliverables.
- **What I saw in the capture:** the page is light, the panels are white with a hairline, there is
  one dark band, one purple button, and the ladder runs in UST-ST-INT-LT-ULT order top to bottom
  (table, legend) and left to right (bar). Two blemishes, which are my choices and not the
  contract's: (1) model-name text (1rem) is visibly larger than the figures beside it (0.875rem)
  in the same table row (Q10); (2) the rung labels have a min-width, so the model names line up
  within one list, but the column is slightly loose.

## Element -> clause

| # | element (brief) | built from | how |
|---|---|---|---|
| 1 | page title + one line of description | C1; front-matter `typography.page-title`, `typography.body`; C3 (ink by ground); C10 (page top margin) | h1 2.4554rem / 700 / 1.2, navy `#163372`. The description is body 1rem / 400 in navy, **not** `#6B7280`, because C3 measures secondary ink at 4.47:1 on the page field and says to use navy there. Page top padding is `spacing.lg` 45px (C10 reserves 45 for the page's top margin). |
| 2 | the page's one deliberate band, headline figure + label | C3 (one full-bleed band `#0A1733`, never the default container; `#E8ECF5` is the ink on the band; `#A8B0C0` is the band's secondary ink at 8.14:1); C11 (band full-bleed and square); C10 (band vertical padding `spacing.lg`); C1 (figures at 400); C2 (tabular); C8 (the band carries no primary action) | A full-width `#0A1733` section with radius 0 and padding 45px 30px. The label uses the `label` typography in `#A8B0C0`, the figure is 2.4554rem / 400 tabular in `#E8ECF5`, and a sub-line is in `#A8B0C0`. Nothing interactive sits in the band. |
| 3 | two-column area: summary + detail table | C12 (40/60, summary 40, gap `spacing.xs`); C3 (panel `#FFFFFF` with a 1px `#C4CBDB` hairline; sunken `#E8EBF0` as a table-header fill); C11 (`rounded.md` 4px); C10 (panel padding 30px; 20px in a dense table's cells and header); C2 (figures right-aligned, tabular, a sign on every change value); C5.6 (row dividers are a boundary at the hairline, 1.63:1 on a panel, above the 1.35 floor); C9 | A grid of `minmax(0,2fr) minmax(0,3fr)` with a 13.5px gap. Summary: panel title, a navy sentence, two stat figures, an allocation bar and a legend. Detail: panel title, the search field, and a 4-column table (Model, YTD, 1Y, Weight) with its header row filled `#E8EBF0` and navy label text (a NEW pairing, measured at 10.04:1 per C9's "measured before it ships"). |
| 4 | the five duration models with YTD, 1Y, weight | C4 (hexes and order locked, UST ST INT LT ULT top to bottom when vertical and left to right when horizontal; every canon mark carries its rung label; text naming a model is navy, never the canon hex); C2; C6 (status never paints a performance cell); C7 (the ladder is exempt from the single-hue ramp) | Table rows and legend rows run top to bottom UST, ST, INT, LT, ULT, and the stacked bar runs left to right in the same order. Each has a canon swatch, a bold rung label and a navy model name. Returns are navy with a printed `+` / `-`, and weights are unsigned (not a change value). |
| 5 | exactly one primary action "Download factsheet" | C8 (indigo `#5F3BE3` fills exactly one persistent element, white label `#FFFFFF` at 6.52:1); front-matter `components.button-primary`; C11 (`rounded.sm` 3px) | A filled indigo button at the page header's right. The rendered DOM measures exactly 1 indigo fill. |
| 6a | one secondary action | front-matter `components.button-secondary` (white, navy text, navy border); C11 (3px); C9 (navy border 12.00:1 on the panel, clears SC 1.4.11); C12.1 (the EMPTY state's one creating action) | "Schedule a delivery", placed as the creating action of the empty panel (item 7). |
| 6b | one text input | front-matter `components.input`; C9 (the input border is `#6B7280`, 4.83:1 on a panel, never the hairline); C5 (`placeholder-` is the ink role) and C5.8 (opacity 1.0); C11 (3px) | A search input labelled "Search models", with navy text and a `#6B7280` border and placeholder. The placeholder `opacity: 1` is set explicitly, per C5.8. |
| 7 | one panel with nothing to show yet | C12 (four designed states; EMPTY = one navy sentence naming what would appear, plus the one action that would create it; in the panel's own frame; navy on `#FFFFFF`); C3 panel | "Scheduled factsheet deliveries": one navy sentence and the secondary action. |
| 8 | one warning-level notice | C6 (warning `#D37C17` measures 3.15:1 and is never text on a light ground: it is an icon or fill beside navy text, always paired with a non-colour cue); C3 (every container is a panel); C9 SC 1.4.11 (the icon at 3.15:1 clears 3:1) | A white panel holding an inline-SVG warning triangle filled `#D37C17`, the word "Warning:" in navy 700 (the non-colour cue), and navy text: "Holdings as of the prior trading day." |
| 9 | a visible keyboard focus on every interactive element | C11 (`:focus-visible` ring `0 0 0 2px #FFFFFF, 0 0 0 4px #5F3BE3` on a light ground; `outline: none` without it is a violation; the ring is the only box-shadow; `prefers-reduced-motion` honoured); C8 (the ring is transient and does not count as the accent spend); front-matter `focus-ring` | The ring on both buttons and the input via `:focus-visible`, which replaces the UA outline with a transparent 2px outline. A `prefers-reduced-motion: reduce` block disables transitions and animation (the page has none). |

## Where the contract did NOT answer, and what I chose

These questions are the finding.

- **Q1. Band placement and what it carries besides the figure.** C3 says one full-bleed band per
  page but not WHERE on the page, and not whether the page title belongs on the band or on the page
  field. *Chose:* the title on the page field, then the warning notice, then the band, then the
  split, then the empty panel.
- **Q2. The headline figure's type.** The contract has no display-figure token. C1 says figures
  are 400 and titles are 700, and it does not say which a hero number is. *Chose:* page-title size
  (2.4554rem) at weight 400, tabular.
- **Q3. The stat figures in the summary.** Same gap. *Chose:* section-title size (1.5169rem) at 400.
- **Q4. C10 vs C12 on the gap between two panels.** C10: "The gap between two panels or two
  sections on one page is `spacing.sm` 20px". C12: a summary/detail split's gap is `spacing.xs`
  (13.5px). The two columns of the split ARE two panels. *Chose:* 13.5px inside the split (C12,
  the more specific clause) and 20px between stacked sections (C10), so two different panel gaps
  appear on one page.
- **Q5. "`spacing.sm` 20px in a dense data table's cells and header" (C10).** This could be cell
  padding on all four sides, horizontal only, or the panel's own inner padding when it holds a
  dense table. 20px on all four sides is not dense. *Chose:* cells and header at 13.5px vertical /
  20px horizontal, with the panel's own padding kept at 30px.
- **Q6. Is a notice a panel?** C3: "every container" is a panel, but the contract names no notice
  or banner component. *Chose:* a panel, including the 30px padding, which makes a one-line notice
  82px tall.
- **Q7. Warning icon.** The contract names no icon set, glyph or size, and does not say whether
  the glyph drawn inside a status icon is held to SC 1.4.11. *Chose:* an inline-SVG triangle 20px
  filled `#D37C17` with a white exclamation mark. White on `#D37C17` measures 3.15:1.
- **Q8. Buttons.** There is no height, padding, label type size or weight, border width, or
  hover / active / disabled value. *Chose:* 40px tall, 0 20px padding, body 1rem at 700, a 1px
  border, and **no hover change at all** (the contract gives no hover value, and C5.8 rules out an
  opacity trick).
- **Q9. Input.** There is no height, width or padding, and no typography for the field label.
  Placeholder colour is covered only through C5's role mapping (`placeholder-` is ink).
  *Chose:* 40px x 280px, 0 13.5px padding, `label` typography for the field label, and a
  `#6B7280` placeholder.
- **Q10. Text cells in a table.** The contract gives `numeral` (0.875rem) for figures and nothing
  for a text cell sitting beside them. *Chose:* body (1rem) for model names and numeral for
  figures. The row mixes two sizes, visibly.
- **Q11. Colouring a return.** C6 forbids status colours in a performance cell. The data family
  carries `data-perf-*` scales, but the contract measures none of them as text, and C5.7's
  positive/negative targets are ratios with no hex. The contract does not say whether a return is
  coloured at all. *Chose:* navy with a printed sign, and no colour on any return.
- **Q12. The minus sign.** C2 shows `+`/`-`, and ASCII hyphen-minus vs U+2212 is not named.
  *Chose:* ASCII hyphen-minus, as in the fixture.
- **Q13. Legend swatch.** There is no size, and it is unclear whether a swatch is a "chip or tag"
  (2px) or a "status dot" (pill). *Chose:* 12 x 12px at 2px.
- **Q14. Stacked bar.** There is no height or separator between adjacent canon hues. Radii are
  "2, 3 and 4px -- or a pill", and the contract does not say whether a square (0) segment is
  legal outside the band. *Chose:* a 16px bar, 2px white gaps, and 2px radius per segment.
- **Q15. Rung label typography.** C4 requires the rung label but gives it no type. *Chose:* body
  size at 700.
- **Q16. Page side margins and a content max-width.** Neither is named. *Chose:* 30px side
  padding and no max-width (reading C10's "dead canvas is a defect" as against centring the
  content in a wide gutter).
- **Q17. Page bottom margin.** It is not named, and 45px and up is reserved for the band and the
  top margin. *Chose:* 30px. (I first wrote 45px, caught it against C10, and changed it before the
  capture.)
- **Q18. "Persistent" primary action (C8).** The contract does not say whether persistent means
  sticky or fixed, or only present in every state. It gives no placement. *Chose:* the page
  header, right-aligned, not sticky.
- **Q19. The EMPTY state's action.** C12.1 asks for "the one action that would create it" and
  does not say which button style it takes. C8 rules out a second indigo, so it is secondary by
  elimination. I used it as the brief's single secondary action. Had I placed a separate
  secondary action elsewhere as well, the brief's "one secondary action" and C12.1 would have
  collided.
- **Q20. Label casing and tracking.** C1 allows tracking for uppercase under 14px, but the
  contract does not say whether labels are uppercase. *Chose:* sentence case, normal tracking.
- **Q21. The focus ring on the band.** `focus-ring-on-band` is specified, but the page puts no
  interactive element in the band, so that ring is not exercised by this page.
- **Q22. A headline figure is not in the fixture.** The fixture has model rows only. *Chose:* an
  invented total AUM of `$1,250,000,000`, labelled on the page as illustrative. The contract names
  no currency or large-number format (full digits vs `$1.25B`).
- **Q23. Precision of derived figures.** Not named. *Chose:* one decimal, to match the fixture.
- **Q24. Intra-component gaps.** The contract governs panel padding and between-section gaps
  only. Nothing covers title-to-text, label-to-input or legend rows. *Chose:* 13.5px (a ladder
  value, in a use the contract does not name), and 6px and 4px, which are **off the ladder**.
- **Q25. The rem base.** Not named. *Assumed:* 16px (set explicitly on `html`).
- **Q26. How Lato is delivered, and the acceptable fallback.** The contract says Lato only and
  "no system UI stack", but gives no font source, no `@font-face`, and no rule for what renders
  when Lato is absent. On this machine the brief's `Lato, sans-serif` resolved to **Arial**, so the
  capture tests the contract's layout and colour under a substitute typeface. A reviewer grading
  C1 against this PNG is grading Arial.
- **Q27. Forced-colours mode.** Not addressed. *Chose:* a `2px solid transparent` outline beside
  the ring, so a focus indicator survives when forced colours strip `box-shadow`.
- **Q28. Responsive behaviour.** No breakpoint or narrow-width rule. *Chose:* none built. The page
  is specified and captured at 1440 px only.
- **Q29. Where a page-level notice sits.** It is not named relative to the band or the content.
  *Chose:* above the band, directly under the page header.
- **Q30. Panel-header layout.** It is not named for a panel that carries both a title and a
  control. *Chose:* title left and the search field right, bottom-aligned.
- **Q31. Row hover / selection in a table.** Not named. *Chose:* none. The rows are not
  interactive.
- **Q32. Blended (weighted) figures.** The contract is silent on whether a summary may state
  derived aggregates, and on how their provenance is marked. *Chose:* allocation-weighted YTD
  +1.5% and 1Y +6.0%, computed from the fixture (arithmetic below), with no provenance marker on
  the page beyond the table's fixture footnote.

## Values I used that the contract does not name

| value | where | note |
|---|---|---|
| `16px` | `html` font-size | rem base (Q25) |
| `30px` | page left/right padding; band left/right padding; page bottom margin | ladder value (`spacing.md`) in uses C10 does not name (Q16, Q17) |
| `13.5px` | title-to-description, notice icon gap, band label-to-figure, summary spacing, legend gaps, table cell vertical padding, input side padding | ladder value (`spacing.xs`) in uses the contract does not name (Q5, Q24) |
| `6px`, `4px` | label-to-input gap, legend row padding; stat label-to-figure | **off the ladder** (Q24) |
| `40px` | button and input height | (Q8, Q9) |
| `280px` | input width | (Q9) |
| `1px` | secondary button and input border width | the front matter gives `borderWidth` only for `panel` |
| `12px` | swatch size | (Q13) |
| `16px`, `2px` | allocation bar height, segment gap | (Q14) |
| `2.2em` | rung label min-width | alignment only |
| `20px` | warning icon size | (Q7) |
| `#FFFFFF` | exclamation glyph inside the warning icon | `on-primary`'s value, reused (Q7) |
| `2px solid transparent` | outline under `:focus-visible` | forced colours (Q27) |
| `color-scheme: light` | `:root` | keeps UA form controls on the light scheme |
| `$1,250,000,000` | band headline figure | **invented**, labelled illustrative on the page (Q22) |
| `+1.5%`, `+6.0%` | weighted YTD and 1Y | **derived from the fixture**: YTD = .12(2.1)+.18(3.4)+.30(5.2)+.25(-1.3)+.15(-3.8) = 1.529; 1Y = .12(4.3)+.18(5.9)+.30(8.1)+.25(6.4)+.15(2.7) = 6.013 |
| page copy | description, summary sentence, notice text, empty-state sentence, footnote | written by the builder |

## New pairings measured (C9: "a new pairing is measured before it ships")

WCAG 2.1 relative-luminance ratio, computed by this builder's own function in the capture script:
navy `#163372` on sunken `#E8EBF0` **10.04**; navy on panel 12.00; navy on page 11.09; `#6B7280` on
panel 4.83; `#A8B0C0` on band 8.14; `#E8ECF5` on band 15.00; `#D37C17` on panel 3.15; `#FFFFFF` on
`#D37C17` 3.15; `#5F3BE3` on panel 6.52 and on page 6.03; hairline `#C4CBDB` on panel 1.63 and on
page 1.50; the canon hexes on panel: UST 2.80, ST 2.15, INT 2.54, LT 3.68, ULT 3.76. Every ratio the
contract also prints agrees with it. The three canon hexes below 3:1 are never the only carrier of
a model's identity on this page: each swatch sits beside its bold rung label and a navy model name
(C4).

## Where this page may sit outside the contract (for the L9 reader, not self-graded)

- C1: the page rendered in **Arial** (Q26). The CSS names Lato only, but the pixels are not Lato.
- C10: the two-column gap is 13.5px, which is under C10's 20px panel gap, because C12 governs (Q4).
- The off-ladder 4px and 6px gaps (Q24).
