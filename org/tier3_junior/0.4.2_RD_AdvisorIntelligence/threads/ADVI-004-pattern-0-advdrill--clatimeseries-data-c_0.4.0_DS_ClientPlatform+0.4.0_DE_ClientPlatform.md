# Thread Receipt: Pattern 0: adv_drill + cla_timeseries data contract

**Thread ID:** ADVI-004-pattern-0-advdrill--clatimeseries-data-c
**Project Serial:** ADVI-004
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-03T22:05:10Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.0_DE_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-03T22:04:56Z
signal: continue
---

## Pattern 0 Alignment -- adv_drill + cla_timeseries

I am the COO convening this alignment thread. Two publisher outputs are needed for the Distribution tab: adv_drill (per-architect NNA time series for ADV continuous view) and cla_timeseries (NMNC/NMEC AUM composition over time for continuous CLA view). Neither exists today. Before any code is written, DS, DE, and RD must agree on exact JSON shapes, TypeScript interfaces, and chart constraints.

This is a re-run. The previous thread produced contracts with three critical gaps: (1) cla_timeseries was missing geo_drill for city-level drill-down, (2) colorMap values were placeholders not real portal tokens, (3) NMNC/NMEC classification logic was assumed without verification. Fix all three this time.

**Turn order:** DS -> DE -> RD. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read lambda_function.py (the publisher Lambda in context) and data_contract.xml before answering. Cite specific function names and field names from those files.

1. For adv_drill: what per-architect and per-client NNA data currently exists? Name specific parquet files, column names, and cardinality. What cumulative NNA time series can you produce per architect -> per client? What date range and density?

2. For cla_timeseries: how is NMNC vs NMEC CURRENTLY defined in the gold layer output? Read data_contract.xml and the publisher Lambda to find the existing definition -- do not assume a 12-month first_seen_date rule. Name the specific field, table, or derivation logic. Can you produce daily NMNC AUM and NMEC AUM at total, geo (state), geo_drill (city within state), and adv (architect) grains?

3. For both: describe the exact output shape you will produce -- field names, nesting, value types (dollars, cumulative, absolute). Show how it relates to existing geo/geo_drill structure in timeseries_chart.json. Include a colorMap field per series with values that reference the existing portal color system (RD will confirm the exact tokens).

**DE (0.4.0_DE_ClientPlatform):** Read types.ts before responding. Specify the exact TypeScript interface names and shapes the portal needs. Name the query key and endpoint path for each.

**RD (0.4.2_RD_AdvisorIntelligence):** Read DistributionTab.tsx before responding. Identify what color tokens are currently in use and specify the exact colorMap values (portal tokens or hex). Flag any chart constraint that affects the data model.

**IMPORTANT (M2):** If any agent cites a field, S3 path, or interface name without naming the file it came from, the next agent must ask for the exact path before treating it as ground truth.

**Final turn must produce a structured contract block with:**
- adv_drill JSON schema (exact field names, types, nesting)
- cla_timeseries JSON schema (including geo_drill for city-level drill)
- colorMap spec with actual portal token names or hex values
- TypeScript interface names (DE confirms)
- S3 key / output location for each
- NMNC/NMEC classification logic (agreed definition verified against existing code, not assumed)


---

## 001.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 1
timestamp: 2026-03-03T22:06:10Z
signal: continue
---

### 1) adv_drill — what data exists today, and what we can produce

**What exists in the BD publisher Lambda today (source: `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`):**
- `load_all()` loads:
  - `gold/client_performance.parquet` as `perf` with columns:
    - `date`, `relationship_id`, `total_aua`, `cum_inflows`, `cum_outflows`, `nna`, `num_accounts`, etc.
  - `gold/views/nna_aua_by_advisor.parquet` as `adv` with columns:
    - `date`, `architect`, `total_aua`, `cum_inflows`, `cum_outflows`, `nna`, `num_relationships`, `num_accounts`
  - `gold/client_dimension.parquet` as `cdim` with columns:
    - `relationship_id`, `relationship_name`, `first_seen_date`, `primary_architect`, `primary_state`, etc.
- `build_timeseries_chart()` currently produces:
  - `adv` view = **AUA by architect** (stacked), built from `adv.total_aua` (not NNA).
  - `nna` view = firm-level cumulative NNA/inflows/outflows from `perf` (relationship grain aggregated to firm).
  - `geo_drill` exists (state -> city AUA) if `gold/views/nna_aua_by_geography_city.parquet` exists.
  - **No `adv_drill` key exists today.**

**What per-architect and per-client NNA data exists:**
- Per-architect daily cumulative NNA exists in `gold/views/nna_aua_by_advisor.parquet` (`adv` df), column `nna` (cumulative from inception).
- Per-relationship daily cumulative NNA exists in `gold/client_performance.parquet` (`perf` df), column `nna` (cumulative from inception).
- Relationship -> architect mapping exists in `gold/client_dimension.parquet` (`cdim.primary_architect`) and also in `gold/accounts_dimension_latest.parquet` (`adim.architect`) but `cdim` is the cleanest relationship-level mapping.

**Therefore, we can produce `adv_drill` without any new gold tables** by:
- Joining `perf[['date','relationship_id','nna']]` to `cdim[['relationship_id','relationship_name','primary_architect']]`
- Filtering to relationships under a given architect
- Pivoting to daily series per relationship (client) and bucketing non-top relationships into `"Other"` (exactly like `geo_drill` buckets cities).

**Cardinality / density / date range:**
- Density: daily points (same as `perf.date` and current `timeseries_chart.json`).
- Date range: whatever is in `perf` (publisher currently uses `date_start = perf['date'].min()` and `date_end = perf['date'].max()`).
- Cardinality: for each architect in the top list (`top_architects` already computed in `build_timeseries_chart()`), we can include top N relationships by latest-day AUA (or by latest-day absolute NNA; we need to pick one). For parity with `geo_drill` (which ranks by latest-day `total_aua`), I recommend ranking relationships by **latest-day `total_aua`** from `perf` (available) to keep “top clients” stable and intuitive.

**Important note for DE/RD:** current `CumulativeChartView` in portal types is generic (`categories: string[]`, `data: [{date, ...dynamic keys}]`). So `adv_drill[architect]` can be a `CumulativeChartView` with categories = relationship display names (or IDs), and data points containing those keys.

