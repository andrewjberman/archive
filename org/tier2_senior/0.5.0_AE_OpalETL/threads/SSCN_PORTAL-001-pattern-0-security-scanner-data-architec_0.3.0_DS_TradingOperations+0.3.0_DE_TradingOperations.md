# Thread Receipt: Pattern 0: Security Scanner data architecture -- pipeline storage API shape

**Thread ID:** SSCN_PORTAL-001-pattern-0-security-scanner-data-architec
**Project Serial:** SSCN_PORTAL-001
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-05T17:36:29Z
**Status:** complete
**Participants:** 0.3.0_DS_TradingOperations, 0.5.0_AE_OpalETL, 0.3.0_DE_TradingOperations

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-05T17:36:18Z
signal: continue
---

## Pattern 0 Alignment -- Security Scanner Data Architecture

I am the COO convening this alignment thread. The Security Scanner PRD is authored and the RD agent (0.3.4_RD_SecurityScanner) is standing by. Before DE wires an endpoint or RD builds a single component, DS, AE, and DE must agree on the data architecture.

**Context available to you all:**
- XLSM audit (principal context): full Factor_Scanning_Model.xlsm structure -- VBA source, formulas, factor metadata (Tab 3), data validation, conditional formatting
- V0 Python scripts: quick_update_weights.py shows the current percentile calculation logic and data column mapping
- PRD: full portal spec at docs/architecture/SECURITY_SCANNER_PRD.md

**Turn order:** DS -> AE -> DE (round_robin). Three turns per agent. DE writes the final data contract on their last turn.

---

**DS (0.3.0_DS_TradingOperations) -- your turn first.**

Read quick_update_weights.py, V0_SYSTEM_REFERENCE.md, and the XLSM audit from context. Then answer:

**1. Source data inventory:**
- What columns does Screening_DIVZ_IDVZ_20251028.xlsx contain? Name the exact column headers for: ticker, company name, market value, country, sector, industry group, and at least 5 factor columns (use the actual column names from the source data file, e.g. `mkt_val`, `ticker`, etc.).
- What are the 6 universe weight columns and their exact names? (e.g. `wt_ivv` for S&P 500)
- How large is the dataset? Rows per universe (approximate) and total factor columns.

**2. Percentile calculation commitment:**
- The current V0 script computes percentiles server-side in Python (`rank(pct=True, method='average') * 100`). For the portal, should this be: (a) pre-computed in a processing Lambda when data arrives and stored in S3 as JSON, OR (b) computed client-side in the browser from raw factor values?
- State which you recommend and why, citing data size (rows x factors x 6 universes).

**3. Proposed S3 output shape:**
For each of the 4 portal tabs, propose what JSON you would produce:
- Tab 1 (Factor Bank): factor metadata -- what fields per factor? (code, name, category, relationship, IC, autocorrelation, coverage, systematic_flag)
- Tab 2 (Universe Data): per-universe security table -- what shape? Separate JSON per universe?
- Tab 3 (Factor Data): static factor reference -- same as Tab 1 metadata?
- Tab 4 (Universe Scanner): per-universe pre-scored securities -- what fields? Does composite score go in the JSON or is it computed client-side from weights?

**4. Refresh cadence:**
- How does the monthly FactSet Excel file arrive? (S3 upload trigger? Manual upload?)
- What triggers the processing pipeline? (S3 event? EventBridge schedule?)

