```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-10-drfr-ptmch-bd-audit</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <note>Superseded by thread DRFR_PTMCH-001. Repo-grounded findings delivered via thread. CLI gates remain -- see findings doc.</note>
  </metadata>

  <objective>
    Audit the BD pipeline gold output structure and assess the feasibility of adding
    a snapshot archive mechanism to support the Portal Time Machine (Layer 2 — BD data).
    BD gold files are currently overwritten in-place with no versioning or historical
    preservation. The Time Machine requires either S3 versioning on opal-data-bd OR
    a snapshot-per-rebuild pattern. Your findings determine which approach is viable
    and at what cost.
  </objective>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      FULL GOLD/ INVENTORY: List all files and directories in `opal-data-bd/gold/`.
      Include: key, size, last modified. Pay attention to:
      - Top-level JSON files (timeseries_chart.json, leaderboards, etc.)
      - `clients/` subdirectory (count of files, total size)
      - `client_detail/` subdirectory
      - `advisors/` and `timeseries/` subdirectories
      - `partner_analytics/` subdirectory
      Commands:
        `aws s3 ls s3://opal-data-bd/gold/ --recursive`
      Report total object count and total size in GB.
    </requirement>

    <requirement id="2">
      GOLD REBUILD CADENCE: Determine how often the gold rebuild runs.
      - Check the `bd-gold-layer-runner` EC2 cron, systemd timers, or any
        EventBridge schedule that triggers it.
      - Is it triggered manually, on a schedule, or by an S3 event?
      - What triggers `bd-portal-publisher` after the rebuild? The known trigger
        is an S3 PutObject event on `opal-data-bd/gold/pipeline-complete.json`.
        Confirm this is still the mechanism (check the Lambda's S3 event trigger
        in the bd-pipeline Terraform or Lambda console).
      Report: "Gold rebuild runs: [schedule or manual]. Publisher trigger: [event]."
    </requirement>

    <requirement id="3">
      SNAPSHOT STORAGE COST ESTIMATE:
      Using the total gold/ size from requirement 1:
      - At the rebuild cadence from requirement 2, how many snapshots accumulate
        per month?
      - With a 90-day retention window, what is the total snapshot storage (GB)?
      - Estimate S3 Standard storage cost per month at $0.023/GB.
      - Is this within acceptable bounds (rough threshold: under $50/month)?
    </requirement>

    <requirement id="4">
      bd-portal-publisher SOURCE PATH:
      Read `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`.
      - Is the source path (`opal-data-bd/gold/`) hardcoded or read from an env var?
      - If hardcoded: what would it take to parameterize it to accept a
        `source_prefix` (e.g., `gold/snapshots/20260305/`)?
      - Estimate the blast radius of this change (other callers, tests, Terraform).
      This determines whether Time Machine can re-use the existing publisher or
      needs a new restore Lambda.
    </requirement>

    <requirement id="5">
      bd-portal-advisor-publisher SCOPE:
      Read `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`.
      - Does it independently read from gold/, or does it receive data from
        bd-portal-publisher as input?
      - Does it need separate snapshot support, or would parameterizing
        bd-portal-publisher be sufficient?
    </requirement>

    <requirement id="6">
      EXISTING HISTORICAL DATA SURVEY:
      Check opal-data-bd/ for any existing historical snapshots or backups:
        `aws s3 ls s3://opal-data-bd/ --recursive` filtered to non-gold/ prefixes.
      Are there any dated folders (e.g., opal-data-bd/archive/, opal-data-bd/backup/)?
      This determines the earliest date the Time Machine can serve for BD data.
      If no historical data exists, explicitly state: "Time Machine for BD data
      can only serve dates from [project deployment date] forward."
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Findings document exists at deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md
      with actual AWS CLI output for requirements 1, 2, 6.
    </criterion>
    <criterion id="2">
      Requirement 3 produces a clear cost verdict: "Snapshot approach is VIABLE
      at $X/month" or "COST CONCERN — explore S3 versioning instead."
    </criterion>
    <criterion id="3">
      Requirement 4 produces a clear verdict on publisher parameterization:
      "Source path is [hardcoded/env-var]. Parameterization requires [N] changes."
    </criterion>
    <criterion id="4">
      Each PRD assumption in Section 4 "For 0.6.0_AE_PartnerETL" is marked CONFIRMED,
      WRONG (with correction), or UNKNOWN (with evidence).
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only audit only. Do NOT modify bd-portal-publisher, Terraform,
    or any gold/ files. Do NOT trigger a gold rebuild.</constraint>
    <constraint>Do NOT write any snapshot files to S3. This is a discovery task only.</constraint>
    <constraint>Do NOT modify any source code files except to create your deliverable.</constraint>
    <constraint>The gold rebuild is currently DEFERRED pending ADVI_49FNV3 completion
    (per COO decision log 2026-03-09). Do NOT trigger it as part of this audit.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="1.0.0_SA_CTO" task="DRFR_PTMCH_PRD.md" status="complete"/>
    <dependency agent="0.7.0_AE_CloudOps" task="DRFR_PTMCH.001.cloudops-versioning-iam-audit.md" status="pending"
      note="CloudOps will audit S3 versioning on opal-data-bd (requirement 2 of their task order). Coordinate — if CloudOps finds versioning is already enabled on opal-data-bd, the snapshot archive approach may be unnecessary. Check their findings before finalizing requirement 3 cost estimate."/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md
      — structured audit findings for all 6 requirements
    </deliverable>
  </deliverables>
</task_order>
```
