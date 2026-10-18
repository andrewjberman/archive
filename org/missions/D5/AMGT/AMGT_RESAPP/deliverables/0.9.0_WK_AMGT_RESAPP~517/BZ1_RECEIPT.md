# AMGT-bz-1 receipt -- 0.9.0_WK_AMGT_RESAPP~517 (round 119, decomposition s.128, row AMGT_RESAPP-D1-W517-S1 and -S2)

Order: `AMGT_RESAPP.TO-AMGT-bz-1.the-rich-exports-money-rows-carry-the-pages-currency-code.md` (issued by 2.0.0_SA_COO~R1).
Branch `wk-AMGT_RESAPP-517`, base (unedited head) `8e81e269f7`, product commit `b175e8965a` (LOCAL).

## What changed

| Path | Change |
|---|---|
| `lib/research/print/render_pack.py` | +27 / -3. New `_export_money_cell` (AMGT-bz-1, placed before `_figures_table`); `_figures_table` wraps `render_figure_line` in it; `_forecast_table` wraps its call the same way. No pack builder, no figure-line function, no `render_print.py` edit. |
| `lib/research/print/tests/test_bz1_rich_money_codes.py` | new, 227 lines, Z1 to Z7, hand-written expectations. |
| `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py` | +13 / -1, Q3 re-scoped (see Tests re-scoped). |
| `lib/research/print/tests/test_by2_rich_export_rules.py` | +11 / -6, R2 and R3 re-scoped (see Tests re-scoped). |
| `lib/research/print/tests/fixtures/bz_served_thesis_<NAME>.json` | new, 8 files (RIO_LN, ICT_PM, GOOGL_US, ICICIBC_IN, HD_US, BA_US, KMB_US, TSM_US), copied byte-identical from round119_prep (2026-10-18, CodeSha256 H3dCSGL..). Line counts 1436, 1755, 1889, 1685, 2679, 2887, 2940, 1904. |
| `lib/research/print/tests/fixtures/bz1_base_export_<NAME>.md` | new, 3 files (RIO_LN 56, ICT_PM 69, GOOGL_US 53 lines): the rich export of each name at the unedited head. Z5 control. |
| `lib/research/print/tests/fixtures/bz1_base_pack_text_<NAME>.txt` | new, 3 files (RIO_LN 46, ICT_PM 47, GOOGL_US 48 lines): the pack text at the unedited head. Z6 control. |
| `lib/research/print/tests/fixtures/bz1_rich_money_table.json` | new, 59 lines: the Step A census (below), with its denominator. |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | +52 lines, two rows appended (AMGT_RESAPP-D1-W517-S1, -S2); no existing row edited. |
| `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~517/` | this receipt and the proof instance. |

The rule as built: for each money-unit figure the export prints (Header table, fiscal-year table, forecast table):
(1) `currency_basis` begins UNMEASURED: unchanged (withheld in the Header as before; the fiscal and forecast tables keep their amount and print no code);
(2) measured, own served `currency`: the code is printed before the amount, through `_own_currency` (called, not copied);
(3) measured, no own currency: `<amount> <unit text> currency not stated`;
(4) every other row: unchanged. A cell that prints no amount (a checkface REFUSE marker) is unchanged; a PROVISIONAL marker leads the amount, so the code goes between the marker and the amount.

## Census

Denominator: the 8 served bodies, 30 money-unit header figures (PAGE_HEADER_MNEMONICS money-unit rows PX_LAST, CUR_MKT_CAP, NET_DEBT, CURR_ENTP_VAL). 25 measured: each gains its own served code. 5 withheld (UNMEASURED): unchanged. Not counted: TSM_US CURR_ENTP_VAL (unit UNRESOLVED, not a money unit: unchanged); ICICIBC_IN CURR_ENTP_VAL (absent from its served body). Fiscal-year and forecast money rows: 0 in the eight bodies (no `fiscal_year_figures`, no `forecast_figures`).

"Today" is the Rendered cell as the unedited head printed it; "must" is hand-written from the rule.

