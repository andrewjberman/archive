# PLATINUM OUTPUT CONTRACT — 49F (bd) Group-D Publishers

**TO:** OPAL_GLDRNS.A1 | **Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-07-15 (~19:2x-19:5xZ window)
**Status:** COMPLETE — 8/8 D scripts pinned.
**THIS DOCUMENT IS THE S4/S5 TARGET ARTIFACT** (OPAL_CONSOLIDATION WS-C): the parity harness (A3)
diffs against these shapes; the cutover writes to these locations. A2's sufficiency verdict censuses
against the inputs named here.

## 0. Basis label (never-summed law)

Every quantity behind every surface in this contract is the **49F BLACK DIAMOND custody basis
(master 0833)** — the bd pipeline tree (`opal-data-bd`). This is NOT the SmartX 0824 basis. No row
in this document may be summed with a 0824-basis quantity; the identity is recorded, never resolved.
The served artifacts themselves carry an in-band basis label where headline NNA is shown
(`headline.nna_basis` in dashboard.json / clients_tab.json — verified in served bytes).

## 1. Method, instruments, vintages

- **Source pin:** repo `CLOUD @ 0f248d7f9` — all `file:line` cites below are at this vintage.
- **Portal consumer cites:** `portal @ 3df9231e (DEV)` — `ai.ts` = `portal/src/api/endpoints/advisor-intelligence.ts`.
- **Served measurements:** full `ListObjectsV2` listings of `s3://opal-data-bd/platinum/` (23,593
  objects), `gold/artifacts/` (44 objects), `gold/entities/`, legacy prefixes — taken 2026-07-15
  ~19:35Z. Fan-out counts below are MEASURED from those listings, not estimated.
- **Shape verification:** 34 served artifacts downloaded and field-tree-enumerated (depth-2), >=2
  per surface class; every shape row cites its emit code. Depth convention: trees below are
  top-envelope field-level; leaf fields beyond depth-2 are carried by the cited emit function.
- **Compiler tools:** `comp-pipescript io` x8 (D-group returns empty manifests — dynamic key
  construction; the tool itself prints "manual review required", which this document is);
  `comp-blast D_04` (2 corpus HOLD claims read: the D_04 clients_tab envelope is a pinned
  cross-firm FE contract; cp1252 crash defect banked in session log). Raw listings/downloads
  rail-marked per the TO's mandate.
- **UNKNOWN is a legal verdict** and appears with a named reason wherever used.

## 2. Denominators

| what | count |
|---|---|
| D scripts pinned | 8/8 |
| Distinct D-owned output key patterns | 46 (36 platinum-or-passthrough + 10 gold-artifact/view) |
| Served platinum objects (whole prefix) | 23,593 |
| Served artifacts field-tree spot-verified | 34 files across 12 surface classes |
| Portal consumer anchors cited | 21 (ai.ts) + 3 Lambda/edge/docstring anchors |
| Surfaces flagged (orphan / mismatch / unknown-consumer) | 9 (sec. 6) |
| D-to-D edges mapped | 12 (sec. 5) |

## 3. Trigger, cadence, runner box (common to all 8)

- **Box:** EC2 `bd-gold-layer-runner` (`i-01003b035d2988dfb`, r6i.4xlarge) — live-verified this
  session (`describe-instances`: exists, `stopped` between runs; boots on trigger, stops at end).
- **Trigger:** `bd-gold-trigger` Lambda (incremental/full) boots the box; the box runs
  `gold_dispatch.sh`. Deploy path: S3 `opal-data-bd/code/gold/` (DS-owned upload).
- **Chain (dispatcher = `gold_dispatch.sh:143`):** `CHAIN_DOWNSTREAM="C_03 C_05 C_07 C_06 C_08 D_00 D_00b D_00c D_00f D_01 D_02 D_03 D_04"`.
- **D-phase ordering (`gold_dispatch.sh:467-485`):**
  - PHASE_D1: `D_00 || D_00c || D_03` (waits on `gold/validation/aua_certification/`)
  - PHASE_D2: `D_00b || D_01` (waits on `gold/canonical/role_aua/`)
  - PHASE_D3: `D_02` -> PHASE_D4: `D_04` -> PHASE_D5: `D_00f`
- **Cadence:** nightly. Measured 2026-07-15 run timeline (LastModified): gold artifacts
  00:46-00:52Z (D_00/D_00c/D_03/D_01), platinum firm 01:04-01:12Z (D_04), advisor_nna_canonical
  01:26Z (D_00f).
- All 8 scripts are dry-run-by-default; `--upload` writes. All writes SSE AES256 or default.

## 4. Per-script contract

