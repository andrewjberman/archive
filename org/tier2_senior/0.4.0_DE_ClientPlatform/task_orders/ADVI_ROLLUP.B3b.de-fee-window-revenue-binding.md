<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-16-advi-rollup-b3b-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>complete</status><!-- portal DEV 3ca28d0 2026-04-16. window_revenue + window_fee_share_usd types added. totalFirmRevenue + advisorRevenue window-bound with annualized fallback. pickAdvisorSplitBps window-aware. bun build exit 0. schema-check clean. /frontend-dev fee_summary_window PASS 1 iter. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3-addendum-B3b</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FEE_WINDOW_REVENUE.md</ref>
    <ref type="companion">ADVI_ROLLUP.B3b.ds-fee-window-revenue-d02.md — DS must ship first.
    Mark new types optional (?) until DS artifact lands on DEV, then tighten.</ref>
  </references>

  <context>
    Compiler pre-check results (run 2026-04-16 by CTO):
    - FeeSummaryPanel.tsx:215 — effectiveWindow: RfsWindow already derived from rfsWindow prop.
    - FeeSummaryPanel.tsx:359 — totalFirmRevenue hardcoded to data.annual_implied_revenue.
      This is the only change needed on the revenue read path.
    - rfsWindow flows: AdvisorBookView (state) -> AdvisorBookClientDetail (prop) -> FeeSummaryPanel (prop).
      No new prop threading needed.
    - FeeAccountTeamShare type: has fee_share_usd (annualized). No window_fee_share_usd yet.
    - FeeSummaryByAccount type: has annual_implied_revenue. No window_revenue yet.
  </context>

  <objective>
    Three changes — types + two binding sites:

    1. TYPES (portal/src/pages/AdvisorIntelligence/types.ts):

       a. Extend FeeSummaryByAccount (~line 1667):
            window_revenue?: {
              qtd: { firm_revenue_usd: number; advisor_revenue_usd: number }
              ytd: { firm_revenue_usd: number; advisor_revenue_usd: number }
              max: { firm_revenue_usd: number; advisor_revenue_usd: number }
            }

       b. Extend FeeAccountTeamShare (~line 1651):
            window_fee_share_usd?: {
              qtd: number
              ytd: number
              max: number
            }

    2. REVENUE BINDING (portal/src/pages/AdvisorIntelligence/tabs/FeeSummaryPanel.tsx):

       At line ~359, replace:
         const totalFirmRevenue = data!.annual_implied_revenue

       With:
         const totalFirmRevenue =
           data!.window_revenue?.[effectiveWindow]?.firm_revenue_usd
           ?? data!.annual_implied_revenue

       Directly below, add:
         const windowAdvisorRevenue =
           data!.window_revenue?.[effectiveWindow]?.advisor_revenue_usd ?? null

       Bind windowAdvisorRevenue wherever Advisor Revenue is rendered in the
       Relationship Summary (currently shows em-dash or annualized figure).
       Guard: only render windowAdvisorRevenue if non-null.

    3. TEAM ATTRIBUTION SPLIT BINDING (FeeSummaryPanel.tsx — per-account advisor split column):

       For each team_attribution entry, replace annualized fee_share_usd with:
         const effectiveFeeShare =
           entry.window_fee_share_usd?.[effectiveWindow] ?? entry.fee_share_usd

       Bind effectiveFeeShare in the Split bps / Advisor Revenue column of the
       Accounts Summary table.

    FALLBACK RULE: always fall back to annualized figure if window_revenue or
    window_fee_share_usd is absent. This ensures the page renders correctly
    before DS artifact lands on DEV.
  </objective>

  <wire_contract>
    FeeSummaryByAccount (types.ts):
      window_revenue?: { qtd/ytd/max: { firm_revenue_usd: number; advisor_revenue_usd: number } }

    FeeAccountTeamShare (types.ts):
      window_fee_share_usd?: { qtd: number; ytd: number; max: number }

    Read path in FeeSummaryPanel:
      effectiveWindow (already defined) drives which window slice is read.
      Fallback to annual_implied_revenue / fee_share_usd when window fields absent.
  </wire_contract>

  <acceptance_criteria>
    1. bun run build exits 0.
    2. comp-transform schema-check FeeSummaryPanel clean — no new MISSING.
       window_revenue and window_fee_share_usd appear in rendered set (not UNUSED)
       once DS artifact lands.
    3. Toggling QTD / YTD / Max on the L3 Fee Summary panel changes Total Firm Revenue value.
    4. Toggling window changes Advisor Revenue value (where team_attribution is populated).
    5. When window_revenue is absent (pre-DS-artifact), panel renders annualized figures —
       no blank/undefined/NaN values.
    6. /frontend-dev Skill invoked with fee_summary_window constitution. PASS required.
    7. MCP COMPLETE to COO with portal DEV commit hash + /frontend-dev PASS confirmation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check FeeSummaryPanel</run>
        <expect>annual_implied_revenue in rendered set. window_revenue absent (expected — DS not
        yet shipped). FeeAccountTeamShare.fee_share_usd in rendered set; window_fee_share_usd absent.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run build</run>
        <expect>Exit 0. No type errors.</expect>
      </step>
      <step>
        <run>comp-transform schema-check FeeSummaryPanel</run>
        <expect>window_revenue in rendered set. window_fee_share_usd in rendered set.
        No new MISSING fields.</expect>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev Skill with fee_summary_window constitution</run>
        <expect>PASS — window toggle changes revenue values, fallback to annualized works,
        no undefined/NaN rendered.</expect>
        <if_mismatch>Iterate up to 5 times per Skill protocol, escalate to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.B3b.ds-fee-window-revenue-d02"
      status="pending" description="window_revenue and window_fee_share_usd fields in client_detail.json.
      Types are optional — FE ships with fallback to annualized. Full test requires DS artifact on DEV."/>
  </dependencies>
</task_order>
