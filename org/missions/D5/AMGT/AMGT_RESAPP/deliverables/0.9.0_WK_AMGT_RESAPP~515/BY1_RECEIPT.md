# AMGT-by-1 receipt -- every served reason the pack prints goes through one plain-sentence mapper

**Worker:** `0.9.0_WK_AMGT_RESAPP~515` (issued by `2.0.0_SA_COO~R1`, round 118, decomposition s.127).
**Branch:** `wk-AMGT_RESAPP-515` (LOCAL, never pushed). **Base:** `afcd188f9b` (the issuance commit).
**Code commit:** `c1b1c53bd7` (LOCAL on `wk-AMGT_RESAPP-515`).
**Task order:** [AMGT_RESAPP.TO-AMGT-by-1](../../task-orders/AMGT_RESAPP.TO-AMGT-by-1.every-served-reason-the-pack-prints-goes-through-one-plain-sentence-mapper.md).

The census below is measured at the base `afcd188f9b` (before the product edit) and again at `c1b1c53bd7`. The
measurements come from `.scratch/by1_census.py` in the worktree (scratch, not committed), which drives the test
module's own variants: `census` (PDF), `rich` (rich helpers) and `figline` (figure-line probe).

## What changed

| Path | Lines (added / removed) | Note |
|---|---|---|
| `lib/research/print/render_pack.py` | 57 / 5 | mapper `_plain_reason` and `_path_token` with the pattern list; routed sites; `NO_POSTURE_SENTENCE` removed |
| `lib/research/print/tests/test_by1_reason_mapper.py` | 309 / 0 | new: Y1 to Y6, 52 tests |
| `lib/research/print/tests/fixtures/by1_base_sections_RIO_LN.json` | 33 / 0 | Y3 base capture, unedited renderer |
| `lib/research/print/tests/fixtures/by1_base_sections_ICT_PM.json` | 64 / 0 | Y3 base capture, unedited renderer |
| `lib/research/print/tests/fixtures/by1_base_sections_GOOGL_US.json` | 50 / 0 | Y3 base capture, unedited renderer |
| `lib/research/print/tests/fixtures/by1_base_figure_lines_RIO_LN.json` | 9 / 0 | Y5 base capture, unedited renderer |
| `lib/research/print/tests/fixtures/by1_base_figure_lines_ICT_PM.json` | 9 / 0 | Y5 base capture, unedited renderer |
| `lib/research/print/tests/fixtures/by1_base_figure_lines_GOOGL_US.json` | 6 / 0 | Y5 base capture, unedited renderer |
| `lib/research/print/tests/test_bu3_pack_long_dates.py` | 8 / 2 | T6 re-scoped (see Tests re-scoped) |
| `lib/research/print/tests/test_build_rich_text.py` | 1 / 1 | one pinned sentence re-scoped |
| `lib/research/api/tests/test_bw4_print_pack_degrades.py` | 2 / 2 | `POSTURE_ABSENT` re-scoped (D3); docstring names the new constant |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | 52 / 0 | rows `AMGT_RESAPP-D1-W515-S1` and `-S2` appended; no existing row edited |

The three fixtures `bx_served_thesis_<NAME>.json` were already in `lib/research/print/tests/fixtures/` and were
compared byte for byte with the served copies in `round117_prep/fixtures/` (`cmp`, all three identical). No copy
was needed, so none is in the commit.

## Census

Denominator: **33 sites** (pdf 18, rich 15). Before and after columns quote the printed line for a served reason
`s3://opal-data-harvest/posture/v1/X/y.json` (S3) and for `AMGT-rj-11 has not landed one` (AMGT). Line numbers are
the base file's (`afcd188f9b`). "Routed" means the site now goes through `_plain_reason`.

