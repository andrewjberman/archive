# Thread Context -- Pattern 0 alignment: Books tab L2/L3/L4 design brief

**Thread ID:** 2026-03-03-books-tab-design
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-03T19:47:40Z

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


---

## Reference Material

### Briefing Notes

This is a Pattern 0 pre-implementation alignment thread for the Books tab (Stream D) of the AdvisorIntelligence completion PRD.

The Books tab has four levels:
  L2: Advisor book (all of this advisor's relationships — default landing for non-admin users)
  L3: Relationship/client view (one client's full detail)
  L4: Account + holdings + lots + performance + tax (deepest view, with lot-level drill-down)

Knowledge source: 0.4.0_DS_ClientPlatform — describes WHAT data currently flows out of the advisor-publisher Lambda and what L4 data exists in the gold layer (scripts 03, 05b, 06) but is NOT yet published. DS must surface the gap between what is available in gold vs what is currently in the S3 publisher output.

Layout proposer: 0.4.2_RD_AdvisorIntelligence — proposes the visual layout for each level (L2/L3/L4), identifies component reuse opportunities, flags any layout constraint that affects what fields DS needs to add to the publisher.

Wiring specifier: 0.4.0_DE_ClientPlatform — reviews DS's gap list and RD's layout, identifies TypeScript interface additions needed, confirms component reuse opportunities, and flags any API endpoint changes required.

Deliverable: a markdown design brief at docs/architecture/advisor_intelligence/books_tab_design_brief.md covering:
  1. L2 advisor book layout (sections with data field mappings)
  2. L3 relationship view layout
  3. L4 account + holdings view with tax summary and lot drill-down
  4. Component reuse opportunities
  5. Publisher data gaps DS must close before RD implements
The final agent turn (DE) must write the design brief path and a structured summary of what changed in the agreed contract.


### advisorintelligence-completion-prd--section-5-books-tab.md

```
# Advisor Intelligence — Completion PRD

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-03
**Status:** ACTIVE — issued to 2.0.0_SA_COO for task order decomposition
**Source:** CEO-CTO interview, 2026-03-03

---

## 1. Context & Scope

Advisor Intelligence is the primary client-facing analytics dashboard for 49 Financial
advisors and firm administrators. The page is at bd-v2.14.0, approximately 85-90%
complete. This PRD covers the remaining work to reach a shippable v1.0 state.

**Pods affected:** Pod 4 (ClientPlatform) exclusively. DE = 0.4.0, DS = 0.4.0,
DT = 0.4.0, RD = 0.4.2_RD_AdvisorIntelligence. Shared infra: 0.6.0_AE_PartnerETL
(BD pipeline), 0.7.0_AE_CloudOps (auth infrastructure).

**Reference files:**
- Portal page: `portal/src/pages/AdvisorIntelligence/`
- API endpoints: `portal/src/api/endpoints/advisor-intelligence.ts`
- Types: `portal/src/pages/AdvisorIntelligence/types.ts`
- Gold scripts: `data/black_diamond/scripts/gold/`
- Lambda publisher: `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`
- Advisor publisher: `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`

---

## 2. Work Streams and Dependency Order

**Dependency rule:** DS data contract work ALWAYS precedes DE/RD portal work.
DT deploys ONLY after DS commits and `data_contract.xml` is updated.

```
Stream A (DS): CLA timeseries + adv_drill + stacked bar period data
  -> Stream B (DT): Deploy publisher Lambda updates
    -> Stream C (DE + RD): Distribution tab continuous views + Advisors tab redesign

Stream D (COO thread): Books tab design brief (DS + RD + DE)
  -> Stream E (DS): Books data contracts (account, holdings, tax)
    -> Stream F (DT): Deploy advisor-publisher updates
      -> Stream G (DE + RD): Books tab implementation

Stream H (parallel, no dependency): Distribution tab snapshot fixes (RD)
Stream I (parallel, no dependency): Advisors tab portal primitives + sort fix (RD)
Stream J (parallel, starts after thread): Auth gating (DS + AE CloudOps)
```

---

## 3. Distribution Tab

### 3A. Continuous NNA — GEO View

**Current state:** The GEO continuous view renders a single aggregated NNA chart.
The data already exists in `timeseries_chart.json` (`geo` view with per-state
categories, and `geo_drill` with per-city categories under each state).

**Required behavior:**
- By default, render the top-8 states as separate series in the cumulative NNA chart,
  using the same visual format as the Assets Overview header panel's cumulative NNA chart
  (same chart type, axis format, color scheme, date range, window toggle).
- Add a **search input** in the left panel controls that filters across all available
  states, including those outside the top-8.
- Clicking a state from the chart legend or search results drills into that state:
  the chart re-renders showing per-city series for cities within that state
  (sourced from `geo_drill[stateKey]` in `timeseries_chart.json`).
- A back/breadcrumb control returns to the state-level view.

**Data status:** READY. `geo_drill` is deployed in `timeseries_chart.json` as of
bd-v2.14.0 (8 states, up to 10 cities each, ~2,000 data points per city).

**Agents:** DE + 0.4.2_RD | No DS work required for this item.

---

### 3B. Continuous NNA — ADV View

**Required behavior:** Same as 3A but for architects instead of states.
- Top architects as separate series, same chart format as Assets Overview NNA.
- Search input for architects not in top list.
- Click architect → drill to client/relationship level, showing that architect's
  clients as series in the same chart format.
- No drill-down past relationship level (client is the terminal grain for ADV).

**Data gap:** `adv_drill` does NOT yet exist in `timeseries_chart.json`. This is
the per-architect → per-client NNA time series, analogous to `geo_drill`.

**DS task:** Update `bd-portal-publisher/lambda_function.py` to generate `adv_drill`:
```
adv_drill: Record<architect_key, CumulativeChartView>
```
Where each `CumulativeChartView` has categories = the architect's top clients, and
data = cumulative NNA time series per client. Pattern follows `geo_drill` exactly.
Update `data_contract.xml` before handing to DT.

**DT task:** Deploy publisher Lambda update. No Terraform changes expected (Lambda code only).

**Agents:** DS first → DT deploy → DE + 0.4.2_RD

---

### 3C. Snapshot NNA — Bell Curve Math Fix

**Issue:** Negative NNA accounts (net outflows) use `|abs|` for the bell curve
percentile threshold calculation. The update to script 09 in commit `8247c6d0`
(2026-03-02) should have addressed this. Needs verification.

**DS task:** Verify that the negative abs calculation in script 09's bell curve
generation produces correct percentile thresholds for outflow accounts. Specifically,
confirm that the P10/P25/Median/P75/P90 thresholds for the outflow distribution
are computed on the absolute values of negative NNA (not signed values). If the
fix did not land in `8247c6d0`, a targeted patch to script 09 is required.

**Verification:** Inspect current `partner_analytics/header_metrics.json` in S3 and
confirm the `distribution` field for the NNA view's negative segments has non-degenerate
percentile thresholds (not all zeros or symmetric with the positive side).

**Agents:** DS to verify → if patch needed, DS patches + DT deploys EC2 script.

---

### 3D. Snapshot CLA — Simplified Visualization

**Current state:** The CLA snapshot view is incorrectly rendering as a flows chart
(NNA-style), which is not the intent.

**Required behavior:** CLA is not about flows. It is about what percentage of
total AUM is attributable to new clients (NMNC) versus existing clients (NMEC).

Snapshot CLA visualization:
- Two colors only: **green = NMNC** (New Client AUA), **blue = NMEC** (Existing Client AUA)
- Show NMNC% and NMEC% of total AUA as a simple proportional display
- Preferred format: horizontal stacked bar or a split donut — clean, no axes, just
  the two proportions with AUA amounts labeled
- Available for current period and time machine (q1/q2/q3 periods) to show how the
  new-client percentage has shifted over time
- No inflow/outflow data. No NNA. No blue/red flows vocabulary. Just two-color NMNC/NMEC split.

**Data status:** `header_metrics.json` already has `views.aua` and CLA data.
The DS needs to confirm that `cla.current.geo.totals.nmnc_nna` and `nmnc_count`
in the CLA structure are populated correctly for this use case. The portal
`ClaView` type already supports this: `{ segments[], totals: { nna, nmnc_nna, nmec_nna, nmnc_count, nmec_count } }`.

**Agents:** 0.4.2_RD (visualization change) + DS to confirm data is populated.

---

### 3E. Continuous CLA — New Time Series View

**Current state:** Does not exist. Not in `timeseries_chart.json`.

**Required behavior:** A time-series chart (same format as Assets Overview cumulative
NNA chart) showing the composition of total AUM between NMNC (new clients, green)
and NMEC (existing clients, blue) over time. This is a stacked area chart where:
- Y-axis = dollar AUM (absolute, not percentage)
- Two areas stacked: NMNC AUM (green) and NMEC AUM (blue)
- Total height = total firm AUM at each date
- Viewable at: total (firm-wide), state grain (e.g., Texas → shows NMNC/NMEC AUM
  composition for Texas clients), city grain (drill-down from state), architect grain
  (no client drill-down needed for CLA — architect is the terminal grain for ADV-CLA)

Search function: same as 3A/3B — search for states or architects not in the top list.

**Data gap:** This time series does NOT exist anywhere in the current pipeline.
The closest data is `client_performance.parquet` which has daily AUA per relationship.
The DS can join `accounts_dimension_latest` to classify each relationship as NMNC or
NMEC (using the advisor assignment history and account open dates), then aggregate
daily NMNC vs NMEC AUM by state/city/architect.

**DS task:** Design and implement `cla_timeseries` output — either in script 09
(extending the EC2 gold layer) or in the publisher Lambda. The output structure:
```
timeseries_chart.json additions:
  cla: {
    total: CumulativeChartView          // categories: ['nmnc', 'nmec']
    geo: CumulativeChartView            // categories: top states
    adv: CumulativeChartView            // categories: top architects
    geo_drill: Record<state, CumulativeChartView>  // cities within state
    // no adv_drill for CLA
  }
```
Where `CumulativeChartView.data` has `nmnc` and `nmec` AUM values per date point.

Confirm NMNC/NMEC classification logic with DE before committing to data contract.
Update `data_contract.xml` before handing to DT.

**Agents:** DS (design + implement) → DT (deploy) → DE + 0.4.2_RD (render)
**Note:** This is the highest DS effort item in this PRD. Schedule accordingly.

---

## 4. Advisors Tab

### 4A. Portal Primitives Refactor

**Issue:** Advisors tab uses ad-hoc layout containers instead of the portal's
standard `Panel`, `PanelHeader`, `PanelContent`, `SmartPanelFooter` from
`@/ui/components/panels`. This breaks visual consistency with the rest of the portal.

**Required behavior:** All sections in the Advisors tab (Top Performers panel,
Rolling Flows panel, Leaderboard panel) must use portal panel primitives.

**Agents:** 0.4.2_RD | No data changes required.

---

### 4B. Top Performers — Stronger Visual Identity

**Issue:** The current Top 3 highlights panel is visually weak — does not
communicate rank and achievement clearly.

**Required behavior:** Top Performers should feel like a podium or headline card
with clear rank (1st/2nd/3rd), the advisor name prominent, and the key metric
(NNA for the active period) immediately readable. Consider trophy/medal iconography
or rank-badge treatment consistent with Lucide icons available in the codebase.

**Agents:** 0.4.2_RD | DE reviews before pushing.

---

### 4C. Rolling Flows — New Visualization Model

**Current state:** Advisors tab shows rolling flows with 30d/90d/1Y window toggles
as line charts. This is low-signal and not anchored to business periods.

**New model — two views, one toggle set:**

**Primary view: Stacked Bar Chart (default)**
- X-axis: architects or implementors (one bar per person)
- Bars stacked: Inflows (positive, e.g. teal), Outflows (negative, inverted downward
  or shown as a negative bar segment), NNA net (implied by the two)
- Sorted lowest to highest by NNA so the highest performers are visually rightmost
- Period toggle: QTD / YTD / 1Y / 3Y / Max
- Architects/Implementors toggle at top (controls both views)

**Secondary view: 1-Year Rolling Line Chart**
- X-axis: date (over the selected period window)
- Y-axis: 1-year rolling NNA value for each advisor
- One line per advisor (top performers by default, all accessible via search/toggle)
- Period toggle controls the x-axis window (how far back dates go), NOT the rolling window
- Rolling window is FIXED at 1 year (full year trailing from each date point)
- Same Architects/Implementors toggle

**Data gap:** Script 10 currently produces trailing rolling NNA at 30d/90d/1Y windows.
This needs:
1. Period-anchored aggregated NNA with inflows/outflows per advisor for stacked bar:
   - QTD = sum from start of current quarter to today
   - YTD = sum from Jan 1 to today
   - 1Y = sum from 1 year ago to today
   - 3Y = sum from 3 years ago to today
   - Max = inception to today
   - For each period: inflows, outflows, nna_net per architect and per implementor
2. 1-year rolling NNA per advisor (daily points) for the line chart — this already
   conceptually exists in script 10 but may need the window fixed at 1Y and date
   range extended to support 3Y/Max x-axis windows

**DS task:** Update script 10 (or produce supplemental output) to generate:
```
advisor_rolling_flows.json additions or replacement:
  stacked_bar: {
    architects: { [period: 'qtd'|'ytd'|'1y'|'3y'|'max']: AdvisorBarEntry[] }
    implementors: { [period]: AdvisorBarEntry[] }
  }
  rolling_1y: {
    architects: AdvisorRollingSeries[]   // daily points, 1Y rolling window
    implementors: AdvisorRollingSeries[]
  }
```
Where `AdvisorBarEntry = { name, inflows, outflows, nna_net }`.
Update `data_contract.xml` before handing to DT.

**Agents:** DS → DT → 0.4.2_RD | DE reviews.

---

### 4D. Leaderboard Sort Stability

**Issue:** Leaderboard entries occasionally render out of order.

**Investigation needed:** Determine whether the issue is:
(a) Frontend sort instability on ties (JS `.sort()` is not stable in all engines for
    equal NNA values), or
(b) Data issue (leaderboard entries in `architect_leaderboard.json` not pre-sorted by rank).

**Fix:** If (a) — use a stable sort (add secondary sort key, e.g. `name`, for ties).
If (b) — fix sort in the publisher Lambda and ensure `rank` field is set correctly.

**Agents:** DE to investigate → 0.4.2_RD if frontend fix, DS + DT if data fix.

---

## 5. Books Tab

### 5A. Access Gating Model

The Books tab serves two user classes with fundamentally different views:

**Admin (L1 — visible only when `userRole === 'admin'`):**
- Sees all advisors in the firm via an advisor selector dropdown
- Can drill into any client's detail view
- L1 is gated to internal users (`isInternal() || isDev()`) using existing `useAuth` pattern

**Advisor (L2 — default landing for non-admins):**
- Lands directly on their own book at login — no dropdown, no selection required
- The portal must resolve the logged-in user → their advisor identity in the gold layer
- Advisor can drill into their own relationships (L3) and accounts (L4)
- Advisor CANNOT see other advisors' relationships or client detail

**Identity resolution (critical path):**
Mapping JWT `userId` → advisor name/ID requires querying `opal-users-v2` DynamoDB table.
This table stores user records keyed by some user identifier. The DS must:
1. Confirm the schema of `opal-users-v2` (what fields identify an advisor)
2. Confirm how those fields map to `accounts_dimension_latest.architect` or
   `rel_architect_lookup.parquet` in the gold layer
3. Determine whether the mapping exists or needs a new registration step
This linkage is the linchpin of the entire Books access model.

**Architecture decision (pending DS investigation):**
The identity resolution should happen at the Lambda level (the API Lambda reads
`opal-users-v2` and scopes its response to the calling user's advisor identity).
The portal should NOT receive cross-advisor data and rely on client-side filtering.
The `opal-partners-data` Lambda or `bd-client-detail` Lambda are the likely candidates
for implementing this scoping.

**Agents:** DS (investigate opal-users-v2 schema) → coordinate with 0.7.0_AE_CloudOps
(auth infrastructure) → DT (deploy Lambda changes).

---

### 5B. Books Tab Hierarchy and Data Scope

**L2 — Advisor Book (aggregate of all relationships):**
- Summary metrics: total AUA, total client count, account count, NNA YTD/QTD/MTD
- AUA composition by client segment (NMNC/NMEC), by geography, by account type
- Tax exposure summary: taxable/deferred/free breakdown (from `client_tax_liability`)
- Income and fees: dividends, interest, fees (from `client_performance`)
- Portfolio composition: asset allocation, expense ratio, concentration
- Engagement: trading activity, avg relationship tenure, active %
- Client list sorted by AUA (for navigation to L3)

**L3 — Relationship/Client view:**
- Same sections as L2 but scoped to one relationship
- Full client detail: all accounts under this relationship
- Performance time series for this relationship's total AUA

**L4 — Account + Holdings:**
- Account-level: AUA, account type, tax status, open date
- Holdings: position list with ticker, name, asset class, current value, weight
- Cost basis and unrealized gain/loss per position (from `03_build_holdings_lots.py`)
- Tax intelligence (primary view): summary of embedded gain/loss by tax status,
  estimated tax liability, positions sorted by unrealized gain
- Lot-level drill-down (secondary, on-demand): individual lots, acquisition date,
  cost basis, unrealized gain/loss — for tax harvest decision support

**Data status for Books:**
- `clients_tab.json`, `advisors/{id}/book.json`: produced by `bd-portal-advisor-publisher`
- Account-level data (`05b_build_account_performance.py`): exists in gold tables
- Holdings lots (`03_build_holdings_lots.py`): exists, with FIFO cost basis
- Tax liability (`06_build_client_tax_liability.py`): exists
- Gap: the publisher Lambda likely does not yet populate all L4 fields. DS must audit
  which fields are present vs. missing from current `clients/{clientKey}.json` output.

---

### 5C. Books Tab — Design Thread Required (COO Action)

The visual design and component decomposition for Books has significant ambiguity.
Before any DE/RD implementation work begins, the COO must run a **bespoke 3-party
thread** to produce a Books design brief:

**Thread configuration:**
- Participants: `0.4.0_DS_ClientPlatform` + `0.4.2_RD_AdvisorIntelligence` + `0.4.0_DE_ClientPlatform`
- Type: Bespoke (gpt-4o, tools enabled, 3 max turns)
- CONTEXT.json must include (M1):
  - `data/black_diamond/scripts/gold/` key script outputs (03, 05b, 06 output shapes)
  - `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`
  - `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`
  - `portal/src/pages/AdvisorIntelligence/ClientDetail/` directory
  - Current `clients_tab.json` S3 output sample
- Opening message must include (M2): DS to push back on any answer not anchored to a specific field in the gold tables or Lambda output.
- Opening question: DS describes what data is available in the gold layer for L2-L4. RD proposes visual layout for each level. DE identifies wiring gaps and component reuse opportunities.

**Thread deliverable:** A markdown design brief at `docs/architecture/advisor_intelligence/books_tab_design_brief.md` covering:
1. L2 advisor book layout (section breakdown with data field mappings)
2. L3 relationship view layout
3. L4 account + holdings view layout with tax summary and lot drill-down
4. Component reuse opportunities (what can be shared across L2/L3/L4)
5. Data gaps DS needs to close before RD can implement

This brief becomes an addendum to this PRD and the source document for the Books tab task orders.

---

## 6. Cross-Cutting: firmId Auth Refactor

**Current state:** Scoped endpoints pass `firmId` as a URL query parameter
(`?firmId=49financial`). This is a security gap — the backend must not trust the
client to self-identify.

**Required state:** `firmId` should come exclusively from the JWT authorizer context
(Cognito `custom:firmId` claim or equivalent). The Lambda reads it from the
`requestContext.authorizer` object injected by API Gateway, not from the query string.

**Scope:** Affects `opal-partners-data` Lambda and any other Lambda that currently
reads `firmId` from the query string for scoped endpoints.

**Agents:** 0.7.0_AE_CloudOps (Cognito claim configuration) + 0.4.0_DT (Lambda update).
This is not blocking completion but must be scheduled before external advisor access goes live.

---

## 7. Work Stream Summary for COO

| Stream | Work | Owner(s) | Blocks |
|--------|------|----------|--------|
| A1 | adv_drill in timeseries_chart.json | 0.4.0_DS | Stream B1, 3B RD |
| A2 | cla_timeseries in timeseries_chart.json | 0.4.0_DS | Stream B1, 3E RD |
| A3 | Stacked bar + 1Y rolling data in advisor_rolling_flows.json | 0.4.0_DS | Stream B2, 4C RD |
| A4 | Snapshot NNA bell curve math verification | 0.4.0_DS | 3C RD (if patch needed) |
| A5 | opal-users-v2 advisor mapping investigation | 0.4.0_DS | Stream J |
| B1 | Deploy bd-portal-publisher with adv_drill + cla_timeseries | 0.4.0_DT | 3B RD, 3E RD |
| B2 | Deploy script 10 updates (stacked bar data) | 0.4.0_DT | 4C RD |
| C1 | Continuous NNA GEO rendering + search + city drill-down | 0.4.2_RD | -- |
| C2 | Continuous NNA ADV rendering + search + client drill-down | 0.4.2_RD | B1 |
| C3 | Snapshot CLA simplified visualization | 0.4.2_RD | -- |
| C4 | Continuous CLA time series rendering | 0.4.2_RD | B1 |
| D | Books tab design thread (COO orchestrates) | COO | Stream E |
| E | Books data contract (DS audits publisher, closes L4 gaps) | 0.4.0_DS | Stream F |
| F | Deploy advisor-publisher with L4 fields | 0.4.0_DT | Stream G |
| G | Books tab implementation | 0.4.0_DE + 0.4.2_RD | F |
| H | Advisors tab portal primitives refactor | 0.4.2_RD | -- (parallel) |
| I | Top Performers visual identity | 0.4.2_RD | -- (parallel) |
| I2 | Leaderboard sort stability investigation + fix | 0.4.0_DE | -- (parallel) |
| J | firmId auth refactor | 0.7.0_AE_CloudOps + 0.4.0_DT | -- (not blocking) |

**Immediate parallel starts (no dependencies):**
Streams A1, A2, A3, A4, A5 (all DS), plus C1 (RD — data already exists), H, I, I2.

---

## 8. Out of Scope for This Release

- `AssetIntelligenceTab.tsx` — exists but not wired to navigation. Formally deferred.
  Will not be wired until Books tab is complete. Revisit in a follow-on PRD.
- Dual timestamp display (`data_as_of` in portal header) — minor polish, tracked
  separately by DE. Non-blocking.
- CausalityEngine — separate initiative, separate PRD.

---

*This document is the single source of truth for AdvisorIntelligence completion.*
*COO: decompose into task orders using the work stream table in Section 7.*
*Reference this document by path in all related task orders.*
```

### advisorintelligence-typescript-types-main-page-types.ts

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
```

### bd-advisor-publisher-lambda-current-s3-output-producer.py

```
"""
BD Portal Advisor Publisher Lambda

Triggered by: S3 ObjectCreated on opal-data-bd/gold/pipeline-complete.json
              (same sentinel as bd-portal-publisher — both run in parallel)

Reads account_performance (the large parquet, ~350MB / 10M rows) to produce:
  - implementor_leaderboard.json   (LeaderboardResponse, by implementor)
  - advisors/{advisor_id}/book.json (AdvisorBookResponse, one per architect)
  - clients/{relationship_id}.json  (ClientDetailResponse, one per client)

Separated from bd-portal-publisher because account_performance is too large
to load alongside the other tables in a single Lambda execution.

Memory: 6144 MB  Timeout: 900 s  Runtime: Python 3.12
Layer:  pandas-pyarrow-layer
"""

import gc
import json
import os
import re
from datetime import datetime, timezone
from io import BytesIO

import boto3
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_BUCKET  = os.environ.get('INPUT_BUCKET',  'opal-data-bd')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'opal-data-bd')
FIRM_ID       = os.environ.get('FIRM_ID',       '49financial')
FIRM_NAME     = os.environ.get('FIRM_NAME',     '49 Financial')

s3 = boto3.client('s3', region_name='us-east-1')

WINDOWS = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _load_parquet(key: str, columns: list = None) -> pd.DataFrame:
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {}
    if columns:
        kwargs['columns'] = columns
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _save_json(data: dict, key: str) -> None:
    body = json.dumps(data, default=str, separators=(',', ':'))
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=body.encode('utf-8'),
        ContentType='application/json',
    )
    print(f"  Wrote {key} ({len(body):,} bytes)")


def _advisor_id(name: str) -> str:
    """Convert advisor display name to URL-safe ID: 'Travis Penfield' -> 'travis_penfield'."""
    clean = re.sub(r'[^a-z0-9_]+', '_', str(name).lower().strip())
    return clean.strip('_') or 'unknown'


def _today() -> pd.Timestamp:
    return pd.Timestamp.now(tz='UTC').normalize().tz_localize(None)


def _window_start(today: pd.Timestamp, days: int) -> pd.Timestamp:
    return today - pd.Timedelta(days=days)


