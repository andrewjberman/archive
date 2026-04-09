<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-027-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>7</wave>
    <phase>Distribution P1 snapshot data</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Audit and fix the platinum partner_analytics snapshot data to support four corrected
    Distribution tab P1 snapshot views. Covers data-side issues only -- companion DE TOs
    .028-.031 handle the frontend. All fixes go into D_04's partner_analytics publisher
    and/or the relevant gold scripts that feed it.

    PREREQUISITE: Complete the grain methodology investigation (step_0 below) before
    writing any platinum data. The outcome determines the asset-value grain for GEO-AUA
    and controls subtext labeling across all P1 snapshot views. Post findings to CTO inbox
    before proceeding to issues 1-4.
  </objective>

  <context>
    The Distribution tab snapshot views read from platinum/firm/partner_analytics_{suffix}.json
    (written by D_04, sourced from D_01 partner_analytics gold artifacts).
    The four P1 views are: GEO-AUA, GEO-NNA, ADV-AUA, ADV-NNA.
    The frontend accesses these as analyticsData?.views?.geo and analyticsData?.views?.adv.

    Four data issues have been identified across the P1 views, described below.
    All are preceded by the mandatory grain methodology investigation in step_0.
  </context>

  <step_0 label="PREREQUISITE: Grain methodology investigation -- do this first">
    <description>
      The numbers shown across all four Distribution views MUST be internally consistent.
      We cannot mix relationship-grain and account-grain values within the same calculation,
      or show AUA from one grain alongside NNA from another grain without them tying.

      Approved methodology matrix (Andrew, 2026-04-09):
        GEO-AUA:  CONDITIONAL -- see geo_coverage_decision below
        GEO-NNA:  ALWAYS accounts (never relationships)
        ADV-AUA:  ALWAYS accounts
        ADV-NNA:  ALWAYS accounts

      The ONLY open question is GEO-AUA. The reason it may need to be relationships:
      state/city geographic data may not be consistently available at account level.
      If we lack account-level geo, we must aggregate up to relationship level to get
      complete geographic coverage.

      geo_coverage_decision:
        DS must answer: for account_performance.parquet (C_03), what percentage of
        account rows have a resolvable state AND city (from client_state, client_country,
        or a join to accounts_dimension/client_dimension)?

        Query: for the latest date in account_performance, count rows with non-null state.
               coverage = non_null_state_rows / total_rows * 100

        OPTION A -- account coverage >= 99.5%:
          Use accounts for GEO-AUA. All four views use accounts. Maximum consistency.
          GEO-AUA subtext (snapshot radial): "X Accounts" + "Y% of firm accounts"
          This is the preferred outcome.

        OPTION B -- account coverage < 99.5%:
          Check relationship-level coverage: for client_performance or client_dimension,
          what % of relationships have a resolvable state?
          If relationship coverage >= 99.5%: use relationships for GEO-AUA.
          If relationship coverage also < 99.5%: escalate to CTO -- geo data is too sparse
          for a geographic view and we need a different approach.

        OPTION C -- account coverage < 99.5% but enrichable:
          If account-level geo data is <99.5% but we can enrich accounts from the
          relationship-level geo (join account → relationship → state/city), and that
          join achieves >= 99.5% coverage: use the enriched account figures.
          This gives account consistency across all 4 views.

      Document the coverage numbers and which option applies.
      Post to CTO inbox BEFORE writing any platinum data for this TO.
    </description>

    <subtext_rule label="Snapshot radial subtext -- depends on geo_coverage_decision outcome">
      This rule applies ONLY to the snapshot radial (P1 views) subtext per segment.
      The bell curve is ALWAYS accounts regardless of the geo_coverage_decision.

      IF geo_coverage_decision = OPTION A or C (accounts for GEO-AUA):
        GEO-AUA radial subtext per segment (state or city):
          Line 1: "{N} Accounts"
          Line 2: "{X.X}% of firm accounts"
        All other views (GEO-NNA, ADV-AUA, ADV-NNA) also use accounts -- consistent.

      IF geo_coverage_decision = OPTION B (relationships for GEO-AUA):
        GEO-AUA radial subtext per segment (state or city):
          Line 1: "{N} Clients"
          Line 2: "{X.X}% of [section/global] clients"
          -- "section clients" = clients within the parent geographic unit
             (e.g. for a city segment: % of that state's clients, not all firm clients)
          -- "global clients" = % of all firm clients (for state-level segments)
          The distinction: state-level segments use % of firm. City-level segments
          (drilldown) use % of that state's client total (section), not firm total.
          This makes the percentages meaningful at each drill level.

      GEO-NNA, ADV-AUA, ADV-NNA radial subtext: ALWAYS accounts.
        Line 1: "{N} Accounts"
        Line 2: "{X.X}% of firm accounts" (or advisor's accounts for ADV drill)

      DS must add the correct count and percentage fields to each platinum segment
      based on the geo_coverage_decision outcome. Both relationship_count AND account_count
      should be present in all segments regardless of which is displayed (DE needs both
      for the bell curve / radial split), but the PRIMARY count driving the AUA
      aggregation must match the geo_coverage_decision.

      DS must also add a top-level field to partner_analytics JSON:
        geo_aua_grain: "accounts" | "relationships"
      Set this to whichever option was chosen. DE reads this field to dynamically select
      the correct count field and label -- it never hardcodes the grain in the frontend.
      This field must also be added to cumulative_chart.json (for P2 continuous views)
      with the same value, so DE .034-.036 can consume it consistently.
    </subtext_rule>
  </step_0>

  <issue_1 label="P1-1 GEO-AUA: relationship_count vs account_count clarity">
    <description>
      The radial (donut) must display CLIENT count (relationships). The bell curve must
      display ACCOUNT count. Verify that the GEO-AUA snapshot data provides BOTH:
        relationship_count (or client_count): unique relationships per state/city segment
        account_count: unique accounts per state/city segment
      Check the snapshot segment schema in platinum/firm/partner_analytics_snap.json
      (or the current snapshot suffix file). If only one count is provided, add the missing one.
      The types.ts already has relationship_count?: number and account_count: number --
      DS must ensure both fields are populated per segment in the platinum output.
    </description>
  </issue_1>

  <issue_2 label="P1-2 GEO-NNA: city-level drilldown must follow Top 9 + Other rule">
    <description>
      The city-level drilldown in the GEO-NNA snapshot currently serves ALL cities individually
      without applying the Top 9 + Other grouping. This violates the standard rule applied
      everywhere else in the portal.

      Fix in D_04 (or the gold script that produces city-level NNA data):
        For each state's city-level NNA drill data, rank cities by absolute NNA value
        (descending). Keep top 9. All remaining cities are aggregated into a single
        "Other" entry with summed NNA.
      The "Other" entry must use the key "Other" (matching existing CITY_COLORS map).
      Apply to both positive and negative NNA periods -- rank by absolute value, not signed.
      If fewer than 9 cities exist for a state, no "Other" entry is needed.

      Verify: for a state with >9 cities (e.g. CA or TX), confirm the platinum city drill
      data has exactly 10 entries (9 named + Other).
    </description>
  </issue_2>

  <issue_3 label="P1-3 ADV-AUA: all-role coverage, center total, relationship counts">
    <description>
      Three sub-issues for the ADV-AUA snapshot:

      3a. Advisor ranking must cover ALL roles (architect/implementor/consultant/local_ops),
          not just architects. Rank by total tagged AUA -- the sum of AUA for all accounts
          where the advisor appears in any role. Since advisors can share accounts across roles,
          this is NOT a sum that should aggregate to firm AUA. It is simply: for each advisor,
          what is the total AUA of all accounts they are tagged to in any capacity?
          Check whether the current ADV-AUA snapshot already reflects multi-role coverage
          (it should, given D_02 multi-role fix in .006). If not, fix the D_04 publisher.
          Top 9 = top 9 advisors by tagged AUA. "Other" = all remaining advisors aggregated.

      3b. Center radial "Total AUA" value must equal the firm headline AUA as displayed in
          the Assets Overview header panel. This is NOT the sum of advisor tagged AUAs
          (that sum is meaningless and will exceed firm AUA due to multi-role overlap).
          The correct source is: the same firm-level total_aua used in the header metrics.
          Verify that the ADV-AUA snapshot's center/total field points to this value.
          If it is currently summing advisor AUAs, fix it to use firm headline AUA directly
          (read from D_00 header_metrics or from the firm-level platinum dashboard).

      3c. Per-advisor subtext must carry:
            relationship_count: number of unique client relationships the advisor is tagged
                                to across all roles (count distinct relationship_id where
                                advisor appears in any role column in account_team)
            pct_of_firm_clients: relationship_count / firm_total_relationships * 100
          "Other" subtext: relationship_count = count of all relationships NOT represented
          by any of the top 9 advisors in any role; pct_of_firm_clients accordingly.
          Add these fields to each ADV-AUA segment in the platinum output.
    </description>
  </issue_3>

  <issue_4 label="P1-4 ADV-NNA: client-level drilldown data for advisor">
    <description>
      The ADV-NNA advisor drilldown into client-level NNA does not work in the portal.
      Determine whether the client-level NNA data exists in the platinum output for each
      advisor, or whether D_04 does not yet publish it.

      Required platinum structure for client-level NNA drilldown:
        platinum/advisors/{id}/nna_clients.json (or equivalent path)
        Content: list of { relationship_id, display_name [pseudonymized], nna, pct_of_advisor_nna }
        Sorted by absolute NNA descending. Top 9 + Other (same rule as everywhere else).
        Note: display_name MUST be pseudonymized -- see PII TO .032.

      If this file already exists in platinum, verify its schema matches what DE needs.
      If it does not exist, add it to D_04's per-advisor publish loop.
      Source: the advisor's book clients list crossed with their period NNA from D_02/C_03.

      Radial = relationships (client_count). Bell curve = accounts (account_count).
      Ensure both counts are available in the advisor-level NNA snapshot data.
    </description>
  </issue_4>

  <deliverables>
    1. Audit report in session log: for each of the 4 issues, current state vs required state
    2. D_04 changes (or upstream gold script changes) to fix issues 1-4
    3. Spot-check: pull sample platinum files for 2 states, 2 advisors after fix and verify
       Top 9 + Other applied, relationship_count and account_count present, center total correct
    4. Notify DE via MCP inbox when platinum data is ready (unblocks .028-.031)
  </deliverables>

  <acceptance_criteria>
    1. GEO-AUA segment schema: both relationship_count and account_count populated per segment
    2. GEO-NNA city drill: every state with >9 cities has exactly top 9 + Other
    3. ADV-AUA: advisor segments cover all roles, center total = firm headline AUA,
       each segment has relationship_count + pct_of_firm_clients
    4. ADV-NNA: per-advisor nna_clients.json exists (with pseudonymized names) for all advisors
    5. All new fields propagate through D_04 and land in S3 after AE re-run
  </acceptance_criteria>


  <compiler_tools>
    Run these BEFORE writing any platinum data to understand the full chain:

    comp-platinum reverse platinum/firm/partner_analytics_snap.json
      -- Back-traces the snapshot file through D_04 → D_01 → gold sources.
         Immediately shows which gold artifact feeds each field. Replaces tracing
         3 scripts manually.

    comp-pipescript io D_01
      -- D_01 produces the partner_analytics artifacts that D_04 passes through.
         Run to see what D_01 reads (canonical_holdings? account_performance?) so
         geo_coverage_decision step_0 knows which parquet to query for coverage %.

    comp-pipescript io D_04
      -- Confirms which partner_analytics fields D_04 currently reads and writes.
         Tells you what already exists vs what needs to be added for issues 1-4.

    comp-blast gold/artifacts/partner_analytics/
      -- Shows downstream consumers of D_01's partner_analytics outputs.
         Run before touching D_01 to assess blast radius.
  </compiler_tools>

</task_order>
