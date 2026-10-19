# CG1 receipt -- `0.9.0_WK_AMGT_RESAPP~530` on `AMGT_RESAPP.TO-AMGT-cg-1`

Base: `4d3c666a3b` (the issuance commit). Branch `wk-AMGT_RESAPP-530`, worktree `C:/dev/wk-resapp-530`.
Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-cg-1.the-rich-export-prints-plain-words-for-every-remaining-reader-state-word.md`.
Census read first: `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round125_prep/READER_STATE_WORD_CENSUS.md`.

## What changed

Every path, with its line count (`git diff --numstat` against `4d3c666a3b`; a new file counts its lines):

- `lib/research/print/render_pack.py`: 24 insertions, 19 deletions (2491 to 2496 lines). Only the writers named in rule (a) and (b) changed; no PDF writer, no `scoped_amgt.py`, no Peers present column, no cf-2 line, no figure, table or citation line.
- `lib/research/print/tests/test_cg1_reader_state_words.py`: new, 280 lines, 24 test functions covering T1 to T12 (T1, T4 to T8 each hold several functions; each Tn is named in the module docstring).
- Existing tests re-scoped (old and new text in `## Tests re-scoped`): `test_posture_markdown.py` 8 lines, `test_cf2_not_available_words.py` 3 lines, `test_model_cases_markdown.py` 25 lines, `test_build_rich_text.py` 10 lines, `test_bv2_rich_dates_and_quotes.py` 13 added and 1 changed, `test_ca3_export_thesis_pillars.py` 13 added and 2 changed, `test_av2_export_equals_page.py` 5 lines, and `lib/research/api/tests/test_by2_rich_route_degrades.py` 2 lines.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 50 insertions (two rows, `AMGT_RESAPP-D1-W530-S1` and `AMGT_RESAPP-D1-W530-S2`).
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~530/`: this receipt, and the proof instance.

Writers changed in `render_pack.py` (base line, then the rule):

| kind | base line(s) | writer | new text |
|---|---|---|---|
| K5 | 1703, 1800 | `_drafted_section_markdown`, `_header_description_lines` | `Description: Not available -- <reason>` |
| K6 | 1887 | `_management_markdown` | `Exec Management: Not available (<words>).` |
| K9 | 1928 | `_peers_markdown(None)` | `Not available -- no peer set supplied to this export` |
| K1 | 2027, 2029 | `_posture_markdown` (non-SERVED) | `Posture: Not available -- <reason>` and `... Nothing is rendered in its place.` |
| K2 | 2037, 2041 | `_posture_markdown` (SERVED, verdict absent) | `Not available -- no call was made: <reason>` (and with the machine disclaimer) |
| K3 | 2130 | `_model_sheet_notes_markdown` | `y/y growth rows: Not available -- the block carries none and this page computes none.` |
| K4 | 2140 | `_model_sheet_notes_markdown` | `<years>: Not available -- the block carries fiscal years <a> to <b> only.` |
| K7 | 2096 (`_model_case_line`) | a non-SERVED case: `<head>: Not available -- <detail>`; a SERVED case: `<head>: <detail>` with no state word |
| K8 | 2173, 2430 | `_refused_figures_markdown`, `build_rich_text` (Model Notes) | `<MNEMONIC>: Not available -- <reason>` |

`NOT_AVAILABLE_WORDS` (`render_pack.py` 1609) is the constant used for every word above; `cf-2`'s lines are unchanged.

## Census

Native Grep of `ABSENT|REFUSED` on `lib/research/print/render_pack.py`, before (base `4d3c666a3b`, read from a scratch copy by `git show`) and after the edit:

- **Before: 61 lines** (63 occurrences). Printing writers among them: 1703, 1800, 1887, 1928, 2027, 2029, 2037, 2041, 2130, 2140, 2173, 2430 (K5, K6, K9, K1, K2, K3, K4, K8). K7 has no ABSENT literal on its print path at base: `_model_case_line` prints the `status` variable (2096), so the literal census does not count it. Line numbers of the base list: 590 847 864 1120 1122 1221 1231 1454 1584 1604 1605 1606 1607 1610 1611 1616 1646 1700 1703 1704 1739 1743 1795 1800 1801 1873 1876 1881 1886 1887 1888 1919 1928 1974 1993 1996 2004 2021 2027 2029 2037 2041 2072 2075 2103 2126 2130 2140 2150 2155 2156 2169 2173 2180 2226 2237 2275 2282 2332 2417 2430.
- **After: 48 lines** (50 occurrences). Line numbers: 590 847 864 1120 1122 1221 1231 1454 1584 1604 1605 1606 1607 1610 1611 1616 1646 1700 1704 1739 1743 1795 1801 1873 1876 1881 1886 1888 1919 1974 1993 1996 2004 2021 2073 2076 2108 2155 2160 2161 2174 2185 2231 2242 2280 2287 2337 2422.
- Classification of the 48 remaining lines: **printing writers: none.** A (sentence-constant or dict names, no state word in the text): 847, 1221, 1231, 1604-1607, 1610, 1611, 1704, 1801, 1886, 1888, 1974, 2021, 2174, 2242. B (comparisons, a default, a screen regex, a map key): 864 (the state-word screen regex), 1122 (comparison), 1616 (`"ABSENT": "absent"` in `_READ_STATUS_WORDS`, which prints the lowercase plain word `absent` for the Peers read suffix, not the state word), 1646 (`"[REFUSED:" in rendered`), 1873 (default `"ABSENT"` for an absent management status), 2076 (default and comparison, never printed). C (comments and docstrings): 590, 1120, 1454, 1584, 1700, 1739, 1743, 1795, 1876, 1881, 1919, 1993, 1996, 2004, 2073, 2108, 2155, 2160, 2161, 2185, 2231, 2280, 2287, 2337, 2422.
- `SERVED` in the file is unchanged in role: no printed state word.
- The PDF writers print no state word (census section 2); the PDF text of the fixture bundle is pinned by T12 (sha256 `b184e349d6f2aef64391840157bb7b099bed5bb7f24b7fd7e5074345ba2b845c`, measured at Step B on the unedited head) and passes unchanged.

## Tests re-scoped

Each line below changed only the pinned string. Old and new text, file and line (post-edit line numbers):

- `lib/research/print/tests/test_posture_markdown.py` 16, 19, 26, 28, 37, 40, 48, 50: `Posture: ABSENT -- ...` becomes `Posture: Not available -- ...`; `ABSENT -- no call was made: ...` becomes `Not available -- no call was made: ...` (both the header and tab forms).
- `lib/research/print/tests/test_cf2_not_available_words.py` 108, 110, 111 (T9 control): `Posture: ABSENT -- ` becomes `Posture: Not available -- `; `y/y growth rows: ABSENT -- ` becomes `y/y growth rows: Not available -- `; `ABSENT -- no peer set supplied to this export` becomes `Not available -- no peer set supplied to this export`. The test name still says "keep their words" (not changed; one assertion per pin).
- `lib/research/print/tests/test_model_cases_markdown.py` (25 lines, rewritten from the same content): `Base case: SERVED -- <v>` becomes `Base case: <v>` (lines 18, 23, 30, 31, 75, 97, 102, 110, 116, 124, 140); `Base case: ABSENT -- <r>` becomes `Base case: Not available -- <r>` (41, 53, 82); `Upside case: ABSENT -- <r>` becomes `Upside case: Not available -- <r>` (48, 54, 74, 81, 142); `Downside case: ABSENT -- <r>` becomes `Downside case: Not available -- <r>` (49, 76, 83); `Opal's historical-multiple reference: SERVED -- 537.70 (f)` becomes `... : 537.70 (f)` (149) and `...: ABSENT -- why` becomes `...: Not available -- why` (151); the label docstring at 146 states the new form.
- `lib/research/print/tests/test_build_rich_text.py`: 136 `IS_DIV_PER_SHR: REFUSED --` becomes `IS_DIV_PER_SHR: Not available --`; 190 `ABSENT --` becomes `Not available --`; 221 `Description: ABSENT -- no description is on file for this name yet` becomes `Description: Not available -- ...`; 269 `Description: ABSENT -- a revenue figure, not the business` becomes `Description: Not available -- ...`; 273 `Description: ABSENT -- no reason recorded` becomes `Description: Not available -- no reason recorded`; 277 `"Description: ABSENT"` becomes `"Description: Not available"`; 446 `Exec Management: ABSENT (the object on file names no officers).` becomes `Exec Management: Not available (...)`; 476 `ABSENT -- no call was made: ...` becomes `Not available -- no call was made: ...`; 490 `Posture: ABSENT -- no posture object has landed ...` becomes `Posture: Not available -- ...`; 567 `CURR_ENTP_VAL: REFUSED --` becomes `CURR_ENTP_VAL: Not available --` (negative assertion, same intent).
- `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py` (Q3, control): 169 `new_line` becomes `Exec Management: Not available (no management object is on file).` (old `Exec Management: ABSENT (no management object is on file).`); lines 177 to 187 add a hand-written `state_rescoped` mapping of three base lines to their new text (old `y/y growth rows: ABSENT -- ...` to `y/y growth rows: Not available -- ...`; old `2027E, 2028E: ABSENT -- the block carries fiscal years 2025 to 2026E only.` to `2027E, 2028E: Not available -- ...`; old `ABSENT -- no peer set supplied to this export` to `Not available -- no peer set supplied to this export`). The recorded fixture `fixtures/bv2_rich_text_base_RIO_LN.txt` is unchanged.
- `lib/research/print/tests/test_ca3_export_thesis_pillars.py` (P5, control): a new `CG1_BASE_TO_NOW_STATE` pair list (lines 133-136) and its application in the loop of `_base_to_now_source` (from line 142): the same two base-to-new pairs as above. The recorded fixtures `fixtures/ca3_base_export_{ICT_PM,GOOGL_US,ICICIBC_IN}.md` are unchanged.
- `lib/research/print/tests/test_av2_export_equals_page.py`: 140 `IS_EPS: REFUSED -- unit not measured` becomes `IS_EPS: Not available -- unit not measured`; 145 `"ABSENT -- the block carries fiscal years"` becomes `"Not available -- the block carries fiscal years"` (negative); 146 `y/y growth rows: ABSENT` becomes `y/y growth rows: Not available`; 148 `2028E: ABSENT -- the block carries fiscal years 2023 to 2027E only.` becomes `2028E: Not available -- ...`; 150 `2026E, 2027E, 2028E: ABSENT -- ...` becomes `2026E, 2027E, 2028E: Not available -- ...`.
- `lib/research/api/tests/test_by2_rich_route_degrades.py`: 31 `ABSENT_PEERS` value `ABSENT -- no peer set supplied to this export` becomes `Not available -- no peer set supplied to this export` (the constant name is unchanged); 203 `Description: ABSENT -- the description read did not complete` becomes `Description: Not available -- the description read did not complete`.

