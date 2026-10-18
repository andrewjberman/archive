# CD1 receipt -- AMGT-cd-1 (0.9.0_WK_AMGT_RESAPP~524, round 122)

Order: `AMGT_RESAPP.TO-AMGT-cd-1.the-pdf-and-export-ceo-sentence-has-a-branch-for-every-known-state`
Base: `db4fbe1394` (issuance commit). Branch `wk-AMGT_RESAPP-524`. Local only; no push.

## What changed

- `lib/research/print/render_pack.py` -- 28 insertions, 4 deletions (`git diff --stat`). Region: the CEO-profile block,
  lines 992 to 1042: the two existing state sentences, four fixed sentences (one per falling-through state), the
  unknown-reading sentence, the `_CEO_PROFILE_FIXED_BY_READING` map, and `_ceo_profile_sentence`. No other region edited.
- `lib/research/print/tests/test_cd1_ceo_sentence_per_state.py` -- new, 312 lines. S1 to S8 as the order names them;
  expectations hand-written from the order's rule and the base lines recorded at `db4fbe1394`.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` -- two rows appended
  (`AMGT_RESAPP-D1-W524-S1`, `AMGT_RESAPP-D1-W524-S2`), 52 added lines; no existing row edited.
- `lib/research/print/tests/fixtures/` -- no file added. The eight `bz_served_thesis_<NAME>.json` fixtures were already
  present and are byte-identical (`cmp`) to `round119_prep/fixtures/`.
- This receipt and the proof instance (second commit).

## Census

Reader state per shape, the reader's `reason` (scoped_amgt.ceo_profile_reading, unedited at db4fbe1394), and the line
printed BEFORE and AFTER the edit. The denominator is 4 falling-through states x 4 non-plain basis kinds (16 cases),
plus one plain basis per state (4 cases), plus one status-token basis per state (4 rows). The census script is
`.scratch/cd1_census.py`; its BEFORE and AFTER outputs are `.scratch/cd1_census_before.txt` and `.scratch/cd1_census_after.txt`.

Basis kinds: `path` = `s3://opal-data-harvest/x/y.json`; `order-id` = `AMGT-rj-11 has not landed one`;
`upper-snake` = `SEARCH_RESULT_LIST was empty`; `too-long` = a basis of more than 300 characters; `status-token` =
`ABSENT, the CEO web search returned 10 url(s).`

| reader state | basis kind | reader reason | line BEFORE | line AFTER |
|---|---|---|---|---|
| SEARCHED_NOTHING_FOUND | plain | the basis, verbatim | `CEO public profile (Jane Doe): The CEO web search returned 10 url(s), none of them on ir.homedepot.com.` | identical |
| SEARCHED_NOTHING_FOUND | path / order-id / upper-snake / too-long | the basis, verbatim (non-plain) | `CEO public profile (Jane Doe): no public profile is on file yet.` | `CEO public profile (Jane Doe): The CEO web search ran and found no profile page for this company.` |
| SEARCHED_NOTHING_FOUND | status-token | rebuilt plain by `_plain_searched_reason` | `...: The CEO web search returned 10 url(s), but none of them was a page on the company's own site.` | identical |
| SEARCHED_LINKS_UNREADABLE | plain | the basis, verbatim | `CEO public profile (Jane Doe): The CEO web search returned 3 url(s), none of them could be confirmed.` | identical |
| SEARCHED_LINKS_UNREADABLE | path / order-id / upper-snake / too-long | the basis, verbatim (non-plain) | `...: no public profile is on file yet.` | `CEO public profile (Jane Doe): The CEO web search returned links, but none could be confirmed as the company's own page.` |
| SEARCHED_LINKS_UNREADABLE | status-token | rebuilt plain by `_plain_searched_reason` | `...: The CEO web search returned 10 url(s), but none could be confirmed as the company's own page.` | identical |
| NOT_SEARCHED | plain | the basis, verbatim | `CEO public profile (Jane Doe): The CEO search was not run for this company.` | identical |
| NOT_SEARCHED | path / order-id / upper-snake / too-long | the basis, verbatim (non-plain) | `...: no public profile is on file yet.` | `CEO public profile (Jane Doe): No CEO web search was run for this company.` |
| NOT_SEARCHED | status-token | the basis, verbatim (NO rebuild on this branch) | `CEO public profile (Jane Doe): ABSENT, the CEO web search returned 10 url(s).` | identical (see Not verified) |
| SEARCH_FAILED | plain | the basis, verbatim | `CEO public profile (Jane Doe): The CEO web search did not complete, so no result is shown.` | identical |
| SEARCH_FAILED | path / order-id / upper-snake / too-long | the basis, verbatim (non-plain) | `...: no public profile is on file yet.` | `CEO public profile (Jane Doe): The CEO web search did not complete.` |
| UNREADABLE_OBJECT | string `corrupt`, or a BOGUS status | none (state branch) | `CEO public profile: The CEO profile could not be read.` | identical |
| NOT_WRITTEN | null, or an absent key | none (state branch) | `CEO public profile: No CEO profile has been written for this company yet.` | identical |
| CONFIRMED, url set | n/a | the basis | `CEO public profile (Jane Doe): https://x.com/ceo` | identical |
| unknown word (monkeypatched reader) | n/a | none | fell through to the fixed fallback | `CEO public profile (Jane Doe): the state of this profile is not recognised by this document.` |
| CONFIRMED, no url (monkeypatched reader) | n/a | none | fell through to the fixed fallback | the third sentence |

