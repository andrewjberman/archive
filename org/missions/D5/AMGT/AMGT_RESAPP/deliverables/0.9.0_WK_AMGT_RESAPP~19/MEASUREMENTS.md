# AMGT-rj-4 -- the measurements, with their denominators

`0.9.0_WK_AMGT_RESAPP~19`, worktree `C:/tmp/wk-amgt-11-2` (branch `wk-amgt_resapp-11-2`,
cut from SITEZ @`fa72663c56`). Every number here is an OUTPUT, not a paraphrase; each carries
what it is out of. DELIVER item 1 of the cell.

## 1. The ETF holdings plane, `s3://opal-data-etfs` -- READ ONLY

Measured 2026-09-15 07:4xZ (BEFORE) and 08:1xZ (AFTER), `.tools/aws` under the operator's
own credentials, plus one client-side-paginated boto3 census at 08:2xZ.

| Reading | BEFORE 07:4xZ | AFTER 08:1xZ |
| --- | --- | --- |
| `gold/` object count | 62 | 62 |
| `gold/` newest key | `gold/_manifests/2026-09-11/0ec4e7a9e3bb.json` | same |
| `gold/` newest LastModified | `2026-09-14T13:01:22+00:00` | same |
| `snapshots/` newest key, size | `snapshots/snapshot_2026-09-14.json`, 2879 | same |
| `snapshots/` count, newest LastModified | (AC1 does not produce these) | 95, `2026-09-14T22:00:17+00:00` |

Whole-bucket census, client-side paginated (a `--query length()` over this bucket returns a
PER-PAGE count -- it printed `1000` then `518`): **1518 objects**. Objects with a
LastModified at or after this worker's first act (2026-09-15T07:40Z): **7 of 1518**, all
`bbg/2026-09-14/*` at 07:52:34Z -- another producer's Bloomberg pull, under a prefix this
cell never reads or writes. **No object under `gold/`, `gold/holding/`, `gold/book/`,
`snapshots/` or `config/` carries a LastModified inside this worker's window.**
Prefix counts: `gold/` 62, `gold/holding/` 14, `gold/book/` 14, `snapshots/` 95,
`config/` 1, `silver/` 482, `daily/` 285, `bbg/` 254, `bbg-testpull/` 300, `platinum/` 38.

### The layout, measured before it was used

`gold/holding/` is partitioned by DATE, not by book: one object per date,
`gold/holding/date=<d>/holding.parquet`, carrying every book as a `book` COLUMN. So the
cell's per-book key-substring count returns 0 for all four books while all four are present
(row `AMGT_RESAPP-Z-W19-S1`).

Newest partition `gold/holding/date=2026-09-11/holding.parquet` (45,452 bytes, LastModified
`2026-09-14T13:01:22+00:00`): **189 rows, 31 columns, 170 distinct tickers**.
Book row counts: **PFDE 90, IDVZ 45, DIVZ 30, PFOE 24 = 189 of 189** -- 4 of 4 books present.
Columns: `date, book, ticker, name, cusip, asset_class, sub_asset_class, industry_group,
industry_group_basis, weight, market_value, shares, price, is_cash, fee, aum, yield,
duration, credit, beta, active, domicile, geography, return_1D, return_WTD, return_MTD,
return_1M, return_QTD, return_1Q, return_YTD, return_1Y`.
**No exchange/listing column exists**; a cusip value is present on 187 of 189 rows.
`snapshots/snapshot_2026-09-14.json` is 2,879 bytes -- four ETF header objects, no holdings.

## 2. The persisted publication-association key surfaces

Client-side-paginated boto3 census of `s3://opal-data-harvest`: **71 objects total.**

| Surface | Denominator | Keys, verbatim |
| --- | --- | --- |
| `publication-links/v1/` | 3 CommonPrefixes, 7 objects | `BA/`, `COST/`, `HD/` |
| `packs/` | 5 CommonPrefixes | `BABA_US`, `BA_US`, `COST_US`, `NVDA_US_Equity`, `SAP_GY_Equity` |
| `derived/model_block/` | 14 objects, 4 first-segments | `BABA_US_Equity`, `BA_US_Equity`, `NVDA_US_Equity`, `SAP_GY_Equity` |
| `derived/model_block_fye/` | 3 objects, 3 first-segments | `BABA_US_Equity`, `BA_US_Equity`, `SAP_GY_Equity` |
| `raw/bloomberg/` | 13 objects, 4 first-segments | as `derived/model_block/` |
| `raw/seekingalpha/` | 18 objects, 3 first-segments | `BABA_US`, `BA_US`, `COST_US` |
| `deliverables/0.9.0_WK_AMGT_RESAPP~1/` | 8 `model_block_*.json` files | `BA_US_Equity`, `BABA_US_Equity`, `SAP_GY_Equity`, `BABACVOCTRL_US_Equity` |

**Three conventions on ONE name**, exactly as `4.0.0_SA_CRO~W` measured: Boeing is `BA US`
(source universe), `BA_US_Equity` (model artifact) and `BA` (publication association).
Keys containing `security-`: **0 of 71** -- the `security-<16 hex>` form is COMPUTED by the
harvester's loader, not persisted (row `AMGT_RESAPP-Z-W19-S3`). The rule is reproduced
exactly here: `security-` + `sha256('Alibaba BABA')[:16]` = `security-b05e0ccdc9868504`,
the CRO's independently measured value.