### D_00.portal_aggregates.py (1,028 lines) — PHASE_D1

| output key | fan-out (measured) | shape (top envelope) | grain | consumer |
|---|---|---|---|---|
| `gold/artifacts/clients_tab.json` (emit :978) | 1, 206,701B @ 07-15 | `{generated_at, data_as_of, firm_id, headline{total_aua, account_count, client_count, fee_rate_pct, income_yield_pct, small_account_count, fee/non-fee splits x4, nna_mtd/qtd/ytd/12m, nna_basis}, tax{taxable/deferred/free +pcts, capital_gains_ttm, qualified splits, cost_basis_by_year, top_gain_positions, ...}}` | firm (N1) | D_04 dashboard build (D_04:350 `clients_tab`); FE via clients-tab Lambda endpoint on split dashboards (ai.ts:446,498) |
| `gold/artifacts/summary/header_metrics.json` (:984) | 1, 1,649B @ 07-15 | `{generated_at, data_as_of, firm_id, firm_name, total{aua, nna_mtd/qtd/ytd/12m, client/account counts, new/existing client splits, q0-q3, fee splits}, by_architect[10]}` | firm | D_04 pass-through (D_04:2494->platinum); FE reads the PLATINUM copy (ai.ts:284). NOTE: FE comment ai.ts:280-283 calls this gold key "DEAD (bd writer removed 2026-06-18)" — MEASURED FALSE at bucket: fresh nightly 07-15. FE-comment drift, flagged sec-6.9 |
| `gold/artifacts/filters/dimensions.json` (:988) | 1 @ 07-15 | `{generated_at, firm_id, dimensions{architect, region, implementor, account_type, tax_status, state}}` | firm | filters endpoint (ai.ts:10 doc block; opal-partners-data proxy) |
| `gold/artifacts/snapshots/aua_by_{architect,tax_status,state,region}.json` (:993) | 4 @ 07-15 | `{generated_at, data_as_of, firm_id, dimension, total_aua, data[47]}` (state sample) | firm x dimension | snapshots endpoint `GET .../snapshots/{dimension}` (ai.ts:10) |
| `platinum/{firm_id}/ownership_map.json` (:998) | 1 (=`platinum/49financial/`), 419,404B | `{schema_version:1, firm_id, generated_at, advisors{...}}` (schema frozen v1) | firm; advisor-keyed map | ADVI_PROFIL.004c edge router (s3_layout.py:224-228 anchor); not an FE fetch |
| `gold/views/nna_aua_by_geography.parquet` + `_city` + `nna_aua_by_advisor.parquet` (:966-968, dual-write LEGACY via `_write_view_parquet` :205-212 — LEGACY map has no entries for these, so single-write in practice) | 3 parquets | (date, state, country) / (date, state, city) / (date, architect) aggregates of client_performance | daily x geo/advisor | D_01 (docstring D_00:10-12; D_01 imports :78) — D-to-D edge |

- **Inputs:** CLIENT_PERFORMANCE, ACCOUNT_PERFORMANCE, ACCOUNT_TEAM, FEE_RATE_HISTORY,
  CLIENT/ACCOUNTS dims, CLIENT_TAX_LIABILITY, REL_ARCHITECT_LOOKUP, `gold/validation/aua_certification/{date}.json` (C_02).
- **Served-AUA guard (contract-load-bearing):** `_resolve_served_aua` (D_00:246-280) — NEVER serves
  a degenerate (<=0) certified AUA; `DEGENERATE_CERT_MODE` env (`hold` default = last-good cert
  within 14d lookback; `gold` = computed position sum). The refactor MUST carry this guard.
- **Env params:** `FIRM_ID`/`FIRM_NAME` (default 49financial), `DEGENERATE_CERT_MODE`.

### D_00b.portal_timeseries.py (1,417 lines) — PHASE_D2

| output key | fan-out | shape | grain | consumer |
|---|---|---|---|---|
| `gold/artifacts/timeseries_chart.json` (emit :1412 via `_save_json`) | 1, 38,674,188B @ 07-15 | `{generated_at, data_as_of, firm_id, date_range{start,end,days}, metadata{new_clients}, aua{quarterly,monthly,annually}, nna/adv/geo/ofc/nna_ofc/nna_geo/nna_adv{description,categories,data[]}, growth_decomposition{description,data}, geo_drill{TX,FL,CA,...}}` | firm; daily series x view | FE direct (ai.ts:300 `/artifacts/timeseries_chart.json`); D_04 pass-through with 3-year NNA gate (D_04:2517-2525) -> `platinum/firm/timeseries_chart.json` (FE ai.ts:409) |

