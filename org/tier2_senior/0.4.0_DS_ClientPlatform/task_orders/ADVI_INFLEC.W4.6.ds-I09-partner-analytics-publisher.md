<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.6-I09-publisher</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>pending</status><!-- GO 2026-04-22 per Andrew directive — assigned to ~A -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>Author `data/inflection/scripts/gold/I_09.generate_partner_analytics.py` — platinum publisher equivalent. Reads gold outputs and writes `platinum/firm/*.json` + `platinum/advisors/{id}/*.json` to opal-data-inf with schema identical to 49F platinum shape. This is the gating script before portal can render Inflection data.</objective>

  <context>PRD §9 W4.6. Mirrors bd-portal-publisher Lambda logic but runs as a gold-chain script on the runner. Schema-identical output is critical — portal components read the same JSON shape regardless of firmId. If Inflection-specific OPTIONAL fields are added (e.g., `investment_model` per PRD §10 Q10), they land as optional keys the portal ignores if absent. Blocked on W4.1-W4.5 all complete.</context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-pipescript io I_09 (once created)</run> — 0 COLUMN GAPS.
    <run>python -m py_compile ... && .tools/ds-commit-gate.sh ...</run>
    Phase 3:
    <run>comp-validate I_09 --artifact /tmp/partner_analytics.json</run> — exits 0.
    <run>comp-pipescript deployed I_09</run> — MATCH.
    <run>aws s3 ls s3://opal-data-inf/platinum/firm/ | head -10</run> — artifacts present.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "This is the gate before W5 portal integration. Do NOT signal W5 start until comp-validate exits 0 and platinum/ artifacts are confirmed in S3."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0. 0 COLUMN GAPS. ds-commit-gate pass.
    2. `platinum/firm/leaderboard.json` schema-identical to 49F equivalent.
    3. `platinum/firm/partner_analytics.json` present.
    4. `platinum/advisors/{id}/*.json` written for all 11 Inflection advisors.
    5. comp-validate exits 0.
    6. comp-pipescript deployed: MATCH.
    7. Session log — MCP COO when complete (W5 gate signal).
  </acceptance_criteria>

  <scope>
    <files><file action="create">data/inflection/scripts/gold/I_09.generate_partner_analytics.py</file></files>
  </scope>

  <requirements>
    <requirement id="1">Schema-identical platinum output to 49F — do NOT add required fields; OPTIONAL only.</requirement>
    <requirement id="2">comp-validate exits 0 before signaling COO.</requirement>
    <requirement id="3">ds-commit-gate + commit + push + S3 upload.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">I_09 committed + pushed.</deliverable>
    <deliverable type="document">Session log with comp-validate output.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT add required fields to platinum schema — optional only.</rule>
    <rule>Do NOT signal W5 without comp-validate exit 0.</rule>
  </do_not>
</task_order>
