<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.008</id>
    <project>ADVI_INFLEC</project>
    <title>Build Inflection asset-class mix — mix_summary.json + timeseries_overview.mix using BD ETFClassifier</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- closure: 15a8f8591 (INF_I_D02d firm_mix_summary composer; mix_summary.json publishes from firm_composition; SUPERSEDED-BY DIAGFIX.010 Orion-native classifier metadata propagation 6f60a47eb); flipped 2026-04-30 by COO ground-truth reconciliation -->
    <priority>high</priority>
    <estimated_effort>2-3h</estimated_effort>
  </metadata>

  <references>
    <ref type="verdict_source">DIAGFIX.006 RAVC VERDICT A (DS 20260429T210Z)</ref>
    <ref type="classifier">data/black_diamond/scripts/gold/lib/etf_classifier.py — BD ETFClassifier (DynamoDB bd-securities + regex fallback)</ref>
    <ref type="test_result">ETFClassifier tested on Inflection holdings_2026-04-28.parquet: 100% AUA classifies. Equity 55.9%, Fixed Income 32.2%, Alternatives 9.7%, Cash 2.2%.</ref>
    <ref type="model_data">silver/api_dims/accounts_v2.model_name — 21 distinct models, 89% AUA coverage ($79.7M/$89.6M)</ref>
    <ref type="iam_dependency">inf-gold-runner may need DynamoDB read on bd-securities table. AE 0.6.1 IAM check in parallel (comp-iam service). See IAM note in scope.</ref>
    <ref type="portal_consumer">mix panel in portal layout — mix_summary.json fetched via getPlatinumFirmMixSummary() (currently returns null — 404); timeseries_overview.mix.quarterly/monthly currently 0 rows</ref>
    <ref type="bd_reference">data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py — BD mix script pattern</ref>
  </references>

  <context>
    DIAGFIX.006 VERDICT A: Orion silver has no raw asset_class field, but BD's ETFClassifier
    (lib/etf_classifier.py) works on (ticker, product_name) and classifies Inflection holdings
    with 100% AUA coverage:
      Equity: $50.05M (55.9%)
      Fixed Income: $28.81M (32.2%)
      Alternatives: $8.73M (9.7%)
      Cash: $2.01M (2.2%)

    One edge case noted by DS: FDRXX (Fidelity Govt Cash Reserves) classifies as fixed_income
    (should be cash) — same as BD handles it. Acceptable for V1.

    Additionally, silver/api_dims/accounts_v2.model_name has 21 distinct IWM/Opal models with
    89% AUA coverage ($79.7M/$89.6M). This is a Inflection-specific secondary dimension for
    a V2 model breakdown panel (out of scope for this TO — noted for later).

    IAM NOTE: The ETFClassifier reads DynamoDB table bd-securities. If inf-gold-runner does not
    have a DynamoDB read policy for bd-securities, the ETFClassifier will fall back to regex-only
    mode. Check: does regex-only mode correctly classify the Inflection holdings tickers?
    DS ran the test in DIAGFIX.006 and got 100% classification — confirm whether this was
    with DynamoDB or regex-fallback. If regex-fallback works for all Inflection tickers,
    DynamoDB access is not needed. AE 0.6.1 running comp-iam check in parallel — see IAM note.

    Do NOT wait for IAM confirmation to start coding. If regex-fallback produces 100% coverage
    in your local test, the script will work without DynamoDB IAM grant. Note which mode
    you used in the RAVC.
  </context>

  <scope>
    STEP 0 — Orion manual_api classification investigation (DO THIS FIRST):
    Before building any classifier, check data/orion/manual_api/ for existing scripts or
    endpoints that return security-level classification data from Orion directly.
    Specifically:
    - Does any existing pull script (pull_inflection_positions.py, pull_inflection_securities.py,
      or equivalent) return asset_class / category / security_type / broad_category alongside
      ticker + product_name in the API response?
    - If yes: pull a sample, document field name + distinct values + AUA coverage.
      RAVC to COO with findings. Use Orion-native classification as PRIMARY source if
      coverage > 70% AUA. Do NOT proceed to ETFClassifier build until COO ACKs.
    - If no native classification in Orion API: document "Orion API has no native classification
      — proceeding with ETFClassifier regex-fallback" in RAVC, then proceed to STEP 1.

    NOTE — Opal securities: Do NOT add special handling for Opal model portfolio securities.
    Andrew assessment: any Opal securities in Inflection's portfolio are coincidental and
    negligible AUA. Classify them via the same path as any other ticker. Flag count in RAVC
    if >5 Opal-branded tickers appear.

    STEP 0a — Verify ETFClassifier mode (only if Step 0 finds no Orion-native data):
    In your DIAGFIX.006 test, check if the classifier used DynamoDB lookups or regex-only.
    Quick test: instantiate with no DDB arg / offline mode and re-run on holdings.
    If coverage is still 100% in regex-only mode: no IAM dependency. Note in RAVC.

    STEP 1 — Create mix script:
    Read BD's C_06.client_mix_timeseries.py in full for pattern reference.
    Create a new script: data/orion/scripts/gold/INF_C_06.asset_mix.py
    (DS: if INF_C_06 is already taken by an AUA timeseries script, use INF_C_08.asset_mix.py
    and rename the existing script in a separate cleanup commit. Do NOT rename and build in
    the same commit — scope it cleanly.)
    
    The script must:
    - from __future__ import annotations (mandatory first import)
    - Load gold/canonical/holdings_{date}.parquet (latest)
    - Load silver/api_dims/assets or equivalent for product_name (ticker name field)
    - Run ETFClassifier on each (ticker, product_name) pair
    - Output platinum/firm/mix_summary.json with schema matching what BD's mix panel expects:
        {
          "data_as_of": "2026-04-28",
          "total_aua": 89590439.60,  (use actual holdings sum — will improve post-002b)
          "mix": [
            {"class": "equity", "value": 50050000.00, "pct": 0.559},
            {"class": "fixed_income", "value": 28810000.00, "pct": 0.322},
            {"class": "alternatives", "value": 8730000.00, "pct": 0.097},
            {"class": "cash", "value": 2010000.00, "pct": 0.022}
          ]
        }
    Verify this schema matches what BD's mix panel expects (check portal code or BD mix artifact).
    
    STEP 2 — Populate timeseries_overview.mix in INF_D_04:
    In INF_D_04.client_portal_summary.py, find the _build_timeseries_overview() function.
    Locate the mix block: currently emits quarterly=[], monthly=[] (empty arrays).
    For each quarter/month with available holdings data, compute the ETFClassifier breakdown.
    Use the same historical holdings parquets available in gold/canonical/.
    If only the current date's holdings exist (no historical): emit current period only with
    a note in RAVC. Do NOT block delivery on historical backfill — V1 with current period
    is acceptable.

    STEP 3 — Pre-commit gate + S3:
    .tools/ds-commit-gate.sh on new mix script + INF_D_04 (if modified)
    aws s3 cp platinum/firm/mix_summary.json to s3://opal-data-inf/platinum/firm/mix_summary.json
    aws s3 cp script to s3://opal-data-inf/code/gold/
    MD5 MATCH verification (comp-pipescript deployed skipped per INF precedent)

    STEP 4 — Re-run + verify:
    Run mix script to generate mix_summary.json.
    If INF_D_04 is modified for timeseries.mix: dispatch INF_D_04 re-run via SSM after the main re-run wave is complete.
    Verify:
      aws s3 ls s3://opal-data-inf/platinum/firm/mix_summary.json (exists, non-empty)
      python3 parse: mix[0].class = 'equity', mix[0].pct approx 0.55
      timeseries_overview.mix.quarterly: at least 1 row
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_C_06 (to confirm if INF_C_06 is taken by another script)</run>
        <expect>If INF_C_06 WRITES timeseries_chart.json or AUA timeseries: use INF_C_08 instead.
        If INF_C_06 shows no output (or shows mix_summary.json): proceed with INF_C_06.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_06.asset_mix.py (or INF_C_08)</run>
        <expect>Exit 0. py_compile + AST + ruff all pass.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 artifact upload">
      <step>
        <run>aws s3 ls s3://opal-data-inf/platinum/firm/mix_summary.json</run>
        <expect>Non-empty file. Artifact exists.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      platinum/firm/mix_summary.json exists on S3. Schema has: data_as_of, total_aua, mix array
      with equity/fixed_income/alternatives/cash entries. Non-zero values.
      Evidence: aws s3 ls + python parse.
    </criterion>
    <criterion id="2">
      timeseries_overview.mix.quarterly has at least 1 row (current period).
      Evidence: python parse of timeseries_overview.json after INF_D_04 re-run.
    </criterion>
    <criterion id="3">
      ds-commit-gate.sh exit 0. S3 artifact uploaded. MD5 MATCH for script.
    </criterion>
    <criterion id="4">
      RAVC to 2.0.0_SA_COO: ETFClassifier mode (DDB or regex-fallback), mix breakdown values,
      artifact S3 verification, timeseries.mix row count, commit hash.
      Note any historical gaps in timeseries.mix if only current period available.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" status="complete">DIAGFIX.006 VERDICT A — ETFClassifier confirmed to work on Inflection holdings</dependency>
    <dependency agent="0.6.1_AE_PartnerETL" status="in_progress">
      IAM check: comp-iam service inf-gold-runner for DynamoDB bd-securities read.
      If IAM gap found: DO NOT BLOCK — use ETFClassifier regex-fallback mode for V1.
      AE will add IAM grant as a follow-on if DDB mode needed.
    </dependency>
    Parallelizable with DIAGFIX.002a/002b/007 but lower urgency.
    Run AFTER the main re-run wave (DIAGFIX.002a → AE re-run → verify) so timeseries.mix
    is populated with the correct AUA-scale data from the fixed INF_D_04.
    NOTE: mix_summary.json generation can run NOW independent of the re-run wave.
    timeseries.mix INF_D_04 integration should wait until after the re-run wave completes
    to avoid a mid-flight INF_D_04 conflict.
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      DE to confirm mix panel renders after mix_summary.json is available on S3.
      DE had confirmed mix panel shows "Asset class mix data unavailable" with null response —
      it will auto-load once the S3 artifact exists (no portal code change needed per C8 diagnostic).
      AE 0.6.1: IAM check for inf-gold-runner DynamoDB bd-securities read (parallel task).
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "feat(ADVI_INFLEC.DIAGFIX.008): INF_C_06/C_08 asset-class mix via ETFClassifier — mix_summary.json + timeseries.mix" \
      -- data/orion/scripts/gold/INF_C_06.asset_mix.py [or INF_C_08] [+ INF_D_04 if timeseries.mix added]
  </commit_identity>
</task_order>
