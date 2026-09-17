# DSGN_REBRND.TO-RB-s-5 -- accent rationing and one control vocabulary: result

Worker `0.9.0_WK_DSGN_REBRND~1`, worktree pair `C:/tmp/wk-dsgn-1f` (workspace `wk-dsgn_rebrnd-1f` @c8ccbdb4f2 base,
portal `wk-dsgn_rebrnd-1f` @63345fac base). Dev server on 5185. Portal work: commit `4e9e422a`, LOCAL.

## What changed (portal 4e9e422a, 12 files)

| file | change |
|---|---|
| `src/ui/components/Controls.tsx` (new) | The ONE vocabulary: `buttonClass(primary / secondary / ghost, canvas / band)` and `Segmented`. In `Segmented` the active option is weight 700 plus a 2px rule, never a filled chip. An option may carry its own hue (the canon ladder). No focus ring is defined here (RB-s-6's). |
| `src/index.css` | `::selection` is on the accent `--semantic-action-primary` (was `--warning`, orange). |
| `src/components/PageHeaderVariants.tsx` | The left rule and the description are navy `--foreground`, not the accent (C8: not a heading colour). |
| `src/components/TabNavigation.tsx` | The active tab is navy weight and a 2px navy rule (C8). Inactive tabs are weight 400 on the hairline. The accent is gone. |
| `src/components/ModelPortfolioModal.tsx` | `ModelNameTrigger` has no dotted underline (it renders as a column header on /positioning). The corner arrow stays. |
| `src/pages/Positioning/Positioning.tsx` | MODELS/ETFS/SATELLITES is `Segmented` on the canvas. |
| `src/pages/Positioning/panels/PositioningSummary.tsx` | Portfolio/Benchmark/Relative/Custom is `Segmented` in the band, with the same caps gating. EXPAND DETAILS is `secondary`. The EtfTickerTrigger header underline is removed. |
| `src/pages/Positioning/tabs/HoldingsTab.tsx` | The duration ladder is `Segmented` with each rung's own hue, in unchanged order. Characteristics/Performance is `Segmented`. |
| `src/pages/PortfolioManagement/components/OptimizationSummaryHeader.tsx` | Upload Portfolio is the `primary`; Resume is `secondary`. |
| `src/components/market-performance/{ExecutiveSummary,MarketRegimeIndicator,SentimentGauge}.tsx` | The three period selectors are `Segmented`. |

## /positioning: five idioms before, one vocabulary after

| before (base 63345fac) | after |
|---|---|
| filled accent pill group MODELS/ETFS/SATELLITES | segmented (canvas): navy, active = 700 + 2px navy rule |
| smaller filled accent pill group Portfolio/Benchmark/Relative/Custom | segmented (band): active = 700 + 2px band-ink rule |
| five-hue control, active chip FILLED with the rung hue | segmented, the same five canon hues in UST-ST-INT-LT-ULT order; active = 700 + 2px rule in the rung's hue |
| filled accent pair Characteristics/Performance | segmented (band) |
| outlined ghost EXPAND DETAILS | secondary (band) |
| dotted/solid column-header underlines | removed |

## The persistent accent, enumerated per route (RB5-AC5 input -- no verdict)

Measured by the DOM walk (`rb-s-5_accent-walk.mjs`, output `rb-s-5_accent-walk.log`). It lists every visible element whose computed background, text, border, fill, stroke or box-shadow is `rgb(95, 59, 227)`, and separates chart/svg DATA from CHROME.

| route | page-level accent (this grant) | shell accent (App.tsx, outside grant) | measured total |
|---|---|---|---|
| /positioning | 0 | 2 (active nav item, avatar) | 2 |
| /portfolio-management | 1: **Upload Portfolio** (the view's one primary action) | 2 | 3 |
| /market | 0 | 2 | 2 |

- DATA accent hits: 0 on all three routes.
- /positioning and /market carry no persistent primary action. Every accent fill on them was a state control (row W1-S20). No action was invented to spend the accent on.
- The shell's two fills are row **W1-S19** (BLOCKING on the budget clause; App.tsx is not in `<paths>`).
- Upload Portfolio sits inside a `#0A1733` band, which C8 bars a primary from. That is the W2-S5 panel divergence (row W1-S20).

Accent pixel share, measured in PIL with a +/-6 tolerance per channel on `#5F3BE3`. This is not an acceptance value: the order's 1.0% is a description of the live site.

| capture | before | after |
|---|---|---|
| /positioning full page | 0.361% (base) | 0.085% (`rb-s-5_positioning_1440.png`) |
| /portfolio-management full page | 0.423% (base) | 0.362% (`rb-s-5_pm_1440.png`) |
| /market full page | 0.290% (base) | the walk capture carries a transient selection highlight, so it is not a like-for-like number |

The walk captures (with the selection highlight on the page title) read 0.335% / 1.015% / 0.509%. The PM figure includes the selected title painted in the accent. The selection is transient and is not counted against the one.

Loudest colour on each page, read from the PNGs (RB5-AC5 input):
- /positioning: the asset-class swatches (data family) and the canon ladder labels. The accent appears only in the shell.
- /portfolio-management: Upload Portfolio.
- /market: the Global RSI bars, a lime-to-yellow gradient from `--perf-weak-pos` / `--perf-weak-pos-dark` (`RSIBars.tsx:155`). That is a chart series in the data family, which the cell permits. Untouched ("the charts keep their colour").

## The counterexample walk (RB5-AC6 input -- no verdict)

On each route the walk FOCUSED a secondary control, SELECTED the page title, and then counted:

| route | focused (transient) | selected (transient) | persistent chrome accent |
|---|---|---|---|
| /positioning | `ETFS` (idle segmented option) | "POSITIONING" | 2 (shell) |
| /portfolio-management | `Resume` (secondary) | "PORTFOLIO MANAGEMENT" | 3 (shell 2 + Upload Portfolio) |
| /market | `1D` (idle segmented option) | "MARKET OVERVIEW" | 2 (shell) |

The focused control did not add to the count on any route: no focused element appears among the CHROME rows. The selection highlight is a pseudo-element and is not an element in the count. Captures: `rb-s-5_walk_positioning.png`, `rb-s-5_walk_pm.png`, `rb-s-5_walk_market.png`.

**Limit of the walk:** no `:focus-visible` ring exists yet (RB-s-6's cell; `index.css` still sets `outline: none !important`). So "focused" here shows that focus does not recolour a secondary into the accent. It does not show what the ring will add.

## Not done, and why

- **App.tsx shell accent** (active nav item, avatar, sidebar border-image): outside `<paths>`. Row W1-S19, BLOCKING on the budget clause.
- **Chartreuse**: already retired by RB-s-4 before this cell. Row W1-S18. The index.css line was not edited.
- **`components/Button.tsx`** (a second, pre-existing variant set: default=accent, outline=accent): left as is. Rewriting it moves every page that imports it, which is wider than this cell's three routes. The one vocabulary for these routes is `ui/components/Controls.tsx`.
- **Other accent chips outside the three routes** (the 379 occurrences of the accent tokens across 132 files at base): not censused or moved. The order scopes to the three routes.
- **The focus ring**: RB-s-6's; not defined here.
