<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-12-05d-date-fix-redeploy</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-12</date>
    <status>pending</status>
  </metadata>

  <objective>
    Deploy the fixed 05d_write_aua_certification.py to EC2 via safe-ec2-deploy.sh.
    Two bugs were found and fixed locally by CTO:
    (1) 05d used datetime.date.today() instead of the data date from client_performance,
        causing it to SKIP every nightly run (silver files are named T-1, not T).
    (2) LIABILITY_TYPES over-excluded Insurance/TermLife/Annuity from certified_aua.
        Both gold and silver include these accounts; excluding them would undercount by ~$60M.
    The fixes are already committed locally. This task order covers commit, deploy, and verify.
  </objective>

  <scope>
    <files>
      <file action="deploy">data/black_diamond/scripts/gold/05d_write_aua_certification.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Commit the 05d fix (already edited locally by CTO) on CLOUD branch.
    </requirement>
    <requirement id="2">
      Deploy to EC2 via safe-ec2-deploy.sh bd-gold-layer-runner. Verify 05d is
      in s3://opal-data-bd/code/gold/ with the updated content.
    </requirement>
    <requirement id="3">
      Verify the fix will work on next nightly run: the data_date derivation
      (max date in client_performance) must match an existing silver allocation file.
      Run a quick S3 check to confirm alignment.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">05d deployed to S3 with data_date fix (no more datetime.date.today())</criterion>
    <criterion id="2">EC2_MANIFEST.json updated with deploy record</criterion>
    <criterion id="3">S3 verification confirms data_date matches available silver allocation</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Use safe-ec2-deploy.sh -- never deploy directly</constraint>
    <constraint>Do not modify any other gold script in this deploy</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">05d fix committed on CLOUD</deliverable>
    <deliverable type="commit">EC2_MANIFEST.json deploy record</deliverable>
  </deliverables>
</task_order>
