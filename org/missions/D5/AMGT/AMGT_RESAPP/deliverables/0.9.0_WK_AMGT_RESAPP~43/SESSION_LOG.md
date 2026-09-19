# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~43 on AMGT_RESAPP AMGT-rk-41

Worktree `/c/tmp/wk-amgt-14-43`, branch `wk-amgt-14-43`, cut from SITEZ HEAD `b501ea3c82`.

1. Bar cleared: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-43`; `org/`, `.tools/` and every
   path named in the order's section 3 exist.
2. Read both never-widen halves in full
   (`org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND14_CHAIN_F_{COO,CTO}_HALVES.md`):
   both carry an `AMGT-rk-41` section, both SIGNED (CTO re-signature 2026-09-18 ~23:3xZ against
   COO halves `541d395e0d`, withholding lifted on D3's bound line). Read in the order named:
   D3 (sections[].sentences ships only PASS, held sentences in a top-level block), D1 (empty
   population/key-set REPORTS, rc 3, never silent 0), D4 (`--only-keys` restricts the live rebuild
   to the three validation names; the twelve covered stay DRY-RUN this round).
3. Read the source: `lib/research/drafting/pipeline.py`, `verbatim.py`, `producer.py`,
   `lib/research/filings/drafting_build.py`, `schema.json`, both test files, `analyze.py`'s
   `write_outputs`/DRAFTING print line, `batch.py`'s `plan_only_check` (the list_objects_v2
   precedent for `filings/v1/<key>/` prefixes), `crosswalk.py`'s `write_pool`/`load_crosswalk`.
4. Built:
   - `pipeline.py`: `_gate_sentences` now returns `(passed, held_no_span, refused, reasons)`;
     `run_pipeline` returns `held_no_span` (list) and `held_no_span_count` beside `dropped`.
     `verbatim.py` untouched (AMGT-rk-40's file).
   - `schema.json`: `held_no_span` (top-level, optional) + `held_sentence` definition; `anchored`
     on the sentence definition; `quoted_spans` description no longer says vacuous PASS.
   - `drafting_build.py`: `build_drafting_document` ships only anchored/PASS sentences in
     `sections[].sentences`; new denominators `sentences_drafted`/`served`/`served_on_span`/
     `served_no_span`/`held_no_span`/`refused`/`split`, with `sentences`/`verbatim_pass`/`quoted`
     KEPT for `analyze.py`'s existing (unedited) DRAFTING print line, now carrying the post-HOLD
     values under their pre-existing labels. New CLI: `--analysis PATH --report`;
     `--rebuild-pool --population PATH [--dry-run] [--pre-act-dir DIR] [--only-keys K1,K2,...]`,
     argparse-driven (AC8), reading the population from the S3 pool key directly (the population
     argument does not resolve to a local path -- confirmed absent locally before building the
     loader) and the newest `filings/v1/<key>/*.analysis.json` per key by `LastModified`, writing
     through `analyze.write_outputs(..., drafting_only=True)` (imported lazily inside the rebuild
     function -- `analyze.py` imports `drafting_build` at module scope, so a top-level import the
     other way would cycle; verified with a live `python -c` import both directions).
   - Tests: `test_drafting.py` gains `TheVerbatimGateHold` (5 tests: HELD, SERVED-anchored,
     neighbour-REFUSE, mutation-REFUSE, mixed-batch split-sums) -- AC1's 4 planted arms plus the
     split-sum arm. `test_filings.py` gains a non-empty-`quoted_spans`/`anchored` assertion on the
     existing schema-valid test and a new `test_the_verbatim_gate_hold_splits_the_pass_count` using
     the fixture's own naturally-occurring no-span sentences (no additional plant needed -- the
     fixture already carries 6 of them, e.g. "Free cash flow is guided to turn positive...").
5. AC1: `python -m unittest discover` both suites -- 18 + 32 = 50 tests, both `OK`.
6. AC2: real EDGAR fetch (CIK 18230, CAT_US_Equity 10-K) + two-pass Anthropic analysis
   (`claude-opus-5`), no `--write-pool`. USD 0.6290 total (pass1 0.4342 cached + pass2 0.1948),
   under the USD 2.00 cap and under AC2's own USD 1.00 bar. DRAFTING line: `sections 5 sentences
   40 dropped 2 verbatim_PASS 23 evidence_records 78` -- D=40 S=23 R=2 H=40-23-2=15, confirmed
   against the written object's own `denominators`.
7. AC3/AC4: offline adapter reads via `AMGT_DRAFTING_ROOT`, exactly as specified. AC3:
   `served_without_span 0`, rc 0. AC4 (planted unanchored sentence): `served_without_span 1`, rc
   1 -- the discriminating pair both hold.
8. AC5 (dry-run, read-only, run BEFORE the deploy entry): `REBUILT (dry-run) 12 of 33; 21 ABSENT`.
   TOTALS `served_on_span=210 held_no_span=179 refused=62` -- 210+179=389, matching the CRO's
   previously measured total-served count exactly (msg 23744), and 179 matches the CRO's measured
   held count exactly. Full per-key table captured to the change-management entry.
9. Opened the change-management entry (committed `b054dcb479`) BEFORE AC6, pasting both
   never-widen halves' fresh sha256 and AC5's full per-key pre-act-sha table, narrowing the blast
   radius to the three validation names per issuer bind D4.
10. AC6 (live, `--only-keys CAT_US_Equity,CSL_AU_Equity,6861_JP_Equity`): `REBUILT 0 of 3; 3
    ABSENT (no analysis object)` -- branch B (none of the three carries a pool analysis object at
    this HEAD; `rk-38`/`rk-39`/`rk-40` not drained). Confirmed by direct `list_objects_v2` on all
    three `drafting/v1/<key>.json` keys immediately after: still 0 objects, unchanged.
11. AC7: two `lambda:invoke` reads on `opal-amgt-scoped-api` for `BA_US_Equity` (one immediately
    after AC6, one repeated) both read IDENTICAL (`served 38 served_without_span 21`) -- AC6 never
    touches BA_US_Equity (a covered, non-validation key, DRY-RUN only per D4), so the criterion's
    own expect (`served_without_span` -> 0 after AC6) is unreachable this round. **AC7 recorded
    FAIL / REFUSED per the order's REFUSAL CLAUSE.** Filed surprise row `AMGT_RESAPP-Z-W43-S1`.
12. AC8: bare `python -m lib.research.filings.drafting_build` -> argparse usage naming
    `--analysis`, `--report`, `--rebuild-pool`, `--population`, `--dry-run`, `--pre-act-dir`, rc 2;
    `--rebuild-pool --population ... --no-such-flag` -> `unrecognized arguments: --no-such-flag`,
    rc 2. Both before AC5 ran (verified: no pool call in either path).
13. Closed the change-management entry (committed `8c052605d9`, together with the surprise row):
    0 keys written, nothing to roll back.
14. Ran `.tools/proof-of-spec-check.py` on the instance below; recorded its exit code verbatim.

**Result: AC1-AC6, AC8 PASS-by-output; AC7 FAIL (REFUSED, measured, row filed). Task order
`<status>` stays `pending` -- not flipped to `complete` (a FAIL row leaves the order open).**
