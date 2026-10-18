# AMGT-bx-3 receipt -- 0.9.0_WK_AMGT_RESAPP~514

Order: `AMGT_RESAPP.TO-AMGT-bx-3.the-pack-prints-the-cleared-machine-written-passages-the-page-shows-each-with-its-label`
(round 117, decomposition s.126, issued by 2.0.0_SA_COO~R1). Branch `wk-AMGT_RESAPP-514`, base `51cbf82b4f`.
Code and tests commit `93edac99e4` (LOCAL). Surprise rows commit `37118895a3` (LOCAL). This receipt and the instance commit after them.

## What changed

- `lib/research/print/render_pack.py` (+125 / -3 lines, commit `93edac99e4`). The region the order names and nothing else:
  - the Management builder (`_print_management`): after the roster, `mgmt_bio`, `mgmt_recent`, then the `mgmt_team_view` gap fill; the CEO profile line stays only when no team-view passage prints;
  - new helpers `_cleared_passage` (the one gate: SERVED fill, text from a served source class, validation CLEARED with verdict PASS and a dated check), `_citation_words` (title and host, never a path), `_machine_label` (one label line), `_print_passage`, `_dossier_failed`, `_team_view_gap_open`, `_pillars_gap_open`, `_print_thesis_pillars`;
  - one call in `build_pack`'s section list: `_print_thesis_pillars(p, thesis_bundle or {})` between Summary and Risks and considerations;
  - the identity fallback in Company description (`identity_description`, only when the served company-description line is empty; `NOT_WRITTEN` for that section is suppressed only when the fallback prints).
  - Summary, Positioning and the figure-line functions are untouched; no import was added at module scope (`urlsplit` is imported inside `_citation_words`).
