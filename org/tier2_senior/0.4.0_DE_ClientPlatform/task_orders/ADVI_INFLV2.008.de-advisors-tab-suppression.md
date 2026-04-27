# Task Order: ADVI_INFLV2.008 — DE: AdvisorsTab + AdvisorPublicProfile Suppression

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-008</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — gates INFLV2.010 (RD smoke)</priority>
  </metadata>

  <objective>
    Andrew direction: "Advisors tab as a whole doesnt make sense for Inflection."
    DROP AdvisorsTab from nav for firmId=inflection. Also suppress AdvisorPublicProfile
    non-admin path. Both driven by useTenantLayout() config from INFLV2.006.
  </objective>

  <scope>
    <task id="1" label="AdvisorsTab nav suppression">
      In the tab navigation component (index.tsx or equivalent):
        - Read layout.tabs.advisors.enabled from useTenantLayout()
        - When enabled === false: do NOT render AdvisorsTab nav entry
        - The tab is removed from navigation, not redirected or error-paged
        - 49F: tabs.advisors.enabled === true → Advisors tab still present
    </task>

    <task id="2" label="AdvisorPublicProfile non-admin suppression">
      Per layout.panels.advisorPublicProfile.enabled from useTenantLayout():
        - When enabled === false: suppress the non-admin AdvisorPublicProfile path
          for Inflection (firm dashboard redirect or appropriate empty-state)
        - DE chooses the exact redirect/suppression mechanism; document in commit
        - 49F: advisorPublicProfile.enabled === true → existing behavior unchanged
    </task>

    <task id="3" label="Regression: 49F Advisors tab unchanged">
      Verify 49F Advisors tab still renders fully. No suppression bleeds over.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      firmId=inflection: AdvisorsTab nav entry absent from tab bar.
    </criterion>
    <criterion id="2">
      firmId=inflection: AdvisorPublicProfile non-admin path suppressed (no visible entry).
    </criterion>
    <criterion id="3">
      firmId=49financial: Advisors tab fully present. No regression.
    </criterion>
    <criterion id="4">
      No new literal `firmId === 'inflection'` strings — all through useTenantLayout().
    </criterion>
    <criterion id="5">
      Portal builds cleanly. No TypeScript errors.
    </criterion>
    <criterion id="6">
      RAVC to 2.0.0_SA_COO.
      Subject: RAVC — ADVI_INFLV2.008 COMPLETE | AdvisorsTab suppressed | portal-v[X]
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gate: INFLV2.006 COMPLETE (useTenantLayout hook must be live).</constraint>
    <constraint>DROP = removed from nav. Not redirect-to-error, not hidden-but-reachable.
    No route should render the AdvisorsTab for firmId=inflection.</constraint>
    <constraint>No emojis in code.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_INFLV2.006"
                status="open"
                note="useTenantLayout hook must exist and return INFLECTION_LAYOUT
                with tabs.advisors.enabled === false."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Tab nav component + AdvisorPublicProfile suppression. Portal DEV branch.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §3 + §8</ref>
    <ref type="nav">portal/src/pages/AdvisorIntelligence/index.tsx (tab navigation)</ref>
    <ref type="layout">portal/src/pages/AdvisorIntelligence/_partners/inflection/layout.ts (INFLV2.006)</ref>
  </references>
</task_order>
```
