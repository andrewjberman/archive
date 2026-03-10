#!/usr/bin/env bash
# run-DRFR_PTMCH-001-portal-time-machine-ae-discovery.sh
#
# Pattern 2: Technical gap investigation -- Portal Time Machine infrastructure discovery
#
# All three AE agents audit their domains in parallel (round-robin). CloudOps goes
# first because their S3 versioning verdict is the single most critical fact that
# changes the architecture for every other layer. OpalETL second (can reference
# the versioning verdict). PartnerETL third (absorbs both CloudOps and OpalETL findings).
#
# Participants:
#   0.7.0_AE_CloudOps   -- S3 versioning, DynamoDB PITR, CloudFront routing, IAM gaps
#   0.5.0_AE_OpalETL    -- yang archive health, ingest-dynamodb scope, FRED path, market-overview
#   0.6.0_AE_PartnerETL -- BD gold inventory, rebuild cadence, snapshot feasibility, publisher parameterization
#
# Deliverables (each agent produces their own findings doc):
#   org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md
#   org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md
#   org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="DRFR_PTMCH"
THREAD_ID=""
TOPIC="Portal Time Machine AE infrastructure discovery"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.7.0_AE_CloudOps,0.5.0_AE_OpalETL,0.6.0_AE_PartnerETL"
MAX_TURNS=2
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context (M1 + M4) -- actual Lambda source required for AE threads
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "yang-capture-output-versions Lambda -- scans json/ prefix, captures S3 VersionIds after pipeline success, writes outputs-manifest.json",
      "path": "infra/aws/lambda/v2_portal/yang_pipeline/outputs/capture-output-versions/lambda_function.py"
    },
    {
      "label": "yang-ingest-dynamodb Lambda -- writes pipeline results to DynamoDB (table name, PK/SK unknown -- must be determined)",
      "path": "infra/aws/lambda/v2_portal/yang_pipeline/outputs/ingest-dynamodb/lambda_function.py"
    },
    {
      "label": "yang-refresh-fred-cache Lambda -- refreshes FRED macro data (output S3 path must be identified)",
      "path": "infra/aws/lambda/v2_portal/yang_pipeline/outputs/refresh-fred-cache/lambda_function.py"
    },
    {
      "label": "opal-data-refresh-api Lambda -- contains handle_rollback (copy_object with CopySourceVersionId), IAM role determines S3 permissions",
      "path": "infra/aws/lambda/data_refresh/lambda_function.py"
    },
    {
      "label": "bd-portal-publisher Lambda -- triggered by pipeline-complete.json S3 event, writes all gold/ JSON outputs",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "bd-portal-advisor-publisher Lambda -- writes per-advisor client files to gold/",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py"
    },
    {
      "label": "yang-pipeline Step Functions definition -- confirms whether capture-output-versions is a step and when it runs relative to generate-manifest",
      "path": "infra/aws/terraform/yang-pipeline/stepfunctions.tf"
    },
    {
      "label": "yang-pipeline IAM -- execution role policies for data-refresh-api and yang pipeline Lambdas",
      "path": "infra/aws/terraform/yang-pipeline/iam.tf"
    },
    {
      "label": "Lambda source map -- all deployed Lambdas and their S3 artifact paths (Lambda@Edge and unmanaged Lambdas NOT listed)",
      "path": "infra/aws/lambda/ci/lambda-source-map.json"
    }
  ],
  "documents": [
    {
      "label": "DRFR_PTMCH PRD -- Portal Time Machine architecture, open questions per AE (Section 4), implementation phases (Section 5)",
      "path": "docs/architecture/DRFR_PTMCH_PRD.md"
    },
    {
      "label": "CloudOps task order -- full question list for 0.7.0_AE_CloudOps",
      "path": "org/tier2_senior/0.7.0_AE_CloudOps/task_orders/DRFR_PTMCH.001.cloudops-versioning-iam-audit.md"
    },
    {
      "label": "OpalETL task order -- full question list for 0.5.0_AE_OpalETL",
      "path": "org/tier2_senior/0.5.0_AE_OpalETL/task_orders/DRFR_PTMCH.001.opal-pipeline-archive-audit.md"
    },
    {
      "label": "PartnerETL task order -- full question list for 0.6.0_AE_PartnerETL",
      "path": "org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/DRFR_PTMCH.001.bd-pipeline-snapshot-audit.md"
    }
  ],
  "inline": "Goal: Three AEs perform their infrastructure discovery audits for the Portal Time Machine project (DRFR_PTMCH) in a shared thread so cross-dependencies are resolved in real time. The most critical single fact is whether S3 versioning is enabled on opal-data-portal-v2 -- if it is NOT enabled, the entire Layer 1 restore mechanism is broken and must be redesigned before any implementation begins. CloudOps (0.7.0) holds this verdict and goes first. OpalETL (0.5.0) goes second -- they can absorb the versioning verdict and adjust their archive health findings accordingly. PartnerETL (0.6.0) goes third -- their snapshot-vs-versioning cost analysis for opal-data-bd depends on CloudOps findings. Each AE produces a structured findings document in their own deliverables/ folder. The thread receipt and each agent's findings document together constitute the Phase 0 discovery package that unblocks Phase 1 implementation task orders."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$OPENING_FILE" << OPENING_EOF
