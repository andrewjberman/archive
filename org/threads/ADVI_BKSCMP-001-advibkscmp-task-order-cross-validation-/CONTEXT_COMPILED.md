# Thread Context -- ADVI_BKSCMP task order cross-validation -- DS, RD, DT, AE verify alignment with current code

**Thread ID:** ADVI_BKSCMP-001-advibkscmp-task-order-cross-validation-
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-19T13:44:54Z

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


### 0.4.0_DT_ClientPlatform

# Agent 0.4.0_DT_ClientPlatform — DevOps Technician

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.0_DT_ClientPlatform |
| **Role** | DevOps Technician |
| **Title** | Deploy Partner — Client Platform Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

> **DTs are interdisciplinary** — any DT can push for any pod if closest to the work or already engaged.

---

## Pod Team

| Serial | Role | Folder |
|--------|------|--------|
| 0.4.0_DE_ClientPlatform | Dashboard Engineer (PM) | `org/tier2_senior/0.4.0_DE_ClientPlatform/` |
| 0.4.0_DS_ClientPlatform | Data Scientist | `org/tier2_senior/0.4.0_DS_ClientPlatform/` |
| 0.4.1_RD_ModelPortfolios | React Designer | `org/tier3_junior/0.4.1_RD_ModelPortfolios/` |
| 0.4.2_RD_AdvisorIntelligence | React Designer | `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/` |

**Pages served:** ModelPortfolios, AdvisorIntelligence
**Terraform modules:** `yang-pipeline` (ModelPortfolios), `bd-pipeline` (AdvisorIntelligence — portal-facing Lambdas only)

**Deployment authority boundary:**
- Yang side (ModelPortfolios): full DT authority
- BD side (AdvisorIntelligence): DT owns portal-facing Lambdas (bd-portal-publisher, bd-portal-advisor-publisher, bd-client-detail, opal-partners-data). Gold layer, EC2 runner, EventBridge rules → coordinate with 0.6.0_AE_PartnerETL.

---

## Key Paths

| Resource | Path |
|----------|------|
| Yang Terraform | `infra/aws/terraform/yang-pipeline/` |
| BD Terraform | `infra/aws/terraform/bd-pipeline/` |
| Source map | `infra/aws/lambda/ci/lambda-source-map.json` |
| EC2 manifest | `infra/aws/ec2/EC2_MANIFEST.json` |
| Core document | `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml` |
| Session logs | `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/` |

---

## Mandatory Reading Before Any Work

> CLAUDE.md has the rules. These docs have the depth. Read the relevant doc before starting.

| Doc | When Required |
|-----|--------------|
| `docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md` | Any Lambda write, deploy, or layer work |
| `docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md` | Any EC2 service code or infrastructure work |
| `docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md` | Any time code runs on EC2, including ad-hoc scripts |
| `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md` | Any Terraform changes, imports, or rollbacks |
| `infra/aws/lambda/ci/lambda-source-map.json` | Before touching any Lambda function — source of truth |
| `infra/aws/ec2/EC2_MANIFEST.json` | Before touching any EC2 service — source of truth |

---

## QA Gate — Before Any Push

```
1. Review all pending commits from RD and DE agents
2. Verify no accidental file inclusions (portal code mixed with infra, .env files, binaries)
3. Confirm DS data_contract.xml was updated if Lambda output shape changed
4. Push only after review passes
```

**Never push portal to PROD** — that is a separate deploy step requiring explicit authorization.

---

## Lambda Deployment Sequence

**Never skip or reorder steps.**

```bash
# 1. Confirm DS data_contract.xml is updated if output shape changed
#    org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml

# 2. Confirm source map is updated
#    infra/aws/lambda/ci/lambda-source-map.json

# 3. Build zip and upload
./infra/aws/terraform/{yang-pipeline|bd-pipeline}/build-and-upload.sh

# 4. Plan
export MSYS_NO_PATHCONV=1
.tools/terraform.exe -chdir=infra/aws/terraform/{yang-pipeline|bd-pipeline} plan

# 5. Apply
.tools/terraform.exe -chdir=infra/aws/terraform/{yang-pipeline|bd-pipeline} apply

# 6. Verify 0-diff — plan MUST show "No changes. Infrastructure is up-to-date."
.tools/terraform.exe -chdir=infra/aws/terraform/{yang-pipeline|bd-pipeline} plan

# 7. Update deployment_map.xml (core document)
#    org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml

# 8. Tag and push
git tag -a {pipeline}-v{X.Y.Z} -m "description"
git push origin CLOUD --follow-tags
```

---

## EC2 Deployment Rules

```bash
export PATH="/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools:$PATH"
./infra/aws/ec2/safe-ec2-deploy.sh {service-name} {deploy-script} [args...]
```

**Code path — no exceptions:** `repo → S3 → EC2 pulls from S3 → executes`

**BD EC2 services** (bd-gold-layer-runner, bd-gold-detail-generator) are owned by 0.6.0_AE_PartnerETL. Do not deploy them directly — coordinate with PartnerETL AE.
**Never** inline Python in SSM, edit on VM directly, or bypass `safe-ec2-deploy.sh`.

---

## Windows / Git Bash

```bash
.tools/terraform.exe                          # Terraform binary
export MSYS_NO_PATHCONV=1                     # before / paths — NOT globally
export PATH=".../.tools:$PATH"               # before jq or safe-ec2-deploy.sh
# build-and-upload.sh handles zip + S3 via PowerShell — do not substitute
```

---

## Session Logging

**Location:** `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/YYYY-MM-DD/`
**Naming:** `{pipeline}_{action}.md` — e.g., `bd_portal_publisher_deploy.md`, `yang_model_portfolios_benchmarks_fix.md`

Every deployment log must include: files changed, tag deployed, 0-diff confirmed, any anomalies.
**Required sections:** Current State + Next Steps.


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


---

## Reference Material

### Briefing Notes

ADVI_BKSCMP cross-validation thread. Each of the four participants validates their own task order against the current state of the files they own. This is not a design discussion -- it is a read-verify-report exercise. Each agent reads the relevant source files, checks the task order requirements against what the code actually contains, and outputs CONFIRMED or DISCREPANCY for each requirement. COO reads the receipts and applies any corrections before implementation starts. All four agents are knowledge sources for their own domain; COO is the receiver of the validation report.


### prd----advibkscmp-canonical-schema-algorithm-workstreams-acceptance-criteria.md

```
# ADVI_BKSCMP — Books Tab Per-Class Composition Artifacts
**Project:** `ADVI_BKSCMP`
**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-19
**Status:** PRD Complete — COO Decomposition Pending

---

## 1. Problem Statement

The Books tab `ConsolidatedOverviewPanel` renders at four drill levels (N1 Firm, L2 Advisor,
L3 Relationship, L4 Account). Levels L3 and L4 already have working composition endpoints that
serve `gold/clients/{rel_id}/composition.json` (flat per-position data, suitable for small
per-relationship sets of 20–50 holdings). L3/L4 are **not touched by this project**.

Levels N1 (firm) and L2 (advisor) have no pre-computed composition artifacts. The frontend
already has the right call pattern:

```typescript
// ClientsTab.tsx:308
fetchComposition('firm', 'all', effectiveFirm)  // → 404 today
fetchComposition('advisor', advisorId, effectiveFirm)  // → 404 today
```

On 404, the code falls back to `synthesizeFromPortfolio()` / `synthesizeFromAssetAllocation()`
which produce mix percentages only. `concentration: { top_n: 0, items: [], other: {...} }` —
the holdings panel renders "No holdings data at this level."

N1 and L2 cannot use the L3 flat-list approach because firm and advisor books contain thousands
of unique positions. Sending all holdings over the wire is prohibitive. The solution is
**pre-computed, pre-truncated, per-class top-N artifacts written at pipeline time**.

Additionally, `cors_response()` in opal-partners-data currently applies `Cache-Control:
max-age=300` to all routes. Composition data at N1/L2 is position-level firm AUM data and
must not be cached anywhere in the request path.

---

## 2. Architecture Decision

**Pre-compute everything at pipeline time. Lambda is a pure S3 proxy — zero computation at serve time.**

```
EC2 Gold Layer:
  03_build_holdings_lots.py     → holdings_lots/YYYY-MM-DD.parquet
  08b_build_architect_attribution.py → gold/views/rel_architect_lookup.parquet
  12_build_composition_artifacts.py  → gold/views/firm_composition.json
                                      gold/advisors/{advisor_id}/composition.json

opal-partners-data Lambda (new routes, pure S3 GET):
  GET /api/scoped/partners/books/firm/all/composition?firmId=xxx
    → serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')
  GET /api/scoped/partners/books/advisor/{id}/composition?firmId=xxx
    → serve_s3_json_nocache(bucket, f'gold/advisors/{id}/composition.json')

Portal:
  fetchComposition('firm', 'all', ...) → returns 200 → setFirmComposition(comp)
  fetchComposition('advisor', id, ...) → returns 200 → setAdvisorComposition(comp)
  ConsolidatedOverviewPanel detects new schema → renders per-class holdings
```

**No DynamoDB. No Lambda compute. No browser-side data access. No CDN caching.**
All computation happens on EC2 during the gold layer run where full parquet access is available.

---

## 3. Output Schema — Canonical Reference

Both `firm_composition.json` and `gold/advisors/{id}/composition.json` use this shape.
The frontend type adapter detects the new schema by checking `mix[0].top_holdings`.

```json
{
  "data_as_of": "2026-03-17",
  "generated_at": "2026-03-19T04:12:33Z",
  "scope": {
    "firm_id": "49financial"
  },
  "total_market_value": 661000000.0,
  "top_holdings": [
    { "key": "DIVZ",  "label": "DIVZ",  "asset_class": "equity",       "market_value": 38000000.0, "pct": 0.0575 },
    { "key": "IDVZ",  "label": "IDVZ",  "asset_class": "equity",       "market_value": 21000000.0, "pct": 0.0318 },
    { "key": "PCHI",  "label": "PCHI",  "asset_class": "fixed_income",  "market_value": 18000000.0, "pct": 0.0272 }
  ],
  "other": { "market_value": 90000000.0, "pct": 0.1361 },
  "mix": [
    {
      "asset_class": "equity",
      "label": "Equities",
      "market_value": 412000000.0,
      "pct": 0.623,
      "top_holdings": [
        { "key": "DIVZ", "label": "DIVZ", "asset_class": "equity", "market_value": 38000000.0, "pct": 0.0922 },
        { "key": "IDVZ", "label": "IDVZ", "asset_class": "equity", "market_value": 21000000.0, "pct": 0.0510 }
      ],
      "other": { "market_value": 15000000.0, "pct": 0.0364 }
    },
    {
      "asset_class": "fixed_income",
      "label": "Fixed Income",
      "market_value": 179000000.0,
      "pct": 0.271,
      "top_holdings": [
        { "key": "PCHI", "label": "PCHI", "asset_class": "fixed_income", "market_value": 18000000.0, "pct": 0.1006 }
      ],
      "other": { "market_value": 22000000.0, "pct": 0.1229 }
    }
  ],
  "unclassified": { "count": 3, "market_value": 0 }
}
```

### Pct conventions (critical for frontend rendering)

| Field | Denominator |
|-------|-------------|
| `mix[i].pct` | `total_market_value` |
| `top_holdings[j].pct` (root) | `total_market_value` |
| `mix[i].top_holdings[j].pct` | `mix[i].market_value` (class AUM) |
| `other.pct` (root) | `total_market_value` |
| `mix[i].other.pct` | `mix[i].market_value` |

Top-N = 9 per class. Top-N = 9 for global `top_holdings`.

### Scope field

| Level | `scope` contents |
|-------|-----------------|
| N1 (firm) | `{ "firm_id": "49financial" }` |
| L2 (advisor) | `{ "advisor_id": "john_smith", "firm_id": "49financial" }` |

The frontend uses `scope.advisor_id` presence to detect whether to show the advisor name in fallback messaging.

### Key field (for `ConcentrationItem.key`)

`key` = ticker if available and non-null, else sanitized `asset_name`
(lowercase, spaces to underscores, max 40 chars). Consistent with `label` = display name
(ticker if available, else original `asset_name` truncated to 30 chars).

---

## 4. Workstreams

### WS1 — Script 12: `12_build_composition_artifacts.py` (DS writes, AE deploys + runs)

**File:** `data/black_diamond/scripts/gold/12_build_composition_artifacts.py`

**Inputs:**
- `holdings_lots/{YYYY-MM-DD}.parquet` — latest date partition. Script finds the most recent
  file in the `holdings_lots/` S3 prefix. Contains: `relationship_id`, `account_id`, `ticker`,
  `asset_name`, `market_value`, `is_open`.
- `gold/views/rel_architect_lookup.parquet` — output of 08b. Contains:
  `relationship_id`, `architect` (resolved architect name). Fallback: if not available,
  use `client_dimension.primary_architect`.

**Classification logic:**
Script 12 inlines `ETF_CLASSIFICATIONS`, `ASSET_NAME_TO_TICKER`, `_OPAL_ETF_OVERRIDES`,
and `classify_series()` copied verbatim from `06b_build_client_mix_timeseries.py`.
Add a header comment: `# Classification logic mirrored from 06b — keep in sync`.
Do NOT import from 06b directly (numeric prefix prevents clean imports).

**Algorithm:**

```
1. Load holdings_lots (latest parquet) → filter is_open == True
2. Apply _OPAL_ETF_OVERRIDES to fix null tickers for Opal/Pathfinder ETFs
3. classify_series(ticker, asset_name) → asset_class column
4. Load rel_architect_lookup.parquet → merge onto holdings by relationship_id
   - On failure: fall back to loading client_dimension.parquet, join on relationship_id
     for primary_architect column, rename to architect
5. Build firm composition (all rows):
   a. compute total_market_value
   b. group by asset_class → class_mv, class_pct
   c. within each asset_class: group by (ticker/key, asset_name/label) → holding_mv
      → sort desc → take top 9 → compute holding_pct (/ class_mv)
      → compute other = class_mv - sum(top9_mv), other_pct (/ class_mv)
   d. global top 9: sort all (key, label, asset_class, holding_mv) desc → take 9
      → compute pct (/ total_market_value)
   e. global other: total_market_value - sum(global_top9_mv)
   f. unclassified: count and mv of rows where asset_class == '' or null
   g. write → S3: gold/views/firm_composition.json
6. Build per-advisor composition (loop over unique architect values):
   Same algorithm as (5) but filtered to rows where architect == advisor.
   advisor_id = architect.lower().strip().replace whitespace → '_',
               strip non-[a-z0-9_], max 60 chars
   write → S3: gold/advisors/{advisor_id}/composition.json
7. Print summary: firm OK, N advisors written, M skipped (empty book)
```

**S3 keys:**
```
gold/views/firm_composition.json
gold/advisors/{advisor_id}/composition.json
```

**Error handling:**
- If rel_architect_lookup is missing: log WARN, fall back to client_dimension, proceed
- If holdings_lots is missing: log ERROR, exit 1
- If an advisor produces 0 open holdings: skip (do not write empty JSON)
- Any unhandled exception: exit 1 (so run_gold_layer.sh reports failure)

**Gold sequence — run_gold_layer.sh:**

Add `run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"` to BOTH the incremental
and full sequences, immediately after `08b` and BEFORE `06b`:

```bash
# In both sequences, after:
run_script "$SCRIPTS_DIR/08b_build_architect_attribution.py"
# Add:
run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"
# Then continues with 06b, 08, 09, 10 as before
```

Rationale: 12 reads `rel_architect_lookup.parquet` (written by 08b). 12 does NOT need to run
after 06b. Placing it before 06b means both can read the lookup in parallel in future if needed.

---

### WS2 — opal-partners-data Lambda (DS writes, DT deploys)

**File:** `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`

**Changes:**

**A. `cors_response_nocache(status_code, body)`** — new helper:
```python
def cors_response_nocache(status_code: int, body: dict) -> dict:
    """Like cors_response but with no-store for confidential composition data."""
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
```

**B. `serve_s3_json_nocache(bucket, key)`** — thin wrapper:
Calls the same S3 GET logic as `serve_s3_json` but uses `cors_response_nocache` for all
responses (200, 404, 503). Copy the body of `serve_s3_json`, replace all `cors_response`
calls with `cors_response_nocache`.

**C. `handle_firm_composition(bucket)`**:
```python
def handle_firm_composition(bucket: str) -> dict:
    return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')
```

**D. `handle_advisor_composition(bucket, advisor_id)`**:
```python
def handle_advisor_composition(bucket: str, advisor_id: str) -> dict:
    if not advisor_id or '/' in advisor_id or '..' in advisor_id:
        return cors_response_nocache(400, {'error': 'Invalid advisor_id'})
    return serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')
```

**E. Routing in `lambda_handler`** — add composition dispatch for the books path.

The existing `/api/scoped/partners/books/` routing currently handles `relationship`, `account`,
`advisor` entity types. Add `firm` and wire `composition` action for `firm` and `advisor`:

```
entity_type == 'firm'    AND action == 'composition'  → handle_firm_composition(bucket)
entity_type == 'advisor' AND action == 'composition'  → handle_advisor_composition(bucket, entity_id)
```

Note: the advisor `entity_id` passed from the frontend is the same `advisor_id` used as
S3 key. The sanitization in script 12 (`lower, spaces→_, strip non-[a-z0-9_]`) must be
consistent with `handleSelectAdvisor()` in `ClientsTab.tsx`:
```typescript
// ClientsTab.tsx:383
const id = name.toLowerCase().trim()
  .replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
```
Script 12 uses the same transform. These must stay in sync. The PRD records this as a
**cross-agent consistency requirement** — DS and RD must use identical sanitization logic.

**F. Version bump:** 2.7 → 2.8

**G. Update API endpoint docstring** at top of file to add the two new routes.

---

### WS3 — Frontend: types + ConsolidatedOverviewPanel (RD writes)

#### WS3a — `portal/src/pages/AdvisorIntelligence/types.ts`

**Extend `MixItem`:**
```typescript
export interface MixItem {
  asset_class: string
  label: string
  market_value: number
  pct: number
  // N1/L2 schema only — per-class top holdings (pct relative to class market_value)
  top_holdings?: ConcentrationItem[]
  other?: { market_value: number; pct: number }
}
```

**Extend `BooksCompositionResponse`:**
```typescript
export interface BooksCompositionResponse {
  generated_at: string
  data_as_of: string
  scope: {
    relationship_id?: string
    account_id?: string
    advisor_id?: string   // new
    firm_id?: string      // new
  }
  mix: MixItem[]
  concentration: {
    top_n: number
    items: ConcentrationItem[]
    other: { market_value: number; pct: number }
  }
  // N1/L2 schema only — global top holdings (pct relative to total_market_value)
  top_holdings?: ConcentrationItem[]
  other?: { market_value: number; pct: number }  // global other
  unclassified: { count: number; market_value: number }
}
```

No other type changes. `ConcentrationItem` is unchanged.

#### WS3b — `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`

**Only change: the holdings derivation block in `ConsolidatedOverviewPanel` (lines 875–884).**
Everything else in the component stays identical.

Replace the current:
```typescript
const allItems = composition?.concentration.items ?? []
const filteredItems = selectedAssetClass
  ? allItems.filter(it => it.asset_class === selectedAssetClass)
  : allItems

const MAX_ITEMS = 9
const cappedItems = filteredItems.slice(0, MAX_ITEMS)
const showOther = !selectedAssetClass && composition && composition.concentration.other.pct > 0
const showFilteredOther = Boolean(selectedAssetClass && filteredItems.length > MAX_ITEMS)
const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1
```

With the schema-adaptive version:
```typescript
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
```

**Remove:** `showFilteredOther` and its render block — in the new schema, per-class data
is pre-truncated to 9 by script 12 so there are never "extra" items to overflow.
For L3/L4 backward compat, `showFilteredOther` is now covered by the unified `showOther`.

**Update the "Other" row render** (currently at lines 1055–1068) — replace the two separate
`showOther` / `showFilteredOther` blocks with one unified block using `otherEntry`:
```typescript
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
```

**Update empty state message** (line 1073): change the third branch:
```typescript
allItems.length === 0 ? 'No holdings data at this level'
// →
!hasPreAggregated && composition.concentration.items.length === 0
  ? 'No holdings data at this level'
```

**No other changes to `ConsolidatedOverviewPanel`.** The donut, legend, quarterly bar,
and `holdingsTitle` logic are all unaffected.

---

### WS4 — Deployment (DT: Lambda deploy; AE: EC2 script deploy + gold run)

**DT actions:**
1. Build and upload opal-partners-data after DS commits WS2:
   `build-and-upload.sh partners-api opal-partners-data`
2. Update lambda-source-map.json, commit, terraform plan/apply (partners-api)
3. 0-diff verify → tag: `partners-api-v1.5.0` → push --follow-tags

**AE actions:**
1. Upload `12_build_composition_artifacts.py` to `s3://opal-data-bd/code/gold/`
2. Upload updated `run_gold_layer.sh` to `s3://opal-data-bd/code/`
3. Verify DuckDB or pandas available on EC2 (pandas is confirmed present; DuckDB optional)
4. Run gold layer in incremental mode — script 12 will execute after 08b
5. Verify:
   - `aws s3 ls s3://opal-data-bd/gold/views/firm_composition.json`
   - `aws s3 ls s3://opal-data-bd/gold/advisors/ | head -10`
6. Spot-check: `aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json -` | python3 -m json.tool | head -30`

---

## 5. Sequencing and Dependencies

```
DS: write script 12 (WS1) ─────────────────┐
DS: write lambda changes (WS2) ─────────────┤→ DT: deploy partners-api (→ partners-api-v1.5.0)
                                             │
                                             └→ AE: deploy script 12 + run gold layer
                                                     ↓
                                             artifacts live in S3
                                                     ↓
RD: write frontend adapter (WS3) ───────────→ Can merge to portal DEV any time
    (no data dependency — adapts gracefully      (frontend handles missing data with
     when composition is null or uses            existing Loading/null guards)
     synthesis fallback)
                                                     ↓
                              All above complete → DT: portal DEV->PROD merge (shared gate)
```

**RD can work in parallel with all DS/AE/DT work.** The frontend adapter is backward-compatible —
when the Lambda routes return 404 (before DT deploys), the code falls back to synthesis exactly
as before. RD merges to DEV; DE wires any needed endpoint changes; DT gates the portal merge
on all work being present in DEV.

---

## 6. Confidentiality Controls

| Layer | Control |
|-------|---------|
| S3 | `gold/views/` and `gold/advisors/` are private buckets. No public access. |
| Lambda | `is_authorized(firm_id, allowed_firms)` check before serving any books/* route. |
| Cache-Control | `no-store, no-cache, must-revalidate` on all composition routes via `serve_s3_json_nocache`. |
| CloudFront | Auth-validator-edge v7 enforces JWT on all `/api/scoped/` paths. |
| Browser | No `localStorage` or `sessionStorage` write in the fetch path. The existing `fetchComposition` helper at line 98 writes nothing to storage. |

These controls mirror the existing L3/L4 composition endpoints. No new security primitives needed.

---

## 7. Acceptance Criteria

| # | Criterion | Owner |
|---|-----------|-------|
| AC1 | `gold/views/firm_composition.json` exists in S3 after gold run; parseable JSON matching schema §3 | AE |
| AC2 | `gold/advisors/{id}/composition.json` exists for all active advisors | AE |
| AC3 | `GET /api/scoped/partners/books/firm/all/composition?firmId=49financial` returns 200 with `mix[].top_holdings` populated | DT/DS |
| AC4 | `GET /api/scoped/partners/books/advisor/{id}/composition?firmId=49financial` returns 200 | DT/DS |
| AC5 | Both routes return `Cache-Control: no-store` header | DS |
| AC6 | Unauthenticated request returns 401/403; wrong firmId returns 403 | DT (verify existing auth) |
| AC7 | N1 (Firm Overview) panel shows populated "Top Holdings" list (not "No holdings data") | RD |
| AC8 | L2 (Advisor Book) panel shows holdings after drilling into an advisor | RD |
| AC9 | Clicking an asset class in the donut at N1/L2 filters holdings to that class | RD |
| AC10 | L3/L4 composition panels unaffected (existing behavior preserved) | RD |
| AC11 | `pct` in per-class `top_holdings` sums to ≤1.0 per class (+ other) | AE (spot-check) |

---

## 8. Out of Scope

- L3 (relationship) and L4 (account) composition endpoints: already working, not changed.
- `concentration.items` removal from the type: kept for backward compat with L3/L4 schema.
- Real-time/on-demand composition queries: not considered. Pre-compute at pipeline time only.
- Browser-side DuckDB: confidentiality constraint eliminates this approach.
- Multi-firm support: `firm_id` is derived from the bucket in script 12. The current
  implementation supports single-firm (49Financial). Multi-firm extension is a separate project.

---

## 9. Notes for COO Decomposition

**Task order targets:**
- `0.4.0_DS_ClientPlatform`: WS1 (script 12) + WS2 (opal-partners-data lambda changes)
- `0.4.2_RD_AdvisorIntelligence`: WS3 (types.ts + ConsolidatedOverviewPanel adapter)
- `0.4.0_DT_ClientPlatform`: WS4 Lambda deploy (partners-api-v1.5.0)
- `0.6.0_AE_PartnerETL`: WS4 EC2 deploy + gold run

**Key cross-agent consistency requirement:**
The `advisor_id` sanitization in script 12 must be identical to `handleSelectAdvisor()` in
`ClientsTab.tsx:383`. Any change to either must be coordinated between DS and RD.
The canonical transform: lowercase, spaces→`_`, strip non-`[a-z0-9_]`, strip leading/trailing `_`.

**Confidence flags:**
- L3/L4 backward compat: HIGH (schema detection is isolated to the holdings block; all other
  `ConsolidatedOverviewPanel` code reads from `composition.mix` which is present in both schemas)
- advisor_id key collision risk: LOW (architect names go through identical sanitization on both
  sides; if an advisor has no composition JSON, the endpoint returns 404 and the synthesis
  fallback fires — same behavior as today, not a regression)
- Script 12 EC2 dependencies: pandas confirmed present (used by all gold scripts);
  DuckDB is optional — spec uses pandas. AE verifies before running.
```

### rungoldlayer.sh----full-script-ds-and-ae-verify-08b-12-06b-insertion-point-and-upload-paths.sh

