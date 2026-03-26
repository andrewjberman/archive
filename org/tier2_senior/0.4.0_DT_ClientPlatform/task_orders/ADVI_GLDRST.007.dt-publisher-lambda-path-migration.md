<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-007-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>blocked</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Update the 3 Lambda handlers (opal-partners-data, bd-portal-publisher,
    bd-portal-advisor-publisher) to read from the new GLDRST S3 key layout.
    Also apply the TX snapshot date anchor fix specified by DS in .005.

    This is the Lambda-side of the copy-then-switch migration. Scripts
    (.004 Phase A) must have already dual-written to new paths before
    this TO begins.
  </objective>

  <context>
    After .004 Phase A completes, both old and new S3 keys exist.
    This TO switches Lambda reads from old to new paths.

    Three Lambdas need updates:
    1. opal-partners-data (infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/)
       - Reads: ~15 gold keys (parquets + JSONs)
    2. bd-portal-publisher (infra/aws/lambda/bd-pipeline/bd-portal-publisher/)
       - Reads: 8 gold parquets
       - Writes: ~10 portal-ready JSONs
    3. bd-portal-advisor-publisher (infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/)
       - Reads: 4 gold parquets
       - Writes: per-advisor book.json, timeseries.json, client detail JSONs

    TX date anchor fix (from DS .005 specification):
    - bd-portal-publisher line 1794: change to US-only max date for snapshot view
  </context>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Update all S3 key references in all 3 Lambda handlers to the new
      GLDRST layout (as defined in lib/s3_layout.py from .004).

      Lambda code cannot import lib/s3_layout.py directly (Lambdas are
      packaged separately). Instead, create a LAMBDA_S3_KEYS dict at the
      top of each Lambda file that mirrors the lib/s3_layout.py constants.
    </requirement>

    <requirement id="2">
      Apply TX snapshot date anchor fix to bd-portal-publisher:
      Use US-only max date for both snapshot and continuous views
      (per DS .005 specification).
    </requirement>

    <requirement id="3">
      Update publisher WRITE paths: portal-ready JSON artifacts should
      be written to gold/artifacts/ and gold/entities/ (new layout),
      with dual-write to old paths for CloudFront backward compat.
    </requirement>

    <requirement id="4">
      Requires Terraform deploy. Update lambda-source-map.json.
      Follow LAMBDA_DEPLOYMENT_PROTOCOL.md.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 3 Lambdas read from new GLDRST S3 key paths</criterion>
    <criterion id="2">TX snapshot date anchor uses US-only max date</criterion>
    <criterion id="3">Publisher dual-writes to old + new artifact paths</criterion>
    <criterion id="4">Terraform plan shows 0-diff after apply</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Requires .004 Phase A (dual-write) to be complete and verified</constraint>
    <constraint>Must follow LAMBDA_DEPLOYMENT_PROTOCOL.md (commit -> plan -> apply -> tag)</constraint>
    <constraint>Dual-write old paths until CloudFront behaviors are updated (.008)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.004" status="pending">
      Phase A (dual-write) must be complete so new S3 keys exist
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.005" status="pending">
      TX date anchor fix specification needed
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_GLDRST.009" status="pending">
      Gold rerun with .004 Phase A to populate new keys
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Lambda S3 path updates + TX date anchor fix</deliverable>
    <deliverable type="deploy">partners-api Terraform deploy</deliverable>
    <deliverable type="deploy">bd-pipeline Terraform deploy</deliverable>
  </deliverables>
</task_order>
