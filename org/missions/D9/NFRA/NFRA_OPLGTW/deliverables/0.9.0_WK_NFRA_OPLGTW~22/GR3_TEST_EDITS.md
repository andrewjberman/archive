# GR3_TEST_EDITS -- existing Schwab test files edited by 0.9.0_WK_NFRA_OPLGTW~22 under OG-gr-3 AMENDMENT A1

Fixture-only edits for R9's grain. No test deleted, skipped or xfailed; no assertion weakened.

- `test_schwab_query.py` -- `write_positions()` gains the `quantity_cash_settled` column (decimal(15,5), 0 on every row, no PII): R9's dim_position grain reads it, and the writer lacked it, so 22 tests here and 13+3 in `test_schwab_export.py` / `test_schwab_export_stream.py` (which import this writer) failed with an engine column error.
- `test_schwab_semantics.py` -- `write_positions()` gains `quantity_cash_settled` (same reason), `write_assets()` gains `security_description_line_1` (R9's dim_asset grain column; a synthetic "D"+cusip text), and the three row sets of `test_ogq3_ac09` gain `quantity_settled_unsettled` + `quantity_cash_settled` (the keys `assert_unique_grain` now indexes), with the duplicate/conflicting rows still equal on all five grain columns, so both refusals are still asserted unchanged.
- `test_schwab_transactions.py` -- `test_mx_s15_grain_declared` restates its control assertion `DATASET_GRAINS["dim_asset"] == ("cusip",)` to R9's `("cusip", "security_description_line_1")`.

NOT edited, still red, and not fixable by a fixture edit: `test_schwab_query.py::test_ogq2_ac20` (row NFRA_OPLGTW-Z-W22-S4).
