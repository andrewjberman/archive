<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-auagap-002-rps-reupload</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL (step 1) + 0.4.0_DS_ClientPlatform (steps 2-5)</issued_to>
    <date>2026-04-22</date>
    <status>active</status>
    <project_code>ADVI_STAUDT</project_code>
    <urgency>URGENT — portal chart blocked. Andrew watching. 1.0.0_SA_CTO fix plan accepted (20260422T123619Z).</urgency>
    <cto_directive>1.0.0_SA_CTO reconciliation: DS~D ANON_* root cause + DS base BFIX1 amplifier — both confirmed. TO1 = immediate unblock.</cto_directive>
  </metadata>

  <objective>
    Replace anonymized Schwab RPS silver partitions (2025-01-02 through end of affected
    window) with correct real-account-ID data. Rerun B_00 + full cascade over that
    window. Verify 49F portal AUA chart shows ~$1.4B for Q1-Q3 2025.
  </objective>

  <root_cause>
    Schwab RPS S3 partitions from 2025-01-02 through approximately 2025-10-31 contain
    anonymized test data (ANON_<hash> account IDs). prepare_schwab_partition() maps
    only 1 of ~3,931 RPS rows per date. schwab_persistent_accts (built from 2026
    universe, ~5,450 accounts) classifies 5,449 accounts as bd_stale → units=0 →
    dropped at units>0 filter. Result: ~3,538 accounts and ~$1.1B AUA missing per date.
    BFIX1 global-latest persistent set amplifies the impact (AUAGAP.003 addresses this
    separately as a structural prevention fix — not required for this TO).
  </root_cause>

  <steps>
    <step id="1" owner="0.6.0_AE_PartnerETL">
      Identify the exact affected date range: first date with ANON_* IDs (known:
      2025-01-02) through the last affected date. Upload correct real-account-ID Schwab
      RPS parquets to:
        s3://opal-data-bd/schwab/silver/rps/date=YYYYMMDD/data.parquet
      for each affected date. Andrew supplies the source Schwab export files.
      When complete: MCP COO + DS with confirmed date range and file count.
    </step>
    <step id="2" owner="0.4.0_DS_ClientPlatform">
      Spot-check AE upload: read 3 dates (2025-02-15, 2025-05-15, 2025-08-15) from
      S3. Verify account_id column contains real 10-digit numeric IDs (not ANON_*).
      Report pass/fail to COO before proceeding to step 3.
    </step>
    <step id="3" owner="0.4.0_DS_ClientPlatform">
      Pre-flag to CTO + COO (formality — scope already authorized). Then rerun:
        B_00.canonical_holdings.py --start-date 2025-01-02 --end-date [AE_confirmed_end] --upload --force
      Monitor for any new anomalies. Do NOT run gold pipeline scripts beyond B_00 in
      this step — cascade is step 4.
    </step>
    <step id="4" owner="0.4.0_DS_ClientPlatform">
      Cascade C-chain and D-chain over affected window:
        C_03 account_performance --start-date 2025-01-02 --upload
        D_00b portal_timeseries --upload (or trigger via gold_dispatch --group D)
      Note: gold_dispatch gate hotfix (f201c75d) is now live — full D-chain will run.
    </step>
    <step id="5" owner="0.4.0_DS_ClientPlatform">
      Verify portal chart: 49F /advisor-intelligence quarterly AUA view shows ~$1.4B
      for Q1-Q3 2025 bars (no more ~$300M dip). Screenshot or MCP COO with confirmed
      values. Run comp-validate as applicable.
    </step>
  </steps>

  <acceptance_criteria>
    1. AE uploads confirmed: date range documented, account_ids are real numerics.
    2. DS spot-check step 2 PASS on all 3 dates.
    3. B_00 rerun completes cleanly over affected window.
    4. C_03 + D-chain cascade completes.
    5. Portal AUA chart Q1-Q3 2025 shows ~$1.4B (within 5% of Q4 2024 baseline).
    6. MCP COO + CTO on completion with before/after values.
  </acceptance_criteria>

  <sequencing>
    AE step 1 → DS step 2 (verify) → DS pre-flag → DS step 3 (B_00) → DS step 4
    (cascade) → DS step 5 (portal check). No parallelism within steps — each gates
    the next. AUAGAP.003 (BFIX1 structural fix) can run in parallel with steps 3-5 or
    immediately after.
  </sequencing>

  <do_not>
    <rule>Do NOT run B_00 before AE step 1 is confirmed complete and DS step 2 passes.</rule>
    <rule>Do NOT skip the pre-flag in step 3 — it is a required formality per policy.</rule>
    <rule>Do NOT implement BFIX1 temporal-scope fix in this TO — that is AUAGAP.003.</rule>
    <rule>Do NOT run gold pipeline scripts beyond the specified scope (B_00 + C_03 + D-chain).</rule>
  </do_not>
</task_order>