def _latest_holdings_lots_key() -> str | None:
    """Return the S3 key of the most recent holdings_lots snapshot."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=INPUT_BUCKET,
                                       Prefix='gold/holdings_lots/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet') and 'backfill' not in obj['Key']
    ])
    return keys[-1] if keys else None


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_sources() -> dict:
    """Load all three source parquets with column pruning."""
    print("Loading source parquets...")

    # account_performance: all dates needed for window calculations and timeseries
    acct = _load_parquet(
        'gold/account_performance.parquet',
        columns=[
            'date', 'account_id', 'relationship_id',
            'architect', 'implementor',
            'tax_status',
            'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
            'num_positions',
        ],
    )
    acct['date'] = pd.to_datetime(acct['date'])

    # client_tax_liability: for tax exposure per advisor book
    tax = _load_parquet(
        'gold/views/client_tax_liability.parquet',
        columns=[
            'relationship_id', 'account_id',
            'tax_status', 'qualified_flag',
            'asset_name', 'ticker',
            'purchase_year',
            'total_cost_basis', 'total_market_value', 'total_accrued_gain',
            'short_term_gain', 'long_term_gain',
            'num_open_lots',
        ],
    )

    # client_dimension: first_seen_date for new_clients + relationship names
    cdim = _load_parquet(
        'gold/client_dimension.parquet',
        columns=[
            'relationship_id', 'relationship_name',
            'first_seen_date',
            'primary_architect', 'primary_implementor',
        ],
    )
    cdim['first_seen_date'] = pd.to_datetime(cdim['first_seen_date'])

    # holdings_lots: latest snapshot for per-client open lot detail
    lots_key = _latest_holdings_lots_key()
    lots = pd.DataFrame()
    if lots_key:
        lots = _load_parquet(lots_key)
    else:
        print("  WARNING: no holdings_lots snapshot found")

    gc.collect()
    return dict(acct=acct, tax=tax, cdim=cdim, lots=lots)


# ---------------------------------------------------------------------------
# Shared computation helpers
# ---------------------------------------------------------------------------

def _snapshot_on(df: pd.DataFrame, date: pd.Timestamp, dim_col: str) -> pd.DataFrame:
    """Return a snapshot of df grouped by dim_col on the closest available date <= date."""
    dates_available = df['date'].unique()
    past = dates_available[dates_available <= date]
    snap_date = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates_available.min())
    snap = df[df['date'] == snap_date]
    return snap.groupby(dim_col).agg(
        total_aua=('total_aua', 'sum'),
        cum_inflows=('cum_inflows', 'sum'),
        cum_outflows=('cum_outflows', 'sum'),
        nna=('nna', 'sum'),
        num_accounts=('account_id', 'nunique'),
        num_relationships=('relationship_id', 'nunique'),
    ).reset_index()


def _nna_for_window(acct_dim: pd.DataFrame, dim_col: str, dim_val: str,
                     today: pd.Timestamp, days: int) -> float:
    """
    NNA for one advisor over a window.
    acct_dim is already filtered to this advisor's rows.
    NNA = (cum_inflows - cum_outflows) at end_date - at start_date, summed across accounts.
    """
    sub = acct_dim.copy()
    dates = sub['date'].sort_values().unique()
    end_date   = pd.Timestamp(dates.max())
    start_date = _window_start(today, days)

    past = dates[dates <= start_date]
    snap_start = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates.min())

    end_vals   = sub[sub['date'] == end_date].agg(
        cum_inflows=('cum_inflows', 'sum'), cum_outflows=('cum_outflows', 'sum'))
    start_vals = sub[sub['date'] == snap_start].agg(
        cum_inflows=('cum_inflows', 'sum'), cum_outflows=('cum_outflows', 'sum'))

    inflow_delta  = float(end_vals['cum_inflows'])  - float(start_vals['cum_inflows'])
    outflow_delta = float(end_vals['cum_outflows']) - float(start_vals['cum_outflows'])
    return inflow_delta - outflow_delta


# ---------------------------------------------------------------------------
# 1. Implementor leaderboard  (LeaderboardResponse)
# ---------------------------------------------------------------------------

def build_implementor_leaderboard(acct: pd.DataFrame, cdim: pd.DataFrame,
                                   today: pd.Timestamp) -> dict:
    """
    Same structure as architect_leaderboard from bd-portal-publisher.
    Uses account_performance grouped by implementor.
    """
    print("Building implementor_leaderboard.json...")

    latest_date = acct['date'].max()
    windows_data = {}

    for label, days in WINDOWS.items():
        w_start = _window_start(today, days)
        dates   = acct['date'].sort_values().unique()
        past    = dates[dates <= w_start]
        snap_start = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates.min())

        end_snap   = _snapshot_on(acct, latest_date, 'implementor')
        start_snap = _snapshot_on(acct, snap_start,  'implementor').set_index('implementor')

        entries = []
        for _, row in end_snap.iterrows():
            impl = str(row['implementor'])
            if not impl or impl.lower() in ('', 'nan', 'none', 'unassigned',
                                             'no implementor value assigned'):
                impl = 'Unassigned'

            total_aua     = float(row['total_aua'])
            client_count  = int(row['num_relationships'])
            account_count = int(row['num_accounts'])

            s_row      = start_snap.loc[impl] if impl in start_snap.index else None
            nna_end    = float(row['nna'])
            nna_start  = float(s_row['nna']) if s_row is not None else 0.0
            nna_window = nna_end - nna_start

            aua_start_val  = float(s_row['total_aua']) if s_row is not None else 0.0
            aua_growth_pct = (
                (total_aua - aua_start_val) / aua_start_val * 100
                if aua_start_val > 0 else 0.0
            )

            # New clients (relationships) whose primary_implementor matches and joined in window
            cdim_match = cdim[cdim['primary_implementor'] == impl]
            new_clients = int((cdim_match['first_seen_date'] >= w_start).sum())

            entries.append({
                'name':            impl,
                'nna':             round(nna_window, 2),
                'aua_growth_pct':  round(aua_growth_pct, 2),
                'new_clients':     new_clients,
                'total_aua':       round(total_aua, 2),
                'client_count':    client_count,
                'account_count':   account_count,
            })

        entries.sort(key=lambda x: x['nna'], reverse=True)
        for i, e in enumerate(entries):
            e['rank'] = i + 1

        total_nna = sum(e['nna'] for e in entries)
        total_aua_all = sum(e['total_aua'] for e in entries)
        windows_data[label] = {
            'entry_count': len(entries),
            'summary': {
                'total_nna':            round(total_nna, 2),
                'total_aua':            round(total_aua_all, 2),
                'total_new_clients':    sum(e['new_clients'] for e in entries),
                'positive_nna_count':   sum(1 for e in entries if e['nna'] >= 0),
                'negative_nna_count':   sum(1 for e in entries if e['nna'] < 0),
            },
            'entries': entries,
        }
        print(f"  Window {label}: {len(entries)} implementors")

    return {
        'generated_at':     datetime.now(timezone.utc).isoformat(),
        'data_as_of':       latest_date.strftime('%Y-%m-%d'),
        'firm_id':          FIRM_ID,
        'leaderboard_type': 'implementor',
        'available_windows': list(WINDOWS.keys()),
        'windows':          windows_data,
    }


# ---------------------------------------------------------------------------
# 2. Per-advisor book files  (AdvisorBookResponse)
# ---------------------------------------------------------------------------

def _build_advisor_tax_exposure(tax: pd.DataFrame, rel_ids: set) -> dict:
    """Tax exposure for a book of relationships from client_tax_liability."""
    book_tax = tax[tax['relationship_id'].isin(rel_ids)]

    if book_tax.empty:
        return {
            'taxable': 0.0, 'taxable_pct': 0.0,
            'tax_deferred': 0.0, 'tax_deferred_pct': 0.0,
            'tax_free': 0.0, 'tax_free_pct': 0.0,
            'qualified_aua': 0.0, 'qualified_pct': 0.0,
            'non_qualified_aua': 0.0, 'non_qualified_pct': 0.0,
            'non_qualified_cost_basis': 0.0,
            'non_qualified_unrealized_gain': 0.0,
            'short_term_gain': 0.0,
            'long_term_gain': 0.0,
        }

    taxable_mv  = float(book_tax.loc[book_tax['tax_status'] == 'taxable',
                                      'total_market_value'].sum())
    deferred_mv = float(book_tax.loc[book_tax['tax_status'] == 'tax_deferred',
                                      'total_market_value'].sum())
    exempt_mv   = float(book_tax.loc[book_tax['tax_status'] == 'tax_exempt',
                                      'total_market_value'].sum())
    total_mv    = taxable_mv + deferred_mv + exempt_mv

    qual_mv    = float(book_tax.loc[book_tax['qualified_flag'] == True,
                                     'total_market_value'].sum())
    nonqual_mv = float(book_tax.loc[book_tax['qualified_flag'] == False,
                                     'total_market_value'].sum())

    taxable_only = book_tax[book_tax['tax_status'] == 'taxable']
    nq_cost_basis   = float(taxable_only['total_cost_basis'].sum())
    nq_unreal_gain  = float(taxable_only['total_accrued_gain'].sum())
    st_gain         = float(taxable_only['short_term_gain'].sum())
    lt_gain         = float(taxable_only['long_term_gain'].sum())

    def pct(v): return round(v / total_mv * 100, 1) if total_mv > 0 else 0.0
    lot_total = qual_mv + nonqual_mv

    return {
        'taxable':                      round(taxable_mv, 2),
        'taxable_pct':                  pct(taxable_mv),
        'tax_deferred':                 round(deferred_mv, 2),
        'tax_deferred_pct':             pct(deferred_mv),
        'tax_free':                     round(exempt_mv, 2),
        'tax_free_pct':                 pct(exempt_mv),
        'qualified_aua':                round(qual_mv, 2),
        'qualified_pct':                round(qual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0,
        'non_qualified_aua':            round(nonqual_mv, 2),
        'non_qualified_pct':            round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0,
        'non_qualified_cost_basis':     round(nq_cost_basis, 2),
        'non_qualified_unrealized_gain': round(nq_unreal_gain, 2),
        'short_term_gain':              round(st_gain, 2),
        'long_term_gain':               round(lt_gain, 2),
    }


def _build_advisor_engagement(acct_book: pd.DataFrame, cdim: pd.DataFrame,
                               rel_ids: set, today: pd.Timestamp) -> dict:
    """Engagement metrics for one advisor's book."""
    ttm_cutoff = today - pd.Timedelta(days=365)
    dates = acct_book['date'].sort_values().unique()
    latest_date = pd.Timestamp(dates.max())

    past_ttm = dates[dates <= ttm_cutoff]
    ttm_start_date = (pd.Timestamp(past_ttm.max()) if len(past_ttm) > 0
                      else pd.Timestamp(dates.min()))

    end_snap   = acct_book[acct_book['date'] == latest_date]
    start_snap = acct_book[acct_book['date'] == ttm_start_date]

    inflows_ttm  = float(end_snap['cum_inflows'].sum())  - float(start_snap['cum_inflows'].sum())
    outflows_ttm = float(end_snap['cum_outflows'].sum()) - float(start_snap['cum_outflows'].sum())
    net_flows_ttm = inflows_ttm - outflows_ttm

    # Average tenure: days since first_seen_date for matching relationships
    book_cdim = cdim[cdim['relationship_id'].isin(rel_ids)]
    avg_tenure_days = 0
    if not book_cdim.empty and book_cdim['first_seen_date'].notna().any():
        tenure = (today - book_cdim['first_seen_date'].dropna()).dt.days
        avg_tenure_days = int(tenure.mean()) if len(tenure) > 0 else 0

    return {
        'net_flows_ttm':   round(net_flows_ttm, 2),
        'inflows_ttm':     round(inflows_ttm, 2),
        'outflows_ttm':    round(outflows_ttm, 2),
        'avg_tenure_days': avg_tenure_days,
    }


def build_advisor_books(acct: pd.DataFrame, tax: pd.DataFrame,
                         cdim: pd.DataFrame, today: pd.Timestamp) -> list:
    """
    Build one AdvisorBookResponse per architect and return a list of (key, dict) pairs.
    """
    print("Building advisor book files...")

    latest_date  = acct['date'].max()
    all_dates    = acct['date'].sort_values().unique()

    # Identify all architect values present in latest snapshot
    latest_snap = acct[acct['date'] == latest_date]
    architects  = latest_snap['architect'].dropna().unique().tolist()
    print(f"  {len(architects)} architects to process")

    # Pre-compute quarterly NNA start dates
    def _qstart(quarters_back: int) -> pd.Timestamp:
        today_q_month = ((today.month - 1) // 3) * 3 + 1
        month = today_q_month - quarters_back * 3
        year  = today.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        return pd.Timestamp(year=year, month=month, day=1)

    ytd_start = pd.Timestamp(today.year, 1, 1)
    qtd_start = _qstart(0)
    mtd_start = pd.Timestamp(today.year, today.month, 1)

    books = []

    for architect in architects:
        arch_str = str(architect)
        adv_id   = _advisor_id(arch_str)

        # All rows for this architect across all dates
        acct_arch = acct[acct['architect'] == architect]
        if acct_arch.empty:
            continue

        # Relationships in this book (from latest snapshot)
        rel_ids = set(latest_snap.loc[latest_snap['architect'] == architect,
                                       'relationship_id'].unique())

        # ---- Summary (latest date) ----
        snap_latest = acct_arch[acct_arch['date'] == latest_date]
        total_aua     = float(snap_latest['total_aua'].sum())
        account_count = int(snap_latest['account_id'].nunique())
        client_count  = int(snap_latest['relationship_id'].nunique())

        # ---- NNA (ytd / qtd / mtd) ----
        def _nna_since(start_ts: pd.Timestamp) -> float:
            past = all_dates[all_dates <= start_ts]
            snap_start_date = (pd.Timestamp(past.max()) if len(past) > 0
                               else pd.Timestamp(all_dates.min()))
            end_v   = acct_arch[acct_arch['date'] == latest_date]
            start_v = acct_arch[acct_arch['date'] == snap_start_date]
            inf_d  = float(end_v['cum_inflows'].sum())  - float(start_v['cum_inflows'].sum())
            out_d  = float(end_v['cum_outflows'].sum()) - float(start_v['cum_outflows'].sum())
            return inf_d - out_d

        nna_ytd = _nna_since(ytd_start)
        nna_qtd = _nna_since(qtd_start)
        nna_mtd = _nna_since(mtd_start)

        # ---- AUA growth (YTD, QTD) ----
        def _aua_at(start_ts: pd.Timestamp) -> float:
            past = all_dates[all_dates <= start_ts]
            snap_date = (pd.Timestamp(past.max()) if len(past) > 0
                         else pd.Timestamp(all_dates.min()))
            rows = acct_arch[acct_arch['date'] == snap_date]
            return float(rows['total_aua'].sum())

        aua_ytd_start = _aua_at(ytd_start)
        aua_qtd_start = _aua_at(qtd_start)
        ytd_growth_pct = ((total_aua - aua_ytd_start) / aua_ytd_start * 100
                          if aua_ytd_start > 0 else 0.0)
        qtd_growth_pct = ((total_aua - aua_qtd_start) / aua_qtd_start * 100
                          if aua_qtd_start > 0 else 0.0)

        # ---- Tax exposure ----
        tax_exposure = _build_advisor_tax_exposure(tax, rel_ids)

        # ---- Engagement ----
        engagement = _build_advisor_engagement(acct_arch, cdim, rel_ids, today)

        # ---- Client list (sorted by AUA desc) ----
        client_snap = (
            snap_latest
            .groupby('relationship_id')['total_aua']
            .sum()
            .reset_index()
            .merge(cdim[['relationship_id', 'relationship_name']],
                   on='relationship_id', how='left')
            .sort_values('total_aua', ascending=False)
        )
        clients = [
            {
                'client_key':  str(r['relationship_id']),
                'client_name': (str(r['relationship_name'])
                                if pd.notna(r['relationship_name'])
                                else str(r['relationship_id'])),
                'aua': round(float(r['total_aua']), 2),
            }
            for _, r in client_snap.iterrows()
        ]

        book = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'data_as_of':   latest_date.strftime('%Y-%m-%d'),

            'book_type': 'architect',
            'book_key':  adv_id,
            'book_name': arch_str,

            'summary': {
                'total_aua':    round(total_aua, 2),
                'client_count': client_count,
                'account_count': account_count,
            },

            'nna': {
                'ytd': round(nna_ytd, 2),
                'qtd': round(nna_qtd, 2),
                'mtd': round(nna_mtd, 2),
            },

            'growth': {
                'ytd_pct': round(ytd_growth_pct, 2),
                'qtd_pct': round(qtd_growth_pct, 2),
            },

            # Tax exposure from client_tax_liability
            # Includes Yang's qualified/non-qualified and cost basis fields
            'tax_exposure': tax_exposure,

            # Income & fees: not available from BD data
            'income_fees': {
                'income_total_ttm':      0.0,
                'avg_income_yield_pct':  0.0,
                'fees_total_ttm':        0.0,
                'avg_fee_rate_pct':      0.0,
            },

            # Portfolio composition: asset class taxonomy not in BD data
            'portfolio_composition': {
                'asset_allocation':  [],
                'avg_expense_ratio': 0.0,
            },

            'engagement': engagement,
            'clients':    clients,
        }

        books.append((_advisor_output_key(adv_id), book))
        print(f"  {arch_str}: AUA=${total_aua:,.0f}, {client_count} clients, "
              f"{account_count} accounts, NNA_YTD=${nna_ytd:,.0f}")

    return books


def _advisor_output_key(adv_id: str) -> str:
    return f'gold/advisors/{adv_id}/book.json'


# ---------------------------------------------------------------------------
# 3. Per-client detail files  (ClientDetailResponse)
# ---------------------------------------------------------------------------

def _build_headline(acct: pd.DataFrame) -> dict:
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date]
    return {
        'total_aua':        round(float(snap['total_aua'].sum()), 2),
        'account_count':    int(snap['account_id'].nunique()),
        'client_count':     1,
        'fee_rate_pct':     0.0,
        'income_yield_pct': 0.0,
    }


def _build_tax(acct: pd.DataFrame, tax: pd.DataFrame, lots: pd.DataFrame,
               today: pd.Timestamp) -> dict:
    """Full tax section for one household."""
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date]

    total_aua    = float(snap['total_aua'].sum())
    aua_taxable  = float(snap.loc[snap['tax_status'] == 'taxable',   'total_aua'].sum())
    aua_deferred = float(snap.loc[snap['tax_status'] == 'tax_deferred', 'total_aua'].sum())
    aua_exempt   = float(snap.loc[snap['tax_status'] == 'tax_exempt', 'total_aua'].sum())

    def pct(v): return round(v / total_aua * 100, 1) if total_aua > 0 else 0.0

    # --- Qualified vs non-qualified from client_tax_liability ---
    tax_qual    = tax[tax['qualified_flag'] == True]
    tax_nonqual = tax[tax['qualified_flag'] == False]
    tax_taxable = tax[tax['tax_status'] == 'taxable']

    qual_mv    = float(tax_qual['total_market_value'].sum())
    nonqual_mv = float(tax_nonqual['total_market_value'].sum())
    lot_total  = qual_mv + nonqual_mv

    qual_pct    = round(qual_mv    / lot_total * 100, 1) if lot_total > 0 else 0.0
    nonqual_pct = round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0

    qual_acct_count    = int(tax_qual['account_id'].nunique())
    nonqual_acct_count = int(tax_nonqual['account_id'].nunique())

    nq_cost_basis  = float(tax_taxable['total_cost_basis'].sum())
    nq_market_val  = float(tax_taxable['total_market_value'].sum())
    nq_unrealized  = float(tax_taxable['total_accrued_gain'].sum())
    st_gain        = float(tax_taxable['short_term_gain'].sum())
    lt_gain        = float(tax_taxable['long_term_gain'].sum())

    # --- Cost basis by purchase year ---
    year_cols = ['purchase_year', 'total_cost_basis', 'total_market_value',
                 'total_accrued_gain', 'short_term_gain', 'long_term_gain', 'asset_name']
    year_cols_avail = [c for c in year_cols if c in tax_taxable.columns]
    if not tax_taxable.empty and 'purchase_year' in tax_taxable.columns:
        year_agg = (
            tax_taxable[year_cols_avail]
            .groupby('purchase_year', dropna=False)
            .agg(
                cost_basis=('total_cost_basis', 'sum'),
                market_value=('total_market_value', 'sum'),
                unrealized_gain=('total_accrued_gain', 'sum'),
                short_term_gain=('short_term_gain', 'sum'),
                long_term_gain=('long_term_gain', 'sum'),
                num_positions=('asset_name', 'nunique'),
            )
            .reset_index()
            .sort_values('purchase_year')
        )
        cost_basis_by_year = [
            {
                'purchase_year':   int(r['purchase_year']) if pd.notna(r['purchase_year']) else None,
                'cost_basis':      round(float(r['cost_basis']), 2),
                'market_value':    round(float(r['market_value']), 2),
                'unrealized_gain': round(float(r['unrealized_gain']), 2),
                'short_term_gain': round(float(r['short_term_gain']), 2),
                'long_term_gain':  round(float(r['long_term_gain']), 2),
                'num_positions':   int(r['num_positions']),
            }
            for _, r in year_agg.iterrows()
        ]
    else:
        cost_basis_by_year = []

    # --- Top gain positions ---
    if not tax_taxable.empty and 'asset_name' in tax_taxable.columns:
        pos_agg = (
            tax_taxable
            .groupby(['asset_name', 'ticker'], dropna=False)
            .agg(
                cost_basis=('total_cost_basis', 'sum'),
                market_value=('total_market_value', 'sum'),
                unrealized_gain=('total_accrued_gain', 'sum'),
                short_term_gain=('short_term_gain', 'sum'),
                long_term_gain=('long_term_gain', 'sum'),
                num_lots=('num_open_lots', 'sum'),
            )
            .reset_index()
            .sort_values('unrealized_gain', ascending=False)
            .head(20)
        )
        top_gain_positions = [
            {
                'asset_name':      str(r['asset_name']),
                'ticker':          str(r['ticker']) if pd.notna(r['ticker']) else None,
                'cost_basis':      round(float(r['cost_basis']), 2),
                'market_value':    round(float(r['market_value']), 2),
                'unrealized_gain': round(float(r['unrealized_gain']), 2),
                'short_term_gain': round(float(r['short_term_gain']), 2),
                'long_term_gain':  round(float(r['long_term_gain']), 2),
                'num_lots':        int(r['num_lots']),
            }
            for _, r in pos_agg.iterrows()
        ]
    else:
        top_gain_positions = []

    # --- Open lots (taxable only) ---
    open_lots = []
    if not lots.empty:
        taxable_open = lots[
            lots.get('is_open', pd.Series(True, index=lots.index)) == True
        ]
        if 'tax_status' in taxable_open.columns:
            taxable_open = taxable_open[taxable_open['tax_status'] == 'taxable']

        sort_cols = [c for c in ['account_id', 'asset_name', 'lot_index']
                     if c in taxable_open.columns]
        if sort_cols:
            taxable_open = taxable_open.sort_values(sort_cols)

        lot_cols = [
            'account_id', 'account_name',
            'asset_name', 'ticker',
            'acquisition_date', 'purchase_year', 'lot_index',
            'current_units', 'cost_per_unit', 'cost_basis',
            'current_price', 'market_value', 'accrued_gain',
            'holding_period_days', 'term',
        ]
        available = [c for c in lot_cols if c in taxable_open.columns]

        for _, row in taxable_open[available].iterrows():
            lot = {}
            for col in available:
                val = row[col]
                if isinstance(val, (pd.Timestamp,)):
                    lot[col] = val.strftime('%Y-%m-%d')
                elif isinstance(val, float) and pd.notna(val):
                    lot[col] = round(val, 4)
                elif pd.isna(val) if not isinstance(val, str) else False:
                    lot[col] = None
                else:
                    lot[col] = val
            open_lots.append(lot)

    return {
        'taxable':          round(aua_taxable, 2),
        'taxable_pct':      pct(aua_taxable),
        'tax_deferred':     round(aua_deferred, 2),
        'tax_deferred_pct': pct(aua_deferred),
        'tax_free':         round(aua_exempt, 2),
        'tax_free_pct':     pct(aua_exempt),
        'capital_gains_ttm': round(nq_unrealized, 2),
        'qualified_aua':               round(qual_mv, 2),
        'qualified_pct':               qual_pct,
        'non_qualified_aua':           round(nonqual_mv, 2),
        'non_qualified_pct':           nonqual_pct,
        'qualified_account_count':     qual_acct_count,
        'non_qualified_account_count': nonqual_acct_count,
        'non_qualified_cost_basis':      round(nq_cost_basis, 2),
        'non_qualified_market_value':    round(nq_market_val, 2),
        'non_qualified_unrealized_gain': round(nq_unrealized, 2),
        'short_term_gain':               round(st_gain, 2),
        'long_term_gain':                round(lt_gain, 2),
        'cost_basis_by_year': cost_basis_by_year,
        'top_gain_positions': top_gain_positions,
        'open_lots': open_lots,
        'open_lots_count': len(open_lots),
    }


def _build_engagement(acct: pd.DataFrame, cdim_row, today: pd.Timestamp) -> dict:
    """NNA flows TTM and relationship tenure."""
    dates = acct['date'].sort_values().unique()
    latest_date = pd.Timestamp(dates.max())

    ttm_cutoff = today - pd.Timedelta(days=365)
    past_ttm   = dates[dates <= ttm_cutoff]
    ttm_start  = (pd.Timestamp(past_ttm.max()) if len(past_ttm) > 0
                  else pd.Timestamp(dates.min()))

    end_snap   = acct[acct['date'] == latest_date]
    start_snap = acct[acct['date'] == ttm_start]

    inflows_ttm  = float(end_snap['cum_inflows'].sum())  - float(start_snap['cum_inflows'].sum())
    outflows_ttm = float(end_snap['cum_outflows'].sum()) - float(start_snap['cum_outflows'].sum())
    net_flows_ttm = inflows_ttm - outflows_ttm

    avg_relationship_years = 0.0
    if cdim_row is not None and pd.notna(cdim_row.get('first_seen_date')):
        days = (today - cdim_row['first_seen_date']).days
        avg_relationship_years = round(days / 365.25, 2)

    return {
        'trading_buys_ttm':      0,
        'trading_sells_ttm':     0,
        'net_flows_ttm':         round(net_flows_ttm, 2),
        'avg_relationship_years': avg_relationship_years,
        'active_clients_pct':    100.0,
    }


def _build_accounts(acct: pd.DataFrame) -> list:
    """Per-account breakdown for the household drill-down panel."""
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date].copy()

    accounts = []
    for _, row in snap.sort_values('total_aua', ascending=False).iterrows():
        accounts.append({
            'account_id':    str(row['account_id']),
            'tax_status':    str(row.get('tax_status', 'taxable')),
            'total_aua':     round(float(row['total_aua']), 2),
            'cum_inflows':   round(float(row['cum_inflows']), 2),
            'cum_outflows':  round(float(row['cum_outflows']), 2),
            'nna':           round(float(row['nna']), 2),
            'num_positions': int(row.get('num_positions', 0)),
        })
    return accounts


def build_client_details(acct: pd.DataFrame, tax: pd.DataFrame,
                         lots: pd.DataFrame, cdim: pd.DataFrame,
                         today: pd.Timestamp) -> int:
    """Pre-generate gold/clients/{relationship_id}.json for every client."""
    print("Building client detail files...")

    latest_date = acct['date'].max()
    latest_snap = acct[acct['date'] == latest_date]
    all_rel_ids = latest_snap['relationship_id'].dropna().unique()
    print(f"  {len(all_rel_ids)} clients to process")

    count = 0
    for rel_id in all_rel_ids:
        rel_id_str = str(rel_id)

        # Filter each source to this relationship
        acct_r = acct[acct['relationship_id'] == rel_id].copy()
        tax_r  = tax[tax['relationship_id'] == rel_id].copy() if not tax.empty else pd.DataFrame()
        lots_r = lots[lots['relationship_id'] == rel_id].copy() if not lots.empty else pd.DataFrame()
        cdim_rows = cdim[cdim['relationship_id'] == rel_id]
        cdim_row  = cdim_rows.iloc[0] if len(cdim_rows) > 0 else None

        if acct_r.empty:
            continue

        # Client name
        client_name = rel_id_str
        if cdim_row is not None and pd.notna(cdim_row.get('relationship_name')):
            client_name = str(cdim_row['relationship_name'])

        # Build response sections
        headline   = _build_headline(acct_r)
        tax_sec    = _build_tax(acct_r, tax_r, lots_r, today)
        engagement = _build_engagement(acct_r, cdim_row, today)
        accounts   = _build_accounts(acct_r)

        response = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'data_as_of':   latest_date.strftime('%Y-%m-%d'),
            'firm_id':      FIRM_ID,
            'client_key':   rel_id_str,
            'client_name':  client_name,
            'headline':     headline,
            'tax':          tax_sec,
            'income_fees': {
                'dividends_ttm': 0.0, 'interest_ttm': 0.0,
                'total_income_ttm': 0.0, 'income_yield_pct': 0.0,
                'management_fees_ttm': 0.0, 'fee_rate_pct': 0.0,
            },
            'portfolio': {
                'allocation': [],
                'weighted_expense_ratio': 0.0,
                'unique_holdings': int(acct_r[acct_r['date'] == latest_date]['num_positions'].sum()),
                'top_5_concentration_pct': 0.0,
            },
            'engagement': engagement,
            'accounts':   accounts,
        }

        _save_json(response, f'gold/clients/{rel_id_str}.json')
        count += 1

    print(f"  Wrote {count} client detail files")
    return count


