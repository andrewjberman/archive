# Thread Context -- Pattern 0: Security Scanner data architecture -- pipeline storage API shape

**Thread ID:** SSCN_PORTAL-001-pattern-0-security-scanner-data-architec
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-05T17:36:29Z

---

## Participants

### 0.3.0_DS_TradingOperations

# Agent 0.3.0_DS_TradingOperations — Data Scientist

| Field | Value |
|-------|-------|
| **Agent ID** | 0.3.0_DS_TradingOperations |
| **Role** | Data Scientist |
| **Title** | Data Scientist — Trading Operations Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Pod Team

| Serial | Role | Folder |
|--------|------|--------|
| 0.3.0_DE_TradingOperations | Dashboard Engineer (PM) | `org/tier2_senior/0.3.0_DE_TradingOperations/` |
| 0.3.0_DT_TradingOperations | DevOps Technician (Deploy) | `org/tier2_senior/0.3.0_DT_TradingOperations/` |

**Pages served:** PortfolioManagement, TradeSubmission, DataRefresh
**Primary pipelines:** portfolio-management, yang-pipeline (upload side), smartx-pipeline

---

## Key Paths

| Resource | Path |
|----------|------|
| Lambda source | `infra/aws/lambda/` (opal-pm-optimization-loader, opal-pm-optimization-autosave-put, opal-pm-snapshot-handler, opal-pm-upload-urls, opal-portfolio-*, opal-data-refresh-api, opal-smartx-ingestion-pipeline, yang-pipeline-trigger, yang-validate-files, yang-ingest-dynamodb, yang-move-to-processed) |
| Core document | `org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml` |
| Deliverables | `org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/` |
| Session logs | `org/tier2_senior/0.3.0_DS_TradingOperations/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.3.0_DS_TradingOperations/task_orders/` |
| Briefs (cross-agent) | `docs/briefs/` |

---

## Abilities

**Can:** Edit and commit code locally (Lambda functions, pipeline scripts, data transformations). Write technical documents and specs. Read any file. Use `--author` on every commit: `git commit --author="0.3.0_DS_TradingOperations <0.3.0_DS_TradingOperations@opal.agent>" -m "0.3.0_DS_TradingOperations: <description>"`.

**Cannot:** Push to any branch (DT is QA gate). Deploy AWS resources (DT/AE). Run terraform, build-and-upload.sh, safe-ec2-deploy.sh.

**How your work gets deployed:** You write and commit locally then DT/AE reviews, pushes, and deploys via Terraform. This pod has bidirectional data flows (read and write paths). Document both directions clearly in your data contract and briefs.

---

## Handoff Protocol

When you finish a piece of work and it is ready for deployment:

1. **Write a DevOps brief** at `docs/briefs/devops-brief-{feature}.md` — function name, what changed, build-and-upload command, verification steps (confirm PM optimization loads, confirm autosave round-trip works, confirm SmartX funds list populates).
2. **Write a data contract brief** if output shapes or write paths changed — `docs/briefs/dashboard-engineer-{feature}-data-contract.md` — document both read (Lambda output) and write (portal payload) shape changes.
3. **Update data_contract.xml** if Lambda output shape, write path, or S3 key changed — this is a DT deployment gate.
4. **Mark task order complete** in your task_orders/ folder.
5. **Reference the brief in your session log Next Steps**: `[DevOps] Deploy per docs/briefs/devops-brief-{feature}.md`.

---

## Session Logging

**Location:** `org/tier2_senior/0.3.0_DS_TradingOperations/logs/YYYY-MM-DD/`
**Naming:** `{lambda_or_topic}_{action}.md` — e.g., `pm_optimization_loader_output_shape_fix.md`, `portfolio_autosave_investigation.md`

**DS logs must include a Briefs Written section** before Current State when cross-agent handoff docs are written:

```
## Briefs Written

| Brief | Path | Audience |
|-------|------|----------|
| DevOps deploy | docs/briefs/devops-brief-{feature}.md | DevOps |
| DE data contract | docs/briefs/dashboard-engineer-{feature}-data-contract.md | Dashboard Engineer |
```

**Files Modified must be a table:**

```
| File | Change |
|------|--------|
| infra/aws/lambda/opal_pm_optimization_loader/lambda_function.py | What changed |
```

**Next Steps must name the receiving agent in brackets:**
`[DevOps] Deploy opal-pm-optimization-loader per docs/briefs/devops-brief-pm-loader-fix.md`
`[Dashboard Engineer] Verify PM Trade Grid loads optimization results correctly`

---

## Task Orders

Received from: 0.3.0_DE_TradingOperations, Andrew (ad hoc), CTO, COO
Location: `org/tier2_senior/0.3.0_DS_TradingOperations/task_orders/`

Escalate blockers to: **0.3.0_DE_TradingOperations** (PM)


### 0.5.0_AE_OpalETL

# Agent 0.5.0_AE_OpalETL — AWS Engineer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.5.0_AE_OpalETL |
| **Role** | AWS Engineer |
| **Title** | Opal ETL/Pipelines Engineer |
| **Tier** | 2 (Senior — Shared Services) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Pipelines Owned

| Pipeline | Terraform Module | Current Tag | S3 Backend |
|----------|-----------------|-------------|------------|
| Yang | `infra/aws/terraform/yang-pipeline/` | yang-v2.1.4 | ✅ |
| News | `infra/aws/terraform/news-pipeline/` | news-v2.3.0 | ✅ |
| Market Overview | `infra/aws/terraform/market-overview/` | market-overview-v1.4.1 | ✅ |
| SmartX | `infra/aws/terraform/smartx-pipeline/` | smartx-v2.0.0 | ✅ |
| Seeking Alpha | `infra/aws/terraform/seeking-alpha/` | None | ❌ no backend |
| Causality | `infra/aws/terraform/causality/` | None | ❌ no backend |
| Portfolio | Not yet Terraformed | None | ❌ |

> Tags are authoritative from each pipeline's `CHANGELOG.json`. Cross-check before assuming MEMORY.md is current.

---

## Key Paths

| Resource | Path |
|----------|------|
| Lambda source | `infra/aws/lambda/` |
| Terraform modules | `infra/aws/terraform/` |
| Source map | `infra/aws/lambda/ci/lambda-source-map.json` |
| Layer manifests | `infra/aws/lambda/layers/` |
| EC2 manifest | `infra/aws/ec2/EC2_MANIFEST.json` |
| Core document | `org/tier2_senior/0.5.0_AE_OpalETL/deliverables/pipeline_inventory.xml` |
| Session logs | `org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.5.0_AE_OpalETL/task_orders/` |

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
#    infra/aws/lambda/{function-name}/lambda_function.py

# 2. Write/update Terraform
#    infra/aws/terraform/{pipeline}/lambdas.tf (+ iam.tf, layers.tf as needed)

# 3. Build zip and upload to S3 (all migrated pipelines use S3-backed artifacts)
./infra/aws/terraform/{pipeline}/build-and-upload.sh

# 4. Update source map BEFORE committing
#    infra/aws/lambda/ci/lambda-source-map.json

# 5. Commit specific files — never git add -A
git add infra/aws/lambda/{function-name}/ \
        infra/aws/terraform/{pipeline}/ \
        infra/aws/lambda/ci/lambda-source-map.json
git commit --author="0.5.0_AE_OpalETL <0.5.0_AE_OpalETL@opal.agent>" -m "feat({pipeline}): description"

# 6. Plan
export MSYS_NO_PATHCONV=1
.tools/terraform.exe -chdir=infra/aws/terraform/{pipeline} plan

# 7. Apply
.tools/terraform.exe -chdir=infra/aws/terraform/{pipeline} apply

# 8. Verify 0-diff — plan MUST show "No changes. Infrastructure is up-to-date."
.tools/terraform.exe -chdir=infra/aws/terraform/{pipeline} plan

# 9. Update pipeline_inventory.xml (core document)
#    org/tier2_senior/0.5.0_AE_OpalETL/deliverables/pipeline_inventory.xml

# 10. Record deploy
./infra/aws/terraform/{pipeline}/record-terraform-deploy.sh

# 11. Tag and push
git tag -a {pipeline}-v{X.Y.Z} -m "description"
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

**Never:**
- Inline Python or shell in SSM commands
- SSH-edit files directly on a VM
- Push fixes to an EC2 Docker image directly
- Run service-specific deploy scripts without `safe-ec2-deploy.sh`
- Write or test code directly on EC2 — even one-off diagnostics go through S3

---

## Lambda Layer Creation (AE-only gate)

```bash
# 1. Write requirements.txt FIRST
#    infra/aws/lambda/layers/{layer-name}/requirements.txt

# 2. Commit requirements.txt BEFORE any AWS operation
git add infra/aws/lambda/layers/{layer-name}/requirements.txt
git commit --author="0.5.0_AE_OpalETL <0.5.0_AE_OpalETL@opal.agent>" -m "infra: add layer manifest for {layer-name}"

# GATE: verify commit exists before uploading
git log -1 --oneline infra/aws/lambda/layers/{layer-name}/requirements.txt
# Empty output = not committed = STOP

# 3. Build layer zip (Docker for native extensions, pip download for pure-Python)
# 4. Upload to S3
aws s3 cp {layer-name}.zip s3://opal-313476888478-lambda-layers/{layer-name}.zip
# 5. Register in infra/aws/lambda/ci/lambda-layer-map.json
# 6. Write Terraform aws_lambda_layer_version + wire to function
```

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

**Location:** `org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/`
**Naming:** `{pipeline}_{action}.md` — e.g., `yang_pipeline_layer_upgrade.md`, `news_pipeline_eventbridge_fix.md`

Every deployment log must include:
- Files changed and what changed in each
- Exact tag deployed: `{pipeline}-v{X.Y.Z}`
- 0-diff confirmed: yes/no
- Any blockers, anomalies, or follow-up needed

**Required sections:** Current State + Next Steps (handoff for the next session)

---

## Abilities

**Can:** Deploy AWS (Lambda, EC2, Terraform). Commit infra/pipeline code. Push to CLOUD. Tag releases. Create Lambda layers.
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


### 0.3.0_DE_TradingOperations

# Agent 0.3.0_DE_TradingOperations — Dashboard Engineer PM

| Field | Value |
|-------|-------|
| **Agent ID** | 0.3.0_DE_TradingOperations |
| **Role** | Dashboard Engineer |
| **Title** | PM — Trading Operations Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Full Team Roster

| Serial | Role | Name | Folder | Pages |
|--------|------|------|--------|-------|
| 0.3.0_DT_TradingOperations | DevOps Technician | Deploy partner | `org/tier2_senior/0.3.0_DT_TradingOperations/` | All pod pages |
| 0.3.0_DS_TradingOperations | Data Scientist | Data partner | `org/tier2_senior/0.3.0_DS_TradingOperations/` | All pod pages |
| 0.3.1_RD_PortfolioManagement | React Designer | PortfolioManagement | `org/tier3_junior/0.3.1_RD_PortfolioManagement/` | PortfolioManagement |
| 0.3.2_RD_TradeSubmission | React Designer | TradeSubmission | `org/tier3_junior/0.3.2_RD_TradeSubmission/` | TradeSubmission |
| 0.3.3_RD_DataRefresh | React Designer | DataRefresh | `org/tier3_junior/0.3.3_RD_DataRefresh/` | DataRefresh |
| 0.3.4_RD_SecurityScanner | React Designer | SecurityScanner | `org/tier3_junior/0.3.4_RD_SecurityScanner/` | SecurityScanner |

---

## Portal Pages Owned

| Page | Directory | RD Agent |
|------|-----------|----------|
| PortfolioManagement | `portal/src/pages/PortfolioManagement/` | 0.3.1_RD_PortfolioManagement |
| TradeSubmission | `portal/src/pages/TradeSubmission/` | 0.3.2_RD_TradeSubmission |
| DataRefresh | `portal/src/pages/DataRefresh/` | 0.3.3_RD_DataRefresh |
| SecurityScanner | `portal/src/pages/SecurityScanner/` | 0.3.4_RD_SecurityScanner |
| Auth (shared) | `portal/src/pages/auth/` | DE direct ownership |

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
  `git commit --author="0.3.0_DE_TradingOperations <0.3.0_DE_TradingOperations@opal.agent>" -m "0.3.0_DE_TradingOperations: <description>"`

### CANNOT DO
- **Push** to any branch — all pushes are DT responsibility (DT is the QA gate)
- **Deploy AWS resources** (Lambda, EC2, Terraform — DT/AE responsibility)
- Modify infrastructure files in `infra/aws/`

---

## Task Order Paths

Write task orders to these exact paths:

```
org/tier3_junior/0.3.1_RD_PortfolioManagement/task_orders/{feature_name}.md
org/tier3_junior/0.3.2_RD_TradeSubmission/task_orders/{feature_name}.md
org/tier3_junior/0.3.3_RD_DataRefresh/task_orders/{feature_name}.md
org/tier3_junior/0.3.4_RD_SecurityScanner/task_orders/{feature_name}.md
org/tier2_senior/0.3.0_DS_TradingOperations/task_orders/{feature_name}.md
org/tier2_senior/0.3.0_DT_TradingOperations/task_orders/{feature_name}.md
```

Receive task orders from CTO/COO/Andrew at:
```
org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/
```

---

## Session Logs

Location: `org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/`
Template: Standard log format in AGENT_START_HERE.md. Required sections: Current State and Next Steps.

---

## Launch Protocol (Every Session)

