# MDPF_VARFLAG — 8-Month Backtest of the Proportional Guard (49 weekly vintages)

**Author:** 3.0.0_SA_CVO · 2026-07-17 ~15:4xZ
**Data:** all 49 archived weekly PKLs `s3://opal-data-portal-v2/benchmarks/data_YYYYMMDD_v1.pkl`
(2025-11-28 → 2026-07-17; 48 consecutive transitions), including the corrupt
`data_20260716_v1.pkl` (.ST Index CIX substitution) and the January year-boundary.
**Method:** per vintage, per security (84 `index_name` series in `return_daily`): YTD return,
1Y return, YTD vol, 1Y vol (compounded daily; vol annualized √252) — 336 cells per transition.
Rule under test: `|Δ| / max(|prior|, 1pp) > threshold`. Script: session scratchpad `backtest.py`.

## Headline: VOLATILITY-change is a near-perfect substitution detector; raw 25% on returns cries wolf

| rule (security level) | healthy flags, 8 months (46 transitions) | Jan boundary | corrupt vintage |
|---|---|---|---|
| 25% on all 4 stats | 2,097 (mean **46.6/week**) | 153 | 22 |
| 400% on all 4 stats | 51 (1.1/week) | 2 | 4 |
| **vol-change > 100%** | **2 total (0.04/week)** | **0** | **2/2 (766%, 679%)** |
| **vol-change > 200%** | **0 in 8 months** | **0** | **2/2** |

**Mechanism:** volatility is a property of the series' identity. A wrong-security substitution
slams vol by 3–10× (Short Term: 2.58 → 22.35); real markets move returns week-to-week but almost
never multiply a diversified series' realized vol overnight. Returns near zero, by contrast, swing
>25%-of-prior routinely (46.6 flags/week at the security level — Natural Gas, crypto, country
indices dominate the recurrers).

## Layer results

1. **Model-level 25% (Andrew's rule on the served cells):** from the earlier served-vintage scan —
   0 flags on the healthy weekly transition, 13/13 on the corrupt vintage. Model aggregates are
   damped; the rule works AS STATED there. Caveat honestly held: served history only spans 07-01,
   so only one healthy weekly pair was observable — the shadow phase accumulates the rest.
2. **Security-level vol >100–200% (the input-side tripwire):** zero-to-two false flags in EIGHT
   MONTHS, catches the substitution class cold. Composable with `validate_data_pkl.py`
   @`2d62804b6` (same layer, same family — this adds the cross-vintage axis to its
   within-vintage ceilings).
3. **January YTD boundary — MEASURED, prediction confirmed:** 20251231→20260109 = 153 flags at
   25%, of which 136 are YTD cells. Any YTD-comparing rule needs the year-boundary pre-registered
   (suppress or re-baseline YTD comparisons on the first uploads of a year) or the guard's first
   January is a wall of false flags.
4. **Cadence reality (for exit criteria):** 8 zero-flag transitions are same-week re-uploads
   (byte-near-identical); true cadence is ~weekly with occasional multi-upload weeks — "prior" must
   be the last ACCEPTED vintage, confirmed again.

## Recommended final guard (evidence-backed, drops into MDPF_VARFLAG unchanged architecture)

- **G1 — served-cell gate (the acknowledge screen):** 25% proportional vs last accepted vintage,
  `max(|prior|, 1pp)` denominator, slow cells only (YTD/1Y/3Y/5Y/SI + vols + AUM), spreads as
  derived annotations, year-boundary pre-registered. Evidence: 0/13 separation on served history.
- **G2 — security-level vol tripwire (input side, silent-strong):** per-security realized-vol
  change >100% vs last accepted PKL → flag. Evidence: 0.04 false/week over 8 months, 2/2 on the
  corrupt pkl. This is the layer that catches a substitution even when model aggregation dilutes it.
- **G3 — static domain bounds** on fast cells; **G4 — structural sentinel** with the
  conditional-cells allowlist (WTD-vol family) + peer-universe change as one flag.
- Shadow-phase exit criterion, now calibratable from data: G1+G2 combined false-flag budget
  ≤2/upload sustained — consistent with what 8 months of history shows is achievable.

— 3.0.0_SA_CVO
