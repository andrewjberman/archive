<task_order>
  <metadata>
    <id>0.4.2_RD_AdvisorIntelligence-2026-04-16-advi-fntend-rd3-fee-scatter-consolidation</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-16</date>
    <status>active</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>RD3</wave>
  </metadata>

  <references>
    <ref type="ds_to">ADVI_FNTEND.B10.ds-fee-scatter-small-account-avg-aua.md — DS emits
    small_account_avg_aua on every advisor entry in advisor_fee_efficiency.json</ref>
    <ref type="source_file">portal/src/pages/AdvisorIntelligence/tabs/FeeEfficiencyPanel.tsx</ref>
  </references>

  <context>
    FeeEfficiencyPanel has one scatter mode today: NNA (x) vs commission (y), log-log,
    dot size proportional to AUA, color encodes efficiency percentile. ViewMode
    ('scatter' | 'table') is the existing outer toggle.

    The new mode surfaces "Consolidation Opportunity": which advisors have the most
    small accounts AND how hard is each one to fix? The second axis — average AUA of
    small accounts — answers that directly. Advisors near the top-right of the chart
    (many small accounts, avg AUA near $40K) are easy wins; bottom-right are structural
    problems.

    FeeEfficiencyAdvisor already maps small_account_count (line 236). small_account_avg_aua
    will be available once DS B10 ships. FE should read it with a fallback of 0.

    Existing data shape (FeeEfficiencyAdvisor, already typed):
      small_account_count: number (from B9, live)
      small_account_avg_aua: number (from B10, pending DS — render gracefully until it lands)
  </context>

  <objective>
    Add a "Consolidation" scatter sub-mode to FeeEfficiencyPanel. The outer ViewMode
    toggle ('scatter' | 'table') stays unchanged. Add a ScatterMode sub-toggle that
    appears only when viewMode === 'scatter'.

    --- Step 1: Type + state ---
    Add type:
      type ScatterMode = 'efficiency' | 'consolidation'

    Add state (default 'efficiency' so nothing regresses):
      const [scatterMode, setScatterMode] = useState<ScatterMode>('efficiency')

    Extend FeeEfficiencyAdvisor (or wherever the mapped advisor type is inferred)
    to include:
      small_account_avg_aua: number   // 0 fallback if field absent from artifact

    In the advisor mapping (around line 236), add:
      small_account_avg_aua: a.small_account_avg_aua ?? 0,

    --- Step 2: ScatterMode sub-toggle ---
    Render a two-option toggle ("Efficiency" / "Consolidation") inside the scatter
    header, visible only when viewMode === 'scatter'. Match the existing toggle
    component style (same variant as the Scatter/Table toggle).

    --- Step 3: Consolidation scatter data ---
    When scatterMode === 'consolidation', derive scatterData as:
      const valid = filteredAdvisors.filter(a => a.small_account_count > 0)
      scatterData = valid.map(a => ({
        x: a.small_account_count,           // integer, linear axis
        y: a.small_account_avg_aua,         // dollars, linear axis
        z: a.aua,                           // dot size proportional to book AUA
        name: a.advisor,
        role: a.role,
        fill: ADVISOR_ROLE_COLORS[a.role] ?? PALETTE.slate500,
      }))

    Advisors with small_account_count === 0 are excluded from this scatter
    (the chart is only about the consolidation problem population).

    Color encodes ROLE (not efficiency percentile) — ADVISOR_ROLE_COLORS from
    lib/chartColors.ts. This makes the chart readable: you can see whether smalls
    are concentrated in a particular role type.

    --- Step 4: Consolidation scatter render ---
    When scatterMode === 'consolidation', replace the existing ScatterChart with:

    Axes (LINEAR, not log-log):
      XAxis: dataKey="x", label "Small Accounts", tickLine, integer ticks
      YAxis: dataKey="y", label "Avg AUA of Small Accounts",
             tickFormatter={v => `$${(v/1000).toFixed(0)}K`}

    Reference line:
      A horizontal ReferenceLine at y=35_000 with label "Near Threshold"
      and a dashed stroke in slate/40. This separates "easy consolidations"
      (above the line) from "structural problems" (below).

    Dot style:
      fill from scatterData[i].fill (role color)
      stroke="transparent"
      opacity={0.85}
      r computed from z (AUA) same formula as efficiency scatter

    Tooltip:
      Advisor name
      Role (formatted label, e.g. "Architect")
      Small Accounts: {x}
      Avg Small AUA: ${y.toLocaleString(undefined, {maximumFractionDigits: 0})}
      Book AUA: ${formatAua(z)}

    Empty state: if scatterMode === 'consolidation' and valid.length === 0,
    render a centered message "No advisors with small accounts in selected roles."

    --- Step 5: helpText update ---
    When scatterMode === 'efficiency': existing helpText unchanged.
    When scatterMode === 'consolidation':
      helpText="Scatter: number of small accounts (x, below $40K threshold) vs.
      average AUA of those accounts (y). Dot size proportional to book AUA, color
      by role. Top-right = many small accounts near threshold (easy consolidations).
      Bottom-right = structurally fragmented book. Reference line at $35K."
  </objective>

  <acceptance_criteria>
    1. Efficiency mode renders identically to today — no regression (log-log NNA vs
       commission, percentile coloring, existing helpText).
    2. Consolidation mode: ScatterMode sub-toggle visible in scatter header.
    3. Consolidation scatter: advisors with small_account_count === 0 are absent.
    4. Reference line renders at y=35_000 with "Near Threshold" label.
    5. Dot color encodes role via ADVISOR_ROLE_COLORS.
    6. Tooltip shows name, role, Small Accounts count, Avg Small AUA, Book AUA.
    7. Empty state message renders when no advisors with small accounts exist in
       selected roles.
    8. bun run build exit 0.
    9. comp-transform schema-check FeeEfficiencyPanel: small_account_avg_aua USED
       (not MISSING). If B10 artifact not yet landed, field reads 0 from fallback —
       chart renders with all dots at y=0, which is expected pending DS emit.
    10. MCP COMPLETE to COO with commit hash + screenshot description of both modes.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check FeeEfficiencyPanel</run>
        <expect>small_account_count USED (existing). small_account_avg_aua likely
        MISSING (not yet in artifact). Note baseline — after B10 lands it will flip
        to USED.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run build</run>
        <expect>Exit 0. No TypeScript errors on new ScatterMode type or mapped field.</expect>
      </step>
      <step>
        <run>comp-transform schema-check FeeEfficiencyPanel</run>
        <expect>small_account_avg_aua USED (field is read by consolidation scatter).
        No new MISSING fields vs B10 pre-land baseline.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <notes>
    - DS B10 (small_account_avg_aua emit) is dispatched in parallel. FE does NOT
      need to wait for B10 — implement with fallback a.small_account_avg_aua ?? 0
      so the toggle and scatter structure are live. The chart will show y=0 for all
      dots until B10 artifact lands; this is expected and documented in helpText.
    - ADVISOR_ROLE_COLORS import: already in FeeEfficiencyPanel via chartColors.ts.
    - ReferenceLine: already imported from recharts (ScatterChart usage in scope).
    - Do NOT change the outer ViewMode toggle. ScatterMode is a sub-toggle, subordinate
      to viewMode === 'scatter'.
  </notes>
</task_order>
