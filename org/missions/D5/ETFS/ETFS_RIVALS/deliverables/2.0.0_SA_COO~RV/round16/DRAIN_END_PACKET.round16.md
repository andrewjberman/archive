# ETFS_RIVALS round 16 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~10:5xZ)

One cell, RIV-pc-1, the repair of round 15's row ETFS_RIVALS-Z-S55 under the ruling of 1.0.0_SA_CTO~Z msg 30787.
Issuance 49a74229dd; build e9965690ad; close 23cdd6450c; merge efea405c1e on site-Z CLOUD (LOCAL). Nothing of rounds 15
or 16 is deployed or served.

## Mechanical criteria

pc-1.AC1 and pc-1.AC2 PASS 0 failures, re-run by the issuer on the branch; proof instance VALID. AC2 re-runs ps-1.AC1,
co-1.AC1, co-1.AC2, md-1.AC1 and md-1.AC2: all PASS. Package suite on merged CLOUD: 849 passed, 2 skipped, 0 failed.
The one granted edit to an earlier check (co-1.AC1.py: `SEC_KEYS` gains "currency"; the fixture plants G4 rows with
currency USD and no close) was diffed by the issuer: no assertion, expected value or message changed.

## The CTO's term 4: the same real run, re-measured

Day 2026-10-06, live inputs, local writes only, code root CLOUD 0f7e460190. Record
`round16/real_run_2026-10-06.after_pc1.json`; measurement `round16/currency_measure_2026-10-06.json` (script
`round16/measure_currency.py`, before = the round-15 run's 13 chart objects, after = this run's).

| Measure | Before (round 15) | After (round 16) |
|---|---|---|
| Fund-securities | 695 | 695 (same keys) |
| Boundary jump above 3x or below 1/3 | 152 | **0** |
| Boundary jump above 5 percent | 353 | 18 (all among USD listings; not examined one by one) |
| Securities carrying a holding-implied point, by stored currency | every currency | USD 263, every other currency 0 |
| USD securities whose points are identical before and after | -- | **263 of 263** |
| US-listed keys stored as USD, points identical | -- | **238 of 238** |
| Euro listings (stored EUR) | 129 of 129 measured had a boundary ratio off by more than 5 percent (min 0.843, median 0.882, max 0.950) | 130 securities, 0 with an implied point |
| Securities with market closes only | 0 | 335 |
| Securities with NO price at all | 0 | **97** |
| Priced points over all objects | 137,292 of 174,445 | **49,639 of 174,445** |

Page: 13 of 13 funds; index.html 1,575,159 B (19.2 percent under the cap); 1 script; 695 chart frames; chart objects
244,929 to 1,147,361 B. In a browser (localhost stand-in): a dollar dialog reads "Price in USD"; a Taiwan listing reads
"Price in TWD", draws its 2 closes, shades the gap with the non-dollar reason, and keeps its 126 trade markers by date
(`round16/r16_realrun_modal_non_usd_365d.png`).

## What the ruling costs today, measured (for 1.0.0_SA_CTO~Z and the J1 grade)

- 97 fund-securities now draw no curve: 96 have no stored currency (no G4 row in the 365-day window) and are treated as
  non-dollar by term 1. 43 of them are US-listed keys (examples: ETFT AAPL, PCLG ADBE, IDVZ BABA, GQGU INTU): positions
  that left the funds before the market table began, so Bloomberg was never asked about them.
- 335 non-dollar securities draw only the 2 to 3 market closes on file. Their year fills only when the Bloomberg range
  backfill (cell RIV-bf-1, Andrew-authorized, not yet run) lands closes for the year.
- So the curve is correct now and mostly empty until the backfill runs: 28 percent of points carry a price, against 79
  percent before the repair.

## Judgment criteria owed at L9

RIV-pc-1 J1, with round 15's RIV-pd-2 J1, RIV-md-1 J1 and RIV-co-1 J1, all on the round-16 run's artifacts.
Seen and not rowed: the "Price in <currency>" label sits on top of the axis's top figure; with markers but no price in
a range the markers ride the top edge.

## Rows

- ETFS_RIVALS-Z-S55 (BLOCKING): repaired by this round; its disposition is the CVO's.
- ETFS_RIVALS-Z-W6-S3 (OBSERVATION): ruled, accepted as built (a key no fund reported keeps the plain gap reason).

## What waits, and on whom

- 3.0.0_SA_CVO~RV: the grades above and the slug.
- 1.0.0_SA_CTO~Z: whether the 96 no-currency securities are acceptable as "no curve", and the never-widen halves for the
  Lambda deploy and the backfill run. The gateway release ask is with the CTO (msg 30755).
- 0.0.0_AB_MSTR~Z on Andrew's word: the push of site-Z CLOUD.
