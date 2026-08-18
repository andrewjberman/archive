# Cottonwood Interpolated Model-Backfill — Design Spec

**Author:** `4.0.0_SA_CRO` (Chief Research Officer) · **Home:** `org/tier1_exec/4.0.0_SA_CRO/` · **Date:** 2026-07-23
**Chain (Andrew-ordered):** this spec → **`3.0.0_SA_CVO` review (schema verified in tandem with CTO's companion)** →
**`2.0.0_SA_COO` TO decomposition.** CTO + COO CC.
**Companion (the aggregation half):** CTO's `GLOBAL_INTERPOLATED_AGGREGATION_SPEC` v0.2 **@068cb96aa** (pinned counterpart)
— its shared schema is the **incumbent provenance vocabulary** this spec emits against (CTO R-1). CVO signs the pinned
pair (CTO's @068cb96aa + this delta against CVO's @76c786b5e pin), then COO decomposes.
**Process (CVO R-5):** this is the ONE consolidated delta re-emission; it then HOLDS — any later change re-enters review
as its own delta.
**Egress:** NONE — design only, on data we already hold. **Extends:** the backfill-mechanism campaign (@63d0805a9) +
the daily-snapshot append spec (3F-G8b) + RCN-0001.
**Grades:** **[GROUNDED]** read at source · **[PROVEN]** computed prior · **[CONTRACT]** fixed by CTO's companion ·
**[PROPOSAL]** design, CVO's to review.

> **One line: build a LABELED interpolated Cottonwood model-AUM series for the ~05-28→07-21 gap — value reconstructed
> backwards from the current-day roster through the healthy transactions feed, model assignment estimated by a fuzzy
> holdings-match — rendered ONLY as "Interpolated" (yellow-dashed), quarantined by a provenance field from every
> measured-fact channel, and superseded point-for-point the instant real measured data arrives. The label is what
> makes "doesn't need to be exact" honest instead of fabricated.**

---

## 1. Authority — this is ORDERED, and it amends ruling 10 by sovereign word

**Andrew-direct (via CTO relay 022743Z, verbatim, confirmed grounded):** *"we need to figure out a strategy for how to
phase in the backfill to the models. I think the way it should work is we create an interpolated backfill based on
cottonwood daily snapshots and overlay based on the fuzzy match. IT doesn't need to be exact and we can display it as
'Interpolated' with a little yellow dashed line over the affected period or something. Should be able to use the
accounts from current day and track the inflows and work it out backwards, have 4.0.0_SA_CRO design it and send a spec
back for CVO review and COO TO decomposition."*

- **This AMENDS ruling 10's "Cottonwood developing" subject** (backfill was HELD-not-forbidden). It is now **ordered**,
  with a mandatory honesty channel. **The yellow-dashed "Interpolated" overlay is a PRODUCT REQUIREMENT, not a
  suggestion** (CTO gate note 1).
- **Design is CRO's; the build chain is not.** Research proposes; CVO reviews; COO decomposes; CTO gates the applies.
  This spec dispatches nothing.

---

## 1a. THE SHARED SCHEMA — ADOPT the incumbent provenance channel WHOLESALE (CTO R-1, @068cb96aa) **[CONTRACT]**

> **AMENDED 2026-08-18 in ONE clause (CTO ruling R-3, `docs/architecture/MDPF_PROVENANCE_CANONICAL_FORM_RULING_20260818.md`
> @fc74f8f6b4):** the dated per-cohort `cohort_provenance` channel is the **REFINEMENT carrier**
> (custody-vs-model split, confidence, window); the **CANONICAL class carrier at every grain is the
> aggregator-derived `point_class[]`** — this section's own "CTO's half", now the reader's **FIRST read**
> rather than its fallback. R-2 of the same ruling renames the per-firm SOURCE-IDENTITY channel (the
> 07-21 source-names shape) to **`cohort_source[]`** — two names for two intents, one class channel.
> No enum change to this spec's vocabulary; `carried` (Global) joins the FE's known set. Everything
> below stands as written under that precedence.

**CTO ruled (024627Z/024707Z): adopt the incumbent `build_aggregate_aua_timeseries.py` provenance vocabulary in full,
not a look-alike.** The decisive reason is INTEROP, not rhetoric: two provenance shapes in one served artifact family
(the incumbent's for 49financial + a look-alike for Cottonwood) recreates the two-null-semantics defect at the
provenance layer — the FE would need two readers forever. So the emitter uses the incumbent's **enum, container, field
name, AND grain**; my per-firm values map onto the finer per-cohort grain, and firm/Global `point_class` **derives**
(per-cohort is strictly finer — nothing the aggregation needs is lost, richness is gained).

```
partners: { cottonwood: {
   model_aua: [...], non_model_aua: [...], partner_custody_total: [...],
   by_model: { <model_key>: { display_name, cohort_class, model_value:[...], account_count:[...] } },
   cohort_provenance: [ { date, custody, model, ... } , ... ],   // PER-COHORT, PER-DATE (incumbent grain)
   backfill_method: "<this spec's method id + version>"          // incumbent field; carries the method tag
} }
// enum on every provenance slot:  measured | interpolated_estimate | absent   (the INCUMBENT string, exactly)
// confidence + window_id ride as ADDITIVE siblings on the cohort_provenance entry (new, additive, non-breaking)
// firm-level + Global point_class DERIVE in the aggregator: any-cohort-interpolated_estimate  (CTO's half)
```

**Bindings on my emitter, non-negotiable (CVO's mutant surface):**
1. **The enum value is `interpolated_estimate` — the INCUMBENT string, EVERYWHERE.** CVO's S1: one string mismatch
   anywhere makes an interpolated point derive `point_class=measured` and render **UNLABELED** — my own worst case.
   Legal values: `measured | interpolated_estimate | absent`.
2. **PER-COHORT grain (finer than per-firm), on the incumbent `cohort_provenance` channel.** This is *more* honest, not
   just contract-compliant: within Cottonwood the **model** cohort can be `interpolated_estimate` (the fuzzy assignment)
   while the **custody** cohort is `measured` (real holdings value back to ~06-08) on the same date — the label marks
   exactly what is estimated (the model split) vs what is measured (the firm value). §5 maps this per period.
3. **Precisely what is REUSED vs ADDED (CTO note 3 — the accuracy the softening instinct wanted, kept alongside the
   adoption):** REUSED wholesale = the channel + enum + container + `backfill_method` carrier + per-cohort grain.
   ADDED additively (new, non-breaking siblings) = `confidence` (mine, the churn-measured degradation §5) + `window_id`.
   The FE MAY render confidence, MUST render the label. `meta.interpolation = {affected_period:[start,end],
   method:<this spec id + version>, generated_at, superseded_dates:[...]}`.

**Scope bound (CTO companion §1):** the **Global aum-timeseries is my ONLY aggregation target.** The **radial
aum-metrics and the bell-curve distribution are current-snapshot, measured-only by construction — my design owes them
NOTHING** and must never reach them (a historical radial, if ever shipped, inherits these timeseries rules). This spec's
output contract is bounded to the dated series.

---

## 2. What the product IS and IS NOT

| | |
|---|---|
| **IS** | A labeled ESTIMATE of the daily model-AUM series over the gap the measured forward series cannot reach (~05-28→07-21). Rendered yellow-dashed, styled distinctly, tagged `interpolated_estimate` per date. |
| **IS NOT** | A measured fact. It NEVER enters the measured-fact channel — not fee-basis, not the G3 penny identities, not a DDB row any downstream consumer treats as truth. **Display-lane only, until explicitly ruled otherwise.** |

**The forward series (3F-G8b, ~07-21+) stays MEASURED and solid.** This spec fills the tail *behind* it and hands the
join-of-the-two to the FE's provenance-driven styling.

---

## 3. THE HONESTY BOUNDARY — structural, and it reconciles with the fingerprint ban **[the load-bearing section]**

**The fingerprint ban STANDS. It does not block this. The distinction is the LABEL, made structural (CTO gate note 2).**
The measured ban (holdings-basket cosine **0.62–0.98**) killed presenting an *inferred past assignment AS FACT*. This is
a different product category: inference presented **AS interpolation**, never crossing into the fact channel. Four
structural guarantees make that boundary real rather than a promise:

1. **Provenance rides the incumbent channel — and ADOPTION is what makes "extend not invent" TRUE (CTO R-1).**
   `build_aggregate_aua_timeseries.py` carries the `cohort_provenance` channel + a `basis_provenance` block (`:530,:578`),
   empty for Cottonwood today (429/429 None). This spec gives it its first real Cottonwood population **in the
   incumbent's exact vocabulary** (§1a): `interpolated_estimate` over the gap, `measured` over the forward region,
   `absent` before ~05-28. **The 49financial provenance already served IS the channel; interoperating with it — same
   enum, same container, same carrier — is what makes this an extension rather than a look-alike.** A divergent shape
   would be the two-null-semantics defect at the provenance layer; adoption is the honesty, not a claim about it.
2. **Render-gated.** An `interpolated_estimate` point renders ONLY under the Interpolated (yellow-dashed) style, and
   CTO's aggregator derives the firm/Global `point_class = interpolated_estimate` if ANY cohort is interpolated. The FE
   already reads this channel to style estimate vs measured (the 49financial precedent); Cottonwood joins that exact
   path, no second reader.
3. **Compute-quarantined — per provenance class, on the ONE channel (S6 consolidated).** `interpolated_estimate` points
   **NEVER feed** a measured-only consumer (fee basis, DDB truth row, `comp-freshness`, the hard `model_aua +
   non_model_aua == firm_total` identity). Measured identities run on measured points and hard-fail as today; an
   interpolated point gets a **consistency check that WARNS loudly but can never fabricate a pass on the measured
   channel** (CTO companion §3.4). The single enforcement handle is the `cohort_provenance` value itself — every
   measured-only consumer filters on it, exactly as the SMA sleeves are (`cohort_class='sma'` filtered from the model
   stack by the FE, `:434`). **One channel, one filter predicate — no parallel `source` key to keep in sync.**
4. **The absence rule — LEARNED FROM A LOGGED INCIDENT.** `YANG_SITTW.TO-1` (`:420-435`): a rederive once **fabricated a
   non-zero interpolated estimate** ($19.67M @ 2024-11-01) where the true value was **$0** (SMA footprint was zero
   pre-launch), superseding a correctly-emitted `None` and mislabeling real non-model residual as a fake cohort.
   **THE RULE THIS TEACHES, binding on this spec: an interpolation MUST emit null/$0 where the true value is
   $0/absent — never a fabricated non-zero.** The structural ceiling (§5) is the hard absence boundary: no Opal-model
   point before its model existed, interpolated or otherwise.

> **This is what keeps "doesn't need to be exact" from becoming a fabrication vector: inexact-but-labeled-and-quarantined
> is honest; inexact-and-unlabeled-in-the-fact-channel is the incident above. The label is load-bearing, not cosmetic.**

---

## 4. THE MECHANISM — Andrew's sketch is the spine **[PROPOSAL, grounded in measured priors]**

Three stages, backwards from today. **The value leg is strong (measured/reconstructable); the assignment leg is the
estimate (where the label lives).**

### Stage A — Anchor: the current-day roster (DETERMINISTIC)
Start from today's 296 Opal accounts and their current model assignment — which is a **100% deterministic READ**, not a
fit (the determinism brief: `accounts/search.strategyName` cross-validated 17/17, 296==296). This is the one exact
point the whole backwards walk hangs from.

### Stage B — Value trajectory, reconstructed backwards **[strong leg]**
For each account, walk day-by-day backwards:
```
V(account, d-1) = V(account, d) - net_external_flow(d) - market_move(d)
```
- Where a **holdings snapshot exists** (cot silver holdings, back to ~06-08), `V` is **measured** — no reconstruction,
  just read. The snapshot anchors the walk and bounds drift.
- Between/behind snapshots, **`net_external_flow` comes from the transactions feed** — deep to ~03-09 and, critically,
  **HEALTHY: qt2 transactions ran clean tonight** (0.6.2 confirmed qt1/2/3 succeeded 02:03–04Z, same jar/path that
  500s only for qt5/qt4). So the backwards-tracking substrate Andrew pointed at is live and unaffected by the qt5
  freeze. `market_move` is derivable from the held securities' price series.
- **This is the "track the inflows and work it out backwards" leg, and it is the trustworthy one** — it is arithmetic
  on measured flows against a measured anchor, not inference.

### Stage C — Assignment overlay: the fuzzy match **[the estimate leg — labeled]**
Which model was each account on, on past date `d`? No dated assignment source exists (qt5 held; rebalancer live-state
only). So estimate it:
- **Fuzzy-match** the account's reconstructed holdings basket on `d` to the model target baskets → best-match model.
- This is the **cosine-similar match the ban forbids AS FACT** — permitted here **only** because it is emitted
  `interpolated_estimate`, render-gated, and compute-quarantined (§3).
- **Aggregate to TERMINAL models (the B2 rollup), not strategies — and this bounds the fuzzy error to a MEASURED
  per-pair washout coefficient** (computed here from the B2 compositions, per CTO's "make it testable not asserted"
  note). The washout coefficient = the fraction of a misassigned account's value that lands on the SAME terminal model
  regardless of which strategy in the confusable pair it is assigned to:

  | Confusable pair | basket cosine | **washout** | max error | error moves only between |
  |---|---|---|---|---|
  | Sat-50 / Sat-60 | 0.969 | **0.75** | 0.25 | Intermediate ↔ Short |
  | Sat-40 / Sat-50 | — | **0.75** | 0.25 | Intermediate ↔ Short |
  | Sat-30 / Sat-40 | — | **0.75** | 0.25 | Intermediate ↔ Short |
  | Sat-60 / Sat-70 | 0.976 | **0.50** | 0.50 | Conservative ↔ Intermediate |
  | Sat-70 / Sat-80 | 0.981 | **0.50** | 0.50 | Conservative ↔ Intermediate |

  **Raw B2 terminal-model weight vectors (R-6, published so CVO re-derives all 5 first-principles — washout =
  Σ min(w_A,w_B) over terminal models):** Sat-30 = {Int 0.25, Short 0.75} · Sat-40 = {Int 0.50, Short 0.50} ·
  Sat-50 = {Int 0.75, Short 0.25} · Sat-60 = {Int 1.00} · Sat-70 = {Cons 0.50, Int 0.50} · Sat-80 = {Cons 1.00}
  (terminal models: Int = Intermediate-Term, Short, Cons = Conservative Growth; from B2, PROVEN). CVO reproduced
  Sat-50/60 = 0.75; these vectors close the other four.

  **Two measured facts that change the design (and that CVO should re-derive):**
  1. **The error is bounded — a misassignment moves only 25–50% of one account's value, and only between two adjacent
     terminal models, never a whole model.** So terminal-grain aggregation is materially more robust than the raw
     strategy cosine suggests — **confirmed, with numbers.**
  2. **BUT washout is NOT uniform, and cosine does NOT predict it.** The *highest*-cosine pairs (Sat-70/80, Sat-60/70 at
     0.98) have the *worst* washout (0.50), while Sat-50/60 (0.969) washes out at 0.75. Basket-confusability and
     terminal-error-boundedness are **orthogonal axes** — so the confidence treatment (§5) must key on the measured
     per-pair washout, **not** on cosine. Report at terminal-model grain, and carry the pair-specific washout into the
     confidence field.

**All three inputs are held today** (roster, holdings, transactions, model composition) — no new feed, no egress.

---

## 5. CONFIDENCE + THE PERIOD MAP — honest where the match is weak, absent where physics forbids

Per-cohort provenance (§1a.2): the **custody** cohort and the **model** cohort can carry different labels on the same
date — the label marks exactly what is estimated vs measured.

| Period | custody cohort (value) | model cohort (assignment) | Render |
|---|---|---|---|
| **~07-21 →** (forward) | `measured` (3F-G8b) | `measured` (deterministic) | solid |
| **~06-08 → 07-21** | **`measured`** (holdings snapshots) | **`interpolated_estimate`** (fuzzy) | model dashed, custody solid |
| **~05-28 → 06-08** | **`interpolated_estimate`** (flows back from 06-08 anchor) | **`interpolated_estimate`** (fuzzy) | yellow-dashed |
| **before ~05-28** | **`absent`** | **`absent`** | **nothing** (physics) |

(Firm/Global `point_class` derives to `interpolated_estimate` whenever ANY cohort is `interpolated_estimate`, per CTO
companion §2 — but the finer per-cohort labels stay, so the ~06-08→07-21 band honestly shows measured value under an
estimated model split. The `confidence` sibling carries how strong that estimate is, per row.)

**Confidence treatment (CTO gate note 3):** the interpolation is honest about — or absent at — its weak points:
- **Structural ceiling ~05-28 is physics and survives** (models created 05-28→07-17; a quarter of the book on 07-06).
  **No point before an account's model existed** — the absence rule (§3.4) binds hardest here.
- **An account created 07-06 has no interpolated history before 07-06** — it did not exist to reconstruct.
- **Where the fuzzy match is weak** (an account whose basket sits between adjacent tiers with no snapshot to anchor it),
  the design's default is **widen the confidence band or emit the terminal-model blend, never a false-precise single
  model.** The `interp.confidence` field (§1a, mine) is **keyed to the measured per-pair washout coefficient** (§4), not
  to cosine: a Sat-50/60 ambiguity carries higher confidence (0.75 washout) than a Conservative↔Intermediate ambiguity
  (Sat-70/80, 0.50 washout). The FE MAY render the band; it MUST render the label.
- **Account-grain coverage denominator — a transactions HOLE degrades to `absent`, not silently interpolated (CTO note
  2).** The backwards walk states, per account, the dates where `net_external_flow` is derivable vs the gaps. Over a
  transactions gap the account's value cannot be reconstructed, so that account contributes **`absent`** for those dates
  — the same absent-vs-interpolated distinction the aggregation enforces at firm grain, applied at ACCOUNT grain inside
  the method. An interpolation never fills its own substrate's hole silently.
- **Never fabricate a non-zero where the true footprint is zero** (§3.4, the YANG_SITTW rule).

---

## 6. Align to the EXISTING interpolation convention — do not invent a method **[GROUNDED]**

The producer already declares `backfill_method_default: "weekly_interpolation_andrew_20260518"` (`:52`) and the
49financial partner already carries a working `{measured | interpolated_estimate}` provenance split. **Cottonwood's
interpolation should extend that established convention, not fork a new one** — same provenance vocabulary, same
`basis_provenance` block shape, a Cottonwood-specific `backfill_method` tag (e.g. `cot_snapshot_flow_fuzzy_20260723`)
added to the `backfill_methods` union. This is the internal analogue of the METHOD-vs-NUMBERS split: align the method
to the incumbent house convention; compute the numbers on Cottonwood's own data.

---

## 7. SUPERSESSION — measured beats interpolated, and the source-keying already handles it **[GROUNDED]**

qt5's HELD-ON-FEED status is an **input, not a blocker** (CTO gate note 5). If the qt5 feed repair (0.6.2's lane) later
yields real *temporal* assignment, or the forward series simply extends, **measured points SUPERSEDE
`interpolated_estimate` ones per `(firm, model, date)`** as an **evented re-emit** (CTO companion §3.3) — precedence
`measured (datamining-backfill | daily-snapshot) > interpolated_estimate`.
- **The overlay window SHRINKS automatically** because it derives from the per-cohort `cohort_provenance`, not from a
  stored config — no window to hand-edit. Supersession is never silent: it is an evented re-emit with the `meta` diff
  named (`superseded_dates[]`).
- **Safe-supersession rule (from the YANG_SITTW incident, §3.4):** a superseding value must itself be **`measured`**; an
  `interpolated_estimate` may NEVER supersede a correctly-emitted null/`absent` (that was the exact 2024-11-01 fault).
  One-directional: `interpolated_estimate → measured`, never the reverse.
- So the interpolated band is **provisional by construction** — it fills the gap honestly today and **dissolves from the
  bottom up** as real data lands, with no rewrite of the series contract.

---

## 8. Validation the build must carry **[PROVEN feasible]**

1. **Per-date firm-total honesty (consistency check, WARN-not-hard-fail on the interpolated class):** even interpolated,
   the model band must not exceed the account universe that existed on `d` (Σ interpolated model_value ≤ reconstructed
   firm total on `d`, components sum). Per CTO companion §3.4 this WARNS loudly on the interpolated class and can never
   fabricate a pass on the measured channel; an interpolation that invents AUM beyond the reconstructed book is the
   fabrication class.
2. **Absence guard — the floor is a machine-checked `max(...)`, not prose (CTO R-3 / CVO M8):** every point's floor is
   **`max(model_creation_date, account_first_existence_date)`** — an account cannot carry an interpolated model point
   before EITHER its model existed OR it existed. This is enforced as **TWO INDEPENDENT LOCKS**: the producer refuses to
   emit below the floor, AND the schema validator independently refuses. Either firing is LOUD; a non-null point below
   the floor is the fabrication class (the direct YANG_SITTW guard). **Prose is not a gate — this lives in the validator.**
3. **Continuity at the seam:** the interpolated tail must join the measured forward series at ~07-21 without a
   discontinuity that is an artifact of the method rather than the data (a step at the seam is a flag).
4. **Provenance completeness + no parallel-array split (CVO mutant):** every affected date carries an inline
   `provenance` on its value tuple; no interpolated point renders solid, no measured point renders dashed; and a planted
   interpolated point MUST be rejected by every measured-only consumer and MUST render with the overlay (CTO §3.1 mutant).
5. **Terminal-model tie:** the interpolated terminal-model split reconciles to the reconstructed account values at the
   B2 composition weights (the same rollup that ties measured to the penny), within a stated, labeled tolerance.

---

## 9. What's proposed, held, decided — and by whom

- **PROPOSED (CRO):** the design above — a labeled, provenance-quarantined, display-lane interpolated Cottonwood
  model-AUM band over ~05-28→07-21, value-reconstructed backwards + fuzzy-assignment overlay at terminal-model grain,
  extending the existing `cohort_provenance`/`weekly_interpolation` machinery, superseded by measured data.
- **FOR CVO REVIEW (3.0.0_SA_CVO):** the honesty boundary (§3) is the review's crux — is the quarantine structural
  enough that "doesn't need to be exact" cannot leak into a measured-fact channel? The absence guard (§8.2) and the
  fingerprint-ban reconciliation (§3) are the specific things to adversarially test.
- **FOR COO DECOMPOSITION (2.0.0_SA_COO):** the build TO — producer placement (`data/assets/scripts`, the deploy-map
  hazard), the FE styling work (yellow-dashed + confidence band), sequencing against 3F-G8b (the forward series is the
  seam the interpolation joins) and the MDPF revamp.
- **CTO gates:** the apply, and the display-lane→wider-use boundary if it is ever proposed to move.
- **NOT this spec's to do:** build, dispatch, register, or move served output.

---

## 10. Grounding

**[GROUNDED]** `cohort_provenance[]` + `basis_provenance` + `interpolated_1c` + the `YANG_SITTW.TO-1` fabrication
incident + `backfill_method_default: weekly_interpolation_andrew_20260518` + `by_model{cohort_class,model_value,
account_count}` (all `build_aggregate_aua_timeseries.py`, read this session) · qt2 transactions healthy tonight (0.6.2
02:03–04Z) · holdings horizon ~06-08, transactions ~03-09 (prior S3 listings). **[PROVEN]** current membership
deterministic 17/17 296==296 (determinism brief); B1/B2 terminal-model composition + the penny-tie; basket cosine
0.62–0.98 (enriched brief); **the terminal-model washout coefficients (0.50–0.75 per confusable pair, computed this
session from the B2 compositions) — and the orthogonality of cosine and washout.** **[PROPOSAL]** the backwards value
reconstruction, the fuzzy assignment overlay, and the confidence treatment (now keyed to the measured washout) — CVO's
to review + re-derive, none built.

**One-line:** extend the estate's existing labeled-interpolation machinery to Cottonwood — measured value reconstructed
backwards, assignment fuzzy-estimated, everything tagged `interpolated_estimate`, render-gated yellow-dashed,
compute-quarantined, absent before ~05-28, and superseded by measured data the moment it arrives — so the gap is filled
honestly instead of either left blank or fabricated as fact.