- `lib/research/print/tests/test_bx3_cleared_machine_passages.py` (new, 241 lines): M1 to M7, hand-written expectations, built with `build_pack` from the committed fixtures, read with PyMuPDF.
- `lib/research/print/tests/fixtures/bx_served_thesis_RIO_LN.json` (1435 lines), `bx_served_thesis_ICT_PM.json` (1754 lines), `bx_served_thesis_GOOGL_US.json` (1888 lines): copies of the round117_prep fixtures, unchanged.
- `lib/research/print/tests/fixtures/bx3_page_draw_table.json` (76 lines): the Step A census, denominator 15.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` (+102 lines, commit `37118895a3`): rows `AMGT_RESAPP-D1-W514-S1` to `S4`, `disarm_owner` `2.0.0_SA_COO~R1` on each.

Decisions the order did not state (each is also a surprise row):

- Gap conditions (row S2). The page draws `mgmt_team_view` only when the dossier carries no served management passage and the read did not fail, and `thesis_pillars` only when the served pillar list is empty and the read did not fail. The pack applies the same conditions. All three fixtures meet them.
- Identity source (row S1). The pack reads the header CIE_DES line as the served company-description line; the page reads `top_band.description_line` or `bundle.description`. No identity block carries text on the three names.
- Label width (row S3). A captioned label is 115 or 120 characters and the paginator wraps at 92, so it prints on two physical lines. The label is one logical line.
- Placement (row S4). The page draws `mgmt_bio` and `mgmt_recent` above the roster; the order's rule puts them after it, and the order was followed.
- A CLEARED block with no parseable `checked_at` day prints nothing, because its label could not carry its day.
- The label separator is ` | `, and a citation prints as `title (host)`; an Opal citation prints its `ref`.

## Census

Denominator 15 block-name pairs: 8 with served text, 7 withheld. Every block is `validation.state` CLEARED with verdict PASS. "Page draws" is hand-written from the page components (`AiFillBlock.tsx`, `ExecManagementTab.tsx`, `ThesisTab.tsx`, `SecurityOverlay.tsx`, nested portal `3a7791c1`). "Pack today" is measured at the base `51cbf82b4f` by `.scratch/base_probe.py` (opening 40 characters searched in the PDF text, label tokens counted).

| name | block | text served | source class | page draws | pack today (base, measured) | pack after AMGT-bx-3 |
|---|---|---|---|---|---|---|
| RIO_LN | identity_description | n | NONE | nothing (NONE gap) | nothing | nothing |
| RIO_LN | mgmt_bio | n | NONE | always: one reason sentence, no passage | nothing | nothing |
| RIO_LN | mgmt_recent | n | NONE | always: one reason sentence, no passage | nothing | nothing |
| RIO_LN | mgmt_team_view | y | WEB_SEARCH | gap open (dossier management ABSENT): passage, chip, caption, citation | nothing | passage under Management after the roster, labelled, CEO profile line not printed |
| RIO_LN | thesis_pillars | n | NONE | nothing (gap, NONE) | nothing | nothing; no Thesis pillars heading |
| ICT_PM | identity_description | n | NONE | nothing (NONE gap) | nothing | nothing |
| ICT_PM | mgmt_bio | y | WEB_SEARCH | always: passage, chip, three citations, drawn ABOVE the roster | nothing | passage under Management after the roster, labelled, three citation lines |
| ICT_PM | mgmt_recent | y | WEB_SEARCH | always: passage, chip, one citation, drawn ABOVE the roster | nothing | passage after mgmt_bio, labelled, one citation line |
| ICT_PM | mgmt_team_view | n | NONE | nothing (gap, NONE) | nothing | nothing |
| ICT_PM | thesis_pillars | y | WEB_SEARCH | gap open (pillar list empty, read not failed): one prose line, caption, citation | nothing | Thesis pillars section between Summary and Risks, labelled with caption |
| GOOGL_US | identity_description | n | NONE | nothing (NONE gap) | nothing | nothing |
| GOOGL_US | mgmt_bio | y | WEB_SEARCH | always: passage, chip, one citation, drawn ABOVE the roster | nothing | passage under Management after the roster, labelled |
| GOOGL_US | mgmt_recent | y | WEB_SEARCH | always: passage, chip, one citation, drawn ABOVE the roster | nothing | passage after mgmt_bio, labelled |
| GOOGL_US | mgmt_team_view | y | WEB_SEARCH | gap open (dossier management ABSENT): passage, caption, citation | nothing | passage after mgmt_recent, labelled with caption; CEO profile line not printed |
| GOOGL_US | thesis_pillars | y | WEB_SEARCH | gap open (pillar list empty): passage, caption, citation | nothing | Thesis pillars section, labelled with caption |

Measured at the base: the three packs print 0 served passages and 0 label tokens, and each prints the line `CEO public profile: no public profile is on file yet.` (the line the order says to keep when no team-view passage prints).

## Runs

- Dry run at the unedited base `51cbf82b4f`, `python -m pytest lib/research/print/tests/test_bx3_cleared_machine_passages.py`: `5 failed, 2 passed`. M1 to M5 fail; M6 and M7 pass. M6 is vacuous at the base: zero label lines, zero passages found.
- After the edit: `7 passed in 13.77s`, exit 0.
- Full print folder after the edit: `1 failed, 153 passed, 4 warnings in 48.75s`; the one FAILED line is `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`, the known base failure. The base folder count (146 passed) is the order's recorded value; it was not re-measured at the base in this session.
- Rendered narrative of the three packs was read as text (not a layout check): RIO LN prints the Trott profile under Management and no CEO profile line; ICT PM prints bio, recent and a Thesis pillars section between Summary and Risks; GOOGL US prints all four, labelled.
- `ruff check --target-version py39` on `render_pack.py` and the new test file: rc 0. `py_compile` rc 0. Added lines are ASCII (0 non-ASCII characters).

## Tests re-scoped

none. No existing test was edited; the only test file added is `test_bx3_cleared_machine_passages.py`.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-bx-5`; nothing here is deployed, and no AWS, HTTP, store, vendor or Bloomberg call was made.
- The whole `lib/research/api` folder is not run in this sparse worktree; the issuer runs it in the full tree after the merge. The `r116_pack_form_check.py` update for the new `Thesis pillars` heading belongs to `AMGT-bx-4` and is not touched here.
- The PDF layout is not looked at; the grade is on the rendered text.
- `safe-commit` printed the naming-gate `NAMING ERROR` for the missing infra function-map folder in this sparse worktree, as recorded in `AMGT_RESAPP-D1-W511-S10`; the commit passed (rc 0). The same worktree condition applies to this commit.
- The gate's one-writer WARN for the investigation file names the laptop's unsuffixed file, which is the path the order names; the per-box file convention is noted by the gate as WARN until C-QUEUE.
- `status` in the order stays `pending`; the flip is the issuer's, as the order's section 5 states.
