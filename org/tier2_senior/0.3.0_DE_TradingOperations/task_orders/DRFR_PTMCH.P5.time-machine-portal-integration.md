```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-p5-de-trading</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
  </metadata>

  <objective>
    Portal-side Time Machine integration. Two deliverables: (1) a React context
    (TimeMachineContext) that carries time_machine_active + view_as_of_date state
    globally across all portal pages, and (2) a "Travel to date" control in
    DataRefresh/HistoryTab that triggers the time machine and sets that context.
    Also issue task orders to 0.3.3_RD_DataRefresh (HistoryTab control) and
    0.3.1_RD_PortfolioManagement (banner + chart filtering).
  </objective>

  <scope>
    <files>
      <file action="create">portal/src/context/TimeMachineContext.tsx</file>
      <file action="modify">portal/src/App.tsx</file>
      <file action="modify">portal/src/api/endpoints/data-refresh.ts</file>
      <file action="modify">portal/src/pages/DataRefresh/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      TimeMachineContext -- create portal/src/context/TimeMachineContext.tsx:

      State shape:
        {
          isActive: boolean
          viewAsOf: string | null        // "YYYY-MM-DD" when active
          initiatedAt: string | null     // ISO timestamp when time machine was triggered
          restorePoints: RestorePoint[]  // populated from GET /data-refresh/archive
        }

      type RestorePoint = {
        execution_id: string
        data_as_of: string          // "YYYY-MM-DD"
        pipeline_completed_at: string
        files_captured: number
      }

      Actions:
        activateTimeMachine(targetDate: string): void
          -- calls POST /data-refresh/time-machine { target_date }
          -- sets isActive=true, viewAsOf=targetDate, initiatedAt=now
        deactivateTimeMachine(): void
          -- calls POST /data-refresh/time-machine { target_date: today's date }
          -- sets isActive=false, viewAsOf=null
        loadRestorePoints(): void
          -- calls GET /data-refresh/archive
          -- populates restorePoints

      Export: TimeMachineProvider (wraps children), useTimeMachine() hook.
    </requirement>

    <requirement id="2">
      Wrap App.tsx with TimeMachineProvider so all pages have access via useTimeMachine().
      Position: outside the router, wraps everything.
    </requirement>

    <requirement id="3">
      data-refresh.ts API endpoints -- add two functions:
        getArchiveRestorePoints(): Promise<{ restore_points: RestorePoint[], count: number }>
          GET /data-refresh/archive

        triggerTimeMachine(targetDate: string): Promise<{ status: string, target_date: string }>
          POST /data-refresh/time-machine  { target_date: targetDate }

      Both require auth (existing auth pattern for data-refresh endpoints).
    </requirement>

    <requirement id="4">
      Issue task order to 0.3.3_RD_DataRefresh:
        DRFR_PTMCH.P5.history-tab-time-machine-control.md
        Scope: "Travel to date" UI in DataRefresh/HistoryTab.
        - Date picker populated from restorePoints (from TimeMachineContext)
        - "Travel" button: calls activateTimeMachine(selectedDate)
        - "Return to current" button: calls deactivateTimeMachine()
        - Loading state while time machine is running (~2-3 min)
        - Show "Time Machine active: viewing [date]" in DataRefresh header when isActive
        Constraint: uses useTimeMachine() hook -- no local state duplication.

      Issue task order to 0.3.1_RD_PortfolioManagement:
        DRFR_PTMCH.P5.time-machine-banner-and-chart-filter.md
        Scope: global banner + PortfolioManagement chart date filtering.
        See requirement 5 below for full spec.
    </requirement>

    <requirement id="5">
      Spec for RD task orders (include in full when issuing):

      0.3.3_RD_DataRefresh -- HistoryTab control:
        - Add "Time Machine" section to HistoryTab below existing execution history
        - Date picker: shows only dates present in restorePoints array (disable others)
        - "Travel to [date]" button: fires activateTimeMachine(date), shows spinner,
          disables button for 3 minutes (async restore, no completion signal)
        - "Return to current" link: fires deactivateTimeMachine()
        - When isActive: show "Viewing portal as of [viewAsOf]" pill in page header

      0.3.1_RD_PortfolioManagement -- banner + chart filter:
        - Global banner: when isActive, show a sticky top banner across ALL pages:
          "Time Machine active -- Viewing portal as of [viewAsOf date]  [Exit]"
          Banner color: amber/yellow to signal non-live state. Exit calls deactivateTimeMachine().
        - PortfolioManagement time series charts (SmartX/model portfolio returns):
          When isActive, filter chart data to only render data points where
          date <= viewAsOf before passing to the chart component.
          These charts consume from json/portfolios/ append-only files.
          The filter is applied at the data-transformation layer, not in the chart component itself.
        - "Data as of [viewAsOf]" label on filtered charts to make the cutoff explicit.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      TimeMachineContext: useTimeMachine() hook available in any portal page.
      activateTimeMachine("2026-02-28") fires POST /data-refresh/time-machine and
      sets isActive=true, viewAsOf="2026-02-28".
    </criterion>
    <criterion id="2">
      App.tsx wrapped with TimeMachineProvider -- no prop-drilling needed.
    </criterion>
    <criterion id="3">
      getArchiveRestorePoints() returns typed RestorePoint[] from GET /data-refresh/archive.
      triggerTimeMachine() POSTs correct payload and returns typed response.
    </criterion>
    <criterion id="4">
      Both downstream task orders issued to 0.3.3_RD and 0.3.1_RD with full spec.
    </criterion>
    <criterion id="5">bunx tsc -b passes. No type errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>TimeMachineContext is the single source of truth for time machine state.
    RD components consume it via useTimeMachine() -- do not duplicate state locally.</constraint>
    <constraint>deactivateTimeMachine() restores to today's date by calling the time machine
    with today -- it does not "undo" the restore. The portal-time-machine Lambda handles
    finding the most recent execution for today's date.</constraint>
    <constraint>The time machine is async -- activateTimeMachine returns immediately after
    firing the API call. The frontend does NOT poll for completion. It sets a 3-minute
    "restoring..." UI state and then clears it, trusting the backend completed.</constraint>
    <constraint>TypeScript strict -- all context values and API responses fully typed.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.5.0_AE_OpalETL" task="DRFR_PTMCH.P5.portal-time-machine-orchestrator.md"
      status="pending"
      note="portal-time-machine Lambda + updated POST /data-refresh/time-machine must be
      deployed before the frontend can call it. DE can build and type against the API
      contract now; deploy gate applies to testing only."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">portal/src/context/TimeMachineContext.tsx -- context + hook + provider</deliverable>
    <deliverable type="commit">App.tsx wrapped with TimeMachineProvider</deliverable>
    <deliverable type="commit">data-refresh.ts -- getArchiveRestorePoints + triggerTimeMachine endpoints</deliverable>
    <deliverable type="commit">DataRefresh/types.ts -- RestorePoint type exported</deliverable>
    <deliverable type="document">Task orders issued to 0.3.3_RD_DataRefresh and 0.3.1_RD_PortfolioManagement</deliverable>
  </deliverables>
</task_order>
```
