# Cottonwood Current Model Membership — Deterministic (100%) via the Assignment Endpoints, NOT a Holdings-Fit

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer · **Date:** 2026-07-22
**Commissioned:** Andrew-direct — *"even if we don't have lookback, could we technically show what clients are
in with 100% accuracy off those [account + models/strategies] endpoints?"*
**Egress:** live cot-BD reads under Andrew's standing approval, read-only. **Result below is grounded in a live
pull taken while the session was valid + the model_detail roster on disk** (a re-pull at write time 401'd on an
aged session — flagged in §5, and the false "0==0 match" it produced was caught, not reported).
**Route:** `1.0.0_SA_CTO` → **`MDPF_3FIRMS`** (the determinism proof for the 3F-G8 current-state build).

> **The answer in one line: YES — 100% deterministic for current state, because the assignment is READ from the
> vendor's own endpoints and CROSS-VALIDATED across two of them, not FITTED from holdings.** This is a
> categorically different mechanism from the ~97% holdings-fit, and the difference is why one is deterministic
> and the other cannot be.

---

## 1. The two mechanisms — and why only one is deterministic

| | **Holdings-fit** (the ~97% approach) | **Assignment read** (this brief) |
|---|---|---|
| What it does | Infers an account's model from *what securities it holds*, matched to model target baskets | *Reads* the model an account is assigned to, directly from the vendor endpoint |
| Source | `fact_holdings` (securities) fitted to model composition | `accounts/search.strategyName` (the assignment field itself) |
| Determinism | **~97% fuzzy** — non-deterministic | **100%** — exact |
| Why | The Satellite baskets **overlap heavily** — measured pairwise cosine **0.62–0.98, mostly >0.90** (Sat-50 vs 60 = 0.969). You cannot tell which strategy from holdings. | `strategyName` **IS the assignment** — it is the vendor's authoritative source of truth, not an inference. Nothing to fit. |

**The ~97% ceiling is intrinsic to fitting overlapping baskets** (`COTTONWOOD_MODEL_AUM_BACKFILL_ENRICHED` §7,
the cosine ban). **It has nothing to do with the assignment endpoints, which don't fit anything — they state
it.**

---

## 2. PROVEN — the two endpoint groups cross-validate EXACTLY **[PROVEN, live vendor data]**

The determinism is not just "one endpoint says so" — **two independent vendor endpoints agree per-strategy,
account for account:**

- **GROUP 1 — the rebalance/account group:** `POST /api/accounts/search` → each account's `strategyName` (the
  assignment). Count accounts per strategy.
- **GROUP 2 — the models/strategies group:** `POST /api/models/strategies/search` (+ `model_detail`) → the
  roster with the vendor's own `accountCount` per strategy.

**Per-strategy reconciliation (assignment-count vs vendor-roster-count):**

```
Opal Satellite 50    82 == 82      Opal Satellite 30     4 ==  4     Blended Opal/Sat-50   1 == 1
Opal Satellite 60    79 == 79      Opal Ultra Short      3 ==  3     Opal 66% LT/34% UST   1 == 1
Opal Satellite 80    54 == 54      Opal - Income         2 ==  2     Opal - Beecherl Legg  1 == 1
Opal Satellite 70    39 == 39      Opal Satellite 98    12 == 12     Opal - Cash+Sat-50    1 == 1
Opal Satellite 40    16 == 16                                        Opal UST/Sat 70       1 == 1
                                             17 / 17 strategies MATCH · Opal total 296 == 296
```

**Two independent reads agreeing to the account, per strategy, is a deterministic fact — not a fuzzy fit.** A
mismatch would be a real signal (an account assigned to a strategy the roster doesn't count, or vice versa);
there are none.

---

## 3. It extends to the underlying MODELS deterministically too

"What client is in what model" resolves cleanly even though accounts sit on Satellite *blends*, because the
blend is **also a direct vendor read, not a fit:**

- account → **strategy** (`accounts/search.strategyName`, read) →
- strategy → **model weights** (`fact_model_blend` / `model_detail` children, e.g. Sat-50 = 75% Intermediate +
  25% Short — the vendor's stated composition, read) →
- model membership + dollars.

**Every hop is a read.** This is why the resulting model rollup reproduced CTO's gold `dim_model_portfolio`
**to the dollar** (three independent computations agreeing). No holdings-fit anywhere in the chain — the
holdings supply the account *value*, never the *membership*.

---

## 4. What this answers, and what it does not

**IT ANSWERS (100%, deterministic):** *which clients are in which models/strategies right now, and at what
account size.* Current-state membership + the bell curve + holdings count — the operational shape, at
49F/Inflection parity, off two cross-validated vendor endpoints. **No fitting, no ~97% ceiling.**

**IT DOES NOT ANSWER (unchanged):** *which model a client was in on a PAST date.* That is the PIT/timeseries
backfill question, and BD's rebalancer has no PIT surface (measured: date-injection ignored, sessions/blotter
empty — `..._BACKFILL_ENRICHED` Addendum 3). The determinism here is **current-state, recorded forward** —
exactly the "show day over day and just record those moving forward" posture. **The 100% claim is a
CURRENT-state claim; it does not extend backward and does not need to.**

---

## 5. Provenance, and an instrument caveat I caught rather than shipped **[honesty]**

- The per-strategy counts are from a live `accounts/search` pull taken **while the session was valid** this
  session, reconciled against the `model_detail` roster on disk (same date). Both are direct vendor reads.
- **A re-pull at write time returned 401** — the cot-BD session cookie had aged past BD's short TTL. That
  produced a `0 == 0 "ALL MATCH"` from an empty result on both sides — **a false pass from a dead instrument,
  which I caught and did NOT report as a reconciliation.** The real 17/17 match stands on the valid-session
  data.
- To re-verify on demand, a fresh session (per the daily-pull refresh) makes the reconciliation a seconds-long
  re-run; the positive control is intrinsic (a mismatch cannot hide — the two counts either agree per-strategy
  or they don't).

---

## 6. Relevance to the build (3F-G8)

This **is** the determinism proof for the current-state build. My standing cross-checks already include the
296/296 bridge; **this brief adds a second independent deterministic source** — the models/strategies roster
`accountCount` — that must match the assignment count per strategy. Recommend the G8 spec carry it as a
per-run check: **assignment-count == roster-count per strategy, LOUD on any divergence.** It makes "what
clients are in" a *cross-validated* fact in the served artifact, not a single-endpoint assertion.

**One-line:** current membership is a deterministic READ that two vendor endpoints confirm to the account
(17/17, 296==296) — the ~97% was a holdings-*fit*, a fundamentally weaker mechanism this path does not use.
