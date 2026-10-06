# Commonwealth price coverage -- read of existing Opal stores (2026-10-06T22:29Z)

Universe: 4634 distinct non-blank CUSIPs from silver transactions s3://opal-data-assets/commonwealth/cottonwood/silver/transactions/date=2026-06-23/. Needed days are an UPPER BOUND (every NYSE trading day from each CUSIP's first Trade_Date through 2026-06-23).

Union across stores: priced on any day 1506 of 4634 securities; 2090953 of 9388961 security-days covered (22.3%). Not priced by any store: 3128 securities.

## By store (ALL asset types)

| store | verdict | priced any day | security-days covered | needed | matched CUSIP / ticker | reused-symbol, not credited |
|---|---|---|---|---|---|---|
| bd.silver.prices.canonical | READ_PRICE_SERIES | 1263 | 1291824 | 9388961 | 0 / 1263 | 126 (121421 days) |
| inf.silver.prices.canonical | READ_PRICE_SERIES | 645 | 359978 | 9388961 | 0 / 645 | 61 (25741 days) |
| cot.silver.prices.canonical | READ_PRICE_SERIES | 1263 | 1280457 | 9388961 | 0 / 1263 | 126 (120287 days) |
| bd.silver.historical_prices | READ_PRICE_SERIES | 1211 | 1667090 | 9388961 | 0 / 1211 | 120 (158988 days) |
| inf.silver.historical_prices | READ_PRICE_SERIES | 1041 | 1463904 | 9388961 | 0 / 1041 | 114 (151979 days) |
| etfs.rivalfunds.gold.security_market | READ_PRICE_SERIES | 56 | 0 | 9388961 | 56 / 0 | 0 (0 days) |
| portal.canon.data_pkl.return_daily | READ_PRICE_SERIES | 0 | 0 | 9388961 | 0 / 0 | 0 (0 days) |
| etfs.bbg-testpull.tickers.history | READ_PRICE_SERIES | 123 | 110204 | 9388961 | 0 / 123 | 18 (10602 days) |
| etfs.bbg.fund_daily | READ_PRICE_SERIES | 0 | 0 | 9388961 | 0 / 0 | 0 (0 days) |

## Union by asset type

| asset type | securities | priced any day | priced in window | days covered | days needed |
|---|---|---|---|---|---|
| Alternative Investment | 22 | 0 | 0 | 0 | 25305 |
| Annuity | 29 | 0 | 0 | 0 | 60198 |
| Cash | 3 | 1 | 1 | 1626 | 8682 |
| Cash Equivalent | 488 | 10 | 10 | 6243 | 482359 |
| ETF | 349 | 262 | 262 | 321592 | 610978 |
| Equity | 1830 | 912 | 908 | 1292174 | 4033672 |
| Fixed Income | 778 | 0 | 0 | 0 | 1749889 |
| Mutual Fund | 978 | 306 | 306 | 446197 | 2015941 |
| Mutual Fund (Closed End) | 99 | 15 | 15 | 23121 | 233016 |
| Unit Investment Trust | 58 | 0 | 0 | 0 | 168921 |

## Stores checked (22) with verdicts

