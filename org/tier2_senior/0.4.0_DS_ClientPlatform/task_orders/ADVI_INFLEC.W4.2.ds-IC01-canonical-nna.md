<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.2-IC01-nna</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>pending</status><!-- GO 2026-04-22 per Andrew directive — assigned to ~A -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author `data/inflection/scripts/gold/I_C01.canonical_nna.py` — NNA from Activity Category in Orion TRN silver. No Schwab overlay (Inflection is single-custodian Fidelity). Mirrors `data/black_diamond/scripts/gold/C_01.canonical_nna.py` but without the schwab_flows.py overlay join. NaT guard mandatory on all date joins (d87377a5 incident). Outputs `gold/canonical/canonical_nna_{date}.parquet` to opal-data-inf.
  </objective>

  <context>PRD §9 W4.2. Simpler than BD's C_01: no Schwab TRN_NNA imputation, no schwab_flows outer-merge that introduced the NaT bug in d87377a5. Inflection NNA = Activity Category from Orion TRN directly. Journal In asymmetry ($58.8M net firm-wide per PRD §10 Q8) needs investigation during silver QA (W3.4). If Journal In is an external transfer pattern, it may belong in NNA; document convention in silver spec and carry forward here.</context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-pipescript io C_01 (BD precedent)</run> — NNA pattern reference.
    <run>python -m py_compile ... && .tools/ds-commit-gate.sh ...</run>
    Phase 2: <run>comp-pipescript io I_C01</run> — 0 COLUMN GAPS.
    Phase 3: <run>comp-pipescript deployed I_C01</run> — MATCH.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W3.4 silver QA + W4.1 (holdings may feed NNA attribution)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0. 0 COLUMN GAPS. ds-commit-gate pass.
    2. Output parquet: non-null nna values for advisors with activity.
    3. NaT guard present on all date joins.
    4. No schwab_flows import or Schwab-specific logic.
    5. Journal In convention documented in session log.
    6. comp-pipescript deployed: MATCH.
    7. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inflection/scripts/gold/I_C01.canonical_nna.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">No Schwab overlay. Fidelity-only NNA from Activity Category.</requirement>
    <requirement id="2">NaT guard mandatory.</requirement>
    <requirement id="3">ds-commit-gate + commit + push + S3 upload.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">I_C01 committed + pushed.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT add schwab_flows import.</rule><rule>Do NOT skip NaT guard.</rule></do_not>
</task_order>
