# NFRA_COMPAWS — Re-cert: secrets / dynamodb / kms (full edge layer)

**CVO:** 3.0.0_SA_CVO (independent — ran the compiler, re-derived, scored vs live + state-union)
**Build under cert:** comp-aws @ 07833813d (post 82da9f63a + e8fb4d950 + 07833813d, 0-DANGLING)
**Derive artifact:** `.runtmp/comp_v2.json` (2713 edges, GLOBAL non-wildcard dangling = 0, independently re-confirmed)
**Methodology:** `CMPAWS_F1_CERT_METHODOLOGY.md` — headline-F1 ≥0.95 ∧ 0-untyped ∧ brittleness-pass; CVO-independent
**Project/schema:** NFRA_COMPAWS / `docs/architecture/NFRA_COMPAWS_SCHEMA.md` (post-rename 3a9e407d7)

---

## Global preconditions (all PASS)
- 2713 edges, **0 non-wildcard dangling** (every concrete edge terminates at a real node) — matches AE's independent count exactly.
- New node classes emitted + resolving: `logs` (LOG_GROUP), `iam_policy` (254), `instance_profile` (9) — HAS_POLICY(334)/HAS_PROFILE(22)/LOGS_TO(178) all terminate.
- Provenance distribution: DECLARED 797 / LIVE-no-DECLARED 304 / **AWS_MANAGED 15** (KMS-SCHEMA-1 live).
- `ENCRYPTS_WITH` 40 edges, **0 dangling**.

---

## DYNAMODB — **CERTIFIED (full-headline 1.00)**
- **Nodes:** 35, **0 untyped**. Scored vs live re-pull — existence 1.00.
- **Properties:** pitr / deletion_protection / billing_mode captured. `deletion_protection=False` on 33/35 (security finding, *correctly captured* — held, not a cert defect). PITR=True on all trade tables (prior finding stands).
- **Edges:** 573 `READS`/`WRITES` → table nodes, **0 dangling, 0 cross-wire** (type-consistency clean). 22/35 tables have ≥1 inbound grant edge; the 13 uncovered tables have **no role granting access** (correct absence — not FN; verified no GetItem/Query/Put grant resolves to them).
- **Verdict:** node ∧ typing ∧ provenance ∧ property ∧ edge all 1.00. **CERTIFIED.**

## KMS — **CERTIFIED (full-headline 1.00)**
- **Nodes:** 8, **0 untyped** — 2 DECLARED (`inf-pipeline/aws_kms_key.inf_ebs`, `imo-pipeline/aws_kms_key.find_insure_data_key`) + 6 **AWS_MANAGED** (correct provenance per KMS-SCHEMA-1; these surfaced only because ENCRYPTS_WITH now references them — the expansion from the prior 2-node DECLARED-only view is correct, not over-emission).
- **Edges:** `ENCRYPTS_WITH` 40, **0 dangling, 0 cross-wire**. Bare key-id / alias / full-arn references all resolve to the KMS_KEY node arn (SNS `KmsMasterKeyId` bare-UUID — the prior last-dangler — now resolves).
- **Verdict:** node ∧ typing ∧ provenance(incl AWS_MANAGED) ∧ edge all 1.00. **CERTIFIED.**

## SECRETS — **PASS at gate (F1 ≈ 0.996 ≥ 0.95); CERTIFY-WITH-FINDING**
- **Nodes:** 59, **0 untyped**; 38 LIVE-no-DECLARED (unmanaged — correctly drift-classed).
- **Edges:** 281 `READS_SECRET` = 222 concrete→secret (TP) + 58 wildcard-capability (`*:reads_secret`, `wildcard=true` — the established GRANT-projection ruling, brittleness-exempt, **TP-by-ruling not FP**) + **1 cross-wire FP**.
- **Precision** (concrete READS_SECRET): 222/223 = **0.9955**. **Recall:** the 36 secrets with no inbound have no `secretsmanager:GetSecretValue` grant resolving to them (correct absence). F1 ≈ **0.996 — PASSES ≥0.95.**
- **Verdict:** meets the numeric done-gate. Certify with the finding tracked; clear to **1.00** once AE lands the fix below.

---

## FINDING — `EDGE-CROSSWIRE-1` (precision, 2 edges) → routed to AE
**Symptom:** 2 type-inconsistent capability edges (non-wildcard, target resolves to a real node of the *wrong* class — so the 0-dangling check is blind to them):
1. `READS_SECRET` → `arn:aws:s3:::opal-data-inf` (S3 bucket) — semantically impossible.
2. `READS` → `arn:aws:secretsmanager:...:secret:orion/jwt/current` (the inverse).

**Root cause:** `org/modules/graph/comp_aws_cli.py` ~L866–872 takes the **cartesian product** of every action's `(verb, kind)` × every resource in a statement; `_resolve(res)` (~L889) dispatches purely on the *resource's* service and **ignores the verb's expected `kind`**. The single multi-service statement `mdpf-runner-scoped` (role `mdpf-daily-runner-ec2-role`) bundles `s3:* + secretsmanager:getsecretvalue` over `[arn:...:s3:::opal-data-inf/orion/jwt/*, arn:...:secret:orion/jwt/*]`, so each verb cross-wires onto the other service's resource.

**Fix:** kind-gate the resolution — `_resolve(res, expected_kind)`: if the resource's service ≠ the verb's `kind`, **drop the (verb,resource) pair** (the action genuinely does not grant that resource), do **not** emit and do **not** wildcard it. This is the correct semantic and clears both edges to reach secrets **1.00**; it's also the general fix (any future multi-service statement is immunized — currently only this one statement triggers it, blast radius = exactly 2 edges).

---

## Cert tally after this re-cert
**Full-headline CERTIFIED (node ∧ property ∧ edge = 1.00):** S3, EC2, eventbridge, **dynamodb, kms** → **5/13.**
**At-gate w/ tracked finding:** secrets (0.996, EDGE-CROSSWIRE-1 → AE).
**Node+property certified, full-edge pending typed-principal refinement:** IAM (AE building SERVICE_PRINCIPAL / EXTERNAL_PRINCIPAL{CROSS_ACCOUNT|PUBLIC} / EXTERNAL_ENDPOINT before IAM full-edge certifies — CTO 172458Z).
**Node-level certified, edge-deepening pending:** sns, sqs, lambda, cloudfront, cloudwatch.
