# NFRA_MCPINDEX -- advisor tables per vendor: where the client_* tools really stand

- Author: 4.0.0_SA_CRO~Y (read-only research brief). Asked by: 1.0.0_SA_CTO~Z, ferried by 0.0.0_AB_MSTR~Z, 2026-10-20 17:12Z.
- Andrew-direct record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261020_16xxZ_MCPORTAL_ENTITLEMENT_EDITING_AND_MCPINDEX_VENDOR_TABLE_LINKING.md` @790786dcfc.
- Code read at workspace HEAD `95be18f23d6` (box/sitez); the adapters last changed at `2d2a56cb04a`. All S3 reads 2026-10-20 ~17:20-17:45Z.
- Evidence beside this file: `census.json` (139 tables, live S3), `census.py`, `colcheck.py`, `probe.py`.
- Calendar: today is Tue 2026-10-20, so the T-1 frontier is Mon 2026-10-19.

## 0. The answer in five lines

1. **Vendor naming is honored.** Each adapter reads its vendor's own column names: Orion camelCase, Black Diamond Cottonwood
   `"Space Names"`, Black Diamond 49F snake_case, Schwab file-native, Commonwealth `Mixed_Case`. **30 of 30** (adapter, table)
   reads ask only for columns that exist in the live newest partition. No adapter assumes a common shape. The concern Andrew
   raised is not the defect class here.
2. **Served state does not match the code.** The live gateway answers `client_resolve_account(firm="inflection")` with
   **`firm_not_served`**, so Orion and Eclipse are dark in production even though HEAD has both adapters wired. The live 49F
   resolve also omits the Schwab refusal that HEAD's core would add (section 3).
3. **Three tools are built but cannot be reached:** Schwab (no resolve, and nothing else mints its ref), Eclipse allocation
   (no tool passes `model`), and Eclipse's account path (it ignores the account-to-model bridge that does exist).
4. **Three answers are stale or wrong for real data:** the 49F resolve bridge is 15 trading days old and misses **2,362 of
   8,032** live 49F accounts; Orion transactions name the custodian under a column the adapter does not read; Commonwealth says
   it has no fee source while its transactions hold 1,683 Management Fee rows.
5. **Every currency field is a dead read.** No vendor table carries a `currency` column (0 of 139 live schemas). All seven
   adapters therefore serve `currency_basis: source_absent`. That is honest, but nothing is being read.

## 1. Domain: vendors, firms, tables (denominator first)

Vendor prefixes on live S3: `opal-data-assets/{blackdiamond,commonwealth,eclipse,orion,schwab,smartx}/`, the live Black
Diamond tables at `opal-data-bd/silver/`, and the Orion/Eclipse producer output at `opal-data-inf/silver/`. The per-firm
buckets (`opal-data-49financial`, `-cottonwood`, `-inflection`) hold only `irpt/`, `mdpf/`, `advi/` and `schwab/.../state/`,
with no vendor silver. `pathfinder/` and `trueshares/` are Opal-issued funds, not advisors. That leaves **6 vendors over 3
firms**: no other advisor vendor exists in S3.

| Vendor | Firm (fence) | Catalogued silver tables | Adapter | Tables the adapter reads |
|---|---|---|---|---|
| Orion | inflection (segment `inflection`) | 5 (+1 `orion/4698` one-shot) | `client_adapter_orion.py` | fact_positions, fact_transactions |
| Eclipse | inflection | 4 | `client_adapter_eclipse.py` | orion fact_positions (resolve), fact_models, fact_model_composition |
| SmartX | 49financial (row filter by advisor_name) | 13 | `client_adapter_smartx.py` | 5 fact_* (roster, account_map, positions, valuation, model_holdings) |
| Schwab | 49financial (all 3 masters) | 57 (19 x 3 masters) | `client_adapter_schwab.py` | dim_position, dim_balance, dim_transaction |
| Black Diamond 49F | 49financial (segment `49f`, id prefix z08) | 4 live (opal-data-bd) + 15 under `blackdiamond/49f|49financial` | `client_adapter_bd49f.py` | dim_account_xref, live unrealized/transactions/fees/allocations, fact_bd_allocation |
| Black Diamond Cottonwood | cottonwood (segment `cottonwood`, id prefix z09) | 14 | `client_adapter_bdcottonwood.py` | fact_allocations, fact_holdings, fact_transactions, 4 model tables |
| Commonwealth | cottonwood | 12 | `client_adapter_commonwealth.py` | crosswalk, positions, account_day_value, transactions |

Catalog denominator: `app/refs/DATA_CATALOG.yaml` holds 268 servable silver rows, 124 of them vendor rows. The census adds
15 live production tables with no catalog row (section 6).

## 2. Verdict grid (tool x vendor), at HEAD

BUILT-OK = reads the right table and real columns and answers. STALE = right table, old data. WRONG = answers, but part of
the answer is wrong. UNREACHABLE = built, but no served call can reach it. MISSING = a source exists and is not read.
REFUSED-OK = the refusal is correct because no source exists.

| Tool | Orion | Eclipse | SmartX | Schwab | BD 49F | BD Cottonwood | Commonwealth |
|---|---|---|---|---|---|---|---|
| resolve_account | BUILT-OK* | WRONG (duplicate of Orion) | BUILT-OK | UNREACHABLE (refuses) | STALE (29% unresolvable) | BUILT-OK (EXERCISED live) | BUILT-OK |
| get_holdings | BUILT-OK* | REFUSED-OK | BUILT-OK | UNREACHABLE | BUILT-OK (lot grain) | BUILT-OK | BUILT-OK (closed 2026-06-23) |
| get_transactions | WRONG (platform) | REFUSED-OK | REFUSED-OK | UNREACHABLE | BUILT-OK | BUILT-OK | BUILT-OK (closed) |
| get_allocation | BUILT-OK (derived) | UNREACHABLE + MISSING bridge | BUILT-OK | UNREACHABLE | STALE profile (2026-08-18) | WRONG label on placeholder (EXERCISED live) | REFUSED-OK |
| get_fees | WRONG (platform; Fee Credit summed) | REFUSED-OK | REFUSED-OK | REFUSED-OK (1 partition seen) | BUILT-OK | BUILT-OK | MISSING (fee rows exist) |

`*` Orion and Eclipse are BUILT at HEAD but **dark in production**: the live call returns `firm_not_served` (section 3).

## 3. The served-versus-code gap (highest stakes)

Exercised 2026-10-20 ~17:45Z through the live `opalgateway` MCP, as an Opal principal:

- `client_resolve_account(firm="inflection", account_last4="0854")` returned `absent_reason: firm_not_served` with
  `source_keys: []`. The last-4 was taken from row 100 of `orion/inflection/silver/fact_positions/date=2026-10-20`, so an
  account with those digits exists.
- At HEAD this cannot happen through the code path read. `client_core.py:194-198` gives orion and eclipse the
  `("segment","inflection")` fence. `client_core.py:403-407` names the segment only when the catalog carries an
  `orion/inflection/silver` row, and the repo catalog carries five. Of the two ways to reach `firm_not_served`, the one that
  fits is `client_adapter_orion.py:66-70` / `client_adapter_eclipse.py:67-71`: `_segments` raises it when `firm_segments`
  comes back empty. That points to a **deployed catalog or fence that lacks the inflection rows**. In support,
  `opal_describe("orion/inflection/silver/fact_positions/")` answered `catalogued: false`. That support is weak, because
  describe may key on an id rather than a prefix.
- `client_resolve_account(firm="49financial", account_last4="0322")` returned the BD 49F and SmartX candidates and **no
  `refusals` key**. At HEAD, `client_core.py:591-592` would add `{"vendor":"schwab","code":"no_resolve_source"}`. Either the
  deployed core predates OG-fc-1 or Schwab is not registered there.
- `client_resolve_account(firm="cottonwood", "8667")` and `client_get_allocation` on its ref answered as HEAD predicts. Those
  two paths match the code.

**Not measured:** the deployed bytes. I did not compare the EC2 build input to HEAD (rule 22a). The owner should diff the
running `app/` and `refs/DATA_CATALOG.yaml` against `95be18f23d6` before treating any HEAD fix as live. **Owner: COO~MI's
deploy lane / CloudOps.**

## 4. Per vendor: tables, columns, freshness, findings

Freshness = newest partition vs T-1 (2026-10-19). Every listed column was checked against the newest partition's live
schema (`colcheck.py`; "used-not-requested" = read with `row.get` but never requested).

### 4.1 Orion (inflection) -- `opal-data-assets/orion/inflection/silver/`

| Table | Partitions | Newest | Rows (newest) | Cols | Size | Read by |
|---|---|---|---|---|---|---|
| fact_positions | 2,368 (2020-04-24..) | 2026-10-20 | 37,026 | 64 | 1.2 MiB | resolve, holdings, allocation (+ eclipse resolve) |
| fact_transactions | 159 (2026-05-12..) | 2026-10-20 | 1,526,116 | 36 | 32.6 MiB | transactions, fees |
| fact_assets | 2,367 | 2026-10-20 | 37,026 | 63 | -- | not read (a duplicate, by design) |
| fact_performance | 162 | 2026-10-20 | 484,861 | 9 | -- | not read |

Columns: positions 14/14 requested present (`accountNumber, accountId, custodian, ticker, ... sleeveType`); transactions
10/10 present.

- **WRONG -- custodian column name.** `fact_transactions` names the custodian `custodianName`. `fact_positions` names it
  `custodian`. `client_adapter_orion.py:27` (TX_COLUMNS) requests neither, yet `:205-207` filters and `:129-130` labels on
  `custodian`. The effect: `get_transactions` / `get_fees` with any `platform` always refuse `platform_not_source_label`, and
  the envelope `platform_label` is always null (`:323-325`, `:374-376`). Live values are `Fidelity_Inflection` (1,525,856
  rows) and `Fidelity_LH` (260). Fix: request `custodianName` and read it in `_labels` / the filter for the tx path.
- **WRONG (judgment) -- fee rule.** `:361` keeps any `transactionDescription` containing "fee". The newest partition holds
  Management Fee 21,300, **Fee Credit 884**, ADR Fee 77, Administrative Fee 20, Administrative Fee Adjustment 14 and Wire
  Fee 7. `:370` sums them signed as stored, so credits and adjustments land in `total_in_window`. Whether that is right
  depends on the sign convention, which is not measured. Only Complete rows count (1,341,555 of 1,526,116).
- **OK with headroom risk -- size.** Every tx call loads the whole 32.6 MiB partition and filters 1.5M rows in Python
  (`:199-201`). That is 51% of the 64 MiB object cap (`harvest_typed.py:24`). `TypedOverCap` carries no `.code`
  (`harvest_typed.py:32`), so past the cap `client_core.py:532-535` re-raises: a crash, not an enveloped refusal.
- `weight_pct` is passed through with `weight_unit: None` (`:284-286`). That is honest: the scale is unverified.
- Not read: Orion carries a billing feed (`opal-data-inf/orion/rate_limit_state_billing.json`), but no billing silver
  exists. So a fee TABLE is MISSING upstream, not in the adapter.

### 4.2 Eclipse (inflection) -- `opal-data-assets/eclipse/inflection/silver/`

| Table | Partitions | Newest | Rows | Cols | Read by |
|---|---|---|---|---|---|
| fact_models | 141 | **2026-10-17** | 18 | 37 | allocation (model path) |
| fact_model_composition | 141 | 2026-10-17 | 9 | 61 | allocation (model path) |
| fact_portfolios_simple | 141 | 2026-10-17 | 846 | 28 | **not read** |
| fact_portfolios_full | 141 | 2026-10-17 | 863 | 62 | not read |

- **STALE by 1 trading day.** The producer's own output `opal-data-inf/silver/eclipse/` has 2026-10-20; the catalogued copy
  stops at 2026-10-17 and is missing 2026-10-19.
- **UNREACHABLE -- allocation.** `client_adapter_eclipse.py:214-220` answers only when `model` is passed. Neither
  `tools.py:1653-1655` nor `client_core.py:546` / `:617-618` passes it, so through the tool every Eclipse allocation is
  `account_not_resolved`.
- **MISSING -- the account-to-model bridge exists.** `fact_portfolios_simple` carries `accountId`, `accountNumber`,
  `custodialAccountNumber` and `modelId`, which is exactly the bridge the module docstring (`:14-16`) says is "not read under
  the contract". Reading it would let `get_allocation(account)` resolve the account to its `modelId`, then reach the existing
  `_model_allocation` (`:223`). This is a contract change and needs a CTO ruling, not an adapter tweak.
- **WRONG -- duplicate resolve.** `:151` resolves through the same Orion `fact_positions` partition that Orion's resolve reads,
  so every Inflection last-4 comes back as two candidates (orion and eclipse) for one account. The eclipse candidate leads
  only to refusals (`:199-211`).
- Targets stop at the security-set level (`:265`). That is correct: no ticker weights exist in composition.

### 4.3 SmartX (49financial, row filter) -- `opal-data-assets/smartx/platform/silver/`

Newest partition 2026-10-20 for every table read, all under 3.2 MiB. Columns: every field the adapter reads with `row.get`
exists (roster 8/8, account_map 3/3, valuation 2/2, model_holdings 3/3, positions 5/6, with only `currency` absent).

- **BUILT-OK -- fence.** `fact_model_allocation_roster` has 10,317 rows and 4 distinct `advisor_name`. Mapped through
  `refs/partner_roster.json` (3 names), **10,242 rows are 49financial and 75 are unmapped and dropped** (counted in
  `unknown_name_rows`, `client_adapter_smartx.py:142-147`). EXERCISED: the live 49F resolve returned a SmartX candidate with 2
  allocations.
- REFUSED-OK: transactions (`:325-331`) and fees (`:390-396`). No transaction or fee table exists among the 13.
- Custodian label "Schwab" is a constant (`:36-38`), claimed `inferred`. That is honest.
- Note: `fact_account_allocations`, `fact_account_detail` and `fact_nonzerosleeve` have 0 rows in their newest partition.
  None is read.

### 4.4 Schwab (49financial, masters 08242234 / 08335338 / 08403355) -- `opal-data-assets/schwab/<master>/silver/`

Fresh: dim_position, dim_balance and dim_transaction are newest at 2026-10-19 = T-1 on all three masters. Columns 8/8, 5/5
and 12/12 present (`account_id, market_value_settled_unsettled, ...`); `currency` is absent.

- **UNREACHABLE -- the whole vendor.** `resolve_account` always refuses `no_resolve_source` (`client_adapter_schwab.py:278-284`).
  The only Schwab ref minter, `mint_account_ref` (`:164-166`), is called **nowhere** in `app/`. So no served call can obtain a
  Schwab account_ref, and `get_holdings` / `get_transactions` / `get_allocation` (`:287-372`) are built but unreachable. To
  make it reachable, build the `dim_account` projection the docstring names (`:7-8`) or grant a masked read of `fact_acc`.
  That is a data-grant decision (fact_acc is PII).
- Master 08403355 (30 accounts in dim_balance) is refused `master_not_registered` (`:36`, `:155-156`), as ruled (A2 S4).
- REFUSED-OK (partly): fees `no_fee_source` (`:375-380`). One `dim_transaction` partition (08242234, 2026-10-19, 1,178
  rows) carries no fee category: Trades 833, Deposits and Withdrawals 190, Security Transfers 107, Electronic Transfers 31,
  OTHER 11. Not swept: the window, and `fact_trn` (140 columns), which may carry fee codes. That is a population this brief
  did not measure.

### 4.5 Black Diamond 49F (49financial, z08) -- `opal-data-bd/silver/` (live) + `opal-data-assets/blackdiamond/49f/silver/`

| Table | Newest | Rows | Read by | State |
|---|---|---|---|---|
| 49f/silver/dim_account_xref | **2026-09-28** | 6,202 | resolve | STALE 15 td (live call `freshness_td: 15`) |
| opal-data-bd silver/unrealized | 2026-10-16 | 114,064 | holdings | weekly; fresh for its cadence |
| silver/transactions | 2026-10-20 (0 rows) | -- | transactions | increment; fresh |
| silver/fees | 2026-10-16 | 3,638 | fees | fresh |
| silver/allocations | 2026-10-16 | 7,394 | allocation weights | fresh |
| 49f/silver/fact_bd_allocation | **2026-08-18 (1 partition)** | 30,577 | allocation profile | STALE, one-shot |

Columns: 3/3, 9/9, 9/9, 8/8, 8/8 and 8/8 present; `currency` is used but absent on three tables.

- **STALE -- the resolve bridge.** The live unrealized partition holds **8,032 distinct z08 accounts; 2,362 (29.4%) are not in
  the 2026-09-28 `dim_account_xref`**. Those accounts get `no_candidate_for_last4` from resolve
  (`client_adapter_bd49f.py:474-485`), so every other tool is unreachable for them. Fence check: all 114,064 unrealized rows
  are z08, so the fence excludes nothing there. Fix: restore the xref producer's cadence. The **producer** is the owner, not
  the adapter.
- **STALE -- the profile.** `fact_bd_allocation` has one partition, 2026-08-18 (`:642-645`). Any `as_of` before it answers
  `no_partition_at_as_of` for the whole allocation, weights included, because `:644` requires both.
- Holdings are tax lots, not positions (`:551`), with quantity absent (`:537-538`). The answer says so; that is correct.

### 4.6 Black Diamond Cottonwood (cottonwood, z09) -- `opal-data-assets/blackdiamond/cottonwood/silver/`

Fresh: fact_allocations and fact_holdings are newest at 2026-10-19; fact_transactions and the model tables at 2026-10-20.
Columns: alloc 3/3, holdings 9/9 (currency absent), tx 12/12, assignment 11/11, roster 4/4, definition 7/7, blend 5/5, all
as `"Space Names"` / mixed case, matching the source.

- EXERCISED live: resolve "8667" gave one candidate (Custodian `Fidelity IWS`, measured), and allocation answered with
  `freshness_td: 0`.
- Join check: assignment `account_number` joins fact_allocations `Account Number` on **852 of 853** accounts.
- **WRONG (label only).** Of 998 assignment rows, 484 strategies join the roster and **all 514 misses are the placeholder
  `"--"`** (0 real join misses). `client_adapter_bdcottonwood.py:487-488` reports them as `model_not_in_roster`, and returns a
  `model_assignment` whose `model_key` is `"--"`. They are accounts with **no model**, which should read
  `no_model_assignment`. EXERCISED: the live answer for the sampled z09 account shows `model_key: "--"`, `absent_reason:
  model_not_in_roster`. The join itself is correct.
- `_s2` twins are xlsx headers and are correctly not read.

### 4.7 Commonwealth (cottonwood) -- `opal-data-assets/commonwealth/cottonwood/silver/`

Closed delivery: every table has one partition, 2026-06-23. The adapter states this (`client_adapter_commonwealth.py:6-7`).
Columns: crosswalk 3/3, positions 7/7, account_day_value 7/7, transactions 11/11 present (`Account_Number, Trade_Date, ...`).

- **MISSING -- fees.** `get_fees` refuses `no_fee_source` (`:310-316`). The transactions table holds Transaction_Type `man`
  on 1,683 rows (description Management Fee), plus General Maintenance Fee 88, Withdraw ManAlt Fee payment 40, Management
  Fee paid by Alt account 40, Consulting Fee Expense 34 and Management Fee paid by check 10. A fee answer is derivable from a
  table the adapter already reads (`:266-271`). This is a contract change.
- REFUSED-OK: allocation (`:302-307`). No allocation table exists among the 12.
- Size: account_day_value is 52.2 MiB of the 64 MiB cap (82%). It is read with an `account` filter (`:220`), which streams.
  It is a closed delivery, so it will not grow.

## 5. Cross-vendor: currency

`_currency_keys` reads `row.get("currency")` in all seven adapters (e.g. `client_adapter_orion.py:118-122`,
`client_adapter_bd49f.py:198-202`), but no adapter requests the column, and **0 of 139 live schemas carry a `currency`,
`ccy` or FX column**. Every answer therefore carries `currency: null, currency_basis: source_absent`. That is correct by
honesty (OG-en-4 forbids a USD default), but the field is a constant. If a currency is ever wanted, it has to come from a
reference join (security master), not from these tables.

## 6. Live tables with no catalog row (the gateway cannot see them)

`opal-data-inf/silver/`: `accounts_dim` (835 rows), `api_dims`, `assets_v2` (2,367 partitions, 59 cols), `eclipse/` (to
2026-10-20), `orion-rest/transactions` and `orion-rest/performance_weekly`, `performance`, `performance_dim`, `prices` and
`transactions`. That last one has 1,663 partitions and 49 cols, adding `rep_id`, `repName`, `advisor_firm`, `activityCategory`
and `trans_type_desc` to the catalogued copy. `opal-data-bd/silver/`: `assets`, `prices`, `realized` (to 2026-10-20) and
`transactions_enriched`. None is needed for the five tools as contracted. `opal-data-inf/silver/transactions` is the only
one that carries rep/advisor attribution for Orion.

## 7. What must be built or modified (ranked by blast radius)

| # | Act | Owner (disarm / specify / write) | Class |
|---|---|---|---|
| 1 | Diff the deployed gateway `app/` + `refs/DATA_CATALOG.yaml` against HEAD; restore Inflection serving (`firm_not_served`) | COO~MI / CTO~Z / CloudOps lane | SERVED |
| 2 | Restore the 49F `dim_account_xref` producer cadence (15 td stale; 2,362 accounts unresolvable) | xref producer owner / CTO~Z / producer lane | SERVED |
| 3 | Orion tx: read `custodianName` (TX_COLUMNS `:27`, filter `:205-207`, labels `:129-130`) | COO~MI / -- / worker | LOCAL |
| 4 | Cottonwood: `"--"` strategy answers `no_model_assignment`, not `model_not_in_roster` (`:487-488`) | COO~MI / -- / worker | LOCAL |
| 5 | Eclipse: pass `model` through the tool or read `fact_portfolios_simple.modelId` for the account path; drop the duplicate resolve candidate | CTO~Z ruling (contract) / COO~MI | LOCAL |
| 6 | Schwab: a resolve source (`dim_account` projection or a masked `fact_acc` grant) so a ref can be minted | CTO~Z + data-grant decision | SERVED |
| 7 | Commonwealth fees from `transactions` (`man` and fee descriptions) | CTO~Z ruling (contract) / COO~MI | LOCAL |
| 8 | Eclipse catalogued copy 1 td behind its producer: name the copier and its schedule | producer owner | SERVED |
| 9 | Orion fee rule: rule on Fee Credit / Adjustment inclusion and the sign | CTO~Z | LOCAL |
| 10 | Make `TypedOverCap` an enveloped refusal (no `.code` today, so a crash at `client_core.py:533-535`) | COO~MI | LOCAL |

## 8. Method, and what this brief does NOT claim

- Census: every catalog vendor row (124) plus 15 live extras, listed in full through the paginator. The newest-partition
  schema was read from the parquet footer. One value probe was run per finding (`probe.py`). Four live tool calls were made
  (inflection resolve, 49F resolve, Cottonwood resolve, Cottonwood allocation).
- Not claimed: anything about the deployed gateway bytes (section 3); partitions other than the newest, except where a count
  says so; the Schwab fee population over a window or in `fact_trn`; the Orion fee sign convention; and per-account
  correctness beyond the counts printed.
- The Cottonwood roster figure (514 misses) was first read as a join failure. Splitting it showed all 514 are the
  placeholder, which is why section 4.6 calls the join correct and the label wrong.
