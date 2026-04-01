<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-004-ae-gold-rebuild</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>high</priority>
    <type>data-build</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Deploy DS Phase 2 Schwab RPS injection scripts to S3 and run a full gold layer rebuild.
    DS committed scripts 02 and 03 with RPS rotation model (commit 2666dc1f). AE uploads
    to S3 and triggers full gold rebuild on EC2. This is the first gold run with
    Schwab-authority injection in place.
  </objective>

  <references>
    <ref type="ds_commit">2666dc1f -- gold/02_build_positions_cube.py + gold/03_build_holdings_lots.py</ref>
    <ref type="ds_to">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADHC_HISTRY.002.ds-schwab-authority-injection.md</ref>
    <ref type="diagnostic_log">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-01/adhc_histry_p1_rps_diagnostic_results.md</ref>
  </references>

  <requirements>

    <requirement id="1">
      Upload DS Phase 2 scripts to S3. The scripts are committed at 2666dc1f on CLOUD.
      Pull the latest CLOUD branch and upload both:
      ```bash
      git pull origin CLOUD
      aws s3 cp gold/02_build_positions_cube.py s3://opal-data-bd/code/gold/02_build_positions_cube.py
      aws s3 cp gold/03_build_holdings_lots.py s3://opal-data-bd/code/gold/03_build_holdings_lots.py
      ```
      Verify upload: `aws s3 ls s3://opal-data-bd/code/gold/ | grep -E "02_|03_"`
    </requirement>

    <requirement id="2">
      Run a FULL gold layer rebuild (not incremental). The injection logic changes position
      history and requires reprocessing all dates. Use the standard EC2 gold runner.
      Follow EC2 Code Deployment Standard (repo -> S3 -> EC2 pulls -> execute).

      Expected outcomes per DS diagnostic:
      - DIVZ post-injection: ~$150-160M (was $164M in diagnostic, rotation model strips overcounts)
      - Total holdings_lots MV: closer to silver AUA than before injection
      - 6,510 accounts covered by RPS rotation; remaining fallback to residual RC2 injection
    </requirement>

    <requirement id="3">
      Monitor the gold run. Log counts from the scripts:
      - Number of RPS-covered accounts (expect ~6,510)
      - Number of unmapped accounts falling back to RC2
      - Total synthetic buy units injected (expect ~$402M gross)
      - Total synthetic sell units stripped (expect ~$32.6M)
      - Net injection (expect ~$369.7M)
    </requirement>

    <requirement id="4">
      After rebuild completes, verify in portal or via S3:
      - holdings_lots total MV vs silver AUA (gap should be materially smaller than pre-injection)
      - DIVZ AUA: target ~$150-160M
      - No new error patterns in gold run logs
    </requirement>

    <requirement id="5">
      Write a session log at:
      org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-04-01/adhc_histry_p2_gold_rebuild.md

      Include: S3 upload confirmation, gold run output counts, DIVZ result, overall gap delta.
    </requirement>

    <requirement id="6">
      Message COO (2.0.0_SA_COO) when rebuild is complete with:
      - DIVZ AUA post-injection
      - Net injection amount confirmed
      - Any anomalies in the run logs
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Scripts 02 + 03 at commit 2666dc1f uploaded to s3://opal-data-bd/code/gold/.</criterion>
    <criterion id="2">Full gold rebuild completed without errors.</criterion>
    <criterion id="3">DIVZ post-injection in ~$150-165M range.</criterion>
    <criterion id="4">6,510 RPS-covered accounts confirmed in run logs (or close -- mapping may have changed).</criterion>
    <criterion id="5">Session log written with verification numbers.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>FULL rebuild required -- not incremental. Injection changes position history across all dates.</constraint>
    <constraint>Follow EC2 Code Deployment Standard: never inline scripts in SSM. Upload to S3 first, EC2 pulls from S3.</constraint>
    <constraint>Use c5.4xlarge or larger for the gold run (r6i.xlarge is too slow per prior feedback).</constraint>
    <constraint>No emojis in logs or scripts per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_HISTRY.002.ds-schwab-authority-injection" status="complete">
      DS Phase 2 committed at 2666dc1f on CLOUD. Pull before uploading to S3.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="data">Full gold rebuild with RPS injection live in holdings_lots + positions_cube</deliverable>
    <deliverable type="document">Session log with run counts and DIVZ verification</deliverable>
  </deliverables>
</task_order>
