# Sourcing Cottonwood Model-Level Daily AUM for the MDPF aggregate-aua-timeseries

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer · **Date:** 2026-07-22
**Commissioned:** Andrew-direct — *"how we would get daily transaction records for aggregate holdings at the
model level ... with the interest of populating this in the Model Portfolio daily aum-timeseries for
Cottonwood."*
**Egress used: NONE.** Every number below is computed from data already in our lake + the operator-supplied
rebalancer bronze. No vendor call.
**Route:** `1.0.0_SA_CTO` — this feeds the existing **WSE_COTMDL** (Cottonwood-into-MDPF) workstream.

> **This is a SOURCING brief, and it PROPOSES.** It does not build, and it does not dispatch into the MDPF
> pipeline, which is mid-revamp and held. It answers *how the data would be obtained and shaped*, with the
> core mechanism **proven on real data**, and hands the build decision to CTO.
> **Evidence grades:** **[PROVEN]** computed end-to-end on real data here · **[GROUNDED]** read at source ·
> **[HELD]** a decision gated elsewhere · **[UNKNOWN]** stated, not inferred.

---

## 1. The answer in one paragraph

**We already pull both halves daily; the work is a JOIN, not a new feed.** Cottonwood's per-account daily
holdings value lands in `opal-data-cot/silver/holdings/{date}.parquet` (from the DataMining qt1 ETL), and the
per-account Opal-model assignment lands in
`opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_accounts/{date}/` (the WS-1 rebalancer pull).
Joining them on the account id, grouping by model, and summing market value yields **model-level daily
aggregate AUM** — the exact series the MDPF `aggregate-aua-timeseries` needs. **No new vendor surface, no new
egress.** The join is proven below: **296 of 296 Opal accounts match, and the result is a clean $126.4M across
14 models.**

---

## 2. The mechanism, proven end-to-end **[PROVEN]**

**Three components, all already flowing daily:**

| # | Component | Source (already landing daily) | Grain |
|---|---|---|---|
| 1 | **Model assignment** — which account is in which Opal model | `blackdiamond/cottonwood/bronze/rebalancer_accounts/{date}/page_*.json` → `externalId` + `strategyName` | account (live-state) |
| 2 | **Daily value** — per-account holdings market value | `opal-data-cot/silver/holdings/{date}.parquet` → `account_id` + `market_value` | account × holding × day |
| 3 | **Aggregate** — join, group, sum | join `rebalancer.externalId == holdings.account_id`, group by model, sum MV | **model × day** |

**The join key is exact.** Both sides carry the `z09`-prefixed external id (`rebalancer.externalId` =
`z0926617691`; `holdings.account_id` = `z0927438111`). **Measured overlap: 296 / 296 Opal-model accounts
present in silver holdings on 2026-07-20. 100%.**

**Proven output — Cottonwood model-level AUM, 2026-07-20 (real, joined):**

| Opal model (strategyName) | Aggregate AUM | Accounts' holding rows |
|---|---|---|
| Opal Satellite 50 | $34,495,311 | 2,060 |
| Opal Satellite 60 | $31,293,131 | 1,613 |
| Opal Satellite 80 | $19,419,636 | 889 |
| Opal Satellite 70 | $17,408,730 | 843 |
| Opal Satellite 40 | $11,784,140 | 373 |
| Opal UST / Sat 70 | $2,313,241 | 31 |
| Opal 66% Long Term / 34% UST | $2,126,594 | 28 |
| Opal - Cash + Satellite 50 | $1,966,515 | 32 |
| Opal Satellite 30 | $1,624,957 | 98 |
| Opal - Income | $1,242,005 | 22 |
| Opal Satellite 98 | $1,118,258 | 177 |
| Blended Opal / Satellite 50 | $1,017,618 | 41 |
| Opal - Beecherl Legg | $515,839 | 35 |
| Opal Ultra Short Term | $55,253 | 32 |
| **model_aua TOTAL** | **$126,381,229** | **14 models** |

**Firm totals the same day** (the other fields MDPF needs): total Cottonwood AUA **$458,114,003** (913
accounts) → **`non_model_aua` = $331,732,774**.

---

## 3. "Daily transaction records" — the interpretation, stated so we build the right thing

The phrase admits two readings. **For an AUM time-series, the first is what you want, and it is what §2
proves:**

- **(A) Daily HOLDINGS SNAPSHOT (the AUM level).** The daily aggregate market value per model. This IS the
  AUM series. **Snapshot-first — exactly the COTETL doctrine** (`COTETL_METHODOLOGY_THESIS.md`): read daily
  value straight from the holdings snapshot, do not reconstruct it from flows. §2 is this.
