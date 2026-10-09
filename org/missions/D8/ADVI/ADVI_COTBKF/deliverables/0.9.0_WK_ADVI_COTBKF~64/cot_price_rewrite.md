# cot_price_rewrite -- local build of the 38 rewritten price files (no S3 write)

Bucket read: opal-data-cot (38 named versions only). Label removed: bd_txn_price. Local files: .scratch/advi_cotbkf/cot_price_rewrite/<key> (uncommitted).

## 1. Bond re-pricing (Yahoo rule committed before the run)

Yahoo calls: 6 (cap 9). Equity deny list: ['BNP.PA', 'BNPQF', 'BNPQY', 'NEM', 'WFC']. Window 2024-01-24 .. 2026-06-09.

| CUSIP | symbol used | closes returned | search hits | note |
|---|---|---|---|---|
| 05613L3H2 | None | 0 | [] | history 05613L3H2 empty;  |
| 95000U2D4 | None | 0 | [] | history 95000U2D4 empty;  |
| 651639AX4 | None | 0 | [] | history 651639AX4 empty;  |

bonds_priced=0/3. A bond with no symbol is unpriced (its rows removed, no replacement).

## 2. Per-key diff

| key | version_before | rows_before | rows_after | removed | repriced | other_rows_identical | sha256_after |
|---|---|---|---|---|---|---|---|
| silver/prices/2026-04-14.parquet | fGDQqialTgvN2alIUQLhQABTfk5c3Bxu | 10105 | 10102 | 3 | 0 | True | 59651c7e4fc1fbf3d7222113838d51d5ee03fe71276f959861858ca367dd58f7 |
| silver/prices/2026-04-16.parquet | caXhQHwomxRDe9Avx41lKomKbjCUA00b | 10124 | 10121 | 3 | 0 | True | 3696ffee3e7c2172cec2bb8479ee481501ebfb2a696a7f618fe78937793c4ea4 |
| silver/prices/2026-04-17.parquet | czKjJFbHforLgeJ3tM.JRH.7pEPmSGGk | 10125 | 10122 | 3 | 0 | True | 2ccae09a8e96e39a9d65b74e812c9d87111397074fcf7eca54d09355725b52e7 |
| silver/prices/2026-04-20.parquet | TwJXQ8zV8U1euL1jTwACFuvZEgqnqkgH | 10126 | 10123 | 3 | 0 | True | 0fcd104f9c70519f111b58bda853544166f013c3d1b6cb119b796c230640776d |
| silver/prices/2026-04-21.parquet | JrzcHd773qTIxPW3jNoUHIhU2Y3C2DbD | 10126 | 10123 | 3 | 0 | True | 2625f32554a10e7560097dcb3855dc9b908e326cf28a54c54737840ad901b009 |
| silver/prices/2026-04-22.parquet | B9X2y1p8EsDlUOusorKGhkn3qSOeDoiY | 10133 | 10130 | 3 | 0 | True | 287ffa41639b61c9fcb294392b12cb67b5b9acf13123f74968fc3c429b33a2cb |
| silver/prices/2026-04-23.parquet | mbuwkdfSEll7X0Yx5t6pdJeG9KBJysgU | 10140 | 10137 | 3 | 0 | True | 0fe7879fda275a7af7ef18645c69d62528f24d90daadc0aae15e2a855d94d624 |
| silver/prices/2026-04-24.parquet | 1OjAMbv9YEv37QyU3Khj0TnW_c8pL0lP | 10147 | 10144 | 3 | 0 | True | 5308673bad47e01dc6fcb7587ee3f3f42e1bf49c6a8b95cee8d9e1d46d442614 |
| silver/prices/2026-04-27.parquet | c0lMrA7E8g0jvaP7TP600MzuD_njTuHY | 10185 | 10182 | 3 | 0 | True | 1f28ae1612c8f2318be85155b30c5cda625cdf231909083d51d565fb2ce7fe29 |
| silver/prices/2026-04-28.parquet | Tbx52ptIPheS6rKNBMrARmKccpBbukVf | 10259 | 10256 | 3 | 0 | True | e6668839bc35b7b2c4ec992d435dbff2197578b6768e5f0b74479afb8b0f204a |
| silver/prices/2026-04-29.parquet | YXLvMjhF.D9otcpUaG1XX66GxgGXcogj | 10259 | 10256 | 3 | 0 | True | 7ba2c50a963e37ae1ce39211dc533e877776cd185b3f746fbeca52ed14655a74 |
| silver/prices/2026-04-30.parquet | 1D08jFPxSuw81TApuiflaJpu0H9zxzWF | 10265 | 10262 | 3 | 0 | True | 4de6006c3123e5e575f26c5b9eedbca4048b7759afa2d73f7e184db22a3da81e |
| silver/prices/2026-05-04.parquet | oFkYK5EB2qpexVPxkI62k6EnJGU6h4G. | 10268 | 10265 | 3 | 0 | True | 25cc51cdc118dfdc0c807a4bbcf448abff8652a706e47e4dcd05e83f82e8ffb8 |
| silver/prices/2026-05-05.parquet | IIFfnW_OUH95tN3CBrrft6llJid3Sjgk | 10275 | 10272 | 3 | 0 | True | 7d4f10ef40c474f15cddb8e2f6c3623594ab85041393cc17f46011448f48a44f |
| silver/prices/2026-05-06.parquet | LfA2PCtbhI3dV_HQ7m7P.ETkkjZKWJI1 | 10278 | 10275 | 3 | 0 | True | bd9bc76a5fa7b145c6e5afc54a8cf8571f99da15f2836687da385966a8fcf2a7 |
| silver/prices/2026-05-07.parquet | be1xbPwTSUP2wcyyV0QApVAM98ck5NT6 | 10283 | 10280 | 3 | 0 | True | f09b229f250698a3a95114aed053eefe3b0464dfd986eaccf215ab60f6c9221d |
| silver/prices/2026-05-08.parquet | SIZGSKhey.dOZ.qhZ4hXTPTW.IvHW03J | 10298 | 10295 | 3 | 0 | True | a5feb27d086814b69e460f50c7e738be98d3bb87afc9433e62aa53e48cae4048 |
| silver/prices/2026-05-11.parquet | nAhHmfBH6B63S7KEBwELRBAJLQmccimq | 10296 | 10293 | 3 | 0 | True | 11bf5d57c18c63230c0334c5c18658f63261c10a9ee535eb376f776236a5902a |
| silver/prices/2026-05-12.parquet | kp7_FU6rA95cy3TNTA8BnDE_HafFHEZw | 10298 | 10295 | 3 | 0 | True | 8258b43832b7f39eb82660d964c62a0703786d1fb0e26cc634cf7d5729616c2a |
| silver/prices/2026-05-13.parquet | KdVXRL7Y60Dt72QV_9ZjxDwoRecBJLq4 | 10308 | 10305 | 3 | 0 | True | 820429192342ebae6ee7b585d4babff82979861c84a5c1886b80a0b086bb2d5a |
| silver/prices/2026-05-14.parquet | .pQnItAObcRxj9jUM0NU_ozL_znuX7SP | 10315 | 10312 | 3 | 0 | True | 5b0508db1f8f63fcab5824af98d6b75cc0d9c0b9a0d163612e4298f7269f0078 |
| silver/prices/2026-05-15.parquet | mD..bqASta3ohrSMbzcoifq6d4mNJ4.0 | 10320 | 10317 | 3 | 0 | True | 1d1fb1f276b50768406da763d5e75224ac2b6afbd8cc00ee1b15ee9563f667d8 |
| silver/prices/2026-05-18.parquet | qQe.cCm5J.T1IhQdwJQcEkszX6RsMaXP | 10323 | 10320 | 3 | 0 | True | 09632d0e50a6696c0f0b1e0f06c7ca580119bd10f207096f50d0626f4ae0e02a |
| silver/prices/2026-05-19.parquet | OcIgOhsAFa8HUCSGLUfuuW_2Q9S_bK.W | 10329 | 10326 | 3 | 0 | True | 3e3c9b66117628275f68095afe49ce16454c29c5573b98d8b69aa56575bae424 |
| silver/prices/2026-05-20.parquet | 8GdsjITbs_y0cE4_rRIgOanVzzlSOOYX | 10361 | 10358 | 3 | 0 | True | efd827d5700e917895da5de8f155fc6a540259e4493d24a78d1558954552968f |
| silver/prices/2026-05-21.parquet | pIjx7aGqJlvyUfrMHhufKKxoo40TC9wR | 10393 | 10390 | 3 | 0 | True | c871006c9e1402ffd53aa2db6d4c509f4ef8d398c742e7ef3710238805794107 |
| silver/prices/2026-05-22.parquet | zwXI4yS8.ZJ1oSmcfziLQ2a4sM3.uZyf | 10394 | 10391 | 3 | 0 | True | a3d0997b26fd94522b223e4775ee8e81a042c64c0b92d7bfc48d2e235d9a18bb |
| silver/prices/2026-05-25.parquet | D.Fx79yUNPIOuldA9S3dfuVq_SQaDh0. | 10393 | 10390 | 3 | 0 | True | 9ccc7e83bc909637fba94a56c6cb2d64a24ff4be7ca3482c42f4c06e1909ed5e |
| silver/prices/2026-05-26.parquet | yX9Gx8AYTtK61H8uYTzk.DSyVpGHXkH1 | 10397 | 10394 | 3 | 0 | True | bc1b90ea9da15059febb48bb88b659108f02240b0b2d9a913d300f5813dfa182 |
| silver/prices/2026-05-27.parquet | 5FxAH5L9g4O8xSSERPMZWb.aWux75hvL | 10398 | 10395 | 3 | 0 | True | 373b5dcf2f10ffa5332b650d2a0065cddfbd7a641cf96c3dc46dd02d9cbe4a41 |
| silver/prices/2026-05-28.parquet | 93CqOKffS4POLtg3xfXcDAspkGsaWFpV | 10405 | 10402 | 3 | 0 | True | d645ac0cd046e3f8525940f89a2fda8f7d51855e987c40e0095f852e4004e706 |
| silver/prices/2026-05-29.parquet | vNaVF9blcQ_5EkZ.UA_DertoV9HNWjRJ | 10416 | 10413 | 3 | 0 | True | 1c839003e1d6860f0fa3c0e54d9927e9cbbcf621522655860bca5f2984fd552d |
| silver/prices/2026-06-01.parquet | PVpSfIr7tjSHRJPRW.MpKXNMAsG1eJcx | 10417 | 10414 | 3 | 0 | True | ec65fe8820f74f5a99112ccf230564e912aca549802edc1a7b4de8578ce74007 |
| silver/prices/2026-06-02.parquet | lhV2qus.hrLyOQdGD3osNxRmQqnlWlEc | 10423 | 10420 | 3 | 0 | True | c6f973ff51c3fc9b5ab6f62153f83dceb0cbe1a0977be10c084a70177d35ee71 |
| silver/prices/2026-06-03.parquet | cPBbHdli7nnIv3Hrs5_ZlmjCfV5sWxt8 | 10429 | 10426 | 3 | 0 | True | 8596205f3516ae0da9b7106b702c1e3679c155e93a262b542147ca788142f0ef |
| silver/prices/2026-06-04.parquet | 6KSd_Co.aCVO0k0JtTTQbSzhS1wFO6tw | 10443 | 10440 | 3 | 0 | True | c92c0279cb0e7394a020c44d47e2430b42bc6667ae1b8dbcd861b17bb3a660bf |
| silver/prices/2026-06-05.parquet | gphtVrpZ0ZTLVuWuYEPPG01tsyusehuO | 10464 | 10461 | 3 | 0 | True | 005775aed4ece252fe3b5f864f1dd8f3f79c8070f8276ecd1f936bc652285267 |
| silver/prices/canonical_prices.parquet | 5JN8rkV4dcE.v64dYVAA6PR5jccvS8Rc | 11291021 | 11289398 | 1623 | 0 | True | 51a1f1f7e19a0ce3d8332484dd53aec431f061d51b1279c9dc020990a17087fa |

