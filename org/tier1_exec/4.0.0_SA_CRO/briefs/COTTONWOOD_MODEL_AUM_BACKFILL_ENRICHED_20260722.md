# Cottonwood Model-AUM BACKFILL — Enriched Brief

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer · **Date:** 2026-07-22
**Commissioned:** Andrew-direct (via `1.0.0_SA_CTO` relay, **confirmed by Andrew directly** — *"Yes I had
written them about the backfill prior to your revision"*), explicitly on the **backfill** aspect of
`COTTONWOOD_MODEL_AUM_TIMESERIES_SOURCING_20260722.md`.
**Egress used: NONE.** All grounded on data already in our lake.
**Route:** `1.0.0_SA_CTO`. **Under LD-0333 nothing dispatches from this until Andrew's word** — it is a design
brief for the MDPF_3FIRMS 3F-B6 backfill queue.

> **Supersedes §5 of the sourcing brief** and folds CTO's two bindings (composition vintage; the structural
> depth ceiling) plus the monolith-fact finding below. **Grades:** **[PROVEN]** computed here · **[GROUNDED]**
> read at source · **[HELD]** gated on the probe · **[UNKNOWN]** stated, not inferred.

---

## 1. The answer, decided

**A dated, fabrication-free MODEL-level AUM series is clean going FORWARD from ~2026-07-21, and cannot be
extended backward without the DataMining temporal probe — and even that cannot pass ~2026-05-28, because the
models did not exist before then.** Everything below is the evidence and the exact design for each branch.

Three numbers bound the whole question:

| Bound | Date | Why | Grade |
|---|---|---|---|
| **Structural ceiling** (nothing can precede this) | **~2026-05-28** | The Opal models were *created* 05-28..07-17. No model series can predate the models. | [PROVEN] |
| **Dated-fact floor** (clean series starts here) | **~2026-07-21** | The monolith model facts are forward-accruing daily snapshots; the daily pull began 07-21. | [PROVEN] |
| **Value-history floor** (holdings reach further back) | **~2026-06-08** | Holdings exist back to 06-08 (firm/account AUM without a model split). | [GROUNDED] |

**The gap that backfill is really about is 05-28 → 07-21 — roughly seven weeks — and it is bridgeable only if
the probe (§4) returns temporal for BOTH assignment and blend.**

---

## 2. A clean model-AUM backfill needs THREE vintages dated — only one is **[PROVEN]**

The B2 rollup (`model_aua[m] = Σ accounts [ account_MV(day) × strategy_blend_weight_on_m ]`) consumes three
inputs. For a *past* date to be fabrication-free, **each must be the value that was true on that date**:

| Vintage | What it is | Dated back in time? | Status |
|---|---|---|---|
| **(c) VALUE** | per-account holdings market value | **YES** — `fact_holdings` / cot silver, back to ~06-08 | **[PROVEN] have it** |
| **(a) ASSIGNMENT** | which strategy each account was on | **NO** — rebalancer roster is live-state, no date field (22 fields, none a date) | **[HELD] the probe** |
| **(b) BLEND** | the strategy→model weights (e.g. Sat-50 = 75/25) | **NO for history** — see §3 | **[HELD] the probe** |

**Value is dated; assignment and blend are not. Backfill is exactly as deep as we can date (a) and (b).**

---

## 3. THE MONOLITH FACTS ARE FORWARD-ACCRUING SNAPSHOTS — the decisive finding **[PROVEN]**

`blackdiamond/cottonwood/silver/` carries `fact_model_assignment`, `fact_model_blend`, `fact_model_definition`
— **each partitioned `date=2026-07-21/ | date=2026-07-22/`, and NOTHING before.**

**These are `date`-as-filing-date snapshots, not a temporal query surface.** Each partition is *that day's
live-state pull* filed under the pull date — the exact "`--date` is a filename, not a query" shape CTO named on
the eclipse puller. Consequence:

- **FORWARD:** every day, a new partition captures that day's real assignment + blend + value. A genuine dated
  series **accrues on its own** — additive, self-extending, no synthesized rows. **This is the clean path, and
  it starts at the first pull (~07-21).**
- **BACKWARD:** there is no June partition because we did not pull in June, and the source is live-state — so
  the monolith facts **structurally cannot supply pre-07-21 assignment or blend.** Backfill cannot come from
  here. It can only come from the one surface that is date-*windowed* rather than date-*filed*: DataMining
  (§4).

