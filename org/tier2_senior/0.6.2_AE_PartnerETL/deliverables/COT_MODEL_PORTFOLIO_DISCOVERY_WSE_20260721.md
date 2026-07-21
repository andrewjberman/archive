# WS-E — Cottonwood Model-Portfolio DISCOVERY (findings + fold-in shape)

**Author:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-21 · **For:** 1.0.0_SA_CTO (WS-E fold-in design), CC 0.0.0_AB_MSTR / 2.0.0_SA_COO
**Mandate:** find WHERE Cottonwood marks Model Portfolios in Black Diamond, characterize the SHAPE + value/count representation, design the opal-data-assets daily fold-in. DISCOVERY ONLY (no build).
**Method:** LOCAL, cot READ-ONLY (Andrew grant @b5af1e929). All egress = cot session, GET/read only. Model list+detail data read from Andrew's own live-UI **HAR capture** (`rebalancer.bdreporting.com.har`) — no mutating call made by me.

---

## 0. TL;DR

- **The model portfolios are NOT in DataMining.** DataMining only exposes a sparse *assignment* dimension (`accountRebalStrategyID/Name`). The models themselves live in the **Black Diamond Rebalancer** app (`rebalancer.bdreporting.com`) → **StrategiesAndModels**.
- **Cottonwood has 60 models defined** in the Rebalancer (DataMining showed only ~2 because most accounts' assignment wasn't captured — the *models* exist regardless). **Scope = STRICT "Opal" in the name** (Andrew-direct 2026-07-21: *"If it doesn't say Opal in the name, then we should not be working with it."*). Non-Opal models (`Core | Satellite`, `Passive`, `529-F2`, fund-/client-named without "Opal") are **out of scope**.
- **Join key proven (exact GUID match):** DataMining `accountRebalStrategyID` **===** Rebalancer model `id`. `439fc4b6…` = **"Opal Satellite 80"**, `c973839d…` = **"Opal Long Term Conservatiove"** — the two GUIDs I found in landed cot allocations resolve exactly.
- **Shape = recursive hierarchy**: model → `hierarchy.children[]` (weighted sub-models/sleeves) → `components[]` (securities w/ symbol + weight). **Blend split = `children[].relativeAllocation`** (the underlying-primary-model weights, sum to 1.0).
- **Andrew's MDPF count-vs-dollar mechanism EXISTS in the data**: +1 count to each underlying primary model; dollar = `account_value × child.relativeAllocation`.
- **Auth pattern**: shared cot OIDC cookie jar (`blackdiamond/cot/session`) → mint a Rebalancer bearer at `GET rebalancer.bdreporting.com/auth/token`. Exercised (200).
- **Current cot AUA (fresh, from cot's own holdings 07-17): ~$437.1M / 845 accounts** — corrects the stale $372.9M/642 (06-09 backfill) I initially quoted.

---

## 1. Where the model is stored (the mechanism)

Black Diamond is a reporting aggregator with ~33 sibling apps under one OIDC realm (`*.bdreporting.com`). Model portfolios are owned by the **Rebalancer** app, confirmed three independent ways:

1. **App module map** (from the BD3 shell JS): `RebalancerModels:"rebalancer_models"`, `RebalancerStrategies:"rebalancer_strategies"`, `RebalancerPrograms:"rebalancer_programs"`, plus a Model Marketplace (`modelmarketplace`).
2. **Injected config** (`apiBase = https://rebalancer.bdreporting.com`; `rebalancerExternalApiBasePath = https://bd3.bdreporting.com/rebalancer/request`; `modelMarketplaceApiBasePath = https://api.bdreporting.com/ModelMarketplace`).
3. **Live traffic (HAR)** — the StrategiesAndModels UI page calls the endpoints in §3.

**DataMining is only a projection.** The DataMining `allocations` (qt5) query carries `Account Strategy Name/ID` (`mappedColumn accountRebalStrategyName / accountRebalStrategyID`) — that is the Rebalancer assignment surfaced as a reporting dimension. It is (a) sparsely populated in the landed data and (b) currently returning 0-row snapshots (the known cot snapshot as-of-date latent bug, `cot_bronze_ingest.py:92-93`). **It is not the source of model definitions or composition** — those never appear in DataMining at all.

## 2. Auth pattern (for the daily pull)

Identical multi-app pattern to DataMining (`AUTHENTICATION.md`):

- Root credential = the shared cot OIDC cookie jar in Secrets Manager `blackdiamond/cot/session` (established today by `cot_bd_session_fetch.py` on the cot-exporter EC2; querying works off-box).
- **Mint a Rebalancer bearer:** `GET https://rebalancer.bdreporting.com/auth/token` (Cookie-authed) → `{"access_token": "..."}`. **Exercised — 200.** (Each sibling app mints its own bearer; the DataMining bearer does NOT work here.)
- Use: `Authorization: Bearer <token>` on the `/api/*` calls in §3.
- TTL: same ~30–60 min effective session TTL; re-mint mid-run; re-pull the cookie on 401.

## 3. API surface (read endpoints)

Base host `https://rebalancer.bdreporting.com`. Observed live (HAR), all **read**:

| Purpose | Call | Body / notes |
|---|---|---|
| **List models/strategies** | `POST /api/models/strategies/search` | `{skip, take, totalResultCount, sort:[{field,isAscending}], searchString}` → paged roster. `totalResultCount = 60`. |
| **Model composition (detail)** | `GET /api/models/{modelId-GUID}` | full recursive hierarchy + components (§4). This is the model holdings/weights. |
| Teams (grouping) | `POST /api/teams/search` | pagination-shaped, same envelope. |
| Marketplace subscription | `POST https://api.bdreporting.com/ModelMarketplace/subscriptions/summary` | `{rebalanceModelId:[guid]}` (whether a model is a marketplace subscription). |

**Roster row shape** (`pagedResults[]`): `{id, name, displayName, accountCount, portfolioCount, relationshipCount, rebalanceAssignmentCount, team, teamExternalId, lastUpdate, rebalanceModelType, provider, aggregateManagedAccountsOnly, adminOnlyModel, isUmaStrategy}`.

`accountCount` / `rebalanceAssignmentCount` per model give the **assignment counts** directly (e.g. Opal Satellite 50 = 82 accts, Sat 60 = 79, Sat 80 = 54, Sat 70 = 39, Sat 40 = 16; several primary Opal models sit at 0 because they're used only as blend *building blocks*, not assigned directly).

## 4. Data shape — the recursive model hierarchy

`GET /api/models/{id}` →
```
{ modelType, isAssigned,
  hierarchy: {
    id, name, displayName, rebalanceModelType,      # "Strategy" at top
    relativeAllocation, absoluteAllocation,          # 1.0 at top
    toleranceBandOptions:{isRelative,maxTolerance,minTolerance},
    children: [                                      # weighted sub-models / sleeves
       { id, name, rebalanceModelType:"Model",
         relativeAllocation, absoluteAllocation,     # <-- THE BLEND / SLEEVE WEIGHT
         children:[...],                             # recursive
         components:[                                # securities (leaf)
            { name:"CDSIX - CALVERT SHORT DURATION INCOME I",
              metadata:{symbol:"CDSIX"},
              absoluteAllocation:0.058,              # weight in WHOLE model
              relativeAllocation:0.10,               # weight within this sleeve
              characteristics:[{value:"252125",name:"AssetId"}] }  # BD AssetId
         ] } ],
    components:[...], characteristics:[{value,name}] },
  team, teamExternalId, relationshipCount, portfolioCount, accountCount }
```

**Weight semantics:** `absoluteAllocation` = weight in the whole model (all leaf components sum to 1.0); `relativeAllocation` = weight within the immediate parent. `children[].relativeAllocation` sums to 1.0 across the children.

**Three observed hierarchy patterns:**
1. **Blend-of-primary-models** (the case Andrew cares about) — children ARE named primary Opal models. Live example, a blend strategy: children = `Opal Conservative Growth` (rel **0.4565**), `Opal Intermediate-Term` (rel **0.4565**), `Opal Ultra Short-Term Income` (rel **0.087**). A client-custom blend: `Opal Conservative Growth` (0.79) + `Opal Ultra Short-Term Income` (0.21).
2. **Asset-sleeve model** — children are asset sleeves (`Sleeve - Bond/Equity/Money Market`), each holding fund components. Not a blend of primary models.
3. **Flat model** — no children; `components[]` directly (e.g. 20 securities).

## 5. The join to DataMining / landed data

- `DataMining accountRebalStrategyID` (GUID) `===` `Rebalancer model.id`. Proven by exact match on the only 2 assigned GUIDs present in landed cot allocations.
- Account → model assignment is thus available two ways: (a) DataMining `allocations` `account_strategy_id` (sparse + currently 0-row — needs the snapshot as-of fix), or (b) the Rebalancer's own per-model `accountCount` / an assignment endpoint (not yet enumerated — the roster gives counts; a per-account assignment list is the remaining discovery item, §8).
- Account **dollar value** comes from the existing cot feeds: `allocations.account_market_value` (per-account, once the as-of bug is fixed) or `holdings.market_value` summed per account (fresh: 07-17).

## 6. Answering the MDPF Model-Portfolios count-vs-dollar requirement

Andrew's rule: a blended account counts **+1 in each underlying model**, but its **dollars split by the blend weights**. This maps cleanly onto §4:

For an account assigned model `M` with value `V`:
- Resolve `M` via the join key, `GET /api/models/{M}`.
- **If `M`'s children are primary models** (name-startswith "Opal" / `rebalanceModelType=="Model"` and the child resolves to a primary-model id): for each child `c` — **count += 1 for model `c.name`**, and **dollars for `c.name` += V × `c.relativeAllocation`**.
- **If `M` is a single (non-blend) model** (asset-sleeve or flat): **count += 1 for `M`**, **dollars for `M` += V** (full).
- Aggregate across all assigned accounts → per-primary-model `{account_count, dollar_value}` = the MDPF page rows.

The **clear mechanism Andrew asked for exists**: `children[].relativeAllocation` is the blend split, and `child.name`/`child.id` identifies the underlying primary model. (Nested blends recurse.)

## 7. opal-data-assets fold-in — ALIGNED to the estate taxonomy (OPAL_CONSOLIDATION_TAXONOMY_STANDARD §A/§D; grounded 2026-07-21, read-only)

**Prefix (grounded, firm-clean):** the Rebalancer is a Black Diamond app → the model data is BD-sourced / cot-scoped, so it lands under the EXISTING cot BD scope:
`s3://opal-data-assets/blackdiamond/cottonwood/{layer}/{type}/{date}` — the SAME source/scope as cot's existing allocations/holdings/realized/unrealized/transactions.
**There is no top-level `cot/` source and one must NOT be created.** cot is a SCOPE under the `blackdiamond` source, exactly like `blackdiamond/49f`, `schwab/{acct}`, `smartx/{feed}`, `eclipse/inflection`, `orion/inflection` (grounded: the six live sources are blackdiamond/eclipse/orion/pathfinder/schwab/smartx/trueshares; `blackdiamond/` scopes = `49f` + `cottonwood`). A separate `cot/` root would fragment cot's BD data across two prefixes and break the cross-firm taxonomy consistency Andrew required. **Firm-sep by scope segment:** the producer writes ONLY `blackdiamond/cottonwood/**`, never `blackdiamond/49f/**` (scope discipline, mirroring `cot_bronze_ingest._assert_firm_separation` + IAM deny).

**Layers** (grammar `{source}/{scope}/{layer}/{type|feed}/{date}`, `{layer}∈bronze|silver|gold|meta`, §A):
- **bronze/** — raw BD Rebalancer JSON, byte-for-byte (Rule 17a; parquet begins at silver): `bronze/rebalancer_models/MODELS_{date}.json` (roster) + `bronze/rebalancer_model_detail/{modelId}_{date}.json` (per-model composition). Mirrors the existing `bronze/{type}/…` raw landing.
- **silver/** — parquet `fact_{type}` COMPLETE tables, dedup + dtype ONLY (Rule 17):
  - `silver/fact_model_definition/date=…/data.parquet` — one row per model × leaf-component (model_id, model_name, is_opal, rebalance_model_type, sleeve_name, symbol, asset_id, absolute_allocation, relative_allocation).
  - `silver/fact_model_blend/date=…/data.parquet` — model_id → child primary-model-id + relative_allocation (the blend split, §6).
  - `silver/fact_model_assignment/date=…/data.parquet` — account_id → model_id (source = Rebalancer-authoritative, §9(1)).
- **gold/** — `dim_*` projections (gold = the one parse-down point): `gold/dim_model_portfolio/` → the MDPF DDB fold-in: per in-scope Opal model `{account_count (+1 per blend membership), dollar_value (Σ account_value × relative_allocation)}` (§6). `blackdiamond/cottonwood/gold/` is currently EMPTY = the target.
- **meta/** — pull provenance to `meta/pulls/{YYYYMMDD}/` (§D) + `meta/conversions/` + a `*-complete.json`/`*-failed.json` stamp pair; NEVER data (mirrors the existing `cottonwood/meta/` + `backfill-status.json`).

**Trigger + implementation (mirror the estate, §D — don't improvise siblings):** follow the existing `opal-assets-bd49f-*` BD producer (already lands `blackdiamond/cottonwood/` BD data): EventBridge-scheduled producer named `{unit}-{function}-{cadence}` (e.g. `opal-assets-bd-rebalancer-daily-pull`); HTTP = requests.Session + urllib3 Retry (C5 `smartx_client`); landing verified by the listing-based set-identity guard (`landing_guard.py` / `mirror_conversion.set_identity`, ListObjectsV2 run-time denominators — never HeadObject); bronze-complete stamp → EventBridge → silver → gold `dim_*` → DDB. Auth = mint the Rebalancer bearer from `blackdiamond/cot/session` (§2). IAM = one scoped `{resource}-role`, scope-exact grants verified per Rule 22a (exact-ARN `simulate-principal-policy` + isolated positive control), PAB-on, firm-sep deny to `blackdiamond/49f`.

**Absence-twin:** §D's target-state law pairs a freshness/absence twin, but NEW SNS/CloudWatch alert creation is **ENFORCEMENT-PAUSED** for the consolidation (Andrew 07-17) — so **no new alarm ships with this**; the twin is noted as deferred target-state.

Still discovery/design only — the build is cloud-side + CTO-gated (the WS-E PRD).

## 8. Open items / caveats (grounded)

- **Per-account → model assignment list — RESOLVED 2026-07-21 (see §11).** Enumerated by scoped live read-only (Andrew egress word 2026-07-21T192455Z @3e563306c): `POST /api/accounts/search`. The `//` below is now historical: ~~the roster gives per-model *counts*; the explicit account→model list still needs one endpoint~~.
- **DataMining allocations feed is 0-row for recent dates** (snapshot as-of latent bug) — the model *assignment via DataMining* is currently frozen at the 06-09 backfill. The Rebalancer API is the fresher/authoritative model source; assignment freshness is the item to resolve for a production daily.
- **Name-filter — RULED (Andrew-direct 2026-07-21):** STRICT. *"If it doesn't say Opal in the name, then we should not be working with it."* Non-Opal products (`Core | Satellite XX`, `Passive XX`, `529-F2`, fund-/client-named without "Opal") are **out of scope** — the fold-in filters to `name LIKE '%Opal%'`. Deeper investigation into whether any non-Opal existing portfolios are silently changing is a **post-launch, non-priority, non-blocker** follow-up ("after this is cleanly incorporated and running smoothly in MDPF for Cottonwood… I doubt that is the case though"). Do NOT gate or expand the launch on it.
- **Primary building-block models** (`Opal Conservative Growth`, `Opal Intermediate-Term`, `Opal Ultra Short-Term Income`, …) are referenced as blend children and may be a distinct set from the *assignable* roster (`rebalanceModelType`: Strategy vs Model) — the fold-in should build the primary-model dimension from the union of children + the roster.
- **Client-custom blend models** (named per client) exist (~a handful); their children ARE primary Opal models, so §6 handles them uniformly.

## 9. CTO disposition of §8 open items (resolved 2026-07-21, no new egress — HAR + landed data)

**(2) Roster partition — STRICT Opal filter (Andrew-ruled).** 60 models → **17 in scope / 43 out**. `Opal Satellite NN` and `Core | Satellite NN` are **DISTINCT families**, so the strict `name ILIKE '%opal%'` filter cleanly separates them (no residual ambiguity):
- **IN (17 models, 296 assigned accts):** Opal Satellite 50 (82), 60 (79), 80 (54), 70 (39), 40 (16), 98 (12), 30 (4), 90 (0); Opal Long Term Conservatiove (0), Opal Long Term Aggressive (0), Opal - Income (2), Opal Ultra Short Term (3), Opal 66% Long Term / 34% UST (1), Opal UST/ Sat 70 (1), Opal - Cash + Satellite 50 (1), Opal - Beecherl Legg (1, client blend), Blended Opal / Satellite 50 (1).
- **OUT (43):** Core\|Satellite family (16 models / 106 accts), Passive (9 / 20), 529-F2 American Funds (5 / 0), other client-named/fund-specific (13 / 24).

**(1) Account→model assignment source — REBALANCER is authoritative; DataMining path insufficient.** The DataMining `accountRebalStrategyID` dim **structurally under-reports**: the last non-frozen allocations (06-09) showed **2** assigned accounts; the Rebalancer shows **296** across the 17 Opal models today. Cause (real assignment growth June→now vs dim under-capture) is **UNVERIFIED** — resolvable only by a fresh non-frozen allocations pull reconciled against the Rebalancer counts. **Recommendation:** source account→model from the **Rebalancer** (system of record, current, internally consistent). The DataMining snapshot-freeze fix is worth doing for the cot allocations table's own freshness + as a reconciliation check, but should NOT be the primary account→model source until proven to match Rebalancer counts. The explicit per-account list needs one Rebalancer endpoint not yet captured (an account-assignments / model-accounts view) — one more HAR from Andrew, or a scoped live read (fresh word). Dependency: the assignment-endpoint capture (primary) and/or the cot snapshot zero-row freeze workstream (the true-reading 18-day issue — **do not close**).

**(3) Strategy vs Model — §6/§7 confirmed + union nuance.** §7 sources assignments against the ASSIGNABLE roster (`rebalanceModelType=Strategy`); §6 decomposes blend strategies to their primary building-block children (`rebalanceModelType=Model`) via `children[].relativeAllocation`. **MDPF row set** = {assignable Opal models that aren't pure primary-model blends} ∪ {primary Opal building-blocks a blend decomposes into} — the fold-in builds the primary-model dimension from the **union** of the roster + the blend children. §7 covers the decomposition; the union-set construction is flagged for the PRD.

## 10. Compliance

cot READ-ONLY + LOCAL throughout; zero writes; zero cross-firm (never read the `blackdiamond/49f` partition even in opal-data-assets). Model list/detail came from Andrew's HAR, not a POST of mine. Live rotating BD cookie kept in-memory only — never logged, echoed, or committed. Discovery only — no fold-in built (CTO-gated, cloud-side).

---

## 11. Per-account → model ASSIGNMENT endpoint — RESOLVED (scoped live read-only)

**Provenance:** Andrew-direct egress word **2026-07-21T192455Z** (verbatim recorded @3e563306c). Method = WS-E discovery method: cot READ-ONLY + LOCAL, minted the Rebalancer bearer off the cot OIDC session (`blackdiamond/cot/session`, still live — bearer 200 this session), GET + read-shaped `/search` POST only. Zero mutating calls, zero writes, firm-clean (zero `blackdiamond/49f`). CTO carried this as the account-source decision (fresh HAR vs scoped live read → Andrew chose the scoped live read).

**THE ENDPOINT:** `POST https://rebalancer.bdreporting.com/api/accounts/search`
- **Auth:** `Authorization: Bearer <token>` from §2 (`GET /auth/token`).
- **Body:** `{"skip":<int>,"take":<int>,"sort":[],"searchString":""}` (same paged envelope as strategies/search; `take=200` works).
- **Response:** `{pageCount, pageNumber, totalResultCount, pagedResults[]}`. **Full cot book = 910 accounts** (paginate skip/take).
- **NO server-side model filter** — tested `modelId / rebalanceModelId / strategyId / modelIds / rebalanceModelIds / filters / assignedModelId`; **every variant returned the full 910** (ignored). Assignment is carried **per row**, filtered client-side.

**Account-row schema (22 fields);** assignment + fold-in-relevant subset:
`accountId` (8-digit internal BD id) · **`externalId`** (`"z09"`+accountId, 11-char — the value-join key) · `name` · `accountNumber` · **`strategyName`** · `programName` · `taxStatus` · `custodianId` · `accountType` · `isManaged` · `canRebalance` · `isClosed` · `discretionary` · `allowSMA` · `isSMA` · `isUmaSleeveAccount` · `isSystemSleeve` · `isRebalancerUma` · `isInRebalanceGroup` · `exclude`.
- **`strategyName` = the assigned Rebalancer strategy/model NAME** (unassigned = `"--"`). **No strategy GUID on the row** → the account→model.id join is by NAME.

**Join account→model.id (1:1, COMPLETE):** `accounts/search.strategyName → roster.name → model.id` (via §3 `POST /api/models/strategies/search`).
- Roster = **60 models / 60 distinct names / 0 duplicate names** → name→id is unambiguous.
- The **43 assigned strategyNames have 0 orphans** — every assigned name resolves in the roster; no account maps to a strategy outside it.

**VALIDATION (the sharp cross-check):** the full-sweep per-strategy account counts **reproduce the roster `accountCount` EXACTLY for every Opal model** — Sat50=82, Sat60=79, Sat80=54, Sat70=39, Sat40=16, Sat98=12, Sat30=4, Ultra Short=3, Income=2, + 5 low-count (Beecherl Legg / 66%LT-34%UST / Cash+Sat50 / UST-Sat70 / Blended-Sat50 each 1) = **296 Opal-assigned accounts across 14 assigned Opal models** = the roster union. → `/api/accounts/search` **IS the authoritative account→model source** (system-of-record, current, internally consistent). It **supersedes DataMining** (2 accts, structurally under-reports; §9(1)). Non-Opal (`Core | Satellite` 100+, `Passive`, fund-named) correctly excluded by the strict Opal filter.

**SMA/sleeve flags — ALL ZERO across the 296 Opal-assigned accounts** (`isSMA=0, allowSMA=0, isUmaSleeveAccount=0, isSystemSleeve=0, isRebalancerUma=0`; `canRebalance=296`). **Cottonwood Opal has NO SMA/UMA sleeve accounts** — the MDPF-revamp SMA-sleeve filtering that applies elsewhere has **nothing to filter here**; every Opal assignment is a single direct rebalancer-strategy assignment, one strategy per account. → the "client holds multiple sleeves" concern does NOT arise for Cottonwood Opal; the +1-count / split-dollars is driven **solely** by the assigned strategy's blend `children[]` (§6), not by multiple account assignments.

**Value join — CONFIRMED (cot data-plane, off-rail-legal):** account VALUE comes from cot **holdings** silver (`s3://opal-data-cot/silver/holdings/{date}.parquet`, **fresh through 2026-07-17** — holdings is a period table, unaffected by the snapshot freeze on allocations/unrealized). Its **`account_id` column = the `"z09"`-prefixed 11-char id = EXACTLY the Rebalancer `externalId`** → **join key: `accounts/search.externalId === holdings.account_id`.** Σ `market_value` per account_id = account value. (holdings also carries `portfolio_id`, `relationship_id`, `account_number`, `asset_id/symbol/cusip`, `units`.)

**COMPLETE MDPF fold-in chain (no further live read required):**
1. `POST /api/accounts/search` (paginate 910) → per account: `externalId`, `strategyName`.
2. Strict Opal name-filter on `strategyName`; map name → `model.id` via roster.
3. `GET /api/models/{model.id}` → composition + blend `children[].relativeAllocation` (§4/§6).
4. cot holdings silver (`account_id == externalId`) → Σ `market_value` = account value.
5. Andrew rule: blend strategy → **+1 count** per underlying primary model, **dollars = account_value × child.relativeAllocation**; single (non-blend) strategy → +1 count + full dollars to that model. (Nested blends recurse.)
6. → `gold/dim_model_portfolio` per in-scope Opal model `{account_count, dollar_value}` → MDPF DDB.

**Necessary endpoints for the MDPF work — COMPLETE SET:**

| Endpoint | Purpose | Status |
|---|---|---|
| `GET rebalancer.bdreporting.com/auth/token` | mint Rebalancer bearer (off cot OIDC session `blackdiamond/cot/session`) | known |
| `POST /api/models/strategies/search` | model roster: name↔id, per-model counts, type (Strategy/Model) | known |
| `GET /api/models/{id}` | model composition + blend `children[].relativeAllocation` | known |
| **`POST /api/accounts/search`** | **account → model assignment (`strategyName` per account) + full 910-account book** | **NEW (this session)** |
| cot **holdings** silver (S3, `opal-data-cot/silver/holdings/`) | per-account `market_value` (join `externalId == account_id`) | existing feed |

(`POST api.bdreporting.com/ModelMarketplace/subscriptions/summary` = marketplace-subscription flag; **NOT needed** for MDPF.)

**Negative finding (so the build doesn't chase it):** the model-scoped GET paths `/api/models/{id}/accounts`, `/assignments`, `/relationships`, `/portfolios`, `/managedaccounts`, `/detail`, and `/api/strategies/{id}/accounts` all return the **SPA shell (200 `text/html`, 131,461 B)** — they are NOT real API routes (the catch-all fallback). `POST …/accounts/search` on model-scoped paths → 405. The authoritative path is the **full-book `/api/accounts/search`** + client-side `strategyName` filter — which is also what the Rebalancer UI does. `POST /api/relationships/search` exists but is 403 (permission-scoped; not needed).
