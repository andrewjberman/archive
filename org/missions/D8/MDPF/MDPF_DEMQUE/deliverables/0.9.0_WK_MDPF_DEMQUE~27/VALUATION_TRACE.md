# DQ-t-35 valuation trace (read-only), re-open 2026-10-11, worker 0.9.0_WK_MDPF_DEMQUE~27

Machine form: `VALUATION_TRACE.json` beside this file. Denominator: FTHSX 4, PFORX 11, total 15 (positions snapshot `silver/positions/date=2026-06-23`). RPIFX has 0 held positions.

## Production binding (step 1)

The production cottonwood gold run is SSM document `opal-cot-gold-run` (`infra/aws/terraform/cot-pipeline/ssm.tf`), which exports `BD_S3_BUCKET=opal-data-cot` and `FIRM_ID=cottonwood`. The firm bucket `opal-data-cottonwood` holds none of the four price and holdings keys read below (HeadObject 404; `gold/timeseries/holdings_lots/` has no objects). Production reads and writes are therefore in **opal-data-cot**.

The production chain does not run `B_01` (holdings_lots, B_01b, B_02, B_03); `ssm.tf` L294 says so, and `run_gold` (L375-404) lists no B_01. `gold/timeseries/holdings_lots/` is empty by design, and D_04 skips its account and position steps when it finds no object (`D_04` L1304-1307).

## The path, as read in production

1. **Price store**: `s3://opal-data-assets/yahoo/global/silver/price_history/cusip=<CUSIP>/prices.parquet` and `lock.json`. LOCKED, claim held, served-file controls read for all three CUSIPs.
2. **Lander target**: `opal-data-cot silver/historical_prices.parquet` (written by `land_cot.py`). HeadObject **404**.
3. **Ticker map**: `opal-data-cot config/ticker_lookup.json`. GetObject **404**. `build_canonical_prices_v2.py` L539-563 skips Tier 2 and uses `YF_OVERRIDES` only. No FTHSX, PFORX or RPIFX entry exists.
4. **Canonical table**: `opal-data-cot silver/prices/canonical_prices.parquet`, name-keyed, ticker blank for these names. For the five FTHSX/PFORX-family names the sources are only `linear_interpolation` and `transaction_observed` (no `yahoo_finance` row). The file's last date is 2026-06-09.
5. **Value artifact**: `opal-data-cot gold/canonical/holdings/2026-10-09.parquet` (B_00). FTHSX-family: 188 accounts, price 57.57-57.67, source `bd_snapshot`. PFORX-family: 334 accounts, price 9.45-9.46, `bd_snapshot`. B_00 L171-173 sets price = BD market value / units, so the page value does not come from the Yahoo or canonical close.
6. **Served household**: `platinum/clients/<rel>/composition.json` (top 9 holdings plus other). Detail: `detail.json`, NoSuchKey.
7. **Route and firm**: `/api/scoped/advisor-intelligence/platinum/clients/{hhId}/composition.json` and `detail.json` (`portal/src/api/endpoints/advisor-intelligence.ts` L489, L1156-1161). Firm: cottonwood. Source read, not the deployed edge.

## The bridge (step 2)

- Crosswalk: `commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.parquet` (1533 rows, 471 MATCHED). Every custodian number in the 15 rows is NOT_MATCHED or AWAITING_PERSON.
- Account links: `commonwealth/cottonwood/silver/account_links/date=2026-06-23/account_links.parquet` (1450 rows, 212 LINKED). None of the 15 numbers appears.
- **Result: no applied link for any of the 15 positions.** A seat does not apply a near match (FWD-9).

## Per position (step 3), summary

- **Read by a page: 0 of 15** (FTHSX 0 of 4, PFORX 0 of 11).
- Unapplied candidates (not used for any verdict):
  - 0QF883612 (FTHSX) to z0927234221: crosswalk AWAITING_PERSON 0.765; exact units on 2026-10-09.
  - B3S606732 (FTHSX) to z0927284761: exact units on 2026-10-09.
  - B3S734752 (FTHSX) to z0927344311: exact units on 2026-10-09.
  - RGY003642 (PFORX) to z0927303741: crosswalk AWAITING_PERSON 0.765.
- The four candidate households' composition.json names none of FTHSX, PFORX or RPIFX in its top 9. Their detail.json is NoSuchKey.

## Candidates (existing resolvers; C-IDENTITY)

- **FTHSX 14064D865**: no candidate. The stores carry FTHSX as the only ticker for this name family. Control: served-file agreement 40.7 (n 627).
- **PFORX 693390882**: PFBPX 42.9 (n 513), PFONX 42.5 (n 506), PFUIX 0.0 (n 513). None reaches 90, so no correction is proposed. The candidates came from a name-stem match, not a resolver output. Control: 42.9 (n 513).
- **RPIFX 77958B402**: no candidate. Control: 39.2 (n 651).

Pulls: 3 of 6 (scratch pacer), the same 3 as the first run. Nothing was written to any store, queue, page or pacer.

## Not read

Applied household or account for any of the 15 (none exists); the candidate households (composition read as unapplied candidates only); the 2026-06-23 production holdings beyond the exact-units test (no exact match on that date); the full price store history; the deployed portal edge; detail.json for any household (NoSuchKey); any Bloomberg source (none called).
