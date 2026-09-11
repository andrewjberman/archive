# AMGT-s-4 -- session log

Worker `0.9.0_WK_AMGT_RESAPP~3`, task order
`AMGT_RESAPP.TO-AMGT-s-4.coverage-reader-non-sa-sources.md`, same worktree/branch as AMGT-s-12
(`wk-AMGT_RESAPP-1-3`), fast-forwarded to SITEZ @f8c76bd3a4 before this cell began.

## Sequence

1. Tree check, status flipped `staged` -> `pending`.
2. Read the dependencies: `lib/research/identity/resolver.py` (my own AMGT-s-12 output --
   `resolve()`, `render_together()`), `lib/research/rules/item.py` (AMGT-s-11's item rule,
   `held_back`, threshold `None`), the CRO's F11 fixture shape (s.3 of
   `AMGT_RESAPP_LAMBDAS_PEERS_IRSCAN_20260910.md`), and the live store's `raw/seekingalpha/`
   layout via `integrations/seekingalpha/config.json` and
   `deliverables/0.9.0_WK_AMGT_RESAPP~9/check_landing.py` (bucket `opal-data-research`, prefix
   `raw/<vendor>/<security_key>/` -- an S3 prefix, not a local path).
3. Built `lib/research/coverage/reader.py`: `extract_display_domain()` (F11, part b),
   `_identity_gate()` (C-IDENTITY-RESOLVED, exercised via `resolver.render_together` -- not
   re-implemented as a bare if-check), `_build_item()` (applies AMGT-s-11's item rule),
   `read()` (ties it together, ranks recency-desc-then-mentions-desc), and
   `check_no_shared_item_sets()` (part c, the unscoped pass, C-SHARED-DEFECT).
4. Built `lib/research/coverage/ir_scan.py` (part d): `build_query()` and `parse_serp_results()`,
   exercised only on the fixture; docstring states verbatim the three substrings AC4 checks for
   (`per-use word`, `G-24`, `not run by AMGT-s-4`) -- no network call anywhere in the module.
5. Built `lib/research/coverage/fixtures.py`: the CRO's own F11 sample verbatim
   (`F11_SAP_FIXTURE`), plus per-security IR/publication fixtures for the three securities
   `AMGT-s-b4` had already selected in its own `run_manifest.json` (`BABA_US`, `BA_US`,
   `COST_US`) -- reused rather than re-derived (filed as `AMGT_RESAPP-Z-W3-S3`, OBSERVATION,
   since the order left the selection open).
6. Wrote `lib/research/coverage/tests/test_reader.py`, AC1's five behaviours as five pytest
   functions -- PASSED on the first correct run (`5 passed`).
7. Built `lib/research/coverage/run_reader.py`: reads the three securities' identities via
   `resolve()`, reads `raw/seekingalpha/<security_key>/` via boto3 (0 keys at every one, as the
   coordinator's message stated -- `AMGT-s-b4` proxy-blocked at the TLS layer, row
   `AMGT_RESAPP-Z-W9-S2`), runs `check_no_shared_item_sets()` across the whole population BEFORE
   writing any file, then writes `coverage_items_<security_key>.json` x3 and `run_summary.json`.
8. Result: 3 securities, 4 items attached (2 `publication` for BABA_US -- one PROVISIONAL, one
   REFUSE by the item rule's own honest logic on the fixture's tag shape; 1 `publication` PASS
   each for BA_US and COST_US), 0 SA raw keys found (recorded, not hidden), 1 `ir`-class item
   dropped per security (identity-gated: `ir_domain` is UNRESOLVED for every one of the 89 names
   at this cut, per AMGT-s-12 bound d -- a real, honest consequence, not a bug in this reader).
9. AC1-AC6 all PASS-by-output on the first correct run of each (AC5/AC6 each run in their own
   Bash call per the coordinator's rail note).
10. Wrote `SPEC_SECTION_coverage.md` (part e) for `AMGT-s-5`'s design spec: the coverage panel's
    data shape, the honest-state rendering rule for `PASS`/`PROVISIONAL`/`REFUSE` (never hide
    `PROVISIONAL` behind `PASS`'s styling), and why an empty IR/SA section today is correct, not a
    defect.

## AC7 (judgment) -- read for the CVO

`coverage_items_BABA_US.json`'s ranked list (SA raw empty at this run, stated with reason in
`run_summary.json`): a Reuters piece dated 2026-09-08 (PROVISIONAL, `mentions: 3`) ranks above a
Bloomberg sector roundup dated 2026-09-01 (REFUSE, `mentions: 10`) -- recency wins over mentions
exactly as designed, and this is the order an analyst would expect ("most recent" first). Every
non-PASS verdict carries a `rule_reason` a reader can act on without opening the source: the
PROVISIONAL item's reason names the missing tag data ("not found in this item's tags at all --
cannot determine aboutness"); the REFUSE item's reason names the broad tag list it was found in
("appears only in a broad affected_tickers tag list of 3 names ... contains the string, not ABOUT
the security"). The `ir`-class item's absence is not silent: `identity_dropped` names the exact
identity key (`ir_domain`) and quotes `render_together`'s own refusal text. The SA half is stated
absent with reason (`sa_raw_keys_found: 0`, `AMGT-s-b4` proxy-blocked, row `AMGT_RESAPP-Z-W9-S2`),
not omitted from the summary.

## What is NOT done (declared, not hidden)

- The live IR SERP scan: built, not run (bound: no G-24 word carried by this order).
- SA content: read, not fetched; 0 objects exist to read at this run.
- No `.tsx`: `SPEC_SECTION_coverage.md` is a data/behaviour spec only (C-DESIGN-SPEC-FIRST).