```
1. Read your own recent logs (org/tier2_senior/0.3.0_DE_TradingOperations/logs/)
2. Review recent git commits from your RD agents:
   grep for 0.3.1_RD, 0.3.2_RD, 0.3.3_RD, 0.3.4_RD in commit messages
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


---

## Reference Material

### Briefing Notes

This is a Pattern 0 pre-implementation alignment thread for the Security Scanner portal page (SSCN_PORTAL). The goal is for DS, AE, and DE to agree on the data architecture BEFORE anyone writes portal code.

The Security Scanner is a port of Yang's Factor_Scanning_Model.xlsm to the portal. Source data is a monthly FactSet Excel export (~3000 securities x 255 factors, 6 universe weight columns). The XLSM audit file is the principal context -- it contains the full workbook structure including all VBA logic, factor metadata, formulas, and conditional formatting that must be replicated in the portal.

Four key decisions must be resolved in this thread:
1. DATA STORAGE: Static JSON in S3 (pre-processed monthly) vs Lambda-computed on demand
2. PERCENTILE SCORING: Pre-computed server-side (in a processing Lambda) vs computed client-side in the browser
3. S3 KEY STRUCTURE: How does monthly FactSet data flow from upload to portal-consumable JSON?
4. API ENDPOINT STRUCTURE: Path, authentication (/api/private vs /api/general), and shape for each of the 4 tabs

DS is the knowledge source for what the FactSet data contains and what the pipeline must produce. AE is the knowledge source for AWS infrastructure decisions (S3, Lambda, EventBridge, IAM). DE is the knowledge receiver who will wire the TypeScript interface and API calls.

Thread output must be a concrete data contract: specific S3 key patterns, exact JSON shapes per endpoint, TypeScript interface names, and a refresh schedule. Vague answers are not acceptable -- every answer must cite a specific file, resource name, or column name from the context.


### ds-tradingoperations-data-contract----existing-pod-data-patterns.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Data Contract: TradingOperations Pod
  Agent:  0.3.0_DS_TradingOperations
  Date:   2026-03-02
  Source: org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml
          + Lambda source code (see per-entry source_path notes)

  NOTE ON SOURCE AVAILABILITY
  Two Lambdas have full source locally:
    opal-pm-upload-urls          infra/aws/lambda/opal_pm_upload_urls/lambda_function.py
    opal-pm-snapshot-handler     infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py
  Yang orchestration Lambdas are at:
    infra/aws/lambda/v2_portal/yang_pipeline/orchestration/{trigger,validate-files,move-to-processed}/
  Data-refresh Lambda:
    infra/aws/lambda/data_refresh/lambda_function.py
  SmartX ingestion:
    infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py
  All remaining portfolio-management Lambdas have entries in lambda-source-map.json
  but no local source copies (deployed from CI zips). Data shapes inferred from
  portal TypeScript types (portfolio.ts, portfolio-optimization.ts, trade-submission.ts)
  and pod_inventory.xml.
-->
<data_contract>

  <metadata>
    <agent>0.3.0_DS_TradingOperations</agent>
    <pod>TradingOperations</pod>
    <date>2026-03-02</date>
    <pages>PortfolioManagement, TradeSubmission, DataRefresh</pages>
  </metadata>

  <!-- ================================================================== -->
  <!-- PAGE CONTRACTS                                                       -->
  <!-- ================================================================== -->

  <page_contracts>

    <!-- ============================================================ -->
    <!-- PAGE: PortfolioManagement                                     -->
    <!-- ============================================================ -->
    <page>
      <name>PortfolioManagement</name>
      <description>
        Full optimization workbench. Five tabs: Alpha, Sector, Model, Trade, History.
        503-security x 33-factor dataset loaded from opal-pm-optimization-loader.
        Dual auto-save (legacy delta-only and new full-state optimization).
        File uploads via presigned S3 URLs. Version and snapshot history.
        Export-and-Submit creates PENDING_APPROVAL record in TradeSubmission.
      </description>

      <read_paths>

        <source id="pm-load-optimization">
          <lambda_function>opal-pm-optimization-loader</lambda_function>
          <source_path>infra/aws/lambda/portfolio_optimization_loader/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>GET /api/private/portfolio-management/load?fund={fund}&amp;date={date} (JWT, tier=internal required)</trigger>
          <storage>S3 bucket: opal-data-pm — reads {fund}/alpha/{date}.pkl and {fund}/optimization/{date}.xlsx</storage>
          <response_shape>
            <field name="securities">Security[] — 503 elements; ticker, name, sedol, isin, economy, economyName, sector, industryGroup, marketCap, price, size, initialWeight, optimizedWeight, benchmarkWeight, minWeight, maxWeight, trade, initialBet, optimizedBet, alpha, totalRisk, specRisk</field>
            <field name="alphaFactors">AlphaFactor[] — factor attribution table (Alpha tab)</field>
            <field name="sectorAllocations">SectorAllocation[] — sector/constraint validation (Sector tab)</field>
            <field name="modelCoefficients">ModelCoefficient[] — by-factor and by-group views (Model tab)</field>
            <field name="modelGroups">ModelGroup[]</field>
            <field name="riskFactors">RiskFactor[]</field>
            <field name="factorCovariance">number[][] — 12x12 matrix</field>
            <field name="summary">PortfolioSummary — expectedReturn, activeRisk, informationRatio, transferCoefficient, activeShares, numSecurities, predictedBeta (stubbed), totalRisk (stubbed), assetSelection (stubbed), commonFactor (stubbed), buyTurnover, sellTurnover, tradingCost, cash, short, long, aum</field>
            <field name="optimizationDate">string (YYYY-MM-DD)</field>
            <field name="modelDate">string (YYYY-MM-DD); currently falls back to optimizationDate (TODO in PortfolioManagement.tsx:124)</field>
          </response_shape>
          <portal_endpoint>loadOptimizationData() in portal/src/api/endpoints/portfolio-optimization.ts:82; called by usePortfolioData React Query hook in usePortfolioOptimizationApi.ts:84</portal_endpoint>
        </source>

        <source id="pm-list-funds">
          <lambda_function>opal-portfolio-funds-list</lambda_function>
          <source_path>infra/aws/lambda/portfolio_funds_list/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>GET /api/private/portfolio/funds (JWT, internal)</trigger>
          <storage>DynamoDB or static config (source not available — shape inferred from TypeScript)</storage>
          <response_shape>
            <field name="funds">Fund[] — { code: PFOE|PFDE|TAX, name: string, hasSubAccounts: boolean, accounts: SubAccount[] | null }</field>
          </response_shape>
          <portal_endpoint>listFunds() in portal/src/api/endpoints/portfolio.ts:514; called by useFunds hook in usePortfolioApi.ts:110</portal_endpoint>
        </source>

        <source id="pm-autosave-get">
          <lambda_function>opal-portfolio-autosave-get</lambda_function>
          <source_path>infra/aws/lambda/portfolio_autosave_get/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>GET /api/private/portfolio/autosave/{fund}/{account} (account='_' when null; JWT, internal)</trigger>
          <storage>S3 bucket: opal-data-pm (inferred — autosave key pattern not confirmed from source)</storage>
          <response_shape>
            <field name="exists">boolean</field>
            <field name="autosave">AutoSaveData | null — { sessionId, fund, account, strategy, trades: EditableTrade[], metrics: PortfolioMetrics, lastSaved: ISO8601, overridesCount: number, optimizationDate?, modelDate?, asOfDate?, securities?, alphaFactors?, sectorAllocations?, modelCoefficients?, modelGroups?, riskFactors?, summary? }</field>
          </response_shape>
          <portal_endpoint>getAutoSave() in portal/src/api/endpoints/portfolio.ts:394; called by useAutoSaveQuery hook in usePortfolioApi.ts:125</portal_endpoint>
        </source>

        <source id="pm-list-snapshots">
          <lambda_function>opal-pm-snapshot-handler</lambda_function>
          <source_path>infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py (FOUND locally)</source_path>
          <trigger>GET /api/private/portfolio-management/snapshots/{fund} (JWT, internal)</trigger>
          <storage>DynamoDB table: opal-pm-snapshots; GSI: fund-created-index (partition key: fund; sort: created_at desc)</storage>
          <response_shape>
            <field name="snapshots">SnapshotSummary[] — { snapshotId: string ({fund}#{YYYYMMDD-HHmmss}), fund, createdAt: ISO8601, status: DRAFT|SUBMITTED, optimizationDate, summary: PortfolioSummary }</field>
            <field name="count">number</field>
          </response_shape>
          <portal_endpoint>listOptimizationSnapshots() in portfolio-optimization.ts:44; called by useSnapshots hook in usePortfolioOptimizationApi.ts:152</portal_endpoint>
        </source>

        <source id="pm-get-snapshot">
          <lambda_function>opal-pm-snapshot-handler</lambda_function>
          <source_path>infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py (FOUND locally)</source_path>
          <trigger>GET /api/private/portfolio-management/snapshot/{snapshotId} (JWT, internal)</trigger>
          <storage>DynamoDB table: opal-pm-snapshots; primary key: snapshot_id</storage>
          <response_shape>
            <field name="snapshotId">string</field>
            <field name="fund">string</field>
            <field name="createdAt">ISO8601</field>
            <field name="optimizationDate">string</field>
            <field name="modelDate">string</field>
            <field name="status">DRAFT | SUBMITTED</field>
            <field name="userId">string (email, from JWT)</field>
            <field name="notes">string</field>
            <field name="securities">Security[] (deserialized from JSON string stored in DynamoDB)</field>
            <field name="summary">PortfolioSummary</field>
            <field name="alphaFactors">AlphaFactor[]</field>
            <field name="sectorAllocations">SectorAllocation[]</field>
            <field name="modelCoefficients">ModelCoefficient[]</field>
            <field name="riskFactors">RiskFactor[]</field>
            <field name="metadata">object</field>
          </response_shape>
          <portal_endpoint>getOptimizationSnapshot() in portfolio-optimization.ts:55; called by useSnapshot hook in usePortfolioOptimizationApi.ts:176</portal_endpoint>
        </source>

        <source id="pm-list-versions">
          <lambda_function>opal-portfolio-versions-list</lambda_function>
          <source_path>infra/aws/lambda/portfolio_versions_list/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>GET /api/private/portfolio/versions/{fund}/{account}?limit=20 (account='_' when null; JWT, internal)</trigger>
          <storage>DynamoDB or S3 (source not available)</storage>
          <response_shape>
            <field name="fund">FundCode</field>
            <field name="account">string | null</field>
            <field name="versions">VersionMetadata[] — { versionId, exportedAt, strategy, tradesCount, overridesCount, uploadedBy, s3Key, submissionId?: string (present on export-and-submit versions), tradeCsvKey?: string }</field>
            <field name="hasMore">boolean</field>
          </response_shape>
          <portal_endpoint>listVersions() in portfolio.ts:486; called by useVersions hook in usePortfolioApi.ts:233</portal_endpoint>
        </source>

        <source id="pm-get-version">
          <lambda_function>opal-portfolio-version-get</lambda_function>
          <source_path>infra/aws/lambda/portfolio_version_get/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>GET /api/private/portfolio/versions/{fund}/{account}/{versionId} (JWT, internal)</trigger>
          <storage>S3 (source not available — key pattern: {s3Key} from VersionMetadata)</storage>
          <response_shape>
            <field name="versionId">string</field>
            <field name="fund">FundCode</field>
            <field name="account">string | null</field>
            <field name="strategy">StrategyType</field>
            <field name="trades">EditableTrade[]</field>
            <field name="metrics">PortfolioMetrics</field>
            <field name="exportedAt">ISO8601</field>
            <field name="uploadedBy">string (email)</field>
          </response_shape>
          <portal_endpoint>loadVersion() in portfolio.ts:500; called by useLoadVersion hook</portal_endpoint>
        </source>

        <source id="pm-export-download">
          <lambda_function>opal-portfolio-export-download</lambda_function>
          <source_path>infra/aws/lambda/portfolio_export_download/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>GET /api/private/portfolio/exports/{fund}/{account}/{versionId}/download (JWT, internal)</trigger>
          <storage>S3: generates presigned GET URL for Vident Trade CSV (tradeCsvKey from VersionMetadata)</storage>
          <response_shape>
            <field name="presignedUrl">string (temporary S3 presigned URL)</field>
            <field name="filename">string</field>
          </response_shape>
          <portal_endpoint>getExportDownloadUrl() in portfolio.ts:472; called directly from HistoryTab.tsx:8</portal_endpoint>
        </source>

        <source id="pm-list-drafts-for-trade">
          <lambda_function>opal-pm-snapshot-handler</lambda_function>
          <source_path>infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py (FOUND locally)</source_path>
          <trigger>GET /api/private/trade-submission/pm-drafts/{fund} (JWT, internal; consumed by TradeSubmission page, not PortfolioManagement)</trigger>
          <storage>DynamoDB table: opal-pm-snapshots; GSI: fund-created-index; filter: status=DRAFT</storage>
          <response_shape>
            <field name="drafts">DraftSummary[] — { snapshotId, createdAt, optimizationDate, summary: { totalTrades, buyTurnover, sellTurnover } }</field>
            <field name="fund">string</field>
          </response_shape>
          <portal_endpoint>Not currently wired to an active portal hook; available for future TradeSubmission integration</portal_endpoint>
        </source>

      </read_paths>

      <write_paths>

        <sink id="pm-upload-files">
          <lambda_function>opal-pm-upload-urls (generates presigned URLs); direct S3 PUT from browser (no Lambda on upload path)</lambda_function>
          <source_path>infra/aws/lambda/opal_pm_upload_urls/lambda_function.py (FOUND locally)</source_path>
          <trigger>User action: upload alpha.pkl and optimization.xlsx via UploadPortfolioModal</trigger>
          <storage>S3 bucket: opal-data-pm; key pattern: {fund}/alpha/{date}.pkl and {fund}/optimization/{date}.xlsx</storage>
          <payload_shape>
            <field name="step1_presign_request">GET /api/private/portfolio-management/upload-urls?fund={fund}&amp;date={date}</field>
            <field name="step1_response">{ alphaPklUrl, optimizationXlsxUrl, expiresIn: 900, paths: { alphaPkl: {fund}/alpha/{date}.pkl, optimizationXlsx: {fund}/optimization/{date}.xlsx }, bucket: opal-data-pm }</field>
            <field name="step2_upload">HTTP PUT to presigned URL; Content-Type: application/octet-stream (pkl) or application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (xlsx); 15-minute expiry</field>
            <field name="auth">JWT tier=internal required for presign; presigned URL is public (self-contained credentials)</field>
          </payload_shape>
        </sink>

        <sink id="pm-optimization-autosave">
          <lambda_function>opal-pm-optimization-autosave-put</lambda_function>
          <source_path>infra/aws/lambda/portfolio_optimization_autosave_put/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>Automatic: useOptimizationAutoSave hook fires every 60 seconds while PM is in the optimization session</trigger>
          <storage>S3 bucket: opal-data-pm (inferred — bucket not confirmed from source)</storage>
          <payload_shape>
            <field name="endpoint">PUT /api/private/portfolio/optimization-autosave/{fund}/{account}</field>
            <field name="body">{ sessionId: string, optimizationDate: string, modelDate: string, securities: Security[], alphaFactors: AlphaFactor[], sectorAllocations: SectorAllocation[], modelCoefficients: ModelCoefficient[], modelGroups: ModelGroup[], riskFactors: RiskFactor[], summary: PortfolioSummary, overridesCount: number }</field>
            <field name="note">FULL state save (not delta). Overwrites entire autosave for this fund/account session. Distinct from opal-portfolio-autosave-put (legacy delta path).</field>
          </payload_shape>
        </sink>

        <sink id="pm-legacy-autosave">
          <lambda_function>opal-portfolio-autosave-put</lambda_function>
          <source_path>infra/aws/lambda/portfolio_autosave_put/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>Automatic: useAutoSave (legacy) hook fires every 60 seconds; sends ONLY changed trades (delta)</trigger>
          <storage>S3 bucket: opal-data-pm (inferred); backend fetches existing 505-trade record, merges changedTrades, saves back</storage>
          <payload_shape>
            <field name="endpoint">PUT /api/private/portfolio/autosave/{fund}/{account}</field>
            <field name="body">{ sessionId: string, changedTrades: Partial&lt;EditableTrade&gt;[], overridesCount: number }</field>
            <field name="note">Legacy path. Being superseded by opal-pm-optimization-autosave-put. Both run concurrently at 60s intervals.</field>
          </payload_shape>
        </sink>

        <sink id="pm-save-snapshot">
          <lambda_function>opal-pm-snapshot-handler</lambda_function>
          <source_path>infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py (FOUND locally)</source_path>
          <trigger>User action: Save Snapshot button in TradeTab</trigger>
          <storage>DynamoDB table: opal-pm-snapshots; item size limit: 400KB</storage>
          <payload_shape>
            <field name="endpoint">POST /api/private/portfolio-management/snapshot</field>
            <field name="body">{ fund, optimizationDate, securities: Security[], summary, alphaFactors, sectorAllocations, modelCoefficients, riskFactors, status: DRAFT|SUBMITTED, notes? }</field>
            <field name="key_generated">snapshot_id = {fund}#{YYYYMMDD-HHmmss} (UTC, server-side)</field>
            <field name="user_id">Injected from JWT by auth-validator-edge (CloudFront Lambda@Edge); request body userId is ignored</field>
            <field name="response">{ snapshotId, fund, createdAt, status }</field>
          </payload_shape>
        </sink>

        <sink id="pm-delete-snapshot">
          <lambda_function>opal-pm-snapshot-handler</lambda_function>
          <source_path>infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py (FOUND locally)</source_path>
          <trigger>User action: Delete Snapshot button (DRAFT only)</trigger>
          <storage>DynamoDB table: opal-pm-snapshots</storage>
          <payload_shape>
            <field name="endpoint">DELETE /api/private/portfolio-management/snapshot/{snapshotId}</field>
            <field name="constraint">Only DRAFT status snapshots can be deleted. SUBMITTED snapshots return 403.</field>
          </payload_shape>
        </sink>

        <sink id="pm-export-and-submit">
          <lambda_function>opal-portfolio-excel-generator (inferred from lambda-source-map.json); creates TradeSubmission DynamoDB record</lambda_function>
          <source_path>infra/aws/lambda/portfolio_excel_generator/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>User action: Export and Submit in ExportModal (TradeTab) — THE PM-to-TradeSubmission bridge</trigger>
          <storage>S3: Vident Trade CSV written to opal-data-pm or portfolio-management bucket (key stored in tradeCsvKey); DynamoDB: TradeSubmission record created with status PENDING_APPROVAL</storage>
          <payload_shape>
            <field name="endpoint">POST /api/private/portfolio/export-and-submit</field>
            <field name="body">{ fund, account, destination: string, weightsAsOf: YYYY-MM-DD, tradesAsOf: YYYY-MM-DD, tradeComments, otherComments?, attestations: { guidelines: bool, liquidity: bool, restricted: bool, execution: bool }, securities: Security[], initiatorEmail, initiatorName }</field>
            <field name="response">{ versionId, submissionId, tradeCsvUrl, tradeCsvKey, exportedAt: ISO8601, totalSecurities: number, tradeCount: number }</field>
            <field name="cross_pod_effect">submissionId appears immediately in TradeSubmission Approvals tab (GET /api/general/trades/submissions/pending refetches every 15s)</field>
          </payload_shape>
        </sink>

        <sink id="pm-upload-pickle-legacy">
          <lambda_function>opal-portfolio-pickle-parser</lambda_function>
          <source_path>infra/aws/lambda/portfolio_pickle_parser/lambda_function.py (NOT FOUND locally; registered in lambda-source-map.json)</source_path>
          <trigger>User action: PKL file upload (DataRefresh page or legacy direct upload path)</trigger>
          <storage>S3 bucket: opal-data-pm (inferred); also creates initial auto-save</storage>
          <payload_shape>
            <field name="endpoint">POST /api/private/portfolio/parse-pickle</field>
            <field name="body">{ file: base64-encoded PKL, filename: string, fund?: FundCode, account?: string, strategy?: StrategyType }</field>
            <field name="response_simple">ImportData — { strategy, weightsAsOf, uploadDate, trades: TradeRecord[], metrics: PortfolioMetrics }</field>
            <field name="response_full">UploadResponse — { sessionId, fund, account, s3Keys: { upload, autosave }, data: { strategy, trades: EditableTrade[], metrics, asOfDate?, weightsAsOf?, tradesAsOf? } }</field>
          </payload_shape>
        </sink>

      </write_paths>
    </page>

    <!-- ============================================================ -->
    <!-- PAGE: TradeSubmission                                         -->
    <!-- ============================================================ -->
    <page>
      <name>TradeSubmission</name>
      <description>
        Trade approval and execution portal. Four tabs: Submit (initiate), Approvals
        (PENDING_APPROVAL queue, 15s refetch), Execution (APPROVED queue, 20s refetch),
        History (COMPLETE/REJECTED, paginated 20/page). Backend: three Lambdas
        (trade-submission-handler, trade-workflow-handler, trade-dashboard-api).
        Uses publicApiRequest (no JWT scope) — auth enforced at Lambda business logic level.
      </description>

      <read_paths>

        <source id="ts-pending-approvals">
          <lambda_function>trade-dashboard-api</lambda_function>
          <source_path>Source not found in local repo; not registered in lambda-source-map.json</source_path>
          <trigger>GET /api/general/trades/submissions/pending; React Query refetch every 15s</trigger>
          <storage>DynamoDB (table name not confirmed — source unavailable)</storage>
          <response_shape>
            <field name="count">number</field>
            <field name="submissions">TradeSubmission[] — full submission objects with PENDING_APPROVAL status</field>
          </response_shape>
          <portal_endpoint>getPendingApprovals() in trade-submission.ts:316; called by usePendingApprovals hook in useTradeSubmissionState.ts:45</portal_endpoint>
        </source>

        <source id="ts-all-submissions">
          <lambda_function>trade-dashboard-api</lambda_function>
          <trigger>GET /api/general/trades/submissions; refetch 30s</trigger>
          <storage>DynamoDB (most-recent-first sort)</storage>
          <response_shape>
            <field name="submissions">TradeSubmission[]</field>
            <field name="count">number</field>
          </response_shape>
          <portal_endpoint>getAllSubmissions() in trade-submission.ts:309; called by useAllSubmissions hook</portal_endpoint>
        </source>

        <source id="ts-my-submissions">
          <lambda_function>trade-dashboard-api</lambda_function>
          <trigger>GET /api/general/trades/submissions/by-initiator?email={email}; refetch 30s</trigger>
          <storage>DynamoDB GSI on initiator_email</storage>
          <response_shape>
            <field name="submissions">TradeSubmission[]</field>
            <field name="count">number</field>
            <field name="initiator">string (email)</field>
          </response_shape>
          <portal_endpoint>getMySubmissions() in trade-submission.ts:323; called by useMySubmissions hook in useTradeSubmissionState.ts:58</portal_endpoint>
        </source>

        <source id="ts-submissions-by-status">
          <lambda_function>trade-dashboard-api</lambda_function>
          <trigger>GET /api/general/trades/submissions/by-status?status={status}; refetch varies (APPROVED: 20s, EXECUTED|COMPLETE|REJECTED: 30-60s)</trigger>
          <storage>DynamoDB GSI on status</storage>
          <response_shape>
            <field name="submissions">TradeSubmission[]</field>
            <field name="count">number</field>
            <field name="status">string</field>
          </response_shape>
          <portal_endpoint>getSubmissionsByStatus() in trade-submission.ts:343; called by useApprovedSubmissions, useExecutedSubmissions, useCompletedSubmissions, useRejectedSubmissions hooks</portal_endpoint>
        </source>

        <source id="ts-excel-download">
          <lambda_function>trade-dashboard-api</lambda_function>
          <trigger>GET /api/general/trades/submissions/{submissionId}/excel; on-demand (user downloads Vident Excel template)</trigger>
          <storage>S3: returns presigned GET URL for excel_s3_key stored on the TradeSubmission record</storage>
          <response_shape>
            <field name="presigned_url">string (auto-opened in new tab by portal)</field>
            <field name="expires_in">number (seconds)</field>
            <field name="filename">string</field>
          </response_shape>
          <portal_endpoint>downloadExcelFile() in trade-submission.ts:365; called by useTradeSubmissionActions.ts:182</portal_endpoint>
        </source>

        <source id="ts-identifier-search">
          <lambda_function>trade-dashboard-api (or trade-submission-handler — not confirmed)</lambda_function>
          <trigger>GET /api/general/trades/identifiers/search?q={query}; on-demand, minimum 2-char query</trigger>
          <storage>DynamoDB or search index for SecurityIdentifier cache (frequency-ranked)</storage>
          <response_shape>
            <field name="identifiers">SecurityIdentifier[] — up to 10 results: { ticker, sedol?, isin?, figi?, last_seen?, source?, occurrences? }</field>
            <field name="count">number</field>
          </response_shape>
          <portal_endpoint>searchIdentifierCache() in trade-submission.ts:389; called by TickerAutocompleteInput.tsx. Also reused by searchSecurities() in portfolio-optimization.ts:185 for PM SecurityLookupModal.</portal_endpoint>
        </source>

      </read_paths>

      <write_paths>

        <sink id="ts-submit-trade">
          <lambda_function>trade-submission-handler</lambda_function>
          <source_path>Source not found in local repo; not registered in lambda-source-map.json</source_path>
          <trigger>User action: Submit button in SubmitTab (after all attestation checkboxes confirmed)</trigger>
          <storage>DynamoDB: creates TradeSubmission record with status PENDING_APPROVAL; S3: Excel/CSV file stored at excel_s3_key</storage>
          <payload_shape>
            <field name="endpoint">POST /api/general/trades/submit</field>
            <field name="body">{ fund: Fund, brokerage: vident|schwab|fidelity|other, weights_as_of: YYYY-MM-DD, proposed_trades_as_of: YYYY-MM-DD, trade_comments?: string, other_comments?: string, attestations: { portfolio_reviewed: bool, trade_rationale_documented: bool, compliance_approved: bool, pre_trade_analysis_complete?: bool }, securities: TradeSecurity[], initiator_email: string, initiator_name: string }</field>
            <field name="TradeSecurity_shape">{ ticker, sedol?, isin?, figi?, current_weight?, proposed_weight?, delta?, trade_instruction?: BUY|SELL|HOLD, comments?, shares?, side?: buy|sell, price?, notes? }</field>
            <field name="response">TradeSubmission — full record with submission_id (format: TRADE-{YYYYMMDD}-{HHmmss}-{A1B2C3}), status: PENDING_APPROVAL, created_at, submitted_at, brokerage_email_sent, submission_date</field>
          </payload_shape>
        </sink>

        <sink id="ts-workflow-approve">
          <lambda_function>trade-workflow-handler</lambda_function>
          <source_path>Source not found in local repo; not registered in lambda-source-map.json</source_path>
          <trigger>User action: Approve button in ApproveModal (Approvals tab); requires approver auth</trigger>
          <storage>DynamoDB: updates TradeSubmission status PENDING_APPROVAL -&gt; APPROVED; sets approved_at, approver_email, approver_name</storage>
          <payload_shape>
            <field name="endpoint">POST /api/general/trades/workflow</field>
            <field name="body">{ action: 'approve', submission_id, user_email, user_name }</field>
            <field name="response">WorkflowActionResponse — { success: bool, submission: TradeSubmission, message: string }</field>
          </payload_shape>
        </sink>

        <sink id="ts-workflow-reject">
          <lambda_function>trade-workflow-handler</lambda_function>
          <trigger>User action: Reject button in RejectModal; rejection_reason required</trigger>
          <storage>DynamoDB: updates status to REJECTED; sets rejected_at, rejection_reason</storage>
          <payload_shape>
            <field name="endpoint">POST /api/general/trades/workflow</field>
            <field name="body">{ action: 'reject', submission_id, user_email, user_name, rejection_reason: string (required) }</field>
          </payload_shape>
        </sink>

        <sink id="ts-workflow-execute">
          <lambda_function>trade-workflow-handler</lambda_function>
          <trigger>User action: Execute button in ExecuteModal (Execution tab); shows brokerage destination</trigger>
          <storage>DynamoDB: updates status APPROVED -&gt; EXECUTED; sets executed_at, executor_email, executor_name</storage>
          <payload_shape>
            <field name="endpoint">POST /api/general/trades/workflow</field>
            <field name="body">{ action: 'execute', submission_id, user_email, user_name }</field>
          </payload_shape>
        </sink>

        <sink id="ts-workflow-complete">
          <lambda_function>trade-workflow-handler</lambda_function>
          <trigger>System or admin action: mark EXECUTED -&gt; COMPLETE (not surfaced in current UI — may be auto-triggered post-execution)</trigger>
          <storage>DynamoDB: updates status to COMPLETE; sets completed_at</storage>
          <payload_shape>
            <field name="endpoint">POST /api/general/trades/workflow</field>
            <field name="body">{ action: 'complete', submission_id, user_email, user_name }</field>
          </payload_shape>
        </sink>

        <sink id="ts-batch-save-identifiers">
          <lambda_function>trade-submission-handler (or trade-dashboard-api — not confirmed)</lambda_function>
          <trigger>Automatic: fires after successful trade submission to increment occurrence counts for all submitted security tickers</trigger>
          <storage>DynamoDB or search index: upserts SecurityIdentifier records; increments occurrences field</storage>
          <payload_shape>
            <field name="endpoint">POST /api/general/trades/identifiers/batch</field>
            <field name="body">{ identifiers: [{ ticker, sedol?, isin?, figi?, source: 'upload' }] }</field>
            <field name="response">{ saved: number, errors: string[] | null }</field>
          </payload_shape>
        </sink>

      </write_paths>
    </page>

    <!-- ============================================================ -->
    <!-- PAGE: DataRefresh                                             -->
    <!-- ============================================================ -->
    <page>
      <name>DataRefresh</name>
      <description>
        Admin/ops-only page (requires Dev userType JWT claim). Triggers the Yang
        pipeline to regenerate PortfolioAnalytics and MarketIntelligence data.
        Upload tab: file drop, pipeline progress (Step Functions polling every 3s).
        History tab: past executions, rollback. CurrentStatePanel: live manifest.json
        data freshness. All routes require scoped API access.
      </description>

      <read_paths>

        <source id="dr-pipeline-status">
          <lambda_function>opal-data-refresh-api</lambda_function>
          <source_path>infra/aws/lambda/data_refresh/lambda_function.py (FOUND locally)</source_path>
          <trigger>GET /api/scoped/data-refresh/status/{executionId}; polled every 3s until terminal state (SUCCEEDED|FAILED|TIMED_OUT|ABORTED)</trigger>
          <storage>AWS Step Functions: describeExecution on YangDataPipeline state machine (ARN: arn:aws:states:us-east-1:313476888478:stateMachine:YangDataPipeline)</storage>
          <response_shape>
            <field name="status">RUNNING | SUCCEEDED | FAILED | TIMED_OUT | ABORTED</field>
            <field name="steps">DataRefreshStep[] — grouped Step Functions steps with status per step</field>
            <field name="currentStep">string</field>
            <field name="executionArn">string</field>
            <field name="error">string | null</field>
          </response_shape>
          <portal_endpoint>getDataRefreshStatus() in portal-proxy.ts line ~1838; called by useDataRefreshState.ts:159</portal_endpoint>
        </source>

        <source id="dr-execution-history">
          <lambda_function>opal-data-refresh-api</lambda_function>
          <source_path>infra/aws/lambda/data_refresh/lambda_function.py (FOUND locally)</source_path>
          <trigger>GET /api/scoped/data-refresh/history?limit={limit}; default limit 20; on-demand (History tab load)</trigger>
          <storage>DynamoDB table: opal-data-refresh-executions</storage>
          <response_shape>
            <field name="executions">DataRefreshHistory[] — { executionId, status, data_as_of, files_processed, duration, triggered_by, created_at }</field>
          </response_shape>
          <portal_endpoint>getDataRefreshHistory() in portal-proxy.ts; called by useDataRefreshState.ts:418</portal_endpoint>
        </source>

        <source id="dr-manifest-freshness">
          <lambda_function>None — direct S3 read via portal-proxy</lambda_function>
          <trigger>GET /api/general/json/latest/manifest.json; React Query with caching; Bearer token from localStorage</trigger>
          <storage>S3 bucket: opal-data-portal-v2; key: json/latest/manifest.json (written by yang-pipeline-trigger as yang-pipeline-metadata.json and by yang-generate-manifest Lambda)</storage>
          <response_shape>
            <field name="generated_at">ISO8601</field>
            <field name="pipeline_execution_id">string (UUID)</field>
            <field name="per-source">data_as_of: YYYY-MM-DD, updated_at: ISO8601 per data source (data_pkl, model_pkl, etc.)</field>
            <field name="freshness_categories">Fresh / Aging / Stale based on age thresholds (thresholds in CurrentStatePanel)</field>
          </response_shape>
          <portal_endpoint>CurrentStatePanel component in DataRefresh; direct fetch in useDataRefreshState.ts</portal_endpoint>
        </source>

      </read_paths>

      <write_paths>

        <sink id="dr-get-upload-urls">
          <lambda_function>opal-data-refresh-api</lambda_function>
          <source_path>infra/aws/lambda/data_refresh/lambda_function.py (FOUND locally)</source_path>
          <trigger>User action: file selection in FileDropZone (step 1 of upload flow)</trigger>
          <storage>S3 bucket: opal-data-portal-v2; staging prefix inferred from uploadId</storage>
          <payload_shape>
            <field name="endpoint">POST /api/scoped/data-refresh/upload-urls</field>
            <field name="body">{ fileInfo: [{ name: string, size: number }] }</field>
            <field name="response">{ uploadId: string, urls: Record&lt;filename, presignedUrl&gt; }</field>
            <field name="allowed_extensions">.pkl, .json, .xlsx, .csv (validated in Lambda)</field>
          </payload_shape>
        </sink>

        <sink id="dr-upload-to-s3">
          <lambda_function>None — direct XHR PUT to presigned URL</lambda_function>
          <trigger>Automatic: fires per file after upload-urls response</trigger>
          <storage>S3 bucket: opal-data-portal-v2; staging path derived from uploadId</storage>
          <payload_shape>
            <field name="method">XMLHttpRequest PUT to presigned S3 URL (per-file, with onprogress callback for UI progress bar)</field>
          </payload_shape>
        </sink>

        <sink id="dr-trigger-pipeline">
          <lambda_function>opal-data-refresh-api (API side); yang-pipeline-trigger (S3 event side)</lambda_function>
          <source_path>infra/aws/lambda/data_refresh/lambda_function.py (FOUND locally); infra/aws/lambda/v2_portal/yang_pipeline/orchestration/trigger/lambda_function.py (FOUND locally)</source_path>
          <trigger>User action: Trigger button after file uploads complete</trigger>
          <storage>
            opal-data-refresh-api: moves staged files to opal-data-portal-v2/uploads/; creates manifest.json at uploads/manifest.json; writes execution record to DynamoDB opal-data-refresh-executions.
            S3 event on uploads/manifest.json triggers yang-pipeline-trigger Lambda.
            yang-pipeline-trigger: reads manifest, generates pipeline_execution_id (UUID), writes json/yang-pipeline-metadata.json and json/latest/{file_type}.json to opal-data-portal-v2, starts YangDataPipeline Step Functions execution.
          </storage>
          <payload_shape>
            <field name="endpoint">POST /api/scoped/data-refresh/trigger</field>
            <field name="body">{ uploadId: string }</field>
            <field name="response">{ executionId: string }</field>
            <field name="conflict_behavior">409 Conflict if pipeline already running (yang-pipeline-trigger checks Step Functions for RUNNING executions; alerts if stuck more than 600s)</field>
          </payload_shape>
        </sink>

        <sink id="dr-rollback">
          <lambda_function>opal-data-refresh-api</lambda_function>
          <source_path>infra/aws/lambda/data_refresh/lambda_function.py (FOUND locally)</source_path>
          <trigger>User action: Rollback button in History tab</trigger>
          <storage>S3: re-uses archived files from a prior execution; DynamoDB opal-data-refresh-executions; starts new Step Functions execution</storage>
          <payload_shape>
            <field name="endpoint">POST /api/scoped/data-refresh/rollback</field>
            <field name="body">{ executionId: string }</field>
            <field name="response">{ newExecutionId: string }</field>
          </payload_shape>
        </sink>

      </write_paths>
    </page>

  </page_contracts>

  <!-- ================================================================== -->
  <!-- CRITICAL FLOWS                                                       -->
  <!-- ================================================================== -->

  <critical_flows>

    <flow name="pm-upload-to-optimization">
      <description>
        PM user uploads new alpha.pkl and optimization.xlsx files. Portal reads
        those files to populate the Trade tab with fresh optimization data.
      </description>
      <steps>
        <step order="1">PM user opens UploadPortfolioModal in PortfolioManagement Trade tab</step>
        <step order="2">Portal calls GET /api/private/portfolio-management/upload-urls?fund={fund}&amp;date={date} (opal-pm-upload-urls Lambda)</step>
        <step order="3">Lambda validates fund (PFDE|PFOE|TAX), date (YYYYMMDD), and JWT tier=internal; returns presigned PUT URLs with 15-minute expiry</step>
        <step order="4">Portal uses XMLHttpRequest PUT to upload alpha.pkl to opal-data-pm/{fund}/alpha/{date}.pkl</step>
        <step order="5">Portal uses XMLHttpRequest PUT to upload optimization.xlsx to opal-data-pm/{fund}/optimization/{date}.xlsx</step>
        <step order="6">PM user navigates to the optimization view (or triggers reload)</step>
        <step order="7">Portal calls GET /api/private/portfolio-management/load?fund={fund}&amp;date={date} (opal-pm-optimization-loader Lambda)</step>
        <step order="8">opal-pm-optimization-loader reads alpha.pkl and optimization.xlsx from opal-data-pm, transforms to optimization response shape, returns 503 securities with 33 factors</step>
        <step order="9">Portal populates useOptimizationState with securities, alpha/sector/model/risk data, summary, and optimization dates</step>
      </steps>
      <note>
        The task order requirement listed yang-pipeline-trigger, yang-validate-files, yang-ingest-dynamodb,
        and yang-move-to-processed as steps in this flow. Based on Lambda source code, the PM upload target
        is opal-data-pm while yang-pipeline-trigger watches opal-data-portal-v2/uploads/manifest.json.
        These are SEPARATE trigger paths. The yang-pipeline-trigger connection to PM uploads could not be
        confirmed from source — see gaps section.
      </note>
    </flow>

    <flow name="datarefresh-to-yang-pipeline">
      <description>
        Dev user triggers full portal data regeneration. Yang pipeline Step Functions
        executes generate-* Lambdas (owned by DS_PortfolioAnalytics) and ingests
        market data (owned by DS_MarketIntelligence).
      </description>
      <steps>
        <step order="1">Dev user on DataRefresh page uploads PKL, Excel, CSV files via FileDropZone</step>
        <step order="2">POST /api/scoped/data-refresh/upload-urls returns { uploadId, presigned PUT URLs per file } (opal-data-refresh-api)</step>
        <step order="3">XHR PUTs upload files to opal-data-portal-v2 staging path (uploadId-scoped)</step>
        <step order="4">POST /api/scoped/data-refresh/trigger moves files to opal-data-portal-v2/uploads/ and creates manifest.json</step>
        <step order="5">S3 event on uploads/manifest.json triggers yang-pipeline-trigger Lambda</step>
        <step order="6">yang-pipeline-trigger reads manifest; extracts data_as_of_date from manifest date field (YYYYMMDD -&gt; YYYY-MM-DD); generates pipeline_execution_id (UUID); writes json/yang-pipeline-metadata.json and json/latest/{file_type}.json to opal-data-portal-v2</step>
        <step order="7">yang-pipeline-trigger starts YangDataPipeline Step Functions (ARN: arn:aws:states:us-east-1:313476888478:stateMachine:YangDataPipeline); returns 409 if already RUNNING</step>
        <step order="8">Step Functions: yang-validate-files verifies all manifest-listed files exist in uploads/ prefix of opal-data-portal-v2; returns manifest + file_metadata</step>
        <step order="9">Step Functions: yang-move-to-processed copies PKL files from uploads/ to opal-data-portal-v2/benchmarks/ with canonical naming ({file_type}_{YYYYMMDD}_{version}.pkl)</step>
        <step order="10">Step Functions: yang-ingest-dynamodb reads data PKL, ingests market data to opal-portal-market-data DynamoDB table (DAILY#YYYY-MM-DD entries and LATEST entries — used by MarketIntelligence pod)</step>
        <step order="11">Step Functions: yang-generate-* Lambdas (DS_PortfolioAnalytics scope) execute positioning, attribution, factor tilts, valuation, macroeconomics, correlation generators — write JSON views to opal-data-portal-v2/json/</step>
        <step order="12">Portal polls GET /api/scoped/data-refresh/status/{executionId} every 3s; displays PipelineProgress grouped by step until terminal state</step>
        <step order="13">On SUCCEEDED: Portal shows navigation links to Valuation, Market Overview, Model Portfolios pages</step>
      </steps>
    </flow>

    <flow name="export-and-submit-to-tradesubmission">
      <description>
        PM user completes optimization, reviews Trade tab, and triggers Export-and-Submit.
        This is the primary PM-to-operations handoff — creates a trade submission
        record that appears in TradeSubmission's Approvals tab for review and execution.
      </description>
      <steps>
        <step order="1">PM user reviews Trade tab (503 securities with optimizedWeight and finalTrade columns), confirms override weights and trade instructions</step>
        <step order="2">PM user opens ExportModal, selects destination (brokerage), reviews attestation checkboxes, confirms Export and Submit</step>
        <step order="3">Portal calls POST /api/private/portfolio/export-and-submit with full ExportAndSubmitRequest (fund, account, destination, weightsAsOf, tradesAsOf, attestations, securities[], initiatorEmail, initiatorName)</step>
        <step order="4">Backend Lambda (opal-portfolio-excel-generator inferred) generates Vident Trade CSV from securities data; uploads to S3</step>
        <step order="5">Backend creates TradeSubmission DynamoDB record with status PENDING_APPROVAL, submissionId (format: TRADE-{YYYYMMDD}-{HHmmss}-{random}), excel_s3_key pointing to Vident CSV</step>
        <step order="6">Response returns { versionId, submissionId, tradeCsvUrl, tradeCsvKey, exportedAt, totalSecurities, tradeCount }</step>
        <step order="7">PM History tab displays this version's submissionId as a navigation link to TradeSubmission page</step>
        <step order="8">TradeSubmission Approvals tab (polling GET /api/general/trades/submissions/pending every 15s) picks up new PENDING_APPROVAL record</step>
        <step order="9">Approver in TradeSubmission: POST /api/general/trades/workflow action=approve (trade-workflow-handler) -&gt; APPROVED</step>
        <step order="10">Executor in TradeSubmission: POST /api/general/trades/workflow action=execute -&gt; EXECUTED; sends to brokerage</step>
        <step order="11">TradeSubmission: POST /api/general/trades/workflow action=complete -&gt; COMPLETE (auto-triggered or admin action)</step>
      </steps>
    </flow>

    <flow name="trade-lifecycle-state-machine">
      <description>Complete trade status progression and rejection paths.</description>
      <steps>
        <step order="1">PENDING_APPROVAL (created by export-and-submit or manual submit via SubmitTab)</step>
        <step order="2a">approve action -&gt; APPROVED (appears in Execution tab)</step>
        <step order="2b">reject action (from PENDING_APPROVAL) -&gt; REJECTED (appears in History tab)</step>
        <step order="3">execute action (from APPROVED) -&gt; EXECUTED</step>
        <step order="3b">reject action (from APPROVED) -&gt; REJECTED</step>
        <step order="4">complete action (from EXECUTED) -&gt; COMPLETE (appears in History tab)</step>
      </steps>
      <note>All transitions via POST /api/general/trades/workflow. rejection_reason required for reject action. All actions require user_email and user_name for audit trail.</note>
    </flow>

  </critical_flows>

  <!-- ================================================================== -->
  <!-- UPSTREAM DEPENDENCIES                                                -->
  <!-- ================================================================== -->

  <upstream_dependencies>

    <dependency name="Yang PKL and Excel Files (PM optimization inputs)">
      <description>
        Yang produces alpha.pkl and optimization.xlsx as outputs of its optimization run.
        These files are the raw inputs for the PortfolioManagement optimization workbench.
        PM users upload them via opal-pm-upload-urls presigned URLs to opal-data-pm.
        File naming convention: alpha {YYYYMMDD}.pkl, optimization-{YYYYMMDD}.xlsx.
        Date is extracted from filename (YYYYMMDD pattern) to set optimizationDate.
      </description>
      <source_system>Yang (external; optimization engine)</source_system>
      <storage>S3 bucket: opal-data-pm; keys: {fund}/alpha/{date}.pkl, {fund}/optimization/{date}.xlsx</storage>
    </dependency>

    <dependency name="Yang Pipeline Data Files (DataRefresh inputs)">
      <description>
        Yang produces data PKL (data YYYYMMDD vN.pkl), model PKL (model YYYYMMDD vN.pkl),
        regression CSV, peer Excel, attribution Excel, CMA Excel, SAA Excel.
        These are uploaded via DataRefresh to trigger the yang pipeline Step Functions.
        File type config in yang-pipeline-trigger: data_pkl (weekly), model_pkl (weekly),
        regression_csv (weekly), peer_excel (monthly), attribution_excel (monthly),
        cma_excel (annually), saa_excel (monthly).
      </description>
      <source_system>Yang (external; data pipeline)</source_system>
      <storage>S3 bucket: opal-data-portal-v2; upload path: uploads/{filename}; processed path: benchmarks/{canonical_name}</storage>
    </dependency>

    <dependency name="SmartX Fund Universe (DataRefresh side effect)">
      <description>
        opal-smartx-ingestion-pipeline Lambda is triggered by EC2 completing CSV upload
        to s3://opal-data-smartx-v2/exports/run-XXXXX/. Pipeline: consolidate CSVs to Parquet,
        append AUM to DynamoDB, generate portal JSON views (aum-timeseries.json append-only),
        AUM metrics (aum-metrics.json), account distribution, detailed model portfolio views.
        Output: opal-data-portal-v2/json/portfolios/ and opal-data-portal-v2/json/model_portfolios/views/.
        This is NOT triggered by DataRefresh — it runs on SmartX EC2 upload completion independently.
      </description>
      <source_system>SmartX EC2 (external; transaction data export)</source_system>
      <storage>
        Source: opal-data-smartx-v2/consolidated/
        DynamoDB: opal-portal-market-data (AUM timeseries)
        Output JSON: opal-data-portal-v2/json/portfolios/, opal-data-portal-v2/json/model_portfolios/views/
      </storage>
    </dependency>

    <dependency name="JWT Auth (CloudFront Lambda@Edge)">
      <description>
        All /api/private/* routes require JWT validated by auth-validator-edge.
        User context (X-User-Email, X-User-Tier) injected as headers.
        Tier must be 'internal' for PM and portfolio Lambdas.
        DataRefresh requires userType 'Dev' claim in JWT.
        TradeSubmission uses publicApiRequest (no JWT scope) — identity from user_email field in request body.
      </description>
    </dependency>

  </upstream_dependencies>

  <!-- ================================================================== -->
  <!-- DATA QUALITY NOTES                                                   -->
  <!-- ================================================================== -->

  <data_quality_notes>

    <note id="dq-1" severity="HIGH">
      Dual auto-save race condition risk: opal-pm-optimization-autosave-put (full state, 60s) and
      opal-portfolio-autosave-put (legacy delta, 60s) both run concurrently. If the legacy path
      reads and merges the existing 505-trade record at the same time the optimization path writes,
      the result could be partial state. No lock or transaction coordination exists between the two
      paths based on available source code.
    </note>

    <note id="dq-2" severity="MEDIUM">
      DynamoDB item size risk for snapshots: opal-pm-snapshot-handler stores full securities arrays
      as JSON strings. A 503-security array with 33 factors each can exceed the 400KB DynamoDB limit.
      Lambda logs a warning at item_size &gt; 400KB but does not fail the put_item call — the DynamoDB
      service will return an error if the limit is exceeded. No S3 overflow path exists.
    </note>

    <note id="dq-3" severity="MEDIUM">
      Summary stats are partially stubbed: predictedBeta, totalRisk, assetSelection, and commonFactor
      in PortfolioSummary are calculated stubs in useOptimizationCalculations.ts (lines 61-64). The
      UI displays these as 0 or placeholder values. They are saved as-is in auto-saves and snapshots.
    </note>

    <note id="dq-4" severity="MEDIUM">
      AUM is hardcoded at $100M default in usePortfolioEditStore.ts:143. The optimization loader
      may return aum in the summary, but the edit store does not pull from it. Export and submission
      summary stats using AUM (turnover cost estimates) will be based on the default.
    </note>

    <note id="dq-5" severity="LOW">
      SEDOL/ISIN/FIGI not populated in transformToExportTrade (portfolio.ts:343-349). The ExportTrade
      sent to export-and-submit has sedol: undefined, isin: undefined, figi: undefined. These fields
      are present in TradeSubmission's TradeSecurity type but will be empty on PM-sourced submissions.
    </note>

    <note id="dq-6" severity="LOW">
      yang-pipeline-trigger: if execution age exceeds 600s, Lambda logs an alert but still returns
      409 — it does not auto-terminate the stuck execution. Manual intervention (Step Functions console)
      is required.
    </note>

    <note id="dq-7" severity="LOW">
      TradeSubmission uses publicApiRequest (no JWT scope). Identity relies solely on user_email
      in request body. No RBAC enforcement at the API gateway level — all business logic enforcement
      is in the Lambda functions. Approver/executor identity can be set to any email string by the client.
    </note>

    <note id="dq-8" severity="LOW">
      opal-smartx-ingestion-pipeline uses emoji characters in logger.info calls (e.g., "checkmark"
      character). Per CLAUDE.md rule 13, emojis break CloudWatch log queries on Windows. This is
      an existing issue in deployed code, not introduced by this analysis.
    </note>

  </data_quality_notes>

  <!-- ================================================================== -->
  <!-- GAPS                                                                 -->
  <!-- ================================================================== -->

  <gaps>

    <gap id="gap-1">
      <description>
        PM upload flow connection to yang pipeline not confirmed from source code.
        Task order requirement 2 describes: "PM uploads Excel -&gt; opal-pm-upload-urls -&gt; S3 upload
        -&gt; yang-pipeline-trigger -&gt; yang-validate-files -&gt; yang-ingest-dynamodb -&gt; yang-move-to-processed
        -&gt; opal-pm-optimization-loader."
        However, opal-pm-upload-urls writes to opal-data-pm, while yang-pipeline-trigger is triggered
        by S3 events on opal-data-portal-v2/uploads/manifest.json. These are separate buckets.
        opal-pm-optimization-loader source (infra/aws/lambda/portfolio_optimization_loader/) was not
        found locally, so it cannot be confirmed whether it reads from yang pipeline outputs or directly
        from opal-data-pm. The critical_flow pm-upload-to-optimization documents the upload-and-load
        path based on what is confirmed. The yang-pipeline-trigger connection is not verified.
      </description>
      <resolution>Read opal-pm-optimization-loader source code when available to confirm S3 read path.</resolution>
    </gap>

    <gap id="gap-2">
      <description>
        trade-submission-handler, trade-workflow-handler, and trade-dashboard-api Lambda source
        files are not present in the local repo and are not registered in lambda-source-map.json.
        DynamoDB table name(s) for TradeSubmission storage are not confirmed (likely opal-trade-submissions
        based on submission_id format, but not verified). Excel S3 bucket for TradeSubmission
        excel_s3_key is not confirmed.
      </description>
      <resolution>Locate trade submission Lambda sources; check their DynamoDB table names and S3 bucket configurations.</resolution>
    </gap>

    <gap id="gap-3">
      <description>
        opal-portfolio-autosave-get S3 key pattern not confirmed. Source infra/aws/lambda/portfolio_autosave_get/
        was not found locally. Bucket (likely opal-data-pm) and key pattern (likely
        {fund}/{account}/autosave.json or similar) are inferred but not verified.
      </description>
      <resolution>Read portfolio_autosave_get source when available.</resolution>
    </gap>

    <gap id="gap-4">
      <description>
        export-and-submit backend Lambda identity uncertain. lambda-source-map.json has
        opal-portfolio-excel-generator registered but its source (infra/aws/lambda/portfolio_excel_generator/)
        was not found locally. It is unclear whether the export-and-submit endpoint is handled by
        opal-portfolio-excel-generator alone or in combination with another Lambda. DynamoDB table
        for versioning (used by opal-portfolio-versions-list, opal-portfolio-version-get) is not confirmed.
      </description>
      <resolution>Read portfolio_excel_generator source and check for export-and-submit handler.</resolution>
    </gap>

    <gap id="gap-5">
      <description>
        getSecurityDetails endpoint (GET /api/private/portfolio-management/security/{ticker}) is
        not yet deployed. portfolio-optimization.ts:201 logs console.warn and proceeds to call
        the endpoint, which will 404. SecurityLookupModal can add securities but factor breakdown
        will not be populated for new securities added after initial load.
      </description>
      <resolution>Deploy opal-pm-security-details Lambda or equivalent backend endpoint.</resolution>
    </gap>

    <gap id="gap-6">
      <description>
        DataRefresh CurrentStatePanel fetches /api/general/json/latest/manifest.json. It is unclear
        whether this points to json/yang-pipeline-metadata.json (written by yang-pipeline-trigger)
        or json/latest/manifest.json (a different path). The yang-pipeline-trigger writes to
        json/yang-pipeline-metadata.json and json/latest/{file_type}.json (one per file type),
        not a single manifest.json. The exact S3 key and response shape for the freshness endpoint
        could not be confirmed without portal-proxy.ts lines 1838-1975 source.
      </description>
      <resolution>Read portal-proxy.ts lines 1838-1975 to confirm the exact S3 key for freshness data.</resolution>
    </gap>

  </gaps>

</data_contract>
```

### factor-scanner-v0----primary-python-pipeline-script-percentile-logic-universe-mapping-data-columns.py

