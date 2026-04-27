<task_order>
  <metadata>
    <id>ADVI_INFLEC.TO-F.ae-e2e-bronze-validation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to><!-- If 0.6.1 back online by gate time: may transfer. -->
    <date>2026-04-27</date>
    <status>staged</status><!-- Gates: TO-A + TO-C + TO-D + TO-E + Andrew A2 (credentials populated). -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>TO-F</wave>
    <supersedes>W3.B.4.ae-e2e-bronze-validation.md (Slack ACs removed; web-form + SNS path)</supersedes>
    <gates_on>TO-A RAVC4 + TO-C RAVC4 + TO-D RAVC4 + TO-E RAVC4 + Andrew A2 (orion/credentials populated)</gates_on>
  </metadata>

  <prd_ref>docs/architecture/ADVI_INFLEC_BRONZERUN_V2.md §5 TO-F (cc170c00)</prd_ref>

  <objective>
    Execute the full live Orion bronze run end-to-end: SSM trigger → Playwright login → OTP
    via SNS SMS + web form → CSV export to S3 → silver conversion. Final gate before W6.1
    (nightly EventBridge schedule) can be enabled.
  </objective>

  <scope>
    1. Trigger opal-inf-export-run SSM command on inf-exporter EC2
    2. Monitor CloudWatch state progression: STARTING → (WAITING_FOR_OTP or skip if no 2FA) → EXPORT_COMPLETE
    3. If WAITING_FOR_OTP: Andrew receives SNS SMS with Function URL → opens URL on phone → submits OTP
    4. Confirm export complete, at least 3 CSVs in s3://opal-data-inf/bronze/orion/{date}/
    5. Trigger convert_orion_to_silver.py (manual or S3 event notification)
    6. Confirm silver parquet in s3://opal-data-inf/silver/transactions/
    7. Update infra/aws/ec2/EC2_MANIFEST.json:
       - inf-exporter.source_path = infra/aws/ec2/inf-exporter/src/stepwise/
       - inf-exporter.deployed_commit = {latest deploy commit hash}
    8. Commit EC2_MANIFEST.json update
    9. Tag inf-pipeline-v{next} (check existing tags: git tag -l "inf-pipeline-v*" | sort -V | tail -5)
    10. Push --follow-tags
    11. RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with full artifact evidence
  </scope>

  <acceptance_criteria>
    1. Export run completes (exit 0). CW logs show STARTING → WAITING_FOR_OTP (or skip) → EXPORT_COMPLETE.
    2. At least 3 CSV files in s3://opal-data-inf/bronze/orion/{date}/.
    3. Andrew received SNS SMS with Lambda Function URL when OTP triggered.
    4. Andrew successfully submitted OTP via mobile web form (CW log shows: "OTP received").
    5. Silver parquet exists for export date in s3://opal-data-inf/silver/transactions/.
    6. otp/current.txt does NOT exist post-run (cleanup confirmed).
    7. EC2_MANIFEST.json inf-exporter.deployed_commit populated and committed.
    8. Tag inf-pipeline-v{next} pushed.
    9. RAVC4 to COO + CTO with: CW log trace, S3 artifact list (bronze + silver), EC2_MANIFEST commit, tag.
  </acceptance_criteria>

  <andrew_required>
    - A2: orion/credentials must be populated in Secrets Manager before this TO can execute.
    - Andrew must be available to respond to SNS OTP SMS during the test run.
  </andrew_required>

  <do_not>
    <rule>Do NOT declare pass without silver parquet confirmed (AC5).</rule>
    <rule>Do NOT enable W6.1 (EventBridge schedule) before RAVC4 on this TO is accepted.</rule>
    <rule>Do NOT assume otp/current.txt cleanup — verify explicitly (AC6).</rule>
  </do_not>
</task_order>