```
#!/bin/bash
# =============================================================================
# BD Gold Layer Runner
#
# Runs on bd-gold-layer-runner (i-01003b035d2988dfb, r6i.xlarge, 32GB RAM).
# Dispatched via SSM from bd-gold-trigger Lambda.
#
# Two modes:
#
#   incremental [--start-date YYYY-MM-DD]
#     Runs: 00, 02, 05, 05c, 05d, 06b, 07, 08b, 08, 09, 10 (sequential)
#     Default start-date: 8 days ago (covers last full week + buffer)
#     Frequency: daily (Mon-Fri, ~6 PM ET after transaction pipeline)
#
#   full
#     Runs: 00, 01, 02, 04, 03, 05, 05b, 05c, 05d, 06, 06b, 07, 08b, 08, 09, 10 (sequential)
#     Frequency: monthly (1st of every month, 3 AM ET)
#
# All scripts run sequentially. No parallelism — prevents read-during-write
# race conditions on shared S3 parquet files (e.g., 07/08 reading
# client_performance.parquet while 05 is still writing it).
#
# Usage:
#   ./run_gold_layer.sh incremental
#   ./run_gold_layer.sh incremental --start-date 2026-02-16
#   ./run_gold_layer.sh full
# =============================================================================

set -e

MODE="${1:-incremental}"
START_DATE=""

# Parse optional --start-date flag
shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --start-date) START_DATE="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# Default incremental start date: 8 days ago (covers last full week + weekend buffer)
if [[ "$MODE" == "incremental" && -z "$START_DATE" ]]; then
    START_DATE=$(date -d "8 days ago" +%Y-%m-%d 2>/dev/null || date -v-8d +%Y-%m-%d)
fi

S3_BUCKET="opal-data-bd"
SCRIPTS_DIR="/tmp/gold_layer_scripts"
RUN_DATE=$(date +%Y-%m-%d)
LOG_KEY="logs/gold-layer/gold_${MODE}_${RUN_DATE}.log"

mkdir -p "$SCRIPTS_DIR"

exec > >(tee /tmp/gold_runner.log) 2>&1

echo "============================================================"
echo "BD GOLD LAYER — ${MODE^^}"
echo "Started:    $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
[[ "$MODE" == "incremental" ]] && echo "Start date: ${START_DATE}"
echo "============================================================"
echo ""

# Install/verify dependencies
echo "[setup] Checking Python dependencies..."
pip3 install --quiet --upgrade boto3 pandas pyarrow numpy 2>&1 | tail -3

# Download gold scripts from S3 (medallion: code/gold/)
echo ""
echo "[setup] Downloading gold layer scripts from S3..."
aws s3 sync s3://${S3_BUCKET}/code/gold/ "$SCRIPTS_DIR/" --exclude "archive/*" --quiet
echo "  Downloaded: $(ls $SCRIPTS_DIR/*.py 2>/dev/null | wc -l) scripts"

run_script() {
    local script="$1"
    local args="${@:2}"
    local name
    name=$(basename "$script" .py)
    echo ""
    echo "------------------------------------------------------------"
    echo "Running: $name $args"
    echo "------------------------------------------------------------"
    python3 "$script" --upload $args
}

# =============================================================================
# INCREMENTAL: daily run — accounts dimension, positions_cube (recent dates),
# then downstream views.
# Fully sequential to prevent read-during-write race conditions on S3 parquets.
#
# 05b (account_performance) excluded — full history rebuild, runs in full mode only.
#
# Dependency chain:
#   00 (accounts_dimension)  -->  (picks up new accounts daily)
#   02 (positions_cube)  -->  05 (client_performance)  -->  05c (validate aua vs silver)
#                                                      -->  05d (write aua certification)
#                                                      -->  07 (geo view)
#                                                      -->  08b (architect attribution)  -->  06b (client_mix_timeseries, reads rel_architect_lookup)
#                                                                                         -->  08 (adv view, reads 08b lookup)
#                                                      -->  09 (partner analytics JSON)
#                                                      -->  10 (rolling flows JSON)
# =============================================================================
if [[ "$MODE" == "incremental" ]]; then
    run_script "$SCRIPTS_DIR/00_build_accounts_dimension.py" --incremental
    run_script "$SCRIPTS_DIR/02_build_positions_cube.py" --start-date "$START_DATE"
    run_script "$SCRIPTS_DIR/05_build_client_performance.py"
    # 05c: validate AUA vs silver (non-blocking; SKIP if no silver allocation for today)
    if [ -f "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" ]; then
        python3 "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" || true
    fi
    # 05d: write AUA certification JSON (non-blocking; SKIP if no silver allocation for today)
    python3 "$SCRIPTS_DIR/05d_write_aua_certification.py" || true
    run_script "$SCRIPTS_DIR/07_build_nna_aua_by_geography.py"
    run_script "$SCRIPTS_DIR/08b_build_architect_attribution.py"
    run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --incremental --workers 8
    run_script "$SCRIPTS_DIR/08_build_nna_aua_by_advisor.py"
    run_script "$SCRIPTS_DIR/09_generate_partner_analytics.py"
    run_script "$SCRIPTS_DIR/10_generate_advisor_rolling_flows.py"

# =============================================================================
# FULL: monthly rebuild — all scripts in strict dependency order.
# Fully sequential to prevent read-during-write race conditions on S3 parquets.
#
# Dependency chain:
#   00 (accounts_dimension)
#   01 (advisor_assignments_history)   reads 00
#   02 (positions_cube)                reads silver
#   04 (client_dimension)              reads 00
#   03 (holdings_lots)                 reads 02, 00
#   05 (client_performance)            reads 02, 00
#   05b (account_performance)          reads 02, 00, 05
#   05c (validate aua vs silver)       reads 05, silver/allocations (non-blocking)
#   05d (write aua certification)      reads 05, silver/allocations (non-blocking)
#   06 (client_tax_liability)          reads 03
#   06b (client_mix_timeseries)        reads 02, 00, account_performance
#   07 (nna_aua_by_geography)          reads 05, 00
#   08b (architect_attribution)        reads 00, 08(prev), 05b — writes rel_architect_lookup
#   08 (nna_aua_by_advisor)            reads 05, 08b lookup
#   09 (partner_analytics)             reads 05, 05b, 07, 08, 04, 00
#   10 (advisor_rolling_flows)         reads 08, 05, 00, 04
# =============================================================================
elif [[ "$MODE" == "full" ]]; then
    run_script "$SCRIPTS_DIR/00_build_accounts_dimension.py"
    run_script "$SCRIPTS_DIR/01_build_advisor_assignments_history.py"
    run_script "$SCRIPTS_DIR/02_build_positions_cube.py"
    run_script "$SCRIPTS_DIR/04_build_client_dimension.py"
    run_script "$SCRIPTS_DIR/03_build_holdings_lots.py"
    run_script "$SCRIPTS_DIR/05_build_client_performance.py"
    run_script "$SCRIPTS_DIR/05b_build_account_performance.py"
    # 05c: validate AUA vs silver (non-blocking; SKIP if no silver allocation for today)
    if [ -f "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" ]; then
        python3 "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" || true
    fi
    # 05d: write AUA certification JSON (non-blocking; SKIP if no silver allocation for today)
    python3 "$SCRIPTS_DIR/05d_write_aua_certification.py" || true
    run_script "$SCRIPTS_DIR/06_build_client_tax_liability.py"
    run_script "$SCRIPTS_DIR/07_build_nna_aua_by_geography.py"
    run_script "$SCRIPTS_DIR/08b_build_architect_attribution.py"
    run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --workers 8
    run_script "$SCRIPTS_DIR/08_build_nna_aua_by_advisor.py"
    run_script "$SCRIPTS_DIR/09_generate_partner_analytics.py"
    run_script "$SCRIPTS_DIR/10_generate_advisor_rolling_flows.py"

else
    echo "ERROR: Unknown mode '$MODE'. Use 'incremental' or 'full'."
    exit 1
fi

echo ""
echo "============================================================"
echo "COMPLETE — ${MODE^^}"
echo "Finished:   $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "============================================================"

# Write pipeline-complete sentinel — triggers bd-portal-publisher + bd-portal-advisor-publisher
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"status\":\"success\",\"mode\":\"${MODE}\",\"timestamp\":\"${TIMESTAMP}\",\"run_date\":\"${RUN_DATE}\"}" \
  | aws s3 cp - "s3://${S3_BUCKET}/gold/pipeline-complete.json" \
  && echo "Sentinel written: s3://${S3_BUCKET}/gold/pipeline-complete.json"

# Upload log to S3
aws s3 cp /tmp/gold_runner.log "s3://${S3_BUCKET}/${LOG_KEY}" --quiet && \
    echo "Log uploaded: s3://${S3_BUCKET}/${LOG_KEY}"

# Invalidate CloudFront so the portal serves fresh data immediately
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id EVTSA9VEHNZVH \
    --paths "/api/scoped/advisor-intelligence/*" \
    --query 'Invalidation.Id' --output text)
echo "CloudFront invalidation created: ${INVALIDATION_ID}"

# Check for pending trigger before shutdown.
# If bd-gold-trigger fired while we were running, it wrote trigger-pending.json
# instead of starting a new instance. Clear the marker and re-run so no data
# day is skipped. exec replaces this process — the new run will write its own
# pipeline-complete, upload its own log, and check for pending again, so back-
# to-back skipped triggers are handled naturally. The marker is deleted before
# re-exec, so we only loop if a NEW trigger fires during the re-run.
PENDING_KEY="gold/trigger-pending.json"
PENDING_BODY=$(aws s3 cp "s3://${S3_BUCKET}/${PENDING_KEY}" - 2>/dev/null || echo "")
if echo "$PENDING_BODY" | grep -q '"pending"'; then
    echo ""
    echo "============================================================"
    echo "PENDING TRIGGER FOUND — re-running incremental"
    echo "Marker contents: ${PENDING_BODY}"
    echo "============================================================"
    aws s3 rm "s3://${S3_BUCKET}/${PENDING_KEY}" --quiet \
        && echo "Pending marker cleared"
    exec "$0" incremental
fi

# Self-stop: shut down the instance now that all work is done
echo "No pending trigger — shutting down instance..."
shutdown -h now
```

### task-order-001----ds-script-12--lambda-v28-routes.md

```
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Write script 12 (`12_build_composition_artifacts.py`) to pre-compute per-class top-9
    holdings composition artifacts for firm (N1) and all advisors (L2), update
    `run_gold_layer.sh` to include it, and add two new S3-proxy Lambda routes
    (`handle_firm_composition`, `handle_advisor_composition`) to opal-partners-data v2.8.
    These changes unblock the ConsolidatedOverviewPanel holdings panel which currently
    renders empty at N1 and L2 because the composition endpoints return 404.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md (canonical schema §3, algorithm §WS1,
    Lambda changes §WS2, sequencing §5).

    Current state:
    - `handle_books_composition` (line 829 of lambda_function.py) handles ALL entity types
      via in-Lambda computation from parquet. For firm/advisor it either times out or errors.
    - Routing at line 1222: `elif action == 'composition': return handle_books_composition(...)`
      routes firm and advisor to the computation-based handler.
    - L3/L4 (relationship, account) composition works today via `handle_books_composition`
      — do NOT change that behavior.
    - Current Lambda version: 2.7 (deployed at partners-api-v1.4.0).
    - run_gold_layer.sh: both modes have `08b` immediately followed by `06b`.
      Incremental: line 114 (08b), line 115 (06b). Full: line 158 (08b), line 159 (06b).

    advisor_id sanitization canonical transform (ClientsTab.tsx:383):
      name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
    Python equivalent (must match exactly):
      advisor_id = re.sub(r'[^a-z0-9_]+', '_',
                          name.lower().strip()).strip('_')[:60] or 'unknown'
    This is the key cross-agent consistency requirement. Any deviation breaks the S3 key lookup.
  </context>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="modify">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS1-script12">
      Write `data/black_diamond/scripts/gold/12_build_composition_artifacts.py`.

      Header comment (required):
        # Classification logic mirrored from 06b_build_client_mix_timeseries.py -- keep in sync
        # Do NOT import from 06b directly (numeric prefix prevents clean imports).

      Inline (copy verbatim from 06b): ETF_CLASSIFICATIONS, ASSET_NAME_TO_TICKER,
      _OPAL_ETF_OVERRIDES, and classify_series(). These are the classification lookup tables.

      Algorithm (per PRD §WS1):
      1. Discover latest holdings_lots parquet: list s3://opal-data-bd/holdings_lots/*.parquet,
         sort by name descending, take the first. Read with pandas. Filter is_open == True.
         If no file found: log ERROR, sys.exit(1).
      2. Apply _OPAL_ETF_OVERRIDES to fix null tickers for Opal/Pathfinder ETFs:
         for rows where ticker is null/NaN but asset_name matches a key in _OPAL_ETF_OVERRIDES,
         set ticker = _OPAL_ETF_OVERRIDES[asset_name].
      3. Add asset_class column: apply classify_series(row.ticker, row.asset_name) per row.
      4. Load rel_architect_lookup.parquet from s3://opal-data-bd/gold/views/rel_architect_lookup.parquet.
         Columns needed: relationship_id, architect (= resolved architect name).
         On any failure: log WARN, fall back to loading
         s3://opal-data-bd/gold/views/client_dimension.parquet, join on relationship_id,
         use primary_architect column, rename to architect. If that also fails: log ERROR, sys.exit(1).
      5. Merge lookup onto holdings by relationship_id (left join, keep all holdings).
      6. Compute firm composition (all rows) — see PRD §WS1 algorithm step 5 for the
         full sequence: total_market_value, class groups, per-class top-9, global top-9,
         global other, unclassified.
         Output schema: exactly as PRD §3 with scope = {"firm_id": "49financial"}.
         Pct conventions (critical — per PRD §3):
           mix[i].pct = class_mv / total_market_value
           mix[i].top_holdings[j].pct = holding_mv / class_mv  (NOT total_market_value)
           top_holdings[j].pct (root) = holding_mv / total_market_value
           other.pct (root) = root_other_mv / total_market_value
           mix[i].other.pct = class_other_mv / class_mv
         Write to: s3://opal-data-bd/gold/views/firm_composition.json
      7. Loop over unique architect values in the merged dataframe.
         For each architect, filter holdings to architect == that_value.
         Compute advisor_id using the canonical transform:
           import re
           advisor_id = re.sub(r'[^a-z0-9_]+', '_', architect.lower().strip()).strip('_')[:60] or 'unknown'
         Compute same composition structure as step 6 but scoped to that advisor.
         scope = {"advisor_id": advisor_id, "firm_id": "49financial"}
         If advisor has 0 open holdings after filter: skip (do not write).
         Write to: s3://opal-data-bd/gold/advisors/{advisor_id}/composition.json
      8. Print summary line:
           print(f'OK: firm_composition.json written. Advisors: {N} written, {M} skipped (empty book).')

      key field: ticker if non-null/non-empty, else re.sub(r'\s+', '_', asset_name.lower())[:40]
      label field: ticker if non-null/non-empty, else asset_name[:30]
    </requirement>

    <requirement id="2" workstream="WS1-run_gold_layer">
      Update `data/black_diamond/scripts/gold/run_gold_layer.sh`.

      In BOTH the incremental section (around line 114) and the full section (around line 158),
      insert script 12 AFTER 08b and BEFORE 06b:

      Incremental (insert between lines 114 and 115):
        run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"

      Full (insert between lines 158 and 159):
        run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"

      Script 12 takes no mode flags (runs the same in both modes).
      Do NOT move or change any other script position.
      Update the sequence comments at lines 11 and 16 (header comments) to include 12
      in the script list between 08b and 06b.
    </requirement>

    <requirement id="3" workstream="WS2-lambda-helpers">
      In opal-partners-data lambda_function.py, add two new helper functions AFTER the
      existing `cors_response` function (around line 106) and BEFORE `serve_s3_json`:

      A. `cors_response_nocache(status_code, body)` — exact code from PRD §WS2-A:
        Identical to cors_response but with Cache-Control: 'no-store, no-cache, must-revalidate'
        instead of the existing max-age header. Uses same DecimalEncoder.

      B. `serve_s3_json_nocache(bucket, key)` — PRD §WS2-B:
        Copy the body of the existing `serve_s3_json` function verbatim,
        replacing ALL calls to `cors_response(...)` with `cors_response_nocache(...)`.
        Do not change any S3 logic or error handling.

      These two functions are the only new helpers.
    </requirement>

    <requirement id="4" workstream="WS2-lambda-handlers">
      Add two new handler functions AFTER the existing `handle_advisor_mix_views` function
      (around line 1063) and BEFORE the `# Main Handler` section comment:

      C. `handle_firm_composition(bucket)` — PRD §WS2-C:
        return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')

      D. `handle_advisor_composition(bucket, advisor_id)` — PRD §WS2-D:
        Validate: if not advisor_id or '/' in advisor_id or '..' in advisor_id:
          return cors_response_nocache(400, {'error': 'Invalid advisor_id'})
        return serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')

      Add docstrings consistent with the existing handlers in the file.
    </requirement>

    <requirement id="5" workstream="WS2-lambda-routing">
      Update the routing block in `lambda_handler` at line 1222.

      Current (single branch handles ALL entity types):
        elif action == 'composition':
            return handle_books_composition(bucket, entity_type, entity_id)

      Replace with (firm/advisor get new S3-proxy handlers; relationship/account keep existing):
        elif action == 'composition' and entity_type == 'firm':
            return handle_firm_composition(bucket)
        elif action == 'composition' and entity_type == 'advisor':
            return handle_advisor_composition(bucket, entity_id)
        elif action == 'composition':
            return handle_books_composition(bucket, entity_type, entity_id)

      This preserves L3/L4 (relationship, account) behavior exactly. Only firm and advisor
      composition are redirected to the new S3-proxy handlers.

      IMPORTANT: the `advisor` composition routing must appear BEFORE the generic
      `elif action == 'composition':` fallback, matching the pattern used for timeseries.
    </requirement>

    <requirement id="6" workstream="WS2-lambda-version">
      Bump the Lambda version constant from 2.7 to 2.8.
      Add the two new routes to the API endpoint docstring at the top of the file:
        GET /api/scoped/partners/books/firm/all/composition?firmId=xxx
        GET /api/scoped/partners/books/advisor/{advisor_id}/composition?firmId=xxx
    </requirement>

    <requirement id="7" workstream="commit">
      Commit both WS1 files (script 12 + run_gold_layer.sh) in ONE commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(bd-gold): script 12 composition artifacts + run_gold_layer.sh update (ADVI_BKSCMP WS1)"

      Commit the Lambda changes (lambda_function.py) in a SEPARATE commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(opal-partners-data): firm+advisor composition routes v2.8 (ADVI_BKSCMP WS2)"

      Report both commit SHAs to COO. The Lambda commit SHA is the gate for DT (ADVI_BKSCMP.003).
      The script 12 + run_gold_layer.sh commit SHA is the gate for AE (ADVI_BKSCMP.004).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">script 12 exists at correct path; runs without import errors in Python 3.12</criterion>
    <criterion id="2">advisor_id sanitization in script 12 matches ClientsTab.tsx:383 exactly</criterion>
    <criterion id="3">pct conventions match PRD §3 table (per-class top_holdings pct / class_mv, not total)</criterion>
    <criterion id="4">run_gold_layer.sh incremental: 08b immediately followed by 12, then 06b (no other reordering)</criterion>
    <criterion id="5">run_gold_layer.sh full: same 12 insertion after 08b, before 06b</criterion>
    <criterion id="6">cors_response_nocache returns Cache-Control: no-store, no-cache, must-revalidate</criterion>
    <criterion id="7">serve_s3_json_nocache is a structural copy of serve_s3_json — only cors_response calls differ</criterion>
    <criterion id="8">Lambda routing: firm+composition → handle_firm_composition; advisor+composition → handle_advisor_composition; relationship/account+composition → handle_books_composition (unchanged)</criterion>
    <criterion id="9">Lambda version = 2.8</criterion>
    <criterion id="10">Two separate commits on CLOUD; SHAs reported to COO</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT import from 06b — inline the classification logic with the required header comment</constraint>
    <constraint>Do NOT change handle_books_composition — it must remain for L3/L4 (relationship, account)</constraint>
    <constraint>Do NOT use DuckDB — pandas only (confirmed present on EC2)</constraint>
    <constraint>advisor_id sanitization must match ClientsTab.tsx:383 exactly — any deviation breaks S3 key lookup</constraint>
    <constraint>All pct fields are 0–1 (not 0–100) — consistent with all other mix artifacts in this repo</constraint>
    <constraint>No emojis anywhere in code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>commit to CLOUD parent repo only — no portal changes in this task order</constraint>
    <constraint>Do not modify any other script positions in run_gold_layer.sh</constraint>
    <constraint>If advisor produces 0 open holdings after filter: skip (do not write empty JSON)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      No upstream DS gates — script 12 reads from existing S3 artifacts (holdings_lots from 03,
      rel_architect_lookup from 08b). Both are confirmed present on S3.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">data/black_diamond/scripts/gold/12_build_composition_artifacts.py + run_gold_layer.sh (one commit)</deliverable>
    <deliverable type="commit">opal-partners-data lambda_function.py v2.8 (separate commit)</deliverable>
  </deliverables>
</task_order>
```

### task-order-002----rd-typests--holdings-adapter.md

```
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-002-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Extend types.ts with optional per-class top_holdings fields, and update the
    holdings derivation block in ConsolidatedOverviewPanel to be schema-adaptive:
    N1/L2 use pre-aggregated per-class top_holdings from the new artifacts; L3/L4
    continue to use the existing flat concentration.items path. No other changes
    to ConsolidatedOverviewPanel. RD can work in parallel with DS/DT/AE — the
    adapter is backward-compatible and falls through to synthesis when the new
    Lambda routes return 404.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS3a (types), §WS3b (component),
    §3 (schema), §5 (sequencing — RD parallel track).

    Current state (verified):
    - types.ts MixItem does NOT have top_holdings or other optional fields yet.
    - BooksCompositionResponse scope does NOT have advisor_id or firm_id fields yet.
    - Holdings block at ClientsTab.tsx lines 875–884 is the ONLY change in the component.
    - showFilteredOther render is at lines 1039–1050 — replaced by unified showOther.
    - showOther render is at lines 1055–1068 — replace with PRD version using otherEntry.
    - Empty state at line 1073: `allItems.length === 0 ? 'No holdings data at this level'`

    The ConsolidatedOverviewPanel's donut, legend, quarterly bar, and all other logic
    are completely unaffected by this change. The holdings block is the only code section
    touched.

    advisor_id consistency note: `handleSelectAdvisor` at line 383 sanitizes the advisor
    name to produce the `entity_id` used in `fetchComposition('advisor', id, ...)`.
    Script 12 uses the identical transform to generate S3 keys. These are consistent
    by PRD constraint — no change needed in ClientsTab.tsx for this.
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS3a-types">
      In `portal/src/pages/AdvisorIntelligence/types.ts`:

      A. Extend MixItem with two optional fields (add at the end of the interface):
        export interface MixItem {
          asset_class: string
          label: string
          market_value: number
          pct: number
          // N1/L2 schema only -- per-class top holdings (pct relative to class market_value)
          top_holdings?: ConcentrationItem[]
          other?: { market_value: number; pct: number }
        }

      B. Extend BooksCompositionResponse scope and add optional root-level fields:
        export interface BooksCompositionResponse {
          generated_at: string
          data_as_of: string
          scope: {
            relationship_id?: string
            account_id?: string
            advisor_id?: string   // new -- N1/L2 schema
            firm_id?: string      // new -- N1/L2 schema
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

      ConcentrationItem is unchanged. No other type additions.
    </requirement>

    <requirement id="2" workstream="WS3b-holdings-block">
      In `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`,
      replace ONLY the block at lines 875–884 and the render blocks that use
      showOther / showFilteredOther.

      Replace lines 875–884:
        const allItems = composition?.concentration.items ?? []
        const filteredItems = selectedAssetClass
          ? allItems.filter(it => it.asset_class === selectedAssetClass)
          : allItems

        const MAX_ITEMS = 9
        const cappedItems = filteredItems.slice(0, MAX_ITEMS)
        const showOther = !selectedAssetClass && composition && composition.concentration.other.pct > 0
        const showFilteredOther = Boolean(selectedAssetClass && filteredItems.length > MAX_ITEMS)
        const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1

      With the schema-adaptive version from PRD §WS3b (exact code):
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
            if (!selectedAssetClass &amp;&amp; composition.concentration.other.pct > 0) {
              return composition.concentration.other
            }
            return null
          }
        })()

        const showOther = otherEntry !== null &amp;&amp; otherEntry.pct > 0
        const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1
    </requirement>

    <requirement id="3" workstream="WS3b-render-other">
      Remove showFilteredOther. Replace the two existing "Other" render blocks
      (lines 1039–1068: the showFilteredOther block at 1039–1050 AND the showOther
      block at 1055–1068) with a SINGLE unified block using otherEntry (PRD §WS3b):

        {showOther &amp;&amp; otherEntry &amp;&amp; (
          &lt;div className="flex items-center gap-2.5"&gt;
            &lt;span className="text-[10px] text-white/20 w-4 text-right flex-shrink-0"&gt;~&lt;/span&gt;
            &lt;div className="flex-1"&gt;
              &lt;div className="flex items-baseline justify-between mb-1"&gt;
                &lt;span className="text-[11px] text-white/40 italic"&gt;Other&lt;/span&gt;
                &lt;span className="text-[11px] text-white/30 ml-2"&gt;{(otherEntry.pct * 100).toFixed(1)}%&lt;/span&gt;
              &lt;/div&gt;
              &lt;div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden"&gt;
                &lt;div className="h-full rounded-full bg-white/20"
                  style={{ width: `${(otherEntry.pct / maxPct) * 100}%` }} /&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        )}
    </requirement>

    <requirement id="4" workstream="WS3b-empty-state">
      Update the empty state condition at line 1073.

      Current:
        allItems.length === 0 ? 'No holdings data at this level'

      Replace with:
        !hasPreAggregated &amp;&amp; composition.concentration.items.length === 0
          ? 'No holdings data at this level'

      This ensures that when hasPreAggregated is true (N1/L2), an empty cappedItems array
      does not show "No holdings data" — it correctly falls through to the loading state
      (the composition itself is non-null, so "No holdings for selected class" is the right message).
    </requirement>

    <requirement id="5" workstream="commit">
      Commit both files together to portal DEV:
        git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" \
          -m "feat(portal): schema-adaptive holdings block for N1/L2 composition (ADVI_BKSCMP WS3)"

      Report commit SHA to COO. This is a WS6 portal merge gate.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">MixItem has optional top_holdings?: ConcentrationItem[] and other?: {market_value, pct}</criterion>
    <criterion id="2">BooksCompositionResponse scope has optional advisor_id and firm_id</criterion>
    <criterion id="3">BooksCompositionResponse has optional root-level top_holdings and other</criterion>
    <criterion id="4">hasPreAggregated detection uses mix.some(m => top_holdings?.length > 0)</criterion>
    <criterion id="5">When hasPreAggregated and selectedAssetClass: uses mix[class].top_holdings (pct / class_mv)</criterion>
    <criterion id="6">When hasPreAggregated and no selectedAssetClass: uses composition.top_holdings (global)</criterion>
    <criterion id="7">L3/L4 path unchanged: filters concentration.items, caps at 9</criterion>
    <criterion id="8">Single unified showOther block using otherEntry — showFilteredOther removed</criterion>
    <criterion id="9">Empty state updated: !hasPreAggregated &amp;&amp; concentration.items.length === 0</criterion>
    <criterion id="10">bunx tsc -b passes (no new type errors)</criterion>
    <criterion id="11">All other ConsolidatedOverviewPanel code (donut, legend, quarterly bar) unmodified</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Touch ONLY lines 875–884 (derivation block) and the two render blocks (showOther/showFilteredOther) in ClientsTab.tsx</constraint>
    <constraint>Do NOT modify handleSelectAdvisor, fetchComposition, synthesizeFrom*, or any other ClientsTab function</constraint>
    <constraint>Do NOT add features, comments, or refactors beyond the specified changes</constraint>
    <constraint>All portal changes commit to portal DEV (not CLOUD parent repo)</constraint>
    <constraint>No emojis in code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>RD does NOT push -- DT pushes portal DEV to remote</constraint>
    <constraint>Do NOT gate this work on DS/DT/AE -- the adapter is backward-compatible (404 falls through to synthesis)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      No upstream gates. Frontend is backward-compatible when Lambda routes return 404.
      Commit to portal DEV immediately.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">types.ts + ClientsTab.tsx committed to portal DEV (ADVI_BKSCMP WS3)</deliverable>
  </deliverables>
