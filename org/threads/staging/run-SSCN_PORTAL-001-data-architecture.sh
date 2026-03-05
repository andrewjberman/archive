#!/usr/bin/env bash
# run-SSCN_PORTAL-001-data-architecture.sh
#
# Pattern 0: Security Scanner data architecture alignment
# Goal: DS + AE + DE agree on data storage, API shape, refresh cadence,
#       and client-side vs server-side percentile scoring BEFORE any code is written.
# Principal context: XLSM audit (full workbook structure + VBA) + PRD + V0 Python scripts
# Participants: DS -> AE -> DE (round_robin, gpt-5.2, tools ON)
# Deliverable: Agreed JSON shapes, S3 key structure, API endpoints, TypeScript interface names.
#              DS closes with a concrete data contract block that DE can type against.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="SSCN_PORTAL"
THREAD_ID=""              # auto-assigned (SSCN_PORTAL-001)
TOPIC="Pattern 0: Security Scanner data architecture -- pipeline storage API shape"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.3.0_DS_TradingOperations,0.5.0_AE_OpalETL,0.3.0_DE_TradingOperations"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context (M1 + M4)
# XLSM audit is the principal context piece per CTO methodology.
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Factor Scanner V0 -- primary Python pipeline script (percentile logic, universe mapping, data columns)",
      "path": "docs/architecture/security-scanner-source/V0_quick_update_weights.py"
    },
    {
      "label": "Yang pipeline Terraform -- reference S3-backed Lambda architecture pattern",
      "path": "infra/aws/terraform/yang-pipeline/main.tf"
    },
    {
      "label": "DS TradingOperations data contract -- existing pod data patterns",
      "path": "org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml"
    }
  ],
  "documents": [
    {
      "label": "Security Scanner PRD -- full portal spec (tabs, scoring algorithm, universes, existing patterns to reuse)",
      "path": "docs/architecture/SECURITY_SCANNER_PRD.md"
    },
    {
      "label": "XLSM Audit -- full Factor_Scanning_Model.xlsm structure: sheet dimensions, header rows, data validation, conditional formatting, formulas, factor metadata (Tab 3), and complete VBA source (Worksheet_Calculate, Worksheet_Change)",
      "path": "docs/architecture/SECURITY_SCANNER_XLSM_AUDIT_COMPACT.md"
    },
    {
      "label": "Factor Scanner V0 system reference -- workflow, file structure, data sources, universe column mapping",
      "path": "docs/architecture/security-scanner-source/V0_SYSTEM_REFERENCE.md"
    }
  ],
  "inline": "This is a Pattern 0 pre-implementation alignment thread for the Security Scanner portal page (SSCN_PORTAL). The goal is for DS, AE, and DE to agree on the data architecture BEFORE anyone writes portal code.\n\nThe Security Scanner is a port of Yang's Factor_Scanning_Model.xlsm to the portal. Source data is a monthly FactSet Excel export (~3000 securities x 255 factors, 6 universe weight columns). The XLSM audit file is the principal context -- it contains the full workbook structure including all VBA logic, factor metadata, formulas, and conditional formatting that must be replicated in the portal.\n\nFour key decisions must be resolved in this thread:\n1. DATA STORAGE: Static JSON in S3 (pre-processed monthly) vs Lambda-computed on demand\n2. PERCENTILE SCORING: Pre-computed server-side (in a processing Lambda) vs computed client-side in the browser\n3. S3 KEY STRUCTURE: How does monthly FactSet data flow from upload to portal-consumable JSON?\n4. API ENDPOINT STRUCTURE: Path, authentication (/api/private vs /api/general), and shape for each of the 4 tabs\n\nDS is the knowledge source for what the FactSet data contains and what the pipeline must produce. AE is the knowledge source for AWS infrastructure decisions (S3, Lambda, EventBridge, IAM). DE is the knowledge receiver who will wire the TypeScript interface and API calls.\n\nThread output must be a concrete data contract: specific S3 key patterns, exact JSON shapes per endpoint, TypeScript interface names, and a refresh schedule. Vague answers are not acceptable -- every answer must cite a specific file, resource name, or column name from the context."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO voice, DS goes first)
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

## Pattern 0 Alignment -- Security Scanner Data Architecture

I am the COO convening this alignment thread. The Security Scanner PRD is authored and the RD agent (0.3.4_RD_SecurityScanner) is standing by. Before DE wires an endpoint or RD builds a single component, DS, AE, and DE must agree on the data architecture.

**Context available to you all:**
- XLSM audit (principal context): full Factor_Scanning_Model.xlsm structure -- VBA source, formulas, factor metadata (Tab 3), data validation, conditional formatting
- V0 Python scripts: quick_update_weights.py shows the current percentile calculation logic and data column mapping
- PRD: full portal spec at docs/architecture/SECURITY_SCANNER_PRD.md

**Turn order:** DS -> AE -> DE (round_robin). Three turns per agent. DE writes the final data contract on their last turn.

---

**DS (0.3.0_DS_TradingOperations) -- your turn first.**

