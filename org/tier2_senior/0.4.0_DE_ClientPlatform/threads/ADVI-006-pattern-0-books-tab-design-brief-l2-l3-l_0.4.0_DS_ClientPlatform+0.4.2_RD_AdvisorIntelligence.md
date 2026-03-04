# Thread Receipt: Pattern 0: Books tab design brief L2 L3 L4

**Thread ID:** ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l
**Project Serial:** ADVI-006
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-04T16:37:03Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.2_RD_AdvisorIntelligence, 0.4.0_DE_ClientPlatform

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-04T16:36:51Z
signal: continue
---

## Pattern 0 Alignment -- Books Tab Design Brief (L2/L3/L4)

I am the COO convening this alignment thread. The Books tab is the deepest, most data-intensive part of AdvisorIntelligence. Before DE wires an endpoint or RD builds a component, DS must surface what data currently flows from the advisor-publisher Lambda and what gold layer data (scripts 03, 05b, 06) is available but NOT yet published.

**This is a re-run.** The previous thread (ADVI-003) failed to produce its required deliverable: the Books design brief. This time, DE MUST write the file docs/architecture/advisor_intelligence/books_tab_design_brief.md on their final turn. If it does not exist after this thread completes, the thread has failed.

**Turn order:** DS -> RD -> DE. Three turns per agent. DE writes the design brief as their final deliverable.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read the advisor-publisher lambda_function.py, scripts 03/05b/06, and data_contract.xml from context. For each level, describe:

