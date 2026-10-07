# Reached-roles census (NFRA_CTLPLN CT-a-1 amendment 1, worker 0.9.0_WK_NFRA_CTLPLN~14)

Taken 2026-10-07T11:05:41Z from the live account, read-only (list/describe/get and iam simulate-principal-policy). Saved: `infra/aws/terraform/nfra-ctlpln-identity/tests/reached_roles_census.json`.

```
ROLE-CENSUS functions=233 tasks=9 hosts=33 roles=175 read=175 unread=0 yes_iam=1 yes_trail=0 yes_delete=9 yes_any=10 no=165 resident_host_role=NO ok=True
```

**Blind spots.** EVALUATOR BLIND SPOTS: iam simulate-principal-policy reads the role's identity policies (and permissions boundary); it does NOT apply resource policies on the target (a bucket policy may still refuse) or organisation SCPs. YES = the role's own policies allow it; NO = firm for identity policy only. Task definitions: latest ACTIVE revision per family only (an older ACTIVE revision may carry a different role). Host routes (documents, S3 prefixes) are read from repository text, not from the account; associations that target hosts by tag, and instance user-data, are not resolved. The role read is the control.

**Resident host** `i-0167fd745ad906a66` (irpt-ycharts-runner): role `irpt-ycharts-runner-role` reads **NO** on all three questions (7 IAM, 4 CloudTrail, 24 bucket-object deletes + bucket delete + dynamodb/rds, N of N read).

## Roles that read YES (10 of 175 distinct roles)

### `bd-exporter-ec2-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-bd
- Policies: attached ['bd-securities-access', 'AmazonSSMManagedInstanceCore']; inline ['AdditionalPermissions', 'advi-49f-chain-access', 'advi-49f-publisher-platinum-put', 'cloudfront-invalidate', 'cross-firm-bucket-deny', 'describe-tags-self', 'events-emit', 'gold-layer-trigger', 'mdpf-secclass-scheduled-put-policy', 'monolith-bd49f-xref-silver-read', 'monolith-schwab-08242234-silver-read', 'monolith-schwab-08335338-silver-read', 'pipeline-chain', 'runner-shared-read', 's3-access', 'schwab-bucket-access']
- Routes (14):
  - HOST i-0090b823a4a0997e3 `bd-gold-qa-runner` (us-east-1, stopped) route=ROUTE-FOUND documents=['opal-bd-49f-session-fetch'] s3_uris=[]
  - HOST i-00abf626b065373bc `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-00c7568bc510f7423 `bd-transactions` (us-east-1, stopped) route=ROUTE-FOUND documents=['opal-bd-49f-session-fetch'] s3_uris=[]
  - HOST i-01003b035d2988dfb `bd-gold-layer-runner` (us-east-1, stopped) route=ROUTE-FOUND documents=['advi-49f-chain-dispatch', 'opal-bd-49f-session-fetch'] s3_uris=[]
  - HOST i-025cba31603a6c8a6 `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-032fa1babe1abe48a `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-03c397afaa967d978 `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-0416edf7e4b901380 `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-0800437d1dbb0b5cc `bd-allocations` (us-east-1, stopped) route=ROUTE-FOUND documents=['opal-bd-49f-session-fetch'] s3_uris=[]
  - HOST i-0868fc7e7ebec26f2 `bd-fees` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-088e7fa9323bac1b9 `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-094c504a4384f9c47 `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-0e6f6dc014fdcf1cd `bd-assets` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]
  - HOST i-0ec91038b9a2c73a6 `historical-prices-fetcher` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]

### `bd-processor-lambda-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-bd
- Policies: attached ['AWSLambdaBasicExecutionRole']; inline ['bd-s3-readwrite', 'pipeline-chain']
- Routes (2):
  - FUNCTION `bd-price-update` (us-east-1) UPDATABLE
  - FUNCTION `opal-bd-transaction-consolidator` (us-east-1) UPDATABLE

### `cot-exporter-ec2-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-cot
- Policies: attached ['AmazonSSMManagedInstanceCore']; inline ['cot-exporter-policy', 'cross-firm-bucket-deny']
- Routes (1):
  - HOST i-0643a5bee8a8feabf `cot-exporter` (us-east-1, stopped) route=ROUTE-FOUND documents=['opal-cot-bd-session-fetch', 'opal-cot-bronze-run', 'opal-cot-gold-run', 'opal-cot-silver-run'] s3_uris=['s3://opal-data-cot/code/bronze/cot_bronze_ingest.py', 's3://opal-data-cot/code/gold/', 's3://opal-data-cot/code/silver/cot_silver_merge.py', 's3://opal-data-cot/logs/cot-exporter/bronze-run/$', 's3://opal-data-cot/logs/cot-exporter/gold-run/$', 's3://opal-data-cot/logs/cot-exporter/session-fetch/$', 's3://opal-data-cot/logs/cot-exporter/silver-run/$']

