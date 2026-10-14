# G2 client tools contract -- the five core `client_*` tools (OG-cl-0, design only, revised to A2)

Read-only design of the five core client-data tools for FWD-22 G2. No code, no IAM, nothing applied. Source rulings: PRD v3.1 Rulings 1-5 and v3.2 (`org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md`, sections "v3.1 addendum" and "v3.2 addendum"); the G2 census (`org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/GATEWAY_DATA_CONTRACTS_20261014/G2_assets_silver.md`, sections 1 and 2 and the per-vendor parts a-e); and the A2 ruling, Andrew-direct via CTO msg 34134 (record @9a314c1e98), which supersedes the CTO msg 34130 ruling.

Role names and grants are measured in `G2_ROLES.json` in this folder; new role names come from `lib/opal_naming.py`.

**Served keys.** The census headings write each table as a logical id (for example `opal-data-assets/silver/orion/inflection/fact_positions`). This contract names the served S3 prefix, `opal-data-assets/<vendor>/<firm>/silver/<table>/`, which is the key form the IAM grants and the prefix census use. The census id is given in parentheses where it differs in form.

## Shared envelope

Every answer from every client tool carries one envelope:

- `as_of`: the requested date, and `partition_date`: the newest partition at or before it that the answer reads.
- `source_keys`: the S3 keys read (masked to the table and partition; never an account number).
- `denominator`: the row count of the one partition read, and the count of candidates where a list is returned. Snapshot tables are never summed across partitions.
- `absent_reason`: null when an answer is returned; otherwise one of the refusal codes named under each tool.
- `platform_label`: the source's own label, unchanged. `platform_label_source`: the column or constant the label came from (for example `Custodian`, `mngdacct_pltfrmcd`, or `constant:smartx`).
- `label_claim`: `measured` when read per row, `inferred` when derived from the producer or the key segment (for example SmartX custodian Schwab, inferred from master 08242234 and not measured per row).
- `freshness_td`: lag of `partition_date` behind the T-1 frontier, in trading days (`lib/trading_calendar.py`, `trading_days_behind`). Every answer states it.

Firm input: one of `49financial`, `cottonwood`, `inflection`. Aliases resolve to these and nothing else: `49f` to `49financial`; `orion/4698` and `4698` to `inflection`. Any other value is refused with `absent_reason` `firm_not_canonical`.

## Firm fence kinds by vendor

- Key-segment (IAM and path): Black Diamond 49F (`opal-data-assets/blackdiamond/49f/silver/`, account prefix `z08`); Black Diamond Cottonwood (`blackdiamond/cottonwood/silver/`, account prefix `z09`); Orion and Eclipse (`orion/inflection/`, `eclipse/inflection/`; the `orion/4698` segment is an alias of inflection and its one-shot table is not read); Schwab (`schwab/<master>/silver/`, three masters, one firm); Commonwealth (`commonwealth/cottonwood/silver/`).
- Row-filter (code only): SmartX. Its objects hold four firms each (Z-S109), so IAM cannot fence them. The adapter filters rows on `fact_model_allocation_roster.advisor_id`, through the firm's canonical input, before anything is returned. Proof: a two-firm negative arm (a request for one firm returns zero rows of the other).
- Tax SMA: no fence is possible under A2, because no opal-data-assets vendor-silver prefix exists for it (status MISSING in `G2_ROLES.json`).
- The 49F key segment in `opal-data-assets` is `blackdiamond/49f/`. `blackdiamond/49financial/silver/` holds the insurance tables only; no core tool reads it.

## Decisions the adapter cells must not re-open

These are binding on every adapter. A cell that needs to change one files a surprise row and waits for the issuer.

