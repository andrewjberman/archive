# ETFS_RIVALS round 15 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~10:2xZ)

Issuance d06e19f939 (9 cells, 5 chains; PRD v0.18 @6e245cbebe FWD-22, FWD-23). All 9 orders are `complete` and merged on
site-Z CLOUD. Nothing of round 15 is deployed or served. Push state: LOCAL (origin CLOUD ec35c9d706 by ls-remote 09:33Z).

## Orders and merges

| Chain | Orders | Close on branch | Merge on CLOUD |
|---|---|---|---|
| ~1 | pd-1, pd-2, md-1 | 7c89d4dcb5 | 116eadfa37 |
| ~2 | ps-1, tm-1, co-1 | 09c726541e | ca77f9dda6 |
| ~3 | bf-1 | 48662fa02c | 8b9455602b |
| ~4 | rt-1 | 62047cb24e | f7f2cb7c2e |
| ~5 | pd-3 | bbed91b11d | 6bf5bb0251 |

Integration fix after the last merge: 370ae7a279 (row Z-W1-S52; the suite read 3 failed, 839 passed before it).

## Mechanical criteria (the checker's match is the verdict)

14 of 14 checks under `round15/checks/` PASS 0 failures on merged CLOUD (run 09:54Z at 80bcd69f78; md-1.AC1, md-1.AC2,
pd-2.AC1 and pd-2.AC2 re-run PASS after 370ae7a279). 9 of 9 proof instances VALID on their branches.
Package suite on CLOUD 370ae7a279: 843 passed, 2 skipped, 0 failed. Gateway `app/tests/test_rivalfunds_view.py` +
`tests/test_principal_cutover.py`: 28 passed.

## Judgment criteria owed at L9 (never self-graded)

- RIV-pd-2 J1, RIV-md-1 J1, RIV-co-1 J1 -- graded on the real run below, and again on the served page after a deploy.

## The one real run (the artifact to grade)

`round15/real_run_2026-10-06.json`, `round15/r15_realrun_modal_30d.png`, `round15/r15_realrun_modal_365d_markers.png`,
script `round15/real_run.py` (@a26fc880e9). Day 2026-10-06 from live inputs, local writes only; the rendered day is at
`C:/tmp/rv-r15-realrun/layer/` on site Z (page, audit, manifest, 13 chart objects).

- Tables: holding_contribution 13 funds / 6,067 rows; buying_trend 13 funds / 1,353 rows; R30 window for IDVZ is
  2026-09-05 to 2026-10-05 (was 2026-08-24 under 30 trading days).
- Page: 13 of 13 funds; index.html 1,575,038 B, 19.2 percent under the 1,950,000 cap (round 14: 34.4 percent); 1 script
  block; 695 chart frames; switch 30d / 90d / 365d, opens on 30d. Audit page: 0 scripts.
- Chart objects: 13, 250,420 to 1,437,554 B (cap 1,900,000), none thinned.
- In a browser (localhost stand-in for the gateway's routes): a dialog fetches its chart object and draws; the range
  buttons redraw; markers and hover work.
- NOT exercised: the served gateway route (no release carries it); cell pd-3 on real data (it needs a sweep's AI run; the
  page's AI accounts still name MTD / QTD / YTD, 10 mentions, all inside the earlier sweep's prose); the Bloomberg range
  backfill live (bf-1 is build only).

## Rows

| Row | Class | State |
|---|---|---|
| ETFS_RIVALS-Z-S55 | BLOCKING, INERT | OPEN. A non-US security's curve joins listing-currency closes to dollar implied prices: 152 of 598 fund-securities jump more than 3x (JP 43/43, LN 54/54, HK 11/11, KS 9/9; US 0/238). The Lambda deploy waits on it. Shape of the repair is at 1.0.0_SA_CTO~Z. |
| ETFS_RIVALS-Z-W1-S51 | OBSERVATION | Ruled into cell co-1 and built (64ca82a511). |
| ETFS_RIVALS-Z-W1-S52 | OBSERVATION | Ruled and built (370ae7a279): a static trade line with no basis points says nothing about them. |
| ETFS_RIVALS-Z-W1-S53 | OBSERVATION | Carried: the audit page keeps "History not yet backfilled"; it carries no script by Andrew's word. |
| ETFS_RIVALS-Z-W2-S16 | OBSERVATION | Carried: chart objects are written only when the page's bytes change. |
| ETFS_RIVALS-Z-W4-S19 | OBSERVATION | Carried: 29 gateway-suite failures at base, none in rivalfunds; owner NFRA_OPLGTW. |

Lesser, seen on the real run, not rowed separately (noted in S55): the chart's y axis pads below zero; the drawing uses
about two thirds of the frame width; page headroom fell from 34.4 to 19.2 percent.

## What waits, and on whom

- Deploy order when S55 is closed: gateway release (NFRA_OPLGTW, ask carried by 1.0.0_SA_CTO~Z, msg 30755; route shape
  `round15/GATEWAY_CHART_ROUTE_AS_BUILT.md`), then the rivalfunds Lambdas under a NEVER-2 ledger entry and a never-widen
  pair, then the Bloomberg backfill dry run and run after a day's 11:00Z vehicle run under its own pair.
- The push of site-Z CLOUD: Andrew's word at 0.0.0_AB_MSTR~Z.
