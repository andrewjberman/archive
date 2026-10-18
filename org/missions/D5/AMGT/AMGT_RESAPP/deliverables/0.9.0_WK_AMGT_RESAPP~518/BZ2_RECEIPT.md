# AMGT-bz-2 receipt -- re-seat of 0.9.0_WK_AMGT_RESAPP~518 (round 119)

Scope: the receipt for the cell the first seat built (commit e65cd904da) and proved (ea2a260b41). This re-seat changed no product file; it writes this receipt, the base snapshot its base citations resolve to, the census script, and one surprise row. Base: 8e81e269f7.

Citation convention: every `path:line` is repo-relative at the worktree HEAD of this commit. A base-only line is cited as `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:<line>`, a byte copy of `git show 8e81e269f7:lib/research/print/render_pack.py`. `lib/research/api/scoped_amgt.py` is byte-identical between 8e81e269f7 and HEAD (`git diff --quiet` exits 0), so its citations hold at base as well.

## What changed

- `lib/research/print/render_pack.py` (e65cd904da: +55 -14; the file is 2379 lines at HEAD). Removes `_CEO_READING_WORDS` (base snapshot `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:1514-1521`). Adds `_LinesOut` (`lib/research/print/render_pack.py:1707-1718`) and `_management_passage_lines` (`lib/research/print/render_pack.py:1721-1744`). Rewrites the Management block of `_management_markdown` (`lib/research/print/render_pack.py:1747`; passages first at `:1765-1766`; CEO-profile gate at `:1799-1802`; no-bio gate at `:1803-1804`). The PDF path is not in the diff hunks: `_ceo_profile_sentence` (`lib/research/print/render_pack.py:970-978`), `_print_management` (`lib/research/print/render_pack.py:1083-1121`) and `build_pack` (`lib/research/print/render_pack.py:1207`, call at `:1322`) are unchanged.
- `lib/research/print/tests/test_bz2_rich_management_equals_pdf.py` (new, 207 lines): M1 x8, M2, M3, M4 x8, M5 control x8.
- `lib/research/api/tests/test_bz2_rich_route_management_input.py` (new, 124 lines): M6 x8 (control), M7 x8.
- `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py` (+6): the Q3 re-scope, see Tests re-scoped.
- `lib/research/print/tests/fixtures/`: `bz_served_thesis_{RIO_LN 1436, ICT_PM 1755, GOOGL_US 1889, ICICIBC_IN 1685, HD_US 2679, BA_US 2887, KMB_US 2940, TSM_US 1904}.json` (eight new files; line counts in brackets) and `bz2_pdf_management_base.json` (264 lines).
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: e65cd904da +75 (rows W518-S1 to S3); commit 749405db0b +25 (row W518-S4, filed by this re-seat).
- This receipt's commit: `BZ2_RECEIPT.md`, `base_8e81e269f7/render_pack.py` (2280 lines, the snapshot), and `census_bz2.py` (82 lines; reruns the census below).

## Cause

Question: why the rich export prints `CEO public-profile reading: the object could not be read` where the PDF prints the CEO profile sentence.

Answer: the export printed the served reading LABEL through a words table and never called the PDF's sentence builder or its passage printers. The label is the reader's catch-all for an object it cannot classify. Both routes read the same management object; they differ in what they print from it.

Each claim, checked at the line cited:

1. Both routes read one management object. `read_thesis_bundle` sets `bundle["management"] = read_management(...)` (`lib/research/api/scoped_amgt.py:4321`; `def read_thesis_bundle` at `lib/research/api/scoped_amgt.py:4214`). The rich branch of `_print_pack` calls it at `lib/research/api/scoped_amgt.py:7878` and the pdf branch at `lib/research/api/scoped_amgt.py:7928`. Each passes the bundle as `thesis_bundle`: rich at `lib/research/api/scoped_amgt.py:7902` into `build_rich_text`, pdf at `lib/research/api/scoped_amgt.py:7947` into `build_pack`. Inside the builders: `lib/research/print/render_pack.py:2301` (`_management_markdown(thesis_bundle)`) and `lib/research/print/render_pack.py:1322` (`_print_management(p, thesis_bundle or {}, drafted)`). At base the same calls sit at `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:2202` and `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:1288`. Verified.

2. The PDF prints the profile sentence. `_ceo_profile_sentence` (`lib/research/print/render_pack.py:970`) reads `ceo_public_profile` (`lib/research/print/render_pack.py:971`) and `ceo_profile_reading` (`lib/research/print/render_pack.py:972`), prints the URL only when the reading is CONFIRMED with a URL (`lib/research/print/render_pack.py:974-975`), and otherwise prints the reading's reason through `_plain_reason` (`lib/research/print/render_pack.py:977`) with the fixed fallback "no public profile is on file yet". `_print_management` (`lib/research/print/render_pack.py:1083`) calls it at `lib/research/print/render_pack.py:1116`, only when management is SERVED (`lib/research/print/render_pack.py:1111`) and no cleared passage printed (`lib/research/print/render_pack.py:1115`). With nothing printed, the no-bio sentence prints at `lib/research/print/render_pack.py:1121`. At base: `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:936-944` (sentence) and `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:1077-1082` (gate and call). Verified.

