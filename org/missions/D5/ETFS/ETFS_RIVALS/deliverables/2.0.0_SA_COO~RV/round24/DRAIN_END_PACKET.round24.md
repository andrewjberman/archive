# ETFS_RIVALS round 24 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~21:1xZ)

One cell, RIV-cu-1: the dialog chart's UI, Andrew's three asks of ~19:0xZ (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261007_190xZ_RIVALFUNDS_SMOKED_POPUPS_GOOD_CHART_UI_NEXT.md`;
ROUND_ANALYSIS.round22 ADDENDUM 1 and 2). Issuance ad4c7c86d2; build b6219703f9; proof 268cd34874; close 0e527447fe;
merge 1974372f40 on site-Z CLOUD (LOCAL). **Not deployed:** the live Lambdas are at 6124b079f3 (rounds 15 to 23).

## Mechanical criteria

cu-1.AC1, cu-1.AC2, cu-1.AC3 PASS 0 failures, re-run by the issuer on the branch; proof instance VALID; the check files
are unchanged by the worker. On merged CLOUD 180673413d: package suite 880 passed, 2 skipped, 0 failed; 30 of 30 check
files under `round15/checks/` PASS 0 failures. One file of product changed: `render.py` (+47 / -20). The page's one
script went from 7,369 to 9,348 bytes; `CHART_CSS` from 308 to 1,588 bytes.

## What was built, against his words

| his words | built |
|---|---|
| the price/date on hover "much more focal, bold, and obvious" | the read-out sits ABOVE the curve inside the frame: the price with its currency at 34px weight 800, the date at 22px weight 700, the price's source at 15px; a dashed guide line and a dot follow the pointer |
| the tooltip, "especially when hovering over a buy/sell moment ... much more dramatic" | one tooltip per chart, shown on hover or keyboard focus of a marker: a 26px weight-800 head line ("Bought $10,592,358"), then the date, basis points and trade count at 17px; green for a buy, red for a sell; the marker itself grows |
| "a box around the chart ... clear dates on x-ticks ... a little more space" | a bordered, rounded frame with its own background; five dated ticks under the plot in every range ("6 Sep" for 30 and 90 days, "Oct 25" for 365); the plot is half again as tall (viewBox 600 x 300) with gridlines and 12px axis text |

## The issuer's real run (day 2026-10-07, from the branch; live inputs, local writes only)

Record `round24/real_run_2026-10-07.after_cu1.json`: status OK; index.html 1,693,555 B (served: 1,690,296; 13.2 percent
under the 1,950,000 cap); 1 script; 690 chart frames; `fund_sections` 2247 buttons, **0 missing**; audit page 1,255,777 B,
unchanged; 13 chart objects, 5,675,727 B, unchanged.

In a browser (Chromium, 1400 x 1000, the local stand-in for the gateway routes), GQGU's section of the Meta dialog:
- 30 days: ticks 6 Sep, 14 Sep, 21 Sep, 29 Sep, 6 Oct; 365 days: Oct 25, Jan 26, Apr 26, Jul 26, Oct 26.
- Pointer on the curve: read-out "744.10 USD / 2026-09-23 / implied from the holding"; the price's computed style is
  34px, weight 800. Screenshot `round24/r24_hover_curve.png`.
- Pointer on the first of 7 markers: the tooltip is shown, `data-side` buy, text "Bought $10,592,358 / on 2026-09-14,
  165 bps of the fund, 1 trade.", wholly inside the frame. Screenshot `round24/r24_hover_marker.png`.
- 365-day range: `round24/r24_365d.png`.

Looked at ONE dialog section in ONE browser. Not looked at: a sell marker, a marker near the top of the plot (the worker
reports the tooltip then flips below the marker and covers part of the curve), a narrow window, a non-dollar listing, a
frame with no price history. The page's console showed 1 error on load; it was not read (the served page was not
compared for the same error).

## Carried from the round-23 deploy (CTO msg 31327)

The republish kept 15 copies under `revisions/`, not 16: BY DESIGN. `publish_page.py` line 951 copies the audit page
only when its bytes differ from the new ones (`prior_audit != audit_b`); round 23 did not change the audit page.

## Judgment criterion owed at L9

RIV-cu-1 J1, on this run in a browser: hovering the curve, the price and date are the most prominent text of the chart;
hovering a buy or sell marker shows what was traded, when and for how much without reading small text; the chart reads
as a framed figure with dates on its x-axis. Then Andrew's own look, which is the acceptance.

## What waits, and on whom

- A deploy of round 24 is a new served act (render.py only, as round 23's was): a never-widen pair, a ledger entry, one
  republish. Asked of 1.0.0_SA_CTO~Z: today after J1, or after the 2026-10-08 11:00Z run.
- Ledger `etfs-rivalfunds-r22`: L4, L5 the 2026-10-08 11:00Z and 13:00Z runs.