## 3. The crosswalk -- INTERFACE X-1

`crosswalk/v1/2026-09-15.json`, 188,380 bytes,
sha256 `c9ea41499ffcf88d07969d6a0ac78ae8631b602368fed5ce270e6a063dfb8a36`.

- input_names **89**, records **89** -- ONE disposition per name.
- MEASURED **33**, UNRESOLVED **56** (33 + 56 = 89).
- UNRESOLVED records carrying a security_key: **0 of 56** -- nothing is guessed.
- records carrying at least one association key: **89 of 89** (5 pilot bare roots + 84
  `security-<16 hex>`; MEASURED records add the pack and model forms).
- conventions carried: **6** -- `bare-root-pilot-key`, `security-hash-key`, `pack-key`,
  `model-key`, `bloomberg-identifier`, `bloomberg-identifier-with-equity-suffix`.
- fixed point: two runs on unchanged inputs are BYTE-IDENTICAL (no run clock in the object).

The single coverage name that is MEASURED upstream but UNRESOLVED here is
`Schlumberger SLB`: its Bloomberg value is `SLB` with no exchange code, and the contract
forbids guessing it as US (34 MEASURED upstream -> 33 canonical; row `W19-S2`).

## 4. The union universe -- INTERFACE U-1

`universe/v1/2026-09-15.json`, 185,928 bytes,
sha256 `b281b0312011580623e3be2c4fdc2d6c70222c3dea86aa41c91fb17d2939f0a4`.
`snapshot_date` **2026-09-14**; holdings read from
`gold/holding/date=2026-09-11/holding.parquet` for all four books.

| Denominator | Value |
| --- | --- |
| coverage | 89 |
| holdings_distinct | 170 |
| union | 256 (= 89 + 170 - 3) |
| both | 3 |
| resolved | 33 |
| unresolved | 223 |
| with_cik | 12 |

The 3 joins are `BA` (PFDE), `HD` (DIVZ) and `VLO` -- each matched on a bare-root PILOT
association key that is PERSISTED at `publication-links/v1/<KEY>/`. 167 of 170 holdings
identifiers stay UNRESOLVED with their raw identifier; 4 of those (`ASML`, `INTU`, `NU`,
`PBR`) are root-equal to a canonical identity and NAME that candidate without merging it
(row `AMGT_RESAPP-Z-W19-S6`).

## 5. The filing identity

SEC ticker-to-CIK table, `https://www.sec.gov/files/company_tickers.json`, fetched once
2026-09-15T07:44:17Z, HTTP 200, 797,759 bytes,
sha256 `82cd5fd9ccffda811b93ba76070460dd41429c02c00e726f83deb71f553c6cff`,
source Last-Modified `Mon, 14 Sep 2026 21:02:02 GMT`: **10,422 rows, 10,422 distinct
tickers**, each `{cik_str, ticker, title}` -- 3 fields, no form type (row `W19-S4`).
Probed over **33 of 33** canonical roots: **15 present, 18 absent** (each recorded).
`form_expected` MEASURED per CIK from `https://data.sec.gov/submissions/CIK<10>.json`
(15 CIKs) as the most recent annual filing among 10-K / 20-F / 40-F.
Egress authority: Andrew-direct ~05:42Z @`dfa63b6d92`. Cache with retrieval times:
`sec_ticker_cik_cache.json` beside this file; the union build reads the CACHE and makes no
network call, so `--dry-run` is offline and deterministic.

**The name-agreement guard fired 3 times of 15 present roots** -- all genuine cross-listing
ticker collisions, refused rather than guessed:

| Canonical identity | SEC ticker | SEC title | Verdict |
| --- | --- | --- | --- |
| `RKT_LN_Equity` (Reckitt Benckiser) | RKT | Rocket Companies, Inc. | REFUSED |
| `ROG_SW_Equity` (Roche) | ROG | ROGERS CORP | REFUSED |
| `ST_SP_Equity` (Singapore Telecom) | ST | Sensata Technologies Holding plc | REFUSED |

The 12 accepted: `ASML_NA` 937966 20-F, `BABA_US` 1577552 20-F, `BA_US` 12927 10-K,
`COST_US` 909832 10-K, `HAL_US` 45012 10-K, `HD_US` 354950 10-K, `INTU_US` 896878 10-K,
`KMB_US` 55785 10-K, `NU_US` 1691493 20-F, `PBR_US` 1119639 20-F, `SAP_GY` 1000184 20-F,
`VLO_US` 1035002 10-K.

## 6. Controls

- **Mutant, FIRED-AS-EXPECTED.** The unmutated `universe/v1` validates; injecting a guessed
  key (`AAPL_US_Equity` onto an UNRESOLVED holding row) makes the schema raise
  `'AAPL_US_Equity' is not of type 'null'` at `names[89].security_key`.
- **Determinism, STABLE.** `--dry-run` twice -> identical sha256 on both objects; a unit arm
  asserts the byte equality for each interface.
- **A defect this control caught.** The first `--dry-run` wrote 191,481 bytes where the pool
  upload carried 188,380: this device's text-mode stdout CRLF-translates the payload, so the
  dry run was not a dry run of the same object. Both emitters now write
  `sys.stdout.buffer`, and the head-object `document-sha256` equals the local sha256 of the
  dry-run bytes exactly.
