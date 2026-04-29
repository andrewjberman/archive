# Task Order: ADVI_INFLV2.007 — DE: BooksTab Inflection Mode

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-007</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <completed_date>2026-04-29</completed_date>
    <ship_evidence>portal commits 58fdf1f (skeleton + ClientsList layout-driven filtering/drill) + 1511d0b (full InflectionInsightsPanel 3-panel impl + 3 fetch helpers + types). Push to origin/DEV pending DT.</ship_evidence>
    <priority>HIGH — gates INFLV2.010 (RD smoke)</priority>
  </metadata>

  <objective>
    Implement the Inflection-mode BooksTab: Firm Overview → ClientsList path with no
    advisor-drill navigation step, a 3-entry advisor list (IWM / Peter / Patrick),
    and the InflectionInsightsPanel slot replacing FeeEfficiencyPanel.

    Driven by useTenantLayout() hook introduced in INFLV2.006.
  </objective>

  <scope>
    <task id="1" label="Firm Overview → ClientsList (no advisor-drill nav)">
      In ClientsTab.tsx:
        - Read layout.tabs.books.advisorDrill.enabled from useTenantLayout()
        - When advisorDrill.enabled === false: skip the advisor-drill navigation step;
          render Firm Overview panels → ClientsList directly
        - When advisorDrill.enabled === true: existing 49F behavior unchanged
    </task>

    <task id="2" label="3-entry advisor list">
      Wherever an advisor list is rendered in BooksTab:
        - Read layout.panels.advisorList from useTenantLayout()
        - Filter rendered entries to allowedAdvisorKeys: ['inflection_wealth_management', 'peter_lee', 'patrick_scanlan']
        - Cap at maxEntries: 3
        - 49F: allowedAdvisorKeys = [] (no cap) → all entries rendered as before
    </task>

    <task id="3" label="InflectionInsightsPanel slot">
      In ClientsTab.tsx:
        - Read layout.tabs.books.revenueOpsPanel from useTenantLayout()
        - When revenueOpsPanel === 'standard': render FeeEfficiencyPanel (existing behavior)
        - When revenueOpsPanel === 'inflection_insights': render InflectionInsightsPanel
          (reads artifact key confirmed by INFLV2.005; panel component per INFLV2.007 scope)
        - When revenueOpsPanel === 'suppressed': render nothing in that slot

      Create:
        portal/src/pages/AdvisorIntelligence/_partners/inflection/components/InflectionInsightsPanel.tsx
        - Reads platinum artifact at key from INFLV2.005 type contract
        - Renders the chosen insight visualization
        - Graceful empty-state if artifact absent (loading / unavailable copy)
    </task>

    <task id="4" label="Regression: 49F BooksTab unchanged">
      Verify 49F BooksTab behavior unchanged:
        - Advisor drill path still present
        - FeeEfficiencyPanel still renders
        - No advisor-list cap applied
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      firmId=inflection: BooksTab renders Firm Overview → ClientsList with no advisor-drill
      navigation entry visible.
    </criterion>
    <criterion id="2">
      firmId=inflection: advisor list renders exactly 3 entries (IWM, Peter Lee, Patrick Scanlan).
      No Keil entries. No entries beyond 3.
    </criterion>
    <criterion id="3">
      firmId=inflection: InflectionInsightsPanel renders in the FeeEfficiencyPanel slot
      (no FeeEfficiencyPanel visible).
    </criterion>
    <criterion id="4">
      firmId=49financial: existing BooksTab behavior unchanged (advisor drill present,
      FeeEfficiencyPanel present, no advisor-list cap).
    </criterion>
    <criterion id="5">
      Portal builds cleanly. No TypeScript errors. No console errors on Inflection BooksTab load.
    </criterion>
    <criterion id="6">
      RAVC to 2.0.0_SA_COO with portal version + brief description of what renders.
      Subject: RAVC — ADVI_INFLV2.007 COMPLETE | BooksTab Inflection mode live | portal-v[X]
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gates: INFLV2.005 COMPLETE (artifact type contract known) + INFLV2.006
    COMPLETE (useTenantLayout hook available).</constraint>
    <constraint>No new literal `firmId === 'inflection'` strings — all routing through
    useTenantLayout().</constraint>
    <constraint>No emojis in code.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_INFLV2.005"
                status="open"
                note="InflectionInsightsPanel artifact type contract needed before
                building the panel component."/>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_INFLV2.006"
                status="open"
                note="useTenantLayout hook must be live."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">ClientsTab.tsx + InflectionInsightsPanel.tsx. Portal DEV branch.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §8 (UI scope)</ref>
    <ref type="component">portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx</ref>
    <ref type="layout">portal/src/pages/AdvisorIntelligence/_partners/inflection/layout.ts (INFLV2.006)</ref>
  </references>
</task_order>
```
