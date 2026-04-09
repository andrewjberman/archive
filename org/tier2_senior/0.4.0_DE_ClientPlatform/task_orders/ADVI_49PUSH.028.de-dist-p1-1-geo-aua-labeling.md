<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-028-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>complete -- helpers + grain wiring shipped (f2e7eca + prior); OPTION A (accounts) confirmed by DS~D. Validation blocked on AE D_01+D_04 re-run.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>7</wave>
    <phase>Distribution P1-1</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P1-1: Snapshot-GEO-AUA view is correct as-is but needs a labeling
    clarification enforced in code. Establish the universal rule for the Distribution tab:
    radial (donut) always shows CLIENT count (relationships), bell curve always shows
    ACCOUNT count. Verify and fix if either chart is currently using the wrong count.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx

    GRAIN METHODOLOGY (approved 2026-04-09):
      GEO-AUA radial:  accounts OR relationships -- depends on DS .027 step_0 decision
      GEO-NNA radial:  always accounts
      ADV-AUA radial:  always accounts
      ADV-NNA radial:  always accounts
      Bell curve:      always accounts across ALL views regardless of radial grain

    DE must read DS .027 step_0 findings before finalizing this TO.
    DS will post the geo_coverage_decision (Option A, B, or C) to the DE inbox.
    The count field wiring and subtext labels depend on that outcome.

    Universal radial/bell split: the radial and bell curve NEVER use the same
    count field as each other when GEO-AUA is relationship-grain. The bell curve
    is ALWAYS accounts. This means for GEO-AUA Option B (relationships):
      Radial: relationship_count, labeled "Clients"
      Bell:   account_count,      labeled "Accounts"
    For all other views and for GEO-AUA Option A/C (accounts):
      Both radial and bell use account_count, but labeled differently:
      Radial: account_count labeled "Accounts" in subtext
      Bell:   account_count on the distribution axis (unlabeled or "Accounts")
  </context>

  <fix_1 label="Implement grain-aware count selection">
    <description>
      Build a centralized count-selection helper that all 8 Distribution views use:

        getRadialCount(segment, view: 'geo-aua' | 'geo-nna' | 'adv-aua' | 'adv-nna',
                       geoAuaGrain: 'accounts' | 'relationships'): number
          - geo-aua + relationships: return segment.relationship_count ?? segment.client_count
          - all others:              return segment.account_count

        getRadialLabel(view, geoAuaGrain): string
          - geo-aua + relationships: "Clients"
          - all others:              "Accounts"

        getBellCount(segment): number
          - always: segment.account_count  (bell curve is always accounts)

      geoAuaGrain is a prop/constant derived from the platinum data itself:
      DS .027 will add a top-level field to the partner_analytics JSON:
        geo_aua_grain: "accounts" | "relationships"
      DE reads this field from analyticsData and passes it through to all views.
      This way the frontend never hardcodes the grain -- it always follows the data.
    </description>
  </fix_1>

  <fix_2 label="Subtext label enforcement based on grain">
    <description>
      Snapshot radial segment subtext (P1 views only):

      IF geo_aua_grain === 'relationships' AND view === 'geo-aua':
        State-level segments:
          Line 1: "{N} Clients"
          Line 2: "{X.X}% of firm clients"  (% of all firm relationships)
        City-level segments (drilldown):
          Line 1: "{N} Clients"
          Line 2: "{X.X}% of {state} clients"  (% of parent state's relationships)

      ALL other views (GEO-NNA, ADV-AUA, ADV-NNA) and GEO-AUA when grain = accounts:
        Line 1: "{N} Accounts"
        Line 2: "{X.X}% of firm accounts"  (state level)
                "{X.X}% of {state} accounts"  (city drilldown level)
                "{X.X}% of firm accounts"  (advisor level, ADV views)
                "{X.X}% of {advisor} accounts"  (client drilldown level, ADV)

      "Other" segment subtext: same format but count = all non-top-9 entities.
      Do not use "relationships" in user-facing text. "Clients" is the correct term.
    </description>
  </fix_2>

  <acceptance_criteria>
    1. geo_aua_grain field read from analyticsData and propagated to all views as a prop
    2. getRadialCount / getRadialLabel / getBellCount helpers centralized and shared
    3. Subtext labeling matches grain: "Clients" for relationship grain, "Accounts" for account grain
    4. City drilldown subtext uses section % (parent state), not global % (firm)
    5. Bell curve always uses account_count regardless of view or grain
    6. No visible regression in GEO-AUA if it was already correct
    7. Build clean, no TypeScript errors
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check DistributionTab
      -- Run BEFORE and AFTER. The before-run shows the current UNUSED fields and
         which fields are being rendered. The after-run confirms relationship_count
         and account_count are both wired correctly and no field became orphaned.
         This catches the "right type, wrong field name" class of error instantly.

    comp-transform fields DistributionTab
      -- Shows every field rendered by DistributionTab and the source it comes from.
         Use this to confirm the getRadialCount / getBellCount helpers are routing
         to the correct platinum fields after the geo_aua_grain branch is added.
  </compiler_tools>

</task_order>
