# bd_txn_provenance -- how the price-source label entered the cot price store

Bucket: opal-data-cot (only bucket touched). Label: bd_txn_price. CUSIPs: 05613L3H2, 95000U2D4, 651639AX4

## 1. Store object head-object

- ContentType: binary/octet-stream
- ETag: "d51cec565b57c7300acdb17d2d830a35-12"
- VersionId: 5JN8rkV4dcE.v64dYVAA6PR5jccvS8Rc
- LastModified: 2026-06-09 20:42:16+00:00
- ContentLength: 97633099
- ServerSideEncryption: AES256
- Metadata (x-amz-meta-*): {}
- parquet created_by: parquet-cpp-arrow version 23.0.1; num_rows: 11291021; row_groups: 11
- parquet schema: ['date', 'asset_name', 'ticker', 'price', 'source']
- parquet schema metadata keys: ['pandas']
- parquet non-pandas schema metadata: {}

## 2. Scan

list_object_versions fully paginated: 67505 versions across 7790 distinct keys scanned.

Parquet versions read (source/cusip/ticker columns only; price-lineage filter): 89 of 67505 versions

### Keys with rows (earliest first)

| key | version | LastModified | rows | size | latest |
|---|---|---|---|---|---|
| silver/prices/2026-04-14.parquet | fGDQqialTgvN2alIUQLhQABTfk5c3Bxu | 2026-06-09T20:42:15+00:00 | 3 | 277915 | True |
| silver/prices/2026-04-16.parquet | caXhQHwomxRDe9Avx41lKomKbjCUA00b | 2026-06-09T20:42:15+00:00 | 3 | 281297 | True |
| silver/prices/2026-04-17.parquet | czKjJFbHforLgeJ3tM.JRH.7pEPmSGGk | 2026-06-09T20:42:15+00:00 | 3 | 281294 | True |
| silver/prices/2026-04-20.parquet | TwJXQ8zV8U1euL1jTwACFuvZEgqnqkgH | 2026-06-09T20:42:15+00:00 | 3 | 281443 | True |
| silver/prices/2026-04-21.parquet | JrzcHd773qTIxPW3jNoUHIhU2Y3C2DbD | 2026-06-09T20:42:15+00:00 | 3 | 280687 | True |
| silver/prices/2026-04-22.parquet | B9X2y1p8EsDlUOusorKGhkn3qSOeDoiY | 2026-06-09T20:42:15+00:00 | 3 | 278575 | True |
| silver/prices/2026-04-23.parquet | mbuwkdfSEll7X0Yx5t6pdJeG9KBJysgU | 2026-06-09T20:42:15+00:00 | 3 | 278669 | True |
| silver/prices/2026-04-24.parquet | 1OjAMbv9YEv37QyU3Khj0TnW_c8pL0lP | 2026-06-09T20:42:15+00:00 | 3 | 281860 | True |
| silver/prices/2026-04-27.parquet | c0lMrA7E8g0jvaP7TP600MzuD_njTuHY | 2026-06-09T20:42:15+00:00 | 3 | 279874 | True |
| silver/prices/2026-04-28.parquet | Tbx52ptIPheS6rKNBMrARmKccpBbukVf | 2026-06-09T20:42:15+00:00 | 3 | 282449 | True |
| silver/prices/2026-04-29.parquet | YXLvMjhF.D9otcpUaG1XX66GxgGXcogj | 2026-06-09T20:42:15+00:00 | 3 | 282316 | True |
| silver/prices/2026-04-30.parquet | 1D08jFPxSuw81TApuiflaJpu0H9zxzWF | 2026-06-09T20:42:15+00:00 | 3 | 282420 | True |
| silver/prices/2026-05-04.parquet | oFkYK5EB2qpexVPxkI62k6EnJGU6h4G. | 2026-06-09T20:42:15+00:00 | 3 | 282444 | True |
| silver/prices/2026-05-05.parquet | IIFfnW_OUH95tN3CBrrft6llJid3Sjgk | 2026-06-09T20:42:15+00:00 | 3 | 282440 | True |
| silver/prices/2026-05-06.parquet | LfA2PCtbhI3dV_HQ7m7P.ETkkjZKWJI1 | 2026-06-09T20:42:15+00:00 | 3 | 282643 | True |
| silver/prices/2026-05-07.parquet | be1xbPwTSUP2wcyyV0QApVAM98ck5NT6 | 2026-06-09T20:42:15+00:00 | 3 | 282642 | True |
| silver/prices/2026-05-08.parquet | SIZGSKhey.dOZ.qhZ4hXTPTW.IvHW03J | 2026-06-09T20:42:15+00:00 | 3 | 286352 | True |
| silver/prices/2026-05-11.parquet | nAhHmfBH6B63S7KEBwELRBAJLQmccimq | 2026-06-09T20:42:15+00:00 | 3 | 285519 | True |
| silver/prices/2026-05-12.parquet | kp7_FU6rA95cy3TNTA8BnDE_HafFHEZw | 2026-06-09T20:42:15+00:00 | 3 | 283296 | True |
| silver/prices/2026-05-13.parquet | KdVXRL7Y60Dt72QV_9ZjxDwoRecBJLq4 | 2026-06-09T20:42:15+00:00 | 3 | 283700 | True |
| silver/prices/2026-05-14.parquet | .pQnItAObcRxj9jUM0NU_ozL_znuX7SP | 2026-06-09T20:42:15+00:00 | 3 | 283657 | True |
| silver/prices/2026-05-15.parquet | mD..bqASta3ohrSMbzcoifq6d4mNJ4.0 | 2026-06-09T20:42:15+00:00 | 3 | 286997 | True |
| silver/prices/2026-05-18.parquet | qQe.cCm5J.T1IhQdwJQcEkszX6RsMaXP | 2026-06-09T20:42:15+00:00 | 3 | 284221 | True |
| silver/prices/2026-05-19.parquet | OcIgOhsAFa8HUCSGLUfuuW_2Q9S_bK.W | 2026-06-09T20:42:15+00:00 | 3 | 284202 | True |
| silver/prices/2026-05-20.parquet | 8GdsjITbs_y0cE4_rRIgOanVzzlSOOYX | 2026-06-09T20:42:15+00:00 | 3 | 284926 | True |
| silver/prices/2026-05-21.parquet | pIjx7aGqJlvyUfrMHhufKKxoo40TC9wR | 2026-06-09T20:42:15+00:00 | 3 | 286136 | True |
| silver/prices/2026-05-22.parquet | zwXI4yS8.ZJ1oSmcfziLQ2a4sM3.uZyf | 2026-06-09T20:42:15+00:00 | 3 | 288993 | True |
| silver/prices/2026-05-25.parquet | D.Fx79yUNPIOuldA9S3dfuVq_SQaDh0. | 2026-06-09T20:42:15+00:00 | 3 | 285955 | True |
| silver/prices/2026-05-26.parquet | yX9Gx8AYTtK61H8uYTzk.DSyVpGHXkH1 | 2026-06-09T20:42:15+00:00 | 3 | 286097 | True |
| silver/prices/2026-05-27.parquet | 5FxAH5L9g4O8xSSERPMZWb.aWux75hvL | 2026-06-09T20:42:15+00:00 | 3 | 286146 | True |
| silver/prices/2026-05-28.parquet | 93CqOKffS4POLtg3xfXcDAspkGsaWFpV | 2026-06-09T20:42:15+00:00 | 3 | 286333 | True |
| silver/prices/2026-05-29.parquet | vNaVF9blcQ_5EkZ.UA_DertoV9HNWjRJ | 2026-06-09T20:42:15+00:00 | 3 | 289529 | True |
| silver/prices/2026-06-01.parquet | PVpSfIr7tjSHRJPRW.MpKXNMAsG1eJcx | 2026-06-09T20:42:16+00:00 | 3 | 286566 | True |
| silver/prices/2026-06-02.parquet | lhV2qus.hrLyOQdGD3osNxRmQqnlWlEc | 2026-06-09T20:42:16+00:00 | 3 | 289576 | True |
| silver/prices/2026-06-03.parquet | cPBbHdli7nnIv3Hrs5_ZlmjCfV5sWxt8 | 2026-06-09T20:42:16+00:00 | 3 | 286683 | True |
| silver/prices/2026-06-04.parquet | 6KSd_Co.aCVO0k0JtTTQbSzhS1wFO6tw | 2026-06-09T20:42:16+00:00 | 3 | 287128 | True |
| silver/prices/2026-06-05.parquet | gphtVrpZ0ZTLVuWuYEPPG01tsyusehuO | 2026-06-09T20:42:16+00:00 | 3 | 290553 | True |
| silver/prices/canonical_prices.parquet | 5JN8rkV4dcE.v64dYVAA6PR5jccvS8Rc | 2026-06-09T20:42:16+00:00 | 1623 | 97633099 | True |

