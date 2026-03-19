# Briefing: Runtime Updates for ADVI_CLSUNI Execution Test

**From:** CHF.SYS.1 (Division Architect, System)
**To:** 2.0.0_SA_COO
**Date:** 2026-03-19
**Context:** Following the first real-world alignment test (run_20260319T180044),
four runtime gaps were identified. Three have been closed. The runtime can now
execute task orders end-to-end with tool access, scope enforcement, and git
commit attribution.

---

## What Changed in the Runtime

All changes are in `org/ka_testing/runtime/`. Nothing is project-specific.
The runtime accepts any task order, any Worker prompt, any working directory.

### 1. invoke_worker_for_execution() — NEW

**File:** `runtime/alignment.py`

Full execution function. Takes a task order and runs a Worker through
KF-staged execution with real tools:

```python
from runtime.alignment import invoke_worker_for_execution, ExecutionResult

result = invoke_worker_for_execution(
    system_prompt="You are a data science agent...",
    task_order_text="WS2: Write lib/etf_classifier.py...",
    worker_id="DS-WORKER",
    worker_serial="DS.CP.1",
    task_order_id="CLSUNI-WS2",
    working_directory="/path/to/ajb_workspace",
    allowed_paths=["data/black_diamond/scripts/gold/lib/etf_classifier.py",
                   "data/black_diamond/scripts/gold/lib/__init__.py"],
    max_iterations=25,
    branch="CLOUD_test",
)

# result.files_written: list of files the Worker created/modified
# result.commit_sha: git commit SHA (if Worker committed in Ad stage)
# result.token_usage: {"input": N, "output": N, "total": N}
# result.success: bool
# result.error: str (if failed)
```

**KF stage progression:**
- Pe: list_dir, grep_files, read_file, run_command (discover context)
- In: read_file, grep_files (targeted reads)
- Ac: write_file, edit_file, apply_patch (WRITE ONLY -- read tools removed)
- Ad: read + write + run_command + git_commit (verify and commit)

**Scope enforcement:** `allowed_paths` restricts write operations to the
task order's declared deliverables. The Worker cannot write outside scope.
Read operations are unrestricted (the Worker needs to read existing code).

**Branch isolation:** Pass `branch="CLOUD_test"` and the Worker executes
on that branch. All commits go to the test branch, not CLOUD.

### 2. git_commit Tool — NEW

**File:** `runtime/tools.py`

Workers call `git_commit(message, author_serial, files)` in the Ad stage:

```python
git_commit(
    message="[CLSUNI] DS.CP.1: implement ETFClassifier shared module",
    author_serial="DS.CP.1",
    files=["data/black_diamond/scripts/gold/lib/etf_classifier.py"]
)
# Returns: "OK: Committed a1b2c3d4e5f6 by DS.CP.1: [CLSUNI] DS.CP.1: implement..."
```

- Stages only specified files (or all changes if files omitted)
- Enforces `--author` format: `{serial} <{serial}@runtime.agent>`
- Returns commit SHA for audit trail
- Available only in Ad stage (after deliverables are written)

### 3. Deploy-Tier Command Classification — UPDATED

**File:** `runtime/tools.py`

`run_command` now classifies commands into three tiers:
- **Safe** (read-only): always allowed. ls, grep, git status, python -c.
- **Build**: allowed when scope permits. pip, bun, cp.
- **Deploy** (infrastructure mutation): `terraform apply`, `build-and-upload.sh`,
  `safe-ec2-deploy.sh`, `docker`, `aws`. Gets 600s timeout (vs 120s).

**No human gate.** Once the PRD is accepted, execution is autonomous.
Deploy-tier commands execute when the Coordinator's dependency graph
confirms all upstream tasks are complete.

### 4. Synthesis Prompt — UPDATED

**File:** `runtime/alignment.py`

Two permanent protocol improvements (not project-specific):

