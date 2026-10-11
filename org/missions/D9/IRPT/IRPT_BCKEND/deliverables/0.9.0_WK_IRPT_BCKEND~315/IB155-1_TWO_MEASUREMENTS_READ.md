# IB155-1 (IB-pr-459) -- the landed prices store against the unadjusted Close, and the performance route's reader over a non-OK day

READ ONLY. Base 9f5ecc2f80. Counts only. Data: `IB155-1_two_measurements.json`; driver `ib155_measure.py` (set-up lines from the ~308 and ~310 scripts run unchanged; the Yahoo pass is ~310's `ib150_fetch_yahoo.py`).

## The two answers

1. **The landed prices store holds the unadjusted Close FOR SOME tickers, and is not a source a scheduled producer can lean on today.** Of 878 tickers, 618 match the reader's Close on every compared day, 30 differ on at least one, 9 have store rows but no yahoo-labelled point on a day the reader has a bar, 214 are not in the store, 7 have no bar from the reader (871 with bars). Of 23,976 ticker-days where both exist, 23,596 are equal (relative 1e-4) and 380 are not. The store's yahoo-labelled points END 2026-06-05 (every label, 2026-06-09), though the object was last written 2026-10-09 13:41:04Z: of the 81,936 ticker-days the 125 window days need, 23,976 are covered (29 percent); no ticker has every needed day; 657 tickers' newest store day is before their newest reader day (reader: 2026-10-09). Refresh: **no schedule found.** The writer is `data/cot/scripts/gold/build_canonical_prices_v2.py` (S_00, upload at :907); the cot gold run in Terraform (`opal-cot-gold-run`) never names it; only `gold_dispatch.sh --chain full` runs it before its freshness gate and no cot trigger of that script was found (the bd twin has a daily 04:00 UTC rule for its own object). The object keeps versions (bucket versioning enabled) and holds 2: 2026-10-09T13:41:04Z and 2026-06-09T20:42:16Z, so the cadence read from the object is two writes four months apart (a floor: a lifecycle rule on non-current versions was not read).
2. **Over a window with a non-OK day the route's reader chains over it and still says `measured`.** For an Inflection account in the 1Y window with one `NON-POSITIVE-BASE` day: `days_excluded` 1, `claim` `measured`, absences `excluded_rows` (PARTIAL) beside the three UNSUPPORTED ones and three `linked_days` PARTIAL (the same three the control carries); a figure is returned over the remaining 248 of 249 days (`days_linked` 248). The control (every row OK, same window): `days_excluded` 0, `claim` `measured`, no `excluded_rows` absence. `chained_over_the_non_ok_day`: true. Code: `performance/holdings_gold.py:246` drops non-OK rows by `status == "OK"` (status-agnostic), `:254` chains the rest, `:314-317` adds the PARTIAL `excluded_rows` absence. **The arm is the reader's own code at this base over the served holdings gold read from S3 -- NOT the deployed function's answer.** What could differ: the deployed package's bytes, the route's authorization, scope resolution and envelope (the scope was built in memory for one permitted account), and the HTTP body (the reader's answer dict was read).

## Measurement 1 in detail

- Address: built by `commonwealth_price_basis_census.py:161` through `commonwealth_price_census.py:282-286` and `lib/opal_naming.py:2339` from `legacy_addresses.json:11`; resolves to the key `silver/prices/canonical_prices.parquet` in the cottonwood data bucket. 11.29 million rows, 5 columns (`date`, `asset_name`, `ticker`, `price`, `source`), 92.9 MB, 4,001 tickers. A point is yahoo-labelled when `source` is `yahoo_finance` (3.40 million rows); the other labels are linear_interpolation (7.83 million), transaction_observed, scoped_override, transaction_observed_capped.
- The 380 unequal ticker-days by cause: 174 constant ratio store/Close that is a whole number or its reciprocal (consistent with a price on another share basis, split-like); 162 constant ratio that is not a whole number; 18 within half a percent; 7 equal to the Close of an adjacent reader day; 19 other. 0 match the Adj Close (so no dividend-adjusted point was found in the compared days). Of the 30 tickers, the unequal days sit in the early part of the window (2026-04-14 to 2026-06-05), where the store's points end.
- Equality rule: `abs(store / Close - 1) <= 1e-4`; store price is the median of the ticker's yahoo-labelled rows for the date; the Close is Yahoo's with `auto_adjust=False`.

## Measurement 2 in detail

Entry `orion` (sources.json:66-68, the Inflection holdings entry the route composes at `installed.py:68`). Served gold: 1,619 partitions to 2026-10-08, 979 accounts, two status tokens (`OK`, `NON-POSITIVE-BASE`). Window: the route has no default window; the longest is Since Inception, where no account has every row OK across the 1,619 partitions, so the read is the 1Y ruled period (2025-10-08 to 2026-10-08, 249 partitions), where 641 accounts are all-OK and 1 account holds 1 to 5 non-OK days inside. Both records have 249 days in the window; `answer_keys`: absences, claim, contract_validated, evidence, refusals, report.

## Fetch and bounds

878 distinct tickers counted before fetching (under the 1,500 stop); 18 calls (17 of 50, 1 of 28), each ticker once, paced 8 seconds, none parallel, none rate-limited. Yahoo only. AWS writes 0, sign-ins 0, functions invoked 0, product files edited 0, builds proposed 0, other sources asked 0.

## Not established

See `not_established` in the JSON: the split-calendar test of the constant ratios; the basis of the non-whole-number ratios; why the store's points stop at 2026-06-05 when the object was rewritten 2026-10-09; the 214 absent tickers' spelling; any run history beyond the 2 retained versions; the reason for the 7 with no bar; the deployed route's answer; a per-token test of the reader's status filter; the other composed entry (not read).

## Surprise

Row `IRPT_BCKEND-D2-W315-S1`: the order's AC1 requires `rows` as an integer and its AC3 refuses an eight-digit token in the outputs; the store's true row count has eight digits, so both cannot hold.