- **(B) Daily FLOW/TRANSACTION records (contributions/withdrawals/trades).** These live in
  `opal-data-cot/silver/transactions/{date}.parquet` (back to 2026-03-09) and would decompose *AUM change*
  into flow vs market movement. **They are NOT the AUM level** — an AUM series built from flows is the
  reconstruct-from-transactions anti-pattern that corrupted 40.2% of inf rows to $0 (D3 §4).

**Recommendation: build the AUM series from (A), snapshot-first.** Keep (B) available as a *separate*
decomposition if MDPF later wants flow-vs-market attribution, but never as the AUM source.

---

## 4. The MDPF target shape — where this lands **[GROUNDED]**

`data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` emits a per-firm columnar JSON the portal pulls
at `/api/general/mdpf/{firm_id}/aggregate-aua-timeseries.json`. The Cottonwood slice must supply:

```
"cottonwood": {
  "partner_name": "Cottonwood Capital Advisors",
  "model_aua":     [ ... daily ... ],   # the $126.4M-class total, per day
  "non_model_aua": [ ... daily ... ],   # firm total - model_aua (the $331.7M residual)
  "by_model": {
    "<model_key>": { "cohort_class": "model",
                     "model_value": [ ... daily ... ],
                     "display_name": "<canonical>" },
    ...
  }
}
```

- **Dates align to the MDPF trading-day axis**, not wall-clock (the axis the revamp is currently fixing).
- **`model_key` → `display_name` resolves through the canonical MDPF model registry** (MDPF_SCOPED.F5) — the
  producer already does this for the other firms, and it is the arbiter for §6's naming problem.
- **`non_model_aua` needs the firm total**, which §2 confirms is available from the same holdings partition
  (all 913 accounts, not just the 296 Opal).

---

## 5. Forward vs backfill — the crux, and where the migration reality bites **[PROVEN / HELD]**

**FORWARD (clean, recommended, no caveat):** each daily run joins *that day's* assignment to *that day's*
holdings. The result is a correct daily model-AUM point, **dated by the pull, self-extending, and
fabrication-free** — it reads two real same-day snapshots. **This satisfies the additive / non-conflicting /
no-hardcoded-start constraint from the lookback brief by construction.** The series simply starts at the first
daily rebalancer pull (~2026-07-21) and grows one honest point per day.

**BACKFILL (gated — do NOT do it naively):** silver holdings exist back to **2026-06-08**, so the *value* half
has history. But the *assignment* half is **live-state only** — the rebalancer roster has no date field (I
proved this: 22 fields, none a date). Back-mapping **today's** assignment onto June holdings is the
fabrication trap: for any account that changed models during the migration, it stamps the wrong model on the
old value.

**How real is that risk here? Measured, and it is not small.** Back-mapping today's assignment onto 2026-06-08
holdings joins **291 / 296** accounts and produces $115.9M — but Cottonwood is **mid-migration**: models were
created between 2026-05-28 and 2026-07-17, a quarter of the book sits on models created on a single day
(07-06), and 5 of today's Opal accounts did not exist on 06-08. **Assignment is demonstrably churning, so a
back-mapped series is demonstrably wrong for the churned accounts** — and we cannot tell which without dated
assignment.

