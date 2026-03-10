#!/usr/bin/env bash
# run-ADVI_APISCP-001-lambda-edge-cloudfront-investigation.sh
#
# Pattern 2: Technical gap investigation — Lambda@Edge + CloudFront deployment
# The CTO PRD (ADVI_APISCP) proposes v4 of shared-advisor-router with dynamic
# S3 origin routing per firm. Three critical unknowns must be verified before
# agents implement:
#   1. Lambda@Edge deployment mechanism (NOT in Terraform or lambda-source-map.json)
#   2. CloudFront origin-request event shape for dynamic origin mutation
#   3. OAI policy scope — per-bucket grants vs wildcard
# Participants:
#   0.7.0_AE_CloudOps: knowledge SOURCE — owns CloudFront, IAM, shared-infra
#   0.4.0_DT_ClientPlatform: knowledge RECEIVER — will implement Lambda@Edge v4

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_APISCP"
THREAD_ID=""              # auto-assigned (ADVI_APISCP-001)
TOPIC="Lambda Edge CloudFront investigation"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.7.0_AE_CloudOps,0.4.0_DT_ClientPlatform"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context (M1 + M4)
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "shared-advisor-router Lambda@Edge v3 (current — URI rewrite only, no origin mutation)",
      "path": "infra/aws/lambda-edge/shared-advisor-router/index.mjs"
    },
    {
      "label": "auth-validator-edge Lambda@Edge v7 (JWT validation, injects X-Firm-Id header)",
      "path": "infra/aws/lambda-edge/auth-validator-edge/index.mjs"
    },
    {
      "label": "shared-infra Terraform (S3 artifact buckets, DynamoDB, IAM — NO CloudFront resources)",
      "path": "infra/aws/terraform/shared-infra/main.tf"
    },
    {
      "label": "S3 module with OAI policy (per-bucket grants, lines 131-159)",
      "path": "infra/aws/multi-account/terraform/modules/s3/main.tf"
    },
    {
      "label": "Lambda source map (Lambda@Edge functions are NOT listed here)",
      "path": "infra/aws/lambda/ci/lambda-source-map.json"
    }
  ],
  "documents": [
    {
      "label": "ADVI_APISCP PRD — Scoped API Multi-Partner Routing Architecture",
      "path": "docs/architecture/ADVI_APISCP_PRD.md"
    },
    {
      "label": "ADVI_APISCP project definition",
      "path": "org/projects/ADVI_APISCP.json"
    }
  ],
  "inline": "Goal: Verify the three critical technical assumptions in the CTO's ADVI_APISCP PRD BEFORE agents implement. The PRD proposes upgrading shared-advisor-router from v3 (URI rewrite only) to v4 (dynamic S3 origin mutation based on X-Firm-Id). The PRD includes pseudocode but three things are unverified: (1) How Lambda@Edge functions are deployed — they are NOT in Terraform or lambda-source-map.json, so the deployment mechanism is unknown; (2) Whether the CloudFront origin-request event shape supports dynamic origin mutation via request.origin.s3 — the PRD's pseudocode assumes this works but it has never been done in this codebase; (3) Whether the OAI (Origin Access Identity) policy grants access to ALL opal-data-* buckets or only the currently-configured origin bucket (opal-data-bd) — the S3 module shows per-bucket grants, which would mean each new partner bucket needs an explicit OAI policy update. 0.7.0_AE_CloudOps is the knowledge SOURCE (owns CloudFront, IAM, OAI, shared-infra). 0.4.0_DT_ClientPlatform is the knowledge RECEIVER (will implement v4 based on verified facts from this thread). The thread receipt becomes the ground truth for the DT task order revision."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO framing)
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

## ADVI_APISCP-001: Lambda@Edge + CloudFront Technical Gap Investigation