- **Inputs:** ACCOUNT/CLIENT_PERFORMANCE, CANONICAL_NNA_PREFIX (partitioned), CANONICAL_ROLE_AUA_PREFIX,
  ACCOUNT_TEAM, REL_ARCHITECT_LOOKUP, dims, HOLDINGS_LOTS_PREFIX, `gold/dimensions/dim_advisor_office.csv` (:102), aua_certification.
- NOTE the served artifact is 36.9MB — the platinum copy (36.1MB) differs only by the D_04 NNA
  3-year gate. Both are live consumers' sources (two FE fns).

### D_00c.portal_leaderboard.py (1,397 lines) — PHASE_D1

| output key | fan-out | shape | grain | consumer |
|---|---|---|---|---|
| `gold/artifacts/employee_leaderboard.json` (emit :1390) | 1, 3,395,623B @ 07-15 | `{generated_at, data_as_of, firm_id, leaderboard_type, role_breakdown_semantics, fee_basis_semantics, available_roles[5], available_windows[9], window_bounds{3M,6M,1Y,2Y,3Y,MTD,QTD,YTD,MAX}, windows{...same 9...}}` | firm; per-window advisor rows | D_04 `build_leaderboard` trims to QTD+YTD -> `platinum/firm/leaderboard.json` (D_04:2188-2408; FE ai.ts:429-438, :1311). Direct platinum pass-through of THIS file: none (see sec-6.1) |

- **Inputs:** ACCOUNT_PERFORMANCE, ACCOUNT_TEAM, REL_ARCHITECT_LOOKUP, CLIENT_DIMENSION,
  ADVISOR_ASSIGNMENTS, ADVISOR_FEE_DETAIL_PREFIX, CANONICAL_NNA_PREFIX, CANONICAL_ROLE_AUA_PREFIX,
  FEE_RATE_HISTORY; shares `lib.advisor_nna_attribution` (BUCKET_KEYS/ROLE_NULLS) with D_00f —
  cross-route per-advisor NNA identity is a pinned invariant (D_00f docstring :24-26).

### D_00f.advisor_nna_canonical.py (973 lines) — PHASE_D5 (last)

| output key | fan-out | shape | grain | consumer |
|---|---|---|---|---|
| `platinum/firm/advisor_nna_canonical.json` (OUTPUT_KEY :91-92; emit :928 via `_write_json_s3` :755-767) | 1, 3,635,776B **GZIP AT REST** (0x1f8b verified; decompressed OK) | `{firm_id, firm_name, generated_at, data_as_of, definition, source, window_vocabulary{QTD,YTD,MAX,1Y,3Y,q_current,q1,q2,q3}, window_bounds{...}, firm{windows,series}, advisors{name->...}, geo{definition,states}, reconciliation{method, tolerance_usd, all_pass, max_abs_delta, series_tie_max_abs_delta, advisors_non_additive...}}` | advisor x window x cohort (+ geo state/city; firm rollup) | DistributionTab Continuous-NNA GEO+ADV — SOLE NNA source (ai.ts:392 `getAdvisorNnaCanonical`) |

- **Inputs:** `gold/canonical/nna/` (C_01 atomic, account x date), `gold/dimensions/accounts_dimension_latest.parquet`,
  `gold/views/account_team.parquet` (C_07, `architect_no_infer`).
- **Contract-load-bearing semantics (docstring :19-49):** all-roles attribution counted once per
  account; NON-ADDITIVE across advisors (~3x firm; firm NNA stays account-once additive);
  49F House + Unassigned preserved as `is_bucket=true` rows; `fee_paying/no_fee` leaves emit NULL
  (never fabricated-zero); `nna_txn = daily_inflow - daily_outflow` over ALL rows (`nna_clean` is a
  quality flag, NOT an aggregation filter). In-artifact `reconciliation` block is a self-check the
  refactor must reproduce.
- **Write sentinel:** post-write head_object freshness assert (:937-948) — silent no-write fails loud.
- **Env params:** `OUTPUT_PREFIX` (default `platinum/`).

### D_01.partner_analytics.py (2,658 lines) — PHASE_D2

| output key | fan-out | shape | grain | consumer |
|---|---|---|---|---|
| `gold/artifacts/partner_analytics/header_metrics_{quarterly,monthly,annual}.json` (`write_s3` :2542-2555) | 3 x ~4.3-4.7MB @ 07-15 | `{generated_at, data_as_of, firm_id, firm_name, granularity, periods{current,q1,q2,q3}, views{aua, nna, geo, adv, ofc, cla, ofc_per_period}}` (quarterly sample; period labels differ per gran) | firm x granularity; views x period | D_04 re-emit -> `platinum/firm/partner_analytics_{gran}.json` (D_04:1880-1922; FE ai.ts:361-369). Legacy `getPartnerAnalytics` route also exists (ai.ts:362 comment) — exact legacy path UNKNOWN (not needed: platinum route is the live one) |
| LEGACY dual-write `gold/partner_analytics/header_metrics_{gran}.json` (:2556-2566) | 3 @ 07-15 | byte-identical | same | none found in FE — migration-era dual-write still burning writes (sec-6.5) |

