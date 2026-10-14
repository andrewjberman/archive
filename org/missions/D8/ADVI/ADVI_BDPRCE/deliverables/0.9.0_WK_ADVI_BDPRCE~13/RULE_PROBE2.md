# BP-c-1 RULE_PROBE2 -- R1.1 (amendment 1) run over the real silver/transactions partitions

Worker `0.9.0_WK_ADVI_BDPRCE~13`, branch `wk-ADVI_BDPRCE-13`, cut from `94d1161b08`. Record: `RULE_PROBE2.json`. Probe script: `rule_probe2.py` (same folder; run at its own path with `python -I`). Nothing served moves; no writer imports the module.

## Reads (claim: measured)

- Ten partitions read with `.tools/aws s3api get-object` (READ verb only): `silver/transactions/<date>.parquet` for 2026-09-16, 09-17, 09-22, 09-23, 10-02, 10-03, 10-08, 10-09, 10-10, plus `silver/bd_assets_dim.parquet`. 2026-10-03 holds 0 rows.
- The probe reads each target date's partition and the next (union, the trade_date key decides, clause 6).
- Determinism: two runs in one process are equal (`deterministic` true). Two separate processes over the same bytes wrote byte-equal files: run 1 (the record) and run 2 both MD5 `523247e6fb2779774f613747a6f08827`, 10,103 bytes.

## The amendment as built (`data/black_diamond/scripts/silver/bd_price_rule.py`, `AMENDMENT = "R1.1"`)

- Default trade set A = {Buy, Sale, Dividend Reinvestment, Income Reinvestment}. `TRADE_TYPES_BUY_SALE` is the sensitivity only.
- Transfer In, Journal, cash legs and all other types are excluded and counted by name; an unseen type is UNCLASSIFIED.
- Par-quoted: a candidate row (name in `par_quoted_candidates(dim)`) is scaled by 1/100 when `price / (|mv|/|units|)` is within 1 percent of 100. Within 1 percent of 1 it is withheld `ratio_near_1`; otherwise withheld `ratio_unrecognised`.
- Carry-forward unchanged; the observation date travels with the price. Interpolation still refused.
- Test: 26 arms, `BD PRICE RULE TEST: OK 26 arms`.

## The dimension rule and its counts

- 12,232 dimension rows. A candidate row is `asset_super_class_bd == 'Fixed Income'` AND `coupon_rate` not null: 1,163 rows, **1,129 candidate names**.
- Four names carry dimension rows that disagree on the test (for example `JPMORGAN CHASE BK N A 5.5% 2024`). A name is a candidate only when every row qualifies, so these four are excluded, not guessed.
- **Coverage gap.** Of the eight round-2 `scale_100x` rows, the rule selects **two** (MIAMI-DADE 5.25%, MISSOURI 5%). The other six are Fixed Income with a null `coupon_rate` and read at 100x. Their ratio `price/(mv/units)` is within 1 percent of 100, so they are listed in `fixed_income_unscaled_with_ratio_near_100` (not scaled). Surprise rows `ADVI_BDPRCE-D1-W13-S1` and `-S2` record this.
- Over the five target dates (2026-09-16, 09-22, 10-02, 10-08, 10-09) the probe scaled 2 asset-dates and withheld 0 rows (`ratio_near_1` 0, `ratio_unrecognised` 0).
- `unit_scale_rows_unchanged` = **2 of 8**. Expected 8 under the ruling as written; the coupon test cannot reach six of them.

## What each named asset reads now (R1.1 against round 2)

| date | asset | R1.1 kind, price | round 2 | note |
|---|---|---|---|---|
| 2026-09-22 | BLACKROCK INC COM | trade, **1074.9259** (4 distinct ids) | B 1074.9259; A absent | expected reinvestment price, met |
| 2026-10-09 | EXXONMOBIL HOLDINGS CORP COM SHS | **absent** (Transfer In only, 168.94 excluded); carry-forward 168.29 observed 2026-10-08 | Transfer In row | expected `absent`, met |
| 2026-10-09 | MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031 | trade, **1.0419** (scaled, id 745369166) | 104.19 | expected 1.0419, met |
| 2026-09-22 | CITIGROUP INC 5.3% 07/22/2032 | trade, **97.021**, not scaled | 97.021 | expected 0.97021, **not met**: coupon null |
| 2026-10-09 | MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033 | trade, **1.0401** (scaled) | 104.01 | scaled |
| 2026-10-02 | ALLSPRING CORE BOND CIT CLASS E2 | trade, **10.3525**, not scaled (2 ids) | 10.3525 | expected, met |
| 2026-09-16 | BANK MIDWEST, PNC, STATE BK INDIA, TRUIST, WELLS FARGO | trade, unchanged 99.662 / 99.5823 / 99.629 / 99.722 / 99.6876 | same | coupon null, not scaled |

## Types seen (raw rows whose trade_date is a target date)

Buy 22,927; Sale 42,727; Dividend 51,411; Dividend Reinvestment 31,835; Income Reinvestment 202; Interest 9,824; Cash Deposit 1,580; Cash Withdrawal 906; Transfer In 882; Transfer Out 373; Expense 636; Journal 52; Capital Gains 21; **Corporate Action 8** (unseen in round 2; UNCLASSIFIED, excluded, all on 2026-10-02, 2 distinct ids). Full counts: `types_seen` in the JSON.

## Could not classify or reconcile (each has a surprise row)

- `Corporate Action` (8 rows, 2026-10-02): counted UNCLASSIFIED.
- Two Sale rows at price 0.0 on 2026-09-22 (INVESCO DISCOVERY Y, ids 734745995 and 734745996) are excluded and counted in `no_price_excluded`. Round 2's record said no trade row lacked a valid price.
- `BEFORE_AFTER.csv` gives BLACKROCK 09-22 `new_price_A` 1078.04 with 0 distinct trades. The round-2 probe (`RULE_PROBE.md`) records variant A as absent for that asset-date.
- The task order's date list omits 2026-09-16, which holds five of the eight `scale_100x` rows. Its partition and the next (09-17) were read as well.

## Denominators

- 2026-10-09 census: 6,333 rows on the date, of which 5 name no asset; 182 assets on the date = 100 priced + 82 absent. The census for every target date is in the JSON `census`.
- `assets_scaled` counts asset-dates with at least one scaled row. `withheld_disagreement` counts rows withheld `ratio_near_1`.
