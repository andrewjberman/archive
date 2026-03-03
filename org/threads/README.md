# Agent Thread System -- Round-Robin Conversation Protocol

## BEFORE YOU CREATE A THREAD

**Read `org/threads/THREAD_KNOWLEDGE.md` first.**

It contains mandatory rules (M1-M5) that govern context injection, model
selection, turn limits, and agent behavior. Skipping it produces threads
where agents fabricate answers or fail to ground their responses in real code.

---

## Overview

The thread system enables structured, multi-turn conversations between agents without requiring Andrew to manually relay messages. A **thread** is a filesystem-backed conversation folder where agents take turns writing messages. The Python orchestrator (`orchestrator.py`) drives the conversation loop via the OpenAI API and can be run from within a Claude Code session.

**Who can create/run threads:** Tier 1 (SA) and Tier 2 (DE, DT, DS, AE) agents.
**Who can participate:** Any agent (including Tier 3 RD agents).

---

## Quick Start

### Create a thread

```bash
./org/threads/create-thread.sh \
  --id "2026-03-02-etl-migration-review" \
  --topic "Review seeking-alpha ETL migration approach" \
  --created-by "1.0.0_SA_CTO" \
  --participants "1.0.0_SA_CTO,0.5.0_AE_OpalETL" \
  --context-file path/to/CONTEXT.json \
  --opening-message path/to/opening.md
```

### Run the orchestrator

```bash
# Bespoke thread (use gpt-4o for grounded technical conversations)
python org/threads/orchestrator.py --thread 2026-03-02-etl-migration-review --model gpt-4o --verbose

# Exploratory sync (use the convenience wrapper -- gpt-4o-mini, no config needed)
./org/threads/run-exploratory.sh 0.1.0_DS_MarketIntelligence 0.5.0_AE_OpalETL
```

### Check results

Thread messages are in `org/threads/{thread_id}/messages/`.
After completion, each participant gets a receipt in their `threads/` folder.

---

## Thread Folder Structure

Each thread is a self-contained folder:

```
org/threads/{thread_id}/
  THREAD.json              # Immutable metadata (set at creation)
  CONTEXT.json             # Context injection manifest (set at creation)
  TURN.json                # Mutable turn state (updated each turn by orchestrator)
  CONTEXT_COMPILED.md      # Generated briefing document (all context merged)
  context/                 # Materialized context files
    agents/                #   Per-participant identity, logs, task orders
    refs/                  #   Documents and code from CONTEXT.json
    commits/               #   Git log/diff output for commit ranges
    inline_notes.md        #   Free-form notes from CONTEXT.json inline field
  messages/
    000.md                 # Opening message (written by thread creator)
    001.md                 # First response
    002.md                 # ...
```

**Thread ID format:** `YYYY-MM-DD-{short-slug}` (e.g., `2026-03-02-etl-migration-review`)

---

## THREAD.json -- Thread Metadata

```json
{
  "id": "2026-03-02-etl-migration-review",
  "created_by": "1.0.0_SA_CTO",
  "created_at": "2026-03-02T10:00:00Z",
  "topic": "Review seeking-alpha ETL migration approach",
  "participants": ["1.0.0_SA_CTO", "0.5.0_AE_OpalETL"],
  "turn_order": "alternating",
  "max_turns_per_agent": 3,
  "status": "active"
}
```

| Field | Description |
|-------|-------------|
| `id` | Thread ID matching the folder name |
| `created_by` | Agent serial who created the thread |
| `created_at` | ISO 8601 timestamp |
| `topic` | Human-readable topic description |
| `participants` | Array of agent serial numbers (the only agents that can participate) |
| `turn_order` | `alternating` (A-B-A-B), `round_robin` (A-B-C-A-B-C), or `directed` (current agent picks next) |
| `max_turns_per_agent` | Max turns per agent (default 3). Total thread cap = N x num_participants |
| `status` | `active`, `complete`, `blocked`, `needs_human` |

### Serial Number Resolution

Everything is derived from the serial number. No redundant paths in THREAD.json.

- `1.0.0_SA_CTO` -> `org/tier1_exec/1.0.0_SA_CTO/`
- `0.5.0_AE_OpalETL` -> `org/tier2_senior/0.5.0_AE_OpalETL/`
- `0.1.2_RD_CausalityEngine` -> `org/tier3_junior/0.1.2_RD_CausalityEngine/`

The tier is determined by which position holds the number:
- `X.0.0` where X > 0 = `tier1_exec`
- `0.Y.0` where Y > 0 = `tier2_senior`
- `0.Y.Z` where Z > 0 = `tier3_junior`

