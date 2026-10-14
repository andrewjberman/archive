# BP-c-5 -- lot key proof, round 3 (ruled key v1.1): the proof FAILS its zero targets; nothing applied

Worker 0.9.0_WK_ADVI_BDPRCE~17, round 3, branch wk-ADVI_BDPRCE-17 cut from 0fc99b5801. Record: `LOT_PROOF2.json`
(written by `test_lot_split2.py --emit-proof`). Result: `LOT SPLIT2 TEST: FAIL` (arms 9 and 10). Measured, not rounded.

## The key and why

Ruled key (PRD v1.1): `(relationship_id, account_id, asset_id, open_date, unit_cost)`, or the export's own lot identifier.
`key_basis` = **relationship_id**. Columns considered for a lot identifier: all 15 recorded headers (`Open Date`,
`Market Value`, `Unit Cost`, `Inherited Date`, `Relationship ID`, `Account Number`, `AccountID`, `AssetID`, `Asset Name`,
`Last Dividend`, `Original Asset Name`, `Asset Display Name`, `Symbol`, `Ticker`, `CUSIP`). No header is a lot, tax-lot or
position identifier. `Relationship ID` is the nearest candidate and is not unique: 3,432 distinct values in 500,000 rows.

Export: `UNREALIZED_DAILY_2026-10-09.xlsx`, VersionId `Wf2Pct313A.w7y1GpuSf2f7FfiKUVats`, sha256 `5700843f...39ef5b`,
500,000 data rows, 15 columns (the same bytes as round 2's recorded export).

## Counts against round 2

| measure | round 2 (4-column key, BP-b-6) | round 3 (ruled 5-column key) |
|---|---|---|
| export rows | 500,000 | 500,000 |
| exact duplicate rows (all 15 columns) | not measured | 0 |
| lot rows | 484,447 | **499,808** |
| rows folded (distinct rows minus lot rows) | 15,553 | **192** |
| colliding groups (null Open Date kept as one value) | 14,865 (14,696 with nulls dropped) | 191 |
| colliding groups still differing on a recorded column | not measured | **191** |

Round 2's 14,696 and 14,514 are pandas `groupby` counts with the default `dropna=True`, which silently drop the 7,384
null-Open-Date rows. Its 30,418 rows is the `dropna=False` count. Round 2 mixed the two conventions. With null Open Date
kept as a value (the convention `drop_duplicates` uses), the figures are 14,865 groups and 14,683 differing on
Relationship ID. The 15,553 folded rows are unchanged by this.

## What the ruled key leaves

- 191 colliding groups (383 rows). Each differs on **Market Value** (191 of 191). One group also differs on **Inherited Date**.
- None of the 192 folded rows has a null Open Date. The residue is not a null-handling artifact.
- Inference, labelled as such: within one snapshot, one asset has one price, so two rows with equal key and different
  Market Value most likely hold different quantities, that is, distinct lots. The export carries no Units column, so this
  is not verified on the recorded export.
- Candidate wider key tested for reference, NOT ruled: key plus `market_value` gives 500,000 lots, 0 folded, 0 colliding.
  Market Value is a daily measured value, not an identity, so this is not a lot key. It is recorded to show where the residue lives.

## Byte equality and address

- Legacy `silver/unrealized/2026-10-09.parquet`: sha256 `d65ce03d4efb0ddd182f54ba0430a327c368eabf3fe3f5f00f896bbd689405ad`,
  108,439 rows, 17 columns. Equal in all three arms (repo on original, patched on original, patched on export with the two
  synthetic columns), and equal to round 2's legacy hash. The two synthetic columns are dropped before the legacy build and
  never reach it. Legacy key `(account_id, asset_name)` is unchanged.
- Lot address (builder output, `lib/opal_naming.py address()`): `s3://opal-data-assets/blackdiamond/49financial/silver/unrealized_lots/date=2026-10-09`.

## The CAP and what an incomplete export means for the zero

- CAP verdict read from `0.9.0_WK_ADVI_BDPRCE~16/CAP.json`: **CAP**. 15 daily exports sit at exactly 500,000 rows from
  2026-07-08 on, including 2026-10-09.
- The proof therefore says that the key does not fold the 500,000 rows it SAW. It does not say that no lot was missed. A
  zero here would hold for the rows exported, not for the snapshot.
- Paging plan (CAP record: slice on the Relationship ID filter): **not runnable from readable data**. S3 holds one unrealized
  object per date and no slice exports. The `_complete/2026-10-09.json` marker carries `has_data_rows`, `bytes` and `landed_at`,
  with no row count or page field. The fixture was NOT paged. A paged fixture would need new Black Diamond exports, which is a
  producer run and is out of bounds.

## What the live first export could change that this fixture cannot

1. The live export carries real `Units` and `Cost Basis`. A key that adds units is a candidate this fixture CANNOT test: the
   fixture's units are synthetic (a hash of the 15 recorded columns). The 192 residual rows may separate on units, or may not.
2. The row cap. If BD lifts it, the row count and the residue change; the 192 are a count on the capped 500,000.
3. The header names. If the live headers differ from the recorded ones, the key columns fail to resolve and the lot table is not written.

## Rollback

Template apply: none performed. The S3 template's prior VersionId, recorded in round 2's `LOT_PROOF.json`, is
`VgzqQbd.3F3sAlllb6SWsjKZ2XvXgAfE`. Restoring it returns the template to its pre-switch bytes.

## Verdict

The ruled key does NOT reach the target. Rows folded 192 (target 0). Colliding groups still differing 191 (target 0).
The apply stays closed. Surfaced as BLOCKING row `ADVI_BDPRCE-D1-W17-S1`, ARMED, disarm owner `2.0.0_SA_COO~K1`.
