# AMGT-ca-1 receipt -- the CEO-profile reader has three states; the PDF and the rich export print from the state

Worker `0.9.0_WK_AMGT_RESAPP~520`, round 120, branch `wk-AMGT_RESAPP-520`, base `62d2e724a3` (the issuance commit).
Order: `AMGT_RESAPP.TO-AMGT-ca-1.the-ceo-profile-reader-has-three-states-and-every-surface-prints-from-the-state.md`.
Rows filed: `AMGT_RESAPP-D1-W520-S1` to `S5` (`disarm_owner` `2.0.0_SA_COO~R1` on each).

## What changed

| path | lines (+/-) |
|---|---|
| `lib/research/api/scoped_amgt.py` (`CEO_READING_NOT_WRITTEN`, the `ceo_profile_reading` docstring table, the null branch, the absence_class-null branch) | 25 / 2 |
| `lib/research/print/render_pack.py` (`_ceo_profile_sentence` with its two state sentences; `_management_passage_lines` takes the served `ceo_bio` sentences and returns a fourth value; `_management_markdown` no-bio gate and docstring) | 44 / 20 |
| `lib/research/api/tests/test_ca1_ceo_reading_three_states.py` (new: R1 to R5) | 105 new |
| `lib/research/print/tests/test_ca1_ceo_three_states.py` (new: C1 to C8, 31 cases; C1, C6 and C7 parametrised) | 243 new |
| `lib/research/api/tests/test_generation_and_pool_routes.py` (re-scope, one assertion pair) | 3 / 1 |
| `lib/research/api/tests/test_served_reasons_plain.py` (re-scope, one set) | 3 / 1 |
| `lib/research/print/tests/test_by1_reason_mapper.py` (re-scope, one constant) | 3 / 1 |
| `lib/research/print/tests/test_bx3_cleared_machine_passages.py` (re-scope, one literal) | 3 / 1 |
| `lib/research/print/tests/test_bz2_rich_management_equals_pdf.py` (re-scope, M5 for TSM_US) | 9 / 1 |
| `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` (five rows appended, 0 existing rows edited) | 125 / 0 |
| `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~520/` (this receipt and the proof instance) | new |

The fixtures `lib/research/print/tests/fixtures/bz_served_thesis_<NAME>.json` (eight names) were already in the worktree; `cmp` against `round119_prep/fixtures/` reads the same for all eight, so nothing was copied. `portal/` is untouched.

The change in one paragraph. The reader returns `NOT_WRITTEN` for a null `ceo_public_profile`, `UNREADABLE_OBJECT` only for a non-null non-dict or a status outside the enum, and `SEARCHED_NOTHING_FOUND` for a written absence whose `absence_class` is missing or null (the producer's own default, `lib/research/management/enrich.py:517` and `:536-538`; the order's pointer `enrich.py` 417-436 is the SERP loader, row S5). `_ceo_profile_sentence` reads the state from the object by calling the reader on it, not from the served `ceo_profile_reading` label, because the label in every fixture predates this cell (it reads `UNREADABLE_OBJECT` for the null profiles and for HD US and BA US); row S2. The sentence for `NOT_WRITTEN` is `CEO public profile: No CEO profile has been written for this company yet.`; for `UNREADABLE_OBJECT` it is `CEO public profile: The CEO profile could not be read.`; every other state prints as before. The export's management section prints the served `ceo_bio` sentences as the PDF does, so the no-bio sentence is not printed over a served bio (W518-S3; row S4 records the tension with the AMGT-ro-1 comment).

## Census

