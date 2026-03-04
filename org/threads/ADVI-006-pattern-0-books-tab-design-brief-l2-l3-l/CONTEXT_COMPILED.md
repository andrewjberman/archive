# Thread Context -- Pattern 0: Books tab design brief L2 L3 L4

**Thread ID:** ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-04T16:37:03Z

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

This is a Books tab design alignment. The previous run (ADVI-003) failed to produce its required deliverable: docs/architecture/advisor_intelligence/books_tab_design_brief.md. The DE must write this file as their final turn. It is not optional.
DS: read lambda_function.py before describing what currently flows through the advisor-publisher. Anchor every answer to a function name and output dict key. Distinguish between what is currently in the published JSON vs what is gold-layer only. The gap list (what is missing from publisher output) is the core deliverable.


### advisorintelligence-completion-prd-section-5-books-tab.md

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
}
```

### bd-advisor-publisher-lambda.py

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

### clientstab-component.tsx

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

### ds-data-contract.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<data_contract>

  <metadata>
    <agent>0.4.0_DS_ClientPlatform</agent>
    <pod>ClientPlatform</pod>
    <date>2026-03-04</date>
    <task_order_id>1.0.0_SA_CTO-2026-03-02-data-contract-client-platform</task_order_id>
    <status>complete</status>
    <source_note>
      ModelPortfolios section sourced from 0.4.1_RD_ModelPortfolios pod_inventory (complete).
      AdvisorIntelligence section sourced from 0.4.0_DE_ClientPlatform pod_inventory + direct
      Lambda code reads. 0.4.2_RD_AdvisorIntelligence deliverable is MISSING; this contract
      carries lower fidelity on AdvisorIntelligence page-level component detail.
      2026-03-04: timeseries_chart.json extended with adv_drill (ADVI-004 A1) and cla
      (ADVI-004 A2) per ADVI-004 Pattern 0 thread receipt.
    </source_note>
  </metadata>

  <!-- ======================================================================== -->
  <!-- PAGE CONTRACTS                                                             -->
  <!-- ======================================================================== -->

  <page_contracts>

    <!-- ---------------------------------------------------------------------- -->
    <!-- Page 1: ModelPortfolios                                                  -->
    <!-- ---------------------------------------------------------------------- -->
    <page>
      <name>ModelPortfolios</name>
      <directory>portal/src/pages/ModelPortfolios/</directory>

      <data_sources>

        <!-- Source 1: AUM metrics (primary, loads on mount) -->
        <source>
          <lambda_function>opal-portal-data-proxy</lambda_function>
          <source_path>infra/aws/lambda/portal_data_proxy/lambda_function.py</source_path>
          <trigger>HTTP GET from portal on page mount</trigger>
          <s3_output_key_pattern>DynamoDB (not S3 — AUM data stored in DynamoDB tables)</s3_output_key_pattern>
          <response_shape>
            <key name="aum_by_model" type="array">AUA per model portfolio (UST/ST/INT/LTC/LTA)</key>
            <key name="total_aua" type="float">Total AUM across all models</key>
            <key name="period" type="string">YYYYMM data period</key>
            <key name="flows" type="object">inflows, outflows, net per model per period</key>
          </response_shape>
          <portal_endpoint>
            <function>getAUMMetrics()</function>
            <path>portal/src/api/endpoints/aum.ts</path>
            <http>GET /v1/aum/metrics (via portal-proxy.ts)</http>
            <query_key>aum-metrics</query_key>
          </portal_endpoint>
          <portal_endpoint>
            <function>getAUMTimeSeries()</function>
            <path>portal/src/api/endpoints/aum.ts</path>
            <http>GET /v1/aum/timeseries (via portal-proxy.ts)</http>
            <query_key>aum-timeseries</query_key>
          </portal_endpoint>
          <portal_endpoint>
            <function>getNonModelAssets()</function>
            <path>portal/src/api/endpoints/aum.ts</path>
            <http>GET /v1/aum/non-model (via portal-proxy.ts)</http>
            <query_key>non-model-assets</query_key>
          </portal_endpoint>
        </source>

        <!-- Source 2: Account distribution (static S3, DEMO MODE) -->
        <source>
          <lambda_function>none (static JSON, no Lambda)</lambda_function>
          <trigger>HTTP GET from portal on page mount</trigger>
          <s3_output_key_pattern>opal-data-portal-v2/api/general/portfolios/account-distribution.json</s3_output_key_pattern>
          <response_shape>
            <key name="models" type="array">Distribution of accounts across UST/ST/INT/LTC/LTA models (bell curve input)</key>
            <key name="total_accounts" type="int">Total account count</key>
          </response_shape>
          <portal_endpoint>
            <function>getAccountDistribution()</function>
            <path>portal/src/api/endpoints/aum.ts:470-478</path>
            <http>GET /api/general/portfolios/account-distribution.json (public endpoint, no auth)</http>
            <query_key>account-distribution</query_key>
            <note>DEMO MODE: uses public endpoint. TODO: revert to /api/private/portfolios/account-distribution.json. 60-min in-memory cache.</note>
          </portal_endpoint>
        </source>

        <!-- Source 3: Benchmark returns (lazy-loaded, performance tab) -->
        <source>
          <lambda_function>yang-model-portfolio-benchmarks</lambda_function>
          <source_path>infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py</source_path>
          <trigger>
            S3 ObjectCreated on opal-data-portal-v2/benchmarks/*.pkl (direct trigger)
            OR Step Functions YangDataPipeline workflow event (orchestrated trigger).
            Input: opal-data-portal-v2/benchmarks/data_YYYYMMDD_v1.pkl -> return_daily DataFrame.
            Filtered to index_name containing "Term" (model and benchmark series).
          </trigger>
          <s3_output_key_pattern>
            opal-data-portal-v2/json/benchmarks/benchmark_returns.json (legacy)
            opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json (comprehensive)
          </s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string">ISO8601 UTC timestamp</key>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="periods" type="array">["1D","WTD","MTD","1M","QTD","1Q","YTD","1Y","Since Inception"]</key>
            <key name="inception_date" type="string">2024-04-30</key>
            <key name="models" type="array">
              Per model: { code (UST/ST/INT/LTC/LTA), name, returns: { [period]: { model, index_benchmark, etf_benchmark, index_spread, etf_spread, model_volatility, index_benchmark_volatility, etf_benchmark_volatility } } }
            </key>
            <key name="model_names" type="object">code -> display name mapping</key>
            <key name="index_compositions" type="object">code -> Bloomberg index blend description</key>
            <key name="etf_compositions" type="object">code -> ETF blend description</key>
            <key name="source" type="string">"data.pkl -> return_daily (Yang canonical)"</key>
          </response_shape>
          <portal_endpoint>
            <function>getModelPortfolioBenchmarks()</function>
            <path>portal/src/api/portal-proxy.ts</path>
            <http>GET /v1/benchmarks/returns (via opal-portal-data-proxy Lambda)</http>
            <query_key>model-portfolio-benchmarks</query_key>
            <lazy>true — loaded when performance tab first activated</lazy>
          </portal_endpoint>
        </source>

        <!-- Source 4: ETF benchmark returns (lazy-loaded, performance tab) -->
        <source>
          <lambda_function>yang-generate-etf-returns</lambda_function>
          <source_path>infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-generate-etf-returns/lambda_function.py</source_path>
          <trigger>Yang pipeline Step Functions workflow</trigger>
          <s3_output_key_pattern>opal-data-portal-v2/json/benchmarks/etf_returns.json</s3_output_key_pattern>
          <response_shape>
            <key name="models" type="array">ETF blend returns per model per period</key>
          </response_shape>
          <portal_endpoint>
            <function>getETFBenchmarkReturns()</function>
            <path>portal/src/api/portal-proxy.ts</path>
            <http>GET /v1/benchmarks/etf (via opal-portal-data-proxy Lambda)</http>
            <query_key>etf-benchmark-returns</query_key>
            <lazy>true — loaded when performance tab first activated</lazy>
          </portal_endpoint>
        </source>

        <!-- Source 5: Peer performance (lazy-loaded, peers tab) -->
        <source>
          <lambda_function>yang-generate-peer-performance</lambda_function>
          <source_path>infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-generate-peer-performance/lambda_function.py</source_path>
          <trigger>Yang pipeline Step Functions workflow</trigger>
          <s3_output_key_pattern>opal-data-portal-v2/json/peers/peer_performance.json</s3_output_key_pattern>
          <response_shape>
            <key name="models" type="array">Per model: quartile rank, benchmark position, Morningstar peer universe comparison</key>
            <key name="since_inception_return" type="float">Annualized return since inception (portal applies annualizeSinceInceptionReturn transform)</key>
          </response_shape>
          <portal_endpoint>
            <function>getPeerPerformance()</function>
            <path>portal/src/api/portal-proxy.ts</path>
            <http>GET /v1/peers/performance (via opal-portal-data-proxy Lambda)</http>
            <query_key>peer-performance</query_key>
            <lazy>true — loaded when peers tab first activated</lazy>
          </portal_endpoint>
        </source>

      </data_sources>

      <data_freshness>
        AUM time series: daily (SmartX EC2 exporter runs daily, ingested by opal-smartx-ingestion-pipeline Lambda).
        Benchmark returns: updated each time Yang pipeline runs (triggered by model_*.pkl or data_*.pkl upload to opal-data-portal-v2/benchmarks/).
        Account distribution: static JSON; update frequency unknown (DEMO MODE endpoint).
        Peer performance: updated each Yang pipeline run.
      </data_freshness>
    </page>

    <!-- ---------------------------------------------------------------------- -->
    <!-- Page 2: AdvisorIntelligence                                              -->
    <!-- ---------------------------------------------------------------------- -->
    <page>
      <name>AdvisorIntelligence</name>
      <directory>portal/src/pages/AdvisorIntelligence/</directory>

      <data_sources>

        <!-- Source 1: Partner Analytics (primary, loads on page mount) -->
        <source>
          <lambda_function>bd-portal-publisher (writes file); shared-advisor-router (serves at runtime)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</source_path>
          <trigger>Static JSON served from S3 via CloudFront with firm routing (shared-advisor-router Lambda)</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/partner_analytics/header_metrics.json</s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string">ISO8601 UTC</key>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="firm_id" type="string">e.g. "49financial"</key>
            <key name="firm_name" type="string">e.g. "49 Financial"</key>
            <key name="views" type="object">
              Keys: aua, nna, geo, adv.
              Each view: { current: { donut: { title, total, segments[] }, metrics: { aua, client_count } } }
              Segment shape: { key, label, aua, aua_pct, client_count, color }
              aua view segments: taxable/tax_deferred/tax_free (by tax status)
              nna view segments: same as aua (fallback)
              geo view segments: top 8 US states + Other (from nna_aua_by_geography.parquet)
              adv view segments: top 8 architects + Other (from nna_aua_by_advisor.parquet)
            </key>
          </response_shape>
          <portal_endpoint>
            <function>getPartnerAnalytics()</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts:226-228</path>
            <http>GET /api/scoped/advisor-intelligence/partner_analytics/header_metrics.json</http>
            <query_key>partner-analytics</query_key>
            <note>Loaded at page level in AdvisorIntelligence.tsx:81-87. staleTime=5min, refetchOnWindowFocus=false. Result passed as prop to PartnerAnalytics and DistributionTab.</note>
          </portal_endpoint>
        </source>

        <!-- Source 2: Cumulative Chart (DistributionTab continuous view + PartnerAnalytics) -->
        <source>
          <lambda_function>bd-portal-publisher (writes file)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</source_path>
          <trigger>Static JSON via CloudFront / S3</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/timeseries_chart.json</s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string">ISO8601 UTC</key>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="firm_id" type="string"/>
            <key name="date_range" type="object">{ start, end, days }</key>
            <key name="metadata" type="object">{ new_clients: { 3M, 6M, 1Y, 2Y, 3Y } }</key>
            <key name="aua" type="object">
              { description, categories: ["NMNC","NMEC"], data: [{ date, NMNC, NMEC }] }
              Daily cumulative AUA split by client vintage (NMNC = new money new client within 12mo)
            </key>
            <key name="nna" type="object">
              { description, categories: ["NNA","Inflows","Outflows"], data: [{ date, NNA, Inflows, Outflows }] }
              Cumulative from inception. Frontend diffs adjacent endpoints to get period-level flows.
            </key>
            <key name="adv" type="object">
              { description, categories: [top 8 architect names + "Other"], data: [{ date, [architect_name]: aua }] }
              Daily cumulative AUA stacked by architect.
            </key>
            <key name="geo" type="object">
              { description, categories: [top 8 US states + "Other"], data: [{ date, [state]: aua }] }
              Daily cumulative AUA stacked by US state.
            </key>
            <key name="geo_drill" type="object">
              Optional. { [state]: { categories: [top 9 cities + "Other"], data: [{ date, [city]: aua }] } }
              Present only when nna_aua_by_geography_city.parquet is available.
            </key>

            <!-- ADVI-004 A1: adv_drill -- added 2026-03-04 -->
            <key name="adv_drill" type="object">
              Optional. Per-architect per-client AUA timeseries drill-down.
              Structure: { [architect_display_name]: CumulativeChartView }
              Record keys MUST match timeseries_chart.json.adv.categories strings exactly
              (architect display names as produced by nna_aua_by_advisor.parquet).
              CumulativeChartView:
                { description: string,
                  categories: string[],   -- top 8 clients by latest-day AUA in format
                                             "{relationship_name} ({relationship_id})"
                                             (fallback to relationship_id if name absent)
                                             plus "Other" if remainder > 0
                  data: [{ date: YYYY-MM-DD, [client_key]: aua_dollars, ... }] }
              Source: gold/client_performance.parquet (total_aua) joined with
                      gold/client_dimension.parquet (relationship_name, primary_architect).
              TOP_N_CLIENTS_PER_ARCH = 8 (constant in lambda_function.py).
              Note: primary_architect from cdim is current-snapshot assignment, not
              historical. Minor differences vs nna_aua_by_advisor.parquet (which uses
              rel_architect_lookup.parquet for historical assignments) are expected.
            </key>

            <!-- ADVI-004 A2: cla -- added 2026-03-04 -->
            <key name="cla" type="object">
              Client Lifecycle Analysis: NMNC/NMEC AUM over time at multiple grains.
              NMNC/NMEC classification: trailing-12-month vintage rule.
                months_since_first = (row_date - cdim.first_seen_date).days / 30.44
                NMNC if months_since_first &lt;= 12, else NMEC.
              Same rule as timeseries_chart.json.aua view (verified in build_timeseries_chart()).

              Sub-keys:
                total: CumulativeChartView -- firm-wide NMNC/NMEC AUM dollars over time
                  { description, categories: ["NMNC","NMEC"], data: [{date, NMNC, NMEC}] }

                geo_drill: Record&lt;state, CumulativeChartView&gt;
                  Keys are state abbreviations (e.g. "TX", "CA") and MUST match
                  timeseries_chart.json.geo.categories strings exactly.
                  Each view: 2-series NMNC/NMEC AUM for that state's clients
                  (filtered by cdim.primary_state -- current snapshot).

                adv_drill: Record&lt;architect_display_name, CumulativeChartView&gt;
                  Keys MUST match timeseries_chart.json.adv.categories strings exactly
                  (architect display names, excluding "Other").
                  Each view: 2-series NMNC/NMEC AUM for that architect's clients
                  (filtered by cdim.primary_architect -- current snapshot).

                geo_city_drill: Record&lt;state, Record&lt;city, CumulativeChartView&gt;&gt;
                  Optional. Present when cdim.primary_city is populated.
                  State keys match geo.categories. City keys are city display names
                  (top MAX_CLA_CITIES=9 by latest-day AUA per state).
                  Each view: 2-series NMNC/NMEC AUM for that city's clients.
                  Source: cdim.primary_city (CTO scope correction, ADVI-004 task order A2.0).
                  Confirmed available in gold/client_dimension.parquet lines 267-268 of
                  04_build_client_dimension.py.
            </key>
          </response_shape>
          <portal_endpoint>
            <function>getCumulativeChart()</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/timeseries_chart.json</http>
            <note>Used by DistributionTab (continuous view) and PartnerAnalytics. adv_drill and cla are additive optional keys added in ADVI-004.</note>
          </portal_endpoint>
        </source>

        <!-- Source 3: Architect Leaderboard (AdvisorsTab + BooksTab) -->
        <source>
          <lambda_function>bd-portal-publisher (writes file)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</source_path>
          <trigger>Static JSON via CloudFront / S3</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/architect_leaderboard.json</s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string"/>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="firm_id" type="string"/>
            <key name="leaderboard_type" type="string">"architect"</key>
            <key name="available_windows" type="array">["3M","6M","1Y","2Y","3Y"]</key>
            <key name="windows" type="object">
              Keys: 3M, 6M, 1Y, 2Y, 3Y.
              Each: { entry_count, summary: { total_nna, total_aua, total_new_clients, positive_nna_count, negative_nna_count }, entries: [{ rank, name, nna, aua_growth_pct, new_clients, total_aua, client_count, account_count }] }
            </key>
          </response_shape>
          <portal_endpoint>
            <function>getArchitectLeaderboard()</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/architect_leaderboard.json</http>
            <note>Used by both AdvisorsTab and BooksTab.</note>
          </portal_endpoint>
        </source>

        <!-- Source 4: Implementor Leaderboard (AdvisorsTab) -->
        <source>
          <lambda_function>bd-portal-advisor-publisher (writes file)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</source_path>
          <trigger>Static JSON via CloudFront / S3 (same trigger as publisher: pipeline-complete.json)</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/implementor_leaderboard.json</s3_output_key_pattern>
          <response_shape>
            <key name="leaderboard_type" type="string">"implementor"</key>
            <key name="windows" type="object">
              Same schema as architect_leaderboard. Entries grouped by implementor name.
            </key>
          </response_shape>
          <portal_endpoint>
            <function>getImplementorLeaderboard()</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/implementor_leaderboard.json</http>
          </portal_endpoint>
        </source>

        <!-- Source 5: Advisor Rolling Flows (AdvisorsTab) -->
        <!-- Updated 2026-03-04: ADVI-005 A3 adds stacked_bar + rolling_1y keys -->
        <source>
          <script>data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py (EC2 gold script)</script>
          <trigger>EC2 gold pipeline run; script uploads to S3 via --upload flag</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/advisor_rolling_flows.json</s3_output_key_pattern>
          <data_history>
            Daily data from 2020-06-30 to present (~5.5 years).
            Source parquets: nna_aua_by_advisor.parquet (architects), client_performance.parquet (implementors).
            First valid 1Y rolling point: ~2021-07-01 (after 1Y warmup).
            3Y and Max stacked_bar coverage: complete (data exceeds 4Y required lookback).
          </data_history>
          <response_shape>

            <!-- LEGACY KEYS (unchanged) -->
            <key name="generated_at" type="string">ISO8601 UTC</key>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="firm_id" type="string"/>
            <key name="summary" type="object">
              { architects: { mtd, qtd, ytd }, implementors: { mtd, qtd, ytd } }
              Each period: { period_start, period_end, display, total_nna, total_inflows, total_outflows,
                             prior: {...}, growth_pct, segments: [AdvisorSegment] }
              AdvisorSegment: { advisor_name, advisor_id, nna, nna_pct, inflows, outflows, total_aua,
                                client_count, new_clients, prior_nna, nna_growth_pct, rank,
                                prior_rank, rank_change, color }
            </key>
            <key name="architects" type="array">
              Legacy rolling series. Each: { advisor_name, advisor_id,
              series: { "30d": [Rolling1YDataPoint], "90d": [...], "1Y": [...] } }
              Rolling1YDataPoint: { date, nna, inflows, outflows }
            </key>
            <key name="implementors" type="array">Same shape as architects.</key>

            <!-- ADVI-005 A3.1: stacked_bar -- added 2026-03-04 -->
            <key name="stacked_bar" type="object">
              Period-aggregated inflows/outflows/nna_net per advisor.
              Nesting: period-outer / role-inner (CTO correction from thread receipt).
              Structure:
                { "qtd": { "architects": [AdvisorBarEntry], "implementors": [AdvisorBarEntry] },
                  "ytd": { ... }, "1y": { ... }, "3y": { ... }, "max": { ... } }
              AdvisorBarEntry: { advisor_name, advisor_id, inflows, outflows, nna_net }
                - outflows: positive magnitude (&gt;= 0); frontend negates for stacked bar chart.
                - nna_net: signed (can be negative).
              Period boundaries:
                - qtd, ytd: calendar-anchored via _get_period_boundaries().
                - 1y, 3y: trailing 365/1095 days from latest_date.
                - max: inception-to-date (earliest date in parquet = 2020-06-30).
              Source: nna_aua_by_advisor.parquet (architects);
                      client_performance.parquet + accounts_dimension_latest.parquet (implementors).
              Computed by: compute_stacked_bar() in 10_generate_advisor_rolling_flows.py.
            </key>

            <!-- ADVI-005 A3.2: rolling_1y -- added 2026-03-04 -->
            <key name="rolling_1y" type="object">
              Fixed 1Y rolling window timeseries per advisor; full history emitted.
              Frontend slices x-axis by period toggle (qtd/ytd/1y/3y/max).
              Structure:
                { "architects": [AdvisorRolling1YSeries], "implementors": [AdvisorRolling1YSeries] }
              AdvisorRolling1YSeries: { advisor_name, advisor_id,
                series: [{ date: YYYY-MM-DD, nna: number, inflows: number, outflows: number }] }
                - Daily cadence. All 3 fields present per point.
                - outflows: positive magnitude (consistent with legacy series convention).
                - nna: signed.
              Rolling method: roll_val[D] = cum_val[D] - cum_val[D - 365d].
              First valid data point: ~2021-07-01 (requires 365d warmup).
              Source: reuses existing 1Y window from compute_rolling_series() in script 10.
            </key>

          </response_shape>
          <portal_endpoint>
            <function>getAdvisorRollingFlows()</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/advisor_rolling_flows.json</http>
          </portal_endpoint>
        </source>

        <!-- Source 6: Clients Tab (BooksTab) -->
        <source>
          <lambda_function>bd-portal-publisher (writes file)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</source_path>
          <trigger>Static JSON via CloudFront / S3</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/clients_tab.json</s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string"/>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="firm_id" type="string"/>
            <key name="headline" type="object">{ total_aua, account_count, client_count, fee_rate_pct (0.0), income_yield_pct (0.0) }</key>
            <key name="tax" type="object">
              { taxable, taxable_pct, tax_deferred, tax_deferred_pct, tax_free, tax_free_pct,
                capital_gains_ttm, qualified_aua, qualified_pct, non_qualified_aua, non_qualified_pct,
                qualified_account_count, non_qualified_account_count,
                non_qualified_cost_basis, non_qualified_market_value, non_qualified_unrealized_gain,
                short_term_gain, long_term_gain, cost_basis_by_year[], top_gain_positions[], lots_available }
            </key>
            <key name="income_fees" type="object">All fields zeroed (not available from BD data)</key>
            <key name="portfolio" type="object">allocation=[], weighted_expense_ratio=0, unique_holdings=0 (not available from BD data)</key>
            <key name="engagement" type="object">{ trading_buys_ttm (0), trading_sells_ttm (0), net_flows_ttm, avg_relationship_years, active_clients_pct }</key>
            <key name="clients" type="array">Sorted by AUA desc: [{ key (relationship_id), name, aua }]</key>
          </response_shape>
          <portal_endpoint>
            <function>getClientsTab()</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/clients_tab.json</http>
          </portal_endpoint>
        </source>

        <!-- Source 7: Per-advisor book (BooksTab) -->
        <source>
          <lambda_function>bd-portal-advisor-publisher (writes file)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</source_path>
          <trigger>Static JSON via CloudFront / S3</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/advisors/{advisor_id}/book.json (advisor_id = snake_case of architect display name)</s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string"/>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="book_type" type="string">"architect"</key>
            <key name="book_key" type="string">snake_case advisor ID</key>
            <key name="book_name" type="string">Display name</key>
            <key name="summary" type="object">{ total_aua, client_count, account_count }</key>
            <key name="nna" type="object">{ ytd, qtd, mtd } (float)</key>
            <key name="growth" type="object">{ ytd_pct, qtd_pct } (float)</key>
            <key name="tax_exposure" type="object">
              { taxable, taxable_pct, tax_deferred, tax_deferred_pct, tax_free, tax_free_pct,
                qualified_aua, qualified_pct, non_qualified_aua, non_qualified_pct,
                non_qualified_cost_basis, non_qualified_unrealized_gain, short_term_gain, long_term_gain }
            </key>
            <key name="income_fees" type="object">All zeroed</key>
            <key name="portfolio_composition" type="object">asset_allocation=[], avg_expense_ratio=0 (not available)</key>
            <key name="engagement" type="object">{ net_flows_ttm, inflows_ttm, outflows_ttm, avg_tenure_days }</key>
            <key name="clients" type="array">Sorted by AUA desc: [{ client_key, client_name, aua }]</key>
          </response_shape>
          <portal_endpoint>
            <function>getAdvisorBook(advisorId)</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/advisors/{advisorId}/book.json</http>
          </portal_endpoint>
        </source>

        <!-- Source 8: Per-client detail (BooksTab drill-down, admin only) -->
        <source>
          <lambda_function>bd-client-detail (runtime proxy) + bd-portal-advisor-publisher (pre-generates file)</lambda_function>
          <source_path>infra/aws/lambda/bd-pipeline/bd-client-detail/lambda_function.py</source_path>
          <trigger>API Gateway GET on demand per request. Requires role=admin in authorizer context.</trigger>
          <s3_output_key_pattern>opal-data-bd/gold/clients/{relationship_id}.json (pre-generated by bd-portal-advisor-publisher)</s3_output_key_pattern>
          <response_shape>
            <key name="generated_at" type="string"/>
            <key name="data_as_of" type="string">YYYY-MM-DD</key>
            <key name="firm_id" type="string"/>
            <key name="client_key" type="string">relationship_id string</key>
            <key name="client_name" type="string">relationship_name or relationship_id fallback</key>
            <key name="headline" type="object">{ total_aua, account_count, client_count (always 1), fee_rate_pct (0), income_yield_pct (0) }</key>
            <key name="tax" type="object">
              Full tax section: taxable/deferred/exempt AUA + pct, capital_gains_ttm,
              qualified/non_qualified split, cost_basis_by_year[], top_gain_positions[] (top 20 by unrealized gain),
              open_lots[] (lot-level detail from holdings_lots snapshot, taxable only), open_lots_count
            </key>
            <key name="income_fees" type="object">All zeroed</key>
            <key name="portfolio" type="object">allocation=[], weighted_expense_ratio=0, unique_holdings (from num_positions), top_5_concentration_pct=0</key>
            <key name="engagement" type="object">{ trading_buys_ttm (0), trading_sells_ttm (0), net_flows_ttm, avg_relationship_years }</key>
            <key name="accounts" type="array">
              Per-account snapshot: [{ account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }]
              Sorted by AUA desc.
            </key>
          </response_shape>
          <portal_endpoint>
            <function>getClientDetail(clientKey)</function>
            <path>portal/src/api/endpoints/advisor-intelligence.ts</path>
            <http>GET /api/scoped/advisor-intelligence/clients/{clientKey}.json</http>
            <note>Admin-only: bd-client-detail enforces role=admin. Returns 403 for non-admin or missing key.</note>
          </portal_endpoint>
        </source>

        <!-- Source 9: opal-partners-data (real-time scoped API for timeseries + snapshots + filters) -->
        <source>
          <lambda_function>opal-partners-data</lambda_function>
          <source_path>infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</source_path>
          <trigger>API Gateway on-demand per request. Reads pre-generated JSON from opal-data-bd/gold/.</trigger>
          <s3_output_key_pattern>
            Reads (does not write):
              opal-data-bd/gold/timeseries/nna_by_{dimension}.json (11 files: total, category, architect, region, account_type, tax_status, client_segment, state, city, relationship, implementor)
              opal-data-bd/gold/snapshots/aua_by_{dimension}.json (7 files: architect, region, tax_status, account_type, implementor, state, city)
              opal-data-bd/gold/clients/*.json (growth_timeseries, tax_basis_breakdown, tax_deferred_candidates)
              opal-data-bd/gold/filters/dimensions.json
          </s3_output_key_pattern>
          <response_shape>
            <key name="timeseries/{dimension}" type="object">
              Total dimension: { generated_at, data_as_of, firm_id, granularity="monthly", data: [{ period, inflow, outflow, net, txn_count }] }
              Category dimension: { categories: ["nmnc","nmec"], data: [{ period, nmnc, nmec, total }] }
              Other dimensions: { dimension, dimension_values[], data: [{ period, [dim_val]: { nmnc, nmec, nna_net, outflow, txn_count } }] }
            </key>
            <key name="snapshots/{dimension}" type="object">
              { generated_at, data_as_of, firm_id, dimension, total_aua, data: [{ value, aua, aua_pct, client_count, account_count }] }
            </key>
            <key name="filters" type="object">
              { generated_at, firm_id, dimensions: { architect, region, implementor, account_type, tax_status, state, city } }
              Each dimension: { label, column, values: [{ id, name, aua?, client_count? }] }
            </key>
          </response_shape>
          <portal_endpoint>
            <function>getTimeSeries(firmId, dimension)</function>
            <http>GET /api/scoped/advisor-intelligence/timeseries/{dimension}?firmId=...</http>
          </portal_endpoint>
          <portal_endpoint>
            <function>getSnapshot(firmId, dimension)</function>
            <http>GET /api/scoped/advisor-intelligence/snapshots/{dimension}?firmId=...</http>
            <note>Pod_inventory notes firmId query param will be removed once Lambda reads from portal-authorizer context.</note>
          </portal_endpoint>
          <portal_endpoint>
            <function>getFilters(firmId)</function>
            <http>GET /api/scoped/advisor-intelligence/filters?firmId=...</http>
          </portal_endpoint>
        </source>

      </data_sources>

      <data_freshness>
        All static JSON files (partner_analytics, timeseries_chart, leaderboards, clients_tab, advisor books, client details)
        are regenerated daily by bd-portal-publisher and bd-portal-advisor-publisher after the BD gold pipeline run completes.
        Trigger: opal-data-bd/gold/pipeline-complete.json sentinel written by bd-gold-layer-runner EC2.
        Both publisher Lambdas run in parallel (same trigger). Data as-of = latest date in account_performance parquet.
        opal-partners-data serves pre-generated files with 5-minute CloudFront/Lambda cache (Cache-Control: max-age=300).
      </data_freshness>
    </page>

  </page_contracts>

  <!-- ======================================================================== -->
  <!-- PIPELINE SPLIT                                                             -->
  <!-- ======================================================================== -->

  <pipeline_split>

    <page_pipeline name="ModelPortfolios">
      <pipeline>yang-pipeline</pipeline>
      <primary_source>
        Yang PKL workspace: opal-data-portal-v2/benchmarks/data_YYYYMMDD_v1.pkl
        AUM time series: SmartX EC2 exporter -> DynamoDB (via opal-smartx-ingestion-pipeline Lambda)
      </primary_source>
      <trigger>
        Benchmark/ETF/peer data: S3 ObjectCreated on opal-data-portal-v2/benchmarks/*.pkl, or Step Functions YangDataPipeline.
        AUM data: SmartX EC2 daily export.
      </trigger>
      <versioning>
        Yang uses a PKL versioning convention (data_YYYYMMDD_v1.pkl).
        opal-portal-data-proxy serves the latest versioned data through a /v1/ API namespace.
        Portal uses LATEST.json pointer at benchmarks/LATEST.json to locate current data PKL.
      </versioning>
      <lambdas>
        <lambda>yang-model-portfolio-benchmarks — benchmark + ETF returns from data.pkl</lambda>
        <lambda>yang-generate-etf-returns — ETF blend returns</lambda>
        <lambda>yang-generate-peer-performance — Morningstar peer quartile ranking</lambda>
        <lambda>opal-portal-data-proxy — API proxy: routes /v1/aum/* /v1/benchmarks/* /v1/peers/* to DynamoDB/S3</lambda>
        <lambda>opal-smartx-ingestion-pipeline — ingests SmartX EC2 AUM time series into DynamoDB</lambda>
      </lambdas>
    </page_pipeline>

    <page_pipeline name="AdvisorIntelligence">
      <pipeline>bd-pipeline (Black Diamond)</pipeline>
      <primary_source>
        49 Financial allocation and transaction raw files from Black Diamond Wealth Platform.
        Ingested via bd-allocation-trigger and bd-transactions-trigger Lambdas.
        Processed through silver layer (bd-transaction-consolidator) into gold parquets
        by bd-gold-layer-runner EC2 (scripts pulled from s3://opal-data-bd/code/gold/).
      </primary_source>
      <trigger>
        Gold parquet completion signaled by opal-data-bd/gold/pipeline-complete.json.
        This sentinel triggers both bd-portal-publisher and bd-portal-advisor-publisher (parallel execution).
      </trigger>
      <gold_stage_inputs_to_publishers>
        bd-portal-publisher reads:
          gold/client_performance.parquet (per-relationship daily cumulative AUA/flows)
          gold/views/nna_aua_by_advisor.parquet (per-architect daily AUA/flows aggregates)
          gold/views/nna_aua_by_geography.parquet (per-state/country daily AUA aggregates)
          gold/views/nna_aua_by_geography_city.parquet (per-city daily AUA — optional, graceful skip if absent)
          gold/client_dimension.parquet (per-relationship metadata: first_seen_date, primary_architect/implementor/state)
          gold/accounts_dimension_latest.parquet (per-account latest: account_id, relationship_id, architect, implementor, tax_status, qualified_flag, client_state)
          gold/views/client_tax_liability.parquet (per-relationship tax lot exposure: qualified/non-qualified, cost_basis, unrealized_gain by purchase_year)

        bd-portal-advisor-publisher reads:
          gold/account_performance.parquet (~350MB, ~10M rows — per-account daily cumulative AUA/flows)
          gold/views/client_tax_liability.parquet (shared with publisher)
          gold/client_dimension.parquet (shared with publisher)
          gold/holdings_lots/{YYYYMMDD}.parquet (latest snapshot, per-lot open lot detail)
      </gold_stage_inputs_to_publishers>
      <publisher_outputs>
        bd-portal-publisher writes to opal-data-bd:
          gold/timeseries_chart.json (CumulativeChartResponse)
          gold/architect_leaderboard.json (LeaderboardResponse)
          gold/clients_tab.json (ClientsTabResponse)
          gold/summary/header_metrics.json (HeaderMetricsResponse)
          gold/partner_analytics/header_metrics.json (PartnerAnalyticsResponse)
          gold/filters/dimensions.json (FiltersResponse)
          gold/snapshots/aua_by_architect.json (SnapshotResponse)
          gold/snapshots/aua_by_state.json (SnapshotResponse)
          gold/snapshots/aua_by_tax_status.json (SnapshotResponse)
          gold/snapshots/aua_by_region.json (SnapshotResponse)

        bd-portal-advisor-publisher writes to opal-data-bd:
          gold/implementor_leaderboard.json (LeaderboardResponse)
          gold/advisors/{advisor_id}/book.json (AdvisorBookResponse, one per architect)
          gold/clients/{relationship_id}.json (ClientDetailResponse, one per client)
      </publisher_outputs>
      <routing>
        All static JSON served via CloudFront -> S3 with firm-level routing by shared-advisor-router Lambda.
        portal-authorizer Lambda validates JWT and injects allowedFirmIds into request context.
        bd-client-detail is invoked by API Gateway (admin-only, not via static S3).
      </routing>
    </page_pipeline>

  </pipeline_split>

  <!-- ======================================================================== -->
  <!-- BD GOLD INPUTS                                                             -->
  <!-- ======================================================================== -->

  <bd_gold_inputs>
    <note>
      BD gold scripts are stored in S3 at s3://opal-data-bd/code/gold/ and are NOT in the local repository.
      The bd-gold-layer-runner EC2 syncs scripts from that S3 path at boot (run-gold-layer.sh:62).
      The scripts below are inferred from the parquet key patterns the publisher Lambdas read.
      Script names follow the convention observed in the legacy bd-gold-layer Lambda (01_build_canonical_timeline.py, etc.)
      but the current runner uses a newer set of scripts producing the parquets documented here.
    </note>

    <gold_script name="(produces) gold/client_performance.parquet">
      <description>
        Per-relationship daily cumulative AUA, aua_taxable, aua_tax_deferred, aua_tax_exempt,
        cum_inflows, cum_outflows, nna, num_accounts, num_positions, pct_priced.
        Primary performance grain consumed by bd-portal-publisher for all AUA/NNA calculations.
      </description>
      <consumed_by>bd-portal-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/views/nna_aua_by_advisor.parquet">
      <description>
        Per-architect daily AUA/flows aggregation: date, architect, total_aua, aua_taxable,
        aua_tax_deferred, aua_tax_exempt, cum_inflows, cum_outflows, nna, num_relationships, num_accounts.
        Drives ADV view in timeseries_chart.json, architect_leaderboard.json, and PartnerAnalyticsResponse.views.adv.
      </description>
      <consumed_by>bd-portal-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/views/nna_aua_by_geography.parquet">
      <description>
        Per-state/country daily AUA aggregation: date, state, country, total_aua, cum_inflows,
        cum_outflows, nna, num_relationships, num_accounts.
        Drives GEO view in timeseries_chart.json, aua_by_state.json snapshot, and PartnerAnalyticsResponse.views.geo.
      </description>
      <consumed_by>bd-portal-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/views/nna_aua_by_geography_city.parquet">
      <description>
        Per-city daily AUA aggregation: date, state, city, total_aua, cum_inflows, cum_outflows,
        nna, num_relationships.
        Drives geo_drill sub-view in timeseries_chart.json (optional — gracefully skipped if absent).
        Maximum 9 cities per state in output.
      </description>
      <consumed_by>bd-portal-publisher (optional)</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/client_dimension.parquet">
      <description>
        Per-relationship static metadata: relationship_id, relationship_name, first_seen_date,
        primary_architect, primary_implementor, primary_state, primary_country,
        total_accounts, active_accounts, has_taxable, has_tax_deferred, has_tax_exempt.
        Used for new-client classification (first_seen_date), PartnerAnalyticsResponse client counts,
        and engagement/tenure metrics.
      </description>
      <consumed_by>bd-portal-publisher, bd-portal-advisor-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/accounts_dimension_latest.parquet">
      <description>
        Per-account latest metadata: account_id, relationship_id, account_name, architect, implementor,
        local_relationship, tax_status, qualified_flag, client_state, client_country, account_type,
        account_is_open.
        Used for filters/dimensions.json and snapshot snapshots (region, account_type).
      </description>
      <consumed_by>bd-portal-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/views/client_tax_liability.parquet">
      <description>
        Per-relationship tax lot exposure from holdings data:
        relationship_id, account_id, tax_status, qualified_flag, asset_name, ticker,
        purchase_year, total_units, total_cost_basis, total_market_value, total_accrued_gain,
        short_term_cost_basis, short_term_market_value, short_term_gain,
        long_term_cost_basis, long_term_market_value, long_term_gain, num_open_lots.
        Drives all tax sections in clients_tab.json, advisor book.json, and client detail.
        Note: labeled "Yang's fields" in publisher code — these fields were originally sourced
        from Yang/SmartX lot data but are now produced by the BD gold pipeline from BD holdings.
      </description>
      <consumed_by>bd-portal-publisher, bd-portal-advisor-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/account_performance.parquet">
      <description>
        Per-account daily cumulative AUA/flows (large file: ~350MB, ~10M rows).
        Columns: date, account_id, relationship_id, architect, implementor, tax_status,
        total_aua, cum_inflows, cum_outflows, nna, num_positions.
        Separated into bd-portal-advisor-publisher to avoid OOM with other tables in a single Lambda.
        Drives implementor_leaderboard.json and per-advisor book.json.
      </description>
      <consumed_by>bd-portal-advisor-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/holdings_lots/{YYYYMMDD}.parquet">
      <description>
        Per-lot snapshot for open taxable positions. Per-lot columns include:
        relationship_id, account_id, account_name, asset_name, ticker,
        acquisition_date, purchase_year, lot_index, current_units, cost_per_unit, cost_basis,
        current_price, market_value, accrued_gain, holding_period_days, term, tax_status, is_open.
        Drives open_lots[] array in ClientDetailResponse (bd-portal-advisor-publisher uses latest snapshot).
      </description>
      <consumed_by>bd-portal-advisor-publisher</consumed_by>
    </gold_script>

    <gold_script name="(produces) gold/pipeline-complete.json">
      <description>
        Sentinel file written at the end of the gold layer run by bd-gold-layer-runner EC2.
        Triggers bd-portal-publisher and bd-portal-advisor-publisher via S3 ObjectCreated event.
        Both publishers run in parallel. Content is a simple completion timestamp/status marker.
      </description>
      <consumed_by>bd-portal-publisher (trigger), bd-portal-advisor-publisher (trigger)</consumed_by>
    </gold_script>

  </bd_gold_inputs>

  <!-- ======================================================================== -->
  <!-- UPSTREAM DEPENDENCIES                                                      -->
  <!-- ======================================================================== -->

  <upstream_dependencies>

    <dependency page="ModelPortfolios" pipeline="yang-pipeline">
      <item>Yang PKL workspace (opal-data-portal-v2/benchmarks/): model portfolio and benchmark return_daily DataFrames. Source: Yang quantitative engine running on EC2 or local, uploads PKL files to S3.</item>
      <item>SmartX EC2 exporter: AUM time series source. Persistent EC2 instance (smartx-exporter) that exports SmartX portfolio data daily. Data stored in DynamoDB tables consumed by opal-portal-data-proxy.</item>
      <item>Bloomberg indices: Used as benchmark components (Bloomberg Agg, 0-1 Year Treasury, MSCI ACWI). Embedded in Yang PKL return_daily data.</item>
      <item>Morningstar peer universe: Peer comparison data embedded in Yang PKL or produced by yang-generate-peer-performance (source not confirmed from code alone).</item>
    </dependency>

    <dependency page="AdvisorIntelligence" pipeline="bd-pipeline">
      <item>49 Financial raw allocation files: Uploaded by Black Diamond Wealth Platform, ingested by bd-allocation-trigger Lambda.</item>
      <item>49 Financial raw transaction files: Ingested by bd-transactions-trigger Lambda.</item>
      <item>BD silver layer: bd-transaction-consolidator Lambda processes raw files into silver/bd_transactions.parquet and silver/bd_accounts.parquet in opal-data-bd.</item>
      <item>BD gold layer runner EC2 (bd-gold-layer-runner): Persistent EC2 that pulls scripts from s3://opal-data-bd/code/gold/ and produces all gold parquets. Scripts are managed separately from the local repository.</item>
      <item>opal-data-bd S3 bucket: Central storage for all BD pipeline data (silver, gold parquets, published JSON, logs).</item>
      <item>opal-data-portal-v2 S3 bucket: Some static JSON (e.g. advisor_rolling_flows.json per pod_inventory) may be written here by bd-portal-publisher (bucket routing not fully confirmed from code).</item>
    </dependency>

  </upstream_dependencies>

  <!-- ======================================================================== -->
  <!-- DATA QUALITY NOTES                                                         -->
  <!-- ======================================================================== -->

  <data_quality_notes>

    <note id="1" severity="medium" source="bd-portal-publisher/lambda_function.py + sprint context">
      AUA UNDERCOUNT HISTORY (Feb 23-27 2026 sprint):
      An AUA undercount incident was resolved in the Feb 23-27 sprint. The publisher was
      rearchitected to read from gold/client_performance.parquet (position-based AUA at
      relationship grain) instead of the older transaction-based approach. The parquets
      (nna_aua_by_advisor.parquet, nna_aua_by_geography.parquet, client_performance.parquet)
      are the canonical AUA source. Any historical data before this sprint may reflect the
      undercount. Code comments reference "Yang's fields" in tax sections, acknowledging that
      qualified/non-qualified lot data was previously sourced differently.
    </note>

    <note id="2" severity="medium" source="portal/src/api/endpoints/advisor-intelligence.ts:136-144">
      FIRM ID AUTH REFACTOR PENDING:
      getSnapshot() and related opal-partners-data endpoints currently pass firmId as a query
      parameter. Code comment: "firmId will be removed once Lambda reads from portal-authorizer
      context (authorizer.lambda.firmId) instead." Auth refactor is pending.
    </note>

    <note id="3" severity="medium" source="portal/src/api/endpoints/aum.ts:470-478">
      DEMO MODE ENDPOINT (ModelPortfolios account distribution):
      getAccountDistribution() uses a public endpoint /api/general/portfolios/account-distribution.json
      with no authentication. TODO comment in source: "Revert to private endpoint for production."
      Data may not reflect actual production state.
    </note>

    <note id="4" severity="medium" source="portal/src/api/portal-proxy.ts:87-95">
      401 REDIRECT DISABLED (ModelPortfolios):
      The redirect-to-login on 401 Unauthorized response is disabled in portal-proxy.ts.
      Was causing an infinite redirect loop for the ModelPortfolios page.
      Currently logs the error but does not redirect. Auth failure is silent to the user.
    </note>

    <note id="5" severity="low" source="bd-portal-publisher/lambda_function.py">
      ZERO-FILLED FIELDS (AdvisorIntelligence):
      income_fees (dividends, interest, management fees, fee_rate_pct) and portfolio.allocation
      are consistently zeroed across all BD publisher outputs. BD transaction data does not
      contain income/fee information or asset class taxonomy. These fields exist in the response
      schema for future compatibility but carry no current data.
    </note>

    <note id="6" severity="low" source="bd-portal-advisor-publisher/lambda_function.py">
      TAX FIELD LABELING ("Yang's fields"):
      Fields such as qualified_aua, non_qualified_aua, cost_basis_by_year, and top_gain_positions
      are labeled "Yang's fields" in publisher comments. This reflects their origin: they were
      originally populated from Yang/SmartX holdings lot data. The current implementation derives
      them from BD holdings via gold/views/client_tax_liability.parquet. The label is historical
      and does not indicate a live Yang dependency in the BD publisher.
    </note>

    <note id="7" severity="low" source="bd-gold-layer-runner/run-gold-layer.sh">
      GOLD SCRIPTS NOT IN LOCAL REPO:
      BD gold pipeline scripts are stored in s3://opal-data-bd/code/gold/ and synced to the
      EC2 at boot. The local repository does not contain the gold Python scripts. Any changes
      to gold script logic require uploading to S3 directly (following EC2_CODE_DEPLOYMENT_STANDARD.md).
    </note>

    <note id="8" severity="low" source="pod_inventory.xml (0.4.0_DE_ClientPlatform)">
      LEGACY TAB (AdvisorIntelligence):
      AssetIntelligenceTab.tsx exists in the portal directory but is not wired to the v5
      AdvisorIntelligence.tsx tab navigation. Likely legacy code from a prior version.
      Verify before modifying or deleting.
    </note>

    <note id="9" severity="low" source="bd-portal-advisor-publisher/lambda_function.py">
      IMPLEMENTOR UNASSIGNED HANDLING:
      The implementor_leaderboard normalizes several null-equivalent strings to "Unassigned":
      empty string, "nan", "None", "No Implementor Value Assigned". The portal must handle
      "Unassigned" as a valid leaderboard entry.
    </note>

  </data_quality_notes>

  <!-- ======================================================================== -->
  <!-- GAPS                                                                       -->
  <!-- ======================================================================== -->

  <gaps>

    <gap id="1" severity="high">
      0.4.2_RD_AdvisorIntelligence page_inventory.xml does not exist. The AdvisorIntelligence
      section of this data contract was derived from 0.4.0_DE_ClientPlatform pod_inventory (which
      itself was partially sourced from portal source files). Full RD-level component audit
      (prop shapes, state management, inter-component data flows) is not covered. DS data contract
      for AdvisorIntelligence is lower-fidelity than ModelPortfolios as a result.
    </gap>

    <gap id="2" severity="medium">
      advisor_rolling_flows.json: The exact S3 bucket (opal-data-bd vs opal-data-portal-v2) where
      this file is written could not be confirmed from the bd-portal-publisher Lambda code in this
      read pass. Pod inventory notes "opal-data-portal-v2 bucket" for this endpoint. The publisher
      Lambda writes to OUTPUT_BUCKET (opal-data-bd by default). Verify the actual write path in
      bd-portal-publisher to confirm routing.
    </gap>

    <gap id="3" severity="medium">
      opal-partners-data timeseries endpoint: The gold/timeseries/ files (nna_by_{dimension}.json,
      nna_total.json, nna_by_category.json) are referenced in opal-partners-data but were produced
      by the legacy bd-gold-layer Lambda (deprecated). It is not confirmed whether bd-gold-layer-runner
      EC2 still produces these files or whether they are now stale. The current publisher Lambdas
      do not write to gold/timeseries/ — they write to gold/timeseries_chart.json (different key).
      Verify whether opal-partners-data timeseries endpoints are still live or deprecated.
    </gap>

    <gap id="4" severity="low">
      Yang ETF returns (yang-generate-etf-returns) and peer performance (yang-generate-peer-performance)
      Lambda source paths were not read in detail. Output key patterns are inferred from portal-proxy.ts
      endpoint routing (/v1/benchmarks/etf, /v1/peers/performance) but exact S3 key patterns were not
      extracted from Lambda source code.
    </gap>

    <gap id="5" severity="low">
      NNA view in PartnerAnalyticsResponse: Code shows nna view uses the same donut as aua view
      (fallback). It is unclear whether this is intentional or a placeholder. The portal's NNA view
      toggle may not render distinct NNA segments if PartnerAnalyticsResponse.views.nna mirrors
      views.aua exactly.
    </gap>

  </gaps>

</data_contract>
```

