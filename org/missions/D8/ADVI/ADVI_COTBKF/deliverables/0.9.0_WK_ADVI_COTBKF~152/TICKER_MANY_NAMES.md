# CB-ca-2 (round 79): basis value against split scaling, and tickers with many names

Worker 0.9.0_WK_ADVI_COTBKF~152. Local copies only: no bucket read, nothing fetched, no code changed. Records: `BASIS_VALUE_AGAINST_SPLIT_SCALING.json`, `TICKER_MANY_NAMES.json`, `TICKER_MANY_NAMES.csv`.

## Item A: where `as_traded_close` is written against the split scaling

All line numbers are `data/assets/scripts/silver/commonwealth_daily_valuation.py`.

**Answer.** The value is written BEFORE the scaling (`value_before_scaling`). The substitution writes it at :271 (yahoo_finance points) and :283 (interpolated days), in call 1 of `run()` (:973); the price input that carries the column is written at :976-978; the scaling (`split_plan` :983, `apply_splits` :984) runs after, on a separate cusip-keyed frame that has no `basis` column (:321 passes `new[PRICE_COLS]` on). Nothing records per point that a point was scaled or needed none; only a per-CUSIP plan and `SUSPECT_BEFORE` rows are kept (:995, :1013). A point therefore leaves the build marked `as_traded_close` and unscaled by construction, in the price input; the price table the chain values with (`security_day_price.parquet`: cusip, date, price, store) carries no marker at all. The signed sentence holds for no security type: the build does not read the type (:96 sets `asset_type` to the empty string).

**Call order in `main` and `run`.** (1) read stores :1048-1051; (2) read split store at the pinned instant :1063 -> :525; (3) `run` :1067; (4) `apply_price_basis` :973 -> `as_traded_store` writes `basis` (:252, :271, :283); (5) price input written with `basis` :976-978; (6) `security_day_prices` :979; (7) `split_plan` :983, only when `cash_leg` is method_r28 or method_r29 (:980; default method_r29, commonwealth_sweeps.py:103); (8) `apply_splits` :984 (every point of a CUSIP in `applied` dated before a split day; no filter on type, store, source or basis); (9) `value_days` :990; (10) `write_prices` :1007; (11) `write_basis_sidecar` :1008.

**Paths marked and unscaled** (11): by construction in the price input (reachable); the price table has no marker (reachable); a split in neither source (reachable); store and rows disagree (reachable); a split the close does not confirm (reachable); a split outside coverage (reachable); the pinned instant (reachable); a type the scaling skips (not reachable, except cash at par, which is never marked); a point after its last split (reachable, unscaled and right, not a defect); a cash leg without the repairs (reachable); CUSIP-keyed splits against ticker-keyed substitution (not established).

**Output check (A6).** `r34/after/` holds `security_day_price.parquet` (no `basis` column), `price_basis.json`, `repair_days.parquet` (not opened), `account_day_value.parquet`; no price input file and no split pin. From `price_basis.json`: 1,049,193 points replaced + 477,980 days re-derived = 1,527,173 points marked `as_traded_close` in the ticker-keyed input, 911 tickers. The count of securities with a split in their held range could not be made from disk.

## Item B: tickers carrying more than one asset name

**Control.** The store has 11,289,398 rows, 5,748,151 with no ticker; 4,000 tickers, 308 with more than one asset_name (strip + upper-case gives the same 4,000 and 308).

**How the build joins a held security to a price.** `universe_from_tx` takes each CUSIP's Symbols from the custodian rows, most common first (:83-98). `match_security` (commonwealth_price_census.py:197-216) tries the CUSIP, then the first Symbol whose key (strip + upper, :184) the store holds and no other CUSIP lists (`symbol_claims` :188-194); `resolve_series` repeats that (:368-385). The silver store is keyed by ticker only (census :57-58). `_clean_priced` keeps (kind, key, day, price, source) and drops `asset_name` (:101-108, PRICE_COLS :60). `security_day_prices` joins on (kind, key) (:402), groups by (cusip, day), and prices a day only if max - min <= 1e-6 x min (:403-406, PRICE_TOL :61); otherwise the day is left blank and blocks later stores (:407-409). So there is no dedupe, no first, no average: every name under a ticker is one series, and a day on which the names' rows differ is blank. I re-derived the build's ticker for every CUSIP by that rule: 1,263 securities, the same 1,263 the table prices from the silver store.

**The test, as written before any security was classed** (`.scratch/w152/TEST.txt`, `written_at` 2026-10-12T02:04:42Z, copied into the record). Order (b) same series, (a) own name, (c) day by day, (d) thresholds 0.001 tolerance, 0.99 own_rows, 0.50 another_names_rows, Jaccard 0.6 with margin 0.1.

**Denominators.** 1,722 CUSIPs in the build's table; 1,720 with a held day (`held_securities`); 1,263 of those have a silver ticker by the build's rule; 769 have at least one held day priced from the silver store (`priced_from_the_store_by_ticker`); 133 of those 769 carry a ticker with more than one name (171 of the 1,263). Securities taking points from more than one store are counted once per store label.

**Classes (133).** names_identical_so_indistinguishable 111; own_rows 10; own_name_not_identified 8; another_names_rows 3 (VOE, WFC, APH); mixed 1 (IGSB). By kind: ETF 48 identical, 6 own_rows, 1 another, 1 mixed, 1 not identified; Equity 59, 4, 2, 0, 7; Mutual Fund 3 identical; Cash 1 identical. Own name found by exact match on 5, by the fuzzy rule on 9, not found on 8 (of the 22 that were not identical).

**Not from their own rows (4 securities).** 1,563 held days (VOE 12, WFC 1,385, APH 48, IGSB 118), 7,816 priced holding account-days, 26 measured account-days. In each, the days not from own rows are days on which the own name has no row in the store and another label of the same ticker has one. The labels look like old and new names of one company or fund (WELLS FARGO & CO COM against WELLS FARGO CO NEW COM; AMPHENOL CORP CL A against AMPHENOL CORP NEW CL A; ISHARES 1-5 YEAR against ISHARES 0-5 YEAR); the test counts them as written.

**Sensitivity (stated in the test).** If a day on which another name's row equals own's is not counted as an own day, 10 own_rows become `mixed`; the record keeps the stated reading.

**The 15.** VEIRX, PCBIX, ABNFX, SGIIX, GFFFX, FOCPX, FCNTX, PRILX, BALCX, AGTHX, DISVX, DFLVX, NFFFX, MEIIX carry one name each (single_name); VGHAX carries 3 names, the same series (names_identical_so_indistinguishable). All 15 are held and priced from the silver store.

**No ticker (457 held securities).** 227 have no Symbol in the custodian rows, 192 a Symbol the store does not hold, 38 a Symbol that other CUSIPs list too. 52 have a priced held day (49 from the gold canonical holdings store, CUSIP first else ticker; 3 from the bbg ticker-history store, by ticker); 405 have no priced held day (431,932 held days unpriced against 275 and 794 priced).

## Off-task row

`ADVI_COTBKF-D2-W152-S1`: three securities (APH, CTVA, KLAC) whose build price on the last store day is 0.5, 0.15 and 0.1 of the store's row.
