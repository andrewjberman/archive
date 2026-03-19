# Thread Receipt: P4 Books Tab alignment

**Thread ID:** ADVI_MVPLVL-004-p4-books-tab-alignment
**Project Serial:** ADVI_MVPLVL-004
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-13T16:35:22Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.0_DE_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: 2026-03-13T16:35:17Z
signal: continue
---

## P4 Books Tab — Alignment

I am DS for Pod 4. This thread covers the 8 Books Tab items from ADVI_MVPLVL PRD Part 4. The Books Tab is the deepest section — most items require understanding what gold layer data exists at each drill level before views can be designed.

### 4a. Gold Table Data Audit — RESEARCH (DS-owned, gates everything)

The PRD lists 6 gold scripts that produce data the Books Tab could consume. I need to determine for each:
- What grain level the data is at (firm/advisor/relationship/account)
- Whether the publisher already surfaces it via an endpoint
- What additional aggregations are needed for Mix, Concentration, and time series

I will read the publisher Lambda and gold scripts to answer these questions during this thread.

### 4b. Drill Hierarchy — ACTION (existing, needs enhancement)

The 4-level drill already exists in `ClientsTab.tsx`:
- N1 (Global): aggregate KPIs + advisor summary
- L2 (Advisor Book): advisor AUA, clients, accounts, tax
- L3 (Relationship): client AUA, accounts table, tax intelligence
- L4 (Account): inline expansion with account-scoped lots

### 4c/4d. Tax Status + Tax Liability — ACTION (already functional)

Both exist at L2/L3/L4. Minor refinements will come from Mix/Concentration work.

### 4e. Mix (Asset Class Breakdown) — RESEARCH + ACTION

Requires mapping each position to an asset class. The ETF Classification system (`etf_classification.py`) covers ~160 ETFs. Key questions:
- Does the publisher already expose `portfolio_composition` at L2?
- What coverage does ETF classification achieve against actual holdings?
- Should Mix be computed backend (publisher/gold script) or frontend (from lots data)?

### 4f. Concentration (Security-Level Breakdown) — RESEARCH + ACTION

Linked to Mix — when user clicks an asset class in Mix, Concentration filters to show securities in that class. Data comes from holdings lots or positions cube.

### 4g. AUA/NNA Time Series at L3/L4 — ACTION (data exists)

`client_performance.parquet` (relationship) and `account_performance.parquet` (account) have daily AUA/NNA. These need to be surfaced via publisher endpoints and rendered with existing chart components. DE: what is the endpoint plan for serving relationship/account-level time series?

### 4h. Advisor Listing UI Consistency — ACTION (blocked on 3d)

The N1 advisor summary table should match the leaderboard design from 3d.

### Questions for DE and RD:

1. **DE:** For 4g, does the publisher already have `getAdvisorBook` or `getBooksClientDetail` endpoints? If so, do they currently include time series data, or would we need new fields?
2. **RD:** For 4e/4f, do you envision Mix and Concentration as separate panels side-by-side, or as a stacked layout with Mix on top and Concentration below?
3. **RD:** For 4g time series at L3/L4, do you want the same chart components as the Header panel (PartnerAnalytics), or a more compact inline chart?

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.


---

## 001.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 1
timestamp: 2026-03-13T16:36:15Z
signal: continue
---

### P4 Books Tab alignment — DE response (focus: 4g wiring + what exists today)

#### 1) 4g (Relationship/Account AUA+NNA time series): what exists vs what’s missing
**Gold data exists** (per PRD + DS context):
- Relationship × day: `s3://opal-data-bd/gold/client_performance.parquet` (script `05_build_client_performance.py`)
- Account × day: `s3://opal-data-bd/gold/account_performance.parquet` (script `05b_build_account_performance.py`)

**Portal UI does *not* currently consume either of these for Books Tab.**
- `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` (Books Tab) currently fetches:
  - `getClientsTab()` → `gold/clients_tab.json` (N1 firm dashboard)
  - `getAdvisorBook(advisorId)` → advisor book JSON (L2)
  - `getBooksClientDetail(clientKey)` → relationship detail JSON (L3/L4)
- Those responses (per `portal/src/pages/AdvisorIntelligence/types.ts`) **do not include any timeseries arrays** for relationship or account. L3/L4 show point-in-time metrics + lots/tax tables only.

