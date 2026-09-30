# SLASH_SAFE_SITES_ROUND24 -- CRPS-z-4 (0.9.0_WK_AMGT_CORPUS~4)

Rule applied: every per-security PATH segment is built with `crosswalk.slash_safe_key(<key>)`; the identity value
inside a document keeps its slash. A slash-free key's path is byte-identical (control in
`lib/research/identity/tests/test_slash_safe_key_sites.py`). Code only: no S3 read or write, no object move, no deploy.

Census (`z4_check.py`): 24 functions at base = 14 ROUTED + 10 MARKED. After: `sites 14 encoded 14 raw 0`.

## A. ROUTED -- census functions (14)

| # | File : function | What it builds | CONSUMER (who reads what it writes / who writes what it reads) |
|---|---|---|---|
| 1 | `lib/research/api/scoped_amgt.py` : `resolve_identity` | `model_block_<enc>.json` under `AMGT_MODEL_BLOCK_ROOT` (landed-artifact surface) | every `/security/{key}/*` route (RESAPP scoped API); the file is written by the model-block landing (RESAPP `0.9.0_WK_AMGT_RESAPP~1/model_block_*.json` shape) |
| 2 | `lib/research/drafting/run_drafting.py` : `main` | `coverage_items_<enc>.json`, `model_block_<enc>.json`, `drafted_sections_<enc>.json` in the RESAPP `~3` / `~1` deliverables dirs | RESAPP AMGT-s-9 drafting deliverable (`0.9.0_WK_AMGT_RESAPP~3/drafted_sections_*.json`) read by the AC2 checker |
| 3 | `lib/research/filings/analyze.py` : `write_outputs` | `drafting/v1/<enc>.json` (pool + `--out-dir` copy) | `scoped_amgt._read_drafting_document` (drafting tab); `posture/packs.build_pack` (D-1) |
| 4 | `lib/research/filings/drafting_build.py` : `_drafting_pool_key` | `drafting/v1/<enc>.json` (splice driver read/write) | same as 3 |
| 5 | `lib/research/freshness/build_view.py` : `build` | `packs/<enc>/` listing for the freshness stamp | freshness view rows (RESAPP freshness tab); reads what `ledger`/`pull_consumer` write under `packs/<enc>/` |
| 6 | `lib/research/ledger/ledger.py` : `_ledger_key` | `packs/<enc>/input_ledger.json` (read + write) | `scoped_amgt.read_input_ledger` (RESAPP ledger route) reads it |
| 7 | `lib/research/peers/engine.py` : `_load_model_block` | local `model_block_<enc>.json` (pool-first read stays in `peers/universe.py`, see row S6) | peers ranker; writes `peers/v1/` (row 8) |
| 8 | `lib/research/posture/judge.py` : `run` | R-1 read `peers/v1/<enc>/<as_of>.json`; (also `pool_key` -> `posture/v1/<enc>/<as_of>.json`) | `scoped_amgt` posture route (`read_pool_object(POSTURE_PREFIX, key)`) reads `posture/v1/<enc>/`; reads what the peers engine wrote |
| 9 | `lib/research/posture/packs.py` : `load_model_block` | local `model_block_<enc>.json` | posture pack builder (`build_pack` -> judge) |
| 10 | `lib/research/posture/packs.py` : `build_pack` | `drafting/v1/<enc>.json`, `management/v1/<enc>/<as_of>.json`, `peers/v1/<enc>/<as_of>.json` (via one `safe_key`) | posture judge; reads what analyze (3), enrich (11) and the peers engine wrote |
| 11 | `lib/research/social/collect.py` : `ledger_path` | local job-ledger file `<enc>_<as_of>.json` (no directory made from the key) | the social collector's own resume path (`collect.run`) |
| 12 | `integrations/bloomberg/research/derive_fye_fixed.py` : `derive_one` | `derived/model_block_fye/<enc>/<stamp>/model_block_fye.json` | `check_join_fye.py` (RESAPP AMGT-r-1 AC2) reads the served block back |
| 13 | `integrations/bloomberg/research/model_block_pull.py` : `stage_derive` | `derived/model_block/<enc>/<stamp>/model_block.json` (and the dry-run message in `cmd_derive`) | `scoped_amgt._read_model_block_pool` / `read_model_block_versions` / `compare_model_blocks`; `run_scores._latest_model_block`; `peers/universe` index; `corpus/dossier` (see row S6) |
| 14 | `integrations/bloomberg/research/pull_consumer.py` : `_write_status` | `packs/<enc>/status.json` (get + put) | the pull consumer's own status merge; freshness view (5) |

## B. ROUTED -- per-security path sites the census could not see (module-constant prefixes; see row S7)

