# WS-E — Cottonwood Model-Portfolio DISCOVERY (findings + fold-in shape)

**Author:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-21 · **For:** 1.0.0_SA_CTO (WS-E fold-in design), CC 0.0.0_AB_MSTR / 2.0.0_SA_COO
**Mandate:** find WHERE Cottonwood marks Model Portfolios in Black Diamond, characterize the SHAPE + value/count representation, design the opal-data-assets daily fold-in. DISCOVERY ONLY (no build).
**Method:** LOCAL, cot READ-ONLY (Andrew grant @b5af1e929). All egress = cot session, GET/read only. Model list+detail data read from Andrew's own live-UI **HAR capture** (`rebalancer.bdreporting.com.har`) — no mutating call made by me.

---

## 0. TL;DR

- **The model portfolios are NOT in DataMining.** DataMining only exposes a sparse *assignment* dimension (`accountRebalStrategyID/Name`). The models themselves live in the **Black Diamond Rebalancer** app (`rebalancer.bdreporting.com`) → **StrategiesAndModels**.
- **Cottonwood has 60 models defined** in the Rebalancer (DataMining showed only ~2 because most accounts' assignment wasn't captured — the *models* exist regardless). Ours = **"Opal" in the name** (Andrew's rule).
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

## 7. Proposed opal-data-assets daily-strategy fold-in (design only — CTO-gated build)

Firm-separated, additive (NEW-TERRITORY rule), read-only pull. Sketch:

1. **New bronze producer** (cloud-side, cot-scoped, mirrors `cot_bronze_ingest.py`'s Model-B env pattern): mint the Rebalancer bearer → `POST /api/models/strategies/search` (paged, all 60) → for each `id`, `GET /api/models/{id}` → land **raw JSON byte-for-byte** under `blackdiamond/cottonwood/bronze/.../rebalancer_models/{date}/` (Rule 17a: raw, no parquet-at-ingest).
2. **Silver**: flatten to two `fact_*` tables — `fact_model_definition` (one row per model × leaf-component: model_id, model_name, is_opal, rebalance_model_type, sleeve_name, symbol, asset_id, absolute_allocation, relative_allocation) and `fact_model_blend` (model_id → child primary-model-id + relative_allocation) — plus `fact_account_model_assignment` (account_id → model_id, from the assignment source in §5/§8).
3. **Gold / DDB fold-in into `opal-assets-daily-aua`**: per primary Opal model, `{account_count (distinct, +1-per-blend-membership), dollar_value (Σ account_value × relative_allocation)}`, keyed for the MDPF Model-Portfolios page. Dollar attribution uses §6.

Guardrails carried: cot-only (never blackdiamond/49f), read-only, raw bronze, Opal-name filter for "ours", the DataMining as-of fix is a prerequisite if the assignment source is `allocations` (else use the Rebalancer assignment source).

## 8. Open items / caveats (grounded)

- **Per-account → model assignment list**: the roster gives per-model *counts*; the explicit account→model list still needs one endpoint (candidate: a Rebalancer assignments endpoint, or fix + use DataMining `allocations` `account_strategy_id`). Not yet enumerated (would benefit from an assignments page in the HAR, or a scoped live read with a fresh word).
- **DataMining allocations feed is 0-row for recent dates** (snapshot as-of latent bug) — the model *assignment via DataMining* is currently frozen at the 06-09 backfill. The Rebalancer API is the fresher/authoritative model source; assignment freshness is the item to resolve for a production daily.
- **Name-filter ambiguity**: Andrew's "Opal in the name = ours" cleanly tags the primary Opal models, but there are Opal-style products without "Opal" in the name (`Core | Satellite XX`, `Passive XX`). Flagging for Andrew's disambiguation whether those count as ours.
- **Primary building-block models** (`Opal Conservative Growth`, `Opal Intermediate-Term`, `Opal Ultra Short-Term Income`, …) are referenced as blend children and may be a distinct set from the *assignable* roster (`rebalanceModelType`: Strategy vs Model) — the fold-in should build the primary-model dimension from the union of children + the roster.
- **Client-custom blend models** (named per client) exist (~a handful); their children ARE primary Opal models, so §6 handles them uniformly.

## 9. Compliance

cot READ-ONLY + LOCAL throughout; zero writes; zero cross-firm (never read the `blackdiamond/49f` partition even in opal-data-assets). Model list/detail came from Andrew's HAR, not a POST of mine. Live rotating BD cookie kept in-memory only — never logged, echoed, or committed. Discovery only — no fold-in built (CTO-gated, cloud-side).
