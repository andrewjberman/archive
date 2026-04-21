<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.0.3-cto-review</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <co_owner>0.4.0_DE_ClientPlatform</co_owner>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Review DE's W5.0.2 folder structure proposal for `portal/src/pages/AdvisorIntelligence/`. Iterate with DE to agreement on target structure. Sign off on the file-move plan so W5.0.4 execution can start. Resolve all AMBIGUOUS component categorizations from W5.0.1.
  </objective>

  <context>
    PRD §7.3. CTO authored the principle ("if shape is same across partners → _shared; if encodes partner decision → _partners/{firm}/"). DE authored the detailed proposal via W5.0.2. CTO's job here is to validate alignment with multi-tenant architectural principle and ensure no unnecessary duplication.

    Key decisions to make in review:
    1. How does `index.tsx` partner-router extract firmId — from AuthContext JWT claim or from URL param?
    2. For AMBIGUOUS components: composition (shared primitive + partner prop injection) vs hard split?
    3. Any `advisor-intelligence.ts` API layer changes that should surface here vs W5.3?
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>Baseline schema. Any deviation from W5.0.1 run = DE made premature code changes. Flag.</expect>

    <run>comp-blast AdvisorIntelligence</run>
    <expect>Downstream blast radius — no active competing TOs touching this tree.</expect>

    Phase 3:
    (N/A — review TO; no code shipped.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Written sign-off comment appended to DE's `advi_inflec_folder_structure_proposal.md` (or separate review doc at CTO's discretion).
    2. Every AMBIGUOUS component from W5.0.1 has a concrete resolution in the sign-off.
    3. `index.tsx` composition pattern agreed (firmId source, partner-router shape).
    4. W5.0.4 unblocked — DE receives explicit GO to proceed with refactor execution.
    5. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/advi_inflec_folder_structure_proposal.md (add review section)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W5.0.2 proposal document.</requirement>
    <requirement id="2">CTO signs off before DE starts W5.0.4. No autonomous execution.</requirement>
    <requirement id="3">If major disagreement: iterate via MCP (max 1 round) before signing off.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Written sign-off on proposal + AMBIGUOUS resolutions.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT let W5.0.4 start without explicit CTO sign-off in the proposal doc.</rule>
  </do_not>
</task_order>
