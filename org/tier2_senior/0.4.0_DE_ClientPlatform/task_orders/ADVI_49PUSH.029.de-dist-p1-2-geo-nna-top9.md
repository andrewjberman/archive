<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-029-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>complete -- enforceTop9Other applied to ALL geo-city snapshot branches (2e94a2c). Data validation blocked on AE D_01+D_04 re-run.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>7</wave>
    <phase>Distribution P1-2</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P1-2: Fix Snapshot-GEO-NNA city-level drilldown to enforce the
    Top 9 + Other rule. Currently cities are displayed individually without grouping,
    violating the standard applied everywhere else in the portal.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    The GEO-NNA snapshot shows state-level NNA distribution in the radial.
    Drilling into a state shows city-level NNA. Andrew confirmed this drilldown does not
    apply the Top 9 + Other rule -- all cities are shown individually.

    The CITY_COLORS palette (line ~174) already supports 9 cities + gray Other.
    DS .027 issue_2 will fix the platinum data to pre-group cities as top 9 + Other.
    This TO handles the frontend enforcement and any residual grouping needed in the UI.
  </context>

  <fix_1 label="Enforce Top 9 + Other for city NNA drilldown">
    <description>
      After DS .027 ships, the platinum city-drill NNA data will be pre-grouped as
      top 9 + Other per state. However, DE must also add a client-side enforcement guard:

      When rendering the city-level NNA drilldown segments, if the data contains more
      than 10 entries (9 named + Other), apply grouping in the UI as a safety net:
        1. Sort by absolute NNA descending
        2. Keep first 9 as named segments
        3. Sum all remaining into an "Other" entry
      This guard ensures correctness even if the platinum data is not yet regrouped or
      if a future DS run accidentally emits ungrouped data.

      The "Other" segment key must be exactly "Other" (matches CITY_COLORS and the existing
      OTHER_COLOR logic at line ~193 in the file).

      Apply this same guard to ALL city-level and state-level drilldowns across the
      Distribution tab for both snapshot and continuous views (not just GEO-NNA P1-2).
      This is the universal rule -- build it as a shared utility function:
        enforceTop9Other(segments: Segment[], valueKey: string): Segment[]
      Call it before rendering any drilldown segment list.
    </description>
  </fix_1>

  <fix_2 label="Radial = Clients, Bell = Accounts (apply universal rule)">
    <description>
      Apply the same radial/bell count rule from .028 to the GEO-NNA view.
      Confirm the city-level NNA radial shows relationship_count per city (Clients),
      and the bell curve shows account_count (Accounts).
    </description>
  </fix_2>

  <acceptance_criteria>
    1. City-level GEO-NNA drilldown shows at most 10 segments (top 9 + Other)
    2. "Other" uses the correct gray color from CITY_COLORS
    3. enforceTop9Other utility is shared and reusable across all drilldown views
    4. Radial uses Clients count, bell curve uses Accounts count
    5. Build clean, no TypeScript errors
    6. Visual: drill into CA or TX (states likely to have >9 cities), confirm grouping
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check DistributionTab
      -- Run after adding enforceTop9Other. Confirms the city drill segments still
         map to their typed fields and the "Other" entry doesn't introduce a
         type mismatch.

    comp-cache collisions
      -- Run after adding any new React Query keys for the city drill data.
         Detects if the new drill key collides with an existing snapshot key
         and would serve stale data.
  </compiler_tools>

</task_order>