```
"""
Quick Update v2.1 - Production-Ready with All Critical Fixes
=============================================================

FIXES APPLIED:
- ✅ BUG #1: Composite scores use Excel formulas (instant recalculation)
- ✅ BUG #2: No worksheet corruption (proper data updates)
- ✅ BUG #3: Efficient bulk operations (no 500k cell loops)
- ✅ BUG #4: Canonical factor mapping (100% coverage)
- ✅ BUG #5: Tab 1/Tab 4 synchronization validation
- ✅ BUG #6: Correct routing when BOTH universe AND factors change

OPERATIONS (Decision Tree):
1. Both universe + factors changed → Full rebuild (Tab 2 + Tab 4)
2. Universe changed only → Update Tab 2, switch Tab 4
3. Factors changed only → Ensure Tab 2 current, rebuild Tab 4
4. No changes → Re-sort Tab 4 only (formulas respond to weights)

Author: Elite VBA Architect
Date: November 3, 2025
Version: 2.1
"""

import pandas as pd
import numpy as np
import os
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
from canonical_factor_mapping import FactorMappingRegistry

print("Quick Update v2.1 - Starting...")
print()

# ==============================================================================
# CONFIGURATION
# ==============================================================================

def find_all_scanner_files(base_name):
    """Find all scanner files with given base name (supports .xlsx and .xlsm)."""
    files = []
    for ext in ['.xlsx', '.xlsm']:
        # Check root folder first
        filepath = f'{base_name}{ext}'
        if os.path.exists(filepath):
            files.append(filepath)
        # Also check models subfolder for backward compatibility
        filepath_models = f'models/{base_name}{ext}'
        if os.path.exists(filepath_models):
            files.append(filepath_models)
    return files

# Find all scanner files
RUSSELL_FILES = find_all_scanner_files('Russell_1000_Scanner')
MSCI_FILES = find_all_scanner_files('MSCI_World_Scanner')
DYNAMIC_FILES = find_all_scanner_files('Dynamic_Factor_Scanner')
FACTOR_SCANNING_FILES = find_all_scanner_files('Factor_Scanning_Model')

ALL_FILES = []
if FACTOR_SCANNING_FILES:
    ALL_FILES.extend(FACTOR_SCANNING_FILES)
if DYNAMIC_FILES:
    ALL_FILES.extend(DYNAMIC_FILES)
if RUSSELL_FILES:
    ALL_FILES.extend(RUSSELL_FILES)
if MSCI_FILES:
    ALL_FILES.extend(MSCI_FILES)

if not ALL_FILES:
    print("ERROR: No scanner files found!")
    print("Run build_factor_scanners.py first to create the models")
    sys.exit(1)

# Formatting constants
HEADER_FILL = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
SUB_HEADER_FILL = PatternFill(start_color='B4C7E7', end_color='B4C7E7', fill_type='solid')
HEADER_FONT = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
TITLE_FONT = Font(name='Calibri', size=24, bold=True, color='1F4E78')
SUBTITLE_FONT = Font(name='Calibri', size=9, italic=True, color='666666')

# Universe mapping
UNIVERSE_OPTIONS = {
    'S&P 500': 'wt_ivv',
    'Russell 1000': 'wt_iwb',
    'Russell 1000 Value': 'wt_iwd',
    'MSCI ACWI ex-US': 'wt_acwx',
    'MSCI EAFE': 'wt_efa',
    'MSCI EAFE Value': 'wt_efv'
}

DATA_FILE = 'data_tables/Screening_DIVZ_IDVZ_20251028.xlsx'


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def preserve_tab1_row_heights(wb):
    """
    Preserve Tab 1 row heights (prevents openpyxl from auto-resizing).
    Row 1: 15 (default)
    Row 2: 60 (logo image centered in merged range A2:J2)
    Row 3: 15 (default)
    """
    if '1-Configuration' in wb.sheetnames:
        ws_tab1 = wb['1-Configuration']
        ws_tab1.row_dimensions[1].height = 15
        ws_tab1.row_dimensions[2].height = 60
        ws_tab1.row_dimensions[3].height = 15


def read_selected_factors_from_tab1(file_path):
    """Read selected factor codes from Tab 1 SELECTED FACTORS section."""
    df_tab1 = pd.read_excel(file_path, sheet_name='1-Configuration', header=None)

    # Find SELECTED FACTORS section
    selected_start = None
    for idx, row in df_tab1.iterrows():
        if pd.notna(row[0]) and 'SELECTED FACTORS' in str(row[0]).upper():
            selected_start = idx + 2
            break

    if selected_start is None:
        return []

    # Read factor codes from column E
    factor_codes = []
    current_row = selected_start
    while current_row < len(df_tab1):
        code = df_tab1.iloc[current_row, 4]  # Column E
        if pd.isna(code) or code == '':
            break
        factor_codes.append(code)
        current_row += 1

    return factor_codes


def read_universe_from_tab1(file_path):
    """Read selected universe from Tab 1 dropdown (Cell C4)."""
    try:
        df_tab1 = pd.read_excel(file_path, sheet_name='1-Configuration', header=None, nrows=5)
        selected = df_tab1.iloc[3, 2]  # Cell C4

        if pd.notna(selected) and selected in UNIVERSE_OPTIONS:
            return (selected, UNIVERSE_OPTIONS[selected])

        return (None, None)
    except Exception as e:
        return (None, None)


def detect_current_universe(file_path):
    """Detect which universe is currently loaded by counting securities in Tab 2 (2-Universe Data)."""
    try:
        df_tab2 = pd.read_excel(file_path, sheet_name='2-Universe Data', header=4)
        num_securities = len(df_tab2)

        # Match to expected universe sizes (with tolerance)
        if 450 < num_securities < 550:
            return ('S&P 500', 'wt_ivv')
        elif 950 < num_securities < 1050:
            return ('Russell 1000', 'wt_iwb')
        elif 800 < num_securities < 900:
            return ('Russell 1000 Value', 'wt_iwd')
        elif 1600 < num_securities < 1750:
            return ('MSCI ACWI ex-US', 'wt_acwx')
        elif 650 < num_securities < 750:
            return ('MSCI EAFE', 'wt_efa')
        elif 350 < num_securities < 450:
            return ('MSCI EAFE Value', 'wt_efv')

        return (None, None)
    except Exception as e:
        return (None, None)


def read_factors_from_tab4(file_path):
    """
    Read which factors are currently in Tab 4 by examining headers.

    Returns:
        List of factor codes (empty list if Tab 4 doesn't exist or is corrupted)
    """
    try:
        wb = load_workbook(file_path, keep_vba=True, data_only=False)

        if '4-Security Scanner' not in wb.sheetnames:
            wb.close()
            return []

        ws = wb['4-Security Scanner']

        # Find header row 1 (has factor names)
        # Look for "Ticker" in column 1 (A) to identify header row
        header_row1 = None
        for row_idx in range(1, 50):
            if ws.cell(row=row_idx, column=1).value == "Ticker":
                header_row1 = row_idx
                break

        if header_row1 is None:
            wb.close()
            return []

        # Read factor names from merged headers (column 8+, every 2 columns)
        # Factors now start at column H (8)
        factor_names = []
        col_idx = 8
        while col_idx <= min(ws.max_column, 200):  # Cap at 200 to avoid inflated max_column
            factor_name = ws.cell(row=header_row1, column=col_idx).value
            if not factor_name:
                break
            factor_names.append(str(factor_name))
            col_idx += 2

        wb.close()

        # Convert display names to codes using canonical mapping
        registry = FactorMappingRegistry(file_path)
        factor_codes = []
        for name in factor_names:
            code = registry.get_code_from_display(name)
            if code:
                factor_codes.append(code)

        return factor_codes

    except Exception as e:
        return []


def calculate_percentiles_with_sign(df, tab3_column, sign):
    """Calculate percentile scores for a factor with sign handling."""
    if tab3_column not in df.columns:
        return pd.Series([np.nan] * len(df), index=df.index)

    factor_values = pd.to_numeric(df[tab3_column], errors='coerce')

    # Handle sign inversion
    if sign in ['-1', 'Inverse', 'inverse']:
        factor_values = -factor_values

    # Calculate percentile rank (0-100 scale)
    percentiles = factor_values.rank(pct=True, method='average') * 100

    return percentiles


# ==============================================================================
# OPERATION 1: FULL TAB 4 REBUILD (Factor changes detected)
# ==============================================================================

def rebuild_tab2_full(file_path, universe_name):
    """
    Full Tab 4 (Security Scanner) rebuild when factors have changed.
    Creates formulas from scratch.
    """
    print(f"\n  REBUILDING TAB 4 (factor changes detected)...")

    try:
        # Initialize canonical mapping
        registry = FactorMappingRegistry(file_path)

        # Read selected factors from Tab 1
        selected_codes = read_selected_factors_from_tab1(file_path)

        if not selected_codes:
            print("  ERROR: No factors selected in Tab 1")
            return False

        # Validate factors
        valid_codes, invalid_codes = registry.validate_factors(selected_codes)

        if invalid_codes:
            print(f"  WARNING: {len(invalid_codes)} invalid factors skipped")

        if not valid_codes:
            print("  ERROR: No valid factors to process")
            return False

        # Build factor metadata
        factors_metadata = [registry.get_factor_metadata(code) for code in valid_codes]

        # Read data from SOURCE DATA FILE (not Tab 3)
        print(f"  Loading data from source file...")
        df_source = pd.read_excel(DATA_FILE, header=4)

        # Filter for current universe (only include stocks with positive weight > 0)
        universe_col = UNIVERSE_OPTIONS.get(universe_name)
        if universe_col and universe_col in df_source.columns:
            print(f"  Filtering by column '{universe_col}' (weight > 0)...")
            df_universe = df_source[df_source[universe_col] > 0].copy()
            print(f"  ✓ Loaded {len(df_universe)} securities for {universe_name}")
        else:
            print(f"  WARNING: Universe '{universe_name}' not found, using all data")
            df_universe = df_source.copy()

        # Calculate percentiles
        print(f"  Calculating percentiles for {len(valid_codes)} factors...")
        for metadata in factors_metadata:
            code = metadata['code']
            tab3_col = metadata['tab3_column']
            sign = metadata['sign']

            percentiles = calculate_percentiles_with_sign(df_universe, tab3_col, sign)
            df_universe[f'{code}_pctl'] = percentiles

        # Calculate composite scores (for initial sorting)
        percentile_cols = [f'{code}_pctl' for code in valid_codes]
        df_universe['composite_score'] = df_universe[percentile_cols].mean(axis=1, skipna=True)

        # Sort
        df_sorted = df_universe.sort_values('composite_score', ascending=False, na_position='last').reset_index(drop=True)

        # DEBUG: Check if company data exists in df_sorted
        print(f"  DEBUG: df_sorted columns: {df_sorted.columns.tolist()[:15]}")
        print(f"  DEBUG: First row ticker={df_sorted.iloc[0].get('ticker')}, name={df_sorted.iloc[0].get('name')}")

        # Rebuild Tab 4 (NON-DESTRUCTIVE - preserves sheet object and VBA code)
        print(f"  Rebuilding Tab 4 structure in-place...")
        wb = load_workbook(file_path, keep_vba=True)

        if '4-Security Scanner' not in wb.sheetnames:
            print(f"  ERROR: Tab 4 not found!")
            wb.close()
            return False

        ws_tab4 = wb['4-Security Scanner']

        # Build structure with formulas (cleanup happens inside this function)
        from surgical_repair import build_tab2_with_formulas
        build_tab2_with_formulas(ws_tab4, df_sorted, factors_metadata, universe_name)

        # Save
        print(f"  Saving workbook...")
        preserve_tab1_row_heights(wb)
        wb.save(file_path)
        wb.close()

        print(f"  [OK] Tab 4 rebuilt with {len(valid_codes)} factors, {len(df_sorted)} securities")

        # NOTE: Tab 2 (2-Universe Data) updates are handled separately in OPERATION 4 (called from orchestration)
        # This keeps Tab 4 and Tab 2 operations completely isolated to prevent sheet corruption

        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# OPERATION 2: RE-SORT TAB 4 ONLY (No factor changes, formulas exist)
# ==============================================================================

def resort_tab2_only(file_path):
    """
    Re-sort Tab 4 (Security Scanner) when no factor changes detected.
    Formulas already exist and work, just need to reorder rows.

    THIS IS FAST: No percentile recalculation, no formula rewriting.
    """
    print(f"\n  RE-SORTING TAB 4 (no factor changes, formulas intact)...")

    try:
        wb = load_workbook(file_path, keep_vba=True, data_only=True)  # data_only=True to read computed values
        ws = wb['4-Security Scanner']

        # Find data start row (look for "Ticker" in column A)
        data_start = None
        for row_idx in range(1, 50):
            if ws.cell(row=row_idx, column=1).value == "Ticker":
                data_start = row_idx + 2
                break

        if not data_start:
            wb.close()
            return False

        # Read all data rows (composite score + ticker for sorting)
        # Column structure: A=Ticker, B=Name, C=Rank, D=Composite
        data_rows = []
        row_idx = data_start
        while row_idx <= ws.max_row:
            ticker = ws.cell(row=row_idx, column=1).value  # Column A = Ticker
            if not ticker:
                break

            composite = ws.cell(row=row_idx, column=4).value  # Column D = Composite
            data_rows.append({
                'row': row_idx,
                'composite': composite if composite is not None else 0,
                'ticker': ticker
            })
            row_idx += 1

        # Sort by composite score (descending)
        data_rows_sorted = sorted(data_rows, key=lambda x: x['composite'], reverse=True)

        # Close and reopen without data_only to preserve formulas
        wb.close()

        wb = load_workbook(file_path, keep_vba=True, data_only=False)
        ws = wb['4-Security Scanner']

        # Read all row data into memory
        # Find actual last column (don't use max_column - it can be inflated by stray formatting)
        # Look at header row to find last column with data
        last_col_with_data = 7  # Minimum: A-G (Ticker, Name, Rank, Composite, Mkt Val, Country, Sector)
        for col in range(8, min(ws.max_column + 1, 200)):  # Cap search at column 200
            header_val = ws.cell(row=data_start - 2, column=col).value  # Header row is 2 rows above data
            if header_val:
                last_col_with_data = col
            elif col > last_col_with_data + 5:  # Stop if we've seen 5 empty columns in a row
                break

        num_cols = last_col_with_data
        print(f"  Reading {len(data_rows)} rows × {num_cols} columns...")
        old_rows = {}
        for item in data_rows:
            old_row = item['row']
            old_rows[old_row] = []
            for col in range(1, num_cols + 1):
                cell = ws.cell(row=old_row, column=col)
                old_rows[old_row].append({
                    'value': cell.value,
                    'number_format': cell.number_format
                })

        # Write back in sorted order
        for new_idx, item in enumerate(data_rows_sorted):
            old_row = item['row']
            new_row = data_start + new_idx

            for col in range(1, num_cols + 1):
                if col == 3:  # Rank column (C) - update with new rank
                    ws.cell(row=new_row, column=3).value = new_idx + 1
                else:
                    cell_data = old_rows[old_row][col - 1]
                    ws.cell(row=new_row, column=col).value = cell_data['value']
                    ws.cell(row=new_row, column=col).number_format = cell_data['number_format']

        # Save
        preserve_tab1_row_heights(wb)
        wb.save(file_path)
        wb.close()

        print(f"  [OK] Tab 4 re-sorted ({len(data_rows_sorted)} securities)")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# OPERATION 3: UNIVERSE SWITCH (Surgical data update)
# ==============================================================================

def switch_universe_efficient(file_path, new_universe_name, new_index_col):
    """
    Efficiently switch universe by updating Tab 3 and recalculating Tab 4.
    Preserves Tab 4 formulas.
    """
    print(f"\n  SWITCHING UNIVERSE to {new_universe_name}...")

    try:
        # Load new universe data (only include stocks with positive weight > 0)
        df_source = pd.read_excel(DATA_FILE, header=4)
        print(f"  Filtering by column '{new_index_col}' (weight > 0)...")
        df_universe = df_source[df_source[new_index_col] > 0].copy()
        print(f"  ✓ Loaded {len(df_universe)} securities for {new_universe_name}")

        # Initialize canonical mapping
        registry = FactorMappingRegistry(file_path)

        # Read selected factors
        selected_codes = read_selected_factors_from_tab1(file_path)
        valid_codes, _ = registry.validate_factors(selected_codes)
        factors_metadata = [registry.get_factor_metadata(code) for code in valid_codes]

        # Calculate percentiles on new universe
        print(f"  Calculating percentiles...")
        for metadata in factors_metadata:
            code = metadata['code']
            tab3_col = metadata['tab3_column']
            sign = metadata['sign']

            percentiles = calculate_percentiles_with_sign(df_universe, tab3_col, sign)
            df_universe[f'{code}_pctl'] = percentiles

        # Calculate composite scores
        percentile_cols = [f'{code}_pctl' for code in valid_codes]
        df_universe['composite_score'] = df_universe[percentile_cols].mean(axis=1, skipna=True)

        # Sort
        df_sorted = df_universe.sort_values('composite_score', ascending=False, na_position='last').reset_index(drop=True)

        # Update Tab 4 directly (Tab 3 not needed for this operation)
        print(f"  Updating Tab 4...")
        wb = load_workbook(file_path, keep_vba=True)

        ws_tab4 = wb['4-Security Scanner']

        # Update title to reflect new universe
        ws_tab4.cell(row=2, column=1).value = f"{new_universe_name} Security Scoring & Values"

        # Find data start (look for "Ticker" in column A, data starts 2 rows below)
        data_start = None
        for row_idx in range(1, 50):
            if ws_tab4.cell(row=row_idx, column=1).value == "Ticker":
                data_start = row_idx + 2  # Skip header row and Filter row
                break

        if not data_start:
            wb.close()
            print(f"  ERROR: Could not find data start row (looking for 'Ticker' in column A)")
            return False

        # OPTIMIZATION: Find and delete old data rows in ONE operation
        last_data_row = data_start
        for row_idx in range(data_start, min(data_start + 2000, ws_tab4.max_row + 1)):
            ticker = ws_tab4.cell(row=row_idx, column=3).value
            if ticker and str(ticker).strip():
                last_data_row = row_idx
            elif row_idx > data_start + 10:
                break

        num_old_rows = last_data_row - data_start + 1

        # Delete old data rows (SAFE: we immediately rebuild them)
        if num_old_rows > 0:
            print(f"  Deleting {num_old_rows} old rows...")
            ws_tab4.delete_rows(data_start, num_old_rows)

        # Write new data with alternating row colors
        print(f"  Writing {len(df_sorted)} new rows...")
        weight_row_start = 7

        # Define fills for alternating rows
        WHITE_FILL = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        LIGHT_GRAY_FILL = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')

        for idx, (_, row_data) in enumerate(df_sorted.iterrows()):
            excel_row = data_start + idx

            # Alternating row color (independent of Tab 2)
            row_fill = WHITE_FILL if idx % 2 == 0 else LIGHT_GRAY_FILL

            # Column A: Ticker
            ticker_cell = ws_tab4.cell(row=excel_row, column=1)
            ticker_cell.value = row_data.get('ticker')
            ticker_cell.fill = row_fill
            ticker_cell.font = Font(name='Calibri', size=11, bold=True)

            # Column B: Name
            company_name = row_data.get('factset_entity_proper_name') or row_data.get('name')
            name_cell = ws_tab4.cell(row=excel_row, column=2)
            name_cell.value = company_name
            name_cell.fill = row_fill

            # Column C: Rank
            rank_cell = ws_tab4.cell(row=excel_row, column=3)
            rank_cell.value = idx + 1
            rank_cell.fill = row_fill

            # Column D: Composite formula (NO FILL - has conditional formatting)
            formula_parts = []
            for factor_idx, metadata in enumerate(factors_metadata):
                pctl_col = 8 + (factor_idx * 2)  # Factors start at column H (8)
                pctl_col_letter = get_column_letter(pctl_col)
                weight_cell_ref = f'$C${weight_row_start + factor_idx}'  # Weights in column C
                formula_parts.append(f'{pctl_col_letter}{excel_row}*{weight_cell_ref}')

            composite_formula = f'=({"+".join(formula_parts)})/100'
            composite_cell = ws_tab4.cell(row=excel_row, column=4)
            composite_cell.value = composite_formula
            composite_cell.number_format = '0.00'
            # DO NOT APPLY FILL - conditional formatting will handle colors

            # Column E: Market Value
            mkt_val_cell = ws_tab4.cell(row=excel_row, column=5)
            mkt_val = row_data.get('mkt_val')
            if pd.notna(mkt_val):
                mkt_val_cell.value = float(mkt_val)
            mkt_val_cell.number_format = '$#,##0'
            mkt_val_cell.fill = row_fill

            # Column F: Country
            country_cell = ws_tab4.cell(row=excel_row, column=6)
            country_cell.value = row_data.get('country_name', '')
            country_cell.fill = row_fill

            # Column G: Sector
            sector_cell = ws_tab4.cell(row=excel_row, column=7)
            sector_cell.value = row_data.get('sector_name', '')
            sector_cell.fill = row_fill

            # Factor data starts at column H (8)
            col = 8
            for metadata in factors_metadata:
                code = metadata['code']
                tab3_col = metadata['tab3_column']

                # Percentile (Score) - NO FILL - has conditional formatting (quintile colors)
                pctl_cell = ws_tab4.cell(row=excel_row, column=col)
                pctl_val = row_data.get(f'{code}_pctl')
                if pd.notna(pctl_val):
                    pctl_cell.value = round(float(pctl_val), 1)
                pctl_cell.number_format = '0.0'
                # DO NOT APPLY FILL - conditional formatting will handle quintile colors

                # Value - Apply alternating row color
                value_cell = ws_tab4.cell(row=excel_row, column=col+1)
                factor_val = row_data.get(tab3_col)
                if pd.notna(factor_val):
                    value_cell.value = float(factor_val)
                value_cell.number_format = '0.00'
                value_cell.fill = row_fill  # Apply alternating color to Value columns

                col += 2

        # Update column F (Country) visibility based on universe type
        us_indexes = ['S&P 500', 'Russell 1000', 'Russell 1000 Value']
        is_us_index = new_universe_name in us_indexes

        if is_us_index:
            ws_tab4.column_dimensions['F'].hidden = True  # Hide Country column for US indexes
            ws_tab4.column_dimensions['F'].width = 0
        else:
            ws_tab4.column_dimensions['F'].hidden = False  # Show Country column for international indexes
            ws_tab4.column_dimensions['F'].width = 16.29

        # Save
        preserve_tab1_row_heights(wb)
        wb.save(file_path)
        wb.close()

        print(f"  [OK] Universe switched to {new_universe_name} ({len(df_sorted)} securities)")
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# OPERATION 4: REBUILD TAB 2 (Populate complete security dataset)
# ==============================================================================

def rebuild_tab3_full(file_path, universe_name):
    """
    Rebuild Tab 2 (2-Universe Data) with complete security dataset for current universe.
    Preserves all structure, formatting, and styling.
    Only updates data rows (7+).

    Args:
        file_path: Path to Excel file
        universe_name: Universe display name

    Returns:
        True if successful, False otherwise
    """
    print(f"\n  REBUILDING TAB 2 (2-Universe Data) with securities...")

    try:
        # Load source data
        print(f"  Loading data from source file...")
        df_source = pd.read_excel(DATA_FILE, header=4)

        # Filter for universe (only include stocks with positive weight > 0)
        universe_col = UNIVERSE_OPTIONS.get(universe_name)
        if universe_col and universe_col in df_source.columns:
            print(f"  Filtering by column '{universe_col}' (weight > 0)...")
            df_universe = df_source[df_source[universe_col] > 0].copy()
            print(f"  ✓ Filtered to {len(df_universe)} securities for {universe_name}")
        else:
            print(f"  WARNING: Universe '{universe_name}' not found, using all data")
            df_universe = df_source.copy()

        # Load workbook
        wb = load_workbook(file_path, keep_vba=True)

        if '2-Universe Data' not in wb.sheetnames:
            print(f"  ERROR: Tab '2-Universe Data' not found")
            wb.close()
            return False

        ws = wb['2-Universe Data']

        # Read headers from Row 5 to understand column mapping
        print(f"  Reading column headers...")
        headers = []
        col_idx = 1
        while col_idx <= min(ws.max_column, 500):  # Cap at 500 to avoid inflated max_column
            header = ws.cell(row=5, column=col_idx).value
            if not header or header == 'FILTER':
                break
            headers.append(header)
            col_idx += 1

        print(f"  Found {len(headers)} columns")

        # Build mapping: Tab 2 header -> source data column
        header_to_source = {}

        # Basic columns (exact matches in source)
        basic_mappings = {
            'Ticker': 'ticker',
            'Company Name': 'name',
            'Mkt Val ($M)': 'mkt_val',
            'Country': 'country_name',
            'Sector': 'sector_name',
            'Industry Group': 'indgrp_name'
        }

        for tab3_header, source_col in basic_mappings.items():
            if tab3_header in headers:
                header_to_source[tab3_header] = source_col

        # Factor columns - Tab 2 has display names, need to map to codes
        # Use Tab 3 (3-Factor Data) to get the factor metadata mapping
        df_tab4 = pd.read_excel(file_path, sheet_name='3-Factor Data', header=4)
        df_tab4 = df_tab4[df_tab4['Factor Code'] != 'FILTER']

        # Build display_name -> code mapping from Tab 3 (3-Factor Data)
        display_to_code = {}
        for _, row in df_tab4.iterrows():
            code = row['Factor Code']
            display = row['Factor Name']
            display_to_code[display] = code

        # Map Tab 2 headers to source columns
        for tab3_header in headers:
            if tab3_header in header_to_source:
                continue  # Already mapped (basic column)

            # Try exact display name match
            if tab3_header in display_to_code:
                code = display_to_code[tab3_header]
                if code in df_universe.columns:
                    header_to_source[tab3_header] = code
                    continue

            # Try with newline converted to space
            tab3_header_clean = tab3_header.replace('\n', ' ')
            if tab3_header_clean in display_to_code:
                code = display_to_code[tab3_header_clean]
                if code in df_universe.columns:
                    header_to_source[tab3_header] = code
                    continue

            # Try reverse: convert Tab 4 display names to Tab 3 format
            for display_name, code in display_to_code.items():
                import re
                display_with_newline = re.sub(r' (\([^)]+\))$', r'\n\1', display_name)

                if display_with_newline == tab3_header:
                    if code in df_universe.columns:
                        header_to_source[tab3_header] = code
                        break

        print(f"  Mapped {len(header_to_source)}/{len(headers)} columns")

        # Delete old data rows (7+)
        print(f"  Deleting old data rows...")
        old_max_row = ws.max_row
        if old_max_row > 6:
            ws.delete_rows(7, old_max_row - 6)

        # Write new data starting at row 7
        print(f"  Writing {len(df_universe)} securities...")

        # Define dollar columns (values in millions)
        dollar_columns = {
            'mkt_val', 'mkt_val_sec', 'ev', 'bv', 'tangible_bv',
            'sales', 'assets', 'equity', 'cash', 'debt',
            'ebitda', 'ebit', 'ocf', 'fcf', 'capex', 'nwc'
        }

        # Alternating row colors
        from openpyxl.styles import PatternFill
        white_fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        light_gray_fill = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')

        # Borders (light gray - Excel default)
        thin_border = Border(
            left=Side(style='thin', color='D3D3D3'),
            right=Side(style='thin', color='D3D3D3'),
            top=Side(style='thin', color='D3D3D3'),
            bottom=Side(style='thin', color='D3D3D3')
        )

        for enum_idx, (_, row_data) in enumerate(df_universe.iterrows()):
            row_idx = 7 + enum_idx

            # Alternating row color
            row_fill = white_fill if enum_idx % 2 == 0 else light_gray_fill

            for col_idx, tab3_header in enumerate(headers, start=1):
                source_col = header_to_source.get(tab3_header)

                if not source_col:
                    continue  # Skip unmapped columns

                value = row_data.get(source_col)

                if pd.notna(value):
                    # Write value with appropriate formatting
                    if source_col == 'ticker':
                        # Ticker column (Column A) - always bold
                        cell = ws.cell(row=row_idx, column=col_idx)
                        cell.value = str(value)
                        cell.font = Font(bold=True)
                        cell.fill = row_fill
                        cell.border = thin_border
                    elif source_col in dollar_columns:
                        # Dollar columns - format with $ and commas
                        cell = ws.cell(row=row_idx, column=col_idx)
                        cell.value = float(value)
                        cell.number_format = '$#,##0'
                        cell.fill = row_fill
                        cell.border = thin_border
                    elif isinstance(value, (int, float)):
                        cell = ws.cell(row=row_idx, column=col_idx)
                        cell.value = float(value)
                        cell.number_format = '0.00'
                        cell.fill = row_fill
                        cell.border = thin_border
                    else:
                        cell = ws.cell(row=row_idx, column=col_idx)
                        cell.value = str(value)
                        cell.fill = row_fill
                        cell.border = thin_border

        # Save
        print(f"  Saving workbook...")
        preserve_tab1_row_heights(wb)
        wb.save(file_path)
        wb.close()

        print(f"  [OK] Tab 2 (2-Universe Data) updated with {len(df_universe)} securities")
        return True

    except Exception as e:
        print(f"  ERROR in rebuild_tab3_full: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# MAIN ORCHESTRATION
# ==============================================================================

def process_file(file_path):
    """
    Intelligently process a single file based on detected changes.
    """
    print(f"\n{'='*80}")
    print(f"Processing: {os.path.basename(file_path)}")
    print(f"{'='*80}")

    # Read current state
    selected_universe, selected_index = read_universe_from_tab1(file_path)
    current_universe, current_index = detect_current_universe(file_path)

    tab1_factors = read_selected_factors_from_tab1(file_path)
    tab4_factors = read_factors_from_tab4(file_path)

    print(f"\nCurrent State:")
    print(f"  Tab 1 selected universe: {selected_universe}")
    print(f"  Tab 2 current universe: {current_universe}")
    print(f"  Tab 1 factors: {len(tab1_factors)}")
    print(f"  Tab 4 factors: {len(tab4_factors)}")

    # DECISION TREE

    # Detect both types of changes
    # Universe changed if:
    # 1. Tab 1 has a selection AND it doesn't match Tab 2 (including Tab 2 = None)
    # 2. OR Tab 2 is None/corrupted but Tab 1 has a valid selection
    universe_changed = (
        selected_universe and
        (not current_universe or selected_universe != current_universe)
    )
    factors_changed = not tab4_factors or set(tab1_factors) != set(tab4_factors)

    # Case 1: BOTH universe AND factors changed - Full rebuild required
    if universe_changed and factors_changed:
        print(f"\n>> OPERATION 1: FULL REBUILD (Universe + Factors changed)")
        if current_universe:
            print(f"  Universe: {current_universe} → {selected_universe}")
        else:
            print(f"  Universe: Corrupted/Unknown → {selected_universe}")

        added = set(tab1_factors) - set(tab4_factors) if tab4_factors else set(tab1_factors)
        removed = set(tab4_factors) - set(tab1_factors) if tab4_factors else set()

        if added:
            print(f"  Factors added: {len(added)}")
        if removed:
            print(f"  Factors removed: {len(removed)}")

        # Step 1: Update Tab 2 (Universe Data) with new universe
        print(f"\n  [Step 1/2] Updating Tab 2 with {selected_universe} data...")
        tab2_result = rebuild_tab3_full(file_path, selected_universe)

        if not tab2_result:
            print(f"  ERROR: Failed to update Tab 2")
            return False

        # Step 2: Rebuild Tab 4 with new factors
        print(f"\n  [Step 2/2] Rebuilding Tab 4 with {len(tab1_factors)} factors...")
        tab4_result = rebuild_tab2_full(file_path, selected_universe)

        return tab4_result

    # Case 2: Universe changed ONLY (no factor changes) - Efficient universe switch
    if universe_changed:
        print(f"\n>> OPERATION 2: UNIVERSE SWITCH")
        if current_universe:
            print(f"  From: {current_universe}")
        else:
            print(f"  From: Corrupted/Unknown")
        print(f"  To: {selected_universe}")

        # Step 1: Update Tab 2 (Universe Data) with new universe
        print(f"\n  [Step 1/2] Updating Tab 2 with {selected_universe} data...")
        tab2_result = rebuild_tab3_full(file_path, selected_universe)

        if not tab2_result:
            print(f"  ERROR: Failed to update Tab 2")
            return False

        # Step 2: Efficiently update Tab 4 data rows (preserves headers, formulas, formatting)
        print(f"\n  [Step 2/2] Updating Tab 4 data rows...")
        tab4_result = switch_universe_efficient(file_path, selected_universe, selected_index)

        return tab4_result

    # Case 3: Factors changed ONLY (no universe change) - Full rebuild
    if factors_changed:
        added = set(tab1_factors) - set(tab4_factors) if tab4_factors else set(tab1_factors)
        removed = set(tab4_factors) - set(tab1_factors) if tab4_factors else set()

        print(f"\n>> OPERATION 3: FULL TAB 4 REBUILD (Factors changed)")
        if added:
            print(f"  Factors added: {len(added)}")
        if removed:
            print(f"  Factors removed: {len(removed)}")
        if not tab4_factors:
            print(f"  Reason: Tab 4 needs initialization")

        universe_name = selected_universe if selected_universe else "Unknown Universe"

        # Step 1: Ensure Tab 2 has current data
        print(f"\n  [Step 1/2] Ensuring Tab 2 has {universe_name} data...")
        tab2_result = rebuild_tab3_full(file_path, universe_name)

        if not tab2_result:
            print(f"  WARNING: Tab 2 update failed, continuing with existing data...")

        # Step 2: Rebuild Tab 4 with new factors
        print(f"\n  [Step 2/2] Rebuilding Tab 4 with {len(tab1_factors)} factors...")
        tab4_result = rebuild_tab2_full(file_path, universe_name)

        return tab4_result

    # Case 4: No changes - Re-sort only (formulas respond to weight changes)
    print(f"\n>> OPERATION 4: RE-SORT")
    print(f"  (No factor or universe changes, formulas intact)")
    return resort_tab2_only(file_path)


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("QUICK UPDATE v2.1 - PRODUCTION READY")
    print("="*80)
    print()
    print(f"Found {len(ALL_FILES)} file(s) to process:")
    for f in ALL_FILES:
        print(f"  - {f}")
    print()

    success_count = 0

    for file_path in ALL_FILES:
        result = process_file(file_path)
        if result:
            success_count += 1

    print()
    print("="*80)
    print("UPDATE COMPLETE")
    print("="*80)
    print()

    if success_count > 0:
        print(f"[OK] Successfully updated {success_count}/{len(ALL_FILES)} file(s)")
        print()
        print("Next steps:")
        print("  1. Reopen the Excel file(s)")
        print("  2. Change weights in Tab 4-Security Scanner")
        print("  3. Watch composite scores recalculate instantly!")
        print()
        return 0
    else:
        print("ERROR: No files were updated successfully")
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

### factor-scanner-v0-system-reference----workflow-file-structure-data-sources-universe-column-mapping.md

```
# Factor Scanner v2.1 - System Reference

**Generated from actual code**: November 3, 2025
**Source of truth**: Active scripts + Factor_Scanning_Model.xlsm

---

## System Overview

**Factor Scanner v2.1** is an Excel-based quantitative screening tool that:
1. Lets users select factors and weights in Excel
2. Automatically updates rankings when weights change
3. Supports 6 universes (S&P 500, Russell 1000, MSCI EAFE, etc.)
4. Covers 255 factors across 11 categories

**Key File**: `Factor_Scanning_Model.xlsm`

---

## How It Works

### User Workflow

1. **Select Universe** (Tab 1, Cell C2)
   - Choose from: S&P 500, Russell 1000, Russell 1000 Value, MSCI ACWI ex-US, MSCI EAFE, MSCI EAFE Value

2. **Select Factors** (Tab 1, Factor Bank)
   - Toggle YES/NO in "Active" column for any of 255 factors
   - Save and close Excel file

3. **Run Update** (Windows Explorer)
   - Double-click `02_MODEL_REFRESH.bat`
   - Script detects changes and updates Excel file

4. **Adjust Weights** (Tab 4, Column B)
   - Change weight percentages (must sum to 100%)
   - Rankings auto-update instantly (if VBA enabled)

### File Structure

```
Factor_Scanner.V2/
├── Factor_Scanning_Model.xlsm      # Main Excel file
├── 02_MODEL_REFRESH.bat            # Quick update launcher
├── data_tables/
│   └── Screening_DIVZ_IDVZ_20251028.xlsx  # Source data (255 factors)
└── scripts/
    ├── python/                     # Python automation scripts
    └── vba/                        # Excel VBA macros
```

---

## Excel File Structure

### Tab 1: 1-Configuration
**Purpose**: Factor selection interface

**Key Areas**:
- Cell C2: Universe dropdown
- Selected Factors table: Current active factors
- Factor Bank: All 255 factors with YES/NO toggles

**User edits**: Toggle YES/NO, select universe

### Tab 2: 2-Ranked Securities
**Purpose**: Final ranked list (read-only)

**Columns**:
- Ticker, Name, Composite Score
- Individual factor percentile ranks

**Updated by**: Python script (quick_update_weights.py)

### Tab 3: 3-Factor Data
**Purpose**: Complete factor dataset (read-only)

**Contains**: All securities × all selected factors
**Source**: Copied from `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx`

### Tab 4: 4-Security Scanner
**Purpose**: **PRIMARY SCORING TAB** - Interactive weights

**Key Features**:
- Column B (rows 6-12): Weight percentages (user editable)
- Composite scores: Excel formulas that auto-recalculate
- Auto-sort: VBA sorts by composite score when weights change

**User edits**: Change weights, watch scores update

---

## Active Scripts

### Python Scripts (6 files)

#### 1. `quick_update_weights.py` ⭐ PRIMARY SCRIPT
**What it does**: Intelligent decision tree for model updates

**4 Operations**:
1. **Both universe + factors changed** → Full rebuild (Tab 2 + Tab 4)
2. **Universe changed only** → Update Tab 2, switch Tab 4 universe
3. **Factors changed only** → Ensure Tab 2 current, rebuild Tab 4
4. **No changes** → Re-sort Tab 4 only

**When to run**: After changing factors or universe in Tab 1

**How to run**: Double-click `02_MODEL_REFRESH.bat`

**Input**: Reads Tab 1 (selected factors, universe)
**Output**: Updates Tab 2 and Tab 4
**Key fix**: Composite scores use Excel formulas (not static values)

#### 2. `surgical_repair.py` ⭐ EMERGENCY REPAIR
**What it does**: Rebuilds Tab 4 from scratch if corrupted

**When to use**:
- Composite scores show static values instead of formulas
- Tab 1/Tab 4 out of sync
- Corrupted worksheet data

**How to run**: `python scripts/python/surgical_repair.py`

**What it fixes**:
- Restores Excel formulas for composite scores
- Rebuilds factor columns from Tab 3
- Applies proper formatting

#### 3. `canonical_factor_mapping.py` (utility)
**What it does**: Maps factor codes ↔ display names ↔ data columns

**Problem solved**: Three-way naming:
- Tab 1 uses codes: `bv`, `sales_gr_1yr`
- Tab 4 uses display names: `Book Value`, `Sales Growth (1 Year)`
- Tab 3 uses column headers: `Book Value`, `Sales Growth\n(1 Year)`

**Used by**: quick_update_weights.py, surgical_repair.py

#### 4. `factor_definitions_registry.py` (utility)
**What it does**: Provides descriptions for all 255 factors

**Example**:
```python
'bv': 'Book value of equity; total assets minus total liabilities'
'sales_gr_1yr': 'One-year historical sales growth; year-over-year revenue growth'
```

**Used by**: export_factor_descriptions.py

#### 5. `export_factor_descriptions.py` (utility)
**What it does**: Exports factor definitions to Excel/CSV for reference

**When to use**: Need factor descriptions outside Excel

#### 6. `calculate_predictive_power_score.py` (analysis)
**What it does**: Calculates PPS (Predictive Power Score) for factors

**When to use**: Quality analysis of factor predictive power

### VBA Scripts (4 files)

#### 1. `Tab1_Combined_VBA.vba`
**What it does**: Tab 1 automation

**Features**:
- Auto-updates "Selected Factors" table when YES/NO changes
- Green highlighting for selected factors
- Popup reminder to run 02_MODEL_REFRESH.bat after changes

#### 2. `Tab3_Combined_VBA.vba`
**What it does**: Tab 3 formatting

**Features**:
- Alternating row colors
- Conditional formatting for percentile ranks

#### 3. `Tab4_Combined_VBA.vba` ⭐ AUTO-SORT
**What it does**: Tab 4 auto-reranking

**Key feature**: `Worksheet_Calculate` event
- Triggers when weights change
- Automatically re-sorts table by composite score
- Updates rank numbers in real-time

**User experience**: Change weight → scores recalculate → table auto-sorts

#### 4. `Workbook_Open_VBA.vba`
**What it does**: Welcome message on workbook open

### Batch Files (2 files)

#### 1. `01_INSTALL_PYTHON_AND_LIBRARIES.bat`
**What it does**: One-time Python setup

**Installs**: Python, pandas, numpy, openpyxl

#### 2. `02_MODEL_REFRESH.bat` ⭐ PRIMARY LAUNCHER
**What it does**: Runs quick_update_weights.py with safety checks

**Safety features**:
- Checks Python is installed
- Auto-installs required libraries if missing
- Reminds user to close Excel file first

---

## Data Flow

```
User changes factors/universe in Tab 1
    ↓
Save & close Excel
    ↓
Run 02_MODEL_REFRESH.bat
    ↓
quick_update_weights.py reads Tab 1
    ↓
Script determines operation (1, 2, 3, or 4)
    ↓
Script updates Tab 2 and/or Tab 4
    ↓
User reopens Excel
    ↓
User changes weights in Tab 4
    ↓
Excel formulas recalculate composite scores
    ↓
VBA auto-sorts table (if enabled)
    ↓
User sees updated rankings instantly
```

---

## Key Technical Details

### Composite Score Formula (Tab 4)
**Formula structure** (example with 3 factors):
```
= (I9*$B$6 + K9*$B$7 + M9*$B$8) / 100
```

Where:
- I9, K9, M9 = Factor percentile scores (0-100)
- $B$6, $B$7, $B$8 = Weight percentages (must sum to 100%)
- Result: Weighted composite score (0-100)

**Why formulas, not static values**: Instant recalculation when weights change

### Universe Column Mapping
```python
UNIVERSE_OPTIONS = {
    'S&P 500': 'wt_ivv',
    'Russell 1000': 'wt_iwb',
    'Russell 1000 Value': 'wt_iwd',
    'MSCI ACWI ex-US': 'wt_acwx',
    'MSCI EAFE': 'wt_efa',
    'MSCI EAFE Value': 'wt_efv'
}
```

### Data Source
**File**: `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx`
**Date**: October 28, 2025
**Factors**: 255 factors across 11 categories
**Securities**: ~3,000+ securities
**Update frequency**: Monthly (date in filename)

---

## Factor Categories (11)

1. **Size** (11 factors): mkt_val, bv, ev, sales, assets, etc.
2. **Efficiency** (11 factors): asset_turn_chg_1yr, receiv_turn_chg_1yr, etc.
3. **Growth** (25 factors): sales_gr_1yr, eps_gr_1yr, ocf_gr_1yr, etc.
4. **Management** (11 factors): asset_gr_1yr, capex_gr_1yr, debt_iss_gr_1yr, etc.
5. **Profitability** (28 factors): roe, roa, roic, ebit_margin, etc.
6. **Quality** (26 factors): accruals, fcf_accruals, asset_quality, etc.
7. **Sentiment** (29 factors): earn_rev_up, earn_rev_down, rec_chg, etc.
8. **Systematic** (38 factors): beta, vol, mom, reversal, etc.
9. **Value** (30 factors): ev_ebit, pe, pb, pcf, etc.
10. **Yield** (27 factors): div_yld, fcf_yld, earn_yld, etc.
11. **Institutional** (19 factors): active_pctout, passive_pctout, hedge_pctout, etc.

**Total**: 255 factors

---

## Troubleshooting

### "No changes detected"
**Cause**: Script didn't detect factor or universe changes
**Fix**: Verify Tab 1 Active column or universe was actually changed and saved

### Composite scores don't recalculate
**Cause**: Formulas replaced with static values
**Fix**: Run `surgical_repair.py` to restore formulas

### Table doesn't auto-sort
**Cause**: VBA macros not enabled
**Fix**: Enable macros when opening Excel, or sort manually

### "Permission denied" error
**Cause**: Excel file is still open
**Fix**: Close all Excel files, run script again

### Wrong factors in Tab 4
**Cause**: Tab 1/Tab 4 out of sync
**Fix**: Run `surgical_repair.py` to rebuild from Tab 1

---

## Version History

### v2.1 (November 3, 2025) - Current
- ✅ Intelligent decision tree (4 operations)
- ✅ Excel formulas for composite scores
- ✅ Non-destructive updates (preserves VBA)
- ✅ Canonical factor mapping (100% coverage)
- ✅ Tab 1/Tab 4 synchronization validation

### v2.0 (October 30, 2025)
- ✅ Surgical repair script
- ✅ Formula-based composite scores
- ✅ Efficient bulk operations

### v1.0 (Pre-October 2025)
- Initial release
- Basic factor selection and ranking

---

## File Locations

### Active Files
```
scripts/python/
├── quick_update_weights.py          ⭐ Primary update script
├── surgical_repair.py               ⭐ Emergency repair
└── utils/
    ├── canonical_factor_mapping.py  (Factor code ↔ name mapping)
    ├── factor_definitions_registry.py (255 factor descriptions)
    └── export_factor_descriptions.py (Export definitions)

scripts/vba/
├── Tab1_Combined_VBA.vba           (Factor selection automation)
├── Tab3_Combined_VBA.vba           (Tab 3 formatting)
├── Tab4_Combined_VBA.vba           ⭐ Auto-sort on weight change
└── Workbook_Open_VBA.vba           (Welcome message)

Root:
├── Factor_Scanning_Model.xlsm      ⭐ Main Excel file
├── 02_MODEL_REFRESH.bat            ⭐ Update launcher
└── 01_INSTALL_PYTHON_AND_LIBRARIES.bat (One-time setup)
```

### Archived Files
```
scripts/python/archive/              (36+ old Python scripts)
scripts/python/archive_2025_fixes/   (Development scripts)
scripts/vba/archive/                 (Old VBA versions)
```

