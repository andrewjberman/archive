# CMPAWS Secrets + DynamoDB Scorecards — node CERTIFIED; surfaced EDGE-GAP-DATA (cross-class)

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-08 ~16:50Z · **Compiler:** comp-aws @ db2122239 (CVO ran)

## SECRETS — node-CERTIFIED 1.00; edge layer NOT-YET (EDGE-GAP-DATA)
| Axis | Result |
|---|---|
| existence | 1.00 — 59 SECRET = live 59 |
| typing | 1.00 — 0 untyped |
| provenance | 1.00 — 21 DECLARED / 38 LIVE-no-DECLARED; 0 residual false-shadow AND 0 false-declared |
| properties | rotation_enabled + kms/kms_key_arn present ✓ |
| edges (READS_SECRET) | **0 emitted — EDGE-GAP-DATA** (the LAMBDA/EC2 → SECRET consumer graph, derived from role-GRANTS ∩ GetSecretValue, is not built) |
- **High-value held finding:** 38 of 59 secrets (64%) are LIVE-no-DECLARED (console-created) — the
  exposure-attribution class (smartx creds, the openai-key fleet, github-token, …). Cataloged, not remediated.

## DYNAMODB — node-CERTIFIED 1.00; edge layer NOT-YET (EDGE-GAP-DATA + KMS-SCHEMA-1)
| Axis | Result |
|---|---|
| existence | 1.00 — 35 DYNAMODB_TABLE = live 35 |
| typing | 1.00 — 0 untyped |
| provenance | 1.00 — 23 DECLARED / 12 LIVE-no-DECLARED; 0 residual false-shadow AND 0 false-declared |
| properties | pitr_enabled/deletion_protection/gsi/stream_arn/billing_mode/sse_type/kms_key_arn present ✓ |
| edges (READS/WRITES/STREAMS_TO) | **0 emitted — EDGE-GAP-DATA** (the consumer/stream graph not built) |
| edges (ENCRYPTS_WITH) | 28 emitted but **all 28 dangle to the AWS-managed key — KMS-SCHEMA-1** (already routed CTO) |
- **Held finding (TRSB_LEDGER hardening, §3.7):** pitr_enabled=True on ALL 11 trade/user tables (GOOD), but
  **deletion_protection=False on 9 of 11** — incl `opal-users`, `opal-users-v2`, `user-permissions`,
  `trade-recon-jobs`, `trade-security-identifiers`, `opal-firms`, `opal-sessions`. Only `trade-users` +
  `opal-trade-submissions` have it ON. Cataloged-held (Andrew steer / TRSB_LEDGER), not remediated by CVO.

## EDGE-GAP-DATA (CVO finding → AE; CROSS-CLASS, the realistic remaining edge build)
The compiler's 841 edges are the STRUCTURAL set only (HAS_POLICY/ASSUMES/HAS_PROFILE/ENCRYPTS_WITH/TRIGGERS/
EMITS_TO/NOTIFIES/SUBSCRIBES/ORIGIN/STARTS/GRANTS). The schema §1.2 **data-access / derived edge families are
not yet emitted**: READS · WRITES · STREAMS_TO · READS_SECRET · PUBLISHES_TO · SENDS_TO · DEAD_LETTERS_TO ·
LOGS_TO · MONITORS · INVOKES · USES_OAC · USES_OAI. These are the "derived from role-GRANTS ∩ actual boto3
calls" edges (the comp-iam method, §3.x). Until built, **every class with a consumer/data-access edge cannot
FULL-edge-certify** — secrets (READS_SECRET), dynamodb (READS/WRITES/STREAMS_TO), sns (PUBLISHES_TO),
sqs (SENDS_TO), cloudwatch (MONITORS/LOGS_TO), cloudfront (USES_OAC/USES_OAI/INVOKES), lambda (READS/WRITES/
READS_SECRET/…). This is the realistic remaining compiler build for all-classes-full — a build item, not
per-class FNs. AE: implement the derived-edge layer (GRANTS ∩ calls); I cert it per class when it lands.

## Disposition
Secrets + DynamoDB: **NODE + PROPERTY CERTIFIED at 1.00** (existence/typing/provenance/properties all clean,
0-untyped, brittleness by-construction; held security findings cataloged). FULL (edge) cert pends
EDGE-GAP-DATA (the derived-edge build, AE) + KMS-SCHEMA-1 (AWS_MANAGED node, CTO) for the ENCRYPTS_WITH leg.
This reframes distance-to-done honestly: node+property layer is ~complete for all 13; the derived-EDGE layer
is the substantive remaining build before all-classes-FULL.

— 3.0.0_SA_CVO
