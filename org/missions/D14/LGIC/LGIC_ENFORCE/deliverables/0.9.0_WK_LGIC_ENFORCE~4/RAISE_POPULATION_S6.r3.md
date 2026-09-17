# RAISE_POPULATION_S6.r3 -- the full distinct RAISE list this round's census hits past the timebox

Measured 2026-09-17 by `0.9.0_WK_LGIC_ENFORCE~4`, this worktree, registry@26623a452ff8583d (after
this cell's own `inf-otp-relay-api` mint), via a direct-library sweep (`census_live`+`census_repo`
items, `grade()` called on every item without stopping at the first RaiseDefect -- the SAME
function `census_judge()` calls, run without its stop-on-first-RAISE behavior so the full
population is visible in one pass instead of 350+ sequential CLI re-runs).

**462 RAISE occurrences; 351 distinct (plane, type, name) triples; 248 distinct names.**

## By first-token (the RAISE's own quoted token)

| token | occurrences |
|---|---|
| `news` | 114 |
| `json` | 69 |
| `trade` | 50 |
| `astn` | 35 |
| `jwt` | 22 |
| `security` | 18 |
| `benchmarks` | 10 |
| `cache` | 9 |
| `consolidated` | 9 |
| `investor-reporting` | 9 |
| `portal` | 8 |
| `config` | 6 |
| `feeds` | 6 |
| `_quarantine` | 6 |
| `sentiment` | 5 |
| `%s` | 5 |
| `exports` | 4 |
| `timeseries` | 4 |
| `uploads` | 4 |
| `otp` | 4 |
| `vpc` | 3 |
| `pm` | 3 |
| `data-refresh` | 3 |
| `infrastructure` | 3 |
| `security-reports` | 3 |
| `trending_reports` | 3 |
| `_ops` | 3 |
| `json-tiered` | 3 |
| `vendedlogs/pipes` | 2 |
| `portfolio` | 2 |
| `ec2` | 2 |
| `session-trigger-mode.json` | 2 |
| `agendas` | 2 |
| `warehouse` | 2 |
| `forwardfill_v2` | 2 |
| `semantic_clusters` | 2 |
| `platform` | 2 |
| `meta` | 2 |
| `opal-cloudtrail-logs-313476888478` | 1 |
| `opal-cur-313476888478` | 1 |
| `opal-security-evidence` | 1 |
| `opal-served-key-write-trail-logs` | 1 |
| `opalinvest-portal` | 1 |
| `imo` | 1 |
| `research` | 1 |
| `dowjones` | 1 |
| `f49` | 1 |
| `opal` | 1 |
| `daily-reports` | 1 |
| `daily` | 1 |
| `backfill_v2` | 1 |
| `corrections` | 1 |
| `bronze-trigger-mode.json` | 1 |
| `contract_integrity` | 1 |
| `quarantine` | 1 |
| `allowlists` | 1 |
| `views` | 1 |
| `raw` | 1 |
| `macro` | 1 |

## Every distinct (plane, type, name) RAISE, with its message

