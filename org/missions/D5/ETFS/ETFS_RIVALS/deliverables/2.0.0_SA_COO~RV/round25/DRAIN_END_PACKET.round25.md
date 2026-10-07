# ETFS_RIVALS round 25 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~23:5xZ)

Two cells by CTO ruling msg 31428. **RIV-rg-1**: a date's rows of gold security_market are the union of all its objects,
by a stated rule -- the disarm of row ETFS_RIVALS-Z-S69 (BLOCKING, ARMED; corrected by Z-S70). **RIV-mr-1**: the chart's
read-out names the marker pointed at and the tooltip never covers it (CVO ADJUDICATION_v28). Issuance 1580bfb033. rg-1:
build 32f3f1943f, close 8e0486fe65, merge 1d2241ca66. mr-1: build 339ba875be, close 342b4653d0, merge 4c34f7f298. Site-Z
CLOUD, LOCAL. **Not deployed:** the live Lambdas are at f9f8334ef6 (rounds 15 to 24).

## Mechanical criteria

rg-1.AC1, AC2, AC3 and mr-1.AC1 PASS 0 failures, re-run by the issuer on each branch; both proof instances VALID; the
check files unchanged by the workers. Suite on the branches: 885 passed (rg-1) and 884 passed (mr-1), 2 skipped, 0 failed.
On merged CLOUD 1e25383b04: package suite 889 passed, 2 skipped, 0 failed; 34 of 34 check files under `round15/checks/` PASS 0 failures.

## RIV-rg-1 on the live table (read by the issuer through the new `g4_rows`, read-only)

| date | objects | before (the one object picked) | after (the union) |
|---|---|---|---|
| 2026-09-29 | 2 | the import: 172 rows, 0 closes, 164 sectors | 589 rows; **430 closes**, 429 day returns, 577 sectors; every close with its own currency (0 closes with a null currency); 434 rows from the live pull, 155 from the import (securities only the import holds: sector, no price) |
| 2026-10-01, 10-05, 10-06 | 1 each | 32 / 582 / 581 rows | identical in every column |
| **2026-10-02 (the control)** | 3 | 601 rows | **identical in every column** |

0 duplicate (security, date) on any date. So the ONLY date whose rows change is 2026-09-29, and every moved figure below
comes from it.

## The before and after of every fund's tables (CTO term 2)

`round25/before_after_tables.py`: the served tables of date=2026-10-07 against the tables the merged code builds from the
same inputs; record `round25/before_after_tables_2026-10-07.json`, every moved row named in it. Instrument control: against
unchanged code it reads 0 moved rows of 6,066 and of 1,406.

- **buying_trend: 0 of 1,406 rows move.**
- **holding_contribution: 3,259 of 6,066 rows move; 2,418 on the page's periods** (30d 747, 90d 761, 365d 910): 2,125
  security rows and 293 sector rows; all 13 funds (CGIC 671, INEQ 427, SCHY 356, TXUE 188, BIDD 184, BASG 122, GQGU 105,
  WCMG 100, PCLG 66, PFOE 56, ETFT 51, TSEL 48, IDVZ 44).
- Why they move: 2026-09-29 is inside every window, and a holding the live pull prices is now priced that day from
  Bloomberg's own day return (`g4_tri`) and not from the fund's valuation (`n_days_holding_implied` falls by one on 2,363
  rows). Ranks follow.
- Size, security rows of the page periods with a moved contribution (1,746): median 0.0085 percentage points; 204 above
  0.05; 36 above 0.10; largest 0.233 -- MediaTek in CGIC, 30 days, +0.062 to +0.295 (rank 5 to 2). The stored day return
  for it on 09-29 is +1.22 percent; the fund's valuation implied a very different day. NOT explained further by this
  seat.
- Top and bottom ten: 108 security rows enter or leave a ten (CGIC 22, INEQ 20, BIDD 16, TXUE 14, SCHY 10, GQGU 6,
  PCLG 6, BASG 4, ETFT 4, PFOE 2, TSEL 2, WCMG 2; IDVZ 0).
- Three securities gain a stored currency and so a price source (`holding_implied` to `mixed`): AJG US (BASG, TSEL),
  JAR LN (INEQ), ATD CN (TXUE).

**A limit of the design, stated because these figures move on it (not introduced by this cell):** each day takes ONE
source, and a market day sits between valuation-implied days. Where a fund's valuation lags the market by a day, the
implied day after a market day can carry the same move again, or miss one. Not measured. It already applies on the four
other market dates.

## The charts and the page

Real run from merged CLOUD (code equal to pin acf83a5716 over the packaged paths), record
`round25/real_run_2026-10-07.after_r25.json`: OK; index.html 1,694,876 B (served 1,693,555; 13.1 percent under the cap); 1
script; `fund_sections` 0 missing of 2,247; audit 1,255,783 B; 13 chart objects, 5,732,176 B (served 5,675,727); 5,896
markers (served 5,894).

Against the served chart objects: on 2026-09-29, **408 points become market closes** (101 were valuation-implied, 307
were empty). 696 points on other dates appear, all valuation-implied, for the securities that gained a stored currency
(a holding-implied price is drawn only for a listing stored as USD). 10 dialog keys appear and 10 go, following the
rankings (a holding gets a dialog when it is in a ten). 4 currencies change from none (AJG US twice, JAR LN to USD, ATD CN
to CAD).

## RIV-mr-1 in a browser (Chromium, 1400 x 1000, GQGU's Meta section, the local stand-in for the gateway routes)

7 of 7 markers: the read-out shows the marker's own day and the price of its point ("665.60 USD | 2026-09-14 | implied
from the holding" beside "Bought $10,592,358 on 2026-09-14"); 0 of 7 tooltips above the svg's top; 0 of 7 overlap the
read-out; after the pointer leaves, the read-out returns to its prompt and the tooltip hides. One marker at the plot's
right edge has its tooltip flush with the frame's border, 0.64 px over it (as round 24 built the clamp; not changed).
Screenshots `round25/r25_marker_readout.png`, `round25/r25_marker_right_edge.png`. ONE section in one browser.

## Worker rows

- Z-W15-S1 (OBSERVATION): bk-1.AC3 pins the trend's read to its own `_read`; honoured, no check edited.
- **Z-W15-S2 (OBSERVATION), an input to round 26:** by the rule as ruled, a security whose live row has no close and whose
  backfill row has one merges to a backfill-marked row; the rankings and the GICS join then drop its sector and parsekey
  with it. No partition mixes live and backfill today; FWD-24's top-ups would.

## Recorded, not graded (issuer ruling at the cut)

The input census still records the date's `revision.newest` object as a price's `location` (on 09-29 that names the
import though the close came from the live pull); the rankings and trend manifests now list every object read.

## Judgment criteria owed at L9

RIV-rg-1 J1 and RIV-mr-1 J1, on this run.

## What waits, and on whom

- The deploy: a never-widen pair with this before and after; ONE republish of 2026-10-07 with `refresh_a1` true (the
  tables' code changed). Asked of 1.0.0_SA_CTO~Z with the COO half.
- Upstream tables of earlier dates (G1's GICS join, G5's parsekeys) are NOT rebuilt by a republish; they read the union
  from the next daily run on.
