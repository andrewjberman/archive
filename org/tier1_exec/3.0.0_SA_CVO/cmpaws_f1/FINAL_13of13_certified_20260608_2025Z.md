# NFRA_COMPAWS — **13/13 CERTIFIED** (sovereign done-gate COMPLETE)

**CVO:** 3.0.0_SA_CVO (independent — compiler + live re-pull + state-union, CVO-measured throughout; never builder self-score)
**Final build:** comp-aws @ 1a073937f | **Derive:** `.runtmp/comp_v9.json` (2787 edges, 0 dangling, 0 crosswire)
**Methodology:** `CMPAWS_F1_CERT_METHODOLOGY.md` — headline-F1 ≥0.95 ∧ 0-untyped ∧ brittleness-pass ∧ CVO-independent

## IAM — **CERTIFIED full-headline 1.00** (13th class; IAM-PUBLIC-DENY-FP closed)
- `GRANTS` 12, **effect=Allow-only, 0 wildcard** (the schwab Deny+Principal:* edge correctly no longer emits a GRANTS edge — a Deny is not a grant). `SERVICE_PRINCIPAL` 4 (AWS_MANAGED), `EXTERNAL_ENDPOINT` 3, `IAM_USER` 0, `EXTERNAL_PRINCIPAL{PUBLIC}` **0** — matches independent live census (0 real Allow public grants account-wide). `PUBLIC_GRANT` findings 0 = true state. `MULTI_STATE_MANAGED` folded (opal-users-v2). HAS_POLICY/HAS_PROFILE/ASSUMES + typed-principal all resolve, 0 dangling.
- **Verdict:** node ∧ typing ∧ provenance(incl AWS_MANAGED/MULTI_STATE_MANAGED) ∧ edges(incl typed-principal, 0-wildcard, 0-FP) all clean. **CERTIFIED.**

## All 13 classes — full-headline CERTIFIED
S3 · EC2 · eventbridge · dynamodb · kms · lambda · secrets · SQS · CloudFront · CloudWatch · StepFunctions · SNS · **IAM**.

Final regression guard (1a073937f): 2787 edges, **0 global dangling, 0 typed-edge crosswires**; node counts s3 33 / iam 114 / dynamodb 35 / kms 8 / secrets 61 / lambda 172 / sns 8 / sqs 2 / cloudfront 4 / cloudwatch 35 / eventbridge 94 / ec2 24 / stepfunctions 1 (live-tracked).

## The gate earned its keep — 4 independent-cert catches, each builder-invisible
1. **EDGE-CROSSWIRE-1** — 2-edge type-violation (READS_SECRET→s3) the 0-dangling check was structurally blind to.
2. **cot 4-class residuals** — in-file metadata / design-doc refs / desc prose / rejected-name-in-narrative, all reported "0-residual" by three lane self-checks.
3. **SFN-INVOKES-NESTED-GAP** — INVOKES recall 9/26 = 0.35 behind a self-reported F1=1.0000 (self-score never scored edges).
4. **IAM-PUBLIC-DENY-FP** — false PUBLIC_GRANT alarm on a Deny guardrail (most security-consequential; a reviewer could weaken a guardrail to "fix" it).

Each was invisible to the builder's own score; each surfaced by independent live measurement. **"AE builds, CVO measures, never AE self-grading" — validated end to end.**

## LD-0167: CLOSED
Sovereign done-gate met: all 13 NFRA_COMPAWS classes CVO-independently certified ≥0.95 headline-F1 (all effectively 1.00), 0-untyped, brittleness-stable, 0-dangling. AE executes the LD-0167 step: snapshot-archive the certified-complete graph as baseline.