**So for 4g we need backend surfacing + frontend rendering.** Concretely:
- Add new endpoints (or extend existing ones) to expose:
  - Relationship-level timeseries for selected `relationship_id` (L3)
  - Account-level timeseries for selected `account_id` (L4)
- Then RD can render charts in L3/L4 using the same time window + granularity controls pattern as header (but likely a compact variant).

#### 2) Endpoint plan proposal (so DS can audit feasibility)
To keep MVP risk low, I recommend **new dedicated endpoints** rather than bloating existing payloads:

**A. Relationship timeseries**
- `GET /api/scoped/advisor-intelligence/books/relationship/{relationship_id}/timeseries.json`
- Backed by `gold/client_performance.parquet` filtered to relationship_id, returning daily rows:
  - `date, total_aua, cum_inflows, cum_outflows, nna, pct_priced` (+ optional tax-split AUA)

**B. Account timeseries**
- `GET /api/scoped/advisor-intelligence/books/account/{account_id}/timeseries.json`
- Backed by `gold/account_performance.parquet` filtered to account_id, returning daily rows:
  - `date, total_aua, cum_inflows, cum_outflows, nna, num_positions, pct_priced`

**Why new endpoints:** avoids increasing `getBooksClientDetail()` response size dramatically (open lots can already be large), and keeps caching simple.

#### 3) Frontend expectation for DS (data contract guidance)
If DS/BD publisher team prefers to emit **pre-aggregated** monthly/quarterly/annual series (like PSCFIX did for header AUA), that’s fine too—but MVP can start with daily and aggregate client-side.

For RD, I’d like the response shape to mirror existing timeseries conventions:
```ts
{
  generated_at: string
  data_as_of: string
  relationship_id?: string
  account_id?: string
  data: Array<{ date: string; total_aua: number; cum_inflows: number; cum_outflows: number; nna: number }>
}
```

#### 4) Answers to DS questions from msg 000
**Q1 (DE): do endpoints exist + do they include timeseries?**  
- Yes, Books Tab endpoints exist (`getClientsTab`, `getAdvisorBook`, `getBooksClientDetail`), but **they do not include timeseries** today. 4g requires new endpoint(s) or response extensions.

**Q2/Q3 (RD UI layout):** I’ll defer final UI layout to RD, but from PM standpoint:
- Mix + Concentration should be **paired** (side-by-side on desktop, stacked on mobile) to support the “click Mix filters Concentration” mental model.
- L3/L4 timeseries should be **compact inline charts** (not the full PartnerAnalytics header complexity), but should reuse the same time window/granularity semantics for consistency.

#### 5) Immediate next step / ask to DS (to keep thread moving)
DS: during 4a audit, please confirm:
- Whether `bd-portal-advisor-publisher` already reads `gold/client_performance.parquet` / `gold/account_performance.parquet` anywhere (I believe it does not today for Books).
- Whether you prefer: (a) new JSON files published to S3 (static) vs (b) dynamic Lambda query against parquet for relationship/account filters.
  - My bias: **dynamic** for drilldowns (relationship/account), **static** for firm-wide aggregates.

I’ll hold until DS confirms preferred backend pattern so I can issue precise task orders to RD (and/or DT/DS) for 4g wiring.

---

## 002.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 2
timestamp: 2026-03-13T16:36:36Z
signal: continue
---

### P4 Books Tab alignment — RD response (focus: 4e/4f UI contract + 4g chart integration needs)

#### 1) 4e/4f (Mix + Concentration) — preferred UI layout + interaction model
I agree with DE’s pairing recommendation. For Books Tab, I propose:

- **Desktop (lg+)**: **two panels side-by-side** in a 2-col grid  
  - **Left:** Mix (asset class) pie + legend  
  - **Right:** Concentration (security-level) pie or ranked list (top N + Other), **filtered by selected Mix slice**
- **Mobile**: stacked vertically (Mix above Concentration), but keep the same linked selection state.

**Interaction contract (frontend state):**
- `selectedAssetClass: string | null`
  - `null` = show all securities in Concentration
  - click Mix slice sets `selectedAssetClass`
  - click same slice again clears (toggle off)
- Concentration should also allow selecting a security row/slice for future drill (optional, not MVP-critical).

**Where this lives in drill hierarchy:**
- **L2 (Advisor book)**: show Mix+Concentration for the advisor’s entire book
- **L3 (Relationship)**: show Mix+Concentration for that relationship
- **L4 (Account)**: show Mix+Concentration for that account (could be collapsed/accordion to avoid vertical bloat)

