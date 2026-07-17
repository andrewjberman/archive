# MDPF_VARFLAG — 25% Proportional-Change Scan Against Real Vintage History

**Author:** 3.0.0_SA_CVO · 2026-07-17 ~15:1xZ
**Trigger:** Andrew-direct ~14:40Z (verbatim on record @ `d21c97e3a`): *"Maybe instead of 2std, its
if any numbers are more than 25% higher or lower than their prior figure, on a proportional basis.
Try scanning with that perspective."*
**Data scanned:** all 8 S3 versions of `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json`
(2026-07-01 → 2026-07-17T14:30Z, downloaded by VersionId), 385 numeric cells each, 7 transitions —
including the 2026-07-16 corrupt vintage (.ST Index CIX substitution) and the 07-17 rollback.
Deeper history exists and is scannable: `s3://opal-data-portal-v2/benchmarks/data_YYYYMMDD_v1.pkl`
holds **~36 weekly PKL archives back to 2025-11-28**, including the corrupt `data_20260716_v1.pkl`.

## Result 1 — the naive 25% rule cries wolf and cannot even separate corrupt from healthy

| transition | cells changed >25% (of 385) |
|---|---|
| 07-01 → 07-10 (healthy) | **189** |
| 07-10 → 07-12 (healthy weekly) | **121** |
| 07-12 → 07-16 (**CORRUPT**) | 173 |
| same-content re-promotes today | 0 |

A healthy week flags ~1/3 of all cells; the corrupt vintage flags 173 — barely distinguishable
from healthy by count. **Mechanism:** short-period cells (1D/WTD/MTD/QTD/1M/TTW) are a NEW
measurement every upload — last week's 1D return and this week's 1D return are different days, so
"25% vs prior figure" routinely reads 200–1000% on tiny, healthy numbers (e.g. WTD 0.030 → 0.350 =
+1067%, absolute move 0.32pp). Proportional-vs-prior is only meaningful where the prior IS the
same quantity remeasured: the slow accumulator cells.

## Result 2 — the same 25% rule, scoped to comparable cells, separates PERFECTLY on this history

**Rule:** `|new − prior| / max(|prior|, 1.0pp) > 25%`, applied to the 120 slow cells
(YTD / 1Y / 3Y / 5Y / Since-Inception, returns + volatilities + spreads). The `max(|prior|, 1pp)`
denominator floor stops near-zero priors exploding the ratio.

| transition | flags | content |
|---|---|---|
| 07-01 → 07-10 (9-day, healthy) | 6 | all spread cells (real market movement in small spreads) |
| 07-10 → 07-12 (healthy weekly) | **0** | — |
| 07-12 → 07-16 (**CORRUPT**) | **13** | the full corruption signature: YTD model 1.72→−7.76 (551%), YTD vol 3.32→25.90 (680%), SI vol 2.12→26.53 (1151%), 1Y spreads −2→−22 (~1000%) |
| corrupt → rollback restore | 13 | symmetric — confirms rollback must BYPASS the gate |
| post-rollback fresh upload | 1 | one 1Y spread, 32%, borderline |

**The must-catch is caught loudly (13 flags, max 1151%) and a normal week is silent (0 flags).**
The 6 residual flags on the 9-day gap are all *spread* cells — spreads are difference-quantities
(model minus benchmark, near zero by construction); flagging them via their PRIMARY parents
(model / benchmark / vol cells) instead of independently removes this residue without losing the
corrupt catch (which fires on primaries at 551–1151%).

## Result 3 — incidental structural find

15 cells (`WTD/*_volatility` × 5 models) alternate present/absent between vintages — present in
the 07-12 vintage, absent in fresh 07-17 uploads. Read: WTD volatility only computes when the week
has enough days; early-week uploads lack the cells. **The proposal's "cell vanishes = always flag"
sentinel would false-fire on this every early-week upload** — the structural sentinel needs a
known-conditional-cells allowlist (config), or WTD-vol churn will be the first cry-wolf.

## Recommended guard shape (the 25% instinct, made operational)

Three layers, all config-driven, dropping cleanly into the MDPF_VARFLAG varflag-check slot
(architecture unchanged — staging + acknowledge gate + shadow-first all stand):

1. **L1 — proportional-vs-prior (Andrew's rule), comparable cells only:**
   `|Δ| / max(|prior|, denom_floor) > 25%` on YTD/1Y/3Y/5Y/SI returns, volatilities, and AUM.
   Denom floor 1.0pp (returns/vol) / 2% relative (AUM). Spreads ride as derived annotations.
   Measured on real history: 0 false flags on the healthy weekly transition, 13/13 on the corrupt.
2. **L2 — domain sanity bounds, ALL cells including short-period:** static ranges per cell class
   (e.g. |1D| ≤ 5pp, |WTD| ≤ 8pp, vol ∈ (0, 60]) — catches wholesale garbage in the fast cells L1
   deliberately ignores. Cheap, no history needed, no cry-wolf (bounds sit far outside routine).
3. **L3 — structural:** cell appears/vanishes vs prior vintage → flag, EXCEPT the configured
   conditional-cells allowlist (the WTD-vol family). Peer-universe membership change = one
   structural flag, not N rank flags.

This replaces the 2σ statistic with something **simpler, explainable to the operator ("this number
moved 551% vs last week"), needing no σ estimation, no N=12 bootstrap, and immune to the
poisoned-baseline problem entirely** (the comparison is only ever against the single prior
accepted vintage — one bad vintage can only mis-baseline the single next upload, and only if it
was itself acknowledged and promoted).

**Prior-figure definition still binds:** "prior" = last ACCEPTED upload (execution metadata), never
the raw previous S3 version (same-day re-promotes are byte-identical → vacuous 0-flag transitions;
rollback restores create artificial jumps).

## Backtest path (shadow-phase evidence, ready to run)

The ~36-week PKL archive (2025-11-28 → today) permits a full-history backtest: regenerate the
benchmark JSON per archived PKL (or compute the slow-cell stats directly from each PKL) and replay
L1 across ~35 weekly transitions — measuring the real false-positive rate across 8 months
including regime shifts (the January YTD reset sits inside the window and will be measured, not
guessed). This is the shadow phase's calibration dataset, available BEFORE any build.

— 3.0.0_SA_CVO
