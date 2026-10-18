# AMGT-ca-2 receipt -- a figure whose source is absent, blank or `?` prints `source not stated`

Worker `0.9.0_WK_AMGT_RESAPP~521`, round 120, order `AMGT_RESAPP.TO-AMGT-ca-2.a-blank-or-question-mark-source-reads-source-not-stated`.
Base (unedited head): `62d2e724a3`, worktree `C:/dev/wk-resapp-521`, branch `wk-AMGT_RESAPP-521`. Product edit is LOCAL; no push, no deploy.

## What changed

- `lib/research/print/render_pack.py` +32 -8. New helpers `SOURCE_NOT_STATED`, `_source_absent`, `_stated_source_copy` (before `_plain_figure_line`). `_plain_figure_line` reads the figure through `_stated_source_copy` and takes its `served_source` from that copy. `_source_words` returns `source not stated` for any absent, blank or `?` source. `_figures_table` and `_forecast_table` hand `render_figure_line` the stated copy. Nothing else changed: `_plain_reason`, `_ceo_profile_sentence`, the export's management and thesis-pillars sections, and `render_print.py` are untouched.
- `lib/research/print/tests/test_ca2_source_not_stated.py` new, 289 lines, 59 cases (S1 4, S2 28, S3 2, S4 8, S5 9, S6 8).
- `lib/research/print/tests/fixtures/ca2_appendix_base_<NAME>.txt` new, eight files (RIO_LN 26, ICT_PM 26, GOOGL_US 27, ICICIBC_IN 26, HD_US 27, BA_US 26, KMB_US 27, TSM_US 25 lines), recorded from the unedited renderer's PDF at `62d2e724a3`. The `bz_served_thesis_<NAME>.json` fixtures were already in `tests/fixtures/` and are byte-identical (sha256) to `round119_prep/fixtures/`, so no copy was made.
- `lib/research/print/tests/test_bz3_appendix_plain_and_verdict.py` +15 -1: one assertion re-scoped (see Tests re-scoped).
- `lib/research/print/tests/test_by2_rich_export_rules.py` +9 -1: one assertion re-scoped (see Tests re-scoped).
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: three rows appended, `AMGT_RESAPP-D1-W521-S1` to `S3`, each with `disarm_owner` `2.0.0_SA_COO~R1`. No existing row edited.
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~521/` this receipt and the proof instance.

Rule: a source that is absent (no key, `None`, empty), whitespace only, or `?` prints as `source not stated`. Judgement: a padded `?` (for example `" ? "`) is treated as `?`, because the printed line would show the same bare question mark.

## Census

Denominator: 7 print sites x 6 source values = 42 cells, measured by running each site's own figure through `build_pack` and `build_rich_text` on the RIO LN fixture (`census_base` and `census_after` in the worker's scratch). Result: 25 cells changed, 17 unchanged (14 Bloomberg controls and 3 withheld Header cells that already read `source not stated`).

Where the bare `?` is made: `lib/research/provenance/render_print.py:221` `source = figure.get("source") or "?"` (read-only, not edited). Every site below reads a figure through `render_figure_line`, so the rule is applied in the pack's wrapper around the call.

| # | Print site (PDF Appendix or rich export) | Function, line (after edit) | absent | `""` | `"   "` | `"?"` | `Bloomberg` / `bloomberg-dapi` |
|---|---|---|---|---|---|---|---|
| 1 | PDF Header, withheld money line (CUR_MKT_CAP) | `_header_print_lines` 711 -> `_withheld_line` 706 -> `_source_words` 695 | `source not stated` (before and after) | same | same | `- ?` -> `- source not stated` | `- Bloomberg` (unchanged) |
| 2 | PDF Header listing (PX_LAST) | `_header_print_lines` 711 -> `_plain_figure_line` 609 (`served_source` 622) | `- ?` -> `- source not stated` | `- ?` -> words | `- The source is on file but is not stated in plain words.` -> words | `- ?` -> words | unchanged |
| 3 | PDF Fiscal year 2026 listing (IS_EPS) | loop at 1366 -> `_plain_figure_line` 609 | `- ?` -> words | `- ?` -> words | fixed sentence -> words | `- ?` -> words | unchanged |
| 4 | PDF Company description (CIE_DES_BULK) | 1331 -> `_description_line` 746 -> `_plain_figure_line` 609 | `company with RIO AU. - ?` -> words | same | fixed sentence -> words | `- ?` -> words | unchanged |
| 5 | Rich export, Header table (PX_LAST) | `_figures_table` 1612 (render 1627-1628) | `· ?` -> `· source not stated |` | `· ?` -> words | `·     |` (whitespace) -> words | unchanged |
| 6 | Rich export, Fiscal year 2026 table (IS_EPS) | `_figures_table` 1612, via `build_rich_text` fiscal rows | `· ?` -> words | `· ?` -> words | whitespace -> words | `· ?` -> words | unchanged |
| 7 | Rich export, forecast table (BEST_EPS on the IS_EPS row, 2026E) | `_forecast_table` 2161 (render 2170) | `· ?` -> words | `· ?` -> words | whitespace -> words | `· ?` -> words | unchanged |

Not a source print site: `_withheld_row_text` (no source), `_export_money_cell` (the amount only), `_header_description_lines` (no figure source).

The four named figures, printed line before and after (base fixtures `bz3_appendix_base_<NAME>.txt` and the rich export of ICICIBC IN):

| Figure | Before | After |
|---|---|---|
| RIO LN SHORT_INT_RATIO | `Short interest ratio (days to cover): not reported - ?` | `Short interest ratio (days to cover): not reported - source not stated` |
| ICT PM SHORT_INT_RATIO | `Short interest ratio (days to cover): not reported - ?` | `Short interest ratio (days to cover): not reported - source not stated` |
| ICICIBC IN CURR_ENTP_VAL | `Enterprise value: not reported - ?`; rich row `... · as of October 17th, 2026 · ? \|` | `Enterprise value: not reported - source not stated`; rich row `... · source not stated \|` |
| ICICIBC IN SHORT_INT_RATIO | `Short interest ratio (days to cover): not reported - ?` | `Short interest ratio (days to cover): not reported - source not stated` |

Read of the three names' appendices after the edit (freshly rendered; the Header and Fiscal year text otherwise unchanged): RIO LN and ICT PM each end the Header with `Short interest ratio (days to cover): not reported - source not stated`; ICICIBC IN carries `Enterprise value: not reported - source not stated` and `Short interest ratio (days to cover): not reported - source not stated` before the closing no-date line.

## Tests re-scoped

Two existing assertions pinned the old `- ?` line for a figure with no served source. Each is re-scoped to a hand-written expectation; the base captures and fixtures themselves are untouched. The rest of each assertion is unchanged.

1. `lib/research/print/tests/test_bz3_appendix_plain_and_verdict.py::test_W2_control_appendix_block_of_the_eight_names_equals_the_base_capture` (RIO_LN, ICT_PM and ICICIBC_IN failed after the edit; GOOGL_US, HD_US, BA_US, KMB_US and TSM_US pass unchanged).
   - Old: `assert "\n".join(_appendix(lines)) == base.rstrip("\n"), name`
   - New: `expected = [CA2_BASE_TO_NOW.get(name, {}).get(ln, ln) for ln in base.rstrip("\n").split("\n")]` then `assert _appendix(lines) == expected, name`, where `CA2_BASE_TO_NOW` maps the base line `Short interest ratio (days to cover): not reported - ?` to `... - source not stated` for RIO_LN and ICT_PM, and `Enterprise value: not reported - ?` and the same short-interest line to the words for ICICIBC_IN.
2. `lib/research/print/tests/test_by2_rich_export_rules.py::test_R6_control_the_pack_pdf_figure_lines_are_byte_identical_to_the_base` (RIO_LN and ICT_PM failed after the edit; GOOGL_US passes unchanged).
   - Old: `assert now == base, name`
   - New: `assert now == [CA2_BASE_TO_NOW.get(ln, ln) for ln in base], name`, where `CA2_BASE_TO_NOW` maps `Short interest ratio (days to cover): not reported - ?` to `... - source not stated`.

Both re-scopes are named here so the issuer can re-run the whole print and api folders in the full tree after the merge.

## Dry run and runs

- Base dry run (unedited head `62d2e724a3`, the new file): `40 failed, 19 passed`. Failed: S1 4 of 4; S2 28 of 28; S4 3 of 8 (RIO_LN, ICT_PM, ICICIBC_IN); S5 2 of 9 (the ICICIBC_IN case of the name test, and the separate row test); S6 3 of 8 (RIO_LN, ICT_PM, ICICIBC_IN). Passed: S3 2 of 2 (controls: the PDF line `- Bloomberg`, the rich cell `bloomberg-dapi` verbatim as served); S4 5 of 8 (GOOGL_US, HD_US, BA_US, KMB_US, TSM_US); S5 7 of 8 and S6 5 of 8 (the names with no bare `?`). Note on S2: the three withheld cases (absent, empty, blank) already printed `source not stated` on their own line at base and fail only on the whole-pack bare-`?` check, because RIO LN's SHORT_INT_RATIO line still reads `- ?` there. The first base run read `41 failed, 18 passed`, before one control expectation (S3, rich export) was corrected to the verbatim served source; the second run is the one recorded here.
- After the edit: `lib/research/print/tests/test_ca2_source_not_stated.py` `59 passed`.
- Print folder, after the edit (the AC2 invocation): `1 failed, 375 passed`, with exactly one FAILED line, the known `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`. The base count stated in the order (`1 failed, 316 passed`) was not re-run in this sparse tree; 316 + 59 new cases = 375 is consistent.
- api subset that imports the renderer (7 files: `test_print_fiscal_year_sort`, `test_print_format_rich`, `test_model_words`, `test_header_date_once`, `test_bw4_print_pack_degrades`, `test_by2_rich_route_degrades`, `test_bz2_rich_route_management_input`): `50 passed`.
- `.tools/commit-gate.sh` on the four `.py` files: `pre-commit gate clean for 4 of 4 file(s)`.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-ca-5` deploys; nothing here is served. No deploy, store, schedule, AWS, vendor or network call was made.
- The whole `lib/research/api` folder is not run in this sparse worktree; the 7 renderer-importing files above are the only api tests run. The issuer runs the print and api folders in the full tree after the merge.
- The 101-name source census (the ruling's grade) is the issuer's read at the drain (`ca-4`, the live pool). This receipt covers the eight fixture names only.
- `_forecast_table` is outside the region the order names (`_figures_table` and its helpers). It is inside the census (row 7) and its one render call is edited; surprise row `AMGT_RESAPP-D1-W521-S3` asks the CTO to rule the region.
- Visual layout is read from the PyMuPDF text layer, not from a rendered image.
