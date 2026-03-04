# Task Order — Continuous View: "Total Clients" at Max Window

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-continuous-max-window-clients</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
    <priority>medium</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    In the Segment Analytics continuous view (both GEO and ADV cohorts), the left-panel
    hero metrics tile currently shows "New Clients" regardless of window selection.
    When window = "Max", this is wrong on two counts:
      1. The value displays "--" (the backend does not populate new_clients['Max']).
      2. "New Clients" is semantically incorrect for an all-time window — over all time,
         every client is a "new" client. The correct label is "Total Clients" and the
         correct value is the current total relationship count.

    Fix: make the tile window-aware.
      - 1Y / 3Y windows:  label = "New Clients",    value = new_clients[window]  (existing)
      - Max window:       label = "Total Clients",  value = current total relationships
  </objective>

  <problem>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    Location: ContinuousChartView component, ~lines 802-807

    Current code:
      &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
        &lt;p className="text-sm font-bold text-white"&gt;
          {data?.metadata?.new_clients?.[window as string] ?? '--'}
        &lt;/p&gt;
        &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;New Clients&lt;/p&gt;
      &lt;/div&gt;

    Root cause:
      data.metadata.new_clients is a Record&lt;string, number&gt; keyed by window string.
      The backend populates keys '1Y' and '3Y' but NOT 'Max', so window='Max' always
      falls through to '--'. Even if it were populated, "New Clients" over all time
      is meaningless — it is equivalent to total clients.

    Affected views:
      Both GEO and ADV continuous AUA views — they share the same ContinuousChartView
      component, so the fix is in one place.
  </problem>

  <fix>
    Three changes required:

    1. Add totalClients?: number to ContinuousChartViewProps interface.
       (~line 658 — interface definition)

    2. Pass totalClients at the ContinuousChartView call site.
       (~line 396-402 in DistributionTab — the JSX element)
       Derive totalClients from analyticsData (available in DistributionTab scope):
         const cohortView = cohort === 'geo'
           ? analyticsData?.views?.geo
           : analyticsData?.views?.adv
         totalClients = cohortView?.current?.metrics?.client_count
                        ?? cohortView?.metrics?.client_count

    3. Make the tile window-aware in ContinuousChartView.
       (~lines 802-807)
       When window === 'Max': label = "Total Clients", value = totalClients ?? '--'
       When window !== 'Max': label = "New Clients",   value = data?.metadata?.new_clients?.[window] ?? '--'
  </fix>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Three locations to edit, all within DistributionTab.tsx.
      </description>

      <change id="1">
        <location>
          ~Lines 658-664 — ContinuousChartViewProps interface
          (search: "interface ContinuousChartViewProps")
        </location>
        <current>
interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record&lt;string, string&gt;
}
        </current>
        <new>
interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record&lt;string, string&gt;
  totalClients?: number
}
        </new>
        <rationale>Adds the optional total relationship count for the Max-window tile.</rationale>
      </change>

      <change id="2">
        <location>
          ~Line 666 — ContinuousChartView function signature
          (search: "function ContinuousChartView({")
        </location>
        <current>