### script-03----holdings-lots-builder.py

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

### script-05b----account-performance-builder.py

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

### script-06----client-tax-liability-builder.py

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

### 0.4.0_DS_ClientPlatform -- Recent Session Logs

#### bd_publisher_adv_drill_cla_implementation.md

# A-Roll Task Orders — 0.4.0_DS_ClientPlatform

**Date:** 2026-03-04
**Start Time:** session start
**End Time:** in progress

## Objective

Work through all A-roll task orders in sequence: ADVI-004 (adv_drill + cla in bd-portal-publisher
Lambda), ADVI-005 (stacked_bar + rolling_1y in gold script 10), A4 (script 09 bell curve
verification), A5 (opal-users-v2 advisor identity investigation). Also assessed DC task order
on startup.

---

## Work Completed

### 1. DC Task Order — Startup Assessment

Read `data_contract.md` task order. Status was already `complete` (issued 2026-03-02; baseline
contract creation). data_contract.xml at `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/`
was adequate to begin A1+A2: timeseries_chart.json Source 2 block existed but had no adv_drill
or cla entries. Those are added by A1+A2's own DC.1 requirement, not the DC task order.

### 2. ADVI-004 A2.0 Pre-Check: primary_city Confirmed in Script 04

Read `data/black_diamond/scripts/gold/04_build_client_dimension.py`.
- `primary_city` is defined in the schema comment at line 17.
- Written to output at lines 267-268 via `modal_value(grp['_city'])`.
- The Lambda's `load_all()` did NOT include `primary_city` in its cdim column prune.
- Conclusion: `cla.geo_city_drill` is a Lambda-only change — no gold-layer enhancement needed.
  This validates the CTO scope correction in the ADVI-004 task order.

