<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-debt-1strun-001-0.5.0_ae_opaletl</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Scan ALL AWS resources in your pipeline scope for technical debt
    across 6 categories: Lambda code, Terraform modules, EC2 services,
    S3 buckets/prefixes, and DynamoDB tables. Produce a structured
    findings log. Report to 0.7.0_AE_CloudOps.
  </objective>

  <scope>
    <files>
      <!-- Lambda code -->
      <file action="scan">infra/aws/lambda/yang-pipeline/</file>
      <file action="scan">infra/aws/lambda/news-pipeline/</file>
      <file action="scan">infra/aws/lambda/market-overview/</file>
      <!-- Terraform modules -->
      <file action="scan">infra/aws/terraform/yang-pipeline/</file>
      <file action="scan">infra/aws/terraform/news-pipeline/</file>
      <file action="scan">infra/aws/terraform/market-overview/</file>
      <!-- EC2 services (check EC2_MANIFEST.json for services in your scope) -->
      <file action="scan">infra/aws/ec2/ (smartx-exporter, seeking-alpha-scraper, moltbot)</file>
      <!-- S3 buckets: enumerate all S3 prefixes your pipelines write to or read from -->
      <file action="audit">S3 buckets: opal-data-yang, opal-data-news, opal-market-overview (and any others)</file>
      <!-- DynamoDB: enumerate all tables your pipelines use -->
      <file action="audit">DynamoDB tables used by yang/news/market-overview Lambdas</file>
    </files>
    <aws_resource_audit>
      For S3 and DynamoDB, run CLI commands to enumerate:
        aws s3 ls (list all buckets, identify which belong to your pipelines)
        aws dynamodb list-tables (identify which your Lambdas reference)
      Cross-reference against Terraform state and Lambda environment variables.
      Flag any resource that exists in AWS but has no corresponding Terraform
      definition (shadow resource) or any Terraform resource that references
      something that no longer exists (orphaned reference).
    </aws_resource_audit>
  </scope>

  <requirements>
    <requirement id="1">
      Scan all files in your scope for the following 6 categories of technical
      debt. For each finding, record: file path, line number(s), category,
      severity (high/medium/low), and a 1-2 sentence description.

      CATEGORIES:

      C1 - DEAD CODE
      Unreachable functions, unused imports, commented-out blocks, variables
      assigned but never read, functions defined but never called, scripts
      that exist but are never executed by any orchestrator or cron.

      C2 - DEPRECATED / SUPERSEDED
      Code that still runs but has been replaced by a newer pattern elsewhere.
      Old classification logic replaced by ETFClassifier. Static dicts that
      should be DynamoDB lookups. Legacy S3 key patterns that have been
      restructured. Stale TODO/FIXME/HACK comments.

      C3 - DUPLICATION / DRIFT RISK
      Same logic implemented in multiple scripts (e.g., S3 read pattern,
      parquet loading, date range calculation). Copy-pasted utility functions.
      Two scripts that classify securities differently. Helper functions that
      exist in multiple gold scripts instead of a shared lib/.

      C4 - HARDCODED CONFIGURATION
      Magic numbers (worker counts, batch sizes, timeouts). Hardcoded S3
      bucket names or key prefixes. Hardcoded region strings. Inline AWS
      account IDs. Configuration that should be environment variables or
      shared constants.

      C5 - ORPHANED INFRASTRUCTURE
      Scripts listed in run_gold_layer.sh that produce output no consumer
      reads. S3 keys written but never read by any Lambda or downstream
      script. DynamoDB tables or S3 prefixes that are no longer referenced.
      Lambda environment variables pointing to resources that no longer exist.

      C6 - STALE ERROR HANDLING
      try/except blocks that swallow exceptions silently (bare except: pass).
      Error messages referencing old variable names or bucket paths. Missing
      error handling on S3 reads, DynamoDB scans, or external API calls.
      Logging that prints to stdout without structured format. Retry logic
      with no backoff or wrong conditions.
    </requirement>

    <requirement id="2">
      OUTPUT FORMAT: Write your findings as a session log at:
        org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-03-23/debt_1strun_scan.md

      Use this structure:
        # DEBT_1STRUN Scan — 0.5.0_AE_OpalETL
        **Date:** 2026-03-23
        **Scope:** infra/aws/lambda/yang-pipeline/, infra/aws/lambda/news-pipeline/, infra/aws/lambda/market-overview/, infra/aws/terraform/yang-pipeline/, infra/aws/terraform/news-pipeline/, infra/aws/terraform/market-overview/

        ## Findings

        | # | File | Lines | Category | Severity | Description |
        |---|------|-------|----------|----------|-------------|
        | 1 | path/to/file.py | 45-67 | C1 Dead | High | ... |

        ## Summary
        - Total findings: N
        - By category: C1: N, C2: N, C3: N, C4: N, C5: N, C6: N
        - High severity: N
        - Recommended priority fixes: [top 3 items by impact]

      If you find ZERO debt in a category, state "None found" — do not skip it.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 6 categories scanned — none skipped</criterion>
    <criterion id="2">Every finding has file path, line numbers, category, severity, and description</criterion>
    <criterion id="3">Findings log written to logs/2026-03-23/debt_1strun_scan.md</criterion>
    <criterion id="4">Summary section with counts and top 3 priority recommendations</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scan only YOUR pipeline scope — do not scan other pipelines (other DS/AE agents handle those)</constraint>
    <constraint>Do not fix anything — this is a scan-only task. Fixes come in .002+ task orders.</constraint>
    <constraint>Report to 0.7.0_AE_CloudOps — they will aggregate your findings.</constraint>
    <constraint>Be concrete: name files, line numbers, function names. No vague "could be improved" findings.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">logs/2026-03-23/debt_1strun_scan.md with structured findings table</deliverable>
  </deliverables>
</task_order>