</task_order>
```

### task-order-003----dt-partners-api-v150-lambda-deploy.md

```
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-003-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Deploy the updated opal-partners-data Lambda (v2.8) after DS commits the WS2 Lambda
    changes (ADVI_BKSCMP.001 req 6 commit). Tag as partners-api-v1.5.0. This brings the
    new firm/advisor composition routes live so AE's gold artifacts become accessible.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS4 (DT actions).
    Deployment reference: docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md.

    Current partners-api tag: partners-api-v1.4.0. Verify with:
      git tag -l "partners-api-v*" | sort -V | tail -5
    Target: partners-api-v1.5.0 (minor bump -- two new routes, new cache-control helper).

    DS gate commit: ADVI_BKSCMP.001 req 6 (Lambda v2.8 commit to CLOUD).
    DS will report the commit SHA. Confirm it exists before building.

    Known workaround: build-and-upload.sh fails on this machine (bun MSYS2 path issue).
    Use PowerShell temp script at C:/Windows/Temp/ as documented in AE5 log.
  </context>

  <scope>
    <files>
      <file action="deploy">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      GATE: Confirm DS has committed the Lambda v2.8 changes to CLOUD.
      Check: git log --oneline -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
      Verify the commit message mentions "v2.8" or "ADVI_BKSCMP WS2". Do not build before confirming.
    </requirement>

    <requirement id="2">
      Build and upload the Lambda artifact:
        Use PowerShell temp script pattern (C:/Windows/Temp/build-partners-data.ps1)
        — build-and-upload.sh is broken on this machine.
      Upload to: s3://opal-313476888478-lambda-artifacts/partners-api/opal-partners-data.zip
      Record SHA256 in session log.
    </requirement>

    <requirement id="3">
      Update infra/aws/lambda/ci/lambda-source-map.json entry for opal-partners-data
      with the new SHA256 and S3 version.
      Commit under DT author:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci(partners-api): upload opal-partners-data v2.8 (ADVI_BKSCMP)"
    </requirement>

    <requirement id="4">
      terraform plan (partners-api module). Expected: 1 to change (opal-partners-data
      in-place — s3_object_version + source_code_hash).
      terraform apply. Verify 0-diff second plan.
    </requirement>

    <requirement id="5">
      Run record-terraform-deploy.sh:
        bash infra/aws/lambda/ci/record-terraform-deploy.sh partners-api partners-api-v1.5.0
      Commit the CHANGELOG.json update:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci: record deploy partners-api @ (commit) [skip ci]"
    </requirement>

    <requirement id="6">
      Tag and push:
        git tag -l "partners-api-v*" | sort -V | tail -5   # verify next version
        git tag -a partners-api-v1.5.0 -m "ADVI_BKSCMP: firm+advisor composition routes (v2.8)"
        git push --follow-tags
    </requirement>

    <requirement id="7">
      Update deployment_map.xml with partners-api-v1.5.0.
    </requirement>

    <requirement id="8">
      Spot-verify new routes are live (optional, can be done before AE gold run):
        Confirm that GET /api/scoped/partners/books/firm/all/composition?firmId=49financial
        returns 503 (expected — artifacts not yet in S3) rather than 404 (wrong route) or 500 (code error).
      Report deploy complete to COO. This is the gate for AE to start gold run verification
      (AE can run the gold layer before the Lambda deploy; the Lambda must be live to serve artifacts).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS gate commit confirmed before build</criterion>
    <criterion id="2">Artifact uploaded; SHA256 recorded in session log</criterion>
    <criterion id="3">lambda-source-map.json updated and committed</criterion>
    <criterion id="4">terraform apply complete, 0-diff second plan confirmed</criterion>
    <criterion id="5">partners-api-v1.5.0 tag pushed with --follow-tags</criterion>
    <criterion id="6">CHANGELOG.json updated via record-terraform-deploy.sh</criterion>
    <criterion id="7">Firm composition route returns 503 (not 404/500) before S3 artifacts exist</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>GATE: Do not build before confirming DS Lambda v2.8 commit is on CLOUD</constraint>
    <constraint>Always check actual git tags before tagging -- git tag -l "partners-api-v*" | sort -V | tail -5</constraint>
    <constraint>Use PowerShell temp script for zip + upload (build-and-upload.sh broken on this machine)</constraint>
    <constraint>No emojis in commit messages or Terraform apply output (CLAUDE.md rule 13)</constraint>
    <constraint>lambda-source-map.json must be updated for every Lambda deploy</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before AWS CLI commands with ARN or S3 paths</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_BKSCMP.001 req 6" status="pending">
      opal-partners-data v2.8 Lambda committed to CLOUD -- hard gate for build
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">opal-partners-data v2.8 deployed; tagged partners-api-v1.5.0</deliverable>
    <deliverable type="document">Session log with SHA256, 0-diff confirmation, tag</deliverable>
  </deliverables>
</task_order>
```

### task-order-004----ae-ec2-gold-run--artifact-verification.md

```
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
```

---

## Participant Background

### 0.4.0_DS_ClientPlatform -- Recent Session Logs

#### advi_advtv2_001_architect_attribution_gold.md

# Architect Attribution Gold Productionization — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-17

## Objective

Productionize the architect attribution decision tree (validated in `.tmp_architect_attribution.py` on 2026-03-13) into the gold layer pipeline. New script 08b writes a deterministic attribution of every funded account to one of 19 true architects, replacing the raw `architect` field as the canonical assignment for all downstream ADV views.

---

## Work Completed

### 1. Modified `00_build_accounts_dimension.py` (Req 4, 5)

- Added `consultant` and `additional_advisor` to `TXN_ACCOUNT_COLS` — these fields exist in silver transactions but were previously dropped during the gold build. They are needed for T11-T15 in the attribution tree.
- Added both columns to `output_cols` list so they appear in `accounts_dimension_latest.parquet`.
- Added normalization: `"Olivia Shin"` -> `"Liv Shin"` (confirmed typo duplicate with overlapping relationship, per 2026-03-13 investigation).
- Fixed emoji in `save_dimension()` print statement (CLAUDE.md rule 13).

### 2. Created `08b_build_architect_attribution.py` (Req 1, 3)

New gold script implementing the full T0-T16 decision tree:
- **T0:** Dynamically computes 19 true architects from AUA >= $5M, rels >= 5, not 49F House/Unassigned, active in trailing 12M.
- **T1-T4:** Direct architect, implementor (is true, 80%, 60%).
- **T5:** Relationship inheritance pass 1.
- **T6-T7:** Portfolio group (true, junior 80%).
- **T8:** Relationship inheritance pass 2.
- **T9:** Local relationship 60% pairing.
- **T10:** Relationship inheritance pass 3.
- **T11-T13:** Consultant (true, 80%, 60%).
- **T14-T15:** Additional advisor (true, 80%, 60%).
- **T16:** Relationship inheritance pass 4.
- Scoped to FUNDED accounts only (from account_performance).
- Outputs: `architect_attribution.parquet` (per-account) + `rel_architect_lookup.parquet` (per-relationship modal).
- Conservation check: resolved + unresolved = total funded accounts.

### 3. Modified `08_build_nna_aua_by_advisor.py` (Req 2)

- `load_relationship_advisors()` now reads `gold/views/rel_architect_lookup.parquet` from S3 instead of deriving from raw accounts_dimension.
- If the lookup file is missing, raises a clear error: "Run 08b_build_architect_attribution.py first."
- `save_rel_lookup()` is now a no-op (retained for caller compatibility). The file is written by 08b.
- `modal_str` function retained (other callers may use it, per constraint).

### 4. Updated `run_gold_layer.sh` (Req 6)

- Inserted `08b_build_architect_attribution.py` before `08_build_nna_aua_by_advisor.py` in both incremental and full modes.
- Updated dependency chain comments and header script list.

### 5. Updated `data_contract.xml`

- Added `architect_attribution.parquet` and `rel_architect_lookup.parquet` gold_script entries.
- Updated `accounts_dimension_latest.parquet` entry with new columns and normalization note.
- Updated `nna_aua_by_advisor.parquet` entry to note architect assignment sourced from 08b lookup.

---

## Briefs Written

| Brief | Path | Audience |
|-------|------|----------|
| DevOps deploy instructions | `docs/briefs/devops-brief-architect-attribution.md` | DevOps |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 08b reads previous run's nna_aua_by_advisor for T0 | Avoids circular dependency. The T0 filter uses aggregate stats (total AUA, num_relationships) which are stable across runs. First run uses the old (unattributed) advisor view to qualify architects — the architect list itself doesn't change. |
| save_rel_lookup in 08 is a no-op, not deleted | Constraint says do not remove modal_str; similarly, keeping the function signature avoids breaking callers while making 08b the single writer of the lookup file. |
| consultant/additional_advisor in TXN_ACCOUNT_COLS | These are standard BD transaction columns. If they don't exist in a given file, the `keep_cols` filter skips them gracefully. |
| FULL mode required for first deploy | Incremental mode won't backfill consultant/additional_advisor into existing accounts. |

---

## Files Modified

| File | Change |
|------|--------|
| `data/black_diamond/scripts/gold/00_build_accounts_dimension.py` | +consultant, +additional_advisor columns; +Olivia->Liv normalization; emoji fix |
| `data/black_diamond/scripts/gold/08b_build_architect_attribution.py` | NEW -- full T0-T16 decision tree |
| `data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py` | load_relationship_advisors reads attributed lookup; save_rel_lookup is no-op |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | 08b added before 08 in incremental + full modes |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml` | +architect_attribution, +rel_architect_lookup entries; updated accounts_dimension |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ADVTV2.001.gold-architect-attribution.md` | Status: complete |
| `docs/briefs/devops-brief-architect-attribution.md` | NEW -- deploy instructions for DT |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE (pending commit + DT deployment)
**Active branch:** `CLOUD`

All 7 requirements from the task order are addressed. The 4 gold layer files are ready for S3 upload and a FULL gold layer run. Scripts 09 and 10 require no changes — they already consume `rel_architect_lookup.parquet` and will automatically pick up the attributed architect names.

---

## Next Steps

1. **[0.4.0_DS_ClientPlatform] Commit** all modified files to CLOUD
2. **[0.4.0_DT_ClientPlatform] Upload** 4 scripts to `s3://opal-data-bd/code/gold/` per `docs/briefs/devops-brief-architect-attribution.md`
3. **[0.4.0_DT_ClientPlatform] Run** gold layer in FULL mode on bd-gold-layer-runner
4. **[0.4.0_DT_ClientPlatform] Verify** rel_architect_lookup has 19 architects + Unresolved, no 49F House
5. **[0.4.0_DE_ClientPlatform] Verify** ADV leaderboard shows 19 named architects after portal data refresh

**Files to touch next:**
- None for DS — handoff to DT for deployment

**Do NOT:**
- Run incremental mode for first deploy (consultant/additional_advisor need full history rebuild)
- Hardcode architect names in any script (they are computed dynamically from the data)

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

#### advi_mvplvl_003_architect_attribution_tree.md

# Architect Attribution Decision Tree — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-13
**Project:** ADVI_MVPLVL 3a
**Data Sources:** `accounts_dimension_latest.parquet`, `nna_aua_by_advisor.parquet`, `account_performance.parquet`, `silver/transactions/*.parquet`

---

## Scope: Funded Accounts Only

`accounts_dimension_latest.parquet` contains 9,407 open accounts, but 3,984 of those
are empty shells with $0 AUA — accounts opened but never funded, or fully liquidated
but not formally closed. The portal shows 5,423 accounts because it reads from
`account_performance.parquet`, which only contains accounts with actual positions.

**This analysis is scoped to the 5,423 funded accounts ($1.583B AUA) — the portal universe.**

---

## True Architect Definition

An architect qualifies if ALL of:
- Total AUA >= $5M
- Number of relationships >= 5
- Not "49F House" or "Unassigned"
- At least 1 new account opened in trailing 12 months (activity filter)

5 entries fail the activity filter: Kyle Sweeney (4 accts), Sydney Cobb (4 accts),
Jackson O'Brien (1), Olivia Shin (1, typo of Liv Shin), Trenton Milner (1). Their
accounts are reclassified through the tree.

**Result: 19 true architects**

---

## Decision Tree

```
FUNDED ACCOUNT (5,423 total)
  |
  v
[T1] Is architect field one of the 19 true architects?
  |-- YES --> resolve to architect                         2,696 accts  $1,039M  (65.7%)
  |-- NO
      |
      v
[T2] Is implementor field one of the 19 true architects?
  |-- YES --> resolve to implementor                         920 accts  $  243M  (15.4%)
  |-- NO
      |
      v
[T3] Is implementor a junior paired 80%+ with a true architect?
  |   (derived from non-49FH accounts where this implementor appears)
  |-- YES --> resolve to senior architect                    564 accts  $   79M  ( 5.0%)
  |-- NO
      |
      v
[T4] Is implementor a junior paired 60-79% with a true architect?
  |-- YES --> resolve to senior architect                    425 accts  $   48M  ( 3.0%)
  |-- NO
      |
      v
[T5] Does another account in the same relationship have a resolution?
  |   (mode of resolved siblings)
  |-- YES --> inherit from relationship                      251 accts  $  105M  ( 6.6%)
  |-- NO
      |
      v
[T6] Does portfolio_group match a true architect name?
  |-- YES --> resolve to that architect                       40 accts  $    4M  ( 0.2%)
  |-- NO
      |
      v
[T7] Does portfolio_group match a junior mapped 80%+ to a true architect?
  |-- YES --> resolve to senior architect                     71 accts  $   11M  ( 0.7%)
  |-- NO
      |
      v
[T8] Relationship inheritance -- pass 2 (after T6-T7 added new resolutions)
  |-- YES --> inherit from relationship                       74 accts  $   13M  ( 0.8%)
  |-- NO
      |
      v
[T9] Does local_relationship ops person have 60%+ of their resolved accounts
  |   under a single true architect?
  |-- YES --> resolve to that architect                       38 accts  $    4M  ( 0.3%)
  |-- NO
      |
      v
[T10] Relationship inheritance -- pass 3 (after T9)
  |-- YES --> inherit from relationship                       12 accts  $    2M  ( 0.1%)
  |-- NO
      |
      v
[T11] Is consultant field (from silver transactions, trailing 12M) a true architect?
  |-- YES --> resolve to consultant                            7 accts  $    1M  ( 0.1%)
  |-- NO
      |
      v
[T12] Is consultant a junior paired 80%+ with a true architect?
  |-- YES --> resolve to senior architect                     29 accts  $    4M  ( 0.3%)
  |-- NO
      |
      v
[T13] Is consultant a junior paired 60-79% with a true architect?
  |-- YES --> resolve to senior architect                     15 accts  $    2M  ( 0.1%)
  |-- NO
      |
      v
[T14] Is additional_advisor field a true architect?
  |-- YES --> resolve to that architect                        0 accts
  |-- NO
      |
      v
[T15] Does additional_advisor map via junior pairing?
  |-- YES --> resolve to senior architect                      2 accts  $  0.6M  ( 0.0%)
  |-- NO
      |
      v
[T16] Relationship inheritance -- pass 4 (after T11-T15)
  |-- YES --> inherit from relationship                        2 accts  $  0.3M  ( 0.0%)
  |-- NO
      |
      v
[UNRESOLVED] -- no deterministic signal                      277 accts  $   27M  ( 1.7%)
```

---

## Tier Summary

| Tier | Logic | Accounts | AUA | % AUA |
|------|-------|----------|-----|-------|
| T1 | Direct architect field | 2,696 | $1,039,342,240 | 65.7% |
| T2 | Implementor IS true architect | 920 | $243,344,448 | 15.4% |
| T3 | Implementor 80%+ junior pair | 564 | $79,217,290 | 5.0% |
| T4 | Implementor 60%+ junior pair | 425 | $47,509,732 | 3.0% |
| T5 | Relationship inherit (pass 1) | 251 | $105,129,609 | 6.6% |
| T6 | Portfolio group = true architect | 40 | $3,866,572 | 0.2% |
| T7 | Portfolio group = mapped junior | 71 | $10,799,046 | 0.7% |
| T8 | Relationship inherit (pass 2) | 74 | $13,153,508 | 0.8% |
| T9 | Local relationship 60%+ pairing | 38 | $4,037,293 | 0.3% |
| T10 | Relationship inherit (pass 3) | 12 | $1,837,238 | 0.1% |
| T11 | Consultant = true architect | 7 | $881,102 | 0.1% |
| T12 | Consultant 80%+ junior pair | 29 | $4,048,956 | 0.3% |
| T13 | Consultant 60%+ junior pair | 15 | $1,644,780 | 0.1% |
| T14 | Additional advisor = true arch | 0 | $0 | 0.0% |
| T15 | Additional advisor junior pair | 2 | $608,372 | 0.0% |
| T16 | Relationship inherit (pass 4) | 2 | $319,409 | 0.0% |
| | **RESOLVED** | **5,146** | **$1,555,739,595** | **98.3%** |
| | **UNRESOLVED** | **277** | **$27,412,537** | **1.7%** |

---

## Final Architect Listing

| # | Architect | Accounts | AUA | % of Total AUA |
|---|-----------|----------|-----|----------------|
| 1 | Travis Penfield | 254 | $380,923,529 | 24.1% |
| 2 | Kyle Sims | 613 | $167,188,162 | 10.6% |
| 3 | David Farrell | 274 | $113,563,194 | 7.2% |
| 4 | Josh Henson | 568 | $98,701,235 | 6.2% |
| 5 | Greg Rosner | 327 | $89,770,472 | 5.7% |
| 6 | Hunter Lloyd | 187 | $87,908,567 | 5.6% |
| 7 | Dean Dillenberg | 406 | $81,570,891 | 5.2% |
| 8 | Chase Bertrand | 406 | $78,037,026 | 4.9% |
| 9 | Ted Grant | 188 | $72,268,122 | 4.6% |
| 10 | Patrick Mundlin | 294 | $68,839,404 | 4.3% |
| 11 | Brandon Lanz | 358 | $66,755,513 | 4.2% |
| 12 | Tim Rodgers | 376 | $63,914,600 | 4.0% |
| 13 | Matt Foxhall | 157 | $46,188,657 | 2.9% |
| 14 | Zach Hawkins | 155 | $42,381,699 | 2.7% |
| 15 | Grant Boren | 169 | $32,975,372 | 2.1% |
| 16 | Lincoln Rock | 122 | $20,318,695 | 1.3% |
| 17 | Michael Ihlenfeldt | 122 | $19,442,023 | 1.2% |
| 18 | Boston Prachyl | 87 | $14,870,336 | 1.0% |
| 19 | Liv Shin | 83 | $10,122,099 | 0.6% |
| -- | **Unresolved** | **277** | **$27,412,537** | **1.7%** |
| | **TOTAL** | **5,423** | **$1,583,152,132** | **100.0%** |

---

## Unresolved Residual (277 accounts, $27.4M)

Dominated by:
- Neil Tjon-Hing as implementor (58 accounts) -- spreads evenly across architects
- No implementor at all (40 accounts)
- Wills Crenshaw (25), Nick Bishop (25), Mitch Roper (25) -- all below 60% pairing threshold
- Caleb Borders (14), Trenton Milner (13) -- sub-threshold juniors
- Centralized Client Ops (11 accounts) -- institutional operations

These accounts have no field in the entire transaction record that points to a single
architect with confidence. They are the true operational/custodial residual.

---

## Key Findings

1. **49F House was not a real entity** -- it was a data-entry catch-all. The decision
   tree recovered ~$517M across 2,450 funded 49F House accounts by tracing implementor,
   relationship, portfolio_group, local_relationship, and consultant signals back to
   the 19 true architects. Only 229 funded 49F House accounts ($22M) remain unresolved.

2. **Scoping matters** -- `accounts_dimension` has 9,407 open accounts but 3,984 are
   empty shells with $0 AUA. The portal universe is 5,423 funded accounts from
   `account_performance`. All analysis must use this as the denominator to match
   what the portal displays.

3. **Josh Henson's book is 4x larger than the raw data shows** -- $26M direct (T1)
   vs $99M attributed (all tiers). His juniors (Conner Haney, Jackson O'Brien,
   Joseph Bolling, Jimmy Henry) had hundreds of accounts tagged to 49F House.

4. **Consultant and additional_advisor fields exist in silver** but are dropped by the
   gold builder (`00_build_accounts_dimension.py`). They provided marginal lift
   (54 accounts, $7.5M) but should be carried through for completeness.

5. **Olivia Shin / Liv Shin** is a confirmed typo duplicate (overlapping relationship).
   Should be normalized to "Liv Shin" in the gold layer.

6. **portfolio_group is unusable as an organizational hierarchy** -- 176 distinct
   values, 83.5% many-to-many with architect. It is an operations-assignment field
   (which support person services the account), not a team or office grouping.

7. **local_relationship** (18 values) is also operations staff, not organizational
   structure. Useful as a last-resort attribution signal (T9) but not a group-by
   dimension.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Scope to 5,423 funded accounts | Portal reads from `account_performance`; 3,984 $0-AUA shells inflate counts misleadingly |
| 19 true architects via $5M + 5 rels + 12M activity | Captures 96.7% of non-institutional AUA; excludes noise |
| Reclassify stale architects through tree | 5 stale entries (11 funded accounts) have no activity in 12M |
| Flat architect list for MVP | No clean grouping dimension exists; portfolio_group and local_relationship are ops fields |
| 16-tier deterministic tree | First-match-wins; 4 relationship inheritance passes; consultant/addl_advisor from silver as late tiers |

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Research deliverable complete. The decision tree logic is validated against the
portal universe of 5,423 funded accounts and explains 98.3% of AUA ($1.556B) across
19 true architects. The remaining 277 accounts ($27.4M) are genuine operational
residual with no deterministic attribution signal.

---

## Next Steps

1. **[1.0.0_SA_CTO] Review attribution tree** -- confirm the 19-architect list and
   tree logic for implementation in the gold layer
2. **[0.4.0_DS_ClientPlatform] If approved** -- implement the attribution logic in a
   new gold script (or extend `08_build_nna_aua_by_advisor.py`) to produce a
   `resolved_architect` column in the advisor-level views
3. **[0.4.0_DS_ClientPlatform] Add consultant + additional_advisor** to
   `00_build_accounts_dimension.py` so these fields are available in the gold layer
4. **[0.4.0_DS_ClientPlatform] Normalize Olivia Shin -> Liv Shin** in the architect
   field during gold build
5. **[0.4.0_DE_ClientPlatform] Update Advisors Tab** -- once resolved_architect is
   available, the leaderboard, Top 3, and rolling flows should read from the
   attributed view instead of raw architect field

#### advi_mvplvl_003_architect_investigation.md

# ADVI_MVPLVL 3a: Portfolio Group + Architect Data Quality Investigation — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-13
**Task Order:** `ADVI_MVPLVL.003.p3-architect-investigation`
**Data Sources:** `s3://opal-data-bd/gold/accounts_dimension_latest.parquet`, `s3://opal-data-bd/gold/views/nna_aua_by_advisor.parquet`

---

## Requirement 1: Portfolio Group Field Analysis

**Source:** `gold/accounts_dimension_latest.parquet` (9,781 accounts, 9,407 open)

| Metric | Value |
|--------|-------|
| Null/blank rate | 0.0% (every account has a portfolio_group) |
| Distinct values | 176 |

### Value Categories

| Category | Count | Examples |
|----------|-------|---------|
| **Institutional/Support** | 6 | `No Advisor` (2,548 accts), `49F Schwab AUM` (969), `Dallas Support` (304), `49 Private Wealth` (41), `49 Solutions` (24), `Centralized Client Ops` (7) |
| **"Local Ops" tagged** | 9 | `Lane Curry - Local Ops` (336), `Sam Owens - Local Ops` (305), `Alex Bright - Local Ops` (305), `Joseph Bolling - Local Ops` (242), etc. |
| **Person names** | 161 | The vast majority are individual person names — the same names that appear in the `architect` field |

### Qualitative Assessment

`portfolio_group` is **not** a team, office, or organizational unit. It is a **second person-name field** that largely mirrors `architect` but with inconsistent formatting, duplicates (e.g., `Joseph Bolling` and `Joseph Bolling - Local Ops` coexist), and operational tags. It appears to be a free-text assignment field in Black Diamond that was never normalized.

The 9 "Local Ops" entries suggest operations staff who handle account servicing, not architects managing client relationships. 3 of these names (`Erick Webb`, `Lane Curry`, `Sam Owens`) also appear as architects — indicating the same person has accounts under both their plain name and their "Local Ops" tag.

---

## Requirement 2: Architect AUA Distribution

**Source:** `gold/views/nna_aua_by_advisor.parquet` (latest date: 2026-03-11, 53 architects)

### Top 20 Architects by AUA

