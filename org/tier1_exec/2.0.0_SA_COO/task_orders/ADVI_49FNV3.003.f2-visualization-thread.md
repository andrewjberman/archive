<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-09-003</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>2.0.0_SA_COO</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
  </metadata>

  <objective>
    Orchestrate a Pattern 0 thread for ADVI_49FNV3 to converge on the correct visualization
    approach for the F2 projection system and GRO chart in the Assets Overview panel
    (PartnerAnalytics.tsx). Andrew reviewed the current implementation and identified
    fundamental issues with projection math (AUA showing 0/0 after fix), GRO chart
    unintelligibility, and tooltip clarity across all three views (AUA, NNA, GRO).

    The thread should produce a converged design specification that the RD can execute.
  </objective>

  <scope>
    <thread>
      <project>ADVI_49FNV3</project>
      <serial>ADVI_49FNV3-003</serial>
      <topic>F2 projection visualization + GRO chart redesign</topic>
      <pattern>Pattern 0 (design convergence before task orders)</pattern>
      <participants>
        <agent role="architect">1.0.0_SA_CTO</agent>
        <agent role="wiring">0.4.0_DE_ClientPlatform</agent>
        <agent role="implementation">0.4.2_RD_AdvisorIntelligence</agent>
      </participants>
    </thread>
  </scope>

  <context_injection>
    Inject the following into the thread CONTEXT.json:

    1. CTO analysis document (MANDATORY — this is the primary input):
       `org/tier1_exec/1.0.0_SA_CTO/deliverables/ADVI_49FNV3-F2-visualization-analysis.md`
       Contains: all flaws identified, current chart patterns across AdvisorIntelligence,
       existing tooltip/hero/projection patterns, and 5 specific questions to converge on.

    2. RD recent session log:
       `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/2026-03-09/ADVI_49FNV3_F2_F4_F6_F7_N1N2.md`
       Contains: what the RD built, commit references, implementation decisions.

    3. The current source file (for reference, not full injection — too large):
       `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`
       Key line ranges: 443-550 (projection logic), 1040-1195 (AUA chart+tooltip),
       1220-1400 (NNA chart+tooltip), 1441-1561 (GRO chart+tooltip), 1576-1610 (legends),
       1930-1985 (hero metrics).

    4. The F2 fix commit diff:
       `git diff 9ce8d3b~1 9ce8d3b` in the portal submodule.
  </context_injection>

  <requirements>
    <requirement id="1">Create the thread using create-thread.sh with --project ADVI_49FNV3
      and the three participants listed above.</requirement>
    <requirement id="2">Inject the CTO analysis document as primary context. The 5 questions
      in Section 7 of the document are the convergence targets.</requirement>
    <requirement id="3">Run the thread to convergence. Each agent contributes their domain
      expertise:
      - CTO (1.0.0_SA_CTO): architectural constraints, data model awareness, pattern
        consistency across the portal
      - DE (0.4.0_DE_ClientPlatform): data contract knowledge, Recharts API capabilities,
        type system implications
      - RD (0.4.2_RD_AdvisorIntelligence): implementation feasibility, visual design
        judgment, what works within Recharts constraints</requirement>
    <requirement id="4">The thread output should be a concrete specification covering:
      - Exact projection formula for each view (AUA stock, NNA flow, GRO flow)
      - Exact tooltip layout for each view (what rows, what labels, what values)
      - GRO chart type decision (keep lines, convert to bars, or hybrid)
      - GRO hero metrics specification
      - Edge case handling (no prior period, period complete, negative projections)</requirement>
    <requirement id="5">After convergence, issue task orders to 0.4.2_RD_AdvisorIntelligence
      based on the agreed specification. These replace the current pending F2 work.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Thread completes with all three agents converging.</criterion>
    <criterion id="2">Output specification addresses all 5 questions from the CTO analysis
      document Section 7.</criterion>
    <criterion id="3">RD task order(s) issued with concrete, implementable requirements
      derived from the thread consensus.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is Pattern 0 — design only, no code. The RD should not start
      implementing until the thread converges and task orders are issued.</constraint>
    <constraint>The thread should reference existing patterns across the portal (documented
      in the CTO analysis Section 6) to maintain visual consistency.</constraint>
    <constraint>GRO data is flow-based (period deltas), not stock-based. Any chart redesign
      must respect this — GRO values can be negative.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="thread">Completed ADVI_49FNV3-003 thread with converged
      visualization specification.</deliverable>
    <deliverable type="document">Task order(s) to 0.4.2_RD_AdvisorIntelligence for
      implementation.</deliverable>
  </deliverables>

  <references>
    <ref type="analysis">org/tier1_exec/1.0.0_SA_CTO/deliverables/ADVI_49FNV3-F2-visualization-analysis.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md (F2 section, corrected 2026-03-09)</ref>
    <ref type="source">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</ref>
    <ref type="commit">Portal DEV 9ce8d3b (F2-fix AUA delta projection)</ref>
    <ref type="commit">Portal DEV 594c3f6 (F2/F4/N1-N2 original implementation)</ref>
  </references>
</task_order>
