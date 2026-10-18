# BZ3 receipt -- AMGT-bz-3 (0.9.0_WK_AMGT_RESAPP~519, round 119)

Base: 8e81e269f7 (issuance). Branch: wk-AMGT_RESAPP-519. Order: AMGT_RESAPP.TO-AMGT-bz-3 (issued by 2.0.0_SA_COO~R1).
Scope: the pack appendix's served `source` and basis definition go through `_plain_reason` or the appendix's fixed sentence; the unknown-verdict sentence reads `steer clear`.

## What changed

- `lib/research/print/render_pack.py` -- 41 insertions, 7 deletions. Regions: the bz-3 block above `_plain_label` (`SOURCE_NOT_PLAIN_SENTENCE`, `PROVENANCE_SEPARATOR`, `_definition_plain`, `_render_fig_for_appendix`); `_plain_label` (definition fallback and forecast branch); `_plain_figure_line` (code segment and source segment); `_source_words`; `UNKNOWN_VERDICT_SENTENCE`; the plain-unknown-verdict form in `_verdict_sentence`. `_plain_reason` itself, the rich export and `render_print.py` are not edited.
- `lib/research/print/tests/test_bz3_appendix_plain_and_verdict.py` -- new, 227 lines. Tests W1 to W6, 34 cases.
- `lib/research/print/tests/test_by1_reason_mapper.py` -- 1 line (the `UNKNOWN_VERDICT` constant, re-scoped; see below).
- `lib/research/print/tests/fixtures/bz_served_thesis_{RIO_LN,ICT_PM,GOOGL_US,ICICIBC_IN,HD_US,BA_US,KMB_US,TSM_US}.json` -- new, 8 copies of the round119_prep fixtures (1435 to 2939 lines each; 556742 bytes in total).
- `lib/research/print/tests/fixtures/bz3_appendix_base_<NAME>.txt` -- new, 8 files, 25 to 27 lines each: the appendix block of each name as the UNEDITED renderer printed it at 8e81e269f7 (recorded at Step A by `.scratch/bz3_record_base.py`, not committed).
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` -- +125 lines, 0 deleted: five rows `AMGT_RESAPP-D1-W519-S1` to `-S5`, each with `disarm_owner` `2.0.0_SA_COO~R1`.
- This receipt, and the proof instance beside it.

## Census

Driver: `.scratch/bz3_census.py`, which renders the three-name fixture pack per site and reads the appendix line of the site's figure (PyMuPDF text). Served strings: `s3://opal-data-harvest/x/y.json` (S3) and `AMGT-rj-11 has not landed one` (AMGT-id). Base line numbers are at 8e81e269f7; the after lines are in the last column.

Denominator: 6 served-text print paths of the Appendix x 2 served strings = 12 driven cases. Not routed (fixed or served values, not the source or definition): `APPENDIX_HEADING`, `APPENDIX_SENTENCE`, `_NO_DATE_NOTE`, the `Header` and `Fiscal year <Y>` headings, and the served value and unit text (`_format_figure_value`, the unit words).

| # | Print path (base line; after line) | Served field printed | BEFORE, S3 served | BEFORE, AMGT-id served | AFTER (both strings) |
|---|---|---|---|---|---|
| 1 | `_withheld_line` -> `_source_words` (642-649; 674-681). Header line for a withheld money figure | `source` | `Market cap: Bloomberg does not confirm this figure's currency - s3://opal-data-harvest/x/y.json` | `... - AMGT-rj-11 has not landed one` | `... - The source is on file but is not stated in plain words.` |
| 2 | `_header_print_lines` -> `_plain_figure_line`, source segment (563-604; 589-640). Header line | `source` | `Share price (last close): GBp 6,816.00 per share - s3://opal-data-harvest/x/y.json` | `... - AMGT-rj-11 has not landed one` | `Share price (last close): GBp 6,816.00 per share - The source is on file but is not stated in plain words.` |
| 3 | `build_pack` Fiscal year loop -> `_plain_figure_line`, source segment. Fiscal year 2026 line | `source` | `Net debt: 14,512.0 million currency not stated - period ending December 31st, 2026 - s3://opal-data-harvest/x/y.json` | `... - AMGT-rj-11 has not landed one` | `... - The source is on file but is not stated in plain words.` |
| 4 | `_plain_label`, basis definition fallback, unknown mnemonic (410-437; 435-455). Header line | `basis.definition` | `S3://opal-data-harvest/x/y.json: GBp 6,816.00 per share - Bloomberg` | `AMGT-rj-11 has not landed one: GBp 6,816.00 per share - Bloomberg` | `A line this pack does not name: GBp 6,816.00 per share - Bloomberg` |
| 5 | `_plain_label`, forecast "estimate of" branch. Fiscal year 2026 line | `basis.definition` | `Consensus estimate of s3://opal-data-harvest/x/y.json: GBp 6,816.00 per share - period ending December 31st, 2026 - Bloomberg` | `Consensus estimate of AMGT-rj-11 has not landed one: ...` | `A line this pack does not name: GBp 6,816.00 per share - period ending December 31st, 2026 - Bloomberg` |
| 6 | `_plain_figure_line`, code segment split on the middle dot (571-573; 596-598). Header line | `basis.definition` (a definition carrying the separator; a probe, no served value does) | `Beta: 1.06x - EQY_BETA (Beta - s3://opal-data-harvest/x/y.json) - Bloomberg` | `Beta: 1.06x - EQY_BETA (Beta - AMGT-rj-11 has not landed one) - Bloomberg` | `Beta: 1.06x - Bloomberg` |