---

**Last Updated**: November 3, 2025
**Version**: v2.1 (Non-Destructive Architecture)
**Maintained By**: Quantitative Analytics Team
```

### security-scanner-prd----full-portal-spec-tabs-scoring-algorithm-universes-existing-patterns-to-reuse.md

```
# Security Scanner PRD

**Project:** `SSCN_PORTAL`
**Macro:** `SSCN`
**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-05
**Status:** Phase 0 -- PRD + data architecture pending

---

## Overview

Port Yang's `Factor_Scanning_Model.xlsm` to the Opal Capital portal as a new page called **Security Scanner**. The Excel workbook provides multi-factor security screening across 6 universes and 255 factors across 11 categories, letting PMs select factors, assign weights, and see dynamically ranked securities.

---

## System Being Ported

The Excel workbook has 4 tabs:

### Tab 1 (1-Configuration)

Factor selection UI with "Selected Factors" and "Factor Bank" sections, universe dropdown, YES/NO toggles. 255 factors across 11 categories (Size, Efficiency, Growth, Management, Profitability, Quality, Sentiment, Systematic, Value, Yield, Institutional). Factor metadata includes: code, display name, category, coverage (PPS), relationship (Positive/Inverse), IC, autocorrelation, systematic flag.

### Tab 2 (2-Universe Data)

Full security dataset for the selected universe. All factor raw values for all securities. Read-only reference.

### Tab 3 (3-Factor Data)

Complete factor metadata -- all 255 factors with their properties (code, name, category, asset class, relationship, IC, autocorrelation, coverage, systematic flag). Static reference data.

### Tab 4 (4-Security Scanner)

Interactive scoring -- weight table (user-editable), composite score formula `=(FactorScore1*Weight1 + ... + FactorScoreN*WeightN)/100`, auto-sort by composite, rank column, per-factor percentile scores + raw values.

VBA handles: auto-sort on weight change (Worksheet_Calculate), factor move between Bank/Selected (Worksheet_Change), alternating row formatting, yellow IC highlighting, auto-rerank on open.

---

## Portal Page Design

| Field | Value |
|-------|-------|
| **Page name** | Security Scanner |
| **Route** | `/security-scanner` |
| **Sidebar** | Tools section, above Portfolio Management |
| **Icon** | `ScanLine` (from lucide-react) |
| **Access** | `requiresDev: true` (dev-only during buildout) |

### Directory Structure

```
portal/src/pages/SecurityScanner/
  SecurityScanner.tsx      # Main page orchestrator
  index.ts                 # Re-export
  types.ts                 # TabType, FactorDefinition, SecurityRow, UniverseId, etc.
  components/
    ScannerHeaderPanel.tsx  # Universe selector, factor chips, weight controls
  tabs/
    FactorBankTab.tsx       # Tab 1: Factor selection (maps Excel Tab 1)
    UniverseDataTab.tsx     # Tab 2: Full security dataset (maps Excel Tab 2)
    FactorDataTab.tsx       # Tab 3: Factor metadata reference (maps Excel Tab 3)
    UniverseScannerTab.tsx  # Tab 4: Weighted scoring + ranking (maps Excel Tab 4)
  hooks/
    useScannerState.ts      # Central state: selectedUniverse, selectedFactors, weights
```

---

## Header Panel (ScannerHeaderPanel)

Persistent above all tabs. Contains:

- **Universe dropdown** -- S&P 500, Russell 1000, Russell 1000 Value, MSCI ACWI ex-US, MSCI EAFE, MSCI EAFE Value
- **Selected factor chips** -- visual summary of active factors with count badge
- **Weight controls** -- inline editable weights per factor (must sum to 100%), or equal-weight button
- Summary stats: universe size, number of selected factors, total weight validation

State owned by parent `SecurityScanner.tsx`, passed down as props to both header and all tabs.

---

## Tab 1: Factor Bank

Maps to Excel "1-Configuration". Two sections:

- **Selected Factors** -- factors currently active (toggleable)
- **Factor Bank** -- all 255 factors, organized by 11 categories, with add/remove toggle
- Each factor row shows: category, display name, code, coverage (PPS), relationship, IC, autocorrelation, systematic flag
- Yellow highlight for highest-IC factor per category (matching Excel behavior)
- Filtering/search by category, name, or code

**Header interaction:** Selecting/deselecting factors here updates the header's selected factors and the scorer in Tab 4.

---

## Tab 2: Universe Data

Maps to Excel "2-Universe Data". Full security table for the selected universe:

- Columns: Ticker, Company Name, Market Value, Country (shown for international universes), Sector, Industry Group, then all selected factor raw values
- Sortable columns, AutoFilter equivalent
- Country column hidden for US universes (S&P 500, Russell 1000, Russell 1000 Value)

**Header interaction:** Changing universe in header reloads this tab's data.

---

## Tab 3: Factor Data

Maps to Excel "3-Factor Data". Static reference table showing all 255 factors:

- Columns: Factor Code, Factor Name, Category, Relationship (Positive/Inverse), Asset Class, Coverage, IC, Autocorrelation, Systematic (Yes/No)
- Conditional formatting: green highlight for "Systematic Equity" asset class, red for "No" systematic
- Sortable, filterable by category
- This tab is independent of header selections -- always shows the full factor universe

**Header interaction:** None -- this is static reference data.

---

## Tab 4: Universe Scanner

Maps to Excel "4-Security Scanner". The primary interactive tab:

- **Weight table** at top -- user edits weights for selected factors (must sum to 100%)
- **Scored securities table** -- all securities in selected universe, with:
  - Rank, Ticker, Name, Composite Score, Market Value, Country (conditional), Industry Group
  - Per-factor columns: Score (percentile 0-100) + Raw Value
- **Composite score** computed client-side: `(Sum of FactorScore_i * Weight_i) / 100`
- **Auto-sort** by composite score descending when weights change
- **Conditional formatting**: quintile colors on score columns, gradient on composite
- Filtering by sector, industry group, country, market cap range

**Header interaction:** Responds to both universe changes AND factor/weight changes.

---

## Universes

| Universe | Excel Column | Approx Size |
|----------|-------------|-------------|
| S&P 500 | `wt_ivv` | ~500 |
| Russell 1000 | `wt_iwb` | ~1000 |
| Russell 1000 Value | `wt_iwd` | ~850 |
| MSCI ACWI ex-US | `wt_acwx` | ~1650 |
| MSCI EAFE | `wt_efa` | ~700 |
| MSCI EAFE Value | `wt_efv` | ~400 |

---

## Factor Categories (11)

| Category | Factor Count | Examples |
|----------|-------------|----------|
| Size | 11 | mkt_val, bv, ev, sales, assets |
| Efficiency | 11 | asset_turn_chg_1yr, receiv_turn_chg_1yr |
| Growth | 25 | sales_gr_1yr, eps_gr_1yr, eps_fwd_gr_1yr |
| Management | 11 | asset_gr_1yr, capex_gr_1yr, debt_iss_gr_1yr |
| Profitability | 28 | roe, roa, roic, ebit_margin |
| Quality | 26 | accruals, fcf_accruals, asset_quality |
| Sentiment | 29 | earn_rev_up, earn_rev_down, rec_chg |
| Systematic | 38 | beta, vol, mom, reversal |
| Value | 30 | ev_ebit, pe, pb, pcf |
| Yield | 27 | div_yld, fcf_yld, earn_yld |
| Institutional | 19 | active_pctout, passive_pctout, hedge_pctout |
| **Total** | **255** | |

---

## Scoring Algorithm

Per-factor percentile: `rank(factor_value, method='average') * 100` (0-100 scale).
Inverse-relationship factors: negate value before ranking.
Composite: `(Sum of percentile_i * weight_i) / 100`.

---

## Data Architecture (Deferred)

Data source decisions deferred to a Pattern 0 thread (DS + DE + AE). Key questions for that thread:

- Where does the FactSet factor data live? (S3 static JSON vs Lambda-computed)
- How is the data refreshed? (Monthly FactSet export pipeline)
- Client-side percentile calculation vs server-side pre-computation
- API endpoint structure (`/api/private/security-scanner/...` or `/api/general/...`)

Current Excel data source: `Screening_DIVZ_IDVZ_20251028.xlsx` -- 255 factors, ~3000 securities, 6 universe weight columns.

### XLSM Audit Script (Thread Context Input)

An extraction script is available to produce a full structured audit of the source Excel workbook (`Factor_Scanning_Model.xlsm`). The output is a single markdown file containing sheet structure, all column headers, formulas, data validation rules, conditional formatting, factor metadata, and the complete VBA source code (all modules verbatim). This audit file should be generated before the Pattern 0 thread starts and provided as thread context to all participants.

**Script:** `scripts/extract_xlsm_audit.py`

```bash
python scripts/extract_xlsm_audit.py <path_to_Factor_Scanning_Model.xlsm>
```

**Output:** `docs/architecture/SECURITY_SCANNER_XLSM_AUDIT.md`

The script uses `openpyxl` (cell data, formulas, conditional formatting) and `oletools` (VBA extraction from `vbaProject.bin`). Both are installed.

---

## Existing Patterns to Reuse

| Pattern | Source | Location |
|---------|--------|----------|
| Multi-tab layout | AdvisorIntelligence | `portal/src/pages/AdvisorIntelligence/` |
| Tab navigation | Shared hook | `portal/src/hooks/useTabNavigation.ts` |
| Tab UI component | Shared component | `portal/src/components/TabNavigation.tsx` |
| Page header | Shared component | `portal/src/components/PageHeaderVariants.tsx` (`PageHeaderCleanBadge`) |
| Error boundary per tab | AdvisorIntelligence | `ErrorBoundary` + `TabErrorFallback` |
| Gradient/quintile coloring | PortfolioManagement | `portal/src/pages/PortfolioManagement/utils/colorUtils.ts` |
| Canonical factor order | PortfolioManagement | `portal/src/pages/PortfolioManagement/utils/factorOrder.ts` |
| State pattern (simple) | AdvisorIntelligence | `useState` for entity selection |

---

## Next Steps

1. COO reads this PRD
2. Pattern 0 thread (DS + DE + AE) for data architecture decisions
3. Task order decomposition to Pod 3 DE after data architecture is resolved
4. RD agent `0.3.4_RD_SecurityScanner` receives implementation task orders
```

### xlsm-audit----full-factorscanningmodelxlsm-structure-sheet-dimensions-header-rows-data-validation-conditional-formatting-formulas-factor-metadata-tab-3-and-complete-vba-source-worksheetcalculate-worksheetchange.md

```
## Sheet Structure

### Sheet: `1-Configuration`

- **Dimensions:** A1:K303
- **Max row:** 303
- **Max col:** 11
- **Merged cells:** 15
  - `A4:B4`
  - `A5:C5`
  - `A8:C8`
  - `E5:J5`
  - `A6:C6`
  - `H8:J8`
  - `E8:G8`
  - `A10:J10`
  - `A2:J2`
  - `E4:J4`
  - `A7:C7`
  - `E6:J6`
  - `C9:G9`
  - `A33:J33`
  - `E7:J7`

### Sheet: `2-Universe Data`

- **Dimensions:** A1:XFD508
- **Max row:** 508
- **Max col:** 16384
- **Merged cells:** 4
  - `A3:F3`
  - `A1:XFD1`
  - `A2:D2`
  - `A4:F4`

### Sheet: `3-Factor Data`

- **Dimensions:** A1:N293
- **Max row:** 293
- **Max col:** 14
- **Merged cells:** 4
  - `A4:B4`
  - `A3:B3`
  - `A2:B2`
  - `A1:B1`

### Sheet: `4-Security Scanner`

- **Dimensions:** A1:XFD531
- **Max row:** 531
- **Max col:** 16384
- **Merged cells:** 22
  - `R28:S28`
  - `J28:K28`
  - `L28:M28`
  - `V28:W28`
  - `X28:Y28`
  - `AD28:AE28`
  - `AJ28:AK28`
  - `AL28:AM28`
  - `AR28:AS28`
  - `A1:XFD1`
  - `A3:H3`
  - `N28:O28`
  - `P28:Q28`
  - `H28:I28`
  - `Z28:AA28`
  - `AB28:AC28`
  - `T28:U28`
  - `AF28:AG28`
  - `A2:D2`
  - `AH28:AI28`
  - ... and 2 more


---

## Header Rows (first 3 rows per sheet)

### Sheet `1-Configuration`

```
Row 1:  |  |  |  |  |  |  |  |  |  | 
Row 2:  |  |  |  |  |  |  |  |  |  | 
Row 3:  |  |  |  |  |  |  |  |  |  | 
```

### Sheet `2-Universe Data`

```
Row 1:  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 2: Complete Index Data |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 3: All securities available fo... |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
  ... (16354 more columns)
```

### Sheet `3-Factor Data`

```
Row 1:  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 2: Factor Intelligence Library |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 3: View universal factor detai... |  |  |  |  |  |  |  |  |  |  |  |  | 
```

### Sheet `4-Security Scanner`

```
Row 1:  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 2: S&P 500 Security Scoring & ... |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 3: Adjust factor weights (must... |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
  ... (16354 more columns)
```

## Defined Names

(none)

## Data Validation Rules

### Sheet `1-Configuration` -- cells `C4`

- **Type:** list
- **Allow blank:** True
- **Formula1:** `"S&P 500,Russell 1000,Russell 1000 Value,MSCI ACWI ex-US,MSCI EAFE,MSCI EAFE Value"`

## Conditional Formatting Rules

### Sheet `1-Configuration` -- `F12:F30 F35:F302`

- **Type:** cellIs
- **Priority:** 49
- **Formula:** `['"Yes"']`
- **Fill color:** FFC6EFCE
- **Font color:** FF006100

### Sheet `1-Configuration` -- `H12:H30 H35:H302`

- **Type:** cellIs
- **Priority:** 50
- **Formula:** `['"Positive"']`
- **Fill color:** FFC6EFCE
- **Font color:** FF006100

### Sheet `1-Configuration` -- `H12:H30 H35:H302`

- **Type:** cellIs
- **Priority:** 51
- **Formula:** `['"Inverse"']`
- **Fill color:** FFFFC7CE
- **Font color:** FF9C0006

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 191
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0),G12<PERCENTILE($G$31:$G$302,0.2))']`
- **Fill color:** FFF8696B

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 192
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.2),G12<PERCENTILE($G$31:$G$302,0.4))']`
- **Fill color:** FFFFA500

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 193
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.4),G12<PERCENTILE($G$31:$G$302,0.6))']`
- **Fill color:** FFFFEB84

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 194
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.6),G12<PERCENTILE($G$31:$G$302,0.8))']`
- **Fill color:** FF9ACD32

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 195
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.8))']`
- **Fill color:** FF63BE7B

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 206
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0),I12<PERCENTILE($I$31:$I$302,0.2))']`
- **Fill color:** FFF8696B

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 207
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.2),I12<PERCENTILE($I$31:$I$302,0.4))']`
- **Fill color:** FFFFA500

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 208
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.4),I12<PERCENTILE($I$31:$I$302,0.6))']`
- **Fill color:** FFFFEB84

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 209
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.6),I12<PERCENTILE($I$31:$I$302,0.8))']`
- **Fill color:** FF9ACD32

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 210
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.8))']`
- **Fill color:** FF63BE7B

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 221
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0),J12<PERCENTILE($J$31:$J$302,0.2))']`
- **Fill color:** FFF8696B

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 222
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.2),J12<PERCENTILE($J$31:$J$302,0.4))']`
- **Fill color:** FFFFA500

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 223
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.4),J12<PERCENTILE($J$31:$J$302,0.6))']`
- **Fill color:** FFFFEB84

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 224
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.6),J12<PERCENTILE($J$31:$J$302,0.8))']`
- **Fill color:** FF9ACD32

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 225
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.8))']`
- **Fill color:** FF63BE7B

### Sheet `3-Factor Data` -- `N1:N1048576`

- **Type:** cellIs
- **Priority:** 3
- **Formula:** `['"Yes"']`
- **Fill color:** 00000000
- **Font color:** FF006100

### Sheet `3-Factor Data` -- `N1:N1048576`

- **Type:** cellIs
- **Priority:** 4
- **Formula:** `['"Yes"']`
- **Fill color:** 00000000

### Sheet `3-Factor Data` -- `D7:D293`

- **Type:** cellIs
- **Priority:** 1
- **Formula:** `['"Positive"']`
- **Fill color:** 00000000
- **Font color:** FF006100

### Sheet `3-Factor Data` -- `D7:D293`

- **Type:** cellIs
- **Priority:** 2
- **Formula:** `['"Inverse"']`
- **Fill color:** 00000000
- **Font color:** FF9C0006

### Sheet `4-Security Scanner` -- `D30:D713`

- **Type:** colorScale
- **Priority:** 102
- **Color scale:** <openpyxl.formatting.rule.ColorScale object>
Parameters:
cfvo=[<openpyxl.formatting.rule.FormatObject object>
Parameters:
type='min', val=None, gte=None, <openpyxl.formatting.rule.FormatObject object>
Parameters:
type='percentile', val=50.0, gte=None, <openpyxl.formatting.rule.FormatObject object>
Parameters:
type='max', val=None, gte=None], color=[<openpyxl.styles.colors.Color object>
Parameters:
rgb='FFF8696B', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', <openpyxl.styles.colors.Color object>
Parameters:
rgb='FFFFEB84', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', <openpyxl.styles.colors.Color object>
Parameters:
rgb='FF63BE7B', indexed=None, auto=None, theme=None, tint=0.0, type='rgb']

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 103
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 104
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 105
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 106
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 107
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 108
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 109
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 110
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 111
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 112
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 113
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 114
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 115
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 116
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 117
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 118
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 119
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 120
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 121
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 122
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 123
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 124
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 125
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 126
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 127
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 128
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 129
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 130
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 131
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 132
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 133
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 134
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 135
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 136
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 137
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 138
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 139
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 140
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 141
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 142
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 143
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 144
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 145
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 146
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 147
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 148
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 149
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 150
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 151
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 152
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 153
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 154
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 155
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 156
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 157
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 158
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 159
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 160
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 161
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 162
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 163
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 164
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 165
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 166
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 167
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 168
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 169
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 170
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 171
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 172
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 173
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 174
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 175
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 176
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 177
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 178
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 179
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 180
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 181
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 182
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 183
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 184
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 185
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 186
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 187
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 188
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 189
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 190
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 191
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 192
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 193
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 194
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 195
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 196
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 197
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

## Formulas

### Sheet `1-Configuration` (1148 formulas)

| Cell | Formula |
|------|---------|
| `G12` | `=IFERROR(ROUND(VLOOKUP(E12,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H12` | `=IFERROR(VLOOKUP(E12,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I12` | `=IFERROR(ROUND(VLOOKUP(E12,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J12` | `=IFERROR(VLOOKUP(E12,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G13` | `=IFERROR(ROUND(VLOOKUP(E13,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H13` | `=IFERROR(VLOOKUP(E13,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I13` | `=IFERROR(ROUND(VLOOKUP(E13,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J13` | `=IFERROR(VLOOKUP(E13,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G14` | `=IFERROR(ROUND(VLOOKUP(E14,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H14` | `=IFERROR(VLOOKUP(E14,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I14` | `=IFERROR(ROUND(VLOOKUP(E14,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J14` | `=IFERROR(VLOOKUP(E14,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G15` | `=IFERROR(ROUND(VLOOKUP(E15,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H15` | `=IFERROR(VLOOKUP(E15,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I15` | `=IFERROR(ROUND(VLOOKUP(E15,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J15` | `=IFERROR(VLOOKUP(E15,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G16` | `=IFERROR(ROUND(VLOOKUP(E16,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H16` | `=IFERROR(VLOOKUP(E16,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I16` | `=IFERROR(ROUND(VLOOKUP(E16,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J16` | `=IFERROR(VLOOKUP(E16,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G17` | `=IFERROR(ROUND(VLOOKUP(E17,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H17` | `=IFERROR(VLOOKUP(E17,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I17` | `=IFERROR(ROUND(VLOOKUP(E17,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J17` | `=IFERROR(VLOOKUP(E17,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G18` | `=IFERROR(ROUND(VLOOKUP(E18,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H18` | `=IFERROR(VLOOKUP(E18,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I18` | `=IFERROR(ROUND(VLOOKUP(E18,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J18` | `=IFERROR(VLOOKUP(E18,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G19` | `=IFERROR(ROUND(VLOOKUP(E19,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H19` | `=IFERROR(VLOOKUP(E19,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I19` | `=IFERROR(ROUND(VLOOKUP(E19,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J19` | `=IFERROR(VLOOKUP(E19,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G20` | `=IFERROR(ROUND(VLOOKUP(E20,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H20` | `=IFERROR(VLOOKUP(E20,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I20` | `=IFERROR(ROUND(VLOOKUP(E20,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J20` | `=IFERROR(VLOOKUP(E20,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G21` | `=IFERROR(ROUND(VLOOKUP(E21,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H21` | `=IFERROR(VLOOKUP(E21,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I21` | `=IFERROR(ROUND(VLOOKUP(E21,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J21` | `=IFERROR(VLOOKUP(E21,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G22` | `=IFERROR(ROUND(VLOOKUP(E22,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H22` | `=IFERROR(VLOOKUP(E22,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I22` | `=IFERROR(ROUND(VLOOKUP(E22,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J22` | `=IFERROR(VLOOKUP(E22,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G23` | `=IFERROR(ROUND(VLOOKUP(E23,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H23` | `=IFERROR(VLOOKUP(E23,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I23` | `=IFERROR(ROUND(VLOOKUP(E23,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J23` | `=IFERROR(VLOOKUP(E23,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G24` | `=IFERROR(ROUND(VLOOKUP(E24,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H24` | `=IFERROR(VLOOKUP(E24,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I24` | `=IFERROR(ROUND(VLOOKUP(E24,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J24` | `=IFERROR(VLOOKUP(E24,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G25` | `=IFERROR(ROUND(VLOOKUP(E25,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H25` | `=IFERROR(VLOOKUP(E25,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I25` | `=IFERROR(ROUND(VLOOKUP(E25,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J25` | `=IFERROR(VLOOKUP(E25,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G26` | `=IFERROR(ROUND(VLOOKUP(E26,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H26` | `=IFERROR(VLOOKUP(E26,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I26` | `=IFERROR(ROUND(VLOOKUP(E26,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J26` | `=IFERROR(VLOOKUP(E26,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G27` | `=IFERROR(ROUND(VLOOKUP(E27,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H27` | `=IFERROR(VLOOKUP(E27,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I27` | `=IFERROR(ROUND(VLOOKUP(E27,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J27` | `=IFERROR(VLOOKUP(E27,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G28` | `=IFERROR(ROUND(VLOOKUP(E28,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H28` | `=IFERROR(VLOOKUP(E28,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I28` | `=IFERROR(ROUND(VLOOKUP(E28,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J28` | `=IFERROR(VLOOKUP(E28,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G29` | `=IFERROR(ROUND(VLOOKUP(E29,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H29` | `=IFERROR(VLOOKUP(E29,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I29` | `=IFERROR(ROUND(VLOOKUP(E29,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J29` | `=IFERROR(VLOOKUP(E29,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G30` | `=IFERROR(ROUND(VLOOKUP(E30,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H30` | `=IFERROR(VLOOKUP(E30,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I30` | `=IFERROR(ROUND(VLOOKUP(E30,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J30` | `=IFERROR(VLOOKUP(E30,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G35` | `=IFERROR(ROUND(VLOOKUP(E35,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H35` | `=IFERROR(VLOOKUP(E35,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I35` | `=IFERROR(ROUND(VLOOKUP(E35,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J35` | `=IFERROR(VLOOKUP(E35,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G36` | `=IFERROR(ROUND(VLOOKUP(E36,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H36` | `=IFERROR(VLOOKUP(E36,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I36` | `=IFERROR(ROUND(VLOOKUP(E36,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J36` | `=IFERROR(VLOOKUP(E36,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G37` | `=IFERROR(ROUND(VLOOKUP(E37,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H37` | `=IFERROR(VLOOKUP(E37,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I37` | `=IFERROR(ROUND(VLOOKUP(E37,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J37` | `=IFERROR(VLOOKUP(E37,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G38` | `=IFERROR(ROUND(VLOOKUP(E38,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H38` | `=IFERROR(VLOOKUP(E38,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I38` | `=IFERROR(ROUND(VLOOKUP(E38,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J38` | `=IFERROR(VLOOKUP(E38,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G39` | `=IFERROR(ROUND(VLOOKUP(E39,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H39` | `=IFERROR(VLOOKUP(E39,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I39` | `=IFERROR(ROUND(VLOOKUP(E39,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J39` | `=IFERROR(VLOOKUP(E39,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G40` | `=IFERROR(ROUND(VLOOKUP(E40,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H40` | `=IFERROR(VLOOKUP(E40,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I40` | `=IFERROR(ROUND(VLOOKUP(E40,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J40` | `=IFERROR(VLOOKUP(E40,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G41` | `=IFERROR(ROUND(VLOOKUP(E41,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H41` | `=IFERROR(VLOOKUP(E41,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I41` | `=IFERROR(ROUND(VLOOKUP(E41,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J41` | `=IFERROR(VLOOKUP(E41,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G42` | `=IFERROR(ROUND(VLOOKUP(E42,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H42` | `=IFERROR(VLOOKUP(E42,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I42` | `=IFERROR(ROUND(VLOOKUP(E42,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J42` | `=IFERROR(VLOOKUP(E42,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G43` | `=IFERROR(ROUND(VLOOKUP(E43,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H43` | `=IFERROR(VLOOKUP(E43,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I43` | `=IFERROR(ROUND(VLOOKUP(E43,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J43` | `=IFERROR(VLOOKUP(E43,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G44` | `=IFERROR(ROUND(VLOOKUP(E44,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H44` | `=IFERROR(VLOOKUP(E44,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I44` | `=IFERROR(ROUND(VLOOKUP(E44,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J44` | `=IFERROR(VLOOKUP(E44,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G45` | `=IFERROR(ROUND(VLOOKUP(E45,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H45` | `=IFERROR(VLOOKUP(E45,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I45` | `=IFERROR(ROUND(VLOOKUP(E45,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J45` | `=IFERROR(VLOOKUP(E45,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G46` | `=IFERROR(ROUND(VLOOKUP(E46,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H46` | `=IFERROR(VLOOKUP(E46,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I46` | `=IFERROR(ROUND(VLOOKUP(E46,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J46` | `=IFERROR(VLOOKUP(E46,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G47` | `=IFERROR(ROUND(VLOOKUP(E47,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H47` | `=IFERROR(VLOOKUP(E47,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I47` | `=IFERROR(ROUND(VLOOKUP(E47,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J47` | `=IFERROR(VLOOKUP(E47,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G48` | `=IFERROR(ROUND(VLOOKUP(E48,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H48` | `=IFERROR(VLOOKUP(E48,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I48` | `=IFERROR(ROUND(VLOOKUP(E48,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J48` | `=IFERROR(VLOOKUP(E48,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G49` | `=IFERROR(ROUND(VLOOKUP(E49,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H49` | `=IFERROR(VLOOKUP(E49,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I49` | `=IFERROR(ROUND(VLOOKUP(E49,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J49` | `=IFERROR(VLOOKUP(E49,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G50` | `=IFERROR(ROUND(VLOOKUP(E50,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H50` | `=IFERROR(VLOOKUP(E50,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I50` | `=IFERROR(ROUND(VLOOKUP(E50,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J50` | `=IFERROR(VLOOKUP(E50,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G51` | `=IFERROR(ROUND(VLOOKUP(E51,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H51` | `=IFERROR(VLOOKUP(E51,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I51` | `=IFERROR(ROUND(VLOOKUP(E51,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J51` | `=IFERROR(VLOOKUP(E51,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G52` | `=IFERROR(ROUND(VLOOKUP(E52,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H52` | `=IFERROR(VLOOKUP(E52,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I52` | `=IFERROR(ROUND(VLOOKUP(E52,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J52` | `=IFERROR(VLOOKUP(E52,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G53` | `=IFERROR(ROUND(VLOOKUP(E53,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H53` | `=IFERROR(VLOOKUP(E53,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I53` | `=IFERROR(ROUND(VLOOKUP(E53,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J53` | `=IFERROR(VLOOKUP(E53,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G54` | `=IFERROR(ROUND(VLOOKUP(E54,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H54` | `=IFERROR(VLOOKUP(E54,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I54` | `=IFERROR(ROUND(VLOOKUP(E54,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J54` | `=IFERROR(VLOOKUP(E54,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G55` | `=IFERROR(ROUND(VLOOKUP(E55,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H55` | `=IFERROR(VLOOKUP(E55,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I55` | `=IFERROR(ROUND(VLOOKUP(E55,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J55` | `=IFERROR(VLOOKUP(E55,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G56` | `=IFERROR(ROUND(VLOOKUP(E56,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H56` | `=IFERROR(VLOOKUP(E56,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I56` | `=IFERROR(ROUND(VLOOKUP(E56,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J56` | `=IFERROR(VLOOKUP(E56,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G57` | `=IFERROR(ROUND(VLOOKUP(E57,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H57` | `=IFERROR(VLOOKUP(E57,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I57` | `=IFERROR(ROUND(VLOOKUP(E57,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J57` | `=IFERROR(VLOOKUP(E57,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G58` | `=IFERROR(ROUND(VLOOKUP(E58,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H58` | `=IFERROR(VLOOKUP(E58,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I58` | `=IFERROR(ROUND(VLOOKUP(E58,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J58` | `=IFERROR(VLOOKUP(E58,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G59` | `=IFERROR(ROUND(VLOOKUP(E59,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H59` | `=IFERROR(VLOOKUP(E59,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I59` | `=IFERROR(ROUND(VLOOKUP(E59,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J59` | `=IFERROR(VLOOKUP(E59,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G60` | `=IFERROR(ROUND(VLOOKUP(E60,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H60` | `=IFERROR(VLOOKUP(E60,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I60` | `=IFERROR(ROUND(VLOOKUP(E60,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J60` | `=IFERROR(VLOOKUP(E60,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G61` | `=IFERROR(ROUND(VLOOKUP(E61,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H61` | `=IFERROR(VLOOKUP(E61,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I61` | `=IFERROR(ROUND(VLOOKUP(E61,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J61` | `=IFERROR(VLOOKUP(E61,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G62` | `=IFERROR(ROUND(VLOOKUP(E62,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H62` | `=IFERROR(VLOOKUP(E62,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I62` | `=IFERROR(ROUND(VLOOKUP(E62,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J62` | `=IFERROR(VLOOKUP(E62,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G63` | `=IFERROR(ROUND(VLOOKUP(E63,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H63` | `=IFERROR(VLOOKUP(E63,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I63` | `=IFERROR(ROUND(VLOOKUP(E63,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J63` | `=IFERROR(VLOOKUP(E63,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G64` | `=IFERROR(ROUND(VLOOKUP(E64,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H64` | `=IFERROR(VLOOKUP(E64,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I64` | `=IFERROR(ROUND(VLOOKUP(E64,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J64` | `=IFERROR(VLOOKUP(E64,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G65` | `=IFERROR(ROUND(VLOOKUP(E65,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H65` | `=IFERROR(VLOOKUP(E65,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I65` | `=IFERROR(ROUND(VLOOKUP(E65,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J65` | `=IFERROR(VLOOKUP(E65,'3-Factor Data'!C:N,10,FALSE),"")` |

... and 948 more formulas (truncated)

### Sheet `4-Security Scanner` (503 formulas)

