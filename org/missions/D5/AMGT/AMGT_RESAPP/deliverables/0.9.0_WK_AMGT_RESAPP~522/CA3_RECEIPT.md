# AMGT-ca-3 receipt -- the rich export prints the Thesis pillars passage wherever the PDF does

**Serial:** `0.9.0_WK_AMGT_RESAPP~522` (round 120, issued by `2.0.0_SA_COO~R1`). **Branch:** `wk-AMGT_RESAPP-522`.
**Base:** `129afa54ec`. **Code commit:** `41faa41432` (LOCAL, not pushed). **Sparse worktree:** `C:/dev/wk-resapp-522`.

## What changed

| path | change | lines |
|---|---|---|
| `lib/research/print/render_pack.py` | new `_ExportLines` sink and `_thesis_pillars_markdown` helper, beside `_undrafted_thesis_markdown` (hunk at 1689); two call sites in `build_rich_text` (hunk at 2291) | +34 / -0 |
| `lib/research/print/tests/test_ca3_export_thesis_pillars.py` | new test file, 26 tests (P1 x3, P2 x5, P3 x5, P4 x4, P5 x3, P6 x3, P7 x3) | +267 |
| `lib/research/print/tests/fixtures/bz_served_thesis_{RIO_LN,ICT_PM,GOOGL_US,ICICIBC_IN,HD_US,BA_US,KMB_US,TSM_US}.json` | the eight round-119 served thesis bodies. Already tracked at base; `cmp` against `round119_prep` is identical for all eight, so no bytes changed | 0 |
| `lib/research/print/tests/fixtures/ca3_base_export_ICT_PM.md` | base rich export of ICT PM, recorded from the unedited renderer | 76 |
| `lib/research/print/tests/fixtures/ca3_base_export_GOOGL_US.md` | base rich export of GOOGL US, recorded from the unedited renderer | 62 |
| `lib/research/print/tests/fixtures/ca3_base_export_ICICIBC_IN.md` | base rich export of ICICIBC IN, recorded from the unedited renderer | 68 |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` | two rows appended: `AMGT_RESAPP-D1-W522-S1`, `AMGT_RESAPP-D1-W522-S2` | +50 |

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

none. No existing test was edited. The print folder is run whole for AC2 (below): `1 failed, 342 passed`.

## Not verified

- The deployed Lambda serves the old renderer until `AMGT-ca-5`. Nothing here is deployed.
- The whole `lib/research/api/tests` folder is not run in this sparse worktree; the issuer runs it in the full tree.
- The SERVED drafting branch is exercised only by P7, which copies one fixture and adds one drafted risks sentence. No
  served fixture has `drafting_status` SERVED.
- The export's Summary heading does not exist (row S1); the placement follows the order's stated position.