- **Inputs:** CLIENT/ACCOUNT_PERFORMANCE, dims, NNA_AUA_BY_GEOGRAPHY(+city)/BY_ADVISOR (D_00 views
  — D-to-D), REL_ARCHITECT_LOOKUP, CANONICAL_NNA_PREFIX, ACCOUNT_TEAM, canonical_role_aua_key,
  `gold/dimensions/dim_advisor_office.csv` (:110), aua_certification.

### D_02.advisor_client_detail.py (3,311 lines) — PHASE_D3

| output key | fan-out (measured) | shape | grain | consumer |
|---|---|---|---|---|
| `gold/entities/advisors/{id}/book.json` (`advisor_book_key`) | 166 @ 07-15 | `{generated_at, data_as_of, book_type, book_key, book_name, active_since, summary{tagged_aua, fee_earning_aua, non_fee_earning_aua, implied_annual_revenue, avg_fee_bps_earned, counts...}, role_breakdown{architect, implementor, consultant, local_ops, additional_advisor}, nna{ytd,qtd,mtd}, growth{...}, tax_exposure{...}, clients[], rfs{...}}` | advisor (L2) | D_04 advisor summary build (D_04:492-680); AdvisorsTab tagged-AUA override provenance (AdvisorsTab.tsx:394,411); opal-partners-data Lambda books path (types.ts:2459) |
| `gold/entities/advisors/{id}/timeseries.json` | 186 (166 current + 20 stale departed-advisor leftovers, sec-6.7) | `{advisor_id, advisor_name, data_as_of, data[]}` (via platinum copy) | advisor daily | D_04 pass-through w/ NNA cutoff -> platinum (D_04:682-687) |
| `gold/entities/advisors/{id}/mix_timeseries.json` (emit :2322) | 55 | period mix response (shares FirmMixViews schema family) | advisor x period | D_04 (mix passthrough family) |
| `gold/entities/clients/{rel_id}/detail.json` | 3,288 | `{generated_at, data_as_of, firm_id, client_key, client_name, headline{...}, tax{... incl. open_lots, cost_basis_by_year, top_gain_positions}, income_fees{...}, accounts[], ...}` | relationship (L3) | D_04 client summary build (D_04:985-1108) |
| `gold/entities/clients/{rel_id}/aua_timeseries.json` | 3,575 | timeseries envelope `{data[]}` | relationship daily | D_04 (client summary rfs/decomposition_90d :740+) |
| `gold/entities/accounts/{acct_id}/aua_timeseries.json` | 8,005 | timeseries envelope | account daily | D_04 account summary build (D_04:1187+) |
| `gold/artifacts/implementor_leaderboard.json` (emit :3197) | 1, 198,301B @ 07-15 | leaderboard family (windows/entries) | firm; implementor rows | UNKNOWN — no FE fetch found in portal grep; possibly legacy DistributionTab route. Flag sec-6.6 |
| `gold/canonical/role_aua/{date}.parquet` (pre-pass emit :3097) | daily partitions | (date, advisor_id, role) AUA+flow table (schema ratified RA-P0) | advisor x role x date | D_00b/D_00c/D_01/D_02 read `CANONICAL_ROLE_AUA_PREFIX` — an INVERTED D-to-D edge (a D script feeding earlier-phase scripts; same-run vs prior-run vintage semantics UNKNOWN — dispatch waits on the prefix at PHASE_D2, `gold_dispatch.sh:473`, while D_02 runs at D3) |

- **Inputs:** ACCOUNT_PERFORMANCE, ACCOUNT_TEAM, ADVISOR_ASSIGNMENTS, ADVISOR_FEE_DETAIL_PREFIX,
  FEE_RATE_HISTORY, CLIENT_DIMENSION, CLIENT_TAX_LIABILITY, HOLDINGS_LOTS_PREFIX, REL_ARCHITECT_LOOKUP,
  CANONICAL_NNA_PREFIX, CANONICAL_ROLE_AUA_PREFIX.
- Docstring (:5) says "no dual-write" — confirmed: no LEGACY imports.

### D_03.composition_artifacts.py (897 lines) — PHASE_D1

