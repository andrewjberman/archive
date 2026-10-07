# ETFS_RIVALS round 18 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~11:5xZ)

One cell, RIV-tl-1, the repair of row ETFS_RIVALS-Z-S56. Issuance 8813da6c04; build ceb48060d0; close 1898957608; merge
4c10ccc170 on site-Z CLOUD (LOCAL). Nothing of rounds 15 to 18 is deployed or served.

## Mechanical criterion

tl-1.AC1 PASS 0 failures, re-run by the issuer on the branch (it re-runs nc-1.AC1, md-1.AC1 and md-1.AC2: all PASS);
proof instance VALID. Package suite on merged CLOUD 5be2c73b12: 854 passed, 2 skipped, 0 failed. The granted edit to
md-1.AC1.py went unused: that file never pinned the old sentence (the cut was wrong about it).

## The real run, re-run and looked at

Day 2026-10-06, live inputs, local writes only, code root CLOUD 5be2c73b12: record
`round18/real_run_2026-10-06.after_tl1.json`. In a browser (localhost stand-in for the gateway's routes) every dialog
was opened and every chart frame read against its fund's chart object:

| Measure | Value |
|---|---|
| Chart frames in the page (DOM count) | 702 |
| Static trade elements saying "No trades in the last 365 days" before the script runs | 0 (was 618) |
| Static elements carrying "The fund's trades over the last 365 days load with the chart." | 618 |
| After the object loads: frames whose list agrees with the object's markers | **702 of 702** |
| -- object holds 0 markers, list says "No trades in the last 365 days" | 77 |
| -- object holds markers, list holds one line each (20 newest plus the "and N earlier" line) | 625 (70 of them capped) |
| Frames still showing the static sentence after load | 0 |

The DOM holds 702 chart frames; `real_run.py`'s own pattern reports 695 (why it misses 7 is unread). Row S56's parse
was therefore right at 702, and its caveat was the wrong way round.
Screenshot `round18/r18_realrun_modal_trade_list.png` (BASG, Kla Corp: three sales listed, agreeing with "3 trades").

## Found on this run: row ETFS_RIVALS-Z-S58 (BLOCKING, INERT)

The month-by-month buying strip labels its cells January to December by position, but since round 15 the trend's months
start at the window's first month. On the screenshot the three sales of October and November 2025 sit under "Jan" and
"Feb". The page holds 393 strips (12 cells on 180, and 2, 4, 7, 10 or 11 on the rest); 248 of 349 R365 trend rows carry
13 month tokens, of which the strip draws the first 12 and drops the newest. The served page (round 14) is correct
today; the defect ships with the round-15 deploy. A round-19 repair cell follows.

## Judgment criteria owed at L9

RIV-tl-1 J1, RIV-nc-1 J1, RIV-pc-1 J1, RIV-pd-2 J1, RIV-md-1 J1, RIV-co-1 J1 -- on this run's artifacts; RIV-pd-2 J1 is
best graded after the round-19 repair.