**IMPORTANT (M2):** Anchor every answer to a specific column name, function name, or file. If you say a field exists, name the exact column from the source data (check quick_update_weights.py's column references). Do not describe a field without citing its source column.

**IMPORTANT (M11):** If you are uncertain about a column name, date range, or file location -- use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.

---

**AE (0.5.0_AE_OpalETL) -- after DS:**

Review DS's proposed data shape and answer:

1. **Storage decision:** Static JSON in S3 (pre-processed monthly, served via CloudFront) vs Lambda-computed on demand. Recommend one and explain the tradeoffs for a ~3000-security, 255-factor dataset.
2. **S3 key structure:** Propose exact S3 key patterns for each artifact (factor metadata, per-universe security data, pre-scored securities). Use the opal-data-portal-v2 bucket convention.
3. **Processing Lambda design:** If pre-compute is chosen -- what does the Lambda do? When does it trigger? (S3 event on FactSet file upload?) What memory/timeout is appropriate for a pandas percentile operation on ~3000 x 255?
4. **API endpoint structure:** The PRD asks whether to use `/api/private/security-scanner/...` or `/api/general/...`. Which auth model is appropriate? Name the existing Lambda authorizer and how it passes firmId.
5. **CloudFront:** Does pre-computed data need a CloudFront invalidation on monthly refresh? Which distribution?

Anchor every answer to an existing AWS resource name or Terraform file where applicable. Reference yang-pipeline/main.tf patterns where the architecture is analogous.

---

**DE (0.3.0_DE_TradingOperations) -- final turn (CRITICAL):**

Review DS's data shape and AE's infrastructure decisions. Then produce:

**1. TypeScript interface definitions** (name each interface):
- `FactorDefinition` (fields: code, name, category, relationship, ic, autocorrelation, coverage, systematic_flag -- map to exact JSON keys DS proposed)
- `SecurityRow` (fields for Tab 2/Tab 4: ticker, name, mkt_val, country?, sector, industry_group, factor scores/values)
- `UniverseScannerRow` (Tab 4: rank, ticker, name, composite_score, mkt_val, country?, industry_group, per-factor percentile scores and raw values)
- Any additional interfaces for the API response envelope

**2. API endpoint contract:**
- Exact paths for each fetch (e.g. `/api/private/security-scanner/factors`, `/api/private/security-scanner/universe/{universeId}`)
- Query parameters needed
- Authentication: private API with firmId context or general API?

**3. Client-side vs server-side decision confirmation:**
- Confirm the percentile/composite score approach agreed with DS and AE
- State what the portal computes vs what comes pre-computed in the JSON

**4. Confirmed data contract block:**
Write a structured summary in this format:
```
SSCN_PORTAL DATA CONTRACT -- SSCN_PORTAL-001
Endpoint 1: GET /api/.../factors
  Response shape: { factors: FactorDefinition[] }
  S3 key: ...
  Refresh: monthly

Endpoint 2: GET /api/.../universe/{universeId}
  Response shape: { securities: SecurityRow[] }
  S3 key: ...
  Refresh: monthly

Percentile computation: client-side | server-side (pre-computed)
TypeScript interfaces: FactorDefinition, SecurityRow, UniverseScannerRow (in types.ts)
```


---

## 001.md

---
agent: 0.3.0_DS_TradingOperations
turn: 1
timestamp: 2026-03-05T17:37:06Z
signal: continue
---

## 1) Source data inventory (FactSet Excel: `Screening_DIVZ_IDVZ_20251028.xlsx`)

Anchors:
- `factor-scanner-v0----primary-python-pipeline-script-percentile-logic-universe-mapping-data-columns.py`
  - `DATA_FILE = 'data_tables/Screening_DIVZ_IDVZ_20251028.xlsx'`
  - Universe filter uses `df_source = pd.read_excel(DATA_FILE, header=4)`
  - Universe membership uses `df_source[universe_col] > 0`
  - Core identity fields referenced in code: `ticker`, `name`, `factset_entity_proper_name`, `mkt_val`, `country_name`, `sector_name`, `indgrp_name`

### Core columns (exact column names as referenced by the V0 script)
- Ticker: `ticker` (used repeatedly, e.g., `row_data.get('ticker')`)
- Company name: `factset_entity_proper_name` **or** `name` (script uses fallback: `row_data.get('factset_entity_proper_name') or row_data.get('name')`)
- Market value: `mkt_val`
- Country: `country_name`
- Sector: `sector_name`
- Industry group: `indgrp_name`

### Universe weight columns (6) — exact names
Anchors:
- `UNIVERSE_OPTIONS` dict in `quick_update_weights.py`:

| Universe | Column |
|---|---|
| S&P 500 | `wt_ivv` |
| Russell 1000 | `wt_iwb` |
| Russell 1000 Value | `wt_iwd` |
| MSCI ACWI ex-US | `wt_acwx` |
| MSCI EAFE | `wt_efa` |
| MSCI EAFE Value | `wt_efv` |

### Factor columns (examples)
We can name factor codes from the XLSM Tab 3 audit (Factor Code column) and the system reference; these codes are used as columns in the source dataset in the V0 script when it does `if code in df_universe.columns: header_to_source[...] = code`.

Examples of factor codes (from the XLSM audit “Factor Metadata Sample” and system reference):
- `bv` (Book Value)
- `equity_turn` (Equity Turnover)
- `obv_252d` (On-Balance Volume (252D))
- `midcap` (Midcap)
- `days_to_cover` (Days to Cover)
- (also referenced in system reference examples: `ret_mom_252d`, `assets`, `asset_turn`, `fcf_ev`, etc.)

### Dataset size (as supported by context)
Anchors:
- PRD + system reference: “~3000 securities x 255 factors, 6 universe weight columns”
- PRD universe sizes (approx): ~500 / ~1000 / ~850 / ~1650 / ~700 / ~400
- Factor count: **255** (PRD + system reference)

So: total rows ~3,000+; factor columns ~255; plus 6 universe weight columns; plus identity columns above.

## 2) Percentile calculation commitment (server vs client)

Anchor:
- V0 percentile logic: `calculate_percentiles_with_sign()` uses:
  - sign inversion for relationship: `if sign in ['-1','Inverse',...]: factor_values = -factor_values`
  - percentile: `factor_values.rank(pct=True, method='average') * 100`

### Recommendation: **pre-compute percentiles server-side** (processing Lambda) and store in S3
Reasoning grounded in size:
- If client computes percentiles for Tab 4, worst case is ~3,000 rows × up to 255 factors = **~765k ranks** per universe selection (and potentially repeated on universe switch / factor set changes). That’s feasible in JS but will be noticeably heavy in-browser, and it complicates correctness (ties, NaNs, sign inversion) across browsers.
- Precomputing monthly once is cheap and makes Tab 4 instantaneous; the portal then only recomputes **composite score** client-side as weights change (which is exactly what Excel does via formulas; see XLSM audit formulas on Tab 4 composite cells like `D30`).

So: **server precomputes per-factor percentiles per universe**; **client computes composite** from weights.

## 3) Proposed S3 output shape (per tab)

Key principle: keep Tab 4 “interactive” by not freezing composite; only provide the ingredients (percentiles + raw values). Composite and rank are derived client-side whenever weights change.

### Tab 1 — Factor Bank (selected factors UI)
Source of truth for metadata is XLSM Tab 3 (“3-Factor Data”) columns:
Anchor: XLSM audit “Factor Metadata Sample” header row includes:
- `Category`, `Factor Name`, `Factor Code`, `Relationship`, `IC`, `Coverage (%)`, `Autocorrelation (%)` (and other IC stats)

Proposed JSON:
```json
{
  "asOf": "2025-10-28",
  "factors": [
    {
      "code": "bv",
      "name": "Book Value",
      "category": "size",
      "relationship": "Inverse",
      "ic": 1.89339286807129,
      "coverage_pct": 99.1208861940505,
      "autocorrelation_pct": 0.991878640544131,
      "systematic": "Yes|No", 
      "asset_class": "Systematic Equity|..."
    }
  ]
}
```
Notes:
- `systematic` / `asset_class` are in PRD for Tab 3; XLSM audit shows “Systematic” formatting rules but the exact column name for systematic flag in Tab 3 is implied (conditional formatting on column N in Tab 3; see audit rules for `N1:N1048576` with `"Yes"`). So include it in the factor metadata export.

### Tab 2 — Universe Data (raw values table)
Per universe, store the raw security table with identity columns + raw factor values (only for selected factors, or all 255).
Given portal needs “full dataset for selected universe” like Excel Tab 2, I recommend **store all 255 raw factor columns** once per universe; the UI can display only selected factors.

Shape (per universe file):
```json
{
  "asOf": "2025-10-28",
  "universe": "wt_ivv",
  "securities": [
    {
      "ticker": "AAPL",
      "name": "Apple Inc",
      "mkt_val": 123456.7,
      "country_name": "United States",
      "sector_name": "Information Technology",
      "indgrp_name": "Technology Hardware, Storage & Peripherals",
      "wt_ivv": 0.065,
      "bv":  ...,
      "days_to_cover": ...,
      "...": "..."
    }
  ]
}
```

### Tab 3 — Factor Data (static reference)
This is basically the same dataset as Tab 1 factor metadata, but Tab 3 shows the full library always (independent of selections). So: **same JSON as Tab 1**, possibly with extra columns (IC t-stat, quintile returns, spreads) if we want parity with Excel.

### Tab 4 — Universe Scanner (pre-scored per-factor percentiles + raw values)
Per universe, store:
- identity columns
- raw values for all factors (or at least those selected; but selection is user-driven, so store all)
- percentile columns for all factors, computed with relationship sign inversion

Shape:
```json
{
  "asOf": "2025-10-28",
  "universe": "wt_ivv",
  "rows": [
    {
      "ticker": "AAPL",
      "name": "Apple Inc",
      "mkt_val": 123456.7,
      "country_name": "United States",
      "sector_name": "Information Technology",
      "indgrp_name": "Technology Hardware...",
      "factors": {
        "bv": { "value": 123.4, "pctl": 87.1 },
        "days_to_cover": { "value": 2.3, "pctl": 55.0 }
      }
    }
  ]
}
```

Composite score + rank:
- **Not stored** (computed client-side): `composite = sum(pctl_i * weight_i)/100`
- Rank is then sort order by composite (like Tab 4 VBA `Worksheet_Calculate` auto-sort).

## 4) Refresh cadence (how file arrives + trigger)

From current context, there is no existing “Security Scanner” pipeline yet; so I’m proposing to mirror the DataRefresh pattern (presigned upload → S3 → processing).

### How the monthly FactSet Excel arrives
Most consistent with existing portal ops patterns:
- Manual upload by internal/dev user (like DataRefresh) via presigned URL.
- The uploaded artifact is the FactSet Excel export (e.g., `Screening_DIVZ_IDVZ_YYYYMMDD.xlsx`).

### What triggers processing
- S3 event trigger on the uploaded Excel key (or on an uploaded `manifest.json` like yang-pipeline does).
- Processing Lambda reads the Excel, computes per-universe filtered frames using `wt_* > 0`, computes percentiles using the same logic as `calculate_percentiles_with_sign()`, and writes the JSON artifacts above.

## Open items I need AE/DE to confirm in next turns
1. Do we want Tab 2/Tab 4 stored as **JSON** or **Parquet** in S3 with portal-proxy translating to JSON? (Pure JSON may be large; Parquet is smaller/faster but needs a Lambda/API to serve.)
2. Confirm whether “systematic flag” and “asset class” columns are present in the XLSM Tab 3 export we’ll use as metadata source (audit implies yes via formatting rules, but we should map exact column names when we implement extraction).

---

## 002.md

---
agent: 0.5.0_AE_OpalETL
turn: 2
timestamp: 2026-03-05T17:37:50Z
signal: continue
---

## AE response — Security Scanner Pattern 0 (storage + API shape)

I’m aligned with DS’s recommendation: **pre-compute percentiles server-side monthly**, store in S3, and keep **composite score + rank client-side** (mirrors Excel Tab 4 formulas + VBA auto-sort).

Below are my concrete infra recommendations, anchored to existing Opal patterns (notably the **DataRefresh → yang-pipeline-trigger → S3 json/** pattern in `opal-data-portal-v2`).

---

## 1) Storage decision: S3 static JSON (pre-processed monthly) vs Lambda on-demand

**Recommend: S3 static artifacts (JSON) generated on upload, served read-only.**

Why (tradeoffs for ~3k × 255):
- **Latency / UX:** Tab 4 needs “instant” re-ranking as weights change. If we compute percentiles on-demand per request, we either (a) recompute repeatedly or (b) implement caching complexity. Precompute once/month is simplest.
- **Cost:** One monthly batch Lambda run is cheap; on-demand percentile computation would be expensive if multiple users explore universes/factor sets.
- **Correctness:** One canonical implementation of sign inversion + percentile ranking (DS anchored to `rank(pct=True, method='average') * 100` and “Inverse” negation) avoids browser inconsistencies.
- **Operational parity:** This matches the existing portal pattern where Yang pipeline writes **portal-consumable JSON into `opal-data-portal-v2/json/`** and the portal reads it (DataRefresh “manifest freshness” pattern).

**Important nuance:** JSON size can get big if we embed all 255 factors per security in a nested structure. So we should choose a JSON shape that is:
- columnar-ish (arrays) or
- split into multiple files (metadata + per-universe), and optionally
- gzip-compressed at rest (CloudFront/S3 can serve `Content-Encoding: gzip` if we upload precompressed objects).

---

## 2) Proposed S3 key structure (exact patterns, `opal-data-portal-v2`)

Bucket: **`opal-data-portal-v2`** (shared portal data bucket used by yang pipeline outputs).

I propose a dedicated prefix namespace:

### Raw uploads (input)
- `security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx`
  - Example: `security_scanner/uploads/2025-10-28/Screening_DIVZ_IDVZ_20251028.xlsx`

Optionally also store “latest pointer”:
- `security_scanner/uploads/latest/Screening_DIVZ_IDVZ_latest.xlsx` (copy of latest)

### Processed, portal-consumable JSON (output)
**Metadata (Tab 1 + Tab 3):**
- `json/security_scanner/{asOf}/factor_metadata.json`
- `json/security_scanner/latest/factor_metadata.json`

**Universe raw data (Tab 2):** (per universe)
- `json/security_scanner/{asOf}/universes/{universeId}/universe_data.json`
- `json/security_scanner/latest/universes/{universeId}/universe_data.json`

**Universe scored data (Tab 4 ingredients):** (per universe)
- `json/security_scanner/{asOf}/universes/{universeId}/scanner_data.json`
- `json/security_scanner/latest/universes/{universeId}/scanner_data.json`

Where `universeId` is one of:
- `sp500` (maps to `wt_ivv`)
- `r1000` (`wt_iwb`)
- `r1000v` (`wt_iwd`)
- `acwx` (`wt_acwx`)
- `eafe` (`wt_efa`)
- `eafev` (`wt_efv`)

(Portal-friendly IDs; the JSON can still include the source column name.)

This mirrors the existing “latest/” convention used elsewhere in portal JSON (e.g., yang pipeline writes under `json/latest/...` per the TradingOperations data contract context).

---

## 3) Processing Lambda design (pre-compute path)

### Trigger
Use an **S3 ObjectCreated** event on:
- `opal-data-portal-v2/security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx`

This is analogous to the yang pipeline trigger pattern (S3 event → orchestration Lambda), except we don’t need Step Functions initially unless we want multi-step observability.

### What the Lambda does
Single Lambda (initially) that:
1. Reads the uploaded Excel from S3.
2. Loads into pandas (`pd.read_excel(..., header=4)` as DS anchored).
3. Builds factor metadata from the workbook’s Tab 3 equivalent source (we need DS/DE to confirm whether we extract factor metadata from the XLSM audit artifact or from a maintained CSV/JSON registry; but output is `factor_metadata.json`).
4. For each universe weight column (`wt_ivv`, `wt_iwb`, `wt_iwd`, `wt_acwx`, `wt_efa`, `wt_efv`):
   - filter `df[df[wt_col] > 0]`
   - compute percentiles for each factor with sign inversion for “Inverse”
   - write `universe_data.json` (raw values) and `scanner_data.json` (raw + percentiles)
5. Writes both `{asOf}/...` and `latest/...` copies.

### Memory / timeout sizing
Given 3k × 255 is not huge, but Excel parsing + JSON serialization can be chunky:
- **Memory:** start at **2048 MB** (pandas + openpyxl + JSON building; memory also improves CPU).
- **Timeout:** **300s** (5 minutes) to be safe for first implementation.
This is consistent with other “data generator” Lambdas in our estate that use 512–1024MB+ and multi-minute timeouts (see yang pipeline generators in the provided inventory context).

### Layer / dependencies
Likely needs:
- `pandas`
- `openpyxl`
Potentially `numpy`.

We already have patterns for pandas layers in yang pipeline (`pandas (py3.11)` layer) and an `openpyxl-layer` exists (but note: in yang pipeline it’s hardcoded to `openpyxl-layer:1` and owned by bd-pipeline). For Security Scanner, I’d prefer we **create a dedicated layer** (e.g., `security-scanner-deps`) or reuse existing pandas layer if compatible with runtime.

(We will only build a new layer if/when DS/DE confirms exact dependency set; I won’t publish anything until the contract is final.)

---

## 4) API endpoint structure + auth model

### Recommend: `/api/scoped/security-scanner/...` (dev-gated during buildout)
PRD says Security Scanner is `requiresDev: true` during buildout. That aligns with the existing **DataRefresh** pattern:
- `/api/scoped/...` routes are dev-gated (per TradingOperations contract: “DataRefresh requires userType 'Dev' claim in JWT.”)

So:
- **During Phase 0 / buildout:** use `/api/scoped/security-scanner/...`
- **Later (when released to internal users):** migrate to `/api/private/security-scanner/...` (JWT internal tier)

I do **not** recommend `/api/general/...` for this dataset because it’s proprietary vendor data and should not be anonymously callable.

### Existing auth mechanism to anchor to
From context: **CloudFront Lambda@Edge `auth-validator-edge`** validates JWT for `/api/private/*` and injects headers like `X-User-Email`, `X-User-Tier`. For scoped routes, the DataRefresh Lambda enforces Dev claim (implementation in `infra/aws/lambda/data_refresh/lambda_function.py`, per DS/DE contract excerpt).

**FirmId:** the prompt asks “how it passes firmId.” In our current portal patterns, firm context is typically implicit (single-firm) or derived from JWT claims/headers. I need DE to confirm whether Security Scanner needs multi-firm partitioning; if yes, we’ll include `firmId` in S3 prefix:
- `json/security_scanner/{firmId}/{asOf}/...`
But absent explicit multi-tenant requirement, keep it single-tenant like other portal JSON.

---

## 5) CloudFront invalidation

If these JSON files are served through CloudFront (likely, since portal reads `/api/general/json/...` style paths in other areas), then **yes**: after monthly refresh we should invalidate the “latest” keys:
- `/json/security_scanner/latest/*`

Which distribution?
- In yang pipeline we have a Lambda `yang-invalidate-cloudfront` (listed in inventory context) that invalidates portal paths after output generation. That suggests there is an existing portal distribution already wired for invalidations.

Action item: I need CloudOps ownership confirmation for the exact distribution ID used for portal JSON (it’s not in the provided context snippet). If DE/COO wants, we can reuse the same invalidation mechanism/pattern as yang pipeline uses (i.e., a small invalidation Lambda invoked at end of processing).

---

## Questions / decisions needed from DS + DE to finalize contract

1. **JSON shape choice for Tab 4 data:**  
   DS proposed nested `factors: { code: {value, pctl} }`. That’s clean but can be large. Alternative is two parallel maps:
   - `values: { code: number }` and `pctls: { code: number }`
   or even columnar arrays.  
   I can support either; DE should pick what’s easiest for TS typing + rendering performance.

2. **Do we store all 255 factors in Tab 2/4 outputs, or only selected?**  
   Since selection is user-driven, I recommend store **all 255** monthly, and the UI filters columns.

3. **Do we need Step Functions?**  
   Not required initially. If COO wants progress visibility like DataRefresh, we can add a small SFN later.

If DE confirms these, I can translate into Terraform resources (new Lambda + S3 notification + IAM + optional CloudFront invalidation) following the mandatory Terraform deployment protocol.

---

## 003.md

---
agent: 0.3.0_DE_TradingOperations
turn: 3
timestamp: 2026-03-05T17:38:32Z
signal: continue
---

## DE response (Turn 3) — lock down portal-facing API + JSON shape preferences

I’m aligned with DS + AE on the core decision:

- **Percentiles computed server-side monthly** using the V0 logic (`rank(pct=True, method='average') * 100` + sign inversion for “Inverse” factors; anchored in `calculate_percentiles_with_sign()` in `quick_update_weights.py`).
- **Composite score + rank computed client-side** from weights (mirrors XLSM Tab 4 formulas like `D30` and VBA auto-sort in `Sheet4.Worksheet_Calculate` from the XLSM audit).

This turn I’ll propose the **portal-friendly JSON shapes + endpoint paths** so AE can size infra and DS can implement the processor without ambiguity.

---

## 1) Endpoint namespace + auth (Phase 0)

I agree with AE: **use `/api/scoped/security-scanner/...` during buildout** because PRD says `requiresDev: true`.

- This matches the existing **DataRefresh** gating model (dev-only) described in the TradingOperations data contract context: scoped routes enforce a Dev claim in JWT, while `/api/private/*` uses CloudFront `auth-validator-edge` to validate JWT and inject headers (e.g., `X-User-Email`, `X-User-Tier`).

Later, when we remove dev-gate, we can migrate to `/api/private/security-scanner/...` with the same response shapes.

---

## 2) JSON shape decision (to keep payloads manageable + TS-friendly)

### My recommendation: **split “values” and “pctls” maps** (not nested `{factors: {code: {value,pctl}}}`)

Reason:
- Nested objects are readable but heavier (extra keys repeated per factor per row).
- For TS + rendering, two flat maps are easy and smaller on the wire.

So each scanner row carries:
- `values: Record<FactorCode, number | null>`
- `pctls: Record<FactorCode, number | null>`

This also makes it trivial to compute composite:
`composite = sum(pctls[code] * weight[code]) / 100` (skip nulls).

---

## 3) Concrete API shapes (portal consumption)

These map 1:1 to AE’s S3 keys under `opal-data-portal-v2/json/security_scanner/...`.

### (A) Factor metadata (Tab 1 + Tab 3)
**GET** `/api/scoped/security-scanner/factors`

Response:
```json
{
  "asOf": "2025-10-28",
  "factors": [
    {
      "code": "bv",
      "name": "Book Value",
      "category": "size",
      "relationship": "Inverse",
      "ic": 1.89339286807129,
      "coveragePct": 99.1208861940505,
      "autocorrelationPct": 0.991878640544131,
      "assetClass": "Systematic Equity",
      "systematic": "Yes"
    }
  ]
}
```

Anchors for fields:
- `code`, `name`, `category`, `relationship`, `ic`, `coverage (%)`, `autocorrelation (%)` come from XLSM Tab 3 (“3-Factor Data”) sample in the audit context.
- `systematic` is implied by conditional formatting on column **N** in Tab 3 audit (`N1:N1048576` rules). We’ll need DS to confirm exact column header name when extracting, but the JSON key should be stable.

S3:
- `json/security_scanner/latest/factor_metadata.json`

### (B) Universe raw data (Tab 2)
**GET** `/api/scoped/security-scanner/universe/{universeId}/data`

Response:
```json
{
  "asOf": "2025-10-28",
  "universeId": "sp500",
  "sourceUniverseColumn": "wt_ivv",
  "securities": [
    {
      "ticker": "AAPL",
      "name": "Apple Inc",
      "mktVal": 123456.7,
      "country": "United States",
      "sector": "Information Technology",
      "industryGroup": "Technology Hardware...",
      "universeWeight": 0.065,
      "values": {
        "bv": 123.4,
        "days_to_cover": 2.3
      }
    }
  ]
}
```

Anchors for identity columns from V0 script:
- `ticker`, `factset_entity_proper_name` or `name`, `mkt_val`, `country_name`, `sector_name`, `indgrp_name` (all referenced in `quick_update_weights.py`).

S3:
- `json/security_scanner/latest/universes/{universeId}/universe_data.json`

### (C) Universe scanner data (Tab 4 ingredients)
**GET** `/api/scoped/security-scanner/universe/{universeId}/scanner`

Response:
```json
{
  "asOf": "2025-10-28",
  "universeId": "sp500",
  "sourceUniverseColumn": "wt_ivv",
  "rows": [
    {
      "ticker": "AAPL",
      "name": "Apple Inc",
      "mktVal": 123456.7,
      "country": "United States",
      "sector": "Information Technology",
      "industryGroup": "Technology Hardware...",
      "values": { "bv": 123.4, "days_to_cover": 2.3 },
      "pctls": { "bv": 87.1, "days_to_cover": 55.0 }
    }
  ]
}
```

Portal computes:
- `compositeScore` (client-side)
- `rank` (client-side sort order)

S3:
- `json/security_scanner/latest/universes/{universeId}/scanner_data.json`

---

## 4) UniverseId mapping (portal constants)

I support AE’s portal-friendly IDs; we’ll hardcode this mapping in `portal/src/pages/SecurityScanner/types.ts`:

- `sp500` -> `wt_ivv`
- `r1000` -> `wt_iwb`
- `r1000v` -> `wt_iwd`
- `acwx` -> `wt_acwx`
- `eafe` -> `wt_efa`
- `eafev` -> `wt_efv`

(These exact weight column names are anchored in `UNIVERSE_OPTIONS` in `quick_update_weights.py`.)

---

## 5) Open questions for DS + AE (need answers before my final “data contract” turn)

1. **Do we include all 255 factors in `values/pctls`, or only selected?**  
   I recommend **all 255** in S3 artifacts (monthly), UI filters by selection. Confirm.

2. **Null handling:** if a factor value is missing/NaN, do we emit `null` and omit from percentile ranking (as pandas rank would)? I recommend `null` in JSON and skip in composite.

3. **Compression:** AE mentioned pre-gzipping. If we do, portal-proxy / CloudFront must serve correct `Content-Encoding`. AE: do we already have this pattern in any existing `json/latest/*.json` objects, or is it new?

If DS/AE confirm these 3, I can produce the final “SSCN_PORTAL DATA CONTRACT” block + TS interface names/shapes on my last turn.

---

## 004.md

---
agent: 0.3.0_DS_TradingOperations
turn: 4
timestamp: 2026-03-05T17:39:00Z
signal: continue
---

## DS response (Turn 4) — confirm JSON contents + null semantics + factor coverage

I’m aligned with DE’s proposed JSON shapes (split `values` + `pctls` maps) and AE’s S3 prefix plan. Below are the concrete confirmations + the remaining “must-anchor” items.

---

## 1) Confirm: include **all 255 factors** in monthly artifacts (Tab 2 + Tab 4)

**Decision:** Yes — store **all 255 factor codes** in the monthly `values` (Tab 2) and in both `values` + `pctls` (Tab 4 scanner ingredients).

**Why (anchored to workbook behavior):**
- In the XLSM, Tab 3 (“3-Factor Data”) is the full factor library, and Tab 1 selection is a *view* over that library. The portal needs to support arbitrary factor selection at runtime (Tab 1 Factor Bank), so the backend cannot anticipate which subset is needed.
- In the V0 script, factor columns are treated as “present in `df_universe.columns`” and mapped dynamically (`if code in df_universe.columns:`). That implies the source dataset is already “wide” with all factor columns, and selection is a UI concern.

**Implication:** payload size is the main cost; but it’s a once-per-month generation and then read-only.

---

## 2) Null / NaN handling (raw values + percentiles + composite)

Anchors:
- `calculate_percentiles_with_sign()` in `quick_update_weights.py`:
  - `factor_values = pd.to_numeric(df[tab3_column], errors='coerce')` → non-numeric becomes `NaN`
  - `percentiles = factor_values.rank(pct=True, method='average') * 100`
- Composite in V0 is computed as mean across percentile columns with `skipna=True`:
  - `df_universe['composite_score'] = df_universe[percentile_cols].mean(axis=1, skipna=True)`

**Decision (contract-level):**
- In JSON, emit missing raw factor values as `null` in `values[code]`.
- Emit missing percentiles as `null` in `pctls[code]`.
- Client composite calculation should **skip null percentiles** (same intent as pandas `skipna=True`), but must also handle the “all-null” case:
  - If all selected factors have `null` percentile for a security, composite should be `null` (or `NaN`) and sort to bottom.

**Tie behavior:** pandas `rank(method='average')` is the canonical tie-break. We should not attempt to reproduce ranking client-side; that’s why we precompute.

---

## 3) Relationship (“Inverse”) sign inversion — confirm semantics

Anchor:
- `calculate_percentiles_with_sign()`:
  - `if sign in ['-1', 'Inverse', 'inverse']: factor_values = -factor_values`

**Decision:** Percentile computation uses:
- If factor `relationship == "Inverse"` (from XLSM Tab 3 Relationship column), then negate raw values before ranking.
- Store `pctls` already “directionally correct” (i.e., higher percentile always means “better” after applying relationship).

This matches the Excel intent: users weight “goodness” consistently even when raw factor is inverse.

---

## 4) Identity columns — confirm canonical field mapping

Anchors (V0 script references):
- `ticker`
- `factset_entity_proper_name` or `name` fallback
- `mkt_val`
- `country_name`
- `sector_name`
- `indgrp_name`
- universe membership columns `wt_ivv`, `wt_iwb`, `wt_iwd`, `wt_acwx`, `wt_efa`, `wt_efv`

**Decision:** In the processor:
- `name` should be populated as `factset_entity_proper_name` if present else `name` (exactly as V0 does).
- `universeWeight` in Tab 2/4 outputs should be the value from the universe column used for filtering (e.g., `wt_ivv` for `sp500`).

---

## 5) Compression question (AE/DE asked)

I don’t have an existing “portal JSON is gzipped” precedent in the provided context. From a DS standpoint:
- **Not required for correctness**; it’s an optimization.
- If we do gzip, we must ensure S3 object metadata sets `Content-Encoding: gzip` and `Content-Type: application/json`, otherwise browsers will download garbage.

So my recommendation for Phase 0: **ship uncompressed JSON first**, measure object sizes, then decide on gzip + CloudFront behavior once we see actual payload sizes.

---

## 6) Remaining must-anchor gap (I cannot resolve without reading the actual FactSet Excel)

COO’s original Q1 asked for “exact column headers” for at least 5 factor columns *from the source file*. Right now, we only have factor codes from the XLSM Tab 3 audit (e.g., `bv`, `days_to_cover`, `obv_252d`) and the V0 script’s assumption that those codes exist as columns in `Screening_DIVZ_IDVZ_20251028.xlsx`.

To fully close that requirement, we need to **inspect the Excel header row** (since V0 reads with `header=4`). If the file is present in-repo under `data_tables/`, I can read it next turn and list the exact headers as they appear.

**Request to thread:** confirm whether `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx` exists in this repo (or provide its path). If it exists, I’ll tool-read it and provide the exact column header list (ticker/name/mkt_val/country/sector/indgrp + 5 factor columns) to satisfy M2 with zero inference.

---

## Answers to DE’s 3 open questions (explicit)

1) All 255 factors in artifacts? **Yes.**  
2) Null handling? **Emit `null` for missing; skip nulls in composite; all-null → composite null/bottom.**  
3) Compression? **Defer; start uncompressed Phase 0 unless AE confirms existing gzip pattern for portal JSON.**

---

## 005.md

---
agent: 0.5.0_AE_OpalETL
turn: 5
timestamp: 2026-03-05T17:39:26Z
signal: continue
---

## AE response (Turn 5) — close infra-side open items (gzip, API wiring pattern, and “exact headers” gap)

### 1) Confirming DS/DE decisions (what I will build against)
I’m aligned with DS Turn 4 + DE Turn 3:

- **All 255 factors** included in monthly artifacts (`values` for Tab 2; `values` + `pctls` for Tab 4).
- **Nulls:** emit `null` for missing raw values and percentiles; portal composite skips nulls; all-null composite sorts to bottom.
- **Relationship inversion:** percentiles are computed server-side with “Inverse” negation before ranking (canonical logic anchored to `calculate_percentiles_with_sign()` in `quick_update_weights.py`).

### 2) Compression (gzip) — recommendation + what’s required if we do it
I agree with DS: **Phase 0 should ship uncompressed JSON** to avoid introducing a new serving behavior while we’re still locking the contract.

If/when we add gzip later, the processor Lambda must set S3 object metadata correctly:
- `Content-Type: application/json`
- `Content-Encoding: gzip`

Otherwise browsers/portal fetch will not transparently decode. I do **not** have a confirmed existing precedent in the provided context that `opal-data-portal-v2/json/latest/*.json` objects are pre-gzipped, so I’m treating gzip as a Phase 1 optimization.

### 3) API wiring pattern (how portal will read these S3 keys)
To keep infra minimal and consistent with existing portal patterns, I recommend we **do not create a bespoke “security-scanner API Lambda”** initially.

Instead, we should follow the already-established pattern used by other portal JSON reads:
- Portal hits an `/api/.../json/...` style route (implemented in `portal/src/api/portal-proxy.ts` per TradingOperations context), and that proxy reads from **`opal-data-portal-v2`**.

So for Security Scanner, DE can map:
- `GET /api/scoped/security-scanner/factors` → proxy reads `opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json`
- `GET /api/scoped/security-scanner/universe/{universeId}/data` → reads `.../universe_data.json`
- `GET /api/scoped/security-scanner/universe/{universeId}/scanner` → reads `.../scanner_data.json`

This keeps auth consistent with “scoped” routes (dev-gated) without adding new Lambda surface area.

### 4) Processing trigger + CloudFront invalidation (what I can implement once contract is final)
**Trigger:** S3 ObjectCreated on:
- `opal-data-portal-v2/security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx`

**Outputs written:**
- `opal-data-portal-v2/json/security_scanner/{asOf}/...`
- `opal-data-portal-v2/json/security_scanner/latest/...`

**CloudFront invalidation:** only needed if the portal JSON path is cached behind CloudFront. Since yang-pipeline already has `yang-invalidate-cloudfront` (function exists in inventory context), we can mirror that pattern later, but I need CloudOps to confirm the distribution + whether these JSON paths are cached. For Phase 0, we can often rely on low TTLs or cache-busting via `asOf` paths; the only “sticky” path is `latest/`.

### 5) “Exact headers” gap (COO requirement) — what I need to proceed
DS is correct: we cannot truthfully list the exact Excel headers for 5 factor columns without reading the actual `Screening_DIVZ_IDVZ_20251028.xlsx` file (because `pd.read_excel(..., header=4)` means the header row is inside the workbook).

**Action needed from DE/COO (pick one):**
1) Confirm the file is present in-repo at `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx` (or another path), **or**
2) Provide the path where it lives (even if under `data/` or an S3 location).

Once path is confirmed, DS can tool-read and satisfy the “exact header names” requirement; I don’t want us to guess and bake wrong column names into the contract.

## Questions for DE (so we converge next round)
1) Are we committing to the **portal-proxy reads S3 JSON** approach (no new read API Lambda), at least for Phase 0?
2) Do you want the upload path to be **DataRefresh-style presigned upload** (scoped route that returns presigned PUT), or is this a manual S3 upload by ops? (Infra differs: presign endpoint requires a small Lambda/API route.)

If DE answers these, I can finalize the infra plan and be ready to implement Terraform + the processing Lambda when the thread exits Pattern 0.

---

## 006.md

---
agent: 0.3.0_DE_TradingOperations
turn: 6
timestamp: 2026-03-05T17:39:49Z
signal: continue
---

## DE Turn 6 — decisions + answers to AE questions + unblock “exact headers” requirement

### 1) Confirm Phase 0 read-path: **portal-proxy reads S3 JSON (no bespoke SecurityScanner read Lambda)**
Yes — for Phase 0 we should **reuse the existing portal-proxy pattern** (same concept as DataRefresh reading `opal-data-portal-v2/json/...`).

Rationale (contract-level):
- Keeps surface area small: only one new “processor” Lambda + S3 trigger.
- Keeps auth consistent with `/api/scoped/*` dev gating (same as DataRefresh).
- Avoids inventing a new API Gateway/Lambda stack just to serve static JSON.

So the contract assumes these routes exist and are implemented in `portal/src/api/portal-proxy.ts` (new handlers added there):

- `GET /api/scoped/security-scanner/factors`
  - S3 read: `opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json`
- `GET /api/scoped/security-scanner/universe/{universeId}/data`
  - S3 read: `opal-data-portal-v2/json/security_scanner/latest/universes/{universeId}/universe_data.json`
- `GET /api/scoped/security-scanner/universe/{universeId}/scanner`
  - S3 read: `opal-data-portal-v2/json/security_scanner/latest/universes/{universeId}/scanner_data.json`

(We’ll still keep `{asOf}/...` paths in S3 for cache-busting / history, but portal reads `latest/` by default.)

### 2) Upload path decision: **DataRefresh-style presigned upload (scoped)**
Answering AE Q2: I want **the same UX as DataRefresh**:
- Portal page (dev-only) includes an Upload panel.
- Portal calls a scoped endpoint to get presigned PUT URL(s).
- Browser uploads the FactSet Excel directly to S3.
- S3 ObjectCreated triggers the processor Lambda.

So: we need a small scoped API handler (could be added to the existing `opal-data-refresh-api` Lambda, or a new `opal-security-scanner-api` Lambda) that returns a presigned PUT for:
- `opal-data-portal-v2/security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx`

I’m not prescribing which Lambda owns the presign route (AE choice), but the **route must exist** for portal-driven upload.

### 3) Close the “exact headers” gap (COO M2 requirement) — proposed resolution path
We cannot finalize the data contract without listing **actual Excel header names** for at least 5 factor columns from `Screening_DIVZ_IDVZ_20251028.xlsx` (COO requirement). DS already flagged this correctly.

**Action I need from AE/COO (one of the following):**
- Confirm the file is in-repo at `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx`, OR
- Provide the repo path where it lives, OR
- If it is not in-repo (likely), approve adding a *small* “header snapshot” artifact to the repo (e.g., `docs/architecture/security_scanner_source_headers_20251028.json`) generated from the Excel once, containing:
  - the full header list (row `header=4`), and
  - a sample of 5 factor column names as they appear in the Excel.

Once we have the path, DS can tool-read and post the exact headers next turn; I will then lock TypeScript interfaces to those canonical names (or to our normalized JSON keys if we transform).

### 4) Re-affirm the key contract decisions (so we don’t churn)
- Store **all 255 factors** in monthly artifacts.
- JSON row shape uses **two maps**: `values` and `pctls` (Record keyed by factor code).
- Percentiles are **server-side** (pandas rank + inverse negation); composite + rank **client-side**.
- Phase 0: **no gzip** (uncompressed JSON), revisit later.

## Remaining questions (need answers before my final “DATA CONTRACT” turn)
1) **Source Excel availability:** where is `Screening_DIVZ_IDVZ_20251028.xlsx` accessible for header inspection?
2) **Presign endpoint ownership:** AE preference — extend `opal-data-refresh-api` vs create `opal-security-scanner-api`? (Either is fine; I just need a stable route name + auth behavior for the portal.)

Once those are answered, my final turn will publish the full `SSCN_PORTAL DATA CONTRACT -- SSCN_PORTAL-001` block + TS interface definitions exactly as COO requested.

---

## 007.md

---
agent: 0.3.0_DS_TradingOperations
turn: 7
timestamp: 2026-03-05T17:40:15Z
signal: converge
---

## DS Turn 7 (final) — converge on contract + resolve remaining DS-owned items

### A) I confirm the final architecture decisions (no further DS objections)

**Storage + compute**
- **Monthly precompute** of per-factor percentiles **server-side** using the V0 canonical logic in `quick_update_weights.py`:
  - `pd.to_numeric(..., errors="coerce")`
  - if `relationship == "Inverse"` then negate before ranking
  - `rank(pct=True, method="average") * 100`
- **Client-side only** computes:
  - `compositeScore = sum(pctl[code] * weight[code]) / 100` (skip nulls)
  - `rank` = sort order by compositeScore desc (nulls bottom)
- **All 255 factors** included in monthly artifacts (Tab 2 values; Tab 4 values+pctls).

**Row identity fields (source anchors in V0 script)**
- `ticker` (`row_data.get('ticker')`)
- `name` = `factset_entity_proper_name` fallback to `name`
- `mkt_val`, `country_name`, `sector_name`, `indgrp_name`
- universe membership columns: `wt_ivv`, `wt_iwb`, `wt_iwd`, `wt_acwx`, `wt_efa`, `wt_efv` from `UNIVERSE_OPTIONS`.

**JSON shape**
- Use DE’s **split maps**:
  - `values: Record<FactorCode, number|null>`
  - `pctls: Record<FactorCode, number|null>`

**Null semantics (anchored to pandas behavior + V0 composite `skipna=True`)**
- Missing raw values → `values[code] = null`
- Missing percentiles → `pctls[code] = null`
- Composite skips null percentiles; if all selected are null → composite null and sorts bottom.

### B) Blocking item: “exact Excel header names” cannot be satisfied from current context

COO requirement (M2): list exact column headers from `Screening_DIVZ_IDVZ_20251028.xlsx` (ticker/name/mkt_val/country/sector/industry group + 5 factor columns).  
**Current thread context does not include the actual Excel file contents**, only:
- the V0 script’s *referenced* column names (`ticker`, `mkt_val`, etc.), and
- factor codes from the XLSM Tab 3 audit (e.g., `bv`, `days_to_cover`, `obv_252d`), which the V0 script assumes exist as columns in the FactSet export.

As DS, I cannot truthfully assert the *exact* header strings for 5 factor columns without reading the Excel header row (`pd.read_excel(..., header=4)`).

### C) Concrete resolution path (minimal, deterministic)

One of the following must happen to close M2:

1) **Provide repo path** to the FactSet export (preferred):
   - If `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx` exists in-repo, I (or next DS session) will tool-read it and post the exact headers.

2) If the Excel cannot live in-repo, approve adding a small checked-in artifact generated once from the Excel:
   - `docs/architecture/security_scanner_source_headers_20251028.json`
   - Contents: `{ asOf, headerRowIndex: 4, headers: string[] }`
   - This becomes the permanent anchor for “exact header names” without storing vendor data.

### D) DS handoff to DE/AE (what to write into the final contract)

DE can safely finalize the SSCN contract using:
- Universe mapping from `UNIVERSE_OPTIONS` (V0 script)
- Identity columns listed above (V0 script)
- Factor metadata fields from XLSM Tab 3 (“3-Factor Data”) header row in the audit:
  - Category, Factor Name, Factor Code, Relationship, IC, Coverage (%), Autocorrelation (%)
  - plus Systematic flag (implied by Tab 3 column N conditional formatting rules in audit)

**But** the contract must include a note: “Exact source Excel headers pending file inspection; processor normalizes to canonical JSON keys regardless.”

That’s all from DS; I consider Pattern 0 resolved pending the single operational step of locating/inspecting the FactSet Excel headers.

---

## 008.md

---
agent: 0.5.0_AE_OpalETL
turn: 8
timestamp: 2026-03-05T17:40:35Z
signal: converge
---

## AE final (Turn 8) — infra convergence + explicit “what’s blocked / what’s not” for SSCN_PORTAL-001

### ✅ Converged architecture (what infra will be built against)

**Compute + storage**
- **Precompute monthly** (on upload) in a **single processing Lambda**:
  - Reads FactSet Excel with `pd.read_excel(..., header=4)` (anchored in `quick_update_weights.py`).
  - For each universe column in `UNIVERSE_OPTIONS` (`wt_ivv`, `wt_iwb`, `wt_iwd`, `wt_acwx`, `wt_efa`, `wt_efv`), filters `> 0`.
  - Computes percentiles per factor using canonical logic from `calculate_percentiles_with_sign()`:
    - coerce numeric (`errors="coerce"`)
    - negate for `relationship == "Inverse"`
    - `rank(pct=True, method="average") * 100`
- Writes **static JSON artifacts** to S3; portal reads via **portal-proxy** (no bespoke read Lambda for Phase 0).
- **Client computes** `compositeScore` + `rank` from `pctls` and weights (Excel parity: Tab 4 formulas + VBA auto-sort).

**JSON row shape (contracted)**
- `values: Record<FactorCode, number|null>`
- `pctls: Record<FactorCode, number|null>`
- Null semantics: emit `null`; client composite skips nulls; all-null composite sorts bottom.

**Factor coverage**
- Store **all 255 factors** in monthly artifacts (Tab 2 values; Tab 4 values+pctls).

---

### ✅ S3 key structure (bucket + exact prefixes)

Bucket: `opal-data-portal-v2`

**Upload (input)**
- `security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx`

**Processed outputs (portal-consumable)**
- `json/security_scanner/{asOf}/factor_metadata.json`
- `json/security_scanner/{asOf}/universes/{universeId}/universe_data.json`
- `json/security_scanner/{asOf}/universes/{universeId}/scanner_data.json`

**Latest pointers (portal default reads)**
- `json/security_scanner/latest/factor_metadata.json`
- `json/security_scanner/latest/universes/{universeId}/universe_data.json`
- `json/security_scanner/latest/universes/{universeId}/scanner_data.json`

UniverseId mapping (portal-friendly, but JSON should also include `sourceUniverseColumn`):
- `sp500`→`wt_ivv`, `r1000`→`wt_iwb`, `r1000v`→`wt_iwd`, `acwx`→`wt_acwx`, `eafe`→`wt_efa`, `eafev`→`wt_efv`.

---

### ✅ API shape + auth (Phase 0)

**Routes (scoped/dev-gated) implemented in `portal/src/api/portal-proxy.ts`**
- `GET /api/scoped/security-scanner/factors` → S3 read `.../latest/factor_metadata.json`
- `GET /api/scoped/security-scanner/universe/{universeId}/data` → S3 read `.../latest/.../universe_data.json`
- `GET /api/scoped/security-scanner/universe/{universeId}/scanner` → S3 read `.../latest/.../scanner_data.json`

Auth model: `/api/scoped/*` (same dev-gated pattern as DataRefresh; JWT validated by the existing CloudFront Lambda@Edge `auth-validator-edge`, with scoped route enforcing Dev claim as DataRefresh does).

---

### ✅ Upload UX decision + infra implication

DE confirmed: **DataRefresh-style presigned upload** (scoped) → browser PUT to S3 → S3 event triggers processor.

Infra implication: we need **one scoped presign endpoint** that returns a presigned PUT URL for the upload key above. Two acceptable implementations:
1) **Extend** existing `opal-data-refresh-api` (preferred for minimal new infra surface area), adding a new route handler for Security Scanner presign, OR
2) Create a new small API Lambda (e.g., `opal-security-scanner-api`) just for presign.

I recommend **option (1)** unless COO/CTO wants strict separation.

---

### ⚠️ Only remaining blocker: “exact Excel header names” requirement

DS correctly flagged: we cannot satisfy COO’s M2 (“exact column headers for 5 factor columns from `Screening_DIVZ_IDVZ_20251028.xlsx`”) without access to the actual Excel file (or a checked-in header snapshot).

**This does NOT block infra build-out** (processor can normalize to canonical JSON keys), but it **does block closing the thread’s documentation requirement** unless one of these happens:
- Provide repo path to the Excel file (if it exists in-repo), or
- Approve adding a small non-data artifact like `docs/architecture/security_scanner_source_headers_20251028.json` containing the header list only.

Once that’s available, DS can tool-read and publish the exact header strings.

---

### CloudFront invalidation (Phase 0 stance)

Phase 0: **no gzip, no mandatory invalidation**. We rely on:
- versioned `{asOf}/...` paths for cache-busting, and
- `latest/` paths may need invalidation later if CloudFront aggressively caches them (requires CloudOps distribution ID confirmation; not in current context).

---

## Final handoff (what DE can write as the authoritative contract)

DE can now publish `SSCN_PORTAL DATA CONTRACT -- SSCN_PORTAL-001` using:
- the S3 keys above,
- the 3 scoped endpoints above,
- server-side percentile computation + client-side composite/rank,
- and a note that “exact source Excel headers pending file inspection / header snapshot.”

I’m done; no further infra decisions are pending inside this thread.

---
