# Thread System — Quick Reference

Multi-turn structured conversations between agents, driven by the OpenAI API.
Threads are project-linked, filesystem-backed, and fully automated.

**Before creating any thread:** read `THREAD_KNOWLEDGE.md` (mandates M1-M9).
**For full technical detail:** see `ARCHITECTURE.md`.
**For configuration and paths:** see `CONFIG.md`.

---

## Quick Start

### 1. Check the project registry

```bash
cat org/projects/REGISTRY.md
```

Every thread must belong to a project. Project code format: `{MACRO}_{6CHAR}` (e.g., `ADVI_V1VERS`).
If your project doesn't exist yet, pick a macro from `org/projects/MACRO_CODES.md`, choose a
6-char suffix, create `org/projects/{PROJECT_CODE}.json` (copy any existing project JSON as a
template), and add a row to REGISTRY.md.

### 2. Write a staging script

Copy `staging/BESPOKE_TEMPLATE.sh`. Set `PROJECT`, `TOPIC`, `PARTICIPANTS`, `CONTEXT`,
and the opening message. Save as `staging/run-{PROJECT_CODE}-{NNN}-{slug}.sh`
(e.g., `staging/run-ADVI_V1VERS-007-books-design.sh`).
The `{PROJECT_CODE}-{NNN}` serial is auto-assigned when you run it -- name the file with the
next expected serial for clarity, but the script will confirm the actual assignment.

### 3. Run it (Bash tool -- no Andrew handoff)

```bash
bash org/threads/staging/run-ADVI_V1VERS-007-books-publisher-gap.sh
```

This scaffolds the thread folder AND runs the orchestrator in one shot.

### 4. Check results

```bash
# Thread messages
ls org/threads/ADVI_V1VERS-007-books-publisher-gap/messages/

# Receipts in agent folders (one per participant)
ls org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI_V1VERS-007-*.md

# Updated project file
cat org/projects/ADVI_V1VERS.json
```

---

## Exploratory Sync (2-party, no config needed)

```bash
./org/threads/run-exploratory.sh 0.4.0_DE_ClientPlatform 0.4.0_DT_ClientPlatform --project ADVI_V1VERS
```

Auto-assigns next serial under the project. Uses `gpt-5.2`, `--no-tools`, 2 max turns.
Pass the full project code (e.g., `ADVI_V1VERS`), not the macro code (`ADVI`).
Both agents must have recent session logs or the thread will be low-signal (O3 rule).

---

## Thread Patterns

| Pattern | When | Participants | Model | Turns | Tools |
|---------|------|-------------|-------|-------|-------|
| **0** Pre-implementation alignment | Before writing any code for a DS→DE→RD interface | DS + DE + RD (round-robin) | gpt-5.2 | 3 | ON |
| **1** Pod delivery audit | Status check before planning | DE + DT | gpt-5.2 | 2 | OFF |
| **2** Technical gap investigation | Unknown before CTO can write PRD | DS + AE or DT | gpt-5.2 | 3 | ON |
| **3** Cross-pod coordination | Feature touching 2+ pods | Both pod DEs | gpt-5.2 | 3 | ON |

Pattern 0 runs BEFORE task orders are written. The thread receipt IS the data contract.

---

## Project Serial System

```
org/projects/ADVI_V1VERS.json    Project registry for AdvisorIntelligence V1 Completion
    thread_counter: 6            Next serial will be ADVI_V1VERS-007

Thread folder:  org/threads/ADVI_V1VERS-007-{slug}/
Receipt format: {agent_folder}/threads/ADVI_V1VERS-007-{slug}_{other_serials}.md

Filter any agent's threads by project:
    ls org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI_V1VERS-*.md

Filter by macro (all ADVI projects):
    ls org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI_*.md
```

Passing `--project ADVI_V1VERS` to `create-thread.sh` or `run-exploratory.sh`:
- Auto-assigns `ADVI_V1VERS-007` as the serial
- Patches `project` and `serial` into `THREAD.json`
- Updates `ADVI_V1VERS.json`: increments `thread_counter`, appends thread entry

---

## Thread ID Formats

| Context | Format | Example |
|---------|--------|---------|
| Project thread | `{PROJECT_CODE}-{NNN}-{slug}` | `ADVI_V1VERS-007-books-publisher-gap` |
| Legacy / non-project | `YYYY-MM-DD-{slug}` | `2026-03-02-etl-migration-review` |

---

## THREAD.json Fields

| Field | Description |
|-------|-------------|
| `id` | Thread folder name |
| `project` | Project code (e.g., `ADVI_V1VERS`) -- only if `--project` was passed |
| `serial` | Project serial (e.g., `ADVI_V1VERS-007`) -- only if `--project` was passed |
| `created_by` | Agent serial who wrote `messages/000.md` |
| `participants` | Agents who take turns (not necessarily includes creator) |
| `turn_order` | `alternating` (A-B) or `round_robin` (A-B-C) |
| `max_turns_per_agent` | Per-agent cap. Total = cap × num_participants |
| `status` | `active` / `complete` / `blocked` / `needs_human` |

---

## Message Format

Every message file (`messages/{NNN}.md`) must start with:

```
---
agent: 0.4.0_DS_ClientPlatform
turn: 1
timestamp: 2026-03-03T20:05:00Z
signal: continue
---

[Message body]
```

Signal values: `continue` (more to discuss) | `converge` (done) | `escalate` (needs human).
Last turn signal MUST be `converge` (enforced by orchestrator turn instructions).

---

## Termination Conditions

1. All agents exhausted `max_turns_per_agent` -- thread completes, receipts written
2. Two consecutive `converge` signals -- thread completes, receipts written
3. Any `escalate` signal -- thread halts as `needs_human`, NO receipts written

---

## orchestrator.py CLI

```
python org/threads/orchestrator.py \
  --thread  ADVI-004-books-publisher-gap \
  --model   gpt-5.2 \
  --verbose \
  [--dry-run]   \   # show prompts without calling API
  [--no-tools]  \   # disable read_file/glob/grep (exploratory threads)
  [--secret openai-api-key]   # AWS Secrets Manager secret name
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Thread not found | Check `org/threads/{thread_id}/THREAD.json` exists |
| Agent folder not found | Serial tier resolution: `0.Y.Z` Z>0 = tier3_junior, `0.Y.0` Y>0 = tier2_senior |
| Signal not parsed | Message must start with raw `---` YAML frontmatter, not a code block |
| Receipts missing | Only written on `complete`. `needs_human` threads skip receipts. |
| Model error | Run `python org/threads/test-model.py --model <name>` to verify |
| Project file not updated | JQ must be at `.tools/jq.exe`. Check create-thread.sh stderr. |

---

**See also:**
- `ARCHITECTURE.md` -- full technical end-to-end (prompt construction, context pipeline, ops)
- `CONFIG.md` -- all paths, models, secrets, defaults
- `THREAD_KNOWLEDGE.md` -- mandatory rules (M1-M9) and failure patterns
