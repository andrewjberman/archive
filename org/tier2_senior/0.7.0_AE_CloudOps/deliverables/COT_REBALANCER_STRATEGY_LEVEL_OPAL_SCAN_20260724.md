# Cottonwood Black Diamond Rebalancer — Scanning Strategies for Opal Model Holdings

**Author:** 0.7.0_AE_CloudOps
**Date:** 2026-07-24 (~1950Z)
**Requested by:** Andrew (direct)
**Type:** Read-only research / findings for the record
**Data vintage:** `opal-data-assets`, `blackdiamond/cottonwood/bronze/…` as-of **2026-07-24** (roster + accounts + 25 model-details); source at repo HEAD.

> **Method + pause note.** This scan is entirely read-only: landed S3 artifacts + source. **No live Black Diamond
> calls were made, no Lambda was invoked, no scope was changed, no message was sent** — the Andrew-direct fabric
> pause (~1943Z) is intact. Nothing here was committed under the pause without word; the report was authored as a
> file first.

---

## 0. The question

For Cottonwood, we draw on the Black Diamond **Rebalancer** endpoint. Some **Strategies** on that endpoint hold
**Opal Models** but were missed initially **because they do not have "Opal" in the Strategy name** (e.g. *Anna
\*9237*, *Moderate Income Portfolio*). Andrew asked:

1. Is there a mechanism to **scan strategies for Opal Model holdings**?
2. Can we track assets **both** at the aggregate **Opal-model** level **and** at the **"Strategy"** level?
3. Can we **find more** strategies that hold Opal models underlying (beyond the 18 supplied)?

---

## 1. How we draw on the Rebalancer endpoint today

`cot-rebalancer-runner` (Lambda `cot-rebalancer-runner`, daily; `MODEL_DETAIL_SCOPE=opal_closure` confirmed on
the deployed function) pulls three types from `https://rebalancer.bdreporting.com` and lands them raw under
`blackdiamond/cottonwood/bronze/`:

| Type | Endpoint | Content | Coverage today |
|---|---|---|---|
| **Roster** | `POST /api/models/strategies/search` | every strategy: `name ↔ id ↔ accountCount` | **RAW-COMPLETE — 60 strategies** |
| **Accounts** | `POST /api/accounts/search` | every account + its `strategyName` (the assignment) | **RAW-COMPLETE — 912 rows** |
| **Composition** | `GET /api/models/{id}` | the blend tree: `children[].relativeAllocation` | **SCOPED — 25 of 60** |

**Key modeling fact:** on this endpoint a **"Strategy" *is* a model in the roster** (the roster endpoint is
literally `/models/strategies/search`). An "Opal Satellite" strategy is a blend model whose children are other
models; an underlying "Opal Model" is a leaf model. So "scanning a Strategy for Opal Models" = walking a
strategy's composition tree and testing whether any (transitive) child is an Opal model.

---

## 2. The mechanism exists — but it is name-gated, by design, and that is the gap

The composition pull runs in scope **`opal_closure`**, which:

- **seeds only on strategies whose *name* contains "opal"** — `_is_opal(name) → "opal" in name.lower()`
  (`cot-rebalancer-runner/lambda_function.py:275,303`), then
- walks **downward** into their children transitively (`_child_model_ids`, `:279-293,316-319`) — **never upward**.

**Consequence (the exact defect Andrew described):** a strategy that *holds* an Opal model but is *not named*
"Opal" is structurally invisible — it is never seeded, and closure never climbs up to it. Its composition is
never pulled, so nothing links it to the Opal models inside it.

**This is not a bug — it is a faithful implementation of a prior ruling.** Andrew-direct 2026-07-21, verbatim
(`org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/COT_MODEL_PORTFOLIO_DISCOVERY_WSE_20260721.md:12,153`):
> *"If it doesn't say Opal in the name, then we should not be working with it."*

That same discovery doc explicitly **deferred** the present question as a post-launch, non-blocking follow-up:
> *"Deeper investigation into whether any non-Opal existing portfolios are silently changing … after this is
> cleanly incorporated and running smoothly … I doubt that is the case though."*

**The current request activates that deferred follow-up and overturns the "I doubt that is the case" —** the
named examples (Anna, Moderate Income Portfolio) are strategies holding/likely-holding Opal models without the
name. **The change is therefore a scope decision, not a code fix.**

The capability to do the scan already exists in the code:
- the runner supports **`MODEL_DETAIL_SCOPE=all`** (`:70,300-301`) — pull `GET /api/models/{id}` for *every* roster model;
- the silver parser **`_walk_hierarchy`** (`data/assets/scripts/silver/rebalancer_conversion.py:244-296`) already
  decomposes *any* blend tree by `relativeAllocation` regardless of name; the strict-Opal filter is a downstream
  **label**, applied at gold, not a pull-time gate.

