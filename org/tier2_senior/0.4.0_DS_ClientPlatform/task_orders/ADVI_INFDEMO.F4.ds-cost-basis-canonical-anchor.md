<task_order>
  <metadata>
    <id>ADVI_INFDEMO.F4</id>
    <slug>ds-cost-basis-canonical-anchor</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-28</date>
    <status>complete</status>
    <reconcile_2026_06_01>DONE -- cost-basis canonical anchor shipped + verify-channel PASS-mechanical, ship-gate (a)-(d) met (a8be3399e, b570b342a). Per-year-display concern spun to F4-followon. (was: in_progress)</reconcile_2026_06_01>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P1 — demo-critical; IWM demo early afternoon 2026-05-28; Andrew Q2=table IS shown</priority>
    <sla>race full-speed; ship-vs-caveat decided by COO on CVO verify result</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFDEMO.md §F4 (CTO)</ref>
    <ref type="prior">docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md (INFFIN.019, 08e9e4301) — diagnosed the OLD $1.31B raw-buy-sum; INFFIN.020 Fix A swapped CBBY to canonical_lots ($274M). This TO is the NEW finding beyond that.</ref>
    <ref type="cto_disposition">1.0.0_SA_CTO 134722Z + 135200Z</ref>
    <ref type="surface">Inflection portal -> AdvisorIntelligence -> Books -> Cost Basis &amp; Tax Status -> Cost Basis by Year table</ref>
  </references>

  <root_cause>
    The Cost Basis by Year table is built from gold/lots/lots_latest.parquet (INF_B_02.canonical_lots.py), a FIFO reconstruction from silver/transactions. The transaction history does NOT reconcile to Orion's authoritative positions API (gold/canonical/holdings):
    - cash-sweep funds (FDRXX/FCASH/...) record buy-side sweep-ins but no sell-side sweep-out on the fund ticker -> FIFO never disposes -> entire inflow history accretes (~90% of excess);
    - disposed/transferred-out positions lack a captured close type_desc -> 14,795 phantom (account,ticker) pairs carried as live lots;
    - "Merge Out Exchange" and similar outflows were UNCLASSIFIED (not in SELL_DESCS);
    - some securities UNDER-retain (buy history predates the silver window).
    Net: 3.15x unit over-retention (Peter Lee: 51.6M lot units vs 16.4M canonical), by-year cost_basis $274M / MV $288M vs true book $166M. Empirically, chasing missing SELL_DESCs closes only ~6% (206K of 3.55M residual units) — FIFO-from-txns structurally cannot tie to the positions API.
  </root_cause>

  <fix>
    INF_B_02 now loads gold/canonical/holdings_* as the authoritative position ANCHOR and uses the FIFO lots only to ATTRIBUTE that position across purchase years. Per (account,ticker):
    - absent from canonical / H&lt;=0  -> drop all lots (kills phantom positions);
    - traceable lots exist            -> scale every remaining unit by H/total (sum to H exactly; preserves purchase-year + blended cost-per-unit; buy_price unchanged);
    - H&gt;0 but zero traceable lots    -> one residual lot at canonical unit price (cost == MV, no spurious gain), bucketed to LOT_FLOOR_YEAR (untraceable acquisition predates the txn window).
    Fail-open: empty anchor (artifact unavailable) skips the clamp -> raw FIFO (no regression vs prior behavior). One rule subsumes cash-sweep + missing-SELL_DESC + phantom + under-retention.
  </fix>

  <validation>
    Local dry-run (edited INF_B_02 on live silver/transactions/2026-05-28 + canonical anchor), Peter Lee scope:
    - by-year MV $165.2M vs canonical $166.1M = 0.995x (was 3.15x)
    - by-year cost_basis $162.8M (just below MV per acceptance bar); overall unrealized gain +$2.43M
    - 22,989 of 23,010 (account,ticker) reconciled; 21 residual mismatches (~$0.9M, ticker-key representation edge cases)
    - ds-commit-gate.sh PASS (py_compile + AST undefined-name + ruff py39)
  </validation>

  <open_flags>
    1. Residual 0.995x (21 positions where lot-ticker != canonical-ticker representation don't anchor; ~$0.9M). Not demo-blocking; tighten post-demo via ticker normalization.
    2. Per-YEAR rows shift under proportional scaling (e.g. Peter 2025 now -$5.2M vs old +$2.3M). TOTAL is correct (+$2.43M); per-year is an attribution convention (proportional vs FIFO-oldest). CVO to sanity-check per-year shape; convention switchable if a year reads oddly in the demo.
  </open_flags>

  <deploy>
    Cycle (Rules 13/14): safe-commit INF_B_02 -> safe-deploy (push CLOUD + S3 upload + comp-pipescript deployed MATCH) -> run INF_B_02 (regen gold/lots/lots_latest) -> run INF_D_02 (regen advisor book.json) -> CF refresh. Then route live book.json to CVO /verify-channel for empirical sign-off. COO decides ship-vs-caveat on the verify result; caveat-fallback = FE suppress/caveat the by-year table (AUA-by-Tax-Status bar carries the panel).
  </deploy>

  <acceptance_criteria>
    AC1: INF_B_02 anchors lot current_units to canonical holdings per (account,ticker). [DONE]
    AC2: ds-commit-gate.sh PASS. [DONE]
    AC3: Peter Lee by-year MV reconciles to ~$166M, cost_basis just below MV. [DONE — 0.995x]
    AC4: Code committed + deployed; lots_latest + book.json regenerated live.
    AC5: CVO /verify-channel empirical PASS on live artifact.
    AC6: COO ship-vs-caveat decision recorded.
  </acceptance_criteria>

  <ravc>DS RAVC2 to COO + CC CTO + CVO on AC4 regen complete; CVO verify gates AC5; COO AC6.</ravc>
</task_order>
