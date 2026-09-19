# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~42 on AMGT_RESAPP AMGT-rk-40

Worktree `/c/tmp/wk-amgt-14-42`, branch `wk-amgt-14-42`, cut from SITEZ HEAD `249d6527bd`.

1. Bar cleared: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-42`; `org/`, `.tools/`, every path
   in the order's section 3, and the AMGT-rk-39 dependency `lib/research/filings/document.py` all
   exist. No BLOCKING row needed.
2. Read the order in full, then `lib/research/filings/passages.py`, `analyze.py`,
   `drafting_build.py`, `lib/research/drafting/{verbatim,pipeline}.py`, `document.py` (family cuts,
   `detect_language`), `fetch.py` (the EDGAR `excerpt` builder, for contrast), and the existing test
   files.
3. Built section 1.2 in full, within this worker's owned surfaces:
   - `passages.py`: `build_passage_map()` stores NFC-normalised, UNFOLDED text; `non_ascii_chars`
     replaces `ascii_replacements`; `to_ascii()`/`_ASCII_MAP` removed. `Locator` now carries a
     SPACED and an UNSPACED index (both offset-preserving into the original text); `normalise`/
     `contains`/`find` take an explicit `unspaced=` parameter.
   - `analyze.py`: `pass_1()` sends the document as one `{"type": "content"}` block per passage,
     for EVERY document; `resolve_pass_1()` adds the `content_block_location` shape (block index
     maps DIRECTLY to a passage id, `cited_text` still checked to lie inside that passage after
     normalisation -- "a block index is never trusted alone") beside the unchanged
     `char_location`/inline-tag shapes; the pass-1 prompt gains ONE language rule when
     `language != "en"`; `pass_2()`'s `max_tokens` scales with pass 1's own output length and a
     truncated reply is recorded (D14); `analyze_source()`/`build_analysis()` record `language`
     (source object's own field, else `document.detect_language`, imported lazily) and a
     `text_encoding` object replacing `ascii_normalisation`. `PROMPT_VERSION` -> `rj6-two-pass/2`,
     `ANALYZER_VERSION` -> `opal-filings-analyze/2.1.0` (AMGT-rk-42 had already landed at
     `2.0.0`, so this order's own instruction was to bump `2.0.0 -> 2.1.0`), and
     `OUTPUT_CONTRACT_FINGERPRINT` recomputed against the moved contract via the live fixture
     (`fe4b12c18b6158e7ef4bec6f9d1f04c993cb10331ed03ed52782c1190e83c83c`) -- `test_batch.py`
     (not this worker's file) reads both dynamically and still passes.
   - `lib/research/drafting/verbatim.py`: `normalise()` gains NFC first and an `unspaced=` mode
     that AUTO-DETECTS from the text's own script share when the caller passes none, because
     `pipeline.py`'s one caller (`check_against_sources -> is_verbatim -> normalise`) is generic
     and carries no language parameter, and `pipeline.py` is AMGT-rk-41's file, not this order's
     to widen.
   - `drafting_build.py`: `longest_verbatim_run()` dispatches on `cjk_share` -- the pre-existing
     spaced-script token search (unchanged, floor 8 tokens) or a NEW character-level binary search
     on whitespace-stripped text (`_longest_verbatim_run_chars`/`_strip_ws_with_offsets`, floor 12
     characters, span returned as the ORIGINAL substring); `_QUOTED_RE` recognises Japanese corner
     brackets beside ASCII double quotes; `quote_method` gains `longest-verbatim-run-chars`.
   - `lib/research/filings/translate.py` (NEW): `translate_output(analysis, caller=None)` -- ONE
     model call per non-English document through `analyze.anthropic_call`, translating every
     served item's text plus the driver's series/unit/why; a count mismatch is a FAILED
     translation recorded on the object with every item left original-only; English makes NO
     call. `--controls` runs VERBATIM-CHARS/NEIGHBOUR-CONTROL/MUTATION-CONTROL;
     `run_relocate_control` checks every `text_translated` does not itself relocate in the
     original.
   - Tests: `test_filings.py` (kana fixture 100% retention replacing the retired ascii test,
     `ThePrecutCitationBlocksResolution`, `TheCharacterLevelVerbatimRule` with its neighbour and
     mutation controls) and the new `test_translation.py` (English skip with an exact call count,
     the full non-English contract, the count-mismatch FAILED arm, the relocate control).
4. **A pure-ASCII-file trap, found and fixed twice this session:** the tool layer that carries
   `Edit`/`Write` parameter text JSON-decodes a literal `\uXXXX` sequence into the actual Unicode
   character before it ever reaches the file -- so typing the six-character escape for the
   Japanese left corner bracket in a parameter to "write an
   ASCII escape" instead WROTE THE LITERAL CHARACTER, silently violating "no non-ASCII byte in
   anything a worker writes" in exactly the files this order is strictest about (`drafting_build.py`
   `_QUOTED_RE`, `analyze.py`'s `LANGUAGE_RULE_TEMPLATE`, and the planned Japanese test fixtures).
   Caught by running the CLAUDE.md detector (`len(b) - len(b.decode('utf-8'))`) on every touched
   file BEFORE committing, not by inspection. Fixed by switching every non-ASCII literal to
   `chr(0x....)` composition (the same convention `passages.py`'s `_QUOTE_MAP` and `verbatim.py`'s
   `_CURLY_QUOTES` already used) -- zero non-ASCII bytes confirmed on all 7 touched `.py` files
   after the fix.
5. AC1: `python -m unittest discover` both suites -- 48 (filings) + 18 (drafting) = 66 tests, both
   `OK`. `.tools/commit-gate.sh` clean for 7 of 7 touched `.py` files.
6. **AC2 measured, live:** ran AMGT-rk-39's CLI (`document.py`) against the real Keyence Yuho PDF
   -- fetch/reflow/family-cut/language-detect all succeed (`family YUHO`, `language ja`). AC2's own
   `python -c` snippet then does `ex = src['excerpt']` on the written `.source.json` and raises
   `KeyError: 'excerpt'` immediately, rc 1: the object `document.py` writes carries `sections`
   (`risk`/`mdna`/`officers`), never `excerpt`. Cross-checked against `fetch.py`'s SEPARATE
   EDGAR-only `build_source_object()`, which DOES build an `excerpt` key -- but from
   `extract_sections()`'s own `sections` dict, a different function, in a file this order does not
   grant. Cross-checked against AMGT-rk-39's OWN task order (`AMGT_RESAPP.TO-AMGT-rk-39...md:183`):
   its own AC2 reads `cut['sections']`, never `excerpt` -- rk-39 never promised this shape.
7. Filed surprise row `AMGT_RESAPP-Z-W42-S1` (GROUNDED, BLOCKING, ARMED, disarm_owner
   `2.0.0_SA_COO~Z`) citing the measured shape and both task orders, then kept working per the
   surprise-channel protocol.
8. Ran AC3, AC4, AC5, AC6 verbatim anyway, to record each one's ACTUAL cascading failure rather
   than infer it: AC3 raises the SAME `KeyError: 'excerpt'` inside `analyze.py main()`, both
   invocations, before any model call (USD 0.00 spent, no cache/analysis object written); AC4 and
   AC5 then raise `FileNotFoundError` on the analysis object AC3 never wrote; AC6 raises
   `FileNotFoundError` on the translated object AC5 never wrote. One root cause, four cascading,
   independently-measured failures.
9. Recorded AC2-AC6 as `FAIL` / REFUSED per the order's own REFUSAL CLAUSE (a criterion that
   cannot be satisfied AS WRITTEN, never repaired by writing to `document.py`/`fetch.py`, which
   this order does not grant, and never satisfied by rewriting the order's own literal
   invocations).
10. Committed code + tests + the surprise row (`0da974e0dd`), then wrote and validated the
    proof-of-spec instance against that commit, then ran `.tools/proof-of-spec-check.py` for all
    six criteria: `VALID (rc=0)`.

**Result (session close): AC1 PASS-by-output; AC2-AC6 FAIL (REFUSED, measured, root cause common to
all five, row `AMGT_RESAPP-Z-W42-S1` filed). `proof-of-spec-check.py` rc=0 (structurally VALID).
Task order `<status>` stays `pending` -- not flipped to `complete` (a FAIL row leaves the order
open). Total live spend this order: USD 0.00 (no model call was ever reached).**
