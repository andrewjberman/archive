# AGENT START HERE — Opal Capital Hierarchical Agent System

**You are an agent in the Opal Capital hierarchical organization. Follow these steps IN ORDER before doing anything else.**

---

## CRITICAL: BANNED AGENTS - READ THIS FIRST

**ABSOLUTELY DO NOT USE THESE AGENTS - THEY PRODUCE FABRICATED INFORMATION:**

### BANNED: Explore Agent
- **Status:** COMPLETELY UNRELIABLE - Produces false information
- **What to do instead:** Use Glob, Grep, and Read tools directly to examine files

### BANNED: Task Agent
- **Status:** UNRELIABLE - Produces inconsistent and poor results
- **What to do instead:** Do the work directly yourself using standard tools

---

## ANTI-PATTERNS (NEVER DO THESE)

- **NEVER write code directly on EC2 instances** - Repo -> S3 -> EC2 pulls from S3 -> executes. Even diagnostic scripts.
- **NEVER push scripts or edits to the EC2 Docker image** - Script fixes happen in the local repo only.
- **Use Edit tool instead of `sed`** for file editing.
- **Use Write tool instead of `cat` with heredocs**.
- **Use Read/Edit/Write tools directly** instead of chaining bash commands for file operations.

---

## Git Workflow

**This workspace has two branching models:**

1. **Parent repo (ajb_workspace):** Single working branch `CLOUD`. All agent work happens here.
2. **Portal submodule (`portal/`):** Uses `DEV` -> `PROD` -> Server deployment workflow.

**Branch Definitions:**
- **`CLOUD`** (parent repo) = The one working branch for all infrastructure, Lambda, data, and docs work
- **`DEV`** (portal submodule only) = Portal development branch
- **`PROD`** (portal submodule only) = Portal production branch
- **`main`** = NOT USED anywhere. Ignore completely.

**No Pull Requests:** This is a single-developer workflow. Use direct push.

---

## MANDATORY: Deployment Reference Docs

All deployment reference docs are included in this org structure at `org/ref/`:

| Doc | Location | When You Need It |
|-----|----------|-----------------|
| Lambda Deployment Protocol | `org/ref/LAMBDA_DEPLOYMENT_PROTOCOL.md` | Any Lambda function work |
| EC2 Deployment Protocol | `org/ref/EC2_DEPLOYMENT_PROTOCOL.md` | Any EC2 service work |
| EC2 Code Deployment Standard | `org/ref/EC2_CODE_DEPLOYMENT_STANDARD.md` | Any code running on EC2 |
| Terraform Pipeline Strategy | `org/ref/TERRAFORM_PIPELINE_STRATEGY.md` | Any Terraform changes |
| CloudFront Deployment Checklist | `org/ref/deployment/cloudfront_deployment_checklist.md` | CloudFront changes |

**Base persona prompts** are at `org/ref/prompts/{role}.md`.

---

## Critical Deployment Rules (Non-Negotiable)

1. **Terraform is the only Lambda deployment mechanism.** Never use `aws lambda update-function-code`, `deploy.sh`, or the AWS console.
2. **Commit before apply.** Write code -> Terraform -> update source map -> git commit -> plan -> apply -> verify 0-diff -> tag -> push.
3. **Dependencies go in Lambda Layers.** No `pip install -t .` into Lambda source dirs.
4. **Update the source map.** Every Lambda must have an entry in `infra/aws/lambda/ci/lambda-source-map.json`.
5. **Tag after deploy.** After 0-diff: `git tag -a {pipeline}-v{X.Y.Z} -m "description"` and `git push --follow-tags`.
6. **Always use `safe-ec2-deploy.sh`.** Never run service-specific deploy scripts directly.
7. **EC2_MANIFEST.json is the source of truth.** Every EC2 service must be registered.
8. **No emojis in code.** Never use emoji characters in production code, debug logs, or any code that runs on AWS.

---

## Step 1: Identify Yourself

Your agent folder contains your identity. Read your folder's files:
1. `README.md` — Your ID, role, responsibilities, reporting chain
2. `prompt.md` — Your scoped persona prompt

Your folder location follows the pattern:
```
org/{tier_folder}/{agent_id}/
```

Tier folders:
- `tier1_exec/` — SA agents (Tier 1)
- `tier2_senior/` — DE, DT, DS, AE agents (Tier 2)
- `tier3_junior/` — RD agents (Tier 3)

---

## Step 2: Read Your Recent Logs (HIGHEST PRIORITY)

**THIS IS THE MOST IMPORTANT STEP.**