| Cell | Formula |
|------|---------|
| `C26` | `=SUM(C7:C25)` |
| `D30` | `=(H30*$C$7+J30*$C$8+L30*$C$9+N30*$C$10+P30*$C$11+R30*$C$12+T30*$C$13+V30*$C$14+X30*$C$15+Z30*$C$16+AB30*$C$17+AD30*$C$18+AF30*$C$19+AH30*$C$20+AJ30*$C$21+AL30*$C$22+AN30*$C$23+AP30*$C$24+AR30*$C$25...` |
| `D31` | `=(H31*$C$7+J31*$C$8+L31*$C$9+N31*$C$10+P31*$C$11+R31*$C$12+T31*$C$13+V31*$C$14+X31*$C$15+Z31*$C$16+AB31*$C$17+AD31*$C$18+AF31*$C$19+AH31*$C$20+AJ31*$C$21+AL31*$C$22+AN31*$C$23+AP31*$C$24+AR31*$C$25...` |
| `D32` | `=(H32*$C$7+J32*$C$8+L32*$C$9+N32*$C$10+P32*$C$11+R32*$C$12+T32*$C$13+V32*$C$14+X32*$C$15+Z32*$C$16+AB32*$C$17+AD32*$C$18+AF32*$C$19+AH32*$C$20+AJ32*$C$21+AL32*$C$22+AN32*$C$23+AP32*$C$24+AR32*$C$25...` |
| `D33` | `=(H33*$C$7+J33*$C$8+L33*$C$9+N33*$C$10+P33*$C$11+R33*$C$12+T33*$C$13+V33*$C$14+X33*$C$15+Z33*$C$16+AB33*$C$17+AD33*$C$18+AF33*$C$19+AH33*$C$20+AJ33*$C$21+AL33*$C$22+AN33*$C$23+AP33*$C$24+AR33*$C$25...` |
| `D34` | `=(H34*$C$7+J34*$C$8+L34*$C$9+N34*$C$10+P34*$C$11+R34*$C$12+T34*$C$13+V34*$C$14+X34*$C$15+Z34*$C$16+AB34*$C$17+AD34*$C$18+AF34*$C$19+AH34*$C$20+AJ34*$C$21+AL34*$C$22+AN34*$C$23+AP34*$C$24+AR34*$C$25...` |
| `D35` | `=(H35*$C$7+J35*$C$8+L35*$C$9+N35*$C$10+P35*$C$11+R35*$C$12+T35*$C$13+V35*$C$14+X35*$C$15+Z35*$C$16+AB35*$C$17+AD35*$C$18+AF35*$C$19+AH35*$C$20+AJ35*$C$21+AL35*$C$22+AN35*$C$23+AP35*$C$24+AR35*$C$25...` |
| `D36` | `=(H36*$C$7+J36*$C$8+L36*$C$9+N36*$C$10+P36*$C$11+R36*$C$12+T36*$C$13+V36*$C$14+X36*$C$15+Z36*$C$16+AB36*$C$17+AD36*$C$18+AF36*$C$19+AH36*$C$20+AJ36*$C$21+AL36*$C$22+AN36*$C$23+AP36*$C$24+AR36*$C$25...` |
| `D37` | `=(H37*$C$7+J37*$C$8+L37*$C$9+N37*$C$10+P37*$C$11+R37*$C$12+T37*$C$13+V37*$C$14+X37*$C$15+Z37*$C$16+AB37*$C$17+AD37*$C$18+AF37*$C$19+AH37*$C$20+AJ37*$C$21+AL37*$C$22+AN37*$C$23+AP37*$C$24+AR37*$C$25...` |
| `D38` | `=(H38*$C$7+J38*$C$8+L38*$C$9+N38*$C$10+P38*$C$11+R38*$C$12+T38*$C$13+V38*$C$14+X38*$C$15+Z38*$C$16+AB38*$C$17+AD38*$C$18+AF38*$C$19+AH38*$C$20+AJ38*$C$21+AL38*$C$22+AN38*$C$23+AP38*$C$24+AR38*$C$25...` |
| `D39` | `=(H39*$C$7+J39*$C$8+L39*$C$9+N39*$C$10+P39*$C$11+R39*$C$12+T39*$C$13+V39*$C$14+X39*$C$15+Z39*$C$16+AB39*$C$17+AD39*$C$18+AF39*$C$19+AH39*$C$20+AJ39*$C$21+AL39*$C$22+AN39*$C$23+AP39*$C$24+AR39*$C$25...` |
| `D40` | `=(H40*$C$7+J40*$C$8+L40*$C$9+N40*$C$10+P40*$C$11+R40*$C$12+T40*$C$13+V40*$C$14+X40*$C$15+Z40*$C$16+AB40*$C$17+AD40*$C$18+AF40*$C$19+AH40*$C$20+AJ40*$C$21+AL40*$C$22+AN40*$C$23+AP40*$C$24+AR40*$C$25...` |
| `D41` | `=(H41*$C$7+J41*$C$8+L41*$C$9+N41*$C$10+P41*$C$11+R41*$C$12+T41*$C$13+V41*$C$14+X41*$C$15+Z41*$C$16+AB41*$C$17+AD41*$C$18+AF41*$C$19+AH41*$C$20+AJ41*$C$21+AL41*$C$22+AN41*$C$23+AP41*$C$24+AR41*$C$25...` |
| `D42` | `=(H42*$C$7+J42*$C$8+L42*$C$9+N42*$C$10+P42*$C$11+R42*$C$12+T42*$C$13+V42*$C$14+X42*$C$15+Z42*$C$16+AB42*$C$17+AD42*$C$18+AF42*$C$19+AH42*$C$20+AJ42*$C$21+AL42*$C$22+AN42*$C$23+AP42*$C$24+AR42*$C$25...` |
| `D43` | `=(H43*$C$7+J43*$C$8+L43*$C$9+N43*$C$10+P43*$C$11+R43*$C$12+T43*$C$13+V43*$C$14+X43*$C$15+Z43*$C$16+AB43*$C$17+AD43*$C$18+AF43*$C$19+AH43*$C$20+AJ43*$C$21+AL43*$C$22+AN43*$C$23+AP43*$C$24+AR43*$C$25...` |
| `D44` | `=(H44*$C$7+J44*$C$8+L44*$C$9+N44*$C$10+P44*$C$11+R44*$C$12+T44*$C$13+V44*$C$14+X44*$C$15+Z44*$C$16+AB44*$C$17+AD44*$C$18+AF44*$C$19+AH44*$C$20+AJ44*$C$21+AL44*$C$22+AN44*$C$23+AP44*$C$24+AR44*$C$25...` |
| `D45` | `=(H45*$C$7+J45*$C$8+L45*$C$9+N45*$C$10+P45*$C$11+R45*$C$12+T45*$C$13+V45*$C$14+X45*$C$15+Z45*$C$16+AB45*$C$17+AD45*$C$18+AF45*$C$19+AH45*$C$20+AJ45*$C$21+AL45*$C$22+AN45*$C$23+AP45*$C$24+AR45*$C$25...` |
| `D46` | `=(H46*$C$7+J46*$C$8+L46*$C$9+N46*$C$10+P46*$C$11+R46*$C$12+T46*$C$13+V46*$C$14+X46*$C$15+Z46*$C$16+AB46*$C$17+AD46*$C$18+AF46*$C$19+AH46*$C$20+AJ46*$C$21+AL46*$C$22+AN46*$C$23+AP46*$C$24+AR46*$C$25...` |
| `D47` | `=(H47*$C$7+J47*$C$8+L47*$C$9+N47*$C$10+P47*$C$11+R47*$C$12+T47*$C$13+V47*$C$14+X47*$C$15+Z47*$C$16+AB47*$C$17+AD47*$C$18+AF47*$C$19+AH47*$C$20+AJ47*$C$21+AL47*$C$22+AN47*$C$23+AP47*$C$24+AR47*$C$25...` |
| `D48` | `=(H48*$C$7+J48*$C$8+L48*$C$9+N48*$C$10+P48*$C$11+R48*$C$12+T48*$C$13+V48*$C$14+X48*$C$15+Z48*$C$16+AB48*$C$17+AD48*$C$18+AF48*$C$19+AH48*$C$20+AJ48*$C$21+AL48*$C$22+AN48*$C$23+AP48*$C$24+AR48*$C$25...` |
| `D49` | `=(H49*$C$7+J49*$C$8+L49*$C$9+N49*$C$10+P49*$C$11+R49*$C$12+T49*$C$13+V49*$C$14+X49*$C$15+Z49*$C$16+AB49*$C$17+AD49*$C$18+AF49*$C$19+AH49*$C$20+AJ49*$C$21+AL49*$C$22+AN49*$C$23+AP49*$C$24+AR49*$C$25...` |
| `D50` | `=(H50*$C$7+J50*$C$8+L50*$C$9+N50*$C$10+P50*$C$11+R50*$C$12+T50*$C$13+V50*$C$14+X50*$C$15+Z50*$C$16+AB50*$C$17+AD50*$C$18+AF50*$C$19+AH50*$C$20+AJ50*$C$21+AL50*$C$22+AN50*$C$23+AP50*$C$24+AR50*$C$25...` |
| `D51` | `=(H51*$C$7+J51*$C$8+L51*$C$9+N51*$C$10+P51*$C$11+R51*$C$12+T51*$C$13+V51*$C$14+X51*$C$15+Z51*$C$16+AB51*$C$17+AD51*$C$18+AF51*$C$19+AH51*$C$20+AJ51*$C$21+AL51*$C$22+AN51*$C$23+AP51*$C$24+AR51*$C$25...` |
| `D52` | `=(H52*$C$7+J52*$C$8+L52*$C$9+N52*$C$10+P52*$C$11+R52*$C$12+T52*$C$13+V52*$C$14+X52*$C$15+Z52*$C$16+AB52*$C$17+AD52*$C$18+AF52*$C$19+AH52*$C$20+AJ52*$C$21+AL52*$C$22+AN52*$C$23+AP52*$C$24+AR52*$C$25...` |
| `D53` | `=(H53*$C$7+J53*$C$8+L53*$C$9+N53*$C$10+P53*$C$11+R53*$C$12+T53*$C$13+V53*$C$14+X53*$C$15+Z53*$C$16+AB53*$C$17+AD53*$C$18+AF53*$C$19+AH53*$C$20+AJ53*$C$21+AL53*$C$22+AN53*$C$23+AP53*$C$24+AR53*$C$25...` |
| `D54` | `=(H54*$C$7+J54*$C$8+L54*$C$9+N54*$C$10+P54*$C$11+R54*$C$12+T54*$C$13+V54*$C$14+X54*$C$15+Z54*$C$16+AB54*$C$17+AD54*$C$18+AF54*$C$19+AH54*$C$20+AJ54*$C$21+AL54*$C$22+AN54*$C$23+AP54*$C$24+AR54*$C$25...` |
| `D55` | `=(H55*$C$7+J55*$C$8+L55*$C$9+N55*$C$10+P55*$C$11+R55*$C$12+T55*$C$13+V55*$C$14+X55*$C$15+Z55*$C$16+AB55*$C$17+AD55*$C$18+AF55*$C$19+AH55*$C$20+AJ55*$C$21+AL55*$C$22+AN55*$C$23+AP55*$C$24+AR55*$C$25...` |
| `D56` | `=(H56*$C$7+J56*$C$8+L56*$C$9+N56*$C$10+P56*$C$11+R56*$C$12+T56*$C$13+V56*$C$14+X56*$C$15+Z56*$C$16+AB56*$C$17+AD56*$C$18+AF56*$C$19+AH56*$C$20+AJ56*$C$21+AL56*$C$22+AN56*$C$23+AP56*$C$24+AR56*$C$25...` |
| `D57` | `=(H57*$C$7+J57*$C$8+L57*$C$9+N57*$C$10+P57*$C$11+R57*$C$12+T57*$C$13+V57*$C$14+X57*$C$15+Z57*$C$16+AB57*$C$17+AD57*$C$18+AF57*$C$19+AH57*$C$20+AJ57*$C$21+AL57*$C$22+AN57*$C$23+AP57*$C$24+AR57*$C$25...` |
| `D58` | `=(H58*$C$7+J58*$C$8+L58*$C$9+N58*$C$10+P58*$C$11+R58*$C$12+T58*$C$13+V58*$C$14+X58*$C$15+Z58*$C$16+AB58*$C$17+AD58*$C$18+AF58*$C$19+AH58*$C$20+AJ58*$C$21+AL58*$C$22+AN58*$C$23+AP58*$C$24+AR58*$C$25...` |
| `D59` | `=(H59*$C$7+J59*$C$8+L59*$C$9+N59*$C$10+P59*$C$11+R59*$C$12+T59*$C$13+V59*$C$14+X59*$C$15+Z59*$C$16+AB59*$C$17+AD59*$C$18+AF59*$C$19+AH59*$C$20+AJ59*$C$21+AL59*$C$22+AN59*$C$23+AP59*$C$24+AR59*$C$25...` |
| `D60` | `=(H60*$C$7+J60*$C$8+L60*$C$9+N60*$C$10+P60*$C$11+R60*$C$12+T60*$C$13+V60*$C$14+X60*$C$15+Z60*$C$16+AB60*$C$17+AD60*$C$18+AF60*$C$19+AH60*$C$20+AJ60*$C$21+AL60*$C$22+AN60*$C$23+AP60*$C$24+AR60*$C$25...` |
| `D61` | `=(H61*$C$7+J61*$C$8+L61*$C$9+N61*$C$10+P61*$C$11+R61*$C$12+T61*$C$13+V61*$C$14+X61*$C$15+Z61*$C$16+AB61*$C$17+AD61*$C$18+AF61*$C$19+AH61*$C$20+AJ61*$C$21+AL61*$C$22+AN61*$C$23+AP61*$C$24+AR61*$C$25...` |
| `D62` | `=(H62*$C$7+J62*$C$8+L62*$C$9+N62*$C$10+P62*$C$11+R62*$C$12+T62*$C$13+V62*$C$14+X62*$C$15+Z62*$C$16+AB62*$C$17+AD62*$C$18+AF62*$C$19+AH62*$C$20+AJ62*$C$21+AL62*$C$22+AN62*$C$23+AP62*$C$24+AR62*$C$25...` |
| `D63` | `=(H63*$C$7+J63*$C$8+L63*$C$9+N63*$C$10+P63*$C$11+R63*$C$12+T63*$C$13+V63*$C$14+X63*$C$15+Z63*$C$16+AB63*$C$17+AD63*$C$18+AF63*$C$19+AH63*$C$20+AJ63*$C$21+AL63*$C$22+AN63*$C$23+AP63*$C$24+AR63*$C$25...` |
| `D64` | `=(H64*$C$7+J64*$C$8+L64*$C$9+N64*$C$10+P64*$C$11+R64*$C$12+T64*$C$13+V64*$C$14+X64*$C$15+Z64*$C$16+AB64*$C$17+AD64*$C$18+AF64*$C$19+AH64*$C$20+AJ64*$C$21+AL64*$C$22+AN64*$C$23+AP64*$C$24+AR64*$C$25...` |
| `D65` | `=(H65*$C$7+J65*$C$8+L65*$C$9+N65*$C$10+P65*$C$11+R65*$C$12+T65*$C$13+V65*$C$14+X65*$C$15+Z65*$C$16+AB65*$C$17+AD65*$C$18+AF65*$C$19+AH65*$C$20+AJ65*$C$21+AL65*$C$22+AN65*$C$23+AP65*$C$24+AR65*$C$25...` |
| `D66` | `=(H66*$C$7+J66*$C$8+L66*$C$9+N66*$C$10+P66*$C$11+R66*$C$12+T66*$C$13+V66*$C$14+X66*$C$15+Z66*$C$16+AB66*$C$17+AD66*$C$18+AF66*$C$19+AH66*$C$20+AJ66*$C$21+AL66*$C$22+AN66*$C$23+AP66*$C$24+AR66*$C$25...` |
| `D67` | `=(H67*$C$7+J67*$C$8+L67*$C$9+N67*$C$10+P67*$C$11+R67*$C$12+T67*$C$13+V67*$C$14+X67*$C$15+Z67*$C$16+AB67*$C$17+AD67*$C$18+AF67*$C$19+AH67*$C$20+AJ67*$C$21+AL67*$C$22+AN67*$C$23+AP67*$C$24+AR67*$C$25...` |
| `D68` | `=(H68*$C$7+J68*$C$8+L68*$C$9+N68*$C$10+P68*$C$11+R68*$C$12+T68*$C$13+V68*$C$14+X68*$C$15+Z68*$C$16+AB68*$C$17+AD68*$C$18+AF68*$C$19+AH68*$C$20+AJ68*$C$21+AL68*$C$22+AN68*$C$23+AP68*$C$24+AR68*$C$25...` |
| `D69` | `=(H69*$C$7+J69*$C$8+L69*$C$9+N69*$C$10+P69*$C$11+R69*$C$12+T69*$C$13+V69*$C$14+X69*$C$15+Z69*$C$16+AB69*$C$17+AD69*$C$18+AF69*$C$19+AH69*$C$20+AJ69*$C$21+AL69*$C$22+AN69*$C$23+AP69*$C$24+AR69*$C$25...` |
| `D70` | `=(H70*$C$7+J70*$C$8+L70*$C$9+N70*$C$10+P70*$C$11+R70*$C$12+T70*$C$13+V70*$C$14+X70*$C$15+Z70*$C$16+AB70*$C$17+AD70*$C$18+AF70*$C$19+AH70*$C$20+AJ70*$C$21+AL70*$C$22+AN70*$C$23+AP70*$C$24+AR70*$C$25...` |
| `D71` | `=(H71*$C$7+J71*$C$8+L71*$C$9+N71*$C$10+P71*$C$11+R71*$C$12+T71*$C$13+V71*$C$14+X71*$C$15+Z71*$C$16+AB71*$C$17+AD71*$C$18+AF71*$C$19+AH71*$C$20+AJ71*$C$21+AL71*$C$22+AN71*$C$23+AP71*$C$24+AR71*$C$25...` |
| `D72` | `=(H72*$C$7+J72*$C$8+L72*$C$9+N72*$C$10+P72*$C$11+R72*$C$12+T72*$C$13+V72*$C$14+X72*$C$15+Z72*$C$16+AB72*$C$17+AD72*$C$18+AF72*$C$19+AH72*$C$20+AJ72*$C$21+AL72*$C$22+AN72*$C$23+AP72*$C$24+AR72*$C$25...` |
| `D73` | `=(H73*$C$7+J73*$C$8+L73*$C$9+N73*$C$10+P73*$C$11+R73*$C$12+T73*$C$13+V73*$C$14+X73*$C$15+Z73*$C$16+AB73*$C$17+AD73*$C$18+AF73*$C$19+AH73*$C$20+AJ73*$C$21+AL73*$C$22+AN73*$C$23+AP73*$C$24+AR73*$C$25...` |
| `D74` | `=(H74*$C$7+J74*$C$8+L74*$C$9+N74*$C$10+P74*$C$11+R74*$C$12+T74*$C$13+V74*$C$14+X74*$C$15+Z74*$C$16+AB74*$C$17+AD74*$C$18+AF74*$C$19+AH74*$C$20+AJ74*$C$21+AL74*$C$22+AN74*$C$23+AP74*$C$24+AR74*$C$25...` |
| `D75` | `=(H75*$C$7+J75*$C$8+L75*$C$9+N75*$C$10+P75*$C$11+R75*$C$12+T75*$C$13+V75*$C$14+X75*$C$15+Z75*$C$16+AB75*$C$17+AD75*$C$18+AF75*$C$19+AH75*$C$20+AJ75*$C$21+AL75*$C$22+AN75*$C$23+AP75*$C$24+AR75*$C$25...` |
| `D76` | `=(H76*$C$7+J76*$C$8+L76*$C$9+N76*$C$10+P76*$C$11+R76*$C$12+T76*$C$13+V76*$C$14+X76*$C$15+Z76*$C$16+AB76*$C$17+AD76*$C$18+AF76*$C$19+AH76*$C$20+AJ76*$C$21+AL76*$C$22+AN76*$C$23+AP76*$C$24+AR76*$C$25...` |
| `D77` | `=(H77*$C$7+J77*$C$8+L77*$C$9+N77*$C$10+P77*$C$11+R77*$C$12+T77*$C$13+V77*$C$14+X77*$C$15+Z77*$C$16+AB77*$C$17+AD77*$C$18+AF77*$C$19+AH77*$C$20+AJ77*$C$21+AL77*$C$22+AN77*$C$23+AP77*$C$24+AR77*$C$25...` |
| `D78` | `=(H78*$C$7+J78*$C$8+L78*$C$9+N78*$C$10+P78*$C$11+R78*$C$12+T78*$C$13+V78*$C$14+X78*$C$15+Z78*$C$16+AB78*$C$17+AD78*$C$18+AF78*$C$19+AH78*$C$20+AJ78*$C$21+AL78*$C$22+AN78*$C$23+AP78*$C$24+AR78*$C$25...` |
| `D79` | `=(H79*$C$7+J79*$C$8+L79*$C$9+N79*$C$10+P79*$C$11+R79*$C$12+T79*$C$13+V79*$C$14+X79*$C$15+Z79*$C$16+AB79*$C$17+AD79*$C$18+AF79*$C$19+AH79*$C$20+AJ79*$C$21+AL79*$C$22+AN79*$C$23+AP79*$C$24+AR79*$C$25...` |
| `D80` | `=(H80*$C$7+J80*$C$8+L80*$C$9+N80*$C$10+P80*$C$11+R80*$C$12+T80*$C$13+V80*$C$14+X80*$C$15+Z80*$C$16+AB80*$C$17+AD80*$C$18+AF80*$C$19+AH80*$C$20+AJ80*$C$21+AL80*$C$22+AN80*$C$23+AP80*$C$24+AR80*$C$25...` |
| `D81` | `=(H81*$C$7+J81*$C$8+L81*$C$9+N81*$C$10+P81*$C$11+R81*$C$12+T81*$C$13+V81*$C$14+X81*$C$15+Z81*$C$16+AB81*$C$17+AD81*$C$18+AF81*$C$19+AH81*$C$20+AJ81*$C$21+AL81*$C$22+AN81*$C$23+AP81*$C$24+AR81*$C$25...` |
| `D82` | `=(H82*$C$7+J82*$C$8+L82*$C$9+N82*$C$10+P82*$C$11+R82*$C$12+T82*$C$13+V82*$C$14+X82*$C$15+Z82*$C$16+AB82*$C$17+AD82*$C$18+AF82*$C$19+AH82*$C$20+AJ82*$C$21+AL82*$C$22+AN82*$C$23+AP82*$C$24+AR82*$C$25...` |
| `D83` | `=(H83*$C$7+J83*$C$8+L83*$C$9+N83*$C$10+P83*$C$11+R83*$C$12+T83*$C$13+V83*$C$14+X83*$C$15+Z83*$C$16+AB83*$C$17+AD83*$C$18+AF83*$C$19+AH83*$C$20+AJ83*$C$21+AL83*$C$22+AN83*$C$23+AP83*$C$24+AR83*$C$25...` |
| `D84` | `=(H84*$C$7+J84*$C$8+L84*$C$9+N84*$C$10+P84*$C$11+R84*$C$12+T84*$C$13+V84*$C$14+X84*$C$15+Z84*$C$16+AB84*$C$17+AD84*$C$18+AF84*$C$19+AH84*$C$20+AJ84*$C$21+AL84*$C$22+AN84*$C$23+AP84*$C$24+AR84*$C$25...` |
| `D85` | `=(H85*$C$7+J85*$C$8+L85*$C$9+N85*$C$10+P85*$C$11+R85*$C$12+T85*$C$13+V85*$C$14+X85*$C$15+Z85*$C$16+AB85*$C$17+AD85*$C$18+AF85*$C$19+AH85*$C$20+AJ85*$C$21+AL85*$C$22+AN85*$C$23+AP85*$C$24+AR85*$C$25...` |
| `D86` | `=(H86*$C$7+J86*$C$8+L86*$C$9+N86*$C$10+P86*$C$11+R86*$C$12+T86*$C$13+V86*$C$14+X86*$C$15+Z86*$C$16+AB86*$C$17+AD86*$C$18+AF86*$C$19+AH86*$C$20+AJ86*$C$21+AL86*$C$22+AN86*$C$23+AP86*$C$24+AR86*$C$25...` |
| `D87` | `=(H87*$C$7+J87*$C$8+L87*$C$9+N87*$C$10+P87*$C$11+R87*$C$12+T87*$C$13+V87*$C$14+X87*$C$15+Z87*$C$16+AB87*$C$17+AD87*$C$18+AF87*$C$19+AH87*$C$20+AJ87*$C$21+AL87*$C$22+AN87*$C$23+AP87*$C$24+AR87*$C$25...` |
| `D88` | `=(H88*$C$7+J88*$C$8+L88*$C$9+N88*$C$10+P88*$C$11+R88*$C$12+T88*$C$13+V88*$C$14+X88*$C$15+Z88*$C$16+AB88*$C$17+AD88*$C$18+AF88*$C$19+AH88*$C$20+AJ88*$C$21+AL88*$C$22+AN88*$C$23+AP88*$C$24+AR88*$C$25...` |
| `D89` | `=(H89*$C$7+J89*$C$8+L89*$C$9+N89*$C$10+P89*$C$11+R89*$C$12+T89*$C$13+V89*$C$14+X89*$C$15+Z89*$C$16+AB89*$C$17+AD89*$C$18+AF89*$C$19+AH89*$C$20+AJ89*$C$21+AL89*$C$22+AN89*$C$23+AP89*$C$24+AR89*$C$25...` |
| `D90` | `=(H90*$C$7+J90*$C$8+L90*$C$9+N90*$C$10+P90*$C$11+R90*$C$12+T90*$C$13+V90*$C$14+X90*$C$15+Z90*$C$16+AB90*$C$17+AD90*$C$18+AF90*$C$19+AH90*$C$20+AJ90*$C$21+AL90*$C$22+AN90*$C$23+AP90*$C$24+AR90*$C$25...` |
| `D91` | `=(H91*$C$7+J91*$C$8+L91*$C$9+N91*$C$10+P91*$C$11+R91*$C$12+T91*$C$13+V91*$C$14+X91*$C$15+Z91*$C$16+AB91*$C$17+AD91*$C$18+AF91*$C$19+AH91*$C$20+AJ91*$C$21+AL91*$C$22+AN91*$C$23+AP91*$C$24+AR91*$C$25...` |
| `D92` | `=(H92*$C$7+J92*$C$8+L92*$C$9+N92*$C$10+P92*$C$11+R92*$C$12+T92*$C$13+V92*$C$14+X92*$C$15+Z92*$C$16+AB92*$C$17+AD92*$C$18+AF92*$C$19+AH92*$C$20+AJ92*$C$21+AL92*$C$22+AN92*$C$23+AP92*$C$24+AR92*$C$25...` |
| `D93` | `=(H93*$C$7+J93*$C$8+L93*$C$9+N93*$C$10+P93*$C$11+R93*$C$12+T93*$C$13+V93*$C$14+X93*$C$15+Z93*$C$16+AB93*$C$17+AD93*$C$18+AF93*$C$19+AH93*$C$20+AJ93*$C$21+AL93*$C$22+AN93*$C$23+AP93*$C$24+AR93*$C$25...` |
| `D94` | `=(H94*$C$7+J94*$C$8+L94*$C$9+N94*$C$10+P94*$C$11+R94*$C$12+T94*$C$13+V94*$C$14+X94*$C$15+Z94*$C$16+AB94*$C$17+AD94*$C$18+AF94*$C$19+AH94*$C$20+AJ94*$C$21+AL94*$C$22+AN94*$C$23+AP94*$C$24+AR94*$C$25...` |
| `D95` | `=(H95*$C$7+J95*$C$8+L95*$C$9+N95*$C$10+P95*$C$11+R95*$C$12+T95*$C$13+V95*$C$14+X95*$C$15+Z95*$C$16+AB95*$C$17+AD95*$C$18+AF95*$C$19+AH95*$C$20+AJ95*$C$21+AL95*$C$22+AN95*$C$23+AP95*$C$24+AR95*$C$25...` |
| `D96` | `=(H96*$C$7+J96*$C$8+L96*$C$9+N96*$C$10+P96*$C$11+R96*$C$12+T96*$C$13+V96*$C$14+X96*$C$15+Z96*$C$16+AB96*$C$17+AD96*$C$18+AF96*$C$19+AH96*$C$20+AJ96*$C$21+AL96*$C$22+AN96*$C$23+AP96*$C$24+AR96*$C$25...` |
| `D97` | `=(H97*$C$7+J97*$C$8+L97*$C$9+N97*$C$10+P97*$C$11+R97*$C$12+T97*$C$13+V97*$C$14+X97*$C$15+Z97*$C$16+AB97*$C$17+AD97*$C$18+AF97*$C$19+AH97*$C$20+AJ97*$C$21+AL97*$C$22+AN97*$C$23+AP97*$C$24+AR97*$C$25...` |
| `D98` | `=(H98*$C$7+J98*$C$8+L98*$C$9+N98*$C$10+P98*$C$11+R98*$C$12+T98*$C$13+V98*$C$14+X98*$C$15+Z98*$C$16+AB98*$C$17+AD98*$C$18+AF98*$C$19+AH98*$C$20+AJ98*$C$21+AL98*$C$22+AN98*$C$23+AP98*$C$24+AR98*$C$25...` |
| `D99` | `=(H99*$C$7+J99*$C$8+L99*$C$9+N99*$C$10+P99*$C$11+R99*$C$12+T99*$C$13+V99*$C$14+X99*$C$15+Z99*$C$16+AB99*$C$17+AD99*$C$18+AF99*$C$19+AH99*$C$20+AJ99*$C$21+AL99*$C$22+AN99*$C$23+AP99*$C$24+AR99*$C$25...` |
| `D100` | `=(H100*$C$7+J100*$C$8+L100*$C$9+N100*$C$10+P100*$C$11+R100*$C$12+T100*$C$13+V100*$C$14+X100*$C$15+Z100*$C$16+AB100*$C$17+AD100*$C$18+AF100*$C$19+AH100*$C$20+AJ100*$C$21+AL100*$C$22+AN100*$C$23+AP10...` |
| `D101` | `=(H101*$C$7+J101*$C$8+L101*$C$9+N101*$C$10+P101*$C$11+R101*$C$12+T101*$C$13+V101*$C$14+X101*$C$15+Z101*$C$16+AB101*$C$17+AD101*$C$18+AF101*$C$19+AH101*$C$20+AJ101*$C$21+AL101*$C$22+AN101*$C$23+AP10...` |
| `D102` | `=(H102*$C$7+J102*$C$8+L102*$C$9+N102*$C$10+P102*$C$11+R102*$C$12+T102*$C$13+V102*$C$14+X102*$C$15+Z102*$C$16+AB102*$C$17+AD102*$C$18+AF102*$C$19+AH102*$C$20+AJ102*$C$21+AL102*$C$22+AN102*$C$23+AP10...` |
| `D103` | `=(H103*$C$7+J103*$C$8+L103*$C$9+N103*$C$10+P103*$C$11+R103*$C$12+T103*$C$13+V103*$C$14+X103*$C$15+Z103*$C$16+AB103*$C$17+AD103*$C$18+AF103*$C$19+AH103*$C$20+AJ103*$C$21+AL103*$C$22+AN103*$C$23+AP10...` |
| `D104` | `=(H104*$C$7+J104*$C$8+L104*$C$9+N104*$C$10+P104*$C$11+R104*$C$12+T104*$C$13+V104*$C$14+X104*$C$15+Z104*$C$16+AB104*$C$17+AD104*$C$18+AF104*$C$19+AH104*$C$20+AJ104*$C$21+AL104*$C$22+AN104*$C$23+AP10...` |
| `D105` | `=(H105*$C$7+J105*$C$8+L105*$C$9+N105*$C$10+P105*$C$11+R105*$C$12+T105*$C$13+V105*$C$14+X105*$C$15+Z105*$C$16+AB105*$C$17+AD105*$C$18+AF105*$C$19+AH105*$C$20+AJ105*$C$21+AL105*$C$22+AN105*$C$23+AP10...` |
| `D106` | `=(H106*$C$7+J106*$C$8+L106*$C$9+N106*$C$10+P106*$C$11+R106*$C$12+T106*$C$13+V106*$C$14+X106*$C$15+Z106*$C$16+AB106*$C$17+AD106*$C$18+AF106*$C$19+AH106*$C$20+AJ106*$C$21+AL106*$C$22+AN106*$C$23+AP10...` |
| `D107` | `=(H107*$C$7+J107*$C$8+L107*$C$9+N107*$C$10+P107*$C$11+R107*$C$12+T107*$C$13+V107*$C$14+X107*$C$15+Z107*$C$16+AB107*$C$17+AD107*$C$18+AF107*$C$19+AH107*$C$20+AJ107*$C$21+AL107*$C$22+AN107*$C$23+AP10...` |
| `D108` | `=(H108*$C$7+J108*$C$8+L108*$C$9+N108*$C$10+P108*$C$11+R108*$C$12+T108*$C$13+V108*$C$14+X108*$C$15+Z108*$C$16+AB108*$C$17+AD108*$C$18+AF108*$C$19+AH108*$C$20+AJ108*$C$21+AL108*$C$22+AN108*$C$23+AP10...` |
| `D109` | `=(H109*$C$7+J109*$C$8+L109*$C$9+N109*$C$10+P109*$C$11+R109*$C$12+T109*$C$13+V109*$C$14+X109*$C$15+Z109*$C$16+AB109*$C$17+AD109*$C$18+AF109*$C$19+AH109*$C$20+AJ109*$C$21+AL109*$C$22+AN109*$C$23+AP10...` |
| `D110` | `=(H110*$C$7+J110*$C$8+L110*$C$9+N110*$C$10+P110*$C$11+R110*$C$12+T110*$C$13+V110*$C$14+X110*$C$15+Z110*$C$16+AB110*$C$17+AD110*$C$18+AF110*$C$19+AH110*$C$20+AJ110*$C$21+AL110*$C$22+AN110*$C$23+AP11...` |
| `D111` | `=(H111*$C$7+J111*$C$8+L111*$C$9+N111*$C$10+P111*$C$11+R111*$C$12+T111*$C$13+V111*$C$14+X111*$C$15+Z111*$C$16+AB111*$C$17+AD111*$C$18+AF111*$C$19+AH111*$C$20+AJ111*$C$21+AL111*$C$22+AN111*$C$23+AP11...` |
| `D112` | `=(H112*$C$7+J112*$C$8+L112*$C$9+N112*$C$10+P112*$C$11+R112*$C$12+T112*$C$13+V112*$C$14+X112*$C$15+Z112*$C$16+AB112*$C$17+AD112*$C$18+AF112*$C$19+AH112*$C$20+AJ112*$C$21+AL112*$C$22+AN112*$C$23+AP11...` |
| `D113` | `=(H113*$C$7+J113*$C$8+L113*$C$9+N113*$C$10+P113*$C$11+R113*$C$12+T113*$C$13+V113*$C$14+X113*$C$15+Z113*$C$16+AB113*$C$17+AD113*$C$18+AF113*$C$19+AH113*$C$20+AJ113*$C$21+AL113*$C$22+AN113*$C$23+AP11...` |
| `D114` | `=(H114*$C$7+J114*$C$8+L114*$C$9+N114*$C$10+P114*$C$11+R114*$C$12+T114*$C$13+V114*$C$14+X114*$C$15+Z114*$C$16+AB114*$C$17+AD114*$C$18+AF114*$C$19+AH114*$C$20+AJ114*$C$21+AL114*$C$22+AN114*$C$23+AP11...` |
| `D115` | `=(H115*$C$7+J115*$C$8+L115*$C$9+N115*$C$10+P115*$C$11+R115*$C$12+T115*$C$13+V115*$C$14+X115*$C$15+Z115*$C$16+AB115*$C$17+AD115*$C$18+AF115*$C$19+AH115*$C$20+AJ115*$C$21+AL115*$C$22+AN115*$C$23+AP11...` |
| `D116` | `=(H116*$C$7+J116*$C$8+L116*$C$9+N116*$C$10+P116*$C$11+R116*$C$12+T116*$C$13+V116*$C$14+X116*$C$15+Z116*$C$16+AB116*$C$17+AD116*$C$18+AF116*$C$19+AH116*$C$20+AJ116*$C$21+AL116*$C$22+AN116*$C$23+AP11...` |
| `D117` | `=(H117*$C$7+J117*$C$8+L117*$C$9+N117*$C$10+P117*$C$11+R117*$C$12+T117*$C$13+V117*$C$14+X117*$C$15+Z117*$C$16+AB117*$C$17+AD117*$C$18+AF117*$C$19+AH117*$C$20+AJ117*$C$21+AL117*$C$22+AN117*$C$23+AP11...` |
| `D118` | `=(H118*$C$7+J118*$C$8+L118*$C$9+N118*$C$10+P118*$C$11+R118*$C$12+T118*$C$13+V118*$C$14+X118*$C$15+Z118*$C$16+AB118*$C$17+AD118*$C$18+AF118*$C$19+AH118*$C$20+AJ118*$C$21+AL118*$C$22+AN118*$C$23+AP11...` |
| `D119` | `=(H119*$C$7+J119*$C$8+L119*$C$9+N119*$C$10+P119*$C$11+R119*$C$12+T119*$C$13+V119*$C$14+X119*$C$15+Z119*$C$16+AB119*$C$17+AD119*$C$18+AF119*$C$19+AH119*$C$20+AJ119*$C$21+AL119*$C$22+AN119*$C$23+AP11...` |
| `D120` | `=(H120*$C$7+J120*$C$8+L120*$C$9+N120*$C$10+P120*$C$11+R120*$C$12+T120*$C$13+V120*$C$14+X120*$C$15+Z120*$C$16+AB120*$C$17+AD120*$C$18+AF120*$C$19+AH120*$C$20+AJ120*$C$21+AL120*$C$22+AN120*$C$23+AP12...` |
| `D121` | `=(H121*$C$7+J121*$C$8+L121*$C$9+N121*$C$10+P121*$C$11+R121*$C$12+T121*$C$13+V121*$C$14+X121*$C$15+Z121*$C$16+AB121*$C$17+AD121*$C$18+AF121*$C$19+AH121*$C$20+AJ121*$C$21+AL121*$C$22+AN121*$C$23+AP12...` |
| `D122` | `=(H122*$C$7+J122*$C$8+L122*$C$9+N122*$C$10+P122*$C$11+R122*$C$12+T122*$C$13+V122*$C$14+X122*$C$15+Z122*$C$16+AB122*$C$17+AD122*$C$18+AF122*$C$19+AH122*$C$20+AJ122*$C$21+AL122*$C$22+AN122*$C$23+AP12...` |
| `D123` | `=(H123*$C$7+J123*$C$8+L123*$C$9+N123*$C$10+P123*$C$11+R123*$C$12+T123*$C$13+V123*$C$14+X123*$C$15+Z123*$C$16+AB123*$C$17+AD123*$C$18+AF123*$C$19+AH123*$C$20+AJ123*$C$21+AL123*$C$22+AN123*$C$23+AP12...` |
| `D124` | `=(H124*$C$7+J124*$C$8+L124*$C$9+N124*$C$10+P124*$C$11+R124*$C$12+T124*$C$13+V124*$C$14+X124*$C$15+Z124*$C$16+AB124*$C$17+AD124*$C$18+AF124*$C$19+AH124*$C$20+AJ124*$C$21+AL124*$C$22+AN124*$C$23+AP12...` |
| `D125` | `=(H125*$C$7+J125*$C$8+L125*$C$9+N125*$C$10+P125*$C$11+R125*$C$12+T125*$C$13+V125*$C$14+X125*$C$15+Z125*$C$16+AB125*$C$17+AD125*$C$18+AF125*$C$19+AH125*$C$20+AJ125*$C$21+AL125*$C$22+AN125*$C$23+AP12...` |
| `D126` | `=(H126*$C$7+J126*$C$8+L126*$C$9+N126*$C$10+P126*$C$11+R126*$C$12+T126*$C$13+V126*$C$14+X126*$C$15+Z126*$C$16+AB126*$C$17+AD126*$C$18+AF126*$C$19+AH126*$C$20+AJ126*$C$21+AL126*$C$22+AN126*$C$23+AP12...` |
| `D127` | `=(H127*$C$7+J127*$C$8+L127*$C$9+N127*$C$10+P127*$C$11+R127*$C$12+T127*$C$13+V127*$C$14+X127*$C$15+Z127*$C$16+AB127*$C$17+AD127*$C$18+AF127*$C$19+AH127*$C$20+AJ127*$C$21+AL127*$C$22+AN127*$C$23+AP12...` |
| `D128` | `=(H128*$C$7+J128*$C$8+L128*$C$9+N128*$C$10+P128*$C$11+R128*$C$12+T128*$C$13+V128*$C$14+X128*$C$15+Z128*$C$16+AB128*$C$17+AD128*$C$18+AF128*$C$19+AH128*$C$20+AJ128*$C$21+AL128*$C$22+AN128*$C$23+AP12...` |
| `D129` | `=(H129*$C$7+J129*$C$8+L129*$C$9+N129*$C$10+P129*$C$11+R129*$C$12+T129*$C$13+V129*$C$14+X129*$C$15+Z129*$C$16+AB129*$C$17+AD129*$C$18+AF129*$C$19+AH129*$C$20+AJ129*$C$21+AL129*$C$22+AN129*$C$23+AP12...` |
| `D130` | `=(H130*$C$7+J130*$C$8+L130*$C$9+N130*$C$10+P130*$C$11+R130*$C$12+T130*$C$13+V130*$C$14+X130*$C$15+Z130*$C$16+AB130*$C$17+AD130*$C$18+AF130*$C$19+AH130*$C$20+AJ130*$C$21+AL130*$C$22+AN130*$C$23+AP13...` |
| `D131` | `=(H131*$C$7+J131*$C$8+L131*$C$9+N131*$C$10+P131*$C$11+R131*$C$12+T131*$C$13+V131*$C$14+X131*$C$15+Z131*$C$16+AB131*$C$17+AD131*$C$18+AF131*$C$19+AH131*$C$20+AJ131*$C$21+AL131*$C$22+AN131*$C$23+AP13...` |
| `D132` | `=(H132*$C$7+J132*$C$8+L132*$C$9+N132*$C$10+P132*$C$11+R132*$C$12+T132*$C$13+V132*$C$14+X132*$C$15+Z132*$C$16+AB132*$C$17+AD132*$C$18+AF132*$C$19+AH132*$C$20+AJ132*$C$21+AL132*$C$22+AN132*$C$23+AP13...` |
| `D133` | `=(H133*$C$7+J133*$C$8+L133*$C$9+N133*$C$10+P133*$C$11+R133*$C$12+T133*$C$13+V133*$C$14+X133*$C$15+Z133*$C$16+AB133*$C$17+AD133*$C$18+AF133*$C$19+AH133*$C$20+AJ133*$C$21+AL133*$C$22+AN133*$C$23+AP13...` |
| `D134` | `=(H134*$C$7+J134*$C$8+L134*$C$9+N134*$C$10+P134*$C$11+R134*$C$12+T134*$C$13+V134*$C$14+X134*$C$15+Z134*$C$16+AB134*$C$17+AD134*$C$18+AF134*$C$19+AH134*$C$20+AJ134*$C$21+AL134*$C$22+AN134*$C$23+AP13...` |
| `D135` | `=(H135*$C$7+J135*$C$8+L135*$C$9+N135*$C$10+P135*$C$11+R135*$C$12+T135*$C$13+V135*$C$14+X135*$C$15+Z135*$C$16+AB135*$C$17+AD135*$C$18+AF135*$C$19+AH135*$C$20+AJ135*$C$21+AL135*$C$22+AN135*$C$23+AP13...` |
| `D136` | `=(H136*$C$7+J136*$C$8+L136*$C$9+N136*$C$10+P136*$C$11+R136*$C$12+T136*$C$13+V136*$C$14+X136*$C$15+Z136*$C$16+AB136*$C$17+AD136*$C$18+AF136*$C$19+AH136*$C$20+AJ136*$C$21+AL136*$C$22+AN136*$C$23+AP13...` |
| `D137` | `=(H137*$C$7+J137*$C$8+L137*$C$9+N137*$C$10+P137*$C$11+R137*$C$12+T137*$C$13+V137*$C$14+X137*$C$15+Z137*$C$16+AB137*$C$17+AD137*$C$18+AF137*$C$19+AH137*$C$20+AJ137*$C$21+AL137*$C$22+AN137*$C$23+AP13...` |
| `D138` | `=(H138*$C$7+J138*$C$8+L138*$C$9+N138*$C$10+P138*$C$11+R138*$C$12+T138*$C$13+V138*$C$14+X138*$C$15+Z138*$C$16+AB138*$C$17+AD138*$C$18+AF138*$C$19+AH138*$C$20+AJ138*$C$21+AL138*$C$22+AN138*$C$23+AP13...` |
| `D139` | `=(H139*$C$7+J139*$C$8+L139*$C$9+N139*$C$10+P139*$C$11+R139*$C$12+T139*$C$13+V139*$C$14+X139*$C$15+Z139*$C$16+AB139*$C$17+AD139*$C$18+AF139*$C$19+AH139*$C$20+AJ139*$C$21+AL139*$C$22+AN139*$C$23+AP13...` |
| `D140` | `=(H140*$C$7+J140*$C$8+L140*$C$9+N140*$C$10+P140*$C$11+R140*$C$12+T140*$C$13+V140*$C$14+X140*$C$15+Z140*$C$16+AB140*$C$17+AD140*$C$18+AF140*$C$19+AH140*$C$20+AJ140*$C$21+AL140*$C$22+AN140*$C$23+AP14...` |
| `D141` | `=(H141*$C$7+J141*$C$8+L141*$C$9+N141*$C$10+P141*$C$11+R141*$C$12+T141*$C$13+V141*$C$14+X141*$C$15+Z141*$C$16+AB141*$C$17+AD141*$C$18+AF141*$C$19+AH141*$C$20+AJ141*$C$21+AL141*$C$22+AN141*$C$23+AP14...` |
| `D142` | `=(H142*$C$7+J142*$C$8+L142*$C$9+N142*$C$10+P142*$C$11+R142*$C$12+T142*$C$13+V142*$C$14+X142*$C$15+Z142*$C$16+AB142*$C$17+AD142*$C$18+AF142*$C$19+AH142*$C$20+AJ142*$C$21+AL142*$C$22+AN142*$C$23+AP14...` |
| `D143` | `=(H143*$C$7+J143*$C$8+L143*$C$9+N143*$C$10+P143*$C$11+R143*$C$12+T143*$C$13+V143*$C$14+X143*$C$15+Z143*$C$16+AB143*$C$17+AD143*$C$18+AF143*$C$19+AH143*$C$20+AJ143*$C$21+AL143*$C$22+AN143*$C$23+AP14...` |
| `D144` | `=(H144*$C$7+J144*$C$8+L144*$C$9+N144*$C$10+P144*$C$11+R144*$C$12+T144*$C$13+V144*$C$14+X144*$C$15+Z144*$C$16+AB144*$C$17+AD144*$C$18+AF144*$C$19+AH144*$C$20+AJ144*$C$21+AL144*$C$22+AN144*$C$23+AP14...` |
| `D145` | `=(H145*$C$7+J145*$C$8+L145*$C$9+N145*$C$10+P145*$C$11+R145*$C$12+T145*$C$13+V145*$C$14+X145*$C$15+Z145*$C$16+AB145*$C$17+AD145*$C$18+AF145*$C$19+AH145*$C$20+AJ145*$C$21+AL145*$C$22+AN145*$C$23+AP14...` |
| `D146` | `=(H146*$C$7+J146*$C$8+L146*$C$9+N146*$C$10+P146*$C$11+R146*$C$12+T146*$C$13+V146*$C$14+X146*$C$15+Z146*$C$16+AB146*$C$17+AD146*$C$18+AF146*$C$19+AH146*$C$20+AJ146*$C$21+AL146*$C$22+AN146*$C$23+AP14...` |
| `D147` | `=(H147*$C$7+J147*$C$8+L147*$C$9+N147*$C$10+P147*$C$11+R147*$C$12+T147*$C$13+V147*$C$14+X147*$C$15+Z147*$C$16+AB147*$C$17+AD147*$C$18+AF147*$C$19+AH147*$C$20+AJ147*$C$21+AL147*$C$22+AN147*$C$23+AP14...` |
| `D148` | `=(H148*$C$7+J148*$C$8+L148*$C$9+N148*$C$10+P148*$C$11+R148*$C$12+T148*$C$13+V148*$C$14+X148*$C$15+Z148*$C$16+AB148*$C$17+AD148*$C$18+AF148*$C$19+AH148*$C$20+AJ148*$C$21+AL148*$C$22+AN148*$C$23+AP14...` |
| `D149` | `=(H149*$C$7+J149*$C$8+L149*$C$9+N149*$C$10+P149*$C$11+R149*$C$12+T149*$C$13+V149*$C$14+X149*$C$15+Z149*$C$16+AB149*$C$17+AD149*$C$18+AF149*$C$19+AH149*$C$20+AJ149*$C$21+AL149*$C$22+AN149*$C$23+AP14...` |
| `D150` | `=(H150*$C$7+J150*$C$8+L150*$C$9+N150*$C$10+P150*$C$11+R150*$C$12+T150*$C$13+V150*$C$14+X150*$C$15+Z150*$C$16+AB150*$C$17+AD150*$C$18+AF150*$C$19+AH150*$C$20+AJ150*$C$21+AL150*$C$22+AN150*$C$23+AP15...` |
| `D151` | `=(H151*$C$7+J151*$C$8+L151*$C$9+N151*$C$10+P151*$C$11+R151*$C$12+T151*$C$13+V151*$C$14+X151*$C$15+Z151*$C$16+AB151*$C$17+AD151*$C$18+AF151*$C$19+AH151*$C$20+AJ151*$C$21+AL151*$C$22+AN151*$C$23+AP15...` |
| `D152` | `=(H152*$C$7+J152*$C$8+L152*$C$9+N152*$C$10+P152*$C$11+R152*$C$12+T152*$C$13+V152*$C$14+X152*$C$15+Z152*$C$16+AB152*$C$17+AD152*$C$18+AF152*$C$19+AH152*$C$20+AJ152*$C$21+AL152*$C$22+AN152*$C$23+AP15...` |
| `D153` | `=(H153*$C$7+J153*$C$8+L153*$C$9+N153*$C$10+P153*$C$11+R153*$C$12+T153*$C$13+V153*$C$14+X153*$C$15+Z153*$C$16+AB153*$C$17+AD153*$C$18+AF153*$C$19+AH153*$C$20+AJ153*$C$21+AL153*$C$22+AN153*$C$23+AP15...` |
| `D154` | `=(H154*$C$7+J154*$C$8+L154*$C$9+N154*$C$10+P154*$C$11+R154*$C$12+T154*$C$13+V154*$C$14+X154*$C$15+Z154*$C$16+AB154*$C$17+AD154*$C$18+AF154*$C$19+AH154*$C$20+AJ154*$C$21+AL154*$C$22+AN154*$C$23+AP15...` |
| `D155` | `=(H155*$C$7+J155*$C$8+L155*$C$9+N155*$C$10+P155*$C$11+R155*$C$12+T155*$C$13+V155*$C$14+X155*$C$15+Z155*$C$16+AB155*$C$17+AD155*$C$18+AF155*$C$19+AH155*$C$20+AJ155*$C$21+AL155*$C$22+AN155*$C$23+AP15...` |
| `D156` | `=(H156*$C$7+J156*$C$8+L156*$C$9+N156*$C$10+P156*$C$11+R156*$C$12+T156*$C$13+V156*$C$14+X156*$C$15+Z156*$C$16+AB156*$C$17+AD156*$C$18+AF156*$C$19+AH156*$C$20+AJ156*$C$21+AL156*$C$22+AN156*$C$23+AP15...` |
| `D157` | `=(H157*$C$7+J157*$C$8+L157*$C$9+N157*$C$10+P157*$C$11+R157*$C$12+T157*$C$13+V157*$C$14+X157*$C$15+Z157*$C$16+AB157*$C$17+AD157*$C$18+AF157*$C$19+AH157*$C$20+AJ157*$C$21+AL157*$C$22+AN157*$C$23+AP15...` |
| `D158` | `=(H158*$C$7+J158*$C$8+L158*$C$9+N158*$C$10+P158*$C$11+R158*$C$12+T158*$C$13+V158*$C$14+X158*$C$15+Z158*$C$16+AB158*$C$17+AD158*$C$18+AF158*$C$19+AH158*$C$20+AJ158*$C$21+AL158*$C$22+AN158*$C$23+AP15...` |
| `D159` | `=(H159*$C$7+J159*$C$8+L159*$C$9+N159*$C$10+P159*$C$11+R159*$C$12+T159*$C$13+V159*$C$14+X159*$C$15+Z159*$C$16+AB159*$C$17+AD159*$C$18+AF159*$C$19+AH159*$C$20+AJ159*$C$21+AL159*$C$22+AN159*$C$23+AP15...` |
| `D160` | `=(H160*$C$7+J160*$C$8+L160*$C$9+N160*$C$10+P160*$C$11+R160*$C$12+T160*$C$13+V160*$C$14+X160*$C$15+Z160*$C$16+AB160*$C$17+AD160*$C$18+AF160*$C$19+AH160*$C$20+AJ160*$C$21+AL160*$C$22+AN160*$C$23+AP16...` |
| `D161` | `=(H161*$C$7+J161*$C$8+L161*$C$9+N161*$C$10+P161*$C$11+R161*$C$12+T161*$C$13+V161*$C$14+X161*$C$15+Z161*$C$16+AB161*$C$17+AD161*$C$18+AF161*$C$19+AH161*$C$20+AJ161*$C$21+AL161*$C$22+AN161*$C$23+AP16...` |
| `D162` | `=(H162*$C$7+J162*$C$8+L162*$C$9+N162*$C$10+P162*$C$11+R162*$C$12+T162*$C$13+V162*$C$14+X162*$C$15+Z162*$C$16+AB162*$C$17+AD162*$C$18+AF162*$C$19+AH162*$C$20+AJ162*$C$21+AL162*$C$22+AN162*$C$23+AP16...` |
| `D163` | `=(H163*$C$7+J163*$C$8+L163*$C$9+N163*$C$10+P163*$C$11+R163*$C$12+T163*$C$13+V163*$C$14+X163*$C$15+Z163*$C$16+AB163*$C$17+AD163*$C$18+AF163*$C$19+AH163*$C$20+AJ163*$C$21+AL163*$C$22+AN163*$C$23+AP16...` |
| `D164` | `=(H164*$C$7+J164*$C$8+L164*$C$9+N164*$C$10+P164*$C$11+R164*$C$12+T164*$C$13+V164*$C$14+X164*$C$15+Z164*$C$16+AB164*$C$17+AD164*$C$18+AF164*$C$19+AH164*$C$20+AJ164*$C$21+AL164*$C$22+AN164*$C$23+AP16...` |
| `D165` | `=(H165*$C$7+J165*$C$8+L165*$C$9+N165*$C$10+P165*$C$11+R165*$C$12+T165*$C$13+V165*$C$14+X165*$C$15+Z165*$C$16+AB165*$C$17+AD165*$C$18+AF165*$C$19+AH165*$C$20+AJ165*$C$21+AL165*$C$22+AN165*$C$23+AP16...` |
| `D166` | `=(H166*$C$7+J166*$C$8+L166*$C$9+N166*$C$10+P166*$C$11+R166*$C$12+T166*$C$13+V166*$C$14+X166*$C$15+Z166*$C$16+AB166*$C$17+AD166*$C$18+AF166*$C$19+AH166*$C$20+AJ166*$C$21+AL166*$C$22+AN166*$C$23+AP16...` |
| `D167` | `=(H167*$C$7+J167*$C$8+L167*$C$9+N167*$C$10+P167*$C$11+R167*$C$12+T167*$C$13+V167*$C$14+X167*$C$15+Z167*$C$16+AB167*$C$17+AD167*$C$18+AF167*$C$19+AH167*$C$20+AJ167*$C$21+AL167*$C$22+AN167*$C$23+AP16...` |
| `D168` | `=(H168*$C$7+J168*$C$8+L168*$C$9+N168*$C$10+P168*$C$11+R168*$C$12+T168*$C$13+V168*$C$14+X168*$C$15+Z168*$C$16+AB168*$C$17+AD168*$C$18+AF168*$C$19+AH168*$C$20+AJ168*$C$21+AL168*$C$22+AN168*$C$23+AP16...` |
| `D169` | `=(H169*$C$7+J169*$C$8+L169*$C$9+N169*$C$10+P169*$C$11+R169*$C$12+T169*$C$13+V169*$C$14+X169*$C$15+Z169*$C$16+AB169*$C$17+AD169*$C$18+AF169*$C$19+AH169*$C$20+AJ169*$C$21+AL169*$C$22+AN169*$C$23+AP16...` |
| `D170` | `=(H170*$C$7+J170*$C$8+L170*$C$9+N170*$C$10+P170*$C$11+R170*$C$12+T170*$C$13+V170*$C$14+X170*$C$15+Z170*$C$16+AB170*$C$17+AD170*$C$18+AF170*$C$19+AH170*$C$20+AJ170*$C$21+AL170*$C$22+AN170*$C$23+AP17...` |
| `D171` | `=(H171*$C$7+J171*$C$8+L171*$C$9+N171*$C$10+P171*$C$11+R171*$C$12+T171*$C$13+V171*$C$14+X171*$C$15+Z171*$C$16+AB171*$C$17+AD171*$C$18+AF171*$C$19+AH171*$C$20+AJ171*$C$21+AL171*$C$22+AN171*$C$23+AP17...` |
| `D172` | `=(H172*$C$7+J172*$C$8+L172*$C$9+N172*$C$10+P172*$C$11+R172*$C$12+T172*$C$13+V172*$C$14+X172*$C$15+Z172*$C$16+AB172*$C$17+AD172*$C$18+AF172*$C$19+AH172*$C$20+AJ172*$C$21+AL172*$C$22+AN172*$C$23+AP17...` |
| `D173` | `=(H173*$C$7+J173*$C$8+L173*$C$9+N173*$C$10+P173*$C$11+R173*$C$12+T173*$C$13+V173*$C$14+X173*$C$15+Z173*$C$16+AB173*$C$17+AD173*$C$18+AF173*$C$19+AH173*$C$20+AJ173*$C$21+AL173*$C$22+AN173*$C$23+AP17...` |
| `D174` | `=(H174*$C$7+J174*$C$8+L174*$C$9+N174*$C$10+P174*$C$11+R174*$C$12+T174*$C$13+V174*$C$14+X174*$C$15+Z174*$C$16+AB174*$C$17+AD174*$C$18+AF174*$C$19+AH174*$C$20+AJ174*$C$21+AL174*$C$22+AN174*$C$23+AP17...` |
| `D175` | `=(H175*$C$7+J175*$C$8+L175*$C$9+N175*$C$10+P175*$C$11+R175*$C$12+T175*$C$13+V175*$C$14+X175*$C$15+Z175*$C$16+AB175*$C$17+AD175*$C$18+AF175*$C$19+AH175*$C$20+AJ175*$C$21+AL175*$C$22+AN175*$C$23+AP17...` |
| `D176` | `=(H176*$C$7+J176*$C$8+L176*$C$9+N176*$C$10+P176*$C$11+R176*$C$12+T176*$C$13+V176*$C$14+X176*$C$15+Z176*$C$16+AB176*$C$17+AD176*$C$18+AF176*$C$19+AH176*$C$20+AJ176*$C$21+AL176*$C$22+AN176*$C$23+AP17...` |
| `D177` | `=(H177*$C$7+J177*$C$8+L177*$C$9+N177*$C$10+P177*$C$11+R177*$C$12+T177*$C$13+V177*$C$14+X177*$C$15+Z177*$C$16+AB177*$C$17+AD177*$C$18+AF177*$C$19+AH177*$C$20+AJ177*$C$21+AL177*$C$22+AN177*$C$23+AP17...` |
| `D178` | `=(H178*$C$7+J178*$C$8+L178*$C$9+N178*$C$10+P178*$C$11+R178*$C$12+T178*$C$13+V178*$C$14+X178*$C$15+Z178*$C$16+AB178*$C$17+AD178*$C$18+AF178*$C$19+AH178*$C$20+AJ178*$C$21+AL178*$C$22+AN178*$C$23+AP17...` |
| `D179` | `=(H179*$C$7+J179*$C$8+L179*$C$9+N179*$C$10+P179*$C$11+R179*$C$12+T179*$C$13+V179*$C$14+X179*$C$15+Z179*$C$16+AB179*$C$17+AD179*$C$18+AF179*$C$19+AH179*$C$20+AJ179*$C$21+AL179*$C$22+AN179*$C$23+AP17...` |
| `D180` | `=(H180*$C$7+J180*$C$8+L180*$C$9+N180*$C$10+P180*$C$11+R180*$C$12+T180*$C$13+V180*$C$14+X180*$C$15+Z180*$C$16+AB180*$C$17+AD180*$C$18+AF180*$C$19+AH180*$C$20+AJ180*$C$21+AL180*$C$22+AN180*$C$23+AP18...` |
| `D181` | `=(H181*$C$7+J181*$C$8+L181*$C$9+N181*$C$10+P181*$C$11+R181*$C$12+T181*$C$13+V181*$C$14+X181*$C$15+Z181*$C$16+AB181*$C$17+AD181*$C$18+AF181*$C$19+AH181*$C$20+AJ181*$C$21+AL181*$C$22+AN181*$C$23+AP18...` |
| `D182` | `=(H182*$C$7+J182*$C$8+L182*$C$9+N182*$C$10+P182*$C$11+R182*$C$12+T182*$C$13+V182*$C$14+X182*$C$15+Z182*$C$16+AB182*$C$17+AD182*$C$18+AF182*$C$19+AH182*$C$20+AJ182*$C$21+AL182*$C$22+AN182*$C$23+AP18...` |
| `D183` | `=(H183*$C$7+J183*$C$8+L183*$C$9+N183*$C$10+P183*$C$11+R183*$C$12+T183*$C$13+V183*$C$14+X183*$C$15+Z183*$C$16+AB183*$C$17+AD183*$C$18+AF183*$C$19+AH183*$C$20+AJ183*$C$21+AL183*$C$22+AN183*$C$23+AP18...` |
| `D184` | `=(H184*$C$7+J184*$C$8+L184*$C$9+N184*$C$10+P184*$C$11+R184*$C$12+T184*$C$13+V184*$C$14+X184*$C$15+Z184*$C$16+AB184*$C$17+AD184*$C$18+AF184*$C$19+AH184*$C$20+AJ184*$C$21+AL184*$C$22+AN184*$C$23+AP18...` |
| `D185` | `=(H185*$C$7+J185*$C$8+L185*$C$9+N185*$C$10+P185*$C$11+R185*$C$12+T185*$C$13+V185*$C$14+X185*$C$15+Z185*$C$16+AB185*$C$17+AD185*$C$18+AF185*$C$19+AH185*$C$20+AJ185*$C$21+AL185*$C$22+AN185*$C$23+AP18...` |
| `D186` | `=(H186*$C$7+J186*$C$8+L186*$C$9+N186*$C$10+P186*$C$11+R186*$C$12+T186*$C$13+V186*$C$14+X186*$C$15+Z186*$C$16+AB186*$C$17+AD186*$C$18+AF186*$C$19+AH186*$C$20+AJ186*$C$21+AL186*$C$22+AN186*$C$23+AP18...` |
| `D187` | `=(H187*$C$7+J187*$C$8+L187*$C$9+N187*$C$10+P187*$C$11+R187*$C$12+T187*$C$13+V187*$C$14+X187*$C$15+Z187*$C$16+AB187*$C$17+AD187*$C$18+AF187*$C$19+AH187*$C$20+AJ187*$C$21+AL187*$C$22+AN187*$C$23+AP18...` |
| `D188` | `=(H188*$C$7+J188*$C$8+L188*$C$9+N188*$C$10+P188*$C$11+R188*$C$12+T188*$C$13+V188*$C$14+X188*$C$15+Z188*$C$16+AB188*$C$17+AD188*$C$18+AF188*$C$19+AH188*$C$20+AJ188*$C$21+AL188*$C$22+AN188*$C$23+AP18...` |
| `D189` | `=(H189*$C$7+J189*$C$8+L189*$C$9+N189*$C$10+P189*$C$11+R189*$C$12+T189*$C$13+V189*$C$14+X189*$C$15+Z189*$C$16+AB189*$C$17+AD189*$C$18+AF189*$C$19+AH189*$C$20+AJ189*$C$21+AL189*$C$22+AN189*$C$23+AP18...` |
| `D190` | `=(H190*$C$7+J190*$C$8+L190*$C$9+N190*$C$10+P190*$C$11+R190*$C$12+T190*$C$13+V190*$C$14+X190*$C$15+Z190*$C$16+AB190*$C$17+AD190*$C$18+AF190*$C$19+AH190*$C$20+AJ190*$C$21+AL190*$C$22+AN190*$C$23+AP19...` |
| `D191` | `=(H191*$C$7+J191*$C$8+L191*$C$9+N191*$C$10+P191*$C$11+R191*$C$12+T191*$C$13+V191*$C$14+X191*$C$15+Z191*$C$16+AB191*$C$17+AD191*$C$18+AF191*$C$19+AH191*$C$20+AJ191*$C$21+AL191*$C$22+AN191*$C$23+AP19...` |
| `D192` | `=(H192*$C$7+J192*$C$8+L192*$C$9+N192*$C$10+P192*$C$11+R192*$C$12+T192*$C$13+V192*$C$14+X192*$C$15+Z192*$C$16+AB192*$C$17+AD192*$C$18+AF192*$C$19+AH192*$C$20+AJ192*$C$21+AL192*$C$22+AN192*$C$23+AP19...` |
| `D193` | `=(H193*$C$7+J193*$C$8+L193*$C$9+N193*$C$10+P193*$C$11+R193*$C$12+T193*$C$13+V193*$C$14+X193*$C$15+Z193*$C$16+AB193*$C$17+AD193*$C$18+AF193*$C$19+AH193*$C$20+AJ193*$C$21+AL193*$C$22+AN193*$C$23+AP19...` |
| `D194` | `=(H194*$C$7+J194*$C$8+L194*$C$9+N194*$C$10+P194*$C$11+R194*$C$12+T194*$C$13+V194*$C$14+X194*$C$15+Z194*$C$16+AB194*$C$17+AD194*$C$18+AF194*$C$19+AH194*$C$20+AJ194*$C$21+AL194*$C$22+AN194*$C$23+AP19...` |
| `D195` | `=(H195*$C$7+J195*$C$8+L195*$C$9+N195*$C$10+P195*$C$11+R195*$C$12+T195*$C$13+V195*$C$14+X195*$C$15+Z195*$C$16+AB195*$C$17+AD195*$C$18+AF195*$C$19+AH195*$C$20+AJ195*$C$21+AL195*$C$22+AN195*$C$23+AP19...` |
| `D196` | `=(H196*$C$7+J196*$C$8+L196*$C$9+N196*$C$10+P196*$C$11+R196*$C$12+T196*$C$13+V196*$C$14+X196*$C$15+Z196*$C$16+AB196*$C$17+AD196*$C$18+AF196*$C$19+AH196*$C$20+AJ196*$C$21+AL196*$C$22+AN196*$C$23+AP19...` |
| `D197` | `=(H197*$C$7+J197*$C$8+L197*$C$9+N197*$C$10+P197*$C$11+R197*$C$12+T197*$C$13+V197*$C$14+X197*$C$15+Z197*$C$16+AB197*$C$17+AD197*$C$18+AF197*$C$19+AH197*$C$20+AJ197*$C$21+AL197*$C$22+AN197*$C$23+AP19...` |
| `D198` | `=(H198*$C$7+J198*$C$8+L198*$C$9+N198*$C$10+P198*$C$11+R198*$C$12+T198*$C$13+V198*$C$14+X198*$C$15+Z198*$C$16+AB198*$C$17+AD198*$C$18+AF198*$C$19+AH198*$C$20+AJ198*$C$21+AL198*$C$22+AN198*$C$23+AP19...` |
| `D199` | `=(H199*$C$7+J199*$C$8+L199*$C$9+N199*$C$10+P199*$C$11+R199*$C$12+T199*$C$13+V199*$C$14+X199*$C$15+Z199*$C$16+AB199*$C$17+AD199*$C$18+AF199*$C$19+AH199*$C$20+AJ199*$C$21+AL199*$C$22+AN199*$C$23+AP19...` |
| `D200` | `=(H200*$C$7+J200*$C$8+L200*$C$9+N200*$C$10+P200*$C$11+R200*$C$12+T200*$C$13+V200*$C$14+X200*$C$15+Z200*$C$16+AB200*$C$17+AD200*$C$18+AF200*$C$19+AH200*$C$20+AJ200*$C$21+AL200*$C$22+AN200*$C$23+AP20...` |
| `D201` | `=(H201*$C$7+J201*$C$8+L201*$C$9+N201*$C$10+P201*$C$11+R201*$C$12+T201*$C$13+V201*$C$14+X201*$C$15+Z201*$C$16+AB201*$C$17+AD201*$C$18+AF201*$C$19+AH201*$C$20+AJ201*$C$21+AL201*$C$22+AN201*$C$23+AP20...` |
| `D202` | `=(H202*$C$7+J202*$C$8+L202*$C$9+N202*$C$10+P202*$C$11+R202*$C$12+T202*$C$13+V202*$C$14+X202*$C$15+Z202*$C$16+AB202*$C$17+AD202*$C$18+AF202*$C$19+AH202*$C$20+AJ202*$C$21+AL202*$C$22+AN202*$C$23+AP20...` |
| `D203` | `=(H203*$C$7+J203*$C$8+L203*$C$9+N203*$C$10+P203*$C$11+R203*$C$12+T203*$C$13+V203*$C$14+X203*$C$15+Z203*$C$16+AB203*$C$17+AD203*$C$18+AF203*$C$19+AH203*$C$20+AJ203*$C$21+AL203*$C$22+AN203*$C$23+AP20...` |
| `D204` | `=(H204*$C$7+J204*$C$8+L204*$C$9+N204*$C$10+P204*$C$11+R204*$C$12+T204*$C$13+V204*$C$14+X204*$C$15+Z204*$C$16+AB204*$C$17+AD204*$C$18+AF204*$C$19+AH204*$C$20+AJ204*$C$21+AL204*$C$22+AN204*$C$23+AP20...` |
| `D205` | `=(H205*$C$7+J205*$C$8+L205*$C$9+N205*$C$10+P205*$C$11+R205*$C$12+T205*$C$13+V205*$C$14+X205*$C$15+Z205*$C$16+AB205*$C$17+AD205*$C$18+AF205*$C$19+AH205*$C$20+AJ205*$C$21+AL205*$C$22+AN205*$C$23+AP20...` |
| `D206` | `=(H206*$C$7+J206*$C$8+L206*$C$9+N206*$C$10+P206*$C$11+R206*$C$12+T206*$C$13+V206*$C$14+X206*$C$15+Z206*$C$16+AB206*$C$17+AD206*$C$18+AF206*$C$19+AH206*$C$20+AJ206*$C$21+AL206*$C$22+AN206*$C$23+AP20...` |
| `D207` | `=(H207*$C$7+J207*$C$8+L207*$C$9+N207*$C$10+P207*$C$11+R207*$C$12+T207*$C$13+V207*$C$14+X207*$C$15+Z207*$C$16+AB207*$C$17+AD207*$C$18+AF207*$C$19+AH207*$C$20+AJ207*$C$21+AL207*$C$22+AN207*$C$23+AP20...` |
| `D208` | `=(H208*$C$7+J208*$C$8+L208*$C$9+N208*$C$10+P208*$C$11+R208*$C$12+T208*$C$13+V208*$C$14+X208*$C$15+Z208*$C$16+AB208*$C$17+AD208*$C$18+AF208*$C$19+AH208*$C$20+AJ208*$C$21+AL208*$C$22+AN208*$C$23+AP20...` |
| `D209` | `=(H209*$C$7+J209*$C$8+L209*$C$9+N209*$C$10+P209*$C$11+R209*$C$12+T209*$C$13+V209*$C$14+X209*$C$15+Z209*$C$16+AB209*$C$17+AD209*$C$18+AF209*$C$19+AH209*$C$20+AJ209*$C$21+AL209*$C$22+AN209*$C$23+AP20...` |
| `D210` | `=(H210*$C$7+J210*$C$8+L210*$C$9+N210*$C$10+P210*$C$11+R210*$C$12+T210*$C$13+V210*$C$14+X210*$C$15+Z210*$C$16+AB210*$C$17+AD210*$C$18+AF210*$C$19+AH210*$C$20+AJ210*$C$21+AL210*$C$22+AN210*$C$23+AP21...` |
| `D211` | `=(H211*$C$7+J211*$C$8+L211*$C$9+N211*$C$10+P211*$C$11+R211*$C$12+T211*$C$13+V211*$C$14+X211*$C$15+Z211*$C$16+AB211*$C$17+AD211*$C$18+AF211*$C$19+AH211*$C$20+AJ211*$C$21+AL211*$C$22+AN211*$C$23+AP21...` |
| `D212` | `=(H212*$C$7+J212*$C$8+L212*$C$9+N212*$C$10+P212*$C$11+R212*$C$12+T212*$C$13+V212*$C$14+X212*$C$15+Z212*$C$16+AB212*$C$17+AD212*$C$18+AF212*$C$19+AH212*$C$20+AJ212*$C$21+AL212*$C$22+AN212*$C$23+AP21...` |
| `D213` | `=(H213*$C$7+J213*$C$8+L213*$C$9+N213*$C$10+P213*$C$11+R213*$C$12+T213*$C$13+V213*$C$14+X213*$C$15+Z213*$C$16+AB213*$C$17+AD213*$C$18+AF213*$C$19+AH213*$C$20+AJ213*$C$21+AL213*$C$22+AN213*$C$23+AP21...` |
| `D214` | `=(H214*$C$7+J214*$C$8+L214*$C$9+N214*$C$10+P214*$C$11+R214*$C$12+T214*$C$13+V214*$C$14+X214*$C$15+Z214*$C$16+AB214*$C$17+AD214*$C$18+AF214*$C$19+AH214*$C$20+AJ214*$C$21+AL214*$C$22+AN214*$C$23+AP21...` |
| `D215` | `=(H215*$C$7+J215*$C$8+L215*$C$9+N215*$C$10+P215*$C$11+R215*$C$12+T215*$C$13+V215*$C$14+X215*$C$15+Z215*$C$16+AB215*$C$17+AD215*$C$18+AF215*$C$19+AH215*$C$20+AJ215*$C$21+AL215*$C$22+AN215*$C$23+AP21...` |
| `D216` | `=(H216*$C$7+J216*$C$8+L216*$C$9+N216*$C$10+P216*$C$11+R216*$C$12+T216*$C$13+V216*$C$14+X216*$C$15+Z216*$C$16+AB216*$C$17+AD216*$C$18+AF216*$C$19+AH216*$C$20+AJ216*$C$21+AL216*$C$22+AN216*$C$23+AP21...` |
| `D217` | `=(H217*$C$7+J217*$C$8+L217*$C$9+N217*$C$10+P217*$C$11+R217*$C$12+T217*$C$13+V217*$C$14+X217*$C$15+Z217*$C$16+AB217*$C$17+AD217*$C$18+AF217*$C$19+AH217*$C$20+AJ217*$C$21+AL217*$C$22+AN217*$C$23+AP21...` |
| `D218` | `=(H218*$C$7+J218*$C$8+L218*$C$9+N218*$C$10+P218*$C$11+R218*$C$12+T218*$C$13+V218*$C$14+X218*$C$15+Z218*$C$16+AB218*$C$17+AD218*$C$18+AF218*$C$19+AH218*$C$20+AJ218*$C$21+AL218*$C$22+AN218*$C$23+AP21...` |
| `D219` | `=(H219*$C$7+J219*$C$8+L219*$C$9+N219*$C$10+P219*$C$11+R219*$C$12+T219*$C$13+V219*$C$14+X219*$C$15+Z219*$C$16+AB219*$C$17+AD219*$C$18+AF219*$C$19+AH219*$C$20+AJ219*$C$21+AL219*$C$22+AN219*$C$23+AP21...` |
| `D220` | `=(H220*$C$7+J220*$C$8+L220*$C$9+N220*$C$10+P220*$C$11+R220*$C$12+T220*$C$13+V220*$C$14+X220*$C$15+Z220*$C$16+AB220*$C$17+AD220*$C$18+AF220*$C$19+AH220*$C$20+AJ220*$C$21+AL220*$C$22+AN220*$C$23+AP22...` |
| `D221` | `=(H221*$C$7+J221*$C$8+L221*$C$9+N221*$C$10+P221*$C$11+R221*$C$12+T221*$C$13+V221*$C$14+X221*$C$15+Z221*$C$16+AB221*$C$17+AD221*$C$18+AF221*$C$19+AH221*$C$20+AJ221*$C$21+AL221*$C$22+AN221*$C$23+AP22...` |
| `D222` | `=(H222*$C$7+J222*$C$8+L222*$C$9+N222*$C$10+P222*$C$11+R222*$C$12+T222*$C$13+V222*$C$14+X222*$C$15+Z222*$C$16+AB222*$C$17+AD222*$C$18+AF222*$C$19+AH222*$C$20+AJ222*$C$21+AL222*$C$22+AN222*$C$23+AP22...` |
| `D223` | `=(H223*$C$7+J223*$C$8+L223*$C$9+N223*$C$10+P223*$C$11+R223*$C$12+T223*$C$13+V223*$C$14+X223*$C$15+Z223*$C$16+AB223*$C$17+AD223*$C$18+AF223*$C$19+AH223*$C$20+AJ223*$C$21+AL223*$C$22+AN223*$C$23+AP22...` |
| `D224` | `=(H224*$C$7+J224*$C$8+L224*$C$9+N224*$C$10+P224*$C$11+R224*$C$12+T224*$C$13+V224*$C$14+X224*$C$15+Z224*$C$16+AB224*$C$17+AD224*$C$18+AF224*$C$19+AH224*$C$20+AJ224*$C$21+AL224*$C$22+AN224*$C$23+AP22...` |
| `D225` | `=(H225*$C$7+J225*$C$8+L225*$C$9+N225*$C$10+P225*$C$11+R225*$C$12+T225*$C$13+V225*$C$14+X225*$C$15+Z225*$C$16+AB225*$C$17+AD225*$C$18+AF225*$C$19+AH225*$C$20+AJ225*$C$21+AL225*$C$22+AN225*$C$23+AP22...` |
| `D226` | `=(H226*$C$7+J226*$C$8+L226*$C$9+N226*$C$10+P226*$C$11+R226*$C$12+T226*$C$13+V226*$C$14+X226*$C$15+Z226*$C$16+AB226*$C$17+AD226*$C$18+AF226*$C$19+AH226*$C$20+AJ226*$C$21+AL226*$C$22+AN226*$C$23+AP22...` |
| `D227` | `=(H227*$C$7+J227*$C$8+L227*$C$9+N227*$C$10+P227*$C$11+R227*$C$12+T227*$C$13+V227*$C$14+X227*$C$15+Z227*$C$16+AB227*$C$17+AD227*$C$18+AF227*$C$19+AH227*$C$20+AJ227*$C$21+AL227*$C$22+AN227*$C$23+AP22...` |
| `D228` | `=(H228*$C$7+J228*$C$8+L228*$C$9+N228*$C$10+P228*$C$11+R228*$C$12+T228*$C$13+V228*$C$14+X228*$C$15+Z228*$C$16+AB228*$C$17+AD228*$C$18+AF228*$C$19+AH228*$C$20+AJ228*$C$21+AL228*$C$22+AN228*$C$23+AP22...` |

