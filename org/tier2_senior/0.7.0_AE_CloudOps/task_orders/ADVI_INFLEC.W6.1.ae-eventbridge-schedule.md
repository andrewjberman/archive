<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w6.1-eventbridge-schedule</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Add EventBridge schedule for `inf-exporter` in `inf-pipeline/eventbridge.tf`. Nightly or intraday cadence (Andrew to confirm frequency). Triggers `inf-exporter` EC2 to start and run `orion_export.ts`. Phase 3 deferred feature — do NOT start until W5 is stable.
  </objective>

  <context>PRD §5.3 Phase 3 + §4.1 row 12. Human-in-the-loop latency accepted (OTP relay). EventBridge schedule triggers EC2 start → exporter runs → waits for OTP → OTP callback from Andrew → download completes → silver/gold chain runs. Blocked on W5 (Inflection portal working end-to-end) + W2.8 (exporter manually validated).</context>

  <compiler_tools_mandate>
    Phase 1: <run>cat infra/aws/terraform/bd-pipeline/eventbridge.tf</run> — pattern reference.
    Phase 2: <run>.tools/terraform.exe plan</run> — EventBridge rule + target additions only.
    Phase 3: <run>aws events list-rules --name-prefix inf-</run> — rule present.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W5 stability + W2.8. Schedule cadence: confirm with Andrew before setting."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. EventBridge schedule rule for inf-exporter in TF state.
    2. Terraform 0-diff on rerun.
    3. Tag inf-pipeline-v{next}.
    4. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="modify">infra/aws/terraform/inf-pipeline/eventbridge.tf</file></files>
  </scope>

  <requirements>
    <requirement id="1">Confirm schedule frequency with Andrew before apply.</requirement>
    <requirement id="2">Blocked on W5 + W2.8.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">eventbridge.tf with schedule rule.</deliverable>
    <deliverable type="tag">inf-pipeline-v{next}.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT deploy before W5 is stable.</rule></do_not>
</task_order>