---

### 2) cla_timeseries — how NMNC vs NMEC is currently defined (verified) and feasibility

**Verified current definition in publisher Lambda (source: `build_timeseries_chart()` in `bd-portal-publisher/lambda_function.py`):**
- The existing `timeseries_chart.json` key `aua` is described as:
  - `"Total AUA by client vintage (NMNC=new <=12mo, NMEC=existing >12mo)"`
- Implementation:
  - `perf_cohort = perf[['date','relationship_id','total_aua']].merge(cdim[['relationship_id','first_seen_date']])`
  - `months_since_first = (date - first_seen_date).days / 30.44`
  - `cohort = 'NMNC' if months_since_first <= 12 else 'NMEC'`
- So **NMNC/NMEC is currently a trailing-12-month “client vintage” classification based on `client_dimension.first_seen_date` relative to each row date**.
- This is also reflected in the data contract excerpt for `timeseries_chart.json` (source: `org/.../deliverables/data_contract.xml`, AdvisorIntelligence Source 2), which states NMNC = “within 12mo”.

So: we do NOT need to invent a new rule; the system already uses the 12-month vintage rule in the publisher Lambda for the `aua` time series.

**Can we produce daily NMNC vs NMEC AUM at required grains?**
- **Total (firm-wide):** yes, already exists as `timeseries_chart.json.aua` (NMNC/NMEC daily AUA).
- **Geo (state):** feasible using `perf` + `cdim.primary_state`:
  - join `perf(date, relationship_id, total_aua)` to `cdim(primary_state, first_seen_date)`
  - compute cohort per row-date as above
  - group by `date, state, cohort` and sum `total_aua`
  - then choose top states (same `TOP_N_GEO` logic) and bucket others to `"Other"` if needed.
- **Geo drill (city within state):** not currently available in `cdim` columns shown in `load_all()` (it has `primary_state` and `primary_country`, but no city). The existing `geo_drill` in `timeseries_chart.json` is built from a dedicated parquet `gold/views/nna_aua_by_geography_city.parquet` (city-level AUA), but that parquet does not include NMNC/NMEC split.
  - To satisfy the PRD requirement “CLA geo_drill (cities within state)”, we have two options:
    1) **Gold-layer change**: produce a city-level relationship mapping (relationship_id -> city) and/or a `nna_aua_by_geography_city`-like view with cohort split. This is higher effort and likely belongs in EC2 gold scripts.
    2) **Publisher-only approach** if we can source city from an already-loaded table. In current Lambda `load_all()`, we do not load any city field in `cdim` or `adim` (adim has `client_state`, `client_country` but no city). So with current inputs, **I cannot truthfully claim we can build CLA city drill purely in Lambda**.
- **Adv (architect):** yes, using `cdim.primary_architect` + cohort logic + `perf.total_aua` aggregation.
- **No adv_drill for CLA:** agreed with PRD; architect is terminal grain for CLA.

**Conclusion:** total/geo/adv CLA timeseries is doable in publisher Lambda with existing parquets. CLA geo_drill (state->city) is **not doable with current loaded columns** unless there is an existing relationship->city attribute somewhere else we can load (not present in the provided `load_all()` column lists). I need DE/COO confirmation whether city is required for CLA v1, and if yes, we likely need an EC2 gold enhancement to expose relationship city (or a cohort-split city view parquet).

---

### 3) Proposed exact output shapes (aligned to existing `timeseries_chart.json` patterns)

#### 3A) `adv_drill` addition to `gold/timeseries_chart.json`
Add optional key:
- `adv_drill: Record<string, CumulativeChartView>`

Where:
- record key = **architect category string exactly as it appears in `timeseries_chart.json.adv.categories`** (currently architect display names, plus `"Other"`).
- each `CumulativeChartView`:
  - `description`: string (e.g., `"Cumulative NNA by relationship for architect {X}"`)
  - `categories`: string[] of relationship labels (top N) plus optional `"Other"`
  - `data`: array of `{ date: 'YYYY-MM-DD', [relationship_label]: number }`
    - values are **cumulative NNA dollars** (same “graph goes up” convention as `nna` view; frontend diffs endpoints for period flows if needed)

Open question for DE/RD: do you want relationship keys to be `relationship_id` (stable) or `relationship_name` (readable but may collide)? I recommend:
- key = `relationship_id` (stable)
- label = `relationship_name` (display)
But `CumulativeChartView` today only has `categories: string[]` (no id/label split). If portal needs both, we’d need a schema extension (e.g., `category_metadata`). I will wait for DE guidance before locking this.

#### 3B) `cla_timeseries` addition to `gold/timeseries_chart.json`
Given the portal already has `metric === 'cla'` placeholder in continuous view, I propose we add a new top-level key (to avoid overloading existing `aua` which is already NMNC/NMEC by vintage but not drillable by geo/adv):

- `cla: { total: CumulativeChartView, geo: CumulativeChartView, adv: CumulativeChartView, geo_drill?: Record<string, CumulativeChartView> }`

Semantics:
- This is **AUM composition**, not NNA.
- Each data point contains **two categories only** at the leaf level: `nmnc` and `nmec` (lowercase) or `NMNC`/`NMEC` (uppercase). Existing `CATEGORY_COLORS` in `DistributionTab.tsx` supports both cases. For consistency with existing `timeseries_chart.json.aua.categories` (currently `['NMNC','NMEC']`), I recommend **uppercase**.

Proposed:
- `cla.total.categories = ['NMNC','NMEC']`
- `cla.total.data = [{date, NMNC: number, NMEC: number}]` (daily AUM)
- `cla.geo.categories = [top states + 'Other']` BUT this conflicts with needing NMNC/NMEC split. So instead:
  - Option 1 (preferred for stacked area): `cla.geo` is **state-level totals of NMNC AUM and NMEC AUM separately** requires 2D (state x cohort) which doesn’t fit `CumulativeChartView` cleanly.
  - Option 2: define `cla.geo` as **two-series only** (NMNC/NMEC) but filtered to a selected state via drill/search. That implies a different API contract (state selector param) which we do not have.
  - Option 3: define `cla.geo` as **top states, but values are NMNC%** (single metric) — but PRD explicitly wants stacked areas of dollars.

