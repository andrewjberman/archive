# ADVI_NNAFEE.002 — RD: Fee Efficiency Views at N1/L2/L3 (REWRITTEN)

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-nnafee-002-rd-v2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit b049089. 3 new components + CanonicalBookView level prop. -->
    <project_code>ADVI_NNAFEE</project_code>
    <priority>high</priority>
    <phase>2</phase>
  </metadata>

  <objective>
    Build 3 new components for fee efficiency at 3 drill levels in Books tab,
    and modify CanonicalBookView to render them conditionally by level.
    This REPLACES the original .002 scope (standalone scatter+table+drilldown).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_NNAFEE_FEE_EFFICIENCY_VIEWS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    ## Component 1: N1 FeeEfficiencyPanel (replaces TaxCostBasisPanel at firm level)

    Recharts ScatterChart:
    - X = nna_trailing_12m, Y = implied_revenue_trailing_12m
    - Dot size = managed_aua (min 6px, max 24px)
    - Dot color = book_growth_rate gradient (red < 0%, gray 0-5%, green > 10%)
    - Dashed regression line (white/30) with slope + R^2 annotation
    - Hover tooltip: advisor, AUA, NNA, revenue, fee yield bps
    - Click dot: navigate to L2 (same as advisor table click)
    - Toggle: [Scatter / Table] — table view is ranked sortable (Advisor, Roles, AUA, Revenue, NNA, Growth, Efficiency, vs Expected)

    Data source: FeeEfficiencyResponse from getAdvisorFeeEfficiency()

    ## Component 2: L2 FeeRoleBreakdownPanel (left half of Row 3 at advisor level)

    ApexCharts donut showing role AUA breakdown:
    - Segments: architect, implementor, consultant, other
    - Below donut: role legend with fee bps and AUA per role
    - Headline: "Wtd Avg Fee: XX bps"

    Data source: fee_summary.by_role from AdvisorBookResponse

    ## Component 3: L3 FeeSummaryPanel (left half of Row 3 at relationship level)

    Fee summary with per-account table:
    - Headlines: weighted_avg_fee_bps, annual_implied_revenue
    - Table: account_id | fee_bps | aua

    Data source: fee_summary.by_account from BooksClientDetailResponse

    ## Component 4: Modify CanonicalBookView

    Add a `level` prop: 'n1' | 'l2' | 'l3' | 'l4'
    Row 3 rendering logic:
    - N1: FeeEfficiencyPanel (full width, replaces TaxCostBasisPanel)
    - L2: grid-cols-2 gap-4 — FeeRoleBreakdownPanel (left) + condensed TaxCostBasisPanel (right)
    - L3: grid-cols-2 gap-4 — FeeSummaryPanel (left) + full TaxCostBasisPanel (right)
    - L4: TaxCostBasisPanel full width (unchanged)
  </scope>

  <requirements>
    <requirement id="1">Read the full PRD: docs/architecture/ADVI_NNAFEE_FEE_EFFICIENCY_VIEWS.md</requirement>
    <requirement id="2">Read org/ref/design/PORTAL_DESIGN_QA.md before writing any components</requirement>
    <requirement id="3">All chart colors from @/lib/chartColors — no hardcoded hex</requirement>
    <requirement id="4">Control labels use canonical pattern: text-xs text-white/50 tracking-wider</requirement>
    <requirement id="5">Scatter dot gradient: PALETTE.red500 (negative growth) -> PALETTE.gray500 (flat) -> PALETTE.green500 (strong growth)</requirement>
    <requirement id="6">Regression line: dashed stroke, white/30 opacity</requirement>
    <requirement id="7">Run bun run build after each component. Commit after each logical chunk.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">N1 shows scatter plot with regression line, toggle to table view works</criterion>
    <criterion id="2">L2 shows donut + condensed tax side by side in grid-cols-2</criterion>
    <criterion id="3">L3 shows fee table + full tax side by side in grid-cols-2</criterion>
    <criterion id="4">L4 unchanged (full width TaxCostBasisPanel)</criterion>
    <criterion id="5">CanonicalBookView accepts level prop and renders correctly at each level</criterion>
    <criterion id="6">bun run build succeeds</criterion>
    <criterion id="7">Zero hardcoded hex, design QA compliant</criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_NNAFEE-001" status="complete">Types and endpoint must exist before RD can consume them</dependency>
  </dependencies>

  <commit_pattern>feat(Books): fee efficiency views at N1/L2/L3 drill levels</commit_pattern>
</task_order>
