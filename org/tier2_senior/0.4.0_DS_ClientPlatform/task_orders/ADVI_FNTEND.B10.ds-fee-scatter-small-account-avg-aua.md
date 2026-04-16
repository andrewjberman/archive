<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-16-advi-fntend-b10-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>complete</status><!-- 0.4.0_DS_ClientPlatform~B 2026-04-16. Commit bb426933. C_08 small_account_avg_aua at (advisor, role) grain + advisor grain. Edge: count==0 -> avg==0.0. py_compile EXIT 0. comp-pipescript deployed C_08 MATCH. Spot-check deferred to post-PROD-nightly. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>B10</wave>
  </metadata>

  <context>
    A new "Consolidation Opportunity" scatter mode is being added to FeeEfficiencyPanel
    (ADVI_FNTEND.RD3). The scatter plots small_account_count (x) vs
    small_account_avg_aua (y) per advisor. small_account_count already emits via B9
    (C_08, commit f2ec98d1). small_account_avg_aua is not yet emitted.

    C_08 already computes the small-account subset at the advisor grain (lines 849-865).
    The mask, per_acct DataFrame, and _by_adv count are all in scope. Adding the average
    requires one additional groupby agg on the same mask — no new data loads or joins.
  </context>

  <objective>
    In C_08.advisor_fee_efficiency.py, in the B9 small_account block (after line 857),
    add the per-advisor mean AUA of small accounts:

      _small_sum_by_adv = per_acct[_small_mask].groupby('advisor')['aua_current'].sum()
      _small_avg_by_adv = (_small_sum_by_adv / _by_adv).fillna(0.0).round(2)
      small_account_avg_aua_by_advisor = {str(k): float(v) for k, v in _small_avg_by_adv.items()}

    Pass small_account_avg_aua_by_advisor into build_scorecard (add as new kwarg,
    defaulting to None).

    In build_scorecard / _build_detail_rows (wherever small_account_count is written
    to the per-advisor emit, around line 440):
      'small_account_avg_aua': float(small_account_avg_aua_by_advisor.get(advisor_key, 0.0)),

    Edge cases:
    - Advisor with small_account_count == 0: emit small_account_avg_aua = 0.0
    - Advisor not in small_account_avg_aua_by_advisor: emit 0.0 (default)
    - NULL aua_current already excluded by _small_mask — no further null handling needed.

    THRESHOLD: use the existing SMALL_ACCOUNT_AUA_THRESHOLD_USD = 40_000 constant.
  </objective>

  <wire_contract>
    Per-advisor emit in advisor_fee_efficiency.json (alongside existing small_account_count):
      small_account_avg_aua: float  -- mean aua_current of below-threshold accounts; 0.0 if none
    Required (non-null) for every advisor entry after this TO ships.
  </wire_contract>

  <acceptance_criteria>
    1. advisor_fee_efficiency.json carries small_account_avg_aua on every advisor entry.
    2. For an advisor with small_account_count > 0: small_account_avg_aua is between
       0 and SMALL_ACCOUNT_AUA_THRESHOLD_USD (exclusive). Values at or above 40_000
       indicate a logic error (threshold filter not applied correctly).
    3. For an advisor with small_account_count == 0: small_account_avg_aua == 0.0.
    4. Spot-check: pick one advisor with known small accounts. Verify
       small_account_avg_aua == sum(aua_current for small accounts) / small_account_count
       to within $1.00 rounding tolerance.
    5. py_compile C_08 exit 0.
    6. comp-pipescript deployed C_08: MATCH before upload.
    7. MCP COMPLETE to COO with commit hash + one advisor spot-check
       (name, small_account_count, small_account_avg_aua).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io C_08</run>
        <expect>No new READs required. aua_current is already in per_acct from existing
        B9 block. Confirm no new S3 reads or joins needed.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile C_08.advisor_fee_efficiency.py</run>
        <expect>Exit 0.</expect>
      </step>
      <step>
        <run>comp-pipescript deployed C_08</run>
        <expect>MATCH.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>
</task_order>
