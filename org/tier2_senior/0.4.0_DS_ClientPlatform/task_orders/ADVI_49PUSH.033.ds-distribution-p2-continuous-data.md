<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-033-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>8</wave>
    <phase>Distribution P2 continuous data</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Extend platinum/firm/cumulative_chart.json (written by D_04) to support three
    data gaps needed by Distribution tab P2 continuous views: (1) new client count
    per period for GEO and ADV views, (2) city-level continuous NNA drill data,
    (3) advisor-level continuous drill data for ADV views.
    Companion DE TOs .034-.036 handle the frontend.

    PREREQUISITE: DS .027 step_0 geo_coverage_decision must be complete before
    building any P2 GEO-AUA continuous data. The grain choice (accounts vs relationships)
    for GEO-AUA must be consistent between P1 (snapshot) and P2 (continuous) views.
    Read .027 step_0 findings before proceeding.
  </objective>

  <context>
    The Distribution tab P2 (continuous) views all read from:
      platinum/firm/cumulative_chart.json → PlatinumCumulativeChartResponse
    Current schema (relevant fields):
      geo:             CumulativeChartView (AUA stacked area by state)
      adv:             CumulativeChartView (AUA stacked area by advisor)
      nna_geo:         NNASeriesView (NNA diverging bar by state)
      nna_adv:         NNASeriesView (NNA diverging bar by advisor)
      geo_drill?:      Record<string, CumulativeChartView> (state → city AUA)
      adv_drill?:      Record<string, CumulativeChartView> (advisor → client AUA)
      nna_geo_drill?:  NNAGeoDrillView (state → city NNA) -- check if populated

    GRAIN METHODOLOGY (approved 2026-04-09, same as .027 step_0):
      GEO-AUA continuous:  accounts IF geo_coverage_decision = A or C, else relationships
      GEO-NNA continuous:  ALWAYS accounts
      ADV-AUA continuous:  ALWAYS accounts
      ADV-NNA continuous:  ALWAYS accounts

    The grain used in the cumulative_chart.json data MUST match the grain used in the
    partner_analytics snapshot data (.027). If both use accounts, they tie.
    If GEO-AUA uses relationships in .027 but accounts here, they won't tie -- invalid.
    Apply the SAME geo_coverage_decision outcome to BOTH P1 and P2 GEO-AUA data.

    TYING RULE: All AUA figures shown anywhere in the Distribution tab must resolve to
    the same firm headline AUA when summed at the appropriate grain. Numbers that cannot
    be made to tie due to grain mismatch must be served from the same grain source.
    When in doubt: choose the grain that produces 100% coverage and document it.
  </context>

  <issue_1 label="New clients per period for all views">
    <description>
      All four P2 continuous views (GEO-AUA, GEO-NNA, ADV-AUA, ADV-NNA) need a
      "New Clients" box showing the count of new client relationships onboarded
      during the selected period/window.

      Definition: new clients = relationships whose first_seen_date falls within
      the selected time window (QTD, YTD, 1Y, etc.). This is the same definition
      used for the "new client assets" breakdown in the AUA view.

      Add to cumulative_chart.json at the firm level:
        new_clients_by_period: {
          quarterly: [ { period: "2026-Q1", label: "Q1 '26", count: N }, ... ],
          monthly:   [ { period: "2026-01", label: "Jan '26", count: N }, ... ],
          annually:  [ { period: "2026",    label: "2026",    count: N }, ... ]
        }
      The frontend will select the appropriate granularity array and derive the
      window total by summing counts within the active time window cutoff.

      Source: client_dimension.first_seen_date aggregated to period grain.
      This data is already available in D_00 (client dimension is loaded there).
      Add the aggregation to D_04's build_cumulative_chart() function.
    </description>
  </issue_1>

  <issue_2 label="City-level NNA continuous drill data">
    <description>
      The GEO-NNA continuous view needs a two-level drill:
        Level 0: firm aggregate NNA (already exists in nna_geo)
        Level 1: click state → state-level NNA continuous series (already in nna_geo per state)
        Level 2: click city → city-level NNA continuous series (MISSING)

      Check: does nna_geo_drill currently exist and is it populated in the platinum file?
      nna_geo_drill should be: Record<state_key, NNASeriesView_by_city>
        i.e. for each state, a NNASeriesView where categories are cities (not states).
        Each city series follows Top 9 + Other rule (same as P1-2 DS .027 issue_2).

      If nna_geo_drill is absent or empty: add it to D_04.build_cumulative_chart().
      Source: nna data from C_06/D_00 at city grain (client_timeseries or nna drill data).
      Check what city-level NNA data D_00 already produces (nna_drill_data with geo city
      columns). If available, aggregate to period grain and write per-state drill objects.

      Apply Top 9 + Other per state (same rule as DS .027 issue_2, consistent across P1/P2).
    </description>
  </issue_2>

  <issue_3 label="Advisor-level continuous drill data for ADV views">
    <description>
      P2-3 (ADV-AUA) and P2-4 (ADV-NNA) need two-level advisor drills:

      ADV-AUA drill:
        Level 0: firm AUA stacked by advisor (exists in adv)
        Level 1: advisor selected → that advisor's AUA continuous series over time
                 (single line/area, not stacked). Check if adv_drill is populated.
        Level 2: client selected → that client's AUA continuous series (pseudonymized)
                 This is a stretch goal -- flag if it would require significant new data.

      ADV-NNA drill:
        Level 0: firm NNA stacked by advisor (exists in nna_adv)
        Level 1: advisor selected → advisor NNA continuous series
        Level 2: client NNA continuous series (pseudonymized, stretch goal)

      For Level 1 ADV drill: check whether adv_drill and nna_adv_drill (if it exists)
      are populated. If adv_drill only has AUA and no NNA equivalent (nna_adv_drill),
      add nna_adv_drill: Record<advisor_id, NNASeriesView_by_client>.
      Apply Top 9 + Other to client entries within each advisor drill.
      Client names: pseudonymized per .032 rule.

      Level 2 client drill: if too data-intensive for initial release, skip and flag
      in session log. DE .036 will note it as a future enhancement.
    </description>
  </issue_3>

  <acceptance_criteria>
    1. cumulative_chart.json contains new_clients_by_period with quarterly/monthly/annually arrays
    2. nna_geo_drill populated: every state key maps to a city-level NNASeriesView (Top 9 + Other)
    3. adv_drill populated (Level 1 AUA by advisor confirmed or added)
    4. nna_adv_drill added: advisor key → NNASeriesView with client-level NNA
    5. All client entries in advisor drill data use pseudonymized display names
    6. Session log: Level 2 client drill status (implemented or deferred with reason)
    7. Notify DE via MCP inbox when data is ready (unblocks .034-.036)
  </acceptance_criteria>


  <compiler_tools>
    comp-pipescript io D_04
      -- Shows what cumulative_chart.json currently reads and what new fields need
         to be added for new_clients_by_period, nna_geo_drill, nna_adv_drill.
         Run first -- faster than reading D_04 top-to-bottom.

    comp-blast platinum/firm/cumulative_chart.json
      -- Shows all frontend components consuming cumulative_chart.json.
         Run before adding new fields to confirm no existing consumer will break
         on the expanded schema.

    comp-pipescript feeds nna_geo
      -- Traces what produces the nna_geo data currently flowing into cumulative_chart.
         Clarifies whether city-level NNA already exists somewhere upstream.
  </compiler_tools>

</task_order>
