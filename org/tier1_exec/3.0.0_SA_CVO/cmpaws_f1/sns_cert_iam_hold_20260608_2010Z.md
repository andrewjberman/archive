# NFRA_COMPAWS — SNS cert (12/13) + IAM HOLD (IAM-PUBLIC-DENY-FP)

**CVO:** 3.0.0_SA_CVO (independent — compiler + independent live bucket-policy census)
**Build:** comp-aws @ da660a835 + 2a205f24a (IAM_PRINCIPAL typed family) | **Derive:** `.runtmp/comp_v8.json` (2788 edges, 0 dangling)

## SNS — **CERTIFIED full-headline 1.00** → 12/13
- 8 nodes, 0 untyped. `SUBSCRIBES` 5, **0 wildcard, 0 dangling** — all typed: `external-endpoint::email::andrew@opalinvest.com` (×2 subs), `external-endpoint::sms::+1786…`, `external-endpoint::sms::+1305…`, and intra-account `inf-otp-alert → lambda inf-ec2-retry`. The EXTERNAL_ENDPOINT family resolves the email/sms endpoints; CTO's no-wildcard-external line met. NOTIFIES/PUBLISHES_TO/ENCRYPTS_WITH intact.
- **Verdict:** node ∧ typing ∧ edge 1.00. **CERTIFIED.**

## IAM — **HOLD (IAM-PUBLIC-DENY-FP)** — NOT 13/13
Most of the IAM typed-principal family is correct:
- `GRANTS` 13, **0 wildcard** (CTO's hard line met — interim wildcard ripped out). `SERVICE_PRINCIPAL` 4 (cloudfront/cloudtrail + 2 CloudFront OAI → AWS_MANAGED, correctly NOT a finding). `IAM_USER` 0. `MULTI_STATE_MANAGED` folded correctly (opal-users-v2 → drift=MULTI_STATE_MANAGED, modules=[portal-auth, shared-infra]). Global 0-dangling.

**FINDING `IAM-PUBLIC-DENY-FP` (precision, security-critical) → AE:** the lone `EXTERNAL_PRINCIPAL{PUBLIC}` node + `finding{PUBLIC_GRANT, surfaced:true}` is a **FALSE POSITIVE**. Independent live census of ALL bucket policies: **0 real public grants (Allow + Principal:\*)**; the only `Principal:*` statements are **2 Deny guardrails** on `opal-data-schwab` (`DenyInsecureTransport`, `DenyUnencryptedObjectUploads` — standard TLS/encryption hardening). The compiler's own GRANTS edge proves it: `opal-data-schwab#policy → public | effect="Deny" | finding_class="PUBLIC_GRANT"` — it records `effect=Deny` but fires PUBLIC_GRANT anyway. A `Deny + Principal:*` is a guardrail (a *positive* security signal), never a public exposure.

**Why this blocks full-headline:** the typed-principal family's headline purpose (CTO 172458Z) is "a PUBLIC/cross-account grant must surface." Surfacing a Deny guardrail as PUBLIC_GRANT is a false alarm on the exact feature being certified — and dangerous (a reviewer could "remediate" the FP by weakening a guardrail). Precision on the PUBLIC finding = 0/1.

**Fix (1 line, compiler already has the data):** gate `EXTERNAL_PRINCIPAL{PUBLIC}` node + `PUBLIC_GRANT` finding on `effect == "Allow"`. A Deny+Principal:* should not produce a public-principal node/finding (optionally type as DENY_GUARDRAIL, but simplest: don't emit). With 0 real Allow public grants account-wide, the corrected family emits **0** PUBLIC findings — the true state.

## Tally → **12/13 full-headline** (SNS certified; IAM held)
S3, EC2, eventbridge, dynamodb, kms, lambda, secrets, SQS, CloudFront, CloudWatch, StepFunctions, **SNS**. IAM clears to 13/13 on the 1-line `IAM-PUBLIC-DENY-FP` effect-gate fix.

## Note: dynamodb opal-users-v2 drift refinement
The MULTI_STATE_MANAGED fold changed opal-users-v2's dynamodb drift_class DECLARED→MULTI_STATE_MANAGED. This is **strictly more correct** (the table IS dual-managed) — a provenance refinement, not a regression. DynamoDB cert HOLDS (existence/typing/edges unchanged; drift_class is now more accurate). No re-touch needed.

## 4th independent-cert catch this session
EDGE-CROSSWIRE-1 (2-edge type-violation) → cot 4-class residuals → SFN-INVOKES-NESTED-GAP (recall 0.35 behind self-F1=1.0) → **IAM-PUBLIC-DENY-FP (false public-exposure alarm)**. Each invisible to the builder's self-check; each caught by independent live measurement. The gate at design spec.
