# NAMING_CENSUS_REPORT -- census mode, the run (LGIC_ENFORCE EN-s-1, DEC-7)

Written by `python lib/opal_naming.py census --live --repo --report <this file>` at registry@50e4fabd1cb6a150.
Every number below is recomputable from the fenced json at the end.

## Status

**STOPPED on the first RAISE**: live plane, type API_GW, name `sentiment-query-api` -- R1.f: 'sentiment' is in no vocabulary; no registry row resolves it. A RAISE is a defect in the rule, the schema or the registry and is never filed under a verdict (NAMING_SCHEMA.json grade.unplaceable), so the rows below are the names judged BEFORE the stop, and the run is not complete.

## The live plane

- Vintage: `Built from the estate as of 2026-09-15 00:57:50 UTC. Stitch source: stitch-codebuild built 2026-09-14T03:01:18Z.  manifest: e8a06d444ae8`.
- Instrument: `comp-find --corpus aws --name . API_GW API_ROUTE CLOUDFRONT_DISTRIBUTION CODEBUILD_PROJECT CW_ALARM DYNAMODB_TABLE EC2_INSTANCE ECS_CLUSTER ECS_TASK_DEFINITION EVENT_RULE EVENT_SOURCE IAM_POLICY IAM_ROLE IAM_USER INSTANCE_PROFILE KMS_KEY LAMBDA LAMBDA_LAYER LOAD_BALANCER LOG_GROUP ROUTE53_RECORD S3Key S3_BUCKET S3_BUCKET_POLICY SCHEDULE SECRET SECURITY_GROUP SERVICE_PRINCIPAL SNS_TOPIC SQS_QUEUE SSM_DOCUMENT STATE_MACHINE VPC_ENDPOINT --all --budget 600`.
- live = **2148** nodes; minus 327 of the NOT GRADED types (API_ROUTE 184, CLOUDFRONT_DISTRIBUTION 2, EVENT_SOURCE 96, IAM_USER 4, KMS_KEY 14, ROUTE53_RECORD 3, SERVICE_PRINCIPAL 21, VPC_ENDPOINT 3); minus 16 names NAMING_SCHEMA.json aws_fixed puts outside the grade's domain (IAM_POLICY 10, LOG_GROUP 4, SECURITY_GROUP 2); live_nameable = **1805**.
- judged_live = **3** of 1805. Verdicts: {'CONFORMANT': 2, 'OUT-OF-PATTERN': 1}.

## The repo plane

- Terraform: 468 tracked .tf files under `infra/aws/terraform/`; the name attribute of each resource of a graded type (`CENSUS_TF_ATTR`), when it is ONE literal; 113 name(s) that are expressions are not names and are not judged.
- Sources: 465 tracked files -- every config.py, and the Lambda sources under `infra/aws/lambda/` (.py, .mjs, .js, .cjs, .ts) -- after 2864 vendored and test files were excluded; each string literal `_census_classify` places as a name; 0 placed template(s) are not names; 0 file(s) unparsed.
- repo = **1869** names; judged_repo = **0**. Verdicts: {}.

## Totals by type (judged rows)

| type | plane | CONFORMANT | ALIAS | OUT-OF-PATTERN | NOT-GRADED |
|---|---|---|---|---|---|
| API_GW | live | 2 | 0 | 1 | 0 |

The comparison against LGIC_NAMING's hand gradings is EN-s-2's and is not made here.

```json
{
 "vintage": "Built from the estate as of 2026-09-15 00:57:50 UTC. Stitch source: stitch-codebuild built 2026-09-14T03:01:18Z.  manifest: e8a06d444ae8",
 "live_command": "comp-find --corpus aws --name . API_GW API_ROUTE CLOUDFRONT_DISTRIBUTION CODEBUILD_PROJECT CW_ALARM DYNAMODB_TABLE EC2_INSTANCE ECS_CLUSTER ECS_TASK_DEFINITION EVENT_RULE EVENT_SOURCE IAM_POLICY IAM_ROLE IAM_USER INSTANCE_PROFILE KMS_KEY LAMBDA LAMBDA_LAYER LOAD_BALANCER LOG_GROUP ROUTE53_RECORD S3Key S3_BUCKET S3_BUCKET_POLICY SCHEDULE SECRET SECURITY_GROUP SERVICE_PRINCIPAL SNS_TOPIC SQS_QUEUE SSM_DOCUMENT STATE_MACHINE VPC_ENDPOINT --all --budget 600",
 "denominators": {
  "repo": 1869,
  "live": 2148,
  "live_nameable": 1805,
  "judged_live": 3,
  "judged_repo": 0,
  "live_not_graded_types": 327,
  "live_aws_fixed": 16
 },
 "registry": "50e4fabd1cb6a150",
 "stopped": {
  "plane": "live",
  "type": "API_GW",
  "current": "sentiment-query-api",
  "message": "R1.f: 'sentiment' is in no vocabulary; no registry row resolves it"
 },
 "rows": [
{"current": "inf-otp-relay-api", "canonical": "{system}-inf-otp-relay-api", "verdict": "OUT-OF-PATTERN", "type": "API_GW", "plane": "live"},
{"current": "opal-portal-data-proxy-api", "canonical": "opal-portal-data-proxy-api", "verdict": "CONFORMANT", "type": "API_GW", "plane": "live"},
{"current": "opal-session-analytics-api", "canonical": "opal-session-analytics-api", "verdict": "CONFORMANT", "type": "API_GW", "plane": "live"}
 ]
}
```
