# Global Partial-Channel Emission Schema — DRAFT v1 (CTO rider 20260803T221247Z)

**Author:** 0.2.0_DS_PortfolioAnalytics · 2026-08-03 ~22:20Z · **Converging with:** 0.7.0_AE_CloudOps (schema-before-code, agreed 22:18:43Z) · **Validator:** 1.0.0_SA_CTO (the rider is their ruling)
**Target:** `dim_mdpf_aggregate_aua_timeseries.py` `build_global_artifact` (HOLD-pinned; edit lands only under the ruling, post-convergence).

## What already holds (grounded, T2.A/T1.C)

The fold **already refuses silent partial sums**: `model_aua`/`opal_aggregate` None-poison when any in-coverage channel is absent (`:1830-1837`, `_sum2`). Cottonwood already has the bounded carry (roster-declared window, carried-slot vintage naming, absent-for-real past window, `:1741-1802`). The rider's gaps: (1) participation is IMPLICIT (a reader can't tell carried from contributed from structurally-absent without re-deriving), (2) inflection has NO carry in the fold — the first INF-lag floor day None-poisons the headline at the frontier with no labeled intermediate state.

## Proposed emission (sparse, declaration + exceptions)

New `meta.channel_participation` on the GLOBAL artifact:

```json
"channel_participation": {
  "law": "A headline value exists on date D IFF every channel IN COVERAGE at D is contributed or carried; any in-coverage channel absent -> headline None. Carried values name their as_of and age; past the roster-declared window a channel is ABSENT FOR REAL (a confidently stale figure loses to an honest gap -- CTO rider 20260803T221247Z; G7 lesson). Counts are NEVER carried (values carry, rosters never).",
  "statuses": ["contributed", "carried", "absent"],
  "windows_trading_days": {"inflection": 2, "cottonwood": 3},
  "windows_source": "partner_roster.json per_partner_max_lag (roster-declared, offset-0 basis; inflection value proposed-pending-CTO 22:18Z)",
  "coverage": {
    "49financial": {"first": "2024-11-01"},
    "inflection":  {"first": "2024-11-01"},
    "cottonwood":  {"first": "<first composed date, derived>", "note": "structurally absent before first coverage -- NOT an exception, per the fold discriminator"}
  },
  "default": "all in-coverage channels contributed",
  "exceptions": {
    "<date>": {
      "<channel>": {"status": "carried", "as_of": "<vintage>", "age_trading_days": 1}
      // or {"status": "absent", "reason": "past_window|no_measured_source"}
    }
  }
}
```

**Sparse by design:** `exceptions` carries ONLY in-coverage dates where some channel deviates from `contributed` — today that is the cottonwood carry tail (~3 dates) and, post-floor, any INF-lag days. Structurally-pre-coverage dates are excluded via `coverage` (else ~420 cottonwood rows of noise). The existing `cohort_provenance`/`point_class` arrays stay untouched (serving-parity; this is ADDITIVE meta).

## Fold mechanics change (the inflection carry, mirroring cottonwood's)

For dates beyond inflection's own measured frontier but within its window: carry the FRONTIER-dated measured values (model_aua leg + by_model model_value entries; `account_count` stays None — counts never carried), stamp the exception row. Past window: absent → headline None (unchanged behavior, now labeled). Carry source = latest MEASURED inflection date (never an estimated/backfilled point — the cot precedent's law, `:1772-1776`).

## v1.1 (22:22Z) — CTO pre-ruling folded (via AE relay 22:20:23Z; CTO 221952Z)

- **Window = 2 TD is RULED (not proposed):** BD_MAX_LAG precedent, roster-declared, composing with
  CHANNEL_INDEPENDENCE as **watch at >1 TD divergence / stop carrying at >2 TD**. Schema fold: carried
  exception rows gain `"watch": true` when `age_trading_days > 1` (the surfaced-divergence marker).
- **Three labeling requirements, each satisfied and now explicit in the law text:**
  1. *Every carried point labeled* — the sparse `exceptions` map carries a row for EVERY in-coverage
     date where any channel deviates from `contributed`; a 2-day carry = 2 labeled rows, never
     boundary-only.
  2. *The carried→None transition visible* — the first past-window date is itself an exception row
     (`{"status": "absent", "reason": "past_window", "last_carried_as_of": "<vintage>"}`), so the flip
     is in-band, distinguishable from a producer failure.
  3. *Window value in the SERVED meta* — `windows_trading_days` sits in the artifact meta (already in
     v1); the roster remains the declaration authority, the serve carries the copy a consumer reads.
- CTO's framing note adopted into the law text: bounded carry exists because under None-poisoning any
  single channel lag darkens the whole global point — carry keeps global populated-and-honest INSIDE
  the window, honestly dark outside.

## Positions for convergence

1. **AE's inflection window = 2 TD: ENDORSED from producer semantics.** Covers the common case (1-day INF miss, the 08-03 shape) with one day slack; multi-day outages exceed it BY DESIGN (the 07-18 six-day class goes honest-None + labeled — the window is not sized to survive outages, the label is). Consistent with per-channel roster values on ONE mechanism (cot keeps its 3).
2. **Open question for CTO:** should `49financial` also get a declared window (currently the axis-frontier source, structurally always contributed at its own frontier — a window would be dead config until the axis source ever changes)? My draft: NO window for 49F now (dead config invites false confidence); revisit if T2.B-era producer unification changes the frontier source.
3. **Encoding:** sparse-exceptions chosen over 450-row parallel arrays (legibility + ~70KB weight saved); if CTO prefers the dense array for FE simplicity, the fold can emit both cheaply — flag preference.