**L2 (Advisor Book -- aggregate of all advisor's relationships):**
- What fields currently appear in the advisor S3 output? Name the actual S3 key pattern and the specific dict keys in the publisher output.
- What summary metrics are currently published (AUA total, client count, NNA)?
- What is MISSING that the PRD requires: NMNC/NMEC breakdown, geography, account type, tax exposure, income/fees, portfolio composition? For each missing field, name the gold layer source file and the specific function or variable that produces it.

**L3 (Relationship/Client View):**
- What currently flows in clients/{clientKey}.json? Name the S3 key pattern. List the top-level dict keys currently present.
- What is missing: performance time series, full account list, client segment data?

**L4 (Account + Holdings + Tax):**
- Script 03: what output does it produce? What fields per lot? Does it currently flow into the publisher output, or is it gold-layer only? Name the specific function and output variable.
- Script 05b: what fields does it produce? Is it in the publisher output?
- Script 06: what output structure does it produce? Is it in the publisher output?
- What L4 fields are COMPLETELY ABSENT from the current publisher output?

**IMPORTANT (M2):** Anchor every answer to a specific function name, dict key, S3 path, or parquet column. If you say "this data is available," name where it currently lives (which file, which variable). Do not say a field exists without citing the source.

**RD (0.4.2_RD_AdvisorIntelligence) -- after DS:**
Propose visual layout for L2, L3, L4. For each level: what sections exist on the page, what data field from DS's description goes in each section, what existing portal components (Panel/PanelContent/DataTable/etc.) can be reused. Do NOT propose fields that DS did not confirm exist.

**DE (0.4.0_DE_ClientPlatform) -- final turn (CRITICAL):**
Review DS's gap list and RD's layout. Then WRITE the design brief to:
  docs/architecture/advisor_intelligence/books_tab_design_brief.md

The brief must cover:
1. L2 advisor book layout with data field mappings (DS confirmed fields only)
2. L3 relationship view layout
3. L4 account + holdings view with tax summary and lot drill-down
4. Component reuse opportunities
5. DS data gaps: explicit list of what must be added to the publisher before RD can implement
6. TypeScript interface additions needed (new types or extensions to existing types)


---

## 001.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 1
timestamp: 2026-03-04T16:37:46Z
signal: continue
---

## Books Tab (L2/L3/L4) — What exists today vs PRD gaps (source-anchored)

Below is strictly what is **currently produced** by the BD publishers and gold scripts in the provided context. I’m anchoring every claim to a **function name + S3 key + dict key** (for JSON) or **script + output key + column names** (for Parquet).

---

# L2 — Advisor Book (one advisor’s aggregate book)

## L2.1 What is currently published (S3 key + dict keys)

**Producer:** `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`  
**Function:** `build_advisor_books(acct, tax, cdim, today)`  
**S3 key pattern written:** `gold/advisors/{advisor_id}/book.json` via `_advisor_output_key(adv_id)` returning `f'gold/advisors/{adv_id}/book.json'`.

**Top-level dict keys in each advisor book.json (per `book = {...}` in `build_advisor_books`)**
- `generated_at`
- `data_as_of`
- `book_type` (hardcoded `"architect"`)
- `book_key` (snake_case id from `_advisor_id()`)
- `book_name` (architect display name string)
- `summary`: `{ total_aua, client_count, account_count }`
- `nna`: `{ ytd, qtd, mtd }` computed by inner `_nna_since(start_ts)`
- `growth`: `{ ytd_pct, qtd_pct }` computed from `_aua_at(start_ts)`
- `tax_exposure`: from `_build_advisor_tax_exposure(tax, rel_ids)`
- `income_fees`: **all zeroed** in `build_advisor_books` (explicit literal)
- `portfolio_composition`: **empty/zeroed** in `build_advisor_books` (explicit literal)
- `engagement`: from `_build_advisor_engagement(acct_arch, cdim, rel_ids, today)`
- `clients`: list of `{ client_key, client_name, aua }` built from `client_snap` merge with `cdim`

## L2.2 Summary metrics currently published
From `summary`, `nna`, `growth`, `engagement`:
- Total AUA: `summary.total_aua` (sum of `acct_arch` latest-date `total_aua`)
- Client count: `summary.client_count` (unique `relationship_id` at latest date)
- Account count: `summary.account_count` (unique `account_id` at latest date)
- NNA: `nna.ytd`, `nna.qtd`, `nna.mtd` (computed from deltas of `cum_inflows`/`cum_outflows`)
- AUA growth %: `growth.ytd_pct`, `growth.qtd_pct`
- Engagement flows TTM: `engagement.net_flows_ttm`, `engagement.inflows_ttm`, `engagement.outflows_ttm`
- Tenure: `engagement.avg_tenure_days` (mean of `today - cdim.first_seen_date`)

## L2.3 PRD-required items that are missing (and where the data would come from)

### (A) NMNC/NMEC breakdown (composition + counts)
**Missing from advisor book.json:** no NMNC/NMEC AUA split, no NMNC/NMEC counts.  
**Gold source that could support it:** `gold/client_dimension.parquet` has `first_seen_date` (loaded in `load_sources()` as `cdim` with columns including `first_seen_date`).  
**Where to implement:** in `build_advisor_books()` using `cdim.first_seen_date` to classify each relationship in `rel_ids` as NMNC vs NMEC (rule needs definition; PRD suggests “new vs existing clients”).  
**Note:** This is not currently computed anywhere in `bd-portal-advisor-publisher`.

### (B) Geography breakdown (state/city) for the advisor’s book
**Missing:** no state/city aggregation in advisor book.json.  
**Potential gold source:** `gold/client_dimension.parquet` includes `primary_state` / `primary_city` in the broader system (confirmed elsewhere in DS logs, but in *this* lambda `load_sources()` prunes cdim to: `relationship_id, relationship_name, first_seen_date, primary_architect, primary_implementor` only).  
**Where to implement:** expand `load_sources()` cdim columns + aggregate within `build_advisor_books()`.

### (C) Account type breakdown
**Missing:** no account_type composition.  
**Gold source:** `gold/accounts_dimension_latest.parquet` contains `account_type` (per script 03/05b docs; also referenced in 05b header).  
**Not loaded by advisor-publisher today.** Would require loading accounts dimension and joining on `account_id` in `build_advisor_books()`.

### (D) Tax exposure summary
**Partially present:** `tax_exposure` exists and is computed in `_build_advisor_tax_exposure()` from `gold/views/client_tax_liability.parquet` (loaded as `tax` in `load_sources()`).
- Present fields include: `taxable`, `tax_deferred`, `tax_free` and pcts, plus `qualified_aua`, `non_qualified_aua`, `non_qualified_cost_basis`, `non_qualified_unrealized_gain`, `short_term_gain`, `long_term_gain`.
**Missing vs PRD:** PRD asks “taxable/deferred/free breakdown (from client_tax_liability)” — that part is covered; but PRD also implies richer tax intelligence (e.g., position-level, lot-level drill). That is **not** in L2 advisor book.json.

### (E) Income/fees
**Missing:** advisor book.json `income_fees` is hardcoded zeros in `build_advisor_books()`.  
**Gold source:** none in BD pipeline as implemented; `account_performance.parquet` does not include fees/income fields (see `load_sources()` acct columns). So this is a true upstream data gap unless a new computation is added.

### (F) Portfolio composition / asset allocation / expense ratio / concentration
**Missing:** `portfolio_composition.asset_allocation` is `[]`, `avg_expense_ratio=0.0` literal in `build_advisor_books()`.  
**Gold source:** not present in scripts 03/05b/06 outputs. Holdings lots (03) has `asset_name/ticker/market_value` at lot grain, but no asset class taxonomy. Could compute concentration/top holdings from holdings_lots snapshot if we join and aggregate, but taxonomy still missing.

---

# L3 — Relationship / Client View (clients/{clientKey}.json)

## L3.1 What is currently published (S3 key + dict keys)

**Producer:** same advisor-publisher lambda  
**Function:** `build_client_details(acct, tax, lots, cdim, today)`  
**S3 key pattern written:** `gold/clients/{relationship_id}.json` via `_save_json(response, f'gold/clients/{rel_id_str}.json')`

**Top-level dict keys in each client detail JSON (`response = {...}`)**
- `generated_at`
- `data_as_of`
- `firm_id`
- `client_key` (relationship_id string)
- `client_name` (from `cdim.relationship_name` fallback to id)
- `headline` (from `_build_headline(acct_r)`)
- `tax` (from `_build_tax(acct_r, tax_r, lots_r, today)`)
- `income_fees` (all zeroed literal)
- `portfolio` (allocation empty; `unique_holdings` derived from `num_positions` sum on latest date)
- `engagement` (from `_build_engagement(acct_r, cdim_row, today)`)
- `accounts` (from `_build_accounts(acct_r)`)

## L3.2 What is missing vs PRD

### (A) Performance time series for the relationship
**Missing:** no timeseries array in the JSON.  
**Gold source that exists:** `gold/client_performance.parquet` (relationship-grain daily) exists in the system, but this lambda does **not** load it; it loads `gold/account_performance.parquet` as `acct`.  
**Where to implement:** either:
- add a timeseries section by aggregating `acct_r` over `date` (since acct has daily rows), or
- load `client_performance.parquet` (smaller than account_performance) and attach.

### (B) “Full account list”
**Present, but minimal:** `accounts` includes only:
`{ account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }` from `_build_accounts()`.  
**Missing:** account_name, account_type, registration type, open date, etc. (those live in `accounts_dimension_latest.parquet`, not loaded here).

### (C) Client segment data (NMNC/NMEC, lifecycle)
**Missing:** no NMNC/NMEC classification fields in client detail JSON.  
**Gold source:** `cdim.first_seen_date` is loaded; could compute “relationship age” and classify.

---

# L4 — Account + Holdings + Tax (and what scripts 03/05b/06 provide)

## L4.1 Script 03 — holdings lots (lot-level)
**Script:** `data/black_diamond/scripts/gold/03_build_holdings_lots.py`  
**Output key pattern:** `gold/holdings_lots/YYYY-MM-DD.parquet` (or `gold/holdings_lots/backfill_...` in full mode)  
**Core builder function:** `build_holdings_lots_snapshot(...)`  
**Lot-level fields (from script header + final `cols` list):**
- identifiers/context: `lot_id`, `snapshot_date`, `account_id`, `relationship_id`, `account_name`, `account_type`, `account_registration_type`, `tax_status`, `qualified_flag`
- security: `asset_name`, `ticker`
- lot detail: `acquisition_date`, `purchase_year`, `lot_index`, `original_units`, `current_units`, `cost_per_unit`, `cost_basis`, `current_price`, `market_value`, `accrued_gain`, `holding_period_days`, `term`, `is_open`, `price_quality`

**Does it flow into publisher output today?**
- **Yes, partially and only at client-detail level:** advisor-publisher loads the latest lots snapshot via `_latest_holdings_lots_key()` and `lots = _load_parquet(lots_key)` in `load_sources()`.
- It is used inside `_build_tax(... open_lots ...)` to populate `tax.open_lots[]` and `tax.open_lots_count` in `gold/clients/{relationship_id}.json`.
- Specifically: `_build_tax()` builds `open_lots` by filtering `lots_r` (relationship filtered) and then iterating rows into dicts with available columns.

**Important limitation:** open lots are filtered to taxable in `_build_tax()`:
- `taxable_open = lots[is_open==True]` then if `tax_status` exists: `taxable_open = taxable_open[taxable_open['tax_status'] == 'taxable']`.

## L4.2 Script 05b — account_performance (account-level daily)
**Script:** `data/black_diamond/scripts/gold/05b_build_account_performance.py`  
**Output:** `gold/account_performance.parquet`  
**Key columns (from script header “Output schema” and `final_cols`):**
- `date`, `account_id`, `relationship_id`
- advisor fields: `architect`, `implementor`, `local_relationship`, `manager`, `investment_strategy_name`
- `tax_status`
- `total_aua`, `cum_inflows`, `cum_outflows`, `nna`
- `num_positions`, `pct_priced`

**Does it flow into publisher output today?**
- **Yes.** It is the primary `acct` table loaded by advisor-publisher `load_sources()` and drives:
  - advisor books (`build_advisor_books`)
  - implementor leaderboard (`build_implementor_leaderboard`)
  - client detail headline/accounts/engagement (`build_client_details`)

## L4.3 Script 06 — client_tax_liability (position x purchase_year aggregation)
**Script:** `data/black_diamond/scripts/gold/06_build_client_tax_liability.py`  
**Output:** `gold/views/client_tax_liability.parquet`  
**Builder function:** `build_tax_liability_view(lots)`  
**Grain:** (relationship_id, account_id, asset_name, purchase_year) (plus account metadata columns)  
**Key columns (from `final_cols` in script 06):**
- relationship/account context: `relationship_id`, `account_id`, `account_name`, `account_type`, `account_registration_type`, `tax_status`, `qualified_flag`
- security: `asset_name`, `ticker`, `purchase_year`
- totals: `num_open_lots`, `total_units`, `total_cost_basis`, `total_market_value`, `total_accrued_gain`
- term splits: `short_term_*` and `long_term_*`
- `snapshot_date`

**Does it flow into publisher output today?**
- **Yes.** advisor-publisher loads it as `tax` in `load_sources()` and uses it in:
  - `_build_advisor_tax_exposure()` for advisor book.json
  - `_build_tax()` for client detail JSON (qualified/non-qualified, cost basis by year, top gain positions, etc.)

## L4.4 L4 fields completely absent from current publisher outputs (hard gaps)

Even though we have lots + account_performance + tax_liability, the following PRD L4 items are **not present** in `gold/clients/{relationship_id}.json` or `gold/advisors/{advisor_id}/book.json` today:

1. **Holdings position list (non-lot) with weights**  
   - No `positions[]` section anywhere.
   - We could derive positions by aggregating lots to (asset_name,ticker) and dividing by total AUA, but that is not implemented.

2. **Account metadata needed for “Account + Holdings” view**  
   - Missing: `account_name`, `account_type`, `account_registration_type`, `qualified_flag` at the *account list* level in client detail JSON.
   - `_build_accounts()` only emits `account_id, tax_status, total_aua, cum_* , nna, num_positions`.

3. **Lot drill-down beyond taxable-only**  
   - `_build_tax()` filters lots to taxable; no lot drill for deferred/exempt accounts.

4. **Performance time series at relationship or account level for the UI**  
   - No `timeseries` key in client detail JSON; no account-level timeseries emitted either.

5. **Portfolio analytics (allocation taxonomy, expense ratio, top-5 concentration)**  
   - `portfolio.allocation` empty, `top_5_concentration_pct=0.0` literal.

6. **Income/fees**  
   - All zeros in both advisor book and client detail.

---

# Immediate implications for the Books design brief (what DE/RD should assume)

- **L2 and L3 are currently “headline + tax + engagement + client list/accounts list” only.** Anything beyond that (NMNC/NMEC composition, geo/account-type breakdown, holdings tables, performance charts) requires DS/DT work first.
- **The only true “holdings” data currently published is `tax.open_lots[]` inside client detail JSON**, and it is taxable-only and embedded under the tax section (built in `_build_tax()`).

---

# Questions I need answered by DE/COO before I can spec the next DS work (to avoid guessing)

1. For Books L2/L3: do we want to **extend the existing advisor-publisher outputs** (`gold/advisors/*` and `gold/clients/*`) or introduce a **new Books-specific JSON** shape? (I recommend extending existing to minimize endpoints.)
2. For NMNC/NMEC: confirm the **classification rule** for Books (same as CLA timeseries “<=12 months since first_seen_date” vs something else).
3. For holdings: is the desired L4 “Holdings” view acceptable as **taxable-only lots first** (what we already have), or must we show **all accounts/positions** regardless of tax status?

If we align on those 3, I can produce a concrete DS task order set: (a) add relationship/account timeseries, (b) enrich accounts list with accounts_dimension_latest fields, (c) add positions aggregation derived from lots, (d) add NMNC/NMEC breakdowns.

---

## 002.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 2
timestamp: 2026-03-04T16:38:48Z
signal: continue
---

## Books Tab (L2/L3/L4) — Proposed UI layout using ONLY DS-confirmed published fields

I’m going to propose a concrete L2/L3/L4 layout that is implementable **today** with what DS confirmed is already published by `bd-portal-advisor-publisher`, and I’ll explicitly label “PRD desired but not yet available” as placeholders (no invented fields).

Primary constraint: **do not design UI that requires NMNC/NMEC composition, geo/account-type breakdown, holdings positions, or income/fees**, because DS confirmed those are missing/zeroed in current JSON outputs.

---

# 0) Navigation model (how user moves L2 → L3 → L4)

We already have the core navigation primitives in `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`:
- Advisor selector (admin only) + client picker
- View mode toggle `book | client`

For the design brief, I recommend we formalize the hierarchy as:

- **L2 Advisor Book** = `getAdvisorBook(advisorId)` (admin selects advisor; advisor users later land here automatically)
- **L3 Relationship/Client** = `getClientDetail(clientKey)` (client picker)
- **L4 Account + Holdings + Tax** = *within L3*, driven by `clientDetail.accounts[]` and `clientDetail.tax.open_lots[]` (no new endpoint)

So L4 is not a new route; it’s a drill-down panel inside the L3 view.

---

# 1) L2 — Advisor Book layout (AdvisorBookResponse)

**Data source:** `GET /api/scoped/advisor-intelligence/advisors/{advisor_id}/book.json`  
**S3 key:** `gold/advisors/{advisor_id}/book.json`  
**Producer:** `build_advisor_books()` in `bd-portal-advisor-publisher`  
**Confirmed keys we can use:**
- `summary.total_aua`, `summary.client_count`, `summary.account_count`
- `nna.{ytd,qtd,mtd}`
- `growth.{ytd_pct,qtd_pct}`
- `tax_exposure.{taxable,taxable_pct,tax_deferred,...,qualified_aua,non_qualified_cost_basis,short_term_gain,long_term_gain,...}`
- `engagement.{net_flows_ttm,inflows_ttm,outflows_ttm,avg_tenure_days}`
- `clients[]: { client_key, client_name, aua }`
- `income_fees` and `portfolio_composition` exist but are **zero/empty** (should be visually de-emphasized or hidden)

### L2 page sections (Panels)

1) **Header / Context Bar (inside Books tab header row)**
   - Admin-only advisor selector (already exists)
   - Client search (already exists) but in L2 it acts as “jump to L3”
   - “As of” timestamp: use `data_as_of` from advisor book response