| output key | fan-out | shape | grain | consumer |
|---|---|---|---|---|
| `gold/views/firm_composition.json` (emit :463-487 family; + LEGACY `gold/firm_composition.json` :177-179) | 1 @ 07-15 (+1 legacy) | `{generated_at, data_as_of, scope{firm_id}, total_market_value, top_holdings[9], other{market_value,pct}, mix[4]{asset_class,label,market_value,pct,top_holdings[9],other}, unclassified{count,market_value}}` (canonical per ADVI_BKSCMP_PRD §3) | firm (N1) | `GET /api/scoped/partners/books/firm/all/composition` (opal-partners-data proxy; D_03 docstring :9-11); D_04 mix_summary embeds it verbatim as `.composition` (verified byte-shape match) |
| `gold/entities/advisors/{id}/composition.json` (+legacy `gold/advisors/{id}/composition.json`) | 165 (+454 legacy objects total under `gold/advisors/`) | same schema, `scope{advisor_id, firm_id}` | advisor (L2) | books advisor composition endpoint (docstring :10); D_04 advisor summary concentration source (D_04:53) |
| `gold/artifacts/firm_mix_views.json` + `firm_mix_views_daily.json` (:463-487, + LEGACY `gold/firm_mix_views*.json`) | 2 (+2 legacy) | period mix views (FirmMixViewsResponse family) | firm x period | D_04 mix_summary build (D_04:383-482) |
| `gold/entities/advisors/{id}/mix.json` + `mix_daily.json` (+legacy advisor mix keys) | 55 + 55 | mix views family | advisor x period | D_04 advisor mix pass-through -> `platinum/advisors/{id}/mix.json` (D_04:689-691; FE ai.ts:416); advisor mix Lambda |
| `gold/views/mix_daily_summary.json` | 1 @ **07-12** (3 days older than siblings) | mix daily rollup | firm daily | D_04 reads MIX_DAILY_SUMMARY (import :104). Vintage lag flagged sec-6.8 |

- **Inputs:** HOLDINGS_LOTS_PREFIX (latest parquet), ACCOUNT_PERFORMANCE, REL_ARCHITECT_LOOKUP,
  CLIENT_DIMENSION, CLIENT_PERFORMANCE, MIX_DAILY_SUMMARY (self-read :436), FIRM_MIX_VIEWS (self-read),
  DynamoDB-backed `ETFClassifier` (lib) — an OFF-S3 dependency the refactor must carry.
- Per-client composition keys (`client_composition_key` imports) — emitted via C_06 path; D_03's own
  client-side writes limited to the advisor/firm families (write sites :168-180, :463-545).

### D_04.client_portal_summary.py (3,793 lines) — PHASE_D4 (the big publisher)

**Firm surfaces (platinum/firm/):**

| output key | fan-out + size | shape | consumer |
|---|---|---|---|
| `dashboard.json` (:315-371) | 1, 576B (SPLIT mode) | `{generated_at, data_as_of, firm_id, headline{total_aua, account/client counts, fee_rate_pct, income_yield_pct, small_account_count, fee splits x6, nna_mtd/qtd/ytd/12m, nna_basis}, split:true}` — split=true because bundle >200KB; non-split would inline `clients_tab`, `employee_leaderboard`, `fee_efficiency` (see cot memory: envelope is a pinned cross-firm FE contract) | `getPlatinumFirmDashboard` (ai.ts:441-499); on split=true FE fetches leaderboard.json + fee_efficiency.json + clients-tab endpoint |
| `fee_efficiency.json` (:368) | 1, 723,638B | C_08 `advisor_fee_efficiency.json` re-emit | dashboard bundle (ai.ts:480-481) |
| `mix_summary.json` (:383-482) | 1, 8,682B | `{generated_at, data_as_of, firm_id, mix{equity,fixed_income,alternatives}, mix_periods[5], concentration{top_n,items,other}, composition{<firm_composition.json embedded>}}` | ai.ts:508 |
| `timeseries_overview.json` (:1785-1870) | 1, 229,129B | `{generated_at, data_as_of, firm_id, aua/nna/growth_decomposition/mix each {quarterly,monthly,annually}}` | ai.ts:356 |
| `partner_analytics_{quarterly,monthly,annual}.json` (:1880-1922) | 3 | D_01 gran files re-emitted (shape = D_01 row) | ai.ts:369 |
| `cumulative_chart.json` (:1981-2158) | 1, 4,657,560B | weekly-sampled geo/adv/nna series (replaces daily timeseries_chart at ~7x smaller — docstring :375) | ai.ts:378 |
| `leaderboard.json` (:2188-2408) | 1, 1,584,902B | `{generated_at, data_as_of, firm_id, role_breakdown_semantics, window_bounds{QTD,YTD,MAX,1Y,3Y}, available_windows[5], windows{...}}` — D_00c employee_leaderboard trimmed + D_02 tagged-AUA override | ai.ts:429-438, :1311 |
| `leaderboard.prior_week.json` (:2398-2399 S3 copy) | 1, 3,395,623B | prior week's leaderboard.json (server-side copy before overwrite) | WoW delta consumers (FE leaderboard deltas) |
| `clients-tab-slim.json` (:2418-2477) | 1, 577B | `{generated_at, data_as_of, firm_id, headline{10 fields}, tax{7 fields}}` — PII-free slim | 49F FE consumer NONE found (bd split-dashboard path uses the clients-tab Lambda). Written for the cot-parity surface family; flag sec-6.4 |
| `header_metrics.json` (:2503-2512 pass-through of D_00 gold) | 1, 1,649B | = D_00 summary/header_metrics.json verbatim | ai.ts:284 |
| `timeseries_chart.json` (:2517-2525 pass-through + 3yr NNA gate) | 1, 36,102,558B | = D_00b artifact with nna/nna_ofc/nna_geo/nna_adv data[] gated >= today-3y | ai.ts:409 |
| `employee_leaderboard.json` | 1, 886,284B @ **2026-04-09 FROZEN** | (April vintage) | NO current writer (pass-through explicitly removed, :2505-2508; build_leaderboard writes leaderboard.json only) + NO consumer found (getEmployeeLeaderboard replaced, ai.ts:429-430). ORPHAN — sec-6.1 |

