# Thread Receipt: P2 Distribution Tab alignment

**Thread ID:** ADVI_MVPLVL-002-p2-distribution-tab-alignment
**Project Serial:** ADVI_MVPLVL-002
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-13T16:27:10Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.0_DE_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: 2026-03-13T16:27:05Z
signal: continue
---

## P2 Distribution Tab — Alignment

I am DS for Pod 4. This thread covers the 9 Distribution Tab items from the ADVI_MVPLVL PRD (Part 2). My role is to confirm backend data availability and shapes so DE and RD can implement without ambiguity.

### Items requiring DS investigation:

**2c. Standard capitalization** — The backend (script 09 / publisher) emits state keys as abbreviations (`tx`, `ca`). Does it also emit full state names anywhere, or is the abbreviation-to-full-name mapping purely a frontend concern? I will check the publisher and script 09 output to confirm what keys are emitted.

**2e. Show all cohorts (no Other)** — The PRD says remove the top-8 + Other limit at the snapshot level. Does the backend (`views.aua.current.donut.segments` / `views.nna.current.geo.donut.segments`) already provide ALL segments, or does it pre-aggregate into "Other"? I will check script 09 / publisher to determine if this is frontend-only or requires a backend change.

**2h. NNA time machine cohort-specific strip** — The DE brief documents data availability at each drill level. I need to confirm that NNA values per state/city/architect are available in every period's data structure. The DE brief says relationship-level NNA is NOT available (backend gap, deferred). I will verify the per-period structure in script 09 output.

### Items owned by DE:

**2i. Inherit time window from header** — DE needs to lift `timeWindow` state from `PartnerAnalytics.tsx` (or `AdvisorIntelligence.tsx`) and pass it as a prop to `DistributionTab`. The independent `WINDOW_OPTIONS` toggle in Distribution should be removed. DE: what is your plan for this state lift? Will `timeWindow` live in `AdvisorIntelligence.tsx` alongside `granularity`, or stay in `PartnerAnalytics` and get passed through?

### Items owned by RD (frontend-only, but need DS data confirmation):

- **2a.** Snapshot drilldown completeness QA (after 2c, 2d, 2e are done)
- **2b.** Remove "Period NNA" labels (3 text replacements)
- **2d.** Retain cohort state across AUA/NNA toggle (remove `metric` from useEffect deps)
- **2f.** Continuous view: all top-level, top 8 + Other at drill level
- **2g.** `no_city` entries grouped into Other at drill level

### Questions for DE and RD:

1. **DE:** For 2i, will you lift `timeWindow` to `AdvisorIntelligence.tsx` (same level as `granularity`)? If so, both PartnerAnalytics and DistributionTab receive it as props. What prop name?
2. **RD:** For 2c state name mapping — do you want a frontend lookup table (abbrev -> full name), or should DS add full state names to the publisher output? Frontend table is faster to ship; backend is more authoritative.
3. **RD:** For 2h NNA strip — the DE brief says 3 levels are supported (state, city, architect) but relationship-level NNA is NOT in the backend. Are you OK deferring relationship-level to post-MVP?

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.


---

## 001.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 1
timestamp: 2026-03-13T16:27:50Z
signal: continue
---

### 2i (DE-owned): plan to inherit time window + remove Distribution’s independent window toggle

I’m going to **lift `timeWindow` state to `portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx`**, alongside the existing `granularity` state, then **thread it down**:

- `AdvisorIntelligence.tsx`
  - `const [timeWindow, setTimeWindow] = useState<TimeWindow>('1Y')` (per PRD 1a-i default)
  - pass to `<PartnerAnalytics timeWindow={timeWindow} onTimeWindowChange={setTimeWindow} ... />`
  - pass to `<DistributionTab timeWindow={timeWindow} ... />`

- `PartnerAnalytics.tsx`
  - remove local `useState<TimeWindow>('3Y')`
  - use props `timeWindow` + `onTimeWindowChange` for the header Window toggle

- `DistributionTab.tsx`
  - remove local `const [window, setWindow] = useState<ChartWindowOption>('1Y')`
  - remove `WINDOW_OPTIONS` toggle UI from Distribution header (continuous-only)
  - use `props.timeWindow` to drive continuous windowing logic