It is a **switch + a reverse-attribution**, not a build.

---

## 3. Strategy-level assignment is ALREADY captured; strategy-level *assets* need one join

Every one of the **912** account rows carries `strategyName` — including the **non-Opal-named** strategies. So we
already have strategy-level *assignment* for all 60 today. Non-Opal strategies with assigned accounts (2026-07-24):

| accounts | strategy (non-Opal-named) |
|---:|---|
| 23 | Core \| Satellite 50 |
| 17 | Core \| Satellite 60 |
| 14 | Core \| Satellite 70 |
| 12 | Core \| Satellite 80 |
| 11 | Janus Henderson Balanced Fund Class I (JBALX) |
| 10 | Core \| Satellite 40 · Core \| Satellite 98 · Passive 80 |
| 6 | Passive 70 |
| 5 | Core \| Satellite 30 · Core \| Satellite Tax-Free 70 |
| **4** | **Moderate Income Portfolio** |
| 3 | Core \| Satellite CA Tax-Free 80 |
| 2 | Core \| Satellite Tax-Free 50 · CSTF50 Moderate G&I - Harris · Core \| Satellite CA Tax-Free 70 · Passive 60 |
| 1 | **Anna \*9237** · **Anna \*9238** · Core / Satellite Equity · CSTF40 Conservative G&I - Gillham · JBALX and FCNTX 80/20 · Eartha Vaughan IRA · Hendrickson Trust · Pena - Conservative · Core \| Satellite Tax-Free 30/40 · Passive 50/98 |

The **"Core \| Satellite" family alone is ~86 accounts** — larger than several in-scope Opal strategies — and its
Opal content is currently invisible.

**Assets (dollars) caveat:** the accounts endpoint row has **no $ value field** (only booleans:
`canRebalance`, `isRebalancerUma`, …). Strategy-level **AUM** must come from joining these accounts to the
holdings/allocations feeds by `accountId`. That join is already proven for the Opal set (discovery reconciled
**$126,381,228.86** across the 296 Opal-assigned accounts to within $0.02). It simply is not wired for the
non-Opal strategies yet.

---

## 4. The 18 supplied Strategies, reconciled against the live roster (60 total)

**14 already in scope** (Opal-named, composition landed today):

| Strategy | accts | Composition (from landed detail) |
|---|---:|---|
| Opal Satellite 30 | 4 | Opal Intermediate-Term 25% · Opal Short-Term 75% |
| Opal Satellite 40 | 16 | Opal Intermediate-Term 50% · Opal Short-Term 50% |
| Opal Satellite 50 | 82 | Opal Intermediate-Term 75% · Opal Short-Term 25% |
| Opal Satellite 60 | 79 | Opal Intermediate-Term 100% |
| Opal Satellite 70 | 39 | Opal Conservative Growth 50% · Opal Intermediate-Term 50% |
| Opal Satellite 80 | 54 | Opal Conservative Growth 100% |
| Opal Satellite 98 | 12 | Opal Long-Term Aggressive 100% |
| Opal - Income | 2 | LEAF (4 securities) |
| Opal - Beecherl Legg | 1 | Opal Conservative Growth 79% · Opal Ultra Short-Term Income 21% |
| Opal - Cash + Satellite 50 | 1 | Opal Intermediate-Term 68% · Opal Short-Term 23% · Opal Ultra Short-Term Income 9% |
| Opal 66% Long Term / 34% UST | 1 | Opal Conservative Growth 66% · Opal Ultra Short-Term Income 34% |
| Opal Ultra Short Term | 3 | Opal Ultra Short-Term Income 100% |
| Opal UST/ Sat 70 | 1 | Opal Conservative Growth 46% · Opal Intermediate-Term 46% · Opal Ultra Short-Term Income 9% |
| **Blended Opal / Satellite 50** | 1 | **Opal Intermediate-Term 19% · Opal Short-Term 6% · Sleeve-Equity 38% · Sleeve-Tax-Free Bond 36% · Sleeve-Core Money Market 2%** |

> *"Blended Opal / Satellite 50" is the proof of the pattern* — Opal models are only **25%** of it; the remaining
> 76% are non-Opal "Sleeve" blocks. A blend can be part-Opal.

**3 are the real gap — non-Opal-named, composition never pulled, cannot currently be confirmed:**
**Anna \*9237** (1 acct) · **Anna \*9238** (1 acct) · **Moderate Income Portfolio** (4 accts).

