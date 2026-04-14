<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-13-office-w3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>complete</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_OFFICE_PRD.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_OFFICE.W1.ds-d01-d00b-ofc-view"
                status="pending"
                description="DS D_01 + D_00b scripts committed and gold artifact live."/>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_OFFICE.W2.ae-dim-upload-gold-run"
                status="pending"
                description="AE gold run complete — OFC artifact live at platinum/ before DE starts visual testing."/>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_REBORN.W6-003.ds-d00c-role-combination-fee-breakdown"
                status="pending"
                description="W6-003 must ship first so types.ts edits here do not conflict with W6-004 types.ts edits. Pull latest before touching types.ts."/>
  </dependencies>

  <objective>
    Add OFC (Office) as a third cohort toggle in DistributionTab alongside GEO and ADV.
    Implement the full Snapshot AUA + NNA + Continuous AUA mode for OFC.
    No new API endpoints — OFC data is additive to existing `partner_analytics_{gran}.json`
    and `timeseries_chart.json` artifacts already consumed by DistributionTab.
  </objective>

  <context>
    PRD §6 (Frontend Implementation) is the authoritative spec. Summary of changes:

    TypeScript types (`types.ts`):
    - Add `OfficeAdvisorEntry` and `OfficeSegment` interfaces (PRD §6.1).
    - Extend `PartnerAnalyticsBaseView` to add `'ofc'`.
    - Extend `CumulativeChartViewMode` to add `'ofc'`.
    - Add optional `ofc?: NnaView` to `NnaPeriodView`.
    NOTE: W6-004 (ADVI_REBORN) will also touch types.ts. Pull latest CLOUD branch
    after W6-003 ships before editing types.ts here.

    DistributionTab.tsx changes (PRD §6.2):
    - `CohortOption = 'geo' | 'adv' | 'ofc'`
    - `COHORT_OPTIONS`: add `{ value: 'ofc', label: 'OFC' }`
    - `GrainView`: add `'ofc-aua' | 'ofc-nna'`
    - OFC palette: add `OFC_PALETTE` to `chartColors.ts` (10 visually-distinct colors,
      different from GEO_PALETTE and ADV_PALETTE)
    - Data access: `viewData` for OFC donut reads `currentSnapshot?.ofc`
      (note: comp-transform schema-check shows chartData is an alias/destructure of
      the PartnerAnalyticsResponse — apply the same access pattern as `adv`)
    - `nnaView` for OFC: `nnaData?.ofc`
    - Drill behavior: OFC L0 donut sliced by office; click → L1 advisor list (top 9 + Other);
      L1 is terminal (no further drill). Use `selectedOfficeKey` state (analogous to
      `selectedStateKey` for GEO / `selectedArchitectKey` for ADV).
    - Continuous AUA + OFC: read `cumulativeData?.ofc` (same structure as `cumulativeData?.adv`).
      analyticsData alias (comp-transform confirmed) is how cumulativeData is accessed — same pattern.
    - Center number override for OFC AUA: `ofc?.metrics?.aua ?? geo?.metrics?.aua`
    - `formatCohortLabel`: extend for OFC case with `formatOfficeLabel` (titleCase, underscores → spaces)
    - OFC L0 search: filter offices by name (analogous to GEO state search; max 10 offices so simple).

    Schema mismatch note from comp-transform schema-check (run 2026-04-13):
    - `chartData` at L658/L687/L859 and `analyticsData` at L606/L687/L841 are rendered
      but not defined in the TypeScript response types. These are destructured aliases
      from the response objects (runtime aliases, not type mismatches per se). Match the
      same access pattern used for GEO and ADV when adding OFC data access.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-transform schema-check DistributionTab` — confirm existing type/render map.
      Note existing `chartData` and `analyticsData` alias pattern.
    - `comp-cache collisions` — confirm no new React Query key conflicts (no new endpoints added).
    - Read `DistributionTab.tsx` L640-L720 to understand chartData/analyticsData destructuring.

    Phase 2 (before committing):
    - `comp-transform fields DistributionTab` — confirm all rendered `ofc.*` fields exist in types.
    - `bun run lint` from portal/ — zero new lint warnings.
    - `bun run build` (or `bunx tsc -b`) — zero TypeScript errors.
    - `/frontend-dev` visual test: OFC donut renders with office labels, legend populated,
      clicking an office shows advisor list, Continuous AUA + OFC shows stacked area chart.

    Phase 3 (after commit):
    - `comp-blast DistributionTab` — confirm blast radius unchanged (still 8 downstream nodes,
      4 endpoints, same opal-partners-data Lambda).
    - Append to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/pages/AdvisorIntelligence/types.ts</shared_resource>
    <shared_resource>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</shared_resource>
    <shared_resource>portal/src/lib/chartColors.ts</shared_resource>
    <also_in_to>ADVI_REBORN.W6-004 (DE — will touch AdvisorsTab.tsx + types.ts; NOT DistributionTab)</also_in_to>
    <required_action>
      Before editing types.ts: confirm W6-003 DS has shipped (pull latest CLOUD).
      Check `git log --oneline -5` before committing — if W6-004 is also in-flight
      on types.ts, coordinate via MCP before staging.
      DistributionTab.tsx and chartColors.ts have no other active TOs — safe to edit.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Three toggle buttons visible in DistributionTab header: [GEO] [ADV] [OFC].
    2. Selecting OFC renders office donut with labeled slices (Austin, Dallas, etc.).
    3. Clicking an office in Snapshot AUA mode → shows top-9 advisor list with AUA + account count.
    4. NNA mode + OFC → diverging bar chart renders per office (Snapshot and Continuous NNA).
    5. Continuous AUA + OFC → stacked area chart renders office categories (reads `cumulativeData?.ofc`).
    6. TypeScript build clean (`bun run build` zero errors).
    7. Zero new lint warnings (`bun run lint`).
    8. `/frontend-dev` visual test passed: OFC donut renders, legend populated, no layout overflow,
       Continuous view switches correctly.
    9. OFC donut center number uses firm headline AUA (same override pattern as ADV .030).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/lib/chartColors.ts</file>
    </files>
    <out_of_scope>
      advisor-intelligence.ts (no endpoint changes needed — OFC data additive to existing artifact).
      AdvisorsTab.tsx (ADVI_REBORN.W6-004 scope).
      Backend scripts (DS W1 scope).
    </out_of_scope>
  </scope>

  <deliverables>
    - Commit to portal DEV with DE author.
    - Session log with compiler tools section + visual test result.
    - MCP message to 2.0.0_SA_COO: "ADVI_OFFICE W3 complete — OFC frontend on portal DEV."
  </deliverables>
</task_order>
