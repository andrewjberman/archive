<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.8-frontend-dev-validation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <co_owner>0.4.0_DT_ClientPlatform</co_owner>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Full-page `/frontend-dev` validation with an Inflection test user on AdvisorIntelligence + leaderboard + books tab + distribution (FidelityCustodianBar). Confirms the complete portal rendering pipeline works for Inflection end-to-end.
  </objective>

  <context>PRD §9 W5.8. Requires platinum artifacts in S3 (W4.6) + auth flow working (W5.6) + portal overrides wired (W5.1) + firmAccess.ts updated (W5.2) + AuthContext dev-mode supports inflection (W5.4). Blocked on all of those. DE drives frontend-dev; DT supports with test JWT/user access.</context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>0 MISSING. All Inflection override components in rendered set.</expect>
    Phase 3:
    <run>/frontend-dev (AdvisorIntelligence constitution, firmId=inflection)</run>
    <expect>PASS. Leaderboard renders 11 advisors. FidelityCustodianBar renders 99.4% Fidelity. Books tab loads per-advisor data. Distribution renders.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W4.6 + W5.1 + W5.2 + W5.4 + W5.6. All five must be complete."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. /frontend-dev constitution: PASS on firmId=inflection.
    2. Leaderboard renders >= 11 advisors with non-zero AUM.
    3. FidelityCustodianBar renders (Fidelity dominant).
    4. Books tab loads without console error.
    5. 0 MISSING in comp-transform schema-check.
    6. Session log with /frontend-dev pass record + screenshot path.
  </acceptance_criteria>

  <scope>
    <files><file action="reference">portal/src/pages/AdvisorIntelligence/ (end-to-end read)</file></files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W4.6 + W5.1 + W5.2 + W5.4 + W5.6.</requirement>
    <requirement id="2">Do NOT accept PARTIAL PASS — all surfaces must render.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with /frontend-dev output.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT accept partial pass.</rule></do_not>
</task_order>
