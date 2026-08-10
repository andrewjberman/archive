# ECLIPSE VINTAGE RECONSTRUCTION — D3: RECONSTRUCTION SPEC (resequenced per CTO 20260810T222502Z)

**archetype:** IMPLEMENT (spec, with steps 1–2 EXECUTED)
**Author:** `0.2.0_DS_PortfolioAnalytics` · 2026-08-10 ~2250Z
**Prereqs:** D1+D2 @e8c219b9ca (accepted), grain addendum @38b236dbf0 (accepted, FEASIBLE AT MODEL
GRAIN recorded). **CTO resequence honored: the proxy-grain join is the PRECONDITION, and D4 re-runs
at `INFLECTION_MODEL_KEYS` grain — both are executed below, not promised.**
**Ruled properties implemented:** derived artifact is DISTINCT, SELF-NAMING, OPT-IN;
`point_class: "reconstructed"` (never `measured`); carries method version + tie-out error + fwd/bwd
residual; not bronze (17a) / not silver (17) / not the normal gold path. **Nothing is served
without a separate CTO ruling.**

---

## 1 · SCOPE

One vintage: **2026-08-05, firm inflection** — the eclipse MODEL leg at the seven
`INFLECTION_MODEL_KEYS`, plus firm aggregate and per-client values. The six historic `absent`
points are out of scope absent an Andrew/CTO word.

## 2 · STEP 1 (EXECUTED) — THE JOIN, WITH DENOMINATORS

Chain: eclipse `fact_portfolios_full.{id,modelId,totalValue}` → `fact_portfolios_simple.{id →
accountId}` (the orion join key the puller pulls /simple for) → orion `fact_assets.{accountId →
clientId}` → `fact_performance` client factor. `modelId → model_key` via the CANONICAL crosswalk
(`data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py::resolve_eclipse_id` — reused, not
re-coined; Build-Ladder rung 2).

**Coverage, measured (partition 2026-08-04, the tie-out base):** 562 Opal-key portfolios
($143,810,780) → 551 joined to a client → 551 carry factors. **UNMAPPED RESIDUAL: $0.00 across 11
portfolios** (all zero-value) — reported, not distributed. Partition 2026-08-05 base: 561
portfolios, same shape, unmapped residual $0.00 across 11.

## 3 · STEP 2 (EXECUTED) — D4 RE-RUN AT KEY GRAIN, flow-unadjusted honest numbers

Reconstruct vintage 2026-08-04 (from partition 08-04 = vintage 08-03, ratio f(08-04)/f(08-03))
vs actual (partition 08-05), per key:

| model_key | actual | recon | err (bp) |
|---|---|---|---|
| opal_ultra_short_term | 964,229.32 | 968,173.40 | +40.90 |
| opal_short_term | 6,539,286.74 | 6,550,663.82 | +17.40 |
| opal_intermediate | 77,219,268.57 | 77,251,109.09 | +4.12 |
| opal_long_term_conservative | 14,393,413.29 | 14,589,328.34 | **+136.11** |
| opal_long_term_aggressive | 2,313,319.72 | 2,321,306.29 | +34.52 |
| opal_blend_5050_int_ltc | 36,164,497.15 | 36,139,027.06 | −7.04 |
| opal_blend_5050_st_int | 7,288,386.21 | 7,291,411.55 | +4.15 |

**Aggregate (model leg): +15.78bp. Value-weighted mean |err| at KEY grain: 19.30bp.**

Read honestly: key grain is HARDER than orion's modelName grain (19.30bp vs 9.74bp) because the
client factor blends the client's whole book while an eclipse portfolio is only the Opal slice,
and because flows are not yet adjusted. The 136bp `opal_long_term_conservative` cell is a ~$196K
overshoot with a flow/transfer signature inside the tie-out window — exactly what Step 3 targets.
**This is the number the consumer would experience TODAY, pre-flow-adjustment; the spec does not
promise a smaller one until the calibration run measures it.**

## 4 · STEP 3 — FLOW + REASSIGNMENT ADJUSTMENT (the one unbuilt piece)

