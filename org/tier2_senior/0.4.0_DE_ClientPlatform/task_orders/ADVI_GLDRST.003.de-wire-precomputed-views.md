<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-003-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Wire the portal to consume pre-computed quarterly/monthly/annually
    period views at L2 (advisor) and L3 (relationship) levels, eliminating
    the client-side deriveQuarterlyFromTimeseries() function. After this,
    all drill levels (N1/L2/L3) use server-side pre-computed views from
    the same script (06b) and methodology.

    Also wire L3 composition to read pre-computed static artifacts
    instead of calling the Lambda handle_books_composition() on the fly.
  </objective>

  <context>
    Current state (DE session log 2026-03-26):
    - N1 Firm: reads gold/firm_mix_views.json (pre-computed, correct)
    - L2 Advisor: deriveQuarterlyFromTimeseries() from mix_timeseries.json
      (now alias-resolved to mix.json which has quarterly/monthly/annually views)
    - L3 Relationship: deriveQuarterlyFromTimeseries() from client_timeseries/{id}.json
      (~50KB daily JSON, 4 numbers extracted)
    - L3 Composition: Lambda handle_books_composition() computes on-the-fly (~3s)

    After DS completes GLDRST.001 and AE completes GLDRST.002:
    - L2: gold/advisors/{id}/mix.json already has views.quarterly/monthly/annually
    - L3: gold/client_timeseries/{id}_views.json will exist (same schema)
    - L3: gold/client_timeseries/{id}_composition.json will exist (same schema as firm)

    Key files:
    - portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx
    - portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx
    - portal/src/api/endpoints/advisor-intelligence.ts
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- WS1: L2 Advisor Mix Views (quarterly bar)                    -->
    <!-- ============================================================ -->
    <requirement id="1">
      WS1: Wire L2 quarterly bar to read advisor mix.json period views
      instead of deriving from daily timeseries.

      The advisor mix.json (served via handle_advisor_mix_views at
      /api/scoped/partners/books/advisor/{id}/mix-views) already has
      the exact shape the quarterly bar needs: views.quarterly[].

      Replace the L2 deriveQuarterlyFromTimeseries() path with a direct
      read of the advisor mix-views endpoint. This is the same pattern
      the N1 firm level already uses with getFirmMixViews().

      Add a getAdvisorMixViews(advisorId) API function if one doesn't
      already exist.
    </requirement>

    <!-- ============================================================ -->
    <!-- WS2: L3 Relationship Mix Views (quarterly bar)               -->
    <!-- ============================================================ -->
    <requirement id="2">
      WS2: Wire L3 quarterly bar to read relationship _views.json.

      After GLDRST.001 lands, each relationship will have:
        gold/client_timeseries/{relationship_id}_views.json

      Add a getRelationshipMixViews(relationshipId) API function that
      reads this artifact via CloudFront. Replace the L3
      deriveQuarterlyFromTimeseries() path.
    </requirement>

    <!-- ============================================================ -->
    <!-- WS3: L3 Relationship Composition (static artifact)           -->
    <!-- ============================================================ -->
    <requirement id="3">
      WS3: Wire L3 composition to read pre-computed artifact instead
      of calling the Lambda.

      After GLDRST.001 lands:
        gold/client_timeseries/{relationship_id}_composition.json

      Update getBooksRelationshipComposition() to read this static
      artifact via CloudFront. Fall back to the Lambda endpoint if
      the artifact is not found (graceful degradation during transition).
    </requirement>

    <!-- ============================================================ -->
    <!-- WS4: Remove deriveQuarterlyFromTimeseries()                  -->
    <!-- ============================================================ -->
    <requirement id="4">
      WS4: Once WS1 and WS2 are wired, remove deriveQuarterlyFromTimeseries()
      and all its call sites. This function should have zero references
      after L2 and L3 both read pre-computed views.

      If L4 (account) still needs it as a temporary measure, leave it
      but add a TODO comment referencing GLDRST L4 phase.
    </requirement>

    <requirement id="5">
      Write a session log at:
        org/tier2_senior/0.4.0_DE_ClientPlatform/logs/{date}/
          advi_gldrst_003_portal_precompute_wiring.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">L2 quarterly bar reads from advisor mix-views endpoint, not derived client-side</criterion>
    <criterion id="2">L3 quarterly bar reads from _views.json artifact, not derived client-side</criterion>
    <criterion id="3">L3 composition reads from static artifact with Lambda fallback</criterion>
    <criterion id="4">deriveQuarterlyFromTimeseries() removed or isolated to L4-only with TODO</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify gold scripts (DS scope)</constraint>
    <constraint>Do NOT modify Lambda code (AE/DT scope for Terraform deploy)</constraint>
    <constraint>Commits go to portal DEV branch</constraint>
    <constraint>Graceful fallback required for all new artifact reads (artifact may not exist during transition)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.001" status="pending">
      L3 _views.json and _composition.json artifacts must exist before WS2/WS3 can be verified
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_GLDRST.002" status="pending">
      Gold rerun must complete to populate all artifacts on S3
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal: L2+L3 quarterly bar wired to pre-computed views</deliverable>
    <deliverable type="commit">Portal: L3 composition wired to static artifact</deliverable>
    <deliverable type="commit">Portal: deriveQuarterlyFromTimeseries removed</deliverable>
    <deliverable type="document">Session log</deliverable>
  </deliverables>
  <tooling>
    <tool module="interpret.crossref_graph" when="before_coding">
      Run against portal/src/ to map which components import from which modules.
      Identify every file that calls deriveQuarterlyFromTimeseries() — these are the
      removal targets. The graph shows blast radius: removing the function breaks
      every component that imports it.
    </tool>

    <tool module="interpret.ast_extractor" when="before_coding">
      Extract TypeScript interface definitions and function signatures from types.ts
      and the tab components. Map the data flow: which interfaces define the quarterly
      view shape, which components consume it, which API calls fetch it.
    </tool>

    <tool module="adapt.differential_regression" when="after_coding">
      Diff the portal types.ts and component files against baseline. Verify: no
      interface fields removed that other components still reference, no orphaned
      imports after deriveQuarterlyFromTimeseries removal.
    </tool>
  </tooling>
</task_order>
