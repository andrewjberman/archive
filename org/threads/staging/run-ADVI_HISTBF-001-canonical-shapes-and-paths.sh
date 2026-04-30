#!/usr/bin/env bash
# ADVI_HISTBF-001 -- Canonical S3 paths and IAM alignment post-DS~B refactor
#
# Roundtable: DS (0.4.0_DS_ClientPlatform, owns both the orchestrator and the
# DS~B refactor) + AE 0.6.1 (IAM owner). Goal: lock the canonical path registry
# before Wave B execution so EC2 does not 403 and gold consumers do not miss silver.
#
# Run from repo root: bash org/threads/staging/run-ADVI_HISTBF-001-canonical-shapes-and-paths.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_HISTBF"
THREAD_ID=""
TOPIC="Canonical S3 paths and IAM alignment post-DS~B refactor"
CREATED_BY="1.0.0_SA_CTO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.6.0_AE_PartnerETL"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context -- source files injected per M1 (inject actual code, not summaries)
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Bronze pull -- positions_mv (DS~B refactored; check bronze_key near end of main())",
      "path": "data/orion/manual_api/pull_inflection_positions_daily.py"
    },
    {
      "label": "Bronze pull -- assets_v2 (DS~B refactored; check bronze_key near end of main())",
      "path": "data/orion/manual_api/pull_inflection_assets_v2.py"
    },
    {
      "label": "Bronze pull -- transactions (DS~D authored; output path in docstring line 21)",
      "path": "data/orion/manual_api/pull_inflection_transactions_rest.py"
    },
    {
      "label": "Bronze pull -- performance (DS~D authored; output path in docstring line 20)",
      "path": "data/orion/manual_api/pull_inflection_performance_rest.py"
    },
    {
      "label": "Silver builder -- assets_v2 (DS~B refactored; BRONZE_KEY_TPL + SILVER_KEY_TPL constants at top)",
      "path": "data/orion/scripts/silver/convert_assets_v2_to_silver.py"
    },
    {
      "label": "Silver builder -- transactions (DS~B refactored; BRONZE_PREFIX + SILVER_PREFIX at top)",
      "path": "data/orion/scripts/silver/convert_transactions_to_silver.py"
    },
    {
      "label": "Silver builder -- performance (DS~B refactored; BRONZE_PREFIX + SILVER_PREFIX at top)",
      "path": "data/orion/scripts/silver/convert_performance_to_silver.py"
    },
    {
      "label": "Silver builder -- positions_mv dispatcher (DS~B refactored convert_orion_api_to_silver.py)",
      "path": "data/orion/scripts/silver/convert_orion_api_to_silver.py"
    },
    {
      "label": "Silver backfill runner (DS~B; BRONZE_KEY_TEMPLATES + SILVER_KEY_TEMPLATES are the path registry; SILVER_BUILDER_CMDS shows what scripts are called)",
      "path": "data/orion/scripts/silver/run_silver_backfill.py"
    },
    {
      "label": "Multi-dim backfill orchestrator (DS BASE; STATE_KEY_FMT + DimSpec list; scripts_dir set to its own directory)",
      "path": "data/orion/manual_api/run_backfill_orchestrator.py"
    },
    {
      "label": "Gold consumer INF_B_00 (reads POSITIONS_MV_PREFIX = silver/positions_mv/; check lines 60-65)",
      "path": "data/orion/scripts/gold/INF_B_00.canonical_holdings.py"
    },
    {
      "label": "Gold consumer INF_I_D03 (reads silver/assets_v2/YYYY-MM-DD.parquet for asset classification)",
      "path": "data/orion/scripts/gold/INF_I_D03.composition_artifacts.py"
    },
    {
      "label": "AE IAM -- inf-bronze-runner EC2 (WriteBronze Sid covers bronze/orion-api/* and bronze/orion-api-v2/* only; check aws_iam_role_policy.inf_bronze_runner_s3)",
      "path": "infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf"
    }
  ],
  "documents": [
    {
      "label": "AE 0.6.1 Wave 1 IAM session log — shows what WriteBronze Sid covers and what was explicitly NOT in scope (CW, SM, rate-state only; no new bronze path grants)",
      "path": "org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-04-30/histbf002b_jwtres001b_iam_alarms_dashboard.md"
    },
    {
      "label": "AE 0.6.1 Wave 2 orchestrator pre-flight log — notes 8 DS pull_inflection_*.py files were staged by DS lane during this session, confirming DS~B path refactor was in-flight concurrently",
      "path": "org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-04-30/histbf002b_jwtres001b_wave2_orchestrator_preflight.md"
    },
    {
      "label": "AE 0.6.1 CTO briefing deliverable — original silver path expectations (Hive-style) and dim scope; AE's pre-refactor mental model of bronze/silver layout",
      "path": "org/tier2_senior/0.6.1_AE_PartnerETL/deliverables/CTO_BRIEFING_INFLEC_HISTBACKFILL_AND_JWT_RESILIENCE_20260430.md"
    }
  ],
  "inline": "CTO-called roundtable for ADVI_HISTBF Wave B pre-flight. DS~B (tilde-lane of 0.4.0_DS_ClientPlatform) recently refactored Inflection bronze/silver S3 paths from Hive-style to BD-pattern flat layout. The backfill orchestrator (DS BASE = same agent serial, committed before DS~B refactor) and the AE IAM policy (committed independently by 0.6.1_AE_PartnerETL, whose session logs are injected) may not be aligned to the new paths. AE 0.6.1's Wave 1 IAM session log is critical context: it shows the IAM grants made that session (CW namespaces, SM grant, rate-state S3) and confirms WriteBronze was not touched in that wave. AE 0.6.1's Wave 2 log notes 8 DS pull_inflection_*.py files were staged by DS~B concurrently, confirming the refactor was in-flight while AE worked. The participant serial is 0.6.0_AE_PartnerETL (routing alias for the 0.6.1 knowledge domain — same agent, same IAM ownership). This thread must produce a locked canonical path table for all 4 dims and a specific Terraform patch plan before Wave B begins. DS answers Q1-Q6 (path table + orchestrator alignment). AE answers Q7-Q9 (IAM gap + patch plan). Third turn is DS synthesis."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- single-quoted heredoc to prevent bash backtick expansion;
