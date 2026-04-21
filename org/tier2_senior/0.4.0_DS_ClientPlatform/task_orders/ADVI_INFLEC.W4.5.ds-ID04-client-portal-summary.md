<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.5-ID04-portal-summary</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>Author `data/inflection/scripts/gold/I_D04.client_portal_summary.py` — client-level portal summary. Mirrors BD D_04. Outputs per-client summary artifacts schema-identical to 49F equivalents.</objective>

  <context>PRD §9 W4.5. Mirror BD D_04 adapted for Inflection silver schema. NaT guard required per d87377a5 incident (D_04 was the crash point — `_nna_period_key` on NaT date). Blocked on W4.2 (NNA canonical).</context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-pipescript io D_04 (BD precedent)</run>. <run>python -m py_compile ... && .tools/ds-commit-gate.sh ...</run>
    Phase 2: <run>comp-pipescript io I_D04</run> — 0 COLUMN GAPS.
    Phase 3: <run>comp-pipescript deployed I_D04</run> — MATCH.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W4.2 (canonical NNA). The d87377a5 NaT crash was at D_04 consuming C_01. NaT guard in I_C01 (W4.2) prevents the crash here, but add defensive guard in I_D04 as well."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0. 0 COLUMN GAPS. ds-commit-gate pass. comp-pipescript deployed: MATCH. NaT guard present. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="create">data/inflection/scripts/gold/I_D04.client_portal_summary.py</file></files>
  </scope>

  <requirements>
    <requirement id="1">NaT guard on all date operations (defensive belt-and-suspenders vs W4.2 guard).</requirement>
    <requirement id="2">ds-commit-gate + commit + push + S3 upload.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">I_D04 committed + pushed.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT skip NaT guard.</rule></do_not>
</task_order>
