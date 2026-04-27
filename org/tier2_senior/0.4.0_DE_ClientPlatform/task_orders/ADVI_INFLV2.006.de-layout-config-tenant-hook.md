# Task Order: ADVI_INFLV2.006 — DE: Per-Firm Layout Config + useTenantLayout Hook

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-006</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <priority>HIGH — start immediately (no gate). Foundation for .007 + .008.</priority>
  </metadata>

  <objective>
    Introduce the per-firm layout config pattern for the AdvisorIntelligence portal.
    Two scattered `firmId === 'inflection'` checks already exist in shared tab components;
    more are imminent (Advisors-tab kill, advisor-list cap, Revenue Ops panel swap,
    AdvisorPublicProfile redirect). Adding more inline gates without a config layer
    guarantees a refactor on partner #3. Build the config layer now.

    Deliverable: `_partners/{firmId}/layout.ts` + `useTenantLayout()` hook +
    migration of two existing scattered checks.
  </objective>

  <scope>
    <task id="1" label="Define TenantLayoutConfig type">
      Create:
        portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts

      Type shape per PRD §5.2:
        export interface TenantLayoutConfig {
          tabs: {
            partnerAnalytics: { enabled: boolean };
            distribution: {
              enabled: boolean;
              cohorts: { geo: 'enabled' | 'stub' | 'disabled'; adv: 'enabled' | 'stub' | 'disabled'; ofc: 'enabled' | 'stub' | 'disabled' };
              stubMessage?: Record<string, string>;
            };
            books: {
              enabled: boolean;
              advisorDrill: { enabled: boolean };
              revenueOpsPanel: 'standard' | 'inflection_insights' | 'suppressed';
            };
            advisors: { enabled: boolean };
          };
          panels: {
            advisorList: { maxEntries: number; allowedAdvisorKeys: string[] };
            advisorPublicProfile: { enabled: boolean };
          };
        }
    </task>

    <task id="2" label="Implement useTenantLayout() hook">
      Create:
        portal/src/pages/AdvisorIntelligence/_shared/hooks/useTenantLayout.ts

      Hook reads current firmId from context (same source as existing firmId usage),
      looks up the layout config, and returns it. Falls back to a DEFAULT_LAYOUT
      (all enabled, standard panels) for unknown firmIds to ensure backwards compat
      for 49F and future partners.

      DEFAULT_LAYOUT: all tabs enabled, cohorts all 'enabled', advisorDrill enabled,
      revenueOpsPanel 'standard', no advisorList cap, advisorPublicProfile enabled.
    </task>

    <task id="3" label="Author Inflection layout config">
      Create:
        portal/src/pages/AdvisorIntelligence/_partners/inflection/layout.ts

      Per PRD §5.2:
        export const INFLECTION_LAYOUT: TenantLayoutConfig = {
          tabs: {
            partnerAnalytics: { enabled: true },
            distribution: {
              enabled: true,
              cohorts: { geo: 'stub', adv: 'enabled', ofc: 'disabled' },
              stubMessage: { geo: 'Geographic data pending Fidelity enrichment.' },
            },
            books: {
              enabled: true,
              advisorDrill: { enabled: false },
              revenueOpsPanel: 'inflection_insights',
            },
            advisors: { enabled: false },
          },
          panels: {
            advisorList: {
              maxEntries: 3,
              allowedAdvisorKeys: ['inflection_wealth_management', 'peter_lee', 'patrick_scanlan'],
            },
            advisorPublicProfile: { enabled: false },
          },
        };
    </task>

    <task id="4" label="Register Inflection layout in hook">
      Wire useTenantLayout() to return INFLECTION_LAYOUT when firmId === 'inflection'.
      Map should be extensible (Record or switch) so future partners add one entry.
    </task>

    <task id="5" label="Migrate existing scattered checks">
      Replace existing literal `firmId === 'inflection'` checks with useTenantLayout() reads:

      1. portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx
         lines 661-662 (cohort dropdown filtering + auto-reset on firm change)
         → read layout.tabs.distribution.cohorts, render geo as stub when cohorts.geo === 'stub'

      2. portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx
         line 577 (hideFeeEfficiency prop → revenueOpsPanel check)
         → read layout.tabs.books.revenueOpsPanel; hide FeeEfficiencyPanel when
           revenueOpsPanel !== 'standard'

      Do NOT yet implement the INFLV2.007/008 changes (BooksTab advisor-drill suppression,
      Advisors tab kill, InflectionInsightsPanel slot) — those are gated on .005 + .006.
      This TO only migrates the two existing checks.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      TenantLayoutConfig type defined. useTenantLayout() hook returns INFLECTION_LAYOUT
      for firmId=inflection and DEFAULT_LAYOUT for any unknown firmId.
    </criterion>
    <criterion id="2">
      49F behavior unchanged: all tabs enabled, cohorts all enabled, standard revenue ops
      panel, no advisor-list cap. Regression: existing 49F smoke (any passing RD test)
      still passes.
    </criterion>
    <criterion id="3">
      Two existing scattered firmId checks migrated to useTenantLayout() reads.
      No remaining literal `firmId === 'inflection'` strings in DistributionTab.tsx
      or ClientsTab.tsx for these two features.
    </criterion>
    <criterion id="4">
      Portal builds cleanly: bun run dev --port 5175 starts without TypeScript errors.
    </criterion>
    <criterion id="5">
      Commit uses DEV branch (portal submodule) with portal-v2.1.X tag increment.
      Author: 0.4.0_DE_ClientPlatform.
    </criterion>
    <criterion id="6">
      RAVC sent to 2.0.0_SA_COO confirming hook + config live. Subject:
      RAVC — ADVI_INFLV2.006 COMPLETE | useTenantLayout live | 2 checks migrated | portal-v[X]
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT add new Inflection-specific feature implementations in this TO
    beyond migrating the two existing checks. Features are .007 + .008.</constraint>
    <constraint>DEFAULT_LAYOUT must be backwards-compatible — 49F must see no behavioral
    change from this PR.</constraint>
    <constraint>No emojis in code.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="none"
                note="No gate — start immediately."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">TenantLayoutConfig type + useTenantLayout hook +
    INFLECTION_LAYOUT config + 2 migrated checks. Portal DEV branch.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO. This is the go-signal gate for
    INFLV2.007 + INFLV2.008.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §5 (architectural pattern)</ref>
    <ref type="existing-checks">portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx:661-662</ref>
    <ref type="existing-checks">portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx:577</ref>
  </references>
</task_order>
```
