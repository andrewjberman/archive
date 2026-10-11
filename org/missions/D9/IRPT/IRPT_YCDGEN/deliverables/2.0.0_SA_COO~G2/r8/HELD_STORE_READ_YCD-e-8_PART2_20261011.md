# IRPT_YCDGEN round 8, cell YCD-e-8 -- part 2: this request's own securities against the held-characteristics store

**By:** `2.0.0_SA_COO~G2`, window 9, one listed read at 2026-10-11T07:34:44Z on irpt-status revision 6. Record
`HELD_STORE_INTERSECT_REQ_5e4149d2_20261011.json` (same folder): counts only; no ticker, amount or file byte is kept.

## Result

| measure | value |
|---|---|
| securities in the request's original upload (distinct tickers) | **10** |
| rows in the store (`s3://opal-data-etfs/bbg/2026-10-09/characteristics.parquet`) | 172, all keyed `<TICKER> US Equity` |
| request tickers with a store row (after the ` US Equity` suffix is stripped, upper-cased) | **0 of 10** |
| request tickers equal to a store key as written | 0 of 10 |
| request tickers with a non-null `CNTRY_OF_DOMICILE` | **0 of 10** |
| request tickers with a non-null `GICS_SECTOR_NAME` | **0 of 10** |
| `bond_maturity` | no store column: 17 of 17 such elements have NO RULE (part 1) |

## Controls

- The file read is the request's own original: its sha256 equals the `sha256` the served route states
  (`91073ddf1385c0df0935c8a0d04709b5d69377ee70e213629d275f60112a23c9`, also the value in
  `F1_49F_PORTFOLIO_PROVENANCE_20261009.json`), and it holds 10 rows, the provenance file's `rows_written`.
- The matching rule discriminates: on the same parquet it finds `AAPL` and `ABBV` and does not find a made-up ticker.
  172 of 172 store keys carry the suffix.

## Reading, against the CTO's two branches (ADDENDUM 8.2)

No rows: for THIS portfolio the held-characteristics store carries none of its 10 securities. The 85 rule-fed sections that
read empty are therefore true for this request, not a failed read. With the 70 that are not kept by design, all 155
`INPUT_MISSING:held_<input>` sections are accounted for without a broken read or join. By the CTO's rule this is the
"data is not kept" branch: the store's coverage (172 securities) is FWD-1's missing hop.

## Limits

- The request's ticker SHAPES were not recorded (only counts were kept, by design). If the upload's symbols are in a different
  symbology from the store's, the resident's own read misses for the same reason this one does; this read cannot tell
  "not covered" from "covered under another symbol". The store's 172 rows hold 8 with a fund expense ratio; the rest read as
  single stocks.
- One request, one portfolio, the latest dated folder. It says nothing about coverage for another portfolio.
- The misleading word stands: `closed_reason` states `INPUT_MISSING` both for "not kept by design" and for "no row for
  this security" (part 1, section 1).
