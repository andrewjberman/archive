# AMGT-bx-3 receipt -- 0.9.0_WK_AMGT_RESAPP~514

Order: `AMGT_RESAPP.TO-AMGT-bx-3.the-pack-prints-the-cleared-machine-written-passages-the-page-shows-each-with-its-label`
(round 117, decomposition s.126, issued by 2.0.0_SA_COO~R1). Branch `wk-AMGT_RESAPP-514`.

Commits (all LOCAL on `wk-AMGT_RESAPP-514`):
- `93edac99e4` the cell's code, tests and fixtures (base `51cbf82b4f`).
- `37118895a3` the surprise rows S1 to S4 (investigation file).
- `a83f29eaa3` AMENDMENT 1 re-seat: Management passages above the roster; the CEO profile line only when no management passage prints; M8 to M10; census fixture updated to the amended placement. Base for the amendment: `2cf00a8cca` (contains the merged head `3dd98e9a9d`).
- This receipt and the proof instance, committed after `a83f29eaa3`.

## What changed

- `lib/research/print/render_pack.py`, commit `93edac99e4` (+125 / -3 lines), then commit `a83f29eaa3` (+13 / -14 lines). The region the order names and nothing else:
  - the Management builder (`_print_management`), AMENDMENT 1 order: the `mgmt_team_view` passage (when it prints), then `mgmt_bio`, then `mgmt_recent`, each with its label, THEN the officer roster; the line `CEO public profile:` prints only when NO management passage (team view, bio or recent) prints; a roster-only Management is unchanged; the NOT_WRITTEN bio sentence still prints when nothing does;
  - new helpers `_cleared_passage` (the one gate: SERVED fill, text from a served source class, validation CLEARED with verdict PASS and a dated check), `_citation_words` (title and host, never a path), `_machine_label` (one label line), `_print_passage`, `_dossier_failed`, `_team_view_gap_open`, `_pillars_gap_open`, `_print_thesis_pillars`;
  - one call in `build_pack`'s section list: `_print_thesis_pillars(p, thesis_bundle or {})` between Summary and Risks and considerations (unchanged by the amendment);
  - the identity fallback in Company description (`identity_description`, only when the served company-description line is empty; unchanged by the amendment).
  - Summary, Positioning and the figure-line functions are untouched.
