# AMGT-by-2 receipt -- the rich export follows the pack's rules in full

**Worker:** `0.9.0_WK_AMGT_RESAPP~515` (issued by `2.0.0_SA_COO~R1`, round 118, decomposition s.127).
**Branch:** `wk-AMGT_RESAPP-515` (LOCAL, never pushed). **Base:** `8c7b466432` (the shared head; contains `AMGT-by-1`'s
`c1b1c53bd7` and `9498d36eb5` and `_plain_reason`).
**Code commit:** `882c46d46c` (LOCAL on `wk-AMGT_RESAPP-515`).
**Task order:** [AMGT_RESAPP.TO-AMGT-by-2](../../task-orders/AMGT_RESAPP.TO-AMGT-by-2.the-rich-export-follows-the-packs-rules-plain-sentences-withheld-figures-guarded-readers.md).

## What changed

| Path | Lines (added / removed) | Note |
|---|---|---|
| `lib/research/print/render_pack.py` | 74 / 23 | rich region only: the rich helpers route every served reason through `_plain_reason`; `_figures_table(withhold=True)` on the Header table; the CEO reading, the absent cause and the read status print in words; `_withheld_row_text` |
| `lib/research/api/scoped_amgt.py` | 31 / 6 | the `fmt == "rich"` branch of `_print_pack` only: the four reads (thesis bundle, peer set, posture, description) each guarded, reported once through `_LOG.warning`. The PDF branch and every other function are unchanged |
| `lib/research/print/tests/test_by2_rich_export_rules.py` | 254 / 0 | new: R1 to R6 (17 test cases with R4 and R5 parametrised) |
| `lib/research/api/tests/test_by2_rich_route_degrades.py` | 205 / 0 | new: R7 to R13 (R11 parametrised, 3 cases) |
| `lib/research/print/tests/test_build_rich_text.py` | 15 / 4 | four assertions re-scoped (see `## Tests re-scoped`) |
| `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py` | 8 / 1 | Q3 re-scoped (see `## Tests re-scoped`) |
| `lib/research/print/tests/fixtures/by2_base_header_GOOGL_US.md` | 15 / 0 | R3 control: the GOOGL US Header section of the export at the unedited head `8c7b466432` |
| `lib/research/print/tests/fixtures/by2_base_pdf_figure_lines_RIO_LN.json` | 25 / 0 | R6 control: the pack PDF's figure lines at the unedited head |
| `lib/research/print/tests/fixtures/by2_base_pdf_figure_lines_ICT_PM.json` | 25 / 0 | R6 control, ICT PM |
| `lib/research/print/tests/fixtures/by2_base_pdf_figure_lines_GOOGL_US.json` | 26 / 0 | R6 control, GOOGL US |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | 101 / 0 | rows `AMGT_RESAPP-D1-W515-S3` to `-S6` appended (disarm_owner `2.0.0_SA_COO~R1` on each); no existing row edited |

The three served fixtures `bx_served_thesis_<NAME>.json` were already in `lib/research/print/tests/fixtures/`. `cmp`
against `round117_prep/fixtures/` reads all three identical, so no copy is in the commit.

## Census

Denominator: **18 sites** of the rich export (the 15 rich rows of the `AMGT-by-1` census, with its row 31 split into its
two callers `_model_cases_markdown` and `_model_case_line`, plus `M3` (the CEO reading code) and `W1` (the Header money
rule), both found in this cell). Each site was exercised alone with a leaky served object (a reason carrying
`s3://opal-data-harvest/x/y.json` and `AMGT-rj-11 has not landed one`), by `.scratch/by2_census.py` at the base and after.
"BEFORE" and "AFTER" quote the line for that site.

