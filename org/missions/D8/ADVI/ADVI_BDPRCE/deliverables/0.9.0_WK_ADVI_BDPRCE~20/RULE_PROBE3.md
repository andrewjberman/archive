# RULE_PROBE3 -- BP-c-1, R1.3 with the served-pair unit source (order section 1.000)

Record: `RULE_PROBE3.json` (md5 378a02eda2288c47108709d5ab71ea8a). Probe: `rule_probe3.py` (read-only, `python -I`).
Determinism: two separate builds in one process, md5 `1fdc9a8fc3eabfb37f1a73665354b025` for both; `deterministic` true.
Read verbs only. The canonical series (md5 = ETag a88a7030f4506ac7e0cdb844382f9d16) and the dimension (md5 = ETag
45dfaab5b5756b8458c6cfae63bf9f38) were fetched this session with `aws s3api get-object`; the transaction partitions are
the verified local copies named by `PARTITIONS2.csv`, each md5-checked before it was read. The lot extract sha256 is
e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b (verified).

## The amendment as built

- `served_unit_map(pairs)` (pure) takes rows of `asset_name`, `served_price`, `per_unit_value`. Per asset the median of
  `served_price / per_unit_value` over its usable pairs; a pair with a missing or non-positive value is skipped.
  Within 10 percent of 100 is `per100`; within 10 percent of 1 is `per_unit`; anything else, or no usable pair, is
  `unreadable`, with the median ratio beside it. The trade-row ratio test in `price_for_date` keeps its 1 percent bands.
- `price_for_date`, `withheld_for_date` and `exclusion_census` take the REQUIRED keyword `served_units`. Fixed Income
  rows follow R1.2 for `per_unit`, as executed or x100 for `per100`, and `unit_unreadable` for `unreadable` or an
  asset missing from the map. `AMENDMENT = "R1.3"`; `RULE_ID = "R1"`.
- The probe's pairs: the 1,689 `transaction_observed` rows of the served canonical series for 2026-09-16..2026-10-13
  (888 assets), each paired with the same-date Buy, Sale, Dividend Reinvestment and Income Reinvestment rows of that
  asset (trade_date keyed, read from the verified partitions 2026-09-16..2026-10-14; 12,726 distinct trade pairs after
  dropping 50,862 repeated transaction ids), plus the 151,035 lot pairs of the lot extract on the served assets.

## Served units (888 served assets)

| per100 | per_unit | unreadable | of which no usable pair |
|---|---|---|---|
| 0 | 807 | 81 | 73 |

Of the 815 assets with a median ratio: 807 sit in the per-unit band (0.9 to 1.1), 8 sit outside both bands (one
between 0.5 and 0.9, three between 1.1 and 5, three between 5 and 50, one at 181.4453: BECTON DICKINSON & CO COM).
No asset sits in the per-100 band. `units_source` in the record names both sources.

## Named assets and the round-2 rows

| asset | date | kind | price | unit | against the order |
|---|---|---|---|---|---|
| MORGAN STANLEY FIN LLC 0% 05/03/2029 | 2025-05-28 | withheld (unit_unreadable), 1 row, ratio 100.0 | none | unreadable | expected 100.0 per100: NOT MET (W20-S5) |
| BLACKROCK INC COM | 2026-09-22 | trade, 4 ids, Dividend Reinvestment | 1074.9259 | per_unit | expected 1074.9259: met |
| MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031 | 2026-10-09 | trade, 1 id, Sale | 1.0419 | per_unit | expected 1.0419: met |
| ALLSPRING CORE BOND CIT CLASS E2 | 2026-10-02 | trade, 2 ids, Buy | 10.3525 | per_unit | expected 10.3525, not scaled: met |

The eight round-2 `scale_100x` rows: 8 of 8 read equal to the served price (`unit_scale_rows_unchanged` 8 of 8). They
are BANK MIDWEST SPIRIT LAKE IOWA 3.85% 2026, PNC BANK NATIONAL ASSOCIATION 4.1% 2027, STATE BK INDIA NEW YORK NY 3.95%
2027, TRUIST BK 3.9% 2026 and WELLS FARGO BANK NATL ASSN 3.8% 2026 (all 2026-09-16), CITIGROUP INC 5.3% 07/22/2032
(2026-09-22, 0.97021), and MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033 and MIAMI-DADE (2026-10-09). Each reads per_unit
and is scaled 100 to 1 by R1.2; 8 scaled asset-dates in all, 2 with a coupon present.

`unit_changed_assets` = 0.

## Par-quoted counts (five probe dates, each read with the next day)

- scaled rows 24; scaled asset-dates 8; per_unit_left 3,847; par_as_executed 0; converted_to_per100 0.
- withheld unit_unreadable 203 (per date: 20, 5, 12, 23, 143); of those 197 read within 1 percent of 1, 1 reads 100.0
  (MORGAN 2025-05-28) and 5 read other ratios. The per-unit shape is withheld here because the unit read fails (W20-S9).
- fixed_income_assets_in_dimension 2,521; conflicting names excluded: JPMORGAN CHASE BK N A 5.5% 2024, NEW YORK
  TRANSN DEV CORP SPL F 5% 12/01/2030, VANGUARD TOTAL BOND MARKET INDEX I.

## Types seen (raw rows with a target trade_date, both partitions of each target)

Buy 8,029; Sale 7,817; Dividend Reinvestment 19,012; Income Reinvestment 201; Dividend 30,839; Interest 9,820; Cash
Deposit 1,386; Cash Withdrawal 841; Transfer In 695; Transfer Out 311; Expense 334; Capital Gains 21; Journal 52.

Not classified: `Corporate Action` (8 rows, all on 2026-10-02). The module does not know the type, so it counts them
UNCLASSIFIED and excludes them, as clause 1 requires (round-2 row W13-S3 recorded the same type).

## What is not met, and where it is filed

- MORGAN STANLEY FIN LLC 0% 05/03/2029 does not read per 100 (no usable pair; its served row on 2025-05-28 reads 1.0,
  per unit): ADVI_BDPRCE-D1-W20-S5.
- No served asset reads per 100 under the ruled 10 percent bands: ADVI_BDPRCE-D1-W20-S6.
- The 2026 partitions sit under `tx/`, not `tx_back/`: ADVI_BDPRCE-D1-W20-S7.
- The served canonical object moved again (ETag a88a7030 at 04:03:36Z): ADVI_BDPRCE-D1-W20-S8.
- Withheld per-unit-shaped rows, re-read on the served-pair source: ADVI_BDPRCE-D1-W20-S9.
- Round-2 rows W20-S1 and W20-S2 are re-read in S5 and S9; W20-S3 and W20-S4 stand as filed.
