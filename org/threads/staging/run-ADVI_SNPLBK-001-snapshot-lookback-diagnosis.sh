#!/usr/bin/env bash
# ADVI_SNPLBK-001: Snapshot Lookback Regression Diagnosis
# Pattern 0 variant: DS + DE + RD diagnose whether backend (script 09) or
# frontend (DistributionTab/types) lost the quarterly lookback data.
#
# Run from repo root: bash org/threads/staging/run-ADVI_SNPLBK-001-snapshot-lookback-diagnosis.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_SNPLBK"
THREAD_ID=""              # auto-assigned from project serial
TOPIC="Snapshot Lookback Regression Diagnosis"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context -- files and briefing injected into CONTEXT_COMPILED.md
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Script 09: partner analytics generator (produces quarterly lookback data)",
      "path": "data/black_diamond/scripts/gold/09_generate_partner_analytics.py"
    },
    {
      "label": "DistributionTab: snapshot view (consumes lookback data)",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx"
    },
    {
      "label": "AdvisorIntelligence types (PeriodSnapshot, PartnerAnalyticsViewWithPeriods, hasTimeMachine)",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "API endpoint (fetches partner_analytics/header_metrics_{suffix}.json)",
      "path": "portal/src/api/endpoints/advisor-intelligence.ts"
    },
    {
      "label": "bd-portal-publisher Lambda (partner_analytics DISABLED -- EC2 script 09 owns output)",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "bd-portal-advisor-publisher Lambda (advisor-level publisher)",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py"
    },
    {
      "label": "EC2 user-data.sh (runs scripts 07, 09, 10, 11 on EC2)",
      "path": "infra/aws/ec2/bd-gold-detail-generator/user-data.sh"
    },
    {
      "label": "bd-gold-layer Lambda (Step 3: generate_snapshots -- different from script 09)",
      "path": "infra/aws/lambda/bd-pipeline/bd-gold-layer/lambda_function.py"
    }
  ],
  "inline": "DIAGNOSTIC THREAD: The Segment Analytics panel (Distribution tab, Snapshot view) previously displayed data from the current quarter plus 3 prior quarters via a 'time machine' strip. This lookback is no longer rendering. The regression could be: (A) backend -- script 09_generate_partner_analytics.py stopped producing q1/q2/q3 period data in its output JSON, (B) frontend -- DistributionTab.tsx or types.ts changed how it reads period data during 49FNV3 work, or (C) publisher -- the bd-portal-publisher Lambda is overwriting the EC2 output (unlikely since partner_analytics is DISABLED in the publisher). DS is the knowledge source for the backend data pipeline and gold scripts. DE is the knowledge source for API wiring and TypeScript interfaces. RD is the knowledge source for how the DistributionTab renders the time machine. Each agent must inspect their layer and report whether the data contract is intact at their boundary. The deliverable is a definitive root-cause diagnosis: which layer broke, which file, and what the fix is."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- written in the voice of CREATED_BY (DS)
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

## Snapshot Lookback Regression -- Diagnostic Thread

I am 0.4.0_DS_ClientPlatform. We are diagnosing a regression in the Segment Analytics panel (Distribution tab, Snapshot view). Previously, the panel displayed the current quarter plus 3 prior quarters in a "time machine" strip. The quarterly lookback is no longer rendering on the frontend.

The regression could be at one of three layers:
1. **Backend (Script 09):** \`09_generate_partner_analytics.py\` may have stopped producing \`q1\`, \`q2\`, \`q3\` period data in its output JSON (\`gold/partner_analytics/header_metrics_quarterly.json\`)
2. **Frontend (DistributionTab):** The component or types may have changed how they consume \`PartnerAnalyticsViewWithPeriods\` during 49FNV3 work
3. **Publisher (unlikely):** The \`bd-portal-publisher\` Lambda could be overwriting EC2 output -- but partner_analytics is explicitly DISABLED in the publisher (line ~1745-1750)

### What I need from each participant

**DS (me):** I will inspect Script 09 to verify it produces the \`current\`, \`q1\`, \`q2\`, \`q3\` structure in the output JSON. I will trace the period computation logic and confirm the output shape includes all 4 periods with their \`donut\`, \`distribution\`, and \`metrics\` sub-objects.

**DE (0.4.0_DE_ClientPlatform):** Inspect the API endpoint wiring. The frontend fetches \`/api/scoped/advisor-intelligence/partner_analytics/header_metrics_quarterly.json\`. Verify:
- Does the API endpoint pass through the full JSON (including q1/q2/q3) or does it transform/strip fields?
- Are the TypeScript types (\`PartnerAnalyticsViewWithPeriods\`, \`PeriodSnapshot\`) correctly typed to receive the backend output?
- Was there any recent change to the response parsing that might drop the period keys?

**RD (0.4.2_RD_AdvisorIntelligence):** Inspect the DistributionTab rendering logic. The \`hasTimeMachine()\` type guard checks for \`'current' in view\`. Verify:
- Is \`hasTimeMachineData\` being evaluated correctly at line ~1661?
- Is the quarter strip rendering block (lines ~2856-2949) receiving the q1/q2/q3 data?
- Was there a recent change to how \`analyticsData\` is structured or passed to \`SnapshotDistributionView\`?
- Check the \`rawView\` construction -- is it using the correct key from the API response to extract the view object?

### Key contract reference

Script 09 output shape (expected):
\`\`\`json
{
  "views": {
    "geo": {
      "current": { "donut": {...}, "distribution": {...}, "metrics": {...} },
      "q1": { "donut": {...}, "distribution": {...}, "metrics": {...} },
      "q2": { ... },
      "q3": { ... }
    },
    "adv": { "current": {...}, "q1": {...}, "q2": {...}, "q3": {...} }
  },
  "periods": { "current": {...}, "q1": {...}, "q2": {...}, "q3": {...} }
}
\`\`\`

Frontend expects: \`PartnerAnalyticsViewWithPeriods\` with \`current: PeriodSnapshot\`, \`q1?: PeriodSnapshot\`, \`q2?: PeriodSnapshot\`, \`q3?: PeriodSnapshot\`.

If any answer references a data field, S3 path, or interface name without citing a specific file or existing code, ask for the exact location before accepting it as ground truth.

## Self-unblock requirement (applies to all participants)

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. Acceptable blockers are things that do not exist yet or require a live data query outside the repo. An unresolved question about a file in this repo is not an acceptable receipt caveat.
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
)
[ -n "$PROJECT" ]   && CREATE_ARGS+=(--project "$PROJECT")
[ -n "$THREAD_ID" ] && CREATE_ARGS+=(--id "$THREAD_ID")

echo "Scaffolding thread..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve the actual thread ID (auto-assigned if project was set)
if [ -z "$THREAD_ID" ] && [ -n "$PROJECT" ]; then
  JQ="${REPO_ROOT}/.tools/jq.exe"
  PROJECT_FILE="${REPO_ROOT}/org/projects/${PROJECT}.json"
  COUNTER=$("$JQ" -r '.thread_counter' "$PROJECT_FILE")
  SERIAL="${PROJECT}-$(printf '%03d' $COUNTER)"
  TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-40 | sed 's/-$//')
  THREAD_ID="${SERIAL}-${TOPIC_SLUG}"
fi

echo ""
echo "Running orchestrator on: ${THREAD_ID}"
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