### `inf-gold-layer-ec2-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-inf
- Policies: attached ['AmazonSSMManagedInstanceCore']; inline ['cloudfront-invalidate', 'cloudwatch-logs', 'cloudwatch-put-metric', 'cross-firm-bucket-deny', 'describe-tags-self', 'kms-ebs-decrypt', 'runner-shared-read', 's3-scoped-inf', 'secrets-manager-orion-jwt', 'self-stop', 'sns-publish-chainfatal', 'ssm-access']
- Routes (1):
  - HOST i-0ed5afded2ebd4ed4 `inf-gold-layer-runner` (us-east-1, stopped) route=ROUTE-FOUND documents=['opal-bd-49f-session-fetch', 'opal-cot-bd-session-fetch', 'opal-inf-export-run', 'opal-inf-jwt-fetch', 'opal-inf-jwt-setup', 'opal-inf-test-login-stage1', 'opal-inf-test-login-stage2', 'opal-inf-test-login-stage3'] s3_uris=['s3://opal-data-inf/code/exporter/inf-jwt-fetch.sh', 's3://opal-data-inf/code/exporter/stepwise/', 's3://opal-data-inf/gold/logs/inf-exporter/$']

### `inf-gold-layer-lambda-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-inf
- Policies: attached ['AWSLambdaBasicExecutionRole']; inline ['cloudfront-invalidate', 'cross-firm-bucket-deny', 'inf-s3-scoped', 'invoke-publisher-fanout']
- Routes (3):
  - FUNCTION `inf-client-detail` (us-east-1) UPDATABLE
  - FUNCTION `inf-portal-advisor-publisher` (us-east-1) UPDATABLE
  - FUNCTION `inf-portal-publisher` (us-east-1) UPDATABLE

### `lambda-execution-role` -- YES-IAM

- IAM actions allowed: iam:PassRole
- Policies: attached ['AWSLambdaBasicExecutionRole']; inline ['BDPipelinePermissions', 'cross-firm-bucket-write-deny', 'FargateTriggerPermissions', 'LambdaSelfInvoke', 'layer3-bd-securities-read', 'NewsSemanticClusteringAccess', 'OpalAuthSecretsAccess', 'OpalDataPMAccess', 'OpalDataPMCacheBustAccess', 'OpalDataPMUploadAccess', 'OpalPMDynamoDBAccess', 'portal-v2-autosave-list-policy', 'PortfolioExportPolicy', 'S3Access', 'SeekingAlpha-S3-Access', 'SeekingAlpha-SecretsAccess', 'SemanticLayer3CurationAccess', 'SemanticTrendingPublisherS3Access']
- Routes (13):
  - FUNCTION `news-semantic-clustering` (us-east-1) UPDATABLE
  - FUNCTION `opal-pm-optimization-autosave-put` (us-east-1) UPDATABLE
  - FUNCTION `opal-pm-optimization-loader` (us-east-1) UPDATABLE
  - FUNCTION `opal-pm-snapshot-handler` (us-east-1) UPDATABLE
  - FUNCTION `opal-pm-upload-urls` (us-east-1) UPDATABLE
  - FUNCTION `opal-portfolio-autosave-get` (us-east-1) UPDATABLE
  - FUNCTION `opal-portfolio-autosave-put` (us-east-1) UPDATABLE
  - FUNCTION `opal-portfolio-funds-list` (us-east-1) UPDATABLE
  - FUNCTION `opal-portfolio-pickle-parser` (us-east-1) UPDATABLE
  - FUNCTION `opal-portfolio-version-get` (us-east-1) UPDATABLE
  - FUNCTION `opal-portfolio-versions-list` (us-east-1) UPDATABLE
  - FUNCTION `semantic-news-layer3-curation` (us-east-1) UPDATABLE
  - FUNCTION `semantic-trending-topics-portal-publisher` (us-east-1) UPDATABLE

### `opal-news-lambda-role` -- YES-DELETE

