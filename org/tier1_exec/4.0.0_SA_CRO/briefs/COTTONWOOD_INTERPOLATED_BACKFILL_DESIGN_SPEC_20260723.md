# Cottonwood Interpolated Model-Backfill — Design Spec

**Author:** `4.0.0_SA_CRO` (Chief Research Officer) · **Home:** `org/tier1_exec/4.0.0_SA_CRO/` · **Date:** 2026-07-23
**Chain (Andrew-ordered):** this spec → **`3.0.0_SA_CVO` review (schema verified in tandem with CTO's companion)** →
**`2.0.0_SA_COO` TO decomposition.** CTO + COO CC.
**Companion (the aggregation half):** CTO's `GLOBAL_INTERPOLATED_AGGREGATION_SPEC_20260723.md` @7ed8a6fd0 — its **§4 is
the SHARED SCHEMA this spec emits against.** CVO verifies the one schema across both before either builds.
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

## 1a. THE SHARED SCHEMA — I emit against CTO's companion contract (his §4) **[CONTRACT, not mine to change]**

CTO pre-committed the honesty envelope so both halves decompose as one program. **My producer emits the firm-level
tuples; his Global aggregator derives `point_class` + the meta block; the FE reads it — one provenance source of
truth, no re-derivation.** The per-date Global entry:

```
{ date, model_aua, non_model_aua, total,
  by_firm: { cottonwood: { model_aua, non_model_aua,
                           provenance: "interpolated",           // legal: measured | interpolated | absent
                           interp: { method_version, confidence, window_id } } },
  point_class: "interpolated"   // DERIVED by CTO's aggregator: any-component-interpolated
}
```

**Three bindings this puts on my emitter, non-negotiable (they are CVO's mutant surface):**
1. **Values and provenance ship in ONE dated tuple — never parallel arrays.** I do not populate a separate
   `cohort_provenance[]` array a consumer could read without the value (that split is a planted CVO mutant). The
   `cohort_provenance` channel is the *carrier concept*; the *shape* is the inline `by_firm.cottonwood.provenance`
   tuple above.
2. **`provenance` value is `interpolated`** (not `interpolated_estimate` — I am aligning my vocabulary to the contract).
3. **`interp.confidence` is MINE to define** (the churn-measured degradation, §5); `method_version` + `window_id` I
   also supply; the FE MAY render confidence, MUST render the label. `meta.interpolation = {affected_period:[start,end],
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

1. **Provenance rides EACH value inline (per §1a) — and the carrier channel already exists.**
   `build_aggregate_aua_timeseries.py` carries the `cohort_provenance` channel + a `basis_provenance` block (`:530,:578`),
   empty for Cottonwood today (429/429 None). This spec gives it its first real Cottonwood population — but in the
   **inline-tuple shape** of §1a (`by_firm.cottonwood.provenance = interpolated`), **not** a parallel array. `measured`
   over the forward region, `interpolated` over the gap, `absent` before ~05-28. **Extending an existing,
   Andrew-established labeling channel, not inventing one.**
2. **Render-gated.** An `interpolated` point renders ONLY under the Interpolated (yellow-dashed) style, and CTO's
   aggregator taints the Global point `interpolated`-class if ANY component is interpolated. The FE already reads
   provenance to style estimate vs measured (the 49financial precedent); Cottonwood joins that path.
3. **Compute-quarantined — per provenance class.** Interpolated points **NEVER feed** a measured-only consumer (fee
   basis, DDB truth row, `comp-freshness`, the hard `model_aua + non_model_aua == firm_total` identity). Measured
   identities run on measured points and hard-fail as today; an interpolated point gets a **consistency check that WARNS
   loudly but can never fabricate a pass on the measured channel** (CTO companion §3.4). The `source=interpolated`
   keying is the enforcement handle, filtered out of every measured aggregation exactly as the SMA sleeves are
   (`cohort_class='sma'` filtered from the model stack by the FE, `:434`).
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
- **Aggregate to TERMINAL models (the B2 rollup), not strategies — and this materially shrinks the fuzzy error.** The
  confusable strategies (Sat-50↔60, cosine 0.969) map to **overlapping terminal models** (Sat-50 = 75% Intermediate +
  25% Short; Sat-60 = 100% Intermediate — B1). Misassigning between adjacent Satellites moves only the *residual*
  Int/Short split, not a whole model — so at the terminal-model level the interpolation is **more robust than the raw
  strategy-level cosine suggests.** Report at terminal-model grain for this reason.

**All three inputs are held today** (roster, holdings, transactions, model composition) — no new feed, no egress.

---

## 5. CONFIDENCE + THE PERIOD MAP — honest where the match is weak, absent where physics forbids

| Period | Value leg | Assignment leg | `provenance` | Render |
|---|---|---|---|---|
| **~07-21 →** (forward) | measured (3F-G8b) | measured (deterministic) | `measured` | solid |
| **~06-08 → 07-21** | **measured** (holdings snapshots) | **interpolated** (fuzzy) | `interpolated` | yellow-dashed |
| **~05-28 → 06-08** | **reconstructed** (flows back from 06-08 anchor) | **interpolated** (fuzzy) | `interpolated` | yellow-dashed |
| **before ~05-28** | — | — | **`absent`** | **nothing** (physics) |

(A value-real / assignment-estimated point is `interpolated`-class — any interpolated component taints the point, per
CTO companion §2. The `interp.confidence` field carries how strong that estimate is, per row.)

**Confidence treatment (CTO gate note 3):** the interpolation is honest about — or absent at — its weak points:
- **Structural ceiling ~05-28 is physics and survives** (models created 05-28→07-17; a quarter of the book on 07-06).
  **No point before an account's model existed** — the absence rule (§3.4) binds hardest here.
- **An account created 07-06 has no interpolated history before 07-06** — it did not exist to reconstruct.
- **Where the fuzzy match is weak** (an account whose basket sits between adjacent tiers with no snapshot to anchor it),
  the design's default is **widen the confidence band or emit the terminal-model blend, never a false-precise single
  model.** A `confidence` scalar per interpolated point is recommended so the FE can render the band, not just the line.
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
yields real *temporal* assignment, or the forward series simply extends, **measured points SUPERSEDE interpolated ones
per `(firm, model, date)`** as an **evented re-emit** (CTO companion §3.3) — via the `source` precedence
`measured (datamining-backfill | daily-snapshot) > interpolated`.
- **The overlay window SHRINKS automatically** because it derives from the per-point `provenance`, not from a stored
  config — no window to hand-edit. Supersession is never silent: it is an evented re-emit with the `meta` diff named
  (`superseded_dates[]`).
- **Safe-supersession rule (from the YANG_SITTW incident, §3.4):** a superseding value must itself be **measured**; an
  interpolated estimate may NEVER supersede a correctly-emitted null/absent (that was the exact 2024-11-01 fault).
  One-directional: `interpolated → measured`, never the reverse.
- So the interpolated band is **provisional by construction** — it fills the gap honestly today and **dissolves from the
  bottom up** as real data lands, with no rewrite of the series contract.

---

## 8. Validation the build must carry **[PROVEN feasible]**

1. **Per-date firm-total honesty (consistency check, WARN-not-hard-fail on the interpolated class):** even interpolated,
   the model band must not exceed the account universe that existed on `d` (Σ interpolated model_value ≤ reconstructed
   firm total on `d`, components sum). Per CTO companion §3.4 this WARNS loudly on the interpolated class and can never
   fabricate a pass on the measured channel; an interpolation that invents AUM beyond the reconstructed book is the
   fabrication class.
2. **Absence guard — TWO LOCKS (the YANG_SITTW test, schema-enforced per CTO §3.2):** the producer refuses to emit, AND
   the schema validator independently refuses, any interpolated point before each model's creation date or before each
   account's first-existence date. Two independent locks, either firing LOUD; a non-zero there is the fabrication class.
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
0.62–0.98 (enriched brief). **[PROPOSAL]** the backwards value reconstruction, the fuzzy assignment overlay, the
terminal-model-washout robustness claim, and the confidence treatment — CVO's to review, none built.

**One-line:** extend the estate's existing labeled-interpolation machinery to Cottonwood — measured value reconstructed
backwards, assignment fuzzy-estimated, everything tagged `interpolated_estimate`, render-gated yellow-dashed,
compute-quarantined, absent before ~05-28, and superseded by measured data the moment it arrives — so the gap is filled
honestly instead of either left blank or fabricated as fact.