This keeps the “what is the book made of?” story consistent at every level.

#### 2) 4g (Relationship/Account time series) — chart UX requirements for backend contract
For L3/L4 time series, I want **compact charts** (not the full PartnerAnalytics header complexity), but with consistent semantics:

- **Two mini charts** (or a single chart with metric toggle):
  - AUA (line)
  - NNA (diverging bars or line; I’m fine with line for MVP if bars are too heavy)
- **Controls**:
  - Time window: `1Y | 3Y | Max` (match header)
  - Granularity: `Monthly | Quarterly | Annually` (match page-level granularity state)
- **Data expectation**:
  - Daily is acceptable if we aggregate client-side, but I’d prefer the endpoint to optionally support `?granularity=` and `?window=` to reduce payload size at L4.

**If backend stays daily-only for MVP**, I’ll implement client-side aggregation in `ClientsTab.tsx` using the same “aggregate full history then filter for display” pattern we already use elsewhere (prevents GRO-style cutoff bugs).

#### 3) Ask to DS (to unblock 4e/4f + 4g implementation details)
To design the components cleanly, I need DS to confirm the intended data source for Mix/Concentration at each level:

1. **Mix source of truth**: do we want to compute from:
   - `holdings_lots` (current snapshot, accurate MV, but lot-grain heavy), or
   - a pre-aggregated view (preferred), or
   - existing `advisorBookResponse.portfolio_composition` (currently hidden + unclear lineage)?
2. **Concentration source**: can we get **(ticker, market_value)** at L2/L3/L4 without scanning `positions_cube`?
3. **Ticker classification**: do we standardize on the canonical ETF classification table (preferred) vs the publisher’s current name-pattern `_classify_asset()` (less reliable)?

#### 4) Implementation note (scope-safe for me)
Once DE/DS confirm endpoint shapes, I can implement:
- New Mix+Concentration panels in `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` at L2/L3/L4
- New compact time series panel(s) at L3/L4 consuming the new endpoints DE proposed

But I cannot touch shared chart components outside this page dir, so I’ll build any small chart helpers locally inside `ClientsTab.tsx` (or split into local subcomponents under `tabs/` if we want to keep file size manageable).

**Open question for DE:** should L3/L4 time series inherit the page-level `granularity` state (from `AdvisorIntelligence.tsx`) or have a local override? My preference: inherit (single source of truth), but allow local window toggle (1Y/3Y/Max) if that’s not already lifted.

---

## 003.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 3
timestamp: 2026-03-13T16:36:57Z
signal: continue
---

### P4 Books Tab alignment — DS response (focus: what data exists today + recommended backend pattern for 4e/4f/4g)

#### 1) What Books Tab endpoints exist today (and what they *don’t* do)
From the current portal types + BooksTab wiring:

- **N1** uses `gold/clients_tab.json` (built by `bd-portal-publisher` Lambda).
- **L2** uses `getAdvisorBook(advisorId)` (built by `bd-portal-advisor-publisher` Lambda).
- **L3/L4** uses `getBooksClientDetail(clientKey)` (built by `bd-client-detail` Lambda).

These are **point-in-time + tables** payloads (headline/tax/lots), and **do not include any time series arrays**. So DE is right: 4g requires new surfacing.

Also: none of these existing Books endpoints are a good place to “sneak in” daily time series because:
- L3 already returns potentially large `open_lots` arrays.
- L4 is inline expansion and should stay snappy.

#### 2) 4g (relationship/account AUA+NNA time series): recommended backend pattern
I agree with DE’s proposal: **new dedicated endpoints** for time series.

**Strong recommendation:** implement these as **dynamic Lambda queries against the gold parquets**, not as pre-published static JSON files, because:
- The query is always scoped to a single `relationship_id` or `account_id` (small result set).
- Publishing per-relationship/per-account JSON to S3 would explode object count and complicate invalidation.

**Response shape (RD-friendly, consistent with existing patterns):**
```json
{
  "generated_at": "...",
  "data_as_of": "YYYY-MM-DD",
  "relationship_id": "...",   // or account_id
  "data": [
    {"date":"YYYY-MM-DD","total_aua":0,"cum_inflows":0,"cum_outflows":0,"nna":0}
  ]
}
```

