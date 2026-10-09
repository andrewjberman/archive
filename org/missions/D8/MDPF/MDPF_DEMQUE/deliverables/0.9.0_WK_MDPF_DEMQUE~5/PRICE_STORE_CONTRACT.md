# PRICE_STORE_CONTRACT -- the file contract ADVI_COTBKF reads (MDPF_DEMQUE DQ-t-6, hop 6)

Writer: `data/mdpf/scripts/demque/price_store.py` (`write`, `write_index`). Reader: dell2's ADVI_COTBKF. No account data lives here.

## Addresses (copied from `lib.opal_naming.address`, not typed)

One CUSIP, for example AMLP:
`s3://opal-data-assets/yahoo/global/silver/price_history/cusip=00162Q866`

The index:
`s3://opal-data-assets/yahoo/global/silver/price_history/index`

A CUSIP address is a folder. Its files are `<address>/prices.parquet`, `splits.parquet`, `dividends.parquet`, `lock.json`.
The index folder holds `index.parquet` and `index.csv` (same rows).

KEY NAMESPACE: the key is Commonwealth's 9-character CUSIP exactly as Commonwealth delivered it (not a Black Diamond CUSIP, not a ticker). A CUSIP absent from the index is not priced; do not guess a neighbour.

## Files and columns

`prices.parquet` -- one row per trading day, ONLY dates inside the lock's `[valid_from, valid_to]`:
- `date` -- trading day, midnight, no time zone.
- `close_served` -- the close as Yahoo serves it today (adjusted for splits; dividends are not folded in).
- `as_traded_close` -- the close as it actually printed that day (every later split undone).
- `cash` -- (DQ-t-21) dividend/interest cash per share, AS TRADED, going ex on that date; 0 on every other day.
- `total_return` -- (DQ-t-21) the day's total return, a fraction (0.01 = 1%): `TR_t = (P_t + D_t) / (P_{t-1} / s_t) - 1` (P as-traded close, D `cash`, s the split ratio on t). Null on the first row of the history (no prior close). Every consumer reads this column; `close_served`, `as_traded_close` and `cash` stay stored for audit.
- `tr_source` -- (DQ-t-21) `yahoo` | `bloomberg` | `accrual` | null: where `total_return` came from.
- `flags` -- (DQ-t-21) list of strings, empty when clean.

The four TR columns come AFTER `date, close_served, as_traded_close`; those three are unchanged (same values, same order, same dtypes), so a reader of the first three is not affected. Builder: `data/mdpf/scripts/demque/tr_column.py`. Two guards, both in the build:
- **(a) missing cash.** Where Bloomberg's stored `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS` (percent, `s3://opal-data-etfs/bbg/<date>/history_topup.parquet`, read only) exists for the name, a NON-ex-date day (`cash` = 0) whose Yahoo TR differs from Bloomberg's by more than 1 bp (`MISSING_CASH_BP`) carries the flag `missing_cash`: Yahoo has not recorded a distribution the market paid. The writer is given the Bloomberg frame (`write(..., bbg=)`); with none, guard (a) cannot fire.
- **(b) money market.** A symbol in `data/mdpf/scripts/demque/money_market.csv` (`symbol, cusip, basis`; seed FXFXX, SALXX) is a $1.00-NAV fund whose Yahoo TR is 0, and never takes Yahoo's TR: a date with a Bloomberg daily TR takes it (`tr_source` `bloomberg`); any other date takes the nearest prior Bloomberg daily TR carried forward (next one back-filled before the first) with `tr_source` `accrual` and flag `accrual_carried_bloomberg_rate` (an estimate, flagged on every such row); a name with no Bloomberg value at all gets null `total_return`, null `tr_source` and flag `money_market_tr_unavailable`.

Until the next scheduled draw rewrites a CUSIP, its `prices.parquet` has only the first three columns: a reader that needs `total_return` treats an absent column as not yet drawn.

`splits.parquet` -- whole history: `date`, `ratio` (new shares per old share, 2.0 = two-for-one).
`dividends.parquet` -- whole history: `date`, `amount` (cash per share). These two keep their full history so a later correction is re-derived, never re-pulled.

`lock.json` -- the lock row: `cusip, yahoo_symbol, valid_from, valid_to, method, observations_checked, observations_passed, median_abs_error, state, claim, locked_at, run_id, supersedes`. Only `state` = `LOCKED` rows are in the store.
- `claim` = `measured`: the Yahoo symbol was proved against the client's own trade prices (observations_passed of observations_checked agreed within tolerance).
- `claim` = `held`: no trade prices existed to prove it against. Not proved; a consumer may refuse it.

`index.parquet` / `index.csv` -- one row per CUSIP: `cusip, yahoo_symbol, valid_from, valid_to, rows, claim, method, as_of, run_id`. `as_of` is the latest price date held.

## Which close to value with

Value a holding with `as_traded_close`. Commonwealth quantities are as traded, so the price must be as traded. `close_served` is kept for comparison only; multiplying a Commonwealth quantity by it is wrong across a split.

## Worked example -- CUSIP 00162Q866 (AMLP)

1. Read the index; find the row with `cusip` = `00162Q866`. It names `yahoo_symbol` AMLP, a `claim`, and the valid range. If `claim` is `held` and you require proof, stop.
2. Read `cusip=00162Q866/prices.parquet`. For a holding on date D inside `[valid_from, valid_to]`, take the row with `date` = D (or the last earlier row if D was not a trading day) and read `as_traded_close`.
3. Market value = Commonwealth quantity x `as_traded_close`.
4. A date outside `[valid_from, valid_to]` has no price in this store: report it unpriced.
