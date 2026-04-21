<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.2-tf-workspace</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Scaffold the `infra/aws/terraform/inf-pipeline/` Terraform workspace by mirroring the `bd-pipeline/` canonical 5-file split. Backend state key `inf-pipeline/tfstate` in `opal-313476888478-terraform-state`. This is the foundation for every subsequent Inflection infrastructure TO (W1.1 bucket, W1.3 DynamoDB row, W2.1-W2.5 compute). Ships with empty module body + backend config first; resources land in subsequent TOs.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.1 row 3. `bd-pipeline` file layout: `main.tf`, `s3.tf`, `lambdas.tf`, `iam.tf`, `ec2.tf`, `eventbridge.tf`, `api-gateway.tf`, `s3-notifications.tf`, `alarms.tf`, `layers.tf`, `outputs.tf`, `CHANGELOG.json`, `code/`. Mirror all with empty/stub bodies; resources added per downstream TOs. Provider + backend config land in `main.tf`; locals land there too.

    Reference `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` for canonical workspace conventions. This TO creates the scaffold; W1.1 adds first live resource (S3 bucket).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>ls infra/aws/terraform/bd-pipeline/</run>
    <expect>main.tf, s3.tf, lambdas.tf, iam.tf, ec2.tf, eventbridge.tf, api-gateway.tf, s3-notifications.tf, alarms.tf, layers.tf, outputs.tf, CHANGELOG.json, code/. Mirror this file set.</expect>

    <run>cat infra/aws/terraform/bd-pipeline/main.tf (first 60 lines)</run>
    <expect>terraform block (required_version >= 1.5.0), aws provider, backend s3 with key=bd-pipeline/tfstate, default_tags. Mirror shape with key=inf-pipeline/tfstate.</expect>

    <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
    <expect>No tags yet (first deploy). First tag will be inf-pipeline-v1.0.0.</expect>

    Phase 2 (during implementation):
    <run>.tools/terraform.exe init (from infra/aws/terraform/inf-pipeline/)</run>
    <expect>Terraform initialized, backend configured, no modules found. Clean init.</expect>

    <run>.tools/terraform.exe plan</run>
    <expect>No changes (scaffold has no resources yet). Plan: 0 to add, 0 to change, 0 to destroy.</expect>

    Phase 3 (after applying W1.1 bucket on top of this scaffold):
    <run>comp-blast opal-data-inf</run>
    <expect>Graph rebuild reflects new bucket; downstream consumer list empty until inf-portal-publisher lands (W2.3).</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `opal-313476888478-terraform-state` S3 bucket (shared across all pipelines). Backend state key `inf-pipeline/tfstate` is NEW and unique — no contention.
    shared_resource: `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` — if any strategy change is needed, coordinate with CTO first. Default is "mirror existing patterns".
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "W1.2 is the foundation for every W1/W2/W6 downstream TO. Complete this scaffold before anything else runs."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `infra/aws/terraform/inf-pipeline/` exists with full file set mirroring bd-pipeline.
    2. `main.tf` has backend config with key=`inf-pipeline/tfstate`, provider defaults mirror BD.
    3. `terraform init` succeeds against S3 backend.
    4. `terraform plan` returns 0 resources (empty scaffold).
    5. `CHANGELOG.json` seeded with v1.0.0 entry documenting initial scaffold.
    6. Commit before apply per CLAUDE.md Rule 2.
    7. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_inflec_w1_2_tf_workspace.md` with init/plan output + file manifest.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/inf-pipeline/main.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/s3.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/lambdas.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/iam.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/ec2.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/eventbridge.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/api-gateway.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/s3-notifications.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/alarms.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/layers.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/outputs.tf</file>
      <file action="create">infra/aws/terraform/inf-pipeline/CHANGELOG.json</file>
      <file action="reference">infra/aws/terraform/bd-pipeline/main.tf</file>
      <file action="reference">infra/aws/TERRAFORM_PIPELINE_STRATEGY.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Mirror bd-pipeline canonical 5-file split — all files present even if stub.</requirement>
    <requirement id="2">Backend S3 key: `inf-pipeline/tfstate` (unique).</requirement>
    <requirement id="3">Provider default_tags: Project=OpalPortal, ManagedBy=Terraform, Environment=Production, System=InflectionPipeline.</requirement>
    <requirement id="4">First `terraform plan` returns 0 resources; scaffold only.</requirement>
    <requirement id="5">CHANGELOG.json seeded per record-terraform-deploy.sh convention.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Full infra/aws/terraform/inf-pipeline/ tree committed; author 0.7.0_AE_CloudOps.</deliverable>
    <deliverable type="tag">None yet — first tag (inf-pipeline-v1.0.0) ships with W1.1 bucket add.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT include any live resources in the scaffold. Scaffold is infrastructure-free.</rule>
    <rule>Do NOT reuse bd-pipeline backend key — MUST be inf-pipeline/tfstate.</rule>
    <rule>Do NOT deploy (no `terraform apply`) — this TO commits scaffold only. Apply happens with W1.1.</rule>
  </do_not>
</task_order>
