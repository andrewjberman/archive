<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-mvplvl-010-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
  </metadata>

  <objective>
    Three diagnostic + fix workstreams for the last remaining data quality issues
    in AdvisorIntelligence. All three are DS-owned (gold scripts + S3 artifacts).
    Findings from WS3 will directly inform the GLDRST canonical methodology.

    WS1: L2 advisor composition not rendering in Books tab
    WS2: PartnerAnalytics Mix toggle showing empty (firm_mix_views.json)
    WS3: Tax liability totals diverge from AUA totals
  </objective>

  <context>
    Architecture:
    - Script 12 (12_build_composition_artifacts.py) writes per-advisor composition
      to gold/advisors/{advisor_id}/composition.json. Lambda reads that key.
      Portal calls getBooksAdvisorComposition(advisorId). N1 (firm) works; L2 does not.
    - Script 06b (06b_build_client_mix_timeseries.py) writes firm_mix_views.json
      and per-advisor mix.json. The PartnerAnalytics Mix toggle reads firm_mix_views.json.
    - Script 06 (06_build_client_tax_liability.py) computes tax breakdown from
      holdings_lots. Script 05 computes AUA from positions_cube. They use different
      base datasets, different pricing, and different account exclusion logic.

    Last full gold run: 2026-03-24 (PRICES.001 ephemeral c5.4xlarge)
    Last incremental gold run: 2026-03-25 (DEBT_1STRUN deploy session)
    Portal PROD: portal-v2.1.17 (2026-03-23, 52-commit merge)
    Lambda: partners-api-v1.9.0

    Key files:
    - data/black_diamond/scripts/gold/12_build_composition_artifacts.py
    - data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py
    - data/black_diamond/scripts/gold/06_build_client_tax_liability.py
    - data/black_diamond/scripts/gold/05_build_client_performance.py
    - data/black_diamond/scripts/gold/02_build_positions_cube.py
    - infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
    - portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx
    - portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx
  </context>

  <scope>
    <files>
      <file action="diagnostic">s3://opal-data-bd/gold/advisors/ (list all composition.json files)</file>
      <file action="diagnostic">s3://opal-data-bd/gold/firm_mix_views.json</file>
      <file action="diagnostic">s3://opal-data-bd/gold/views/client_tax_liability.parquet</file>
      <file action="modify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="modify">data/black_diamond/scripts/gold/06_build_client_tax_liability.py</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- WS1: L2 Advisor Composition (Books Tab)                      -->
    <!-- ============================================================ -->
    <requirement id="1">
      WS1 DIAGNOSTIC: Verify advisor composition artifacts exist on S3.

      Step 1a: List all advisor composition files:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep composition.json

      Step 1b: If files exist, pick 3 advisors that are visible in the portal.
      Download their composition.json and verify:
        - JSON is well-formed
        - mix[] array is non-empty with market_value > 0
        - top_holdings[] is non-empty
        - advisor_id in scope matches what the portal would send

      Step 1c: If files are MISSING or EMPTY:
        - Check script 12's log output from the 2026-03-25 gold run
        - Trace the rel_architect_lookup.parquet: how many unique architects?
        - Are any architects mapped to "Unassigned" and thus excluded?
        - Is account_performance.parquet filtering too aggressively (45-day gate)?

      Step 1d: Verify S3 key alignment. The portal sanitizes advisor names via
      ClientsTab.tsx:383 (JS). Script 12 sanitizes via _advisor_id() at line 163
      (Python). Download the actual S3 keys and compare against what the portal
      sends in the HTTP request. Any mismatch = the artifact exists but the Lambda
      can't find it.
    </requirement>

    <requirement id="2">
      WS1 FIX: Based on diagnostic findings, fix the root cause:

      If artifacts missing: fix script 12 (architect lookup, filtering logic, etc.)
      If key mismatch: align sanitization between Python and TypeScript
      If artifacts present and keys match: the issue is in the Lambda or portal
        wiring -- document the finding and escalate to DE.

      Commit any script changes to CLOUD with descriptive message.
    </requirement>

    <!-- ============================================================ -->
    <!-- WS2: PartnerAnalytics Mix Toggle (firm_mix_views.json)       -->
    <!-- ============================================================ -->
    <requirement id="3">
      WS2 DIAGNOSTIC: Inspect firm_mix_views.json on S3.

      Step 2a: Download and inspect:
        aws s3 cp s3://opal-data-bd/gold/firm_mix_views.json - | python -m json.tool | head -100

      Check:
        - How many periods in views.quarterly? views.monthly? views.annually?
        - Are the values non-zero?
        - Does data_as_of match the latest gold run date?

      Step 2b: If only 1 period per granularity, this confirms the known issue:
      incremental 06b runs only accumulate data for the lookback window. The
      03-24 FULL gold run should have populated full history. Verify whether the
      full run actually executed 06b (check the run log).

      Step 2c: Also check per-advisor mix files:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep mix.json
      Verify at least a few advisors have mix.json with multiple periods.

      IMPORTANT: The Lambda route handle_advisor_mix_timeseries() reads
      gold/advisors/{id}/mix_timeseries.json (line 1056), but script 06b writes
      gold/advisors/{id}/mix.json. This is a confirmed S3 key mismatch for the
      advisor mix-timeseries route. Document whether this affects the firm-level
      Mix toggle (it should not -- firm uses firm_mix_views.json which is correct).
    </requirement>

    <requirement id="4">
      WS2 FIX: Based on findings:

      If firm_mix_views.json is sparse: determine whether a full gold rerun is
      needed, or whether 06b can be modified to rebuild full history from
      mix_daily.json accumulators without a full pipeline run.

      If the advisor mix_timeseries.json key mismatch is confirmed: fix EITHER
      the Lambda (read mix.json instead of mix_timeseries.json) OR script 06b
      (write mix_timeseries.json as an alias). Prefer fixing 06b since Lambda
      changes require Terraform deploy. Add a symlink write or rename.

      Commit any script changes to CLOUD.
    </requirement>

    <!-- ============================================================ -->
    <!-- WS3: Tax Liability vs AUA Divergence                         -->
    <!-- ============================================================ -->
    <requirement id="5">
      WS3 DIAGNOSTIC: Quantify the divergence and isolate root causes.

      Five known methodology gaps between script 06 (tax) and script 05 (AUA):

      (a) Ghost account exclusion: script 06 has NONE. Scripts 02/05 apply
          aua_overrides.json + phantom exclusion. This is the suspected primary
          driver.

      (b) Different base datasets: script 06 reads holdings_lots (FIFO lots,
          script 03). Script 05 reads positions_cube (cumulative units, script 02).
          Different reconstruction methods from the same transactions.

      (c) Different pricing: script 06 uses market_value pre-computed in
          holdings_lots (latest single price). Script 05 uses canonical_prices
          daily series with forward-fill.

      (d) Different date semantics: script 06 = single snapshot from latest
          holdings_lots. Script 05 = daily timeseries (latest date in positions_cube).

      (e) Backfill capping: script 02 caps forward-fill for backfill-only accounts.
          Script 03/06 does not.

      Step 3a: Compute the aggregate divergence:
        - Sum script 06 market_value by tax_status (taxable, tax_deferred, tax_exempt)
        - Sum script 05 AUA by tax_status (aua_taxable, aua_tax_deferred, aua_tax_exempt)
        - Report: total delta, delta by tax_status, delta as % of AUA

      Step 3b: Isolate gap (a) -- ghost accounts:
        - Load aua_overrides.json and the phantom exclusion set from script 02
        - Filter holdings_lots to only excluded accounts
        - Sum their market_value -- this is the ghost account contribution to
          the tax liability that is absent from AUA

      Step 3c: Isolate gap (b+c) -- base dataset + pricing:
        - For accounts that are NOT ghost/phantom (present in both datasets),
          compare lot-level MV (script 06) vs position-level MV (script 05)
        - Report: how much divergence remains after removing ghost accounts?

      Step 3d: Produce a ranked table of the top 20 accounts by absolute
      divergence (|tax_mv - aua_mv|). For each, note the driver: ghost,
      pricing, backfill cap, etc.
    </requirement>

    <requirement id="6">
      WS3 FIX: Apply ghost account exclusion to script 06.

      At minimum, add the same aua_overrides.json exclusion that script 05 uses.
      This should be a direct port of the exclusion logic. If the phantom
      exclusion set from script 02 is also relevant, add that too.

      Document the before/after divergence numbers in your session log.
      These findings feed directly into GLDRST's canonical methodology design.

      Commit changes to CLOUD.
    </requirement>

    <!-- ============================================================ -->
    <!-- Session log                                                  -->
    <!-- ============================================================ -->
    <requirement id="7">
      Write a session log at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-26/
          advi_mvplvl_010_l2_mix_tax_diagnostic.md

      Include:
        - WS1 findings: what S3 artifacts exist, root cause, fix applied
        - WS2 findings: firm_mix_views.json state, mix_timeseries key mismatch
        - WS3 findings: divergence numbers, ranked account table, gap attribution
        - All commit hashes
        - Explicit next steps for AE (gold rerun if needed) and DE (portal fixes if needed)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">WS1: Root cause of L2 advisor composition failure identified and either fixed (script change) or escalated (documented DE/Lambda issue)</criterion>
    <criterion id="2">WS2: firm_mix_views.json inspected, sparseness confirmed or denied, fix applied or full-rebuild flagged</criterion>
    <criterion id="3">WS2: mix_timeseries.json vs mix.json S3 key mismatch documented and fix committed</criterion>
    <criterion id="4">WS3: Aggregate divergence quantified with per-gap attribution</criterion>
    <criterion id="5">WS3: Ghost account exclusion added to script 06, before/after numbers documented</criterion>
    <criterion id="6">Session log written with all findings, commits, and next steps</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify portal code (ClientsTab.tsx, PartnerAnalytics.tsx) -- that is DE scope</constraint>
    <constraint>Do NOT modify the Lambda (lambda_function.py) -- that requires Terraform deploy via AE/DT</constraint>
    <constraint>Do NOT trigger a gold rerun -- flag if one is needed and AE will execute</constraint>
    <constraint>For WS3, the goal is diagnosis + minimal fix (ghost exclusion). The full canonical methodology alignment is GLDRST scope.</constraint>
    <constraint>All S3 reads are diagnostic only -- do NOT write to S3</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="n/a">
      No blocking dependencies. All diagnostic data is on S3 from the 2026-03-25 gold run.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">Session log with WS1/WS2/WS3 diagnostic findings</deliverable>
    <deliverable type="commit">Script 12 fix (if L2 composition issue is script-side)</deliverable>
    <deliverable type="commit">Script 06b fix (mix_timeseries.json key alias)</deliverable>
    <deliverable type="commit">Script 06 fix (ghost account exclusion)</deliverable>
    <deliverable type="document">WS3 divergence numbers feeding into GLDRST canonical methodology</deliverable>
  </deliverables>
</task_order>