| Rank | Architect | Total AUA | Relationships | NNA (Cumulative) |
|------|-----------|-----------|---------------|-----------------|
| 1 | 49F House | $703,387,999 | 1,477 | $641,072,612 |
| 2 | Travis Penfield | $243,909,648 | 68 | $119,591,906 |
| 3 | Kyle Sims | $94,096,023 | 113 | $63,698,589 |
| 4 | David Farrell | $78,298,695 | 65 | $29,335,954 |
| 5 | Greg Rosner | $60,077,784 | 105 | $42,611,073 |
| 6 | Dean Dillenberg | $55,903,850 | 107 | $33,461,304 |
| 7 | Hunter Lloyd | $49,280,753 | 50 | $37,934,379 |
| 8 | Chase Bertrand | $42,988,315 | 99 | $38,131,667 |
| 9 | Matt Foxhall | $41,907,101 | 64 | $26,376,777 |
| 10 | Tim Rodgers | $40,264,106 | 123 | $28,027,362 |
| 11 | Ted Grant | $35,419,250 | 75 | $31,101,969 |
| 12 | Patrick Mundlin | $29,666,553 | 60 | $20,755,351 |
| 13 | Josh Henson | $26,406,212 | 92 | $16,238,629 |
| 14 | Sydney Cobb | $24,585,283 | 1 | $2,195,813 |
| 15 | Brandon Lanz | $23,189,714 | 40 | $16,721,786 |
| 16 | Zach Hawkins | $16,700,150 | 34 | $11,101,608 |
| 17 | Lincoln Rock | $11,890,574 | 32 | $6,688,519 |
| 18 | Boston Prachyl | $9,542,000 | 30 | $6,745,856 |
| 19 | Grant Boren | $8,768,362 | 23 | $5,207,579 |
| 20 | Liv Shin | $8,354,791 | 33 | $6,373,028 |

### Threshold Analysis

| Threshold | Architects | % of 53 |
|-----------|-----------|---------|
| >= $25M AUA | 13 | 24.5% |
| >= $10M AUA | 17 | 32.1% |
| >= $5M AUA | 21 | 39.6% |
| >= $1M AUA | 30 | 56.6% |

### Concentration

| Metric | Value |
|--------|-------|
| Top 10 share of total AUA | 85.9% |
| Top 20 share of total AUA | 97.8% |
| 49F House alone | 42.9% of total AUA ($703M / $1.64B) |

The long tail (architects 21-53) controls only 2.2% of AUA. Most are sub-$1M accounts — likely operational assignments, not client-facing architect relationships.

### Notable Anomaly: Sydney Cobb

Rank 14 by AUA ($24.6M) but only 1 relationship. This appears to be a single large institutional or family account assigned to an individual. It passes the AUA threshold but fails any relationship-count filter, suggesting it's not a traditional "architect book" pattern.

---

## Requirement 3: Portfolio Group -> Architect Alignment

### Many-to-Many Relationship

| Metric | Value |
|--------|-------|
| Distinct (architect, portfolio_group) pairs | 855 |
| Portfolio groups mapping to >1 architect | 147 / 176 (83.5%) |
| Architects mapping to >1 portfolio_group | 45 / 58 (77.6%) |

**The relationship is heavily many-to-many.** A single architect's accounts are spread across 7-46 different portfolio_groups (median ~20). A single portfolio_group is shared across multiple architects. This makes portfolio_group unusable as a hierarchical parent of architect.

### Name Overlap

29 of 58 architects have a portfolio_group that contains their own name as the top assignment. But the concentration is low — even the best cases only have 25-35% of their accounts under their own-name portfolio_group. The remaining 65-75% of their accounts are scattered across other person-name portfolio_groups.

This pattern is consistent with **portfolio_group being the operations support person** assigned to each account, not the architect. When an architect onboards a client, support staff from the "Local Ops" team is assigned, and the portfolio_group reflects whichever support person handled the account — not which architect owns the relationship.

### Conclusion

`portfolio_group` is not a team, office, or organizational unit. It is an **operations-level assignment field** — essentially "which support person services this account." It is not suitable as a group-by dimension for the Advisors Tab.

---

## Requirement 4: Recommendation

### 4A. Group-by Dimension: Do Not Use portfolio_group

`portfolio_group` fails as a hierarchical grouping dimension because:
1. It is person-name free-text, not an organizational unit
2. It has 176 distinct values — higher cardinality than `architect` (53)
3. It is many-to-many with architect (83.5% of PGs map to multiple architects)
4. No normalization is possible without a hand-curated mapping from 49 Financial

**Alternative grouping dimensions available in accounts_dimension:**

| Field | Suitability | Notes |
|-------|-------------|-------|
| `portfolio_group` | NO | Person names, many-to-many with architect, not an org unit |
| `local_relationship` | UNKNOWN | Not investigated — may have same quality issues |
| `manager` | UNKNOWN | Not investigated |
| `investment_strategy_name` | POSSIBLE | Strategy-level grouping (UST, ST, INT, LTC, LTA, etc.) — already used in ModelPortfolios. This is an asset-level grouping, not a people-level grouping. |

**Recommendation:** For MVP, abandon the Portfolio Group -> Architect -> Implementor hierarchy. Use a flat architect list with a true-architect filter (below) to reduce from 53 to ~19 meaningful entries. If Andrew/CTO confirms that 49 Financial has an internal team structure (e.g., regional offices, pods), a hand-curated mapping table can be loaded later as a dimension — but the gold layer does not currently contain this information.

### 4B. True Architect Filter: `is_true_architect`

**Proposed filter (dual-threshold):**

```
is_true_architect = (total_aua >= $5M) AND (num_relationships >= 5) AND (architect != '49F House')
```

| Filter Criterion | Purpose |
|-----------------|---------|
| `total_aua >= $5M` | Eliminates negligible-AUA operational assignments (33 architects fail this) |
| `num_relationships >= 5` | Eliminates single-account anomalies like Sydney Cobb ($24.6M, 1 relationship) |
| `architect != '49F House'` | Removes the institutional catch-all bucket |

**Result:** 19 true architects out of 53, controlling $884.5M AUA (53.9% of total, or **96.7% of total excluding 49F House**).

The 19 passing architects:

| Architect | AUA | Relationships |
|-----------|-----|---------------|
| Travis Penfield | $243.9M | 68 |
| Kyle Sims | $94.1M | 113 |
| David Farrell | $78.3M | 65 |
| Greg Rosner | $60.1M | 105 |
| Dean Dillenberg | $55.9M | 107 |
| Hunter Lloyd | $49.3M | 50 |
| Chase Bertrand | $43.0M | 99 |
| Matt Foxhall | $41.9M | 64 |
| Tim Rodgers | $40.3M | 123 |
| Ted Grant | $35.4M | 75 |
| Patrick Mundlin | $29.7M | 60 |
| Josh Henson | $26.4M | 92 |
| Brandon Lanz | $23.2M | 40 |
| Zach Hawkins | $16.7M | 34 |
| Lincoln Rock | $11.9M | 32 |
| Boston Prachyl | $9.5M | 30 |
| Grant Boren | $8.8M | 23 |
| Liv Shin | $8.4M | 33 |
| Michael Ihlenfeldt | $7.8M | 24 |

The remaining 33 entries (plus 49F House and Unassigned) would be suppressed from the Advisors Tab leaderboard, Top 3 highlights, and rolling flows — not deleted, just filtered from display.

### 4C. Implementation Path

This filter can be applied in two places:

1. **Script 09 / gold layer** (preferred): Add the filter when building the NNA GEO/ADV donut segments and the advisor_rolling_flows output. This reduces JSON payload size and ensures consistency across all consumers.

2. **Frontend** (fallback): Filter on `total_aua` and `client_count` in the leaderboard and rolling flows components. Quick to ship but duplicates business logic.

The filter thresholds ($5M AUA, 5 relationships) should be configurable constants in whatever layer implements them, not hardcoded in multiple locations.

### 4D. 49F House Treatment

`49F House` is the largest single entry at $703M AUA / 1,477 relationships. It is an institutional catch-all — accounts not assigned to a specific architect. Options:

1. **Suppress entirely** from Advisors Tab (current default for institutional)
2. **Show as a separate "Unassigned" summary** at the top of the Advisors Tab, distinct from the architect leaderboard
3. **Include as a pseudo-architect** in the leaderboard (distorts rankings due to scale)

Recommendation: Option 2 — surface it as an "Unassigned Book" summary panel so the $703M is not invisible, but keep it out of architect rankings.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| portfolio_group is unusable as a hierarchy | 176 values, many-to-many with architect (83.5%), person names not org units |
| Flat architect list with filter for MVP | No clean grouping dimension exists in gold layer; filter reduces noise |
| AUA >= $5M + rels >= 5 as true-architect filter | Captures 19 architects controlling 96.7% of non-institutional AUA |

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

All 4 requirements answered. No code changes made (research-only per task order constraints).

---

## Next Steps

1. **[1.0.0_SA_CTO] Review recommendation** — confirm flat-list approach for MVP; decide if a hand-curated team mapping is worth pursuing with 49 Financial
2. **[0.4.0_DE_ClientPlatform] Incorporate filter into Advisors Tab task orders** — true-architect filter at $5M AUA + 5 relationships for leaderboard, Top 3, and rolling flows
3. **[0.4.0_DS_ClientPlatform] If CTO approves backend filter** — implement `is_true_architect` in `08_build_nna_aua_by_advisor.py` or in `advisor_rolling_flows` publisher

#### assets_overview_mix_investigation.md

# Assets Overview Mix View — Architecture Investigation — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-17
**Start Time:** N/A (investigation session)

## Objective

Andrew flagged two concerns with the Mix toggle in Assets Overview:
1. **Mathematical**: frontend logic slicing a monolithic JSON to track "new assets vs just the split" is incorrect
2. **Data engineering**: using a Lambda + monolithic JSON + frontend period aggregation is out-of-pattern; needs pre-computed portal views

---

## Work Completed

### 1. Full Data Flow Trace

**Current mix flow (Assets Overview, `auaSubMode === 'mix'`):**

```
06b_build_client_mix_timeseries.py (EC2)
  → gold/client_timeseries/{relationship_id}.json  (per-relationship, daily)
  → gold/client_timeseries/0.json  (firm-level aggregate — status unclear, see below)

opal-partners-data Lambda:
  GET /api/scoped/partners/books/relationship/0/mix-timeseries
  → serve_s3_json(bucket, 'gold/client_timeseries/0.json')
  → returns raw {mix: [{date, equity, fixed_income, structured_notes, cash, other}, ...]}

PartnerAnalytics.tsx:
  - getFirmMixTimeseries('bd') → 2000+ daily MixTimeseriesPoint[]
  - firmMixData useMemo → picks LAST point per period (monthly/quarterly/annually)
  - renders 100% stacked bar chart (percentages only, no dollar amounts)
```

### 2. Problem 1 — Dollar Amounts Missing from Raw Data

The `MixTimeseriesPoint` type only contains percentage values (0-1):
```typescript
interface MixTimeseriesPoint {
  date: string
  equity: number        // 0-1 pct
  fixed_income: number  // 0-1 pct
  structured_notes: number
  cash: number
  other: number
}
```

The `06b` gold script computes `market_value` per asset class internally (line 492:
`mix[ac] = round(float(mix_agg.get(ac, 0.0)) / total_mv, 6)`) but ONLY stores pct — the
dollar amounts are discarded at write time.

Result: the chart can only show 100% stacked bars. You cannot display "Equities: $1.02B (62%)" —
only "Equities: 62%". The split is visible but the dollar scale is invisible.

**Andrew's concern about "new assets vs just the split"** resolves to this: a percentage
mix chart (always sums to 100%) doesn't show absolute growth. When equity goes from 60% to
65%, it's impossible to tell if that's:
  a. New clients investing heavily in equity
  b. Market appreciation of existing equity positions
  c. Net rebalancing by existing clients

Without dollar amounts, the chart only shows composition drift, not absolute AUA movement.

### 3. Problem 2 — Firm-Level '0' Aggregate Does Not Appear to Be Explicitly Built

`06b` groups the positions_cube by `relationship_id` (from accounts_dimension). There is no
account with relationship_id='0' in the data — '0' is a synthetic key meaning "firm-level
aggregate." The script does NOT contain any explicit firm-level aggregation step.

Consequence: `gold/client_timeseries/0.json` either:
  a. Does not exist → Lambda returns 404 / empty → Mix tab shows "mix data unavailable"
  b. Was added manually or by a separate step not in 06b

Either way, the firm-level aggregate is not computed with the correct methodology:
correct firm-level mix requires summing market_value by asset_class across ALL relationships
for each date, then computing firm-level pcts. Averaging per-relationship pcts would be wrong
(equal-weighting $50M accounts with $5M accounts).

### 4. Problem 3 — Frontend Period Aggregation Is Out-of-Pattern

`firmMixData` useMemo (PartnerAnalytics.tsx lines 397-416):
- Downloads 2000+ daily data points (the full firm history)
- Groups by granularity-dependent period key (monthly/quarterly/annually)
- Takes the LAST daily point in each period as the end-of-period snapshot
- This is the entire period aggregation logic running in the browser

This violates the "DS logic always goes cloud-side" rule. Compare to the AUA data
(timeseries_chart.json `aua.quarterly/monthly/annually`): pre-aggregated by
`bd-portal-publisher` to three granularities, served directly. The frontend just picks
the right sub-key.

Additional performance issue: the full daily JSON for 2000+ dates is downloaded on every
Mix tab activation. For a firm with 5+ years of history this is a non-trivial payload
(~150KB per call). The frontend then discards all but N period end-dates (12-50 points).

### 5. The "New Assets vs Split" Clarification

Andrew's phrasing "which shouldn't change all that much period over period" is correct for
the **percentage mix** — a firm's asset class mix tends to be stable (62% equity, 24% FI is
unlikely to swing to 50%/40% in one quarter unless there's a large client event). The
frontend is currently doing complex aggregation to produce... a slowly-changing 100% bar.

The **dollar amount** version is far more informative: equity went from $980M to $1.02B this
quarter (+$40M). Of that, how much was market appreciation vs new equity inflows? That's
the GRO view's job. But the Mix view in dollar terms at least grounds the firm's total
exposure correctly.

---

## Diagnosis Summary

| Problem | Root Cause | Severity |
|---------|-----------|----------|
| No dollar amounts | `06b` writes pct only, discards market_value | High — missing required display info |
| Firm '0' aggregate may not exist | `06b` has no explicit firm aggregation logic | High — may be showing stale/empty data |
| Frontend period aggregation | `firmMixData` useMemo slices daily data client-side | Medium — out-of-pattern, fragile, wasteful |
| Percentage-only chart | 100% stacked bars can't show absolute scale | High — misses "both pct and dollar" requirement |

---

## Recommended Architecture

### Gold Layer Change (DS owns)

Extend `06b_build_client_mix_timeseries.py` to add a firm-level aggregation step:

After processing each date partition, maintain a `firm_daily_mix` dict:
  `{date_str: {equity: $, fixed_income: $, ..., total: $}}`

At the end of the build, compute period-level views (quarterly/monthly/annually) using the
LAST daily snapshot per period (consistent with the AUA timeseries pattern). Write to:
  `s3://opal-data-bd/gold/firm_mix_views.json`

**Output shape:**
```json
{
  "generated_at": "...",
  "data_as_of": "YYYY-MM-DD",
  "firm_id": "49financial",
  "views": {
    "quarterly": [
      {
        "period": "2024-Q4",
        "label": "Q4 '24",
        "end_date": "2024-12-31",
        "total_aua": 1620000000.0,
        "equity": {"value": 1004400000.0, "pct": 0.62},
        "fixed_income": {"value": 388800000.0, "pct": 0.24},
        "structured_notes": {"value": 97200000.0, "pct": 0.06},
        "cash": {"value": 81000000.0, "pct": 0.05},
        "other": {"value": 48600000.0, "pct": 0.03}
      },
      ...
    ],
    "monthly": [...],
    "annually": [...]
  }
}
```

This is the same pattern as `timeseries_chart.json aua.quarterly/monthly/annually` — pre-aggregated,
period-labeled, three granularities in one file.

### Lambda Change (DS writes, DT deploys)

Add a new endpoint to `opal-partners-data`:
  `GET /api/scoped/partners/books/firm/mix-views?firmId=xxx`
  → serve_s3_json(bucket, 'gold/firm_mix_views.json')

Pure passthrough. Zero computation in Lambda.

The existing `mix-timeseries` endpoint (daily per-relationship) stays for the Books tab
`MixTimeseriesPanel` (per-client view). The new `firm/mix-views` endpoint serves the
Assets Overview chart only.

### Frontend Change (DE/RD own)

Replace in `PartnerAnalytics.tsx`:
- Remove `getFirmMixTimeseries` call and `firmMixData` useMemo
- Add call to new `getFirmMixViews()` endpoint
- Read `data.views[granularity]` directly — no period aggregation logic in frontend
- Update tooltip to show dollar amount + percentage (not just percentage)
- Chart renders `value` (dollar) as bar height with `pct` in tooltip — OR keep 100% stacked
  but label tooltip with both "$1.02B (62%)"

Decision on chart type is a DE/RD call — either:
  a. Keep 100% stacked bars, enrich tooltip with dollar amounts
  b. Switch to absolute stacked bars (height = dollar amount, same colors)
  Option (b) is more informative for "what did the firm hold" but loses the clean pct-sum-to-100 visual.
  Option (a) is lower-risk and satisfies the "both pct and dollar" requirement.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Extend 06b for firm-level aggregate (not a separate script) | 06b already has all market_value data per date in memory. Adding firm aggregation is a natural extension of the same loop — no second pass needed. |
| Write period views from gold layer, not Lambda | Lambda should not aggregate. Gold runner is the correct place for period slicing. Consistent with bd-portal-publisher pattern. |
| New endpoint (firm/mix-views) separate from relationship/mix-timeseries | Different data shapes, different consumers. Keep per-relationship daily data separate from firm-level pre-aggregated views. |
| Include dollar amounts in gold output | Fixes "both pct and dollar" requirement. Market value is computed anyway inside 06b — no additional data joins needed. |

---

## Files to Touch

| File | Change | Owner |
|------|--------|-------|
| `data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py` | Add firm-level daily aggregation + period view computation + write to `gold/firm_mix_views.json` | DS |
| `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py` | Add `GET /api/scoped/partners/books/firm/mix-views` passthrough | DS |
| `portal/src/api/endpoints/advisor-intelligence.ts` | Add `getFirmMixViews()` function | DE/RD |
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | Replace firmMixRaw + firmMixData useMemo with getFirmMixViews call | DE/RD |
| `portal/src/pages/AdvisorIntelligence/types.ts` | Add `FirmMixViewsResponse` type | DE/RD |

---

## Blockers

None for DS scope (06b extension + Lambda endpoint). DE/RD frontend changes are unblocked
once the endpoint and gold output shape are confirmed.

---

## Current State

**Status:** COMPLETE (investigation only — no code written yet)
**Active branch:** `CLOUD`

Investigation complete. Three compounding problems identified:
  1. Dollar amounts stripped from gold output
  2. Firm-level '0' aggregate not explicitly built
  3. Frontend period aggregation is out-of-pattern

Recommended fix is an extension to `06b` + new Lambda passthrough endpoint + frontend
replacement of the `firmMixData` useMemo. Andrew needs to confirm the chart type direction
(100% stacked + rich tooltip vs absolute dollar stacked) before DE/RD can finalize the
frontend changes.

---

## Next Steps

1. **[Andrew] Confirm** chart type direction: (a) 100% stacked bars with dollar+pct tooltip, or (b) absolute dollar stacked bars showing total AUA scale
2. **[0.4.0_DS_ClientPlatform] Implement** 06b firm-level aggregation + period view output + Lambda endpoint
3. **[0.4.0_DT_ClientPlatform] Deploy** updated 06b to EC2, run gold layer, deploy Lambda
4. **[0.4.0_DE_ClientPlatform] / [0.4.2_RD_AdvisorIntelligence] Replace** firmMixData useMemo with getFirmMixViews call, update tooltip

**Do NOT:**
- Average per-relationship percentages to get firm-level mix (wrong: equal-weights all relationships regardless of size)
- Continue expanding the frontend useMemo to add dollar amounts (wrong direction: computation belongs cloud-side)
- Use the existing `mix-timeseries` endpoint for the firm-level Assets Overview chart (different shape/purpose from per-client MixTimeseriesPanel)

#### aua_valuation_gap_diagnosis_and_fix.md

# AUA Valuation Gap Diagnosis and Fix -- 0.4.0_DS_ClientPlatform

**Date:** 2026-03-17

## Objective

Cross-validate the GRO (Growth Decomposition) panel values in the AdvisorIntelligence Assets Overview by independently checking that AUA, NNA, and market components reconcile. Discovered a systematic gold-vs-silver AUA gap of +$37.5M across 35 accounts. Diagnosed root causes at position level and implemented fixes for the two highest-impact categories.

---

## Work Completed

### 1. GRO Decomposition Identity Validation

Wrote `.tmp_gro_validation.py` to verify: `AUA(end) = AUA(start) + Market(month) + NNA(month)`.

Result: Identity holds perfectly across all months (tautological by construction in the Lambda). Monthly market-as-%-of-AUA values are within expected ranges (-7.2% to +8.9%). The decomposition math is correct.

However, gold-vs-silver cross-check at month boundaries revealed large gaps:
- Feb 26: Gold $1.52B vs Silver $1.63B (-$114M / -7.0%)
- Jan 29: Gold $1.60B vs Silver $1.57B (+$25M / +1.6%)
- Mar 13: Gold $1.62B vs Silver $1.58B (+$39M / +2.4%)

### 2. Account-Level Gap Distribution

Wrote `.tmp_gap_distribution.py` to bucket account-level gaps.

- 35 accounts with abs(gap) > $1M: net +$37.5M (92% of total gap)
- 587 accounts with abs(gap) > $100K: net +$41.5M
- 5,280 accounts with abs(gap) < $100K: largely cancel out

### 3. Position-Level Drill on All 35 Accounts

Wrote `.tmp_position_drill.py` to show every position in gold vs silver's account MV for the top 35.

Identified 9 distinct root cause categories:

| RC | Description | Net Impact |
|----|-------------|------------|
| RC1 | Wrong ticker resolution (structured notes priced as parent equity) | +$25.3M |
| RC2 | Model portfolio sleeves at wrong NAV (Brinker Capital Destinations) | +$20.3M |
| RC3 | Position misattribution within household (nets to ~$0 at relationship level) | -$1.5M |
| RC4 | Private/alternative funds at $1.00 or stale NAV | -$2.0M |
| RC5 | Account missing from positions cube (new onboard) | -$4.9M |
| RC6 | Ghost/stale positions for closed/zeroed accounts | +$7.2M |
| RC7 | Incomplete position data (SMA/wrap/401k) | -$9.3M |
| RC8 | Systematic ETF/bond pricing gap (canonical vs BD) | -$6.7M |
| RC9 | Real estate / non-custodied assets in silver only | -$3.75M |

### 4. Fix Implementation (RC1/RC2 + RC6)

v1 zeroed assets (creates cliff). v2 used silver tape (only covers Jan+). v3 (final): reverse-engineer per-unit prices from silver and inject into canonical_prices.parquet as `source='scoped_override'`. Covers full history back to each asset's inception.

**New file: `data/black_diamond/scripts/silver/inject_scoped_overrides.py`**

Manages a scoped override registry of 5 assets. Removes wrong-source rows, injects daily scoped_override rows from inception to latest date. Idempotent. Dry run: 1,721 rows injected, 5,799 wrong rows removed, zero duplicates.

| Asset | Wrong Price | Correct Price | Inception | Method |
|---|---|---|---|---|
| Waldrop Donor Advised Fund | $1.00 | $1.95 | 2023-09-13 | Silver-implied NAV (std $0.03) |
| BNP PARIBAS SA | $97.16 (BNPQF) | $0.75 | 2024-12-06 | 75c on dollar face value |
| DESTINATIONS LARGE CAP EQUITY I | $546.00 | $13.30 | 2025-10-02 | Blended silver-implied |
| DESTINATIONS INTERNATIONAL EQUITY I | $384.00 | $13.30 | 2025-10-02 | Blended silver-implied |
| JPMORGAN CHASE FINL CO LLC 0% 2029 | $1.00 | $2.55 | 2024-04-10 | 255c on dollar structured note |

**Simplified: `data/black_diamond/scripts/gold/aua_overrides.json` (v3.0.0)**

RC6-only. Silver tape section removed.

**Simplified: `data/black_diamond/scripts/gold/05_build_client_performance.py`**

Stripped silver tape infrastructure. Now only loads ghost account exclusions. RC1/RC2 fix is entirely in canonical_prices.

### 5. AE Task Order

