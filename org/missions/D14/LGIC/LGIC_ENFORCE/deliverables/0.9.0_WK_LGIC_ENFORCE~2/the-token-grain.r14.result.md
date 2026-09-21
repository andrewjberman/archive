# LGIC_ENFORCE.TO-EN-p-38-r14 -- result

`0.9.0_WK_LGIC_ENFORCE~2`, round 14, cell `EN-p-38`. Worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-14-2`, branch
`wk-lgic-enforce-14-2`, created from `a2e031e4c7`.

**RE-GRADE (this section added 2026-09-19, worktree `.worktrees/wk-lgic-enforce-14-2b`, branch
`wk-lgic-enforce-14-2b`, from `dc11dc6a3a`):** at the first cut, `P38R14-AC2` FAILED because the
checker's vintage arm graded BOTH round-14 cells' records in one ANDed pass, so the sibling cell
`EN-r-7`'s absent record (worked in a separate, unmerged worktree) failed this cell's criterion even
though this cell's own half was clean. That diagnosis was correct and is filed as
`LGIC_ENFORCE-S106`; the order was right not to flip `complete` on it. The checker is now REPAIRED
(@`acdba45160`): the vintage arm grades the records PRESENT IN ITS CHECKOUT and refuses only a
genuinely empty population. Re-run against the same committed `TOKEN_GRAIN_R14.json` (`a87eb27fbf`,
unchanged) now reads `PASS-R14-VINTAGE-FIELD`. See "Criteria run" below for all three re-run
invocations and outputs.

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

## Criteria run (re-grade, this worktree, this commit)

- `P38R14-AC1` (`p38-grain`): **PASS-P38-GRAIN**, rc=0. `by-token sum 1449 vs rows 1303 (difference
  146)`, `rows carrying MORE THAN ONE token: 138`, `distribution: {'1': 1165, '2': 130, '3': 8}`,
  `input pinned at: c05f9f9fc9`. Unchanged from the first cut.
- `P38R14-AC2` (`r14-vintage-field`): **PASS-R14-VINTAGE-FIELD**, rc=0 (was FAIL at the first cut --
  see RE-GRADE note above). Output: `records present in THIS checkout: 1 ['EN-p-38'] (the arm grades
  these and only these -- S106)`; `EN-p-38: fixed inputs named at pin: 2 ['R14_BASE.json',
  'check_en_r14.py'], each commit resolvable: True`.
- `P38R14-AC3` (`r14-stale-proofs`): **PASS-R14-STALE-PROOFS**, rc=0. Re-run output: `EN-r-7: 2
  fixed-input commits since the cut (informational), 0 proofs at risk, 0 record enumerates` /
  `EN-p-38: 2 fixed-input commits since the cut (informational), 0 proofs at risk, 0 record
  enumerates`. Set equality holds; no refusal (the commit count rose from 1 to 2 across the S106
  repair, purely informational, 0 proofs at risk either time).
- `P38R14-AC4`: judgment, recorded for `3.0.0_SA_CVO` at L9, no verdict from this seat.

## Not claimed

- No re-opening of round 13; no touching `EN-r-7`'s question, record, or render field; no producer
  change; no re-measurement of the grain figures (AC1's figures stand from the first cut, input still
  pinned at `c05f9f9fc9`).
- This cell did not repair the checker -- that repair is `2.0.0_SA_COO~G`'s, filed and merged as
  `LGIC_ENFORCE-S106` @`acdba45160`, before this re-grade order issued.

## Surprises

None newly filed by this cell on the re-grade: `LGIC_ENFORCE-S106` (the checker defect this re-grade
answers) was filed and repaired by others before this order issued; the instrument self-test
(`selftest-arms`, 33 arms including 4 new WIRING arms) was re-run and read
`VERDICT: PASS-ARMS-DISCRIMINATE` before any criterion was re-run.
