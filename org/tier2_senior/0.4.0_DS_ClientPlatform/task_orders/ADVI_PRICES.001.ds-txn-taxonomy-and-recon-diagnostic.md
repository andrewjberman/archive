<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-prices-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
    <thread_serial>ADVI_PRICES-001</thread_serial>
    <thread_ref>org/threads/ADVI_PRICES-001-lot-valuation-reconciliation-investigati/</thread_ref>
  </metadata>

  <objective>
    Two deliverables to close the ADVI_PRICES investigation:

    WS1: Enumerate all distinct transaction_type and transaction_sub_type values in
    silver/transactions/ and identify any exit-like types NOT in the SELL_TYPES or
    CA_SELL_SUBTYPES allowlists in 03_build_holdings_lots.py. Then expand those
    allowlists and retest.

    WS2: Build a same-date reconciliation diagnostic script that joins
    silver/allocations/D.parquet with gold/holdings_lots/D.parquet at account level,
    classifies each divergence into RC1 (phantom lots), RC2 (allocation-only), or
    RC3 (pricing/unit mismatch), and produces a summary waterfall.

    CRITICAL CONTEXT UPDATE (same-date recon, 2026-03-19):
    - Same-date net gap is only +$25.6M (+1.6%), down from $68M with 1-day mismatch
    - 269 phantom accounts (+$91M excess), 156 missing-lots accounts (-$28M)
    - ZERO accounts are account_is_open==False with open lots, so the allocation
      liveness hard stop (Fix Track B from thread) will NOT help. The phantoms are
      in accounts BD still reports as OPEN.
    - The phantom problem is therefore purely about unrecognized exit transaction
      types — accounts are open but specific positions should be closed.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
      <file action="create">data/black_diamond/scripts/diagnostics/recon_lots_vs_allocations.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS1 — Transaction taxonomy enumeration.

      Read all silver/transactions/ parquets (or a representative recent window,
      e.g. last 30 days) and produce a frequency table of:
        (transaction_type, transaction_sub_type) -> count, net_units_impact

      Compare against SELL_TYPES and CA_SELL_SUBTYPES in 03_build_holdings_lots.py.
      Flag any types that appear to reduce positions but are NOT in the allowlists.

      Special attention to: 'Journal', 'Transfer', 'Withdrawal', 'Fee',
      'Return of Capital', 'Spin-Off', 'Reorganization', or any type with
      negative units that isn't classified as a sell.

      Deliver: a markdown table of findings + the proposed allowlist expansion.
    </requirement>

    <requirement id="2">
      WS1 — Expand SELL_TYPES and/or CA_SELL_SUBTYPES in 03_build_holdings_lots.py
      based on the findings from requirement 1.

      Do NOT blindly add all negative-unit types. Some (e.g., short sells being
      covered, returns of capital) may have different semantics. Use judgment and
      document each addition with a rationale comment.
    </requirement>

    <requirement id="3">
      WS2 — Build recon_lots_vs_allocations.py diagnostic script.

      Inputs: --date YYYY-MM-DD (required)
      Reads:
        - s3://opal-data-bd/silver/allocations/{date}.parquet
        - s3://opal-data-bd/gold/holdings_lots/{date}.parquet

      Outputs (to stdout + optional --output-dir for parquet):
        1. Summary: BD AUA total, lot MV total, net gap, % gap
        2. Per-account join: account_id, bd_aua, lot_mv, diff, pct_diff, account_type
        3. Classification of each account into:
           - RC1_PHANTOM: lot_mv > 2x bd_aua
           - RC2_ALLOC_ONLY: bd_aua > $1K and lot_mv == 0
           - RC3_INSURANCE: account_type == 'Insurance' and diff < -$100
           - RC4_NON_INVESTMENT: account_type in Bank/Savings/CreditCard/Loans/Mortgage/TermLife
           - RC5_NORMAL: everything else
        4. Waterfall: $ impact per RC category

      This replaces the ad-hoc Python I ran in this session. It should be
      reusable for ongoing monitoring.
    </requirement>

    <requirement id="4">
      WS2 — For the 269 phantom accounts, drill into the top 20 by excess and
      identify the specific securities driving the overshoot. For each, check
      whether the security has any transactions in the last 90 days. If a
      security has zero transactions in 90 days but the lot is still open,
      that's strong evidence of a missing exit event.

      Account ID list: s3://opal-data-bd/diagnostics/prices_recon_accounts_2026-03-19.json
      (field: phantom_accounts.ids)
    </requirement>

    <requirement id="5">
      Commit WS1 (taxonomy expansion) and WS2 (diagnostic script) separately.
      WS1 commit: feat(gold): expand SELL_TYPES/CA_SELL_SUBTYPES for lot closure
      WS2 commit: feat(diagnostics): recon_lots_vs_allocations.py
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Transaction type frequency table delivered with clear flag on unrecognized exit types</criterion>
    <criterion id="2">SELL_TYPES or CA_SELL_SUBTYPES expanded with rationale per addition</criterion>
    <criterion id="3">recon_lots_vs_allocations.py runs locally with --date 2026-03-19 and produces the waterfall</criterion>
    <criterion id="4">Top 20 phantom accounts drilled with security-level detail and 90-day transaction check</criterion>
    <criterion id="5">Both commits on CLOUD branch</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify 02_build_positions_cube.py — only 03_build_holdings_lots.py for WS1</constraint>
    <constraint>Do NOT run gold layer rerun — that is AE's responsibility after these changes are committed</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      Account ID lists uploaded to s3://opal-data-bd/diagnostics/prices_recon_accounts_2026-03-19.json.
      Same-date holdings_lots/2026-03-19.parquet confirmed to exist.
      No blockers.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">WS1: SELL_TYPES/CA_SELL_SUBTYPES taxonomy expansion in 03_build_holdings_lots.py</deliverable>
    <deliverable type="commit">WS2: recon_lots_vs_allocations.py diagnostic script</deliverable>
    <deliverable type="document">Transaction type frequency table + phantom account drill-down in session log</deliverable>
  </deliverables>
</task_order>
