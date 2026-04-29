<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.9-ec2-manifest</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29: EC2_MANIFEST.json has all 4 inf-* services registered (inf-gold-layer-runner, inf-gold-qa-runner, inf-exporter, inf-bronze-runner). -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Register the Inflection pipeline's EC2 services + S3 bucket in `infra/aws/ec2/EC2_MANIFEST.json` per CLAUDE.md Rule 8 ("source of truth for all EC2 services; CI/CD depends on it"). Services in scope: `inf-gold-layer-runner` (W2.1), `inf-exporter` (W2.4), `inf-gold-qa-runner` (Phase 2). Bucket `opal-data-inf` (W1.1) referenced where applicable. Entries staged; populated as each compute resource lands in W2.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.1 rows 7-9 + CLAUDE.md Rule 8. Manifest entries follow the existing format (see `infra/aws/ec2/EC2_MANIFEST.json` — `bd-gold-layer-runner`, `bd-exporter` entries as precedent). Per `feedback_ec2_gold_runner_sizing.md` + `feedback_prod_runner_eventbridge_only.md` memory: each runner has a scope (`prod`/`qa`), a sizing note, and IAM role pointer.

    **Sequencing:** This TO authors manifest STUB entries for all three EC2 services at project start (placeholder instance IDs + instance types). W2.1 populates `inf-gold-layer-runner` actual values. W2.4 populates `inf-exporter`. `inf-gold-qa-runner` stub stays `Phase 2` label until that TO lands.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>cat infra/aws/ec2/EC2_MANIFEST.json | head -100</run>
    <expect>Existing BD entries (bd-gold-layer-runner, bd-gold-qa-runner, bd-exporter). Mirror field shape.</expect>

    <run>jq '.services | keys[]' infra/aws/ec2/EC2_MANIFEST.json</run>
    <expect>Service key list. Inflection names must be unique.</expect>

    Phase 2 (during implementation):
    Stub entries added for:
    - `inf-gold-layer-runner` (status: Phase 1, sized c6a.2xlarge per PRD §6.2, IAM role `inf-gold-layer`)
    - `inf-exporter` (status: Phase 2, sized t3.medium per PRD §6.3)
    - `inf-gold-qa-runner` (status: Phase 2 deferred, placeholder)

    <run>python -m json.tool infra/aws/ec2/EC2_MANIFEST.json > /dev/null</run>
    <expect>JSON valid; no parse errors.</expect>

    Phase 3 (after each W2.x lands):
    Manifest entries updated with real instance IDs + ARNs.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `infra/aws/ec2/EC2_MANIFEST.json` — shared across all AE agents.
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "Stub entries now; full population per W2.1/W2.4 TO. Do NOT touch BD entries. JSON must remain valid after every edit (`python -m json.tool` gate)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Three stub entries present in EC2_MANIFEST.json: `inf-gold-layer-runner`, `inf-gold-qa-runner`, `inf-exporter`.
    2. Each entry includes: instance_type (from PRD §6), status (Phase 1/2), IAM role name, and a comment pointing to the responsible W2 TO.
    3. JSON validates via `python -m json.tool`.
    4. `opal-data-inf` S3 bucket is represented in whatever section EC2_MANIFEST.json tracks buckets (if applicable — some manifests are EC2-only; if so, skip).
    5. Session log with diff + jq verification.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json</file>
      <file action="reference">CLAUDE.md Rules 7-11</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Preserve existing manifest entries byte-for-byte. Only additive edits.</requirement>
    <requirement id="2">JSON must validate after every edit.</requirement>
    <requirement id="3">No emojis. ASCII only.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">EC2_MANIFEST.json with stub entries + session log. Author 0.7.0_AE_CloudOps.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT touch BD entries.</rule>
    <rule>Do NOT populate real instance IDs in this TO — those land with W2.1/W2.4.</rule>
    <rule>Do NOT break JSON validity.</rule>
  </do_not>
</task_order>
