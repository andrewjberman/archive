# TO DSGN_REBRND.TO-RB-s-14 -- boundary parity -- result

Worker `0.9.0_WK_DSGN_REBRND~1`, workspace worktree `C:/tmp/wk-dsgn-1j` (branch `wk-dsgn_rebrnd-1j`, base
`ff2bcda841`), portal worktree on `a65b939a` (read only; no portal commit under this order). Rows committed at
`56997da6ea`; everything else in the commit that flips this order. All commits LOCAL.

## What was done

- The `taste` extractor was run **in place** from
  `C:/Users/AndrewBerman/Desktop/ajb_workspace/.claude/skills/taste/references/extract.js` (16,596 bytes, sha256
  `82a8831c215c9b316e7ca655af6f469570de9216db3c21b41c9eeac1fa92347a`; pinned `senlindesign/taste-skill` @`6dce223f2f`).
  It was never copied, edited, committed or fetched. A scratch Playwright harness (`rb-s-14_harness.mjs`, using the
  library `portal/scripts/ui-smoke.mjs` uses, with ui-smoke's auth stub and fixture routing) evaluated the file
  unmodified in each page at 1440x900 and took a full-page render.
- Routes, the fixed comparison set of brief IV.9: `/market` (fixture `rb-s-9-market.json`, 11 of 11 keys matched),
  `/positioning` (`rb-s-9-attribution.json`, 3 of 4 matched; the unmatched key is `allocation_summary.json`, which
  /positioning never requests) and `/portfolio-management` (no populated fixture exists, row `DSGN_REBRND-W3-S3`;
  measured with live data refused, so its figures read 0.00).
- extract.js takes no reading of numerals, chart colours, status and data tokens, `color-scheme`, or the painted
  focus ring. The harness takes those beside it, labelled separately. Painted pixel shares were read from the
  renders as a second instrument (`rb-s-14_pixels.py`). An attribution pass (`rb-s-14_shadows.mjs`,
  `rb-s-14_probe.mjs`) named the elements carrying the shadows, the Inter text, the 8px radius and the figure colours.
- `design/brand/portal-routes.json` (`rb-s-14_build.py`) mirrors `design/brand/opalinvest.com.json`'s shape: the
  same top-level keys, plus `method` and, in place of the site file's `portalDelta`, `siteDelta`, one entry per
  IV.3 dimension. The comparison cites the site by JSON pointer and never restates a site value. The portal
  canvas therefore occurs once in the file, as the measured `color.canvas.hex`.

## Criteria as run

| id | invocation (verbatim, `<WS>` = `/c/tmp/wk-dsgn-1j`) | deciding output | status |
|---|---|---|---|
| RB14-AC1 | `cd <WS> && timeout 120 python -c "...ROUTES-MEASURED..."` | `ROUTES-MEASURED: 13` / `VERDICT: MEASURED`, rc=0 | PASS-by-output (the 13 is a key count, row W1-S35; routes 3 of 3 in `pagesAnalyzed`) |
| RB14-AC2 | `cd <WS> && timeout 120 python -c "...SITE-CANVAS..."` | `SITE-CANVAS: #F4F6FA PORTAL-FILE: True CANVAS-IN-PORTAL: True` / `VERDICT: PARITY-CANVAS`, rc=0 | PASS-by-output |
| RB14-AC3 | `cd <WS>/portal && timeout 120 node scripts/ui-smoke.mjs market <deliverables>/rb-s-14_market_final_1440.png --port 5190; echo rc=$?` | `LOC   : /market`, `CANVAS: rgb(244, 246, 250)`, `rc=0` | PASS-by-output; PNG read |
| RB14-AC4 | judgment | the table below | RECORDED (L9, `3.0.0_SA_CVO`) |
| RB14-AC5 | judgment | the on-demand half listed below; the walk is not this worker's | RECORDED (L9, `3.0.0_SA_CVO`) |

The AC3 render was read. It ran without fixtures, as written: light canvas, band panels, EMPTY in Trending
Topics, Top/Bottom Performers and Daily Cloud, ERROR in U.S. Regime and in the tab body with one cause and a
retry, and the Global RSI bars still lime and yellow (row `DSGN_REBRND-S3`).

## The IV.3 table, side by side (RB14-AC4 input; no verdict)

Site values are from `design/brand/opalinvest.com.json`; its three pages are listed in the order `/`,
`/investment-platform/`, `/opal-ai/`. Portal values are from `design/brand/portal-routes.json`, route order
`/market`, `/positioning`, `/portfolio-management`. "Stands on" names what the difference sits on, when there is one.

| Dimension | Site | Portal | measuredComparison | Stands on |
|---|---|---|---|---|
| Typeface | Lato, exclusive (313 / 332 / 187) | Lato 1668 / 692 / 345; Inter on 34 elements of /market, all svg text/tspan in the Daily Cloud word cloud | EQUAL on 2 of 3; /market differs by 34 of 1702 | a chart inside a band panel |
| Numerals | Lato tabular (brief IV.3; the file takes no numeral reading) | Lato, `tabular-nums` on 373 / 74 / 17 of 373 / 74 / 17 digit-bearing elements | EQUAL to the brief's value | -- |
| Canvas | `#F4F6FA`, DOM share 67.1 / 64.0 / 56.3 % | body background `#F4F6FA` on 3 of 3; DOM share 39.4 / not in top 8 / 41.9 %, pixel 16.42 / 16.43 / 24.64 % | value EQUAL; share DIFFERS | the `#0A1733` band: DOM 38 / 46.4 / 48.7 %, pixel 73.89 / 45.58 / 48.27 %, every rendered panel (site: 31.1 / 20.9 / 20.3 %) |
| Navy's role | `#163372` text and hairline, 0.4 / 0.2 / 0.4 % | `#163372` title and active-tab ink, pixel 0.06 / 0.06 / 0.18 %; not a surface | EQUAL | -- |
| Status colours | none in the file | 4 `--status-*` tokens; the 270 +/- figures on /market paint `#2DCE89` x147 and `#F5365C` x123, matching no token (row W1-S37) | SITE-HAS-NO-VALUE | -- |
| Chart colours | none in the file | 23 `--data-*` tokens, disjoint from `--status-*`; series fills `#10B981` / `#3B82F6` on /positioning | SITE-HAS-NO-VALUE | the charts-keep-their-colour ruling |
| Loudest colour | `#5F3BE3` accent at 1.0 / 0.7 / 0.9 % | /market bucket `#F83858` 0.121 % (red figure text); /positioning `#3888F8` 10.548 % (the Equities series); /portfolio-management `#5838E8` 0.255 % (the accent button) | EQUAL on /portfolio-management; DIFFERS on /market and /positioning | /positioning: a chart series; /market: figure text on the band |
| Radius | 2, 3, 4px + pill + circle; no mid-range | 3, 4, 8px + pill; 8px on 47 / 27 / 23 elements | DIFFERS | the band: 40 / 26 / 22 of the 8px elements stand on `#0A1733` |
| Shadows | 0 | painting on 5 / 1 / 2 elements: nav-rail shadow-lg (3 of 3), the Optimization Report band panel, 4 red 12px glows on /market markers | DIFFERS (row W1-S36) | bands and chart markers |
| Focus ring | `rgb(95,59,227) 0 0 0 2px` | white 2px then `#5F3BE3` 2px (`0 0 0 4px`); `:focus-visible` on the first stop 3 of 3; 0 `outline: none !important` rules | colour and width EQUAL; the portal adds a 2px white gap | -- |
| `color-scheme` | n/a | `light` on html and body, 3 of 3 | SITE-HAS-NO-VALUE | -- |

"Loudest" is defined as the pixel bucket (4 bits per channel) holding at least 0.1 % of the render with the
highest HSV saturation x value. The hex values are bucket centres. Outside IV.3, the file also records these
differences: weights 300-700, with 600 dominant on /market, against the site's 400 and 700; h1 30px/700 with
0.75px tracking against 72px/700 normal; and a 50/50 two-column grid on /portfolio-management against the
site's 40/60.

## On-demand half for RB14-AC5

- `design/brand/opalinvest.com.json` and `design/brand/portal-routes.json`.
- Portal renders at 1440 (full page): `rb-s-14_market_extract_1440.png`, `rb-s-14_positioning_extract_1440.png`,
  `rb-s-14_portfolio-management_extract_1440.png`; and the AC3 capture `rb-s-14_market_final_1440.png`.
- `rb-s-14_side-by-side_1440.png`: the two files' values side by side, one row per IV.3 dimension, with the three
  portal renders as thumbnails. It is a render of measurements, **not of the site**. No site render is on record,
  and a new capture of opalinvest.com is egress this order carries no word for (row W1-S34). The site half of
  the pair is ABSENT.

## Controls

- AC2 negative arm: the builder re-run with the measured body background replaced by `rgb(195, 202, 218)`,
  written to scratch; the verbatim AC2 expression there reads `CANVAS-IN-PORTAL: False` / `VERDICT: NO-PARITY`.
  In the real file, `F4F6FA` occurs exactly once, in `color.canvas.hex`.
- AC1 blindness: the verbatim AC1 expression on a bare `{"a":1,"b":2,"c":3}` file reads `VERDICT: MEASURED` (row W1-S35).
- Determinism: AC3 run twice, with the same LOC and CANVAS and rc=0 both times. The pixel and build steps were
  re-run after a lint-only fix, and both outputs came out byte-identical (sha256 `460098ab...` portal-routes.json,
  `a2e8064f...` pixel shares).

## Rows

`DSGN_REBRND-W1-S34` (no site render; egress), `-W1-S35` (AC1 counts keys), `-W1-S36` (shadows no longer agree),
`-W1-S37` (/market figure colours outside both token families). All OBSERVATION / INERT, committed at `56997da6ea`.

## Not done

- The human walk (RB14-AC5), which is L9's.
- A site-side render (row W1-S34).
- The skill's step 3 (tasteDNA), because this is the step-1 measurement.
- A populated /portfolio-management, because no fixture exists (row W3-S3).
- Any fix: every difference above is recorded, not remedied, since this order's grant is the parity file and the channel.
