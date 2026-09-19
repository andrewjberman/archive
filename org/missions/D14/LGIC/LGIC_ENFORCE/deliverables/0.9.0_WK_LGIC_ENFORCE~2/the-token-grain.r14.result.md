# LGIC_ENFORCE.TO-EN-p-38-r14 -- result

`0.9.0_WK_LGIC_ENFORCE~2`, round 14, cell `EN-p-38`. Worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-14-2`, branch
`wk-lgic-enforce-14-2`, created from `a2e031e4c7`.

## What landed

`TOKEN_GRAIN_R14.json` (committed `a87eb27fbf`) reconciles S102's 1449-vs-1303 by naming the two
grains and MEASURING the multiplicity from the row-level artifact at its pin, never inferring it
from `sum - rows`.

- **Input pin:** `c05f9f9fc9`, read with `git show c05f9f9fc9:<path>` (never the working tree).
- **`by_token_sum`:** 1449 (recomputed by counting, per token, how many of the 3264 judged rows in
  `PLACEHOLDER_POPULATION_TABLE_R13.md`'s `canonical` column contain that literal token string; the
  per-token counts -- 1119/122/108/85/7/5/1/1/1 -- match `PLACEHOLDER_POPULATION_R13.json`'s own
  `tokens.by_token[].rows` exactly, at the same pin, from a DIFFERENT artifact -- corroboration, not
  repetition).
- **`rows_with_a_placeholder`:** 1303 (recomputed the same way: rows whose `canonical` column
  contains at least one of the 9 tokens; matches `population.rows_with_a_placeholder` at the pin).
- **`rows_carrying_more_than_one`:** 138, MEASURED from the row-level artifact -- per row, count how
  many of the 9 tokens are present in that row's `canonical` cell, then count rows where that count
  exceeds 1. NOT inferred from `sum - rows` (146): that naive figure over-states the multi-token row
  count because 8 of the 1303 rows carry THREE tokens, each over-contributing 2 to the sum instead
  of 1, so `sum - rows` (146) != `rows_carrying_more_than_one` (138) by exactly the 8 rows' second
  excess unit (146 - 138 = 8).
- **Distribution** (subtraction from the 1303-row denominator, not a forward list): 1165 rows carry
  exactly 1 token, 130 carry exactly 2, 8 carry exactly 3. `1165 + 130 + 8 = 1303`, closing the row
  denominator. `1165*1 + 130*2 + 8*3 = 1449`, closing the token-incidence sum.
- **Reconciliation sentence:** in `TOKEN_GRAIN_R14.json`'s `grain.reconciliation` field.
- **Vintage:** `fixed_inputs_at_pin` names `check_en_r14.py` and `R14_BASE.json`, both at
  `a2e031e4c772737c29e328420dae9f1a17c6d2df` (the L6 issuance commit that minted them), each
  resolved by `git cat-file -e <commit>:<path>`.

## Criteria run (this worktree, this commit)

- `P38R14-AC1` (`p38-grain`): **PASS-P38-GRAIN**, rc=0.
- `P38R14-AC2` (`r14-vintage-field`): **FAIL-R14-VINTAGE-FIELD**, rc=0. The checker grades BOTH
  round-14 cells in one arm. `EN-p-38`'s half is clean (`fixed inputs named at pin: 2 ['R14_BASE.json',
  'check_en_r14.py']`, `each commit resolvable: True`). `EN-r-7`'s half fails because
  `ONE_RENDER_PATH_R14.json` does not exist in this worktree -- `0.9.0_WK_LGIC_ENFORCE~1` works that
  cell in its OWN worktree/branch, unmerged here. The order's own "WIRING AT THE CUT" line names this:
  "`AC1` and `AC2` **FAIL** (no record exists yet)." This is the expected cross-cell state at the cut,
  not a defect in this cell's work, and not something this cell's grant permits fixing (`EN-r-7`'s
  question and its deliverables/~1/ tree are out of bounds).
- `P38R14-AC3` (`r14-stale-proofs`): **PASS-R14-STALE-PROOFS**, rc=0. 1 fixed-input commit since the
  cut for each cell (the mint itself), 0 proofs at risk, 0 named re-run, set equality holds.
- `P38R14-AC4`: judgment, recorded for `3.0.0_SA_CVO` at L9, no verdict from this seat.

## Not claimed

- AC2 does not pass in this worktree; it cannot, by construction, until `EN-r-7`'s record exists and
  the two cells' work is merged. This cell's own half of AC2 is clean.
- No re-opening of round 13; no touching `EN-r-7`'s question, record, or render field; no producer
  change.

## Surprises

None filed by this cell. No criterion was found unsatisfiable by a correct artifact: AC1's arm
explicitly admits `rows_carrying_more_than_one: 0` (proven in `selftest-arms`,
`POSITIVE-BAR-grain-zero-overlap-is-admissible`), and the honest measured answer here (138, non-zero)
satisfied it on the first try. AC2's FAIL is the order's own stated cut-time wiring, not a new finding.
