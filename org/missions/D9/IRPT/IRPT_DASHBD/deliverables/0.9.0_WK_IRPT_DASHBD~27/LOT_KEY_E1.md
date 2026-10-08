# LOT_KEY_E1 -- the realized-lot key (TO-DB-b-47), counts only

Day 2026-10-06. Source: the realized-lot partition of that day, read from S3 (reads only). No lot id, account or amount is written.

## Counts
- Rows read: 175 (the rows whose lot id repeats), 87 ids, 36 accounts; rows identical in every table column: 0.
- Unique under the current key (firm, account, closing date, lot id): 87 of 175.
- Current key plus one column, unique of 175: ticker_symbol 87, cusip 87, quantity 175, acquired_date 90, holding_term 87, proceeds 175, cost_basis 175, realized_gain 173, custodian_cost_basis 175.
- Smallest column set over every column tried: size 1, [['quantity']].
- Key: the current key plus `quantity` (the first column, in table order, that completes it). Unique under it: 175 of 175.
- Necessary within the 175: ['quantity']; dropping it leaves 87 of 175. Each current-key column dropped alone leaves 175 of 175 (quantity alone separates these rows; row IRPT_DASHBD-W27-S1).
- Whole day frame (2523 rows): unique under the current key 2435, under the new key 2523; dropping lot id from the new key leaves 2357, dropping quantity leaves 2435; identical-in-every-column rows 0.
- The producer's realized_rows over the whole day frame: 2523 rows in, 2523 out, refused False, repeated keys 0.
- Rows per account over the 36 accounts (rows: accounts): {'2': 28, '4': 1, '12': 2, '14': 2, '16': 1, '20': 1, '27': 1}.

## Change
- Realized contract `primary_key` and the producer's `PRIMARY_KEYS` now end in `quantity`; the unrealized contract is unchanged (its rows are summed per lot id, so its id cannot repeat).
- realized_rows keeps both refusals: a row identical in every column to another, and a repeat of the whole key.
- Tests: 43 pass, including three new ones (one named `shared_id`, two named `true_duplicate`).