Step A census, the Management section of each name, rendered from the unedited head (`62d2e724a3`) and after the edit, both surfaces. Denominator: 8 names, 2 surfaces each. `CEO` is the CEO-profile line; `passage` is a cleared machine passage on the page (its line holds the CEO line's place by rule R6).

| name | PDF base | export base | PDF after | export after |
|---|---|---|---|---|
| RIO_LN | passage, no CEO line | passage, no CEO line | passage, no CEO line | passage, no CEO line |
| ICT_PM | passage, no CEO line | passage, no CEO line | passage, no CEO line | passage, no CEO line |
| GOOGL_US | passage, no CEO line | passage, no CEO line | passage, no CEO line | passage, no CEO line |
| ICICIBC_IN | passage, no CEO line | passage, no CEO line | passage, no CEO line | passage, no CEO line |
| HD_US | `CEO public profile (EDWARD P. DECKER): The CEO web search returned 10 url(s), none of them on ir.homedepot.com, so no page could be confirmed as the company's own (a redirect or short link can hide where it leads).` | same line | same line (byte-identical) | same line (byte-identical) |
| BA_US | passage, no CEO line | passage, no CEO line | passage, no CEO line | passage, no CEO line |
| KMB_US | passage, no CEO line | passage, no CEO line | passage, no CEO line | passage, no CEO line |
| TSM_US | `CEO public profile: no public profile is on file yet.` | same | `CEO public profile: No CEO profile has been written for this company yet.` | same |

Denominator: 8 of 8 names; 2 of 8 print a CEO line at the base (HD US, TSM US); 2 of 8 change (TSM US, both surfaces). `diff` of the base and after census: two lines changed, both TSM US, both surfaces.

The census is read from the rendered pack text (PyMuPDF for the PDF, the markdown for the export). The five passage names print no CEO line on either surface, before and after.

## Tests

Step A dry run, the two new test files on the unedited head (`62d2e724a3`): **8 failed, 32 passed**. The failing cases: C1 TSM_US; C2 (the pack raised `AttributeError: 'str' object has no attribute 'get'`, row S3); C3; C6 corrupt copy (same crash); C8; R1; R4 (two cases). Controls passing at the base: C4 (HD US byte-identical, BA US no line), C5, C6 (eight names and the BOGUS and served copies), C7 (eight names), R2, R3, R5 (four controls).

After the edit: **40 passed** (AC1 run, below).

Existing tests, the seven files named in the order, at the base: `2 failed, 133 passed`. The two failures are `test_generation_and_pool_routes.py::test_11_coverage_is_P1_over_the_association_keys_newest_first` and `::test_15_the_model_slice_is_the_landed_blocks_own_fiscal_rows`; they fail at the base and are not touched by this cell. After the edit and the re-scopes below, the same seven files plus the two new files read `2 failed, 173 passed` (the same two failures).

Print folder, after the edit: `1 failed, 347 passed` with the one known failure (AC2). The order's recorded base reads `1 failed, 316 passed`; the print folder was not re-run at the base in this session.

## Tests re-scoped

Five assertions pinned the old words of a null or non-dict profile. Each is re-scoped to the new state, old and new written out:

1. `lib/research/print/tests/test_by1_reason_mapper.py` `CEO_FIXED` (site `management-ceo-profile`, a null profile): old `CEO public profile: no public profile is on file yet.`; new `CEO public profile: No CEO profile has been written for this company yet.`
2. `lib/research/api/tests/test_generation_and_pool_routes.py` `test_13b`, the last block: old `reading(None)` asserted `UNREADABLE_OBJECT` with basis `the object is not a dict`; new `reading("corrupt")` asserts the same two values (a non-null non-dict stays the failed read). The null case is `NOT_WRITTEN` in R1 of the new file.
3. `lib/research/api/tests/test_served_reasons_plain.py` `test_ceo_reading_reason_is_plain_for_a_stored_legacy_basis`: old `{"UNREADABLE_OBJECT", "SEARCHED_NOTHING_FOUND", "SEARCHED_LINKS_UNREADABLE"}`; new `{"SEARCHED_NOTHING_FOUND", "SEARCHED_LINKS_UNREADABLE"}` (the BA shape with no `absence_class` is a written absence).
4. `lib/research/print/tests/test_bz2_rich_management_equals_pdf.py` M5, TSM_US only: the recorded base line `CEO public profile: no public profile is on file yet.` is replaced by `CEO public profile: No CEO profile has been written for this company yet.`; every other line of the recorded base is compared unchanged, and the replacement is asserted to match exactly once.
5. `lib/research/print/tests/test_bx3_cleared_machine_passages.py` M10 (GOOGL_US, every machine block withheld): old literal `CEO public profile: no public profile is on file yet.`; new literal `CEO public profile: No CEO profile has been written for this company yet.` (the line's place and count assertions are unchanged).

## Page

The page is not edited. `portal/src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx` `CeoProfile` (lines 188-246) handles six known words and falls through to one fixed line for any other. For `NOT_WRITTEN` the page prints `CEO public profile{who}: no public profile is on file yet.` with `data-ceo-profile="NOT_WRITTEN"` and the basis in `data-ceo-profile-basis`, so the new word shows the old sentence, not the new one. For the narrowed `UNREADABLE_OBJECT` the page prints the same fallback sentence with `data-ceo-profile="UNREADABLE_OBJECT"`: a failed read still shows the words the ruling says are wrong for it. For a written absence with no class, once the reader is served (AMGT-ca-5), HD US and BA US change on the page from the fallback to `CEO public profile{who}: searched, nothing found -- <basis>`. The issuer carries the page's wording and the `types.ts` reading union to the CTO; `ManagementBlock.ceo_profile_reading` is not edited here.

## Not verified

- The deployed Lambda serves the old renderer and the old reader until `AMGT-ca-5`; nothing here is deployed. The served `ceo_profile_reading` label in every fixture is the old reader's output and stays stale until then (row S2, ARMED, disarm owner the issuer).
- The whole `lib/research/api` folder was not run in this sparse worktree; only the seven named files and the two new ones. The issuer runs the whole print and api folders in the full tree.
- `RESOLVED` with no `url` still reads `UNREADABLE_OBJECT` (unchanged from the base; it is outside the three states' definitions), and an `ABSENT` with an unknown `absence_class` value still reads `UNREADABLE_OBJECT`. Both are judgments the order did not name; neither occurs in the eight fixtures.
- The page's wording (`ExecManagementTab.tsx`) and the `types.ts` reading union were not changed; the page's behaviour is described above from its source, not run in a browser.
- The AC2 base count was not re-measured in this session (`1 failed, 316 passed` is the order's recorded base).
