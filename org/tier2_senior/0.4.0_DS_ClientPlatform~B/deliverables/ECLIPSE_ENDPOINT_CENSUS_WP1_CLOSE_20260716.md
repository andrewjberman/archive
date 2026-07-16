# Eclipse endpoint-structure census -- WP1 close instrument (exercised, value-discriminated)

**Author:** 0.4.0_DS_ClientPlatform~B
**Date:** 2026-07-16 ~16:1xZ
**Trigger chain:** Andrew-direct (my terminal ~15:0xZ: "We already established that there is
backfill for eclipse, and that we cannot conflate the shape of our tool with the shape of the
data eclipse offers and endpoint structure... your task is investigating the endpoint structure
for Eclipse") -> CTO formal REOPEN + census standard (152353Z: exercised, value-discriminated,
standing grants, zero speculative load).
**Probe artifacts:** eclipse_audit_census_probes_20260716.json (this dir; T1/SMOKE bodies
stripped to counts, raw 15.9MB retained in session scratchpad).

## VERDICT (one paragraph)

The 07-13..15 hole interior IS vendor-recoverable -- as EVENT HISTORY, not snapshot time-travel.
Eclipse publishes a full API catalog (its existence itself falsifies the "no vendor catalog"
premise for Eclipse): 493 paths / 56 groups, including a 21-endpoint Audit_and_Logging group
with date-ranged portfolio/model audit histories, plus date-ranged closed-trade history carrying
point-in-time portfolio values. Exercised probes: the range params are HONORED (positive
controls matched vendor-stamped discriminator dates to the second), negatives returned clean
zero. There is NO as-of parameter on the snapshot endpoints (/portfolio/portfolios*), so the
4-file daily-partition shape CANNOT be re-fetched for a past date -- the honest-holes rejection
of labeled-copies STANDS; what changes is that REAL VENDOR BYTES for the hole exist in the
vendor's own history shape (auditlog + closedTrades window pulls).

## 1. The conflation, measured

| Surface | Paths | Source |
|---|---:|---|
| Our productionized tool (pull_eclipse_portfolios.py) | 5 | data/inf/API/domains/eclipse/endpoints/README.md |
| Eclipse's published API V1 | **493** (56 groups) | https://api.orioneclipse.com/doc/ (OpenAPI 3.0.3, spec embedded in /doc/swagger-ui-init.js, 2.57MB) |

Our coverage of the vendor surface: 5/493 = 1.0%. The D3 "no vendor catalog" premise
(DATA_PLATFORM_D3:27) cited ADVI_ORIAPI section 1 -- a statement about ORION CONNECT -- and was
carried onto Eclipse, where a public catalog exists. Same conflation class, one layer deeper.
The prior local records (D3 arch spec, DC2 briefs, 05-14 feasibility brief) enumerate only
HAR-observed/probed endpoints; the .runtmp HARs of record were never archived (verified gone).

## 2. Vendor surface relevant to the hole (from the published spec)

- `GET /v1/auditlog/portfolio/{portfolioId}?fromDate&toDate` -- field-level change rows
  (changeType Insert/Updated/Deleted, editedOn/editedBy, name/model/tags/isDisabled/doNotTrade/...).
- `GET /v1/auditlog/model/{modelId}` + `/v1/auditlog/modelDetail/{modelId}` -- model-layer history.
- `GET /v1/tradeorder/closedTrades?startDate&endDate` -- full trade ledger rows incl. the
  portfolio's totalValue/managedValue/excludedValue AT TRADE TIME (in-hole valuations, vendor-native).
- `GET /v1/tradeorder/instances/portfolio/{portfolioId}/search?startDate&endDate` +
  `/tradeLogs/{portfolioId}/instances` -- rebalance-instance history per portfolio.
- `GET /v1/report/allocations?startDate&endDate` (unprobed; Reports group).
- NOT offered: any as-of/date parameter on `/v1/portfolio/portfolios` or `/simple` (snapshot
  endpoints are current-state only -- the one true part of the original premise).

## 3. Exercised probes (6 calls ~16:0xZ, standing Eclipse JWT via SM orion/eclipse_jwt/current, all HTTP 200)

Discriminators held IN HAND before probing, from bronze/eclipse/2026-07-16/portfolios_simple.json:
the hole's changed set = 18 edited + 3 created = 21 portfolios (matches the 074e2530b manifest
count exactly; IDs 2, 86, 165, 192, 328, 341, 426, 440, 468, 484, 485, 1077, 1340, 1374, 1381,
1419, 1420, 1421).

