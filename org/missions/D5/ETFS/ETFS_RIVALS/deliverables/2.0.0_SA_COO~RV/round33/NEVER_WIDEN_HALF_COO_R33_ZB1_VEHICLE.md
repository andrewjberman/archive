# NEVER-WIDEN -- COO half -- ETFS_RIVALS round 33: RIV-zb-1 reaches the site-Z vehicle (`2.0.0_SA_COO~RV`, 2026-10-17 ~07:2xZ)

**The act:** the site-Z working tree takes CLOUD at or after merge @91fd54467f, so the scheduled 11:00Z vehicle's rivalfunds
enrichment leg (`data/etfs/scripts/rivalfunds/enrichment_bloomberg.py`, daily mode) runs RIV-zb-1. Site-Z scheduled tasks run the
working tree (`integrations/bloomberg/READ_HERE.md` section 3), so the tree update IS the deploy. First run: 2026-10-19 11:00Z (the
next trading day), writing partition 2026-10-16. Authority: `1.0.0_SA_CTO~DELL1` msg 7376 (round 33, "each close under its own
venue's trading date"); Andrew-direct "completely filled ... now".

## Write set

One new object per run under `gold/security_market/date=<D>/market-<capture time>-<digest>.parquet` (D = the report date, NYSE T-1),
plus its `pull-enrichment` market marker -- the same keys the leg writes today. No other writer changes. The Lambda chain does not run
this module's market pull (the enrichment leg runs only on the Terminal machine), so no Lambda package moves.

## What it changes, read from the producer's rule (both branches)

- A security whose historical answer dated D carries PX_LAST: `px_close` and `total_return_index` are that answer, `price_date` = D,
  `as_of_source` "historical". Today the same row carries the reference PX_LAST taken at the capture time (Z-S85/Z-S87: right for US
  names captured before the US open, wrong for Asian names, not a close for European names, wrong for any name captured mid-session).
- A security with no historical PX_LAST dated D (its venue shut on D, or no answer): `px_close` and `total_return_index` NULL, where
  today it carries the snapshot value. The rankings then take the holding-implied path for that (security, D), as they already do for
  any unpriced day.
- Descriptive fields (GICS, CRNCY, name, parsekey): unchanged source (the reference request), now asked of every security.
- Measured on 2026-10-15's daily object: 579 rows, 0 historical today; under the rule the historical count is the securities answering
  for that date. Expected: every US name and most others; the null count is the venue-shut set.
- Points: one historical request of 2 fields per security in addition to today's reference request, about 2 x 580 = 1,160 more points
  a run, inside surface A.

## Readers that see it

The G4 readers of the package (census of `g4_window(`, `g4_rows(`, `"security_market"` over `data/etfs/scripts/rivalfunds/*.py`: 10
non-test modules): the rankings (`gold_holding_contribution`), `gold_trade_schedule`, `gold_buying_trend`, `gold_canonical_shape`,
`price_series`, `gold_input_census`, `history_owed`, `dramatic_move`, `publish_page`, and the enrichment module itself.

## Rollback per key

Revert the merge on CLOUD and let the site-Z tree take it before the next 11:00Z run; an object already written stays (a delete is
Andrew's act). Nothing here deletes.
