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
