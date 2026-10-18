# AMGT-ca-3 receipt -- the rich export prints the Thesis pillars passage wherever the PDF does

**Serial:** `0.9.0_WK_AMGT_RESAPP~522` (round 120, issued by `2.0.0_SA_COO~R1`). **Branch:** `wk-AMGT_RESAPP-522`.
**Base:** `129afa54ec`. **Code commit:** `41faa41432` (LOCAL, not pushed). **Amendment 1 commit:** `33edcbdf16` (LOCAL, not pushed; the re-scoped P5 control and surprise row S3). **Sparse worktree:** `C:/dev/wk-resapp-522`.

## What changed

| path | change | lines |
|---|---|---|
| `lib/research/print/render_pack.py` | new `_ExportLines` sink and `_thesis_pillars_markdown` helper, beside `_undrafted_thesis_markdown` (hunk at 1689); two call sites in `build_rich_text` (hunk at 2291) | +34 / -0 |
| `lib/research/print/tests/test_ca3_export_thesis_pillars.py` | new test file, 26 tests (P1 x3, P2 x5, P3 x5, P4 x4, P5 x3, P6 x3, P7 x3) | +267 |
| `lib/research/print/tests/fixtures/bz_served_thesis_{RIO_LN,ICT_PM,GOOGL_US,ICICIBC_IN,HD_US,BA_US,KMB_US,TSM_US}.json` | the eight round-119 served thesis bodies. Already tracked at base; `cmp` against `round119_prep` is identical for all eight, so no bytes changed | 0 |
| `lib/research/print/tests/fixtures/ca3_base_export_ICT_PM.md` | base rich export of ICT PM, recorded from the unedited renderer | 76 |
| `lib/research/print/tests/fixtures/ca3_base_export_GOOGL_US.md` | base rich export of GOOGL US, recorded from the unedited renderer | 62 |
| `lib/research/print/tests/fixtures/ca3_base_export_ICICIBC_IN.md` | base rich export of ICICIBC IN, recorded from the unedited renderer | 68 |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | two rows appended: `AMGT_RESAPP-D1-W522-S1`, `AMGT_RESAPP-D1-W522-S2` (code commit); row `AMGT_RESAPP-D1-W522-S3` appended in Amendment 1 (`33edcbdf16`) | +50, then +26 |
| `lib/research/print/tests/test_ca3_export_thesis_pillars.py` (Amendment 1, `33edcbdf16`) | P5 control: one named constant `CA2_BASE_TO_NOW_SOURCE`, one helper `_base_to_now_source`, one comparison line re-scoped | +12 / -1 |

The PDF is untouched. The diff has no hunk in the PDF region (`_pillars_gap_open` 1065, `_print_thesis_pillars` 1071,
`_cleared_passage` 993, `_print_passage` 1043 are read only). No existing test was edited.

**Placement.** The export has no summary heading (row S1). The section sits immediately before `## Risks and Considerations`
when `drafting_status` is SERVED, and immediately after the single `## Investment Thesis` block when it is not (every
fixture). Both positions are before `## Management/Board`.

**Printed form.** The section is `## Thesis pillars`, a blank line, then `_print_passage`'s own lines (the passage text,
the label `machine-drafted, cleared <long day> | <source words> | Machine-written, not the research team's pillars.`, and
one line per citation), then a blank. Dates pass through the export's `_long_days` exactly as the PDF's `_wrap` passes them.

## Census

Denominator: 8 names. Columns read from the served fixtures and from `render_pack.py` at base `129afa54ec`.
The block carries no `status` key on any of the eight (row S2); the fill's status is `ai_fill.status`.

| name | ai_fill.status | `_pillars_gap_open` | block source_class | validation state / verdict / checked_at | `_cleared_passage` | PDF prints Thesis pillars | export prints pillars (base) |
|---|---|---|---|---|---|---|---|
| RIO_LN | SERVED | y | NONE | CLEARED / PASS / 2026-10-16T16:52:04Z | n (text null) | n | n |
| ICT_PM | SERVED | y | WEB_SEARCH | CLEARED / PASS / 2026-10-16T16:52:04Z | y | y | n |
| GOOGL_US | SERVED | y | WEB_SEARCH | CLEARED / PASS / 2026-10-16T16:52:04Z | y | y | n |
| ICICIBC_IN | SERVED | y | WEB_SEARCH | CLEARED / PASS / 2026-10-16T16:52:04Z | y | y | n |
| HD_US | SERVED | y | NONE | CLEARED / PASS / 2026-10-16T16:52:04Z | n (text null) | n | n |
| BA_US | SERVED | y | NONE | CLEARED / PASS / 2026-10-16T16:52:04Z | n (text null) | n | n |
| KMB_US | SERVED | y | NONE | CLEARED / PASS / 2026-10-16T16:52:04Z | n (text null) | n | n |
| TSM_US | SERVED | n (dossier `thesis_pillars` holds 2 pillars) | NONE | CLEARED / PASS / 2026-10-16T16:52:04Z | n (text null) | n | n |

