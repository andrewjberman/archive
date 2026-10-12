# STORE_UNADJUSTED_FIELD -- ADVI_COTBKF.TO-CB-bz-2 (round 78), worker 0.9.0_WK_ADVI_COTBKF~149, written 2026-10-12T01:12:30Z

The store does not hold an unadjusted close for any of the 15 funds: its one price column (`price`, from the writer's `close`) equals the cache's unadjusted Close on only 3.2 to 10.2 percent of the dates each fund has a Yahoo row (within 0.1 percent), is at or below it on 99.9 to 100 percent of dates, and equals it only on the last dates before the store's last vendor row; it is not the cache's Adj Close times one constant either (5 to 16 distinct ratios per fund), which fits a dividend-adjusted series as of an earlier pull. The unadjusted close exists on disk only in the local vendor cache, and it covers every one of the 20718 held trading days of the 15 funds (0 uncovered, 0 before 2020-06-29); the store covers 0 of 29834 held dates with an unadjusted field, the cache covers 20718 of 29834 (the other 9116 are non-trading days the build interpolates).

## The store and its writer

- Store object: s3://opal-data-cot/silver/prices/canonical_prices.parquet, LastModified 2026-10-09T13:41:04Z, 97,443,387 bytes, 11,289,398 rows. Read by ONE get (plus one head) through the .tools/aws shim; the local copy is flattened to kind, key, day, price, source.
- Schema, from the object: date timestamp[ns], asset_name string, ticker string, price double, source string. One price column. No source_firm column (the writer at HEAD writes one, data/cot/scripts/gold/build_canonical_prices_v2.py:873), so the object was written by an earlier version of the writer.
- Writer: the price is the `close` column of silver/historical_prices.parquet (data/cot/scripts/gold/build_canonical_prices_v2.py:822), source `yahoo_finance` (:703-707); `transaction_observed` fills only dates Yahoo lacks (:709-713); `linear_interpolation` :744; `carry_forward` :755. The writer carries ONE price, never an adjusted and an unadjusted side by side.

## Is an unadjusted close in the store?

No. For all 15 funds `store_field` = none: `price` equals the cache's unadjusted Close on 3.2 to 10.2 percent of dates (within 0.1 percent) and equals it only on the last dates before the store's last vendor row (2026-06-05). It is not the cache Adj Close times one constant (5 to 16 distinct ratios per fund). `transaction_observed` (custodian-derived) appears once in the 15 funds' rows (DFLVX 2026-04-14, equal to the cache Close); `scoped_override` and `transaction_observed_capped` exist elsewhere in the object.

| ticker | store dates (adjusted price rows) | first | last | share = Close (Yahoo rows) | held dates | by store (unadj.) | by cache | held trading days | cache trading | uncovered trading |
|---|---|---|---|---|---|---|---|---|---|---|
| VEIRX | 1595 | 2022-01-27 | 2026-06-09 | 0.049 | 1677 | 0 | 1177 | 1177 | 1177 | 0 |
| PCBIX | 1749 | 2021-08-26 | 2026-06-09 | 0.100 | 1831 | 0 | 1283 | 1283 | 1283 | 0 |
| ABNFX | 2092 | 2020-09-17 | 2026-06-09 | 0.032 | 2174 | 0 | 1520 | 1520 | 1520 | 0 |
| SGIIX | 2165 | 2020-07-06 | 2026-06-09 | 0.083 | 2210 | 0 | 1535 | 1535 | 1535 | 0 |
| GFFFX | 2164 | 2020-07-07 | 2026-06-09 | 0.078 | 2246 | 0 | 1571 | 1571 | 1571 | 0 |
| FOCPX | 2156 | 2020-07-15 | 2026-06-09 | 0.080 | 2172 | 0 | 1499 | 1499 | 1499 | 0 |
| FCNTX | 2156 | 2020-07-15 | 2026-06-09 | 0.055 | 2201 | 0 | 1528 | 1528 | 1528 | 0 |
| PRILX | 1633 | 2021-12-20 | 2026-06-09 | 0.102 | 1633 | 0 | 1121 | 1121 | 1121 | 0 |
| BALCX | 1510 | 2022-04-22 | 2026-06-09 | 0.055 | 1510 | 0 | 1036 | 1036 | 1036 | 0 |
| AGTHX | 2154 | 2020-07-17 | 2026-06-09 | 0.079 | 2236 | 0 | 1563 | 1563 | 1563 | 0 |
| DISVX | 1807 | 2021-06-29 | 2026-06-09 | 0.038 | 1807 | 0 | 1242 | 1242 | 1242 | 0 |
| DFLVX | 2049 | 2020-10-30 | 2026-06-09 | 0.034 | 2049 | 0 | 1407 | 1407 | 1407 | 0 |
| NFFFX | 1668 | 2021-11-15 | 2026-06-09 | 0.101 | 1750 | 0 | 1227 | 1227 | 1227 | 0 |
| MEIIX | 2161 | 2020-07-10 | 2026-06-09 | 0.032 | 2243 | 0 | 1568 | 1568 | 1568 | 0 |
| VGHAX | 2095 | 2020-09-14 | 2026-06-09 | 0.033 | 2095 | 0 | 1441 | 1441 | 1441 | 0 |
| total | | | | | 29834 | 0 | 20718 | 20718 | 20718 | 0 |

Held dates = the dates the build (r34/after/security_day_price) values the fund, including non-trading days it interpolates (9116 of them). A trading day is a NYSE session (lib/trading_calendar, cross-checked against 1,639 SPY bars). Held trading days before 2020-06-29: 0 (earliest held day is 2020-07-06). Within the back-fill window to 2026-06-22: 29226 held dates, 20110 held trading days, 0 without a cache bar. In the csv, `store_dates`/`store_first`/`store_last` count the dates the store has an (adjusted) price row for the ticker; `held_covered_by_store` is 0 because no store field is the unadjusted series.

## The fifteenth

VGHAX lacks trades to test on, not a field and not dates: 5 trade units (1 within 1 percent of the cache Close, 2 in 1-5 percent, 2 in 5-20 percent; class too_few; median ratio 0.9592 to the cache Close), against 6 to 1,596 for the other 14. The cache Close covers all 1,441 of its held trading days and the store holds no unadjusted field for it, as for the other 14. Beside that, the store's key VGHAX is not one security: it carries 3 asset_names (VANGUARD HEALTH CARE INV from 2020-09-14, INVESCO HEALTH CARE INVSTOR from 2021-12-17, VANGUARD HEALTH CARE ADM from 2023-03-03) with the same Yahoo series under all three (4,926 rows on 2,095 dates), so the 2,095 held dates from 2020-09-14 rest on a ticker-keyed series that three names share; which of the three the held CUSIP is was not read.

## Upstream landing (code only)

data/mdpf/scripts/demque/land_cot.py: :1-5 docstring (lands into s3://opal-data-cot/silver/historical_prices.parquet, columns ticker, date, close); :23 HIST_COLS = [ticker, date, close]; :79 HIST_KEY = the row cottonwood-silver-historical-prices; :150 close = pd.to_numeric(px['as_traded_close']); :144-145 a ticker already present is never rewritten. Writer side: data/cot/scripts/gold/build_canonical_prices_v2.py:169-170 (INPUT_ADDRESSES['historical_prices'], registry row cottonwood-silver-historical-prices, infra/logic/registry/legacy_addresses.json:117-119) and :566-574.

no, by code: the landing declares ONE price column (close) and no second price field, so it keeps nothing the store drops. For a NEW ticker that one column is the as-traded close (land_cot.py:150); for a ticker already present it writes nothing (:144-145), and the 15 funds' rows are existing rows whose loader this cell did not read.

## Not established

- What the `close` column of silver/historical_prices.parquet is in the vendor's own terms, and who wrote the 15 funds' rows into it: land_cot.py only appends NEW tickers (:144-145); the original loader of existing rows was not read. 'Dividend-adjusted as of an earlier pull' is inferred from the ratios to the cache (price <= Close on 99.9 to 100 percent of common dates; ratio to Close rises to 1.0 on the last dates; ratio to the later-pulled Adj Close is a step function of 5 to 16 values), not read from a field.
- Held dates after the store's last date (2026-06-09): 680 fund-days for 10 funds are valued from the gold holdings snapshot (build `store` = cottonwood-gold-canonical-holdings), not from the store; the store has no row for them and this cell did not read the snapshot's price basis (bd_snapshot, market value over units, per the round-77 records).
- The store's own last vendor row for all 15 is 2026-06-05; the 2026-06-06..2026-06-09 rows are flat at the 2026-06-05 price and labelled linear_interpolation (2 to 3 trading days per fund, 0 carry_forward rows exist in the object).
- The cache is a file on one box, not a store a build reads; 'covered by the cache' is the existence of a cache bar, not a statement that a build can read it. Whether the cache Close is as-traded for every date (not only where it reproduces the price paid, 14 of 15 funds) is the round-77 test, not re-run here.
- Trading day = a NYSE session by lib/trading_calendar.is_trading_day (calendar_source: NYSE/hardcoded-fallback-2010-2027, covering all years read); cross-checked against the SPY bars in the same cache: 1,639 of 1,639 weekdays from 2020-06-29 to 2026-10-08 agree. No other local price copy was searched for an unadjusted close; the count of uncovered days is against the store and the cache only.
- The object was loaded whole (97 MB) to read the 15 tickers; two aggregate counts over all rows were printed (source value counts; tickers with more than one asset_name). No price of another ticker was printed or written.