- Delete actions allowed: dynamodb:DeleteTable; data buckets: (not bucket-scoped)
- Policies: attached ['AWSLambdaBasicExecutionRole', 'AmazonS3ReadOnlyAccess', 'AmazonDynamoDBFullAccess']; inline ['cross-firm-bucket-read-deny', 'cross-firm-secret-deny', 'invoke-trending-publisher', 'opal-news-secrets-read']
- Routes (2):
  - FUNCTION `opal-news-layer3-curation` (us-east-1) UPDATABLE
  - FUNCTION `opal-news-layer3-curation` (us-east-2) UPDATABLE

### `opal-portal-lambda-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-news-v2, opal-data-portal-v2
- Policies: attached []; inline ['cross-firm-secret-deny', 'lambda-invoke-finbert', 'MonitorAnthropicSecretRead', 'MonitorDataFreshnessRead', 'MonitorGraphHeadContractRead', 'MonitorLogsRead', 'MonitorSnsEgressRead', 'opal-bedrock-invoke', 'opal-cloudfront-invalidation', 'opal-infrastructure-monitor', 'opal-portal-dynamodb', 'opal-portal-logs', 'opal-portal-s3-read', 'opal-portal-secrets', 'opal-sessions-dynamodb', 'opal-sessions-secrets', 'portal-origin-verify-secret', 'SecretsManagerAccess']
- Routes (12):
  - FUNCTION `finbert-batch-processor` (us-east-1) UPDATABLE
  - FUNCTION `opal-infrastructure-monitor` (us-east-1) UPDATABLE
  - FUNCTION `opal-market-overview-tiered-generator` (us-east-1) UPDATABLE
  - FUNCTION `opal-market-regime-classifier` (us-east-1) UPDATABLE
  - FUNCTION `opal-news-ai-sentiment` (us-east-1) UPDATABLE
  - FUNCTION `opal-portal-authorizer` (us-east-1) DENIED-TODAY
  - FUNCTION `opal-portal-data-proxy` (us-east-1) UPDATABLE
  - FUNCTION `opal-portal-fear-greed-fetcher` (us-east-1) UPDATABLE
  - FUNCTION `opal-portal-rest-authorizer` (us-east-1) DENIED-TODAY
  - FUNCTION `opal-portal-volatility-fetcher` (us-east-1) UPDATABLE
  - FUNCTION `opal-session-analytics` (us-east-1) UPDATABLE
  - FUNCTION `opal-trending-topics-portal-publisher` (us-east-1) UPDATABLE

### `smartx-exporter-role-20251218220948293500000001` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-portal-v2
- Policies: attached ['AmazonSSMManagedInstanceCore']; inline ['ecr-access', 'lambda-invoke', 's3-access', 'secrets-access', 'self-shutdown']
- Routes (1):
  - HOST i-06ebcb27395eb3f49 `smartx-exporter` (us-east-1, stopped) route=NO-ROUTE-FOUND documents=[] s3_uris=[]

### `smartx-ingestion-lambda-role` -- YES-DELETE

- Delete actions allowed: s3:DeleteObject; data buckets: opal-data-portal-v2
- Policies: attached ['AWSLambdaBasicExecutionRole']; inline ['smartx-dynamodb-access', 'smartx-s3-access']
- Routes (1):
  - FUNCTION `opal-smartx-ingestion-pipeline` (us-east-1) UPDATABLE

## The ten name-protected functions

- `auth-validator-edge` -> `lambda-edge-execution-role`: NO
- `cache-control-injector` -> `lambda-edge-execution-role`: NO
- `opal-portal-authorizer` -> `opal-portal-lambda-role`: YES-DELETE
- `opal-portal-rest-authorizer` -> `opal-portal-lambda-role`: YES-DELETE
- `opalinvest-auth-handler` -> `opalinvest-auth-lambda-role`: NO
- `public-data-router` -> `lambda-edge-execution-role`: NO
- `shared-advisor-router` -> `lambda-edge-execution-role`: NO
- `shared-advisor-router-response` -> `lambda-edge-execution-role`: NO
- `trade-auth-handler` -> `trade-submission-lambda-role`: NO
- `trade-authorizer` -> `trade-submission-lambda-role`: NO

## Counts

Routes by kind: {'function': 233, 'host': 32, 'task-role': 9, 'task-exec-role': 9}. Hosts with no instance profile: [('i-06376c11d8b3c3443', 'seeking-alpha-scraper', 'stopped')]. Hosts NO-ROUTE-FOUND in the repository read: 21 of 33.