2) **Panel: “Advisor Book Summary” (hero metrics)**
   - Big number: `summary.total_aua`
   - Secondary tiles:
     - `summary.client_count`
     - `summary.account_count`
     - `nna.ytd`, `nna.qtd`, `nna.mtd`
     - `growth.ytd_pct`, `growth.qtd_pct`
   - Visual: use portal `Panel` + `PanelHeader` + `PanelContent` (no custom SubPanel)
   - Note: NNA values can be negative; apply portal “near-zero gray” pattern if we already have it in this page (or at least avoid red for ~0).

3) **Panel: “Tax Exposure”**
   - Donut or stacked bar for `tax_exposure.taxable_pct / tax_deferred_pct / tax_free_pct`
   - Below: “Qualified vs Non-qualified” using `qualified_pct / non_qualified_pct`
   - Below: small table for:
     - `non_qualified_cost_basis`
     - `non_qualified_unrealized_gain`
     - `short_term_gain`
     - `long_term_gain`
   - Important: current BooksTab uses hardcoded hex colors; in the real implementation we should switch to semantic tokens (but that’s implementation, not brief).

4) **Panel: “Engagement”**
   - `engagement.net_flows_ttm`, `inflows_ttm`, `outflows_ttm`
   - `avg_tenure_days` displayed as years (days / 365.25)
   - Avoid “trading buys/sells” because DS confirmed those are not present in advisor book.

5) **Panel: “Clients (Relationships)”**
   - Table list from `clients[]` sorted by `aua` (already sorted by publisher)
   - Columns: Client name, AUA
   - Row click: sets selected client → transitions to L3 (client view)
   - Reuse: existing table pattern from `AdvisorSummaryTable` in ClientsTab.tsx (but refactor to portal primitives).

**PRD-required but not available yet (should be hidden, not stubbed):**
- Income & Fees (advisor book has zeros)
- Portfolio Composition (empty allocation)

---

# 2) L3 — Relationship/Client view layout (ClientDetailResponse)