Totals: removed=1734 repriced=0; label rows found = 1734.

## 3. Writer census (repo, by file:line) -- writers of the cot price prefix

Scanned 780 .py/.sh/.tf files under ['data/cot', 'data/black_diamond/scripts', 'data/inf/scripts', 'infra/aws/lambda/cot-pipeline', 'infra/aws/terraform/cot-pipeline', 'infra/aws/ec2']. A writer = a file with an S3 write call (upload_file, put_object, upload_fileobj, copy_object, aws s3 cp/sync/mv) whose call text names the price prefix or a name bound to it (name-based, per file: may over-include).

| file | key lines | write lines | bucket lines | price names | in own tree | named in own tf | run by live gold doc |
|---|---|---|---|---|---|---|---|
| data/cot/scripts/gold/build_canonical_prices_v2.py | [(21, '6. Write             -> silver/prices/canonical_prices.parquet'), (30, 'Output: silver/prices/canonical_prices.parquet'), (617, "output_key = 'silver/prices/canonical_prices.parquet'")] | [(624, 's3.upload_file(str(local_path), S3_BUCKET, output_key)')] | [(56, "S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-cot')")] | ['output_key'] | True | False | False |
| data/black_diamond/scripts/gold/build_canonical_prices_v2.py | [(21, '6. Write             -> silver/prices/canonical_prices.parquet'), (32, 'Output: silver/prices/canonical_prices.parquet'), (653, "output_key = 'silver/prices/canonical_prices.parquet'")] | [(660, 's3.upload_file(str(local_path), S3_BUCKET, output_key)')] | [(57, "S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')")] | ['output_key'] | False | False | False |
| data/black_diamond/scripts/silver/backfill_yahoo_prices_safe.py | [(46, "TELEMETRY_KEY = 'silver/prices/backfill_telemetry.json'")] | [(235, 's3.put_object(Bucket=S3_BUCKET, Key=TELEMETRY_KEY, Body=body)')] | [(42, "S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')")] | ['TELEMETRY_KEY'] | False | False | False |
| data/black_diamond/scripts/silver/bd_price_update.py | [(10, 'a. Load silver/prices/canonical_prices.parquet  (current full table)'), (317, "df = _load_parquet_bytes('silver/prices/canonical_prices.parquet')"), (609, "s3.put_object(Bucket=S3_BUCKET, Key='silver/prices/canonical_prices.parquet',"), (618, '"""Write today\'s price rows to silver/prices/YYYY-MM-DD.parquet.')] | [(609, "s3.put_object(Bucket=S3_BUCKET, Key='silver/prices/canonical_prices.parquet',"), (666, 's3.put_object(Bucket=S3_BUCKET, Key=key, Body=buf.getvalue())')] | [(47, "S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')")] | ['key'] | False | False | False |
| data/black_diamond/scripts/silver/inject_scoped_overrides.py | [(55, 'CANONICAL_KEY = "silver/prices/canonical_prices.parquet"'), (268, 'f"Set to e.g. \'silver/prices/canonical_prices_v2_dryrun.parquet\' "')] | [(253, 's3.put_object(Bucket=S3_BUCKET, Key=output_key, Body=buf.read())')] | [(54, "S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')")] | ['CANONICAL_KEY', 'default', 'output_key'] | False | False | False |
| data/inf/scripts/gold/INF_build_canonical_prices.py | [(21, 'silver/prices/canonical_prices.parquet'), (50, "OUTPUT_KEY = 'silver/prices/canonical_prices.parquet'")] | [(480, 's3.upload_file(str(local_path), S3_BUCKET, OUTPUT_KEY,')] | [(47, "S3_BUCKET = 'opal-data-inf'")] | ['OUTPUT_KEY'] | False | False | False |
| data/inf/scripts/silver/backfill_yahoo_prices.py | [(50, "TELEMETRY_KEY = 'silver/prices/backfill_telemetry.json'")] | [(247, 's3.put_object(Bucket=S3_BUCKET, Key=TELEMETRY_KEY, Body=body,')] | [(46, "S3_BUCKET = 'opal-data-inf'")] | ['TELEMETRY_KEY'] | False | False | False |