---
agent: ${CREATED_BY}
turn: 0
timestamp: ${TS}
signal: continue
---

## DRFR_PTMCH-001: Portal Time Machine -- AE Infrastructure Discovery

I am the COO opening this Pattern 2 discovery thread. The CTO has written the Portal Time Machine PRD (DRFR_PTMCH). The goal is to restore every portal data source to its state as of 5:00 PM ET on a target date. Before any implementation task orders can be written, three AEs must audit their domains and produce structured findings documents.

**Turn order:** CloudOps -> OpalETL -> PartnerETL -> CloudOps -> OpalETL -> PartnerETL (round-robin, 2 turns each).

**Cross-dependency rule:** When you read a finding from an agent who went before you, absorb it and adjust your analysis accordingly. Do not duplicate their work -- build on it.

**Self-unblock requirement (M11):** If you are uncertain about any infrastructure fact -- a Lambda output path, an S3 prefix pattern, a DynamoDB table name, a Terraform resource -- READ the file during this thread and resolve it before your final turn. Acceptable blockers are live AWS CLI queries (e.g., \`aws s3api get-bucket-versioning\`, \`aws cloudfront get-distribution-config\`) which cannot be run from within the thread. An unresolved question about a file in the repo is NOT an acceptable final-turn caveat.

---

## For 0.7.0_AE_CloudOps (Turn 1 -- most critical)

You own the single highest-priority question in this entire project:

**Is S3 versioning enabled on \`opal-data-portal-v2\`?**

The entire Layer 1 rollback mechanism (\`yang-capture-output-versions\` writing VersionIds, \`handle_rollback\` calling \`copy_object\` with \`CopySourceVersionId\`) ONLY works if versioning is enabled. The \`opal-data-refresh-api\` Lambda's \`handle_rollback\` is in your context -- read it to understand what it currently does. Then check whether the S3 versioning state in Terraform or any config file confirms enabled/disabled. If you cannot determine it from repo files alone, state: "Must verify via AWS CLI: \`aws s3api get-bucket-versioning --bucket opal-data-portal-v2\`" and explain what each possible response means for the architecture.

Answer all 6 questions from your task order in your findings document at \`org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md\`:

1. S3 versioning status on \`opal-data-portal-v2\` (ENABLED / NOT ENABLED / unknown -- requires CLI)
2. S3 versioning status on \`opal-data-bd\` (same)
3. Version cost estimate for \`json/\` prefix at weekly yang cadence with 90-day lifecycle
4. DynamoDB tables the yang pipeline writes to (read \`yang-ingest-dynamodb\` Lambda in context). For each: is PITR enabled? Does portal read from it at request time?
5. CloudFront path routing on \`EVTSA9VEHNZVH\`: which paths serve \`opal-data-portal-v2\` vs \`opal-data-bd\`? Does \`/api/public/*\` invalidation cover BD data? (Read the Lambda@Edge source files in context -- \`shared-advisor-router\` and \`auth-validator-edge\` if present.)
6. IAM gaps: does \`opal-data-refresh-api\` Lambda have \`s3:GetObjectVersion\` on \`opal-data-portal-v2\`, and \`s3:PutObject\` on \`opal-data-bd/gold/*\`? Read \`iam.tf\` in context.

---

## For 0.5.0_AE_OpalETL (Turn 2)

After CloudOps reports on S3 versioning, you have the critical context you need for your most important question:

**Are the \`outputs-manifest.json\` files in \`opal-data-portal-v2/data-refresh/archive/\` actually capturing non-null versionId values?**

If CloudOps confirms versioning is NOT enabled, the answer is: all versionIds are null -- CRITICAL BLOCKER. State this as confirmed and move to documenting the gap. If CloudOps confirms it IS enabled, you must still verify the archive health by reading \`yang-capture-output-versions\` Lambda source (in your context) and determining whether the Lambda is correctly invoked from the Step Functions definition (also in context).

Answer all 6 questions from your task order in your findings document at \`org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md\`:

1. Archive health verdict: are versionIds non-null? (Use CloudOps finding + Lambda source + stepfunctions.tf analysis)
2. Full \`json/latest/\` inventory: you cannot list S3 live, but read the yang generator Lambdas in the source map to enumerate what files they write. Cross-check against what \`capture-output-versions\` would scan (the 10-minute window logic in the Lambda).
3. \`yang-capture-output-versions\` placement in Step Functions: read \`stepfunctions.tf\` -- is it a step? Does it run on every execution or only full runs?
4. \`yang-ingest-dynamodb\` scope: read the Lambda source in context. Which DynamoDB table(s), what PK/SK, and does the portal read from it at request time or is it pipeline-internal only?
5. \`yang-refresh-fred-cache\` output path: read the Lambda source. What S3 key(s) does it write? Is it under \`json/latest/\` (captured by archive) or a separate prefix?
6. Market-overview pipeline: from \`lambda-source-map.json\` in context, identify market-overview Lambdas and what they write to.

---

## For 0.6.0_AE_PartnerETL (Turn 3)

By the time you write, you have CloudOps's versioning verdict for \`opal-data-bd\` and OpalETL's archive analysis. Use them.

Your primary question is snapshot feasibility for BD data:

**Is the snapshot-per-rebuild approach (copy \`gold/\` to \`snapshots/{YYYYMMDD}/\` after each rebuild) cost-viable? Or should opal-data-bd use S3 versioning instead?**

Read the \`bd-portal-publisher\` and \`bd-portal-advisor-publisher\` Lambda sources in context. Count the output files they write. Estimate the gold/ total size (you cannot run S3 CLI in-thread, but the Lambda code shows which files are written -- use that as a proxy for count; estimate size from file types). Then estimate snapshot storage cost at $0.023/GB over 90 days.

Answer all 6 questions from your task order in your findings document at \`org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md\`:

1. BD gold/ inventory: enumerate files written by \`bd-portal-publisher\` and \`bd-portal-advisor-publisher\` from their source code. List each output key pattern and estimated size category (small JSON / large JSON / parquet).
2. Gold rebuild cadence: from your own session logs and the EC2 staleness investigation you completed today, you know the rebuild schedule. Document it.
3. Snapshot storage cost estimate: given file count and cadence, calculate 90-day retention cost. Verdict: VIABLE or COST CONCERN.
4. \`bd-portal-publisher\` source path: read the Lambda. Is \`opal-data-bd/gold/\` hardcoded or from an env var? What parameterization is needed?
5. \`bd-portal-advisor-publisher\` scope: does it independently query gold/ or receive data from the publisher? Does it need separate snapshot support?
6. Existing historical data: from your knowledge of opal-data-bd (no CLI in-thread), are there any existing backup or archive prefixes? State the earliest Time Machine date for BD data.

---

## Final turn for each agent (Turn 4, 5, 6)

Your second turn is for:
1. Resolving any cross-agent questions surfaced in round 1
2. Producing your complete findings document (write it to disk using your tools)
3. Providing implementation recommendations based on confirmed facts

**Each agent must write their findings document before their final turn ends.** The findings doc is the deliverable -- the thread receipt alone is not sufficient.

---

## What the COO needs from this thread

After the thread completes, I will:
1. Read all three findings documents
2. Verify any "must CLI verify" items directly
3. Write Phase 1 implementation task orders for CloudOps (enable versioning), OpalETL (yang-time-machine Lambda), PartnerETL (BD snapshot mechanism), and DE/RD (frontend Time Machine control)

The success criterion for this thread: each AE's findings document contains confirmed (not assumed) facts grounded in Lambda source, Terraform, or explicit "requires CLI" flags with the exact command to run.
OPENING_EOF

# ---------------------------------------------------------------------------
# Scaffold and run
# ---------------------------------------------------------------------------

CREATE_ARGS=(
  --topic           "$TOPIC"
  --created-by      "$CREATED_BY"
  --participants    "$PARTICIPANTS"
  --context-file    "$CONTEXT_FILE"
  --opening-message "$OPENING_FILE"
  --max-turns       "$MAX_TURNS"
  --turn-order      round_robin
  --project         "$PROJECT"
)

echo "Scaffolding thread DRFR_PTMCH-001..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve the actual thread ID
JQ="${REPO_ROOT}/.tools/jq.exe"
PROJECT_FILE="${REPO_ROOT}/org/projects/${PROJECT}.json"
COUNTER=$("$JQ" -r '.thread_counter' "$PROJECT_FILE")
SERIAL="${PROJECT}-$(printf '%03d' $COUNTER)"
TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-40 | sed 's/-$//')
THREAD_ID="${SERIAL}-${TOPIC_SLUG}"

echo ""
echo "Running orchestrator on: ${THREAD_ID}"
export PATH="/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools:$PATH"
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
