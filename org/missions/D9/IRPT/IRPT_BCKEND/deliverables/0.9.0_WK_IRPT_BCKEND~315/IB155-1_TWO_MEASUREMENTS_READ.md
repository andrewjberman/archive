# IB155-1 (IB-pr-459) -- the landed prices store against the unadjusted Close, and the performance route's reader over a non-OK day

READ ONLY. Base 9f5ecc2f80. Counts only. Data: `IB155-1_two_measurements.json`; driver `ib155_measure.py` (set-up lines from the ~308 and ~310 scripts run unchanged; the Yahoo pass is ~310's `ib150_fetch_yahoo.py`).

## AMENDMENT 1 -- the answer per fund class, and the store's date coverage (read these first)

**Governing sentence: an adjusted close dates nothing.** Counts only; the same 878 tickers, the same rule (relative 1e-4), the same Yahoo cache (no second pass). Driver `ib155_by_class.py`; members `by_fund_class`, `how_a_fund_is_marked_replaced`, `admitted_types_holding_not_replaced_funds`, `the_store_holds_the_unadjusted_close_by_class`, `store_date_coverage` in the json.

### 1. The store's dates (decides whether the store can be a witness at all)

- **The store holds no yahoo-labelled point on any of the 85 graded days (2026-06-10 to 2026-10-09), for any ticker: 0 of 85.** Of any label, also 0 of 85. Its newest yahoo-labelled point is **2026-06-05**; its newest point of any label is 2026-06-09. As it stands it cannot be a witness for a single graded day.
- The 23,976 compared ticker-days are not on the graded days. They fall on **37 distinct dates, 2026-04-15 to 2026-06-05**, all of them before the first graded day (7,776 in April, 12,960 in May, 3,240 in June; 0 on a graded day). Of the 40 trading days before the first graded day the store covers 37 for some ticker (it has nothing for 2026-06-08 and 2026-06-09, nor for 2026-04-14).
- So every equality below is read on the store's newest weeks, the days nearest its build, where an adjusted and an unadjusted close differ least. It says nothing of its older points and nothing of the graded days.

### 2. The marker: how a fund is marked replaced

The flag is the `class` column of the build's price-basis census (`price_basis_census.csv` of `0.9.0_WK_ADVI_COTBKF~60`, 3,580 tickers): `dividend_adjusted` or `mixed` is replaced (`commonwealth_daily_valuation.py:205` SUBSTITUTE_CLASSES; `:200-201` the census path; `:214-221` load; `:246-288` the replacement, with `:258-262` keeping the store's points for a flagged ticker that has no cached Yahoo series). It is a table of the build, not a column of the store (the store has `date`, `asset_name`, `ticker`, `price`, `source` only). The round-76 records call the same set `substituted` (`PRICE_PAID.json` population: the series that differ between `r34/before` and `r34/after`; 73; equal to the 73 `substituted` of `VALIDATED_UNADJUSTED.csv` column `group`). Checked here against that record: all 73 substituted funds are census class dividend_adjusted (60) or mixed (13), none of the 197 left on the store is; the census class predicts the record's flag for 270 of 270. Caveat: the cached-series condition of `:258-262` is the build's input and was not read, so here `replaced` means flagged.

### 3. The three classes (878 tickers; outcomes in the json order)

| class | tickers | every day equal | some days not equal | no yahoo point | not in store | no reader bar | ticker-days compared | equal | not equal | median store / Close on unequal days |
|---|---|---|---|---|---|---|---|---|---|---|
| replaced | 517 | 488 | 22 | 7 | 0 | 0 | 18,870 | 18,537 | 333 | 1.241 (quartiles 1.0033 and 5.0) |
| not_replaced | 141 | 130 | 8 | 2 | 0 | 1 | 5,106 | 5,059 | 47 | 4.0 (quartiles 4.0 and 4.0) |
| not_a_fund_or_unmarked | 220 | 0 | 0 | 0 | 214 | 6 | 0 | 0 | 0 | none (no compared day) |
| sum = the whole | 878 | 618 | 30 | 9 | 214 | 7 | 23,976 | 23,596 | 380 | |