**Data source:** `GET /api/scoped/advisor-intelligence/clients/{clientKey}.json`  
**S3 key:** `gold/clients/{relationship_id}.json`  
**Producer:** `build_client_details()` in advisor-publisher  
**Confirmed keys we can use:**
- `headline.total_aua`, `headline.account_count`
- `tax.*` including `cost_basis_by_year[]`, `top_gain_positions[]`, `open_lots[]`, `open_lots_count`
- `engagement.net_flows_ttm`, `engagement.avg_relationship_years`
- `accounts[]: { account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }`
- `income_fees` zeroed, `portfolio` mostly empty except `unique_holdings`

### L3 page sections (Panels)

1) **Panel: “Client Summary”**
   - Big number: `headline.total_aua`
   - Tiles:
     - `headline.account_count`
     - `tax.taxable_pct / tax_deferred_pct / tax_free_pct`
     - `engagement.net_flows_ttm`
     - `engagement.avg_relationship_years`
   - Timestamp: `data_as_of`

2) **Panel: “Accounts” (this is the bridge to L4)**
   - Table from `accounts[]`
   - Columns:
     - Account ID (until we have account_name)
     - Tax status
     - AUA
     - NNA (signed)
     - Positions (`num_positions`)
   - Row click sets `selectedAccountId` local state (L4 drill)

3) **Panel: “Tax Intelligence”**
   - Subsections:
     - Tax status AUA split: `taxable/tax_deferred/tax_free` + pct
     - Qualified vs non-qualified: `qualified_aua`, `non_qualified_aua`, counts if present (client detail includes `qualified_account_count`, `non_qualified_account_count`)
     - Cost basis by year table: `tax.cost_basis_by_year[]`
     - Top gain positions table: `tax.top_gain_positions[]` (top 20)
   - This panel is the highest-signal part of current published data; should be prominent.

4) **Panel: “Open Lots (Taxable)”**
   - Use `tax.open_lots[]` with `tax.open_lots_count`
   - Provide filters:
     - Term: short_term vs long_term (field `term`)
     - Account: derived from `open_lots.account_id`
   - Columns (only those present in open_lots dict): `asset_name`, `ticker`, `market_value`, `cost_basis`, `accrued_gain`, `acquisition_date`, `term`, `account_id`
   - This is effectively the current “holdings” view, but explicitly framed as taxable open lots.

**PRD-required but not available yet (should not be designed as real charts):**
- Relationship performance time series (DS confirmed missing)
- Portfolio allocation taxonomy (empty)
- Income/fees (zero)

---

# 3) L4 — Account + Holdings + Tax drill-down (within L3)

Given current data, L4 can only be:

### L4.1 Account detail (from `clientDetail.accounts[]`)
When `selectedAccountId` is set:
- Show a compact “Account Detail” panel:
  - `account_id`
  - `tax_status`
  - `total_aua`
  - `cum_inflows`, `cum_outflows`, `nna`
  - `num_positions`
- No account_name/account_type/open_date available yet (DS confirmed absent).

### L4.2 Account-scoped lots (from `clientDetail.tax.open_lots[]`)
Filter `open_lots` by `account_id === selectedAccountId`:
- Show “Open Lots for Account” table (same columns as above)
- Add a “Back to all accounts” control (clears selectedAccountId)

This gives a real L4 experience without inventing holdings positions.

---

# 4) Component reuse opportunities (within portal/src/pages/AdvisorIntelligence/)

Concrete reuse targets based on current code:

1) **Header bar / pickers**
   - Existing in `tabs/ClientsTab.tsx`: advisor picker + client search + view toggle.
   - Refactor into smaller components inside the page directory (still within allowed scope):
     - `BooksHeaderBar`
     - `AdvisorPicker` (admin-only)
     - `ClientPicker`

2) **Metric tiles**
   - Reuse the existing “HeadlineNumbersContent” pattern but convert to portal tokens and make it generic:
     - `HeadlineMetricGrid` (accepts array of `{label, value, intent}`)

3) **Tables**
   - Reuse the `AdvisorSummaryTable` table styling for:
     - Clients list (L2)
     - Accounts list (L3)
     - Top gain positions (L3)
     - Open lots (L3/L4)

4) **Tax donut**
   - Current `TaxIntelligenceContent` uses Recharts Pie and hardcoded colors.
   - Keep the structure but swap colors to semantic tokens in implementation.

---

# 5) Questions / confirmations needed before DE writes the brief (no guessing)

1) **Should we hide Income & Fees and Portfolio Composition panels entirely** until DS publishes non-zero data?  
   DS confirmed these are literal zeros/empty in both advisor book and client detail outputs today.

2) For L4, is it acceptable that “Holdings” is **taxable open lots only** (explicitly labeled), since `_build_tax()` filters lots to taxable?  
   If not acceptable, DS needs to change `_build_tax()` filtering and/or publish a positions list.

3) Do we want L4 as **inline drill-down** (recommended) or a separate route/subpage?  
   Inline is implementable now with local state; separate route adds complexity without new data.

If DE confirms these three, the design brief can be written with no ambiguity and no phantom fields.

---

## 003.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 3
timestamp: 2026-03-04T16:39:35Z
signal: continue
---

## DE synthesis (Turn 3): lock the implementable L2/L3/L4 scope + enumerate wiring gaps for the brief

I’m aligning DS’s “what exists” with RD’s “what we can render today” and calling out the *hard blockers* that must be resolved before we can claim PRD-complete Books.

### 1) What we can ship **today** (no backend changes) — and should therefore be the baseline in the design brief

**L2 Advisor Book (per-advisor aggregate)**
- Data source: `gold/advisors/{advisor_id}/book.json` written by `build_advisor_books()` in `bd-portal-advisor-publisher`.
- Implementable sections (all DS-confirmed non-zero fields):
  - Summary hero: `summary.total_aua`, `summary.client_count`, `summary.account_count`
  - NNA cards: `nna.{mtd,qtd,ytd}`
  - Growth: `growth.{qtd_pct,ytd_pct}`
  - Tax Exposure: `tax_exposure.*` (including qualified/non-qualified + gains fields)
  - Engagement: `engagement.{net_flows_ttm,inflows_ttm,outflows_ttm,avg_tenure_days}`
  - Clients table: `clients[] { client_key, client_name, aua }` (navigation to L3)

**L3 Relationship/Client**
- Data source: `gold/clients/{relationship_id}.json` written by `build_client_details()`.
- Implementable sections:
  - Client summary: `headline.total_aua`, `headline.account_count`
  - Accounts table: `accounts[] { account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }`
  - Tax Intelligence: `tax.*` including `cost_basis_by_year[]`, `top_gain_positions[]`
  - Open Lots (taxable only): `tax.open_lots[]`, `tax.open_lots_count`
  - Engagement: `engagement.{net_flows_ttm,avg_relationship_years}`

**L4 Account + Holdings + Tax (inline drill within L3)**
- Implementable as *account-scoped views* using existing L3 payload:
  - Account detail from `accounts[]` row
  - Holdings drill from `tax.open_lots[]` filtered by `account_id`
- Important constraint (must be explicit in brief): lots are **taxable-only** due to `_build_tax()` filtering in advisor-publisher.

This “today” scope is what RD proposed and is consistent with DS’s audit.

---

### 2) Hard gaps vs PRD (must be in the brief as “DS/DT required before implementation”)

These are not UI problems; they are publisher output gaps.