**Pre-state / post-state distinction:** The Coordinator now assesses
CURRENT state (what exists on disk) vs TARGET state (what the design
says should exist). `status: "match"` means the interface works right
now. If both Workers acknowledge a pending change, status is `"missing"`
(the target interface doesn't exist yet), not `"match"`. This prevents
the false-match on DS->RD from the first run.

**CRD truth-state tag extraction:** Workers write `[KNOWN]`, `[SUSPECTED]`,
`[UNKNOWN]`, `[BLOCKED]` inline in prose. The Coordinator extracts these
and reports them as `producer_confidence` / `consumer_confidence` on each
interface. `enforce_truth_state()` validates -- if the Coordinator reports
`unknown` or `blocked` on a `match`, it gets downgraded automatically.

### 5. Full Agent Roster

`run_alignment.py` now includes all 5 PRD agents:
- AE_CloudOps (shared infra, DynamoDB)
- DS_ClientPlatform (gold scripts, classifier, Lambda handlers)
- RD_AdvisorIntelligence (portal types, components)
- DT_ClientPlatform (Terraform, Lambda deploy)
- AE_PartnerETL (EC2 ops, seed/classify, gold runs)

---

## How to Run the Updated Test

### Phase 1-4 (alignment only, same as before but with fixes):

```bash
cd ajb_workspace/
HIERARCHY_LLM_PROVIDER=openai python -m org.ka_testing.advi_clsuni.run_alignment
```

Expected improvements over first run:
- 5 Workers instead of 3 (AE agents included)
- DS->RD interface should be `missing` not `match` (pre/post fix)
- Truth-state labels extracted from prose by Coordinator
- AE_PartnerETL should appear in task orders

### Phase 5 (execution -- NEW):

To exercise `invoke_worker_for_execution()`, extend `run_alignment.py`
with a Phase 5 loop that takes the enriched task orders from Phase 4 and
dispatches them to Workers in dependency order.

The execution loop pattern:

```python
from runtime.alignment import invoke_worker_for_execution

# Level 0: AE_CloudOps (no upstream dependencies)
from runtime.alignment import PreFlightCheck

# Level 0: AE_CloudOps (no upstream dependencies)
result_ae = invoke_worker_for_execution(
    system_prompt=WORKER_AE_CLOUDOPS_PROMPT,
    task_order_text=enriched_task_orders["AE_CloudOps"],
    worker_id="AE-CLOUDOPS", worker_serial="AE.CO.1",
    task_order_id="CLSUNI-WS1",
    working_directory=str(AJB_WORKSPACE),
    allowed_paths=["infra/aws/terraform/shared-infra/"],
    branch="CLOUD_test",
    # No pre-flight -- AE_CloudOps is the first mover
)

# Level 1a: DS (depends on AE completing WS1)
# DS is code-writing only -- no pre-flight needed, test branch is safe
result_ds = invoke_worker_for_execution(
    system_prompt=WORKER_DS_PROMPT,
    task_order_text=enriched_task_orders["DS"],
    worker_id="DS-WORKER", worker_serial="DS.CP.1",
    task_order_id="CLSUNI-WS2-6",
    working_directory=str(AJB_WORKSPACE),
    allowed_paths=[
        "data/black_diamond/scripts/gold/lib/",
        "data/black_diamond/scripts/classification/",
        "data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py",
    ],
    branch="CLOUD_test",
)

# Level 3: AE_PartnerETL (gold run -- infrastructure mutation)
result_ae_etl = invoke_worker_for_execution(
    system_prompt=WORKER_AE_PARTNERETL_PROMPT,
    task_order_text=enriched_task_orders["AE_PartnerETL"],
    worker_id="AE-PARTNERETL", worker_serial="AE.PE.1",
    task_order_id="CLSUNI-WS8-AE",
    working_directory=str(AJB_WORKSPACE),
    allowed_paths=["data/black_diamond/scripts/"],
    branch="CLOUD_test",
    pre_flight_checks=[
        PreFlightCheck(
            name="bd-securities-item-count",
            command='aws dynamodb describe-table --table-name bd-securities '
                    '--query "Table.ItemCount" --output text | '
                    'python3 -c "import sys; c=int(sys.stdin.read().strip()); '
                    'sys.exit(0 if c >= 100 else 1)"',
            failure_message="bd-securities table has < 100 items. "
                "Seed and classify must complete before gold run.",
        ),
    ],
)
# If pre-flight fails, result_ae_etl.success = False
# but DS, RD, DT results are unaffected
```

### Pre-Flight Checks — NEW

Infrastructure Workers carry `pre_flight_checks`: deterministic shell
commands that run before the LLM is invoked. If any check fails, THIS
Worker stops (`success=False`, `pre_flight_failures` populated) but the
rest of the pipeline continues. Other Workers are not blocked.

This replaces the human gate for infrastructure-mutation operations:

| Worker | Pre-flight needed? | Check |
|--------|--------------------|-------|
| AE_CloudOps (Terraform) | No for test | First mover, creates the table |
| DS (code writing) | No | Test branch, reversible |
| RD (TypeScript) | No | Test branch, reversible |
| DT (Lambda deploy) | Yes for production | Verify DS code committed, table exists |
| AE_PartnerETL (seed+classify) | No | Only writes to new table |
| AE_PartnerETL (gold run) | Yes | bd-securities must have >100 items |

Pre-flight checks are autonomous -- no human input. They are explicit
contracts on infrastructure state, not approval gates.

### Cost Model Clarification

Each `invoke_worker_for_execution()` is **N sequential LLM calls** (one
per iteration in the KF loop), not a single call. `max_iterations=25`
means up to 25 LLM round-trips for that Worker.

**Realistic cost estimate:**
- 5 Workers x ~15-25 iterations x ~5K tokens/iteration
- Most Workers won't use full budget (DS is the heaviest)
- Total: 400-600K tokens, ~$4-6 at gpt-4o pricing
- Still cheap: one horizontal thread alignment used to cost 600K-1.2M
  for alignment ALONE, before any code was written

**Output:** Each Worker produces an `ExecutionResult` with files_written,
commit_sha, token_usage, pre_flight_failures. The Coordinator can verify
deliverables against acceptance criteria after all Workers complete.

---

## What's NOT in This Update

- **No automated Phase 5 loop in run_alignment.py.** The execution loop
  needs to be built by the COO based on the Phase 4 task orders. The
  runtime provides `invoke_worker_for_execution()` -- the orchestration
  (which Worker runs when, dependency checking) is the COO's job.

- **No verification phase (Phase 6).** After Workers execute, someone
  needs to verify deliverables against acceptance criteria. This could
  be a Coordinator re-invocation or a deterministic check. Not built yet.

- **No ask_user anywhere.** Once the PRD is accepted, execution is fully
  autonomous. Pre-flight checks replace human gates for infrastructure
  operations -- deterministic, no human in the loop.
