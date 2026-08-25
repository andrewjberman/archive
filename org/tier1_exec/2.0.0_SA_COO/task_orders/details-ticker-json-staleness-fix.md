# Task Order (ad-hoc, no PRD): details/{ticker}.json tier is stale -- likely unscheduled generator

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-details-ticker-json-staleness</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DE_MarketIntelligence</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "details-ticker-json-staleness-fix" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>STAGED, not urgent -- CTO-ruled ad-hoc, no PRD needed. Pick up whenever it fits (found during MKOV_RETFIX.TO-1, not blocking).</dispatch_state>
    <gate_note>None -- COO-resolvable whenever capacity allows.</gate_note>
  </metadata>

  <objective>details/{ticker}.json served tier is stale (latest_date 2026-01-09, generated 2026-01-13 -- ~6 months old as of this TO) and materially wrong (S&amp;P 3Y showed 0.866 vs the fresh summary/'s correct 0.7536). Likely the details-tier generator branch isn't scheduled. Find and fix the scheduling gap; do not just regenerate once (that masks the recurrence).</objective>

  <requirements>
    <requirement id="1">Confirm root cause: is the details-tier generator genuinely unscheduled, or scheduled-but-failing silently?</requirement>
    <requirement id="2">Fix the scheduling/execution gap so details/{ticker}.json stays fresh going forward, not just a one-time regeneration.</requirement>
    <requirement id="3">Regenerate current data once the schedule is fixed, confirm it matches summary/'s values.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>Root cause documented (unscheduled vs silently-failing).</criterion>
    <criterion>details/{ticker}.json shows a current latest_date matching summary/'s freshness, cited with actual values.</criterion>
    <criterion>Recurrence prevented -- either a working schedule or a freshness alarm if generation genuinely can't be made reliable.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="finding">0.1.0_DE_MarketIntelligence RAVC MKOV_RETFIX.TO-1, 20260707T163951Z</ref>
  </references>
</task_order>
```