1. Check your logs folder: `{your_agent_folder}/logs/`
2. Find the most recent date folder
3. Read ALL logs from that date
4. Understand what you were working on, decisions made, blockers, next steps

**Why YOUR logs are CRITICAL:**
- You are continuing YOUR previous work - not starting fresh
- Your logs contain YOUR decisions, blockers, next steps
- Without this, you WILL lose context and repeat work

---

## Step 3: Read Your Prompt

Read `{your_agent_folder}/prompt.md` and adopt that role. You should now:
- Think like that specialist
- Follow their principles and methodology
- Stay within your scoped responsibility
- Escalate to your reporting chain when needed

---

## Step 4: Understand Your Place in the Hierarchy

Read `org/ORG_CHART.md` to understand:
- Who you report to
- Who reports to you (if any)
- Your pod members
- Shared services available to you

**Escalation rules:**
- RD agents escalate to their pod's DE
- DE/DT/DS agents escalate to CTO (technical) or COO (resource/scheduling)
- AE agents escalate to CTO (technical) or COO (resource/scheduling)

---

## Step 4b: Check Daily Collaborative Log (Tier 1 and Tier 2 only)

If you are a Tier 1 or Tier 2 agent, check today's daily log:
```
org/daily_log/YYYY-MM-DD.md
```

This shows what other agents are working on, pushing, or deploying today. Before pushing, deploying, or committing to shared paths, add your own entry. See `org/CROSS_POD_COORDINATION.md` for the full daily log protocol.

---

## Step 5: Provide Oriented Summary

Give the user a brief summary:
```
Agent: [ID and name]
Role: [role type]
Pod: [pod name, if applicable]
Reports to: [manager agent ID]
Current priority: [from logs if any]
Key context: [from recent logs]

Ready to work. What would you like me to focus on?
```

---

## Session Logging Protocol

### Log Location

Logs go in YOUR agent folder:
```
{your_agent_folder}/logs/YYYY-MM-DD/descriptive_thesis_of_work.md
```

**Example:** `org/tier3_junior/0.0.1_RD_MarketPerformance/logs/2026-03-02/chart_component_refactor.md`

### Log Template

```markdown
# [Thesis Title] - [Agent ID]

**Date:** YYYY-MM-DD
**Start Time:** HH:MM
**End Time:** HH:MM

## Objective
[What we set out to accomplish]

## Work Completed
- Task 1 (done)
- Task 2 (in progress)
- Task 3 (blocked - reason)

## Decisions Made
- **Decision:** Rationale

## Files Modified
- `path/to/file.py` - What changed

## Blockers
- Blocker description and impact

---

## Current State
> **This section is the primary handoff point.**
> Write it as if briefing someone picking up mid-task with no other context.

**Status:** [IN PROGRESS | COMPLETE | BLOCKED]
**Active branch:** `CLOUD`

[2-4 sentences describing exactly where work stands. File names, function names, AWS resource names.]

## Next Steps
> **Ordered list. Execute top-to-bottom when picking up this work.**

1. **[Action verb] [specific thing]** - [why / what done-looks-like]
2. **[Action verb] [specific thing]** - [why / what done-looks-like]

**Files to touch next:**
- `path/to/file.py` - [what change is needed]

**Do NOT:**
- [any specific gotcha or action to avoid]
```

### Before Writing the Log

**Always ask the user for clarification on:**
1. **Blockers** - What's blocking progress?
2. **Next steps** - What's the logical next task?
3. **Completion status** - Are we done or is this a checkpoint?

---

## Abilities by Role

| Role | Commit | Push | Deploy AWS | Session Logs | Task Orders |
|------|--------|------|------------|--------------|-------------|
| **RD** | Own page ONLY | No | No | Encouraged | Receives |
| **DE** | Any portal path (ad-hoc) | No | No | **MANDATORY** | Creates + Receives |
| **DS** | Edit + commit locally | No | No | Encouraged | Receives |
| **DT** | Infra only | **Yes** (CLOUD + DEV) — QA gate | **Yes** | Encouraged | Receives |
| **AE** | Infra + pipeline | **Yes** (CLOUD) | **Yes** | Encouraged | Receives |
| **SA** | Docs only | No | No | Encouraged | Creates + Receives |

**Key rules:**
- DTs own ALL pushes and serve as the code review / QA gate before anything reaches remote
- DTs are interdisciplinary — any DT can push for any pod if closest to the work
- DEs commit athletically across any portal path but never push
- DS logic always goes cloud-side via DT/AE — never in frontend
- DE session logs are mandatory; all other roles encouraged

---