| plane | type | name | message |
|---|---|---|---|
| live | API_GW | `sentiment-query-api` | R1.f: 'sentiment' is in no vocabulary; no registry row resolves it |
| live | API_GW | `trade-submission-api` | R1.c: 'trade' is an unresolved token (V2) |
| live | CW_ALARM | `astn-wsjft-orchestrator-errors` | R1.c: 'astn' is an unresolved token (V2) |
| live | DYNAMODB_TABLE | `opal-news-articles` | R2: 'news' after opal is an unresolved token (V2) |
| live | DYNAMODB_TABLE | `opal-news-trending-daily` | R2: 'news' after opal is an unresolved token (V2) |
| live | DYNAMODB_TABLE | `opal-trade-submissions` | R2: 'trade' after opal is an unresolved token (V2) |
| live | DYNAMODB_TABLE | `semantic-news-trending-daily` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| live | DYNAMODB_TABLE | `trade-security-identifiers` | R1.c: 'trade' is an unresolved token (V2) |
| live | DYNAMODB_TABLE | `trade-users` | R1.c: 'trade' is an unresolved token (V2) |
| live | EC2_INSTANCE | `astn-wsjft-scraper` | R1.c: 'astn' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-100am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-100pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-1100am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-1100pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-300am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-345pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-400pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-500am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-500pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-600pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-700am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-745pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-845am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-api-900pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-12pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-1am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-3pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-4am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-6pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-9am` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-rss-9pm` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `news-trending-analysis-daily` | R1.c: 'news' is an unresolved token (V2) |
| live | EVENT_RULE | `security-sweep-comprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| live | EVENT_RULE | `trade-parquet-nightly-export` | R1.c: 'trade' is an unresolved token (V2) |
| live | IAM_POLICY | `NewsIngestionPolicy` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_POLICY | `NewsSemanticClusteringAccess` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_POLICY | `SecuritySweepComprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| live | IAM_POLICY | `VPCFlowLogsPolicy` | R1.f: 'vpc' is in no vocabulary; no registry row resolves it |
| live | IAM_POLICY | `astn-wsjft-orchestrator` | R1.c: 'astn' is an unresolved token (V2) |
| live | IAM_POLICY | `astn-wsjft-scheduler-invoke` | R1.c: 'astn' is an unresolved token (V2) |
| live | IAM_POLICY | `astn-wsjft-scraper` | R1.c: 'astn' is an unresolved token (V2) |
| live | IAM_POLICY | `news-dashboard-policy` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_POLICY | `news-sentiment-permissions` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_POLICY | `opal-cloudtrail-logs-313476888478#policy` | R8: the resource 'opal-cloudtrail-logs-313476888478'#policy names cannot be placed from its name |
| live | IAM_POLICY | `opal-cur-313476888478#policy` | R8: the resource 'opal-cur-313476888478'#policy names cannot be placed from its name |
| live | IAM_POLICY | `opal-data-security#policy` | B2: 'security' after opal-data- is no scope key |
| live | IAM_POLICY | `opal-data-security-access-logs#policy` | B2: 'security' after opal-data- is no scope key |
| live | IAM_POLICY | `opal-news-secrets-read` | R2: 'news' after opal is an unresolved token (V2) |
| live | IAM_POLICY | `opal-security-evidence#policy` | R8: the resource 'opal-security-evidence'#policy names cannot be placed from its name |
| live | IAM_POLICY | `opal-served-key-write-trail-logs#policy` | R8: the resource 'opal-served-key-write-trail-logs'#policy names cannot be placed from its name |
| live | IAM_POLICY | `opalinvest-portal#policy` | R8: the resource 'opalinvest-portal'#policy names cannot be placed from its name |
| live | IAM_POLICY | `portal-origin-verify-secret` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| live | IAM_POLICY | `portal-time-machine-invoke-downstream` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| live | IAM_POLICY | `semantic-news-permissions` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| live | IAM_POLICY | `trade-submission-policy` | R1.c: 'trade' is an unresolved token (V2) |
| live | IAM_ROLE | `astn-wsjft-orchestrator-role` | R1.c: 'astn' is an unresolved token (V2) |
| live | IAM_ROLE | `astn-wsjft-scheduler-role` | R1.c: 'astn' is an unresolved token (V2) |
| live | IAM_ROLE | `astn-wsjft-scraper-role` | R1.c: 'astn' is an unresolved token (V2) |
| live | IAM_ROLE | `news-dashboard-processor-role` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_ROLE | `news-ingestion-lambda-role` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_ROLE | `news-sentiment-lambda-role` | R1.c: 'news' is an unresolved token (V2) |
| live | IAM_ROLE | `opal-news-lambda-role` | R2: 'news' after opal is an unresolved token (V2) |
| live | IAM_ROLE | `portal-auth-lambda-role` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| live | IAM_ROLE | `security-sweep-dedicated-role` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| live | IAM_ROLE | `semantic-news-lambda-role` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| live | IAM_ROLE | `sentiment_query_api-role` | R1.f: 'sentiment' is in no vocabulary; no registry row resolves it |
| live | IAM_ROLE | `trade-submission-lambda-role` | R1.c: 'trade' is an unresolved token (V2) |
| live | IAM_ROLE | `vpc-flow-logs-role` | R1.f: 'vpc' is in no vocabulary; no registry row resolves it |
| live | INSTANCE_PROFILE | `astn-wsjft-scraper-profile` | R1.c: 'astn' is an unresolved token (V2) |
| live | LAMBDA | `astn-wsjft-orchestrator` | R1.c: 'astn' is an unresolved token (V2) |
| live | LAMBDA | `cache-control-injector` | R1.f: 'cache' is in no vocabulary; no registry row resolves it |
| live | LAMBDA | `news-ingestion-scheduler` | R1.c: 'news' is an unresolved token (V2) |
| live | LAMBDA | `news-semantic-clustering` | R1.c: 'news' is an unresolved token (V2) |
| live | LAMBDA | `news-trending-analysis` | R1.c: 'news' is an unresolved token (V2) |
| live | LAMBDA | `opal-news-ai-sentiment` | R2: 'news' after opal is an unresolved token (V2) |
| live | LAMBDA | `opal-news-layer3-curation` | R2: 'news' after opal is an unresolved token (V2) |
| live | LAMBDA | `portal-time-machine` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| live | LAMBDA | `security-sweep-comprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| live | LAMBDA | `semantic-news-layer3-curation` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| live | LAMBDA | `sentiment_query_api` | R1.f: 'sentiment' is in no vocabulary; no registry row resolves it |
| live | LAMBDA | `trade-auth-handler` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA | `trade-authorizer` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA | `trade-dashboard-api` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA | `trade-identifier-cache` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA | `trade-parquet-batch-export` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA | `trade-submission-handler` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA | `trade-workflow-handler` | R1.c: 'trade' is an unresolved token (V2) |
| live | LAMBDA_LAYER | `news-trending-deps` | R1.c: 'news' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/astn-wsjft-orchestrator` | R1.c: 'astn' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/cache-control-injector` | R1.f: 'cache' is in no vocabulary; no registry row resolves it |
| live | LOG_GROUP | `/aws/lambda/news-ingestion-scheduler` | R1.c: 'news' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/news-semantic-clustering` | R1.c: 'news' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/news-trending-analysis` | R1.c: 'news' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/opal-news-ai-sentiment` | R2: 'news' after opal is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/opal-news-layer3-curation` | R2: 'news' after opal is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/portal-time-machine` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| live | LOG_GROUP | `/aws/lambda/security-sweep-comprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| live | LOG_GROUP | `/aws/lambda/semantic-news-layer3-curation` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| live | LOG_GROUP | `/aws/lambda/sentiment_query_api` | R1.f: 'sentiment' is in no vocabulary; no registry row resolves it |
| live | LOG_GROUP | `/aws/lambda/trade-auth-handler` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/trade-authorizer` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/trade-dashboard-api` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/trade-identifier-cache` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/trade-parquet-batch-export` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/trade-submission-handler` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/trade-workflow-handler` | R1.c: 'trade' is an unresolved token (V2) |
| live | LOG_GROUP | `/aws/lambda/us-east-1.cache-control-injector` | R1.f: 'cache' is in no vocabulary; no registry row resolves it |
| live | LOG_GROUP | `/aws/vendedlogs/pipes/opal-globgrph-projection-worker` | L2: service 'vendedlogs/pipes' gives no resource type |
| live | LOG_GROUP | `/aws/vpc/flowlogs` | L2: service 'vpc' gives no resource type |
| live | S3_BUCKET | `opal-data-astn` | B2: 'astn' after opal-data- is no scope key (V2) |
| live | S3_BUCKET | `opal-data-imo` | B2: 'imo' after opal-data- is no scope key |
| live | S3_BUCKET | `opal-data-news-av` | B2: 'news' after opal-data- is no scope key (V2) |
| live | S3_BUCKET | `opal-data-news-v2` | B2: 'news' after opal-data- is no scope key (V2) |
| live | S3_BUCKET | `opal-data-pm` | B2: 'pm' after opal-data- is no scope key |
| live | S3_BUCKET | `opal-data-portfolio` | B2: 'portfolio' after opal-data- is no scope key |
| live | S3_BUCKET | `opal-data-research` | B2: 'research' after opal-data- is no scope key |
| live | S3_BUCKET | `opal-data-security` | B2: 'security' after opal-data- is no scope key |
| live | S3_BUCKET | `opal-data-security-access-logs` | B2: 'security' after opal-data- is no scope key |
| live | S3_BUCKET | `opal-data-trade-submissions` | B2: 'trade' after opal-data- is no scope key (V2) |
| live | S3_BUCKET_POLICY | `opal-data-security` | B2: 'security' after opal-data- is no scope key |
| live | S3_BUCKET_POLICY | `opal-data-security-access-logs` | B2: 'security' after opal-data- is no scope key |
| live | SCHEDULE | `astn-wsjft-3am-run` | R1.c: 'astn' is an unresolved token (V2) |
| live | SECRET | `astn/brightdata/residential-proxy` | R1.c: 'astn' is an unresolved token (V2) |
| live | SECRET | `astn/ft/credentials` | R1.c: 'astn' is an unresolved token (V2) |
| live | SECRET | `astn/ft/session` | R1.c: 'astn' is an unresolved token (V2) |
| live | SECRET | `astn/kimi/api-key` | R1.c: 'astn' is an unresolved token (V2) |
| live | SECRET | `dowjones/credentials` | R1.f: 'dowjones' is in no vocabulary; no registry row resolves it |
| live | SECURITY_GROUP | `astn-wsjft-scraper-sg` | R1.c: 'astn' is an unresolved token (V2) |
| live | SNS_TOPIC | `astn-wsjft-alerts` | R1.c: 'astn' is an unresolved token (V2) |
| live | SNS_TOPIC | `trade-pipeline-ses-bounces` | R1.c: 'trade' is an unresolved token (V2) |
| live | SNS_TOPIC | `trade-pipeline-ses-complaints` | R1.c: 'trade' is an unresolved token (V2) |
| repo | CW_ALARM | `astn-wsjft-orchestrator-errors` | R1.c: 'astn' is an unresolved token (V2) |
| repo | DYNAMODB_TABLE | `opal-trade-submissions` | R2: 'trade' after opal is an unresolved token (V2) |
| repo | DYNAMODB_TABLE | `trade-security-identifiers` | R1.c: 'trade' is an unresolved token (V2) |
| repo | DYNAMODB_TABLE | `trade-users` | R1.c: 'trade' is an unresolved token (V2) |
| repo | EC2_INSTANCE | `astn-wsjft-scraper` | R1.c: 'astn' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-100am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-100pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-1100am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-1100pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-300am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-345pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-400pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-500am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-500pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-600pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-700am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-745pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-845am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-api-900pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-12pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-1am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-3pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-4am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-6pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-9am` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-rss-9pm` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `news-trending-analysis-daily` | R1.c: 'news' is an unresolved token (V2) |
| repo | EVENT_RULE | `security-sweep-comprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| repo | IAM_POLICY | `F49ServedAndSourceRead` | R1.f: 'f49' is in no vocabulary; no registry row resolves it |
| repo | IAM_POLICY | `NewsIngestionPolicy` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_POLICY | `NewsSemanticClusteringAccess` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_POLICY | `SecuritySweepComprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| repo | IAM_POLICY | `astn-wsjft-orchestrator` | R1.c: 'astn' is an unresolved token (V2) |
| repo | IAM_POLICY | `astn-wsjft-scheduler-invoke` | R1.c: 'astn' is an unresolved token (V2) |
| repo | IAM_POLICY | `astn-wsjft-scraper` | R1.c: 'astn' is an unresolved token (V2) |
| repo | IAM_POLICY | `news-dashboard-policy` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_POLICY | `news-sentiment-permissions` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_POLICY | `opal-news-secrets-read` | R2: 'news' after opal is an unresolved token (V2) |
| repo | IAM_POLICY | `portal-origin-verify-secret` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| repo | IAM_POLICY | `portal-time-machine-invoke-downstream` | R1.f: 'portal' is in no vocabulary; no registry row resolves it |
| repo | IAM_POLICY | `semantic-news-permissions` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| repo | IAM_POLICY | `trade-submission-policy` | R1.c: 'trade' is an unresolved token (V2) |
| repo | IAM_ROLE | `astn-wsjft-orchestrator-role` | R1.c: 'astn' is an unresolved token (V2) |
| repo | IAM_ROLE | `astn-wsjft-scheduler-role` | R1.c: 'astn' is an unresolved token (V2) |
| repo | IAM_ROLE | `astn-wsjft-scraper-role` | R1.c: 'astn' is an unresolved token (V2) |
| repo | IAM_ROLE | `news-dashboard-processor-role` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_ROLE | `news-ingestion-lambda-role` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_ROLE | `news-sentiment-lambda-role` | R1.c: 'news' is an unresolved token (V2) |
| repo | IAM_ROLE | `opal-news-lambda-role` | R2: 'news' after opal is an unresolved token (V2) |
| repo | IAM_ROLE | `security-sweep-dedicated-role` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| repo | IAM_ROLE | `semantic-news-lambda-role` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| repo | IAM_ROLE | `trade-submission-lambda-role` | R1.c: 'trade' is an unresolved token (V2) |
| repo | INSTANCE_PROFILE | `astn-wsjft-scraper-profile` | R1.c: 'astn' is an unresolved token (V2) |
| repo | LAMBDA | `astn-wsjft-orchestrator` | R1.c: 'astn' is an unresolved token (V2) |
| repo | LAMBDA | `cache-control-injector` | R1.f: 'cache' is in no vocabulary; no registry row resolves it |
| repo | LAMBDA | `news-ingestion-scheduler` | R1.c: 'news' is an unresolved token (V2) |
| repo | LAMBDA | `news-semantic-clustering` | R1.c: 'news' is an unresolved token (V2) |
| repo | LAMBDA | `news-trending-analysis` | R1.c: 'news' is an unresolved token (V2) |
| repo | LAMBDA | `opal-news-ai-sentiment` | R2: 'news' after opal is an unresolved token (V2) |
| repo | LAMBDA | `opal-news-layer3-curation` | R2: 'news' after opal is an unresolved token (V2) |
| repo | LAMBDA | `security-sweep-comprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| repo | LAMBDA | `semantic-news-layer3-curation` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| repo | LAMBDA | `trade-auth-handler` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA | `trade-authorizer` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA | `trade-dashboard-api` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA | `trade-identifier-cache` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA | `trade-parquet-batch-export` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA | `trade-submission-handler` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA | `trade-workflow-handler` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LAMBDA_LAYER | `news-trending-deps` | R1.c: 'news' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/cache-control-injector` | R1.f: 'cache' is in no vocabulary; no registry row resolves it |
| repo | LOG_GROUP | `/aws/lambda/news-ingestion-scheduler` | R1.c: 'news' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/news-semantic-clustering` | R1.c: 'news' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/news-trending-analysis` | R1.c: 'news' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/opal-news-ai-sentiment` | R2: 'news' after opal is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/opal-news-layer3-curation` | R2: 'news' after opal is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/security-sweep-comprehensive` | R1.f: 'security' is in no vocabulary; no registry row resolves it |
| repo | LOG_GROUP | `/aws/lambda/semantic-news-layer3-curation` | R1.d: the unresolved token 'news' (V2) comes before any system (V1) |
| repo | LOG_GROUP | `/aws/lambda/trade-auth-handler` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/trade-authorizer` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/trade-dashboard-api` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/trade-identifier-cache` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/trade-parquet-batch-export` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/trade-submission-handler` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/lambda/trade-workflow-handler` | R1.c: 'trade' is an unresolved token (V2) |
| repo | LOG_GROUP | `/aws/vendedlogs/pipes/opal-globgrph-projection-worker` | L2: service 'vendedlogs/pipes' gives no resource type |
| repo | LOG_GROUP | `/opal/github-actions-runner` | L2: service 'opal' gives no resource type |
| repo | S3Key | `%s` | K1: segment 1 '%s' is neither a source nor a tier |
| repo | S3Key | `%s/date=%s/data.parquet` | K1: segment 1 '%s' is neither a source nor a tier |
| repo | S3Key | `_quarantine/` | K1: segment 1 '_quarantine' is neither a source nor a tier |
| repo | S3Key | `agendas/` | K1: segment 1 'agendas' is neither a source nor a tier |
| repo | S3Key | `allowlists/partner-egress.json` | K1: segment 1 'allowlists' is neither a source nor a tier |
| repo | S3Key | `backfill_v2/` | K1: segment 1 'backfill_v2' is neither a source nor a tier |
| repo | S3Key | `benchmarks/LATEST.json` | K1: segment 1 'benchmarks' is neither a source nor a tier |
| repo | S3Key | `benchmarks/data_` | K1: segment 1 'benchmarks' is neither a source nor a tier |
| repo | S3Key | `benchmarks/model_` | K1: segment 1 'benchmarks' is neither a source nor a tier |
| repo | S3Key | `benchmarks/model_20251226_v1.pkl` | K1: segment 1 'benchmarks' is neither a source nor a tier |
| repo | S3Key | `blackdiamond/49f/_ops/probe/` | K3: '_ops' is not a tier (V7) |
| repo | S3Key | `blackdiamond/49f/_ops/pull_state.json` | K3: '_ops' is not a tier (V7) |
| repo | S3Key | `blackdiamond/49f/_ops/taxsma_roster.json` | K3: '_ops' is not a tier (V7) |
| repo | S3Key | `blackdiamond/49f/session-trigger-mode.json` | K3: 'session-trigger-mode.json' is not a tier (V7) |
| repo | S3Key | `blackdiamond/cot/session-trigger-mode.json` | K3: 'session-trigger-mode.json' is not a tier (V7) |
| repo | S3Key | `blackdiamond/cottonwood/meta/` | K3: 'meta' is not a tier (V7) |
| repo | S3Key | `blackdiamond/cottonwood/meta/templates/` | K3: 'meta' is not a tier (V7) |
| repo | S3Key | `cache/fred/BAMLC0A0CM.csv` | K1: segment 1 'cache' is neither a source nor a tier |
| repo | S3Key | `cache/fred/BAMLH0A0HYM2.csv` | K1: segment 1 'cache' is neither a source nor a tier |
| repo | S3Key | `config/dynamic_stopwords.json` | K1: segment 1 'config' is neither a source nor a tier |
| repo | S3Key | `config/etf_universe.json` | K1: segment 1 'config' is neither a source nor a tier |
| repo | S3Key | `config/last-trigger.json` | K1: segment 1 'config' is neither a source nor a tier |
| repo | S3Key | `config/mdpf/route_bindings.yaml` | K1: segment 1 'config' is neither a source nor a tier |
| repo | S3Key | `config/ticker_lookup.json` | K1: segment 1 'config' is neither a source nor a tier |
| repo | S3Key | `consolidated/smartx_allocations.parquet` | K1: segment 1 'consolidated' is neither a source nor a tier |
| repo | S3Key | `contract_integrity/latest.json` | K1: segment 1 'contract_integrity' is neither a source nor a tier |
| repo | S3Key | `daily-reports/` | K1: segment 1 'daily-reports' is neither a source nor a tier |
| repo | S3Key | `daily/49financial` | K1: segment 1 'daily' is neither a source nor a tier |
| repo | S3Key | `data-refresh/archive/` | K1: segment 1 'data-refresh' is neither a source nor a tier |
| repo | S3Key | `data-refresh/varflag/` | K1: segment 1 'data-refresh' is neither a source nor a tier |
| repo | S3Key | `ec2/astn-wsjft/deploy.sh` | K1: segment 1 'ec2' is neither a source nor a tier |
| repo | S3Key | `ec2/etfs-reports` | K1: segment 1 'ec2' is neither a source nor a tier |
| repo | S3Key | `exports/` | K1: segment 1 'exports' is neither a source nor a tier |
| repo | S3Key | `forwardfill_v2/` | K1: segment 1 'forwardfill_v2' is neither a source nor a tier |
| repo | S3Key | `infrastructure/freshness_manifest.json` | K1: segment 1 'infrastructure' is neither a source nor a tier |
| repo | S3Key | `infrastructure/reports/` | K1: segment 1 'infrastructure' is neither a source nor a tier |
| repo | S3Key | `infrastructure/status/latest.json` | K1: segment 1 'infrastructure' is neither a source nor a tier |
| repo | S3Key | `investor-reporting/directory` | K1: segment 1 'investor-reporting' is neither a source nor a tier |
| repo | S3Key | `investor-reporting/directory/_refresh` | K1: segment 1 'investor-reporting' is neither a source nor a tier |
| repo | S3Key | `investor-reporting/directory/latest.json` | K1: segment 1 'investor-reporting' is neither a source nor a tier |
| repo | S3Key | `investor-reporting/export/{firm}/{export_id}/receipt.json` | K1: segment 1 'investor-reporting' is neither a source nor a tier |
| repo | S3Key | `investor-reporting/holdings` | K1: segment 1 'investor-reporting' is neither a source nor a tier |
| repo | S3Key | `json-tiered/market-overview` | K1: segment 1 'json-tiered' is neither a source nor a tier |
| repo | S3Key | `json-tiered/market-overview/details/` | K1: segment 1 'json-tiered' is neither a source nor a tier |
| repo | S3Key | `json-tiered/market-overview/summary/all-returns.json` | K1: segment 1 'json-tiered' is neither a source nor a tier |
| repo | S3Key | `json/` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/benchmarks/benchmark_returns.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/benchmarks/etf_returns.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/benchmarks/model_portfolio_benchmarks.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/benchmarks/model_portfolio_timeseries.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/capital-markets/assumptions.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/capital-markets/views.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/correlations/correlation_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/factor-tilts/` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/latest/` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/latest/manifest.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/macro_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/macro_data_fred.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/timeseries/` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/timeseries/10y.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/timeseries/2y.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/vix_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/volatility_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/macro/yield_curve_fred.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/market/market-regime-history.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/market/market-regime.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/market_metrics.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/mdpf/{firm}/account-distribution.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/model_portfolios/views/` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/peers/peer_performance.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/portfolios/` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/portfolios/account-distribution.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/portfolios/aum-metrics.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/portfolios/aum-timeseries.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/portfolios/non_model_assets.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/positioning/allocation_summary.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/positioning/holdings_attribution_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/positioning/opal_aggregate.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/positioning/positioning_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/security_scanner` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/security_scanner/latest` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/semantic-trending/latest.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/sentiment/fear-greed-index.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/sentiment/keyword-history-articles` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/sentiment/keyword-history-summary` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/sentiment/keyword-sentiments.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/trending/latest.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/valuation/risk_premium_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/valuation/valuation_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/yang-pipeline-metadata.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `json/yang/volatility_data.json` | K1: segment 1 'json' is neither a source nor a tier |
| repo | S3Key | `macro/macro_data.json` | K1: segment 1 'macro' is neither a source nor a tier |
| repo | S3Key | `mdpf/feeds` | K3: 'feeds' is not a tier (V7) |
| repo | S3Key | `mdpf/feeds/model_aua_positions` | K3: 'feeds' is not a tier (V7) |
| repo | S3Key | `mdpf/feeds/non_model_aua` | K3: 'feeds' is not a tier (V7) |
| repo | S3Key | `orion/bronze-trigger-mode.json` | K3: 'bronze-trigger-mode.json' is not a tier (V7) |
| repo | S3Key | `orion/jwt/current.json` | K3: 'jwt' is not a tier (V7) |
| repo | S3Key | `orion/jwt/trigger-mode.json` | K3: 'jwt' is not a tier (V7) |
| repo | S3Key | `otp/current.txt` | K1: segment 1 'otp' is neither a source nor a tier |
| repo | S3Key | `otp/state.json` | K1: segment 1 'otp' is neither a source nor a tier |
| repo | S3Key | `platinum/reports/%s/etf_ownership.pdf` | K4a: '%s' is not an entity partition {entity}={id} |
| repo | S3Key | `platinum/reports/corrections/ETFS_ORION_LABEL_CORRECTION` | K4a: 'corrections' is not an entity partition {entity}={id} |
| repo | S3Key | `quarantine/` | K1: segment 1 'quarantine' is neither a source nor a tier |
| repo | S3Key | `security-reports/` | K1: segment 1 'security-reports' is neither a source nor a tier |
| repo | S3Key | `security-reports/latest_ai_summary.txt` | K1: segment 1 'security-reports' is neither a source nor a tier |
| repo | S3Key | `security-reports/latest_score.json` | K1: segment 1 'security-reports' is neither a source nor a tier |
| repo | S3Key | `semantic_clusters/latest.json` | K1: segment 1 'semantic_clusters' is neither a source nor a tier |
| repo | S3Key | `sentiment/keyword-sentiments.json` | K1: segment 1 'sentiment' is neither a source nor a tier |
| repo | S3Key | `smartx/jwt/current.json` | K3: 'jwt' is not a tier (V7) |
| repo | S3Key | `smartx/platform/silver/fact_model_allocation_roster` | K3: 'platform' is not a tier (V7) |
| repo | S3Key | `smartx/platform/silver/fact_model_aum_daily` | K3: 'platform' is not a tier (V7) |
| repo | S3Key | `smartx/raw` | K3: 'raw' is not a tier (V7) |
| repo | S3Key | `timeseries/` | K1: segment 1 'timeseries' is neither a source nor a tier |
| repo | S3Key | `trending_reports/` | K1: segment 1 'trending_reports' is neither a source nor a tier |
| repo | S3Key | `trending_reports/latest.json` | K1: segment 1 'trending_reports' is neither a source nor a tier |
| repo | S3Key | `uploads/` | K1: segment 1 'uploads' is neither a source nor a tier |
| repo | S3Key | `uploads/manifest.json` | K1: segment 1 'uploads' is neither a source nor a tier |
| repo | S3Key | `views/account_distribution.json` | K1: segment 1 'views' is neither a source nor a tier |
| repo | S3Key | `warehouse/_branch_head.main.json` | K1: segment 1 'warehouse' is neither a source nor a tier |
| repo | S3_BUCKET | `opal-data-astn` | B2: 'astn' after opal-data- is no scope key (V2) |
| repo | S3_BUCKET | `opal-data-news-av` | B2: 'news' after opal-data- is no scope key (V2) |
| repo | S3_BUCKET | `opal-data-news-v2` | B2: 'news' after opal-data- is no scope key (V2) |
| repo | S3_BUCKET | `opal-data-pm` | B2: 'pm' after opal-data- is no scope key |
| repo | S3_BUCKET | `opal-data-portal-s3` | B2: 'portal' after opal-data- is no scope key |
| repo | S3_BUCKET | `opal-data-portfolio` | B2: 'portfolio' after opal-data- is no scope key |
| repo | S3_BUCKET | `opal-data-security` | B2: 'security' after opal-data- is no scope key |
| repo | S3_BUCKET | `opal-data-security-access-logs` | B2: 'security' after opal-data- is no scope key |
| repo | S3_BUCKET | `opal-data-trade-submissions` | B2: 'trade' after opal-data- is no scope key (V2) |
| repo | SCHEDULE | `astn-wsjft-3am-run` | R1.c: 'astn' is an unresolved token (V2) |
| repo | SECURITY_GROUP | `astn-wsjft-scraper-sg` | R1.c: 'astn' is an unresolved token (V2) |
| repo | SNS_TOPIC | `astn-wsjft-alerts` | R1.c: 'astn' is an unresolved token (V2) |
| repo | SNS_TOPIC | `trade-pipeline-ses-bounces` | R1.c: 'trade' is an unresolved token (V2) |
| repo | SNS_TOPIC | `trade-pipeline-ses-complaints` | R1.c: 'trade' is an unresolved token (V2) |