**1 does not exist in the roster: "Opal Satellite 15"** — the live ladder is 30 → 40 → 50 → 60 → 70 → 80 → 90 → 98;
there is no 15. (Worth confirming whether it was renamed, retired, or never existed.)

---

## 5. The underlying Opal building-block models (what to scan *for*)

The 6 leaf models that are the actual "Opal Models":

| Opal building-block model | # securities |
|---|---:|
| Opal Conservative Growth | 15 |
| Opal Intermediate-Term | 19 |
| Opal Short-Term | 17 |
| Opal Ultra Short-Term Income | 14 |
| Opal Long-Term Aggressive | 14 |
| Opal - Income | 4 |

**Data-quality flags surfaced in passing (not blockers):**
- **Duplicate leaf:** both *"Opal Long Term Aggressive"* and *"Opal Long-**Term** Aggressive"* exist as separate
  14-security models (hyphen difference). Likely a dup to reconcile.
- **Typo:** *"Opal Long Term Conservatiove"* (wraps Opal Conservative Growth 100%).

---

## 6. More strategies that likely hold Opal models — INFERRED, pending a scope=all pull

**Cannot be confirmed from landed data** (their composition was never pulled). By naming pattern + the
Blended-Opal/Satellite-50 precedent, the high-probability holders, ranked by account exposure:

1. **The entire "Core \| Satellite" family (~86 accounts)** — 30/40/50/60/70/80/98 + Tax-Free + CA Tax-Free
   variants. "Satellite" is the Opal blend concept; Opal models are almost certainly the satellite sleeve.
   **Largest hidden pool.**
2. **Moderate Income Portfolio** (4), **Anna \*9237 / \*9238** (1 each) — Andrew's own examples.
3. CSTF40/CSTF50 (advisor G&I blends), **Core / Satellite Equity**, **JBALX and FCNTX 80/20**, and client-named
   books (Eartha Vaughan IRA, Hendrickson Trust, Pena – Conservative).

*Explicitly out (no Opal expected): the `Passive XX` and `529-F2 American Funds` families — index/fund products.*

---

## 7. What closes this (design, not yet executed)

1. **One discovery run with `MODEL_DETAIL_SCOPE=all`** — lands all 60 compositions instead of 25. Cottonwood-only,
   additive, read-scope widening (a config change + a single pull; goes through the normal deploy path, not under
   the pause). A permanent daily flip vs a one-time discovery run is Andrew's call — a one-time run answers the
   question at least cost.
2. **Reverse-attribution:** flag any strategy whose transitive `children` include one of the 6 Opal leaves. That
   is the definitive, name-independent "which Strategies hold Opal models" list, at Strategy grain. (Replaces the
   name-seed with a holdings-seed — climb up, not just down.)
3. **Strategy-level assets:** join the resulting strategies' accounts → holdings feed by `accountId`, group by
   `strategyName`. Yields **both grains** — aggregate Opal-model AUM **and** per-Strategy AUM — including the
   non-Opal-named strategies.

**Net:** the pull mechanism, the parser, and the assignment data already support this. What is missing is (a) the
scope switch and (b) reverse (parent→Opal-child) attribution instead of name-gating. Both are small and additive.

---

## Appendix — evidence (denominators + keys)

- **Roster:** `blackdiamond/cottonwood/bronze/rebalancer_models/2026-07-24/page_000.json` — `totalResultCount=60`,
  60 rows, 0 pagination gap.
- **Accounts:** `…/rebalancer_accounts/2026-07-24/` — 912 rows; `strategyName` present on every row.
- **Composition:** `…/rebalancer_model_detail/2026-07-24/` — **25** files (identical count every day 07-21→07-24;
  **no `scope=all` run has ever landed**).
- **Scope in production:** `aws lambda get-function-configuration --function-name cot-rebalancer-runner` →
  `MODEL_DETAIL_SCOPE=opal_closure`.
- **Source:** `infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py` (`:275,279-293,296-320`);
  `data/assets/scripts/silver/rebalancer_conversion.py` (`_walk_hierarchy` `:244-296`; `is_opal_name`
  `rebalancer_schemas.py:197-202`).
- **Prior ruling + discovery numbers:** `…/0.6.2_AE_PartnerETL/deliverables/COT_MODEL_PORTFOLIO_DISCOVERY_WSE_20260721.md`
  (296 accounts / 14 assigned Opal models; $126,381,228.86 dim total; strict-name ruling verbatim).

**What this scan did NOT do:** no live BD call, no Lambda invoke, no scope change, no commit/apply/deploy, no
message to any agent. All findings are from landed artifacts + source under the fabric pause.