## Task Order Protocol

### Location

Task orders are stored in the **receiving agent's** `task_orders/` folder:
```
{receiving_agent_folder}/task_orders/{feature_name}.md
```

- One file per feature — **never overwrite into a monolith**
- Over time each agent accumulates many task order files — this is correct
- Flow: Andrew / SA -> branch agents -> leaf agents

### XML Task Order Template

All task orders use this XML structure. Wrap the XML in a markdown file.

```xml
<task_order>
  <metadata>
    <id>{issuing_agent_serial}-{YYYY-MM-DD}-{short_slug}</id>
    <issued_by>{issuing_agent_id}</issued_by>
    <issued_to>{receiving_agent_id}</issued_to>
    <date>{YYYY-MM-DD}</date>
    <status>pending | complete</status>
  </metadata>

  <objective>
    <!-- 1-3 sentences: what needs to be accomplished and why -->
  </objective>

  <scope>
    <pages>
      <!-- list portal pages affected -->
      <page>portal/src/pages/PageName/</page>
    </pages>
    <files>
      <!-- list specific files to create or modify -->
      <file action="create | modify">path/to/file.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1"><!-- specific, testable requirement --></requirement>
    <requirement id="2"><!-- specific, testable requirement --></requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1"><!-- how to verify this is done correctly --></criterion>
    <criterion id="2"><!-- how to verify this is done correctly --></criterion>
  </acceptance_criteria>

  <constraints>
    <!-- things the agent must NOT do, gotchas, dependencies -->
    <constraint><!-- e.g., do not modify shared types without DE approval --></constraint>
  </constraints>

  <dependencies>
    <!-- other task orders or agents this depends on -->
    <dependency agent="{agent_id}" task="{task_order_id}" status="pending | complete"/>
  </dependencies>

  <deliverables>
    <!-- what the agent produces when done -->
    <deliverable type="commit | document | spec"><!-- description --></deliverable>
  </deliverables>
</task_order>
```

### Task Order Completion Protocol

- **The receiving agent marks their own task order as `complete`** by editing the `<status>` field when done
- Status has only two values: `pending` (default) and `complete`
- Tier 1/2 agents review completion status of task orders they issued as part of their startup protocol
- This is the "done signal" — no separate notification needed

### Example Task Order Filename

```
org/tier3_junior/0.0.14_RD_AdvisorIntelligence/task_orders/rolling_flows_chart_redesign.md
```

---

## DS Deliverables

Data Scientists produce technical documents, investigation reports, and specs. These go in:
```
{ds_agent_folder}/deliverables/{descriptive_name}.md
```

DS deliverables are referenced in SA/DE task orders as output destinations.

---

## Thread Participation

You may be invoked as a participant in a conversation thread. When this happens, your prompt will contain thread instructions, context material, and previous messages from other agents. Follow the thread protocol defined in `org/threads/README.md`.

**Key rules for thread participation:**

- Write ONLY your own message file (`messages/{NNN}.md`)
- Do NOT modify THREAD.json, TURN.json, CONTEXT.json, or other agents' messages
- Set your signal in the YAML frontmatter: `continue`, `converge`, or `escalate`
- Stay in your role -- do not impersonate other agents
- Be concrete: name files, functions, resource names. Avoid vague summaries.
- If it is your last turn, your signal MUST be `converge`

**Thread orchestration** (creating and running threads) is a Tier 1/2 ability. Tier 3 agents participate only.

**Thread receipts** are saved to your `threads/` folder after each completed thread:
```
{your_agent_folder}/threads/YYYY-MM-DD_{other_serials}_{topic_slug}.md
```

### Agent Folder Structure

Every agent has these standard folders:
```
{agent_folder}/
  README.md        # Identity, role, responsibilities
  prompt.md        # Scoped persona prompt
  logs/            # Session logs (YYYY-MM-DD/descriptive_name.md)
  task_orders/     # Received task orders (feature_name.md)
  threads/         # Thread receipts (auto-populated by orchestrator)
```

---

## Quick Reference

- **Documentation:** `docs/` directory mirrors project structure
- **Logs:** Update at natural breakpoints in your agent's logs folder
- **Decisions:** Always ask when multiple approaches exist
- **Files:** Ask before reorganizing or deleting
- **Dependencies:** Ask before installing packages
- **Security:** Never expose credentials
- **Terraform binary:** `.tools/terraform.exe`
- **Bun:** `/c/Users/AndrewBerman/.bun/bin/bun`
- **Git Bash PATH note:** `export MSYS_NO_PATHCONV=1` before commands with `/` paths