No remainder in any column. `the_store_holds_the_unadjusted_close_by_class`: **replaced FOR_SOME; not_replaced FOR_SOME; not_a_fund_or_unmarked CANNOT_BE_TOLD** (the whole stays FOR_SOME). The unmarked class holds 155 registered-investment-company types and 65 exchange-traded equity types by the earlier reads' type maps, so it contains funds: the census lists only tickers that carry yahoo-labelled rows, and 214 of these 220 are not in the store at all, so there is no store point to set beside the Close.

What separates the two ends of an adjusted close: on the ticker-days where the reader's Adj Close differs from its Close by more than 1e-4 (replaced 17,988; not_replaced 1,133), the store equals the **Close** on 17,655 and 1,127, equals the **Adj Close** on 0 and 0, and neither on 333 and 6. The unequal days are whole-number-like multiples (a median of 4.0 for not_replaced), not a dividend-sized shortfall. This is the store's newest weeks only: it does not reproduce the round-76 finding (a stored close about three quarters of the price paid on the funds left on the store), which is read over trades back to 2021 and so over older points; this measurement neither confirms nor refutes it.

### 4. The nine admitted type pairs (securities among the 878; one ticker can hold more than one id; 884 in all)

| type pair (SEC asset type / share class) | securities | replaced | not_replaced | unmarked | not_replaced with unequal days |
|---|---|---|---|---|---|
| Exchange-Traded Equity Securities / Not Available | 529 | 360 | 102 | 67 | 1 |
| Registered Investment Companies (RIC) / ETF | 30 | 29 | 0 | 1 | 0 |
| RIC / A | 11 | 0 | 5 | 6 | 1 |
| RIC / No Load | 12 | 4 | 3 | 5 | 0 |
| RIC / Other | 32 | 2 | 8 | 22 | 0 |
| RIC / Retirement | 11 | 0 | 2 | 9 | 2 |
| RIC / Inv | 2 | 0 | 2 | 0 | 0 |
| RIC / Inst | 84 | 16 | 7 | 61 | 4 |
| RIC / Not Available | 173 | 109 | 12 | 52 | 0 |
| total | 884 | 520 | 141 | 223 | 8 |

(`not_replaced` totals 141, the class's ticker count; its 8 with unequal days are the class's 8 `some_days_not_equal`.) Eight security ids appear in both earlier maps with a differing ticker or pair; the first map's entry was kept (`id_pair_conflicts_between_the_maps`).

## The prior answers (unchanged by the amendment)

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

878 distinct tickers counted before fetching (under the 1,500 stop); 18 calls (17 of 50, 1 of 28), each ticker once, paced 8 seconds, none parallel, none rate-limited. Yahoo only. Amendment 1 made no further call (`fetch.passes` 1): it was computed from the cache of that pass. AWS writes 0, sign-ins 0, functions invoked 0, product files edited 0, builds proposed 0, other sources asked 0.

## Not established

See `not_established` in the JSON: the split-calendar test of the constant ratios; the basis of the non-whole-number ratios; why the store's points stop at 2026-06-05 when the object was rewritten 2026-10-09; the 214 absent tickers' spelling; any run history beyond the 2 retained versions; the reason for the 7 with no bar; the deployed route's answer; a per-token test of the reader's status filter; the other composed entry (not read).

## Surprise

Row `IRPT_BCKEND-D2-W315-S1`: the order's AC1 requires `rows` as an integer and its AC3 refuses an eight-digit token in the outputs; the store's true row count has eight digits, so both cannot hold. The issuer amended the check (AMENDMENT 2 in `p155_cells.py`: an integer count is scrubbed before the eight-digit test), and all three criteria now print PASS; no number was altered.