| File : function | Path | Consumer |
|---|---|---|
| `scoped_amgt.py` : `read_pool_object` | `<prefix><enc>/` for peers, management, scores, posture | RESAPP scoped routes (peers, management, scores, posture); pairs with writers 8, 10, `enrich.management_key`, `run_scores` |
| `scoped_amgt.py` : `_read_model_block_pool` | `derived/model_block/<enc>/` newest stamp | RESAPP Model tab (`read_model_block`); pairs with writer 13 |
| `scoped_amgt.py` : `read_model_block_versions`, `compare_model_blocks` | `derived/model_block/<enc>/[<stamp>/model_block.json]` | RESAPP versions / compare routes |
| `scoped_amgt.py` : `read_input_ledger` | `packs/<enc>/input_ledger.json` | RESAPP ledger route; pairs with writer 6 |
| `scoped_amgt.py` : `_read_drafting_document` | `drafting/v1/<enc>.json` AND the local `AMGT_DRAFTING_ROOT/<enc>.json` (replaces the earlier `'/'->'-'` local replace, now one encoding for both) | RESAPP drafting tab; pairs with writers 3, 4 |
| `management/enrich.py` : `management_key` | `management/v1/<enc>/<as_of>.json` (used by `write_document`, `_read_management_object`, `proxy_officers`) | `scoped_amgt` management route; `posture/packs` (10) |
| `management/enrich.py` : `compute_pool` | READER: maps a listed partition back to its identity with `security_key_from_slash_safe` (a legacy raw-slash name is kept as found), so both forms of one name group as ONE name across the move window | `management/v1/_pool/<as_of>.json` (consumed by `scoped_amgt` + `posture/packs`) |
| `peers/engine.py` : `pool_key` | `peers/v1/<enc>/<as_of>.json` | `scoped_amgt` peers route; `posture/judge` (8); `run_scores._latest_peer_set` |
| `scores/run_scores.py` : `_latest_model_block`, `_latest_peer_set`, `run` | `derived/model_block/<enc>/`, `peers/v1/<enc>/`, `scores/v1/<enc>/<as_of>.json` | `scoped_amgt` scores route (`read_pool_object(SCORES_PREFIX, key)`) |
| `model_block_pull.py` : `_model_block_keys_in_store` | READER: decodes a stored segment to its identity; legacy raw-slash partition kept as found (marked, see C) | the admit / corpus backlog "which names already have a block" join |

Inverse used for readers: `crosswalk.security_key_from_slash_safe` exists (exact inverse of `slash_safe_key`); it is used
in `compute_pool` and `_model_block_keys_in_store`. A raw-slash segment cannot be an encoded form (the inverse refuses
`/`), which is how the two forms are told apart during the round-25 move window.

## C. MARKED `# slash-safe: not a per-security path (<reason>)` (10)

| File : function | Reason (verbatim on the marker line) |
|---|---|
| `lib/research/identity/crosswalk.py` : `_record_for` | the packs/ and derived/ literals are provenance PROSE naming where the key form was measured; the record builds no path |
| `lib/research/management/enrich.py` : `reproject_public_profile` | builds no per-security path itself -- the read and write go through `management_key` |
| `lib/research/management/enrich.py` : `research_stored_ceo` | same |
| `lib/research/management/enrich.py` : `rederive_roster_reason` | same |
| `lib/research/management/enrich.py` : `main` | literals are `--help` text and the SKIP-POOL message; every write and read goes through `management_key` |
| `lib/research/peers/engine.py` : `resolve_subject` | the `model_block_%s.json` literals are reason text; the read goes through `_load_model_block` |
| `lib/research/peers/engine.py` : `run_batch` | literals are log/help text; the write goes through `pool_key` |
| `lib/research/peers/engine.py` : `main` | literals are help text; the write goes through `pool_key` |
| `lib/research/scores/run_scores.py` : `_robustness_record` | builds no path -- the literal is the reason text of an ABSENT record |
| `integrations/bloomberg/research/model_block_pull.py` : `_model_block_keys_in_store` | a PREFIX listing; it DECODES each stored segment with `security_key_from_slash_safe` and builds no per-security path |

## D. AMGT_RESAPP files for the round-25 deploy

The scoped-API deploy (Terraform `infra/aws/terraform/harvest/scoped-amgt-api.tf`, package built by
`build-and-upload-scoped-amgt.sh` -- both outside this worktree's sparse cone, named from the change-management ledger
history) ships **`lib/research/api/scoped_amgt.py`**, which this cell changed at: `resolve_identity`, `read_pool_object`,
`_read_model_block_pool`, `read_model_block_versions`, `compare_model_blocks`, `read_input_ledger`,
`_read_drafting_document`. Its closure already imports `lib.research.identity.crosswalk` (line 115) and this cell adds no
new import to it, so the closure is unchanged. RESAPP deliverable files the code reads or writes by key: 
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~1/model_block_<key>.json` and
`.../0.9.0_WK_AMGT_RESAPP~3/{coverage_items,drafted_sections}_<key>.json` (`run_drafting.main`, slash-free names only today, unchanged).

Readers OUTSIDE this order's paths that still build a raw per-security path (filed as `AMGT_CORPUS-Z-W4-S6`, for the
round-25 move): `lib/research/peers/universe.py` (`model_block_pool_index` keys by the stored segment;
`read_model_block_from_pool` looks up the identity) and `lib/research/corpus/dossier.py` (:927, :966). `lib/research/filings/fetch.py:472
pool_key` is a label, never dereferenced.

## E. Tests

`lib/research/identity/tests/test_slash_safe_key_sites.py`: 70 cases -- each routed writer and reader for `BP/_LN_Equity` and
`BRK/B_US_Equity`, each with the slash-free control `CAT_US_Equity`; both-forms grouping in `compute_pool` and
`_model_block_keys_in_store`; a legacy raw-slash file is not read by `resolve_identity`.
