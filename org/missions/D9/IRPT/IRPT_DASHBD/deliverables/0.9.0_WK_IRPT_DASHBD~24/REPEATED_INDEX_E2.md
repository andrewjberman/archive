# REPEATED_INDEX_E2 -- counts only (TO-DB-b-42, cell DB-b-42)

Source: the one declared custody source (bucket and `transactions_prefix` read from sources.json, nothing typed).
Frames built by `read_partition(..., columns=transaction_columns(src))`, exactly as `FlowCache.get` does before `classify_and_sum`.

- trading days 2026-01-02..2026-10-05 (lib/trading_calendar.py): 190
- partitions read: 190; days with no partition: 0
- frames read: 190; rows read: 1,403,930
- frames whose index has a repeated label: 0 of 190
- index type observed: RangeIndex (unnamed) on 190 of 190
- verdict: CANNOT. No code edited; the read is the evidence.

Reason, structural: the frame's index is pyarrow's default RangeIndex (no index column is selected by `columns=`), and a multi-object day is joined with `pd.concat(ignore_index=True)`, which rebuilds a RangeIndex. A served input cannot supply a repeated label.
