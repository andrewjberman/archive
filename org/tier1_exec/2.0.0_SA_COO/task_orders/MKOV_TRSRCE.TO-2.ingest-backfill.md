# Task Order: MKOV_TRSRCE TO-2 -- Ingest + full historical backfill (STAGED, gated on TO-1)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mkov-trsrce-to2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence / 0.1.0_AE (co-owned per pipescript's producer ownership)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MKOV_TRSRCE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>STAGED, CONTENT STALE (v1.0 scope, kept for reference) -- PRD revised to v1.1 (commit 41de08a6b): TO-2 is now EAFE-only, path-dependent on TO-1's answer (path a=cheap net-dividend adjustment on existing gross figure, b=moderate source-existing-net-series, c=heavier NDDUEAFE-direct fallback -- only path c resembles this file's current full-migration content). COO will REWRITE this TO to the actual path once TO-1 answers, not just GO the content as-written. Do NOT begin on this file's current content.</dispatch_state>
    <gate_note>Gates: depends on TO-1's answer (path a/b/c). Effort: 2-4h if path a/b [v1.1, much smaller], 1-2 sessions if path c [fallback, closer to this file's current scope].</gate_note>
  </metadata>

  <objective>yang-ingest-dynamodb derives daily_return/return from the new TR tickers for the 3 changed benchmarks; price field stays sourced from the unchanged price tickers (non-negotiable -- RSI + regime-classifier depend on it being byte-identical). Full historical backfill of opal-portal-market-data for the new TR series -- every historical date, not just going-forward.</objective>

  <requirements>
    <requirement id="1">yang-ingest-dynamodb derives daily_return/return from the new TR tickers (SPXT/RU20INTR/NDDUEAFE) for the 3 changed benchmarks.</requirement>
    <requirement id="2">price field stays sourced from the unchanged price tickers (SPX/RTY/MXEA) -- non-negotiable, verify byte-identical not just "field present."</requirement>
    <requirement id="3">Full historical backfill of opal-portal-market-data for the new TR series -- every historical date, zero gaps, zero silent splice.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast yang-ingest-dynamodb</run>
        <expect>Confirms every downstream reader before touching the writer -- cross-check against PRD SS2's consumer table for completeness (includes yang-model-portfolio-benchmarks, a real consumer the PRD's audit surfaced).</expect>
        <if_mismatch>STOP -- a downstream reader not in PRD SS2's table needs disposition before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Diff the backfilled series for zero gaps vs the existing price-ticker date range; diff the price field byte-identical pre/post change (a real diff, not "field present").</run>
        <expect>Zero gaps, byte-identical price field.</expect>
        <if_mismatch>STOP -- any gap or price-field drift is a hard blocker, not a documented caveat.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>pipescript market-overview + pipescript model-portfolios (re-run post-deploy)</run>
        <expect>MA-02 (RSI) and MA-03 (regime classifier) output UNCHANGED -- a parity check (byte-identical on a fixed historical date), not just "still runs."</expect>
        <if_mismatch>STOP -- any drift in MA-02/MA-03 output means the price-field non-negotiable was violated somewhere in the pipeline; do not ship.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion>opal-portal-market-data has full-history TR-derived daily_return for SPXT/RU20INTR/NDDUEAFE-mapped tickers, zero gaps, zero silent splice at any date.</criterion>
    <criterion>price field for the same 3 tickers is byte-identical pre/post change (diffed, not assumed).</criterion>
    <criterion>MA-02 (RSI) and MA-03 (regime classifier) outputs are byte-identical pre/post change on a fixed historical date (parity proof, not just "no errors").</criterion>
    <criterion>Session log's Compiler Tools section documents the blast-radius + parity re-checks.</criterion>
  </acceptance_criteria>

  <cross_domain_coordination>
    <item>Gates MKOV_TRSRCE.TO-3 (0.2.0_DS_PortfolioAnalytics re-verification) -- notify COO on completion.</item>
  </cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRSRCE_PRD.md SS6 TO-2</ref>
    <ref type="project">org/projects/MKOV_TRSRCE.json</ref>
  </references>
</task_order>
```
