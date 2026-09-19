# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~38, AMGT-rk-34

1. Bar check: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-38`; `git rev-parse --short=10 HEAD`
   -> `1ecea91b11`; `org/`, `.tools/` and every path in section 3 present. TREE-OK.
2. Dependency read (section 1.2): printed `_FIELD_MAP_PATH` ->
   `integrations/bloomberg/research/field_map.json`, `exists True`. Home is beside the producer,
   not under `org/missions/` -- rk-33 has landed. Landing commit: `git log -1 --format=%h -- <home>`
   -> `39e80692d9`. Schema (top-level keys): `securities`, `fields` (32 entries), `cross_security_findings`.
3. Read `model_block_pull.py` in full (`_resolved_unit`/`_resolved_sign`/`_field_map`, `stage_derive`,
   `cmd_derive`, `main()`'s 3-security cap), the proof-of-method builder
   (`deliverables/0.9.0_WK_AMGT_RESAPP~1/build_field_map.py`), `lib/research/checkface/run_checks.py`
   (`unit_status_for`), `lib/research/rules/figure.py` (`qualify`), and both never-widen ledger halves'
   AMGT-rk-34 sections in full before any live act.
4. AC1 PRE-ACT run: crosswalk `crosswalk/v1/2026-09-19.json`, `keyed_names 36` (moved from the cut's 33 --
   the 3 extra are the validation names, now identity-keyed with no raw). `names_with_block 33 of 36`,
   `REFUSE_NOT_YET_BUILT 348` with per_field matching the Model brief's cut figure exactly.
5. Wrote `integrations/bloomberg/research/build_unit_map.py` (RULED item 2's production builder):
   reads the producer's own bucket/mnemonics/security_key, keys per-security entries on the raw
   object's OWN top-level string (never reconstructed by replace), additive merge (never disturbs an
   existing MEASURED entry), UNRESOLVED-per-security entries carry the RULED item-3(b) literal contract
   text with a descriptive reason. Hardened `_stamps_with_refdata` against a stamp folder that carries
   no refdata.json (measured on the 3 validation names -- an identity.json-only landing; see surprise
   row S5) after the first cut crashed `NoSuchKey` against exactly this shape.
6. `--dry-run --securities "CAT US Equity" "CSL AU Equity" "6861 JP Equity"` -> 3 explicit UNRESOLVED
   terminal states, 0 bytes written (git status unchanged). `--dry-run --population crosswalk` -> 33 of
   36 WOULD-WRITE, 3 UNRESOLVED (the validation names).
7. Real run `--population crosswalk` (no `--dry-run`): wrote 32 field entries updated for 30 of 33 names,
   1-2 for the 3 already-mostly-measured pilots (SAP GY / BA US / BABA US Equity) -- verified no existing
   MEASURED pilot entry regressed (diffed pre/post field_map.json on the 4 previously-dict-shaped
   mnemonics). ASCII-only confirmed (0 non-ASCII bytes in both the map and the builder).
8. Opened change-management entry `amgt-rk34-unit-map-rederive-20260918` (3 legs) BEFORE the first
   derive write, per section 3.
9. Ran `model_block_pull.py derive` in 11 batches of 3 (F2/G-24 cap) over the exact 33 (sec_key, security
   string) pairs the raw itself carries (never the crosswalk's underscore form, per the CTO half's
   M-GAP-1 caution) -- every batch printed `DERIVE DONE: 3 of 3`, every derived block's
   `fiscal_year_row_count > 0` (8-10 FY rows each, none zero -- the M-GAP-1 empty-branch check).
10. AC1 POST-ACT run: `REFUSE_NOT_YET_BUILT 38` (not 0), per_field `CURR_ENTP_VAL 1, IS_DIV_PER_SHR 17,
    CAPITAL_EXPEND 10, PE_RATIO 10`; `REFUSE_OTHER 0`. Traced to the structural collision between RULED
    item 3(b)'s literal contract text and `unit_status_for`'s substring match (surprise row S2) --
    genuine per-security UNRESOLVED cases (BA US / NU US Equity zero-dividend IS_DIV_PER_SHR; BP/ LN
    Equity's out-of-band PE_RATIO; BBSE3 BZ Equity's ambiguous CAPITAL_EXPEND magnitude; one
    CURR_ENTP_VAL case) read NOT-YET-BUILT, never REFUSE_OTHER. AC1 recorded FAIL against its literal
    bar, per the REFUSAL CLAUSE -- not repaired (lib/ outside this order's `<paths>`; owner named by the
    CTO half's own M-DISAGREE-1(a) as "the L6 cut").
11. AC2 run: `securities_with_entry_for_every_mnemonic 33 of 36`, `missing_pairs 96` (all 3 validation
    names x 32 mnemonics, correctly absent). PLANTED_NO_ENTRY unchanged (`SEE field_map.json ... not yet
    built`, status `NOT-YET-BUILT`). FAIL against the literal "33 of 33 / missing_pairs 0" bar (crosswalk
    drift, surprise row S4).
12. AC3 run (post-act, live Lambda invoke on `opal-amgt-scoped-api`): all 3 names statusCode 200,
    CodeSha256 unchanged before/after (`baiKT5I+k7ciCX/rtQzYy7bTSWgApSeAXYtSZhe4fUE=`). BA_US_Equity and
    BP%2F_LN_Equity each carry `REFUSE_NOT_YET_BUILT 10` (same root cause as AC1); HD_US_Equity reads 0.
    The invocation's own `model_status` extraction (`inner.get('model')...`) is a no-op bug -- corrected
    read confirms `SERVED` on all three (surprise row S3). FAIL against the literal bar.
13. AC4 run: rc 0, all 3 explicit UNRESOLVED terminal states, `s3_unchanged True`, `map_bytes_unchanged
    True`, porcelain line count unchanged (3 before, 3 after). PASS.
14. Controls: mutant (dry-run against SAP GY Equity, raw present -> WOULD-WRITE, discriminating from the
    3 no-raw UNRESOLVED cases) FIRED-AS-EXPECTED; determinism (dry-run over the 3 validation names, run
    twice) STABLE, byte-identical sha256.
15. Filed 5 surprise rows (`AMGT_RESAPP-Z-W38-S1`..`S5`) in `INVESTIGATION_v1.md`, all class OBSERVATION /
    hazard_standing INERT.
16. Committed `9b43cd7baf` (build_unit_map.py, field_map.json, pre_act_stamps.json, the change-management
    open sentinel, the surprise rows). Closed all 3 change-management legs and the ledger entry; committed
    `e2c8deb5f8` (sentinel removal, post_act_stamps.json).
17. Wrote the proof_of_spec instance: AC1/AC2/AC3 FAIL (measured, with full reasoning and status_reason),
    AC4 PASS. `<status>` NOT flipped to `complete` -- a FAIL row leaves the order open per the harness
    contract; this is the final report on it.
