# BP-c-1 RULE_PROBE2 -- R1.2 (amendment 2) run over the real silver/transactions partitions

Worker `0.9.0_WK_ADVI_BDPRCE~13`, branch `wk-ADVI_BDPRCE-13`, cut from `e82f01c4ff` with the issuer's `544d551f1d`. Record: `RULE_PROBE2.json`. Probe script: `rule_probe2.py` (same folder; run at its own path with `python -I`). Nothing served moves; no writer imports the module.

## Reads (claim: measured)

- Nine partitions read with `.tools/aws s3api get-object` (READ verb only), read at `2026-10-14T02:22:48Z`: `silver/transactions/<date>.parquet` for 2026-09-16, 09-17, 09-22, 09-23, 10-02, 10-03, 10-08, 10-09, 10-10 (each target date and its next day), plus `silver/bd_assets_dim.parquet`. Every ETag matched the MD5 of the local copy. 2026-10-03 holds 0 rows of the on-date census.
- Determinism: two runs in one process are equal (`deterministic` true). Two separate processes over the same bytes wrote byte-equal files. Run 1 (the record) and run 2 both have MD5 `94d27407d4e97f5ae7bdfba737307313`, 19,059 bytes.

## The amendment as built (`data/black_diamond/scripts/silver/bd_price_rule.py`, `AMENDMENT = "R1.2"`)

- Default trade set A = {Buy, Sale, Dividend Reinvestment, Income Reinvestment}. `TRADE_TYPES_BUY_SALE` is the sensitivity only.
- Transfer In, Journal, cash legs and all other types are excluded and counted by name; an unseen type is UNCLASSIFIED.
- Per row, `_par_decide`: `ratio = price / (|market_value| / |units|)`.
  - A Fixed Income asset (`asset_super_class_bd == 'Fixed Income'`, the name set passed in) with ratio within 1 percent of 100 is SCALED by 1/100.
  - A Fixed Income asset with ratio within 1 percent of 1 is a per-unit quote: LEFT ALONE, counted `per_unit_left`, never withheld.
  - Any other Fixed Income ratio, or no computable ratio, is WITHHELD `ratio_unrecognised` with its printed ratio.
  - A non-Fixed-Income row within 1 percent of 100 is WITHHELD with its ratio (never scaled). Other non-Fixed-Income rows are kept at their price, as in round 2.
- The coupon is a corroborating read only (`coupon_corroboration`). It decides nothing; the candidate set does not depend on it.
- Candidate names: a name is Fixed Income only when every dimension row for it carries the class. Mixed names are excluded and listed.
- Carry-forward unchanged; the observation date travels with the price. Interpolation still refused.
- Test: 36 arms, `BD PRICE RULE TEST: OK 36 arms`.

## The dimension rule and its counts

- 12,232 dimension rows; 2,562 rows carry `Fixed Income`.
- **2,521 Fixed Income asset names** in the dimension (every row of the name is Fixed Income).
- Three names carry rows that disagree on the class and are excluded and listed: JPMORGAN CHASE BK N A 5.5% 2024 (Fixed Income and Cash & Cash Equivalents), NEW YORK TRANSN DEV CORP SPL F 5% 12/01/2030 (Fixed Income and To Be Classified), VANGUARD TOTAL BOND MARKET INDEX I (Fixed Income and To Be Classified). Under the class test alone, NEW YORK ST DORM AUTH and PREMONT TEX IND SCH DIST no longer conflict; round 3's first seat listed them through the coupon test.
- Over the five target dates (each with its next partition read):
  - **Scaled rows: 24** across 8 asset-dates. 2026-09-16: 5 rows (5 names); 2026-09-22: 5 rows (CITIGROUP); 2026-10-09: 14 rows (MIAMI-DADE 7, MISSOURI 7).
  - **Per unit left: 39,114 rows** across 36 Fixed Income names (per date: 507, 1,381, 955, 35,112, 1,159).
  - **Withheld: 9 rows, all `ratio_unrecognised`**, and no others. VANGUARD SHORT-TERM INVESTMENT-GRADE INV on 2026-09-16 (5 rows, ratio 1.084382) and POLEN OPPORTUNISTIC HIGH YIELD - INS on 2026-10-08 (4 rows, ratio 1.043334). Both are Fixed Income funds whose price sits 4 to 8 percent off market value per unit; neither is within 1 percent of 1 or of 100.
  - `withheld_ratios` (all nine, sorted): 1.0433 x4, 1.0844 x5. No non-Fixed-Income row was withheld on the five dates.