Chain (static): {"catalog_S_00": [78, "S_00|build_canonical_prices_v2.py|"], "prep_pregate": [1071, "_should_run_silver_prep=1"], "ssm_gold_doc": [304, "name            = \"opal-cot-gold-run\""], "lambda_gold_mode": [328, "if mode == 'gold-run':"], "lambda_gold_doc": [46, "GOLD_RUN_SSM_DOCUMENT = 'opal-cot-gold-run'"]}

Terraform: 17 .tf files; schedule_expression rules: [('cot-detection-layer.tf', 154, 'rate(15 minutes)'), ('cot-etf-ownership-daily.tf', 225, 'cron(30 10 * * ? *)'), ('satellites-characteristics-producer.tf', 358, 'cron(30 12 * * ? *)'), ('satellites-registry-producer.tf', 287, 'cron(0 7 * * ? *)'), ('schedule-et.tf', 90, 'cron(30 7 * * ? *)')]

### Live reads (one describe/get per named resource)

- {"kind": "events.describe_rule", "name": "cot-session-complete", "state": "ENABLED", "schedule": null, "has_event_pattern": true}
- {"kind": "events.describe_rule", "name": "cot-bronze-complete", "state": "ENABLED", "schedule": null, "has_event_pattern": true}
- {"kind": "events.describe_rule", "name": "cot-silver-complete", "state": "ENABLED", "schedule": null, "has_event_pattern": true}
- {"kind": "events.describe_rule", "name": "bd-cot-keepalive-sched", "state": "ENABLED", "schedule": "rate(15 minutes)", "has_event_pattern": false}
- {"kind": "events.describe_rule", "name": "cot-etf-ownership-daily-schedule", "state": "ENABLED", "schedule": "cron(30 10 * * ? *)", "has_event_pattern": false}
- {"kind": "events.describe_rule", "name": "cot-satellites-registry-producer-daily", "state": "ENABLED", "schedule": "cron(0 7 * * ? *)", "has_event_pattern": false}
- {"kind": "events.describe_rule", "name": "cot-satellites-characteristics-producer-daily", "state": "ENABLED", "schedule": "cron(30 12 * * ? *)", "has_event_pattern": false}
- {"kind": "scheduler.get_schedule", "name": "cot-bd-session-daily-et", "state": "ENABLED", "schedule": "cron(30 7 * * ? *)", "tz": "America/New_York", "target": "{\"mode\":\"session-refresh\"}"}
- {"kind": "ssm.get_document", "name": "opal-cot-gold-run", "state": "Active", "version": "10", "chars": 4108, "mentions_build_canonical_prices": false, "mentions_gold_dispatch": false, "mentions_inject": false, "mentions_S_00": false}

Blind: the code mirror the gold-run document syncs (code/gold/ in the cot bucket) is not in the repo and was not read; only the scripts the live document names are known to run. The silver-prefix writers outside the cot tree default to another firm's bucket and are env-overridable; nothing the live document runs calls them.

writers=7; scheduled=0 (writers whose script the live gold-run document runs, reached from the ENABLED live schedule through the ENABLED chain rules).

COT-PRICE-REWRITE keys=38 rows_removed=1734 rows_repriced=0 other_rows_identical=True bonds_priced=0/3 writers=7 scheduled=0