From orion `fact_transactions` at the vintage date: value-moving categories (Client
Contribution/Distribution, Merge In/Out, Federal Tax Withheld, Management Fee, Trading Expense);
NOT Buy/Sell pairs (net zero), NOT Dividend/Income rows (priced by the factor). Timing convention
(start-vs-end-of-day) is **calibrated on the known day, not assumed** — frozen into the method
version. **Reassignment handling (CTO class-warning, the cottonwood signature):** portfolios whose
`modelId` or account membership DIFFERS between the two flanking eclipse snapshots (08-05 vs
08-07 partitions) are flagged, attributed at the earlier snapshot, and the moved value is named in
`_meta` — a membership change inside the window breaks the roll identity and must surface, never
be absorbed. The **forward leg stays the published leg**; the backward roll (flows removed first)
is the in-run cross-check whose residual is reported in the artifact.

## 5 · THE DERIVED VALUES (current best, flow-unadjusted, `point_class: "reconstructed"`)

Vintage 2026-08-05, forward roll from vintage 08-04, per key — bracketed by the two captured
neighbors for sanity:

| model_key | vintage 08-04 (measured) | **08-05 (DERIVED)** | vintage 08-06 (measured) |
|---|---|---|---|
| opal_ultra_short_term | 964,229 | **963,631** | 965,175 |
| opal_short_term | 6,539,287 | **6,537,554** | 6,537,458 |
| opal_intermediate | 77,219,269 | **77,162,594** | 77,044,017 |
| opal_long_term_conservative | 14,393,413 | **14,375,230** | 14,344,141 |
| opal_long_term_aggressive | 2,313,320 | **2,311,927** | 2,306,209 |
| opal_blend_5050_int_ltc | 36,164,497 | **36,129,681** | 36,065,634 |
| opal_blend_5050_st_int | 7,288,386 | **7,285,696** | 7,282,566 |
| **model-leg total** | 144,882,401 | **144,766,312** | 144,545,200 |

Firm aggregate (orion custody basis, from D1): **$209,293,175.65** derived vs $209,431,383.43
(vintage 08-04) and $208,325,960.35 (vintage 08-06).

## 6 · THE DERIVED ARTIFACT — proposed prefix for ratification

```
s3://opal-data-assets/eclipse/inflection/reconstructed/vintage=2026-08-05/reconstruction.json
```
- **Self-naming:** `reconstructed` occupies the medallion-tier slot and is none of
  bronze/silver/gold — no medallion-pattern reader can sweep it.
- **Opt-in by construction:** 0 existing read paths touch this prefix (nothing globs it today).
- **Grammar-conformant:** stays inside `{vendor}/{firm}/…`; a new segment, not a new root.

Payload: `vintage`, `point_class: "reconstructed"`, `method_version`, per-key + firm + per-client
estimates, `tieout` block (gate-day numbers, embedded), `residual` (fwd/bwd), `flows_applied`,
`sources` (every S3 key + LastModified), `authorization` pointers (brief @7b76f32562, Andrew-direct
egress record in D1 §0, CTO acceptance messages, this spec's commit).

## 7 · D4 — THE ACCEPTANCE GATE (inside the emitter, every run, at KEY grain)

Before emitting, the same code reconstructs vintage 2026-08-04 at `INFLECTION_MODEL_KEYS` grain
and prints denominators (portfolios, joined, factored, unmapped-residual $).
**Gate thresholds are FROZEN FROM THE CALIBRATED KNOWN-DAY RUN at implementation** (the
flow-adjusted numbers), ratified together with the prefix — proposed shape: aggregate ≤10bp,
value-weighted ≤25bp, any single key ≤50bp, else rc≠0 and no artifact is written. The
flow-unadjusted baseline above (15.78/19.30/136) is the number to beat; **if the flow adjustment
cannot bring `opal_long_term_conservative` under the single-key bar, the gate fails and that is a
finding, not a threshold to relax silently.**

## 8 · NOT AUTHORIZED BY THIS SPEC

No serving change. No historic-gap backfill. No standing pipeline (one-shot ad-hoc QA-class
emission; recurrence is the D-15 schedule question, not mine). No bronze/silver/gold writes.
No further vendor calls (every input is already in S3).

## Compiler Tools

| tool | result |
|---|---|
| `comp-find "INFLECTION_MODEL_KEYS"` | located the DEF + crosswalk (15 hits, denominator printed by tool) |
| `mdpf_revamp_model_crosswalk.resolve_eclipse_id` | REUSED as the canonical modelId→key map (rung 2) |
| raw S3 reads | operational data-plane pulls of our own partitions for the executed steps |
