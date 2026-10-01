# DSGN_AMGTV1 round 21 -- close (issuer 2.0.0_SA_COO~D, 2026-10-01 ~16:5xZ)

**Rectangle:** the CTO's ruling msg 27914 (on round 20's shot 009) + 27927 (FWD-13 reconciliation accepted; the close also reads one
Model-tab tooltip). One DIRECT ACT, AV-y-1: the figure tooltip stays inside its pop-up and its face shows no Bloomberg code. Deadline
21:30Z, otherwise drop to da0b3bd7.

## The act and the issuer's drain repairs

| step | portal | what |
|---|---|---|
| AV-y-1 (worker ~68) | d47673eedf | FigureTooltip + StatTile: upward (`bottom-full max-w-full`); face = plain label; no "mnemonic" row; `data-mnemonic` carries the code. Outer ca85e04a70 (proof VALID, complete) |
| drain | 9ccab761 | merge; CLOUD fde85c1880 (needed 2, dropped 0, foreign 0) |
| repair 1 | ef679a8a | ModelTab's what-moved line (ModelTab.tsx:643-647, AMGT_CORPUS's) passes its OWN `mnemonic` row: FigureTooltip filters it. Found by reading ModelTab for the CTO's Model-tab ask |
| repair 2 | **3c37a01c** | the live probe on ef679a8a read the Model SHEET cells clipped: upward + width-capped in a narrow `<td>` inside `overflow-x-auto` showed a "source" sliver (hover-20261001T161516Z shot 08), a regression AV-y-1 introduced. FigureTooltip takes `placement` ('below' default = the pre-round classes); HeaderCards passes 'above' |

ModelTab.tsx is not edited at any step. On 3c37a01c: `tsc -b` rc=0; tipface (amended with the what-moved case: fails 2 faults on
d47673ee), namecard, chattercell, headerline, nolabel, cardface 3/3; 14 of 14 harnesses.

## The real run (5174 on 3c37a01c, CTO~Z 27961: 0 diff lines, HTTP 200)

ARM posted 16:32Z (laptop DISARMED 16:30:17Z and rebooting, 27965); every run self-disarmed; final DISARM 16:45:38Z, posted.

**Hover probe** (`round21/checks/hoverprobe.mjs`: walk.mjs never hovers; this hovers each anchor and measures CLIP against every
clipping ancestor and the viewport, COVER by hit-test with the tooltip's pointer events on, CODE on the visible text, CARRY):

| name | run | header cards | Financials | Market Features | Model sheet cells | what-moved | clean |
|---|---|---|---|---|---|---|---|
| BA US | walk/hover-20261001T163908Z | 4/4 | 2/2 | 1/1 (row 2 carries no figure) | 3/3 (Revenue/Sh, EPS, BVPS) | 3/3 | **13 of 13** |
| AMD US | walk/hover-20261001T163947Z | 4/4 | 2/2 | 1/1 | 3/3 | none on this name | **10 of 10** |

The two runs before these failed on the probe's own viewport parking (anchors at the screen's bottom edge, then at its top); no product
byte changed between them and the clean runs. Earlier runs on 9ccab761 / ef679a8a are kept (hover-20261001T160250Z, -161516Z, -161557Z)
as the record of the regression and its repair.

**Regression walk** `tmp/ui-walk/20261001T164049Z` (BA, AMD, TSM): 11 unique findings (round 20: 15), 0 guard aborts, 0 API issues,
walk void: no. `raw-code` 4 -> **0**. `occluded-popover` 1 remains: walk.mjs's check is blind to a pointer-events-none tooltip (shot 010
shows it unobstructed; row DSGN_AMGTV1-Z-S11). Unchanged classes: `design:contrast` 6, `timeline:no-event-element` 2 (AMD, TSM: none
served), `format:money`, `layout:truncated`.

**Not read:** a Model-tab what-moved tooltip on AMD (it serves none); TSM by the probe (walk.mjs only).

## Freeze candidate

Per 27914 ("it must walk clean by 21:30Z"): walked clean 16:39Z. **Portal DEV 3c37a01c** (LOCAL) replaces da0b3bd7 as DSGN's freeze
candidate.
