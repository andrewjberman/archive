# MDPF_VARFLAG — Final Guard Shape, Scoped Per Andrew Ruling (Model Portfolios Page Only)

**Author:** 3.0.0_SA_CVO · 2026-07-17 ~15:3xZ
**Scope ruling (Andrew-direct ~15:30Z, verbatim on record):** *"This should not be per security,
it should only be on items in the Model Portfolios Page. that means benchmark returns and peer
returns tabs specifically"* — supersedes the backtest report's per-security G2 layer for this guard.

## Scope

The guard operates on the SERVED cells of exactly two artifacts (the two tabs):

| Tab | Served artifact | cells (censused live 07-17) |
|---|---|---|
| Benchmark returns | `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json` | 385 |
| Peer returns | `s3://opal-data-portal-v2/json/peers/peer_performance.json` | 210 |

(`model_portfolio_timeseries.json` feeds the same page; CTO to confirm whether its terminal-window
stats render on either tab — if yes it joins the config, if no it stays out. Page-scope is the
test, per the ruling.)

**RESOLVED (CTO 163001Z):** (1) the peers served JSON's 07-01 generation is EXPECTED — the
generator is monthly, gated on a peer Excel in the upload manifest; next regeneration ~07-31; the
guard baselines on accepted-upload events, cadence explicit per artifact. (2) timeseries JSON is
PAGE-in (`ReturnVolatilityScatter` in `ModelPortfolios.tsx`); WHICH TAB pends a DE render check —
**held OUT of the guard config until that lands** (in only if it renders on the Benchmark or Peers
tab, per the verbatim tab-scope).

**RESOLVED (DE 164356Z — render-verified, exercised-grade):** `ReturnVolatilityScatter` renders on
the **BENCHMARK tab only** (`ModelPortfolios.tsx:1902-1906`, `:1416` @ portal DEV `064658cd2`;
per-tab screenshots + DOM probes; peers tab absent) → **`model_portfolio_timeseries.json` is IN
scope.** **GRAIN RULE (CVO, binding for the config):** censused live 07-17, the artifact carries
**14,450 numeric leaves — full daily series arrays, not summary cells.** Per-cell V1 at that grain
is the wrong instrument (weekly restatements touch every array; 14k comparisons = pure noise).
The guard checks **derived terminal stats per series** (terminal cumulative return + realized vol
over the standard windows — tens of cells, computed at the gate), plus structural checks (series
count, length-monotonic-append, last-point date == data_as_of). The 25% V1 rule applies to those
derived cells exactly as to the other benchmarks-tab cells.

## The guard — three checks, all on served cells, all vs the LAST ACCEPTED upload

**V1 — 25% proportional on comparable cells (the acknowledge-screen driver).**
`|new − prior| / max(|prior|, 1pp) > 25%` on the slow cells: YTD / 1Y / 3Y / 5Y / Since-Inception
returns AND volatilities, both tabs. Spreads (model−benchmark differences) annotate their parent
flags rather than flagging independently. Peer ranked/percentile cells: level-domain validity
(percentile ∈ [0,100], rank ∈ [1,N]) + the same 25% rule on underlying return levels where served.
- Evidence: 0 flags on the healthy weekly served transition; 13/13 on the corrupt 07-16 vintage
  (551–1151%). **The vol discriminator survives page-scoping** — model-level volatility cells are
  ON the benchmarks tab and carried the loudest corrupt signature (YTD vol 3.32→25.90 = 680%).
- Year-boundary: YTD comparisons suppressed/re-baselined on the first accepted upload of a year
  (Jan boundary measured at 136 YTD false flags without it).

**V2 — static sanity bounds on the fast cells** (1D/WTD/MTD/QTD/1M/TTW, both tabs): fixed
per-class ranges (e.g. |1D| ≤ 5pp, |WTD| ≤ 8pp, vol ∈ (0, 60]). Week-over-week comparison is
meaningless there (new measurement each week — 46.6 flags/week measured under a proportional
rule); bounds catch wholesale garbage without ever firing on routine moves.

**V3 — structural sentinel:** cell appears/vanishes vs prior accepted vintage → flag, EXCEPT the
conditional-cells allowlist (the 15 WTD-volatility cells that legitimately come and go by
day-of-week — measured). Peer-universe membership change → ONE structural flag, not N rank flags.

## Definitions that bind

- **"Prior figure" = the last ACCEPTED upload's served value** (execution metadata), never the raw
  previous S3 version (same-day re-promotes and rollback restores would corrupt the comparison —
  both observed live in the version stack on 07-17).
- **Rollback executions bypass the gate** and are excluded as baselines (they re-publish an old
  vintage; the corrupt→rollback transition itself read 13 flags — symmetric with the corruption).
- **Peers tab bootstrap:** one served vintage exists as of today; V1 arms there as history accrues
  (V2/V3 active from day one — they need no history).

## Where it sits (unchanged from CTO's proposal)

Generators → staging → varflag-check (V1+V2+V3) → 0 flags = auto-promote / ≥1 flag = SFN pause +
acknowledge-or-cancel UX on the Data Refresh page → promote + CF invalidate. Fail-closed 24h
auto-cancel. Shadow-first phasing; shadow exit criterion (evidence-backed): ≤2 false flags per
upload sustained across 3 consecutive clean uploads.

**Config registration invariant (fails-open guard, unchanged from my review):** every configured
pattern must match ≥1 staged key AND every staged key under the two tabs' prefixes must match ≥1
pattern — either miss is a loud structural flag.

— 3.0.0_SA_CVO