I am the COO convening this Pattern 2 thread. The CTO has written PRD ADVI_APISCP proposing a v4 upgrade to \`shared-advisor-router\` Lambda@Edge that adds dynamic S3 origin routing per firm. The PRD includes pseudocode, but I have identified three critical assumptions that have NOT been verified against the actual infrastructure. No agent should implement until these are resolved.

**Turn order:** CloudOps (source) -> DT ClientPlatform (receiver). Three turns per agent.

---

### The three unknowns

#### Unknown 1: Lambda@Edge deployment mechanism

\`infra/aws/lambda-edge/shared-advisor-router/index.mjs\` and \`infra/aws/lambda-edge/auth-validator-edge/index.mjs\` exist in the repo, but:
- They are NOT in \`lambda-source-map.json\` (checked — no lambda-edge entries)
- They are NOT in any Terraform module under \`infra/aws/terraform/\`
- CloudFront distribution \`EVTSA9VEHNZVH\` is not managed by Terraform
- The deployment mechanism is completely unknown

**CloudOps: How were these Lambda@Edge functions deployed?** Look for:
- AWS CLI deploy scripts, Makefile targets, or CI scripts in or near \`infra/aws/lambda-edge/\`
- CloudFormation templates (separate from Terraform)
- Manual console deployment (check for package.json scripts, deploy notes, README)
- Any evidence of how auth-validator-edge reached v7 — there must be a deployment history

If you cannot find the deployment mechanism in the repo, state that clearly. That itself is a critical finding — it means DT must discover it via AWS CLI (\`aws lambda list-versions-by-function\`, \`aws cloudfront get-distribution-config\`) before implementing.

#### Unknown 2: CloudFront origin-request event shape for dynamic origin mutation

The PRD v4 pseudocode does this:

\`\`\`javascript
const firmId = request.headers["x-firm-id"]?.[0]?.value;
const bucket = \`opal-data-\${firmId}\`;
request.origin = {
  s3: {
    domainName: \`\${bucket}.s3.us-east-1.amazonaws.com\`,
    region: "us-east-1",
    authMethod: "origin-access-identity",
    path: "",
    customHeaders: {}
  }
};
request.headers["host"] = [{ key: "Host", value: \`\${bucket}.s3.us-east-1.amazonaws.com\` }];
\`\`\`

**DT ClientPlatform: Verify this event shape.** Specifically:
1. Does \`request.origin.s3\` exist on origin-request events? (It should — origin-request triggers run after cache miss, before CloudFront contacts the origin)
2. Can you MUTATE \`request.origin.s3.domainName\` to point to a different bucket than what CloudFront is configured with?
3. Does \`authMethod: "origin-access-identity"\` work when the target bucket is NOT the distribution's configured origin? Or does OAI only authenticate against the configured origin?
4. Is \`request.origin = { s3: { ... } }\` (full replacement) correct, or must you mutate individual fields on the existing object?

Read the current v3 handler (\`shared-advisor-router/index.mjs\`) — it only does URI rewrite, never touches \`request.origin\`. Also read \`auth-validator-edge/index.mjs\` to confirm the X-Firm-Id header injection format.

#### Unknown 3: OAI policy scope

The S3 module (\`infra/aws/multi-account/terraform/modules/s3/main.tf\`, lines 131-159) shows that OAI grants are **per-bucket**:

\`\`\`hcl
principals {
  type        = "AWS"
  identifiers = [var.cloudfront_oai_arn]
}
resources = ["\${aws_s3_bucket.this.arn}/*"]
\`\`\`

This means the OAI can only access buckets that explicitly grant it access. The PRD assumes a wildcard \`opal-data-*\` pattern, but the Terraform module does NOT do this.

**CloudOps: Answer these questions:**
1. Which S3 buckets currently have an OAI policy granting CloudFront access? Is it only \`opal-data-bd\`, or are there others?
2. When a new partner bucket (\`opal-data-{firmId}\`) is created, does the OAI policy get automatically applied? Or must someone explicitly add it per bucket?
3. Is there a Terraform module or script that creates partner buckets with OAI policies already attached?
4. If OAI grants are per-bucket, what is the onboarding sequence for a new firm? The PRD says "no IAM changes needed (wildcard opal-data-* already grants access)" — is this actually true?

Use tool access to search for: \`cloudfront_oai\` references in Terraform, OAI ARN values, S3 bucket policies on \`opal-data-bd\`.

---

### Self-unblock requirement (M11)

If you are uncertain about any of the three unknowns: READ the files. Search for deploy scripts. Check Terraform state references. Do NOT close this thread with "we need to check X" — check it now. You have tool access. The only acceptable unresolved items are things that require live AWS CLI queries (e.g., \`aws cloudfront get-distribution-config\`) which cannot be run from within this thread.

### Final turn must produce:

1. **Deployment mechanism verdict** — how Lambda@Edge is deployed, or explicit statement that it must be discovered via AWS CLI
2. **Event shape verification** — whether \`request.origin.s3\` dynamic mutation is supported, with any caveats
3. **OAI policy scope** — per-bucket or wildcarded, and what the onboarding sequence for new partner buckets actually requires
4. **Revised implementation guidance** — what the DT task order should say, correcting any PRD assumptions that turned out to be wrong
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

echo "Scaffolding thread..."
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
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