Source of the BEFORE and AFTER lines: `.scratch/bz3_census_before.txt` and `.scratch/bz3_census_after.txt` (the driver's output at 8e81e269f7 and after the edit). Row 6's AFTER line drops the fragments and the label stays the table's.

Served source and definition values of the eight names, read from the fixtures (denominator 194 header figures across 8 names): 190 carry `bloomberg-dapi`, 4 carry no source key (`CURR_ENTP_VAL` IN; `SHORT_INT_RATIO` IN, PM, LN); 0 definitions carry the middle dot. Among the fiscal-period sources, see S1 (`bloomberg-dapi (fiscal-period join, model_block_fye)`, bu3 fixture).

## Tests

- Dry run at the unedited base (Step A), `python -m pytest lib/research/print/tests/test_bz3_appendix_plain_and_verdict.py -q`:
  - Final base run, after the test corrections below: **15 failed, 19 passed (34 cases)**. Failing: W1 12 of 12 (six sites x two strings), W4 3 of 3 (the constant and the two rendered cases). Passing as controls: W2 8 of 8, W3 1 of 1, W5 2 of 2, W6 8 of 8.
  - The first base run was 14 failed, 20 passed, before three corrections to my own test file, all made before the cell's edit: W3 expected the header-listing form (the `date not stored` segment belongs to `_plain_figure_line`); the middle-dot probe used NET_DEBT, which RIO withholds, so it never reached the code segment (now EQY_BETA); W1's label cases raised a TypeError from a keyword collision in the helper (renamed). Then the path checks were made case-insensitive, because the label code upper-cases a first letter (S4). Each correction is a fix to the test, none to the renderer.
- After the edit, AC1 literal invocation: **34 passed** (two runs, both 34 passed, exit 0).
- AC2 full print folder, after the edit: `1 failed, 283 passed` with the one known FAILED line. A first post-edit run gave `3 failed, 281 passed`: `test_bu3_pack_long_dates.py::test_T6` and `test_bv2_rich_dates_and_quotes.py::test_Q4` failed on the fiscal-period source `bloomberg-dapi (fiscal-period join, model_block_fye)`, which the mapper judged before the estate's own clean-up. The fix judges the source after the clean-up (surprise S1); both controls then passed.

## Tests re-scoped

- `lib/research/print/tests/test_by1_reason_mapper.py`, line 57, constant `UNKNOWN_VERDICT` (used by the SITES row `positioning-unknown-verdict`, test Y2):
  - old: `The verdict on file is not one of better, worse, hold or steer_clear: no call is shown.`
  - new: `The verdict on file is not one of better, worse, hold or steer clear: no call is shown.`
  - The assertion is unchanged (`expected in flat`); only the hand-written expectation moved, as the order's item 4 says.
- No other existing test pins the changed words (grep of `lib/` for `steer_clear: no call` and `not one of better` at base: the constant in `render_pack.py` and this one line of `test_by1_reason_mapper.py`).

## Decisions beyond the order's literal text (for the issuer's reading)

- Item 3 routes the source as it prints, after the estate's own clean-up (`bloomberg-dapi` to `Bloomberg`, the `model_block_fye` cut). Routing it before the clean-up failed T6 and Q4 (S1).
- A served definition that carries the middle dot is not plain for the appendix (`_definition_plain`). The separator is the one the figure line itself uses; a definition containing it splits its own code segment (S3). This is a rule beyond `_plain_reason`, stated in `render_pack.py`.
- The plain unknown-verdict form at `render_pack.py` `_verdict_sentence` now reads `steer clear` too (S2).
- An absent source prints the render's `?` fallback, which the byte-identical control holds; left as is (S5).

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-bx-5`; nothing here is deployed (no deploy, no store, no AWS, no vendor, no network call).
- The whole `lib/research/api` folder is not run in this sparse worktree; the issuer runs it in the full tree after the merge. The print folder was run in full (283 passed, 1 known failure).
- The W6 UPPER_SNAKE check covers the eight names' whole pack text, not only the appendix; it passes.
- Ruff ran through `.tools/commit-gate.sh` (clean on the three edited `.py` files).
