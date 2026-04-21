<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.3-publisher-shells</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Provision Lambda shells for `inf-portal-publisher`, `inf-portal-advisor-publisher`, and `inf-client-detail` in `inf-pipeline/lambdas.tf`. Each mirrors the corresponding bd-pipeline Lambda. S3 artifacts scoped to `opal-data-inf`. IAM scoped to `opal-data-inf` only.
  </objective>

  <context>PRD §4.1 rows 5-7. Shells are functional copies of bd equivalents with bucket/prefix substitution (opal-data-bd → opal-data-inf). DS populates the publisher logic in W4.6. AE's job here is infrastructure + shell code.</context>

  <compiler_tools_mandate>
    Phase 1: Read bd-pipeline lambdas for each publisher — copy pattern.
    Phase 2: <run>.tools/terraform.exe plan</run> — 3 Lambda additions, matching IAM additions.
    Phase 3: <run>comp-iam service inf-portal-publisher</run> — 0 MISSING. Same for advisor-publisher and client-detail.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W1.1 (opal-data-inf bucket must exist for S3 IAM scoping)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All three Lambdas provisioned.
    2. comp-iam service on each: 0 MISSING.
    3. S3 access scoped to opal-data-inf only.
    4. Source map updated for all three.
    5. Tag inf-pipeline-v1.2.0.
    6. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/inf-pipeline/lambdas.tf</file>
      <file action="modify">infra/aws/terraform/inf-pipeline/iam.tf</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Mirror bd-pipeline publisher pattern — only bucket references differ.</requirement>
    <requirement id="2">No cross-bucket IAM access.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">lambdas.tf + iam.tf + source map.</deliverable>
    <deliverable type="tag">inf-pipeline-v1.2.0.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT grant access to opal-data-bd.</rule>
  </do_not>
</task_order>