... and 303 more formulas (truncated)

## Factor Metadata Sample

Source sheet: `3-Factor Data`

Headers: ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8', 'col_9', 'col_10', 'col_11', 'col_12', 'col_13', 'col_14']

Total rows: 292 (excluding header)

First 20 factors:

| col_1 | col_2 | col_3 | col_4 | col_5 | col_6 | col_7 | col_8 | col_9 | col_10 | col_11 | col_12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Factor Intelligence Li... |  |  |  |  |  |  |  |  |  |  |  |
| View universal factor ... |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |
| Category | Factor Name | Factor Code | Relationship | IC | IC T-stat | Top Quintile Return (%) | Top Quintile IR | Q1-Q5 Spread Return (%) | Spread IR | Coverage (%) | Autocorrelation (%) |
| Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter |
| efficiency | Equity Turnover | equity_turn | Positive | 1.37521935778231 | 4.25170163083262 | 1.92115311826781 | 0.482617897348461 | 2.77941208067995 | 0.412785509962611 | 97.3561150126597 | 0.9886501543931481 |
| size | Book Value | bv | Inverse | 1.89339286807129 | 4.69039938853598 | 4.88241242968992 | 1.05565279769077 | 7.80311452584383 | 1.03655210845247 | 99.1208861940505 | 0.991878640544131 |
| technical | On-Balance Volume (252D) | obv_252d | Positive | 1.90055885729556 | 3.15891474215683 | 3.08990485270934 | 0.531265284760733 | 4.47505669138757 | 0.375751022248153 | 99.9984798513716 | 0.889912065722666 |
| size | Midcap | midcap | Inverse | 1.4028351989317 | 2.45433238898501 | 4.65256215074325 | 0.664012077674092 | 7.63072597281469 | 0.67666721623283 | 100 | 0.994198267671694 |
| short | Days to Cover | days_to_cover | Inverse | 1.75111125670913 | 5.52855617780306 | 1.49536943131652 | 0.431788979296344 | 3.31099550999251 | 0.588924156308917 | 72.3991104182622 | 0.773713896304915 |
| crowding | Passive Percentage Out... | passive_pctout | Inverse | 2.56960270499106 | 6.13719456425249 | 2.911511645942 | 0.789761246123792 | 7.5037442756398 | 1.07035810150214 | 16.9773865716076 | 0.989905356398842 |
| crowding | Hedge Fund Percentage ... | hf_pcprt | Positive | 2.81953086361645 | 5.19530178876076 | 3.35649498161615 | 0.642865788034959 | 6.45699844669216 | 0.667472220035522 | 16.9741080956005 | 0.9678108866681719 |
| momentum | Return Momentum (252D) | ret_mom_252d | Positive | 1.91382890581844 | 2.30260946195158 | 2.71078407028806 | 0.363479677027832 | 3.48861162889146 | 0.21083365617963 | 99.237482475989 | 0.885121644089437 |
| size | Assets | assets | Inverse | 1.4507225015952 | 3.12001152152347 | 3.67473827142265 | 0.756356753045383 | 6.52444826510831 | 0.824747024775652 | 99.3653336178145 | 0.9946631496287109 |
| efficiency | Asset Turnover | asset_turn | Positive | 1.35744886164547 | 3.64004591600206 | 1.62196716975107 | 0.438898117061167 | 2.76818155431744 | 0.458515354454842 | 99.0396567435576 | 0.9909652351849719 |
| value | Free Cash Flow to Ente... | fcf_ev | Positive | 1.17381073881098 | 2.73446357502335 | 2.08302508469067 | 0.484769858941515 | 2.7534882435871 | 0.362024536084877 | 89.9770369611535 | 0.92715974392477 |
| management | CAPEX to Depreciation | capex_depr | Inverse | 0.899988501973998 | 2.94753836080475 | 0.846640700048699 | 0.257577712903933 | 0.896065558219938 | 0.15148637230969 | 94.0652814744603 | 0.968640939156991 |
| profitability | Cash Flow Return on In... | cfroic | Positive | 1.41943971800185 | 3.41461844605571 | 1.32799395317609 | 0.344314111560683 | 2.18053075017633 | 0.260997170621121 | 98.3197273825373 | 0.9640618544699019 |
| short | Short Interest / Share... | short_pct_chg_12m | Inverse | 1.18256526083126 | 3.84484116797243 | 1.54383760101692 | 0.444327545203067 | 3.80309225196508 | 0.701081198230951 | 69.2252136691015 | 0.771929702412614 |
| profitability | Cash Flow Return on Eq... | cfroe | Positive | 1.27798249868379 | 3.68904030708186 | 0.853945206618869 | 0.264464000943632 | 1.56959311122992 | 0.223499287661771 | 96.2932518079149 | 0.957706294237733 |

