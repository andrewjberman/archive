# RULE_PROBE3 -- BP-c-1, R1 AMENDMENT R1.3 over real partitions (worker 0.9.0_WK_ADVI_BDPRCE~20, round 3)

Read-only. Partitions read with `.tools/aws s3api get-object` (READ verb): `silver/transactions/<date>.parquet` for
2025-05-28, 2025-05-29, 2026-09-16, 2026-09-17, 2026-09-22, 2026-09-23, 2026-10-02, 2026-10-03, 2026-10-09,
2026-10-10, and `silver/bd_assets_dim.parquet`. Served units read from the round-2 lot extract
(`C:/dev/wk-bdprce-r2-7-data/lot_extract.csv`, sha256 `e7e618d7...2b50b`, verified). Record: `RULE_PROBE3.json`,
generator `rule_probe3.py`. Deterministic: `true` (two builds in one process compared byte-equal).

## The amendment as built (R1.3)

- `served_unit_map(lots, name, price, qty, mv)`: pure. Per asset, the median over its lots of price / (|mv| / |qty|).
  Skips a lot with zero or missing qty or mv (per the order) and, as built, a lot with a missing or non-positive
  price (surprise W20-S4). Within 1 percent of 100 reads `per100`; of 1, `per_unit`; else `unreadable`.
- `served_units` is a REQUIRED keyword (no default) on `price_for_date`, `withheld_for_date`, `exclusion_census`.
- Fixed Income, `per_unit`: R1.2 unchanged. `per100`: ratio near 100 used as executed; ratio near 1 multiplied by
  100; other ratio withheld `ratio_unrecognised`. `unreadable` or absent from the map: withheld `unit_unreadable`.
- Non-Fixed-Income rows keep R1.2 behaviour whatever their unit. Carry-forward carries the series-unit price.
- `AMENDMENT = "R1.3"`, `RULE_ID = "R1"`. Module test: 49 arms, `BD PRICE RULE TEST: OK 49 arms`.

## Served units and the dimension (measured)

- Lot extract: 198,295 lots, 2,909 asset names. Served unit: per100 **0**, per_unit **2,500**, unreadable **409**.
  Skipped lots: 16,339 with zero or missing qty or mv; 35 with missing or non-positive price.
- Dimension: 12,232 rows, 2,562 Fixed Income rows, 2,521 Fixed Income names; 3 conflicting names excluded
  (JPMORGAN CHASE BK N A 5.5% 2024; NEW YORK TRANSN DEV CORP SPL F 5% 12/01/2030; VANGUARD TOTAL BOND MARKET INDEX I).
- Of the 2,521 Fixed Income names, 342 are in the extract map (266 per_unit, 76 unreadable); 2,179 are absent.
- Scaled rows **0**; coupon-corroborated scaled rows 0; per_unit_left rows 3,990; par_as_executed 0;
  converted_to_per100 0; withheld 84, all `unit_unreadable` (unit_unreadable_rows 84).

## Named assets: R1.3 against round 2

| asset | date | R1.3 kind | R1.3 price | round 2 (served old / new A) | note |
|---|---|---|---|---|---|
| MORGAN STANLEY FIN LLC 0% 05/03/2029 | 2025-05-28 | withheld | none (1 row, ratio 100.0) | 115.995 served / 100.0 new A (carry on 2026-10-05, BEFORE_AFTER) | unit unreadable: absent from extract |
| BLACKROCK INC COM | 2026-09-22 | trade | 1074.9259 (4 ids, Dividend Reinvestment) | 1073.1623 / 1078.04 | per_unit; matches the order's reinvestment price |
| MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031 | 2026-10-09 | withheld | none (7 rows, ratio 100.0) | 1.0419 / 104.19 | unit unreadable: absent from extract |
| ALLSPRING CORE BOND CIT CLASS E2 | 2026-10-02 | trade | 10.3525 (2 ids) | 10.3525 / 10.3525 | per_unit; unchanged |

## The round-2 scale_100x rows

- unit_scale_rows_unchanged: **0 of 8**. All eight read `withheld unit_unreadable`: five on 2026-09-16 (BANK MIDWEST
  SPIRIT LAKE IOWA 3.85%, PNC BANK NATIONAL ASSOCIATION 4.1%, STATE BK INDIA NEW YORK NY 3.95%, TRUIST BK 3.9%,
  WELLS FARGO BANK NATL ASSN 3.8%), CITIGROUP INC 5.3% (2026-09-22), MIAMI-DADE and MISSOURI ST HEALTH (2026-10-09).
  None of the eight names is in the extract.
- Against R1.2 simulated on the same dates (every Fixed Income name read as per unit): R1.2 scaled 25 rows; R1.3
  withholds those 25 (near-100 ratios) plus 54 near-1 rows and 5 rows at about 1.084 that R1.2 withheld too.

## Units and types

- unit_changed_assets **0**: the probe's trade/carry assets that are in the extract (BLACKROCK, ALLSPRING) read
  1074.9259 against served 1082.39, and 10.3525 against 10.3525; neither is a 100x or 1/100 reading.
- types_seen (rows on the five target dates, both partitions): Buy 8029; Sale 7817; Dividend Reinvestment 19012;
  Income Reinvestment 201; Dividend 30839; Interest 9820; Cash Deposit 1386; Cash Withdrawal 841; Transfer In 695;
  Transfer Out 311; Expense 334; Journal 52; Capital Gains 21; Corporate Action 8 (UNCLASSIFIED, excluded).

## What could not be read or classified

- 409 extract assets read unreadable and 84 probe rows were withheld for it; per100 is empty in the extract, so the
  ruling's per100 path is exercised only by the planted frames, never by a served series.
- The served 115.995 for MORGAN comes from the round-2 served output (BEFORE_AFTER.csv), not from the extract.
  The module does not read it: the unit source is the order's, and widening it is not this worker's call.

## Surprises filed (`INVESTIGATION_v1.md`, rows ADVI_BDPRCE-D1-W20-S1..S4)

- S1 (ARMED, disarm 2.0.0_SA_COO~K1): the extract does not carry the named bonds or the eight round-2 names.
- S2 (ARMED, disarm 2.0.0_SA_COO~K1): 54 per-unit-shaped rows withheld for an absent unit.
- S3 (INERT): the four named dates omit 2026-09-16, which holds five of the eight round-2 rows.
- S4 (INERT): the module also skips non-positive or missing prices, which the order does not name.
