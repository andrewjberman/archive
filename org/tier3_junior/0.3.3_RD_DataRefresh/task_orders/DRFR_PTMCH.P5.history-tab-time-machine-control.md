```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-12-drfr-ptmch-p5-rd-datarefresh</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.3_RD_DataRefresh</issued_to>
    <date>2026-03-12</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <parent_task>DRFR_PTMCH.P5.time-machine-portal-integration</parent_task>
  </metadata>

  <objective>
    Add a "Time Machine" control section to the DataRefresh HistoryTab.
    Users select a historical date from available restore points and trigger
    the portal-wide time machine, which restores all data sources to that date.
    All state comes from useTimeMachine() -- no local state duplication.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/DataRefresh/HistoryTab.tsx (or equivalent)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add a "Time Machine" section to HistoryTab below the existing execution history list.
    </requirement>

    <requirement id="2">
      Date picker: shows only dates present in the restorePoints array (from useTimeMachine()).
      Dates not in restorePoints are disabled/not selectable.
      On mount, call loadRestorePoints() to populate the list.
    </requirement>

    <requirement id="3">
      "Travel to [date]" button:
      - Fires activateTimeMachine(selectedDate) from useTimeMachine()
      - Shows a spinner/loading indicator
      - Disables the button for 3 minutes (async restore, no completion signal)
      - After 3 minutes, re-enable the button automatically
    </requirement>

    <requirement id="4">
      "Return to current" link/button:
      - Only visible when isActive is true (from useTimeMachine())
      - Fires deactivateTimeMachine() from useTimeMachine()
    </requirement>

    <requirement id="5">
      When isActive is true: show a "Viewing portal as of [viewAsOf]" pill/badge
      in the DataRefresh page header area.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Selecting a date from restorePoints and clicking "Travel" calls
      activateTimeMachine with the correct date string.
    </criterion>
    <criterion id="2">
      While restoring (3-minute window), button shows loading state and is disabled.
    </criterion>
    <criterion id="3">
      "Return to current" appears only when isActive=true and calls deactivateTimeMachine.
    </criterion>
    <criterion id="4">
      Active state pill visible in page header when time machine is active.
    </criterion>
    <criterion id="5">bunx tsc -b passes. No type errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      useTimeMachine() is the single source of truth. Do NOT duplicate isActive,
      viewAsOf, or restorePoints in local component state.
    </constraint>
    <constraint>
      The time machine is async -- there is no completion callback. The UI uses a
      3-minute timer then clears the loading state, trusting the backend completed.
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
    <deliverable type="commit">HistoryTab Time Machine control section with date picker,
    travel button, return link, and active state pill</deliverable>
  </deliverables>
</task_order>
```
