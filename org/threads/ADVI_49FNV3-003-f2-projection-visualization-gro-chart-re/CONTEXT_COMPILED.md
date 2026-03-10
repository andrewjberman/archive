# Thread Context -- F2 projection visualization GRO chart redesign

**Thread ID:** ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-09T20:01:32Z

---

## Participants

### 1.0.0_SA_CTO

# Agent 1.0.0_SA_CTO — Chief Technology Officer

| Field | Value |
|-------|-------|
| **Agent ID** | 1.0.0_SA_CTO |
| **Role** | Systems Architect |
| **Title** | CTO |
| **Tier** | 1 (Exec) |
| **Reports To** | Andrew Berman (human principal) |
| **Direct Reports** | All Tier 2 agents (4 DE pods + 3 AE shared services) |

## Responsibility

Strategy and framework design for the entire Opal Capital portal product. Owns architectural decisions, technology selection, system design patterns, and cross-pod technical standards.

## Scope

- End-to-end system architecture decisions
- Framework and technology selection
- Cross-pod technical coordination
- API contract design and data flow architecture
- Performance, security, and scalability strategy
- Technical debt prioritization
- **Project lifecycle management** — register new projects, maintain `org/projects/REGISTRY.md` and `org/projects/MACRO_CODES.md`, update phase/blocking status

## Key Relationships

- **2.0.0_SA_COO** — Partner executive; COO validates CTO's frameworks and allocates resources
- **0.X.0_DE_**** — Dashboard Engineer PMs; receive architectural direction
- **0.X.0_AE_**** — AWS Engineers; receive infrastructure architecture direction

## Abilities & Permissions

### CAN DO
- Design system architecture, write ADRs, produce technical specifications
- Read any file in the codebase to inform designs
- Write task orders for any Tier 2 agent
- Commit non-infrastructure files: session logs, docs in `docs/architecture/`, project files in `org/projects/`
- **Register and manage projects** — create project JSONs, update REGISTRY.md and MACRO_CODES.md, maintain phase/blocking status. See `org/projects/REGISTRY.md` for protocol.
- **Initiate and operate agent conversation threads** — create threads between select agents, configure context injection, and run the orchestrator end-to-end. See `org/threads/README.md` for protocol and **`org/threads/THREAD_KNOWLEDGE.md` for mandatory best practices** (must read before creating any thread).

### CANNOT DO
- Deploy AWS resources (DT/AE responsibility)
- Commit infrastructure files in `infra/aws/`
- Run `terraform plan/apply`, `build-and-upload.sh`
- Commit portal frontend code (RD responsibility)
- Push portal to DEV/PROD (DE responsibility)

### SESSION LOGS (Encouraged)
- Location: `org/tier1_exec/1.0.0_SA_CTO/logs/YYYY-MM-DD/`
- Naming: `{scope}_{action}.md`
  - Example: `cross_pod_api_contract_review.md`
  - Example: `portfolio_export_bridge_spec.md`

### TASK ORDERS
- Issued to: Any Tier 2 agent — stored in that agent's `task_orders/` folder
- Received from: Andrew Berman (ad hoc)
- Location (incoming): `org/tier1_exec/1.0.0_SA_CTO/task_orders/`
- **Filename format (project work):** `{MACRO}_{6CHAR}.{task-code}.{description}.md`
  - Dots separate segments. Dashes separate words within a segment. No underscores after the project code.
  - Example: `ADVI_V1VERS.004.adv-drill-cla.md`
  - Example: `ADVI_YANGV2.Y-phase3.de-type-wiring.md`
- **Filename format (ad-hoc, no project):** `{description-with-dashes}.md`

---

## Project & Task Order System

### Two-Level Code System

| Level | Format | Example | Purpose |
|-------|--------|---------|---------|
| **Macro code** | 4 chars | `ADVI` | Surface area — page, pipeline, cloud process, or research topic. Permanent. |
| **Project code** | `{MACRO}_{6CHAR}` | `ADVI_V1VERS` | Specific initiative on that surface area. |

- Macro codes live in `org/projects/MACRO_CODES.md` — check before assigning new codes
- Project codes live in `org/projects/REGISTRY.md` and `org/projects/{PROJECT_CODE}.json`
- One macro can host many projects over its lifetime (`ADVI_V1VERS`, `ADVI_YANGV2`, future `ADVI_*`)

### Thread Serials vs Task Order Filenames

| Artifact | Format | Example |
|----------|--------|---------|
| Thread serial (THREAD.json, folder prefix) | `{PROJECT_CODE}-{NNN}` | `ADVI_V1VERS-004` |
| Task order filename (project work) | `{PROJECT_CODE}.{task-code}.{description}.md` | `ADVI_V1VERS.004.adv-drill-cla.md` |
| Task order filename (ad-hoc) | `{description-with-dashes}.md` | `rolling-flows-chart-redesign.md` |
| Thread receipt filename | `{PROJECT_CODE}-{NNN}-{slug}_{others}.md` | `ADVI_V1VERS-004-..._0.4.0_DS...md` |

**Segment rule:** dots separate distinct segments; dashes separate words within a segment.
Thread serials use **hyphen** between project code and number (`ADVI_V1VERS-004`).
Task order filenames use **dots** between every segment (`ADVI_V1VERS.004.adv-drill-cla.md`).
These are distinct and must not be conflated.

### Blocker Verification (enforce in all task orders and PRDs)

Agents must not declare BLOCKED without first checking the blocking agent's directory.
The three valid statuses are:

- **BLOCKED** — evidence found in blocking agent's logs/task_orders confirming dependency is pending
- **AMBIGUOUS** — no corroborating evidence in blocking agent's directory; route to COO/DE
- *(no blocker)* — evidence confirms dependency already delivered; agent proceeds

If a task order or session log arrives stating BLOCKED without citing the blocking
agent's log or task order path as evidence, treat it as AMBIGUOUS and investigate.
Full protocol: `org/AGENT_START_HERE.md` → Blocker Verification Protocol.

### New Project Workflow (CTO responsibility)

1. Pick or add a macro code in `org/projects/MACRO_CODES.md`
2. Choose a 6-char suffix abbreviating the initiative → project code = `{MACRO}_{6CHAR}`
3. Write the PRD in `docs/architecture/{FEATURE}.md`
4. Create `org/projects/{PROJECT_CODE}.json` with `project_code`, `macro_code`, `name`, `prds`, `status`, `phase`, `blocking`, `created`, `pods`, `pipeline`, `thread_counter: 0`, `threads: []`
5. Add a row to `org/projects/REGISTRY.md`
6. Hand off to COO with briefing

### Status Reporting Rule

When Andrew asks "where are we", "who has done what", or any status/progress question,
always refer to agents by their **full serial** (e.g., `0.4.0_DS_ClientPlatform`, not
"DS" or "the DS agent"). This applies to tables, prose, and next-steps lists. The full
serial is required so Andrew can locate the agent folder and verify directly.

### Key Paths

| Resource | Path |
|----------|------|
| Macro code registry | `org/projects/MACRO_CODES.md` |
| Project registry | `org/projects/REGISTRY.md` |
| Project JSON template | any existing `org/projects/*.json` |
| Thread system | `org/threads/README.md` |
| Thread best practices | `org/threads/THREAD_KNOWLEDGE.md` |


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

Goal: Converge on the correct visualization design for projection ghost bars (AUA/NNA/GRO) and the GRO chart redesign in PartnerAnalytics.tsx. The CTO analysis document (Section 7) poses 5 specific convergence questions that must be answered. CTO is the architectural authority (pattern consistency, data model awareness). DE knows the data contracts, Recharts API capabilities, and type system implications. RD knows implementation feasibility and visual design within Recharts constraints. IMPORTANT: There are 3 portal DEV commits AFTER the F2-fix that CTO analyzed (9ce8d3b). Commits 28517dd (filter ghost keys from tooltips), 2f84197 (projection section in tooltips), and 8e9facd (project last bar in dataset) may address some flaws. Participants MUST read the current PartnerAnalytics.tsx source to verify which flaws are still present before proposing fixes.


### 49fnv3-prd-f2-section.md

```
# PRD: AdvisorIntelligence 49Financial V3 (ADVI_49FNV3)

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-06
**Project Code:** ADVI_49FNV3
**Macro:** ADVI (AdvisorIntelligence)
**Pods:** 0.4 (ClientPlatform)
**Pipeline:** bd-pipeline

---

## 1. Context

49Financial's data team reviewed the current AdvisorIntelligence page and provided
feedback on 2026-03-05. This project addresses both outstanding fixes from YANGV2
and new features requested by 49's leadership. YANGV2 is now closed; Y14 (Books
access gating) and remaining polish items graduate into this project.

---

## 2. Scope Overview

Two categories of work, with fixes prioritized before new features:

| Category | Items | Priority |
|----------|-------|----------|
| Fixes (F1-F7) | GRO data, projected bars, Segment Analytics drilldowns, stacked advisor bar, QTD/YTD timing, Unassigned sorting, zebra striping | P0 -- address first |
| New Features (N1-N3) | Books admin dashboard, advisor drilldown, relationship drilldown | P1 -- after fixes |

---

## 3. Fixes

### F1: GRO Mode Shows No Data

**Location:** Assets Overview panel toggle in PartnerAnalytics.tsx
**Symptom:** Selecting GRO mode shows "Growth decomposition data unavailable."
**Frontend status:** Fully wired. PartnerAnalytics.tsx reads
`timeseriesData?.growth_decomposition` and renders a 3-line chart (market, NNA, total)
with colors defined (violet/blue/amber). Legend and tooltip are implemented.
**Data contract status:** Y5 added `growth_decomposition` to timeseries_chart.json.
Shape: `{ period: "YYYY-MM", market: float, nna: float, total: float }` where
`market = aua_end - aua_start - nna`.
**Probable cause:** Lambda publisher (bd-portal-publisher) is not emitting the field,
or the gold layer data feeding it is empty/missing.
**Action:** DS/DE investigation. Check bd-portal-publisher lambda_function.py for
growth_decomposition build logic. If absent, DS implements; if present but empty,
trace to gold layer source.

### F2: Projected Bars for Partial Periods

**Location:** Assets Overview panel -- AUA (NMEC/NMNC), NNA (Inflows/Outflows/Net),
and GRO views across all granularities (monthly/quarterly/annually).
**Behavior:** For the current incomplete period, display a faint ghost extension of
each bar showing the projected full-period value.
**Methodology (metric-dependent -- stock vs flow):**

  AUA is a stock (point-in-time portfolio value). NNA and GRO are flows (accumulate
  over a period). The projection formula MUST differ:

  **Flow metrics (NNA inflows, NNA outflows, GRO market/nna/total):**
  - `projected_flow = actual_flow * (total_period_days / elapsed_days)`
  - Cap: `abs(prior_period_flow) * 1.5`
  - Ghost = projected_flow - actual_flow

  **Stock metrics (AUA — NMEC, NMNC):**
  - `delta = current_value - prior_period_end_value`
  - `projected_delta = delta * (total_period_days / elapsed_days)`
  - `projected_value = prior_period_end_value + projected_delta`
  - Cap: `prior_period_end_value + abs(prior_period_change) * 1.5`
    (where `prior_period_change = prior_end - prior_start`)
  - Ghost = projected_value - current_value

  The key distinction: for AUA you extrapolate the CHANGE from prior period end,
  not the level itself. Multiplying a $1.55B stock value by a time ratio produces
  nonsensical results ($2B+ projections for a single quarter).

  **CORRECTION (2026-03-09):** The original PRD specified `actual * (total_period_days
  / elapsed_days)` uniformly for all metrics. This is only correct for flow metrics.
  For stock metrics it produces absurd projections. The formula above replaces it.

  - Apply constraint: projection capped per the formulas above. This prevents noise
    on short timelines (e.g., 2 days into a month) from producing absurd projections.
  - The ghost portion (projected minus actual) renders as a faint/translucent
    extension of the bar using the same color at reduced opacity (~20-30%).
**Applies to:**
  - AUA view: NMEC bar and NMNC bar each get ghost extensions (stock projection)
  - NNA view: Inflows bar (blue ghost), Outflows bar (red ghost), Net dash/marker (flow projection)
  - GRO view: Each of the three lines (market, NNA, total) gets a dashed extension
    to the projected value for the current period (flow projection)
**Data source:** Computation is frontend-only. The portal already has the actual
partial-period data and the prior period's completed value in the same dataset.
No Lambda/DS changes required.

### F3: Missing City-Level and Client-Level Drilldowns in Segment Analytics

**Location:** Snapshot NNA section in Segment Analytics panel (DistributionTab.tsx)
**Symptom:** City and Client drill levels are not available in the NNA segment view.
**Expected:** Clicking a state in the NNA geo donut should drill to cities within
that state. Clicking a city should drill to individual clients.
**Data contract status:** Y6b added city drill (`nna_geo_drill` in timeseries_chart.json)
and Y6d added relationship drill. Both were confirmed complete in the DS data contract.
**Action:** DE/RD investigation. The data likely exists but the frontend drill
interaction is not wired for the Snapshot NNA panel specifically. Check whether
the cumulative chart views provide the drill data and wire the click handlers.

### F4: Top Ten Advisors Stacked Bar View

**Location:** AdvisorsTab.tsx -- top ten advisors panel (architect or implementor,
depending on toggle)
**Design:**
  - Blue bar for inflows (above zero line)
  - Red bar for outflows (below zero line, same style as NNA in main header panel)
  - Gold horizontal dash showing NNA level overlaid on the bar (similar to the
    triangle markers in Peer Performance on the ModelPortfolios page)
  - Bars sorted by NNA descending (or by total AUA, confirm with Andrew)
**Data source:** `advisor_rolling_flows.json` has monthly stacked_bar data per
advisor (Y13). The leaderboard data has per-advisor NNA. May need to combine
both sources or extend the publisher to emit a top-ten stacked bar view.
**Action:** DS to confirm data shape supports inflow/outflow per advisor. DE/RD
to implement the stacked bar visualization.

### F5: QTD/YTD Timing Bug

**Location:** AdvisorsTab.tsx -- period toggle (QTD/YTD/window)
**Symptom:** In March 2026, QTD and YTD show different values. Since March is in
Q1, QTD (Jan 1 - today) and YTD (Jan 1 - today) should be identical date ranges
and produce the same numbers.
**Action:** DS + DE investigation. Check the date boundary logic in both the Lambda
publisher (server-side period computation) and the portal frontend (client-side
period filtering). One of them is computing Q1 start incorrectly or using a
different reference date.

### F6: Unassigned Implementors Sorting

**Location:** Leaderboard table in AdvisorsTab.tsx (implementor view)
**Symptom:** "Unassigned" appears ranked by NNA/AUA like a real advisor, potentially
appearing at #1 on the leaderboard.
**Expected behavior:** "Unassigned" should be pinned to the bottom of the table,
below all named advisors, same treatment as "49F House" (the firm account). It
should still be visible for transparency but should not participate in ranking.
**Action:** RD fix. Add "Unassigned" to the same exclusion list as "49F House" in
the leaderboard sort/render logic.

### F7: Zebra Striping on Leaderboard

**Location:** Leaderboard table rows in AdvisorsTab.tsx
**Symptom:** Rows have uniform background, making it hard to scan across columns.
**Expected:** Alternating row backgrounds (zebra striping) matching the pattern
used in SecurityScanner and PortfolioManagement pages.
**Action:** RD fix. Apply the same alternating row background style already used
in other pages. Likely a CSS/className addition on table rows.

---

## 4. New Features: Books Tab

### Architecture: Three-Layer Drill Hierarchy

```
Layer 1: Firm Admin Dashboard (default top-down view)
  |
  +-- Layer 2: Advisor Book View (architect or implementor drilldown)
        |
        +-- Layer 3: Relationship Detail View (individual client/household)
```

### N1: Firm Admin Dashboard (Layer 1)

**Position:** Top of Books tab, above the existing advisor summary table.
**Purpose:** Give firm leadership a top-down view of the entire book of business
using heuristic panels.

**Phase 1 panels (data exists today):**

| Panel | Data Source | Notes |
|-------|-----------|-------|
| Tax Status Breakdown | accounts_dimension `tax_status` | Donut or horizontal bar: Taxable / Tax-Deferred / Tax-Exempt with AUA amounts and percentages. Data already in `clients_tab.json` tax object. |
| AUA by Advisor (top N) | architect_leaderboard.json | Horizontal bar showing AUA concentration across architects/implementors. Data exists. |
| Account & Client Distributions | clients_tab.json headline | Total accounts, total clients (relationships), median AUA. Cards or KPI tiles. |
| Engagement Summary | clients_tab.json engagement | Net flows TTM, average relationship tenure, active clients percentage. |

**Phase 2 panels (require new pipeline work):**

| Panel | Requirement | Notes |
|-------|------------|-------|
| Firm-Level Asset Allocation | New gold layer script/table. Allocations feed has account-level market values but lacks per-security asset class tags. Need either security-level BD data with asset class enrichment, or a pre-computed allocation report from BD API. | Flag for DS/AE to investigate BD data availability. |
| Fee Revenue by Advisor | New BD pipeline feed. `income_fees` is currently zeroed in both clients_tab.json and per-advisor JSONs ("not available from BD data"). BD has this data; needs new ingestion pipeline, dim table, backfill, and gold layer integration. | Flag for AE to scope BD API endpoint for fee data. |

### N2: Advisor Book View (Layer 2)

**Trigger:** Click an advisor row in the firm dashboard or the existing advisor
summary table.
**Content:** Relationship-level aggregate for the selected advisor (architect or
implementor). This is a drilldown of the Layer 1 firm view, scoped to one advisor.

**Panels:**
- Advisor's tax status breakdown (same donut as firm, filtered to this advisor)
- Advisor's client list with AUA (already exists in per-advisor JSONs: `clients` array)
- Advisor's NNA and engagement metrics (already in per-advisor JSONs: `nna`, `engagement`)
- Advisor's AUA trend over time (if timeseries data exists per advisor)

**Data source:** Per-advisor JSONs from bd-portal-advisor-publisher. The data
contract (Source 7) confirms these exist with tax, engagement, and clients fields.

### N3: Relationship Detail View (Layer 3)

**Trigger:** Click a relationship/client row in the advisor book view.
**Content:** Individual relationship-level drilldown showing that household's
accounts, positions, and activity.

**Data availability:** This may require extending the publisher to emit
per-relationship detail JSONs, or it may already exist in the ClientDetail
components (portal has `AdvisorIntelligence/ClientDetail/` directory with
PortfolioBalancePanel and TimeSeriesPanel). Needs DE/DS investigation to
confirm data coverage.

### N4: Y14 Access Gating (Deferred)

**From YANGV2:** Books tab advisor-scoped access via partner identity DynamoDB
table + JWT authorizer context. Auth chain is deployed (J1/J2/J3 verified).
Not a Phase 1 priority -- focus is getting data and interface structure complete
first. Will be addressed when the Books tab is ready for external advisor access.

---

## 5. Agents & Responsibilities

| Agent | Role |
|-------|------|
| 0.4.0_DS_ClientPlatform | F1 investigation (GRO data), F5 investigation (QTD/YTD), Books tab data extensions, Phase 2 data scoping |
| 0.4.0_DE_ClientPlatform | F3 wiring, F4 data shape confirmation, F5 investigation, Books tab component architecture, data contract updates |
| 0.4.2_RD_AdvisorIntelligence | F2 (projected bars), F4 (stacked bar viz), F6 (Unassigned sorting), F7 (zebra striping), N1-N3 (Books UI) |
| 0.4.0_DT_ClientPlatform | Lambda deploys, EC2 diagnostic runs, portal push |
| 0.6.0_AE_PartnerETL | Phase 2: BD API investigation for fee data and asset class data |

---

## 6. Phasing

| Phase | Scope | Blocking |
|-------|-------|----------|
| Phase 1a | Fixes F1-F7 | F1 blocks GRO projected bars in F2. F5 may block Advisors tab correctness. Others independent. |
| Phase 1b | Books tab Layer 1 (firm dashboard with Phase 1 panels) + Layer 2 (advisor drilldown) | Data exists today. Requires DE component architecture + RD implementation. |
| Phase 2a | Layer 3 (relationship detail) + Y14 access gating | Needs DE/DS investigation on data availability for per-relationship views. |
| Phase 2b | Firm-level asset allocation panel + fee revenue panel | Requires new BD pipeline feeds. AE scopes. |

---

## 7. Success Criteria

| Criterion | Target |
|-----------|--------|
| F1: GRO mode | Shows 3-line chart with real data |
| F2: Projected bars | Ghost bars visible for current partial period in all views, capped at 1.5x prior |
| F3: Segment drilldowns | City and client levels accessible from Snapshot NNA |
| F4: Stacked advisor bar | Blue inflows / red outflows / gold NNA dash for top 10 advisors |
| F5: QTD/YTD | Identical values when QTD period equals YTD period |
| F6: Unassigned | Pinned to bottom of leaderboard |
| F7: Zebra striping | Alternating row backgrounds on leaderboard |
| N1: Firm dashboard | Tax breakdown, AUA by advisor, account/client distributions, engagement visible |
| N2: Advisor drilldown | Click advisor -> see their book with tax, clients, NNA, engagement |

---

## 8. Risks

| Risk | Mitigation |
|------|-----------|
| F1 root cause unknown (Lambda vs gold layer vs data) | DS investigation first; do not attempt frontend fixes |
| F2 projection cap may feel arbitrary at 1.5x | Start with 1.5x, adjust based on Andrew/Yang feedback after seeing it live |
| F5 timing bug may be systemic (affect other period calculations) | Investigation should audit all period boundary computations, not just QTD/YTD |
| Books Layer 3 may need new publisher output | Phase 2a scoping will determine; existing ClientDetail components may partially cover this |
| Fee/asset allocation data not in current BD pipeline | Explicitly Phase 2; does not block Books tab launch |
```

### advisorintelligence-typescript-types.ts

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

// Single data point for cumulative chart
export interface CumulativeChartDataPoint {
  date: string
  [category: string]: string | number  // Dynamic categories (NMNC, NMEC, TX, etc.)
}

// View data for cumulative chart
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
  aua: CumulativeChartView   // Cumulative NNA by client cohort
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
export type ChartWindowOption = '3M' | '6M' | '1Y' | '2Y' | '3Y' | 'Max'

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

// Time period keys for time machine
export type TimePeriodKey = 'current' | 'q1' | 'q2' | 'q3'

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

