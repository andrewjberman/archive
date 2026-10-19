# CE1 RECEIPT -- AMGT-ce-1 (round 123), worker 0.9.0_WK_AMGT_RESAPP~525

Order: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-ce-1.a-reason-carrying-a-reader-status-word-is-not-plain.md`
Base: worktree HEAD `2fe324e11e` at the cut (issuance `613ec8aef1` is its ancestor; row AMGT_RESAPP-D1-W525-S2).
Branch: `wk-AMGT_RESAPP-525`.

## What changed

- `lib/research/print/render_pack.py`: 3 lines inserted in `_NOT_PLAIN_PATTERNS` (one comment line, one two-line entry). Tuple length 10 at the base, 11 now. Nothing else in the file moved (`git diff --numstat`: 3 insertions, 0 deletions).
- `lib/research/print/tests/test_ce1_status_word_screen.py`: new, 223 lines, tests T1 to T8.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 2 rows appended after the last row (`AMGT_RESAPP-D1-W525-S1`, `AMGT_RESAPP-D1-W525-S2`); 51 insertions, 0 deletions.
- This receipt and the proof instance, in this deliverables folder.

## Census

`_ceo_profile_sentence` on a NOT_SEARCHED profile (status ABSENT, query null, ceo_name Jane Doe) whose basis is `<WORD>, the CEO web search returned 10 url(s).`, measured by `.scratch/ce1_probe.py` at the base and after the edit:

| word | BEFORE (2fe324e11e) | AFTER |
|---|---|---|
| ABSENT | `CEO public profile (Jane Doe): ABSENT, the CEO web search returned 10 url(s).` | `CEO public profile (Jane Doe): No CEO web search was run for this company.` |
| CONFIRMED | `CEO public profile (Jane Doe): CONFIRMED, the CEO web search returned 10 url(s).` | `CEO public profile (Jane Doe): No CEO web search was run for this company.` |
| NOT_SEARCHED | fixed sentence (already caught by `\w_\w`) | fixed sentence |
| SEARCHED_NOTHING_FOUND | fixed sentence (`\w_\w`) | fixed sentence |
| SEARCHED_LINKS_UNREADABLE | fixed sentence (`\w_\w`) | fixed sentence |
| SEARCH_FAILED | fixed sentence (`\w_\w`) | fixed sentence |
| NOT_WRITTEN | fixed sentence (`\w_\w`) | fixed sentence |
| UNREADABLE_OBJECT | fixed sentence (`\w_\w`) | fixed sentence |

Denominator: 8 words, 2 changed (ABSENT, CONFIRMED), 6 unchanged (already screened by the underscore pattern).

W524-S1 exact string (T1): BEFORE `CEO public profile (Jane Doe): ABSENT, the CEO web search returned 10 url(s).`; AFTER `CEO public profile (Jane Doe): No CEO web search was run for this company.`

Callers of `_plain_reason(` in `render_pack.py`: 23 call sites (the `def` line makes 24 matches). Each takes its own fixed sentence when the served reason carries one of the eight words. Three call sites pass `fixed=None`, so a reason carrying a word drops that clause rather than printing a sentence: the definition gate (`_definition_plain`, the basis definition is omitted), the unknown verdict in `_verdict_sentence` (prints `UNKNOWN_VERDICT_SENTENCE`), and the thesis-driver series (the driver clause is dropped from the chart line). These are the by-design branches of the caller, not changed here.

Eight fixture names (T5 and the existing cd1 S5 check): HD_US and BA_US print the base line byte-identically; the six NOT_WRITTEN names are unchanged (a null object, not a basis).

## Tests

Run once on the unedited head (`git show HEAD:...render_pack.py`, the tuple at 10 entries), the new file: `7 failed, 21 passed`. Failing: T1, T2[ABSENT], T2[CONFIRMED], T3[ABSENT], T3[CONFIRMED], T7, T8. Passing controls at the base: T4 (3 of 3), T5 (2 of 2), T6 (4 of 4), plus T2 and T3 for the six underscore words, which the existing pattern already screened.

After the edit: `28 passed` (AC1, exit 0).

Named existing tests, base and after: `test_by1_reason_mapper.py`, `test_cd1_ceo_sentence_per_state.py`, `test_ca1_ceo_three_states.py`, `test_bz2_rich_management_equals_pdf.py`: `148 passed` at the base and `148 passed` after.

Whole print tests folder (AC2): `FAILED lib/research/print/tests/test_av2_export_equals_page.py::test_pdf_text_carries_no_field_code_and_names_every_line_in_words` (the one failure at the base too), `1 failed, 499 passed`.

## Tests re-scoped

none

## Not verified

- The deployed Lambda serves the old pattern set until `AMGT-ce-4`.
- The whole api folder (`lib/research/api/tests`) was not run in this sparse worktree; the issuer runs it in the full tree.
- The 101-name census (`AMGT-ce-3`) was not run here; it is the issuer's read.
- The literal chart line `The chart: ABSENT` (`render_pack.py`, `_thesis_driver_chart_markdown`, pinned by `test_ba18_chart_line.py`) is outside the tuple and was not changed; see `AMGT_RESAPP-D1-W525-S1`.