Pins not touched: `test_ba18_chart_line.py` (its ABSENT is a comment), `test_by2_rich_export_rules.py` (a comment), `test_bz1_rich_money_codes.py` (reads `bz1_base_export_*.md`; no assertion on a moved line; passes unchanged), `test_ce1_status_word_screen.py` (asserts the absence of the word; still true), the `ABSENT` status values in input fixtures and in api tests that are not render output.

## Runs

Base (the unedited head, new file present, before any writer or test re-scope): `python -m pytest lib/research/print/tests/test_cg1_reader_state_words.py`: **18 failed, 6 passed** of 24 test functions (the failing ones: T1, T2, T3, T4 x2, T5 x3, T6, T7 x4, T8 x3, T9, T11; passing: the controls T1-control, T4-control, T5-control, T6-control, T10, T12).

After the writer edit, before any re-scope: the cg-1 file **24 passed**; `lib/research/print/tests` **34 failed, 503 passed**. Of the 34, 33 were existing pins of moved lines (the list above) and one was the known `test_pdf_text_carries_no_field_code_and_names_every_line_in_words`.

After the re-scope (final): `lib/research/print/tests` **1 failed, 536 passed** (the one failure is the known PDF test, and it fails for its own PDF header-figure assertion, unchanged); `lib/research/api/tests` seven renderer files (`test_by2_rich_route_degrades`, `test_print_format_rich`, `test_print_fiscal_year_sort`, `test_model_words`, `test_header_date_once`, `test_bz2_rich_route_management_input`, `test_bw4_print_pack_degrades`): **50 passed**.

## Not verified

- The deployed Lambda serves the old words until `AMGT-cg-4`; this cell changes the repository only.
- The portal page and the page-versus-export harness (`exportCompare.harness.cjs`, `peersReadFailed.harness.cjs`) move in `AMGT-cg-2`; the portal is not in this sparse worktree and was not touched.
- The whole api folder was not run in this sparse worktree; the seven renderer files above were run. The issuer runs the full tree.
- The live export of the 101 names was not re-read; the claims are from the fixture bundles and the synthetic inputs of the tests.
- `_refused_figures_markdown` (render_pack.py 2152) has no production call site; it is re-worded and tested by direct call, and the export's K8 line is tested through `build_rich_text`. Row `AMGT_RESAPP-D1-W530-S1` files this.
- The committed base fixtures were not re-recorded; the two controls map the moved lines by hand (AMGT-cf-2 precedent). Row `AMGT_RESAPP-D1-W530-S2` files this.
