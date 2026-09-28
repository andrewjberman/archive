# IB-yr-1 session log -- 0.9.0_WK_IRPT_BCKEND~63

Task order: `IRPT_BCKEND.TO-IB-yr-1.saved-type-refuses-before-generation.md`, issued by `2.0.0_SA_COO~Y`, issuance `ecbb08548f`.

## Build

1. `recipe.step_read_back` (`infra/aws/lambda/investor-reporting/ycharts/generate/recipe.py`): the return dict now
   carries `saved_portfolio_type`, set to `effective.get("model_portfolio_type")` when `source == "saved_portfolio"`,
   else `None`. No other comparison-row logic touched.
2. `ResidentAssembly.run` (`infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py`): the semantic
   read-back checkpoint filter now also keeps `saved_portfolio_type`. Immediately after the checkpoint write and
   before `step_validate`/generation, a new gate raises `WorkerAttention("TOLERANCE_REQUIRES_STATIC")` when any
   read-back row is `tolerated` AND `saved_portfolio_type` is present AND is not `"fixed"`. `tolerance_requires_static`
   (the post-download printed-Type check) is untouched and still runs second, for the `fixed`/absent arms.
3. No test file edited (optional step skipped; the read-only R19_CHECKS harness already exercises all three arms).

## Runs

- `Y19-1-AC1` (`-k not_fixed`): `1 passed, 2 deselected in 2.21s`, rc 0.
- `Y19-1-AC2` (`-k fixed_or_absent`): `2 passed, 1 deselected in 4.68s`, rc 0.
- Full regression, `infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_resident_worker.py`:
  `39 passed, 8 skipped in 31.10s`, rc 0 -- no pre-existing test broken by the new gate.

## Premise check

Task-order line citations (`resident_worker.py` lines 259-271 for `tolerance_requires_static`, called at ~219-220;
`recipe.py` `step_read_back` lines 629-701) matched the world at HEAD `ecbb08548f` closely enough to act on directly;
no surprise row filed.