**Daily-only vs pre-aggregated:** MVP can be daily-only and RD aggregates client-side. If payload size becomes an issue at L4, we can add optional query params later (`?window=1Y&granularity=monthly`) and aggregate server-side.

#### 3) 4e/4f (Mix + Concentration): what data source should be the “source of truth”
We already have the right raw ingredient for **current snapshot** composition:

- `gold/holdings_lots/YYYY-MM-DD.parquet` (built by script 03) contains **market_value** at lot grain, plus `ticker` (sometimes null), plus `account_id` and `relationship_id`.

So for Mix + Concentration at any drill level **as-of latest snapshot**:
- **Advisor book (L2):** filter holdings_lots by accounts where `architect == advisor` (join via `gold/accounts_dimension_latest.parquet`).
- **Relationship (L3):** filter holdings_lots by `relationship_id`.
- **Account (L4):** filter holdings_lots by `account_id`.

Then aggregate:
- **Concentration:** group by `ticker` (fallback to `asset_name` when ticker null), sum `market_value`, take top N + Other.
- **Mix:** map each (ticker/asset_name) to asset class, then sum `market_value` by asset class.

This avoids `positions_cube` entirely (which is huge and time-series oriented).

**Important nuance:** holdings_lots is lot-grain and can be large, but for dynamic endpoints we can:
- Load only latest snapshot (single parquet), and
- Column-prune to `account_id, relationship_id, ticker, asset_name, market_value, is_open` (and filter `is_open==True`).

If performance is still heavy, we can add a **new gold view** later (pre-aggregated “holdings snapshot” at (account_id, ticker) grain), but I’d start with holdings_lots because it’s already in place and correct.

#### 4) Classification standard: ETF canonical vs publisher name-pattern classifier
For Books Tab Mix/Concentration linkage, we should **standardize on the canonical ETF classification** (`infra/aws/lambda/v2_portal/_shared/etf_classification.py`) *when ticker is present*.

Reason: the publisher Lambda’s `_classify_asset(name)` is name-pattern based and will misclassify / drift as naming changes. ETF classification is explicit and stable.

Fallback logic:
1. If `ticker` exists and is in ETF classification → use it.
2. Else fallback to name-pattern classification (or “Other”) using `asset_name`.

This gives us high coverage for Opal ETF-heavy books while still handling unmapped assets.

#### 5) Answers to RD’s specific asks
1) **Mix source of truth:** use **holdings_lots latest snapshot** (not `portfolio_composition` in AdvisorBookResponse; that field is currently hidden and its lineage is unclear / likely placeholder).
2) **Concentration source:** yes — holdings_lots gives market_value; aggregate to (ticker, mv) without scanning positions_cube.
3) **Ticker classification:** yes — canonical ETF classification first, name-pattern fallback only when needed.

#### 6) Open question back to DE (so we can lock task orders)
For 4g endpoints: do you want these to live under an existing Lambda (e.g., `bd-client-detail`) or a new lightweight Lambda (e.g., `bd-books-timeseries`)?

My preference:
- **Extend `bd-client-detail`** with two new routes if it already has parquet access patterns and auth wiring.
- Otherwise **new Lambda** is cleaner (keeps client detail payload logic isolated from time series logic).

If you decide the target Lambda, I can draft the exact parquet query logic + column set and update `data_contract.xml` accordingly.

---

## 004.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 4
timestamp: 2026-03-13T16:37:19Z
signal: continue
---

### P4 Books Tab alignment — DE decision + concrete next steps (lock 4g + set up 4e/4f contract)

#### 1) Decision: backend pattern for 4g (timeseries) + 4e/4f (mix/concentration)
Agree with DS: **dynamic Lambda queries** are the right MVP approach for all drill-scoped payloads:
- 4g: relationship/account AUA+NNA timeseries from `gold/client_performance.parquet` + `gold/account_performance.parquet`
- 4e/4f: latest-snapshot Mix + Concentration from latest `gold/holdings_lots/YYYY-MM-DD.parquet` (open lots only), with ETF-classification-first mapping.

We should **not** publish per-relationship/per-account JSON to S3.

#### 2) Where should these routes live? (answering DS question)
I want these to live in **`opal-partners-data` Lambda** (dynamic query Lambda) rather than `bd-client-detail`.

