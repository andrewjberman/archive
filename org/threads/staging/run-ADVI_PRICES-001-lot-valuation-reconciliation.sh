#!/usr/bin/env bash
# run-ADVI_PRICES-001-lot-valuation-reconciliation.sh
# Pattern 2: Technical gap investigation
# DS + AE + DT investigating $68M net divergence between lot MV and BD silver AUA
#
# Run from repo root: bash org/threads/staging/run-ADVI_PRICES-001-lot-valuation-reconciliation.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_PRICES"
THREAD_ID=""
TOPIC="Lot Valuation Reconciliation Investigation"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.6.0_AE_PartnerETL,0.4.0_DT_ClientPlatform"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context -- source files and briefing
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Gold: build holdings_lots (FIFO lot reconstruction)",
      "path": "data/black_diamond/scripts/gold/03_build_holdings_lots.py"
    },
    {
      "label": "Gold: build positions cube",
      "path": "data/black_diamond/scripts/gold/02_build_positions_cube.py"
    },
    {
      "label": "Gold: build accounts dimension",
      "path": "data/black_diamond/scripts/gold/00_build_accounts_dimension.py"
    },
    {
      "label": "Silver: merge daily allocation incremental",
      "path": "data/black_diamond/scripts/silver/merge-daily-allocation-incremental.py"
    },
    {
      "label": "Silver: inject scoped price overrides",
      "path": "data/black_diamond/scripts/silver/inject_scoped_overrides.py"
    },
    {
      "label": "Silver: BD price update",
      "path": "data/black_diamond/scripts/silver/bd_price_update.py"
    },
    {
      "label": "Gold: validate AUA vs silver",
      "path": "data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py"
    },
    {
      "label": "Gold: run_gold_layer.sh",
      "path": "data/black_diamond/scripts/gold/run_gold_layer.sh"
    },
    {
      "label": "Bronze: convert daily allocation to parquet",
      "path": "data/black_diamond/scripts/bronze/convert_daily_allocation_to_parquet.py"
    }
  ],
  "inline": "INVESTIGATION THREAD: BD lot-level valuation reconciliation.\n\nGOAL: Identify every systematic driver of the $68M net gap ($211M over / $143M under) between our gold holdings_lots market_value and BD silver allocations account_market_value, then design programmatic fixes.\n\nROLES:\n- DS (0.4.0_DS_ClientPlatform) is the KNOWLEDGE SOURCE on lot reconstruction logic, pricing, and the FIFO algorithm in 03_build_holdings_lots.py. DS also owns 05c_validate_aua_vs_silver.py.\n- AE (0.6.0_AE_PartnerETL) is the KNOWLEDGE SOURCE on the silver ingestion pipeline, S3 data layout, EC2 execution, and what BD actually sends in the daily feeds.\n- DT (0.4.0_DT_ClientPlatform) is the KNOWLEDGE SOURCE on deployment state, Lambda configurations, and any Terraform-managed infrastructure involved in pricing or valuation.\n\nDELIVERABLE: A ranked list of divergence root causes with proposed fixes, estimated impact per cause, and the data/code changes required. This will become the input for COO task order decomposition.\n\nCRITICAL CONTEXT (from COO session 2026-03-23):\n\nThe COO ran a full reconciliation of the 2026-03-19 silver allocations ($1.593B, 6,415 accounts) against the 2026-03-20 gold holdings_lots (401,063 open lots across 7,791 accounts, limited to silver-overlapping accounts: $1.662B across 5,998 accounts).\n\nNET GAP: +$68.2M (lot MV exceeds BD AUA by 4.3%)\n\nBut the NET understates the problem. The GROSS picture:\n- 2,574 accounts where lot MV EXCEEDS BD AUA: +$211M total overshoot\n- 3,778 accounts where lot MV is LESS than BD AUA: -$143M total undershoot\n- These partially offset to the $68M net, but both directions need explanation.\n\nWATERFALL DECOMPOSITION (COO analysis):\n\n1. PHANTOM LOTS (+$74M, 271 accounts): Our lot MV is >2x BD's reported AUA. Worst case: z0819189891 has a single BNP Paribas lot at $20.8M but BD says the account is $1.9M. Account z0821392551 has $7.5M in ETFs but BD reports $3K. These are likely stale lots our FIFO thinks are open but BD has closed/transferred.\n\n2. MISSING LOTS (-$27M, 146 accounts): BD reports AUA but we have $0 in lots. 30 are Bank accounts, 11 Savings, 7 'No Type Assigned', 5 Insurance. These are likely held-away or non-tradeable assets BD tracks at account level but doesn't include in the transaction feed.\n\n3. INSURANCE/ANNUITY SHORTFALL (-$8M, 96 accounts): BD reports policy value but underlying sub-account holdings aren't fully visible in transactions. Opaque wrappers.\n\n4. NON-INVESTMENT ACCOUNTS (+$2M, 103 accounts): Bank, Savings, CreditCard, Loans, Mortgage, TermLife. Noise.\n\n5. NORMAL ACCOUNTS NET (+$11M, 5,534 accounts): Median divergence -0.4%, mean +0.9%. The net positive comes from a fat right tail:\n   - 992 accounts overshoot by >20% (+$97M). Heavily IRA-concentrated (535 of 992). Top securities are standard ETFs (Pathfinder, IDVZ, VTV, IEFA, JEPI). Hypothesis: DRIP lots that our FIFO creates but BD nets into parent position.\n   - 473 accounts undershoot by >20% (-$57M). Corporate accounts disproportionate (-$9.7M from 8 accounts). Hypothesis: advisory fee deductions or billings that reduce BD-reported AUA without appearing as exit transactions.\n\nQUESTIONS FOR DS:\n1. In 03_build_holdings_lots.py, how does the FIFO algorithm handle dividend reinvestment (DRIP) transactions? Does it create a new lot per reinvestment? Could this inflate lot count and MV relative to BD's position-level reporting?\n2. What exit transaction types does the FIFO algorithm recognize? Is there a type for transfers-out, journal entries, or corporate actions (mergers, spinoffs) that would zero a position?\n3. The 05c_validate_aua_vs_silver.py script exists — what does it currently check? Does it flag the per-account divergences we're seeing?\n4. How are prices assigned to lots? Is current_price from a daily feed, or is it the last-known price from a transaction? Could stale pricing explain the overshoots on large accounts?\n\nQUESTIONS FOR AE:\n1. What does the daily BD allocation feed contain vs the transaction feed? Does the allocation feed have position-level detail or only account-level totals?\n2. What is the S3 layout for silver allocations vs silver transactions? How far back do we have daily snapshots?\n3. Are there known gaps in the transaction feed — transaction types BD sends that we ignore or don't parse?\n4. For the 146 accounts with $0 lots: is it possible BD sends allocation data for accounts that have NO transaction history in our feed?\n\nQUESTIONS FOR DT:\n1. Are there any scheduled jobs or Lambda functions involved in pricing updates for the gold layer?\n2. Is the silver-to-gold pipeline fully automated or does it require manual triggers?\n3. What's the deployment state of the price override / scoped override system?\n\nSelf-unblock requirement: If you are uncertain about a data field, date range, output shape, or script behavior, use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- written in the voice of COO
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$OPENING_FILE" << OPENING_EOF
---
agent: 2.0.0_SA_COO
turn: 0
timestamp: ${TS}
signal: continue
---

