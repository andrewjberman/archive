# OG-gr-2 (round 15) -- why dim_position 2026-09-21 collides under the candidate grain

READ-ONLY (Andrew-direct 2026-10-03 ~17:3xZ). `writes: 0`. Record: `GRAIN_R15.json`. Scripts beside it as `*.py.txt`.

**Verdict: GRAIN_FOUND.** `[account_id, cusip, l_s, quantity_settled_unsettled, quantity_cash_settled]` is unique on 52 of 52
qualified snapshots (26 dim_position, 26 dim_asset with the unchanged OG-v-6 grain), the added column blank on 0 rows. The same
holds on the 4 snapshots of 2026-10-02 (now qualified, held outside the 52; surprise row W22-S2).

## 1. The collision, per master (counts and flags only)

At each master (08242234, 08335338) on 2026-09-21 the candidate has one colliding group of 2 rows; it is the same declared key at both masters.

- Key columns (account_id, cusip, l_s, quantity_settled_unsettled): equal in both rows, none blank.
- Columns that DIFFER between the two rows: `accounting_rule_code` (CASH vs MARGIN), `quantity_cash_settled` (1 vs 0),
  `quantity_margin_settled` (0 vs 1). The other 27 columns are equal, including `_source_file` (one file for both rows).
  Per-column flags for all 30 columns: `GRAIN_R15.json` `collision_2026_09_21.masters.<master>.per_column_flag_all_columns`.
- Same key on neighbouring qualified dates (no 09-19/09-20: weekend; nearest qualified are 09-18 and 09-22):

| date | rows, declared key | state | rows, candidate key | rows' accounting_rule_code / quantity_settled_unsettled |
|---|---|---|---|---|
| 2026-09-17 | 1 | present | 1 | CASH / 1 |
| 2026-09-18 | 1 | present | 1 | CASH / 1 |
| 2026-09-21 | 2 | duplicated | 2 | CASH / 1 and MARGIN / 1 |
| 2026-09-22 | 1 | present | 0 (quantity is 2) | CASH / 2 |
| 2026-09-23 | 1 | present | 0 | (see json) |

Both masters read identically.

## 2. Decision: not an upstream defect

The 09-21 pair is a CASH portion (1) and a MARGIN portion (1) of one position; 09-22 carries one CASH row of 2 = 1 + 1. The rows are
not whole-row duplicates, come from one source file, and each has a self-consistent cash/margin split. Other declared keys already
carry CASH and MARGIN rows of differing quantity on every day printed. The candidate collides only because the two portions have
equal quantity. So UPSTREAM_DEFECT is false and no owner is named.

## 3. The grain, and the alternatives measured (28 dim_position snapshots incl. 2026-10-02)

- Added column `quantity_cash_settled`: unique 28 of 28, 0 blanks. `quantity_margin_settled`: the same (equal alternative, not chosen).
- `accounting_rule_code` (the semantic discriminator) is unique 28 of 28 but BLANK at 08335338 from 2026-09-21 (1 to 3 rows per
  snapshot, 10 of 28 snapshots; those rows have blank cusip, l_s, tax_code and zero quantities). It fails "never blank".
- The other 23 columns fail uniqueness on 26 of 28 snapshots.

## 4. Caveats for the CTO (not graded here)

A quantity is a mechanical, not semantic, key column (a MARGIN and a SHORT row of equal quantity both carry cash 0). Whether to key on
`accounting_rule_code` despite its blank rows, or accept the quantity column, is the CTO's call. Uniqueness on 52 (+4) snapshots does
not prove the next snapshot will not collide.