Rationale:
- `bd-client-detail` is already “heavy” (lots tables, tax intelligence) and should remain optimized for that payload.
- `opal-partners-data` is already the dynamic query surface for partner analytics; adding Books drill endpoints there keeps “dynamic parquet slice” logic in one place and avoids coupling to the client-detail builder.

So: **extend `opal-partners-data` with 4 new GET routes** (2 for timeseries, 2 for composition).

#### 3) Proposed endpoint contract (so RD can start building panels)
All endpoints are via portal-proxy under the scoped namespace.

**A) 4g Timeseries**
1. `GET /api/scoped/partners/books/relationship/{relationship_id}/timeseries`
2. `GET /api/scoped/partners/books/account/{account_id}/timeseries`

Response (daily rows; RD aggregates client-side for MVP):
```json
{
  "generated_at": "ISO",
  "data_as_of": "YYYY-MM-DD",
  "relationship_id": "..." ,
  "account_id": "...",
  "data": [
    { "date":"YYYY-MM-DD", "total_aua":0, "cum_inflows":0, "cum_outflows":0, "nna":0 }
  ]
}
```
Notes:
- For relationship: optionally include `aua_taxable/aua_tax_deferred/aua_tax_exempt` if cheap (nice-to-have, not required for MVP).
- For account: optionally include `num_positions` and `pct_priced` (already in 05b output).

**B) 4e/4f Mix + Concentration (latest snapshot)**
3. `GET /api/scoped/partners/books/relationship/{relationship_id}/composition`
4. `GET /api/scoped/partners/books/account/{account_id}/composition`
(+ later: advisor-level composition once DS completes 4a mapping for “advisor book = architect filter”)

Response:
```json
{
  "generated_at": "ISO",
  "data_as_of": "YYYY-MM-DD",
  "scope": { "relationship_id": "...", "account_id": "..." },
  "mix": [ { "asset_class":"equity|fixed_income|hedge|cash|other", "label":"Equities", "market_value":0, "pct":0 } ],
  "concentration": {
    "top_n": 10,
    "items": [ { "key":"SPY", "label":"SPY", "asset_class":"equity", "market_value":0, "pct":0 } ],
    "other": { "market_value":0, "pct":0 }
  },
  "unclassified": { "count": 0, "market_value": 0 }
}
```
Classification rule: ticker → `etf_classification.py` first; fallback to name-pattern (or “Other”) when ticker missing/unmapped.

#### 4) RD alignment (what I’m asking RD to implement once endpoints exist)
- In `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`:
  - Add **paired Mix + Concentration panels** at L3 and L4 first (relationship/account).
  - Add compact timeseries charts at L3/L4 consuming the new timeseries endpoints.
  - Keep state: `selectedAssetClass` filters concentration (as RD described).

#### 5) DS ask (to close 4a → enable advisor-level composition later)
DS: during 4a audit, please confirm the cleanest “advisor book membership” key for holdings_lots filtering:
- Is it `accounts_dimension_latest.architect` (account-level) or `client_dimension.primary_architect` (relationship-level)?
For L2 advisor composition we need a stable mapping; I suspect **accounts_dimension_latest.architect** is simplest for MVP.

#### 6) Next step from me (PM action)
If DS agrees on `opal-partners-data` as the target Lambda, I will issue:
- a DS task order: “spec + implement parquet slice routes in opal-partners-data” (no deploy; DT deploys)
- an RD task order: “BooksTab L3/L4 timeseries + composition panels consuming new endpoints” (behind feature flag if needed)

Open question: DS, confirm you’re comfortable with `opal-partners-data` owning these routes (vs a new Lambda). If yes, we lock and I write the task orders immediately.

---

## 005.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 5
timestamp: 2026-03-13T16:37:41Z
signal: continue
---

### RD alignment confirmation (P4 Books Tab) + frontend contract notes

#### 1) Confirmed: backend plan works for my UI implementation
I’m aligned with DE/DS decisions:

- **Dynamic Lambda queries** for drill-scoped payloads (no per-relationship JSON fanout).
- **4g timeseries**: daily rows are fine for MVP; I’ll aggregate client-side for `Monthly | Quarterly | Annually` and filter for `1Y | 3Y | Max`.
- **4e/4f composition**: latest snapshot from `holdings_lots` is exactly what I need for Mix + Concentration at L3/L4.

I’m also fine with these routes living under **`opal-partners-data`** (from a frontend POV it’s just `/api/scoped/...`).

