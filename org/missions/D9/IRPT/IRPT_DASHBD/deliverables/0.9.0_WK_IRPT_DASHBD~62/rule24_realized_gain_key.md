# Rule-24 record -- `realized_gain` joins the account_lot_realized primary key (IRPT_DASHBD.TO-DB-b-87, round 41, E5)

Worker 0.9.0_WK_IRPT_DASHBD~62. Ordered by 1.0.0_SA_CTO~DELL2 ADDENDUM 10 (msg 3225), row IRPT_DASHBD-S40. Counts and column names only: no
account, lot id or amount appears here. Evidence: `LOTS_KEY_R41.json` and `repeat_census_r41.py` in this folder.

## The change

`account_lot_realized` primary key, before and after (producer `PRIMARY_KEYS[TABLE_REALIZED]` equals the contract `primary_key`):

| | key |
|---|---|
| before (DB-b-73) | firm, account_id, business_date, lot_id, quantity, proceeds |
| after (this order) | firm, account_id, business_date, lot_id, quantity, proceeds, **realized_gain** |

## The reading that decides it

The 2026-10-08 realized-lot partition holds 35,834 rows over the 7,620 population accounts. Eight pairs (eight accounts, group size 2 each)
share the whole current key. Every pair differs in at least four custodian columns; none is identical in every column (0 of 8), so this is
not a source duplicate. Per pair, the differing custodian columns are:

- all 8 pairs: `gain_loss_dollars`, `gain_loss_percentage`, `w_s`, `disallowed_loss_amount`;
- 3 pairs also: `original_purchase_price`, `transaction_cost`, `transaction_cost_per_share`, `transaction_gain_loss_dollars`, `transaction_gain_loss_pct`.

Each pair is one lot split in two by a wash sale (the same shape as the 2026-10-07 pair, LOTS_KEY_E1.json): the same order, opening event,
acquired date, quantity, proceeds and cost basis, with a wash flag `w_s` and a disallowed loss on one half only, so the gain differs. The
producer's rule for a distinct real lot is to keep both rows and extend the key by the minimal real lot attribute.

## The four postulates

(i) **MECE over a declared domain.** Domain: the columns of `account_lot_realized` (19, printed in the producer's `ARROW_REALIZED`) -- a key
member must be a column of the table the key guards, because `emit_day()`'s `duplicate_keys` reads the output rows. Subtraction: 19 columns
less the 6 columns of the current key leaves 13 candidates; read over
the 8 output pairs, the candidate columns that differ within a pair are {`realized_gain`} -- 1 of 13 non-key columns, in 8 of 8 pairs;
`cost_basis`, `custodian_cost_basis`, `basis_source`, `closing_tie`, `acquired_date`, `holding_term`, `holding_trading_days`, `ticker_symbol`
and `cusip` are equal within every pair. The custodian columns that also differ (`w_s`, `disallowed_loss_amount`, `gain_loss_percentage`, ...)
are not columns of this table, so none can be a key member without a schema change. The domain was falsified once before use: the pairs were
read from the whole partition (35,834 of 35,834 rows are population accounts), not from a sample.

(ii) **Same grain.** The key names one realized lot-close event: (lot id, quantity, proceeds) say which lot and how much closed for what;
`realized_gain` is a property of that same event (proceeds less the basis the event was measured from), not of an account, a day or a
security. No coarser or finer grain enters.

(iii) **Intent coherence.** One axis, one intent: the key's only intent is row identity within an account and closing date. `realized_gain`
joins as an identity member because it is the figure that tells the wash-sale halves apart, not as a value to be summed by the key. The
refusal is kept for a true duplicate: a repeat of the whole new key still refuses by name ("key is not unique"), and a row identical in
every column still refuses ("identical in every column").

(iv) **State coherence.** This remedy moves the realized key and the refusal in `realized_rows()`. It does NOT move: the unrealized and
activity tables' keys; the served returns and class tables; any stored row (nothing is written, nothing deployed -- DB-b-88 releases it);
the earlier days' uniqueness (adding a column to a key cannot create a duplicate: 2026-10-07 is 3,245 rows with 0 repeats under the new key).

## Why the smallest

A key addition of size 0 cannot separate a pair that shares the whole key. Of the single columns of the table, only `realized_gain`
separates all eight pairs, so size 1 is the minimum and the choice is unique. (Rounds 28 and 37 chose `quantity` and `proceeds` the same way:
the first table column in table order that separates; `cost_basis` precedes `realized_gain` in table order and does not separate here.)

## Word-boundary token census (comp-find, corpus=all, 71,079 files scanned, tracked + untracked + ignored minus the printed floor)

- `\brealized_gain\b`: 37 hits -- bands DEF 1, SURFACED 9, CONFIG 13, TEST 9, DOC 5. The producer, its test file, the contract and the
  earlier lot-key records name it; the one non-IRPT_DASHBD source hit is a diagnostic script in `data/cot/scripts/gold/`, a different table.
- `\baccount_lot_realized\b`: 208 hits -- DEF 5, SURFACED 10, CONFIG 130, TEST 8, DOC 55. The consumers that read the table are the
  reporting-gold handler and the release checks; none of them types the key (a read of the lambda's emission test for `PRIMARY_KEYS`,
  `primary_key`, `proceeds` and the refusal wording returns no match).
- `PRIMARY_KEYS|primary_key.*lot_id|lot_id.*quantity.*proceeds`: 40 hits, 2 DEF (the producer and the round-41 check), the rest records
  and the two contracts. The only two typed copies of the realized key are the producer and the contract, both changed in this commit.

## The effect (measured on the pandas 2.2.3 kit, full lots stage, default batch)

- 2026-10-08: refusals 0 (was LOTS_SKIPPED); 35,834 realized rows, 0 repeats under the new key and 8 under the old; all 8 pairs kept whole
  row each, nothing collapsed.
- 2026-10-07: refusals 0; 3,245 realized rows, 0 repeats.
- Peak and wall for both days are in `LOTS_KEY_R41.json`, under the 1,740.8 MB and 765 s bounds.
- Producer tests: one new test (`test_a_repeat_pair_with_the_same_id_quantity_and_proceeds_but_other_gain_is_kept_whole_row_each`) and one
  changed test (the true-duplicate-key refusal now differs in `acquired_date`, since gain is a key column).
