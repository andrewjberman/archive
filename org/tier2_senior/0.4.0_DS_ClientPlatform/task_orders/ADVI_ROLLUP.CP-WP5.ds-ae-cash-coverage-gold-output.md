<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-WP5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-17</date>
    <status>staged</status><!-- Flip to active after CP-DS1 ships. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P0 behind CP-AE1 + CP-DS1 — required for Gate 2 (full firm AUA recon)</priority>
  </metadata>

  <context>
    B_01.holdings_lots does NOT emit cash lots. After CP-DS1 ships, gold chain produces non-cash
    AUA only (~$1,660,325,207 from silver/allocations/2026-04-15). Firm headline total_aua is
    $1,694,648,746 — the $34,323,539 difference is cash positions (2.03% of firm AUA).

    Andrew's completion target ("everything mapped") requires the full firm AUA to reconcile
    against silver/allocations. Cash coverage is the last gap.

    Gate 1 (CP-DS1): non-cash MV within 2% of $1,660,325,207. COMPLETED by CP-DS1.
    Gate 2 (this TO): (non-cash + cash) within 2% of $1,694,648,746 headline.
  </context>

  <objective>
    Add cash lot coverage to the gold chain so that the full firm-level total_aua
    (non-cash holdings_lots + cash positions) reconciles to silver/allocations headline.

    Scope: design the cash coverage path in coordination with DS + AE. Two candidate approaches:
      (a) Add cash rows to B_01.holdings_lots output (simplest — single emitter)
      (b) Separate cash aggregation script feeding into the downstream AUA rollup
    CTO to advise preferred approach before DS writes code.
  </objective>

  <acceptance_criteria>
    1. Gold firm total_aua (non-cash + cash) within 2% of silver/allocations/2026-04-15 headline $1,694,648,746.
       2% band: $1,660,755,771 – $1,728,541,721.
    2. All 6,543 accounts have a complete position record (no accounts with only cash and no lots).
    3. cash coverage adds no regressions to existing non-cash consumers (B_01b, C_02, C_03, C_05, C_06, C_07).
    4. comp-validate exits 0 on gold output including cash rows.
    5. MCP COMPLETE to COO with: gate 2 recon figure, commit hash, account coverage count.
  </acceptance_criteria>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-DS1" status="staged"
      description="CP-DS1 must ship and validate first. Cash coverage builds on a clean non-cash foundation."/>
  </dependencies>

  <next>
    CP-WP5 COMPLETE = full firm AUA Gate 2 reached. ADVI_ROLLUP gold chain is operationally complete.
    BD_FORCE_CLOSE_OVERRIDE permanently off. Nightly runs clean at ~$1.69B firm total_aua.
  </next>
</task_order>
