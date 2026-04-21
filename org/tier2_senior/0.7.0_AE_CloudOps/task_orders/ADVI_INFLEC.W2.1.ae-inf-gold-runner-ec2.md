<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.1-gold-runner-ec2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Provision `inf-gold-layer-runner` EC2 (c6a.2xlarge, Amazon Linux 2023, dedicated) in `infra/aws/terraform/inf-pipeline/ec2.tf`. Mirror `bd-gold-layer-runner` pattern exactly: EBS gp3 200GB, IAM role `inf-gold-layer` (S3 full access `opal-data-inf` only), SSM access, CloudWatch Logs, watchdog timer (grace-window pattern per `11478af7`). Register in EC2_MANIFEST.json (update W1.9 stub entry with real instance ID).
  </objective>

  <context>
    PRD §6.1-§6.2. Dedicated runner per Andrew 2026-04-21 ("different data source"). Spec: c6a.2xlarge (8 vCPU / 16 GB). Watchdog: same 5-min grace-window pattern shipped in `11478af7` (not GOLD_KEEP_ALIVE). `inf-gold-dispatch.sh --from I_00 --chain full` will be authored in W3/W4. This TO provisions the EC2 only.
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>cat infra/aws/terraform/bd-pipeline/ec2.tf</run>
    <expect>bd-gold-layer-runner pattern. Mirror for inf-gold-layer-runner.</expect>
    <run>comp-iam service inf-gold-layer</run>
    <expect>No MISSING perms after iam.tf includes S3 full access on opal-data-inf, SSM, CWLogs.</expect>

    Phase 3:
    <run>aws ec2 describe-instances --filters Name=tag:Name,Values=inf-gold-layer-runner --query 'Reservations[*].Instances[*].{ID:InstanceId,State:State.Name,Type:InstanceType}'</run>
    <expect>1 instance, state stopped or running, type c6a.2xlarge.</expect>
    <run>comp-pipescript deployed inf-gold-dispatch (once script exists)</run>
    (Deferred to W3/W4 — skip in this TO.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: EC2_MANIFEST.json — update W1.9 stub with real instance ID after Terraform apply.
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "W1.1 bucket must exist before runner provisioned (runner IAM scoped to opal-data-inf). W1.2 workspace required."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `inf-gold-layer-runner` EC2 provisioned and registered in EC2_MANIFEST.json with real instance ID.
    2. IAM role `inf-gold-layer` has S3 access on `opal-data-inf` only — not `opal-data-bd`.
    3. Watchdog pattern matches `11478af7` grace-window approach.
    4. Terraform 0-diff on rerun.
    5. Tag `inf-pipeline-v1.1.0` with `--follow-tags`.
    6. Session log with terraform plan/apply output, instance ID, IAM policy doc, comp-iam run.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/inf-pipeline/ec2.tf</file>
      <file action="modify">infra/aws/terraform/inf-pipeline/iam.tf</file>
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">c6a.2xlarge — do not substitute without COO approval.</requirement>
    <requirement id="2">Watchdog: grace-window pattern (11478af7). No GOLD_KEEP_ALIVE touch.</requirement>
    <requirement id="3">IAM isolation: opal-data-inf only. No cross-bucket access.</requirement>
    <requirement id="4">Tag after deploy per CLAUDE.md Rule 6.</requirement>
    <requirement id="5">safe-ec2-deploy.sh for any code deployment per CLAUDE.md Rule 7.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">ec2.tf + iam.tf changes. EC2_MANIFEST.json updated.</deliverable>
    <deliverable type="tag">inf-pipeline-v1.1.0.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT share IAM role with bd-gold-layer-runner.</rule>
    <rule>Do NOT use GOLD_KEEP_ALIVE watchdog — use 11478af7 grace-window.</rule>
  </do_not>
</task_order>
