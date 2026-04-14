# ADVI_NNAFEE.007 — Design Note: Interval-Aware Advisor List on Books N1

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-nnafee-007-design</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>RD (Books tab)</issued_to>
    <date>2026-04-07</date>
    <status>complete</status><!-- COO session 28 2026-04-14 sweep: ADVI_NNAFEE absorbed into ADVI_REBORN per REGISTRY; superseded by REBORN .005-.008 + .011-.013 -->
    <project_code>ADVI_NNAFEE</project_code>
    <priority>high</priority>
  </metadata>

  <design_note>
    ## Context

    Andrew confirmed (2026-04-07): The advisor list on the Books N1 (firm dashboard)
    must be interval-aware, driven by the fee efficiency panel's period selector.

    ## Period Selector

    The fee efficiency panel on Books N1 should offer: **QTD / YTD / 1Y / 3Y / Max**

    This selector drives BOTH the fee efficiency scatter AND the advisor list below it.

    ## Metric Behavior by Interval

    | Metric | Interval-sensitive? | Notes |
    |--------|-------------------|-------|
    | AUA | NO | Always latest snapshot, same number regardless of interval |
    | NNA | YES | Sum over selected window |
    | Growth (AUA %) | YES | Relative to window start AUA |
    | New Clients | YES | count of relationships with first_seen_date >= window start |
    | Revenue | YES | Implied revenue over selected window |
    | Fee Yield (bps) | YES | From fee efficiency data (already windowed) |
    | Efficiency Ratio | YES | From fee efficiency data (already windowed) |

    ## Data Sources

    - **Employee leaderboard** (`employee_leaderboard.json`): Already has windows
      (3M/6M/1Y/2Y/3Y/QTD/YTD). Use `windows[selectedWindow].entries[]` for
      NNA, growth, new_clients, AUA.

    - **Fee efficiency scorecard** (`advisor_fee_efficiency.json`): Currently has
      trailing_12m + YTD fields per advisor. If additional windows are needed,
      DS must add them to the gold script (C_08).

    ## Advisors Tab Comparison

    The Advisors tab leaderboard already works this way — the Top Performers toggle
    (QTD/YTD/trailing_12m) drives which window of data is displayed. The Books N1
    advisor list should follow the same pattern but with its own period selector
    on the fee efficiency panel.

    ## Implementation Notes for RD

    1. Fee efficiency panel period selector state should be lifted to the Books N1
       page level (or shared via context) so the advisor list can read it.
    2. When period changes, swap the employee leaderboard window AND re-filter
       fee efficiency data by the matching period.
    3. AUA column always reads from the latest snapshot (not windowed).
    4. The `getEmployeeLeaderboard()` endpoint is already wired (NNAFEE.004).
    5. Map period selector values to leaderboard window keys:
       QTD -> 'qtd', YTD -> 'ytd', 1Y -> '1Y', 3Y -> '3Y', Max -> use largest available window
  </design_note>
</task_order>