# ---------------------------------------------------------------------------
# Lambda handler
# ---------------------------------------------------------------------------

def lambda_handler(event, context):
    print("=" * 70)
    print("BD PORTAL ADVISOR PUBLISHER")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")
    print("=" * 70)

    today = _today()

    try:
        # ------------------------------------------------------------------
        # Step 1: Load parquets
        # ------------------------------------------------------------------
        print("\n=== Step 1: Load parquets ===")
        data = load_sources()
        acct = data['acct']
        tax  = data['tax']
        cdim = data['cdim']
        lots = data['lots']

        # ------------------------------------------------------------------
        # Step 2: Implementor leaderboard
        # ------------------------------------------------------------------
        print("\n=== Step 2: Implementor leaderboard ===")
        impl_lb = build_implementor_leaderboard(acct, cdim, today)
        _save_json(impl_lb, 'gold/implementor_leaderboard.json')

        # ------------------------------------------------------------------
        # Step 3: Per-advisor book files
        # ------------------------------------------------------------------
        print("\n=== Step 3: Advisor book files ===")
        books = build_advisor_books(acct, tax, cdim, today)

        for key, book_data in books:
            _save_json(book_data, key)

        # ------------------------------------------------------------------
        # Step 4: Per-client detail JSONs
        # ------------------------------------------------------------------
        print("\n=== Step 4: Client detail files ===")
        client_count = build_client_details(acct, tax, lots, cdim, today)

        # ------------------------------------------------------------------
        # Step 5: Summary
        # ------------------------------------------------------------------
        latest_date = acct['date'].max()
        total_aua   = float(acct[acct['date'] == latest_date]['total_aua'].sum())

        print(f"\n=== Step 5: Complete ===")
        print(f"  Implementor leaderboard: written")
        print(f"  Advisor books:           {len(books)} files")
        print(f"  Client details:          {client_count} files")
        print(f"  Data as of:              {latest_date.date()}")
        print(f"  Total AUA (acct grain):  ${total_aua:,.0f}")
        print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 70)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':       'success',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'data_as_of':   latest_date.strftime('%Y-%m-%d'),
                'total_aua':    round(total_aua, 2),
                'advisor_books_written': len(books),
                'client_details_written': client_count,
            }),
        }

    except Exception as exc:
        import traceback
        print(f"\nFATAL: {exc}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'error', 'error': str(exc)}),
        }
```

### clientdetailpage-current-l3l4-entry-point.tsx

```
/**
 * Client Detail Page
 *
 * Simple 2x2 layout:
 * - Top left (1x1): AI Executive Summary
 * - Top right (1x1): Portfolio Balance pie charts
 * - Bottom (2x1): Time Series
 */

import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, User } from 'lucide-react'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { Panel, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { AISummaryPanel } from './panels/AISummaryPanel'
import { PortfolioBalancePanel } from './panels/PortfolioBalancePanel'
import { TimeSeriesPanel } from './panels/TimeSeriesPanel'
import type { ClientDetailResponse } from './types'

export function ClientDetailPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  const firmId = searchParams.get('firmId') || '49financial'
  const architectKey = searchParams.get('architectKey')
  const clientKey = searchParams.get('clientKey')
  const clientLabel = searchParams.get('clientLabel') || 'Client'

  const [clientData, setClientData] = useState<ClientDetailResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!clientKey) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- valid data fetching pattern
      setIsLoading(false)
      return
    }
    // TODO: Replace with actual API call
    setTimeout(() => {
      setClientData(null)
      setIsLoading(false)
    }, 300)
  }, [firmId, architectKey, clientKey])

  const handleBack = () => navigate('/advisor-intelligence')

  if (!clientKey) {
    return (
      <PageThemeProvider accentColor="hsl(var(--primary))">
        <Panel variant="chart">
          <PanelContent className="py-12 text-center">
            <p className="text-white/60">No client selected.</p>
            <button onClick={handleBack} className="mt-4 text-[hsl(var(--primary))] hover:underline">
              ← Back to Assets Overview
            </button>
          </PanelContent>
        </Panel>
      </PageThemeProvider>
    )
  }

  return (
    <PageThemeProvider accentColor="hsl(var(--primary))">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleBack}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <ArrowLeft size={20} className="text-white/60" />
          </button>
          <div className="flex items-center gap-3">
            <User size={24} className="text-[hsl(var(--primary))]" />
            <div>
              <h1 className="text-xl font-semibold text-white">{clientLabel}</h1>
              <p className="text-sm text-white/50">
                Architect: {architectKey?.replace(/_/g, ' ') || 'Unknown'}
              </p>
            </div>
          </div>
        </div>

        {isLoading ? (
          <LoadingInline className="py-12" />
        ) : (
          <>
            {/* Top Row: 1x1 + 1x1 */}
            <div className="grid grid-cols-2 gap-6">
              <AISummaryPanel data={clientData} />
              <PortfolioBalancePanel data={clientData} />
            </div>

            {/* Bottom Row: 2x1 */}
            <TimeSeriesPanel data={clientData} />
          </>
        )}
      </div>
    </PageThemeProvider>
  )
}
```

### clientdetail-types-current-portal-types-for-detail-view.ts

```
/**
 * Client Detail Page Types
 * Matches output from 09_generate_client_detail.py
 */

/** Tax exposure breakdown */
export interface TaxExposure {
  taxable: number
  tax_deferred: number
  tax_free: number
  taxable_pct: number
  tax_deferred_pct: number
  tax_free_pct: number
}

/** Portfolio exposure data */
export interface PortfolioExposure {
  tax: TaxExposure
}

/** Time series data point */
export interface ClientTimeSeriesPoint {
  date: string            // "2025-01"
  period: string          // "Jan '25"
  total_aua: number
  inflows: number
  outflows: number
  net_flows: number
}

/** Time series data */
export interface ClientTimeSeries {
  description: string
  start_date: string
  end_date: string
  data: ClientTimeSeriesPoint[]
}

/** AI-generated portfolio summary */
export interface PortfolioSummary {
  summary: string
  characteristics?: string[]
  risk_profile?: 'conservative' | 'moderate' | 'aggressive' | 'unknown'
  objectives?: string[]
  generated_at?: string
}

/** Point-in-time snapshot */
export interface PortfolioSnapshot {
  date: string
  label: string
  total_aua: number
  account_count: number
  exposure?: PortfolioExposure
}

/** Full client detail response */
export interface ClientDetailResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  architect_key: string
  architect_name: string
  client_key: string
  client_name: string

  summary: {
    total_aua: number
    account_count: number
    relationship_start_date?: string
    last_activity_date?: string
  }

  portfolio_summary?: PortfolioSummary
  exposure: PortfolioExposure

  snapshots?: {
    current: PortfolioSnapshot
    q1?: PortfolioSnapshot
    q2?: PortfolioSnapshot
    q3?: PortfolioSnapshot
  }

  timeseries: ClientTimeSeries
}
```

### clientstab-component-current-l2l3-entry-point.tsx

```
/**
 * Books Tab - Advisor Intelligence
 *
 * Individual advisor book drilldown. For admin users, provides
 * advisor selector and client-level detail. For advisor users (future),
 * this is their home page.
 *
 * Layout:
 * +------------------------------------------------------------+
 * |  [Book] [Client]    |  Search clients...                    |
 * +-----------------------------+------------------------------+
 * |    AI Executive Summary     |      Headline Numbers         |
 * +----------+----------+------+-----+-------------------------+
 * |   Tax    |  Income  | Portfolio  |     Engagement           |
 * |  Intel   |  & Fees  |   Comp    |      Metrics             |
 * +----------+----------+-----------+-------------------------+
 */

import { useState, useEffect, useMemo } from 'react'
import { useSelectTracking } from '@/hooks/useFilterTracking'
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { Panel } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import {
  Sparkles,
  DollarSign,
  Users,
  Wallet,
  TrendingUp,
  PiggyBank,
  Receipt,
  Activity,
  Search,
  ChevronDown,
  Building2,
  User,
  ChevronRight,
} from 'lucide-react'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import { getClientsTab, getClientDetail, getArchitectLeaderboard, getAdvisorBook } from '@/api/endpoints/advisor-intelligence'
import { useAuth } from '@/hooks/useAuth'
import type {
  ClientsTabResponse,
  ClientDetailResponse,
  ClientOption,
  ClientsTabHeadline,
  ClientsTabTax,
  ClientsTabIncomeFees,
  ClientsTabPortfolio,
  ClientsTabEngagement,
  LeaderboardEntry,
  AdvisorBookResponse,
} from '../types'

interface BooksTabProps {
  firmId: string
}

type ViewMode = 'book' | 'client'

