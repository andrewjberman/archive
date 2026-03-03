# Task Order: Stream I — Top Performers Visual Identity Redesign

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-i-top-performers</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Redesign the Top Performers (Top 3 highlights) panel in AdvisorsTab to communicate
    rank and achievement clearly. Current design is visually weak — rank, name, and NNA
    are not prominent enough. No data dependency. Start immediately.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
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
    <requirement id="I.1">
      Read AdvisorsTab.tsx before making changes. Understand how Top Performers data
      is currently rendered (data source, current card/list structure, period toggle
      integration). Check which Lucide icons are currently imported in the file
      or elsewhere in the portal before deciding on iconography.
    </requirement>
    <requirement id="I.2">
      Redesign the Top Performers panel so that for each of the top 3 advisors:
        - Rank (1st / 2nd / 3rd) is visually prominent — use a medal/badge treatment
          or rank number styled as a badge, using Lucide icons available in the codebase
        - Advisor name is large and immediately readable
        - Key metric (NNA for the active period) is immediately readable below the name
        - Overall feel: achievement-oriented, podium or headline card style
      Consistent with portal design language — do not introduce third-party icon sets.
    </requirement>
    <requirement id="I.3">
      The redesign must work across all period toggles.
      When the active period changes, Top Performers rankings and NNA values update.
      Do not hard-code period-specific data.
    </requirement>
    <requirement id="I.4">
      Run bunx tsc -b after changes. DE reviews the visual design before DT pushes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Rank (1/2/3) is visually prominent using portal-consistent iconography (Lucide or badge styling).</criterion>
    <criterion id="2">Advisor name and NNA metric are immediately readable in the card.</criterion>
    <criterion id="3">Rankings update correctly across all period toggles (QTD/YTD/1Y/3Y/Max).</criterion>
    <criterion id="4">bunx tsc -b passes with no new type errors.</criterion>
    <criterion id="5">DE reviewed and approved the visual design before DT push.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Use only Lucide icons already in the codebase. Check what is available before choosing iconography.</constraint>
    <constraint>Do NOT introduce new icon packages or third-party illustration libraries.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or label. Plain ASCII text labels only.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/AdvisorsTab -- I Top Performers visual redesign"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">AdvisorsTab.tsx: Top Performers panel redesigned with rank prominence and medal/badge treatment</deliverable>
  </deliverables>
</task_order>
```