Read quick_update_weights.py, V0_SYSTEM_REFERENCE.md, and the XLSM audit from context. Then answer:

**1. Source data inventory:**
- What columns does Screening_DIVZ_IDVZ_20251028.xlsx contain? Name the exact column headers for: ticker, company name, market value, country, sector, industry group, and at least 5 factor columns (use the actual column names from the source data file, e.g. \`mkt_val\`, \`ticker\`, etc.).
- What are the 6 universe weight columns and their exact names? (e.g. \`wt_ivv\` for S&P 500)
- How large is the dataset? Rows per universe (approximate) and total factor columns.

**2. Percentile calculation commitment:**
- The current V0 script computes percentiles server-side in Python (\`rank(pct=True, method='average') * 100\`). For the portal, should this be: (a) pre-computed in a processing Lambda when data arrives and stored in S3 as JSON, OR (b) computed client-side in the browser from raw factor values?
- State which you recommend and why, citing data size (rows x factors x 6 universes).

**3. Proposed S3 output shape:**
For each of the 4 portal tabs, propose what JSON you would produce:
- Tab 1 (Factor Bank): factor metadata -- what fields per factor? (code, name, category, relationship, IC, autocorrelation, coverage, systematic_flag)
- Tab 2 (Universe Data): per-universe security table -- what shape? Separate JSON per universe?
- Tab 3 (Factor Data): static factor reference -- same as Tab 1 metadata?
- Tab 4 (Universe Scanner): per-universe pre-scored securities -- what fields? Does composite score go in the JSON or is it computed client-side from weights?

**4. Refresh cadence:**
- How does the monthly FactSet Excel file arrive? (S3 upload trigger? Manual upload?)
- What triggers the processing pipeline? (S3 event? EventBridge schedule?)

**IMPORTANT (M2):** Anchor every answer to a specific column name, function name, or file. If you say a field exists, name the exact column from the source data (check quick_update_weights.py's column references). Do not describe a field without citing its source column.

**IMPORTANT (M11):** If you are uncertain about a column name, date range, or file location -- use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.

---

**AE (0.5.0_AE_OpalETL) -- after DS:**

Review DS's proposed data shape and answer:

1. **Storage decision:** Static JSON in S3 (pre-processed monthly, served via CloudFront) vs Lambda-computed on demand. Recommend one and explain the tradeoffs for a ~3000-security, 255-factor dataset.
2. **S3 key structure:** Propose exact S3 key patterns for each artifact (factor metadata, per-universe security data, pre-scored securities). Use the opal-data-portal-v2 bucket convention.
3. **Processing Lambda design:** If pre-compute is chosen -- what does the Lambda do? When does it trigger? (S3 event on FactSet file upload?) What memory/timeout is appropriate for a pandas percentile operation on ~3000 x 255?
4. **API endpoint structure:** The PRD asks whether to use \`/api/private/security-scanner/...\` or \`/api/general/...\`. Which auth model is appropriate? Name the existing Lambda authorizer and how it passes firmId.
5. **CloudFront:** Does pre-computed data need a CloudFront invalidation on monthly refresh? Which distribution?

Anchor every answer to an existing AWS resource name or Terraform file where applicable. Reference yang-pipeline/main.tf patterns where the architecture is analogous.

---

**DE (0.3.0_DE_TradingOperations) -- final turn (CRITICAL):**

Review DS's data shape and AE's infrastructure decisions. Then produce:

**1. TypeScript interface definitions** (name each interface):
- \`FactorDefinition\` (fields: code, name, category, relationship, ic, autocorrelation, coverage, systematic_flag -- map to exact JSON keys DS proposed)
- \`SecurityRow\` (fields for Tab 2/Tab 4: ticker, name, mkt_val, country?, sector, industry_group, factor scores/values)
- \`UniverseScannerRow\` (Tab 4: rank, ticker, name, composite_score, mkt_val, country?, industry_group, per-factor percentile scores and raw values)
- Any additional interfaces for the API response envelope

**2. API endpoint contract:**
- Exact paths for each fetch (e.g. \`/api/private/security-scanner/factors\`, \`/api/private/security-scanner/universe/{universeId}\`)
- Query parameters needed
- Authentication: private API with firmId context or general API?

**3. Client-side vs server-side decision confirmation:**
- Confirm the percentile/composite score approach agreed with DS and AE
- State what the portal computes vs what comes pre-computed in the JSON

**4. Confirmed data contract block:**
Write a structured summary in this format:
\`\`\`
SSCN_PORTAL DATA CONTRACT -- SSCN_PORTAL-001
Endpoint 1: GET /api/.../factors
  Response shape: { factors: FactorDefinition[] }
  S3 key: ...
  Refresh: monthly

Endpoint 2: GET /api/.../universe/{universeId}
  Response shape: { securities: SecurityRow[] }
  S3 key: ...
  Refresh: monthly

Percentile computation: client-side | server-side (pre-computed)
TypeScript interfaces: FactorDefinition, SecurityRow, UniverseScannerRow (in types.ts)
\`\`\`
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