function ContinuousChartView({ data, cohort, metric, window, categoryColorMap }: ContinuousChartViewProps) {
        </current>
        <new>
function ContinuousChartView({ data, cohort, metric, window, categoryColorMap, totalClients }: ContinuousChartViewProps) {
        </new>
        <rationale>Destructures the new prop.</rationale>
      </change>

      <change id="3">
        <location>
          ~Lines 396-402 — ContinuousChartView JSX call site in DistributionTab
          (search: "&lt;ContinuousChartView" — the component usage, not the definition)
        </location>
        <current>
            &lt;ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
            /&gt;
        </current>
        <new>
            &lt;ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
              totalClients={
                cohort === 'geo'
                  ? (analyticsData?.views?.geo?.current?.metrics?.client_count
                     ?? analyticsData?.views?.geo?.metrics?.client_count)
                  : (analyticsData?.views?.adv?.current?.metrics?.client_count
                     ?? analyticsData?.views?.adv?.metrics?.client_count)
              }
            /&gt;
        </new>
        <rationale>
          analyticsData and cohort are both in scope in DistributionTab at this point.
          Derives total relationship count from the current period snapshot metrics.
          The ?? fallback handles both the legacy PartnerAnalyticsView shape (.metrics)
          and the current PartnerAnalyticsViewWithPeriods shape (.current.metrics).
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Lines 802-807 — "New Clients" tile inside ContinuousChartView
          (search: the bg-white/5 div with "New Clients" label text)
        </location>
        <current>
        &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
          &lt;p className="text-sm font-bold text-white"&gt;
            {data?.metadata?.new_clients?.[window as string] ?? '--'}
          &lt;/p&gt;
          &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;New Clients&lt;/p&gt;
        &lt;/div&gt;
        </current>
        <new>
        &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
          &lt;p className="text-sm font-bold text-white"&gt;
            {window === 'Max'
              ? (totalClients?.toLocaleString() ?? '--')
              : (data?.metadata?.new_clients?.[window as string]?.toLocaleString() ?? '--')}
          &lt;/p&gt;
          &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;
            {window === 'Max' ? 'Total Clients' : 'New Clients'}
          &lt;/p&gt;
        &lt;/div&gt;
        </new>
        <rationale>
          Max window: shows total relationship count with "Total Clients" label.
            - Semantically correct: over all time every client is cumulative total.
            - Fixes the '--' display (new_clients['Max'] is never populated by backend).
          1Y / 3Y: unchanged — shows new_clients[window] with "New Clients" label.
          .toLocaleString() added to both paths for consistent number formatting.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. Use offset reads:
      - ~line 658 for Changes 1-2 (interface + function signature)
      - ~line 390 for Change 3 (call site)
      - ~line 800 for Change 4 (tile)
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 4 changes as a unit. Change 3 and Change 4 are the user-visible
      fix; Changes 1 and 2 are the required plumbing.
    </requirement>
    <requirement id="3">
      The type access paths for totalClients in Change 3 use optional chaining
      with a ?? fallback to handle both the legacy PartnerAnalyticsView shape
      (direct .metrics.client_count) and the current PartnerAnalyticsViewWithPeriods
      shape (.current.metrics.client_count). Verify the actual types at read time
      and adjust if needed — the intent is to get the current total relationship count
      for the selected cohort (geo or adv).
    </requirement>
    <requirement id="4">
      analyticsData is the PartnerAnalyticsResponse prop passed into DistributionTab.
      It is in scope at the ContinuousChartView call site (line ~396). You are not
      introducing a new data fetch or state variable.
    </requirement>
    <requirement id="5">
      Do not change the 1Y or 3Y behavior. The existing new_clients[window] path
      is correct for those windows.
    </requirement>
    <requirement id="6">
      Commit with tag:
      "0.4.0_DE_ClientPlatform: fix continuous view — Total Clients at Max window"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="7">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/continuous_view_max_window_clients_fix.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      ContinuousChartViewProps interface has totalClients?: number field.
    </criterion>
    <criterion id="2">
      ContinuousChartView function signature destructures totalClients.
    </criterion>
    <criterion id="3">
      At the call site, totalClients is derived from analyticsData.views[cohort]
      current relationship count (with legacy shape fallback).
    </criterion>
    <criterion id="4">
      When window = "Max":
        - Tile label = "Total Clients"
        - Tile value = current total relationship count (not '--')
    </criterion>
    <criterion id="5">
      When window = "1Y" or "3Y":
        - Tile label = "New Clients" (unchanged)
        - Tile value = new_clients[window] from metadata (unchanged)
    </criterion>
    <criterion id="6">
      Both GEO and ADV cohorts exhibit the correct behavior (they share
      ContinuousChartView so this is automatic).
    </criterion>
    <criterion id="7">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not change the window toggle options (1Y, 3Y, Max) or their ordering.
    </constraint>
    <constraint>
      Do not change any other hero metric tiles (the gain-since-start tile
      or growth-rate tile in the 2-column grid above). Only the "New Clients"
      / "Total Clients" tile is in scope.
    </constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (4 changes: ContinuousChartViewProps, function signature, call site prop,
      window-aware tile label + value)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/continuous_view_max_window_clients_fix.md
    </deliverable>
  </deliverables>
</task_order>
```
