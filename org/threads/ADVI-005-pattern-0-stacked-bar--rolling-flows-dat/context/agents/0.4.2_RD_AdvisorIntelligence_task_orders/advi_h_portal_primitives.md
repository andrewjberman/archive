# Task Order: Stream H — Advisors Tab Portal Primitives Refactor

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-h-portal-primitives</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Refactor all sections of AdvisorsTab.tsx to use portal panel primitives
    (Panel, PanelHeader, PanelContent, SmartPanelFooter) instead of ad-hoc layout
    containers. Purely structural — visual output must be identical after refactor.
    No data dependency. Start immediately.
  </objective>

  <references>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref>portal/src/ui/components/panels</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="H.1">
      Read AdvisorsTab.tsx and the portal panel primitives at @/ui/components/panels
      before making changes. Identify the three sections to refactor:
        - Top Performers panel
        - Rolling Flows panel
        - Leaderboard panel
      Identify which ad-hoc container elements currently wrap each section.
    </requirement>
    <requirement id="H.2">
      Replace ad-hoc containers with portal panel primitives:
        Panel        — outer card container
        PanelHeader  — section title and any header controls
        PanelContent — content area
        SmartPanelFooter — footer area (if used)
      The visual output after refactor must be identical to the current layout.
      This is a structural change only — do not alter any data, chart logic, or styling.
    </requirement>
    <requirement id="H.3">
      Run bunx tsc -b after refactor. DE reviews for visual regression and structural
      correctness before DT pushes to DEV.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All three Advisors tab sections use Panel/PanelHeader/PanelContent primitives.</criterion>
    <criterion id="2">Visual output is pixel-identical to pre-refactor layout (no unintended styling change).</criterion>
    <criterion id="3">bunx tsc -b passes with no new type errors.</criterion>
    <criterion id="4">DE reviewed and approved before DT push.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Structural refactor only. Do not touch chart logic, data fetching, or styling values.</constraint>
    <constraint>Do NOT use emojis in any component or comment. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/AdvisorsTab -- H portal primitives refactor"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">AdvisorsTab.tsx: all sections refactored to portal panel primitives</deliverable>
  </deliverables>
</task_order>
```