// Single view with multiple period snapshots
export interface PartnerAnalyticsViewWithPeriods {
  current: PeriodSnapshot
  q1?: PeriodSnapshot          // Last quarter (e.g., "Q4 '25")
  q2?: PeriodSnapshot          // 2 quarters ago (e.g., "Q3 '25")
  q3?: PeriodSnapshot          // 3 quarters ago (e.g., "Q2 '25")
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

// All periods metadata
export interface PeriodsMetadata {
  current: PeriodDefinition
  q1: PeriodDefinition
  q2: PeriodDefinition
  q3: PeriodDefinition
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
  period: 'q1' | 'q2' | 'q3'
): PeriodSnapshot | undefined {
  if (hasTimeMachine(view)) {
    return view[period]
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
  quantity: number
  cost_basis: number
  market_value: number
  unrealized_gain: number
  term: string
  acquisition_date?: string
}
```

### cto-f2-visualization-analysis-primary----contains-all-4-flaws--5-convergence-questions.md

```
# F2 Projection Visualization Analysis — Assets Overview Panel

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-09
**Project:** ADVI_49FNV3
**For:** Thread context injection — COO orchestrates CTO + DE + RD convergence

---

## 1. What This Document Is

Andrew reviewed the F2 projected ghost bars implementation (portal DEV commit `594c3f6`,
fix commit `9ce8d3b`) and identified fundamental issues with how projections are computed,
displayed, and explained to the user. This document catalogs every flaw found in the
2026-03-09 CTO review session so the thread participants can converge on a correct design.

---

## 2. Current Architecture of Assets Overview

The Assets Overview panel in PartnerAnalytics.tsx has three view modes, toggled by
[AUA] [NNA] [GRO] buttons:

| View | Chart Type | Data Source | What It Shows |
|------|-----------|-------------|---------------|
| AUA | BarChart (stacked) | timeseries_chart.json `.aua` | Point-in-time portfolio value, split by NMEC (new clients) / NMNC (existing clients) |
| NNA | ComposedChart (diverging bar + line) | timeseries_chart.json `.nna` | Period flows: blue inflows above zero, red outflows below, gold net line |
| GRO | ComposedChart (3 lines) | timeseries_chart.json `.growth_decomposition` | Monthly AUA delta decomposed into Market + NNA = Total |

All three views share:
- Granularity toggle: Monthly / Quarterly / Annually
- Time window: 1Y / 3Y / Max
- Click-to-select a bar for breakdown table filtering (AUA/NNA only)
- Period-over-period growth in tooltips (AUA/NNA only)
- Hero metrics below chart (AUA: total + growth, NNA: inflows/outflows/net + growth)
- Footnote explaining the chart

F2 added ghost/projection extensions to all three views for the current incomplete period.

---

## 3. Flaw 1: AUA Projection Uses Wrong Formula (FIXED — verify 0/0 regression)

### Original bug (now patched by 9ce8d3b)
The original code did `projected = actual * ratio` where `actual` is AUA (a stock value,
e.g. $1.55B) and `ratio = totalDays / elapsedDays`. This is only valid for flow metrics.
For AUA, it produces absurd results: $1.55B * 1.5 = $2.325B.

### Fix applied
Commit `9ce8d3b` changed to delta-based extrapolation:
```
delta = actual - priorEnd
projectedDelta = delta * ratio
projectedValue = priorEnd + projectedDelta
ghost = max(0, cappedValue - actual)
```

### New problem: 0/0 projections
Andrew reports both NMEC and NMNC projections now show 0. Likely causes:

**Cause A — No prior period in windowed data.** `aggregatedAuaData` is filtered by
`timeWindowCutoff` (line 212-213) before aggregation. If the current period is `idx === 0`
in the filtered array, `prior === null`, `priorEnd === actual`, `delta === 0`, ghost = 0.
This happens when:
- Granularity = Annually and Window = 1Y (only 2026 visible)
- Granularity = Quarterly and Window = 1Y (Q1 2025 may be partial/missing)

**Cause B — Period already complete.** Line 455: `if (elapsedDays >= totalDays) return aug`.
If the last data point in the period is dated at or past the period end (e.g., publisher
wrote March 31 data), the period is treated as complete and no ghost is generated.

**Fix needed:** When `prior === null`, the code should either:
- Skip the ghost (don't show projection when there's no reference point) — honest
- Look back further in the raw data for a prior period end value — robust
- At minimum, not silently produce 0/0 with no user feedback

The thread should decide which approach is correct.

---

## 4. Flaw 2: GRO Chart Is Unintelligible

### What GRO shows
Monthly AUA change decomposed into two drivers:
- **Market**: AUA change from market price movement (appreciation/depreciation)
- **NNA**: AUA change from net new asset flows (money in minus money out)
- **Total**: Market + NNA = actual AUA change for the period

### What's wrong

**4a. No header or context.** The chart area has no title or subtitle explaining what
the user is looking at. The only explanation is a footnote at the very bottom:
`"Market = AUA change from market movement. NNA = net new assets from client flows."` —
most users won't read this.

**4b. Legend labels are too terse.** The legend shows `Market`, `NNA`, `Total` with
small colored line swatches. A user unfamiliar with the decomposition has no idea what
these mean. Compare to the NNA view which uses `Inflows`, `Outflows`, `Net Flow` —
concrete, action-oriented labels.

**4c. Tooltip dumps raw values with no context.** The GRO tooltip (line 1533-1553)
iterates `payload.map()` and shows:
```
Mar '26
Market    $45M
NNA       $12M
Total     $57M
```
No explanation of what Market or NNA means. No sign indication (+ or -). No
period-over-period comparison (unlike AUA and NNA tooltips which show MoM/QoQ growth).
No indication of whether this is good or bad.

**4d. Projection lines leak into tooltip.** The dashed projection lines (`market_proj`,
`nna_proj`, `total_proj`) are rendered as separate Recharts `<Line>` series with
`legendType="none"`. But the tooltip iterates ALL payload entries, so when hovering
the projected point, it shows 6 entries: Market, NNA, Total, market_proj, nna_proj,
total_proj. The `_proj` entries have no display name and look like duplicates.

**4e. No hero metrics.** AUA view has hero metrics below the chart (total AUA, growth %,
growth $). NNA view has hero metrics (inflows, outflows, net). GRO view has nothing —
just the chart and footnote. There's no at-a-glance summary of the decomposition.

**4f. Y-axis units unclear.** The Y-axis shows raw dollar values ($0, $50M, $100M) but
doesn't label whether these are absolute AUA values or period deltas. They're period
deltas — "this month the market added $45M" — but nothing says that.

---

## 5. Flaw 3: NNA Tooltip Projection Display

The NNA tooltip (line 1326-1351) does show projections for the current period, but the
presentation is confusing:

```
Projected
  Inflows (add)    +$50M
  Outflows (add)   -$30M
  Projected Net    +$83M
```

"Inflows (add)" shows the GHOST INCREMENT (projected minus actual), not the full
projected value. The user sees their actual inflow is $50M and the projection "adds"
$50M, but they have to do the mental math to get projected inflow = $100M. The AUA
tooltip has the same pattern — shows ghost increments labeled "(add)".

Better approach: show the full projected values clearly:
```
Projected Full Period
  Inflows     +$100M    (currently $50M)
  Outflows    -$60M     (currently $30M)
  Net         +$40M     (currently $20M)
```

---

## 6. Existing Chart Patterns Across AdvisorIntelligence (Reference for Thread)

### Tooltip patterns already established

| View | Tooltip Content | Period Comparison | Projection |
|------|----------------|-------------------|------------|
| AUA (PartnerAnalytics) | Total AUA + per-category breakdown + MoM/QoQ/YoY growth $ and % | Yes | Ghost increment "(add)" + projected total |
| NNA (PartnerAnalytics) | Inflows/Outflows/Net + MoM/QoQ/YoY change | Yes | Ghost increment "(add)" + projected net |
| GRO (PartnerAnalytics) | Raw Market/NNA/Total values only | No | Dashed lines, no tooltip handling |
| NNA Diverging (DistributionTab continuous) | Inflows/Outflows/Net NNA per period | No | None |
| CLA Stacked Area (DistributionTab continuous) | Category breakdown + total | No | None |
| AUA Stacked Area (DistributionTab continuous) | Category breakdown + growth | No | None |
| Top Ten Stacked Bar (AdvisorsTab) | Per-advisor inflow/outflow/NNA | No | None |
| Leaderboard (AdvisorsTab) | Tabular — no chart tooltip | N/A | None |

### Hero metric patterns

| View | Hero Metrics |
|------|-------------|
| AUA | Total AUA, Growth $, Growth %, comparison label |
| NNA (gross) | Inflows, Outflows, Net Flow — each with growth $ and % |
| NNA (net only) | Net New Assets with growth $ and % |
| GRO | NONE — no hero metrics |

### Chart type patterns

| Pattern | Used In |
|---------|---------|
| Stacked BarChart | AUA (PartnerAnalytics), AUA continuous (DistributionTab) |
| Diverging ComposedChart (bar+line) | NNA (PartnerAnalytics), NNA continuous (DistributionTab) |
| Multi-line ComposedChart | GRO (PartnerAnalytics) |
| Stacked AreaChart | AUA/CLA continuous (DistributionTab) |
| Donut (ApexCharts) | Snapshot distribution (DistributionTab) |
| Bell curve histogram | Snapshot distribution (DistributionTab) |

### Projection patterns

| Pattern | Used In |
|---------|---------|
| Ghost bar (translucent stacked extension, 25% opacity) | AUA bars, NNA inflow/outflow bars |
| Dashed line extension | GRO market/nna/total lines |
| None | All DistributionTab views, AdvisorsTab views |

---

## 7. Questions for the Thread to Converge On

1. **AUA projection 0/0 fix:** When there's no prior period in the windowed data, what
   should happen? Options: (a) no ghost shown, (b) fall back to raw daily data for a prior
   reference, (c) show a "projection unavailable" indicator.

2. **GRO chart redesign:** Should GRO be a multi-line chart or something else? Options:
   (a) keep 3 lines but add hero metrics + better tooltip + Y-axis label, (b) convert to
   diverging bar chart matching NNA pattern (Market above zero, NNA below zero, Total as
   line), (c) convert to stacked bar (Market + NNA = Total per period), (d) something else.

3. **Projection tooltip format:** Should projections show (a) ghost increments with
   "(add)" labels (current), (b) full projected values with current values parenthetical,
   (c) both actual and projected as separate clearly-labeled rows?

4. **GRO tooltip:** Should it (a) follow the NNA tooltip pattern (structured rows with
   sign coloring), (b) include period-over-period comparison like AUA/NNA, (c) show
   projection for current period, (d) all of the above?

5. **GRO hero metrics:** What metrics should appear below the chart? Candidates:
   latest period Market $, latest period NNA $, latest period Total $, cumulative over
   window, growth rate.

---

## 8. RD Recent Work (Thread Context)

### Portal DEV commits (2026-03-09):
- `594c3f6` — F2/F4/N1-N2 visual implementation (ghost bars, stacked bar top 10, Books)
- `9ce8d3b` — F2-fix: AUA projection delta-based extrapolation

### Portal DEV commits (2026-03-04, prior session):
- Y1+Y4+Y6+Y12 visual fixes
- Y8 AUA continuous stacked bar (uncommitted)
- ADVI-005 4C stacked bar (per-advisor inflows/outflows)
- DistributionTab C1-C4 (GEO continuous, ADV drill, CLA snapshot/continuous)

### RD session log:
`org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/2026-03-09/ADVI_49FNV3_F2_F4_F6_F7_N1N2.md`

### Key RD constraint:
0.4.2_RD_AdvisorIntelligence works only within their page scope (AdvisorIntelligence).
They can reference patterns from other pages but cannot modify them. All Recharts
components are available (Bar, Line, Area, ComposedChart, etc.). ApexCharts is lazy-loaded
for donuts only.
```

### partneranalytics.tsx----assets-overview-panel-auannagro-views--projection-logic.tsx

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
import { AreaChart, Area, BarChart, Bar, Cell, ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { Panel, PanelHeader, PanelContent, PanelFooter } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { Tooltip } from '@/components/Tooltip'
import { HelpCircle } from 'lucide-react'
import { formatCurrency } from '@/lib/universalNumberFormatter'
import type { PartnerAnalyticsResponse, PartnerAnalyticsViewMode, DistributionStats, DonutSegment, CitySegment, ClientSegment, TimePeriodKey, PeriodSnapshot, PartnerAnalyticsViewWithPeriods, PartnerAnalyticsView, CumulativeChartResponse, GrowthDecompositionPoint } from '../types'
import { hasTimeMachine } from '../types'
import { getCumulativeChart } from '@/api/endpoints/advisor-intelligence'
import { useSelectTracking } from '@/hooks/useFilterTracking'

// Granularity options for bar charts (Monthly | Quarterly | Annually)
type GranularityOption = 'monthly' | 'quarterly' | 'annually'

// Panel view mode: AUA (stacked bar), NNA (diverging bar), GRO (growth decomposition lines)
type PanelViewMode = 'aua' | 'nna' | 'gro'

// AUA sub-mode: Clients (NMNC/NMEC) or Mix (asset class breakdown)
type AuaSubMode = 'clients' | 'mix'

// Y3-FE: AUA sub-mode label — placeholder pending Andrew/Yang decision
const AUA_SUB_MODE_CLIENTS_LABEL = 'Clients'

// Time window for chart data
type TimeWindow = '1Y' | '3Y' | 'Max'

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

// Y5-FE: GRO growth decomposition line colors
const GRO_COLORS = {
  market: '#8B5CF6',  // Violet — Market Performance
  nna: '#2196F3',     // Blue — NNA (reuse existing NNA color)
  total: '#F59E0B',   // Amber — Total AUA Change
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

interface PartnerAnalyticsProps {
  data: PartnerAnalyticsResponse | null
  isLoading: boolean
  selectedFirmId: string
  onPartnerChange: (firmId: string) => void
  granularity: GranularityOption
  onGranularityChange: (g: GranularityOption) => void
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

export function PartnerAnalytics({ data, isLoading, selectedFirmId, onPartnerChange, granularity, onGranularityChange }: PartnerAnalyticsProps) {
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

  // Time window: 1Y, 3Y, Max
  const [timeWindow, setTimeWindow] = useState<TimeWindow>('3Y')

  // Bar Chart state with analytics tracking for granularity
  // granularity is controlled from AdvisorIntelligence.tsx (drives the query re-fetch)
  const [selectedBarPeriod, setSelectedBarPeriod] = useState<string | null>(null) // Selected bar period key (e.g., "2023-Q1")

  // Shared/cached timeseries query to avoid duplicate network fetches across tabs/components
  const { data: timeseriesData, isLoading: timeseriesLoading } = useQuery<CumulativeChartResponse>({
    queryKey: ['advisor-intelligence', 'cumulative-chart'],
    queryFn: () => getCumulativeChart(),
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
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

  // Aggregate daily AUA data to monthly/quarterly/annually for stacked bar chart
  const aggregatedAuaData = useMemo(() => {
    if (!timeseriesData?.aua?.data) return []

    const allData = timeseriesData.aua.data
    const dailyData = timeWindowCutoff
      ? allData.filter(p => new Date(String(p.date) + 'T12:00:00') >= timeWindowCutoff)
      : allData
    const categories = timeseriesData.aua.categories || []
    if (dailyData.length === 0 || categories.length === 0) return []

    // Group by period
    const periodMap = new Map<string, { period: string; label: string; endDate: string; [key: string]: number | string }>()

    dailyData.forEach((point) => {
      const date = new Date(point.date + 'T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      // For cumulative data, we want the latest value in each period (end of period snapshot)
      const existing = periodMap.get(periodKey) || { period: periodKey, label: periodLabel, endDate: point.date }

      categories.forEach((cat) => {
        existing[cat] = Number(point[cat]) || 0
      })
      existing.endDate = point.date

      periodMap.set(periodKey, existing)
    })

    return Array.from(periodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

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
      const periodInflows  = entry.lastInflows  - prevInflows
      const periodOutflows = entry.lastOutflows - prevOutflows

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

  // Y3-FE: Aggregate aua_mix data (asset class breakdown) by period
  const aggregatedMixData = useMemo(() => {
    const mixView = timeseriesData?.aua_mix
    if (!mixView?.data || mixView.data.length === 0) return []

    const categories = mixView.categories || []
    const mixData = timeWindowCutoff
      ? mixView.data.filter(p => new Date(p.period + '-01T12:00:00') >= timeWindowCutoff)
      : mixView.data

    if (mixData.length === 0) return []

    // aua_mix data is monthly. Aggregate to quarter/year when needed.
    const periodMap = new Map<string, { period: string; label: string; [k: string]: number | string }>()

    mixData.forEach((point) => {
      const date = new Date(point.period + '-01T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      // For cumulative AUA mix, take end-of-period snapshot (last month in the period)
      const entry: { period: string; label: string; [k: string]: number | string } = { period: periodKey, label: periodLabel }
      point.segments.forEach(seg => {
        entry[seg.label] = seg.value
      })
      periodMap.set(periodKey, entry)
    })

    return Array.from(periodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // Y3-FE: Categories for the Mix stacked bar
  const mixCategories = useMemo(() => {
    return timeseriesData?.aua_mix?.categories || []
  }, [timeseriesData])

  // Y5-FE: Aggregate growth_decomposition data by period
  const aggregatedGroData = useMemo(() => {
    const groView = timeseriesData?.growth_decomposition
    if (!groView?.data || groView.data.length === 0) return []

    const groData = timeWindowCutoff
      ? groView.data.filter(p => new Date(p.period + '-01T12:00:00') >= timeWindowCutoff)
      : groView.data

    if (groData.length === 0) return []

    // GRO data is monthly. For quarterly/annually, SUM values (not snapshot).
    const periodMap = new Map<string, { period: string; label: string; market: number; nna: number; total: number }>()

    groData.forEach((point: GrowthDecompositionPoint) => {
      const date = new Date(point.period + '-01T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      const existing = periodMap.get(periodKey) || { period: periodKey, label: periodLabel, market: 0, nna: 0, total: 0 }
      existing.market += point.market
      existing.nna += point.nna
      existing.total += point.total
      periodMap.set(periodKey, existing)
    })

    return Array.from(periodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // ============================================================================
  // F2: Projected ghost bars for the current incomplete period
  // ============================================================================

  const currentPeriodKey = useMemo(() => {
    return getPeriodInfo(new Date()).periodKey
  }, [getPeriodInfo])

  // Compute total and elapsed days for a given period
  function computePeriodDays(g: GranularityOption, periodKey: string): { totalDays: number; elapsedDays: number } {
    const now = new Date()
    if (g === 'monthly') {
      const [y, m] = periodKey.split('-').map(Number)
      const start = new Date(y, m - 1, 1)
      const end = new Date(y, m, 0)
      return {
        totalDays: end.getDate(),
        elapsedDays: Math.max(1, Math.floor((now.getTime() - start.getTime()) / 86400000)),
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
        elapsedDays: Math.max(1, Math.floor((now.getTime() - start.getTime()) / 86400000)),
      }
    } else {
      const y = Number(periodKey)
      const start = new Date(y, 0, 1)
      const end = new Date(y, 11, 31)
      return {
        totalDays: Math.floor((end.getTime() - start.getTime()) / 86400000) + 1,
        elapsedDays: Math.max(1, Math.floor((now.getTime() - start.getTime()) / 86400000)),
      }
    }
  }

  // AUA: add ghost extension fields for the most recent incomplete period
  const augmentedAuaData = useMemo(() => {
    if (aggregatedAuaData.length === 0) return aggregatedAuaData
    const cats = timeseriesData?.aua?.categories || []
    const lastIdx = aggregatedAuaData.length - 1
    return aggregatedAuaData.map((entry, idx) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aug = { ...entry } as any
      cats.forEach(cat => { aug[`${cat}_ghost`] = 0 })

      // Only project the last bar (most recent period with data)
      if (idx !== lastIdx) return aug

      const { totalDays, elapsedDays } = computePeriodDays(granularity, entry.period)
      if (elapsedDays >= totalDays) return aug

      const prior = idx > 0 ? aggregatedAuaData[idx - 1] : null
      const ratio = totalDays / elapsedDays

      const priorPrior = idx > 1 ? aggregatedAuaData[idx - 2] : null

      cats.forEach(cat => {
        const actual = Number(entry[cat]) || 0
        const priorEnd = prior ? (Number((prior as Record<string, unknown>)[cat]) || 0) : actual
        const delta = actual - priorEnd
        const projectedDelta = delta * ratio
        const projectedValue = priorEnd + projectedDelta

        // Cap: use prior period's change magnitude if available, else current delta
        const priorPriorVal = priorPrior ? (Number((priorPrior as Record<string, unknown>)[cat]) || 0) : priorEnd
        const priorPeriodChange = Math.abs(priorEnd - priorPriorVal)
        const capDelta = (priorPrior ? priorPeriodChange : Math.abs(delta)) * 1.5
        const cappedValue = Math.min(projectedValue, priorEnd + capDelta)

        aug[`${cat}_ghost`] = Math.max(0, cappedValue - actual)
      })

      return aug
    })
  }, [aggregatedAuaData, granularity, timeseriesData])

  // NNA: add ghost extension fields for the most recent incomplete period
  const augmentedNnaData = useMemo(() => {
    if (aggregatedNnaData.length === 0) return aggregatedNnaData
    const lastNnaIdx = aggregatedNnaData.length - 1
    return aggregatedNnaData.map((entry, idx) => {
      const aug = { ...entry, inflow_ghost: 0, outflow_ghost: 0 }

      if (idx !== lastNnaIdx) return aug

      const { totalDays, elapsedDays } = computePeriodDays(granularity, entry.period)
      if (elapsedDays >= totalDays) return aug

      const prior = idx > 0 ? aggregatedNnaData[idx - 1] : null
      const ratio = totalDays / elapsedDays

      // Inflows (positive)
      const projInflow = entry.inflow * ratio
      const priorInflow = prior ? prior.inflow : entry.inflow
      const capInflow = Math.abs(priorInflow) * 1.5
      aug.inflow_ghost = Math.max(0, Math.min(projInflow, capInflow) - entry.inflow)

      // Outflows (negative) — ghost extends further negative
      const projOutflow = entry.outflow * ratio
      const priorOutflow = prior ? prior.outflow : entry.outflow
      const capOutflow = -Math.abs(priorOutflow) * 1.5
      aug.outflow_ghost = Math.min(0, Math.max(projOutflow, capOutflow) - entry.outflow)

      return aug
    })
  }, [aggregatedNnaData, granularity])

  // GRO: add dashed projection point for the most recent incomplete period
  const augmentedGroData = useMemo(() => {
    if (aggregatedGroData.length === 0) return aggregatedGroData
    const lastIdx = aggregatedGroData.length - 1
    const last = aggregatedGroData[lastIdx]

    const { totalDays, elapsedDays } = computePeriodDays(granularity, last.period)
    if (elapsedDays >= totalDays) return aggregatedGroData

    const prior = lastIdx > 0 ? aggregatedGroData[lastIdx - 1] : null
    const ratio = totalDays / elapsedDays

    const project = (actual: number, priorVal: number | undefined) => {
      const projected = actual * ratio
      const cap = Math.abs(priorVal ?? actual) * 1.5
      if (actual >= 0) return Math.min(projected, cap)
      return Math.max(projected, -cap)
    }

    const projectedPoint = {
      period: last.period + '_proj',
      label: last.label,
      market: project(last.market, prior?.market),
      nna: project(last.nna, prior?.nna),
      total: project(last.total, prior?.total),
      _isProjection: true,
    }

    // Mark the last actual point for dashed line rendering
    const markedLast = { ...last, market_proj: last.market, nna_proj: last.nna, total_proj: last.total }
    const markedProj = { ...projectedPoint, market_proj: projectedPoint.market, nna_proj: projectedPoint.nna, total_proj: projectedPoint.total }

    return [
      ...aggregatedGroData.slice(0, lastIdx).map(d => ({ ...d, market_proj: null as number | null, nna_proj: null as number | null, total_proj: null as number | null })),
      markedLast,
      markedProj,
    ]
  }, [aggregatedGroData, granularity])

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
  const barCategories = timeseriesData?.aua?.categories || []

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
              onClick={() => { setTimeWindow(opt); setSelectedBarPeriod(null); }}
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
                    />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null

                        // Separate actual vs ghost (projection) entries
                        const actualPayload = payload.filter(entry => !String(entry.dataKey).endsWith('_ghost'))
                        const ghostPayload = payload.filter(entry => String(entry.dataKey).endsWith('_ghost'))
                        const total = actualPayload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                        const sortedPayload = [...actualPayload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
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

                        // Projection totals for current period
                        const hasProjections = isCurrentPeriod && ghostPayload.some(e => (Number(e.value) || 0) > 0)
                        const projectedTotal = hasProjections ? total + ghostPayload.reduce((sum, e) => sum + (Number(e.value) || 0), 0) : 0

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
                                <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected</div>
                                {ghostPayload
                                  .filter(e => (Number(e.value) || 0) > 0)
                                  .sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                                  .map((entry, index) => {
                                    const catName = String(entry.dataKey).replace('_ghost', '')
                                    return (
                                      <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                        <span className="text-white/50">
                                          {getBarCategoryDisplayName(catName)} (add)
                                        </span>
                                        <span className="text-white/60 font-medium">
                                          +{formatCurrency(Number(entry.value) || 0)}
                                        </span>
                                      </div>
                                    )
                                  })}
                                <div className="flex items-center justify-between gap-4 text-xs border-t border-white/5 pt-1">
                                  <span className="text-white/50 font-medium">Projected Total</span>
                                  <span className="text-white/60 font-semibold">
                                    {formatCurrency(projectedTotal)}
                                  </span>
                                </div>
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
                    {/* F2: Ghost bar extensions for projected current period */}
                    {[...barCategories].reverse().map((cat, idx) => {
                      const baseColor = getBarCategoryColor(cat, idx)
                      const isLastCategory = idx === barCategories.length - 1
                      return (
                        <Bar
                          key={`${cat}_ghost`}
                          dataKey={`${cat}_ghost`}
                          stackId="aua"
                          fill={baseColor}
                          fillOpacity={0.25}
                          radius={isLastCategory ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                          isAnimationActive={false}
                        />
                      )
                    })}
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
                        const periodData = payload[0]?.payload as { inflow: number; outflow: number; net: number; period: string; inflow_ghost: number; outflow_ghost: number }
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
                                    <span className="text-white/70 font-medium">Net Flow</span>
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
                            {isCurrentNnaPeriod && ((periodData?.inflow_ghost || 0) > 0 || (periodData?.outflow_ghost || 0) > 0) && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected</div>
                                {(periodData?.inflow_ghost || 0) > 0 && (
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50">Inflows (add)</span>
                                    <span className="text-white/60 font-medium">+{formatCurrency(periodData.inflow_ghost)}</span>
                                  </div>
                                )}
                                {(periodData?.outflow_ghost || 0) > 0 && (
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50">Outflows (add)</span>
                                    <span className="text-white/60 font-medium">-{formatCurrency(periodData.outflow_ghost)}</span>
                                  </div>
                                )}
                                <div className="flex items-center justify-between gap-4 text-xs border-t border-white/5 pt-1">
                                  <span className="text-white/50 font-medium">Projected Net</span>
                                  <span className="text-white/60 font-semibold">
                                    {formatCurrency(
                                      (periodData.inflow + (periodData.inflow_ghost || 0)) +
                                      (periodData.outflow - (periodData.outflow_ghost || 0))
                                    )}
                                  </span>
                                </div>
                              </div>
                            )}
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
                        {/* F2: Ghost bar extensions for projected current period */}
                        <Bar dataKey="inflow_ghost" stackId="nna" fill={NNA_COLORS.inflow} fillOpacity={0.25} radius={[4, 4, 0, 0]} isAnimationActive={false} />
                        <Bar dataKey="outflow_ghost" stackId="nna" fill={NNA_COLORS.outflow} fillOpacity={0.25} radius={[0, 0, 4, 4]} isAnimationActive={false} />
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
                  </ComposedChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' && aggregatedMixData.length > 0 && mixCategories.length > 0 ? (
                /* Y3-FE: AUA Mix Stacked Bar Chart (asset class breakdown) */
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={aggregatedMixData}
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
                      tickFormatter={(value) => {
                        if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`
                        if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                    />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null
                        // Filter out ghost keys from tooltip display
                        const visiblePayload = payload.filter(entry => !String(entry.dataKey).endsWith('_ghost'))
                        const total = visiblePayload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                        const sortedPayload = [...visiblePayload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                        return (
                          <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                            <div className="text-white font-bold text-sm mb-2">{label}</div>
                            <div className="flex items-center justify-between gap-6 mb-2">
                              <span className="text-white/70 text-sm">Total AUA</span>
                              <span className="text-white font-semibold text-sm">{formatCurrency(total)}</span>
                            </div>
                            <div className="space-y-1.5 border-t border-white/10 pt-2">
                              {sortedPayload.map((entry, index) => (
                                <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                  <div className="flex items-center gap-2">
                                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }} />
                                    <span className="text-white/70">{String(entry.dataKey)}</span>
                                  </div>
                                  <span className="text-white font-medium">{formatCurrency(Number(entry.value) || 0)}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )
                      }}
                    />
                    {[...mixCategories].reverse().map((cat, idx) => {
                      const color = getAssetClassColor(cat, idx)
                      const isLast = idx === mixCategories.length - 1
                      return (
                        <Bar
                          key={cat}
                          dataKey={cat}
                          stackId="mix"
                          fill={color}
                          fillOpacity={0.85}
                          radius={isLast ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                        />
                      )
                    })}
                  </BarChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                /* Y3-FE: Mix data unavailable */
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">Asset class mix data unavailable</p>
                </div>
              ) : panelViewMode === 'gro' && augmentedGroData.length > 0 ? (
                /* Y5-FE: GRO Growth Decomposition 3-Line Chart */
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={augmentedGroData}
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
                      tickFormatter={(value) => {
                        if (Math.abs(value) >= 1e9) return `${value < 0 ? '-' : ''}$${(Math.abs(value) / 1e9).toFixed(1)}B`
                        if (Math.abs(value) >= 1e6) return `${value < 0 ? '-' : ''}$${(Math.abs(value) / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                    />
                    <ReferenceLine y={0} stroke="rgba(255,255,255,0.15)" strokeDasharray="3 3" />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null
                        return (
                          <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                            <div className="text-white font-bold text-sm mb-2">{label}</div>
                            <div className="space-y-1.5">
                              {payload.map((entry, index) => (
                                <div key={index} className="flex items-center justify-between gap-6 text-xs">
                                  <div className="flex items-center gap-2">
                                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: entry.color as string }} />
                                    <span className="text-white/70">{String(entry.name)}</span>
                                  </div>
                                  <span className="text-white font-medium">{formatCurrency(Number(entry.value) || 0)}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )
                      }}
                    />
                    <Line type="monotone" dataKey="market" name="Market" stroke={GRO_COLORS.market} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="nna" name="NNA" stroke={GRO_COLORS.nna} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="total" name="Total" stroke={GRO_COLORS.total} strokeWidth={2} dot={false} />
                    {/* F2: Dashed projection lines for current incomplete period */}
                    <Line type="monotone" dataKey="market_proj" stroke={GRO_COLORS.market} strokeWidth={2} strokeDasharray="6 3" dot={false} connectNulls={false} isAnimationActive={false} legendType="none" />
                    <Line type="monotone" dataKey="nna_proj" stroke={GRO_COLORS.nna} strokeWidth={2} strokeDasharray="6 3" dot={false} connectNulls={false} isAnimationActive={false} legendType="none" />
                    <Line type="monotone" dataKey="total_proj" stroke={GRO_COLORS.total} strokeWidth={2} strokeDasharray="6 3" dot={false} connectNulls={false} isAnimationActive={false} legendType="none" />
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
                mixCategories.map((cat, idx) => (
                  <div key={cat} className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: getAssetClassColor(cat, idx) }} />
                    <span className="text-xs text-white/70">{cat}</span>
                  </div>
                ))
              ) : panelViewMode === 'gro' ? (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.market }} />
                    <span className="text-xs text-white/70">Market</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.nna }} />
                    <span className="text-xs text-white/70">NNA</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.total }} />
                    <span className="text-xs text-white/70">Total</span>
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
              const findComparablePriorSnapshot = (
                dailyData: Array<Record<string, unknown>>,
                currentPeriodKey: string,
                priorPeriodKey: string,
                isCurrentPeriodInProgress: boolean
              ): { point: Record<string, unknown>; daysCompared: number } | null => {
                if (!isCurrentPeriodInProgress) {
                  // Completed period: use end-of-period (last data point in prior period)
                  const priorPoints = dailyData.filter(p => {
                    const d = new Date(String(p.date) + 'T12:00:00')
                    return getPeriodInfo(d).periodKey === priorPeriodKey
                  })
                  if (priorPoints.length === 0) return null
                  return { point: priorPoints[priorPoints.length - 1], daysCompared: 0 }
                }

                // In-progress period: find comparable day-offset
                const currentStart = getPeriodStartDate(currentPeriodKey)
                const currentEndDate = new Date(String(src.endDate) + 'T12:00:00')
                const dayOffset = Math.floor((currentEndDate.getTime() - currentStart.getTime()) / (1000 * 60 * 60 * 24))

                const priorStart = getPeriodStartDate(priorPeriodKey)
                const targetDate = new Date(priorStart)
                targetDate.setDate(targetDate.getDate() + dayOffset)

                // Find the closest daily data point at or before the target date in the prior period
                const priorPoints = dailyData.filter(p => {
                  const d = new Date(String(p.date) + 'T12:00:00')
                  return getPeriodInfo(d).periodKey === priorPeriodKey && d <= targetDate
                })
                if (priorPoints.length === 0) return null
                return { point: priorPoints[priorPoints.length - 1], daysCompared: dayOffset + 1 }
              }

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

              if (auaPriorAgg && timeseriesData?.aua?.data) {
                const comp = findComparablePriorSnapshot(
                  timeseriesData.aua.data,
                  String(src.period),
                  String(auaPriorAgg.period),
                  isLatestPeriod && !isSelectedPeriod
                )
                if (comp) {
                  const priorTotal = barCategories.reduce((sum, cat) => sum + (Number(comp.point[cat]) || 0), 0)
                  const priorNew = Number(comp.point['NMNC']) || Number(comp.point['nmnc']) || 0
                  const priorExisting = Number(comp.point['NMEC']) || Number(comp.point['nmec']) || 0
                  auaComparableDays = comp.daysCompared

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
                  {src.endDate && (
                    <div className="text-[10px] text-white/30 text-center mt-3">
                      as of {new Date((src.endDate as string) + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
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

### rd-session-log-2026-03-09----what-was-built-and-why.md

```
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
```

---

## Participant Background

### 1.0.0_SA_CTO -- Recent Session Logs

#### advi_49fnv3_prd_and_1236b_correction.md

# ADVI_49FNV3 PRD + $1.236B Error Correction -- 1.0.0_SA_CTO

**Date:** 2026-03-06

---

## Objective

1. Correct the erroneous $1.236B AUA figure that propagated from a prior DS
   investigation into AUAVAR thread artifacts, task orders, and logs.
2. Author the PRD for ADVI_49FNV3 (49Financial V3): 7 fixes + Books tab
   three-layer drill hierarchy.

---

## Work Completed

### 1. $1.236B Error Correction

The DS Phase 1 reconciliation investigation (2026-03-05) reported our gold layer
model at $1.236B AUA. This was a prior agent error conflating NNA and AUA metrics.
Our actual non-cash AUA is ~$1.545B. The erroneous figure propagated into the
AUAVAR-001 thread (all 6 messages + CONTEXT_COMPILED), both AUAVAR task orders,
the COO session log, thread receipts, the daily log, and the CTO PRD.

Corrected 8 files that future agents will read on startup:

| File | Correction |
|------|-----------|
| DS log `bd_model_schwab_reconciliation_investigation.md` | Prominent correction banner at top |
| PRD `AUA_VARIANCE_ANALYSIS_PRD.md` | Prior art section rewritten, risk table updated |
| DS task order `ADVI_AUAVAR.001-DS` | Background corrected, Step 1 simplified |
| DT task order `ADVI_AUAVAR.002-DT` | Background corrected, scope narrowed |
| COO log `advi_nnavar_auavar_project_launch.md` | Receipt summary corrected |
| DS thread receipt | Correction banner added |
| DT thread receipt | Correction banner added |
| Daily log `2026-03-06.md` | Corrected with note |

Untouched: 11 frozen thread artifacts (messages 000-006, CONTEXT_COMPILED, context
injection copies). These are historical records per protocol. COO briefed to be
aware of contamination if injecting thread content into future contexts.

### 2. ADVI_49FNV3 PRD

PRD authored at `docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md`.

**Fixes (P0):**
- F1: GRO mode no data (frontend wired, Lambda/data investigation needed)
- F2: Projected bars for partial periods (extrapolate with 1.5x cap, frontend-only)
- F3: Missing city/client drilldowns in Snapshot NNA Segment Analytics
- F4: Top ten advisors stacked bar (blue inflows, red outflows, gold NNA dash)
- F5: QTD/YTD timing bug (March 2026: Q1=YTD, should be identical)
- F6: Unassigned implementors pinned to bottom of leaderboard
- F7: Zebra striping on leaderboard rows

**New Features (P1):**
- N1: Books tab firm admin dashboard (tax status, AUA by advisor, distributions, engagement)
- N2: Advisor book drilldown (per-advisor tax, clients, NNA, engagement)
- N3: Relationship detail drilldown (Layer 3, may need publisher extension)
- N4: Y14 access gating (deferred from YANGV2, not Phase 1 priority)

**Phase 2 (noted, not blocking):**
- Firm-level asset allocation (new gold layer script/table needed)
- Fee revenue by advisor (new BD API feed needed -- data exists in BD)

**Key codebase findings:**
- GRO frontend is complete (PartnerAnalytics.tsx lines 372-400, 1272-1326)
- Tax status exists in gold layer (accounts_dimension `tax_status_1`, normalized)
- clients_tab.json already has tax breakdown (taxable/deferred/exempt with AUA)
- Per-advisor JSONs have tax, engagement, clients arrays
- income_fees is zeroed throughout ("not available from BD data")
- asset_allocation is zeroed ("not available from BD data")

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| $1.236B is an error, not a gold-vs-gold discrepancy | Andrew confirmed: prior agent conflated NNA and AUA. Our actual non-cash AUA is ~$1.545B. |
| Projected bar cap at 1.5x prior period | Andrew's direction: simple extrapolation with guardrail to suppress short-timeline noise |
| Fees and asset allocation are Phase 2 | Data doesn't exist in current pipeline. Noted but does not block Books tab launch. |
| Y14 access gating deferred again | Priority is data and interface structure. Auth chain already deployed. |
| Books tab three-layer hierarchy | Firm (admin) -> Advisor (drilldown) -> Relationship (detail). Natural top-down drill pattern. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| 8 files corrected for $1.236B error | See table above | No -- local |
| `docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md` | Created -- full PRD | No -- local |
| `org/projects/ADVI_49FNV3.json` | Created -- project JSON | No -- local |
| `org/projects/REGISTRY.md` | Added ADVI_49FNV3 to active | No -- local |
| This session log | Created | No -- local |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Three projects registered this session: ADVI_NNAVAR, ADVI_AUAVAR, ADVI_49FNV3.
YANGV2 closed. $1.236B error corrected across 8 files. COO briefed on thread
contamination. All files local only -- pending DT commit and push.

---

## Next Steps

1. **[2.0.0_SA_COO] Read ADVI_49FNV3 PRD and decompose into task orders** -- fixes
   F1-F7 are P0 (address first), Books tab N1-N3 are P1.
2. **[2.0.0_SA_COO] Rectify AUAVAR-001 thread artifacts** -- per CTO briefing,
   frozen thread messages contain $1.236B error. COO is aware.
3. **[0.4.0_DT_ClientPlatform] Commit and push CLOUD** -- carries all three project
   registrations, YANGV2 closure, error corrections, PRDs, and session logs.

#### advi_pod4_status_review_and_coo_handoff.md

# ADVI Pod 4 Status Review + COO Handoff Brief — 1.0.0_SA_CTO

**Date:** 2026-03-04
**Agent:** 1.0.0_SA_CTO
**Branch:** CLOUD

---

## Objective

Audit Pod 4 (ClientPlatform) commit activity and task order status across all agents for the
ADVI project. Produce a handoff brief for 2.0.0_SA_COO to oversee the next phase of implementation.

---

## Work Completed

### 1. Pod 4 Commit Activity Audit (2026-03-02 through 2026-03-04)

| Commit | Agent | Description |
|--------|-------|-------------|
| `5f60d30e` | 0.4.0_DS | feat(bd-portal-publisher): adv_drill + cla timeseries (ADVI-004 A1+A2) |
| `18f4e48c` | 0.4.0_DS | Session log for A1+A2 implementation |
| `f2e3c675` | 0.4.0_DS | DevOps brief for DT: ADVI-004 bd-portal-publisher deploy |
| `ff7f1ba3` | 0.4.0_DE | pod_inventory.xml: leaderboard sort resolved |
| `816f6fa2` | 0.4.0_DE | Session log + I2 task order marked complete |
| `6048ce3c` | 0.4.0_DE | Session log + ADVI-004 types task order marked complete |
| `076e1120` | 0.4.0_DT | Prompt enrichment for Pod 4 agents |
| `5efb15f4` | 0.4.0_DE | pod_inventory.xml upgraded to full-fidelity from 0.4.2 RD audit |
| `4a8e3d47` | 0.4.0_DE | Session log for pod_inventory.xml upgrade |

Portal DEV commits (not yet pushed):
- `3dc9dc5` — 0.4.0_DE: leaderboard sort stability fix (I2)
- `7df26bb` — 0.4.0_DE: cla type extension on CumulativeChartResponse (ADVI-004 TY)

No RD (0.4.2) or DT (0.4.0) commits in this window. No DT session logs exist yet.

### 2. Task Order Status Audit

| Task Order | Agent | Status | Notes |
|------------|-------|--------|-------|
| `ADVI-004-adv_drill_cla.md` | DS | **complete** | A1+A2 committed at `5f60d30e`, data_contract.xml updated |
| `ADVI-004-portal_types_wiring.md` | DE | **complete** | cla type added at portal DEV `7df26bb` |
| `ADVI-005-rolling_flows_data.md` | DS | **pending** | A3 not started (next DS priority) |
| `ADVI-004-distribution_continuous.md` | RD | **pending** | C2+C4 blocked on DT Stream B1 deploy |
| `ADVI-005-advisors_tab.md` | RD | **pending** | 4C blocked on DT Stream B2 deploy |

### 3. Data Contract Validation

Reviewed DS `data_contract.xml` (868 lines). Cross-checked ADVI-004 additions against
`bd-portal-publisher/lambda_function.py`:
- All field names, constants, nesting structure match code
- NMNC/NMEC classification rule documented and verified
- Record key alignment documented (adv_drill keys match adv.categories, cla.geo_drill keys match geo.categories)

Minor cosmetic issues (non-blocking):
- Gap #1 and source_note still say 0.4.2 RD page_inventory.xml is "MISSING" (it was delivered 2026-03-02)
- `primary_city` omitted from gold_script description for client_dimension.parquet
- Source 5 (advisor_rolling_flows.json) still low-fidelity; will be rewritten when DS does A3

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| No corrections needed before B1 deploy | Code-to-contract alignment verified; cosmetic gaps don't affect deploy |
| COO handoff covers B1+A3 as parallel tracks | B1 and A3 are independent; both can proceed simultaneously |

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Pod 4 is executing well. DS delivered A1+A2 same-day. DE picked up the types task order
within the same session window and completed it. The critical path now forks: DT can deploy
B1 immediately (devops brief ready), while DS starts A3 (ADVI-005 stacked_bar + rolling_1y).
RD is blocked on both B1 and B2 deploys.

---

## COO Handoff Brief

Output in chat below this log.

#### advi_v1vers_yangv2_state_reconciliation.md

# ADVI V1VERS + YANGV2 State Reconciliation — 1.0.0_SA_CTO

**Date:** 2026-03-05
**Scope:** Cross-referencing DE completeness audit (commit c1c50e3a) against CTO project JSONs and REGISTRY

---

## Objective

DE (0.4.0_DE_ClientPlatform) ran a full task order completeness sweep across ADVI_V1VERS and ADVI_YANGV2,
committed at c1c50e3a. CTO project JSONs and REGISTRY.md were stale relative to that audit.
Reconcile the org state to match verified ground truth.

---

## Work Completed

### 1. Audit Findings (from c1c50e3a)

**V1VERS: 8/8 complete.** All task orders across DE, DS (x2), AE, DT, RD (x2) verified delivered.
J1 (AE) and J2/J3 (DT) verified via log evidence and git tags.

**YANGV2: 8/9 complete.** One pending (DT portal push, not blocked). One gap (Y14, no task order).

| Open Item | Owner | Status |
|---|---|---|
| `ADVI_YANGV2.portal-push.phase3.md` | DT | PENDING — 5 commits (542197c->9b902dc) on local portal DEV, not blocked |
| `acat-inkind-nna-testing.md` Step 2 | DS | IN PROGRESS — DT brief not yet written |
| Y14 Books access gating | COO | GAP — auth chain live (J1+J2+J3 verified), no task order issued |
| NNA canonical fix (9bfb289b+b4f2d7a7) | CEO | Awaiting go/no-go before DT triggers rebuild |

### 2. Project JSON Updates

**ADVI_V1VERS.json:** Closed. `status` set to `"complete"`, `phase` updated to reflect 8/8 verified,
`blocking` cleared, `closed` date set 2026-03-05.

**ADVI_YANGV2.json:** Phase updated to "Phase 3: 8/9 complete, DT push pending, Y14 gap."
Blocking updated to enumerate all three open items (DT push + COO Y14 + CEO NNA go/no-go).

### 3. REGISTRY.md Updates

- Moved `ADVI_V1VERS` to Completed/Archived table.
- Updated `ADVI_YANGV2` active row to reflect Phase 3 state and current blocking.

---

## Decisions Made

| Decision | Rationale |
|---|---|
| Close ADVI_V1VERS | 8/8 task orders verified complete by DE audit. No open items in V1VERS scope. Y14 is YANGV2 scope (Yang feedback PRD Section 4.1). |
| Y14 is a COO action, not a CTO PRD | Auth chain is complete; the gap is a missing task order to RD for ClientsTab.tsx scoping logic. No architecture input needed — COO can issue directly from DE audit findings. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/projects/ADVI_V1VERS.json` | status->complete, phase/blocking updated, closed date added | No — local |
| `org/projects/ADVI_YANGV2.json` | phase and blocking updated to reflect Phase 3 state | No — local |
| `org/projects/REGISTRY.md` | V1VERS moved to completed; YANGV2 row updated | No — local |
| `org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-05/advi_v1vers_yangv2_state_reconciliation.md` | This file | No — local |

---

## Blockers

None for CTO. Open items are COO execution (Y14 task order), DT execution (portal push),
DS execution (ACAT DT brief), and CEO decision (NNA canonical fix go/no-go).

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Project JSONs and REGISTRY.md now match DE audit ground truth (c1c50e3a).
ADVI_V1VERS is closed. ADVI_YANGV2 is in Phase 3 with three open items tracked in the JSON.

---

## Next Steps

1. **[DT]** Execute `ADVI_YANGV2.portal-push.phase3.md` — push portal DEV through 9b902dc, update CLOUD submodule pointer. Not blocked.
2. **[DS]** Write `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md` — ACAT v3 EC2 run instructions for DT. Not blocked.
3. **[COO]** Issue Y14 task order to RD (0.4.2_RD_AdvisorIntelligence) — ClientsTab.tsx advisor scoping logic. Auth chain live.
4. **[Andrew]** Populate `opal-partner-49financial` DynamoDB table with advisor email mappings before Y14 goes live.
5. **[CEO/Andrew]** Go/no-go on NNA canonical fix (commits 9bfb289b+b4f2d7a7) — gates DT gold layer rebuild.
6. **[COO]** Open Y17 AI RAG mini-PRD when Books tab is stable.

#### macro_project_code_system.md

# Macro/Project Code System — 1.0.0_SA_CTO

**Date:** 2026-03-05
**Agent:** 1.0.0_SA_CTO
**Branch:** CLOUD

---

## Objective

Design and implement a two-level code system to eliminate conflation between
surface area identifiers (pages, pipelines, cloud processes, research) and
specific project initiatives. One macro can host many projects over its lifetime.

---

## Work Completed

### 1. Problem Identified

`ADVI` was serving double duty as both the AdvisorIntelligence page identifier
AND the project code. V1 completion (threads 001-006) and Yang Feedback V2
(21 work streams) were both registered under the same `ADVI.json`, making
thread serials, task orders, and commits ambiguous across different initiatives
on the same surface area.

### 2. Design

Two-level system:

| Level | Format | Example | Purpose |
|-------|--------|---------|---------|
| Macro code | 4 chars | `ADVI` | Surface area — permanent, never a project code |
| Project code | `{MACRO}_{6CHAR}` | `ADVI_V1VERS` | Specific initiative |

Thread serials: `{PROJECT_CODE}-{NNN}` → `ADVI_V1VERS-007`
Task orders: `{PROJECT_CODE}-{NNN}-{slug}.md`
Project JSON: `org/projects/{PROJECT_CODE}.json`
Scripts: unchanged (treat project code as opaque string)

### 3. Core System Files Updated (commit 3d5fc658)

| File | Change |
|------|--------|
| `PAGE_CODES.md` → `MACRO_CODES.md` | Renamed via git mv; language updated throughout |
| `ADVI.json` → `ADVI_V1VERS.json` | V1 completion project; all 6 threads carry `legacy_serial` fields |
| `ADVI_YANGV2.json` | New — Yang Feedback V2 project, thread_counter 0 |
| `PFMG_VISPOL.json` | New — Trade Engine Visual Polish (PFMG macro) |
| `REGISTRY.md` | Restructured with Macro + Project Code columns |
| `AGENT_START_HERE.md` | Task order filename convention updated |
| `1.0.0_SA_CTO/prompt.md` | New project workflow + MACRO_CODES.md reference |
| `2.0.0_SA_COO/prompt.md` | Project file refs + task order format |
| `threads/THREAD_KNOWLEDGE.md` | M8 + M10 updated to PROJECT_CODE format |
| `threads/README.md` | All examples updated |
| `threads/ARCHITECTURE.md` | Schema, file structure, receipt naming |

### 4. Retroactive Cleanup Task Orders Issued

Scope analysis: 16 task order files and 9 thread receipt files across 5 agents,
plus 3 THREAD.json files in thread folders. Session logs and thread internals
(CONTEXT_COMPILED.md, messages/) are left as-is (historical records).

| Task Order | Issued To | File |
|------------|-----------|------|
| COO scope: THREAD.json + AE/DT task orders | 2.0.0_SA_COO | `org/tier1_exec/2.0.0_SA_COO/task_orders/macro_project_code_retroactive_cleanup.md` |
| Pod 4 scope: DE/DS/RD task orders + receipts | 0.4.0_DE_ClientPlatform | `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/macro_project_code_retroactive_cleanup.md` |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| "Macro code" not "page code" | Surface areas include pipelines, cloud processes, research — not just pages |
| `{MACRO}_{6CHAR}` format | Underscore as separator is readable and valid in filenames; 6-char suffix is human-meaningful |
| `ADVI_V1VERS` for all V1 threads (001-006) | Grandfathering under one project is cleaner than splitting; `legacy_serial` field preserves old IDs |
| Thread folder directory names not renamed | Too disruptive; THREAD.json field update is sufficient for correctness |
| Session logs not renamed | Historical records; renaming would destroy context traceability |
| DE handles all pod 4 renames | DE has commit authority across all pod 4 paths; most efficient in one pass |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/projects/MACRO_CODES.md` | Renamed from PAGE_CODES.md + content update | Yes — `3d5fc658` |
| `org/projects/ADVI_V1VERS.json` | Renamed from ADVI.json + schema update | Yes — `3d5fc658` |
| `org/projects/ADVI_YANGV2.json` | Created | Yes — `3d5fc658` |
| `org/projects/PFMG_VISPOL.json` | Created | Yes — `3d5fc658` |
| `org/projects/REGISTRY.md` | Restructured | Yes — `3d5fc658` |
| `org/AGENT_START_HERE.md` | Task order convention | Yes — `3d5fc658` |
| `org/tier1_exec/1.0.0_SA_CTO/prompt.md` | Project lifecycle protocol | Yes — `3d5fc658` |
| `org/tier1_exec/2.0.0_SA_COO/prompt.md` | Project file refs | Yes — `3d5fc658` |
| `org/threads/THREAD_KNOWLEDGE.md` | M8 + M10 | Yes — `3d5fc658` |
| `org/threads/README.md` | Examples | Yes — `3d5fc658` |
| `org/threads/ARCHITECTURE.md` | Schema + structure | Yes — `3d5fc658` |
| `org/tier1_exec/2.0.0_SA_COO/task_orders/macro_project_code_retroactive_cleanup.md` | New task order | No — local |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/macro_project_code_retroactive_cleanup.md` | New task order | No — local |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE (core system), PENDING (retroactive cleanup)
**Active branch:** CLOUD

Core two-level code system is committed at `3d5fc658`. Two task orders issued for
retroactive file renames: COO handles THREAD.json (3 files) and AE/DT task orders
(2 files); DE handles all pod 4 task order renames (10 files) and receipt renames
(8 files). Going forward, next ADVI V1 thread is `ADVI_V1VERS-007`, next YANGV2
thread is `ADVI_YANGV2-001`.

---

## Next Steps

1. **[COO] Execute `macro_project_code_retroactive_cleanup.md`** — THREAD.json updates + AE/DT renames
2. **[DE] Execute `macro_project_code_retroactive_cleanup.md`** — pod 4 task order + receipt renames
3. **[DT] Push CLOUD** — carry both cleanup commits + session log to remote

#### nnavar_auavar_project_registration.md

# NNAVAR + AUAVAR Project Registration & YANGV2 Closure -- 1.0.0_SA_CTO

**Date:** 2026-03-06

---

## Objective

Register two new ADVI projects for BD gold layer data quality analysis (NNA correlation
optimization and AUA variance decomposition), close ADVI_YANGV2, and hand off to COO
for task order decomposition.

---

## Work Completed

### 1. ADVI_NNAVAR -- NNA Variance Optimization

**PRD authored** at `docs/architecture/NNA_VARIANCE_OPTIMIZATION_PRD.md`.

Key framing: ACAT parameter grid (v2, executed 2026-03-05) showed Pearson r plateau at
0.175 -- ACAT adjustment adds $12-22M but doesn't move correlation. The $120M gap is
driven by factors outside ACAT (JNL exclusion calibration, velocity caps, dedup
aggressiveness, account coverage, timing). Project scope extends beyond parameter
tuning to full gap decomposition by filter category.

Significant prior art exists:
- DS Phase 3 analysis (ACAT production design complete)
- v2 param grid results on S3 (analysis pending)
- Correlation summary script written but not yet run

### 2. ADVI_AUAVAR -- AUA Variance Analysis

**PRD authored** at `docs/architecture/AUA_VARIANCE_ANALYSIS_PRD.md`.

Key framing: ~$55M gap between our $1.545B non-cash AUA and BD's $1.60B. 49Financial
leadership relies on BD. Prior DS investigation (5-phase reconciliation) found fundamental
data source difference. This project refocuses: segment-level decomposition to identify
which account/asset/pricing segments explain the gap. Outcome is explanation + addressable
vs explainable classification per segment.

Note: DS prior investigation erroneously reported our model at $1.236B (prior agent
conflated NNA and AUA metrics). Our actual non-cash AUA is ~$1.545B. Correction notes
added to DS log, PRD, task orders, COO log, and thread receipts on 2026-03-06.

### 3. ADVI_YANGV2 Closure

Marked complete. Y14 (Books access gating) deferred to upcoming ADVI_49FNV3 project.
All other task orders were delivered per DE audit (c1c50e3a). DT portal push and SSCN
wave pushes completed.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| NNAVAR scope extends beyond ACAT parameters | v2 grid proved ACAT alone doesn't move correlation. Gap decomposition by filter category is the real work. |
| AUAVAR framed as "explain the gap from BD" not "fix our model" | 49 leadership uses BD. The question is what we're missing, not whether our methodology is wrong. |
| Close YANGV2 with Y14 deferred to 49FNV3 | Y14 (Books access gating) is part of the broader Books tab completion that 49 data team flagged. Better scoped under 49FNV3. |
| Both projects to Pod 4 (ClientPlatform) | DS, DT, and AE resources are all Pod 4 / PartnerETL. BD pipeline is the data source. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `docs/architecture/NNA_VARIANCE_OPTIMIZATION_PRD.md` | Created -- full PRD | No -- local |
| `docs/architecture/AUA_VARIANCE_ANALYSIS_PRD.md` | Created -- full PRD | No -- local |
| `org/projects/ADVI_NNAVAR.json` | Created -- project JSON | No -- local |
| `org/projects/ADVI_AUAVAR.json` | Created -- project JSON | No -- local |
| `org/projects/ADVI_YANGV2.json` | status->complete, phase updated, closed date added | No -- local |
| `org/projects/REGISTRY.md` | YANGV2 moved to completed; NNAVAR + AUAVAR added to active | No -- local |
| This session log | Created | No -- local |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Two new projects registered (NNAVAR, AUAVAR). YANGV2 closed. All files local only --
pending DT commit and push. COO handoff below.

---

## Next Steps

1. **[2.0.0_SA_COO] Read both PRDs and decompose into task orders** -- primary agents are
   0.4.0_DS_ClientPlatform (analysis) and 0.4.0_DT_ClientPlatform (EC2 execution).
   AE (0.6.0_AE_PartnerETL) consulted if BD data enrichment needed.
2. **[0.4.0_DT_ClientPlatform] Commit and push CLOUD** -- carries PRDs, project JSONs,
   REGISTRY update, YANGV2 closure, and this session log.
3. **[Andrew] Discuss ADVI_49FNV3 scope** -- Books tab completion + 49Financial data team
   feedback from yesterday.

#### proactive_downstream_check_protocol.md

# Proactive Downstream Check Protocol — 1.0.0_SA_CTO

**Date:** 2026-03-05
**Scope:** New startup protocol added to AGENT_START_HERE.md + session log template + CTO prompt

---

## Objective

Agents were starting with full context of their own work but zero visibility into what happened
downstream after a handoff. This caused gaps like the Y14 issue: J1+J2+J3 all delivered, auth
chain live, but no agent surfaced the missing task order on startup. Fixed by adding Step 2b
(Proactive Downstream Check) to the universal agent startup protocol.

---

## Design

### The problem

An agent marks a task order complete and logs `[0.4.0_DE_ClientPlatform] receive commit abc1234`.
Next session: they start fresh, read their own logs, see "complete." But they have no idea whether
DE actually acted on the commit, found a blocker, or is waiting on something upstream.
The blind spot is everything that happened AFTER the handoff.

### The mechanism

Two-direction check at startup, one hop deep:

1. **Downstream:** Scan most recent log's `## Next Steps` for `[agent_serial]` tags.
   Read each tagged agent's latest log folder. See what they did with the handoff.

2. **Upstream:** Check `<issued_by>` in pending task orders. Read issuing agent's latest log.
   See if scope changed or new dependencies emerged.

**Depth limit: one hop.** The startup cost of reading 2-3 agent log folders is negligible.
Recursing further would be an unbounded org scan — wrong for startup.

### The discovery mechanism

The `[agent_serial]` tags in `## Next Steps` were already in the template but used role names
(`[Dashboard Engineer]`) which can't be resolved to a folder path. Changed to full serials
(`[0.4.0_DE_ClientPlatform]`). Now Step 2b can resolve `org/tier2_senior/{serial}/logs/{latest}/`
mechanically.

### What this catches

- Task order marked complete but downstream agent blocked (you'd see it in their log)
- Handoff commit pushed but receiving agent hasn't started (AMBIGUOUS — surface in orientation)
- Issuing agent changed scope mid-task (you'd see it in their latest log)
- Gate cleared but no task order issued (the Y14 pattern — you'd see "J1+J2+J3 complete" in AE
  and DT logs at startup and immediately recognize Y14 is unblocked with no owner)

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/AGENT_START_HERE.md` | Added Step 2b (Proactive Downstream Check) between Steps 2 and 3 | No — local |
| `org/AGENT_START_HERE.md` | Updated Step 5 orientation summary template to include `Downstream check:` field | No — local |
| `org/AGENT_START_HERE.md` | Updated `## Next Steps` template to require agent serials, not role names | No — local |
| `org/tier1_exec/1.0.0_SA_CTO/prompt.md` | On Launch step 3 rewritten to incorporate Step 2b + DE/DT log reads for active projects | No — local |
| `org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-05/proactive_downstream_check_protocol.md` | This file | No — local |

---

## Decisions Made

| Decision | Rationale |
|---|---|
| One hop only | Startup cost must stay low. Two hops would be an org-wide audit, not a startup check. |
| `[agent_serial]` tags as discovery mechanism | Serials map directly to folder paths. Role names do not. Templates already had tags -- just needed the format tightened. |
| Step 2b not Step 6 | Must happen before adopting the role persona (Step 3) so the agent can contextualize what they read. Reading downstream logs without your role frame active is fine; acting on them requires the frame. |
| Role prompts: update CTO only now | AGENT_START_HERE.md is the canonical authority. Other role prompts will naturally incorporate Step 2b when agents read AGENT_START_HERE.md. A COO task order cascade is optional -- not required for the protocol to take effect. |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Step 2b is live in AGENT_START_HERE.md. Next Steps template updated. CTO prompt updated.
All agents will encounter Step 2b on their next startup via the mandatory AGENT_START_HERE.md read.
Role prompts for non-CTO agents will be updated organically or via COO cascade.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Commit and push CLOUD** -- carries AGENT_START_HERE.md change,
   project JSON updates (V1VERS closed, YANGV2 Phase 3), REGISTRY.md, session logs.
2. **[2.0.0_SA_COO] Issue Y14 task order to RD** -- auth chain live, no task order exists.
3. **[Andrew] Go/no-go on NNA canonical fix** -- commits 9bfb289b+b4f2d7a7 awaiting decision.

#### security_scanner_prd.md

# Session Log: Security Scanner PRD

**Agent:** 1.0.0_SA_CTO
**Date:** 2026-03-05
**Scope:** PRD authoring + project registration for Security Scanner

---

## Objective

Create the PRD and org registration for the Security Scanner portal page -- a port of Yang's Factor_Scanning_Model.xlsm Excel workbook to the Opal Capital portal.

## Work Completed

1. **Authored PRD** at `docs/architecture/SECURITY_SCANNER_PRD.md`
   - Documented all 4 Excel tabs and their portal equivalents
   - Specified portal page design: route, sidebar placement, directory structure
   - Defined header panel, all 4 tabs, scoring algorithm, universes, factor categories
   - Identified existing patterns to reuse (AdvisorIntelligence tabs, PortfolioManagement colors)
   - Deferred data architecture to Pattern 0 thread

2. **Registered macro code** `SSCN` in `org/projects/MACRO_CODES.md` under Pod 3

3. **Created project** `SSCN_PORTAL` with JSON at `org/projects/SSCN_PORTAL.json`

4. **Added registry row** in `org/projects/REGISTRY.md`

5. **Created RD agent** `0.3.4_RD_SecurityScanner`
   - README, prompt, logs/, task_orders/ at `org/tier3_junior/0.3.4_RD_SecurityScanner/`
   - Added to ORG_CHART.md Pod 3 leaf agents
   - Added to DE README team roster and pages table

## Decisions Made

- **Route:** `/security-scanner` -- consistent with kebab-case portal convention
- **Sidebar placement:** Tools section, above Portfolio Management
- **Icon:** `ScanLine` from lucide-react -- visually represents scanning/filtering
- **Access:** `requiresDev: true` during buildout
- **Data architecture:** Deliberately deferred to Pattern 0 thread (DS + DE + AE) -- no premature API decisions
- **Agent serial:** `0.3.4` -- next available in Pod 3 after 0.3.3_RD_DataRefresh

## Files Modified

| File | Change |
|------|--------|
| `docs/architecture/SECURITY_SCANNER_PRD.md` | Created -- full PRD |
| `org/projects/MACRO_CODES.md` | Added `SSCN` row to Pod 3 table |
| `org/projects/REGISTRY.md` | Added `SSCN_PORTAL` row to Active Projects |
| `org/projects/SSCN_PORTAL.json` | Created -- project JSON |
| `org/tier3_junior/0.3.4_RD_SecurityScanner/README.md` | Created -- agent identity |
| `org/tier3_junior/0.3.4_RD_SecurityScanner/prompt.md` | Created -- RD persona prompt |
| `org/tier3_junior/0.3.4_RD_SecurityScanner/logs/.gitkeep` | Created |
| `org/tier3_junior/0.3.4_RD_SecurityScanner/task_orders/.gitkeep` | Created |
| `org/ORG_CHART.md` | Added 0.3.4 to Pod 3 leaf agents |
| `org/tier2_senior/0.3.0_DE_TradingOperations/README.md` | Added 0.3.4 to team roster and pages table |
| `org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-05/security_scanner_prd.md` | This file |

## Blockers

None. PRD is complete. Data architecture is an open question for the Pattern 0 thread, not a blocker on this deliverable.

## Current State

PRD authored, project registered, RD agent created. Ready for COO review.

## Next Steps

- [COO] Read PRD and initiate Pattern 0 thread for data architecture (DS + DE + AE)
- [COO] Decompose into task orders for Pod 3 DE after data architecture resolves
- [0.3.0_DE] Receive task orders and cascade to 0.3.4_RD_SecurityScanner

#### trade_engine_visual_polish_prd.md

# Trade Engine Visual Polish PRD — 1.0.0_SA_CTO

**Date:** 2026-03-04
**Agent:** 1.0.0_SA_CTO
**Branch:** CLOUD

---

## Objective

Write a PRD for Yang's 13-item feedback list on the PortfolioManagement page. All items are
frontend-only visual/UX improvements: conditional cell highlighting, gradient color scales,
capitalize group names, canonical group ordering, zero-weight formatting, size column coloring,
new finalBet derived column, and a Reset Zero button.

---

## Work Completed

### 1. Yang Feedback Triage (13 items)

Went through Yang's raw feedback line by line. Resolved 3 ambiguities with Andrew:
- Size column "O" = Other (not a typo for S). L=green, M=yellow, O=red.
- Reset Zero = sets all finalTrade to 0 (hold everything). Confirmed.
- Canonical group order = from Yang's signal DataFrame, not alphabetical.

### 2. Canonical Factor Group Order Discovery

Traced through the data flow:
- Yang's alpha PKL contains a `signal` DataFrame with 33 factors in canonical row order
- `lambda_function.py` line 651-654: merges signal metadata and sorts by `order` column
- `factorDescriptions.ts`: comments organize factors by group in the same canonical sequence
- Alpha tab "By Factor" default view preserves Lambda array order (correct)
- Alpha tab "By Group" view sorts alphabetically (bug — line 74 of AlphaTab.tsx)

Canonical order: size, efficiency, growth, management, profitability, quality, value,
analyst, governance, crowding, insider, short, beta, momentum, technical (15 groups, 33 factors).

### 3. PRD Written

`docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md` — 13 items fully spec'd with:
- Current state per component
- Exact thresholds and color rules
- File paths and line numbers
- Implementation patterns (threshold vs gradient vs CSS)

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Pod 3 (TradingOperations) owns all work | PortfolioManagement page is Pod 3, not Pod 2 |
| Extract CANONICAL_GROUP_ORDER to shared util | Needed by AlphaTab, ModelTab, and SecurityDetailModal |
| Reuse getGradientBackground from PortfolioGrid | Already exists for optimizedBet gradient; extend to other columns |
| Stale data bug excluded from PRD | Already addressed via cache-busting fix pushed separately |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md` | New PRD | No -- local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

PRD written and reviewed with Andrew. COO handoff brief delivered in chat. Ready for
2.0.0_SA_COO to decompose into task orders for Pod 3 DE (0.3.0_DE_TradingOperations).
All 13 items are independent with no blocking dependencies.

---

## Next Steps

1. **[COO] Read PRD and decompose into task orders** -- `docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md`
2. **[COO] Issue task orders to 0.3.0_DE_TradingOperations** -- suggested 5 groupings in handoff brief
3. **[DE] Decide RD delegation vs direct implementation** -- all items are portal-only
4. **[DT] Push portal DEV when DE work is committed** -- standard QA gate

**Do NOT:**
- Issue task orders to Pod 2 (PortfolioAnalytics) -- this is Pod 3 work
- Modify any Lambda or backend code -- all items are frontend-only
- Change the Lambda factor order -- the canonical order is already correct in the backend

#### yang_feedback_prd_v2.md

# Yang Feedback PRD V2 — 1.0.0_SA_CTO

**Date:** 2026-03-04
**Agent:** 1.0.0_SA_CTO
**Branch:** CLOUD

---

## Objective

Ingest Yang's 4-part feedback on the Advisor Intelligence page, organize into
architectural requirements, and produce a V2 PRD for COO decomposition into
updated task orders.

---

## Work Completed

### 1. Yang Feedback Ingestion (4 parts)

Received and organized 29+ feedback items from Andrew (relaying Yang's review):

| Section | Items | Key Changes |
|---------|-------|-------------|
| Assets Overview (Header) | 1-8 | AUA stack flip, asset mix toggle, NNA bar alignment, new GRO mode |
| Distribution | 9-16 + 2.2b/2.2c/2.3b | Bucket removal, city drill-down, ADV relationship drill-down, outflows quartile fix, area->stacked bar |
| Advisors | 17-21 | QTD/YTD bug, Advisor toggle, drop 1Y rolling, NNA bar format |
| Books | 22-29 | Admin/non-admin architecture, tax-dominant client view, AI exec summary RAG |

### 2. V2 PRD Written

`docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md`

- 21 new work streams (Y1-Y17 + Y3-FE, Y5-FE, Y6b, Y6c, Y6d)
- 5 execution phases defined
- Full dependency graph
- Relationship to V1 PRD documented (what's unchanged, extended, or replaced)
- Naming decisions flagged for Andrew/Yang

### 3. Late Additions (Andrew follow-up)

- **2.2b:** Snapshot GEO-NNA city-level drill-down (state -> city)
- **2.2c:** Outflows quartile inversion fix scoped to ALL 4 grain levels (state, city, architect, relationship)
- **2.3b:** Snapshot ADV-NNA relationship-level drill-down (architect -> relationship)

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| V2 PRD as new document, not in-place edit of V1 | V1 has completed streams with status tracking; overwriting would lose that history |
| GRO data uses accounting identity (AUA_end - AUA_start - NNA) | No new raw data needed if period AUA endpoints and NNA both available |
| AI RAG system recommended as separate mini-PRD | Too large and architecturally distinct to bundle with visual feedback items |
| Outflows quartile fix scoped to all 4 levels | Same logical error applies everywhere NNA outflows are percentile-ranked |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md` | Created — full V2 PRD | No — local only |
| `org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-04/yang_feedback_prd_v2.md` | Created — this log | No — local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

V2 PRD is written and ready for COO decomposition. No commits pushed yet — DT owns the
push gate. The PRD defines 21 new work streams across all Pod 4 agents plus AE shared
services. Phase 1 (frontend-only visual changes) can start immediately once COO issues
task orders. Phase 2 (DS data work) runs in parallel.

---

## Next Steps

1. **[COO] Read V2 PRD and decompose into task orders** — see handoff briefing
2. **[DT] Push CLOUD** — PRD + session log need to reach remote
3. **[COO] Update existing RD task orders** — C2/C4/4C may need scope adjustments per Yang feedback
4. **[DS] Phase 2 data batch** — after COO issues task orders

**Do NOT:**
- Issue task orders directly to leaf agents from this PRD — COO decomposes
- Start ADVI-006 thread before J3 is live
- Bundle AI RAG system (Y17) into the main task order set — separate mini-PRD needed


### 1.0.0_SA_CTO -- Recent Commits

# Recent commits by 1.0.0_SA_CTO

7dacb90a 1.0.0_SA_CTO: ADVI_49FNV3 PRD + $1.236B AUA error correction
d9595f8a org(1.0.0_SA_CTO): AGENT_START_HERE -- enforce PROD is merge-only from DEV
67f51245 2.0.0_SA_COO: ADVI_AUAVAR correction -- $1.236B figure was NNA/AUA conflation error
70febc7b 1.0.0_SA_CTO: ADVI_NNAVAR + ADVI_AUAVAR project registration -- PRDs, project JSONs, registry update
17ec8a99 org(1.0.0_SA_CTO): SSCN_PORTAL scaffolding + PRDs (Security Scanner, Trade Engine Visual Polish, Yang V2 Feedback)
d8f6deac org(1.0.0_SA_CTO): Step 2b proactive downstream check + ADVI state reconciliation
5033abf6 org(1.0.0_SA_CTO): blocker verification protocol -- check before declaring blocked
f27e785e org(1.0.0_SA_CTO): segment rule -- dots between segments, dashes within segments
3e460957 org(1.0.0_SA_CTO): READMEs -- macro/project code system + task order format
042de2d4 org(1.0.0_SA_CTO): task order filename format -- dot separator, dashes only
3bbc980a org(1.0.0_SA_CTO): retroactive cleanup task orders + session log
3d5fc658 org(1.0.0_SA_CTO): two-level code system -- macro codes + project codes
b9b9ca24 org(1.0.0_SA_CTO): ADVI-006 thread artifacts + ADVI.json thread_counter + DE task order
b665c837 org(1.0.0_SA_CTO): HOTFIX task order -- snapshot drilldown broken (account_performance fallback undeployed)
ecc2e826 org(1.0.0_SA_CTO): C3 CLA snapshot addendum -- header_metrics source + composition redesign
80131a6b org(1.0.0_SA_CTO): COO handoff brief + pre-drafted J1/J2/J3 task orders for partner identity table
520ec5b1 docs(1.0.0_SA_CTO): revise PRD -- per-partner table, not universal; 49 Financial first
64486d60 docs(1.0.0_SA_CTO): Partner Identity Table PRD + Pod 4 work summary for external review
7a9b968d log(1.0.0_SA_CTO): ADVI Pod 4 status review + COO handoff brief
f1dc9d0a log(1.0.0_SA_CTO): ADVI thread execution and process improvements session

### 0.4.0_DE_ClientPlatform -- Recent Session Logs

#### advi_49fnv3_f3_f5_n1n2_investigation.md

# ADVI_49FNV3 — F3/F5/N1-N2 Investigation and Closeout — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-06
**Start Time:** session start
**End Time:** session end

## Objective

Close out three pending ADVI_49FNV3 DE task orders: F5-DE (QTD/YTD period toggle
investigation), F3 (DistributionTab NNA geo drill wiring), and N1-N2-DE (firm dashboard +
advisor book wiring). DS confirmed F5 is not a Lambda bug; DT confirmed N1+N2 wiring was
already implemented in the prior session (1dc96b5).

---

## Work Completed

### 1. F5-DE: QTD/YTD Period Toggle Investigation

**Task order:** `ADVI_49FNV3.F5-DE.qtd-ytd-frontend-investigation.md`

**DS finding (from advi_49fnv3_f1_f5_investigation.md):**
- `bd-portal-advisor-publisher` computes `qtd_start = Jan 1, 2026` and
  `ytd_start = Jan 1, 2026` for any date in Q1. Identical. Lambda is correct.
- Root cause is **not** in the Lambda.

**DT finding (from advi_49fnv3_session1.md, prior session):**
- `periodToChartWindow('qtd')` in `AdvisorsTab.tsx` maps to `'3M'` (trailing 90 days).
- `periodToChartWindow('ytd')` maps to `'1Y'` (trailing 1 year).
- The leaderboard publisher emits **rolling trailing windows** only. In March 2026,
  QTD = Jan 1 to today (~65 days) but `'3M'` = trailing 90 days from today. These are
  different date ranges producing different NNA values.
- **Frontend cannot fix this alone.** Fix requires DS to emit a `qtd` calendar window
  in `architect_leaderboard.json` and `implementor_leaderboard.json`.

**DE finding:** No code change made. Root cause is rolling-vs-calendar window mismatch.
Fix is Lambda-side (DS task). Task order marked complete.

---

### 2. F3: DistributionTab NNA Geo Drill Investigation

**Task order:** `ADVI_49FNV3.F3.segment-drilldown-wiring.md`

**Investigation:**

Audited `DistributionTab.tsx` and `types.ts` against task order requirements.

**Q1: Is `nna_geo_drill` from `timeseries_chart.json` consumed by the Snapshot NNA donut?**

NO — and correctly so. `nna_geo_drill` from `timeseries_chart.json` has type
`NNAGeoDrillView` (`{ [stateKey]: { categories: string[], data: NNASeriesPoint[] } }`).
This is a **time series**, not donut segment data. It is consumed by
`ContinuousNnaDivergingView` (line 443) for the continuous NNA chart — the correct use.

**Q2: Is state→city drill wired for the Snapshot NNA geo donut?**

YES — already wired. `handleSegmentClick` at line 1815-1834 handles NNA geo drill:
- If `nnaDrillData[seg.key]` exists → `setSelectedStateKey(seg.key)` + `setGeoDrillLevel('city')`
- City segments built from `nnaDrillData[selectedStateKey].by_city` at line 1658-1668

`nnaDrillData` reads from `analyticsData.views.nna[period].geo.drill` in
`header_metrics_quarterly.json`. This is the correct data source for distribution stats.

**Q3: Is `by_city` data populated in the published JSON?**

YES — confirmed in `data/black_diamond/scripts/gold/09_generate_partner_analytics.py`,
lines 1061-1087 (Y6b block): `geo_drill_dist[state] = { total: ..., by_city: {...} }`.
The EC2 script emits `by_city: Record<string, DistributionStats>` for each top state
that has at least 2 relationships in any city. This feeds into `views.nna[period].geo.drill`.

**Q4: City→client drill?**

NOT available in GEO mode. `by_city` entries are `DistributionStats` aggregates, not
individual relationship records. Y6d client drill is ADV-mode only (architect →
relationships via `views.nna[period].adv.drill[arch].distribution`). There is no
per-relationship list within geo city entries. This is a data constraint, not a wiring gap.

**Conclusion:** No code change needed. F3 wiring is complete in existing code. Task order
marked complete.

---

### 3. N1-N2-DE: Firm Dashboard + Advisor Book Wiring Verification

**Task order:** `ADVI_49FNV3.N1-N2-DE.firm-dashboard-and-advisor-book-wiring.md`

Prior DT session (1dc96b5) implemented all requirements. Verified against task order:

| Requirement | Status |
|---|---|
| TypeScript interfaces from design brief Section 6 | Done — already in `types.ts` (AdvisorBookResponse, BooksClientDetailResponse, BooksClientAccount, BooksClientTaxDetail, CostBasisYear, GainPosition, OpenLot) |
| N1 Firm Overview KPIs | Done — `N1FirmDashboard` component, Panel 1 (line 930-940 of ClientsTab.tsx) |
| N1 Tax Status Breakdown | Done — TaxRow components, Panel 2 (lines 942-952) |
| N1 Engagement Summary | Done — FlowMetric + MetricCard, Panel 3 (lines 954-966) |
| N1 AUA by Advisor (1Y, sorted by total_aua, row click -> N2) | Done — `AdvisorSummaryTable` (line 329, sorts by total_aua desc, onClick -> handleSelectAdvisor) |
| N2 Advisor Book View (L2AdvisorBook) | Done — all 4 panels: Summary KPIs, Tax Exposure, Engagement, Clients table (lines 345-426) |
| advisorId slug fix | Done — exact replica of `_advisor_id()` at line 186 |
| Access gate `isInternal() \|\| isDev()` | Done — line 52-53 |
| Data fetch: leaderboard + clients_tab in parallel | Done — Promise.all at lines 84-98 |

Task order marked complete. Updated N1-N2-RD task order dependency from `pending` to
`complete`. RD may review and polish visual layout per their task order.

---

## Decisions Made

| Decision | Rationale |
|---|---|
| F5-DE: no frontend fix | Root cause is rolling-vs-calendar window mismatch in leaderboard publisher. Frontend maps `qtd` to `'3M'` which is incorrect but unfixable until Lambda emits a `qtd` calendar window. Route to DS for Lambda fix. |
| F3: no wiring change | State→city drill already wired in `handleSegmentClick`. `nna_geo_drill` from timeseries_chart.json is correctly NOT used in snapshot donut — it's time series data for the continuous view. |
| F3: city→client gap as data constraint | EC2 script 09 emits `by_city: DistributionStats`, not relationship lists. ADV mode has client drill but GEO city level does not. Correct behavior — no stub or workaround. |
| N1-N2-DE: complete without new code | DT implemented all functional requirements in 1dc96b5. No additional wiring needed. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F5-DE.qtd-ytd-frontend-investigation.md` | status -> complete | No — local only |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F3.segment-drilldown-wiring.md` | status -> complete | No — local only |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.N1-N2-DE.firm-dashboard-and-advisor-book-wiring.md` | status -> complete | No — local only |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_49FNV3.N1-N2-RD.firm-dashboard-and-advisor-book-ui.md` | dependency status -> complete, constraint note updated | No — local only |

---

## Blockers

- **F5 fix**: BLOCKED on DS — Lambda must emit a `qtd` calendar window in
  `architect_leaderboard.json` / `implementor_leaderboard.json`. Task order F5-DS is
  with 0.4.0_DS_ClientPlatform.
- **F1 GRO data**: BLOCKED on DT — bd-portal-publisher redeploy required per
  `docs/briefs/devops-brief-49fnv3-f1-gro-publisher-fix.md`. No DE action.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

All three DE task orders for ADVI_49FNV3 are closed. No portal code changes were made
this session — all findings were investigative. Key result: the snapshot NNA geo drill
in DistributionTab.tsx is already correctly wired via `views.nna[period].geo.drill[state].by_city`
from partner_analytics JSON. N1+N2 wiring in ClientsTab.tsx is complete. N1-N2-RD task
order dependency is unblocked for 0.4.2_RD_AdvisorIntelligence.

---

## Next Steps

1. **[0.4.0_DS_ClientPlatform] F5 Lambda fix** — emit `qtd` calendar window in leaderboard
   JSON so `periodToChartWindow('qtd')` can map to `'qtd'` directly instead of `'3M'` approximation.
2. **[0.4.0_DT_ClientPlatform] F1 redeploy** — rebuild and redeploy bd-portal-publisher per
   devops brief to surface `growth_decomposition` in portal GRO mode.
3. **[0.4.2_RD_AdvisorIntelligence] N1-N2-RD visual polish** — dependency now resolved,
   RD can review DT's panel implementation and polish visual layout per task order.
4. **[0.4.2_RD_AdvisorIntelligence] F2, F4** — projected bars and stacked bar (already
   issued task orders per COO session).

**Files to touch next:**
- None (all DE items complete for this project sprint)

**Do NOT:**
- Wire `nna_geo_drill` from `timeseries_chart.json` into the snapshot NNA donut — it is
  a time series and is correctly placed in the continuous view.
- Fix F5 frontend-side — the window mismatch cannot be resolved without a Lambda-side
  `qtd` calendar window addition.

#### advi_49fnv3_f3_fix_nna_drill_tdz.md

# ADVI_49FNV3 F3-fix + F3b: NNA Drill Fixes -- 0.4.0_DE_ClientPlatform

**Date:** 2026-03-09
**Portal DEV commits:** `9c1881a` -> `3367cd8`
**Workspace CLOUD commit:** pending

## Objective

Fix the NNA snapshot drill error in DistributionTab.tsx. Andrew confirmed on 2026-03-09
that clicking a state in NNA+GEO Snapshot mode triggers an error. CTO reopened F3 via
task order `ADVI_49FNV3.F3-fix.nna-snapshot-drill-error.md`, overriding the prior
2026-03-06 investigative closeout.

---

## Work Completed

### 1. Root Cause: Temporal Dead Zone (TDZ) in useMemo Ordering

`nnaDrillData` was declared at line 1707 via `useMemo`, but consumed inside the
`segments` useMemo factory at line 1658. JavaScript `const` declarations are hoisted
but not initialized until execution reaches the declaration (TDZ).

**The crash sequence:**
1. User clicks a state segment in NNA+GEO Snapshot mode
2. `handleSegmentClick` sets `geoDrillLevel('city')` + `selectedStateKey(seg.key)`
3. React re-renders. The `segments` useMemo runs first (line 1655) because its deps
   (`geoDrillLevel`) changed
4. Inside the factory, the condition `metric === 'nna' && nnaDrillData?.[...]` executes
5. `nnaDrillData` is a `const` declared later at line 1707 -- still in the TDZ
6. `ReferenceError: Cannot access 'nnaDrillData' before initialization`

**Why it wasn't caught earlier:**
- On initial render, `geoDrillLevel === 'state'` so the `if` at line 1656 is false --
  `nnaDrillData` is never accessed, no TDZ error
- AUA mode drill doesn't hit the NNA branch (`metric !== 'nna'`) so also no TDZ
- The error only surfaces on the FIRST NNA drill click (the re-render where
  `geoDrillLevel` transitions from 'state' to 'city')

### 2. Secondary Bug: Missing useMemo Dependencies

The `segments` dependency array was `[cohort, geoDrillLevel, advDrillLevel, selectedStateKey, selectedArchitectKey, baseSegments]` -- missing both `metric` and `nnaDrillData`. This meant:
- Switching between AUA and NNA while drilled would use stale city segments
- Changes to the drill data (e.g., period change) wouldn't recompute segments

### 3. Fix Applied

Two changes in a single commit (`9c1881a`):
1. Moved `nnaDrillData` useMemo declaration from line 1707 to line 1655 (before
   `segments` memo). Added comment: "MUST be declared before `segments` memo which reads it"
2. Added `metric` and `nnaDrillData` to the `segments` dependency array

### 4. Drill Path Verification (All 5 Acceptance Criteria)

| Drill Path | Status | Detail |
|---|---|---|
| GEO state -> city (NNA) | FIXED | `nnaDrillData` now accessible; `by_city` entries map to DonutSegment with `aua=abs(total)`, `client_count=count` |
| City -> client (NNA GEO) | Graceful | No per-relationship data in `by_city` (each entry is DistributionStats, not a segment list). City click toggles selection only. `hasNoDrillData` guard at line 1874 shows "No city-level data available" if segments empty |
| ADV architect -> client (NNA) | Graceful | ADV drill data has `{ distribution, relationship_count }` per architect, no per-relationship segments. `parent?.clients?.length` is false for NNA donut segments. Falls to empty segments -> `hasNoDrillData` UI message |
| GEO state -> city (AUA) | Unaffected | Uses `parent.cities` path (line 1683), not `nnaDrillData` |
| ADV architect -> client (AUA) | Unaffected | Uses `parent.clients` path (line 1694) |

### 5. F3b: Continuous NNA Drill Parity (`3367cd8`)

**Task order:** `ADVI_49FNV3.F3b.continuous-nna-drill-parity.md`

**Data investigation:** Checked `bd-portal-publisher` Lambda for drill data availability:
- `nna_geo_drill`: EXISTS -- `{ [state]: { categories, data } }` (city-level NNA timeseries)
- `nna_adv_drill`: DOES NOT EXIST -- Lambda only emits `nna_adv` (top-level architect NNA)
- No second-level city drill data (city within state is terminal)

**Changes to ContinuousNnaDivergingView:**

| Change | Detail |
|--------|--------|
| ADV drill enabled | Click architect legend item -> filters `nna_adv` to single-architect series (`categories: [drillParent]`). Shows that architect's NNA diverging bars only. |
| Drill state reset | `useEffect(() => setDrillParent(null), [cohort])` -- prevents stale drill on cohort switch |
| CLA-style breadcrumb | Replaced simple back button with breadcrumb: `ChevronLeft All States / StateName` (matches ClaContinuousView pattern) |
| Legend always visible | Categories shown at both levels: drillable with arrow at top, static (no arrow) when drilled. Uses `getCategoryDisplayName()` for consistent label formatting. |
| `canDrill` expanded | Was `cohort === 'geo' && !!data?.nna_geo_drill`. Now also `cohort === 'adv' && !!(nnaSeriesView?.categories?.length)` |
| `drillSeriesView` memo | Changed from inline ternary to `useMemo` with proper dependency tracking |

**Graceful degradation:** Since `nna_adv_drill` doesn't exist, the ADV drill shows the single-architect
series from the top-level `nna_adv` data (filtering categories to just the selected architect). This
produces a valid single-series diverging bar chart -- no error, no dead-end click.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Move declaration, don't restructure | Minimal diff. The memo logic is correct; only the declaration order was wrong. |
| No defensive try-catch | TDZ is a deterministic crash from declaration order, not a data shape issue. Moving the declaration eliminates it permanently. |
| City-to-client and ADV-to-client: accept graceful degradation | EC2 script 09 emits `DistributionStats` per city (not segment lists). ADV drill emits aggregate `distribution` per architect. Neither provides per-relationship detail for donut rendering. Existing `hasNoDrillData` UI handles this correctly. |
| F3b: ADV drill via category filter, not dedicated data | `nna_adv_drill` doesn't exist in Lambda. Filtering `nna_adv` to `categories: [architect]` achieves single-architect view without backend changes. |
| F3b: No second-level GEO drill | `nna_geo_drill[state]` is city-level timeseries -- already terminal. No per-city-relationship data exists in the Lambda output. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | F3-fix: Move nnaDrillData before segments; add metric + nnaDrillData to deps | Yes -- portal DEV `9c1881a` |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | F3b: ADV drill + breadcrumb + legend parity in ContinuousNnaDivergingView | Yes -- portal DEV `3367cd8` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F3-fix.nna-snapshot-drill-error.md` | status -> complete | No -- local only |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F3b.continuous-nna-drill-parity.md` | status -> complete | No -- local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`, workspace `CLOUD`

Two commits: `9c1881a` (F3-fix: snapshot TDZ crash) and `3367cd8` (F3b: continuous drill parity).
F3-fix moved `nnaDrillData` declaration above its consumer memo. F3b added ADV drill to
ContinuousNnaDivergingView (filter to single-architect series from nna_adv), CLA-style breadcrumb,
and always-visible category legend. `bunx tsc -b` clean. No `nna_adv_drill` data exists in Lambda,
so ADV drill uses category filtering as graceful degradation.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push portal DEV** -- commits `594c3f6` (F2/F4/N1-N2) + `9c1881a` (F3-fix) + `3367cd8` (F3b) pending push. DT QA gate.
2. **[0.4.0_DE_ClientPlatform] Review RD commit `594c3f6`** -- F2 projected bars, F4 stacked bar, N1-N2 polish. Still pending DE review.

**Do NOT:**
- Add per-relationship donut segments to city or ADV drill -- the data doesn't exist in the EC2 output and there's no task order requesting it
- Modify `handleSegmentClick` -- the click guard logic is correct, it was only the memo ordering that was wrong
- Add `nna_adv_drill` to the Lambda without a DS task order -- current category filter approach is sufficient

#### benchmark_scatter_granular_selection.md

# Benchmark Scatter Granular Selection — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-06
**Portal DEV commits:** `60f1ee0` -> `0ac188c` -> `5cc598f` -> `b3f3bec` -> `adc5e4c` -> `fcaa484` -> `a1fb029` -> `a493db4` -> `312ca3d`
**Workspace CLOUD commit:** `pending`

## Objective

Add a general/granular state toggle to the Return vs Volatility scatter chart on the
ModelPortfolios Benchmark tab. Clicking a legend item enters granular state: only that
model's circle and paired benchmark diamond are visible, the chart auto-zooms around
them, and persistent tooltip cards appear on both points without hover. Clicking again
returns to general state. Clicking a different model while in granular state switches
context directly.

---

## Work Completed

### 1. Core State + Legend Interaction (`60f1ee0`)

Added `selectedModel: string | null` state. `null` = general, code string = granular.
- `filteredData` filters `scatterData` to the selected model's 2 points in granular state
- Axis domains recalculate from `filteredData` automatically — chart auto-zooms with no
  extra logic
- Model legend `<div>` items converted to `<button>` elements: toggle on same code,
  switch on different code, `opacity-30` on unselected items, white ring + bold label
  on selected item, 200ms transitions throughout

### 2. Persistent Tooltips — Iteration History

Six iterations to arrive at the correct implementation. Documented in full for future reference.

#### Attempt 1 — SVG text labels via `makeShapeRenderer` factory (`0ac188c`, `5cc598f`)
Approach: extend shape renderer to also draw SVG `<rect>` + `<text>` elements as
persistent labels when `showLabel=true`.
Issues: SVG text has no CSS wrapping control, size/content was too abbreviated, and
grid-aware placement (above/below based on return rank + axis padding) was overly
complex for what was essentially a cosmetic layer.
Reverted.

#### Attempt 2 — HTML cards below the chart (`b3f3bec`)
Approach: remove SVG labels entirely; render `<CustomTooltip active={true} ...>`
as a flex row of HTML divs below the `ResponsiveContainer`.
Issue: user wanted tooltips inside the chart adjacent to their data points, not
in a separate section below.
Reverted.

#### Attempt 3 — `Customized` component with `foreignObject` (`adc5e4c`)
Approach: use Recharts' `Customized` component (receives chart internals as props)
to render `<foreignObject>` tooltip cards at pixel positions computed from `xAxisMap`
and `yAxisMap` scales.
Issue: Recharts 3.x deprecated `Customized`. The `xAxisMap`/`yAxisMap` internal
state it relied on no longer exists in v3 — early-return guard always fired, nothing
rendered.

#### Attempt 4 — Recharts 3.x public hooks (`fcaa484`)
Approach: replace `Customized` with a `GranularTooltips` component (direct chart
child) using `useXAxisDomain(0)`, `useYAxisDomain(0)`, `usePlotArea()` — all public
v3 exports. Construct linear scales manually from domain + plot area to compute exact
pixel positions. Render `<foreignObject>` + `<CustomTooltip>`.
Issues: (a) `TH=128` too small — tooltip HTML was ~136px for long model names,
foreignObject clips at declared height. (b) bottom clamp used `plotBottom` (plot area
edge) not `chartHeight` (full SVG height), over-restricting vertical range.

#### Attempt 5 — Fix bottom clip (`a1fb029`)
Added `useChartHeight()` hook; clamp `ty` against `svgHeight - 8` rather than
`plotBottom`. Bumped `TH=160`. Resolved bottom cutoff.

#### Attempt 6 — No-wrap + Z-order (`a493db4`, `312ca3d`)
Two final issues:
1. Text wrapping: long model names wrapped at 220px foreignObject width. Fix: set
   `style={{ whiteSpace: 'nowrap' }}` on wrapper div (inherited by all CustomTooltip
   text); bumped `TW=300`, dropped `TH=130` (single-line content is shorter).
2. Z-order: Recharts 3.x renders custom children through its own pipeline, so
   CartesianGrid could appear after the `<g>` in SVG document order (last = topmost
   in SVG). Fix: `useLayoutEffect` with `svg.appendChild(g)` after each render —
   fires synchronously before browser paint, moves `<g>` to last child of the SVG
   unconditionally. Guard `svg.lastElementChild !== g` makes it a no-op when
   already in position.

### 3. Final Architecture of `GranularTooltips`

```tsx
function GranularTooltips({ points }) {
  const gRef = useRef<SVGGElement>(null)
  useLayoutEffect(() => {
    const g = gRef.current
    if (!g) return
    const svg = g.closest('svg')
    if (svg && svg.lastElementChild !== g) svg.appendChild(g)
  })
  const xDomain = useXAxisDomain(0)   // public Recharts 3.x hook
  const yDomain = useYAxisDomain(0)   // public Recharts 3.x hook
  const plotArea = usePlotArea()      // public Recharts 3.x hook
  const chartHeight = useChartHeight() // public Recharts 3.x hook
  // manual linear scales mirroring XAxis/YAxis
  // model → right of point, benchmark → left, fallback on overflow
  // vertical clamp to [plotTop, svgHeight - 8]
  // <foreignObject> per point, whiteSpace: nowrap, overflow="visible"
  // <CustomTooltip active={true} payload={[{payload: point}]} />
}
```

Hover tooltip (`<Tooltip content={<CustomTooltip />} />`) suppressed in granular
state to avoid double-display.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `useLayoutEffect` for SVG reorder | Fires before paint; no user-visible flicker. `useEffect` would be too late. |
| Public hooks only (`useXAxisDomain`, `usePlotArea`, etc.) | `useXAxis`/`useYAxis` are internal-only in Recharts 3.x, not exported from index |
| Manual linear scale construction | Scale is linear with known domain+range; matches Recharts exactly without private API access |
| `whiteSpace: 'nowrap'` on wrapper div | `white-space` is inherited CSS — cascades to all CustomTooltip text without modifying shared component |
| model → right, benchmark → left | Opposite sides guarantees no overlap; both points share same model code so same X range |
| Hover tooltip suppressed in granular state | Both pinned and hover would show simultaneously; pinned already shows full info |
| BenchmarkHeatmap unaffected | Scoped to scatter chart only per Andrew |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/components/ReturnVolatilityScatter.tsx` | Full granular feature + GranularTooltips | Yes — `312ca3d` (DEV) |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** `DEV` (portal), `CLOUD` (workspace)

`ReturnVolatilityScatter.tsx` is complete through `312ca3d`. Portal DEV pushed to
`origin/DEV`. CLOUD submodule pointer updated and pushed. Feature is live on remote.

---

## Next Steps

None — feature complete and pushed.

**Do NOT:**
- Touch `BenchmarkHeatmap.tsx` — heatmap granular filtering is explicitly out of scope.
- Modify `ModelPortfolios.tsx` — feature is self-contained in `ReturnVolatilityScatter.tsx`.

#### coo_briefing_all_gates_cleared.md

# COO Briefing: All CTO Stall Items Resolved — Phase 3 Unblocked

**Date:** 2026-03-05
**From:** 0.4.0_DE_ClientPlatform
**To:** 2.0.0_SA_COO

---

## Status: All 5 CTO-Flagged Items Resolved

| # | Item | Status | Who | Evidence |
|---|------|--------|-----|----------|
| 1 | DS Phase 2 batch | DEPLOYED | DS committed, DT deployed | Lambda `bd-v2.16.2`, EC2 `bd-v2.16.3` — both tagged and pushed |
| 2 | DT J2/J3 | COMPLETE | DT | Commit `67a400b3`, deployment_map updated, task order marked complete |
| 3 | DE ADVI-006 design brief | COMPLETE | DE | Commit `aaf97585`, brief at `docs/architecture/advisor_intelligence/books_tab_design_brief.md`, task order marked complete |
| 4 | Portal DEV push | PUSHED | DT | `2291669..4b768c3` — 15 commits (RD Phase 1 + Y4 fixes + Y8 AUA stacked bar) |
| 5 | Phase 3 FE task orders | AWAITING COO | -- | All gates cleared |

---

## What's Unblocked

**Phase 3 FE task orders can be issued now.** Both prerequisite gates are satisfied:

1. **DS delivery gate** — DS Phase 2 batch (11 streams: Y2/Y3/Y5/Y6b/Y6c/Y6d/Y7/Y9/Y10/Y11/Y13) is committed, deployed, and live. New data keys available: `growth_decomposition`, `nna_geo`, `nna_adv`, `nna_geo_drill`, `aua_mix`, Y6b city drill, Y6d relationship drill, Y13 monthly stacked bar.

2. **Books design brief gate** — ADVI-006 brief complete with L2/L3/L4 field mappings, 6 backend gaps documented with exact function targets, TypeScript interfaces drafted. Ready for RD task order decomposition.

**Books tab (Y14/Y15/Y16)** — additionally unblocked by DT J2/J3 completion (auth-handler + authorizer deployed).

---

## Action Required

COO to issue Phase 3 FE task orders. DE is reactive until received.

#### coo_handoff_pod4_state_validation.md

# COO Handoff: Pod 4 State Validation — 2026-03-05

**From:** 0.4.0_DE_ClientPlatform
**To:** 2.0.0_SA_COO
**Date:** 2026-03-05
**Scope:** Full pod 4 agent state audit — DE, DT, DS, RD_AdvisorIntelligence, RD_ModelPortfolios

---

## Summary

ADVI_YANGV2 Phases 1–4 are fully implemented and approved. Portal DEV has 5 unpushed
commits awaiting DT push. DS has two additional research outputs (NNA canonical fix +
orphan theory disproof) that are committed but **awaiting CEO decision** before a gold
layer rebuild can be triggered. RD_ModelPortfolios has no active work. No open DE task
orders remain.

---

## Agent-by-Agent State

### 0.4.0_DE_ClientPlatform — IDLE / COMPLETE

**Last active:** 2026-03-05
**Open task orders:** 0 (all complete)

| Task Order | Status |
|---|---|
| `ADVI_V1VERS.004.portal-types-wiring.md` | complete |
| `ADVI_V1VERS.006.books-design-brief.md` | complete |
| `ADVI_YANGV2.Y-phase3.de-type-wiring.md` | complete |
| `macro_project_code_retroactive_cleanup.md` | complete |

**What was done this session:**
- Reviewed and approved all 4 Phase 3 RD commits (`7460f35` → `9b902dc`): Y3-FE, Y5-FE,
  Y6b/Y6d/Y9, Y13, Y15. tsc clean confirmed.
- Executed retroactive macro/project code cleanup across pod 4 (27 renames, 14 XML
  metadata updates, CLOUD commit `ad206388`).

**Status:** Reactive. Awaiting new task orders from COO.

---

### 0.4.0_DT_ClientPlatform — IDLE / PENDING PUSH

**Last active:** 2026-03-04 (bd-v2.16.2 / bd-v2.16.3 deploy + J2/J3 + portal submodule push)
**Open task orders:** 0 (J2/J3 complete; deployment_audit superseded)

**Latest deployment tags:**

| Tag | What | Status |
|---|---|---|
| `bd-v2.15.0` | bd-portal-publisher (adv_drill + cla) | DEPLOYED |
| `bd-v2.15.1` | bd-gold-layer-runner (script 10) | DEPLOYED |
| `bd-v2.16.1` | HOTFIX account_performance date fallback | DEPLOYED |
| `bd-v2.16.2` | bd-portal-publisher Yang V2 Phase 2 (Y3/Y5/Y9) | DEPLOYED |
| `bd-v2.16.3` | bd-gold-layer-runner Yang V2 Phase 2 (Y6b/Y6c/Y6d/Y7/Y13) | DEPLOYED |

**PENDING — Portal DEV push:** DT last pushed portal DEV at `4b768c3`. Five new
approved commits are sitting locally:

| Commit | Author | Description |
|---|---|---|
| `542197c` | DE | Y3/Y5/Y6b/Y6c/Y6d/Y9/Y13/Y15 type wiring |
| `7460f35` | RD | Y3-FE AUA mix sub-toggle + Y5-FE GRO mode |
| `0bd3f66` | RD | Y6b/Y6d snapshot drill + Y9 continuous NNA bar |
| `54163de` | RD | Y13 rolling flows diverging bar |
| `9b902dc` | RD | Y15 Books tab L2/L3/L4 MVP |

**Action required from COO:** Issue DT a push order for portal DEV through `9b902dc`.

---

### 0.4.0_DS_ClientPlatform — IDLE / CEO DECISION PENDING

**Last active:** 2026-03-05
**Open task orders:** 0 (all V1VERS and YANGV2 task orders complete)

**What is deployed (CLOUD, part of bd-v2.16.2/v2.16.3):**
- Y2: NMNC/NMEC classification confirmed correct — no patch needed
- Y3: Asset class AUA mix (holdings_lots join) — Lambda deployed
- Y5: Growth decomposition time series — Lambda deployed
- Y6b: City-level NNA drill data — script 09 deployed
- Y6c: Outflows quartile inversion fix — script 09 deployed
- Y6d: Relationship-level ADV drill data — script 09 deployed
- Y7: Single-account AUA binning fix — script 09 deployed
- Y9: Diverging NNA bar data at all drill levels — Lambda deployed
- Y10: QTD/YTD math bug — investigated and fixed
- Y11: "Advisor" field investigation — no distinct Advisor field exists in BD gold layer (confirmed); Y11 resolved as "no Advisor toggle possible"
- Y13: Monthly stacked_bar granularity — script 10 deployed

**Two additional DS outputs NOT in a task order (research-driven):**

**1. NNA canonical classification fix (commits `9bfb289b`, `b4f2d7a7`):**
DS discovered that BD's NNA figures undercount Schwab's by ~40% due to phantom
flows from internal journal entries (`JNL - LONG` / `JNL - SHORT`) and Schwab-internal
cash sweeps (`TRF BTWN SCH ACCTS`, `TO SEP ACCT MGR`, `FDIC sweeps`). Fix is committed
to `05_build_client_performance.py` and `05b_build_account_performance.py`.

**Status: Awaiting CEO approval before gold layer rebuild.** The fix would require
re-running the full gold layer pipeline and redeploying. Net NNA impact is small
(-$1.5M over 4 months), but accuracy improvement is material (12,050 phantom events
removed). DS logged this as requiring CEO decision, not a routine DT deploy.

**2. ACAT orphan theory disproof (log: `smoke_test_orphan_theory.md`):**
DS investigated whether BD has missing ACAT transaction records that explain the
Schwab NNA gap. **Conclusion: Disproven.** BD transaction coverage is complete (0%
orphan rate). The NNA gap is entirely a cash flow classification boundary issue, not
a data completeness gap. No allocation-diff pipeline is warranted.

**Action required from COO/CEO:** Decide whether to approve the NNA canonical
classification rebuild (commits `9bfb289b` + `b4f2d7a7`). If approved, DT deploys
via `safe-ec2-deploy.sh` followed by a triggered pipeline run.

---

### 0.4.2_RD_AdvisorIntelligence — IDLE / COMPLETE

**Last active:** 2026-03-05 (portal DEV `9b902dc`)
**Open task orders:** 0 (all 8 YANGV2 task orders complete)

**Completed YANGV2 FE streams:**

| Commit | Streams | Status |
|---|---|---|
| `f9c0e59` | Y1, Y4 (partial), Y6, Y12 | complete |
| `76c7621` → `2981133` | Y4 final fix | complete |
| `4b768c3` | Y8 | complete — pushed to remote |
| `7460f35` | Y3-FE, Y5-FE | complete — awaiting DT push |
| `0bd3f66` | Y6b-FE, Y6d-FE, Y9-FE | complete — awaiting DT push |
| `54163de` | Y13-FE | complete — awaiting DT push |
| `9b902dc` | Y15 Books L2/L3/L4 | complete — awaiting DT push |

**What Y15 covers:** L2 advisor book summary (AUA/clients/NNA/growth KPIs, tax
exposure, engagement, clients table), L3 client detail (getBooksClientDetail endpoint,
taxable open lots with term filter), L4 inline account drill (open_lots filtered by
account_id). Admin/internal gate (`isInternal() || isDev()`) maintained.

**Unimplemented YANGV2 streams (no task orders issued):**
- Y2: NMNC/NMEC audit — resolved as no-op (DS confirmed classification is correct)
- Y11: Advisor toggle — resolved as no data (DS confirmed no Advisor field exists)
- Y14: Books access gating — blocked on J1→J2→J3 chain (J2/J3 now live; J1 AE work)
- Y17: AI RAG executive summary — deferred, flagged for separate PRD

---

### 0.4.1_RD_ModelPortfolios — NO ACTIVE WORK

**Last active:** Unknown (no log entries in any date folder)
**Open task orders:** `page_inventory.md`, `xtick_spacing_fix.md` (check statuses)
**Status:** Dormant. No YANGV2 work assigned to this agent. ModelPortfolios page
not part of the Yang V2 feedback scope.

---

## Open Items by Priority

### P0 — Blocked on DT push

**Portal DEV has 5 approved commits not yet on remote.** All Phase 3 FE work (Books tab,
Y13 rolling flows, Y6b/Y6d drills, Y3-FE AUA mix, Y5-FE GRO mode) is sitting in local
portal DEV at `9b902dc`. None of this is visible to users until DT pushes and a portal
PROD build runs.

**Assign:** 0.4.0_DT_ClientPlatform push portal DEV → `9b902dc`.

---

### P1 — CEO Decision Required

**NNA canonical classification fix** is committed but not deployed. The fix removes
12,050 phantom events (internal journals + Schwab sweeps) from NNA computation. Net
dollar impact is small. Accuracy improvement is material. Requires CEO direction because
it changes the definition of a core metric (NNA) and the gold layer rebuild touches the
full pipeline.

**Assign:** Andrew/Yang to decide. If approved → DT deploys scripts 05/05b + triggers
pipeline run → gold layer updates.

---

### P2 — Y14 Books Access Gating (J1 dependency)

Books tab is live (Y15 implemented) but showing admin-only content. The access model
(advisors see only their own book) depends on the full J1→J2→J3 partner identity chain.
J2/J3 (auth-handler + authorizer passthrough) are deployed as of bd-v2.16.2. J1
(DynamoDB `opal-partner-49financial` table with `advisorKey` mapping) is an AE task
(0.7.0_AE_CloudOps).

**Status:** J1 is the only remaining gate. AE has the task order
(`ADVI_V1VERS.J1.partner-identity-dynamo.md`).

---

### P3 — Y17 AI RAG Executive Summary (Deferred)

Three-level AI-generated summaries (firm/advisor/client) defined in the Yang V2 PRD
Section 4.5. Marked as requiring a separate mini-PRD. High effort. No agents assigned.
DS (context design) + 0.7.0_AE_CloudOps (Lambda + Claude API infrastructure) are the
leads when this is activated.

**Assign:** COO to decide when to open Y17 track and issue mini-PRD.

---

## ADVI_YANGV2 Completion Scorecard

| Phase | Streams | Status |
|---|---|---|
| Phase 1 — Visual (no data dep) | Y1, Y4, Y6, Y8, Y12 | COMPLETE + deployed to portal remote |
| Phase 2 — DS data batch | Y2, Y3, Y5, Y6b, Y6c, Y6d, Y7, Y9, Y10, Y11, Y13 | COMPLETE — bd-v2.16.2 / bd-v2.16.3 live |
| Phase 3 — FE integration | Y3-FE, Y5-FE, Y6b-FE, Y6d-FE, Y9-FE, Y13-FE | COMPLETE — portal DEV `9b902dc`, DT push pending |
| Phase 4 — Books | Y15 L2/L3/L4 | COMPLETE — portal DEV `9b902dc`, DT push pending |
| Phase 5 — AI Summary | Y17 | NOT STARTED — deferred |

Resolved as no-ops: Y2 (classification correct), Y11 (no Advisor field in data)
Blocked on external: Y14 (J1 AE gate), Y17 (deferred)

---

## Recommended COO Actions

1. **Issue DT push order** for portal DEV `9b902dc` — highest priority, unblocks Y15 Books tab for users
2. **Escalate NNA canonical fix** to CEO (Andrew/Yang) for go/no-go on gold layer rebuild
3. **Check J1 AE status** — `ADVI_V1VERS.J1.partner-identity-dynamo.md` in 0.7.0_AE_CloudOps task_orders; if complete, Y14 access gating can be activated
4. **Decide Y17 timeline** — open AI RAG mini-PRD when Books tab is stable post-Y14

#### rd_phase3_review_all_complete.md

# RD Phase 3 Review — All 4 Task Orders Complete — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-05
**Portal DEV commits reviewed:** `7460f35` -> `0bd3f66` -> `54163de` -> `9b902dc`
**Workspace CLOUD commit:** pending (this log + task order status updates)

## Objective

Review all Phase 3 RD portal DEV commits (4 commits covering Y3-FE, Y5-FE, Y6b-FE, Y6d-FE, Y9-FE, Y13-FE, Y15) for correctness, type safety, task order compliance, and tsc cleanliness. Mark all task orders complete if approved.

---

## Work Completed

### 1. 7460f35 — Y3-FE AUA mix sub-toggle + Y5-FE GRO growth decomposition mode

**Files:** `PartnerAnalytics.tsx` — 3 files, -100/+170 lines.

**Y3-FE (AUA Mix):** New `auaSubMode` state (`'clients' | 'mix'`). Secondary toggle rendered inside AUA panel content area. `mix` view iterates `aua_mix` data from DS Phase 2 response key — segments mapped with appropriate color styling. No data fetching changes. Type-safe against `AuaMixView` added in `542197c`.

**Y5-FE (Growth Decomposition):** New `growthMode` state (`'standard' | 'decomposition'`). Decomposition path renders `GrowthDecompositionView` from DS response `growth_decomposition` key. Standard path unchanged.

**Compliance check:** No emojis. No API calls added. No shared type mutations. `tsc` clean.

**Verdict: APPROVED.**

---

### 2. 0bd3f66 — Y6b/Y6d snapshot NNA drill + Y9-FE continuous NNA diverging bar

**Files:** `DistributionTab.tsx` — 3 files, -60/+196 lines.

**Y6b-FE (GEO snapshot drill):** Click handler on state-level bars opens drill-down view. State selected stores `selectedGeoState`. Drill uses `nna_geo_drill` key on `CumulativeChartResponse` — matches `NNAGeoDrillView` type. Back button clears selection.

**Y6d-FE (Relationship drill):** Same pattern on ADV snapshot. `selectedDrillKey` state. Drill uses `drill` key on `NnaView` — matches `NNADistributionDrill` type.

**Y9-FE (Continuous NNA diverging bar):** `ComposedChart` with `stackOffset="sign"` — inflows above zero, outflows below. Uses `nna_series` and `nna_adv` keys from `CumulativeChartResponse`. Type-safe against `NNASeriesView`/`NNAGeoDrillView` from `542197c`.

**Compliance check:** No emojis. No shared type mutations. `tsc` clean.

**Verdict: APPROVED.**

---

### 3. 54163de — Y13-FE rolling flows per-period diverging bar with interval toggle

**Files:** `AdvisorsTab.tsx` — 2 files, -45/+111 lines.

Replaced per-advisor stacked bar (deprecated by Yang feedback removing advisor-level breakdown) with per-period aggregate diverging bar. `ComposedChart` with `stackOffset="sign"`. Interval toggle (Month/Quarter/Year) drives `aggregatedFlowsData` memo — sums `inflow`/`outflow` per period from `monthly` key on `AdvisorRollingFlowsResponseV2`. Type-safe against `monthly?` added in `542197c`. No advisor-row loop in chart anymore — aggregate only. Correct per task order requirement.

**Compliance check:** No emojis. No API calls changed. `tsc` clean.

**Verdict: APPROVED.**

---

### 4. 9b902dc — Y15 Books tab L2/L3/L4 MVP

**Files:** `ClientsTab.tsx` + supporting files — 4 files, -270/+380+ lines. Largest Phase 3 commit.

**L2 (Advisor Book Summary):** AUA/clients/accounts/NNA/growth KPI cards using `AdvisorBookResponse` (existing type, existing `getAdvisorBook()` endpoint). Tax Exposure panel. Engagement panel (flows TTM + avg tenure). Clients table with row click triggering L3.

**L3 (Client Detail):** Activated by `selectedClientKey`. Calls `getBooksClientDetail(clientKey)` — the new endpoint wired in `542197c`. Uses `BooksClientDetailResponse`. Taxable Open Lots panel with term filter (ST/LT/All). Account table.

**L4 (Inline Account Drill):** `selectedAccountId` state. Drills `open_lots` array filtered by `account_id` and `term`. Renders inline below account table row, no modal/routing.

**Key compliance checks:**
- `income_fees` and `portfolio_composition` panels: all references are in removed lines (`-`), none in added code. Correctly hidden per task order and ADVI-006 brief.
- `isInternal() || isDev()` gate: maintained at component top level.
- "Taxable Open Lots" label used (not "Holdings").
- `getBooksClientDetail` (not legacy `getClientDetail`).
- No emojis. `tsc` clean.

**Verdict: APPROVED.**

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| All 4 task orders marked complete | All commits pass type safety, task order compliance, and tsc checks |
| No follow-up type changes required | RD consumed all types from `542197c` correctly; no gaps found |
| Y15 `BooksClientDetailResponse` naming validated | RD used the correct name (not legacy `ClientDetailResponse`) |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y3-Y5-FE-header-panel.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y6b-Y6d-Y9-FE-drill-and-continuous-nna.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y13-FE-rolling-flows-nna-bar.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y15-books-tab-l2-l3-l4.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-05/rd_phase3_review_all_complete.md` | This log | Yes -- CLOUD (this commit) |

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

All Phase 3 DE responsibilities complete. RD delivered all 4 Phase 3 task orders (Y3/Y5, Y6b/Y6d/Y9, Y13, Y15) — 4 portal DEV commits (`7460f35` -> `0bd3f66` -> `54163de` -> `9b902dc`) reviewed, approved, and task orders marked complete. tsc clean confirmed. Portal DEV now has 20 approved commits total (20 commits ahead of last DT push at `4b768c3`, now advanced to `9b902dc`). No open DE task orders remain.

---

## Next Steps

1. **[DT] Push portal DEV** — 4 new approved commits (`7460f35` -> `0bd3f66` -> `54163de` -> `9b902dc`), brings portal DEV to `9b902dc`
2. **[COO/CTO] Review Phase 3 completeness** — all Yang V2 FE streams (Y3/Y5/Y6b/Y6d/Y8/Y9/Y13/Y15) implemented and approved
3. **[DE] Await next task orders** — reactive until new work arrives

**Do NOT:**
- Touch `portal/` — all portal work belongs to DT push gate
- Mark any RD task orders without reading the commit diffs

#### rd_y4_y8_review_and_advi006_brief.md

# RD Y4/Y8 Commit Review + ADVI-006 Books Design Brief — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-05
**Portal DEV commits reviewed:** `f9c0e59` -> `76c7621` -> `7258c5e` -> `2981133` -> `4b768c3`
**Workspace CLOUD commit:** pending (this log + brief commit)

## Objective

Catch-up review of 5 new RD portal DEV commits (4 Y4 fixes + 1 Y8 feature) not covered by prior session logs. Then execute ADVI-006 task order: write Books tab design brief.

---

## Reviews Completed

### f9c0e59 — Y1+Y4+Y6+Y12 phase 1 visual fixes

3 files, -332/+39 lines. Scope:
- **PartnerAnalytics.tsx**: Y1 reversed `barCategories` (NMEC bottom, NMNC top). Y4 added `stackOffset="sign"` to NNA ComposedChart.
- **AdvisorsTab.tsx**: Y12 removal of 1Y Rolling view per Yang feedback. Deleted `RollingFlowsChart`, `Rolling1YChart`, unused state (`flowsMetric`, `flowsWindow`, `flowsView`), unused types/constants. Rolling Flows panel simplified to stacked bar only. Clean dead code removal — no chart logic altered.
- **DistributionTab.tsx**: Y6 NNA distribution filter — exclude histogram bins within [-1000, 1000] range. Added explanatory footnote for the exclusion.

No emojis. No data fetching changes. **Verdict: APPROVED.**

### 76c7621 — Y4 fix: net line at actual NNA value, not midpoint

1 file, -4/+2 lines. Removed incorrect midpoint computation for NNA net line; now uses `net` directly (= actual NNA = inflows + outflows). **Verdict: APPROVED.**

### 7258c5e — Y4 fix: remove stackId from NNA bars

1 file, -2/+2 lines. Intermediate iteration — removed `stackId="nna"` to test independent bar rendering. Superseded by next commit. **Verdict: APPROVED (iteration).**

### 2981133 — Y4 fix: align NNA bars on same x-position

1 file, -2/+3 lines. Re-added `stackId="nna"` on both inflow/outflow bars, extracted variables for clarity. Final correct state: stacked bars with `stackOffset="sign"` makes inflows above 0, outflows below 0, both on same x-position. **Verdict: APPROVED.**

### 4b768c3 — Y8 continuous AUA area-to-stacked-bar + interval toggle

1 file (DistributionTab.tsx), -115/+141 lines. Major visual change:
- Replaced `AreaChart`/`Area` with `BarChart`/`Bar` for continuous AUA view.
- New `auaInterval` state: Month/Quarter/Year toggle. `aggregatedBarData` memo takes last data point per period (end-of-period snapshot — correct for cumulative AUA).
- NMNC renders on top (Y1 consistency via `[...displayCategories].reverse()`).
- Tooltip uses `periodLabel` instead of raw date. `stackId="aua"`. Top bar gets `radius={[4, 4, 0, 0]}`.
- No new API calls, no type changes, no emojis.

**Verdict: APPROVED.**

---

## DT Signal

All 5 portal DEV commits approved. Combined with prior session approval (10 commits), DT is cleared to push full portal DEV history.

---

## ADVI-006 Design Brief

Executed task order `ADVI-006-books_design_brief.md`. Synthesized thread turns 6 (DE scope), 7 (DS data confirmation), 8 (RD layout spec) into `docs/architecture/advisor_intelligence/books_tab_design_brief.md`.

---

## Phase 3 Type Wiring (ADVI-Y-phase3-de-type-wiring)

Executed COO task order. Added all TypeScript types for DS Phase 2 deployed data + ADVI-006 Books types. This unblocks all Phase 3 RD task orders.

Portal DEV commit `542197c`:

**Extended existing types:**
- `DistributionStats`: +`inflow_percentiles`, `outflow_percentiles`, `inflow_count`, `outflow_count` (Y6c)
- `NnaView`: +`drill?: NNADistributionDrill` (Y6b/Y6d)
- `CumulativeChartResponse`: +`growth_decomposition?`, `nna_geo?`, `nna_adv?`, `nna_geo_drill?`, `aua_mix?` (Y5/Y9/Y3)
- `AdvisorRollingFlowsResponseV2`: +`monthly?` (Y13)

**New types added:**
- Y6b/Y6d: `NNADistributionDrillEntry`, `NNADistributionDrill`
- Y5: `GrowthDecompositionPoint`, `GrowthDecompositionView`
- Y9: `NNASeriesPoint`, `NNASeriesView`, `NNAGeoDrillView`
- Y3: `AuaMixSegment`, `AuaMixPoint`, `AuaMixView`
- Y15: `BooksClientDetailResponse`, `BooksClientAccount`, `BooksClientTaxDetail`, `CostBasisYear`, `GainPosition`, `OpenLot`

**New endpoint:** `getBooksClientDetail(clientKey)` in `advisor-intelligence.ts`

**Note on Y15 naming:** Design brief specified `ClientDetailResponse` but that name was already taken by the legacy `clients_tab.json` type (line 777). Named `BooksClientDetailResponse` to avoid collision per task order constraint "do not modify existing types." Existing `AdvisorBookResponse` (line 901) already covers L2 — no new L2 type needed. Existing `getAdvisorBook()` endpoint already wired.

tsc clean (no errors).

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-05/rd_y4_y8_review_and_advi006_brief.md` | This log | Yes -- CLOUD `aaf97585` (initial), updated this commit |
| `docs/architecture/advisor_intelligence/books_tab_design_brief.md` | ADVI-006 deliverable | Yes -- CLOUD `aaf97585` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-006-books_design_brief.md` | Status: pending -> complete | Yes -- CLOUD `aaf97585` |
| `portal/src/pages/AdvisorIntelligence/types.ts` | +184 lines: Y3/Y5/Y6b/Y6c/Y6d/Y9/Y13/Y15 types | Yes -- portal DEV `542197c` |
| `portal/src/api/endpoints/advisor-intelligence.ts` | +BooksClientDetailResponse import, +getBooksClientDetail() | Yes -- portal DEV `542197c` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-Y-phase3-de-type-wiring.md` | Status: pending -> complete | Yes -- CLOUD (this commit) |

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

All DE responsibilities cleared:
- 16 portal DEV commits approved (10 prior + 5 RD review + 1 type wiring `542197c`)
- ADVI-006 design brief written and committed
- Phase 3 type wiring complete — RD is unblocked
- Both task orders marked complete

---

## Next Steps

1. **[DT] Push portal DEV** -- 16 commits approved (must include `542197c`)
2. **[COO] Issue Phase 3 RD task orders** -- all gates cleared (DS delivered, types wired, brief done)
3. **[DE] Await Phase 3 RD output** -- reactive until RD commits land

#### task_order_completeness_audit.md

# Task Order Completeness Audit: ADVI_V1VERS + ADVI_YANGV2 — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-05
**Method:** Full sweep of all task orders in both project namespaces + all ad-hoc task orders
across pod 4. Blocker Verification Protocol (AGENT_START_HERE.md) applied to every
non-complete item before any BLOCKED or AMBIGUOUS designation.

---

## 1. Complete Task Order Status Table

### ADVI_V1VERS

| Task Order | Agent | Status | Verification |
|---|---|---|---|
| `ADVI_V1VERS.004.portal-types-wiring.md` | DE | **complete** | Portal DEV `7df26bb` |
| `ADVI_V1VERS.006.books-design-brief.md` | DE | **complete** | CLOUD `aaf97585`, brief at `docs/architecture/advisor_intelligence/books_tab_design_brief.md` |
| `ADVI_V1VERS.004.adv-drill-cla.md` | DS | **complete** | CLOUD `cc3ad9fa` (adv_drill + cla in bd-portal-publisher) |
| `ADVI_V1VERS.005.rolling-flows-data.md` | DS | **complete** | CLOUD `6a3ff256` (stacked_bar + monthly in script 10) |
| `ADVI_V1VERS.J1.partner-identity-dynamo.md` | AE | **complete** | VERIFIED — see section 3 |
| `ADVI_V1VERS.J2-J3.auth-handler-authorizer.md` | DT | **complete** | VERIFIED — see section 3 |
| `ADVI_V1VERS.004.distribution-continuous.md` | RD | **complete** | Portal DEV (C2/C4 in DistributionTab) |
| `ADVI_V1VERS.005.advisors-tab.md` | RD | **complete** | Portal DEV (stacked bar + rolling 1Y rendered) |

**V1VERS: 8 of 8 task orders complete.**

---

### ADVI_YANGV2

| Task Order | Agent | Status | Verification |
|---|---|---|---|
| `ADVI_YANGV2.Y-phase2.ds-data-batch.md` | DS | **complete** | CLOUD `0c9bb501`/`cc3ad9fa`/`6a3ff256`, deployed bd-v2.16.2/v2.16.3 |
| `ADVI_YANGV2.Y-phase3.de-type-wiring.md` | DE | **complete** | Portal DEV `542197c` |
| `ADVI_YANGV2.Y1-Y4-Y6-Y12.phase1-visual.md` | RD | **complete** | Portal DEV `f9c0e59`→`2981133` |
| `ADVI_YANGV2.Y8.continuous-aua-stacked-bar.md` | RD | **complete** | Portal DEV `4b768c3` (pushed to remote) |
| `ADVI_YANGV2.Y3-Y5.fe-header-panel.md` | RD | **complete** | Portal DEV `7460f35` |
| `ADVI_YANGV2.Y6b-Y6d-Y9.fe-drill-and-continuous-nna.md` | RD | **complete** | Portal DEV `0bd3f66` |
| `ADVI_YANGV2.Y13.fe-rolling-flows-nna-bar.md` | RD | **complete** | Portal DEV `54163de` |
| `ADVI_YANGV2.Y15.books-tab-l2-l3-l4.md` | RD | **complete** | Portal DEV `9b902dc` |
| `ADVI_YANGV2.portal-push.phase3.md` | DT | **PENDING** | Not started — see section 2 |

**YANGV2: 8 of 9 task orders complete. 1 pending (DT portal push).**

---

### Ad-hoc task orders (pre-namespace, still active scope)

| Task Order | Agent | Status | Notes |
|---|---|---|---|
| `advi_c1_geo_continuous.md` | RD | **complete** | DistributionTab C1 (continuous GEO NNA) done |
| `advi_c3_cla_snapshot.md` + addendum | RD | **complete** | CLA snapshot view done |
| `advi_h_portal_primitives.md` | RD | **complete** | Portal primitives refactor done |
| `advi_i_top_performers.md` | RD | **complete** | Top performers visual done |
| `continuous_view_max_window_clients_fix.md` | RD | **complete** | Done |
| `distribution_nomenclature_fix.md` | RD | **complete** | Done |
| `xtick_spacing_fix.md` + addendum | RD | **complete** | Done |
| `advi_a4_bell_curve_verify.md` | DS | **complete** | Snapshot NNA bell curve verified — no patch needed |
| `advi_a5_users_v2_mapping.md` | DS | **complete** | Scenario C — no advisorKey mapping exists in opal-users-v2 |
| `acat-inkind-nna-testing.md` | DS | **PENDING** | Not blocked — see section 2 |
| `HOTFIX-drilldown-account-perf-fallback.md` | DT | **complete** | bd-v2.16.1 deployed |
| `deployment_audit.md` | DT | **superseded** | Superseded by deployment_map.xml |

---

## 2. Open Items — Detailed Status

### OPEN #1 — DT: ADVI_YANGV2.portal-push.phase3.md

**Status: PENDING (not blocked)**

**What:** Push portal DEV to remote origin/DEV through `9b902dc` (5 commits:
`542197c` → `7460f35` → `0bd3f66` → `54163de` → `9b902dc`). Update parent repo
submodule pointer on CLOUD.

**Blocker Verification (Protocol Step 1–3):**
- Step 1: Checked DT's task order — no dependency agents listed. Task order states
  "No code changes — push only."
- Step 2: No dependency to check — this is a standalone push with all prereqs already
  satisfied (DE-reviewed at `f9161bed`, commits DE-approved).
- Step 3: **Not blocked.** DT can execute immediately.

**Who acts:** 0.4.0_DT_ClientPlatform
**What they do:** `cd portal && git push origin DEV`, then update CLOUD submodule pointer.
**Impact of not doing:** Y3-FE, Y5-FE, Y6b-FE, Y6d-FE, Y9-FE, Y13-FE, Y15 all
unreachable on remote. The Books tab, GRO mode, NNA drills, and rolling flows bar are
invisible to the server deployment pipeline until this push happens.

---

### OPEN #2 — DS: acat-inkind-nna-testing.md (Steps 2–5 pending)

**Status: IN PROGRESS (not blocked on Steps 1–2; BLOCKED on Steps 3–5)**

**What:** CEO-directed investigation of ACAT in-kind NNA undercount ($106M inflow gap
vs Schwab TOA). 5-step task order.

**Step 1 (commit scripts):** COMPLETE — `90424dba` committed `diag_acat_inkind_scan_v1/v2/v3.py`.

**Step 2 (write DT brief):** NOT DONE. `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md`
does not exist. DS's 2026-03-05 session logs (`canonical_nna_logic.md`,
`smoke_test_orphan_theory.md`) make no mention of this brief. This is DS's next action
and they can execute it now — no dependency.

**Steps 3–5 (DT run → DS analysis → DS production design brief):**
**Blocker Verification for Steps 3–5:**
- Step 1 (protocol): Checked DT task orders — no ACAT EC2 run task order issued to DT yet. The brief (Step 2) is the prerequisite.
- Step 2 (protocol): DS has not written the brief that would trigger DT's action.
- Step 3 (protocol): **BLOCKED on DS completing Step 2** (DT brief not written → DT cannot act → DS cannot read output → DS cannot write analysis or design brief).
  Evidence: `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md` does not exist. DT task orders contain no ACAT item.

**Who acts next:** 0.4.0_DS_ClientPlatform — write `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md`.
**Then:** 0.4.0_DT_ClientPlatform — upload v3 to S3, run on EC2, capture output.
**Then:** DS — read S3 output, write analysis + production design brief.

---

## 3. Blocker Verification: J1 + J2/J3 (Cited as Y14 Gate)

Both items are cited as gating Y14 (Books access gating). Applied full protocol.

### J1 — opal-partner-49financial DynamoDB table (AE)

**Blocker Verification:**
- Step 1: Read `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-04/advi_j1_partner_identity_dynamo_deploy.md`.
  Log documents full deploy sequence:
  - CLOUD commit `1b918471`: `feat(shared-infra): opal-partner-49financial DynamoDB table + IAM read policy`
  - `terraform apply`: 2 added, 0 destroyed, 0-diff confirmed
  - AWS CLI verification: table ACTIVE, hash_key=email, ByAdvisorRole GSI present
  - Table ARN: `arn:aws:dynamodb:us-east-1:313476888478:table/opal-partner-49financial`
  - Tag `shared-infra-v1.3.0` applied and pushed (confirmed: `git tag -l "shared-infra-*"` returns v1.3.0)
- Step 2: Log and git tag both corroborate delivery. Task order marked complete.
- Step 3: **Not blocked. J1 is verified complete.**

### J2/J3 — auth-handler + portal-authorizer (DT)

**Blocker Verification:**
- Step 1: Checked DT CLOUD commits.
  - `de023eed`: `feat(portal-authorizer): J3 -- pass advisorKey/advisorName/advisorRole to Lambda context (ADVI-J3)`
  - `ba0cbc19`: `0.4.0_DT_ClientPlatform: deployment_map.xml -- portal-auth J2/J3 (v1.1.0/v1.2.0)`
  - `67a400b3`: `0.4.0_DT_ClientPlatform: deployment_map.xml bd-v2.16.2/bd-v2.16.3 + J2/J3 complete`
  - DT task order `ADVI_V1VERS.J2-J3.auth-handler-authorizer.md` status: complete
- Step 2: Multiple CLOUD commits + task order corroborate delivery.
- Step 3: **Not blocked. J2/J3 verified complete.**

**Consequence for Y14:** J1 + J2 + J3 are all confirmed live. The auth chain that
gates Books advisor access is complete. Y14 is **unblocked**. No task order has been
issued for Y14 implementation.

---

## 4. Untouched PRD Streams (No Task Orders Issued)

The Yang V2 PRD (Section 5) defines 21 streams. The following were never given task orders:

| Stream | Why No Task Order | Current State |
|---|---|---|
| **Y2** — NMNC/NMEC period-bookend audit | DS investigated and found no patch needed | Resolved as no-op (data_contract.xml documents finding) |
| **Y11** — Advisor field investigation | DS investigated; no distinct Advisor field exists in BD gold | Resolved as no-op. Y13 Advisor toggle cannot be built. |
| **Y14** — Books access gating (portal) | Was gated on J1+J2+J3. Now unblocked. No task order issued. | **GAP — see section 5** |
| **Y17** — AI RAG executive summary | Deferred by CTO/COO; flagged for separate mini-PRD | Intentionally deferred |

Y2 and Y11 are legitimately closed without task orders (investigation-only, resolved
as no-ops). Y17 is intentionally deferred. **Y14 is a gap** — the gate cleared,
but no task order was ever issued for the implementation.

---

## 5. Y14 Gap Analysis — Books Access Gating

**What Y14 requires (from Yang V2 PRD Section 4.1):**

The Books tab (`ClientsTab.tsx`) currently gates all content behind `isInternal() || isDev()`.
Y14 is the switch from this admin-only model to a role-based model where:
- Admin users (internal/dev) see all advisors via dropdown — unchanged
- Authenticated advisor users see **only their own book** — new behavior
- The JWT (now containing `advisorKey`, `advisorName`, `advisorRole` via J3) is the
  identity source

**What the auth chain delivers (verified above):**
- `advisorKey`, `advisorName`, `advisorRole` are injected into the Lambda context by
  the portal-authorizer (J3)
- The auth-handler reads `opal-partner-49financial` at login to resolve portal user
  email → advisor identity (J2)
- The table exists and is empty (J1) — **populated at advisor onboarding time by Andrew**

**What is still needed for Y14:**
1. **RD task order** — `ClientsTab.tsx` needs to read `advisorKey` from auth context
   and scope the Books content to that advisor when the user is not admin/internal
2. **Portal API/backend** — the `getAdvisorBook(advisorKey)` call must be scoped to
   the logged-in advisor's key (currently the advisory key is likely hardcoded or passed
   via admin selector)
3. **Population gate** — Y14 cannot be used by real advisors until `opal-partner-49financial`
   has their email → advisorKey entries (Andrew's manual action)

**Note:** Y14 is frontend-only (RD + DE), no new Lambda or data work needed. The
backend auth chain is complete. The portal just needs to read the advisor identity from
the JWT claims and conditionally scope the Books view.

---

## 6. Committed-But-Undeployed Code

Two DS commits are on CLOUD but not deployed — separate from the task order system:

| Commits | What | Status |
|---|---|---|
| `9bfb289b` + `b4f2d7a7` | NNA canonical classification fix (scripts 05 + 05b — exclude JNL journals and Schwab sweeps) | **Awaiting CEO go/no-go before DT triggers gold layer rebuild** |

This is not tracked in any task order. The fix was research-driven (Schwab SOT
cross-reference session). CEO decision is the gate.

---

## 7. Action Summary for COO

| Priority | Action | Owner | Unblocks |
|---|---|---|---|
| P0 | Execute portal DEV push (`ADVI_YANGV2.portal-push.phase3.md`) | **DT** | Y15 Books tab, Y3-FE/Y5-FE/Y6b-FE/Y6d-FE/Y9-FE/Y13-FE reaching server deploy pipeline |
| P1 | Write DT brief for ACAT v3 EC2 run (`acat-inkind-nna-testing.md` Step 2) | **DS** | DT EC2 run → DS analysis → production design brief |
| P1 | Execute ACAT v3 EC2 run once DS brief is written | **DT** | DS analysis → CEO design review |
| P2 | Issue Y14 task order to RD | **COO** | Books tab advisor access gating (auth chain ready; table needs populating) |
| P2 | Populate `opal-partner-49financial` with advisor email mappings | **Andrew** | Y14 actually usable by real advisors |
| P3 | CEO go/no-go on NNA canonical fix (commits `9bfb289b`+`b4f2d7a7`) | **CEO/Andrew** | DT gold layer rebuild + improved NNA accuracy |
| P4 | Issue Y17 mini-PRD when Books tab is stable | **COO** | AI RAG executive summary |

---

## Status: COMPLETE
**Active branch:** CLOUD
**Workspace CLOUD commit:** pending (this log)


### 0.4.0_DE_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DE_ClientPlatform

4da580a1 0.4.0_DE_ClientPlatform: ADVI_49FNV3 -- F3/F5/N1-N2 investigation complete, task orders closed
de994aec 0.4.0_DE_ClientPlatform: ModelPortfolios/Benchmark -- granular scatter selection + persistent tooltips (session log + submodule)
dd667949 0.4.0_DE_ClientPlatform: update portal submodule -- Y6b/Y6d drill fix (3702264)
7855dea3 0.4.0_DE_ClientPlatform: update portal submodule -- multi-granularity header_metrics (b0a33d7)
0ee72ab2 0.4.0_DE_ClientPlatform: update portal submodule -- Y6/Y6c NNA distribution fixes (b8cbf7a)
c1c50e3a 0.4.0_DE_ClientPlatform: task order completeness audit -- V1VERS + YANGV2 full sweep
518159a7 0.4.0_DE_ClientPlatform: COO handoff -- pod 4 state validation 2026-03-05
ad206388 0.4.0_DE_ClientPlatform: retroactive macro/project code cleanup -- pod 4 scope
3bbc980a org(1.0.0_SA_CTO): retroactive cleanup task orders + session log
f9161bed 0.4.0_DE_ClientPlatform: Phase 3 RD review complete + all 4 task orders marked complete
87cfe32c 0.4.0_DE_ClientPlatform: Phase 3 type wiring complete + COO briefing + session log update
d9686db0 org(2.0.0_SA_COO): ADVI-006 run + trade engine polish task orders
3252e5ce 0.4.0_DE_ClientPlatform: V2 types + RD task order refresh (gates cleared ADVI-004/005)
6048ce3c 0.4.0_DE_ClientPlatform: session log + ADVI-004 types task order complete
816f6fa2 0.4.0_DE_ClientPlatform: session log + I2 task order complete (leaderboard sort)
ff7f1ba3 0.4.0_DE_ClientPlatform: pod_inventory.xml -- leaderboard sort resolved
4a8e3d47 log(0.4.0_DE_ClientPlatform): pod_inventory.xml upgrade session log
5efb15f4 0.4.0_DE_ClientPlatform: upgrade pod_inventory.xml AdvisorIntelligence to full-fidelity from 0.4.2 RD audit
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order

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

#### ADVI-005_4C_stacked_bar_rolling_1y.md

# ADVI-005 4C — Stacked Bar Primary + Rolling 1Y Secondary — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `0bceb64`

## Objective

Implement Advisors tab rolling flows redesign (Stream 4C):
- Primary view: stacked bar chart (inflows up / outflows down) per advisor per period
- Secondary view: rolling 1Y line chart sliced by period toggle
- Legacy fallback preserved when stacked_bar or rolling_1y keys absent

Gate status was CLEARED (bd-v2.15.1). Types added by DE at portal DEV `5125eb9`.

---

## Work Completed

### Imports

- Recharts: added `BarChart as RechartsBarChart`, `Bar`, `ReferenceLine`
- Types: replaced `AdvisorRollingFlowsResponse` with `AdvisorRollingFlowsResponseV2`;
  added `AdvisorBarEntry`, `AdvisorRolling1YSeries`, `StackedBarPeriodKey`

### New types + constants

- `type FlowsViewMode = 'primary' | 'secondary'`
- `STACKED_BAR_PERIOD_OPTIONS` — qtd/ytd/1y/3y/max with labels QTD/YTD/1Y/3Y/Max
- `FLOWS_VIEW_OPTIONS` — Stacked / 1Y Rolling

### New state

- `flowsView: FlowsViewMode` — defaults to `'primary'`
- `stackedBarPeriod: StackedBarPeriodKey` — defaults to `'ytd'`
- `flowsData` type upgraded from `AdvisorRollingFlowsResponse | null` to `AdvisorRollingFlowsResponseV2 | null`

### Rolling Flows panel

Header now shows view toggle (Stacked / 1Y Rolling) + period toggle (QTD/YTD/1Y/3Y/Max).
Content conditionally renders:
- `StackedBarChart` when `flowsView === 'primary' && flowsData?.stacked_bar`
- `Rolling1YChart` when `flowsView === 'secondary' && flowsData?.rolling_1y`
- Legacy `RollingFlowsChart` as fallback when new keys absent

### StackedBarChart (new component)

| Property | Value |
|----------|-------|
| Chart type | Recharts BarChart |
| Data source | `data.stacked_bar[period][role]` (AdvisorBarEntry[]) |
| Sort order | nna_net ascending (lowest leftmost, highest rightmost) |
| Inflows bar | `stackId="flows"`, fill: hsl(var(--success)), opacity 0.75 |
| Outflows bar | `stackId="flows"`, fill: hsl(var(--destructive)), opacity 0.75, dataKey="outflowsNeg" |
| Outflows encoding | Positive in JSON; negated client-side: `outflowsNeg = -e.outflows` |
| Reference line | y=0 at rgba(255,255,255,0.2) |
| X-axis | advisor_name, angle -45, 12-char truncation |
| Tooltip | Custom content showing advisor_name + inflows/outflows/nna_net |

Waterfall style: inflows segment 0→inflows, outflows segment inflows→(inflows + outflowsNeg).
Net position of bar = nna_net.

### Rolling1YChart (new component)

| Property | Value |
|----------|-------|
| Chart type | Recharts LineChart (same pattern as legacy RollingFlowsChart) |
| Data source | `data.rolling_1y[role]` (AdvisorRolling1YSeries[]) |
| Period slicing | `period` toggle controls x-axis cutoff date (rolling window stays 1Y) |
| Selection | Same `selectedAdvisorIds` set as leaderboard row clicks |
| Metric plotted | nna (per contract: NNA-only primary; inflows/outflows in series for future) |
| Tooltip | advisor_name + formatted NNA per date |

Period → startDate mapping:
- qtd: start of current calendar quarter
- ytd: Jan 1 of current year
- 1y: 365 days ago
- 3y: 3 years ago
- max: no cutoff (full history)

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| stackId="flows" on both bars | Waterfall: inflows up from 0, outflows pull back from inflows top |
| flowsData typed as V2 (not V1) | Gate cleared; V2 extends V1 so backward compat holds |
| Legacy fallback path kept | Guard on stacked_bar/rolling_1y keys per 4C.5 requirement |
| Period toggle shared between primary and secondary | PRD: both views show period toggle; secondary uses it to slice x-axis |
| Default period: ytd | Most relevant business view; qtd too short, max too wide |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | 4C stacked bar + rolling 1Y | Yes — portal DEV `0bceb64` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Portal DEV is 7 commits ahead of origin: `3dc9dc5`, `7df26bb`, `5125eb9`, `ed832db`, `5f42dc6`, `bdcd00c`, `0bceb64`.
`bunx tsc -b` clean.

---

## Next Steps

1. **[DE] Review 4C visual design** before DT pushes portal DEV.
2. **[RD 0.4.2] Task 6 — advi_c3_cla_snapshot** — CLA snapshot view fix in DistributionTab.
3. **[RD 0.4.2] Task 7 — advi_c1_geo_continuous** — GEO continuous NNA view.
4. **[RD 0.4.2] Task 9 — ADVI-004 C2+C4** — ADV continuous + CLA continuous (gated).

#### AdvisorsTab_H_portal_primitives_I_top_performers.md

# AdvisorsTab H + I — Portal Primitives Refactor + Top Performers Redesign — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commits:** `5f42dc6` (H) -> `bdcd00c` (I)

## Objective

Task H: Replace ad-hoc `SubPanel`/`SubPanelHeader` in AdvisorsTab with portal primitives.
Task I: Redesign Top Performers panel for rank prominence and achievement feel.
H before I per dependency order — H provides canonical structure that I builds on.

---

## Work Completed

### 1. Task H — Portal Primitives Refactor (`5f42dc6`)

Removed inline `SubPanel` (lines 97-103) and `SubPanelHeader` (lines 105-112) component
definitions. Both were locally defined shadows of the portal primitive system.

Replaced all three section usages:

| Section | Old | New |
|---------|-----|-----|
| Top Performers | `SubPanel` + `SubPanelHeader` | `Panel variant="chart" className="overflow-hidden"` + `PanelHeader` + `PanelContent noPadding` |
| Rolling Flows | `SubPanel` + `SubPanelHeader` | Same pattern |
| Leaderboard | `SubPanel` + `SubPanelHeader` | Same pattern |

`PanelContent noPadding` preserves inner padding from the existing `<div className="p-4">`
wrappers — no content layout change. `overflow-hidden` added to Panel to preserve corner
clipping behavior that `SubPanel` had.

Note: `Panel variant="chart"` uses `bg-[hsl(var(--semantic-background-contentPanel))]`
rather than the old `bg-white/5`. Minor visual difference (flat vs slightly elevated). This
is the canonical portal treatment — content layout, chart sizes, and section positions
are identical.

### 2. Task I — Top Performers Visual Redesign (`bdcd00c`)

| Element | Before | After |
|---------|--------|-------|
| Rank badge | Absolute-positioned `-top-2 -left-2` w-7 h-7 corner circle | Top of card w-10 h-10 center-aligned badge |
| Rank text | `text-sm font-bold` | `text-lg font-black` |
| Advisor name | `text-sm font-semibold ml-4` | `text-base font-bold` — top element under badge |
| NNA metric | `text-xl font-bold` | `text-2xl font-black` — hero metric |
| Trophy icon | In PanelHeader only | PanelHeader + rank-1 card accent (`size={16}`) |
| Card layout | Relative-positioned corner badge + margin offset | Flex column: badge row -> name -> NNA -> secondary |
| Card radius | `rounded-lg` | `rounded-xl` |

`rankStyles` updated to separate `badgeBg`, `badgeBorder`, `badgeText` for the new badge
component. No new Lucide imports — `Trophy` already present.

Data flow unchanged: `top3` slice of `data.windows[window].entries`, responds to all period
toggles (3M/6M/1Y/2Y/3Y) via the existing `window` prop.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `overflow-hidden` on Panel | SubPanel had it; without it, rounded corners clip incorrectly on sticky table header |
| `PanelContent noPadding` for all three sections | Content manages its own padding; PanelContent's default `p-6` would break chart/table sizing |
| Trophy icon at card level for rank 1 only | Adds achievement signal without cluttering ranks 2 and 3 |
| `text-2xl font-black` for NNA | NNA is the primary achievement metric — needs to read immediately; font-black adds weight |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | H: panel primitives refactor | Yes — portal DEV `5f42dc6` |
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | I: Top Performers visual redesign | Yes — portal DEV `bdcd00c` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Portal DEV is 6 commits ahead of origin: `3dc9dc5`, `7df26bb`, `5125eb9`, `ed832db`,
`5f42dc6`, `bdcd00c`. AdvisorsTab structure is now canonical. `bunx tsc -b` clean.

---

## Next Steps

1. **[RD 0.4.2] Start 4C (ADVI-005-advisors_tab)** — Stacked bar + rolling 1Y on AdvisorsTab.
   Use `AdvisorRollingFlowsResponseV2`. H is done so no structural collision risk.
2. **[RD 0.4.2] DistributionTab: C3 -> C1 -> C2+C4** — after 4C.
3. **[DE] Review all committed work** — before DT pushes DEV.

**Files to touch next:**
- `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` — 4C stacked bar + rolling 1Y

#### DistributionTab_C1_geo_continuous.md

# DistributionTab C1 — GEO Continuous Search and Drill — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `4469ad7`

## Objective

Update the GEO continuous NNA view: limit chart to top-8 state series, add search input
covering all available states, keep existing click-to-drill into per-city data.

## Work Completed

### Top-8 display limit

Added `displayCategories` useMemo:
```tsx
const displayCategories = useMemo(() => {
  if (cohort === 'geo' && !isDrilled) return categories.slice(0, 8)
  return categories
}, [categories, cohort, isDrilled])
```
All chart rendering (gradients, Area components) and legend rendering switched from
`categories` to `displayCategories`. Metrics (`areaMetrics`, `startingTotal`) also use
`displayCategories` — consistent with what is shown in the chart.

For ADV cohort and for drilled city view: all categories rendered (no limit).

### Search input (GEO state level only)

Added `geoSearch: string` state. Search input renders in the left panel when
`cohort === 'geo' && !isDrilled` (before the legend).

- Input filters `categories` (full list, not just top-8) by display name
- Dropdown appears below input when `geoSearch` is non-empty
- Each result shows the state color dot, name, and right-arrow drill affordance
- Clicking a result: `setDrillParent(cat)` + clears search
- "No states found" empty state
- X button clears search

Search and geoSearch state both reset on cohort/metric change (via existing `useEffect`).

### Breadcrumb update

Replaced "Back to States" back button with breadcrumb path:
```
< All States / StateName
```
- Left-click on "All States" returns to state level
- StateName is read-only display

### No new API calls

Drill is purely local state — `setDrillParent(cat)` → `data?.geo_drill?.[cat]` (existing logic).
Search is also local state filtering `categories`. No new endpoints or queries.

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | C1 GEO continuous search + drill | Yes — portal DEV `4469ad7` |

## Blockers

None. tsc clean.

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`
Portal DEV: 9 commits ahead of origin.

## Next Steps

**[RD 0.4.2] Task 9 — ADVI-004 C2+C4** — ADV continuous + CLA continuous.
Gate CLEARED at bd-v2.15.0. Types at portal DEV `7df26bb`.

#### DistributionTab_C2_C4_adv_drill_cla_continuous.md

# DistributionTab C2+C4 — ADV Drill + CLA Continuous — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `c562257`

## Objective

C2: ADV continuous NNA with architect->client drill (adv_drill now live at bd-v2.15.0).
C4: CLA continuous stacked area with full drill hierarchy (total/geo_drill/geo_city_drill/adv_drill).

---

## Work Completed

### C2 — ADV Continuous Drill

The drill logic for ADV already existed in `ContinuousChartView`:
```tsx
const drillViewData = isDrilled
  ? (cohort === 'geo' ? data?.geo_drill?.[drillParent!] : data?.adv_drill?.[drillParent!])
  : undefined
const showAdvComingSoon = isDrilled && cohort === 'adv' && !drillViewData
```
With `adv_drill` now live (bd-v2.15.0), this path returns real data. The "coming soon" message
only shows when drillViewData is undefined — no longer triggered.

**Fix added:** `canLegendDrill` now guards against second-level drill in ADV:
```tsx
// Before:
const canLegendDrill = (cohort === 'adv') || (cohort === 'geo' && !!data?.geo_drill)
// After:
const canLegendDrill = (cohort === 'adv' && !isDrilled) || (cohort === 'geo' && !!data?.geo_drill)
```
Client-level entries (drilled ADV) no longer show drill arrow buttons — ADV is terminal at client grain.

**Breadcrumb** was already updated in C1 to show `All Architects / ArchitectName` for ADV.

### C4 — CLA Continuous (new ClaContinuousView component)

Added new `ClaContinuousView` component (~200 lines) replacing the "Coming soon" placeholder.

**Data source:** `data.cla` (CumulativeChartResponse.cla — guarded if absent)

**Drill levels (GEO cohort):**
| Level | Data source | Drill to |
|-------|------------|---------|
| Total | `cla.total` | States from `cla.geo_drill` keys |
| State | `cla.geo_drill[stateKey]` | Cities from `cla.geo_city_drill[stateKey]` keys (guarded) |
| City | `cla.geo_city_drill[stateKey][cityKey]` | Terminal |

**Drill levels (ADV cohort):**
| Level | Data source | Drill to |
|-------|------------|---------|
| Total | `cla.total` | Architects from `cla.adv_drill` keys |
| Architect | `cla.adv_drill[advKey]` | Terminal |

**Chart:** Recharts AreaChart with `stackId="cla"` — same pattern as main continuous view.
Colors: `CATEGORY_COLORS.NMNC` (#16A34A green) and `CATEGORY_COLORS.NMEC` (#2563EB blue).
Fallback: `FALLBACK_COLORS` for any unexpected categories.

**Left panel layout:**
- Breadcrumb with back buttons at each level
- Hero metric: total AUA of current view
- NMNC/NMEC legend (current series)
- Contextual drill list (states/cities/architects) with right-arrow affordance, max-h-[160px] scroll

**Breadcrumb:** `< All States / StateName / CityName` (geo) or `< All Architects / ArchitectName` (adv).
Clicking intermediate breadcrumb level clears child drill (e.g., clicking StateName clears cityKey).

**Window toggle:** Updated to show for CLA mode too (removed `metric !== 'cla'` exclusion).
`CumulativeChartView` added to types import.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | C2 ADV drill + C4 CLA continuous | Yes — portal DEV `c562257` |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`
Portal DEV: 10 commits ahead of origin: `3dc9dc5`, `7df26bb`, `5125eb9`, `ed832db`,
`5f42dc6`, `bdcd00c`, `0bceb64`, `174958a`, `4469ad7`, `c562257`.

All 9 tasks complete. Portal DEV ready for DE review before DT push.

---

## All Tasks Summary

| # | Task | Commit | Status |
|---|------|--------|--------|
| 1 | distribution_nomenclature_fix | pre-applied | complete |
| 2 | continuous_view_max_window_clients_fix | ed832db | complete |
| 3 | xtick_spacing_fix | pre-applied | complete |
| 4 | advi_h_portal_primitives | 5f42dc6 | complete |
| 5 | advi_i_top_performers | bdcd00c | complete |
| 6 | advi_c3_cla_snapshot (addendum) | 174958a | complete |
| 7 | advi_c1_geo_continuous | 4469ad7 | complete |
| 8 | ADVI-005 4C stacked bar + rolling 1Y | 0bceb64 | complete |
| 9 | ADVI-004 C2+C4 ADV drill + CLA continuous | c562257 | complete |

#### DistributionTab_C3_cla_snapshot.md

# DistributionTab C3 — CLA Snapshot Redesign — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `174958a`

## Objective

Replace the CLA snapshot diverging bar chart (inflows/outflows/NNA) with a composition view
showing NMNC vs NMEC book breakdown. Data source corrected to `getHeaderMetrics()` per addendum
`advi_c3_cla_snapshot_addendum.md` (1.0.0_SA_CTO-2026-03-04).

---

## Work Completed

### Data source change

Removed all `analyticsData.views.cla` reads from `ClaSnapshotView`. Added `useQuery` inside
the component:
```tsx
const { data: headerData, isLoading: headerLoading } = useQuery<HeaderMetricsResponse>({
  queryKey: ['headerMetrics'],
  queryFn: getHeaderMetrics,
  staleTime: 5 * 60 * 1000,
})
```
No prop threading. No dependency on `PartnerAnalyticsResponse`.

### Props interface update

| Removed | Kept |
|---------|------|
| `analyticsData: PartnerAnalyticsResponse` | `cohort: CohortOption` (kept for future use) |
| `selectedPeriod: TimePeriodKey` | |
| `onPeriodChange: (period: TimePeriodKey) => void` | |

Call site updated: `<ClaSnapshotView cohort={cohort} />`. Parent `selectedPeriod`/`setSelectedPeriod`
state preserved for other views (DistributionQuarterlyStrip, NnaQuarterlyStrip).

### Layout

Two-column flex split (same pattern as the rest of DistributionTab):

**Left partition:** Donut + legend + quarter strip
- Recharts `PieChart` with inner radius 60, outer 92 — two segments NMNC (green `#16A34A`) / NMEC (blue `#2563EB`)
- Absolute-positioned center label: `nmnc_pct%` + "New Clients" subtitle
- Legend: per-segment label, %, relationship count, AUA dollar amount
- Quarter strip: read-only mini stacked bars showing NMNC/NMEC mix per Q0-Q3
  - Finds last timeseries data point where `date <= dates.qN`
  - Falls back to `total.new_client_pct` for q0 if timeseries absent

**Right partition:** Account size distribution histogram + stats
- Recharts `BarChart` — two grouped bars per bin (NMNC green, NMEC blue)
- Bin labels: `nmnc_dist.histogram.bin_labels`
- Per-segment stats card: median, mean, count
- Legend row

### Removed

- `CLA_COLORS` constant (flows vocabulary — removed entirely)
- `ClaBarDatum` interface
- All NNA/inflows/outflows rendering
- Debug `console.log` statement
- `ClaView` type import (no longer used)

### New imports

- Recharts: `PieChart, Pie` (added to existing imports)
- API: `getHeaderMetrics` (added alongside `getCumulativeChart`)
- Types: `HeaderMetricsResponse, SegmentDistribution, RollingTimeseriesDataPoint`

### TypeScript fix

Recharts `Tooltip` `formatter` prop requires `value: number | undefined, name: string | undefined`
to match the `Formatter<number, string>` type signature. Fixed the formatter lambda accordingly.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `useQuery` inside component, not prop threading | Addendum constraint: no headerData prop on DistributionTab |
| `_cohort` parameter name | cohort prop kept for future geo/adv split; unused now to avoid lint |
| Quarter strip reversed order | Show oldest→newest left-to-right (Q3→Q0) for natural time flow |
| Grouped bars (not overlapping) | Clearest comparison for NMNC vs NMEC account sizes |
| Stats card instead of reference lines | Median/mean are dollar values, not bin labels; text readout is cleaner |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | C3 CLA snapshot redesign | Yes — portal DEV `174958a` |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Portal DEV is 8 commits ahead of origin.

---

## Next Steps

1. **[DE] Review C3 visual design** — confirm queryKey `['headerMetrics']` matches any existing
   key used by other components calling `getHeaderMetrics()`.
2. **[RD 0.4.2] Task 7 — advi_c1_geo_continuous** — GEO continuous NNA view.
3. **[RD 0.4.2] Task 9 — ADVI-004 C2+C4** — ADV continuous + CLA continuous.

#### DistributionTab_nomenclature_and_max_window_fix.md

# DistributionTab Nomenclature + Max Window Fix — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `ed832db`

## Objective

Execute task orders `distribution_nomenclature_fix` and `continuous_view_max_window_clients_fix`
on DistributionTab.tsx, plus confirm xtick_spacing_fix (addendum) is already applied.

---

## Work Completed

### 1. Audit of Pre-Applied Changes

Before writing any code, audited DistributionTab.tsx against all three task orders.

**distribution_nomenclature_fix (11 changes):** 10 of 11 already applied in a prior session.
- `SnapshotDistributionChartProps.isNnaMode?: boolean` — present
- `SnapshotDistributionChart` function signature destructures `isNnaMode = false` — present
- Y-axis NNA label: `'Relationships (log)'` instead of `'Number of Relationships'`. Deviation
  is intentional — `(log)` suffix accurately reflects the log scale used in NNA mode. Left as-is.
- X-axis label: `{isNnaMode ? 'Period NNA' : 'Account Size'}` — present
- Tooltip row 1: `{isNnaMode ? 'NNA Range' : 'Account Size'}` — present
- Tooltip row 2: `{isNnaMode ? 'Relationship Count' : 'Account Count'}` — present
- `SnapshotDistributionMetrics` signature has `isNnaMode?: boolean` — present
- Primary tile: `{isNnaMode ? 'Total Relationships' : 'Total Accounts'}` — present
- Both `<SnapshotDistributionChart>` and `<SnapshotDistributionMetrics>` call sites pass `isNnaMode={isNnaMode}` — present
- AUA footnote muted span: `' Distribution reflects funded accounts only, log-spaced bins.'` — present

**xtick_spacing_fix (addendum — 3 changes):** Fully applied.
- Both containers at `h-[450px]` (donut ~line 1271, bell curve ~line 1449) — present
- `AreaChart margin={{ ..., bottom: 50 }}` — present
- `XAxis` uses custom SVG tick renderer with `height={50}`, `dy={12}`, `transform="rotate(-45)"` — present
- Y-axis label div: `justify-center`, `pointer-events-none`, `width: '16px'` — present
- X-axis label div: `bottom: '6px'`, `left: 'calc(50% + 15px)'` — present

### 2. continuous_view_max_window_clients_fix — Implemented (4 changes)

**The issue:** `ContinuousChartView` always shows "New Clients" tile. At Max window,
`data.metadata.new_clients['Max']` is never populated by the backend — always shows '--'.
"New Clients" is also semantically wrong over all time (every client is cumulative total).

**Type investigation:** The task order specified `cohortView?.current?.metrics?.client_count ?? cohortView?.metrics?.client_count`.
This fails tsc: `PartnerAnalyticsView.metrics` is `ViewMetrics` (no `client_count`); only
`PartnerAnalyticsViewWithPeriods.current.metrics` is `PeriodMetrics` (has `client_count`).
Used `hasTimeMachine()` guard (already imported) to satisfy TypeScript.

| Change | Location | What |
|--------|----------|------|
| Interface | `ContinuousChartViewProps` | Added `totalClients?: number` |
| Signature | `ContinuousChartView` | Destructures `totalClients` |
| Call site | `<ContinuousChartView>` in `DistributionTab` | IIFE with `hasTimeMachine` guard derives `view.current.metrics.client_count` |
| Tile | ~line 807 | `window === 'Max'` ternary: label/value switch |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `hasTimeMachine` guard instead of task order's `??` fallback | `ViewMetrics` has no `client_count` — task order's double-access pattern fails tsc. Guard is correct and already used elsewhere in the file. |
| IIFE at call site | `hasTimeMachine` needs a variable to guard; IIFE keeps it inline without polluting JSX scope above. |
| Leave Y-axis `'Relationships (log)'` as-is | More informative than `'Number of Relationships'`; log scale is factual for NNA mode. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | `totalClients` prop wiring + Max window tile fix | Yes — portal DEV `ed832db` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Tasks 1 (nomenclature — pre-applied), 2 (max window — implemented), and 3 (xtick — pre-applied)
are all done. `bunx tsc -b` clean. Portal DEV is now 4 commits ahead of origin: `3dc9dc5`,
`7df26bb`, `5125eb9`, `ed832db`. DE reviews before DT pushes.

---

## Next Steps

1. **[RD 0.4.2] Start H (advi_h_portal_primitives)** — AdvisorsTab panel primitives refactor.
   Must precede I (Top Performers redesign) and 4C (stacked bar).
2. **[RD 0.4.2] Then I (advi_i_top_performers)** — Top Performers visual redesign.
3. **[RD 0.4.2] Then 4C (ADVI-005)** — Stacked bar + rolling 1Y in AdvisorsTab.
4. **[RD 0.4.2] DistributionTab: C3, C1, C2+C4** — in that order.

**Files to touch next:**
- `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` — H then I then 4C

**Do NOT:**
- Push portal DEV — DT is the push gate after DE reviews
- Start 4C before completing H (structural refactor prevents collision)

#### Y1_Y4_Y6_Y12_phase1_visual.md

# Y1+Y4+Y6+Y12 Phase 1 Visual Fixes -- 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commits:** `f9c0e59` -> `76c7621` -> `7258c5e` -> `2981133`

## Objective

Execute four Phase 1 visual-only changes from Yang V2 PRD. All use existing data, no DS/DT dependency.

---

## Work Completed

### Y1 -- AUA Stack Order Flip (PartnerAnalytics.tsx)

Reversed `barCategories` array in the `Bar` map so NMNC (new clients, green) renders above
NMEC (existing clients, blue). Recharts renders first-declared Bar at bottom of stack.
`[...barCategories].reverse()` ensures NMEC is bottom, NMNC is top regardless of data order.

### Y4 -- NNA Diverging Bar Alignment + Net Line (PartnerAnalytics.tsx)

This required three iterations to get right. The task order's instructions were incorrect
about Recharts stacking mechanics. Documenting the full iteration for future reference.

**Attempt 1 (`f9c0e59`):** Added `stackId="nna"` to both Bar components + `netMidpoint`
field with formula `(inflow + outflow) / 2` for the Line dataKey.

Two problems:
- `stackId` without `stackOffset="sign"` causes Recharts to stack additively: outflow bar
  renders ON TOP of inflow bar (starting from inflow's top, going downward), not
  independently from zero. Visually broken.
- `netMidpoint` formula was wrong. NNA line should show actual net value (e.g., +10M
  inflows - 20M outflows = -10M NNA), not the geometric center of the bar span.

**Attempt 2 (`76c7621`):** Fixed net line -- reverted Line dataKey back to `"net"` (actual
NNA value), removed `netMidpoint` computed field. Net line now correctly shows actual NNA.

**Attempt 3 (`7258c5e`):** Removed `stackId="nna"` entirely to fix the stacking problem.
Bars now extend independently from zero (inflow up, outflow down). But without stackId,
Recharts places the two bars side-by-side (two thin columns per period) -- visually messy.

**Final fix (`2981133`):** The correct Recharts pattern for diverging bars at the same
x-position:
1. Add `stackOffset="sign"` to the `<ComposedChart>` component
2. Add `stackId="nna"` to both `<Bar>` components

`stackOffset="sign"` is the key -- it tells Recharts to route positive values above zero
and negative values below zero when stacking. Combined with `stackId`, both bars share one
column per period while each extends from the zero line in the correct direction.

**Recharts diverging bar reference (for future agents):**
- `stackId` alone = additive stacking (bar 2 starts where bar 1 ends). WRONG for diverging.
- No `stackId` = side-by-side bars. Correct direction but misaligned x-position.
- `stackId` + `stackOffset="sign"` = diverging bars at same x-position. CORRECT.

### Y6 -- Snapshot NNA Bucket Filter + Footnote (DistributionTab.tsx)

**Y6.1:** Added `filteredIndices` array in `SnapshotDistributionChart`. In NNA mode, filters
out any histogram bin where both `bins[i]` (lo) and `bins[i+1]` (hi) fall within [-1000, 1000].
Non-NNA mode passes all bins through.

**Y6.2:** Added footnote below NNA histogram: "Relationships with net flows between -$1,000
and $1,000 are excluded from this distribution." Wrapped in JSX fragment with existing footnote.

### Y12 -- Drop 1Y Rolling from Advisors Tab (AdvisorsTab.tsx)

Removed:
- `FlowsViewMode` type
- `FLOWS_VIEW_OPTIONS` constant
- `flowsView` / `setFlowsView` state
- View toggle from Rolling Flows PanelHeader
- `Rolling1YChart` component (~120 lines)
- `RollingFlowsChart` legacy component (~110 lines)
- `activeFlowsSeries` useMemo
- `FlowsMetric` type, `FLOWS_METRIC_OPTIONS`, `FLOWS_WINDOW_OPTIONS` constants
- `flowsMetric`, `flowsWindow` state
- Unused imports: `LineChart`, `Line`, `useMemo`, `Users`, `AdvisorRolling1YSeries`,
  `RollingFlowsWindowKey`, `RollingFlowsDataPoint`, `AdvisorRollingSeries`, `LINE_COLORS`

Kept: StackedBarChart, period toggle (QTD/YTD/1Y/Max), role toggle.

**DS coordination note:** rolling_1y key removal from script 10 is DS's call -- confirm no
other consumer before DS drops it. Y12 removes the UI only.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `[...barCategories].reverse()` for Y1 | Declarative reversal; works regardless of data order |
| `stackOffset="sign"` + `stackId="nna"` for Y4 | Only correct Recharts pattern for diverging bars at same x-position. See iteration notes above. |
| Net line uses `dataKey="net"` (actual NNA) | Task order's midpoint formula was wrong; NNA line must show true net value |
| `filteredIndices` array for Y6 | Filters by numeric bin boundaries, not label strings |
| Bulk removal for Y12 | 332 lines deleted, 39 added. Clean separation of concerns. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | Y1 stack flip + Y4 diverging bar (4 commits) | Yes -- portal DEV `f9c0e59` `76c7621` `7258c5e` `2981133` |
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | Y12 1Y rolling removal | Yes -- portal DEV `f9c0e59` |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Y6 bucket filter + footnote | Yes -- portal DEV `f9c0e59` |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

All four Y-streams implemented across 4 commits. Portal DEV head at `2981133`.
Andrew confirmed Y4 NNA diverging bar visual is correct.

---

## Next Steps

1. **[DE] Review commits** before DT pushes portal DEV.
2. **[RD 0.4.2] Next task orders** -- ADVI-Y8 (continuous AUA stacked bar) pending.

#### Y8_continuous_aua_stacked_bar.md

# Y8 Continuous AUA Stacked Bar -- 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commits:** pending (uncommitted on portal DEV)

## Objective

Convert the AUA continuous view from AreaChart (stacked area) to BarChart (stacked bar)
and add a Month/Quarter/Year interval toggle. Task order: ADVI-Y8-continuous-aua-stacked-bar.

---

## Work Completed

### Y8 -- Continuous AUA: Area to Stacked Bar + Interval Toggle (DistributionTab.tsx)

**State (line 690):** Added `auaInterval` state (`'monthly' | 'quarterly' | 'annually'`,
default `'monthly'`) to `ContinuousChartView`. Per-view state -- does not leak to other
metrics or views.

**Aggregation memo (lines 757-791):** Added `aggregatedBarData` useMemo that buckets
daily `filteredChartData` into period snapshots:
- `getPeriodKey()` maps each date to a month, quarter, or year key + display label
- Uses last-data-point-per-period strategy (end-of-period snapshot for cumulative AUA data)
- Sorted by period key for chronological ordering
- Only runs when `metric === 'aua'` (NNA and CLA early-return before this code path)

**Chart replacement (lines 956-1066):** Replaced `AreaChart`/`Area` with `BarChart`/`Bar`:
- Stacked bars with `stackId="aua"`, 0.85 fill opacity
- Reversed `displayCategories` for render order (NMNC on top, consistent with Y1)
- Rounded top corners (`radius={[4,4,0,0]}`) on topmost bar segment
- `vertical={false}` on CartesianGrid for cleaner bar chart appearance
- Cursor changed from line stroke to subtle fill highlight

**Interval toggle (lines 958-973):** Pill toggle (Month / Quarter / Year) positioned
top-right of the chart area. Uses same styling pattern as other toggles in the codebase
(bg-white/10 container, bg-white/20 active state).

**Tooltip:** Simplified -- shows period label (e.g., "Mar '26", "Q1 '26", "2026")
instead of raw date. "Cumulative AUA" header. Categories sorted by value descending.

### What was NOT changed

- NNA and CLA views are unaffected (early returns before the bar chart code path)
- `Area` import remains in the file -- may be used by other chart paths; did not audit
- No color changes, no data source changes
- No new dependencies

---

## Technical Notes

**Why last-data-point-per-period (not average or sum)?**
AUA is cumulative (total assets under advisement at a point in time). Summing or averaging
daily AUA values within a month has no financial meaning. The correct bar value is the
end-of-period snapshot -- the last available data point before the period boundary.

**Why `metric !== 'aua'` guard returns empty array?**
At the chart render level, only AUA reaches the BarChart path. But the memo runs on every
render regardless of which early-return fires. The guard prevents unnecessary computation
and ensures `aggregatedBarData` is always a valid empty array for non-AUA metrics.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Y8 area-to-bar + interval toggle | Pending |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| End-of-period snapshot (last point per period) | Cumulative AUA is a point-in-time metric; sum/average is meaningless |
| Reversed displayCategories for bar order | Consistent with Y1 -- NMNC (new) on top of NMEC (existing) |
| Per-view `auaInterval` state | Interval preference is specific to AUA continuous view; no reason to share globally |
| Pill toggle top-right | Matches existing toggle patterns; does not crowd the category list on the left |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** CODE COMPLETE -- awaiting commit
**Active branch:** portal `DEV`
**tsc:** Clean (no type errors)

The DistributionTab.tsx diff also contains unrelated PortfolioManagement changes from another
agent's work. Y8 changes are isolated to the `ContinuousChartView` component within
DistributionTab.tsx.

---

## Next Steps

1. **Commit Y8** to portal DEV (isolated commit for DistributionTab.tsx Y8 changes only).
2. **Visual QA** -- Andrew/Yang confirm stacked bar appearance and interval toggle behavior.
3. **Check if `Area` import can be cleaned up** -- audit whether any other chart path in DistributionTab.tsx still uses Area.


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

513adfdf org(0.4.2_RD_AdvisorIntelligence): Y8 session log + phase 1 task order status update
ce2cb497 0.4.2_RD_AdvisorIntelligence: mark 9 task orders complete + session logs + portal submodule advance
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b5ace0c0 org: quality audit -- fix bugs, upgrade thin profiles, seed missing deliverables
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
42f99352 logs: 0.4.2_RD_AdvisorIntelligence distribution nomenclature fix session log
2f8de475 docs(org): add xtick fix addendum for 0.4.2_RD_AdvisorIntelligence
4e046836 logs: 0.4.2_RD_AdvisorIntelligence xtick spacing fix session log