| Name | Mnemonic | served currency (basis) | today | must |
|---|---|---|---|---|
| RIO_LN | PX_LAST | GBp (quote) | `6816.0 PRICE ...` | `GBp 6816.0 PRICE ...` |
| RIO_LN | CUR_MKT_CAP | none (UNMEASURED) | `Market cap: Bloomberg does not confirm this figure's currency` | unchanged |
| RIO_LN | NET_DEBT | none (UNMEASURED) | `Net debt: ...does not confirm...` | unchanged |
| RIO_LN | CURR_ENTP_VAL | none (UNMEASURED) | `Enterprise value: ...does not confirm...` | unchanged |
| ICT_PM | PX_LAST | PHP (quote) | `860.0 PRICE ...` | `PHP 860.0 PRICE ...` |
| ICT_PM | CUR_MKT_CAP | PHP (quote) | `1735465117699.9998 ABSOLUTE ...` | `PHP 1735465117699.9998 ABSOLUTE ...` |
| ICT_PM | NET_DEBT | none (UNMEASURED) | `Net debt: ...does not confirm...` | unchanged |
| ICT_PM | CURR_ENTP_VAL | USD (reporting) | `33087.51831274085 MILLIONS ...` | `USD 33087.51831274085 MILLIONS ...` |
| GOOGL_US | PX_LAST | USD (quote) | `340.59 PRICE ...` | `USD 340.59 PRICE ...` |
| GOOGL_US | CUR_MKT_CAP | USD (reporting) | `4143539940000.0005 ABSOLUTE ...` | `USD 4143539940000.0005 ABSOLUTE ...` |
| GOOGL_US | NET_DEBT | USD (reporting) | `-63902.0 MILLIONS ...` | `USD -63902.0 MILLIONS ...` |
| GOOGL_US | CURR_ENTP_VAL | USD (reporting) | `4037738.9400000004 MILLIONS ...` | `USD 4037738.9400000004 MILLIONS ...` |
| ICICIBC_IN | PX_LAST | INR (quote) | `1397.0 PRICE ...` | `INR 1397.0 PRICE ...` |
| ICICIBC_IN | CUR_MKT_CAP | INR (reporting) | `10030308914450.0 ABSOLUTE ...` | `INR 10030308914450.0 ABSOLUTE ...` |
| ICICIBC_IN | NET_DEBT | INR (reporting) | `-347490.182 MILLIONS ...` | `INR -347490.182 MILLIONS ...` |
| HD_US | PX_LAST | USD (quote) | `309.63 PRICE ...` | `USD 309.63 PRICE ...` |
| HD_US | CUR_MKT_CAP | USD (reporting) | `308914638898.38 ABSOLUTE ...` | `USD 308914638898.38 ABSOLUTE ...` |
| HD_US | NET_DEBT | USD (reporting) | `64249.0 MILLIONS ...` | `USD 64249.0 MILLIONS ...` |
| HD_US | CURR_ENTP_VAL | USD (reporting) | `369699.63889838 MILLIONS ...` | `USD 369699.63889838 MILLIONS ...` |
| BA_US | PX_LAST | USD (quote) | `190.21 PRICE ...` | `USD 190.21 PRICE ...` |
| BA_US | CUR_MKT_CAP | USD (reporting) | `150336281504.2 ABSOLUTE ...` | `USD 150336281504.2 ABSOLUTE ...` |
| BA_US | NET_DEBT | USD (reporting) | `26965.0 MILLIONS ...` | `USD 26965.0 MILLIONS ...` |
| BA_US | CURR_ENTP_VAL | USD (reporting) | `181979.28150420001 MILLIONS ...` | `USD 181979.28150420001 MILLIONS ...` |
| KMB_US | PX_LAST | USD (quote) | `105.57 PRICE ...` | `USD 105.57 PRICE ...` |
| KMB_US | CUR_MKT_CAP | USD (reporting) | `35110369041.659996 ABSOLUTE ...` | `USD 35110369041.659996 ABSOLUTE ...` |
| KMB_US | NET_DEBT | USD (reporting) | `6866.0 MILLIONS ...` | `USD 6866.0 MILLIONS ...` |
| KMB_US | CURR_ENTP_VAL | USD (reporting) | `40795.36904165999 MILLIONS ...` | `USD 40795.36904165999 MILLIONS ...` |
| TSM_US | PX_LAST | USD (quote) | `412.61 PRICE ...` | `USD 412.61 PRICE ...` |
| TSM_US | CUR_MKT_CAP | USD (quote) | `2139991042503.9302 ABSOLUTE ...` | `USD 2139991042503.9302 ABSOLUTE ...` |
| TSM_US | NET_DEBT | none (UNMEASURED) | `Net debt: ...does not confirm...` | unchanged |

Not printed by the export (surprise AMGT_RESAPP-D1-W517-S1): AVG_DAILY_VALUE_TRADED_3M (served GBp for RIO_LN) and CRNCY_ADJ_MKT_CAP. Neither is in PAGE_HEADER_MNEMONICS or SHEET_ROWS.

