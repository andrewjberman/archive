<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-039-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~A</issued_to>
    <date>2026-04-09</date>
    <status>COMPLETE -- fix_1 + fix_2 done (commit d6eb8ec DEV). fix_3 held per COO instruction.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>9</wave>
    <phase>Advisors tab UX polish</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Enrich the AUA and GRO bar chart tooltips in the Advisors tab with contextually
    meaningful data. Both tooltips are currently minimal (name + one value).
    All required fields already exist on LeaderboardEntry -- this is a pure frontend change.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx

    Current state:
      AUA tooltip (line ~877): name + AUA only
      GRO tooltip (line ~951): name + growth % only

    Both chart data objects are sparse -- they need to be enriched from the full
    LeaderboardEntry to pass context through to the tooltip render function.

    LeaderboardEntry fields available (all already present, no DS work needed):
      total_aua, aua_growth_pct, nna, inflows, outflows, client_count,
      account_count, new_clients, name, advisor_id, roles, role_breakdown

    Derived in DE (no new platinum field needed):
      period_start_aua = total_aua / (1 + aua_growth_pct / 100)
        -- this is the AUA at the start of the selected window, back-calculated
        -- use toFixed(0) rounding; precision is sufficient for a tooltip display
      growth_value = total_aua - period_start_aua
        -- dollar value of the growth over the period
  </context>

  <fix_1 label="GRO tooltip -- enrich chart data and redesign tooltip layout">
    <description>
      Step 1: Enrich the GRO chart data object (line ~917-922).
      Currently: { name, growth }
      Change to: { name, growth, total_aua, period_start_aua, growth_value }
        const period_start_aua = e.aua_growth_pct !== -100
          ? e.total_aua / (1 + e.aua_growth_pct / 100)
          : 0
        const growth_value = e.total_aua - period_start_aua

      Step 2: Redesign the GRO tooltip content (line ~954-967).
      Layout:

        ┌─────────────────────────────────┐
        │  {Advisor Name}   [bold, white] │
        ├─────────────────────────────────┤
        │  Period Start    $XXX.X M       │  ← white/50, right-aligned value white/80
        │  Current AUA     $XXX.X M       │  ← white/50, right-aligned value white (brighter)
        ├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤  (light divider)
        │  Growth          +X.X%          │  ← label white/50, value colored green/red, font-bold
        │  Growth Value    +$XX.X M       │  ← label white/50, value colored green/red
        └─────────────────────────────────┘

      Implementation notes:
        - Use the existing two-column flex layout pattern (label left, value right, gap-6)
          already established in the NNA tooltip (lines ~467-489). Match that spacing.
        - Color for growth and growth_value: emerald-400 if positive, red-400 if negative.
          Use the same color for both rows so they read as a paired decomposition.
        - Period Start and Current AUA rows use white/80 for the value (neutral -- not colored).
        - The divider between the AUA rows and the growth rows is a subtle border-t border-white/10.
        - "Period Start" label = first day of the selected window (QTD/YTD).
          Do not compute a date -- just label it "Period Start". The window label is
          visible from the toggle above the chart.
        - Formatting: use formatCurrency for all dollar values. Use toFixed(1)% for growth %.
          Prefix growth values with '+' when positive.
    </description>
  </fix_1>

  <fix_2 label="AUA tooltip -- add client and account context">
    <description>
      Step 1: Enrich the AUA chart data object (line ~917 area for AUA view).
      Currently: { name, aua, color }
      Change to: { name, aua, color, client_count, account_count, new_clients }

      Step 2: Redesign the AUA tooltip (lines ~877-890).
      Layout:

        ┌─────────────────────────────────┐
        │  {Advisor Name}   [bold, white] │
        ├─────────────────────────────────┤
        │  Total AUA       $XXX.X M       │  ← main value, white, slightly larger text (text-sm)
        ├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
        │  Clients             NNN        │  ← white/50 label, white/80 value, text-xs
        │  Accounts            NNN        │
        │  New Clients          NN        │  ← "this period" implied by the window toggle
        └─────────────────────────────────┘

      Implementation notes:
        - Total AUA row: text-sm font-semibold, no color (white). Stands out as the
          primary metric. No dot/color swatch needed -- it is the only primary value.
        - Clients / Accounts / New Clients: use the same two-column layout as GRO.
          Values are integers -- no formatCurrency, just toLocaleString() or plain number.
        - New Clients labeled as "New Clients" with no further qualifier.
          If new_clients is 0 for this advisor in the window, still show it ("0").
        - Keep the tooltip compact -- four rows total plus the name header.
    </description>
  </fix_2>

  <fix_3 label="Shared tooltip container style">
    <description>
      Both tooltips currently use slightly different padding:
        AUA:  px-3 py-2
        GRO:  px-3 py-2
        NNA:  px-4 py-3
      Standardize to px-4 py-3 across all three for visual consistency.
      Min-width: 200px on both so they don't collapse on short advisor names.
      Add min-w-[200px] to the tooltip container div.
    </description>
  </fix_3>

  <acceptance_criteria>
    1. GRO tooltip shows: advisor name / Period Start AUA / Current AUA / divider /
       Growth % / Growth Value -- all correctly formatted and colored
    2. AUA tooltip shows: advisor name / Total AUA / divider / Clients / Accounts / New Clients
    3. Both tooltips use px-4 py-3 padding and min-w-[200px]
    4. Color logic: green for positive growth, red for negative, neutral for AUA values
    5. No TypeScript errors -- chart data types updated to include the new fields
    6. No DS changes required -- all data sourced from existing LeaderboardEntry fields
  </acceptance_criteria>


  <compiler_tools>
    comp-transform trace AdvisorsTab
      -- Run before coding. Shows exactly which LeaderboardEntry fields are already
         flowing into the chart data objects vs which ones need to be added.
         Tells you whether total_aua, client_count, account_count, new_clients are
         accessible at the tooltip render site or need to be threaded through.
         Saves reading the full data flow manually.
  </compiler_tools>

</task_order>
