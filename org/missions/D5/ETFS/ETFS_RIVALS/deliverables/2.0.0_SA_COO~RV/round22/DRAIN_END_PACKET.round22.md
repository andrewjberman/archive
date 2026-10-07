# ETFS_RIVALS round 22 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~15:5xZ)

One cell, RIV-pm-1, the second display cell of ROUND_ANALYSIS.round20 plus, by amendment before any spawn, the marker
repair of row ETFS_RIVALS-Z-C-S64 (CTO ruling msg 31031). Issuance 96792f2f46; amendment 6ce602bd1e; build 1a829c5a1f;
the issuer's strip fix ef6dbb5eee; close 04e8520123; merge c6ac7335a5 on site-Z CLOUD (LOCAL). Nothing of rounds 15 to 22
is deployed or served. The pin for the Lambda deploy now holds rounds 15 to 22.

## Mechanical criteria

pm-1.AC1, pm-1.AC2, pm-1.AC3 PASS 0 failures, re-run by the issuer on the branch; proof instance VALID. On merged CLOUD
23d65887ca: package suite 876 passed, 2 skipped, 0 failed; 26 of 26 check files under `round15/checks/` PASS 0 failures.

## The CTO's proof for row C-S64, on the real day (msg 31031)

Real run of day 2026-10-06 from merged CLOUD 23d65887ca (live inputs, local writes only): record
`round22/real_run_2026-10-06.after_pm1.json`; `round22/marker_proof.py` against the run made BEFORE the fold (round 19),
record `round22/marker_proof_2026-10-06.json`.

| The ruling's term | Read |
|---|---|
| GQGU's 7 Bloomberg keys hold the 86 | **86 of 86 found by content** (side, start, end, dollars) under AAPL 12, LLY 10, LRCX 9, META 20, MU 9, PM 19, UNH 7 |
| Total markers per fund equal the run before the fold, all 13 funds | **11 of 13 reconcile exactly** once round 22's two other changes are counted (213 zero-dollar markers dropped: BIDD 24, CGIC 118, ETFT 1, SCHY 54, TXUE 16; 3 page-day markers added: GQGU 2, IDVZ 1). **BASG holds 10 more and GQGU 33 more**, every one under a key that existed before: trades the fund made under another key, now gathered by the one-key rule (cause D of the R3 read; for example BASG GOOG and SPCX, GQGU IBKR 13 and META 1). No fund lost a non-zero marker |
| 0 dialogs show a buying section above "No trades" | **0**: no section whose strip shows a bought or sold month has an object with 0 markers; the static page holds 0 "No trades" sentences; in a browser, of 695 frames 0 show a traded strip above a "No trades" list |

So the term "totals equal for all 13" holds for 11 funds as an equality and for 2 as a gain with its cause; it is stated
that way, not as 13 of 13.

## The rest of the cell, on the same run

- Month strips: 393, every cell labelled; 393 carry `data-part` on the first cell and nowhere else; 389 of 393 agree with
  the markers' months, and the 4 that do not (CGIC AEM CN, BASG CARR, PCLG LLY, GQGU IBKR) each have a marker in the first
  month before the window's first day, the part month. Row Z-S59's 11 are down to those 4 by-design cases.
- In a browser, all 695 frames opened: 98 read "No price history is stored for this holding yet." with no svg (round 17
  counted 97 with no stored currency; the 98th is not identified here, and BIDD 6475395Z GR, a stored currency with no
  price, is the candidate); 2 read "Fewer than two prices on file in this
  range." with no svg at the opening 30-day range; 595 draw; 0 read "Chart could not load".
- Two display faults seen on the first look and fixed by the issuer on the branch before the merge (ef6dbb5eee): the
  13th cell wrapped onto a second row (round 21's strip met a 12-column grid in page_theme.py), and the part-month label
  overprinted the bar. After: 0 of 393 strips wrap; a part month is an asterisk on its label with one note under the
  strip. Screenshots `round22/r22_realrun_modal_part_month.BEFORE_css_fix.png` and `round22/r22_realrun_modal_part_month.png`
  (the after picture is the second real run's page with the final rule swapped in; the final run from merged CLOUD
  carries the rule and the 13-column grid, read from its page text).
- Page 1,695,878 B, 13.0 percent under the 1,950,000 cap; audit page 1,255,195 B, 0 scripts; the real run took 248 s
  end to end on this machine (two gold tables and the publish).

## Judgment criterion owed at L9

RIV-pm-1 J1, on this run, with RIV-pl-1 J1 if not yet graded. md-1 J1 and pd-2 J1 stay owed on the served page.

## What waits, and on whom

- 2.0.0_SA_COO~RV: the COO never-widen half for the Lambda deploy at a pin holding rounds 15 to 22, with its plan, to
  1.0.0_SA_CTO~Z. The gateway route is live (r26).
- Andrew read the served page at ~15:4xZ and saw no dialog and no 30d / 90d / 365d switch: that is the undeployed rounds
  (record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261007_153xZ_FOUR_ACTS_ANSWERED_BBG_ROUTE_GOOD_TEAMS_VIA_OPALAI_RIVALS_SMOKE_BUN_VIA_CTLPLN.md`).
