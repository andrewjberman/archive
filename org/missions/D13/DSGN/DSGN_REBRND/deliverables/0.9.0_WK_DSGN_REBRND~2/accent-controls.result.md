# DSGN_REBRND.TO-RB-s-5 -- Amendment 1 result (0.9.0_WK_DSGN_REBRND~2)

Worktree pair `C:/tmp/wk-dsgn-2c` (workspace `wk-dsgn_rebrnd-2c` from 3b45dfb5e3; portal `wk-dsgn_rebrnd-2c`
from a65b939a). Portal commit **a7c4fa4f** (12 files). Dev server on port 5193. Everything is LOCAL; nothing
was pushed, merged or fetched.

Round 1's work stands untouched: the one control vocabulary (`Controls.tsx`), weight-and-rule active states on
every toggle and segmented control, chartreuse retired, `::selection` on the accent. The duration-ladder canon
lock is untouched.

## 1. The five identity sites (Andrew's budget)

| # | site | file:line at a7c4fa4f | was (a65b939a) | now |
|---|---|---|---|---|
| 1 | page-title rule | `src/components/PageHeaderVariants.tsx:39` | `bg-[hsl(var(--foreground))]` | `bg-[hsl(var(--semantic-action-primary))]` |
| 2 | header subtext | `PageHeaderVariants.tsx:54` (the `<p>`; checker anchors at :51) | `text-[hsl(var(--foreground))]` | `text-[hsl(var(--semantic-action-primary))]`; the `<h1>` stays navy |
| 3 | active tab | `src/components/TabNavigation.tsx:69-70` | navy text + navy border | accent text + accent border, still `font-bold`; inactive unchanged |
| 4 | sidebar active item | `src/App.tsx:192-193` | white bold + white `border-l-2`, no fill | accent fill, KEEPING white bold label and white `border-l-2` rule |
| 5 | user avatar | `src/App.tsx:386` | grey ring, no fill | accent fill, white initial (the grey ring is dropped; the table's "becomes" names only the fill) |

The markup shapes the checker anchors on are unchanged (`w-[3px]` div, `{description && (` paragraph, the
`isActive ? '...'` branches, the `rounded-full` div wrapping `{user?.name...}`).

## 2. The favicon

- `public/favicon.svg` (1,577 B): a `#5F3BE3` circle filling a 100x100 box; the three paths of
  `public/logos/opal-icon-white.svg` (1,606 B) copied byte-for-byte by `rb-s-5r_build_favicon_svg.py`, which
  read its own output back: `PATHS-BYTE-EQUAL: True`, mark box 59.627 x 60.000 of 100 (0.60 of the diameter),
  centred at offset 20.1864, 20.0000.
- `public/apple-touch-icon.png` 180x180 (6,812 B), rendered from the SVG by `rb-s-5r_render_icons.mjs` with the
  same playwright-core + system Edge as `scripts/ui-smoke.mjs`, SVG inlined as a data: URL. Pixel census read
  back from the written bytes: indigo 62.3%, white 12.7%, transparent 20.8% (the corners outside the disc),
  antialias 4.2%; probes corner `rgba(0,0,0,0)`, ring `rgba(95,59,227,255)`.
- `index.html:5` `rel="icon"` -> `/favicon.svg`; `:6` `rel="apple-touch-icon" sizes="180x180"` ->
  `/apple-touch-icon.png`. `favicon.png` and `logos/opal-icon-color.svg` are left in place.
- Nothing was fetched from opalinvest.com or any other site.

READ before the flip:
- `rb-s-5r_favicon_32.png` (32x32) and `rb-s-5r_favicon_32_x8.png` (its pixels magnified 8x): an indigo disc with
  the white two-rounded-squares mark centred; the mark's strokes are about 2px at 32px and stay distinct.
- `rb-s-5r_favicon_context.png`: the icon at 16px and 32px beside a tab title, on a white tab strip and on a
  dark one. On both it reads as an indigo sphere with a white mark; at 16px the mark's inner detail softens but
  the disc and the white mark are distinct.
- `portal/public/apple-touch-icon.png` (180x180): a crisp indigo disc, white mark centred.
- For L9: the touch icon's corners are transparent because the SVG is a circle. iOS is reported to composite
  transparent touch-icon pixels onto black; that is recalled, not measured on any device here.

## 3. The carriers of the rule

The order's seven, all updated:
1. `portal/DESIGN.md` C8 (now :351-359) replaced with the order's verbatim text.
2. `portal/DESIGN.md` :7 (front-matter description), :419-420 (Do), :426 (Don't).
3. `portal/CLAUDE.md:52-54`.
4. `design/systems/portal/DESIGN_SYSTEM.md` :64 and :97.
5. `.claude/skills/frontend-dev/SKILL.md:58-60`.
6. Code comments: `PageHeaderVariants.tsx:34-38` and `:52-53`, `TabNavigation.tsx:64-68`, `Controls.tsx:2-3,7-11`.

Found and NOT on the list (row `DSGN_REBRND-W2-S18`): updated in grant -- the `DESIGN.md` front-matter
`components.tab-active` token (navy -> indigo), `DESIGN.md:435-436` ("accent rationed to one per view", now
qualified), `Controls.tsx:18`, `SentimentGauge.tsx:49`, `MarketRegimeIndicator.tsx:61`,
`OptimizationSummaryHeader.tsx:184-186`. Read and left because still true: `index.css:304-307` and `:500-503`,
`Controls.tsx:59-62`. Out of grant, not edited: the brief's O4 (`docs/briefs/portal-visual-elevation-brief-20260911.md:62`)
and the PRD's FWD-4.

## 4. RB5-AC5R input -- the accent enumerated per route (RECORDED, NO VERDICT)

From `rb-s-5r_accent-walk.log` (DOM walk: every visible element whose computed background, own text, border,
border-image, fill, stroke or box-shadow resolves to `rgb(95, 59, 227)`), plus the three criterion PNGs.

| route | persistent ACTION | identity sites present | OTHER | data accent |
|---|---|---|---|---|
| /positioning | 0 | 4 of 5: 1, 2, 4, 5 (no TabNavigation on this route; its MODELS/ETFS/SATELLITES is a segmented control, navy weight and rule) | sidebar border-image (row W2-S19) | 0 |
| /portfolio-management | 1: `Upload Portfolio` (1217,158 160x32) | 5 of 5 (tab = ALPHA) | sidebar border-image | 0 |
| /market | 0 | 5 of 5 (tab = MULTI-ASSET) | sidebar border-image | 0 |

- The walk lists a second OTHER per route: a `<span>` INSIDE the subtext `<p>` (the description's own child).
  That is site 2, which the walk's classifier did not reach because it tested for an `<h1>` sibling on the
  element itself. It is my instrument's miss, not a seventh place.
- /positioning and /market carry no primary action at all, and /portfolio-management's one sits inside a
  `#0A1733` band, where C8 says the band carries no primary action -- both already on round 1's row
  `DSGN_REBRND-W1-S20`, unchanged by this amendment.
- Tabs, toggles and segmented controls: no option on the three routes has an accent fill. The only accent tab
  treatment is TabNavigation's active tab (text + 2px rule, no fill); every segmented control reads weight and
  a rule (the PNGs: WTD, 90D, Portfolio, Characteristics, INT, MODELS).
- Sidebar active item with its fill ignored: white bold label plus the white 2px left rule
  (`border-l-2 border-[hsl(var(--palette-white))]`); in the collapsed rail the captures show the icon-only
  square, whose left rule is 2px of white against the indigo fill.
- The avatar sits on the band: its indigo fill against `#0A1733` is 2.72:1; its white initial on the indigo is
  6.52:1. Recorded, not judged.
- Loudest non-brand colour: /market's Global RSI lime-to-yellow bars, a chart series in the data family
  (untouched; "the charts keep their colour"), and the canon ladder hues on /positioning (locked).

## 5. RB5-AC6 input -- the counterexample walk (RECORDED, NO VERDICT)

Each route: focus a secondary control by keyboard (Shift+Tab, Tab, so `:focus-visible` paints), select the
`<h1>`, enumerate.

| route | focused (focus-visible) | selected | persistent ACTIONS | identity sites (not counted) | transient |
|---|---|---|---|---|---|
| /positioning | button ETFS (true) | "POSITIONING" | 0 | 4 | ETFS's accent ring (box-shadow) |
| /portfolio-management | button COLLAPSE (true) | "PORTFOLIO MANAGEMENT" | 1 (Upload Portfolio) | 5 | none: COLLAPSE sits in a band, where C11's ring is `#E8ECF5`, not the accent |
| /market | button 1D (true) | "MARKET OVERVIEW" | 0 | 5 | none: 1D sits in a band (as above) |

Focusing a secondary and selecting text moved the persistent ACTION count by 0 on every route. The selection
highlight is a `::selection` pseudo-element: visible as indigo behind the title in the walk PNGs, and outside
every element's computed style, so it cannot enter the count.

Instrument correction, disclosed: the walk's first run landed focus on `<body>` on /portfolio-management
because its Resume button is disabled without a fund loaded. The script was changed to take enabled
candidates only and to print where focus landed; the log in this folder is the second run, over all three routes.

## 6. Criteria (final committed tree, portal a7c4fa4f)

| id | invocation (short) | deciding output |
|---|---|---|
| RB5-AC1 | `bun run typecheck` | `rc=0` |
| RB5-AC2 | `ui-smoke positioning` | `LOC /positioning`, `CANVAS: rgb(244, 246, 250)`, `rc=0` |
| RB5-AC3 | `ui-smoke portfolio-management` | `LOC /portfolio-management`, `CANVAS: rgb(244, 246, 250)`, `rc=0` |
| RB5-AC4 | chartreuse count | `CHARTREUSE: 0`, `VERDICT: RETIRED` |
| RB5-AC5R | judgment | recorded above, no verdict |
| RB5-AC6 | judgment | recorded above, no verdict |
| RB5-AC7 | `ui-smoke market` | `LOC /market`, `CANVAS: rgb(244, 246, 250)`, `rc=0` |
| RB5-AC8 | `rb5-accent-check.py` | `SITES RESTORED: 7 of 7`, `VERDICT: ACCENTS-RESTORED` (0 of 7 at this worker's start) |

## 7. Not done

- The sidebar rail's accent `border-image` (`App.tsx:265`): not named by the order, left in place, row
  `DSGN_REBRND-W2-S19`.
- The brief's O4 and the PRD's FWD-4 still state the retired rule: out of grant, row `DSGN_REBRND-W2-S18`.
- The workspace `portal` gitlink is not moved; the portal commit lives on the portal branch only.
