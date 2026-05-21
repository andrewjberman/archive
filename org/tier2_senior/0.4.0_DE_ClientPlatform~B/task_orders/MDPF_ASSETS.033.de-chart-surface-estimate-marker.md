<task_order>
  <metadata>
    <id>MDPF_ASSETS.033</id>
    <slug>de-chart-surface-estimate-marker</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-05-21 (authored as the .031 chart-surfacing follow-on -- CTO~B ruling: stub now, parked)</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>HELD -- no live 0.4.0_DE_ClientPlatform~B session exists. Authored now as a hard artifact (CTO~B ruling 2026-05-21: a real TO file beats "author it later") so the chart-surfacing follow-on cannot be dropped. GO when Andrew spins up the DE~B session -- it bundles with the VALGATE Phase-2 DE~B set (ADHC_VALGATE.004-.006) for a single DE~B engagement. COO~B flips dispatch_held=false + GOs at that point. || DISPATCHED 2026-05-21 by 1.0.0_SA_CTO~B -- Andrew brought 0.4.0_DE_ClientPlatform~B online; COO~B closed, so CTO~B (the remaining ~B exec) GOs the bundle. Sequenced P3/LAST after the VALGATE Class-D suite (.004/.005 P1, .006 P2). RAVC2 to CTO~B (not COO~B -- closed).</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P3 -- a portal FE marker-render follow-on; the underlying MDPF v0.9 data + the data-layer marker it keys on are already shipped. Not on any critical path.</priority>
    <sla>~1-2h DE wall -- a focused chart-component change keyed on an existing data field.</sla>
  </metadata>

  <references>
    <origin>MDPF_ASSETS.031 (2024-depth v0.9 backfill) AC2 -- the marked-estimate segment must be "chart-surfaced": the Model Portfolios Daily AUA Analysis chart visibly flagging the pre-2025-12-23 estimated extension. .031 delivered the DATA-layer marking (per-partition meta.estimate_tier="2024_depth_extension" + the rollup); the chart VISUAL render is a separate portal/DE-lane task -- correctly outside DS scope. CTO~B carved it out as this tracked follow-on.</origin>
    <data_hook>The render keys on existing shipped data: every aggregate_aua/{date}.json partition for 2024-11-01..2025-12-22 carries meta.estimate_tier="2024_depth_extension"; aggregate_aua_timeseries.json spans 2024-11-01..present. The .031 estimated segment is the clean constant range 2024-11-01..2025-12-22 (boundary 2025-12-23 = the .029 reconciled floor). No new data work -- the hook is in place.</data_hook>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9.</prd>
  </references>

  <context>
    The Model Portfolios "Daily AUA Analysis" chart now renders a continuous v0.9 trend back to 2024-11-01. The segment 2024-11-01..2025-12-22 is a marked best-estimate (RPS-based, no in-range crosswalk anchor -- per the .031 Option-A clamped-fit calibration, Andrew informed-YES); the segment from 2025-12-23 forward is the crosswalk-reconciled .029/.028 series. A chart reader must be able to SEE where the reconciled series ends and the estimated extension begins. .031 shipped the per-partition data marker; this TO makes the chart render it.
  </context>

  <scope>
    <step>In the Model Portfolios page chart component (portal/src/pages/ModelPortfolios.tsx -- the Daily AUA Analysis chart; DE confirms the exact component at GO time), visually distinguish the estimated 2024-depth segment (2024-11-01..2025-12-22) from the reconciled segment (2025-12-23 onward). Treatment is a DE design call -- e.g. a dashed/lighter line weight, a shaded band, or a legend annotation -- such that a reader plainly sees the boundary.</step>
    <step>Key the visual treatment on the data the .031 backfill already ships -- the per-partition meta.estimate_tier (or the constant boundary date 2025-12-23) -- not a hardcoded magic range duplicated in the FE.</step>
    <step>Portal-submodule work: portal DEV branch; standard portal build/verify; no parent-repo data change.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">The Daily AUA Analysis chart visibly distinguishes the estimated 2024-depth segment (2024-11-01..2025-12-22) from the reconciled segment -- a reader can see where the reconciled series ends and the marked estimate begins.</ac>
    <ac id="AC2">The visual treatment is driven by the data (estimate_tier / the boundary date), not a hardcoded FE range.</ac>
    <ac id="AC3">Portal DEV branch; portal build clean; no parent-repo change. Session log; RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Daily AUA Analysis chart visually flagging the estimated 2024-depth segment. RAVC2 to COO~B CC CTO~B.
  </deliverables>
</task_order>