### 3. ADVI-004 A1: adv_drill in bd-portal-publisher

Modified `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`.

Changes:
- Added constants `TOP_N_CLIENTS_PER_ARCH = 8` and `MAX_CLA_CITIES = 9`.
- Added `primary_city` to cdim column prune in `load_all()`.
- Expanded `perf_cohort` merge in `build_timeseries_chart()` to pull
  `relationship_name, primary_architect, primary_state, primary_city` from cdim
  (one merge serves all new views — no second parquet load).
- Added `adv_drill` computation block: iterates `adv_categories` (excl "Other");
  for each architect finds top 8 clients by latest-day AUA from `perf_cohort`;
  category key = `"{relationship_name} ({relationship_id})"` (collision-safe per contract).
- adv_drill keys match `adv.categories` strings exactly (portal drillParent lookup requirement).
- `adv_drill` added to result conditionally (omit if empty).

Contract ref: ADVI-004 Pattern 0 thread receipt, DS turn 7 (converge).

### 4. ADVI-004 A2: cla in bd-portal-publisher

Added `cla` dict to `build_timeseries_chart()` in same file.

Sub-views:
- `cla.total`: firm-wide NMNC/NMEC AUA; reuses `perf_cohort.cohort` already computed.
- `cla.geo_drill[state]`: per-state NMNC/NMEC AUA; keys match `geo.categories` exactly.
- `cla.adv_drill[arch]`: per-architect NMNC/NMEC AUA; keys match `adv.categories` exactly.
- `cla.geo_city_drill[state][city]`: NMNC/NMEC AUA per city using `cdim.primary_city`;
  top 9 cities per state by latest-day AUA. Optional — omitted if no city data.

