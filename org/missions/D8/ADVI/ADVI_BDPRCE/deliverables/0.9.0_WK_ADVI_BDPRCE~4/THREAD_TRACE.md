# BP-a-4 -- THE THREAD: one 49 Financial holding with no public ticker, its served price traced to rule and trades

Record: `THREAD_TRACE.json` (AC1 PASS). Trace output: `TRACE_2026-10-09.json` (from `trace_price.py`). Worker `0.9.0_WK_ADVI_BDPRCE~4`, read 2026-10-13T14:50:10Z. Claim: measured. Read verbs only; no object written, no producer run, no product file edited. No client name, advisor name or raw account id is written here; the account is the hash reference `3c0cf325f23f`.

## The served object

`opal-data-49financial` key `advi/49financial/platinum/entities/clients/0/detail.json`, VersionId `VzILgp.KR2G8UFNcDbZLo3GcSkNmFnPC`, ETag `a6206d366191b111dee1f384f90d4ba1`, LastModified 2026-10-13T05:39:43Z. Its `data_as_of` field is 2026-10-09 (the served as-of date used here). The lot list sits at `tax.open_lots`, one row per lot, with `account_id`, `asset_name`, `ticker`, `current_price`, `quantity`, `market_value`.

Producer chain: `data/black_diamond/scripts/gold/B_01.holdings_lots.py` prices each lot (`current_price`, :1333 and :2627); `D_02.advisor_client_detail.py` writes `open_lots` into the client response (:2578) and keys it by `client_detail_key` (:2971; `gold/entities/clients/{id}/detail.json` per `lib/s3_layout.py:239-240`); `lib/platinum_dest_view.py` maps that legacy key to `advi/49financial/platinum/entities/clients/{id}/detail.json` in `opal-data-49financial`. The portal reads the same key (`portal/src/api/endpoints/advisor-intelligence.ts:1156-1160`).

## The holding

- Account ref `3c0cf325f23f` (first 12 hex of sha256 of the account id), lot 1.
- Asset `VANGUARD MORNINGSTAR GROWTH ETF`, `ticker` null in the served object. The name is also absent from `config/ticker_lookup.json` of `opal-data-bd` (10,206 entries, text search).
- Quantity 20.5278, served `current_price` 91.9833, `market_value` 1888.2155, acquired 2026-07-02.

## The served price and its rule

- Served price: 91.983333 (the lot shows 91.9833, 4 dp). Source `transaction_observed` at 2026-10-09 in `silver/prices/canonical_prices.parquet`, version `V7JNX.GmPYQcEVMywtMRnjk.fSdQl1WA`.
- Rule, in plain words: the price is the median of the per-unit value (|market_value| / |units|) of the asset's trades on 2026-10-09, after the filters at `data/black_diamond/scripts/silver/bd_price_update.py:335-341` (median at :344; applied at `build_target_date_rows:463-464`).
- Trades: 123 rows, 23 distinct `transaction_id` values. The full list (repeats kept, as the rule keeps them) is in `THREAD_TRACE.json` `trade_ids`.
- Recompute: median over all 123 rows = 91.983333, equal to the served price (`recompute_equals_served` true).
- Gap class: EQUAL, `GAP_ROWS.csv` row 2026-10-09 / VANGUARD MORNINGSTAR GROWTH ETF (evidence `current:tnLerK0Z`).

## The tie on the same date

`silver/prices/2026-10-09.parquet` (version `LhM3NuODjCiM_VUkEQiojppZtVu4Jf7y`) also carries this asset on 2026-10-09 with `transaction_observed` at 92.216667. The served lot follows the canonical row (91.983333), not the daily row. The daily value is not reproduced by the same trades. The trace tool's stable pick takes the daily row, so its `match` flag reads false for this holding. Filed as a surprise row (`ADVI_BDPRCE-D1-W4-S3`).

## The writer

Canonical version `V7JNX` (2026-10-13T12:48:05Z) was written by the S_00 run `b09cfe1b7fe6`: `build_canonical_prices_v2.py` puts the table, and `inject_scoped_overrides.py` is auto-chained and puts it again. Rule copy: `build_canonical_prices_v2.py resolve_prices_for_asset:394-458`. The writer identity is inferred (WRITERS.json row 2 and 3; claim inferred, not measured per principal).

## Why this holding (shape and counts)

- Shape a (direct) applies at the served date, so the chain shape was not needed.
- Population read: 26 of 3,510 client `detail.json` objects (every 140th key in the served home listing). These 26 hold 586 untickered, non-cash lots over 138 assets.
- Direct candidates (lot price equals the canonical row on the as-of date, source `transaction_observed`, class EQUAL): 64 lots.
- Chain candidates (lot price equals a carry-forward or linear row on the as-of date, anchor EQUAL and equal in price): 63 lots.
- Other lots: 61 lots whose price matches no canonical row on the as-of date, and 8 assets absent from canonical. Surprise row `ADVI_BDPRCE-D1-W4-S2`.
- First candidate in file order: client object 0, lot 1 of account ref `3c0cf325f23f`.
- Not a full census: the served home holds 3,510 detail objects of about 4 MB each. Surprise row `ADVI_BDPRCE-D1-W4-S4`.

## Reproduce

1. `aws s3api get-object --bucket opal-data-49financial --key advi/49financial/platinum/entities/clients/0/detail.json --version-id VzILgp.KR2G8UFNcDbZLo3GcSkNmFnPC <file>`, then select the lot with `hashlib.sha256(str(account_id)).hexdigest()[:12] == "3c0cf325f23f"` and `asset_name == "VANGUARD MORNINGSTAR GROWTH ETF"`.
2. `python org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~2/trace_price.py --asset "VANGUARD MORNINGSTAR GROWTH ETF" --date 2026-10-09 --out <file>`.
3. `python org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/2.0.0_SA_COO~K1/round1/checks/r1_checks.py thread --file org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~4/THREAD_TRACE.json`.

## Premise notes

- The served object's `data_as_of` is 2026-10-09 in 24 of the 26 sampled objects (two older). T-1 for 2026-10-13 is 2026-10-12, so the served home is one trading day behind T-1 for these objects. Surprise row `ADVI_BDPRCE-D1-W4-S1`.
- The chain shape the task order expected at the served date does not occur here, because 2026-10-09 has transaction-observed rows in both files.
