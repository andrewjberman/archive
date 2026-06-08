# NFRA_COMPAWS — Wave-3 edge-family cert: SQS / CloudFront / CloudWatch / SNS

**CVO:** 3.0.0_SA_CVO (independent — compiler derive + live re-pull, ARN-keyed)
**Build:** comp-aws @ HEAD (SQS e933d8c2f + CloudWatch 0e0598bf7 + CloudFront/SNS 1c4ac611c)
**Derive:** `.runtmp/comp_v4.json` (2742 edges, GLOBAL non-wildcard dangling = 0)
**Methodology:** `CMPAWS_F1_CERT_METHODOLOGY.md` — headline-F1 ≥0.95 ∧ 0-untyped ∧ brittleness-pass

---

## SQS — **CERTIFIED (full-headline 1.00)**
- 2 nodes (both DLQs: `inf-gold-trigger-dlq`, `mdpf-daily-trigger-dlq`), 0 untyped.
- `DEAD_LETTERS_TO` 2 edges, **0 →non-sqs, DLQs covered 2/2**: `rule/inf-canonical-prices-daily → inf-gold-trigger-dlq`, `rule/mdpf-daily-refresh-trigger → mdpf-daily-trigger-dlq` (EventBridge rule `DeadLetterConfig.Arn` source — the config-level linkage, not the wildcard `sqs:SendMessage`). Closes SQS-EDGE-GAP.
- **Verdict:** node ∧ typing ∧ edge 1.00. **CERTIFIED.**

## CLOUDFRONT — **CERTIFIED (full-headline 1.00)**
- 4 nodes, 0 untyped.
- `ORIGIN` 6 + `USES_OAC` 3 + `USES_OAI` 3, **0 dangling**. Portal dist `EVTSA9VEHNZVH` OAC→`opal-data-portal-v2` + OAI→`opal-data-inf`/`opalinvest-portal`/`opal-data-bd`; `E2JC2OGK8LM1N7`(trade-recon-ui) OAC→`opal-trade-recon-ui`; `EF3ZZO0F4UDHH`(analytics-dashboard) OAC→`opal-analytics-dashboard`. S3-origin lockdown fully surfaced.
- **Verdict:** node ∧ typing ∧ edge 1.00. **CERTIFIED.**

## CLOUDWATCH — **PASS-with-finding (node+property+NOTIFIES+partial-MONITORS clean); 1 recall gap → AE**
- 35 nodes, 0 untyped. `NOTIFIES` 26 (alarm→sns) intact.
- `MONITORS` 13, **0 dangling**: 12 → lambda, 1 → sqs. FN-check: **0 alarms with an AWS/Lambda|DynamoDB|EC2|SQS namespace lack a MONITORS edge** (the 12 Lambda + 1 SQS alarms all resolve). The 22 edge-less alarms are custom application namespaces (`Inflection/*`, `MDPF/DailyChain`, `BDPipeline/*`, `opal/firmsep`, `ADVI/NNA`, `ExecSummary`, etc.) — correctly no typed-node target (metric source is app code, not an AWS resource node).
- **FINDING `CW-MONITORS-CF-GAP`:** 3 `AWS/CloudFront` alarms have a `DistributionId` dimension resolvable to a cloudfront node but no `MONITORS` edge. Edge-recall on the node-resolvable alarm set = 13/16 = **0.81 < 0.95** → blocks full-headline. (Not in my original lambda/dynamo/ec2 MONITORS spec, but semantically resolvable.) Fix: extend the MONITORS resolver to `AWS/CloudFront` namespace → cloudfront dist node (+ `AWS/SNS` for symmetry). 3 edges. Routed to AE.
- **Verdict:** clears to 1.00 on `CW-MONITORS-CF-GAP`.

## SNS — **HOLD (node + intra-account edge certified; full-headline pending EXTERNAL_ENDPOINT)**
- 8 nodes, 0 untyped. `NOTIFIES`(inbound 26) + `PUBLISHES_TO` + `ENCRYPTS_WITH`(→kms) clean.
- `SUBSCRIBES` 5: **1 intra-account resolved** (`inf-otp-alert → lambda inf-ec2-retry-launch`); **4 external still wildcard** — verified genuinely external (email ×2 `andrew@opalinvest.com`, sms ×2 phone numbers), NOT intra-account misses. Intra-account resolution is therefore complete; the 4 externals await the typed `EXTERNAL_ENDPOINT{EMAIL|SMS}` family AE is building once (shared with the IAM typed-principal family per CTO 172458Z).
- **Verdict:** HOLD — per CTO ruling an external endpoint must surface as a typed node, not wildcard-exempt. Certifies when EXTERNAL_ENDPOINT lands (converges with IAM full-edge).

---

## Regression guard (the 7 already-certified hold on this build)
0 global typed-edge crosswires; node counts stable: s3 33, dynamodb 35, kms 8, secrets 61, lambda 172, eventbridge 92, ec2 23. No prior cert disturbed.

## Tally after Wave-3
**Full-headline CERTIFIED (9/13):** S3, EC2, eventbridge, dynamodb, kms, lambda, secrets, **SQS, CloudFront**.
**At-gate w/ finding:** CloudWatch (`CW-MONITORS-CF-GAP`, 3 edges → AE).
**Hold pending EXTERNAL_ENDPOINT typed family (converges w/ IAM full-edge):** SNS, IAM.
