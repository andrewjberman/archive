<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-18-mvp318-005-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-18</date>
    <status>complete</status>
    <project_code>ADVI_MVP318</project_code>
  </metadata>

  <objective>
    Complete the ConsolidatedOverviewPanel in the Books tab (WS4): N1 (firm) and L3 (relationship)
    views have no blockers — start immediately. L2 (advisor book) view is blocked on WS3d+e
    (endpoints live + DE types available). Conditional: if the WS1-A diagnostic shows Root Cause B
    (frontend windowing), add an "AUA as of [date]" subtitle to the continuous view in DistributionTab.
    All work commits to portal DEV.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_MVP318_PRD.md §WS1-C, §WS3f, §WS4, §WS5.
    Architecture background: docs/architecture/ADVI_data_lineage.md.

    DT will report the WS1-A diagnostic result (Root Cause A/B/C). Monitor for that report.
    If Root Cause B: add DistributionTab subtitle immediately (WS1-C).
    If Root Cause A or C: skip WS1-C.

    Existing endpoints for N1 and L3 views:
    - Firm-level: existing firm/mix-views and partner analytics endpoints (already wired elsewhere in portal)
    - Relationship-level: existing /books/relationship/{rel_id}/timeseries and /books/relationship/{rel_id}/mix-timeseries
    Advisor-level (L2): new endpoints after WS3d+e — getAdvisorTimeseries() and getAdvisorMixTimeseries()
    (DE will add these types and functions).

    The ConsolidatedOverviewPanel must handle three drill levels:
    - Level 0 (N1): firm-level metrics — fires when no advisor or relationship is selected
    - Level 1 (L2): advisor book metrics — fires when an advisor is selected
    - Level 2 (L3): relationship-level metrics — fires when a relationship is selected
  </context>

  <scope>
    <files>
      <file action="create-or-modify">portal/src/pages/AdvisorIntelligence/tabs/BooksTab.tsx (or ConsolidatedOverviewPanel.tsx if separate)</file>
      <file action="modify-conditional">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx (WS1-C, only if Root Cause B)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS4-N1" priority="immediate">
      Complete the N1 (firm-level) view in ConsolidatedOverviewPanel. No blockers.

      N1 view shows firm-wide metrics:
      - Total AUA (snapshot), NNA (period-dependent), asset class mix breakdown
      - Quarterly metrics bar: MTD/QTD/YTD NNA, AUA growth %, client count
      - Use existing firm-level endpoints (whatever is already wired for firm analytics)

      Wire to ConsolidatedOverviewPanel at drill level 0 (no advisor, no relationship selected).
      If no firm-level timeseries endpoint exists for the quarterly bar, use the same approach
      as the L3 relationship view — derive from the relationship roll-up or use a stub with a
      TODO comment for the WS3 phase.
    </requirement>

    <requirement id="2" workstream="WS4-L3" priority="immediate">
      Complete the L3 (relationship-level) view in ConsolidatedOverviewPanel. No blockers.

      L3 view shows single-relationship metrics:
      - Relationship AUA (snapshot), NNA, asset class mix breakdown
      - Quarterly metrics bar: MTD/QTD/YTD NNA, AUA growth %
      - Use existing /books/relationship/{rel_id}/timeseries and
        /books/relationship/{rel_id}/mix-timeseries endpoints

      Wire to ConsolidatedOverviewPanel at drill level 2 (relationship selected).
    </requirement>

    <requirement id="3" workstream="WS4-L2-structure" priority="immediate">
      Implement the L2 (advisor book) view UI structure in ConsolidatedOverviewPanel now.
      Leave the data connection in a loading/skeleton state until WS3d+e completes.

      L2 view will show:
      - Advisor AUA (sum across all relationships), NNA, asset class mix breakdown
      - Quarterly metrics bar: MTD/QTD/YTD NNA, AUA growth %
      - Data from getAdvisorTimeseries() and getAdvisorMixTimeseries() (not yet available)

      Implement the component branch and prop interface. Pass a placeholder data source
      (empty arrays or null) until DE commits the types and the endpoints are live.
      Wire to ConsolidatedOverviewPanel at drill level 1 (advisor selected, no relationship).
    </requirement>

    <requirement id="4" workstream="WS4-L2-wire" condition="After DT confirms WS3d deploy AND DE commits advisor types">
      GATE: Both DT (WS3d deploy) and DE (WS3e types + functions) must be complete.

      After gate clears:
      - Replace the L2 loading placeholder with real data calls:
          const { data } = useQuery(['advisor-ts', advisorId], () => getAdvisorTimeseries(advisorId, firmId))
          const { data: mixData } = useQuery(['advisor-mix-ts', advisorId, window], () =>
            getAdvisorMixTimeseries(advisorId, firmId, window))
        (Adapt to whatever query/fetch pattern is used in the rest of BooksTab)
      - Wire timeseries data to the quarterly metrics bar
      - Wire mix data to the asset class breakdown

      Commit all ConsolidatedOverviewPanel work (N1 + L3 + L2) to portal DEV in one commit:
        git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" \
          -m "feat(portal): ConsolidatedOverviewPanel N1+L2+L3 views complete (ADVI_MVP318 WS4)"
      Report commit SHA to COO — this triggers DE's pod_inventory update and is a WS6 gate.
    </requirement>

    <requirement id="5" workstream="WS1-C" condition="Only if DT reports Root Cause B from WS1-A diagnostic">
      If DT's diagnostic result is Root Cause B (S3 values match, gap is frontend-only):

      Add a subtitle to the continuous view in portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      that shows the chart's data date. The subtitle should read: "Data as of [date]" where [date]
      comes from the response's data_as_of field (or equivalent — inspect the response shape).

      This aligns user expectations: the snapshot is "right now" and the chart is a historical trend.
      No backend change required.

      Commit to portal DEV:
        git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" \
          -m "feat(portal): DistributionTab continuous view data-as-of subtitle (ADVI_MVP318 WS1-C)"
      This is a WS6 gate condition.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">N1 firm view renders in ConsolidatedOverviewPanel with real firm-level data</criterion>
    <criterion id="2">L3 relationship view renders with real relationship timeseries + mix data</criterion>
    <criterion id="3">L2 advisor view UI structure present; loads with real data after WS3d+e gates clear</criterion>
    <criterion id="4">Panel correctly switches between N1/L2/L3 based on drill level selection</criterion>
    <criterion id="5">WS1-C subtitle present in DistributionTab if Root Cause B (skip if A or C)</criterion>
    <criterion id="6">All commits to portal DEV under 0.4.2_RD_AdvisorIntelligence author</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT wire L2 data calls before DT confirms WS3d deploy — endpoints will 404</constraint>
    <constraint>Do NOT implement WS1-C unless DT explicitly reports Root Cause B</constraint>
    <constraint>N1 and L3 views start immediately — no gates</constraint>
    <constraint>All portal changes commit to portal DEV, not CLOUD parent repo</constraint>
    <constraint>No emojis in any code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>Use 0.4.2_RD_AdvisorIntelligence as git author on all commits</constraint>
    <constraint>Do not add docstrings or extra comments to unchanged surrounding code</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MVP318.002 req 4" status="pending">
      opal-partners-data deployed (WS3d) — gate for L2 data wiring only (req 4)
    </dependency>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_MVP318.004 req 2" status="pending">
      getAdvisorTimeseries + getAdvisorMixTimeseries types committed — gate for L2 data wiring only (req 4)
    </dependency>
    <dependency agent="none" task="N1+L3" status="clear">
      N1 and L3 views: no upstream gates — start immediately
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">ConsolidatedOverviewPanel N1+L2+L3 committed to portal DEV (WS4 complete)</deliverable>
    <deliverable type="commit">DistributionTab "AUA as of [date]" subtitle committed (WS1-C, conditional on Root Cause B)</deliverable>
  </deliverables>
</task_order>