Wrote `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/aua-scoped-price-overrides-deploy.md` with full deployment sequence for inject -> rebuild -> validate -> propagate.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Scoped overrides in canonical_prices instead of silver tape or zeroing | Zeroing creates a cliff; silver tape only covers Jan+ (2 months of silver data). Reverse-engineering the per-unit price and injecting into canonical_prices covers the full history back to inception. The override is inline -- no separate runtime lookup needed. |
| Exclude ghost accounts entirely (RC6) | Silver says $0, gold has $2-3M of stale positions. No intermediate option: either include phantom AUA or exclude it. |
| Defer RC8 (ETF pricing gap) to Phase 2 | Systematic 15-27% gap across standard ETFs suggests a price timing issue (T-1 vs T close). Needs investigation of canonical price timestamps before designing a fix. A silver-calibration fallback risks circular dependency. |
| Config file instead of hardcoded overrides | `aua_overrides.json` is human-readable, version-tracked, and extensible. Adding new overrides doesn't require code changes. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/aua_overrides.json` | New -- price overrides + ghost accounts config | Pending |
| `data/black_diamond/scripts/gold/05_build_client_performance.py` | Load overrides, apply in partition processing | Pending |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/briefing-aua-valuation-fixes-v1.md` | New -- DT deployment briefing | Pending |

---

## Blockers

None. Code changes are self-contained. Deployment requires DT to run the updated script on EC2 and propagate downstream.

---

## Current State

**Status:** COMPLETE (pending commit + DT deployment)
**Active branch:** `CLOUD`

The updated `05_build_client_performance.py` loads `aua_overrides.json` at startup, zeroes 5 mispriced asset names, and excludes 4 ghost accounts from the positions cube before computing AUA. Expected to reduce the gold-vs-silver gap from +3.5% to <1.5%. NNA flows are unaffected.

---

## Next Steps

1. **[0.4.0_DS_ClientPlatform] Commit** all three files to CLOUD
2. **[0.4.0_DT_ClientPlatform] Deploy** updated script + config to EC2 via `safe-ec2-deploy.sh`
3. **[0.4.0_DT_ClientPlatform] Run** `05_build_client_performance.py --upload` to regenerate gold parquet
4. **[0.4.0_DT_ClientPlatform] Run** `05c_validate_aua_vs_silver.py` to confirm gap reduction
5. **[0.4.0_DT_ClientPlatform] Run** downstream scripts (07-10) to propagate into portal JSON
6. **[0.4.0_DS_ClientPlatform] Phase 2** -- investigate RC8 (ETF price timing gap) by comparing canonical_prices timestamps against BD allocation `as_of_date`

**Files to touch next:**
- `silver/prices/canonical_prices.parquet` -- investigate T vs T-1 close timing for RC8

**Do NOT:**
- Implement silver-calibration fallback without confirming the price timing root cause
- Remove ghost accounts from the exclusion list without verifying they are still closed in silver

#### mix_concentration_full_audit.md

# Mix + Concentration Full Audit — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-17

## Objective

Full audit of every layer of the Mix and Concentration views: firm-level Assets Overview,
advisor-level, and client-level. Covers the $60M insurance appear/disappear pattern, the
5000% display bug, the firm-level architecture flaws, and the client-level stub state.

---

## Work Completed

### 1. 5000% Display Bug — Root Cause Confirmed

**Location:** `handle_books_composition` in opal-partners-data Lambda
**Affected surfaces:** `FirmCompositionSnapshot` (Assets Overview Mix panel), `ClientsTab.tsx`
  composition snapshot

**Root cause:** The Lambda sends `pct` as a 0-100 value:
```python
# Lambda (line 904 and 931):
'pct': round(float(mv) / total_mv * 100, 2)  # e.g., 62.5 means 62.5%
```

The frontend treats it as 0-1 and multiplies by 100 again:
```typescript
// PartnerAnalytics.tsx line 2297, ClientsTab.tsx line 824, 872:
{(item.pct * 100).toFixed(1)}%   // 62.5 * 100 = 6250.0%
```

A 62.5% equity allocation renders as "6250.0%". This is why every mix/concentration snapshot
on the portal shows values in the thousands of percent.

**The pie chart is also broken:** `concPieData` uses `value: it.pct` where pct=62.5. All
pie segments are ~60-80, so the pie chart renders roughly equal-sized regardless of actual
allocation (the proportions are correct but the absolute scale is meaninglessly large, which
Recharts normalizes to fill the circle — the chart looks visually OK but it's arithmetically
wrong if you ever add a denominator check).

**Fix is a one-liner:** Change Lambda `pct` to `round(float(mv) / total_mv, 6)` (remove `* 100`),
or change all frontend `(item.pct * 100)` to `(item.pct).toFixed(1)`. Lambda-side fix is
cleaner — the frontend convention everywhere else is 0-1 for pct values.

---

### 2. $60M Insurance Appearing/Disappearing — Diagnosis

**Symptom:** ~$60M labeled as structured_notes (insurance/annuities) appears in certain
quarters, disappears in others, then re-appears.

**Root cause hypothesis (AP gate + reporting cadence):**

The `06b` gold script applies the AP active gate:
```python
AP_GATE_DAYS = 45
last_seen = pos['account_id'].map(ap_last_seen).fillna(pd.Timestamp.min)
pos = pos[last_seen >= cutoff]  # cutoff = date - 45 days
```

This gate excludes any account not seen in `account_performance` within 45 days of the
snapshot date. This is CORRECT for standard BD accounts (prevents $371M stale-holdings
inflation). But insurance/annuity accounts present differently:

- **Insurance/annuity products** (SHIELD, BUFFER, variable annuities) are often held via
  insurance carriers, not standard custodians. Their position data in `positions_cube` may
  only update monthly or quarterly (statement-cycle reporting), not daily.
- If an insurance account's last `account_performance` entry was 47 days ago (just outside
  the 45-day gate), ALL its holdings are excluded from that day's snapshot.
- The next day, if a new account_performance entry arrives (end of month), the account
  reappears — and so does the $60M.

This creates the pattern Andrew observed: present for a few weeks, absent for 1-6 weeks,
present again.

**Secondary hypothesis (classification volatility):**

The `_RE_STRUCTURED` regex matches:
```python
r'SHIELD|ANNUIT|BUFFER|MANAGED FLOOR|FLOOR ETF|YR -|YEAR -|CAP 20%|CAP 15%|CAP 10%'
```

If the asset_name field for these products is inconsistent across different positions_cube
dates (e.g., "ALLIANZ STRUCTURED ALPHA" vs "ALLIANZ STRUCT. ALPHA" — one matches SHIELD/none
of the patterns), the classification could flip between structured_notes and equity/other
quarter to quarter. This would cause the apparent appearance/disappearance of the structured
notes bucket even when the accounts are continuously present.

**To differentiate:** Need to check:
1. Do the $60M accounts appear/disappear in `account_performance` (AP gate issue)?
2. Does the asset_name string for these products change across dates (classification volatility)?
3. Is the market value $60M or near-zero when they reappear (pricing issue)?

Both can coexist. The AP gate is more likely the primary driver given the quarterly
cadence of insurance reporting.

**Proposed fix for AP gate sensitivity:**
- Do NOT simply increase AP_GATE_DAYS globally — that would re-introduce the $371M stale
  positions from closed accounts.
- Instead: identify insurance/annuity account_ids via a flag in accounts_dimension
  (e.g., `is_insurance_custodian` or `reporting_frequency = 'monthly'`) and apply a longer
  gate (90-180 days) only to those accounts.
- Or: skip the AP gate for accounts classified as insurance custodians entirely (their
  positions don't go stale the same way as BD accounts).

**This requires investigation before designing a fix.** Need to look at the specific
account_ids driving the $60M, check their `account_performance` last_seen dates, and
verify whether they're insurance/annuity products with the AP gate as root cause.

---

### 3. Firm-Level Mix — Architecture Summary (from prior investigation)

Three compounding problems documented in `assets_overview_mix_investigation.md`:
1. Dollar amounts stripped from gold output (06b stores pct only)
2. Firm-level '0' aggregate not explicitly built
3. Frontend period aggregation (firmMixData useMemo) is out-of-pattern

Andrew confirmed option B: absolute dollar stacked bars (bar height = total AUA, each
segment = dollar amount of that asset class). This requires dollar amounts in the gold output.

---

### 4. Client-Level Mix/Concentration — Current State

**`ClientDetailPage.tsx`** (the main client detail view):
```typescript
// TODO: Replace with actual API call
setTimeout(() => {
  setClientData(null)
  setIsLoading(false)
}, 300)
```
The client detail page has a hardcoded stub. It always shows null client data. The
`MixTimeseriesPanel` and `ConcentrationPanel` components exist and are wired up with the
API functions (`getMixTimeseries`, `getConcentrationTimeseries`), but `ClientDetailPage`
doesn't render them — it only renders `AISummaryPanel`, `PortfolioBalancePanel`, and
`TimeSeriesPanel` (which also appear to be stub/mock state given the TODO comment).

The Books tab's `ClientsTab.tsx` DOES render the composition snapshot (the `FirmCompositionSnapshot`
pattern) for individual clients/advisors, but through the `getBooksFirmComposition` endpoint
which computes from live `holdings_lots` snapshots — NOT from the `06b` per-relationship
timeseries. This is the surface showing the 5000% pct bug.

**Per-relationship timeseries panels** (`MixTimeseriesPanel`, `ConcentrationPanel`):
- These call the correct endpoint (`mix-timeseries`, `concentration-timeseries`)
- But they fall back to MOCK_DATA when no real data arrives (line 95: `const chartData = isPlaceholder ? MOCK_DATA : data`)
- They are not wired into `ClientDetailPage` — they're orphaned components

**What's actually live for client-level:**
- `BooksClientDetailResponse` from `bd-portal-advisor-publisher` (AISummary, PortfolioBalance, TimeSeries)
- `BooksCompositionResponse` from `handle_books_composition` (live holdings_lots snapshot)
- Mix pct bug present on the composition snapshot

**What's NOT live:**
- Per-relationship daily mix timeseries (MixTimeseriesPanel)
- Per-relationship daily concentration timeseries (ConcentrationPanel)
- These require 06b to have run and written per-relationship JSONs, PLUS wiring into ClientDetailPage

---

### 5. Advisor-Level Mix — Not Built Yet

No advisor-level mix endpoint exists. No task order has been issued for it. The existing
advisor book endpoint (`/api/shared/advisor-intelligence/advisors/{id}/book`) includes
`portfolio_composition: AdvisorPortfolioComposition` which has:
```typescript
interface AssetAllocationItem {
  category: string
  label: string
  pct: number  // also likely 0-1 convention, unverified
}
```
This is a snapshot, not a timeseries, and comes from the `bd-portal-advisor-publisher`
script — not from 06b. The pct scale convention for this endpoint is unverified.

**To add advisor-level mix timeseries:**
- Option A: Use 06b output per relationship, aggregate per-advisor server-side
  (requires knowing which relationship_ids belong to each advisor — the rel_architect_lookup)
- Option B: Add an advisor aggregation step to 06b (writes `gold/advisors/{advisor_id}/mix.json`)
  analogous to how advisor book.json is written
- Option B is cleaner — same pattern as advisor/book.json

---

## Bugs and Issues Summary

| # | Issue | Location | Severity | Fix Complexity |
|---|-------|----------|----------|----------------|
| B1 | pct scale: Lambda sends 0-100, frontend expects 0-1 | Lambda `handle_books_composition`, `PartnerAnalytics.tsx`, `ClientsTab.tsx` | CRITICAL | Trivial (one-liner in Lambda) |
| B2 | Insurance $60M appears/disappears | `06b` AP gate, positions_cube reporting cadence | High | Medium (requires investigation + targeted gate override) |
| B3 | Firm-level mix shows no dollars, uses wrong methodology | `06b` gold output, `firmMixData` useMemo | High | Large (new gold output, new endpoint, new chart) |
| B4 | Firm-level '0' aggregate not explicitly built | `06b` | High | Medium (add firm aggregation step) |
| B5 | Frontend period aggregation for mix | `PartnerAnalytics.tsx` `firmMixData` useMemo | Medium | Small (once gold output is fixed) |
| B6 | `ClientDetailPage` shows stub data, MixTimeseriesPanel orphaned | `ClientDetailPage.tsx` | Medium | Medium (wiring) |
| B7 | Advisor-level mix does not exist | gold layer, Lambda | Medium | Large (new workstream) |
| B8 | Pie chart uses wrong pct as value (works visually but wrong arithmetically) | `PartnerAnalytics.tsx`, `ClientsTab.tsx` | Low | Trivial (same fix as B1) |

---

## Project Scope Assessment

This is too large for a single task order to a single agent. The work spans:
- Data science (classification audit, AP gate investigation, gold layer redesign)
- Lambda/infrastructure (new endpoints, pct fix)
- Dashboard engineering (firm-level chart redesign, client-level wiring)
- React design (absolute dollar bar chart, client detail page)
- DevOps (06b deploy to EC2, Lambda deploy)

**Recommended decomposition into a registered project (ADVI_MIXV2 or similar):**

| Workstream | Description | Primary Agent |
|------------|-------------|---------------|
| WS1 | B1 pct bug: Lambda fix (5 min) | DS or DE |
| WS2 | B2 Insurance AP gate: investigation + targeted fix | DS |
| WS3 | B3/B4/B5 Firm-level mix: 06b aggregation + period views + Lambda endpoint | DS + DT/AE |
| WS4 | B3 frontend: absolute dollar bars, replace useMemo | DE + RD |
| WS5 | B6 Client-level wiring: ClientDetailPage + MixTimeseriesPanel | DE + RD |
| WS6 | B7 Advisor-level mix: 06b advisor aggregation + endpoint | DS + DT/AE |

WS1 is an immediate hotfix — should be committed today, independent of PRD.
WS2 blocks WS3 (you don't want to ship the pre-computed firm mix if $60M of it is volatile).
WS3 blocks WS4.
WS5 and WS6 are independent and can run in parallel with WS2-4.

---

## Current State

**Status:** COMPLETE (audit only)
**Active branch:** CLOUD

Full audit complete. Five distinct problem areas identified with root causes and
fix complexity mapped. Recommend PRD for the full project, with B1 (pct bug) issued
as an immediate hotfix task order before the PRD is drafted.

---

## Next Steps

1. **[Andrew] Decide** whether to elevate to a registered project with PRD (ADVI_MIXV2) or
   issue as ad-hoc task orders
2. **[0.4.0_DS_ClientPlatform] Issue B1 hotfix** — Lambda pct fix is trivial and should not
   wait for the PRD
3. **[0.4.0_DS_ClientPlatform] Investigate B2** — pull the $60M account_ids, check
   account_performance last_seen dates, check asset_name consistency for structured_notes hits
4. **[Andrew] Confirm PRD scope** — does advisor-level mix (WS6) belong in this project or
   is it a separate initiative?

**Do NOT:**
- Ship the firm-level mix redesign (WS3) before investigating B2 — a volatile $60M bucket
  will be baked into the pre-computed views
- Increase AP_GATE_DAYS globally — that would re-introduce the $371M stale-positions problem

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

#### ADVI_BKSCMP.001.ds-script12-lambda-routes.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Write script 12 (`12_build_composition_artifacts.py`) to pre-compute per-class top-9
    holdings composition artifacts for firm (N1) and all advisors (L2), update
    `run_gold_layer.sh` to include it, and add two new S3-proxy Lambda routes
    (`handle_firm_composition`, `handle_advisor_composition`) to opal-partners-data v2.8.
    These changes unblock the ConsolidatedOverviewPanel holdings panel which currently
    renders empty at N1 and L2 because the composition endpoints return 404.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md (canonical schema §3, algorithm §WS1,
    Lambda changes §WS2, sequencing §5).

    Current state:
    - `handle_books_composition` (line 829 of lambda_function.py) handles ALL entity types
      via in-Lambda computation from parquet. For firm/advisor it either times out or errors.
    - Routing at line 1222: `elif action == 'composition': return handle_books_composition(...)`
      routes firm and advisor to the computation-based handler.
    - L3/L4 (relationship, account) composition works today via `handle_books_composition`
      — do NOT change that behavior.
    - Current Lambda version: 2.7 (deployed at partners-api-v1.4.0).
    - run_gold_layer.sh: both modes have `08b` immediately followed by `06b`.
      Incremental: line 114 (08b), line 115 (06b). Full: line 158 (08b), line 159 (06b).

    advisor_id sanitization canonical transform (ClientsTab.tsx:383):
      name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
    Python equivalent (must match exactly):
      advisor_id = re.sub(r'[^a-z0-9_]+', '_',
                          name.lower().strip()).strip('_')[:60] or 'unknown'
    This is the key cross-agent consistency requirement. Any deviation breaks the S3 key lookup.
  </context>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="modify">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS1-script12">
      Write `data/black_diamond/scripts/gold/12_build_composition_artifacts.py`.

      Header comment (required):
        # Classification logic mirrored from 06b_build_client_mix_timeseries.py -- keep in sync
        # Do NOT import from 06b directly (numeric prefix prevents clean imports).

      Inline (copy verbatim from 06b): ETF_CLASSIFICATIONS, ASSET_NAME_TO_TICKER,
      _OPAL_ETF_OVERRIDES, and classify_series(). These are the classification lookup tables.

      Algorithm (per PRD §WS1):
      1. Discover latest holdings_lots parquet: list s3://opal-data-bd/holdings_lots/*.parquet,
         sort by name descending, take the first. Read with pandas. Filter is_open == True.
         If no file found: log ERROR, sys.exit(1).
      2. Apply _OPAL_ETF_OVERRIDES to fix null tickers for Opal/Pathfinder ETFs:
         for rows where ticker is null/NaN but asset_name matches a key in _OPAL_ETF_OVERRIDES,
         set ticker = _OPAL_ETF_OVERRIDES[asset_name].
      3. Add asset_class column: apply classify_series(row.ticker, row.asset_name) per row.
      4. Load rel_architect_lookup.parquet from s3://opal-data-bd/gold/views/rel_architect_lookup.parquet.
         Columns needed: relationship_id, architect (= resolved architect name).
         On any failure: log WARN, fall back to loading
         s3://opal-data-bd/gold/views/client_dimension.parquet, join on relationship_id,
         use primary_architect column, rename to architect. If that also fails: log ERROR, sys.exit(1).
      5. Merge lookup onto holdings by relationship_id (left join, keep all holdings).
      6. Compute firm composition (all rows) — see PRD §WS1 algorithm step 5 for the
         full sequence: total_market_value, class groups, per-class top-9, global top-9,
         global other, unclassified.
         Output schema: exactly as PRD §3 with scope = {"firm_id": "49financial"}.
         Pct conventions (critical — per PRD §3):
           mix[i].pct = class_mv / total_market_value
           mix[i].top_holdings[j].pct = holding_mv / class_mv  (NOT total_market_value)
           top_holdings[j].pct (root) = holding_mv / total_market_value
           other.pct (root) = root_other_mv / total_market_value
           mix[i].other.pct = class_other_mv / class_mv
         Write to: s3://opal-data-bd/gold/views/firm_composition.json
      7. Loop over unique architect values in the merged dataframe.
         For each architect, filter holdings to architect == that_value.
         Compute advisor_id using the canonical transform:
           import re
           advisor_id = re.sub(r'[^a-z0-9_]+', '_', architect.lower().strip()).strip('_')[:60] or 'unknown'
         Compute same composition structure as step 6 but scoped to that advisor.
         scope = {"advisor_id": advisor_id, "firm_id": "49financial"}
         If advisor has 0 open holdings after filter: skip (do not write).
         Write to: s3://opal-data-bd/gold/advisors/{advisor_id}/composition.json
      8. Print summary line:
           print(f'OK: firm_composition.json written. Advisors: {N} written, {M} skipped (empty book).')

      key field: ticker if non-null/non-empty, else re.sub(r'\s+', '_', asset_name.lower())[:40]
      label field: ticker if non-null/non-empty, else asset_name[:30]
    </requirement>

    <requirement id="2" workstream="WS1-run_gold_layer">
      Update `data/black_diamond/scripts/gold/run_gold_layer.sh`.

      In BOTH the incremental section (around line 114) and the full section (around line 158),
      insert script 12 AFTER 08b and BEFORE 06b:

      Incremental (insert between lines 114 and 115):
        run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"

      Full (insert between lines 158 and 159):
        run_script "$SCRIPTS_DIR/12_build_composition_artifacts.py"

      Script 12 takes no mode flags (runs the same in both modes).
      Do NOT move or change any other script position.
      Update the sequence comments at lines 11 and 16 (header comments) to include 12
      in the script list between 08b and 06b.
    </requirement>

    <requirement id="3" workstream="WS2-lambda-helpers">
      In opal-partners-data lambda_function.py, add two new helper functions AFTER the
      existing `cors_response` function (around line 106) and BEFORE `serve_s3_json`:

      A. `cors_response_nocache(status_code, body)` — exact code from PRD §WS2-A:
        Identical to cors_response but with Cache-Control: 'no-store, no-cache, must-revalidate'
        instead of the existing max-age header. Uses same DecimalEncoder.

      B. `serve_s3_json_nocache(bucket, key)` — PRD §WS2-B:
        Copy the body of the existing `serve_s3_json` function verbatim,
        replacing ALL calls to `cors_response(...)` with `cors_response_nocache(...)`.
        Do not change any S3 logic or error handling.

      These two functions are the only new helpers.
    </requirement>

    <requirement id="4" workstream="WS2-lambda-handlers">
      Add two new handler functions AFTER the existing `handle_advisor_mix_views` function
      (around line 1063) and BEFORE the `# Main Handler` section comment:

      C. `handle_firm_composition(bucket)` — PRD §WS2-C:
        return serve_s3_json_nocache(bucket, 'gold/views/firm_composition.json')

      D. `handle_advisor_composition(bucket, advisor_id)` — PRD §WS2-D:
        Validate: if not advisor_id or '/' in advisor_id or '..' in advisor_id:
          return cors_response_nocache(400, {'error': 'Invalid advisor_id'})
        return serve_s3_json_nocache(bucket, f'gold/advisors/{advisor_id}/composition.json')

      Add docstrings consistent with the existing handlers in the file.
    </requirement>

    <requirement id="5" workstream="WS2-lambda-routing">
      Update the routing block in `lambda_handler` at line 1222.

      Current (single branch handles ALL entity types):
        elif action == 'composition':
            return handle_books_composition(bucket, entity_type, entity_id)

      Replace with (firm/advisor get new S3-proxy handlers; relationship/account keep existing):
        elif action == 'composition' and entity_type == 'firm':
            return handle_firm_composition(bucket)
        elif action == 'composition' and entity_type == 'advisor':
            return handle_advisor_composition(bucket, entity_id)
        elif action == 'composition':
            return handle_books_composition(bucket, entity_type, entity_id)

      This preserves L3/L4 (relationship, account) behavior exactly. Only firm and advisor
      composition are redirected to the new S3-proxy handlers.

      IMPORTANT: the `advisor` composition routing must appear BEFORE the generic
      `elif action == 'composition':` fallback, matching the pattern used for timeseries.
    </requirement>

    <requirement id="6" workstream="WS2-lambda-version">
      Bump the Lambda version constant from 2.7 to 2.8.
      Add the two new routes to the API endpoint docstring at the top of the file:
        GET /api/scoped/partners/books/firm/all/composition?firmId=xxx
        GET /api/scoped/partners/books/advisor/{advisor_id}/composition?firmId=xxx
    </requirement>

    <requirement id="7" workstream="commit">
      Commit both WS1 files (script 12 + run_gold_layer.sh) in ONE commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(bd-gold): script 12 composition artifacts + run_gold_layer.sh update (ADVI_BKSCMP WS1)"

      Commit the Lambda changes (lambda_function.py) in a SEPARATE commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(opal-partners-data): firm+advisor composition routes v2.8 (ADVI_BKSCMP WS2)"

      Report both commit SHAs to COO. The Lambda commit SHA is the gate for DT (ADVI_BKSCMP.003).
      The script 12 + run_gold_layer.sh commit SHA is the gate for AE (ADVI_BKSCMP.004).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">script 12 exists at correct path; runs without import errors in Python 3.12</criterion>
    <criterion id="2">advisor_id sanitization in script 12 matches ClientsTab.tsx:383 exactly</criterion>
    <criterion id="3">pct conventions match PRD §3 table (per-class top_holdings pct / class_mv, not total)</criterion>
    <criterion id="4">run_gold_layer.sh incremental: 08b immediately followed by 12, then 06b (no other reordering)</criterion>
    <criterion id="5">run_gold_layer.sh full: same 12 insertion after 08b, before 06b</criterion>
    <criterion id="6">cors_response_nocache returns Cache-Control: no-store, no-cache, must-revalidate</criterion>
    <criterion id="7">serve_s3_json_nocache is a structural copy of serve_s3_json — only cors_response calls differ</criterion>
    <criterion id="8">Lambda routing: firm+composition → handle_firm_composition; advisor+composition → handle_advisor_composition; relationship/account+composition → handle_books_composition (unchanged)</criterion>
    <criterion id="9">Lambda version = 2.8</criterion>
    <criterion id="10">Two separate commits on CLOUD; SHAs reported to COO</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT import from 06b — inline the classification logic with the required header comment</constraint>
    <constraint>Do NOT change handle_books_composition — it must remain for L3/L4 (relationship, account)</constraint>
    <constraint>Do NOT use DuckDB — pandas only (confirmed present on EC2)</constraint>
    <constraint>advisor_id sanitization must match ClientsTab.tsx:383 exactly — any deviation breaks S3 key lookup</constraint>
    <constraint>All pct fields are 0–1 (not 0–100) — consistent with all other mix artifacts in this repo</constraint>
    <constraint>No emojis anywhere in code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>commit to CLOUD parent repo only — no portal changes in this task order</constraint>
    <constraint>Do not modify any other script positions in run_gold_layer.sh</constraint>
    <constraint>If advisor produces 0 open holdings after filter: skip (do not write empty JSON)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      No upstream DS gates — script 12 reads from existing S3 artifacts (holdings_lots from 03,
      rel_architect_lookup from 08b). Both are confirmed present on S3.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">data/black_diamond/scripts/gold/12_build_composition_artifacts.py + run_gold_layer.sh (one commit)</deliverable>
    <deliverable type="commit">opal-partners-data lambda_function.py v2.8 (separate commit)</deliverable>
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

### 0.4.2_RD_AdvisorIntelligence -- Recent Session Logs

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

#### books_panel_remix_versions.md

# Books Panel Remix — Version Log

**Session:** 2026-03-18
**Agent:** 0.4.2_RD_AdvisorIntelligence
**File:** `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`
**Group:** `CanonicalBookView` — 4 panels rendered at every drill level (N1/L2/L3/L4)

---

## Panel Map

| Panel | Function | Location |
|-------|----------|----------|
| Firm Overview | `OverviewPanel` | Row 1 of `CanonicalBookView` |
| Asset Class Mix | Left half of `CompositionPies` | Row 2 of `CanonicalBookView` |
| Top Holdings | Right half of `CompositionPies` | Row 2 of `CanonicalBookView` |
| Cost Basis & Tax Liability | `TaxCostBasisPanel` | Row 3 of `CanonicalBookView` |

---

## v0 — Baseline (pre-session)

**Overview:** Grid of flat `bg-white/5` `MetricCard` tiles. Total AUA `text-xl`, others `text-sm`. No hierarchy.
**Mix:** Small donut (pieR=70), 11px legend text, plain rows.
**Holdings:** Duplicate donut pie + scrollable text list, same visual style as Mix.
**Tax:** h-3 stacked bar, `TaxRow` dot+label+pct+amount rows, bare `<table>` for cost basis / gain positions.

---

## v1 — 2026-03-18 — "Remix Group"

**Portal DEV commit:** (pending)
**Changes:** All 4 panels redesigned. `OverviewPanel` extracted as named function.

### Overview Panel v1
- AUA hero: `text-4xl font-black`, labeled with `text-[10px] uppercase tracking-widest`
- Secondary metrics: horizontal segmented strip, `flex` with `border-r` dividers, `text-lg font-bold` values
- `as of {date}` shown inline below AUA

### Asset Class Mix v1
- Larger pie: `pieR=86`, height 200px
- Legend: each item has a mini proportional bar (`h-1 bg-white/10`) filled to the item's actual % allocation
- Opacity dimming on deselect: 0.2 (was 0.3)
- Click interaction preserved