Split notes. (1) For SEARCHED_NOTHING_FOUND, SEARCHED_LINKS_UNREADABLE and the UNREADABLE fallback, the reader rebuilds
a basis that carries a status token (`ABSENT`, `REFUSED`, `NOT_SERVED`, `not served`, `unsupported`) as a plain
sentence from the URL count. Such a reading has no plain/non-plain split: it always prints the rebuilt sentence. (2)
SEARCH_FAILED is read only from a basis that starts with its fixed prefix; a status-token basis reads as
SEARCHED_NOTHING_FOUND, so no SEARCH_FAILED status-token row exists. (3) NOT_SEARCHED's reason is the basis verbatim,
so its plain/non-plain split is the basis's own (see Not verified, row S1).

Eight fixture names (AFTER, read from both formats): the six null names print the not-written line where no passage
holds the place (RIO_LN, ICT_PM, GOOGL_US, ICICIBC_IN, KMB_US, TSM_US: TSM_US prints it; the other five have a cleared
passage holding the place, as at the base); HD_US prints its base line byte for byte; BA_US prints no CEO line on either
surface (a passage holds the place, as at the base). Delta 0 on all eight (test S5).

## Tests re-scoped

none.

The phrase `no public profile is on file yet` is in the print tests only in `test_bz2_rich_management_equals_pdf.py`
(M5, already re-scoped at AMGT-ca-1 to the NOT_WRITTEN line for TSM_US, which the edit does not move), and in comments of
`test_by1_reason_mapper.py` and `test_bx3_cleared_machine_passages.py`. No print or api test pins the old fallback for a
non-plain reason.

## Test runs

- New file, base (unedited `db4fbe1394` render_pack): `23 failed, 16 passed`. The 23 are S1 (16), S3 (2), S6 (4) and S8 (1).
- New file, after the edit: `39 passed in 11.09s`.
- Existing CEO-related tests, base and after (`test_by1_reason_mapper.py`, `test_bz2_rich_management_equals_pdf.py`,
  `test_ca1_ceo_three_states.py`, `test_bx3_cleared_machine_passages.py`, api `test_ca1_ceo_reading_three_states.py`,
  api `test_served_reasons_plain.py`, api `test_ceo_reading_new_basis.py`): `143 passed` at base, `143 passed` after.
- AC1 literal: `39 passed in 12.05s`, exit=0.
- AC2 literal: one FAILED line, `test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words`,
  and `1 failed, 471 passed, 4 warnings in 213.26s`. 471 = the base 432 plus the 39 new tests.

## Not verified

- The deployed Lambda serves the old renderer until AMGT-cd-4. Nothing here is served.
- The whole api folder is not run in this sparse worktree. The issuer runs it in the full tree.
- Test S7 (no state word, path or id in a printed line) passes at the base as well. It guards against leakage, and the
  base's non-plain lines carried no such token; S1, S3, S6 and S8 are the ones that discriminate the defect.
- The NOT_SEARCHED status-token shape (row `AMGT_RESAPP-D1-W524-S1`): a plain reason that carries the word ABSENT prints
  it. Rule (a) (plain prints as served) and rule (c) (no state word) disagree for this shape. This worker kept rule (a)
  and changed no plain branch. No eight-name fixture carries it.
- Rule (c) forbids `has been written` in a fixed sentence, while the NOT_WRITTEN sentence carries it. This worker read
  rule (c) as applying to the four fixed sentences and the third sentence; NOT_WRITTEN keeps its own sentence (test S4).
- No portal file touched; no push; no DEV or PROD write. `scoped_amgt.py`, `render_print.py`, `long_day.py` untouched.
