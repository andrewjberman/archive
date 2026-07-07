# Task Order: MKOV_RETFIX TO-2 -- Residual-bps reconciliation (terminal-diff)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mkov-retfix-to2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>DISPATCHED 2026-07-07 -- Andrew-direct P0, PRD docs/architecture/MKOV_RETFIX_PRD.md (commit c8eed34f8) SS6 TO-2.</dispatch_state>
    <gate_note>Gates: requires Yang terminal access (confirmed available). Effort: 2-4h (terminal-dependent). Data-reconciliation task, no code change.</gate_note>
  </metadata>

  <objective>Close the 6-32bp residual (S&amp;P +18bp, Russell +32bp, Agg +6bp per Andrew's figures, post-rounding-adjustment) between Yang's computed gross-TR series (on price tickers SPX/RTY/MXEA) and Bloomberg's PUBLISHED total-return index (SPXT/RU20INTR/net-EAFE equivalent) to a source-grounded arithmetic explanation -- not "close enough."</objective>

  <requirements>
    <requirement id="1">Pull Bloomberg's published TR index series (SPXT, RU20INTR, or index-appropriate TR ticker) over the identical 2023-07-03 to 2026-06-30 window via the Yang terminal; diff series-vs-series against our computed return field, day by day, not just endpoint-to-endpoint.</requirement>
    <requirement id="2">Isolate the residual to a named, evidenced cause (methodology delta in dividend timing/reinvestment assumption, index-vintage mismatch, or genuinely unexplained -- if unexplained, say so explicitly rather than papering over it).</requirement>
    <requirement id="3">If the residual turns out to be closeable (e.g., Yang should ingest the published TR index directly instead of computing gross-TR from the price ticker), flag as a new PRD candidate -- do NOT silently patch the pipeline as a side effect of this investigation.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>none -- this is a data-reconciliation task, not a code change</run>
        <expect>Starting evidence base is the already-completed raw-PKL grounding (PRD SS2: decimal-precision ruled out, daily-vs-monthly frequency ruled out, window-boundary convention confirmed correct).</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Pull Bloomberg published TR series via Yang terminal, day-level diff vs our computed return field over the identical window</run>
        <expect>A day-level diff pattern that either isolates a specific, named methodology delta or definitively rules out the leading candidates (dividend-timing/reinvestment assumption, index-vintage mismatch).</expect>
        <if_mismatch>STOP before writing up "unexplained" -- confirm the terminal pull itself is correct (right ticker, right window, right series type) before concluding no explanation exists.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit"><step><run>none additional</run><expect>N/A</expect><if_mismatch>N/A</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion>Series-vs-series diff isolates the residual to a named, evidenced cause -- or explicitly documents it as genuinely unexplained, not glossed over.</criterion>
    <criterion>Written up as a brief (docs/briefs/) citing the exact Bloomberg ticker(s) pulled, the window, and the day-level diff summary.</criterion>
    <criterion>If closeable, flagged as a new PRD candidate rather than silently patched.</criterion>
  </acceptance_criteria>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MKOV_RETFIX_PRD.md SS6 TO-2</ref>
    <ref type="project">org/projects/MKOV_RETFIX.json</ref>
    <ref type="brief">docs/briefs/market-overview-3y-return-price-vs-total-return-20260707.md</ref>
  </references>
</task_order>
```
