# AMGT-bw-2 receipt -- the printed pack reads as a note (round 116)

Worker: `0.9.0_WK_AMGT_RESAPP~511`. Issuer: `2.0.0_SA_COO~R1`. Worktree: `C:/dev/wk-resapp-511`, branch `wk-AMGT_RESAPP-511`.
Base: `52a137e363` (the issuance commit). Nested portal worktree at PROD `ff611566`, read-only, not touched.

The cell: FWD-5 was graded NOT MET on the round-115 printed packs (about 830 lines of `label: value - Bloomberg`;
RIO LN's Management section printed the constant `NOT_WRITTEN["bio"]`). The round-116 form puts the narrative first and
the model figures in an appendix. The currency-label functions (`_format_figure_value`, `_money`, `_currency_of`,
`_plain_figure_line`'s currency handling, `_header_figures_for_print`) are untouched.

## Inventory

Denominator: 18 sections listed (`lib/research/print/tests/fixtures/bw2_sections.json`, `denominator.sections_listed` = 18;
F8 checks it equals the entry count). Dispositions: 11 `render`, 0 `state_absent`, 7 `out_of_scope` (each with a reason in the fixture).

| id | page section (tab) | served fields | pack input today | PDF today | disposition | pack position |
|---|---|---|---|---|---|---|
| S01 | Recommendation (Thesis) | drafted_sections[recommendation] | drafted sections, no argument | content or NOT_WRITTEN | render | Summary |
| S02 | Investment thesis (Thesis) | drafted_sections[investment_thesis] | drafted sections, no argument | content or NOT_WRITTEN | render | Summary |
| S03 | Risks (Thesis) | drafted_sections[risks] | drafted sections, no argument | content | render | Risks and considerations |
| S04 | Company description (Thesis) | drafted company_description, header CIE_DES | drafted sections, model block | description line and sentences | render | Company description |
| S05 | CEO bio (Thesis, ceo_bio window) | drafted_sections[ceo_bio] | drafted sections, no argument | nothing (constant bio placeholder) | render | Management, first |
| S06 | Research-notes sections (Thesis) | thesis_bundle.dossier_sections | none on the PDF path | nothing | out_of_scope | -- |
| S07 | Thesis pillars (Thesis) | thesis_bundle.dossier_fields.thesis_pillars | none on the PDF path | nothing | out_of_scope | -- |
| S08 | Chart, segment table, segment breakdown (Thesis) | thesis_driver_chart, segment_table, segment_breakdown | none on the PDF path | nothing | out_of_scope | -- |
| S09 | Held-uncited count line (Thesis footer) | held_uncited_count, held_uncited_basis | none on the PDF path | nothing | out_of_scope | -- |
| S10 | The research team on management (Exec Management) | thesis_bundle.dossier_fields.management.value | none on the PDF path | nothing | render | Management, after the CEO bio |
| S11 | Officer roster (Exec Management) | thesis_bundle.management.officers[] | none on the PDF path | nothing | render | Management |
| S12 | CEO public profile line (Exec Management) | management.ceo_public_profile, ceo_profile_reading | none on the PDF path | nothing | render | Management, last |
| S13 | Management bio, recent developments, management view (AI fills) | thesis_bundle.ai_fill | none on the PDF path | nothing | out_of_scope | -- |
| S14 | Analyst posture verdict and claims (Posture) | posture.verdict, comparable, basis[] | none on the PDF path | nothing | render | Positioning |
| S15 | Comparable set and CSC columns (Peers) | peer_set members, csc_columns | none on the PDF path | nothing | render | Peers |
| S16 | What changed (Model) | two stored model versions | none: one model_block is the input | nothing | out_of_scope | one sentence printed under What changed |
| S17 | Model-tab notes under the figure rows (Model) | modelSheet rows and group notes | model block (figures only) | nothing | out_of_scope | -- (inside the appendix figures) |
| S18 | Model figures: Header and Fiscal year listings (Model) | model block figures | model block, always present | figure lines under Model figures | render | Appendix: model figures, unchanged lines |

Reasons for the seven `out_of_scope` entries are in the fixture: S06, S07, S08, S09 are not sections round-116 Step C names
(for the next enrichment list); S13 is machine-written gap fill, not served text; S16 has no two-version input; S17 sits
under the figure rows, which are printed unchanged.

Verified inputs (Step A): `_print_pack`'s PDF branch passed only `display_form, block`; `build_pack` therefore had no
management, posture or peer input on the served PDF route. The CEO passage is NOT a field of `management` (no passage
key there); the page's passage is `dossier_fields.management.value` and the CEO bio is `drafted_sections[ceo_bio]` (surprise
row `AMGT_RESAPP-D1-W511-S1`).

## What changed

Paths, with line counts (`git diff --numstat` against `52a137e363`; new files counted by `wc -l`):

- `lib/research/print/render_pack.py`: 193 insertions, 27 deletions. New helpers above `build_pack`: `APPENDIX_HEADING`,
  `APPENDIX_SENTENCE`, `NO_POSTURE_SENTENCE`, `NO_PEERS_SENTENCE`, `POSTURE_DISCLAIMER`, `WHAT_CHANGED_SENTENCE`,
  `_dossier_management_passage`, `_officer_line`, `_ceo_profile_sentence`, `_print_management`, `_comparable_label`,
  `_verdict_sentence`, `_print_positioning`, `_print_peers`. `build_pack`: new keyword `write_rich: bool = True` (gates the
  existing `build_rich_text` markdown write; default keeps every other caller's behaviour); the body reordered (page 1:
  title, Printed, Summary; then Risks and considerations, Company description, Management, Positioning, Peers, What changed;
  then page break and Appendix: model figures with the Header and Fiscal year listings, lines unchanged). The two currency
  assignments (`trading_cur`, `reporting_cur`) moved up unchanged, since the company description line uses them too.
  `NOT_WRITTEN["bio"]` is printed only when management has no content (reused as it stands; it says why).
- `lib/research/api/scoped_amgt.py` (Step B, `_print_pack` only): AMENDMENT 1 added 12 insertions and 1 deletion (the PDF
  branch handed `build_pack` the three served reads). AMENDMENT 2 (Part 3) replaced the three inline reads with three guarded
  reads: 22 insertions and 3 deletions against `9590e6e5a5`. Each read is its own try/except; a raising reader is `None`
  (absent) and writes one `_LOG.warning` line. No other function of the file was touched. See `## Print route reads`.
- `lib/research/api/tests/test_bw4_print_pack_degrades.py` (AMENDMENT 2, Part 3, new): 195 lines, six tests (D1 to D6).
  Run once on the UNGUARDED route: D1, D2, D3, D4 and D5 failed with the reader's `RuntimeError`; D6 passed (5 failed, 1 passed).
  After the guard: 6 passed.
- `lib/research/api/tests/test_print_format_rich.py` (AMENDMENT 2, Part 2): one test re-scoped and renamed, 23 insertions, 5 deletions.
- `lib/research/print/tests/test_bw1_currency_labels.py` (AMENDMENT 2, Part 1): C3, and C7 for ICT_PM and RIO_LN re-scoped to the
  figure lines as a multiset, 58 insertions, 12 deletions (a `_figure_lines` helper and `EXPECTED_FIGURE_CHANGES` added).
- `lib/research/print/tests/test_bw2_pack_form.py` (new): 252 lines, ten tests (F1, F2 twice, F3, F4, F5, F6, F7 twice, F8).
- `lib/research/print/tests/fixtures/bw2_sections.json` (new, Step A inventory): 189 lines.
- `lib/research/print/tests/fixtures/bw2_base_figure_lines_RIO_LN.txt` (new): 12 lines, the base figure lines recorded from the
  UNEDITED renderer before the product edit (`.scratch/record_bw2_base.py`).
- `lib/research/print/tests/fixtures/bw2_management_bundle.json` (new, SYNTHETIC): 66 lines.
- `lib/research/print/tests/fixtures/bw2_no_management_bundle.json` (new, SYNTHETIC): 40 lines.
- `lib/research/print/tests/fixtures/bw2_posture_and_peers.json` (new, SYNTHETIC): 30 lines.
- `lib/research/print/tests/fixtures/bu3_pack_text_base_ICT_PM.txt`: re-recorded, 35 insertions, 32 deletions (see Tests changed).
- `lib/research/print/tests/fixtures/bu3_pack_text_base_RIO_LN.txt`: re-recorded, 32 insertions, 28 deletions.
- `lib/research/print/tests/test_build_rich_text.py` (AMENDMENT 1, commit `e0c8b25368`): the one re-scoped test (see Tests changed), 86 insertions, 6 deletions.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 130 insertions (five rows, W511-S1 to S5), then one row W511-S6 (the amendment commit).
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~511/` (this receipt and the proof instance).

The base-text proof (printed before `--write`, `.scratch/bu3_rerecord_proof.py`): the new lines were de-wrapped and mapped through
the inverse long form, as T6 does. For ICT_PM the REMOVED lines are exactly four headings: `Investment thesis`, `Management/Board`,
`Model figures`, `Recommendation`. For RIO_LN the same four. Every other old logical line survives in the new text, and
the ADDED lines are the new headings (`Appendix: model figures`, `Management`, `Peers`, `Positioning`, `Summary`, `What changed`)
and the narrative sentences (the "no analyst posture", "no peer set", "what changed" sentences and the appendix sentence).
Shared-line order changed as the reorder requires. The subset premise as written does not hold by those four headings
(surprise row `AMGT_RESAPP-D1-W511-S4`).

## Tests changed

- One existing test edited, under AMENDMENT 1 (issuer ruling, round 116; commit `e0c8b25368`): see the bullet below. No other existing test file was edited.
- Fixtures re-recorded (data the T6 control compares, not a test): `bu3_pack_text_base_ICT_PM.txt` and
  `bu3_pack_text_base_RIO_LN.txt`, after the proof above. `test_bu3_pack_long_dates.py` T6 passes on them.
- `test_ax4_brand_form.py::test_no_raw_internal_marker_and_each_unwritten_section_says_so` passes WITHOUT edit: it asserts
  `NOT_WRITTEN["bio"]` appears in the flat text for a bundle-less pack, and it still does, because the no-content branch reuses that
  sentence.
- RE-SCOPED under AMENDMENT 1 (commit `e0c8b25368`, the issuer's ruling; row `AMGT_RESAPP-D1-W511-S2`):
  `test_build_rich_text.py::test_build_pack_pdf_and_txt_byte_identical_with_and_without_bundles` is renamed
  `test_build_pack_bundles_add_narrative_only_and_the_md_rule_holds`. The docstring says the PDF half of the AMGT-rl-10 contract
  is superseded by the CTO's FWD-5 ruling (`ledger/ROUND_ANALYSIS.round115.R1.md` items 2 and 3) and the `.md` half stays.
  - OLD assertions: `sha256(pdf_neg) == sha256(pdf_pos)` (the PDF bytes identical with and without the bundles), and
    `sha256(txt_neg) == sha256(txt_pos)`; plus the `.md` rule (no `.md` without a bundle, the `.md` with one).
  - NEW assertions, hand-written: (1) the `.md` rule unchanged; (2) the `Appendix: model figures` section identical in both
    builds, carrying `Header` and `Fiscal year 2016`; (3) Summary, Risks and considerations, Company description identical and
    non-empty; (4) the sections that differ are exactly `Management`, `Positioning`, `Peers`, and the lines the no-bundle build
    prints alone are exactly the three not-on-file sentences (`No chief executive or board biography has been written for this
    company yet.`, `No analyst posture is on file for this company yet.`, `No peer set is on file for this company yet.`), each
    bundle-fed section gaining lines; (5) the no-bundle build prints every narrative section with a body, never a bare heading.
  - Run after the re-scope: `test_build_rich_text.py` 22 passed (the renamed test included).
- RE-SCOPED under AMENDMENT 2 (issuer, the merge repair; slot re-seated; these commits sit after `9590e6e5a5`). The five
  tests below (four test functions, five parametrized cases) are the ONLY existing tests this amendment changes; no other test is edited.
  - `test_bw1_currency_labels.py::test_C3_googl_us_control_text_is_unchanged_from_base` (Part 1): OLD `_render("GOOGL_US")`
    text `== _base("GOOGL_US")` (the whole pre-bw-2 text). NEW: `sorted(figure lines of the new text) ==
    sorted(figure lines of the base text)`, with the count of figure lines hand-written as 4 (Company name, Currency,
    Market cap, the no-date note). The base figure lines are derived from the recorded `bw1_pack_text_base_GOOGL_US.txt`
    (the block after `Model figures` before `Recommendation`); the `bu3_pack_text_base_*.txt` fixtures are untouched.
  - `test_bw1_currency_labels.py::test_C7_base_and_edited_text_differ_only_on_money_lines[ICT_PM]` and `[RIO_LN]` (Part 1):
    OLD difflib opcodes over the whole text, every changed line matches `MONEY_LINE`. NEW: a `Counter` multiset difference of
    the figure lines; every removed or added line matches `MONEY_LINE`, AND the removed and added lists equal
    `EXPECTED_FIGURE_CHANGES[name]` (hand-written). ICT PM: removed `Market value, currency-adjusted: USD 1,735,465.1 million -
    Bloomberg`, added none. RIO LN: removed `Market cap: GBp 115,578.9 million - Bloomberg`, `Market value, currency-adjusted:
    USD 115,578.9 million - Bloomberg`, `Enterprise value: USD 173,616.0 million - Bloomberg`; added `Market cap: 115,578.9
    million currency not stated - Bloomberg`, `Enterprise value: 173,616.0 million currency not stated - Bloomberg`.
  - `lib/research/api/tests/test_print_format_rich.py::test_default_and_fmt_pdf_are_byte_identical_to_build_pack_itself` is
    RENAMED `test_default_and_fmt_pdf_equal_build_pack_with_the_same_served_bundles` (Part 2). OLD: the route's default PDF,
    its `fmt=pdf` PDF and `build_pack(DISPLAY_FORM, model_block, out_dir=tmp_path)` (NO bundles) have one sha256. NEW: the
    three readers are monkeypatched to the fixture's served objects; the default PDF, the `fmt=pdf` PDF and `build_pack(...,
    write_text=False, write_rich=False, thesis_bundle=thesis, peer_set=bundle["peers"], posture=thesis.get("posture"))` have
    one sha256. Status 200 and headers asserted as before.
  - Run after the re-scope: the four tests pass (`test_bw1_currency_labels.py` and the renamed route test are in AC3's 52 passed).
  - Base-fixture note: the bw1 controls use the `bw1_pack_text_base_*.txt` fixtures, which were not re-recorded.
- `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` fails as it does at base
  (the order names it).

## Print route reads

Before and after, in `lib/research/api/scoped_amgt.py` `_print_pack`, PDF branch only (the rich branch is not edited; see the
row `AMGT_RESAPP-D1-W511-S9`). Read from the source; the failure rows below are also measured by `test_bw4_print_pack_degrades.py`.

- BEFORE (`9590e6e5a5`): `build_pack(display_form, block, write_text=False, write_rich=False,
  thesis_bundle=read_thesis_bundle(...), peer_set=read_peer_set(...), posture=read_posture(...))`. No guard: a raising reader
  propagates out of `_print_pack`, the route returns no PDF.
- AFTER (this amendment): each read sits in its own `try`. On an exception the variable is `None` (absent), one line is written
  through `_LOG.warning("print pack <thesis bundle | peer set | posture> read failed for %s: %s: %s", ...)` (the module logger
  `segment_breakdown` uses for a failed read), and the PDF is built. `read_thesis_bundle` still calls `read_posture` internally;
  that inner call is unchanged.
- On a failed reader the PDF prints, for the section it feeds: thesis bundle -> `Management` prints `No chief executive or board
  biography has been written for this company yet.`; peer set -> `Peers` prints `No peer set is on file for this company yet.`;
  posture -> `Positioning` prints `No analyst posture is on file for this company yet.`. Each is `build_pack`'s existing absence
  sentence, so no bare heading. The figure appendix is unchanged (the readers feed no figure line).
- Route tests (`test_bw4_print_pack_degrades.py`): D1 to D3 assert the phrase `<Section> <absence sentence>` in the flattened PDF
  text; D4 asserts the appendix text equals the all-served build's; D5 asserts exactly one WARNING record naming `thesis bundle`,
  `RuntimeError` and the key; D6 asserts the all-served PDF equals `build_pack` with the same three objects.

- The PDF branch calls `read_thesis_bundle`, `read_peer_set` and `read_posture` (the same three the rich branch reads), then
  `build_pack` with `write_text=False, write_rich=False`. `read_thesis_bundle` itself also calls `read_drafted_sections`,
  `read_management` and `read_posture` (lines 4288, 4321, 4322), so `read_posture` runs twice on this route.
- Failure, the reader RAISES: BEFORE this amendment the exception propagated and the route returned no PDF. AFTER this amendment
  the pack builds with the section's absence sentence and one warning line (see the BEFORE and AFTER bullets above).
- Failure, the reader RETURNS an absent or failed object (the readers' own statuses): the pack builds. Thesis bundle with
  no management or no passage: Management prints the one sentence `No chief executive or board biography has been written for
  this company yet.` (or the CEO profile line when the roster is served). Drafted sections with a drafting status other than
  SERVED: Summary, Risks and Company description print the page's not-written sentence, or `The drafted text could not be read
  when this print was made.` when the bundle carries an error. Peer set with basis `absent`: Peers prints its reason; an empty
  peer set prints `No peer set is on file for this company yet.` Posture ABSENT: `Posture: ABSENT -- <reason>.`; READ_FAILED:
  `Posture: the read did not complete -- not evidence that no posture exists.` plus the reason; no posture object: `No analyst
  posture is on file for this company yet.`
- Latency: NOT MEASURED. The reads are served-store reads; no network or store read is made in this cell (order bounds).

## Not verified

- The deployed Lambda serves the old renderer until the round-116 redeploy (`AMGT-bw-5`). No live pack was read or built from a live store.
- The visual page layout was not looked at (no rendered image was inspected; text only).
- Which served passage is RIO LN's "CEO passage" on the live payload is not confirmed. The pack prints both served passages
  (`dossier_fields.management.value` and `drafted_sections[ceo_bio]`); surprise row `AMGT_RESAPP-D1-W511-S1`.
- The PDF route's latency and failure modes with the three added reads are not measured (surprise row `AMGT_RESAPP-D1-W511-S3`).
- Model-tab notes are inventoried only as S17 (out of scope, under the figure rows); the What-changed panel's two-version read
  is not built (S16).
- The research-notes sections (S06), the thesis pillars (S07), the charts (S08), the AI fills (S13) are not printed by this cell.
- The round-115 long-date and verbatim rules were checked on the fixtures only (F7 and the existing bu3/bv2 tests).
- The Positioning comparable label does not reproduce the page's fallback identity (surprise row `AMGT_RESAPP-D1-W511-S6`).
- AMENDMENT 2 runs at the start, on `9590e6e5a5`: the four named tests failed (`test_bw1_currency_labels.py` C3, and C7 for ICT_PM
  and RIO_LN; `test_print_format_rich.py::test_default_and_fmt_pdf_are_byte_identical_to_build_pack_itself`). The print folder
  read `4 failed, 143 passed`. After Parts 1 to 3: `1 failed, 146 passed` (the one failure is `test_av2`, which fails at base).
- The api folder is not an acceptance criterion. Five api files that call `_print_pack` or `build_pack` were run: 38 passed and
  3 failed, the three being `test_fiscal_scope_contract.py` tests on a producer file missing from this sparse worktree and on
  fiscal counts this amendment does not touch (surprise row `AMGT_RESAPP-D1-W511-S7`). The full api folder is not run here.
- The nested portal is checked out at `ff61156612`, not the `portal_ref` `3a7791c107` that Part 2 names; the fixture the tests read
  exists at the checkout (surprise row `AMGT_RESAPP-D1-W511-S8`).
