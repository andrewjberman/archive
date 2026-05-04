#!/usr/bin/env bash
# run-ADHC_WAVPLN-001-wave-sequencing.sh
# CTO+COO joint thread — multi-project wave sequencing and agent dispatch plan
# Models: 1.0.0_SA_CTO=claude-sonnet-4-6, 2.0.0_SA_COO=gpt-5.5
# Run from repo root: bash org/threads/staging/run-ADHC_WAVPLN-001-wave-sequencing.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

PROJECT="ADHC_WAVPLN"
THREAD_ID=""
TOPIC="Wave sequencing and agent dispatch plan across all active projects"
CREATED_BY="1.0.0_SA_CTO"
PARTICIPANTS="1.0.0_SA_CTO,2.0.0_SA_COO"
MAX_TURNS=3
PARTICIPANT_MODELS='{"1.0.0_SA_CTO":"claude-sonnet-4-6","2.0.0_SA_COO":"gpt-5.5"}'

# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "documents": [
    {"label": "Project Registry — all active + completed projects", "path": "org/projects/REGISTRY.md"},
    {"label": "ADHC_WAVPLN project JSON", "path": "org/projects/ADHC_WAVPLN.json"},
    {"label": "ADVI_HISTBF project JSON", "path": "org/projects/ADVI_HISTBF.json"},
    {"label": "ADVI_INFLEC project JSON", "path": "org/projects/ADVI_INFLEC.json"},
    {"label": "ADVI_JWTRES project JSON", "path": "org/projects/ADVI_JWTRES.json"},
    {"label": "ADVI_ORIAPI project JSON", "path": "org/projects/ADVI_ORIAPI.json"},
    {"label": "ADVI_ROLLUP project JSON", "path": "org/projects/ADVI_ROLLUP.json"},
    {"label": "ADVI_INFLV2 project JSON", "path": "org/projects/ADVI_INFLV2.json"},
    {"label": "ADVI_INFSHIP project JSON", "path": "org/projects/ADVI_INFSHIP.json"},
    {"label": "ADHC_CLCOMM project JSON", "path": "org/projects/ADHC_CLCOMM.json"},
    {"label": "ADHC_OWNPTH project JSON", "path": "org/projects/ADHC_OWNPTH.json"},
    {"label": "TRSB_PATHFIX project JSON", "path": "org/projects/TRSB_PATHFIX.json"}
  ],
  "inline": "Thread ADHC_WAVPLN-001. CTO (1.0.0_SA_CTO) has done a full startup reconciliation and TO inventory sweep across all 10 active projects. CTO opens with the authoritative TO inventory table, cross-project dependency map, and key stale-document flags surfaced during reconciliation. COO reviews, corrects, adds any items from their concurrent session 54 sweep, then produces the deliverable: wave groups with agent assignments, gate conditions, and parallelization logic. CTO validates wave groups and flags any architectural concerns. COO closes with a finalised wave plan ready for Andrew to use as a spawn manifest."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message — written in the voice of 1.0.0_SA_CTO
# NOTE: heredoc is single-quoted to prevent dollar-sign expansion on currency
# figures ($197M, $429M etc). Timestamp is injected via a preceding echo.
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Write frontmatter with variable expansion
printf -- '---\nagent: 1.0.0_SA_CTO\nturn: 0\ntimestamp: %s\nsignal: continue\n---\n' "$TS" > "$OPENING_FILE"
# Append body as literal (no variable expansion — contains currency figures with $)
cat >> "$OPENING_FILE" << 'OPENING_EOF'

## Wave Planning — Full TO Inventory (CTO Session 4, 2026-05-01)

I am 1.0.0_SA_CTO. This is thread ADHC_WAVPLN-001 under project ADHC_WAVPLN. Andrew has asked us to produce a coordinated wave dispatch plan across all active projects so he can begin spawning agents immediately. Deliverable: wave groups (parallelizable where possible) with named agents, gate conditions, and sequencing rationale. I'll present the full TO inventory, flag stale document discoveries, then ask you to produce the plan.

---

## Active Projects (10)

