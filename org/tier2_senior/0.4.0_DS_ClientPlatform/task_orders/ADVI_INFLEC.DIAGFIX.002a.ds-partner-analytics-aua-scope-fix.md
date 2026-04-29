<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.002a</id>
    <project>ADVI_INFLEC</project>
    <title>AUA scope fix — partner_analytics + leaderboard switch to aum_snapshot (Option 1 immediate)</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>critical</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="gates">DIAGFIX.001 RAVC COMPLETE (AE 0.6.1 20260429T204910Z) — root cause confirmed</ref>
    <ref type="root_cause">INF_B_00 "last seen wins" nav_price=0 bug; 40.2% of holdings rows market_value=$0; 666/782 accounts affected</ref>
    <ref type="ae_recommendation">Option 1 — use aum_snapshot.managed_value per advisor as AUA denominator; same pattern as D_04 (validated $182,552,380.96)</ref>
    <ref type="symptom">partner_analytics_quarterly total AUA = $89.6M (should be $182.6M); distribution percentiles zero</ref>
    <ref type="coordinate_with">DIAGFIX.004 FIX C — same script INF_09, different fix (AUA distribution percentile VALUE COLUMN). Co-develop or sequence: fix AUA source first (this TO), then verify percentile column fix.</ref>
    <ref type="diagfix_002b">DIAGFIX.002b routes INF_B_00 nav_price root cause fix separately (parallel)</ref>
  </references>

  <context>
    DIAGFIX.001 COMPLETE (AE 0.6.1). Root cause confirmed: Option D — "last seen wins" nav_price
    logic in INF_B_00. Non-trade TRN events (fee payments, journals, income distributions) carry
    nav_price=0. When the LAST transaction for (account, ticker) is a non-trade event, the
    holding's market_value = units * 0.0 = $0. Result: holdings.sum() = $89.6M vs. correct
    $182.6M from aum_snapshot.managed_value.

    AE 0.6.1 recommends Option 1 (immediate) for DIAGFIX.002a: switch AUA denominator in
    partner_analytics and leaderboard gold scripts from holdings.market_value.sum() to
    aum_snapshot.managed_value per advisor. Same pattern as D_04 (already validated at $182.6M).

    DIAGFIX.002b (parallel) handles the INF_B_00 nav_price root cause.
    This TO (002a) = Option 1 — immediate, low-risk, unblocks portal display.

    COORDINATION NOTE: INF_09.generate_partner_analytics.py is ALSO targeted by DIAGFIX.004
    FIX C (AUA distribution percentile VALUE COLUMN = None/zero). The two fixes address
    different bugs in the same script. Preferred sequence: fix AUA source column in this TO,
    then apply DIAGFIX.004 FIX C percentile column fix. If DS is already mid-edit on INF_09
    for DIAGFIX.004, bundle both fixes in one pass.

    AUM snapshot by advisor (for reference):
      peter_lee: 198 HH, $161,925,085
      patrick_scanlan: 73 HH, $20,372,728
      inflection_wealth_management: 3 HH, $254,567
      TOTAL: $182,552,380.96
  </context>

  <scope>
    STEP 1 — Audit scripts using holdings-derived AUA:
    comp-pipescript io INF_09 — confirm READS silver/holdings or gold/canonical/holdings.
    Also check any leaderboard script (INF_D_05 or equivalent) and book.json generator.
    List all scripts where holdings.market_value.sum() or equivalent is used for AUA denominator.

    STEP 2 — Fix INF_09.generate_partner_analytics.py:
    Load aum_snapshot managed_value:
      aum = pd.read_parquet(S3_SILVER_AUM_SNAPSHOT)  # silver/aum_snapshot/latest or dated
      advisor_aua = aum.groupby('advisor_id')['managed_value'].sum()
      total_aua = aum['managed_value'].sum()  # = $182,552,380.96
    Replace holdings-derived AUA sums with aum_snapshot values in:
      views.aua.total (the scalar firm-level AUA)
      views.aua.by_advisor (per-advisor AUA)
    For views.aua.distribution (per-account AUA percentiles):
      Use aum_snapshot.groupby('account_id')['managed_value'].sum() for per-account values.
      This is the input to p25/p50/p75 — the VALUE COLUMN that was None/zero in DIAGFIX.004 FIX C.
      Fixing the source here may resolve DIAGFIX.004 FIX C simultaneously — verify after re-run.
    Leave views.geo, views.nna, views.client_acquisition unchanged.

    STEP 3 — Fix leaderboard script (if holdings-derived AUA found):
    Same aum_snapshot swap for any AUA column in leaderboard output.
    Use advisor_aua[advisor_id] per advisor row.

    STEP 4 — Pre-commit gate + S3 upload:
    .tools/ds-commit-gate.sh on all modified scripts.
    aws s3 cp each to s3://opal-data-inf/code/gold/
    comp-pipescript deployed MATCH for each.

    STEP 5 — Re-run + verify:
    Dispatch INF_09 (+ leaderboard if modified) via SSM on EC2.
    Verify partner_analytics_quarterly.json:
      views.aua.total = ~$182,552,380.96
      views.aua.by_advisor.peter_lee = ~$161,925,085
      views.aua.distribution.total.p50 != 0 (expected $100K-$500K range)
      — if p50 is now non-zero, DIAGFIX.004 FIX C is resolved simultaneously; note in RAVC.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_09</run>
        <expect>READS includes silver/holdings or gold/canonical/holdings. If aum_snapshot is NOT
        listed as a READ, the import must be added. Any COLUMN GAP for managed_value documented.</expect>
        <if_mismatch>If aum_snapshot path unknown, check INF_D_04 (already uses it — confirmed $182.6M)
        for the exact S3 key pattern and reuse.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_09.generate_partner_analytics.py</run>
        <expect>Exit 0. py_compile + AST + ruff all pass.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>comp-pipescript deployed INF_09</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload. Do not dispatch re-run until MATCH confirmed.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      After re-run: partner_analytics_quarterly.json views.aua.total = $182,552,380.96 (+/- 0.1%).
      Per-advisor: peter_lee ~$161.9M, patrick_scanlan ~$20.4M.
      Evidence: python parse of artifact in session log.
    </criterion>
    <criterion id="2">
      views.aua.distribution.total.p50 != 0 (bonus: if fixing AUA source also resolves DIAGFIX.004 FIX C,
      note it explicitly in RAVC so COO can mark FIX C as resolved).
    </criterion>
    <criterion id="3">
      Leaderboard AUA column updated (if applicable). Evidence: artifact snippet.
    </criterion>
    <criterion id="4">
      ds-commit-gate.sh exit 0. comp-pipescript deployed MATCH for all modified scripts.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO: commit hash, before/after artifact snippets, S3 deploy MATCH,
      and explicit note on whether DIAGFIX.004 FIX C p50/p75 is also resolved.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL" status="complete">DIAGFIX.001 RAVC — root cause confirmed</dependency>
    COORDINATE with DIAGFIX.004 FIX C (INF_09 percentile VALUE COLUMN — same file, different bug).
    Does NOT block on DIAGFIX.002b (INF_B_00 fix — parallel, lower urgency).
    Does NOT block on DIAGFIX.003, .004, .006.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    Option 2 (INF_B_00 nav_price root cause) routed separately as DIAGFIX.002b.
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "fix(ADVI_INFLEC.DIAGFIX.002a): partner_analytics + leaderboard AUA scope fix — aum_snapshot Option 1" \
      -- data/orion/scripts/gold/INF_09.generate_partner_analytics.py [+ leaderboard script if modified]
  </commit_identity>
</task_order>
