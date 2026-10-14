# BP-c-7 -- where the prices of the 1,859 off-canonical lots came from (round 3, read-only)

Worker `0.9.0_WK_ADVI_BDPRCE~19`, claim: **measured**. Record: `OFFCANON.json`. Lot lines: `OFFCANON_LOTS.csv` (keys hashed).
Scripts: `scripts/bp_c7_fetch.py`, `bp_c7_classify.py`, `bp_c7_named_rps.py`, `bp_c7_named_holdings.py`, `bp_c7_named_historical.py`, `bp_c7_record.py`.

## Counts (denominator 1,859 lots, 353 distinct asset/price/date triples, 340 assets)

| Class | Lots | Triples |
|---|---|---|
| EQUALS_OLDER_CANONICAL_VERSION | 310 | 22 |
| EQUALS_DAILY_FILE_ROW | 0 | 0 |
| EQUALS_NAMED_OTHER_SOURCE | 1,118 | 146 |
| UNEXPLAINED | 431 | 185 |

The 431 unexplained lots are 397 priced lots (159 triples) and 34 lots with no served price at all (the literal string `nan`, 26 triples). The 34 are counted here because the round-2 bucket put them in the off-canonical class; they are not prices.

Versions read: all 841 parquet versions of the price store (657 canonical, 184 daily), 0 failures. The earlier 14-day stage was not enough to classify, so the read widened to the full listing.

## Biggest groups

- Older canonical version: LORD ABBETT SHORT DURATION INCOME I at 3.82 (72 lots). The price sits in the canonical table as a 2022-10-12 row (transaction_observed) and is carried in 656 older versions.
- Named source (Schwab RPS): VANGUARD MORNINGSTAR GROWTH ETF at 83.78 (300 lots). The order's example lot is not a canonical price at all. 83.78 is the closing price of ticker VUG in the 2026-07-23 RPS partition, on accounts that hold the lot.
- Unexplained: COLUMBIA INTERMEDIATE DUR MUNI BD ADV at 9.5379 (106 lots); OCEAN PARK TACTICAL CORE INCOME INSTL at 19.3702 (44 lots).

By asset-name kind (diagnostic, from the name only): ETF 419 lots (416 named RPS); bond or income funds 700 (250 named, 252 older canonical, 198 unexplained); other 740 (452 named, 57 older canonical, 231 unexplained).

## What each source means for the served price

- **Older canonical version (310 lots):** the lot carries a price the canonical table held in an earlier build, not the current one. A number that was once canonical and was later superseded.
- **Daily file (0 lots):** 18 triples have a daily-file row, and every one of them also has an older canonical row. The first-match order gives them to the class above, so this class is empty by precedence. In the data, the daily row and the canonical row for those triples coincide.
- **Named other source (1,118 lots):** the served price equals a Schwab RPS closing price from the 2026-07-23 partition. B_01 reprices lots from RPS (`B_01.holdings_lots.py:2215-2288`), and its partition resolver falls back to the latest partition when the snapshot date has none (`:529-560`). No partition exists after 2026-07-23, so the 2026-10-09 lots take July closes. The match is account plus exact price (negative control 0 of 305; positive control 300 of 300). For 132 of the 146 triples every matching row carries one ticker. The other 14 are price collisions across securities, so the binding is strong, not exact.

## What a later fix would change (named, not made)

- Named-source lots: the repricing read the July partition for an October snapshot. A fix would either land a current RPS partition or stop the fallback at `B_01.holdings_lots.py:529-560`, so the served price moves to the 2026-10-09 canonical value (VUG-type lots: 91.98 on the example date, not 83.78).
- Older-canonical lots: the price read an earlier canonical state. A fix reads the current row for `data_as_of`.
- The 34 literal-nan lots need a source that emits a price, or an exclusion from the off-canonical count.

## What stays unexplained

- 397 priced lots (159 triples) match no canonical version, no daily row, no 2026-07-23 RPS account-price, and no 2026-10-09 canonical holdings row at that name, account and price (`gold/canonical/holdings/2026-10-09.parquet`, B_01:1169, 1288-1334; control 0 of 158, positive control 300 of 300).
- `silver/historical_prices.parquet` cannot be bound by name: it has no asset_name and the lots carry no ticker. A value-only check gives 3 coincidences of 158 (0.0001, 1.0, 9.69), none classed (surprise row ADVI_BDPRCE-D1-W19-S3).
- Not read: name-variant canonical rows (the projection kept only the 340 names and their tickers); the one unexplained lot dated other than 2026-10-09; the RPS and holdings checks bind by account and price, not by cusip, because the extract has no cusip.

Surprise rows filed: `ADVI_BDPRCE-D1-W19-S1` (34 nan-price lots inside the off-canonical class), `-S2` (no RPS partition after 2026-07-23), `-S3` (historical table not bindable by name).