# envsubst handles only the two shell variable substitutions we need.
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
export _CTO_AGENT="$CREATED_BY"
export _CTO_TS="$TS"

cat << 'OPENING_EOF' | envsubst '${_CTO_AGENT}${_CTO_TS}' > "$OPENING_FILE"
---
agent: ${_CTO_AGENT}
turn: 0
timestamp: ${_CTO_TS}
signal: continue
---

## Why this thread exists

DS~B (tilde-lane of 0.4.0_DS_ClientPlatform) refactored Inflection bronze/silver S3
paths from Hive-style layout to BD-pattern flat layout. Two things were committed on
independent timelines that may not be aligned:

1. The multi-dim backfill orchestrator (run_backfill_orchestrator.py) was authored by
   DS BASE at ~15:38 UTC, before DS~B landed the refactor at ~16:05-16:15 UTC.
2. The AE IAM policy (inf-bronze-runner.tf WriteBronze Sid) was expanded to cover
   bronze/orion-api-v2/* before DS~B changed the output paths.

Before Wave B execution begins, we need a locked canonical path table and a list of
every misalignment that would produce a runtime S3 403 or a gold consumer read miss.

My pre-read observations (verify by reading the files yourself -- do not take as
authoritative, I may have misread):

- pull_inflection_assets_v2.py CODE writes to bronze/assets/{date}.parquet but the
  MODULE DOCSTRING still says bronze/orion-api-v2/{snap_iso}/assets.parquet. Code
  is right; docstring is stale.
- pull_inflection_positions_daily.py CODE writes to bronze/positions/{date}.parquet
  but DOCSTRING still says bronze/orion-api-v2/{snap_iso}/positions.parquet.
- convert_assets_v2_to_silver.py writes to silver/assets_v2/{date}.parquet (code
  looks correct). Docstring says old Hive path.
- inf-bronze-runner.tf WriteBronze Sid covers bronze/orion-api/* and
  bronze/orion-api-v2/* ONLY -- does NOT cover bronze/positions/*, bronze/assets/*,
  bronze/transactions/*, bronze/performance/*.
- INF_B_00.canonical_holdings.py reads from POSITIONS_MV_PREFIX = 'silver/positions_mv/'
  but run_silver_backfill.py calls convert_orion_api_to_silver.py to produce
  positions_mv silver. It is unclear whether that script writes to
  silver/positions_mv/{date}.parquet or the old Hive path.

## Questions for DS (Turn 1 -- answer all before AE speaks)

Q1 -- Canonical path table. Read your refactored scripts and run_silver_backfill.py.
State the exact S3 key pattern (not the prefix, the full key template with extension)
for every dim, both bronze and silver. Use exact string literals from the code:

  Dim          | Bronze key (written by pull script) | Silver key (written by silver builder)
  -------------|--------------------------------------|---------------------------------------
  positions_mv | ?                                   | ?
  assets_v2    | ?                                   | ?
  transactions | ?                                   | ?
  performance  | ?                                   | ?

Q2 -- positions_mv silver builder. run_silver_backfill.py calls
convert_orion_api_to_silver.py with --dim positions_mv --upload. Read
convert_orion_api_to_silver.py and find the exact S3 key it writes for
--dim positions_mv. Does it match SILVER_KEY_TEMPLATES["positions_mv"] in
run_silver_backfill.py? If not, which is authoritative and what must be patched?

Q3 -- Stale docstrings. List every module-level docstring in files you touched that
still references an old path (orion-api-v2, api_dims, orion-rest). These must be
patched before Wave B ships so the next agent reading these files is not misled.

Q4 -- Silver IAM surface. Do the silver converters run on the inf-bronze-runner EC2
(using the EC2 IAM role) or on a separate Lambda during the backfill? If EC2, is
there a silver/* PutObject grant in inf-bronze-runner.tf? If Lambda, name it.

Q5 -- Orchestrator scripts_dir. The orchestrator sets scripts_dir to its own
directory (data/orion/manual_api/). Confirm: are pull_inflection_transactions_rest.py
and pull_inflection_performance_rest.py in that same directory? And are the --upload
flags the orchestrator passes the correct flag names in those scripts?

Q6 -- State key alignment. The orchestrator uses STATE_KEY_FMT =
"orion/rate_limit_state_{dim_name}.json". List the dim_name= values passed to
AdaptiveRateLimiter in each pull script and verify they match the dim names in
BACKFILL_DIMS so per-dim state files are consistent.

## Questions for AE 0.6.1 (Turn 2)

Q7 -- IAM gap. Read inf-bronze-runner.tf WriteBronze Sid. List every bronze/* path
prefix the policy currently covers. Then list the bronze output paths DS confirmed in
Q1. State explicitly which new paths are NOT covered and what must be patched.

Q8 -- Silver write IAM. If DS confirms (Q4) that silver converters run on the
inf-bronze-runner EC2 during the backfill, list the silver/* prefixes that need
s3:PutObject grants in the EC2 IAM policy and confirm whether they are present.

Q9 -- Patch plan. State the exact Terraform change needed: resource name, Sid,
new Resource ARN list. Do not say "add a policy" -- name the specific
aws_iam_role_policy resource and the exact ARN strings to add. If multiple Sids
need changes, list each one. Patch must be safe to apply before Wave B starts.

## DS synthesis (Turn 3)

After hearing AE's patch plan in Turn 2, DS provides the locked canonical path
table (complete Q1 answers, confirmed) and states: (a) which docstrings need patches
before Wave B, (b) whether the orchestrator needs any code changes, (c) whether
positions_mv silver chain is coherent end-to-end. This is the thread deliverable.

## Self-unblock requirement

If any answer requires reading a file to verify, read it. Do not close with
"would need to check" -- check now. The one acceptable caveat is live S3 key
existence (requires a runtime query). Everything else is in-repo.
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

echo "Scaffolding thread ADVI_HISTBF-001..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve assigned thread ID from project JSON
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