- `lib/research/print/tests/test_bx3_cleared_machine_passages.py` (new in `93edac99e4`, 241 lines; `a83f29eaa3` adds 51 lines and changes 3): M1 to M7 as before; M8, M9, M10 added by the amendment; the R2 and R6 docstring lines re-worded to the amended rule.
- `lib/research/print/tests/fixtures/bx_served_thesis_RIO_LN.json`, `..._ICT_PM.json`, `..._GOOGL_US.json`: copies of the round117_prep fixtures, unchanged.
- `lib/research/print/tests/fixtures/bx3_page_draw_table.json`: the Step A census, denominator 15. The amendment (`a83f29eaa3`) rewrites the `pack_after_bx3` values to the amended placement and adds an `amendment_1_note`; the page-draw and pack-today columns are unchanged.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` (commit `37118895a3`): rows `AMGT_RESAPP-D1-W514-S1` to `S4`, `disarm_owner` `2.0.0_SA_COO~R1` on each. The amendment files no new row.

Decisions the order did not state (each is also a surprise row from the first run):

- Gap conditions (row S2). The page draws `mgmt_team_view` only when the dossier carries no served management passage and the read did not fail, and `thesis_pillars` only when the served pillar list is empty and the read did not fail. The pack applies the same conditions. All three fixtures meet them.
- Identity source (row S1). The pack reads the header CIE_DES line as the served company-description line; the page reads `top_band.description_line` or `bundle.description`. No identity block carries text on the three names.
- Label width (row S3). A captioned label is 115 or 120 characters and the paginator wraps at 92, so it prints on two physical lines. The label is one logical line.
- Placement (row S4). The first run followed the order's original rule (passages after the roster). The page draws `mgmt_bio` and `mgmt_recent` above the roster. AMENDMENT 1 moved the passages above the roster; the order as amended is followed here. Row S4 is not edited.
- A CLEARED block with no parseable `checked_at` day prints nothing, because its label could not carry its day.
- The label separator is ` | `, and a citation prints as `title (host)`; an Opal citation prints its `ref`.

## Census

Denominator 15 block-name pairs: 8 with served text, 7 withheld. Every block is `validation.state` CLEARED with verdict PASS. "Page draws" is hand-written from the page components (`AiFillBlock.tsx`, `ExecManagementTab.tsx`, `ThesisTab.tsx`, `SecurityOverlay.tsx`, nested portal `3a7791c1`). "Pack today" is measured at the base `51cbf82b4f` by `.scratch/base_probe.py`. "Pack after" is the amended placement (AMENDMENT 1); the full table is `lib/research/print/tests/fixtures/bx3_page_draw_table.json`.

| name | block | text served | source class | page draws | pack today (base, measured) | pack after AMGT-bx-3, amended |
|---|---|---|---|---|---|---|
| RIO_LN | identity_description | n | NONE | nothing (NONE gap) | nothing | nothing |
| RIO_LN | mgmt_bio | n | NONE | always: one reason sentence, no passage | nothing | nothing |
| RIO_LN | mgmt_recent | n | NONE | always: one reason sentence, no passage | nothing | nothing |
| RIO_LN | mgmt_team_view | y | WEB_SEARCH | gap open (dossier management ABSENT): passage, chip, caption, citation | nothing | first in Management, above the roster, labelled; CEO profile line not printed |
| RIO_LN | thesis_pillars | n | NONE | nothing (gap, NONE) | nothing | nothing; no Thesis pillars heading |
| ICT_PM | identity_description | n | NONE | nothing (NONE gap) | nothing | nothing |
| ICT_PM | mgmt_bio | y | WEB_SEARCH | always: passage, chip, three citations, drawn ABOVE the roster | nothing | first in Management, above the roster, labelled; CEO profile line not printed |
| ICT_PM | mgmt_recent | y | WEB_SEARCH | always: passage, chip, one citation, drawn ABOVE the roster | nothing | above the roster, after mgmt_bio, labelled |
| ICT_PM | mgmt_team_view | n | NONE | nothing (gap, NONE) | nothing | nothing |
| ICT_PM | thesis_pillars | y | WEB_SEARCH | gap open (pillar list empty, read not failed): one prose line, caption, citation | nothing | Thesis pillars section between Summary and Risks, labelled with caption |
| GOOGL_US | identity_description | n | NONE | nothing (NONE gap) | nothing | nothing |
| GOOGL_US | mgmt_bio | y | WEB_SEARCH | always: passage, chip, one citation, drawn ABOVE the roster | nothing | above the roster, after mgmt_team_view, labelled |
| GOOGL_US | mgmt_recent | y | WEB_SEARCH | always: passage, chip, one citation, drawn ABOVE the roster | nothing | above the roster, after mgmt_bio, labelled |
| GOOGL_US | mgmt_team_view | y | WEB_SEARCH | gap open (dossier management ABSENT): passage, caption, citation | nothing | first in Management, above the roster, labelled with caption; CEO profile line not printed |
| GOOGL_US | thesis_pillars | y | WEB_SEARCH | gap open (pillar list empty): passage, caption, citation | nothing | Thesis pillars section, labelled with caption |

Measured at the base: the three packs print 0 served passages and 0 label tokens, and each prints the line `CEO public profile: no public profile is on file yet.`. After AMENDMENT 1 that line prints on none of the three names (each carries a management passage: RIO LN the team view, ICT PM the bio and recent, GOOGL US all four).

## Runs

- Dry run at the unedited base `51cbf82b4f` (first cut), `python -m pytest lib/research/print/tests/test_bx3_cleared_machine_passages.py`: `5 failed, 2 passed`. M1 to M5 fail; M6 and M7 pass. M6 is vacuous at that base: zero label lines, zero passages found.
- After the first edit: `7 passed in 13.77s`, exit 0.
- Dry run of the amendment's new tests on the pre-amendment head `2cf00a8cca` renderer (M8, M9, M10 added, the renderer not yet edited): `2 failed, 8 passed`. M8 and M9 fail (the passages sit after the roster and the CEO line prints); M10 passes on it, as the control for the roster-and-CEO-line-as-before arm.
- After AMENDMENT 1 (commit `a83f29eaa3`), AC1: `10 passed`, exit 0.
- After AMENDMENT 1, AC2 (the print folder): `1 failed, 186 passed, 4 warnings in 69.88s`; the one FAILED line is `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`, the known base failure. P = 186, at least 183.
- Rendered narrative of the three packs was read as text (not a layout check): RIO LN opens Management with the Trott profile, labelled, then the roster and no CEO profile line; ICT PM opens Management with the bio, labelled, then recent, then the roster; GOOGL US opens with team view, bio, recent, then the roster, all labelled.
- `ruff check --target-version py39` on `render_pack.py` and the test file: `All checks passed!`, rc 0. `py_compile` rc 0. Added lines are ASCII (0 non-ASCII characters in the amendment's diff).

## Tests re-scoped

- No assertion of M1 to M7 was edited. The amendment's order asked for a re-scope of "assertions that pin the old placement": none of the existing assertions pinned the roster-relative order (M1 and M2 check position inside the Management section only, and M1 checks that the CEO line is absent there). The R2 and R6 lines of the test file's docstring are re-worded to the amended rule. Old docstring R2: "mgmt_bio, mgmt_recent and mgmt_team_view print inside Management after the roster, in that order". New: "inside Management, mgmt_team_view, mgmt_bio and mgmt_recent print before the officer roster, in that order". Old R6: "stays when no mgmt_team_view passage prints, and is not printed when one does". New: "prints only when NO management passage (team view, bio or recent) prints".
- Existing tests outside the bx-3 file: none edited.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-bx-5`; nothing here is deployed, and no AWS, HTTP, store, vendor, model or Bloomberg call was made.
- The whole `lib/research/api` folder is not run in this sparse worktree; the issuer runs it in the full tree after the merge. The `r116_pack_form_check.py` update for the new `Thesis pillars` heading belongs to `AMGT-bx-4` and is not touched here.
- The PDF layout is not looked at; the grade is on the rendered text.
- `safe-commit` printed the naming-gate `NAMING ERROR` for the missing infra function-map folder in this sparse worktree, as recorded in `AMGT_RESAPP-D1-W511-S10`; the commits passed (rc 0). The client-data check printed WARN (hashed account-id list absent on this box); the amendment commit touches no account data.
- `status` in the order stays `pending`; the flip is the issuer's, as the order's section 5 states.
