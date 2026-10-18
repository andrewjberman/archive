# AMGT-bx-1 receipt -- 0.9.0_WK_AMGT_RESAPP~512

Base: `51cbf82b4f` (issuance). Code commit: `aa93cada46` (LOCAL on `wk-AMGT_RESAPP-512`). Order: `AMGT_RESAPP.TO-AMGT-bx-1.the-pack-summary-reads-the-served-recommendation-and-no-state-sentence-names-a-path-or-an-order.md`.

## What changed

- `lib/research/print/render_pack.py`: 85 insertions, 9 deletions (region: the Summary, the Positioning and the Peers absence sites; `_print_management`, the figure-line functions and the markdown writers are untouched).
- `lib/research/print/tests/test_bx1_summary_positioning.py`: new, 253 lines, 18 cases (S1 to S8).
- `lib/research/print/tests/fixtures/bx_served_thesis_RIO_LN.json`, `..._ICT_PM.json`, `..._GOOGL_US.json`: copied from the round117_prep folder, 1435, 1754, 1888 lines.
- `lib/research/print/tests/fixtures/bx1_figure_lines_base_RIO_LN.txt` (7 lines), `..._ICT_PM.txt` (7), `..._GOOGL_US.txt` (4): S6's base capture, taken from the unedited renderer at `51cbf82b4f`.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 5 rows appended (`AMGT_RESAPP-D1-W512-S1` to `-S5`), 125 lines added to the file, each row `disarm_owner` `2.0.0_SA_COO~R1`.

## Base run (unedited head `51cbf82b4f`, before the edit)

`python -m pytest lib/research/print/tests/test_bx1_summary_positioning.py -q`: **14 failed, 4 passed**.
Failing: S1 (1), S2 (1), S3 (1), S4 (3), S5 drafted arm (1), S7 (3), S8 (4). Passing: S5 absent arm (1) and S6 controls (3). The S5 absent arm passes at the base (surprise row S1).

## After the edit

- AC1 (the order's literal invocation): `18 passed in 11.25s` / `exit=0`.
- AC2 (the order's literal invocation): `FAILED lib/research/print/tests/test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` / `1 failed, 164 passed, 4 warnings in 50.21s`.

## Census

Denominator: 23 print sites on the PDF/txt surface (every section builder `build_pack` reaches). 8 change, 15 stay (each named). Before and after are the printed line for the case the site handles.

| # | Site (builder) | Served state | Before | After |
|---|---|---|---|---|
| C1 | Summary, drafted recommendation sentences | drafted sentences SERVED | the sentence | unchanged |
| C2 | Summary, absence of the recommendation | drafted absent | "No recommendation has been written for this company yet." whatever the position | the same sentence ONLY when the drafted AND the served position are absent |
| C3 | Summary, served recommendation text | `last_stated_position` SERVED | absent (not read) | the served `text` (RIO: `MAINTAIN 2.75% POSITION IN IDVZ`) |
| C4 | Summary, fund and weight | SERVED, not line-only | absent | `Fund IDVZ, weight 2.75 per cent of the fund.` (not for GOOGL US, line-only) |
| C5 | Summary, citation | SERVED with citation | absent | `Source: research report "Rio Tinto H1 2026 Earnings Update", passage 2.` |
| C6 | Summary, drafted thesis absent | drafted absent | "No investment thesis has been written for this company yet." | unchanged |
| C7 | Summary, drafted thesis sentences | SERVED | the sentence | unchanged |
| C8 | Risks, absent or error | drafted absent / read failed | plain sentence / "could not be read" | unchanged |
| C9 | Company description, absent | description absent | plain sentence; "Filed detail ..." heading line | unchanged |
| C10 | Management, absent bio | bio absent | "No chief executive or board biography ..." | unchanged (Management builder: AMGT-bx-3) |
| C11 | Management, CEO profile sentence | reading not CONFIRMED | "CEO public profile ...: <reason>" | unchanged; carries none for the three names (reading UNREADABLE_OBJECT, reason null); surprise row S3 |
| C12 | Positioning, posture None | no posture object | "No analyst posture is on file for this company yet." | unchanged (pinned by api test D3, outside the grant); surprise row S2 |
| C13 | Positioning, posture ABSENT | `status` ABSENT | `Posture: ABSENT -- <reason>.` with `s3://` and `AMGT-rj-11` | "No positioning view is on file for this name." |
| C14 | Positioning, posture READ_FAILED | read failed | first line + the raw reason | first line only (the raw reason is not printed) |
| C15 | Positioning, SERVED verdict absent | verdict `absent` | `ABSENT -- no call was made: <reason>` | "No positioning call was made for this name." |
| C16 | Positioning, verdict sentence, disclaimer, claims | SERVED | served text | unchanged |
| C17 | Peers, peer set None | no peer set | "No peer set is on file for this company yet." | unchanged |
| C18 | Peers, basis absent | `basis` absent | the raw served reason | "No peer set is on file for this company yet." |
| C19 | Peers, members and column counts | SERVED | counts | unchanged |
| C20 | What changed | fixed sentence | plain | unchanged |
| C21 | Appendix, lead sentence | fixed sentence | plain | unchanged |
| C22 | Appendix, figure lines (Header, Fiscal year) | figures | figure lines | unchanged (bx-2 region; S6 control) |
| C23 | Title and Printed line | run date | plain | unchanged |

Rich markdown export (`build_rich_text`, the `.md` file): NOT in the table. Its reason-bearing sites (`_undrafted_thesis_markdown` prints the drafting reason with `s3://` and `NoSuchKey`; `_posture_markdown`, `_peers_markdown`, `_management_markdown`, `_drafted_section_markdown`, `_model_case_line` and the refused-figure lines print served reasons verbatim) are carried unchanged: their wording is pinned by `test_posture_markdown.py` and `test_build_rich_text.py`, and changing it is a multi-assertion re-scope beyond the one-assertion bound. Surprise row S4.

## Tests re-scoped

none. No existing test was edited. The api folder was not edited.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-bx-5`; no live pack was rendered and no AWS or network call was made.
- The api folder (`lib/research/api/tests`) was not run in this sparse worktree; the issuer runs it in the full tree. Known pins there that this cell touches: `test_bw4_print_pack_degrades.py` D3 (the posture None arm, kept unchanged) and D2 (the peer reader raising, kept unchanged). Other api tests that call `build_pack` were not run.
- Summary order: the cell's order (a) drafted recommendation and thesis, (b) served line, (c) absence sentence, so for the three names the thesis line ("No investment thesis has been written ...") prints before the served recommendation. The reader sees it that way; this is a read-back question for the issuer, not changed here.
- The sparse worktree lacks `org/surprise_channel/schemas/investigation_item.schema.json`; the row form was checked against the base copy (surprise row S5).
- The status flip stays with the issuer (order section 5, and `<paths>` does not grant the task-order file).
