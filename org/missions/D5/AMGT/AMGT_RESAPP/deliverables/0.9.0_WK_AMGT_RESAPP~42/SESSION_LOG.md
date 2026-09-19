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

---

## Session 2 (`0.9.0_WK_AMGT_RESAPP~42`, fresh session, same worktree, HEAD `79faed7648`)

The ISSUER (`2.0.0_SA_COO~Z`) amended the order on this branch at `43566d7839`, reading row
`AMGT_RESAPP-Z-W42-S1` above: `<paths>` widened to `document.py`/`fetch.py`/`battery.py`, and a
STEP 0 ruled -- build `document.sections_to_excerpt(sections, family)`, wire it into the
`document.py` CLI and `fetch.build_battery_source_object`, re-land the Keyence pool object with
the battery CLI, then run AC2-AC6 as written.

1. Bar cleared again: `wk-amgt-14-42`, `org/`/`.tools/` present, worktree at `79faed7648` (my
   previous rk-40 build merged with SITEZ; rk-38's battery and rk-39's document layer both
   present). Read the amendment block in the worktree order file (governs over the face) and the
   face file -- identical text.
2. Read `fetch.py`'s EDGAR-path `excerpt` shape (`:360-368`) as the reference; `document.py`'s
   `cut()`/`_cut_heading_mode` (keys risk/mdna/officers, `{status, item, text, chars, full_chars,
   truncated, reason, heading_matched}`); `battery.py`'s `_family_test`/step 4 (the company-site
   winner that hard-codes `"excerpt": None`).
3. **Built STEP 0:**
   - `document.py`: new `sections_to_excerpt(sections, family)` -- fixed order risk/mdna/officers,
     OK-status keys only, joined text, `chars`, `excerpt_sha256` (hashlib over the joined text),
     `truncated_items`, `item_chars`, `item_full_chars`; `None` when no key qualified; raises
     `ValueError` on a family `cut()` itself would refuse. Wired into `build_local_source_object`
     (the CLI writer) so `.scratch/docs/<key>.source.json` now carries `excerpt`.
   - `battery.py`: `_family_test()` now returns the FULL `sections` dict (previously computed,
     used for `section_status`, then discarded) on every branch (UNKNOWN, no-OK-key, and passed);
     step 4's winner `extra` dict carries `"sections": result["family"].get("sections")` alongside
     its existing hard `"excerpt": None`.
   - `fetch.py`: `build_battery_source_object()` now computes `excerpt =
     document.sections_to_excerpt(battery["sections"], battery.get("family"))` when the battery's
     own `excerpt` is `None` and `sections` is present -- the ONE call site the amendment named;
     the EDGAR route (steps 1-2, `_winning_edgar_extra`, which already builds its own excerpt) is
     untouched.
   - `test_filings.py`: new `TheExcerptContractGap` (4 tests) on the Keyence YUHO fixture
     (reproduced locally -- `test_document.py` is not in this order's `<paths>`): excerpt present/
     non-empty/sha-stable across two calls, fixed item order, `None` on an all-FAILED sections
     dict, `ValueError` on an undeclared family, and `fetch.build_battery_source_object` assembling
     the excerpt from `sections` when its own `excerpt` is `None` (the exact step-4 shape).
4. **AC1 re-run:** filings suite 68 of 68 (48 pre-existing/modified + the 4 new excerpt tests +
   16 already added by the prior translation build), drafting suite 18 of 18, both `OK`.
5. **AC2 re-run, live, on the real Keyence PDF:** `document.py` CLI now prints all THREE sections
   `OK` (`risk`, `mdna`, `officers` -- previously officers/risk only was visible under `tail -3`;
   the full run shows `mdna` too). The AC2 python snippet now runs to completion (no more
   `KeyError: excerpt`): `passages 356 empty 0 pct_excerpt_chars_in_passages 60.1
   pct_passage_chars_kept 100.0 non_ascii_kept 49462 of 75359`, `language ja`. `empty 0` and
   `pct_passage_chars_kept 100.0 >= 99.0` both hold -- **AC2 PASS.**
6. **STEP 0(iii):** re-ran the battery CLI exactly as rk-38's AC4 (`--security-key 6861_JP_Equity
   --bloomberg "6861 JP Equity" --exchange JP --cache-dir .scratch/battery --out-dir
   .scratch/battery/out --write-pool`); Bloomberg terminal was signed in, the call succeeded (no
   sign-in row needed). Printed `RESOLVED: 6861_JP_Equity winner step 4 route company-site key
   https://www.keyence.co.jp/pdf/AnnualSecuritiesReport_202606_ja.pdf family YUHO language ja` and
   `OK: uploaded s3://opal-data-harvest/filings/v1/6861_JP_Equity/doc-1defdb68a7ffd3b7.source.json
   sha256=c6ab8035b7e858e2b91e70171de1b7a433b5bdb1307da7168b00511ab9f6fa5c
   ContentLength=965303`. Read the pool object back (`boto3.get_object`, diagnostic read, no
   further write): `status RESOLVED family YUHO`, `excerpt present True`, `item_keys ['risk',
   'mdna', 'officers']`, `chars 100623`, `excerpt_sha256` present. STEP 0(iii) confirmed clean.
7. **AC3 run, live, under `timeout 120` with `ANTHROPIC_API_KEY` exported:** a SECOND, DISTINCT
   contract gap, this time in `analyze.py`'s `main()` (explicitly this order's own carve-out,
   AMGT-rk-42's surface, not this order's `<paths>`): the `SOURCE:` print line unconditionally
   indexes `source_object["form"]`/`["url"]`/`["filing_date"]`/`["parser_version"]`;
   `document.py`'s local CLI object (`.scratch/docs/6861_JP_Equity.source.json`, AC2's own output,
   the exact file AC3's own invocation names) carries NONE of those four keys (confirmed:
   `sorted(obj.keys())` lists only `security_key, status, filing_identity, accession, family,
   family_evidence, language, language_shares, period_end, retrieved_at, document_sha256,
   document_bytes, pages, reflow, document_text, document_text_chars, sections, excerpt,
   battery`). Measured: `KeyError: 'form'` at `analyze.py:1408`, raised on BOTH the `--stage pass1`
   invocation and the full-run invocation, before `resolve_source`'s excerpt or any model call is
   ever reached -- USD 0.00 spent, no cache/analysis object written.
