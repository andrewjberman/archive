<task_order>
  <metadata>
    <id>ADVI_49FNV3.F2.projected-bars</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement F2: projected ghost bars for the current incomplete period in the Assets Overview panel
    (AUA view, NNA view, GRO view). This is a frontend-only change — no Lambda or DS work required.
    The portal already has all the data needed.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">For the current incomplete period, compute the projected full-period value:
      `projected = actual * (total_period_days / elapsed_days)`. Apply constraint: the projection is
      capped at 1.5x the prior completed period's value in either direction. The ghost portion
      (projected minus actual) renders as a faint translucent extension of the bar at ~20-30% opacity
      using the same color as the bar.</requirement>
    <requirement id="2">AUA view: NMEC bar and NMNC bar each get ghost extensions upward.</requirement>
    <requirement id="3">NNA view: Inflows bar (blue ghost), Outflows bar (red ghost, extends downward).
      The Net dash/marker does not get a ghost — it shows only the partial actual.</requirement>
    <requirement id="4">GRO view: Each of the 3 lines (market, NNA, total) gets a dashed extension to
      the projected value for the current period. The dashed segment should visually distinguish
      projection from actuals.</requirement>
    <requirement id="5">Applies across all granularities: monthly, quarterly, annually.</requirement>
    <requirement id="6">Ghost bars must NOT appear for any completed period — only the most recent
      incomplete period gets the extension.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Ghost bar visible for current partial period on all three views.</criterion>
    <criterion id="2">Ghost disappears on any completed period. No ghost on historical bars.</criterion>
    <criterion id="3">1.5x cap works: a 2-day-old month does not show an absurd projection spike.</criterion>
    <criterion id="4">GRO view shows dashed line extension, not a solid bar.</criterion>
    <criterion id="5">Portal DEV commit with `--author` flag. DE to review before DT pushes to PROD.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No backend changes. This is computed entirely from data already in the portal dataset.</constraint>
    <constraint>Do not change the chart structure for completed periods.</constraint>
    <constraint>DE must review the commit before DT pushes to PROD.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit implementing ghost bars on all 3 views.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