**Prop name:** `timeWindow` (type `'1Y' | '3Y' | 'Max'`) to match PartnerAnalytics’ semantics.  
**Note:** Distribution currently uses `ChartWindowOption` (`'3M'|'6M'|'1Y'|'2Y'|'3Y'|'Max'`). For MVP alignment, we’ll standardize Distribution to the header’s 3 options. That means:
- update Distribution’s window type usage to accept only `'1Y'|'3Y'|'Max'` (or map internally).

This keeps “one source of truth” and satisfies 2i.

---

### DS questions (2c / 2e / 2h): what I believe is already true from the context

**2e (show all cohorts, no Other):**  
Script `09_generate_partner_analytics.py` currently has `MAX_SEGMENTS = 8` and explicitly builds an `"Other States"` / `"Other Architects"` segment in both `build_geo_view()` and `build_adv_view()` (and similarly in NNA views). So backend is **pre-aggregating** into Other today. If PRD requires “no Other” in Snapshot, we either:
- (A) change script 09 to emit all segments (preferred for correctness + consistent ordering), or
- (B) accept backend top-8+Other and only remove frontend filtering (won’t meet requirement).

So DS: please confirm you’re aligned that **2e is backend work in script 09**, not just frontend.

**2c (capitalization / state names):**  
Backend GEO segments are labeled with whatever `geo_ts['state']` contains. In the publisher lambda, state is treated as abbreviations (top states list from `geo['state']`). In script 09, `label: state` and `key = state.lower()`. So if `state` is “TX”, frontend will show “TX” unless we map. I recommend **frontend mapping abbrev→full name** for MVP speed, unless DS prefers to normalize in gold/views.

**2h (NNA cohort-specific strip):**  
Agree with the DE brief: state/city/architect are supported by existing `views.nna[period]` structure; relationship-level is not. RD should implement the 3-level traversal only.

---

### Two concrete asks to DS to unblock RD implementation sequencing

1) **Confirm 2e**: are you willing to change `09_generate_partner_analytics.py` to emit *all* state/architect segments (no Other) for Snapshot? If yes, we need to decide whether to:
   - remove `MAX_SEGMENTS` entirely for Snapshot outputs, or
   - emit both: `segments_all` + `segments_top8` (but that’s a schema change).

2) **Confirm 2c source of truth**: do we want to treat `geo_ts.state` as abbreviations permanently and map in frontend, or do you want to normalize to full names in gold/views (or in script 09 output)?

Once DS answers those, I’ll write the RD task order bundle for DistributionTab items (2b-2h) with the correct assumptions.

---

---

## 002.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 2
timestamp: 2026-03-13T16:28:12Z
signal: continue
---

### RD alignment responses (2c / 2e / 2h) + implementation notes for my side

#### 2c — Standard capitalization (states/cities/architects)
I’m aligned with DE’s recommendation: **frontend mapping for state abbreviations → full state names** is the fastest MVP path and doesn’t require touching gold/views.

Concrete plan in `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`:
- Add a small `STATE_ABBREV_TO_NAME` map (or helper `formatStateLabel(keyOrLabel)`).
- Replace all `selectedStateKey?.toUpperCase()` usages (noted in PRD at ~1928/1967/1974/1994/2133) with `formatStateLabel(selectedStateKey)`.
- Ensure donut legend + breadcrumb + strip labels use the *label* when available (from backend), but if backend label is abbreviated, we still map it.
- Cities: keep the existing title-casing logic, but also implement 2g (“no_city” → Other) so we don’t end up with “No City” as a first-class segment.
- Architects: use backend `label` as display, and only “prettify” keys when label missing (replace `_` with space + title case).

**DS ask:** please confirm whether `geo_ts.state` is always USPS abbreviations (TX/CA) and whether there are any non-US / “Unknown” values we should map to a safe fallback (“Unknown”, “Other States”).

#### 2e — Snapshot show all cohorts (no “Other”)
From the context, script 09 currently enforces `MAX_SEGMENTS = 8` and emits `"Other States"` / `"Other Architects"` (and similarly for NNA). That means **frontend cannot satisfy “show all cohorts” unless backend stops pre-aggregating**.

So I’m blocked on DS decision here:
- If DS updates `09_generate_partner_analytics.py` to emit all segments (no Other) for snapshot views, I will:
  - remove any remaining top-8 limiting in snapshot rendering (donut + legend + summary)
  - keep drill-level top-8+Other behavior only where PRD allows it (continuous drill level per 2f)
- If backend stays top-8+Other, I can only remove *frontend* filtering (which won’t meet PRD intent).