**Entity fan-outs (measured 2026-07-15):**

| output key | measured | docstring claim | shape (spot-verified x2) |
|---|---|---|---|
| `platinum/advisors/{id}/summary.json` (:492-680) | 166 | ~20 | `{generated_at, data_as_of, advisor_id, distribution{total}, book{19 fields incl. tagged_aua, rfs}, mix, mix_periods[5], concentration{top_n,items,other}, fee_summary{weighted_avg_fee_bps, annual_implied_revenue, by_role}, tax_exposure{19 fields}, active_since, role_breakdown}` |
| `platinum/advisors/{id}/timeseries.json` (:682-687) | 166 | — | `{advisor_id, advisor_name, data_as_of, data[662]}` (NNA cutoff gated) |
| `platinum/advisors/{id}/mix.json` (:689-691) | 55 | N advisor mix | D_03 mix pass-through; partial fan-out = only advisors with D_03 mix data |
| `platinum/advisors/{id}/nna_clients.json` (:2541-2670) | 166 | — | `{generated_at, data_as_of, advisor_id, total_nna, client_count, clients[<=10]}` (Top 9 + Other, QTD) |
| `platinum/advisors/{id}/positions.json` (:2684-2865) | 163 | — | `{advisor_id, firm_id, as_of_date, total_aum, positions_count, top_n_limit, positions[25]}` |
| `platinum/advisors/{id}/exec_summary.json` | 160 @ **2026-05-04 FROZEN** | — | `{advisor_id, firm_id, generated_at, model, input_hash, bullets[], permissions_scope}` (LLM batch artifact). NO writer in any D script; STILL CONSUMED (ai.ts:941,947). Sec-6.2 |
| `platinum/clients/{rel_id}/summary.json` (:985-1108) | 3,143 | ~600 | `{generated_at, data_as_of, relationship_id, detail{client_name,total_aua,accounts,tax}, mix, mix_periods, concentration, decomposition_90d{market_growth,nna,synthetic_correction}, fee_summary{by_account,window_revenue,...}, rfs{12 windows-fields}}` |
| `platinum/clients/{rel_id}/views.json` (:1112) | 3,143 | — | `{generated_at, data_as_of, relationship_id, views{quarterly,monthly,annually}}` (C_06 re-emit) |
| `platinum/clients/{rel_id}/composition.json` (:1116) | 3,117 | — | D_03-family composition, scope{relationship_id, firm_id} (C_06 re-emit) |
| `platinum/clients/{rel_id}/mix_timeseries.json` (:1130-1167) | 3,143 | ~600 | `{generated_at, data_as_of, relationship_id, mix[1261]}` |
| `platinum/clients/{rel_id}/concentration.json` (:1168-1175) | 3,143 | ~600 | `{generated_at, data_as_of, relationship_id, concentration[1261]}` |
| `platinum/accounts/{acct_id}/summary.json` (:1187-1341) | 7,012 | ~3,500 | `{generated_at, data_as_of, account_id, total_market_value, mix, concentration, timeseries[932-1187], rfs{12}}` |