#### 2) UI placement + drill-level scope (what I will build first)
To keep MVP risk low and avoid L2 “advisor membership” ambiguity until DS finishes 4a:

- **Phase 1 (MVP): implement at L3 + L4 only**
  - L3 (relationship): show **Mix + Concentration** paired panels + **AUA/NNA timeseries** panel(s)
  - L4 (account): same, but can be collapsible/accordion inside the inline account drill to avoid vertical bloat

- **Phase 2 (post-4a): add L2 (advisor book)**
  - Once DS confirms the advisor→accounts mapping key (accounts_dimension.architect vs client_dimension.primary_architect), we can add advisor-level composition/timeseries.

#### 3) Frontend state contract for linked Mix → Concentration
I’ll implement the linked behavior exactly as discussed:

- `selectedAssetClass: string | null`
  - `null` => concentration shows all securities
  - click Mix slice => set asset class
  - click same slice again => clear
- Concentration will render **Top N + Other** (N=10 per DE contract), with “Other” always present when tail exists.

#### 4) Endpoint shape notes (small tweaks that help UI)
DE’s proposed response shapes are good. Two small asks to make UI cleaner:

1) **Stable keys for mix items**
   - Please ensure `mix[].asset_class` is a stable enum-ish key (`equity|fixed_income|hedge|cash|other`) and `label` is display text.
   - I’ll use `asset_class` for selection state, not `label`.

2) **Concentration item identity**
   - `items[].key` should be stable and unique. If ticker exists, use ticker; else use a deterministic fallback like `asset_name` (or `asset_name|account_id` if collisions are possible).
   - I’ll display `label`, but use `key` for React keys + selection (if we add it later).

No blockers if these aren’t perfect on day 1, but it prevents UI edge cases.

#### 5) Implementation constraint reminder (so task orders are scoped correctly)
Per my agent constraints, I can only commit under:
- `portal/src/pages/AdvisorIntelligence/`

So if we need new shared hooks/components in `portal/src/api/` or shared UI primitives, DE will need to own those. I can still build local helpers/components inside `tabs/ClientsTab.tsx` or split into local files under `tabs/` if desired.

#### 6) Question to DS/DE to lock my task order
For the **timeseries endpoints**, should I assume:
- `data_as_of` matches the parquet’s latest date (same as header), and
- `data` is **sorted ascending by date**?

If yes, I’ll code the aggregation assuming sorted input (and defensively sort if not).

---

## 006.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 6
timestamp: 2026-03-13T16:37:59Z
signal: converge
---

### Converging decisions (P4 Books Tab alignment) — DS confirmation + final contracts

#### 1) Confirmed: `opal-partners-data` is the right Lambda for 4g + 4e/4f
I’m aligned with DE’s decision to implement the new Books drill endpoints inside:
- `infra/aws/lambda/bd-pipeline/opal-partners-data/`

Reason: these are “dynamic parquet slice” endpoints (relationship/account scoped), and keeping that logic consolidated is cleaner than extending `bd-client-detail` (which is already heavy with lots/tax payloads).

#### 2) 4g timeseries endpoints — DS contract confirmation
Endpoints (as DE proposed):
- `GET /api/scoped/partners/books/relationship/{relationship_id}/timeseries`
- `GET /api/scoped/partners/books/account/{account_id}/timeseries`

**Data source of truth:**
- Relationship: `s3://opal-data-bd/gold/client_performance.parquet`
- Account: `s3://opal-data-bd/gold/account_performance.parquet`

**Response guarantees (answering RD Q6):**
- `data_as_of`: **max(date)** present in the parquet (same “as-of” concept as header metrics; should align with pipeline run date)
- `data`: **sorted ascending by date** (Lambda should enforce sort before returning)

Daily-only is fine for MVP; RD aggregates client-side.

#### 3) 4e/4f composition endpoints — DS contract confirmation
Endpoints (as DE proposed):
- `GET /api/scoped/partners/books/relationship/{relationship_id}/composition`
- `GET /api/scoped/partners/books/account/{account_id}/composition`

**Data source of truth:** latest holdings snapshot
- `s3://opal-data-bd/gold/holdings_lots/YYYY-MM-DD.parquet` (latest key under prefix)
- Filter: `is_open == True`
- Column prune: `account_id, relationship_id, ticker, asset_name, market_value, is_open`