// Special value for "All Advisors" selection
const ALL_ADVISORS = '__all__'

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export function BooksTab({ firmId }: BooksTabProps) {
  // Auth context for role-based UI
  const { isInternal, isDev } = useAuth()

  // Firm admin can see advisor dropdown and summary table
  // All current users are internal (Opal employees), so everyone sees firm_admin view
  const isFirmAdmin = isInternal() || isDev()

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [bookData, setBookData] = useState<ClientsTabResponse | null>(null)
  const [clientDetailData, setClientDetailData] = useState<ClientDetailResponse | null>(null)
  const [viewMode, setViewMode] = useSelectTracking<ViewMode>('view-mode', 'book', 'advisor-intelligence-clients')
  const [selectedClient, setSelectedClient] = useState<ClientOption | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const [isLoadingClient, setIsLoadingClient] = useState(false)

  // Advisor selection state (for firm admin view)
  const [selectedAdvisor, setSelectedAdvisor] = useState<string>(ALL_ADVISORS)
  const [advisorSummary, setAdvisorSummary] = useState<LeaderboardEntry[]>([])
  const [isAdvisorDropdownOpen, setIsAdvisorDropdownOpen] = useState(false)
  const [advisorBookData, setAdvisorBookData] = useState<AdvisorBookResponse | null>(null)
  const [isLoadingAdvisor, setIsLoadingAdvisor] = useState(false)

  // Fetch book data on mount
  useEffect(() => {
    if (!firmId) {
      setIsLoading(false)
      return
    }

    let cancelled = false
    setIsLoading(true)
    setError(null)

    getClientsTab()
      .then((data) => {
        if (!cancelled) {
          setBookData(data)
          setIsLoading(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch clients tab data:', err)
          setError(err.message || 'Failed to load data')
          setIsLoading(false)
        }
      })

    return () => { cancelled = true }
  }, [firmId])

  // Fetch client detail when a client is selected
  useEffect(() => {
    console.log('[ClientsTab] selectedClient changed:', selectedClient)
    if (!selectedClient) {
      setClientDetailData(null)
      return
    }

    let cancelled = false
    setIsLoadingClient(true)
    console.log('[ClientsTab] Fetching client detail for:', selectedClient.key)

    getClientDetail(selectedClient.key)
      .then((data) => {
        if (!cancelled) {
          setClientDetailData(data)
          setIsLoadingClient(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch client detail:', err)
          // Keep showing book data on error, just log it
          setClientDetailData(null)
          setIsLoadingClient(false)
        }
      })

    return () => { cancelled = true }
  }, [selectedClient])

  // Reset to book view when firm changes
  useEffect(() => {
    setViewMode('book')
    setSelectedClient(null)
    setSearchQuery('')
    setClientDetailData(null)
    setSelectedAdvisor(ALL_ADVISORS)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- setViewMode is stable
  }, [firmId])

  // Fetch advisor summary for firm admin view
  useEffect(() => {
    if (!firmId || !isFirmAdmin) return

    let cancelled = false
    getArchitectLeaderboard()
      .then((data) => {
        if (!cancelled && data?.windows?.['1Y']?.entries) {
          setAdvisorSummary(data.windows['1Y'].entries)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch advisor summary:', err)
        }
      })

    return () => { cancelled = true }
  }, [firmId, isFirmAdmin])

  // Fetch advisor book data when a specific advisor is selected
  useEffect(() => {
    if (!firmId || selectedAdvisor === ALL_ADVISORS) {
      setAdvisorBookData(null)
      return
    }

    // Convert advisor name to ID format (e.g., "Travis Penfield" → "travis_penfield")
    const advisorId = selectedAdvisor.toLowerCase().replace(/\s+/g, '_')

    let cancelled = false
    setIsLoadingAdvisor(true)

    getAdvisorBook(advisorId)
      .then((data) => {
        if (!cancelled) {
          setAdvisorBookData(data)
          setIsLoadingAdvisor(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch advisor book:', err)
          setAdvisorBookData(null)
          setIsLoadingAdvisor(false)
        }
      })

    return () => { cancelled = true }
  }, [firmId, selectedAdvisor])

  // Get clients list - use advisor book clients when advisor selected, otherwise firm book
  const clientsList = useMemo(() => {
    if (selectedAdvisor !== ALL_ADVISORS && advisorBookData?.clients) {
      // Map advisor clients to ClientOption format
      const mapped = advisorBookData.clients.map(c => ({
        key: c.client_key,
        name: c.client_name,
        aua: c.aua,
      }))
      console.log('[ClientsTab] clientsList from advisor book:', mapped.length, 'clients')
      return mapped
    }
    console.log('[ClientsTab] clientsList from firm book:', bookData?.clients?.length ?? 0, 'clients')
    return bookData?.clients ?? []
  }, [selectedAdvisor, advisorBookData, bookData])

  // Get selected advisor name for display
  const selectedAdvisorName = useMemo(() => {
    if (selectedAdvisor === ALL_ADVISORS) return 'All Advisors'
    if (advisorBookData?.book_name) return advisorBookData.book_name
    const advisor = advisorSummary.find(a => a.name === selectedAdvisor)
    return advisor?.name ?? selectedAdvisor
  }, [selectedAdvisor, advisorSummary, advisorBookData])

  // Filter clients based on search query
  const filteredClients = useMemo(() => {
    if (!searchQuery.trim()) return clientsList
    const query = searchQuery.toLowerCase()
    return clientsList.filter(c => c.name.toLowerCase().includes(query))
  }, [searchQuery, clientsList])

  // Calculate relationship years - compute once when client data changes
  // Use state to store computed value and update in effect to avoid impure render
  const [clientRelationshipYears, setClientRelationshipYears] = useState(0)
  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rawDetail = clientDetailData as any
    if (!rawDetail?.summary?.relationship_start_date) {
      setClientRelationshipYears(0)
      return
    }
    const startDate = new Date(rawDetail.summary.relationship_start_date).getTime()
    const years = (Date.now() - startDate) / (365.25 * 24 * 60 * 60 * 1000)
    setClientRelationshipYears(years)
  }, [clientDetailData])

  if (!firmId) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center">
          <p className="text-white/60">Select a partner to view client data</p>
        </PanelContent>
      </Panel>
    )
  }

  if (isLoading) {
    return <LoadingInline className="py-12" />
  }

  if (error) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center">
          <p className="text-red-400">Error: {error}</p>
        </PanelContent>
      </Panel>
    )
  }

  // Select data based on view mode
  // Check that clientDetailData has the expected structure
  // Note: Client detail files use different schema (summary vs headline, exposure.tax vs tax)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawClientDetail = clientDetailData as any
  const hasValidClientDetail = clientDetailData && (rawClientDetail?.summary || clientDetailData.headline)
  const isClientView = viewMode === 'client' && selectedClient && hasValidClientDetail
  const isAdvisorView = selectedAdvisor !== ALL_ADVISORS && advisorBookData

  // Default fallback values
  const defaultHeadline: ClientsTabHeadline = { total_aua: 0, account_count: 0, client_count: 0, fee_rate_pct: 0, income_yield_pct: 0 }
  const defaultTax: ClientsTabTax = { taxable: 0, taxable_pct: 0, tax_deferred: 0, tax_deferred_pct: 0, tax_free: 0, tax_free_pct: 0, capital_gains_ttm: 0 }
  const defaultIncomeFees: ClientsTabIncomeFees = { dividends_ttm: 0, interest_ttm: 0, total_income_ttm: 0, income_yield_pct: 0, management_fees_ttm: 0, fee_rate_pct: 0 }
  const defaultPortfolio: ClientsTabPortfolio = { allocation: [], weighted_expense_ratio: 0, unique_holdings: 0, top_5_concentration_pct: 0 }
  const defaultEngagement: ClientsTabEngagement = { trading_buys_ttm: 0, trading_sells_ttm: 0, net_flows_ttm: 0, avg_relationship_years: 0, active_clients_pct: 0 }

  // Map client detail data (different schema) to panel component types
  // Client detail has: summary, exposure.tax, snapshots, timeseries
  const clientHeadline: ClientsTabHeadline | null = rawClientDetail?.summary ? {
    total_aua: rawClientDetail.summary.total_aua ?? 0,
    account_count: rawClientDetail.summary.account_count ?? 0,
    client_count: 1, // Single client
    fee_rate_pct: 0, // Not available in client detail
    income_yield_pct: 0, // Not available in client detail
  } : null

  const clientTax: ClientsTabTax | null = rawClientDetail?.exposure?.tax ? {
    taxable: rawClientDetail.exposure.tax.taxable ?? 0,
    taxable_pct: rawClientDetail.exposure.tax.taxable_pct ?? 0,
    tax_deferred: rawClientDetail.exposure.tax.tax_deferred ?? 0,
    tax_deferred_pct: rawClientDetail.exposure.tax.tax_deferred_pct ?? 0,
    tax_free: rawClientDetail.exposure.tax.tax_free ?? 0,
    tax_free_pct: rawClientDetail.exposure.tax.tax_free_pct ?? 0,
    capital_gains_ttm: 0, // Not available
  } : null

  // Calculate net flows from timeseries if available
  const clientNetFlowsTTM = rawClientDetail?.timeseries?.data?.slice(-12).reduce(
    (sum: number, d: { net_flows?: number }) => sum + (d.net_flows ?? 0), 0
  ) ?? 0

  const clientEngagement: ClientsTabEngagement | null = rawClientDetail?.summary ? {
    trading_buys_ttm: 0, // Not available
    trading_sells_ttm: 0, // Not available
    net_flows_ttm: clientNetFlowsTTM,
    avg_relationship_years: clientRelationshipYears,
    active_clients_pct: 100, // Single client, assume active
  } : null

  // Map advisor book data to existing panel component types
  const advisorHeadline: ClientsTabHeadline | null = advisorBookData ? {
    total_aua: advisorBookData.summary.total_aua,
    account_count: advisorBookData.summary.account_count,
    client_count: advisorBookData.summary.client_count,
    fee_rate_pct: advisorBookData.income_fees.avg_fee_rate_pct,
    income_yield_pct: advisorBookData.income_fees.avg_income_yield_pct,
  } : null

  const advisorTax: ClientsTabTax | null = advisorBookData ? {
    taxable: advisorBookData.tax_exposure.taxable,
    taxable_pct: advisorBookData.tax_exposure.taxable_pct,
    tax_deferred: advisorBookData.tax_exposure.tax_deferred,
    tax_deferred_pct: advisorBookData.tax_exposure.tax_deferred_pct,
    tax_free: advisorBookData.tax_exposure.tax_free,
    tax_free_pct: advisorBookData.tax_exposure.tax_free_pct,
    capital_gains_ttm: 0, // Not available in advisor book
  } : null

  const advisorIncomeFees: ClientsTabIncomeFees | null = advisorBookData ? {
    dividends_ttm: 0, // Not available in advisor book (only total income)
    interest_ttm: 0, // Not available in advisor book
    total_income_ttm: advisorBookData.income_fees.income_total_ttm,
    income_yield_pct: advisorBookData.income_fees.avg_income_yield_pct,
    management_fees_ttm: advisorBookData.income_fees.fees_total_ttm,
    fee_rate_pct: advisorBookData.income_fees.avg_fee_rate_pct,
  } : null

  const advisorPortfolio: ClientsTabPortfolio | null = advisorBookData ? {
    allocation: advisorBookData.portfolio_composition.asset_allocation.map(a => ({
      name: a.label,
      pct: a.pct,
    })),
    weighted_expense_ratio: advisorBookData.portfolio_composition.avg_expense_ratio,
    unique_holdings: 0, // Not available in advisor book
    top_5_concentration_pct: 0, // Not available in advisor book
  } : null

  const advisorEngagement: ClientsTabEngagement | null = advisorBookData ? {
    trading_buys_ttm: 0, // Not available in advisor book
    trading_sells_ttm: 0, // Not available in advisor book
    net_flows_ttm: advisorBookData.engagement.net_flows_ttm,
    avg_relationship_years: advisorBookData.engagement.avg_tenure_days / 365,
    active_clients_pct: 100, // Not available in advisor book, assume 100%
  } : null

  // Select appropriate data source: client detail > advisor book > firm book > defaults
  // Note: Client detail uses mapped values (clientHeadline, clientTax, etc.) due to different schema
  const headlineData: ClientsTabHeadline = isClientView
    ? (clientHeadline ?? defaultHeadline)
    : isAdvisorView
    ? (advisorHeadline ?? defaultHeadline)
    : (bookData?.headline ?? defaultHeadline)

  const taxData: ClientsTabTax = isClientView
    ? (clientTax ?? defaultTax)
    : isAdvisorView
    ? (advisorTax ?? defaultTax)
    : (bookData?.tax ?? defaultTax)

  const incomeFeesData: ClientsTabIncomeFees = isClientView
    ? defaultIncomeFees // Client detail doesn't have income/fees breakdown
    : isAdvisorView
    ? (advisorIncomeFees ?? defaultIncomeFees)
    : (bookData?.income_fees ?? defaultIncomeFees)

  const portfolioData: ClientsTabPortfolio = isClientView
    ? defaultPortfolio // Client detail doesn't have portfolio composition
    : isAdvisorView
    ? (advisorPortfolio ?? defaultPortfolio)
    : (bookData?.portfolio ?? defaultPortfolio)

  const engagementData: ClientsTabEngagement = isClientView
    ? (clientEngagement ?? defaultEngagement)
    : isAdvisorView
    ? (advisorEngagement ?? defaultEngagement)
    : (bookData?.engagement ?? defaultEngagement)

  const handleClientSelect = (client: ClientOption) => {
    console.log('[ClientsTab] handleClientSelect called:', client)
    setSelectedClient(client)
    setSearchQuery('')
    setIsDropdownOpen(false)
  }

  return (
    <Panel variant="chart" className="p-0">
      {/* Header Bar: View Mode Toggle + Advisor Picker (firm admin) + Client Picker */}
      <div className="flex items-center gap-4 p-4 border-b border-white/10">
        {/* View Mode Toggle */}
        <div className="flex items-center bg-white/10 rounded-lg p-1">
          <button
            onClick={() => {
              setViewMode('book')
              setSelectedClient(null)
            }}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
              viewMode === 'book'
                ? 'bg-[hsl(var(--primary))] text-white'
                : 'text-white/60 hover:text-white/80 hover:bg-white/10'
            }`}
          >
            <Building2 size={14} />
            Book
          </button>
          <button
            onClick={() => setViewMode('client')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
              viewMode === 'client'
                ? 'bg-[hsl(var(--primary))] text-white'
                : 'text-white/60 hover:text-white/80 hover:bg-white/10'
            }`}
          >
            <User size={14} />
            Client
          </button>
        </div>

        {/* Advisor Picker - only for firm admin */}
        {isFirmAdmin && (
          <div className="relative">
            <button
              onClick={() => setIsAdvisorDropdownOpen(!isAdvisorDropdownOpen)}
              className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white hover:bg-white/10 hover:border-white/20 transition-colors"
            >
              <Users size={14} className="text-white/50" />
              <span className="max-w-[140px] truncate">{selectedAdvisorName}</span>
              <ChevronDown size={14} className={`text-white/50 transition-transform ${isAdvisorDropdownOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Advisor Dropdown */}
            {isAdvisorDropdownOpen && (
              <div className="absolute top-full left-0 mt-1 bg-[#1e1e2d] border border-white/20 rounded-lg shadow-xl z-50 min-w-[200px] max-h-64 overflow-y-auto">
                {/* All Advisors option */}
                <div
                  onClick={() => {
                    setSelectedAdvisor(ALL_ADVISORS)
                    setIsAdvisorDropdownOpen(false)
                  }}
                  className={`px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors ${
                    selectedAdvisor === ALL_ADVISORS ? 'bg-white/15' : ''
                  }`}
                >
                  <span className="text-sm text-white font-medium">All Advisors</span>
                </div>
                <div className="border-t border-white/10" />
                {/* Individual advisors - sorted by AUA descending */}
                {[...advisorSummary].sort((a, b) => b.total_aua - a.total_aua).map((advisor) => (
                  <div
                    key={advisor.name}
                    onClick={() => {
                      setSelectedAdvisor(advisor.name)
                      setIsAdvisorDropdownOpen(false)
                    }}
                    className={`px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors ${
                      selectedAdvisor === advisor.name ? 'bg-white/15' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white">{advisor.name}</span>
                      <span className="text-xs text-white/50">{formatCurrency(advisor.total_aua)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Client Picker - always visible */}
        <div className="relative flex-1 max-w-md">
          <div
            className={`flex items-center gap-2 border rounded-lg px-3 py-2 transition-colors ${
              viewMode === 'client'
                ? 'bg-white/10 border-white/20 cursor-pointer hover:border-white/30'
                : 'bg-white/5 border-white/10 cursor-pointer hover:border-white/20'
            }`}
            onClick={() => {
              if (viewMode === 'book') setViewMode('client')
              setIsDropdownOpen(!isDropdownOpen)
            }}
          >
            <Search size={14} className="text-white/50" />
            <input
              type="text"
              placeholder={selectedClient ? selectedClient.name : "Search clients..."}
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value)
                if (viewMode === 'book') setViewMode('client')
                setIsDropdownOpen(true)
              }}
              onClick={(e) => {
                e.stopPropagation()
                if (viewMode === 'book') setViewMode('client')
                setIsDropdownOpen(true)
              }}
              className="flex-1 bg-transparent text-sm text-white placeholder-white/50 outline-none"
            />
            <ChevronDown size={14} className={`text-white/50 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </div>

          {/* Dropdown */}
          {isDropdownOpen && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-[#1e1e2d] border border-white/20 rounded-lg shadow-xl z-50 max-h-64 overflow-y-auto">
              {filteredClients.length === 0 ? (
                <div className="px-3 py-4 text-sm text-white/50 text-center">
                  No clients found
                </div>
              ) : (
                filteredClients.map((client) => (
                  <div
                    key={client.key}
                    onClick={() => handleClientSelect(client)}
                    className={`px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors ${
                      selectedClient?.key === client.key ? 'bg-white/15' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white">{client.name}</span>
                      <span className="text-xs text-white/60">{formatCurrency(client.aua)}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Selected advisor/client badge */}
        {(selectedAdvisor !== ALL_ADVISORS || selectedClient) && (
          <div className="text-sm text-white/70 flex items-center gap-2">
            {selectedClient ? (
              <>
                Viewing: <span className="text-white font-medium">{selectedClient.name}</span>
                {isLoadingClient && <span className="text-white/50 text-xs">(Loading...)</span>}
              </>
            ) : selectedAdvisor !== ALL_ADVISORS && (
              <>
                Advisor: <span className="text-white font-medium">{selectedAdvisorName}</span>
                {isLoadingAdvisor && <span className="text-white/50 text-xs">(Loading...)</span>}
              </>
            )}
          </div>
        )}
      </div>

      {/* Advisor Summary Table - Show when "All Advisors" selected and firm admin */}
      {isFirmAdmin && selectedAdvisor === ALL_ADVISORS && advisorSummary.length > 0 && (
        <div className="p-4 border-b border-white/10">
          <AdvisorSummaryTable
            data={advisorSummary}
            onSelectAdvisor={(advisorName) => {
              setSelectedAdvisor(advisorName)
            }}
          />
        </div>
      )}

      {/* Content Area - always visible */}
      <div className="p-4 space-y-4">
        {/* Top Row: AI Summary + Headline Numbers */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <SubPanel>
            <SubPanelHeader title="AI Executive Summary" />
            <div className="flex items-center justify-center h-[140px]">
              <div className="flex flex-col items-center">
                <Sparkles size={28} className="text-[hsl(var(--primary))]/40 mb-2" />
                <p className="text-xs text-white/50 text-center max-w-[200px]">
                  {isClientView
                    ? `AI summary for ${selectedClient?.name} coming soon.`
                    : selectedAdvisor !== ALL_ADVISORS
                    ? `Insights for ${selectedAdvisorName} coming soon.`
                    : "Firm-wide insights coming soon."
                  }
                </p>
              </div>
            </div>
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Headline Numbers" />
            <HeadlineNumbersContent data={headlineData} isClientView={!!isClientView} />
          </SubPanel>
        </div>

        {/* Bottom Row: 4 equal panels */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <SubPanel>
            <SubPanelHeader title="Tax Intelligence" />
            <TaxIntelligenceContent data={taxData} />
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Income & Fees" />
            <IncomeFeesContent data={incomeFeesData} />
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Portfolio Composition" />
            <PortfolioCompositionContent data={portfolioData} />
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Engagement Metrics" />
            <EngagementMetricsContent data={engagementData} />
          </SubPanel>
        </div>
      </div>
    </Panel>
  )
}

// ============================================================================
// SUB-PANEL COMPONENTS (Internal containers within the main panel)
// ============================================================================

function PanelContent({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <div className={className}>{children}</div>
}

function SubPanel({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`bg-white/5 rounded-lg border border-white/10 overflow-hidden ${className}`}>
      {children}
    </div>
  )
}

function SubPanelHeader({ title }: { title: string }) {
  return (
    <div className="px-4 py-2.5 bg-[hsl(var(--bg-header))] rounded-t-lg">
      <h3 className="text-xs font-semibold text-white uppercase tracking-wide">{title}</h3>
    </div>
  )
}

// ============================================================================
// CONTENT COMPONENTS (Just the inner content, no panel wrapper)
// ============================================================================

/** Headline Numbers Content */
function HeadlineNumbersContent({ data, isClientView }: { data: ClientsTabHeadline; isClientView?: boolean }) {
  const metrics = isClientView ? [
    { label: 'Total AUA', value: formatCurrency(data.total_aua), icon: DollarSign },
    { label: 'Accounts', value: data.account_count.toLocaleString(), icon: Wallet },
    { label: 'Fee Rate', value: `${data.fee_rate_pct.toFixed(2)}%`, icon: Receipt },
    { label: 'Income Yield', value: `${data.income_yield_pct.toFixed(2)}%`, icon: TrendingUp },
  ] : [
    { label: 'Total AUA', value: formatCurrency(data.total_aua), icon: DollarSign },
    { label: 'Accounts', value: data.account_count.toLocaleString(), icon: Wallet },
    { label: 'Clients', value: data.client_count.toLocaleString(), icon: Users },
    { label: 'Fee Rate', value: `${data.fee_rate_pct.toFixed(2)}%`, icon: Receipt },
    { label: 'Income Yield', value: `${data.income_yield_pct.toFixed(2)}%`, icon: TrendingUp },
  ]

  return (
    <div className="p-3">
      <div className="grid grid-cols-2 gap-2">
        {/* Total AUA - large, spans full width */}
        <div className="col-span-2 bg-white/5 rounded-lg p-2.5 text-center">
          <p className="text-xl font-bold text-white">{metrics[0].value}</p>
          <p className="text-[10px] text-white/50">{metrics[0].label}</p>
        </div>
        {/* Other metrics - 2x2 grid */}
        {metrics.slice(1).map((metric, i) => (
          <div key={i} className="bg-white/5 rounded-lg p-2 flex items-center gap-2">
            <metric.icon size={14} className="text-white/40 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-white">{metric.value}</p>
              <p className="text-[10px] text-white/50">{metric.label}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ============================================================================
// BOTTOM ROW CONTENT COMPONENTS
// ============================================================================

const TAX_COLORS = ['#EF4444', '#F59E0B', '#10B981'] // Taxable, Deferred, Free

/** Tax Intelligence Content */
function TaxIntelligenceContent({ data }: { data: ClientsTabTax }) {
  const pieData = [
    { name: 'Taxable', value: data.taxable_pct, amount: data.taxable },
    { name: 'Tax-Deferred', value: data.tax_deferred_pct, amount: data.tax_deferred },
    { name: 'Tax-Free', value: data.tax_free_pct, amount: data.tax_free },
  ]

  return (
    <div className="p-4">
      {/* Pie Chart */}
      <div className="flex justify-center">
        <ResponsiveContainer width="100%" height={140}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={60}
              dataKey="value"
              stroke="rgba(0,0,0,0.3)"
              strokeWidth={1}
            >
              {pieData.map((_, i) => (
                <Cell key={i} fill={TAX_COLORS[i]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="space-y-1.5 mt-3">
        {pieData.map((item, i) => (
          <div key={i} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: TAX_COLORS[i] }} />
              <span className="text-white/70">{item.name}</span>
            </div>
            <span className="text-white/90 font-medium">{item.value}%</span>
          </div>
        ))}
      </div>

      {/* Capital Gains callout */}
      <div className="mt-4 pt-3 border-t border-white/10">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">TTM Capital Gains</span>
          <span className="text-white/80 font-medium">{formatCurrency(data.capital_gains_ttm)}</span>
        </div>
      </div>
    </div>
  )
}

/** Income & Fees Content */
function IncomeFeesContent({ data }: { data: ClientsTabIncomeFees }) {
  return (
    <div className="p-4">
      {/* Income Section */}
      <div className="space-y-2">
        <div className="flex items-center gap-2 text-white/50 text-xs">
          <PiggyBank size={14} />
          <span>TTM Income</span>
        </div>
        <div className="bg-white/5 rounded-lg p-2.5">
          <p className="text-base font-bold text-[#10B981]">{formatCurrency(data.total_income_ttm)}</p>
          <div className="flex justify-between text-[10px] text-white/50 mt-1">
            <span>Div: {formatNumberTo3Digits(data.dividends_ttm, { unit: '$' })}</span>
            <span>Int: {formatNumberTo3Digits(data.interest_ttm, { unit: '$' })}</span>
          </div>
        </div>
        <div className="flex justify-between text-xs">
          <span className="text-white/50">Income Yield</span>
          <span className="text-[#10B981] font-medium">{data.income_yield_pct.toFixed(2)}%</span>
        </div>
      </div>

      {/* Fees Section */}
      <div className="space-y-2 mt-4">
        <div className="flex items-center gap-2 text-white/50 text-xs">
          <Receipt size={14} />
          <span>TTM Fees</span>
        </div>
        <div className="bg-white/5 rounded-lg p-2.5">
          <p className="text-base font-bold text-white">{formatCurrency(data.management_fees_ttm)}</p>
          <p className="text-[10px] text-white/50 mt-1">Management Fees</p>
        </div>
        <div className="flex justify-between text-xs">
          <span className="text-white/50">Fee Rate</span>
          <span className="text-white/80 font-medium">{data.fee_rate_pct.toFixed(2)}%</span>
        </div>
      </div>
    </div>
  )
}

/** Portfolio Composition Content */
function PortfolioCompositionContent({ data }: { data: ClientsTabPortfolio }) {
  const ALLOCATION_COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#6B7280']

  return (
    <div className="p-4">
      {/* Allocation bars */}
      <div className="space-y-2.5">
        {data.allocation.map((item, i) => (
          <div key={i} className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className="text-white/70">{item.name}</span>
              <span className="text-white/90 font-medium">{item.pct}%</span>
            </div>
            <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all"
                style={{ width: `${item.pct}%`, backgroundColor: ALLOCATION_COLORS[i] }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Metrics */}
      <div className="pt-3 border-t border-white/10 space-y-1.5 mt-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Holdings</span>
          <span className="text-white/80 font-medium">{data.unique_holdings.toLocaleString()}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Top 5 Conc.</span>
          <span className="text-white/80 font-medium">{data.top_5_concentration_pct}%</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Avg ER</span>
          <span className="text-white/80 font-medium">{data.weighted_expense_ratio.toFixed(2)}%</span>
        </div>
      </div>
    </div>
  )
}

/** Engagement Metrics Content */
function EngagementMetricsContent({ data }: { data: ClientsTabEngagement }) {
  return (
    <div className="p-4">
      {/* Net Flows */}
      <div className="bg-white/5 rounded-lg p-3 text-center">
        <p className={`text-lg font-bold ${data.net_flows_ttm >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
          {data.net_flows_ttm >= 0 ? '+' : ''}{formatCurrency(data.net_flows_ttm)}
        </p>
        <p className="text-[10px] text-white/50 mt-1">TTM Net Flows</p>
      </div>

      {/* Trading Activity */}
      <div className="space-y-2 mt-4">
        <div className="flex items-center gap-2 text-white/50 text-xs">
          <Activity size={14} />
          <span>TTM Trading</span>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-white/5 rounded-lg p-2 text-center">
            <p className="text-sm font-semibold text-[#10B981]">{data.trading_buys_ttm.toLocaleString()}</p>
            <p className="text-[10px] text-white/50">Buys</p>
          </div>
          <div className="bg-white/5 rounded-lg p-2 text-center">
            <p className="text-sm font-semibold text-[#EF4444]">{data.trading_sells_ttm.toLocaleString()}</p>
            <p className="text-[10px] text-white/50">Sells</p>
          </div>
        </div>
      </div>

      {/* Relationship Metrics */}
      <div className="pt-3 border-t border-white/10 space-y-1.5 mt-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Avg Tenure</span>
          <span className="text-white/80 font-medium">{data.avg_relationship_years.toFixed(2)} yrs</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Active</span>
          <span className="text-[#10B981] font-medium">{data.active_clients_pct}%</span>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// ADVISOR SUMMARY TABLE (Firm Admin View)
// ============================================================================

interface AdvisorSummaryTableProps {
  data: LeaderboardEntry[]
  onSelectAdvisor: (advisorName: string) => void
}

/** Advisor Summary Table - Shows when "All Advisors" is selected */
function AdvisorSummaryTable({ data, onSelectAdvisor }: AdvisorSummaryTableProps) {
  return (
    <SubPanel>
      <SubPanelHeader title="Advisor Summary" />
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/10">
              <th className="text-left text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">Advisor</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">AUA</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">Clients</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">NNA (1Y)</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">Growth</th>
              <th className="w-8"></th>
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 10).map((advisor, i) => (
              <tr
                key={advisor.name}
                onClick={() => onSelectAdvisor(advisor.name)}
                className="border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors group"
              >
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-white/30 w-4">{i + 1}</span>
                    <span className="text-sm text-white font-medium">{advisor.name}</span>
                  </div>
                </td>
                <td className="text-right px-4 py-3">
                  <span className="text-sm text-white/80 font-mono">{formatCurrency(advisor.total_aua)}</span>
                </td>
                <td className="text-right px-4 py-3">
                  <span className="text-sm text-white/70">{advisor.client_count.toLocaleString()}</span>
                </td>
                <td className="text-right px-4 py-3">
                  <span className={`text-sm font-mono ${advisor.nna >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
                    {advisor.nna >= 0 ? '+' : ''}{formatCurrency(advisor.nna)}
                  </span>
                </td>
                <td className="text-right px-4 py-3">
                  <span className={`text-sm font-medium ${advisor.aua_growth_pct >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
                    {advisor.aua_growth_pct >= 0 ? '+' : ''}{advisor.aua_growth_pct.toFixed(1)}%
                  </span>
                </td>
                <td className="px-2 py-3">
                  <ChevronRight size={14} className="text-white/30 group-hover:text-white/60 transition-colors" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data.length > 10 && (
        <div className="px-4 py-2 text-center text-[10px] text-white/40 border-t border-white/5">
          Showing top 10 of {data.length} advisors
        </div>
      )}
    </SubPanel>
  )
}
```

### script-03--holdings-lots-builder-l4-source.py

```
#!/usr/bin/env python3
"""
Build Holdings Lots — Individual Lot Tracking for Tax Calculations

Produces a lot-level snapshot of all open positions, enabling:
  - Short-term vs long-term capital gain classification
  - Tax liability estimation per account and household
  - Drill-down: household → account → position → lot

Schema:
  lot_id                    str   — "{account_id}:{asset_name}:{lot_index}:{buy_date}"
  snapshot_date             date  — date of this snapshot (today's date)
  account_id                str
  relationship_id           str   — household key (from accounts_dimension)
  account_name              str   — display name (from accounts_dimension)
  account_type              str   — e.g. 'IRA', 'RothIRA', 'Brokerage' (from BD allocations)
  account_registration_type str   — e.g. 'Contributory IRA', 'Individual' (from BD allocations)
  tax_status                str   — 'taxable' | 'tax_deferred' | 'tax_exempt'
  qualified_flag            bool  — False = taxable (non-qualified); True = retirement account
  asset_name                str
  ticker                    str   (may be null for unmapped assets)
  acquisition_date          date  — when this lot was purchased
  purchase_year             int   — year(acquisition_date)
  lot_index                 int   — FIFO order within this position (1 = oldest)
  original_units            float — units purchased in this lot
  current_units             float — units remaining after FIFO sells
  cost_per_unit             float — per-unit purchase price
  cost_basis                float — current_units × cost_per_unit
  current_price             float — latest canonical price
  market_value              float — current_units × current_price
  accrued_gain              float — market_value − cost_basis
  holding_period_days       int   — snapshot_date − acquisition_date
  term                      str   — 'short_term' (< 365 days) | 'long_term' (≥ 365)
  is_open                   bool  — True if current_units > 0
  price_quality             str   — price source label

Input:
  - silver/transactions/                    — deduplicated transaction history
  - silver/prices/                          — canonical daily prices
  - gold/accounts_dimension_latest.parquet  — account metadata (tax_status, qualified_flag, etc.)

Output:
  - gold/holdings_lots/YYYY-MM-DD.parquet  (snapshot for today)
  - gold/holdings_lots/backfill_YYYY-MM-DD_to_YYYY-MM-DD.parquet  (--full)

Usage:
    python 03_build_holdings_lots.py --dry-run
    python 03_build_holdings_lots.py --upload
    python 03_build_holdings_lots.py --upload --full   (backfill all dates)

Author: Data Scientist (Claude)
Date: 2026-02-19
"""

import argparse
import gc
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, date
from pathlib import Path
from io import BytesIO
from typing import List, Optional

import pandas as pd
import numpy as np
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')
MAX_WORKERS = 64

SHORT_TERM_DAYS = 365  # < 365 days -> short-term capital gain

# Transaction types matched to silver/transactions/ values
BUY_TYPES = frozenset({
    'Buy', 'Reinvestment', 'Dividend Reinvestment',
    'Income Reinvestment', 'Capital Gains Reinvestment',
    'Transfer In', 'Buy to Close',
    'Option Exercise', 'Short Cover',
})
SELL_TYPES = frozenset({
    'Sale', 'Short Sale', 'Transfer Out',
    'Expiration', 'Option Exercise (sell)',
})

# Corporate Action sub-types (from transaction_sub_type column).
# Canonical reference: 02_build_positions_cube.py defines these identically.
# See docs/data/transaction_type_canonical_reference.md for the full taxonomy.
CA_BUY_SUBTYPES = frozenset({
    'Conversion In',   # new share class appears (paired with Conversion Out)
    'Spinoff',         # new position spun off from parent
    'Split',           # additional units from stock split
})
CA_SELL_SUBTYPES = frozenset({
    'Merger',          # old ticker ceases to exist -- units exit
    'Conversion Out',  # old share class leaves (paired with Conversion In)
    'Cash in Lieu',    # fractional share cleanup -- small unit removal
    'Reverse Split',   # units reduced by reverse split
})


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_transactions() -> pd.DataFrame:
    """Load all deduplicated transactions with parallel I/O."""
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading transactions (parallel)... ", end='', flush=True)

    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/transactions/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])

    if not keys:
        raise RuntimeError("No transaction parquet files found")

    t0 = datetime.now(timezone.utc)
    dfs = [None] * len(keys)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_read_parquet_from_s3, k): i for i, k in enumerate(keys)}
        done = 0
        for future in as_completed(futures):
            dfs[futures[future]] = future.result()
            done += 1
            if done % 500 == 0:
                print(f"[{done:,}/{len(keys):,}]", end=' ', flush=True)

    df = pd.concat(dfs, ignore_index=True)
    del dfs; gc.collect()
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()

    if 'transaction_id' in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=['transaction_id'], keep='last')
        removed = before - len(df)
        print(f"{len(df):,} rows ({removed:,} dupes) in {elapsed:.1f}s")
    else:
        print(f"{len(df):,} rows in {elapsed:.1f}s")

    df['trade_date'] = pd.to_datetime(df['trade_date'])
    return df


def load_latest_prices() -> pd.DataFrame:
    """Load most recent price for each asset from canonical prices."""
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading canonical prices...", end=' ', flush=True)

    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/prices/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])

    if not keys:
        raise RuntimeError("No canonical prices found. Run build_canonical_prices_v2.py first.")

    dfs = [pd.read_parquet(BytesIO(s3.get_object(Bucket=S3_BUCKET, Key=k)['Body'].read()))
           for k in sorted(keys)]
    prices = pd.concat(dfs, ignore_index=True)
    prices['date'] = pd.to_datetime(prices['date'])

    # Keep latest price per asset
    latest = (prices.sort_values('date', ascending=False)
              .drop_duplicates(subset=['asset_name'], keep='first')
              [['asset_name', 'ticker', 'price', 'source', 'date']])

    print(f"{len(prices):,} rows loaded → {len(latest):,} assets (latest price)")
    return latest


def load_accounts_dimension() -> pd.DataFrame:
    """Load gold/accounts_dimension_latest.parquet for account metadata enrichment.

    Returns DataFrame with account_id, relationship_id, account_name, account_type,
    account_registration_type, tax_status, qualified_flag.
    Returns empty DataFrame if not yet built (script degrades gracefully).
    """
    print("Loading accounts dimension...", end=' ', flush=True)
    key = 'gold/accounts_dimension_latest.parquet'
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        # Keep only the columns we need for enrichment
        keep = ['account_id', 'relationship_id', 'account_name', 'account_type',
                'account_registration_type', 'tax_status', 'qualified_flag']
        available = [c for c in keep if c in df.columns]
        df = df[available].drop_duplicates(subset=['account_id'], keep='first')
        print(f"{len(df):,} accounts")
        return df
    except Exception as e:
        print(f"not found ({e}) — lots will lack tax metadata")
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Core FIFO lot builder
# ---------------------------------------------------------------------------

def build_lots_for_group(
        account_id: str,
        asset_name: str,
        group_txns: pd.DataFrame,
) -> List[dict]:
    """
    Build open lot list for one (account, asset) position using FIFO.

    Process:
    1. Create one lot per buy transaction (sorted oldest first)
    2. Apply sells in chronological order, depleting oldest lots first
    3. Return all lots with remaining units (open lots)
       plus closed lots (for realized gain tracking)

    Expects a pre-classified '_is_buy' boolean column on group_txns
    (True = buy/CA-buy, False = sell/CA-sell).

    Returns list of lot dicts.
    """
    buys = (group_txns[group_txns['_is_buy']]
            .sort_values('trade_date')
            .reset_index(drop=True))
    sells = (group_txns[~group_txns['_is_buy']]
             .sort_values('trade_date')
             .reset_index(drop=True))

    if len(buys) == 0:
        return []

    # Initialize lots
    lots = []
    for lot_idx, (_, row) in enumerate(buys.iterrows(), start=1):
        units = abs(row['units'])
        if units == 0:
            continue
        mv = abs(row.get('market_value', 0) or 0)
        cost_per_unit = mv / units if units > 0 else 0.0
        lots.append({
            'lot_index': lot_idx,
            'acquisition_date': row['trade_date'],
            'original_units': units,
            'remaining_units': units,
            'cost_per_unit': cost_per_unit,
        })

    # Apply sells (FIFO: oldest lot first)
    sell_events = list(sells[['trade_date', 'units']].itertuples(index=False, name=None))

    lot_ptr = 0  # Index of oldest not-fully-depleted lot
    for sell_date, sell_units_raw in sell_events:
        remaining_to_sell = abs(sell_units_raw)

        i = lot_ptr
        while remaining_to_sell > 0 and i < len(lots):
            lot = lots[i]
            if lot['acquisition_date'] > sell_date:
                break  # Selling a lot that doesn't exist yet — data anomaly, skip
            consumed = min(lot['remaining_units'], remaining_to_sell)
            lot['remaining_units'] -= consumed
            remaining_to_sell -= consumed
            if lot['remaining_units'] <= 1e-8:
                lot['remaining_units'] = 0.0
                lot_ptr = i + 1  # This lot is fully consumed
            i += 1

    return lots


def build_holdings_lots_snapshot(
        transactions: pd.DataFrame,
        latest_prices: pd.DataFrame,
        accounts_dim: pd.DataFrame,
        snapshot_date: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    """
    Build holdings lots snapshot for all open positions.

    Args:
        transactions:  All transactions (source of truth for positions)
        latest_prices: Latest canonical price per asset
        accounts_dim:  Accounts dimension (tax_status, qualified_flag, relationship_id, etc.)
        snapshot_date: Date for this snapshot (default: today)

    Returns:
        DataFrame with lot-level rows, enriched with account tax metadata.
    """
    if snapshot_date is None:
        snapshot_date = pd.Timestamp.now().normalize()

    print(f"\n=== Building holdings lots snapshot for {snapshot_date.date()} ===")

    type_col = 'transaction_type' if 'transaction_type' in transactions.columns else 'action'
    sub_col = 'transaction_sub_type' if 'transaction_sub_type' in transactions.columns else None

    # Filter to transactions on or before snapshot date
    txn = transactions[transactions['trade_date'] <= snapshot_date].copy()

    # Classify unit-changing transactions: standard buy/sell + Corporate Actions
    is_buy = txn[type_col].isin(BUY_TYPES)
    is_sell = txn[type_col].isin(SELL_TYPES)
    is_ca = txn[type_col] == 'Corporate Action'
    if sub_col and is_ca.any():
        is_ca_buy = is_ca & txn[sub_col].isin(CA_BUY_SUBTYPES)
        is_ca_sell = is_ca & txn[sub_col].isin(CA_SELL_SUBTYPES)
        n_ca = int(is_ca.sum())
        n_ca_buy = int(is_ca_buy.sum())
        n_ca_sell = int(is_ca_sell.sum())
        print(f"  Corporate Actions: {n_ca:,} total "
              f"(buy={n_ca_buy:,}, sell={n_ca_sell:,}, "
              f"unclassified={n_ca - n_ca_buy - n_ca_sell:,})")
    else:
        is_ca_buy = pd.Series(False, index=txn.index)
        is_ca_sell = pd.Series(False, index=txn.index)

    all_buy = is_buy | is_ca_buy
    all_sell = is_sell | is_ca_sell

    # Filter to unit-changing transactions with valid assets
    unit_mask = (all_buy | all_sell) & txn['asset_name'].notna() & (txn['units'] != 0)
    unit_txns = txn[unit_mask].copy()
    unit_txns['_is_buy'] = all_buy[unit_mask]

    groups = list(unit_txns.groupby(['account_id', 'asset_name'], sort=False))
    total = len(groups)
    print(f"  Processing {total:,} (account, asset) groups...")

    all_lots = []
    for i, ((account_id, asset_name), grp) in enumerate(groups):
        lots = build_lots_for_group(account_id, asset_name, grp)

        for lot in lots:
            # Only include lots with meaningful remaining units
            if lot['remaining_units'] < 1e-8:
                is_open = False
                lot['remaining_units'] = 0.0
            else:
                is_open = True

            holding_days = (snapshot_date - lot['acquisition_date']).days

            all_lots.append({
                'lot_id': (f"{account_id}:{asset_name}:"
                           f"{lot['lot_index']}:{lot['acquisition_date'].date()}"),
                'snapshot_date': snapshot_date,
                'account_id': account_id,
                'asset_name': asset_name,
                'acquisition_date': lot['acquisition_date'],
                'lot_index': lot['lot_index'],
                'original_units': lot['original_units'],
                'current_units': lot['remaining_units'],
                'cost_per_unit': lot['cost_per_unit'],
                'cost_basis': lot['remaining_units'] * lot['cost_per_unit'],
                'holding_period_days': holding_days,
                'term': 'short_term' if holding_days < SHORT_TERM_DAYS else 'long_term',
                'is_open': is_open,
            })

        if (i + 1) % 10000 == 0:
            print(f"    [{i+1:,}/{total:,}] {(i+1)/total*100:.0f}%")

    print(f"  Generated {len(all_lots):,} lots")

    if not all_lots:
        return pd.DataFrame()

    df = pd.DataFrame(all_lots)

    # Join latest prices
    df = df.merge(
        latest_prices[['asset_name', 'ticker', 'price', 'source']].rename(
            columns={'price': 'current_price', 'source': 'price_quality'}
        ),
        on='asset_name',
        how='left',
    )

    # Market value and accrued gain
    df['market_value'] = df['current_units'] * df['current_price']
    df['accrued_gain'] = df['market_value'].fillna(0.0) - df['cost_basis']

    # Enrich with account metadata (tax_status, qualified_flag, relationship_id, etc.)
    if not accounts_dim.empty:
        df = df.merge(accounts_dim, on='account_id', how='left')
    else:
        # Graceful degradation — populate with nulls so schema is consistent
        for col in ['relationship_id', 'account_name', 'account_type',
                    'account_registration_type', 'tax_status', 'qualified_flag']:
            df[col] = None

    # purchase_year — derived from acquisition_date; avoids repeated compute downstream
    df['purchase_year'] = df['acquisition_date'].dt.year.astype('Int64')

    # Column order
    cols = [
        'lot_id', 'snapshot_date',
        # Account context
        'account_id', 'relationship_id', 'account_name',
        'account_type', 'account_registration_type',
        'tax_status', 'qualified_flag',
        # Position identity
        'asset_name', 'ticker',
        # Lot detail
        'acquisition_date', 'purchase_year', 'lot_index',
        'original_units', 'current_units',
        'cost_per_unit', 'cost_basis',
        'current_price', 'market_value', 'accrued_gain',
        'holding_period_days', 'term', 'is_open', 'price_quality',
    ]
    df = df[[c for c in cols if c in df.columns]]
    df = df.sort_values(['account_id', 'asset_name', 'lot_index']).reset_index(drop=True)

    # Summary
    open_lots = df[df['is_open']]
    print(f"\n  Open lots:          {len(open_lots):,}")
    print(f"  Unique positions:   {open_lots.groupby(['account_id', 'asset_name']).ngroups:,}")
    print(f"  Total market value: ${open_lots['market_value'].sum():,.0f}")
    print(f"  Total cost basis:   ${open_lots['cost_basis'].sum():,.0f}")
    print(f"  Accrued gain:       ${open_lots['accrued_gain'].sum():,.0f}")
    if 'tax_status' in open_lots.columns:
        print(f"\n  By tax_status:")
        for ts, grp in open_lots.groupby('tax_status', dropna=False):
            mv = grp['market_value'].sum()
            print(f"    {str(ts):<14}  {len(grp):>8,} lots  MV=${mv:>12,.0f}")
    print(f"\n  By term:")
    for term, grp in open_lots.groupby('term'):
        mv = grp['market_value'].sum()
        gain = grp['accrued_gain'].sum()
        print(f"    {term:<12}  {len(grp):>8,} lots  "
              f"MV=${mv:>12,.0f}  Gain=${gain:>12,.0f}")

    return df


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_lots(df: pd.DataFrame, upload: bool = False, full: bool = False):
    """Save holdings lots to gold layer."""
    print("\n=== Saving holdings lots ===")

    snap_date = df['snapshot_date'].iloc[0].strftime('%Y-%m-%d')

    if full:
        output_key = f"gold/holdings_lots/backfill_{snap_date}.parquet"
    else:
        output_key = f"gold/holdings_lots/{snap_date}.parquet"

    local_path = Path(f'/tmp/holdings_lots_{snap_date}.parquet')
    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.2f} MB")

    if upload:
        s3.upload_file(str(local_path), S3_BUCKET, output_key)
        print(f"  ✓ s3://{S3_BUCKET}/{output_key}")
    else:
        print(f"  [DRY RUN] Would upload to: s3://{S3_BUCKET}/{output_key}")

    local_path.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Build Holdings Lots (FIFO lot tracking for tax)'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    parser.add_argument('--full', action='store_true',
                        help='Backfill mode (uses all history)')
    parser.add_argument('--date', type=str, default=None,
                        help='Snapshot date YYYY-MM-DD (default: today)')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD HOLDINGS LOTS")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    transactions = load_transactions()
    latest_prices = load_latest_prices()
    accounts_dim = load_accounts_dimension()

    snapshot_date = (pd.Timestamp(args.date) if args.date
                     else pd.Timestamp.now().normalize())

    print(f"\n  Snapshot date: {snapshot_date.date()}")

    lots = build_holdings_lots_snapshot(transactions, latest_prices, accounts_dim, snapshot_date)

    if len(lots) == 0:
        print("\nWARNING: No open lots found")
        return 0

    if not args.dry_run:
        save_lots(lots, upload=args.upload, full=args.full)

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(lots):,} lots | {lots['is_open'].sum():,} open")
    print(f"  Open AUA: ${lots[lots['is_open']]['market_value'].sum():,.0f}")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

### script-05b--account-performance-builder-l4-source.py

```
#!/usr/bin/env python3
"""
Build Account Performance -- Account-Level AUA + Flows Timeseries

Produces a daily account-level performance timeseries covering
2020-06-30 to present. This is the foundational account-grain table that
enables:

  - Advisor book drill-down: filter by architect/implementor -> group by
    relationship_id for household roll-up, or view account-level detail
  - Account-specific AUA growth tracking
  - Any higher-level aggregation (all advisor fields denormalized)

All advisor fields are denormalized into each row so the table is fully
self-contained without joining accounts_dimension at query time.

Data sources and their roles:
  gold/positions_cube/YYYY-MM-DD.parquet   -- units per (account, asset) per day
    NOTE: date is the FILENAME, not a column. Each partition has only three
    columns: account_id, asset_name, units. Date is injected from the filename
    at load time.

  silver/prices/canonical_prices.parquet  -- price per (asset_name, date)
    Joined on (asset_name, date). Prices not present today are forward-filled
    within each asset_name from the most recent known price and flagged as
    'carried_forward_05b'.

  gold/accounts_dimension_latest.parquet  -- account metadata
    Provides relationship_id, tax_status, and all advisor fields per account_id.
    Accounts absent from dimension default to 'taxable' tax_status.

  silver/transactions/  -- cash flow events (uniform daily partitions)
    Source for cum_inflows, cum_outflows, nna. Only NNA-relevant transaction
    types counted (Cash Deposit, Transfer In, Cash Withdrawal, Transfer Out).
    Cumulative flows computed via daily groupby + cumsum, reindexed to the
    full positions_cube date spine per account.

Output schema (grain: one row per date x account_id):
  date                      date
  account_id                str
  relationship_id           str    -- household key; 'acct_{account_id}' if unmapped
  architect                 str    -- lead advisor
  implementor               str    -- implementing advisor
  local_relationship        str    -- local relationship manager (local_ops in BD)
  manager                   str    -- portfolio manager
  investment_strategy_name  str    -- strategy label
  tax_status                str    -- taxable | tax_deferred | tax_exempt
  total_aua                 float  -- sum(units * price) for this account on this date
  cum_inflows               float  -- cumulative cash/transfer inflows since inception
  cum_outflows              float  -- cumulative cash/transfer outflows since inception
  nna                       float  -- cum_inflows - cum_outflows
  num_positions             int    -- distinct assets held on this date
  pct_priced                float  -- fraction of AUA with a direct canonical price

Verification:
  SUM(total_aua) on latest date must equal 05_client_performance SUM(total_aua)
  GROUP BY (date, relationship_id) SUM(total_aua) must match 05 row-for-row

Output: gold/account_performance.parquet

Performance:
  canonical_prices is pre-forward-filled once before the loop, making
  process_date_partition stateless. All 2,065 date partitions are then
  processed in parallel via ThreadPoolExecutor(max_workers=16).
  Expected runtime: ~5-8 min on r6i.xlarge (was ~30 min serial).
  Peak memory: ~4-5 GB (more concurrent S3 reads vs ~3.5 GB serial).

Usage:
    python 05b_build_account_performance.py --dry-run
    python 05b_build_account_performance.py --upload

Author: Data Scientist (Claude)
Date: 2026-02-25
"""

import argparse
import gc
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO

import pandas as pd
import numpy as np
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')
MAX_WORKERS = 64

# NNA-relevant transaction types (same as 05_build_client_performance)
INFLOW_TYPES  = frozenset({'Cash Deposit', 'Transfer In'})
OUTFLOW_TYPES = frozenset({'Cash Withdrawal', 'Transfer Out'})

# Price sources that count as "real" for pct_priced
REAL_PRICE_SOURCES = frozenset({
    'transaction_observed', 'yahoo_finance', 'linear_interpolation',
})

# Outlier cap per flow event -- same as 05 (neutralises z0818656451-style garbage)
FLOW_CAP = 50_000_000

# Advisor fields to denormalize from accounts_dimension
ADVISOR_FIELDS = [
    'architect',
    'implementor',
    'local_relationship',  # stored as local_ops in raw data, renamed in accounts_dimension
    'manager',
    'investment_strategy_name',
]


def _read_parquet_from_s3(key: str) -> pd.DataFrame:
    """Read a single parquet file from S3. Thread-safe."""
    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(resp['Body'].read()))


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def list_positions_cube_keys() -> list:
    """List all positions_cube partition keys sorted by date."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='gold/positions_cube/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])
    if not keys:
        raise RuntimeError(
            "No positions_cube partitions found. "
            "Run 02_build_positions_cube.py first."
        )
    return sorted(keys)


def load_canonical_prices(cube_dates: list[pd.Timestamp]) -> pd.DataFrame:
    """
    Load canonical prices and expand to a dense (asset_name, date) grid so
    every asset has a price for every positions_cube date.

    canonical_prices.parquet has no null prices (build_canonical_prices_v2
    fills every row via 4-tier hierarchy). But it may not have a row for
    every (asset, date) combination — e.g., if an asset was first seen on
    2023-01-15, it has rows from that date onward, but canonical_prices may
    be sparse on weekend dates or dates where bd-price-update didn't run.

    The old approach of ffill() within existing rows was a no-op because
    there were no nulls to fill. The fix: create a complete (asset, date)
    grid using the positions_cube dates, merge in known prices, then
    forward-fill to cover gaps. This makes process_date_partition truly
    stateless — every asset on every date has a price via simple lookup.
    """
    print("Loading canonical prices...", end=' ', flush=True)
    resp = s3.get_object(Bucket=S3_BUCKET,
                         Key='silver/prices/canonical_prices.parquet')
    prices = pd.read_parquet(BytesIO(resp['Body'].read()))
    prices['date'] = pd.to_datetime(prices['date'])
    prices = prices[['date', 'asset_name', 'price', 'source']].copy()
    n_raw = len(prices)
    n_assets = prices['asset_name'].nunique()
    print(f"{n_raw:,} rows | {n_assets:,} assets")

    # Build a dense grid: every asset x every positions_cube date
    # Only include dates >= each asset's first appearance in canonical_prices
    print("  Expanding to dense (asset, date) grid...", end=' ', flush=True)
    all_assets = prices['asset_name'].unique()
    cube_dates_idx = pd.DatetimeIndex(sorted(set(cube_dates)))

    # Per-asset first date — don't create rows before the asset existed
    asset_first = prices.groupby('asset_name')['date'].min()

    # Build grid efficiently: for each asset, include cube_dates >= first_date
    grid_parts = []
    for asset, first_dt in asset_first.items():
        asset_dates = cube_dates_idx[cube_dates_idx >= first_dt]
        if len(asset_dates) > 0:
            grid_parts.append(pd.DataFrame({
                'asset_name': asset,
                'date': asset_dates,
            }))

    if not grid_parts:
        print("WARNING: empty grid")
        return prices

    grid = pd.concat(grid_parts, ignore_index=True)
    del grid_parts
    print(f"{len(grid):,} cells")

    # Merge known prices into the grid
    dense = grid.merge(prices, on=['asset_name', 'date'], how='left')
    del grid

    # Forward-fill within each asset (sorted by date) — THIS now actually
    # fills gaps because the grid has rows for dates without canonical prices
    dense = dense.sort_values(['asset_name', 'date'])

    _had_price = dense['price'].notna()
    dense['price']  = dense.groupby('asset_name')['price'].ffill()
    dense['source'] = dense.groupby('asset_name')['source'].ffill()

    # Label newly-filled rows
    _newly_filled = ~_had_price & dense['price'].notna()
    dense.loc[_newly_filled, 'source'] = 'carried_forward_05b'

    # Drop rows still without a price (asset's first canonical date is after
    # its first positions_cube date — no price history to carry forward)
    n_unfilled = dense['price'].isna().sum()
    if n_unfilled > 0:
        print(f"  WARNING: {n_unfilled:,} cells with no price "
              f"(assets without any canonical price before their cube dates)")
    dense = dense.dropna(subset=['price'])

    n_filled = int(_newly_filled.sum())
    print(f"  Dense prices: {len(dense):,} rows "
          f"({n_filled:,} carry-forward rows created, "
          f"{n_raw:,} original canonical rows)")
    return dense


def load_accounts_dimension() -> pd.DataFrame:
    """
    Load accounts dimension for account-level metadata.

    Returns account_id, relationship_id, tax_status, and all advisor fields.
    Accounts absent from dimension will get defaults at processing time.
    """
    print("Loading accounts dimension...", end=' ', flush=True)
    try:
        resp = s3.get_object(Bucket=S3_BUCKET,
                             Key='gold/accounts_dimension_latest.parquet')
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        print(f"{len(df):,} accounts")
        # Collect all useful columns -- advisor fields may be missing in older builds
        keep = ['account_id', 'relationship_id', 'tax_status'] + ADVISOR_FIELDS
        available = [c for c in keep if c in df.columns]
        missing = set(keep) - set(available)
        if missing:
            print(f"  NOTE: accounts_dimension missing columns (will default to empty): "
                  f"{sorted(missing)}")
        return df[available].drop_duplicates(subset=['account_id'])
    except Exception as e:
        raise RuntimeError(
            f"accounts_dimension not found ({e}). "
            "Run 00_build_accounts_dimension.py --upload first."
        )


def load_flows_from_transactions() -> pd.DataFrame:
    """
    Compute daily NNA-relevant cash flows per (date, account_id) from transactions.

    Returns DataFrame: date, account_id, daily_inflow, daily_outflow

    Only Cash Deposit, Transfer In (inflows) and Cash Withdrawal, Transfer Out
    (outflows) are counted. All other transaction types are excluded from NNA.

    Identical logic to 05_build_client_performance.load_flows_from_transactions()
    except the result is kept at account grain (not yet joined to relationships).
    """
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading transactions for flows (parallel)... ", end='', flush=True)

    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='silver/transactions/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])

    if not keys:
        raise RuntimeError("No transaction data found in silver layer.")

    t0 = datetime.now(timezone.utc)
    dfs = [None] * len(keys)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_read_parquet_from_s3, k): i for i, k in enumerate(keys)}
        done = 0
        for future in as_completed(futures):
            dfs[futures[future]] = future.result()
            done += 1
            if done % 500 == 0:
                print(f"[{done:,}/{len(keys):,}]", end=' ', flush=True)

    txns = pd.concat(dfs, ignore_index=True)
    del dfs; gc.collect()
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
    print(f"loaded in {elapsed:.1f}s")

    if 'transaction_id' in txns.columns:
        txns = txns.drop_duplicates(subset=['transaction_id'], keep='last')

    txns['trade_date'] = pd.to_datetime(txns['trade_date'], errors='coerce')
    txns = txns.dropna(subset=['trade_date', 'account_id', 'market_value'])

    type_col = 'transaction_type' if 'transaction_type' in txns.columns else 'action'

    # Second-pass composite dedup (catches sign-flipped duplicates with different IDs)
    txns['_mv_abs'] = txns['market_value'].abs()
    before = len(txns)
    txns = txns.drop_duplicates(
        subset=['account_id', 'trade_date', type_col, '_mv_abs'], keep='last'
    )
    txns = txns.drop(columns=['_mv_abs'])
    removed = before - len(txns)
    if removed > 0:
        print(f"  WARNING: {removed:,} rows removed by composite dedup")

    is_inflow  = txns[type_col].isin(INFLOW_TYPES)
    is_outflow = txns[type_col].isin(OUTFLOW_TYPES)
    flow_mask  = is_inflow | is_outflow
    flows = txns[flow_mask].copy()

    flows['daily_inflow']  = np.where(is_inflow[flow_mask],  flows['market_value'].abs(), 0.0)
    flows['daily_outflow'] = np.where(is_outflow[flow_mask], flows['market_value'].abs(), 0.0)

    _in_total  = flows['daily_inflow'].sum()
    _out_total = flows['daily_outflow'].sum()
    print(f"\n  Flow classification:")
    print(f"    Inflow  events: {is_inflow[flow_mask].sum():>8,}   raw total: ${_in_total:>16,.0f}")
    print(f"    Outflow events: {is_outflow[flow_mask].sum():>8,}   raw total: ${_out_total:>16,.0f}")
    print(f"    Implied NNA:    ${_in_total - _out_total:>16,.0f}")

    # Outlier cap -- same $50M threshold as 05
    n_capped_in  = (flows['daily_inflow']  > FLOW_CAP).sum()
    n_capped_out = (flows['daily_outflow'] > FLOW_CAP).sum()
    if n_capped_in > 0 or n_capped_out > 0:
        flows['daily_inflow']  = flows['daily_inflow'].clip(upper=FLOW_CAP)
        flows['daily_outflow'] = flows['daily_outflow'].clip(upper=FLOW_CAP)
        print(f"  OUTLIER GUARD: capped {n_capped_in} inflows and "
              f"{n_capped_out} outflows at ${FLOW_CAP:,.0f}")

    daily = flows.groupby(
        ['trade_date', 'account_id'], sort=True
    ).agg(
        daily_inflow=('daily_inflow',  'sum'),
        daily_outflow=('daily_outflow', 'sum'),
    ).reset_index().rename(columns={'trade_date': 'date'})

    print(f"  {len(txns):,} transactions -> {len(daily):,} account x date flow events")
    return daily


# ---------------------------------------------------------------------------
# Core builder -- partition-by-date processing
# ---------------------------------------------------------------------------

def process_date_partition(
    key: str,
    prices_day: pd.DataFrame,
    accounts: pd.DataFrame,
) -> pd.DataFrame:
    """
    Process one date's positions_cube partition and return AUA per (date, account_id).

    Stateless: prices_day is already forward-filled by load_canonical_prices(),
    so no mutable last_prices dict is needed. Safe to call concurrently from
    multiple threads.

    Returns daily_agg_df (empty DataFrame if partition has no rows).
    """
    date_str = key.split('/')[-1].replace('.parquet', '')
    date = pd.Timestamp(date_str)

    resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
    pos = pd.read_parquet(BytesIO(resp['Body'].read()))

    if pos.empty:
        return pd.DataFrame()

    # Vectorized price join — prices_day is pre-forward-filled so a simple
    # left merge covers all assets; remaining NaN (assets with no price history
    # at all) fall back to 0.
    if not prices_day.empty:
        pos = pos.merge(
            prices_day[['asset_name', 'price', 'source']],
            on='asset_name',
            how='left',
        )
    else:
        pos['price']  = np.nan
        pos['source'] = None

    pos['price'] = pos['price'].fillna(0.0)

    # Vectorized priced-AUA flag — avoids closure over pos inside groupby lambda
    pos['market_value'] = pos['units'] * pos['price']
    pos['priced_mv']    = pos['market_value'].where(
        pos['source'].isin(REAL_PRICE_SOURCES), 0.0
    )

    # Join accounts dimension — brings in relationship_id, tax_status, advisor fields
    pos = pos.merge(accounts, on='account_id', how='left')

    no_rel = pos['relationship_id'].isna() | (pos['relationship_id'] == '')
    pos.loc[no_rel, 'relationship_id'] = 'acct_' + pos.loc[no_rel, 'account_id']

    if 'tax_status' not in pos.columns:
        pos['tax_status'] = 'taxable'
    pos['tax_status'] = pos['tax_status'].fillna('taxable')

    for field in ADVISOR_FIELDS:
        if field not in pos.columns:
            pos[field] = ''
        else:
            pos[field] = pos[field].fillna('')

    # Per-account metadata (1:1 with account_id — take first row per account)
    meta_cols = ['relationship_id', 'tax_status'] + ADVISOR_FIELDS
    meta_cols_present = [c for c in meta_cols if c in pos.columns]
    meta = (pos.groupby('account_id')[meta_cols_present]
            .first()
            .reset_index())

    # Aggregate AUA metrics — fully vectorized, no closures over outer scope
    agg = pos.groupby('account_id').agg(
        total_aua=('market_value', 'sum'),
        num_positions=('asset_name', 'nunique'),
        priced_aua=('priced_mv', 'sum'),
    ).reset_index()

    agg['pct_priced'] = np.where(
        agg['total_aua'] > 0,
        agg['priced_aua'] / agg['total_aua'],
        1.0,
    )
    agg = agg.drop(columns=['priced_aua'])

    agg = agg.merge(meta, on='account_id', how='left')
    agg['date'] = date
    return agg


def build_account_performance(
        cube_keys: list,
        prices:    pd.DataFrame,
        accounts:  pd.DataFrame,
        flows:     pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the account-level daily AUA + flows timeseries.

    Partitions are processed concurrently with ThreadPoolExecutor (16 workers).
    process_date_partition is stateless — prices are pre-forward-filled by
    load_canonical_prices(), so workers share no mutable state.

    Memory: ~4-5 GB peak (more concurrent S3 reads in flight vs ~3.5 GB serial).
    Runtime: ~5-8 min on r6i.xlarge vs ~30 min for the serial version.
    """
    print("\n=== Building account performance ===")

    # Index pre-filled prices by date for O(1) per-partition lookup
    print("  Indexing prices by date...")
    prices_by_date = {d: g for d, g in prices.groupby('date')}
    print(f"  {len(prices_by_date):,} dates in canonical_prices")

    if 'tax_status' not in accounts.columns:
        accounts = accounts.copy()
        accounts['tax_status'] = 'taxable'

    n_total = len(cube_keys)
    print(f"  Processing {n_total:,} date partitions (16 parallel workers)...")

    # Build (future -> index) map so results can be ordered correctly
    daily_aggs = []
    done = 0

    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {}
        for i, key in enumerate(cube_keys):
            date = pd.Timestamp(key.split('/')[-1].replace('.parquet', ''))
            prices_day = prices_by_date.get(date, pd.DataFrame())
            futures[pool.submit(process_date_partition, key, prices_day, accounts)] = i

        for future in as_completed(futures):
            agg = future.result()
            if not agg.empty:
                daily_aggs.append(agg)
            done += 1
            if done % 200 == 0 or done == n_total:
                print(f"    [{done}/{n_total}] complete  "
                      f"({len(daily_aggs):,} partitions with data)")

    print(f"  Partition processing complete: {len(daily_aggs):,} days")

    agg_all = pd.concat(daily_aggs, ignore_index=True)
    del daily_aggs; gc.collect()

    # ------------------------------------------------------------------
    # Build cumulative flows per (date, account_id)
    # ------------------------------------------------------------------
    print("  Building cumulative flows...")

    # Build full date x account spine so cumsum covers every day each account existed
    all_dates = agg_all[['date', 'account_id']].drop_duplicates()
    flow_spine = all_dates.merge(flows, on=['date', 'account_id'], how='left')
    flow_spine['daily_inflow']  = flow_spine['daily_inflow'].fillna(0.0)
    flow_spine['daily_outflow'] = flow_spine['daily_outflow'].fillna(0.0)

    flow_spine = flow_spine.sort_values(['account_id', 'date'])
    flow_spine['cum_inflows']  = (flow_spine
                                  .groupby('account_id')['daily_inflow']
                                  .cumsum())
    flow_spine['cum_outflows'] = (flow_spine
                                  .groupby('account_id')['daily_outflow']
                                  .cumsum())
    flow_spine['nna'] = flow_spine['cum_inflows'] - flow_spine['cum_outflows']

    # ------------------------------------------------------------------
    # Join flows to AUA timeseries
    # ------------------------------------------------------------------
    result = agg_all.merge(
        flow_spine[['date', 'account_id', 'cum_inflows', 'cum_outflows', 'nna']],
        on=['date', 'account_id'],
        how='left',
    )
    for col in ['cum_inflows', 'cum_outflows', 'nna']:
        result[col] = result[col].fillna(0.0)

    # Final column order
    final_cols = [
        'date', 'account_id',
        'relationship_id',
        'architect', 'implementor', 'local_relationship',
        'manager', 'investment_strategy_name',
        'tax_status',
        'total_aua',
        'cum_inflows', 'cum_outflows', 'nna',
        'num_positions',
        'pct_priced',
    ]
    result = result[[c for c in final_cols if c in result.columns]]
    result = result.sort_values(['date', 'account_id']).reset_index(drop=True)

    # Summary
    latest_date = result['date'].max()
    latest = result[result['date'] == latest_date]
    total_aua = latest['total_aua'].sum()

    print(f"\n  Date range:    {result['date'].min().date()} -> {latest_date.date()}")
    print(f"  Total rows:    {len(result):,}")
    print(f"  Accounts:      {result['account_id'].nunique():,}")
    print(f"  Relationships: {result['relationship_id'].nunique():,}")
    print(f"\n  As of {latest_date.date()}:")
    print(f"    Total AUA:     ${total_aua:>16,.0f}")
    print(f"    Cum NNA:       ${latest['nna'].sum():>16,.0f}")
    print(f"    Pct priced:    {latest['pct_priced'].mean()*100:>15.1f}%")
    print(f"    Active accounts: {len(latest):,}")

    # Advisor book summary
    if 'architect' in latest.columns:
        print(f"\n  By architect (top 8 by AUA):")
        arch_agg = (latest.groupby('architect')['total_aua'].sum()
                    .sort_values(ascending=False).head(8))
        for arch, aua in arch_agg.items():
            pct = aua / total_aua * 100 if total_aua > 0 else 0
            n_accts = (latest['architect'] == arch).sum()
            print(f"    {arch:<30}  ${aua:>16,.0f}  ({pct:4.1f}%)  {n_accts} accounts")

    return result


# ---------------------------------------------------------------------------
# Cross-validation against 05
# ---------------------------------------------------------------------------

def cross_validate_vs_client_performance(result: pd.DataFrame) -> bool:
    """
    Verify that SUM(total_aua) on the latest date matches 05_client_performance.

    Returns True if validation passes (within 0.1% tolerance), False otherwise.
    """
    print("\n=== Cross-validating against client_performance (05) ===")
    try:
        resp = s3.get_object(Bucket=S3_BUCKET, Key='gold/client_performance.parquet')
        perf05 = pd.read_parquet(BytesIO(resp['Body'].read()))
        perf05['date'] = pd.to_datetime(perf05['date'])
    except Exception as e:
        print(f"  SKIP: client_performance not accessible ({e})")
        return True

    latest_date = result['date'].max()
    aua_05b = result[result['date'] == latest_date]['total_aua'].sum()

    perf05_latest = perf05[perf05['date'] == latest_date]
    if perf05_latest.empty:
        print(f"  SKIP: client_performance has no rows for {latest_date.date()}")
        return True
    aua_05 = perf05_latest['total_aua'].sum()

    diff = abs(aua_05b - aua_05)
    pct_diff = diff / aua_05 * 100 if aua_05 > 0 else 0

    print(f"  05_client_performance AUA: ${aua_05:>16,.0f}")
    print(f"  05b_account_performance AUA: ${aua_05b:>16,.0f}")
    print(f"  Difference: ${diff:>16,.0f} ({pct_diff:.4f}%)")

    if pct_diff > 0.1:
        print(f"  FAIL: AUA difference exceeds 0.1% tolerance")
        return False

    print(f"  PASS: AUA cross-check within tolerance")

    # NNA check
    nna_05b = result[result['date'] == latest_date]['nna'].sum()
    nna_05  = perf05_latest['nna'].sum()
    nna_diff_pct = abs(nna_05b - nna_05) / abs(nna_05) * 100 if nna_05 != 0 else 0
    print(f"  NNA 05:  ${nna_05:>16,.0f}")
    print(f"  NNA 05b: ${nna_05b:>16,.0f}  ({nna_diff_pct:.4f}% diff)")
    if nna_diff_pct > 0.1:
        print(f"  WARN: NNA difference exceeds 0.1% -- investigate flow dedup")
    else:
        print(f"  PASS: NNA cross-check within tolerance")

    return True


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_performance(df: pd.DataFrame, upload: bool = False):
    """Save account performance to gold layer."""
    print("\n=== Saving account performance ===")

    output_key = 'gold/account_performance.parquet'
    local_path = Path('/tmp/account_performance.parquet')

    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.1f} MB")

    if upload:
        s3.upload_file(str(local_path), S3_BUCKET, output_key)
        print(f"  OK: s3://{S3_BUCKET}/{output_key}")
    else:
        print(f"  [DRY RUN] Would upload to: s3://{S3_BUCKET}/{output_key}")

    local_path.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Build Account Performance')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD ACCOUNT PERFORMANCE")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load source data ===")
    cube_keys = list_positions_cube_keys()
    print(f"Positions cube: {len(cube_keys):,} date partitions")

    # Extract dates from cube keys for dense price grid construction
    cube_dates = [
        pd.Timestamp(k.split('/')[-1].replace('.parquet', ''))
        for k in cube_keys
    ]

    prices   = load_canonical_prices(cube_dates)
    accounts = load_accounts_dimension()
    flows    = load_flows_from_transactions()

    print("\n=== Step 2: Build account performance timeseries ===")
    perf = build_account_performance(cube_keys, prices, accounts, flows)

    print("\n=== Step 3: Cross-validate ===")
    cross_validate_vs_client_performance(perf)

    print("\n=== Step 4: Save ===")
    save_performance(perf, upload=args.upload and not args.dry_run)

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(perf):,} account x date rows")
    print(f"  {perf['account_id'].nunique():,} accounts")
    print(f"  {perf['relationship_id'].nunique():,} relationships")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

### script-06--client-tax-liability-builder-l4-source.py

```
#!/usr/bin/env python3
"""
Build Client Tax Liability View

Aggregates gold/holdings_lots to the position × purchase_year grain, producing
an advisor-intelligence view for tax planning conversations:

  - Qualified (tax_deferred / tax_exempt) vs non-qualified (taxable) split per client
  - For non-qualified accounts: FIFO cost basis + purchase year by asset and term
  - Short-term vs long-term capital gain breakdown at every level
  - Supports drill-down: household → account → asset → purchase_year

Yang's requirements addressed:
  1. Split of qualified vs non-qualified per client     → qualified_flag, tax_status columns
  2. Cost basis by asset, based on aggregated position  → total_cost_basis per position row
  3. Cost basis by asset, based on tax lot              → query holdings_lots directly (lot grain)
  4. Purchase year for both grains                      → purchase_year column

Grain: one row per (relationship_id, account_id, asset_name, purchase_year)
       This is the "aggregated position" level Yang requested.
       For lot-level detail, query gold/holdings_lots/ directly.

Schema:
  relationship_id            str
  relationship_name          str   (from accounts_dimension via timeline)
  account_id                 str
  account_name               str
  account_type               str   — 'IRA' | 'RothIRA' | 'Brokerage' | 'Joint' | etc.
  account_registration_type  str   — 'Contributory IRA' | 'Individual' | etc.
  tax_status                 str   — 'taxable' | 'tax_deferred' | 'tax_exempt'
  qualified_flag             bool  — False = taxable (non-qualified); True = retirement account
  asset_name                 str
  ticker                     str
  purchase_year              int   — year(acquisition_date) — cohort for tax planning
  num_open_lots              int   — number of open FIFO lots in this cohort
  total_units                float
  total_cost_basis           float — FIFO cost basis; meaningful for taxable accounts
  total_market_value         float
  total_accrued_gain         float — unrealized gain; taxable on sale for taxable accounts
  short_term_lots            int
  short_term_units           float
  short_term_cost_basis      float — held < 365 days → taxed at ordinary income rates
  short_term_market_value    float
  short_term_gain            float
  long_term_lots             int
  long_term_units            float
  long_term_cost_basis       float — held ≥ 365 days → taxed at preferential LTCG rates
  long_term_market_value     float
  long_term_gain             float
  snapshot_date              date

Input:
  - gold/holdings_lots/YYYY-MM-DD.parquet  (latest snapshot, built by 03_build_holdings_lots.py)

Output:
  - gold/views/client_tax_liability.parquet

Usage:
    python 06_build_client_tax_liability.py --dry-run
    python 06_build_client_tax_liability.py --upload

Author: Data Scientist (Claude)
Date: 2026-02-20
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO

import pandas as pd
import numpy as np
import boto3

S3_BUCKET = 'opal-data-bd'
s3 = boto3.client('s3', region_name='us-east-1')


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_latest_holdings_lots() -> pd.DataFrame:
    """Load the most recent holdings_lots snapshot from gold layer."""
    paginator = s3.get_paginator('list_objects_v2')
    print("Loading holdings lots...", end=' ', flush=True)

    keys = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='gold/holdings_lots/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.parquet'):
                keys.append(obj['Key'])

    if not keys:
        raise RuntimeError(
            "No holdings_lots snapshots found. "
            "Run 03_build_holdings_lots.py --upload first."
        )

    latest_key = sorted(keys)[-1]
    print(f"latest: {latest_key}...", end=' ', flush=True)
    resp = s3.get_object(Bucket=S3_BUCKET, Key=latest_key)
    df = pd.read_parquet(BytesIO(resp['Body'].read()))
    print(f"{len(df):,} lots")
    return df


# ---------------------------------------------------------------------------
# Build view
# ---------------------------------------------------------------------------

def build_tax_liability_view(lots: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate open holdings lots to the position × purchase_year grain.

    One row per (relationship_id, account_id, asset_name, purchase_year).
    Includes both all-accounts and per-term (short/long) breakdowns.
    """
    print("\n=== Building client tax liability view ===")

    # Work with open lots only — forward-looking tax liability
    open_lots = lots[lots['is_open']].copy()
    print(f"  Open lots: {len(open_lots):,} of {len(lots):,} total")

    if open_lots.empty:
        raise RuntimeError("No open lots found — run 03_build_holdings_lots.py first.")

    # Ensure required columns exist (graceful if accounts_dim wasn't available)
    for col, default in [
        ('relationship_id',           None),
        ('account_name',              ''),
        ('account_type',              ''),
        ('account_registration_type', ''),
        ('tax_status',                'taxable'),
        ('qualified_flag',            False),
        ('purchase_year',             open_lots['acquisition_date'].dt.year if 'acquisition_date' in open_lots.columns else 0),
    ]:
        if col not in open_lots.columns:
            open_lots[col] = default

    snapshot_date = open_lots['snapshot_date'].iloc[0]

    # ---------- helpers for conditional aggregation ----------
    def agg_term(df, term):
        """Aggregate lots for a specific term (short_term / long_term)."""
        sub = df[df['term'] == term]
        return sub.agg(
            lots=('lot_id', 'count'),
            units=('current_units', 'sum'),
            cost_basis=('cost_basis', 'sum'),
            market_value=('market_value', 'sum'),
            gain=('accrued_gain', 'sum'),
        )

    # ---------- group by position × purchase_year ----------
    group_keys = [
        'relationship_id', 'account_id', 'account_name',
        'account_type', 'account_registration_type',
        'tax_status', 'qualified_flag',
        'asset_name', 'ticker',
        'purchase_year',
    ]
    # Drop group keys that are missing entirely
    group_keys = [k for k in group_keys if k in open_lots.columns]

    print(f"  Grouping by: {group_keys}")

    grouped = open_lots.groupby(group_keys, dropna=False)

    # Total aggregation
    totals = grouped.agg(
        num_open_lots=('lot_id', 'count'),
        total_units=('current_units', 'sum'),
        total_cost_basis=('cost_basis', 'sum'),
        total_market_value=('market_value', 'sum'),
        total_accrued_gain=('accrued_gain', 'sum'),
    ).reset_index()

    # Short-term aggregation
    st = (open_lots[open_lots['term'] == 'short_term']
          .groupby(group_keys, dropna=False)
          .agg(
              short_term_lots=('lot_id', 'count'),
              short_term_units=('current_units', 'sum'),
              short_term_cost_basis=('cost_basis', 'sum'),
              short_term_market_value=('market_value', 'sum'),
              short_term_gain=('accrued_gain', 'sum'),
          ).reset_index())

    # Long-term aggregation
    lt = (open_lots[open_lots['term'] == 'long_term']
          .groupby(group_keys, dropna=False)
          .agg(
              long_term_lots=('lot_id', 'count'),
              long_term_units=('current_units', 'sum'),
              long_term_cost_basis=('cost_basis', 'sum'),
              long_term_market_value=('market_value', 'sum'),
              long_term_gain=('accrued_gain', 'sum'),
          ).reset_index())

    # Join all three aggregations
    result = totals.merge(st, on=group_keys, how='left')
    result = result.merge(lt, on=group_keys, how='left')

    # Fill NaN for positions with no short-term or long-term lots
    st_cols = ['short_term_lots', 'short_term_units', 'short_term_cost_basis',
               'short_term_market_value', 'short_term_gain']
    lt_cols = ['long_term_lots', 'long_term_units', 'long_term_cost_basis',
               'long_term_market_value', 'long_term_gain']
    for col in st_cols + lt_cols:
        if col in result.columns:
            result[col] = result[col].fillna(0.0)
    for col in ['short_term_lots', 'long_term_lots']:
        if col in result.columns:
            result[col] = result[col].fillna(0).astype(int)

    result['snapshot_date'] = snapshot_date

    # Final column order
    final_cols = [
        'relationship_id', 'account_id', 'account_name',
        'account_type', 'account_registration_type',
        'tax_status', 'qualified_flag',
        'asset_name', 'ticker',
        'purchase_year',
        'num_open_lots',
        'total_units', 'total_cost_basis', 'total_market_value', 'total_accrued_gain',
        'short_term_lots', 'short_term_units', 'short_term_cost_basis',
        'short_term_market_value', 'short_term_gain',
        'long_term_lots', 'long_term_units', 'long_term_cost_basis',
        'long_term_market_value', 'long_term_gain',
        'snapshot_date',
    ]
    result = result[[c for c in final_cols if c in result.columns]]
    result = result.sort_values(
        ['relationship_id', 'account_id', 'asset_name', 'purchase_year'],
        na_position='last',
    ).reset_index(drop=True)

    # Summary
    print(f"\n  Rows (position × purchase_year): {len(result):,}")
    print(f"  Unique relationships: {result['relationship_id'].nunique():,}")
    print(f"  Unique accounts:      {result['account_id'].nunique():,}")
    print(f"  Unique assets:        {result['asset_name'].nunique():,}")
    if 'tax_status' in result.columns:
        print(f"\n  By tax_status:")
        for ts, grp in result.groupby('tax_status', dropna=False):
            mv = grp['total_market_value'].sum()
            gain = grp['total_accrued_gain'].sum()
            print(f"    {str(ts):<14}  {len(grp):>8,} positions  "
                  f"MV=${mv:>14,.0f}  Accrued Gain=${gain:>12,.0f}")
    print(f"\n  Non-qualified (taxable) breakdown by term:")
    taxable = result[result['tax_status'] == 'taxable'] if 'tax_status' in result.columns else result
    for label, cb_col, gain_col in [
        ('Short-term', 'short_term_cost_basis', 'short_term_gain'),
        ('Long-term',  'long_term_cost_basis',  'long_term_gain'),
    ]:
        if cb_col in taxable.columns:
            cb = taxable[cb_col].sum()
            gain = taxable[gain_col].sum()
            print(f"    {label:<12}  Cost Basis=${cb:>14,.0f}  Gain=${gain:>12,.0f}")

    return result


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_view(df: pd.DataFrame, upload: bool = False):
    """Save client tax liability view to gold/views/."""
    print("\n=== Saving client tax liability view ===")

    output_key = 'gold/views/client_tax_liability.parquet'
    local_path = Path('/tmp/client_tax_liability.parquet')

    df.to_parquet(local_path, index=False, engine='pyarrow', compression='snappy')
    size_mb = local_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.2f} MB")

    if upload:
        s3.upload_file(str(local_path), S3_BUCKET, output_key)
        print(f"  ✓ s3://{S3_BUCKET}/{output_key}")
    else:
        print(f"  [DRY RUN] Would upload to: s3://{S3_BUCKET}/{output_key}")

    local_path.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Build Client Tax Liability View (position × purchase_year grain)'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show stats, no upload')
    parser.add_argument('--upload', action='store_true',
                        help='Upload to S3')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD CLIENT TAX LIABILITY VIEW")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    print("\n=== Step 1: Load holdings lots ===")
    lots = load_latest_holdings_lots()

    print("\n=== Step 2: Build view ===")
    view = build_tax_liability_view(lots)

    print("\n=== Step 3: Save ===")
    if not args.dry_run:
        save_view(view, upload=args.upload)
    else:
        print("  [DRY RUN] Skipping save")

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  {len(view):,} rows (position × purchase_year grain)")
    print(f"  Snapshot: {view['snapshot_date'].iloc[0].date() if len(view) else 'n/a'}")
    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

---

## Participant Background

### 0.4.0_DS_ClientPlatform -- Pending Task Orders

#### advisor_intelligence_completion.md

# Task Order: AdvisorIntelligence Data Completion — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-ds-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement all data-layer additions for AdvisorIntelligence completion. Streams A1, A2,
    and A3 require Pattern 0 alignment threads to run FIRST — the thread receipts define
    the exact JSON shapes and TypeScript interfaces DS must implement. Do NOT implement
    A1/A2/A3 based on this task order's descriptions alone; the thread receipt is the
    binding specification. Streams A4 and A5 have no interface dependency and start
    immediately. Stream E is blocked by the Books tab design thread (Stream D).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref type="data-contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py</file>
      <file action="verify">data/black_diamond/scripts/gold/09_build_distribution_stats.py</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM A4 — Snapshot NNA bell curve math verification            -->
    <!-- UNBLOCKED — start immediately, no interface dependency           -->
    <!-- ================================================================ -->
    <requirement id="A4.1">
      Verify that commit 8247c6d0 correctly implemented |abs| for negative NNA accounts
      in script 09's bell curve percentile threshold calculation.
      Open partner_analytics/header_metrics.json from S3 and inspect the distribution
      field for the NNA view's outflow segment.
      Confirm P10/P25/Median/P75/P90 thresholds are non-degenerate: not all zero,
      not symmetric mirrors of the positive side.
    </requirement>
    <requirement id="A4.2">
      If the fix did NOT land: write a targeted patch to script 09 and coordinate with
      0.4.0_DT to deploy the EC2 script update.
      If the fix DID land: document the verification result in your session log with
      the specific threshold values observed in header_metrics.json.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A5 — opal-users-v2 advisor identity investigation         -->
    <!-- UNBLOCKED — start immediately, no interface dependency           -->
    <!-- ================================================================ -->
    <requirement id="A5.1">
      Investigate the schema of the opal-users-v2 DynamoDB table (read-only):
        - What fields identify an advisor (userId, email, advisorId, firmId)?
        - What is the partition key / sort key structure?
    </requirement>
    <requirement id="A5.2">
      Determine whether a mapping from opal-users-v2 identity fields to
      accounts_dimension_latest.architect or rel_architect_lookup.parquet already exists:
        (a) Direct field match
        (b) Email-based lookup
        (c) No existing mapping — new data registration step required
      Document findings in your session log. This is the linchpin for Books tab auth gating.
      If option (c): flag as a blocker and surface to COO and CTO before any auth work proceeds.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A1 — adv_drill in timeseries_chart.json                   -->
    <!-- BLOCKED: run Pattern 0 thread first                              -->
    <!-- Thread: org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A1.1">
      GATE: Do not implement adv_drill until the Pattern 0 alignment thread
      (2026-03-03-continuous-nna-cla-alignment) has completed and you have a receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      The thread receipt is the binding specification for the adv_drill JSON shape,
      S3 key pattern, cardinality constraints, and date range. Implement exactly what
      was agreed in the thread — not what is described in the PRD or this task order.
    </requirement>
    <requirement id="A1.2">
      In the thread, you are the knowledge source. Describe what per-architect and
      per-client NNA data currently exists in the gold layer. Name specific parquet
      files, column names, and cardinality. Let DE specify the TypeScript interface
      and RD specify the chart constraint — then converge on the exact shape.
    </requirement>
    <requirement id="A1.3">
      After thread completes: implement adv_drill in bd-portal-publisher/lambda_function.py
      per the agreed contract. Update data_contract.xml with the agreed shape, S3 key,
      and grain definitions BEFORE signaling DT to deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A2 — cla_timeseries in timeseries_chart.json              -->
    <!-- BLOCKED: run Pattern 0 thread first (same thread as A1)          -->
    <!-- Thread: org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A2.1">
      GATE: Same as A1 — do not implement cla_timeseries until the thread receipt from
      2026-03-03-continuous-nna-cla-alignment is in your threads/ folder.
      The thread defines: NMNC/NMEC classification logic (agreed with DE and RD),
      the exact JSON structure, grain definitions (total/geo/adv/geo_drill),
      and whether implementation lives in script 09 (EC2) or the publisher Lambda.
    </requirement>
    <requirement id="A2.2">
      In the thread, surface what NMNC/NMEC classification data currently exists in
      the gold layer. Do NOT assume the classification. Name the specific field or
      derivation logic and let all three agents agree on the definition in the thread.
      Do not commit any classification logic until DE has confirmed it matches how
      CLA is currently defined in header_metrics.json.
    </requirement>
    <requirement id="A2.3">
      After thread completes: implement cla_timeseries per the agreed contract.
      Update data_contract.xml BEFORE signaling DT to deploy.
      Note: adv_drill and cla_timeseries should deploy together in one publisher update
      (Stream B1) to minimize deploy events.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A3 — Stacked bar + 1Y rolling for Advisors tab            -->
    <!-- BLOCKED: run Pattern 0 thread first                              -->
    <!-- Thread: org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A3.1">
      GATE: Do not modify script 10 until the Pattern 0 alignment thread
      (2026-03-03-advisors-stacked-bar-alignment) has completed and you have a receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      The thread receipt defines: the exact output schema for advisor_rolling_flows.json,
      how outflows are encoded (sign convention vs separate field), what period-anchored
      aggregation is feasible given available history, and the TypeScript interface
      DE and RD agreed on.
    </requirement>
    <requirement id="A3.2">
      In the thread, describe what script 10 currently computes, what parquet columns
      carry inflows vs outflows vs net NNA, and what date history is available.
      Be specific about whether inflows and outflows are tracked separately in the
      source data or only as net NNA. Let DE and RD shape the output contract from
      what you describe as feasible.
    </requirement>
    <requirement id="A3.3">
      After thread completes: implement the agreed stacked_bar and rolling_1y output
      in script 10. Update data_contract.xml BEFORE signaling DT for Stream B2 deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM E — Books data contract audit (BLOCKED by Stream D)       -->
    <!-- ================================================================ -->
    <requirement id="E.1">
      BLOCKED: Do not begin Stream E until the Books design thread
      (2026-03-03-books-tab-design) completes and you have a receipt in your threads/ folder.
      In that thread, you are the knowledge source. Read the advisor-publisher Lambda and
      scripts 03, 05b, and 06 carefully. Describe precisely what each script produces
      and which of those outputs currently flow into the publisher vs remain gold-layer only.
    </requirement>
    <requirement id="E.2">
      After thread: produce a gap list (what L4 fields exist in gold but are absent from
      the publisher output). Add to data_contract.xml as a pending Books L4 section.
      Implement the publisher additions. Update data_contract.xml to complete status
      BEFORE signaling DT for Stream F deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">A4: Bell curve verification result in session log with actual threshold values; patch applied if needed.</criterion>
    <criterion id="2">A5: opal-users-v2 mapping findings documented in session log; option (c) flagged to COO if no mapping exists.</criterion>
    <criterion id="3">A1: adv_drill implemented per thread receipt; data_contract.xml updated; DT deploy confirmed.</criterion>
    <criterion id="4">A2: cla_timeseries implemented per thread receipt; classification logic agreed in thread; data_contract.xml updated.</criterion>
    <criterion id="5">A3: advisor_rolling_flows.json updated per thread receipt; data_contract.xml updated; DT deploy confirmed.</criterion>
    <criterion id="6">E: L4 publisher gap list produced and closed; data_contract.xml updated (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>A1, A2, A3 are BLOCKED until Pattern 0 thread receipts are in your threads/ folder. Do not implement from PRD descriptions alone — the thread contract supersedes the PRD's suggested shapes.</constraint>
    <constraint>data_contract.xml must be updated and committed BEFORE signaling DT to deploy any Lambda change. This is a non-negotiable quality gate.</constraint>
    <constraint>Do NOT deploy directly. Hand off to 0.4.0_DT via your session log next steps with the commit hash of your code change.</constraint>
    <constraint>Do NOT use emojis in any script, Lambda, or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>Start A4 and A5 in your first session. These have no thread dependency.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-continuous-nna-cla-alignment" status="pending" note="A1 and A2 blocked until thread receipt"/>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-advisors-stacked-bar-alignment" status="pending" note="A3 blocked until thread receipt"/>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-books-tab-design" status="pending" note="E blocked until thread receipt"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Script 09 verification result (and patch if needed)</deliverable>
    <deliverable type="document">Session log with A5 opal-users-v2 findings</deliverable>
    <deliverable type="commit">bd-portal-publisher/lambda_function.py: adv_drill + cla_timeseries per thread receipt (A1+A2)</deliverable>
    <deliverable type="commit">10_generate_advisor_rolling_flows.py: stacked_bar + rolling_1y per thread receipt (A3)</deliverable>
    <deliverable type="document">data_contract.xml updated for A1, A2, A3 (before each DT deploy)</deliverable>
    <deliverable type="document">data_contract.xml updated with Books L4 contract (post-thread, Stream E)</deliverable>
  </deliverables>
</task_order>
```


### 0.4.0_DS_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DS_ClientPlatform

076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context

### 0.4.2_RD_AdvisorIntelligence -- Pending Task Orders

#### advisor_intelligence_completion.md

# Task Order: AdvisorIntelligence Portal Completion — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-rd-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement all portal-layer changes for AdvisorIntelligence completion. Covers
    7 streams: Distribution tab continuous and snapshot views (C1-C4), Advisors tab
    UI refactor (H, I, 4C stacked bar), and Books tab implementation (G — blocked).
    Streams C1, C3, H, and I have no data dependencies and can start immediately.
    Streams C2 and C4 are blocked by DT deploying the updated publisher (Stream B1).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref>portal/src/pages/AdvisorIntelligence/</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Distribution tab -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <!-- Advisors tab -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <!-- Books tab (blocked) -->
      <!-- portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx and related — pending thread -->
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM C1 — Continuous NNA GEO: search + city drill-down         -->
    <!-- UNBLOCKED — geo_drill data already in timeseries_chart.json      -->
    <!-- ================================================================ -->
    <requirement id="C1.1">
      Update the GEO continuous NNA view in DistributionTab to render the top-8 states
      as separate series in the cumulative NNA chart. Use the same chart type, axis format,
      color scheme, and window toggle as the Assets Overview header panel's cumulative NNA chart.
      Data source: timeseries_chart.json geo view (per-state categories).
    </requirement>
    <requirement id="C1.2">
      Add a search input in the left panel controls that filters across ALL available states
      (not just top-8). States outside top-8 are accessible via search.
    </requirement>
    <requirement id="C1.3">
      Implement click-to-drill interaction:
        - Clicking a state in the chart legend OR selecting from search drills into that state
        - Chart re-renders showing per-city series for that state
          (sourced from timeseries_chart.json geo_drill[stateKey])
        - A breadcrumb/back control returns to the state-level view
      The drill state is local UI state — no API call needed (data already in the JSON).
    </requirement>
    <requirement id="C1.4">
      The back/breadcrumb must clearly display the current drill level:
        "All States" (default) or "Texas" (drilled) etc.
      Consistent with the existing GEO/ADV cohort toggle pattern already in the page.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C2 — Continuous NNA ADV: search + client drill-down       -->
    <!-- BLOCKED: requires Stream B1 (DT deploys adv_drill)               -->
    <!-- ================================================================ -->
    <requirement id="C2.1">
      GATE: Do not begin C2 until DT confirms adv_drill is deployed and present in
      timeseries_chart.json S3 output.
    </requirement>
    <requirement id="C2.2">
      Implement ADV continuous NNA view using the adv_drill shape agreed in the
      Pattern 0 thread (2026-03-03-continuous-nna-cla-alignment). The thread receipt
      defines: adv_drill JSON structure, architect key format, client series format,
      and the TypeScript interface name DE typed against. Do not infer the shape from
      the PRD alone — use the receipt as the binding spec.
      Behavior:
        - Top architects as separate series, same chart format as GEO view
        - Search input for architects not in top list
        - Click architect -> drill to client/relationship level (adv_drill[architectKey])
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level
    </requirement>
    <requirement id="C2.3">
      The ADV drill interaction uses the same component and pattern as GEO drill (C1).
      Factor out the drill logic into a shared hook or utility if C1 and C2 share enough
      structure — but only if the abstraction is clean. No premature abstraction.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C3 — Snapshot CLA: simplified two-color visualization     -->
    <!-- UNBLOCKED — data already in header_metrics.json                  -->
    <!-- ================================================================ -->
    <requirement id="C3.1">
      Replace the current CLA snapshot rendering (which incorrectly uses a flows/NNA chart)
      with a clean two-color proportional display:
        - Green = NMNC (New Client AUA percentage of total AUA)
        - Blue = NMEC (Existing Client AUA percentage of total AUA)
        - Preferred format: horizontal stacked bar or split donut — clean, no axes,
          just the two proportions with AUA dollar amounts labeled
      NO inflow/outflow data. NO NNA vocabulary. NO blue/red flows visual language.
    </requirement>
    <requirement id="C3.2">
      The visualization must support the time machine period selector (q1/q2/q3 periods)
      to show how the new-client percentage has shifted over time.
      Data source: header_metrics.json views.aua CLA structure
        (cla.current.geo.totals.nmnc_nna and related fields).
      Confirm field availability with DS if uncertain which fields carry NMNC/NMEC AUA.
    </requirement>
    <requirement id="C3.3">
      Label each segment clearly: "New Clients (NMNC)" in green, "Existing Clients (NMEC)"
      in blue. Include the AUA dollar amount and percentage for each segment.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA: new time series stacked area chart   -->
    <!-- BLOCKED: requires Stream B1 (DT deploys cla_timeseries)          -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE: Do not begin C4 until DT confirms cla_timeseries is deployed and present in
      timeseries_chart.json S3 output (cla.total field).
    </requirement>
    <requirement id="C4.2">
      Implement the continuous CLA view using the cla_timeseries shape agreed in the
      Pattern 0 thread (2026-03-03-continuous-nna-cla-alignment). The thread receipt
      defines: exact JSON structure (field names for NMNC and NMEC series, grain keys),
      S3 key, and the TypeScript interface name DE typed against.
      Chart behavior:
        - Y-axis = dollar AUM (absolute), two stacked areas: NMNC (green) and NMEC (blue)
        - Total height at each date = total firm AUM
        - Date range = same window toggle as other continuous views
        - Grains: total (firm-wide), geo/geo_drill, adv (architect terminal — no client drill)
      Use the agreed field names from the thread receipt, not the PRD's suggested naming.
    </requirement>
    <requirement id="C4.3">
      Add search input and drill-down behavior consistent with C1/C2:
        - GEO view: search states, click to drill to cities
        - ADV view: search architects (no client drill-down for CLA)
      Same breadcrumb/back pattern.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM H — Advisors tab: Portal Primitives Refactor              -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="H.1">
      Refactor all sections in AdvisorsTab.tsx to use portal panel primitives:
        Panel, PanelHeader, PanelContent, SmartPanelFooter from @/ui/components/panels
      Sections affected: Top Performers panel, Rolling Flows panel, Leaderboard panel.
      The visual output should be identical to the current layout after refactor —
      this is purely a structural change to match portal conventions.
    </requirement>
    <requirement id="H.2">
      Run bunx tsc -b after refactor to confirm no type errors introduced.
      DE reviews before DT pushes.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM I — Advisors tab: Top Performers visual identity           -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="I.1">
      Redesign the Top Performers (Top 3 highlights) panel to communicate rank and
      achievement more clearly:
        - Rank (1st / 2nd / 3rd) must be visually prominent
        - Advisor name prominent
        - Key metric (NNA for the active period) immediately readable
        - Use trophy/medal iconography or rank-badge treatment using Lucide icons
          already in the codebase (confirm which Lucide icons are available before choosing)
    </requirement>
    <requirement id="I.2">
      The redesign must work for all period toggles (QTD/YTD/1Y/3Y/Max).
      When the active period changes, Top Performers rankings update accordingly.
    </requirement>
    <requirement id="I.3">
      DE reviews the visual design before DT pushes to DEV.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM 4C — Advisors tab: New Rolling Flows visualization        -->
    <!-- BLOCKED: requires Stream B2 (DT deploys script 10 stacked bar)  -->
    <!-- ================================================================ -->
    <requirement id="4C.1">
      GATE: Do not begin 4C until DT confirms stacked_bar data is in
      advisor_rolling_flows.json S3 output (from script 10 Stream B2 deploy).
    </requirement>
    <requirement id="4C.2">
      Implement PRIMARY VIEW — Stacked Bar Chart — using the shape agreed in the
      Pattern 0 thread (2026-03-03-advisors-stacked-bar-alignment). The thread receipt
      defines: exact top-level key names in advisor_rolling_flows.json, how outflows
      are encoded (negative number? separate field? sign flag?), period key names,
      and the TypeScript interface name.
      Chart behavior:
        - X-axis: one bar per architect or implementor (per toggle)
        - Bars show inflows, outflows, NNA net per the agreed encoding
        - Sorted lowest to highest by NNA (highest performers rightmost)
        - Period toggle: per agreed period keys in thread receipt
        - Architects / Implementors toggle controls both views
      Use the agreed field names from the thread receipt, not the PRD's suggested naming.
    </requirement>
    <requirement id="4C.3">
      Implement SECONDARY VIEW — 1-Year Rolling Line Chart — using the rolling_1y shape
      agreed in the same thread receipt (2026-03-03-advisors-stacked-bar-alignment).
      The thread defines: per-advisor series structure, date+value format, and
      what date range DS committed to providing.
      Chart behavior:
        - X-axis: dates over the selected period window (period toggle = x-axis window)
        - Y-axis: 1-year rolling NNA per advisor (fixed 1Y rolling window per date point)
        - Same Architects/Implementors toggle as primary view
    </requirement>
    <requirement id="4C.4">
      View toggle (Primary / Secondary) must be clear and accessible.
      Recommended: a segmented control or tab above the chart area.
      The period toggle and Architects/Implementors toggle must remain visible in both views.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM G — Books tab implementation                               -->
    <!-- BLOCKED: requires Stream D thread receipt + Stream F deploy      -->
    <!-- ================================================================ -->
    <requirement id="G.1">
      BLOCKED: Do not begin Books tab implementation until both:
        (a) Stream D (Books design thread) receipt is available at:
            org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/
        (b) Stream F (DT deploys advisor-publisher with L4 fields) is confirmed complete.
      The thread receipt defines the visual design brief for L2/L3/L4. Do not design
      the Books tab independently — the thread outcome is the specification.
    </requirement>
    <requirement id="G.2">
      When gates are met: implement Books tab per the design brief at
        docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Scope: L2 (advisor book), L3 (relationship view), L4 (account + holdings + tax).
      Access gating: admin sees advisor selector (all advisors), advisor sees only own book.
      Use portal panel primitives throughout (consistent with Stream H refactor).
    </requirement>
    <requirement id="G.3">
      DE coordinates the Books tab implementation — RD implements visuals,
      DE handles API wiring and auth gating logic.
      Do not wire auth gating until 0.7.0_AE_CloudOps has confirmed opal-users-v2 mapping.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C1: GEO continuous NNA shows top-8 states as series; search filters all states; click drills to cities; breadcrumb returns to state view.</criterion>
    <criterion id="2">C2: ADV continuous NNA identical to GEO but for architects and clients (post-B1 deploy).</criterion>
    <criterion id="3">C3: CLA snapshot is a clean two-color NMNC/NMEC split; no flows/NNA vocabulary; time machine periods work.</criterion>
    <criterion id="4">C4: CLA continuous is a stacked area chart with NMNC (green) and NMEC (blue) AUM over time at all grains (post-B1).</criterion>
    <criterion id="5">H: All Advisors tab sections use portal panel primitives; bunx tsc -b passes; no visual regression.</criterion>
    <criterion id="6">I: Top Performers shows clear rank (1/2/3), advisor name, and NNA with medal/badge treatment; works across all periods.</criterion>
    <criterion id="7">4C: Stacked bar primary view + rolling line secondary view implemented with period toggle and Architects/Implementors toggle.</criterion>
    <criterion id="8">G: Books tab L2/L3/L4 implemented per design brief; access gating functional (post-thread and post-F).</criterion>
    <criterion id="9">bunx tsc -b passes after each stream's changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Immediate start items (no blocks): C1, C3, H, I. Begin these in your first activation session.</constraint>
    <constraint>C2 and C4 blocked by DT Stream B1 deploy — check DT session log for deploy confirmation before starting.</constraint>
    <constraint>4C blocked by DT Stream B2 deploy — same pattern.</constraint>
    <constraint>G blocked by Stream D thread completion AND Stream F deploy.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>DE (0.4.0_DE_ClientPlatform) must review C3 NMNC/NMEC label accuracy and Top Performers (I) before DT pushes to DEV.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/{Tab} -- description"</constraint>
    <constraint>NOTE: You have 3 pending task orders (page_inventory, distribution_nomenclature_fix, continuous_view_max_window_clients_fix). Complete those before starting C1 if they conflict with the Distribution tab changes. Confirm with DE if there is overlap.</constraint>
    <constraint>NOTE: You have no prior session logs. Write a session log after your first activation and first work session. The COO needs it before scheduling the Books thread (Stream D).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="C2, C4 blocked by B1; 4C blocked by B2"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="G blocked by thread completion"/>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="G blocked by F deploy"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="C3 field confirmation — DS to confirm NMNC/NMEC field names in header_metrics.json"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: GEO continuous with search + drill (C1)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: ADV continuous with search + drill (C2, post-B1)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: CLA snapshot two-color (C3)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: CLA continuous stacked area (C4, post-B1)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: portal primitives refactor (H)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: Top Performers visual redesign (I)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: stacked bar primary + rolling line secondary (4C, post-B2)</deliverable>
    <deliverable type="commit">ClientsTab.tsx and related: Books tab L2/L3/L4 (G, post-thread + post-F)</deliverable>
  </deliverables>
</task_order>
```

#### continuous_view_max_window_clients_fix.md

# Task Order — Continuous View: "Total Clients" at Max Window

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-continuous-max-window-clients</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>medium</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    In the Segment Analytics continuous view (both GEO and ADV cohorts), the left-panel
    hero metrics tile currently shows "New Clients" regardless of window selection.
    When window = "Max", this is wrong on two counts:
      1. The value displays "--" (the backend does not populate new_clients['Max']).
      2. "New Clients" is semantically incorrect for an all-time window — over all time,
         every client is a "new" client. The correct label is "Total Clients" and the
         correct value is the current total relationship count.

    Fix: make the tile window-aware.
      - 1Y / 3Y windows:  label = "New Clients",    value = new_clients[window]  (existing)
      - Max window:       label = "Total Clients",  value = current total relationships
  </objective>

  <problem>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    Location: ContinuousChartView component, ~lines 802-807

    Current code:
      &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
        &lt;p className="text-sm font-bold text-white"&gt;
          {data?.metadata?.new_clients?.[window as string] ?? '--'}
        &lt;/p&gt;
        &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;New Clients&lt;/p&gt;
      &lt;/div&gt;

    Root cause:
      data.metadata.new_clients is a Record&lt;string, number&gt; keyed by window string.
      The backend populates keys '1Y' and '3Y' but NOT 'Max', so window='Max' always
      falls through to '--'. Even if it were populated, "New Clients" over all time
      is meaningless — it is equivalent to total clients.

    Affected views:
      Both GEO and ADV continuous AUA views — they share the same ContinuousChartView
      component, so the fix is in one place.
  </problem>

  <fix>
    Three changes required:

    1. Add totalClients?: number to ContinuousChartViewProps interface.
       (~line 658 — interface definition)

    2. Pass totalClients at the ContinuousChartView call site.
       (~line 396-402 in DistributionTab — the JSX element)
       Derive totalClients from analyticsData (available in DistributionTab scope):
         const cohortView = cohort === 'geo'
           ? analyticsData?.views?.geo
           : analyticsData?.views?.adv
         totalClients = cohortView?.current?.metrics?.client_count
                        ?? cohortView?.metrics?.client_count

    3. Make the tile window-aware in ContinuousChartView.
       (~lines 802-807)
       When window === 'Max': label = "Total Clients", value = totalClients ?? '--'
       When window !== 'Max': label = "New Clients",   value = data?.metadata?.new_clients?.[window] ?? '--'
  </fix>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Three locations to edit, all within DistributionTab.tsx.
      </description>

      <change id="1">
        <location>
          ~Lines 658-664 — ContinuousChartViewProps interface
          (search: "interface ContinuousChartViewProps")
        </location>
        <current>
interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record&lt;string, string&gt;
}
        </current>
        <new>
interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record&lt;string, string&gt;
  totalClients?: number
}
        </new>
        <rationale>Adds the optional total relationship count for the Max-window tile.</rationale>
      </change>

      <change id="2">
        <location>
          ~Line 666 — ContinuousChartView function signature
          (search: "function ContinuousChartView({")
        </location>
        <current>
function ContinuousChartView({ data, cohort, metric, window, categoryColorMap }: ContinuousChartViewProps) {
        </current>
        <new>
function ContinuousChartView({ data, cohort, metric, window, categoryColorMap, totalClients }: ContinuousChartViewProps) {
        </new>
        <rationale>Destructures the new prop.</rationale>
      </change>

      <change id="3">
        <location>
          ~Lines 396-402 — ContinuousChartView JSX call site in DistributionTab
          (search: "&lt;ContinuousChartView" — the component usage, not the definition)
        </location>
        <current>
            &lt;ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
            /&gt;
        </current>
        <new>
            &lt;ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
              totalClients={
                cohort === 'geo'
                  ? (analyticsData?.views?.geo?.current?.metrics?.client_count
                     ?? analyticsData?.views?.geo?.metrics?.client_count)
                  : (analyticsData?.views?.adv?.current?.metrics?.client_count
                     ?? analyticsData?.views?.adv?.metrics?.client_count)
              }
            /&gt;
        </new>
        <rationale>
          analyticsData and cohort are both in scope in DistributionTab at this point.
          Derives total relationship count from the current period snapshot metrics.
          The ?? fallback handles both the legacy PartnerAnalyticsView shape (.metrics)
          and the current PartnerAnalyticsViewWithPeriods shape (.current.metrics).
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Lines 802-807 — "New Clients" tile inside ContinuousChartView
          (search: the bg-white/5 div with "New Clients" label text)
        </location>
        <current>
        &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
          &lt;p className="text-sm font-bold text-white"&gt;
            {data?.metadata?.new_clients?.[window as string] ?? '--'}
          &lt;/p&gt;
          &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;New Clients&lt;/p&gt;
        &lt;/div&gt;
        </current>
        <new>
        &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
          &lt;p className="text-sm font-bold text-white"&gt;
            {window === 'Max'
              ? (totalClients?.toLocaleString() ?? '--')
              : (data?.metadata?.new_clients?.[window as string]?.toLocaleString() ?? '--')}
          &lt;/p&gt;
          &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;
            {window === 'Max' ? 'Total Clients' : 'New Clients'}
          &lt;/p&gt;
        &lt;/div&gt;
        </new>
        <rationale>
          Max window: shows total relationship count with "Total Clients" label.
            - Semantically correct: over all time every client is cumulative total.
            - Fixes the '--' display (new_clients['Max'] is never populated by backend).
          1Y / 3Y: unchanged — shows new_clients[window] with "New Clients" label.
          .toLocaleString() added to both paths for consistent number formatting.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. Use offset reads:
      - ~line 658 for Changes 1-2 (interface + function signature)
      - ~line 390 for Change 3 (call site)
      - ~line 800 for Change 4 (tile)
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 4 changes as a unit. Change 3 and Change 4 are the user-visible
      fix; Changes 1 and 2 are the required plumbing.
    </requirement>
    <requirement id="3">
      The type access paths for totalClients in Change 3 use optional chaining
      with a ?? fallback to handle both the legacy PartnerAnalyticsView shape
      (direct .metrics.client_count) and the current PartnerAnalyticsViewWithPeriods
      shape (.current.metrics.client_count). Verify the actual types at read time
      and adjust if needed — the intent is to get the current total relationship count
      for the selected cohort (geo or adv).
    </requirement>
    <requirement id="4">
      analyticsData is the PartnerAnalyticsResponse prop passed into DistributionTab.
      It is in scope at the ContinuousChartView call site (line ~396). You are not
      introducing a new data fetch or state variable.
    </requirement>
    <requirement id="5">
      Do not change the 1Y or 3Y behavior. The existing new_clients[window] path
      is correct for those windows.
    </requirement>
    <requirement id="6">
      Commit with tag:
      "0.4.0_DE_ClientPlatform: fix continuous view — Total Clients at Max window"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="7">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/continuous_view_max_window_clients_fix.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      ContinuousChartViewProps interface has totalClients?: number field.
    </criterion>
    <criterion id="2">
      ContinuousChartView function signature destructures totalClients.
    </criterion>
    <criterion id="3">
      At the call site, totalClients is derived from analyticsData.views[cohort]
      current relationship count (with legacy shape fallback).
    </criterion>
    <criterion id="4">
      When window = "Max":
        - Tile label = "Total Clients"
        - Tile value = current total relationship count (not '--')
    </criterion>
    <criterion id="5">
      When window = "1Y" or "3Y":
        - Tile label = "New Clients" (unchanged)
        - Tile value = new_clients[window] from metadata (unchanged)
    </criterion>
    <criterion id="6">
      Both GEO and ADV cohorts exhibit the correct behavior (they share
      ContinuousChartView so this is automatic).
    </criterion>
    <criterion id="7">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not change the window toggle options (1Y, 3Y, Max) or their ordering.
    </constraint>
    <constraint>
      Do not change any other hero metric tiles (the gain-since-start tile
      or growth-rate tile in the 2-column grid above). Only the "New Clients"
      / "Total Clients" tile is in scope.
    </constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (4 changes: ContinuousChartViewProps, function signature, call site prop,
      window-aware tile label + value)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/continuous_view_max_window_clients_fix.md
    </deliverable>
  </deliverables>
</task_order>
```

#### distribution_nomenclature_fix.md

# Task Order — Distribution Chart Nomenclature Fix: AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-distribution-nomenclature-advisor-intelligence</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>high</priority>
    <type>nomenclature-fix</type>
  </metadata>

  <objective>
    Fix all axis labels, tooltip labels, metrics tile labels, and footnotes in
    SnapshotDistributionChart and SnapshotDistributionMetrics to use accurate,
    mode-aware nomenclature.

    The chart operates in two fundamentally different data modes, each with its
    own correct unit of analysis:

    - AUA mode  (default, isNnaMode=false):
        Histogram bins individual Black Diamond *account* balances.
        Data source: gold/account_performance.parquet (account_id level).
        One observation = one funded account.
        Canonical unit: "account".

    - NNA mode  (isNnaMode=true):
        Histogram bins each *relationship's* period NNA.
        Data source: client_performance.parquet (relationship_id level).
        One observation = one relationship (relationship_id).
        Canonical unit: "relationship".

    Current labels ("Client AUA", "Client Count", "Number of Clients", "Total Clients")
    are wrong in both modes:
    - In AUA mode: data is account-level but labels imply relationship-level.
    - In NNA mode: "client" is informal and non-specific; "relationship" is the
      correct BD term that matches the underlying relationship_id key.

    ModelPortfolios (SmartX data) uses "Holdings" for the equivalent chart.
    AdvisorIntelligence (Black Diamond data) must NOT copy "holdings" — the correct
    BD term is "account". The formatting pattern (consistent label + tooltip + footnote)
    is the same; only the vocabulary differs.
  </objective>

  <data_context>
    Confirmed by reading data/black_diamond/scripts/gold/09_generate_partner_analytics.py:

    AUA distribution (lines 584, 621-623):
      acct_arch = acct_perf_day (gold/account_performance.parquet)
      arch_accts = acct_arch[acct_arch['architect'] == arch]
      adv_dist   = calculate_distribution_stats(arch_accts['total_aua'])
      One row = one Black Diamond account (account_id level).
      DistributionStats.count = number of funded accounts in that segment.

    NNA distribution (line 396-400, 508-509):
      rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        returns DataFrame with columns: relationship_id, period_nna
      calculate_nna_distribution_stats(rel_nna['period_nna'])
      One row = one relationship (relationship_id level).
      DistributionStats.count = number of relationships.

    ModelPortfolios reference (AccountDistributionChart.tsx):
      Y-axis:       "Number of Holdings"    (SmartX-specific vocabulary)
      X-axis:       "Holding Size"          (SmartX-specific vocabulary)
      Tooltip row 1: "Holding Size"
      Tooltip row 2: "Account Count"        (note: row 2 already says "Account")
      Metrics tile: "Total Holdings"        (SmartX-specific vocabulary)
      Footnote:     "Excludes {N} newly opened holdings with $0 balance (unfunded)."

    AdvisorIntelligence must NOT use "Holdings" — that is SmartX terminology.
    The correct BD vocabulary is "account" (singular/plural) for AUA mode and
    "relationship" for NNA mode.
  </data_context>

  <nomenclature_standard>
    AUA mode (isNnaMode = false) — account-level data:
      Y-axis label:       "Number of Accounts"
      X-axis label:       "Account Size"
      Tooltip row 1 key:  "Account Size"
      Tooltip row 2 key:  "Account Count"
      Metrics tile label: "Total Accounts"
      Footnote amber:     "Excludes accounts with $0 balance (unfunded)."
      Footnote muted:     " Distribution reflects funded accounts only, log-spaced bins."

    NNA mode (isNnaMode = true) — relationship-level data:
      Y-axis label:       "Number of Relationships"
      X-axis label:       "Period NNA"
      Tooltip row 1 key:  "NNA Range"
      Tooltip row 2 key:  "Relationship Count"
      Metrics tile label: "Total Relationships"
      Footnote:           (keep existing NNA footnote — no change)
  </nomenclature_standard>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Eleven changes across four locations:
        (A) SnapshotDistributionChartProps interface + function signature (~lines 1696-1702)
        (B) SnapshotDistributionChart body — axis labels + tooltip (~lines 1759-1812)
        (C) SnapshotDistributionMetrics function signature + primary tile (~lines 1853-1877)
        (D) Call sites in SnapshotDistributionView + right-partition footnote (~lines 1444-1462)
      </description>

      <!-- ================================================================ -->
      <!-- A. SnapshotDistributionChartProps + function signature           -->
      <!-- ================================================================ -->

      <change id="1">
        <location>~Lines 1696-1700 — SnapshotDistributionChartProps interface</location>
        <current>
interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
}
        </current>
        <new>
interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
  isNnaMode?: boolean
}
        </new>
        <rationale>Adds the mode flag so the chart can render mode-aware labels.</rationale>
      </change>

      <change id="2">
        <location>~Line 1702 — SnapshotDistributionChart function signature</location>
        <current>
function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount }: SnapshotDistributionChartProps) {
        </current>
        <new>
function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount, isNnaMode = false }: SnapshotDistributionChartProps) {
        </new>
        <rationale>Destructures the new prop with a safe default of false (AUA mode).</rationale>
      </change>

      <!-- ================================================================ -->
      <!-- B. SnapshotDistributionChart body — axis labels + tooltip        -->
      <!-- ================================================================ -->

      <change id="3">
        <location>
          ~Line 1760 — Y-axis label text inside SnapshotDistributionChart
          (the span inside the absolute-positioned vertical div,
           search context: writingMode vertical-rl, text "Number of Clients")
        </location>
        <current>
          Number of Clients
        </current>
        <new>
          {isNnaMode ? 'Number of Relationships' : 'Number of Accounts'}
        </new>
        <rationale>
          AUA mode: counts individual Black Diamond accounts.
          NNA mode: counts relationships (relationship_id level).
          "Clients" was wrong for both.
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Line 1767 — X-axis label span inside SnapshotDistributionChart
          (absolute-positioned div at bottom, search: "Client AUA")
        </location>
        <current>
          &lt;span className="text-[11px] text-white/50"&gt;Client AUA&lt;/span&gt;
        </current>
        <new>
          &lt;span className="text-[11px] text-white/50"&gt;{isNnaMode ? 'Period NNA' : 'Account Size'}&lt;/span&gt;
        </new>
        <rationale>
          AUA mode: x-axis is the size of an individual account ("Account Size").
          NNA mode: x-axis is the relationship's period NNA ("Period NNA").
        </rationale>
      </change>

      <change id="5">
        <location>
          ~Line 1807 — Tooltip row 1 label inside RechartsTooltip
          (search: the span with text "Client AUA" — first row in tooltip content)
        </location>
        <current>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;Client AUA&lt;/span&gt;
        </current>
        <new>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;{isNnaMode ? 'NNA Range' : 'Account Size'}&lt;/span&gt;
        </new>
        <rationale>Tooltip row 1 names the x-axis bin. Must match x-axis label.</rationale>
      </change>

      <change id="6">
        <location>
          ~Line 1811 — Tooltip row 2 label inside RechartsTooltip
          (search: the span with text "Client Count" — second row in tooltip content)
        </location>
        <current>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;Client Count&lt;/span&gt;
        </current>
        <new>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;{isNnaMode ? 'Relationship Count' : 'Account Count'}&lt;/span&gt;
        </new>
        <rationale>
          AUA mode: the bar height is a count of accounts in that size bin.
          "Account Count" matches ModelPortfolios tooltip row 2 exactly.
          NNA mode: count is relationships.
        </rationale>
      </change>

      <!-- ================================================================ -->
      <!-- C. SnapshotDistributionMetrics — function signature + tile label -->
      <!-- ================================================================ -->

      <change id="7">
        <location>
          ~Line 1853 — SnapshotDistributionMetrics function signature
          (search: "function SnapshotDistributionMetrics({ data, currentData }")
        </location>
        <current>
function SnapshotDistributionMetrics({ data, currentData }: { data: DistributionStats; currentData?: DistributionStats | null }) {
        </current>
        <new>
function SnapshotDistributionMetrics({ data, currentData, isNnaMode = false }: { data: DistributionStats; currentData?: DistributionStats | null; isNnaMode?: boolean }) {
        </new>
        <rationale>Adds mode flag so the primary tile label can be mode-aware.</rationale>
      </change>

      <change id="8">
        <location>
          ~Lines 1874-1878 — Primary tile inside SnapshotDistributionMetrics
          (search: comment "Total Clients" and the div containing it)
        </location>
        <current>
        {/* Total Clients */}
        &lt;div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40 min-w-[100px]"&gt;
          &lt;div className="text-xs text-white/90 font-semibold mb-1"&gt;Total Clients&lt;/div&gt;
          &lt;div className="text-lg font-bold text-white"&gt;{data.count.toLocaleString()}&lt;/div&gt;
        &lt;/div&gt;
        </current>
        <new>
        {/* Total Accounts / Total Relationships */}
        &lt;div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85())]/40 min-w-[100px]"&gt;
          &lt;div className="text-xs text-white/90 font-semibold mb-1"&gt;{isNnaMode ? 'Total Relationships' : 'Total Accounts'}&lt;/div&gt;
          &lt;div className="text-lg font-bold text-white"&gt;{data.count.toLocaleString()}&lt;/div&gt;
        &lt;/div&gt;
        </new>
        <rationale>
          AUA mode: count is funded Black Diamond accounts → "Total Accounts".
          NNA mode: count is relationships → "Total Relationships".
          data.count is correct for both — only the label text changes.
        </rationale>
      </change>

      <!-- ================================================================ -->
      <!-- D. Call sites + right-partition footnote                         -->
      <!-- ================================================================ -->

      <change id="9">
        <location>
          ~Line 1444 — SnapshotDistributionChart JSX element inside SnapshotDistributionView
          (search: "&lt;SnapshotDistributionChart" — the component usage, not its definition)
        </location>
        <current>
              &lt;SnapshotDistributionChart
                data={distributionData}
                accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                globalMaxCount={globalMaxCount}
              /&gt;
        </current>
        <new>
              &lt;SnapshotDistributionChart
                data={distributionData}
                accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                globalMaxCount={globalMaxCount}
                isNnaMode={isNnaMode}
              /&gt;
        </new>
        <rationale>
          isNnaMode is already a const in SnapshotDistributionView scope
          (derived from: const isNnaMode = metric === 'nna').
          Threading it into the chart component so it can render mode-aware labels.
        </rationale>
      </change>

      <change id="10">
        <location>
          ~Line 1451 — SnapshotDistributionMetrics JSX element inside SnapshotDistributionView
          (search: "&lt;SnapshotDistributionMetrics data={distributionData}")
        </location>
        <current>
              &lt;SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} /&gt;
        </current>
        <new>
              &lt;SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} isNnaMode={isNnaMode} /&gt;
        </new>
        <rationale>Threads the mode flag into the metrics component for the tile label.</rationale>
      </change>

      <change id="11">
        <location>
          ~Lines 1457-1461 — AUA branch of the right-partition footnote
          (search: amber span "Excludes accounts with $0 balance (unfunded)."
           and the muted span " Distribution uses log-spaced bins across funded accounts only.")
        </location>
        <current>
                    &lt;span className="text-amber-400 font-bold"&gt;Excludes accounts with $0 balance (unfunded).&lt;/span&gt;
                    &lt;span className="text-white/40"&gt; Distribution uses log-spaced bins across funded accounts only.&lt;/span&gt;
        </current>
        <new>
                    &lt;span className="text-amber-400 font-bold"&gt;Excludes accounts with $0 balance (unfunded).&lt;/span&gt;
                    &lt;span className="text-white/40"&gt; Distribution reflects funded accounts only, log-spaced bins.&lt;/span&gt;
        </new>
        <rationale>
          The amber span is already correct — "accounts" is right.
          Only the muted span changes: shorter phrasing, consistent with ModelPortfolios
          footnote structure ("reflects funded accounts only" instead of the more wordy
          "uses log-spaced bins across funded accounts only").
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. Use offset reads:
      - ~line 1696 for Changes 1-2 (interface + function signature)
      - ~line 1755 for Changes 3-6 (axis labels + tooltip body)
      - ~line 1853 for Changes 7-8 (metrics component)
      - ~line 1440 for Changes 9-11 (call sites + footnote)
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 11 changes. Do not apply a subset.
      Changes 3-6 and 8 are the most visible to users. Changes 1-2 and 7 are
      the prerequisite interface wiring. Changes 9-11 are the connective tissue.
    </requirement>
    <requirement id="3">
      isNnaMode is already declared in SnapshotDistributionView scope as:
        const isNnaMode = metric === 'nna'
      You are NOT introducing a new variable. You are only threading it as a prop
      into SnapshotDistributionChart (Change 9) and SnapshotDistributionMetrics
      (Change 10), then consuming it inside those functions (Changes 3-8).
    </requirement>
    <requirement id="4">
      Do not change the NNA footnote text (the isNnaMode=true branch, ~line 1454).
      Only the AUA branch text is updated (Change 11 — muted span wording only).
    </requirement>
    <requirement id="5">
      Do not change the right-partition section header (distributionLabel h4),
      the help tooltip on that header, or the donut legend client_count labels.
      Those are in separate scope and are not part of this task.
    </requirement>
    <requirement id="6">
      Do not change any percentile tile (P10/P25/Median/P75/P90) in
      SnapshotDistributionMetrics. Only the primary "Total" tile (Change 8) changes.
    </requirement>
    <requirement id="7">
      ModelPortfolios uses data.account_count; DistributionTab uses data.count.
      These are different TypeScript interface shapes (aum endpoint vs AI types).
      Do NOT attempt to change data.count to data.account_count. Display label
      changes only — field access is untouched.
    </requirement>
    <requirement id="8">
      Commit with tag:
      "0.4.0_DE_ClientPlatform: fix distribution chart nomenclature — accounts/relationships"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="9">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/distribution_nomenclature_fix.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      SnapshotDistributionChartProps has isNnaMode?: boolean field.
    </criterion>
    <criterion id="2">
      In AUA mode (isNnaMode=false):
      Y-axis = "Number of Accounts"
      X-axis = "Account Size"
      Tooltip row 1 = "Account Size"
      Tooltip row 2 = "Account Count"
    </criterion>
    <criterion id="3">
      In NNA mode (isNnaMode=true):
      Y-axis = "Number of Relationships"
      X-axis = "Period NNA"
      Tooltip row 1 = "NNA Range"
      Tooltip row 2 = "Relationship Count"
    </criterion>
    <criterion id="4">
      SnapshotDistributionMetrics primary tile:
      AUA mode = "Total Accounts", NNA mode = "Total Relationships".
    </criterion>
    <criterion id="5">
      Right-partition AUA footnote muted span reads:
      " Distribution reflects funded accounts only, log-spaced bins."
    </criterion>
    <criterion id="6">
      isNnaMode={isNnaMode} is present on both
      &lt;SnapshotDistributionChart&gt; and &lt;SnapshotDistributionMetrics&gt; call sites.
    </criterion>
    <criterion id="7">
      No other labels, data fields, percentile tiles, section headers,
      or donut legend text changed.
    </criterion>
    <criterion id="8">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not use "Holdings" anywhere — that is SmartX/ModelPortfolios vocabulary.
      AdvisorIntelligence data is Black Diamond. The correct terms are
      "account" (AUA mode) and "relationship" (NNA mode).
    </constraint>
    <constraint>
      Change 8 edits the JSX comment and the tile label text only.
      The className strings on the surrounding divs are identical — match them
      exactly when constructing the old_string for the Edit tool.
    </constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
    <constraint>
      Changes 3-6 use JSX expressions ({isNnaMode ? '...' : '...'}) inside
      text nodes. Verify JSX is syntactically valid after each edit.
    </constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (11 changes: SnapshotDistributionChartProps, SnapshotDistributionChart body,
      SnapshotDistributionMetrics, call sites, AUA footnote)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/distribution_nomenclature_fix.md
    </deliverable>
  </deliverables>
</task_order>
```

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

#### xtick_spacing_fix.md

# Task Order — X-Tick Spacing Fix: AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-advisor-intelligence</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>high</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    Make the DistributionTab split layout in AdvisorIntelligence visually canonical
    with the equivalent split layout in ModelPortfolios. This means:
    (a) the donut (left partition) and bell curve (right partition) containers are
        the same height, and
    (b) the metrics rows below each chart partition sit at the same vertical level.
    Root cause is four structural mismatches vs ModelPortfolios, not purely a tick
    spacing issue.
  </objective>

  <problem>
    Four differences vs ModelPortfolios cause the visual disparity:

    1. DONUT CONTAINER HEIGHT (primary cause of layout misalignment):
       DistributionTab wraps the ApexCharts donut (left partition) in h-[380px].
       ModelPortfolios wraps its donut in h-[450px].
       This 70px mismatch means the left partition is shorter than the right, so
       the SnapshotDistributionMetrics row starts at a different Y position than
       the donut-side content — the two partitions are not level.

    2. BELL CURVE CONTAINER HEIGHT (mirrors problem 1):
       DistributionTab wraps SnapshotDistributionChart (right partition) in h-[380px].
       ModelPortfolios wraps AccountDistributionChart in h-[450px].
       The 70px deficit directly shrinks the plot area and makes the chart cramped.

    3. XAXIS HEIGHT (cause of gap between tick labels and metrics):
       SnapshotDistributionChart uses XAxis height={72}.
       AccountDistributionChart uses XAxis height={50}.
       The extra 22px allocates a dead strip of space below the axis line — the tick
       labels at negative angle extend upward (not downward) so that strip is visually
       empty, creating the perceived gap between the chart and the metrics row below.

    4. TICK MARGIN (secondary — same as other charts):
       No tickMargin set, so labels are flush against the axis line.
  </problem>

  <fix_standard>
    Four changes required to make DistributionTab canonical with ModelPortfolios:
    1. Donut container height: h-[380px] → h-[450px]   (DistributionTab.tsx ~line 1266)
    2. Bell curve container height: h-[380px] → h-[450px]  (DistributionTab.tsx ~line 1443)
    3. XAxis height: 72 → 50                            (SnapshotDistributionChart XAxis)
    4. tickMargin={16}                                  (SnapshotDistributionChart XAxis)
    The bottom margin change (15 → 50) also stands — with the container now at 450px,
    bottom=50 gives a plot area of 320px (identical to ModelPortfolios after its own fix:
    450 - 30 - 50 - 50 = 320).
    With both partitions at h-[450px], the SnapshotDistributionMetrics row and the
    donut-side quarter strip sit at identical vertical positions — matching ModelPortfolios.
  </fix_standard>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Four locations to edit:
        (1) the donut container div ~line 1266 (LEFT partition),
        (2) the bell curve container div ~line 1443 (RIGHT partition),
        (3) SnapshotDistributionChart AreaChart margin ~line 1764, and
        (4) SnapshotDistributionChart XAxis ~lines 1772-1780.
        All four are inside DistributionTab.tsx.
      </description>

      <change id="1">
        <location>
          ~Line 1266 — donut container div in the LEFT partition
          (search context: directly inside
           "&lt;div className="w-full max-w-[700px] flex flex-col gap-6 items-center"&gt;"
           in the LEFT PARTITION section, wrapping the ApexCharts donut + legend row)
        </location>
        <current>&lt;div className="h-[380px] flex items-center justify-center relative"&gt;</current>
        <new>&lt;div className="h-[450px] flex items-center justify-center relative"&gt;</new>
        <rationale>
          ModelPortfolios wraps its donut in h-[450px]. With the left partition at
          h-[380px] and the right at h-[450px] (after Change 2), the two partitions
          are mismatched in height — the SnapshotDistributionMetrics row starts 70px
          higher than the donut-side content. Setting both to h-[450px] levels them.
        </rationale>
      </change>

      <change id="2">
        <location>
          ~Line 1443 — chart container div wrapping SnapshotDistributionChart
          (search context: directly inside
           "&lt;div className="w-full max-w-[700px] flex flex-col gap-6 items-center"&gt;"
           in the RIGHT PARTITION section)
        </location>
        <current>&lt;div className="h-[380px] w-full min-w-0"&gt;</current>
        <new>&lt;div className="h-[450px] w-full min-w-0"&gt;</new>
        <rationale>
          ModelPortfolios uses h-[450px]. The 70px deficit is the primary cause of
          the cramped plot area. This is the most important change for the bell curve.
        </rationale>
      </change>

      <change id="3">
        <location>
          ~Line 1764 — AreaChart margin prop inside SnapshotDistributionChart
          (search context: the AreaChart directly under
           "&lt;ResponsiveContainer width="100%" height="100%"&gt;" inside
           SnapshotDistributionChart)
        </location>
        <current>margin={{ top: 30, right: 10, left: 0, bottom: 15 }}</current>
        <new>margin={{ top: 30, right: 10, left: 0, bottom: 50 }}</new>
        <rationale>
          With h-[450px] container, bottom=50 yields plot area of 320px
          (450 - 30 - 50 - 50 = 320) — identical to ModelPortfolios after its fix.
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Lines 1772-1780 — XAxis inside SnapshotDistributionChart AreaChart
        </location>
        <current>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-55}
            textAnchor="end"
            height={72}
            interval={0}
          /&gt;
        </current>
        <new>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-55}
            textAnchor="end"
            height={50}
            interval={0}
            tickMargin={16}
          /&gt;
        </new>
        <rationale>
          height: 72 → 50 — matches AccountDistributionChart. The 22px reduction
          eliminates the dead strip below the axis line (tick labels at negative angle
          extend upward, not downward, so that strip was visually empty whitespace).
          tickMargin={16} — adds gap between axis tick line and label text.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. The file is very large.
      Read ~line 1260 for the donut container div (Change 1).
      Read ~line 1440 for the bell curve container div (Change 2).
      Read ~line 1690 onward for SnapshotDistributionChart (Changes 3 and 4).
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 4 changes. Changes 1 and 2 (both container heights) are the most
      important — they are what levels the two partitions. Do not apply a subset.
    </requirement>
    <requirement id="3">
      The two h-[380px] → h-[450px] changes are on different divs with different
      className strings:
      - Change 1 (donut): "h-[380px] flex items-center justify-center relative"
      - Change 2 (bell curve): "h-[380px] w-full min-w-0"
      Do not confuse them. Match on the full className string for each Edit call.
    </requirement>
    <requirement id="4">
      Do not touch any other container divs, chart components, or XAxis elements
      in DistributionTab.tsx. The only div heights being changed are the two at
      ~line 1266 and ~line 1443. No other heights, no other charts.
    </requirement>
    <requirement id="5">
      Do NOT touch the other XAxis elements in DistributionTab.tsx:
      - ComposedChart XAxis at ~line 546 (continuous view) — not in scope
      - AreaChart XAxis at ~line 862 (daily NNA chart) — not in scope
      - ClaSnapshotView XAxis at ~line 2067 (CLA diverging bar) — not in scope
    </requirement>
    <requirement id="6">
      Commit with tag: "0.4.0_DE_ClientPlatform: canonicalize AdvisorIntelligence distribution layout"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="7">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Donut container div (LEFT partition, ~line 1266) is h-[450px] (was h-[380px]).
    </criterion>
    <criterion id="2">
      Bell curve container div (RIGHT partition, ~line 1443) is h-[450px] (was h-[380px]).
    </criterion>
    <criterion id="3">
      SnapshotDistributionChart AreaChart bottom margin = 50.
    </criterion>
    <criterion id="4">
      SnapshotDistributionChart XAxis height = 50 (was 72). tickMargin={16}.
    </criterion>
    <criterion id="5">
      Resulting plot area = 450 - 30 - 50 - 50 = 320px. Matches ModelPortfolios.
    </criterion>
    <criterion id="6">
      Both partitions at h-[450px]: SnapshotDistributionMetrics and donut-side
      quarter strip sit at identical vertical positions — layout mirrors ModelPortfolios.
    </criterion>
    <criterion id="7">
      No other container heights or XAxis elements in DistributionTab.tsx modified.
    </criterion>
    <criterion id="8">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Change 1 must target the div at ~line 1266 (className contains "flex items-center justify-center relative"). Change 2 must target the div at ~line 1443 (className contains "w-full min-w-0"). Do not swap them.</constraint>
    <constraint>Do not change angle, textAnchor, fontSize, or interval on the XAxis.</constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
    <constraint>
      This fix is being applied in parallel with task order
      0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-model-portfolios (issued to 0.4.1_RD_ModelPortfolios).
      Both fixes must use identical tickMargin={16} standard for cross-page uniformity.
    </constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx (4 changes:
      donut container height, bell curve container height, AreaChart bottom margin,
      XAxis height + tickMargin)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md
    </deliverable>
  </deliverables>
</task_order>
```


### 0.4.2_RD_AdvisorIntelligence -- Recent Commits

# Recent commits by 0.4.2_RD_AdvisorIntelligence

076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b5ace0c0 org: quality audit -- fix bugs, upgrade thin profiles, seed missing deliverables
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
42f99352 logs: 0.4.2_RD_AdvisorIntelligence distribution nomenclature fix session log
2f8de475 docs(org): add xtick fix addendum for 0.4.2_RD_AdvisorIntelligence
4e046836 logs: 0.4.2_RD_AdvisorIntelligence xtick spacing fix session log

### 0.4.0_DE_ClientPlatform -- Recent Session Logs

#### pod_inventory_upgrade_ai_full_fidelity.md

# pod_inventory.xml Upgrade: AdvisorIntelligence Full-Fidelity — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-03
**Start Time:** session start
**End Time:** ~15 min
**Workspace CLOUD commit:** `5efb15f4`

## Objective

Upgrade the AdvisorIntelligence section of pod_inventory.xml from medium-fidelity (sourced from
portal source reads) to full-fidelity now that 0.4.2_RD_AdvisorIntelligence produced their
page_inventory.xml deliverable (2026-03-02, discovered at session start today).

---

## Work Completed

### 1. Read 0.4.2_RD page_inventory.xml

Confirmed deliverable exists and is 100% complete (16 .tsx files, 3 .ts files, 10 API calls,
all shared imports traced). Key additions vs. prior pod_inventory AdvisorIntelligence section:
- Full tab state (UI state variables per tab documented)
- CLA metric in Distribution tab documented
- Drill-down path (states->cities, architects->clients) confirmed
- lifecycle_and_state section: state management approach, full data_flow sequence, type_guards
- unused_tabs section: AssetIntelligenceTab correctly labeled as NOT wired in v5
- `useAuth` and `useFilterTracking` shared imports confirmed (BooksTab)
- `@/lib/dateUtils.formatPanelTimestamp` import confirmed (page level)

### 2. Updated pod_inventory.xml

Changes made:
- `rd_deliverable_status` for 0.4.2: MISSING -> complete
- Removed `rd_deliverable_warning` block; replaced with `rd_audit_completeness` note
- Upgraded all 3 tab descriptions with full state/behavior detail from RD audit
- Added `unused_tabs` section for AssetIntelligenceTab
- Added `lifecycle_and_state` section (state_management, data_flow, type_guards)
- Removed missing_deliverable known_issue for 0.4.2; replaced with accurate limitation notes
- pod_health: missing_deliverables_count 1 -> 0; blocker #1 cleared; summary updated
- date: 2026-03-02 -> 2026-03-03 with last_updated note

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Add `lifecycle_and_state` section to AdvisorIntelligence only | ModelPortfolios is simpler (fewer state interactions); AI has complex multi-tab state that the DE must track for task order coordination |
| Add `unused_tabs` as separate section from `tabs` | Separates what is functional from what is present but unwired — prevents future confusion when issuing task orders |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml` | Upgraded AdvisorIntelligence section to full-fidelity | Yes — `5efb15f4` |

---

## Blockers

None. The previous session blocker (0.4.2 page_inventory.xml missing) is resolved.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

pod_inventory.xml is now at 100% fidelity for both pod pages. AdvisorIntelligence section
sourced from the 0.4.2_RD page_inventory.xml (produced 2026-03-02). Both RD deliverables are
complete. Wave 3 DS data_contract.xml issuance is now unblocked for the ClientPlatform pod.

---

## Next Steps

1. **Await Wave 3 DS task order from CTO/COO** — DS can now issue data_contract.xml for
   ClientPlatform. DS needs to trace: getPartnerAnalytics -> bd-portal-publisher Lambda -> S3;
   getAUMMetrics -> opal-portal-data-proxy -> SmartX DynamoDB.

2. **Monitor 0.4.2_RD_AdvisorIntelligence task order status** — The SA-issued page_inventory
   task order is still marked `pending` even though the deliverable was produced. Either 0.4.2
   should mark it `complete` themselves, or flag to SA for cleanup.

**Files to touch next:**
- None required immediately. Waiting on Wave 3 DS task order.

**Do NOT:**
- Issue Wave 3 DS task orders without CTO/COO direction — that is SA responsibility
- Modify any portal source files (no active code task orders)


### 0.4.0_DE_ClientPlatform -- Pending Task Orders

#### advisor_intelligence_completion.md

# Task Order: AdvisorIntelligence DE Completion — 0.4.0_DE_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-de-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Drive completion of the AdvisorIntelligence page to v1.0 shippable state.
    DE responsibilities: leaderboard sort stability investigation (I2), review
    gate for all RD deliverables before DT pushes, NMNC/NMEC classification
    acknowledgment for DS (A2 gate), and Books tab coordination (G — blocked by thread).
    DE session logs are MANDATORY and are the primary status signal for COO tracking.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</ref>
    <ref>portal/src/pages/AdvisorIntelligence/</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="review">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM I2 — Leaderboard sort stability investigation + fix       -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="I2.1">
      Investigate the leaderboard sort stability issue:
        (a) Frontend: check whether JS .sort() on equal NNA values is stable.
            Read AdvisorsTab.tsx sort logic — if there is no secondary sort key
            for ties, add name as a stable tiebreaker.
        (b) Data: check architect_leaderboard.json S3 output — confirm the rank
            field is correctly set and entries are pre-sorted by rank in the publisher.
      Determine root cause (a), (b), or both.
    </requirement>
    <requirement id="I2.2">
      If (a) — frontend sort fix: implement stable sort in AdvisorsTab.tsx.
        Use: .sort((a, b) => a.nna !== b.nna ? a.nna - b.nna : a.name.localeCompare(b.name))
        or equivalent. Commit the fix.
      If (b) — data fix: document the publisher sort bug in your session log and
        file a follow-up item in your next steps for DS + DT to address via script
        update and Lambda deploy.
      If both: fix the frontend sort now; flag the data issue separately.
    </requirement>
    <requirement id="I2.3">
      After investigation, update pod_inventory.xml to reflect the current leaderboard
      sort behavior (resolved vs. open).
    </requirement>

    <!-- ================================================================ -->
    <!-- PATTERN 0 THREAD PARTICIPATION — A1+A2 and A3                   -->
    <!-- ================================================================ -->
    <requirement id="thread.1">
      You are a participant in two Pattern 0 alignment threads. These threads run
      BEFORE DS writes any code for A1, A2, and A3. Your role in each:

      Thread 1 (2026-03-03-continuous-nna-cla-alignment):
        After DS describes available gold layer data, specify:
        - The TypeScript interface name(s) and shape the portal will use for adv_drill
        - The TypeScript interface name(s) and shape for cla_timeseries
        - The NMNC/NMEC definition your portal types currently expect
          (check header_metrics.json CLA structure vs what DS proposes)
        - Any query key or endpoint path change needed in advisor-intelligence.ts

      Thread 2 (2026-03-03-advisors-stacked-bar-alignment):
        After DS describes what script 10 can produce, specify:
        - The TypeScript interface for the stacked bar data per period
        - The TypeScript interface for the rolling 1Y series
        - How the period toggle maps to data keys
        - Outflow encoding requirement from a portal typing perspective

      The thread receipts are the binding interface specs. Your task orders for
      C2, C4, and 4C (issued to RD) reference these receipts. Do NOT finalize
      those stream requirements before the receipts are available.
    </requirement>

    <!-- ================================================================ -->
    <!-- RD REVIEW GATE — all streams before DT push                      -->
    <!-- ================================================================ -->
    <requirement id="review.1">
      You are the QA review gate for all RD (0.4.2_RD) commits before DT pushes to DEV.
      Review each stream as RD completes it:
        - C1 (GEO continuous): verify drill interaction works correctly, breadcrumb is clear
        - C3 (CLA snapshot): verify two-color NMNC/NMEC labels are accurate and match header_metrics.json field values
        - H (portal primitives refactor): verify no visual regression, panel structure is correct
        - I (Top Performers): verify rank clarity, period toggle updates rankings
        - C2, C4, 4C: review when RD signals completion (after DT B1/B2 deploys)
      Signal DT to push to DEV only after you have reviewed and approved.
    </requirement>
    <requirement id="review.2">
      After each RD stream you review, note it in your mandatory session log:
        - Stream reviewed, what you found, any corrections sent back to RD, approval status
      This is your primary status reporting mechanism to COO.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM G — Books tab coordination (BLOCKED by Stream D thread)   -->
    <!-- ================================================================ -->
    <requirement id="G.1">
      BLOCKED: Do not begin Books tab wiring until Stream D thread completes.
      When thread receipt lands in your threads/ folder, read the Books design brief at:
        docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Your role for Books tab: API wiring (hook up L2/L3/L4 endpoints), auth gating
      logic (admin vs advisor view), and component structure — RD owns visual layout.
    </requirement>
    <requirement id="G.2">
      Auth gating for Books tab:
        - Admin (userRole === 'admin'): show advisor selector dropdown (all advisors)
        - Advisor: land directly on their own book — no dropdown, no selection
        - Use existing useAuth pattern for isInternal() / isDev() for L1 gating
        - Advisor identity resolution (JWT userId -> advisor name): implement ONLY after
          DS A5 investigation confirms the opal-users-v2 -> gold layer mapping exists.
          Do not assume the mapping exists until DS confirms.
    </requirement>
    <requirement id="G.3">
      Update pod_inventory.xml when Books tab API endpoints are wired.
      The Books tab section in pod_inventory.xml is currently missing — add it.
    </requirement>

    <!-- ================================================================ -->
    <!-- ONGOING — Session log mandate                                     -->
    <!-- ================================================================ -->
    <requirement id="log.1">
      DE session logs are MANDATORY. Write a session log for EVERY work session at:
        org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-03/{scope_action}.md
      Minimum sections: Objective, Work Completed, Decisions Made, Files Modified,
      Blockers, Current State, Next Steps.
      Include portal DEV commit hashes in header and Files Modified table.
    </requirement>
    <requirement id="log.2">
      Your first session log is also the pre-flight signal for COO to schedule
      the Books design thread (Stream D). COO cannot run the thread until you have
      at least one session log (O3 constraint in THREAD_KNOWLEDGE.md).
      Write your first session log after your initial orientation, before beginning I2.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">I2: Leaderboard sort root cause identified; frontend fix committed if applicable; data issue flagged if applicable.</criterion>
    <criterion id="2">A2-gate: NMNC/NMEC classification acknowledged in writing in session log before DS commits cla_timeseries.</criterion>
    <criterion id="3">All RD streams reviewed and documented in session log before DT pushes each stream to DEV.</criterion>
    <criterion id="4">Session log written for every work session (mandatory — no exceptions).</criterion>
    <criterion id="5">pod_inventory.xml updated for I2 resolution and Books tab endpoint wiring (post-thread).</criterion>
    <criterion id="6">Books tab auth gating wired and functional after DS A5 confirms mapping (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Session logs are MANDATORY for DE — not optional. This is a system-wide rule, not just for this task order.</constraint>
    <constraint>Do NOT push to DEV yourself. DT owns all pushes. Your role: review and approve.</constraint>
    <constraint>Do NOT implement Books tab auth gating until DS A5 confirms opal-users-v2 -> gold layer mapping exists.</constraint>
    <constraint>Do NOT use emojis in any code or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>NOTE: You have no prior session logs. Write your first log immediately after orientation — it is the trigger for the COO to schedule the Books thread.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="A2-gate requires DS to send classification logic for acknowledgment"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="G blocked until thread completes"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="advisor_intelligence_completion" status="pending" note="Review gate on all C/H/I/G streams"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Leaderboard sort fix in AdvisorsTab.tsx (if frontend root cause)</deliverable>
    <deliverable type="document">Mandatory session log for every work session — first log triggers COO thread scheduling</deliverable>
    <deliverable type="document">Written NMNC/NMEC classification acknowledgment in session log</deliverable>
    <deliverable type="document">RD stream review notes in session log for each reviewed stream</deliverable>
    <deliverable type="commit">Books tab API wiring + auth gating (post-thread, per design brief)</deliverable>
    <deliverable type="commit">pod_inventory.xml updated for I2 and Books tab</deliverable>
  </deliverables>
</task_order>
```


### 0.4.0_DE_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DE_ClientPlatform

5efb15f4 0.4.0_DE_ClientPlatform: upgrade pod_inventory.xml AdvisorIntelligence to full-fidelity from 0.4.2 RD audit
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
0033f9ca 0.4.0_DE_ClientPlatform: fix Daily AUA Analysis bottom margin to 70
e70b9730 0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts (corrected values)
4bda06a8 0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts

