#!/usr/bin/env bash
# run-ADVI_49FNV3-003-f2-projection-gro-redesign.sh
#
# Pattern 0: F2 projection visualization + GRO chart redesign
# CTO identified 4 flaws in the F2 implementation. Thread converges on
# exact formulas, tooltip layouts, GRO chart type, hero metrics, edge cases.
# Participants: CTO -> DE -> RD (round_robin, gpt-5.2, tools ON)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_49FNV3"
THREAD_ID=""              # auto-assigned (ADVI_49FNV3-003)
TOPIC="F2 projection visualization GRO chart redesign"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="1.0.0_SA_CTO,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
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
      "label": "PartnerAnalytics.tsx -- Assets Overview panel (AUA/NNA/GRO views + projection logic)",
      "path": "portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx"
    },
    {
      "label": "AdvisorIntelligence TypeScript types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    }
  ],
  "documents": [
    {
      "label": "CTO F2 Visualization Analysis (PRIMARY -- contains all 4 flaws + 5 convergence questions)",
      "path": "org/tier1_exec/1.0.0_SA_CTO/deliverables/ADVI_49FNV3-F2-visualization-analysis.md"
    },
    {
      "label": "RD session log (2026-03-09) -- what was built and why",
      "path": "org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/2026-03-09/ADVI_49FNV3_F2_F4_F6_F7_N1N2.md"
    },
    {
      "label": "49FNV3 PRD (F2 section)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md"
    }
  ],
  "inline": "Goal: Converge on the correct visualization design for projection ghost bars (AUA/NNA/GRO) and the GRO chart redesign in PartnerAnalytics.tsx. The CTO analysis document (Section 7) poses 5 specific convergence questions that must be answered. CTO is the architectural authority (pattern consistency, data model awareness). DE knows the data contracts, Recharts API capabilities, and type system implications. RD knows implementation feasibility and visual design within Recharts constraints. IMPORTANT: There are 3 portal DEV commits AFTER the F2-fix that CTO analyzed (9ce8d3b). Commits 28517dd (filter ghost keys from tooltips), 2f84197 (projection section in tooltips), and 8e9facd (project last bar in dataset) may address some flaws. Participants MUST read the current PartnerAnalytics.tsx source to verify which flaws are still present before proposing fixes."
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

## Pattern 0 Alignment -- F2 Projection Visualization + GRO Chart Redesign

I am the COO convening this alignment thread for ADVI_49FNV3 (49Financial V3). Andrew reviewed the F2 projected ghost bars implementation and identified fundamental issues. CTO has written a detailed analysis document (injected as primary context) cataloging 4 flaws and posing 5 convergence questions.

**Turn order:** CTO -> DE -> RD. Three turns per agent.

### Current State (read before responding)

The F2 implementation has evolved through multiple commits on portal DEV:
- \`594c3f6\` -- Original F2 ghost bars + F4 stacked bar + N1-N2 (RD)
- \`9ce8d3b\` -- F2-fix: AUA projection uses delta-based extrapolation (RD)
- \`28517dd\` -- F2-fix: filter ghost keys from AUA and NNA tooltips
- \`2f84197\` -- F2: projection section in AUA and NNA tooltips for current period
- \`8e9facd\` -- F2: project the last bar in dataset, not just the calendar-current period

**CTO's analysis was written against 9ce8d3b.** Three additional commits (28517dd, 2f84197, 8e9facd) landed after the analysis. These may partially address Flaws 3 and 4. ALL participants must read the CURRENT PartnerAnalytics.tsx source to verify which flaws remain before proposing solutions.

### 4 Flaws Identified (CTO Analysis Sections 3-6)

1. **AUA projection 0/0 regression** -- Delta-based formula produces zero ghost when no prior period exists in windowed data (e.g., Annually + 1Y window shows only current year, no prior to delta against).
2. **GRO chart unintelligible** -- No title, terse legend, raw tooltip, no hero metrics, Y-axis unlabeled, projection lines leak into tooltip.
3. **NNA/AUA tooltip projection format** -- Shows ghost increment "(add)" instead of full projected values. User must do mental math.
4. **GRO tooltip leaks _proj entries** -- Dashed projection lines rendered as separate Line series appear as duplicate rows in tooltip.

### 5 Convergence Questions (CTO Analysis Section 7)

1. **AUA projection 0/0 fix:** When no prior period in windowed data, what should happen? (a) no ghost, (b) fall back to raw data for prior reference, (c) "projection unavailable" indicator.
2. **GRO chart redesign:** Keep multi-line or convert? (a) keep lines + add hero/tooltip/label, (b) diverging bar like NNA, (c) stacked bar, (d) other.
3. **Projection tooltip format:** (a) ghost increments with "(add)", (b) full projected values with current parenthetical, (c) actual and projected as separate rows.
4. **GRO tooltip:** (a) structured rows with sign coloring, (b) include period-over-period, (c) show projection for current period, (d) all of the above.
5. **GRO hero metrics:** What to display below chart? Latest period Market/NNA/Total, cumulative, growth rate?

### Instructions per Participant

**CTO (1.0.0_SA_CTO) -- your turn first.**
You wrote the analysis. After reading the CURRENT source (not just your analysis), confirm which flaws remain and which the 3 newer commits addressed. Then state your architectural position on each of the 5 questions. Reference existing patterns from your Section 6 catalog to justify consistency.

**DE (0.4.0_DE_ClientPlatform):**
Read PartnerAnalytics.tsx and types.ts. For each convergence question, specify:
- What Recharts API patterns support the proposed solution (stackOffset, ReferenceLine, custom tooltip, etc.)
- Any TypeScript type implications (new interfaces, augmented data shapes)
- Data contract awareness: what fields exist in timeseries_chart.json growth_decomposition vs what needs to change

**RD (0.4.2_RD_AdvisorIntelligence):**
You built the current implementation. After reading the CTO analysis and the other participants' positions:
- Confirm implementation feasibility for each proposed solution
- Flag any Recharts constraints that would block a proposal
- Propose specific component structure (which Recharts components, props, data transformations)

### Self-unblock requirement (M11)

If you are uncertain about a field name, data shape, Recharts prop, or current code behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. You have tool access -- use it.

### Final turn must produce a structured contract block with:

- Exact projection formula for each view (AUA stock metric, NNA flow metric, GRO flow metric)
- Exact tooltip layout for each view (rows, labels, values, sign formatting)
- GRO chart type decision (line, bar, or hybrid) with component specification
- GRO hero metrics (what metrics, what format)
- Edge case handling (no prior period, period already complete, negative projections, short windows)
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
