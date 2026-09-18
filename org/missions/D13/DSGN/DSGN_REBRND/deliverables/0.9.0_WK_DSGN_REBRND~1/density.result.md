# DSGN_REBRND.TO-RB-s-9 -- density -- result

Worker `0.9.0_WK_DSGN_REBRND~1`, branch `wk-dsgn_rebrnd-1h` in both repos. Portal commit `e216de95`,
rows commit `d30bc6bc32`, all LOCAL. The renders were captured at 1440x900 against populated fixtures, with
the dev server on 5187.

## What changed (portal `e216de95`)

| file | change | clause |
|---|---|---|
| `src/ui/components/panels/PanelContent.tsx` | default inner padding 24px -> 30px | C10 panel inner = spacing.md |
| `src/ui/components/panels/PanelHeader.tsx`, `PanelFooter.tsx` | horizontal inset -> 30px, so the title, content and source line share one edge | C10 |
| `src/pages/MarketPerformance/MarketPerformance.tsx` (2), `Positioning/Positioning.tsx`, `Attribution/Attribution.tsx` | page column `space-y-6` (24px) -> `space-y-5` (20px) | C10 between sections = spacing.sm |
| `src/pages/Attribution/components/StylePolicyComparison.tsx` | fixed 32px ornament; bars start 24px from the axis; the label moves outside a bar it does not fit; bar sized by a column-flex wrapper the Tooltip trigger stretches across; three `p-8` overrides removed | row S1; W1-S31 |
| `src/pages/TicketCenter/TicketCenter.tsx:174` | comment only: light canvas `#F4F6FA`, law = DESIGN.md C3 | row W1-S24 |
| `.frontend-dev/testing/rb-s-9-{market,sparse,attribution}.json` | ui-smoke `--fixtures` maps (11 / 3 / 4 URL keys, all matched) | "use populated fixtures" |

No panel, row or content was added. No figure or computation changed.

## Criteria as run

| id | output (deciding line) | status |
|---|---|---|
| RB9-AC1 | `tsc -b --noEmit` ... `rc=0` | PASS |
| RB9-AC2 | `LOC   : /market`, `CANVAS: rgb(244, 246, 250)`, `FIXTURES: 11 declared; 11 matched >=1 URL`, `rc=0` | PASS |
| RB9-AC3 | `LOC   : /positioning`, `CANVAS: rgb(244, 246, 250)`, `FIXTURES: 3 declared; 3 matched >=1 URL`, `rc=0` | PASS |
| RB9-AC4 | before/after table below | RECORDED (judgment, L9) |
| RB9-AC5 | sparse control below; row W1-S29 | RECORDED (judgment, L9) |
| RB9-AC6 | gaps 20px vs panel inner 30px, below | RECORDED (judgment, L9) |
| RB9-AC7 | `LABEL/ORNAMENT PAIRS MEASURED: 8` / `OVERLAPPING: 0 []` / `VERDICT: NO-COLLISION` | PASS |

The PNGs were read before the flip: `rb-s-9_market_populated_1440.png`, `rb-s-9_positioning_sparse_1440.png`,
`rb-s-9_attribution_after_1440.png`.

## Measurements (instrument `rb-s-9_measure.mjs`, same fixtures before and after)

| route | docHeight before -> after | share of viewport below last content, before -> after | section gaps before -> after | panel inner padding before -> after |
|---|---|---|---|---|
| /market (populated) | 3572 -> 3580 | 0.036 -> 0.036 | 24,24,24 -> 20,20,20 | 24px x2 -> 30px x2 |
| /positioning (sparse) | 1565 -> 1581 | 0.036 -> 0.036 | 24,24 -> 20,20 | 24px x2 -> 30px x2 |
| /attribution (populated) | 1601 -> 1601 | 0.036 -> 0.036 | 24,24 -> 20,20 | 32px + 24px -> 30px x2 |

0.036 = `<main>`'s 32px bottom padding / 900. On populated data, none of these routes has the lower third of empty
canvas (row W1-S30). The sparse control keeps all three panels, holds one holding per book, and ends on the
Holdings Breakdown panel's source-line footer. The contract names no page terminator and none was invented
(row W1-S29).

Divergence labels (8 pairs: QTD, YTD, 1Y and SI, each with one narrow and one wide bar):

| | bar widths (px) | pairs overlapping the ornament |
|---|---|---|
| before (portal `fb6f5023`) | 62.5, 16, 16, 66.2, 60.9, 66.2, 62.5, 44.1 | 8 of 8 (11 to 33.1 px) |
| after (`e216de95`) | 424, 29.2, 23, 424, 413.7, 424, 424, 282.7 | 0 of 8 |

The narrow bars (+0.6% at 29.2px, -0.5% at 23px) carry their label outside the bar, on the side away from the axis.

## Rows

- `DSGN_REBRND-W1-S29`: DESIGN.md has no page-terminator clause. OBSERVATION, INERT.
- `DSGN_REBRND-W1-S30`: the lower-third premise is not reproduced on populated data. OBSERVATION, INERT.
- `DSGN_REBRND-W1-S31`: the Tooltip trigger shrink-wrapped the bars, a third collision cause. OBSERVATION, INERT.

## Not done

- `space-y-6` in the other 38 files under `src/pages/` (51 occurrences across 41 files, mostly inner containers
  and modals). Only the three routes this order renders were moved.
- No page terminator (W1-S29).
- The fixtures for trending topics and the regime signals render those cards' empty or zero states. The shapes are
  approximations, so these two cards are not evidence of their populated look.
- Dense table cell padding (C10's 20px), the bars' radius and glow (C11): not this cell.
- Other Tooltip-wrapped percent-width elements in `portal/src`: not censused (W1-S31).