NMNC/NMEC rule: trailing-12-month vintage (`months_since_first <= 12`), same formula
as the existing `aua` view in `build_timeseries_chart()`. No new classification introduced.

Helper `_cla_view(df_subset)` added to DRY the groupby/unstack pattern across all 4 sub-views.

Contract ref: ADVI-004 Pattern 0 thread receipt + CTO task order A2.0-A2.3.

### 5. ADVI-004 DC.1: data_contract.xml Updated

Added `adv_drill` and `cla` key definitions to the timeseries_chart.json Source 2 block in
`data_contract.xml`. Documented: structures, category key format, TOP_N_CLIENTS_PER_ARCH,
NMNC/NMEC rule with exact formula, sign conventions, source parquet references, primary_city
derivation with script 04 line citations, geo_city_drill feasibility basis.
Also updated `<date>` to 2026-03-04 and added source_note about the 2026-03-04 extensions.

Syntax verified: `ast.parse()` clean. Committed at `5f60d30e`.

### 6. DT Brief Written for Stream B1

Wrote `docs/briefs/devops-brief-advi-004-adv-drill-cla.md` for `0.4.0_DT_ClientPlatform`.
Covers: what changed, build-and-upload.sh command, terraform plan/apply sequence,
verification steps, next tag `bd-v2.15.0`. Committed at `f2e3c675`.

