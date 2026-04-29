<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.2-gold-trigger-lambda</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: inf-gold-trigger Lambda module deployed (lambdas.tf line 76). -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Provision `inf-gold-trigger` Lambda shell in `inf-pipeline/lambdas.tf`. Mirrors `bd-gold-trigger` — starts gold runner via SSM SendCommand. S3 artifact uploaded from a mirrored source file. IAM scoped to `inf-gold-layer-runner` instance only.
  </objective>

  <context>PRD §4.1 row 4. Mirror bd-gold-trigger exactly; swap instance target to inf-gold-layer-runner ID (from W2.1). Phase 1 dispatch: manual SSM. EventBridge schedule deferred to W6.</context>

  <compiler_tools_mandate>
    Phase 1: <run>cat infra/aws/terraform/bd-pipeline/lambdas.tf | head -60</run> — Lambda module pattern to mirror.
    Phase 2: <run>.tools/terraform.exe plan</run> — 1 Lambda + IAM additions, nothing else.
    Phase 3: <run>comp-iam service inf-gold-trigger</run> — no MISSING perms. <run>aws lambda invoke --function-name inf-gold-trigger /tmp/resp.json; cat /tmp/resp.json</run> — dry-run or SSM dispatch confirmed.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W2.1 (inf-gold-layer-runner instance ID needed for IAM scoping)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Lambda `inf-gold-trigger` deployed; can invoke via AWS console or CLI.
    2. IAM scoped to inf-gold-layer-runner instance.
    3. comp-iam service inf-gold-trigger: 0 MISSING.
    4. Source map updated.
    5. Tag inf-pipeline-v1.1.0 (same as W2.1 if concurrent).
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
    <requirement id="1">Mirror bd-gold-trigger. No new logic.</requirement>
    <requirement id="2">Terraform-only deploy.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">lambdas.tf + iam.tf + source map.</deliverable>
    <deliverable type="tag">inf-pipeline-v1.1.0.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT add EventBridge schedule here — that is W6.1.</rule>
  </do_not>
</task_order>
