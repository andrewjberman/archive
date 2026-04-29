<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.004</id>
    <project>ADVI_INFLEC</project>
    <title>Fix timeseries end_date/$106B spike + concentration_risk empty + AUA dist percentiles zero</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>2-3h</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnostic_brief">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ADVI_INFLEC_DIAGNOSTIC_BRIEF_20260429.md §C2 §C3 §C6 §C7</ref>
    <ref type="script_timeseries">data/orion/scripts/gold/INF_I_D00b.portal_timeseries.py</ref>
    <ref type="script_concentration">data/orion/scripts/gold/INF_D_07.concentration_risk.py</ref>
    <ref type="script_partner_analytics">data/orion/scripts/gold/INF_09.generate_partner_analytics.py</ref>
    <ref type="symptom_c2">timeseries_overview latest 2026Q2 end_date='2026-06-30' displayed as 'Jun 30' — should be data_as_of = 2026-04-28</ref>
    <ref type="symptom_c3">timeseries_overview monthly 2024-02 Total AUA = $106,915,047,884 — $106B spike artifact, will render as chart spike</ref>
    <ref type="symptom_c7">platinum/firm/concentration_risk.json = '[]' (2 bytes). INFGRD.003 generated empty output.</ref>
    <ref type="symptom_c6">partner_analytics_quarterly.views.aua.distribution.total: mean=0.0, p25=0.0, p50=0.0, p75=0.0, min=0.0, max=0.0 — while views.geo.distribution.total has real percentiles</ref>
  </references>

  <context>
    Three independent DS gold script bugs bundled in this TO. All are self-contained fixes
    not gated on the AUA scope investigation (DIAGFIX.001). Execute in parallel with DIAGFIX.002+003.

    FIX A — INF_I_D00b timeseries: Two bugs in the same script.
    Bug A1: In-progress quarter (2026Q2) is emitted with end_date='2026-06-30' (projected quarter
    end) instead of data_as_of='2026-04-28' (actual snapshot date). PartnerAnalytics.tsx line 1844
    reads end_date for the "as of" sub-caption, causing "Jun 30, 2026" to display.
    Fix: For any period where end_date > data_as_of, set end_date = data_as_of in the output.
    Bug A2: 2024-02 entry has Total AUA = $106,915,047,884 (~$106B). Bad input row, renders as
    a vertical spike in the AUA bar chart.
    Fix: Add outlier detection — any period where AUA > PREV_PERIOD * 10 (or > $10B absolute
    threshold) should be suppressed or flagged. Suppress the row, emit a warning to log.

    FIX B — INF_D_07 concentration_risk: Output is '[]' (empty list). The script either
    has no Inflection data passing its filters, or the firm_id/rep_id filter excludes all
    accounts. Check: does INF_D_07 use a holdings-derived source (which has the $89.6M
    scope bug)? If so, there may still be SOME holdings data — check why even the $89.6M
    accounts aren't producing concentration output. Most likely a threshold filter that
    requires N accounts or $X AUA to emit, and the holdings data isn't passing the threshold.
    Fix: Relax the threshold or fix the filter. Even with $89.6M scope, there should be
    concentration entries for ~307 accounts.

    FIX C — INF_09 partner_analytics AUA distribution percentiles:
    views.aua.distribution.total has count=307 and sum=$89.6M but mean=0, p25=0, p50=0.
    views.geo.distribution.total has REAL percentiles (p25=$20K, p50=$49K, p75=$131K).
    This means the percentile computation logic works — but the VALUE COLUMN being passed
    to the AUA distribution percentile computation is wrong (likely None, zeros, or the
    wrong field name). Fix the column reference for the AUA distribution computation to
    use the correct market_value / AUA field.
  </context>

  <scope>
    FIX A — INF_I_D00b.portal_timeseries.py (timeseries end_date + spike):

    STEP A1 — Read INF_I_D00b in full. Find where quarterly/monthly periods are constructed.
    Locate the line that sets end_date for the current in-progress period.

    STEP A2 — Fix in-progress end_date: where end_date is computed from quarter end
    (e.g., 'YYYY-06-30' for Q2), add a cap:
      end_date = min(computed_end_date, data_as_of)
    where data_as_of is the watermark date. Apply to both monthly and quarterly outputs.

    STEP A3 — Fix $106B spike: after computing period AUAs, add outlier suppression:
      OUTLIER_THRESHOLD = 10_000_000_000  # $10B hard cap per period
      for any row where total_aua > OUTLIER_THRESHOLD: skip row, log
        print(f"WARN: timeseries outlier suppressed period={period} aua={total_aua:.0f}")
    This is belt-and-suspenders; root cause investigation of the bad input row is lower
    priority and can be a follow-on.

    FIX B — INF_D_07.concentration_risk.py (empty output):

    STEP B1 — Read INF_D_07 in full. Identify:
    - What is the input data source (silver/holdings or silver/aum_snapshot)?
    - What filters are applied (rep_id, firm_id, account_status, AUA threshold)?
    - What is the minimum threshold for emitting a concentration entry?

    STEP B2 — Run a diagnostic: how many rows survive each filter? Print row counts
    after each filter step. The empty [] means 0 rows survive somewhere.

    STEP B3 — Fix the filter or threshold that's zeroing out all Inflection accounts.
    Most likely causes:
    a. rep_id filter doesn't include {3, 11, 12}
    b. AUA threshold (e.g., "only accounts > $500K AUA") excludes all accounts
    c. Data column name mismatch (e.g., looking for 'managed_value' when column is
       'market_value')
    Fix whichever applies. Output should include concentration entries for Inflection
    accounts (even with the $89.6M scope limitation — that's still 307 accounts).

    FIX C — INF_09.generate_partner_analytics.py (AUA distribution percentiles):

    STEP C1 — Read INF_09 in full. Find the views.aua.distribution computation.
    Compare it to the views.geo.distribution computation (which works correctly).

    STEP C2 — Identify the value column. The AUA distribution should aggregate over
    account-level AUA values (market_value or equivalent). If the column is None or
    the wrong name, percentiles will be computed over zeros.
    Fix: use the same AUA value column that drives the sum ($89.6M total — check what
    column that sum is computed from).

    STEP C3 — Verify the fix locally:
    python3 -c "import json; d=json.load(open('/tmp/test_pa.json'));
    dist=d['views']['aua']['distribution']['total'];
    print('p50=', dist.get('p50'), 'p75=', dist.get('p75'))"
    p50 and p75 should be non-zero (expected range: $100K-$500K for a 307-account firm).

    All three fixes — pre-commit gate + S3 upload:
    .tools/ds-commit-gate.sh INF_I_D00b.portal_timeseries.py INF_D_07.concentration_risk.py \
      INF_09.generate_partner_analytics.py
    aws s3 cp each fixed script to s3://opal-data-inf/code/gold/
    comp-pipescript deployed on each — MATCH required before re-run dispatch.

    Re-run on EC2:
    Dispatch INF_I_D00b, INF_D_07, INF_09 via orion-gold-dispatch.sh (or SSM).
    Each can run standalone — no full chain needed.

    Verify outputs:
    - timeseries_overview.json: latest quarterly end_date = '2026-04-28', no $106B row
    - concentration_risk.json: non-empty list (at least 1 entry)
    - partner_analytics_quarterly.json views.aua.distribution.total p50 != 0
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_I_D00b</run>
        <expect>WRITES includes platinum/firm/timeseries_overview.json. READS includes silver/aum_snapshot
        or equivalent. Document any COLUMN GAPS.</expect>
      </step>
      <step>
        <run>comp-pipescript io INF_D_07</run>
        <expect>READS includes silver/holdings or equivalent. WRITES includes platinum/firm/concentration_risk.json.</expect>
        <if_mismatch>If READS don't include holdings, identify the actual input source and document in RAVC.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io INF_09</run>
        <expect>WRITES includes partner_analytics_quarterly.json. READS includes silver holdings or accounts.
        Confirm no new COLUMN GAPS introduced.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_I_D00b.portal_timeseries.py data/orion/scripts/gold/INF_D_07.concentration_risk.py data/orion/scripts/gold/INF_09.generate_partner_analytics.py</run>
        <expect>Exit 0. py_compile + AST + ruff all pass for all three files.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>comp-pipescript deployed INF_I_D00b INF_D_07 INF_09</run>
        <expect>MATCH for all three.</expect>
        <if_mismatch>Re-upload. Do not dispatch re-run until all three MATCH.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      INF_I_D00b fix: after re-run, timeseries_overview.json quarterly latest entry
      has end_date = '2026-04-28' (not '2026-06-30'). No row with AUA > $10B.
      Evidence: python parse of S3 artifact in session log.
    </criterion>
    <criterion id="2">
      INF_D_07 fix: after re-run, concentration_risk.json is non-empty (at least 1 entry).
      Evidence: python parse showing len(data) > 0.
    </criterion>
    <criterion id="3">
      INF_09 fix: after re-run, partner_analytics_quarterly views.aua.distribution.total
      has non-zero p50 (expected $100K-$500K range).
      Evidence: python parse of p50/p75 values in session log.
    </criterion>
    <criterion id="4">
      .tools/ds-commit-gate.sh exit 0 on all three modified scripts.
      comp-pipescript deployed MATCH for all three.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO: commit hash, S3 deploy MATCH for all three scripts,
      before/after artifact snippets for each fix.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="independent"/>
    Parallelizable with DIAGFIX.001, .002, .003, .005.
    NOT gated on DIAGFIX.001 (scope investigation) — these are independent computation bugs.
  </dependencies>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "fix(ADVI_INFLEC.DIAGFIX.004): timeseries end_date cap + spike suppression + conc_risk filter + AUA dist percentiles" \
      -- data/orion/scripts/gold/INF_I_D00b.portal_timeseries.py \
         data/orion/scripts/gold/INF_D_07.concentration_risk.py \
         data/orion/scripts/gold/INF_09.generate_partner_analytics.py
  </commit_identity>
</task_order>
