# Task Order (ad-hoc, no PRD per CTO): Market Overview 3Y return modal reads low -- frontend-only fix

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-market-overview-3y-return-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DE_PortfolioAnalytics</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>DISPATCHED 2026-07-07 -- CTO-ruled ad-hoc, no PRD needed (docs/briefs/market-overview-3y-return-price-vs-total-return-20260707.md, source-confirmed by 0.2.0_DS_PortfolioAnalytics). Pipeline is faithful all the way to the served card -- no cloud/ingest change in scope.</dispatch_state>
    <gate_note>3 of 4 indices match Bloomberg to the bp once the fix is understood -- confirms the bug is isolated to the modal's own computation, not upstream data.</gate_note>
  </metadata>

  <objective>IndexPerformanceModal.tsx:185 computes "3Y Return" from the `price` level (ex-dividend price return) instead of the already-served total-return `period_returns` field -- reads 1.4-2.8pt low across indices. Fix + two riders in the same file/session (CTO-specified, all three in one fix pass).</objective>

  <requirements>
    <requirement id="1">Read the served total-return field (`period_returns`), not a re-derivation from `price`.</requirement>
    <requirement id="2">Rider: modal currently shows cumulative return, not annualized -- annualize it.</requirement>
    <requirement id="3">Rider: modal currently uses a rolling today-1095d window instead of a clean 3-calendar-year window -- align to calendar-year.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check IndexPerformanceModal</run>
        <expect>Confirms `period_returns` field shape/type before wiring it into the 3Y calc.</expect>
        <if_mismatch>STOP -- resolve the field shape mismatch before writing the fix.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Re-run the 4-index comparison against Bloomberg (the same check DS 0.2.0's brief used) post-fix</run>
        <expect>All 4 indices match to the bp (or the EAFE gross-vs-net delta only, which is explicitly OUT of scope -- see below).</expect>
        <if_mismatch>STOP if a NON-EAFE index still mismatches -- that indicates the fix itself is wrong, not just the known convention gap.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion>3Y return reads from period_returns (TR), annualized, calendar-year-aligned -- cite the before/after numbers per index in the session log.</criterion>
    <criterion>Bloomberg cross-check re-run post-fix, cited with actual numbers.</criterion>
    <criterion>Session log's Compiler Tools section reproduces the schema-check run.</criterion>
  </acceptance_criteria>

  <not_in_scope>
    EAFE gross-vs-net dividend convention (our MXEA gross TR vs the street's net EAFE, NDDUEAFE) -- a data-governance/convention call Andrew already knows about (he initiated the investigation via DS), NOT a bug. Do not fold into this TO's acceptance criteria; it stays a separately-tracked open decision.
  </not_in_scope>

  <references>
    <ref type="brief">docs/briefs/market-overview-3y-return-price-vs-total-return-20260707.md</ref>
  </references>
</task_order>
```