**A) Advisor identity scoping (L2 advisor landing for non-admin) — BLOCKER**
- DS A5 found **no mapping exists** from JWT user → gold advisor slug in `opal-users-v2`.
- Without an `advisorKey` (e.g., `travis_penfield`) on USER#PROFILE, we cannot implement L2 for advisor users securely.
- This must be called out as the gating dependency for “advisor mode” Books.

**B) Relationship performance time series (PRD wants it; not published)**
- `gold/clients/{relationship_id}.json` has no `timeseries` key.
- Data exists in `gold/account_performance.parquet` (already loaded by advisor-publisher) and/or `gold/client_performance.parquet` (not loaded).
- Needs publisher enhancement: add `timeseries` array (date, total_aua, flows) at relationship grain.

**C) Account metadata for L4 (account_name/type/registration/open_date)**
- Client detail `accounts[]` lacks `account_name`, `account_type`, `account_registration_type`, `qualified_flag`.
- Those fields exist in gold layer (accounts dimension / holdings lots), but advisor-publisher doesn’t publish them in `_build_accounts()`.

**D) Holdings “positions list” (not just lots) + weights**
- No `positions[]` anywhere in current JSON.
- We can derive positions by aggregating lots (or other holdings tables), but it is not implemented/published.

**E) Non-taxable lots / holdings**
- Current `open_lots[]` is taxable-only; PRD implies broader holdings visibility.
- Requires changing `_build_tax()` lot filtering and/or publishing separate holdings sections per tax status.

**F) Income/fees + portfolio taxonomy**
- `income_fees` and `portfolio_composition/allocation` are explicitly zero/empty in publisher outputs.
- This is either a true upstream data absence or a future enrichment project; brief should recommend hiding these panels until real data exists.

---

### 3) Design decisions I’m making now (so the brief is unambiguous)

1) **L4 is inline drill-down inside L3** (not a new route) for MVP.  
   Reason: all required data for current L4 (accounts + taxable lots) is already in the L3 payload; routing adds complexity without new information.

2) **Hide (do not stub) Income & Fees and Portfolio Composition** until DS publishes non-zero fields.  
   Reason: current values are literal zeros/empty arrays; showing them harms credibility.

3) **Explicitly label holdings as “Taxable Open Lots”** in UI.  
   Reason: `_build_tax()` filters to taxable; we must not imply full holdings coverage.

---

### 4) What I need from COO/CTO (or DS confirmation) before final brief write-up

To avoid writing a brief that later contradicts policy:

- Confirm the intended **advisorKey mapping plan** (DS recommendation: add `advisorKey` to `opal-users-v2` USER#PROFILE) and whether Books advisor mode is blocked until that’s live.
- Confirm whether “Holdings” in v1 is acceptable as **taxable-only lots**, or whether we must expand to all tax statuses before shipping Books externally.

If those two are confirmed, I can write the final `docs/architecture/advisor_intelligence/books_tab_design_brief.md` with a clean “MVP now” vs “PRD-complete later” split and a precise DS gap list.

---

## 004.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 4
timestamp: 2026-03-04T16:40:02Z
signal: continue
---

Two confirmations + one concrete “next DS work” proposal, all anchored to current publisher functions/keys so DE can write the brief without ambiguity.

## 1) Confirmations requested by DE (from my side)

### 1A) Advisor identity scoping (advisor-mode L2 landing) is a hard blocker
Confirmed. Based on A5 investigation (opal-users-v2 has no `advisorId/advisorName/advisorKey`), we cannot securely scope Books for non-admin advisors until we add a mapping attribute.

**What must exist (minimum viable):**
- Add `advisorKey` (string) to `opal-users-v2` USER#PROFILE items, e.g. `advisorKey: "travis_penfield"`.
- That `advisorKey` must match the advisor slug used by the publisher output path:
  - `bd-portal-advisor-publisher` writes advisor books to `gold/advisors/{adv_id}/book.json` where `adv_id` is produced by `_advisor_id(name)` (snake_case).
  - Portal must request `getAdvisorBook(advisorKey)` and backend must enforce that the caller can only access their own `advisorKey`.

Until that exists, Books can only be “admin/internal” (current `useAuth` gating in `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`).

### 1B) Holdings coverage in v1: taxable-only lots is what we *actually* have today
Confirmed. In `bd-portal-advisor-publisher` client detail generation:
- Lots are loaded in `load_sources()` via `_latest_holdings_lots_key()` and `_load_parquet(lots_key)`.
- Lots are emitted only inside `ClientDetailResponse.tax.open_lots[]`, built in `_build_tax(...)`.
- `_build_tax()` filters to taxable lots only:
  - `taxable_open = lots[is_open==True]` then `taxable_open = taxable_open[taxable_open['tax_status'] == 'taxable']` (when column exists).

So the UI label must be “Taxable Open Lots” unless/until we change `_build_tax()` and/or publish a broader holdings section.

## 2) Publisher audit clarifications DE should encode in the brief (avoid portal/backend mismatch)

### 2A) L3 client detail JSON already contains an account list, but it is “thin”
`_build_accounts(acct_r)` emits per-account snapshot rows with keys:
`account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions`.

It does **not** include `account_name/account_type/account_registration_type/qualified_flag/open_date`. Those live in gold (accounts dimension / holdings lots), but are not published in `accounts[]` today.

### 2B) Relationship performance timeseries is missing, but we can derive it without new gold tables
Even though `gold/clients/{relationship_id}.json` has no `timeseries`, the advisor-publisher already loads `gold/account_performance.parquet` as `acct` (daily account-grain). We can aggregate `acct_r.groupby('date')` to produce a relationship-grain series without loading `gold/client_performance.parquet`.

This is the cleanest DS patch if PRD requires a relationship AUA/flows chart.

## 3) Concrete DS “gap-closing” work items (so the brief can list exact backend changes)

If COO/CTO want PRD-complete Books (beyond the MVP UI), the next DS/DT stream should be explicitly:

### 3A) Enrich client detail `accounts[]` with account metadata
**Where:** `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`  
**Function to change:** `_build_accounts(acct: pd.DataFrame)` and/or `build_client_details(...)`  
**Gold source to load:** `gold/accounts_dimension_latest.parquet` (not currently loaded in advisor-publisher)  
**Fields to add per account row:** `account_name, account_type, account_registration_type, qualified_flag` (and any open-date field if it exists in accounts dimension; not in current context).

### 3B) Add relationship-level timeseries to `gold/clients/{relationship_id}.json`
**Where:** same lambda  
**Function to change:** `build_client_details(...)`  
**Proposed new top-level key:** `timeseries` (array) or `performance_timeseries` (name DE chooses; but must be consistent with portal types)  
**Source:** aggregate `acct_r` (already loaded) by `date`:
- `total_aua = sum(total_aua)`
- `cum_inflows = sum(cum_inflows)`
- `cum_outflows = sum(cum_outflows)`
- `nna = sum(nna)` (or recompute as inflows-outflows)

### 3C) Publish a positions list (non-lot holdings) + weights (optional but PRD-aligned)
**Where:** same lambda, inside client detail response  
**Source:** either:
- aggregate `lots_r` to `(asset_name, ticker)` with `market_value` and compute `weight = market_value / total_taxable_mv`, or
- if we later add a non-taxable holdings source, compute across all tax statuses.

This is currently **absent** from all JSON outputs.

---

## 4) One question back to COO/DE (needed to keep DS changes minimal)
For the v1 Books release target: do we want to treat “relationship timeseries” as:
- **(Option 1)** AUA-only (simpler; fewer fields; less confusion with cumulative flows), or
- **(Option 2)** AUA + cumulative inflows/outflows + NNA (derived from `account_performance` and consistent with existing `cum_*` semantics)?

I can implement either, but the portal type contract should pick one to avoid churn.

If DE confirms (a) advisorKey plan is accepted and (b) taxable-only lots are acceptable for v1, then the design brief can cleanly split:
- “MVP implementable now” (no backend changes)
- “PRD-complete requires DS/DT streams 3A-3C + advisorKey auth workstream”

---

## 005.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 5
timestamp: 2026-03-04T16:40:31Z
signal: continue
---

## RD Turn 5 — Lock UI spec for Books L2/L3/L4 (MVP) + explicitly mark PRD gaps as “backend required”

I’m going to translate DS’s confirmations (turn 4) into **unambiguous UI decisions** DE can encode in the design brief, and I’ll answer DS’s remaining question (timeseries option) from a frontend/UX standpoint.

---

# 1) Confirmed MVP UI decisions (implementable with current publisher outputs)

## 1A) Advisor-mode Books is BLOCKED (identity mapping)
I agree with DS/DE: until `opal-users-v2` has an `advisorKey` that matches `_advisor_id()` output (e.g. `travis_penfield`), Books must remain **admin/internal only**.

**UI implication for the brief:**
- Keep current gating pattern in `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` (`isInternal() || isDev()`).
- Do not design any “advisor landing” UX yet; it will be a follow-on once auth mapping exists.

## 1B) Holdings must be labeled “Taxable Open Lots”
DS confirmed `_build_tax()` filters `tax.open_lots[]` to `tax_status == 'taxable'`. Therefore:

**UI copy must be explicit:**
- Panel title: **“Taxable Open Lots”**
- Helper text (tooltip or subtext): “Lots shown are taxable accounts only (current publisher output).”

No “Holdings” label without qualifier.

## 1C) L4 is inline drill-down inside L3 (no new route)
I recommend we keep L4 as **inline** within the L3 client view:
- Select account row from `clientDetail.accounts[]`
- Filter `clientDetail.tax.open_lots[]` by `account_id`

This is the only L4 we can truthfully deliver today.

---

# 2) L2 / L3 / L4 layout (sections + exact fields)

## L2 — Advisor Book (from `gold/advisors/{advisor_id}/book.json`)
Panels (all use portal primitives: `Panel`, `PanelHeader`, `PanelContent`):

1) **Advisor Book Summary**
- `summary.total_aua`
- `summary.client_count`
- `summary.account_count`
- `nna.mtd`, `nna.qtd`, `nna.ytd`
- `growth.qtd_pct`, `growth.ytd_pct`
- Timestamp: `data_as_of`