**The one thing that would make backfill clean** is the **temporal-vs-current probe** from the lookback brief
(`COTTONWOOD_ASSIGNMENT_LOOKBACK_OPTIONS_20260722.md §3`): if the DataMining qt1/allocations **account-strategy
dimension** proves *temporal* (the assignment in force on each row's date), a historical query returns real
`(account, model, MV, date)` and backfill is fabrication-free. **Until that probe returns TEMPORAL, backfill
is forbidden** and the series is forward-only. **[HELD on the probe.]**

---

## 6. NAMING — a real mismatch you should see before this is built **[GROUNDED]**

**The models you named — "Opal Conservative Growth, Ultra-Short Term, Intermediate Term" — are NOT the models
that hold the accounts.** Measured against today's roster:

| Named model | Accounts on a strategy with that name |
|---|---|
| Conservative Growth | **0** |
| Intermediate | **0** |
| Short-Term | **0** |
| Long-Term | **0** |
| Ultra Short | 3 |

The 296 Opal accounts are on the **"Satellite 50/60/70/80/…"** strategies and a handful of blends (§2). And
separately, the rebalancer **model *definitions*** include "Opal Conservative Growth", "Opal Intermediate-Term",
"Opal Short-Term", "Opal Ultra Short-Term Income" — **all created 2026-05-28, all with ZERO accounts** (the
addendum in the lookback brief).

**So there are two distinct Opal model vocabularies at Cottonwood**: the *definition* names (Conservative
Growth / Intermediate / …, unpopulated) and the *assignment* names (Satellite 50/60/…, populated). **This must
be reconciled before the series is built**, or `by_model` will key on Satellite names while the product
expects Conservative-Growth-style names. **The MDPF canonical model registry (F5) is the right arbiter** —
someone (Andrew/CTO) needs to rule whether the Satellite tiers ARE the risk-model line under different labels,
or whether the definition-named models are still being populated by the migration. **This is a taxonomy
decision, not a data-engineering one, and it is the single most likely thing to make a first build wrong.**

---

## 7. Validation the build must carry **[PROVEN feasible]**

1. **model_aua + non_model_aua == firm total** per day (identity; $126.4M + $331.7M = $458.1M holds on 07-20).
2. **Per-model account count ties to the rebalancer roster** (296 total; the 14-model split in §2 is the
   check).
3. **Cross-service account bridge is exact** — the `externalId ↔ account_id` join is 296/296; a drop below
   100% is a real signal (an account in the rebalancer but not in holdings = a coverage gap to flag, not to
   silently drop).
4. **Frozen-vs-stable caveat carries** — the two rebalancer days (07-21, 07-22) are byte-identical; per COO's
   standing point, a stable roster and a frozen feed are indistinguishable from storage alone. The daily join
   must not treat "assignment unchanged" as "feed confirmed live."

---

## 8. What's proposed, what's held, what's decided by whom

- **PROPOSED (CRO):** a gold producer that joins the daily rebalancer assignment to daily cot silver holdings,
  aggregates to model × day, and emits the `cottonwood` MDPF firm slice. **Forward-only** until the temporal
  probe clears backfill. No new egress.
- **HELD:** (a) the temporal-vs-current probe gates any backfill; (b) MDPF itself is mid-revamp — this feeds
  WSE_COTMDL, it does not land into a held pipeline unprompted.
- **DECISIONS (Andrew / CTO):** the §6 model-naming/taxonomy reconciliation (the blocker); whether forward-only
  is acceptable as the v1 (per the migration reframing, it should be); build lane + sequencing against the
  MDPF revamp.
- **NOT this brief's to do:** build, dispatch, or register. Research proposes.

---

## 9. Grounding

**[PROVEN]** the 296/296 join and the $126.4M / $331.7M / $458.1M model/non-model/total split
(`rebalancer_accounts` 2026-07-22 × `cot silver/holdings` 2026-07-20, computed here); the 291/296 06-08
back-map and its churn risk; the §6 naming counts. **[GROUNDED]** the MDPF target shape
(`build_aggregate_aua_timeseries.py:12-98`, read at source); silver holdings horizon (S3 listing, earliest
2026-06-08); rebalancer roster has no date field (22-field schema, addendum to the lookback brief). **[HELD]**
the temporal probe (lookback brief §3); the MDPF revamp state. **[UNKNOWN]** whether the definition-named
models (Conservative Growth etc.) are mid-migration-populating or deprecated labels — §6, a decision not a
measurement.

**Companion:** `COTTONWOOD_ASSIGNMENT_LOOKBACK_OPTIONS_20260722.md` (the assignment-history question this
sourcing depends on).

---

# ADDENDUM — 2026-07-22, Andrew correction: the Satellites are WEIGHTED BLENDS OF MODELS, and the backfill mechanism tested

**Andrew, two corrections after the brief:** *(1)* the Opal Satellites are comprised of weights of models;
*(2)* joining against holdings/transactions is the whole point of backfill — the dated event is what we need.
**Both are right. §5 and §6 of the brief were wrong or incomplete. This addendum supersedes them.** Zero
egress — computed from `rebalancer_model_detail` (already pulled daily) + cot silver holdings.

## B1. §6 was NOT a naming mismatch — it is COMPOSITION **[PROVEN]**

The Satellites are risk-tiered **weighted blends of the real Opal models**. Grounded in the
`rebalancer_model_detail` hierarchy (`rebalanceModelType: Strategy` -> children `rebalanceModelType: Model`
with `absoluteAllocation`):

| Strategy (what accounts hold) | = weighted models (what you named) |
|---|---|
| Satellite 50 (82) | **75% Intermediate-Term + 25% Short-Term** |
| Satellite 60 (79) | **100% Intermediate-Term** |
| Satellite 80 (54) | **100% Conservative Growth** |
| Satellite 70 (39) | **50% Conservative Growth + 50% Intermediate-Term** |
| Satellite 40 (16) | **50% Intermediate-Term + 50% Short-Term** |
| Satellite 98 (12) | **100% Long-Term Aggressive** |
| Satellite 30 (4) | **25% Intermediate-Term + 75% Short-Term** |
| Ultra Short Term (3) | **100% Ultra Short-Term Income** |
| + 5 bespoke blends (1 acct each) | Conservative Growth / Short-Term / UST-Income / Sleeve mixes |

**So the "0-account" models (Conservative Growth, Intermediate-Term, Short-Term, Ultra Short-Term Income) are
not unpopulated — they are the TERMINAL models, populated indirectly through the Satellite blends.** The
brief's §6 "taxonomy decision" framing was wrong: there is no ambiguity to rule on, there is a **composition to
apply**. Each model definition also carries its **security basket** with weights (e.g. Intermediate-Term =
BIV 3.28% + IEFA 11.3% + JAAA 4.19% + ...), so the model layer is fully specified.

## B2. The correct aggregation is a WEIGHT ROLLUP, and it is proven **[PROVEN]**

`model_aua[model] = Sum over accounts [ account_MV(day) x strategy_weight_on_model ]`

Computed on 2026-07-20 (rebalancer assignment x model-composition weights x cot silver holdings):

| Model | Daily AUM |
|---|---|
| Opal Intermediate-Term | $74,760,167 |
| Opal Conservative Growth | $30,991,060 |
| Opal Short-Term | $16,246,582 |
| Opal Ultra Short-Term Income | $1,259,943 |
| Opal Long-Term Aggressive | $1,118,258 |
| (Sleeve residuals) | $763,214 |
| **TOTAL** | **$125,139,224** |

Ties to the strategy-level $126.4M within **$1.24M**, which is exactly the one strategy with no model
composition (`Opal - Income`, 2 accounts) that falls through the rollup -- a **named, measured residual**, not
a silent gap. So `by_model` in the MDPF slice should key on the **real models** (Intermediate-Term,
Conservative Growth, ...), computed by this rollup, with `Opal - Income` handled explicitly.

**All THREE inputs already land daily:** `rebalancer_accounts` (assignment) + `rebalancer_model_detail`
(the blend + security weights) + cot silver holdings (value). The forward pipeline needs no new feed.

## B3. SNAPSHOT is the way, and the FORWARD series is snapshot-native + proven

Confirming directly: yes, snapshot-first is right, and the forward model-AUM series is a pure daily snapshot
join — that day's holdings x that day's assignment x that day's composition -> that day's model AUM. Dated by
the pull, self-extending, fabrication-free. **B2 IS that computation for one day.** The original brief covered
snapshot-first for the *AUM level* (§3) but did NOT carry the model-weight decomposition; B1/B2 are that
missing piece.

## B4. BACKFILL — I TESTED the holdings/transactions idea. Honest result: the direct fingerprint FAILS, and here is what works instead

Your instinct — use the dated daily holdings/transactions as the temporal anchor so we do not depend on
live-state assignment — is the right target. I tested the most direct form of it:

**TESTED AND WEAK: recover a past date's STRATEGY by matching that day's holdings basket to the known target
baskets.** It fails because **the strategy baskets are nearly identical** — they are all built from the same
~15 ETFs at different weights. Measured pairwise basket cosine similarity: **Satellite 50 vs 60 = 0.969,
80 vs 70 = 0.981, 60 vs 70 = 0.976** — mostly >0.90. **You cannot reliably tell which strategy an account was
on from its holdings alone**, so holdings-fingerprinting would misassign the blend and is not defensible
(it is inference-from-similarity, the fabrication class).

**WHAT ACTUALLY GIVES DATED BACKFILL, in order of cleanliness:**

1. **The DataMining temporal assignment dimension (the real unlock).** IF the qt1/allocations
   `accountRebalStrategyID` dimension is *temporal* (the §3 probe of the lookback brief), a historical query
   returns dated `(account, strategy, date)` -> apply the B2 model-weight rollup -> **dated model-level AUM
   back to the coverage horizon, fabrication-free.** This is the path that turns the snapshot approach into a
   real backfill. **Still gated on that one probe.** It is now the single highest-value open item, because it
   unlocks history for BOTH the strategy and (via B2) the model level.

2. **Transactions as dated CHANGE-events (your "some kind of daily event").** The transaction stream is dated
   and real back to 2026-03-09. A rebalance into a strategy produces a datable *cluster* of trades matching
   the target basket -- so transactions can date *when an account's composition changed*, bounding the windows
   in which assignment was stable. This does not name the strategy on its own (same basket-overlap problem),
   but it tells you *when to trust* a carried-forward assignment vs when it changed -- a real guard against the
   fabrication B4-fingerprint falls into. Secondary, and a genuine use of the dated event you pointed at.

3. **Forward-only (the safe default).** If neither probe clears, the series starts at the first daily pull and
   grows -- honest, self-extending, and per the migration reframing, already a correct answer.

**Net:** snapshot is the way (confirmed); the model decomposition is the correction (B1/B2, proven); and the
dated-event backfill you are pointing at is real but runs through the **temporal DataMining dimension**, not
through holdings-basket matching (which I tested and it is too coarse). The composition weights (B1) are what
make it *model*-level rather than *strategy*-level either way.
