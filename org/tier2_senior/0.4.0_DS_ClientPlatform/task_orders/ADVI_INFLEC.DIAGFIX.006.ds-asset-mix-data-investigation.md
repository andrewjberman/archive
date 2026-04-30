<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.006</id>
    <project>ADVI_INFLEC</project>
    <title>Asset class / mix data investigation — determine Orion data availability for mix panel</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- closure 2026-04-29: RAVC VERDICT A (investigation-only TO; mix data exists via ETFClassifier on ticker+product_name); SUPERSEDED by DIAGFIX.010 Orion-native classifier (regex classifier + bd-securities cache deleted); flipped 2026-04-30 by COO ground-truth reconciliation -->
    <priority>high</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="diagnostic_brief">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ADVI_INFLEC_DIAGNOSTIC_BRIEF_20260429.md §C8</ref>
    <ref type="symptom_c8">timeseries_overview.mix.quarterly = 0 rows; timeseries_overview.mix.monthly = 0 rows; platinum/firm/mix_summary.json MISSING from S3</ref>
    <ref type="portal_behavior">Mix chart/panel shows "Asset class mix data unavailable"; getPlatinumFirmMixSummary() catches 404 and returns null</ref>
    <ref type="bd_precedent">data/black_diamond/scripts/gold/ — BD mix scripts for reference on expected schema</ref>
  </references>

  <context>
    The Inflection portal mix panel is completely dark. Two artifacts are missing:
    1. mix_summary.json — not on S3; getPlatinumFirmMixSummary() returns null
    2. timeseries_overview.mix — 0 rows in both quarterly and monthly

    Before DS builds anything, we need to know: does the Orion bronze/silver data
    for Inflection include asset class or model/strategy fields that would power a
    mix breakdown? Orion is a fundamentally different custodian stack than BD —
    the available field set may not include model_name, asset_class, or equivalent
    allocation metadata.

    This TO is an investigation. If data exists, DS proceeds to build mix_summary.json
    and populate timeseries_overview.mix. If data does not exist (or is too sparse to
    be useful), COO will suppress the mix panel for Inflection in layout.ts (DE scope).

    Two specific questions:
    Q1 — Asset class data: Does Orion silver include an asset_class (or equivalent)
         field on positions/holdings rows for Inflection? What are the distinct values?
         What fraction of positions/AUA has a populated asset_class?
    Q2 — Model/strategy data: Does Orion silver include a model_name, strategy,
         sleeve_name, or equivalent field? Same coverage check.

    These are the two inputs the mix panel needs: asset class breakdown (equity/fixed
    income/alternatives/cash/etc.) and optionally model/strategy allocation.
  </context>

  <scope>
    STEP 1 — Audit bronze/silver column availability:
    Load the Inflection silver holdings parquet(s) (silver/holdings/ or equivalent).
    List all column names. Check for any of:
      asset_class, asset_type, security_type, category, model_name, model_id,
      strategy, sleeve, allocation_type, style_box, broad_category

    If none are present in holdings, also check:
      silver/positions/ (if separate from holdings)
      silver/accounts/ (may have account-level model assignment)
      data/orion/manual_api/ or bronze CSVs for any allocation-related files

    STEP 2 — Coverage check (if any field found):
    For any candidate field found in Step 1:
      - df[field].notna().sum() and df[field].nunique()
      - df.groupby(field)['market_value'].sum().sort_values(ascending=False)
    Is the field populated for most accounts (~80%+) or only a minority?
    Report: field name, distinct values, AUA coverage (% of total).

    STEP 3 — BD parity check:
    Look at the BD mix script (data/black_diamond/scripts/gold/) to understand what
    field drives the BD mix panel. Document what Inflection has vs. what BD uses.
    Identify any gap (e.g., BD has model_name; Orion only has broad_category).

    STEP 4 — Verdict:
    Based on Steps 1-3, reach one of these conclusions:
      VERDICT A: Data exists, coverage sufficient (>80% AUA). DS can build mix_summary.json
                 and populate timeseries_overview.mix. Propose the field to use.
      VERDICT B: Data exists but coverage sparse (<50% AUA). Marginal value.
                 Recommend suppressing panel; note what would be needed for full coverage.
      VERDICT C: No asset class / model field present in Orion silver for Inflection.
                 Recommend suppressing the mix panel in layout.ts.

    RAVC to 2.0.0_SA_COO with verdict + evidence (column names, coverage %, sample values).
    COO will either:
      - On VERDICT A: issue a follow-on TO for mix_summary.json + timeseries.mix build
      - On VERDICT B/C: issue a DE TO to suppress the mix panel in layout.ts
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before investigation">
      <step>
        <run>comp-pipescript io INF_C_06</run>
        <expect>If INF_C_06 exists (client_mix_timeseries): shows what fields it reads.
        Column gaps in mix-related fields are directly relevant.</expect>
        <if_mismatch>If INF_C_06 does not exist or has no mix fields: document as evidence
        for VERDICT C. Include in RAVC.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="N/A — investigation only">
      <step>
        <run>N/A — no writes in this TO. No comp-* gate needed.</run>
        <expect>Absence acknowledged.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      Complete column audit of silver/holdings (and silver/positions, silver/accounts if
      needed): list every field checked and whether it exists + data type.
      Evidence: python output in session log.
    </criterion>
    <criterion id="2">
      Coverage report for any candidate mix field: distinct values, AUA coverage %.
      If no field found: explicit statement that no asset class / model field exists.
      Evidence: groupby / notna computation in session log.
    </criterion>
    <criterion id="3">
      BD parity note: what field BD uses vs. what Orion provides.
      Evidence: BD script field name vs. Orion silver field name (or absence).
    </criterion>
    <criterion id="4">
      RAVC to 2.0.0_SA_COO: explicit VERDICT A / B / C with evidence summary.
      No commit needed — investigation only.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="independent"/>
    Parallelizable with DIAGFIX.001-005. Investigation only.
    VERDICT gates any follow-on mix build or panel suppression TO.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    Read-only investigation. No gold script changes in this TO.
  </cross_domain_coordination>

  <commit_identity>
    No commit needed — investigation only. Session log entry + RAVC to COO.
  </commit_identity>
</task_order>
