# AMGT-bx-2 receipt -- 0.9.0_WK_AMGT_RESAPP~513, round 117

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-bx-2.the-pack-resolves-a-money-figures-currency-by-the-pages-rule-and-withholds-what-the-page-withholds.md`
Branch `wk-AMGT_RESAPP-513`, base (issuance) `51cbf82b4f`, code commit `0eb6290a5e` (LOCAL, not pushed).

## What changed

| path | change |
|---|---|
| `lib/research/print/render_pack.py` | +56 / -3 lines: the bx-2 rule in the header-line printer and its helpers (`CURRENCY_UNCONFIRMED_WORDS`, `_is_money_unit`, `_currency_unmeasured`, `_withheld`, `_source_words`, `_withheld_line`), and `_header_print_lines` |
| `lib/research/print/tests/test_bx2_currency_page_rule.py` | new, 231 lines: K1 to K7 |
| `lib/research/print/tests/fixtures/bx_served_thesis_RIO_LN.json` | new, copy of the served fixture, 1436 lines |
| `lib/research/print/tests/fixtures/bx_served_thesis_ICT_PM.json` | new, copy of the served fixture, 1755 lines |
| `lib/research/print/tests/fixtures/bx_served_thesis_GOOGL_US.json` | new, copy of the served fixture, 1889 lines |
| `lib/research/print/tests/fixtures/bx2_page_rule_table.json` | new, the census table (284 lines; 18 rows) |
| `lib/research/print/tests/fixtures/bx2_base_fiscal_lines.json` | new, the base Fiscal year recording for K6 (27 lines) |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | two rows appended: `AMGT_RESAPP-D1-W513-S1`, `AMGT_RESAPP-D1-W513-S2` |
| this receipt and the proof instance | committed with the surprise rows, after the code commit |

Not touched: the Summary, Positioning and Management builders; `build_pack`'s section order; `render_print.py`; `scoped_amgt.py`; `long_day.py`; `portal/` (nested checkout shows modified and is not staged); `org/devices/`.

The rule, in one line: a header money figure whose served `currency_basis` begins UNMEASURED prints `<label>: Bloomberg does not confirm this figure's currency - <source>` (the page's words); a measured figure keeps `_money`'s own-code rule; the same-value dedup compares the printed amounts as before. Fiscal Year lines do not read the rule.

## Census

Denominator: 18 money-unit header figures (6 per name; unit PRICE, PER SHARE, MILLIONS other than a share count, or ABSOLUTE full currency units). Source: the three served fixtures of 2026-10-18. "Page prints" is the page's rule applied by hand (`StatTile.tsx` formatStatValue and isUnmeasuredBasis; `HeaderCards.tsx` withheldReason). "Pack base" is the base renderer's line (census run at `51cbf82b4f`). "Pack after" is the required line, and it is what the test file checks.

