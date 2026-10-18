# BV2 receipt -- AMGT-bv-2 (0.9.0_WK_AMGT_RESAPP~509)

Task order: `AMGT_RESAPP.TO-AMGT-bv-2.rich-export-dates-and-verbatim-quotes` (round 115, decomposition s.124; CTO round-114 analysis items 2 and 3, W506-S4 and W506-S5).
Base: `e58e97c92e` (issuance commit). Branch `wk-AMGT_RESAPP-509`, worktree `C:/dev/wk-resapp-509`. Local only; nothing pushed.

## Quote census

Read of `lib/research/print/render_pack.py` at the base. Denominator: 37 functions read, 30 blocks listed, 6 blocks exempt. Machine form: `lib/research/print/tests/fixtures/bv2_quote_blocks.json`.

Exempt (verbatim source quotation) is true only for a served sentence that IS the filing's own text (`generated` false and `quoted_spans` equal to `[text]`, the `drafting_build` filing-sentence branch), or an evidence passage printed as the source's own words. A quoted span inside a drafted (generated true) sentence is the system's prose, not a block.

| ID | Surface, function (base line) | Prints | Verbatim | Exempt | Reason |
|---|---|---|---|---|---|
| K01 | pack, build_pack (735) | title, company name [security] | false | false | system heading from a served name |
| K02 | pack, build_pack (736) | Printed <run date> | false | false | system words |
| K03 | pack, _plain_figure_line via build_pack (743) | header figure lines | false | false | served data field in words |
| K04 | pack, _plain_figure_line via build_pack (749) | fiscal-year figure lines | false | false | served data field in words |
| K05 | pack, _print_drafted, recommendation (656) | filing-sentence | true | true | the sentence is the filing's own words |
| K06 | pack, _print_drafted, recommendation (656) | drafted sentence | false | false | model prose |
| K07 | pack, _description_line (763) | description figure (CIE_DES) | false | false | vendor data field value, not a quotation block |
| K08 | pack, build_pack company description (769) | filing-sentence | true | true | the sentence is the filing's own words |
| K09 | pack, build_pack company description (769) | drafted sentence | false | false | model prose |
| K10 | pack, _print_drafted, investment_thesis (656) | filing-sentence | true | true | the sentence is the filing's own words |
| K11 | pack, _print_drafted, investment_thesis (656) | drafted sentence | false | false | model prose |
| K12 | pack, _print_drafted, risks (656) | filing-sentence | true | true | the sentence is the filing's own words |
| K13 | pack, _print_drafted, risks (656) | drafted sentence | false | false | model prose |
| K14 | pack, build_pack / _print_drafted (659) | static headings, NOT_WRITTEN, error line | false | false | system words |
| X01 | rich, build_rich_text (1577) | title, intro, section headings | false | false | system words |
| X02 | rich, _figures_table header (991) | header rows, render_figure_line cell | false | false | served data field, provenance renderer |
| X03 | rich, _header_description_lines (1081) | Description: served text or ABSENT | false | false | served description field, not a quotation block |
| X04 | rich, _figures_table fiscal (991) | fiscal rows | false | false | served data field |
| X05 | rich, _forecast_table (1466) | forecast rows | false | false | served data field |
| X06 | rich, _drafted_section_markdown (1022) | filing-sentence | true | true | the sentence is the filing's own words |
| X07 | rich, _drafted_section_markdown (1022) | drafted sentence | false | false | model prose |
| X08 | rich, _drafted_section_markdown (1032) | `> <id> -- accession -- location` | false | false | citation metadata composed by the system |
| X09 | rich, _drafted_section_markdown (1038) | `> "<evidence passage>"` | true | true | an evidence passage printed as the source's own words |
| X10 | rich, _drafted_section_markdown (1017) | Description: ABSENT -- reason | false | false | system reason text |
| X11 | rich, _undrafted_thesis_markdown (1061) | drafting reason lines | false | false | system reason text |
| X12 | rich, _management_markdown (1117) | officer table, CEO reading | false | false | served officer fields and a system reading |
| X13 | rich, _peers_markdown (1163) | peer tables and ABSENT lines | false | false | served peer data |
| X14 | rich, _posture_markdown (1241) | verdict, claims, cites | false | false | the judge's own claim text and cite ids |
| X15 | rich, Model Notes (1634) | ABSENT, REFUSED, driver chart lines | false | false | system footnote text |
| X16 | rich, Source line (1651) | vintages, generated_at | false | false | metadata timestamps |

Functions on no print path (read, not called by `build_pack` or `build_rich_text`): `_refuse_verdicts`, `_model_cases_markdown`, `_model_case_line`, `_case_currency`, `_refused_figures_markdown`.

Finding: `build_pack` prints NO evidence passage. The only verbatim source text on the pack path is the filing-sentence kind (K05, K08, K10, K12). The CTO ruling's premise that the pack prints quoted passages holds for the rich export (X09) only. Row `AMGT_RESAPP-D1-W509-S1`.

