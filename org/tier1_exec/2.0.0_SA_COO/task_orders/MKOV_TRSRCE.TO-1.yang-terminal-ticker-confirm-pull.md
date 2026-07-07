# Task Order: MKOV_TRSRCE TO-1 -- Yang terminal: ticker confirmation + full-history pull

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mkov-trsrce-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>DISPATCHED 2026-07-07 -- Andrew-direct implementation (not just candidate), PRD docs/architecture/MKOV_TRSRCE_PRD.md (commit 6aa0b5741) SS6 TO-1. Starting gate for TO-2/TO-3, both staged behind this.</dispatch_state>
    <gate_note>Gates: none (starting point). Effort: Yang-dependent (terminal access, human timeline) -- coordinate with Andrew on the Yang terminal pull, do not attempt to self-source.</gate_note>
  </metadata>

  <objective>Confirm exact Bloomberg terminal symbols for SPXT/RU20INTR/NDDUEAFE (published TR indices for S&amp;P/Russell2000/EAFE-net) and pull full history matching the existing PKL depth (1095+ days minimum, per the 3Y support requirement) for all three -- coordinating the Yang terminal pull with Andrew/whoever executes it. Confirm the unchanged price-ticker series (SPX/RTY/MXEA) continue delivering unchanged in the same PKL.</objective>

  <requirements>
    <requirement id="1">Confirm exact Bloomberg terminal symbols for SPXT, RU20INTR, NDDUEAFE.</requirement>
    <requirement id="2">Coordinate the full-history pull (matching existing price-ticker depth, no gaps) for all 3 TR tickers.</requirement>
    <requirement id="3">Confirm price-ticker series (SPX/RTY/MXEA) continue unchanged in the same PKL delivery -- this is the non-negotiable from TO-2 that TO-1 must not break at the source.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>New PKL delivery contains both series (unchanged price tickers + new TR tickers) for all 3 benchmarks, full history, no gaps vs the existing price-ticker history depth.</criterion>
  </acceptance_criteria>

  <cross_domain_coordination>
    <item>This is the hard gate for MKOV_TRSRCE.TO-2 (ingest+backfill, 0.1.0_DS_MarketIntelligence/0.1.0_AE) and TO-3 (re-verification, 0.2.0_DS_PortfolioAnalytics). Both stay staged (not dispatched) until this TO's acceptance criteria are met -- notify COO on completion so TO-2 can be GO'd.</item>
  </cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRSRCE_PRD.md SS6 TO-1</ref>
    <ref type="project">org/projects/MKOV_TRSRCE.json</ref>
  </references>
</task_order>
```
