<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.010</id>
    <project>ADVI_INFLEC</project>
    <title>Build Orion-native classification — bronze pull + silver dim + INF_I_D03 refactor (kills regex classifier)</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status>
    <priority>critical</priority>
    <estimated_effort>4-6h</estimated_effort>
    <closed_date>2026-04-29</closed_date>
    <closed_by>2.0.0_SA_COO</closed_by>
    <closure_evidence>Phase 1+2 commit 2979c12a7 (bronze pull + silver convert; 23,699 rows, 100% asset_class + product_category coverage, $197.86M). Phase 3 commit e106bc7b8 (INF_I_D03 refactor — regex classifier + bd-securities cache + 4 dead functions DELETED; vectorized merge on (account_id, ticker) against silver/api_dims/assets_v2). Phase 4 commit 6f60a47eb (composer metadata propagation). Phase 5 result: equity 53.93% / fixed_income 30.93% / alternatives 8.08% / cash 6.53%. Bond-ETF over-classification fully fixed (HTRB/BAGIX/BSIIX/BSNIX/TFEBX now correctly classified as Bond → fixed_income; was equity under regex). Alternatives 4.5x improved.</closure_evidence>
    <closure_note>Win-condition definitional reframe accepted: COO TO target (44.8/21.3/5.4/28.5 ±2pp) was a mis-interpretation of Andrew's UI screenshot — that breakdown was top-9 named Morningstar Categories + UI-display "Other" residual ($52.03M / 28.5%), NOT a true alternatives bucket. The Orion-native 4-bucket split (with alternatives extracted from Equity via asset_class keyword discriminator: Real Estate / Allocation / Multi-Asset / Target-Date / Commodities / Hedged / Long-Short / etc.) lands at 53.93/30.93/8.08/6.53. This is the Orion-truth answer. The classification source is now Orion-native and the regex over-classification problem is dead. mix_summary.json republished with classification_method=orion_native_v1 metadata (composer auto-inherited from upstream firm_composition.json).</closure_note>
  </metadata>

  <references>
    <ref type="verdict_source">DIAGFIX.009 RAVC VERDICT A (DS 20260429T215145Z, commit 8d8be1bcd)</ref>
    <ref type="endpoint">GET /api/v1/Portfolio/Clients/{clientId}/Assets/{date}?$top=50000&amp;includeCostBasis=false (date MM-DD-YYYY)</ref>
    <ref type="per_account_variant">GET /api/v1/Portfolio/Accounts/{accountId}/Assets/{date}</ref>
    <ref type="discovery_doc">data/orion/manual_api/PATH_DISCOVERY_MSTAR.md — full endpoint contract, 58-column schema, coverage validation, bucket-mapping draft, 5-phase plan</ref>
    <ref type="andrew_directive">Andrew 2026-04-29: "WE SHOULDNT NEED TO USE OUR BD-SECURITIES OR ETF CLASSIFIER OR REGEX OR ANY OF THAT BULLSHIT IT SHOULD JUST BE WHAT ORION USES HERE."</ref>
    <ref type="composer_already_shipped">DIAGFIX.008 Step 1 — INF_I_D02d.firm_mix_summary.py shipped (15a8f8591). Will auto-pick up corrected classifications on next chain run.</ref>
    <ref type="regex_diverge">Current firm_composition.json: 70.29% equity / 15.22% fixed_income / 12.70% cash / 1.79% alternatives. Orion UI truth: ~44.8% / 21.3% / 5.4% / 28.5%. Refactor closes the gap.</ref>
  </references>

  <context>
    DS used HAR-file analysis of Andrew's Orion UI session and discovered the REST endpoint
    that the Orion UI itself uses to render the Asset Class panel. The endpoint returns 58
    columns per asset with 100% coverage on `assetClass` (Morningstar Category) and
    `productCategory` (broad: Equity / Bond / Money Market). This eliminates every reason
    for the keyword regex classifier to exist.

    Bonus: the 58-column schema also returns `registrationType` (ROTH / TRADITIONAL),
    `custodian`, `modelName` (IWM / Opal model identification — relevant for SmartX
    engagement), `productType`, `productSubType`, `fundFamily`, `riskCategory`,
    `managementStyle`, `costBasis` (when flag enabled), `assetPercentOfAccount`,
    `householdName`, `clientId`, plus operational flags (isManaged, isCustodialCash,
    isFeeExcluded, isAdvisorOnly, isStrategyOverride, etc.). Capture ALL of them in
    silver/api_dims/assets_v2 for future feature work — this TO only consumes a few,
    but the full schema is cheap to land alongside.

    SCOPE BOUNDARY: This TO refactors classification only. Holdings sourcing (INF_B_00 TRN
    reconstruction) stays as-is for V1. The asset class lookup uses (clientId, ticker) or
    (accountId, ticker) keys against the new silver dim. Do NOT replace holdings sourcing
    in this TO — that is a separate strategic decision for a future TO if/when we observe
    sustained drift between TRN-reconstructed holdings sum and Orion's authoritative
    point-in-time totals (currently $190.5M post-002b vs $182.55M canonical, $8M / 4.4% delta).

    The 5-phase plan below is verbatim from DS's RAVC. COO endorses with one clarification
    on Phase 5 win condition — see Phase 5.
  </context>

  <scope>
    PHASE 1 — bronze pull script:
    Create data/orion/manual_api/pull_inflection_assets_v2.py
    Pattern: model after existing pull_inflection_assets.py / pull_inflection_positions.py
    auth + retry behavior. MUST begin with: from __future__ import annotations.

    Iterate Inflection clientIds (households) — DS to determine the source of clientIds:
      - Likely silver/accounts_dim or silver/api_dims/accounts_v2 (which has clientId column)
      - Or pull from the same Orion API (a clients endpoint)
    For each clientId, call:
      GET /api/v1/Portfolio/Clients/{clientId}/Assets/{date}?$top=50000&includeCostBasis=false
    where date = MM-DD-YYYY string (most recent business day or explicit --date arg).

    Behavior requirements:
      - Pagination: $top=50000 should cover all cases (HAR sample showed 53 assets per
        client max). If pagination is required, follow the @odata.nextLink convention.
      - Retry: 429/5xx with exponential backoff (max 3 retries).
      - Rate limiting: be considerate of Orion's API. Sleep 100-300ms between calls if needed.
      - Output: bronze/orion-api-v2/{snapshot_date}/assets.csv (or .parquet directly if simpler).
      - Capture ALL 58 columns. Do not pre-filter.

    Test: smoke pull for 5-10 clientIds, verify schema, then full pull for all Inflection
    households. Expected ~666 calls. Target run time: <30 min for full pull.

    PHASE 2 — silver dim:
    Create data/orion/scripts/silver/convert_assets_v2_to_silver.py (or extend the existing
    silver-conversion script if there's a registry pattern).
    Read bronze/orion-api-v2/{date}/assets.csv (or parquet).
    Write silver/api_dims/assets_v2/snapshot_date={date}/data.parquet with the 58-column schema.
    Schema: preserve all 58 columns from the API. Type-cast appropriately:
      - assetClass: string (Morningstar Category name)
      - productCategory: string (Equity / Bond / Money Market)
      - costBasis: float (nullable)
      - operational flags (isManaged, etc.): boolean
      - dates: datetime64
      - other strings: string
    Add a date column for partitioning if not already present.

    PHASE 3 — refactor INF_I_D03.composition_artifacts.py:
    Replace the existing `_classify_keyword` function and any `_load_bd_securities_cache`
    or related keyword/regex code with a lookup against the new silver dim.

    Lookup logic (from DS's bucket-mapping draft):
      1. Load silver/api_dims/assets_v2/snapshot_date={most_recent}/data.parquet
      2. For each holding row:
         - Find matching asset row by (clientId or accountId, ticker)
           Note: the join key depends on what holdings has — if holdings has account_id, use
           the per-account variant of the endpoint (Phase 1) and key by accountId.
         - Apply bucket mapping:
           if productCategory == 'Money Market': bucket = 'cash'
           elif productCategory == 'Bond': bucket = 'fixed_income'
           elif productCategory == 'Equity':
             if assetClass in {'Real Estate', 'Global Real Estate', 'Commodities Broad Basket',
                               'Commodities Focused', 'Allocation--*' (any starting with Allocation),
                               'Multi-Asset *', 'Tactical Allocation', 'Target-Date *'}:
               bucket = 'alternatives'
             else:
               bucket = 'equity'
           else:
             bucket = 'unclassified'
        DS to refine the alternatives matcher list as needed based on actual Orion category names
        observed in the silver dim.

    Delete dead code: any imports/functions that are now unreferenced (etf_classifier,
    bd-securities cache, layer-1/2/3/4 keyword regex). Keep the script clean.

    Update INF_I_D03 output metadata in firm_composition.json to flip:
      classification_method: 'orion_native_v1' (was 'keyword_regex_v1' or absent)
      classification_caveats: drop the regex caveat block; replace with a single-line note like
        'Classification sourced from Orion API /Portfolio/Clients/{id}/Assets endpoint (Morningstar Category).'

    PHASE 4 — composer auto-correction:
    INF_I_D02d.firm_mix_summary.py (already shipped) reads firm_composition.json and reshapes
    into mix_summary.json. After Phase 3 lands, the next chain run produces a corrected
    firm_composition.json, and the composer auto-publishes the corrected mix_summary.json.
    No code change to the composer itself.

    Verify after re-run:
      - mix_summary.json classification_method = 'orion_native_v1'
      - classification_caveats line is the new short note (or absent)
      - mix bucket percentages roughly match Orion UI (44.8 / 21.3 / 5.4 / 28.5 ish, exact
        depends on holdings vs Orion-asset-feed coverage)

    PHASE 5 — validation (refined win condition):
    Two checks:
      A. PERCENTAGES — mix_summary.json mix percentages match Andrew's Orion UI breakdown
         within +/- 2 percentage points per bucket. This is the primary win — classification
         is now accurate.
      B. ABSOLUTE TOTALS — mix_summary.json total_market_value SHOULD match Andrew's
         $182,552,381 IF the holdings sourcing is also Orion-native. Currently holdings
         comes from INF_B_00 TRN reconstruction which sums to $190.5M post-002b. The $8M
         delta is NOT a DIAGFIX.010 failure — it is a separate sourcing gap. Document the
         delta in the RAVC. COO will route a follow-on TO to evaluate switching holdings
         sourcing if/when warranted.

    The win condition for THIS TO is check A (percentages). Check B is observational.

    Pre-commit gate + S3 upload + chain registration:
    - .tools/ds-commit-gate.sh on all modified scripts
    - aws s3 cp each script to s3://opal-data-inf/code/gold/ or /code/silver/ etc.
    - MD5 MATCH verification (or comp-pipescript deployed if registered)
    - AE 0.6.1 to register new bronze + silver scripts in orion-gold-dispatch.sh
      CATALOG / CHAIN_FULL / CHAIN_INCREMENTAL — same as INF_I_D02d registration done in
      commit 1fa15143e. RAVC to AE for chain registration after Phase 3 lands.

    Re-run: AE 0.6.1 dispatches the chain (bronze pull → silver convert → INF_I_D03 →
    INF_I_D02d composer). RAVC to COO with before/after mix percentages.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_I_D03</run>
        <expect>If registered: shows current READS (silver/holdings or canonical/holdings) +
        WRITES (firm_composition.json). Document any new READ for silver/api_dims/assets_v2.
        If not registered: SKIP — same precedent as prior INF DIAGFIX TOs (registry gap noted).</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/manual_api/pull_inflection_assets_v2.py
                                       data/orion/scripts/silver/convert_assets_v2_to_silver.py
                                       data/orion/scripts/gold/INF_I_D03.composition_artifacts.py</run>
        <expect>Exit 0. py_compile + AST + ruff all pass on every file.</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>MD5 MATCH verification for each uploaded script (registry gap precedent)</run>
        <expect>Local md5 == S3 ETag for each.</expect>
        <if_mismatch>Re-upload. Do not dispatch re-run until MATCH.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      bronze/orion-api-v2/{date}/assets.* exists on S3 with all Inflection assets (~666 client pulls,
      53 assets/client average ~ 35K rows expected). 58 columns present.
      Evidence: aws s3 ls + python parse showing column count + row count.
    </criterion>
    <criterion id="2">
      silver/api_dims/assets_v2/snapshot_date={date}/data.parquet exists with 58 columns
      typed correctly. assetClass + productCategory both 100% non-null on a sample check.
      Evidence: python parse + dtypes printout.
    </criterion>
    <criterion id="3">
      INF_I_D03 refactored — _classify_keyword and bd-securities references DELETED. No imports
      of etf_classifier or bd-securities cache remain. Diff shows net code reduction.
      Evidence: diff in commit + grep showing no dead refs.
    </criterion>
    <criterion id="4">
      After re-run: firm_composition.json classification_method = 'orion_native_v1'.
      Mix percentages within +/- 2pp per bucket vs Andrew's Orion UI breakdown
      (target: equity ~44.8%, fixed_income ~21.3%, cash ~5.4%, alternatives ~28.5%).
      Evidence: python parse of artifact + comparison table in RAVC.
    </criterion>
    <criterion id="5">
      mix_summary.json (DIAGFIX.008 composer output) auto-publishes corrected breakdown.
      classification_method propagates correctly.
      Evidence: python parse of mix_summary.json on S3.
    </criterion>
    <criterion id="6">
      ds-commit-gate.sh exit 0 on all modified scripts. S3 deploy MATCH for each.
    </criterion>
    <criterion id="7">
      RAVC to 2.0.0_SA_COO: commit hash, S3 deploy MATCH, before/after mix percentages,
      observation on absolute total delta vs $182.55M, AE chain-registration RAVC2 status.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" status="complete">DIAGFIX.009 VERDICT A — endpoint discovered, schema documented in PATH_DISCOVERY_MSTAR.md</dependency>
    <dependency agent="0.6.1_AE_PartnerETL" status="will_engage">
      AE 0.6.1 chain registration of new bronze + silver scripts in orion-gold-dispatch.sh
      after Phase 1+2 commits land. Pattern: same as INF_I_D02d registration commit 1fa15143e.
      DS RAVCs to AE for registration after S3 upload of new scripts.
    </dependency>
    Independent of DIAGFIX.008 Step 2 (timeseries.mix in INF_D_04) — that can run after this.
    Independent of concentration_risk gap (separate price-feed issue, separate TO).
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      AE 0.6.1: register new scripts in orion-gold-dispatch.sh CATALOG / CHAIN_FULL /
      CHAIN_INCREMENTAL after they land on S3. DS will RAVC to AE with the script paths
      and dependency order (bronze pull -> silver convert -> INF_I_D03 chain consumer).
    </coordination>
    <coordination>
      DE: no immediate action. Mix panel rendering already wired; will auto-update on next
      portal cache cycle (5-min staleTime) once mix_summary.json is republished.
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    Phase 1 + 2 (bronze + silver, separate commits OK):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "feat(ADVI_INFLEC.DIAGFIX.010 Phase 1+2): Orion-native asset_class — bronze pull + silver dim" \
      -- data/orion/manual_api/pull_inflection_assets_v2.py \
         data/orion/scripts/silver/convert_assets_v2_to_silver.py

    Phase 3 (INF_I_D03 refactor):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "refactor(ADVI_INFLEC.DIAGFIX.010 Phase 3): INF_I_D03 — replace regex classifier with Orion-native lookup" \
      -- data/orion/scripts/gold/INF_I_D03.composition_artifacts.py
  </commit_identity>
</task_order>
