# SESSION LOG -- `0.9.0_WK_AMGT_RESAPP~47` on `AMGT-rk-45` (management-one-pool)

Worktree `/c/tmp/wk-amgt-14-47`, branch `wk-amgt-14-47`, cut from SITEZ HEAD `32c1d8ad4a`.

## 1. Bar check
- `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-47`; `org/`, `.tools/`, `lib/research/management/`,
  `lib/research/api/` all present -> TREE-OK.
- Worktree HEAD `32c1d8ad4afffba32edfbb5878e896a026356967` == SITEZ HEAD at spawn: `AMGT-rk-43`'s adapter
  change (commit `c4d4e43d08`, merged `12722614b2`) is already present, satisfying the sequencing clause
  ("do not edit scoped_amgt.py until the COO's continuation says rk-43 has drained").

## 2. Re-grounding
- Both never-widen halves read: `NEVER_WIDEN_ROUND14_CHAIN_E_COO_HALVES.md` (sha256
  `a41ead71ea87a409b19cbacbd0567eff47e68a93a5ecb4ec7327c11786e8d923`) and
  `..._CTO_HALVES.md` (sha256 `0e702e1f923fea87306693770cff2caf7434e717be30b419d301e6bcb2902f7d`).
  Both carry an `AMGT-rk-45` section; CTO half's RE-SIGNATURE (2026-09-18 ~23:3xZ) reads "WITHHOLDING
  LIFTED -- SIGNED" against the changed `compute_pool`.
- Scheduled task re-measured: `MSYS_NO_PATHCONV=1 schtasks /Query /TN OpalResearch-ExecManagement /XML` ->
  `<Enabled>false</Enabled>`.
- Lambda-artifacts bucket versioning re-measured: `aws s3api get-bucket-versioning --bucket
  opal-313476888478-lambda-artifacts` -> `{"Status": "Enabled"}`.
- Adapter single-writer queue check (issuer rule, run twice -- once before the build, once recorded in the
  ledger): `git log --oneline $(git merge-base HEAD SITEZ)..SITEZ -- lib/research/api
  lib/research/checkface infra/aws/lambda/research/scoped_amgt_api
  infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh` -> printed nothing both times.

## 3. Build
- `compute_pool()` (`lib/research/management/enrich.py`) rewritten: lists `management/v1/` once, groups by
  NAME via `rsplit("/", 1)` (never `split("/")[n]`, so `BP/_LN_Equity` groups as one name), keeps the newest
  dated object per name, counts `names_with_roster` only on RESOLVED + >=1 officer, recomputes each officer's
  tenure at the pool's own `as_of` via `roster.tenure_years(role_start, as_of)`. Meta gains
  `objects_listed`/`names_seen`/`newest_per_name`/`dates_spanned`.
- `read_universe()` rewritten to resolve the NEWEST `universe/v1/<date>.json` vintage (listing convention
  matching `read_pool_object`) when no explicit `universe_key` is given; `names_in_union` null only when no
  universe object exists at all.
- Pool object gains `universe_vintage` (string|null); `pool.schema.json` updated (`additionalProperties:
  false` closed, field added to `required`).
- `enrich.main()` gains `--pool-only` (security-key no longer required with it) + shared `_print_pool_lines()`
  helper used by both the pool-only and the normal write-pool branches.
- `lib/research/api/scoped_amgt.py:2431`: dropped `as_of=document.get("as_of")` from the pool `read_pool_object`
  call -- every served name now reads the NEWEST pool object.
- Tests: 6 new `PoolAverageTest` methods (same-name-two-dates, zero-officer-RESOLVED, slash-name, two-pool-
  objects, tenure-recompute, universe-two-vintages) + the 3 pre-existing tests restated for the new grouping/
  recompute semantics and new meta keys. `python -m unittest ...PoolAverageTest -v`: 9 of 9 OK. Full
  `test_management.py`: 47 of 47 OK. `commit-gate.sh` clean on all 4 changed `.py`/`.json` files.

## 4. Deploy (co-signed act)
- Ledger opened: `org/critical_paths/change_management/20260919T0530Z_amgt-rk45-one-pool_deploy_completion.md`
  (2 legs: L1 pool write, `opal-amgt-scoped-api` adapter redeploy).
- AC2 (pre-act count bar): 14 keys, 12 names, 7 names_with_officers_across_dates -- matches the order's own
  cited cut figures exactly.
