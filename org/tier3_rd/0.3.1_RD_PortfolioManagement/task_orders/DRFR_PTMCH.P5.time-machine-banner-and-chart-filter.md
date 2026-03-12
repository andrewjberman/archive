```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-12-drfr-ptmch-p5-rd-portfoliomgmt</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.1_RD_PortfolioManagement</issued_to>
    <date>2026-03-12</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <parent_task>DRFR_PTMCH.P5.time-machine-portal-integration</parent_task>
  </metadata>

  <objective>
    Two deliverables: (1) a global sticky banner visible on ALL portal pages when the
    time machine is active, and (2) date-filtered time series charts on the
    PortfolioManagement page that only show data up to viewAsOf when active.
  </objective>

  <scope>
    <files>
      <file action="create-or-modify">portal/src/components/TimeMachineBanner.tsx (new component)</file>
      <file action="modify">portal/src/App.tsx (render banner inside DashboardLayout)</file>
      <file action="modify">portal/src/pages/PortfolioManagement/ (chart data filtering)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Global banner: when isActive is true (from useTimeMachine()), render a sticky
      top banner across ALL portal pages:

        "Time Machine active -- Viewing portal as of [viewAsOf date]  [Exit]"

      - Banner color: amber/yellow background to signal non-live state
      - Position: sticky top, above page content but below sidebar
      - "Exit" button calls deactivateTimeMachine()
      - Banner disappears immediately when isActive becomes false
    </requirement>

    <requirement id="2">
      Render the banner component inside DashboardLayout (App.tsx), above the
      main content area. It reads state from useTimeMachine() -- no props needed.
    </requirement>

    <requirement id="3">
      PortfolioManagement time series charts (SmartX / model portfolio returns):
      When isActive is true, filter chart data to only render data points where
      date <= viewAsOf BEFORE passing data to the chart component.

      These charts consume from json/portfolios/ append-only files. The filter
      is applied at the data-transformation layer, not inside the chart component.
    </requirement>

    <requirement id="4">
      When charts are filtered (isActive=true), show a "Data as of [viewAsOf]"
      label on each filtered chart to make the cutoff date explicit to the user.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      When isActive=true, amber banner is visible at the top of every page
      showing the viewAsOf date with an Exit button.
    </criterion>
    <criterion id="2">
      Clicking Exit calls deactivateTimeMachine() and banner disappears.
    </criterion>
    <criterion id="3">
      PortfolioManagement charts show only data points with date <= viewAsOf
      when time machine is active.
    </criterion>
    <criterion id="4">
      "Data as of [date]" label visible on filtered charts.
    </criterion>
    <criterion id="5">bunx tsc -b passes. No type errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      useTimeMachine() is the single source of truth. Do NOT duplicate isActive
      or viewAsOf in local component state.
    </constraint>
    <constraint>
      Chart filtering happens at the data-transformation layer (before data reaches
      the chart component), not via chart library props or axis limits.
    </constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.0_DE_TradingOperations"
      task="TimeMachineContext created and App.tsx wrapped"
      status="complete"
      note="useTimeMachine() hook is available from portal/src/context/TimeMachineContext.tsx"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">TimeMachineBanner component + DashboardLayout integration</deliverable>
    <deliverable type="commit">PortfolioManagement chart date filtering with "Data as of" labels</deliverable>
  </deliverables>
</task_order>
```
