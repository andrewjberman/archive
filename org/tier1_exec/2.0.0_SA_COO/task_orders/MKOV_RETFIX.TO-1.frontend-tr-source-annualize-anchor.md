# Task Order: MKOV_RETFIX TO-1 -- Frontend fix: TR source + annualization + window anchoring (all toggles)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mkov-retfix-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DE_MarketIntelligence</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07 -- Andrew-direct P0, PRD docs/architecture/MKOV_RETFIX_PRD.md (commit c8eed34f8) SS6 TO-1. Supersedes the held ad-hoc TO market-overview-3y-return-modal-fix.md (which stays on record for the routing-correction history, not dispatched). CLOSED 2026-07-07T17:22Z -- promoted to PROD.</dispatch_state>
    <gate_note>Gates: none -- pipeline is faithful, no upstream dependency. Effort: 2-4h. Andrew wants this driven to a DEPLOYED fix, not parked.</gate_note>
  </metadata>

  <objective>portal/src/components/market-performance/IndexPerformanceModal.tsx currently computes its return stat by diffing historical_prices (PRICE return) instead of reading the already-served, already-correct total-return period_returns field -- reads 1.4-2.8pt low across indices. Fix + 2 riders per PRD SS6 TO-1.</objective>

  <requirements>
    <requirement id="1">Stat computation reads period_returns[period] from the served payload instead of diffing historical_prices.</requirement>
    <requirement id="2">Annualize display for periods &gt;1Y (3Y, 5Y) per (1 + cumulative) ** (365.25/PERIOD_CALENDAR_DAYS[period]) - 1; leave 1Y and shorter as period return (already ~annualized for 1Y). Label explicitly (e.g. "3Y Return (annualized)").</requirement>
    <requirement id="3">Window anchoring: period_returns is already data-date-anchored on the backend, so reading it directly (req 1) resolves the STAT's anchoring defect as a side effect. Separately confirm the chart's date-range display (if any) also reflects the data's latest date, not new Date(), for consistency with the stat.</requirement>
    <requirement id="4">Rider: quick check whether ExecutiveSummary has the same price-diff pattern (per PRD SS4) -- if yes, same fix; if no, note it in the session log and move on.</requirement>
    <requirement id="5">ANDREW FINAL SIGN-OFF ADDITION (20260707T1656Z, via 0.2.0_DS_PortfolioAnalytics) -- trailing-period capping: every trailing window is bounded to EXACTLY its full period from the data date -- no undershoot (the 2.97y bug) and no overshoot; if available history is shorter than the requested period, cap gracefully + label rather than silently showing a truncated "3Y". Verify each toggle spans its true period.</requirement>
    <requirement id="6">NON-NEGOTIABLE (CTO audit, restated in Andrew's sign-off): the chart's price LINE stays sourced from the unchanged price tickers -- do not break RSI/regime. (Already true per PRD SS4's "chart line unchanged in this PRD" -- this requirement is a verify-not-broken check, not new scope.)</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check IndexPerformanceModal</run>
        <expect>NOT-FOUND per PRD SS5.2 (known compiler-graph coverage gap, already flagged for the graph-coverage backlog, not blocking) -- if it now resolves, use its output instead of the manual line-cite; if still NOT-FOUND, confirm period_returns field shape via direct read of market-overview-tiered-generator/lambda_function.py, cite line numbers in the session log.</expect>
        <if_mismatch>N/A -- NOT-FOUND is the expected/known result; compensate via direct source read per the PRD's already-established pattern.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Re-run the 4-index Bloomberg comparison (DS 0.2.0's brief methodology) post-fix, for every period toggle touched -- not just 3Y.</run>
        <expect>S&amp;P/Russell/EAFE/Agg match Bloomberg to the bp (or the known EAFE gross-vs-net delta only, explicitly out of scope per PRD SS1).</expect>
        <if_mismatch>STOP if a non-EAFE index still mismatches -- indicates the fix itself is wrong, not just the known convention gap.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-cache collisions</run>
        <expect>No new query-key collision introduced by the fix (confirms PRD SS3's no-cache-key-risk finding still holds post-change).</expect>
        <if_mismatch>Surface immediately -- a new collision from this change needs disposition before it ships further.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion>3Y/5Y read from period_returns, annualized, cite before/after numbers per index (S&amp;P/Russell/EAFE/Agg) in the session log.</criterion>
    <criterion>1Y and shorter toggles unaffected in value (still period return) but confirmed data-date-anchored, not today-anchored.</criterion>
    <criterion>Bloomberg cross-check re-run post-fix for every period toggle exercised, cited with actual numbers.</criterion>
    <criterion>ExecutiveSummary rider check result documented (fixed, or confirmed not-applicable).</criterion>
    <criterion>Session log's Compiler Tools section documents the schema-check attempt + cache-collision re-run.</criterion>
    <criterion>Trailing-period capping verified per toggle: no undershoot/overshoot vs the requested period, graceful+labeled degradation when history is shorter than requested. This is Andrew's explicit GO condition for the DT promote -- must be verified before DT pushes, not assumed from req 1-3's fix.</criterion>
    <criterion>Chart price-line source confirmed unchanged (still the raw price tickers, not touched by this fix).</criterion>
  </acceptance_criteria>

  <evidence>
    PROD promote LANDED: commit f3ce600c (--no-ff merge of origin/DEV df9323de, empty parity diff), tag portal-v2.1.132 (peeled-verified), CI run 28884926281 conclusion SUCCESS, workspace pointer CLOUD e2004a5a4 pushed. All 7 requirements + all 7 acceptance criteria met, including req 5 (trailing-period capping, added post-hoc from Andrew's final sign-off, fixed+verified in df9323de -- zero live tickers actually affected, but the guard is real and committed). DT's promote pre-flight independently caught the uncommitted req-5 change and correctly HELD until DE committed it -- no half-verified batch shipped. Batch (whole-head, 4 commits): df9323de (req4/5 cap) + 7a58a54d (items 1-3) + f07b0b25 (AE docs) + 4d646417 (unrelated ClientPlatform NNA fix, pre-existing in the batch). DE running served-parity eyeball on the live PROD modal as final confirm.
  </evidence>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MKOV_RETFIX_PRD.md SS6 TO-1</ref>
    <ref type="project">org/projects/MKOV_RETFIX.json</ref>
    <ref type="brief">docs/briefs/market-overview-3y-return-price-vs-total-return-20260707.md</ref>
  </references>
</task_order>
```