Read errors: 0 []

cot code keys naming the inject or exceptions file (listed, not read): []

## 3. Writers' history

### git log data/cot/scripts/gold/build_canonical_prices_v2.py
```
319a716cb4 2026-06-12T16:04:35-04:00 0.4.0_DS_ClientPlatform fix(cot/DEBTSCAN D2X-DS-03+04): remove 49F-only scoped-inject auto-chain from cot S_00 + add B_03->C_00 AUAGAP guard
d892fe5001 2026-06-11T09:18:42-04:00 0.4.0_DS_ClientPlatform NFRA_DTAFLP TO-1b: retarget cot gold opal-data-bd->opal-data-cot (7 live + Schwab default + provenance)
6b0be4337e 2026-06-10T09:23:08-04:00 0.4.0_DS_ClientPlatform [PRESERVE-SEED][AUTHORIZED] NFRA_DTAFLP TO-1: faithful cot gold S3 seed -> data/cot/scripts/gold/

```
Commits within +-3 days of the store write (2026-06-09T20:42:16Z):
```
319a716cb4 2026-06-12T16:04:35-04:00 fix(cot/DEBTSCAN D2X-DS-03+04): remove 49F-only scoped-inject auto-chain from cot S_00 + add B_03->C_00 AUAGAP guard
d892fe5001 2026-06-11T09:18:42-04:00 NFRA_DTAFLP TO-1b: retarget cot gold opal-data-bd->opal-data-cot (7 live + Schwab default + provenance)
6b0be4337e 2026-06-10T09:23:08-04:00 [PRESERVE-SEED][AUTHORIZED] NFRA_DTAFLP TO-1: faithful cot gold S3 seed -> data/cot/scripts/gold/

```
### git log data/cot/scripts/gold/gold_dispatch.sh
```
d892fe5001 2026-06-11T09:18:42-04:00 0.4.0_DS_ClientPlatform NFRA_DTAFLP TO-1b: retarget cot gold opal-data-bd->opal-data-cot (7 live + Schwab default + provenance)
6b0be4337e 2026-06-10T09:23:08-04:00 0.4.0_DS_ClientPlatform [PRESERVE-SEED][AUTHORIZED] NFRA_DTAFLP TO-1: faithful cot gold S3 seed -> data/cot/scripts/gold/

```
Commits within +-3 days of the store write (2026-06-09T20:42:16Z):
```
d892fe5001 2026-06-11T09:18:42-04:00 NFRA_DTAFLP TO-1b: retarget cot gold opal-data-bd->opal-data-cot (7 live + Schwab default + provenance)
6b0be4337e 2026-06-10T09:23:08-04:00 [PRESERVE-SEED][AUTHORIZED] NFRA_DTAFLP TO-1: faithful cot gold S3 seed -> data/cot/scripts/gold/

```
### git log infra/aws/terraform/cot-pipeline/ssm.tf
```
a69977a205 2026-09-27T14:33:30-04:00 0.6.2_AE_PartnerETL~S fix(IRPT_BCKEND.TO-IB-s158, 0.6.2_AE_PartnerETL~S): session-fetch uploads its log on failure -- EXIT_CODE=$? was dead code under set -e
ce99054e44 2026-07-29T04:11:12-04:00 0.7.0_AE_CloudOps~A cot(4:30p ET move, Andrew-direct ~0445Z via CTO 045223Z): session anchor -> Scheduler cron(30 16) America/New_York + mirror -> cron(30 18) America/New_York (DST-safe; old UTC rules die in the same change, no dual-trigger window) + bounded late-publish retry in opal-cot-bronze-run (sentinel-keyed, 4x15min, idempotent re-invoke, a RETRY never an alarm)
68a9662936 2026-06-29T09:55:11-04:00 0.7.0_AE_CloudOps infra(cot-pipeline): wire DATEMODE-B holdings retry-net into opal-cot-bronze-run SSM doc (placement A, DS co-author 6241d7227 confirmed) -- cot_bronze_ingest.py --backfill-holdings-net runs BEFORE the main pull/sentinel (re-land valued holdings -> silver Cond-2 ETag-reprocess picks up), NON-GATING separable failure domain; COT_DETECTION_SNS_ARN + COT_MARKET_HOLIDAYS env wired (IAM CotDetectionSnsPublish already declared)
daa38655c6 2026-06-26T12:08:20-04:00 0.6.0_AE_PartnerETL feat(ADVI_COTETL.L4-GUARD): PIECE-2 ACTIVATION -- re-point opal-cot-bd-session-fetch SSM doc off MFA-failing cot_bd_session_fetch.py -> canonical gateway-self-fetch wrapper (./run-bd-auto-login.sh). Ends the cot silent-re-freeze: the box self-fetches the OTP via the OPLMCP gateway (zero live-agent). Doc name unchanged -> event-driven session->bronze->silver->gold chain preserved. CVO 6-clause SOUND 155721Z + CTO GO 160147Z + COO GO 160251Z. e2e PROVEN (happy+6a+6b+6c). Ledger 20260626T1607Z.
f784a1e921 2026-06-22T19:29:34-04:00 0.7.0_AE_CloudOps infra(ADVI_COTETL WORK A): chain A_05 assets_dimension after B_00 in opal-cot-gold-run (DS owner-review PASS; A_05==cbbbefb01; optional/data-layer gold/dimensions). + deploy-ledger. [plain-commit: tool ledger files]
c19d40212a 2026-06-22T16:38:49-04:00 0.7.0_AE_CloudOps infra(ADVI_COTETL fast-follow): chain D_01 partner_analytics before D_04 in opal-cot-gold-run (CHAIN-ONLY per DS/COO; D_04 already publishes gold/artifacts->platinum). Fixes header-vs-Distribution vintage skew; D_01==c5bc7ba49 reads account_performance/C_03. + deploy-ledger. [plain-commit: tool ledger files trip safe-commit pathspec; plan 0-destroy]
7240a89338 2026-06-22T13:49:36-04:00 0.7.0_AE_CloudOps infra(ADVI_COTETL.CLEANUP Leg-1): de-chain dead C_00 canonical_performance + C_02 client_performance from opal-cot-gold-run (CTO-confirmed; post snapshot-perf 5c80bf6ca) + deploy-ledger. AE-dechain leg; DS deletes .py AFTER (hard order). [plain-commit: tool-created ledger files trip safe-commit pathspec; plan 0-destroy]
ded252bae1 2026-06-22T10:59:40-04:00 0.7.0_AE_CloudOps infra(ADVI_COTETL.DATEMODE-C): add non-gating daily holdings refresh to opal-cot-silver-run SSM chain (decoupled; sentinel unaffected) + deploy ledger
161f764350 2026-06-11T12:20:28-04:00 0.7.0_AE_CloudOps ADVI_COTETL.CHAIN-FIX: add cot_silver_merge --finalize as LAST step of opal-cot-silver-run (silver sentinel emission)
0c4be78767 2026-06-11T11:36:16-04:00 0.7.0_AE_CloudOps NFRA_DTAFLP: scrub stale 'mirrored from 49F' echo string in cot ssm.tf:272 (CVO AC10 residual)
2976e40a2e 2026-06-10T09:44:41-04:00 0.7.0_AE_CloudOps~B feat(NFRA_DTAFLP): TO-2 sever ssm.tf re-mirror framing + TO-3 wire cot into comp-pipescript deployed
97e40bd147 2026-06-10T08:54:15-04:00 0.7.0_AE_CloudOps~B feat(NFRA_DTAFLP): deploy-gate cross-firm bucket guard + ssm.t
```
Commits within +-3 days of the store write (2026-06-09T20:42:16Z):
```
161f764350 2026-06-11T12:20:28-04:00 ADVI_COTETL.CHAIN-FIX: add cot_silver_merge --finalize as LAST step of opal-cot-silver-run (silver sentinel emission)
0c4be78767 2026-06-11T11:36:16-04:00 NFRA_DTAFLP: scrub stale 'mirrored from 49F' echo string in cot ssm.tf:272 (CVO AC10 residual)
2976e40a2e 2026-06-10T09:44:41-04:00 feat(NFRA_DTAFLP): TO-2 sever ssm.tf re-mirror framing + TO-3 wire cot into comp-pipescript deployed
97e40bd147 2026-06-10T08:54:15-04:00 feat(NFRA_DTAFLP): deploy-gate cross-firm bucket guard + ssm.tf re-mirror footgun doc
6e75df5852 2026-06-09T16:47:52-04:00 fix(ADVI_COTETL): add polars to gold-run pip install (C_00 needs it)
35f8c0aa96 2026-06-09T16:28:24-04:00 fix(ADVI_COTETL): pin gold pandas==2.2.3 (cot-exporter ships pandas 3.0 which breaks 49F gold)
1d547fe7cc 2026-06-09T15:54:43-04:00 fix(ADVI_COTETL): gold-run syncs code from opal-data-cot mirror (honors bucket isolation)
b4b8993a07 2026-06-09T12:04:55-04:00 fix(ADVI_COTETL): set SCHWAB_S3_BUCKET=opal-data-cot in opal-cot-gold-run — forces try/except degradation not empty join (Andrew-direct)
80c34f9a3a 2026-06-09T11:17:58-04:00 feat(ADVI_COTETL): extend opal-cot-silver-run SSM doc to include realized+unrealized tables (all 4 tables: transactions+allocations+realized+unrealized)
3d93ff57da 2026-06-09T11:08:15-04:00 feat(ADVI_COTETL): silver-daily + gold-daily EventBridge rules (DISABLED) + opal-cot-gold-run SSM doc (18-script COT gold chain)
d73de487bc 2026-06-09T10:17:16-04:00 feat(ADVI_COTETL): add opal-cot-silver-run SSM doc (silver merge, manual trigger v1)
e888ccad6c 2026-06-08T17:21:17-04:00 fix(cot-pipeline): opal-cot-bronze-run SSM DRY_RUN via env (no --dry-run flag), clean up stale exports
9e9da8ae9f 2026-06-08T17:19:40-04:00 fix(cot-pipeline): opal-cot-bronze-run SSM CLI args + Table param
0f57df6eb0 2026-06-08T17:17:51-04:00 fix(cot-pipeline): opal-cot-bronze-run SSM python3->python3.11 (boto3) + HOME=/root
9f3dbe7c12 2026-06-08T16:30:13-04:00 fix(cot-pipeline): session-fetch S
```
Builder revision in force at the store write: 

