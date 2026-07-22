# Cottonwood Operational Shape — how to get the 49F/Inflection account-membership+size pattern from Black Diamond

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer · **Date:** 2026-07-22
**Commissioned:** Andrew-direct — get for Cottonwood/BD the shape we get for 49F via SmartX and Inflection via
Eclipse: *"what clients have holdings with what models and what is the size of those accounts so that we can
get the account bell curve size distribution, daily holdings count, etc."*
**Tools used (comp-rail):** `comp-which` → `comp-cache map` → `comp-cluster ModelPortfolios` → `comp-grep`,
`pipescript`. Live cot-BD reads under Andrew's standing egress approval (read-only).
**Route:** `1.0.0_SA_CTO` → **folds into `MDPF_3FIRMS`** (Andrew-direct 2026-07-22 — *not* WSE_COTMDL; the
sourcing + backfill briefs already fold into MDPF_3FIRMS PRD v1.1/v1.2, and this operational-shape brief joins
them there). Nothing dispatches under LD-0333 until Andrew's word.

> **The reframe, and it resolves the "surely BD can do this":** **BD CAN, and it already does — proven live
> below.** The operational shape you want (bell curve, size distribution, holdings count, membership) is
> **CURRENT-STATE**, and it needs **no history at all** — the bell-curve producer's own docstring says
> *"account-size distribution — no historical/backfill question."* My prior backfill deep-dive was answering a
> strictly harder question (the AUM *timeseries*) than this target requires. **These are two separate
> deliverables; only the timeseries has a backfill problem.**

---

## 1. PROVEN — the full operational shape, computed from Cottonwood/BD today **[PROVEN]**

From the exact (account × model × size) triple (rebalancer `accounts/search` membership × monolith
`fact_holdings` value, 296/296 join):

```
ACCOUNT-SIZE BELL CURVE (296 Opal accounts, 2026-07-20)      DAILY HOLDINGS COUNT
  <$100K       98  ################################          per account: min 2 / median 37 / max 50
  $100-250K    74  ########################
  $250-500K    45  ###############             percentiles: p10 $36,832 | median $204,514
  $500K-1M     44  ##############                            p90 $1,146,569 | max $4,475,340
  $1-2.5M      32  ##########
  >$2.5M        3  #                            BY MODEL: Sat-50 82 accts avg $421K | Sat-60 79 avg $396K
                                                          Sat-80 54 avg $360K | Sat-70 39 avg $446K ...
```

**This is the 49F/Inflection shape, produced from Black Diamond. Nothing operationally essential is missing.**

---

## 2. The target contract — what the portal actually consumes **[GROUNDED, via comp-cluster]**

`comp-cluster ModelPortfolios` resolves the page's panel cluster to these served artifacts. **Andrew confirmed
the page structure (2026-07-22), and it maps cleanly onto the current-vs-historical split:**

| Portal location | Artifact | Nature |
|---|---|---|
| **"Portfolio Analytics" header** | **`json/portfolios/aum-metrics.json`** (`by_model` current AUM weights) | **CURRENT SNAPSHOT** |
| **"Portfolio Analytics" header** | **`json/portfolios/account-distribution.json`** (the bell curve / size dist) | **CURRENT SNAPSHOT** |
| **AUM tab** | **`json/portfolios/aum-timeseries.json`** (the line chart) | **HISTORICAL — the only backfill element** |
| (supporting) | `non_model_assets.json`, benchmarks, peers | — |

**The two Portfolio-Analytics-header artifacts are both current-snapshot — Path A builds both now. The backfill
question is confined entirely to the AUM-tab timeseries.** Every firm renders through the **same** contract,
keyed by `firmOverride` (`comp-cache map`: `advisor-book-account`, `firm-leaderboard`, ... all `firmOverride`).
**Adding Cottonwood = emitting these JSONs under `firmId=cottonwood`.**

---

## 3. How the existing firms build it — and why Cottonwood is the same pattern **[GROUNDED]**

`data/smartx/scripts/compute_per_firm_account_distribution.py` builds `account-distribution.json` for both:

| Firm | Source feed (the account × model × size triple) |
|---|---|
| **49financial** | `opal-data-smartx-v2/consolidated/smartx_allocations.parquet` — SmartX `enterprises/allocations` (account, model, value in ONE feed) |
| **inflection** | `opal-data-inf/gold/eclipse/{latest}/model_portfolio_accounts.parquet` — Eclipse per-account model + value |

