<task_order>
  <metadata>
    <id>ADVI_49FNV3.F7.zebra-striping</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
  </metadata>

  <objective>
    Fix F7: leaderboard table rows have uniform background, making the table hard to scan.
    Apply alternating row backgrounds (zebra striping) matching the pattern used in
    SecurityScanner and PortfolioManagement pages.
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
    <requirement id="1">Read the leaderboard table row rendering in AdvisorsTab.tsx. Find where
      row `className` is set.</requirement>
    <requirement id="2">Check SecurityScanner or PortfolioManagement page for the existing zebra
      striping pattern. Use the exact same CSS/Tailwind classes — do not invent a new pattern.</requirement>
    <requirement id="3">Apply the alternating row background to all leaderboard rows in both
      architect and implementor views.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Leaderboard rows alternate background color matching other pages.</criterion>
    <criterion id="2">Style is visually consistent with SecurityScanner / PortfolioManagement.</criterion>
    <criterion id="3">Portal DEV commit with `--author` flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Match existing patterns exactly. Do not create new color variables or CSS classes.</constraint>
    <constraint>Can be combined with F6 in the same commit if both are trivial changes.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit adding zebra striping to leaderboard.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