No commit of the cot builder path exists before the store write. Earliest cot-path commit (the faithful S3 seed of the mirror the gold run synced, read as the builder content in force): 6b0be4337e40fc0183ceb2f776352cbcdaf0a017 2026-06-10T09:23:08-04:00 [PRESERVE-SEED][AUTHORIZED] NFRA_DTAFLP TO-1: faithful cot gold S3 seed -> data/cot/scripts/gold/
Shared builder path last commit before the write: 64b6b9d65a258533eca535101ab7688805901b5f 2026-04-27T10:41:04-04:00 log(COMP_LEARNS.session13): CVO ruling reception + revised iter-7 -- q03-only scored, q02/q11 stripped (R-CTO-1 P0)
- cot path, SEED commit (content of the S3 mirror the run synced) 6b0be4337e: non-comment inject lines [(22, '6b. Auto-chain       -> inject_scoped_overrides.py --upload  (enforced in code)'), (481, 'def _run_inject_scoped_overrides():'), (669, '_run_inject_scoped_overrides()')]
- shared builder path, last commit before the write 64b6b9d65a: non-comment inject lines [(22, '6b. Auto-chain       -> inject_scoped_overrides.py --upload  (enforced in code)'), (481, 'def _run_inject_scoped_overrides():'), (669, '_run_inject_scoped_overrides()')]
Run config exports BD_S3_BUCKET=cot bucket: {'data/cot/scripts/gold/gold_dispatch.sh': [], 'infra/aws/terraform/cot-pipeline/ssm.tf': [(233, '"export BD_S3_BUCKET=opal-data-cot",'), (310, 'description   = "COT gold chain — syncs scripts from opal-data-cot/code/gold/ (cot\'s own git-versioned gold tree; NEVER mirrored from opal-data-bd), runs with B'), (331, '"export BD_S3_BUCKET=opal-data-cot",')]}
Dispatch syncs the cot bucket code/silver/ (inject resolvable at run): [(504, 'aws s3 sync "s3://$BD_S3_BUCKET/code/silver/" "/tmp/silver/" --quiet')]
Live cot path candidates at HEAD (non-comment inject/label lines under data/cot): []