2) **Tax Exposure**
- `tax_exposure.taxable`, `taxable_pct`
- `tax_exposure.tax_deferred`, `tax_deferred_pct`
- `tax_exposure.tax_free`, `tax_free_pct`
- `tax_exposure.qualified_aua`, `qualified_pct`
- `tax_exposure.non_qualified_aua`, `non_qualified_pct`
- `tax_exposure.non_qualified_cost_basis`
- `tax_exposure.non_qualified_unrealized_gain`
- `tax_exposure.short_term_gain`, `long_term_gain`

3) **Engagement**
- `engagement.net_flows_ttm`
- `engagement.inflows_ttm`
- `engagement.outflows_ttm`
- `engagement.avg_tenure_days` (display as years)

4) **Clients (Relationships)**
- `clients[]: { client_key, client_name, aua }`
- Row click navigates to L3 by setting selected client.

**Explicitly hide (not stub):**
- `income_fees` (zeroed)
- `portfolio_composition` (empty/zeroed)

## L3 — Client Detail (from `gold/clients/{relationship_id}.json`)
1) **Client Summary**
- `headline.total_aua`
- `headline.account_count`
- Timestamp: `data_as_of`

2) **Accounts**
- `accounts[]: { account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }`
- Row click sets `selectedAccountId` (L4 drill)

3) **Tax Intelligence**
- Tax status split: `tax.taxable`, `tax.taxable_pct`, `tax.tax_deferred`, `tax.tax_deferred_pct`, `tax.tax_free`, `tax.tax_free_pct`
- Qualified/non-qualified: `tax.qualified_aua`, `tax.qualified_pct`, `tax.non_qualified_aua`, `tax.non_qualified_pct`
- Counts (if present in client detail): `tax.qualified_account_count`, `tax.non_qualified_account_count`
- Tables:
  - `tax.cost_basis_by_year[]`
  - `tax.top_gain_positions[]`

4) **Taxable Open Lots**
- `tax.open_lots[]`, `tax.open_lots_count`
- Filters: term (`term`) + account (`account_id`)

5) **Engagement**
- `engagement.net_flows_ttm`
- `engagement.avg_relationship_years`

**Explicitly hide (not stub):**
- `income_fees` (zeroed)
- `portfolio.allocation` (empty)

## L4 — Account drill (inline inside L3)
When `selectedAccountId` is set:

1) **Account Detail (selected row)**
- From the selected `accounts[]` entry:
  - `account_id`, `tax_status`, `total_aua`, `cum_inflows`, `cum_outflows`, `nna`, `num_positions`

2) **Taxable Open Lots (Account-scoped)**
- Filter `tax.open_lots[]` by `account_id === selectedAccountId`

---

# 3) Answer DS question: relationship timeseries option (frontend preference)

DS asked whether relationship timeseries should be AUA-only vs AUA + cumulative flows.

**Frontend recommendation: Option 2 (AUA + cum_inflows + cum_outflows + nna)**, because:
- The client detail already exposes account-level `cum_inflows/cum_outflows/nna` in `accounts[]`, so a relationship-level timeseries with the same semantics is consistent and easier to explain.
- Even if we only chart AUA initially, having flows in the payload enables:
  - tooltips (“flows since start of window”)
  - future “net flows” overlays without another backend change.

**UI guardrail:** default chart should be **AUA-only line/area**; flows can be secondary toggle later.

---

# 4) Component reuse callouts DE should include in the brief

All within `portal/src/pages/AdvisorIntelligence/`:

- Refactor `tabs/ClientsTab.tsx` into smaller internal components (still page-local):
  - `BooksHeaderBar` (advisor picker + client picker + timestamp)
  - `ClientsTable` (reused for L2 clients + L3 accounts)
  - `TaxLotsTable` (reused for L3 all lots + L4 account-scoped lots)
- Use portal panel primitives everywhere (no custom `SubPanel` containers).
- Use existing number formatting utilities already imported in ClientsTab (`formatCurrency`, etc.).

---

# 5) Remaining open items (for DE to mark as “backend required” in the brief)

- Advisor identity mapping (`opal-users-v2` `advisorKey`) + backend enforcement for advisor users.
- Enrich `accounts[]` with account metadata (account_name/type/registration/qualified_flag).
- Relationship-level timeseries key added to client detail JSON.
- Positions list + weights (non-lot holdings) if PRD requires it.
- Non-taxable lots/holdings if PRD requires “full holdings” beyond taxable.

I’m ready for DE to write the brief with the above as the MVP baseline + explicit DS gap list.



---

## 006.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 6
timestamp: 2026-03-04T16:41:00Z
signal: continue
---

Locking the Books MVP scope + converting DS/RD inputs into the exact structure I will write into `docs/architecture/advisor_intelligence/books_tab_design_brief.md` on my final turn.

