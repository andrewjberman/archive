<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-003b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_49FNV3-003</thread_serial>
    <thread_ref>org/threads/ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re/</thread_ref>
  </metadata>

  <objective>
    Replace the ghost bar projection model with a dashed horizontal line at the projected value
    for the last bar in the AUA and NNA chart views. The ghost bar approach fails to communicate
    downward projections (ghost = max(0,...) means no visual when projected value is below actual).
    A dashed horizontal line works in both directions: green if projected is above actual, red if
    below. This applies to AUA and NNA views in PartnerAnalytics.tsx. GRO already uses dashed
    line projection (Total-only) per ADVI_49FNV3.003 — keep that as-is.

    This task order SUPERSEDES the ghost bar requirements from ADVI_49FNV3.003. The GRO chart
    redesign, GRO hero metrics, GRO tooltip, and AUA/NNA tooltip format changes from .003 still
    stand — only the AUA/NNA projection VISUAL changes from ghost bars to dashed lines.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">AUA projection visual: Remove the ghost bar extensions (translucent stacked
      bars at 25% opacity). Replace with a dashed horizontal ReferenceLine at the projected total
      AUA value for the last displayed period. The line should span the width of the last bar only
      (or the full chart width — whichever is cleaner in Recharts).
      - Green dashed line if projected total AUA > actual total AUA (upward projection).
      - Red dashed line if projected total AUA < actual total AUA (downward projection).
      - No line if period is complete or projection unavailable.</requirement>

    <requirement id="2">NNA projection visual: Same pattern. For NNA gross mode, show dashed
      horizontal lines for projected inflows and projected outflows (or just projected net — use
      judgment on which is clearest). For NNA net-only mode, show projected net as dashed line.
      - Green if projected net > actual net.
      - Red if projected net < actual net.</requirement>

    <requirement id="3">Keep the full-history prior lookup for AUA (the allSortedAuaPeriods
      pattern from .003). The projection FORMULA is unchanged — only the VISUAL changes from
      ghost bar to dashed line.</requirement>

    <requirement id="4">Remove all _ghost dataKeys, ghost Bar components, and ghost-related
      tooltip filtering from AUA and NNA chart rendering. The augmentedAuaData and augmentedNnaData
      memos should compute projected values (not ghost increments) and store them as e.g.
      _projectedTotal, _projectedInflow, _projectedOutflow, _projectedNet for tooltip consumption.</requirement>

    <requirement id="5">AUA/NNA tooltip "Projected Full Period" section: Instead of computing
      projected from actual + ghost, read the stored projected values directly. Show:
      - "Projected Total: $P (currently $A)" for AUA.
      - "Projected Inflows: +$P / Outflows: -$P / Net: +/-$P (currently ...)" for NNA gross.
      Format per ADVI_49FNV3.003 thread spec (full values, not increments).</requirement>

    <requirement id="6">GRO: No changes to the GRO chart from .003. GRO already uses dashed line
      for Total-only projection. Keep as-is.</requirement>

    <requirement id="7">Edge cases (unchanged from .003):
      - No prior period in full history: no projection line, tooltip shows "Projection unavailable
        (insufficient history)".
      - Period complete (elapsedDays >= totalDays): no projection line.
      - Projection formula unchanged: delta-based for AUA, ratio-based for NNA flows.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">AUA Monthly/Quarterly/Annual: last bar has a dashed horizontal line at
      projected total AUA. Green if up, red if down. Line visible in all three granularities
      when the last period is incomplete.</criterion>
    <criterion id="2">NNA: last bar has a dashed horizontal line for projected net (at minimum).
      Green/red by direction.</criterion>
    <criterion id="3">No ghost bars remain in AUA or NNA charts. No _ghost dataKeys in the
      Bar components.</criterion>
    <criterion id="4">Tooltip shows full projected values with "(currently ...)" parentheticals.
      No "(add)" rows.</criterion>
    <criterion id="5">GRO chart unchanged from .003 (stacked bars + total line + dashed projection).</criterion>
    <criterion id="6">bunx tsc -b passes clean.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Single file: PartnerAnalytics.tsx only.</constraint>
    <constraint>No backend or data contract changes.</constraint>
    <constraint>This supersedes the ghost bar visual from .003 only. All other .003 specs
      (GRO redesign, tooltips, hero metrics) remain in effect.</constraint>
    <constraint>Recharts ReferenceLine or a custom SVG element are both acceptable for the
      dashed line. Use whichever produces the cleanest result.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.2_RD_AdvisorIntelligence"
                task="ADVI_49FNV3.003.f2-projection-gro-redesign"
                status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit replacing ghost bars with dashed projection lines.
      Commit message: "0.4.2_RD_AdvisorIntelligence: ADVI_49FNV3.003b -- projection dashed line replaces ghost bars"</deliverable>
  </deliverables>

  <references>
    <ref type="thread">org/threads/ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re/</ref>
    <ref type="task_order">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_49FNV3.003.f2-projection-gro-redesign.md</ref>
  </references>
</task_order>