| # | Site (base line) | by-1 row | Served field | BEFORE | AFTER | Result |
|---|---|---|---|---|---|---|
| P1 | `_peers_markdown` absent reason (1679) | 19 | peer_set.reason, peer_read.status | `<reason> (read READ_FAILED)` | `No peer set is on file for this company yet. (read failed)` | routed; status in words |
| P2 | `_peers_markdown` absent column (1718) | 20 | csc_columns.absent[].reason | `C1: ABSENT -- <reason>` | `C1: ABSENT -- the registry join for this column is not on file yet` | routed |
| Q1 | `_posture_markdown` ABSENT (1766) | 21 | posture.reason | `Posture: ABSENT -- <reason>` (two lines) | `Posture: ABSENT -- no positioning view is on file for this name` (two lines) | routed |
| Q2 | `_posture_markdown` READ_FAILED (1758) | 22 | posture.reason | the raw reason on its own line | `the reason on file is not stated in plain words` | routed |
| Q3 | `_posture_markdown` SERVED absent verdict (1779) | 23 | posture.reason | `ABSENT -- no call was made: <reason>` (two lines) | `ABSENT -- no call was made: the reason on file is not stated in plain words` (two lines) | routed |
| M1 | `_management_markdown` ABSENT (1637) | 24 | absent_because, reason | `Exec Management: ABSENT (NO_OBJECT).` then the raw reason | `Exec Management: ABSENT (no management object is on file).` then `no management object is on file for this name` | code in words; reason routed |
| M2 | `_management_markdown` READ_FAILED (1631) | 25 | management.reason | the raw reason | `the reason on file is not stated in plain words` | routed |
| M3 | `_management_markdown` CEO reading (1658) | new | ceo_profile_reading.reading | `CEO public-profile reading: UNREADABLE_OBJECT` | `CEO public-profile reading: the object could not be read` | state code in words |
| D1 | `_undrafted_thesis_markdown` INVALID (1591) | 26 | drafting_reason | `Cause: <reason>` | `Cause: the reason on file is not stated in plain words` | routed |
| D2 | `_undrafted_thesis_markdown` incomplete (1596) | 27 | drafting_reason | `The read did not complete: <reason>` | `The read did not complete: the reason on file is not stated in plain words` | routed |
| H1 | `_header_description_lines` (1609) | 28 | description.reason | `Description: ABSENT -- <reason>` | `Description: ABSENT -- no description is on file for this name yet` | routed |
| H2 | `_drafted_section_markdown` verdict (1539) | 29 | description_verdict_reason | `Description: ABSENT -- <reason>` | `Description: ABSENT -- no description is on file for this name yet` | routed |
| H3 | `_thesis_driver_chart_markdown` (1928) | 30 | thesis_driver.series | `The chart: ABSENT -- the thesis driver is "<series>"` | `The chart: ABSENT` (a non-plain series is not printed) | routed |
| C1 | `_model_cases_markdown` via `_model_case_line` (1837) | 31 | case.reason | `Base case: ABSENT -- <reason>` | `Base case: ABSENT -- the reason on file is not stated in plain words` | routed (no export caller; see `-S4`) |
| C2 | `_model_case_line` (1837), direct caller | 31 | case.reason | same | same | routed |
| R1 | `_refused_figures_markdown` (1913) | 32 | check_face reason | `IS_EPS: REFUSED -- <reason>` | `IS_EPS: REFUSED -- the check did not pass for this figure; no value is shown` | routed (test-only caller) |
| F1 | `build_rich_text` REFUSED row via `_row_refusals` (2168) | 33 | check_face reason | `IS_EPS: REFUSED -- <reason>` | same as R1 | routed |
| W1 | `_figures_table` Header rows (bx-2 rule) | new | currency_basis UNMEASURED, money unit | `Market cap` `115578925918.1821 ABSOLUTE (full currency units)`; `Net debt` `14512.0 MILLIONS`; `Enterprise value` `173616.0345711613 MILLIONS` (RIO LN) | `Market cap: Bloomberg does not confirm this figure's currency` (and the two others); no amount | withheld, as the page withholds |

**Money figure lines, before and after.** RIO LN: three withheld rows (the amounts above) now read the page's words.
ICT PM: `Net debt` withheld; `Market cap` and `Enterprise value` print their measured amounts as before. GOOGL US: the
Header section is identical to the base capture (`diff` clean; R3 compares the four money rows byte for byte). The
money-row census has 4 rows per name: `PX_LAST`, `CUR_MKT_CAP`, `NET_DEBT`, `CURR_ENTP_VAL`.

**Leak census, after.** `.scratch/by2_census.py` at the committed tree: no `s3://`, no `AMGT-`, no `NoSuchKey` and no ISO
day remains in any of the 18 sites. The UPPER_SNAKE tokens left are the figure's own mnemonic (see `-S6`): the
`IS_EPS: REFUSED` line and the Rendered cell's own code segment on measured rows.

## Tests re-scoped

Each re-scoped assertion pinned a served reason or a served state code, which is the bound's category. Each is replaced
by a hand-written expectation; every other assertion of each file is unchanged.

1. `lib/research/print/tests/test_build_rich_text.py`, `test_description_bundle_carries_the_pages_absent_reason_verbatim`
   - old: `assert "Description: ABSENT -- {0}".format(absent_description["reason"]) in text`
   - new: `assert "Description: ABSENT -- no description is on file for this name yet" in text` and
     `assert absent_description["reason"] not in text` (the reason names `CIE_DES` and `CIE_DES_BULK`: not plain words).
2. `lib/research/print/tests/test_build_rich_text.py`, `test_undrafted_thesis_read_incomplete_carries_its_own_reason`
   - old: `assert "The read did not complete: no drafted document at s3://opal-data-harvest/drafting/v1/X.json" in text`
   - new: `assert "The read did not complete: the reason on file is not stated in plain words" in text` and
     `assert "s3://" not in text`.
3. `lib/research/print/tests/test_build_rich_text.py`, `test_exec_management_absent_matches_the_pages_own_two_lines`
   - old: `assert "Exec Management: ABSENT (ZERO_OFFICERS)." in text` and
     `assert "the object carries 0 officers and no roster_reason" in text`
   - new: `assert "Exec Management: ABSENT (the object on file names no officers)." in text`,
     `assert "ZERO_OFFICERS" not in text`, `assert "the object carries 0 officers and no roster_reason" not in text`, and
     `assert "no management object is on file for this name" in text`. The reason carries `roster_reason`, a field code.
