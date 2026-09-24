# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~39 on AMGT_RESAPP.TO-AMGT-rk-35 (rolling history window)

Worktree: `/c/tmp/wk-amgt-14-39`, branch `wk-amgt-14-39`, cut from SITEZ HEAD `bdaf6431a2`.

1. Verified tree grant (`org/`, `.tools/`, every section-3 path) present. Read both never-widen
   halves for chain M (`NEVER_WIDEN_ROUND14_CHAIN_M_{COO,CTO}_HALVES.md`), confirmed `AMGT-rk-35`
   SIGNED in both, hashed both files fresh (COO `594ba746e3ad48da...`, CTO `db0e1bbaffeef441...`).
2. Ran the section-1.2 dependency check: `build_unit_map.py` present, `_FIELD_MAP_PATH` resolves
   beside the producer (not a worker folder) -- rk-34/rk-33 landed as required. Builder landing
   hash `162435481b`.
3. Re-read `model_block_pull.py` at HEAD (line numbers had moved from the order's draft-time
   citation, as flagged): the pull-log C-PRODUCTION-HOME item (RULED 5) was ALREADY fixed by
   rk-33 (`39e80692d9`) -- filed nothing new for it (AC1's `pull_log_literal_in_source 0` already
   held before this cell's edit); moved straight to items 1-4 and 6.
4. Built: rolling end date (`_rolling_end_date`), CLOSED-fiscal-year derive split
   (`_STATEMENT_FIELDS`, `_FY_NOT_CLOSED_REASON`, `history_window`), unit-map-at-instantiation
   (`_ensure_unit_map` calling `build_unit_map.build_entries`), required `--securities`, `--dry-run`
   for both stages. Verified against a synthetic CSL/Keyence-shaped fixture (in-memory fake S3,
   `.scratch/unit_test_stage_derive2.py`) BEFORE any live act: closed/excluded split correct,
   `history_window` correct, `check_block` REFUSE_NOT_YET_BUILT 0.
5. Found (fixed in the same edit, before commit): `_ensure_unit_map`'s `field_map.json` write used
   `Path.write_text` without `newline="\n"`, which CRLF-ifies on this device (pre-existing in
   `build_unit_map.py`'s own writer, carried into HEAD's committed `field_map.json` -- 10292 CRLF
   bytes already there). Fixed my own call site and normalized `field_map.json`'s existing bytes
   to LF before committing (content unchanged, JSON re-validated).
6. Opened change-management entry `amgt-rk35-rolling-window-validation-names-20260918` (3 legs)
   BEFORE the live pull. Recorded `pre_act_stamps.json` (36 crosswalk-keyed names, fresh read)
   before any live act. Committed L1 (code) at `f3175defae`.
7. Live act: `pull` then `derive` on exactly `"CAT US Equity" "CSL AU Equity" "6861 JP Equity"`
   (six Bloomberg requests total, two per name). Ran AC1 (dry-run, pre-act) through AC4
   (post-derive) verbatim per the order's invocations.
8. AC4's literal script counts the 3 validation names among the crosswalk's covered-name
   population (they are now identity-keyed there, landed by a parallel R14-I1/rk-31 cell before
   this order's own live act, exactly as the never-widen COO half anticipated: "Both orderings are
   covered"). Recorded the measurement honestly (served_stamps_moved 3, all three being the
   validation names themselves; the OTHER 33 names show 0 movement) and marked AC4 FAIL against
   its literal bar per the REFUSAL CLAUSE, filing row `AMGT_RESAPP-Z-W39-S1`.
9. Filed `AMGT_RESAPP-Z-W39-S2` for a pre-existing, unrelated defect found while censusing every
   consumer of `model_block_pull.stage_pull` before editing it: `pull_consumer.py` calls it with
   4 positional args against a 3-parameter signature (predates this order, out of its RULED scope).
10. Closed all 3 change-management legs and the entry. Wrote and validated the proof-of-spec
    instance.