So I need to pause here: the PRD’s desired CLA continuous behavior (“stacked area chart where two areas are NMNC AUM and NMEC AUM; viewable at total, state, city, architect”) implies the chart is always two categories (NMNC/NMEC) and the *scope* changes (total vs a selected state vs a selected city vs a selected architect). That is not the same as current geo/adv continuous NNA behavior (many categories at once).

**Therefore the clean contract is not “cla.geo is top states”; it is “cla_geo_drill provides per-state two-series views”.**
Concretely:
- `cla.total`: firm-wide NMNC/NMEC AUM (2 series)
- `cla.geo`: state-level selector list (not a chart view) OR omit
- `cla.geo_drill[state]`: the 2-series NMNC/NMEC AUM for that state
- `cla.geo_city_drill[state][city]`: 2-series for that city (if available)
- `cla.adv_drill[architect]`: 2-series for that architect (terminal)

But the PRD text in context asked for:
```
cla: {
  total: CumulativeChartView          // categories: ['nmnc', 'nmec']
  geo: CumulativeChartView            // categories: top states
  adv: CumulativeChartView            // categories: top architects
  geo_drill: Record<state, CumulativeChartView>
}
```
I believe that structure is internally inconsistent with “two stacked areas” requirement unless the portal intends to show *many* stacked areas (states) for CLA, which contradicts “two colors only” (NMNC green, NMEC blue). I’m flagging this now so DE/RD can decide the intended UX.

My recommendation (data-model-first, matches “two colors only”):
- Continuous CLA chart should always be 2 categories (NMNC/NMEC).
- Drill/search changes the *population slice* (total vs selected state vs selected city vs selected architect).
- That means we should publish:
  - `cla_total` (2-series)
  - `cla_geo` as a list of available states (for search UI) + per-state 2-series in `cla_geo_drill`
  - `cla_adv` as a list of available architects + per-architect 2-series in `cla_adv_drill`
This is a different schema than the PRD draft block; I need DE to confirm which UX they’re implementing.

---

### 4) colorMap requirement (what I can commit to now)

In the current portal `DistributionTab.tsx`, colors are primarily **hex strings** (e.g., `GEO_COLORS`, `ADV_COLORS`, `CATEGORY_COLORS`), and the donut reads `seg.color` if present, else falls back to palettes.

In the publisher Lambda today, segment colors are hex strings (e.g., `'#4CAF50'`, `'#2196F3'`, etc.) in `build_partner_analytics()` (though that Lambda path is disabled for partner_analytics; EC2 script 09 owns it). For `timeseries_chart.json`, there is currently **no colorMap**.

Given that, I propose:
- For `adv_drill` and any new CLA timeseries keys, **do not add colorMap initially**; let portal assign colors deterministically from existing palettes (as it already does for continuous charts).
- If COO insists on a backend-provided `colorMap`, we can add:
  - `color_map: Record<string, string>` where values are hex strings (not portal tokens), because the backend does not know portal CSS token names and the portal already accepts hex in multiple places.

I need RD to confirm whether they truly require “portal token names” vs hex. The current code strongly suggests hex is acceptable and already used.

---

### Decisions / questions for DE + COO (need answers before I code)
1. **adv_drill keys:** should categories be `relationship_id` (stable) or `relationship_name` (readable)? If readable, how do we avoid collisions?
2. **CLA continuous UX:** is the continuous CLA chart intended to show:
   - (A) two series only (NMNC/NMEC) with drill selecting the slice (my recommendation), or
   - (B) many series (states/architects) like existing geo/adv charts (contradicts “two colors only”)?
3. **CLA geo_drill city requirement:** do we have an existing relationship->city field available in gold (not shown in current Lambda loads)? If not, are we authorizing an EC2 gold enhancement to expose it? Without that, CLA city drill cannot be produced truthfully.

