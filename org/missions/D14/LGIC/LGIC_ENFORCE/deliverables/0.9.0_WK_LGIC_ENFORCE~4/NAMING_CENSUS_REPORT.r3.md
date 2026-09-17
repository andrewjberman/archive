# NAMING_CENSUS_REPORT -- census mode, the run (LGIC_ENFORCE EN-s-1, DEC-7)

Written by `python lib/opal_naming.py census --live --repo --report <this file>` at registry@26623a452ff8583d.
Every number below is recomputable from the fenced json at the end.

## Status

**STOPPED on the first RAISE**: live plane, type CW_ALARM, name `astn-wsjft-orchestrator-errors` -- R1.c: 'astn' is an unresolved token (V2). A RAISE is a defect in the rule, the schema or the registry and is never filed under a verdict (NAMING_SCHEMA.json grade.unplaceable), so the rows below are the names judged BEFORE the stop, and the run is not complete.

## The live plane

- Vintage: `Built from the estate as of 2026-09-17 14:41:29 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest: c92a803a1057`.
- Instrument: `comp-find --corpus aws --name . API_GW API_ROUTE CLOUDFRONT_DISTRIBUTION CODEBUILD_PROJECT CW_ALARM DYNAMODB_TABLE EC2_INSTANCE ECS_CLUSTER ECS_TASK_DEFINITION EVENT_RULE EVENT_SOURCE IAM_POLICY IAM_ROLE IAM_USER INSTANCE_PROFILE KMS_KEY LAMBDA LAMBDA_LAYER LOAD_BALANCER LOG_GROUP ROUTE53_RECORD S3Key S3_BUCKET S3_BUCKET_POLICY SCHEDULE SECRET SECURITY_GROUP SERVICE_PRINCIPAL SNS_TOPIC SQS_QUEUE SSM_DOCUMENT STATE_MACHINE VPC_ENDPOINT --all --budget 600`.
- live = **2190** nodes; minus 346 of the NOT GRADED types (API_ROUTE 202, CLOUDFRONT_DISTRIBUTION 2, EVENT_SOURCE 97, IAM_USER 4, KMS_KEY 14, ROUTE53_RECORD 3, SERVICE_PRINCIPAL 21, VPC_ENDPOINT 3); minus 16 names NAMING_SCHEMA.json aws_fixed puts outside the grade's domain (IAM_POLICY 10, LOG_GROUP 4, SECURITY_GROUP 2); live_nameable = **1828**.
- judged_live = **21** + carded_live **2** (NOT-JUDGED, R-29) = 23 of live_nameable 1828. Verdicts: {'CONFORMANT': 3, 'OUT-OF-PATTERN': 18}.

## The repo plane

- Terraform: 473 tracked .tf files under `infra/aws/terraform/`; the name attribute of each resource of a graded type (NAMING_SCHEMA.json tf_type_map), when it is ONE literal; 128 name(s) that are expressions are not names and are not judged.
- Sources: 468 tracked files -- every config.py, and the Lambda sources under `infra/aws/lambda/` (.py, .mjs, .js, .cjs, .ts) -- after 2864 vendored and test files were excluded; each string literal `_census_classify` places as a name; 0 placed template(s) are not names; 0 file(s) unparsed.
- repo = **1878** names; judged_repo = **0** + carded_repo **0** (NOT-JUDGED, R-29) = 0. Verdicts: {}.

## Carded (NOT-JUDGED, R-29 / AMENDMENT 1)

2 name(s) carded rather than graded -- each RAISE's owner could not be measured from a declared source, or its mint would touch a GENERATED POLICY on an APPLIED resource; see each name's owner card. `sentiment-query-api` (live); `trade-submission-api` (live)

## Totals by type (judged rows)

| type | plane | CONFORMANT | ALIAS | OUT-OF-PATTERN | NOT-GRADED |
|---|---|---|---|---|---|
| API_GW | live | 2 | 0 | 1 | 0 |
| CODEBUILD_PROJECT | live | 1 | 0 | 4 | 0 |
| CW_ALARM | live | 0 | 0 | 13 | 0 |

The comparison against LGIC_NAMING's hand gradings is EN-s-2's and is not made here.

