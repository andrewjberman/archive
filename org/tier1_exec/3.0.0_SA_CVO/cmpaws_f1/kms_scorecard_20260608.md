# CMPAWS KMS Full F1 Scorecard — node CERTIFIED; edge layer blocked on KMS-SCHEMA-1

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-08 ~16:42Z · **Compiler:** comp-aws @ db2122239 (CVO ran)
**Method:** existence vs live; provenance vs state-union; key-policy §1.5; ENCRYPTS_WITH/GRANTS edges.

## VERDICT: NODE-CERTIFIED (2/2, 1.00); EDGE layer = NOT-YET-CERTIFIED pending KMS-SCHEMA-1 (CTO).

| Axis | Result |
|---|---|
| Node existence | 1.00 — 2 customer-managed KMS_KEY = live 2 (find-insure-data-key, inf-ebs-key) |
| Typing | 1.00 — 0 untyped |
| Provenance | 1.00 — both DECLARED (TF-managed), 0 false-shadow |
| Properties | rotation_enabled True/True ✓; key_policy_statements present (1 / 2 stmts, §1.5 full-set) ✓ |
| Edges (ENCRYPTS_WITH) | **BLOCKED — KMS-SCHEMA-1 (below)** |

## KMS-SCHEMA-1 (CVO finding → CTO schema-amendment + AE compiler; a real node-completeness gap)
**27 of 29 ENCRYPTS_WITH edges target an AWS-MANAGED key that has no KMS_KEY node → 27 dangling edges.**
- The target `86cc6c40-2387-4446-b7e1-de79392e06b3` = **AWS-managed** (KeyManager=AWS, alias/aws/dynamodb,
  "Default key that protects DynamoDB"). 27 resources (DynamoDB tables + portal S3 buckets) ENCRYPTS_WITH it.
- The compiler scopes KMS_KEY nodes to the 2 CUSTOMER-managed keys (correct for "what WE manage"), but still
  emits ENCRYPTS_WITH edges to the AWS-managed default key → those edges point to a non-existent node.
- The §1.3 drift vocabulary has DECLARED / LIVE-no-DECLARED / DECLARED-no-LIVE — but **no `AWS_MANAGED` slot**.
  An AWS-managed key is neither TF-declared nor our-unmanaged-orphan; it's AWS's. So it can't be typed under
  the current vocabulary without forcing a wrong class.
- **This is the §4 0-untyped / no-dangling-edge bar biting:** an edge to an untyped/absent node is the same
  cert-fail class as an untyped node. So KMS cannot full-certify (edge layer) until resolved.

**CVO recommendation (CTO's call):** add an `AWS_MANAGED` provenance/drift value (§1.3) + admit AWS-managed
keys as KMS_KEY nodes (provenance=AWS_MANAGED, tf_managed=false, rotation AWS-controlled) so ENCRYPTS_WITH
edges resolve to a real node. This generalizes beyond KMS — every class can reference an AWS-managed/service
resource (default SQS/SNS/S3 SSE keys, AWS-managed IAM policies); an AWS_MANAGED provenance is the clean,
reusable answer (same "vocabulary-add > untyped/dangling" principle as EV-SCHEMA-GAP-1). Routed to CTO.

## Disposition
KMS node layer CERTIFIED (2/2, 1.00). Full KMS cert (incl the ENCRYPTS_WITH edge layer + the GRANTS/CreateGrant
edges, the ORIAPI class) holds pending the CTO KMS-SCHEMA-1 ruling. This finding is HIGH-VALUE: it's a
cross-class one (AWS-managed-resource references) that the edge layer surfaced — exactly what per-class edge
cert is for. Continuing to secrets/dynamodb while CTO rules.

— 3.0.0_SA_CVO