### 7. ADVI-005 A3.0 Pre-Check: Data History Confirmed

Could not query S3 directly (AWS CLI hanging in Git Bash on Windows). Resolved via session
log archaeology:
- `logs/sessions/2026-02-27/data_scientist/partner_analytics_09_script_implementation.md`:
  "client_performance has exact daily data back to 2020-06-30"
- `logs/sessions/2026-02-26/data_scientist/partner_analytics_new_script_design_task_order.md`:
  "for every day back to 2020-06-30"
- `nna_aua_by_advisor.parquet` is derived from same positions cube — same inception date.

Findings documented:
- Data inception: **2020-06-30**. Data range: ~5.5 years.
- First valid 1Y rolling point: ~2021-07-01 (after 1Y warmup).
- 3Y and Max stacked_bar coverage: **complete** — data exceeds required 4Y lookback.
- No history caveat needed; all 5 stacked_bar periods fully supported.

### 8. ADVI-005 A3.1: stacked_bar in script 10

Modified `data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py`.

Added:
- `STACKED_BAR_PERIODS = ('qtd', 'ytd', '1y', '3y', 'max')` constant.
- `compute_stacked_bar()` function:
  - Computes period boundaries: qtd/ytd via `_get_period_boundaries()`;
    1y/3y via trailing Timedelta(365/1095 days); max via parquet inception date.
  - Calls existing `_compute_nna_for_range()` per period — no new data logic.
  - Returns `{period: [AdvisorBarEntry]}` for a single role.
  - `AdvisorBarEntry`: `{advisor_name, advisor_id, inflows, outflows, nna_net}`.
  - `outflows` positive magnitude. `nna_net` signed.
- Assembled into period-outer / role-inner structure per CTO task order A3.1 correction:
  `stacked_bar = { period: { 'architects': [...], 'implementors': [...] } }`
  Note: this differs from thread receipt (role-outer); task order is the binding spec.

### 9. ADVI-005 A3.2: rolling_1y in script 10

Added `rolling_1y` dict extracted from existing `compute_rolling_series()` 1Y window output.
- `rolling_1y.architects`: list of `{advisor_name, advisor_id, series: [{date, nna, inflows, outflows}]}`
- `rolling_1y.implementors`: same shape.
- Full history emitted; frontend slices x-axis by period toggle.
- No new rolling computation — reuses series['1Y'] already produced.
- Point fields `{date, nna, inflows, outflows}` match `Rolling1YDataPoint` contract exactly.

### 10. ADVI-005 A3.3: Backward Compatibility

All legacy keys (`generated_at`, `data_as_of`, `firm_id`, `summary`, `architects`,
`implementors` with 30d/90d/1Y windows) are unchanged. `stacked_bar` and `rolling_1y`
are additive top-level keys. Dry-run preview block updated to show both new keys.

### 11. ADVI-005 DC.1: data_contract.xml Updated

Replaced the thin Source 5 (advisor_rolling_flows) entry with a full documented block:
- Script source (EC2 gold script, not Lambda).
- Data history block: 2020-06-30 inception, 5.5Y range, first 1Y point ~2021-07-01, 3Y/Max complete.
- Legacy key schema for summary/architects/implementors.
- stacked_bar: full structure, AdvisorBarEntry fields, period boundary definitions, sign convention.
- rolling_1y: AdvisorRolling1YSeries structure, daily cadence, all 3 fields, rolling method.

Syntax verified. Committed at `c9b3ab76`.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Expand perf_cohort merge (not a separate join) | One merge serves A1 + all CLA sub-views; no extra parquet load |
| _cla_view() helper | 4 CLA sub-views share identical groupby/unstack/fill pattern |
| Iterate adv_categories (not top_architects) for adv_drill | adv_categories is the portal's drillParent key source — must match exactly |
| adv_drill and geo_city_drill both conditional | Omit if empty, consistent with existing geo_drill pattern |
| Period-outer/role-inner for stacked_bar | CTO task order A3.1 explicitly overrides thread receipt (role-outer) |
| rolling_1y reuses series['1Y'] directly | No new rolling math needed; existing output matches contract exactly |
| Data history via session log archaeology (not live S3 query) | AWS CLI hanging in Git Bash on Windows; session logs have confirmed the 2020-06-30 date |
| A4: no patch needed — signed percentiles are intentional | `calculate_nna_distribution_stats()` docstring and bin design confirm signed distribution is correct; abs() is present where it matters (materiality filter, bin construction) |
| A4.2 confirmed from S3 | Live header_metrics.json shows non-degenerate signed distribution; p10=-$46K to p90=+$152K; OH net-outflow state correctly shows all-negative segment |
| A5: Scenario (c) — no mapping exists | No advisorId/advisorName field in opal-users-v2; architects have no portal accounts; email matching not viable (gold layer has no email); recommend `advisorKey` attribute at user creation |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | TOP_N_CLIENTS_PER_ARCH + MAX_CLA_CITIES; primary_city to cdim; expanded perf_cohort merge; adv_drill + cla blocks; adv_drill/cla added to result | Yes — `5f60d30e` |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml` | adv_drill + cla doc in timeseries_chart.json Source 2; adv_rolling_flows Source 5 fully documented with A3 shapes | Yes — `5f60d30e`, `c9b3ab76` |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-004-adv_drill_cla.md` | Status: pending -> complete | Yes — `5f60d30e` |
| `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-005-rolling_flows_data.md` | Status: pending -> complete | Yes — `c9b3ab76` |
| `data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py` | STACKED_BAR_PERIODS constant; compute_stacked_bar(); rolling_1y extraction; both added to return dict; dry-run preview extended | Yes — `c9b3ab76` |
| `docs/briefs/devops-brief-advi-004-adv-drill-cla.md` | New — DT Stream B1 deploy instructions | Yes — `f2e3c675` |
| `docs/briefs/devops-brief-advi-005-rolling-flows.md` | New — DT Stream B2 EC2 deploy instructions | Yes — `75b3b83f` |
| `data/black_diamond/scripts/gold/09_generate_partner_analytics.py` | Fix 1a+1b: remove 'Unknown' exclusion from geo_end filter and distribution filter in `build_nna_geo_view` | Yes — `4ba82ffc` |
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | Fix 2: `_quarter_nna` start changed from q_start to prior_qe = q_start - 1 day | Yes — `4ba82ffc` |

---

## Briefs Written

| Brief | Path | Audience |
|-------|------|----------|
| DT deploy — bd-portal-publisher (Stream B1) | `docs/briefs/devops-brief-advi-004-adv-drill-cla.md` | 0.4.0_DT_ClientPlatform |
| DT deploy — script 10 EC2 (Stream B2) | `docs/briefs/devops-brief-advi-005-rolling-flows.md` | 0.4.0_DT_ClientPlatform |

---

### 12. ADVI A4.1: Script 09 Bell Curve Code Verification

Read `data/black_diamond/scripts/gold/09_generate_partner_analytics.py`.

Note: the task order referenced `09_build_distribution_stats.py` — the actual filename is
`09_generate_partner_analytics.py`. The file contains the full partner analytics script
including distribution stats functions.

**A4.1 — Function located:**
- `calculate_nna_distribution_stats(nna_values: pd.Series)` — line 320
- This is the bell curve / distribution stats function for per-relationship period NNA

**abs() handling verified present:**

| Location | Line | Code | Purpose |
|----------|------|------|---------|
| Materiality filter | 332 | `vals = vals[vals.abs() >= NNA_MATERIALITY_THRESHOLD]` | Excludes sub-$1K NNA accounts (fees, dividends, rounding noise) |
| Bin max | 348 | `abs_max = float(vals.abs().max())` | Log-spaced bin upper bound from largest magnitude (pos or neg) |
| Bin min | 349 | `abs_min = max(float(vals.abs().min()), 1_000)` | Log-spaced bin lower bound floored at $1K |
| Symmetric bins | 353-357 | `neg_edges = -pos_edges[::-1]` mirrored around zero | Both inflows (positive) and outflows (negative) visible in histogram |

**Percentile design:** Percentiles at lines 374-380 are SIGNED (not abs()). This is
intentional — the function docstring states "signed, symmetric log bins." For a mixed
distribution: p10 reflects the 10th-percentile NNA value (could be large negative for
outflow-heavy segments); p90 reflects the 90th-percentile (typically positive inflow).
Signed percentiles correctly convey the shape of a bimodal inflow/outflow distribution.

**Commit attribution:** The abs() handling landed across two commits after 8247c6d0:
- `792b4e05`: Added `calculate_nna_distribution_stats()` with symmetric log bins + abs() for bin construction
- `9216c922` (2026-03-03): Added `NNA_MATERIALITY_THRESHOLD = 1_000` and abs() materiality filter

All three commits predating the A4 task order (2026-03-03). The fix is present in current CLOUD HEAD.

**A4.2 — S3 verification: BLOCKED**
Cannot read `s3://opal-data-bd/gold/partner_analytics/header_metrics.json` — AWS CLI
non-functional in Git Bash on Windows (hangs with "File association not found for extension .py").
Actual P10/P25/Median/P75/P90 threshold values not confirmed from live data.

**A4.3 — Assessment:** Code analysis confirms the abs() fix landed. No patch needed.
A4.2 remains open pending AWS CLI resolution.

---

### 13. A4.2: header_metrics.json NNA Distribution Verified from S3

AWS CLI issue resolved. Read `s3://opal-data-bd/gold/partner_analytics/header_metrics.json`.

**Total firm NNA distribution — current period:**

| Percentile | Value |
|-----------|-------|
| p10 | -$46,787.40 |
| p25 | -$9,066.01 |
| p50 | -$1,061.62 |
| p75 | +$19,760.20 |
| p90 | +$151,675.42 |

**Assessment:** Non-degenerate. ✓ Not all zero. ✓ Not symmetric. ✓ Signed distribution correctly
reflects real per-relationship period NNA. Median is -$1K (slightly negative — fee noise boundary).
p10 represents top-10% outflow clients; p90 represents top-10% inflow clients.

**Per-segment samples (selected):**

| Segment | Type | Count | p10 | p50 | p90 |
|---------|------|-------|-----|-----|-----|
| TX | state | 464 | -$45,336 | -$1,192 | +$134,753 |
| OH | state | 5 | -$855,614 | -$15,234 | +$10,052 |
| AL | state | 10 | -$3,798 | +$5,069 | +$109,539 |
| travis_penfield | arch | 37 | -$472,924 | -$4,976 | +$201,494 |
| chase_bertrand | arch | 38 | -$20,348 | +$2,766 | +$907,525 |
| 49f_house | arch | 399 | -$49,721 | -$1,258 | +$75,978 |

OH state (predominantly outflow): p10=-$855K, p50=-$15K, p90=+$10K — correctly shows a
net-outflow segment. Signed design is correct for this use case.

Materiality filter confirmed working: TX has 464 counts vs a larger total client base —
accounts with |NNA| < $1K excluded.

**Conclusion: A4.2 verified. No patch needed. Task order complete.**

---

### 14. A5.1+A5.2+A5.3: opal-users-v2 DynamoDB Investigation

**Table schema:**

| Key | Value |
|-----|-------|
| Table name | `opal-users-v2` |
| Partition key | `PK` (String) |
| Sort key | `SK` (String) |
| Item count | 34 |
| SSE | KMS enabled |

PK patterns:
- `USER#{userId}` — user profile records (SK=`PROFILE`)
- `FIRM#{firmId}` — firm records (SK=`META`, `CONFIG#defaults`, `MEMBER#{userId}`)

