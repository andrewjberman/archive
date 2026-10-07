# ETFS_RIVALS round 21 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~14:1xZ)

One cell, RIV-pl-1, cut on the CVO's L9 grades for rounds 15 to 19 (ADJUDICATION_v20 row ETFS_RIVALS-Z-C-S60) minutes
before ROUND_ANALYSIS.round20 @c9a9e27770 arrived. Issuance 722eb2804e; build 52f8b4f41d; close b1a4837abe (committed in
the worker's worktree during 0.0.0_AB_MSTR~Z's merge window); merge e3ea0014bc on site-Z CLOUD, after the pull-merge
fad25b1527. Rounds 15 to 20 are on origin (0.0.0_AB_MSTR~Z msg 30999: origin CLOUD fad25b1527 by ls-remote); round 21's
merge is LOCAL. Nothing of rounds 15 to 21 is deployed or served.

## Mechanical criterion

pl-1.AC1 PASS 0 failures, re-run by the issuer on the branch; proof instance VALID. The granted edit to ml-1.AC1.py is two
lines (arm (a): 13 cells; arm (e): 13 months at most, one repeated). On merged CLOUD 69a3834108: package suite 870 passed,
2 skipped, 0 failed; 23 of 23 check files under `round15/checks/` end PASS 0 failures.

## The real run, on the worker's branch before the merge (code root C:/tmp/wk-riv-r21-11 @1bd3c3efeb)

Day 2026-10-06, live inputs, local writes only: record `round21/real_run_2026-10-06.after_pl1.json`; screenshot
`round21/r21_realrun_modal_twd_365d.png`; the rendered day at `C:/tmp/rv-r21-realrun/layer/` on site Z.

| Measure | Value |
|---|---|
| Month strips | 393: 13 cells on 180 (first cell "Oct 25", last "Oct 26", all 180), and 2, 4, 7, 10 or 11 on the rest |
| BASG Kla Corp (the CVO's example of a strip with no October 2025 cell) | Oct 25 sold, Nov sold, then no trade through Oct 26; its list shows the three sales |
| Caption "Trades in the last 365 days" directly before the trades element | 695 of 695 chart frames (DOM) |
| Chart width | svg 972 px in a 972 px frame (CGIC 2454 TT) |
| "Price in TWD" label | overlaps no other text of the chart (bounding boxes read in the browser) |
| Page size | 1,688,519 B, 13.4 percent under the 1,950,000 cap (round 19: 15.9; round 14: 34.4) |
| Chart frames / chart-object keys | 695 / 695 (the round-19 run: 702 / 702) |

**The 7 frames fewer than round 19 are round 20's parsekey repair seen on real data:** the keys in the round-19 objects
and not in this run's are GQGU's CUSIP-keyed 037833100, 30303M102, 512807306, 532457108, 595112103, 718172109 and
91324P102; no key is new. They are folded into their Bloomberg keys now that buying_trend loads the parsekey (rows
Z-S57, Z-S61).

Correction to the round-18 packet: it said real_run.py's count of 695 frames was short of a DOM count of 702. real_run.py
counted correctly on every run; the two figures came from different runs (695 before round 18's inputs, 702 after).

## What ROUND_ANALYSIS.round20 rules that this cell does not carry (the next display cell)

- R3: the oldest cell is marked as a PART month (this cell labels it with its year and does not mark it).
- R2 item 2: a fund-security with markers and no prices draws no curve and reads the no-history sentence.
- R2 item 4: a range with fewer than two price points draws no curve for that range and says so.
- From the R3 read (`round21/READ_R3_S59_CAUSE.md`): markers through the page day; a zero-dollar trade is not a marker.
R2 items 1 and 3 (each section headed by its own window; the currency label) are in this cell.

## Judgment criterion owed at L9

RIV-pl-1 J1, on this run. md-1 J1 and pd-2 J1 stay owed on the served page.

## Rows

ETFS_RIVALS-Z-W11-S1 (OBSERVATION): ruled at the close. ETFS_RIVALS-Z-S62 (OBSERVATION): the vehicle runs the working
tree; this round touched render.py only, which the vehicle does not run.
