# Task Order: MKOV_TRSRCE TO-3 -- Re-verification across all in-scope served artifacts (STAGED, gated on TO-2)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mkov-trsrce-to3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MKOV_TRSRCE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>STAGED -- gated on MKOV_TRSRCE.TO-2's backfill completion. COO will GO this on TO-2's RAVC.</dispatch_state>
    <gate_note>Own proposed ownership/scope (SME/validation) per 0.2.0_DS_PortfolioAnalytics's own offer.</gate_note>
  </metadata>

  <objective>Post-backfill, recompute 3Y annualized (and other periods) from the new served period_returns for all 4 headline benchmarks; confirm match to Bloomberg's published TR to the basis point. Re-run the model_portfolio_benchmarks.json/benchmark_returns.json comparison to confirm model-portfolio benchmark comparisons reflect the corrected series. Confirm precompute_market_metrics output shifted consistently, not just "didn't error."</objective>

  <requirements>
    <requirement id="1">Recompute 3Y annualized (and other periods) from new served period_returns for all 4 headline benchmarks; confirm match to Bloomberg published TR to the bp.</requirement>
    <requirement id="2">Re-run model_portfolio_benchmarks.json/benchmark_returns.json comparison, confirm it reflects the corrected series.</requirement>
    <requirement id="3">Confirm precompute_market_metrics output shifted consistently (a real before/after comparison, not just absence of errors).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>All 4 headline benchmarks match Bloomberg's published TR to the bp, cited with actual numbers.</criterion>
    <criterion>model_portfolio_benchmarks.json/benchmark_returns.json comparison re-run and cited.</criterion>
    <criterion>precompute_market_metrics before/after shift documented, not just "ran clean."</criterion>
  </acceptance_criteria>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRSRCE_PRD.md SS6 TO-3</ref>
    <ref type="project">org/projects/MKOV_TRSRCE.json</ref>
  </references>
</task_order>
```
