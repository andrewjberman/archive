# RULE_PROBE3 -- BP-c-1, R1.3 with the served-pair unit source, second correction (order section 1.0000)

Record: `RULE_PROBE3.json` (md5 73539f000ee5c0728194777bc7bff5fb, read_at 2026-10-14T04:34:19Z). Probe: `rule_probe3.py`
(read-only, `python -I`, run at the worktree root). Determinism: two builds in one process, both md5
`52f96ec013b50ae1375ec19125485c2b`; `deterministic` true.

Reads: the canonical series `silver/prices/canonical_prices.parquet` (ETag a88a7030f4506ac7e0cdb844382f9d16, live
head-object at 04:3xZ agrees), the dimension `silver/bd_assets_dim.parquet` (ETag 45dfaab5b5756b8458c6cfae63bf9f38,
agrees), the lot extract (sha256 e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b), and the 1,928
verified transaction partitions named by `PARTITIONS2.csv` (each md5-checked before it is read; tx_back and tx).

## The amendment as built

- `served_unit_map(pairs)` (pure) takes rows of `asset_name`, `served_price`, `per_unit_value`. Per asset, the MEDIAN of
  `served_price / per_unit_value` over all its usable pairs. A median in [50, 200] is `per100`; in [0.5, 2] is
  `per_unit`; anything else, or no usable pair, is `unreadable`, with the median beside it. The bands are coarse
  (inclusive) because a pair may mix dates. The trade-row ratio test in `price_for_date` keeps its 1 percent bands.
- `price_for_date`, `withheld_for_date` and `exclusion_census` take the REQUIRED keyword `served_units`. A Fixed Income
  row follows R1.2 for `per_unit`, is used as executed or x100 for `per100`, and is withheld `unit_unreadable` for
  `unreadable` or an asset missing from the map. `AMENDMENT = "R1.3"`; `RULE_ID = "R1"`.

## The pairs: three sources, one median per asset

For each served (asset, date) of the window 2026-09-16..2026-10-13 (1,689 `transaction_observed` rows, 888 assets):

1. nearest_earlier_trade: the single most recent trade row of that asset with trade_date strictly before the served date
   (types Buy, Sale, Dividend Reinvestment, Income Reinvestment), searched over all 1,928 verified cached partitions.
   1,382 pairs. 2,636,506 earlier trade rows on served assets were scanned; 85 had no usable per-unit value.
2. same_date_trade: the same types on the served date, from the verified partitions 2026-09-16..2026-10-14 (trade_date
   keyed). 12,726 distinct pairs after 50,862 repeated transaction ids were dropped.
3. lot_extract: the lots of the served assets, (current_price, |market_value| / |quantity|). 151,035 usable pairs.

## Served units (888 served assets)

| per100 | per_unit | unreadable | of which no usable pair |
|---|---|---|---|
| 1 | 824 | 63 | 59 |

Resolved by source (assets with at least one pair from the source): nearest_earlier_trade 677; same_date_trade 744;
lot_extract 503; any source 829; no pair 59 (888 - 829).

The one per100 asset: **MORGAN STANLEY FIN LLC 0% 05/03/2029** (served median 115.995, from its nearest earlier Buy).

The 4 unreadable assets that do have a pair, with median ratios between the bands: CALL NVIDIA CORP $250 EXP 10/02/26
0.4972393179404657; ISHARES CORE U.S. AGGREGATE BOND ETF 3.549831616098765; VANGUARD FTSE ALL-WORLD EX-US SMALL-CAP ETF
3.817494809041611; VISTANCE NETWORKS INC COM 3.7725. ISHARES is filed as ADVI_BDPRCE-D1-W20-S12 and -S13.

Per-unit assets whose median sits outside 0.9 to 1.1 (inside the band, read per_unit): 38 (for example EXXONMOBIL HOLDINGS
CORP COM SHS 1.8719). None is near 100, so no per_unit asset is contradicted by a 100x trade or lot.

`unit_changed_assets` = 0. `units_source` in the record names the three sources.

## Named assets (probe dates; each read with the next day)

