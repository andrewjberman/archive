<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-17-advtv2-002-dt-gold-deploy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <project_code>ADVI_ADVTV2</project_code>
  </metadata>

  <objective>
    Deploy the architect attribution gold layer scripts to EC2 (bd-gold-layer-runner),
    run a FULL gold layer rebuild, and verify that rel_architect_lookup.parquet contains
    exactly 19 named architects + Unresolved. This propagates architect attribution
    downstream into 08, 09, 10 and ultimately into portal JSON for all ADV views.
  </objective>

  <context>
    DS 001 is complete (2026-03-17, pending DS commit). DS modified four gold scripts:
    - NEW: data/black_diamond/scripts/gold/08b_build_architect_attribution.py
    - MOD: data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py
    - MOD: data/black_diamond/scripts/gold/00_build_accounts_dimension.py
    - MOD: data/black_diamond/scripts/gold/run_gold_layer.sh

    Deploy brief is at: docs/briefs/devops-brief-architect-attribution.md (read it first).

    FULL mode is required for the first run because 00_build_accounts_dimension.py
    now reads consultant and additional_advisor from silver transactions — incremental
    mode will not backfill these into existing accounts_dimension rows.
  </context>

  <scope>
    <files>
      <file action="none">data/black_diamond/scripts/gold/08b_build_architect_attribution.py (upload to S3)</file>
      <file action="none">data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py (upload to S3)</file>
      <file action="none">data/black_diamond/scripts/gold/00_build_accounts_dimension.py (upload to S3)</file>
      <file action="none">data/black_diamond/scripts/gold/run_gold_layer.sh (upload to S3)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Verify DS commit to CLOUD is complete (check git log for 08b, 08, 00, run_gold_layer.sh).
      Do not deploy uncommitted code.
    </requirement>

    <requirement id="2">
      Upload all 4 modified scripts to S3 per the devops brief:
        s3://opal-data-bd/code/gold/08b_build_architect_attribution.py
        s3://opal-data-bd/code/gold/08_build_nna_aua_by_advisor.py
        s3://opal-data-bd/code/gold/00_build_accounts_dimension.py
        s3://opal-data-bd/code/gold/run_gold_layer.sh
      Use the standard EC2 code deployment pattern (repo -> S3 -> EC2 pulls).
      Follow EC2_CODE_DEPLOYMENT_STANDARD.md.
    </requirement>

    <requirement id="3">
      On bd-gold-layer-runner EC2, pull the updated scripts from S3.
      Run the gold layer in FULL mode (not incremental):
        ./run_gold_layer.sh --full
      FULL mode is required because 00_build_accounts_dimension.py now ingests
      consultant and additional_advisor from silver transactions for the first time.
    </requirement>

    <requirement id="4">
      Verify rel_architect_lookup.parquet on S3:
        aws s3 cp s3://opal-data-bd/gold/views/rel_architect_lookup.parquet /tmp/
        python3 -c "import pandas as pd; df=pd.read_parquet('/tmp/rel_architect_lookup.parquet'); print(df['resolved_architect'].nunique(), 'architects'); print(df['resolved_architect'].unique())"

      Expected: exactly 19 distinct named architects plus "Unresolved". No "49F House",
      no "Unassigned", no stale/retired architects.
    </requirement>

    <requirement id="5">
      Verify architect_attribution.parquet on S3:
        Check that conservation holds: resolved + unresolved rows = total funded accounts.
        (DS printed this during dry-run — confirm counts match or are close to 5,423 funded accounts
        with ~98.3% resolved.)
    </requirement>

    <requirement id="6">
      After FULL gold run completes, verify downstream scripts 09 and 10 ran without errors
      (they are part of run_gold_layer.sh --full). Spot-check that portal JSON files updated:
        aws s3 ls s3://opal-data-bd/gold/portal/ --recursive | sort -k1,2 | tail -10
      Confirm at least one portal JSON has a recent modified timestamp.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 4 scripts uploaded to S3 and pulled onto EC2</criterion>
    <criterion id="2">FULL gold layer run completes without errors</criterion>
    <criterion id="3">rel_architect_lookup.parquet contains exactly 19 named architects + Unresolved</criterion>
    <criterion id="4">No "49F House", "Unassigned", or stale architects in rel_architect_lookup</criterion>
    <criterion id="5">Downstream scripts 09 and 10 run successfully (no code changes required)</criterion>
    <criterion id="6">Portal JSON files updated with recent timestamp</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>FULL mode required for first run — do NOT use incremental mode</constraint>
    <constraint>Do NOT modify any scripts on EC2 directly — pull from S3 only</constraint>
    <constraint>EC2 code deployment follows EC2_CODE_DEPLOYMENT_STANDARD.md (repo -> S3 -> EC2 pulls)</constraint>
    <constraint>Wait for DS commit to CLOUD before uploading to S3 (req 1 is a gate)</constraint>
    <constraint>No emojis in any SSM commands or scripts (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ADVTV2.001.gold-architect-attribution" status="complete">
      All 4 scripts modified and data_contract.xml updated. Pending DS commit to CLOUD.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">4 gold scripts deployed to bd-gold-layer-runner via S3</deliverable>
    <deliverable type="verify">FULL gold layer run complete, rel_architect_lookup verified</deliverable>
    <deliverable type="document">Session log documenting verification output</deliverable>
  </deliverables>
</task_order>