## VBA Source Code

### Module: `Sheet1.cls`

- **Stream:** `VBA/Sheet1`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet1"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
'========================================
' Tab 1 (1-Configuration) - COMBINED VBA
'========================================
' HIERARCHICAL ORGANIZATION (Bottom to Top - Operational Order):
'
' USER-FACING MACROS (ordered by execution sequence):
'   1. Tab1_01_ClearFormattingAroundFactorBank      - Lowest level: Clear protected rows
'   2. Tab1_02_ApplyAlternatingRowsToFactorBank     - Base layer: Alternating rows (A-F)
'   3. Tab1_03_ApplyAlternatingRowsToSelectedFactors - Base layer: Alternating rows (A-F)
'   4. Tab1_04_ReapplyYellowHighlighting            - Top layer: Yellow highlighting (B-E)
'   5. Tab1_05_ApplySystematicFactorsFormatting     - Top layer: Red "No" formatting (F)
'   6. Tab1_06_RefreshAllTab1Formatting             - Master: Calls all in correct order
'
' FORMATTING LAYERS:
'   Columns A-F: Alternating rows (base) + Yellow (B-E) + Systematic Factors formatting (F) on top
'   Column F: "Yes" (default) or "No" (red background + dark red text)
'   Columns G-J: Conditional formatting ONLY (no direct fills)
'
' AUTOMATIC EVENT HANDLERS (run automatically):
'   - Worksheet_Change                  - Handles YES/NO factor selection
'   - Worksheet_Activate                - Runs when sheet activated
'
' INTERNAL SUBROUTINES (called by events):
'   - HandleFactorSelection             - Process factor selection
'   - MoveFromBankToSelected            - Move factor to Selected
'   - MoveFromSelectedToBank            - Move factor to Bank
'
'========================================

Option Explicit

'========================================
' PART 1: USER-FACING MACROS (Operational Order: Bottom to Top)
'========================================

Sub Tab1_01_ClearFormattingAroundFactorBank()
    '=====================================================================
    ' STEP 1 (Lowest Level): Clear conditional formatting from protected rows
    ' Protected: 2 rows above FACTOR BANK (blank) and 1 row below (header)
    '=====================================================================

    On Error Resume Next

    Dim ws As Worksheet
    Set ws = Me

    Dim factorBankRow As Long
    factorBankRow = 0

    ' Find "FACTOR BANK" in Column A
    Dim r As Long
    For r = 1 To 100
        Dim cellText As String
        cellText = Trim(UCase(CStr(ws.Cells(r, 1).Value)))

        If InStr(cellText, "FACTOR BANK") > 0 Then
            factorBankRow = r
            Exit For
        End If
    Next r

    ' If not found, exit
    If factorBankRow = 0 Then Exit Sub

    ' Clear conditional formatting from:
    ' - 2 rows above FACTOR BANK (blank rows)
    ' - 1 row below FACTOR BANK (header row)
    Dim protectedRows As Variant
    protectedRows = Array(factorBankRow - 2, factorBankRow - 1, factorBankRow + 1)

    Dim protRow As Variant
    For Each protRow In protectedRows
        If protRow > 0 And protRow <= ws.Rows.Count Then
            ' Clear conditional formatting from columns G, H, I, J
            ws.Range("G" & protRow & ":J" & protRow).FormatConditions.Delete
        End If
    Next protRow

End Sub

Sub Tab1_02_ApplyAlternatingRowsToFactorBank()
    '=====================================================================
    ' STEP 2 (Base Layer): Alternating white/gray rows for Factor Bank (columns A-F)
    ' Column F will have conditional formatting (green for "Yes") applied on top
    ' Columns G-J have conditional formatting (quintiles, relationship colors)
    ' PRESERVES yellow highlighting on columns B-E for highest IC factors
    '=====================================================================
    Dim ws As Worksheet
    Dim bankStart As Long
    Dim bankEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim isYellowRow As Boolean

    ' Reference to this worksheet
    Set ws = Me

    ' Find Factor Bank start
    bankStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "FACTOR BANK") > 0 Then
            bankStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    If bankStart = 0 Then
        MsgBox "Could not find FACTOR BANK section", vbCritical
        Exit Sub
    End If

    ' Find Factor Bank end (first empty row in column E)
    bankEnd = bankStart
    For i = bankStart To 500
        If ws.Cells(i, 5).Value = "" Then
            bankEnd = i - 1
            Exit For
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)
    Const COLOR_YELLOW As Long = 65535          ' RGB(255, 255, 0)
    Const COLOR_GREEN As Long = 13434828        ' RGB(200, 230, 201) - Light green for "Yes"

    ' Apply alternating rows to columns A-F
    For rowIdx = 0 To (bankEnd - bankStart)
        i = bankStart + rowIdx

        ' Check if this row has yellow highlighting (check column B)
        isYellowRow = (ws.Cells(i, 2).Interior.Color = COLOR_YELLOW)

        ' Check if column F has green highlighting (for "Yes")
        Dim isGreenActive As Boolean
        isGreenActive = (ws.Cells(i, 6).Interior.Color = COLOR_GREEN)

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Apply to columns A-F
        For col = 1 To 6
            Set cell = ws.Cells(i, col)

            ' Preserve yellow highlighting for columns B-E
            If isYellowRow And (col >= 2 And col <= 5) Then
                cell.Interior.Color = COLOR_YELLOW
            ' Preserve green highlighting for column F
            ElseIf isGreenActive And col = 6 Then
                cell.Interior.Color = COLOR_GREEN
            Else
                ' Apply alternating color
                cell.Interior.Color = rowColor
            End If
        Next col

        ' DO NOT touch columns G-J (7-10) - they have conditional formatting (quintiles, relationship)
    Next rowIdx

End Sub

Sub Tab1_03_ApplyAlternatingRowsToSelectedFactors()
    '=====================================================================
    ' STEP 3 (Base Layer): Alternating white/gray rows for Selected Factors (columns A-F)
    ' Column F will have conditional formatting (green for "Yes") applied on top
    ' Columns G-J have conditional formatting (quintiles, relationship colors)
    ' PRESERVES yellow highlighting on columns B-E for highest IC factors
    '=====================================================================
    Dim ws As Worksheet
    Dim selectedStart As Long
    Dim selectedEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim isYellowRow As Boolean

    ' Reference to this worksheet
    Set ws = Me

    ' Find Selected Factors start
    selectedStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "SELECTED FACTORS") > 0 Then
            selectedStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    If selectedStart = 0 Then Exit Sub

    ' Find Selected Factors end (first empty row in column E)
    selectedEnd = selectedStart
    For i = selectedStart To 500
        If ws.Cells(i, 5).Value = "" Then
            selectedEnd = i - 1
            Exit For
        End If
    Next i

    ' If no data, exit
    If selectedEnd < selectedStart Then Exit Sub

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)
    Const COLOR_YELLOW As Long = 65535          ' RGB(255, 255, 0)
    Const COLOR_GREEN As Long = 13434828        ' RGB(200, 230, 201) - Light green for "Yes"

    ' Apply alternating rows to columns A-F
    For rowIdx = 0 To (selectedEnd - selectedStart)
        i = selectedStart + rowIdx

        ' Check if this row has yellow highlighting (check column B)
        isYellowRow = (ws.Cells(i, 2).Interior.Color = COLOR_YELLOW)

        ' Check if column F has green highlighting (for "Yes")
        Dim isGreenActive As Boolean
        isGreenActive = (ws.Cells(i, 6).Interior.Color = COLOR_GREEN)

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Apply to columns A-F
        ' Column F will have conditional formatting (green for "Yes") applied on top
        For col = 1 To 6
            Set cell = ws.Cells(i, col)

            ' Preserve yellow highlighting for columns B-E
            If isYellowRow And (col >= 2 And col <= 5) Then
                cell.Interior.Color = COLOR_YELLOW
            ' Preserve green highlighting for column F
            ElseIf isGreenActive And col = 6 Then
                cell.Interior.Color = COLOR_GREEN
            Else
                ' Apply alternating color
                cell.Interior.Color = rowColor
            End If
        Next col

        ' DO NOT touch columns G-J (7-10)
        ' Column G: Coverage (conditional: percentile-based quintile colors)
        ' Column H: Relationship (conditional: green for "Positive", red for "Inverse")
        ' Column I: IC (conditional: percentile-based quintile colors)
        ' Column J: Autocorrelation (conditional: percentile-based quintile colors)
        '
        ' Applying direct cell fills to these columns would HIDE the conditional formatting
        ' By leaving them untouched, Excel displays conditional formatting on top of no fill
    Next rowIdx

End Sub

Sub Tab1_04_ReapplyYellowHighlighting()
    '=====================================================================
    ' STEP 4 (Top Layer): Apply yellow highlighting to highest IC factors
    ' Searches BOTH Selected Factors AND Factor Bank sections
    ' Yellow highlighting follows the factor regardless of which section it's in
    ' MUST run AFTER alternating rows to sit on top of base formatting
    '=====================================================================
    Dim ws As Worksheet
    Dim selectedStart As Long, selectedEnd As Long
    Dim bankStart As Long, bankEnd As Long
    Dim i As Long
    Dim categories As Object
    Dim category As String
    Dim factorCode As String
    Dim icValue As Variant
    Dim bestIC As Double
    Dim bestRow As Long

    Set ws = Me
    Set categories = CreateObject("Scripting.Dictionary")

    ' Find Selected Factors start
    selectedStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "SELECTED FACTORS") > 0 Then
            selectedStart = i + 2
            Exit For
        End If
    Next i

    ' Find Factor Bank start
    bankStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "FACTOR BANK") > 0 Then
            bankStart = i + 2
            Exit For
        End If
    Next i

    If bankStart = 0 Then Exit Sub

    ' Find Selected Factors end (if exists)
    If selectedStart > 0 Then
        selectedEnd = selectedStart
        For i = selectedStart To bankStart - 3
            If ws.Cells(i, 5).Value = "" Then
                selectedEnd = i - 1
                Exit For
            End If
        Next i
        If selectedEnd < selectedStart Then selectedEnd = selectedStart - 1
    Else
        selectedEnd = 0
    End If

    ' Find Factor Bank end
    bankEnd = bankStart
    For i = bankStart To 500
        If ws.Cells(i, 5).Value = "" Then
            bankEnd = i - 1
            Exit For
        End If
    Next i

    ' Find highest IC in each category across BOTH sections
    ' First check Selected Factors
    If selectedStart > 0 And selectedEnd >= selectedStart Then
        For i = selectedStart To selectedEnd
            category = Trim(CStr(ws.Cells(i, 2).Value))
            factorCode = Trim(CStr(ws.Cells(i, 5).Value))

            If category = "" Or factorCode = "" Then GoTo NextSelectedFactor

            ' Get IC value from column I (9)
            icValue = ws.Cells(i, 9).Value

            If IsNumeric(icValue) Then
                If Not categories.Exists(category) Then
                    categories.Add category, Array(i, CDbl(icValue))
                Else
                    If CDbl(icValue) > categories(category)(1) Then
                        categories(category) = Array(i, CDbl(icValue))
                    End If
                End If
            End If

NextSelectedFactor:
        Next i
    End If

    ' Then check Factor Bank
    For i = bankStart To bankEnd
        category = Trim(CStr(ws.Cells(i, 2).Value))
        factorCode = Trim(CStr(ws.Cells(i, 5).Value))

        If category = "" Or factorCode = "" Then GoTo NextBankFactor

        ' Get IC value from column I (9)
        icValue = ws.Cells(i, 9).Value

        If IsNumeric(icValue) Then
            If Not categories.Exists(category) Then
                categories.Add category, Array(i, CDbl(icValue))
            Else
                If CDbl(icValue) > categories(category)(1) Then
                    categories(category) = Array(i, CDbl(icValue))
                End If
            End If
        End If

NextBankFactor:
    Next i

    ' Clear all yellow highlighting from BOTH sections
    Const COLOR_WHITE As Long = 16777215
    Const COLOR_LIGHT_GRAY As Long = 15921906

    ' Clear Selected Factors
    If selectedStart > 0 And selectedEnd >= selectedStart Then
        For i = selectedStart To selectedEnd
            Dim selectedIdx As Long
            selectedIdx = i - selectedStart

            Dim selectedColor As Long
            If selectedIdx Mod 2 = 0 Then
                selectedColor = COLOR_WHITE
            Else
                selectedColor = COLOR_LIGHT_GRAY
            End If

            ws.Cells(i, 2).Interior.Color = selectedColor
            ws.Cells(i, 3).Interior.Color = selectedColor
            ws.Cells(i, 4).Interior.Color = selectedColor
            ws.Cells(i, 5).Interior.Color = selectedColor
        Next i
    End If

    ' Clear Factor Bank
    For i = bankStart To bankEnd
        Dim bankIdx As Long
        bankIdx = i - bankStart

        Dim bankColor As Long
        If bankIdx Mod 2 = 0 Then
            bankColor = COLOR_WHITE
        Else
            bankColor = COLOR_LIGHT_GRAY
        End If

        ws.Cells(i, 2).Interior.Color = bankColor
        ws.Cells(i, 3).Interior.Color = bankColor
        ws.Cells(i, 4).Interior.Color = bankColor
        ws.Cells(i, 5).Interior.Color = bankColor
    Next i

    ' Apply yellow highlighting to highest IC factors (in either section)
    Const COLOR_YELLOW As Long = 65535

    Dim key As Variant
    For Each key In categories.Keys
        bestRow = categories(key)(0)

        ' Apply yellow to columns B-E
        ws.Cells(bestRow, 2).Interior.Color = COLOR_YELLOW
        ws.Cells(bestRow, 3).Interior.Color = COLOR_YELLOW
        ws.Cells(bestRow, 4).Interior.Color = COLOR_YELLOW
        ws.Cells(bestRow, 5).Interior.Color = COLOR_YELLOW
    Next key

End Sub

Sub Tab1_05_ApplySystematicFactorsFormatting()
    '=====================================================================
    ' STEP 5: Apply "Systematic Factors" column formatting (Column F)
    ' - Applies red background + dark red text (regular weight) to "No" values
    ' - Matches "Inverse" formatting style from column H (Relationship)
    ' Excel default red: Background #FFC7CE, Text #9C0006, Regular (not bold)
    '=====================================================================
    Dim ws As Worksheet
    Dim selectedStart As Long, selectedEnd As Long
    Dim bankStart As Long, bankEnd As Long
    Dim i As Long

    Set ws = Me

    ' Define Excel's default red conditional formatting colors (matches "Inverse" in column H)
    Const COLOR_RED_BG As Long = 13551615      ' RGB(255, 199, 206) = #FFC7CE
    Const COLOR_RED_TEXT As Long = 393372     ' RGB(156, 0, 6) = #9C0006
    Const COLOR_BLACK_TEXT As Long = 0         ' RGB(0, 0, 0) = Black

    ' Find Selected Factors start
    selectedStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "SELECTED FACTORS") > 0 Then
            selectedStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    ' Find Factor Bank start
    bankStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "FACTOR BANK") > 0 Then
            bankStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    If bankStart = 0 Then Exit Sub

    ' Find Selected Factors end (if exists)
    If selectedStart > 0 Then
        selectedEnd = selectedStart
        For i = selectedStart To bankStart - 3
            If ws.Cells(i, 5).Value = "" Then
                selectedEnd = i - 1
                Exit For
            End If
        Next i
        If selectedEnd < selectedStart Then selectedEnd = 0
    Else
        selectedEnd = 0
    End If

    ' Find Factor Bank end
    bankEnd = bankStart
    For i = bankStart To 500
        If ws.Cells(i, 5).Value = "" Then
            bankEnd = i - 1
            Exit For
        End If
    Next i

    ' Apply formatting to Selected Factors section
    If selectedStart > 0 And selectedEnd >= selectedStart Then
        For i = selectedStart To selectedEnd
            Dim cellValue As String
            cellValue = Trim(UCase(CStr(ws.Cells(i, 6).Value)))

            ' Apply formatting based on value (do not modify cell values)
            If cellValue = "NO" Then
                ws.Cells(i, 6).Interior.Color = COLOR_RED_BG
                ws.Cells(i, 6).Font.Color = COLOR_RED_TEXT
                ws.Cells(i, 6).Font.Bold = False  ' Regular weight, not bold
            ElseIf cellValue = "YES" Then
                ' Reset to default (alternating row color will be applied by other functions)
                ws.Cells(i, 6).Font.Color = COLOR_BLACK_TEXT
                ws.Cells(i, 6).Font.Bold = False
            End If
        Next i
    End If

    ' Apply formatting to Factor Bank section
    For i = bankStart To bankEnd
        cellValue = Trim(UCase(CStr(ws.Cells(i, 6).Value)))

        ' Apply formatting based on value (do not modify cell values)
        If cellValue = "NO" Then
            ws.Cells(i, 6).Interior.Color = COLOR_RED_BG
            ws.Cells(i, 6).Font.Color = COLOR_RED_TEXT
            ws.Cells(i, 6).Font.Bold = False  ' Regular weight, not bold
        ElseIf cellValue = "YES" Then
            ' Reset to default (alternating row color will be applied by other functions)
            ws.Cells(i, 6).Font.Color = COLOR_BLACK_TEXT
            ws.Cells(i, 6).Font.Bold = False
        End If
    Next i

End Sub

Sub Tab1_06_RefreshAllFormatting()
    '=====================================================================
    ' STEP 6 (Master Function): Refresh ALL Tab 1 formatting in correct order
    ' Call this after any sorting operation or data changes
    ' Executes all formatting steps in proper sequence
    '=====================================================================
    Call Tab1_01_ClearFormattingAroundFactorBank
    Call Tab1_02_ApplyAlternatingRowsToFactorBank
    Call Tab1_03_ApplyAlternatingRowsToSelectedFactors
    Call Tab1_04_ReapplyYellowHighlighting
    Call Tab1_05_ApplySystematicFactorsFormatting
End Sub

'========================================
' PART 2: AUTOMATIC EVENT HANDLERS
'========================================

Private Sub Worksheet_Change(ByVal Target As Range)
    On Error GoTo ErrorHandler

    ' Handle Column A changes (YES/NO factor selection)
    If Target.Column = 1 And Target.Cells.Count = 1 Then
        Call HandleFactorSelection(Target)
    End If

    ' Handle Column G-J changes (clear formatting around FACTOR BANK)
    If Target.Column >= 7 And Target.Column <= 10 Then
        Call Tab1_01_ClearFormattingAroundFactorBank
    End If

    Exit Sub

ErrorHandler:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
End Sub

Private Sub Worksheet_Activate()
    '=====================================================================
    ' Run when sheet is activated (clear formatting around FACTOR BANK)
    '=====================================================================
    On Error Resume Next
    Call Tab1_01_ClearFormattingAroundFactorBank
End Sub

'========================================
' PART 3: INTERNAL SUBROUTINES (Called by Events)
'========================================

Private Sub HandleFactorSelection(Target As Range)
    '=====================================================================
    ' Handle YES/NO changes in Column A
    '=====================================================================
    On Error GoTo ErrorHandler

    Application.EnableEvents = False
    Application.ScreenUpdating = False

    Dim changedRow As Long
    changedRow = Target.Row

    Dim factorCode As String
    factorCode = Trim(CStr(Me.Cells(changedRow, 5).Value))

    If factorCode = "" Or factorCode = "Code" Then GoTo Cleanup

    Dim newValue As String
    newValue = UCase(Trim(CStr(Target.Value)))

    Dim selectedStart As Long, bankStart As Long

    ' Find sections dynamically
    Dim r As Long
    selectedStart = 0
    bankStart = 0

    For r = 1 To 50
        On Error Resume Next
        Dim cellText As String
        cellText = ""
        cellText = CStr(Me.Cells(r, 1).Value)
        cellText = UCase(Trim(cellText))
        On Error GoTo ErrorHandler

        ' Exact match for "SELECTED FACTORS"
        If cellText = "SELECTED FACTORS" Then
            selectedStart = r + 2  ' Data starts 2 rows after header
        End If

        ' Exact match for "FACTOR BANK"
        If cellText = "FACTOR BANK" Then
            bankStart = r + 2
            Exit For
        End If
    Next r

    ' Validation
    If selectedStart = 0 Or bankStart = 0 Then
        MsgBox "Cannot find sections. Selected at row " & (selectedStart - 2) & ", Bank at row " & (bankStart - 2), vbCritical
        GoTo Cleanup
    End If

    If changedRow >= bankStart Then
        If newValue = "YES" Then
            Call MoveFromBankToSelected(Me, changedRow, selectedStart, bankStart)
        End If
    ElseIf changedRow >= selectedStart And changedRow < (bankStart - 2) Then
        If newValue = "NO" Then
            Call MoveFromSelectedToBank(Me, changedRow, selectedStart, bankStart)
        End If
    End If

Cleanup:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    Exit Sub

ErrorHandler:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    MsgBox "Error " & Err.Number & ": " & Err.Description & vbCrLf & "Row: " & changedRow, vbCritical
End Sub

Private Sub MoveFromBankToSelected(ws As Worksheet, sourceRow As Long, selectedStart As Long, bankStart As Long)
    Dim factorGroup As String
    Dim factorPPS As Double

    factorGroup = Trim(CStr(ws.Cells(sourceRow, 2).Value))
    factorPPS = Val(ws.Cells(sourceRow, 7).Value)

    Dim insertRow As Long
    insertRow = selectedStart

    Dim r As Long
    Dim selectedEnd As Long
    selectedEnd = bankStart - 3  ' End of Selected Factors is 3 rows before Factor Bank header

    Dim foundGroup As Boolean
    foundGroup = False

    For r = selectedStart To selectedEnd
        Dim checkCode As String
        checkCode = Trim(CStr(ws.Cells(r, 5).Value))

        If checkCode = "" Then
            insertRow = r
            Exit For
        End If

        Dim checkGroup As String
        checkGroup = Trim(CStr(ws.Cells(r, 2).Value))

        ' First: Find matching group
        If checkGroup = factorGroup Then
            foundGroup = True

            ' Second: Within group, sort by PPS (coverage) descending
            Dim checkPPS As Double
            checkPPS = Val(ws.Cells(r, 7).Value)

            If factorPPS > checkPPS Then
                insertRow = r
                Exit For
            End If

            insertRow = r + 1

        ' If we found the group but now see a different group, insert here (end of our group)
        ElseIf foundGroup = True Then
            insertRow = r
            Exit For
        End If
    Next r

    ws.Rows(sourceRow).Cut
    ws.Rows(insertRow).Insert Shift:=xlDown
    ws.Cells(insertRow, 1).Value = "YES"

    ' Refresh all formatting after move (uses master function)
    Call Tab1_06_RefreshAllFormatting
End Sub

Private Sub MoveFromSelectedToBank(ws As Worksheet, sourceRow As Long, selectedStart As Long, bankStart As Long)
    Dim factorGroup As String
    Dim factorPPS As Double

    factorGroup = Trim(CStr(ws.Cells(sourceRow, 2).Value))
    factorPPS = Val(ws.Cells(sourceRow, 7).Value)

    Dim insertRow As Long
    insertRow = bankStart

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, 5).End(xlUp).Row

    Dim foundGroup As Boolean
    foundGroup = False

    Dim r As Long
    For r = bankStart To lastRow
        Dim checkCode As String
        checkCode = Trim(CStr(ws.Cells(r, 5).Value))

        If checkCode = "" Or checkCode = "Code" Then GoTo NextRow

        Dim checkGroup As String
        checkGroup = Trim(CStr(ws.Cells(r, 2).Value))

        If checkGroup = factorGroup Then
            foundGroup = True

            Dim checkPPS As Double
            checkPPS = Val(ws.Cells(r, 7).Value)

            If factorPPS > checkPPS Then
                insertRow = r
                Exit For
            End If

            insertRow = r + 1

        ElseIf foundGroup = True Then
            insertRow = r
            Exit For
        End If

NextRow:
    Next r

    ws.Rows(sourceRow).Cut
    ws.Rows(insertRow).Insert Shift:=xlDown
    ws.Cells(insertRow, 1).Value = "NO"

    ' Refresh all formatting after move (uses master function)
    Call Tab1_06_RefreshAllFormatting
End Sub


```

### Module: `ThisWorkbook.cls`

- **Stream:** `VBA/ThisWorkbook`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "ThisWorkbook"
Attribute VB_Base = "0{00020819-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Private Sub Workbook_Open()
    '=====================================================================
    ' Auto-Sort on File Open + Factor Status Cleanup
    '=====================================================================
    ' INSTALLATION: Copy this code into ThisWorkbook code window
    '
    ' WHAT IT DOES:
    ' - Cleans up Tab 1 factor status (Factor Bank = all NO, Selected Factors = all YES)
    ' - Sorts Tab 4 by composite score (descending)
    ' - Updates rank numbers (1, 2, 3...)
    '
    ' Version: 3.4
    ' Date: October 31, 2025
    ' Update: Added absolute path fallback for logo loading
    '=====================================================================

    On Error Resume Next

    Application.ScreenUpdating = False

    ' =====================================================================
    ' PART 0: Re-insert Logo to Tab 1 (Centered in merged A2:J2)
    ' =====================================================================
    Dim ws1 As Worksheet
    Set ws1 = Nothing

    ' Find Tab 1 ("1-Configuration")
    For Each ws1 In ThisWorkbook.Worksheets
        If InStr(ws1.Name, "Configuration") > 0 Or ws1.Name = "1-Configuration" Then
            Exit For
        End If
    Next ws1

    If Not ws1 Is Nothing Then
        ' Remove any existing pictures in Tab 1 to avoid duplicates
        Dim pic As Picture
        For Each pic In ws1.Pictures
            pic.Delete
        Next pic

        ' Insert logo - Relative path (portable across folders)
        Dim logoPath As String
        logoPath = ThisWorkbook.Path & "\scripts\dev_tools\logo.png"

        If Dir(logoPath) <> "" Then
            ' Set row heights
            ws1.Rows(1).RowHeight = 15  ' Row 1 default height
            ws1.Rows(2).RowHeight = 60  ' Row 2 for logo (merged A2:J2)
            ws1.Rows(3).RowHeight = 15  ' Row 3 default height

            ' Merge cells A2:J2 for logo placement
            On Error Resume Next
            ws1.Range("A2:J2").UnMerge  ' Unmerge first in case already merged
            ws1.Range("A2:J2").Merge
            On Error GoTo 0

            ' Insert picture in merged range A2:J2 (centered)
            Set pic = ws1.Pictures.Insert(logoPath)
            With pic
                ' Get the merged range dimensions
                Dim mergedRange As Range
                Set mergedRange = ws1.Range("A2:J2")

                Dim mergedWidth As Double
                Dim mergedHeight As Double
                mergedWidth = mergedRange.Width
                mergedHeight = mergedRange.Height

                ' Lock aspect ratio first to calculate proper dimensions
                .ShapeRange.LockAspectRatio = msoTrue

                ' Set height to match row height with padding, width will adjust proportionally
                Dim padding As Double
                padding = 5  ' Points padding

                .Height = mergedHeight - (padding * 2)
                ' Width automatically adjusts based on aspect ratio

                ' Center the image horizontally and vertically in the merged range
                .Top = mergedRange.Top + padding
                .Left = mergedRange.Left + (mergedWidth - .Width) / 2  ' Center horizontally

                ' Move and size with cells
                .Placement = xlMoveAndSize
            End With
        End If
    End If

    ' =====================================================================
    ' PART 1: Clean up Tab 1 Factor Status
    ' =====================================================================

    If Not ws1 Is Nothing Then
        Dim selectedStartRow As Long
        Dim bankStartRow As Long
        Dim bankEndRow As Long
        Dim activeCol As Long
        Dim codeCol As Long

        activeCol = 1  ' Column A
        codeCol = 5    ' Column E

        ' Find section boundaries
        Dim j As Long
        For j = 1 To 300
            If Not IsEmpty(ws1.Cells(j, activeCol)) Then
                If InStr(1, ws1.Cells(j, activeCol).Value, "SELECTED FACTORS", vbTextCompare) > 0 Then
                    selectedStartRow = j + 2
                ElseIf InStr(1, ws1.Cells(j, activeCol).Value, "FACTOR BANK", vbTextCompare) > 0 Then
                    bankStartRow = j + 2
                End If
            End If
        Next j

        bankEndRow = ws1.Cells(ws1.Rows.Count, codeCol).End(xlUp).Row

        ' Set all Factor Bank entries to NO
        Dim bankRow As Long
        For bankRow = bankStartRow To bankEndRow
            If ws1.Cells(bankRow, codeCol).Value <> "" And ws1.Cells(bankRow, codeCol).Value <> "Code" Then
                Dim cellValue As String
                cellValue = UCase(Trim(CStr(ws1.Cells(bankRow, activeCol).Value)))
                If cellValue = "YES" Or cellValue = "TRUE" Then
                    ws1.Cells(bankRow, activeCol).Value = "NO"
                End If
            End If
        Next bankRow

        ' Set all Selected Factors entries to YES
        Dim selectedRow As Long
        For selectedRow = selectedStartRow To selectedStartRow + 100
            If ws1.Cells(selectedRow, codeCol).Value = "" Then Exit For

            Dim selValue As String
            selValue = UCase(Trim(CStr(ws1.Cells(selectedRow, activeCol).Value)))
            If selValue = "NO" Or selValue = "FALSE" Or selValue = "" Then
                ws1.Cells(selectedRow, activeCol).Value = "YES"
            End If
        Next selectedRow
    End If

    ' =====================================================================
    ' PART 2: Auto-Sort Tab 4
    ' =====================================================================

    ' Find Tab 4 ("4-Security Scanner")
    Dim ws As Worksheet
    Dim foundSheet As Boolean
    foundSheet = False

    For Each ws In ThisWorkbook.Worksheets
        If InStr(ws.Name, "Scanner") > 0 Or ws.Name = "4-Security Scanner" Then
            foundSheet = True
            Exit For
        End If
    Next ws

    If Not foundSheet Then
        Application.ScreenUpdating = True
        Exit Sub
    End If

    ' Find header rows
    Dim headerRow1 As Long
    Dim i As Long
    headerRow1 = 0
    For i = 1 To 50
        If ws.Cells(i, 1).Value = "Ticker" Then
            headerRow1 = i
            Exit For
        End If
    Next i

    If headerRow1 = 0 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If

    Dim headerRow2 As Long, dataStartRow As Long, dataEndRow As Long
    Dim compositeCol As Long, lastDataCol As Long

    headerRow2 = headerRow1 + 1
    dataStartRow = headerRow2 + 1
    compositeCol = 4  ' Column D - Composite score

    ' Find last row with data
    dataEndRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row  ' Column A = Ticker

    If dataEndRow < dataStartRow Then
        Application.ScreenUpdating = True
        Exit Sub
    End If

    ' Find last data column
    lastDataCol = ws.Cells(headerRow2, ws.Columns.Count).End(xlToLeft).Column

    ' Sort by Composite Score (descending)
    ws.Sort.SortFields.Clear
    ws.Sort.SortFields.Add2 _
        key:=ws.Range(ws.Cells(dataStartRow, compositeCol), ws.Cells(dataEndRow, compositeCol)), _
        SortOn:=xlSortOnValues, _
        Order:=xlDescending, _
        DataOption:=xlSortNormal

    With ws.Sort
        .SetRange ws.Range(ws.Cells(dataStartRow, 1), ws.Cells(dataEndRow, lastDataCol))
        .Header = xlNo
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With

    ' Update rank column (1, 2, 3...)
    For i = 0 To (dataEndRow - dataStartRow)
        ws.Cells(dataStartRow + i, 3).Value = i + 1  ' Column C = Rank
    Next i

    Application.ScreenUpdating = True

End Sub



```

### Module: `Sheet4.cls`

- **Stream:** `VBA/Sheet4`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet4"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
'========================================
' Tab 4 (4-Security Scanner) - COMBINED VBA
'========================================
' HIERARCHICAL ORGANIZATION (Bottom to Top - Operational Order):
'
' USER-FACING MACROS (ordered by execution sequence):
'   1. Tab4_01_ApplyAlternatingRows         - Base layer: Alternating white/gray rows
'   2. Tab4_02_RefreshAllFormatting         - Master: Calls all in correct order
'
' AUTOMATIC EVENT HANDLERS (run automatically):
'   - Worksheet_Calculate                   - Auto-sort when weights change
'   - Worksheet_Activate                    - Refresh formatting when activated
'
'========================================

Option Explicit

'========================================
' PART 1: USER-FACING MACROS (Operational Order: Bottom to Top)
'========================================

Sub Tab4_01_ApplyAlternatingRows()
    '=====================================================================
    ' STEP 1 (Base Layer): Apply alternating white/gray rows to data columns
    '
    ' Columns with ALTERNATING ROWS (base layer):
    '   A: Ticker
    '   B: Name
    '   C: Rank
    '   D: Composite (NO FILL - has conditional formatting)
    '   E: Mkt Val
    '   F: Country
    '   G: Industry Group
    '   H+: Factor columns (Score columns have conditional formatting, Value columns get fills)
    '
    ' Pattern: Even rows (0,2,4...) = White, Odd rows (1,3,5...) = Light Gray
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim numFactors As Long

    ' Reference to Tab 4
    Set ws = ThisWorkbook.Sheets("4-Security Scanner")

    ' Find data start (look for "Ticker" in column A, data starts 2 rows below)
    dataStart = 0
    For i = 1 To 50
        If ws.Cells(i, 1).Value = "Ticker" Then
            dataStart = i + 2  ' Skip header row and Filter row
            Exit For
        End If
    Next i

    If dataStart = 0 Then
        MsgBox "Error: Could not find data start row", vbCritical
        Exit Sub
    End If

    ' Find last row with data (Ticker column A)
    dataEnd = dataStart
    For i = dataStart To 2000
        If ws.Cells(i, 1).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Count number of factors (look at weight table starting at row 7)
    numFactors = 0
    For i = 7 To 50
        If ws.Cells(i, 1).Value = "TOTAL" Then
            Exit For
        End If
        If ws.Cells(i, 2).Value <> "" Then
            numFactors = numFactors + 1
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)

    ' Apply alternating rows
    For rowIdx = 0 To (dataEnd - dataStart)
        i = dataStart + rowIdx

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Column A: Ticker
        ws.Cells(i, 1).Interior.Color = rowColor

        ' Column B: Name
        ws.Cells(i, 2).Interior.Color = rowColor

        ' Column C: Rank
        ws.Cells(i, 3).Interior.Color = rowColor

        ' Column D: Composite - DO NOT FILL (has conditional formatting)
        ' Leave as-is

        ' Column E: Mkt Val
        ws.Cells(i, 5).Interior.Color = rowColor

        ' Column F: Country
        ws.Cells(i, 6).Interior.Color = rowColor

        ' Column G: Industry Group
        ws.Cells(i, 7).Interior.Color = rowColor

        ' Factor columns start at H (column 8)
        ' Pattern: Score (H), Value (I), Score (J), Value (K), etc.
        ' Only apply fills to VALUE columns (odd positions: I, K, M, O, etc.)
        Dim factorCol As Long
        Dim factorIdx As Long
        For factorIdx = 0 To numFactors - 1
            ' Score column (H, J, L, N, etc.) - DO NOT FILL (has conditional formatting)
            ' Value column (I, K, M, O, etc.) - APPLY FILL
            factorCol = 8 + (factorIdx * 2)  ' Score column
            ' Skip Score column, fill Value column
            ws.Cells(i, factorCol + 1).Interior.Color = rowColor
        Next factorIdx
    Next rowIdx

End Sub

Sub Tab4_02_RefreshAllFormatting()
    '=====================================================================
    ' STEP 2 (Master Function): Refresh ALL Tab 4 formatting in correct order
    ' Call this after any data changes, sorting, or manual edits
    '=====================================================================
    Call Tab4_01_ApplyAlternatingRows