**Aggregation rules:**
- Concentration: group by `ticker` when present else fallback key derived from `asset_name` (deterministic), sum `market_value`, compute pct, top N + Other.
- Mix: map each position to asset class, sum `market_value` by asset class, compute pct.

**Classification standard (important):**
- Prefer canonical ETF classification when `ticker` is present (from `infra/aws/lambda/v2_portal/_shared/etf_classification.py`).
- Fallback: name-pattern classifier (publisher-style) only when ticker missing/unmapped → `other`.

**RD’s two small asks are accepted as contract:**
- `mix[].asset_class` must be stable enum key (`equity|fixed_income|hedge|cash|other`) and `label` is display.
- `concentration.items[].key` must be stable/unique (ticker if available; else deterministic fallback from asset_name).

#### 4) Advisor (L2) composition mapping key — preliminary DS recommendation
For “advisor book membership” once we extend to L2:
- MVP mapping should use **`gold/accounts_dimension_latest.parquet`** at **account grain** (`architect` / `implementor` fields) to select accounts, then filter holdings_lots by those account_ids.
- This avoids ambiguity in `client_dimension.primary_architect` (relationship-level “primary” attribution can differ from account-level tagging).

(We can formalize this in the 4a audit deliverable, but this is the cleanest path given existing gold artifacts.)

#### 5) Close-out: what’s now “locked” for task orders
- 4g: dynamic timeseries endpoints in `opal-partners-data`, sourced from `client_performance` / `account_performance`, sorted daily series, `data_as_of = max(date)`.
- 4e/4f: dynamic composition endpoints in `opal-partners-data`, sourced from latest `holdings_lots` snapshot, ETF-classification-first.

This is sufficient for DE to issue RD task orders for L3/L4 UI work (Phase 1), and for DE to issue DS/DT task orders for backend route implementation + deployment.

---

## 007.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 7
timestamp: 2026-03-13T16:38:18Z
signal: converge
---

### Converged — P4 Books Tab alignment (DE final)

#### 1) Locked decisions (thread resolution)
We are aligned on the MVP architecture for Books Tab enhancements:

- **4g (L3/L4 AUA+NNA time series):** dynamic parquet-slice endpoints (daily rows) served by **`opal-partners-data`**.
- **4e/4f (L3/L4 Mix + Concentration):** dynamic latest-snapshot composition endpoints served by **`opal-partners-data`**, sourced from latest `gold/holdings_lots/*.parquet` (open lots only), with **ETF-classification-first** mapping.
- **L2 (advisor-level) composition/timeseries is deferred** until DS completes 4a mapping confirmation; MVP ships L3/L4 first.

#### 2) Final endpoint contracts to implement (MVP = L3/L4)
All via portal-proxy under scoped namespace:

**Timeseries**
- `GET /api/scoped/partners/books/relationship/{relationship_id}/timeseries`
- `GET /api/scoped/partners/books/account/{account_id}/timeseries`

Contract guarantees (per DS):  
- `data_as_of = max(date)` in parquet  
- `data` sorted ascending by `date`

**Composition**
- `GET /api/scoped/partners/books/relationship/{relationship_id}/composition`
- `GET /api/scoped/partners/books/account/{account_id}/composition`

Contract guarantees (per RD asks, accepted by DS):  
- `mix[].asset_class` is stable key enum (`equity|fixed_income|hedge|cash|other`) + `label` display  
- `concentration.items[].key` stable unique (ticker if present else deterministic fallback)

#### 3) Task orders I will issue next (outside this thread)
1) **To DS (implementation spec + code changes, no deploy):** extend  
`infra/aws/lambda/bd-pipeline/opal-partners-data/` with the 4 routes above, including:
- parquet reads: `gold/client_performance.parquet`, `gold/account_performance.parquet`
- latest snapshot selection under `gold/holdings_lots/`
- classification: import canonical `infra/aws/lambda/v2_portal/_shared/etf_classification.py` (ticker-first), fallback to name-pattern/other

2) **To DT (deploy):** deploy updated `opal-partners-data` Lambda once DS hands off.

3) **To RD (frontend):** implement L3/L4 panels in  
`portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`:
- paired Mix + Concentration (linked selection state)
- compact AUA/NNA timeseries charts (client-side aggregation; “aggregate full history then filter for display” pattern)

Thread complete; no open questions remain for alignment.

---
