<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRD.006</id>
    <project>ADVI_INFGRD</project>
    <title>INF_D_04 AUA column fix — firm_managed_aum → managed_value.sum()</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRD.md</ref>
    <ref type="investigation_log">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-04-29/infgrd003_gold_chain_aua_investigation.md</ref>
    <ref type="target_script">data/orion/scripts/gold/INF_D_04.client_portal_summary.py</ref>
    <ref type="silver_artifact">s3://opal-data-inf/silver/aum_snapshot/2026-04-21.parquet (stale)</ref>
  </references>

  <context>
    INFGRD.003 chain ran on 2026-04-29 (c8756c41, c6a.4xlarge). Chain completed C_02 through D_07
    (skipping D_03 for IAM issue). platinum/firm/header_metrics.json now shows total_aua = $89.6M.
    Andrew's actual Inflection AUA per Orion as of 2026-04-29: $182.71M.

    Root cause (documented by AE 0.6.1 in investigation log):
    INF_D_04.client_portal_summary.py build_dashboard() has a column name mismatch:
      CURRENT (wrong): 'firm_managed_aum' — this column does NOT exist in silver/aum_snapshot/*.parquet
      ACTUAL column: 'managed_value' (per-household managed AUM value)
      CORRECT sum: managed_value.sum() across all rows for Inflection rep_ids = firm AUM

    Because the override branch never fires, total_aua falls back to
    holdings['market_value'].sum() = $89.6M (gross holdings sum, not managed AUM).

    aum_snapshot state:
    - Only file: silver/aum_snapshot/2026-04-21.parquet — 8 days stale
    - Columns: snapshot_date, household_id, household_name, rep_id, rep_name, advisor_key,
      rep_bucket, managed_value, unmanaged_value, source_file, advisor_firm
    - managed_value.sum() as of 2026-04-21 = $200,070,081 (not $182.71M — stale by 8 days)
    - Source: "Homepage Quick AUM Report - Rep_AlongsideL.csv" from Orion
    - Rep IDs present: [3, 11, 12] (correct Inflection rep_ids)

    Two fixes required:
    1. INF_D_04 code fix (this TO)
    2. Fresh aum_snapshot pull for 2026-04-29 date (this TO if bronze script locatable,
       or COO will route separately)

    Once D_04 is fixed and aum_snapshot is fresh, AE 0.6.1 re-runs D_04 + INF_09 to
    republish platinum. COO will relay GO to AE 0.6.1 after DS RAVC.

    Andrew directive: "there should be no 'close' or margin of error, we should be getting
    the exact number from orion." The fix must produce platinum/firm/header_metrics.json
    with total_aua = managed_value.sum() from the freshest aum_snapshot partition.
  </context>

  <scope>
    Task A — INF_D_04 code fix (required):
    In data/orion/scripts/gold/INF_D_04.client_portal_summary.py, build_dashboard() function:

    FIND (approximate lines based on investigation):
    ```python
    if not aum_snapshot.empty and 'firm_managed_aum' in aum_snapshot.columns:
        aum_val = aum_snapshot['firm_managed_aum'].iloc[0]
        if aum_val:
            total_aua = float(aum_val)
    ```

    REPLACE WITH:
    ```python
    if not aum_snapshot.empty and 'managed_value' in aum_snapshot.columns:
        aum_val = float(aum_snapshot['managed_value'].sum())
        if aum_val:
            total_aua = aum_val
    ```

    Rationale: aum_snapshot has one row per household, so the firm-level AUM is the sum
    of all household managed_value entries. The original code used .iloc[0] on a wrong
    column name — both bugs corrected here.

    Task B — Fresh aum_snapshot pull (required if bronze script locatable):
    Find the bronze/silver script that generates silver/aum_snapshot/ from Orion.
    Check:
    1. data/orion/scripts/bronze/ — look for any script referencing "aum_snapshot",
       "Quick AUM", "aum", "Rep_AlongsideL"
    2. data/orion/scripts/silver/ — look for convert scripts reading aum-related files
    3. data/orion/manual_api/ — any existing pull scripts

    If found: run the script for 2026-04-29 to produce silver/aum_snapshot/2026-04-29.parquet.
    Verify: managed_value.sum() ≈ $182.71M (within rounding margin).

    If NOT found: document the search in session log + RAVC. COO will route separately
    (likely manual pull from Orion via ORIAPI bronze runner or a new script).

    Task C — Pre-commit gate (mandatory per CLAUDE.md rule 14):
    Run .tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py
    All three checks (py_compile + AST + ruff) must exit 0 before commit.

    Task D — S3 upload (required):
    After pre-commit gate passes:
    aws s3 cp data/orion/scripts/gold/INF_D_04.client_portal_summary.py \
      s3://opal-data-inf/code/gold/INF_D_04.client_portal_summary.py

    Verify: comp-pipescript deployed INF_D_04 shows MATCH.

    If aum_snapshot updated: also upload the new silver parquet to S3.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_D_04</run>
        <expect>READS includes silver/aum_snapshot. WRITES includes platinum/firm/header_metrics.json.
        No new COLUMN GAPS introduced by this fix (we are fixing a column name, not adding new reads).</expect>
        <if_mismatch>STOP if new COLUMN GAPS appear. Document all PORTAL CONSUMERS in session log.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed INF_D_04</run>
        <expect>STALE (since we haven't uploaded yet — confirming baseline). Note the current deployed hash.</expect>
        <if_mismatch>If MATCH: confirm current S3 version is the pre-fix version. Proceed anyway — we're about to fix it.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py</run>
        <expect>Exit 0. All three checks pass: py_compile OK, AST undefined-name scan CLEAN, ruff CLEAN.</expect>
        <if_mismatch>STOP. Fix all gate failures before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit and after S3 upload">
      <step>
        <run>comp-pipescript deployed INF_D_04</run>
        <expect>MATCH — deployed script hash matches committed version.</expect>
        <if_mismatch>STOP. S3 upload failed or wrong version uploaded. Re-run aws s3 cp.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      INF_D_04.client_portal_summary.py build_dashboard() reads 'managed_value' column
      and sums all rows (managed_value.sum()). The 'firm_managed_aum' reference is gone.
      Evidence: diff in session log.
    </criterion>
    <criterion id="2">
      .tools/ds-commit-gate.sh exits 0 on the patched file. Evidence: gate output in
      session log.
    </criterion>
    <criterion id="3">
      Script committed with .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A" -m
      "fix(ADVI_INFGRD.006): INF_D_04 managed_value column fix — AUA override branch now fires"
      Evidence: commit hash in RAVC.
    </criterion>
    <criterion id="4">
      aws s3 cp uploaded to s3://opal-data-inf/code/gold/INF_D_04.client_portal_summary.py.
      comp-pipescript deployed INF_D_04 shows MATCH. Evidence: both in session log.
    </criterion>
    <criterion id="5">
      aum_snapshot Task B outcome documented: either (a) fresh 2026-04-29 parquet uploaded
      to s3://opal-data-inf/silver/aum_snapshot/ with managed_value.sum() ≈ $182.71M,
      OR (b) script not found + search log provided so COO can route separately.
    </criterion>
    <criterion id="6">
      RAVC to COO after S3 upload confirmed. Include: commit hash, s3 cp confirmation,
      aum_snapshot outcome (fresh parquet or not-found), and explicit signal that AE
      0.6.1 is cleared for D_04 + D_09 re-run.
      Do NOT signal AE 0.6.1 directly — COO relays the GO.
    </criterion>
    <criterion id="7">
      Session log includes Compiler Tools section reproducing all three phase mandates
      with observed output and pass/fail vs expect.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL" task="ADVI_INFGRD.003" status="complete-with-flags">
      Chain ran but platinum AUA wrong. This TO fixes the root cause.
      DS RAVC completion → COO relays GO to AE 0.6.1 for D_04 re-run.
    </dependency>
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      After DS RAVC: COO sends GO to AE 0.6.1 for EC2 re-run of D_04 + INF_09.
      DS must NOT trigger the chain directly. COO owns sequencing.
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh \
      --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "fix(ADVI_INFGRD.006): INF_D_04 managed_value column fix — AUA override branch now fires" \
      -- data/orion/scripts/gold/INF_D_04.client_portal_summary.py
  </commit_identity>

  <notes>
    D_03 IAM issue (dynamodb:Scan on bd-securities) is a SEPARATE issue tracked in AE scope.
    Not in this TO's scope. D_03 was skipped in the chain and will remain skipped until
    AE 0.7.0 addresses the IAM Terraform fix.

    aum_snapshot staleness: if 2026-04-29 parquet not achievable today, the fix still
    improves AUA accuracy (from $89.6M holdings-based to $200M+ managed-value-based from
    the 2026-04-21 snapshot). But $182.71M exact requires a fresh pull.
    Andrew's directive requires exact. If bronze script not found, document clearly in RAVC.
  </notes>
</task_order>