Once DE answers (esp. #2), I can propose the final JSON schema block and then implement in `bd-portal-publisher/lambda_function.py` + update `data_contract.xml`.

---

## 002.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 2
timestamp: 2026-03-03T22:07:08Z
signal: continue
---

### DE readout (portal contract + constraints) — anchored to `portal/src/pages/AdvisorIntelligence/types.ts` + `DistributionTab.tsx`

#### 0) Ground truth: what the portal can ingest today (no new TS types required)
From `portal/src/pages/AdvisorIntelligence/types.ts`:

- **Continuous chart contract** is already generic:
  - `CumulativeChartView = { description: string; categories: string[]; data: CumulativeChartDataPoint[] }`
  - `CumulativeChartDataPoint = { date: string; [category: string]: string | number }`
- **CumulativeChartResponse** already supports:
  - `geo_drill?: Record<string, CumulativeChartView>`
  - `adv_drill?: Record<string, CumulativeChartView>`

From `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`:

- Continuous drill logic is already implemented generically:
  - `drillViewData = cohort === 'geo' ? data?.geo_drill?.[drillParent] : data?.adv_drill?.[drillParent]`
  - So **adding `adv_drill` to `timeseries_chart.json` is sufficient** for ADV continuous drill to “just work” (no new endpoint, no new query key).
- Color handling in continuous view:
  - Uses `getCategoryColor()` with (1) `categoryColorMap` (built from snapshot donut segments), else (2) `CATEGORY_COLORS` (NMNC/NMEC), else (3) palette fallback (GEO_COLORS/ADV_COLORS).
  - Therefore **backend-provided colorMap is not required** for continuous charts to be stable.

#### 1) Endpoints + query keys (no changes)
Per `portal/src/api/endpoints/advisor-intelligence.ts` usage in `DistributionTab.tsx`:

- `getCumulativeChart()` -> `GET /api/scoped/advisor-intelligence/timeseries_chart.json`
  - React Query key in `DistributionTab.tsx`: `['advisor-intelligence', 'cumulative-chart']`
- So both **adv_drill** and any **cla_timeseries** additions must land inside the same S3 object:
  - `opal-data-bd/gold/timeseries_chart.json` (written by `bd-portal-publisher`)

No new endpoint should be introduced for Pattern 0.

---

### 2) adv_drill contract — DE decision points + recommendation

**Portal constraint:** `adv_drill` must be `Record<string, CumulativeChartView>` (per TS type). Each view’s `categories` must be strings that also appear as keys in each `data[]` point.

**Key decision (DS asked): relationship_id vs relationship_name**
- If DS uses `relationship_name` as the category key, collisions are possible and would silently merge series in the chart (bad).
- If DS uses `relationship_id` as the category key, it is stable and collision-free, but less readable in legend.

**Recommendation (DE):**
- Use **relationship_id as the category key** in `adv_drill[architect].categories`.
- For readability, DS should format the category string as:  
  `"{relationship_name} ({relationship_id})"`  
  This stays within the existing `string[]` categories contract (no schema extension), avoids collisions, and gives RD a readable legend/search target.

**Shape (must match existing TS):**
```ts
// in CumulativeChartResponse
adv_drill?: Record<string, CumulativeChartView>
```
Where:
- `adv_drill[architectKey].categories = [clientKey1, clientKey2, ..., 'Other'?]`
- `adv_drill[architectKey].data = [{ date: 'YYYY-MM-DD', [clientKey1]: number, ... }]`
- Values: **cumulative NNA dollars** (consistent with `nna` view semantics; frontend diffs endpoints for period flows).

---

### 3) cla_timeseries contract — portal UX constraint conflicts (needs resolution now)

DS correctly flagged an inconsistency: the PRD text wants **two colors only** (NMNC green, NMEC blue) and a **stacked area** of NMNC vs NMEC AUM over time. That implies **exactly two categories** at any time.

But the draft schema in the PRD context block suggests:
- `cla.geo.categories = top states` and `cla.adv.categories = top architects`  
That would create many stacked areas (states/architects), which violates “two colors only”.

**Portal implementation reality (DistributionTab.tsx today):**
- Continuous view currently assumes:
  - For `metric !== 'nna' && metric !== 'cla'`, it renders stacked areas for `viewData.categories` (many categories).
  - For `metric === 'cla'`, it early-returns “Coming soon” placeholder.
- So we have freedom to implement CLA continuous as a **separate render path** that expects exactly two categories.

**DE decision (proposed): adopt “always 2-series, drill changes slice” model**
This matches the PRD’s “two colors only” requirement and avoids the inconsistent “top states as categories” idea.

Concretely, I propose the CLA timeseries additions to `timeseries_chart.json` be:

```json
"cla": {
  "total": { "description": "...", "categories": ["NMNC","NMEC"], "data": [ { "date": "...", "NMNC": 0, "NMEC": 0 } ] },
  "geo_drill": { "TX": { "description": "...", "categories": ["NMNC","NMEC"], "data": [ ... ] } },
  "geo_city_drill": { "TX": { "Austin": { "description": "...", "categories": ["NMNC","NMEC"], "data": [ ... ] } } },
  "adv_drill": { "Travis Penfield": { "description": "...", "categories": ["NMNC","NMEC"], "data": [ ... ] } }
}
```

Notes:
- This **does not require** `cla.geo` or `cla.adv` as multi-category views.
- It does require portal work (RD) to:
  - Add `metric === 'cla'` continuous rendering path that reads `data.cla.total` by default
  - Add search + drill selection that swaps the view to `geo_drill[state]`, then optionally `geo_city_drill[state][city]`, or `adv_drill[architect]`
- This is consistent with the PRD behavior: “viewable at total, state, city, architect”.

**Blocking question for DS (must be answered with file/column evidence):**
- Can DS produce **relationship -> city** mapping from existing gold inputs?  
In the provided `bd-portal-publisher/lambda_function.py` `load_all()` column lists, I only see:
  - `cdim`: `primary_state`, no city
  - `adim`: `client_state`, no city
So CLA city drill likely requires a gold-layer enhancement (EC2) unless there is an existing parquet with relationship-level city not currently loaded.

If city is truly required for CLA continuous v1, we should treat it as **gold-layer dependency** (DS + DT/AE PartnerETL), not a publisher-only change.

---

### 4) colorMap spec (portal reality)
COO asked for “portal token names or hex values”. In `DistributionTab.tsx`, the system already uses **hex strings** extensively:
- `GEO_COLORS`, `ADV_COLORS`, `CITY_COLORS`, `CLIENT_COLORS`, `CATEGORY_COLORS` are all hex.
- Snapshot donut uses `seg.color` (hex) if present.

**DE position:** backend should emit **hex** if it emits anything; portal token names are not used in these chart paths today.

Also: for `timeseries_chart.json`, continuous charts do not currently consume a backend colorMap at all. So I recommend **no colorMap field** in `timeseries_chart.json` additions for Pattern 0. If we later need it, we can add an optional `color_map: Record<string,string>` at the view level without breaking existing parsing.

---

### 5) What I need from DS in next turn (to converge)
1. Confirm you will implement `adv_drill` inside `gold/timeseries_chart.json` (same object) and that architect keys match `adv.categories` strings exactly (so drillParent lookup works).
2. For CLA continuous: confirm whether you agree with the **2-series + drill-slice** schema (total + geo_drill + geo_city_drill + adv_drill), and whether city drill is feasible without new gold inputs. If not feasible, explicitly mark “CLA geo_city_drill blocked; requires gold-layer relationship->city field”.

Once DS confirms, I will issue a short RD guidance note (what to render + which keys to read) and we can converge on the final structured contract block.

---

## 003.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 3
timestamp: 2026-03-03T22:07:55Z
signal: continue
---

### RD readout (DistributionTab constraints + color spec) — anchored to `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`

#### 1) Ground truth: what colors the portal uses today (and what backend should emit)
In `DistributionTab.tsx`, all chart colors are currently **hex strings**, not portal token names:

- Palettes:
  - `GEO_COLORS`, `ADV_COLORS`, `CITY_COLORS`, `CLIENT_COLORS` are all hex arrays.
  - `OTHER_COLOR = '#6B7280'`
- Category colors:
  - `CATEGORY_COLORS` maps `NMNC/nmnc` to `'#16A34A'` and `NMEC/nmec` to `'#2563EB'` (plus Other).
- Snapshot donut:
  - Uses `seg.color` if present; otherwise falls back to the palettes above.
- Continuous stacked area:
  - Uses `getCategoryColor()` which prefers:
    1) `categoryColorMap` derived from snapshot donut segment keys (hex),
    2) `CATEGORY_COLORS` (hex),
    3) palette fallback (hex).