#### 2h — NNA time machine strip cohort-specific values
Yes, I’m OK with the CTO-scoped MVP: **state, city, architect only**; relationship-level cohort-specific NNA is deferred.

Implementation on my side (per DE brief):
- Update `NnaQuarterlyStrip` props to accept:
  - `parentSegmentKey: string | null` (state or architect)
  - `childSegmentKey: string | null` (city only)
- Change `getNna(period)` traversal:
  - top level: `cohortView.metrics.nna`
  - parent selected: `cohortView.donut.segments.find(key).value`
  - city selected: `cohortView.drill[parentKey].by_city[childKey].total`
- Also apply 2b here: remove “Period NNA” label; replace with just “NNA” or cohort label (e.g., “Texas NNA”) per PRD.

#### 2d — Retain cohort drill state across AUA/NNA toggle
I’ll implement exactly as PRD: remove `metric` from the drill-reset `useEffect` deps, and add a narrower effect that only clears `selectedSegmentKey` on metric change.

---

### One dependency question for DE (2i threading)
Once you lift `timeWindow` to `AdvisorIntelligence.tsx`, please confirm whether you want Distribution continuous to:
- **(A)** accept only `'1Y' | '3Y' | 'Max'` (preferred; simplest), and I’ll update Distribution’s `ChartWindowOption` usage accordingly, or
- **(B)** keep Distribution’s richer window type and map header values into it (e.g., `1Y→1Y`, `3Y→3Y`, `Max→Max`), leaving the type as-is.

I can adapt either way, but I’d prefer (A) to avoid dead code paths (3M/6M/2Y) after we remove the Distribution window toggle UI.

---

### Summary of what I need from DS to proceed cleanly
1) Confirm state abbreviation universe + any edge cases (`Unknown`, non-US).  
2) Confirm whether DS will change script 09 to remove top-8+Other for snapshot (2e). If yes, I’ll implement frontend “show all” immediately; if no, we should explicitly de-scope 2e or accept backend work as required.

---

## 003.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 3
timestamp: 2026-03-13T16:28:46Z
signal: continue
---

### DS answers (2c / 2e / 2h) — grounded in current script 09 behavior

#### 2c — State abbreviations + edge cases (what backend emits today)
From `data/black_diamond/scripts/gold/09_generate_partner_analytics.py`:

- **GEO AUA snapshot (`build_geo_view`)**
  - `label` is set to `state` directly (`'label': state`)
  - `key` is `state.lower()`
  - It filters out `state == 'Unknown'` and blank for the **AUA GEO donut** (so “Unknown” should not appear as a segment in AUA GEO snapshot).
- **GEO NNA snapshot (`build_nna_geo_view`)**
  - It keeps non-blank states and explicitly says “keep 'Unknown' as a named segment” in comments; code filters only `state.notna() & state != ''` (so **Unknown can appear** in NNA GEO).
  - `key` is `row['state'].lower()`, `label` is `row['state']`.

So for RD: assume **state labels are whatever is in `gold/views/nna_aua_by_geography.parquet.state`**. In practice that has historically been USPS abbreviations (TX/CA/…), but the code does not enforce it. Edge cases you must handle safely:
- `Unknown` (especially in NNA GEO)
- blanks (already filtered out)
- possible non-US if `country` isn’t filtered consistently in NNA path (AUA GEO filters “Unknown” but not by country in the donut; NNA GEO uses `state,country` merge but doesn’t filter country beyond what’s in the parquet)

**Recommendation for MVP:** frontend mapping `TX -> Texas` etc is correct, with a passthrough fallback for already-full names and for `Unknown`.

#### 2e — “Show all cohorts in Snapshot (no Other)” is BACKEND work (script 09)
Confirmed: script 09 hard-caps snapshot donut segments at 8 and emits “Other …” buckets:
- `MAX_SEGMENTS = 8`
- AUA GEO: `top_states = geo_day.head(MAX_SEGMENTS)` then appends `"Other States"` if remainder exists
- AUA ADV: same pattern with `"Other Architects"`
- NNA GEO / NNA ADV: same top-8 + other pattern

So **frontend-only changes cannot satisfy 2e** as written in PRD. If we want “all cohorts, no Other” in Snapshot, DS needs to change script 09.

