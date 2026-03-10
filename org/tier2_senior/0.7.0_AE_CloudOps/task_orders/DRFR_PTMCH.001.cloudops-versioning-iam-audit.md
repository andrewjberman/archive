```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-10-drfr-ptmch-cloudops-audit</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <note>Superseded by thread DRFR_PTMCH-001. CTO-issued task orders are a protocol deviation -- COO issues task orders. Work delivered via thread receipt. CLI gates remain (S3 versioning, DynamoDB PITR, CloudFront config) -- see findings doc.</note>
  </metadata>

  <objective>
    Audit the cloud infrastructure prerequisites for the Portal Time Machine feature.
    The Time Machine requires S3 versioning on two buckets, DynamoDB PITR knowledge,
    complete CloudFront path-to-origin mapping, and IAM gap analysis. Your findings
    are a hard gate before any implementation work begins. Produce a structured
    findings document at your deliverables/ folder.
  </objective>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      S3 VERSIONING — opal-data-portal-v2: Run
      `aws s3api get-bucket-versioning --bucket opal-data-portal-v2`.
      Record exact response. If versioning is not Enabled, document what enabling it
      would require (procedure, risks to in-flight pipelines, safe window).
    </requirement>

    <requirement id="2">
      S3 VERSIONING — opal-data-bd: Run
      `aws s3api get-bucket-versioning --bucket opal-data-bd`.
      Record exact response. Assess whether versioning is a viable mechanism for BD
      gold files vs. the snapshot archive approach described in the PRD.
    </requirement>

    <requirement id="3">
      S3 VERSION COST ESTIMATE: For opal-data-portal-v2/json/, estimate:
      - How many distinct object keys exist in json/latest/ and json/ top level?
      - At approximately weekly yang pipeline runs, how many versions accumulate
        over 90 days?
      - What is the estimated S3 storage cost delta from enabling versioning with
        a 90-day noncurrent version lifecycle rule?
      Use `aws s3api list-objects-v2 --bucket opal-data-portal-v2 --prefix json/`
      with `--query "length(Contents)"` for the count.
    </requirement>

    <requirement id="4">
      DYNAMODB TABLES — Yang pipeline: Identify all DynamoDB tables that the yang
      pipeline writes to. The known writer is `yang-ingest-dynamodb`. Check the
      Lambda's env vars and source code. For each write-path table:
      - Is Point-in-Time Recovery (PITR) enabled? Check via
        `aws dynamodb describe-continuous-backups --table-name {table}`.
      - Does the portal frontend read from this table at request time (i.e., portal
        fetches DynamoDB items on page load), or is it only used during pipeline
        processing (pre-computed to JSON before portal reads)?
      - Verdict: does Time Machine require DynamoDB rollback for this table?
    </requirement>

    <requirement id="5">
      CLOUDFRONT PATH ROUTING: For distribution EVTSA9VEHNZVH (the portal CDN),
      list every origin and the path patterns routed to it. Specifically:
      - What path(s) serve opal-data-portal-v2/json/* content?
      - What path(s) serve opal-data-bd/gold/* content (via proxy or direct)?
      - Does /api/public/* invalidation cover yang outputs AND BD outputs?
        Or does BD data serve via /api/scoped/* requiring a separate invalidation?
      Use `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`.
    </requirement>

    <requirement id="6">
      IAM GAP ANALYSIS: Does the `opal-data-refresh-api` Lambda execution role have:
      - `s3:GetObjectVersion` on opal-data-portal-v2 (needed for version restore)?
      - `s3:GetObject` and `s3:PutObject` on opal-data-bd/gold/* (needed for BD copy-back)?
      - `s3:GetObject` on opal-data-bd/snapshots/* (needed to read BD snapshots)?
      List each permission, whether it exists, and what policy grants it (or what
      needs to be added).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Findings document exists at deliverables/DRFR_PTMCH.001.cloudops-findings.md
      with a section per requirement (1-6) containing actual CLI output or
      AWS console-confirmed data, not assumptions.
    </criterion>
    <criterion id="2">
      Each PRD assumption in Section 4 "For 0.7.0_AE_CloudOps" is marked CONFIRMED,
      WRONG (with correction), or UNKNOWN (with explanation of why it could not be
      determined).
    </criterion>
    <criterion id="3">
      CloudFront origin routing is documented as a table:
      path pattern | origin | bucket | requires separate invalidation?
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only AWS audit only. Do NOT enable S3 versioning, modify IAM
    policies, or change any CloudFront config. Document recommendations only.</constraint>
    <constraint>Do NOT modify any source code files. This is a discovery task.</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before any aws CLI commands with ARN paths
    on Git Bash (Windows).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="1.0.0_SA_CTO" task="DRFR_PTMCH_PRD.md" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md
      — structured audit findings for all 6 requirements
    </deliverable>
  </deliverables>
</task_order>
```
