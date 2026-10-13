# BP-b-3 -- lot census of the 49 Financial served home (round 2, read-only)

Worker `0.9.0_WK_ADVI_BDPRCE~7`, claim: **measured**. Record: `CENSUS.json`. Script: `scripts/census_bp_b3.py`.
Diagnostics: `scripts/census_diagnostics.py` -> `census_diagnostics.txt`. Extract (outside the checkout, not committed):
`C:/dev/wk-bdprce-r2-7-data/lot_extract.csv`, sha256 `e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b`, 198,295 rows.

## Counts

- Objects: 3,510 `detail.json` objects listed and read, 0 failed (3,931 client folders exist; 421 hold no `detail.json` and are out of scope).
- By key class: catch_all 1, acct_z 138, z0 3,371, other 0 (every `zN` key begins `z0`).
- Lots: 198,295 in 1,900 objects. All 3,510 carry a `tax.open_lots` list; 1,610 of them are empty (`open_lots_presence.txt`).
- Classes: `PRICED_FROM_CANONICAL` 4,208; `PRICED_OFF_NO_CANONICAL` 1,859; `NOT_UNTICKERED` 192,228. Sum = lots.
- Untickered lots (null, empty or UNKNOWN): 6,067 over 962 names in 942 objects. Cash-like names (regex, see below): 946, none off.

## Off-canonical lots (1,859)

- Partition: 1,814 have a canonical row for the asset on the as-of date with a different price (median absolute gap 0.55); 45 are on assets with no canonical row at all (34 names).
- Of the 1,814, 300 equal a canonical price of the asset on another date, all more than 5 days from the as-of date; 1,514 equal no canonical price of the asset.
- Equal-to-no-canonical-price total: 1,559 (1,514 + 45).
- By entity class: z0 1,792; catch_all 67; acct_z 0.
- Non-cash untickered lots: 1,859 of 5,121 are off (36.3%). The task order's 26-object sample found 61 of 586 (10.4%). The sample is not representative of the home.

## Mapping gap

- Listed-but-untickered: 1 asset, 1 lot. NACEL ENERGY CORP COM, present in `ticker_lookup.json` with ticker NCE.
- Canonical rows carry a ticker for 0 untickered names, so that condition gives 0.
- The third condition is unevaluable: `silver/historical_prices.parquet` has no `asset_name` column (date, ticker, close, fetch_date, source). Its ticker set (3,628 tickers) was not joined by name. The listed count is therefore a lower bound on conditions 1 and 2 only.

## market_value = quantity x current_price

- Lots checked: 198,261 (lots with all three numeric). Broken at tolerance max(0.01, 1e-6 x |market_value|): 21,614.
- Broken lots by class: NOT_UNTICKERED 20,520; PRICED_FROM_CANONICAL 742; PRICED_OFF_NO_CANONICAL 352.
- Of the broken lots, 16,297 carry market_value 0. Among the rest, quantity x price over market_value has quantiles 1.02 / 1.60 / 4.96 / 19.7 / 228 (5th to 95th percentile); no single multiplier explains them.

## data_as_of

- 43 distinct dates across the 3,510 objects; 3,267 objects at 2026-10-09 and 144 at 2026-04-02. Lot-bearing objects span 21 dates (2026-04-08 to 2026-10-09).

## Method

- Untickered: `ticker` null, empty or `UNKNOWN` after trimming. Ticker served in the extract is blank for null and the raw string otherwise.
- PRICED_FROM_CANONICAL: canonical row for the asset name on `data_as_of` with |price - current_price| <= 1e-6 x max(1, |price|).
- Canonical: 12,649,131 rows, 11,143 assets, 6,100,222 rows carrying a ticker. Nearest-row search window +/-5 days.
- Cash regex (diagnostic only, not a class): `CASH|MONEY MARKET|MM|FDIC|SWEEP` on the asset name.
- `account_ref` = first 12 hex of sha256(account_id). Raw account ids are never written.

## Privacy and what was not read

- `client_name` and `account_name` were parsed in memory and never printed or written.
- acct_z object keys embed an account number. The extract and committed sample carry them as `acct_z#<sha12>`. To re-read an acct_z object, list the prefix and match the hash.
- The committed sample hashes every client key (`obj#<sha12>`). The extract keeps raw z-keys outside the checkout, since the next cell re-reads by key.
- Raw object bodies were streamed, not stored. Failures: none.
- Not read: the 10,929 top-level zN files (`.json`, `_views`, `_composition`), out of scope; any per-lot pricing source (the object carries none).
- Sample: 200 rows, seed 20261013: 100 of the 1,859 PRICED_OFF_NO_CANONICAL, 50 NOT_UNTICKERED, 50 PRICED_FROM_CANONICAL.
