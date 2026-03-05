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

**Example:** `org/tier3_junior/0.1.1_RD_MarketPerformance/logs/2026-03-02/chart_component_refactor.md`

### Base Log Template

```markdown
# [Thesis Title] — [Agent ID]

**Date:** YYYY-MM-DD
**Start Time:** HH:MM
**End Time:** HH:MM

## Objective

[1-3 sentences: what was set out to accomplish and why. Name the feature, bug, or investigation.]

---

## Work Completed

[Organize into numbered sections for distinct pieces of work. Use tables where data is structured.]

### 1. [First work unit]

[Narrative + table or code block as appropriate. Be specific: function names, S3 paths, commit hashes, actual output.]

### 2. [Second work unit]

...

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| [What was decided] | [Why — include alternatives considered if significant] |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `path/to/file.py` | What changed | Yes — `abc1234` / No — local only |

---

## Blockers

- [Blocker description, impact, and who can unblock it]

---

## Current State

> **Primary handoff point. Write as if briefing someone with zero prior context.**

**Status:** IN PROGRESS | COMPLETE | BLOCKED
**Active branch:** `CLOUD`

[2-4 dense sentences. Name specific files, functions, AWS resource names, commit hashes, S3 paths. Avoid vague summaries.]

---

## Next Steps

> Ordered list. Top-to-bottom execution order. Tag with [Agent] when handing off to another agent.

1. **[Action verb] [specific thing]** — [why / what done looks like]
2. **[Dashboard Engineer] [specific action]** — [cross-agent handoff]
3. **[DevOps] [specific action]** — [cross-agent handoff]

**Files to touch next:**
- `path/to/file.py` — [what change is needed]

**Do NOT:**
- [Specific anti-pattern to avoid — name the wrong command, wrong path, wrong approach]
- [Another gotcha]
```

---

### Role-Specific Log Additions

Each role extends the base template with additional sections suited to their work.

**DE (Dashboard Engineer) — add to header and Files Modified:**
```markdown
**Portal DEV commits:** `abc1234` → `def5678` → `ghi9012`
**Workspace CLOUD commit:** `jkl3456`
```
Files Modified table must include the commit hash in the Committed column. When work breaks something, embed a `## Postmortem` section between Work Completed and Decisions Made with: Root Cause, a table of shape/contract mismatches, and Resolution tracking.

**DS (Data Scientist) — add Briefs Written section before Current State:**
```markdown
## Briefs Written

| Brief | Path | Audience |
|-------|------|----------|
| DevOps deploy instructions | `docs/briefs/devops-brief-{feature}.md` | DevOps |
| Data contract for DE | `docs/briefs/dashboard-engineer-{feature}-data-contract.md` | Dashboard Engineer |
| Investigation reference | `docs/briefs/data-scientist-{topic}-investigation.md` | Reference |
```
DS briefs are the formal cross-agent handoff artifact. Write them first; list them here. Next Steps must name the receiving agent in brackets: `[DevOps] Upload scripts to S3`.