**My proposed backend approach (minimal schema change):**
- Add a CLI/config flag in `09_generate_partner_analytics.py` like `--no-other-snapshot` (default OFF to avoid surprising perf regressions).
- When enabled:
  - For **Snapshot donut segments** in AUA GEO/ADV and NNA GEO/ADV: emit *all* segments (sorted by AUA or abs(NNA) as currently), **do not** append “Other”.
  - Keep existing “Other” behavior where PRD allows it (continuous drill level is frontend; but for snapshot we can remove Other cleanly).
- This is a backend behavior change but **not a JSON schema change** (still `segments: [...]`), which is ideal for RD.

**One caution:** emitting all states/architects could be 30–60+ segments; donut readability is a UI concern, but PRD explicitly asks for it.

If DE agrees, I can take a task order to implement this in `data/black_diamond/scripts/gold/09_generate_partner_analytics.py`.

#### 2h — NNA cohort-specific strip data availability
Agree with DE + RD: data is already present for the 3 MVP levels:
- State: `views.nna[period].geo.donut.segments[].value`
- City: `views.nna[period].geo.drill[state].by_city[city].total`
- Architect: `views.nna[period].adv.donut.segments[].value`

Relationship-level per-period NNA is not emitted (only distribution stats), so defer.

---

### Two decisions needed from DE/PM to unblock backend work

1) **Do we want DS to implement 2e in script 09 now?**  
   If yes, I’ll implement the `--no-other-snapshot` behavior (or equivalent constant) and document it in a brief + update `data_contract.xml` if needed (shouldn’t be, if schema unchanged).

2) **Do we want “Unknown” to appear in GEO NNA donut?**  
   Script 09 currently allows it in NNA GEO. If frontend mapping is added, RD should also decide whether to display it or fold into Other (but 2e removes Other). If you want it suppressed, that’s another small script 09 tweak (filter `Unknown` in NNA GEO like AUA GEO does).

---

## 004.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 4
timestamp: 2026-03-13T16:29:08Z
signal: continue
---

### Decisions (DE/PM) to unblock P2 alignment

#### Decision 1 — 2e “Show all cohorts in Snapshot (no Other)”
**YES: DS should implement 2e in script 09 now.**  
Reason: as you confirmed, `09_generate_partner_analytics.py` currently hard-caps at `MAX_SEGMENTS=8` and emits `Other*` buckets for AUA GEO/ADV and NNA GEO/ADV. RD cannot meet PRD 2e with frontend-only changes.

**Implementation preference:** do **not** introduce a CLI flag for MVP. Just change the snapshot builders to emit all segments (schema unchanged). If we later need a perf/readability cap, we can reintroduce a flag or config, but PRD explicitly wants “all cohorts”.

Concretely (script 09):
- AUA GEO: remove `top_states/other_states` split; iterate all `geo_day` rows (after existing filters) and emit segments for each state.
- AUA ADV: same for all architects.
- NNA GEO/ADV: same (rank by `abs(period_nna)` as today).
- Remove “Other States/Other Architects” append blocks.

This keeps JSON shape identical (`donut.segments[]`), just changes cardinality + removes `key='other'` segment.

#### Decision 2 — “Unknown” handling in GEO NNA donut
**Keep `Unknown` as a segment for NNA GEO (no backend suppression) for MVP.**  
Reason: NNA GEO currently allows it; suppressing it would hide real flows that have missing state attribution. With 2e removing “Other”, we still need a place for unattributed flows to land. RD can display it as “Unknown” (no state-name mapping applied) and optionally style it muted.

(If Andrew/CTO later wants it hidden, we can add a follow-up change to filter it out, but that would be a product decision because it discards information.)

---

### RD guidance (so you can proceed while DS patches 09)

- **2c mapping:** proceed with frontend `STATE_ABBREV_TO_NAME` mapping with passthrough fallback; treat `Unknown` as passthrough.
- **2h strip:** proceed with the 3-level traversal only (state/city/architect). Relationship-level remains deferred.

---

### Next actions / ownership

1) **[DS]** Please implement 2e changes in `data/black_diamond/scripts/gold/09_generate_partner_analytics.py` (remove top-8 + Other aggregation for snapshot donuts in AUA GEO/ADV and NNA GEO/ADV). No schema change expected; just cardinality.  
2) **[RD]** Continue implementing 2b/2c/2d/2f/2g/2h assuming snapshot donuts will soon contain full segment lists and no `other` segment.  
3) **[DE]** I will proceed with 2i state lift (`timeWindow` to `AdvisorIntelligence.tsx`) as described in my prior turn; RD can assume Distribution continuous will accept only `'1Y'|'3Y'|'Max'` (we’ll standardize types accordingly).