Role code is extracted from position 2 of the serial (e.g., `SA`, `AE`, `RD`), mapped to base prompts:
- SA -> `org/ref/prompts/systems_architect.md`
- DE -> `org/ref/prompts/dashboard_engineer.md`
- DT -> `org/ref/prompts/devops_technician.md`
- DS -> `org/ref/prompts/data_scientist.md`
- AE -> `org/ref/prompts/aws_engineer.md`
- RD -> `org/ref/prompts/react_designer.md`

---

## CONTEXT.json -- Context Injection Manifest

This is how you inject shared context into the thread. All participants see the same compiled context.

```json
{
  "documents": [
    {
      "label": "Architecture Spec",
      "path": "docs/architecture/PORTFOLIO_EXPORT_TRADE_SUBMISSION_BRIDGE.md"
    }
  ],
  "code": [
    {
      "label": "Trade Submission API",
      "path": "portal/src/api/endpoints/trade-submission.ts"
    },
    {
      "label": "Portfolio Types",
      "path": "portal/src/types/portfolio-optimization.ts",
      "lines": "1-50"
    }
  ],
  "commits": [
    {
      "label": "Recent BD pipeline changes",
      "range": "bd-v2.13.0..HEAD",
      "paths": ["data/black_diamond/"]
    }
  ],
  "logs": [
    {
      "label": "AE session log",
      "agent": "0.5.0_AE_OpalETL",
      "date": "2026-03-01"
    },
    {
      "label": "DS investigation",
      "path": "org/tier2_senior/0.1.0_DS_MarketIntelligence/deliverables/correlation_analysis.md"
    }
  ],
  "inline": "Additional briefing notes written by the thread creator. Free-form markdown."
}
```

### Auto-Injected Context (No Manual Specification Needed)

For every participant listed in THREAD.json, the system automatically injects:

1. **Identity:** `{agent_folder}/README.md` -> `context/agents/{serial}_README.md`
2. **Recent logs:** Most recent session logs -> `context/agents/{serial}_logs/`
3. **Task orders:** Pending task orders -> `context/agents/{serial}_task_orders/`

### Explicit Context Resolution

| Type | How It Gets Materialized |
|------|--------------------------|
| `documents` | File copied to `context/refs/{label_slug}.md` |
| `code` | File copied to `context/refs/{label_slug}` (with optional line range extraction) |
| `commits` | `git log --oneline` + `git diff --stat` written to `context/commits/{label_slug}.txt` |
| `logs` (by agent+date) | Log files copied to `context/refs/` |
| `logs` (by path) | File copied to `context/refs/` |
| `inline` | Written to `context/inline_notes.md` |

### Why Copy Instead of Live Paths?

- Thread becomes a self-contained, auditable artifact
- Source files may change between turns -- the thread should reference the state at creation time
- Agents can be scoped to only read the thread folder

---

## TURN.json -- Turn State

```json
{
  "turn_number": 2,
  "next_agent": "1.0.0_SA_CTO",
  "turns_taken": {
    "1.0.0_SA_CTO": 1,
    "0.5.0_AE_OpalETL": 1
  },
  "status": "active",
  "last_updated": "2026-03-02T10:05:00Z"
}
```

Updated by the orchestrator after each agent completes its turn. Agents never modify this file.

---

## Message Format

Each message is `messages/{NNN}.md` (zero-padded 3 digits):

```markdown
---
agent: 0.5.0_AE_OpalETL
turn: 1
timestamp: 2026-03-02T10:05:00Z
signal: continue
---

## Response

[Agent's actual content -- analysis, questions, proposals, decisions]

## Open Questions

- Question 1 for the other participant
- Question 2

## Signal

- **continue** -- I have questions / more to discuss
  (or **converge** -- I believe we have reached agreement)
  (or **escalate** -- This needs human input, reason: ...)
```

### Signal Values

| Signal | Meaning | Orchestrator Action |
|--------|---------|---------------------|
| `continue` | More to discuss, questions remain | Advance to next agent's turn |
| `converge` | Conversation has reached resolution | If both agents signal converge consecutively, thread completes |
| `escalate` | Needs human input | Set thread status to `needs_human`, halt |

### Forced Convergence

On an agent's **last turn** (turns_taken == max_turns_per_agent), the signal MUST be `converge`. The turn instructions template enforces this.

---

## Orchestrator Usage

