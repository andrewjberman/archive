# BP-a-4 -- THE THREAD: one EXXONMOBIL HOLDINGS CORP COM SHS lot in a normal 49 Financial client object, its served price traced to rule and trades

Record: `THREAD_TRACE.json` (AC1 PASS: `THREAD record ok rule=... trades=4 equal=true`). Worker `0.9.0_WK_ADVI_BDPRCE~4`, amendment 2 re-seat, read 2026-10-13T15:07Z. Claim: measured. Read verbs only; no object written, no producer run, no product file edited. No client name, advisor name or raw account id is written here; the account is the hash reference `420deb1a5526` (first 12 hex of sha256 of the account id).

## The served object (client_key class: normal)

- `opal-data-49financial`, key `advi/49financial/platinum/entities/clients/z08334146/detail.json`, VersionId `ZCjWpzPR1n2uZl849onevhS.pIvSQhVA`, `data_as_of` 2026-10-09.
- Entity key class `z0...`, not `0`. The object holds 110 open lots.
- The portal reads the same key pattern (`portal/src/api/endpoints/advisor-intelligence.ts:1156-1160`). The producer chain (`B_01.holdings_lots.py` prices each lot, `D_02.advisor_client_detail.py` writes `open_lots`, `lib/platinum_dest_view.py` maps the key) was read by the earlier worker for the first candidate and is not re-read here.

## The holding

- Asset `EXXONMOBIL HOLDINGS CORP COM SHS`, served `ticker` null, no entry in `config/ticker_lookup.json` (exact name). Rule used: the task order's no-public-ticker rule (null ticker OR no lookup entry). The record does not claim the security has no listing (surprise row `ADVI_BDPRCE-D1-W4-S9`).
- Lots 2 and 3 of account ref `420deb1a5526`, quantity 73 each, `current_price` 168.94 on both.
- Condition d (one served price): every open lot of the asset in this object carries 168.94. Pass.

## The served price and its rule

- Served price **168.94**, source `transaction_observed`, date 2026-10-09, in `silver/prices/canonical_prices.parquet` (VersionId `V7JNX.GmPYQcEVMywtMRnjk.fSdQl1WA`). Shape a (direct).
- Rule, in plain words: the price is the median of the per-unit value (|market_value| / |units|) of the asset's trades on 2026-10-09 in `silver/transactions/2026-10-09.parquet`, after the filters at `data/black_diamond/scripts/silver/bd_price_update.py:335-341` (median at :344; applied at `build_target_date_rows:463-464`).
- Trades: 4 rows, **one distinct transaction id** (`745369343`, repeated four times; the rule keeps repeats; surprise row `ADVI_BDPRCE-D1-W4-S7`). Trade ids are listed in `THREAD_TRACE.json`.
- Recompute: median of the four rows = 168.94, equal to the served price (`recompute_equals_served` true).
- Gap class: EQUAL (`GAP_ROWS.csv` line 1608, evidence `current:tnLerK0Z`).

## The tie on the same date (read this before using the daily file)

`silver/prices/2026-10-09.parquet` (VersionId `LhM3NuODjCiM_VUkEQiojppZtVu4Jf7y`) also carries this asset on 2026-10-09, with source `carry_forward` at 162.155. The served lot follows the canonical row (168.94). The daily value is not a trade median. The instrument's default run (`trace_price.py`) takes the daily row as its stable pick, so it reports `carry_forward` with zero trades and names the wrong carry input (surprise rows `ADVI_BDPRCE-D1-W4-S5` and `ADVI_BDPRCE-D1-W4-S6`). The canonical row is traced with `trace_canonical_only.py`, which calls the instrument's own `trace_asset_date` with only the canonical object.

## The writer

Canonical version `V7JNX` (2026-10-13T12:48:05Z) was written by the S_00 run `b09cfe1b7fe6`: `build_canonical_prices_v2.py` puts the table (rule copy `resolve_prices_for_asset:394-458`), then `inject_scoped_overrides.py` is auto-chained and puts it again (`WRITERS.json` rows 2 and 3). The writer is named for the serving version; the per-row history of the 2026-10-09 Exxon row across versions was not traced. Claim inferred.

## Why this holding (counts, and the first fitting row)

- Population: 120 normal client detail objects, a stride sample of 3,509 normal `detail.json` keys (the `acct_z` and `z0` classes). Objects tried: 120. Objects with an untickered holding: 33 (all dated 2026-10-09). Untickered (object, asset) pairs: 91. Pairs failing condition d (one served price): 0.
- Shape a (direct) candidates: 12 pairs, all with `transaction_observed` at the as-of date and class EQUAL. Shape a exists, so shape b was not needed for selection.
- Shape b (chain) candidates: 22 pairs, linear_interpolation at the as-of date with an EQUAL anchor at equal price. Carry-forward rows: none in the sample. Shape b failures: 33 pairs (25 with no anchor, 5 EXPLAINED_OTHER, 2 UNEXPLAINED, 1 EXPLAINED_BY_MULTIDAY_WINDOW). Mismatch of lot price against the canonical row on the as-of date: 22 pairs.
- First fitting candidate in sample order: sample position 58, this object, this asset.
- The sample is not a census of 3,509 objects. The one-price result (0 failing) is for this sample only. The one-price failure the issuer measured sits in the catch-all entity, which is excluded.

## Rejected first candidate (kept for the record; not the thread)

- Object `entities/clients/0/detail.json` (VersionId `VzILgp.KR2G8UFNcDbZLo3GcSkNmFnPC`), VANGUARD MORNINGSTAR GROWTH ETF, 2026-10-09, direct shape, 91.983333 from 123 trade rows (23 distinct ids), recompute equal. Trace output: `TRACE_2026-10-09.json`.
- Rejected by the issuer (amendment 2) on two conditions. (c) Entity `0` is a catch-all: its client name reads as a bucket label, it holds 210 accounts and 3,052 open lots, and it is not a client an advisor opens. (d) In that object the same asset carries two served prices on one date (83.78 on 5 lots, 91.9833 on 14 lots).
- Not re-measured here; the reasons are the issuer's, from amendment 2.

## Reproduce

1. Fetch the served object (read only): `aws s3api get-object --bucket opal-data-49financial --key advi/49financial/platinum/entities/clients/z08334146/detail.json --version-id ZCjWpzPR1n2uZl849onevhS.pIvSQhVA <file>`; select the lots whose `account_id` hashes to `420deb1a5526` and whose `asset_name` is `EXXONMOBIL HOLDINGS CORP COM SHS`.
2. `python org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~4/trace_canonical_only.py --asset "EXXONMOBIL HOLDINGS CORP COM SHS" --date 2026-10-09 --out <file>` (expect `source=transaction_observed trades=4 match=true`).
3. `python org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/2.0.0_SA_COO~K1/round1/checks/r1_checks.py thread --file org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~4/THREAD_TRACE.json`.

The default instrument run, `trace_price.py --asset ... --date 2026-10-09` (output `TRACE_2026-10-09_thread.json`), shows the daily-first tie pick and is kept as evidence of S5 and S6.