---

## 005.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 5
timestamp: 2026-03-13T16:29:31Z
signal: continue
---

### Acknowledged decisions + what I’ll implement next (RD scope)

#### 2e backend change (DS) — how I’ll treat it on the frontend
Aligned with DE decision: once script 09 removes top-8 + “Other” in snapshot donuts, I will assume:
- Snapshot donut `segments[]` can be **high-cardinality** (all states / all architects)
- There may be **no `key: 'other'`** segment anymore
- `Unknown` may appear (at least in NNA GEO), and I’ll render it as a normal segment but visually muted if needed

Frontend implications in `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`:
- Remove any snapshot-side assumptions that `Other` exists or that we should slice to 8.
- Ensure legend list is scrollable (it already is) and remains usable with 30–60 entries.

#### 2c capitalization — proceed with frontend mapping + safe fallbacks
I’ll implement a `formatStateLabel(stateLabelOrKey: string)` helper:
- If it matches a USPS abbrev (case-insensitive), map to full name.
- If it’s already a full name (e.g., “Texas”), passthrough.
- If it’s `Unknown`, passthrough.
Then replace all `selectedStateKey?.toUpperCase()` usages in snapshot breadcrumb/help text with `formatStateLabel(selectedStateKey)`.

Architects: display `seg.label` (backend-provided) and only prettify keys if label missing.

#### 2h NNA strip cohort-specific values — implement per DE brief (3 levels)
I’ll update `NnaQuarterlyStrip` to accept:
- `parentSegmentKey` (state or architect)
- `childSegmentKey` (city only)
and traverse:
- top level: `metrics.nna`
- parent: `donut.segments[].value`
- city: `drill[parent].by_city[child].total`

Also applying 2b here: strip subtitle becomes just **“NNA”** (or cohort label if we decide to show it).

#### 2f/2g continuous drill behavior
Given DE’s note that Distribution continuous will standardize to header window options, I’ll keep my changes focused on:
- **Top level:** show all cohorts (no “Other” bucketing)
- **Drill level:** allow top-8 + “Other” (and fold `no_city` into “Other”)

(If DS’s 2e change only affects snapshot, continuous still needs these frontend adjustments per PRD.)

---

### One confirmation request (so I don’t fight DE’s 2i refactor)
When DE lands 2i, I will update DistributionTab’s window typing to **only** `'1Y' | '3Y' | 'Max'` and remove `3M/6M/2Y` paths. If DE wants a mapping layer instead, please flag now; otherwise I’ll proceed with the simplified type.

---

### Ready-for-task-order checklist (what I’m unblocked on)
- I can start implementing **2b/2c/2d/2f/2g/2h** immediately in `DistributionTab.tsx`.
- I will treat **2e** as “backend pending” but make the UI resilient to both cases (with/without `Other`) to avoid a brittle merge window.

---

## 006.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 6
timestamp: 2026-03-13T16:29:51Z
signal: converge
---

### Final DS confirmation + backend plan (2c / 2e / 2h)

#### 2c (capitalization / state naming) — backend reality
Backend state `label` is whatever is in `gold/views/nna_aua_by_geography.parquet.state` (script 09 uses it verbatim). Historically this is USPS abbreviations, but **not enforced**. Edge cases to handle safely in frontend:
- `Unknown` (notably allowed in **NNA GEO** path)
- blanks are already filtered out
So RD’s frontend `STATE_ABBREV_TO_NAME` mapping with passthrough fallback is the correct MVP approach.

#### 2h (NNA time machine strip cohort-specific values) — data is already there for MVP levels
Confirmed available in every period emitted by script 09:
- State: `views.nna[period].geo.donut.segments[].value` (signed)
- City: `views.nna[period].geo.drill[state].by_city[city].total` (DistributionStats.total)
- Architect: `views.nna[period].adv.donut.segments[].value` (signed)
Relationship-level per-period NNA is **not** emitted (only aggregate DistributionStats), so deferring that level is consistent with the CTO scope.

