# ADVI_REBORN.W3-001 — RD: Upgrade AUA Mix legend to match AUA Client card structure

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w3-001-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit cd7f023. Card structure with QoQ changes, color-tinted, click-to-filter preserved. -->
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS3</phase>
  </metadata>

  <objective>
    Upgrade the AUA (Mix) legend in the Assets Overview panel (ClientsTab.tsx)
    to use the same nested container/card structure as the AUA (Client) quarterly
    cards. Currently it's flat buttons with color dot + label + value + pct.
    It needs to be structured cards with period values, period-over-period change
    in both percentage and absolute value, color-coded like the Client version.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_PRD.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <context>
    EXACT REFERENCE PATTERN (PartnerAnalytics.tsx lines 1933-1969):
    The AUA (Client) metric tiles in the PartnerAnalytics panel. Three flex-1 cards:
    - Each card: `flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg border`
    - Color-tinted background + border using withOpacity(color, 0.1) / withOpacity(color, 0.3)
    - Label: `text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2`
    - Hero value: `text-2xl font-bold` in the category color
    - Change line: `text-sm font-semibold` with +$X.XM (+X.X%) in emerald/red
    - Comparison label: `text-[9px] text-white/40 tracking-widest` e.g. "vs Q1 '26"
    
    Currently shows: "New Clients $0 -$87.9M(-100.0%) vs Q1 '26" / "Existing Clients $1.62B +$99.7M(+6.6%) vs Q1 '26" / "Total AUA $1.62B +$11.8M(+0.7%) vs Q1 '26"
    
    You want IDENTICAL structure but for: Fixed Income / Equity / Alternatives
    Each color-tinted with its mixPieColor().

    CURRENT MIX LEGEND (lines 1071-1093 of ClientsTab.tsx):
    - Simple clickable buttons: color dot + label + currency value + pct
    - No period-over-period comparison
    - No nested card structure

    DATA AVAILABLE:
    - quarterlyMix state (line 850+): array of quarterly snapshots with per-class AUA
    - composition.mix: current period with asset_class, market_value, pct
    - getClassAua() helper already exists to extract per-class AUA from quarterly data
  </context>

  <scope>
    File: portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx

    Replace the flat legend (lines 1071-1093) with card-structured legend:

    1. ORDER: Fixed Income, Equity, Alternatives (left to right) — this is the display order Andrew wants
    2. Each asset class gets a card matching the AUA Client pattern:
       - Color-coded left border or background tint using mixPieColor()
       - Asset class label
       - Current period value (formatted currency)
       - Period-over-period change: absolute value change + percentage change
       - Green for positive change, red for negative, gray for flat
    3. Wrap in the same container style: `bg-white/5 border border-white/10 rounded-lg flex`
    4. Keep the clickable behavior (clicking a class filters the donut + other panels)
    5. Use the quarterlyMix data to compute period-over-period changes (same calcQoQ pattern as the Client cards)
  </scope>

  <requirements>
    <requirement id="1">Card order must be: Fixed Income, Equity, Alternatives (left to right)</requirement>
    <requirement id="2">Each card shows: asset class name, current value, period change ($ and %), color-coded</requirement>
    <requirement id="3">Match the visual structure of the AUA Client quarterly cards (lines 866-910)</requirement>
    <requirement id="4">Keep click-to-filter behavior (onSelectAssetClass)</requirement>
    <requirement id="5">Colors from chartColors.ts mixPieColor() — no hardcoded hex</requirement>
    <requirement id="6">Commit after implementation. bun run build must pass.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Mix legend shows 3 cards in order: Fixed Income, Equity, Alternatives</criterion>
    <criterion id="2">Each card shows value + period-over-period change with color coding</criterion>
    <criterion id="3">Visual structure matches AUA Client cards (nested container/card pattern)</criterion>
    <criterion id="4">Click filtering still works</criterion>
    <criterion id="5">bun run build succeeds</criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency>None — data already available in quarterlyMix + composition.mix</dependency>
  </dependencies>

  <commit_pattern>feat(ClientsTab): upgrade Mix legend to card structure matching Client AUA pattern</commit_pattern>
</task_order>
