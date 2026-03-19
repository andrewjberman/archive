#!/usr/bin/env bash
# P2 Distribution Tab Alignment Thread — ADVI_MVPLVL
#
# Pattern 0 (DS + DE + RD, 3-party round robin). DS checks backend "Other"
# aggregation and state name mapping. DE owns state lift for time window
# inheritance (2i). RD owns 8 rendering items. All three must agree on
# prop threading and data shapes.
#
# Run from repo root: bash org/threads/staging/run-ADVI_MVPLVL-002-p2-distribution-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_MVPLVL"
THREAD_ID=""
TOPIC="P2 Distribution Tab alignment"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context -- M1 compliance
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "DistributionTab.tsx — snapshot/continuous, drill state, capitalization, Other logic, NNA strip",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx"
    },
    {
      "label": "PartnerAnalytics.tsx — Assets Overview panel (timeWindow state that 2i needs to inherit from)",
      "path": "portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx"
    },
    {
      "label": "AdvisorIntelligence.tsx — page root, granularity state, prop threading to tabs",
      "path": "portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx"
    },
    {
      "label": "AdvisorIntelligence types — all type definitions",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "bd-portal-publisher Lambda — produces partner_analytics JSON with donut segments, distribution stats",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "09_generate_partner_analytics.py — EC2 script that builds partner_analytics/header_metrics_{quarterly,monthly,annual}.json",
      "path": "data/black_diamond/scripts/gold/09_generate_partner_analytics.py"
    },
    {
      "label": "DE brief on NNA cohort-specific time machine strip (2h reference)",
      "path": "org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-13/nna_cohort_specific_time_machine_brief.md"
    }
  ],
  "documents": [
    {
      "label": "ADVI_MVPLVL PRD — Part 2 (Distribution Tab) is the scope for this thread",
      "path": "docs/architecture/ADVI_MVPLVL_PRD.md"
    }
  ],
  "inline": "Goal: Align DS, DE, and RD on the 9 Distribution Tab work items (2a-2i) before task orders are written. DS checks: does the backend pre-aggregate into Other (2e), does it provide state abbreviations or full names (2c), are all cohort NNA values available per-period per-segment (2h)? DE owns: time window state lift from PartnerAnalytics to DistributionTab (2i). RD owns: all 9 rendering items but needs confirmed data shapes from DS and prop interface from DE. Deliverable: concrete agreement on what DS/DE will provide and what RD will consume for each item."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- DS goes first
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$OPENING_FILE" << OPENING_EOF
---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: ${TS}
signal: continue
---

## P2 Distribution Tab — Alignment

I am DS for Pod 4. This thread covers the 9 Distribution Tab items from the ADVI_MVPLVL PRD (Part 2). My role is to confirm backend data availability and shapes so DE and RD can implement without ambiguity.

### Items requiring DS investigation:

**2c. Standard capitalization** — The backend (script 09 / publisher) emits state keys as abbreviations (\`tx\`, \`ca\`). Does it also emit full state names anywhere, or is the abbreviation-to-full-name mapping purely a frontend concern? I will check the publisher and script 09 output to confirm what keys are emitted.

**2e. Show all cohorts (no Other)** — The PRD says remove the top-8 + Other limit at the snapshot level. Does the backend (\`views.aua.current.donut.segments\` / \`views.nna.current.geo.donut.segments\`) already provide ALL segments, or does it pre-aggregate into "Other"? I will check script 09 / publisher to determine if this is frontend-only or requires a backend change.

**2h. NNA time machine cohort-specific strip** — The DE brief documents data availability at each drill level. I need to confirm that NNA values per state/city/architect are available in every period's data structure. The DE brief says relationship-level NNA is NOT available (backend gap, deferred). I will verify the per-period structure in script 09 output.

### Items owned by DE:

**2i. Inherit time window from header** — DE needs to lift \`timeWindow\` state from \`PartnerAnalytics.tsx\` (or \`AdvisorIntelligence.tsx\`) and pass it as a prop to \`DistributionTab\`. The independent \`WINDOW_OPTIONS\` toggle in Distribution should be removed. DE: what is your plan for this state lift? Will \`timeWindow\` live in \`AdvisorIntelligence.tsx\` alongside \`granularity\`, or stay in \`PartnerAnalytics\` and get passed through?

### Items owned by RD (frontend-only, but need DS data confirmation):

- **2a.** Snapshot drilldown completeness QA (after 2c, 2d, 2e are done)
- **2b.** Remove "Period NNA" labels (3 text replacements)
- **2d.** Retain cohort state across AUA/NNA toggle (remove \`metric\` from useEffect deps)
- **2f.** Continuous view: all top-level, top 8 + Other at drill level
- **2g.** \`no_city\` entries grouped into Other at drill level

### Questions for DE and RD:

1. **DE:** For 2i, will you lift \`timeWindow\` to \`AdvisorIntelligence.tsx\` (same level as \`granularity\`)? If so, both PartnerAnalytics and DistributionTab receive it as props. What prop name?
2. **RD:** For 2c state name mapping — do you want a frontend lookup table (abbrev -> full name), or should DS add full state names to the publisher output? Frontend table is faster to ship; backend is more authoritative.
3. **RD:** For 2h NNA strip — the DE brief says 3 levels are supported (state, city, architect) but relationship-level NNA is NOT in the backend. Are you OK deferring relationship-level to post-MVP?

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.
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
