# NFRA_COMPAWS — CloudWatch full-edge re-cert (CW-MONITORS-CF-GAP closed)

**CVO:** 3.0.0_SA_CVO (independent) | **Build:** comp-aws @ e5d34a40c | **Derive:** `.runtmp/comp_v5.json` (2745 edges, 0 dangling)

## CLOUDWATCH — **CERTIFIED (full-headline 1.00)**
- 35 nodes, 0 untyped.
- `NOTIFIES` 26 (alarm→sns) intact.
- `MONITORS` **16, 0 dangling**: 12 → lambda, 3 → cloudfront (the CW-MONITORS-CF-GAP fix: AWS/CloudFront DistributionId-dim → dist node), 1 → sqs. **FN-check: 0 typed-namespace alarms (AWS/Lambda|DynamoDB|EC2|SQS|SNS|CloudFront) lack a MONITORS edge** → edge-recall 16/16 = 1.00 (was 13/16 = 0.81). The 19 edge-less alarms are all custom application namespaces (`Inflection/*`, `MDPF`, `BDPipeline`, `opal/firmsep`, `ADVI/NNA`, `ExecSummary`, ...) — correct absence (metric source is app code, not an AWS resource node).
- **Verdict:** node ∧ typing ∧ NOTIFIES ∧ MONITORS all 1.00. **CERTIFIED.** Closes `CW-MONITORS-CF-GAP`.

## Regression guard
0 global dangling, 0 typed-edge crosswires; SQS DEAD_LETTERS_TO 2, CloudFront USES_OAC/OAI 6 intact. No prior cert disturbed.

## Tally: **10/13 full-headline**
S3, EC2, eventbridge, dynamodb, kms, lambda, secrets, SQS, CloudFront, **CloudWatch**.
**Remaining:** SNS + IAM (clear together on EXTERNAL_ENDPOINT typed family); StepFunctions (13th class, not yet built). IAM cert also folds MULTI_STATE_MANAGED drift class (schema v0.4 §1.3, a4c88a949).
