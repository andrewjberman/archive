# BP-b-8 -- one unlisted holding, traced to R1 (round 2, read-only)

Worker `0.9.0_WK_ADVI_BDPRCE~12`. Record: `THREAD2.json`. Claim: measured. Served object: the z0 client detail
object whose key is in `THREAD2.json` (`served_object_key`), VersionId `HYPH2uKxlFNG38t2uQTVea9AhSB_8JHQ`, data_as_of 2026-10-09.

## The served price

- Asset: **ALLSPRING CORE BOND CIT CLASS E2**. Ticker: none (null in the served lot and in every source checked).
- Served `current_price` 10.3525 on all 72 lots of the object, in two accounts (71 lots in account_ref `f0fd0fb36c99`,
  1 lot in `38cc4c0aa5ee`). One served price per object. `market_value` 25,985.29 = quantity 2,510.05 x 10.3525.
- Kind: collective investment trust (CIT). The name carries the token CIT; the BD dimension row is To Be Classified,
  fixed_income, class_source unclassified, with a CUSIP as its only identifier.

## R1 in plain words (CTO ruling R1, merged module `bd_price_rule.py`)

The price of an untickered holding on a date is the median of its distinct trades (each transaction_id once) at the
executed price column. Non-trade rows are excluded. Ties between sources go to SOURCE_RANK, then a stable sort. With no
trade on the date, the last observed trade price is carried, with its observation date. Interpolation is banned.

## What R1 says for this holding

- On 2026-10-09 there is no Buy or Sale row, so R1 cannot price it from that day's trades (shape a fails).
- The last observed trade is 2026-10-02: two distinct Buy trades, `742108391` at 10.353 and `742108404` at 10.352.
  Their median is **10.3525**, which the carry-forward carries to 2026-10-09 with observation date 2026-10-02.
- No Buy or Sale for this asset exists in the 2026-01-01 to 2026-10-10 transaction window after 2026-10-02.
- `recompute_equals_served` is true.

## Where the served row came from (trace_price_v2.py)

The trace follows the canonical row: `linear_interpolation`, value 10.3525. The daily partition row for 2026-10-09 is
`carry_forward`, value 10.3525. Both equal the served price. The trace reports `trade_ids` empty, because it follows the
interpolated row and does not apply R1. Interpolation is banned as an output source by R1 clause 5. The value matches
R1's carry, but the row that wrote the served price is the banned interpolation.

## Why the holding is unlisted

Sources checked, each by name:
1. Served ticker (extract): blank for all 72 lots.
2. `config/ticker_lookup.json`: no entry.
3. `canonical_prices.parquet` ticker column, all dates (611 rows): no ticker.
4. `silver/historical_prices.parquet`: no asset_name column, so no name join. The dimension CUSIP is not in its ticker set.
5. `YF_OVERRIDES`, `OPAL_ETF_OVERRIDES`, `TICKER_CORRECTIONS` (`lib/ticker_overrides.py`): no entry.
6. `silver/bd_assets_dim.parquet`: ticker NaN; symbol holds the CUSIP 01988T753, not a ticker.

## The tie

No same-date source tie decided the value. On 2026-10-02 the two trades are both transaction-observed, and R1's median
of two prices is their mean. On 2026-10-09 the daily row and the canonical row tie at 10.3525. SOURCE_RANK would rank
linear_interpolation (2) ahead of carry_forward (3), which picks the canonical row the lot read. R1 clause 5 refuses
interpolation as an output, so the R1 output is the carry-forward dated 2026-10-02.

## Candidate counts (lots)

start 6,067 untickered lots; after entity class (not catch_all) 5,477; after the listed-asset exclusion 5,476; after
PRICED_FROM_CANONICAL 3,685; after one price per object and asset 3,657 (1,861 object-asset groups).
Step 5 over the 371 unlisted groups of 198 names: shape a 0; no Buy or Sale in the 2026 window 338; shape b evaluable 33
(20 equal to R1 carry, 13 unequal). Earlier history was not scanned.

## Reproduce

1. `timeout 120 python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~8/trace_price_v2.py --asset "ALLSPRING CORE BOND CIT CLASS E2" --lot-object "<served_object_key from THREAD2.json>"`
2. `timeout 300 python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~12/recompute_R1_BP-b-8.py`
3. `timeout 60 python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/2.0.0_SA_COO~K1/round2/checks/r2_checks.py thread2 --file org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~12/THREAD2.json`
