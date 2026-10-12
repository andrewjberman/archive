# STORE_WRITER -- what wrote the Cottonwood price store object (CB-ca-3, round 79)

Object: `s3://opal-data-cot/silver/prices/canonical_prices.parquet` (key as named in `infra/logic/registry/legacy_addresses.json:11-13`
and `data/assets/scripts/analysis/commonwealth_price_census.py:57-58`). Record: `STORE_WRITER.json`.

## 1. The versions (one listing of the one key: 2 entries, both the exact key, 0 delete markers)

| version | last modified (UTC) | size | rows | current | columns | sources |
|---|---|---|---|---|---|---|
| 76.rgWIXYdLNsXSwrXvyuEmaEtfr9y98 | 2026-10-09T13:41:04Z | 97,443,387 | 11,289,398 | yes | date, asset_name, ticker, price, source | linear_interpolation 7,831,140; yahoo_finance 3,396,067; transaction_observed 50,143; scoped_override 12,042; transaction_observed_capped 6 |
| 5JN8rkV4dcE.v64dYVAA6PR5jccvS8Rc | 2026-06-09T20:42:16Z | 97,633,099 | 11,291,021 | no | same five | the same, plus bd_txn_price 1,623 |

Changed between them: no column added or removed; 1,623 rows removed, all `bd_txn_price` (3 pseudo-identifier tickers, 2024-01-24 to 2026-06-09);
every other row identical on all five columns (11,289,398 of 11,289,398); the 12,042 `scoped_override` rows identical; date range 2006-01-02 to
2026-06-09 in both. The 15 funds: 31,985 rows in each version, 0 changed by more than 0.1 percent, 0 in one version only: `the_15_changed_fund_days` = 0.
The live object's sha256 (51a1f1f7e19a0ce3...) equals the `sha256_after` of the CB-aj-1 manifest for this key.

## 2. Which code

- The live shape (five columns, no `source_firm`, `scoped_override` rows) IS the June shape. `source_firm` was added by `298721a585` at 2026-10-09
  14:06:13Z, 25 minutes after the live write.
- `scoped_override` and `bd_txn_price` are assigned only by `data/black_diamond/scripts/silver/inject_scoped_overrides.py` (and `bd_price_update.py:449`
  for the former). The cot builder `data/cot/scripts/gold/build_canonical_prices_v2.py` auto-chained that injector (commit `29a831ae0e`, 2026-04-10; present in
  the cot seed `6b0be4337e`) until `319a716cb4` (2026-06-12) removed it; the cot tree never held an injector. Sweep denominators: `scoped_override` 609 hits
  across 75,998 files (repo), 12 hits across 6,451 files (data/cot, data/mdpf, data/assets, infra/aws/lambda, cot-pipeline terraform); `canonical_prices`
  119 hits across 6,451 files.
- `code_that_matches_the_live_shape`: builder + bd injector as of the cot seed, `6b0be4337e..d892fe5001` (before `319a716cb4`); `matches` = not_established,
  because no cot-tree file alone produces `scoped_override`, and the deployed cot mirror (`code/gold/`, `code/silver/`) was NOT read.

## 3. Which run, whose

- LIVE version: a version-gated put of the CB-aj-1 locally filtered file by `0.7.0_AE_CloudOps~CB2` for TO-CB-aj-2, issued by `2.0.0_SA_COO~C2`, ledger
  `org/critical_paths/change_management/20261009T1320Z_advi-cotbkf-cot-price-rewrite-cb-aj-2-20261009_deploy_completion.md` leg W1 (the same sha256 and both version
  ids); bytes built by `0.9.0_WK_ADVI_COTBKF~64`. Not a builder run.
- EARLIER version (2026-06-09T20:42:16Z): no record in the tree; `run.non_current_version_run.whose` = not_established. It shares a two-second window with 37 daily
  price files the cot builder does not write. CloudTrail PutObject for the key, the 2026-06-09 SSM command history, or the gold-run log under
  `s3://opal-data-cot/logs/cot-exporter/gold-run/` would settle it; none was read.

## 4. Owner today

Not established as an owner of record for the object: `comp-estate --resource canonical_prices` names only the 49 Financial store chains (`advi-bd /
bd-canonical-prices`, `bd-historical-prices`); the Cottonwood names are SUBJECT_ABSENT_FROM_CORPUS (135 of 135 chains). The registry row's reader is ADVI_COTBKF
(active, dell2); the writer was built by the closed ADVI_COTETL and ADVI_GLDOPS.

Remote reads: 1 `list-object-versions` and 1 `get-object --version-id` on this one key. No write, delete, restore, head or other key.