- `bd.silver.prices.canonical` -- **READ_PRICE_SERIES** -- 12,570,765 rows (date, asset_name, ticker, price, source); 2006-01 onward; sources include carry_forward, scoped_override, linear_interpolation, transaction_observed, yahoo_finance
- `inf.silver.prices.canonical` -- **READ_PRICE_SERIES** -- 1,455,147 rows (date, ticker, price, source); 2020-06 onward
- `cot.silver.prices.canonical` -- **READ_PRICE_SERIES** -- 11,291,021 rows (date, asset_name, ticker, price, source); 2006-01 onward
- `bd.silver.historical_prices` -- **READ_PRICE_SERIES** -- 5,868,653 rows (date, ticker, close, fetch_date, source=yahoo_finance); 2020-01 onward
- `inf.silver.historical_prices` -- **READ_PRICE_SERIES** -- 4,927,223 rows (date, ticker, close, fetch_date, source=yahoo_finance); 2019-09 onward
- `etfs.rivalfunds.gold.security_market` -- **READ_PRICE_SERIES** -- G4 gold, Bloomberg-derived px_close keyed by security_id (CUSIP for US names); date=<d> partitions, MEASURED 4 partitions (not the ~730 days the order assumed)
- `portal.canon.data_pkl.return_daily` -- **READ_PRICE_SERIES** -- Yang/MDPF model-portfolio pickle canon: 136,965 rows, 87 series (79 Index, 4 Curncy, 4 Comdty), 2019-12 onward; no Equity series, so a ticker match is not expected
- `etfs.bbg-testpull.tickers.history` -- **READ_PRICE_SERIES** -- Bloomberg test pull 2026-08-21: one history.csv (date, price, return) per ticker folder; 176 ticker folders
- `etfs.bbg.fund_daily` -- **READ_PRICE_SERIES** -- daily Bloomberg fund pull: one fund_daily.csv per date folder (PX_LAST, NAV, assets) for the Opal-tracked ETFs (DIVZ, IDVZ, PFDE, PFOE)
- `bd.silver.interpolated_prices` -- **NAME_KEYED** -- 4,580,221 rows (asset_name, date, price, data_quality, num_observations): a daily series keyed by asset_name only -- no CUSIP or ticker column to match a Symbol on
- `bd+cot.silver.prices.daily_slices` -- **DERIVED_NOT_READ** -- bd 168 and cot 90 daily slice files (about 10k rows each) beside canonical_prices.parquet; the same row shape (date, asset_name, ticker, price, source) as the canonical file read above
- `bd.silver.bd_assets+daily_positions` -- **DERIVED_NOT_READ** -- 3,449,107-row transaction asset table (a per-transaction price) and the 683 MB daily positions table: firm holdings, a price only where a position or trade existed
- `inf.silver.assets_v2` -- **DERIVED_NOT_READ** -- 2,353 daily Orion position snapshots (1.9 GB) with current_price per held ticker: a mark on a held position, derived from the canonical series above
- `bd+inf+cot.gold.timeseries` -- **DERIVED_NOT_READ** -- account_performance, client_performance, holdings_lots, positions_cube: valuations and returns built from the price series above, not a price series
- `portal.canon.data_pkl.price_monthly` -- **NOT_PRICE_SERIES** -- 38 yearly files (date, index_name, bbg_ticker, price): MONTHLY index levels (Treasury yields), not daily
- `mdpf.feeds.etf_net_assets+etfs.silver.netassets` -- **NOT_PRICE_SERIES** -- NAV, net assets and shares for the four tracked funds (4 rows a day): fund NAV, not a close, same four tickers as etfs.bbg.fund_daily
- `portal.json.benchmarks+market` -- **NOT_PRICE_SERIES** -- benchmark and model-portfolio return JSON, market regime, FRED macro: index-level or composite returns
- `harvest.raw+packs+silver` -- **NOT_PRICE_SERIES** -- per-ticker officer, article and filing harvests (39 raw ticker folders, 105 packs): text, not prices
- `ycharts.firms` -- **NOT_PRICE_SERIES** -- generated report experiments and synthetic-firm inputs
- `mdpf.bronze+assets.gold.mdpf` -- **NOT_PRICE_SERIES** -- model composition and AUA aggregates
- `trade-submissions.parquet.securities` -- **NOT_PRICE_SERIES** -- one 8 KB securities file of January 2026 trade submissions
- `local.data.yang_pkl` -- **NOT_PRICE_SERIES** -- the pickle pipeline's code and a valuation JSON; its pickle data lands in opal-data-portal-v2 (canon/data_pkl, read above)

A price counted here may be a carried-forward, interpolated or transaction-observed value; the JSON carries each store's `by_source` split. No vendor was called and nothing was written to any store.