So for this thread’s “colorMap values must be real portal tokens or hex”: **hex is the only format actually used in this file today**. I recommend backend emits **hex** if it emits anything; otherwise omit colorMap entirely (portal already assigns deterministic colors).

#### 2) adv_drill: portal drill mechanics + key constraints
Continuous drill is already wired:

- `drillParent` is set by clicking a legend item (category string).
- Drill lookup is:
  - `data?.adv_drill?.[drillParent]` for ADV cohort.

Therefore the backend contract must satisfy:

1) **Top-level key:** `adv_drill?: Record<string, CumulativeChartView>` inside `timeseries_chart.json` (already in TS type).
2) **Record key alignment:** the `adv_drill` record keys must match the **exact strings in `timeseries_chart.json.adv.categories`** (because `drillParent` is literally the category string).
   - If `adv.categories` are architect display names (as in current publisher code), `adv_drill` must use those same display names as keys.
3) **Child view shape:** each `CumulativeChartView` must have:
   - `categories: string[]` where each category string is also a key in each `data[]` point.
   - `data: [{ date: 'YYYY-MM-DD', [category]: number }]`

On DS vs DE question (relationship_id vs relationship_name): from a pure UI standpoint, I agree with DE’s recommendation to avoid collisions by making the category string unique. Since we cannot add metadata without changing TS types, the safest UI-friendly approach is:

- category string = `"Relationship Name (relationship_id)"` (still a string, collision-resistant, readable in legend + search).

#### 3) cla_timeseries: portal UX constraint (two colors only) and what I need from backend
For **continuous CLA**, the PRD requirement is “two colors only” (NMNC green, NMEC blue) and a stacked area where the two areas are NMNC AUM and NMEC AUM. That implies:

- At any given chart render, `categories` must be exactly `['NMNC','NMEC']` (or lowercase variants; current code supports both, but uppercase matches existing `timeseries_chart.json.aua.categories`).

I agree with DE: CLA continuous should be a **2-series view where drill/search changes the slice**, not a “top states as categories” multi-series chart (that would violate the two-color rule).

So the backend contract I can implement cleanly is:

- `timeseries_chart.json` adds a top-level `cla` object with:
  - `cla.total: CumulativeChartView` (2 categories: NMNC/NMEC)
  - `cla.geo_drill: Record<stateKey, CumulativeChartView>` (each is 2 categories NMNC/NMEC)
  - `cla.geo_city_drill: Record<stateKey, Record<cityKey, CumulativeChartView>>` (each is 2 categories NMNC/NMEC) **REQUIRED by PRD**, but I understand DS may be blocked by missing relationship->city mapping in current Lambda inputs.
  - `cla.adv_drill: Record<architectKey, CumulativeChartView>` (each is 2 categories NMNC/NMEC; architect is terminal for CLA)

Portal-side, I will implement a dedicated `metric === 'cla'` continuous render path that:
- defaults to `data.cla.total`
- allows drill selection to swap to `geo_drill[state]`, then `geo_city_drill[state][city]`, or `adv_drill[architect]`
- uses fixed colors from `CATEGORY_COLORS`:
  - NMNC = `#16A34A`
  - NMEC = `#2563EB`

#### 4) Critical blocker I need DS to answer (with file/column evidence)
PRD gap (must not repeat ADVI-001): **CLA geo_drill must include city-level drill**.

From the provided `bd-portal-publisher/lambda_function.py` `load_all()` column lists, I do not see a relationship-level city field in `cdim` or `adim`, so DS may not be able to build `cla.geo_city_drill` without a gold-layer enhancement.

I need DS to confirm one of these, explicitly:
- (A) There *is* an existing gold parquet/column that provides `relationship_id -> city` (name the parquet key and column), so publisher Lambda can build CLA city drill, or
- (B) It does not exist today; CLA city drill requires a gold-layer change (EC2 script) and is blocked until that’s added.

#### 5) Summary of RD “colorMap spec” for final contract block
- **Preferred:** no colorMap fields added for Pattern 0; portal assigns colors deterministically.
- **If backend must provide:** `color_map: Record<string, string>` where values are **hex strings** only (e.g., `'#16A34A'`), not token names.

#### 6) What I will change in portal once backend lands (for planning)
- `DistributionTab.tsx`:
  - Implement `metric === 'cla'` continuous view (replace “Coming soon”) reading `data.cla.*`.
  - Add search + drill UI for CLA similar to GEO/ADV drill, but always rendering 2-series NMNC/NMEC.
  - Ensure drill reset behavior on cohort/metric changes (already present for other metrics).

Questions remaining are primarily DS-side feasibility for CLA city drill and final naming/key alignment for `adv_drill` keys.

---

## 004.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 4
timestamp: 2026-03-03T22:08:22Z
signal: continue
---

### DS confirmation + final feasibility answers (anchored to `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` and existing portal types)

#### 1) adv_drill: I confirm I will implement this inside `gold/timeseries_chart.json` (same object, same endpoint)
- **File to change:** `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`
- **Function to extend:** `build_timeseries_chart(...)`
- **Output location (unchanged):** `s3://opal-data-bd/gold/timeseries_chart.json` (written by `_save_json(chart, 'gold/timeseries_chart.json')`)

**Key alignment guarantee (per RD requirement):**
- In current code, `adv.categories` are built from `top_architects` derived from `adv['architect']` values (display names) plus optional `"Other"`.
- I will key `adv_drill` by the **exact same architect strings** used in `adv.categories` (i.e., the values in `top_architects`, not a normalized key), so `data.adv_drill[drillParent]` resolves.

**Data sources / columns (already loaded by `load_all()`):**
- `perf` from `gold/client_performance.parquet`: `date`, `relationship_id`, `total_aua`, `nna` (cumulative)
- `cdim` from `gold/client_dimension.parquet`: `relationship_id`, `relationship_name`, `primary_architect`

