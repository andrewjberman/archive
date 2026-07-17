# MDPF_VARFLAG — Peers Tab Backtest (10 monthly vintages) + History-Claim Correction

**Author:** 3.0.0_SA_CVO · 2026-07-17 ~16:2xZ
**Trigger:** Andrew-direct (~16:1xZ): peers data has been uploaded monthly for 6+ months — the
archived copies exist and we did not know the path.

## CORRECTION on the record

My earlier reports said the peers tab has "ONE served vintage ever / essentially no history."
**That was true of the SERVED JSON's S3 version stack and false of the estate.** The upload
archive lives at **`s3://opal-data-portal-v2/data-refresh/archive/exec-{id}/`** — one folder per
Data-Refresh execution, holding the original uploaded workbook. For peers: **15 archived
executions, 10 distinct monthly vintages, 2025-12 → 2026-06-30.** Andrew was right; the
prior claim measured the wrong layer. (The peers *served* JSON was still only generated once —
07-01 — which is its own small finding: monthly uploads have NOT been refreshing the served peers
artifact since 07-01; the 06-30 workbook upload is the last one reflected. CTO to confirm whether
that is expected or a stalled leg.)

## Backtest: V1 rule month-over-month across the 10 vintages

Parsed every `Peer Table` (2 model blocks × percentile-envelope rows × period columns; 252 cells,
336 from 2026-06-12). Rule: `|Δ| / max(|prior|, 1pp) > 25%` on Statistic cells, 9 transitions.

| period class | flag rate (cell-transitions) | verdict at MONTHLY cadence |
|---|---|---|
| YTD | **70/126 = 56%** | unusable — legit monthly moves off a small base routinely exceed 25% (worst: Mar→Apr Intermediate YTD −0.19 → 6.60 = 679%, a real rally; Dec→Jan = the year reset, as predicted) |
| 1 Year | 18/126 = 14% (~2/month) | marginal at 25%; usable at a monthly-calibrated threshold (~50%) |
| Since Inception | **7/126 = 6%** | usable near as-is |

**The finding that matters: the 25% threshold is cadence-relative.** It was calibrated on weekly
benchmark deltas; peers upload monthly, so healthy deltas are ~4× larger and YTD-off-a-small-base
is structurally proportional-hostile. Same rule, same page, different clock → different threshold.

Rank cells: max legitimate month-over-month rank move measured at **233 places** (peer universes
are hundreds of funds) — confirms ranks must NEVER be proportional-flagged; level-domain checks
only.

## Peers-specific guard (replaces the generic V1 there; V2/V3 unchanged)

- **P1 — proportional on the stable long windows only:** 1 Year + Since Inception Statistic cells,
  threshold calibrated to monthly cadence (50% opening bid; shadow refines). YTD Statistic cells:
  bounds-only (V2 class).
- **P2 — the percentile-envelope invariant (free, no history needed, peers-unique):** each block
  serves Percentile 5/25/50/75/95 rows plus the portfolio row. Two deterministic checks per
  upload: **(i) monotonicity** — the percentile rows must be ordered (P5 ≥ P25 ≥ P50 ≥ P75 ≥ P95
  for return cells); **(ii) envelope-scale** — the portfolio row must sit within a widened
  envelope (e.g. P5 + 2×(P5−P95) headroom). A wrong-series substitution (the .ST class) lands
  wildly outside the envelope of a real peer universe — this catches it with ZERO vintage history,
  which matters because peers history arrives monthly and slowly.
- **P3 — rank/percentile domain checks:** rank ∈ [1, N_universe], percentile ∈ [0,100],
  universe-size change = one structural flag.

## Where this leaves the whole guard

| surface | cadence | primary check | evidence |
|---|---|---|---|
| Benchmarks tab (385 cells) | weekly | V1 25% on slow cells incl model vols | 0 healthy / 13 corrupt (served); 8-month pkl backtest |
| Peers tab (210 cells) | monthly | P1 (1Y/SI @ ~50%) + P2 envelope + P3 domain | 10-vintage backtest: YTD 56% FP / SI 6% FP; envelope check history-free |

Both tabs: vs last ACCEPTED upload; V2 static bounds; V3 structural sentinel; year-boundary
pre-registration; config registration invariant. Architecture unchanged.

— 3.0.0_SA_CVO