4. `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py`, `test_Q3_control_inverse_of_export_equals_base_export_recorded_at_base_head`
   - old: `assert mapped == recorded` (the recorded base carries the one line `Exec Management: ABSENT (NO_OBJECT).`).
   - new: `old_line = "Exec Management: ABSENT (NO_OBJECT)."`, `new_line = "Exec Management: ABSENT (no management object is on file)."`,
     `assert old_line in recorded`, `expected = [new_line if ln == old_line else ln for ln in recorded]`,
     `assert mapped == expected`. Diff of the 54 lines before the re-scope: that one line, and nothing else.
   - `bv2_rich_text_base_RIO_LN.txt` is recorded base text and is not edited.

The `test_bw4_print_pack_degrades.py` and `test_print_format_rich.py` api tests pass unchanged.

## Run record

- **Base (unedited head `8c7b466432`), the two new files run once:** `15 failed, 2 passed` on the first run
  (R3 failed for a sort-order mistake in its own expected list, fixed to a set comparison); on the second run
  **`14 failed, 3 passed`** of 17. The 3 passes are the controls R3 (GOOGL money rows), R6 (pack PDF figure lines) and R12
  (route equals `build_rich_text`). The 14 failures are R1, R2 (`Net debt` withheld), the three R4 variants, R5, R7 to R11
  (three), and R13.
- **After the product edit, committed `882c46d46c`:** the two new files `17 passed in 2.43s`, exit 0 (AC1).
- **Print folder (AC2):** `1 failed, 249 passed` in 89.56 s; the one FAILED line is
  `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`, the known failure
  (the order states the base reads `1 failed, 189 passed`; not re-measured here). 249 is 241 (AMGT-by-1's count at
  `c1b1c53bd7`) plus the eight new print tests.
- **Rich-route api tests:** `test_print_format_rich.py`, `test_bw4_print_pack_degrades.py`,
  `test_by2_rich_route_degrades.py`: `18 passed`; `test_print_fiscal_year_sort.py`: `5 passed`.
- `python -I -m ruff check --target-version py39` on the six changed Python files: `All checks passed!`, rc 0.
  `lib/research/api/scoped_amgt.py` carries 7 non-ASCII characters, the same count as its base; none added.

## Not verified

- **Deploy.** Nothing is deployed. The Lambda serves the old renderer until `AMGT-bx-5`. No AWS, store, vendor, model or
  network call was made. The risk-reflex HOLDs at the commit (`scoped_amgt.py` and `render_pack.py`) cite the deploy
  completion records `20260924T2133Z_amgt-corpus-fwd12-model-block-pull` and `20260926T0935Z_amgt-rs-2-the-redeploy`; the
  closure diff of the next deploy against the deployed build is the place those notes apply. Not run here.
- **Whole api folder.** Not run in this sparse worktree; the four files above that touch the rich route were run. The
  issuer runs the api folder in the full tree after the merge.
- **R2 as written.** The order's R2 expects `Market cap` to print `PHP` and `Enterprise value` to print `USD` on the
  export. The export table prints measured money rows without a currency code (base and after), rule (2) keeps them
  unchanged and control R3 forbids a code on the GOOGL money rows. R2 is graded on what the table can carry. The
  PHP and USD lines are the PDF's (`Market cap: PHP 1,735,465.1 million`). Surprise `AMGT_RESAPP-D1-W515-S3`.
- **Rule (4) and `_model_cases_markdown`.** The case rule takes CRNCY when a case carries no code (AMGT-rs-1, the page's
  `caseCurrency`). The export does not call it, so no export line is affected. Surprise `AMGT_RESAPP-D1-W515-S4`.
- **The api region.** The order's bound 2 says not to edit `scoped_amgt.py`; its region and paths grant the rich branch.
  Only the rich branch was edited. Surprise `AMGT_RESAPP-D1-W515-S5`.
- **The rich Rendered cell's own code.** R5 is graded with the figure's own mnemonic legitimate. Surprise `AMGT_RESAPP-D1-W515-S6`.
- **Served figure sources.** Surprise `AMGT_RESAPP-D1-W515-S2` (ARMED, from by-1) is untouched: the figure-line
  functions are outside this cell's region. The served sources were not read (no AWS call).
- **Not routed, by design.** Basis claim text in Positioning (`-S1`); the registry codes in the Peers present-column table
  (`code`, not a reason); evidence `location` and accession lines and the drafted prose (served content, not reasons; no
  fixture carries them). The Model Notes `<MNEMONIC>: REFUSED` line keeps the row's own mnemonic.
- **Layout.** The export is Markdown, read as text; the PDF was not inspected visually. The text of the three names' exports
  was read once (`.scratch/after/`): the rewritten lines read as intended.
- **Description guard.** `read_description` is the fourth reader the rich branch calls; it is guarded too (rule 3). Its
  absence is written as `{"status": "ABSENT", "reason": "the description read did not complete"}`, because
  `build_rich_text` prints the Description line only for a description it is given.