| # | Function (base line) | Surface | Served field read | BEFORE (S3 / AMGT) | AFTER | Fixed sentence |
|---|---|---|---|---|---|---|
| 1 | `_print_positioning` None arm (1068-1071) | pdf | posture argument None (the route's read raised) | "No analyst posture is on file for this company yet." / same | "No positioning view is on file for this name." / same | POSITIONING_ABSENT_SENTENCE (changed: S2 unified) |
| 2 | `_print_positioning` absent arm (1078-1081) | pdf | posture.status ABSENT, posture.reason | "No positioning view is on file for this name." / same (reason not printed) | same | POSITIONING_ABSENT_SENTENCE (unchanged) |
| 3 | `_print_positioning` READ_FAILED arm (1073-1077) | pdf | posture.status READ_FAILED, posture.reason | "Posture: the read did not complete -- not evidence that no posture exists." / same | same | unchanged |
| 4 | `_verdict_sentence` unknown verdict (1063; called at 1086) | pdf | posture.verdict (SERVED) | "Verdict s3://opal-data-harvest/posture/v1/X/y.json is not one of better, worse, hold or steer_clear: no call is shown." / "Verdict AMGT-rj-11 has not landed one is not one of ..." | "The verdict on file is not one of better, worse, hold or steer_clear: no call is shown." / same | UNKNOWN_VERDICT_SENTENCE (changed: routed) |
| 5 | `_print_peers` absent (1104-1108) | pdf | peer_set.basis absent, peer_set.reason | "No peer set is on file for this company yet." / same | same | NO_PEERS_SENTENCE (unchanged) |
| 6 | `_print_peers` members and column counts (1109-1117) | pdf | members name and ticker, csc counts | content, not a reason: not routed | same | none |
| 7 | `_print_management` absent bio (1038-1041) | pdf | management.reason, absent_because (not printed) | "No chief executive or board biography has been written for this company yet." / same | same | NOT_WRITTEN["bio"] (unchanged) |
| 8 | `_ceo_profile_sentence` reason (891-898; called at 1035) | pdf | management.ceo_profile_reading.reason | "CEO public profile: s3://opal-data-harvest/posture/v1/X/y.json." / "CEO public profile: AMGT-rj-11 has not landed one." | "CEO public profile: no public profile is on file yet." / same | "no public profile is on file yet" (changed: routed) |
| 9 | `_citation_words` Opal branch (950; called at 967) | pdf | ai_fill citation ref, source_kind opal | "s3://opal-data-harvest/posture/v1/X/y.json" / "AMGT-rj-11 has not landed one" | "Opal source" / same | "Opal source" (changed: routed) |
| 10 | `_citation_words` web branch, title and host (944-949) | pdf | citation title, url host | content, not a reason: not routed | same | none |
| 11 | `_print_drafted` error (768-769) and `_print_summary` rec_error (864-866) | pdf | drafted.error | "The drafted text could not be read when this print was made." / same (error text not printed) | same | unchanged |
| 12 | `_print_positioning` basis claims (1089-1095) | pdf | posture.basis[].claim | analyst text printed as served (no SERVED posture in the fixtures, so not exercised) | same | NOT ROUTED: surprise `AMGT_RESAPP-D1-W515-S1` |
| 13 | `_comparable_label` (1044-1050; via the SERVED verdict sentence) | pdf | comparable_identity.display_ticker, comparable_name | identity text, not a reason: not routed | same | none |
| 14 | `_served_position_lines`, `_citation_line`, `_report_title` (809-844) | pdf | last_stated_position value, fund, size_pct, citation report_key and locator | content, and the report's own title (AMGT-bx-1 S1 requires it) | same | none |
| 15 | `_cleared_passage`, `_machine_label`, `_print_passage` (913-969) | pdf | ai_fill block text, source_class, validation | served passage text; an unknown source class returns None | same | none |
| 16 | `_plain_figure_line` (563-603): the source segment | pdf (Appendix) | fiscal figure source, non-BBG, passed through `_long_days` only | "Synthetic definition: 1.50x - s3://opal-data-harvest/bronze/x.json" (probe) / same class of output | same | OUT OF REGION (figure-line function): NOT ROUTED: surprise `AMGT_RESAPP-D1-W515-S2` (ARMED) |
| 17 | `_plain_label` (410-437): basis.definition | pdf (Appendix) | figure basis.definition when no mapped name | "S3://opal-data-harvest/x/y.json definition: 1.50x - Bloomberg" (probe) | same | OUT OF REGION: row `-S2` |
| 18 | `_withheld_line` and `_source_words` (642-654) | pdf (Appendix) | withheld money figure, served source | "Market cap: Bloomberg does not confirm this figure's currency - AMGT-rj-11 feed" (probe) | same | OUT OF REGION: row `-S2` |
| 19 | `_peers_markdown` absent (1626-1631) | rich | peer_set.reason | "s3://opal-data-harvest/posture/v1/X/y.json" / "AMGT-rj-11 has not landed one" | identical (not edited) | by-2 |
| 20 | `_peers_markdown` absent column (1666-1669) | rich | csc_columns.absent[].reason | "C1: ABSENT -- s3://opal-data-harvest/posture/v1/X/y.json" / "C1: ABSENT -- AMGT-rj-11 has not landed one" | identical | by-2 |
| 21 | `_posture_markdown` ABSENT (1713-1724) | rich | posture.reason | "Posture: ABSENT -- s3://..." (both lines) / "Posture: ABSENT -- AMGT-rj-11 has not landed one" | identical | by-2 |
| 22 | `_posture_markdown` READ_FAILED (1706-1711) | rich | posture.reason | raw reason on its own line | identical | by-2 |
| 23 | `_posture_markdown` SERVED absent verdict (1727-1735) | rich | posture.reason | "ABSENT -- no call was made: s3://..." | identical | by-2 |
| 24 | `_management_markdown` ABSENT (1589-1592) | rich | management.absent_because, reason | "Exec Management: ABSENT (NO_OBJECT)." then the raw reason | identical | by-2 |
| 25 | `_management_markdown` READ_FAILED (1582-1583) | rich | management.reason | raw reason on its own line | identical | by-2 |
| 26 | `_undrafted_thesis_markdown` INVALID (1541) | rich | drafting_reason | "Cause: s3://..." | identical | by-2 |
| 27 | `_undrafted_thesis_markdown` read incomplete (1545) | rich | drafting_reason | "The read did not complete: s3://..." | identical | by-2 |
| 28 | `_header_description_lines` (1558) | rich | description.reason | "Description: ABSENT -- s3://..." | identical | by-2 |
| 29 | `_drafted_section_markdown` company_description verdict (1492-1493) | rich | description_verdict_reason | "Description: ABSENT -- s3://..." | identical | by-2 |
| 30 | `_thesis_driver_chart_markdown` (1881) | rich | thesis_driver.series | 'The chart: ABSENT -- the thesis driver is "s3://..."' | identical | by-2 |
| 31 | `_model_case_line` (1785); not called by `build_rich_text` | rich | case.reason | "Base case: ABSENT -- s3://..." | identical | by-2 (test-only callers) |
| 32 | `_refused_figures_markdown` (1861); not called by `build_rich_text` | rich | check_face reason | "X: REFUSED -- s3://..." | identical | by-2 (test-only callers) |
| 33 | `build_rich_text` REFUSED row (2114-2116) via `_row_refusals` (1914-1933) | rich | check_face reason | read from code, not run in this census: prints the reason verbatim | identical | by-2 |

**Counts:** pdf 18 rows: 4 changed (rows 1, 4, 8, 9), 14 unchanged (fixed sentence already, content, or out of region).
Rich 15 rows, all unchanged (`rich` output byte-identical before and after, checked by `diff`).

## Tests re-scoped

Each old assertion and its new hand-written expectation:

1. `lib/research/api/tests/test_bw4_print_pack_degrades.py`, `POSTURE_ABSENT` (line 39, asserted by test D3 when the
   posture read raises, so `build_pack` receives `posture=None`).
   - old: `Positioning No analyst posture is on file for this company yet.`
   - new: `Positioning No positioning view is on file for this name.`
   - Docstring line 11 now names `POSITIONING_ABSENT_SENTENCE` for the posture arm.
2. `lib/research/print/tests/test_build_rich_text.py`, `_NO_BUNDLE_SENTENCES[1]` (line 291), asserted by
   `test_build_pack_bundles_add_narrative_only_and_the_md_rule_holds` in clauses (4) and (5).
   - old: `No analyst posture is on file for this company yet.`
   - new: `No positioning view is on file for this name.`
3. `lib/research/print/tests/test_bu3_pack_long_dates.py`, T6 (lines 151-163). T6 compared the whole rendered text
   with the recorded bu3 base text, which carries the old posture line. Re-scoped, not weakened: the test now asserts
   the old line is present in the base (so the substitution is not vacuous) and that the rendered text equals the base
   with that ONE line replaced by the new line; every other line is compared as before.
   - old: `mapped == _dewrap(base)`
   - new: `expected = [new_line if ln == old_line else ln for ln in base]`, `mapped == expected`, with `old_line` the
     old sentence and `new_line` the new one.
   - `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py::test_Q4_control_bu3_pack_test_still_passes` re-runs
     the bu3 file in a subprocess; it failed only because T6 failed, and it passes now with T6 re-scoped. Q4 itself
     is not edited.

The recorded bu3 base texts (`fixtures/bu3_pack_text_base_*.txt`) still carry the old line. They are recorded base
text and are read only by T6, so they are not edited.

No other test asserts `No analyst posture is on file`. `NO_POSTURE_SENTENCE` has no reference left in `lib/` (grep).

## Run record

- Base, unedited head `afcd188f9b`, `lib/research/print/tests/test_by1_reason_mapper.py`: **42 failed, 10 passed**
  of 52. The 10 passes are the Y2 cases of the sites already fixed at base (positioning absent, read failed, peers
  absent, management absent, summary drafted error; two reasons each). Y3 and Y5 read as missing-fixture failures in
  that run; after the base captures were taken from the unedited renderer, the six controls passed at base (6 passed).
- After the product edit at `c1b1c53bd7`: **52 passed** (AC1), 18.85 s and 18.47 s, exit 0 on two runs.
- AC2 at `c1b1c53bd7`: **1 failed, 241 passed** (the known `test_av2` failure only). Before the T6 re-scope the same
  folder read 3 failed (av2, T6 and, through its subprocess, Q4).
- `python -I -m ruff check --target-version py39` on the five changed Python files: All checks passed, rc 0.

## Not verified

- **Deploy.** Nothing is deployed. The deployed Lambda serves the old renderer until `AMGT-bx-5`. No AWS, store, vendor
  or network call was made.
- **Whole api folder.** Only `test_bw4_print_pack_degrades.py` was run in this sparse worktree. The issuer runs the
  api folder in the full tree after the merge.
- **Served figure sources.** Surprise `-S2` is ARMED because the figure-line functions print a served source raw. The
  served source values were not read (no AWS call), so whether a live source carries a path is unmeasured.
- **Positioning claims.** A basis claim printed in Positioning is not routed (row `-S1`). No fixture carries a SERVED
  posture, so the claim path is not exercised by any control.
- **Layout.** The grade is on the rendered text. The PDF layout was not inspected visually.
- **Known failure.** `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`
  fails at the base as well. It was not investigated.
- **Disarm.** This cell's code disarms `AMGT_RESAPP-D1-W512-S2` (the None arm prints the absent-posture sentence) and
  `AMGT_RESAPP-D1-W512-S3` (the CEO reason goes through the mapper). Those rows were not edited (append-only); the
  disarm is for `2.0.0_SA_COO~R1` to confirm.