## 1) MVP scope (implementable with current published JSON — no DS/DT work)

### L2 — Advisor Book (admin/internal only)
**Source:** `GET /api/scoped/advisor-intelligence/advisors/{advisorId}/book.json`  
**S3:** `opal-data-bd/gold/advisors/{advisor_id}/book.json`  
**Producer:** `bd-portal-advisor-publisher` → `build_advisor_books()` → `_advisor_output_key()`

**Panels + field mappings (only non-zero / real fields):**
1) **Advisor Book Summary**
   - `summary.total_aua`, `summary.client_count`, `summary.account_count`
   - `nna.mtd`, `nna.qtd`, `nna.ytd`
   - `growth.qtd_pct`, `growth.ytd_pct`
   - timestamp: `data_as_of`
2) **Tax Exposure**
   - tax status split: `tax_exposure.taxable(_pct)`, `tax_deferred(_pct)`, `tax_free(_pct)`
   - qualified/non-qualified: `qualified_aua(_pct)`, `non_qualified_aua(_pct)`
   - planning fields: `non_qualified_cost_basis`, `non_qualified_unrealized_gain`, `short_term_gain`, `long_term_gain`
3) **Engagement**
   - `engagement.net_flows_ttm`, `inflows_ttm`, `outflows_ttm`, `avg_tenure_days` (display as years)
4) **Clients (Relationships)**
   - `clients[]: { client_key, client_name, aua }` (row click navigates to L3)

**Explicit hide (not stub):**
- `income_fees` (hardcoded zeros in `build_advisor_books()`)
- `portfolio_composition` (empty/zeroed literal)

### L3 — Relationship/Client view
**Source:** `GET /api/scoped/advisor-intelligence/clients/{clientKey}.json`  
**S3:** `opal-data-bd/gold/clients/{relationship_id}.json`  
**Producer:** `bd-portal-advisor-publisher` → `build_client_details()`

**Panels + field mappings:**
1) **Client Summary**
   - `headline.total_aua`, `headline.account_count`, timestamp `data_as_of`
2) **Accounts**
   - `accounts[]: { account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }`
   - row click sets `selectedAccountId` (L4 inline drill)
3) **Tax Intelligence**
   - tax status AUA split: `tax.taxable(_pct)`, `tax_deferred(_pct)`, `tax_free(_pct)`
   - qualified/non-qualified: `tax.qualified_aua(_pct)`, `tax.non_qualified_aua(_pct)`
   - counts if present: `tax.qualified_account_count`, `tax.non_qualified_account_count`
   - tables:
     - `tax.cost_basis_by_year[]`
     - `tax.top_gain_positions[]`
4) **Taxable Open Lots** (must be labeled exactly like this)
   - `tax.open_lots[]`, `tax.open_lots_count`
   - filters: `term`, `account_id`
   - note: taxable-only is enforced in `_build_tax()` (filters `tax_status == 'taxable'`)
5) **Engagement**
   - `engagement.net_flows_ttm`, `engagement.avg_relationship_years`

**Explicit hide (not stub):**
- `income_fees` (zeroed literal)
- `portfolio.allocation` (empty), other portfolio fields that are placeholders

### L4 — Account + holdings drill-down (inline inside L3; no new route)
**Data source:** same L3 payload
1) **Account Detail**
   - selected row from `accounts[]`
2) **Taxable Open Lots (Account-scoped)**
   - filter `tax.open_lots[]` by `account_id === selectedAccountId`

## 2) Hard blockers / backend-required gaps (must be explicit in brief)

### A) Advisor-mode access (non-admin) is blocked on identity mapping
**Finding:** DS A5: `opal-users-v2` has no `advisorKey` / advisor mapping; architects don’t exist as portal users.  
**Requirement for advisor-mode L2:** add `advisorKey` to USER#PROFILE in `opal-users-v2` matching `_advisor_id()` output (e.g., `travis_penfield`), and enforce scoping server-side (portal must not receive cross-advisor data).

### B) Relationship performance time series missing in client detail JSON
`gold/clients/{relationship_id}.json` has no `timeseries`.  
DS proposal is clean: derive from `acct_r` (already loaded from `gold/account_performance.parquet`) by `groupby('date')` and publish **Option 2** payload (AUA + `cum_inflows` + `cum_outflows` + `nna`) so frontend can chart AUA now and use flows later.

### C) Account metadata missing in `accounts[]`
Need `account_name`, `account_type`, `account_registration_type`, `qualified_flag` (and open date if available) by loading `gold/accounts_dimension_latest.parquet` and enriching `_build_accounts()` output.

### D) Holdings “positions list” + weights absent
No `positions[]` anywhere. If PRD requires it, publisher must aggregate holdings (likely from `lots_r` initially) into position rows with weights.

### E) Non-taxable holdings/lots absent
Current lots are taxable-only. If PRD requires “full holdings,” `_build_tax()` filtering must change and/or a new holdings section must be published.

### F) Income/fees + portfolio taxonomy are true placeholders
Currently hardcoded zeros/empty arrays in publisher output; brief will recommend hiding until a real upstream source exists.

## 3) One last confirmation I need from COO/CTO (to avoid rework)
For v1 external advisor rollout, is it acceptable that “Holdings” is **taxable open lots only** (explicitly labeled), with “full holdings across all tax statuses” deferred?  
- If **yes**: MVP stands; DS gap list focuses on identity mapping + timeseries + account metadata.
- If **no**: we must treat expanding holdings coverage as a release blocker and add a DS/DT stream to change `_build_tax()` and/or publish a broader holdings structure.

Once I have that, my final turn will be the actual brief file content (L2/L3/L4 layouts + component reuse + explicit DS gap list + TypeScript interface additions).

---

## 007.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 7
timestamp: 2026-03-04T16:41:26Z
signal: converge
---

Two final inputs for the design brief (so DE can write it without any “implied” data), plus my recommendation on the COO/CTO open question.

## 1) “What exists” recap — anchor points DE should cite verbatim

### L2 advisor book JSON (per-advisor)
- **Written by:** `bd-portal-advisor-publisher` (`infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`)
- **Function:** `build_advisor_books(acct, tax, cdim, today)`
- **S3 key:** `gold/advisors/{advisor_id}/book.json` via `_advisor_output_key(adv_id)`
- **Holdings/positions:** **none** (no `positions[]`, no `holdings[]`)
- **Income/fees + portfolio taxonomy:** present as keys but **literal zeros/empty** in `build_advisor_books()` (`income_fees` hardcoded zeros; `portfolio_composition.asset_allocation=[]`)

### L3 client detail JSON (relationship/household)
- **Written by:** same lambda
- **Function:** `build_client_details(acct, tax, lots, cdim, today)`
- **S3 key:** `gold/clients/{relationship_id}.json` via `_save_json(response, f'gold/clients/{rel_id_str}.json')`
- **Top-level keys:** `headline`, `tax`, `income_fees` (zeroed), `portfolio` (mostly empty), `engagement`, `accounts`
- **Lots are only published here:** under `tax.open_lots[]` built in `_build_tax(...)`

### L4 “holdings” reality today
- **Lots source:** latest `gold/holdings_lots/YYYY-MM-DD.parquet` loaded by `_latest_holdings_lots_key()` in `load_sources()`
- **Lots emission point:** `_build_tax()` creates `open_lots[]`
- **Critical constraint:** `_build_tax()` filters to taxable only:
  - `taxable_open = taxable_open[taxable_open['tax_status'] == 'taxable']` (when column exists)
