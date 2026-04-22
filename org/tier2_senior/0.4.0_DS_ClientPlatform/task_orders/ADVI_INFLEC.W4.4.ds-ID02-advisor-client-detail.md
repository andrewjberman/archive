<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.4-ID02-client-detail</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <completed>2026-04-22</completed>
    <completed_by>0.4.0_DS_ClientPlatform~A</completed_by>
    <evidence>data/orion/scripts/gold/I_D02.advisor_client_detail.py — py_compile PASS, ds-commit-gate PASS, MATCH on S3. platinum/advisors/ has 9 advisor subdirs (book.json). platinum/clients/ has per-client detail JSON.</evidence>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>Author `data/inflection/scripts/gold/I_D02.advisor_client_detail.py` — per-advisor client detail view. Mirrors BD D_02 pattern. Outputs per-advisor client records schema-identical to 49F platinum/advisors/{id}/. Single Fidelity custodian simplifies the custodian-breakdown field.</objective>

  <context>PRD §9 W4.4. Similar to BD D_02; adapter for Inflection silver schema (W3.1). No Schwab split — Fidelity is effectively 100% custodian share per advisor. Blocked on W4.1 + W4.2 outputs.</context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-pipescript io D_02 (BD precedent)</run>
    <run>python -m py_compile ... && .tools/ds-commit-gate.sh ...</run>
    Phase 2: <run>comp-pipescript io I_D02</run> — 0 COLUMN GAPS.
    Phase 3: <run>comp-pipescript deployed I_D02</run> — MATCH.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W4.1 + W4.2."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0. 0 COLUMN GAPS. ds-commit-gate pass. comp-pipescript deployed: MATCH. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="create">data/inflection/scripts/gold/I_D02.advisor_client_detail.py</file></files>
  </scope>

  <requirements>
    <requirement id="1">Mirror D_02. No Schwab custodian split.</requirement>
    <requirement id="2">ds-commit-gate + commit + push + S3 upload.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">I_D02 committed + pushed.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT add Schwab custodian breakdown.</rule></do_not>
</task_order>