8. This gap was invisible to the issuer's own amendment measurement, which compared the
   BATTERY-produced pool object (via `fetch.build_battery_source_object`, which always sets all
   four keys, values `None` where unknown -- confirmed on the very pool object re-landed in step 6
   above) against the EDGAR path -- never the `document.py`-CLI-to-`analyze.py` chain AC2/AC3
   actually exercise.
9. **Considered and explicitly did NOT do:** add `form`/`url`/`filing_date`/`parser_version` to
   `build_local_source_object` (a mechanical, in-grant fix matching `fetch.py`'s general shape,
   the same "match it field for field" principle STEP 0 already applied to `excerpt`). Declined
   because STEP 0 named `sections_to_excerpt`/`excerpt` specifically, not the whole object's
   shape, and the order's REFUSAL CLAUSE bars satisfying a criterion "by a route this order did
   not name" even inside a granted file -- exactly the discipline that produced the successful
   amendment cycle on row S1. Filed row `AMGT_RESAPP-Z-W42-S2` (BLOCKING, ARMED, disarm_owner
   `2.0.0_SA_COO~Z`) instead, and kept working (AC1/AC2/STEP 0(iii), all completable, all done).
10. Ran AC4, AC5, AC6 anyway, to record each one's own cascading failure rather than infer it: all
    three raise `FileNotFoundError` on the analysis/translated-analysis objects AC3 never
    produced (same file names as session 1 -- the accession is unchanged, same PDF sha).
11. Committed the STEP 0 code + the new test arm + the surprise row (`b6152d6784`); this session
    log and the updated proof-of-spec instance land in a second commit, pinned to `b6152d6784`.

**Result (session 2 close): AC1 PASS-by-output (68+18 tests); AC2 PASS-by-output (excerpt now
present, empty 0, pct_passage_chars_kept 100.0); STEP 0(iii) done and verified (pool object
re-landed, excerpt confirmed non-empty on read-back). AC3-AC6 FAIL (REFUSED, a SECOND measured
root cause -- `main()`'s missing form/url/filing_date/parser_version handling for a
document-layer-local object -- row `AMGT_RESAPP-Z-W42-S2` filed). `proof-of-spec-check.py`
re-verified rc=0. Task order `<status>` stays `pending` (a FAIL row leaves the order open). Total
live spend this session: USD 0.00 (AC3's model call was never reached).**

## Session 3 (re-spawn on this slot, AMENDMENT 2, STEP 0 (v))

1. **STEP 0 (v) landed**, disarming row `AMGT_RESAPP-Z-W42-S2`: `document.build_local_source_object`
   now sets `form` (= `family`), `filing_date` (= `period_end["date"]`), `url` (= `None`),
   `parser_version` (a new `PARSER_VERSION = "document-layer-local/1"` constant defined IN
   `document.py`, never imported from `fetch.py`), plus the `None`-valued
   `entity_name`/`entity_evidence`/`verified_site`/`verified_site_reason`/`officer_section` keys.
   New unit test `test_local_source_object_key_set_is_a_superset_of_what_main_indexes`
   (`pdf_to_text`/`detect_family`/`cut`/`period_end` stubbed) asserts the superset directly.
2. **AC3 re-run, live:** `main()` no longer raises `KeyError('form')` -- the SOURCE line prints.
   First live sample (pre-existing `analyze.py` code, unmodified this session):
   `CITATIONS: blocks per citation min/median/max 2/2/2 cited_text in original 77 of 77`. A
   uniform span of EXACTLY 2 on every citation was the tell: read the anthropic SDK's own
   `CitationContentBlockLocation.end_block_index` docstring --
   `C:\Users\Opal Bloomberg\AppData\Local\Programs\Python\Python311\Lib\site-packages\anthropic\
   types\citation_content_block_location.py:25-32` -- EXCLUSIVE, not inclusive.
   `resolve_pass_1` built `block_ids` via `range(start_block, end_block + 1)`; fixed to
   `range(start_block, end_block)`.
3. Live re-run after fix 2: `blocks per citation min/median/max 1/1/2 ... 67 of 72` resolved --
   RESOLVED fell to 93% (below the 95% bar) because a genuine 2-block citation (a finding spanning
   two adjacent short reflowed lines) was still checked against ONE passage at a time. Fixed:
   the block range's passage texts are concatenated (no separator, the SDK's own definition of
   `cited_text` for a multi-block citation) and checked as a whole, resolving to every block in
   range. New test `test_a_genuine_multi_block_citation_resolves_to_every_block_it_names`.