| name | mnemonic | served currency | served currency_basis | class | page prints | pack base (51cbf82b4f) | pack after (0eb6290a5e) | status |
|---|---|---|---|---|---|---|---|---|
| RIO LN | PX_LAST | GBp | quote (CRNCY) | MEASURED_CODED | GBp 6,816.00 | Share price (last close): GBp 6,816.00 per share - Bloomberg | same | printed |
| RIO LN | CUR_MKT_CAP | none | UNMEASURED: PX_LAST x EQY_SH_OUT_REAL ... | WITHHELD | withheld (dash; reason on hover) | Market cap: 115,578.9 million currency not stated - Bloomberg | Market cap: Bloomberg does not confirm this figure's currency - Bloomberg | printed |
| RIO LN | NET_DEBT | none | UNMEASURED: the market-cap currency is not established ... | WITHHELD | withheld | Net debt: 14,512.0 million currency not stated - Bloomberg | Net debt: Bloomberg does not confirm this figure's currency - Bloomberg | printed |
| RIO LN | CURR_ENTP_VAL | none | UNMEASURED: the market-cap currency is not established ... | WITHHELD | withheld | Enterprise value: 173,616.0 million currency not stated - Bloomberg | Enterprise value: Bloomberg does not confirm this figure's currency - Bloomberg | printed |
| RIO LN | AVG_DAILY_VALUE_TRADED_3M | GBp | quote (CRNCY) | MEASURED_CODED | GBp 10.98B (not on key row) | Average daily value traded (three months): GBp 10,983.0 million - Bloomberg | same | printed |
| RIO LN | CRNCY_ADJ_MKT_CAP | none | UNMEASURED: PX_LAST x EQY_SH_OUT_REAL ... | WITHHELD | withheld (not on key row) | none (same-value dedup drops it against CUR_MKT_CAP) | none (dedup drops it: both withheld, same printed amount) | dedup_dropped |
| ICT PM | PX_LAST | PHP | quote (CRNCY) | MEASURED_CODED | PHP 860.00 | Share price (last close): PHP 860.00 per share - Bloomberg | same | printed |
| ICT PM | CUR_MKT_CAP | PHP | quote (CRNCY) | MEASURED_CODED | PHP 1.74T | Market cap: PHP 1,735,465.1 million - Bloomberg | same | printed |
| ICT PM | NET_DEBT | none | UNMEASURED: the identity read does not separate ... | WITHHELD | withheld | Net debt: 3,648.9 million currency not stated - Bloomberg | Net debt: Bloomberg does not confirm this figure's currency - Bloomberg | printed |
| ICT PM | CURR_ENTP_VAL | USD | reporting (EQY_FUND_CRNCY) | MEASURED_CODED | USD 33.09B | Enterprise value: USD 33,087.5 million - Bloomberg | same | printed |
| ICT PM | AVG_DAILY_VALUE_TRADED_3M | PHP | quote (CRNCY) | MEASURED_CODED | PHP 1.41B (not on key row) | Average daily value traded (three months): PHP 1,409.1 million - Bloomberg | same | printed |
| ICT PM | CRNCY_ADJ_MKT_CAP | PHP | quote (CRNCY) | MEASURED_CODED | PHP 1.74T (not on key row) | none (same-value dedup) | none (same-value dedup) | dedup_dropped |
| GOOGL US | PX_LAST | USD | quote (CRNCY) | MEASURED_CODED | $340.59 | Share price (last close): USD 340.59 per share - Bloomberg | same | printed |
| GOOGL US | CUR_MKT_CAP | USD | reporting (EQY_FUND_CRNCY) | MEASURED_CODED | $4.14T | Market cap: USD 4,143,539.9 million - Bloomberg | same | printed |
| GOOGL US | NET_DEBT | USD | reporting (EQY_FUND_CRNCY) | MEASURED_CODED | -$63.90B | Net debt: USD -63,902.0 million - Bloomberg | same | printed |
| GOOGL US | CURR_ENTP_VAL | USD | reporting (EQY_FUND_CRNCY) | MEASURED_CODED | $4.04T | Enterprise value: USD 4,037,738.9 million - Bloomberg | same | printed |
| GOOGL US | AVG_DAILY_VALUE_TRADED_3M | USD | quote (CRNCY) | MEASURED_CODED | $9.33B (not on key row) | Average daily value traded (three months): USD 9,330.7 million - Bloomberg | same | printed |
| GOOGL US | CRNCY_ADJ_MKT_CAP | USD | reporting (EQY_FUND_CRNCY) | MEASURED_CODED | $4.14T (not on key row) | none (same-value dedup) | none (same-value dedup) | dedup_dropped |

Counts: 18 figures = 4 printed withheld (RIO LN Market cap, Net debt, Enterprise value; ICT PM Net debt) + 3 dedup-dropped (the CRNCY_ADJ_MKT_CAP alias of RIO LN, ICT PM and GOOGL US, each carrying the same printed amount as CUR_MKT_CAP) + 11 measured lines printed unchanged. The full census with the served basis strings is `lib/research/print/tests/fixtures/bx2_page_rule_table.json`, and K7 checks its denominator, its class column and each printed line against it.

## Test run at the base (dry run, unedited head `51cbf82b4f`)

`python -m pytest lib/research/print/tests/test_bx2_currency_page_rule.py -q -p no:cacheprovider --color=no -rfE`:
`5 failed, 7 passed in 11.36s`. Failed: K1, K2, K5, K7 for RIO LN, K7 for ICT PM. Passed: K3, K4, K6 (x3), K7 coverage, K7 GOOGL US.

## Test run after the edit

AC1, exact invocation, twice: `12 passed in 10.70s` / `exit=0` (and `12 passed in 9.63s` on the first run). Names present: K1, K2, K3, K4, K5, K6 (x3, one per name), K7 (coverage; agreement x3).

AC2, the print folder: `1 failed, 158 passed, 4 warnings in 52.12s`. The one FAILED line is `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`, which fails at the base as well. The base reads `1 failed, 146 passed`; the 12 new tests account for the difference.

## Tests re-scoped

none. No existing test file was edited. `test_bw1_currency_labels.py` and `test_bw2_pack_form.py` pass unchanged because their fixtures carry no `currency_basis` field, so the withholding rule does not reach them.

## Commit-gate and reflex notes

`bash .tools/commit-gate.sh` passed on both edited `.py` files. The pre-commit risk reflex printed a HOLD on `render_pack.py` citing the closed deploy record `org/critical_paths/change_management/20260926T0935Z_amgt-rs-2-the-redeploy_deploy_completion.md` (closure diff discipline for a redeploy). That record is historical; this order performs no deploy. The redeploy `AMGT-bx-5` must re-run the closure diff against the built artifact.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-bx-5`. Nothing here is live; no AWS, store, HTTP or vendor call was made.
- The whole api folder is not run in this sparse worktree; the issuer runs it in the full tree.
- The rich-text document (`pack_<sec>.md`) still prints raw served amounts for withheld figures (surprise row `AMGT_RESAPP-D1-W513-S1`); `_figures_table` is outside the owned region and was not changed.
- The reporting-currency sentence in the order (surprise row `AMGT_RESAPP-D1-W513-S2`) is recorded, not acted on.
- The `<status>` flip is the issuer's, not made here.
