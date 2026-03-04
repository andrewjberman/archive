# Task Order: Stream C3 — Snapshot CLA Simplified Two-Color Visualization

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-c3-cla-snapshot</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>complete</status>
  </metadata>

  <objective>
    Fix the Snapshot CLA view in DistributionTab, which is incorrectly rendering as a
    flows/NNA chart. Replace with a clean two-color NMNC/NMEC proportional display.
    Data is in header_metrics.json — no DS deploy needed. Start immediately.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="C3.1">
      Read DistributionTab.tsx and types.ts before making changes. Locate the current
      CLA snapshot rendering. Identify which fields from header_metrics.json it currently
      uses and confirm against the ClaView type in types.ts.
      If uncertain which specific fields carry NMNC/NMEC AUA, check with DE before committing.
    </requirement>
    <requirement id="C3.2">
      Replace the current CLA snapshot rendering with a clean two-color proportional display:
        - Green = NMNC (New Client AUA)
        - Blue = NMEC (Existing Client AUA)
        - Format: horizontal stacked bar or split donut — clean, no axes, just two
          proportions with AUA dollar amounts and percentages labeled
        - Labels: "New Clients (NMNC)" in green, "Existing Clients (NMEC)" in blue
      ZERO inflow/outflow data. ZERO NNA vocabulary. ZERO blue/red flows visual language.
      This is a composition view, not a flows view.
    </requirement>
    <requirement id="C3.3">
      The visualization must support the time machine period selector (q1/q2/q3)
      to show how the new-client percentage has shifted across periods.
      Each period selection updates the NMNC/NMEC proportions shown.
    </requirement>
    <requirement id="C3.4">
      Run bunx tsc -b after changes. DE reviews NMNC/NMEC label accuracy against
      actual header_metrics.json field values before DT pushes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">CLA snapshot shows only two colors: green NMNC and blue NMEC. No flows chart elements.</criterion>
    <criterion id="2">Each segment labeled with name, AUA dollar amount, and percentage.</criterion>
    <criterion id="3">Time machine period selector (q1/q2/q3) updates proportions correctly.</criterion>
    <criterion id="4">DE has confirmed NMNC/NMEC field accuracy against header_metrics.json before DT push.</criterion>
    <criterion id="5">bunx tsc -b passes with no new type errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No inflow/outflow data, no NNA. CLA = client lifecycle composition (new vs existing), not flows.</constraint>
    <constraint>If uncertain about which header_metrics.json fields map to NMNC/NMEC AUA, ask DE before implementing. Do not guess field names.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- C3 CLA snapshot two-color redesign"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: CLA snapshot replaced with two-color NMNC/NMEC proportional display</deliverable>
  </deliverables>
</task_order>
```
