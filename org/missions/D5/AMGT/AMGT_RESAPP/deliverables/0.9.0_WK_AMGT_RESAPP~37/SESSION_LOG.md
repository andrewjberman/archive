# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~37 on AMGT-rk-33 (C-PRODUCTION-HOME)

Worktree `/c/tmp/wk-amgt-14-37`, branch `wk-amgt-14-37`, cut from SITEZ HEAD `047aee5478`.

## Sequence

1. Verified the worktree bar (`git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-37`; `org/`, `.tools/`,
   `lib/opal_naming.py`, `infra/logic/registry/` all present; TREE-OK).
2. Verified the `sec` VENDOR row is present in `infra/logic/registry/systems.json` (landed before spawn,
   per RULED 1 -- confirmed, no edit made to the registry).
3. Ran AC1's builder invocation BEFORE any code edit (the discriminator): SEC bronze address builds into
   `s3://opal-data-assets/...` (REFUSED-BY-REGISTRY per the issuer amendment -- bucket is not
   `opal-data-harvest`); candidate-universe gold address builds into `s3://opal-data-harvest/...` (LIVE --
   bucket exists, confirmed via `head_bucket`).
4. **Unit map**: copied `deliverables/0.9.0_WK_AMGT_RESAPP~1/field_map.json` byte-for-byte to
   `integrations/bloomberg/research/field_map.json`; repointed `_FIELD_MAP_PATH` beside the producer;
   retired the cumulative repo `pull_log.json` write, replaced with one `raw/bloomberg/<KEY>/<stamp>/
   pull_log.json` object per pull (put-if-absent, beside the raw landing it records).
5. **SEC cache**: added `sec_table_address()` / `sec_table_prefix()` (builder-derived, never typed) and
   rewrote `load_sec_cache()` to read the newest pool partition, REFUSING LOUDLY (never falling back to a
   repo path) when the partition is absent -- which it genuinely is, since the registry gate forbids
   writing the landing to `opal-data-assets`. Removed `SEC_CACHE_DEFAULT` and the `~19` literal. Added test
   arms in `test_union_universe.py` (local/env override honoured; absent-pool-object loud refusal, mocked,
   no network).
6. **Peer candidate universe**: added `candidate_universe_address()`; made `cache_path()` a pure
   resolution (pool-address-derived local read-cache, or an unhomed scratch path on a builder refusal, never
   a worker's deliverables folder); made `fetch_factor_metadata()` and `load_candidate_universe()` NEVER
   write on a read (removed the `_write_json` call the D24 defect named); added `refresh_candidate_universe()`
   as the ONLY writer (write local + land pool + read back), wired into `main() --refresh`. Removed the `~21`
   literal. Added the AC4-shaped negative arm to `test_peers.py` (a stale cache file passed via the LOCAL
   override is rebuilt in memory and never rewritten).
7. Performed the ONE-TIME LIVE LANDING for the candidate-universe cache (the negative/LIVE arm): read the
   currently-committed `~21/candidate_universe.json` bytes, landed them unchanged at
   `s3://opal-data-harvest/amgt/harvest/gold/candidate_universe/date=2026-08-06/candidate_universe.json` via
   `crosswalk.write_pool` (put + head-readback, sha256 `934ba4783731f431...`), and materialized the local
   read-cache mirror so `cache_path()` resolves to an existing, openable file.
8. Ran AC4 TWICE: BEFORE (original unmodified `universe.py`, restored from `.scratch/universe.py.orig`)
   showed `stale_file_unchanged False, cache_sha256_written True` (the D24 bug, reproduced); AFTER (the fixed
   code) showed `stale_file_unchanged True, cache_sha256_written False` (fixed). Both recorded verbatim.
9. Ran AC5: negative arm confirmed (`ADDRESS` printed, `bucket_exists True`, `warn_lines 0`).
10. Ran AC6's census: 50 hits across 25 files remain naming a worker folder; the three PRD-named instances
    are ABSENT as required. Filed as residue (row S2).
11. Ran AC7: both unit suites OK (37 + 27 tests), `validate` -> `VALIDATE: OK`, `generate --out .scratch/gen`
    diagnostic run. Found the `sec` VENDOR row adds NO vector diff (mark-line only on `vectors.json`), but the
    already-landed `harvest` PRODUCT scope row (inserted before `etfs` per its own note) shifts the
    `refuses_product_scope` vector's scope from `etfs` to `harvest` in `opal_name.tftest.hcl` -- MORE than the
    mark line. Per RULED 1's own instruction ("if anything beyond the mark line changes, STOP and file a
    row"), did NOT regenerate either tracked GENERATED file into the tree; filed row S4.
12. Filed FOUR surprise rows total: S1 (the SEC registry-gate refusal, ARMED, disarm owner
    `1.0.0_SA_CTO~Z`), S2 (the AC6 residue census), S3 (AC2's own expect text states 36 fields; the source
    artifact carries 32 -- a discrepancy in the order's stated expectation, not this cell's act), S4 (the
    vector-selection side effect above).
13. Graded AC3 (SEC live landing) and AC7 (generated-file byte equality) as NOT PASS-by-output given the
    measured state above; left `<status>` at `pending` (not flipped to `complete`).

## Files touched (within `<paths>`)

- `integrations/bloomberg/research/model_block_pull.py` (modified)
- `integrations/bloomberg/research/field_map.json` (new, byte-for-byte copy)
- `lib/research/identity/build_universe.py` (modified)
- `lib/research/identity/tests/test_union_universe.py` (modified, new test arms)
- `lib/research/peers/universe.py` (modified)
- `lib/research/peers/tests/test_peers.py` (modified, new test arm)
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` (4 rows appended)
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~37/` (this log + the proof instance)

Not touched: `infra/aws/terraform/modules/opal_name/tests/vectors.json`,
`infra/aws/terraform/modules/opal_name/tests/opal_name.tftest.hcl` (both left at their committed HEAD bytes
per the REFUSAL CLAUSE -- see row S4), and
`org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-rk-33.production-home.md` (`<status>`
stays `pending`).