#### 2e (show all cohorts in Snapshot; no “Other”) — DS will implement in script 09 (backend-required)
Aligned with DE decision: this must be done in `data/black_diamond/scripts/gold/09_generate_partner_analytics.py` by removing the `MAX_SEGMENTS=8` top-N split and the “Other States/Other Architects” append blocks for **snapshot donuts**:
- AUA GEO (`build_geo_view`)
- AUA ADV (`build_adv_view`)
- NNA GEO (`build_nna_geo_view`)
- NNA ADV (`build_nna_adv_view`)

This is a **behavior/cardinality change only**; JSON schema stays `donut.segments: [...]` (just more segments, and no `key='other'` segment). Per DE decision, we will **keep `Unknown`** as a segment in NNA GEO.

**Implementation note (perf):** this increases segment count (likely 30–60 states/architects). Script 09 already loads all needed data; the incremental cost is mostly Python loop + JSON size. No schema change expected.

### Handoff expectation
Once I implement 2e in script 09, I’ll produce:
- a DS session log with exact file changes + verification notes (segment counts, presence/absence of `other`)
- a DevOps brief for uploading the updated gold script to `s3://opal-data-bd/code/gold/09_generate_partner_analytics.py` and running gold in the appropriate mode (likely incremental unless upstream dims changed)

Thread-wise, alignment is complete: DE owns 2i state lift; RD can proceed on 2b/2c/2d/2f/2g/2h assuming snapshot donuts will soon be “all cohorts, no Other,” and should remain resilient during the deploy window.

---

## 007.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 7
timestamp: 2026-03-13T16:30:10Z
signal: converge
---

## Convergence — P2 Distribution Tab alignment (2a–2i)

We’re aligned across DS/DE/RD on ownership, data shapes, and the two key backend-vs-frontend boundaries.

### Final decisions / agreements

**2e “Show all cohorts in Snapshot (no Other)” = BACKEND REQUIRED (script 09)**
- Confirmed by DS + DE: `data/black_diamond/scripts/gold/09_generate_partner_analytics.py` currently enforces `MAX_SEGMENTS = 8` and emits `Other States` / `Other Architects` (AUA GEO/ADV and NNA GEO/ADV).
- **Decision:** DS will remove top-8 + Other aggregation in script 09 for snapshot donuts (schema unchanged; cardinality increases; `key='other'` disappears).

**Unknown handling**
- **Decision:** keep `Unknown` as a segment in **NNA GEO** (do not suppress in backend). Frontend should display it as-is (optionally muted).

**2c capitalization / state names = FRONTEND mapping**
- Backend labels are whatever is in `gold/views/nna_aua_by_geography.parquet.state` (often USPS abbreviations, not enforced).
- **Decision:** RD implements `STATE_ABBREV_TO_NAME` mapping with passthrough fallback; remove `.toUpperCase()` usages in `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`.

**2h NNA time machine strip cohort-specific values = FRONTEND-only (3 levels)**
- Supported levels: **state, city, architect** using:
  - state/architect: `views.nna[period].{geo|adv}.donut.segments[].value`
  - city: `views.nna[period].geo.drill[state].by_city[city].total`
- Relationship-level per-period NNA is a backend gap and **deferred post-MVP**.

**2i inherit time window from header = DE-owned state lift**
- **Decision:** lift `timeWindow` to `portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx`, pass to:
  - `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`
  - `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`
- Distribution Continuous will standardize to header window options: **`'1Y' | '3Y' | 'Max'`** and remove its independent window toggle.

### Concrete next actions (by agent)

**[0.4.0_DS_ClientPlatform]**
- Implement 2e in `data/black_diamond/scripts/gold/09_generate_partner_analytics.py`:
  - remove `MAX_SEGMENTS` top-N split + “Other” append blocks in:
    - `build_geo_view()`, `build_adv_view()`, `build_nna_geo_view()`, `build_nna_adv_view()`
  - keep `Unknown` in NNA GEO
- Provide DS session log + DevOps upload brief for `s3://opal-data-bd/code/gold/09_generate_partner_analytics.py`.

**[0.4.2_RD_AdvisorIntelligence]**
- Proceed implementing 2b/2c/2d/2f/2g/2h in `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`, assuming snapshot donuts will become “all cohorts, no Other” (and keep UI resilient during deploy window).

**[0.4.0_DE_ClientPlatform]**
- Execute 2i state lift in `AdvisorIntelligence.tsx` + prop threading into PartnerAnalytics + DistributionTab; remove Distribution’s independent window state/UI and align types to `'1Y'|'3Y'|'Max'`.

This resolves the alignment questions; remaining work is execution per above.

---
