# RB-s-13 result: render and keyboard coverage over the inventory

TO `DSGN_REBRND.TO-RB-s-13` | worker `0.9.0_WK_DSGN_REBRND~3` | workspace `wk-dsgn_rebrnd-3b` @4721f1f6ee | portal `wk-dsgn_rebrnd-3b` @a65b939a.
Both repos equal `feature/d13-visual-elevation` at the start. At the end, portal is still @a65b939a. The workspace feature branch
gained one commit (962874be33, a COO checkpoint log) that touches nothing under `DSGN_REBRND`, `design/brand` or `portal`.
So the measured tree did not move.

## Coverage, stated against the inventory's denominator

Denominator: `design/brand/portal-surface-inventory.json`, 99 rows over 24 routes. 96 rows carry a render obligation and 58
carry a keyboard obligation.

| obligation | on record | read |
|---|---|---|
| render | 96 of 96: one PNG per `route\|state` key, mapped in `rb13-coverage.json` | 96 of 96 looked at |
| keyboard walk | 58 of 58: 1,379 stops, a clipped screenshot at every stop, all tiled into one sheet per walk under `walks/` | 58 of 58 sheets looked at |

**Does each render show its named state?** Per-row detail is in `rb13-state-reached.json`.

| verdict | rows |
|---|---|
| YES: the render shows the named condition (defects noted) | 65 |
| YES-NO-VISIBLE-DIFFERENCE: condition constructed, page draws nothing that depends on it | 6 |
| NO: the render shows a different condition | 23 |
| NOT-RENDERABLE: the product has no on-screen form (row W3-S1) | 2 |
| **total** | **96** |

The 23 NO rows break down as follows (row W3-S3):
- **12 DEFAULT rows.** These routes have no ui-smoke fixture, and the live dev plane answers the inert token with 401. So the
  render shows the route's error handling, not populated data.
- **10 EMPTY rows.** Without a fixture, the only empty body the harness can construct is a bare `[]`. Under it, nine routes fall
  to the app error boundary and `/factor-tilts` renders ERROR.
- **1 toggled row.** `/valuations` renders no control to toggle while its data is refused.

`rb13-coverage-check.py` reads COVERED either way. It proves a render exists, not what the render shows.

## Method

- **Capture harness.** `rb-s-13_capture.mjs` uses ui-smoke.mjs's own mechanism: system Edge headless, 1440x900, the
  `/auth/refresh` stub, exact-origin CORS, and a full-page PNG. Each render prints `LOC` and `CANVAS`. 96 of 96 printed
  `rgb(244, 246, 250)`, and 94 of 96 landed on their route; the two exceptions are the no-permission redirects.
- **How each state was constructed:**
  - DEFAULT: a fixture where one is consumable (`rb-s-9-market.json` for /market, `rb-s-9-attribution.json` for /positioning
    and /attribution), otherwise the live plane.
  - EMPTY: every data request answered 200 with its fixture body emptied (arrays become `[]`), or a bare `[]`.
  - LOADING: every data request held.
  - ERROR: every data request answered 503.
  - TOGGLED: the route's own control, found in a probe pass and clicked.
  - NO-PERMISSION: the denying claim for the route's gate.
  - Auth routes: each state driven through the page's own form and a stubbed `/auth/*` answer.
- **Keyboard walk.** Tab from a blurred document until focus returns to the first stop. At each stop the harness records the
  element, `:focus-visible` and the computed ring, and takes a clipped screenshot.
- **Plan.** `rb-s-13_build_plan.py` emits one job per obligation row from the inventory. It printed 96 jobs, 96 distinct keys and
  58 walks.

### A defect in my own instrument, found by reading and corrected

The first run counted any re-seen element as a wrap. A native date input moves focus between its segments without changing
`document.activeElement`, so four walks ended at their first date input: `/investor-reporting` default and error, and
`/trade-submission` default and error. After the correction, only a return to the first stop counts as a wrap, and a repeat
of the previous element counts as a segment move.

All 58 walks were re-run with the corrected rule:
- 53 matched the original stop sequence exactly, so their sheets stand.
- The four date-input walks now reach the rest of each page (31 and 34 stops) and replace the truncated sheets.
- The fifth difference was `/attribution` toggled-panel failing on mount in the parallel re-run. Three sequential re-runs
  reproduced the original walk exactly (row W3-S6).

## Criteria as run

| id | deciding output | verdict |
|---|---|---|
| RB13-AC1 | `RENDER-OBLIGATIONS: 96 of 99` / `VERDICT: HAS-OBLIGATIONS`, rc=0 | PASS by output |
| RB13-AC2R | `COVERED: 96 of 96 \| distinct PNGs used 96` / `VERDICT: COVERED`, rc=0 | PASS by output (see the NO rows above for what COVERED does not measure) |
| RB13-AC3 | `LOC : /market`, `CANVAS: rgb(244, 246, 250)`, `rc=0`; PNG read | PASS by output |
| RB13-AC4 | judgment: recorded below | UNVERIFIABLE-BY-INSTRUMENT (3.0.0_SA_CVO at L9) |

**RB13-AC4 (judgment), for 3.0.0_SA_CVO at L9.**
- Every one of the 96 render obligations has a render on record, and I read each one.
- Every one of the 58 keyboard obligations has a complete walk.
- Coverage is stated against the inventory's 96 and 58.
- What each render actually shows is in `rb13-state-reached.json`. I do not claim a named state for a render that shows a
  different one.

## What the LOOK found (rows filed)

- **W3-S3** (ARMED): 23 obligations are not rendered in their named state, and the coverage check cannot see that.
- **W3-S4** (ARMED): failures drawn as data, EMPTY or LOADING on seven routes. The sharpest is /market's RSI and Fear & Greed
  showing "50 Neutral", timestamped now, while every request fails.
- **W3-S5** (INERT): a dozen non-designed state treatments and developer text on client surfaces.
- **W3-S6** (INERT):
  - Keyboard: the upload drop zones on /data-refresh and /trade-submission never take focus; /portfolios puts two stops on
    invisible chart internals; one in five /attribution loads failed on mount.
  - Visual: the RSI "90D" marker is clipped; /trade-submission's fields are mid-grey inside the band.

## Not done, with reason

- **No fixture was minted and no real bearer was used.** `portal/.frontend-dev/testing/` is outside `<paths>`, and minting a live
  token is not this order's act. So the 12 DEFAULT rows without fixtures show the live plane's 401 handling.
- **No defect was fixed.** The BOUNDS say render and read, never edit.
- **Dev server.** Stopped before the final report.