3. The export at base printed the reading word. The words table maps `UNREADABLE_OBJECT` to "the object could not be read" (`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:1514-1521`, the entry at `:1520`). `_management_markdown` at `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/base_8e81e269f7/render_pack.py:1656` read only `ceo_profile_reading.reading` (`:1701`) and printed `CEO public-profile reading: <word>` after the roster table (`:1702-1705`). Base `:1656-1706` holds no `ceo_public_profile` reference, no call to `_ceo_profile_sentence` and no `_print_passage` call; the base references to those names are at `:937` (inside the sentence builder), `:1073` and `:1082` (inside `_print_management`). Verified by grep of the snapshot.

4. The reader labels a null or unclassified profile `UNREADABLE_OBJECT`. `ceo_profile_reading` (`lib/research/api/scoped_amgt.py:4912`) returns `UNREADABLE_OBJECT` for a non-dict profile (`lib/research/api/scoped_amgt.py:4938-4944`; `reading_basis` "the object is not a dict", `reason` None). Six names carry a null `ceo_public_profile`: `lib/research/print/tests/fixtures/bz_served_thesis_RIO_LN.json:1206`, `lib/research/print/tests/fixtures/bz_served_thesis_ICT_PM.json:1356`, `lib/research/print/tests/fixtures/bz_served_thesis_GOOGL_US.json:1711`, `lib/research/print/tests/fixtures/bz_served_thesis_ICICIBC_IN.json:1295`, `lib/research/print/tests/fixtures/bz_served_thesis_KMB_US.json:1879`, `lib/research/print/tests/fixtures/bz_served_thesis_TSM_US.json:1401`. RIO_LN's reading block is at `lib/research/print/tests/fixtures/bz_served_thesis_RIO_LN.json:1200-1205`. HD US and BA US carry a dict with status ABSENT and a query set but no `absence_class`; no branch in `lib/research/api/scoped_amgt.py:4965-4988` matches, so both fall to the final return at `lib/research/api/scoped_amgt.py:4989-4996`, with `reading_basis` "status=ABSENT query=set absence_class=None" (`lib/research/print/tests/fixtures/bz_served_thesis_HD_US.json:1682`; `lib/research/print/tests/fixtures/bz_served_thesis_BA_US.json:1820`). Their `reason` is the producer's basis sentence, passed through `_plain_searched_reason` (`lib/research/api/scoped_amgt.py:4897-4909`; a plain basis is returned verbatim at `lib/research/api/scoped_amgt.py:4902-4903`). The profile objects: `lib/research/print/tests/fixtures/bz_served_thesis_HD_US.json:1686-1695` (status at `:1692`) and `lib/research/print/tests/fixtures/bz_served_thesis_BA_US.json:1824-1830` (status at `:1830`). Verified.

5. Consequence, measured in Census: the export at base carried the label's words for 8 of 8 names, while the PDF carried the sentence for the same object. At HEAD the export prints the PDF's words for all eight.

First-seat findings (a) to (d): each holds at the lines above; none is struck. One correction: the first seat's docstring in `lib/research/api/tests/test_bz2_rich_route_management_input.py:1-2` says M6 shows that both routes read "through the SAME reader". M6 does not show that (see Not verified, item 3). The shared reader is shown by claim 1 alone.

## Census

Method: `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~518/census_bz2.py` builds, for each of the eight fixtures, the PDF (`build_pack`) and the rich text (`build_rich_text`) with run date 2026-10-18, once from the base snapshot and once from HEAD, and reads each Management section. One deviation: the base snapshot sits outside `lib/research/print/`, so its `FONT_DIR` is pointed at the HEAD fonts (the single line `base_rp.FONT_DIR = head_rp.FONT_DIR`). Denominator: 8 names.

| Name | Served `ceo_public_profile` (Cause 4) | PDF Management: CEO-profile line (base = HEAD) | PDF cleared-passage labels (base = HEAD) | Export at base 8e81e269f7 | Export at HEAD | Roster rows base / HEAD (served officers) |
|---|---|---|---|---|---|---|
| RIO_LN | null | none (a passage holds the place) | 1 | `CEO public-profile reading: the object could not be read` | no CEO line; the same 1 passage label as the PDF | 11 / 11 (11) |
| ICT_PM | null | none (passages) | 2 | `CEO public-profile reading: the object could not be read` | no CEO line; the same 2 labels | 24 / 24 (24) |
| GOOGL_US | null | none (passages) | 3 | `CEO public-profile reading: the object could not be read` | no CEO line; the same 3 labels | 7 / 7 (7) |
| ICICIBC_IN | null | none (passages) | 2 | `CEO public-profile reading: the object could not be read` | no CEO line; the same 2 labels | 16 / 16 (16) |
| HD_US | dict, ABSENT, query set | `CEO public profile (EDWARD P. DECKER): The CEO web search returned 10 url(s), none of them on ir.homedepot.com, so no page could be confirmed as the company's own (a redirect or short link can hide where it leads).` (the PDF wraps it over three lines) | 0 | `CEO public-profile reading: the object could not be read` | the same sentence, on one line, as the PDF's words | 10 / 10 (10) |
| BA_US | dict, ABSENT, query set | none (the team-view passage holds the place) | 1 | `CEO public-profile reading: the object could not be read` | no CEO line; the same 1 label | 12 / 12 (12) |
| KMB_US | null | none (passages) | 1 | `CEO public-profile reading: the object could not be read` | no CEO line; the same 1 label | 14 / 14 (14) |
| TSM_US | null | `CEO public profile: no public profile is on file yet.` | 0 | `CEO public-profile reading: the object could not be read` | `CEO public profile: no public profile is on file yet.` | 32 / 32 (32) |

