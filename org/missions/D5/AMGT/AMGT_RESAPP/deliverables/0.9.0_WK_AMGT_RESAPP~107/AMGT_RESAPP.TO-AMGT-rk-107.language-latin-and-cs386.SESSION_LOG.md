# Session log -- `0.9.0_WK_AMGT_RESAPP~107` on `AMGT-rk-107` (round 28, the Lenovo trial's wave 0)

Worktree `C:/tmp/wk-amgt-28-107`, branch `wk-amgt-28-107`, base `0ed364cff0`.

1. First act: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-28-107`; `org/` and `.tools/` present -- TREE-OK.
2. Read the task order in full. Read `lib/research/filings/document.py:330-365` (`detect_language`) and
   `lib/research/harvest/filings.py:297-312` (`_first_differing_outcome_field`) at the branch HEAD to
   confirm the MEASURED STATE matched the order's text (the `ascii_share > 0.5` -> `"en"` branch; the
   length branch printing `len(old_fields)`/`len(new_fields)`).
3. Snapshotted working-tree bytes of both modules to `.scratch/r107/*.orig` (mutation discipline).
4. Ran AC0 BEFORE any edit -- baseline: the two function bodies as measured; filings suite `100 passed`
   (F0); harvest suite `79 passed` (H0).
5. Edited `document.detect_language`: the ascii-majority branch now tokenizes the lower-cased sample
   (`[a-zA-Z]+`) and scores it against nine ASCII-only stopword sets (`en`, `de`, `fr`, `it`, `es`, `nl`,
   `pt`, `sv`, `da`, module constants `_STOPWORDS`/`_STOPWORD_LANGS`/`_MIN_STOPWORD_HITS`); the language
   with the most hits wins, `"en"` wins ties (first in `_STOPWORD_LANGS` order), and `"en"` is also the
   fallback when no language reaches `_MIN_STOPWORD_HITS` (a stated known limit for a language outside
   the table). The returned dict gains `"stopword_hits"`. `ja`/`zh`/`ko`/`unknown` branches and the
   letter-share computation are untouched.
6. Edited `harvest/filings.py` `_first_differing_outcome_field`'s length branch ONLY: it now reports
   `len((existing.get("battery") or {}).get("attempts") or [])` against the same for `new`, labelled
   `"battery.attempts length: <old> -> <new>"`, instead of the flattened field-pair counts (CTO round-27
   analysis, msg 24239 -- C-S386). Nothing else in the function changed.
7. Wrote `lib/research/filings/tests/test_language_latin.py` (6 arms: German/French/Italian fixtures --
   ~60-80 words each, ASCII-transliterated, plus one literal accented word each -- detected as
   `de`/`fr`/`it`; an English fixture stays `en`; a kana fixture stays `ja` unchanged with
   `stopword_hits == {}`; `stopword_hits` reported with all nine language keys and `de` as the max for
   the German fixture).
8. Wrote `lib/research/harvest/tests/test_changed_held_length_text.py` (1 arm: 2 attempts vs 3 attempts
   with an equal common prefix -- `"battery.attempts length: 2 -> 3"`).
9. Ran AC1 (6 passed) and AC2 (1 passed) directly against the uncommitted edits.
10. Committed the two edited modules and two new test files (`0de2c26e825f14821f51c0dd18a43f9439423c8c`)
    so AC4's `git diff 96cc4dae9d HEAD` has a real HEAD to diff against.
11. Re-ran AC1 (6 passed), AC2 (1 passed), AC3 (filings `106 passed` = F0+6; harvest `80 passed` = H0+1)
    and AC4 (`changed_code_files` exactly the four paths; all four `compiles True crlf 0`;
    `non_ascii_chars 0` for both production files; 20 for the two new test fixtures -- 4 accented Latin
    characters plus the 16-character kana sentence) against the committed HEAD -- all PASS.
12. Ran a planted mutant control: temporarily reverted the ascii-majority branch to unconditional `"en"`
    (bypassing the stopword test) and re-ran `test_language_latin.py` -- 5 of 6 arms FAILED as expected
    (`de`/`fr`/`it`/`stopword_hits_reported`/`english_text_still_en` all failed on the assertion or
    KeyError; only the unaffected `ja` arm still passed), FIRED-AS-EXPECTED. Restored the fixed file
    byte-for-byte from the `.scratch/r107/document.py.fixed` snapshot taken right after step 6/before the
    mutant edit; `diff` against the snapshot showed 0 differences and `git status --short` showed the
    working tree clean against the committed HEAD.
13. Ran `test_language_latin.py` and `test_changed_held_length_text.py` twice each (pre- and post-mutant
    restore) with identical PASSED test names both times (timing only differed) -- STABLE.
14. Ran `py_compile` and `ruff check` on the four changed files directly (both clean) in addition to the
    `commit-gate` checks that ran inside `safe-commit.sh`.
15. Wrote this proof-of-spec instance, validated it with this worktree's own
    `.tools/proof-of-spec-check.py`, flipped `<status>` to `complete`, and committed the deliverables +
    task-order flip in a second commit.

No AWS call, no S3 write, no vendor/Bloomberg call, no install, no cron/alarm/monitor armed. The four
existing callers, `analyze.py`, translation code, the API's `text_translated` drop (gap G-6) and
`store.py` were not touched. Branch `wk-amgt-14-50` / worktree `C:/tmp/wk-amgt-14-50` never referenced,
read, shown, diffed or checked out.
