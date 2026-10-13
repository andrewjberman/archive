# CB-cc-1 consumer read -- minted table (ADVI_COTBKF, round 81) -- 0.9.0_WK_ADVI_COTBKF~158

Record: `CONSUMER_READ.json` (same folder). Read-only; nothing built, served, written or corrected.

**Served objects.** Each of the three minted prefixes holds one object (`part-00000.parquet`, LastModified 2026-10-09T12:41Z). Listing limit 5; no NextToken, so each count is complete.

**Graph (comp-platinum reverse, --firm cot).** No portal-page reader of the minted prefixes. The named control (`s3://opal-data-cot/silver/prices/canonical_prices.parquet`) returned no consumer, so the record uses `platinum/firm/client_directory.json`, which returns CottonwoodClientsSection and ClientsTab. The minted keys have no producer edge: the builder addresses them through `lib/opal_naming`, so literal-key queries cannot see it.

**Code, direct consumers (2).**
- `data/assets/scripts/silver/commonwealth_account_return_daily.py` lines 221-226, 479, 482, 486: reads all three minted tables. No route.
- `data/assets/scripts/silver/commonwealth_price_basis_census.py` lines 292-295: reads `account_day_value`. Census script, no route.

Writers, not consumers: `commonwealth_fwd3_serve.py` (--apply, not run); the ARD guarded mint writes gold `account_return_daily`, not the minted tables.

**Second hop (not established).** ARD output feeds gold `account_return_daily`, then `reporting-publish` (platinum/reporting series), then the portal InvestorReporting dashboard. The read route is recorded as planned, not applied (`infra/aws/lambda/ci/lambda-source-map.json:6485`).

**Build after 2026-06-05.** The minted tables end at 2026-06-22. Minted rows dated 2026-06-08 to 2026-06-22 are in the served copy (measured by counts and store labels). The one-day steps dated 2026-09-04 and 2026-10-02 are after every minted date, so they feed no minted table: HELD for those steps. The value-level link is inferred from builder inputs.

**disarm_fact_a = consumers_found.** Per CTO ruling 1, W155-S1 stays ARMED. Surprise rows: ADVI_COTBKF-D2-W158-S1 to S5.