**Series semantics:**
- `adv_drill[architect].data[*][clientCategory]` will be **cumulative NNA dollars** (from `perf.nna`, summed across relationships if “Other” bucket).
- Daily density and date range identical to existing `timeseries_chart.json` (driven by `perf['date']`).

**Category key choice (DE decision):**
- I will use collision-resistant category strings:
  - `"{relationship_name} ({relationship_id})"` when `relationship_name` is present
  - fallback: `"{relationship_id}"` if name missing
- This stays within existing `CumulativeChartView.categories: string[]` contract (no schema extension).

**Top-N + Other bucketing:**
- Mirror `geo_drill` pattern: choose top relationships per architect by **latest-day `total_aua`** (stable, intuitive), keep top N (I propose 9 to match `MAX_DRILL_CITIES=9`), bucket remainder to `"Other"`.

---

#### 2) cla_timeseries: NMNC/NMEC definition is already verified (and I will reuse it)
Anchored to `build_timeseries_chart()` in `bd-portal-publisher/lambda_function.py`:

- Existing cohort logic for `timeseries_chart.json.aua`:
  - join `perf(date, relationship_id, total_aua)` with `cdim(first_seen_date)`
  - compute `months_since_first = (date - first_seen_date).days / 30.44`
  - `NMNC` if `months_since_first <= 12` else `NMEC`

So for CLA continuous, I will **reuse this exact rule** (no new interpretation).

---

#### 3) cla_timeseries output shape: I agree with DE/RD “2-series + drill selects slice” model
I agree the PRD’s earlier draft block (`cla.geo.categories = top states`) conflicts with “two colors only”. The only consistent model is:

- every CLA chart view has `categories = ['NMNC','NMEC']`
- drill/search changes the slice (total vs a specific state vs a specific city vs a specific architect)

**Therefore I will implement in `timeseries_chart.json` a new top-level key:**
- `cla` (object), with these subkeys:

1) `cla.total: CumulativeChartView`
- `categories: ['NMNC','NMEC']`
- `data: [{date, NMNC: number, NMEC: number}]`
- values are **AUM dollars** (from `perf.total_aua` aggregated), not NNA.

2) `cla.geo_drill: Record<stateKey, CumulativeChartView>`
- `stateKey` will be the same state strings used elsewhere (e.g., `TX`, `CA`), sourced from `cdim.primary_state` (already loaded).
- each state view is again 2-series NMNC/NMEC AUM.

3) `cla.adv_drill: Record<architectName, CumulativeChartView>`
- keyed by architect display name (same string domain as `adv.categories`).
- each architect view is 2-series NMNC/NMEC AUM.

4) `cla.geo_city_drill`: **BLOCKED with current Lambda inputs**
- With the current `load_all()` column lists:
  - `cdim` includes `primary_state` but **no city**
  - `adim` includes `client_state` / `client_country` but **no city**
  - `geo_city` parquet (`gold/views/nna_aua_by_geography_city.parquet`) includes `state`, `city`, `total_aua` but **does not include relationship_id**, and therefore cannot be cohort-split into NMNC/NMEC using `first_seen_date`.
- Conclusion: **publisher Lambda cannot truthfully build `cla.geo_city_drill` today** without a relationship-level city attribute (relationship_id -> city) in some gold parquet.

This is the critical “do not repeat ADVI-001” gap: city drill for CLA requires a gold-layer enhancement.

---

#### 4) Infrastructure needed (gold-layer) to unblock CLA city drill (explicit request for AE/DevOps)
Infrastructure needed (AWS Engineer / DevOps task):
- New/extended gold parquet providing **relationship_id -> city** (and state) mapping, or a cohort-ready city view.
- Options (either is sufficient):
  1) Extend `gold/client_dimension.parquet` to include `primary_city` (and ensure it is populated), OR
  2) Produce a new parquet `gold/views/relationship_geography.parquet` with columns: `relationship_id, state, city` (plus country if needed), OR
  3) Produce a new cohort-ready aggregate view `gold/views/cla_aua_by_geography_city.parquet` with columns: `date, state, city, nmnc_aua, nmec_aua` (pre-aggregated).
- Used by: `bd-portal-publisher` Lambda (`infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`) to populate `timeseries_chart.json -> cla.geo_city_drill`
- Protocol: docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md §3.4 (if a new layer/package is needed; otherwise standard gold script upload process)

I will not implement this gold change myself in this thread; I’m documenting it as a required upstream dependency.

---

#### 5) colorMap: I will not add it (portal uses hex already)
Per RD/DE confirmation, portal chart code uses hex palettes and does not consume a backend colorMap for `timeseries_chart.json`. I will **omit colorMap** from these additions.

---

### Two final confirmations needed before I start coding (so we converge cleanly)
1) **COO/DE:** Is it acceptable to ship CLA continuous with `cla.total`, `cla.geo_drill`, `cla.adv_drill` first, and mark `cla.geo_city_drill` as blocked pending gold enhancement? (I can still structure the JSON so adding `geo_city_drill` later is non-breaking.)
2) **DE/RD:** For `cla.geo_drill` keys, do you want state abbreviations (`TX`) or normalized keys (`texas_tx`)? Current ecosystem uses abbreviations in `geo` categories (from `nna_aua_by_geography.parquet.state`), so I will default to abbreviations unless told otherwise.

Once I get those two answers, I can proceed to implement `adv_drill` + `cla` additions in `build_timeseries_chart()` and update `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml` accordingly.

---

## 005.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 5
timestamp: 2026-03-03T22:08:56Z
signal: continue
---

1) Yes — acceptable to ship CLA continuous **without** `cla.geo_city_drill` in v1, as long as we:
- keep the schema forward-compatible (i.e., add `cla.geo_city_drill` later without breaking existing consumers), and
- explicitly mark city drill as **BLOCKED on gold-layer relationship->city mapping** in the contract + DS session log + COO brief.

This preserves the “do not fabricate city drill” rule and still unblocks RD to implement CLA continuous for:
- total (firm-wide),
- state slice (via `cla.geo_drill[state]`),
- architect slice (via `cla.adv_drill[architect]`).

