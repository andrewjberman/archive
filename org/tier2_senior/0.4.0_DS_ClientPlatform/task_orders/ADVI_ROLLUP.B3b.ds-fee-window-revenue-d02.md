<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-16-advi-rollup-b3b-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>complete</status><!-- 0.4.0_DS_ClientPlatform~B 2026-04-16. Commit 1f91954c. D_02 fee_summary.window_revenue.{qtd/ytd/max}.{firm_revenue_usd, advisor_revenue_usd} + team_attribution[].window_fee_share_usd.{qtd/ytd/max}. annual_implied_revenue preserved. py_compile EXIT 0. comp-pipescript deployed D_02 MATCH. Spot-check deferred to post-PROD-nightly. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3-addendum-B3b</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FEE_WINDOW_REVENUE.md</ref>
    <ref type="design_response">DS design response 20260416T200524Z — Option B confirmed, 5-7 hr estimate</ref>
    <ref type="precedent">ADVI_FNTEND.B3 (team_attribution emit, code-complete 544877cc) — this TO extends B3 with window-scoped fields</ref>
  </references>

  <context>
    L3 Fee Summary panel (portal DEV 3f558c0) has a QTD/YTD/Max window toggle.
    NNA already window-scoped. Revenue is hardcoded to annualized figures.
    Andrew directive: Total Firm Revenue and Advisor Revenue must respond to the window toggle.

    D_02 already has all required data:
    - acct DataFrame (account_performance + fee_bps from fee_rate_history join) — for firm revenue
    - fee_rate_history split columns (architect_split, implementor_split, etc.) — for advisor revenue
    No new gold reads or artifact dependencies.
  </context>

  <objective>
    Extend D_02.advisor_client_detail.py (build_client_details / client_detail.json emit) with
    two new data shapes:

    1. fee_summary.window_revenue — per-window firm + advisor revenue for the relationship:

       For each window (qtd, ytd, max):
         window_start = cutoff date for that window (QTD = start of current quarter,
                        YTD = Jan 1 of current year, Max = earliest account date)
         firm_revenue_usd = sum over accounts in relationship of:
           (account_aua * fee_bps / 10_000 / TRADING_DAYS_PER_YEAR) * days_in_window
           where days_in_window = (latest_date - window_start).days + 1
           and account_aua/fee_bps read from the PIT snapshot at latest_date
           (same snap_latest used for existing annualized compute)
         advisor_revenue_usd = sum across all team members of their prorated share
           = firm_revenue_usd * sum(split_pct for advisor's roles on accounts in relationship)

    2. team_attribution[].window_fee_share_usd — per-advisor per-window fee share:

       For each team member already in team_attribution[], add:
         window_fee_share_usd: {
           qtd: float,
           ytd: float,
           max: float
         }
       Computed as: (account_aua * fee_bps / 10_000 / TRADING_DAYS) * days_in_window * split_pct
       summed over all accounts in the relationship where this advisor has a role.

    CONSTANTS:
    - TRADING_DAYS_PER_YEAR = 252 (or match existing constant in D_02 if present)
    - Window cutoffs: use same logic as existing nna_qtd/nna_ytd/nna_max window definitions in D_02

    BACKWARD COMPAT:
    - annual_implied_revenue stays in fee_summary (other consumers may read it)
    - fee_share_usd stays in team_attribution (annualized, unchanged)
    - window_revenue and window_fee_share_usd are additive new fields
  </objective>

  <wire_contract>
    client_detail.json fee_summary additions:
      window_revenue: {
        qtd: { firm_revenue_usd: float, advisor_revenue_usd: float },
        ytd: { firm_revenue_usd: float, advisor_revenue_usd: float },
        max: { firm_revenue_usd: float, advisor_revenue_usd: float }
      }

    team_attribution[] entry additions:
      window_fee_share_usd: { qtd: float, ytd: float, max: float }

    Both required (not optional) in every emit after this TO ships.
    Round all revenue figures to 2 decimal places.
    advisor_revenue_usd in window_revenue = aggregate across ALL team members
    (not scoped to the profile advisor — per-advisor breakdown is in team_attribution).
  </wire_contract>

  <acceptance_criteria>
    1. client_detail.json for at least one relationship carries window_revenue with all three windows.
    2. Travis Penfield QTD firm_revenue_usd is a plausible fraction of Max firm_revenue_usd
       (sanity: QTD should be roughly 1/4 of Max for a stable book).
    3. sum(team_attribution[i].window_fee_share_usd.qtd) ~= window_revenue.qtd.advisor_revenue_usd
       (within float rounding — if split_pcts sum to 1.0 for all accounts).
    4. annual_implied_revenue unchanged from pre-TO value for the same relationship.
    5. team_attribution[] entries all carry window_fee_share_usd.
    6. py_compile D_02 exit 0.
    7. comp-pipescript deployed D_02: MATCH before upload.
    8. comp-validate D_02 exit 0 after QA rerun.
    9. MCP COMPLETE to COO with commit hash + Travis QTD/YTD/Max firm revenue sample
       + one team_attribution window_fee_share_usd sample.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>READS includes acct (account_performance) and fee_rate_history. No new READs
        required for this change. No COLUMN GAPS for fee_bps or split_pct columns.</expect>
        <if_mismatch>STOP. If fee_bps or split_pct columns are missing from the load list,
        add them first and flag to COO before writing revenue logic.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_02</run>
        <expect>Downstream: client_detail.json -> D_04 -> portal platinum/clients/*. No other
        consumers of client_detail. Additive fields do not break existing consumers.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-pipescript deployed D_02</run>
        <expect>MATCH.</expect>
        <if_mismatch>Coordinate with AE before upload.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile D_02.advisor_client_detail.py</run>
        <expect>Exit 0.</expect>
      </step>
    </phase>
    <phase id="3" when="after QA rerun">
      <step>
        <run>comp-validate D_02 --artifact /tmp/client_detail_sample.json</run>
        <expect>Exit 0. window_revenue and window_fee_share_usd fields present,
        non-null, reasonable values.</expect>
        <if_mismatch>STOP. Do not signal COO until clean.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. All inputs already in D_02.
  </dependencies>

  <next>
    On MCP COMPLETE: DE B3b binding TO fires.
  </next>
</task_order>