## Test runs

Unedited head (`render_pack.py` identical to `e58e97c92e`, `git diff --stat` empty), run once:

```
python -m pytest lib/research/print/tests/test_bv2_rich_dates_and_quotes.py -q -p no:cacheprovider --color=no
2 failed, 3 passed in 8.43s
```

- Q1 FAILED: the long-form presence check, `assert "October 17th, 2026" in text`; the export's Source line still read `vintages 2026-10-17T01:02:03Z`. The ISO check was not reached in that run.
- Q2 FAILED: the PDF arm, the verbatim passage was long-formed in the drafted sentence.
- Q3, Q4, Q5 PASSED.

Two assertions were edited after this run, both after the product edit and before AC1: Q1's second non-vacuity line (`period ending December 31st, 2026`, which the export does not print; replaced by `EPS (consensus estimate)`), and Q2's day detector (`ISO_DAY` replaced by the digit-bounded `ISO_DAY_BOUNDED`, because the accession `0001234567-12-150001` contains the day-shaped run `4567-12-15`). The check of Q1's ISO day and Q3's day mapping are unchanged.

After the edit:

- AC1: `timeout 300 python -m pytest lib/research/print/tests/test_bv2_rich_dates_and_quotes.py -q -p no:cacheprovider --color=no` gives `5 passed in 6.96s`, exit 0.
- AC2: `timeout 580 python -m pytest lib/research/print/tests -q -p no:cacheprovider --color=no` gives `FAILED lib/research/print/tests/test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` and `1 failed, 125 passed in 25.42s`. That failure is the pre-existing one the order names: the header line for the share price lacks the segment `- date not stored with this figure`, a header-wording mismatch that this cell does not touch.
- Control: `test_bu3_pack_long_dates.py` run from the new file (Q4) gives `7 passed`.

## What changed

- `lib/research/print/render_pack.py`: 47 insertions, 15 deletions. Digit-bounded day pattern (`_DAY_IN_TEXT`); `_Verbatim` line marker; `_is_source_quotation` (the filing-sentence rule); `_wrap(..., verbatim=False)` and `Paginator.line(..., verbatim=False)`; `_served_sentence_items`; `_print_drafted` and the company-description loop print a filing sentence verbatim; `_drafted_section_markdown` carries the filing sentence and the passage as `_Verbatim`; `build_rich_text` applies `_long_days` to every other line of the finished document, once, before the write.
- `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py`: 181 lines, new. Q1 to Q5.
- `lib/research/print/tests/fixtures/bv2_quote_blocks.json`: 52 lines, new. The census.
- `lib/research/print/tests/fixtures/bv2_passage_RIO_LN.json`: 38 lines, new. The Q2 drafted sections (own fixture, ISO day `2026-03-01` inside the passage).
- `lib/research/print/tests/fixtures/bv2_rich_text_base_RIO_LN.txt`: 53 lines, new. The base export, recorded from the unedited renderer before the edit.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 78 insertions, three rows (`AMGT_RESAPP-D1-W509-S1` to `-S3`).
- This receipt and the proof-of-spec instance in the same deliverables folder.

Against the base export, seven lines differ, each by the day rewrite only: the header's CRNCY and PX_LAST `as of` cells, the IS_EPS 2025 and 2026E `as of` cells, the recommendation and risks sentences, and the Source line's vintages. No line of the base export that carried no date changed.

## What scoped_amgt does with the rich text

Read only, `lib/research/api/scoped_amgt.py` lines 7866 to 7889. For `fmt=rich` it calls `build_rich_text(display_form, block, thesis_bundle=read_thesis_bundle(...), peer_set=read_peer_set(...), posture=read_posture(...), description=read_description(...))`, opens the returned `.md` as UTF-8, and returns the body unchanged as `text/markdown; charset=utf-8` with status 200. It does no date handling and no post-processing, so the change in `render_pack.py` reaches the served body with no change to `scoped_amgt.py`.

## Not verified

- The deployed scoped API Lambda serves the old renderer until `AMGT-bv-5`. No live export was read or fetched.
- The live packs of BA, HD and KMB were not read. Whether they print quoted passages in the pack path is unverified; the census finds none at this base (row `-S1`).
- The Q1 and Q2 fixtures are synthetic. The RIO bundle is built from the bu3 fixture by `_rio_bundle`, not a landed bundle.
- PDF content was checked by text extraction only (PyMuPDF 1.28.2 for the PDF, pypdf layout for the `.txt`), not visually.
- Q3 compares days on both sides, because the base export carries full ISO timestamps that the day-only rule cannot restore (row `-S2`). The recorded base text is unedited.
- The av2 test failure is pre-existing and was not fixed; it is outside this order.
- No deploy, no push, no DEV or PROD touch, no portal change.
