# IRPT_YCDGEN round 8, cell YCD-e-8 (CTO ADDENDUM 8.2 @d954d8deba) -- why 155 Opal-held sections say INPUT_MISSING: part 1

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~07:2xZ, read-only. Part 2 (this request's own securities against the store) needs the
request's tickers and follows in one served read.

## 1. The stated reason does not say which of three things happened (code)

`infra/aws/lambda/investor-reporting/ycharts/research/opal_producer.py:104-116` `closed_reason`: EVERY layout reason that starts
`NOT_HELD:` becomes `INPUT_MISSING:held_<group>`. `held_data.value_of` (`held_data.py:271-288`) returns NotHeld for three
different causes: the group has no rule (Opal holds no such figure, by design); a field mismatch; or
`<table>.<field> is empty for all N holdings`. The page states one reason for all three. The layout's own word is kept only in
the run's trace.

## 2. The 158 Opal-held elements of the Overview map, split by rule (code + the map in the repo)

Map `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json`: 254 elements, 158 with `computed: OPAL_HELD`. The
census of the report (`SECTION_CENSUS_REQ_5e4149d2_REV6_20261011.md`) read 155 of them NOT_AVAILABLE and 3 with a value.

| class | elements | what it means |
|---|---|---|
| NO RULE in `held_data.RULES` | 70 | Opal does not keep the figure, by design: bond-sleeve look-through 30, market-cap and style-box 14, no per-holding table 11, and 15 others. A NOT_AVAILABLE here is the designed answer under a misleading word |
| HAS RULE, fed from the characteristics parquet | 85 | `CNTRY_OF_DOMICILE` 67 (every `region_exposure_*`), `GICS_SECTOR_NAME` 14 (every `stock_sector_*`), `FUND_EXPENSE_RATIO` 2, `EQY_DVD_YLD_IND_NET` 1, `CUR_MKT_CAP` 1 |
| HAS RULE, fed from `etf-classifications` (`asset_class`) | 3 | |
| field mismatch | 0 | |

The CTO's three inputs: `region_exposure` 67 of 67 HAS RULE; `stock_sector` 14 of 14 HAS RULE; `bond_maturity` 17 of 17 NO RULE.

So of the 155 unavailable: 70 are "not kept, by design", and **85 are rule-fed from the characteristics parquet and all 85 read
empty**. (Arithmetic: 158 - 70 - 85 = 3 = the classification-fed elements = the 3 Opal-held sections that carry a value.)

## 3. The store itself (direct read)

`s3://opal-data-etfs/bbg/2026-10-09/characteristics.parquet`, 20,392 bytes, LastModified 2026-10-10T11:06:48Z, the latest dated
folder. Read with pyarrow 25.0.1.

- Rows: **172 securities**. Key column `security`, in the form `<TICKER> US Equity`.
- `CNTRY_OF_DOMICILE`: non-null 172 of 172. `GICS_SECTOR_NAME`: 164 of 172. `CUR_MKT_CAP`: 169 of 172.
  `EQY_DVD_YLD_IND_NET`: 137 of 172. `FUND_EXPENSE_RATIO`: 8 of 172.

The store holds rows for these inputs, for a universe of 172 securities only.

## 4. What is established and what is not

- ESTABLISHED: the data IS kept for 172 securities; 85 rule-fed sections read empty for this request; 70 others are not kept by
  design.
- NOT ESTABLISHED: whether this request's 10 securities (one 49financial account, `F1_49F_PORTFOLIO_PROVENANCE_20261009.json`)
  are among the 172. If 0 of 10 are, the 85 are true for this portfolio (the store's coverage is the missing hop). If some are,
  the report's read or join is the break (the key form `<TICKER> US Equity`, or the read itself on the host).
- Part 2 decides it: the count of the request's tickers present in the store's key set, k of 10, with no ticker written.