2) For `cla.geo_drill` keys: use **state abbreviations** (e.g., `"TX"`, `"CA"`) exactly as they appear in existing BD outputs:
- aligns with `timeseries_chart.json.geo.categories` (built from `gold/views/nna_aua_by_geography.parquet.state` in `build_timeseries_chart()`),
- aligns with current portal drill behavior where `drillParent` is literally the category string.

So: `cla.geo_drill` should be keyed by the same state strings used in `geo.categories` (and not normalized keys like `texas_tx`).

Contract note (so DS can proceed cleanly):
- `timeseries_chart.json` additions should be:
  - `adv_drill?: Record<string, CumulativeChartView>` (architect display name keys matching `adv.categories`)
  - `cla: { total: CumulativeChartView; geo_drill: Record<string, CumulativeChartView>; adv_drill: Record<string, CumulativeChartView>; geo_city_drill?: ... (future) }`
- No `colorMap` required; portal uses hex palettes (`CATEGORY_COLORS` etc.) in `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`.

Open item I’m flagging for the final contract block (COO visibility):
- `cla.geo_city_drill` is a **hard dependency** on adding relationship-level city to gold (e.g., `client_dimension.primary_city` or a new `relationship_geography.parquet`). Without `relationship_id -> city`, publisher cannot cohort-split city AUM into NMNC/NMEC.

---

## 006.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 6
timestamp: 2026-03-03T22:09:08Z
signal: continue
---

DE + DS alignment looks good from the portal side. Two concrete confirmations + one small portal-driven constraint to bake into the final contract block.

## 1) Confirmed: ship CLA continuous without `cla.geo_city_drill` (forward-compatible)
I agree with DE: we should ship Pattern 0 with:

- `timeseries_chart.json.adv_drill` (ADV continuous drill to relationship/client series)
- `timeseries_chart.json.cla.total` + `cla.geo_drill` + `cla.adv_drill`

…and explicitly mark `cla.geo_city_drill` as **BLOCKED** pending a gold-layer relationship->city mapping. Portal can render total/state/architect slices immediately; city drill can be added later without breaking.

Portal implementation note: in `DistributionTab.tsx` I will treat `cla.geo_city_drill` as optional and only show the “City” drill affordance when present.

## 2) Key alignment constraints (must be explicit in contract)
Anchored to `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` continuous drill lookup:

- `adv_drill` record keys MUST match `timeseries_chart.json.adv.categories` strings exactly (architect display names), because `drillParent` is literally the clicked legend category string.
- `cla.geo_drill` record keys MUST match `timeseries_chart.json.geo.categories` strings exactly (state abbreviations like `TX`, `CA`) for the same reason (drillParent is the category string).

This is critical; if DS normalizes keys (snake_case) the drill will silently fail.

## 3) Color spec (ground truth: hex only in this file)
Per `DistributionTab.tsx`, all palettes and category colors are hex strings:
- NMNC: `#16A34A`
- NMEC: `#2563EB`
- Other: `#6B7280`

So for the final contract block:
- **No `colorMap` field is required** for `timeseries_chart.json` additions.
- If leadership insists on a color map, it must be `Record<string, string>` with **hex values** (not token names). But again: portal does not consume it today.

## 4) Minor but important portal constraint: category strings must be unique
For `adv_drill[architect].categories`, I support DE’s recommendation and DS’s plan:

- category string should be collision-resistant and readable:
  - `"{relationship_name} ({relationship_id})"` (fallback to relationship_id if name missing)

Because `CumulativeChartView.categories` is `string[]` only (no id/label split), collisions would merge series.

## 5) Remaining question (for DS, to lock contract wording)
When DS buckets “Other” in `adv_drill`, please confirm:
- category name is exactly `"Other"` (capital O) to match existing portal handling (`OTHER_COLOR` and `buildColorMap()` treat `"Other"` specially).

If yes, I think we’re ready for COO’s final structured contract block.

---

## 007.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 7
timestamp: 2026-03-03T22:09:21Z
signal: converge
---

## Pattern 0 Contract — adv_drill + cla_timeseries (final DS confirmation)

### A) adv_drill (ADV continuous drill-down) — WILL SHIP in `timeseries_chart.json`

**Backend file / function (source of truth):**
- `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`
- Extend: `build_timeseries_chart(perf, adv, geo, cdim, today, geo_city=None)`

**S3 output (unchanged):**
- `s3://opal-data-bd/gold/timeseries_chart.json`

**Data inputs (already loaded in `load_all()`):**
- `gold/client_performance.parquet` (`perf`): `date`, `relationship_id`, `total_aua`, `nna` (cumulative)
- `gold/client_dimension.parquet` (`cdim`): `relationship_id`, `relationship_name`, `primary_architect`

**JSON addition (exact shape):**
- Add optional key at top level of `timeseries_chart.json`:
```json
"adv_drill": {
  "<architect_display_name>": {
    "description": "Cumulative NNA by relationship for architect <name>",
    "categories": ["<relationship_name> (<relationship_id>)", "...", "Other"],
    "data": [
      { "date": "YYYY-MM-DD", "<relationship_name> (<relationship_id>)": 123.45, "Other": 67.89 },
      ...
    ]
  }
}
```

**Key alignment constraints (portal-required):**
- `adv_drill` record keys MUST match `timeseries_chart.json.adv.categories` strings exactly (architect display names), because the portal drill lookup is `data.adv_drill[drillParent]`.

**Semantics:**
- Values are **cumulative NNA dollars** (from `perf.nna`, summed across relationships per day).
- Daily density and date range follow `perf.date` (same as existing `timeseries_chart.json`).

**Bucketing / uniqueness:**
- Top relationships per architect selected by **latest-day `total_aua`** (stable).
- Category string will be collision-resistant: `"{relationship_name} ({relationship_id})"` (fallback to `relationship_id` if name missing).
- Bucket remainder into **exactly `"Other"`** (capital O) — confirmed.

---

### B) cla_timeseries (Continuous CLA AUM composition) — WILL SHIP partially; city drill BLOCKED

**NMNC/NMEC definition (verified in existing publisher code):**
- From `build_timeseries_chart()` current `aua` view logic:
  - Join `perf(date, relationship_id, total_aua)` with `cdim(first_seen_date)`
  - Compute `months_since_first = (date - first_seen_date).days / 30.44`
  - `NMNC` if `months_since_first <= 12` else `NMEC`
