# Thread System — Configuration Reference

All tunable settings for the thread orchestration system.
Edit this file when paths, models, or defaults change.

---

## Model Settings

| Use case | Model | Flag |
|----------|-------|------|
| Code-grounded threads (Pattern 0, Pattern 2) | `gpt-5.2` | `--model gpt-5.2` |
| Planning/coordination threads (Pattern 1, Pattern 3) | `gpt-5.2` | `--model gpt-5.2` |
| Default in `orchestrator.py` | `gpt-5.2` | (built-in default) |
| Default in `run-exploratory.sh` | `gpt-5.2` | (built-in default) |

**WARN:** `gpt-5.3-codex` is completions-only and NOT compatible with `client.chat.completions.create()`.
Run `python org/threads/test-model.py --model <name>` to verify any new model before using it.

---

## Paths

| Resource | Path | Notes |
|----------|------|-------|
| Threads directory | `org/threads/` | Thread folders live here |
| Staging scripts | `org/threads/staging/` | One script per planned thread |
| Templates | `org/threads/templates/` | THREAD.json, TURN.json, CONTEXT.json, message.md |
| Project registry | `org/projects/REGISTRY.md` | Human-readable project index |
| Project files | `org/projects/{CODE}.json` | One file per project, auto-updated by create-thread.sh |
| Base persona prompts | `org/ref/prompts/{role}.md` | Injected as system prompt prefix for each agent |
| Agent folders | `org/{tier}/{serial}/` | Source for auto-injected context |
| JQ binary | `.tools/jq.exe` | Required by create-thread.sh and run-exploratory.sh |
| Python executable | `/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe` | Windows path for staging scripts |

---

## Secrets

| Secret | Storage | Key |
|--------|---------|-----|
| OpenAI API key | AWS Secrets Manager | `openai-api-key` |

The orchestrator first checks `OPENAI_API_KEY` environment variable. If not set, it fetches
from Secrets Manager using `--secret` flag (default: `openai-api-key`).

Override: `OPENAI_API_KEY=<key> python org/threads/orchestrator.py --thread <id>`
Custom secret: `python org/threads/orchestrator.py --thread <id> --secret my-secret-name`

---

## Turn Limits (Defaults by Pattern)

| Pattern | `--max-turns` | Total messages (incl. opening) |
|---------|--------------|-------------------------------|
| Pattern 0 (pre-implementation alignment) | 3 | 10 (3-party) or 7 (2-party) |
| Pattern 1 (delivery audit) | 2 | 5 (2-party) |
| Pattern 2 (technical investigation) | 3 | 7 (2-party) |
| Pattern 3 (cross-pod coordination) | 3 | 7 (2-party) |

---

## Thread ID Formats

| Context | Format | Example |
|---------|--------|---------|
| Project thread | `{CODE}-{NNN}-{slug}` | `ADVI-004-books-publisher-gap` |
| Non-project (legacy) | `YYYY-MM-DD-{slug}` | `2026-03-02-etl-migration-review` |
| Exploratory (auto) | `YYYY-MM-DD-{a1slug}+{a2slug}-sync` | `2026-03-03-ds-clientplatform+de-clientplatform-sync` |

---

## Receipt Filename Format

```
{agent_folder}/threads/{thread_id}_{other_serials}.md
```

Examples:
- `org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-004-books-publisher-gap_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md`
- `org/tier1_exec/1.0.0_SA_CTO/threads/2026-03-02-etl-migration-review_0.5.0_AE_OpalETL.md`

---

## Tool Call Limits (orchestrator.py)

| Setting | Value | Location |
|---------|-------|----------|
| Max tool calls per turn | 5 | `orchestrator.py:MAX_TOOL_CALLS_PER_TURN` |
| Max file size (chars) | 50,000 | `orchestrator.py:FILE_SIZE_LIMIT` |

Available tools for agents in bespoke threads: `read_file`, `glob_files`, `grep_content`.
Exploratory threads run with `--no-tools` (auto-passed by `run-exploratory.sh`).

---

## Compatibility Test

Before using any new model with the orchestrator:

```bash
python org/threads/test-model.py --model <model-name>
```

Checks: (1) chat completions endpoint compatibility, (2) `temperature=0.3` support.
Both must pass. If `max_tokens` error appears, the model uses `max_completion_tokens`
(newer API style) -- update the test but do NOT update the orchestrator unless needed.
