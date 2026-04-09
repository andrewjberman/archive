<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-045-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>11</wave>
    <phase>Books tab fee efficiency correctness</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Full audit and fix of C_08.advisor_fee_efficiency.py. Three confirmed issues:
    1. Commission math doesn't tie to what the portal displays for fee_bps × AUA
    2. Efficiency ratio display appears inverted or mislabeled for Cole Pettis case
    3. Negative NNA advisors hardcoded to 0th percentile -- needs principled handling
    Report findings to CTO before committing any formula changes.
  </objective>

  <context>
    C_08 commission formula (line ~228):
      commission = fee_bps_weighted / 10000 × managed_aua × (calendar_days / 365.25)

    Efficiency percentile (line ~233-241):
      ratio = commission / nna
      lower ratio = more commission per NNA dollar = LESS efficient
      efficiency_pctile = ratio.rank(ascending=True, pct=True) × 100
      i.e. lower ratio → lower percentile rank → less efficient
      advisors with nna <= 0: efficiency_pctile hardcoded to 0

    Observed issues (Andrew, 2026-04-09):

    ISSUE 1 -- Grace McCasland YTD:
      Portal shows: fee_bps = 33.1, commission = $17.9K
      Andrew's check: 0.00331 × displayed_AUA = $21.6K ≠ $17.9K
      Question: is the $17.9K a prorated YTD figure (correct) or wrong?
      The formula multiplies by calendar_days/365.25 so YTD commission IS prorated.
      If AUA used in the formula ≠ AUA shown in the portal, this explains the gap.
      The portal likely shows tagged_aua or managed_aua from the leaderboard, but C_08
      uses its own managed_aua from fee_detail. If these differ, the math won't reconcile.

    ISSUE 2 -- Cole Pettis efficiency ranking:
      Portal shows: efficiency at 10th percentile, ratio = 0.53%
      Andrew: Cole should have very high efficiency -- something is wrong.
      Hypothesis: if ratio = commission/nna and Cole's is 0.53%, that means he generates
      $188 NNA per $1 commission -- highly efficient. With ascending rank, he should be
      near the 100th pctile, not 10th.
      Alternative hypothesis: the DISPLAYED "ratio" is a different field than the
      efficiency_pctile is actually computed from (e.g., displayed = nna/commission,
      computed = commission/nna). A display label inversion would explain both the
      Grace and Cole cases.

    ISSUE 3 -- Negative NNA hardcode:
      Advisors with nna <= 0 all get efficiency_pctile = 0 regardless of their commission.
      An advisor with small negative NNA and tiny commissions is treated identically to
      one with large negative NNA and large commissions. This is crude and misleading.
  </context>

  <investigation_1 label="Commission formula audit">
    <description>
      Step 1: For Grace McCasland YTD window, extract from the C_08 intermediate data:
        - managed_aua used in the commission formula
        - fee_bps_weighted
        - calendar_days for YTD window
        - resulting commission
      Verify: fee_bps_weighted / 10000 × managed_aua × (calendar_days/365.25) = $17.9K

      Step 2: Compare managed_aua (C_08's source) to the AUA figure displayed in the
      portal's fee efficiency table for Grace. If different, identify which source each
      comes from and why they diverge.

      The portal likely displays managed_aua from the leaderboard (D_00/D_02 path) while
      C_08 uses fee_detail (from silver advisor_fee_detail). These may disagree on:
        - Which accounts are fee-earning
        - Split percentages
        - Snapshot date

      Step 3: Document the formula clearly in session log:
        "commission = fee_bps_weighted / 10000 × managed_aua × (days/365.25)"
        "This is a time-prorated estimate, NOT the actual invoiced amount from BD"
        "The displayed bps × displayed AUA ≠ commission because commission uses
         C_08's own managed_aua, not the leaderboard AUA"
        Note whether this methodology is correct or should be changed.

      If the formula is correct but the DISPLAY is misleading (showing a bps × AUA
      multiplication that doesn't reconcile to the commission): flag to DE to add
      a footnote or tooltip explaining the prorated estimate methodology.
    </description>
  </investigation_1>

  <investigation_2 label="Efficiency ratio display vs calculation audit">
    <description>
      Determine exactly what "ratio" is being DISPLAYED in the fee efficiency table
      vs what is used to compute efficiency_pctile.

      C_08 computes: ratio = commission / nna (used for pctile ranking)
      Portal might display: nna / commission (which would appear as a large number or %)
      OR: the portal might display fee_bps_weighted as "ratio" (a completely different field)

      Test: for Cole Pettis, extract from platinum fee_efficiency.json:
        commission, nna, efficiency_pctile, regression_residual_ratio, fee_bps_weighted
      Determine which field = 0.53% as displayed.

      If 0.53% = commission/nna:
        Cole's commission/nna = 0.53% → $188 NNA per $1 commission → very efficient
        efficiency_pctile should be near 100 → if showing 10th, ranking logic is inverted
        Fix: check ascending=True in rank() -- lower commission/nna = MORE efficient = HIGHER pctile
        The current logic (ascending=True → lower ratio → higher pctile) IS correct.
        If Cole shows 10th pctile with 0.53% ratio, either the data is wrong or there
        are many advisors with even lower ratios (even more efficient). Verify.

      If 0.53% = fee_bps_weighted/100 (i.e. bps displayed as %):
        Then "ratio" in the portal is fee bps, not efficiency ratio. Mislabeled column.
        Fix: rename the column in the portal (DE fix) and show the actual commission/nna ratio.

      If 0.53% = regression_residual_ratio:
        The portal is showing the regression residual, not the efficiency percentile.
        Diagnose and correct the field mapping.

      Post confirmed root cause to CTO inbox before fixing.
    </description>
  </investigation_2>

  <fix_negative_nna label="Principled negative NNA handling">
    <description>
      Current: all advisors with nna <= 0 get efficiency_pctile = 0. This is wrong.
      An advisor with nna = -$1K and tiny commissions is very different from one with
      nna = -$5M and large commissions. Both get 0th pctile today.

      Approved approach: maintain a two-tier ranking system.
        TIER 1 (positive NNA): rank by commission/nna ascending (current logic, unchanged)
          efficiency_pctile = percentile within Tier 1 × pct_of_all_advisors_in_tier1
          e.g. if 80% of advisors have positive NNA, Tier 1 pctiles range from 0 to 80

        TIER 2 (zero or negative NNA): rank by MAGNITUDE of NNA descending
          i.e. nna closer to 0 = less bad = ranked higher within Tier 2
          Tier 2 pctiles range from 0 to (100 - pct_tier1)
          e.g. if 20% of advisors have non-positive NNA, Tier 2 pctiles range 0-20

        Final efficiency_pctile:
          Tier 2 advisors: ranked within Tier 2 by |nna| descending
            least-negative NNA → highest Tier 2 pctile (just below the Tier 1 floor)
          Tier 1 advisors: start above where Tier 2 ends

        Example with 10 advisors, 8 positive NNA, 2 negative:
          Negative NNA advisors ranked by |nna| desc within Tier 2:
            nna = -$100K → pctile = 20%  (higher = less bad)
            nna = -$500K → pctile = 10%  (lower = worse)
          Positive NNA advisors ranked by commission/nna asc, mapped to 20-100:
            best ratio → pctile = 100%
            worst ratio → pctile = 30% (just above the Tier 2 ceiling of 20)

      This gives ALL advisors a meaningful, comparable percentile within a coherent scale.
      Advisors with negative NNA always rank below those with positive NNA, but are still
      differentiated from each other.

      Implement in C_08._build_window_data() replacing the current hardcoded-0 block.
    </description>
  </fix_negative_nna>

  <period_completeness_check label="Verify all windows compute correctly">
    <description>
      Andrew flagged "math I just don't understand in certain time periods."
      After fixing the above, spot-check ALL windows (QTD, YTD, 1Y, 3Y, Max) for
      at least 5 advisors each:
        1. commission = fee_bps_weighted/10000 × managed_aua × days/365.25: verify manually
        2. efficiency_pctile: verify rank ordering is correct within each window
        3. Advisors appearing in some windows but not others: document why (insufficient data?)

      Specific check: Max window (longest period) -- does calendar_days/365.25 correctly
      compute to the full history length, or is there a cap/truncation?

      Document any windows where the math looks off before declaring fixed.
    </description>
  </period_completeness_check>

  <acceptance_criteria>
    1. Root cause of Grace commission discrepancy documented and explained
    2. Root cause of Cole "ratio" display issue identified and fixed (DS data side)
    3. Negative NNA advisors have differentiated pctiles (no more all-zeros)
    4. All 5 windows spot-checked and math verified
    5. Findings posted to CTO inbox before any formula change committed to D_00/C_08
    6. efficiency_pctile field range confirmed 0-100 for all advisors after fix
  </acceptance_criteria>


  <compiler_tools>
    comp-pipescript io C_08
      -- Full I/O manifest for C_08: what it reads (fee_rate_history, account_performance,
         advisor_assignments_history) and what it writes (advisor_fee_efficiency.json).
         Run before diving into C_08's 300 lines -- confirms which parquets to query
         for the Grace and Cole investigations.

    comp-platinum reverse platinum/firm/fee_efficiency.json
      -- Traces fee_efficiency.json back through D_04 → C_08 → source parquets.
         Shows the exact field path from C_08's output to what the portal renders.
         Key for identifying whether the "ratio" display issue is in C_08 or D_04's
         pass-through.

    comp-blast gold/artifacts/advisor_fee_efficiency.json
      -- Shows all downstream consumers of C_08's output. Confirms only D_04 reads it
         (important before changing the output schema for the negative NNA fix).

    comp-transform schema-check FeeEfficiencyPanel
      -- Run after DS fixes land in platinum. Confirms all rendered fields in the
         panel match their TypeScript types and no new UNUSED fields were introduced.
         This is a post-fix verification tool, not pre-investigation.
  </compiler_tools>

</task_order>