- Coupon corroboration: 2 of the 8 scaled asset-dates carry a non-null coupon (MIAMI-DADE, MISSOURI). The other six have a null coupon and are scaled all the same.
- `unit_scale_rows_unchanged` = **8 of 8**. Each round-2 `scale_100x` row now reads equal to its served per-unit price (`old_price` in `BEFORE_AFTER.csv`) within `1e-6 * max(1, |served|)`. The PNC row differs from its served value by 5e-7, which is the rounding in the round-2 list.

## What each named asset reads now (R1.2 against round 2)

| date | asset | R1.2 kind, price | round 2 | note |
|---|---|---|---|---|
| 2026-09-22 | BLACKROCK INC COM | trade, **1074.9259** (4 distinct ids, Dividend Reinvestment) | B 1074.9259; A absent | read as before |
| 2026-10-09 | EXXONMOBIL HOLDINGS CORP COM SHS | **absent** (Transfer In only); carry-forward 168.29 observed 2026-10-08 | Transfer In row | read as before |
| 2026-10-09 | MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031 | trade, **1.0419** (scaled, id 745369166) | 104.19 | equal to served 1.0419 |
| 2026-09-22 | CITIGROUP INC 5.3% 07/22/2032 | trade, **0.97021** (scaled, coupon null) | 97.021 | equal to served 0.97021 |
| 2026-10-09 | MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033 | trade, **1.0401** (scaled) | 104.01 | equal to served 1.0401 |
| 2026-10-02 | ALLSPRING CORE BOND CIT CLASS E2 | trade, **10.3525**, not scaled (2 ids) | 10.3525 | not scaled; its dimension class is To Be Classified, so it is kept as a non-Fixed-Income row (see the surprise rows) |
| 2026-09-16 | BANK MIDWEST, PNC, STATE BK INDIA, TRUIST, WELLS FARGO | trade, scaled to 0.99662 / 0.995823 / 0.99629 / 0.99722 / 0.996876 | 0.99662 / 0.9958225 / 0.99629 / 0.99722 / 0.9968764 | each equal to served; coupon null |

## Types seen (raw rows whose trade_date is a target date; 163,384 rows)

Buy 22,927; Sale 42,727; Dividend 51,411; Dividend Reinvestment 31,835; Income Reinvestment 202; Interest 9,824; Cash Deposit 1,580; Cash Withdrawal 906; Transfer In 882; Transfer Out 373; Expense 636; Journal 52; Capital Gains 21; Corporate Action 8 (UNCLASSIFIED, excluded, all on 2026-10-02). Full counts: `types_seen` in the JSON.

## Denominators (per target date, rows on the date)

| date | rows | kept | scaled | per unit left | withheld | no price | no asset | assets on date / priced / absent |
|---|---|---|---|---|---|---|---|---|
| 2026-09-16 | 13,816 | 2,835 | 5 | 507 | 5 | 0 | 0 | 212 / 174 / 38 |
| 2026-09-22 | 52,858 | 23,082 | 5 | 1,381 | 0 | 2 | 5 | 232 / 196 / 36 |
| 2026-10-02 | 5,861 | 4,471 | 0 | 955 | 0 | 0 | 0 | 486 / 442 / 44 |
| 2026-10-08 | 84,516 | 62,868 | 0 | 35,112 | 4 | 0 | 0 | 466 / 426 / 40 |
| 2026-10-09 | 6,333 | 4,414 | 14 | 1,159 | 0 | 0 | 5 | 182 / 100 / 82 |

Each row lands in exactly one class (`exclusion_census`); `kept` includes the scaled and per-unit rows.

## Could not classify or reconcile (each has a surprise row)

- ALLSPRING CORE BOND CIT CLASS E2 is `To Be Classified` in the dimension, not Fixed Income. It reads 10.3525 by the non-Fixed-Income keep path.
- Two Fixed Income funds withheld on their ratio: VANGUARD SHORT-TERM INVESTMENT-GRADE INV (2026-09-16) and POLEN OPPORTUNISTIC HIGH YIELD - INS (2026-10-08). The rule withholds them and nothing replaces their price on those dates.
- Three dimension names with mixed class rows (listed above), where round 3's coupon-based list named four.
- The amendment is silent on a non-Fixed-Income row whose ratio is neither near 1 nor near 100. It is kept at its executed price (round 2's behaviour), which is the reading recorded here.
- The task order's date list omits 2026-09-16, which holds five of the eight `scale_100x` rows. The probe reads that partition and its next day.
- Corporate Action (8 rows, 2026-10-02): counted UNCLASSIFIED (first seat's row S3).
- Two Sale rows at price 0.0 on 2026-09-22 (INVESCO DISCOVERY Y): excluded and counted in `no_price_excluded` (first seat's row S6).
