# BP-c-5 -- lot key proof, round 3, PRD v1.3 re-seat (second seat ~23): the key carries units; the zero is deferred

Worker 0.9.0_WK_ADVI_BDPRCE~23, round 3, branch wk-ADVI_BDPRCE-23. Record: `LOT_PROOF3.json` (written by
`test_lot_split3.py --emit-proof`). Result: `LOT SPLIT3 TEST: OK 10 arms`. Nothing applied; no S3 write.

## The key and why

PRD v1.3 (CTO call 67ac): lot = (`relationship_id`, `account_id`, `asset_id`, `open_date`, `unit_cost`, `units`).
Market Value does not join the key. `key_basis` = **relationship_id**; `keyed_on_lot` = true (unique on the six columns
in the synthetic run). The patched module's `LOT_KEY_COLS` is that list, checked by arm-free assertion at load.
Columns considered for a lot identifier: all 15 recorded headers. None is a lot, tax-lot or position id.
`Relationship ID` is the nearest candidate: 3,432 distinct values in 500,000 rows.

## The 192, and what it means

Under the five-column key that v1.3 extends (no units): the patched module folds **192** rows (lot rows 499,808 from
500,000), and an independent pandas recount on the raw rows gives **192**. Equal (arm 10). Exact duplicate rows: 0.
Colliding groups on the five columns: 191, differing on Market Value in 191 and on Inherited Date in 1 (seat ~17's
numbers, reproduced). Under v1.3 those rows separate only if their `units` differ. Whether they do is UNKNOWN: the
recorded export carries no Units column, so the 192 are not separated on this fixture.

## Why a fixture cannot prove the zero

1. The recorded export (sha256 5700843f...39ef5b, VersionId Wf2Pct313A.w7y1GpuSf2f7FfiKUVats) has no Units and no
   Cost Basis column. The v1.3 key cannot be evaluated on it.
2. The synthetic `units` used by the arms (a hash of the 15 recorded columns) separates any two rows that differ on any
   column. Its 500,000 lot rows and 0 folded are true by construction, NOT evidence. The record labels them
   (`lot_rows_basis`, `synthetic_units_folded`) and they are not read as a result.
3. The mechanism is proven on a planted frame (arm 9): two rows equal on the five old columns and different on units
   both survive (2 lots); the same two rows with equal units fold to one (1 lot).

## What the first real export must show (the apply's pair, not this seat)

- Read the first real export under the apply's pair (PRD v1.3: the zero is read there, not here).
- Pass: **0 rows folded** under the six-column key, and **no colliding group differing on any column**, both read back
  from the written lot table.
- The apply's rollback: the S3 template's prior VersionId from round 2's record,
  `VgzqQbd.3F3sAlllb6SWsjKZ2XvXgAfE` (`LOT_PROOF.json` field `template.s3_version_id`).
- If the zero fails: the residue is the record, and a wider key is a CTO call, never a silent widening.

## Legacy output and address

- Legacy `silver/unrealized/2026-10-09.parquet`: sha256 `d65ce03d4efb0ddd182f54ba0430a327c368eabf3fe3f5f00f896bbd689405ad`,
  108,439 rows, 17 columns. Equal in arms 1 and 2 and equal to round 2's and seat ~17's recorded hash. The test pins the
  clock to seat ~17's value because the legacy bytes carry `_ingested_at`.
- Lot address (builder output, `lib/opal_naming.py address()`): `s3://opal-data-assets/blackdiamond/49financial/silver/unrealized_lots/date=2026-10-09`.

## The CAP and what an incomplete export means for the zero

- CAP verdict read from `0.9.0_WK_ADVI_BDPRCE~16/CAP.json`: **CAP** (15 daily exports at exactly 500,000 from 2026-07-08).
- The proof says the key does not fold the 500,000 rows it SAW. It says nothing about rows never exported.
- Paging plan: **not runnable from readable data**. A read-only key listing of `forwardfill_v2/unrealized/` gives 91 keys:
  76 daily xlsx (one per date), 15 `_complete` markers, 0 other. No slice object exists, and the markers carry no row
  count. The fixture was not paged.

## Arms (10, all PASS)

1-2 legacy bytes equal (repo on original, patched on original and with the synthetic columns); 3 lot table larger than
legacy and unique on its key; 4 units and cost basis in the lot table, in neither legacy table; 5 builder address;
6 SKIP path on the original export; 7 negative control; 8 relationship id survives; 9 planted frame, v1.3 key;
10 five-column fold through the patched module (192) equals the independent recount (192), printed, not asserted zero.

## Verdict

The v1.3 key is in the patched script and proven on a planted frame. The zero is DEFERRED to the first real export under
the apply's pair, as the CTO ruled. Nothing is applied. Surprise rows: `ADVI_BDPRCE-D1-W23-S1..S3` (see the investigation file).