**Analytical artifacts (gold/, not platinum):**

| output key | measured | shape | consumer |
|---|---|---|---|
| `gold/platinum/firm/cohort_a_summary.json` (:2878-3051) | 1, 2,867B @ 07-15 | `{account_count, total_aua, client_count, state_distribution[27], top_n_named[20], snapshot_date, methodology_note, generated_at}` | FE reads `platinum/firm/cohort_a_summary.json` (ai.ts:1341) — **PATH MISMATCH, key absent at consumed path.** Sec-6.3 |
| `gold/platinum/firm/cash_coverage_summary.json` (:3063-3151) | 1, 295,681B @ 07-15 | `{firm_cash_aggregate, per_account[6877], source_date, account_count, cash_bearing_account_count, source_artifact, methodology_note, generated_at}` | NONE found in FE. Analytical/audit artifact — sec-6.4 |
| `gold/artifacts/49f/out_of_scope_accounts.json` (:3163,:3392) + `c1_recovered_accounts.json` (:3188,:3664) | 2 | audit censuses | none (audit artifacts by design) |

- **Inputs (D-to-D + external):** docstring :49-58 — D_00 (employee_leaderboard, clients_tab),
  C_08 (advisor_fee_efficiency), D_03 (firm_mix_views, firm_composition, advisor mix/composition),
  D_02 (book/timeseries/mix_timeseries, client detail/aua_timeseries), C_06 (client
  timeseries/views/composition), B_01 (holdings_lots), D_01 (header_metrics_{gran}),
  MIX_DAILY_SUMMARY, CANONICAL_NNA_PREFIX, ACCOUNT_PERFORMANCE, ACCOUNT_TEAM, dims,
  lib.exclusions (ghost accounts + insurance config + AP gate), ETFClassifier (DynamoDB).
- **Number-consistency law (docstring :38-47):** every level derives from the same
  account_performance snapshot; D_04 consolidates, NEVER re-aggregates. Firm total =
  clients_tab.headline.total_aua; advisor AUA = D_02 book.summary.total_aua; client AUA = D_02
  detail.headline.total_aua. THE refactor invariant.
- **Destructive op (contract-relevant):** stale-advisor cleanup deletes `platinum/advisors/{id}/`
  prefixes for departed advisors, guarded against empty-current-set mass delete (:693-731). The
  guard is artifact-scope-blind for CURRENT advisors — the exec_summary orphan mechanism (sec-6.2).

## 5. D-to-D edge map (census for A2)

```
D_00.views (nna_aua_by_geography/_city/_advisor) -----------------> D_01
D_00.clients_tab + summary/header_metrics + (employee_leaderboard) -> D_04 (dashboard, pass-throughs)
D_00b.timeseries_chart --------------------------------------------> D_04 (3yr-NNA-gated pass-through)
D_00c.employee_leaderboard ----------------------------------------> D_04.build_leaderboard (trim + D_02 override)
D_01.header_metrics_{gran} (gold/artifacts/partner_analytics/) ----> D_04.partner_analytics_{gran}
D_02.book/timeseries/mix_timeseries (advisors) --------------------> D_04 advisor summaries
D_02.detail/aua_timeseries (clients, accounts) --------------------> D_04 client + account summaries
D_02.role_aua parquet (gold/canonical/role_aua/) ------------------> D_00b, D_00c, D_01, D_02 (INVERTED
                                          edge; same-run vs prior-run vintage UNKNOWN -- named above)
D_03.firm_mix_views(+daily)/firm_composition ----------------------> D_04.mix_summary
D_03.advisor mix/mix_daily/composition ----------------------------> D_04 advisor mix + summary concentration
External-in: C_01 nna atomic -> D_00f; C_02 aua_certification -> D_00/D_00b/D_01;
             C_06 client artifacts -> D_04; C_07 account_team -> (all); C_08 fee_efficiency -> D_04;
             B_01 holdings_lots -> D_03/D_04
```

## 6. Findings (each carries its own disposition path)

1. **`platinum/firm/employee_leaderboard.json` — ORPHAN (writer-less + consumer-less).** Frozen
   2026-04-09; pass-through deliberately removed (D_04:2505-2508); FE replaced the consumer
   (ai.ts:429-430). RETIREMENT CANDIDATE — flagged, not silently carried (per TO d).
2. **`platinum/advisors/{id}/exec_summary.json` — CONSUMED-BUT-FROZEN.** 160 files @ 2026-05-04;
   generator absent from all 8 D scripts (an LLM batch artifact, `model`+`input_hash` fields); FE
   still fetches it (ai.ts:941-947). Mechanism of survival: D_04's cleanup deletes departed-ADVISOR
   prefixes, never stale artifact TYPES for current advisors. Disposition needed: retire the FE
   fetch or re-home the generator (route to CTO with A2).
