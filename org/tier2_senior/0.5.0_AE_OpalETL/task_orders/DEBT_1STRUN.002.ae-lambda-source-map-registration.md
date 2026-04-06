<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-debt-1strun-002-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>DEBT_1STRUN</project_code>
    <priority>high</priority>
  </metadata>

  <objective>
    Register all 26 unmapped Lambda functions in lambda-source-map.json.
    This is the highest-leverage fix -- CI drift detection, parity checks,
    and build tooling depend on this file. Without it, 23% of Lambdas are
    invisible to the deployment system.
  </objective>

  <scope>
    <files>
      <file action="edit">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="source-map">
      **Register 26 unmapped Lambdas in source map**

      The 0.7.0_AE_CloudOps DEBT_1STRUN.001 audit identified 31 unmapped functions.
      5 Lambda@Edge functions were registered by AUTH_TFIMPT (portal-auth-v1.8.0).
      The remaining 26 need source map entries.

      For each function, determine:
      1. **Source path** -- where the code lives in the repo (scan infra/aws/lambda/)
      2. **Pipeline** -- which TF pipeline manages it (or "unmapped" if none)
      3. **Runtime** -- python3.11, python3.12, nodejs20.x

      Categories from the audit:
      - Trade subsystem (10): trade-auth-handler, trade-authorizer, trade-dashboard-api,
        trade-identifier-cache, trade-parquet-batch-export, trade-recon-api, trade-recon-auth,
        trade-recon-authorizer, trade-recon-processor, trade-submission-handler,
        trade-workflow-handler
      - Security/infra monitoring (4): access-anomaly-scanner, cost-anomaly-scanner,
        ec2-auto-shutdown-enforcer, ec2-runtime-monitor
      - Market overview (3): market-update-data-aggregator, market-update-exporter,
        market-update-generator
      - Other (6): bd-allocation-file-checker, opal-bd-transaction-consolidator,
        deck-generation, infrastructure-daily-snapshot, opal-session-analytics,
        opal-cloudfront-market-generator
      - Delete candidates (2): test-yfinance-simple, yfinance-aapl-test
        (do NOT register -- flag for deletion)

      For functions without repo source, set source_path to "EXTERNAL" and add a
      comment. These need code to be pulled from AWS before they can be managed.
    </deliverable>
  </deliverables>

  <tooling>
    1. **crossref_graph** -- Run on infra/aws/lambda/ to find source dirs for unmapped functions.
    2. **coverage_auditor** -- Source = AWS Lambda list, Registry = source-map entries.
       Confirms the gap matches the audit and catches any new functions deployed since.
  </tooling>

  <references>
    <ref type="audit">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DEBT_1STRUN.001_infrastructure_audit.md</ref>
    <ref type="source_map">infra/aws/lambda/ci/lambda-source-map.json</ref>
  </references>

  <dependencies>
    None. Can begin immediately on GO.
  </dependencies>
</task_order>
