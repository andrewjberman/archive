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