- Therefore any UI must label this as **Taxable Open Lots**, not generic “Holdings”.

## 2) Backend gap list — exact DS/DT work items (file + function targets)

If/when we move beyond MVP, these are the minimal publisher changes (all in `bd-portal-advisor-publisher/lambda_function.py`):

1) **Relationship performance timeseries (PRD asks for it)**
   - **Target:** `build_client_details(...)`
   - **Source:** aggregate `acct_r` (already loaded from `gold/account_performance.parquet`) by `date`
   - **Recommended payload (RD preference):** AUA + `cum_inflows` + `cum_outflows` + `nna` (Option 2)

2) **Enrich `accounts[]` with account metadata**
   - **Target:** `_build_accounts(acct: pd.DataFrame)`
   - **New gold load needed:** `gold/accounts_dimension_latest.parquet`
   - **Fields to add:** `account_name`, `account_type`, `account_registration_type`, `qualified_flag` (open date only if it exists in accounts dimension; not evidenced in current context)

3) **Positions list + weights (optional, PRD-aligned)**
   - **Target:** `build_client_details(...)` (new `positions[]` section)
   - **Source:** aggregate `lots_r` to `(asset_name, ticker)` with `market_value`, compute `weight`
   - Note: initially would be taxable-only unless we expand holdings coverage.

## 3) COO/CTO open question — my recommendation (for v1 external advisor rollout)

**Recommendation:** accept “Holdings” as **taxable open lots only** for v1, with explicit labeling, and defer “full holdings across all tax statuses” to a follow-on stream.

Reason (source-grounded): the only holdings-like structure currently published is `tax.open_lots[]`, and it is taxable-filtered in `_build_tax()`. Expanding to all tax statuses is not a small UI tweak; it is a contract change (and potentially a payload size/perf issue) that should be scheduled intentionally.

This lets Books ship sooner once the true blocker is resolved:
- **Advisor identity mapping** (A5): add `advisorKey` to `opal-users-v2` USER#PROFILE matching `_advisor_id()` output, and enforce server-side scoping.

That’s all from DS; DE has enough to write the brief with a clean MVP vs “backend required” split.

---

## 008.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 8
timestamp: 2026-03-04T16:42:17Z
signal: converge
---

## RD final input — Books tab L2/L3/L4 MVP UI spec (field-accurate) + brief-ready “do/don’t” list

This is my last pass to ensure the design brief is implementable with **only** DS-confirmed publisher outputs, and that we don’t accidentally imply PRD-complete holdings/fees/portfolio data.

### 1) MVP layout decisions (brief should treat as binding)

**A) Access model (MVP)**
- Books remains **admin/internal only** until identity mapping exists.
- Gating stays as-is in `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` using `useAuth()` (`isInternal() || isDev()`).
- No “advisor landing” UX in MVP (blocked on `opal-users-v2` `advisorKey` mapping per DS A5).

**B) L4 is inline drill-down inside L3**
- No new route. L4 is driven by local state:
  - `selectedAccountId` from `clientDetail.accounts[]`
  - lots filtered from `clientDetail.tax.open_lots[]`

**C) Holdings labeling**
- Any holdings panel must be titled **“Taxable Open Lots”** (not “Holdings”), because `_build_tax()` filters `tax.open_lots[]` to `tax_status == 'taxable'` in `bd-portal-advisor-publisher`.

**D) Hide placeholders**
- Do **not** render panels for:
  - `income_fees` (literal zeros in both advisor book + client detail)
  - `portfolio_composition` / `portfolio.allocation` (empty/placeholder)
- Brief should explicitly say “hidden until non-zero data is published” (not stubbed).

---

### 2) L2 / L3 / L4 sections with exact field mappings (copy/paste into brief)

#### L2 — Advisor Book (AdvisorBookResponse)
Source: `GET /api/scoped/advisor-intelligence/advisors/{advisorId}/book.json`  
S3: `opal-data-bd/gold/advisors/{advisor_id}/book.json`

Panels:
1) **Advisor Book Summary**
- `summary.total_aua`, `summary.client_count`, `summary.account_count`
- `nna.mtd`, `nna.qtd`, `nna.ytd`
- `growth.qtd_pct`, `growth.ytd_pct`
- timestamp: `data_as_of`

2) **Tax Exposure**
- `tax_exposure.taxable`, `taxable_pct`
- `tax_exposure.tax_deferred`, `tax_deferred_pct`
- `tax_exposure.tax_free`, `tax_free_pct`
- `tax_exposure.qualified_aua`, `qualified_pct`
- `tax_exposure.non_qualified_aua`, `non_qualified_pct`
- `tax_exposure.non_qualified_cost_basis`
- `tax_exposure.non_qualified_unrealized_gain`
- `tax_exposure.short_term_gain`, `long_term_gain`

3) **Engagement**
- `engagement.net_flows_ttm`, `inflows_ttm`, `outflows_ttm`
- `engagement.avg_tenure_days` (display as years)

4) **Clients (Relationships)**
- `clients[]: { client_key, client_name, aua }` (row click -> L3)

#### L3 — Client Detail (ClientDetailResponse)
Source: `GET /api/scoped/advisor-intelligence/clients/{clientKey}.json`  
S3: `opal-data-bd/gold/clients/{relationship_id}.json`

Panels:
1) **Client Summary**
- `headline.total_aua`, `headline.account_count`
- timestamp: `data_as_of`

2) **Accounts**
- `accounts[]: { account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions }`
- row click sets `selectedAccountId` (L4)

3) **Tax Intelligence**
- `tax.taxable`, `taxable_pct`, `tax.tax_deferred`, `tax_deferred_pct`, `tax.tax_free`, `tax_free_pct`
- `tax.qualified_aua`, `qualified_pct`, `tax.non_qualified_aua`, `non_qualified_pct`
- counts if present: `tax.qualified_account_count`, `tax.non_qualified_account_count`
- tables:
  - `tax.cost_basis_by_year[]`
  - `tax.top_gain_positions[]`

4) **Taxable Open Lots**
- `tax.open_lots[]`, `tax.open_lots_count`
- filters: `term`, `account_id`

5) **Engagement**
- `engagement.net_flows_ttm`, `engagement.avg_relationship_years`

#### L4 — Account drill (inline inside L3)
1) **Account Detail**
- selected `accounts[]` row: `account_id`, `tax_status`, `total_aua`, `cum_inflows`, `cum_outflows`, `nna`, `num_positions`

2) **Taxable Open Lots (Account-scoped)**
- filter `tax.open_lots[]` by `account_id === selectedAccountId`

---

### 3) Backend-required items (brief should list as “cannot implement until published”)

1) Advisor-mode scoping: `opal-users-v2` needs `advisorKey` matching `_advisor_id()` output; backend must enforce scoping.
2) Relationship performance timeseries: add a new key to `gold/clients/{relationship_id}.json` (RD preference: include AUA + `cum_inflows` + `cum_outflows` + `nna`, but chart AUA by default).
3) Enrich `accounts[]` with account metadata (`account_name`, `account_type`, `account_registration_type`, `qualified_flag`) — currently absent.
4) Positions list + weights (non-lot holdings) — currently absent.
5) Non-taxable holdings/lots — currently absent; taxable-only lots are acceptable for MVP if explicitly labeled.

That’s all — DE should now be able to write the brief with a clean MVP vs PRD-complete split and no phantom fields.

---