3. **`cohort_a_summary.json` PATH MISMATCH.** Written to `gold/platinum/firm/` (D_04:2878), consumed
   at `platinum/firm/` (ai.ts:1341); no router maps between them (infra grep: zero `gold/platinum`
   references in `infra/aws/lambda`); the consumed key does not exist in the bucket. Either the FE
   call is dead code or it 404s. Route to CTO with A2 (MISSING-class analog).
4. **Consumer-less-for-49F surfaces (flagged, not carried silently):** `platinum/firm/clients-tab-slim.json`
   (cot-parity family; 49F split-dashboard path uses the Lambda endpoint) and
   `gold/platinum/firm/cash_coverage_summary.json` (analytical). Also FE consumers exist for keys
   ABSENT in bd: `activity_scan_*`, `cash_drag_*`, `firm_concentrations.json`, `client_directory.json`
   (ai.ts:1420-1498, :519 — inf-authored surfaces; 49F-side production is a design decision for the
   refactor, not a defect).
5. **Migration-era legacy dual-writes still burning:** D_01 legacy gran files
   (`gold/partner_analytics/header_metrics_{gran}.json`, fresh nightly, no consumer found);
   D_03 legacy `gold/advisors/` (454 objects) + legacy firm mix/composition keys. Plus frozen relics
   with no current writer: `gold/partner_analytics/header_metrics.json` (2026-03-04),
   `gold/partner_analytics/timeseries_chart.json` (2026-02-12; retired fargate-era producer).
   Cutover should retire rather than port these.
6. **`gold/artifacts/implementor_leaderboard.json` consumer UNKNOWN** (fresh nightly; no FE fetch
   found in portal grep). Named reason: possible non-`ai.ts` consumer; needs one component-level
   sweep before a retirement call.
7. **Stale entity stragglers:** gold/entities advisor timeseries 186 vs 166 books (20 departed-advisor
   leftovers — gold/entities has NO cleanup analog to D_04's platinum cleanup); platinum clients
   60 files @ 07-10/07-11; platinum accounts 18 files @ 07-03/07-11 (entity-set drift between runs).
8. **`gold/views/mix_daily_summary.json` @ 07-12** while its D_03 siblings are 07-15 (3-day lag,
   write-on-change semantics vs a defect: UNKNOWN — one run-log read adjudicates it).
9. **FE-comment drift (record hygiene):** ai.ts:280-283 claims the D_00 gold header_metrics writer
   was "removed 2026-06-18" — the artifact is measurably fresh nightly (07-15 00:46Z). The re-path
   to platinum was correct anyway; the stated reason is false at the bucket.
10. **D_04 docstring drift:** the header output list (:9-32) omits nna_clients, positions,
   exec_summary (retired), clients-tab-slim, leaderboard.prior_week, fee_efficiency, cohort_a,
   cash_coverage, 49f audit artifacts; fan-out counts are ~2x stale (measured column above).
   The CONTRACT (this doc) supersedes the docstring for S4/S5 purposes.

## 7. What the refactor must carry (invariant digest for A2/A3)

- The D_04 number-consistency law (one account_performance snapshot; no re-aggregation).
- The D_00 degenerate-cert floor (`_resolve_served_aua` — never <=0 AUA served).
- The D_00f canonical NNA semantics (all-roles once-per-account, non-additive, bucket rows
  preserved, NULL-not-zero fee leaves, nna_clean not a filter) + gzip-at-rest + write sentinel.
- The cross-route advisor-NNA identity (D_00c and D_00f share lib.advisor_nna_attribution).
- The split-dashboard envelope contract (dashboard.json split flag + sibling fetches; cot needs it
  INLINE — cross-firm FE contract, memory reference_cot_firm_book_data_shape_divergence).
- The 3-year NNA gate on the platinum timeseries_chart copy (FIX6, D_04:2518-2524).
- The stale-advisor cleanup WITH its empty-set guard, extended (finding 2) to artifact-type scope.
- In-band basis labels (`nna_basis`) on every headline NNA emit.
- CacheControl headers: JSON emits carry `public, max-age=300, s-maxage=3600` (gold_utils:80,
  D_01:2553); D_03 serves with `no-store` per its docstring — per-surface cache policy is part of
  the contract.
- OFF-S3 dependencies: DynamoDB ETFClassifier (D_03/D_04), lib.exclusions ghost/insurance configs.

-- END OF CONTRACT --
