# Briefing: Docker Runtime + Context Windowing Fix

> **REVIVAL PREREQUISITE (added 2026-07-25, runtime retired per LD-0286):** `runtime/nodes/architect.py:62` and
> `runtime/nodes/coordinator.py:421` spawn bare `['find',...]`, which on a native-Windows host resolves to
> **System32 `find.exe`, not GNU find** (CreateProcess searches System32 before PATH; `shutil.which` does not
> reveal this) — both sites return rc=2 and silently degrade (`if rc == 0:` swallows it); they have likely never
> worked outside the container. **Before any revival: migrate both to `.tools/msys_argv_guard.py
> msys_safe_run()`** (note: inside Docker this is moot — the hazard is host-side execution only, which the
> "No Uncontainerized Runtime" rule below already forbids). Record: NFRA_TOOLUNIFY census SYNTHESIS.md §3.

**To:** 2.0.0_SA_COO
**Date:** 2026-03-19
**Context:** First live-fire burned 440K tokens on one Worker. Root cause
identified and fixed. All future runs MUST use the Docker container.

---

## Rule: No Uncontainerized Runtime

Do NOT run `python -m org.ka_testing.advi_clsuni.run_alignment` directly.
All execution goes through Docker. No exceptions.

The container provides:
- Live telemetry dashboard at http://localhost:8111
- Filesystem isolation (only the mounted workspace is accessible)
- Predictable environment (no Windows path issues, no MSYS, no WMI hangs)
- Kill the container to kill the run (no orphaned Python processes)

---

## What Caused the 440K Token Burn

`_invoke_staged()` carried the FULL message history across all KF stages.
Every file the Worker read in Pe stage stayed in the conversation context
for In, Ac, and Ad. By iteration 11, each API call was sending ~40K tokens
of accumulated file contents that the Worker no longer needed.

AE_CloudOps read `main.tf` (large Terraform file) in Pe, then carried that
content through 11 iterations. 40K x 11 = 440K tokens. One Worker. Before
any code was written.

## What Was Fixed

**Context windowing at stage boundaries.** At each KF stage transition
(Pe->In, In->Ac, Ac->Ad), the message history is compressed:

- Raw tool_result messages (file contents) are DROPPED
- The LLM's text reasoning (what it learned) is KEPT (last 3 blocks, ≤4K)
- System prompt and task order are preserved
- Each stage starts with ~4-6K of context instead of accumulated 20-40K

**Expected cost per Worker:** 60-80K tokens (was 440K).
**Expected cost for all 5 Workers:** 300-400K tokens (~$3-4 at gpt-4o).

Both `llm.py` (Anthropic) and `llm_openai.py` (OpenAI) are fixed.
The Docker image has been rebuilt with the fix.

---

## How to Run

### Step 1: Get the OpenAI API key

```bash
export AWS_EC2_METADATA_DISABLED=true
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id multi-threadv2 --query SecretString --output text)
```

### Step 2: Start the container

```bash
cd C:/Users/AndrewBerman/Desktop/ajb_workspace/org/ka_testing

docker run -it --rm \
  -v C:/Users/AndrewBerman/Desktop/ajb_workspace:/workspace \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e HIERARCHY_LLM_PROVIDER=openai \
  -e AWS_EC2_METADATA_DISABLED=true \
  -p 8111:8111 \
  runtime:latest \
  --phase execution \
  --config .runtime/config.json \
  --branch CLOUD_test
```

### Step 3: Open the dashboard

http://localhost:8111

You will see:
- Top bar: total tokens, cost ($), wall time, agent count
- Agent cards (left): one per Worker with status, KF stage progress,
  token counters, tool call activity stream
- Event stream (right): every LLM iteration, tool call, stage transition

### Step 4: Watch and verify

Monitor the dashboard. If any Worker's token count starts climbing past
100K, something is wrong -- kill the container (`Ctrl+C` or `docker stop`).

Normal behavior: each Worker should use 60-80K tokens across 8-12
iterations. The stage progress bar should show Pe->In->Ac->Ad progression.

---

## Config File

The container expects a config JSON at the path given by `--config`.
For the CLSUNI test, create `.runtime/config.json` in ajb_workspace root.

The config has two sections: `workers` (for alignment phases) and
`task_orders` (for execution phase).

For Phase 5 execution only (alignment already tested), the config needs
`task_orders` -- an array of objects, each with:

```json
{
  "identity": "AE-CLOUDOPS",
  "serial": "AE.CO.1",
  "prompt": "You are an infrastructure agent...",
  "task_order_text": "## Task Order: ...",
  "task_order_id": "CLSUNI-WS1",
  "summary": "AE_CloudOps: Terraform bd-securities",
  "allowed_paths": ["infra/aws/terraform/shared-infra/main.tf"],
  "max_iterations": 10,
  "blocks": ["DT.CP.1"],
  "pre_flight_checks": []
}
```

Key fields:
- `allowed_paths`: Worker can ONLY write to these paths
- `max_iterations`: keep at 10-12 (not 20-25)
- `blocks`: list of serials that should be skipped if this Worker fails
- `pre_flight_checks`: deterministic shell commands that must pass first

---

## Iteration Budgets (Revised)

| Worker | max_iterations | Rationale |
|--------|---------------|-----------|
| AE_CloudOps | 10 | Read main.tf, write one resource block, verify |
| DS | 12 | Create new file from spec, smoke test |
| RD | 10 | Edit existing types.ts + ClientsTab.tsx |
| DT | 10 | Copy file, edit import, verify |
| AE_PartnerETL | 8 | Create script from spec, syntax check |

These are hard caps. With context windowing, each iteration carries ~6K
context (not 40K). Total budget: ~500K tokens for all 5 Workers.

---

## What NOT to Do

- Do NOT run `python -m org.ka_testing.advi_clsuni.run_alignment` directly
- Do NOT set max_iterations above 12 for any Worker
- Do NOT skip the dashboard -- if you can't see http://localhost:8111,
  something is wrong with the container
- Do NOT re-run without checking the results from the first attempt --
  the AE_CloudOps Worker may have written to main.tf already. Check
  `git diff` on CLOUD_test branch before re-running.

---

## After the Run

Results are written to:
- Container: `/workspace/.runtime/results/`
- Host: `ajb_workspace/.runtime/results/`
- JSONL telemetry: `KA_CLSUNI-events.jsonl` (same directory)

Review:
1. Token spend per Worker (should be 60-80K each)
2. Files written (from ExecutionResult)
3. Commit SHAs (from git_commit tool calls)
4. Any pre-flight failures
5. `git log CLOUD_test` to see all Worker commits