```json
{
 "vintage": "Built from the estate as of 2026-09-17 14:41:29 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest: c92a803a1057",
 "live_command": "comp-find --corpus aws --name . API_GW API_ROUTE CLOUDFRONT_DISTRIBUTION CODEBUILD_PROJECT CW_ALARM DYNAMODB_TABLE EC2_INSTANCE ECS_CLUSTER ECS_TASK_DEFINITION EVENT_RULE EVENT_SOURCE IAM_POLICY IAM_ROLE IAM_USER INSTANCE_PROFILE KMS_KEY LAMBDA LAMBDA_LAYER LOAD_BALANCER LOG_GROUP ROUTE53_RECORD S3Key S3_BUCKET S3_BUCKET_POLICY SCHEDULE SECRET SECURITY_GROUP SERVICE_PRINCIPAL SNS_TOPIC SQS_QUEUE SSM_DOCUMENT STATE_MACHINE VPC_ENDPOINT --all --budget 600",
 "denominators": {
  "repo": 1878,
  "live": 2190,
  "live_nameable": 1828,
  "judged_live": 21,
  "judged_repo": 0,
  "live_not_graded_types": 346,
  "live_aws_fixed": 16,
  "carded_live": 2,
  "carded_repo": 0
 },
 "registry": "26623a452ff8583d",
 "stopped": {
  "plane": "live",
  "type": "CW_ALARM",
  "current": "astn-wsjft-orchestrator-errors",
  "message": "R1.c: 'astn' is an unresolved token (V2)"
 },
 "not_judged": [
  {
   "name": "sentiment-query-api",
   "plane": "live",
   "card": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/OWNER_CARDS_S6.r3.md#card-1----sentiment-query-api-live-api_gw"
  },
  {
   "name": "trade-submission-api",
   "plane": "live",
   "card": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/OWNER_CARDS_S6.r3.md#card-2----trade-submission-api-live-api_gw"
  }
 ],
 "rows": [
{"current": "inf-otp-relay-api", "canonical": "advi-inf-otp-relay-api", "verdict": "OUT-OF-PATTERN", "type": "API_GW", "plane": "live"},
{"current": "opal-portal-data-proxy-api", "canonical": "opal-portal-data-proxy-api", "verdict": "CONFORMANT", "type": "API_GW", "plane": "live"},
{"current": "opal-session-analytics-api", "canonical": "opal-session-analytics-api", "verdict": "CONFORMANT", "type": "API_GW", "plane": "live"},
{"current": "estate-report-seam-freshness-publisher", "canonical": "estate-report-seam-freshness-publisher-build", "verdict": "OUT-OF-PATTERN", "type": "CODEBUILD_PROJECT", "plane": "live"},
{"current": "globgrph-derive-build", "canonical": "globgrph-derive-build", "verdict": "CONFORMANT", "type": "CODEBUILD_PROJECT", "plane": "live"},
{"current": "opal-drift-producer", "canonical": "opal-drift-producer-build", "verdict": "OUT-OF-PATTERN", "type": "CODEBUILD_PROJECT", "plane": "live"},
{"current": "opal-stitch-produce", "canonical": "opal-stitch-produce-build", "verdict": "OUT-OF-PATTERN", "type": "CODEBUILD_PROJECT", "plane": "live"},
{"current": "semantic-clustering-lambda-build", "canonical": "{system}-semantic-clustering-lambda-build", "verdict": "OUT-OF-PATTERN", "type": "CODEBUILD_PROJECT", "plane": "live"},
{"current": "ExecIncrParityFailure", "canonical": "{system}-exec-incrparity-failure-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "FIRMSEP-auth-advisor-scoping-denied", "canonical": "firmsep-auth-advisor-scoping-denied-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "FIRMSEP-auth-ownership-map-fetch-failed", "canonical": "firmsep-auth-ownership-map-fetch-failed-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "FIRMSEP-auth-ownership-map-schema-mismatch", "canonical": "firmsep-auth-ownership-map-schema-mismatch-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "FIRMSEP-auth-tier-denied", "canonical": "firmsep-auth-tier-denied-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "FIRMSEP-shared-advisor-router-denied", "canonical": "firmsep-shared-advisor-router-denied-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "Inflection-HistBackfill-FailureSpike", "canonical": "{system}-inf-hist-backfill-failure-spike-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "Inflection-JwtResilience-NearExpirySpike", "canonical": "{system}-inf-jwt-resilience-near-expiry-spike-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "Inflection-SilverChain-DimConversionFailure", "canonical": "{system}-inf-silver-chain-dim-conversion-failure-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "OPSEC-auth-login-rate-limit-blocked", "canonical": "{system}-opsec-auth-login-rate-limit-blocked-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "OPSEC-auth-throttled", "canonical": "{system}-opsec-auth-throttled-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "PortfolioExcelGenerator-Errors", "canonical": "{system}-portfolio-excel-generator-errors-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"},
{"current": "YChartsSessionEviction", "canonical": "ycharts-session-eviction-alarm", "verdict": "OUT-OF-PATTERN", "type": "CW_ALARM", "plane": "live"}
 ]
}
```