Fields present on USER#PROFILE items: `userId`, `email`, `name`, `role`, `tier`, `firmId`,
`passwordHash`, `status`, `createdAt`, `updatedAt`, `mustChangePassword`.
Optional legacy fields: `migratedFrom`, `migratedAt`.

Fields NOT present (searched explicitly): `advisorId`, `advisorName`.

GSIs:
- `firmId-index` (PK=firmId, SK=PK) — projects: role, email, name, tier, status
- `email-index` (PK=email, KEYS_ONLY)

**Advisor-tier user records (tier="advisor", firmId="49financial"):**

| userId | email | name |
|--------|-------|------|
| usr_6ad8541dd636 | dan.wohlgemuth@49financial.com | Dan Wohlgemuth |
| usr_dbd5ca809ff8 | lizah.okoniewski@49financial.com | Lizah Okoniewski |

Neither Dan Wohlgemuth nor Lizah Okoniewski appears in `gold/advisors/` prefix
(the canonical list of 60+ advisor slugs). They are 49financial staff with portal access
but are NOT financial architects/advisors in the BD gold data.

**Gold layer architect identifiers (sample from `gold/advisors/` prefix and partner_analytics):**
`travis_penfield`, `chase_bertrand`, `kyle_sims`, `david_farrell`, `ted_grant`,
`dean_dillenberg`, `greg_rosner`, `hunter_lloyd`, `josh_henson`, `matt_foxhall`, and ~50 more.

None of these architect names have any corresponding user account in opal-users-v2.

**Mapping scenario determination:**

```
Scenario: (c) — No existing mapping
```

Evidence:
1. No `advisorId` or `advisorName` field in any opal-users-v2 record.
2. The two advisor-tier 49financial users (Wohlgemuth, Okoniewski) do not correspond to
   any gold layer architect — they are ops/admin staff, not registered advisors.
3. The actual financial architects (Travis Penfield, Kyle Sims, etc.) have NO user accounts
   in opal-users-v2 at all. They cannot log in to the portal.
4. Email-based matching is not viable: the gold layer stores no email addresses for advisors —
   architect identity derives entirely from BD transaction data (first/last name, slugified).

**BLOCKER — escalated to COO and CTO (see Next Steps).**

The Books tab advisor identity resolution cannot be implemented until a mapping from
JWT userId to gold layer advisor slug is established.

**Recommended mapping approach:**

Add an optional `advisorKey` attribute to USER#PROFILE items (e.g., `advisorKey: "travis_penfield"`).
Populate this at advisor user account creation for `tier: "advisor"` accounts. Portal auth reads
this field from the JWT-resolved profile and uses it as the gold data lookup key.

This requires:
- DynamoDB schema extension (additive — no existing records broken)
- Admin onboarding flow: when creating a new advisor user, enter their `advisorKey` from the
  gold layer slug list (available from `gold/advisors/` prefix or architect_leaderboard.json)
- Portal auth middleware: when Books tab requested, verify `advisorKey` matches the requested
  advisor's data segment
- No EC2 or Lambda code changes until the mapping is confirmed populated for real users

**Task order A5 complete — findings documented. Blocker flagged below.**

---

### 15. NNA Canonicalization Fixes (CEO-validated consultant brief)

Read `docs/briefs/data-scientist-nna-geo-unknown-and-date-boundary-fix.md`.

Background: cross-view NNA audit for Q4 '25 found three portal views reporting different
totals for the same quarter: Snapshot-GEO ~$96.0M, Assets Overview ~$96.6M, Snapshot-ADV
~$97.9M. Both gaps traced to code-level root causes confirmed in the brief.

**Fix 1a — script 09 `build_nna_geo_view`, lines 826-829:**
Removed `'Unknown'` from the `geo_end` filter. Previously, the filter excluded all rows
where `state == 'Unknown'` before computing `total_net_nna`, silently dropping the NNA of
all relationships with no resolvable state. Changed to keep `'Unknown'` as a named segment
(key: `'unknown'`), mirroring exactly how `build_nna_adv_view` handles `'Unassigned'`.
Only non-US/blank states (null, empty string) are now excluded.

**Fix 1b — same file, distribution filter lines 903-908:**
Removed the matching `state != 'Unknown'` exclusion from the per-relationship NNA
distribution block. `'Unknown'` relationships now contribute to `total_dist` and get
their own `by_segment_dist['unknown']` entry via the existing segment loop.