```
Usage: ./org/threads/orchestrator.sh [options]

Options:
  --thread <id>       Run a specific thread (default: run all active threads)
  --concurrency <n>   Max threads to run in parallel (default: 1)
  --dry-run           Show what would be invoked without running
  --verbose           Print agent prompts and responses to stdout
```

### Core Loop (Per Thread)

1. Read THREAD.json and TURN.json
2. Check termination conditions
3. Determine next agent from TURN.json
4. Resolve agent serial -> folder paths
5. Build system prompt (base persona + scoped prompt)
6. Build user prompt (CONTEXT_COMPILED.md + all messages + turn instructions)
7. Invoke `claude -p` with the constructed prompts
8. Validate agent wrote the expected message file
9. Parse signal from the message frontmatter
10. Update TURN.json (increment turn, set next agent)
11. Check termination again
12. If complete: write thread receipts to each participant's `threads/` folder

### Termination Conditions

- All agents have exhausted their max turns
- Last two consecutive messages both signal `converge`
- Any message signals `escalate` (thread halts as `needs_human`)

### Thread Receipts

When a thread completes, a compiled markdown receipt is saved to each participant's `threads/` folder:

```
{agent_folder}/threads/YYYY-MM-DD_{other_serials}_{topic_slug}.md
```

For a 2-party thread between CTO and OpalETL:
- `org/tier1_exec/1.0.0_SA_CTO/threads/2026-03-02_0.5.0_AE_OpalETL_etl-migration-review.md`
- `org/tier2_senior/0.5.0_AE_OpalETL/threads/2026-03-02_1.0.0_SA_CTO_etl-migration-review.md`

For multi-party threads (3+ participants), other serials are joined with `+`:
- `2026-03-02_0.5.0_AE_OpalETL+0.3.0_DE_TradingOps_pipeline-review.md`

---

## create-thread.sh Usage

```
Usage: ./org/threads/create-thread.sh \
  --id <thread-id> \
  --topic <topic-string> \
  --created-by <agent-serial> \
  --participants <comma-separated-serials> \
  --context-file <path-to-CONTEXT.json> \
  --opening-message <path-to-opening.md> \
  [--max-turns <n>]           # default: 3
  [--turn-order <type>]       # default: alternating
```

### What It Does

1. Creates `org/threads/{id}/` with subdirectories
2. Writes THREAD.json from arguments
3. Auto-injects participant context (README, logs, task orders) via serial resolution
4. Resolves explicit CONTEXT.json entries (copies docs, runs git log, etc.)
5. Generates CONTEXT_COMPILED.md
6. Copies opening message as `messages/000.md`
7. Writes initial TURN.json pointing to the second participant

---

## Agent Turn Instructions

When an agent is invoked by the orchestrator, it receives turn instructions appended to its prompt:

```
## YOUR TURN -- Thread Protocol

You are participating in a structured conversation thread.

**Your identity:** {agent_serial} ({role})
**Thread topic:** {topic}
**Turn:** {turn_number} of max {max_total_turns}
**Your turns remaining:** {remaining}

### Instructions

1. Read the CONTEXT section below -- this is your shared briefing material.
2. Read all previous messages in order.
3. Write your response to: org/threads/{thread_id}/messages/{NNN}.md
4. Use the message template (YAML frontmatter with agent, turn, timestamp, signal).
5. Set your signal:
   - continue -- you have more to discuss or questions remain
   - converge -- you believe the conversation has reached resolution
   - escalate -- you need human input (explain why in your message)

### Constraints
- Stay in your role. Do not impersonate other agents.
- Do not modify THREAD.json, TURN.json, CONTEXT.json, or other agents' messages.
- Only write your own message file.
- Reference context documents by their label (e.g., "per the Architecture Spec...").
- Be concrete. Name files, functions, resource names. Avoid vague summaries.
- If this is your last turn, your signal MUST be converge (forced convergence).
```

---

## Troubleshooting

### Thread stuck on "active" but no agent is responding
Check TURN.json -- the `next_agent` serial may not resolve to a valid folder. Verify the agent folder exists under `org/{tier}/`.

### Agent wrote message but signal not parsed
The orchestrator reads the YAML frontmatter `signal:` field. Ensure the message starts with `---` and has a valid signal value.

### Context materialization failed
Check that all paths in CONTEXT.json exist relative to the repo root. The `commits` range must be valid git refs.

### Thread receipts not generated
Receipts are only generated when the thread reaches `complete` status (convergence or max turns). Threads that end as `needs_human` do not auto-generate receipts.
