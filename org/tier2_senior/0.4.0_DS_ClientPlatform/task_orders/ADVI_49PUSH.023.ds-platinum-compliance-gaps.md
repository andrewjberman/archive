<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-023-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>6</wave>
    <phase>P3 compliance</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Extend D_04.client_portal_summary.py to publish all remaining platinum/ files
    required to eliminate the 8 frontend gold/ reads identified in the compliance audit.
    After this TO, every advisor-intelligence.ts endpoint must resolve to a platinum/ path.
    D_04 is the only writer of platinum/ -- no gold/ or silver/ reads from the portal.
  </objective>

  <context>
    A compliance audit of advisor-intelligence.ts identified 8 endpoints still reading
    directly from gold/ or silver/ paths. The goal of ADVI_49PUSH is "D_04 only feeds
    the portal" -- these are violations. D_04 already reads most of the source files;
    the missing step is publishing them into platinum/.

    Audit results (violations):

    | Endpoint                        | Current path                                         | D_04 already reads? |
    |---------------------------------|------------------------------------------------------|---------------------|
    | getHeaderSummary (L217,232)     | artifacts/summary/header_metrics.json (D_00)         | NO -- new read req  |
    | getPartnerAnalyticsHeader (L254)| artifacts/partner_analytics/header_metrics_{s}.json  | YES (pass-through)  |
    | getTimeseriesChart (L270)       | artifacts/timeseries_chart.json (D_00)               | YES (missing write) |
    | getClientViews (L555)           | entities/clients/{relId}_views.json (external/silver)| NO -- new read req  |
    | getClientComposition (L569)     | entities/clients/{relId}_composition.json (silver)   | YES (missing write) |
    | getAdvisorFeeEfficiency (L596)  | artifacts/advisor_fee_efficiency.json (C_08)         | YES -- already done |
    | getEmployeeLeaderboard (L613)   | artifacts/employee_leaderboard.json (D_00)           | YES (missing write) |
    | advisor mix Lambda (L534)       | gold/entities/advisors/{id}/mix.json (D_03)          | YES (missing write) |

    Note: platinum/firm/fee_efficiency.json is already written by D_04. getAdvisorFeeEfficiency
    just needs a frontend switch (separate DE TO). No D_04 change needed for that one.

    Note: getPartnerAnalyticsHeader (legacy endpoint) already has a platinum counterpart
    (platinum/firm/partner_analytics_{suffix}.json). The legacy gold endpoint should be
    DELETED from advisor-intelligence.ts by DE -- no new D_04 file needed.

    So the actual D_04 changes required are 5 new platinum publishers + 2 new source reads.
  </context>

  <deliverables>

    <deliverable id="1">
      <title>platinum/firm/header_metrics.json</title>
      <description>
        New read + pass-through publish.
        Source: gold/artifacts/summary/header_metrics.json (written by D_00).
        Target: platinum/firm/header_metrics.json
        Content: pass the full D_00 object through unchanged. Do not reshape.
        This feeds getHeaderSummary (the top-of-page AUA / NNA / client count metrics bar).
      </description>
    </deliverable>

    <deliverable id="2">
      <title>platinum/firm/timeseries_chart.json</title>
      <description>
        D_04 already reads TIMESERIES_CHART (gold/artifacts/timeseries_chart.json).
        Add a platinum write: platinum/firm/timeseries_chart.json.
        Content: pass the full D_00 object through unchanged.
        This feeds getTimeseriesChart (AUA/NNA time series on the header).
      </description>
    </deliverable>

    <deliverable id="3">
      <title>platinum/firm/employee_leaderboard.json</title>
      <description>
        D_04 already reads EMPLOYEE_LEADERBOARD (gold/artifacts/employee_leaderboard.json).
        Add a platinum write: platinum/firm/employee_leaderboard.json.
        Content: pass the full D_00 object through unchanged.
        This feeds getEmployeeLeaderboard (the firm-wide employee leaderboard table).
      </description>
    </deliverable>

    <deliverable id="4">
      <title>platinum/advisors/{id}/mix.json (per-advisor)</title>
      <description>
        D_04 already reads advisor_mix_key (gold/entities/advisors/{id}/mix.json, written by D_03).
        For every advisor that has a mix.json in gold/entities/advisors/, write a copy to
        platinum/advisors/{id}/mix.json.
        Content: pass the D_03 object through unchanged.
        This feeds the advisor mix Lambda (currently reads gold/entities/advisors/{id}/mix.json directly).
      </description>
    </deliverable>

    <deliverable id="5">
      <title>platinum/clients/{id}/views.json (per-client)</title>
      <description>
        New read + per-client publish.
        Source: gold/entities/clients/{relId}_views.json (external/silver writer).
        Note: the key pattern uses underscore suffix, not directory: {relId}_views.json.
        For every client that has a _views.json in gold/entities/clients/, write a copy to
        platinum/clients/{relId}/views.json (normalize to directory format for consistency).
        Content: pass through unchanged.
        This feeds getClientViews (client detail panel: views/engagement data).
      </description>
    </deliverable>

    <deliverable id="6">
      <title>platinum/clients/{id}/composition.json (per-client)</title>
      <description>
        D_04 already reads client_composition_key (gold/entities/clients/{relId}_composition.json).
        It currently writes platinum/clients/{id}/concentration.json and mix_timeseries.json
        but NOT a raw composition pass-through.
        Add a write: platinum/clients/{relId}/composition.json.
        Content: pass the silver composition object through unchanged.
        This feeds getClientComposition (client portfolio composition breakdown).
      </description>
    </deliverable>

  </deliverables>

  <compliance_notes>
    After this TO is complete and AE deploys + re-runs D_04:
    - DE will switch the 6 corresponding frontend endpoints to platinum/ paths (.024 companion TO)
    - DE will delete getPartnerAnalyticsHeader legacy endpoint (already has platinum counterpart)
    - DE will switch getAdvisorFeeEfficiency to platinum/firm/fee_efficiency.json (already written by D_04)
    - Result: 0 gold/ or silver/ reads from advisor-intelligence.ts

    Do NOT restructure or reshape any of the pass-through objects. The frontend TypeScript
    types were written against the existing gold/ schemas. Shape changes = DE type changes
    (a separate workstream). Pass through verbatim.

    After writing, run validate_platinum_consistency.py (once .009 is complete) or spot-check
    a sample of each new file type from S3 before declaring done.
  </compliance_notes>

  <acceptance_criteria>
    1. D_04 writes platinum/firm/header_metrics.json on every full run
    2. D_04 writes platinum/firm/timeseries_chart.json on every full run
    3. D_04 writes platinum/firm/employee_leaderboard.json on every full run
    4. D_04 writes platinum/advisors/{id}/mix.json for every advisor with a gold mix.json
    5. D_04 writes platinum/clients/{id}/views.json for every client with a gold _views.json
    6. D_04 writes platinum/clients/{id}/composition.json for every client with a gold _composition.json
    7. All 6 files exist in S3 after AE re-runs D_04
    8. Spot-check: sample 5 advisors and 5 clients -- platinum file content matches gold source
    9. No changes to existing platinum/ publishers or to gold/ read logic for other scripts
  </acceptance_criteria>


  <compiler_tools>
    Run these BEFORE writing any code to avoid redundant manual tracing:

    comp-pipescript io D_04
      -- Confirms the current read/write manifest for D_04. Tells you exactly what paths
         D_04 already reads before you add new ones. Authoritative -- faster than grepping.

    comp-blast platinum/firm/dashboard.json
      -- Shows all frontend components that depend on D_04's existing platinum outputs.
         Run before touching any existing D_04 publisher to check blast radius.

    comp-pipescript chain D_04
      -- Confirms D_04's position in gold_dispatch.sh chain so new publishers run at
         the right time relative to D_00/D_01/D_02/D_03.
  </compiler_tools>

</task_order>