Prior carriers (hit written more than 60 s before the store write): 0; copy-source evidence in git/S3 listing for them: none found

## 4. Class

`shared_builder_run` -- by the pre-committed rule.

## 5. Delete list for Andrew (listed only, nothing deleted)

| key | version | LastModified | size | rows |
|---|---|---|---|---|
| silver/prices/2026-04-14.parquet | fGDQqialTgvN2alIUQLhQABTfk5c3Bxu | 2026-06-09T20:42:15+00:00 | 277915 | 3 |
| silver/prices/2026-04-16.parquet | caXhQHwomxRDe9Avx41lKomKbjCUA00b | 2026-06-09T20:42:15+00:00 | 281297 | 3 |
| silver/prices/2026-04-17.parquet | czKjJFbHforLgeJ3tM.JRH.7pEPmSGGk | 2026-06-09T20:42:15+00:00 | 281294 | 3 |
| silver/prices/2026-04-20.parquet | TwJXQ8zV8U1euL1jTwACFuvZEgqnqkgH | 2026-06-09T20:42:15+00:00 | 281443 | 3 |
| silver/prices/2026-04-21.parquet | JrzcHd773qTIxPW3jNoUHIhU2Y3C2DbD | 2026-06-09T20:42:15+00:00 | 280687 | 3 |
| silver/prices/2026-04-22.parquet | B9X2y1p8EsDlUOusorKGhkn3qSOeDoiY | 2026-06-09T20:42:15+00:00 | 278575 | 3 |
| silver/prices/2026-04-23.parquet | mbuwkdfSEll7X0Yx5t6pdJeG9KBJysgU | 2026-06-09T20:42:15+00:00 | 278669 | 3 |
| silver/prices/2026-04-24.parquet | 1OjAMbv9YEv37QyU3Khj0TnW_c8pL0lP | 2026-06-09T20:42:15+00:00 | 281860 | 3 |
| silver/prices/2026-04-27.parquet | c0lMrA7E8g0jvaP7TP600MzuD_njTuHY | 2026-06-09T20:42:15+00:00 | 279874 | 3 |
| silver/prices/2026-04-28.parquet | Tbx52ptIPheS6rKNBMrARmKccpBbukVf | 2026-06-09T20:42:15+00:00 | 282449 | 3 |
| silver/prices/2026-04-29.parquet | YXLvMjhF.D9otcpUaG1XX66GxgGXcogj | 2026-06-09T20:42:15+00:00 | 282316 | 3 |
| silver/prices/2026-04-30.parquet | 1D08jFPxSuw81TApuiflaJpu0H9zxzWF | 2026-06-09T20:42:15+00:00 | 282420 | 3 |
| silver/prices/2026-05-04.parquet | oFkYK5EB2qpexVPxkI62k6EnJGU6h4G. | 2026-06-09T20:42:15+00:00 | 282444 | 3 |
| silver/prices/2026-05-05.parquet | IIFfnW_OUH95tN3CBrrft6llJid3Sjgk | 2026-06-09T20:42:15+00:00 | 282440 | 3 |
| silver/prices/2026-05-06.parquet | LfA2PCtbhI3dV_HQ7m7P.ETkkjZKWJI1 | 2026-06-09T20:42:15+00:00 | 282643 | 3 |
| silver/prices/2026-05-07.parquet | be1xbPwTSUP2wcyyV0QApVAM98ck5NT6 | 2026-06-09T20:42:15+00:00 | 282642 | 3 |
| silver/prices/2026-05-08.parquet | SIZGSKhey.dOZ.qhZ4hXTPTW.IvHW03J | 2026-06-09T20:42:15+00:00 | 286352 | 3 |
| silver/prices/2026-05-11.parquet | nAhHmfBH6B63S7KEBwELRBAJLQmccimq | 2026-06-09T20:42:15+00:00 | 285519 | 3 |
| silver/prices/2026-05-12.parquet | kp7_FU6rA95cy3TNTA8BnDE_HafFHEZw | 2026-06-09T20:42:15+00:00 | 283296 | 3 |
| silver/prices/2026-05-13.parquet | KdVXRL7Y60Dt72QV_9ZjxDwoRecBJLq4 | 2026-06-09T20:42:15+00:00 | 283700 | 3 |
| silver/prices/2026-05-14.parquet | .pQnItAObcRxj9jUM0NU_ozL_znuX7SP | 2026-06-09T20:42:15+00:00 | 283657 | 3 |
| silver/prices/2026-05-15.parquet | mD..bqASta3ohrSMbzcoifq6d4mNJ4.0 | 2026-06-09T20:42:15+00:00 | 286997 | 3 |
| silver/prices/2026-05-18.parquet | qQe.cCm5J.T1IhQdwJQcEkszX6RsMaXP | 2026-06-09T20:42:15+00:00 | 284221 | 3 |
| silver/prices/2026-05-19.parquet | OcIgOhsAFa8HUCSGLUfuuW_2Q9S_bK.W | 2026-06-09T20:42:15+00:00 | 284202 | 3 |
| silver/prices/2026-05-20.parquet | 8GdsjITbs_y0cE4_rRIgOanVzzlSOOYX | 2026-06-09T20:42:15+00:00 | 284926 | 3 |
| silver/prices/2026-05-21.parquet | pIjx7aGqJlvyUfrMHhufKKxoo40TC9wR | 2026-06-09T20:42:15+00:00 | 286136 | 3 |
| silver/prices/2026-05-22.parquet | zwXI4yS8.ZJ1oSmcfziLQ2a4sM3.uZyf | 2026-06-09T20:42:15+00:00 | 288993 | 3 |
| silver/prices/2026-05-25.parquet | D.Fx79yUNPIOuldA9S3dfuVq_SQaDh0. | 2026-06-09T20:42:15+00:00 | 285955 | 3 |
| silver/prices/2026-05-26.parquet | yX9Gx8AYTtK61H8uYTzk.DSyVpGHXkH1 | 2026-06-09T20:42:15+00:00 | 286097 | 3 |
| silver/prices/2026-05-27.parquet | 5FxAH5L9g4O8xSSERPMZWb.aWux75hvL | 2026-06-09T20:42:15+00:00 | 286146 | 3 |
| silver/prices/2026-05-28.parquet | 93CqOKffS4POLtg3xfXcDAspkGsaWFpV | 2026-06-09T20:42:15+00:00 | 286333 | 3 |
| silver/prices/2026-05-29.parquet | vNaVF9blcQ_5EkZ.UA_DertoV9HNWjRJ | 2026-06-09T20:42:15+00:00 | 289529 | 3 |
| silver/prices/2026-06-01.parquet | PVpSfIr7tjSHRJPRW.MpKXNMAsG1eJcx | 2026-06-09T20:42:16+00:00 | 286566 | 3 |
| silver/prices/2026-06-02.parquet | lhV2qus.hrLyOQdGD3osNxRmQqnlWlEc | 2026-06-09T20:42:16+00:00 | 289576 | 3 |
| silver/prices/2026-06-03.parquet | cPBbHdli7nnIv3Hrs5_ZlmjCfV5sWxt8 | 2026-06-09T20:42:16+00:00 | 286683 | 3 |
| silver/prices/2026-06-04.parquet | 6KSd_Co.aCVO0k0JtTTQbSzhS1wFO6tw | 2026-06-09T20:42:16+00:00 | 287128 | 3 |
| silver/prices/2026-06-05.parquet | gphtVrpZ0ZTLVuWuYEPPG01tsyusehuO | 2026-06-09T20:42:16+00:00 | 290553 | 3 |
| silver/prices/canonical_prices.parquet | 5JN8rkV4dcE.v64dYVAA6PR5jccvS8Rc | 2026-06-09T20:42:16+00:00 | 97633099 | 1623 |

Note: the store key is a full price file; the rows are 38 version(s); removal of the label rows means a rebuild, not a key delete, for the live store (Andrew's call).

BD-TXN-PROVENANCE keys_scanned=7790 keys_with_rows=38 earliest=silver/prices/2026-04-14.parquet@2026-06-09T20:42:15Z class=shared_builder_run