## Lot Valuation Reconciliation — COO Investigation Brief

I'm 2.0.0_SA_COO. I've just completed a full reconciliation of our gold holdings_lots market values against BD's silver allocations (the official AUA source of truth). The results show a systematic divergence that we need to diagnose and fix.

### The Problem

**BD says our AUA is \$1.593B. Our lot reconstruction says \$1.662B for the same accounts. That's a \$68M net gap (+4.3%).**

But the net masks the real issue. The gross picture:
- **2,574 accounts** where our lots EXCEED BD's AUA by **\$211M** total
- **3,778 accounts** where our lots FALL SHORT of BD's AUA by **\$143M** total

Both directions need explanation. Here's what I've decomposed so far:

### Waterfall

| Category | Amount | Accounts | Hypothesis |
|----------|--------|----------|------------|
| Phantom lots (our MV > 2x BD) | +\$74M | 271 | Stale lots FIFO thinks are open but BD has closed. Worst: BNP Paribas \$20.8M lot in a \$1.9M account. |
| Missing lots (BD has AUA, we have \$0) | -\$27M | 146 | Held-away assets, bank accounts, non-tradeable positions BD tracks but doesn't send in transaction feed. |
| Insurance/annuity shortfall | -\$8M | 96 | Opaque wrappers — BD reports policy value but sub-account holdings not in transaction feed. |
| Non-investment accounts | +\$2M | 103 | Bank, Savings, Loan, Mortgage, CreditCard, TermLife. Noise. |
| Normal accounts (>20% overshoot) | +\$97M | 992 | DRIP lot inflation? 535 are IRAs. Top securities are standard ETFs (Pathfinder, IDVZ, VTV, IEFA, JEPI). |
| Normal accounts (>20% undershoot) | -\$57M | 473 | Fee deductions? Corporate accounts disproportionate (\$9.7M from 8 accounts). |
| Normal accounts (within 20%) | -\$29M | 4,069 | Pricing lag (silver=03-19, lots=03-20) + normal pricing variance. Median -0.4%. |

### What I Need From Each of You

**DS:** You own the FIFO algorithm in \`03_build_holdings_lots.py\` and the validation script \`05c_validate_aua_vs_silver.py\`. I need you to:
1. Explain how DRIP transactions are handled — do they create new lots? Could this inflate MV vs BD's position-level view?
2. Identify what exit transaction types the FIFO recognizes. Are transfers-out and corporate actions covered?
3. Describe what \`05c_validate_aua_vs_silver.py\` currently checks and whether it flags per-account divergences.
4. Explain the pricing model — where does \`current_price\` come from for each lot?

**AE:** You own the silver ingestion pipeline and EC2 execution. I need you to:
1. Describe what BD actually sends in the allocation feed vs the transaction feed. Is the allocation feed account-level only?
2. Identify any known gaps in the transaction feed — types we ignore or don't parse.
3. Explain whether the 146 accounts with \$0 lots could be allocation-only accounts (no transaction history).
4. Describe the S3 data layout and how far back we have daily snapshots.

**DT:** You own deployment state. I need you to:
1. Confirm the deployment state of the pricing pipeline — are price overrides, silver-to-gold automation, and daily scheduling all operational?
2. Identify any Lambda or scheduled jobs involved in pricing that could affect lot valuation.

Read the injected source files. Use tools to read additional files as needed. Do NOT speculate on behavior you can verify by reading code. Every answer must cite a file path and line number.

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close with a caveat that file inspection would answer.
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