ADVI_HISTBF, ADVI_INFLEC, ADVI_INFLV2, ADVI_INFSHIP, ADVI_JWTRES, ADVI_ORIAPI, ADVI_ROLLUP, ADHC_CLCOMM, ADHC_OWNPTH, TRSB_PATHFIX.

---

## Complete TO Inventory (CTO-verified 2026-05-01 Session 4)

### IN-FLIGHT (monitoring only; no new spawns needed)

| TO | Agent | Project | Notes |
|---|---|---|---|
| HISTBF.003 | 0.4.0_DS_ClientPlatform + 0.6.1_AE_PartnerETL | ADVI_HISTBF | EC2 inf-bronze-runner; run_backfill_orchestrator.py; dim order positions_mv->assets_v2->transactions->performance; AE 0.6.1 owns dispatch + CW monitoring |
| INFLV2.009 | 0.6.1_AE_PartnerETL | ADVI_INFLV2 | INFGRD.003 chain rerun; AE started 2026-04-29 13:43Z |
| INFLEC.ORNREN.001 | 0.4.0_DS_ClientPlatform | ADVI_INFLEC | DS orion script rename in flight |

### PENDING — gate-ready once trigger fires

| TO | Agent | Project | Gate | Spawn-ready? |
|---|---|---|---|---|
| HISTBF.004 | 0.4.0_DS_ClientPlatform | ADVI_HISTBF | HISTBF.003 RAVC4 | No — waiting .003 |
| HISTBF.005 | 0.4.0_DS_ClientPlatform | ADVI_HISTBF | HISTBF.003 RAVC4 | No — waiting .003 |
| HISTBF.006 | 0.4.0_DS_ClientPlatform | ADVI_HISTBF | HISTBF.003 RAVC4 | No — waiting .003 |
| INFLV2.010 | 0.4.2_RD_AdvisorIntelligence | ADVI_INFLV2 | INFLV2.009 completion | No — waiting .009 |
| INFSHIP.A2 | 0.6.1_AE_PartnerETL | ADVI_INFSHIP | DIAGFIX.012 Phase 5 RAVC4 | YES — GATE LIFTED (flag below) |
| ORIAPI 3-step close | 2.0.0_SA_COO authors | ADVI_ORIAPI | Cycle 2 clean (today 12:13Z UTC) | COO-authored post Cycle 2 confirm |
| JWTRES.002 Option B | COO authors; AE 0.7.0 executes | ADVI_JWTRES | Option A validation window | Not yet — HISTBF backfill is the real-world exercise |

### STAGED — no active gate; awaiting bandwidth or Andrew GO

| TO | Agent | Project | Notes |
|---|---|---|---|
| ROLLUP.SL-P1b | 0.4.0_DS_ClientPlatform | ADVI_ROLLUP | 3 consecutive nightly cleans from SL-P1; WP-10b observation active |
| ROLLUP.SL-P2 | 0.4.0_DS_ClientPlatform | ADVI_ROLLUP | Gates SL-P1b pass |
| ROLLUP.SL-P3 | 0.4.0_DS_ClientPlatform | ADVI_ROLLUP | Gates SL-P2 pass |
| ROLLUP.BDPLNNASCHEMA | 0.4.0_DS_ClientPlatform | ADVI_ROLLUP | 49EXEC TO 1+5+ORPHRELID gate (all complete per registry) — COO confirm |
| CLCOMM.TO-3 | 0.5.0_AE_OpalETL | ADHC_CLCOMM | Andrew smoke-test gate (fresh feature_clb session needed) |
| CLCOMM.TO-4 | COO authors | ADHC_CLCOMM | Gates CLCOMM.TO-3 PASS |
| INFLEC.ORNREN.003 | 0.4.0_DS_ClientPlatform | ADVI_INFLEC | Andrew-activated (Option B + divergence rule locked 2026-04-30 PM) |
| INFLEC.Q10 | 0.4.0_DS_ClientPlatform | ADVI_INFLEC | staged-low; investigation-only |

### STUCK — escalation pending Andrew

