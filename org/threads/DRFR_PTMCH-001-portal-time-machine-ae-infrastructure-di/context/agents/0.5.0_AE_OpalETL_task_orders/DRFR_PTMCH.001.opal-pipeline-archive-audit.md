```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-10-drfr-ptmch-opalet-audit</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
  </metadata>

  <objective>
    Audit the yang pipeline archive infrastructure and all opal-managed pipeline
    S3 output patterns to determine what the Portal Time Machine can and cannot
    restore for Layer 1 (yang outputs) and Layer 4 (FRED/market-overview/other).
    Your findings are a hard gate before implementation. The most critical question
    is whether `yang-capture-output-versions` is writing non-null versionId values
    in production — if not, the preferred rollback mechanism is broken and must be
    fixed before any Time Machine work proceeds.
  </objective>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      ARCHIVE HEALTH CHECK — most critical requirement:
      List the 5 most recent entries in `opal-data-portal-v2/data-refresh/archive/`.
      For each execution:
      - Does `outputs-manifest.json` exist?
      - Open it: do the entries in `outputs.*.versionId` contain actual version ID
        strings (e.g., "abc123...") or null?
      - If null: S3 versioning is NOT enabled on opal-data-portal-v2. Flag as
        CRITICAL BLOCKER.
      - If non-null: confirm by picking one key/versionId pair and running
        `aws s3api get-object --bucket opal-data-portal-v2 --key {key}
        --version-id {versionId} /dev/null` to verify the version is retrievable.
      Command: `aws s3 ls s3://opal-data-portal-v2/data-refresh/archive/ --recursive`
      filtered to outputs-manifest.json files.
    </requirement>

    <requirement id="2">
      json/latest/ FULL INVENTORY: List all files currently in
      `opal-data-portal-v2/json/latest/` and `opal-data-portal-v2/json/` (top level).
      For each file: key, size, last modified.
      Command: `aws s3 ls s3://opal-data-portal-v2/json/latest/`
      and `aws s3 ls s3://opal-data-portal-v2/json/ --recursive`
      (note which files are NOT under json/latest/).
      Cross-check against the yang generator Lambda list (26 Lambdas) — are there
      json/ files that yang-capture-output-versions would miss because they fall
      outside the 10-minute time window?
    </requirement>

    <requirement id="3">
      yang-capture-output-versions PRODUCTION VERIFICATION:
      Check CloudWatch Logs for the `yang-capture-output-versions` Lambda function.
      - When was it last invoked?
      - Did it succeed?
      - How many files did it capture (look for log line "Captured N output versions")?
      - Is it in the Step Functions definition as a step? (Check stepfunctions.tf or
        the AWS Step Functions console for YangDataPipeline state machine definition.)
      - Is it invoked on EVERY pipeline run, or only on full runs?
    </requirement>

    <requirement id="4">
      yang-ingest-dynamodb SCOPE:
      Read `infra/aws/lambda/v2_portal/yang_pipeline/outputs/ingest-dynamodb/lambda_function.py`
      and identify:
      - Which DynamoDB table(s) does it write to?
      - What items (PK/SK structure, data fields)?
      - Is this data read by the portal at request time, or is it only used
        during pipeline processing (pre-computed to json/latest/ before portal reads)?
      Report: "Portal reads DynamoDB at runtime: YES/NO. Tables affected: [list]."
    </requirement>

    <requirement id="5">
      yang-refresh-fred-cache OUTPUT PATH:
      Read `infra/aws/lambda/v2_portal/yang_pipeline/outputs/refresh-fred-cache/lambda_function.py`.
      - What S3 key(s) does it write?
      - Is it under `json/latest/` (captured by archive) or a different prefix?
      - If different: this is a gap in the Time Machine. Document the path and size.
    </requirement>

    <requirement id="6">
      MARKET-OVERVIEW PIPELINE OUTPUT AUDIT:
      Identify the market-overview pipeline Lambda(s) from lambda-source-map.json.
      For each Lambda: what S3 bucket and key prefix does it write to?
      Is the output under opal-data-portal-v2/json/latest/ (captured), or separate?
      What is the approximate refresh cadence (daily, weekly, event-driven)?
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Findings document exists at deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md
      with actual AWS CLI output pasted for requirements 1, 2, 3.
    </criterion>
    <criterion id="2">
      Requirement 1 produces a clear verdict: "Version-based restore is FEASIBLE"
      or "Version-based restore is BROKEN — versionIds are null — CRITICAL BLOCKER".
    </criterion>
    <criterion id="3">
      Requirement 4 produces a clear verdict: "Portal reads DynamoDB at runtime:
      YES (table X) — DynamoDB restore required" or "NO — skip DynamoDB rollback".
    </criterion>
    <criterion id="4">
      Each PRD assumption in Section 4 "For 0.5.0_AE_OpalETL" is marked CONFIRMED,
      WRONG (with correction), or UNKNOWN (with evidence).
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only audit only. Do NOT modify any S3 objects, Lambda functions,
    or DynamoDB items. Do NOT trigger the yang pipeline.</constraint>
    <constraint>Do NOT modify any source code files except to create your deliverable.</constraint>
    <constraint>If you find that outputs-manifest.json is missing or versionIds are
    null for ALL recent executions, escalate immediately to 1.0.0_SA_CTO before
    continuing with other requirements — this changes the entire project architecture.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="1.0.0_SA_CTO" task="DRFR_PTMCH_PRD.md" status="complete"/>
    <dependency agent="0.7.0_AE_CloudOps" task="DRFR_PTMCH.001.cloudops-versioning-iam-audit.md" status="pending"
      note="Coordinate on S3 versioning findings — your requirement 1 may duplicate CloudOps req 1. If CloudOps runs first and confirms versioning is off, skip the versionId check and report CRITICAL BLOCKER directly."/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md
      — structured audit findings for all 6 requirements
    </deliverable>
  </deliverables>
</task_order>
```