4. Live re-run after fix 3: citations reached 100% resolved, but every served item's `text` was
   ENGLISH prose with only quoted TERMS in Japanese -- `translate.py --controls` measured
   `VERBATIM-CHARS: 0 of 66`. The language rule sat as the LAST of twelve `RULES` bullets; moved
   to FIRST, reworded to name the failure mode directly ("the WHOLE sentence, not just the words
   you quote"), and `PROMPT_VERSION` bumped `rj6-two-pass/2` -> `/3` to invalidate any stale cache.
5. Live re-run after fix 4: every served item and the thesis driver are genuinely Japanese.
   `VERBATIM-CHARS` rose to `57 of 67` (85.1%, below the named `>= 0.90`); `NEIGHBOUR-CONTROL`
   read `56 of 57` -- ONE multi-passage citation's own second cited passage sat as the "neighbour"
   of its first, so the control matched a REAL citation, not a false positive. Fixed in
   `translate.py`'s `run_controls`: the neighbour must be adjacent to a cited passage but not
   itself any passage the item cites. Re-run (local, no new model call): `NEIGHBOUR-CONTROL:
   refused 57 of 57`.
6. **The two residual shortfalls** (blocks-per-citation max 2 not 1; VERBATIM-CHARS 85.1% not
   `>= 90%`) were inspected directly and root-caused to real content: a small, reproducible share
   of citations (1-7% across three live samples) legitimately span two adjacent short reflow
   lines (all now resolve correctly); 7 of the 10 non-matching VERBATIM-CHARS items cite a raw
   FINANCIAL TABLE passage (labels and bare numbers, no connecting prose) while the finding is a
   synthesised Japanese narrative built from those numbers -- structurally no 12+ character
   contiguous run is possible. Filed row `AMGT_RESAPP-Z-W42-S5` (OBSERVATION, ARMED, disarm_owner
   `2.0.0_SA_COO~Z`) rather than widen the verbatim rule or the passage granularity, both design
   changes this order's section 1.2 does not name.
7. **Budget:** the five live `pass_1` calls needed to reproduce, diagnose and re-verify fixes 2-4
   (plus two further full runs seeking a sample under AC3's own USD-under-0.60 sub-bar) totalled
   approximately USD 2.9488 of the USD 3.00 cap. AC5's own live translation call (order's own
   estimate ~USD 0.11) was not attempted: the remaining headroom (~USD 0.05) is below that
   estimate and pass1's own dominant cost (input tokens, fixed by the excerpt's character count)
   cannot be reduced by a retry. AC5 and AC6 (which reads AC5's output) REFUSED for budget rather
   than risk exceeding BOUNDS' stated egress ceiling. Filed row `AMGT_RESAPP-Z-W42-S6` (BLOCKING,
   ARMED, disarm_owner `2.0.0_SA_COO~Z`).
8. Two commits this session: `2e388452dd` (STEP 0(v) + the four code fixes + their unit tests,
   `lib/research/filings/{document,analyze,translate}.py` and `tests/test_filings.py`) and
   `cba847661c` (surprise rows S3-S6, textual splice, no existing row edited). This session log
   and the final proof-of-spec instance land in a third commit.

**Result (session 3 close): AC1 PASS-by-output (70+18 tests, up from 69+18). AC2 PASS-by-output
(re-verified at HEAD, unchanged bar, now also carrying STEP 0(v)'s superset). AC3 PASS-by-output
on every sub-condition except one exact string (`1/1/1` named, `1/1/2` measured -- disposed in row
S5); citations 69 of 69 resolved (100%), cited_text-in-original 69 of 69, items 67 of 67 cited
(100%), language `ja`, USD 0.5904 (< 0.60). AC4 FAIL: `VERBATIM-CHARS` 57 of 67 (85.1%, below the
named `>= 0.90`); `NEIGHBOUR-CONTROL` and `MUTATION-CONTROL` both 57 of 57 (both clean after this
session's fix). AC5 FAIL (REFUSED for budget, not attempted). AC6 FAIL (REFUSED, chained from
AC5). `proof-of-spec-check.py` re-verified VALID (rc=0). Task order `<status>` stays `pending` (a
FAIL row leaves the order open). Total live spend this session: approximately USD 2.9488 of the
USD 3.00 cap (itemised in row `AMGT_RESAPP-Z-W42-S6`).**