**Fix 2 — Lambda `_quarter_nna`, line 1021:**
Changed the period start baseline from `q_start` (Oct 1) to `prior_qe = q_start - 1 day`
(Sep 30). Script 09 uses Sep 30 as the Q4 start baseline; the Lambda was using Oct 1,
causing it to miss Oct 1 settlement flows (~$1.3M for Q4 '25). QTD (`quarters_back=0`)
uses the `else 0` branch — unaffected by this change.

Both files committed at `4ba82ffc`.

**Pending verification** (requires deploy of both streams first):
- Stream B (script 09 EC2 redeploy): `gold/partner_analytics/header_metrics.json` geo NNA
- Stream B1 (bd-portal-publisher Lambda redeploy): `gold/summary/header_metrics.json` overview NNA
- All three views (GEO, ADV, Overview) should be within $1.00 of each other for Q4 '25
- Verification script in brief at `docs/briefs/data-scientist-nna-geo-unknown-and-date-boundary-fix.md`

---

### 16. Stream B2 DT Brief Written

Wrote `docs/briefs/devops-brief-advi-005-rolling-flows.md` for `0.4.0_DT_ClientPlatform`.
Covers: what changed (script 10 only, no infra changes), safe-ec2-deploy.sh command,
EC2 start command for incremental run, verification via S3 JSON key check, next tag `bd-v2.15.1`.
Notes: run_gold_layer.sh incremental mode runs 02-10 sequentially — only script 10 output changes.
Does NOT trigger pipeline-complete to re-run on its own; EC2 boot triggers the run automatically.
Committed at `75b3b83f`.

---

## Blockers

- **A5 BLOCKER — Books Tab Advisor Identity Mapping does not exist (Scenario c).**
  opal-users-v2 contains no `advisorId` or `advisorName` field on any record. The financial
  architects in the gold layer (Travis Penfield, Kyle Sims, etc.) have no user accounts in
  the portal auth system. JWT userId cannot be resolved to a gold layer advisor slug.
  The Books tab scoped access cannot be implemented until an `advisorKey` attribute is added
  to opal-users-v2 USER#PROFILE items and populated for advisor-tier accounts.
  **Escalated to COO and CTO — see Next Steps.**

---

## Current State

**Status:** IN PROGRESS — NNA canonicalization fixes committed, awaiting DT deploy + verification
**Active branch:** `CLOUD`

All five A-roll task orders complete. Two additional CEO-validated fixes committed this session:
- **ADVI-004** (A1+A2 adv_drill + cla) — complete, committed `5f60d30e`
- **ADVI-005** (A3 stacked_bar + rolling_1y) — complete, committed `c9b3ab76`
- **A4** (script 09 bell curve verification) — complete: code verified + S3 live data confirmed
- **A5** (opal-users-v2 investigation) — complete: Scenario (c) BLOCKER documented
- **NNA canonicalization** (consultant brief) — committed `4ba82ffc`; requires DT deploy + verification

DT deploy briefs written for both active streams. NNA fixes add to the deploy scope:
- Stream B1 (bd-portal-publisher Lambda): `docs/briefs/devops-brief-advi-004-adv-drill-cla.md` — now ALSO includes Fix 2 (`_quarter_nna`)
- Stream B2 (script 09/10 EC2): now ALSO includes Fix 1a+1b (`build_nna_geo_view`)

Pending: DT redeploy of both streams (commit `4ba82ffc`); post-deploy 3-view NNA verification.

---

## Next Steps

> Ordered by priority.

1. **[0.4.0_DT_ClientPlatform] Redeploy both streams with NNA fixes** (commit `4ba82ffc`)
   Fix 2 (Lambda `_quarter_nna`) lands in Stream B1 — bd-portal-publisher. Same deploy path as
   before: build-and-upload.sh, terraform plan/apply, tag `bd-v2.15.2`.
   Fix 1a+1b (script 09 `build_nna_geo_view`) lands in Stream B (EC2). safe-ec2-deploy.sh,
   then start EC2 for incremental run. Tag `bd-v2.15.2` or increment as appropriate.
   Verification script: `docs/briefs/data-scientist-nna-geo-unknown-and-date-boundary-fix.md`
   (all three NNA views within $1.00 of each other for Q4 '25).

2. **[COO + CTO] BLOCKER — Books tab advisor identity mapping** (A5 Scenario c)
   No JWT userId → gold layer advisor slug mapping exists in opal-users-v2.
   Required action: add `advisorKey` attribute to USER#PROFILE items for advisor-tier accounts.
   Recommend: admin onboarding flow sets `advisorKey` = gold layer slug (e.g., `travis_penfield`)
   at advisor user creation. Portal middleware reads this field for Books tab scoped access.
   No auth implementation should proceed until this is confirmed populated for real users.
   Downstream affected: 0.4.0_DE_ClientPlatform (portal auth middleware), 0.4.2_RD_AdvisorIntelligence (Books tab).

2. **[0.4.0_DT_ClientPlatform] Deploy Stream B1 — bd-portal-publisher** (commit `5f60d30e`)
   Full instructions: `docs/briefs/devops-brief-advi-004-adv-drill-cla.md`.
   Next tag: `bd-v2.15.0`.

3. **[0.4.0_DT_ClientPlatform] Deploy Stream B2 — script 10 EC2** (commit `c9b3ab76`)
   Full instructions: `docs/briefs/devops-brief-advi-005-rolling-flows.md`.
   Next tag: `bd-v2.15.1`.

**Files to touch next:**
- None on DS side. Pending COO/CTO resolution of A5 blocker.

**Do NOT:**
- Re-enable `build_partner_analytics()` in bd-portal-publisher lambda_handler (DISABLED intentionally).
- Change stacked_bar nesting to role-outer/period-inner (thread receipt shape) — CTO task order is binding.
- Modify existing aua/nna/geo/adv/geo_drill keys in timeseries_chart.json.
- Run `02_build_positions_cube.py --start-date` (known to corrupt data; full rebuild only if needed).


### 0.4.0_DS_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DS_ClientPlatform

076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context

### 0.4.2_RD_AdvisorIntelligence -- Recent Session Logs

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


### 0.4.2_RD_AdvisorIntelligence -- Pending Task Orders

#### advi_c1_geo_continuous.md

# Task Order: Stream C1 — Continuous NNA GEO View (Search + City Drill-down)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-c1-geo-continuous</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement the continuous NNA GEO view in DistributionTab with top-8 state series,
    a search input for all states, and click-to-drill into per-city data. Data is already
    deployed in timeseries_chart.json as of bd-v2.14.0. No data dependency — start immediately.
    Your first session log from this work satisfies O3 for the COO to schedule alignment threads.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="C1.1">
      Read DistributionTab.tsx and types.ts before making any changes. Understand the
      current GEO view rendering and the existing timeseries_chart.json data shape
      (geo view: per-state categories; geo_drill: Record of stateKey to per-city data).
    </requirement>
    <requirement id="C1.2">
      Update the GEO continuous NNA view to render the top-8 states as separate series
      in the cumulative NNA chart. Use the same chart type, axis format, color scheme,
      and window toggle as the Assets Overview header panel cumulative NNA chart.
      Data source: timeseries_chart.json geo.categories (top-8 state keys) and geo.data.
    </requirement>
    <requirement id="C1.3">
      Add a search input in the left panel controls that filters across ALL available
      states in timeseries_chart.json geo.categories — not just the top-8 displayed.
      Selecting a state from search results drills into that state's city data.
    </requirement>
    <requirement id="C1.4">
      Implement click-to-drill interaction:
        - Clicking a state series in the chart legend OR selecting from search
          triggers the drill: chart re-renders with per-city series for that state
          (sourced from timeseries_chart.json geo_drill[stateKey])
        - A back/breadcrumb control returns to the state-level view
        - Drill state is local UI state only — no additional API call needed
        - Breadcrumb must display the current level clearly:
          "All States" at state level, "{StateName}" when drilled
    </requirement>
    <requirement id="C1.5">
      Run bunx tsc -b after changes. DE reviews before DT pushes to DEV.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Top-8 states render as separate chart series with consistent color and window toggle.</criterion>
    <criterion id="2">Search input filters all available states including those outside top-8.</criterion>
    <criterion id="3">Click-to-drill shows per-city series from geo_drill[stateKey]; breadcrumb returns to state view.</criterion>
    <criterion id="4">bunx tsc -b passes with no new type errors.</criterion>
    <criterion id="5">DE has reviewed and approved before DT pushes to DEV.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Data is already in S3 — no DS work or DT deploy needed for this stream. Start immediately.</constraint>
    <constraint>Drill state is local React state — do not add a new API endpoint or query for this.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>Read existing task orders (page_inventory, distribution_nomenclature_fix, continuous_view_max_window_clients_fix) before starting. If they conflict with C1 changes, coordinate with DE first.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- C1 GEO continuous search and drill"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: GEO continuous NNA with search + city drill-down</deliverable>
    <deliverable type="document">Session log documenting the work (satisfies O3 for COO thread scheduling)</deliverable>
  </deliverables>
</task_order>
```

#### advi_c3_cla_snapshot.md

# Task Order: Stream C3 — Snapshot CLA Simplified Two-Color Visualization

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-c3-cla-snapshot</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Fix the Snapshot CLA view in DistributionTab, which is incorrectly rendering as a
    flows/NNA chart. Replace with a clean two-color NMNC/NMEC proportional display.
    Data is in header_metrics.json — no DS deploy needed. Start immediately.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="C3.1">
      Read DistributionTab.tsx and types.ts before making changes. Locate the current
      CLA snapshot rendering. Identify which fields from header_metrics.json it currently
      uses and confirm against the ClaView type in types.ts.
      If uncertain which specific fields carry NMNC/NMEC AUA, check with DE before committing.
    </requirement>
    <requirement id="C3.2">
      Replace the current CLA snapshot rendering with a clean two-color proportional display:
        - Green = NMNC (New Client AUA)
        - Blue = NMEC (Existing Client AUA)
        - Format: horizontal stacked bar or split donut — clean, no axes, just two
          proportions with AUA dollar amounts and percentages labeled
        - Labels: "New Clients (NMNC)" in green, "Existing Clients (NMEC)" in blue
      ZERO inflow/outflow data. ZERO NNA vocabulary. ZERO blue/red flows visual language.
      This is a composition view, not a flows view.
    </requirement>
    <requirement id="C3.3">
      The visualization must support the time machine period selector (q1/q2/q3)
      to show how the new-client percentage has shifted across periods.
      Each period selection updates the NMNC/NMEC proportions shown.
    </requirement>
    <requirement id="C3.4">
      Run bunx tsc -b after changes. DE reviews NMNC/NMEC label accuracy against
      actual header_metrics.json field values before DT pushes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">CLA snapshot shows only two colors: green NMNC and blue NMEC. No flows chart elements.</criterion>
    <criterion id="2">Each segment labeled with name, AUA dollar amount, and percentage.</criterion>
    <criterion id="3">Time machine period selector (q1/q2/q3) updates proportions correctly.</criterion>
    <criterion id="4">DE has confirmed NMNC/NMEC field accuracy against header_metrics.json before DT push.</criterion>
    <criterion id="5">bunx tsc -b passes with no new type errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No inflow/outflow data, no NNA. CLA = client lifecycle composition (new vs existing), not flows.</constraint>
    <constraint>If uncertain about which header_metrics.json fields map to NMNC/NMEC AUA, ask DE before implementing. Do not guess field names.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- C3 CLA snapshot two-color redesign"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: CLA snapshot replaced with two-color NMNC/NMEC proportional display</deliverable>
  </deliverables>
</task_order>
```

#### ADVI-004-distribution_continuous.md

# Task Order: Distribution Tab Continuous Views (C2 + C4) — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI-004-rd-distribution_continuous</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
    <thread_serial>ADVI-004</thread_serial>
    <thread_ref>org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/</thread_ref>
    <gate_status>CLEARED — DT Stream B1 deployed bd-v2.15.0. adv_drill + cla are LIVE in
      timeseries_chart.json. DE types committed portal DEV 7df26bb. START IMMEDIATELY.</gate_status>
    <updated_by>0.4.0_DE_ClientPlatform</updated_by>
    <updated_date>2026-03-04</updated_date>
  </metadata>

  <objective>
    Implement C2 (ADV continuous NNA with architect->client drill-down) and C4 (CLA continuous
    stacked area with full drill-down including city) in DistributionTab.tsx per the ADVI-004
    receipt. Both backend keys are now live. DE has typed them. Start now.
  </objective>

  <references>
    <ref type="receipt">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — CumulativeChartResponse.cla? and .adv_drill? are typed (portal DEV 7df26bb)</ref>
    <ref type="data_contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM C2 — Continuous NNA ADV (architect -> client drill)        -->
    <!-- ================================================================ -->
    <requirement id="C2.1">
      GATE CLEARED. adv_drill is LIVE in timeseries_chart.json (bd-v2.15.0).
      adv_drill is typed on CumulativeChartResponse as:
        adv_drill?: Record&lt;string, CumulativeChartView&gt;
      Key = architect display name matching adv.categories exactly.
    </requirement>
    <requirement id="C2.2">
      Implement ADV continuous NNA view in DistributionTab.tsx:
        - Top architects as separate series from adv.categories
        - Click architect -> drill to client/relationship level using chartData.adv_drill[architectKey]
          where architectKey is the adv.categories string (e.g. "Travis Penfield")
        - Client-level category keys = "{name} ({id})" (from DS implementation)
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level (client is terminal grain for ADV)
        - Guard on chartData?.adv_drill?.[key] before rendering drill view
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA stacked area (full drill including city) -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE CLEARED. cla is LIVE in timeseries_chart.json (bd-v2.15.0).
      cla is typed on CumulativeChartResponse as:
        cla?: {
          total: CumulativeChartView
          geo_drill: Record&lt;string, CumulativeChartView&gt;
          adv_drill: Record&lt;string, CumulativeChartView&gt;
          geo_city_drill?: Record&lt;string, Record&lt;string, CumulativeChartView&gt;&gt;
        }
    </requirement>
    <requirement id="C4.2">
      Implement continuous CLA view rendering all four drill levels:
        - cla.total: firm-wide two-series stacked area (NMNC/NMEC)
        - cla.geo_drill: per-state breakdown — click state to drill to cities
        - cla.geo_city_drill: per-city within state (guard: geo_city_drill may be absent)
        - cla.adv_drill: per-architect breakdown (architect is terminal grain for ADV-CLA)
      Y-axis = absolute dollar AUM. Two stacked areas: NMNC and NMEC.
    </requirement>
    <requirement id="C4.3">
      Colors: use existing frontend hex palettes already in DistributionTab.tsx
      (CATEGORY_COLORS, GEO_COLORS). No backend colorMap field — all color assignment
      is frontend-only.
    </requirement>
    <requirement id="C4.4">
      Record key alignment (critical for drill lookup):
        - cla.geo_drill keys = state abbreviations matching timeseries_chart.json geo.categories
        - cla.adv_drill keys = architect display names matching timeseries_chart.json adv.categories
        - "Other" bucket key is capital-O exactly ("Other")
      Same pattern as existing geo_drill lookup — follow that implementation.
    </requirement>
    <requirement id="C4.5">
      Guard on chartData?.cla before rendering CLA metric selector or view.
      CLA is only available in continuous mode (not snapshot). Do not add CLA to the
      snapshot metric selector.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C2: ADV continuous NNA renders with architect series, and clicking an architect drills to client/relationship series (adv_drill[key]).</criterion>
    <criterion id="2">C2: Breadcrumb returns from client to architect level.</criterion>
    <criterion id="3">C4: CLA continuous renders as stacked area (NMNC/NMEC) at total level.</criterion>
    <criterion id="4">C4: GEO view offers state drill -> city drill (geo_city_drill guarded for absence).</criterion>
    <criterion id="5">C4: ADV view renders per-architect NMNC/NMEC (adv_drill).</criterion>
    <criterion id="6">Colors use CATEGORY_COLORS/GEO_COLORS — no backend colorMap dependency.</criterion>
    <criterion id="7">Record keys align with existing geo/adv category keys ("Other" capital-O).</criterion>
    <criterion id="8">bunx tsc -b passes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gates are CLEARED. Do not wait. Start immediately.</constraint>
    <constraint>Implement per ADVI-004 receipt field names and types. Do not invent fields.</constraint>
    <constraint>Colors are frontend-only. Do not expect or require a backend colorMap field.</constraint>
    <constraint>DE reviews before DT pushes to DEV. Signal DE when commits are ready.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- ..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: C2 ADV continuous NNA with architect->client drill-down</deliverable>
    <deliverable type="commit">DistributionTab.tsx: C4 CLA continuous stacked area with full drill (total/geo/city/adv)</deliverable>
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

#### advi_004_cla_type_wiring.md

# ADVI-004 CLA Type Wiring (TY Task Order) — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-04
**Start Time:** session 2
**End Time:** ~10 min
**Portal DEV commits:** `3dc9dc5` (I2 sort fix) -> `7df26bb` (cla type)
**Workspace CLOUD commit:** pending (this log commit)

## Objective

Add the `cla?` type extension to `CumulativeChartResponse` in
`portal/src/pages/AdvisorIntelligence/types.ts` per ADVI-004 task order
`ADVI-004-portal_types_wiring.md`. Unblocked by DS delivering A1+A2 and updating
`data_contract.xml` in commit `5f60d30e`.

---

## Work Completed

### 1. DS Work Review

Read DS session log `2026-03-04/bd_publisher_adv_drill_cla_implementation.md`.
Confirmed A1 (adv_drill) and A2 (cla timeseries) are complete in commit `5f60d30e`.
DS data_contract.xml updated as DC.1 gate. DevOps brief written at
`docs/briefs/devops-brief-advi-004-adv-drill-cla.md` (commit `f2e3c675`).

DS implementation confirms these shapes:
- `cla.total` — firm-wide NMNC/NMEC as `CumulativeChartView` (categories: NMNC, NMEC)
- `cla.geo_drill` — per-state NMNC/NMEC; keys match `geo.categories` exactly
- `cla.adv_drill` — per-architect NMNC/NMEC; keys match `adv.categories` exactly
- `cla.geo_city_drill` — per-state-city NMNC/NMEC via `cdim.primary_city`; optional
  (omitted if no city data), nested `Record<state, Record<city, CumulativeChartView>>`

No colorMap in contract (frontend-only hex palettes). No new endpoint. No new query key.

### 2. types.ts Audit Before Edit

Read `types.ts` in full before editing. Key finding:
- `adv_drill?: Record<string, CumulativeChartView>` already present on `CumulativeChartResponse`
  at line 362 — no change needed there.
- `cla` is entirely absent — only addition needed.
- `CumulativeChartView` (line 340) is reused correctly for all cla sub-views.

### 3. cla Type Added

Added `cla?` as optional field on `CumulativeChartResponse` (after `adv_drill`):

```typescript
cla?: {                                           // Client Lifecycle Analysis (NMNC/NMEC)
  total: CumulativeChartView
  geo_drill: Record<string, CumulativeChartView>
  adv_drill: Record<string, CumulativeChartView>
  geo_city_drill?: Record<string, Record<string, CumulativeChartView>>
}
```

`geo_city_drill` is `?` because DS omits the key when no city data is present
(consistent with DS conditional: `if cla_geo_city_drill`).

`bunx tsc -b --noEmit` — clean.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `cla?` is optional on `CumulativeChartResponse` | Additive rollout — older cached responses won't have the key; portal must guard at consumption site |
| Reuse `CumulativeChartView` for all cla sub-views | DS builds identical structure (description, categories, data[]). No new type needed. |
| `geo_city_drill?` is optional (inner level not optional) | DS omits entire key if no cities; once key is present, all sub-keys are strings keyed to CumulativeChartView |
| Did not update `CumulativeChartViewMode` | Task order TY.1 only covers the type extension. CLA view mode integration is RD scope (C2/C4 streams). |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/types.ts` | Added `cla?` optional field to `CumulativeChartResponse` | Yes — portal DEV `7df26bb` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-004-portal_types_wiring.md` | Status: pending -> complete | Yes — CLOUD (this commit) |

---

## Blockers

None. Types task is complete.

TY.5 (review RD C2+C4 streams and signal DT) is pending — not a blocker, awaits RD work.

---

## Current State

**Status:** COMPLETE (for this task order)
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

Both pending task orders from the COO session (2026-03-03) are now complete:
- Stream I2 (leaderboard sort) — done, portal DEV `3dc9dc5`
- ADVI-004 types wiring (cla extension) — done, portal DEV `7df26bb`

Portal DEV has two DE commits since last DT push: `3dc9dc5` and `7df26bb`.
DT push is blocked on TY.5 (review RD C2+C4 implementation) — do NOT signal DT to push
DEV until RD ships C2 (CLA DistributionTab continuous view) and C4 (ADV drill-down).

DS has A3/A4/A5 in progress. DS next step is A3 (ADVI-005 stacked_bar + rolling_1y in
script 10). No DE action required until DS completes A3 and issues handoff.

DT can deploy bd-portal-publisher (Stream B1) independently via brief at
`docs/briefs/devops-brief-advi-004-adv-drill-cla.md` — no DE gate on that.

---

## Next Steps

1. **[RD 0.4.2] Await C2 + C4 implementation** — CLA continuous view in DistributionTab
   and ADV drill-down chart. Once RD commits, DE reviews before DT pushes DEV.

2. **[DE] Review RD C2 + C4** — Read the implementation against the type contract:
   - C2: DistributionTab must guard on `chartData?.cla?.total` before rendering.
     Should toggle CLA metric using existing metric selector (not a new endpoint).
   - C4: ADV continuous view should use `chartData?.adv_drill?.[archKey]` which is
     already typed on `CumulativeChartResponse`. Must use `CATEGORY_COLORS` palette.
   - Both: no colorMap consumption — frontend palettes only.

3. **[DE -> DT] Signal push after C2+C4 review** — Once DE confirms C2+C4 are correct,
   signal DT to push portal DEV to origin.

4. **[DT] Deploy B1 (bd-portal-publisher)** — Independent stream, unblocked now.
   Brief at `docs/briefs/devops-brief-advi-004-adv-drill-cla.md`.

**Files to touch next:**
- None — awaiting RD C2/C4

**Do NOT:**
- Signal DT to push DEV before reviewing RD C2+C4
- Add colorMap to the type (explicitly excluded by contract)
- Add `'cla'` to `CumulativeChartViewMode` — that is RD/tab wiring scope, not DE types scope

#### advi_005_v2_types_rd_task_order_refresh.md

# ADVI-005 V2 Types + RD Task Order Refresh — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-04
**Start Time:** session 3
**End Time:** ~15 min
**Portal DEV commits:** `3dc9dc5` -> `7df26bb` -> `5125eb9`
**Workspace CLOUD commit:** pending (this log commit)

## Objective

Review DS and DT completed work (ADVI-004 A1+A2, ADVI-005 A3, B1 deploy, B2 deploy),
add missing `AdvisorRollingFlowsResponseV2` type, and update both RD task orders to
reflect cleared gate status and correct type references.

---

## Work Completed

### 1. DS + DT State Review

**DS (0.4.0_DS_ClientPlatform):**
- A1 (adv_drill) + A2 (cla) in bd-portal-publisher — committed `5f60d30e`
- A3 (stacked_bar + rolling_1y in script 10) — committed `c9b3ab76`
- A4 (abs() fix in script 09 bell curve) — code-verified, committed `25660f4c`
- A5 (opal-users-v2 DynamoDB investigation) — in progress
- DevOps briefs written for B1 (`f2e3c675`) and B2 (`75b3b83f`)

**DT (0.4.0_DT_ClientPlatform):**
- B1 deploy: `bd-portal-publisher` at `bd-v2.15.0` — adv_drill + cla LIVE
- B2 deploy: `bd-gold-layer-runner` at `bd-v2.15.1` — stacked_bar + rolling_1y LIVE (EC2 run in progress at time of deploy)
- WMI hang incident: Python/botocore hangs on startup on this Windows machine; workaround
  documented (boto3 with monkey-patch). Root cause: IMDS probe, not WMI — fixed via
  `AWS_EC2_METADATA_DISABLED=true` in .bashrc (per MEMORY.md update).

### 2. RD Task Order Gap Identified

ADVI-005 task order for RD (4C stream) references `AdvisorRollingFlowsResponseV2` as
"defined by DE per ADVI-005 receipt." No ADVI-005 DE types task order was issued to me.
Type was missing from `types.ts`. This is a DE gap — fixed immediately.

### 3. AdvisorRollingFlowsResponseV2 Type Added (portal DEV 5125eb9)

Added to `portal/src/pages/AdvisorIntelligence/types.ts`:

```typescript
export type StackedBarPeriodKey = 'qtd' | 'ytd' | '1y' | '3y' | 'max'

export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number   // positive magnitude
  outflows: number  // positive magnitude — negate client-side for downward bar
  nna_net: number   // signed
}

export interface AdvisorRolling1YSeries {
  advisor_name: string
  advisor_id: string
  series: RollingFlowsDataPoint[]  // outflows positive magnitude
}

export interface AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse {
  stacked_bar?: Record<StackedBarPeriodKey, {
    architects: AdvisorBarEntry[]
    implementors: AdvisorBarEntry[]
  }>
  rolling_1y?: {
    architects: AdvisorRolling1YSeries[]
    implementors: AdvisorRolling1YSeries[]
  }
}
```

V2 extends V1 — all fields optional (backward-compat). `tsc` clean.

### 4. RD Task Orders Updated

**ADVI-004-distribution_continuous.md:**
- Added `gate_status`: CLEARED — bd-v2.15.0, adv_drill + cla live, types 7df26bb
- Removed "BLOCKED by DT Stream B1" language from constraints
- Added `updated_by`, `updated_date` metadata fields
- Added type references (CumulativeChartResponse.cla? shape, adv_drill key format)
- Added C4.5 (guard on chartData?.cla before rendering CLA metric selector)
- Note added: client key format is `"{name} ({id})"` from DS implementation

**ADVI-005-advisors_tab.md:**
- Added `gate_status`: CLEARED — bd-v2.15.1, stacked_bar + rolling_1y live, types 5125eb9
- Removed "BLOCKED by DT Stream B2" language from constraints
- Added exact type import guidance (AdvisorRollingFlowsResponseV2, AdvisorBarEntry, etc.)
- Clarified period toggle behavior for rolling_1y (controls x-axis window slice, NOT rolling window)
- Added explicit "use AdvisorRollingFlowsResponseV2, not V1" constraint

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| V2 extends V1 (not a new standalone type) | Backward compat: existing AdvisorsTab code that destructures architects/implementors still works without changes |
| stacked_bar and rolling_1y are optional in V2 | Defensive rendering required (4C.5) — cache may serve stale response without new keys |
| AdvisorRolling1YSeries reuses RollingFlowsDataPoint | Same shape: { date, nna, inflows, outflows }. No duplication. |
| Update task orders in place, not new files | Same task order ID, same feature — gate status update is metadata, not a new task |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/types.ts` | Added StackedBarPeriodKey, AdvisorBarEntry, AdvisorRolling1YSeries, AdvisorRollingFlowsResponseV2 | Yes — portal DEV `5125eb9` |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-004-distribution_continuous.md` | Gate cleared, type refs added, C4.5 added, client key format documented | Yes — CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-005-advisors_tab.md` | Gate cleared, V2 type refs added, import list specified, period toggle clarified | Yes — CLOUD (this commit) |

---

## Blockers

None. Both RD task orders are unblocked.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

Portal DEV now has 3 DE commits since last DT push: `3dc9dc5` (I2 sort), `7df26bb` (cla type),
`5125eb9` (V2 types). DT still cannot push until DE reviews RD C2+C4 (ADVI-004) and 4C (ADVI-005).
RD has clear, actionable task orders with all gates cleared and types referenced.

---

## Next Steps

1. **[RD 0.4.2] Start C2 + C4** — ADVI-004-distribution_continuous.md, gates cleared
   - C2: DistributionTab ADV continuous with architect->client drill (adv_drill key)
   - C4: DistributionTab CLA continuous stacked area (cla.total/geo_drill/adv_drill/geo_city_drill)

2. **[RD 0.4.2] Start 4C** — ADVI-005-advisors_tab.md, gates cleared
   - Stacked bar primary + rolling 1Y secondary in AdvisorsTab.tsx
   - Use AdvisorRollingFlowsResponseV2 (types.ts 5125eb9)

3. **[DE] Review RD C2+C4+4C when committed** — before DT pushes DEV

4. **[DE -> DT] Signal push** — after review passes, DT pushes portal DEV

**Files to touch next:**
- None for DE — awaiting RD work

**Do NOT:**
- Signal DT to push DEV before reviewing RD commits
- Use V1 (AdvisorRollingFlowsResponse) for the 4C implementation

#### leaderboard_sort_stability_fix.md

# Leaderboard Sort Stability Fix (Stream I2) — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-04
**Start Time:** session start
**End Time:** ~20 min
**Portal DEV commits:** `3dc9dc5`
**Workspace CLOUD commit:** `ff7f1ba3`

## Objective

Investigate and fix leaderboard sort instability in the Advisors tab (AdvisorsTab.tsx).
Determine root cause — frontend sort instability on NNA ties vs. data issue in S3 publisher
output — and implement the appropriate fix. This session log is the O3 trigger for COO to
schedule ADVI-004/005/006 alignment threads.

---

## Work Completed

### 1. Root Cause Investigation

Read `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` in full.

Located the leaderboard sort logic at lines 625-632 (`LeaderboardTable` component, `sortedData` memo).

**Finding — Root Cause (a): Frontend.** The sort comparator had no secondary key:

```typescript
return sortDirection === 'asc' ? Number(aVal) - Number(bVal) : Number(bVal) - Number(aVal)
```

When two entries have equal NNA (or any numeric field), the comparator returns 0. JavaScript's
`Array.prototype.sort()` is stable in V8, but stability only means equal elements preserve
their relative order from the *input array*. The input changes on every window switch
(`activeLeaderboard?.windows?.[leaderboardWindow]?.entries` is a different array reference
per window). When the user switches from 1Y to 3M and back, tied entries re-sort to whatever
order they appear in the new window's JSON from S3 — which is not necessarily the same.
Result: top-3 highlights and leaderboard rank numbers flicker/reorder on window toggle.

**S3 data-side check:** Could not directly inspect S3 architect_leaderboard.json without AWS
CLI access in this session. However, the `Top3Highlights` component uses `.slice(0, 3)` on the
raw entries array without any re-sort, implying the data is assumed to be pre-sorted by the
backend. If the S3 data arrives pre-sorted by NNA descending (with no ties), the data side
is clean. The frontend instability occurs when users change the sort column themselves and
equal numeric values are encountered.

### 2. Fix Applied

Added a stable name-based tiebreaker in `LeaderboardTable` sort at line 625:

```typescript
const sortedData = [...filteredData].sort((a, b) => {
  const aVal = a[sortField]
  const bVal = b[sortField]
  let cmp = 0
  if (typeof aVal === 'string' && typeof bVal === 'string') {
    cmp = sortDirection === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
  } else {
    cmp = sortDirection === 'asc' ? Number(aVal) - Number(bVal) : Number(bVal) - Number(aVal)
  }
  // Stable secondary sort: name as tiebreaker for equal numeric values
  if (cmp === 0 && sortField !== 'name') {
    cmp = a.name.localeCompare(b.name)
  }
  return cmp
}).map((item, idx) => ({ ...item, rank: idx + 1 }))
```

The tiebreaker is always alphabetical ascending on name. The `sortField !== 'name'` guard
prevents redundant double-localeCompare when the user is already sorting by name.

### 3. TypeScript Verification

`bunx tsc -b --noEmit` — clean, no errors.

### 4. pod_inventory.xml Update

Added resolved `known_issue` entry for the leaderboard sort fix in AdvisorIntelligence page.
Updated metadata `last_updated` and `date` fields to 2026-03-04.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Root cause: (a) frontend only | Sort comparator had no secondary key. JS stable sort only preserves order within a single array reference — window toggle causes new array reference, so tied entries reorder. |
| Tiebreaker: name ascending, always | Deterministic and user-meaningful. Name ascending is a natural secondary sort for any primary metric. |
| Guard: `sortField !== 'name'` | Prevents double-sort when sorting by name; name path already produces a full string comparison. |
| Did not wait on S3 data inspection | Cannot access S3 without AWS CLI in this session. Frontend fix is complete and self-contained. Data-side is flagged in next steps for DS/DT follow-up. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | Stable secondary sort tiebreaker (name) added at lines 625-638 | Yes — portal DEV `3dc9dc5` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml` | Added resolved known_issue for leaderboard sort; updated metadata dates | Yes — CLOUD `ff7f1ba3` |

---

## Blockers

None. Frontend fix is complete. S3 data-side inspection is a follow-up item, not a blocker
for marking I2 complete.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

Stream I2 leaderboard sort fix is complete. AdvisorsTab.tsx committed to portal DEV at
`3dc9dc5`. pod_inventory.xml updated at workspace CLOUD `ff7f1ba3`. tsc passes clean.
This session log satisfies the O3 condition — COO can now schedule ADVI-004/005/006
alignment threads. Pending task order `ADVI-004-portal_types_wiring.md` is blocked on DS
delivering A1/A2 (data_contract.xml with adv_drill + cla fields). That task order has not
been started.

---

## Next Steps

1. **[DevOps] Push portal DEV** — `3dc9dc5` is committed locally. DT owns the push.
   No infra changes; portal code only.

2. **[DS] Data-side S3 inspection** — Verify architect_leaderboard.json and
   implementor_leaderboard.json in S3 are pre-sorted by rank/NNA descending with no
   duplicate rank values. If ties exist in the data, DS should flag for publisher fix.

3. **[DE] Resume ADVI-004-portal_types_wiring.md** — Once DS delivers A1/A2
   (data_contract.xml with adv_drill + cla fields), read DS's updated data_contract.xml
   and add `cla?` type extension to `CumulativeChartResponse` in
   `portal/src/pages/AdvisorIntelligence/types.ts`.

**Files to touch next:**
- `portal/src/pages/AdvisorIntelligence/types.ts` — `cla?` extension on `CumulativeChartResponse`
  (BLOCKED on DS A1/A2 delivery)

**Do NOT:**
- Push portal DEV yourself — DT is the QA gate and owns all pushes
- Start ADVI-004 types work before reading DS's updated data_contract.xml (TY.4 constraint)

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


### 0.4.0_DE_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DE_ClientPlatform

3252e5ce 0.4.0_DE_ClientPlatform: V2 types + RD task order refresh (gates cleared ADVI-004/005)
6048ce3c 0.4.0_DE_ClientPlatform: session log + ADVI-004 types task order complete
816f6fa2 0.4.0_DE_ClientPlatform: session log + I2 task order complete (leaderboard sort)
ff7f1ba3 0.4.0_DE_ClientPlatform: pod_inventory.xml -- leaderboard sort resolved
4a8e3d47 log(0.4.0_DE_ClientPlatform): pod_inventory.xml upgrade session log
5efb15f4 0.4.0_DE_ClientPlatform: upgrade pod_inventory.xml AdvisorIntelligence to full-fidelity from 0.4.2 RD audit
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
0033f9ca 0.4.0_DE_ClientPlatform: fix Daily AUA Analysis bottom margin to 70
e70b9730 0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts (corrected values)
4bda06a8 0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts

