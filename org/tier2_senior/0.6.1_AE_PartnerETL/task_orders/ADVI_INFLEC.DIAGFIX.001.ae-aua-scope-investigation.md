<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.001</id>
    <project>ADVI_INFLEC</project>
    <title>AUA scope investigation — trace holdings $89.6M vs aum_snapshot $182.6M gap</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- closure 2026-04-29: investigation verdict shipped via session log; root cause = INF_B_00 nav_price guard (40.2% market_value=$0) + _build_aua_view targeting holdings instead of aum_snapshot; both fixed in DS DIAGFIX.002a (aa030d272) + DIAGFIX.002b (127fe2a17); geo donut downstream fix shipped (e39ebd025); flipped 2026-04-30 by COO ground-truth reconciliation -->
    <priority>critical</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnostic_brief">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ADVI_INFLEC_DIAGNOSTIC_BRIEF_20260429.md §Part 1C C1</ref>
    <ref type="silver_holdings">s3://opal-data-inf/silver/holdings/ (or local data/)</ref>
    <ref type="silver_aum">s3://opal-data-inf/silver/aum_snapshot/2026-04-29.parquet</ref>
    <ref type="inflection_rep_ids">INFLECTION_REP_IDS = {3, 11, 12}</ref>
  </references>

  <context>
    Every gold script that aggregates advisor-level data lands at $89.6M:
    - partner_analytics_quarterly.views.aua.donut.total = $89,590,439
    - leaderboard QTD sum = $89,590,439
    - book.json sum across all 3 advisors = $89,590,439

    But canonical header_metrics.total.aua = $182,552,380 (from aum_snapshot managed_value.sum()).

    DE brief hypothesis: a shared upstream filter in the silver holdings excludes roughly half
    the firm's accounts. The ~$93M gap is too consistent to be a script-level bug — it points
    to silver data coverage.

    This TO investigates WHY the holdings-derived total = $89.6M when the managed AUM = $182.6M.
    The finding will gate DIAGFIX.002a (partner_analytics scope fix).
  </context>

  <scope>
    STEP 1 — Quantify the silver holdings for Inflection:
    Load silver/holdings/ parquet(s) filtered to rep_ids {3, 11, 12}.
    Compute: market_value.sum(), unique household_id count, unique account_id count.
    Target: confirms ~$89.6M market_value across N households.

    STEP 2 — Compare against aum_snapshot 2026-04-29:
    Load silver/aum_snapshot/2026-04-29.parquet.
    Compute: managed_value.sum() (should be ~$182.6M), unique household_id count.
    Cross-join by household_id: how many HH are in aum_snapshot but NOT in silver/holdings/?

    STEP 3 — Characterize the gap:
    For the ~$93M of accounts IN aum_snapshot but NOT IN silver/holdings:
    - How many households? (~130-150 estimated based on $93M delta)
    - Are they assigned to a specific rep_id (3, 11, or 12)?
    - Do they appear in silver/accounts/ with any account_status code (e.g., 'inactive', 'pending')?
    - Do they appear in silver/positions/ at all?

    STEP 4 — Root cause hypothesis:
    Based on Step 3, identify the most likely cause:
    A. Accounts exist in aum_snapshot but have NO positions data in the Orion holdings export
       (managed externally / model-only / fee-only accounts with no security positions)
    B. Accounts filtered out by a status code in the silver canonical_holdings script
       (e.g., account_status != 'active' filter in INF_B_00.canonical_holdings.py)
    C. Accounts have different rep_id in holdings vs aum_snapshot (ID mismatch)
    D. Something else

    STEP 5 — Quick check on INF_B_00.canonical_holdings.py:
    Read data/orion/scripts/gold/INF_B_00.canonical_holdings.py.
    Check for any account_status, account_type, or AUM-filter that could exclude accounts.
    Note the filter criteria.

    RAVC to COO with: Step 1-3 numbers + Step 4 root cause + Step 5 filter audit.
    Do NOT attempt fixes — investigation only. COO routes DIAGFIX.002a after findings.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before investigation">
      <step>
        <run>comp-pipescript io INF_B_00</run>
        <expect>READS: silver/holdings or orion bronze. Shows any column gaps that could explain missing accounts.</expect>
        <if_mismatch>Document any COLUMN GAPS in RAVC.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="N/A — investigation only">
      <step>
        <run>N/A — no comp-* tool for silver parquet inspection. Documented as out-of-scope.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      Exact silver/holdings market_value.sum() for rep_ids {3,11,12}. Confirms ~$89.6M baseline.
      Evidence: python3 computation in session log.
    </criterion>
    <criterion id="2">
      Household ID cross-join: N households in aum_snapshot NOT in holdings. Managed value of gap.
      Evidence: computation in session log.
    </criterion>
    <criterion id="3">
      Root cause classified (A/B/C/D from Step 4) with evidence.
      Evidence: analysis + supporting parquet query in session log.
    </criterion>
    <criterion id="4">
      INF_B_00 filter audit: any account_status / account_type filters documented.
      Evidence: code excerpt in session log.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO: all findings with explicit recommendation for fix path.
      COO will route DIAGFIX.002a (scope fix) once findings received.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="none"/>
    Investigation TO — parallelizable with DIAGFIX.002/.003/.004/.005.
    Does NOT block DIAGFIX.002 (dashboard crash fix) or DIAGFIX.003-005.
    DOES gate DIAGFIX.002a (partner_analytics scope fix) — that TO fires after this RAVC.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    Read-only investigation. No gold script changes in this TO.
  </cross_domain_coordination>

  <commit_identity>
    No commit needed — investigation only. Session log entry + RAVC to COO.
  </commit_identity>

  <notes>
    Also check: do the "missing" accounts appear in any Orion bronze CSV
    (data/orion/manual_api/ or bronze S3) under a filename that suggests they
    were never included in the holdings pull? This would confirm Option A above.
  </notes>
</task_order>
