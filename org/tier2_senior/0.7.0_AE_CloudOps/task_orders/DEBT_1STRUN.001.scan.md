<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-debt-1strun-001-0.7.0_ae_cloudops</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Scan ALL shared AWS infrastructure for technical debt across 6 categories:
    shared Terraform modules, Lambda layers, CI tooling, EC2 manifests, IAM
    roles/policies, S3 buckets, and DynamoDB tables. Also enumerate all AWS
    resources to build a complete inventory. AND aggregate findings from
    0.5.0_AE_OpalETL and 0.6.0_AE_PartnerETL. Produce a structured findings
    log and an aggregate infrastructure report. Report to 2.0.0_SA_COO.
  </objective>

  <scope>
    <files>
      <!-- Shared infra code -->
      <file action="scan">infra/aws/terraform/shared-infra/</file>
      <file action="scan">infra/aws/lambda/layers/</file>
      <file action="scan">infra/aws/lambda/ci/ (build scripts, source maps, layer maps)</file>
      <file action="scan">infra/aws/ec2/ (all EC2 service directories, EC2_MANIFEST.json, deploy scripts)</file>
      <!-- Portal notifications (S3 trigger infra) -->
      <file action="scan">infra/aws/terraform/portal-notifications/</file>
    </files>
    <aws_resource_audit>
      FULL AWS RESOURCE INVENTORY — this is the most critical part of the
      CloudOps scan. Enumerate ALL resources and cross-reference against code:

      1. S3 BUCKETS:
         aws s3 ls
         For each bucket: list top-level prefixes, identify owner pipeline,
         flag any bucket or prefix with no corresponding Terraform definition
         or no code that reads/writes to it.

      2. DYNAMODB TABLES:
         aws dynamodb list-tables --region us-east-1
         For each table: identify which Lambda or script uses it, flag any
         table with no code references (orphaned) or no Terraform definition.

      3. LAMBDA FUNCTIONS:
         aws lambda list-functions --region us-east-1
         Cross-reference against lambda-source-map.json. Flag any function
         that exists in AWS but is not in the source map (shadow Lambda).
         Flag any source map entry whose function no longer exists.

      4. IAM ROLES:
         aws iam list-roles (filter to opal-* or project-related prefixes)
         Flag roles attached to no resource or with overly broad policies.

      5. EC2 INSTANCES:
         aws ec2 describe-instances --region us-east-1
         Cross-reference against EC2_MANIFEST.json. Flag instances not in
         the manifest, and manifest entries with null instance_id or stale
         deployed_commit.

      6. SECRETS MANAGER:
         aws secretsmanager list-secrets --region us-east-1
         Flag secrets that are no longer referenced by any Lambda env var
         or script.

      7. EVENTBRIDGE RULES:
         aws events list-rules --region us-east-1
         Flag rules targeting deleted Lambdas or with no active targets.

      Report each resource class as a separate section in your findings.
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
        org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-23/debt_1strun_scan.md

      Use this structure:
        # DEBT_1STRUN Scan — 0.7.0_AE_CloudOps
        **Date:** 2026-03-23
        **Scope:** infra/aws/terraform/shared-infra/, infra/aws/lambda/layers/, infra/aws/lambda/ci/, infra/aws/ec2/

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

    <requirement id="3">
      AGGREGATION: After completing your own scan, collect the scan logs from:
        - org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-03-23/debt_1strun_scan.md
        - org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-03-23/debt_1strun_scan.md

      Produce an aggregate infrastructure report at:
        org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-23/debt_1strun_infra_aggregate.md

      Combine all AE findings (yours + 0.5.0 + 0.6.0), deduplicate cross-pipeline
      patterns, and rank the top 10 infrastructure debt items by severity and blast
      radius. This aggregate report goes to 2.0.0_SA_COO.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 6 categories scanned — none skipped</criterion>
    <criterion id="2">Every finding has file path, line numbers, category, severity, and description</criterion>
    <criterion id="3">Findings log written to logs/2026-03-23/debt_1strun_scan.md</criterion>
    <criterion id="4">Summary section with counts and top 3 priority recommendations</criterion>
    <criterion id="5">Aggregate report written to logs/2026-03-23/debt_1strun_infra_aggregate.md combining all AE findings</criterion>
    <criterion id="6">Aggregate report ranks top 10 infrastructure debt items by severity and blast radius</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scan only YOUR infrastructure scope — do not scan pipeline-specific code (other DS/AE agents handle those)</constraint>
    <constraint>Do not fix anything — this is a scan-only task. Fixes come in .002+ task orders.</constraint>
    <constraint>Report to 2.0.0_SA_COO — the aggregate report is the final AE deliverable for this scan phase.</constraint>
    <constraint>Be concrete: name files, line numbers, function names. No vague "could be improved" findings.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">logs/2026-03-23/debt_1strun_scan.md with structured findings table</deliverable>
    <deliverable type="document">logs/2026-03-23/debt_1strun_infra_aggregate.md with combined AE findings and top 10 ranking</deliverable>
  </deliverables>
</task_order>
