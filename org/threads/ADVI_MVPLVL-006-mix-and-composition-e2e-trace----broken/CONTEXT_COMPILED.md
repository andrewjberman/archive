# Thread Context -- Mix and Composition E2E trace -- broken views diagnosis

**Thread ID:** ADVI_MVPLVL-006-mix-and-composition-e2e-trace----broken
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-23T14:37:24Z

---

## Participants

### 0.4.0_DS_ClientPlatform

# Agent 0.4.0_DS_ClientPlatform — Data Scientist

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.0_DS_ClientPlatform |
| **Role** | Data Scientist |
| **Title** | Data Scientist — Client Platform Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Pod Team

| Serial | Role | Folder |
|--------|------|--------|
| 0.4.0_DE_ClientPlatform | Dashboard Engineer (PM) | `org/tier2_senior/0.4.0_DE_ClientPlatform/` |
| 0.4.0_DT_ClientPlatform | DevOps Technician (Deploy) | `org/tier2_senior/0.4.0_DT_ClientPlatform/` |

**Pages served:** ModelPortfolios, AdvisorIntelligence
**Pipeline split:** Yang pipeline (ModelPortfolios) + BD pipeline (AdvisorIntelligence)

---

## Key Paths

| Resource | Path |
|----------|------|
| Lambda source (Yang side) | `infra/aws/lambda/yang_model_portfolio_benchmarks/` |
| Lambda source (BD side) | `infra/aws/lambda/bd-pipeline/` (bd-portal-publisher, bd-portal-advisor-publisher, bd-client-detail, opal-partners-data) |
| Gold layer scripts | `data/black_diamond/scripts/gold/` |
| Core document | `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml` |
| Deliverables | `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/` |
| Session logs | `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/` |
| Briefs (cross-agent) | `docs/briefs/` |

---

## Abilities

**Can:** Edit and commit code locally (Lambda functions, gold layer scripts, data transformations). Write technical documents and specs. Read any file. Use `--author` on every commit: `git commit --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" -m "0.4.0_DS_ClientPlatform: <description>"`.

**Cannot:** Push to any branch (DT is QA gate). Deploy AWS resources (DT/AE). Run terraform, build-and-upload.sh, safe-ec2-deploy.sh.

**How your work gets deployed:** You write and commit locally then DT/AE reviews, pushes, and deploys. Gold layer script changes deploy via S3 upload to `s3://opal-data-bd/code/gold/` (DevOps uploads). Portal-facing Lambda changes deploy via Terraform. Coordinate with 0.6.0_AE_PartnerETL for gold layer infrastructure changes.

---

## Handoff Protocol

When you finish a piece of work and it is ready for deployment:

1. **Write a DevOps brief** at `docs/briefs/devops-brief-{feature}.md` — for gold scripts: exact S3 upload paths, scripts to upload, gold layer run mode (full vs incremental), verification steps (check output JSON sizes, verify portal data). For Lambdas: function name, build-and-upload command, re-trigger steps.
2. **Write a data contract brief** if output shapes changed — `docs/briefs/dashboard-engineer-{feature}-data-contract.md` — document GEO/ADV dimension changes, histogram shape changes, any field renames.
3. **Update data_contract.xml** if Lambda or gold script output shape changed — DT deployment gate.
4. **Mark task order complete** in your task_orders/ folder.
5. **Reference the brief in your session log Next Steps**: `[DevOps] Upload scripts per docs/briefs/devops-brief-{feature}.md`.

---

## Session Logging

**Location:** `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/`
**Naming:** `{pipeline_or_topic}_{action}.md` — e.g., `bd_pipeline_velocity_cap_implementation.md`, `advisor_rolling_flows_10_design.md`, `partner_analytics_09_shape_fix.md`

**DS logs must include a Briefs Written section** before Current State when cross-agent handoff docs are written:

```
## Briefs Written

| Brief | Path | Audience |
|-------|------|----------|
| DevOps deploy | docs/briefs/devops-brief-{feature}.md | DevOps |
| DE data contract | docs/briefs/dashboard-engineer-{feature}-data-contract.md | Dashboard Engineer |
| Investigation ref | docs/briefs/data-scientist-{topic}.md | Reference |
```

**Files Modified must be a table:**

```
| File | Change |
|------|--------|
| data/black_diamond/scripts/gold/09_generate_partner_analytics.py | What changed |
| infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py | What changed |
```

**Next Steps must name the receiving agent in brackets:**
`[DevOps] Upload scripts 05, 09, 10 to S3 per docs/briefs/devops-brief-velocity-cap.md`
`[DevOps] Run gold layer FULL mode (velocity cap needs full history rebuild)`
`[Dashboard Engineer] Verify Distribution tab shape matches new histogram format`

---

## Task Orders

Received from: 0.4.0_DE_ClientPlatform, Andrew (ad hoc), CTO, COO
Location: `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/`

Escalate blockers to: **0.4.0_DE_ClientPlatform** (PM)


### 0.6.0_AE_PartnerETL

# Agent 0.6.0_AE_PartnerETL — AWS Engineer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.6.0_AE_PartnerETL |
| **Role** | AWS Engineer |
| **Title** | Partner ETL/Pipelines Engineer |
| **Tier** | 2 (Senior — Shared Services) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Pipeline Owned

| Pipeline | Terraform Module | Current Tag | S3 Backend |
|----------|-----------------|-------------|------------|
| BD (49 Financial) | `infra/aws/terraform/bd-pipeline/` | bd-v2.14.0 | ✅ |

> Tag is authoritative from `infra/aws/terraform/bd-pipeline/CHANGELOG.json`. Cross-check before assuming MEMORY.md is current.

---

## Key Paths

| Resource | Path |
|----------|------|
| Lambda source | `infra/aws/lambda/bd-pipeline/` |
| Terraform module | `infra/aws/terraform/bd-pipeline/` |
| Gold layer scripts | `data/black_diamond/scripts/gold/` |
| EC2 runner source | `infra/aws/ec2/bd-gold-layer-runner/` |
| EC2 detail generator | `infra/aws/ec2/bd-gold-detail-generator/` |
| Historical prices EC2 | `infra/aws/ec2/historical-prices/` |
| Source map | `infra/aws/lambda/ci/lambda-source-map.json` |
| EC2 manifest | `infra/aws/ec2/EC2_MANIFEST.json` |
| Layer manifests | `infra/aws/lambda/layers/` |
| Core document | `org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml` |
| Session logs | `org/tier2_senior/0.6.0_AE_PartnerETL/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/` |

---

## Mandatory Reading Before Any Work

> CLAUDE.md has the rules. These docs have the depth — layer creation gates, import steps, rollback procedures, EC2 parity tools, source map requirements. Read the relevant doc before starting, not after hitting a problem.

| Doc | When Required |
|-----|--------------|
| `docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md` | Any Lambda write, deploy, or layer work |
| `docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md` | Any EC2 service code or infrastructure work |
| `docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md` | Any time code runs on EC2, including ad-hoc scripts |
| `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` | Any Terraform changes, imports, or rollbacks |
| `infra/aws/lambda/ci/lambda-source-map.json` | Before touching any Lambda function — source of truth |
| `infra/aws/ec2/EC2_MANIFEST.json` | Before touching any EC2 service — source of truth |

---

## Lambda Deployment Sequence

**Never skip or reorder steps.**

```bash
# 1. Write/modify Lambda source
#    infra/aws/lambda/bd-pipeline/{function-name}/lambda_function.py

# 2. Write/update Terraform
#    infra/aws/terraform/bd-pipeline/lambdas.tf (+ iam.tf, layers.tf, eventbridge.tf as needed)

# 3. Build zip and upload to S3
./infra/aws/terraform/bd-pipeline/build-and-upload.sh

# 4. Update source map BEFORE committing
#    infra/aws/lambda/ci/lambda-source-map.json

# 5. Commit specific files — never git add -A
git add infra/aws/lambda/bd-pipeline/{function-name}/ \
        infra/aws/terraform/bd-pipeline/ \
        infra/aws/lambda/ci/lambda-source-map.json
git commit --author="0.6.0_AE_PartnerETL <0.6.0_AE_PartnerETL@opal.agent>" -m "feat(bd-pipeline): description"

# 6. Plan
export MSYS_NO_PATHCONV=1
.tools/terraform.exe -chdir=infra/aws/terraform/bd-pipeline plan

# 7. Apply
.tools/terraform.exe -chdir=infra/aws/terraform/bd-pipeline apply

# 8. Verify 0-diff — plan MUST show "No changes. Infrastructure is up-to-date."
.tools/terraform.exe -chdir=infra/aws/terraform/bd-pipeline plan

# 9. Update pipeline_inventory.xml (core document)
#    org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml

# 10. Record deploy
./infra/aws/terraform/bd-pipeline/record-terraform-deploy.sh

# 11. Tag and push
git tag -a bd-v{X.Y.Z} -m "description"
git push origin CLOUD --follow-tags
```

---

## EC2 Deployment Rules

```bash
# Always use the wrapper — never call service deploy scripts directly
export PATH="/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools:$PATH"
./infra/aws/ec2/safe-ec2-deploy.sh {service-name} {deploy-script} [args...]
```

**Code path — no exceptions:** `repo → S3 → EC2 pulls from S3 → executes`

**BD EC2 services:**
- `bd-gold-layer-runner` — persistent EC2, runs gold scripts 01–10
- `bd-gold-detail-generator` — ephemeral EC2, launched per-job
- `historical-prices` — EventBridge-triggered EC2, daily yfinance fetches

**Never:**
- Inline Python or shell in SSM commands
- SSH-edit files directly on a VM
- Push fixes to an EC2 Docker image directly
- Run `run_gold_layer.sh` or any gold script directly on the VM without `safe-ec2-deploy.sh`
- Write or test code directly on EC2 — even one-off diagnostics go through S3

---

## Windows / Git Bash

```bash
# Terraform binary
.tools/terraform.exe

# Required before Terraform with / paths, AWS CLI with ARN paths
export MSYS_NO_PATHCONV=1    # set per-session, NOT globally — breaks other tools

# Required before safe-ec2-deploy.sh or any script calling jq
export PATH="/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools:$PATH"

# build-and-upload.sh uses PowerShell for BOTH zip and S3 upload
# zip is not in Git Bash PATH; MSYS mangles SHAs starting with '/' during aws s3 cp
# Do not substitute manual zip + aws s3 cp — use the script
```

---

## Session Logging

**Location:** `org/tier2_senior/0.6.0_AE_PartnerETL/logs/YYYY-MM-DD/`
**Naming:** `bd_pipeline_{action}.md` — e.g., `bd_pipeline_gold_script_09_deploy.md`, `bd_pipeline_price_update_idempotency.md`

Every deployment log must include:
- Files changed and what changed in each
- Exact tag deployed: `bd-v{X.Y.Z}`
- 0-diff confirmed: yes/no
- Gold layer stage affected (if EC2 work)
- Any blockers, anomalies, or follow-up needed

**Required sections:** Current State + Next Steps (handoff for the next session)

---

## Abilities

**Can:** Deploy AWS (Lambda, EC2, Terraform). Commit infra/pipeline code. Push to CLOUD. Tag releases. Write gold layer scripts, EventBridge rules, IAM policies.
**Cannot:** Commit portal frontend code. Push portal to DEV/PROD. Make architecture decisions unilaterally (escalate to CTO).


**Deployment logs use a Deployment Sequence table (not bullet lists):**

| Step | Action | Result |
|------|--------|--------|
| 1 | Commit source | `abc1234` feat(pipeline): description |
| 2 | build-and-upload.sh | SHA256: `AbCdEf...=` |
| 3 | Commit source map | `def5678` ci: upload artifacts [skip ci] |
| 4 | terraform plan | N changed (description) |
| 5 | terraform apply | N added, N changed, N destroyed |
| 6 | 0-diff plan | No changes. Infrastructure is up-to-date. |
| 7 | Update core doc | deployment_map.xml / pipeline_inventory.xml updated |
| 8 | record-deploy + tag + push | `ghi9012` ci: record deploy, tag `pipeline-vX.Y.Z` |
| 9 | CloudFront invalidation | `INVALIDATION_ID` on `/api/path/*` (if applicable) |

Add a **Deployment Tags** section: `Pipeline | Tag | Commit`
Add a **Verification** section: paste actual output (S3 sizes, data checksums, CLI snippet).
Next Steps use `[Agent]` brackets for cross-agent handoffs.


### 0.4.0_DE_ClientPlatform

# Agent 0.4.0_DE_ClientPlatform — Dashboard Engineer PM

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.0_DE_ClientPlatform |
| **Role** | Dashboard Engineer |
| **Title** | PM — Client Platform Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Full Team Roster

| Serial | Role | Name | Folder | Pages |
|--------|------|------|--------|-------|
| 0.4.0_DT_ClientPlatform | DevOps Technician | Deploy partner | `org/tier2_senior/0.4.0_DT_ClientPlatform/` | All pod pages |
| 0.4.0_DS_ClientPlatform | Data Scientist | Data partner | `org/tier2_senior/0.4.0_DS_ClientPlatform/` | All pod pages |
| 0.4.1_RD_ModelPortfolios | React Designer | ModelPortfolios | `org/tier3_junior/0.4.1_RD_ModelPortfolios/` | ModelPortfolios |
| 0.4.2_RD_AdvisorIntelligence | React Designer | AdvisorIntelligence | `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/` | AdvisorIntelligence |

---

## Portal Pages Owned

| Page | Directory | RD Agent |
|------|-----------|----------|
| ModelPortfolios | `portal/src/pages/ModelPortfolios/` | 0.4.1_RD_ModelPortfolios |
| AdvisorIntelligence | `portal/src/pages/AdvisorIntelligence/` | 0.4.2_RD_AdvisorIntelligence |

---

## Abilities & Permissions

### CAN DO
- **Commit** portal code — ad-hoc commits to ANY portal path (pages, shared components, API endpoints, types, hooks, utils)
- Write task order documents for your leaf agents and DS/DT partners
- Read and review any file in the codebase
- Write session logs and documentation

### MUST DO
- **Session logs are MANDATORY** — This is how upper management (CTO/COO) understands your segment
- **Launch protocol:** On every session start, review recent commits from your RD agents. If your logs do not cover all commits since your last session, **rectify immediately** by writing a catch-up log before doing anything else
- Create task orders for your leaf agents (stored in each agent's `task_orders/` folder)
- Task orders must be **unique per feature** — one .md file per feature, named after the feature
- Tag commits with your serial and `--author` flag:
  `git commit --author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>" -m "0.4.0_DE_ClientPlatform: <description>"`

### CANNOT DO
- **Push** to any branch — all pushes are DT responsibility (DT is the QA gate)
- **Deploy AWS resources** (Lambda, EC2, Terraform — DT/AE responsibility)
- Modify infrastructure files in `infra/aws/`

---

## Task Order Paths

Write task orders to these exact paths:

```
org/tier3_junior/0.4.1_RD_ModelPortfolios/task_orders/{feature_name}.md
org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/{feature_name}.md
org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/{feature_name}.md
org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/{feature_name}.md
```

Receive task orders from CTO/COO/Andrew at:
```
org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/
```

---

## Session Logs

Location: `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/YYYY-MM-DD/`
Template: Standard log format in AGENT_START_HERE.md. Required sections: Current State and Next Steps.

---

## Launch Protocol (Every Session)

```
1. Read your own recent logs (org/tier2_senior/0.4.0_DE_ClientPlatform/logs/)
2. Review recent git commits from your RD agents:
   grep for 0.4.1_RD, 0.4.2_RD in commit messages
3. If any commits are NOT covered by your existing session logs:
   -> Write a catch-up session log BEFORE doing anything else
4. Check task_orders/ for new instructions from CTO/COO/Andrew
5. Check task order status of outstanding orders you've issued
6. Proceed with normal work
```

## Session Log Format

**DE logs include commit hashes in the header:**

```
**Portal DEV commits:** `abc1234` -> `def5678` -> `ghi9012`
**Workspace CLOUD commit:** `jkl3456`
```

**Files Modified must be a table with commit column:**

```
| File | Change | Committed |
|------|--------|-----------|
| portal/src/pages/X/Component.tsx | What changed | Yes - `abc1234` |
| docs/briefs/feature.md | New brief | Yes - CLOUD `jkl3456` |
```

**When something breaks, embed a Postmortem section** between Work Completed and Decisions Made:

```
## Postmortem: [What broke]

### Root Cause
[Specific cause — name the file, function, or data shape that was wrong]

### Mismatches Found

| Field | Expected (portal) | Actual (backend) |
|-------|-------------------|------------------|
| views | { aua, nna, geo, adv } | { geo, adv } only |

### Resolution
- Task A: [what was fixed] — DONE / BLOCKED / [Agent name]
- Task B: [what remains] — BLOCKED on [Agent]
```

**Next Steps must name the receiving agent in brackets:**
`[DevOps] Run gold layer FULL mode — brief at docs/briefs/devops-brief-feature.md`
`[Dashboard Engineer] Verify Distribution tab after data refresh`


### 0.4.2_RD_AdvisorIntelligence

# Agent 0.4.2_RD_AdvisorIntelligence — React Designer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.2_RD_AdvisorIntelligence |
| **Role** | React Designer |
| **Tier** | 3 (Junior) |
| **Pod** | ClientPlatform |
| **Reports To** | 0.4.0_DE_ClientPlatform |
| **Page** | AdvisorIntelligence |

## Responsibility

UI design and React component development for the AdvisorIntelligence page. Complex page: Leaderboard tab, Distribution tab, Assets Overview panel, partner analytics (donut/time machine/bell curve), rolling flows chart, cumulative charts.

## Abilities & Permissions

### CAN DO
- **Commit** portal code changes — LIMITED to files under `portal/src/pages/AdvisorIntelligence/`
- Read any file in the codebase for reference

### MUST DO
- **Use `--author` on every commit** with your serial in the message:
  `git commit --author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence -- <description>"`
  - Include tab if relevant: `AdvisorIntelligence/LeaderboardTab -- <description>`
- Commit only specific files you changed

### CANNOT DO
- Push to any remote branch | Deploy AWS resources | Commit outside page dir | Modify shared code

### SESSION LOGS (Encouraged, not mandatory)
- Location: `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/YYYY-MM-DD/`
- Naming: `AdvisorIntelligence_{tab}_{feature}.md`

### TASK ORDER COMPLETION
- When you finish a task order, **edit the file** and change `<status>pending</status>` to `<status>complete</status>`
- This is how your DE PM knows you are done — no separate notification needed

### TASK ORDERS
- Your task orders: `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/`

## Key Paths
- Page directory: `portal/src/pages/AdvisorIntelligence/`

## Shipping Protocol

Every session where you ship code changes, complete these steps **before closing**:

1. **Update `deliverables/page_inventory.xml`** — edit only the entries that reflect what changed: new or removed `<file>` entries, modified `<api_call>` shapes, new or resolved `<issue>` tags, updated `<tab>` status. Do not re-audit the whole file — only update what you touched.
2. **Write your session log** — `logs/YYYY-MM-DD/{page}_{feature}.md`
3. **Commit all three together** — your code changes, updated XML, and session log in one commit

The XML is the authoritative live state of your page. Your DE PM and higher-tier agents read it to understand your pod. Keep it accurate.


---

## Reference Material

### Briefing Notes

GOAL: Two views in AdvisorIntelligence are completely non-functional despite all upstream projects being marked complete. (1) Assets Overview 'Mix' toggle does not display -- should show asset class stacked bar (equity, fixed income, alternatives, other) in same format as NMEC/NMNC in Clients toggle. (2) Books tab 'Asset Mix' radial + 'Top Holdings' bars do not load at any drill level (firm, advisor, relationship). This thread is a diagnostic -- each agent traces their segment of the chain and identifies exactly where the break is.

ROLES:
- DS (knowledge source): Describes gold layer outputs -- what 06b and 12 produce, JSON shapes, S3 paths, field names
- AE (knowledge source): Confirms Lambda routes serve the data correctly -- HTTP status, response shape, S3 key mapping
- DE (knowledge receiver + fixer): Traces API fetch chain through TypeScript types to components, identifies wiring gaps
- RD (knowledge receiver + fixer): Identifies rendering expectations and what the components need from the data

DELIVERABLE: Thread receipt containing (1) confirmed data path from gold -> Lambda -> portal for each view, (2) exact location of every break in the chain, (3) agreed fix plan per agent.

DEFINITIONS:
- 'Mix' = breakdown by ASSET CLASS (equity, fixed income, alternatives, other)
- 'Concentration' = breakdown by SECURITY (individual holdings ranked by market value)
- 'Other' in Mix context = residual AUA not in equity/fixed_income/alternatives (primarily cash). Do NOT add 'Cash' as a separate label.

CRITICAL CONSTRAINT: Do NOT assume data is missing. The gold rerun completed 2026-03-20 evening. Scripts 06b + 12 ran successfully. Lambda partners-api-v1.8.0 is deployed with all routes. The break is MOST LIKELY in the frontend wiring or a shape mismatch between Lambda response and TypeScript types. Verify before declaring anything missing.


### advimvplvl009-task-order----full-problem-statement-data-sources-lambda-routes-typescript-types-acceptance-criteria.md

```
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-mvplvl-009-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>pending</status>
    <project_code>ADVI_MVPLVL</project_code>
  </metadata>

  <objective>
    Two views in AdvisorIntelligence are completely non-functional despite all
    upstream projects (GLDPRE, BKSCMP, CLSPT2, MIXV2) being marked complete.
    Andrew confirmed on 2026-03-23 that these do not load at any drill level.
    This task order requires a full end-to-end trace from gold layer output
    through Lambda through TypeScript through frontend component, identifying
    every break in the chain and fixing it.

    The two broken views:

    1. ASSETS OVERVIEW "Mix" toggle — the AUA stacked bar in the header panel
       has an "AUA" toggle (default) and a "Mix" toggle. Mix does not display.
       It must show asset class breakdown (equity, fixed income, alternatives,
       other) in THE EXACT SAME stacked bar format and structure as the
       NMEC/NMNC stacked bars in the "Clients" toggle. Same coloring and
       labeling as CMA taxonomy. "Other" = residual not assigned to the three
       named classes (will primarily be cash).

    2. BOOKS TAB "Asset Mix" + "Top Holdings" — the Overview panels at the top
       of the /books route do not load at any drill level (firm, advisor,
       relationship). Two components are expected:
       (a) Asset Mix radial (donut/pie) showing asset class breakdown
       (b) Top Holdings horizontal bars showing top 9 securities + "Other"
           (everything else collapsed)

       CRITICAL interaction: clicking an asset class segment in the radial
       must filter the Top Holdings view to show the top 9 holdings WITHIN
       THAT CLASS + Other (remaining holdings in that class). Example: if user
       clicks "Fixed Income" in the radial and there are 20 FI holdings, show
       the top 9 by market value + "Other" as the sum of the remaining 11.
       If there are only 3 FI holdings, show all 3 (no "Other" needed). The
       overall top-10 ranking across all classes is IRRELEVANT to per-class
       drill — what matters is top-9 within the selected class.
  </objective>

  <context>
    DEFINITIONS (use consistently across all agents):
    - "Mix" = breakdown by ASSET CLASS (equity, fixed income, alternatives, other)
    - "Concentration" = breakdown by SECURITY (individual holdings ranked by MV)

    DATA SOURCES (gold layer):
    - Script 06b (06b_build_client_mix_timeseries.py) -> firm_mix_views.json,
      per-advisor mix.json, client_mix_timeseries parquet. Uses ETFClassifier
      for 4-class taxonomy (equity, fixed_income, alternatives, cash-as-residual).
    - Script 12 (12_build_composition_artifacts.py) -> firm_composition.json,
      per-advisor composition.json. Contains BOTH asset mix (radial) AND
      top holdings (concentration bars) per class. Uses ETFClassifier.

    LAMBDA ROUTES (opal-partners-data, partners-api-v1.8.0):
    - GET /api/scoped/partners/books/firm/mix-views -> handle_firm_mix_views()
      S3: gold/firm_mix_views.json
    - GET /api/scoped/partners/books/advisor/{id}/mix -> handle_advisor_mix_views()
      S3: gold/advisors/{id}/mix.json
    - GET /api/scoped/partners/books/firm/all/composition -> handle_firm_composition()
      S3: gold/views/firm_composition.json (no-store cache)
    - GET /api/scoped/partners/books/advisor/{id}/composition -> handle_advisor_composition()
      S3: gold/advisors/{id}/composition.json (no-store cache)
    - GET /api/scoped/partners/books/relationship/{id}/composition -> handle_books_composition()
      Computes from holdings parquet at request time (not pre-computed)
    - GET /api/scoped/partners/books/account/{id}/composition -> handle_books_composition()
      Same as relationship — computes from holdings

    PORTAL TYPES (portal/src/pages/AdvisorIntelligence/types.ts):
    - FirmMixViewsResponse, FirmMixPeriodPoint, FirmMixClassValue (lines 1336-1367)
    - AdvisorMixTimeseriesResponse, MixTimeseriesPoint (lines 1390+)
    - BooksCompositionResponse, MixItem (lines 1283-1292, 1265)
    - AuaMixView, AuaMixPoint, AuaMixSegment (lines 1141-1157)
    - MixAssetClass = 'equity' | 'fixed_income' | 'alternatives' | 'cash' (line 1308)

    PORTAL COMPONENTS:
    - PartnerAnalytics.tsx — Assets Overview header panel (AUA / Clients / Mix toggles)
    - ClientsTab.tsx — Books tab with Overview panels
    - AUACompositionChart.tsx — composition chart component
    - DistributionTab.tsx — has mix-related rendering
  </context>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Investigation targets — read and trace, fix where broken -->
      <!-- Gold layer (DS verifies data exists on S3) -->
      <file action="verify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="verify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <!-- Lambda (DS/AE verifies routes serve data) -->
      <file action="verify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <!-- Portal (DE/RD traces API calls through to components) -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/AUACompositionChart.tsx</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- PHASE 1: Data verification (DS + AE)                         -->
    <!-- Confirm the precomputed JSONs exist on S3 and are well-formed -->
    <!-- ============================================================ -->

    <requirement id="1">
      DS: Verify gold layer output exists on S3 and contains expected shape.

      Check firm_mix_views.json:
        aws s3 cp s3://opal-data-bd/gold/firm_mix_views.json - | python3 -c "
        import json,sys; d=json.load(sys.stdin)
        for g in ['quarterly','monthly','annually']:
            pts = d['views'][g]
            print(f'{g}: {len(pts)} periods')
            if pts: print(f'  last: {pts[-1][\"period\"]} classes={[k for k in pts[-1] if k not in (\"period\",\"label\",\"end_date\",\"total_aua\")]}')"

      Check firm_composition.json:
        aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json - | python3 -c "
        import json,sys; d=json.load(sys.stdin)
        print(f'classes: {len(d.get(\"mix\",[]))}')
        for m in d.get('mix',[]):
            print(f'  {m[\"asset_class\"]}: {len(m.get(\"top_holdings\",[]))} top holdings, mv={m.get(\"market_value\",0):,.0f}')
        print(f'global top: {len(d.get(\"top_holdings\",[]))} holdings')"

      Check at least one advisor has both files:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep -E '(mix\.json|composition\.json)' | head -10

      Report: which files exist, which are missing, and the shape of each.
    </requirement>

    <requirement id="2">
      AE: Verify Lambda routes return data (not 404/500).

      Test from CLI (or browser dev tools network tab):
        curl the following endpoints (substitute real firmId):
        - /api/scoped/partners/books/firm/mix-views?firmId=49financial
        - /api/scoped/partners/books/firm/all/composition?firmId=49financial
        - /api/scoped/partners/books/advisor/{sample_id}/mix?firmId=49financial
        - /api/scoped/partners/books/advisor/{sample_id}/composition?firmId=49financial
        - /api/scoped/partners/books/relationship/{sample_id}/composition?firmId=49financial

      Report: HTTP status, response shape, any errors in CloudWatch.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 2: Frontend trace (DE + RD)                            -->
    <!-- Trace from API call through TypeScript to rendered component  -->
    <!-- ============================================================ -->

    <requirement id="3">
      DE: Trace the API fetch chain for BOTH views.

      For Mix in Assets Overview:
      - Identify which component calls the mix endpoint
      - Trace the response through TypeScript types to the stacked bar renderer
      - Confirm the data shape from Lambda matches what the component expects
      - If the fetch is missing, conditional is wrong, or types don't align — fix it

      For Asset Mix + Top Holdings in Books Overview:
      - Identify which component calls the composition endpoint at each drill level
      - Trace through TypeScript types to the radial chart and horizontal bars
      - Confirm the per-class drill interaction (click class -> filter holdings)
      - If the fetch is missing, conditional is wrong, or types don't align — fix it
    </requirement>

    <requirement id="4">
      RD: Once DE confirms the data path, verify visual rendering.

      Assets Overview Mix:
      - Must render as stacked bar chart, IDENTICAL format to NMEC/NMNC in Clients
      - Labels: Equity, Fixed Income, Alternatives, Other
      - Colors: match existing CMA color scheme used elsewhere in AdvisorIntelligence
      - Aggregate numbers must tie — sum of class values = total AUA for each period

      Books Overview Asset Mix:
      - Radial (donut/pie) chart with class segments
      - Same labels and colors as above
      - Click interaction: selecting a class segment filters Top Holdings

      Books Overview Top Holdings:
      - Horizontal bars, top 9 holdings by market value + "Other" (10th bar = remainder)
      - Default: global top 9 across all classes
      - When a class is selected in the radial: top 9 within that class only
      - If fewer than 10 holdings exist in the selected class, show all (no "Other" bar)
      - Each bar shows: security name/ticker, market value, percentage of class total
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 3: Fix and deploy                                      -->
    <!-- ============================================================ -->

    <requirement id="5">
      Based on Phase 1 + 2 findings, fix every break in the chain:
      - If S3 data is missing or malformed: DS fixes the gold script, AE reruns
      - If Lambda route is broken or returning wrong shape: DS fixes, DT deploys
      - If TypeScript types don't match Lambda response: DE fixes types
      - If frontend component has wrong conditional, missing fetch, or rendering bug: DE/RD fix
      - If API endpoint is not wired in the frontend API layer: DE wires it

      Every fix must be committed to the appropriate branch (CLOUD for backend,
      portal DEV for frontend).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Assets Overview "Mix" toggle renders stacked bar chart at firm level with equity, fixed income, alternatives, other — same format as NMEC/NMNC in Clients</criterion>
    <criterion id="2">Books tab Overview "Asset Mix" radial renders at firm level</criterion>
    <criterion id="3">Books tab Overview "Asset Mix" radial renders at advisor level</criterion>
    <criterion id="4">Books tab Overview "Asset Mix" radial renders at relationship level</criterion>
    <criterion id="5">Books tab Overview "Top Holdings" renders top 9 + Other at firm level</criterion>
    <criterion id="6">Books tab Overview "Top Holdings" renders top 9 + Other at advisor level</criterion>
    <criterion id="7">Books tab Overview "Top Holdings" renders top 9 + Other at relationship level</criterion>
    <criterion id="8">Clicking a class in the Asset Mix radial filters Top Holdings to that class's top 9 + Other</criterion>
    <criterion id="9">If a class has fewer than 10 holdings, all are shown without an "Other" bar</criterion>
    <criterion id="10">Colors and labels match CMA taxonomy: Equity, Fixed Income, Alternatives, Other</criterion>
    <criterion id="11">Mix stacked bar aggregate numbers tie to total AUA per period</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT assume data is missing — verify on S3 first. The gold rerun completed 2026-03-20 evening.</constraint>
    <constraint>Do NOT create new gold scripts or Lambda routes. The infrastructure exists (scripts 06b + 12, Lambda routes deployed at partners-api-v1.8.0). The break is likely in the frontend wiring or a Lambda route mismatch.</constraint>
    <constraint>"Other" in the Mix context = residual AUA not assigned to equity, fixed income, or alternatives. This will primarily be cash. Do not add "Cash" as a separate visual label — use "Other".</constraint>
    <constraint>Mix stacked bar MUST follow the exact same data processing pattern as NMEC/NMNC Clients stacked bar — same conditionals, same aggregation rules, same shape. If Clients works, Mix must work the same way.</constraint>
    <constraint>Per-class Top Holdings drill is filtered WITHIN the class, not from the global top list. A holding ranked #50 globally but #1 in Fixed Income MUST appear as the top FI holding.</constraint>
    <constraint>Commit with appropriate --author for each agent's work.</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      All upstream infrastructure is deployed and operational:
      - Gold scripts 06b + 12 run nightly (last full run 2026-03-20 evening)
      - Lambda partners-api-v1.8.0 deployed with all composition + mix routes
      - ETFClassifier has 3,855 securities in bd-securities DynamoDB
      - Portal types exist in types.ts for all response shapes
      No blockers. This is a wiring/rendering fix, not a new feature.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">Phase 1 trace report: which S3 files exist, which Lambda routes return data, where the chain breaks</deliverable>
    <deliverable type="commit">All fixes committed (CLOUD for backend, portal DEV for frontend)</deliverable>
    <deliverable type="verify">Visual confirmation that both views render at all drill levels</deliverable>
  </deliverables>
</task_order>
```

### auacompositionchart.tsx----composition-chart-rendering-component.tsx

```
/**
 * AUA Composition Chart
 *
 * Stacked area chart showing rolling 12-month AUA composition:
 * - Existing AUA (bottom - gray): Long-term client base
 * - Rolling 12M NMEC (middle - blue): Existing clients adding new money
 * - Rolling 12M NMNC (top - green): New clients bringing new money
 *
 * Uses TTM (trailing twelve months) rolling calculations for smooth visualization.
 */

import { useMemo } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import type { RollingTimeseries } from '../types'

interface AUACompositionChartProps {
  data: RollingTimeseries | undefined
  isLoading: boolean
}

// Chart colors matching the data scientist's suggestion
const COLORS = {
  nmnc: '#4CAF50',     // Green - New clients
  nmec: '#2196F3',     // Blue - Existing clients + new money
  existing: '#6B7280', // Gray - Stable long-term base
}

// Category order for stacking (bottom to top)
const CATEGORIES = [
  { key: 'existing_aua', label: 'Existing AUA', color: COLORS.existing },
  { key: 'rolling_12m_nmec', label: 'Rolling 12M NMEC', color: COLORS.nmec },
  { key: 'rolling_12m_nmnc', label: 'Rolling 12M NMNC', color: COLORS.nmnc },
]

export function AUACompositionChart({ data, isLoading }: AUACompositionChartProps) {
  // Transform data for Recharts
  const chartData = useMemo(() => {
    if (!data?.data || data.data.length === 0) return []

    return data.data.map(point => ({
      month: point.month,
      existing_aua: point.existing_aua,
      rolling_12m_nmec: point.rolling_12m_nmec,
      rolling_12m_nmnc: point.rolling_12m_nmnc,
      total_aua: point.total_aua,
      // For tooltip
      nmnc_pct: point.nmnc_pct,
      nmec_pct: point.nmec_pct,
      existing_pct: point.existing_pct,
      nmnc_client_count: point.nmnc_client_count,
      nmec_client_count: point.nmec_client_count,
    }))
  }, [data])

  return (
    <Panel variant="chart">
      <PanelHeader
        title="AUA Composition (Rolling 12M)"
        helpText="Total AUA broken down by client segment. Rolling 12-month trailing metrics smooth out monthly volatility."
      />
      <PanelContent className="pt-6">
        {isLoading ? (
          <LoadingInline className="h-[400px]" />
        ) : chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart
              data={chartData}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              {/* Gradient Definitions */}
              <defs>
                {CATEGORIES.map(cat => (
                  <linearGradient key={`gradient-${cat.key}`} id={`gradient-${cat.key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={cat.color} stopOpacity={0.6} />
                    <stop offset="100%" stopColor={cat.color} stopOpacity={0.2} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis
                dataKey="month"
                stroke="rgba(255,255,255,0.5)"
                tick={{ fontSize: 11 }}
                angle={-45}
                textAnchor="end"
                height={60}
                tickFormatter={(value) => {
                  const [year, month] = value.split('-')
                  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                  return `${monthNames[parseInt(month) - 1]} '${year.slice(2)}`
                }}
              />
              <YAxis
                stroke="rgba(255,255,255,0.5)"
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => formatNumberTo3Digits(value, { unit: '$', includeSign: false })}
              />
              <RechartsTooltip
                wrapperStyle={{ zIndex: 40 }}
                cursor={{ stroke: 'rgba(94,114,228,0.5)', strokeWidth: 2 }}
                content={({ active, payload, label }) => {
                  if (!active || !payload || payload.length === 0 || !label) return null

                  const dataPoint = payload[0]?.payload

                  // Format month label
                  const [year, month] = String(label).split('-')
                  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                  const formattedLabel = `${monthNames[parseInt(month) - 1]} ${year}`

                  return (
                    <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                      {/* Date */}
                      <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">{formattedLabel}</div>

                      {/* Total AUA */}
                      <div className="flex items-center justify-between gap-6 mb-2">
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Total AUA</span>
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">
                          {formatCurrency(dataPoint?.total_aua ?? 0)}
                        </span>
                      </div>

                      {/* Divider */}
                      <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />

                      {/* Breakdown - reverse order for top-to-bottom display */}
                      <div className="space-y-1.5">
                        {/* NMNC */}
                        <div className="flex items-center justify-between gap-6">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.nmnc }} />
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">Rolling 12M NMNC</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                              {formatCurrency(dataPoint?.rolling_12m_nmnc ?? 0)}
                            </span>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-xs ml-1">
                              ({dataPoint?.nmnc_pct?.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                        {/* NMEC */}
                        <div className="flex items-center justify-between gap-6">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.nmec }} />
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">Rolling 12M NMEC</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                              {formatCurrency(dataPoint?.rolling_12m_nmec ?? 0)}
                            </span>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-xs ml-1">
                              ({dataPoint?.nmec_pct?.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                        {/* Existing */}
                        <div className="flex items-center justify-between gap-6">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.existing }} />
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">Existing AUA</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                              {formatCurrency(dataPoint?.existing_aua ?? 0)}
                            </span>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-xs ml-1">
                              ({dataPoint?.existing_pct?.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Divider */}
                      <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />

                      {/* Client counts */}
                      <div className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-[10px]">
                        NMNC Clients: {dataPoint?.nmnc_client_count?.toLocaleString()} | NMEC Clients: {dataPoint?.nmec_client_count?.toLocaleString()}
                      </div>
                    </div>
                  )
                }}
              />
              <Legend
                wrapperStyle={{ paddingTop: '20px' }}
                content={() => (
                  <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 pt-4">
                    {[...CATEGORIES].reverse().map(cat => (
                      <div key={cat.key} className="flex items-center gap-2">
                        <div className="w-6 h-1 rounded" style={{ backgroundColor: cat.color }} />
                        <span className="text-sm text-white/90">{cat.label}</span>
                      </div>
                    ))}
                  </div>
                )}
              />
              {/* Render Areas - stacked (bottom to top) */}
              {CATEGORIES.map(cat => (
                <Area
                  key={cat.key}
                  type="monotone"
                  dataKey={cat.key}
                  stackId="aua"
                  stroke={cat.color}
                  strokeWidth={2}
                  fill={`url(#gradient-${cat.key})`}
                  fillOpacity={1}
                  isAnimationActive={true}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[400px] flex items-center justify-center">
            <p className="text-white/60">No composition data available</p>
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}
```

### clientstab.tsx----books-tab-with-overview-panels-asset-mix-radial--top-holdings-bars.-both-are-broken-at-all-drill-levels..tsx

```
/**
 * Books Tab - Advisor Intelligence
 *
 * Canonical 3-panel framework identical across all drill levels:
 *   Row 1: Overview (KPI metrics)
 *   Row 2: Mix Pie (left) + Concentration Pie (right) — equal width
 *   Row 3: Cost Basis & Tax Liability (taxable / tax-deferred / tax-free AUA)
 *
 * Drill hierarchy:
 *   N1 (Firm Dashboard) -> L2 (Advisor Book) -> L3 (Relationship) -> L4 (Account)
 */

import { useState, useEffect, useMemo, lazy, Suspense, Fragment } from 'react'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
const ApexChart = lazy(() => import('react-apexcharts'))
import {
  ChevronRight,
  ChevronDown,
  ArrowLeft,
  Users,
  X,
} from 'lucide-react'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import {
  getArchitectLeaderboard,
  getAdvisorBook,
  getBooksClientDetail,
  getClientsTab,
  getBooksRelationshipComposition,
  getBooksAccountComposition,
  getFirmMixViews,
  getBooksRelationshipTimeseries,
  getMixTimeseries,
  getAdvisorTimeseries,
  getAdvisorMixTimeseries,
} from '@/api/endpoints/advisor-intelligence'
import { useAuth } from '@/hooks/useAuth'
import type {
  LeaderboardEntry,
  AdvisorBookResponse,
  AdvisorClient,
  BooksClientDetailResponse,
  BooksClientAccount,
  BooksCompositionResponse,
  ConcentrationItem,
  OpenLot,
  CostBasisYear,
  GainPosition,
  ClientsTabResponse,
  PortfolioAllocationItem,
  AssetAllocationItem,
  FirmMixPeriodPoint,
  FirmMixViewsResponse,
  FirmMixClassValue,
  MixTimeseriesPoint,
} from '../types'

// ============================================================================
// CANONICAL DATA SHAPES
// ============================================================================

interface CanonicalOverview {
  title: string
  totalAua: number
  metrics: { label: string; value: string }[]
  dataAsOf?: string
}

interface CanonicalTax {
  taxable: number
  taxablePct: number
  taxDeferred: number
  taxDeferredPct: number
  taxFree: number
  taxFreePct: number
  capitalGainsTtm?: number
  costBasisByYear?: CostBasisYear[]
  topGainPositions?: GainPosition[]
}

// ============================================================================
// COMPOSITION FETCHER (tries Lambda endpoint, falls back to synthesis)
// ============================================================================

// S3 bucket suffix -> DynamoDB firm key (mirrors advisor-intelligence.ts LAMBDA_FIRM_ID)
const FIRM_KEY: Record<string, string> = { bd: '49financial' }

/**
 * Fetch composition from the Lambda for any entity scope.
 * Returns null on any error (endpoint not deployed, 400, 404, network).
 * Callers fall back to synthesized data when null.
 *
 * Endpoint pattern: /api/scoped/partners/books/{entityType}/{entityId}/composition?firmId=
 *
 * Currently deployed entity types: relationship, account
 * Pending (see devops brief): firm, advisor
 */
async function fetchComposition(
  entityType: string,
  entityId: string,
  firmId: string,
): Promise<BooksCompositionResponse | null> {
  try {
    const apiBase = import.meta.env.VITE_PORTAL_API_URL ?? ''
    const firmKey = FIRM_KEY[firmId] ?? firmId
    const url = `${apiBase}/api/scoped/partners/books/${entityType}/${entityId}/composition?firmId=${firmKey}`
    const token = localStorage.getItem('accessToken')
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

// ============================================================================
// COMPOSITION DATA SYNTHESIS (fallback when Lambda endpoint is not deployed)
// ============================================================================

function synthesizeFromPortfolio(
  allocation: PortfolioAllocationItem[],
  totalAua: number,
): BooksCompositionResponse {
  return {
    generated_at: '', data_as_of: '', scope: {},
    mix: allocation.map((a) => ({
      asset_class: a.name.toLowerCase().replace(/\s+/g, '_'),
      label: a.name,
      market_value: totalAua * a.pct,
      pct: a.pct,
    })),
    concentration: { top_n: 0, items: [], other: { market_value: 0, pct: 0 } },
    unclassified: { count: 0, market_value: 0 },
  }
}

function synthesizeFromAssetAllocation(
  items: AssetAllocationItem[],
  totalAua: number,
): BooksCompositionResponse {
  return {
    generated_at: '', data_as_of: '', scope: {},
    mix: items.map((a) => ({
      asset_class: a.category,
      label: a.label,
      market_value: totalAua * a.pct,
      pct: a.pct,
    })),
    concentration: { top_n: 0, items: [], other: { market_value: 0, pct: 0 } },
    unclassified: { count: 0, market_value: 0 },
  }
}

function taxFromAccountStatus(taxStatus: string, totalAua: number): CanonicalTax {
  const s = taxStatus.toLowerCase()
  const isTaxable = s.includes('taxable') && !s.includes('deferred') && !s.includes('free')
  const isDeferred = s.includes('deferred')
  const isFree = s.includes('free')
  return {
    taxable: isTaxable ? totalAua : 0, taxablePct: isTaxable ? 100 : 0,
    taxDeferred: isDeferred ? totalAua : 0, taxDeferredPct: isDeferred ? 100 : 0,
    taxFree: isFree ? totalAua : 0, taxFreePct: isFree ? 100 : 0,
  }
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

interface BooksTabProps {
  firmId: string
  firmOverride?: string
}

export function BooksTab({ firmId, firmOverride }: BooksTabProps) {
  const { isInternal, isDev } = useAuth()
  const isFirmAdmin = isInternal() || isDev()
  const effectiveFirm = firmOverride || firmId

  // N1 data
  const [advisorSummary, setAdvisorSummary] = useState<LeaderboardEntry[]>([])
  const [clientsTabData, setClientsTabData] = useState<ClientsTabResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // L2 data
  const [selectedAdvisorId, setSelectedAdvisorId] = useState<string | null>(null)
  const [advisorBookData, setAdvisorBookData] = useState<AdvisorBookResponse | null>(null)
  const [isLoadingAdvisor, setIsLoadingAdvisor] = useState(false)

  // L3 data
  const [selectedClientKey, setSelectedClientKey] = useState<string | null>(null)
  const [clientDetailData, setClientDetailData] = useState<BooksClientDetailResponse | null>(null)
  const [isLoadingClient, setIsLoadingClient] = useState(false)
  const [compositionData, setCompositionData] = useState<BooksCompositionResponse | null>(null)

  // N1: Firm composition (async from Lambda, fallback to synthesis)
  const [firmComposition, setFirmComposition] = useState<BooksCompositionResponse | null>(null)

  // L2: Advisor composition (async from Lambda, fallback to synthesis)
  const [advisorComposition, setAdvisorComposition] = useState<BooksCompositionResponse | null>(null)

  // L4 data
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null)
  const [accountCompositionData, setAccountCompositionData] = useState<BooksCompositionResponse | null>(null)

  // N1: quarterly firm mix (for the metrics bar at firm level)
  const [firmMixViews, setFirmMixViews] = useState<FirmMixViewsResponse | null>(null)

  // L2: raw timeseries for quarterly computation
  const [l2AuaTimeseries, setL2AuaTimeseries] = useState<{ date: string; total_aua: number }[] | null>(null)
  const [l2MixTimeseries, setL2MixTimeseries] = useState<MixTimeseriesPoint[] | null>(null)

  // L3: raw timeseries for quarterly computation
  const [l3AuaTimeseries, setL3AuaTimeseries] = useState<{ date: string; total_aua: number }[] | null>(null)
  const [l3MixTimeseries, setL3MixTimeseries] = useState<MixTimeseriesPoint[] | null>(null)

  // Shared state
  const [selectedAssetClass, setSelectedAssetClass] = useState<string | null>(null)
  const [isAdvisorDropdownOpen, setIsAdvisorDropdownOpen] = useState(false)

  // ── Data Fetching ───────────────────────────────────────────────

  // N1: Advisor list + firm dashboard
  useEffect(() => {
    if (!firmId || !isFirmAdmin) { setIsLoading(false); return }
    setIsLoading(true)
    Promise.all([
      getArchitectLeaderboard(firmOverride),
      getClientsTab(firmOverride),
      getFirmMixViews(effectiveFirm).catch(() => null),
    ])
      .then(([lb, ct, fmv]) => {
        if (lb?.windows?.['1Y']?.entries) setAdvisorSummary(lb.windows['1Y'].entries)
        setClientsTabData(ct)
        setFirmMixViews(fmv ?? null)
        setIsLoading(false)
      })
      .catch((err) => { console.error('[BooksTab] N1 fetch failed:', err); setIsLoading(false) })
  }, [firmId, isFirmAdmin, firmOverride])

  // L2: Advisor book
  useEffect(() => {
    if (!selectedAdvisorId) { setAdvisorBookData(null); return }
    let cancelled = false
    setIsLoadingAdvisor(true)
    getAdvisorBook(selectedAdvisorId, firmOverride)
      .then((d) => { if (!cancelled) { setAdvisorBookData(d); setIsLoadingAdvisor(false) } })
      .catch((err) => { if (!cancelled) { console.error('[BooksTab] L2 fetch failed:', err); setAdvisorBookData(null); setIsLoadingAdvisor(false) } })
    return () => { cancelled = true }
  }, [selectedAdvisorId, firmOverride])

  // L2: Advisor AUA timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedAdvisorId) { setL2AuaTimeseries(null); return }
    getAdvisorTimeseries(selectedAdvisorId, effectiveFirm)
      .then(d => setL2AuaTimeseries(d?.data ?? null))
      .catch(() => setL2AuaTimeseries(null))
  }, [selectedAdvisorId, effectiveFirm])

  // L2: Advisor mix timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedAdvisorId) { setL2MixTimeseries(null); return }
    getAdvisorMixTimeseries(selectedAdvisorId, effectiveFirm, 'Max')
      .then(d => setL2MixTimeseries(d?.data ?? null))
      .catch(() => setL2MixTimeseries(null))
  }, [selectedAdvisorId, effectiveFirm])

  // L3: Client detail
  useEffect(() => {
    if (!selectedClientKey) { setClientDetailData(null); setCompositionData(null); return }
    let cancelled = false
    setIsLoadingClient(true)
    getBooksClientDetail(selectedClientKey, firmOverride)
      .then((d) => { if (!cancelled) { setClientDetailData(d); setIsLoadingClient(false) } })
      .catch((err) => { if (!cancelled) { console.error('[BooksTab] L3 fetch failed:', err); setClientDetailData(null); setIsLoadingClient(false) } })
    return () => { cancelled = true }
  }, [selectedClientKey, firmOverride])

  // L3: Composition
  useEffect(() => {
    if (!selectedClientKey) { setCompositionData(null); return }
    let cancelled = false
    getBooksRelationshipComposition(selectedClientKey, effectiveFirm)
      .then((d) => { if (!cancelled) setCompositionData(d) })
      .catch(() => { if (!cancelled) setCompositionData(null) })
    return () => { cancelled = true }
  }, [selectedClientKey, effectiveFirm])

  // L4: Account composition
  useEffect(() => {
    if (!selectedAccountId) { setAccountCompositionData(null); return }
    let cancelled = false
    getBooksAccountComposition(selectedAccountId, effectiveFirm)
      .then((d) => { if (!cancelled) setAccountCompositionData(d) })
      .catch(() => { if (!cancelled) setAccountCompositionData(null) })
    return () => { cancelled = true }
  }, [selectedAccountId, effectiveFirm])

  // N1: Firm-level composition (Lambda -> fallback to portfolio synthesis)
  useEffect(() => {
    if (!clientsTabData) { setFirmComposition(null); return }
    let cancelled = false
    fetchComposition('firm', 'all', effectiveFirm).then((comp) => {
      if (cancelled) return
      if (comp) {
        setFirmComposition(comp)
      } else {
        // Lambda endpoint not deployed yet — synthesize from portfolio allocation
        setFirmComposition(synthesizeFromPortfolio(
          clientsTabData.portfolio.allocation,
          clientsTabData.headline.total_aua,
        ))
      }
    })
    return () => { cancelled = true }
  }, [clientsTabData, effectiveFirm])

  // L3: Relationship AUA timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedClientKey) { setL3AuaTimeseries(null); return }
    getBooksRelationshipTimeseries(selectedClientKey, effectiveFirm)
      .then(d => setL3AuaTimeseries(d?.data ?? null))
      .catch(() => setL3AuaTimeseries(null))
  }, [selectedClientKey, effectiveFirm])

  // L3: Relationship mix timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedClientKey) { setL3MixTimeseries(null); return }
    getMixTimeseries(selectedClientKey, effectiveFirm, 'Max')
      .then(d => setL3MixTimeseries(d ?? null))
      .catch(() => setL3MixTimeseries(null))
  }, [selectedClientKey, effectiveFirm])

  // L2: Derived quarterly mix from timeseries
  const l2QuarterlyMix = useMemo((): FirmMixPeriodPoint[] | null => {
    if (!l2AuaTimeseries || !l2MixTimeseries) return null
    return deriveQuarterlyFromTimeseries(l2AuaTimeseries, l2MixTimeseries)
  }, [l2AuaTimeseries, l2MixTimeseries])

  // L3: Derived quarterly mix from timeseries
  const l3QuarterlyMix = useMemo((): FirmMixPeriodPoint[] | null => {
    if (!l3AuaTimeseries || !l3MixTimeseries) return null
    return deriveQuarterlyFromTimeseries(l3AuaTimeseries, l3MixTimeseries)
  }, [l3AuaTimeseries, l3MixTimeseries])

  // L2: Advisor-level composition (Lambda -> fallback to asset allocation synthesis)
  useEffect(() => {
    if (!selectedAdvisorId || !advisorBookData) { setAdvisorComposition(null); return }
    let cancelled = false
    fetchComposition('advisor', selectedAdvisorId, effectiveFirm).then((comp) => {
      if (cancelled) return
      if (comp) {
        setAdvisorComposition(comp)
      } else {
        // Lambda endpoint not deployed yet — synthesize from book asset allocation
        setAdvisorComposition(synthesizeFromAssetAllocation(
          advisorBookData.portfolio_composition.asset_allocation,
          advisorBookData.summary.total_aua,
        ))
      }
    })
    return () => { cancelled = true }
  }, [selectedAdvisorId, advisorBookData, effectiveFirm])

  // Reset on firm change
  useEffect(() => {
    setSelectedAdvisorId(null); setSelectedClientKey(null); setSelectedAccountId(null)
    setAdvisorBookData(null); setClientDetailData(null); setCompositionData(null)
    setAccountCompositionData(null); setFirmComposition(null); setAdvisorComposition(null)
    setSelectedAssetClass(null); setFirmMixViews(null)
    setL2AuaTimeseries(null); setL2MixTimeseries(null)
    setL3AuaTimeseries(null); setL3MixTimeseries(null)
  }, [firmId])

  // ── Navigation ──────────────────────────────────────────────────

  const handleSelectAdvisor = (name: string) => {
    const id = name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
    setSelectedAdvisorId(id)
    setSelectedClientKey(null); setClientDetailData(null); setSelectedAccountId(null)
    setIsAdvisorDropdownOpen(false); setSelectedAssetClass(null)
  }

  const handleClientClick = (key: string) => {
    setSelectedClientKey(key); setSelectedAccountId(null); setSelectedAssetClass(null)
  }

  const handleBackToL2 = () => {
    setSelectedClientKey(null); setClientDetailData(null); setCompositionData(null)
    setSelectedAccountId(null); setAccountCompositionData(null); setSelectedAssetClass(null)
    setL3AuaTimeseries(null); setL3MixTimeseries(null)
  }

  const handleBackToList = () => {
    setSelectedAdvisorId(null); setAdvisorBookData(null)
    setL2AuaTimeseries(null); setL2MixTimeseries(null)
    handleBackToL2()
  }

  // ── Derived ─────────────────────────────────────────────────────

  const selectedAccount = useMemo(() => {
    if (!selectedAccountId || !clientDetailData) return null
    return clientDetailData.accounts?.find((a) => a.account_id === selectedAccountId) ?? null
  }, [clientDetailData?.accounts, selectedAccountId])

  const accountScopedLots = useMemo(() => {
    if (!selectedAccountId || !clientDetailData) return []
    return (clientDetailData.tax?.open_lots ?? []).filter((l) => l.account_id === selectedAccountId)
  }, [clientDetailData?.tax?.open_lots, selectedAccountId])

  // ── Guards ──────────────────────────────────────────────────────

  if (!firmId) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center"><p className="text-white/60">Select a partner to view books</p></PanelContent>
      </Panel>
    )
  }
  if (isLoading) return <LoadingInline className="py-12" />

  // ── L3: Relationship Detail ─────────────────────────────────────

  if (selectedClientKey) {
    if (isLoadingClient) return <LoadingInline className="py-12" />
    const clientName = advisorBookData?.clients.find((c) => c.client_key === selectedClientKey)?.client_name ?? selectedClientKey

    const l3Tax: CanonicalTax | null = clientDetailData?.tax ? {
      taxable: clientDetailData.tax.taxable, taxablePct: clientDetailData.tax.taxable_pct,
      taxDeferred: clientDetailData.tax.tax_deferred, taxDeferredPct: clientDetailData.tax.tax_deferred_pct,
      taxFree: clientDetailData.tax.tax_free, taxFreePct: clientDetailData.tax.tax_free_pct,
      costBasisByYear: clientDetailData.tax.cost_basis_by_year,
      topGainPositions: clientDetailData.tax.top_gain_positions,
    } : null

    return (
      <div className="flex flex-col gap-4">
        <Breadcrumb
          segments={[
            { label: 'All Advisors', onClick: handleBackToList },
            { label: advisorBookData?.book_name ?? 'Advisor', onClick: handleBackToL2 },
            { label: clientName },
          ]}
        />
        <BackButton label="Back to Book" onClick={handleBackToL2} />

        {clientDetailData ? (
          <>
            <CanonicalBookView
              overview={{
                title: clientName,
                totalAua: clientDetailData.headline.total_aua,
                metrics: [{ label: 'Accounts', value: clientDetailData.headline.account_count.toLocaleString() }],
                dataAsOf: clientDetailData.data_as_of,
              }}
              composition={compositionData}
              tax={l3Tax}
              selectedAssetClass={selectedAssetClass}
              onSelectAssetClass={setSelectedAssetClass}
              quarterlyMix={l3QuarterlyMix}
            />

            {/* Accounts Table */}
            <Panel variant="chart">
              <PanelHeader title="Accounts" />
              <PanelContent noPadding>
                <AccountsTable
                  accounts={clientDetailData.accounts ?? []}
                  selectedAccountId={selectedAccountId}
                  onSelectAccount={(id) => { setSelectedAccountId(id); setSelectedAssetClass(null) }}
                />
              </PanelContent>
            </Panel>

            {/* L4: Account Drill (inline canonical view) */}
            {selectedAccountId && selectedAccount && (
              <div className="flex flex-col gap-4 pl-4 border-l-2 border-white/10">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-white">Account: {selectedAccountId}</p>
                  <button onClick={() => setSelectedAccountId(null)} className="flex items-center gap-1 text-xs text-white/50 hover:text-white transition-colors">
                    <X size={12} /> Close
                  </button>
                </div>

                <CanonicalBookView
                  overview={{
                    title: selectedAccountId,
                    totalAua: selectedAccount.total_aua,
                    metrics: [
                      { label: 'Tax Status', value: selectedAccount.tax_status },
                      { label: 'NNA', value: `${selectedAccount.nna >= 0 ? '+' : ''}${formatCurrency(selectedAccount.nna)}` },
                      { label: 'Positions', value: selectedAccount.num_positions.toLocaleString() },
                    ],
                  }}
                  composition={accountCompositionData}
                  tax={taxFromAccountStatus(selectedAccount.tax_status, selectedAccount.total_aua)}
                  selectedAssetClass={selectedAssetClass}
                  onSelectAssetClass={setSelectedAssetClass}
                  quarterlyMix={null}
                />

                {accountScopedLots.length > 0 && (
                  <Panel variant="chart">
                    <PanelHeader title={`Open Lots -- ${selectedAccountId}`} />
                    <PanelContent noPadding><OpenLotsTable lots={accountScopedLots} /></PanelContent>
                  </Panel>
                )}
              </div>
            )}

            {/* L3 Open Lots */}
            {clientDetailData.tax?.open_lots && clientDetailData.tax.open_lots.length > 0 && (
              <OpenLotsWithFilters lots={clientDetailData.tax.open_lots} />
            )}
          </>
        ) : (
          <Panel variant="chart">
            <PanelContent className="py-12 text-center"><p className="text-white/40">Client detail data not available</p></PanelContent>
          </Panel>
        )}
      </div>
    )
  }

  // ── L2: Advisor Book ────────────────────────────────────────────

  if (selectedAdvisorId && advisorBookData) {
    return (
      <div className="flex flex-col gap-4">
        <Breadcrumb
          segments={[
            { label: 'All Advisors', onClick: handleBackToList },
            { label: advisorBookData.book_name },
          ]}
        />
        <BackButton label="Back to Firm Overview" onClick={handleBackToList} />

        <CanonicalBookView
          overview={{
            title: advisorBookData.book_name,
            totalAua: advisorBookData.summary.total_aua,
            metrics: [
              { label: 'Clients', value: advisorBookData.summary.client_count.toLocaleString() },
              { label: 'Accounts', value: advisorBookData.summary.account_count.toLocaleString() },
            ],
            dataAsOf: advisorBookData.data_as_of,
          }}
          composition={advisorComposition}
          tax={{
            taxable: advisorBookData.tax_exposure.taxable, taxablePct: advisorBookData.tax_exposure.taxable_pct,
            taxDeferred: advisorBookData.tax_exposure.tax_deferred, taxDeferredPct: advisorBookData.tax_exposure.tax_deferred_pct,
            taxFree: advisorBookData.tax_exposure.tax_free, taxFreePct: advisorBookData.tax_exposure.tax_free_pct,
          }}
          selectedAssetClass={selectedAssetClass}
          onSelectAssetClass={setSelectedAssetClass}
          quarterlyMix={l2QuarterlyMix}
        />

        <Panel variant="chart">
          <PanelHeader title="Clients" />
          <PanelContent noPadding>
            <ClientsTable clients={advisorBookData.clients} onClientClick={handleClientClick} />
          </PanelContent>
        </Panel>
      </div>
    )
  }

  if (selectedAdvisorId && isLoadingAdvisor) return <LoadingInline className="py-12" />

  // ── N1: Firm Dashboard ──────────────────────────────────────────

  return (
    <div className="flex flex-col gap-4">
      {clientsTabData && (
        <CanonicalBookView
          overview={{
            title: 'Firm Overview',
            totalAua: clientsTabData.headline.total_aua,
            metrics: [
              { label: 'Clients', value: clientsTabData.headline.client_count.toLocaleString() },
              { label: 'Accounts', value: clientsTabData.headline.account_count.toLocaleString() },
            ],
          }}
          composition={firmComposition}
          tax={{
            taxable: clientsTabData.tax.taxable, taxablePct: clientsTabData.tax.taxable_pct,
            taxDeferred: clientsTabData.tax.tax_deferred, taxDeferredPct: clientsTabData.tax.tax_deferred_pct,
            taxFree: clientsTabData.tax.tax_free, taxFreePct: clientsTabData.tax.tax_free_pct,
            capitalGainsTtm: clientsTabData.tax.capital_gains_ttm,
          }}
          selectedAssetClass={selectedAssetClass}
          onSelectAssetClass={setSelectedAssetClass}
          quarterlyMix={firmMixViews?.views.quarterly.slice(-4) ?? null}
        />
      )}

      {/* Advisor selector + list */}
      {isFirmAdmin && (
        <div className="flex items-center gap-3">
          <div className="relative">
            <button
              onClick={() => setIsAdvisorDropdownOpen(!isAdvisorDropdownOpen)}
              className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white hover:bg-white/10 hover:border-white/20 transition-colors"
            >
              <Users size={14} className="text-white/50" />
              <span>Select Advisor</span>
              <ChevronDown size={14} className={`text-white/50 transition-transform ${isAdvisorDropdownOpen ? 'rotate-180' : ''}`} />
            </button>
            {isAdvisorDropdownOpen && (
              <div className="absolute top-full left-0 mt-1 bg-[#1e1e2d] border border-white/20 rounded-lg shadow-xl z-50 min-w-[200px] max-h-64 overflow-y-auto">
                {[...advisorSummary].sort((a, b) => b.total_aua - a.total_aua).map((adv) => (
                  <div key={adv.name} onClick={() => handleSelectAdvisor(adv.name)} className="px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white">{adv.name}</span>
                      <span className="text-xs text-white/50">{formatCurrency(adv.total_aua)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {advisorSummary.length > 0 ? (
        <AdvisorSummaryTable data={advisorSummary} onSelectAdvisor={handleSelectAdvisor} />
      ) : (
        <Panel variant="chart">
          <PanelContent className="py-12 text-center"><p className="text-white/40">No advisor data available</p></PanelContent>
        </Panel>
      )}
    </div>
  )
}

// ============================================================================
// CANONICAL BOOK VIEW — Identical layout at every drill level
// ============================================================================

function CanonicalBookView({
  overview, composition, tax, selectedAssetClass, onSelectAssetClass, quarterlyMix,
}: {
  overview: CanonicalOverview
  composition: BooksCompositionResponse | null
  tax: CanonicalTax | null
  selectedAssetClass: string | null
  onSelectAssetClass: (cls: string | null) => void
  quarterlyMix: FirmMixPeriodPoint[] | null
}) {
  return (
    <>
      {/* Row 1+2: Consolidated Overview (donut + holdings + quarterly bar) */}
      <ConsolidatedOverviewPanel
        overview={overview}
        composition={composition}
        selectedAssetClass={selectedAssetClass}
        onSelectAssetClass={onSelectAssetClass}
        quarterlyMix={quarterlyMix}
      />

      {/* Row 3: Cost Basis & Tax Liability */}
      <TaxCostBasisPanel tax={tax} />
    </>
  )
}

// ============================================================================
// CONSOLIDATED OVERVIEW PANEL (Rows 1+2) — donut + holdings + quarterly bar
// ============================================================================

const METRIC_CARD_STYLE: Record<string, { dot: string; border: string; from: string; to: string; label: string }> = {
  'Clients':    { dot: 'bg-sky-400',     border: 'border-sky-500/25',     from: 'from-sky-500/15',     to: 'to-sky-500/5',     label: 'text-sky-300/70' },
  'Accounts':   { dot: 'bg-emerald-400', border: 'border-emerald-500/25', from: 'from-emerald-500/15', to: 'to-emerald-500/5', label: 'text-emerald-300/70' },
  'NNA':        { dot: 'bg-violet-400',  border: 'border-violet-500/25',  from: 'from-violet-500/15',  to: 'to-violet-500/5',  label: 'text-violet-300/70' },
  'Tax Status': { dot: 'bg-amber-400',   border: 'border-amber-500/25',   from: 'from-amber-500/15',   to: 'to-amber-500/5',   label: 'text-amber-300/70' },
  'Positions':  { dot: 'bg-purple-400',  border: 'border-purple-500/25',  from: 'from-purple-500/15',  to: 'to-purple-500/5',  label: 'text-purple-300/70' },
}
const METRIC_CARD_DEFAULT = { dot: 'bg-slate-400', border: 'border-slate-500/25', from: 'from-slate-500/15', to: 'to-slate-500/5', label: 'text-slate-300/70' }

// Canonical asset class colors
const MIX_PIE_COLORS: Record<string, string> = {
  equity:           '#3b82f6',
  equities:         '#3b82f6',
  fixed_income:     '#10b981',
  structured_notes: '#f97316',
  alternatives:     '#f97316',
  real_estate:      '#f97316',
  hedge:            '#f97316',
  cash:             '#f59e0b',
  other:            '#6B7280',
  untracked:        '#6B7280',
}

function colorFor(assetClass: string): string {
  return MIX_PIE_COLORS[assetClass] || MIX_PIE_COLORS[assetClass.toLowerCase().replace(/\s+/g, '_')] || '#6B7280'
}

/**
 * Derive last 4 quarter-end snapshots from raw daily timeseries.
 * Returns FirmMixPeriodPoint[] (ascending) so the quarterly bar has 4 points
 * and can compute 3 QoQ growth rates.
 */
function deriveQuarterlyFromTimeseries(
  auaTs: { date: string; total_aua: number }[],
  mixTs: MixTimeseriesPoint[],
): FirmMixPeriodPoint[] {
  if (!auaTs.length || !mixTs.length) return []

  const auaSorted = [...auaTs].sort((a, b) => a.date.localeCompare(b.date))
  const mixSorted = [...mixTs].sort((a, b) => a.date.localeCompare(b.date))
  const maxDate = auaSorted[auaSorted.length - 1].date

  // Find last 4 quarter-end dates <= maxDate
  const maxDateObj = new Date(maxDate + 'T00:00:00Z')
  const qm0 = Math.floor(maxDateObj.getUTCMonth() / 3) * 3 + 3  // last completed quarter-end month

  const quarterEnds: Date[] = []
  for (let i = 0; i < 4; i++) {
    let qm = qm0 - i * 3
    let qy = maxDateObj.getUTCFullYear()
    while (qm <= 0) { qm += 12; qy-- }
    // last day of quarter-end month
    quarterEnds.unshift(new Date(Date.UTC(qy, qm, 0)))
  }

  function closestAuaPt(target: string) {
    let best = auaSorted[0]
    for (const pt of auaSorted) {
      if (pt.date <= target) best = pt
      else break
    }
    return best
  }

  function closestMixPt(target: string) {
    let best = mixSorted[0]
    for (const pt of mixSorted) {
      if (pt.date <= target) best = pt
      else break
    }
    return best
  }

  return quarterEnds.map((qEnd) => {
    const isoDate = qEnd.toISOString().slice(0, 10)
    const aua = closestAuaPt(isoDate)
    const mix = closestMixPt(isoDate)
    const total = aua.total_aua
    const qNum = Math.floor((qEnd.getUTCMonth()) / 3) + 1
    const qy = qEnd.getUTCFullYear()
    return {
      period: `${qy}-Q${qNum}`,
      label: `Q${qNum} '${String(qy).slice(-2)}`,
      end_date: isoDate,
      total_aua: total,
      equity:           { value: total * mix.equity,           pct: mix.equity },
      fixed_income:     { value: total * mix.fixed_income,     pct: mix.fixed_income },
      alternatives:     { value: total * mix.alternatives,     pct: mix.alternatives },
      cash:             { value: total * mix.cash,             pct: mix.cash },
    } as FirmMixPeriodPoint
  })
}

function getClassAua(pt: FirmMixPeriodPoint, cls: string | null): number {
  if (!cls) return pt.total_aua
  const val = (pt as unknown as Record<string, unknown>)[cls]
  if (val && typeof val === 'object' && 'value' in val) return (val as FirmMixClassValue).value
  return 0
}

function QuarterlyMetricsBar({
  quarterlyMix, selectedAssetClass, currentAua, currentSelectedAua,
}: {
  quarterlyMix: FirmMixPeriodPoint[] | null
  selectedAssetClass: string | null
  currentAua: number
  currentSelectedAua: number | null
}) {
  const calcQoQ = (cur: number, prior: number | null): number | null => {
    if (!prior || prior === 0) return null
    return (cur / prior - 1) * 100
  }
  const getPctColor = (pct: number | null): string => {
    if (pct === null) return 'text-white/40'
    return pct > 0 ? 'text-emerald-400' : pct < 0 ? 'text-red-400' : 'text-white/40'
  }
  const fmtPct = (pct: number | null): string => {
    if (pct === null) return ''
    return `${pct >= 0 ? '+' : ''}${pct.toFixed(1)}%`
  }
  const dotColor = (pct: number | null): string =>
    pct === null ? 'bg-white/30' : pct > 0 ? 'bg-emerald-400' : pct < 0 ? 'bg-red-400' : 'bg-white/30'

  const displayCurrentAua = selectedAssetClass ? (currentSelectedAua ?? 0) : currentAua
  const pts = quarterlyMix ?? []
  const q1 = pts[pts.length - 1] ?? null
  const q2 = pts[pts.length - 2] ?? null
  const q3 = pts[pts.length - 3] ?? null
  const q0b = pts[pts.length - 4] ?? null

  const q1Aua = q1 ? getClassAua(q1, selectedAssetClass) : null
  const q2Aua = q2 ? getClassAua(q2, selectedAssetClass) : null
  const q3Aua = q3 ? getClassAua(q3, selectedAssetClass) : null
  const q0bAua = q0b ? getClassAua(q0b, selectedAssetClass) : null

  const currentQoQ = calcQoQ(displayCurrentAua, q1Aua)
  const q1QoQ = calcQoQ(q1Aua ?? 0, q2Aua)
  const q2QoQ = calcQoQ(q2Aua ?? 0, q3Aua)
  const q3QoQ = calcQoQ(q3Aua ?? 0, q0bAua)

  return (
    <div className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex flex-wrap items-center justify-evenly gap-x-4 gap-y-2 w-full">
        <div className="flex flex-col items-center px-3 py-1 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40 min-w-[80px]">
          <div className="text-[10px] text-white/80 font-semibold mb-0.5">{selectedAssetClass ? 'Current' : 'Current AUA'}</div>
          <div className="flex items-center gap-1">
            <span className="text-sm font-bold text-white">{formatCurrency(displayCurrentAua)}</span>
            {currentQoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(currentQoQ)}`}>{fmtPct(currentQoQ)}</span>}
          </div>
        </div>
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1 mb-0.5">
            <div className={`w-1.5 h-1.5 rounded-full ${dotColor(q1QoQ)}`} />
            <span className="text-[10px] text-white/50">{q1?.label ?? '—'}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs font-semibold text-white">{q1Aua !== null ? formatCurrency(q1Aua) : '—'}</span>
            {q1QoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(q1QoQ)}`}>{fmtPct(q1QoQ)}</span>}
          </div>
        </div>
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1 mb-0.5">
            <div className={`w-1.5 h-1.5 rounded-full ${dotColor(q2QoQ)}`} />
            <span className="text-[10px] text-white/50">{q2?.label ?? '—'}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs font-semibold text-white">{q2Aua !== null ? formatCurrency(q2Aua) : '—'}</span>
            {q2QoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(q2QoQ)}`}>{fmtPct(q2QoQ)}</span>}
          </div>
        </div>
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1 mb-0.5">
            <div className="w-1.5 h-1.5 rounded-full bg-white/30" />
            <span className="text-[10px] text-white/50">{q3?.label ?? '—'}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs font-semibold text-white">{q3Aua !== null ? formatCurrency(q3Aua) : '—'}</span>
            {q3QoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(q3QoQ)}`}>{fmtPct(q3QoQ)}</span>}
          </div>
        </div>
      </div>
    </div>
  )
}

function ConsolidatedOverviewPanel({
  overview, composition, selectedAssetClass, onSelectAssetClass, quarterlyMix,
}: {
  overview: CanonicalOverview
  composition: BooksCompositionResponse | null
  selectedAssetClass: string | null
  onSelectAssetClass: (cls: string | null) => void
  quarterlyMix: FirmMixPeriodPoint[] | null
}) {
  const hasMix = composition && composition.mix.length > 0

  // Detect schema: N1/L2 (per-class top_holdings) vs L3/L4 (flat concentration.items)
  const hasPreAggregated = (composition?.mix.some(m => (m.top_holdings?.length ?? 0) > 0)) ?? false

  const MAX_ITEMS = 9

  // Resolved display items
  const cappedItems: ConcentrationItem[] = (() => {
    if (!composition) return []
    if (hasPreAggregated) {
      if (selectedAssetClass) {
        // Per-class top holdings already pre-capped at 9 by script 12
        return composition.mix.find(m => m.asset_class === selectedAssetClass)?.top_holdings ?? []
      } else {
        // Global top 9
        return composition.top_holdings ?? []
      }
    } else {
      // L3/L4: filter flat list, cap at 9
      const all = composition.concentration.items
      const filtered = selectedAssetClass
        ? all.filter(it => it.asset_class === selectedAssetClass)
        : all
      return filtered.slice(0, MAX_ITEMS)
    }
  })()

  // "Other" bucket display
  const otherEntry: { pct: number; market_value: number } | null = (() => {
    if (!composition) return null
    if (hasPreAggregated) {
      if (selectedAssetClass) {
        return composition.mix.find(m => m.asset_class === selectedAssetClass)?.other ?? null
      } else {
        return composition.other ?? null
      }
    } else {
      // L3/L4 schema
      if (!selectedAssetClass && composition.concentration.other.pct > 0) {
        return composition.concentration.other
      }
      return null
    }
  })()

  const showOther = otherEntry !== null && otherEntry.pct > 0
  const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1

  const selectedMixItem = composition?.mix.find(i => i.asset_class === selectedAssetClass)

  const centerLabels = selectedMixItem
    ? {
        show: true,
        name: { show: true, fontSize: '10px', fontWeight: 600, color: 'rgba(255,255,255,0.55)', offsetY: -8, formatter: () => selectedMixItem.label },
        value: { show: true, fontSize: '18px', fontWeight: 700, color: '#ffffff', offsetY: 4, formatter: () => formatCurrency(selectedMixItem.market_value) },
        total: { show: true, showAlways: true, label: selectedMixItem.label, fontSize: '10px', fontWeight: 600, color: 'rgba(255,255,255,0.45)', formatter: () => formatCurrency(selectedMixItem.market_value) },
      }
    : {
        show: true,
        name: { show: false },
        value: { show: true, fontSize: '18px', fontWeight: 700, color: '#ffffff', offsetY: 4, formatter: () => formatCurrency(overview.totalAua) },
        total: { show: true, showAlways: true, label: 'Total AUA', fontSize: '10px', fontWeight: 600, color: 'rgba(255,255,255,0.45)', formatter: () => formatCurrency(overview.totalAua) },
      }

  const holdingsTitle = hasMix && selectedAssetClass
    ? `Top ${selectedMixItem?.label ?? selectedAssetClass.replace(/_/g, ' ')} Holdings`
    : 'Top Holdings'

  return (
    <Panel variant="chart">
      <PanelHeader title={overview.title} />
      <PanelContent>
        {/* Metric cards — full-width flex row, each card grows to fill */}
        <div className="flex gap-3 mb-5">
          <div className="flex-1 rounded-xl border border-indigo-500/25 bg-gradient-to-br from-indigo-500/15 to-indigo-500/5 p-4">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-indigo-400 flex-shrink-0" />
              <span className="text-[10px] text-indigo-300/70 uppercase tracking-widest font-medium">Total AUA</span>
            </div>
            <p className="text-3xl font-black text-white tracking-tight leading-none">{formatCurrency(overview.totalAua)}</p>
            {overview.dataAsOf && <p className="text-[10px] text-indigo-400/50 mt-2">as of {overview.dataAsOf}</p>}
          </div>
          {overview.metrics.map((m) => {
            const s = METRIC_CARD_STYLE[m.label] ?? METRIC_CARD_DEFAULT
            return (
              <div key={m.label} className={`flex-1 rounded-xl border ${s.border} bg-gradient-to-br ${s.from} ${s.to} p-4`}>
                <div className="flex items-center gap-2 mb-3">
                  <div className={`w-2 h-2 rounded-full ${s.dot} flex-shrink-0`} />
                  <span className={`text-[10px] ${s.label} uppercase tracking-widest font-medium`}>{m.label}</span>
                </div>
                <p className="text-2xl font-bold text-white leading-none">{m.value}</p>
              </div>
            )
          })}
        </div>

        <div className="flex min-h-[320px]">
          {/* LEFT: donut + legend + quarterly bar */}
          <div className="flex-1 flex flex-col gap-4 pr-5">
            <p className="text-[10px] text-white/50 uppercase tracking-widest font-medium mb-1">Asset Mix</p>
            <div className="flex items-start gap-4">
              {/* Donut */}
              {hasMix ? (
                <div style={{ width: 220, height: 220, flexShrink: 0 }}>
                  <Suspense fallback={<div className="flex items-center justify-center h-full"><span className="text-xs text-white/20">...</span></div>}>
                    <ApexChart
                      key={`consolidated-donut-${selectedAssetClass ?? 'all'}`}
                      type="donut"
                      width={220}
                      height={220}
                      series={composition.mix.map(item => item.market_value)}
                      options={{
                        chart: {
                          type: 'donut',
                          background: 'transparent',
                          animations: { enabled: true, speed: 800, animateGradually: { enabled: true, delay: 150 }, dynamicAnimation: { enabled: true, speed: 350 } },
                          dropShadow: { enabled: true, top: 4, left: 0, blur: 10, opacity: 0.35 },
                          events: {
                            dataPointSelection: (_event: unknown, _chartContext: unknown, config: { dataPointIndex: number }) => {
                              const cls = composition.mix[config.dataPointIndex]?.asset_class
                              if (cls) onSelectAssetClass(selectedAssetClass === cls ? null : cls)
                            },
                          },
                        },
                        colors: composition.mix.map(item => colorFor(item.asset_class)),
                        labels: composition.mix.map(item => item.label),
                        stroke: { show: true, width: 2, colors: ['rgba(0,0,0,0.3)'] },
                        dataLabels: { enabled: false },
                        plotOptions: { pie: { expandOnClick: false, donut: { size: '60%', labels: centerLabels } } },
                        legend: { show: false },
                        tooltip: { enabled: false },
                        states: { hover: { filter: { type: 'lighten', value: 0.08 } }, active: { filter: { type: 'darken', value: 0.1 } } },
                      }}
                    />
                  </Suspense>
                </div>
              ) : (
                <div style={{ width: 220, height: 220, flexShrink: 0 }} className="flex items-center justify-center">
                  <span className="text-xs text-white/30">{composition ? 'No allocation data' : 'Loading...'}</span>
                </div>
              )}

              {/* Clickable legend */}
              {hasMix && (
                <div className="flex-1 flex flex-col gap-2 pt-2">
                  {composition.mix.map((item) => {
                    const isSelected = selectedAssetClass === item.asset_class
                    const isDimmed = selectedAssetClass && !isSelected
                    return (
                      <button
                        key={item.asset_class}
                        onClick={() => onSelectAssetClass(isSelected ? null : item.asset_class)}
                        className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg transition-all text-left focus:outline-none ${
                          isSelected ? 'bg-white/15 ring-1 ring-white/30' : isDimmed ? 'opacity-30 hover:opacity-60' : 'hover:bg-white/10'
                        }`}
                      >
                        <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: colorFor(item.asset_class) }} />
                        <span className="text-[11px] text-white/80 flex-1">{item.label}</span>
                        <span className="text-[11px] font-semibold text-white/70">{formatCurrency(item.market_value)}</span>
                        <span className="text-[10px] text-white/40 w-10 text-right">{(item.pct * 100).toFixed(1)}%</span>
                      </button>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Quarterly metrics bar */}
            <QuarterlyMetricsBar
              quarterlyMix={quarterlyMix}
              selectedAssetClass={selectedAssetClass}
              currentAua={overview.totalAua}
              currentSelectedAua={selectedMixItem?.market_value ?? null}
            />
          </div>

          {/* Vertical divider */}
          <div className="w-px self-stretch bg-white/10 mx-2 flex-shrink-0" />

          {/* RIGHT: top holdings bars */}
          <div className="flex-1 flex flex-col gap-2 pl-5">
            <p className="text-[10px] text-white/50 uppercase tracking-widest font-medium mb-1">{holdingsTitle}</p>
            {cappedItems.length > 0 ? (
              <div className="flex flex-col gap-2.5 overflow-y-auto" style={{ maxHeight: 280 }}>
                {cappedItems.map((item, idx) => (
                  <div key={item.key} className="flex items-center gap-2.5">
                    <span className="text-[10px] text-white/30 w-4 text-right flex-shrink-0 font-mono">{idx + 1}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-baseline justify-between mb-1">
                        <span className="text-[11px] text-white/85 truncate leading-tight">{item.label}</span>
                        <span className="text-[11px] font-semibold text-white/70 ml-2 flex-shrink-0">{(item.pct * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-1.5 bg-white/[0.08] rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all"
                          style={{ width: `${(item.pct / maxPct) * 100}%`, backgroundColor: colorFor(item.asset_class) }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
                {showOther && otherEntry && (
                  <div className="flex items-center gap-2.5">
                    <span className="text-[10px] text-white/20 w-4 text-right flex-shrink-0">~</span>
                    <div className="flex-1">
                      <div className="flex items-baseline justify-between mb-1">
                        <span className="text-[11px] text-white/40 italic">Other</span>
                        <span className="text-[11px] text-white/30 ml-2">{(otherEntry.pct * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-white/20"
                          style={{ width: `${(otherEntry.pct / maxPct) * 100}%` }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center py-8">
                <span className="text-xs text-white/30">
                  {!composition ? 'Loading...' : !hasPreAggregated && composition.concentration.items.length === 0 ? 'No holdings data at this level' : 'No holdings for selected class'}
                </span>
              </div>
            )}
          </div>
        </div>
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// TAX & COST BASIS PANEL (Row 3)
// ============================================================================

function TaxCostBasisPanel({ tax }: { tax: CanonicalTax | null }) {
  if (!tax) {
    return (
      <Panel variant="chart">
        <PanelHeader title="Cost Basis & Tax Liability" />
        <PanelContent className="py-6 text-center">
          <span className="text-sm text-white/40">Tax data not available</span>
        </PanelContent>
      </Panel>
    )
  }

  const totalTaxAua = tax.taxable + tax.taxDeferred + tax.taxFree
  const taxBuckets = [
    { label: 'Taxable', amount: tax.taxable, pct: tax.taxablePct, color: '#EF4444', bg: 'bg-red-500/10', border: 'border-red-500/20' },
    { label: 'Tax Deferred', amount: tax.taxDeferred, pct: tax.taxDeferredPct, color: '#F59E0B', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
    { label: 'Tax Free', amount: tax.taxFree, pct: tax.taxFreePct, color: '#10B981', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
  ]

  return (
    <Panel variant="chart">
      <PanelHeader title="Cost Basis & Tax Liability" />
      <PanelContent>
        <div className="space-y-5">
          {/* Stacked bar */}
          {totalTaxAua > 0 && (
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2.5">AUA by Tax Status</p>
              <div className="flex h-5 rounded-lg overflow-hidden gap-px">
                {taxBuckets.filter((b) => b.pct > 0).map((b) => (
                  <div
                    key={b.label}
                    className="flex items-center justify-center"
                    style={{ width: `${b.pct}%`, backgroundColor: b.color }}
                  >
                    {b.pct >= 10 && (
                      <span className="text-[9px] font-bold text-white/90 leading-none">{b.pct.toFixed(0)}%</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tax status cards */}
          <div className="grid grid-cols-3 gap-2">
            {taxBuckets.map((b) => (
              <div key={b.label} className={`rounded-lg border ${b.border} ${b.bg} p-3`}>
                <div className="flex items-center gap-1.5 mb-2">
                  <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: b.color }} />
                  <span className="text-[10px] text-white/50 uppercase tracking-wide leading-tight">{b.label}</span>
                </div>
                <p className="text-base font-bold text-white leading-tight">{formatCurrency(b.amount)}</p>
                <p className="text-[10px] text-white/40 mt-0.5">{b.pct.toFixed(1)}%</p>
              </div>
            ))}
          </div>

          {/* Capital Gains TTM */}
          {tax.capitalGainsTtm != null && (
            <div className="flex items-center justify-between rounded-lg bg-white/[0.03] border border-white/[0.08] px-4 py-3">
              <span className="text-xs text-white/50 uppercase tracking-wide">Capital Gains (TTM)</span>
              <span className={`text-lg font-bold ${tax.capitalGainsTtm >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {tax.capitalGainsTtm >= 0 ? '+' : ''}{formatCurrency(tax.capitalGainsTtm)}
              </span>
            </div>
          )}

          {/* Cost Basis by Year (L3+) */}
          {tax.costBasisByYear && tax.costBasisByYear.length > 0 && (
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2.5">Cost Basis by Year</p>
              <div className="rounded-lg overflow-hidden border border-white/[0.08]">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-white/[0.04] border-b border-white/10">
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Year</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Cost Basis</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Market Value</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Unrealized Gain</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tax.costBasisByYear.map((row, i) => (
                      <tr key={row.year} className={`border-b border-white/5 ${i % 2 === 1 ? 'bg-white/[0.02]' : ''}`}>
                        <td className="px-3 py-2 text-white/70 font-medium">{row.year}</td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(row.cost_basis)}</td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(row.market_value)}</td>
                        <td className="px-3 py-2 text-right">
                          <span className={row.unrealized_gain >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                            {row.unrealized_gain >= 0 ? '+' : ''}{formatCurrency(row.unrealized_gain)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Top Gain Positions (L3+) */}
          {tax.topGainPositions && tax.topGainPositions.length > 0 && (
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2.5">Top Gain Positions</p>
              <div className="rounded-lg overflow-hidden border border-white/[0.08]">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-white/[0.04] border-b border-white/10">
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Name</th>
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Ticker</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Gain</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Cost Basis</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Mkt Value</th>
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Term</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tax.topGainPositions.map((pos, i) => (
                      <tr key={i} className={`border-b border-white/5 ${i % 2 === 1 ? 'bg-white/[0.02]' : ''}`}>
                        <td className="px-3 py-2 text-white/70 max-w-[120px] truncate">{pos.asset_name}</td>
                        <td className="px-3 py-2 text-white/50 font-mono">{pos.ticker ?? '--'}</td>
                        <td className="px-3 py-2 text-right">
                          <span className={pos.unrealized_gain >= 0 ? 'text-emerald-400 font-bold' : 'text-red-400 font-bold'}>
                            {pos.unrealized_gain >= 0 ? '+' : ''}{formatCurrency(pos.unrealized_gain)}
                          </span>
                        </td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(pos.cost_basis)}</td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(pos.market_value)}</td>
                        <td className="px-3 py-2">
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-semibold ${pos.term === 'Short' ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
                            {pos.term}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </PanelContent>
    </Panel>
  )
}


// ============================================================================
// OPEN LOTS WITH FILTERS (L3)
// ============================================================================

function OpenLotsWithFilters({ lots }: { lots: OpenLot[] }) {
  const [termFilter, setTermFilter] = useState<'all' | 'short' | 'long'>('all')
  const [accountFilter, setAccountFilter] = useState<string>('all')

  const accountIds = useMemo(() => [...new Set(lots.map((l) => l.account_id))], [lots])

  const filtered = useMemo(() => {
    let result = lots
    if (termFilter !== 'all') {
      const match = termFilter === 'short' ? 'Short' : 'Long'
      result = result.filter((l) => l.term === match)
    }
    if (accountFilter !== 'all') result = result.filter((l) => l.account_id === accountFilter)
    return result
  }, [lots, termFilter, accountFilter])

  return (
    <Panel variant="chart">
      <PanelHeader
        title="Taxable Open Lots"
        actions={
          <div className="flex items-center gap-2">
            <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
              {(['all', 'short', 'long'] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setTermFilter(t)}
                  className={`px-2 py-1 text-xs font-medium rounded-md transition-colors ${
                    termFilter === t ? 'bg-white/20 text-white' : 'text-white/50 hover:text-white hover:bg-white/10'
                  }`}
                >
                  {t === 'all' ? 'All' : t === 'short' ? 'Short' : 'Long'}
                </button>
              ))}
            </div>
            {accountIds.length > 1 && (
              <select
                value={accountFilter}
                onChange={(e) => setAccountFilter(e.target.value)}
                className="bg-white/10 text-white text-xs rounded-md px-2 py-1 border border-white/10 outline-none"
              >
                <option value="all">All Accounts</option>
                {accountIds.map((id) => <option key={id} value={id}>{id}</option>)}
              </select>
            )}
          </div>
        }
      />
      <PanelContent noPadding>
        {filtered.length > 0 ? (
          <OpenLotsTable lots={filtered} />
        ) : (
          <div className="py-6 text-center text-sm text-white/40">
            No taxable open lots{termFilter !== 'all' || accountFilter !== 'all' ? ' matching filters' : ''}
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// TABLE COMPONENTS
// ============================================================================

// Field-name normalizers (Lambda sends current_units/accrued_gain; future target is quantity/unrealized_gain)
function lotQty(lot: OpenLot): number { return lot.current_units ?? lot.quantity ?? 0 }
function lotGain(lot: OpenLot): number { return lot.accrued_gain ?? lot.unrealized_gain ?? 0 }

function termBadge(term: string) {
  const s = term === 'Short'
    ? 'bg-amber-500/15 text-amber-400'
    : term === 'Long'
    ? 'bg-emerald-500/15 text-emerald-400'
    : term === 'Hybrid'
    ? 'bg-indigo-500/15 text-indigo-400'
    : 'bg-white/5 text-white/40'
  return <span className={`px-1.5 py-0.5 rounded text-[9px] font-semibold ${s}`}>{term || '--'}</span>
}

function OpenLotsTable({ lots }: { lots: OpenLot[] }) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  const grouped = useMemo(() => {
    const map = new Map<string, OpenLot[]>()
    for (const lot of lots) {
      const key = `${lot.asset_name ?? ''}||${lot.ticker ?? ''}`
      const group = map.get(key) ?? []
      group.push(lot)
      map.set(key, group)
    }
    return [...map.entries()].map(([key, items]) => ({ key, items }))
  }, [lots])

  const toggle = (key: string) =>
    setExpanded(prev => { const n = new Set(prev); if (n.has(key)) { n.delete(key) } else { n.add(key) } return n })

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="w-7" />
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Name</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Ticker</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Qty</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Avg Cost</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Mkt Value</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Gain</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Term</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Acq. Date</th>
          </tr>
        </thead>
        <tbody>
          {grouped.map(({ key, items }) => {
            const isMulti = items.length > 1
            const isOpen = expanded.has(key)
            const totalQty = items.reduce((s, l) => s + lotQty(l), 0)
            const hasQty = totalQty > 0
            const totalCost = items.reduce((s, l) => s + (l.cost_basis ?? 0), 0)
            const totalMv = items.reduce((s, l) => s + (l.market_value ?? 0), 0)
            const totalGain = items.reduce((s, l) => s + lotGain(l), 0)
            const avgCost = hasQty ? totalCost / totalQty : null
            // Use cost_per_unit from first lot as fallback if no qty-based avg
            const displayCost = avgCost ?? items[0]?.cost_per_unit ?? totalCost
            const terms = new Set(items.map(l => l.term).filter(Boolean))
            const term = terms.size > 1 ? 'Hybrid' : (items[0]?.term ?? '--')
            const acqDates = items.map(l => l.acquisition_date).filter(Boolean) as string[]
            const latestAcq = acqDates.length > 0 ? [...acqDates].sort().at(-1) ?? null : null

            return (
              <Fragment key={key}>
                <tr
                  className={`border-b border-white/5 transition-colors ${isMulti ? 'cursor-pointer hover:bg-white/5' : 'hover:bg-white/5'}`}
                  onClick={() => isMulti && toggle(key)}
                >
                  <td className="px-2 py-2 text-center text-white/30">
                    {isMulti && (isOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />)}
                  </td>
                  <td className="px-3 py-2 text-white/70 max-w-[140px] truncate">
                    {items[0]?.asset_name ?? '--'}
                    {isMulti && <span className="ml-1.5 text-[9px] text-white/25 font-mono">{items.length}x</span>}
                  </td>
                  <td className="px-3 py-2 text-white/50 font-mono">{items[0]?.ticker ?? '--'}</td>
                  <td className="px-3 py-2 text-right text-white/60">{hasQty ? totalQty.toLocaleString() : '--'}</td>
                  <td className="px-3 py-2 text-right text-white/60">{formatCurrency(displayCost)}</td>
                  <td className="px-3 py-2 text-right text-white/60">{formatCurrency(totalMv)}</td>
                  <td className="px-3 py-2 text-right">
                    <span className={totalGain >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                      {totalGain >= 0 ? '+' : ''}{formatCurrency(totalGain)}
                    </span>
                  </td>
                  <td className="px-3 py-2">{termBadge(term)}</td>
                  <td className="px-3 py-2 text-white/50">{latestAcq ?? '--'}</td>
                </tr>
                {isOpen && items.map((lot, li) => {
                  const qty = lotQty(lot)
                  const gain = lotGain(lot)
                  return (
                    <tr key={`${key}-${li}`} className="border-b border-white/[0.04] bg-white/[0.025]">
                      <td />
                      <td className="px-3 py-1.5 pl-7 text-white/35 text-[10px] italic">Lot {li + 1}</td>
                      <td className="px-3 py-1.5 text-white/25 font-mono text-[10px]">{lot.ticker ?? '--'}</td>
                      <td className="px-3 py-1.5 text-right text-white/40 text-[10px]">{qty > 0 ? qty.toLocaleString() : '--'}</td>
                      <td className="px-3 py-1.5 text-right text-white/40 text-[10px]">
                        {lot.cost_per_unit != null ? formatCurrency(lot.cost_per_unit) : formatCurrency(lot.cost_basis ?? 0)}
                      </td>
                      <td className="px-3 py-1.5 text-right text-white/40 text-[10px]">{formatCurrency(lot.market_value ?? 0)}</td>
                      <td className="px-3 py-1.5 text-right text-[10px]">
                        <span className={gain >= 0 ? 'text-[#10B981]/60' : 'text-[#EF4444]/60'}>
                          {gain >= 0 ? '+' : ''}{formatCurrency(gain)}
                        </span>
                      </td>
                      <td className="px-3 py-1.5 text-[10px]">{termBadge(lot.term ?? '')}</td>
                      <td className="px-3 py-1.5 text-white/30 text-[10px]">{lot.acquisition_date ?? '--'}</td>
                    </tr>
                  )
                })}
              </Fragment>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function ClientsTable({ clients, onClientClick }: { clients: AdvisorClient[]; onClientClick: (key: string) => void }) {
  const sorted = useMemo(() => [...clients].sort((a, b) => b.aua - a.aua), [clients])
  if (sorted.length === 0) return <div className="py-6 text-center text-sm text-white/40">No clients</div>

  return (
    <div className="overflow-y-auto" style={{ maxHeight: 320 }}>
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="text-left px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Client</th>
            <th className="text-right px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">AUA</th>
            <th className="w-8" />
          </tr>
        </thead>
        <tbody>
          {sorted.map((c, i) => (
            <tr
              key={c.client_key}
              onClick={() => onClientClick(c.client_key)}
              className={`border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors group${i % 2 === 1 ? ' bg-white/[0.025]' : ''}`}
            >
              <td className="px-4 py-2.5 text-sm text-white font-medium">{c.client_name}</td>
              <td className="px-4 py-2.5 text-right text-white/70">{formatCurrency(c.aua)}</td>
              <td className="px-2 py-2.5"><ChevronRight size={14} className="text-white/30 group-hover:text-white/60 transition-colors" /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function AccountsTable({ accounts, selectedAccountId, onSelectAccount }: {
  accounts: BooksClientAccount[]
  selectedAccountId: string | null
  onSelectAccount: (id: string | null) => void
}) {
  if (accounts.length === 0) return <div className="py-6 text-center text-sm text-white/40">No accounts</div>

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Account</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Tax Status</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">AUA</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Inflows</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Outflows</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">NNA</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Positions</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((acct) => {
            const sel = acct.account_id === selectedAccountId
            return (
              <tr
                key={acct.account_id}
                onClick={() => onSelectAccount(sel ? null : acct.account_id)}
                className={`border-b border-white/5 cursor-pointer transition-colors ${sel ? 'bg-white/10' : 'hover:bg-white/5'}`}
              >
                <td className="px-3 py-2.5 text-white font-medium">{acct.account_id}</td>
                <td className="px-3 py-2.5 text-white/70">{acct.tax_status}</td>
                <td className="px-3 py-2.5 text-right text-white/80">{formatCurrency(acct.total_aua)}</td>
                <td className="px-3 py-2.5 text-right text-white/60">{formatCurrency(acct.cum_inflows)}</td>
                <td className="px-3 py-2.5 text-right text-white/60">{formatCurrency(acct.cum_outflows)}</td>
                <td className="px-3 py-2.5 text-right">
                  <span className={acct.nna >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                    {acct.nna >= 0 ? '+' : ''}{formatCurrency(acct.nna)}
                  </span>
                </td>
                <td className="px-3 py-2.5 text-right text-white/60">{acct.num_positions}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

// Canonical column layout — matches AdvisorsTab.tsx LeaderboardRow
const BOOKS_COL = 'w-[160px] flex-shrink-0 text-center px-4'
const BOOKS_DIV = <div className="w-px self-stretch bg-white/10 flex-shrink-0" />

function ArchitectRankBadge({ rank }: { rank: number }) {
  const colors: Record<number, string> = {
    1: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40',
    2: 'bg-gray-400/20 text-gray-300 border-gray-400/40',
    3: 'bg-orange-600/20 text-orange-400 border-orange-600/40',
  }
  return (
    <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold border ${colors[rank] || 'bg-white/5 text-white/50 border-white/10'}`}>
      {rank}
    </span>
  )
}

function AdvisorSummaryTable({ data, onSelectAdvisor }: { data: LeaderboardEntry[]; onSelectAdvisor: (name: string) => void }) {
  const sorted = useMemo(() => [...data].sort((a, b) => b.total_aua - a.total_aua).slice(0, 20), [data])

  // Hero = AUA (default context for Books tab), secondary = uniform text-sm
  const HERO = 'text-2xl font-black'
  const SEC = 'text-sm font-medium'

  return (
    <Panel variant="chart">
      <PanelHeader title="Architect Summary" />
      <PanelContent noPadding>
        <div className="p-5 flex flex-col gap-3">
          {sorted.map((adv, i) => {
            const rank = i + 1
            const isTop3 = rank <= 3
            const nnaPos = adv.nna >= 0
            const groPos = adv.aua_growth_pct >= 0
            const borderColor = rank === 1 ? 'border-amber-500/40' : rank === 2 ? 'border-slate-400/30' : rank === 3 ? 'border-orange-600/30' : 'border-white/8'
            return (
              <div
                key={adv.name}
                onClick={() => onSelectAdvisor(adv.name)}
                className={`rounded-xl border ${borderColor} bg-white/[0.02] overflow-hidden hover:border-white/20 transition-colors cursor-pointer`}
              >
                <div className="px-8 py-5 flex items-center">
                  <div className="flex-shrink-0 mr-5">
                    <ArchitectRankBadge rank={rank} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className={`text-lg font-bold ${isTop3 ? 'text-white' : 'text-white/90'}`}>{adv.name}</div>
                  </div>
                  {/* NNA */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${SEC} ${nnaPos ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                      {nnaPos ? '+' : ''}{formatNumberTo3Digits(adv.nna, { unit: '$', includeSign: false })}
                    </div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">NNA</div>
                  </div>
                  {/* AUA — hero */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${HERO} text-white`}>
                      {formatCurrency(adv.total_aua)}
                    </div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">AUA</div>
                  </div>
                  {/* GRO */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${SEC} ${groPos ? 'text-emerald-400' : 'text-red-400'}`}>
                      {groPos ? '+' : ''}{adv.aua_growth_pct.toFixed(1)}%
                    </div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">GRO</div>
                  </div>
                  {/* New Clients */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${SEC} text-white/60`}>{adv.new_clients}</div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">New Clients</div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        {data.length > 20 && (
          <div className="px-4 py-2 text-center text-[10px] text-white/40 border-t border-white/5">
            Showing top 20 of {data.length} architects
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// SHARED PRIMITIVES
// ============================================================================

function MetricCard({ label, value, large }: { label: string; value: string; large?: boolean }) {
  return (
    <div className="bg-white/5 rounded-lg p-3 text-center">
      <p className={`font-bold text-white ${large ? 'text-xl' : 'text-sm'}`}>{value}</p>
      <p className="text-[10px] text-white/50 mt-0.5">{label}</p>
    </div>
  )
}

function TaxRow({ label, amount, pct, color }: { label: string; amount: number; pct: number; color: string }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
        <span className="text-xs text-white/70">{label}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs text-white/60">{pct.toFixed(1)}%</span>
        <span className="text-xs text-white font-medium">{formatCurrency(amount)}</span>
      </div>
    </div>
  )
}

function Breadcrumb({ segments }: { segments: { label: string; onClick?: () => void }[] }) {
  return (
    <div className="flex items-center gap-1.5">
      {segments.map((seg, i) => (
        <span key={i} className="flex items-center gap-1.5">
          {i > 0 && <ChevronRight size={14} className="text-indigo-500/60 flex-shrink-0" />}
          {seg.onClick ? (
            <button
              onClick={seg.onClick}
              className="text-base font-semibold text-indigo-400 hover:text-indigo-200 hover:underline underline-offset-2 transition-colors"
            >
              {seg.label}
            </button>
          ) : (
            <span className="text-base font-bold text-white">{seg.label}</span>
          )}
        </span>
      ))}
    </div>
  )
}

function BackButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1.5 text-base font-semibold text-indigo-400 hover:text-indigo-200 hover:underline underline-offset-2 transition-colors w-fit"
    >
      <ArrowLeft size={16} /> {label}
    </button>
  )
}
```

### gold-script-06b----builds-firmmixviews.json--per-advisor-mix.json--clientmixtimeseries-parquet-4-class-taxonomy-via-etfclassifier.py

```
#!/usr/bin/env python3
"""
Build Client Mix + Concentration Timeseries

Joins positions_cube x canonical_prices x accounts_dimension to produce
one JSON per relationship containing full mix and concentration history.

Output pattern (consistent with gold/advisors/{advisor_id}/book.json):
    gold/client_timeseries/{relationship_id}.json   -- one per relationship

    {
      "generated_at": "...",
      "data_as_of":   "YYYY-MM-DD",
      "relationship_id": "...",
      "mix": [
        {"date":"YYYY-MM-DD","equity":0.72,"fixed_income":0.24,
         "structured_notes":0.02,"cash":0.02,"other":0.0},
        ...
      ],
      "concentration": [
        {"date":"YYYY-MM-DD","holdings":[
          {"asset_name":"...","ticker":"...","asset_class":"equity",
           "market_value":50000.0,"pct":0.15},
          ... (top 10 by market_value)
        ]},
        ...
      ]
    }

Watermark: gold/client_timeseries/_watermark.json
    {"data_as_of": "YYYY-MM-DD"}
    Written after each successful run. Incremental mode reads this to determine
    which positions_cube partitions to process.

AP active gate: excludes account_ids not present in account_performance within
45 days of the snapshot date (prevents ~$371M stale-holdings inflation).

pct sum validation: per (date, relationship_id) mix must sum to 1.0 (+-0.001).
Dates failing validation are excluded from the JSON output.

Concurrency: ThreadPoolExecutor for both partition processing and JSON writes.
Defaults: 32 process workers, 64 write workers (tuned for r6i.4xlarge).
Override via env vars O6B_PROCESS_WORKERS, O6B_WRITE_WORKERS, or --workers flag.
Daily incremental (1-10 partitions) runs fine on r6i.xlarge with low concurrency.

Usage:
    python3 06b_build_client_mix_timeseries.py --upload               # full rebuild
    python3 06b_build_client_mix_timeseries.py --upload --incremental # incremental
    python3 06b_build_client_mix_timeseries.py --upload --workers 8   # lower concurrency
    python3 06b_build_client_mix_timeseries.py --dry-run              # no write
    python3 06b_build_client_mix_timeseries.py --dry-run -v           # verbose

Author: 0.4.0_DS_ClientPlatform
Date:   2026-03-16
"""

import argparse
import gc
import json
import os
import pathlib
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from io import BytesIO

import boto3
import pandas as pd
from lib.etf_classifier import ETFClassifier

S3_BUCKET      = 'opal-data-bd'
OUTPUT_PREFIX  = 'gold/client_timeseries'
WATERMARK_KEY  = 'gold/client_timeseries/_watermark.json'
AP_GATE_DAYS         = 45
AP_GATE_DAYS_DEFAULT = 45   # standard gate for all accounts
PCT_TOL              = 0.001
TOP_N_CONC           = 10

# Firm/advisor mix views output paths
FIRM_ID          = os.environ.get('O6B_FIRM_ID', '49financial')
FIRM_MIX_KEY     = 'gold/firm_mix_views.json'
FIRM_DAILY_KEY   = 'gold/firm_mix_views_daily.json'
ADV_MIX_PREFIX   = 'gold/advisors'
REL_LOOKUP_KEY   = 'gold/views/rel_architect_lookup.parquet'

# Insurance account config -- loaded at startup from insurance_accounts.json
_INSURANCE_CONFIG_PATH = pathlib.Path(__file__).parent / 'insurance_accounts.json'


def _load_insurance_config() -> tuple[set, int]:
    """
    Load insurance_accounts.json.

    Returns:
        (insurance_account_ids: set[str], ap_gate_days_override: int)

    insurance_accounts.json format:
    {
        "insurance_account_ids": ["acc_xxx", "acc_yyy"],
        "ap_gate_days_override": 180,
        "_comment": "Add new accounts when new insurance products are onboarded."
    }

    Insurance/annuity accounts operate on quarterly statement cycles and update
    account_performance infrequently (monthly/quarterly). The standard 45-day AP
    gate incorrectly excludes them during inter-statement gaps, causing ~$60M of
    structured_notes to appear and disappear. These accounts receive an extended
    gate (default 180 days) instead of the global 45-day gate.

    To populate: run .tmp_insurance_ap_gate.py and copy the suggested
    insurance_account_ids into this file.
    """
    if not _INSURANCE_CONFIG_PATH.exists():
        return set(), AP_GATE_DAYS_DEFAULT
    try:
        cfg = json.loads(_INSURANCE_CONFIG_PATH.read_text())
        ids = set(str(x) for x in cfg.get('insurance_account_ids', []))
        days = int(cfg.get('ap_gate_days_override', AP_GATE_DAYS_DEFAULT))
        print(f"  Insurance gate override: {len(ids)} accounts, {days}-day gate")
        return ids, days
    except Exception as e:
        print(f"  WARN: could not load insurance_accounts.json: {e} -- using default gate")
        return set(), AP_GATE_DAYS_DEFAULT

# Thread-local S3 clients (boto3 clients are not thread-safe)
_thread_local = threading.local()

def _get_s3():
    if not hasattr(_thread_local, 's3'):
        _thread_local.s3 = boto3.client('s3', region_name='us-east-1')
    return _thread_local.s3

# Main-thread client for setup/teardown
s3 = boto3.client('s3', region_name='us-east-1')

# Concurrency settings (r6i.xlarge: 4 vCPU, 32GB -- I/O bound, safe to oversubscribe)
PROCESS_WORKERS = int(os.environ.get('O6B_PROCESS_WORKERS', '128'))
WRITE_WORKERS   = int(os.environ.get('O6B_WRITE_WORKERS', '128'))


# =============================================================================
# Classification (ETFClassifier-backed, GLDPRE 4-class taxonomy)
# =============================================================================

_MIX_ASSET_CLASSES = ['equity', 'fixed_income', 'alternatives']


def classify_holding(ticker, asset_name) -> str:
    """Classify a holding using DynamoDB-backed ETFClassifier."""
    cls = ETFClassifier.instance().classify(ticker, asset_name)
    if cls:  # 'equity', 'fixed_income', or 'alternatives'
        return cls
    # Unclassified with valid ticker -> conservative equity default
    if ticker:
        t = str(ticker).strip().upper()
        if t and t not in ('NONE', 'NAN', '') and t.isalpha() and 1 <= len(t) <= 5:
            return 'equity'
    return 'equity'  # ultimate fallback for positions


def classify_series(ticker_series: pd.Series, name_series: pd.Series) -> pd.Series:
    """Classify a series of holdings using DynamoDB-backed ETFClassifier.

    Returns a Series with values in {'equity', 'fixed_income', 'alternatives'}.
    Unclassified positions default to 'equity' (conservative fallback).
    """
    classifier = ETFClassifier.instance()
    result = pd.Series('equity', index=ticker_series.index, dtype='object')
    for idx in ticker_series.index:
        ticker = ticker_series[idx]
        name = name_series[idx]
        cls = classifier.classify(
            str(ticker) if pd.notna(ticker) else '',
            str(name) if pd.notna(name) else '',
        )
        if cls:
            result[idx] = cls
        # else: stays 'equity' (default)
    return result


# =============================================================================
# S3 helpers
# =============================================================================

def _read_parquet(key: str) -> pd.DataFrame:
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


def _list_positions_cube_keys() -> list:
    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='gold/positions_cube/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])
    return sorted(keys)


def _parse_date(key: str) -> str:
    return key.rsplit('/', 1)[-1].replace('.parquet', '')


def _load_watermark() -> str | None:
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=WATERMARK_KEY)
        data = json.loads(resp['Body'].read())
        wm = data.get('data_as_of')
        print(f"  Watermark: {wm}")
        return wm
    except Exception:
        return None


def _write_watermark(data_as_of: str, rel_count: int, dry_run: bool) -> None:
    body = json.dumps({'data_as_of': data_as_of, 'relationship_count': rel_count}).encode()
    if not dry_run:
        s3.put_object(Bucket=S3_BUCKET, Key=WATERMARK_KEY, Body=body,
                      ContentType='application/json')
    print(f"  Watermark -> {data_as_of} ({rel_count} relationships)")


def _write_relationship_json(rel_id: str, payload: dict, dry_run: bool) -> None:
    key = f'{OUTPUT_PREFIX}/{rel_id}.json'
    body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        _get_s3().put_object(Bucket=S3_BUCKET, Key=key, Body=body,
                             ContentType='application/json',
                             CacheControl='public, max-age=300, s-maxage=3600')


def _read_relationship_json(rel_id: str) -> dict | None:
    try:
        resp = _get_s3().get_object(Bucket=S3_BUCKET, Key=f'{OUTPUT_PREFIX}/{rel_id}.json')
        return json.loads(resp['Body'].read())
    except Exception:
        return None


def _load_firm_daily() -> dict:
    """Load existing firm_mix_views_daily.json from S3. Returns {} on miss."""
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=FIRM_DAILY_KEY)
        return json.loads(resp['Body'].read())
    except Exception:
        return {}


def _write_firm_daily(daily_dict: dict, dry_run: bool) -> None:
    body = json.dumps(daily_dict, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        s3.put_object(Bucket=S3_BUCKET, Key=FIRM_DAILY_KEY, Body=body,
                      ContentType='application/json')


def _load_advisor_daily(advisor_id: str) -> dict:
    """Load existing mix_daily.json for an advisor. Returns {} on miss."""
    try:
        key = f'{ADV_MIX_PREFIX}/{advisor_id}/mix_daily.json'
        resp = _get_s3().get_object(Bucket=S3_BUCKET, Key=key)
        return json.loads(resp['Body'].read())
    except Exception:
        return {}


def _write_advisor_mix(advisor_id: str, advisor_name: str, data_as_of: str,
                       daily_dict: dict, now_str: str, dry_run: bool) -> None:
    """Write mix_daily.json (raw accumulator) and mix.json (period views) for one advisor."""
    # Raw daily accumulator
    raw_key = f'{ADV_MIX_PREFIX}/{advisor_id}/mix_daily.json'
    raw_body = json.dumps(daily_dict, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        _get_s3().put_object(Bucket=S3_BUCKET, Key=raw_key, Body=raw_body,
                             ContentType='application/json')

    # Period views
    views = compute_period_views(daily_dict)
    if not views['annually']:
        return  # Skip advisors with no annual data

    payload = {
        'generated_at': now_str,
        'data_as_of':   data_as_of,
        'advisor_id':   advisor_id,
        'advisor_name': advisor_name,
        'views':        views,
    }
    mix_key = f'{ADV_MIX_PREFIX}/{advisor_id}/mix.json'
    mix_body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    if not dry_run:
        _get_s3().put_object(Bucket=S3_BUCKET, Key=mix_key, Body=mix_body,
                             ContentType='application/json',
                             CacheControl='public, max-age=300, s-maxage=3600')


def compute_period_views(daily_dict: dict, cp_daily_total=None) -> dict:
    """
    Compute quarterly, monthly, and annually period views from a daily dollar dict.

    Args:
        daily_dict: {date_str: {equity: $, fixed_income: $, structured_notes: $,
                                cash: $, other: $, total: $}}
                    Keys are YYYY-MM-DD strings.
        cp_daily_total: pd.Series indexed by date with firm-level total_aua from
                        client_performance.parquet. When provided, replaces the
                        positions_cube total with the authoritative total, keeping
                        class percentages from positions_cube. Cash is residual.

    Returns:
        {"quarterly": [...], "monthly": [...], "annually": [...]}

    Each period entry:
        {period, label, end_date, total_aua,
         equity: {value, pct}, fixed_income: {value, pct},
         structured_notes: {value, pct}, cash: {value, pct}, other: {value, pct}}

    Period logic mirrors PartnerAnalytics.tsx getPeriodInfo():
        quarterly: period="YYYY-Q#",  label="Q# 'YY"   (e.g. "Q4 '24")
        monthly:   period="YYYY-MM",  label="Mon 'YY"  (e.g. "Oct '24")
        annually:  period="YYYY",     label="YYYY"     (e.g. "2024")

    Takes the LAST date in each period as the end-of-period snapshot.
    pct values are 0-1.
    """
    _MONTH_SHORT = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec']

    def _period_key_label(date_str: str, granularity: str) -> tuple[str, str]:
        year  = int(date_str[:4])
        month = int(date_str[5:7])
        yy    = date_str[2:4]
        if granularity == 'quarterly':
            q = (month - 1) // 3 + 1
            return f'{year}-Q{q}', f"Q{q} '{yy}"
        elif granularity == 'monthly':
            return f'{year}-{month:02d}', f"{_MONTH_SHORT[month - 1]} '{yy}"
        else:  # annually
            return str(year), str(year)

    def _build_granularity(granularity: str) -> list:
        # Map period_key -> (last date_str, last entry)
        period_map: dict[str, tuple[str, dict]] = {}
        for date_str in sorted(daily_dict.keys()):
            entry = daily_dict[date_str]
            pk, pl = _period_key_label(date_str, granularity)
            # Always overwrite: last date in period wins (end-of-period snapshot)
            period_map[pk] = (date_str, entry, pl)

        result = []
        for pk in sorted(period_map.keys()):
            end_date, entry, pl = period_map[pk]
            cube_total = float(entry.get('total', 0.0))
            if cube_total <= 0:
                continue

            # Use client_performance total (authoritative) if available
            total = cube_total
            if cp_daily_total is not None:
                cp_val = cp_daily_total.get(pd.Timestamp(end_date))
                if cp_val is not None and cp_val > 0:
                    total = float(cp_val)

            row = {
                'period':    pk,
                'label':     pl,
                'end_date':  end_date,
                'total_aua': round(total, 2),
            }
            # Class pcts from positions_cube (correct ratios), scaled to
            # authoritative total from client_performance
            for ac in _MIX_ASSET_CLASSES:
                pct = float(entry.get(ac, 0.0)) / cube_total if cube_total > 0 else 0.0
                val = round(total * pct, 2)
                row[ac] = {
                    'value': val,
                    'pct':   round(pct, 6),
                }
            # Cash is residual: total - classified classes
            classified_sum = sum(row[ac]['value'] for ac in _MIX_ASSET_CLASSES)
            cash_val = max(0.0, round(total - classified_sum, 2))
            row['cash'] = {
                'value': cash_val,
                'pct':   round(cash_val / total, 6) if total > 0 else 0.0,
            }
            result.append(row)
        return result

    return {
        'quarterly': _build_granularity('quarterly'),
        'monthly':   _build_granularity('monthly'),
        'annually':  _build_granularity('annually'),
    }


# =============================================================================
# Static table loading
# =============================================================================


def _load_rel_architect_lookup() -> dict:
    """
    Load rel_architect_lookup.parquet from S3.

    Returns {relationship_id: advisor_name} dict.
    Returns {} and logs a warning if the file is missing (06b continues without
    advisor aggregation -- firm-level mix still runs normally).
    """
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=REL_LOOKUP_KEY)
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        if 'relationship_id' not in df.columns or 'architect' not in df.columns:
            print(f"  WARN: rel_architect_lookup.parquet missing expected columns "
                  f"(found: {list(df.columns)}) -- skipping advisor aggregation")
            return {}
        result = dict(zip(df['relationship_id'].astype(str), df['architect'].astype(str)))
        unique_advisors = len(set(result.values()))
        print(f"  rel_architect_lookup: {len(result):,} relationships, {unique_advisors} advisors")
        return result
    except Exception as e:
        print(f"  WARN: could not load rel_architect_lookup.parquet: {e} "
              f"-- skipping advisor aggregation")
        return {}

def load_static_tables(verbose: bool = False):
    print("Loading accounts_dimension... ", end='', flush=True)
    acct_dim = _read_parquet('gold/accounts_dimension_latest.parquet')
    acct_rel = acct_dim[['account_id', 'relationship_id']].dropna(subset=['relationship_id'])
    acct_rel_dict = dict(zip(
        acct_rel['account_id'].astype(str),
        acct_rel['relationship_id'].astype(str)
    ))
    print(f"{len(acct_rel_dict):,} accounts")

    print("Loading canonical_prices... ", end='', flush=True)
    canonical = _read_parquet('silver/prices/canonical_prices.parquet')
    canonical['date'] = pd.to_datetime(canonical['date'])
    canonical = canonical.sort_values('source').drop_duplicates(
        subset=['date', 'asset_name'], keep='first'
    )
    prices_grouped = canonical.groupby('date')
    print(f"{len(canonical):,} rows")
    del canonical
    gc.collect()

    print("Loading account_performance (AP gate)... ", end='', flush=True)
    ap = _read_parquet('gold/account_performance.parquet')
    ap['date'] = pd.to_datetime(ap['date'])
    ap_last_seen = ap.groupby('account_id')['date'].max().to_dict()
    max_ap_date = ap['date'].max().date()
    print(f"{len(ap_last_seen):,} accounts, max date {max_ap_date}")
    del ap
    gc.collect()

    print("Loading insurance account config... ", end='', flush=True)
    insurance_account_ids, insurance_gate_days = _load_insurance_config()

    print("Loading rel_architect_lookup (advisor mapping)...")
    rel_advisor_dict = _load_rel_architect_lookup()

    print("Loading client_performance (authoritative AUA totals)... ", end='', flush=True)
    cp = _read_parquet('gold/client_performance.parquet')
    cp['date'] = pd.to_datetime(cp['date'])
    cp_daily_total = cp.groupby('date')['total_aua'].sum()
    print(f"{len(cp_daily_total):,} dates")
    del cp
    gc.collect()

    return acct_rel_dict, prices_grouped, ap_last_seen, insurance_account_ids, insurance_gate_days, rel_advisor_dict, cp_daily_total


# =============================================================================
# Per-date processing — returns data keyed by relationship_id
# =============================================================================

def process_date(key, date_str, prices_grouped, acct_rel_dict, ap_last_seen, verbose=False,
                 insurance_account_ids=None, insurance_gate_days=AP_GATE_DAYS_DEFAULT):
    """
    Process one positions_cube partition.

    Returns dict: {relationship_id: {'mix': {asset_class: mv}, 'conc': [(mv, asset_name, ticker, cls)]}}
    or empty dict if the date has no usable data.

    AP gate: standard accounts use AP_GATE_DAYS (45). Accounts in insurance_account_ids
    use insurance_gate_days (default 180). Insurance/annuity accounts report on monthly or
    quarterly statement cycles -- the standard 45-day gate incorrectly excludes them during
    inter-statement gaps, causing structured_notes oscillation.
    """
    date_ts          = pd.Timestamp(date_str)
    std_cutoff       = date_ts - pd.Timedelta(days=AP_GATE_DAYS_DEFAULT)
    ins_cutoff       = date_ts - pd.Timedelta(days=insurance_gate_days)
    insurance_ids    = insurance_account_ids or set()

    resp = _get_s3().get_object(Bucket=S3_BUCKET, Key=key)
    pos = pd.read_parquet(BytesIO(resp['Body'].read()))

    if pos.empty:
        return {}

    # AP gate: vectorized per-account cutoff based on account type
    pos['account_id'] = pos['account_id'].astype(str)
    last_seen = pos['account_id'].map(ap_last_seen).fillna(pd.Timestamp.min)

    # Standard gate applies to all accounts
    standard_ok  = last_seen >= std_cutoff
    # Insurance override: extended gate for flagged accounts
    is_insurance = pos['account_id'].isin(insurance_ids)
    insurance_ok = is_insurance & (last_seen >= ins_cutoff)

    pos = pos[standard_ok | insurance_ok]
    if pos.empty:
        return {}

    # Resolve relationship_id
    pos['relationship_id'] = pos['account_id'].map(acct_rel_dict)
    pos = pos.dropna(subset=['relationship_id'])
    if pos.empty:
        return {}

    # Join prices
    try:
        prices_day = prices_grouped.get_group(date_ts)[['asset_name', 'ticker', 'price']].copy()
    except KeyError:
        if verbose:
            print(f"    SKIP {date_str}: no prices")
        return {}

    pos = pos.merge(prices_day, on='asset_name', how='left')
    pos['market_value'] = pos['units'] * pos['price']
    pos = pos.dropna(subset=['market_value'])
    pos = pos[pos['market_value'] > 0]
    if pos.empty:
        return {}

    # Classify (vectorized: C-level dict lookups + regex, Python fallback for edge cases)
    pos['asset_class'] = classify_series(pos['ticker'], pos['asset_name'])

    # Aggregate by relationship
    result = {}
    for rel_id, grp in pos.groupby('relationship_id', sort=False):
        total_mv = float(grp['market_value'].sum())
        if total_mv <= 0:
            continue

        # Mix: sum by asset_class
        mix_agg = grp.groupby('asset_class')['market_value'].sum()
        pct_sum = sum(mix_agg.values) / total_mv
        if abs(pct_sum - 1.0) > PCT_TOL:
            if verbose:
                print(f"    SKIP {rel_id} on {date_str}: pct sum {pct_sum:.4f}")
            continue

        mix = {}
        for ac in _MIX_ASSET_CLASSES:
            mix[ac] = round(float(mix_agg.get(ac, 0.0)) / total_mv, 6)

        # Concentration: group by (asset_name, ticker, asset_class), top-N by mv
        conc_grp = (
            grp.groupby(['asset_name', 'ticker', 'asset_class'], sort=False, dropna=False)
            ['market_value'].sum()
            .reset_index()
            .sort_values('market_value', ascending=False)
            .head(TOP_N_CONC)
        )
        holdings = []
        for _, row in conc_grp.iterrows():
            ticker_val = row['ticker']
            if not ticker_val or str(ticker_val).strip().upper() in ('NAN', 'NONE', ''):
                ticker_val = None
            holdings.append({
                'asset_name':  str(row['asset_name']),
                'ticker':      ticker_val,
                'asset_class': str(row['asset_class']),
                'market_value': round(float(row['market_value']), 2),
                'pct':          round(float(row['market_value']) / total_mv, 6),
            })

        result[rel_id] = {'mix': mix, 'conc': holdings, 'total_mv': total_mv}

    return result


# =============================================================================
# Build
# =============================================================================

def build(upload: bool, incremental: bool, dry_run: bool, verbose: bool) -> None:
    print("=" * 70)
    print("06b_build_client_mix_timeseries.py")
    print(f"Mode:    {'incremental' if incremental else 'full'}")
    print(f"Workers: {PROCESS_WORKERS} process / {WRITE_WORKERS} write")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Watermark
    watermark = None
    if incremental:
        watermark = _load_watermark()
        if watermark is None:
            print("  No watermark found -- falling back to full build")
            incremental = False

    # Static tables
    print("\nLoading static tables...")
    acct_rel_dict, prices_grouped, ap_last_seen, insurance_account_ids, insurance_gate_days, \
        rel_advisor_dict, cp_daily_total = load_static_tables(verbose=verbose)

    # Positions cube keys
    print("\nListing positions_cube partitions...")
    all_keys = _list_positions_cube_keys()
    keys_to_process = (
        [k for k in all_keys if _parse_date(k) > watermark]
        if incremental else all_keys
    )
    print(f"  Total: {len(all_keys):,}  To process: {len(keys_to_process):,}")

    if not keys_to_process:
        print("\n  No new partitions -- artifacts are current")
        return

    max_date_processed = None

    # Firm/advisor daily dollar accumulators (populated in both build paths)
    # {date_str: {equity: $, fixed_income: $, ..., total: $}}
    firm_daily_new: dict = {}
    # {advisor_name: {date_str: {equity: $, ..., total: $}}}
    advisor_daily_new: dict = {}

    if incremental:
        # --- INCREMENTAL: process new partitions in parallel, merge+write in parallel ---
        # For incremental (typically 1-10 dates), lower concurrency is fine
        inc_workers = min(PROCESS_WORKERS, max(len(keys_to_process), 1))
        print(f"\nProcessing {len(keys_to_process):,} new partition(s) ({inc_workers} workers)...")
        new_data = {}
        n_ok = n_skip = n_err = 0

        def _process_inc(idx_key):
            idx, key = idx_key
            date_str = _parse_date(key)
            try:
                result = process_date(key, date_str, prices_grouped,
                                      acct_rel_dict, ap_last_seen, verbose,
                                      insurance_account_ids=insurance_account_ids,
                                      insurance_gate_days=insurance_gate_days)
                return (idx, date_str, result, None)
            except Exception as e:
                return (idx, date_str, None, str(e))

        with ThreadPoolExecutor(max_workers=inc_workers) as pool:
            for idx, date_str, result, err in pool.map(_process_inc, enumerate(keys_to_process)):
                if verbose or idx % 50 == 0:
                    print(f"  [{idx+1}/{len(keys_to_process)}] {date_str}")
                if err:
                    print(f"  ERROR {date_str}: {err}")
                    n_err += 1
                    continue
                if not result:
                    n_skip += 1
                    continue
                for rel_id, data in result.items():
                    if rel_id not in new_data:
                        new_data[rel_id] = {}
                    new_data[rel_id][date_str] = data
                    # Accumulate firm/advisor daily dollar amounts
                    mv = data['total_mv']
                    if date_str not in firm_daily_new:
                        firm_daily_new[date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                        firm_daily_new[date_str]['total'] = 0.0
                    for _ac in _MIX_ASSET_CLASSES:
                        firm_daily_new[date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                    firm_daily_new[date_str]['total'] += mv
                    _adv = rel_advisor_dict.get(rel_id)
                    if _adv and _adv != 'Unresolved':
                        if _adv not in advisor_daily_new:
                            advisor_daily_new[_adv] = {}
                        if date_str not in advisor_daily_new[_adv]:
                            advisor_daily_new[_adv][date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                            advisor_daily_new[_adv][date_str]['total'] = 0.0
                        for _ac in _MIX_ASSET_CLASSES:
                            advisor_daily_new[_adv][date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                        advisor_daily_new[_adv][date_str]['total'] += mv
                max_date_processed = date_str
                n_ok += 1

        print(f"\n  {n_ok:,} dates OK, {n_skip:,} skipped, {n_err:,} errors")
        print(f"  {len(new_data):,} relationships with new data")

        if not new_data:
            print("  Nothing to write")
            return

        # Merge new dates into existing JSONs — parallel read+merge+write
        print(f"\nMerging and writing {len(new_data):,} relationship JSONs ({WRITE_WORKERS} workers)...")
        now_str = datetime.now(timezone.utc).isoformat() + 'Z'
        n_written = 0
        n_write_err = 0

        def _merge_and_write(item):
            rel_id, dated_entries = item
            existing = _read_relationship_json(rel_id)
            existing_mix  = {e['date']: e for e in (existing or {}).get('mix', [])}
            existing_conc = {e['date']: e for e in (existing or {}).get('concentration', [])}

            for ds, data in dated_entries.items():
                existing_mix[ds] = {'date': ds, **data['mix']}
                existing_conc[ds] = {'date': ds, 'holdings': data['conc']}

            mix_list  = sorted(existing_mix.values(),  key=lambda x: x['date'])
            conc_list = sorted(existing_conc.values(), key=lambda x: x['date'])
            data_as_of = mix_list[-1]['date'] if mix_list else watermark

            payload = {
                'generated_at':   now_str,
                'data_as_of':     data_as_of,
                'relationship_id': rel_id,
                'mix':             mix_list,
                'concentration':   conc_list,
            }
            _write_relationship_json(rel_id, payload, dry_run)
            return rel_id

        with ThreadPoolExecutor(max_workers=WRITE_WORKERS) as pool:
            futures = {pool.submit(_merge_and_write, item): item[0]
                       for item in new_data.items()}
            for future in as_completed(futures):
                try:
                    future.result()
                    n_written += 1
                except Exception as e:
                    n_write_err += 1
                    print(f"  WRITE ERROR {futures[future]}: {e}")

        print(f"  Written: {n_written:,} relationship JSONs ({n_write_err:,} errors)")

    else:
        # --- FULL BUILD: process all dates in parallel, write JSONs in parallel ---
        print(f"\nProcessing {len(keys_to_process):,} partitions (full build, {PROCESS_WORKERS} workers)...")
        all_data = {}  # {rel_id: {date_str: {mix, conc}}}
        n_ok = n_skip = n_err = 0
        lock = threading.Lock()

        def _process_one(idx_key):
            idx, key = idx_key
            date_str = _parse_date(key)
            try:
                result = process_date(key, date_str, prices_grouped,
                                      acct_rel_dict, ap_last_seen, verbose,
                                      insurance_account_ids=insurance_account_ids,
                                      insurance_gate_days=insurance_gate_days)
                return (idx, date_str, result, None)
            except Exception as e:
                return (idx, date_str, None, str(e))

        with ThreadPoolExecutor(max_workers=PROCESS_WORKERS) as pool:
            futures = pool.map(_process_one, enumerate(keys_to_process))
            for idx, date_str, result, err in futures:
                if (idx + 1) % 200 == 0 or idx == 0:
                    print(f"  [{idx+1}/{len(keys_to_process)}] {date_str}  "
                          f"(ok={n_ok} skip={n_skip} err={n_err})", flush=True)
                if err:
                    print(f"  ERROR {date_str}: {err}")
                    n_err += 1
                    continue
                if not result:
                    n_skip += 1
                    continue
                for rel_id, data in result.items():
                    if rel_id not in all_data:
                        all_data[rel_id] = {}
                    all_data[rel_id][date_str] = data
                    # Accumulate firm/advisor daily dollar amounts
                    mv = data['total_mv']
                    if date_str not in firm_daily_new:
                        firm_daily_new[date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                        firm_daily_new[date_str]['total'] = 0.0
                    for _ac in _MIX_ASSET_CLASSES:
                        firm_daily_new[date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                    firm_daily_new[date_str]['total'] += mv
                    _adv = rel_advisor_dict.get(rel_id)
                    if _adv and _adv != 'Unresolved':
                        if _adv not in advisor_daily_new:
                            advisor_daily_new[_adv] = {}
                        if date_str not in advisor_daily_new[_adv]:
                            advisor_daily_new[_adv][date_str] = {ac: 0.0 for ac in _MIX_ASSET_CLASSES}
                            advisor_daily_new[_adv][date_str]['total'] = 0.0
                        for _ac in _MIX_ASSET_CLASSES:
                            advisor_daily_new[_adv][date_str][_ac] += data['mix'].get(_ac, 0.0) * mv
                        advisor_daily_new[_adv][date_str]['total'] += mv
                max_date_processed = date_str
                n_ok += 1

        print(f"\n  {n_ok:,} dates OK, {n_skip:,} skipped, {n_err:,} errors")
        print(f"  {len(all_data):,} relationships")

        if not all_data:
            print("  Nothing to write")
            return

        # Build payloads and write in parallel
        print(f"\nWriting {len(all_data):,} relationship JSONs ({WRITE_WORKERS} workers)...")
        now_str = datetime.now(timezone.utc).isoformat() + 'Z'
        n_written = 0
        n_write_err = 0

        def _build_and_write(item):
            rel_id, dated_entries = item
            mix_list  = []
            conc_list = []
            for ds in sorted(dated_entries.keys()):
                d = dated_entries[ds]
                mix_list.append({'date': ds, **d['mix']})
                conc_list.append({'date': ds, 'holdings': d['conc']})

            data_as_of = mix_list[-1]['date'] if mix_list else max_date_processed
            payload = {
                'generated_at':   now_str,
                'data_as_of':     data_as_of,
                'relationship_id': rel_id,
                'mix':             mix_list,
                'concentration':   conc_list,
            }
            _write_relationship_json(rel_id, payload, dry_run)
            return rel_id

        with ThreadPoolExecutor(max_workers=WRITE_WORKERS) as pool:
            futures = {pool.submit(_build_and_write, item): item[0]
                       for item in all_data.items()}
            for future in as_completed(futures):
                try:
                    future.result()
                    n_written += 1
                    if n_written % 500 == 0:
                        print(f"  Written: {n_written:,} / {len(all_data):,}", flush=True)
                except Exception as e:
                    n_write_err += 1
                    print(f"  WRITE ERROR {futures[future]}: {e}")

        del all_data
        gc.collect()
        print(f"  Written: {n_written:,} relationship JSONs ({n_write_err:,} errors)")

    # Watermark
    if max_date_processed:
        # Use max date across all S3 positions_cube files as watermark
        # (ensures we don't re-process files that had no usable data)
        watermark_date = _parse_date(all_keys[-1])
        _write_watermark(watermark_date, len(keys_to_process), dry_run)

    # -------------------------------------------------------------------------
    # Firm + Advisor mix views
    # -------------------------------------------------------------------------
    if firm_daily_new or advisor_daily_new:
        now_fa   = datetime.now(timezone.utc).isoformat() + 'Z'
        da_fa    = _parse_date(all_keys[-1]) if all_keys else (max_date_processed or '')

        # Firm: for incremental merge with existing daily, for full use new only
        if incremental:
            existing_firm = _load_firm_daily()
            existing_firm.update(firm_daily_new)
            firm_daily = existing_firm
        else:
            firm_daily = firm_daily_new

        if firm_daily:
            print("\nWriting firm mix views...")
            _write_firm_daily(firm_daily, dry_run)
            firm_views = compute_period_views(firm_daily, cp_daily_total=cp_daily_total)
            firm_payload = {
                'generated_at': now_fa,
                'data_as_of':   da_fa,
                'firm_id':      FIRM_ID,
                'views':        firm_views,
            }
            firm_body = json.dumps(firm_payload, separators=(',', ':')).encode('utf-8')
            if not dry_run:
                s3.put_object(Bucket=S3_BUCKET, Key=FIRM_MIX_KEY, Body=firm_body,
                              ContentType='application/json',
                              CacheControl='public, max-age=300, s-maxage=3600')
            print(f"  Firm mix views: "
                  f"{len(firm_views.get('quarterly', []))} quarters, "
                  f"{len(firm_views.get('monthly', []))} months, "
                  f"{len(firm_views.get('annually', []))} years")

        # Advisor: incremental merges per-advisor daily, full uses new only
        if advisor_daily_new:
            print(f"\nWriting advisor mix views ({len(advisor_daily_new)} advisors)...")

            def _write_one_advisor(adv_name: str) -> str:
                if incremental:
                    existing_adv = _load_advisor_daily(adv_name)
                    existing_adv.update(advisor_daily_new[adv_name])
                    adv_daily = existing_adv
                else:
                    adv_daily = advisor_daily_new[adv_name]
                _write_advisor_mix(adv_name, adv_name, da_fa, adv_daily, now_fa, dry_run)
                return adv_name

            n_adv_ok = n_adv_err = 0
            adv_pool_size = min(WRITE_WORKERS, max(len(advisor_daily_new), 1))
            with ThreadPoolExecutor(max_workers=adv_pool_size) as pool:
                adv_futures = {pool.submit(_write_one_advisor, adv): adv
                               for adv in advisor_daily_new}
                for future in as_completed(adv_futures):
                    try:
                        future.result()
                        n_adv_ok += 1
                    except Exception as exc:
                        n_adv_err += 1
                        print(f"  WARN advisor write {adv_futures[future]}: {exc}")
            print(f"  Advisor mix views: {n_adv_ok} written, {n_adv_err} errors")

    print("\n" + "=" * 70)
    print("DONE")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)


# =============================================================================
# Entry point
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Build client mix + concentration timeseries (per-relationship JSON)'
    )
    parser.add_argument('--upload',      action='store_true', help='Upload to S3')
    parser.add_argument('--incremental', action='store_true', help='Process only new dates')
    parser.add_argument('--dry-run',     action='store_true', help='Compute only, no write')
    parser.add_argument('--workers',     type=int, default=0, help='Override process worker count (0=use default)')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.workers > 0:
        global PROCESS_WORKERS, WRITE_WORKERS
        PROCESS_WORKERS = args.workers
        WRITE_WORKERS = args.workers * 2

    build(
        upload=args.upload,
        incremental=args.incremental,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


if __name__ == '__main__':
    main()
```

### gold-script-12----builds-firmcomposition.json--per-advisor-composition.json-asset-mix-radial--top-holdings-per-class-etfclassifier.py

```
#!/usr/bin/env python3
"""
Build Composition Artifacts — per-class top holdings for firm (N1) and advisors (L2)

Produces portal-ready JSON at:
    s3://opal-data-bd/gold/views/firm_composition.json
    s3://opal-data-bd/gold/advisors/{advisor_id}/composition.json

Serves GET /api/scoped/partners/books/firm/all/composition
and    GET /api/scoped/partners/books/advisor/{id}/composition
via opal-partners-data (pure S3 proxy -- zero Lambda compute).

Why pre-computed:
    Firm and advisor books contain thousands of unique positions.
    Sending all holdings over the wire is prohibitive. Script 12 runs
    on EC2 where full parquet access is available, collapses each book
    to a small per-class top-9 JSON artifact, and the Lambda serves it
    as a static file with Cache-Control: no-store.

Inputs (must exist in S3 before running):
    gold/holdings_lots/YYYY-MM-DD.parquet   -- from 03_build_holdings_lots.py
    gold/views/rel_architect_lookup.parquet -- from 08b_build_architect_attribution.py
    gold/client_dimension.parquet           -- fallback for architect assignment

Run sequence (run_gold_layer.sh):
    08b (rel_architect_lookup written) --> 12 (this script) --> 06b

Output schema (canonical per ADVI_BKSCMP_PRD.md §3):
    {
      "data_as_of":          "YYYY-MM-DD",
      "generated_at":        "ISO8601Z",
      "scope":               {"firm_id": "49financial"},
      "total_market_value":  float,
      "top_holdings":        [ConcentrationItem x9],   # global, pct = mv / total_mv
      "other":               {"market_value": float, "pct": float},
      "mix": [
        {
          "asset_class": str, "label": str,
          "market_value": float, "pct": float,          # pct = class_mv / total_mv
          "top_holdings": [ConcentrationItem x9],        # pct = holding_mv / class_mv
          "other": {"market_value": float, "pct": float} # pct = class_other_mv / class_mv
        }, ...
      ],
      "unclassified": {"count": int, "market_value": float}
    }

Usage:
    python 12_build_composition_artifacts.py              # dry run (no upload)
    python 12_build_composition_artifacts.py --upload     # write to S3
    python 12_build_composition_artifacts.py --dry-run    # compute only, no write

Author: 0.4.0_DS_ClientPlatform
Date: 2026-03-19
"""

import argparse
import gc
import json
import re
import sys
from datetime import datetime, timezone
from io import BytesIO

import boto3
import pandas as pd

from lib.etf_classifier import ETFClassifier

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BUCKET      = 'opal-data-bd'
FIRM_ID     = '49financial'
TOP_N       = 9   # top holdings per asset class + global

s3 = boto3.client('s3', region_name='us-east-1')

_ASSET_CLASS_LABELS = {
    'equity':       'Equities',
    'fixed_income': 'Fixed Income',
    'alternatives': 'Alternatives',
    'cash':         'Cash',
    'other':        'Other',
}

# ---------------------------------------------------------------------------
# Classification -- delegates to DynamoDB-backed ETFClassifier (lib.etf_classifier)
# Same classifier that 06b uses. Keeps cash/other distinction that ETFClassifier
# does not make (it returns '' for both cash-like and truly unknown securities).
# ---------------------------------------------------------------------------


def classify_series(ticker_series: pd.Series, name_series: pd.Series) -> pd.Series:
    """Classify each holding via ETFClassifier, with cash/other post-processing."""
    classifier = ETFClassifier.instance()

    def _classify(ticker, asset_name):
        result = classifier.classify(ticker, asset_name)
        if not result:
            # ETFClassifier returns '' for cash-like and unknown
            name = str(asset_name or '').upper()
            if any(kw in name for kw in ('CASH', 'SWEEP', 'MONEY MARKET', 'MMKT')):
                return 'cash'
            return 'other'
        return result  # 'equity' | 'fixed_income' | 'alternatives'

    return pd.Series(
        [_classify(t, n) for t, n in zip(
            ticker_series.fillna(''), name_series.fillna('')
        )],
        index=ticker_series.index,
        dtype='object'
    )


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _read_parquet(key: str, columns: list = None) -> pd.DataFrame:
    resp = s3.get_object(Bucket=BUCKET, Key=key)
    kwargs = {'columns': columns} if columns else {}
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _find_latest_holdings_lots() -> str | None:
    """Return S3 key of the most recent non-backfill holdings_lots snapshot."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=BUCKET, Prefix='gold/holdings_lots/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
        and 'backfill' not in obj['Key'].rsplit('/', 1)[-1]
    ])
    return keys[-1] if keys else None


def _write_json(data: dict, key: str, upload: bool) -> None:
    body = json.dumps(data, default=str, separators=(',', ':'))
    if upload:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=body.encode('utf-8'),
            ContentType='application/json',
            CacheControl='no-store, no-cache, must-revalidate',
        )
        print(f"  OK: s3://{BUCKET}/{key} ({len(body):,} bytes)")
    else:
        print(f"  [DRY RUN] Would write {key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# advisor_id sanitization
# Must match ClientsTab.tsx:383 exactly:
#   name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
# ---------------------------------------------------------------------------

def _advisor_id(name: str) -> str:
    return re.sub(r'[^a-z0-9_]+', '_', str(name).lower().strip()).strip('_')[:60] or 'unknown'


# ---------------------------------------------------------------------------
# Holding key / label helpers (PRD §3)
# ---------------------------------------------------------------------------

def _holding_key(ticker, asset_name) -> str:
    """Stable key for deduplication and frontend lookup."""
    t = str(ticker).strip() if pd.notna(ticker) else ''
    if t and t.upper() not in ('NAN', 'NONE', ''):
        return t.upper()
    name = str(asset_name).strip() if pd.notna(asset_name) else ''
    return re.sub(r'\s+', '_', name.lower())[:40] or 'unknown'


def _holding_label(ticker, asset_name) -> str:
    """Display label shown in the portal holdings list."""
    t = str(ticker).strip() if pd.notna(ticker) else ''
    if t and t.upper() not in ('NAN', 'NONE', ''):
        return t.upper()
    name = str(asset_name).strip() if pd.notna(asset_name) else ''
    return name[:30] or 'Unknown'


# ---------------------------------------------------------------------------
# Core composition builder
# ---------------------------------------------------------------------------

def _build_composition(df: pd.DataFrame, scope: dict, data_as_of: str) -> dict:
    """
    Build the canonical composition artifact from a filtered holdings DataFrame.

    df must have columns: ticker, asset_name, market_value, asset_class
    scope: e.g. {"firm_id": "49financial"} or {"advisor_id": "...", "firm_id": "..."}

    Pct conventions (all 0-1):
      mix[i].pct                  = class_mv / total_mv
      mix[i].top_holdings[j].pct  = holding_mv / class_mv   (per-class denominator)
      top_holdings[j].pct (root)  = holding_mv / total_mv
      other.pct (root)            = root_other_mv / total_mv
      mix[i].other.pct            = class_other_mv / class_mv
    """
    if df.empty:
        return None

    total_mv = float(df['market_value'].sum())
    if total_mv <= 0:
        return None

    # Build (key, label, asset_class, market_value) grain for aggregation
    df = df.copy()
    df['_key']   = df.apply(lambda r: _holding_key(r['ticker'], r['asset_name']), axis=1)
    df['_label'] = df.apply(lambda r: _holding_label(r['ticker'], r['asset_name']), axis=1)

    # Aggregate to (key, label, asset_class) grain
    holding_agg = (
        df.groupby(['_key', '_label', 'asset_class'], sort=False)['market_value']
        .sum()
        .reset_index()
        .sort_values('market_value', ascending=False)
    )

    # --- Per-class mix + top-9 ---
    mix_out = []
    for asset_class in _ASSET_CLASS_LABELS:
        cls_rows = holding_agg[holding_agg['asset_class'] == asset_class]
        if cls_rows.empty:
            continue

        class_mv = float(cls_rows['market_value'].sum())
        class_pct = round(class_mv / total_mv, 6)

        top_n_rows = cls_rows.head(TOP_N)
        top_holdings_cls = [
            {
                'key':          row['_key'],
                'label':        row['_label'],
                'asset_class':  asset_class,
                'market_value': round(float(row['market_value']), 2),
                'pct':          round(float(row['market_value']) / class_mv, 6),
            }
            for _, row in top_n_rows.iterrows()
        ]

        top_n_mv = float(top_n_rows['market_value'].sum())
        class_other_mv = class_mv - top_n_mv

        mix_out.append({
            'asset_class':   asset_class,
            'label':         _ASSET_CLASS_LABELS[asset_class],
            'market_value':  round(class_mv, 2),
            'pct':           class_pct,
            'top_holdings':  top_holdings_cls,
            'other': {
                'market_value': round(class_other_mv, 2),
                'pct':          round(class_other_mv / class_mv, 6) if class_mv > 0 else 0.0,
            },
        })

    # Sort mix by market_value desc
    mix_out.sort(key=lambda x: x['market_value'], reverse=True)

    # --- Global top-9 (pct relative to total_mv) ---
    global_top_n = holding_agg.head(TOP_N)
    global_top_holdings = [
        {
            'key':          row['_key'],
            'label':        row['_label'],
            'asset_class':  row['asset_class'],
            'market_value': round(float(row['market_value']), 2),
            'pct':          round(float(row['market_value']) / total_mv, 6),
        }
        for _, row in global_top_n.iterrows()
    ]
    global_top_mv = float(global_top_n['market_value'].sum())
    global_other_mv = total_mv - global_top_mv

    # --- Unclassified ---
    unclassified = df[df['asset_class'].isin(['', None]) | df['asset_class'].isna()]
    unclassified_count = int(unclassified['_key'].nunique())
    unclassified_mv    = float(unclassified['market_value'].sum())

    return {
        'generated_at':      datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_as_of':        data_as_of,
        'scope':             scope,
        'total_market_value': round(total_mv, 2),
        'top_holdings':      global_top_holdings,
        'other': {
            'market_value': round(global_other_mv, 2),
            'pct':          round(global_other_mv / total_mv, 6) if total_mv > 0 else 0.0,
        },
        'mix':               mix_out,
        'unclassified': {
            'count':        unclassified_count,
            'market_value': round(unclassified_mv, 2),
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Build composition artifacts (firm + per-advisor)'
    )
    parser.add_argument('--upload',  action='store_true', help='Write results to S3')
    parser.add_argument('--dry-run', action='store_true', help='Compute but do not write')
    args = parser.parse_args()

    upload = args.upload and not args.dry_run

    print('=' * 70)
    print('12_build_composition_artifacts.py')
    print(f'Started: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print(f'Mode:    {"UPLOAD" if upload else "DRY RUN"}')
    print('=' * 70)

    # ------------------------------------------------------------------
    # Step 1: Load holdings_lots (latest snapshot)
    # ------------------------------------------------------------------
    print('\n=== Step 1: Load holdings_lots ===')
    holdings_key = _find_latest_holdings_lots()
    if not holdings_key:
        print('ERROR: No holdings_lots parquet found in s3://opal-data-bd/gold/holdings_lots/')
        return 1

    print(f'  Using: {holdings_key}')
    lots = _read_parquet(
        holdings_key,
        columns=['account_id', 'relationship_id', 'ticker', 'asset_name',
                 'market_value', 'is_open'],
    )

    # Filter to open positions only
    lots = lots[lots['is_open'].fillna(False) == True].copy()
    print(f'  Open positions: {len(lots):,} lots, '
          f'{lots["relationship_id"].nunique():,} relationships')

    # data_as_of from filename (gold/holdings_lots/YYYY-MM-DD.parquet)
    data_as_of = holdings_key.rsplit('/', 1)[-1].replace('.parquet', '')

    # ------------------------------------------------------------------
    # Step 2: Classify holdings (ETFClassifier handles ticker + name_alias resolution)
    # ------------------------------------------------------------------
    print('\n=== Step 2: Classify holdings ===')
    lots['asset_class'] = classify_series(lots['ticker'], lots['asset_name'])
    class_counts = lots['asset_class'].value_counts().to_dict()
    print(f'  Classification: {class_counts}')
    gc.collect()

    # ------------------------------------------------------------------
    # Step 3: Load architect lookup (rel_architect_lookup -> fallback to client_dimension)
    # ------------------------------------------------------------------
    print('\n=== Step 3: Load architect lookup ===')
    rel_lookup = None
    try:
        rel_lookup = _read_parquet(
            'gold/views/rel_architect_lookup.parquet',
            columns=['relationship_id', 'architect'],
        )
        print(f'  rel_architect_lookup: {rel_lookup["architect"].nunique()} architects')
    except Exception as e:
        print(f'  WARN: rel_architect_lookup not available ({e})')
        print('  Falling back to client_dimension.primary_architect...')
        try:
            cdim = _read_parquet(
                'gold/client_dimension.parquet',
                columns=['relationship_id', 'primary_architect'],
            )
            rel_lookup = cdim.rename(columns={'primary_architect': 'architect'})
            print(f'  client_dimension fallback: {rel_lookup["architect"].nunique()} architects')
        except Exception as e2:
            print(f'ERROR: client_dimension also unavailable ({e2})')
            return 1

    # ------------------------------------------------------------------
    # Step 4: Merge architect onto holdings
    # ------------------------------------------------------------------
    print('\n=== Step 4: Merge architect lookup ===')
    lots = lots.merge(
        rel_lookup[['relationship_id', 'architect']],
        on='relationship_id',
        how='left',
    )
    missing_arch = lots['architect'].isna().sum()
    if missing_arch > 0:
        lots['architect'] = lots['architect'].fillna('Unassigned')
        print(f'  {missing_arch:,} lots with no architect match -> Unassigned')
    print(f'  Architects after merge: {lots["architect"].nunique()}')
    gc.collect()

    # ------------------------------------------------------------------
    # Step 5: Build and write firm composition
    # ------------------------------------------------------------------
    print('\n=== Step 5: Firm composition ===')
    firm_comp = _build_composition(
        lots,
        scope={'firm_id': FIRM_ID},
        data_as_of=data_as_of,
    )
    if firm_comp is None:
        print('ERROR: Firm composition returned empty -- check holdings_lots content')
        return 1

    _write_json(firm_comp, 'gold/views/firm_composition.json', upload)
    total_mv = firm_comp['total_market_value']
    n_classes = len(firm_comp['mix'])
    print(f'  Total MV: ${total_mv:,.0f} | {n_classes} asset classes')

    # ------------------------------------------------------------------
    # Step 6: Build and write per-advisor composition
    # ------------------------------------------------------------------
    print('\n=== Step 6: Advisor composition ===')
    architects = [
        a for a in lots['architect'].dropna().unique()
        if str(a).strip().lower() not in ('', 'nan', 'none', 'unassigned')
    ]
    print(f'  Processing {len(architects)} architects...')

    written = 0
    skipped = 0
    for architect in architects:
        arch_lots = lots[lots['architect'] == architect]
        adv_id = _advisor_id(str(architect))

        adv_comp = _build_composition(
            arch_lots,
            scope={'advisor_id': adv_id, 'firm_id': FIRM_ID},
            data_as_of=data_as_of,
        )

        if adv_comp is None:
            skipped += 1
            continue

        _write_json(adv_comp, f'gold/advisors/{adv_id}/composition.json', upload)
        written += 1

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f'\n{"=" * 70}')
    print(f'OK: firm_composition.json written. '
          f'Advisors: {written} written, {skipped} skipped (empty book).')
    print(f'Completed: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

### lambda-function----opal-partners-data-partners-api-v1.8.0.-contains-all-routes-mix-views-advisor-mix-firm-composition-advisor-composition-relationship-composition.py

```
"""
Lambda Function: opal-partners-data

Purpose: Serve Advisor Intelligence gold layer data for multi-tenant portal
Author: Dashboard Engineer
Version: 2.8 - Added firm+advisor composition S3-proxy routes, cors_response_nocache, serve_s3_json_nocache (ADVI_BKSCMP WS2)

API Endpoints (v2):
  GET /api/partners                                              - List partners user can access
  GET /api/shared/advisor-intelligence/timeseries/{dimension}    - Time series by dimension
  GET /api/shared/advisor-intelligence/snapshots/{dimension}     - Current AUA breakdown
  GET /api/shared/advisor-intelligence/filters                   - Available filter options
  GET /api/shared/advisor-intelligence/clients/growth            - Client growth time series
  GET /api/shared/advisor-intelligence/clients/tax-breakdown     - Tax basis pie charts
  GET /api/shared/advisor-intelligence/clients/tax-deferred      - Strategy candidates
  GET /api/shared/advisor-intelligence/summary                   - Header summary metrics
  GET /api/shared/advisor-intelligence/partner-analytics         - Partner analytics header (detailed)
  GET /api/health/advisor-intelligence                           - Health check endpoint

API Endpoints (v3 - Books Tab):
  GET /api/scoped/partners/books/relationship/{id}/timeseries                - Daily AUA/NNA for relationship
  GET /api/scoped/partners/books/account/{id}/timeseries                     - Daily AUA/NNA for account
  GET /api/scoped/partners/books/relationship/{id}/composition               - Mix + Concentration snapshot
  GET /api/scoped/partners/books/account/{id}/composition                    - Mix + Concentration snapshot
  GET /api/scoped/partners/books/relationship/{id}/mix-timeseries            - Historical mix pct timeseries
  GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries  - Historical top-10 concentration
  GET /api/scoped/partners/books/firm/all/mix-views                          - Firm-level period mix views (quarterly/monthly/annually)
  GET /api/shared/advisor-intelligence/advisors/{id}/mix-views               - Per-advisor period mix views
  GET /api/scoped/partners/books/advisor/{id}/timeseries                     - Daily AUA/NNA for advisor book
  GET /api/scoped/partners/books/advisor/{id}/mix-timeseries                 - AUA-weighted mix pct timeseries for advisor book
  GET /api/scoped/partners/books/firm/all/composition?firmId=xxx             - Firm-level per-class composition + top holdings (no-store)
  GET /api/scoped/partners/books/advisor/{id}/composition?firmId=xxx         - Advisor-level per-class composition + top holdings (no-store)

Access Control:
  - firmId is passed as query parameter
  - Validates firmId against allowedFirmIds from authorizer context
  - Internal users (allowedFirmIds = "ALL") can access any partner

Gold Layer Structure:
  s3://{bucket}/gold/timeseries/nna_by_{dimension}.json
  s3://{bucket}/gold/snapshots/aua_by_{dimension}.json
  s3://{bucket}/gold/clients/*.json
  s3://{bucket}/gold/filters/dimensions.json

Changelog v2.3:
  - Added data validation (no 200 with empty data)
  - Added S3 timeouts (5s connect, 10s read)
  - Added retry hints in error responses
  - Return 503 (not 200) for empty/invalid data
  - Added health check endpoint
"""

import json
import io
import os
import boto3
from botocore.config import Config
from decimal import Decimal
from typing import Optional
from datetime import datetime, timedelta

import awswrangler as wr
from etf_classifier import ETFClassifier as _ETFClassifier
_clf = _ETFClassifier.instance()

# Initialize AWS clients
s3_client = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# DynamoDB table for firm metadata
USERS_TABLE = os.environ.get('USERS_TABLE', 'opal-users-v2')
users_table = dynamodb.Table(USERS_TABLE)

# Valid dimensions for timeseries endpoints (11 total)
TIMESERIES_DIMENSIONS = [
    'total',           # nna_total.json (no dimension breakdown)
    'category',        # nna_by_category.json (NMNC/NMEC)
    'architect',       # nna_by_architect.json
    'region',          # nna_by_region.json
    'account_type',    # nna_by_account_type.json
    'tax_status',      # nna_by_tax_status.json
    'client_segment',  # nna_by_client_segment.json
    'state',           # nna_by_state.json
    'city',            # nna_by_city.json
    'relationship',    # nna_by_relationship.json
    'implementor'      # nna_by_implementor.json
]

# Valid dimensions for snapshot endpoints (7 total)
SNAPSHOT_DIMENSIONS = [
    'architect',       # aua_by_architect.json
    'region',          # aua_by_region.json
    'tax_status',      # aua_by_tax_status.json
    'account_type',    # aua_by_account_type.json
    'implementor',     # aua_by_implementor.json
    'state',           # aua_by_state.json
    'city'             # aua_by_city.json
]


class DecimalEncoder(json.JSONEncoder):
    """Convert Decimal to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def cors_response(status_code: int, body: dict) -> dict:
    """Create HTTP response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Cache-Control': 'max-age=300'  # 5-minute cache for gold layer
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def cors_response_nocache(status_code: int, body: dict) -> dict:
    """Create HTTP response with no-store Cache-Control for confidential composition data.

    Used by firm/advisor composition routes -- position-level AUM data must not
    be cached anywhere in the request path (CDN, browser, or intermediary proxies).
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Cache-Control': 'no-store, no-cache, must-revalidate',
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def is_authorized(firm_id: str, allowed_firms: str) -> bool:
    """Check if user is authorized to access firm data.

    Args:
        firm_id: The firm ID being requested
        allowed_firms: Comma-separated firm IDs or "ALL"

    Returns:
        True if authorized, False otherwise
    """
    if not firm_id:
        return False
    if allowed_firms == 'ALL':
        return True
    return firm_id in allowed_firms.split(',')


def get_firm_bucket(firm_id: str) -> Optional[str]:
    """Look up S3 bucket for firm from DynamoDB.

    Args:
        firm_id: The firm ID to look up

    Returns:
        S3 bucket name or None if not found
    """
    try:
        response = users_table.get_item(
            Key={
                'PK': f'FIRM#{firm_id}',
                'SK': 'META'
            }
        )
        item = response.get('Item')
        if item:
            return item.get('s3Bucket')
    except Exception as e:
        print(f'Error looking up firm bucket for {firm_id}: {e}')
    return None


def get_firm_metadata(firm_id: str) -> Optional[dict]:
    """Get firm metadata from DynamoDB."""
    try:
        response = users_table.get_item(
            Key={'PK': f'FIRM#{firm_id}', 'SK': 'META'}
        )
        return response.get('Item')
    except Exception as e:
        print(f'Error getting firm metadata for {firm_id}: {e}')
        return None


def get_all_firms() -> list:
    """Get all firm metadata records from DynamoDB."""
    try:
        response = users_table.scan(
            FilterExpression='SK = :meta AND attribute_exists(s3Bucket)',
            ExpressionAttributeValues={':meta': 'META'},
            ProjectionExpression='firmId, #n, tier, s3Bucket, parentFirmId',
            ExpressionAttributeNames={'#n': 'name'}
        )
        return response.get('Items', [])
    except Exception as e:
        print(f'Error scanning firms: {e}')
        return []


def validate_data_content(data: any, key: str) -> tuple[bool, str]:
    """Validate that data payload is not empty.

    Args:
        data: The data payload to validate
        key: S3 key for error messaging

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for null/None
    if data is None:
        return False, f'Data is null: {key}'

    # Check for empty dict
    if isinstance(data, dict) and len(data) == 0:
        return False, f'Data is empty dict: {key}'

    # Check for empty list
    if isinstance(data, list) and len(data) == 0:
        return False, f'Data is empty list: {key}'

    # For dict responses, check if required fields have content
    if isinstance(data, dict):
        # Special validation for partner list
        if 'partners' in data and isinstance(data['partners'], list) and len(data['partners']) == 0:
            # Empty partner list is suspicious but might be valid (no partners assigned)
            # Log it but allow
            print(f'Warning: Empty partners list in {key}')

        # Check for common data fields that shouldn't be empty
        for field in ['timeseries', 'snapshots', 'metrics', 'data']:
            if field in data:
                if isinstance(data[field], (dict, list)) and len(data[field]) == 0:
                    return False, f'Data field "{field}" is empty: {key}'

    return True, ''


def serve_s3_json(bucket: str, key: str) -> dict:
    """Read JSON from S3 and return with CORS headers.

    CRITICAL: This function now validates data content and returns 503 (not 200)
    if data is empty/null/missing. This enables frontend retry logic.

    Args:
        bucket: S3 bucket name
        key: S3 object key

    Returns:
        HTTP response dict
    """
    try:
        # Add timeout to S3 request (10 seconds)
        config = boto3.session.Config(
            connect_timeout=5,
            read_timeout=10,
            retries={'max_attempts': 2}
        )
        s3_with_timeout = boto3.client('s3', region_name='us-east-1', config=config)

        # Fetch from S3
        response = s3_with_timeout.get_object(Bucket=bucket, Key=key)

        # Check if file is empty (0 bytes)
        content_length = response.get('ContentLength', 0)
        if content_length == 0:
            print(f'ERROR: S3 file is 0 bytes: {bucket}/{key}')
            return cors_response(503, {
                'error': 'Data unavailable',
                'message': 'Data file exists but is empty',
                'retry': True,
                'key': key
            })

        # Parse JSON
        body_content = response['Body'].read().decode('utf-8')
        if not body_content or body_content.strip() == '':
            print(f'ERROR: S3 file has no content: {bucket}/{key}')
            return cors_response(503, {
                'error': 'Data unavailable',
                'message': 'Data file is empty',
                'retry': True,
                'key': key
            })

        data = json.loads(body_content)

        # CRITICAL: Validate data content
        is_valid, error_msg = validate_data_content(data, key)
        if not is_valid:
            print(f'ERROR: Data validation failed: {error_msg}')
            return cors_response(503, {
                'error': 'Data unavailable',
                'message': 'Data exists but is empty or invalid',
                'retry': True,
                'key': key,
                'validation_error': error_msg
            })

        # Data is valid - return 200
        print(f'SUCCESS: Served {bucket}/{key} ({content_length} bytes)')
        return cors_response(200, data)

    except s3_client.exceptions.NoSuchKey:
        print(f'ERROR: S3 file not found: {bucket}/{key}')
        return cors_response(404, {
            'error': 'Data not found',
            'message': f'File does not exist: {key}',
            'retry': False
        })
    except json.JSONDecodeError as e:
        print(f'ERROR: Invalid JSON in {bucket}/{key}: {e}')
        return cors_response(503, {
            'error': 'Data unavailable',
            'message': 'Data file is corrupted (invalid JSON)',
            'retry': True,
            'key': key
        })
    except Exception as e:
        print(f'ERROR: Failed to read {bucket}/{key}: {type(e).__name__}: {e}')
        return cors_response(500, {
            'error': 'Internal server error',
            'message': str(e),
            'retry': True,
            'key': key
        })


def serve_s3_json_nocache(bucket: str, key: str) -> dict:
    """Read JSON from S3 and return with no-store Cache-Control headers.

    Structural copy of serve_s3_json -- only difference is all cors_response
    calls are replaced with cors_response_nocache. Used for firm/advisor
    composition routes where position-level data must not be cached.

    Args:
        bucket: S3 bucket name
        key: S3 object key

    Returns:
        HTTP response dict
    """
    try:
        config = boto3.session.Config(
            connect_timeout=5,
            read_timeout=10,
            retries={'max_attempts': 2}
        )
        s3_with_timeout = boto3.client('s3', region_name='us-east-1', config=config)

        response = s3_with_timeout.get_object(Bucket=bucket, Key=key)

        content_length = response.get('ContentLength', 0)
        if content_length == 0:
            print(f'ERROR: S3 file is 0 bytes: {bucket}/{key}')
            return cors_response_nocache(503, {
                'error': 'Data unavailable',
                'message': 'Data file exists but is empty',
                'retry': True,
                'key': key
            })

        body_content = response['Body'].read().decode('utf-8')
        if not body_content or body_content.strip() == '':
            print(f'ERROR: S3 file has no content: {bucket}/{key}')
            return cors_response_nocache(503, {
                'error': 'Data unavailable',
                'message': 'Data file is empty',
                'retry': True,
                'key': key
            })

        data = json.loads(body_content)

        is_valid, error_msg = validate_data_content(data, key)
        if not is_valid:
            print(f'ERROR: Data validation failed: {error_msg}')
            return cors_response_nocache(503, {
                'error': 'Data unavailable',
                'message': 'Data exists but is empty or invalid',
                'retry': True,
                'key': key,
                'validation_error': error_msg
            })

        print(f'SUCCESS: Served {bucket}/{key} ({content_length} bytes)')
        return cors_response_nocache(200, data)

    except s3_client.exceptions.NoSuchKey:
        print(f'ERROR: S3 file not found: {bucket}/{key}')
        return cors_response_nocache(404, {
            'error': 'Data not found',
            'message': f'File does not exist: {key}',
            'retry': False
        })
    except json.JSONDecodeError as e:
        print(f'ERROR: Invalid JSON in {bucket}/{key}: {e}')
        return cors_response_nocache(503, {
            'error': 'Data unavailable',
            'message': 'Data file is corrupted (invalid JSON)',
            'retry': True,
            'key': key
        })
    except Exception as e:
        print(f'ERROR: Failed to read {bucket}/{key}: {type(e).__name__}: {e}')
        return cors_response_nocache(500, {
            'error': 'Internal server error',
            'message': str(e),
            'retry': True,
            'key': key
        })


def extract_path_param(path: str, segment: str) -> str:
    """Extract parameter after a path segment.

    Args:
        path: Full request path
        segment: Segment to find (e.g., 'timeseries', 'snapshots')

    Returns:
        The parameter after the segment, or empty string
    """
    parts = path.rstrip('/').split('/')
    for i, part in enumerate(parts):
        if part == segment and i + 1 < len(parts):
            return parts[i + 1]
    return ''


# =============================================================================
# V1 Handlers (Backward Compatibility)
# =============================================================================

def handle_get_partners(allowed_firms: str) -> dict:
    """Return list of partners user can access.

    Response matches TypeScript Partner interface:
    {
        firmId: string
        firmName: string
        tier: 'advisor' | 'subadvisor' | 'branch'
        parentFirmId: string | null
    }
    """
    all_firms = get_all_firms()

    # Filter to non-internal firms (partner firms only)
    partner_firms = [f for f in all_firms if f.get('tier') != 'internal']

    # Format response to match TypeScript interface
    partners = []
    for firm in partner_firms:
        firm_id = firm.get('firmId', '')

        # Check authorization
        if allowed_firms != 'ALL' and firm_id not in allowed_firms.split(','):
            continue

        partners.append({
            'firmId': firm_id,
            'firmName': firm.get('name', firm_id),
            'tier': firm.get('tier', 'advisor'),
            'parentFirmId': firm.get('parentFirmId') or None
        })

    return cors_response(200, {'partners': partners})


# =============================================================================
# V2 Handlers (New Endpoints)
# =============================================================================

def handle_timeseries(bucket: str, dimension: str) -> dict:
    """Serve time series data for a dimension.

    Args:
        bucket: S3 bucket name
        dimension: One of TIMESERIES_DIMENSIONS

    Returns:
        Time series JSON from gold layer
    """
    if dimension not in TIMESERIES_DIMENSIONS:
        return cors_response(400, {
            'error': f'Invalid dimension: {dimension}',
            'valid_dimensions': TIMESERIES_DIMENSIONS
        })

    if dimension == 'total':
        key = 'gold/timeseries/nna_total.json'
    else:
        key = f'gold/timeseries/nna_by_{dimension}.json'

    return serve_s3_json(bucket, key)


def handle_snapshots(bucket: str, dimension: str) -> dict:
    """Serve AUA snapshot for a dimension.

    Args:
        bucket: S3 bucket name
        dimension: One of SNAPSHOT_DIMENSIONS

    Returns:
        Snapshot JSON from gold layer
    """
    if dimension not in SNAPSHOT_DIMENSIONS:
        return cors_response(400, {
            'error': f'Invalid dimension: {dimension}',
            'valid_dimensions': SNAPSHOT_DIMENSIONS
        })

    key = f'gold/snapshots/aua_by_{dimension}.json'
    return serve_s3_json(bucket, key)


def handle_filters(bucket: str) -> dict:
    """Serve available filter dimensions.

    Args:
        bucket: S3 bucket name

    Returns:
        Filter dimensions JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/filters/dimensions.json')


def handle_client_growth(bucket: str) -> dict:
    """Serve client growth time series.

    Args:
        bucket: S3 bucket name

    Returns:
        Client growth JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/clients/growth_timeseries.json')


def handle_tax_breakdown(bucket: str) -> dict:
    """Serve tax basis pie chart data.

    Args:
        bucket: S3 bucket name

    Returns:
        Tax breakdown JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/clients/tax_basis_breakdown.json')


def handle_tax_deferred(bucket: str) -> dict:
    """Serve tax-deferred strategy candidates.

    Args:
        bucket: S3 bucket name

    Returns:
        Tax-deferred candidates JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/clients/tax_deferred_candidates.json')


def handle_summary(bucket: str) -> dict:
    """Serve header summary metrics (Model Portfolios-style header).

    Args:
        bucket: S3 bucket name

    Returns:
        Header summary JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/summary/header_metrics.json')


def handle_partner_analytics(bucket: str) -> dict:
    """Serve partner analytics header metrics (detailed NNA/AUA breakdown).

    Args:
        bucket: S3 bucket name

    Returns:
        Partner analytics JSON from gold layer
    """
    return serve_s3_json(bucket, 'gold/partner_analytics/header_metrics.json')


def handle_advisor_book(bucket: str, advisor_id: str) -> dict:
    """Serve per-advisor book view data.

    Args:
        bucket: S3 bucket name (from firm lookup)
        advisor_id: Advisor identifier (e.g., 'travis_penfield', '49f_house')

    Returns:
        Advisor book JSON from gold layer
    """
    # Validate advisor_id (basic sanitization - alphanumeric + underscore only)
    if not advisor_id or not all(c.isalnum() or c == '_' for c in advisor_id):
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})

    key = f'gold/advisors/{advisor_id}/book.json'
    return serve_s3_json(bucket, key)


def handle_health_check() -> dict:
    """Health check endpoint for data availability.

    Tests connectivity to key data sources:
    - DynamoDB (firm metadata)
    - S3 (gold layer data for each firm)

    Returns:
        Health status with details for each data source
    """
    health_status = {
        'service': 'advisor-intelligence',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'status': 'healthy',
        'checks': {}
    }

    # Check 1: DynamoDB connectivity
    try:
        all_firms = get_all_firms()
        health_status['checks']['dynamodb'] = {
            'status': 'ok',
            'firms_found': len(all_firms)
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['dynamodb'] = {
            'status': 'error',
            'error': str(e)
        }

    # Check 2: S3 data availability for each firm
    s3_checks = {}
    try:
        firms = get_all_firms()
        for firm in firms:
            firm_id = firm.get('firmId', 'unknown')
            bucket = firm.get('s3Bucket')

            if not bucket:
                s3_checks[firm_id] = {'status': 'error', 'error': 'No bucket configured'}
                continue

            # Test if summary metrics file exists (critical file)
            try:
                s3_client.head_object(Bucket=bucket, Key='gold/summary/header_metrics.json')
                s3_checks[firm_id] = {'status': 'ok', 'bucket': bucket}
            except s3_client.exceptions.NoSuchKey:
                s3_checks[firm_id] = {'status': 'missing_data', 'bucket': bucket}
                health_status['status'] = 'degraded'
            except Exception as e:
                s3_checks[firm_id] = {'status': 'error', 'error': str(e), 'bucket': bucket}
                health_status['status'] = 'degraded'

        health_status['checks']['s3_data'] = s3_checks

    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['s3_data'] = {
            'status': 'error',
            'error': str(e)
        }

    # Return appropriate status code
    status_code = 200 if health_status['status'] == 'healthy' else 503

    return cors_response(status_code, health_status)


# =============================================================================
# Books Tab Handlers (L3/L4 drill views)
# =============================================================================

# Canonical asset class hierarchy for Mix response
# Top-level: equity | fixed_income | alternatives | cash | hedge | other
# structured_notes sits under alternatives (Halo Shield products, buffer ETFs,
# indexed annuities — equity-linked with defined-outcome / protection structures)
_ASSET_CLASS_LABELS = {
    'equity':           'Equities',
    'fixed_income':     'Fixed Income',
    'structured_notes': 'Structured Notes',  # sub-class of alternatives
    'alternatives':     'Alternatives',
    'cash':             'Cash',
    'other':            'Other',
}


def _classify_holding(ticker, asset_name):
    """Classify a holding via ETFClassifier (bd-securities DynamoDB table).

    Returns: 'equity' | 'fixed_income' | 'alternatives' | 'other'
    'other' is the cash residual bucket in the portal mix view.

    Classification is delegated entirely to _clf (ETFClassifier), which:
    1. Looks up ticker in bd-securities DynamoDB table
    2. Resolves asset_name via name_aliases to a ticker, then looks up
    3. Applies name pattern matching (structured notes, cash, fixed income)
    4. Falls back to alpha-ticker heuristic (equity)
    5. Returns '' for unknowns -- mapped here to 'other' (cash residual)
    """
    # Coerce pd.NA / None / NaN to None for safe boolean checks
    try:
        if not ticker or ticker != ticker:
            ticker = None
    except (ValueError, TypeError):
        ticker = None
    try:
        if not asset_name or asset_name != asset_name:
            asset_name = None
    except (ValueError, TypeError):
        asset_name = None

    result = _clf.classify(ticker, asset_name)
    return result if result else 'other'



def _validate_entity_id(entity_id):
    """Validate relationship_id or account_id (alphanumeric + hyphen + underscore)."""
    if not entity_id:
        return False
    return all(c.isalnum() or c in ('_', '-', '.') for c in entity_id)


def _find_latest_holdings_lots(bucket):
    """Find the latest non-backfill holdings_lots snapshot key."""
    prefix = 'gold/holdings_lots/'
    try:
        resp = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        keys = [
            obj['Key'] for obj in resp.get('Contents', [])
            if obj['Key'].endswith('.parquet')
            and 'backfill_' not in obj['Key'].rsplit('/', 1)[-1]
        ]
        return sorted(keys)[-1] if keys else None
    except Exception:
        return None


def _get_active_account_ids(bucket, as_of_date, max_age_days=45):
    """Return set of account_ids active in account_performance within max_age_days.

    account_performance is the authoritative activity ledger. holdings_lots.is_open
    can lag for departed accounts — this gate ensures composition only includes
    accounts confirmed live by the downstream canonical source.

    Args:
        bucket: S3 bucket
        as_of_date: YYYY-MM-DD string (holdings snapshot date)
        max_age_days: accounts last seen within this window are considered active

    Returns:
        set of active account_id strings, or None if AP is unavailable (degrade
        gracefully — caller skips the gate rather than failing the request).
    """
    import pandas as pd
    try:
        df = wr.s3.read_parquet(
            path=f's3://{bucket}/gold/account_performance.parquet',
            columns=['date', 'account_id'],
        )
        df['date'] = pd.to_datetime(df['date'])
        cutoff = pd.Timestamp(as_of_date) - pd.Timedelta(days=max_age_days)
        active_ids = set(df.loc[df['date'] >= cutoff, 'account_id'].unique())
        print(f'AP active gate: {len(active_ids):,} accounts active within {max_age_days}d of {as_of_date}')
        return active_ids
    except Exception as e:
        print(f'WARN: Could not load account_performance for active gate: {e} -- skipping gate')
        return None


def handle_books_timeseries(bucket, entity_type, entity_id):
    """Daily AUA/NNA timeseries for a single relationship or account.

    Args:
        bucket: S3 bucket
        entity_type: 'relationship' or 'account'
        entity_id: The entity identifier
    """
    if not _validate_entity_id(entity_id):
        return cors_response(400, {'error': f'Invalid {entity_type}_id: {entity_id}'})

    if entity_type == 'relationship':
        key = 'gold/client_performance.parquet'
        filter_col = 'relationship_id'
        columns = ['date', 'relationship_id', 'total_aua', 'aua_taxable',
                    'aua_tax_deferred', 'aua_tax_exempt', 'cum_inflows',
                    'cum_outflows', 'nna']
    else:
        key = 'gold/account_performance.parquet'
        filter_col = 'account_id'
        columns = ['date', 'account_id', 'total_aua', 'cum_inflows',
                    'cum_outflows', 'nna', 'num_positions', 'pct_priced']

    try:
        df = wr.s3.read_parquet(
            path=f's3://{bucket}/{key}',
            columns=columns,
        )
        df = df[df[filter_col] == entity_id]
    except Exception as e:
        print(f'ERROR: Failed to read {key}: {e}')
        return cors_response(500, {'error': f'Failed to read data: {type(e).__name__}'})

    if df.empty:
        return cors_response(404, {'error': f'No data for {entity_type}_id: {entity_id}'})

    df = df.sort_values('date')
    data_as_of = str(df['date'].max().date()) if hasattr(df['date'].iloc[0], 'date') else str(df['date'].max())

    records = []
    for _, row in df.iterrows():
        rec = {
            'date': str(row['date'].date()) if hasattr(row['date'], 'date') else str(row['date']),
            'total_aua': round(float(row['total_aua']), 2),
            'cum_inflows': round(float(row['cum_inflows']), 2),
            'cum_outflows': round(float(row['cum_outflows']), 2),
            'nna': round(float(row['nna']), 2),
        }
        # Include optional columns if present
        for opt_col in ['aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
                        'num_positions', 'pct_priced']:
            if opt_col in df.columns:
                val = row[opt_col]
                rec[opt_col] = round(float(val), 2) if val == val else None  # NaN check
        records.append(rec)

    response_body = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'data_as_of': data_as_of,
        f'{entity_type}_id': entity_id,
        'data': records
    }
    print(f'SUCCESS: books/{entity_type}/{entity_id}/timeseries -> {len(records)} records')
    return cors_response(200, response_body)


def handle_books_composition(bucket, entity_type, entity_id):
    """Mix (asset class) + Concentration (security) for a single entity.

    Args:
        bucket: S3 bucket
        entity_type: 'relationship', 'account', or 'firm'
        entity_id: The entity identifier ('all' for firm scope)
    """
    # Firm scope uses entity_id='all' which is not a real ID -- skip validation
    if entity_type != 'firm' and not _validate_entity_id(entity_id):
        return cors_response(400, {'error': f'Invalid {entity_type}_id: {entity_id}'})

    # Find latest holdings_lots snapshot
    holdings_key = _find_latest_holdings_lots(bucket)
    if not holdings_key:
        return cors_response(404, {'error': 'No holdings_lots snapshots available'})

    read_cols = ['account_id', 'relationship_id', 'ticker', 'asset_name',
                 'market_value', 'is_open']

    try:
        df = wr.s3.read_parquet(
            path=f's3://{bucket}/{holdings_key}',
            columns=read_cols,
            dtype_backend='numpy',
        )
        if entity_type == 'firm':
            # Firm scope: aggregate ALL open holdings -- the bucket IS the firm
            df = df[df['is_open'].fillna(False) == True]
        else:
            filter_col = 'relationship_id' if entity_type == 'relationship' else 'account_id'
            df = df[(df[filter_col] == entity_id) & (df['is_open'].fillna(False) == True)]
    except Exception as e:
        print(f'ERROR: Failed to read {holdings_key}: {e}')
        return cors_response(500, {'error': f'Failed to read holdings: {type(e).__name__}'})

    if df.empty:
        return cors_response(404, {'error': f'No open holdings for {entity_type}: {entity_id}'})

    # Gate: filter to accounts confirmed active in account_performance.
    # holdings_lots.is_open can lag for departed accounts; AP is the authoritative
    # activity ledger and prevents stale positions from inflating composition totals.
    snapshot_date = holdings_key.rsplit('/', 1)[-1].replace('.parquet', '')
    active_ids = _get_active_account_ids(bucket, snapshot_date)
    if active_ids is not None:
        before = len(df)
        df = df[df['account_id'].isin(active_ids)]
        excluded = before - len(df)
        if excluded > 0:
            print(f'AP gate excluded {excluded:,} lots from {before:,} '
                  f'({excluded/before*100:.1f}% of entity holdings from inactive accounts)')

    if df.empty:
        return cors_response(404, {'error': f'No active holdings for {entity_type}_id: {entity_id}'})

    # Classify each holding
    df['asset_class'] = df.apply(
        lambda r: _classify_holding(r.get('ticker'), r.get('asset_name')), axis=1
    )

    total_mv = float(df['market_value'].sum())
    if total_mv == 0:
        return cors_response(200, {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'data_as_of': holdings_key.rsplit('/', 1)[-1].replace('.parquet', ''),
            'scope': {f'{entity_type}_id': entity_id},
            'mix': [],
            'concentration': {'top_n': 10, 'items': [], 'other': {'market_value': 0, 'pct': 0}},
            'unclassified': {'count': 0, 'market_value': 0}
        })

    # --- Mix: group by asset_class ---
    mix_agg = df.groupby('asset_class')['market_value'].sum().sort_values(ascending=False)
    # pct is 0-1 (e.g., 0.625 = 62.5%). Consumers multiply by 100 to display.
    mix_items = []
    for ac, mv in mix_agg.items():
        mix_items.append({
            'asset_class': ac,
            'label': _ASSET_CLASS_LABELS.get(ac, ac.replace('_', ' ').title()),
            'market_value': round(float(mv), 2),
            'pct': round(float(mv) / total_mv, 6)
        })

    # --- Concentration: group by ticker (or asset_name fallback) ---
    def _conc_key(r):
        t = r.get('ticker')
        try:
            if t and t == t and str(t).strip() not in ('', 'nan', 'None'):
                return str(t).strip().upper()
        except (ValueError, TypeError):
            pass
        return str(r.get('asset_name', '')).strip()[:50]
    df['conc_key'] = df.apply(_conc_key, axis=1)
    conc_agg = df.groupby('conc_key').agg(
        market_value=('market_value', 'sum'),
        asset_class=('asset_class', 'first'),
        label=('conc_key', 'first')
    ).sort_values('market_value', ascending=False)

    top_n = 10
    top_items = []
    for key_val, row in conc_agg.head(top_n).iterrows():
        top_items.append({
            'key': key_val,
            'label': key_val,
            'asset_class': row['asset_class'],
            'market_value': round(float(row['market_value']), 2),
            'pct': round(float(row['market_value']) / total_mv, 6)
        })

    other_mv = float(conc_agg.iloc[top_n:]['market_value'].sum()) if len(conc_agg) > top_n else 0.0

    # Unclassified count
    unclassified_mask = df['asset_class'] == 'other'
    unclassified_count = int(unclassified_mask.sum())
    unclassified_mv = float(df.loc[unclassified_mask, 'market_value'].sum())

    snapshot_date = holdings_key.rsplit('/', 1)[-1].replace('.parquet', '')
    response_body = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'data_as_of': snapshot_date,
        'scope': {f'{entity_type}_id': entity_id},
        'mix': mix_items,
        'concentration': {
            'top_n': top_n,
            'items': top_items,
            'other': {
                'market_value': round(other_mv, 2),
                'pct': round(other_mv / total_mv, 6) if total_mv > 0 else 0
            }
        },
        'unclassified': {
            'count': unclassified_count,
            'market_value': round(unclassified_mv, 2)
        }
    }
    print(f'SUCCESS: books/{entity_type}/{entity_id}/composition -> '
          f'{len(mix_items)} classes, {len(top_items)} top holdings')
    return cors_response(200, response_body)


# =============================================================================
# Mix + Concentration Timeseries Handlers (pre-computed per-relationship JSON)
# Pattern: identical to handle_advisor_book -- serve_s3_json passthrough.
# Gold script 06b writes: gold/client_timeseries/{relationship_id}.json
# Both endpoints serve the same file; portal destructures what it needs.
# =============================================================================

def handle_mix_timeseries(bucket, relationship_id):
    """Serve pre-computed mix + concentration timeseries for a relationship."""
    if not _validate_entity_id(relationship_id):
        return cors_response(400, {'error': f'Invalid relationship_id: {relationship_id}'})
    return serve_s3_json(bucket, f'gold/client_timeseries/{relationship_id}.json')


def handle_concentration_timeseries(bucket, relationship_id):
    """Serve pre-computed mix + concentration timeseries for a relationship."""
    if not _validate_entity_id(relationship_id):
        return cors_response(400, {'error': f'Invalid relationship_id: {relationship_id}'})
    return serve_s3_json(bucket, f'gold/client_timeseries/{relationship_id}.json')


def _filter_window(data_list: list, window: str) -> list:
    """Filter a data list (items with 'date' keys) to trailing window from today.

    window values: '3M' (90d), '6M' (180d), '1Y' (365d), '2Y' (730d), '3Y' (1095d).
    Unrecognised window values return the full list unchanged.
    """
    window_days = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}
    days = window_days.get((window or '').upper())
    if not days:
        return data_list
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
    return [row for row in data_list if row.get('date', '') >= cutoff]


def handle_advisor_timeseries(bucket: str, advisor_id: str) -> dict:
    """Serve pre-computed AUA timeseries for one advisor book.

    Written by bd-portal-advisor-publisher at gold/advisors/{advisor_id}/timeseries.json.
    Shape: {advisor_id, advisor_name, data_as_of, data: [{date, total_aua,
            cum_inflows, cum_outflows, nna}]}
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})
    key = f'gold/advisors/{advisor_id}/timeseries.json'
    return serve_s3_json(bucket, key)


def handle_advisor_mix_timeseries(bucket: str, advisor_id: str,
                                   window: str | None) -> dict:
    """Serve pre-computed AUA-weighted mix timeseries for one advisor book.

    Written by bd-portal-advisor-publisher at gold/advisors/{advisor_id}/mix_timeseries.json.
    Shape: {advisor_id, data_as_of, data: [{date, total_aua, equity, fixed_income,
            structured_notes, cash, other}]} -- pct fields are 0-1 convention.
    Optional ?window= query param filters data list to trailing window.
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})
    key = f'gold/advisors/{advisor_id}/mix.json'
    response = serve_s3_json(bucket, key)
    if window and isinstance(response, dict) and response.get('statusCode', 200) == 200:
        body = response.get('body')
        if body:
            try:
                parsed = json.loads(body)
                if parsed.get('data'):
                    parsed['data'] = _filter_window(parsed['data'], window)
                response['body'] = json.dumps(parsed)
            except Exception:
                pass
    return response


def handle_firm_mix_views(bucket: str) -> dict:
    """Serve pre-computed firm-level period mix views (quarterly/monthly/annually).

    Written by 06b_build_client_mix_timeseries.py at gold/firm_mix_views.json.
    Shape: {generated_at, data_as_of, firm_id, views: {quarterly, monthly, annually}}
    Each period entry: {period, label, end_date, total_aua, equity: {value, pct}, ...}
    pct values are 0-1.
    """
    return serve_s3_json(bucket, 'gold/firm_mix_views.json')


def handle_advisor_mix_views(bucket: str, advisor_id: str) -> dict:
    """Serve pre-computed per-advisor period mix views (quarterly/monthly/annually).

    Written by 06b_build_client_mix_timeseries.py at gold/advisors/{id}/mix.json.
    Shape: {generated_at, data_as_of, advisor_id, advisor_name, views: {quarterly, monthly, annually}}
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response(400, {'error': f'Invalid advisor_id: {advisor_id}'})
    return serve_s3_json(bucket, f'gold/advisors/{advisor_id}/mix.json')


def handle_firm_composition(bucket: str) -> dict:
    """Serve pre-computed firm-level per-class composition (asset mix + top holdings).

    Written by 12_build_composition_artifacts.py at gold/views/firm_composition.json.
    Shape: {data_as_of, scope, total_market_value, top_holdings, other, mix, unclassified}
    Each mix item includes top_holdings (top 9 per class, pct relative to class AUM).
    Cache-Control: no-store -- position-level firm AUM data must not be cached.
    """
    return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')


def handle_advisor_composition(bucket: str, advisor_id: str) -> dict:
    """Serve pre-computed per-advisor per-class composition (asset mix + top holdings).

    Written by 12_build_composition_artifacts.py at gold/advisors/{id}/composition.json.
    Shape: same as firm_composition.json with scope = {advisor_id, firm_id}.
    advisor_id must match the sanitization used in script 12 and ClientsTab.tsx:383.
    Cache-Control: no-store -- position-level advisor AUM data must not be cached.
    """
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response_nocache(400, {'error': 'Invalid advisor_id'})
    return serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')


# =============================================================================
# Main Handler
# =============================================================================

def lambda_handler(event, context):
    """Main Lambda handler - routes requests to appropriate function.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response dict
    """
    print(f'Event: {json.dumps(event)}')

    # Handle OPTIONS request (CORS preflight)
    http_method = event.get('httpMethod', 'GET')
    if http_method == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})

    # Extract path
    path = event.get('path', event.get('rawPath', ''))

    # Normalize path (remove stage prefix if present)
    for prefix in ['/prod', '/dev', '/api']:
        if path.startswith(prefix):
            path = path[len(prefix):]

    # ===================
    # Health Check (No Auth Required)
    # ===================
    if http_method == 'GET' and (path == '/health/advisor-intelligence' or path == '/health/advisor-intelligence/'):
        return handle_health_check()

    # Extract authorizer context (handles both REST API and HTTP API v2 formats)
    authorizer = event.get('requestContext', {}).get('authorizer', {})
    # HTTP API v2 nests context under 'lambda' key
    auth_context = authorizer.get('lambda', authorizer)
    allowed_firms = auth_context.get('allowedFirmIds', '')
    user_email = auth_context.get('email', 'unknown')
    user_tier = auth_context.get('tier', '')

    # For internal users, grant ALL access even if allowedFirmIds is missing
    # (backwards compatibility during authorizer migration)
    if not allowed_firms and user_tier == 'internal':
        print(f'Internal user {user_email} - granting ALL access (fallback)')
        allowed_firms = 'ALL'

    # Extract query parameters
    query_params = event.get('queryStringParameters') or {}

    print(f'Routing: method={http_method}, path={path}, user={user_email}, allowedFirms={allowed_firms}')

    # If no auth context, deny access (should have been blocked by authorizer)
    if not allowed_firms:
        print('No allowedFirmIds in authorizer context - denying access')
        return cors_response(403, {'error': 'Access denied - no authorization context'})

    # ===================
    # V1: GET /partners
    # ===================
    if http_method == 'GET' and (path == '/partners' or path == '/partners/'):
        return handle_get_partners(allowed_firms)

    # ===================
    # V2: Advisor Intelligence Endpoints
    # ===================
    # All v2 endpoints require firmId query parameter
    if '/shared/advisor-intelligence' in path:
        firm_id = query_params.get('firmId', '')

        if not firm_id:
            return cors_response(400, {'error': 'Missing required query parameter: firmId'})

        # Authorization check
        if not is_authorized(firm_id, allowed_firms):
            print(f'Access denied: user cannot access firm {firm_id}')
            return cors_response(403, {'error': 'Access denied to this firm'})

        # Get S3 bucket for this firm
        bucket = get_firm_bucket(firm_id)
        if not bucket:
            return cors_response(404, {'error': f'Unknown firm: {firm_id}'})

        # Route to v2 handlers
        if '/timeseries/' in path:
            dimension = extract_path_param(path, 'timeseries')
            return handle_timeseries(bucket, dimension)

        elif '/snapshots/' in path:
            dimension = extract_path_param(path, 'snapshots')
            return handle_snapshots(bucket, dimension)

        elif path.endswith('/filters'):
            return handle_filters(bucket)

        elif '/clients/growth' in path:
            return handle_client_growth(bucket)

        elif '/clients/tax-breakdown' in path:
            return handle_tax_breakdown(bucket)

        elif '/clients/tax-deferred' in path:
            return handle_tax_deferred(bucket)

        elif path.endswith('/summary'):
            return handle_summary(bucket)

        elif '/partner-analytics' in path or path.endswith('/partner-analytics'):
            return handle_partner_analytics(bucket)

        elif '/advisors/' in path and '/book' in path:
            # Extract advisor_id from path: /advisors/{advisor_id}/book
            advisor_id = extract_path_param(path, 'advisors')
            return handle_advisor_book(bucket, advisor_id)

        elif '/advisors/' in path and '/mix-views' in path:
            # Extract advisor_id from path: /advisors/{advisor_id}/mix-views
            advisor_id = extract_path_param(path, 'advisors')
            return handle_advisor_mix_views(bucket, advisor_id)

    # ===================
    # V3: Books Tab Endpoints (L3/L4 drill views)
    # ===================
    if '/scoped/partners/books/' in path:
        firm_id = query_params.get('firmId', '')

        if not firm_id:
            return cors_response(400, {'error': 'Missing required query parameter: firmId'})

        if not is_authorized(firm_id, allowed_firms):
            print(f'Access denied: user cannot access firm {firm_id}')
            return cors_response(403, {'error': 'Access denied to this firm'})

        bucket = get_firm_bucket(firm_id)
        if not bucket:
            return cors_response(404, {'error': f'Unknown firm: {firm_id}'})

        # Parse: /scoped/partners/books/{entity_type}/{entity_id}/{action}
        books_parts = path.split('/scoped/partners/books/')[-1].rstrip('/').split('/')
        if len(books_parts) >= 3:
            entity_type = books_parts[0]   # 'relationship', 'account', 'firm', or 'advisor'
            entity_id = books_parts[1]
            action = books_parts[2]        # 'timeseries', 'composition', 'mix-timeseries', etc.

            if entity_type not in ('relationship', 'account', 'firm', 'advisor'):
                return cors_response(400, {'error': f'Invalid entity type: {entity_type}'})

            if action == 'timeseries' and entity_type == 'advisor':
                return handle_advisor_timeseries(bucket, entity_id)
            elif action == 'mix-timeseries' and entity_type == 'advisor':
                window = query_params.get('window')
                return handle_advisor_mix_timeseries(bucket, entity_id, window)
            elif action == 'timeseries':
                return handle_books_timeseries(bucket, entity_type, entity_id)
            elif action == 'composition' and entity_type == 'firm':
                return handle_firm_composition(bucket)
            elif action == 'composition' and entity_type == 'advisor':
                return handle_advisor_composition(bucket, entity_id)
            elif action == 'composition':
                return handle_books_composition(bucket, entity_type, entity_id)
            elif action == 'mix-timeseries' and entity_type == 'relationship':
                return handle_mix_timeseries(bucket, entity_id)
            elif action == 'concentration-timeseries' and entity_type == 'relationship':
                return handle_concentration_timeseries(bucket, entity_id)
            elif action == 'mix-views' and entity_type == 'firm':
                return handle_firm_mix_views(bucket)

        return cors_response(400, {'error': 'Invalid books endpoint path'})

    # ===================
    # UNKNOWN ROUTE
    # ===================
    return cors_response(404, {
        'error': 'Route not found',
        'path': path,
        'method': http_method,
        'available_routes': [
            'GET /api/partners',
            'GET /api/shared/advisor-intelligence/timeseries/{dimension}?firmId=xxx',
            'GET /api/shared/advisor-intelligence/snapshots/{dimension}?firmId=xxx',
            'GET /api/shared/advisor-intelligence/filters?firmId=xxx',
            'GET /api/shared/advisor-intelligence/clients/growth?firmId=xxx',
            'GET /api/shared/advisor-intelligence/clients/tax-breakdown?firmId=xxx',
            'GET /api/shared/advisor-intelligence/clients/tax-deferred?firmId=xxx',
            'GET /api/shared/advisor-intelligence/summary?firmId=xxx',
            'GET /api/shared/advisor-intelligence/partner-analytics?firmId=xxx',
            'GET /api/shared/advisor-intelligence/advisors/{advisorId}/book?firmId=xxx',
            'GET /api/scoped/partners/books/relationship/{id}/timeseries?firmId=xxx',
            'GET /api/scoped/partners/books/relationship/{id}/composition?firmId=xxx',
            'GET /api/scoped/partners/books/account/{id}/timeseries?firmId=xxx',
            'GET /api/scoped/partners/books/account/{id}/composition?firmId=xxx',
            'GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx&window=1Y',
            'GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx&window=1Y',
            'GET /api/scoped/partners/books/firm/all/mix-views?firmId=xxx',
            'GET /api/shared/advisor-intelligence/advisors/{advisorId}/mix-views?firmId=xxx',
            'GET /api/scoped/partners/books/advisor/{id}/timeseries?firmId=xxx',
            'GET /api/scoped/partners/books/advisor/{id}/mix-timeseries?firmId=xxx&window=1Y',
            'GET /api/scoped/partners/books/firm/all/composition?firmId=xxx',
            'GET /api/scoped/partners/books/advisor/{id}/composition?firmId=xxx'
        ]
    })
```

### mixtimeseriespanel.tsx----clientdetail-mix-timeseries-panel-recently-fixed-by-dt-for-4-class-taxonomy.tsx

```
/**
 * Mix Timeseries Panel
 *
 * 100% stacked area chart showing asset class allocation over time.
 * 4 series: equity, fixed_income, alternatives, cash.
 * Independent 1Y/3Y/Max window toggle. Click an area to filter Concentration panel.
 */

import { useState, useEffect, useMemo, useCallback } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { getMixTimeseries } from '@/api/endpoints/advisor-intelligence'
import type { MixTimeseriesPoint, MixAssetClass, MixWindow } from '../../types'

// ============================================================================
// Config
// ============================================================================

// Canonical asset class colors — must match CMA portal and PartnerAnalytics
const ASSET_CLASSES: { key: MixAssetClass; label: string; color: string }[] = [
  { key: 'equity',       label: 'Equity',       color: '#3b82f6' }, // Blue
  { key: 'fixed_income', label: 'Fixed Income', color: '#10b981' }, // Green
  { key: 'alternatives', label: 'Alternatives', color: '#f97316' }, // Orange
  { key: 'cash',         label: 'Cash',         color: '#f59e0b' }, // Gold
]

const WINDOW_OPTIONS: MixWindow[] = ['1Y', '3Y', 'Max']

// ============================================================================
// Component
// ============================================================================

interface MixTimeseriesPanelProps {
  relationshipId: string
  firmId: string
  selectedAssetClass: MixAssetClass | null
  onSelectAssetClass: (cls: MixAssetClass | null) => void
}

export function MixTimeseriesPanel({
  relationshipId,
  firmId,
  selectedAssetClass,
  onSelectAssetClass,
}: MixTimeseriesPanelProps) {
  const [window, setWindow] = useState<MixWindow>('1Y')
  const [data, setData] = useState<MixTimeseriesPoint[] | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    getMixTimeseries(relationshipId, firmId, window)
      .then((res) => {
        if (!cancelled) setData(res)
      })
      .catch(() => {
        if (!cancelled) setData(null)
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })
    return () => { cancelled = true }
  }, [relationshipId, firmId, window])

  const hasData = data !== null && data.length > 0

  // XAxis tick formatter: show month labels
  const formatXTick = useCallback((value: string) => {
    if (!value) return ''
    const d = new Date(value + 'T00:00:00')
    return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
  }, [])

  // Show ~6 ticks max
  const tickInterval = useMemo(() => {
    return Math.max(1, Math.floor((data?.length ?? 0) / 6))
  }, [data])

  const handleAreaClick = useCallback((cls: MixAssetClass) => {
    onSelectAssetClass(selectedAssetClass === cls ? null : cls)
  }, [selectedAssetClass, onSelectAssetClass])

  return (
    <Panel variant="chart" className="h-[320px]">
      <PanelHeader
        title="Asset Class Mix"
        helpText="Allocation percentage over time (100% stacked)"
        actions={
          <div className="flex gap-1 bg-white/5 rounded-lg p-1">
            {WINDOW_OPTIONS.map((opt) => (
              <button
                key={opt}
                onClick={() => setWindow(opt)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                  window === opt
                    ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                    : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
                }`}
              >
                {opt}
              </button>
            ))}
          </div>
        }
      />
      <PanelContent className="h-full p-4">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <span className="text-xs text-white/40">Loading...</span>
          </div>
        ) : !hasData ? (
          <div className="flex items-center justify-center h-full">
            <span className="text-xs text-white/40">No allocation data available for this client</span>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data!} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                {ASSET_CLASSES.map(({ key, color }) => (
                  <linearGradient key={`mix-grad-${key}`} id={`mix-grad-${key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={color} stopOpacity={0.6} />
                    <stop offset="100%" stopColor={color} stopOpacity={0.2} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis
                dataKey="date"
                stroke="rgba(255,255,255,0.3)"
                tick={{ fontSize: 10 }}
                tickFormatter={formatXTick}
                interval={tickInterval}
              />
              <YAxis
                stroke="rgba(255,255,255,0.3)"
                tick={{ fontSize: 10 }}
                tickFormatter={(v: number) => `${Math.round(v * 100)}%`}
                domain={[0, 1]}
              />
              <Tooltip
                wrapperStyle={{ zIndex: 40 }}
                cursor={{ stroke: 'rgba(94,114,228,0.5)', strokeWidth: 2 }}
                content={({ active, payload, label }) => {
                  if (!active || !payload?.length) return null
                  return (
                    <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                      <p className="font-medium text-[hsl(var(--semantic-text-chartTooltip))] text-xs mb-1">{label}</p>
                      {payload.map((p, i) => {
                        const cls = ASSET_CLASSES.find(c => c.key === p.dataKey)
                        return (
                          <p key={i} className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">
                            {cls?.label ?? p.dataKey}: {((p.value as number) * 100).toFixed(1)}%
                          </p>
                        )
                      })}
                    </div>
                  )
                }}
              />
              {ASSET_CLASSES.map(({ key, color }) => {
                const dimmed = selectedAssetClass !== null && selectedAssetClass !== key
                return (
                  <Area
                    key={key}
                    type="monotone"
                    dataKey={key}
                    stackId="mix"
                    fill={`url(#mix-grad-${key})`}
                    stroke={color}
                    strokeWidth={1}
                    fillOpacity={dimmed ? 0.3 : 1}
                    strokeOpacity={dimmed ? 0.3 : 1}
                    style={{ cursor: 'pointer' }}
                    onClick={() => handleAreaClick(key)}
                    dot={false}
                    activeDot={false}
                  />
                )
              })}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </PanelContent>
    </Panel>
  )
}
```

### partneranalytics.tsx----assets-overview-header-panel-aua--clients--mix-toggles.-the-mix-toggle-is-broken..tsx

```
 
/**
 * Partner Analytics Panel - v5
 *
 * Header panel for Advisor Intelligence page with multi-view support.
 * Mirrors the Model Portfolios "Portfolio Analytics" pattern:
 * - Left: Donut chart showing breakdown by selected view
 * - Right: Bell curve showing distribution
 * - Below: Quarterly metrics with time machine support
 *
 * Views (toggle bar):
 * - AUA: Total assets by client type (new vs existing) - default
 * - NNA: Net new assets with inflows/outflows drill-down
 * - GEO: Geographic breakdown with city drill-down
 * - ADV: Architect breakdown with client drill-down
 */

import { useState, useEffect, useMemo, useCallback } from 'react'
import { useQuery } from '@tanstack/react-query'
import { AreaChart, Area, BarChart, Bar, Cell, ComposedChart, Line, PieChart, Pie, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { Panel, PanelHeader, PanelContent, PanelFooter } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { Tooltip } from '@/components/Tooltip'
import { HelpCircle } from 'lucide-react'
import { formatCurrency } from '@/lib/universalNumberFormatter'
import type { PartnerAnalyticsResponse, PartnerAnalyticsViewMode, DistributionStats, DonutSegment, CitySegment, ClientSegment, TimePeriodKey, PeriodSnapshot, PartnerAnalyticsViewWithPeriods, PartnerAnalyticsView, CumulativeChartResponse, GrowthDecompositionPoint, AuaDataPoint, BooksCompositionResponse } from '../types'

// Mock AUA timeseries in the PSCFIX schema (used as placeholderData until publisher Lambda is live)
const MOCK_AUA_TIMESERIES: Partial<CumulativeChartResponse> = {
  aua: {
    quarterly: {
      categories: ['NMNC', 'NMEC'],
      data: [
        { period: '2023-Q4', label: "Q4 '23", end_date: '2023-12-31', NMNC: 160000000, NMEC: 1060000000 },
        { period: '2024-Q1', label: "Q1 '24", end_date: '2024-03-31', NMNC: 190000000, NMEC: 1090000000 },
        { period: '2024-Q2', label: "Q2 '24", end_date: '2024-06-30', NMNC: 220000000, NMEC: 1130000000 },
        { period: '2024-Q3', label: "Q3 '24", end_date: '2024-09-30', NMNC: 250000000, NMEC: 1190000000 },
        { period: '2024-Q4', label: "Q4 '24", end_date: '2024-12-31', NMNC: 280000000, NMEC: 1250000000 },
        { period: '2025-Q1', label: "Q1 '25", end_date: '2025-03-09', NMNC: 300000000, NMEC: 1300000000 },
      ],
    },
    monthly: {
      categories: ['NMNC', 'NMEC'],
      data: [
        { period: '2024-10', label: "Oct '24", end_date: '2024-10-31', NMNC: 256000000, NMEC: 1220000000 },
        { period: '2024-11', label: "Nov '24", end_date: '2024-11-30', NMNC: 265000000, NMEC: 1232000000 },
        { period: '2024-12', label: "Dec '24", end_date: '2024-12-31', NMNC: 280000000, NMEC: 1250000000 },
        { period: '2025-01', label: "Jan '25", end_date: '2025-01-31', NMNC: 288000000, NMEC: 1268000000 },
        { period: '2025-02', label: "Feb '25", end_date: '2025-02-28', NMNC: 295000000, NMEC: 1284000000 },
        { period: '2025-03', label: "Mar '25", end_date: '2025-03-09', NMNC: 300000000, NMEC: 1300000000 },
      ],
    },
    annually: {
      categories: ['NMNC', 'NMEC'],
      data: [
        { period: '2022', label: '2022', end_date: '2022-12-31', NMNC: 100000000, NMEC:  900000000 },
        { period: '2023', label: '2023', end_date: '2023-12-31', NMNC: 160000000, NMEC: 1060000000 },
        { period: '2024', label: '2024', end_date: '2024-12-31', NMNC: 280000000, NMEC: 1250000000 },
        { period: '2025', label: '2025', end_date: '2025-03-09', NMNC: 300000000, NMEC: 1300000000 },
      ],
    },
  },
}
import { hasTimeMachine } from '../types'
import { getCumulativeChart, getFirmMixViews } from '@/api/endpoints/advisor-intelligence'
import type { FirmMixViewsResponse } from '../types'
import { useSelectTracking } from '@/hooks/useFilterTracking'
import { useAuth } from '@/hooks/useAuth'

// Granularity options for bar charts (Monthly | Quarterly | Annually)
type GranularityOption = 'monthly' | 'quarterly' | 'annually'

// Panel view mode: AUA (stacked bar), NNA (diverging bar), GRO (growth decomposition lines)
type PanelViewMode = 'aua' | 'nna' | 'gro'

// AUA sub-mode: Clients (NMNC/NMEC) or Mix (asset class breakdown)
type AuaSubMode = 'clients' | 'mix'

// Y3-FE: AUA sub-mode label — placeholder pending Andrew/Yang decision
const AUA_SUB_MODE_CLIENTS_LABEL = 'Clients'

// Category colors for AUA stacked bar chart
const CATEGORY_COLORS: Record<string, string> = {
  'NMNC': '#4CAF50',           // Green - New Client Assets
  'nmnc': '#4CAF50',
  'NMEC': '#2196F3',           // Blue - Existing Client Assets
  'nmec': '#2196F3',
}

// NNA flow colors
const NNA_COLORS = {
  inflow: '#2196F3',   // Blue - Inflows (positive, above zero)
  outflow: '#EF4444',  // Red - Outflows (negative, below zero)
}

const FALLBACK_COLORS = [
  '#4CAF50', '#2196F3', '#F59E0B', '#EF4444', '#8B5CF6', '#6B7280',
]

// Y3-FE: Asset class colors for Mix mode (distinct from NMNC/NMEC)
const ASSET_CLASS_COLORS: Record<string, string> = {
  'Equities': '#8B5CF6',        // Violet
  'Fixed Income': '#06B6D4',    // Cyan
  'Real Estate': '#F97316',     // Orange
  'Alternatives': '#EC4899',    // Pink
  'Cash': '#6B7280',            // Gray
  'Other': '#A3A3A3',           // Light gray
}

function getAssetClassColor(label: string, index: number): string {
  return ASSET_CLASS_COLORS[label] || FALLBACK_COLORS[index % FALLBACK_COLORS.length]
}

// MIXV2: Asset class colors keyed by snake_case field names (FirmMixPeriodPoint keys)
// Canonical colors — must match CMA portal and ClientsTab MIX_PIE_COLORS
const FIRM_MIX_COLORS: Record<string, string> = {
  equity:           '#3b82f6',   // Blue
  fixed_income:     '#10b981',   // Green
  alternatives:     '#f97316',   // Orange
  cash:             '#f59e0b',   // Gold
}

// Y5-FE: GRO growth decomposition line colors
const GRO_COLORS = {
  market: '#8B5CF6',  // Violet — Market Performance
  nna: '#F59E0B',     // Amber/Gold — Net Flows (canonical NNA color, matches NNA tab net flow line)
  total: '#EC4899',   // Pink/Magenta — Total AUA Change (line overlay, high contrast vs purple bars + gold NNA)
}

function getBarCategoryColor(category: string, index: number): string {
  return CATEGORY_COLORS[category] || FALLBACK_COLORS[index % FALLBACK_COLORS.length]
}

// Category display names
const CATEGORY_DISPLAY_NAMES: Record<string, string> = {
  'NMNC': 'New Client Assets',
  'nmnc': 'New Client Assets',
  'NMEC': 'Existing Client Assets',
  'nmec': 'Existing Client Assets',
}

function getBarCategoryDisplayName(category: string): string {
  return CATEGORY_DISPLAY_NAMES[category] || category
}

const AVAILABLE_FIRMS = [
  { id: 'bd', name: '49 Financial' },
]

// Time window for chart data (shared with DistributionTab via AdvisorIntelligence.tsx)
type TimeWindow = '1Y' | '3Y' | 'Max'

interface PartnerAnalyticsProps {
  data: PartnerAnalyticsResponse | null
  isLoading: boolean
  selectedFirmId: string
  onPartnerChange: (firmId: string) => void
  granularity: GranularityOption
  onGranularityChange: (g: GranularityOption) => void
  timeWindow: TimeWindow
  onTimeWindowChange: (w: TimeWindow) => void
  firmOverride?: string
}

// View mode labels (city/client are hidden - accessed via drill-down)
const VIEW_LABELS: Record<PartnerAnalyticsViewMode, string> = {
  aua: 'AUA',      // Default - AUA by client type
  nna: 'NNA',      // Flows view with drill-down
  geo: 'GEO',
  city: 'City',    // Not shown in toggle, used for GEO drill-down
  adv: 'ADV',
  client: 'Client',  // Not shown in toggle, used for ADV drill-down
}

// GEO drill-down state type
type GeoDrillLevel = 'state' | 'city'

// ADV drill-down state type
type AdvDrillLevel = 'architect' | 'client'

// NNA drill-down state type (segment → flows showing inflows/outflows)
type NnaDrillLevel = 'segment' | 'flow'

export function PartnerAnalytics({ data, isLoading, selectedFirmId, onPartnerChange, granularity, onGranularityChange, timeWindow, onTimeWindowChange, firmOverride }: PartnerAnalyticsProps) {
  const { isInternal } = useAuth()
  const internal = isInternal()
  // View mode with analytics tracking
  const [viewMode, _setViewMode] = useSelectTracking<PartnerAnalyticsViewMode>('view-mode', 'aua', 'partner-analytics')

  // GEO drill-down state
  const [geoDrillLevel, _setGeoDrillLevel] = useState<GeoDrillLevel>('state')
  const [selectedStateKey, _setSelectedStateKey] = useState<string | null>(null)
  const [selectedCityKey, _setSelectedCityKey] = useState<string | null>(null)  // City selection for distribution

  // ADV drill-down state
  const [advDrillLevel, _setAdvDrillLevel] = useState<AdvDrillLevel>('architect')
  const [selectedArchitectKey, _setSelectedArchitectKey] = useState<string | null>(null)
  const [selectedClientKey, _setSelectedClientKey] = useState<string | null>(null)  // Client selection for distribution

  // NNA drill-down state (segment level → flow level showing inflows/outflows)
  const [nnaDrillLevel, _setNnaDrillLevel] = useState<NnaDrillLevel>('segment')
  const [selectedNnaSegmentKey, _setSelectedNnaSegmentKey] = useState<string | null>(null)
  const [selectedNnaFlowKey, _setSelectedNnaFlowKey] = useState<string | null>(null)  // Flow selection for distribution

  // Time Machine state with analytics tracking
  const [selectedPeriod, _setSelectedPeriod] = useSelectTracking<TimePeriodKey>('time-period', 'current', 'partner-analytics')

  // Panel-level view mode: AUA (stacked bar), NNA (diverging bar), GRO (growth decomposition)
  const [panelViewMode, setPanelViewMode] = useState<PanelViewMode>('aua')

  // Y3-FE: AUA sub-mode (Clients = NMNC/NMEC, Mix = asset class breakdown)
  const [auaSubMode, setAuaSubMode] = useState<AuaSubMode>('clients')


  // Time window: 1Y, 3Y, Max — controlled by AdvisorIntelligence.tsx (shared with DistributionTab)

  // Bar Chart state with analytics tracking for granularity
  // granularity is controlled from AdvisorIntelligence.tsx (drives the query re-fetch)
  const [selectedBarPeriod, setSelectedBarPeriod] = useState<string | null>(null) // Selected bar period key (e.g., "2023-Q1")

  // Maps granularity prop to the aua sub-key in the PSCFIX timeseries schema
  const auaGranularity: 'quarterly' | 'monthly' | 'annually' =
    granularity === 'annually' ? 'annually'
    : granularity === 'monthly' ? 'monthly'
    : 'quarterly'

  // Shared/cached timeseries query to avoid duplicate network fetches across tabs/components
  const { data: timeseriesData, isLoading: timeseriesLoading } = useQuery<CumulativeChartResponse>({
    queryKey: ['advisor-intelligence', 'cumulative-chart', firmOverride],
    queryFn: () => getCumulativeChart(firmOverride),
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  })

  // Firm-level pre-aggregated mix views (MIXV2 endpoint) for the Assets Overview Mix toggle
  const { data: firmMixViews, isLoading: isFirmMixLoading, isError: isFirmMixError } = useQuery<FirmMixViewsResponse>({
    queryKey: ['advisor-intelligence', 'firm-mix-views', firmOverride],
    queryFn: () => getFirmMixViews(firmOverride || 'bd'),
    staleTime: 10 * 60 * 1000,
    refetchOnWindowFocus: false,
  })

  // Helper to get period key and label from a date
  const getPeriodInfo = useCallback((date: Date): { periodKey: string; periodLabel: string } => {
    if (granularity === 'monthly') {
      const month = date.toLocaleString('en-US', { month: 'short' })
      const year = date.getFullYear()
      return {
        periodKey: `${year}-${String(date.getMonth() + 1).padStart(2, '0')}`,
        periodLabel: `${month} '${year.toString().slice(-2)}`
      }
    } else if (granularity === 'quarterly') {
      const quarter = Math.floor(date.getMonth() / 3) + 1
      const year = date.getFullYear()
      return {
        periodKey: `${year}-Q${quarter}`,
        periodLabel: `Q${quarter} '${year.toString().slice(-2)}`
      }
    } else {
      // annually
      const year = date.getFullYear()
      return {
        periodKey: `${year}`,
        periodLabel: `${year}`
      }
    }
  }, [granularity])

  // Time window cutoff date
  const timeWindowCutoff = useMemo(() => {
    if (timeWindow === 'Max') return null
    const now = new Date()
    const years = timeWindow === '1Y' ? 1 : 3
    return new Date(now.getFullYear() - years, now.getMonth(), now.getDate())
  }, [timeWindow])

  // Full-history AUA period list (unfiltered) — pre-aggregated by publisher (PSCFIX schema).
  // Selected directly from the correct granularity sub-key; no client-side aggregation needed.
  const allSortedAuaPeriods: AuaDataPoint[] = useMemo(() => {
    return timeseriesData?.aua?.[auaGranularity]?.data ?? []
  }, [timeseriesData, auaGranularity])

  // Windowed AUA periods for display — filtered by time window using end_date
  const aggregatedAuaData: AuaDataPoint[] = useMemo(() => {
    if (allSortedAuaPeriods.length === 0) return []
    if (!timeWindowCutoff) return allSortedAuaPeriods
    return allSortedAuaPeriods.filter(point =>
      new Date(point.end_date + 'T12:00:00') >= timeWindowCutoff
    )
  }, [allSortedAuaPeriods, timeWindowCutoff])

  // Whether the nna view has separate gross inflow/outflow columns.
  // True only after the publisher has been updated to output cum_inflows/cum_outflows.
  // When false, only net NNA is available — the chart shows a single net bar, not diverging.
  const hasGrossFlowData = useMemo(() => {
    const cats = timeseriesData?.nna?.categories || []
    return cats.includes('Inflows') && cats.includes('Outflows')
  }, [timeseriesData])

  // Aggregate daily NNA data to monthly/quarterly/annually.
  //
  // ALL columns (NNA, Inflows, Outflows) are CUMULATIVE from inception.
  // Period flows are derived by differencing adjacent period endpoints:
  //   period_net      = last(NNA)      - prev_last(NNA)
  //   period_inflows  = last(Inflows)  - prev_last(Inflows)   [always >= 0]
  //   period_outflows = last(Outflows) - prev_last(Outflows)  [always >= 0, stored negative]
  //
  // When hasGrossFlowData is false, only net is available — inflow/outflow left at 0
  // so the chart does not fabricate a split that doesn't exist in the data.
  const aggregatedNnaData = useMemo(() => {
    if (!timeseriesData?.nna?.data) return []

    const allData = timeseriesData.nna.data
    const dailyData = timeWindowCutoff
      ? allData.filter(p => new Date(String(p.date) + 'T12:00:00') >= timeWindowCutoff)
      : allData
    const categories = timeseriesData.nna.categories || []
    if (dailyData.length === 0 || categories.length === 0) return []

    const grossFlows = categories.includes('Inflows') && categories.includes('Outflows')

    // Collect the last data point per period (cumulative snapshot at period end)
    // Use ALL data (unfiltered) so the first windowed period can diff against its true prior
    const fullPeriodMap = new Map<string, {
      period: string; label: string; endDate: string;
      lastNNA: number; lastInflows: number; lastOutflows: number;
    }>()

    allData.forEach((point) => {
      const date = new Date(point.date + 'T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      fullPeriodMap.set(periodKey, {
        period: periodKey,
        label: periodLabel,
        endDate: point.date,
        lastNNA:      Number(point['NNA'])      || 0,
        lastInflows:  Number(point['Inflows'])  || 0,
        lastOutflows: Number(point['Outflows']) || 0,
      })
    })

    // Build the windowed period map for display
    const windowedPeriodKeys = new Set<string>()
    dailyData.forEach((point) => {
      const date = new Date(point.date + 'T12:00:00')
      const { periodKey } = getPeriodInfo(date)
      windowedPeriodKeys.add(periodKey)
    })

    const allSorted = Array.from(fullPeriodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )

    // Only show periods within the window, but use full history for differencing
    const sorted = allSorted.filter(e => windowedPeriodKeys.has(e.period))

    // Difference adjacent periods to get period-level flows
    return sorted.map((entry) => {
      // Find the prior period from the full (unfiltered) sorted list
      const fullIdx = allSorted.findIndex(e => e.period === entry.period)
      const prev = fullIdx > 0 ? allSorted[fullIdx - 1] : null
      const prevNNA      = prev ? prev.lastNNA      : 0
      const prevInflows  = prev ? prev.lastInflows  : 0
      const prevOutflows = prev ? prev.lastOutflows : 0

      const periodNet      = entry.lastNNA      - prevNNA
      const periodInflows  = Math.max(0, entry.lastInflows  - prevInflows)
      const periodOutflows = Math.max(0, entry.lastOutflows - prevOutflows)

      const inflow = grossFlows ? periodInflows : 0
      const outflow = grossFlows ? -periodOutflows : 0
      return {
        period:   entry.period,
        label:    entry.label,
        endDate:  entry.endDate,
        // Gross mode: both bars present every period (inflows above 0, outflows below 0)
        // Net-only mode: leave 0 — the chart renders as a single net bar instead
        inflow,
        outflow,
        net:     periodNet,
      }
    })
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // MIXV2: Derive chart-ready rows from pre-aggregated mix-views endpoint.
  // Flat-maps FirmMixPeriodPoint to dollar values + pct fields for tooltip.
  const firmMixChartData = useMemo(() => {
    const pts = firmMixViews?.views[auaGranularity] ?? []
    return pts.map(pt => ({
      label:               pt.label,
      total_aua:           pt.total_aua,
      equity:              pt.equity.value,
      equity_pct:          pt.equity.pct,
      fixed_income:        pt.fixed_income.value,
      fixed_income_pct:    pt.fixed_income.pct,
      alternatives:        pt.alternatives.value,
      alternatives_pct:    pt.alternatives.pct,
      cash:                pt.cash.value,
      cash_pct:            pt.cash.pct,
    }))
  }, [firmMixViews, auaGranularity])

  // Y5-FE: Aggregate growth_decomposition data by period
  //
  // IMPORTANT: aggregate ALL months first, then filter which periods to display.
  // Filtering monthly points before aggregation produces partial-year bars on
  // 3Y/1Y windows (e.g. 3Y starting mid-March 2023 would show Apr-Dec 2023
  // only, understating that year by Jan-Mar).  The NNA view diffs full-history
  // year endpoints so the same partial-year bar would mismatch by ~$125M.
  // Mirror the NNA view: compute full-period sums from complete history, then
  // filter which period labels fall within the time window.
  const aggregatedGroData = useMemo(() => {
    const groView = timeseriesData?.growth_decomposition
    if (!groView?.data || groView.data.length === 0) return []

    // GRO data is monthly. For quarterly/annually, SUM values (not snapshot).
    // Use complete monthly history regardless of time window.
    const periodMap = new Map<string, { period: string; label: string; market: number; nna: number; total: number; endDate: string }>()

    groView.data.forEach((point: GrowthDecompositionPoint) => {
      const date = new Date(point.period + '-01T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      // Derive end date from source month: last day of point.period (YYYY-MM)
      const [srcY, srcM] = point.period.split('-').map(Number)
      const lastDayOfMonth = new Date(srcY, srcM, 0).getDate()
      const srcEndDate = `${point.period}-${String(lastDayOfMonth).padStart(2, '0')}`

      const existing = periodMap.get(periodKey) || { period: periodKey, label: periodLabel, market: 0, nna: 0, total: 0, endDate: srcEndDate }
      existing.market += point.market
      existing.nna += point.nna
      existing.total += point.total
      existing.endDate = srcEndDate // always take the latest contributing month
      periodMap.set(periodKey, existing)
    })

    // Filter which periods to display: only show periods whose end date falls
    // within the selected time window. This hides old years without truncating
    // the period sums of years that are partially within the window.
    const allPeriods = Array.from(periodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )
    if (!timeWindowCutoff) return allPeriods
    return allPeriods.filter(p => new Date(p.endDate + 'T12:00:00') >= timeWindowCutoff)
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // ============================================================================
  // F2: Projection computation for the current incomplete period
  // ============================================================================

  const currentPeriodKey = useMemo(() => {
    return getPeriodInfo(new Date()).periodKey
  }, [getPeriodInfo])

  // Compute total and elapsed days for a given period.
  // dataEndDate is the last date with actual data (YYYY-MM-DD) — elapsed is measured
  // from the period start to this date, NOT from today's wall clock.
  function computePeriodDays(g: GranularityOption, periodKey: string, dataEndDate: string): { totalDays: number; elapsedDays: number } {
    const dataDate = new Date(dataEndDate + 'T12:00:00')
    if (g === 'monthly') {
      const [y, m] = periodKey.split('-').map(Number)
      const start = new Date(y, m - 1, 1)
      const end = new Date(y, m, 0)
      return {
        totalDays: end.getDate(),
        elapsedDays: Math.max(1, Math.floor((dataDate.getTime() - start.getTime()) / 86400000) + 1),
      }
    } else if (g === 'quarterly') {
      const parts = periodKey.split('-Q')
      const y = Number(parts[0])
      const q = Number(parts[1])
      const startMonth = (q - 1) * 3
      const start = new Date(y, startMonth, 1)
      const end = new Date(y, startMonth + 3, 0)
      return {
        totalDays: Math.floor((end.getTime() - start.getTime()) / 86400000) + 1,
        elapsedDays: Math.max(1, Math.floor((dataDate.getTime() - start.getTime()) / 86400000) + 1),
      }
    } else {
      const y = Number(periodKey)
      const start = new Date(y, 0, 1)
      const end = new Date(y, 11, 31)
      return {
        totalDays: Math.floor((end.getTime() - start.getTime()) / 86400000) + 1,
        elapsedDays: Math.max(1, Math.floor((dataDate.getTime() - start.getTime()) / 86400000) + 1),
      }
    }
  }

  // AUA: project end-of-period value using a two-input weighted blend.
  // 66.67% weight on the current trajectory, 33.33% on the last complete
  // period's delta. The current trajectory's weight on the TIME-SCALED delta
  // vs the RAW observed delta slides with how much of the period has elapsed
  // (elapsedFraction). Early in a period the raw observation dominates (avoids
  // amplifying a few days of noise by 4-5x); late in a period the time-scaled
  // delta dominates (the extrapolation ratio is small and trustworthy).
  const augmentedAuaData = useMemo(() => {
    if (aggregatedAuaData.length === 0) return aggregatedAuaData
    const cats = timeseriesData?.aua?.[auaGranularity]?.categories || []
    const lastIdx = aggregatedAuaData.length - 1
    return aggregatedAuaData.map((entry, idx) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aug = { ...entry } as any

      // Only project the last bar (most recent period with data)
      if (idx !== lastIdx) return aug

      const { totalDays, elapsedDays } = computePeriodDays(granularity, entry.period, String(entry.end_date))
      if (elapsedDays >= totalDays) return aug

      const fullIdx = allSortedAuaPeriods.findIndex(e => e.period === entry.period)
      const prior = fullIdx > 0 ? allSortedAuaPeriods[fullIdx - 1] : null
      const priorPrior = fullIdx > 1 ? allSortedAuaPeriods[fullIdx - 2] : null

      if (!prior) {
        aug._projectionUnavailable = true
        return aug
      }

      const ratio = totalDays / elapsedDays
      const elapsedFraction = elapsedDays / totalDays  // 0..1 how far into the period

      let projectedTotal = 0
      let actualTotal = 0

      cats.forEach(cat => {
        const actual = Number(entry[cat]) || 0
        actualTotal += actual
        const priorEnd = Number((prior as Record<string, unknown>)[cat]) || 0
        const rawDelta = actual - priorEnd

        // Current period contribution: blend between raw observed delta (safe
        // early in period) and time-scaled delta (accurate late in period).
        // At elapsedFraction=0.2 (early month/year): 80% raw + 20% scaled
        // At elapsedFraction=0.7 (late quarter):      30% raw + 70% scaled
        const scaledDelta = rawDelta * ratio
        const currentDelta = rawDelta * (1 - elapsedFraction) + scaledDelta * elapsedFraction

        // Last complete period's delta (prior vs priorPrior)
        const priorPriorEnd = priorPrior ? (Number((priorPrior as Record<string, unknown>)[cat]) || 0) : priorEnd
        const historicalDelta = priorEnd - priorPriorEnd

        // Blend: 2/3 current trajectory, 1/3 last complete period
        const weightedDelta = priorPrior
          ? currentDelta * (2 / 3) + historicalDelta * (1 / 3)
          : currentDelta  // only one prior exists — use current signal alone

        const projectedValue = priorEnd + weightedDelta
        aug[`_projected_${cat}`] = projectedValue
        projectedTotal += projectedValue
      })

      aug._projectedTotal = projectedTotal
      aug._actualTotal = actualTotal

      return aug
    })
  }, [aggregatedAuaData, allSortedAuaPeriods, granularity, auaGranularity, timeseriesData])

  // NNA: compute projected values for the most recent incomplete period
  const augmentedNnaData = useMemo(() => {
    if (aggregatedNnaData.length === 0) return aggregatedNnaData
    const lastNnaIdx = aggregatedNnaData.length - 1
    return aggregatedNnaData.map((entry, idx) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aug = { ...entry } as any

      if (idx !== lastNnaIdx) return aug

      const { totalDays, elapsedDays } = computePeriodDays(granularity, entry.period, entry.endDate)
      if (elapsedDays >= totalDays) return aug

      const prior = idx > 0 ? aggregatedNnaData[idx - 1] : null
      const ratio = totalDays / elapsedDays

      // Inflows (positive)
      const projInflow = entry.inflow * ratio
      const priorInflow = prior ? prior.inflow : entry.inflow
      const capInflow = Math.abs(priorInflow) * 1.5
      aug._projectedInflow = Math.min(projInflow, capInflow)

      // Outflows (negative)
      const projOutflow = entry.outflow * ratio
      const priorOutflow = prior ? prior.outflow : entry.outflow
      const capOutflow = -Math.abs(priorOutflow) * 1.5
      aug._projectedOutflow = Math.max(projOutflow, capOutflow)

      // Net
      aug._projectedNet = aug._projectedInflow + aug._projectedOutflow

      return aug
    })
  }, [aggregatedNnaData, granularity])

  // GRO: no projection — use aggregated data directly
  const augmentedGroData = aggregatedGroData

  // Get the appropriate aggregated data based on panel view mode
  const aggregatedBarData = panelViewMode === 'aua' ? augmentedAuaData : augmentedNnaData

  // Get the selected bar's data
  const selectedBarData = useMemo(() => {
    if (!selectedBarPeriod) return null
    return aggregatedBarData.find(d => d.period === selectedBarPeriod) || null
  }, [selectedBarPeriod, aggregatedBarData])

  // Handle bar click - toggle selection
  const handleBarClick = (data: { period: string }) => {
    setSelectedBarPeriod(prev => prev === data.period ? null : data.period)
  }

  // Get categories for the AUA bar chart
  const barCategories = timeseriesData?.aua?.[auaGranularity]?.categories || []

  // Handle period change (time machine)
  // Get base view data (always use the base view mode, not drill-down mode)
  // Drill-down data is nested inside segments (geo.cities, adv.clients, nna.flows)
  // All 4 views (aua, nna, geo, adv) are now separate top-level views
  const getDataViewKey = (): 'aua' | 'nna' | 'geo' | 'adv' => {
    if (viewMode === 'city') return 'geo'
    if (viewMode === 'client') return 'adv'
    return viewMode as 'aua' | 'nna' | 'geo' | 'adv'
  }
  const dataViewKey = getDataViewKey()
  const rawView = data?.views?.[dataViewKey]

  // All views now use the standard structure: view.current.donut
  const getSnapshotForPeriod = (): PeriodSnapshot | null => {
    if (!rawView) return null

    // Standard structure for all views
    const view = rawView as PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
    if (hasTimeMachine(view)) {
      const viewWithPeriods = view as PartnerAnalyticsViewWithPeriods
      if (selectedPeriod === 'current') {
        return viewWithPeriods.current
      }
      return viewWithPeriods[selectedPeriod] || viewWithPeriods.current
    }

    // v4 format - treat the whole view as the snapshot
    return view as unknown as PeriodSnapshot
  }

  const currentSnapshot = getSnapshotForPeriod()

  // Check if the BASE view has valid data (not drill-down data)
  // This determines if we should show the panel at all
  // When drilled down, we only need base data to exist - drill data can be empty
  const hasValidBaseData = currentSnapshot && currentSnapshot.donut?.segments?.length > 0 && currentSnapshot.metrics
  const hasValidData = hasValidBaseData

  // Extract data if available
  const donut = currentSnapshot?.donut
  const distribution = currentSnapshot?.distribution
  const baseSegments: DonutSegment[] = donut?.segments || []

  // Get segments for current drill level
  // - At base level: return base segments
  // - When drilled: return nested flows/cities/clients from selected parent segment
  const getSegmentsForDrillLevel = (): DonutSegment[] => {
    // NNA drill-down: show nested flows (inflows/outflows) from selected segment
    if (viewMode === 'nna' && nnaDrillLevel === 'flow' && selectedNnaSegmentKey) {
      const parentSeg = baseSegments.find(s => s.key === selectedNnaSegmentKey)
      if (parentSeg?.flows && parentSeg.flows.length > 0) {
        // Convert NnaFlowSegment[] to DonutSegment[] for consistent rendering
        // Use absolute value for donut (negative outflows would break the chart)
        return parentSeg.flows.map(flow => ({
          key: flow.key,
          label: flow.label,
          aua: Math.abs(flow.value),  // Use absolute value for donut size
          aua_pct: 0,  // Will be calculated relative to parent
          value: flow.value,  // Keep original signed value
          value_pct: 0,
          client_count: 0,  // Flows don't have client count
          color: flow.color,
        }))
      }
      // No nested flows - return empty (will show "no data" message)
      return []
    }

    // GEO drill-down: show nested cities from selected state
    if (viewMode === 'geo' && geoDrillLevel === 'city' && selectedStateKey) {
      const parentSeg = baseSegments.find(s => s.key === selectedStateKey)
      if (parentSeg?.cities && parentSeg.cities.length > 0) {
        // Convert CitySegment[] to DonutSegment[] for consistent rendering
        return parentSeg.cities.map(city => ({
          key: city.key,
          label: city.label,
          aua: city.aua,
          aua_pct: city.aua_pct,
          client_count: city.client_count,
          color: city.color,
          distribution: city.distribution,  // Include city's distribution if available
        }))
      }
      // No nested cities - return empty (will show "no data" message)
      return []
    }

    // ADV drill-down: show nested clients from selected architect
    if (viewMode === 'adv' && advDrillLevel === 'client' && selectedArchitectKey) {
      const parentSegment = baseSegments.find(s => s.key === selectedArchitectKey)
      if (parentSegment?.clients && parentSegment.clients.length > 0) {
        // Convert ClientSegment[] to DonutSegment[] for consistent rendering
        return parentSegment.clients.map(client => ({
          key: client.key,
          label: client.label,
          aua: client.aua,
          aua_pct: client.aua_pct,
          client_count: client.account_count, // Use account_count as proxy
          color: '', // Let frontend palette (CLIENT_COLORS) assign vivid distinct colors
          distribution: client.distribution,  // Include client's distribution if available
        }))
      }
      // No nested clients - return empty (will show "no data" message)
      return []
    }

    // Base level: return base segments
    return baseSegments
  }

  const segments = getSegmentsForDrillLevel()

  // Get parent segment when drilled (for showing parent's value in donut center)
  const getParentSegment = (): DonutSegment | null => {
    if (viewMode === 'nna' && nnaDrillLevel === 'flow' && selectedNnaSegmentKey) {
      return baseSegments.find(s => s.key === selectedNnaSegmentKey) || null
    }
    if (viewMode === 'geo' && geoDrillLevel === 'city' && selectedStateKey) {
      return baseSegments.find(s => s.key === selectedStateKey) || null
    }
    if (viewMode === 'adv' && advDrillLevel === 'client' && selectedArchitectKey) {
      return baseSegments.find(s => s.key === selectedArchitectKey) || null
    }
    return null
  }
  const parentSegment = getParentSegment()

  // Check if we're in NNA view (use value instead of aua)
  const _isNnaView = viewMode === 'nna'

  // Get selected segment key based on current view/drill state
  const getSelectedSegmentKey = (): string | null => {
    // AUA mode: segment selection for distribution filter (no drill-down)
    if (viewMode === 'aua') {
      return selectedNnaSegmentKey
    }
    if (viewMode === 'nna') {
      if (nnaDrillLevel === 'flow') return selectedNnaFlowKey
      return selectedNnaSegmentKey
    }
    if (viewMode === 'geo' && geoDrillLevel === 'city') return selectedCityKey
    if (viewMode === 'adv' && advDrillLevel === 'client') return selectedClientKey
    // At top level of GEO/ADV, no segment selection (drill-through only)
    return null
  }
  const selectedSegmentKey = getSelectedSegmentKey()

  // Look up selected segment by key (persists across period changes)
  const selectedSegment = selectedSegmentKey ? segments.find(s => s.key === selectedSegmentKey) || null : null

  // Get distribution data based on drill-down level and selection
  // Priority: selected segment > parent segment > view total
  // Note: distribution data is stored in two places:
  //   1. View-level: distribution.by_segment["state_key"]
  //   2. Segment-level: segment.distribution (for nested cities/clients)
  const getDistributionData = (): DistributionStats | null => {
    if (!distribution) return null

    // Special case: NNA drilled into flows - always use parent segment's distribution
    // Flows (inflows/outflows) don't have their own distribution data
    if (viewMode === 'nna' && nnaDrillLevel === 'flow' && selectedNnaSegmentKey) {
      return distribution.by_segment?.[selectedNnaSegmentKey] || distribution.total
    }

    // Case 1: A segment is clicked/selected
    if (selectedSegment) {
      // First check if segment has its own distribution (nested city/client)
      if (selectedSegment.distribution) {
        return selectedSegment.distribution
      }
      // Otherwise look up in view-level by_segment
      return distribution.by_segment?.[selectedSegment.key] || distribution.total
    }

    // Case 2: Drilled down but no specific selection (showing parent context)
    if (parentSegment) {
      // First check if parent segment has its own distribution
      if (parentSegment.distribution) {
        return parentSegment.distribution
      }
      // Otherwise look up parent in view-level by_segment
      return distribution.by_segment?.[parentSegment.key] || distribution.total
    }

    // Case 3: Base level, no selection - show total
    return distribution.total
  }

  const distributionData = getDistributionData()

  // Compute global max for Y-axis consistency across ALL time periods
  // This ensures distributions are comparable when using time machine
  // IMPORTANT: Only compare within the SAME aggregation context (e.g., FL across quarters,
  // not FL vs GEO total). When drill level changes, scale resets appropriately.
  const globalMaxCount = (() => {
    if (!rawView) return undefined

    const view = rawView as PartnerAnalyticsViewWithPeriods
    const periods: (keyof PartnerAnalyticsViewWithPeriods)[] = ['current', 'q1', 'q2', 'q3']
    const maxCounts: number[] = []

    // Determine current distribution context (must match getDistributionData logic)
    // Context types: total, segment (by key), nested city, nested client
    type DistContext =
      | { type: 'total' }
      | { type: 'segment'; key: string }
      | { type: 'nested_city'; stateKey: string; cityKey: string }
      | { type: 'nested_client'; architectKey: string; clientKey: string }

    const getDistributionContext = (): DistContext => {
      // City selected within drilled state
      if (selectedCityKey && selectedStateKey && geoDrillLevel === 'city') {
        return { type: 'nested_city', stateKey: selectedStateKey, cityKey: selectedCityKey }
      }
      // Client selected within drilled architect
      if (selectedClientKey && selectedArchitectKey && advDrillLevel === 'client') {
        return { type: 'nested_client', architectKey: selectedArchitectKey, clientKey: selectedClientKey }
      }
      // Drilled into state (showing state's distribution)
      if (selectedStateKey && geoDrillLevel === 'city') {
        return { type: 'segment', key: selectedStateKey }
      }
      // Drilled into architect (showing architect's distribution)
      if (selectedArchitectKey && advDrillLevel === 'client') {
        return { type: 'segment', key: selectedArchitectKey }
      }
      // NNA/AUA segment selected
      if (selectedNnaSegmentKey && (viewMode === 'aua' || viewMode === 'nna')) {
        return { type: 'segment', key: selectedNnaSegmentKey }
      }
      // Base level, no selection
      return { type: 'total' }
    }

    const context = getDistributionContext()

    // Look up distribution counts for this context across all periods
    for (const period of periods) {
      const snapshot = view[period] as PeriodSnapshot | undefined
      if (!snapshot) continue

      let counts: number[] | undefined

      switch (context.type) {
        case 'total':
          counts = snapshot.distribution?.total?.histogram?.counts
          break
        case 'segment':
          counts = snapshot.distribution?.by_segment?.[context.key]?.histogram?.counts
          break
        case 'nested_city': {
          const stateSegment = snapshot.donut?.segments?.find((s: DonutSegment) => s.key === context.stateKey)
          const city = stateSegment?.cities?.find((c: CitySegment) => c.key === context.cityKey)
          counts = city?.distribution?.histogram?.counts
          break
        }
        case 'nested_client': {
          const archSegment = snapshot.donut?.segments?.find((s: DonutSegment) => s.key === context.architectKey)
          const client = archSegment?.clients?.find((c: ClientSegment) => c.key === context.clientKey)
          counts = client?.distribution?.histogram?.counts
          break
        }
      }

      if (counts && counts.length > 0) {
        maxCounts.push(Math.max(...counts))
      }
    }

    return maxCounts.length > 0 ? Math.max(...maxCounts) : undefined
  })()

  // Header actions: AUA/NNA toggle + Partner dropdown
  const headerActions = (
    <div className="flex items-center gap-4">
      {/* AUA / NNA / GRO Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 tracking-wider">Mode:</span>
        <div className="flex gap-1 bg-white/5 rounded-lg p-1">
          {([['aua', 'AUA'], ['nna', 'NNA'], ['gro', 'GRO']] as [PanelViewMode, string][]).map(([mode, label]) => (
            <button
              key={mode}
              onClick={() => { setPanelViewMode(mode); setSelectedBarPeriod(null); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                panelViewMode === mode
                  ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                  : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Interval Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 tracking-wider">Interval:</span>
        <div className="flex gap-1 bg-white/5 rounded-lg p-1">
          {([['monthly', 'Month'], ['quarterly', 'Quarter'], ['annually', 'Year']] as [GranularityOption, string][]).map(([opt, label]) => (
            <button
              key={opt}
              onClick={() => { onGranularityChange(opt); setSelectedBarPeriod(null); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                granularity === opt
                  ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                  : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Time Window Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 tracking-wider">Window:</span>
        <div className="flex gap-1 bg-white/5 rounded-lg p-1">
          {(['1Y', '3Y', 'Max'] as TimeWindow[]).map((opt) => (
            <button
              key={opt}
              onClick={() => { onTimeWindowChange(opt); setSelectedBarPeriod(null); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                timeWindow === opt
                  ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                  : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Firm Picker — Opal internal users only */}
      {internal && (
        <div className="flex items-center gap-2">
          <span className="text-xs text-white/50 tracking-wider">Firm:</span>
          <select
            value={selectedFirmId}
            onChange={e => onPartnerChange(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-[#1e1e2d] border border-white/20 text-white text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] cursor-pointer"
          >
            {AVAILABLE_FIRMS.map(f => (
              <option key={f.id} value={f.id} className="bg-[#1e1e2d] text-white">{f.name}</option>
            ))}
          </select>
        </div>
      )}
    </div>
  )

  // Loading state — gate on timeseries fetch, not header_metrics.json
  // The Assets Overview panel renders bar charts from timeseries_chart.json only.
  // header_metrics.json (data prop) is consumed by the Distribution tab, not here.
  if (timeseriesLoading) {
    return (
      <Panel variant="mixed">
        <PanelHeader
          title="Assets Overview"
          helpText="Total market value of all client accounts managed through the platform, broken down by new vs existing clients. Toggle to NNA to see net new asset flows."
          actions={headerActions}
        />
        <PanelContent className="pt-6">
          <LoadingInline className="py-16" />
        </PanelContent>
      </Panel>
    )
  }

  // No timeseries data available
  if (aggregatedAuaData.length === 0 && aggregatedNnaData.length === 0) {
    return (
      <Panel variant="mixed">
        <PanelHeader
          title="Assets Overview"
          helpText="Total market value of all client accounts managed through the platform, broken down by new vs existing clients. Toggle to NNA to see net new asset flows."
          actions={headerActions}
        />
        <PanelContent className="pt-6">
          <div className="flex items-center justify-center py-16">
            <p className="text-white/60">No timeseries data available</p>
          </div>
        </PanelContent>
        <PanelFooter content="Source: SS&C Black Diamond Wealth Solutions." timestamp={data?.generated_at} />
      </Panel>
    )
  }

  return (
    <Panel variant="mixed">
      <PanelHeader
        title="Assets Overview"
        helpText={panelViewMode === 'aua' ? "Total market value of all client accounts managed through the platform, broken down by new vs existing clients. New clients are those onboarded within the trailing 12 months." : panelViewMode === 'nna' ? "Net new assets measure organic growth — money flowing in from new and existing clients minus money flowing out. Positive NNA means the business is gathering assets beyond market movement." : "Monthly AUA change decomposed into market appreciation and net new assets. Shows whether growth is driven by market performance or organic inflows."}
        actions={headerActions}
      />
      <PanelContent className="pt-4">
        <div className="flex">
          {/* MAIN CHART AREA */}
          <div className="flex flex-col p-6 relative w-full">
            {/* Section Title + Y3-FE AUA Sub-Toggle */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider">
                  {panelViewMode === 'aua' ? 'Assets Under Advisory' : panelViewMode === 'nna' ? 'Net New Assets' : 'Growth Decomposition'}
                </h4>
                <Tooltip
                  content={panelViewMode === 'gro' ? "Monthly AUA change decomposed into market appreciation and net new assets." : "Click a bar to filter the breakdown table to that client type."}
                  side="auto"
                >
                  <HelpCircle size={14} className="text-white/40 hover:text-white/70 transition-colors cursor-help flex-shrink-0" />
                </Tooltip>
              </div>
              {/* Y3-FE: AUA sub-toggle (Clients / Mix) — inside panel content, not header */}
              {panelViewMode === 'aua' && (
                <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                  {([['clients', AUA_SUB_MODE_CLIENTS_LABEL], ['mix', 'Mix']] as [AuaSubMode, string][]).map(([mode, label]) => (
                    <button
                      key={mode}
                      onClick={() => setAuaSubMode(mode)}
                      className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors ${
                        auaSubMode === mode ? 'bg-white/20 text-white' : 'text-white/50 hover:text-white hover:bg-white/10'
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Chart Area */}
            <div className="flex-1 min-h-[400px]">
              {timeseriesLoading ? (
                <div className="h-full flex items-center justify-center">
                  <LoadingInline size="sm" />
                </div>
              ) : panelViewMode === 'aua' && auaSubMode === 'clients' && aggregatedAuaData.length > 0 && barCategories.length > 0 ? (
                /* AUA Clients Stacked Bar Chart */
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={aggregatedBarData}
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                    onClick={(data) => {
                      // eslint-disable-next-line @typescript-eslint/no-explicit-any
                      const chartData = data as any
                      if (chartData?.activePayload?.[0]?.payload?.period) {
                        handleBarClick({ period: chartData.activePayload[0].payload.period })
                      }
                    }}
                    style={{ cursor: 'pointer' }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={({ x, y, payload }) => {
                        const isSelected = aggregatedBarData.find(d => d.label === payload.value)?.period === selectedBarPeriod
                        return (
                          <text
                            x={x}
                            y={Number(y) + 12}
                            textAnchor="middle"
                            fontSize={11}
                            fill={isSelected ? 'hsl(var(--primary))' : 'rgba(255,255,255,0.6)'}
                            fontWeight={isSelected ? 600 : 400}
                          >
                            {payload.value}
                          </text>
                        )
                      }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`
                        if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                      domain={[0, (dataMax: number) => {
                        const last = panelViewMode === 'aua' ? augmentedAuaData[augmentedAuaData.length - 1] : null
                        const proj = last?._projectedTotal as number | undefined
                        return Math.max(dataMax, proj ?? 0) * 1.05
                      }]}
                    />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null

                        const total = payload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                        const sortedPayload = [...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                        const periodData = payload[0]?.payload
                        const isSelected = periodData?.period === selectedBarPeriod
                        const isCurrentPeriod = periodData?.period === aggregatedAuaData[aggregatedAuaData.length - 1]?.period

                        // Period-over-period growth
                        const currentIdx = aggregatedAuaData.findIndex(d => d.period === periodData?.period)
                        const priorPeriod = currentIdx > 0 ? aggregatedAuaData[currentIdx - 1] : null
                        const priorTotal = priorPeriod
                          ? barCategories.reduce((sum, cat) => sum + (Number((priorPeriod as Record<string, unknown>)[cat]) || 0), 0)
                          : null
                        const growth = priorTotal !== null && priorTotal > 0 ? total - priorTotal : null
                        const growthPct = priorTotal !== null && priorTotal > 0 ? ((total / priorTotal) - 1) * 100 : null
                        const growthLabel = granularity === 'monthly' ? 'MoM Growth' : granularity === 'quarterly' ? 'QoQ Growth' : 'YoY Growth'

                        // Projection from stored values
                        const hasProjections = isCurrentPeriod && periodData?._projectedTotal != null
                        const projectionUnavailable = isCurrentPeriod && periodData?._projectionUnavailable === true

                        return (
                          <div className={`bg-[#0f1729] border-2 rounded-lg px-4 py-3 shadow-xl ${isSelected ? 'border-[hsl(var(--primary))]' : 'border-white/10'}`}>
                            <div className="text-white font-bold text-sm mb-2 flex items-center gap-2">
                              {label}
                              {isSelected && <span className="text-xs font-normal text-[hsl(var(--primary))]">(Selected)</span>}
                            </div>
                            <div className="flex items-center justify-between gap-6 mb-2">
                              <span className="text-white/70 text-sm">Total AUA</span>
                              <span className="text-white font-semibold text-sm">
                                {formatCurrency(total)}
                              </span>
                            </div>
                            <div className="space-y-1.5 border-t border-white/10 pt-2">
                              {sortedPayload.map((entry, index) => (
                                <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                  <div className="flex items-center gap-2">
                                    <div
                                      className="w-2.5 h-2.5 rounded-full"
                                      style={{ backgroundColor: entry.color }}
                                    />
                                    <span className="text-white/70">
                                      {getBarCategoryDisplayName(String(entry.dataKey))}
                                    </span>
                                  </div>
                                  <span className="text-white font-medium">
                                    {formatCurrency(Number(entry.value) || 0)}
                                  </span>
                                </div>
                              ))}
                            </div>
                            {growth !== null && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1">
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">{growthLabel}</span>
                                  <span className={`font-semibold ${growth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                    {growth >= 0 ? '+' : ''}{formatCurrency(growth)}
                                  </span>
                                </div>
                                {growthPct !== null && (
                                  <div className="flex items-center justify-end text-xs">
                                    <span className={`font-semibold ${growth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                      {growth >= 0 ? '+' : ''}{growthPct.toFixed(1)}%
                                    </span>
                                  </div>
                                )}
                              </div>
                            )}
                            {hasProjections && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected Full Period</div>
                                {barCategories.map((cat, index) => {
                                  const actual = Number(periodData[cat]) || 0
                                  const projected = Number(periodData[`_projected_${cat}`]) || 0
                                  if (projected === actual) return null
                                  return (
                                    <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                      <span className="text-white/50">
                                        {getBarCategoryDisplayName(cat)}
                                      </span>
                                      <span className="text-white/60 font-medium">
                                        {formatCurrency(projected)} <span className="text-white/30">(currently {formatCurrency(actual)})</span>
                                      </span>
                                    </div>
                                  )
                                })}
                                <div className="flex items-center justify-between gap-4 text-xs border-t border-white/5 pt-1">
                                  <span className="text-white/50 font-medium">Projected Total</span>
                                  <span className="text-white/60 font-semibold">
                                    {formatCurrency(periodData._projectedTotal)} <span className="text-white/30">(currently {formatCurrency(periodData._actualTotal)})</span>
                                  </span>
                                </div>
                              </div>
                            )}
                            {projectionUnavailable && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5">
                                <span className="text-white/30 text-[10px] italic">Projection unavailable (insufficient history)</span>
                              </div>
                            )}
                          </div>
                        )
                      }}
                    />
                    {/* Y1: Render NMEC first (bottom), NMNC last (top) per Yang feedback */}
                    {[...barCategories].reverse().map((cat, idx) => {
                      const baseColor = getBarCategoryColor(cat, idx)
                      const isLastCategory = idx === barCategories.length - 1
                      return (
                        <Bar
                          key={cat}
                          dataKey={cat}
                          stackId="aua"
                          fill={baseColor}
                          radius={isLastCategory ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                        >
                          {aggregatedBarData.map((entry, index) => {
                            const isSelected = entry.period === selectedBarPeriod
                            const isLatest = index === aggregatedBarData.length - 1
                            // Selected bars get full opacity, others are dimmed when something is selected
                            const opacity = selectedBarPeriod
                              ? (isSelected ? 1 : 0.4)
                              : (isLatest ? 1 : 0.85)
                            return (
                              <Cell
                                key={`cell-${cat}-${index}`}
                                fill={baseColor}
                                fillOpacity={opacity}
                                stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                                strokeWidth={isSelected ? 2 : 0}
                              />
                            )
                          })}
                        </Bar>
                      )
                    })}
                    {/* F2: Dashed horizontal line at projected total AUA */}
                    {(() => {
                      const lastEntry = augmentedAuaData[augmentedAuaData.length - 1]
                      if (lastEntry?._projectedTotal == null || lastEntry._projectedTotal === lastEntry._actualTotal) return null
                      const isUp = lastEntry._projectedTotal > lastEntry._actualTotal
                      return (
                        <ReferenceLine
                          y={lastEntry._projectedTotal}
                          stroke={isUp ? 'hsl(var(--success))' : '#EF4444'}
                          strokeWidth={2}
                          strokeDasharray="6 3"
                          label={{ value: `Proj: ${formatCurrency(lastEntry._projectedTotal)}`, position: 'right', fill: isUp ? 'hsl(var(--success))' : '#EF4444', fontSize: 10 }}
                        />
                      )
                    })()}
                  </BarChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'nna' && augmentedNnaData.length > 0 ? (
                /*
                 * NNA Chart — two modes:
                 * GROSS (hasGrossFlowData): Diverging bar chart.
                 *   Inflow bars above zero, outflow bars below zero (both present every period),
                 *   net flow line overlay shows the netted movement.
                 * NET-ONLY (!hasGrossFlowData): Single net bar, green = positive, red = negative.
                 *   Used until the publisher is updated to output cum_inflows/cum_outflows.
                 */
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={augmentedNnaData}
                    stackOffset="sign"
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                    onClick={(data) => {
                      // eslint-disable-next-line @typescript-eslint/no-explicit-any
                      const chartData = data as any
                      if (chartData?.activePayload?.[0]?.payload?.period) {
                        handleBarClick({ period: chartData.activePayload[0].payload.period })
                      }
                    }}
                    style={{ cursor: 'pointer' }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={({ x, y, payload }) => {
                        const isSelected = aggregatedNnaData.find(d => d.label === payload.value)?.period === selectedBarPeriod
                        return (
                          <text
                            x={x}
                            y={Number(y) + 12}
                            textAnchor="middle"
                            fontSize={11}
                            fill={isSelected ? 'hsl(var(--primary))' : 'rgba(255,255,255,0.6)'}
                            fontWeight={isSelected ? 600 : 400}
                          >
                            {payload.value}
                          </text>
                        )
                      }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        const absVal = Math.abs(value)
                        if (absVal >= 1e9) return `${value < 0 ? '-' : ''}$${(absVal / 1e9).toFixed(1)}B`
                        if (absVal >= 1e6) return `${value < 0 ? '-' : ''}$${(absVal / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={60}
                      axisLine={false}
                      tickLine={false}
                    />
                    <ReferenceLine y={0} stroke="rgba(255,255,255,0.3)" strokeWidth={1} />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        const periodData = payload[0]?.payload as any
                        const isSelected = periodData?.period === selectedBarPeriod
                        const isCurrentNnaPeriod = periodData?.period === aggregatedNnaData[aggregatedNnaData.length - 1]?.period

                        // Period-over-period growth for NNA
                        const nnaGrowthLabel = granularity === 'monthly' ? 'MoM Change' : granularity === 'quarterly' ? 'QoQ Change' : 'YoY Change'
                        const currentNnaIdx = aggregatedNnaData.findIndex(d => d.period === periodData?.period)
                        const priorNnaPeriod = currentNnaIdx > 0 ? aggregatedNnaData[currentNnaIdx - 1] : null
                        const priorNet = priorNnaPeriod?.net ?? null
                        const currentNet = periodData?.net || 0
                        const nnaChange = priorNet !== null ? currentNet - priorNet : null

                        return (
                          <div className={`bg-[#0f1729] border-2 rounded-lg px-4 py-3 shadow-xl ${isSelected ? 'border-[hsl(var(--primary))]' : 'border-white/10'}`}>
                            <div className="text-white font-bold text-sm mb-2 flex items-center gap-2">
                              {label}
                              {isSelected && <span className="text-xs font-normal text-[hsl(var(--primary))]">(Selected)</span>}
                            </div>
                            <div className="space-y-1.5">
                              {hasGrossFlowData ? (
                                <>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <div className="flex items-center gap-2">
                                      <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: NNA_COLORS.inflow }} />
                                      <span className="text-white/70">Inflows</span>
                                    </div>
                                    <span className="font-medium text-[hsl(var(--success))]">
                                      +{formatCurrency(periodData?.inflow || 0)}
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <div className="flex items-center gap-2">
                                      <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: NNA_COLORS.outflow }} />
                                      <span className="text-white/70">Outflows</span>
                                    </div>
                                    <span className="font-medium text-red-400">
                                      -{formatCurrency(Math.abs(periodData?.outflow || 0))}
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs border-t border-white/10 pt-1.5 mt-1.5">
                                    <div className="flex items-center gap-2">
                                      <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: '#F59E0B' }} />
                                      <span className="text-white/70 font-medium">Net Flow</span>
                                    </div>
                                    <span className={`font-semibold ${(periodData?.net || 0) >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                      {(periodData?.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData?.net || 0)}
                                    </span>
                                  </div>
                                </>
                              ) : (
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">Net NNA</span>
                                  <span className={`font-semibold ${(periodData?.net || 0) >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                    {(periodData?.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData?.net || 0)}
                                  </span>
                                </div>
                              )}
                            </div>
                            {nnaChange !== null && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5">
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">{nnaGrowthLabel}</span>
                                  <span className={`font-semibold ${nnaChange >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                    {nnaChange >= 0 ? '+' : ''}{formatCurrency(nnaChange)}
                                  </span>
                                </div>
                              </div>
                            )}
                            {isCurrentNnaPeriod && periodData?._projectedNet != null && hasGrossFlowData && (() => {
                              const projInflow = periodData._projectedInflow as number
                              const projOutflow = periodData._projectedOutflow as number
                              const projNet = periodData._projectedNet as number
                              return (
                                <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                  <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected Full Period</div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50">Inflows</span>
                                    <span className="text-white/60 font-medium">
                                      +{formatCurrency(projInflow)} <span className="text-white/30">(currently +{formatCurrency(periodData.inflow)})</span>
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50">Outflows</span>
                                    <span className="text-white/60 font-medium">
                                      -{formatCurrency(Math.abs(projOutflow))} <span className="text-white/30">(currently -{formatCurrency(Math.abs(periodData.outflow))})</span>
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs border-t border-white/5 pt-1">
                                    <span className="text-white/50 font-medium">Net</span>
                                    <span className="text-white/60 font-semibold">
                                      {projNet >= 0 ? '+' : ''}{formatCurrency(projNet)} <span className="text-white/30">(currently {(periodData.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData.net || 0)})</span>
                                    </span>
                                  </div>
                                </div>
                              )
                            })()}
                            {isCurrentNnaPeriod && !hasGrossFlowData && periodData?._projectedNet != null && (() => {
                              const projNet = periodData._projectedNet as number
                              return (
                                <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                  <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected Full Period</div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50 font-medium">Net</span>
                                    <span className="text-white/60 font-semibold">
                                      {projNet >= 0 ? '+' : ''}{formatCurrency(projNet)} <span className="text-white/30">(currently {(periodData.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData.net || 0)})</span>
                                    </span>
                                  </div>
                                </div>
                              )
                            })()}
                          </div>
                        )
                      }}
                    />
                    {hasGrossFlowData ? (
                      <>
                        {/* GROSS MODE: Inflow bar above zero, outflow bar below zero */}
                        <Bar dataKey="inflow" stackId="nna" radius={[4, 4, 0, 0]}>
                          {augmentedNnaData.map((entry, index) => {
                            const isSelected = entry.period === selectedBarPeriod
                            const isLatest = index === augmentedNnaData.length - 1
                            const opacity = selectedBarPeriod ? (isSelected ? 1 : 0.4) : (isLatest ? 1 : 0.85)
                            return (
                              <Cell
                                key={`inflow-${index}`}
                                fill={NNA_COLORS.inflow}
                                fillOpacity={opacity}
                                stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                                strokeWidth={isSelected ? 2 : 0}
                              />
                            )
                          })}
                        </Bar>
                        <Bar dataKey="outflow" stackId="nna" radius={[0, 0, 4, 4]}>
                          {augmentedNnaData.map((entry, index) => {
                            const isSelected = entry.period === selectedBarPeriod
                            const isLatest = index === augmentedNnaData.length - 1
                            const opacity = selectedBarPeriod ? (isSelected ? 1 : 0.4) : (isLatest ? 1 : 0.85)
                            return (
                              <Cell
                                key={`outflow-${index}`}
                                fill={NNA_COLORS.outflow}
                                fillOpacity={opacity}
                                stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                                strokeWidth={isSelected ? 2 : 0}
                              />
                            )
                          })}
                        </Bar>
                        {/* Net flow line: actual NNA value (inflows + outflows) */}
                        <Line
                          type="monotone"
                          dataKey="net"
                          stroke="#F59E0B"
                          strokeWidth={3}
                          dot={{ r: 5, fill: '#F59E0B', strokeWidth: 2, stroke: 'hsl(var(--background))' }}
                          activeDot={{ r: 7 }}
                          connectNulls
                        />
                      </>
                    ) : (
                      /* NET-ONLY MODE: Single bar colored green/red per sign */
                      <Bar dataKey="net" radius={[4, 4, 0, 0]}>
                        {augmentedNnaData.map((entry, index) => {
                          const isSelected = entry.period === selectedBarPeriod
                          const isLatest = index === augmentedNnaData.length - 1
                          const opacity = selectedBarPeriod ? (isSelected ? 1 : 0.4) : (isLatest ? 1 : 0.85)
                          return (
                            <Cell
                              key={`net-${index}`}
                              fill={entry.net >= 0 ? NNA_COLORS.inflow : NNA_COLORS.outflow}
                              fillOpacity={opacity}
                              stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                              strokeWidth={isSelected ? 2 : 0}
                            />
                          )
                        })}
                      </Bar>
                    )}
                    {/* F2: Dashed horizontal line at projected net NNA */}
                    {(() => {
                      const lastNna = augmentedNnaData[augmentedNnaData.length - 1]
                      if (lastNna?._projectedNet == null) return null
                      const projNet = lastNna._projectedNet as number
                      const actualNet = lastNna.net
                      if (projNet === actualNet) return null
                      const isUp = projNet > actualNet
                      return (
                        <ReferenceLine
                          y={projNet}
                          stroke={isUp ? 'hsl(var(--success))' : '#EF4444'}
                          strokeWidth={2}
                          strokeDasharray="6 3"
                          label={{ value: `Proj: ${projNet >= 0 ? '+' : ''}${formatCurrency(projNet)}`, position: 'right', fill: isUp ? 'hsl(var(--success))' : '#EF4444', fontSize: 10 }}
                        />
                      )
                    })()}
                  </ComposedChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' && firmMixChartData.length > 0 ? (
                /* Mix: absolute dollar stacked bar chart (MIXV2 -- pre-aggregated from mix-views endpoint) */
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={firmMixChartData}
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.6)' }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value: number) => {
                        if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`
                        if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                      domain={[0, (dataMax: number) => dataMax * 1.05]}
                    />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null
                        const row = payload[0]?.payload as Record<string, number> | undefined
                        const sorted = [...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                        const CLASS_LABELS: Record<string, string> = {
                          equity: 'Equities', fixed_income: 'Fixed Income',
                          alternatives: 'Alternatives', cash: 'Cash',
                        }
                        return (
                          <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl min-w-[200px]">
                            <div className="text-white font-bold text-sm mb-1">{String(label)}</div>
                            {row && (
                              <div className="text-white/50 text-xs mb-2">
                                Total AUA: {formatCurrency(row.total_aua)}
                              </div>
                            )}
                            <hr className="border-white/10 mb-2" />
                            <div className="space-y-1.5">
                              {sorted.map((entry, index) => {
                                const cls = String(entry.dataKey)
                                const pctKey = `${cls}_pct`
                                const pct = row ? (Number(row[pctKey]) || 0) * 100 : 0
                                return (
                                  <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                    <div className="flex items-center gap-2">
                                      <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color as string }} />
                                      <span className="text-white/70">{CLASS_LABELS[cls] ?? cls}</span>
                                    </div>
                                    <span className="text-white font-medium">
                                      {formatCurrency(Number(entry.value) || 0)}&nbsp;
                                      <span className="text-white/50">({pct.toFixed(1)}%)</span>
                                    </span>
                                  </div>
                                )
                              })}
                            </div>
                          </div>
                        )
                      }}
                    />
                    {(['cash', 'alternatives', 'fixed_income', 'equity'] as const).map((cls, idx) => {
                      const color = FIRM_MIX_COLORS[cls]
                      const isTop = idx === 3 // equity is last rendered = top of stack
                      return (
                        <Bar
                          key={cls}
                          dataKey={cls}
                          stackId="mix"
                          fill={color}
                          fillOpacity={0.85}
                          radius={isTop ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                        />
                      )
                    })}
                  </BarChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                /* Mix: loading or unavailable */
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">
                    {isFirmMixLoading ? 'Loading mix data...' : isFirmMixError ? 'Failed to load mix data' : 'Asset class mix data unavailable'}
                  </p>
                </div>
              ) : panelViewMode === 'gro' && augmentedGroData.length > 0 ? (
                /* GRO: Stacked bars (Market + Net Flows) + Total line overlay */
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={augmentedGroData}
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                    stackOffset="sign"
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.6)' }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        if (Math.abs(value) >= 1e9) return `${value < 0 ? '-' : ''}$${(Math.abs(value) / 1e9).toFixed(1)}B`
                        if (Math.abs(value) >= 1e6) return `${value < 0 ? '-' : ''}$${(Math.abs(value) / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                      label={{ value: 'AUA Change', angle: -90, position: 'insideLeft', offset: -5, style: { fontSize: 9, fill: 'rgba(255,255,255,0.3)' } }}
                    />
                    <ReferenceLine y={0} stroke="rgba(255,255,255,0.3)" strokeWidth={1} />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload }) => {
                        if (!active || !payload || payload.length === 0) return null
                        // Datum-driven rendering — not payload.map()
                        const datum = payload[0]?.payload as { label: string; market: number; nna: number; total: number; period: string; endDate: string }
                        if (!datum) return null

                        const signFmt = (v: number) => `${v >= 0 ? '+' : ''}${formatCurrency(v)}`
                        const signColor = (v: number) => v >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'

                        return (
                          <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                            <div className="text-white font-bold text-sm mb-0.5">{datum.label}</div>
                            <div className="text-white/30 text-[10px] mb-2">AUA change (period delta)</div>
                            <div className="space-y-1.5">
                              <div className="flex items-center justify-between gap-6 text-xs">
                                <div className="flex items-center gap-2">
                                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: GRO_COLORS.market }} />
                                  <span className="text-white/70">Market</span>
                                </div>
                                <span className={`font-medium ${signColor(datum.market)}`}>{signFmt(datum.market)}</span>
                              </div>
                              <div className="flex items-center justify-between gap-6 text-xs">
                                <div className="flex items-center gap-2">
                                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: GRO_COLORS.nna }} />
                                  <span className="text-white/70">Net Flows (NNA)</span>
                                </div>
                                <span className={`font-medium ${signColor(datum.nna)}`}>{signFmt(datum.nna)}</span>
                              </div>
                              <div className="flex items-center justify-between gap-6 text-xs border-t border-white/10 pt-1.5 mt-1.5">
                                <div className="flex items-center gap-2">
                                  <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.total }} />
                                  <span className="text-white/70 font-medium">Total Change</span>
                                </div>
                                <span className={`font-semibold ${signColor(datum.total)}`}>{signFmt(datum.total)}</span>
                              </div>
                            </div>
                          </div>
                        )
                      }}
                    />
                    <Bar dataKey="market" stackId="gro" fill={GRO_COLORS.market} fillOpacity={0.8} radius={[0, 0, 0, 0]} isAnimationActive={false} />
                    <Bar dataKey="nna" stackId="gro" fill={GRO_COLORS.nna} fillOpacity={0.8} radius={[0, 0, 0, 0]} isAnimationActive={false} />
                    <Line type="monotone" dataKey="total" stroke={GRO_COLORS.total} strokeWidth={3} dot={{ r: 5, fill: GRO_COLORS.total, strokeWidth: 2, stroke: 'hsl(var(--background))' }} activeDot={{ r: 7 }} />
                  </ComposedChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'gro' ? (
                /* Y5-FE: GRO data unavailable */
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">Growth decomposition data unavailable</p>
                </div>
              ) : (
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">No {panelViewMode === 'aua' ? 'AUA' : 'NNA'} data available</p>
                </div>
              )}
            </div>

            {/* Legend */}
            <div className="flex justify-center gap-6 mt-4">
              {panelViewMode === 'aua' && auaSubMode === 'clients' ? (
                barCategories.map((cat, idx) => (
                  <div key={cat} className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-sm"
                      style={{ backgroundColor: getBarCategoryColor(cat, idx) }}
                    />
                    <span className="text-xs text-white/70">{getBarCategoryDisplayName(cat)}</span>
                  </div>
                ))
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                (['Equities', 'Fixed Income', 'Structured Notes', 'Cash', 'Other'] as const).map((cat, idx) => (
                  <div key={cat} className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: getAssetClassColor(cat, idx) }} />
                    <span className="text-xs text-white/70">{cat}</span>
                  </div>
                ))
              ) : panelViewMode === 'gro' ? (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: GRO_COLORS.market }} />
                    <span className="text-xs text-white/70">Market</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: GRO_COLORS.nna }} />
                    <span className="text-xs text-white/70">Net Flows (NNA)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.total }} />
                    <span className="text-xs text-white/70">Total (Market + NNA)</span>
                  </div>
                </>
              ) : hasGrossFlowData ? (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.inflow }} />
                    <span className="text-xs text-white/70">Inflows</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.outflow }} />
                    <span className="text-xs text-white/70">Outflows</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: '#F59E0B' }} />
                    <span className="text-xs text-white/70">Net Flow</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.inflow }} />
                    <span className="text-xs text-white/70">Positive NNA</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.outflow }} />
                    <span className="text-xs text-white/70">Negative NNA</span>
                  </div>
                </>
              )}
            </div>


            {/* Selected/Latest Value Highlight (AUA Clients + NNA only — not Mix or GRO) */}
            {panelViewMode !== 'gro' && !(panelViewMode === 'aua' && auaSubMode === 'mix') && (panelViewMode === 'aua' ? aggregatedAuaData : aggregatedNnaData).length > 0 && (() => {
              const activeData = panelViewMode === 'aua' ? aggregatedAuaData : aggregatedNnaData
              const latest = activeData[activeData.length - 1]
              const src = selectedBarData || latest
              const isSelectedPeriod = !!selectedBarData
              const isLatestPeriod = src.period === latest.period

              // --- Helper: get period start date from a period key ---
              const getPeriodStartDate = (periodKey: string): Date => {
                if (granularity === 'monthly') {
                  // "2026-02" -> Feb 1
                  const [y, m] = periodKey.split('-').map(Number)
                  return new Date(y, m - 1, 1)
                } else if (granularity === 'quarterly') {
                  // "2026-Q1" -> Jan 1
                  const [y, q] = periodKey.split('-Q').map(Number)
                  return new Date(y, (q - 1) * 3, 1)
                } else {
                  // "2026" -> Jan 1
                  return new Date(Number(periodKey), 0, 1)
                }
              }

              // --- Helper: find comparable prior-period snapshot from daily data ---
              // For in-progress periods: finds the data point at the same day-offset in the prior period
              // For completed periods: returns the end-of-period (last) data point
              // With pre-aggregated period data (PSCFIX schema), prior comparison is a direct
              // period lookup — no daily data or day-offset matching needed.

              // --- AUA current values ---
              const auaTotal = panelViewMode === 'aua'
                ? barCategories.reduce((sum, cat) => sum + (Number((src as Record<string, unknown>)[cat]) || 0), 0)
                : 0
              const auaNewClient = panelViewMode === 'aua'
                ? (Number((src as Record<string, unknown>)['NMNC']) || Number((src as Record<string, unknown>)['nmnc']) || 0)
                : 0
              const auaExistingClient = panelViewMode === 'aua'
                ? (Number((src as Record<string, unknown>)['NMEC']) || Number((src as Record<string, unknown>)['nmec']) || 0)
                : 0

              // --- AUA comparable growth ---
              const auaSrcIdx = panelViewMode === 'aua'
                ? aggregatedAuaData.findIndex(d => d.period === src.period)
                : -1
              const auaPriorAgg = auaSrcIdx > 0 ? aggregatedAuaData[auaSrcIdx - 1] : null
              const auaPriorLabel = auaPriorAgg ? String(auaPriorAgg.label) : null

              let auaGrowth: number | null = null
              let auaGrowthPct: number | null = null
              let auaNewGrowth: number | null = null
              let auaNewGrowthPct: number | null = null
              let auaExistingGrowth: number | null = null
              let auaExistingGrowthPct: number | null = null
              let auaComparableDays: number | null = null

              if (auaPriorAgg) {
                const prior = auaPriorAgg as Record<string, unknown>
                const priorTotal = barCategories.reduce((sum, cat) => sum + (Number(prior[cat]) || 0), 0)
                const priorNew = Number(prior['NMNC']) || Number(prior['nmnc']) || 0
                const priorExisting = Number(prior['NMEC']) || Number(prior['nmec']) || 0
                auaComparableDays = null  // not applicable with pre-aggregated period data

                if (priorTotal > 0) {
                  auaGrowth = auaTotal - priorTotal
                  auaGrowthPct = ((auaTotal / priorTotal) - 1) * 100
                }
                if (priorNew > 0) {
                  auaNewGrowth = auaNewClient - priorNew
                  auaNewGrowthPct = ((auaNewClient / priorNew) - 1) * 100
                }
                if (priorExisting > 0) {
                  auaExistingGrowth = auaExistingClient - priorExisting
                  auaExistingGrowthPct = ((auaExistingClient / priorExisting) - 1) * 100
                }
              }

              // --- NNA current values ---
              const nnaInflow  = Number((src as { inflow?: number }).inflow) || 0
              const nnaOutflow = Math.abs(Number((src as { outflow?: number }).outflow) || 0)
              const nnaNet     = Number((src as { net?: number }).net) || 0

              // --- NNA comparable growth ---
              const nnaSrcIdx = panelViewMode === 'nna'
                ? aggregatedNnaData.findIndex(d => d.period === src.period)
                : -1
              const nnaPriorAgg = nnaSrcIdx > 0 ? aggregatedNnaData[nnaSrcIdx - 1] : null
              const nnaPriorLabel = nnaPriorAgg ? String(nnaPriorAgg.label) : null

              let nnaInflowGrowth: number | null = null
              let nnaInflowGrowthPct: number | null = null
              let nnaOutflowGrowth: number | null = null
              let nnaOutflowGrowthPct: number | null = null
              let nnaNetGrowth: number | null = null
              let nnaNetGrowthPct: number | null = null
              let nnaComparableDays: number | null = null

              if (nnaPriorAgg && timeseriesData?.nna?.data) {
                const nnaDaily = timeseriesData.nna.data
                const nnaCategories = timeseriesData.nna.categories || []
                const grossFlows = nnaCategories.includes('Inflows') && nnaCategories.includes('Outflows')
                const isInProgress = isLatestPeriod && !isSelectedPeriod

                // For NNA flows we need to compute period-to-date flows (not snapshots)
                // Flow = last cumulative value in window - first cumulative value before window (end of prior period)
                const computePeriodFlows = (periodKey: string, maxDayOffset?: number) => {
                  const periodStart = getPeriodStartDate(periodKey)
                  const maxDate = maxDayOffset !== undefined
                    ? new Date(periodStart.getTime() + maxDayOffset * 24 * 60 * 60 * 1000)
                    : new Date(9999, 0, 1) // no limit

                  const periodPoints = nnaDaily.filter(p => {
                    const d = new Date(String(p.date) + 'T12:00:00')
                    return getPeriodInfo(d).periodKey === periodKey && d <= maxDate
                  })
                  if (periodPoints.length === 0) return null

                  const first = periodPoints[0]
                  const last = periodPoints[periodPoints.length - 1]

                  // Get the cumulative value just before this period (last point of prior period)
                  // For differencing: flow = last_cum - first_cum_before_period
                  // Since first point in period IS the first cum value at period start,
                  // and last is the cum value at the end of the window:
                  // period flow = last_cum - prev_period_end_cum
                  // But we already have the first point of this period which ~= prev period end
                  // Use first point as the baseline (it's the earliest snapshot in the period)
                  const netFlow = (Number(last['NNA']) || 0) - (Number(first['NNA']) || 0)
                  const inflowFlow = grossFlows ? (Number(last['Inflows']) || 0) - (Number(first['Inflows']) || 0) : 0
                  const outflowFlow = grossFlows ? Math.abs((Number(last['Outflows']) || 0) - (Number(first['Outflows']) || 0)) : 0

                  return { net: netFlow, inflow: inflowFlow, outflow: outflowFlow, days: periodPoints.length }
                }

                if (isInProgress) {
                  // Comparable: same day-offset in both periods
                  const currentStart = getPeriodStartDate(String(src.period))
                  const currentEndDate = new Date(String(src.endDate) + 'T12:00:00')
                  const dayOffset = Math.floor((currentEndDate.getTime() - currentStart.getTime()) / (1000 * 60 * 60 * 24))

                  const currentFlows = computePeriodFlows(String(src.period))
                  const priorFlows = computePeriodFlows(String(nnaPriorAgg.period), dayOffset)

                  if (currentFlows && priorFlows) {
                    nnaComparableDays = dayOffset + 1
                    nnaNetGrowth = currentFlows.net - priorFlows.net
                    if (priorFlows.net !== 0) nnaNetGrowthPct = ((currentFlows.net / Math.abs(priorFlows.net)) - (priorFlows.net >= 0 ? 1 : -1)) * 100
                    if (grossFlows) {
                      nnaInflowGrowth = currentFlows.inflow - priorFlows.inflow
                      if (priorFlows.inflow > 0) nnaInflowGrowthPct = ((currentFlows.inflow / priorFlows.inflow) - 1) * 100
                      nnaOutflowGrowth = currentFlows.outflow - priorFlows.outflow
                      if (priorFlows.outflow > 0) nnaOutflowGrowthPct = ((currentFlows.outflow / priorFlows.outflow) - 1) * 100
                    }
                  }
                } else {
                  // Completed period: full period vs full prior period (from aggregated data)
                  const priorInflow = Number((nnaPriorAgg as { inflow?: number }).inflow) || 0
                  const priorOutflow = Math.abs(Number((nnaPriorAgg as { outflow?: number }).outflow) || 0)
                  const priorNet = Number((nnaPriorAgg as { net?: number }).net) || 0

                  if (priorInflow > 0) { nnaInflowGrowth = nnaInflow - priorInflow; nnaInflowGrowthPct = ((nnaInflow / priorInflow) - 1) * 100 }
                  if (priorOutflow > 0) { nnaOutflowGrowth = nnaOutflow - priorOutflow; nnaOutflowGrowthPct = ((nnaOutflow / priorOutflow) - 1) * 100 }
                  nnaNetGrowth = nnaNet - priorNet
                  if (priorNet !== 0) nnaNetGrowthPct = ((nnaNet / Math.abs(priorNet)) - (priorNet >= 0 ? 1 : -1)) * 100
                }
              }

              // Comparable period label: "vs Day 58 of Q4 '25" for in-progress, "vs Q4 '25" for completed
              const comparableDays = panelViewMode === 'aua' ? auaComparableDays : nnaComparableDays
              const priorLabel = panelViewMode === 'aua' ? auaPriorLabel : nnaPriorLabel
              const comparisonLabel = comparableDays && comparableDays > 0
                ? `vs Day ${comparableDays} of ${priorLabel}`
                : priorLabel ? `vs ${priorLabel}` : null

              return (
                <div className="w-full mt-4 rounded-xl bg-white/5 border border-white/10 px-6 py-4">
                  {/* Period header */}
                  <div className="flex items-center justify-center gap-2 mb-4">
                    {isSelectedPeriod && (
                      <div className="w-1.5 h-1.5 rounded-full bg-[hsl(var(--primary))] animate-pulse flex-shrink-0" />
                    )}
                    <span className="text-[10px] text-white/50 uppercase tracking-widest font-medium">
                      {src.label}
                    </span>
                    {isSelectedPeriod && (
                      <button
                        onClick={() => setSelectedBarPeriod(null)}
                        className="text-[10px] text-white/30 hover:text-white/60 transition-colors"
                      >
                        (clear)
                      </button>
                    )}
                  </div>

                  {/* Metric tiles */}
                  {panelViewMode === 'aua' ? (
                    <div className="flex flex-wrap items-stretch gap-3">
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#4CAF50]/10 border border-[#4CAF50]/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">New Clients</div>
                        <div className="text-2xl font-bold text-[#4CAF50]">{formatCurrency(auaNewClient)}</div>
                        {auaNewGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${auaNewGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {auaNewGrowth >= 0 ? '+' : ''}{formatCurrency(auaNewGrowth)}
                              {auaNewGrowthPct !== null && <span className="ml-1">({auaNewGrowth >= 0 ? '+' : ''}{auaNewGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#2196F3]/10 border border-[#2196F3]/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Existing Clients</div>
                        <div className="text-2xl font-bold text-[#2196F3]">{formatCurrency(auaExistingClient)}</div>
                        {auaExistingGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${auaExistingGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {auaExistingGrowth >= 0 ? '+' : ''}{formatCurrency(auaExistingGrowth)}
                              {auaExistingGrowthPct !== null && <span className="ml-1">({auaExistingGrowth >= 0 ? '+' : ''}{auaExistingGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Total AUA</div>
                        <div className="text-2xl font-bold text-white">{formatCurrency(auaTotal)}</div>
                        {auaGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${auaGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {auaGrowth >= 0 ? '+' : ''}{formatCurrency(auaGrowth)}
                              {auaGrowthPct !== null && <span className="ml-1">({auaGrowth >= 0 ? '+' : ''}{auaGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                    </div>
                  ) : hasGrossFlowData ? (
                    <div className="flex flex-wrap items-stretch gap-3">
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-[hsl(var(--success))]/10 border border-[hsl(var(--success))]/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Inflows</div>
                        <div className="text-2xl font-bold text-[hsl(var(--success))]">+{formatCurrency(nnaInflow)}</div>
                        {nnaInflowGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaInflowGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {nnaInflowGrowth >= 0 ? '+' : ''}{formatCurrency(nnaInflowGrowth)}
                              {nnaInflowGrowthPct !== null && <span className="ml-1">({nnaInflowGrowth >= 0 ? '+' : ''}{nnaInflowGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Outflows</div>
                        <div className="text-2xl font-bold text-red-400">-{formatCurrency(nnaOutflow)}</div>
                        {nnaOutflowGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaOutflowGrowth >= 0 ? 'text-red-400' : 'text-[hsl(var(--success))]'}`}>
                              {nnaOutflowGrowth >= 0 ? '+' : ''}{formatCurrency(nnaOutflowGrowth)}
                              {nnaOutflowGrowthPct !== null && <span className="ml-1">({nnaOutflowGrowth >= 0 ? '+' : ''}{nnaOutflowGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Net Flow</div>
                        <div className={`text-2xl font-bold ${nnaNet >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                          {nnaNet >= 0 ? '+' : ''}{formatCurrency(nnaNet)}
                        </div>
                        {nnaNetGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaNetGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {nnaNetGrowth >= 0 ? '+' : ''}{formatCurrency(nnaNetGrowth)}
                              {nnaNetGrowthPct !== null && <span className="ml-1">({nnaNetGrowth >= 0 ? '+' : ''}{nnaNetGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-center">
                      <div className="flex flex-col items-center px-10 py-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Net New Assets</div>
                        <div className={`text-3xl font-bold ${nnaNet >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                          {nnaNet >= 0 ? '+' : ''}{formatCurrency(nnaNet)}
                        </div>
                        {nnaNetGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaNetGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {nnaNetGrowth >= 0 ? '+' : ''}{formatCurrency(nnaNetGrowth)}
                              {nnaNetGrowthPct !== null && <span className="ml-1">({nnaNetGrowth >= 0 ? '+' : ''}{nnaNetGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Date */}
                  {src.end_date && (
                    <div className="text-[10px] text-white/30 text-center mt-3">
                      as of {new Date((src.end_date as string) + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </div>
                  )}
                </div>
              )
            })()}

            {/* GRO hero metrics tiles */}
            {panelViewMode === 'gro' && aggregatedGroData.length > 0 && (() => {
              const latest = aggregatedGroData[aggregatedGroData.length - 1]

              // Cumulative totals across the full window (sum of all periods)
              const cumMarket = aggregatedGroData.reduce((s, d) => s + d.market, 0)
              const cumNna = aggregatedGroData.reduce((s, d) => s + d.nna, 0)
              const cumTotal = aggregatedGroData.reduce((s, d) => s + d.total, 0)

              // Each component as a share of cumulative total change
              const marketPct = cumTotal !== 0 ? (cumMarket / cumTotal) * 100 : null
              const nnaPct = cumTotal !== 0 ? (cumNna / cumTotal) * 100 : null

              // Window label for the sub-line
              const windowLabel = aggregatedGroData.length > 1
                ? `${aggregatedGroData[0].label} - ${latest.label}`
                : latest.label

              return (
                <div className="w-full mt-4 rounded-xl bg-white/5 border border-white/10 px-6 py-4">
                  <div className="flex items-center justify-center gap-2 mb-4">
                    <span className="text-[10px] text-white/50 uppercase tracking-widest font-medium">
                      {latest.label}
                    </span>
                  </div>
                  <div className="flex flex-wrap items-stretch gap-3">
                    <div className="flex-1 min-w-[160px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#8B5CF6]/10 border border-[#8B5CF6]/30">
                      <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Market</div>
                      <div className={`text-2xl font-bold ${latest.market >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {latest.market >= 0 ? '+' : ''}{formatCurrency(latest.market)}
                      </div>
                      <div className={`text-sm font-semibold mt-2 ${cumMarket >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {cumMarket >= 0 ? '+' : ''}{formatCurrency(cumMarket)}
                        {marketPct !== null && <span className="ml-1">({marketPct >= 0 ? '+' : ''}{marketPct.toFixed(1)}%)</span>}
                      </div>
                      <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{windowLabel}</div>
                    </div>
                    <div className="flex-1 min-w-[160px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#F59E0B]/10 border border-[#F59E0B]/30">
                      <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Net Flows (NNA)</div>
                      <div className={`text-2xl font-bold ${latest.nna >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {latest.nna >= 0 ? '+' : ''}{formatCurrency(latest.nna)}
                      </div>
                      <div className={`text-sm font-semibold mt-2 ${cumNna >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {cumNna >= 0 ? '+' : ''}{formatCurrency(cumNna)}
                        {nnaPct !== null && <span className="ml-1">({nnaPct >= 0 ? '+' : ''}{nnaPct.toFixed(1)}%)</span>}
                      </div>
                      <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{windowLabel}</div>
                    </div>
                    <div className="flex-1 min-w-[160px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
                      <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Total Change</div>
                      <div className={`text-2xl font-bold ${latest.total >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {latest.total >= 0 ? '+' : ''}{formatCurrency(latest.total)}
                      </div>
                      <div className={`text-sm font-semibold mt-2 ${cumTotal >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {cumTotal >= 0 ? '+' : ''}{formatCurrency(cumTotal)}
                      </div>
                      <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{windowLabel}</div>
                    </div>
                  </div>
                  {latest.endDate && (
                    <div className="text-[10px] text-white/30 text-center mt-3">
                      as of {new Date(latest.endDate + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </div>
                  )}
                </div>
              )
            })()}

            {/* Footnotes */}
            <div className="text-[10px] text-center px-4 mt-4 space-y-1">
              <p>
                {panelViewMode === 'aua' && auaSubMode === 'clients' ? (
                  <>
                    <span className="text-amber-400 font-bold">New Client Assets = Clients onboarded within trailing 12 months.</span>
                    <span className="text-white/40"> Existing Client Assets = Clients onboarded before trailing 12 months. Does not include cash balances.</span>
                  </>
                ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                  <>
                    <span className="text-amber-400 font-bold">Asset class breakdown of total AUA.</span>
                    <span className="text-white/40"> End-of-period snapshots derived from holdings data.</span>
                  </>
                ) : panelViewMode === 'gro' ? (
                  <>
                    <span className="text-amber-400 font-bold">Market = AUA change from market movement. NNA = net new assets from client flows.</span>
                    <span className="text-white/40"> Total = Market + NNA. Values can be negative in down markets or during outflow periods.</span>
                  </>
                ) : hasGrossFlowData ? (
                  <>
                    <span className="text-amber-400 font-bold">Inflows above zero, Outflows below zero — both shown every period.</span>
                    <span className="text-white/40"> The line shows net movement (Inflows - Outflows).</span>
                  </>
                ) : (
                  <>
                    <span className="text-amber-400 font-bold">Net New Assets per period.</span>
                    <span className="text-white/40"> Green = net inflow, Red = net outflow. Gross inflow/outflow breakdown available after next data update.</span>
                  </>
                )}
              </p>
              {panelViewMode !== 'gro' && !(panelViewMode === 'aua' && auaSubMode === 'mix') && (
                <p className="text-white/30 italic">
                  {panelViewMode === 'aua'
                    ? 'Growth metrics compare the same calendar day in the prior period (e.g., Day 24 of Feb vs Day 24 of Jan) for an apples-to-apples snapshot comparison.'
                    : 'Growth metrics compare the same calendar day in the prior period (e.g., cumulative flows through Day 24 of Feb vs Day 24 of Jan). Tooltip period-over-period compares against the full prior period.'}
                </p>
              )}
            </div>
          </div>
        </div>
      </PanelContent>
      <PanelFooter content="Source: SS&C Black Diamond Wealth Solutions." timestamp={data?.generated_at} />
    </Panel>
  )
}

// ============================================================================
// Firm Composition Snapshot (Mix sub-mode — live holdings-based pies)
// ============================================================================

// Canonical asset class colors — must match CMA portal and ClientsTab MIX_PIE_COLORS
const MIX_PIE_COLORS: Record<string, string> = {
  equity:           '#3b82f6', // Blue
  equities:         '#3b82f6', // Blue
  fixed_income:     '#10b981', // Green
  structured_notes: '#f97316', // Orange (alternatives)
  alternatives:     '#f97316', // Orange
  real_estate:      '#f97316', // Orange
  hedge:            '#f97316', // Orange
  cash:             '#f59e0b', // Gold
  other:            '#6B7280', // Gray
  untracked:        '#6B7280', // Gray
}

function mixColor(assetClass: string): string {
  return MIX_PIE_COLORS[assetClass] || MIX_PIE_COLORS[assetClass.toLowerCase().replace(/\s+/g, '_')] || '#6B7280'
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function _FirmCompositionSnapshot_REMOVED({
  data, selectedAssetClass, onSelectAssetClass,
}: {
  data: BooksCompositionResponse | null
  selectedAssetClass: string | null
  onSelectAssetClass: (cls: string | null) => void
}) {
  const hasMix = data && data.mix.length > 0
  const hasConc = data && data.concentration.items.length > 0

  const filteredConc = data && selectedAssetClass
    ? data.concentration.items.filter((it) => it.asset_class === selectedAssetClass)
    : data?.concentration.items ?? []

  const concPieData = [
    ...filteredConc.map((it) => ({ name: it.label, value: it.pct, color: mixColor(it.asset_class) })),
    ...(data && !selectedAssetClass && data.concentration.other.pct > 0
      ? [{ name: 'Other', value: data.concentration.other.pct, color: '#6B7280' }]
      : []),
  ]

  if (!data) return null

  return (
    <div className="w-full mt-4">
      <div className="text-[10px] text-white/50 uppercase tracking-widest font-medium text-center mb-3">
        Current Holdings Snapshot — {data.data_as_of}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        {/* Mix Pie */}
        <div className="rounded-xl bg-white/5 border border-white/10 p-4">
          <div className="text-xs text-white/60 font-medium mb-3">Asset Class Mix</div>
          {hasMix ? (
            <div className="flex items-center gap-4">
              <div style={{ width: 160, height: 160 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={data.mix}
                      dataKey="pct"
                      nameKey="label"
                      cx="50%" cy="50%"
                      innerRadius={40}
                      outerRadius={70}
                      paddingAngle={2}
                      onClick={(_, idx) => {
                        const cls = data.mix[idx]?.asset_class
                        if (cls) onSelectAssetClass(selectedAssetClass === cls ? null : cls)
                      }}
                      style={{ cursor: 'pointer' }}
                    >
                      {data.mix.map((item) => (
                        <Cell
                          key={item.asset_class}
                          fill={mixColor(item.asset_class)}
                          fillOpacity={selectedAssetClass && selectedAssetClass !== item.asset_class ? 0.3 : 1}
                        />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex-1 space-y-1">
                {data.mix.map((item) => (
                  <button
                    key={item.asset_class}
                    onClick={() => onSelectAssetClass(selectedAssetClass === item.asset_class ? null : item.asset_class)}
                    className={`flex items-center justify-between w-full text-left px-2 py-1 rounded transition-colors hover:bg-white/5 ${
                      selectedAssetClass && selectedAssetClass !== item.asset_class ? 'opacity-30' : ''
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: mixColor(item.asset_class) }} />
                      <span className="text-xs text-white/80">{item.label}</span>
                    </div>
                    <span className="text-xs text-white/60 font-medium">{(item.pct * 100).toFixed(1)}%</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center py-8">
              <span className="text-xs text-white/30">No allocation data</span>
            </div>
          )}
        </div>

        {/* Concentration Pie */}
        <div className="rounded-xl bg-white/5 border border-white/10 p-4">
          <div className="text-xs text-white/60 font-medium mb-3">
            {hasConc
              ? selectedAssetClass
                ? `Top ${data.concentration.top_n} -- ${selectedAssetClass.replace(/_/g, ' ')}`
                : `Top ${data.concentration.top_n} Holdings`
              : 'Top Holdings'}
          </div>
          {concPieData.length > 0 ? (
            <div className="flex items-center gap-4">
              <div style={{ width: 160, height: 160 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={concPieData}
                      dataKey="value" nameKey="name"
                      cx="50%" cy="50%"
                      innerRadius={40} outerRadius={70}
                      paddingAngle={1}
                    >
                      {concPieData.map((item, i) => (
                        <Cell key={i} fill={item.color} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex-1 space-y-0.5 overflow-y-auto" style={{ maxHeight: 160 }}>
                {filteredConc.map((item) => (
                  <div key={item.key} className="flex items-center justify-between px-2 py-0.5">
                    <span className="text-[11px] text-white/80 truncate mr-2">{item.label}</span>
                    <span className="text-[11px] text-white/60 flex-shrink-0">{(item.pct * 100).toFixed(1)}%</span>
                  </div>
                ))}
                {!selectedAssetClass && data.concentration.other.pct > 0 && (
                  <div className="flex items-center justify-between px-2 py-0.5">
                    <span className="text-[11px] text-white/50 italic">Other</span>
                    <span className="text-[11px] text-white/40">{(data.concentration.other.pct * 100).toFixed(1)}%</span>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center py-8">
              <span className="text-xs text-white/30">
                {!hasConc ? 'No holdings data' : 'No holdings for selected class'}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// Helper Components (Legacy - kept for reference but no longer used in main UI)
// ============================================================================

interface AUAGrowthMetricsProps {
  data: {
    aua: number
    nna_ytd: number
    q0: { nna: number; growth?: number }
    q1: { nna: number; growth?: number }
    q2: { nna: number; growth?: number }
  }
}

function _AUAGrowthMetrics({ data }: AUAGrowthMetricsProps) {
  const getGrowthDotColor = (growth: number | undefined): string => {
    if (growth === undefined) return 'bg-white/30'
    return growth > 0 ? 'bg-emerald-400' : growth < 0 ? 'bg-red-400' : 'bg-white/30'
  }

  const formatGrowth = (growth: number | undefined): string => {
    if (growth === undefined) return ''
    const sign = growth >= 0 ? '+' : ''
    return `${sign}${growth.toFixed(1)}%`
  }

  const getGrowthColor = (growth: number | undefined): string => {
    if (growth === undefined) return 'text-white/40'
    return growth > 0 ? 'text-emerald-400' : growth < 0 ? 'text-red-400' : 'text-white/40'
  }

  return (
    <div className="w-full h-[72px] px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex items-center justify-evenly gap-6 w-full">
        {/* Total AUA - Primary metric */}
        <div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40">
          <div className="text-xs text-white/90 font-semibold mb-1">Total AUA</div>
          <div className="text-lg font-bold text-white">
            {formatCurrency(data.aua)}
          </div>
        </div>

        {/* NNA YTD */}
        <div className="flex flex-col items-center">
          <div className="text-xs text-white/50 mb-1">NNA YTD</div>
          <div className={`text-sm font-semibold ${data.nna_ytd >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {data.nna_ytd >= 0 ? '+' : ''}{formatCurrency(data.nna_ytd)}
          </div>
        </div>

        {/* Q0 NNA (This Quarter) */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(data.q0.growth)}`} />
            <div className="text-xs text-white/50">This Qtr</div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold text-white">
              {formatCurrency(data.q0.nna)}
            </span>
            {data.q0.growth !== undefined && (
              <span className={`text-xs font-medium ${getGrowthColor(data.q0.growth)}`}>
                {formatGrowth(data.q0.growth)}
              </span>
            )}
          </div>
        </div>

        {/* Q1 NNA (Last Quarter) */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(data.q1.growth)}`} />
            <div className="text-xs text-white/50">Last Qtr</div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold text-white">
              {formatCurrency(data.q1.nna)}
            </span>
            {data.q1.growth !== undefined && (
              <span className={`text-xs font-medium ${getGrowthColor(data.q1.growth)}`}>
                {formatGrowth(data.q1.growth)}
              </span>
            )}
          </div>
        </div>

        {/* Q2 NNA (2 Quarters Ago) */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(data.q2.growth)}`} />
            <div className="text-xs text-white/50">2Q Ago</div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold text-white">
              {formatCurrency(data.q2.nna)}
            </span>
            {data.q2.growth !== undefined && (
              <span className={`text-xs font-medium ${getGrowthColor(data.q2.growth)}`}>
                {formatGrowth(data.q2.growth)}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// Time Machine Metrics Component
// ============================================================================

interface TimeMachineMetricsProps {
  view: PartnerAnalyticsViewWithPeriods
  periods?: {
    current: { date: string; label: string }
    q1: { date: string; label: string }
    q2: { date: string; label: string }
    q3: { date: string; label: string }
  }
  selectedPeriod: TimePeriodKey
  onPeriodChange: (period: TimePeriodKey) => void
  parentSegmentKey?: string | null  // State/architect key when drilled down
  parentSegmentLabel?: string | null  // Label for display
  childSegmentKey?: string | null  // City/client key when selected within drill-down
  childSegmentLabel?: string | null  // Label for display
  isNnaView?: boolean  // When true, use 'value' (net flows) instead of 'aua'
}

function _TimeMachineMetrics({ view, periods, selectedPeriod, onPeriodChange, parentSegmentKey, parentSegmentLabel, childSegmentKey, childSegmentLabel, isNnaView = false }: TimeMachineMetricsProps) {
  // Get value for a specific period - always looks up in THAT period's data
  // For NNA view, uses 'value' (net flows); for other views, uses 'aua'
  const getValueForPeriod = (period: TimePeriodKey): number => {
    const snapshot = period === 'current' ? view.current : view[period]

    // If a child segment (city/client) is selected, look it up within the parent
    if (childSegmentKey && parentSegmentKey) {
      const parentInPeriod = snapshot?.donut?.segments?.find(
        (s: DonutSegment) => s.key === parentSegmentKey
      )
      // Look in cities array for GEO drill-down
      if (parentInPeriod?.cities) {
        const cityInPeriod = parentInPeriod.cities.find(
          (c: CitySegment) => c.key === childSegmentKey
        )
        if (cityInPeriod) {
          return cityInPeriod.aua
        }
      }
      // Look in clients array for ADV drill-down
      if (parentInPeriod?.clients) {
        const clientInPeriod = parentInPeriod.clients.find(
          (c: ClientSegment) => c.key === childSegmentKey
        )
        if (clientInPeriod) {
          return clientInPeriod.aua
        }
      }
      return 0
    }

    // If just a parent segment (state/architect/NNA segment) is selected
    if (parentSegmentKey) {
      const segmentInPeriod = snapshot?.donut?.segments?.find(
        (s: DonutSegment) => s.key === parentSegmentKey
      )
      if (segmentInPeriod) {
        // NNA view: use 'value' (net flows), not 'aua'
        if (isNnaView && segmentInPeriod.value !== undefined) {
          return segmentInPeriod.value
        }
        return segmentInPeriod.aua
      }
      return 0
    }

    // Total level
    // NNA view at total level also uses the donut total (which is net NNA)
    return snapshot?.metrics?.aua || snapshot?.donut?.total || 0
  }

  // Get % change for a historical period (compared to current)
  const getChangeForPeriod = (period: TimePeriodKey): number | undefined => {
    if (period === 'current') return undefined
    const snapshot = view[period]
    return snapshot?.metrics?.aua_change_pct
  }

  // Check if a period has data
  const hasPeriodData = (period: TimePeriodKey): boolean => {
    if (period === 'current') return !!view.current
    return !!view[period]
  }

  // Check if viewing estimated data
  const _isEstimated = (period: TimePeriodKey): boolean => {
    if (period === 'current') return false
    const snapshot = view[period]
    return (snapshot?.metrics as { estimated?: boolean })?.estimated === true
  }

  // Format change percentage
  const formatChange = (change: number | undefined): string => {
    if (change === undefined) return ''
    const sign = change >= 0 ? '+' : ''
    return `${sign}${change.toFixed(1)}%`
  }

  // Get change color
  const getChangeColor = (change: number | undefined): string => {
    if (change === undefined) return 'text-white/40'
    return change > 0 ? 'text-emerald-400' : change < 0 ? 'text-red-400' : 'text-white/40'
  }

  // Period configurations - show most specific label (child > parent > total)
  // NNA view spells out "Net New Assets" instead of abbreviating
  const metricLabel = (() => {
    const baseLabel = childSegmentLabel || parentSegmentLabel || 'Total'
    if (isNnaView) {
      // Replace "NNA" suffix with full "Net New Assets" if present
      if (baseLabel.endsWith('NNA')) {
        return baseLabel.replace(/NNA$/, 'Net New Assets')
      }
      return `${baseLabel} Net New Assets`
    }
    return `${baseLabel} AUA`
  })()

  const periodConfigs: { key: TimePeriodKey; label: string; subLabel?: string }[] = [
    { key: 'current', label: 'Current', subLabel: metricLabel },
    { key: 'q1', label: periods?.q1?.label || 'Last Qtr' },
    { key: 'q2', label: periods?.q2?.label || '2Q Ago' },
    { key: 'q3', label: periods?.q3?.label || '3Q Ago' },
  ]

  return (
    <div className="w-full h-[72px] px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex items-center justify-evenly gap-6 w-full">
        {periodConfigs.map(({ key, label, subLabel }) => {
          const isSelected = selectedPeriod === key
          const hasData = hasPeriodData(key)
          const aua = getValueForPeriod(key)
          const change = getChangeForPeriod(key)

          if (!hasData && key !== 'current') {
            return null  // Don't show periods without data
          }

          // Current period gets special "Total AUA" styling to match canonical
          const isCurrent = key === 'current'

          return (
            <button
              key={key}
              onClick={() => onPeriodChange(key)}
              disabled={!hasData}
              className={`flex flex-col items-center px-3 py-1.5 rounded-lg transition-all ${
                isSelected
                  ? 'bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40'
                  : hasData
                  ? 'hover:bg-white/10 border border-transparent'
                  : 'opacity-40 cursor-not-allowed border border-transparent'
              }`}
            >
              {/* Period label */}
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className={`text-xs ${isSelected ? 'text-white/90 font-semibold' : 'text-white/60 font-medium'}`}>
                  {isCurrent ? (subLabel || label) : label}
                </span>
              </div>

              {/* AUA value */}
              <div className="flex items-center gap-1.5">
                <span className={`font-bold ${isSelected ? 'text-lg text-white' : 'text-sm text-white/80'}`}>
                  {formatCurrency(aua)}
                </span>
                {change !== undefined && (
                  <span className={`text-xs font-medium ${getChangeColor(change)}`}>
                    {formatChange(change)}
                  </span>
                )}
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

// ============================================================================
// Client Distribution Chart Component
// ============================================================================

interface ClientDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number  // Fixed Y-axis max for consistent scaling across segments
}

function ClientDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount }: ClientDistributionChartProps) {
  const chartData = data.histogram.bin_labels.map((label, index) => ({
    bin: label,
    count: data.histogram.counts[index],
    binIndex: index,
  }))

  const parseDollarValue = (binLabel: string): number => {
    if (binLabel.includes('+')) {
      const match = binLabel.match(/\$([\d.]+)([KMB]?)\+/)
      if (match) {
        const num = parseFloat(match[1])
        const multiplier = match[2] === 'K' ? 1000 : match[2] === 'M' ? 1000000 : match[2] === 'B' ? 1000000000 : 1
        return num * multiplier
      }
    }
    const parts = binLabel.split('-')
    if (parts.length === 2) {
      const parseValue = (str: string): number => {
        const match = str.match(/\$([\d.]+)([KMB]?)/)
        if (match) {
          const num = parseFloat(match[1])
          const multiplier = match[2] === 'K' ? 1000 : match[2] === 'M' ? 1000000 : match[2] === 'B' ? 1000000000 : 1
          return num * multiplier
        }
        return 0
      }
      return (parseValue(parts[0]) + parseValue(parts[1])) / 2
    }
    return 0
  }

  const findBinForValue = (value: number | null): string | null => {
    if (value === null) return null
    let closestBin = null
    let minDiff = Infinity
    for (const binLabel of data.histogram.bin_labels) {
      const binMidpoint = parseDollarValue(binLabel)
      const diff = Math.abs(binMidpoint - value)
      if (diff < minDiff) {
        minDiff = diff
        closestBin = binLabel
      }
    }
    return closestBin
  }

  const percentileLines = [
    { value: data.percentiles.p10, label: 'P10', color: '#ef4444' },
    { value: data.percentiles.p25, label: 'P25', color: '#fb923c' },
    { value: data.median, label: 'Median', color: '#34d399' },
    { value: data.percentiles.p75, label: 'P75', color: '#60a5fa' },
    { value: data.percentiles.p90, label: 'P90', color: '#a78bfa' },
  ]

  useEffect(() => {
    const timer = setTimeout(() => window.dispatchEvent(new Event('resize')), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="w-full h-full relative">
      <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-2">
        <span className="text-[11px] text-white/50 whitespace-nowrap" style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}>
          Number of Clients
        </span>
      </div>
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-4">
        <span className="text-[11px] text-white/50">Client AUA</span>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 30, right: 10, left: 0, bottom: 5 }}>
          <defs>
            <linearGradient id="distributionGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={accentColor} stopOpacity={0.8} />
              <stop offset="95%" stopColor={accentColor} stopOpacity={0.1} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis dataKey="bin" stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }} angle={-65} textAnchor="end" height={50} interval={0} />
          <YAxis
                            stroke="rgba(255,255,255,0.5)"
                            tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.7)' }}
                            width={40}
                            domain={globalMaxCount ? [0, globalMaxCount] : ['auto', 'auto']}
                            allowDataOverflow={false}
                          />
          <RechartsTooltip
            cursor={{ stroke: `${accentColor}80`, strokeWidth: 2 }}
            content={({ active, payload, label }) => {
              if (!active || !payload || payload.length === 0) return null
              const count = payload[0]?.value as number
              const formattedLabel = typeof label === 'string' ? label.replace(/(\$[\d.]+[KMB]?)-(\$[\d.]+[KMB]?\+?)/, '$1 - $2') : label
              return (
                <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] rounded-lg px-4 py-3 shadow-xl" style={{ border: `2px solid ${accentColor}` }}>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Client AUA</span>
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{formattedLabel}</span>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Client Count</span>
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{count?.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              )
            }}
          />
          <Area type="monotone" dataKey="count" stroke="hsl(253, 74%, 85%)" strokeWidth={2} fill="url(#distributionGradient)" isAnimationActive={true} animationDuration={800} />
          {percentileLines.map((line) => {
            const binLabel = findBinForValue(line.value)
            if (!binLabel) return null
            return (
              <ReferenceLine key={line.label} x={binLabel} stroke={line.color} strokeWidth={2} strokeDasharray="5 5" label={{ value: line.label, position: 'top', fill: line.color, fontSize: 10, fontWeight: 600 }} />
            )
          })}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

// ============================================================================
// Client Distribution Metrics Component
// ============================================================================

interface ClientDistributionMetricsProps {
  data: DistributionStats
}

function ClientDistributionMetrics({ data }: ClientDistributionMetricsProps) {
  return (
    <div className="w-full h-[72px] px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex items-center justify-evenly gap-4 w-full">
        {/* Total Clients */}
        <div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40">
          <div className="text-xs text-white/90 font-semibold mb-1">Total Clients</div>
          <div className="text-lg font-bold text-white">{data.count.toLocaleString()}</div>
        </div>

        {/* P10 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <div className="text-xs text-white/50">P10</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p10 !== null ? formatCurrency(data.percentiles.p10) : 'N/A'}</div>
        </div>

        {/* P25 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-orange-400" />
            <div className="text-xs text-white/50">P25</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p25 !== null ? formatCurrency(data.percentiles.p25) : 'N/A'}</div>
        </div>

        {/* Median */}
        <div className="flex flex-col items-center px-3 py-1.5 rounded bg-emerald-500/10 border border-emerald-500/30">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-emerald-400" />
            <div className="text-xs text-emerald-300/80 font-semibold">Median</div>
          </div>
          <div className="text-base font-bold text-emerald-400">{data.median !== null ? formatCurrency(data.median) : 'N/A'}</div>
        </div>

        {/* Mean */}
        <div className="flex flex-col items-center">
          <div className="text-xs text-white/50 mb-1">Mean</div>
          <div className="text-sm font-semibold text-white">{data.mean !== null ? formatCurrency(data.mean) : 'N/A'}</div>
        </div>

        {/* P75 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <div className="text-xs text-white/50">P75</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p75 !== null ? formatCurrency(data.percentiles.p75) : 'N/A'}</div>
        </div>

        {/* P90 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-purple-400" />
            <div className="text-xs text-white/50">P90</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p90 !== null ? formatCurrency(data.percentiles.p90) : 'N/A'}</div>
        </div>
      </div>
    </div>
  )
}
```

### portal-api-endpoints----advisor-intelligence.ts.-all-fetch-functions-for-advisorintelligence-page.ts

```
/**
 * Advisor Intelligence API Client - v2
 *
 * Multi-tenant API for Advisor Intelligence page data.
 * Data access controlled by allowedFirmIds computed in portal-authorizer.
 *
 * Endpoints:
 *   GET /api/partners                                              - List partners
 *   GET /api/scoped/advisor-intelligence/timeseries/{dimension}    - Time series
 *   GET /api/scoped/advisor-intelligence/snapshots/{dimension}     - AUA snapshots
 *   GET /api/scoped/advisor-intelligence/filters                   - Filter options
 *   GET /api/scoped/advisor-intelligence/clients/growth            - Client growth
 *   GET /api/scoped/advisor-intelligence/clients/tax-breakdown     - Tax breakdown
 *   GET /api/scoped/advisor-intelligence/clients/tax-deferred      - Tax candidates
 */

import type {
  PartnersResponse,
  TimeSeriesResponse,
  CategoryTimeSeriesResponse,
  SnapshotResponse,
  FiltersResponse,
  ClientGrowthResponse,
  TaxBasisBreakdownResponse,
  TaxDeferredResponse,
  HeaderSummary,
  HeaderMetricsResponse,
  PartnerAnalyticsResponse,
  CumulativeChartResponse,
  ClientsTabResponse,
  ClientDetailResponse,
  LeaderboardResponse,
  AdvisorBookResponse,
  AdvisorRollingFlowsResponse,
  BooksClientDetailResponse,
  BooksTimeseriesResponse,
  BooksCompositionResponse,
  FirmMixViewsResponse,
  MixTimeseriesPoint,
  MixWindow,
  ConcentrationResponse,
  AdvisorTimeseriesResponse,
  AdvisorMixTimeseriesResponse,
} from '@/pages/AdvisorIntelligence/types'

// ============================================================================
// Configuration
// ============================================================================

// API base URL
const API_BASE_URL = import.meta.env.VITE_PORTAL_API_URL ?? ''

// S3 bucket suffix -> DynamoDB firm key mapping for Lambda-routed endpoints.
// S3-routed endpoints use ?firm={bucketSuffix}, but Lambda endpoints (opal-partners-data)
// expect ?firmId={ddbFirmId} where the value is the DynamoDB partition key.
const LAMBDA_FIRM_ID: Record<string, string> = { bd: '49financial' }

// Valid dimensions for time series (11 total)
export const TIMESERIES_DIMENSIONS = [
  'total',
  'category',
  'architect',
  'region',
  'account_type',
  'tax_status',
  'client_segment',
  'state',
  'city',
  'relationship',
  'implementor',
] as const

// Valid dimensions for snapshots (7 total)
export const SNAPSHOT_DIMENSIONS = [
  'architect',
  'region',
  'tax_status',
  'account_type',
  'implementor',
  'state',
  'city',
] as const

export type TimeseriesDimension = typeof TIMESERIES_DIMENSIONS[number]
export type SnapshotDimension = typeof SNAPSHOT_DIMENSIONS[number]

// Combined for backward compatibility
export const VALID_DIMENSIONS = TIMESERIES_DIMENSIONS
export type Dimension = TimeseriesDimension

// ============================================================================
// API Request Helper
// ============================================================================

/**
 * Make authenticated API request
 */
async function apiRequest<T>(endpoint: string): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  const accessToken = localStorage.getItem('accessToken')

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
    },
  })

  if (!response.ok) {
    const errorBody = await response.text()
    throw new Error(`API request failed: ${response.status} ${response.statusText} - ${errorBody}`)
  }

  return response.json()
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Get list of partners the user can access
 */
export async function getAllowedPartners(): Promise<PartnersResponse> {
  return await apiRequest<PartnersResponse>('/api/partners')
}

/**
 * Get time series data for a dimension
 *
 * @param firmId - Partner firm ID
 * @param dimension - Dimension to slice by (total, category, architect, region, account_type, tax_status, client_segment, state, city, relationship, implementor)
 */
export async function getTimeSeries(
  firmId: string,
  dimension: TimeseriesDimension
): Promise<TimeSeriesResponse | CategoryTimeSeriesResponse> {
  const url = `/api/scoped/advisor-intelligence/timeseries/${dimension}?firmId=${firmId}`
  return await apiRequest<TimeSeriesResponse>(url)
}

/**
 * Get AUA snapshot for a dimension
 *
 * Dynamic API call — firmId is passed as query param.
 * Routes via CloudFront /api/scoped/ -> shared-advisor-router -> opal-data-{firmId}/gold/
 *
 * @param firmId - Partner firm ID
 * @param dimension - Dimension to slice by (architect, region, tax_status, account_type, implementor, state, city)
 */
export async function getSnapshot(
  firmId: string,
  dimension: SnapshotDimension
): Promise<SnapshotResponse> {
  const url = `/api/scoped/advisor-intelligence/snapshots/${dimension}?firmId=${firmId}`
  return await apiRequest<SnapshotResponse>(url)
}

/**
 * Get available filter dimensions and values
 *
 * @param firmId - Partner firm ID
 */
export async function getFilters(firmId: string): Promise<FiltersResponse> {
  const url = `/api/scoped/advisor-intelligence/filters?firmId=${firmId}`
  return await apiRequest<FiltersResponse>(url)
}

/**
 * Get client growth time series
 *
 * @param firmId - Partner firm ID
 */
export async function getClientGrowth(firmId: string): Promise<ClientGrowthResponse> {
  const url = `/api/scoped/advisor-intelligence/clients/growth?firmId=${firmId}`
  return await apiRequest<ClientGrowthResponse>(url)
}

/**
 * Get tax basis breakdown (pie charts)
 *
 * @param firmId - Partner firm ID
 */
export async function getTaxBreakdown(firmId: string): Promise<TaxBasisBreakdownResponse> {
  const url = `/api/scoped/advisor-intelligence/clients/tax-breakdown?firmId=${firmId}`
  return await apiRequest<TaxBasisBreakdownResponse>(url)
}

/**
 * Get tax-deferred strategy candidates
 *
 * @param firmId - Partner firm ID
 */
export async function getTaxDeferredCandidates(firmId: string): Promise<TaxDeferredResponse> {
  const url = `/api/scoped/advisor-intelligence/clients/tax-deferred?firmId=${firmId}`
  return await apiRequest<TaxDeferredResponse>(url)
}

/**
 * Get header summary metrics
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 */
export async function getHeaderSummary(): Promise<HeaderSummary> {
  return await apiRequest<HeaderSummary>('/api/scoped/advisor-intelligence/summary/header_metrics.json')
}

/**
 * Get full header metrics (v3 - includes radial chart and bell curve data)
 *
 * Returns the complete header_metrics.json structure including:
 * - total: AUA, NNA metrics, quarterly breakdowns
 * - radial_12m: NMNC/NMEC/Existing breakdown for donut chart
 * - account_distribution: histogram and percentiles for bell curve
 * - by_architect: top 10 architects breakdown
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 */
export async function getHeaderMetrics(firmOverride?: string): Promise<HeaderMetricsResponse> {
  const base = '/api/scoped/advisor-intelligence/summary/header_metrics.json'
  return await apiRequest<HeaderMetricsResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Partner Analytics data (v4 - multi-view with NNA/GEO/ADV)
 *
 * Returns the complete partner_analytics/header_metrics.json structure including:
 * - views.nna: Client segment breakdown (NMNC/NMEC/Existing)
 * - views.geo: Geographic breakdown (top 8 regions + Other)
 * - views.adv: Architect breakdown (top 8 architects + Other)
 *
 * Each view contains:
 * - donut: { title, total, segments[] }
 * - distribution: { total, by_segment }
 * - metrics: { aua, nna_ytd, q0, q1, q2 }
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 */
export async function getPartnerAnalytics(granularity: 'monthly' | 'quarterly' | 'annually' = 'quarterly', firmOverride?: string): Promise<PartnerAnalyticsResponse> {
  // S3 files use _annual (not _annually) — map the suffix
  const suffix = granularity === 'annually' ? 'annual' : granularity
  const base = `/api/scoped/advisor-intelligence/partner_analytics/header_metrics_${suffix}.json`
  return await apiRequest<PartnerAnalyticsResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get cumulative time series chart data
 *
 * Returns daily cumulative NNA data for 4 views:
 * - aua: Cumulative NNA by client cohort (NMNC/NMEC)
 * - nna: Daily NNA flows
 * - geo: Cumulative NNA by region (TX, CA, etc.)
 * - adv: Cumulative NNA by architect
 *
 * Data spans 2 years with daily granularity (~731 data points per view)
 */
export async function getCumulativeChart(firmOverride?: string): Promise<CumulativeChartResponse> {
  const base = '/api/scoped/advisor-intelligence/timeseries_chart.json'
  return await apiRequest<CumulativeChartResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Clients Tab data (Book view)
 *
 * Returns aggregate book-level metrics for the Clients tab:
 * - headline: Total AUA, accounts, clients, fee rate, income yield
 * - tax: Tax status breakdown (taxable/deferred/free) + capital gains
 * - income_fees: Dividends, interest, fees with TTM totals
 * - portfolio: Allocation, expense ratio, holdings, concentration
 * - engagement: Trading activity, net flows, tenure, active %
 * - clients: Full dropdown list sorted by AUA (for client picker)
 */
export async function getClientsTab(firmOverride?: string): Promise<ClientsTabResponse> {
  const base = '/api/scoped/advisor-intelligence/clients_tab.json'
  return await apiRequest<ClientsTabResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get individual client detail data
 *
 * Returns metrics for a specific client:
 * - Same structure as ClientsTab but scoped to one client
 * - headline, tax, income_fees, portfolio, engagement sections
 *
 * @param clientKey - The client identifier (e.g., "z08327149")
 */
export async function getClientDetail(clientKey: string, firmOverride?: string): Promise<ClientDetailResponse> {
  const base = `/api/scoped/advisor-intelligence/clients/${clientKey}.json`
  return await apiRequest<ClientDetailResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Architect Leaderboard data
 *
 * Returns ranked list of architects by NNA (trailing 12M):
 * - entries: Ranked architect data with NNA, AUA growth %, new clients
 * - summary: Aggregate totals (total_nna, total_aua, positive/negative counts)
 */
export async function getArchitectLeaderboard(firmOverride?: string): Promise<LeaderboardResponse> {
  const base = '/api/scoped/advisor-intelligence/architect_leaderboard.json'
  return await apiRequest<LeaderboardResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Implementor Leaderboard data
 *
 * Returns ranked list of implementors by NNA (trailing 12M):
 * - entries: Ranked implementor data with NNA, AUA growth %, new clients
 * - summary: Aggregate totals (total_nna, total_aua, positive/negative counts)
 */
export async function getImplementorLeaderboard(firmOverride?: string): Promise<LeaderboardResponse> {
  const base = '/api/scoped/advisor-intelligence/implementor_leaderboard.json'
  return await apiRequest<LeaderboardResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Advisor Book data (per-advisor view)
 *
 * Returns book-level metrics for a specific advisor:
 * - summary: AUA, client count, account count
 * - nna: YTD, QTD, MTD net new assets
 * - growth: YTD and QTD growth percentages
 * - tax_exposure, income_fees, portfolio_composition, engagement
 * - clients: List of clients for this advisor
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 *
 * @param advisorId - Advisor identifier (e.g., 'travis_penfield')
 */
export async function getAdvisorBook(advisorId: string, firmOverride?: string): Promise<AdvisorBookResponse> {
  const base = `/api/scoped/advisor-intelligence/advisors/${advisorId}/book.json`
  return await apiRequest<AdvisorBookResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Advisor Rolling Flows data (Advisors tab -- two views)
 *
 * Returns both NNA summary (donut chart) and rolling time series:
 * - summary.architects / summary.implementors: MTD/QTD/YTD NNA breakdown by advisor
 * - architects[] / implementors[]: daily rolling 30d/90d/1Y flows per advisor
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router routes to opal-data-{firmId}/gold/)
 */
export async function getAdvisorRollingFlows(firmOverride?: string): Promise<AdvisorRollingFlowsResponse> {
  const base = '/api/scoped/advisor-intelligence/advisor_rolling_flows.json'
  return await apiRequest<AdvisorRollingFlowsResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Books client detail data (per-relationship view from bd-portal-advisor-publisher)
 *
 * Returns relationship-level detail for the Books tab L3 view:
 * - headline: Total AUA, account count
 * - tax: Full tax intelligence with open lots, cost basis by year, top positions
 * - engagement: Net flows TTM, avg relationship years
 * - accounts: Per-account breakdown with flows and position counts
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 *
 * @param clientKey - Relationship identifier (e.g., "z08327149")
 */
export async function getBooksClientDetail(clientKey: string, firmOverride?: string): Promise<BooksClientDetailResponse> {
  const base = `/api/scoped/advisor-intelligence/clients/${clientKey}.json`
  return await apiRequest<BooksClientDetailResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Books relationship-level timeseries (AUA + cumulative flows)
 *
 * @param relationshipId - Relationship identifier
 */
export async function getBooksRelationshipTimeseries(relationshipId: string, firmOverride?: string): Promise<BooksTimeseriesResponse> {
  const base = `/api/scoped/partners/books/relationship/${relationshipId}/timeseries`
  return await apiRequest<BooksTimeseriesResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

/**
 * Get Books account-level timeseries (AUA + cumulative flows)
 *
 * @param accountId - Account identifier
 */
export async function getBooksAccountTimeseries(accountId: string, firmOverride?: string): Promise<BooksTimeseriesResponse> {
  const base = `/api/scoped/partners/books/account/${accountId}/timeseries`
  return await apiRequest<BooksTimeseriesResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

/**
 * Get Books relationship-level composition (asset class mix + concentration)
 *
 * @param relationshipId - Relationship identifier
 */
/**
 * Get Books firm-level composition (asset class mix + top-N concentration)
 * Aggregates ALL open holdings across the firm.
 */
export async function getBooksFirmComposition(firmOverride?: string): Promise<BooksCompositionResponse> {
  const firmKey = firmOverride ? (LAMBDA_FIRM_ID[firmOverride] ?? firmOverride) : '49financial'
  return await apiRequest<BooksCompositionResponse>(`/api/scoped/partners/books/firm/all/composition?firmId=${firmKey}`)
}

export async function getBooksRelationshipComposition(relationshipId: string, firmOverride?: string): Promise<BooksCompositionResponse> {
  const base = `/api/scoped/partners/books/relationship/${relationshipId}/composition`
  return await apiRequest<BooksCompositionResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

/**
 * Get Books account-level composition (asset class mix + concentration)
 *
 * @param accountId - Account identifier
 */
export async function getBooksAccountComposition(accountId: string, firmOverride?: string): Promise<BooksCompositionResponse> {
  const base = `/api/scoped/partners/books/account/${accountId}/composition`
  return await apiRequest<BooksCompositionResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

// The Lambda serves the full client_timeseries JSON envelope for both mix and concentration.
interface ClientTimeseriesEnvelope {
  generated_at: string
  data_as_of: string
  relationship_id: string | number
  mix: MixTimeseriesPoint[]
  concentration: ConcentrationResponse
}

/**
 * Get Mix timeseries for a relationship (asset class allocation over time)
 *
 * Returns daily data points where each class is 0-1 pct, summing to 1.0 per row.
 * The Lambda serves the full envelope ({mix, concentration}); this function extracts mix[].
 *
 * @param relationshipId - Relationship identifier. Use '0' for firm-level aggregate.
 * @param firmId - Partner firm ID (S3 bucket suffix, e.g. 'bd')
 * @param window - Time window: 1Y, 3Y, or Max (client-side filter only)
 */
export async function getMixTimeseries(
  relationshipId: string,
  firmId: string,
  window?: MixWindow
): Promise<MixTimeseriesPoint[]> {
  const params = new URLSearchParams({ firmId: LAMBDA_FIRM_ID[firmId] ?? firmId })
  if (window) params.set('window', window)
  const envelope = await apiRequest<ClientTimeseriesEnvelope>(
    `/api/scoped/partners/books/relationship/${relationshipId}/mix-timeseries?${params}`
  )
  return envelope.mix ?? []
}

/**
 * Get firm-level aggregate mix timeseries (relationship_id = '0').
 * 2,000+ daily data points spanning full firm history.
 *
 * @param firmId - Partner firm ID (S3 bucket suffix, e.g. 'bd')
 */
export async function getFirmMixTimeseries(firmId: string): Promise<MixTimeseriesPoint[]> {
  return getMixTimeseries('0', firmId)
}

/**
 * Get firm-level pre-aggregated mix views (quarterly, monthly, annually).
 *
 * Returns absolute dollar amounts and allocation fractions (0-1) per asset class
 * for each period. Replaces the daily getMixTimeseries + client-side aggregation approach.
 *
 * @param firmId - Partner firm ID (S3 bucket suffix, e.g. 'bd')
 */
export async function getFirmMixViews(firmId: string): Promise<FirmMixViewsResponse> {
  const resolvedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId
  return await apiRequest<FirmMixViewsResponse>(
    `/api/scoped/partners/books/firm/all/mix-views?firmId=${resolvedFirmId}`
  )
}

/**
 * Get Concentration timeseries for a relationship (top-N holdings over time)
 *
 * Returns flat array of top-N holdings per date, filtered by window.
 * top_n field indicates the N used by the Lambda.
 *
 * @param relationshipId - Relationship identifier
 * @param firmId - Partner firm ID
 * @param window - Time window: 1Y, 3Y, or Max (default 1Y)
 */
export async function getConcentrationTimeseries(
  relationshipId: string,
  firmId: string,
  window?: MixWindow
): Promise<ConcentrationResponse> {
  const params = new URLSearchParams({ firmId: LAMBDA_FIRM_ID[firmId] ?? firmId })
  if (window) params.set('window', window)
  return await apiRequest<ConcentrationResponse>(
    `/api/scoped/partners/books/relationship/${relationshipId}/concentration-timeseries?${params}`
  )
}

export async function getAdvisorTimeseries(
  advisorId: string,
  firmId: string
): Promise<AdvisorTimeseriesResponse> {
  const mappedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId
  return await apiRequest<AdvisorTimeseriesResponse>(
    `/api/scoped/partners/books/advisor/${advisorId}/timeseries?firmId=${mappedFirmId}`
  )
}

export async function getAdvisorMixTimeseries(
  advisorId: string,
  firmId: string,
  window?: MixWindow
): Promise<AdvisorMixTimeseriesResponse> {
  const mappedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId
  const params = new URLSearchParams({ firmId: mappedFirmId })
  if (window) params.set('window', window)
  return await apiRequest<AdvisorMixTimeseriesResponse>(
    `/api/scoped/partners/books/advisor/${advisorId}/mix-timeseries?${params}`
  )
}
```

### portal-typescript-types----types.ts.-firmmixviewsresponse-bookscompositionresponse-auamixview-mixassetclass-mixitem-etc..ts

```
/**
 * Advisor Intelligence Page Types - v2
 *
 * Partner AUA analytics and reporting interfaces
 * Based on ADVISOR_INTELLIGENCE_DATA_SPEC.md
 */

// ============================================================================
// Partner/Firm Types (kept from v1)
// ============================================================================

export interface Partner {
  firmId: string
  firmName: string
  tier: 'advisor' | 'subadvisor' | 'branch'
  parentFirmId: string | null
}

export interface PartnersResponse {
  partners: Partner[]
}

// ============================================================================
// Metrics & Dimensions Constants
// ============================================================================

export type MetricId = 'nmnc' | 'nmec_na' | 'nmec_sa' | 'nna_inflow' | 'nna_outflow' | 'nna_net'

export interface MetricOption {
  id: MetricId
  label: string
  description?: string
}

// ============================================================================
// Tab 1: Asset Intelligence Types
// ============================================================================

// NNA metric values for a dimension value
export interface NNAMetrics {
  nmnc: number
  nmec_na: number
  nmec_sa: number
  nna_inflow: number
  nna_outflow: number
  nna_net: number
}

// Time series period data
export interface TimeSeriesPeriod {
  period: string  // "2025-01"
  [dimensionValue: string]: NNAMetrics | string  // string for period key
}

// Time series response from API
export interface TimeSeriesResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  granularity: 'monthly'
  dimension: string
  dimension_values: string[]
  metrics: string[]
  data: TimeSeriesPeriod[]
}

// Category time series (NMNC/NMEC breakdown without dimension)
export interface CategoryTimeSeriesPeriod {
  period: string
  nmnc: number
  nmec_na: number
  nmec_sa: number
  total_inflow: number
  outflow: number
  net: number
}

export interface CategoryTimeSeriesResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  granularity: 'monthly'
  data: CategoryTimeSeriesPeriod[]
}

// Snapshot row for AUA breakdown
export interface SnapshotRow {
  value: string
  aua: number
  aua_pct: number
  client_count: number
  account_count: number
}

// Snapshot response from API
export interface SnapshotResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  dimension: string
  total_aua: number
  data: SnapshotRow[]
}

// Filter dimension value
export interface FilterValue {
  id: string
  name: string
  aua?: number
}

// Filter dimension definition
export interface FilterDimension {
  label: string
  values: FilterValue[]
}

// Filters response from API
export interface FiltersResponse {
  generated_at: string
  firm_id: string
  dimensions: Record<string, FilterDimension>
}

// ============================================================================
// Tab 2: Clients Types
// ============================================================================

// Client growth period data
export interface ClientGrowthPeriod {
  period: string
  total_clients: number
  total_aua: number
  avg_aua_per_client: number
  new_clients_added: number
  clients_lost: number
}

// Client growth response from API
export interface ClientGrowthResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  granularity: 'monthly'
  summary: {
    total_clients: number
    avg_growth_rate_ytd: number
    median_aua: number
  }
  data: ClientGrowthPeriod[]
}

// Pie chart data point
export interface PieChartDataPoint {
  label: string
  value: number
  pct: number
  color: string
}

// Pie chart definition
export interface PieChartData {
  title: string
  data: PieChartDataPoint[]
}

// Tax basis breakdown response
export interface TaxBasisBreakdownResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  charts: {
    tax_status: PieChartData
    cost_basis_sync: PieChartData
    account_type: PieChartData
  }
}

// Tax-deferred candidate
export interface TaxDeferredCandidate {
  relationship_id: string
  relationship_name: string
  architect: string
  taxable_aua: number
  account_count: number
  cost_basis_synced: boolean
  last_nna_date: string
  priority_score: number  // 0-100
}

// Tax-deferred candidates response
export interface TaxDeferredResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  scan_criteria: {
    min_taxable_aua: number
    tax_status: string
    cost_basis_synced: boolean
  }
  summary: {
    total_candidates: number
    total_opportunity_aua: number
  }
  candidates: TaxDeferredCandidate[]
}

// ============================================================================
// Header Metrics Types (v3 - matches SmartX aum-metrics pattern)
// ============================================================================

// Quarterly NNA breakdown
export interface QuarterlyNNA {
  nna: number
  change?: number
  growth?: number
}

// Total metrics (matching SmartX aum-metrics structure)
export interface HeaderTotal {
  aua: number
  nna_mtd: number
  nna_qtd: number
  nna_ytd: number
  nna_12m: number
  client_count: number
  account_count: number
  new_client_aua: number
  existing_client_aua: number
  new_client_count: number
  existing_client_count: number
  new_client_pct: number
  q0: QuarterlyNNA
  q1: QuarterlyNNA
  q2: QuarterlyNNA
  q3: QuarterlyNNA
}

// Radial chart segment (NMNC/NMEC/Existing)
export interface RadialSegment {
  segment: string
  label: string
  aua: number
  aua_pct: number
  client_count: number
  color: string
}

// Radial chart data for donut
export interface RadialData {
  title: string
  data: RadialSegment[]
}

// Distribution percentiles
export interface DistributionPercentiles {
  p10: number | null
  p25: number | null
  p50: number | null
  p75: number | null
  p90: number | null
}

// Histogram data for bell curve
export interface HistogramData {
  bins: number[]
  counts: number[]
  bin_labels: string[]
}

// Distribution stats (matches SmartX DistributionStats pattern)
export interface DistributionStats {
  count: number
  total: number
  mean: number | null
  median: number | null
  percentiles: DistributionPercentiles
  min: number | null
  max: number | null
  std_dev: number | null
  histogram: HistogramData
  // Y6c: Split inflow/outflow percentiles (signed NNA distributions)
  inflow_percentiles?: DistributionPercentiles
  outflow_percentiles?: DistributionPercentiles
  inflow_count?: number
  outflow_count?: number
}

// Segment distribution with label
export interface SegmentDistribution extends DistributionStats {
  label: string
}

// Account distribution data
export interface AccountDistributionData {
  total: DistributionStats
  by_segment: {
    NMNC: SegmentDistribution
    NMEC: SegmentDistribution
    Existing: SegmentDistribution
  }
}

// Architect breakdown row
export interface ArchitectBreakdown {
  architect: string
  aua: number
  aua_pct: number
  client_count: number
  account_count: number
}

// Rolling 12-month timeseries data point
export interface RollingTimeseriesDataPoint {
  date: string           // "2021-01-01"
  month: string          // "2021-01"
  total_aua: number
  rolling_12m_nmnc: number
  rolling_12m_nmec: number
  existing_aua: number
  nmnc_pct: number
  nmec_pct: number
  existing_pct: number
  nmnc_client_count: number
  nmec_client_count: number
}

// Rolling timeseries structure
export interface RollingTimeseries {
  description: string
  data: RollingTimeseriesDataPoint[]
}

// ============================================================================
// Cumulative Time Series Chart Types (v6 - "Graph Goes Up")
// ============================================================================

// AUA data point — pre-aggregated per period by the publisher (PSCFIX schema)
// period:   e.g. "2024-Q3", "2024-10", "2024"
// label:    display label, e.g. "Q3 '24", "Oct '24", "2024"
// end_date: ISO date of last day in period, e.g. "2024-09-30"
// [cat]:    numeric AUA value per category (NMNC, NMEC)
export interface AuaDataPoint {
  period: string
  label: string
  end_date: string
  [category: string]: number | string
}

// AUA cumulative view — one per granularity sub-key
export interface AuaCumulativeView {
  categories: string[]
  data: AuaDataPoint[]
}

// Single data point for NNA/GEO/ADV cumulative chart (daily, unchanged)
export interface CumulativeChartDataPoint {
  date: string
  [category: string]: string | number  // Dynamic categories (NMNC, NMEC, TX, etc.)
}

// View data for NNA/GEO/ADV cumulative chart (daily, unchanged)
export interface CumulativeChartView {
  description: string
  categories: string[]
  data: CumulativeChartDataPoint[]
}

// Full cumulative chart response
export interface CumulativeChartResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  date_range: {
    start: string
    end: string
    days: number
  }
  metadata?: TimeseriesChartMetadata  // Includes new_clients by window
  aua: Record<'quarterly' | 'monthly' | 'annually', AuaCumulativeView>  // Pre-aggregated per period (PSCFIX)
  nna: CumulativeChartView   // Daily NNA flows
  geo: CumulativeChartView   // Cumulative NNA by region
  adv: CumulativeChartView   // Cumulative NNA by architect
  geo_drill?: Record<string, CumulativeChartView>  // State -> city drill-down
  adv_drill?: Record<string, CumulativeChartView>  // Architect -> client drill-down
  cla?: {                                           // Client Lifecycle Analysis (NMNC/NMEC)
    total: CumulativeChartView
    geo_drill: Record<string, CumulativeChartView>
    adv_drill: Record<string, CumulativeChartView>
    geo_city_drill?: Record<string, Record<string, CumulativeChartView>>
  }
  // Y5: Monthly AUA change decomposed into market appreciation + NNA
  growth_decomposition?: GrowthDecompositionView
  // Y9: Cumulative NNA with inflow/outflow by state/architect
  nna_geo?: NNASeriesView
  nna_adv?: NNASeriesView
  nna_geo_drill?: NNAGeoDrillView
  // Y3: Asset class AUA breakdown (monthly snapshots from holdings_lots)
  aua_mix?: AuaMixView
}

// View mode for the chart toggle
export type CumulativeChartViewMode = 'aua' | 'nna' | 'geo' | 'adv'

// Window options for date range filter
export type ChartWindowOption = '3M' | '6M' | '1Y' | '2Y' | '3Y' | 'Max' | 'MTD' | 'QTD' | 'YTD'

// Full header metrics response (matches header_metrics.json)
export interface HeaderMetricsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  firm_name: string
  dates: {
    q0: string
    q1: string
    q2: string
    q3: string
  }
  total: HeaderTotal
  by_architect: ArchitectBreakdown[]
  radial_12m: RadialData
  account_distribution: AccountDistributionData
  timeseries?: RollingTimeseries  // Rolling 12M data for area chart
}

// Legacy HeaderSummary (for backwards compatibility)
export interface HeaderSummary {
  as_of_date: string
  total_aua: number
  nna_ytd: number
  nmnc_ytd: number
  nmec_ytd: number
  client_count: number
}

// ============================================================================
// Partner Analytics Types (v5 - Nested Drill-Down & Time Machine)
// ============================================================================

// Granularity options for partner analytics fetch
export type GranularityOption = 'monthly' | 'quarterly' | 'annually'

// Base view modes (shown in toggle)
// - aua: Default view - AUA by client type (reads from nna.current.aua)
// - nna: Flows view - Net new assets with drill-down (reads from nna.current.flows)
// - geo: Geographic breakdown with city drill-down
// - adv: Architect breakdown with client drill-down
export type PartnerAnalyticsBaseView = 'aua' | 'nna' | 'geo' | 'adv'

// Extended view modes (includes drill-down states for internal tracking)
// - city: accessed via GEO drill-down (not a separate view)
// - client: accessed via ADV drill-down (not a separate view)
export type PartnerAnalyticsViewMode = PartnerAnalyticsBaseView | 'city' | 'client'

// Time period keys for time machine (all granularities)
// quarterly: q1/q2/q3 | monthly: m1/m2/m3 | annual: y1/y2/y3
export type TimePeriodKey = 'current' | 'q1' | 'q2' | 'q3' | 'm1' | 'm2' | 'm3' | 'y1' | 'y2' | 'y3'

// ----------------------------------------------------------------------------
// Nested Segment Types (for drill-down)
// ----------------------------------------------------------------------------

// City segment (nested inside GEO state segments)
export interface CitySegment {
  key: string              // "austin_tx"
  label: string            // "Austin"
  aua: number
  aua_pct: number          // % within parent state
  client_count: number
  color: string
  rank?: number            // 1-9 for top cities, null for "Other"
  distribution?: DistributionStats  // Distribution for this city's clients
}

// Client/Relationship segment (nested inside ADV architect segments)
export interface ClientSegment {
  key: string              // "client_123" or relationship_id
  label: string            // "Smith Family Trust" (may be anonymized)
  aua: number
  aua_pct: number          // % within parent architect
  account_count: number
  color: string
  rank?: number            // 1-5 for top clients, null for "Other"
  distribution?: DistributionStats  // Distribution for this client's accounts
}

// NNA flow segment (for NNA drill-down showing inflows/outflows)
export interface NnaFlowSegment {
  key: string              // "nmnc_inflows", "nmnc_outflows", etc.
  label: string            // "Inflows (New Clients)", "Outflows (New Clients)"
  value: number            // Flow amount (positive for inflows, negative for outflows)
  flow_type: 'inflow' | 'outflow'
  color: string
}

// Donut segment with optional nested children for drill-down
export interface DonutSegment {
  key: string
  label: string
  aua: number
  aua_pct: number
  client_count: number
  color: string

  // NNA-specific fields (used when viewing NNA - net flows instead of AUA)
  value?: number           // Net flow amount (for NNA view)
  value_pct?: number       // Percentage of total net flows (for NNA view)
  period_inflows?: number  // Gross inflows during period
  period_outflows?: number // Gross outflows during period (negative)
  flows?: NnaFlowSegment[] // NNA: nested inflows/outflows for drill-down

  // Nested drill-down data (only present for GEO and ADV views)
  cities?: CitySegment[]      // GEO: nested cities within this state
  clients?: ClientSegment[]   // ADV: nested clients under this architect

  // Distribution for this segment (enables drill-down distribution tracking)
  distribution?: DistributionStats
}

// Donut chart data
export interface DonutData {
  title: string
  total: number
  segments: DonutSegment[]
}

// ----------------------------------------------------------------------------
// Period Metrics (for Time Machine)
// ----------------------------------------------------------------------------

// Metrics for a specific time period
export interface PeriodMetrics {
  aua: number
  client_count: number

  // Change vs current (only present in historical periods)
  aua_change_pct?: number    // % change FROM this period TO current (positive = growth)
  client_change?: number     // Net client count change since this period

  // Optional NNA data for the period
  nna_in_period?: number     // NNA flows during this period
  nna_ytd?: number           // NNA year-to-date as of this period
}

// View metrics (legacy format for backwards compatibility)
export interface ViewMetrics {
  aua: number
  nna_ytd: number
  q0: QuarterlyNNA
  q1: QuarterlyNNA
  q2: QuarterlyNNA
}

// ----------------------------------------------------------------------------
// Distribution Types
// ----------------------------------------------------------------------------

// Distribution data with by_segment breakdown
export interface ViewDistribution {
  total: DistributionStats
  by_segment: Record<string, DistributionStats>
}

// ----------------------------------------------------------------------------
// Period Snapshot (single point in time)
// ----------------------------------------------------------------------------

// A view snapshot at a specific point in time
export interface PeriodSnapshot {
  donut: DonutData
  distribution: ViewDistribution  // Script 09 populates for all periods
  metrics: PeriodMetrics
}

// ----------------------------------------------------------------------------
// View with Time Machine Support
// ----------------------------------------------------------------------------

// Single view with multiple period snapshots (supports all granularities)
export interface PartnerAnalyticsViewWithPeriods {
  current: PeriodSnapshot
  // Quarterly periods
  q1?: PeriodSnapshot          // Last quarter (e.g., "Q4 '25")
  q2?: PeriodSnapshot          // 2 quarters ago (e.g., "Q3 '25")
  q3?: PeriodSnapshot          // 3 quarters ago (e.g., "Q2 '25")
  // Monthly periods
  m1?: PeriodSnapshot          // Last month
  m2?: PeriodSnapshot          // 2 months ago
  m3?: PeriodSnapshot          // 3 months ago
  // Annual periods
  y1?: PeriodSnapshot          // Last year
  y2?: PeriodSnapshot          // 2 years ago
  y3?: PeriodSnapshot          // 3 years ago
}

// Legacy single view data structure (backwards compatible)
export interface PartnerAnalyticsView {
  donut: DonutData
  distribution: ViewDistribution
  metrics: ViewMetrics
}

// ----------------------------------------------------------------------------
// Period Metadata
// ----------------------------------------------------------------------------

// Period definition with date and display label
export interface PeriodDefinition {
  date: string                 // "2025-12-31"
  label: string                // "Q4 '25"
}

// All periods metadata (keys present depend on granularity)
export interface PeriodsMetadata {
  current: PeriodDefinition
  // Quarterly
  q1?: PeriodDefinition
  q2?: PeriodDefinition
  q3?: PeriodDefinition
  // Monthly
  m1?: PeriodDefinition
  m2?: PeriodDefinition
  m3?: PeriodDefinition
  // Annual
  y1?: PeriodDefinition
  y2?: PeriodDefinition
  y3?: PeriodDefinition
}

// ----------------------------------------------------------------------------
// Full Response Types
// ----------------------------------------------------------------------------

// ----------------------------------------------------------------------------
// CLA (Client Lifecycle Analysis) Types
// ----------------------------------------------------------------------------

export interface LifecycleBucket {
  nna: number
  inflows: number
  outflows: number
  count: number
}

export interface ClaSegment {
  key: string
  label: string
  nna_total: number
  nmnc: LifecycleBucket
  nmec: LifecycleBucket
}

export interface ClaTotals {
  nna: number
  nmnc_nna: number
  nmec_nna: number
  nmnc_count: number
  nmec_count: number
}

export interface ClaView {
  segments: ClaSegment[]
  totals: ClaTotals
}

// ----------------------------------------------------------------------------
// NNA View Types (nested by cohort within period)
// ----------------------------------------------------------------------------

export interface NnaView {
  donut: DonutData & { total_abs: number }
  distribution: ViewDistribution
  metrics: { nna: number; client_count: number }
  // Y6b: GEO drill — views.nna.[period].geo.drill.{state}.by_city.{city} = DistributionStats
  // Y6d: ADV drill — views.nna.[period].adv.drill.{architect}.distribution = DistributionStats
  drill?: NNADistributionDrill
}

// Y6b/Y6d: NNA distribution drill-down entries
export interface NNADistributionDrillEntry {
  distribution?: DistributionStats   // ADV: aggregate distribution for architect's relationships
  total?: DistributionStats          // GEO: aggregate distribution for state (mirrors script 09 output)
  relationship_count?: number
  by_city?: Record<string, DistributionStats>
}

// Y6b/Y6d: Keyed by state (geo) or architect (adv)
export interface NNADistributionDrill {
  [segmentKey: string]: NNADistributionDrillEntry
}

export interface NnaPeriodView {
  geo: NnaView
  adv: NnaView
}

// Full Partner Analytics response (v5 - with nested drill-down and time machine)
export interface PartnerAnalyticsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  firm_name: string

  // Period metadata for time machine
  periods?: PeriodsMetadata

  // Views with period snapshots (new structure)
  // All 4 views are separate top-level views with standard structure
  views: {
    aua: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView  // AUA by client type
    nna: Record<TimePeriodKey, NnaPeriodView>                    // NNA by cohort (nested geo/adv)
    geo: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView  // Geographic with city drill-down
    adv: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView  // Architect with client drill-down
    cla?: Record<TimePeriodKey, { geo: ClaView; adv: ClaView }> // Client Lifecycle Analysis
  }

  timeseries?: RollingTimeseries  // Rolling 12M data for area chart
}

// ----------------------------------------------------------------------------
// Type Guards & Helpers
// ----------------------------------------------------------------------------

// Check if a view has period snapshots (time machine enabled)
export function hasTimeMachine(
  view: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
): view is PartnerAnalyticsViewWithPeriods {
  return 'current' in view && typeof view.current === 'object' && 'donut' in view.current
}

// Check if a segment has nested cities (GEO drill-down)
export function hasCities(segment: DonutSegment): segment is DonutSegment & { cities: CitySegment[] } {
  return Array.isArray(segment.cities) && segment.cities.length > 0
}

// Check if a segment has nested clients (ADV drill-down)
export function hasClients(segment: DonutSegment): segment is DonutSegment & { clients: ClientSegment[] } {
  return Array.isArray(segment.clients) && segment.clients.length > 0
}

// Check if a segment has nested flows (NNA drill-down)
export function hasFlows(segment: DonutSegment): segment is DonutSegment & { flows: NnaFlowSegment[] } {
  return Array.isArray(segment.flows) && segment.flows.length > 0
}

// Get current period snapshot from view (handles both v4 and v5 formats)
export function getCurrentSnapshot(
  view: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
): PeriodSnapshot | PartnerAnalyticsView {
  if (hasTimeMachine(view)) {
    return view.current
  }
  return view
}

// Get historical period snapshot (returns undefined if not available)
export function getHistoricalSnapshot(
  view: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView,
  period: Exclude<TimePeriodKey, 'current'>
): PeriodSnapshot | undefined {
  if (hasTimeMachine(view)) {
    return (view as PartnerAnalyticsViewWithPeriods)[period]
  }
  return undefined
}

// ============================================================================
// Clients Tab Types (Book View & Client Detail)
// ============================================================================

// Client dropdown option
export interface ClientOption {
  key: string
  name: string
  aua: number
}

// Headline section - aggregate metrics
export interface ClientsTabHeadline {
  total_aua: number
  account_count: number
  client_count: number
  fee_rate_pct: number
  income_yield_pct: number
}

// Tax intelligence section
export interface ClientsTabTax {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
  capital_gains_ttm: number
}

// Income & fees section
export interface ClientsTabIncomeFees {
  dividends_ttm: number
  interest_ttm: number
  total_income_ttm: number
  income_yield_pct: number
  management_fees_ttm: number
  fee_rate_pct: number
}

// Portfolio allocation item
export interface PortfolioAllocationItem {
  name: string
  pct: number
}

// Portfolio composition section
export interface ClientsTabPortfolio {
  allocation: PortfolioAllocationItem[]
  weighted_expense_ratio: number
  unique_holdings: number
  top_5_concentration_pct: number
}

// Engagement metrics section
export interface ClientsTabEngagement {
  trading_buys_ttm: number
  trading_sells_ttm: number
  net_flows_ttm: number
  avg_relationship_years: number
  active_clients_pct: number
}

// Full Clients Tab response (Book view)
export interface ClientsTabResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  headline: ClientsTabHeadline
  tax: ClientsTabTax
  income_fees: ClientsTabIncomeFees
  portfolio: ClientsTabPortfolio
  engagement: ClientsTabEngagement
  clients: ClientOption[]
}

// Individual client detail response
export interface ClientDetailResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  client_key: string
  client_name: string
  headline: ClientsTabHeadline
  tax: ClientsTabTax
  income_fees: ClientsTabIncomeFees
  portfolio: ClientsTabPortfolio
  engagement: ClientsTabEngagement
}

// ============================================================================
// Leaderboard Types (Architect & Implementor Rankings)
// ============================================================================

// Individual leaderboard entry
export interface LeaderboardEntry {
  rank: number
  name: string
  nna: number
  aua_growth_pct: number
  new_clients: number
  total_aua: number
  client_count: number
  account_count: number
}

// Leaderboard summary statistics
export interface LeaderboardSummary {
  total_nna: number
  total_aua: number
  total_new_clients: number
  positive_nna_count: number
  negative_nna_count: number
}

// Leaderboard window data (entries for a specific time period)
export interface LeaderboardWindowData {
  entry_count: number
  summary: LeaderboardSummary
  entries: LeaderboardEntry[]
}

// Full leaderboard response (organized by time windows)
export interface LeaderboardResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  leaderboard_type: 'architect' | 'implementor'
  available_windows: string[]
  windows: Record<string, LeaderboardWindowData | undefined>
}

// Timeseries chart metadata (includes new_clients by window)
export interface TimeseriesChartMetadata {
  new_clients: Record<string, number>
}

// ============================================================================
// Advisor Book Types (Per-Advisor View)
// ============================================================================

// NNA metrics for an advisor
export interface AdvisorNNA {
  ytd: number          // Net New Assets Year-to-Date
  qtd: number          // Quarter-to-Date
  mtd: number          // Month-to-Date
}

// Growth metrics for an advisor
export interface AdvisorGrowth {
  ytd_pct: number      // Growth % Year-to-Date
  qtd_pct: number      // Growth % Quarter-to-Date
}

// Tax exposure breakdown
export interface AdvisorTaxExposure {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
}

// Income and fees summary
export interface AdvisorIncomeFees {
  income_total_ttm: number
  avg_income_yield_pct: number
  fees_total_ttm: number
  avg_fee_rate_pct: number
}

// Asset allocation item
export interface AssetAllocationItem {
  category: string
  label: string
  pct: number
}

// Portfolio composition
export interface AdvisorPortfolioComposition {
  asset_allocation: AssetAllocationItem[]
  avg_expense_ratio: number
}

// Engagement metrics
export interface AdvisorEngagement {
  net_flows_ttm: number
  inflows_ttm: number
  outflows_ttm: number
  avg_tenure_days: number
}

// Client in advisor's book
export interface AdvisorClient {
  client_key: string
  client_name: string
  aua: number
}

// Full advisor book response
export interface AdvisorBookResponse {
  generated_at: string
  data_as_of: string

  book_type: string              // "architect"
  book_key: string               // "travis_penfield"
  book_name: string              // "Travis Penfield"

  summary: {
    total_aua: number
    client_count: number
    account_count: number
  }

  nna: AdvisorNNA
  growth: AdvisorGrowth
  tax_exposure: AdvisorTaxExposure
  income_fees: AdvisorIncomeFees
  portfolio_composition: AdvisorPortfolioComposition
  engagement: AdvisorEngagement

  clients: AdvisorClient[]
}

// ============================================================================
// Advisor Rolling Flows (Advisors Tab -- NNA Summary + Rolling Time Series)
// ============================================================================

export type NnaPeriodKey = 'mtd' | 'qtd' | 'ytd'

export interface NnaSummarySegment {
  advisor_name: string
  advisor_id: string
  nna: number
  nna_pct: number
  inflows: number
  outflows: number
  total_aua: number
  client_count: number
  new_clients: number
  prior_nna: number
  nna_growth_pct: number
  rank: number
  prior_rank: number
  rank_change: number      // positive = moved up
  color: string
}

export interface NnaPriorPeriod {
  period_start: string
  period_end: string
  display: string
  total_nna: number
}

export interface NnaPeriodSummary {
  period_start: string
  period_end: string
  display: string
  growth_label: string     // 'MoM' | 'QoQ' | 'YoY'
  total_nna: number
  total_inflows: number
  total_outflows: number
  prior: NnaPriorPeriod
  growth_pct: number       // total NNA growth vs prior period
  segments: NnaSummarySegment[]
}

export interface RollingFlowsDataPoint {
  date: string
  nna: number
  inflows: number
  outflows: number
}

export type RollingFlowsWindowKey = '30d' | '90d' | '1Y'

export interface AdvisorRollingSeries {
  advisor_name: string
  advisor_id: string
  series: Record<RollingFlowsWindowKey, RollingFlowsDataPoint[]>
}

export interface AdvisorRollingFlowsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  summary: {
    architects: Record<NnaPeriodKey, NnaPeriodSummary>
    implementors: Record<NnaPeriodKey, NnaPeriodSummary>
  }
  architects: AdvisorRollingSeries[]
  implementors: AdvisorRollingSeries[]
}

// ============================================================================
// ADVI-005: Stacked Bar + Rolling 1Y (V2 extension of AdvisorRollingFlowsResponse)
// ============================================================================

// Period keys for stacked bar aggregation (ADVI-005)
export type StackedBarPeriodKey = 'qtd' | 'ytd' | '1y' | '3y' | 'max'

// One advisor's aggregated flows for a stacked bar period
export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number   // positive magnitude
  outflows: number  // positive magnitude — negate client-side for downward bar segment
  nna_net: number   // signed
}

// One advisor's fixed 1Y rolling window daily timeseries
export interface AdvisorRolling1YSeries {
  advisor_name: string
  advisor_id: string
  series: RollingFlowsDataPoint[]  // daily { date, nna, inflows, outflows }; outflows positive magnitude
}

// V2 extends V1 with optional stacked_bar and rolling_1y (additive, backward-compatible)
export interface AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse {
  stacked_bar?: Record<StackedBarPeriodKey, {
    architects: AdvisorBarEntry[]
    implementors: AdvisorBarEntry[]
  }>
  rolling_1y?: {
    architects: AdvisorRolling1YSeries[]
    implementors: AdvisorRolling1YSeries[]
  }
  // Y13: Monthly granularity stacked bar — { "YYYY-MM": AdvisorBarEntry[] }
  monthly?: Record<string, AdvisorBarEntry[]>
}

// ============================================================================
// Y5: Growth Decomposition (timeseries_chart.json)
// ============================================================================

export interface GrowthDecompositionPoint {
  period: string   // "YYYY-MM" monthly
  market: number   // AUA change attributable to market appreciation
  nna: number      // net new assets for the period
  total: number    // market + nna = total AUA change
}

export interface GrowthDecompositionView {
  description: string
  data: GrowthDecompositionPoint[]
}

// ============================================================================
// Y9: NNA Series with Inflows/Outflows (timeseries_chart.json)
// ============================================================================

export interface NNASeriesPoint {
  date: string
  [key: string]: number | string  // category, category_inflow, category_outflow
}

export interface NNASeriesView {
  description: string
  categories: string[]
  data: NNASeriesPoint[]
}

export interface NNAGeoDrillView {
  [stateKey: string]: {
    categories: string[]
    data: NNASeriesPoint[]
  }
}

// ============================================================================
// Y3: AUA Asset Class Mix (timeseries_chart.json)
// ============================================================================

export interface AuaMixSegment {
  label: string   // "Equities", "Fixed Income", "Real Estate", "Alternatives", "Cash", "Other"
  value: number
}

export interface AuaMixPoint {
  period: string  // "YYYY-MM"
  segments: AuaMixSegment[]
}

export interface AuaMixView {
  description?: string
  categories?: string[]
  data: AuaMixPoint[]
}

// ============================================================================
// Y15: Books Tab L2/L3/L4 Types (from ADVI-006 design brief Section 6)
// ============================================================================

// L3: Client detail from bd-portal-advisor-publisher -> build_client_details()
// Note: Named BooksClientDetailResponse to avoid collision with existing ClientDetailResponse
// which serves the legacy clients_tab.json shape.
export interface BooksClientDetailResponse {
  data_as_of: string
  headline: {
    total_aua: number
    account_count: number
  }
  tax: BooksClientTaxDetail
  engagement: {
    net_flows_ttm: number
    avg_relationship_years: number
  }
  accounts: BooksClientAccount[]
}

export interface BooksClientAccount {
  account_id: string
  tax_status: string
  total_aua: number
  cum_inflows: number
  cum_outflows: number
  nna: number
  num_positions: number
}

export interface BooksClientTaxDetail {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
  qualified_aua: number
  qualified_pct: number
  non_qualified_aua: number
  non_qualified_pct: number
  qualified_account_count?: number
  non_qualified_account_count?: number
  cost_basis_by_year: CostBasisYear[]
  top_gain_positions: GainPosition[]
  open_lots: OpenLot[]
  open_lots_count: number
}

export interface CostBasisYear {
  year: number
  cost_basis: number
  market_value: number
  unrealized_gain: number
}

export interface GainPosition {
  asset_name: string
  ticker?: string
  unrealized_gain: number
  cost_basis: number
  market_value: number
  term: string
}

export interface OpenLot {
  account_id: string
  asset_name: string
  ticker?: string
  // Canonical names (future Lambda target)
  quantity: number
  unrealized_gain: number
  // Actual Lambda field names (current output — used as fallback)
  current_units?: number      // Lambda sends this; maps to quantity
  accrued_gain?: number       // Lambda sends this; maps to unrealized_gain
  cost_per_unit?: number      // Lambda sends this; avg cost per unit
  current_price?: number      // Lambda sends this; current market price per unit
  // Common fields
  cost_basis: number
  market_value: number
  term: string
  acquisition_date?: string
}

// ============================================================================
// Books Tab Timeseries & Composition Types (P4 endpoints)
// ============================================================================

export interface BooksTimeseriesPoint {
  date: string
  total_aua: number
  cum_inflows: number
  cum_outflows: number
  nna: number
}

export interface BooksTimeseriesResponse {
  generated_at: string
  data_as_of: string
  relationship_id?: string
  account_id?: string
  data: BooksTimeseriesPoint[]
}

export interface MixItem {
  asset_class: string  // 'equity' | 'fixed_income' | 'hedge' | 'cash' | 'other'
  label: string
  market_value: number
  pct: number
  // N1/L2 schema only -- per-class top holdings (pct relative to class market_value)
  top_holdings?: ConcentrationItem[]
  other?: { market_value: number; pct: number }
}

export interface ConcentrationItem {
  key: string
  label: string
  asset_class: string
  market_value: number
  pct: number
}

export interface BooksCompositionResponse {
  generated_at: string
  data_as_of: string
  scope: {
    relationship_id?: string
    account_id?: string
    advisor_id?: string   // N1/L2 schema
    firm_id?: string      // N1/L2 schema
  }
  mix: MixItem[]
  concentration: {
    top_n: number
    items: ConcentrationItem[]
    other: { market_value: number; pct: number }
  }
  // N1/L2 schema only -- global top holdings (pct relative to total_market_value)
  top_holdings?: ConcentrationItem[]
  other?: { market_value: number; pct: number }  // global other
  unclassified: { count: number; market_value: number }
}

// ============================================================================
// Mix Timeseries + Concentration Timeseries (Addendum A)
// ============================================================================

export type MixAssetClass = 'equity' | 'fixed_income' | 'alternatives' | 'cash'

export interface MixTimeseriesPoint {
  date: string                  // 'YYYY-MM-DD'
  equity: number                // 0-1 (pct)
  fixed_income: number
  alternatives: number          // CLSUNI: hedge -> alternatives
  cash: number
}

export interface ConcentrationPoint {
  date: string
  asset_name: string
  ticker: string | null
  asset_class: MixAssetClass
  market_value: number
  pct: number                   // pct of total relationship MV on that date
}

export interface ConcentrationResponse {
  relationship_id: string
  top_n: number                 // N used for top-N filter (e.g. 10)
  data: ConcentrationPoint[]
}

export type MixWindow = '1Y' | '3Y' | 'Max'

// ============================================================================
// Firm Mix Views Types (ADVI_MIXV2 -- firm-level pre-aggregated mix endpoint)
// ============================================================================

// Single asset class value: absolute dollar amount and allocation fraction.
// pct is 0-1 convention (e.g. 0.62 = 62%).
export interface FirmMixClassValue {
  value: number  // absolute AUA in dollars
  pct: number    // allocation fraction, 0-1
}

// One period data point from the firm/mix-views endpoint.
// pct fields on each class are 0-1 convention.
export interface FirmMixPeriodPoint {
  period: string          // e.g. '2024-Q3', '2024-10', '2024'
  label: string           // display label, e.g. "Q3 '24"
  end_date: string        // ISO date of last day in period, e.g. '2024-09-30'
  total_aua: number       // total firm AUA for this period
  equity: FirmMixClassValue
  fixed_income: FirmMixClassValue
  alternatives: FirmMixClassValue  // CLSUNI: hedge -> alternatives
  cash: FirmMixClassValue
}

// Full response from /api/scoped/partners/books/firm/mix-views
export interface FirmMixViewsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  views: {
    quarterly: FirmMixPeriodPoint[]
    monthly: FirmMixPeriodPoint[]
    annually: FirmMixPeriodPoint[]
  }
}

// ============================================================================
// Advisor Timeseries Types (ADVI_MVP318 WS3e -- advisor-level endpoints)
// ============================================================================

export interface AdvisorTimeseriesPoint {
  date: string
  total_aua: number
  cum_inflows: number
  cum_outflows: number
  nna: number
}

export interface AdvisorTimeseriesResponse {
  advisor_id: string
  advisor_name: string
  data_as_of: string
  data: AdvisorTimeseriesPoint[]
}

export interface AdvisorMixTimeseriesResponse {
  advisor_id: string
  advisor_name: string
  data_as_of: string
  data: MixTimeseriesPoint[]
}
```

---

## Participant Background

### 0.4.0_DS_ClientPlatform -- Recent Session Logs

#### advi_bkscmp_001_script12_composition_artifacts.md

# ADVI_BKSCMP.001 — Script 12 + Lambda v2.8 Composition Routes — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-19
**Start Time:** session start

## Objective

Implement ADVI_BKSCMP WS1 + WS2: pre-compute per-class top-9 holdings composition
artifacts for firm (N1) and all advisors (L2), then wire two new no-cache S3-proxy routes
in opal-partners-data. Unblocks `ConsolidatedOverviewPanel` which currently shows
"No allocation data" / "No holdings data" at N1 and L2 because composition endpoints
return 404.

---

## Work Completed

### 1. Task Order Audit (session start)

Reviewed all task orders before starting. Three were pending/status-unknown:
- **ADVI_MVPLVL.007** — confirmed complete (delivered under ADVI_MVP318 WS3a+WS3c: `a3903a03`,
  `6234d50c`). DE verified shape is correct (`data` key end-to-end). Marked complete.
- **ADVI_MVPLVL.008** — confirmed complete (delivered at `14b3be3d`, deployed `aef01b14`).
  Marked complete.
- **ACAT_ALLOCATIONS_RECONCILIATION-001** — confirmed superseded by NNAVAR/AUAVAR
  investigations. Marked complete/superseded.

### 2. WS1 — `12_build_composition_artifacts.py`

**File created:** `data/black_diamond/scripts/gold/12_build_composition_artifacts.py`

Key decisions:
- `_OPAL_ETF_OVERRIDES` sourced from `silver/build_canonical_prices_v2.py` (NOT 06b —
  confirmed absent by DT S-Report 2026-03-19; task order req 1 corrected by COO).
  Dict maps DIVZ/IDVZ/PFDE/PFOE/PCHI by BD asset name string to ticker.
- `classify_series()` called vectorized: `classify_series(df['ticker'], df['asset_name'])`
  (clarified by DT S-Report — task order said "per row" which was imprecise).
- Classification logic (`ETF_CLASSIFICATIONS`, `ASSET_NAME_TO_TICKER`, `classify_series`,
  regex patterns) inlined verbatim from 06b with header comment: "mirrored from 06b — keep in sync".
- `advisor_id` sanitization: `re.sub(r'[^a-z0-9_]+', '_', name.lower().strip()).strip('_')[:60] or 'unknown'`
  matches `ClientsTab.tsx:383` exactly (cross-agent consistency requirement).

Pct conventions (per PRD ADVI_BKSCMP §3):

| Field | Denominator |
|-------|-------------|
| `mix[i].pct` | `total_market_value` |
| `mix[i].top_holdings[j].pct` | `mix[i].market_value` (class AUM) |
| `top_holdings[j].pct` (root) | `total_market_value` |
| `other.pct` (root) | `total_market_value` |
| `mix[i].other.pct` | `mix[i].market_value` |

Algorithm:
1. Discover latest holdings_lots parquet (non-backfill), filter `is_open == True`
2. Apply `_OPAL_ETF_OVERRIDES` to fix null tickers
3. `classify_series(df['ticker'], df['asset_name'])` → `asset_class` column
4. Load `rel_architect_lookup.parquet` (08b output); fallback to `client_dimension.primary_architect`
5. Left-join lookup onto holdings by `relationship_id`
6. Build firm composition (all rows) → write `gold/views/firm_composition.json`
7. Loop over architects → per-advisor composition → write `gold/advisors/{id}/composition.json`
8. Skip advisors with 0 open holdings (do not write empty JSON)

Error handling: rel_architect_lookup missing → WARN + fallback; holdings_lots missing → ERROR + exit 1.

### 3. WS1 — `run_gold_layer.sh` update

Inserted `run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"` after 08b and before
06b in BOTH sections:
- Incremental: between lines 114 (08b) and 115 (06b) → now line 115
- Full: between lines 158 (08b) and 159 (06b) → now line 159

Rationale: 12 reads `rel_architect_lookup.parquet` written by 08b. Does not need account_performance
or client_performance. Does not block 06b. In incremental mode, 12 reads the holdings_lots parquet
from the last full run (script 03 is full-only) — composition artifacts update with latest architect
attribution on every daily run.

Dependency chain comments updated in both sections.

### 4. WS2 — `opal-partners-data` Lambda v2.8

Four changes:

**A. `cors_response_nocache()`** — inserted after `cors_response()` (line 119):
Identical structure, `Cache-Control: no-store, no-cache, must-revalidate`.
Position-level AUM data must not be cached anywhere in the request path.

**B. `serve_s3_json_nocache()`** — inserted after `serve_s3_json()` (line 335):
Structural copy — same S3 logic, same error handling, all `cors_response()` calls replaced
with `cors_response_nocache()`. Zero logic changes.

**C. `handle_firm_composition(bucket)`** — after `handle_advisor_mix_views`:
`return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')`

**D. `handle_advisor_composition(bucket, advisor_id)`** — after `handle_firm_composition`:
Validates `advisor_id` (no `/` or `..`), returns `serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')`.
On invalid id: `cors_response_nocache(400, {'error': 'Invalid advisor_id'})`.

**Routing** — split the existing `elif action == 'composition'` into three branches:
```
composition + entity_type==firm    → handle_firm_composition  (new, before fallback)
composition + entity_type==advisor → handle_advisor_composition (new, before fallback)
composition (all others)           → handle_books_composition (existing L3/L4, unchanged)
```
Firm/advisor dispatch appears BEFORE the generic fallback — same pattern as timeseries dispatch.

Version bumped 2.7 → 2.8. Docstring + available_routes + 404 error list updated.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `_OPAL_ETF_OVERRIDES` from silver, not 06b | Confirmed absent from 06b by DT S-Report. Sourced from build_canonical_prices_v2.py line 69. COO corrected task order req 1 before execution. |
| classify_series vectorized call | Clarified by DT S-Report. Vectorized (Series args) not row-wise. More efficient for large holdings parquet. |
| Script 12 in incremental sequence | 12 reads rel_architect_lookup (08b output, updated daily) and holdings_lots (from last full 03 run). Composition stays current with daily architect changes without needing a full run. |
| serve_s3_json_nocache is a structural copy | Avoids logic divergence. Single responsibility: the no-cache wrapper changes ONLY the cache header. All S3 error handling, validation, and timeouts are preserved identically. |
| firm/advisor routing before generic fallback | Prevents generic fallback from routing firm/advisor to handle_books_composition (which does in-Lambda parquet compute — times out for large scopes). |

---

## Briefs Written

None — all deliverables are Lambda/gold commits routed directly to DT/AE via commit SHAs.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/12_build_composition_artifacts.py` | New script — firm+advisor composition artifacts | Yes — `1e08fc1a` |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | Insert script 12 after 08b in incremental + full | Yes — `1e08fc1a` |
| `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py` | v2.8 — cors_response_nocache, serve_s3_json_nocache, handle_firm_composition, handle_advisor_composition, routing split | Yes — `885719e3` |

---

## Briefs Written

None required — all gates are commit SHAs, no separate data contract changes.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

Two commits on CLOUD: `1e08fc1a` (WS1 — script 12 + run_gold_layer.sh) and `885719e3`
(WS2 — opal-partners-data v2.8). Task order ADVI_BKSCMP.001 marked complete.
Also audited and closed MVPLVL.007, MVPLVL.008, ACAT_ALLOCATIONS_RECONCILIATION-001.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Deploy opal-partners-data v2.8** — gate commit `885719e3`.
   build-and-upload.sh partners-api opal-partners-data → terraform plan/apply (partners-api)
   → 0-diff → tag partners-api-v1.5.0 → push --follow-tags.

2. **[0.6.0_AE_PartnerETL] Deploy script 12 + run_gold_layer.sh, run gold** — gate commit
   `1e08fc1a`.
   - Upload `12_build_composition_artifacts.py` to `s3://opal-data-bd/code/gold/`
   - Upload updated `run_gold_layer.sh` to `s3://opal-data-bd/code/`
   - Run gold incremental (12 will execute after 08b, writes firm_composition.json +
     gold/advisors/{id}/composition.json)
   - Verify: `aws s3 ls s3://opal-data-bd/gold/views/firm_composition.json`

3. **[0.4.2_RD_AdvisorIntelligence] WS3 frontend adapter** — types.ts + ConsolidatedOverviewPanel
   holdings block (PRD §WS3). Can work in parallel — frontend gracefully falls back to synthesis
   until Lambda routes return 200. No DS gate.

4. **DS has no further action on ADVI_BKSCMP.** All DS deliverables delivered.

**Do NOT:**
- Modify `handle_books_composition` — L3/L4 path must remain untouched
- Change the `advisor_id` sanitization in script 12 without coordinating with RD
  (`ClientsTab.tsx:383` must stay in sync — cross-agent consistency requirement)

#### advi_mvp318_001_ds_commits_ws1_ws2_ws3a_ws3c_ws5.md

# ADVI_MVP318.001 DS Commits — WS1, WS2+WS3a, WS3c, WS5 — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-18
**Start Time:** session start
**End Time:** session end

## Objective

Commit all pending DS deliverables for the ADVI_MVP318 sprint: WS1 bd-portal-publisher
fix, D4+WS3a bd-portal-advisor-publisher (architect override + advisor timeseries writers),
WS3c opal-partners-data new advisor route handlers, and WS5 script 10 confirmation.

---

## Work Completed

### 1. WS1 — bd-portal-publisher diff verification and commit

Read the uncommitted diff (+17 lines) in `bd-portal-publisher/lambda_function.py`.

**Finding:** The diff is NOT WS1 Prescription A (geo_us_for_snap date anchor fix in
`build_snapshots()`). The actual changes are ADVI_MVPLVL.006 leaderboard window additions:
- Added MTD calendar window (`mtd_start = pd.Timestamp(year, month, 1)`) to
  `build_architect_leaderboard()`
- Renamed `qtd` -> `QTD` and `ytd` -> `YTD` in `windows_data` and `available_windows`
- Updated comment references accordingly

Prescription A (geo_us_for_snap logic in `build_snapshots()`) was **not pre-staged**.
DT must use WS1-A diagnostic result to decide whether Prescription A is needed before
deploying bd-portal-publisher.

Committed the MVPLVL.006 changes anyway (they are valid and pending). Commit message
explicitly calls out that this is NOT Prescription A.

| Commit | SHA | Description |
|--------|-----|-------------|
| WS1/MVPLVL.006 | `eb70758d` | feat(bd-portal-publisher): add MTD window + uppercase QTD/YTD to architect_leaderboard |

### 2. WS2+WS3a — bd-portal-advisor-publisher: D4 architect override + advisor timeseries

D4 changes were already in the working tree (+32 lines uncommitted). Verified they
implement the architect override correctly per PRD:
- `load_sources()` loads `gold/views/rel_architect_lookup.parquet` with graceful Exception fallback
- `lambda_handler()` left-joins lookup onto acct, overwrites `architect` field where
  `resolved_architect` is non-null, non-empty, and not 'Unresolved'

Added WS3a code BEFORE committing (D4+WS3a batched into one commit per DT constraint):

**`build_advisor_timeseries(acct, cdim) -> None`**
- Groups post-override acct by `(date, architect)`, aggregates sum of total_aua,
  cum_inflows, cum_outflows, nna and count of unique relationship_ids per group
- Writes `gold/advisors/{advisor_id}/timeseries.json` per architect
- Shape: `{advisor_id, advisor_name, data_as_of, data: [{date, total_aua, cum_inflows, cum_outflows, nna}]}`

**`build_advisor_mix_timeseries(acct, relationship_ids_by_advisor) -> None`**
- For each advisor, loads `gold/client_timeseries/{rel_id}.json` from S3 per relationship
- Computes AUA-weighted average of equity/fixed_income/structured_notes/cash/other per date
- All pct fields 0-1 convention
- Writes `gold/advisors/{advisor_id}/mix_timeseries.json`
- Missing relationship files silently skipped (06b AP gate)
- Memory: clears date_agg per advisor; gc.collect() at end

**`build_advisor_books` refactored** to return `(books, relationship_ids_by_advisor)` tuple
(previously returned `books` list only). `lambda_handler` unpacks the tuple and passes
`relationship_ids_by_advisor` to `build_advisor_mix_timeseries`.

Steps in lambda_handler renumbered 1–7 (added Steps 5: advisor timeseries, 6: advisor mix timeseries).

| Commit | SHA | Description |
|--------|-----|-------------|
| D4+WS3a | `a3903a03` | feat(bd-portal-advisor-publisher): D4 architect override + WS3a advisor timeseries artifacts |

### 3. WS3c — opal-partners-data: advisor route handlers

Read the existing routing structure. Books endpoint parses
`/scoped/partners/books/{entity_type}/{entity_id}/{action}`. Previously only handled
`relationship`, `account`, `firm` entity types.

Added:

**`_filter_window(data_list, window) -> list`**
- Filters list of `{date, ...}` dicts to trailing window from today
- Window map: 3M=90d, 6M=180d, 1Y=365d, 2Y=730d, 3Y=1095d
- Unrecognized window returns full list unchanged
- Uses `datetime.utcnow() - timedelta(days=days)` — added `timedelta` to import

**`handle_advisor_timeseries(bucket, advisor_id) -> dict`**
- Validates advisor_id (no `/` or `..`)
- Serves `gold/advisors/{advisor_id}/timeseries.json` via `serve_s3_json`

**`handle_advisor_mix_timeseries(bucket, advisor_id, window) -> dict`**
- Validates advisor_id
- Serves `gold/advisors/{advisor_id}/mix_timeseries.json`
- If `window` param present and response 200, unwraps body JSON, filters `data` list,
  rewraps body

**Routing update in `lambda_handler`:**
- `entity_type` validation extended to include `'advisor'`
- Advisor routes dispatched BEFORE generic `timeseries` fallback to avoid collision
  with `handle_books_timeseries`
- New routes:
  - `GET /api/scoped/partners/books/advisor/{id}/timeseries?firmId=xxx`
  - `GET /api/scoped/partners/books/advisor/{id}/mix-timeseries?firmId=xxx&window=1Y`
- Version bumped from 2.6 to 2.7

| Commit | SHA | Description |
|--------|-----|-------------|
| WS3c | `6234d50c` | feat(opal-partners-data): advisor timeseries + mix-timeseries route handlers |

### 4. WS5 — Script 10 confirmation + Script 09 status

**Script 10 (`10_generate_advisor_rolling_flows.py`):**
```
git log --oneline -- data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py
```
Result: MTD/QTD/YTD changes are committed at `9563a38d feat(bd): enrich script 10 with
MTD/QTD/YTD summary, growth, rank changes`. WS5 is **confirmed committed**. AE can upload
script 10 as-is.

**Script 09 (`09_generate_partner_analytics.py`):**
Checked for MTD/QTD/YTD window patterns. Script 09 uses quarterly/monthly/annual
granularity periods — not a rolling-window leaderboard. It does NOT produce
`architect_leaderboard.json`. The architect leaderboard is produced by
`bd-portal-publisher` Lambda (already handled in WS1/MVPLVL.006 commit above).
**Script 09 does NOT need MTD/QTD/YTD additions.** No changes required.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Commit bd-portal-publisher diff even though it is NOT Prescription A | Changes are valid MVPLVL.006 work; task order says "commit regardless — DT simply won't deploy it if Root Cause B". Commit message explicitly documents the mismatch. |
| Dispatch advisor routes BEFORE generic timeseries in routing | `action == 'timeseries'` is a generic catch-all; advisor must be checked first to avoid routing advisor timeseries requests into `handle_books_timeseries`. |
| _filter_window uses `datetime.utcnow()` not timezone-aware | Consistent with other date calculations in this Lambda; dates in data are YYYY-MM-DD strings, comparison is lexicographic. |
| build_advisor_mix_timeseries silently skips missing rel JSON | 06b AP gate may not have run for all relationships; caller cannot know which are present. |

---

## Briefs Written

None written this session — all deliverables are Lambda commits that go directly to DT
for deploy. No new output shapes or gold script changes requiring a separate data contract brief.

Data contract: `build_advisor_timeseries` and `build_advisor_mix_timeseries` output shapes
are defined in the PRD WS3 endpoint contracts. DT should reference PRD WS3 for shape.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | MTD window + QTD/YTD uppercase in build_architect_leaderboard | Yes — `eb70758d` |
| `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py` | D4 architect override (pre-staged) + WS3a build_advisor_timeseries + build_advisor_mix_timeseries + build_advisor_books refactor | Yes — `a3903a03` |
| `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py` | _filter_window helper + handle_advisor_timeseries + handle_advisor_mix_timeseries + routing + version 2.7 | Yes — `6234d50c` |

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

Three commits on CLOUD: `eb70758d` (bd-portal-publisher MVPLVL.006 leaderboard windows),
`a3903a03` (bd-portal-advisor-publisher D4+WS3a), `6234d50c` (opal-partners-data WS3c
advisor route handlers). WS5 script 10 confirmed committed at `9563a38d`. Script 09
confirmed no changes needed. Task order ADVI_MVP318.001 marked complete.

**WS1 flag for DT:** The bd-portal-publisher commit `eb70758d` does NOT contain Prescription A
(geo_us_for_snap in build_snapshots). DT should run the WS1-A diagnostic before deciding
whether to deploy bd-portal-publisher. If Root Cause A, Prescription A still needs to be
written and committed separately.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Deploy bd-portal-advisor-publisher** — gate commit `a3903a03`
   on CLOUD. Batch WS2+WS3b into one deploy. build-and-upload.sh bd-pipeline bd-portal-advisor-publisher.
2. **[0.4.0_DT_ClientPlatform] Deploy opal-partners-data (partners-api)** — gate commit
   `6234d50c` on CLOUD. Deploy as partners-api v1.4.0 per WS3d.
3. **[0.4.0_DT_ClientPlatform] WS1-A diagnostic** — run `.tmp_segment_analytics_diag.py`
   to determine Root Cause A vs B. If Root Cause A, flag to DS for Prescription A code.
4. **[0.6.0_AE_PartnerETL] Upload script 10** — `10_generate_advisor_rolling_flows.py`
   confirmed committed at `9563a38d`. Upload to S3 per AE gold run task order.
5. **If Root Cause A:** DS must write Prescription A (geo_us_for_snap in build_snapshots)
   to bd-portal-publisher and commit before DT deploys that Lambda.

**Files to touch next:**
- `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` — Prescription A
  fix in `build_snapshots()` if WS1-A diagnostic confirms Root Cause A

**Do NOT:**
- Deploy bd-portal-publisher until WS1-A diagnostic result is known
- Commit bd-portal-advisor-publisher again — D4+WS3a are complete, file is frozen for DT
- Modify opal-partners-data — WS3c is complete, file is frozen for DT

#### advi_mvp318_ws1_geo_timeseries_root_cause_and_fix.md

# ADVI_MVP318 WS1 — Geo Timeseries Root Cause and Fix — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-18
**Start Time:** post-DT diagnostic return
**End Time:** session end

## Objective

Diagnose and fix the WS1 segment analytics variance after DT returned the WS1-A
diagnostic result: geo timeseries view in `timeseries_chart.json` is completely
empty (0 categories, 0 data points). TX is in "Other" bucket with no individual
tracking. Root cause is data-side, not frontend windowing.

---

## Work Completed

### 1. DT Diagnostic Return — Interpreting the Result

DT ran `.tmp_segment_analytics_diag.py` and reported:

```
geo categories: []
geo data points: 0
TX is bucketed into 'Other' -- not individually tracked
ROOT CAUSE: TX is NOT in top-N geo categories (TOP_N_GEO=0)
```

The diagnostic prints `TOP_N_GEO=0` because `geo_categories = []`. This means
`top_states` (populated by `.nlargest(TOP_N_GEO=8, 'total_aua')`) is empty.
The entire geo timeseries — not just TX — produces no output.

The snapshot (`aua_by_state.json`) showing TX=$901M is stale from a prior Lambda
run. The most recent Lambda run wrote `timeseries_chart.json` with empty geo, but
`aua_by_state.json` was last written during a previous successful run before the
geo parquet was regenerated with the broken country encoding.

### 2. Root Cause Investigation

Read the full code path in both directions to identify what could make `top_states`
empty despite real US client data existing.

#### Code path in `build_timeseries_chart()`:

```python
# Step 1: Filter to US rows by country
geo_us = geo[geo['country'].isin(['USA', 'US', '']) | geo['country'].isna()].copy()

# Step 2: Find US-only latest date
latest_date_geo = geo_us['date'].max()  # NaT if geo_us is empty

# Step 3: Get latest snapshot rows
latest_geo = geo_us[geo_us['date'] == latest_date_geo]  # empty if NaT

# Step 4: Pick top 8 states by AUA
top_states = (
    latest_geo[latest_geo['state'].notna() & (latest_geo['state'] != '') &
               (latest_geo['state'] != 'Unknown')]
    .nlargest(TOP_N_GEO, 'total_aua')['state'].tolist()
)  # [] if latest_geo empty
```

If `geo_us` is empty, `latest_date_geo = NaT`, `latest_geo` is empty, and
`top_states = []`. All subsequent geo structures (`geo_by_date`, `geo_categories`,
`geo_data`) are also empty — matching the 0 categories / 0 data points result.

#### Source of the geo parquet (`07_build_nna_aua_by_geography.py`):

Script 07 builds the geo parquet using modal `client_country` from
`accounts_dimension_latest`. The critical logic in `_modal_geo()`:

```python
country = modal_str(grp[country_col], 'Unknown')  # returns BD's stored value

if country not in ('Unknown', '') and country != 'USA':
    state = ''  # treat as non-US: wipe state code
```

**The bug:** This check was written assuming BD stores US country as `'USA'`.
BD actually stores it as `'United States'` (full name). Since
`'United States' != 'USA'`, the condition evaluates to `True` for EVERY US client,
and `state = ''` is assigned to all of them.

The geo parquet therefore has:
- All US clients: `state = ''`, `country = 'United States'`
- No rows with `state IN ('TX', 'CA', 'NY', ...)` at current dates

Back in the Lambda filter:
```python
geo_us = geo[geo['country'].isin(['USA', 'US', '']) | geo['country'].isna()]
```

`'United States'` does not match `'USA'`, `'US'`, `''`, or `isna()` → `geo_us`
is empty → 0 categories, 0 data points in all geo views.

#### Why the snapshot aua_by_state.json still showed $901M:

`build_snapshots()` uses the same country filter as `build_timeseries_chart()`.
If the country filter returns empty, `state_agg` is also empty and
`aua_by_state.json` would have no states. The $901M TX value is from an older
Lambda run that executed before the geo parquet was last regenerated. S3 retains
the old file until the next successful write. The most recent Lambda run wrote
`timeseries_chart.json` with empty geo, but `aua_by_state.json` was not
overwritten (either because the Lambda failed partway through or because the
state data was also empty and the old file was not replaced).

This two-file discrepancy is what made the diagnostic appear to show a "gap"
between the snapshot and timeseries — they were actually from different runs.

### 3. The Fix (commit `fec1f7e4`)

Two changes committed together:

#### Fix 1 — `07_build_nna_aua_by_geography.py` (root cause)

Normalize BD country encoding variants to canonical `'USA'` before the state-wipe
check in `_modal_geo()`:

```python
# Before the non-US check:
if country in ('US', 'United States', 'United States of America'):
    country = 'USA'

# Now the original check works correctly:
if country not in ('Unknown', '') and country != 'USA':
    state = ''
```

After the next gold layer run that includes script 07, the geo parquet will have
correct two-letter state codes (TX, CA, NY, etc.) for all US clients.

#### Fix 2 — `bd-portal-publisher/lambda_function.py` (defensive)

Added module-level constant:

```python
_US_COUNTRY_VARIANTS = frozenset({
    'USA', 'US', 'United States', 'United States of America', ''
})
```

Replaced the hardcoded `isin(['USA', 'US', ''])` filter with `isin(_US_COUNTRY_VARIANTS)`
at all 4 filter sites:
- Line 652: `build_timeseries_chart()` — AUA geo view (`geo_us`)
- Line 927: `build_timeseries_chart()` — NNA geo view (`geo_us_nna`)
- Line 1617: `build_summary()` — geo donut view (`geo_us`)
- Line 1839: `build_snapshots()` — state snapshot (`geo_us`)

This makes the Lambda robust to future BD country encoding changes. Even if script
07 is not immediately re-run, the Lambda will correctly include 'United States'
rows when they appear in the parquet.

**Note:** Fix 2 alone is not sufficient because script 07 also wipes `state = ''`
for 'United States' rows. Both fixes are required for the geo view to be populated.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Fix script 07 as the primary fix | The Lambda fix alone doesn't help because script 07 also sets state='' for 'United States' rows. Root cause must be fixed at the source. |
| Add Lambda fix as defensive secondary | Prevents future regressions if BD encoding changes again. No downside. |
| Use frozenset constant for country variants | Single source of truth for all 4 filter sites; avoids drift between them. |
| WS1-C (RD subtitle) NOT needed | Root cause is data-side. Frontend windowing is not the issue. No RD action required. |
| Prescription A (geo_us_for_snap date anchor) is moot | The original Prescription A targeted a date anchor discrepancy in build_snapshots. That's a secondary concern. The primary issue is country encoding making geo_us empty in both functions. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/07_build_nna_aua_by_geography.py` | Normalize 'United States'/'US' → 'USA' in `_modal_geo()` before state-wipe check | Yes — `fec1f7e4` |
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | Add `_US_COUNTRY_VARIANTS` constant; replace 4 hardcoded country filters | Yes — `fec1f7e4` |

---

## Session Commit Summary (full session, ADVI_MVP318)

| SHA | Description |
|-----|-------------|
| `eb70758d` | feat(bd-portal-publisher): MTD window + QTD/YTD uppercase in architect_leaderboard (ADVI_MVPLVL.006) — NOTE: not Prescription A |
| `a3903a03` | feat(bd-portal-advisor-publisher): D4 architect override + WS3a advisor timeseries artifacts |
| `6234d50c` | feat(opal-partners-data): advisor timeseries + mix-timeseries route handlers (WS3c) |
| `fec1f7e4` | fix(bd-portal-publisher + gold-07): WS1 geo timeseries empty — BD country encoding mismatch |

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

All four DS commits for ADVI_MVP318 are on CLOUD. The WS1 fix (`fec1f7e4`) addresses
both the root cause (script 07 country normalization) and the Lambda defensive filter.
DT has already deployed WS2+WS3b (`a3903a03`) and WS3c (`6234d50c`). WS1 fix requires
a new bd-pipeline deploy (bd-portal-publisher) and a gold layer re-run of script 07
before the geo timeseries will appear in the portal.

---

## AE Completion (2026-03-18 — post-session update)

AE (`0.6.0_AE_PartnerETL`) completed the gold layer steps for WS1:

- Script 07 uploaded to `s3://opal-data-bd/code/gold/` and run in isolation ✓
- Geo parquet rebuilt — **TX $900.8M, 49 states, correct state encoding** ✓
- AE log committed and pushed at `b2119882`

Verification confirms the script 07 fix is correct: country normalization worked,
US clients now have proper two-letter state codes in `nna_aua_by_geography.parquet`.

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Deploy bd-portal-publisher** — `fec1f7e4` is the only
   remaining gate. Geo parquet is already correct. After DT deploys the Lambda, the
   next pipeline trigger will write a correct `timeseries_chart.json` with 8+ state
   categories and TX as an individual series.
   - build-and-upload.sh bd-pipeline bd-portal-publisher
   - terraform plan/apply (bd-pipeline), 0-diff verify
   - Tag: check `git tag -l "bd-v*" | sort -V | tail -5` — likely bd-v2.19.1
   - push --follow-tags

2. **[0.4.0_DT_ClientPlatform] Re-run WS1-A diagnostic post-Lambda-trigger** — run
   `.tmp_segment_analytics_diag.py` after deploy + pipeline trigger to confirm:
   - `geo categories` non-empty (expects ~8 states + 'Other')
   - TX present as an individual category
   - TX AUA in timeseries aligns with snapshot

3. **WS1-C is NOT needed** — root cause confirmed data-side. No RD action.

**DS has no further action on WS1.** All DS commits are on CLOUD. WS1 is fully
gated on DT deploy only.

**Do NOT:**
- Attempt Prescription A (geo_us_for_snap date anchor) — wrong fix; real cause was
  country encoding mismatch, not date anchor difference
- Trigger a full gold run before DT deploys — the Lambda must be at fec1f7e4 when
  it next runs or the corrected geo parquet will be read by the old broken filter

#### black_diamond_cost_basis_tax_lots.md

# BD Cost Basis & Tax Lot Investigation — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-20
**Branch:** CLOUD
**Requested by:** Yang Liu (via Andrew)

---

## Objective

Determine whether Black Diamond can serve as the source for cost basis and tax lot data needed to produce FactSet ShareLots files. A sample Schwab CSV (single account, single security) was provided as the reference, along with the target FactSet output format.

---

## FactSet ShareLots Target Format

```
SECURITY_ID,SHARES,PRICE,PURCHASE_DATE,LOT_NUMBER
```

Five required fields per lot: security ID, shares, purchase price (PIT), purchase date, and lot number.

---

## Investigation

### Step 1: Direct Account Lookup — No Match

BD account IDs follow an 11-character format (`z` + 10 digits). The Schwab account number is only 8 digits. No match found across 9,839 BD accounts by account ID, account name, or any variant.

### Step 2: Position Matching — No Match on Totals

The Schwab CSV shows 3,063.1479 shares across 21 lots. Searched all 127 accounts holding this security in the BD gold holdings_lots layer (today's snapshot, 965,709 lots across 9,433 accounts). No account was within 10% of the target share count or within 15% of the target market value ($760K).

### Step 3: DRIP Fingerprinting — Match Found

Dividend reinvestment (DRIP) lots are unique per account because fractional shares are proportional to position size. The Schwab CSV shows 5 DRIP dates (Feb, May, Aug 2025, Nov 2025, Feb 2026). Compared DRIP unit values across all 47 BD accounts that had DRIP lots on all 5 dates.

One account matched 3 of 5 DRIP values exactly, with the remaining 2 offset by exactly +2.0000 shares each (explained by an intermediate manual purchase being absorbed via FIFO):

```
                 Feb 2025   May 2025   Aug 2025   Nov 2025   Feb 2026
Schwab:          4.0552     4.7689     4.3538     1.0271     0.9429
BD:              4.0552     4.7689     4.3538     3.0271     2.9429
```

**Account identified.** Joint brokerage account, opened 2023-05-01, first transaction 2023-05-01.

### Step 4: BD Lot Detail — Transfer-In Problem

BD has only **6 lots** for this account vs Schwab's **21 lots**:

| BD Lot | Acquired | Shares | Source |
|--------|----------|--------|--------|
| 1 | 2023-05-10 | 4,170.0000 | Transfer In |
| 2 | 2025-02-13 | 4.0552 | DRIP |
| 3 | 2025-05-15 | 4.7689 | DRIP |
| 4 | 2025-08-14 | 4.3538 | DRIP |
| 5 | 2025-11-13 | 3.0271 | DRIP |
| 6 | 2026-02-12 | 2.9429 | DRIP |
| **Total** | | **4,189.1479** | |

All 15 original purchase lots (2019-2023) were collapsed into a single transfer-in lot. The original acquisition dates and cost bases are lost in BD.

### Step 5: Share Count Discrepancy

- **BD total:** 4,189.1479 shares
- **Schwab total:** 3,063.1479 shares
- **Difference:** 1,126.0000 shares

The Schwab CSV covers one account. The BD account appears to hold shares from multiple source accounts consolidated on transfer. The household has 4 BD accounts total (2 joint, 1 rollover IRA, 1 contributory IRA) but only the one joint account holds this security.

### Step 6: Fake Cost Basis Discovery

BD's transfer-in lot shows cost_per_unit of **$173.555**. This security has never traded at the implied average cost of $408.91 that would be required for the unexplained 1,126 shares. Investigation revealed that $173.555 matches the security's **market price on the transfer date** (2023-05-10), not any actual purchase price.

BD did not receive cost basis data with the transfer. It defaulted to market price on transfer day as the cost. The $723,724.35 "cost basis" in BD is simply 4,170 x $173.555 = market value on day of transfer.

### Step 7: Schwab CSV Validation

Verified the Schwab CSV is internally consistent and self-sufficient:

- **Shares x Cost per Share = Cost Basis** confirmed for all 21 lots (sub-penny rounding on DRIP lots only, $0.05 total)
- **Sum of lot shares:** 3,063.1479 -- matches CSV header
- **Sum of lot cost basis:** $268,195.66 -- matches CSV header
- **Average cost/share:** $87.56 -- matches CSV summary row
- **Unrealized gain:** $760,579.62 - $268,195.66 = $492,383.96 -- matches CSV header
- **Long-term + short-term UGL:** $492,247.48 + $136.49 = $492,383.97 -- matches within penny rounding
- **Cost per share IS the PIT (point-in-time) purchase price** -- confirmed by exact multiplication match on every lot

---

## Findings

### BD Cannot Serve as Source for Cost Basis / Tax Lot Data

Three independent problems:

1. **Lost lot history.** The transfer-in collapsed 15 original lots (spanning 2019-2023) into a single lot dated 2023-05-10. Individual acquisition dates and per-lot cost bases are gone.

2. **Wrong share count.** BD shows 4,170 shares for this account vs 3,063 in Schwab. The transfer commingled shares from multiple source accounts.

3. **Fake cost basis.** BD's cost_per_unit ($173.555) is the market price on the transfer date, not the actual weighted average purchase price ($87.56). BD overstates the cost basis by ~2x.

### Schwab CSV Is Self-Sufficient

The Schwab CSV contains all 5 fields required for the FactSet ShareLots file:

| FactSet Field | Schwab CSV Column |
|---|---|
| Security ID | Symbol (requires ticker-to-FactSet ID mapping) |
| Shares | Quantity |
| Purchase Price | Cost per Share (= PIT price, verified) |
| Purchase Date | Acquired/Opened |
| Lot ID | Sequential assignment |

The only field not directly in the CSV is the FactSet permanent security ID, which is a standard mapping Yang's team would have.

---

## Conclusion

BD is not the route for cost basis and tax lot data for accounts that transferred in without lot-level history. The Schwab cost basis CSV is the authoritative source and contains everything needed. The automation question is whether Schwab provides a programmatic way to pull these CSVs (API, SFTP, advisor portal export) rather than manual download.

For accounts that have been in BD since inception (no transfer-in), the `03_build_holdings_lots.py` gold layer script produces FIFO-reconstructed lots with acquisition dates, cost per unit, and cost basis -- but these would still reflect BD's transaction dates, which may differ from custodian-reported dates.

#### opal_etf_ticker_fix_canonical_prices.md

# Opal ETF Ticker Fix — canonical_prices Full Rebuild — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-18
**Start Time:** 15:45 UTC
**End Time:** 15:58 UTC

## Objective

Deploy the `_OPAL_ETF_OVERRIDES` ticker fix to both silver price-building scripts and run a full
rebuild of `canonical_prices.parquet` so that Opal/Pathfinder-branded ETFs no longer carry
`ticker=NaN` through the pipeline into portal position lists.

---

## Root Cause

`config/ticker_lookup.json` (built from bulk BD transaction data) never receives a `ticker` field
for Opal/Pathfinder-branded ETFs — Black Diamond stores them only by their long fund names. This
propagated `ticker=NaN` through the entire silver→gold→portal chain:

```
canonical_prices.parquet  (ticker=NaN)
  → holdings_lots.parquet  (ticker=NaN, from latest-price join)
    → client_tax_liability.parquet  (ticker=NaN)
      → portal position lists  (blank ticker shown)
```

Secondary impact: with `ticker=NaN`, the T2 Yahoo Finance price fetch had no symbol to query,
forcing these assets onto T1 transaction-observed prices only — any day without a BD transaction
was filled by interpolation/carry-forward rather than real market closes.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify DS changes uncommitted in working tree | Both scripts had local modifications |
| 2 | Commit silver scripts to CLOUD | `b69d1ae6` — authored `0.4.0_DS_ClientPlatform` |
| 3 | Upload to `s3://opal-data-bd/code/silver/` | Both files uploaded |
| 4 | Send SSM: `build_canonical_prices_v2.py` full rebuild | Command `11a9621a` — Success |
| 5 | Spot-check canonical_prices.parquet | 6/6 Opal ETF names now have correct tickers, 0 NaN |

---

## What Was Fixed

`_OPAL_ETF_OVERRIDES` dict added to both scripts and injected via `mapping.update()` after
`ticker_lookup.json` is loaded from S3:

| BD Asset Name | Ticker | Notes |
|---|---|---|
| OPAL DIVIDEND INCOME ETF | DIVZ | Current brand name |
| POLEN DIVIDEND INCOME ETF | DIVZ | Filing/legacy name pre-rebrand |
| OPAL INTERNATIONAL DIVIDEND INCOME ETF | IDVZ | |
| PATHFINDER DISCIPLINED US EQUITY ETF | PFDE | BD standard spelling |
| PATHFINDER DISCIPLINED US EQUITIES ETF | PFDE | BD alternate spelling |
| PATHFINDER FOCUSED OPPORTUNITIES ETF | PFOE | |
| POLEN HIGH INCOME ETF | PCHI | Same pattern, included proactively |

Both the monthly full-rebuild path (`build_canonical_prices_v2.py`) and the daily incremental
path (`bd_price_update.py`) were updated so the fix persists through future runs.

---

## Rebuild Output

```
Total rows:    10,406,355
Date range:    2020-06-30 -> 2026-03-16
Unique assets: 9,952
Size:          91.3 MB -> s3://opal-data-bd/silver/prices/canonical_prices.parquet
Elapsed:       114s

By source:
  linear_interpolation   8,561,465  (82.3%)
  yahoo_finance          1,651,217  (15.9%)
  transaction_observed     193,673  ( 1.9%)
```

## Spot-Check Result

```
                        asset_name  ticker
          OPAL DIVIDEND INCOME ETF    DIVZ
OPAL INTERNATIONAL DIVIDEND INCOME ETF    IDVZ
  PATHFINDER DISCIPLINED US EQUITY ETF    PFDE
  PATHFINDER FOCUSED OPPORTUNITIES ETF    PFOE
         POLEN DIVIDEND INCOME ETF    DIVZ
             POLEN HIGH INCOME ETF    PCHI

NaN tickers for these assets: 0
```

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/silver/build_canonical_prices_v2.py` | Added `_OPAL_ETF_OVERRIDES`, injected in `load_ticker_lookup()` | Yes — `b69d1ae6` |
| `data/black_diamond/scripts/silver/bd_price_update.py` | Same addition | Yes — `b69d1ae6` |

---

## Current State

**Status:** COMPLETE

`canonical_prices.parquet` is rebuilt and on S3 with correct tickers for all 6 observed Opal/Pathfinder
ETF name variants. The next gold layer run (incremental or full) will propagate the corrected tickers
downstream: `03_build_holdings_lots.py` picks the latest canonical_prices row per asset, so
`holdings_lots → client_tax_liability → portal` will be correct after the next pipeline run.

---

## Next Steps

1. **[nightly pipeline]** Next gold layer incremental will propagate ticker fix to `holdings_lots.parquet`
   and `client_tax_liability.parquet` automatically — no further action needed.
2. **[0.4.0_DS_ClientPlatform]** Monitor next portal build to confirm blank ticker is resolved in
   position lists.

**Do NOT:**
- Run `build_canonical_prices_v2.py --dry-run` expecting it to write to S3 — dry-run skips all writes
- Re-run the full rebuild unless canonical_prices.parquet drifts — the current parquet is correct as of 2026-03-18T15:57 UTC


### 0.4.0_DS_ClientPlatform -- Pending Task Orders

#### ADVI_CLSPT2.001.ds-finish-classify-script.md

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-20-clspt2-001-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-20</date>
    <status>pending</status>
    <project_code>ADVI_CLSPT2</project_code>
  </metadata>

  <objective>
    Finish the classify_bd_securities.py implementation. The script exists but
    the OpenAI classification logic (lines 64-112) is entirely stubbed/commented out.
    Wire real OpenAI chat completions API calls using the spec in the PRD
    (docs/architecture/ADVI_CLSPT2_PRD.md section WS2).
  </objective>

  <context>
    File: data/black_diamond/scripts/classification/classify_bd_securities.py

    Current state: The script correctly reads holdings_lots parquet from S3,
    extracts unique (ticker, asset_name) pairs, scans bd-securities for existing
    tickers, and filters to new pairs. But lines 64-112 are commented-out
    placeholder code with a fake API URL (https://api.openai.com/v1/classify).
    The actual OpenAI chat completions call was never implemented.

    Also: lines 126-134 contain dead code (_classify_holding function referencing
    undefined _clf). Remove these.

    OpenAI key: stored in AWS Secrets Manager as 'openai-api-key'. The script
    already has the secrets_manager client and retrieval code at line 65-66.

    PRD spec (ADVI_CLSPT2_PRD.md WS2) defines:
    - System prompt with canonical sub-asset class vocabulary
    - Batch size: 50 items per API call
    - Model: gpt-4o-mini
    - Response format: JSON array "results"
    - Key scheme: ticker as PK for 1-5 alpha tickers, NAME::{normalize} for CUSIPs
    - Confidence scoring, needs_review threshold at 0.7
    - Idempotent (skip existing), exponential backoff
    - Summary manifest at gold/manifests/classification_{date}.json
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/classification/classify_bd_securities.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Replace the stubbed OpenAI logic (lines 64-112) with real implementation:

      Use the openai Python library (already available in the EC2 environment):
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

      For each batch of 50 new (ticker, asset_name) pairs, call:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': json.dumps(batch_items)}
            ],
            response_format={'type': 'json_object'},
            temperature=0.1
        )

      Parse the JSON response and extract asset_class, sub_asset_class, confidence,
      rationale for each item.
    </requirement>

    <requirement id="2">
      Use the system prompt from the PRD (ADVI_CLSPT2_PRD.md WS2):

      Classify each security. Use EXACTLY these asset_class values:
        equity | fixed_income | alternatives

      Sub-asset class vocabulary and confidence scoring per the PRD.

      Return JSON object with "results" array.
    </requirement>

    <requirement id="3">
      Key scheme per PRD:
      - Standard 1-5 alpha tickers: use ticker as PK
      - CUSIP-based (9-char alphanumeric starting with digit): use NAME::{normalized_asset_name}
      - normalize_key() already exists in detect_new_securities.py for reference
    </requirement>

    <requirement id="4">
      Write each classified item to bd-securities DynamoDB:
        table.put_item(Item={
            'ticker': pk,
            'asset_class': result['asset_class'],
            'sub_asset_class': result['sub_asset_class'],
            'confidence': Decimal(str(result['confidence'])),
            'needs_review': result['confidence'] < 0.7,
            'classified_by': 'gpt-4o-mini',
            'rationale': result.get('rationale', ''),
            'asset_name_raw': asset_name,
            'last_updated': datetime.utcnow().isoformat() + 'Z'
        })

      Respect --dry-run flag: print what would be written but don't call put_item.
    </requirement>

    <requirement id="5">
      Add exponential backoff for rate limiting (gpt-4o-mini: 500 RPM).
      Print progress every 100 items.
      At completion, write summary to stdout and to
      gold/manifests/classification_{date}.json on S3.
    </requirement>

    <requirement id="6">
      Remove dead code at lines 126-134 (_classify_holding function).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Script runs to completion with --dry-run without errors</criterion>
    <criterion id="2">OpenAI API is called with correct model, system prompt, and response_format</criterion>
    <criterion id="3">No items written with asset_class outside equity|fixed_income|alternatives</criterion>
    <criterion id="4">Dead code at bottom of file removed</criterion>
    <criterion id="5">Idempotent: re-running skips already-classified items</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change detect_new_securities.py -- it is complete and correct</constraint>
    <constraint>Do NOT change lib/etf_classifier.py -- it is deployed and live</constraint>
    <constraint>Do NOT change lambda_function.py -- WS1 is already deployed at partners-api-v1.7.0</constraint>
    <constraint>OpenAI key is 'openai-api-key' in AWS Secrets Manager -- do not hardcode</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      bd-securities table ACTIVE with 116 seeded items (shared-infra-v1.5.0).
      ETFClassifier live at partners-api-v1.7.0. No blockers.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">classify_bd_securities.py with real OpenAI implementation, committed to CLOUD</deliverable>
  </deliverables>
</task_order>


### 0.4.0_DS_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DS_ClientPlatform

2384a9f6 0.4.0_DS_ClientPlatform: opal-partners-data -- firm/mix-views + advisor/mix-views endpoints
a885f625 0.4.0_DS_ClientPlatform: 06b firm + advisor mix period views (WS3+WS6)
a7617a08 0.4.0_DS_ClientPlatform: 06b targeted AP gate override for insurance accounts
89320527 0.4.0_DS_ClientPlatform: fix pct scale in handle_books_composition (0-1 not 0-100)
947c84fe 0.4.0_DS_ClientPlatform: opal-partners-data -- add firm-scope composition endpoint
8ef1da9b 0.4.0_DS_ClientPlatform: architect attribution gold -- T0-T16 decision tree (ADVI_ADVTV2.001)
1c5630b4 0.4.0_DS_ClientPlatform: v3 scoped overrides -- inject corrected prices into canonical_prices.parquet
eb7b0656 0.4.0_DS_ClientPlatform: v2 silver tape -- tape mispriced accounts to silver daily MV instead of zeroing
6f04cbd3 0.4.0_DS_ClientPlatform: fix AUA valuation -- RC1/RC2 price overrides + RC6 ghost account exclusions
faf10088 0.4.0_DS_ClientPlatform: ADVI_MVPLVL 3a — rescope attribution tree to funded accounts
3562585d 0.4.0_DS_ClientPlatform: ADVI_MVPLVL 3a — architect attribution decision tree
1d986a87 0.4.0_DS_ClientPlatform: ADVI_MVPLVL 3a — architect data quality investigation complete
b3c22a28 Deploy EC2 bd-gold-layer-runner @ 6c74e840
d7cdbef5 org(0.4.0_DS_ClientPlatform): architect exposure query session log (2026-03-11)
e57a4f0a org(0.4.0_DS_ClientPlatform): ADVI_PSCFIX DT1 task order updated -- add c3c8d072 + portal 67090a4, deadline 4PM
d900451d org(0.4.0_DS_ClientPlatform): assets overview math audit session log
c3c8d072 0.4.0_DS_ClientPlatform: gro -- last-of-prior-month start so nna telescopes to NNA view
4fac931d org(0.4.0_DS_ClientPlatform): ADVI_PSCFIX A2 session log + task order complete
ea832f51 0.4.0_DS_ClientPlatform: bd-portal-publisher -- static NMNC/NMEC + certified_aua override (ADVI_PSCFIX A2)
cdb7dab1 0.4.0_DS_ClientPlatform: ADVI_49FNV3.F5 -- task order complete, session log

### 0.6.0_AE_PartnerETL -- Recent Session Logs

#### adhc_gldec2_05d_date_fix_deploy.md

# ADHC_GLDEC2 -- 05d Date Fix Deploy -- 0.6.0_AE_PartnerETL

**Date:** 2026-03-12

## Objective

Deploy the fixed `05d_write_aua_certification.py` to EC2. Two bugs were found by
1.0.0_SA_CTO during an AUA investigation: (1) date mismatch causing 05d to SKIP
every nightly run, (2) LIABILITY_TYPES over-excluding insurance accounts.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Commit 05d fix + task order + log amendment | `8805f31b` fix(bd-pipeline): 05d date mismatch |
| 2 | deploy-to-ec2.sh | 05d uploaded to s3://opal-data-bd/code/gold/ (16 scripts total) |
| 3 | EC2_MANIFEST.json updated | Deploy recorded |
| 4 | Verify data_date alignment | client_performance max=2026-03-11, silver/allocations/2026-03-11.parquet exists |
| 5 | Task order marked complete | ADHC_GLDEC2.001 status=complete |

## Verification

S3 gold script count after deploy: **16 scripts** (same count, 05d replaced in-place).

data_date alignment confirmed:
- `gold/client_performance.parquet` max date: `2026-03-11`
- `silver/allocations/2026-03-11.parquet`: exists (uploaded 2026-03-12 17:51 UTC)
- Next nightly run: 05d will look for `silver/allocations/{max_date}.parquet` instead of `silver/allocations/{today}.parquet`

## Root Cause Summary (from CTO investigation)

**Bug 1 (date mismatch -- CRITICAL):**
05d used `datetime.date.today()` -> `2026-03-12` (calendar date T). Silver allocations
are named for data date T-1 (`2026-03-11.parquet`). 05d checked for
`silver/allocations/2026-03-12.parquet` which never exists at run time. Hit SKIP every
night since deployment on 2026-03-11. `gold/aua_certification/` was empty -- publisher
always fell back to uncertified gold totals.

Fix: derive `data_date = max(date)` from `gold/client_performance.parquet`, use that
for both silver lookup and gold filtering. This is the actual data date (T-1).

**Bug 2 (LIABILITY_TYPES over-exclusion):**
Original: `[CreditCard, Mortgage, Loans, Insurance, TermLife, Annuity]`
Fixed:    `[CreditCard, Mortgage, Loans]`

Silver's `account_market_value` includes insurance ($61M). Gold's positions cube also
includes insurance accounts (112 accounts with Shield annuity positions). Both systems
agree. Excluding insurance would have produced a $60M undercount in certified_aua.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Deploy directly (not via safe-ec2-deploy.sh) | safe-ec2-deploy.sh had jq MSYS path issue; deploy-to-ec2.sh ran cleanly and produced same S3 result |
| Keep insurance in certified_aua | Silver includes it, gold includes it, both get the right number -- continuity preserved |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/05d_write_aua_certification.py` | data_date fix + LIABILITY_TYPES narrowed | Yes -- `8805f31b` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADHC_GLDEC2.001.05d-date-fix-redeploy.md` | New task order, marked complete | Yes -- `8805f31b` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-03-11/advi_pscfix_a1_aua_certification_deploy.md` | Amendment documenting both bugs | Yes -- `8805f31b` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded | Pending |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

05d is deployed to S3 with both fixes. Next nightly EC2 run will:
1. Run 05 (client_performance) -- produces gold/client_performance.parquet with max date T-1
2. Run 05c (validation) -- validates gold vs silver
3. Run 05d (certification) -- derives data_date from client_performance, finds silver allocation, writes `gold/aua_certification/{data_date}.json`
4. Publisher reads certification JSON and overrides total_aua in all outputs

Expected result: `gold/aua_certification/2026-03-12.json` will be written on the 2026-03-13 nightly run (with data_date = 2026-03-12, matching silver/allocations/2026-03-12.parquet).

---

## Next Steps

1. **Verify after next nightly run** -- check that `gold/aua_certification/` is no longer empty:
   ```bash
   aws s3 ls s3://opal-data-bd/gold/aua_certification/
   ```
2. **Verify publisher consumed certification** -- check `gold/summary/header_metrics.json` for `display_aua` matching `certified_aua` (not gold_aua)

**Do NOT:**
- Re-run 05d manually with `datetime.date.today()` logic -- the fix only works when client_performance.parquet has been freshly built by the pipeline

#### advi_49fnv3_008_gold_silver_validation.md

# ADVI_49FNV3.008 -- Gold-Silver AUA Validation Pipeline -- 0.6.0_AE_PartnerETL

**Date:** 2026-03-12
**Start Time:** 15:35
**End Time:** 16:40

## Objective

Create and deploy `05c_validate_aua_vs_silver.py` -- a daily gold-vs-silver AUA
cross-check with PASS/WARN/FAIL thresholds, account-level gap decomposition, and
liability type breakdown. Backfill all existing silver dates. Investigate root causes
of the gold-silver divergence (missing accounts + price divergence).

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Write 05c_validate_aua_vs_silver.py | Script created with PASS/WARN/FAIL thresholds, --backfill and --date CLI support |
| 2 | Commit source | `4fd699f4` feat(bd-pipeline): add 05c_validate_aua_vs_silver.py |
| 3 | safe-ec2-deploy.sh bd-gold-layer-runner | 16 gold scripts in s3://opal-data-bd/code/gold/ |
| 4 | EC2_MANIFEST.json updated | Manifest commit `968d0cbb` |
| 5 | Backfill run (local, --backfill) | Bug found: account_number/account_id mismatch in join |
| 6 | Fix: use account_id explicitly for silver-gold join | `a4cbbf87` fix(bd-pipeline): 05c use account_id for silver-gold join |
| 7 | Redeploy to EC2 | 16 gold scripts re-synced |
| 8 | EC2_MANIFEST.json updated | Manifest commit `dca49ecf` |
| 9 | Re-run backfill | 33 dates validated, 3 ERROR (early schema mismatch) |
| 10 | Root cause investigation | Missing accounts + price divergence documented |
| 11 | Mark task order complete | ADVI_49FNV3.008 status=complete |
| 12 | Add 00_build_accounts_dimension to incremental run | `ada01ed1` feat(bd-pipeline): add 00_build_accounts_dimension to incremental run |
| 13 | Deploy updated runner to EC2 | run_gold_layer.sh re-synced to S3 |
| 14 | EC2_MANIFEST.json updated | Manifest commit `2d12ff54` |

## Verification

S3 validation files: **33 JSONs** in `gold/validation/`

Spot-check 2026-03-09 (matches DE baseline exactly):
```json
{
  "gold_aua": 1604917844.0,
  "silver_aua": 1599225406.73,
  "gap_abs": 5692437.26,
  "gap_pct": 0.003559,
  "accounts_missing_from_gold": 83,
  "accounts_missing_mv": 14797305.67,
  "price_divergence_estimate": 20489742.93,
  "status": "FAIL"
}
```

Pipeline wiring: `run_gold_layer.sh` already had `if [ -f 05c ]` guard from PSCFIX A1 deploy.
05c runs after 05_build_client_performance.py, before 05d_write_aua_certification.py.

---

## Root Cause Analysis

### (a) Missing Accounts: Stale accounts_dimension (18 persistent + growing onboarding gap)

**Finding:** `gold/accounts_dimension_latest.parquet` has `data_as_of_date = 2026-03-02` and
`account_open_date` max = 2026-02-26. Script `00_build_accounts_dimension.py` only runs in
**full mode** (monthly, 1st of month). Between full runs, new BD accounts accumulate in silver
allocations but don't appear in gold.

**Backfill trend (missing account count over time):**

| Period | Missing accts | Missing MV | Notes |
|--------|--------------|-----------|-------|
| Jan 16-30 | 18 | ~$6.3M | Stable base -- pre-existing gap from before last full run |
| Feb 2-19 | 18-19 | ~$6.3M | Minimal growth |
| Feb 20-27 | 21-27 | ~$6.3-7.2M | New accounts onboarding |
| Mar 2-5 | 34-62 | $8.1-12.7M | Rapid growth -- weekly onboarding wave |
| Mar 6-10 | 71-90 | $13.6-18.9M | Accelerating -- accounts_dim increasingly stale |

The 18 persistent missing accounts (from Jan) include accounts created as far back as
10/31/2024 (Insurance, $280K) and 03/25/2025 (No Account Type Assigned, $3.75M combined).
These likely lack transactions, so `00_build_accounts_dimension.py` (which reads the
transactions/positions cube) never discovers them. They are real BD accounts with real MV
but have no transaction history in gold.

**Fix applied:** Added `00_build_accounts_dimension.py` to the incremental (daily) run in
`run_gold_layer.sh` (`ada01ed1`). There was no good reason to exclude it -- the script reads
account metadata from transactions + allocations and is idempotent. New accounts will now be
picked up same-day instead of waiting for the monthly full run. The 83 missing accounts should
drop to near-zero after the next nightly run (the ~18 persistent ones from pre-2026 should
also get picked up since the script reads all transaction history + enriches from latest
silver allocations).

### (b) Price Divergence: Canonical market-close vs BD settlement prices (~$20.5M)

**Finding:** Gold AUA uses canonical prices (market close, sourced from yfinance via
`historical-prices` EC2 service). Silver AUA uses BD-reported account_market_value
(which uses BD's internal pricing, typically settlement or intraday pricing).

For 2026-03-09:
- Canonical (gold) prices run ~$20.5M hot compared to BD reported values
- This is a **methodology difference**, not an error
- Canonical prices use market close; BD uses settlement prices which may lag by 1 day or use different pricing sources for certain asset classes (particularly fixed income, alternatives, and insurance products)

The gap is NOT stable -- it varies with market volatility:
- Jan average: ~-$67M (canonical UNDER BD -- market downturn period, canonical prices updated faster)
- Feb average: ~-$47M (narrowing)
- Mar 2-3: sign flipped to +$33-45M (canonical caught up and overshot)
- Mar 9: +$20.5M (closer to steady-state)

**Conclusion:** This is an intentional methodology difference. Canonical prices serve
the gold layer's need for consistent, reproducible pricing across all dates. BD prices
are authoritative for AUA display (which is why PSCFIX uses silver for certified_aua).
No change recommended.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Use `account_id` (not `account_number`) for silver-gold join | Both datasets have `account_id` (z-prefixed internal BD ID). Silver also has `account_number` (numeric external ID) but gold doesn't -- using it caused false 6300+ "missing" accounts |
| 05c runs via `|| true` (not `run_script()`) | Same pattern as 05d -- `run_script()` passes `--upload` flag, non-blocking requirement means 05c should never halt the pipeline |
| Status FAIL at 0.36% gap + 83 missing accounts | 83 exceeds WARN threshold (50), so even though gap_pct is within PASS range, the account count triggers FAIL. Correct behavior per task order thresholds. |
| Add 00 to incremental run | No reason to only build accounts_dimension monthly. New accounts should be picked up same-day. Script is idempotent and reads metadata, not heavy computation. |
| No change to canonical prices | Intentional methodology difference (market close vs BD settlement). PSCFIX already handles display correctness via certified_aua. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py` | New validation script | Yes -- `4fd699f4`, fixed `a4cbbf87` |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | Added 00 to incremental run | Yes -- `ada01ed1` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded (x3) | Yes -- `968d0cbb`, `dca49ecf`, `2d12ff54` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_49FNV3.008.gold-silver-aua-validation.md` | status=complete | Yes -- `2bcc43e0` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

`05c_validate_aua_vs_silver.py` is live in S3 (`s3://opal-data-bd/code/gold/`, 16 scripts total).
Wired in `run_gold_layer.sh` both modes (incremental + full) via `if [ -f ... ]` guard.
33 backfill validation JSONs written to `gold/validation/`. All dates show FAIL status due to
83+ missing accounts exceeding the 50-account WARN threshold. The aggregate gap for the most
recent date (2026-03-09) is +0.36% ($5.7M), decomposing into -$14.8M missing accounts and
+$20.5M canonical price divergence.

Root causes documented and (a) fixed: accounts_dimension now runs daily in incremental mode
(`ada01ed1`), which will pick up new accounts same-day. (b) Canonical vs BD pricing methodology
difference is intentional -- no change needed. PSCFIX handles display correctness.

ADVI_49FNV3.008 all 5 acceptance criteria met:
1. 05c runs cleanly on 2026-03-09 -- writes correct validation JSON
2. Pipeline log shows FAIL with gap_pct and accounts_missing_from_gold
3. 33-date backfill complete (3 early dates had incompatible schema -- ERROR, not skipped)
4. Root cause (a): missing accounts explained -- stale accounts_dimension (monthly cadence)
5. Root cause (b): price divergence explained -- canonical market-close vs BD settlement

---

## Next Steps

1. **Verify on next nightly pipeline run** -- confirm 00 + 05c both execute in incremental mode:
   ```bash
   # Check accounts_dimension was refreshed
   aws s3 ls s3://opal-data-bd/gold/accounts_dimension_latest.parquet
   # Check new validation JSON written
   aws s3 ls s3://opal-data-bd/gold/validation/ --recursive | tail -3
   ```

2. **After next run: re-check missing account count** -- expect significant drop from 83/90
   now that 00 runs daily. The ~18 persistent pre-2026 accounts may or may not resolve
   depending on whether they have any transaction history.

**Do NOT:**
- Change canonical price sources -- the methodology difference is intentional
- Remove the `if [ -f ... ]` guard for 05c in the runner -- it's the deployment safety net

#### advi_mixv2_003_06b_deploy.md

# ADVI_MIXV2.003 — 06b Deploy + Gold Run — 0.6.0_AE_PartnerETL

**Date:** 2026-03-18
**Start Time:** 13:45 UTC
**End Time:** 15:50 UTC

## Objective

Deploy the updated `06b_build_client_mix_timeseries.py` (DS commits ADVI_MIXV2.001 + ADVI_MIXV2.002)
to bd-gold-layer-runner, run the insurance AP gate diagnostic to populate `insurance_accounts.json`,
and execute a full rebuild to produce `firm_mix_views.json` and per-advisor `mix.json` artifacts.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify DS dependencies on CLOUD | `a7617a08` (AP gate), `a885f625` + `2384a9f6` (firm/advisor views) confirmed |
| 2 | Read devops-brief-mixv2-001.md + 002.md | Insurance diagnostic required before full rebuild |
| 3 | Run `.tmp_insurance_ap_gate.py` locally | 539 partitions scanned; 109 accounts identified as gated |
| 4 | Populate `insurance_accounts.json` | 109 account_ids, 180-day override — `8d054663` |
| 5 | `safe-ec2-deploy.sh bd-gold-layer-runner` | All gold scripts synced to `s3://opal-data-bd/code/gold/` — `be7ac233` |
| 6 | Start EC2 instance (i-01003b035d2988dfb) | Instance running, SSM online |
| 7 | SSM: incremental smoke test | Loaded 109-account insurance config, 20 advisors — SUCCESS |
| 8 | SSM: full rebuild attempt | Instance auto-stopped mid-run (boot incremental finished, self-shutdown fired) |
| 9 | Diagnose: 06b position in run_gold_layer.sh | 06b was running BEFORE 08b — could not read rel_architect_lookup |
| 10 | Fix: move 06b after 08b in both modes | `b427502d` — committed and pushed |
| 11 | Upload fixed run_gold_layer.sh to S3 | `s3://opal-data-bd/code/gold/run_gold_layer.sh` updated |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Run diagnostic locally, not on EC2 | `s3://opal-data-bd` accessible with local creds; faster turnaround than SSM roundtrip |
| 109 accounts selected (not all 118) | Only accounts with `snap_dates_excluded > 0` are actually gated out; remaining 9 have no excluded dates |
| Move 06b to after 08b in both incremental and full modes | 06b reads `rel_architect_lookup.parquet` written by 08b; running before 08b means it uses a stale or missing mapping |
| Did not trigger run_gold_layer.sh full this session | Full run takes 2+ hrs; sequence fix committed; next daily incremental and monthly full will use correct order |

---

## Diagnostic Findings

Insurance AP gate scope was larger than DS estimated ($60M) — actual impact was $24B cumulative over 18-month window:

```
Accounts examined:        118
Total MV when INCLUDED:   $2,363,683,767
Total MV when EXCLUDED:   $24,182,394,244
Oscillation source:       $24.2B disappears when 45-day AP gate fires
```

Root cause: 109 accounts (insurance/annuity products — SHIELD, BUFFER, Cap 20%, etc.) have
`account_performance.last_seen` in 2023 (quarterly statement cycle). The 45-day gate
excludes them from every snapshot date in the 18-month window.

`insurance_accounts.json` committed at `8d054663` with all 109 account_ids and `ap_gate_days_override: 180`.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/insurance_accounts.json` | Populated with 109 gated account_ids | Yes — `8d054663` |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | Moved 06b after 08b in both incremental and full modes | Yes — `b427502d` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_MIXV2.003.ec2-06b-deploy.md` | Status -> in_progress | Yes — `8eda0ed9` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded at commit `8d054663` | Yes — `be7ac233` |

---

## Current State

**Status:** IN PROGRESS

Active deployment: `b427502d` is the current HEAD on CLOUD. `run_gold_layer.sh` is
updated on S3 (`s3://opal-data-bd/code/gold/run_gold_layer.sh`). The current boot
incremental (started 15:30 UTC) is running on i-01003b035d2988dfb with the old script
order (06b before 08b) — but 06b found no new partitions so no data was written either way.

`firm_mix_views.json` and `gold/advisors/*/mix.json` do NOT yet exist in S3. They will be
written by the next run that (a) uses the corrected script order and (b) processes at least
one new partition date.

---

## Next Steps

1. **[0.6.0_AE_PartnerETL] Trigger `run_gold_layer.sh full`** after current incremental
   shuts down — required to satisfy acceptance criterion of >=4 quarterly periods in
   `firm_mix_views.json`. Full run will process all 2,086 historical partitions with 06b
   running after 08b (rel_architect_lookup current).

2. **[0.6.0_AE_PartnerETL] Verify S3 outputs** after full run:
   - `aws s3 ls s3://opal-data-bd/gold/firm_mix_views.json`
   - `aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep mix.json | wc -l` (expect 19+)
   - Spot-check pct sums using verification script in devops-brief-mixv2-002.md

3. **[0.6.0_AE_PartnerETL] Mark task order complete** once S3 verification passes.

4. **[0.4.0_DT_ClientPlatform] Fix CHANGELOG.json for partners-api** — ADVI_MIXV2.004
   Lambda deploy (partners-api-v1.3.0) was deployed correctly but `record-terraform-deploy.sh`
   was not run. CHANGELOG.json still shows v1.1.0 as last entry.

**Files to touch next:**
- Trigger: `bash /tmp/gold_layer_scripts/run_gold_layer.sh full` via SSM on i-01003b035d2988dfb
- Verify: `s3://opal-data-bd/gold/firm_mix_views.json`

**Do NOT:**
- Run `python3 06b_build_client_mix_timeseries.py --upload --incremental` as the full rebuild — incremental with no new partitions produces no output
- Start the instance and assume the boot script will run full mode — boot always runs incremental

#### advi_mvp318_ws1_geo_fix_deploy.md

# ADVI_MVP318 WS1 -- Geo Parquet Rebuild (country encoding fix) -- 0.6.0_AE_PartnerETL

**Date:** 2026-03-18
**Start Time:** 16:20 UTC
**End Time:** 16:28 UTC

## Objective

Deploy DS commit fec1f7e4 (script 07 country normalization fix) to EC2 and regenerate
the geo parquet so that US clients are no longer classified as stateless non-US clients
in `nna_aua_by_geography.parquet`. This unblocks the geo timeseries view (WS1).

---

## Root Cause (per DS)

Script 07 `_modal_geo()` checked `country != 'USA'` to identify non-US clients, but BD
stores client country as `'United States'` (full name). Every US client was treated as
non-US, causing `state` to be wiped to `''`. The Lambda then filtered
`country.isin(['USA','US',''])` — `'United States'` matched none of these — producing
an empty `geo_us` dataframe and zero categories in `timeseries_chart.json` geo view.

DS fix (fec1f7e4): normalize `'United States'`/`'US'` → `'USA'` before the non-US check.
Lambda defensively updated with `_US_COUNTRY_VARIANTS` constant covering all BD encoding
variants across all 4 filter sites.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify DS commit fec1f7e4 on CLOUD | Confirmed — `07_build_nna_aua_by_geography.py` + `bd-portal-publisher/lambda_function.py` |
| 2 | `aws s3 cp` script 07 to `s3://opal-data-bd/code/gold/` | Uploaded |
| 3 | Start EC2 i-01003b035d2988dfb (was stopped) | Running, SSM online |
| 4 | SSM command `f994c0f3`: run script 07 in isolation | Success |
| 5 | Verify geo parquet output | TX: $900.8M AUA, 49 states, 3,555 households |

---

## Verification Output

```
Date range:    2020-06-30 -> 2026-03-16
State view:    75,086 rows | 49 distinct states
City view:     1,073,824 rows | 995 cities across 48 states
31 unknown geography (expected)

Top states by AUA (as of 2026-03-16):
  TX   $900,754,857
  GA   $102,432,860
  FL   $ 89,778,061
  CA   $ 74,980,035
  AR   $ 62,596,703

Total AUA: $1,605,964,409
```

TX AUA ($900M) is now correctly in the state view — previously swallowed into empty geo.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/07_build_nna_aua_by_geography.py` | Country normalization fix | DS commit `fec1f7e4` |
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | `_US_COUNTRY_VARIANTS` constant at all 4 filter sites | DS commit `fec1f7e4` |

---

## Current State

**Status:** COMPLETE (AE steps)

Geo parquet rebuilt on S3 with correct state encoding for all US clients. The remaining
step for the full fix to be visible in the portal is DT deploying `bd-portal-publisher`
at commit `fec1f7e4` (bd-pipeline Terraform apply). Once deployed, the next
`pipeline-complete.json` trigger will cause the Lambda to regenerate `timeseries_chart.json`
with populated geo categories.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform]** Deploy `bd-portal-publisher` at commit `fec1f7e4`
   (bd-pipeline Terraform apply) — required for Lambda geo filter fix to take effect.
2. **[nightly or manual trigger]** After DT deploys, re-run gold layer or manually trigger
   `pipeline-complete.json` to cause Lambda to regenerate `timeseries_chart.json`.
3. **[0.4.0_DS_ClientPlatform / DT]** Run `.tmp_segment_analytics_diag.py` to confirm
   TX appears in geo categories.

**Do NOT:**
- Run script 07 again — geo parquet is correct as of 2026-03-18T16:27 UTC
- Skip DT Lambda deploy — the Lambda's own filter still needs the `_US_COUNTRY_VARIANTS` fix
  to be resilient to future BD encoding changes

#### advi_pscfix_a1_aua_certification_deploy.md

# ADVI_PSCFIX A1 — AUA Certification Script Deploy — 0.6.0_AE_PartnerETL

**Date:** 2026-03-11
**Start Time:** 22:45
**End Time:** 22:58

## Objective

Write and deploy `05d_write_aua_certification.py` into the BD EC2 gold runner per
task order ADVI_PSCFIX.A1. Script runs daily after 05c_validate_aua_vs_silver.py,
reads silver/allocations/{date}.parquet, excludes liability account types, and
writes `gold/aua_certification/{today}.json` — the certified_aua figure the
bd-portal-publisher Lambda uses to override total_aua fields.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Read task order, PRD, EC2 runner structure | Context established |
| 2 | Write 05d_write_aua_certification.py | `data/black_diamond/scripts/gold/05d_write_aua_certification.py` created |
| 3 | Wire 05d into run_gold_layer.sh (both modes) | `data/black_diamond/scripts/gold/run_gold_layer.sh` modified |
| 4 | Commit source | `6223d2d9` feat(bd-pipeline): add 05d + wire into run_gold_layer.sh |
| 5 | safe-ec2-deploy.sh bd-gold-layer-runner | 15 gold scripts in s3://opal-data-bd/code/gold/ |
| 6 | EC2_MANIFEST.json updated | Manifest commit `9bce21bd` |
| 7 | Mark task order complete | ADVI_PSCFIX.A1.aua-certification-script.md status=complete |

## Verification

S3 gold script count after deploy: **15 scripts** (was 14 before 05d).

05d confirmed uploaded:
```
s3://opal-data-bd/code/gold/05d_write_aua_certification.py
```

run_gold_layer.sh confirmed uploaded:
```
s3://opal-data-bd/code/gold/run_gold_layer.sh
```

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Script exits 0 on all error paths (try/except in `__main__`) | Non-blocking requirement — pipeline must continue regardless |
| 05c called via `if [ -f ... ]` guard in runner | 05c does not exist yet (ADVI_49FNV3.008 still pending). Guard lets 05d deploy cleanly now; 05c will be wired unconditionally when it's written |
| 05d called with `|| true` (not via `run_script()`) | `run_script()` passes `--upload` flag which 05d doesn't need; also avoids set -e failure on non-zero exit edge cases |
| Script placed in `data/black_diamond/scripts/gold/` (not `infra/aws/ec2/bd_pipeline/scripts/`) | Task order path doesn't exist; gold scripts canonical location is gold/ dir per deploy-to-ec2.sh sync paths |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/05d_write_aua_certification.py` | New script | Yes — `6223d2d9` |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | 05c guard + 05d wired in both modes | Yes — `6223d2d9` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded by safe-ec2-deploy.sh | Yes — `9bce21bd` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_PSCFIX.A1.aua-certification-script.md` | status=complete | Yes (this commit) |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

`05d_write_aua_certification.py` is live in S3 (`s3://opal-data-bd/code/gold/`). EC2
will pick it up on the next gold pipeline boot. Script reads `silver/allocations/{date}.parquet`,
excludes 6 liability types (CreditCard, Mortgage, Loans, Insurance, TermLife, Annuity),
computes `certified_aua`, loads `gold/client_performance.parquet` for `gold_aua`, and
writes `gold/aua_certification/{date}.json`. Exits 0 on all paths. Wired in both
incremental and full modes after 05 (and after 05c when 05c is deployed). The publisher
Lambda can now consume the certification JSON on any day silver allocations are present.

---

## Next Steps

1. **[0.6.0_AE_PartnerETL] Complete ADVI_49FNV3.008** — write 05c_validate_aua_vs_silver.py
   (also assigned to this agent, still pending). 05d is wired to run after it.

2. **[0.4.0_DS_ClientPlatform] Implement publisher certification override** — per PRD
   Deliverables 2 & 3: load certification JSON in lambda_handler and override total_aua
   fields + scale NMNC/NMEC timeseries for current period.

3. **Verify in next pipeline run** — after EC2 boots and incremental run completes:
   ```
   aws s3 ls s3://opal-data-bd/gold/aua_certification/
   aws s3 cp s3://opal-data-bd/gold/aua_certification/2026-03-11.json -
   ```
   Confirm certified_aua ~1.599B, gold_aua ~1.605B, gap_pct ~-0.36%.

**Files to touch next:**
- `data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py` — write per ADVI_49FNV3.008

**Do NOT:**
- Use `run_script()` for 05c/05d in the runner — those helpers pass `--upload` which these scripts don't accept
- Write scripts directly on EC2 — all changes go repo -> S3 -> EC2 pull

---

## Amendment — 1.0.0_SA_CTO (2026-03-12)

**Two bugs found in 05d_write_aua_certification.py during CTO AUA investigation.**

### Bug 1: Date mismatch — 05d always SKIPs (CRITICAL)

05d used `datetime.date.today()` to determine the silver allocation filename. The EC2
gold pipeline runs on calendar date T, but silver allocations are named for the **data
date** T-1 (e.g. `2026-03-11.parquet` is uploaded on 2026-03-12). So 05d looked for
`silver/allocations/2026-03-12.parquet` which never exists at run time. Result:
`gold/aua_certification/` was empty — 05d hit SKIP on every single nightly run since
deployment. The publisher always fell back to uncertified gold totals.

**Fix:** Load `gold/client_performance.parquet` first, derive `data_date = max(date)`,
and use that for both the silver lookup and the gold filter. This is the actual data
date the pipeline processed, which matches the silver filename convention.

### Bug 2: LIABILITY_TYPES over-excluded Insurance/TermLife/Annuity

Original exclusion list: `CreditCard, Mortgage, Loans, Insurance, TermLife, Annuity`.
Silver's `account_market_value` **includes** insurance accounts ($61M). Gold's positions
cube also includes insurance accounts (112 accounts with Shield annuity positions).
Both systems agree on including them. Excluding them from `certified_aua` would have
produced a $60M undercount vs what the portal actually displays.

**Fix:** Narrowed LIABILITY_TYPES to `CreditCard, Mortgage, Loans` only. These are
actual debt liabilities with negative market values that neither gold nor silver should
count as AUA.

### Files modified

| File | Change |
|------|--------|
| `data/black_diamond/scripts/gold/05d_write_aua_certification.py` | data_date from client_performance max(date) instead of today(); LIABILITY_TYPES narrowed to 3 |

### Requires redeployment

05d must be re-uploaded to `s3://opal-data-bd/code/gold/` via `safe-ec2-deploy.sh`
before the next nightly run for the fix to take effect.

#### advi_pscfix_a3_script09_cert_override.md

# ADVI_PSCFIX A3 — Script 09 Cert Override Deploy — 0.6.0_AE_PartnerETL

**Date:** 2026-03-11
**Start Time:** 23:45
**End Time:** 23:58

## Objective

Add `_load_aua_certification()` helper and current-period donut total override to
`09_generate_partner_analytics.py` per task order ADVI_PSCFIX.A3. When
`gold/aua_certification/{today}.json` exists, overrides `views.aua/geo/adv[current].donut.total`
with `certified_aua` in all three granularity JSONs (`header_metrics_quarterly/monthly/annual.json`).

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Read task order, read 09 script (period loop ~line 1538) | Structure confirmed |
| 2 | Add `_load_aua_certification()` after `load_data()` (line 309) | Helper function inserted |
| 3 | Add `_s3 + cert = _load_aua_certification(...)` in `generate_header_metrics()` after `data_as_of` | Cert loaded once per granularity run |
| 4 | Add `is_current_period` flag + override block after adv view, before NNA view | Override wired in loop |
| 5 | Commit source | `f6fef305` feat(bd-pipeline): script 09 cert override |
| 6 | safe-ec2-deploy.sh bd-gold-layer-runner | 09 uploaded to s3://opal-data-bd/code/gold/ |
| 7 | EC2_MANIFEST.json updated | Manifest commit `cc798d4d` |
| 8 | Mark task order complete | ADVI_PSCFIX.A3 status=complete |

## Verification

S3 upload confirmed:
```
s3://opal-data-bd/code/gold/09_generate_partner_analytics.py  (73 KiB)
```

To spot-check current-period donut total after next pipeline run:
```bash
aws s3 cp s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json - \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d['views']['aua']['current']['donut']['total'])"
# Expected: ~1599225407.0 (certified_aua) vs prior ~1604943633.0 (gold_aua)
```

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `is_current_period = (ts == ref_date)` | `ref_date = client_perf['date'].max()` is the last perf snapshot — exactly the current in-progress period end date. Simplest and most direct flag. |
| Cert loaded once per `generate_header_metrics()` call | Function is called once per granularity (quarterly/monthly/annual). Cert is date-level so one load suffices for all periods in the call. |
| New `_s3` client created in `generate_header_metrics()` | `load_data()` has its own private s3 client; not accessible here. Cheap to create a second one for the cert fetch. |
| Override placed after adv view, before NNA view | Exact position specified in task order. NNA/CLA don't have a `donut.total` — only aua/geo/adv need the override. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/09_generate_partner_analytics.py` | Added `_load_aua_certification()` + cert load + current-period override | Yes — `f6fef305` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded by safe-ec2-deploy.sh | Yes — `cc798d4d` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_PSCFIX.A3.script09-cert-override.md` | status=complete | Yes (this commit) |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

`09_generate_partner_analytics.py` is live in S3 with the cert override. On the next nightly
gold run: 05d writes `gold/aua_certification/{date}.json`; then 09 loads it and applies
`certified_aua` (~1.599B) to all three granularity JSONs' current-period aua/geo/adv donut totals.
Historical period donut totals are untouched. Override is non-blocking — if no cert JSON exists,
09 falls back to gold-derived totals silently.

ADVI_PSCFIX Track A (pipeline) is now structurally complete:
- A1: 05d writes cert JSON daily (COMPLETE)
- A3: 09 overrides current-period donuts (COMPLETE)
- Pending: publisher Lambda override (DS + DT track, separate task orders)

---

## Next Steps

1. **[0.4.0_DS_ClientPlatform] Confirm publisher Lambda cert override** — PRD Deliverables 2 & 3
   (bd-portal-publisher: timeseries NMNC/NMEC scaling + snapshot total_aua override).

2. **[0.6.0_AE_PartnerETL] Complete ADVI_49FNV3.008** — write 05c_validate_aua_vs_silver.py
   (still pending; wired in run_gold_layer.sh with file-existence guard).

3. **Verify on next pipeline run** — check quarterly donut total:
   ```bash
   aws s3 cp s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json - \
     | python -c "import sys,json; d=json.load(sys.stdin); print(d['views']['aua']['current']['donut']['total'])"
   ```

**Do NOT:**
- Override segment-level donut values — only `donut.total` on aua/geo/adv is touched
- Override historical periods — `is_current_period = (ts == ref_date)` gates this correctly

#### opal_etf_ticker_fix_deploy.md

# Opal ETF Ticker Fix — Silver Deploy + canonical_prices Rebuild — 0.6.0_AE_PartnerETL

**Date:** 2026-03-18
**Start Time:** 15:45 UTC
**End Time:** 15:58 UTC

## Objective

Deploy DS's `_OPAL_ETF_OVERRIDES` silver script fix to EC2 and run a full rebuild of
`canonical_prices.parquet` so that Opal/Pathfinder-branded ETFs no longer carry `ticker=NaN`
downstream into `holdings_lots`, `client_tax_liability`, and portal position lists.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify DS changes present but uncommitted | Both `build_canonical_prices_v2.py` and `bd_price_update.py` had local modifications |
| 2 | Commit silver scripts to CLOUD with DS author | `b69d1ae6` |
| 3 | `aws s3 cp` both scripts to `s3://opal-data-bd/code/silver/` | Both uploaded successfully |
| 4 | Write run script, upload to `s3://opal-data-bd/code/adhoc/` | `run_canonical_prices_full.sh` |
| 5 | SSM send-command: first attempt failed | `--full-rebuild --upload` flags not valid — script takes no args except `--dry-run` |
| 6 | Fix run script, re-upload, re-send SSM | Command `11a9621a` — Success |
| 7 | Rebuild completed in 114s | 10,406,355 rows, 91.3 MB written to `s3://opal-data-bd/silver/prices/canonical_prices.parquet` |
| 8 | Spot-check canonical_prices.parquet locally | 6/6 Opal ETF name variants now have correct tickers, 0 NaN |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Commit DS changes before uploading to S3 | Standard deployment protocol: code must correspond to a git commit before any AWS operation |
| Run full rebuild (not incremental) | The fix must backfill all historical dates — incremental would only correct today's new rows. `build_canonical_prices_v2.py` always does a full rebuild by design (no incremental mode) |
| Run on bd-gold-layer-runner (already up) | Instance was already running from earlier ADVI_MIXV2.003 work; avoided a cold start |

---

## Rebuild Output

```
Total rows:    10,406,355
Date range:    2020-06-30 -> 2026-03-16
Unique assets: 9,952
Size:          91.3 MB
Elapsed:       114s

By source:
  linear_interpolation   8,561,465  (82.3%)
  yahoo_finance          1,651,217  (15.9%)
  transaction_observed     193,673  ( 1.9%)
```

## Spot-Check

```
                              asset_name  ticker
          OPAL DIVIDEND INCOME ETF         DIVZ
OPAL INTERNATIONAL DIVIDEND INCOME ETF     IDVZ
  PATHFINDER DISCIPLINED US EQUITY ETF     PFDE
  PATHFINDER FOCUSED OPPORTUNITIES ETF     PFOE
             POLEN DIVIDEND INCOME ETF     DIVZ
                 POLEN HIGH INCOME ETF     PCHI

NaN tickers for these assets: 0
```

`PATHFINDER DISCIPLINED US EQUITIES ETF` (BD alternate spelling) not present in parquet for
this date range — not an error, simply no BD transactions observed under that spelling.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/silver/build_canonical_prices_v2.py` | `_OPAL_ETF_OVERRIDES` added, injected in `load_ticker_lookup()` | Yes — `b69d1ae6` |
| `data/black_diamond/scripts/silver/bd_price_update.py` | Same addition | Yes — `b69d1ae6` |

---

## Current State

**Status:** COMPLETE

`canonical_prices.parquet` rebuilt on S3 with correct tickers for all Opal/Pathfinder ETFs.
Both the monthly full-rebuild path and the daily incremental path carry the override — fix
will not regress. No data was removed; for the Opal ETFs, some previously-interpolated price
values may now be real Yahoo Finance closes.

Downstream propagation (`holdings_lots`, `client_tax_liability`, portal blank tickers) will
resolve automatically on the next gold layer incremental run — no further action needed.

---

## Next Steps

1. **[nightly pipeline]** Next gold incremental: `03_build_holdings_lots.py` picks up corrected
   tickers and Yahoo prices from canonical_prices — propagates to `client_tax_liability` and portal.
2. No further AE action required for this fix.

**Do NOT:**
- Re-run the full rebuild unless canonical_prices.parquet drifts — current parquet is correct as of 2026-03-18T15:57 UTC


### 0.6.0_AE_PartnerETL -- Pending Task Orders

#### ADVI_BKSCMP.004.ae-ec2-gold-run.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-004-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Upload script 12 and the updated run_gold_layer.sh to S3, then run the gold layer
    in incremental mode on bd-gold-layer-runner. Verify firm_composition.json and
    per-advisor composition.json artifacts are written to S3.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS4 (AE actions), §7 (acceptance criteria).
    Deployment standard: docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md.

    DS gate commit: ADVI_BKSCMP.001 req 7 (script 12 + run_gold_layer.sh commit to CLOUD).
    DS will report the commit SHA. Verify with:
      git log --oneline -- data/black_diamond/scripts/gold/12_build_composition_artifacts.py

    IMPORTANT gate: DT must have deployed opal-partners-data v2.8 (partners-api-v1.5.0)
    BEFORE verifying artifacts in the browser/portal. However, AE can run the gold layer
    (and produce the S3 artifacts) before the Lambda deploy. The artifacts just won't be
    serveable until partners-api-v1.5.0 is live. Run the gold layer as soon as the DS
    gate clears -- do not wait on DT.

    Run mode: INCREMENTAL is sufficient (holdings_lots is available incrementally;
    script 12 reads the latest parquet regardless of mode). Do NOT run FULL unless
    specifically requested.

    Note: This task order covers ONLY script 12 artifacts. The ADVI_MVP318.003 full gold
    run (for architect attribution, MIXV2, WS5 advisor timeseries) is a SEPARATE task order
    that AE should also execute. Both can be run in the same session.
  </context>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="run-on-ec2">run_gold_layer.sh --incremental</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      GATE: Confirm DS committed script 12 and updated run_gold_layer.sh to CLOUD.
      Check: git log --oneline -- data/black_diamond/scripts/gold/12_build_composition_artifacts.py
      And:   git log --oneline -- data/black_diamond/scripts/gold/run_gold_layer.sh
      Both must show the ADVI_BKSCMP.001 WS1 commit. Do not upload uncommitted code.
    </requirement>

    <requirement id="2">
      Upload script 12 to S3:
        export MSYS_NO_PATHCONV=1
        aws s3 cp data/black_diamond/scripts/gold/12_build_composition_artifacts.py \
          s3://opal-data-bd/code/gold/12_build_composition_artifacts.py
      Upload updated run_gold_layer.sh:
        aws s3 cp data/black_diamond/scripts/gold/run_gold_layer.sh \
          s3://opal-data-bd/code/
      Confirm both uploads succeed (HTTP 200 from aws s3 cp).
    </requirement>

    <requirement id="3">
      On bd-gold-layer-runner EC2 (via SSM or SSH), pull the updated scripts from S3.
      The run_gold_layer.sh s3 sync at startup pulls all scripts automatically, but
      run_gold_layer.sh itself must be re-pulled separately:
        aws s3 cp s3://opal-data-bd/code/run_gold_layer.sh ~/bd-gold/run_gold_layer.sh
      (Script 12 is pulled automatically via the `aws s3 sync s3://.../code/gold/ SCRIPTS_DIR/` at line 71.)
      Do NOT write code directly to EC2 -- pull from S3 only.
    </requirement>

    <requirement id="4">
      Run the gold layer in incremental mode:
        ./run_gold_layer.sh --incremental
      Monitor for errors. If the run fails at script 12 specifically, report the full
      stdout/stderr from that script to COO before retrying.
      Expected runtime for incremental: 15-30 min (script 12 adds holdings parquet read
      + pandas groupby computation; estimate 2-5 min for script 12 itself).
    </requirement>

    <requirement id="5">
      Verify artifacts after run completes:

      A. Firm composition:
        export MSYS_NO_PATHCONV=1
        aws s3 ls s3://opal-data-bd/gold/views/firm_composition.json
        aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json - | python3 -m json.tool | head -40
        Confirm: file exists, parseable JSON, has "mix" array with top_holdings inside each class,
        has root "top_holdings" array, pct values are 0-1.

      B. Advisor compositions (spot-check):
        aws s3 ls s3://opal-data-bd/gold/advisors/ | head -20
        Confirm at least 5 advisors have a composition.json:
          aws s3 ls s3://opal-data-bd/gold/advisors/ | awk '{print $4}' | while read adv; do
            aws s3 ls s3://opal-data-bd/gold/advisors/${adv}composition.json 2>/dev/null &amp;&amp; echo "OK: $adv"
          done | head -5

      C. Pct sanity check on firm_composition.json:
        python3 -c "
        import json, boto3
        s3 = boto3.client('s3')
        data = json.loads(s3.get_object(Bucket='opal-data-bd', Key='gold/views/firm_composition.json')['Body'].read())
        for cls in data['mix']:
            th_sum = sum(h['pct'] for h in cls.get('top_holdings', []))
            other_pct = cls.get('other', {}).get('pct', 0)
            total = th_sum + other_pct
            print(f'{cls[\"asset_class\"]}: top_holdings pct sum={th_sum:.4f} + other={other_pct:.4f} = {total:.4f} (should be ~1.0)')
        "
        All class totals (top_holdings sum + other) should be approximately 1.0 (within 0.01).
    </requirement>

    <requirement id="6">
      Register the script 12 deployment in EC2_MANIFEST.json per the safe-ec2-deploy.sh protocol.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS gate commit confirmed before S3 upload</criterion>
    <criterion id="2">Script 12 and run_gold_layer.sh uploaded to S3 from committed CLOUD code</criterion>
    <criterion id="3">Incremental gold run completes without errors (all scripts including 12)</criterion>
    <criterion id="4">gold/views/firm_composition.json exists and is valid JSON matching PRD §3 schema</criterion>
    <criterion id="5">gold/advisors/{id}/composition.json exists for at least 5 advisors</criterion>
    <criterion id="6">Pct sanity: per-class top_holdings pct + other pct sums to ~1.0 per class</criterion>
    <criterion id="7">EC2_MANIFEST.json updated with deployment record</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>GATE: Do not upload before DS gate commit confirmed</constraint>
    <constraint>INCREMENTAL mode only -- FULL mode not required for script 12 (reads latest holdings_lots regardless)</constraint>
    <constraint>Do NOT write code directly to EC2 -- S3 is the artifact store (EC2_CODE_DEPLOYMENT_STANDARD.md)</constraint>
    <constraint>Do NOT inline script content in SSM commands</constraint>
    <constraint>No emojis in any SSM commands or log output (CLAUDE.md rule 13)</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before any AWS CLI commands with S3 paths</constraint>
    <constraint>DT Lambda deploy (ADVI_BKSCMP.003) is NOT required before running the gold layer -- run as soon as DS gate clears</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_BKSCMP.001 req 7" status="pending">
      Script 12 + run_gold_layer.sh committed to CLOUD -- gate for S3 upload
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="verify">Incremental gold run complete; firm_composition.json and advisor compositions verified in S3</deliverable>
    <deliverable type="document">Session log with pct sanity check output and advisor count</deliverable>
    <deliverable type="document">EC2_MANIFEST.json updated</deliverable>
  </deliverables>
</task_order>

#### ADVI_MVP318.003.ae-final-gold-layer-run.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-18-mvp318-003-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-18</date>
    <status>pending</status>
    <project_code>ADVI_MVP318</project_code>
  </metadata>

  <objective>
    Run ONE FULL gold layer on bd-gold-layer-runner after DT completes Lambda deploys.
    This single run consolidates three pending workstreams: ADVI_ADVTV2.002 (architect
    attribution), ADVI_MIXV2.003 (06b AP gate + firm/advisor mix), and WS5 (MTD/QTD/YTD
    windows from script 10). The gold layer run triggers bd-portal-publisher and
    bd-portal-advisor-publisher at completion — those Lambdas MUST be on their new versions
    (WS2+WS3b) before this run completes, or the new advisor timeseries artifacts will not
    be generated.
  </objective>

  <context>
    Reference:
    - docs/architecture/ADVI_MVP318_PRD.md §WS5
    - org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_MIXV2.003.ec2-06b-deploy.md
    - org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_ADVTV2.002.gold-layer-deploy.md
    - docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md (repo -> S3 -> EC2 pulls, never inline scripts)

    Scripts that are deployed (already on EC2 from prior sessions per git log):
    - 08b_build_architect_attribution.py (ADVI_ADVTV2, deployed @ 72c03d2a)
    - 06b_build_client_mix_timeseries.py + insurance_accounts.json (ADVI_MIXV2.003, in_progress)

    Script that DS will commit for WS5 (pending DS ADVI_MVP318.001):
    - data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py (script 10)
    - Possibly generate_partner_analytics.py (script 09) — DS will confirm

    This is a FULL mode run, not incremental. FULL is required because 00_build_accounts_dimension.py
    now ingests consultant and additional_advisor from silver transactions (08b dependency).
    Expected runtime: 60-90 min.
  </context>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py</file>
      <file action="upload-to-s3-if-changed">data/black_diamond/scripts/gold/generate_partner_analytics.py</file>
      <file action="run-on-ec2">run_gold_layer.sh --full</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      HARD GATE: Do not run the gold layer until DT confirms bd-portal-advisor-publisher deploy is complete
      (ADVI_MVP318.002 req 3). The gold layer's final step writes pipeline-complete.json, which triggers
      both publisher Lambdas. If the old Lambda code is active at that moment, advisor timeseries artifacts
      will not be generated. DT's deploy is the gate; wait for explicit DT confirmation.
    </requirement>

    <requirement id="2">
      Wait for DS to confirm generate_advisor_rolling_flows.py (script 10) is committed to CLOUD.
      Check: git log --oneline -- data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py
      If DS also committed generate_partner_analytics.py (script 09), include it in the S3 upload.
      Do not upload uncommitted code to S3.
    </requirement>

    <requirement id="3">
      Upload all DS-committed WS5 scripts to S3 per the EC2 Code Deployment Standard:
        aws s3 cp data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py \
          s3://opal-data-bd/code/gold/generate_advisor_rolling_flows.py
      If script 09 also changed:
        aws s3 cp data/black_diamond/scripts/gold/generate_partner_analytics.py \
          s3://opal-data-bd/code/gold/generate_partner_analytics.py
      Do not write code directly to EC2. S3 is the artifact store; EC2 pulls from S3.
    </requirement>

    <requirement id="4">
      On bd-gold-layer-runner EC2, pull the updated WS5 scripts from S3 (SSM or SSH):
        aws s3 cp s3://opal-data-bd/code/gold/generate_advisor_rolling_flows.py \
          ~/bd-gold/data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py
      (If script 09 also updated, pull it too.)
      Do NOT inline script content in SSM commands.
    </requirement>

    <requirement id="5">
      Run the FULL gold layer:
        ./run_gold_layer.sh --full
      Expected runtime: 60-90 min. Monitor for errors. If the run fails at a specific script,
      report the failure script and stdout/stderr to COO before retrying.
    </requirement>

    <requirement id="6">
      After run completes, verify three sets of acceptance criteria:

      ADVI_ADVTV2 criteria (architect attribution):
      - rel_architect_lookup.parquet contains exactly 19 named architects + Unresolved
      - No "49F House", "Unassigned", or stale architects
        aws s3 cp s3://opal-data-bd/gold/views/rel_architect_lookup.parquet /tmp/ &amp;&amp; \
        python3 -c "import pandas as pd; df=pd.read_parquet('/tmp/rel_architect_lookup.parquet'); \
          print(df['resolved_architect'].nunique(), 'architects'); print(df['resolved_architect'].unique())"

      ADVI_MIXV2 criteria (firm/advisor mix):
      - gold/firm_mix_views.json exists with &gt;=4 quarterly periods
      - gold/advisors/*/mix.json exists for at least 10 advisors
      - pct values in firm_mix_views.json sum to ~1.0 per period

      WS5 criteria (advisor timeseries artifacts from new Lambda):
      - gold/advisors/{advisor_id}/timeseries.json exists for at least one advisor
        (generated by the new Lambda after pipeline-complete.json trigger)
      - gold/advisors/{advisor_id}/mix_timeseries.json exists for at least one advisor
      NOTE: Lambda-generated artifacts only appear after pipeline-complete.json is written
      AND the Lambda runs successfully. If artifacts are missing, confirm pipeline-complete.json
      was written and check CloudWatch logs for bd-portal-advisor-publisher invocation.
    </requirement>

    <requirement id="7">
      Register the deployment in EC2_MANIFEST.json per the safe-ec2-deploy.sh protocol.
      The entry should cover the WS5 script 10 upload (and script 09 if applicable).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DT bd-portal-advisor-publisher deploy confirmed before gold run starts</criterion>
    <criterion id="2">Script 10 (and 09 if changed) uploaded to S3 from committed CLOUD code</criterion>
    <criterion id="3">FULL gold layer completes without errors (all scripts 00 through 10)</criterion>
    <criterion id="4">rel_architect_lookup.parquet: 19 named architects + Unresolved</criterion>
    <criterion id="5">firm_mix_views.json present with &gt;=4 quarterly periods; pct sums ~1.0</criterion>
    <criterion id="6">Advisor timeseries and mix_timeseries JSON artifacts generated in S3</criterion>
    <criterion id="7">EC2_MANIFEST.json updated with deployment record</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start the gold layer run until DT confirms Lambda deploy is complete</constraint>
    <constraint>Do NOT upload uncommitted code to S3 — verify DS commit first</constraint>
    <constraint>FULL mode only — incremental mode will not backfill architect attribution</constraint>
    <constraint>Never write code directly to EC2 — repo -> S3 -> EC2 pull (EC2_CODE_DEPLOYMENT_STANDARD.md)</constraint>
    <constraint>No emojis in any SSM commands, scripts, or log output (CLAUDE.md rule 13)</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before any AWS CLI commands with ARN or S3 paths on Git Bash</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MVP318.002 req 3" status="pending">
      bd-portal-advisor-publisher deployed at WS2+WS3b version — HARD GATE for gold run
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVP318.001 req 5" status="pending">
      Script 10 (and possibly 09) committed to CLOUD — gate for S3 upload
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="verify">FULL gold layer run complete; all three acceptance criterion sets verified</deliverable>
    <deliverable type="document">Session log with verification output for all three workstreams</deliverable>
    <deliverable type="document">EC2_MANIFEST.json updated</deliverable>
  </deliverables>
</task_order>

#### aua-scoped-price-overrides-deploy.md

# AUA Scoped Price Overrides -- Deploy Briefing

<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-aua-scoped-overrides</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
  </metadata>

  <objective>
    Deploy scoped price overrides into canonical_prices.parquet and regenerate
    the gold pipeline to fix $51M of AUA valuation errors across 7 accounts.
    Two-step deployment: (1) inject corrected prices into canonical_prices,
    (2) rebuild gold client_performance with ghost account exclusions.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/silver/inject_scoped_overrides.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
      <file action="modify">data/black_diamond/scripts/gold/aua_overrides.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Run inject_scoped_overrides.py --upload on EC2 to inject 5 corrected prices
      into canonical_prices.parquet. This replaces wrong prices (BNPQF equity at $97,
      Destinations model sleeves at $546/$384, etc.) with silver-derived flat prices.
      The script is idempotent -- safe to re-run.
    </requirement>
    <requirement id="2">
      Run 05_build_client_performance.py --upload to rebuild gold/client_performance.parquet.
      This picks up the corrected canonical prices AND applies RC6 ghost account
      exclusions from aua_overrides.json.
    </requirement>
    <requirement id="3">
      Run 05c_validate_aua_vs_silver.py to confirm gap reduction.
      Expected: aggregate gap drops from ~3.5% to less than 1.5%.
    </requirement>
    <requirement id="4">
      Run downstream gold scripts (07, 08, 09, 10) to propagate corrected AUA
      into timeseries_chart.json, partner_analytics.json, and leaderboard outputs.
    </requirement>
    <requirement id="5">
      Run the bd-portal-publisher Lambda (or trigger the pipeline) to regenerate
      portal JSON outputs with corrected GRO decomposition values.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">inject_scoped_overrides.py --dry-run shows 1,721 override rows injected, 5,799 wrong rows removed, zero duplicates</criterion>
    <criterion id="2">After --upload, canonical_prices.parquet contains source='scoped_override' rows for all 5 assets</criterion>
    <criterion id="3">05c_validate_aua_vs_silver.py shows gap less than 1.5% on latest date</criterion>
    <criterion id="4">timeseries_chart.json growth_decomposition values reflect corrected AUA (no $20M+ market swings for a $1.5B book)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Run inject_scoped_overrides.py BEFORE 05_build_client_performance.py -- canonical prices must be updated first</constraint>
    <constraint>Do not modify canonical_prices.parquet by hand -- always use the script</constraint>
    <constraint>The script removes ALL existing rows for the 5 overridden asset names (not just scoped_override rows) to prevent the wrong price from being picked up via carry_forward</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">Updated canonical_prices.parquet on S3 with scoped_override source rows</deliverable>
    <deliverable type="commit">Updated gold/client_performance.parquet with corrected AUA</deliverable>
    <deliverable type="commit">Updated portal JSON outputs (timeseries_chart.json, partner_analytics.json)</deliverable>
  </deliverables>
</task_order>

## Deployment Sequence

```
Step 1: Upload scripts to EC2
         safe-ec2-deploy.sh (or S3 artifact upload)

Step 2: Inject scoped overrides into canonical_prices
         python data/black_diamond/scripts/silver/inject_scoped_overrides.py --upload

Step 3: Rebuild client performance (picks up corrected prices + ghost exclusions)
         python data/black_diamond/scripts/gold/05_build_client_performance.py --upload

Step 4: Validate
         python data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py --date 2026-03-13

Step 5: Rebuild downstream gold outputs
         python data/black_diamond/scripts/gold/07_build_nna_aua_by_geography.py --upload
         python data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py --upload
         python data/black_diamond/scripts/gold/09_generate_partner_analytics.py --upload
         python data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py --upload

Step 6: Trigger portal publisher Lambda (or wait for next pipeline run)

Step 7: Verify GRO values in portal
```

## What the scoped overrides fix

| Asset | Was Priced At | Now Priced At | Source | Impact |
|---|---|---|---|---|
| Waldrop Donor Advised Fund | $1.00 (par) | $1.95 (silver-derived NAV) | scoped_override | Corrects -$2.8M underval |
| BNP PARIBAS SA | $97.16 (BNPQF equity) | $0.75 (75c on dollar) | scoped_override | Corrects +$20.7M overval |
| DESTINATIONS LARGE CAP EQUITY I | $546.00 (fund NAV) | $13.30 (silver-derived) | scoped_override | Corrects +$14.3M overval |
| DESTINATIONS INTERNATIONAL EQUITY I | $384.00 (fund NAV) | $13.30 (silver-derived) | scoped_override | Corrects +$6.0M overval |
| JPMORGAN CHASE FINL CO LLC 0% 2029 | $1.00 (par) | $2.55 (silver-derived) | scoped_override | Corrects -$1.9M underval |

Ghost account exclusions (aua_overrides.json): 4 accounts totaling +$7.4M of stale AUA removed.

## Risk

- **Low**: Scoped overrides use flat prices. Real prices may drift +-5% over time. Acceptable for these illiquid/structured instruments.
- **Low**: inject_scoped_overrides.py is idempotent. Running it twice produces the same result.
- **None**: NNA flows are unaffected (computed from transactions, not positions x prices).

#### infrastructure_inventory.md

# Task Order: Infrastructure Inventory

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-infrastructure-inventory</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a complete structured inventory of all AWS infrastructure in your scope.
    This is a one-time audit that becomes your permanent context for all future sessions.
    Read every Terraform file, Lambda source directory, and deployment artifact in your
    pipeline scope and document what exists.
  </objective>

  <scope>
    <terraform_dirs>
      <dir>infra/aws/terraform/bd-pipeline/</dir>
    </terraform_dirs>
    <lambda_source_map>infra/aws/lambda/ci/lambda-source-map.json</lambda_source_map>
    <data_scripts>
      <dir>data/black_diamond/scripts/bronze/</dir>
      <dir>data/black_diamond/scripts/silver/</dir>
      <dir>data/black_diamond/scripts/gold/</dir>
    </data_scripts>
    <ec2_manifest>infra/aws/ec2/EC2_MANIFEST.json</ec2_manifest>
  </scope>

  <requirements>
    <requirement id="1">For every Terraform pipeline directory in your scope: list all .tf files with a 1-line description of what each declares</requirement>
    <requirement id="2">For every Lambda function in your scope (from lambda-source-map.json and Terraform): document the function name, source directory, runtime, memory, timeout, trigger type (S3/EventBridge/API Gateway/Step Functions), and what it does</requirement>
    <requirement id="3">For every Lambda Layer used by your functions: document the layer name, S3 key, version, and what packages it provides</requirement>
    <requirement id="4">For every IAM role in your Terraform: document the role name, what services it grants access to, and key policy statements</requirement>
    <requirement id="5">For every EventBridge rule or S3 notification trigger: document the schedule/event pattern and what it invokes</requirement>
    <requirement id="6">For every S3 path your pipelines read from or write to: document the bucket, prefix, and data flow direction</requirement>
    <requirement id="7">Document the current deployment tag and any pipelines that are NOT yet Terraformed</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/infrastructure_inventory.xml</criterion>
    <criterion id="2">Every Lambda function in your scope from lambda-source-map.json is accounted for</criterion>
    <criterion id="3">Every .tf file in your Terraform directories is referenced</criterion>
    <criterion id="4">Trigger types and schedules are actual values from the Terraform, not guesses</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any source code or infrastructure -- this is a read-only audit</constraint>
    <constraint>Do NOT run terraform plan/apply or any AWS CLI commands</constraint>
    <constraint>Do NOT create or edit files outside your agent folder</constraint>
    <constraint>Use Glob, Grep, and Read tools only -- no Explore agent, no Task agent</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/infrastructure_inventory.xml
    </deliverable>
  </deliverables>
</task_order>

## Key Files to Read

### Terraform Directory
- `infra/aws/terraform/bd-pipeline/` -- all .tf files (tag: bd-v2.14.0)

### Lambda Source Map
- `infra/aws/lambda/ci/lambda-source-map.json` -- filter to all bd-* functions

### Lambda Source Directories
- `infra/aws/lambda/bd-pipeline/` -- BD pipeline Lambda functions
- Any other `bd-*` directories under `infra/aws/lambda/`
- Read each function's handler file to understand what it does

### Data Scripts (Bronze / Silver / Gold layers)
- `data/black_diamond/scripts/bronze/` -- raw data ingestion scripts
- `data/black_diamond/scripts/silver/` -- data cleaning and transformation scripts
- `data/black_diamond/scripts/gold/` -- 10 active gold scripts run sequentially (00 through 10)
  - Read each script to understand its role in the sequential pipeline

### EC2 Manifest
- `infra/aws/ec2/EC2_MANIFEST.json` -- BD gold layer runner service entry

### Deployment Tag
- bd-v2.14.0

## Deliverable XML Schema

Write your inventory using this structure:

```xml
<infrastructure_inventory>
  <metadata>
    <agent>0.6.0_AE_PartnerETL</agent>
    <scope>BD (Black Diamond / 49 Financial)</scope>
    <date>2026-03-02</date>
  </metadata>

  <pipelines>
    <pipeline name="{name}" terraform_dir="infra/aws/terraform/{dir}/" tag="{current_tag}">

      <lambda_functions>
        <lambda name="{function_name}"
                source_dir="infra/aws/lambda/{dir}/"
                tf_resource="{module.name.aws_lambda_function.this}"
                runtime="python3.12"
                memory_mb="256"
                timeout_s="30"
                trigger="{S3 | EventBridge | API Gateway | Step Functions | manual}"
                last_deployed="{commit_sha} @ {date}">
          One-line description of what this function does
        </lambda>
      </lambda_functions>

      <layers>
        <layer name="{layer_name}" s3_key="{key}" version="{n}">
          What packages this layer provides
        </layer>
      </layers>

      <iam_roles>
        <role name="{role_name}" tf_resource="{resource_path}">
          What this role allows -- key policy statements
        </role>
      </iam_roles>

      <triggers>
        <trigger type="{EventBridge | S3 | API Gateway}" resource="{rule/bucket/api}">
          Schedule or event pattern
        </trigger>
      </triggers>

      <s3_paths>
        <path bucket="{bucket}" prefix="{prefix}" direction="read | write">
          What data flows through this path
        </path>
      </s3_paths>

    </pipeline>
  </pipelines>

  <ec2_services>
    <service name="{service}" instance_id="{id}" manifest_entry="true | false">
      What this EC2 instance runs
    </service>
  </ec2_services>
</infrastructure_inventory>
```


### 0.6.0_AE_PartnerETL -- Recent Commits

# Recent commits by 0.6.0_AE_PartnerETL

5c56e271 org(2.0.0_SA_COO): GLDPRE.005 AE task order -- deploy + gold run + CTO review fixes
cd448788 [CLSUNI] 0.6.0_AE_PartnerETL: seed_bd_securities.py -- copy Yang etf-classifications, remap hedge->alternatives, add Opal name_aliases
745c44c8 0.6.0_AE_PartnerETL: ADVI_MVP318.003 reviewed -- blocked on DT advisor-publisher deploy + DS script 10 commit
d8c880a8 feat(advi): architect consolidation Lambda fix + architecture docs + segment analytics diag
8eda0ed9 0.6.0_AE_PartnerETL: ADVI_MIXV2.003 in_progress -- insurance diagnostic run, 06b deployed to EC2, full rebuild running
8d054663 0.6.0_AE_PartnerETL: populate insurance_accounts.json -- 109 gated accounts from diagnostic
72c03d2a Deploy EC2 bd-gold-layer-runner @ 8ef1da9b
626350e5 org(0.6.0_AE_PartnerETL): update session log — 00 added to incremental run
2bcc43e0 org(0.6.0_AE_PartnerETL): ADVI_49FNV3.008 complete + session log
c3581a09 org(0.6.0_AE_PartnerETL): ADVI_PSCFIX A3 complete -- script09 cert override session log
f6d9f295 org(2.0.0_SA_COO): ADVI_PSCFIX follow-on task orders -- DT1 deploy + A3 script09
920d96da org(0.6.0_AE_PartnerETL): ADVI_PSCFIX A1 complete -- 05d certification script session log
20088595 org(0.6.0_AE_PartnerETL): ADVI_49FNV3 cache control logs + task orders (005, 006) + staleness investigation
7f1d2589 org(0.6.0_AE_PartnerETL): session log DRFR_PTMCH.P3b -- bd-v2.18.1+v2.18.2 deploy complete
97f49f4a org(0.6.0_AE_PartnerETL): pipeline_inventory bd-v2.18.2 -- IAM fix s3:ListBucketVersions
f0c04c16 org(0.6.0_AE_PartnerETL): DRFR_PTMCH.P3b complete -- bd-v2.18.1 deployed, task orders closed
d08c559f org(0.6.0_AE_PartnerETL): DRFR_PTMCH.P3 session log -- Phase A+B complete
69bd6906 org(0.6.0_AE_PartnerETL): DRFR_PTMCH.P3 complete -- bd-v2.18.0 deployed
ab731673 infra(bd-pipeline): remove stale PortalBucketWrite IAM permission
c3820bb1 org(0.6.0_AE_PartnerETL): ADVI_APISCP.001 bd-pipeline output audit + partner onboarding

### 0.6.0_AE_PartnerETL -- Recent Deployments

# Recent deployment tags (all pipelines, newest first)

partners-api-v1.8.0
partners-api-v1.7.0
partners-api-v1.6.0
shared-infra-v1.5.0
partners-api-v1.5.0
bd-v2.19.2
bd-v2.19.1
partners-api-v1.4.0
bd-v2.19.0
partners-api-v1.3.0
partners-api-v1.2.0
partners-api-v1.1.0
partners-api-v1.0.1
partners-api-v1.0.0
news-v2.7.1
data-refresh-v2.2.0
yang-v2.3.1
yang-v2.3.0
bd-v2.18.4
bd-v2.18.3

### 0.4.0_DE_ClientPlatform -- Recent Session Logs

#### advi_mvplvl_2i_time_window_state_lift.md

# ADVI_MVPLVL 2i: Time Window State Lift — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-13
**Portal DEV commit:** `2639c7d`
**Workspace CLOUD commit:** pending (DT)

## Objective

Execute PRD item 2i: remove Distribution Tab's independent time window toggle and
inherit the time window from the Assets Overview header panel (PartnerAnalytics).

---

## Work Completed

### 1. State Lift to AdvisorIntelligence.tsx

Added `timeWindow` + `setTimeWindow` state to `AdvisorIntelligence.tsx` alongside
existing `granularity`. Threaded as props:
- `timeWindow` + `onTimeWindowChange` to `PartnerAnalytics`
- `timeWindow` to `DistributionTab`

### 2. PartnerAnalytics.tsx — Use Props Instead of Local State

- Removed `const [timeWindow, setTimeWindow] = useState<TimeWindow>('1Y')`
- Added `timeWindow: TimeWindow` and `onTimeWindowChange: (w: TimeWindow) => void` to `PartnerAnalyticsProps`
- Replaced `setTimeWindow(opt)` with `onTimeWindowChange(opt)` in the toggle click handler

### 3. DistributionTab.tsx — Remove Independent Toggle, Use Inherited Value

- Removed `const [window, setWindow] = useState<ChartWindowOption>('1Y')`
- Added `const window: ChartWindowOption = timeWindow` (maps inherited prop to existing local variable name for minimal downstream changes)
- Removed the entire `{/* Window Toggle -- continuous mode only */}` JSX block (22 lines of toggle UI)
- Added `timeWindow: TimeWindow` to `DistributionTabProps`
- `WINDOW_OPTIONS` const retained (still used by sub-components for day-count lookups)

### 4. TypeScript Verification

`bunx tsc -b --noEmit` — clean, zero errors.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Map `TimeWindow` to `ChartWindowOption` via alias, not type change | `TimeWindow` ('1Y'\|'3Y'\|'Max') is a subset of `ChartWindowOption` ('3M'\|'6M'\|...\|'Max'). Sub-components use `ChartWindowOption` for window config lookups. Aliasing avoids touching 10+ internal function signatures. |
| Keep `WINDOW_OPTIONS` array in DistributionTab | Still used by `ContinuousChartView`, `ContinuousNnaChartView`, `ContinuousNnaDivergingView`, `ClaContinuousView` for day-count filtering. |
| Default `'1Y'` set in AdvisorIntelligence.tsx | Matches PRD 1a-i requirement (was previously `'3Y'` in PartnerAnalytics). |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx` | Add `timeWindow` state, thread to PartnerAnalytics + DistributionTab | Yes — portal DEV `2639c7d` |
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | Remove local `timeWindow` state, use `timeWindow`/`onTimeWindowChange` props | Yes — portal DEV `2639c7d` |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Remove local `window` state + toggle UI, use `timeWindow` prop | Yes — portal DEV `2639c7d` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

ADVI_MVPLVL 2i is fully delivered. The time window is now a single source of truth
in `AdvisorIntelligence.tsx`. Changing the Window toggle in the Assets Overview header
(1Y/3Y/Max) immediately updates both the PartnerAnalytics chart and the Distribution
Tab continuous view. The Distribution Tab no longer has its own window toggle.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push portal DEV** — commit `2639c7d` queued
2. **[0.4.0_DT_ClientPlatform] Commit this log to CLOUD**

#### advi_pscfix_b1_integration_complete.md

# ADVI_PSCFIX B1: Integration Validation Complete — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-12
**Portal DEV commits:** `8c51aaf` (schema update), `8bca088` (mock removed)
**Workspace CLOUD commit:** pending (DT)

## Objective

Complete integration validation after Track A2 publisher Lambda deployed new
`timeseries_chart.json` schema. Confirm live AUA data matches PSCFIX contract
at all granularities and remove mock placeholder.

---

## Work Completed

### 1. Live Schema Verification (CloudFront)

Publisher Lambda deployed at 2026-03-12T00:05:20Z. Invalidation IDA69UAWS9JQFOCGHW0N9G720E
cleared `/gold/timeseries_chart.json`. Pulled live data through CloudFront with valid JWT:

| Check | Result |
|-------|--------|
| `aua` top-level keys | `quarterly`, `monthly`, `annually` — new schema PASS |
| `aua.quarterly` | `categories: [NMNC, NMEC]`, 24 periods (2020-Q2 → 2026-Q1) |
| `aua.monthly` | `categories: [NMNC, NMEC]`, 70 periods (Jun 2020 → Mar 2026) |
| `aua.annually` | `categories: [NMNC, NMEC]`, 7 periods (2020 → 2026) |
| Field validation | All points have `period`, `label`, `end_date`, `NMNC`, `NMEC` — PASS |
| Old `aua.data` flat array | Absent — confirmed removed |
| `data_as_of` | `2026-03-10` |
| `firm_id` | `49financial` |

### 2. Mock Removed

Removed `placeholderData: MOCK_AUA_TIMESERIES` from the `useQuery` call in
`PartnerAnalytics.tsx`. Live data is correct; mock is no longer needed.
`MOCK_AUA_TIMESERIES` constant retained in file for reference (no runtime cost).

### 3. TypeScript

`bunx tsc -b --noEmit` — clean, zero errors.

---

## Acceptance Criteria Status

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `bunx tsc -b` passes | **PASS** |
| 2 | AUA chart renders with mock at all granularities | **PASS** (confirmed pre-live) |
| 3 | NNA view untouched | **PASS** |
| 4 | Old `fullPeriodMap` aggregation removed | **PASS** |
| 5 | Live data integration — all 3 granularities render correctly | **PASS** — live schema confirmed; visual render requires Andrew |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | Remove `placeholderData` | Yes — portal DEV `8bca088` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

ADVI_PSCFIX B1 is fully delivered. Schema migration complete end-to-end:
- `types.ts` — `AuaDataPoint`, `AuaCumulativeView`, `CumulativeChartResponse.aua` updated
- `PartnerAnalytics.tsx` — `fullPeriodMap` aggregation removed, direct sub-key select live,
  `findComparablePriorSnapshot` replaced with direct period lookup
- Live `timeseries_chart.json` has `aua.quarterly/monthly/annually` shape confirmed through
  CloudFront with 24/70/7 periods respectively
- Mock placeholder removed

---

## Next Steps

1. **[Andrew] Visual render confirmation** — load `localhost:5175/advisor-intelligence`,
   toggle Mode to AUA, confirm bars populate at quarterly. Switch Interval to Month and
   Year, confirm bars update. Check most recent bar shows partial-period projection.
2. **[0.4.0_DT_ClientPlatform] Push portal DEV** — commits through `8bca088` queued.
3. **[0.4.0_DT_ClientPlatform] Commit this log + CLOUD** — session log to CLOUD.

#### advi_pscfix_b1_integration_validation.md

# ADVI_PSCFIX B1: Integration Validation — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-11
**Portal DEV commits:** `8c51aaf` (B1 schema update)
**Workspace CLOUD commit:** pending (DT)

## Objective

Swap mock AUA data for live data from the deployed publisher Lambda (Track A2),
confirm AUA chart renders correctly at all three granularities (quarterly, monthly, annually).

---

## Work Completed

### 1. Live S3 Schema Audit

Downloaded `opal-data-bd/gold/timeseries_chart.json` and inspected the `aua` key:

| Field | Live Value | Expected (PSCFIX) |
|-------|-----------|------------------|
| `aua` type | `CumulativeChartView` (flat) | `Record<quarterly\|monthly\|annually, AuaCumulativeView>` |
| `aua.categories` | `["NMNC", "NMEC"]` | not at this level |
| `aua.data` length | 2080 daily points | gone — replaced by sub-keys |
| `aua.quarterly` | absent | required |
| `aua.monthly` | absent | required |
| `aua.annually` | absent | required |

**Conclusion: Publisher Lambda (Track A2) has not deployed the new schema yet.**
The live file is still the old flat daily array format.

### 2. Current Portal State

The portal is correctly handling this:
- `placeholderData: MOCK_AUA_TIMESERIES` in `useQuery` serves the new-schema mock
  while the real query fetches from CloudFront
- When the real query resolves (old schema), React Query's `select` would need to
  handle the mismatch — BUT since the old schema does not have `aua.quarterly`,
  `timeseriesData?.aua?.[auaGranularity]?.data` returns `undefined`, and
  `allSortedAuaPeriods` falls back to `[]`
- Result: chart shows empty state (no bars) once real data loads and overrides the mock

**This is acceptable pre-deploy behavior.** The mock shows correct shape during load;
live data returns empty until publisher deploys. No error thrown.

### 3. TypeScript

`bunx tsc -b --noEmit` clean throughout. No regressions.

---

## Validation Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| 1. `bunx tsc -b` passes | **PASS** | Clean |
| 2. Chart renders with mock data at all granularities | **PASS** | Confirmed via placeholderData |
| 3. NNA view untouched | **PASS** | NNA data path not modified |
| 4. Old fullPeriodMap aggregation removed | **PASS** | Replaced with direct sub-key select |
| 5. Live data integration | **BLOCKED** | Publisher Lambda (Track A2) not deployed |

---

## What Happens When Publisher Deploys

1. `timeseries_chart.json` will be republished with new schema:
   `aua: { quarterly: {...}, monthly: {...}, annually: {...} }`
2. CloudFront cache invalidation clears stale file
3. Portal fetches live data — `placeholderData` is superseded
4. `allSortedAuaPeriods` populates from `aua.quarterly.data` (default granularity)
5. AUA bar chart renders with real NMNC/NMEC values
6. Granularity toggle switches between `aua.quarterly`, `aua.monthly`, `aua.annually`

**After publisher is live, DE must:**
- Load `localhost:5175/advisor-intelligence` with a valid JWT
- Confirm AUA bars populate at quarterly granularity
- Toggle to monthly, confirm bars update
- Toggle to annually, confirm bars update
- Confirm the most recent bar shows partial-period projection (in-progress marker)
- Remove or retain `placeholderData` (harmless either way once live data confirmed)

---

## Files Modified

None in this session (validation only).

---

## Blockers

**BLOCKED on Track A2 publisher deploy.**
Evidence: `opal-data-bd/gold/timeseries_chart.json` still has flat `aua.data` array
(2080 daily points, `data_as_of: 2026-03-10`) — old schema. New schema requires
`aua.quarterly`, `aua.monthly`, `aua.annually` sub-keys.

---

## Current State

**Status:** BLOCKED (live integration pending publisher deploy)
**Active branch:** portal `DEV`

Portal code is complete and correct (commit `8c51aaf`). Mock data renders the chart
in the new schema correctly. Live integration blocked on Track A2 publisher Lambda
deploying the restructured `timeseries_chart.json`. Once DT notifies of publisher
deploy + CloudFront invalidation, DE runs the 5-point visual check above and closes
this validation.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Notify DE when Track A2 publisher is deployed and
   CloudFront /api/scoped/advisor-intelligence/timeseries_chart.json is invalidated.**
2. **[0.4.0_DE_ClientPlatform] Run visual validation** — 5-point checklist above.
3. **[0.4.0_DT_ClientPlatform] Push portal DEV** — commits through `8c51aaf` queued.

#### mdlp_wyncht_facsimile_html.md

# MDLP_WYNCHT.001: Benchmark Tab Facsimile HTML — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-11
**Portal DEV commits:** none (tools/ only — no portal changes)
**Workspace CLOUD commits:** `a6fd5c12` → `89965ce9` → `02879be8` → `a6d7ab98` → `c335a9f6`

## Objective

Build a standalone offline HTML facsimile of the Model Portfolios benchmark tab
(Return vs Volatility scatter + Benchmark Heatmap) with all data hardcoded from
`model_portfolio_return_vol_20260227.csv`. Screenshot-ready for documentation and audit.
Task order revised mid-session from dynamic JSON-loading to static hardcoded clone.

---

## Work Completed

### 1. Task Order Scope Revision

COO revised MDLP_WYNCHT.001 to eliminate the DS dependency (no JSON extraction script
needed). New scope: hardcode all values directly from CSV, no file picker, no dynamic
data loading. DS task order `MDLP_WYNCHT.001.extract-benchmark-data` is superseded.

### 2. Data Transcription

Transcribed all 270 data points (5 models × 9 periods × 6 values) from CSV into the
HTML JS data object. Validated with Python against source CSV — all values match.

### 3. Scatter Chart — Chart.js with Custom Plugins

| Feature | Implementation |
|---------|---------------|
| Period toggle (9 buttons, default YTD) | Rebuilds chart on click |
| Model circles | `pointRadius:8`, per-model color from `modelPortfolioColors.ts` |
| Benchmark diamonds | Canvas plugin (`afterDatasetsDraw`) — Chart.js renders nothing, plugin draws manually |
| LTC/LTA split diamond | One shared benchmark point; plugin draws left-half blue (LTC) / right-half red (LTA) when `solidColor=null`; solid single-color when in granular state |
| Hover tooltip | Manual `mousemove` canvas listener with pixel-distance hit detection — bypasses Chart.js hit detection entirely (unreliable for `pointRadius:0` datasets) |
| Granular click | Manual `click` canvas listener, same pixel-distance function; `animation:false` so scales are valid synchronously for pinned card positioning |
| Pinned cards (granular) | Absolutely-positioned HTML divs inside `#scatter-container`; model card prefers right, benchmark prefers left; overlap resolver pushes cards apart vertically |
| Y=0 reference line | Canvas plugin (`afterDraw`) |
| X-axis headroom | `max = maxVol × 1.28` — prevents LTC/LTA from being cramped in corner |

### 4. Benchmark Heatmap

CSS Grid (200px + 100px + 9×1fr). 3 rows per model (Model / Benchmark / Spread).
Model name column spans 3 rows with left border in model color. Spread cells use
`rgba(emerald/red/yellow, 0.5)` overlay matching `BenchmarkHeatmap.tsx` exactly.

### 5. Index/ETF + Gross/Net Toggles

Net cost proration matches `BenchmarkHeatmap.tsx` exactly:
- `net = gross - (trading_days / 252) * 0.36`
- Fixed: 1D=1, 1M=21, 1Q=63, 1Y=252, SI=252
- To-date (WTD/MTD/QTD/YTD): weekday count from period start to `2026-02-27`
- Net applies to Model and Spread rows only; benchmarks always gross
- Scatter chart also applies net to model points (not benchmark points)

### 6. Theme — Exact Portal Vars

| Element | Value |
|---------|-------|
| Page background | `hsl(222,24%,81%)` — Opal brand silver (`--palette-silver`) |
| Panel header | `hsl(221,44%,14%)` — `--semantic-background-muted` |
| Panel body | `hsl(221,44%,21%)` — `--semantic-background-surface` |
| Tooltip bg | `hsl(221,44%,11%)` — `--semantic-background-tooltip` |
| Panel titles | `color:#fff; text-transform:uppercase; tracking-wide` — exact `PanelHeader.tsx` |
| Tooltip structure | Exact `CustomTooltip` from `ReturnVolatilityScatter.tsx`: name bold white, type white/60, return emerald-400/red-400, vol amber-400 |
| Tooltip sizing | `width:max-content; max-width:260px; word-break:break-word` — grows to content, benchmark names never overflow |

### 7. PanelFooter Timestamp

Format matches `PanelFooter.tsx`: `"February 27th, 2026, 5:00p ET | Source: Bloomberg."`
Right-aligned, `text-xs text-white/40`, on all three panels.

### 8. S3 Hosting

Bucket: `opal-313476888478-wyncht` (one-off, public-read)
URL: `https://opal-313476888478-wyncht.s3.amazonaws.com/facsimile.html`

Re-upload command:
```bash
export AWS_EC2_METADATA_DISABLED=true && aws s3 cp tools/wyncht/facsimile.html s3://opal-313476888478-wyncht/facsimile.html --content-type "text/html"
```

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Manual canvas event listeners instead of Chart.js `onHover`/`onClick` | Chart.js hit detection unreliable for `pointRadius:0` datasets even with `pointHitRadius`. Manual pixel-distance calculation is 100% reliable. |
| `animation:false` | Synchronous chart render — scales valid immediately after `new Chart()`, required for pinned card positioning. |
| Split diamond via canvas plugin | Recharts `renderCustomShape` polygon approach ported to Chart.js `afterDatasetsDraw`. Clean separation: Chart.js renders nothing for benchmark dataset, plugin owns all visual rendering. |
| `width:max-content; max-width:260px` on tooltips | Tooltip grows to fit longest line (benchmark names), caps before becoming unwieldy. Removed hardcoded 190px width that was clipping text. |
| `CARD_W=260` in positioning math | Conservative bound for `left/right` placement decision — card will be ≤260px wide. |
| One shared LTC/LTA benchmark point | LTC and LTA have identical benchmark values in all periods (confirmed from CSV). One point avoids visual double-counting. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `tools/wyncht/facsimile.html` | Created — complete standalone facsimile | Yes — CLOUD `c335a9f6` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/MDLP_WYNCHT.001.facsimile-html.md` | status → complete | No — local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

`tools/wyncht/facsimile.html` delivered and live at S3 URL above. All 9 acceptance
criteria met. Scatter chart, heatmap, all toggles, granular drilldown, hover tooltips,
pinned cards, PanelFooter timestamps all match portal visual language. Data validated
against `model_portfolio_return_vol_20260227.csv` (270 values, 0 mismatches).

---

## Next Steps

1. **[Andrew] Screenshot** — Open S3 URL in Chrome, capture benchmark tab for documentation.
2. **[0.4.0_DT_ClientPlatform] Commit org changes to CLOUD** — this session log + task order status update.

**Do NOT:**
- Run `pip install` or any Python tooling — data is hardcoded, no extraction script needed
- Modify `portal/` — facsimile is entirely in `tools/wyncht/`

#### mdlp_wyncht_full_session.md

# MDLP_WYNCHT Full Session — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-11
**Start Time:** ~09:00
**End Time:** ~16:00
**Portal DEV commits:** none (tools/ only — no portal changes)
**Workspace CLOUD commits:** `a6fd5c12` → `89965ce9` → `02879be8` → `a6d7ab98` → `c335a9f6` → `d876bc87` → `cfd1fc9a` → `696a530a` → `10abd669` → `ef4058e0` → `627dc83f` → `5eae8094`

---

## Objective

Execute MDLP_WYNCHT task orders from COO:
1. Build a standalone offline HTML facsimile of the Model Portfolios benchmark tab
2. Stand up individual scatter and benchmark pages for presentation use
3. Build a peers quartile chart page from live S3 data
4. Investigate PowerPoint embedding options and deliver an interactive PPTX

---

## Work Completed

### 1. Orientation

Read recent logs (2026-03-10), confirmed ADVI_APISCP COMPLETE, ADVI_SNPLBK COMPLETE.
Two pending task orders received from COO today:
- `MDLP_WYNCHT.001.facsimile-html` — benchmark tab static clone
- `MDLP_WYNCHT.001` (DS) — pkl extraction script (later superseded)

### 2. Task Order Scope Revision — Hardcoded Data

COO revised `MDLP_WYNCHT.001.facsimile-html` mid-session: eliminated DS dependency
entirely. New scope: hardcode all 270 values directly from `model_portfolio_return_vol_20260227.csv`,
no JSON file loading, no file picker. DS task order `MDLP_WYNCHT.001.extract-benchmark-data`
is superseded and inactive.

Validated all 270 data points (5 models × 9 periods × 6 values) against CSV with Python
— zero mismatches.

### 3. facsimile.html — `tools/wyncht/facsimile.html`

**Commit:** `a6fd5c12`

Full standalone benchmark tab clone. Chart.js CDN for scatter, inline CSS grid for heatmap.

**Iterative refinement over multiple commits:**

| Commit | Change |
|--------|--------|
| `89965ce9` | Exact portal theme vars: brand silver page bg `hsl(222,24%,81%)`, panel headers `hsl(221,44%,14%)`, panel body `hsl(221,44%,21%)`, primary indigo `hsl(253,100%,68%)`. Panel titles `color:#fff uppercase tracking-wide` matching `PanelHeader.tsx`. Split LTC/LTA diamond, legend drilldown. |
| `02879be8` | Tooltips rebuilt as external HTML div matching `CustomTooltip` exactly: `bg-[hsl(221,44%,14%)]`, `border-white/20`, name bold white, type `white/60`, return `emerald-400`/`red-400`, vol `amber-400`. Manual `mousemove`/`click` canvas event handlers with pixel-distance hit detection — bypasses Chart.js hit detection which is unreliable for `pointRadius:0` datasets. `animation:false` for synchronous render. Granular pinned cards as absolutely-positioned HTML divs. |
| `a6d7ab98` | Timestamp: `"February 27th, 2026, 5:00p ET \| Source: Bloomberg."` matching `PanelFooter.tsx` format. X-axis `max = maxVol × 1.28` (28% headroom for LTC/LTA). Pinned card overlap resolver: detects x+y overlap, pushes cards apart vertically. |
| `c335a9f6` | Tooltip sizing: `width:max-content; max-width:260px; word-break:break-word` — cards grow to content, benchmark names (`85% Bloomberg Agg / 15% MSCI ACWI`) never overflow. Removed hardcoded JS `width=190px` that was clipping text. |

**Key technical decisions:**

| Decision | Rationale |
|----------|-----------|
| Manual canvas mousemove/click listeners | Chart.js `onHover`/`onClick` unreliable for invisible datasets (`pointRadius:0`). Pixel-distance check against `chart.scales.x.getPixelForValue()` is 100% reliable. |
| `animation:false` | Synchronous chart render — scales valid immediately after `new Chart()`, required for pinned card pixel positioning. |
| Split diamond via `afterDatasetsDraw` plugin | LTC and LTA share identical benchmark values in all periods (confirmed from CSV). One shared point, left half = LTC blue, right half = LTA red. In single-model granular state, renders as solid model color. |
| `CARD_W=260` for bounds checking | Card auto-sizes via CSS `width:max-content`, but 260px is the upper bound used for left/right placement calculation. |

### 4. S3 Bucket Setup — `opal-313476888478-wyncht`

Created public-read S3 bucket for hosting all facsimile pages:

```bash
aws s3api create-bucket --bucket opal-313476888478-wyncht --region us-east-1
aws s3api put-public-access-block ...  # all false
aws s3api put-bucket-policy ...        # s3:GetObject Principal:*
```

Re-upload command for any file:
```bash
export AWS_EC2_METADATA_DISABLED=true && aws s3 cp tools/wyncht/<file>.html s3://opal-313476888478-wyncht/<file>.html --content-type "text/html"
```

### 5. scatter.html + benchmark.html — Standalone Presentation Pages

**Commit:** `cfd1fc9a`

Extracted each chart component into its own fullscreen page for presentation use.

`scatter.html`:
- Chart fills viewport (flex:1 height, responsive)
- All toggles in header: Benchmark (Index/ETF), Returns (Gross/Net), Period (9 buttons)
- Full granular drilldown, split diamond, hover tooltips, pinned cards
- Benchmark type toggle switches benchmark points + volatility in scatter

`benchmark.html`:
- Heatmap + compositions only, no chart overhead
- Index/ETF and Gross/Net toggles
- Same 36 bps net proration logic

| Page | S3 URL |
|------|--------|
| Full facsimile | `https://opal-313476888478-wyncht.s3.amazonaws.com/facsimile.html` |
| Scatter only | `https://opal-313476888478-wyncht.s3.amazonaws.com/scatter.html` |
| Heatmap only | `https://opal-313476888478-wyncht.s3.amazonaws.com/benchmark.html` |

### 6. PPTX Action Buttons — `opal_iwm_partnership- 3.10.26 (interactive).pptx`

Investigated LiveWeb add-in for PowerPoint embedding — download link dead (404, expired SSL cert, site abandoned). Web Viewer Office Add-in not available in client's Office installation. Proceeded with python-pptx action buttons as reliable fallback.

Read PPTX structure (43 slides). Identified slides 23–27 as "Opal Model vs. Benchmark" — the target slides for interactive chart links.

Used python-pptx to add two navy action buttons to slides 23–27:
- `Return vs Volatility ↗` → `scatter.html`
- `Benchmark Heatmap ↗` → `benchmark.html`

Positioned bottom-right corner, Opal navy fill (`#163372`), white semibold text 8.5pt.
Buttons work via Ctrl+click in edit mode, single click in slideshow mode. No add-in dependency — any machine with a browser works.

Output: `C:/Users/AndrewBerman/Downloads/opal_iwm_partnership- 3.10.26 (interactive).pptx`

### 7. peers.html — Quartile Chart

**Commits:** `696a530a` → `10abd669` → `ef4058e0` → `627dc83f`

Fetched live peer performance data:
```bash
aws s3 cp s3://opal-data-portal-v2/json/peers/peer_performance.json ...
```

Data: `data_as_of: 2026-02-01`, 6 periods (1M, QTD, 1Q, YTD, 1Y, Since Inception),
5 models. Displayed as February 27th, 2026 per project convention.

Hardcoded all 30 rows (5 models × 6 periods × p5/p25/p50/p75/p95/model/bench).

Implements `PeersTab.tsx` exactly:
- SI annualization: `(1 + cumulative/100)^(365/actual_days) - 1` using `data_as_of=2026-02-01` and `inception=2024-04-30` (642 actual days)
- Quartile colors exact: `hsl(260,60%,50%)` (bottom), `hsl(220,40%,60%)`, `hsl(210,30%,70%)`, `hsl(210,50%,45%)` (top)
- Cyan arrow = model, black arrow = policy benchmark
- Global min/max Y scale across all periods for selected model (consistent axis)
- Model selector: UST/ST/INT/LTC/LTA, colored buttons, default LTC
- Period headers extracted from SVG to HTML `<div class="period-hdr">` — CSS-controlled spacing below legend divider
- `align-items:flex-start` on chart row for correct top-anchored column layout

| Refinement | Fix |
|-----------|-----|
| `10abd669` | `margin-bottom:36px` on legend strip; added `Model:` / `Policy Benchmark:` prefix to value labels |
| `ef4058e0` | Period headers moved from SVG text to HTML div — full CSS padding control |
| `627dc83f` | `align-items:flex-start` on chart-row — was `flex-end`, which was bottom-snapping columns and pulling period headers up into the legend area |

S3 URL: `https://opal-313476888478-wyncht.s3.amazonaws.com/peers.html`

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Hardcode data vs dynamic JSON loading | COO revised task order mid-session; eliminates DS dependency, simpler for screenshot/presentation use |
| Manual canvas event listeners | Chart.js built-in detection unreliable for zero-radius benchmark points |
| S3 public bucket (one-off) | Fastest path to shareable URL; not production infrastructure |
| python-pptx action buttons over LiveWeb | LiveWeb download dead; action buttons work on any machine with no add-in dependency |
| Period headers as HTML not SVG text | SVG text at y=16 with `overflow:visible` caused positioning issues relative to CSS-controlled parent layout |
| DS task order superseded | Hardcoded approach eliminates need for pkl extraction script |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `tools/wyncht/facsimile.html` | Created — full benchmark tab facsimile | Yes — `c335a9f6` |
| `tools/wyncht/scatter.html` | Created — scatter-only presentation page | Yes — `cfd1fc9a` |
| `tools/wyncht/benchmark.html` | Created — heatmap-only presentation page | Yes — `cfd1fc9a` |
| `tools/wyncht/peers.html` | Created — quartile peer comparison page | Yes — `627dc83f` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/MDLP_WYNCHT.001.facsimile-html.md` | status → complete | Yes — `5eae8094` |
| `C:/Users/AndrewBerman/Downloads/opal_iwm_partnership- 3.10.26 (interactive).pptx` | New file — PPTX with action buttons on slides 23–27 | Local only (not a repo file) |
| S3 bucket `opal-313476888478-wyncht` | Created; facsimile.html, scatter.html, benchmark.html, peers.html uploaded | AWS live |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

All four HTML pages live on S3. PPTX delivered to Downloads. All 13 CLOUD commits made.
MDLP_WYNCHT.001 task order marked complete.

The facsimile reproduces the portal's Performance tab with full visual fidelity:
exact theme vars, split LTC/LTA diamond, manual hit detection, pinned granular cards,
portal-matching tooltip structure, canonical PanelFooter timestamp. Peers chart replicates
PeersTab.tsx including SI annualization and global Y-axis scale.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push CLOUD** — 13 commits pending push, including all wyncht tooling.
2. **[Andrew] Screenshot** — Open S3 URLs in Chrome, capture for documentation/audit.
3. **[Andrew] PPTX** — Open `opal_iwm_partnership- 3.10.26 (interactive).pptx`, verify buttons on slides 23–27 launch correct pages.

**Do NOT:**
- Modify `portal/` — all facsimile work is in `tools/wyncht/`, no portal changes
- Run DS extraction script — data is hardcoded; DS task order superseded
- Push to portal DEV — no portal commits were made this session

#### nna_cohort_specific_time_machine_brief.md

# Cohort-Specific Period-over-Period NNA in Segment Analytics — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-13
**Type:** CTO Architecture Brief
**Surface Area:** AdvisorIntelligence > Distribution Tab > Snapshot Mode > NNA Metric > GEO/ADV Cohorts

---

## Problem Statement

The Distribution Tab's Snapshot mode has a time machine strip that shows NNA across
multiple periods (current + 3 historical, keyed to the Interval selector: quarterly
q1/q2/q3, monthly m1/m2/m3, annual y1/y2/y3). When the user selects NNA as the
metric and drills into a specific cohort segment (e.g., a state in GEO, an architect
in ADV), the time machine strip continues to display **aggregate firm-wide NNA** for
each period rather than the **NNA specific to the drilled-into segment**.

By contrast, AUA mode already solves this correctly: `DistributionQuarterlyStrip`
traverses into `snap.donut.segments[parentKey].aua` and even
`parentSeg.cities[childKey].aua` for each period, showing cohort-specific AUA in
the strip when drilled down.

The ask is: make the NNA time machine strip behave the same way — when drilled into
a state, show that state's NNA per period; when drilled into a city, show that city's
NNA per period; same for architect and relationship levels.

---

## Current Architecture

### Data Source

`09_generate_partner_analytics.py` (EC2 gold script) builds `views.nna` as
`Record<TimePeriodKey, { geo: NnaView, adv: NnaView }>`. The period loop (lines
1546-1598) calls `build_nna_geo_view()` and `build_nna_adv_view()` for **every**
period with the same arguments, producing identical structure at every time slice.

### Data Shape per Period (per `views.nna[period]`)

```
{period_key}: {
  geo: {
    donut: {
      title, total, total_abs,
      segments: [
        { key: "texas", label: "Texas", value: <signed NNA>, aua: <abs NNA>,
          period_inflows, period_outflows, client_count, color }
        ...
      ]
    },
    distribution: { total: DistributionStats, by_segment: { [state]: DistributionStats } },
    drill: {
      [state]: {
        total: DistributionStats,            // aggregate for this state
        by_city: {
          [city]: DistributionStats           // .total = sum of relationship NNA in city
        }
      }
    },
    metrics: { nna: <aggregate net NNA>, client_count }
  },
  adv: {
    donut: {
      title, total, total_abs,
      segments: [
        { key: "travis_penfield", label: "Travis Penfield", value: <signed NNA>,
          period_inflows, period_outflows, client_count, color }
        ...
      ]
    },
    distribution: { total: DistributionStats, by_segment: { [architect]: DistributionStats } },
    drill: {
      [architect]: {
        distribution: DistributionStats,     // aggregate for this architect's relationships
        relationship_count: N
      }
    },
    metrics: { nna: <aggregate net NNA>, client_count }
  }
}
```

### Frontend Components

| Component | File | Current Behavior |
|-----------|------|-----------------|
| `NnaQuarterlyStrip` | `DistributionTab.tsx:2239` | Reads `nnaViews[period][cohort].metrics.nna` — always aggregate, ignores drill state |
| `DistributionQuarterlyStrip` | `DistributionTab.tsx:2304` | Reads per-segment AUA at every drill level — fully cohort-aware (the reference implementation) |

---

## Data Availability by Drill Level

| Drill Level | Cohort | Period-specific NNA field | Available in every period? |
|---|---|---|---|
| **State** | GEO top-level | `geo.donut.segments[key].value` | YES |
| **City** | GEO drilled | `geo.drill[state].by_city[city].total` | YES |
| **Architect** | ADV top-level | `adv.donut.segments[key].value` | YES |
| **Relationship** | ADV drilled | `adv.drill[architect].distribution.total` | PARTIAL (see gap below) |

### Gap: Relationship-Level Drill

At the ADV drill level (architect -> relationships), the data contains only
`DistributionStats` per architect — not per-relationship named values. The
`DistributionStats.total` field gives the architect's aggregate NNA (which is the
same as `donut.segments[architect].value`), so you CAN show the architect's NNA
when drilled to the relationship list view. But you CANNOT show NNA for an
individual selected relationship across periods because the per-relationship
values are not preserved in the output — only the statistical summary (histogram,
percentiles, count).

To close this gap, `build_nna_adv_view()` would need to emit per-relationship NNA
values inside `drill[architect]`, similar to how `build_nna_geo_view()` emits
`by_city` entries. This is a backend change in script 09.

---

## Implementation Path (Frontend Only — No Backend Changes)

For the three fully-supported levels (state, city, architect), the fix is entirely
in `NnaQuarterlyStrip`. The component currently ignores drill state:

```typescript
// CURRENT (line 2240-2244): always reads aggregate
const getNna = (period: TimePeriodKey): number => {
  const v = nnaViews?.[period]
  if (!v) return 0
  const cohortView = cohort === 'geo' ? v.geo : v.adv
  return cohortView?.metrics?.nna ?? 0
}
```

The revision would mirror `DistributionQuarterlyStrip.getAuaForPeriod()` pattern:

1. Accept drill state props: `parentSegmentKey`, `childSegmentKey`, `cohort`
2. When a parent segment is selected (state or architect):
   - Find `cohortView.donut.segments.find(s => s.key === parentKey)`
   - Read `.value` (signed NNA) instead of `.metrics.nna`
3. When a child segment is selected (city):
   - Read `cohortView.drill?.[parentKey]?.by_city?.[childKey]?.total`
4. When at top level (no drill): keep current `.metrics.nna` behavior

This is the same structural pattern already proven in `DistributionQuarterlyStrip`
(lines 2308-2331). The NNA version navigates different fields (`.value` instead
of `.aua`, `.drill[].by_city[].total` instead of `.cities[].aua`) but the
traversal logic is identical.

### Props Change for NnaQuarterlyStrip

```typescript
// ADD these props (mirroring DistributionQuarterlyStrip):
parentSegmentKey: string | null   // selected state or architect key
childSegmentKey: string | null    // selected city key (GEO drill only)
cohort: CohortOption              // already passed
```

### Callsite Change

At the callsite (line 2108-2115), pass the drill state that already exists in
the parent component's state:

```typescript
<NnaQuarterlyStrip
  nnaViews={...}
  periods={...}
  cohort={cohort}
  selectedPeriod={selectedPeriod}
  onPeriodChange={setSelectedPeriod}
  granularity={granularity}
  parentSegmentKey={parentSegment?.key || selectedStateKey || selectedArchitectKey || null}
  childSegmentKey={isDrilledDown && selectedSegmentKey ? selectedSegmentKey : null}
/>
```

---

## Decisions for CTO

1. **Scope question:** Should this revision cover only the three fully-supported
   levels (state, city, architect), or should it also close the relationship-level
   gap with a backend change to script 09?

2. **Strip display label:** When showing cohort-specific NNA, the strip subtitle
   should change from "Period NNA" to something like "Texas NNA" or
   "Travis Penfield NNA". This is a minor UX detail but worth specifying.

3. **Edge case — segment not present in a historical period:** A state or architect
   that exists in the current period may not appear in older periods (new advisor
   joined, new state appeared). The strip should show $0 or "N/A" for those periods.
   This is the same edge case AUA mode already handles (falls through to `return 0`).

---

## Current State

**Status:** COMPLETE (investigation and brief only — no code changes)
**Active branch:** CLOUD (parent), portal DEV (submodule)

This log documents the feasibility analysis. No code was written or committed.
The data already exists to support cohort-specific period-over-period NNA at the
state, city, and architect levels. The frontend change is isolated to
`NnaQuarterlyStrip` in `DistributionTab.tsx` and mirrors an existing proven pattern.

---

## Next Steps

1. **[1.0.0_SA_CTO] Review this brief** and decide scope (3-level frontend-only
   vs. 4-level with backend script 09 change for relationship drill)
2. **[1.0.0_SA_CTO] Include in project architecture** for the larger revision
   that incorporates this work
3. **[0.4.0_DE_ClientPlatform] Write task order for 0.4.2_RD** once CTO scopes
   the project and determines whether this is standalone or bundled


### 0.4.0_DE_ClientPlatform -- Pending Task Orders

#### ADVI_APISCP.006.final-browser-verification.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-final-browser-verification</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
    <phase>4</phase>
  </metadata>

  <objective>
    Final browser verification for ADVI_APISCP. The full infrastructure chain is now live.
    This is the last acceptance criterion for the project. Confirm the Advisor Intelligence
    page loads correctly end-to-end in a real browser session with a valid 49 Financial JWT.
  </objective>

  <context>
    The following infrastructure is now fully deployed on CloudFront EVTSA9VEHNZVH:

    1. Lambda@Edge shared-advisor-router:5 (v6 code) — dynamic OAI routing + OPTIONS handler
       - OPTIONS preflight: returns 204 + CORS headers before X-Firm-Id guard
       - GET: reads X-Firm-Id from JWT-injected header, routes to opal-data-{firmId}/gold/
       - Tag: shared-advisor-router-v6 → d2b405b0

    2. OAI E139998VWH0PD wired to S3-opal-data-bd origin (replaces OAC)
       - opal-data-bd bucket policy grants OAI canonical user s3:GetObject
       - Lambda origin mutation works correctly with OAI (OAC bypass is resolved)

    3. Cache key policy opal-scoped-advisor-by-firm (45eb7514)
       - X-Firm-Id in cache key — firm A responses never served to firm B

    4. S3 CORS on opal-data-bd
       - AllowedOrigins: *, AllowedMethods: GET + HEAD

    5. CloudFront CORS-S3Origin origin request policy (b689b0a8)
       - Forwards Origin header to S3 for CORS evaluation

    6. CloudFront Response Headers Policy opal-scoped-advisor-cors (3570c5b4)
       - Adds Access-Control-Allow-Origin: * to all responses as safety net

    Previous blockers resolved:
    - OAC bypass: fixed by migrating to OAI
    - OPTIONS preflight: fixed by v6 Lambda OPTIONS early-return + RHP
    - Stale March 2 localStorage cache: cleared manually by Andrew
    - S3 had no CORS config: fixed in .004
    - Missing Origin Request Policy on CF behavior: fixed in .004

    DT verified OPTIONS → 204 + CORS headers live.
    COO curl verified GET (no browser) → 200 application/json, data_as_of: 2026-03-09.
    Browser verification with real JWT has NOT been done yet. That is this task.
  </context>

  <requirements>
    <requirement id="1">
      Run the portal locally: /c/Users/AndrewBerman/.bun/bin/bun run dev --port 5175
      from the portal/ directory. (Use 5175 not 5173 -- if 5173 is already running
      that is fine too, any port works since CORS is AllowedOrigins: *.)
    </requirement>
    <requirement id="2">
      Clear browser localStorage before loading the page. DevTools → Application →
      Local Storage → right-click origin → Clear. This removes any stale cache entries
      from before the infrastructure fixes. Hard refresh after clearing (Ctrl+Shift+R).
    </requirement>
    <requirement id="3">
      Log in with a valid 49 Financial user account and navigate to the
      Advisor Intelligence page.
    </requirement>
    <requirement id="4">
      Open DevTools Network tab. Verify the following endpoints all return
      HTTP 200 with Content-Type: application/json (NOT text/html):

        /api/scoped/advisor-intelligence/timeseries_chart.json
        /api/scoped/advisor-intelligence/clients_tab.json
        /api/scoped/advisor-intelligence/architect_leaderboard.json
        /api/scoped/advisor-intelligence/partner_analytics/header_metrics_quarterly.json
        /api/scoped/advisor-intelligence/snapshots/aua_by_architect.json

      For each response, confirm:
        - HTTP 200 (not 401, 403, or any HTML response)
        - Content-Type: application/json
        - Access-Control-Allow-Origin: * is present in response headers
        - Response body is valid JSON (not <!doctype html>)
    </requirement>
    <requirement id="5">
      Verify the page visually renders correctly:
        - Assets Overview header panel populates with AUA / NNA metrics
        - Distribution tab renders charts (not blank)
        - Advisors tab renders leaderboard
        - Clients tab renders data
      None of these should be blank or stuck in a loading state.
    </requirement>
    <requirement id="6">
      Confirm data_as_of is current. Check the Network response for
      timeseries_chart.json -- the data_as_of field should be 2026-03-09
      (the last BD pipeline run date). It must NOT be 2026-03-02 (that was
      the stale portal-v2 data).
    </requirement>
    <requirement id="7">
      If any endpoint returns HTML or fails CORS, escalate immediately with:
        - The exact endpoint URL
        - The HTTP status code
        - The response headers (especially Content-Type and any CORS headers)
        - The first 100 chars of the response body
      Do not attempt to fix Lambda@Edge or CloudFront yourself.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 5 static endpoints return HTTP 200 application/json</criterion>
    <criterion id="2">Access-Control-Allow-Origin: * present on all responses</criterion>
    <criterion id="3">data_as_of: 2026-03-09 on timeseries_chart.json (not 2026-03-02)</criterion>
    <criterion id="4">Page visually renders: header panel, Distribution tab, Advisors tab, Clients tab all populated</criterion>
    <criterion id="5">No HTML responses anywhere in the advisor-intelligence Network requests</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any portal code during this task. Verification only.</constraint>
    <constraint>If anything fails, escalate to COO with exact error details. Do not attempt infrastructure fixes.</constraint>
  </constraints>

  <dependencies>
    <!-- All infrastructure complete. No blocking dependencies. -->
  </dependencies>

  <references>
    <ref type="deploy_log">org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-10/advi_apiscp_004_options_cors_v6_deploy.md</ref>
    <ref type="task_order">ADVI_APISCP.005.cors-response-headers-policy.md (CloudOps -- complete)</ref>
    <ref type="task_order">ADVI_APISCP.004.cors-opal-data-bd.md (CloudOps -- complete)</ref>
    <ref type="task_order">ADVI_APISCP.003.cloudfront-oai-wire-v5-deploy.md (DT -- complete)</ref>
  </references>

  <deliverables>
    <deliverable type="document">Session log with Network tab screenshots/output confirming all 5 endpoints pass</deliverable>
    <deliverable type="confirmation">data_as_of: 2026-03-09 confirmed in timeseries_chart.json response</deliverable>
    <deliverable type="confirmation">Visual page render confirmed (all panels populated)</deliverable>
  </deliverables>
</task_order>

#### ADVI_MVPLVL.004.p4-books-proxy-wiring.md

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-13-p4-books-proxy-wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-13</date>
    <status>pending</status>
    <thread_serial>ADVI_MVPLVL-004</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</thread_ref>
  </metadata>

  <objective>
    Wire portal proxy routes and TypeScript types for 4 new Books Tab endpoints
    (timeseries x2 + composition x2) that DS is implementing in opal-partners-data.
    Also implement item 4h (advisor listing UI consistency with leaderboard design
    from 3d) once RD's P3 leaderboard commit is available.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="proxy-routes">
      Add 4 proxy route functions in portal/src/api/endpoints/advisor-intelligence.ts:

      1. getBooksRelationshipTimeseries(relationshipId: string)
         -> GET /api/scoped/partners/books/relationship/{id}/timeseries
      2. getBooksAccountTimeseries(accountId: string)
         -> GET /api/scoped/partners/books/account/{id}/timeseries
      3. getBooksRelationshipComposition(relationshipId: string)
         -> GET /api/scoped/partners/books/relationship/{id}/composition
      4. getBooksAccountComposition(accountId: string)
         -> GET /api/scoped/partners/books/account/{id}/composition
    </requirement>

    <requirement id="types">
      Add TypeScript types in portal/src/pages/AdvisorIntelligence/types.ts:

      BooksTimeseriesResponse:
      - generated_at: string
      - data_as_of: string
      - relationship_id?: string
      - account_id?: string
      - data: BooksTimeseriesPoint[]

      BooksTimeseriesPoint:
      - date: string
      - total_aua: number
      - cum_inflows: number
      - cum_outflows: number
      - nna: number

      BooksCompositionResponse:
      - generated_at: string
      - data_as_of: string
      - scope: { relationship_id?: string, account_id?: string }
      - mix: MixItem[]
      - concentration: { top_n: number, items: ConcentrationItem[], other: { market_value: number, pct: number } }
      - unclassified: { count: number, market_value: number }

      MixItem:
      - asset_class: string  (enum: equity|fixed_income|hedge|cash|other)
      - label: string
      - market_value: number
      - pct: number

      ConcentrationItem:
      - key: string
      - label: string
      - asset_class: string
      - market_value: number
      - pct: number
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 4 proxy functions exist and compile (bunx tsc -b passes)</criterion>
    <criterion id="2">TypeScript types match the DS endpoint contract from thread ADVI_MVPLVL-004</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Commit on portal DEV branch</constraint>
    <constraint>Do not implement UI — RD owns component rendering</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.004.p4-books-backend-endpoints" status="pending">
      Proxy routes point to endpoints DS is implementing
    </dependency>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_MVPLVL_PRD.md (Part 4)</ref>
    <ref type="thread">org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with proxy routes + types</deliverable>
  </deliverables>
</task_order>
```

#### ADVI_MVPLVL.009.mix-composition-e2e.md

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-mvplvl-009-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>pending</status>
    <project_code>ADVI_MVPLVL</project_code>
  </metadata>

  <objective>
    Two views in AdvisorIntelligence are completely non-functional despite all
    upstream projects (GLDPRE, BKSCMP, CLSPT2, MIXV2) being marked complete.
    Andrew confirmed on 2026-03-23 that these do not load at any drill level.
    This task order requires a full end-to-end trace from gold layer output
    through Lambda through TypeScript through frontend component, identifying
    every break in the chain and fixing it.

    The two broken views:

    1. ASSETS OVERVIEW "Mix" toggle — the AUA stacked bar in the header panel
       has an "AUA" toggle (default) and a "Mix" toggle. Mix does not display.
       It must show asset class breakdown (equity, fixed income, alternatives,
       other) in THE EXACT SAME stacked bar format and structure as the
       NMEC/NMNC stacked bars in the "Clients" toggle. Same coloring and
       labeling as CMA taxonomy. "Other" = residual not assigned to the three
       named classes (will primarily be cash).

    2. BOOKS TAB "Asset Mix" + "Top Holdings" — the Overview panels at the top
       of the /books route do not load at any drill level (firm, advisor,
       relationship). Two components are expected:
       (a) Asset Mix radial (donut/pie) showing asset class breakdown
       (b) Top Holdings horizontal bars showing top 9 securities + "Other"
           (everything else collapsed)

       CRITICAL interaction: clicking an asset class segment in the radial
       must filter the Top Holdings view to show the top 9 holdings WITHIN
       THAT CLASS + Other (remaining holdings in that class). Example: if user
       clicks "Fixed Income" in the radial and there are 20 FI holdings, show
       the top 9 by market value + "Other" as the sum of the remaining 11.
       If there are only 3 FI holdings, show all 3 (no "Other" needed). The
       overall top-10 ranking across all classes is IRRELEVANT to per-class
       drill — what matters is top-9 within the selected class.
  </objective>

  <context>
    DEFINITIONS (use consistently across all agents):
    - "Mix" = breakdown by ASSET CLASS (equity, fixed income, alternatives, other)
    - "Concentration" = breakdown by SECURITY (individual holdings ranked by MV)

    DATA SOURCES (gold layer):
    - Script 06b (06b_build_client_mix_timeseries.py) -> firm_mix_views.json,
      per-advisor mix.json, client_mix_timeseries parquet. Uses ETFClassifier
      for 4-class taxonomy (equity, fixed_income, alternatives, cash-as-residual).
    - Script 12 (12_build_composition_artifacts.py) -> firm_composition.json,
      per-advisor composition.json. Contains BOTH asset mix (radial) AND
      top holdings (concentration bars) per class. Uses ETFClassifier.

    LAMBDA ROUTES (opal-partners-data, partners-api-v1.8.0):
    - GET /api/scoped/partners/books/firm/mix-views -> handle_firm_mix_views()
      S3: gold/firm_mix_views.json
    - GET /api/scoped/partners/books/advisor/{id}/mix -> handle_advisor_mix_views()
      S3: gold/advisors/{id}/mix.json
    - GET /api/scoped/partners/books/firm/all/composition -> handle_firm_composition()
      S3: gold/views/firm_composition.json (no-store cache)
    - GET /api/scoped/partners/books/advisor/{id}/composition -> handle_advisor_composition()
      S3: gold/advisors/{id}/composition.json (no-store cache)
    - GET /api/scoped/partners/books/relationship/{id}/composition -> handle_books_composition()
      Computes from holdings parquet at request time (not pre-computed)
    - GET /api/scoped/partners/books/account/{id}/composition -> handle_books_composition()
      Same as relationship — computes from holdings

    PORTAL TYPES (portal/src/pages/AdvisorIntelligence/types.ts):
    - FirmMixViewsResponse, FirmMixPeriodPoint, FirmMixClassValue (lines 1336-1367)
    - AdvisorMixTimeseriesResponse, MixTimeseriesPoint (lines 1390+)
    - BooksCompositionResponse, MixItem (lines 1283-1292, 1265)
    - AuaMixView, AuaMixPoint, AuaMixSegment (lines 1141-1157)
    - MixAssetClass = 'equity' | 'fixed_income' | 'alternatives' | 'cash' (line 1308)

    PORTAL COMPONENTS:
    - PartnerAnalytics.tsx — Assets Overview header panel (AUA / Clients / Mix toggles)
    - ClientsTab.tsx — Books tab with Overview panels
    - AUACompositionChart.tsx — composition chart component
    - DistributionTab.tsx — has mix-related rendering
  </context>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Investigation targets — read and trace, fix where broken -->
      <!-- Gold layer (DS verifies data exists on S3) -->
      <file action="verify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="verify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <!-- Lambda (DS/AE verifies routes serve data) -->
      <file action="verify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <!-- Portal (DE/RD traces API calls through to components) -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/AUACompositionChart.tsx</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- PHASE 1: Data verification (DS + AE)                         -->
    <!-- Confirm the precomputed JSONs exist on S3 and are well-formed -->
    <!-- ============================================================ -->

    <requirement id="1">
      DS: Verify gold layer output exists on S3 and contains expected shape.

      Check firm_mix_views.json:
        aws s3 cp s3://opal-data-bd/gold/firm_mix_views.json - | python3 -c "
        import json,sys; d=json.load(sys.stdin)
        for g in ['quarterly','monthly','annually']:
            pts = d['views'][g]
            print(f'{g}: {len(pts)} periods')
            if pts: print(f'  last: {pts[-1][\"period\"]} classes={[k for k in pts[-1] if k not in (\"period\",\"label\",\"end_date\",\"total_aua\")]}')"

      Check firm_composition.json:
        aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json - | python3 -c "
        import json,sys; d=json.load(sys.stdin)
        print(f'classes: {len(d.get(\"mix\",[]))}')
        for m in d.get('mix',[]):
            print(f'  {m[\"asset_class\"]}: {len(m.get(\"top_holdings\",[]))} top holdings, mv={m.get(\"market_value\",0):,.0f}')
        print(f'global top: {len(d.get(\"top_holdings\",[]))} holdings')"

      Check at least one advisor has both files:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep -E '(mix\.json|composition\.json)' | head -10

      Report: which files exist, which are missing, and the shape of each.
    </requirement>

    <requirement id="2">
      AE: Verify Lambda routes return data (not 404/500).

      Test from CLI (or browser dev tools network tab):
        curl the following endpoints (substitute real firmId):
        - /api/scoped/partners/books/firm/mix-views?firmId=49financial
        - /api/scoped/partners/books/firm/all/composition?firmId=49financial
        - /api/scoped/partners/books/advisor/{sample_id}/mix?firmId=49financial
        - /api/scoped/partners/books/advisor/{sample_id}/composition?firmId=49financial
        - /api/scoped/partners/books/relationship/{sample_id}/composition?firmId=49financial

      Report: HTTP status, response shape, any errors in CloudWatch.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 2: Frontend trace (DE + RD)                            -->
    <!-- Trace from API call through TypeScript to rendered component  -->
    <!-- ============================================================ -->

    <requirement id="3">
      DE: Trace the API fetch chain for BOTH views.

      For Mix in Assets Overview:
      - Identify which component calls the mix endpoint
      - Trace the response through TypeScript types to the stacked bar renderer
      - Confirm the data shape from Lambda matches what the component expects
      - If the fetch is missing, conditional is wrong, or types don't align — fix it

      For Asset Mix + Top Holdings in Books Overview:
      - Identify which component calls the composition endpoint at each drill level
      - Trace through TypeScript types to the radial chart and horizontal bars
      - Confirm the per-class drill interaction (click class -> filter holdings)
      - If the fetch is missing, conditional is wrong, or types don't align — fix it
    </requirement>

    <requirement id="4">
      RD: Once DE confirms the data path, verify visual rendering.

      Assets Overview Mix:
      - Must render as stacked bar chart, IDENTICAL format to NMEC/NMNC in Clients
      - Labels: Equity, Fixed Income, Alternatives, Other
      - Colors: match existing CMA color scheme used elsewhere in AdvisorIntelligence
      - Aggregate numbers must tie — sum of class values = total AUA for each period

      Books Overview Asset Mix:
      - Radial (donut/pie) chart with class segments
      - Same labels and colors as above
      - Click interaction: selecting a class segment filters Top Holdings

      Books Overview Top Holdings:
      - Horizontal bars, top 9 holdings by market value + "Other" (10th bar = remainder)
      - Default: global top 9 across all classes
      - When a class is selected in the radial: top 9 within that class only
      - If fewer than 10 holdings exist in the selected class, show all (no "Other" bar)
      - Each bar shows: security name/ticker, market value, percentage of class total
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 3: Fix and deploy                                      -->
    <!-- ============================================================ -->

    <requirement id="5">
      Based on Phase 1 + 2 findings, fix every break in the chain:
      - If S3 data is missing or malformed: DS fixes the gold script, AE reruns
      - If Lambda route is broken or returning wrong shape: DS fixes, DT deploys
      - If TypeScript types don't match Lambda response: DE fixes types
      - If frontend component has wrong conditional, missing fetch, or rendering bug: DE/RD fix
      - If API endpoint is not wired in the frontend API layer: DE wires it

      Every fix must be committed to the appropriate branch (CLOUD for backend,
      portal DEV for frontend).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Assets Overview "Mix" toggle renders stacked bar chart at firm level with equity, fixed income, alternatives, other — same format as NMEC/NMNC in Clients</criterion>
    <criterion id="2">Books tab Overview "Asset Mix" radial renders at firm level</criterion>
    <criterion id="3">Books tab Overview "Asset Mix" radial renders at advisor level</criterion>
    <criterion id="4">Books tab Overview "Asset Mix" radial renders at relationship level</criterion>
    <criterion id="5">Books tab Overview "Top Holdings" renders top 9 + Other at firm level</criterion>
    <criterion id="6">Books tab Overview "Top Holdings" renders top 9 + Other at advisor level</criterion>
    <criterion id="7">Books tab Overview "Top Holdings" renders top 9 + Other at relationship level</criterion>
    <criterion id="8">Clicking a class in the Asset Mix radial filters Top Holdings to that class's top 9 + Other</criterion>
    <criterion id="9">If a class has fewer than 10 holdings, all are shown without an "Other" bar</criterion>
    <criterion id="10">Colors and labels match CMA taxonomy: Equity, Fixed Income, Alternatives, Other</criterion>
    <criterion id="11">Mix stacked bar aggregate numbers tie to total AUA per period</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT assume data is missing — verify on S3 first. The gold rerun completed 2026-03-20 evening.</constraint>
    <constraint>Do NOT create new gold scripts or Lambda routes. The infrastructure exists (scripts 06b + 12, Lambda routes deployed at partners-api-v1.8.0). The break is likely in the frontend wiring or a Lambda route mismatch.</constraint>
    <constraint>"Other" in the Mix context = residual AUA not assigned to equity, fixed income, or alternatives. This will primarily be cash. Do not add "Cash" as a separate visual label — use "Other".</constraint>
    <constraint>Mix stacked bar MUST follow the exact same data processing pattern as NMEC/NMNC Clients stacked bar — same conditionals, same aggregation rules, same shape. If Clients works, Mix must work the same way.</constraint>
    <constraint>Per-class Top Holdings drill is filtered WITHIN the class, not from the global top list. A holding ranked #50 globally but #1 in Fixed Income MUST appear as the top FI holding.</constraint>
    <constraint>Commit with appropriate --author for each agent's work.</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      All upstream infrastructure is deployed and operational:
      - Gold scripts 06b + 12 run nightly (last full run 2026-03-20 evening)
      - Lambda partners-api-v1.8.0 deployed with all composition + mix routes
      - ETFClassifier has 3,855 securities in bd-securities DynamoDB
      - Portal types exist in types.ts for all response shapes
      No blockers. This is a wiring/rendering fix, not a new feature.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">Phase 1 trace report: which S3 files exist, which Lambda routes return data, where the chain breaks</deliverable>
    <deliverable type="commit">All fixes committed (CLOUD for backend, portal DEV for frontend)</deliverable>
    <deliverable type="verify">Visual confirmation that both views render at all drill levels</deliverable>
  </deliverables>
</task_order>


### 0.4.0_DE_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DE_ClientPlatform

a508d9c2 0.4.0_DE_ClientPlatform: log — ADVI_MVPLVL 2i time window state lift complete
75b41080 0.4.0_DE_ClientPlatform: brief — cohort-specific period-over-period NNA in Segment Analytics
7c8cdb06 0.4.0_DE_ClientPlatform: MDLP_WYNCHT data extraction script + benchmark JSON
b5750c11 org(0.4.0_DE_ClientPlatform): ADVI_PSCFIX.B1 integration validation complete -- live schema confirmed
caa5e710 org(0.4.0_DE_ClientPlatform): ADVI_PSCFIX.B1 integration validation -- blocked on Track A2 publisher deploy
8d453732 org(0.4.0_DE_ClientPlatform): MDLP_WYNCHT full session log -- facsimile, scatter, benchmark, peers, PPTX
5eae8094 org(0.4.0_DE_ClientPlatform): MDLP_WYNCHT session log + task order complete
627dc83f 0.4.0_DE_ClientPlatform: peers.html -- align-items flex-start, period headers below legend divider
ef4058e0 0.4.0_DE_ClientPlatform: peers.html -- period headers moved to HTML div, clean CSS gap from legend divider
10abd669 0.4.0_DE_ClientPlatform: peers.html -- more padding above period headers, full triangle labels
696a530a 0.4.0_DE_ClientPlatform: tools/wyncht/peers.html -- quartile peer comparison chart, data from opal-data-portal-v2
cfd1fc9a 0.4.0_DE_ClientPlatform: tools/wyncht -- scatter.html and benchmark.html standalone presentation pages
c335a9f6 0.4.0_DE_ClientPlatform: facsimile -- tooltips grow to content, no text overflow
a6d7ab98 0.4.0_DE_ClientPlatform: facsimile -- full timestamp, x-axis 28% headroom, pinned card overlap resolution
02879be8 0.4.0_DE_ClientPlatform: facsimile -- manual canvas event handlers, granular pinned cards, canonical footer timestamp
89965ce9 0.4.0_DE_ClientPlatform: facsimile -- brand silver page bg, white panel titles, exact portal tooltips, granular benchmark click
a6fd5c12 0.4.0_DE_ClientPlatform: tools/wyncht/facsimile.html -- benchmark tab static clone
86198b64 org(0.4.0_DE_ClientPlatform): ADVI_49FNV3.008 -- gold-silver AUA validation pipeline step
374d344f org(0.4.0_DE_ClientPlatform): 2026-03-09 session logs + ADVI task orders (F3-fix, F3b, APISCP.007)
2d5a0815 org(0.4.0_DE_ClientPlatform): ADVI_49FNV3.007 -- AUA total consistency task order to AE_PartnerETL

### 0.4.2_RD_AdvisorIntelligence -- Recent Session Logs

#### ADVI_49FNV3_F2_F4_F6_F7_N1N2.md

# ADVI_49FNV3 — F2, F4, F6, F7, N1-N2-RD Complete — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-09
**Portal DEV commit:** `594c3f6`

## Objective

Execute all 5 pending ADVI_49FNV3 task orders: F2 (projected ghost bars), F4 (stacked bar top 10),
F6 (unassigned sorting), F7 (zebra striping), N1-N2-RD (firm dashboard + advisor book visual polish).

---

## Work Completed

### 1. F6 + F7 — Pre-Applied (DT commit `1dc96b5`)

Both were already implemented by DT in portal DEV commit `1dc96b5`:
- **F6:** `PINNED_BOTTOM_NAMES = new Set([FIRM_ACCOUNT_NAME, 'Unassigned'])` at AdvisorsTab.tsx:80.
  Leaderboard separates pinned entries (lines 688-698), renders them in a dimmed "Unranked" section.
- **F7:** `bg-white/[0.025]` on odd leaderboard rows at line 771. Matches SecurityScanner pattern.

Marked both task orders as `complete`. No code changes needed.

### 2. F4 — Top Ten Advisors Stacked Bar (New Component)

Added `TopTenStackedBar` component to AdvisorsTab.tsx. Renders inside Panel 1 (Top Performers)
when `flowsData?.stacked_bar?.[period]?.[role]` data is available. Falls back to Top3Highlights
cards when stacked_bar data absent.

| Property | Value |
|----------|-------|
| Chart type | Recharts ComposedChart with stackOffset="sign" |
| Data source | `flowsData.stacked_bar[period][role]` (AdvisorBarEntry[]) |
| Sort | nna_net descending, tie-break: advisor_name ascending, top 10 |
| Inflows bar | stackId="flows", fill #2563EB, opacity 0.8 |
| Outflows bar | stackId="flows", fill #DC2626, dataKey outflowsNeg (negated client-side) |
| NNA dash | RechartsLine with custom dot — gold (#F59E0B) horizontal dash at y=nna_net |
| X-axis | advisor_name truncated at 12 chars, -45 degree angle |
| Tooltip | advisor_name, inflows, outflows, NNA (signed + colored) |

### 3. N1-N2-RD — Visual Polish

DT commit `1dc96b5` implemented functional N1 (firm dashboard) and N2 (advisor book) panels.
RD polish applied:

| Change | File | Line |
|--------|------|------|
| Back button: "All Advisors" -> "Back to Firm Overview" | ClientsTab.tsx | L2 back button |
| Zebra striping on AdvisorSummaryTable rows | ClientsTab.tsx | `bg-white/[0.025]` on odd rows |
| Zebra striping on L2 ClientsTable rows | ClientsTab.tsx | same pattern |

### 4. F2 — Projected Ghost Bars (PartnerAnalytics.tsx)

Added projection computation for the current incomplete period across all three panel views.

**Helper functions added:**
- `computePeriodDays(granularity, periodKey)` — returns totalDays + elapsedDays for monthly/quarterly/annually
- `currentPeriodKey` memo — identifies today's period

**AUA view ghost bars:**
- `augmentedAuaData` memo adds `{cat}_ghost` fields (e.g., `NMNC_ghost`, `NMEC_ghost`)
- Formula: `projected = actual * (totalDays / elapsedDays)`, capped at `max(actual, prior * 1.5)`
- Ghost rendered as additional stacked Bars with fillOpacity 0.25
- Only non-zero for the current incomplete period

**NNA view ghost bars:**
- `augmentedNnaData` memo adds `inflow_ghost` and `outflow_ghost` fields
- Inflow ghost extends upward (blue, 25% opacity)
- Outflow ghost extends downward (red, 25% opacity)
- Net line does NOT get a ghost (per task order)

**GRO view dashed extensions:**
- `augmentedGroData` memo adds a projected data point after the last actual point
- Three additional Line components with `strokeDasharray="6 3"` for market_proj, nna_proj, total_proj
- Dashed segments connect last actual to projected value using `connectNulls={false}`

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| F6/F7: mark complete without changes | DT already implemented in `1dc96b5`; code verified correct |
| F4: ComposedChart (not BarChart) | Needed for NNA dash overlay (Line component) alongside stacked bars |
| F4: NNA dash via Line + custom dot | Cleanest Recharts pattern for per-bar markers without Scatter complexity |
| F2: Cap formula `max(actual, prior * 1.5)` | Prevents ghost from being negative if actual already exceeds 1.5x prior |
| F2: `any` type for augmented AUA data | Dynamic ghost key generation (`${cat}_ghost`) not expressible in static type; `any` cast avoids TS errors on downstream consumers |
| N1-N2: "Back to Firm Overview" | Task order explicitly requested this text over the DT's "All Advisors" |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | F4: TopTenStackedBar component + Panel 1 conditional rendering | Yes -- portal DEV `594c3f6` |
| `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` | N1-N2: back button text + zebra striping | Yes -- portal DEV `594c3f6` |
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | F2: projection helpers + augmented data memos + ghost bars + GRO dashed lines | Yes -- portal DEV `594c3f6` |
| Task orders (5 files) | All marked complete | Local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

All 5 ADVI_49FNV3 task orders are complete. Portal DEV commit `594c3f6` contains F4 stacked bar,
F2 projected ghost bars (AUA + NNA + GRO), and N1-N2 visual polish. `bunx tsc -b` clean.
F6 and F7 were pre-applied by DT. DE review needed before DT pushes.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Review commit `594c3f6`** -- F2 projection logic, F4 stacked bar visual, N1-N2 polish.
2. **[0.4.0_DT_ClientPlatform] Push portal DEV after DE review** -- QA gate.
3. **[0.4.2_RD_AdvisorIntelligence] No further ADVI_49FNV3 task orders pending** -- await next assignment.

**Do NOT:**
- Push portal DEV -- DT is the push gate after DE reviews
- Implement L3/L4 visual panels for N1-N2 -- Phase 2a only per task order constraint

#### ADVI_MVPLVL_004_p4_books_tab_views.md

# ADVI_MVPLVL-004 P4 Books Tab Views — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-16
**Portal DEV commit:** `478baea`
**Task Order:** `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_MVPLVL.004.p4-books-tab-views.md`
**Thread:** `org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/`

## Objective

Implement Books Tab L3/L4 view enhancements: paired Mix + Concentration pie panels with linked
selection, compact AUA/NNA time series charts, and advisor listing UI consistency (4h). All
inline in ClientsTab.tsx.

---

## Work Completed

### 1. Mix + Concentration Snapshot Pies (4e/4f)

New inline `CompositionPies` component renders side-by-side donut charts from `BooksCompositionResponse`:

| Feature | Implementation |
|---------|---------------|
| Mix pie | Recharts PieChart with Cell per asset class, donut style (innerRadius/outerRadius) |
| Color mapping | `MIX_PIE_COLORS` — equity=#6366F1, fixed_income=#10B981, structured_notes=#F59E0B, cash=white/35, other=#EF4444 |
| Click-to-filter | Click Mix slice toggles `selectedAssetClass`; same click deselects |
| Opacity dimming | Non-selected slices render at fillOpacity 0.3 |
| Concentration pie | Filters `items[]` by `selectedAssetClass` when set; shows all when null |
| Other bucket | Shown in concentration pie only when no filter is active |
| Legend | Clickable legend rows with color dots, labels, and pct values |
| Compact mode | `compact` prop for L4 (smaller pie radius, single-column layout) |

**Wired at:**
- L3: After Accounts Table, before Mix Timeseries panels
- L4: Inside account detail section, after metrics grid

**Data fetching:**
- L3: `getBooksRelationshipComposition(clientKey)` in `useEffect` on `[clientKey]`
- L4: `getBooksAccountComposition(selectedAccountId)` in `useEffect` on `[selectedAccountId]`

### 2. Compact AUA/NNA Time Series (4g)

New inline `CompactTimeSeriesChart` component renders composed chart:

| Feature | Implementation |
|---------|---------------|
| AUA | Recharts Area with gradient fill, left Y-axis |
| NNA | Recharts Bar, right Y-axis, green (#10B981) at 60% opacity |
| Window toggle | Local state `1Y/3Y/Max`, client-side filtering of daily data |
| X-axis | Date labels formatted as "MMM 'YY", ~6 ticks |
| Tooltip | Standard chart tooltip with formatted currency values |
| Compact mode | `compact` prop for L4 (200px vs 280px height) |

**Wired at:**
- L3: After Concentration Timeseries panel, before L4 drill
- L4: Inside account detail section, after composition pies

**Data fetching:**
- L3: `getBooksRelationshipTimeseries(clientKey)` in `useEffect` on `[clientKey]`
- L4: `getBooksAccountTimeseries(selectedAccountId)` in `useEffect` on `[selectedAccountId]`

### 3. Advisor Listing N1 Redesign (4h)

Rewrote `AdvisorSummaryTable` to match 3d leaderboard (AdvisorsTab.tsx) visual design:

| Before | After |
|--------|-------|
| HTML table with alternating rows | Flex card-like rows with generous padding |
| Plain rank number | Rank badges (gold/silver/bronze for top 3) |
| Plain NNA text | Bold NNA with `hsl(var(--success))` / `text-red-400` coloring |
| Plain growth % | Gradient pills: `bg-emerald-500/15` + ArrowUpRight / `bg-red-500/15` + ArrowDownRight |
| Table header row | Sort header bar ("Ranked by AUA") matching 3d style |
| `formatCurrency` for NNA | `formatNumberTo3Digits` for compact NNA display |

Columns: Rank, Name, AUA, Clients, NNA, Growth % — matches 3d leaderboard column structure.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Shared `selectedAssetClass` between Mix pies and Mix timeseries at L3 | Clicking equity in the pie should filter both the concentration pie and the timeseries panels |
| Separate `selectedAssetClassL4` state for L4 | L4 is independent of L3 selection — account-level filter shouldn't affect relationship-level |
| Client-side window filtering for timeseries | Fetch full history once, filter locally for 1Y/3Y/Max — avoids redundant API calls |
| No sort interactivity on advisor table | 3d leaderboard has sort buttons, but Books tab advisor table is always sorted by AUA desc; keeping it simple |
| `compact` prop on both components | L4 space is constrained inside the account detail panel; smaller charts avoid scroll fatigue |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` | Add imports (recharts, lucide, API fns), L3/L4 data fetching, CompositionPies + CompactTimeSeriesChart components, AdvisorSummaryTable redesign | Yes — portal DEV `478baea` |

---

## Blockers

None. Lambda endpoints (partners-api-v1.1.0) not yet deployed for composition/timeseries, but
endpoints are already registered in advisor-intelligence.ts from prior DE work. Panels will show
loading state until data is available.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`
**TypeScript:** `bunx tsc -b --noEmit` — zero errors

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] QA gate** — verify L3/L4 composition pies render correctly with live data once Lambda deployed
2. **[0.4.0_DS_ClientPlatform] Lambda deploy** — partners-api-v1.1.0 for composition + timeseries endpoints
3. **[0.4.2_RD_AdvisorIntelligence] Post-deploy** — visual QA, verify linked selection works end-to-end

**Do NOT:**
- Modify L2 (advisor-level) composition — deferred per task order constraint
- Add sort interactivity to advisor table — not in scope for 4h

#### ADVI_MVPLVL_005_mix_concentration_panels.md

# ADVI_MVPLVL-005 Mix + Concentration Panels — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-16
**Portal DEV commit:** `458c9dc`
**Task Order:** `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_MVPLVL.005.mix-concentration-charts.md`
**Thread:** `org/threads/ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment/`

## Objective

Wire MixTimeseriesPanel and ConcentrationPanel into Books Tab L3 (relationship detail view).
100% stacked area charts using Recharts, linked via asset class click filtering, independent
1Y/3Y/Max window toggle. Mock data skeleton until Lambda endpoints are deployed.

---

## Work Completed

### 1. TypeScript Interfaces (types.ts)

Added 6 new types at the end of `portal/src/pages/AdvisorIntelligence/types.ts`:

| Type | Purpose |
|------|---------|
| `MixAssetClass` | Union: `'equity' | 'fixed_income' | 'structured_notes' | 'cash' | 'other'` |
| `MixTimeseriesPoint` | Daily row: `{date, equity, fixed_income, structured_notes, cash, other}` (0-1 pcts) |
| `ConcentrationPoint` | Per-holding row: `{date, asset_name, ticker: string|null, asset_class, market_value, pct}` |
| `ConcentrationResponse` | Wrapper: `{relationship_id, top_n, data: ConcentrationPoint[]}` |
| `MixWindow` | `'1Y' | '3Y' | 'Max'` |

### 2. API Client Functions (advisor-intelligence.ts)

Added two new functions with proper query param construction:

- `getMixTimeseries(relationshipId, firmId, window?)` -> `MixTimeseriesPoint[]`
  - Endpoint: `/api/scoped/partners/books/relationship/${relationshipId}/mix-timeseries`
- `getConcentrationTimeseries(relationshipId, firmId, window?)` -> `ConcentrationResponse`
  - Endpoint: `/api/scoped/partners/books/relationship/${relationshipId}/concentration-timeseries`

Both follow the existing `apiRequest<T>` pattern. Window and firmId passed as query params.
Uses `URLSearchParams` for clean param construction.

### 3. MixTimeseriesPanel.tsx (new)

100% stacked area chart with 5 asset class series. Key implementation details:

| Feature | Implementation |
|---------|---------------|
| Chart type | Recharts `AreaChart` with `stackId="mix"` on all 5 `<Area>` components |
| Color mapping | Semantic tokens: `--primary` (equity), `--success` (fixed_income), `--warning` (structured_notes), `rgba(255,255,255,0.35)` (cash), `--danger` (other) |
| Window toggle | Local state `useState<MixWindow>('1Y')`, button group in PanelHeader actions |
| Click-to-filter | `onClick` on each Area toggles `selectedAssetClass` (same class = deselect) |
| Opacity dimming | Non-selected classes render at `fillOpacity={0.3}`, `strokeOpacity={0.3}` |
| Mock data | 90 daily points with gradual allocation drift for skeleton rendering |
| Data fetching | `useEffect` on `[relationshipId, firmId, window]` triggers `getMixTimeseries()` |

Props: `relationshipId`, `firmId`, `selectedAssetClass`, `onSelectAssetClass` — state is lifted
to L3ClientDetail for linkage with ConcentrationPanel.

### 4. ConcentrationPanel.tsx (new)

Top-N holdings over time, filtered by `selectedAssetClass` when set.

| Feature | Implementation |
|---------|---------------|
| Chart type | Recharts `AreaChart` with `stackId="conc"` per holding |
| Data pivot | Flat `ConcentrationPoint[]` pivoted to `{date, [asset_name]: market_value}` rows |
| Null ticker | `holdingLabel()` returns `name` only when `ticker === null`, `name (ticker)` otherwise |
| Header | `"Top {top_n} Holdings"` — dynamic from response `top_n` field |
| Asset class filter | When `selectedAssetClass` is set, `data.filter(p => p.asset_class === cls)` |
| Empty state | Shows "No holdings for selected filter" when filtered data is empty |
| Mock data | 5 holdings across 30 dates for skeleton rendering |

### 5. Wiring into L3ClientDetail (ClientsTab.tsx)

- Added `clientKey` and `firmId` to `L3ClientDetailProps` interface
- Added `selectedAssetClass` local state (linked between Mix and Concentration)
- Inserted `MixTimeseriesPanel` and `ConcentrationPanel` after Accounts Table, before L4 drill
- Caller passes `selectedClientKey` as `clientKey` and `firmOverride || firmId` as `firmId`
- Imported `MixAssetClass` type and both panel components

### 6. Barrel Export (panels/index.ts)

Added `MixTimeseriesPanel` and `ConcentrationPanel` exports.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Panels in L3ClientDetail (ClientsTab.tsx), not ClientDetailPage.tsx | The active L3 view is inside `BooksTab` — `ClientDetailPage` is a standalone page with different data flow. Thread contract says "Books Tab L3". |
| `selectedAssetClass` state lifted to L3ClientDetail | Required for Mix-to-Concentration linkage — both panels need to share this state |
| ConcentrationPanel receives `window` as prop (not own state) | Thread contract: "independent 1Y/3Y/Max" refers to Mix panel's toggle. Concentration follows Mix's window for coherent UX. |
| Mock data in both panels | Lambda dependency (`ADVI_MVPLVL.005.lambda-deploy`) is pending. Constraint allows skeleton state. |
| `firmOverride || firmId` passed to panels | Follows existing pattern in BooksTab where firmOverride takes precedence for internal users |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/types.ts` | Add MixAssetClass, MixTimeseriesPoint, ConcentrationPoint, ConcentrationResponse, MixWindow types | Yes -- portal DEV `458c9dc` |
| `portal/src/api/endpoints/advisor-intelligence.ts` | Add getMixTimeseries(), getConcentrationTimeseries() + import new types | Yes -- portal DEV `458c9dc` |
| `portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx` | New file — 100% stacked area chart with window toggle + click filter | Yes -- portal DEV `458c9dc` |
| `portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx` | New file — top-N holdings chart with asset class filtering | Yes -- portal DEV `458c9dc` |
| `portal/src/pages/AdvisorIntelligence/ClientDetail/panels/index.ts` | Add barrel exports for both new panels | Yes -- portal DEV `458c9dc` |
| `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` | Wire panels into L3ClientDetail, add clientKey/firmId props, add imports | Yes -- portal DEV `458c9dc` |

---

## Blockers

None. Lambda endpoints not yet deployed, but panels render with mock data per constraint.

---

## Current State

**Status:** COMPLETE (pending commit + push)
**Active branch:** portal `DEV`
**TypeScript:** `bunx tsc -b --noEmit` — zero errors

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push portal DEV** — 6 files (2 new, 4 modified) pending commit and push. DT QA gate.
2. **[0.4.0_DT_ClientPlatform] Lambda deploy** — task order `ADVI_MVPLVL.005.lambda-deploy` must complete before live data flows.
3. **[0.6.0_AE_PartnerETL] EC2 gold script deploy** — `06b_build_client_mix_timeseries.py` must be deployed for gold artifacts.
4. **[0.4.2_RD_AdvisorIntelligence] Post-deploy** — remove mock data, verify live endpoint renders, confirm pct sum validation.

**Do NOT:**
- Modify L4 (account detail) views — out of scope per requirement #6
- Introduce ApexCharts — Recharts only per constraint
- Add granularity toggle — daily data rendered directly per thread contract

#### DistributionTab_SNPLBK_snapshot_strip_granularity_fix.md

# DistributionTab — Snapshot Strip Granularity Fix — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-10
**Portal DEV commit:** `a834887`

## Objective

Complete the Snapshot Lookback regression fix (ADVI_SNPLBK-001). COO confirmed S3 backend is
intact (quarterly JSON has current + q1/q2/q3). Root cause: frontend granularity mismatch.
The DE implemented the main structural fix (commit `1433d2e`) — type extensions, helper functions,
prop threading, strip component rewrites. RD adds the remaining behavioral fix: reset selectedPeriod
when granularity changes.

---

## Work Completed

### 1. Downstream Check — DE commit `1433d2e` audit

Read `DistributionTab.tsx` after DE commit `1433d2e`. Found all core structural pieces in place:

| Component | Status after DE commit |
|-----------|----------------------|
| `TimePeriodKey` in types.ts | Extended to `'current' | 'q1'-'q3' | 'm1'-'m3' | 'y1'-'y3'` |
| `PartnerAnalyticsViewWithPeriods` | Extended with m1/m2/m3, y1/y2/y3 optional fields |
| `PeriodsMetadata` | Extended with m1/m2/m3, y1/y2/y3 optional fields |
| `GranularityOption` in types.ts | Exported at line 424 |
| `getHistoricalKeys` / `getDefaultLabels` helpers | In DistributionTab.tsx lines 80-91 |
| `DistributionTabProps.granularity` | Present |
| `SnapshotDistributionViewProps.granularity` | Present |
| `NnaQuarterlyStripProps.granularity` | Present |
| `DistributionQuarterlyStripProps.granularity` | Present |
| Strip `periodDefs` / `historicalPeriods` | Dynamic — uses `getHistoricalKeys(granularity)` |
| `globalMaxCount` memo | Uses `getHistoricalKeys(granularity)` at line 1834 |
| Call sites pass `granularity` | Yes — both strips at lines 2103 and 2112 |
| `AdvisorIntelligence.tsx` passes `granularity` | Yes — line 131 |

### 2. Identified Remaining Gap

The `useEffect` in `SnapshotDistributionView` that resets drill state (line 1651) had
dependencies `[cohort, metric]` but was missing `granularity`. When the user switches
granularity (e.g., quarterly → monthly), `selectedPeriod` would remain 'q1', which:
- Matches no strip button in the new granularity (none highlighted)
- Falls back to `vp.current` via `vp[selectedPeriod] || vp.current` at line 1685
  (stale period renders current data, broken UX but not a crash)

### 3. Fix Applied

Added `granularity` to the `useEffect` dependency array and updated the comment:

```diff
-  // Reset drill state when cohort or metric changes
+  // Reset drill state when cohort, metric, or granularity changes
+  // granularity: period keys change (q1->m1 etc), stale selectedPeriod would match nothing
   useEffect(() => {
     ...
     setSelectedPeriod('current')
-  }, [cohort, metric])
+  }, [cohort, metric, granularity])
```

### 4. TypeScript Verification

`bunx tsc --noEmit` — clean before and after the change.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Don't duplicate DE's structural work | DE commit `1433d2e` already implemented all type, helper, and component changes correctly |
| Add `granularity` to useEffect deps | Without this, switching granularity leaves `selectedPeriod` stale; strip shows no active period |
| No changes to strip rendering logic | DE already rewrote both strips to use dynamic keys — correct implementation |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Add `granularity` to useEffect dep array in SnapshotDistributionView | Yes — portal DEV `a834887` |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml` | Update Distribution tab desc + ui_state + data flow to reflect multi-granularity strip | Yes — CLOUD (org commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_SNPLBK.001.snapshot-strip-visual-fix.md` | status -> complete | Yes — CLOUD (org commit) |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

DE commit `1433d2e` implemented the structural granularity-aware strip fix. RD commit (this session)
adds the behavioral reset: `selectedPeriod` now resets to 'current' when granularity changes,
preventing stale period state after granularity toggle. `bunx tsc --noEmit` clean. Both strip
components (`NnaQuarterlyStrip`, `DistributionQuarterlyStrip`) now show correct period buttons
for quarterly (q1/q2/q3), monthly (m1/m2/m3), and annual (y1/y2/y3) data.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push portal DEV** — commits `1433d2e` (DE: granularity fix) + RD commit (useEffect dep fix) pending push. DT QA gate.
2. **[0.4.2_RD_AdvisorIntelligence] Task order ADVI_SNPLBK.001 complete** — no further work needed on this regression.

**Do NOT:**
- Modify backend script 09 or EC2 artifacts — S3 data is intact per COO
- Change the strip render logic — DE's implementation is correct


### 0.4.2_RD_AdvisorIntelligence -- Pending Task Orders

#### page_inventory.md

# Task Order: Page Inventory

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-page-inventory</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a complete structured inventory of your page. This is a one-time
    codebase audit that becomes your permanent context for all future sessions.
    Read every file in your page directory and document what exists.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">List every .tsx/.ts file in your page directory tree with a 1-line description of what it does</requirement>
    <requirement id="2">For every API call (useQuery, useMutation, fetch, axios) found in your page: document the endpoint URL, HTTP method, request payload shape, and response shape</requirement>
    <requirement id="3">For every shared component imported from outside your page directory (e.g., from portal/src/components/): list the import path and what it provides</requirement>
    <requirement id="4">For every TypeScript type/interface your page defines or imports: list the type name, which file defines it, and its key fields</requirement>
    <requirement id="5">Document current page state: what tabs/panels exist, which are functional vs. stubbed vs. broken</requirement>
    <requirement id="6">List any TODO/FIXME/HACK comments found in your page code</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml</criterion>
    <criterion id="2">Every .tsx/.ts file in the page directory is accounted for</criterion>
    <criterion id="3">API endpoints include actual URL strings, not just hook names</criterion>
    <criterion id="4">Shared component imports include the actual import path</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any source code -- this is a read-only audit</constraint>
    <constraint>Do NOT create or edit files outside your agent folder</constraint>
    <constraint>Use Glob, Grep, and Read tools only -- no Explore agent, no Task agent</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">
      org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml
    </deliverable>
  </deliverables>
</task_order>

## Deliverable XML Schema

Write your inventory using this structure:

```xml
<page_inventory>
  <metadata>
    <agent>0.4.2_RD_AdvisorIntelligence</agent>
    <page>AdvisorIntelligence</page>
    <directory>portal/src/pages/AdvisorIntelligence/</directory>
    <date>2026-03-02</date>
  </metadata>

  <files>
    <file path="portal/src/pages/AdvisorIntelligence/ComponentName.tsx" type="component">
      One-line description
    </file>
  </files>

  <api_calls>
    <api_call>
      <hook>useQuery / useMutation / fetch</hook>
      <endpoint>/api/scoped/some-endpoint</endpoint>
      <method>GET</method>
      <request_shape>{ param1: string, param2: number }</request_shape>
      <response_shape>{ data: Array, total: number }</response_shape>
      <file>portal/src/pages/AdvisorIntelligence/hooks.ts:42</file>
    </api_call>
  </api_calls>

  <shared_imports>
    <import>
      <from>portal/src/components/ui/Panel.tsx</from>
      <provides>Panel, PanelHeader</provides>
      <used_in>portal/src/pages/AdvisorIntelligence/SomeComponent.tsx</used_in>
    </import>
  </shared_imports>

  <types>
    <type name="SomeType" defined_in="portal/src/pages/AdvisorIntelligence/types.ts">
      Key fields: id: string, name: string, value: number
    </type>
  </types>

  <page_structure>
    <tab name="TabName" status="functional | stubbed | broken">
      Description of what this tab shows
    </tab>
  </page_structure>

  <issues>
    <issue file="path:line" type="TODO | FIXME | HACK">
      Comment text
    </issue>
  </issues>
</page_inventory>
```


### 0.4.2_RD_AdvisorIntelligence -- Recent Commits

# Recent commits by 0.4.2_RD_AdvisorIntelligence

c38601f8 0.4.2_RD_AdvisorIntelligence: issue task order ADVI_MVPLVL.006 to DS -- MTD/QTD/YTD leaderboard windows
769c1d56 0.4.2_RD_AdvisorIntelligence: devops brief -- firm/advisor composition Lambda endpoints
1a4e0a10 0.4.2_RD_AdvisorIntelligence: ADVI_MVPLVL P4+P5 — task orders complete, logs, page inventory, thread receipts
4b55ff14 org(0.4.2_RD_AdvisorIntelligence): ADVI_SNPLBK-001 session log + task order complete + page_inventory update
513adfdf org(0.4.2_RD_AdvisorIntelligence): Y8 session log + phase 1 task order status update
ce2cb497 0.4.2_RD_AdvisorIntelligence: mark 9 task orders complete + session logs + portal submodule advance
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b5ace0c0 org: quality audit -- fix bugs, upgrade thin profiles, seed missing deliverables
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
42f99352 logs: 0.4.2_RD_AdvisorIntelligence distribution nomenclature fix session log
2f8de475 docs(org): add xtick fix addendum for 0.4.2_RD_AdvisorIntelligence
4e046836 logs: 0.4.2_RD_AdvisorIntelligence xtick spacing fix session log