Totals (denominator 8 names in each):
- The export carries `could not be read`: 8 of 8 at base; 0 of 8 at HEAD.
- The PDF Management section is identical at base and HEAD: 8 of 8 (`base PDF == head PDF`).
- Export and PDF carry the same words for the CEO-profile line and the passages: 8 of 8 (test M1 x8 in the AC1 run below; the HD line is equal in words, not in wrapping).
- Roster rows equal the served officer count: 8 of 8.

AC1 run at HEAD (this re-seat): `python -m pytest lib/research/print/tests/test_bz2_rich_management_equals_pdf.py lib/research/api/tests/test_bz2_rich_route_management_input.py -q` reads `42 passed in 25.26s`, exit 0.

## Tests re-scoped

One re-scope, in `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py`, test Q3 (`def test_Q3_control_inverse_of_export_equals_base_export_recorded_at_base_head` at `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py:147`).
- Old assertion (before e65cd904da): the expected list is the recorded base export with one line mapped, `expected = [new_line if ln == old_line else ln for ln in recorded]` (`lib/research/print/tests/test_bv2_rich_dates_and_quotes.py:171`), then `assert mapped == expected` (`lib/research/print/tests/test_bv2_rich_dates_and_quotes.py:178`), with no insertion.
- New assertion (HEAD `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py:172-177`): after the line mapping, `[no_bio, ""]` is inserted after the reason line and its blank, at `at = expected.index("no management object for this name") + 2` (`lib/research/print/tests/test_bv2_rich_dates_and_quotes.py:176`; `no_bio` at `:175` is "No chief executive or board biography has been written for this company yet."). The sentence is the PDF's own (`lib/research/print/render_pack.py:127`; the PDF prints it at `lib/research/print/render_pack.py:1121`).
- Why: the Q3 bundle (`_rio_bundle`, `lib/research/print/tests/test_bv2_rich_dates_and_quotes.py:53-62`) carries no management object, so management is ABSENT and, with no passage, the export now prints the no-bio sentence as the PDF does (`lib/research/print/render_pack.py:1803-1804`).
- Result at HEAD: `test_bv2_rich_dates_and_quotes.py` runs `5 passed` (this re-seat).
- No other test was re-scoped. The first seat's pre-edit count (26 failed, 16 passed) is recorded in e65cd904da and was not re-run here.

## Not verified

1. The deployed Lambda serves the old renderer until AMGT-bx-5 (carried from the order's section 5; not checked here).
2. The api folder and the whole print folder were not run in this re-seat; the issuer runs them in the full tree. The first seat recorded `275 passed` with one known failure (`test_av2_export_equals_page.py`) in ea2a260b41; not re-run here.
3. M6 is a control that cannot fail on the reader it names. Its stub (`lib/research/api/tests/test_bz2_rich_route_management_input.py:56`) returns the same bundle to both routes, and the spies (`lib/research/api/tests/test_bz2_rich_route_management_input.py:85-105`) compare that object with itself, so equality holds by construction. The route-level reading rests on Cause claim 1 (code), not on M6. M6's base run was not repeated here.
4. M7 (`lib/research/api/tests/test_bz2_rich_route_management_input.py:109-124`) raises at `read_thesis_bundle` (`lib/research/api/tests/test_bz2_rich_route_management_input.py:115`), one call above `read_management` (`lib/research/api/scoped_amgt.py:4321`). The management reader's own raise is not run; the guard both routes share is exercised (`lib/research/api/scoped_amgt.py:7877-7881` and `lib/research/api/scoped_amgt.py:7927-7931`). Recorded as `AMGT_RESAPP-D1-W518-S4` in `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`, committed as 749405db0b.
5. The portal's use of the served label `UNREADABLE_OBJECT` was not verified (row `AMGT_RESAPP-D1-W518-S2`); the label remains in the management object.
6. The export's no-bio branch (management not SERVED and no passage) is reached by none of the eight fixtures; only the re-scoped Q3 test reaches it. The export does not count served `ceo_bio` sentences that the PDF counts (row `AMGT_RESAPP-D1-W518-S3`, inert for the eight).
7. The census reads the 2026-10-18 fixtures only: no live read, no AWS, no HTTP, no vendor call.
8. First-seat row S1 (BA US premise): confirmed by the census (BA US: one passage label in both PDF and export, no CEO-profile line in either).