- This exact rule will be reused for CLA timeseries (no new interpretation).

**JSON addition (exact shape; 2-series only, drill selects slice):**
Add a new top-level key:
```json
"cla": {
  "total": CumulativeChartView,
  "geo_drill": { "<STATE>": CumulativeChartView },
  "adv_drill": { "<architect_display_name>": CumulativeChartView }
  // "geo_city_drill": omitted for now (blocked)
}
```

Where each `CumulativeChartView` is:
```json
{
  "description": "...",
  "categories": ["NMNC", "NMEC"],
  "data": [
    { "date": "YYYY-MM-DD", "NMNC": 123.45, "NMEC": 678.90 },
    ...
  ]
}
```

**Grains included in v1:**
- `cla.total`: firm-wide NMNC/NMEC **AUM dollars** over time (from `perf.total_aua` aggregated by cohort).
- `cla.geo_drill[state]`: per-state NMNC/NMEC AUM over time.
  - State keys are **state abbreviations** (e.g., `"TX"`, `"CA"`) and MUST match the same string domain as `timeseries_chart.json.geo.categories`.
- `cla.adv_drill[architect]`: per-architect NMNC/NMEC AUM over time.
  - Architect keys are **display names** and MUST match `timeseries_chart.json.adv.categories`.

**Explicitly BLOCKED in v1 (cannot be produced truthfully with current Lambda inputs):**
- `cla.geo_city_drill` (state -> city -> NMNC/NMEC AUM timeseries)
- Reason (anchored to current `load_all()` columns):
  - `cdim` has `primary_state` but no city field
  - `adim` has `client_state/client_country` but no city field
  - `gold/views/nna_aua_by_geography_city.parquet` has `state/city/total_aua` but no `relationship_id`, so cannot cohort-split by `first_seen_date`

**Gold-layer dependency to unblock CLA city drill (for AE/DevOps):**
- Add relationship-level city mapping in gold, e.g.:
  - extend `gold/client_dimension.parquet` with `primary_city`, OR
  - new `gold/views/relationship_geography.parquet` with `relationship_id, state, city`, OR
  - pre-aggregated `gold/views/cla_aua_by_geography_city.parquet` with `date, state, city, nmnc_aua, nmec_aua`

---

### C) colorMap spec (resolved)
- No backend `colorMap` will be added for Pattern 0.
- Portal uses hex palettes already (see `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`), and continuous charts do not consume a backend color map.

---

### D) TypeScript interface names + endpoint (for completeness)
- Portal reads via existing:
  - `getCumulativeChart()` -> `GET /api/scoped/advisor-intelligence/timeseries_chart.json`
  - React Query key: `['advisor-intelligence', 'cumulative-chart']`
- Types already support:
  - `CumulativeChartResponse.adv_drill?: Record<string, CumulativeChartView>`
- `cla` is a new top-level key in the JSON; portal will need to treat it as an extension on `CumulativeChartResponse` (DE/RD will handle TS update as needed).

This closes the contract for Pattern 0.

---

## 008.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 8
timestamp: 2026-03-03T22:09:43Z
signal: converge
---

## Pattern 0 (ADVI-004) — DE final confirmation + contract lock

### 1) Contract is ACCEPTED as written by DS (turn 7), with one DE clarification
I accept DS’s final contract for:

- `adv_drill` added to **existing** `s3://opal-data-bd/gold/timeseries_chart.json`
- `cla` added to the same JSON with:
  - `cla.total`
  - `cla.geo_drill`
  - `cla.adv_drill`
- `cla.geo_city_drill` explicitly **BLOCKED** pending gold-layer relationship→city mapping

**DE clarification (TypeScript):** `portal/src/pages/AdvisorIntelligence/types.ts` currently defines:
- `CumulativeChartResponse` with `adv_drill?: Record<string, CumulativeChartView>` already
- but it does **not** include a `cla` key today

So portal work will require a TS extension (non-breaking) to add:
```ts
cla?: {
  total: CumulativeChartView
  geo_drill: Record<string, CumulativeChartView>
  adv_drill: Record<string, CumulativeChartView>
  geo_city_drill?: Record<string, Record<string, CumulativeChartView>> // future
}
```
No new endpoint, no new query key.

### 2) Key alignment rules (must be treated as hard requirements)
Anchored to `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` drill lookup:

- `timeseries_chart.json.adv_drill` record keys MUST match `timeseries_chart.json.adv.categories` strings exactly (architect display names).
- `timeseries_chart.json.cla.geo_drill` record keys MUST match `timeseries_chart.json.geo.categories` strings exactly (state abbreviations like `TX`, `CA`).
- `Other` bucket must be exactly `"Other"` (capital O) — DS confirmed.

### 3) ColorMap resolution (thread requirement satisfied)
Anchored to `DistributionTab.tsx`: charts use **hex** palettes (`CATEGORY_COLORS`, `GEO_COLORS`, etc.). Therefore:
- No `colorMap` field is required for `timeseries_chart.json` additions.
- If ever added later, it must be hex strings, not placeholder tokens.

### 4) NMNC/NMEC rule (verified, not assumed)
Anchored to `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` `build_timeseries_chart()`:
- NMNC/NMEC classification is trailing-12-month vintage using `cdim.first_seen_date` relative to each row date (`months_since_first <= 12 => NMNC else NMEC`).
- CLA timeseries reuses this exact rule.

### 5) Explicit blocker statement (for COO visibility)
`cla.geo_city_drill` is **not implementable in publisher Lambda** with current loaded inputs because there is no relationship-level city attribute; `gold/views/nna_aua_by_geography_city.parquet` lacks `relationship_id` so cannot be cohort-split. This requires a gold-layer enhancement (EC2) to add relationship→city mapping or a cohort-ready city aggregate.

### 6) Deployment / ownership reminder
- DS will implement backend changes in: `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` (DT deploys).
- RD will implement portal rendering for continuous CLA once `cla` lands (and ADV continuous drill will “just work” once `adv_drill` exists).
- No infra/Terraform changes expected for Pattern 0.

This thread is resolved; proceed to implementation + data_contract.xml update + DT deploy handoff.

---
