#!/usr/bin/env bash
# run-ADHC_GPTCST-001-openai-cost-audit-inventory.sh
#
# Pattern 2: GPT Cost Audit — AE inventory and optimization investigation
# Two AEs own all automated OpenAI callers:
#   0.5.0_AE_OpalETL: news pipeline suite, image generators, market update, keyword intel
#   0.7.0_AE_CloudOps: infrastructure_monitor (already has openai_cost_tracker.py)
# Thread goal: produce complete inventory of all callers, models, frequencies, and
# Phase 2/3 recommendations (optimize + integrate into morning report).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADHC_GPTCST"
THREAD_ID=""              # auto-assigned (ADHC_GPTCST-001)
TOPIC="OpenAI cost audit caller inventory"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.5.0_AE_OpalETL,0.7.0_AE_CloudOps"
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
      "label": "Infrastructure monitor — OpenAI cost tracker (existing)",
      "path": "infra/aws/lambda/infrastructure_monitor/openai_cost_tracker.py"
    },
    {
      "label": "Infrastructure monitor — main Lambda",
      "path": "infra/aws/lambda/infrastructure_monitor/lambda_function.py"
    },
    {
      "label": "Infrastructure monitor — OpenAI integration README",
      "path": "infra/aws/lambda/infrastructure_monitor/README_OPENAI_INTEGRATION.md"
    },
    {
      "label": "News trending analysis Lambda",
      "path": "infra/aws/lambda/news_trending_analysis/lambda_function.py"
    },
    {
      "label": "News layer 3 curation Lambda",
      "path": "infra/aws/lambda/news_layer3_curation/lambda_function.py"
    },
    {
      "label": "Semantic news layer 3 curation Lambda",
      "path": "infra/aws/lambda/semantic-news-layer3-curation/lambda_function.py"
    },
    {
      "label": "Trending image generator Lambda",
      "path": "infra/aws/lambda/trending_image_generator/lambda_function.py"
    },
    {
      "label": "Trending image selector Lambda",
      "path": "infra/aws/lambda/trending_image_selector/lambda_function.py"
    },
    {
      "label": "Market update generator Lambda",
      "path": "infra/aws/lambda/market_update_generator/lambda_function.py"
    },
    {
      "label": "Keyword intelligence generator Lambda",
      "path": "infra/aws/lambda/keyword_intelligence_generator/lambda_function.py"
    },
    {
      "label": "SmartX AI supervisor (EC2)",
      "path": "infra/aws/ec2/smartx-exporter/ai-supervisor-v2.py"
    },
    {
      "label": "Lambda source map",
      "path": "infra/aws/lambda/ci/lambda-source-map.json"
    }
  ],
  "documents": [
    {
      "label": "ADHC_GPTCST project definition",
      "path": "org/projects/ADHC_GPTCST.json"
    }
  ],
  "inline": "Goal: Produce a complete inventory of ALL automated OpenAI API callers in the Opal Capital infrastructure. OpenAI costs are accelerating unexpectedly. Andrew wants to know exactly which functions call which models (gpt-5_2-2025-12-11, gpt-4o-mini-2024-07-18, gpt-4o-2024-08-06, dall-e-3, etc.), how often, and at what token volume. 0.5.0_AE_OpalETL owns the news pipeline Lambdas, image generators, market update, and keyword intelligence generators — these are likely the bulk of spend. 0.7.0_AE_CloudOps owns infrastructure_monitor which ALREADY has an openai_cost_tracker.py — this is the Phase 3 integration point for the morning report. Both agents must READ the injected source files and produce grounded answers. The thread output should be: (1) a complete caller inventory table, (2) Phase 2 optimization recommendations (leaks, redundant calls, model downgrades, caching), and (3) Phase 3 integration plan for wiring cost tracking into the morning report."
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

## ADHC_GPTCST-001: OpenAI Cost Audit — Caller Inventory + Optimization

I am the COO convening this investigation thread. OpenAI API costs are accelerating unexpectedly. Andrew wants a complete audit across three phases:

1. **Audit** — inventory all automated OpenAI callers, models used, call frequency, token volume
2. **Optimize** — identify leaks, redundant calls, oversized model selection, missing caching
3. **Integrate** — wire GPT token spend into the morning infrastructure report for ongoing tracking

**Turn order:** OpalETL -> CloudOps. Three turns per agent.

### Pre-identified callers (from codebase grep)

**Lambda callers (0.5.0_AE_OpalETL):**
- \`news_trending_analysis\` — news pipeline
- \`news_layer3_curation\` — news pipeline
- \`semantic-news-layer3-curation\` — news pipeline
- \`trending_image_generator\` — DALL-E / image generation
- \`trending_image_selector\` — image selection with GPT
- \`market_update_generator\` — market commentary
- \`keyword_intelligence_generator\` — keyword extraction
- \`portal_data_proxy\` — unclear usage
- \`security-sweep-comprehensive\` — security scanning
- \`news_semantic_clustering\` — news grouping

**Lambda callers (0.7.0_AE_CloudOps):**
- \`infrastructure_monitor\` — already has \`openai_cost_tracker.py\`

**EC2 callers:**
- \`smartx-exporter/ai-supervisor-v2.py\` — trade execution AI
- \`seeking_alpha_scraper\` — multiple GPT-assisted scripts

**Non-AWS (local):**
- \`org/threads/orchestrator.py\` — agent thread system (gpt-5.2)

### 0.5.0_AE_OpalETL — your turn first.

Read each of the Lambda source files injected in context. For EACH caller, report:

| Field | What to report |
|-------|---------------|
| Function name | Lambda function name or EC2 script |
| Model used | Exact model string (e.g., gpt-4o-mini-2024-07-18) |
| Call type | chat.completions, images.generate, embeddings, etc. |
| Trigger | EventBridge schedule, S3 event, API Gateway, manual |
| Frequency | How often it fires (daily, hourly, per-event, etc.) |
| Est. tokens/call | Rough estimate from prompt size + response |
| Purpose | What it does (1 sentence) |
| Optimization potential | Can it use a cheaper model? Is it redundant? Is output cached? |

Also check: are any of these Lambdas DEPRECATED or NOT CURRENTLY DEPLOYED? Check the source map (\`lambda-source-map.json\`) to see which ones are active vs orphaned. Orphaned callers that still fire are pure waste.

Use your tool access to read any files not already in context (e.g., EventBridge rules in Terraform, \`news_semantic_clustering\` source, \`portal_data_proxy\` source).

### 0.7.0_AE_CloudOps — after OpalETL.

1. Read \`openai_cost_tracker.py\` and the infrastructure monitor README. Report what cost tracking already exists — what does it track, how often, what's in the morning report today?
2. For each caller OpalETL identifies, assess: is it visible in the existing cost tracker? If not, what's needed to add it?
3. Propose the Phase 3 integration plan: what changes to infrastructure_monitor are needed to surface per-function GPT spend in the morning report?
4. Also audit the \`smartx-exporter/ai-supervisor-v2.py\` (EC2) — this is closer to your shared services domain.

### Self-unblock requirement (M11)

If you are uncertain about a model string, trigger schedule, or whether a Lambda is deployed: READ the source file and the source map. Do not guess. Do not close this thread with "we need to check X" — check it now. You have tool access.

### Final turn must produce:

1. **Complete caller inventory table** (all fields above, every caller)
2. **Phase 2 optimization recommendations** — ranked by estimated cost impact
3. **Phase 3 integration plan** — specific changes to infrastructure_monitor to add GPT cost visibility to the morning report
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
