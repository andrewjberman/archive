# AMGT-bx-1 receipt -- 0.9.0_WK_AMGT_RESAPP~512

Base: `51cbf82b4f` (issuance), then the re-seat on the merged head `3dd98e9a9d` (the drain of bx-1, bx-2, bx-3). Code commit (cell): `aa93cada46`. Code commit (AMENDMENT 1, Summary order): `8a7cdc94e8`. Both LOCAL on `wk-AMGT_RESAPP-512`. Order: `AMGT_RESAPP.TO-AMGT-bx-1.the-pack-summary-reads-the-served-recommendation-and-no-state-sentence-names-a-path-or-an-order.md` (AMENDMENT 1 at its section 1).

## What changed

Amendment 1 (commit `8a7cdc94e8`):

- `lib/research/print/render_pack.py`: 22 lines changed (the `_print_summary` builder only: the served block now prints first; the drafted recommendation sentences next; then the drafted thesis sentences or the thesis absence sentence; the no-recommendation sentence only when both the drafted recommendation and the served position are absent, and it leads then). The diff stat reads 22 changed lines (12 insertions, 10 deletions in the function body and its docstring).
- `lib/research/print/tests/test_bx1_summary_positioning.py`: 30 lines added (the S9 and S10 cases and the docstring entries for them). No existing line edited.

The cell (commit `aa93cada46`, unchanged by the amendment):

- `lib/research/print/render_pack.py`: 85 insertions, 9 deletions (region: the Summary, the Positioning and the Peers absence sites; `_print_management`, the figure-line functions and the markdown writers are untouched).
- `lib/research/print/tests/test_bx1_summary_positioning.py`: new; 21 cases after the amendment (S1 to S8 as before, S9 twice, S10 once).
- `lib/research/print/tests/fixtures/bx_served_thesis_RIO_LN.json`, `..._ICT_PM.json`, `..._GOOGL_US.json`: copied from the round117_prep folder, not edited.
- `lib/research/print/tests/fixtures/bx1_figure_lines_base_RIO_LN.txt` (7 lines), `..._ICT_PM.txt` (7), `..._GOOGL_US.txt` (4): S6's base capture, taken from the unedited renderer at `51cbf82b4f`.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 5 rows (`AMGT_RESAPP-D1-W512-S1` to `-S5`), each `disarm_owner` `2.0.0_SA_COO~R1`. No row filed by the amendment.

## Base run for the amendment (unedited renderer at `2cf00a8cca`, the merged head, before the Summary edit; the new S9 and S10 cases in place)

`python -m pytest lib/research/print/tests/test_bx1_summary_positioning.py -q`: **3 failed, 18 passed**.
Failing: S9 RIO LN (1), S9 both-absent (1), S10 (1). The controls and every other case pass at the base, as expected: the three failures are the ordering the amendment names.

## After the amendment

- AC1 (the order's literal invocation): `21 passed in 14.10s` / `exit=0`.
- AC2 (the order's literal invocation): `FAILED lib/research/print/tests/test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` / `1 failed, 186 passed, 4 warnings in 72.08s`.

## Census

Denominator: 23 print sites on the PDF/txt surface (every section builder `build_pack` reaches). 8 change, 15 stay (each named). Before and after are the printed line for the case the site handles. The amendment moves the position of C3 to C5 (the served block) to the top of Summary and C1 (the drafted recommendation) below it; the census's content is unchanged.

| # | Site (builder) | Served state | Before | After |
|---|---|---|---|---|
| C1 | Summary, drafted recommendation sentences | drafted sentences SERVED | the sentence (first) | the sentence (after the served block) |
| C2 | Summary, absence of the recommendation | drafted absent | "No recommendation has been written for this company yet." whatever the position | the same sentence ONLY when the drafted AND the served position are absent; then it leads |
| C3 | Summary, served recommendation text | `last_stated_position` SERVED | absent (not read) | the served `text` (RIO: `MAINTAIN 2.75% POSITION IN IDVZ`), first in Summary |
| C4 | Summary, fund and weight | SERVED, not line-only | absent | `Fund IDVZ, weight 2.75 per cent of the fund.` (not for GOOGL US, line-only) |
| C5 | Summary, citation | SERVED with citation | absent | `Source: research report "Rio Tinto H1 2026 Earnings Update", passage 2.` |
| C6 | Summary, drafted thesis absent | drafted absent | "No investment thesis has been written for this company yet." (before the served line) | unchanged text; now after the served block |
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

none. No existing assertion pins the Summary order: the existing S5 drafted-arm test asserts containment of the sentence and of the served line, not their order, so it is unchanged. No test in the print folder or in the api folder was edited.

## Commit-gate notes

- The pre-commit risk reflex printed a HOLD on `lib/research/print/render_pack.py` (13 recorded claims; the cited line is a redeploy ledger entry about a closure diff, `org/critical_paths/change_management/20260926T0935Z_amgt-rs-2-the-redeploy_deploy_completion.md:15`). The gate passed and the commit landed; the hold was read from the sparse worktree's copy of the map and was not adjudicated here.
- `safe-commit.sh` warned that the hashed account-id list is absent at `C:\Users\Test\.opal\account_id_hashes.txt`, so the commit was not checked for client account ids. The diff carries no account id.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-bx-5`; no live pack was rendered and no AWS or network call was made.
- The api folder (`lib/research/api/tests`) was not run in this sparse worktree; the issuer runs it in the full tree. Known pins there that this cell touches: `test_bw4_print_pack_degrades.py` D3 (the posture None arm, kept unchanged) and D2 (the peer reader raising, kept unchanged). Other api tests that call `build_pack` were not run.
- The sparse worktree lacks `org/surprise_channel/schemas/investigation_item.schema.json`; the row form was checked against the base copy (surprise row S5).
- The status flip stays with the issuer (order section 5, and `<paths>` does not grant the task-order file).