| asset | date | kind | price | served unit | served median |
|---|---|---|---|---|---|
| MORGAN STANLEY FIN LLC 0% 05/03/2029 | 2025-05-28 | trade, 1 id, Buy, executed 100.0 (ratio 100.0, as executed) | 100.0 | per100 | 115.995 |
| BLACKROCK INC COM | 2026-09-22 | trade, 4 ids (Dividend Reinvestment rows; 1074.9259 per unit, market_value/units 1074.9259) | 1074.9259 | per_unit | 1.0 |
| MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031 | 2026-10-09 | trade, 1 id, Sale | 1.0419 | per_unit | 1.0 |
| ALLSPRING CORE BOND CIT CLASS E2 | 2026-10-02 | trade, 2 ids, Buy | 10.3525 | per_unit | 1.0000001436 |

All four read as the order expects (MORGAN 100.0 per 100, not 1.0; BLACKROCK 1074.9259; MIAMI-DADE 1.0419; ALLSPRING
10.3525, not scaled).

The eight round-2 `scale_100x` rows: 8 of 8 read equal to the served price (`unit_scale_rows_unchanged` 8 of 8): BANK
MIDWEST SPIRIT LAKE IOWA 3.85% 2026, PNC BANK NATIONAL ASSOCIATION 4.1% 2027, STATE BK INDIA NEW YORK NY 3.95% 2027,
TRUIST BK 3.9% 2026 and WELLS FARGO BANK NATL ASSN 3.8% 2026 (2026-09-16), CITIGROUP INC 5.3% 07/22/2032 (2026-09-22),
MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031 and MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033 (2026-10-09). Each reads
per_unit and is scaled 100 to 1 under R1.2 (8 scaled asset-dates, 24 scaled rows, 2 with a coupon present).

## Par-quoted counts (five probe dates)

- Fixed Income assets in the dimension: 2,521 names (2,562 rows); conflicting names excluded: JPMORGAN CHASE BK N A 5.5%
  2024, NEW YORK TRANSN DEV CORP SPL F 5% 12/01/2030, VANGUARD TOTAL BOND MARKET INDEX I.
- scaled rows 24; scaled asset-dates 8; per_unit_left 3,847; par_as_executed 1 (MORGAN 2025-05-28); converted_to_per100 0.
- withheld unit_unreadable 202 rows (per date: 2025-05-28 19, 2026-09-16 5, 2026-09-22 12, 2026-10-02 23, 2026-10-09 143).
  Their ratios: 197 within 1 percent of 1; 5 at 1.0844; none near 100. They belong to 18 assets: 17 that the served map
  does not carry (190 rows, no transaction_observed row in the window) and ISHARES CORE U.S. AGGREGATE BOND ETF (12 rows,
  median 3.5498 between the bands). See ADVI_BDPRCE-D1-W20-S11 and -S12.

## Types seen (raw rows with a target trade_date, both partitions of each target)

Buy 8,029; Sale 7,817; Dividend Reinvestment 19,012; Income Reinvestment 201; Dividend 30,839; Interest 9,820; Cash
Deposit 1,386; Cash Withdrawal 841; Transfer In 695; Transfer Out 311; Expense 334; Capital Gains 21; Journal 52;
Corporate Action 8 (not in the module's known types: counted UNCLASSIFIED and excluded).

## What is not met, and where it is filed

- Nothing named is unmet. The round-2 surprise rows are re-read on the second correction:
  - W20-S1 (no lot for the named and scale names) still holds: ADVI_BDPRCE-D1-W20-S10.
  - W20-S5 (MORGAN has no usable pair) no longer holds: MORGAN now reads a pair (the 2025-05-28 Buy). No new row.
  - W20-S6 (no served asset reads per 100) no longer holds: one asset does. No new row.
  - W20-S9 (Fixed Income rows withheld as unit_unreadable) still holds in its new form: ADVI_BDPRCE-D1-W20-S11.
- The 4 between-band assets: ADVI_BDPRCE-D1-W20-S12.
- ISHARES CORE U.S. AGGREGATE BOND ETF: its lot pairs dominate its median: ADVI_BDPRCE-D1-W20-S13.
- The S7 and S8 rows are unchanged facts and are not re-filed.