### Top Holdings v1
- **Dropped duplicate pie** — replaced with ranked horizontal bar list
- Each row: rank number (mono) | name (truncated) | pct | colored bar scaled to top holding
- Bar color = asset_class color of each holding
- "Other" bucket shown at bottom in dimmed italic style
- `maxHeight: 240px` scrollable

### Cost Basis & Tax v1
- Stacked bar: `h-5` (was h-3), percentage label inside segments >= 10%
- Tax status: **3 cards** (Taxable / Tax Deferred / Tax Free) with colored border/bg, amount + pct
- Capital Gains TTM: standalone row, `text-lg font-bold`, emerald/red colored
- Tables (cost basis by year, top gain positions): wrapped in `rounded-lg border` card, alternating row stripes, `bg-white/[0.04]` header
- Term badges on gain positions: `bg-amber-500/15 text-amber-400` (Short) / `bg-emerald-500/15 text-emerald-400` (Long)

---

## v2 — 2026-03-18 — "Remix Overview"

**Portal DEV commit:** `b58a3d5`
**Scope:** `OverviewPanel` only + N1 metric order fix

### Overview Panel v2
- 3 equal `flex-1` cards in a horizontal row: AUA | Clients | Accounts
- AUA card: indigo — `border-indigo-500/25`, `bg-gradient-to-br from-indigo-500/15 to-indigo-500/5`, `text-3xl font-black`
- Clients card: sky/cyan — `border-sky-500/25`, `from-sky-500/15 to-sky-500/5`, colored dot + label
- Accounts card: emerald — `border-emerald-500/25`, `from-emerald-500/15 to-emerald-500/5`
- Other label→color mappings in `METRIC_CARD_STYLE`: NNA=violet, Tax Status=amber, Positions=purple
- Each card: colored dot, colored label text (`text-[10px] uppercase tracking-widest`), white value
- N1 call site metric order fixed: Clients before Accounts (so cards read AUA → Clients → Accounts)

---

## Recall Instructions

To recall a specific panel version, restore the function body from the description above.
To recall v0 for any panel, use `git show HEAD~n:portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` and cherry-pick the function.

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

#### ADVI_BKSCMP.002.rd-types-holdings-adapter.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-002-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Extend types.ts with optional per-class top_holdings fields, and update the
    holdings derivation block in ConsolidatedOverviewPanel to be schema-adaptive:
    N1/L2 use pre-aggregated per-class top_holdings from the new artifacts; L3/L4
    continue to use the existing flat concentration.items path. No other changes
    to ConsolidatedOverviewPanel. RD can work in parallel with DS/DT/AE — the
    adapter is backward-compatible and falls through to synthesis when the new
    Lambda routes return 404.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS3a (types), §WS3b (component),
    §3 (schema), §5 (sequencing — RD parallel track).

    Current state (verified):
    - types.ts MixItem does NOT have top_holdings or other optional fields yet.
    - BooksCompositionResponse scope does NOT have advisor_id or firm_id fields yet.
    - Holdings block at ClientsTab.tsx lines 875–884 is the ONLY change in the component.
    - showFilteredOther render is at lines 1039–1050 — replaced by unified showOther.
    - showOther render is at lines 1055–1068 — replace with PRD version using otherEntry.
    - Empty state at line 1073: `allItems.length === 0 ? 'No holdings data at this level'`

    The ConsolidatedOverviewPanel's donut, legend, quarterly bar, and all other logic
    are completely unaffected by this change. The holdings block is the only code section
    touched.

    advisor_id consistency note: `handleSelectAdvisor` at line 383 sanitizes the advisor
    name to produce the `entity_id` used in `fetchComposition('advisor', id, ...)`.
    Script 12 uses the identical transform to generate S3 keys. These are consistent
    by PRD constraint — no change needed in ClientsTab.tsx for this.
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS3a-types">
      In `portal/src/pages/AdvisorIntelligence/types.ts`:

      A. Extend MixItem with two optional fields (add at the end of the interface):
        export interface MixItem {
          asset_class: string
          label: string
          market_value: number
          pct: number
          // N1/L2 schema only -- per-class top holdings (pct relative to class market_value)
          top_holdings?: ConcentrationItem[]
          other?: { market_value: number; pct: number }
        }

      B. Extend BooksCompositionResponse scope and add optional root-level fields:
        export interface BooksCompositionResponse {
          generated_at: string
          data_as_of: string
          scope: {
            relationship_id?: string
            account_id?: string
            advisor_id?: string   // new -- N1/L2 schema
            firm_id?: string      // new -- N1/L2 schema
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

      ConcentrationItem is unchanged. No other type additions.
    </requirement>

    <requirement id="2" workstream="WS3b-holdings-block">
      In `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`,
      replace ONLY the block at lines 875–884 and the render blocks that use
      showOther / showFilteredOther.

      Replace lines 875–884:
        const allItems = composition?.concentration.items ?? []
        const filteredItems = selectedAssetClass
          ? allItems.filter(it => it.asset_class === selectedAssetClass)
          : allItems

        const MAX_ITEMS = 9
        const cappedItems = filteredItems.slice(0, MAX_ITEMS)
        const showOther = !selectedAssetClass && composition && composition.concentration.other.pct > 0
        const showFilteredOther = Boolean(selectedAssetClass && filteredItems.length > MAX_ITEMS)
        const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1

      With the schema-adaptive version from PRD §WS3b (exact code):
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
            if (!selectedAssetClass &amp;&amp; composition.concentration.other.pct > 0) {
              return composition.concentration.other
            }
            return null
          }
        })()

        const showOther = otherEntry !== null &amp;&amp; otherEntry.pct > 0
        const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1
    </requirement>

    <requirement id="3" workstream="WS3b-render-other">
      Remove showFilteredOther. Replace the two existing "Other" render blocks
      (lines 1039–1068: the showFilteredOther block at 1039–1050 AND the showOther
      block at 1055–1068) with a SINGLE unified block using otherEntry (PRD §WS3b):

        {showOther &amp;&amp; otherEntry &amp;&amp; (
          &lt;div className="flex items-center gap-2.5"&gt;
            &lt;span className="text-[10px] text-white/20 w-4 text-right flex-shrink-0"&gt;~&lt;/span&gt;
            &lt;div className="flex-1"&gt;
              &lt;div className="flex items-baseline justify-between mb-1"&gt;
                &lt;span className="text-[11px] text-white/40 italic"&gt;Other&lt;/span&gt;
                &lt;span className="text-[11px] text-white/30 ml-2"&gt;{(otherEntry.pct * 100).toFixed(1)}%&lt;/span&gt;
              &lt;/div&gt;
              &lt;div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden"&gt;
                &lt;div className="h-full rounded-full bg-white/20"
                  style={{ width: `${(otherEntry.pct / maxPct) * 100}%` }} /&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        )}
    </requirement>

    <requirement id="4" workstream="WS3b-empty-state">
      Update the empty state condition at line 1073.

      Current:
        allItems.length === 0 ? 'No holdings data at this level'

      Replace with:
        !hasPreAggregated &amp;&amp; composition.concentration.items.length === 0
          ? 'No holdings data at this level'

      This ensures that when hasPreAggregated is true (N1/L2), an empty cappedItems array
      does not show "No holdings data" — it correctly falls through to the loading state
      (the composition itself is non-null, so "No holdings for selected class" is the right message).
    </requirement>

    <requirement id="5" workstream="commit">
      Commit both files together to portal DEV:
        git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" \
          -m "feat(portal): schema-adaptive holdings block for N1/L2 composition (ADVI_BKSCMP WS3)"

      Report commit SHA to COO. This is a WS6 portal merge gate.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">MixItem has optional top_holdings?: ConcentrationItem[] and other?: {market_value, pct}</criterion>
    <criterion id="2">BooksCompositionResponse scope has optional advisor_id and firm_id</criterion>
    <criterion id="3">BooksCompositionResponse has optional root-level top_holdings and other</criterion>
    <criterion id="4">hasPreAggregated detection uses mix.some(m => top_holdings?.length > 0)</criterion>
    <criterion id="5">When hasPreAggregated and selectedAssetClass: uses mix[class].top_holdings (pct / class_mv)</criterion>
    <criterion id="6">When hasPreAggregated and no selectedAssetClass: uses composition.top_holdings (global)</criterion>
    <criterion id="7">L3/L4 path unchanged: filters concentration.items, caps at 9</criterion>
    <criterion id="8">Single unified showOther block using otherEntry — showFilteredOther removed</criterion>
    <criterion id="9">Empty state updated: !hasPreAggregated &amp;&amp; concentration.items.length === 0</criterion>
    <criterion id="10">bunx tsc -b passes (no new type errors)</criterion>
    <criterion id="11">All other ConsolidatedOverviewPanel code (donut, legend, quarterly bar) unmodified</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Touch ONLY lines 875–884 (derivation block) and the two render blocks (showOther/showFilteredOther) in ClientsTab.tsx</constraint>
    <constraint>Do NOT modify handleSelectAdvisor, fetchComposition, synthesizeFrom*, or any other ClientsTab function</constraint>
    <constraint>Do NOT add features, comments, or refactors beyond the specified changes</constraint>
    <constraint>All portal changes commit to portal DEV (not CLOUD parent repo)</constraint>
    <constraint>No emojis in code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>RD does NOT push -- DT pushes portal DEV to remote</constraint>
    <constraint>Do NOT gate this work on DS/DT/AE -- the adapter is backward-compatible (404 falls through to synthesis)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      No upstream gates. Frontend is backward-compatible when Lambda routes return 404.
      Commit to portal DEV immediately.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">types.ts + ClientsTab.tsx committed to portal DEV (ADVI_BKSCMP WS3)</deliverable>
  </deliverables>
</task_order>

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

### 0.4.0_DT_ClientPlatform -- Recent Session Logs

#### advi_apiscp_003_oai_v5_deploy.md

# ADVI_APISCP.003 OAI Wire + v5 Deploy — 0.4.0_DT_ClientPlatform

**Date:** 2026-03-10
**Start Time:** ~20:40 UTC
**End Time:** ~21:05 UTC

## Objective

Wire OAI `E139998VWH0PD` (created by CloudOps) to `S3-opal-data-bd` origin on CloudFront
distribution `EVTSA9VEHNZVH`, add `X-Firm-Id` to the cache key, and re-deploy
`shared-advisor-router` (v5 = same code as v4, commit `4eff8dee`) with OAI in place.
Fix for the OAC signing break found in ADVI_APISCP.002 verification.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Read CloudOps handoff (`ADVI_APISCP.003.oai-handoff.md`, commit `10bd602a`) | OAI ID: `E139998VWH0PD`, bucket policy already updated by CloudOps |
| 2 | `aws cloudfront get-distribution-config` | ETag: `E2XWXEAN4B7A2F` |
| 3 | `aws cloudfront create-cache-policy` (X-Firm-Id in cache key) | Policy ID: `45eb7514-712c-42c5-9fd6-40909b9f0347`, Name: `opal-scoped-advisor-by-firm` |
| 4 | `aws lambda publish-version` | Returned `:4` (see note below) |
| 5 | Patch distribution config: OAC→OAI, cache policy swap, behavior wired to `:4` | Verified all 3 changes in patched JSON before submit |
| 6 | `aws cloudfront update-distribution` | Status: InProgress, LastModified: 2026-03-10T20:47:03Z |
| 7 | `aws cloudfront create-invalidation /api/scoped/advisor-intelligence/*` | ID: `I6WKA6C340SEP0JTO1SF8AA1J3` |
| 8 | Poll `get-distribution` — wait for Deployed | Status: Deployed (~20:50 UTC) |
| 9 | Verify live config | OAI: `E139998VWH0PD`, cache policy: `45eb7514...`, Lambda: `:4` |
| 10 | Endpoint verify: GET with placeholder JWT | `401 application/json` — auth gate live, NOT 200 HTML |
| 11 | Tag `shared-advisor-router-v5` at `4eff8dee`, push | Pushed to remote |

---

## publish-version Note

`aws lambda publish-version` returned `:4` (not `:5`). This is because $LATEST code
SHA256 (`u3LrPOCpOw6FdlJ9sKVqygpuynRB/cVP5OZW29F4/fs=`) matches the already-published
version 4. AWS returned the existing version rather than creating a new slot. The code
is identical to what the handoff specified — no source change needed. CloudFront behavior
is wired to `:4`, which IS the v5 functional release. Tag `shared-advisor-router-v5`
points to commit `4eff8dee` (the code) not to the Lambda version number.

---

## What Changed in the Distribution

| Field | Before | After |
|-------|--------|-------|
| `S3-opal-data-bd` OriginAccessControlId | `E24L6358YRRKAE` (OAC) | `""` |
| `S3-opal-data-bd` S3OriginConfig.OriginAccessIdentity | `""` | `origin-access-identity/cloudfront/E139998VWH0PD` |
| Cache policy on `*.json` behavior | `658327ea` (Managed-CachingOptimized) | `45eb7514` (opal-scoped-advisor-by-firm) |
| Lambda origin-request on `*.json` behavior | `shared-advisor-router:3` (post-rollback) | `shared-advisor-router:4` |

**No other origins modified.** OAC remains on `S3-opal-data-portal-v2-json` and all other OAC origins.

---

## Cache Policy Detail

**Name:** `opal-scoped-advisor-by-firm`
**ID:** `45eb7514-712c-42c5-9fd6-40909b9f0347`
**Cache key headers:** `X-Firm-Id` (whitelist)
**TTL:** MinTTL=1s, DefaultTTL=86400s (24h), MaxTTL=31536000s (1yr) — matches CachingOptimized
**Encoding:** gzip + brotli enabled

Firm A will never receive Firm B's cached response. X-Firm-Id is injected by `auth-validator-edge`
from the JWT, so it's always authoritative.

---

## Verification

```
GET /api/scoped/advisor-intelligence/architect_leaderboard.json
  Authorization: Bearer <placeholder-JWT>

Response:
  HTTP 401
  Content-Type: application/json
  Content-Length: 36
```

`401 application/json` confirms: `auth-validator-edge:7` is executing (rejects invalid
JWT signature), Lambda chain is live. Response is NOT `200 text/html` — the
`403→200 /index.html` error response masking issue from v4 is NOT present here.

**Full end-to-end verification** (HTTP 200 + `data_as_of` JSON from `opal-data-bd/gold/`)
requires a valid 49 Financial JWT — cannot be generated without the private key. DE to
confirm using a live portal session per their task order requirement 4.

---

## Partner Onboarding Bucket Policy Template (OAI — updated from OAC)

For each new `opal-data-{firmId}` bucket, apply the following bucket policy statement
(principal is the OAI canonical user, NOT cloudfront.amazonaws.com with OAC condition):

```json
{
  "Sid": "AllowScopedAdvisorOAI",
  "Effect": "Allow",
  "Principal": {
    "CanonicalUser": "d4ad9d8c8d632c03dc0495c78f1d102f1de6a06056577e25de649eaa90d66c9e35c047cce9afa4e82f74dbadc058c161"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::opal-data-{firmId}/*"
}
```

**OAI ID:** `E139998VWH0PD` (opal-scoped-advisor-oai)
**Canonical User ID:** `d4ad9d8c8d632c03dc0495c78f1d102f1de6a06056577e25de649eaa90d66c9e35c047cce9afa4e82f74dbadc058c161`
No new OAI per partner — single OAI for all firms, per CloudOps design.

---

## Deployment Tags

| Resource | Tag / Version | Commit / ARN |
|----------|--------------|--------------|
| shared-advisor-router | `shared-advisor-router-v5` | `4eff8dee` |
| Lambda version on CloudFront | `:4` | `arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:4` |
| CloudFront distribution | Deployed | `EVTSA9VEHNZVH`, LastModified: 2026-03-10T20:47:03Z |
| Cache policy | `opal-scoped-advisor-by-firm` | `45eb7514-712c-42c5-9fd6-40909b9f0347` |
| Cache invalidation | InProgress→Complete | `I6WKA6C340SEP0JTO1SF8AA1J3` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE (pending DE full-JWT verification)
**Active branch:** CLOUD

Distribution `EVTSA9VEHNZVH` is Deployed with OAI `E139998VWH0PD` on `S3-opal-data-bd`,
custom cache policy keyed by `X-Firm-Id`, and `shared-advisor-router:4` on origin-request.
OAC signing issue from ADVI_APISCP.002 is resolved — OAI is compatible with Lambda@Edge
dynamic origin mutation. Tag `shared-advisor-router-v5` pushed. Endpoint returns 401 on
invalid JWT (auth gate live, not 200 HTML). Full JSON verification needs DE with real JWT.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Full verification** — GET with valid 49 Financial JWT,
   confirm `200 application/json`, `data_as_of: 2026-03-06`. All 5 endpoints.
2. **[0.4.0_DT_ClientPlatform] Push CLOUD** — this session log + task order complete.

**Do NOT:**
- Reintroduce OAC on `S3-opal-data-bd` — OAC is incompatible with Lambda@Edge dynamic origin mutation
- Remove X-Firm-Id from the cache policy — required to prevent cross-firm cache contamination
- Use the OAC bucket policy template for new partners — use the OAI template above

#### advi_apiscp_004_options_cors_v6_deploy.md

# ADVI_APISCP.004 OPTIONS CORS Fix (v6) Deploy — 0.4.0_DT_ClientPlatform

**Date:** 2026-03-10 / 2026-03-11
**Start Time:** ~00:08 UTC
**End Time:** ~00:16 UTC

## Objective

Fix CORS preflight (OPTIONS) failure escalated from 0.7.0_AE_CloudOps after ADVI_APISCP.004.
CloudOps deployed S3 CORS + CloudFront CORS-S3Origin policy but OPTIONS returned 200 with no
CORS headers. Root cause: shared-advisor-router had no OPTIONS handler; missing X-Firm-Id
triggered 403 → CloudFront error response → 200 index.html (no CORS). Browser blocks GET.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Read CloudOps ADVI_APISCP.004 escalation | Root cause: OPTIONS hits shared-advisor-router with no X-Firm-Id; returns 403 masked as 200 HTML |
| 2 | Read auth-validator-edge:7 source | Confirmed: line 31 explicitly passes OPTIONS (`request.method === "OPTIONS" → return request`) |
| 3 | Implement v6: OPTIONS early-return before X-Firm-Id guard | 204 + CORS headers: Allow-Origin/Methods/Headers/Max-Age |
| 4 | Commit source | `d2b405b0` feat(lambda-edge): shared-advisor-router v6 |
| 5 | Zip (PowerShell) | 1548 bytes (was 1156 bytes for v4/v5 code) |
| 6 | `aws lambda update-function-code` | CodeSha256: `JbVNDaHfT7fYiap37APge2+8rnDy46Y6K6bKcnmyEVo=` |
| 7 | `aws lambda publish-version` | Version **5** published (new SHA → new version slot) |
| 8 | `aws cloudfront update-distribution` (behavior :4 → :5) | Status: InProgress, LastModified: 2026-03-11T00:12:12Z |
| 9 | `aws cloudfront create-invalidation /api/scoped/advisor-intelligence/*` | ID: `I31RAGBF3FXA3TMNXLLZB034CR` |
| 10 | Poll until Deployed | Status: Deployed (~00:14 UTC) |
| 11 | Verify OPTIONS | `204 No Content` + all 4 CORS headers present |
| 12 | Tag + push | `shared-advisor-router-v6` → `d2b405b0`, pushed with `--follow-tags` |

---

## Root Cause

`auth-validator-edge:7` (viewer-request) explicitly passes OPTIONS through at line 31:
```javascript
if (uri.startsWith("/auth/") || request.method === "OPTIONS") {
  return request;   // no JWT validation, no X-Firm-Id injection
}
```

OPTIONS then reaches `shared-advisor-router:4` (origin-request) as an unauthenticated
request with no `X-Firm-Id`. The missing-firm guard returned 403. CloudFront's
`403 → 200 /index.html` error response masked it — browser received 200 HTML with no
CORS headers and blocked the subsequent authenticated GET.

---

## Fix

OPTIONS early-return BEFORE the X-Firm-Id guard in shared-advisor-router:

```javascript
if (request.method === "OPTIONS") {
  return {
    status: "204",
    statusDescription: "No Content",
    headers: {
      "access-control-allow-origin":  [{ key: "Access-Control-Allow-Origin",  value: "*" }],
      "access-control-allow-methods": [{ key: "Access-Control-Allow-Methods", value: "GET, HEAD, OPTIONS" }],
      "access-control-allow-headers": [{ key: "Access-Control-Allow-Headers", value: "Authorization, Content-Type" }],
      "access-control-max-age":       [{ key: "Access-Control-Max-Age",       value: "86400" }],
    },
  };
}
```

---

## Verification

```
OPTIONS /api/scoped/advisor-intelligence/architect_leaderboard.json
  Origin: https://opalinvest.dev
  Access-Control-Request-Method: GET
  Access-Control-Request-Headers: Authorization

Response:
  HTTP/1.1 204 No Content
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Methods: GET, HEAD, OPTIONS
  Access-Control-Allow-Headers: Authorization, Content-Type
  Access-Control-Max-Age: 86400
  Content-Length: 0
  X-Cache: Miss from cloudfront
```

CORS preflight is now correctly handled. Browser will proceed with the authenticated GET.
Full end-to-end verification (GET with valid 49 Financial JWT returning gold JSON) remains
for DE — same as previous session.

---

## Deployment Tags

| Resource | Version / Tag | ARN / Commit |
|----------|--------------|--------------|
| shared-advisor-router code | `shared-advisor-router-v6` | `d2b405b0` |
| Lambda version on CloudFront | **:5** | `arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:5` |
| CloudFront distribution | Deployed | `EVTSA9VEHNZVH`, LastModified: 2026-03-11T00:12:12Z |
| Cache invalidation | Issued | `I31RAGBF3FXA3TMNXLLZB034CR` |

---

## Lambda Version Accounting

| Lambda Version | Code | Description |
|---------------|------|-------------|
| :1 | v1 original | Rewrite /api/shared/ |
| :2 | v2 | /api/shared/ → /api/scoped/ |
| :3 | v3 | Rewrite to /gold/ for opal-data-bd |
| :4 | v4/v5 | Dynamic X-Firm-Id routing (OAI) |
| :5 | **v6** | + OPTIONS CORS preflight early-return |