End Sub

'========================================
' PART 2: AUTOMATIC EVENT HANDLERS
'========================================

Private Sub Worksheet_Calculate()
    '=====================================================================
    ' Auto-Rerank v2.5 - Automatically sorts Tab 4 when weights change
    '=====================================================================
    ' WHAT IT DOES:
    ' - Detects when composite scores recalculate (due to weight changes)
    ' - Automatically sorts securities by composite score (descending)
    ' - Maintains rank numbers 1, 2, 3...
    ' - Refreshes alternating row formatting after sort
    '
    ' Column structure:
    ' - Ticker (A), Name (B), Rank (C), Composite (D), Mkt Val (E), Country (F), Industry Group (G)
    ' - Composite column is D (sorts descending)
    ' - Rank column is C (auto-updated after sort)
    ' - Factor columns start at column H (8)
    '=====================================================================

    On Error Resume Next

    ' Only run if this is the active sheet
    If ActiveSheet.Name <> Me.Name Then Exit Sub

    ' Prevent recursive calculation triggers
    Application.EnableEvents = False
    Application.ScreenUpdating = False

    Dim ws As Worksheet
    Set ws = Me

    Dim i As Long  ' Loop counter variable

    ' Find header row (look for "Ticker" in column A)
    Dim headerRow1 As Long
    headerRow1 = 0
    For i = 1 To 50
        If ws.Cells(i, 1).Value = "Ticker" Then
            headerRow1 = i
            Exit For
        End If
    Next i

    If headerRow1 = 0 Then
        Application.EnableEvents = True
        Application.ScreenUpdating = True
        Exit Sub
    End If

    Dim headerRow2 As Long
    Dim dataStartRow As Long
    Dim compositeCol As Long

    headerRow2 = headerRow1 + 1
    dataStartRow = headerRow2 + 1
    compositeCol = 4  ' Column D

    ' Find last row with data (Column A = Ticker)
    Dim dataEndRow As Long
    dataEndRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' Verify we have data to sort
    If dataEndRow < dataStartRow Then
        Application.EnableEvents = True
        Application.ScreenUpdating = True
        Exit Sub
    End If

    ' Find last data column
    Dim lastDataCol As Long
    lastDataCol = ws.Cells(headerRow2, ws.Columns.Count).End(xlToLeft).Column

    ' Sort by Composite Score (descending)
    ws.Sort.SortFields.Clear
    ws.Sort.SortFields.Add2 _
        key:=ws.Range(ws.Cells(dataStartRow, compositeCol), ws.Cells(dataEndRow, compositeCol)), _
        SortOn:=xlSortOnValues, _
        Order:=xlDescending, _
        DataOption:=xlSortNormal

    With ws.Sort
        .SetRange ws.Range(ws.Cells(dataStartRow, 1), ws.Cells(dataEndRow, lastDataCol))
        .Header = xlNo
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With

    ' Update rank column (1, 2, 3...)
    Dim rankCol As Long
    rankCol = 3  ' Column C
    For i = 0 To (dataEndRow - dataStartRow)
        ws.Cells(dataStartRow + i, rankCol).Value = i + 1
    Next i

    ' Refresh alternating rows after sort
    Call Tab4_01_ApplyAlternatingRows

    Application.EnableEvents = True
    Application.ScreenUpdating = True

End Sub

Private Sub Worksheet_Activate()
    '=====================================================================
    ' Refresh formatting when sheet is activated
    '=====================================================================
    On Error Resume Next
    Call Tab4_02_RefreshAllFormatting
End Sub

'========================================
' NOTES:
' - Alternating rows are independent of Tab 2 data
' - Conditional formatting on columns D (Composite) and H/J/L/N (Factor Scores) is preserved
' - Pattern matches Tab 1 exactly: even=white, odd=gray
' - Auto-sorts when weights change (via Worksheet_Calculate)
' - Auto-refreshes formatting after sort
' - Use Tab4_02_RefreshAllFormatting as the main entry point for manual refresh
'========================================


```

### Module: `Sheet2.cls`

- **Stream:** `VBA/Sheet2`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet2"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Private Sub Worksheet_Calculate()
      '=====================================================================
      ' Auto-Sort Tab 3 - Alphabetically by Company Name
      '=====================================================================
      ' This code goes in the Sheet3 code window (Tab 3: "3-Data (Complete)")
      '
      ' WHAT IT DOES:
      ' - Automatically sorts all securities alphabetically by Company Name
      ' - Maintains all data integrity across all columns
      ' - Preserves header structure (rows 1-6)
      '
      ' STRUCTURE:
      ' - Rows 1-5: Title/headers
      ' - Row 6: FILTER row
      ' - Row 7+: Data rows
      ' - Column B: Company Name (sort key)
      '=====================================================================

      On Error Resume Next

      ' Only run if this is the active sheet
      If ActiveSheet.Name <> Me.Name Then Exit Sub

      ' Prevent recursive calculation triggers
      Application.EnableEvents = False
      Application.ScreenUpdating = False

      Dim ws As Worksheet
      Set ws = Me

      ' CONFIGURATION
      Dim headerRow As Long
      Dim dataStartRow As Long
      Dim companyNameCol As Long

      ' Tab 3 structure:
      ' Row 5: Headers (Ticker, Company Name, Mkt Val, etc.)
      ' Row 6: FILTER row
      ' Row 7+: Data
      headerRow = 5
      dataStartRow = 7
      companyNameCol = 2  ' Column B = Company Name

      ' Find last row with data (check Ticker column)
      Dim dataEndRow As Long
      dataEndRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row  ' Column A = Ticker

      ' Verify we have data to sort
      If dataEndRow < dataStartRow Then
          Application.EnableEvents = True
          Application.ScreenUpdating = True
          Exit Sub
      End If

      ' Find last data column
      Dim lastDataCol As Long
      lastDataCol = ws.Cells(headerRow, ws.Columns.Count).End(xlToLeft).Column

      ' Sort by Company Name (ascending/alphabetical)
      ws.Sort.SortFields.Clear
      ws.Sort.SortFields.Add _
          key:=ws.Range(ws.Cells(dataStartRow, companyNameCol), ws.Cells(dataEndRow, companyNameCol)), _
          SortOn:=xlSortOnValues, _
          Order:=xlAscending, _
          DataOption:=xlSortNormal

      With ws.Sort
          .SetRange ws.Range(ws.Cells(dataStartRow, 1), ws.Cells(dataEndRow, lastDataCol))
          .Header = xlNo
          .MatchCase = False
          .Orientation = xlTopToBottom
          .SortMethod = xlPinYin
          .Apply
      End With

      Application.EnableEvents = True
      Application.ScreenUpdating = True

  End Sub


```

### Module: `Sheet3.cls`

- **Stream:** `VBA/Sheet3`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet3"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
'========================================
' Tab 3 (3-Factor Data) - COMBINED VBA
'========================================
' HIERARCHICAL ORGANIZATION (Bottom to Top - Operational Order):
'
' USER-FACING MACROS (ordered by execution sequence):
'   1. Tab3_01_ApplyAlternatingRows                - Base layer: Alternating white/gray rows
'   2. Tab3_02_ReapplySystematicEquityHighlighting - Top layer: Green highlighting for Systematic Equity (Column F)
'   3. Tab3_03_ApplySystematicFactorsFormatting    - Top layer: Red "No" formatting (Column N)
'   4. Tab3_04_RefreshAllFormatting                - Master: Calls all in correct order
'
'========================================

Option Explicit

'========================================
' PART 1: USER-FACING MACROS (Operational Order: Bottom to Top)
'========================================

Sub Tab3_01_ApplyAlternatingRows()
    '=====================================================================
    ' STEP 1 (Base Layer): Apply alternating white/gray rows to columns A-F
    ' Column F will have green highlighting applied on top by next step
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim isGreenRow As Boolean

    ' Reference to Tab 3
    Set ws = ThisWorkbook.Sheets("3-Factor Data")

    ' Data starts at row 7 (after Filter row 6)
    dataStart = 7

    ' Find last row with data (Factor Code column C)
    dataEnd = dataStart
    For i = dataStart To 1000
        If ws.Cells(i, 3).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)
    Const COLOR_GREEN As Long = 13434828        ' RGB(200, 230, 201) - Light green

    ' Apply alternating rows to columns A-F
    For rowIdx = 0 To (dataEnd - dataStart)
        i = dataStart + rowIdx

        ' Check if this row has green highlighting (check column F for existing green)
        isGreenRow = (ws.Cells(i, 6).Interior.Color = COLOR_GREEN)

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Apply to columns A-F
        For col = 1 To 6
            Set cell = ws.Cells(i, col)

            ' Preserve green highlighting for column F
            If isGreenRow And col = 6 Then
                cell.Interior.Color = COLOR_GREEN
            Else
                ' Apply alternating color
                cell.Interior.Color = rowColor
            End If
        Next col
    Next rowIdx

End Sub

Sub Tab3_02_ReapplySystematicEquityHighlighting()
    '=====================================================================
    ' STEP 2 (Top Layer): Apply green highlighting to "Systematic Equity" rows
    ' Searches column F (Asset Class) and applies green to matching rows
    ' MUST run AFTER alternating rows to sit on top of base formatting
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long
    Dim assetClass As String

    Set ws = ThisWorkbook.Sheets("3-Factor Data")

    ' Data starts at row 7
    dataStart = 7

    ' Find last row with data (Factor Code column C)
    dataEnd = dataStart
    For i = dataStart To 1000
        If ws.Cells(i, 3).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215
    Const COLOR_LIGHT_GRAY As Long = 15921906
    Const COLOR_GREEN As Long = 13434828  ' RGB(200, 230, 201) - Light green

    ' First, clear all green highlighting (reset to alternating colors)
    For i = dataStart To dataEnd
        Dim rowIdx As Long
        rowIdx = i - dataStart

        Dim alternatingColor As Long
        If rowIdx Mod 2 = 0 Then
            alternatingColor = COLOR_WHITE
        Else
            alternatingColor = COLOR_LIGHT_GRAY
        End If

        ' Reset column F to alternating color
        ws.Cells(i, 6).Interior.Color = alternatingColor
    Next i

    ' Apply green highlighting to "Systematic Equity" rows
    For i = dataStart To dataEnd
        ' Get Asset Class value from column F (6)
        assetClass = Trim(UCase(CStr(ws.Cells(i, 6).Value)))

        If assetClass = "SYSTEMATIC EQUITY" Then
            ' Apply green to column F
            ws.Cells(i, 6).Interior.Color = COLOR_GREEN
        End If
    Next i

End Sub

Sub Tab3_03_ApplySystematicFactorsFormatting()
    '=====================================================================
    ' STEP 3: Apply "Systematic Factors" column formatting (Column N)
    ' - Applies red background + dark red text (regular weight) to "No" values
    ' - Matches "Inverse" formatting style from column D (Relationship)
    ' Excel default red: Background #FFC7CE, Text #9C0006, Regular (not bold)
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long

    Set ws = ThisWorkbook.Sheets("3-Factor Data")

    ' Define Excel's default red conditional formatting colors (matches "Inverse" in column D)
    Const COLOR_RED_BG As Long = 13551615      ' RGB(255, 199, 206) = #FFC7CE
    Const COLOR_RED_TEXT As Long = 393372     ' RGB(156, 0, 6) = #9C0006
    Const COLOR_BLACK_TEXT As Long = 0         ' RGB(0, 0, 0) = Black

    ' Data starts at row 7 (after Filter row 6)
    dataStart = 7

    ' Find last row with data (Factor Code column A)
    dataEnd = dataStart
    For i = dataStart To 1000
        If ws.Cells(i, 1).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Apply formatting to all data rows
    For i = dataStart To dataEnd
        Dim cellValue As String
        cellValue = Trim(UCase(CStr(ws.Cells(i, 14).Value)))  ' Column N = 14

        ' Apply formatting based on value (do not modify cell values)
        If cellValue = "NO" Then
            ws.Cells(i, 14).Interior.Color = COLOR_RED_BG
            ws.Cells(i, 14).Font.Color = COLOR_RED_TEXT
            ws.Cells(i, 14).Font.Bold = False  ' Regular weight, not bold
        ElseIf cellValue = "YES" Then
            ' Reset to default (alternating row color will be applied by other functions)
            ws.Cells(i, 14).Font.Color = COLOR_BLACK_TEXT
            ws.Cells(i, 14).Font.Bold = False
        End If
    Next i

End Sub

Sub Tab3_04_RefreshAllFormatting()
    '=====================================================================
    ' STEP 4 (Master Function): Refresh ALL Tab 3 formatting in correct order
    ' Call this after any data changes or sorting
    ' Executes all formatting steps in proper sequence
    '=====================================================================
    Call Tab3_01_ApplyAlternatingRows
    Call Tab3_02_ReapplySystematicEquityHighlighting
    Call Tab3_03_ApplySystematicFactorsFormatting
End Sub

'========================================
' PART 2: AUTOMATIC EVENT HANDLERS
'========================================

Private Sub Worksheet_Change(ByVal Target As Range)
    '=====================================================================
    ' Automatically refresh formatting when column F (Asset Class) changes
    '=====================================================================
    On Error GoTo ErrorHandler

    ' If column F changed, refresh formatting
    If Target.Column = 6 And Target.Cells.Count = 1 Then
        Application.EnableEvents = False
        Call Tab3_04_RefreshAllFormatting
        Application.EnableEvents = True
    End If

    Exit Sub

ErrorHandler:
    Application.EnableEvents = True
    MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
End Sub

Private Sub Worksheet_Activate()
    '=====================================================================
    ' Refresh formatting when sheet is activated
    '=====================================================================
    On Error Resume Next
    Call Tab3_04_RefreshAllFormatting
End Sub


```
```

### yang-pipeline-terraform----reference-s3-backed-lambda-architecture-pattern.tf

```
# Yang Pipeline — Terraform Module
#
# Manages: S3 trigger → Step Functions → 25+ Lambdas
# Pattern: Canonical 7-file split (lambdas, iam, stepfunctions, triggers, outputs)
# No EC2 or EventBridge schedule — pipeline triggered by S3 upload
#
# Resources imported from existing AWS infrastructure.
# Run IMPORT_COMMANDS.sh after terraform init to import existing resources.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "opal-313476888478-terraform-state"
    key    = "yang-pipeline/tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "OpalPortal"
      ManagedBy   = "Terraform"
      Environment = "Production"
      System      = "YangPipeline"
    }
  }
}

locals {
  account_id      = "313476888478"
  region          = "us-east-1"
  lambda_role_arn = "arn:aws:iam::${local.account_id}:role/yang-pipeline-lambda-role"

  # Shared layers
  pandas_layer   = "arn:aws:lambda:${local.region}:${local.account_id}:layer:pandas-pyarrow-layer:1"
  openpyxl_layer = "arn:aws:lambda:${local.region}:${local.account_id}:layer:openpyxl-layer:1"
  aws_pandas_312 = "arn:aws:lambda:${local.region}:336392948345:layer:AWSSDKPandas-Python312:16"
}
```

---

## Participant Background

### 0.5.0_AE_OpalETL -- Pending Task Orders

#### infrastructure_inventory.md

# Task Order: Infrastructure Inventory

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-infrastructure-inventory</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
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
      <dir>infra/aws/terraform/yang-pipeline/</dir>
      <dir>infra/aws/terraform/news-pipeline/</dir>
      <dir>infra/aws/terraform/market-overview/</dir>
      <dir>infra/aws/terraform/smartx-pipeline/</dir>
      <dir>infra/aws/terraform/seeking-alpha/</dir>
      <dir>infra/aws/terraform/portfolio-management/</dir>
      <dir>infra/aws/terraform/causality/</dir>
    </terraform_dirs>
    <lambda_source_map>infra/aws/lambda/ci/lambda-source-map.json</lambda_source_map>
    <data_scripts>
      <dir>data/yang/</dir>
      <dir>data/seeking-alpha/</dir>
    </data_scripts>
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
    <criterion id="1">Output is valid XML written to org/tier2_senior/0.5.0_AE_OpalETL/deliverables/infrastructure_inventory.xml</criterion>
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
      org/tier2_senior/0.5.0_AE_OpalETL/deliverables/infrastructure_inventory.xml
    </deliverable>
  </deliverables>
</task_order>

## Key Files to Read

### Terraform Directories
- `infra/aws/terraform/yang-pipeline/` -- all .tf files (tag: yang-v2.1.0)
- `infra/aws/terraform/news-pipeline/` -- all .tf files (tag: news-v2.4.0)
- `infra/aws/terraform/market-overview/` -- all .tf files (tag: market-overview-v1.4.0)
- `infra/aws/terraform/smartx-pipeline/` -- all .tf files (tag: smartx-v1.0.0)
- `infra/aws/terraform/seeking-alpha/` -- all .tf files (NOT yet tagged/Terraformed)
- `infra/aws/terraform/portfolio-management/` -- all .tf files (NOT yet tagged/Terraformed)
- `infra/aws/terraform/causality/` -- all .tf files (NOT yet tagged/Terraformed)

### Lambda Source Map
- `infra/aws/lambda/ci/lambda-source-map.json` -- filter to functions belonging to yang, news, market-overview, smartx, seeking-alpha, portfolio, and causality pipelines

### Lambda Source Directories
- `infra/aws/lambda/` -- all subdirectories for yang, news, smartx, market, causality, portfolio, seeking-alpha functions
- Read each function's handler file to understand what it does

### Data Scripts
- `data/yang/` -- Yang pipeline data processing scripts
- `data/seeking-alpha/` -- Seeking Alpha data processing scripts

### Deployment Tags
- yang-v2.1.0, news-v2.4.0, market-overview-v1.4.0, smartx-v1.0.0
- seeking-alpha, portfolio, causality -- NOT yet tagged or Terraformed

## Deliverable XML Schema

Write your inventory using this structure:

```xml
<infrastructure_inventory>
  <metadata>
    <agent>0.5.0_AE_OpalETL</agent>
    <scope>Yang, News, Market Overview, SmartX, Seeking Alpha, Portfolio, Causality</scope>
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


### 0.5.0_AE_OpalETL -- Recent Commits

# Recent commits by 0.5.0_AE_OpalETL

972c52f5 org(1.0.0_SA_CTO): session log -- AE prompt enrichment (Session D complete)
6da4c13f 0.5.0_AE_OpalETL: enrich OpalETL agent prompt with source-grounded context
d327b3f2 feat(org): AE team wave — pipeline inventories + mandatory protocol reads

### 0.5.0_AE_OpalETL -- Recent Deployments

# Recent deployment tags (all pipelines, newest first)

bd-v2.16.2
bd-v2.16.3
bd-v2.16.1
bd-v2.17.0
portfolio-management-v1.7.0
portal-auth-v1.3.0
portal-auth-v1.2.2
portal-auth-v1.2.1
portal-auth-v1.2.0
portal-auth-v1.1.0
shared-infra-v1.3.0
bd-v2.15.3
bd-v2.15.2
bd-v2.16.0
bd-v2.15.1
bd-v2.15.0
portal-auth-v1.0.0
yang-v2.1.6
yang-v2.1.5
yang-v2.1.4

### 0.3.0_DE_TradingOperations -- Recent Session Logs

#### wave2_pod_inventory_activation.md

# Wave 2 Pod Inventory Activation — 0.3.0_DE_TradingOperations

**Date:** 2026-03-02
**Start Time:** ~19:00
**End Time:** ~19:30

## Objective

Complete Wave 2 activation task order from 1.0.0_SA_CTO. Produce pod_inventory.xml as permanent
ground-truth context for the TradingOperations pod: PortfolioManagement, TradeSubmission, DataRefresh.

## Work Completed

- Read org/AGENT_START_HERE.md (orientation protocol)
- Read org/tier2_senior/0.3.0_DE_TradingOperations/README.md and prompt.md (identity)
- Read org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-02/org_activation_plan.md (full 6-wave plan)
- Read task order: org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/pod_inventory.md
- Read all 3 RD page_inventory.xml deliverables:
  - org/tier3_junior/0.3.1_RD_PortfolioManagement/deliverables/page_inventory.xml (55 files)
  - org/tier3_junior/0.3.2_RD_TradeSubmission/deliverables/page_inventory.xml (16 files)
  - org/tier3_junior/0.3.3_RD_DataRefresh/deliverables/page_inventory.xml (12 files)
- Read portal/src/api/endpoints/portfolio-optimization.ts (full)
- Read portal/src/api/endpoints/trade-submission.ts (full)
- Read portal/src/api/endpoints/portfolio.ts (full)
- Read portal/src/api/portal-proxy.ts (DataRefresh section, lines 1838-1975 via grep)
- Read portal/src/hooks/useYangData.ts (thin YangDataContext wrapper — not used by this pod)
- Wrote deliverable: org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml
- Marked task order status: complete

## Decisions Made

- **Decision: useYangData.ts not consumed by this pod** — DataRefresh reads manifest.json directly for
  freshness; PM/TS do not use Yang timestamp. Documented as low-criticality external dependency.

- **Decision: Intra-pod bridge is the highest-value architectural insight** — exportAndSubmit() in
  portfolio.ts is the sole connection between PortfolioManagement and TradeSubmission. Documented
  as HIGH criticality intra_pod_workflow with full endpoint chain.

- **Decision: Dual auto-save paths flagged as risk** — PM has legacy (trade-based via updateAutoSave)
  AND new optimization-state (via saveOptimizationAutoSave). Both run 60s intervals. Zustand store
  (usePortfolioStore) and React Query coexist, creating state split complexity.

- **Decision: DataRefresh is dev-gated (scoped API)** — not accessible to regular users. Noted in
  pod_health operational_note.

## Files Modified

- `org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml` — created
- `org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/pod_inventory.md` — status: pending -> complete
- `org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-02/wave2_pod_inventory_activation.md` — this file

## Blockers

None. All 3 RD deliverables were present. All portal endpoint files were present and readable.
useYangData.ts was present but is not consumed by this pod.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

pod_inventory.xml is written at the correct path and follows the schema specified in the task order.
All sections are populated from actual file reads (no inference). Task order marked complete.
The deliverable is ready for the Wave 3 DS agent (0.3.0_DS_TradingOperations) to consume as input
for the data_contract.xml task.

## Next Steps

> Ordered list for next session pickup.

1. **Receive Wave 3 task order** from 1.0.0_SA_CTO — DS data_contract.xml task order will reference
   this pod_inventory.xml as primary input. No action required from DE until task order arrives.

2. **Monitor open issues in PortfolioManagement** — 9 TODO stubs in calculation hooks are technical
   debt. If Andrew or CTO flags these for sprint work, issue task orders to 0.3.1_RD_PortfolioManagement
   with specific hooks to address (useOptimizationCalculations.ts lines 61-72, usePortfolioEditStore.ts:143).

3. **Track getSecurityDetails backend** — 0.3.0_DS_TradingOperations or a DT should confirm whether
   opal-pm-optimization-loader or a separate Lambda handles /api/private/portfolio-management/security/{ticker}.
   Currently unimplemented — breaks SecurityLookupModal add-security flow.

**Files to touch next:**
- None for DE until Wave 3 DS task order is issued

**Do NOT:**
- Modify any portal source files — this was a read-and-document activation task
- Issue Wave 3 DS task orders — that is the CTO's responsibility after Wave 2 is fully complete
  across all 4 DE pods


### 0.3.0_DE_TradingOperations -- Pending Task Orders

#### trade_engine_polish_TO1_threshold_highlighting.md

# Task Order: Trade Engine Visual Polish — TO-1: Threshold Highlighting

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Apply threshold-based conditional text coloring to Risk Decomposition, Alpha tab, and Sector tab
    columns. Covers PRD items 2, 3, 4, and 5. All changes are cosmetic — no data contract changes,
    no API changes. Route to 0.3.1_RD_PortfolioManagement or handle directly.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/components/OptimizationSummaryHeader.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/SectorTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 2 — Risk Decomposition Exposure columns (OptimizationSummaryHeader.tsx lines 359-367):
        Initial Exposure:   green if > 0.1,  red if &lt; -0.1, neutral otherwise
        Optimized Exposure: green if > 0.1,  red if &lt; -0.1, neutral otherwise
        Trade (Exposure):   green if > 0.05, red if &lt; -0.05, neutral otherwise
      Apply text color: hsl(var(--success)) for green, hsl(var(--danger)) for red,
      text-white/70 for neutral.
    </requirement>
    <requirement id="2">
      PRD Item 3 — Risk Decomposition Contribution columns (OptimizationSummaryHeader.tsx lines 373-381):
        Initial Contribution:   red if > 5, no green threshold (one-directional)
        Optimized Contribution: red if > 5, no green threshold (one-directional)
        Delta (Contribution):   green if &lt; -2 (reducing risk = good), red if > 2
      Same color tokens as above.
    </requirement>
    <requirement id="3">
      PRD Item 4 — Alpha tab (AlphaTab.tsx). Currently only Trade uses getTradeColor with +-0.01.
      Change ALL three columns (Initial Bet, Optimized Bet, Trade) to +-0.1 threshold:
        green if > 0.1, red if &lt; -0.1, neutral otherwise
      Apply in both the By Factor view (line 431, 434-438) and the By Group view (lines 278-282).
      Update or replace the getTradeColor function if it is hardcoded to +-0.01 for these columns.
    </requirement>
    <requirement id="4">
      PRD Item 5 — Sector tab (SectorTab.tsx). Currently Trade columns use +-0.01 threshold.
      New thresholds:
        Initial Bet:   green if > 2,   red if &lt; -2
        Optimized Bet: green if > 2,   red if &lt; -2
        Trade:         green if > 0.5, red if &lt; -0.5
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Risk Decomp table: Exposure and Contribution columns color per spec. Neutral band renders white/70.</criterion>
    <criterion id="2">Alpha tab By Factor + By Group: all three columns use +-0.1 thresholds. Old +-0.01 threshold replaced.</criterion>
    <criterion id="3">Sector tab: bet columns use +-2, trade column uses +-0.5.</criterion>
    <criterion id="4">No TypeScript errors. No regression on other PortfolioManagement tabs.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No data contract changes. No new props through component boundaries if avoidable — these are purely local styling decisions.</constraint>
    <constraint>Reuse existing color token pattern (hsl(var(--success)), hsl(var(--danger))) that is already in use in the file. Do not introduce new CSS classes or Tailwind utilities that do not already exist in the portal.</constraint>
    <constraint>DT pushes portal DEV after DE reviews. DE must not signal DT push until DE has visually inspected the changes.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with items 2-5 complete</deliverable>
    <deliverable type="document">Session log noting commit hashes and a brief confirmation that tsc passes</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO2_gradient_color_scales.md

# Task Order: Trade Engine Visual Polish — TO-2: Gradient Color Scales

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Apply continuous gradient background color scales to Model tab (items 6) and Trade tab
    (items 8, 9). Adds initialBet gradient and a new derived finalBet column. Pattern is
    getGradientBackground already used by PortfolioGrid.tsx (lines 466-516).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 6 — Model tab (ModelTab.tsx):
      Apply continuous gradient to Coefficient and Weight columns.
      Scale: white (low) to green (high) — same direction as positive values = good.
      Reuse getGradientBackground from PortfolioGrid.tsx. If not currently importable,
      extract it to a shared util (e.g., portal/src/pages/PortfolioManagement/utils/colorUtils.ts)
      and update both files to import from there.
    </requirement>
    <requirement id="2">
      PRD Item 8 — Trade tab (PortfolioGrid.tsx): apply gradient to totalRisk and specRisk columns.
      Scale: INVERTED — green (low risk) to red (high risk). Higher value = more red.
      getGradientBackground likely needs an invert flag or a separate inverted-gradient call.
      Read the existing implementation (lines 466-516) before implementing.
    </requirement>
    <requirement id="3">
      PRD Item 9a — Trade tab: apply same gradient as optimizedBet to initialBet column.
      optimizedBet already has the full red-yellow-green gradient via getGradientBackground.
      initialBet currently shows black text with no gradient. Apply the same treatment.
    </requirement>
    <requirement id="4">
      PRD Item 9b — Trade tab: add new finalBet column.
      finalBet = finalWeight - benchmarkWeight (derived client-side, same pattern as finalTrade).
      Place finalBet adjacent to optimizedBet and initialBet in column order.
      Apply the same gradient coloring as optimizedBet and initialBet.
      Use a valueGetter (not a data field) to compute finalBet from finalWeight and benchmarkWeight.
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Model tab Coefficient and Weight cells show white-to-green gradient backgrounds.</criterion>
    <criterion id="2">Trade tab totalRisk and specRisk cells show green-to-red (inverted) gradient.</criterion>
    <criterion id="3">initialBet has same gradient treatment as optimizedBet.</criterion>
    <criterion id="4">finalBet column present, positioned adjacent to initialBet/optimizedBet, gradient applied, value = finalWeight - benchmarkWeight.</criterion>
    <criterion id="5">No TypeScript errors. getGradientBackground is either still in place or cleanly refactored to a shared util used by both callers.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read getGradientBackground (PortfolioGrid.tsx lines 466-516) before writing any gradient code. Do not duplicate the logic; import or extract it.</constraint>
    <constraint>finalBet is a derived field only — do not add it to any TypeScript interface or data contract. It is computed in the valueGetter at render time.</constraint>
    <constraint>No Lambda, Terraform, or API changes. This is pure frontend.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with items 6, 8, 9 complete</deliverable>
    <deliverable type="document">Session log with commit hashes and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO3_trade_tab_formatting.md

# Task Order: Trade Engine Visual Polish — TO-3: Trade Tab Formatting

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Two formatting changes to PortfolioGrid.tsx AG Grid column definitions:
    zero-weight cells display as dash, and size column cells get color-coded backgrounds.
    Covers PRD items 7 and 10.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 7 — Zero weight to dash:
      For columns initialWeight, optimizedWeight, finalWeight, benchmarkWeight:
      When value === 0, display "–" (en-dash, U+2013) instead of "0.00%".
      Implement via value formatter: if value === 0, return "–"; else return the existing
      percentage format. Do not change non-zero formatting.
    </requirement>
    <requirement id="2">
      PRD Item 10 — Size column coloring:
      Size column currently shows raw S/M/L/O value, bold, centered, no background color.
      Add cellStyle (or cellRenderer) that sets a muted translucent background per value:
        L (Large):   rgba(34, 197, 94, 0.15)   — green muted
        M (Mid):     rgba(234, 179, 8, 0.15)   — yellow muted
        O (Other):   rgba(239, 68, 68, 0.15)   — red muted
        S (Small):   rgba(239, 68, 68, 0.15)   — red muted (same as O)
      These are background colors, not text colors. Keep existing text styling intact.
    </requirement>
    <requirement id="3">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Securities with 0.00% weight show "–" in all four weight columns. Non-zero weights unchanged.</criterion>
    <criterion id="2">Size column cells: L = green tint, M = yellow tint, O = red tint, S = red tint. No change to text or bold formatting.</criterion>
    <criterion id="3">No TypeScript errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change value formatters for non-zero weights — only the zero case is affected.</constraint>
    <constraint>Use rgba with 0.15 alpha or similar muted value appropriate for the dark theme. Do not use full-opacity colors that clash with selected row highlighting.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit with items 7 and 10 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO4_capitalize_canonical_order.md

# Task Order: Trade Engine Visual Polish — TO-4: Capitalize + Canonical Group Ordering

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Create shared CANONICAL_GROUP_ORDER constant, apply capitalize CSS to all group name cells,
    and replace alphabetical group sort with canonical order in AlphaTab, ModelTab, and
    SecurityDetailModal. Covers PRD items 1, 11, and 13.
  </objective>

  <scope>
    <files>
      <file action="create">portal/src/pages/PortfolioManagement/utils/factorOrder.ts</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/SecurityDetailModal.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create portal/src/pages/PortfolioManagement/utils/factorOrder.ts with:

        export const CANONICAL_GROUP_ORDER = [
          'size',
          'efficiency',
          'growth',
          'management',
          'profitability',
          'quality',
          'value',
          'analyst',
          'governance',
          'crowding',
          'insider',
          'short',
          'beta',
          'momentum',
          'technical',
        ] as const

        export type CanonicalGroup = typeof CANONICAL_GROUP_ORDER[number]

        export function canonicalGroupIndex(group: string): number {
          const idx = (CANONICAL_GROUP_ORDER as readonly string[]).indexOf(group.toLowerCase())
          return idx === -1 ? CANONICAL_GROUP_ORDER.length : idx
        }

      This order matches the signal DataFrame row order in Yang's alpha PKL. Source of truth
      is portal/src/pages/PortfolioManagement/utils/factorDescriptions.ts (comment order).
      Implementation pattern mirrors ECONOMY_ORDER in TradeTab.tsx (line 249).
    </requirement>
    <requirement id="2">
      PRD Item 13 — AlphaTab.tsx By Group sort (line 74):
      Replace the .localeCompare sort with canonicalGroupIndex sort:
        - Before: a.group.localeCompare(b.group)
        - After:  canonicalGroupIndex(a.group) - canonicalGroupIndex(b.group)
      Import canonicalGroupIndex from utils/factorOrder.ts.
    </requirement>
    <requirement id="3">
      PRD Item 1 — AlphaTab.tsx By Factor view group cells (line 421):
      Add CSS class "capitalize" (or style text-transform: capitalize) to group name cells.
      The By Group view already has capitalize at line 273 — leave that intact.
    </requirement>
    <requirement id="4">
      PRD Item 13 — ModelTab.tsx By Group sort:
      Apply the same canonical group ordering via canonicalGroupIndex to ModelTab's By Group
      aggregated view (where groups are currently sorted alphabetically or by Lambda response order).
      Read ModelTab.tsx before implementing to confirm where the sort happens.
    </requirement>
    <requirement id="5">
      PRD Item 1 — ModelTab.tsx:
      Apply capitalize CSS to group column cells (wherever group names appear in the table).
    </requirement>
    <requirement id="6">
      PRD Item 11 — SecurityDetailModal.tsx:
      1. Apply capitalize CSS class to group name cells in the factor list.
      2. Sort the factor list by canonical group order (canonicalGroupIndex on the group field).
         Within each group, preserve the original factor order from the data array.
    </requirement>
    <requirement id="7">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">factorOrder.ts exists with the 15-group CANONICAL_GROUP_ORDER array, exactly as specified.</criterion>
    <criterion id="2">AlphaTab By Group view: groups appear in canonical order (size first, technical last), not alphabetical.</criterion>
    <criterion id="3">AlphaTab By Factor view: group name cells show capitalized text (Size, Efficiency, etc.).</criterion>
    <criterion id="4">ModelTab By Group view: groups in canonical order; group cells capitalized.</criterion>
    <criterion id="5">SecurityDetailModal: factor list sorted by canonical group order; group cells capitalized.</criterion>
    <criterion id="6">No TypeScript errors. No regression on the By Factor views (which are already correct).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>CANONICAL_GROUP_ORDER must live in factorOrder.ts — do not inline it in each component file. All three components import from the shared util.</constraint>
    <constraint>Groups not in CANONICAL_GROUP_ORDER sort to the end (canonicalGroupIndex returns CANONICAL_GROUP_ORDER.length for unknown groups). This is the fallback pattern — do not throw on unknown groups.</constraint>
    <constraint>Do not modify factorDescriptions.ts. It is the source of truth (read-only reference).</constraint>
    <constraint>Capitalize is a CSS presentation concern only — do not transform the data string. The underlying group value remains lowercase in the data model.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with factorOrder.ts + items 1, 11, 13 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO5_reset_zero_button.md

# Task Order: Trade Engine Visual Polish — TO-5: Reset Zero Button

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Add "Reset Zero" button to the Trade tab button group. When clicked, sets finalTrade = 0 for
    ALL securities (hold everything as-is; propose no trades). Covers PRD item 12.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/TradeTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/PortfolioManagement.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Button placement: in TradeTab.tsx button group (line ~368), insert "Reset Zero" between
      "Reset All" and "Export". The button group currently has:
        Reset Selected | Reset All | Export | Submit
      After change:
        Reset Selected | Reset All | Reset Zero | Export | Submit
    </requirement>
    <requirement id="2">
      Button behavior — "Reset Zero":
      Sets finalTrade = 0 for ALL securities.
      Implementation: finalWeight = initialWeight for every security.
      This is the "hold everything" state — tell the optimizer to make no changes.
      This is DISTINCT from "Reset All" which sets finalWeight = optimizedWeight (optimizer's suggestion).
    </requirement>
    <requirement id="3">
      TradeTab.tsx: add onResetZero prop (callback, no arguments). Wire the button to call it.
      Match the pattern of the existing onResetAll prop — read TradeTab.tsx before implementing
      to confirm the exact prop signature pattern.
    </requirement>
    <requirement id="4">
      PortfolioManagement.tsx: implement handleResetZero. It should iterate over all securities
      in state and set each security's finalWeight to its initialWeight (and finalTrade to 0).
      Read PortfolioManagement.tsx and usePortfolioEditStore to understand the correct state
      mutation path before implementing. Do not assume — cite the state update mechanism.
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Reset Zero button appears in the correct position between Reset All and Export.</criterion>
    <criterion id="2">Clicking Reset Zero sets finalTrade = 0 for all securities and finalWeight = initialWeight for all securities.</criterion>
    <criterion id="3">Reset All still works correctly (finalWeight = optimizedWeight) — no regression.</criterion>
    <criterion id="4">No TypeScript errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read TradeTab.tsx (around line 368) and PortfolioManagement.tsx BEFORE implementing. The existing button callbacks are the implementation pattern to follow.</constraint>
    <constraint>Do not use finalWeight = 0 — that would set holdings to zero. The correct operation is finalWeight = initialWeight (hold current positions).</constraint>
    <constraint>No backend changes, no API calls, no Lambda changes. Pure frontend state operation.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit with item 12 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```


### 0.3.0_DE_TradingOperations -- Recent Commits

# Recent commits by 0.3.0_DE_TradingOperations

d9686db0 org(2.0.0_SA_COO): ADVI-006 run + trade engine polish task orders