**DT/AE (DevOps/AWS Engineer) — replace Work Completed with Deployment Sequence table, add Deployment Tags:**
```markdown
## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Commit source | `abc1234` feat(pipeline): description |
| 2 | build-and-upload.sh | SHA256: `AbCdEf...=` |
| 3 | Commit source map | `def5678` ci: upload artifacts [skip ci] |
| 4 | terraform plan | N changed (description) |
| 5 | terraform apply | N added, N changed, N destroyed |
| 6 | 0-diff plan | No changes. Infrastructure is up-to-date. |
| 7 | Update core doc | deployment_map.xml / pipeline_inventory.xml |
| 8 | record-deploy + tag + push | `ghi9012` ci: record deploy [skip ci], tag `pipeline-vX.Y.Z` |
| 9 | CloudFront invalidation | `INVALIDATION_ID` on `/api/path/*` |

## Verification

[Paste actual output confirming the deploy worked — S3 object sizes, data checksums, API response snippet, or CLI output.]

## Deployment Tags

| Pipeline | Tag | Commit |
|----------|-----|--------|
| {pipeline} | `{pipeline}-vX.Y.Z` | `abc1234` |
```

**RD (React Designer) — add commit reference to header:**
```markdown
**Portal DEV commit:** `abc1234`
```

---

### Before Writing the Log

**Always confirm:**
1. **Status** — COMPLETE, IN PROGRESS, or BLOCKED (one word, no hedging)
2. **Blockers** — what is blocking, who can unblock
3. **Next steps** — ordered, self-contained, cross-agent attributed where needed

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

### Agent Commit Identity (Non-Negotiable)

Every agent commit MUST use the `--author` flag to attribute the commit to the agent, not to the machine user. Git has separate Author and Committer fields — the committer stays as Andrew (repo owner), the author is the agent.

**Format:**
```bash
git commit --author="{agent_serial} <{agent_serial}@opal.agent>" -m "message"
```

**Examples:**
```bash
# RD agent committing page work
git commit --author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>" \
  -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- fix nomenclature"

# DT agent committing infra work
git commit --author="0.1.0_DT_MarketIntelligence <0.1.0_DT_MarketIntelligence@opal.agent>" \
  -m "feat(news-pipeline): update trending scanner timeout"

# DE agent committing portal work
git commit --author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>" \
  -m "0.4.0_DE_ClientPlatform: fix advisor intelligence API endpoint wiring"

# SA agent committing docs/org work
git commit --author="1.0.0_SA_CTO <1.0.0_SA_CTO@opal.agent>" \
  -m "org(1.0.0_SA_CTO): cross-pod API contract spec"
```

**Why this matters:**
- `git log --format='%an'` shows which agent authored each commit
- `git log --author="0.4.0"` filters to a specific agent's work
- GitHub displays the author distinctly from the committer
- DE launch protocol (`git log --grep`) and thread commit injection both depend on agent attribution

**Never** commit without `--author`. If you see a commit attributed to the machine user, it was made outside the agent system.

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
    <!-- If this task order was produced from a project thread, include: -->
    <thread_serial>{PROJECT_CODE}-{NNN}</thread_serial>  <!-- e.g., ADVI_V1VERS-004 -->
    <thread_ref>org/threads/{thread_id}/</thread_ref>
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

### Task Order Filename Convention

**From a project thread** (top-down, Tier 1/2 initiated):
```
{agent_folder}/task_orders/{PROJECT_CODE}-{NNN}-{feature_slug}.md
```
The `{PROJECT_CODE}-{NNN}` prefix is the thread serial that produced this task order.
This links the task order back to the thread receipt and the project file.

Project code format: `{MACRO}_{6CHAR}` (e.g., `ADVI_V1VERS`, `ADVI_YANGV2`).
Macro codes are in `org/projects/MACRO_CODES.md`. Project codes are registered in `org/projects/REGISTRY.md`.

Examples:
```
org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_V1VERS-004-adv_drill.md
org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_V1VERS-004-continuous_nna_rendering.md
```

**Ad-hoc** (no project / lateral between agents):
```
{agent_folder}/task_orders/{feature_slug}.md
```
No prefix. Used for work that doesn't trace to a formal project thread.

```
org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/rolling_flows_chart_redesign.md
```

Filtering task orders by project in any agent folder:
```bash
ls org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_V1VERS-*.md   # all V1VERS project work
ls org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_YANGV2-*.md   # all YANGV2 project work
ls org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_*.md          # all ADVI macro work
```

---

## DS Deliverables

Data Scientists produce technical documents, investigation reports, and specs. These go in:
```
{ds_agent_folder}/deliverables/{descriptive_name}.md
```

DS deliverables are referenced in SA/DE task orders as output destinations.

---

## Core Document Maintenance Protocol

Every agent above Tier 3 has a **core document** — a living XML deliverable that represents the current ground truth of their domain. These documents are not written once at activation and forgotten. They must be kept current as work progresses.

### Core Documents by Role

| Role | Core Document | Location |
|------|--------------|----------|
| RD | `page_inventory.xml` | `{agent_folder}/deliverables/` |
| DE | `pod_inventory.xml` | `{agent_folder}/deliverables/` |
| DS | `data_contract.xml` | `{agent_folder}/deliverables/` |
| DT | `deployment_map.xml` | `{agent_folder}/deliverables/` |
| AE | `pipeline_inventory.xml` | `{agent_folder}/deliverables/` |
| SA | `architecture_brief.xml` | `{agent_folder}/deliverables/` |

### Update Trigger (all roles)

Update your core document when you make a **structural change** to your domain:
- New resource, endpoint, file, or data source added
- Existing resource removed or renamed
- Shape or contract of an interface changes
- Configuration change with operational impact (memory, timeout, S3 key)

Do **not** update for cosmetic changes, patch deployments with no contract change, or internal refactors with no external interface change.

### Role-Specific Timing

**RD:** Update `page_inventory.xml` in the same commit as the page code change.

**DE:** Update `pod_inventory.xml` in the same commit as the portal code change that affects the pod's API endpoints, shared components, or page structure.

**DS:** Update `data_contract.xml` at handoff — in the same commit as the Lambda code change, before handing off to DT/AE for deployment. Verify your update against `infra/aws/lambda/ci/lambda-source-map.json` to confirm the deployed version aligns with what you documented. This update is a **gate**: DT should not deploy a Lambda whose output shape changed without a corresponding data_contract.xml update.

**DT:** Update `deployment_map.xml` after `terraform apply` reaches 0-diff, before `git tag`. The update is committed as part of the post-deploy commit sequence:
```
apply → 0-diff → update deployment_map.xml → commit → tag → push --follow-tags
```
Verification: the 0-diff Terraform plan is the proof that state matches your document.

**AE:** Update `pipeline_inventory.xml` after `terraform apply` reaches 0-diff, before `record-terraform-deploy.sh`. Part of the standard deploy sequence:
```
apply → 0-diff → update pipeline_inventory.xml → record-terraform-deploy.sh → commit → tag → push --follow-tags
```
The `current_tag` in `pipeline_inventory.xml` must always match the tag in `CHANGELOG.json`.

### Cross-Agent Consistency

When your change implies another agent's core document is now stale:
- Note it in your session log under "Files Modified"
- Issue a task order to the affected agent if the staleness is significant
- Do **not** edit another agent's core document yourself

Example: DS changes a Lambda output shape → DS updates `data_contract.xml` → DT deploys → DT updates `deployment_map.xml`. Each agent updates their own document; no agent crosses into another's deliverable.

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

**SA and DE agents run thread scripts themselves via the Bash tool. Do NOT ask Andrew to run them.**
When a staging script exists, invoke it directly:
```bash
bash org/threads/staging/run-YYYY-MM-DD-{slug}.sh
```
The orchestrator is fully automated -- it writes messages, advances turns, and deposits
receipts without any human intervention. Andrew is never in the execution loop.

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
  deliverables/    # Core document and other deliverables (Tier 2+ agents)
```

The `deliverables/` folder holds the agent's **core document** (see Core Document Maintenance Protocol below) and any other structured output artifacts.

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