Read: the PDF prints the section for 3 of 8 names (ICT PM, GOOGL US, ICICIBC IN); the export printed it for 0 of 8 at
base. After the edit the export prints it for exactly those 3, and for 0 of the 5 controls (P1 3/3, P2 5/5).

## Runs

- Base (unedited head `129afa54ec`, new test file run once): `9 failed, 14 passed in 23.63s`. Failing: P1 x3, P5 x3, P6 x3
  (the new behaviour). Passing: P2 x5, P3 x5, P4 x4 (controls).
- After the edit: `26 passed in 19.93s`, then `26 passed in 19.26s` (the AC1 literal run).

## Tests re-scoped

One assertion, in this order's own P5 control (not a test that existed at base), re-scoped by Amendment 1; see the
`## Amendment 1` section below for the old and new assertion. No existing test was edited. The print folder is run
whole for AC2 (below): at the code commit `1 failed, 342 passed`; after Amendment 1 `1 failed, 432 passed`.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-ca-5`. Nothing here is deployed.
- The whole `lib/research/api/tests` folder is not run in this sparse worktree; the issuer runs it in the full tree.
- The SERVED drafting branch is exercised only by P7, which copies one fixture and adds one drafted risks sentence. No
  served fixture has `drafting_status` SERVED.
- The export's Summary heading does not exist (row S1); the placement follows the order's stated position.

## Amendment 1

**Why.** The issuer's merged tree (`dda778e2f8`, with the other two round-120 cells `a1eb3b86ce` and `f64668f0e8`) failed
P5 for ICICIBC IN on the `## Header` section. The base fixture recorded `?` as the source of two figure rows; AMGT-ca-2
prints `source not stated` for an absent, blank or `?` source, on purpose. P5 compared that section to the base
text, so another cell's intended change failed this cell's control.

**Counts.** The file at the amended head, before the re-scope: `1 failed, 25 passed` (the failing case
`test_P5_control_export_outside_the_pillars_section_equals_the_base_export[ICICIBC_IN]`). After the re-scope: `26 passed`.
The print folder run once after the re-scope: `1 failed, 432 passed in 217.36s` (the one failure is the known
`test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`).

**Re-scoped assertion (one; `test_P5_control_export_outside_the_pillars_section_equals_the_base_export`).**
- Old: `assert now[heading] == was[heading], heading`
- New: `assert now[heading] == _base_to_now_source(was[heading]), heading`, where `CA2_BASE_TO_NOW_SOURCE = (chr(183) + " ? |", chr(183) + " source not stated |")`
  is the named constant (comment: AMGT-ca-2 changed it on purpose), and `_base_to_now_source` rewrites only a BASE line that
  ends in the first element of that pair, to the second. The map is applied to the base side only; every other line is
  compared exactly. The fixture is not edited; no product file and no other test is touched.

**Surprise row S3 (`AMGT_RESAPP-D1-W522-S3`, OBSERVATION, INERT, disarm_owner `2.0.0_SA_COO~R1`).** The amendment names
two rows that carry the unstated source (`CURR_ENTP_VAL` and `SHORT_INT_RATIO`). The measured bytes hold one: the base
fixture's Header has nine figure rows, and only `CURR_ENTP_VAL` (line 17) ends in the `?` source cell. No `SHORT_INT_RATIO`
row exists in the base fixture or in the current export of ICICIBC IN (rendered in this worktree, 75 lines). The map is
written generically, so it covers every such row, and no `SHORT_INT_RATIO` line is mapped or invented. The issuer rules
whether the amendment text is corrected.

**Commits.** Test re-scope and the row: `33edcbdf16` (LOCAL). This receipt and the proof instance: see the commit that
carries them (LOCAL, the amendment's second commit). Code commit `41faa41432` is unchanged.
