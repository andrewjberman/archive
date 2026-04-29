<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.1-bucket</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29: opal-data-inf bucket exists, fully TF-managed in inf-pipeline/s3.tf, layout mirrors opal-data-bd. Closed during AE TO sweep. -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Create `opal-data-inf` S3 bucket with bucketing layout that mirrors `opal-data-bd` exactly (`code/gold/`, `silver/`, `gold/canonical/`, `gold/timeseries/`, `gold/artifacts/`, `platinum/firm/`, `platinum/advisors/{advisorId}/`, `bronze/orion/`, `otp/`). This is the single authoritative S3 home for all Inflection partner data. Per PRD §4.1 the serving layer is already multi-tenant by firmId — adding this bucket + the FIRM#inflection DynamoDB row (W1.3) + Lambda@Edge mapping (W1.6/W1.7) is the entire Inflection storage provisioning.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.1 (row 1) + §5.2 ingestion flow. Bucket is written to by `inf-exporter` (W2.4) + DS silver converter + gold runner; read by `opal-partners-data` Lambda (already multi-tenant by firmId). Bucket layout mirrors `opal-data-bd` because Inflection pipeline pattern mirrors BD pipeline pattern at the artifact-path level — DS gold scripts write `gold/canonical/`, `platinum/firm/`, `platinum/advisors/{id}/` under the same keys Inflection and 49F/BD share.

    Additional key that is NEW vs `opal-data-bd`: `otp/current.txt` — ephemeral OTP relay path for `inf-exporter` (see PRD §6.3). Scope IAM accordingly — only `inf-exporter` role writes/reads `otp/`, and Andrew gets an explicit scoped credential (or uses the SNS topic + relay form — to be decided in W2.5).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>aws s3 ls opal-data-bd/ --summarize</run>
    <expect>Top-level folders: bronze/, silver/, gold/, platinum/, code/, lambda-layers/. Confirm prefix list.</expect>
    <if_mismatch>Unexpected new top-level prefix on BD means bucketing has drifted; match it in opal-data-inf or flag to COO before proceeding.</if_mismatch>

    <run>Read infra/aws/terraform/bd-pipeline/s3.tf</run>
    <expect>Module pattern, lifecycle policy, CORS config, public-access-block, versioning, encryption. Mirror all.</expect>

    Phase 2 (during implementation):
    <run>terraform plan (from inf-pipeline workspace — depends on W1.2)</run>
    <expect>Exactly 1 S3 bucket + dependent resources (public-access-block, versioning, encryption, CORS if applicable) — no drift on other resources.</expect>

    Phase 3 (after apply):
    <run>aws s3 ls opal-data-inf/</run>
    <expect>Empty bucket (no objects yet) + all top-level folders created via empty placeholder objects (or omit placeholders — decision AE's, document in session log).</expect>

    <run>aws s3api get-public-access-block --bucket opal-data-inf</run>
    <expect>All four block settings = true (matches opal-data-bd hardening).</expect>

    <run>comp-iam gaps</run>
    <expect>No new gaps introduced by the new bucket's IAM policies.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: shared-infra Terraform state key `shared-infra/tfstate` — bucket is created under inf-pipeline workspace but any shared-infra IAM policy touching bucket inventory must be coordinated.
    also_in_to: W1.2 (inf-pipeline workspace creation — this TO depends on W1.2 being done first).
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "W1.1 executes INSIDE W1.2's workspace. Complete W1.2 scaffold first, then this TO creates the bucket as the workspace's first live resource. No other concurrent TO touches this bucket."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Bucket `opal-data-inf` exists and is accessible only to IAM principals in account 313476888478 (public-access-block all true).
    2. Bucket layout mirrors `opal-data-bd` — same top-level prefix set plus `otp/`.
    3. Terraform state key `inf-pipeline/tfstate` contains the bucket as a tracked resource.
    4. Encryption enabled (SSE-S3 or SSE-KMS — match BD).
    5. Versioning enabled (match BD).
    6. CORS config (if present on BD) mirrored.
    7. `comp-iam gaps` shows no new permission gaps after iam.tf change.
    8. EC2_MANIFEST.json updated if this bucket is referenced by an EC2 service (coordinate with W1.9).
    9. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_inflec_w1_1_bucket.md` with terraform plan/apply output, compiler runs, and tag annotation.
    10. Tag `inf-pipeline-v1.0.0` (or next increment if W1.2 tagged first) pushed with `--follow-tags`.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/inf-pipeline/s3.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/iam.tf (partial — only bucket-scoped policies)</file>
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json (coordinate with W1.9 — may be batched)</file>
      <file action="reference">infra/aws/terraform/bd-pipeline/s3.tf (template)</file>
      <file action="reference">docs/architecture/ADVI_INFLEC.md §4.1 §5.2</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Mirror `opal-data-bd` bucketing layout exactly — top-level prefixes + hardening settings (encryption, versioning, public-access-block).</requirement>
    <requirement id="2">Add `otp/` top-level prefix — NEW vs BD. IAM scope on `otp/*` is `inf-exporter` only (write/read) + an Andrew-delivered OTP path (see W2.5 for relay decision).</requirement>
    <requirement id="3">No cross-bucket IAM — `inf-gold-*` roles get access to `opal-data-inf` only, never `opal-data-bd`. Multi-tenant isolation is structural.</requirement>
    <requirement id="4">Terraform-managed. NO `aws s3api create-bucket` CLI. Creation must be in `inf-pipeline/s3.tf`.</requirement>
    <requirement id="5">Follow CLAUDE.md Rule 2 (commit before apply) + Rule 6 (tag after deploy).</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">`infra/aws/terraform/inf-pipeline/{s3.tf,iam.tf}` with bucket + scoped IAM. Author 0.7.0_AE_CloudOps.</deliverable>
    <deliverable type="tag">`inf-pipeline-v1.0.0` (or next increment) annotated tag with `--follow-tags`.</deliverable>
    <deliverable type="document">Session log with terraform plan/apply output, compiler runs.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT create the bucket via CLI. Terraform-only.</rule>
    <rule>Do NOT skip public-access-block. Block all four settings.</rule>
    <rule>Do NOT grant cross-bucket access to `opal-data-bd` from any inf-* IAM role.</rule>
    <rule>Do NOT start before W1.2 scaffold merged.</rule>
  </do_not>
</task_order>