The RIO_LN block of the round-115 `bu3` fixture (not a served body) also carries fiscal IS_EPS and consensus IS_EPS money rows; they now print `GBp 6.4 PER SHARE (local)` and `GBp 6.9 PER SHARE (local)` (surprise AMGT_RESAPP-D1-W517-S2).

The three names' exports were read once after the edit (diff against the base captures): only the four money rows of each name changed, and only by the code prefix. The PDF pack text was not edited (Z6 control).

## Tests re-scoped

Three existing tests pinned the old money rows. Each is re-scoped by hand, the old and new assertions named.

1. `test_bv2_rich_dates_and_quotes.py::test_Q3_control_inverse_of_export_equals_base_export_recorded_at_base_head`. Old: `mapped == recorded`, with the recorded base lines compared as they are (the one Exec Management line re-scoped as before). New: three recorded base lines are mapped by hand to their coded form before the comparison, each mapping must match exactly one base line: `| PX_LAST | Share price (last close) | 6816.0 PRICE` becomes `... | GBp 6816.0 PRICE`; `| IS_EPS | Diluted earnings per share for the fiscal year. | 6.4 PER SHARE` becomes `... | GBp 6.4 PER SHARE`; `| IS_EPS | EPS (consensus estimate) | 6.9 PER SHARE` becomes `... | GBp 6.9 PER SHARE`. Every other line is still compared as before.
2. `test_by2_rich_export_rules.py::test_R2_ict_pm_net_debt_withheld_and_the_measured_market_cap_and_enterprise_value_keep_their_amounts`. Old: `market.startswith("1735465117699.9998 ABSOLUTE")`; `enterprise.startswith("33087.51831274085 MILLIONS")`; and the rule-(4) check that neither cell carries PHP or USD. New: `market.startswith("PHP 1735465117699.9998 ABSOLUTE (full currency units)")`; `enterprise.startswith("USD 33087.51831274085 MILLIONS")`; the rule-(4) check is removed, because the own code is now the expectation. The withheld-words check and the CRNCY check are unchanged.
3. `test_by2_rich_export_rules.py::test_R3_control_googl_us_money_rows_are_byte_identical_to_the_base`. Old: `now_rows[m] == base_rows[m]` for each money row. New: the first two cells of each money row are identical to the base, and the third cell equals `"USD " + <base third cell>`.

No other existing test changed. The full folder run after the change: `1 failed, 256 passed` (the one known failure).

## Test runs

Base (unedited head `8e81e269f7`, new test file run once before the product edit): `5 failed, 2 passed in 2.92s`. Failing, as the new behaviour requires: Z1, Z2, Z3, Z4, Z7. Passing, as the controls require: Z5, Z6.

After the edit: `7 passed in 2.88s` (run several times; final run recorded in the instance).

Full folder, first after-edit run before the three re-scopes: `4 failed, 253 passed` (the known failure plus Q3, R2, R3). After the re-scopes and the final render_pack edit: `1 failed, 256 passed, 4 warnings in 100.54s`. The known failure is `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` (base reads `1 failed, 249 passed`; 249 + the seven new tests = 256).

Z-clause changed from the order text: Z1's AVG_DAILY_VALUE_TRADED_3M clause asserts that the export prints no row for that mnemonic (surprise AMGT_RESAPP-D1-W517-S1). Z6 compares the pack text before the appendix heading, not the appendix, because AMGT-bz-3 edits the appendix; this follows the round-116 lesson.

## Not verified

- The deployed Lambda serves the old renderer until AMGT-bx-5. Nothing here was deployed, no store was read, no AWS, vendor or network call was made.
- The whole api folder was not run: this worktree is sparse. The issuer runs the print and api folders in the full tree after the merge.
- The fiscal-year and forecast branches of `_export_money_cell` are exercised only by the synthetic Z4 cases and by the RIO bu3 Q3 fixture; no served body carries a fiscal or forecast money figure.
- A PROVISIONAL fiscal PX_LAST row (checkface marker) is covered only by the direct Z4 string case, not by a served figure.
- The `.tools/hooks` risk-reflex printed a HOLD on `render_pack.py` citing `org/critical_paths/change_management/20260926T0935Z_amgt-rs-2-the-redeploy_deploy_completion.md` (an L1 verify note for the amgt-rs-2 redeploy). The commit was not blocked. The deployed-build comparison belongs to AMGT-bx-5, not to this cell.
- The `bx_served_thesis_*` fixtures from round 117 were not re-copied; they are already in the folder and unchanged.
- The `portal` submodule shows as modified in the worktree; it was not staged or committed.