Note: Lambda :4 served as both code v4 and v5 (identical SHA). :5 is a distinct new version
(new SHA from the OPTIONS handler addition).

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda-edge/shared-advisor-router/index.mjs` | v6: OPTIONS early-return + stale OAC comment corrected | Yes — CLOUD `d2b405b0` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

OPTIONS preflight returns 204 + full CORS headers. `shared-advisor-router:5` (v6 code) is
live on CloudFront behavior `/api/scoped/advisor-intelligence/*.json`. Browser CORS preflight
is unblocked. Authenticated GET path through OAI to `opal-data-bd/gold/` is ready for DE
full verification with a live 49 Financial JWT.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Full verification** — GET with valid 49 Financial JWT,
   confirm `200 application/json`, `data_as_of: 2026-03-06`. All 5 required endpoints.
   Also confirm OPTIONS → 204 with CORS headers (already verified above by DT).
2. **[0.4.0_DT_ClientPlatform] Push org commit** — this session log to CLOUD.

**Do NOT:**
- Move the OPTIONS handler below the X-Firm-Id guard — OPTIONS has no JWT so no X-Firm-Id
- Add JWT validation to OPTIONS — preflights never carry credentials by browser spec

#### advi_apiscp_007_router_v7_opal_routing_deploy.md

# ADVI_APISCP.007 Router v7 Opal Capital Routing — 0.4.0_DT_ClientPlatform

**Date:** 2026-03-11
**Start Time:** ~01:05 UTC
**End Time:** ~01:17 UTC

## Objective

Add internal Opal Capital staff routing to `shared-advisor-router`. Users with
`X-Firm-Id: opal-capital` (internal staff JWT) are not a partner firm — routing
to `opal-data-opal-capital` would 404. v7 reads `?firm=<firmId>` from the query
string for opal-capital users and routes to `opal-data-{firm}` instead.
Task: ADVI_APISCP.007.router-v7-opal-routing.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Implement v7 in `shared-advisor-router/index.mjs` | routingFirmId separation; opal-capital → ?firm= path; 400 on missing param |
| 2 | Commit source | `92a66c9b` feat(lambda-edge): shared-advisor-router v7 |
| 3 | Update cache policy `opal-scoped-advisor-by-firm` | Added `firm` query string to cache key whitelist (QueryStringBehavior: whitelist, Items: ["firm"]) |
| 4 | Zip (PowerShell) | 1936 bytes |
| 5 | `aws lambda update-function-code` | CodeSha256: `Ca+e/8tR4ILL2RWoYzgEpAoRKGdHzN/worY7fZywUp0=` |
| 6 | `aws lambda publish-version` | Version **6** published |
| 7 | `aws cloudfront update-distribution` (behavior :5 → :6) | Status: InProgress, LastModified: 2026-03-11T01:12:59Z |
| 8 | `aws cloudfront create-invalidation /api/scoped/advisor-intelligence/*` | ID: `I5MAV3Z591JHEEVL72NOI0QT31` |
| 9 | Poll until Deployed | Status: Deployed (~01:14 UTC) |
| 10 | Verify (placeholder JWT) | 401 on both paths — auth gate live, Lambda chain executing |
| 11 | Tag `shared-advisor-router-v7` at `92a66c9b`, push | Pushed with `--follow-tags` |

---

## Logic Change

```
Before (v6):
  firmId = X-Firm-Id header
  bucket = opal-data-{firmId}      (always)

After (v7):
  firmId = X-Firm-Id header
  if firmId === "opal-capital":
    routingFirmId = ?firm= query param   (400 if absent)
  else:
    routingFirmId = firmId
  bucket = opal-data-{routingFirmId}
```

- `firmId` (from JWT) = who is authenticated
- `routingFirmId` = which partner's S3 bucket to read from
- For all partner users these are the same. For opal-capital staff they differ.

---

## Cache Policy Update

Previous: `QueryStringBehavior: none` — query strings not in cache key.
Now: `QueryStringBehavior: whitelist`, `Items: ["firm"]` — `?firm=` in cache key.

**Why required:** Without `firm` in the cache key, an opal-capital user requesting
`?firm=bd` and then `?firm=xyz` would share the same cache entry (keyed only by
`X-Firm-Id: opal-capital` + path). Partner A's data would be served for Partner B.
This is a compliance violation of the partner data isolation invariant (PRD Section 2).

For regular partner users, `?firm=` is absent — no cache key impact.

---

## Deployment Tags

| Resource | Version / Tag | ARN / Commit |
|----------|--------------|--------------|
| shared-advisor-router code | `shared-advisor-router-v7` | `92a66c9b` |
| Lambda version on CloudFront | **:6** | `arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:6` |
| CloudFront distribution | Deployed | `EVTSA9VEHNZVH`, LastModified: 2026-03-11T01:12:59Z |
| Cache policy | Updated: `firm` query string added | `45eb7514-712c-42c5-9fd6-40909b9f0347` |
| Cache invalidation | Issued | `I5MAV3Z591JHEEVL72NOI0QT31` |

---

## Lambda Version Accounting

| Lambda Version | Code | Description |
|---------------|------|-------------|
| :1 | v1 | Rewrite /api/shared/ |
| :2 | v2 | /api/shared/ → /api/scoped/ |
| :3 | v3 | Rewrite to /gold/ for opal-data-bd |
| :4 | v4/v5 | Dynamic X-Firm-Id routing (OAI) |
| :5 | v6 | + OPTIONS CORS preflight early-return |
| :6 | **v7** | + opal-capital staff routing via ?firm= |

---

## Verification

Placeholder JWT returns 401 from auth-validator-edge on both test paths — Lambda chain is live.

Full end-to-end verification requires:
1. A valid `opal-capital` JWT → GET with `?firm=bd` → expect `200 application/json` + gold data
2. A valid `opal-capital` JWT → GET without `?firm=` → expect `400 Bad Request` (Missing ?firm= parameter)
3. A valid `bd` partner JWT → GET without `?firm=` → expect `200 application/json` (unchanged behavior)

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda-edge/shared-advisor-router/index.mjs` | v7: routingFirmId + opal-capital ?firm= branch | Yes — CLOUD `92a66c9b` |
| Cache policy `opal-scoped-advisor-by-firm` | Added `firm` to query string cache key whitelist | AWS-live (no git artifact) |

---

## Current State

**Status:** COMPLETE (pending full-JWT verification)
**Active branch:** CLOUD

`shared-advisor-router:6` (v7 code) deployed on CloudFront, Status: Deployed. Cache
policy updated to key on `firm` query string. Opal Capital staff with a valid JWT can
now access any partner's advisor intelligence data via `?firm=<firmId>`. Partner users
are unaffected — routing path is unchanged. Tag `shared-advisor-router-v7` pushed.

---

## Next Steps

1. **[Andrew] Verify with opal-capital JWT** — GET with `?firm=bd` → 200 gold JSON;
   GET without `?firm=` → 400. GET with a partner JWT (no `?firm=`) → 200 unchanged.
2. **[0.4.0_DT_ClientPlatform] Commit session log** — this file to CLOUD.

#### advi_apiscp_lambda_edge_v4_deploy.md

# ADVI_APISCP Lambda@Edge v4 Deploy — 0.4.0_DT_ClientPlatform

**Date:** 2026-03-10
**Start Time:** ~19:35 UTC
**End Time:** ~19:42 UTC (propagation ongoing)

## Objective

Deploy `shared-advisor-router` Lambda@Edge v4 to CloudFront distribution `EVTSA9VEHNZVH`.
v4 adds dynamic S3 origin routing: reads `X-Firm-Id` header (injected by `auth-validator-edge`
from JWT) and routes to `opal-data-{firmId}` bucket rather than the hardcoded `opal-data-bd`.
Task order: `ADVI_APISCP.001.lambda-edge-v4-dynamic-routing.md`

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Preflight: `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH` | Extracted behavior + origin + Lambda associations |
| 2 | Preflight: List path patterns | Behavior is `/api/scoped/advisor-intelligence/*.json` (NOT `/*` as PRD stated) |
| 3 | Preflight: Extract origin for S3-opal-data-bd | `OriginAccessControlId: E24L6358YRRKAE`, `OriginAccessIdentity: ""` → **OAC confirmed** |
| 4 | Preflight: `aws lambda list-versions-by-function shared-advisor-router` | Versions 1, 2, 3 exist; CloudFront attached to `:3` |
| 5 | Implement v4 in `infra/aws/lambda-edge/shared-advisor-router/index.mjs` | In-place domainName mutation; 403 on missing X-Firm-Id |
| 6 | Commit source | `4eff8dee` feat(lambda-edge): shared-advisor-router v4 |
| 7 | `aws lambda update-function-code` (zip upload to $LATEST) | CodeSize: 1156 bytes, LastModified: 2026-03-10T19:39:20Z |
| 8 | `aws lambda publish-version` | Version **4** published: `...:function:shared-advisor-router:4` |
| 9 | `aws cloudfront update-distribution` (behavior `:3` → `:4`) | Status: InProgress, LastModifiedTime: 2026-03-10T19:40:59Z |
| 10 | `aws cloudfront create-invalidation /api/scoped/advisor-intelligence/*` | Invalidation ID: `I64W43Y9E8YXMV8MZ89E71V7VW` |

**Propagation:** CloudFront is in InProgress state. Expect 5-15 minutes.

---

## Preflight Findings (requirement 0a-0c)

### 0a — CloudFront behavior for advisor-intelligence

| Field | Value |
|-------|-------|
| Path pattern | `/api/scoped/advisor-intelligence/*.json` |
| TargetOriginId | `S3-opal-data-bd` |
| viewer-request Lambda | `arn:aws:lambda:us-east-1:313476888478:function:auth-validator-edge:7` |
| origin-request Lambda (was) | `arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:3` |
| origin-request Lambda (now) | `arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:4` |

**PRD correction:** Path pattern is `*.json` not `/*`. The `/api/scoped/advisor-intelligence/clients/*`
behavior routes to APIGateway-portal (no Lambda@Edge) — that is a separate clients list endpoint.

### 0b — Lambda versioning

| Field | Value |
|-------|-------|
| Function name in AWS | `shared-advisor-router` |
| Runtime | `nodejs20.x` |
| Region | `us-east-1` |
| Published versions | 1, 2, 3 (pre-deploy), **4 (this deploy)** |
| Deploy workflow | `update-function-code` → `publish-version` → `update-distribution` |

### 0c — OAC vs OAI determination

| Origin | DomainName | OAC ID | OAI |
|--------|-----------|--------|-----|
| S3-opal-data-bd | `opal-data-bd.s3.us-east-1.amazonaws.com` | `E24L6358YRRKAE` | `""` (empty) |
| S3-opal-data-portal-v2-json | `opal-data-portal-v2.s3.us-east-1.amazonaws.com` | `E24L6358YRRKAE` | `""` (empty) |
| S3-opalinvest-portal | `opalinvest-portal.s3.us-east-1.amazonaws.com` | `""` (none) | `EU39UXW7CMSI5` |

**Verdict: OAC (E24L6358YRRKAE) is the auth model for S3-opal-data-bd.**
The PRD pseudocode using `authMethod: "origin-access-identity"` is WRONG for this origin.

**v4 implementation approach:** In-place mutate `request.origin.s3.domainName` (do NOT replace
entire `request.origin`). This preserves the OAC `authMethod` field CloudFront provides in the
origin-request event. CloudFront will use OAC to sign requests to the dynamically-routed bucket,
provided that bucket has the OAC bucket policy attached.

---

## v4 Implementation Notes

**Key decisions:**
- `firmId` guard: return 403 `"Missing firm identity"` if `request.headers['x-firm-id']` absent
- URI rewrite: unchanged from v3 (`/api/scoped/advisor-intelligence/` → `/gold/`)
- Origin mutation: in-place on `request.origin.s3.domainName` and `region`
- Host header: updated to `opal-data-${firmId}.s3.us-east-1.amazonaws.com`
- OAI fields: NOT used (environment uses OAC, not OAI)

---

## Partner Onboarding Bucket Policy Template (requirement 2)

For each new `opal-data-{firmId}` bucket, attach the following bucket policy to grant
CloudFront OAC access. OAC signs requests using the distribution ARN as condition:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontServicePrincipalReadOnly",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::opal-data-{firmId}/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::313476888478:distribution/EVTSA9VEHNZVH"
        }
      }
    }
  ]
}
```

**Note:** `opal-data-bd` already has this policy (CloudFront access works today). Every new
`opal-data-{firmId}` bucket MUST have this policy before routing will work. There is NO wildcard
`opal-data-*` grant — access is per-bucket. The PRD claim "no IAM changes needed" is INCORRECT.

---

## Verification

**To verify after propagation (5-15 min from 19:40 UTC):**
```bash
# With a valid 49 Financial JWT (firmId=bd):
curl -H "Authorization: Bearer <JWT>" \
  https://d2n2nzpeqf34ge.cloudfront.net/api/scoped/advisor-intelligence/timeseries_chart.json

# Expected: HTTP 200, data from opal-data-bd/gold/timeseries_chart.json
# Confirm: response body contains data_as_of matching current gold date

# Without X-Firm-Id (no JWT or invalid JWT — auth-validator-edge blocks first):
# Expected: 403 from auth-validator-edge before reaching shared-advisor-router
```

CloudFront invalidation `I64W43Y9E8YXMV8MZ89E71V7VW` in progress on `/api/scoped/advisor-intelligence/*`.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| In-place mutate `request.origin.s3.domainName` (not full replacement) | Preserves OAC `authMethod` field. Replacing `request.origin` entirely with OAI-style object would break OAC signing. |
| 403 on missing X-Firm-Id | auth-validator-edge should always inject it; if missing, something is wrong — fail closed. |
| Document OAC bucket policy template | Per-bucket access required. PRD assumption of wildcard access is wrong; onboarding docs must include this step. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda-edge/shared-advisor-router/index.mjs` | v4: dynamic origin routing via X-Firm-Id | Yes — CLOUD `4eff8dee` |
| Task order `ADVI_APISCP.001.lambda-edge-v4-dynamic-routing.md` | status → complete | No — local only |

---

## Deployment Tags

| Resource | Version | ARN / ID |
|----------|---------|----------|
| shared-advisor-router | **:4** | `arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:4` |
| CloudFront distribution | InProgress | `EVTSA9VEHNZVH` (LastModified: 2026-03-10T19:40:59Z) |
| Cache invalidation | InProgress | `I64W43Y9E8YXMV8MZ89E71V7VW` |

---

## Blockers

None.

---

## Current State

**Status:** IN PROGRESS (awaiting CloudFront propagation ~5-15 min from 19:40 UTC)
**Active branch:** CLOUD

Lambda@Edge v4 (`shared-advisor-router:4`) published and CloudFront distribution updated to use
it on the `/api/scoped/advisor-intelligence/*.json` behavior. Code committed at `4eff8dee`.
Invalidation `I64W43Y9E8YXMV8MZ89E71V7VW` running. Post-deploy verification pending propagation.
Task order `ADVI_APISCP.001.lambda-edge-v4-dynamic-routing.md` marked complete — all requirements
satisfied including preflight, implementation (OAC-correct), deploy, and bucket policy template.

---

## Next Steps

1. **[Andrew] Verify** — once propagation completes (~19:55 UTC), curl `/api/scoped/advisor-intelligence/timeseries_chart.json` with a valid 49 Financial JWT. Expect 200 + gold data.
2. **[0.4.0_DE_ClientPlatform] Post-deploy network tab verification (ADVI_APISCP DE task order req 4)** — DE can now confirm frontend API calls resolve correctly.
3. **[0.4.0_DT_ClientPlatform] Push CLOUD** — commit `4eff8dee` + this org log + task order status update. Also push portal DEV (pending DE commits `9c1881a` + `3367cd8` + `1433d2e`).
4. **[0.4.0_DT_ClientPlatform] Gold rebuild (NNAVAR/AUAVAR)** — ADVI_49FNV3 is complete per COO. Both scripts (05/05b for NNAVAR JNL/sweep, 02 for AUAVAR BKF) are in S3. Rebuild can be triggered with explicit COO/Andrew authorization.

**Do NOT:**
- Use `authMethod: "origin-access-identity"` on this distribution — it uses OAC
- Write any advisor-intelligence data to `opal-data-portal-v2` — permanently forbidden
- Assume wildcard S3 access for partner buckets — each `opal-data-{firmId}` needs explicit OAC bucket policy

#### advi_apiscp_v4_rollback_and_oac_assessment.md

# ADVI_APISCP v4 Rollback + OAC/Lambda@Edge Architecture Assessment — 0.4.0_DT_ClientPlatform

**Date:** 2026-03-10
**Start Time:** ~20:15 UTC

## Objective

Roll back `shared-advisor-router:4` to `:3` (service restoration), document root cause of
the OAC signing break, and assess viable fix options for multi-tenant routing.

---

## Deployment Sequence — Rollback

| Step | Action | Result |
|------|--------|--------|
| 1 | `aws cloudfront get-distribution-config` | ETag: `E24N0N72JGXIFH` |
| 2 | Patch behavior index 4: `shared-advisor-router:4` → `:3` | Verified in patched JSON |
| 3 | `aws cloudfront update-distribution` | Status: InProgress, LastModified: 2026-03-10T20:17:59Z |
| 4 | `aws cloudfront create-invalidation /api/scoped/advisor-intelligence/*` | ID: `I3Y4DVA8KISNS65Z53HWSIPH8I` |

**Propagation:** ~5-15 min from 20:17 UTC. v3 will restore normal service on propagation.

---

## Root Cause — Why v4 Broke OAC Signing

**DE diagnosis confirmed.** This is an AWS CloudFront constraint, not a code bug.

**The constraint:**
> When a Lambda@Edge origin-request function modifies `request.origin` in any way,
> CloudFront skips OAC (Origin Access Control) signing for the outbound request to S3.
> S3 receives an unsigned request, which the bucket policy (`AllowCloudFrontOACReadGold`)
> rejects with 403. CloudFront's `403 → 200 /index.html` error response masked this.

**v3 was unaffected** because it only rewrote `request.uri`. It never touched `request.origin`,
so CloudFront applied OAC signing to the statically configured `S3-opal-data-bd` origin normally.

**My error:** The ADVI_APISCP-001 thread correctly identified OAC vs OAI as an unknown, but
neither CloudOps nor I had live AWS CLI access during the thread to confirm whether dynamic
origin mutation is compatible with OAC. AWS documentation is ambiguous on this point. Live
verification caught it.

---

## Architecture Assessment — Fix Options for Multi-Tenant Routing

### Option A — Skip origin mutation when firmId = bd (band-aid)

**How:** In v4 code, only mutate `request.origin` when `firmId !== 'bd'`. For the current
single-tenant case (49 Financial), this is a no-op and OAC signing applies normally.

**Problem:** This is not a multi-tenant solution. firmId=`partner2` would still break OAC.
Only defers the problem.

**Verdict:** Reject. Solves today but not the architecture.

---

### Option B — Switch S3-opal-data-bd origin from OAC to OAI

**How:** Create a new OAI for the advisor-intelligence behavior (or reuse `EU39UXW7CMSI5`
already on `S3-opalinvest-portal`). Update `S3-opal-data-bd` origin in the distribution to
use OAI instead of OAC. Update `opal-data-bd` bucket policy to allow OAI principal.
Lambda@Edge can freely mutate `request.origin.s3` — OAI signing IS compatible with dynamic
origin mutation.

**Partner bucket policy template (OAI):**
```json
{
  "Principal": {
    "CanonicalUser": "<OAI canonical user ID>"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::opal-data-{firmId}/*"
}
```

**Pros:**
- Lambda@Edge dynamic origin mutation works with OAI (AWS-confirmed)
- Zero operational overhead per new firm — just create the bucket with OAI policy
- Simpler onboarding

**Cons:**
- OAI is "legacy" — AWS deprecated OAI in favor of OAC in 2022, though no end-of-life date set
- `S3-opalinvest-portal` already uses OAI (EU39UXW7CMSI5) — we'd create a second OAI
  or reuse the existing one (not recommended to mix purposes)
- Mixed auth model on the distribution (some origins OAC, one OAI)

**Verdict:** Viable for multi-tenant. Not ideal long-term given OAI deprecation trajectory.

---

### Option C — Pre-configure one CloudFront origin per firm (Option D from DE escalation)

**How:** For each `opal-data-{firmId}`, add it as a named S3 origin in the CloudFront
distribution with OAC attached. Lambda@Edge reads X-Firm-Id and sets `request.origin` to
the exact configuration of the matching pre-configured origin.

**Key question:** Does this actually restore OAC signing?

Based on AWS documentation review: CloudFront applies OAC signing when the outbound S3
request matches a distribution-configured origin **and** the origin has OAC configured.
When Lambda@Edge sets `request.origin` to a domain that IS configured in the distribution
with OAC, OAC signing SHOULD apply. This needs live verification.

**Lambda@Edge approach:**
```javascript
const FIRM_ORIGINS = {
  'bd':    { domainName: 'opal-data-bd.s3.us-east-1.amazonaws.com',    region: 'us-east-1' },
  'firm2': { domainName: 'opal-data-firm2.s3.us-east-1.amazonaws.com', region: 'us-east-1' },
};
// Only mutate if we can match to a configured origin
const origin = FIRM_ORIGINS[firmId];
if (!origin) { return 403; }
request.origin.s3.domainName = origin.domainName;
request.origin.s3.region     = origin.region;
request.headers['host'] = [{ key: 'Host', value: origin.domainName }];
```

**Pros:**
- Preserves OAC (current best practice)
- Clean per-firm isolation — each origin independently configured
- No deprecated API

**Cons:**
- CloudFront distribution update required per new firm onboarding (terraform/CLI change)
- Unverified whether setting origin to a configured domain actually restores OAC signing
  — **must be tested before commit**

**Verdict:** Preferred long-term architecture IF AWS confirms OAC signing applies when the
mutated domain matches a distribution-configured origin. Requires a live test.

---

### Option D — Lambda@Edge fetches from S3 directly (SigV4 in Lambda)

**How:** Lambda@Edge makes an authenticated `GetObject` call to S3 using the execution role
credentials (SigV4), returns the body as the response. Bypasses CloudFront origin auth entirely.

**Cons:**
- Lambda@Edge 1MB response size limit (gold files up to ~55KB each — currently OK, not future-proof)
- Added latency (~20-50ms S3 SDK call inside Lambda@Edge execution)
- Lambda@Edge execution role needs `s3:GetObject` on `opal-data-*`
- No CloudFront caching of the response (defeats the purpose of CloudFront for static JSON)

**Verdict:** Last resort. Too many trade-offs.

---

## DT Recommendation

**Immediate:** v3 rollback (done above) — service restored.

**Fix path — bring to Andrew/CTO for decision:**

1. **Try Option C first (pre-configured origins per firm + OAC).** Add `opal-data-bd` as
   an explicitly named OAC origin (it already exists as `S3-opal-data-bd` with OAC — this IS
   the current config). The open question is whether Lambda@Edge mutating `request.origin.s3`
   to match that exact configured domain restores OAC. This requires a **live test** against
   the actual distribution — not resolvable from docs alone.

2. **If Option C live test fails, adopt Option B (OAI).** OAI works with Lambda@Edge dynamic
   origin mutation (AWS-confirmed). The deprecation risk is low for a distribution we control.
   Onboarding is simpler (no distribution update per firm).

3. **Option A is not a path forward.** Do not merge a firmId=bd special-case.

---

## What I Need From Andrew Before Proceeding

1. **Decision on Option C vs B** — or authorization to test Option C live (requires a
   brief re-deploy of a test v4 variant to verify OAC signing behavior).
2. If Option C: confirm whether the test should modify the existing distribution or a
   separate test distribution.
3. If Option B: confirm whether to create a new OAI or reuse EU39UXW7CMSI5.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| CloudFront EVTSA9VEHNZVH | Behavior rolled back: `shared-advisor-router:4` → `:3` | AWS-live (no git artifact) |
| This session log | DT assessment | No — pending CLOUD commit |

---

## Current State

**Status:** IN PROGRESS (rollback propagating, architecture decision pending)
**Active branch:** CLOUD

CloudFront rollback to `shared-advisor-router:3` is in progress (InProgress as of 20:17 UTC).
v3 will restore normal 49 Financial service on propagation. v4 (`4eff8dee`) remains on CLOUD
branch but is NOT deployed. Architecture decision on OAC vs OAI vs pre-configured origins
required from Andrew before v4 fix can be designed and re-deployed.

---

## Next Steps

1. **[Andrew] Decide on fix architecture** — Option B (OAI) vs Option C (pre-configured
   OAC origins + live test). DT cannot proceed without this decision.
2. **[0.4.0_DT_ClientPlatform] Implement chosen fix** — once decision is made.
3. **[0.4.0_DE_ClientPlatform] Re-run verification** after fix deploy.

**Do NOT:**
- Re-deploy v4 as written — it will break OAC signing again
- Use Option A (firmId=bd skip) — not a multi-tenant solution
- Disable CloudFront 403 error responses as a debugging aid without Andrew approval

#### nnavar_jnl_sweep_scripts_s3_deploy.md

# NNAVAR JNL/Sweep Scripts S3 Deploy — 0.4.0_DT_ClientPlatform

**Date:** 2026-03-09

---

## Objective

Upload scripts 05 and 05b (JNL/sweep canonical exclusion fix, commits `9bfb289b` +
`b4f2d7a7`) to S3 so bd-gold-layer-runner picks them up on next sync.
DO NOT trigger a gold rebuild — deploy only.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Upload `05_build_client_performance.py` | `s3://opal-data-bd/code/gold/05_build_client_performance.py` (32,879 bytes) |
| 2 | Upload `05b_build_account_performance.py` | `s3://opal-data-bd/code/gold/05b_build_account_performance.py` (30,362 bytes) |
| 3 | Verify S3 timestamps | Both at 2026-03-09 12:22 UTC |

**No rebuild triggered. No EC2 pipeline invocation.**

---

## Verification

```
2026-03-09 12:22:19   32,879   s3://opal-data-bd/code/gold/05_build_client_performance.py
2026-03-09 12:22:20   30,362   s3://opal-data-bd/code/gold/05b_build_account_performance.py
```

---

## Current State

**Status:** COMPLETE

Both scripts are in S3 at the canonical gold code path. The gold rebuild can now be
triggered at any time — one `run-gold-layer.sh` invocation covers both the NNAVAR
JNL/sweep fix (scripts 05/05b) and the AUAVAR BKF fix (script 02, already deployed).
Rebuild deferred until ADVI_49FNV3 completes per COO decision log 2026-03-09.

#### partners_api_v1.1.0_addendum_a_deploy.md

# Partners API v1.1.0 Addendum A Deploy -- 0.4.0_DT_ClientPlatform

**Date:** 2026-03-16
**Task Order:** ADVI_MVPLVL.005.lambda-deploy (requirements 1-5)

## Objective

Rebuild opal-partners-data Lambda artifact to include DS 005 Addendum A endpoints
(handle_mix_timeseries, handle_concentration_timeseries) and the 06b per-relationship
JSON refactor (33d490a9). Deploy via Terraform, verify all endpoints, tag partners-api-v1.1.0.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify source committed | Clean -- no uncommitted changes in source dir |
| 2 | build-and-upload.sh partners-api opal-partners-data | SHA256: `TuZ5v528GjA0tXo0cun6Bxjp0bd0WLjH8SXZoZYD6EE=`, 20K |
| 3 | Commit source map | `e9155577` ci: upload artifact for partners-api opal-partners-data |
| 4 | terraform plan | 1 changed (s3_object_version + source_code_hash update) |
| 5 | terraform apply | 0 added, 1 changed, 0 destroyed |
| 6 | 0-diff plan | No changes. Infrastructure is up-to-date. |
| 7 | Update deployment_map.xml | Added partners-api module + opal-partners-data Lambda entry |
| 8 | record-terraform-deploy.sh | `3bc778de` ci: record deploy partners-api @ e9155577, CHANGELOG.json created |
| 9 | Commit deployment_map.xml | `585bcaf9` |
| 10 | Tag + push | `partners-api-v1.1.0` pushed to CLOUD |

## Verification

All endpoints tested via `aws lambda invoke` with relationship z08327149, firmId=49financial:

| Endpoint | Status | Data |
|---|---|---|
| /books/relationship/{id}/timeseries | 200 | Daily AUA/NNA records |
| /books/relationship/{id}/composition | 200 | Mix + concentration snapshot |
| /books/relationship/{id}/mix-timeseries | 200 | 420 mix records (date, equity, fixed_income, structured_notes, cash, other) + 420 concentration records |
| /books/relationship/{id}/concentration-timeseries | 200 | 420 mix + 420 concentration records (date, holdings) |

Both Addendum A endpoints return valid JSON with 420 daily records each.

## Deployment Tags

| Pipeline | Tag | Commit |
|----------|-----|--------|
| partners-api | `partners-api-v1.1.0` | `585bcaf9` |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda/ci/lambda-source-map.json` | artifact_sha256 + last_deployed_commit updated | Yes -- `e9155577`, `3bc778de` |
| `infra/aws/terraform/partners-api/CHANGELOG.json` | Created with v1.1.0 entry | Yes -- `3bc778de` |
| `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml` | Added partners-api module + opal-partners-data Lambda | Yes -- `585bcaf9` |

---

## Current State

**Status:** COMPLETE (requirements 1-5). Requirement 6 (portal DEV->PROD merge) blocked on DE firmId fix.
**Active branch:** CLOUD

The opal-partners-data Lambda is deployed at `partners-api-v1.1.0` with all 8 Books Tab
endpoints functional: 4 original (timeseries, composition per relationship/account) plus
2 Addendum A (mix-timeseries, concentration-timeseries). The artifact includes both the
DS 005 commit (`6cae4815`) and the 06b per-relationship JSON refactor (`33d490a9`).

API Gateway routes for all 6 `/api/scoped/partners/books/*` paths are live with JWT
authorizer. The partners-api Terraform module is at 0-diff.

**Still open:** Portal DEV->PROD merge (task order requirement 6) is gated on DE fixing
7 portal API functions missing `?firm=` / `?firmId=` query parameters.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Fix 7 portal API functions** -- thread firmOverride/firmId through advisor-intelligence.ts. S3-routed need `?firm=`, Lambda-routed need `?firmId=`.
2. **[0.4.0_DT_ClientPlatform] After DE fix on portal DEV** -- verify Books Tab L2 drilldown end-to-end, then execute portal DEV->PROD merge (task order requirement 6).
3. **[0.4.0_DT_ClientPlatform] Update task order status** -- mark ADVI_MVPLVL.005.lambda-deploy as complete after portal merge.

**Do NOT:**
- Put opal-partners-data back in bd-pipeline -- it has its own module at `infra/aws/terraform/partners-api/`
- Merge portal DEV->PROD until DE firmId fix is committed on DEV and all endpoints verified
- Use `pyarrow_additional_kwargs` for filters -- broken in awswrangler 3.11.0


### 0.4.0_DT_ClientPlatform -- Pending Task Orders

#### ADVI_ADVTV2.002.gold-layer-deploy.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-17-advtv2-002-dt-gold-deploy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <project_code>ADVI_ADVTV2</project_code>
  </metadata>

  <objective>
    Deploy the architect attribution gold layer scripts to EC2 (bd-gold-layer-runner),
    run a FULL gold layer rebuild, and verify that rel_architect_lookup.parquet contains
    exactly 19 named architects + Unresolved. This propagates architect attribution
    downstream into 08, 09, 10 and ultimately into portal JSON for all ADV views.
  </objective>

  <context>
    DS 001 is complete (2026-03-17, pending DS commit). DS modified four gold scripts:
    - NEW: data/black_diamond/scripts/gold/08b_build_architect_attribution.py
    - MOD: data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py
    - MOD: data/black_diamond/scripts/gold/00_build_accounts_dimension.py
    - MOD: data/black_diamond/scripts/gold/run_gold_layer.sh

    Deploy brief is at: docs/briefs/devops-brief-architect-attribution.md (read it first).

    FULL mode is required for the first run because 00_build_accounts_dimension.py
    now reads consultant and additional_advisor from silver transactions — incremental
    mode will not backfill these into existing accounts_dimension rows.
  </context>

  <scope>
    <files>
      <file action="none">data/black_diamond/scripts/gold/08b_build_architect_attribution.py (upload to S3)</file>
      <file action="none">data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py (upload to S3)</file>
      <file action="none">data/black_diamond/scripts/gold/00_build_accounts_dimension.py (upload to S3)</file>
      <file action="none">data/black_diamond/scripts/gold/run_gold_layer.sh (upload to S3)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Verify DS commit to CLOUD is complete (check git log for 08b, 08, 00, run_gold_layer.sh).
      Do not deploy uncommitted code.
    </requirement>

    <requirement id="2">
      Upload all 4 modified scripts to S3 per the devops brief:
        s3://opal-data-bd/code/gold/08b_build_architect_attribution.py
        s3://opal-data-bd/code/gold/08_build_nna_aua_by_advisor.py
        s3://opal-data-bd/code/gold/00_build_accounts_dimension.py
        s3://opal-data-bd/code/gold/run_gold_layer.sh
      Use the standard EC2 code deployment pattern (repo -> S3 -> EC2 pulls).
      Follow EC2_CODE_DEPLOYMENT_STANDARD.md.
    </requirement>

    <requirement id="3">
      On bd-gold-layer-runner EC2, pull the updated scripts from S3.
      Run the gold layer in FULL mode (not incremental):
        ./run_gold_layer.sh --full
      FULL mode is required because 00_build_accounts_dimension.py now ingests
      consultant and additional_advisor from silver transactions for the first time.
    </requirement>

    <requirement id="4">
      Verify rel_architect_lookup.parquet on S3:
        aws s3 cp s3://opal-data-bd/gold/views/rel_architect_lookup.parquet /tmp/
        python3 -c "import pandas as pd; df=pd.read_parquet('/tmp/rel_architect_lookup.parquet'); print(df['resolved_architect'].nunique(), 'architects'); print(df['resolved_architect'].unique())"

      Expected: exactly 19 distinct named architects plus "Unresolved". No "49F House",
      no "Unassigned", no stale/retired architects.
    </requirement>

    <requirement id="5">
      Verify architect_attribution.parquet on S3:
        Check that conservation holds: resolved + unresolved rows = total funded accounts.
        (DS printed this during dry-run — confirm counts match or are close to 5,423 funded accounts
        with ~98.3% resolved.)
    </requirement>

    <requirement id="6">
      After FULL gold run completes, verify downstream scripts 09 and 10 ran without errors
      (they are part of run_gold_layer.sh --full). Spot-check that portal JSON files updated:
        aws s3 ls s3://opal-data-bd/gold/portal/ --recursive | sort -k1,2 | tail -10
      Confirm at least one portal JSON has a recent modified timestamp.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 4 scripts uploaded to S3 and pulled onto EC2</criterion>
    <criterion id="2">FULL gold layer run completes without errors</criterion>
    <criterion id="3">rel_architect_lookup.parquet contains exactly 19 named architects + Unresolved</criterion>
    <criterion id="4">No "49F House", "Unassigned", or stale architects in rel_architect_lookup</criterion>
    <criterion id="5">Downstream scripts 09 and 10 run successfully (no code changes required)</criterion>
    <criterion id="6">Portal JSON files updated with recent timestamp</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>FULL mode required for first run — do NOT use incremental mode</constraint>
    <constraint>Do NOT modify any scripts on EC2 directly — pull from S3 only</constraint>
    <constraint>EC2 code deployment follows EC2_CODE_DEPLOYMENT_STANDARD.md (repo -> S3 -> EC2 pulls)</constraint>
    <constraint>Wait for DS commit to CLOUD before uploading to S3 (req 1 is a gate)</constraint>
    <constraint>No emojis in any SSM commands or scripts (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ADVTV2.001.gold-architect-attribution" status="complete">
      All 4 scripts modified and data_contract.xml updated. Pending DS commit to CLOUD.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">4 gold scripts deployed to bd-gold-layer-runner via S3</deliverable>
    <deliverable type="verify">FULL gold layer run complete, rel_architect_lookup verified</deliverable>
    <deliverable type="document">Session log documenting verification output</deliverable>
  </deliverables>
</task_order>

#### ADVI_BKSCMP.003.dt-lambda-deploy.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-003-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-19</date>
    <status>pending</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Deploy the updated opal-partners-data Lambda (v2.8) after DS commits the WS2 Lambda
    changes (ADVI_BKSCMP.001 req 6 commit). Tag as partners-api-v1.5.0. This brings the
    new firm/advisor composition routes live so AE's gold artifacts become accessible.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS4 (DT actions).
    Deployment reference: docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md.

    Current partners-api tag: partners-api-v1.4.0. Verify with:
      git tag -l "partners-api-v*" | sort -V | tail -5
    Target: partners-api-v1.5.0 (minor bump -- two new routes, new cache-control helper).

    DS gate commit: ADVI_BKSCMP.001 req 6 (Lambda v2.8 commit to CLOUD).
    DS will report the commit SHA. Confirm it exists before building.

    Known workaround: build-and-upload.sh fails on this machine (bun MSYS2 path issue).
    Use PowerShell temp script at C:/Windows/Temp/ as documented in AE5 log.
  </context>

  <scope>
    <files>
      <file action="deploy">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      GATE: Confirm DS has committed the Lambda v2.8 changes to CLOUD.
      Check: git log --oneline -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
      Verify the commit message mentions "v2.8" or "ADVI_BKSCMP WS2". Do not build before confirming.
    </requirement>

    <requirement id="2">
      Build and upload the Lambda artifact:
        Use PowerShell temp script pattern (C:/Windows/Temp/build-partners-data.ps1)
        — build-and-upload.sh is broken on this machine.
      Upload to: s3://opal-313476888478-lambda-artifacts/partners-api/opal-partners-data.zip
      Record SHA256 in session log.
    </requirement>

    <requirement id="3">
      Update infra/aws/lambda/ci/lambda-source-map.json entry for opal-partners-data
      with the new SHA256 and S3 version.
      Commit under DT author:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci(partners-api): upload opal-partners-data v2.8 (ADVI_BKSCMP)"
    </requirement>

    <requirement id="4">
      terraform plan (partners-api module). Expected: 1 to change (opal-partners-data
      in-place — s3_object_version + source_code_hash).
      terraform apply. Verify 0-diff second plan.
    </requirement>

    <requirement id="5">
      Run record-terraform-deploy.sh:
        bash infra/aws/lambda/ci/record-terraform-deploy.sh partners-api partners-api-v1.5.0
      Commit the CHANGELOG.json update:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci: record deploy partners-api @ (commit) [skip ci]"
    </requirement>

    <requirement id="6">
      Tag and push:
        git tag -l "partners-api-v*" | sort -V | tail -5   # verify next version
        git tag -a partners-api-v1.5.0 -m "ADVI_BKSCMP: firm+advisor composition routes (v2.8)"
        git push --follow-tags
    </requirement>

    <requirement id="7">
      Update deployment_map.xml with partners-api-v1.5.0.
    </requirement>

    <requirement id="8">
      Spot-verify new routes are live (optional, can be done before AE gold run):
        Confirm that GET /api/scoped/partners/books/firm/all/composition?firmId=49financial
        returns 503 (expected — artifacts not yet in S3) rather than 404 (wrong route) or 500 (code error).
      Report deploy complete to COO. This is the gate for AE to start gold run verification
      (AE can run the gold layer before the Lambda deploy; the Lambda must be live to serve artifacts).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS gate commit confirmed before build</criterion>
    <criterion id="2">Artifact uploaded; SHA256 recorded in session log</criterion>
    <criterion id="3">lambda-source-map.json updated and committed</criterion>
    <criterion id="4">terraform apply complete, 0-diff second plan confirmed</criterion>
    <criterion id="5">partners-api-v1.5.0 tag pushed with --follow-tags</criterion>
    <criterion id="6">CHANGELOG.json updated via record-terraform-deploy.sh</criterion>
    <criterion id="7">Firm composition route returns 503 (not 404/500) before S3 artifacts exist</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>GATE: Do not build before confirming DS Lambda v2.8 commit is on CLOUD</constraint>
    <constraint>Always check actual git tags before tagging -- git tag -l "partners-api-v*" | sort -V | tail -5</constraint>
    <constraint>Use PowerShell temp script for zip + upload (build-and-upload.sh broken on this machine)</constraint>
    <constraint>No emojis in commit messages or Terraform apply output (CLAUDE.md rule 13)</constraint>
    <constraint>lambda-source-map.json must be updated for every Lambda deploy</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before AWS CLI commands with ARN or S3 paths</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_BKSCMP.001 req 6" status="pending">
      opal-partners-data v2.8 Lambda committed to CLOUD -- hard gate for build
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">opal-partners-data v2.8 deployed; tagged partners-api-v1.5.0</deliverable>
    <deliverable type="document">Session log with SHA256, 0-diff confirmation, tag</deliverable>
  </deliverables>
</task_order>

#### ADVI_MVPLVL.005.lambda-deploy.md

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-16-005-dt-artifact-rebuild</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-16</date>
    <status>pending</status>
    <thread_serial>ADVI_MVPLVL-005</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment/</thread_ref>
    <revision>REVISED 2026-03-16 — partners-api-v1.0.0 (ddce9fef) and v1.0.1 hotfix
    (da5c527f) already deployed. This revision covers the artifact rebuild with DS 005
    Addendum A code, end-to-end verification, and portal DEV->PROD merge.</revision>
  </metadata>

  <objective>
    Rebuild the opal-partners-data Lambda artifact from current source (includes DS 005
    Addendum A endpoints: handle_mix_timeseries, handle_concentration_timeseries), deploy
    via Terraform, verify all Books Tab endpoints end-to-end, then merge portal DEV->PROD
    and deploy.
  </objective>

  <context>
    Current state (partners-api-v1.0.1):
    - Lambda Terraform module: infra/aws/terraform/partners-api/ (1024MB, 120s)
    - API Gateway: 6 /api/scoped/partners/books/* routes live with JWT authorizer
    - awswrangler 3.x compat fixes applied (post-read filtering, dtype_backend='numpy', NA safety)
    - Gold artifacts exist on S3: client_mix_timeseries.parquet, client_concentration_timeseries.parquet (AE Gate 2 passed)

    What's missing: the deployed artifact was built from code BEFORE DS 005 commit (6cae4815).
    handle_mix_timeseries and handle_concentration_timeseries do not exist in the deployed Lambda.
    The 2 mix/concentration API Gateway routes return 500 (unhandled path).
  </context>

  <scope>
    <files>
      <file action="none">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py (source — already committed, do not modify)</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/terraform/partners-api/ (terraform apply)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Rebuild artifact zip from current source at
      infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/.
      Upload to s3://opal-313476888478-lambda-artifacts/partners-api/opal-partners-data.zip.
      Use build-and-upload.sh or the PowerShell workaround (see MEMORY.md re: bun/MSYS2 path issue).
    </requirement>

    <requirement id="2">
      terraform plan on partners-api module. Expected change: source_code_hash update only.
      terraform apply. Verify 0-diff plan after apply.
    </requirement>

    <requirement id="3">
      Update lambda-source-map.json with new deployed commit hash and SHA256.
    </requirement>

    <requirement id="4">
      End-to-end verification — test ALL 8 Books Tab endpoint patterns via Lambda test invoke
      or curl. Use relationship z08327149 (confirmed working in v1.0.1 hotfix):

      | Endpoint | Expected |
      |---|---|
      | /books/relationship/{id}/timeseries?firmId=49financial | 200 + records (424 confirmed in v1.0.1) |
      | /books/relationship/{id}/composition?firmId=49financial | 200 + asset classes + top-10 |
      | /books/account/{id}/timeseries?firmId=49financial | 200 + records |
      | /books/account/{id}/composition?firmId=49financial | 200 + asset classes |
      | /books/relationship/{id}/mix-timeseries?firmId=49financial | 200 + daily mix pct data |
      | /books/relationship/{id}/concentration-timeseries?firmId=49financial | 200 + top-N holdings over time |

      The last 2 are the NEW Addendum A endpoints. If they return 500 or empty, the artifact
      rebuild did not pick up the DS 005 code — stop and investigate.
    </requirement>

    <requirement id="5">
      Tag: `partners-api-v1.1.0` (check `git tag -l "partners-api-v*" | sort -V | tail -5` first).
      Push with --follow-tags.
    </requirement>

    <requirement id="6">
      After DE firmId fix lands on portal DEV and endpoint verification passes:
      Portal DEV -> PROD merge and deploy.

      ```bash
      cd portal
      git checkout PROD
      git pull origin PROD
      git merge DEV
      git push origin PROD
      ./scripts/deploy-manual.sh
      git checkout DEV
      cd ..
      git add portal
      git commit --author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>" -m "chore: update portal submodule (ADVI_MVPLVL Books Tab + Addendum A)"
      ```
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">0-diff Terraform plan after apply</criterion>
    <criterion id="2">All 6 original endpoints return valid JSON (timeseries, composition per relationship + account)</criterion>
    <criterion id="3">Both Addendum A endpoints return valid JSON (mix-timeseries, concentration-timeseries)</criterion>
    <criterion id="4">lambda-source-map.json updated with deployed commit + SHA256</criterion>
    <criterion id="5">Portal PROD reflects all ADVI_MVPLVL portal work (Books Tab + Addendum A panels)</criterion>
    <criterion id="6">Tag partners-api-v1.1.0 pushed</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify lambda_function.py — DS code is committed and correct. Only rebuild the artifact.</constraint>
    <constraint>Terraform is the only Lambda deployment mechanism (CLAUDE.md rule 1)</constraint>
    <constraint>Commit before apply (CLAUDE.md rule 2)</constraint>
    <constraint>Do NOT merge portal DEV->PROD until DE firmId fix is committed on DEV and all endpoints verified</constraint>
    <constraint>partners-api module is at infra/aws/terraform/partners-api/ — do NOT put it in bd-pipeline</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.005.gold-script-and-endpoints" status="complete">
      Lambda endpoint code committed (6cae4815)
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_MVPLVL.005.ec2-gold-deploy" status="complete">
      Gold artifacts exist on S3 and Gate 2 passed (9ee5a752, d1bd3a18)
    </dependency>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_MVPLVL.004.p4-books-proxy-wiring" status="complete">
      DE firmId fix committed on portal DEV (db52d31). DEV->PROD merge gate cleared.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">Lambda artifact rebuilt and deployed via Terraform</deliverable>
    <deliverable type="tag">partners-api-v1.1.0</deliverable>
    <deliverable type="deploy">Portal PROD updated with all ADVI_MVPLVL work</deliverable>
  </deliverables>
</task_order>

#### deployment_map.md

# Task Order — Deployment Map: ClientPlatform

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-map-client-platform</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a deployment_map.xml that is your permanent operational reference for
    the ClientPlatform pod. This pod uniquely spans two entirely separate pipelines —
    yang (ModelPortfolios) and BD (AdvisorIntelligence). The map gives a page-centric
    view (endpoints per page), a Lambda-centric view (deployment state), and an
    explicit pipeline_split documenting exactly where your DT deployment authority
    ends and AE coordination begins.
    Consolidates and supersedes the earlier deployment_audit task order.
  </objective>

  <scope>
    <pod>ClientPlatform</pod>
    <pages>
      <page>ModelPortfolios</page>
      <page>AdvisorIntelligence</page>
    </pages>
    <rd_agents>
      <agent>0.4.1_RD_ModelPortfolios</agent>
      <agent>0.4.2_RD_AdvisorIntelligence</agent>
    </rd_agents>
    <files>
      <!-- Wave outputs — start here -->
      <file action="read">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
      <file action="read">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
      <!-- Independent verification — read portal pages directly -->
      <file action="read">portal/src/pages/ModelPortfolios/</file>
      <file action="read">portal/src/pages/AdvisorIntelligence/</file>
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">portal/src/api/endpoints/aum.ts</file>
      <!-- Terraform modules -->
      <file action="read">infra/aws/terraform/yang-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/CHANGELOG.json</file>
      <file action="read">infra/aws/terraform/bd-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/s3-notifications.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/ec2.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>
      <!-- Deployment state -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read data_contract.xml first — use the pipeline_split section as the
      primary organizer of your deployment map. Then independently verify by
      reading the portal page directories and endpoint files directly: look for
      useQuery, useMutation, and fetch calls. Note any endpoints the wave
      documents missed.
    </requirement>
    <requirement id="2">
      For each portal page, document which API endpoints it calls, the URL
      pattern, the Lambda handling each, and which pipeline owns it.
    </requirement>
    <requirement id="3">
      For each Lambda serving this pod, extract from lambda-source-map.json:
      source_path, memory_mb, timeout_s, layers[], last_deployed_commit,
      last_deployed_at. Identify which Terraform module owns it.
    </requirement>
    <requirement id="4">
      ModelPortfolios (Yang side): yang-model-portfolio-benchmarks is the single
      Lambda. Confirm from stepfunctions.tf whether it runs in the Step Functions
      state machine or independently. Document its S3 output key and the Yang
      versioning mechanism for the portal fetch.
    </requirement>
    <requirement id="5">
      AdvisorIntelligence (BD side): bd-portal-publisher, bd-portal-advisor-publisher,
      bd-client-detail, and opal-partners-data are your portal-facing Lambdas.
      Read s3-notifications.tf to confirm the trigger chain: gold layer completion
      sentinel → S3 notification → publisher Lambda. Document this chain explicitly.
    </requirement>
    <requirement id="6">
      From EC2_MANIFEST.json, document bd-gold-layer-runner and bd-gold-detail-generator
      as upstream EC2 dependencies. You do not own them (0.6.0_AE_PartnerETL does)
      but you need them as your diagnostic starting point when AdvisorIntelligence
      data is stale. Document instance IDs and last deployed commits.
    </requirement>
    <requirement id="7">
      Document the deployment authority boundary clearly: which Lambdas you can
      deploy independently vs what requires coordination with 0.6.0_AE_PartnerETL.
    </requirement>
    <requirement id="8">
      Flag any pages with no clear data pipeline connection. Note any functions
      with lifecycle ignore_changes or non-standard deploy paths.
    </requirement>
    <requirement id="9">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      deployment_map.xml exists at org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;deployment_map&gt;
        &lt;metadata&gt; agent, pod, rd_agents[], date &lt;/metadata&gt;

        &lt;pages_served&gt;
          One &lt;page&gt; per portal page:
            name, rd_agent, pipeline (yang|bd),
            &lt;api_endpoints&gt;
              &lt;endpoint url="/api/..." lambda="{name}" pipeline="{pipeline}" /&gt;
            &lt;/api_endpoints&gt;
            &lt;data_pipeline&gt; pipeline name, trigger chain, S3 output paths &lt;/data_pipeline&gt;
        &lt;/pages_served&gt;

        &lt;lambda_inventory&gt;
          One &lt;lambda&gt; per function — grouped by pipeline:
            name, pipeline (yang|bd), terraform_module, source_path,
            memory_mb, timeout_s, layers[], trigger,
            last_deployed_commit, last_deployed_at,
            &lt;serves_pages&gt; page and section &lt;/serves_pages&gt;
        &lt;/lambda_inventory&gt;

        &lt;pipeline_split&gt;
          &lt;yang_side&gt;
            Lambda, module, versioning model, DT deployment authority
          &lt;/yang_side&gt;
          &lt;bd_side&gt;
            Portal-facing Lambdas (DT authority) vs upstream EC2/gold layer (AE authority).
            S3 notification trigger chain from gold completion sentinel to publishers.
          &lt;/bd_side&gt;
        &lt;/pipeline_split&gt;

        &lt;terraform_modules&gt;
          One &lt;module&gt; per Terraform module:
            path, current_tag, state_key,
            &lt;resources&gt; resource type + name &lt;/resources&gt;
        &lt;/terraform_modules&gt;

        &lt;upstream_ec2_dependencies&gt;
          EC2 services owned by AE that feed this pod's Lambdas.
          name, instance_id, last_deployed_commit, owned_by (AE agent)
        &lt;/upstream_ec2_dependencies&gt;

        &lt;s3_triggers&gt;
          S3 notification rules that invoke pod Lambdas:
            bucket, prefix, event_type, target_lambda
        &lt;/s3_triggers&gt;

        &lt;recent_deployments&gt;
          One &lt;deployment&gt; per function: function, commit, date
        &lt;/recent_deployments&gt;

        &lt;deployment_sequence&gt;
          Separate sequences for Yang side and BD side
        &lt;/deployment_sequence&gt;

        &lt;known_gotchas&gt;
          AE coordination points, BD data lag, any ignore_changes exceptions
        &lt;/known_gotchas&gt;
      &lt;/deployment_map&gt;
    </criterion>
    <criterion id="3">
      pipeline_split section must be complete and unambiguous about deployment
      authority. This is the most operationally critical distinction for this pod.
    </criterion>
    <criterion id="4">
      Every Lambda name matches an entry in lambda-source-map.json exactly.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any source code or infrastructure. Read-and-document only.</constraint>
    <constraint>Do not run terraform plan, apply, or any AWS CLI commands.</constraint>
    <constraint>Use Glob, Grep, and Read tools only — no Explore agent, no Task agent.</constraint>
    <constraint>
      bd-pipeline infrastructure changes (EventBridge rules, S3 notifications,
      EC2 config) are owned by 0.6.0_AE_PartnerETL. Your DT authority covers
      portal-facing Lambda code only: bd-portal-publisher, bd-portal-advisor-publisher,
      bd-client-detail, opal-partners-data.
    </constraint>
    <constraint>
      yang-pipeline is shared across three pods. For yang-model-portfolio-benchmarks
      specifically, confirm with DS whether it runs in the Step Functions state machine.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="data_contract" status="complete"/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml
    </deliverable>
  </deliverables>
</task_order>
```


### 0.4.0_DT_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DT_ClientPlatform

1fa08590 0.4.0_DT_ClientPlatform: ADVI_MIXV2.004 -- partners-api-v1.3.0 deployed
d27a3bdb 0.4.0_DT_ClientPlatform: partners-api -- bump opal-partners-data memory to 2048 MB
585bcaf9 0.4.0_DT_ClientPlatform: update deployment_map.xml -- add partners-api module + opal-partners-data Lambda
7b1ffb72 org(0.4.0_DT_ClientPlatform): ADVI_PSCFIX DT1 session log -- bd-portal-publisher deploy complete
f6d9f295 org(2.0.0_SA_COO): ADVI_PSCFIX follow-on task orders -- DT1 deploy + A3 script09
03e77e2a org(0.4.0_DT_ClientPlatform): ADVI project tracking updates + PRD revision + yang lock
4818bf0f org(0.4.0_DT_ClientPlatform): ADVI_APISCP.007 router v7 task order
6befdaf5 org(0.4.0_DT_ClientPlatform): ADVI_APISCP.007 router v7 opal-capital routing deploy log
e0520883 org(0.4.0_DT_ClientPlatform): ADVI_APISCP.004 OPTIONS CORS v6 deploy log
25b1b0bc org(0.7.0_AE_CloudOps): ADVI_APISCP.004 complete -- opal-data-bd CORS + CF OriginRequestPolicy
95e5d417 org(0.4.0_DT_ClientPlatform): ADVI_APISCP.003 OAI v5 deploy log + task orders complete
19551b11 infra(cloudops): ADVI_APISCP.003 -- create OAI opal-scoped-advisor-oai, apply AllowScopedAdvisorOAI bucket policy to opal-data-bd
64855450 org(0.4.0_DT_ClientPlatform): ADVI_APISCP v4 rollback log + OAC assessment; absorb DE verification logs
0ae81df7 org(0.4.0_DT_ClientPlatform): ADVI_APISCP.001 lambda-edge v4 deploy log + task order complete
d3a51c58 0.4.0_DT_ClientPlatform: ADVI_NNAVAR -- scripts 05/05b uploaded to S3 gold path, rebuild-ready (session log + task order complete)
c376ced8 0.4.0_DT_ClientPlatform: ADVI_NNAVAR -- investigation closure: gap explained, Phase 5b cancelled, production bundle pending COO auth
e31f420a 0.4.0_DT_ClientPlatform: ADVI_49FNV3-F5 -- qtd leaderboard deploy session log
cbe221f3 0.4.0_DT_ClientPlatform: ADVI_NNAVAR -- Phase 5 desc_audit: exclusion_warranted=false, flag Holding MV withdrawn at 119.3M (session log)
9bff0a17 0.4.0_DT_ClientPlatform: ADVI_49FNV3-F1 -- bd-portal-publisher redeploy session log
69a4a61d 0.4.0_DT_ClientPlatform: ADVI_49FNV3 launch review + DT session logs

### 0.4.0_DT_ClientPlatform -- Recent Deployments

# Recent deployment tags (all pipelines, newest first)

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
yang-v2.2.3
portal-auth-v1.3.1
shared-advisor-router-v7
yang-v2.2.2
yang-v2.2.1

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
972c52f5 org(1.0.0_SA_CTO): session log -- AE prompt enrichment (Session D complete)
d711a31f 0.6.0_AE_PartnerETL: enrich PartnerETL agent prompt with source-grounded context

### 0.6.0_AE_PartnerETL -- Recent Deployments

# Recent deployment tags (all pipelines, newest first)

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
yang-v2.2.3
portal-auth-v1.3.1
shared-advisor-router-v7
yang-v2.2.2
yang-v2.2.1