- AC3 (dry `--pool-only`): `pool_avg_tenure_years 4.09 names_in_union 250 names_with_roster 7
  officers_with_role_start 40 universe_vintage 2026-09-16`; meta `objects_listed 14 names_seen 12
  newest_per_name 12 dates_spanned 2` -- matches the order's cited cut figures.
- SURPRISE (row `AMGT_RESAPP-Z-W47-S1`): the halves describe the pool write as an in-place OVERWRITE of
  today's null-valued key (true at the 2026-09-18 cut); this worker's UTC today is 2026-09-19 and
  `management/v1/_pool/2026-09-19.json` was a fresh 404, not an overwrite. Recorded in the ledger; per-key
  rollback restated as `delete-object`, not re-put.
- AC4 (`--pool-only --write-pool`): wrote `management/v1/_pool/2026-09-19.json`, read back byte-identical
  to AC3's dry line in every field (sha256 `dee6a647358af0ca...`). Post-act key count 15 = pre-act 14 + 1 new
  key, every other key unchanged (listed and diffed).
- Adapter redeploy: build-and-upload-scoped-amgt.sh -> new VersionId `Av11PsPOZh87INPUaV10ic2t4Gd8MtAf`, local
  sha256 `baiKT5I+k7ciCX/rtQzYy7bTSWgApSeAXYtSZhe4fUE=`. First `safe-apply` attempt refused at the fabric-wide
  HALTGT checkpoint (182 pending routine messages, none STOP-class, none naming AMGT_RESAPP/scoped_amgt --
  all unrelated `deploy_ledger.py` gate-bypass backlog + CRO harvest-topic threads to other seats). Re-ran
  `HALT_ACK=1` per the gate's own documented unblock; apply succeeded: `Apply complete! Resources: 0 added,
  1 changed, 0 destroyed.` Post-act `get-function-configuration`: CodeSha256
  `baiKT5I+k7ciCX/rtQzYy7bTSWgApSeAXYtSZhe4fUE=` (pre-act `OOsJzs7BDkgtOUogdG39/BZNw3PlRrLatxCFVI528qY=`),
  matches the uploaded artifact exactly. Targeted 0-diff replan: "No changes." Verify-on-served: queried the
  LIVE API Gateway directly (`aws apigatewayv2 get-routes --api-id 7k3ed8px20`) for the true route set -- 13
  GET + 3 POST, matching the rk-19/rk-43 precedent's "13 of 13 GET routes" shape (an earlier partial census
  against the Terraform module's own output block undercounted at 8; corrected in the ledger). 13 of 13 GET
  routes invoked live post-act, 0 FunctionError, LOST=[].
- AC5: `BA_US_Equity` (2026-09-15 object) and `NU_US_Equity` (2026-09-18 object) both serve
  `pool_read.object_key management/v1/_pool/2026-09-19.json`, same `pool_avg_tenure_years 4.09`, same
  `pool_denominator`; planted `HOLLOW_NONEXISTENT_KEY_Equity` serves `management_status ABSENT`, `pool_avg
  null`.
- Both ledger legs closed with full proof; `deploy_ledger.py close` -> CLOSED, sentinel removed. Post-close
  correction appended naming the true 13-GET-route count.

## 5. Full test sweep
- `python -m pytest lib/research/api/tests/ -q`: 158 passed, 2 failed -- the SAME two pre-existing failures
  AMGT-rk-43 documented (row `AMGT_RESAPP-Z-W45-S3`), both on the superseded `ceo_profile_reading` sentence-
  parsed contract, unrelated to this order's pool/adapter change. Confirmed test_13's own
  `pool_avg_tenure_years` assertion still passes (coincidentally, since its two planted pool dates make
  "newest" and "the name's own as_of" the same date) -- filed as row `AMGT_RESAPP-Z-W47-S2` since the test's
  comment now states a rationale ("the name's own as_of, not the other one") this order's change retires.

## 6. Commits (this worktree, branch `wk-amgt-14-47`)
- `cb20dc2b91` -- code: `enrich.py`, `pool.schema.json`, `test_management.py`, `scoped_amgt.py`.
- (this commit) -- ops: ledger entry, surprise rows, proof-of-spec instance, this session log, task-order
  `<status>` flip.

## 7. Rows filed
- `AMGT_RESAPP-Z-W47-S1` -- pool key pre-act ABSENT (fresh key), not an overwrite as the halves describe.
- `AMGT_RESAPP-Z-W47-S2` -- `lib/research/api/tests/` `test_13`'s comment/fixture no longer discriminates
  newest-object-per-name from same-as_of after this order's adapter change.