1. Last-4 is never a key. It is never unique on any firm (49F BD 2,741 of 6,186 accounts collide; Cottonwood 84 of 998; Schwab about 54%, 4,056 of 7,555 on 08242234 and 4,156 of 7,646 on 08335338; Commonwealth 731 of 1,533; SmartX 2,692 of 5,999; Orion and Eclipse 22-30 per table). Every tool that takes `account_last4` returns the candidate list first, and every other client tool takes a resolved account.
2. The Schwab masters 08242234, 08335338 and 08403355 overlap (7,534 accounts of 08242234 and all 30 of 08403355 also sit under 08335338). The adapter dedupes by account and never sums across masters. Master 08403355 is admitted by the gateway IAM and is not yet in the registry (proposal in `G2_SCOPES_PROPOSAL.md`).
3. Snapshot-in-every-partition tables are read from the newest partition only and never summed: Orion `fact_transactions` and `fact_performance` (summing counts each transaction about 145 times), BD `dim_advisor_fee_role`, Cottonwood holdings, unrealized and allocations, and the SmartX platform tables. Rolling-window tables (Cottonwood realized and transactions) are read from the newest partition and deduplicated on their event id. Schwab `trn`, `dim_transaction` and `rld` are per-day event files that do sum across partitions, so they are read over the requested window, never as a snapshot.
4. A2 (CTO msg 34134, Andrew-direct): every `client_*` adapter reads ONLY `opal-data-assets/<vendor>/<firm>/silver/` prefixes. No `opal-data-bd`, no `opal-data-mdpf` feeds, no per-firm Tax SMA gold (`opal-data-49financial` and `opal-data-cottonwood` mdpf gold). The excluded stores are listed under NOT USED below.
5. Unregistered SmartX firms Titleist, Canopy and Parable are never returned (v3.2 correction 3): their rows have no `firm_id` in `partner_roster.json`. An unknown `advisor_id` is never mapped to the nearest firm.
6. Freshness is stated in trading days behind the T-1 frontier (2026-10-13, today's frontier), from `lib/trading_calendar.py`, on every answer. The census figures are that calendar's; this cell re-ran three of them (2026-09-28 gives 11, 2026-07-17 gives 61, 2026-06-23 gives 78). The calendar answers from its hardcoded NYSE fallback today and says so.
7. Black Diamond answers state their trading-day lag on every answer. A 49F table at 11 td or 39 td, and any frozen table, may not answer as current. The 49F tables are behind (see the Black Diamond clauses).
8. OPEN ITEM, Black Diamond increment versus snapshot grain: UNMEASURED per table. The adapter cell measures it per table before any tool sums or spans dates. Until then, no BD tool sums across partitions or across a date span.

## `client_resolve_account`

**Inputs.** `firm` (canonical, required); `account_last4` (4 characters, required); `platform` (optional; the source's own label, never a guessed crosswalk); `as_of` (optional, default the newest partition). A second disambiguator, `account_suffix` (last 6) or `account_ref` from a prior call, pins one account.

**Answer and envelope.** `candidates`: every account whose custodian number ends in `account_last4`, never one picked. Each candidate carries `account_ref` (masked, for example `****1234` plus the vendor id), `vendor`, `segment` (the key segment or master), `platform_label`, `platform_label_source`, `label_claim`, and `collisions` (accounts sharing the last-4 in the same firm). The envelope of the shared section applies.

**Adapters (served prefix, freshness in trading days).**
- Black Diamond 49F: `opal-data-assets/blackdiamond/49f/silver/dim_account_xref/`, newest 2026-09-28, 11 td (its producer ends OutOfMemory; the answer states the 11). Candidates carry the BD account id, which is never last-4. The `49financial/silver_legacy/` copy is NOT USED.
- Black Diamond Cottonwood: `opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations/` and `fact_allocations_s2/`, 2026-10-13, 0 td.
- Orion: `opal-data-assets/orion/inflection/silver/fact_positions/`, 2026-10-13, 0 td. Eclipse has no resolve source of its own; it resolves through the Orion `accountId`.
- SmartX: `opal-data-assets/smartx/platform/silver/fact_allocation_account_map/` (49F only; no row exists for the other firms) and `fact_model_allocation_roster/`, 2026-10-13, 0 td. The map is empty on weekends and holidays, so a weekend `as_of` falls back to the prior trading day and says so.
- Commonwealth: `opal-data-assets/commonwealth/cottonwood/silver/crosswalk/` and `account_links/`, newest 2026-06-23, 78 td (closed delivery; the answer carries the 78).
- Schwab: no resolve source. `fact_acc` (the account directory) is PII and is not granted to the gateway, and the `dim_account` projection the census proposes does not exist. The tool refuses with `no_resolve_source` until the projection is built and granted.
- Tax SMA: no vendor-silver prefix exists (A2). The tool refuses with `no_vendor_silver_taxsma`.

**Fence.** Key-segment per vendor (see the fence kinds). The firm's segments are read only; a request for one firm never reads another firm's segment. SmartX applies the row filter on the roster before the candidate list is built.

**Refusal arms.** `firm_not_canonical` (any firm outside the three canonical values); `platform_not_source_label` (a `platform` value that is not the source's own label, for example a contract label such as SmartX on Schwab); `platform_enum_open` (Schwab's platform labels conflict, census O-3, so no Schwab platform filter is served until the CTO rules one enum); `no_resolve_source` (Schwab, above); `no_vendor_silver_taxsma` (Tax SMA); `last4_malformed` (not four alphanumerics); `firm_unregistered` (Titleist, Canopy and Parable rows are dropped and counted, never named as results).

## `client_get_holdings`

**Inputs.** `firm` (canonical, required); `account` (a resolved `account_ref`, required; a last-4 is refused here); `platform` (optional, source label); `as_of` (optional).

**Answer and envelope.** `positions` (ticker or cusip, quantity, market value, weight within the account), `cash`, and the totals of the one partition read. The envelope applies, and the envelope states when the source is weekly or a snapshot of its cadence.

**Adapters (served prefix, freshness in trading days).**
- Black Diamond 49F: no holdings table exists under `opal-data-assets/blackdiamond/49f/silver/` (its silver holds dim_account_xref, dim_advisor_fee_role, fact_bd_allocation and fact_taxsma_report only). The tool refuses with `no_source_49f_a2`. The live weekly unrealized table is in `opal-data-bd`, which is NOT USED.
- Black Diamond Cottonwood: `opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/` and `fact_holdings_s2/` (daily snapshot), 2026-10-13, 0 td. Lots come from `fact_unrealized` in a separate tool.
- Orion: `opal-data-assets/orion/inflection/silver/fact_positions/`, newest partition 2026-10-13, 0 td. `fact_assets` is a duplicate of it and is not read.
- Schwab: `opal-data-assets/schwab/<master>/silver/dim_position/` and `dim_balance/` for 08242234, 08335338 and 08403355, all 2026-10-13, 0 td. The adapter dedupes by account across the three masters (decision 2) and never sums.
- SmartX: `opal-data-assets/smartx/platform/silver/fact_allocation_positions/` and `fact_allocation_valuation/`, 2026-10-13, 0 td. Per allocation; the valuation envelope carries all five basis components and the gold basis is not applied.
- Commonwealth: `opal-data-assets/commonwealth/cottonwood/silver/positions/` (469 rows) and `account_day_value/`, newest 2026-06-23, 78 td.
- Tax SMA: refused `no_vendor_silver_taxsma`.
- Eclipse: no holdings table. The tool refuses with `vendor_no_holdings`.

**Fence.** Key-segment for every vendor except SmartX (row filter on the roster, two-firm negative arm).

**Refusal arms.** `firm_not_canonical`; `account_not_resolved` (a last-4 or a bare number was passed; the caller must resolve first); `no_source_49f_a2` (49F, above); `platform_not_source_label`; `platform_enum_open` (Schwab); `vendor_no_holdings` (Eclipse); `no_vendor_silver_taxsma` (Tax SMA). `stale_weekly_source` is not a refusal: a weekly source is answered from its newest partition with its weekly label.

## `client_get_transactions`

**Inputs.** `firm` (canonical, required); `account` (resolved `account_ref`, required); `start` and `end` (dates, required; a window of at most 13 months); `platform` (optional, source label); `as_of` (optional).

**Answer and envelope.** `transactions`: each row with its date, type, amount (gross, never net, where the source distinguishes them), and the source's own id. `count_in_window` is the denominator. Rows deduplicated on the source event id. The envelope applies.

**Adapters (served prefix, freshness in trading days).**
- Black Diamond 49F: no transactions table exists under `opal-data-assets/blackdiamond/49f/silver/`. The tool refuses with `no_source_49f_a2`. The live transactions table in `opal-data-bd` and the frozen `silver_legacy/transactions` (34 td) are both NOT USED.
- Black Diamond Cottonwood: `opal-data-assets/blackdiamond/cottonwood/silver/fact_transactions/` and `fact_transactions_s2/`, rolling window; read the newest partition, deduplicated on `TransactionID` (12,755 of the newest 12,905 ids repeat in the prior partition), 2026-10-14, 0 td.
- Orion: `opal-data-assets/orion/inflection/silver/fact_transactions/`, newest partition only (it rewrites the full history), 2026-10-13, 0 td; only Complete rows, deduplicated on id.
- Schwab: `opal-data-assets/schwab/<master>/silver/dim_transaction/` for the three masters, 2026-10-13, 0 td; event files that sum across partitions, read over the window. The flow tag the catalog lacks is not served this round.
- Commonwealth: `opal-data-assets/commonwealth/cottonwood/silver/transactions/` (14 parts, 1,416,497 rows; newest 2026-06-23, 78 td). Part semantics are not measured in the census: the adapter cell measures them before it reads a window.
- SmartX and Tax SMA: no account-transaction table. Refused as `vendor_no_transactions`.

**Fence.** Key-segment for every vendor except SmartX and Tax SMA (refused).

**Refusal arms.** `firm_not_canonical`; `account_not_resolved`; `window_too_long` (over 13 months); `window_before_first_partition`; `vendor_no_transactions` (SmartX, Tax SMA); `no_source_49f_a2` (49F); `platform_enum_open` (Schwab).

## `client_get_allocation`

**Inputs.** `firm` (canonical, required); `account` (resolved `account_ref`) or `model` (the source's model key, for model-grain answers); `platform` (optional); `as_of` (optional). The tool answers model assignment and targets (PRD Ruling 1); weights by asset class are read from holdings and labelled as derived.

**Answer and envelope.** `model_assignment` (model key, `cohort_class`, `model_value` where the source has them), `targets` (target weights by security or security set, with the grain stated), `weights` (derived, labelled `derived`). The envelope applies.

**Adapters (served prefix, freshness in trading days).**
- Black Diamond 49F: `opal-data-assets/blackdiamond/49f/silver/fact_bd_allocation/`, one partition, newest 2026-08-18, 39 td. It gives the account's market-value profile only. No model assignment exists (49F has no rebalancer silver); the answer carries `absent_reason` `no_model_assignment_49f` and the 39.
- Black Diamond Cottonwood: `opal-data-assets/blackdiamond/cottonwood/silver/fact_model_assignment/`, `fact_model_definition/` (target weights), `fact_model_blend/` and `fact_model_roster/`, all 2026-10-14, 0 td. The `gold/` `dim_model_portfolio` is NOT USED (A2 reads silver only).
- Orion: weights from `opal-data-assets/orion/inflection/silver/fact_positions/` (0 td), derived.
- Eclipse: `opal-data-assets/eclipse/inflection/silver/fact_portfolios_full/` (drift, cash need, model, status; 2026-10-13, 0 td), `fact_models/` (2026-10-13, 0 td) and `fact_model_composition/` (2026-10-13, 0 td; security-set targets, no ticker weights). `fact_portfolios_simple` is stalled at 2 td (census Z-S111) and is not read.
- Schwab: no model table. Weights are derived from `dim_position/` and `dim_balance/` (0 td) for the three masters; `model_assignment` is refused as `no_model_source`.
- SmartX: `opal-data-assets/smartx/platform/silver/fact_model_allocation_roster/` (model and status per allocation, 2026-10-13, 0 td) and `fact_model_holdings/` (model targets, 0 td). `fact_model_performance` is not read.
- Commonwealth: no allocation table in the closed delivery; refused as `no_allocation_source`.
- Tax SMA: refused `no_vendor_silver_taxsma`. The `taxsma_assets` gold is NOT USED.

**Fence.** Key-segment for every vendor except SmartX (row filter on the roster).

**Refusal arms.** `firm_not_canonical`; `account_not_resolved`; `no_model_assignment_49f`; `no_source_49f_a2` (49F, where no market-value profile exists); `no_model_source` (Schwab); `no_allocation_source` (Commonwealth); `no_vendor_silver_taxsma` (Tax SMA); `model_key_not_in_firm` (a model key that the firm's roster does not carry; a model is never borrowed from another firm).

## `client_get_fees`

**Inputs.** `firm` (canonical, required); `account` (resolved `account_ref`, required); `start` and `end` (dates, required; at most 13 months); `platform` (optional); `as_of` (optional).

**Answer and envelope.** `fees`: each fee row with its date, fee type, amount and the source id, `total_in_window`, and the denominator. The envelope applies; the source's fee-type label is carried unchanged.

**Adapters (served prefix, freshness in trading days).**
- Black Diamond 49F: no fee-row table exists under `opal-data-assets/blackdiamond/49f/silver/`. The tool refuses with `no_source_49f_a2`. The live `opal-data-bd silver/fees` (newest 2026-10-12) and `silver_legacy/fees` (35 td, frozen) are NOT USED. `dim_advisor_fee_role` (11 td) is a fee-schedule table, not a fee-row source, and this tool does not read it.
- Black Diamond Cottonwood: Management Fee rows of `opal-data-assets/blackdiamond/cottonwood/silver/fact_transactions/`, 0 td, behind the Cottonwood one-firm fence (prefix `blackdiamond/cottonwood/` and account prefix `z09`).
- Orion: fee rows of `opal-data-assets/orion/inflection/silver/fact_transactions/` (newest partition, 0 td; the flows of the census include fees).
- Schwab, SmartX, Commonwealth and Tax SMA: no fee table in the G2 silver census. Refused as `no_fee_source`. The SmartX fee statement sits under `advi/`, which holds 0 objects in this bucket (census O-6), so it is not read.

**Fence.** Key-segment per vendor; the Cottonwood branch carries its own one-firm fence, distinct from the 49F branch.

**Refusal arms.** `firm_not_canonical`; `account_not_resolved`; `window_too_long`; `no_fee_source`; `no_source_49f_a2` (49F); `fee_branch_fence` (a Cottonwood account reaching the 49F branch, or the reverse, is refused, never merged).

## Black Diamond clauses (all BD tools)

- The BD adapter reads `opal-data-assets/blackdiamond/<firm>/silver/` only (A2). Firm segment `49f` for 49F; `cottonwood` for Cottonwood.
- Every BD answer states its trading-day lag (decision 7). The 49F lags in this contract: dim_account_xref 11 td, dim_advisor_fee_role 11 td, fact_bd_allocation 39 td (census Z-S110 for the producer).
- Increment versus snapshot grain is an OPEN ITEM (decision 8). No BD tool sums or spans dates until the adapter cell measures the grain per table.

## NOT USED under A2 (one line each)

- `opal-data-bd`, all prefixes: the live 49F silver (`silver/fees`, `transactions`, `allocations`, `realized`, `unrealized`, `prices`) and `schwab/silver/` (the `49-schwab-conv` tables, stopped 2026-07-23, 57 td). NOT USED.
- `opal-data-assets blackdiamond/49financial/silver_legacy/`: the frozen 2026-08-25 copy of opal-data-bd silver (assets 80 td, transactions_enriched 122 td, fees 35 td); not a `silver/` prefix. NOT USED.
- `opal-data-mdpf` feeds (for example `mdpf/feeds/model_aua_positions/<firm>/`, PRD v3.2): NOT USED.
- `opal-data-49financial mdpf/49financial/gold/taxsma_assets/` (per-firm Tax SMA gold): NOT USED.
- `opal-data-cottonwood mdpf/cottonwood/gold/taxsma_assets/` (per-firm Tax SMA gold): NOT USED.
- `opal-data-assets` `blackdiamond/cottonwood/gold/dim_model_portfolio` and every other non-silver prefix (bronze, gold, meta, `_ops`): outside the silver-only rule. NOT USED.
- `opal-data-assets gateway/global/silver/taxsma_workbook`: a multi-firm workbook (RIA column) under the gateway prefix, not a vendor-silver prefix. NOT USED by any core tool.
- `blackdiamond_list_fees` (the existing tool): a non-G2 tool that reads `opal-data-bd`. This cell does not change it, and no `client_*` tool calls it.

## Tax SMA: status MISSING

No `opal-data-assets` vendor-silver prefix exists for Tax SMA. Its only served forms are the per-firm mdpf `taxsma_assets` gold (NOT USED, above) and the multi-firm gateway workbook (NOT USED, above). Every Tax SMA tool call refuses with `no_vendor_silver_taxsma`. This is a gap for the issuer to route, not a silver source this contract invents.

## Not in this contract

The rest of G2 (lots, realized, performance, profile, insurance) is the G2 rest group and is contracted in a later cell. `commonwealth_describe_delivery`, `etfs_get_fund_holdings` and `prices_get_history` are not client tools this round.
