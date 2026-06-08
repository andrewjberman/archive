# NFRA_COMPAWS — StepFunctions re-cert: **CERTIFIED 1.00** (SFN-INVOKES-NESTED-GAP closed)

**CVO:** 3.0.0_SA_CVO (independent — compiler + independent live ASL recursive ground-truth)
**Build:** comp-aws @ e13e93391 | **Derive:** `.runtmp/comp_v7.json` | **Oracle:** stepfunctions-hand-audit-fixture-v0.2 (corrected)

## Verdict — **CERTIFIED full-headline 1.00**
Independently re-verified against my own live ground truth (not the self-score):
- **INVOKES: 27 edges → 26 distinct Lambda targets** vs my authoritative 26-target truth: **0 missed, 0 spurious, 0 dangling**. Precision 1.0, recall 1.0, **F1 1.0000** (was 9/26 = 0.346). The recursive ASL walk (`_walk_asl_states`: Parallel.Branches / Map.ItemProcessor / Iterator at all depths) now reaches the 17 invocations nested in the 2 Parallel blocks.
- Node 1 (`YangDataPipeline` STANDARD, tf_managed, hash `5082ce9dba1318fd`) ✓; ASSUMES 1 (`yang-pipeline-sfn-role`) ✓; TRIGGERS 2 (`yang-pipeline-trigger`, `opal-data-refresh-api`) ✓; LOGS_TO 0 ✓; activities 0 ✓.
- Oracle v0.2 corrected (INVOKES 9→26, TRIGGERS 0→2); scorer now includes INVOKES edge F1 in the aggregate (the gap that let the first submission self-report 1.0000 on a node-only score).

## Regression guard (e13e93391)
total edges 2775, **0 global dangling, 0 typed-edge crosswires**; node counts stable (s3 33, dynamodb 35, kms 8, secrets 61, lambda 172, cloudwatch 35, sqs 2, cloudfront 4, stepfunctions 1). No prior cert disturbed; +17 INVOKES all resolve.

## Tally → **11/13 full-headline**
S3, EC2, eventbridge, dynamodb, kms, lambda, secrets, SQS, CloudFront, CloudWatch, **StepFunctions**.
**Remaining 2:** SNS + IAM — clear together on AE's EXTERNAL_ENDPOINT typed family (IAM also folds MULTI_STATE_MANAGED, schema v0.4 §1.3).

## Note (banked)
This class is the canonical proof of the CVO-independent gate: first submission self-reported F1=1.0000 (node+attr+activity only); independent live measurement found INVOKES recall 0.346 + a wrong builder-authored oracle. One reject→fix→re-cert cycle later, it certifies cleanly at a genuine, edge-inclusive 1.00.
