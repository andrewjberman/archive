# LEGACY_ROWS_Z-W19-S16 -- the ten bare-partition chatter rows (read-only measure, 0.9.0_WK_AMGT_RESAPP~278, round 77)

Method: two DynamoDB `query` calls (reads only) on `opal-harvest-security-metrics`, 2026-10-06; no put, update or delete by any path.
Note: the ten rows are CHATTER-axis rows (`TRENDING_CHATTER#2026-09-15`), not price rows.

## Count and keys
Partition `TRENDING_CHATTER#2026-09-15` holds **11 items** (Count 11 = ScannedCount 11, no LastEvaluatedKey): **10 rows** + 1 `_CURRENT` pointer.
Rows (all computed_at 2026-09-15T18:55Z, rank_sort 00001-00010): 2317 TT, 9433 JP, 992 HK, ASML NA, BA US, BABA US, BBSE3 BZ, BP/ LN, COST US, Enel IM.
Pointer `_CURRENT`: state COMPLETE, generation_id `20260915T200841Z-adf383740a9e`, row_count 10, written_at 2026-09-15T20:08Z, run_id R20260915T200833Z.

## Answer 1 -- does any served route read the bare partition's rows?
No. `lib/research/api/scoped_amgt.py` touches the bare partition only for the pointer: `read_generation_pointer` (line 444-452) does GetItem
`{axis_date: partition_key(axis, date), ticker: "_CURRENT"}`; rows come from `read_generation_rows` (line 511-532) -> `_query_generation`
(line 491-510), a query of `generation_key(...)` = `TRENDING_CHATTER#<date>#<generation_id>` only. The point read (line ~3390, `read_point_record`) follows the same pointer.
The line-1772 batch read is also pointer-only. The ten bare rows are served by nothing live; only a rolled-back adapter that read the bare partition's rows would serve them.

## Answer 2 -- are the names also in a generation partition?
Yes. Generation partition `TRENDING_CHATTER#2026-09-15#20260915T200841Z-adf383740a9e` holds 10 rows (computed_at 2026-09-15T20:08Z). 9 of 10 names match exactly;
the tenth differs by case only (bare `Enel IM`, generation `ENEL IM`). So all 10 names are duplicated, 10 of 10.

## Answer 3 -- shadowed, duplicated or orphaned?
DUPLICATED and unserved: the bare rows are not the only copy of any name; the generation partition holds the committed copy the pointer serves.
The bare rows are the pre-act producer's output (score 0, raw_chatter_count 0, window_total_count 0 per the row), superseded by the 20:08Z generation.
The before-values of the 18:55Z upsert were never captured and cannot now be recovered from this read.

## Recommended disposition
LEAVE AS A RECORD (close Z-W19-S16 on this evidence). No remedy: the rows are inert to every live route, a delete is outside this cell's grant, and the pointer shares
the partition so a partition-level clean-up would need an item-level delete that buys nothing. If the issuer ever wants them gone, that is a separate owner-approved,
item-level delete of the 10 `rank_sort` rows only, never the `_CURRENT` pointer.
