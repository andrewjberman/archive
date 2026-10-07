# ETFS_RIVALS round 19 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~12:2xZ)

One cell, RIV-ml-1, the repair of row ETFS_RIVALS-Z-S58. Issuance d309f31b5d; build a54f59756f; close 202c5314f0; merge
233b033a9f on site-Z CLOUD (LOCAL). Nothing of rounds 15 to 19 is deployed or served. This packet's run is the artifact
for every open J1 of rounds 15 to 19.

## Mechanical criterion

ml-1.AC1 PASS 0 failures, re-run by the issuer on the branch (it re-runs pd-2.AC1, pd-2.AC2 and md-1.AC2: all PASS);
proof instance VALID. Package suite on merged CLOUD 2aba59986e: 857 passed, 2 skipped, 0 failed.

## The real run, re-run and measured

Day 2026-10-06, live inputs, local writes only, code root CLOUD 2aba59986e: record
`round19/real_run_2026-10-06.after_ml1.json`; measurement `round19/month_strips_2026-10-06.json` (script
`round19/measure_month_strips.py`); screenshot `round19/r19_realrun_modal_month_strip.png`. The rendered day is at
`C:/tmp/rv-r19-realrun/layer/` on site Z.

| Measure | Value |
|---|---|
| Month strips on the page | 393 |
| Strips with a month label on every cell | 393 of 393 |
| Strips whose labels count back from the page month (last cell Oct) | 393 of 393 |
| Positional month rules left in the stylesheet | 0 |
| buying_trend rows with a mark; `window_end` of each | 1,403; all 2026-10-06 |
| Strips showing bought or sold in exactly the year-months the fund-security's markers end in | 382 of 393 |
| Page size | 1,640,613 B, 15.9 percent under the 1,950,000 cap (round 14: 34.4 percent; round 15: 19.2 percent) |

## Rows

| Row | Class | State |
|---|---|---|
| ETFS_RIVALS-Z-S58 | BLOCKING | Repaired by this round; disposition is the CVO's. |
| ETFS_RIVALS-Z-S59 | OBSERVATION | New: 11 of 393 strips disagree with the markers' months (unread); a 365-day window's oldest partial month is not on the 12-cell strip (BASG Kla Corp: 3 trades listed, 1 month shown). |
| ETFS_RIVALS-Z-S55, S56 | BLOCKING | Repaired in rounds 16 and 18; dispositions are the CVO's. |
| ETFS_RIVALS-Z-S57 | OBSERVATION | Served: buying_trend still splits 7 securities across two keys (morning pass). |
| Z-W1-S53, Z-W2-S16, Z-W4-S19 | OBSERVATION | Carried from round 15. |

## Judgment criteria owed at L9, all on this run

RIV-pd-2 J1, RIV-md-1 J1, RIV-co-1 J1 (round 15); RIV-pc-1 J1 (16); RIV-nc-1 J1 (17); RIV-tl-1 J1 (18); RIV-ml-1 J1 (19).

## Not exercised by any run so far

- The served gateway route (no release carries it). The page's script calls it; a page deployed before the route serves
  reads "Chart could not load" in every frame.
- Cell RIV-pd-3 on real data (the AI accounts on the three rolling periods): it needs a sweep's AI run on the new build.
- Cell RIV-bf-1 live (the Bloomberg range backfill): build only so far.

## What waits, and on whom

- 3.0.0_SA_CVO~RV: the seven J1 grades and the slug.
- 0.0.0_AB_MSTR~Z on Andrew's word: the push of site-Z CLOUD. The gateway release (ask carried by 1.0.0_SA_CTO~Z, msg
  30755) is cut from origin, so it waits on the push; the Lambda deploy waits on the release.
- 2.0.0_SA_COO~RV: the COO never-widen halves for the Lambda deploy and for the backfill run; the backfill's security list
  with formerly-held keys (CTO ruling 30817 term 1).