| Probe | Call | Result | Discrimination |
|---|---|---|---|
| SMOKE | modeling/models | 200, 18 rows | session live; no re-exchange needed |
| P1 (+) | auditlog/portfolio/2?fromDate=2026-07-10&toDate=2026-07-16 | 200, 1 row: Updated, editedOn **2026-07-13T18:10:24Z**, editedBy J.Brandenburg | held discriminator 18:10:27Z -- same edit action, 3s intra-action delta (snapshot carries last write; audit row logs the action). In-window, vendor-stamped, range honored |
| P2 (+) | auditlog/portfolio/1419 (same window) | 200, 2 rows: **Insert 2026-07-15T16:29:24Z** + **Updated 16:36:17Z** | BYTE-MATCH to held createdOn 16:29:24Z and editedOn 16:36:17Z. An honored range param cannot hide against this |
| N1 (-) | auditlog/portfolio/88 (in 835-roster, untouched since 2025-08-13) | 200, **0 rows** | separate invocation (22a); no phantom rows |
| M1 (-) | auditlog/model/3 (same window) | 200, **0 rows** | "models static across the hole" upgraded to EXERCISED-vendor-surface grade |
| T1 | tradeorder/closedTrades?startDate=2026-07-13&endDate=2026-07-15 | 200, **2,937 rows** | full trade detail; first row ties portfolio 468 (one of the 21) to Manual Rebalance 2026-07-13T14:24:05Z w/ portfolio totalValue at trade time -- cross-confirms the portfolio-edit trail with trading activity |

Positive controls run in isolation from negatives; each probe a separate invocation (Rule 22a).
Coverage denominator: 6/6 probes returned 200; 2/2 positives matched held vendor stamps;
2/2 negatives clean-zero; probed groups = Audit_and_Logging + Closed_Trades + Models
(Reports/Trade_Instances mapped, unprobed -- no speculative load beyond the census need).

## 4. What this means for the disposition (CTO's call; my recommendation)

The CTO close-fork (152353Z) was: history exists -> true-vintage backfill, manifest amends,
WP1 FILLED; else citation upgrade, holes stand. The exercised answer is BETWEEN the forks:

- History EXISTS and is real-vendor-bytes pullable (audit rows + trade ledger + instance logs).
- Snapshot-shape backfill does NOT exist (no as-of on /portfolio/portfolios) -- so no
  2026-07-1{3,4,5}/ partitions of the standard 4-file shape can honestly exist; the labeled-copy
  rejection stands; the twin's >=-token predicate fix (0.7.0 -> CTO) is right regardless.

**RECOMMENDATION: FILLED-VIA-HISTORY-ARTIFACTS.** One-shot window pull, landed as the vendor's
own shapes under NEW bronze artifact types (e.g. bronze/eclipse/_history/{auditlog_portfolio,
auditlog_model,closed_trades,trade_instances}/2026-07-13_2026-07-15.json): ~45 calls
(21 portfolio auditlogs + 18 model auditlogs + closedTrades + instance logs for the 21),
same magnitude as 4 daily pulls. That closes the manifest's genuinely-unknown residual (the 21
portfolios' intermediate paths) with EXERCISED artifacts, keeps every honest-holes principle
intact, and leaves the daily 4-file cadence untouched. Market-value decorations for unchanged
portfolios stay orion-derivable (WP5 class) per the manifest. Manifest amendment rides
0.7.0's authorship on this evidence; my silver leg stays today-forward.

## 5. Corrections this census lands on the record

1. "Eclipse vendor API is current-state-only, no time-travel" (074e2530b holes[].reason,
   pre-AMEND) -- FALSE as written: current-state-only is true of the SNAPSHOT endpoints, false
   of the surface (Audit_and_Logging + dated trade history). The AMENDED block's own residual
   pointed here.
2. "Orion and Eclipse publish no developer API catalog" (D3:27) -- FALSE for Eclipse:
   https://api.orioneclipse.com/doc/ is public, OpenAPI 3.0.3, 493 paths. D3/domain docs need a
   catalog-pointer amendment (routed with these findings).
3. The 05-14 feasibility HARs (.runtmp/*.har) were never archived -- the endpoint-structure
   record dies with scratch dirs. The published catalog now supersedes HAR archaeology for READ
   surface; the write surface remains HAR-only territory (D5 frontier, unchanged).