And the MDPF_REVAMP producer `dim_mdpf_account_distribution.py` reads it from the **monolith**:
`fact_allocation_valuation.equity` (size) + `fact_model_allocation_roster` (membership).

**Cottonwood's monolith silver ALREADY carries the equivalents** (`aws s3 ls` — proven present):
`fact_model_assignment` + `fact_model_roster` (membership), `fact_holdings` + `fact_allocations` (size),
`fact_model_blend` (the Satellite→archetypal crosswalk). **The inputs exist. The producer exists. The contract
exists. This is a third-firm wiring, not a new capability.**

---

## 4. The ONE structural difference between BD and SmartX/Eclipse — and it is bridged

**SmartX and Eclipse hand you (account, model, value) in a SINGLE feed. Black Diamond SPLITS it:**
membership lives on the rebalancer (`accounts/search.strategyName`), value lives in holdings/DataMining.
**Confirmed live:** `clientReview/accounts/search` carries `strategyName` but has **no value field** (22
fields, none a size) — so there is no one-call BD analog of SmartX `enterprises/allocations`.

**This is the entire "gap," and it is already closed:** the monolith join (`fact_model_assignment` ×
`fact_holdings` on the `z09` external id) reunites them — **296/296, proven, and it reproduces CTO's gold
`dim_model_portfolio` to the dollar.** BD isn't missing the data; it distributes it across two services, and
our silver already re-joins it.

---

## 5. Brainstorm — the paths to deliver it, ranked

**PATH A — near-term, recommended: point the existing distribution producer at Cottonwood's monolith facts.**
`fact_model_assignment`/`fact_model_roster` (membership) × `fact_holdings`/`fact_allocations` (size), apply the
`fact_model_blend` Satellite→archetypal crosswalk (CTO's WS-3 builder already does this), emit
`json/mdpf/cottonwood/account-distribution.json` + the non-model + count fields. **Same producer, same
contract, third firm. No history, no probe, no new egress — the bell curve is current-state.** This is the
whole of your operational ask, buildable now.

**PATH B — alternative single-source (if we want to avoid the rebalancer×holdings join):** the DataMining
**qt5 allocations** query with the **Account-strategy dimension** selected returns account MV **and** strategy
in one query, and it is **date-windowed** — so it could serve both the current distribution AND (if the
strategy dimension proves temporal) the backfill in one path. This is the same DataMining probe from the
backfill brief, here doing double duty. Worth running regardless.

**PATH C — the daily holdings COUNT** is trivial from `fact_holdings` (holding rows per account per day —
§1 shows it). No new source.

**Explicitly NOT needed for the operational shape:** the rebalancer date-injection (measured dead end), the
sessions/blotter history (empty), and any backfill. Those belong only to the *timeseries*, §6.

---

## 6. Keep the two deliverables separate — this is the key to not over-scoping

| Deliverable | Portal location | Nature | Status |
|---|---|---|---|
| **aum-metrics.json** (current AUM weights) | Portfolio Analytics header | **CURRENT-STATE** | **Buildable NOW** — Path A, no history. |
| **account-distribution.json** (bell curve, size dist, holdings count, membership) | Portfolio Analytics header | **CURRENT-STATE** | **Buildable NOW** — Path A. §1 proves the data. |
| **aum-timeseries.json** (the model-AUA line chart) | AUM tab | **HISTORICAL** | Forward-only clean from ~07-21; backfill gated on the DataMining temporal probe; ~05-28 structural ceiling (backfill brief). |

**Andrew-confirmed 2026-07-22:** the Portfolio-Analytics-header artifacts (aum-metrics + distribution) are both
current snapshot; the backfill is *only* the AUM-tab timeseries chart. **The operational shape you asked for is
the first two rows, and it does not wait on the third.** Conflating them is what made BD look deficient — the
current-state book is complete; only the historical *line* is migration-bounded.

---

## 7. Recommendation

Wire Cottonwood into the existing `account-distribution.json` producer from its monolith facts (Path A) — a
near-term, no-egress, no-backfill build that gives Andrew the bell curve, size distribution, holdings count,
and per-model membership at 49F/Inflection parity. Run the DataMining qt5-allocations probe (Path B) in
parallel — it is the single query that could also unlock the timeseries backfill. Everything is grounded;
nothing dispatches under LD-0333 until Andrew's word.
