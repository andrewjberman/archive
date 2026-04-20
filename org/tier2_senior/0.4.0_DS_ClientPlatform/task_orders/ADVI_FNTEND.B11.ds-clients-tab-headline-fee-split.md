<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-16-advi-fntend-b11-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>active</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>B11</wave>
  </metadata>

  <context>
    The N1 Firm Overview (Books-tab landing, ClientsTab) got a card layout aligned with
    the L2 Book Overview pattern (portal DEV 19b8987). Four cards now render:
      - Total AUA (indigo)
      - Fee-Paying Clients (emerald) + "{aua} AUA" sub
      - Non-Fee-Paying Clients (pink) + "{aua} AUA" sub
      - Accounts (slate) + red "{N} small (&lt;$40k)" sub

    ClientsTabHeadline currently emits: total_aua, account_count, client_count,
    fee_rate_pct (hardcoded 0.0 in D_00), income_yield_pct.

    The five new fields are optional on the FE type — cards render em-dash until
    DS emits. No FE change needed on emit; the cards activate automatically.

    D_00.portal_aggregates.py produces clients_tab.json. The headline block is built
    around line 545 from perf_latest (canonical_performance at relationship grain).
    D_00 does not currently load fee_rate_history or account-level AUA data.
  </context>

  <objective>
    In D_00.portal_aggregates.py, extend the headline block (around line 545-578)
    with five new fields:

      fee_earning_client_count     int  -- clients with >= 1 fee-paying account firm-wide
      non_fee_earning_client_count int  -- client_count - fee_earning_client_count
      fee_earning_aua              float -- firm-wide AUA on fee-paying accounts
      non_fee_earning_aua          float -- firm-wide AUA on non-fee-paying accounts
      small_account_count          int   -- unique accounts with AUA &lt; 40_000

    DEFINITIONS (match advisor-level analogs already in D_02/C_08):
      fee-paying account = is_billable == True AND split_pct > 0 (from fee_rate_history,
        same logic as build_fee_summary_by_account in D_02)
      small account = account with total_aua &lt; SMALL_ACCOUNT_AUA_THRESHOLD_USD (40_000),
        same constant and logic as C_08 B9

    DATA SOURCES TO LOAD (new reads for D_00):
      1. fee_rate_history (A_02 output, same S3 key used by D_02):
         Used to classify accounts as fee-paying or non-fee-paying.
         Join on account_id to get is_billable, split columns.
         Use latest date snapshot (snap_latest equivalent).

      2. account-level AUA snapshot (C_03 canonical_performance at account grain,
         or C_00 canonical_performance — whichever D_00 can most cleanly load):
         Used to get total_aua per account for fee_earning_aua, non_fee_earning_aua,
         and small_account_count. The perf_latest in D_00 is at relationship grain
         (num_accounts, not account_id) — cannot be used directly.

    comp-pipescript io D_00 first to confirm correct S3 keys before writing.

    EMIT in the headline dict:
      'fee_earning_client_count':     int(fee_earning_clients),
      'non_fee_earning_client_count': int(non_fee_earning_clients),
      'fee_earning_aua':              round(float(fee_earning_aua), 2),
      'non_fee_earning_aua':          round(float(non_fee_earning_aua), 2),
      'small_account_count':          int(small_account_count),

    Sanity checks to log in run summary:
      fee_earning_aua + non_fee_earning_aua ~= headline.total_aua (within rounding)
      fee_earning_client_count + non_fee_earning_client_count == client_count
  </objective>

  <wire_contract>
    clients_tab.json headline additions:
      fee_earning_client_count:     int
      non_fee_earning_client_count: int
      fee_earning_aua:              float
      non_fee_earning_aua:          float
      small_account_count:          int
    All required (non-null) after this TO ships. FE type already has them as optional.
  </wire_contract>

  <acceptance_criteria>
    1. clients_tab.json headline carries all five fields.
    2. fee_earning_client_count + non_fee_earning_client_count == client_count.
    3. fee_earning_aua + non_fee_earning_aua within 1% of total_aua
       (minor delta expected from accounts with null fee data).
    4. small_account_count consistent with C_08 B9 firm-wide total
       (same threshold, same account universe — values should be equal or within
        a small epsilon from snapshot-date differences).
    5. py_compile D_00 exit 0.
    6. comp-pipescript deployed D_00: MATCH before upload.
    7. MCP COMPLETE to COO with commit hash + spot-check values
       (fee_earning_client_count, fee_earning_aua, small_account_count).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_00</run>
        <expect>Identify current S3 READs. Confirm fee_rate_history and account-level
        AUA S3 keys before adding new loads. Flag any COLUMN GAPS.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile D_00.portal_aggregates.py</run>
        <expect>Exit 0.</expect>
      </step>
      <step>
        <run>comp-pipescript deployed D_00</run>
        <expect>MATCH.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <notes>
    - This TO is NOT pre-run critical. FE renders em-dash until fields land.
      Execute after tonight's gold run completes (don't interrupt the run sequence).
    - SMALL_ACCOUNT_AUA_THRESHOLD_USD = 40_000 — use module-level constant, same as C_08.
    - If loading account-level AUA requires a new S3 artifact that significantly increases
      D_00 runtime, flag to CTO before writing — there may be a lighter path via D_04
      aggregation after D_02 completes.
  </notes>
</task_order>
