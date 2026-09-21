<!-- ADDITIVE SIBLING. The original is READ-ONLY and not one byte of it moved.
     Author: 0.9.0_WK_LGIC_ENFORCE~1, LGIC_ENFORCE round 19, cell EN-h-1.
     Hand side re-measured at the census vintage the MACHINE side used:
       Built from the estate as of 2026-09-18 12:17:28 UTC. Stitch source: stitch-codebuild built 2026-09-18T03:01:14Z. manifest 247f3933a1fd
       org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r8.md @54659987c0
     The machine side is NOT re-graded here and grade() is never called.
-->

# GRADING_RULE -- WORKED CASES, HAND SIDE RE-MEASURED (round 19)

Sibling of `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`. 45 worked cases, re-derived at this cell's write time.

```json
{
 "vintage": "Built from the estate as of 2026-09-18 12:17:28 UTC. Stitch source: stitch-codebuild built 2026-09-18T03:01:14Z. manifest 247f3933a1fd",
 "note": "Re-measured hand side of GRADING_RULE.md section 9's worked cases. Each verdict/canonical_form is the WRITTEN RULE re-applied against the registry at 54659987c0; `basis` names the row that decided it. The original GRADING_RULE.md is unchanged.",
 "worked_cases": [
  {
   "name": "mdpf-gold-lambda",
   "type": "LAMBDA",
   "verdict": "CONFORMANT",
   "canonical_form": "mdpf-gold-lambda",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "mdpf-gold-lambda",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "mdpf-lambda-lambda",
   "type": "LAMBDA",
   "verdict": "RAISE",
   "canonical_form": null,
   "verdict_at_round_9": "RAISE",
   "canonical_form_at_round_9": null,
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "orion-orion-lambda-lambda",
   "type": "LAMBDA",
   "verdict": "RAISE",
   "canonical_form": null,
   "verdict_at_round_9": "RAISE",
   "canonical_form_at_round_9": null,
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "inf-silver-chain",
   "type": "LAMBDA",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "advi-inf-silver-chain-lambda",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "{system}-inf-silver-chain-lambda",
   "basis": "REVISED-REGISTRY-ROW",
   "evidence": "infra/logic/registry/resources.json @54659987c0 carries the row (inf-silver-chain, LAMBDA) -> system advi; GRADING_RULE.md R1.d says the placeholder stands only until the registry's resource-to-system row fills it"
  },
  {
   "name": "inf-api-eclipse",
   "type": "LAMBDA",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "eclipse-inf-api-lambda",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "eclipse-inf-api-lambda",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "etfs-canon-fanin-role",
   "type": "IAM_ROLE",
   "verdict": "CONFORMANT",
   "canonical_form": "etfs-canon-fanin-role",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "etfs-canon-fanin-role",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "bd-49f-runner-role",
   "type": "IAM_ROLE",
   "verdict": "ALIAS",
   "canonical_form": "blackdiamond-49f-runner-role",
   "verdict_at_round_9": "ALIAS",
   "canonical_form_at_round_9": "blackdiamond-49f-runner-role",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "FredMacroIngestionLambdaRole",
   "type": "IAM_ROLE",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "fred-macro-ingestion-lambda-role",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "fred-macro-ingestion-lambda-role",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "irpt-directory-policy",
   "type": "IAM_POLICY",
   "verdict": "CONFORMANT",
   "canonical_form": "irpt-directory-policy",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "irpt-directory-policy",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "s3-etfs-read",
   "type": "IAM_POLICY",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "etfs-s3-read-policy",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "etfs-s3-read-policy",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-data-49financial#policy",
   "type": "IAM_POLICY",
   "verdict": "CONFORMANT",
   "canonical_form": "opal-data-49financial#policy",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "opal-data-49financial#policy",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "mdpf-daily-runner-profile",
   "type": "INSTANCE_PROFILE",
   "verdict": "CONFORMANT",
   "canonical_form": "mdpf-daily-runner-profile",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "mdpf-daily-runner-profile",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "default",
   "type": "SECURITY_GROUP",
   "verdict": "NOT-GRADED",
   "canonical_form": null,
   "verdict_at_round_9": "NOT-GRADED",
   "canonical_form_at_round_9": null,
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "etfs-reports-reporter-sg",
   "type": "SECURITY_GROUP",
   "verdict": "CONFORMANT",
   "canonical_form": "etfs-reports-reporter-sg",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "etfs-reports-reporter-sg",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-portal-data-proxy-api",
   "type": "API_GW",
   "verdict": "CONFORMANT",
   "canonical_form": "opal-portal-data-proxy-api",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "opal-portal-data-proxy-api",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "irpt-jobs",
   "type": "DYNAMODB_TABLE",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "irpt-jobs-table",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "irpt-jobs-table",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "irpt-export-dlq",
   "type": "SQS_QUEUE",
   "verdict": "CONFORMANT",
   "canonical_form": "irpt-export-dlq",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "irpt-export-dlq",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "etfs-reports-alerts",
   "type": "SNS_TOPIC",
   "verdict": "CONFORMANT",
   "canonical_form": "etfs-reports-alerts",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "etfs-reports-alerts",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "Inflection-SilverChain-DimConversionFailure",
   "type": "CW_ALARM",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "advi-inf-silver-chain-dim-conversion-failure-alarm",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "{system}-inf-silver-chain-dim-conversion-failure-alarm",
   "basis": "REVISED-REGISTRY-ROW",
   "evidence": "infra/logic/registry/resources.json @54659987c0 carries the row (Inflection-SilverChain-DimConversionFailure, CW_ALARM) -> system advi; GRADING_RULE.md R1.d says the placeholder stands only until the registry's resource-to-system row fills it"
  },
  {
   "name": "pandas-pyarrow-layer",
   "type": "LAMBDA_LAYER",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "{system}-pandas-pyarrow-layer",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "{system}-pandas-pyarrow-layer",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "mdpf-daily-runner",
   "type": "EC2_INSTANCE",
   "verdict": "CONFORMANT",
   "canonical_form": "mdpf-daily-runner",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "mdpf-daily-runner",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-stitch-produce",
   "type": "CODEBUILD_PROJECT",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "opal-stitch-produce-build",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "opal-stitch-produce-build",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-cot-silver-run",
   "type": "SSM_DOCUMENT",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "opal-cot-silver-run-document",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "opal-cot-silver-run-document",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "globgrph-serving",
   "type": "ECS_TASK_DEFINITION",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "globgrph-serving-task",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "globgrph-serving-task",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "YangDataPipeline",
   "type": "STATE_MACHINE",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "yang-data-pipeline-sfn",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "yang-data-pipeline-sfn",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-gateway",
   "type": "LOAD_BALANCER",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "gateway-lb",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "gateway-lb",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-globgrph",
   "type": "ECS_CLUSTER",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "globgrph-cluster",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "globgrph-cluster",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "etfs-netassets-daily",
   "type": "EVENT_RULE",
   "verdict": "CONFORMANT",
   "canonical_form": "etfs-netassets-daily",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "etfs-netassets-daily",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "bd-49f-session-complete",
   "type": "EVENT_RULE",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "blackdiamond-49f-session-complete-{cadence}",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "blackdiamond-49f-session-complete-{cadence}",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "wsb-49f-model-aua-pull-daily",
   "type": "SCHEDULE",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "{system}-49f-wsb-model-aua-pull-daily",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "{system}-49f-wsb-model-aua-pull-daily",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "mdpf-accrual-bridge-daily",
   "type": "SCHEDULE",
   "verdict": "CONFORMANT",
   "canonical_form": "mdpf-accrual-bridge-daily",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "mdpf-accrual-bridge-daily",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "/aws/lambda/mdpf-gold-lambda",
   "type": "LOG_GROUP",
   "verdict": "CONFORMANT",
   "canonical_form": "/aws/lambda/mdpf-gold-lambda",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "/aws/lambda/mdpf-gold-lambda",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-data-bd",
   "type": "S3_BUCKET",
   "verdict": "ALIAS",
   "canonical_form": "opal-data-49financial",
   "verdict_at_round_9": "ALIAS",
   "canonical_form_at_round_9": "opal-data-49financial",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-cloudtrail-logs-313476888478",
   "type": "S3_BUCKET",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "opal-313476888478-cloudtrail-logs",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "opal-313476888478-cloudtrail-logs",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "opal-data-cot",
   "type": "S3_BUCKET_POLICY",
   "verdict": "ALIAS",
   "canonical_form": "opal-data-cottonwood",
   "verdict_at_round_9": "ALIAS",
   "canonical_form_at_round_9": "opal-data-cottonwood",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "platinum/firm/header_metrics.json",
   "type": "S3Key",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "advi/{scope}/platinum/firm/header_metrics.json",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "advi/{scope}/platinum/firm/header_metrics.json",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "code/gold/*",
   "type": "S3Key",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "{source}/{scope}/code/gold/*",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "{source}/{scope}/code/gold/*",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "schwab/08335338/silver/fact_rps/",
   "type": "S3Key",
   "verdict": "CONFORMANT",
   "canonical_form": "schwab/08335338/silver/fact_rps/",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "schwab/08335338/silver/fact_rps/",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz",
   "type": "S3Key",
   "verdict": "CONFORMANT",
   "canonical_form": "mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "advi/49financial/platinum/advisors/advisor_id=A123/positions.json",
   "type": "S3Key",
   "verdict": "CONFORMANT",
   "canonical_form": "advi/49financial/platinum/advisors/advisor_id=A123/positions.json",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "advi/49financial/platinum/advisors/advisor_id=A123/positions.json",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "advi/49financial/platinum/firm/fee_efficiency.json",
   "type": "S3Key",
   "verdict": "CONFORMANT",
   "canonical_form": "advi/49financial/platinum/firm/fee_efficiency.json",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "advi/49financial/platinum/firm/fee_efficiency.json",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "advi/49financial/platinum/firm/top_holdings.json",
   "type": "S3Key",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "advi/49financial/platinum/firm/top-holdings.json",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "advi/49financial/platinum/firm/top-holdings.json",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "blackdiamond/49f/credentials",
   "type": "SECRET",
   "verdict": "CONFORMANT",
   "canonical_form": "blackdiamond/49f/credentials",
   "verdict_at_round_9": "CONFORMANT",
   "canonical_form_at_round_9": "blackdiamond/49f/credentials",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "inf/otp-relay/token",
   "type": "SECRET",
   "verdict": "OUT-OF-PATTERN",
   "canonical_form": "{system}/inf/otp-relay/token",
   "verdict_at_round_9": "OUT-OF-PATTERN",
   "canonical_form_at_round_9": "{system}/inf/otp-relay/token",
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  },
  {
   "name": "4ba4753c-98f4-47c0-9a47-6dacaa1b6370",
   "type": "KMS_KEY",
   "verdict": "NOT-GRADED",
   "canonical_form": null,
   "verdict_at_round_9": "NOT-GRADED",
   "canonical_form_at_round_9": null,
   "basis": "UNCHANGED-AGREEING",
   "evidence": "agreed at round 9; the re-measure does not move it"
  }
 ]
}
```