**Composition vintage is real, and measured.** Across the only two days we hold, the strategy→model **blend
ratios were stable** (0 of 15 strategies moved 07-21→07-22), **but Satellite 50's security weights DID move.**
So composition drifts. For the AUM rollup only the *blend ratio* (b) matters — n=2 says it was stable for two
days, which says **nothing** about whether Sat-50 was 75/25 in June. **Applying today's blend to a June date is
a fabrication at the composition layer even with perfect dated assignment** (CTO binding #1). The probe must
therefore answer BOTH temporalities.

---

## 4. THE PROBE — now the single gate, extended to both vintages **[HELD]**

**Question:** does DataMining expose, as a *date-windowed query*, (a) the account→strategy assignment **and**
(b) the strategy/model blend **that were in force on a past date** — or does it stamp *today's* onto historical
rows?

**Test (one template re-persist + queries on an already-authorized path, no new wire):**
1. Select the Account-level assignment dimensions (`accountRebalStrategyID`, `AccountRebalAssignmentID`) — and
   separately probe whether `fact_model_blend`/`fact_model_definition` history is queryable by date.
2. Run for a recent window **and** a pre-change window.
3. **Positive control is MANDATORY** (your lookback-brief requirement, and CTO's): include an account **known**
   to have changed strategy between the two windows — else "identical" cannot fail, and the test proves
   nothing. *Source the known-changed account from the forward roster diffs as they accrue (§6).*
4. **Read the discriminator on BOTH (a) and (b):** does the value differ between windows for the same
   account/strategy?
   - **BOTH temporal → clean backfill to the structural ceiling.** §5.
   - **Either current-stamped → that layer cannot be backfilled.** §5 branch-2.

Until the probe returns, **the model series is forward-only from ~07-21.** No exceptions — a back-map from
today's state is the fabrication we measured (§7).

---

## 5. The two design branches, specified

### Branch 1 — probe returns TEMPORAL for (a) AND (b): backfill IS clean, to ~05-28
Backfill join, per past date `D` (D ≥ ~05-28):
```
model_aua[m, D] = Σ accounts [ holdings_MV(account, value_date=D)          # (c) dated
                             × blend_weight(strategy_on(account, D), m, asof=D) ]   # (a)+(b) dated
where strategy_on(account, D) is the assignment IN FORCE on D.
```
**Carry BOTH vintages explicitly — the builder's TWO-DATES law (CTO):** `date=` is the *assignment* date;
`value_date` is the *dollars'* as-of. Conflating them presents Monday's dollars as Wednesday's. A backfill row
is `(model, effective_date, value_date, value)` — never a single date.
**Ceiling is ~05-28 regardless** — no query returns a model that did not exist.

### Branch 2 — probe returns CURRENT for either: name what is honestly recoverable, do not paper the gap
If assignment or blend cannot be dated, the model split cannot be backfilled. The honest options, in order:
1. **Holdings-only firm/account AUM history, NO model split, back to ~06-08.** This is real, dated, and
   fabrication-free — it is just coarser (firm total + non-model, no `by_model` pre-07-21). A legitimate
   partial that MDPF can render as "model breakdown begins 07-21."
2. **A labelled `unknown-assignment` band** for 05-28→07-21: show the model-eligible dollars exist but their
   model split is undetermined. Explicit, not invented.
3. **Pure forward-only** — the migration reframing already makes this a correct answer, not a placeholder.

**Recommendation under Branch 2: option 1 + forward-only** — give Andrew the firm/non-model history that IS
real, and start `by_model` at 07-21. Never a synthesized pre-07-21 model split.

---

## 6. TRANSACTIONS as a dated GUARD — accepted as a guard, not a license, with its own limit **[GROUNDED]**

The dated transaction stream (`fact_transactions`, back to ~03-09) cannot *name* a strategy (same basket
overlap that killed fingerprinting), but it can date *when an account's composition changed* — bounding the
windows in which a carried-forward assignment is trustworthy.

**The sharp limit (CTO's symmetry, and it is correct): the same basket similarity that kills fingerprinting
CAPS the change-detector for ADJACENT-strategy switches.** A Sat-50 → Sat-60 move (basket cosine 0.969)
produces a trade cluster nearly indistinguishable from ordinary flow rebalancing. So **detected rotation →
never carry across (sound); no rotation detected → nothing is licensed** (absence-of-signal cannot affirm
stability precisely where it is weakest).

**Free calibration as the forward window accrues (a standing research item worth taking):** daily roster diffs
give *dated, observed* reassignments; score each against its transaction signature; this **measures** the
detector's real hit-rate on adjacent vs distant switches before anyone leans on it. It also **manufactures the
probe's positive control** (§4.3) — a known-changed account — for free.

---

## 7. Why a naive back-map is banned — measured, not asserted **[PROVEN]**

Back-mapping today's assignment onto 06-08 holdings joins 291/296 and yields $115.9M — but the migration makes
it wrong: models created 05-28..07-17, a quarter of the book on models created on a single day (07-06), 5 of
today's Opal accounts absent on 06-08. And holdings-fingerprinting cannot rescue it: strategy baskets are
**cosine 0.62–0.98, mostly >0.90** — a *measured* ban, not an a-priori one. Any pre-07-21 model split not
sourced from a dated (a)+(b) is a future contradiction we would author ourselves.

---

## 8. Constraints, sources, hazards

- **Migration constraint (binding):** additive · no synthesized rows · no hardcoded start · non-conflicting
  with data that arrives later. The forward series satisfies all four by construction; any backfill must too.
- **Sources — MONOLITH ONLY:** `blackdiamond/cottonwood/silver/{fact_holdings, fact_model_assignment,
  fact_model_blend, fact_model_definition}` (equivalence-verified vs the cot tree by CTO: 16,762 rows / 913
  accounts / max per-account delta 0.0 / total $458,114,003.10). Cite these, not `opal-data-cot/silver`.
- **Deploy-map hazard (CTO):** the producer stays under `data/assets/scripts/` — `data/cot` gold
  **auto-deploys on push past co-sign gates by construction**.
- **Cross-check role:** my strategy-level join is the STANDING DAILY cross-check (3F-G3): strategy-sum ==
  dim-sum to the penny; model + non_model == firm total; externalId bridge exactly 296/296, any drop a
  coverage flag never a silent drop. **Frozen-vs-stable liveness requirement carries (3F-B6):** unchanged
  assignment across days is not a live-feed confirmation.

## 9. One-line

**Forward is clean and starts itself (~07-21); the ~05-28→07-21 gap opens only if the probe dates BOTH
assignment and blend; nothing reaches before ~05-28 because the models did not; and until the probe, the only
honest history is holdings-level firm AUM, never a synthesized model split.**
