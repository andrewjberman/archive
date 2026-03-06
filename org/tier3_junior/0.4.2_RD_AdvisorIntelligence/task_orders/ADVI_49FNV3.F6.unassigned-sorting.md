<task_order>
  <metadata>
    <id>ADVI_49FNV3.F6.unassigned-sorting</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
  </metadata>

  <objective>
    Fix F6: "Unassigned" implementor appears ranked by NNA/AUA on the leaderboard, sometimes at #1.
    It should be pinned to the bottom of the table alongside "49F House", not participating in ranking.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Find the leaderboard sort/render logic in AdvisorsTab.tsx. Locate where
      "49F House" is currently excluded from ranking (or pinned to bottom). Name the exact variable,
      array, or filter condition.</requirement>
    <requirement id="2">Add "Unassigned" to the same exclusion/pin list as "49F House". Both entries
      must appear at the bottom of the table, below all named advisors, in both architect and
      implementor views.</requirement>
    <requirement id="3">"Unassigned" remains visible for transparency — it is not hidden. It is simply
      not ranked.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">"Unassigned" appears at the bottom of the leaderboard in implementor view
      regardless of its NNA or AUA value.</criterion>
    <criterion id="2">"49F House" behavior is unchanged (still pinned to bottom).</criterion>
    <criterion id="3">Portal DEV commit with `--author` flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>One-line or minimal change only. Do not refactor the sort logic beyond what is needed.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit pinning "Unassigned" to bottom of leaderboard.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
