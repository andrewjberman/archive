<task_order>
  <metadata>
    <id>ADVI_INFLEC.W8.4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>pending</status>
    <acked>pending</acked>
    <project_code>ADVI_INFLEC</project_code>
    <priority>P1 — Andrew directive 2026-04-22; sequencing gate for W8.2 Inflection coverage</priority>
    <sla>~30min (read-only DDB verification)</sla>
    <decision_authority>Andrew directive 2026-04-22 (PRD §9 W8)</decision_authority>
    <dependency to="none">Independent read-only check. Runs first as pre-flight.</dependency>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §9 W8 (commit 7fae09b9)</ref>
    <ref type="related_to" status="pending">ADVI_INFLEC.W5.5 (DT provisions first Inflection users) — this TO verifies W5.5's output count before W8.2 depends on it</ref>
    <ref type="ddb_table">opal-partner-inflection (in `us-east-1`, module `partner-firm-table`, created by 0.7.0_AE_CloudOps)</ref>
  </references>

  <objective>
    Verify `opal-partner-inflection` DynamoDB table contains at least one real-advisor identity row (beyond the 2 baseline items created by AE's infrastructure provisioning) to support W8.2's Inflection JWT test coverage.

    EXPLICIT SCOPE: READ-ONLY. If insufficient rows, escalate back to DT W5.5 for provisioning — do NOT author new user-row provisioning code under this TO.
  </objective>

  <scope>
    <files>
      <file action="read-only">DynamoDB table opal-partner-inflection (AWS CLI / console)</file>
      <file action="read-only">infra/aws/terraform/partner-firms/inflection.tf (for baseline item reference)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Scan opal-partner-inflection and classify rows:
      <run>aws dynamodb scan --table-name opal-partner-inflection --region us-east-1 --output json</run>
      Classify each item as BASELINE (created by AE infrastructure — the 2 existing items) vs REAL-ADVISOR (identity rows matching partner-firm user schema per `infra/aws/users/partner-schemas/49financial.md` equivalent shape).
    </requirement>
    <requirement id="2">Report counts:
      - Total item count
      - Baseline item count + their keys
      - Real-advisor row count + their keys (if any)
    </requirement>
    <requirement id="3">Decision tree:
      - IF real-advisor count ≥ 1 AND at least one has `firmRole: admin` → W8.2 Inflection leg CLEARED. MCP DT with the test-user identifier list + record as GO signal.
      - IF real-advisor count ≥ 1 BUT none `firmRole: admin` → W8.2 Inflection leg CLEARED FOR VIEW-ONLY. Still MCP DT with list + flag admin-tier gap.
      - IF real-advisor count = 0 → W8.2 Inflection leg DEFERRED. MCP DT 0.4.0 with a heads-up referencing W5.5 (first Inflection user provisioning) and escalate back to COO so W8.2 status stays staged-Inflection-only.
    </requirement>
    <requirement id="4">Commit with `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"` and `--only` on session log only (no infra or portal changes under this TO).</requirement>
  </requirements>

  <compiler_tools_mandate>
    Phase 1 (before scan): none — this is read-only DDB verification, no blast-radius risk.
    Phase 3 (after scan): append row-count matrix to `org/compiler-tools-log.md` with `manual-ddb-scan` tool type (acceptable per "one sentence why no comp-* tool" convention).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <downstream to="W8.2">W8.2 Inflection leg GO/NO-GO signal. MCP DT with result.</downstream>
    <upstream to="W5.5" status="pending">W5.5 is the work that POPULATES this table with real users. W8.4 VERIFIES. If W5.5 hasn't landed users, W8.4 escalates (does not provision).</upstream>
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="1">Item count matrix in session log (total / baseline / real-advisor / admin-tier).</ac>
    <ac id="2">Explicit decision recorded: CLEARED / CLEARED-VIEW-ONLY / DEFERRED.</ac>
    <ac id="3">MCP to 0.4.0_DT_ClientPlatform with result (either test-user list or deferral + W5.5 reference).</ac>
    <ac id="4">MCP to 2.0.0_SA_COO with decision summary.</ac>
    <ac id="5">Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/{date}/inflec_w8_4_partner_table_gate.md`.</ac>
  </acceptance_criteria>

  <deliverables>
    <deliverable type="document">Session log with row-count matrix + decision</deliverable>
    <deliverable type="mcp">MCP to DT (W8.2 Inflection leg GO/NO-GO)</deliverable>
    <deliverable type="mcp">MCP to COO (decision summary)</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT create, modify, or delete any DDB items under this TO. Read-only scan.</rule>
    <rule>Do NOT provision new Inflection users — that's W5.5's scope (DT 0.4.0).</rule>
    <rule>Do NOT touch infra/aws/terraform/partner-firms/inflection.tf.</rule>
  </do_not>
</task_order>
