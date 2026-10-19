# CF2 receipt -- AMGT-cf-2 (round 124)

Worker 0.9.0_WK_AMGT_RESAPP~528, branch wk-AMGT_RESAPP-528, worktree C:/dev/wk-resapp-528.
Base: issuance commit 5dae2841dd. Task order: org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-cf-2.a-peers-absent-column-and-the-chart-line-print-not-available-not-the-state-word.md

## What changed

- lib/research/print/render_pack.py: 2488 -> 2491 lines (+5 -2). (a) module constant `NOT_AVAILABLE_WORDS = "Not available"` beside `ABSENT_COLUMN_SENTENCE`, with a one-line comment naming AMGT-cf-2. (b) `_peers_markdown` absent-column loop prints `"{0}: {1} -- {2}"` with `NOT_AVAILABLE_WORDS`; the column, the `_plain_reason` text and the fixed fallback are unchanged. (c) `_thesis_driver_chart_markdown` line is `"The chart: " + NOT_AVAILABLE_WORDS` plus the same series tail; the print conditions and the `[]` returns are unchanged. Nothing else in the module moved.
- lib/research/print/tests/test_cf2_not_available_words.py: new, 124 lines. Thirteen test items (T1 to T4 parametrised, T5, T6, T7a to T7d, T8, T9, T10), hand-written expectations.
- lib/research/print/tests/test_ba18_chart_line.py: 29 -> 30 lines (one re-scoped assertion, see Tests re-scoped).
- lib/research/print/tests/test_by2_rich_export_rules.py: 267 -> 268 lines (one re-scoped expectation tuple, see Tests re-scoped).
- lib/research/print/tests/test_bv2_rich_dates_and_quotes.py: 206 -> 211 lines (one added mapping for the recorded chart line, see Tests re-scoped).
- org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~528/CF2_RECEIPT.md (this file) and the instance AMGT_RESAPP.TO-AMGT-cf-2.a-peers-absent-column-and-the-chart-line-print-not-available-not-the-state-word.proof_of_spec.json.
- Not touched: lib/research/api/scoped_amgt.py, any portal path, org/devices/, the TO file (its status flip is the issuer's), the surprise channel (no row filed).

## Census

`ABSENT` literal count in lib/research/print/render_pack.py (native Grep, content mode, every line listed):

- BEFORE (unedited head 5dae2841dd): 50 lines.
- AFTER: 48 lines.
- The difference is exactly the two lines the cell names: head line 1969, `"{0}: ABSENT -- {1}".format(` (now the `NOT_AVAILABLE_WORDS` form, no literal), and head line 2187, `line = "The chart: ABSENT" + ...` (now `"The chart: " + NOT_AVAILABLE_WORDS + ...`). The chart's docstring at head line 2177 and every other ABSENT line (Posture, the no-call lines, the y/y and estimate-year lines, Description, Exec Management, the no-peer-set line, the Model Cases lines) are untouched and keep their literal.

## Tests

Base run (the unedited head render_pack.py, swapped in from `git show HEAD:` for the run and restored from a scratch copy; new test file present):
- test_cf2_not_available_words.py: `9 failed, 24 passed` across the four files run together (test_ba18_chart_line.py, test_by2_rich_export_rules.py, test_bv2_rich_dates_and_quotes.py, test_cf2_not_available_words.py). The nine failures are T1 to T4 (4), T5, T6, T7a, T7b, T10. The passes at base are T7c, T7d, T8 (present-column and member rows), T9 (other ABSENT lines), and the three pinned files' own tests (all pass at base, as expected).
- Base run of the one known-failing av2 test (`test_pdf_text_carries_no_field_code_and_names_every_line_in_words`): fails at head with the same assertion (line 175, the header figure `Share price (last close): local currency 100.00 per share - date not stored with this figure - Bloomberg`). Same failure after the edit.
- Recorded base lines for T8 (present column row and member row), hand-written: `| Revenue | CSC_REV | peer |` and `| Acme Corp | ACME US | Industrials | US | 1234.5 |`. Both pass at base and after.

After the edit:
- test_cf2_not_available_words.py: `13 passed`.
- The four files together: `33 passed`.

## Tests re-scoped

Each re-scope changes only a pinned peers-column line or chart line. No other ABSENT pin was touched.

1. lib/research/print/tests/test_ba18_chart_line.py, line 19 (after the edit line 19-20). Old: `['The chart: ABSENT -- the thesis driver is "EBITDA"']`. New: `['The chart: Not available -- the thesis driver is "EBITDA"']`.
2. lib/research/print/tests/test_by2_rich_export_rules.py, line 205 (after the edit 205-206). Old expect tuple: `(FIXED_REFUSED, "C1: ABSENT -- ", "The chart: ABSENT")`. New: `(FIXED_REFUSED, "C1: Not available -- ", "The chart: Not available")`.
3. lib/research/print/tests/test_bv2_rich_dates_and_quotes.py, after the existing `Exec Management` mapping (new lines 172-177). The committed base fixture lib/research/print/tests/fixtures/bv2_rich_text_base_RIO_LN.txt line 50 (`The chart: ABSENT`) is NOT edited; the test maps the recorded line to `The chart: Not available` the same way the test already maps the Exec Management line, and asserts the recorded line is present first. Old: `The chart: ABSENT` (recorded). New expected: `The chart: Not available`.

Not re-scoped (pinned by the tests, outside the ruling's list, and left with their words): `Posture: ABSENT`, `ABSENT -- no call was made`, `y/y growth rows: ABSENT`, `<years>: ABSENT -- the block carries fiscal years`, `Description: ABSENT`, `Exec Management: ABSENT`, `ABSENT -- no peer set supplied to this export`, the Model Cases `<name> case: ABSENT` lines. These are recorded for the issuer as an open question, not a worker finding.

## Not verified

- The deployed Lambda serves the old words until AMGT-cf-4.
- The page (PeersTab.tsx) still shows ABSENT on these lines because the portal is not in this cell.
- The whole lib/research/api folder is not run in this sparse worktree; the issuer runs it in the full tree. The api folder was grepped for the pinned strings (no matches for the peers-column or chart lines).
- test_av2_export_equals_page.py: only its one known failure remains; no other failure in the print folder.