| TO | Agent | Project | Status |
|---|---|---|---|
| TRSB_PATHFIX.TO-2 | 0.3.0_DT_TradingOperations | TRSB_PATHFIX | STUCK — GO sent 2026-04-30 12:37Z; DT last log 2026-03-05; no commit. Escalated to COO via RAVC2; COO ACKed, surfacing to Andrew for spawn/reassign. On RAVC4: project closeable. |

### TO-BE-AUTHORED (post external trigger)

| Item | Author | Trigger |
|---|---|---|
| JWTRES.002 Option B | 2.0.0_SA_COO | Andrew signals validation window sufficient |
| ADHC_OWNPTH project close | 1.0.0_SA_CTO | 9/9 TOs complete (flag below) — closeable now |

### COMPLETE (confirmed this session — not in wave plan)

INFLV2.002 (cbc4f2713), INFLEC.DIAGFIX.012 (RAVC4 2026-04-30T18:35Z), INFLEC.ORNREN.002 (AE dispatch done), INFLEC.Q8, INFLEC.Q9, INFLEC.W4.14 (superseded), ADHC_OWNPTH.009

---

## Stale Document Flags (CTO-surfaced)

**FLAG 1 — INFSHIP.A2 gate is lifted:**
ADVI_INFSHIP Blocking column says "Phase 0a DS BASE consult gated on DIAGFIX.012 Phase 5 RAVC4." DIAGFIX.012 Phase 5 RAVC4 delivered 2026-04-30T18:35Z (all comp-validate PASS). Gate is cleared. ADVI_INFSHIP.A2 (AE 0.6.1 Orion Asset API vendor investigation) is spawn-ready now.

**FLAG 2 — ADHC_OWNPTH is 9/9 complete:**
REGISTRY says "8 of 9 TOs COMPLETE / TO 9 STAGED-LOW." ADHC_OWNPTH.009 XML status = complete. 9/9 done. Project is closeable today.

**FLAG 3 — ADVI_JWTRES Blocking column is stale:**
Blocking says "Andrew + COO joint sequencing in flight." Andrew's actual ruling: "Option A -> validate -> Option B; standalone project." Non-blocking for wave plan.

---

## Agent/Org Constraints

- 0.4.0_DS_ClientPlatform: .003 in-flight + 4 staged (HISTBF .004/.005/.006 + ORNREN.003 + Q10 + ROLLUP TOs). This is the primary bandwidth bottleneck.
- 0.6.1_AE_PartnerETL: .003 monitoring + .009 in-flight + INFSHIP.A2 newly unblocked.
- 0.3.0_DT_TradingOperations: stuck agent — no new assignments until Andrew resolves spawn/reassign.
- 0.5.0_AE_OpalETL: CLCOMM.TO-3 staged (Andrew gate).
- 0.4.2_RD_AdvisorIntelligence: INFLV2.010 staged (gates .009).

---

## Request to COO

Please (1) correct or add anything from your concurrent session 54 sweep I may have missed, then (2) produce the wave plan with:

- **Wave groups** — parallel TOs in same wave; serialized TOs in later waves
- **Agent assignments** — named serial per TO
- **Gate conditions** — what event starts each wave
- **DS bandwidth sequencing** — DS 0.4.0 is the bottleneck; call out how you manage the HISTBF silver wave vs ROLLUP staged TOs

Deliverable format: numbered wave table Andrew can use as a spawn manifest, plus 2-3 sentences on key serializations.
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

# Resolve thread ID from project counter (assigned by create-thread.sh)
if [ -z "$THREAD_ID" ] && [ -n "$PROJECT" ]; then
  JQ="${REPO_ROOT}/.tools/jq.exe"
  PROJECT_FILE="${REPO_ROOT}/org/projects/${PROJECT}.json"
  COUNTER=$("$JQ" -r '.thread_counter' "$PROJECT_FILE")
  SERIAL="${PROJECT}-$(printf '%03d' "$COUNTER")"
  TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-40 | sed 's/-$//')
  THREAD_ID="${SERIAL}-${TOPIC_SLUG}"
fi

echo ""
echo "Running orchestrator on: ${THREAD_ID}"
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --participant-models "$PARTICIPANT_MODELS" \
  --anthropic-secret  anthropic-api-key \
  --openai-secret     openai-api-key \
  --verbose
