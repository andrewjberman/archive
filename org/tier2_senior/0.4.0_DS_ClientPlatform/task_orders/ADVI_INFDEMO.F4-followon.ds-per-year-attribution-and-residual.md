<task_order>
  <metadata>
    <id>ADVI_INFDEMO.F4-followon</id>
    <slug>ds-per-year-attribution-and-residual</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-28</date>
    <status>parked</status>
    <reconcile_2026_06_01>PARKED (post-demo readability tail). ADVI_INFMVP shipped + Andrew-smoke-passed (portal-v2.1.107); per-year-attribution = suppress/caveat graceful-hide (Andrew Q3), likely folded/moot. Surfaced to COO -- closeable unless Andrew wants the per-year display refined. (was: pending)</reconcile_2026_06_01>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P2 — POST-DEMO. Demo covered by suppressing the per-year table (CVO CONCERN). No demo-clock pressure.</priority>
  </metadata>

  <references>
    <ref type="parent">ADVI_INFDEMO.F4 (reconciliation DONE + accepted; commit b570b342a, CVO verify a8be3399e)</ref>
    <ref type="prd">docs/architecture/ADVI_INFDEMO.md §F4</ref>
    <ref type="accept">2.0.0_SA_COO F4-ravc2-accept 1440Z; 1.0.0_SA_CTO 1438Z</ref>
  </references>

  <context>
    The F4 canonical-anchor fix RECONCILED the Cost Basis by Year TOTAL to canonical ($166.1M, CVO-verified 8295/8295 exact). Two items remain, both POST-DEMO (the by-year table is suppressed for the demo via RD; the AUA-by-Tax-Status bar + reconciled totals carry the panel). The reconciliation is the foundation; this TO is the remaining display-granularity + edge-case work.
  </context>

  <scope>
    1. PER-YEAR ATTRIBUTION CORRECTNESS (the real open item): the per-(account,ticker) total reconciles to canonical exactly, but the split ACROSS purchase years is best-effort because the transaction history doesn't net to positions. Current convention = proportional scaling, which produces artifacts (Peter Lee 2025 shows -$5.23M, 2026 holds 49% of the book). FIFO-oldest doesn't help (concentrates more in recent years). Proper fix likely needs EITHER real acquisition-date lot data (custodian lot feed) OR an explicit product decision to label the by-year split "estimated." Make the by-year splits reflect real per-year performance before RD un-hides the table. Route through CVO /verify-channel.
    2. $0.87M RESIDUAL: 21 of 23,010 (account,ticker) where lot-ticker != canonical-ticker representation don't anchor (0.995x not 1.000x). Add ticker normalization between lots and canonical holdings so they match; closes the residual to ~1.000x.
  </scope>

  <acceptance_criteria>
    AC1: per-year by-year splits reflect real acquisition-year cost basis (not a scaling artifact), OR an explicit "estimated attribution" product label is agreed + applied.
    AC2: ticker-normalization closes the $0.87M residual (by-year total reconciles to canonical ~1.000x).
    AC3: CVO /verify-channel empirical PASS on the per-year shape + total.
    AC4: RD un-hides the by-year table once AC1-AC3 land.
  </acceptance_criteria>

  <notes>
    Reconciliation (cash handling + canonical-anchor) is DONE + verified — folded in as complete. This TO is the per-year attribution + residual tail only. No rush; demo is covered by suppress.
  </notes>
</task_order>
