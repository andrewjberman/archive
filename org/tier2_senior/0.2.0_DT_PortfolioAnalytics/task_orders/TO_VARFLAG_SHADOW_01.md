# TO_VARFLAG_SHADOW_01 — MDPF_VARFLAG P1 SHADOW: the variance gate in log-only mode

**Project:** MDPF_VARFLAG  **Issuer:** 1.0.0_SA_CTO  **Assignee:** 0.2.0_DT_PortfolioAnalytics
**Status:** complete — reconciled 2026-08-04 (status line never flipped at close; work shipped 2026-07-17). Evidence: shadow built+deployed+exercised yang-pipeline-v1.5.0 @ba33c44e63 (6/6 corrupt separation, 0/600 healthy, 1.85 FP/upload vs budget 2), deploy ledger CLOSED @dd301a232e, post-close v1.5.1 baseline-horizon hardening ledger CLOSED @6cd5ddaae8, session log @bc7f9484d0.  **Issued:** 2026-07-17T17:0xZ  **Priority:** P1 — behind nothing (your P0 + BE01 are closed); parallel to your tax-pt2 tasking at your judgment.

## Authority chain

Andrew ratified the guard statistic stack ~16:55Z via CVO relay ("Use your recs for all and relay to
CTO", record @f5cee1a8a): V1/V2/V3 benchmarks + P1/P2/P3 peers + derived-stats grain for timeseries.
Architecture per `docs/architecture/MDPF_VARFLAG_PROPOSAL.md` (@6b86d2712, §2 staging+gate, §5 phasing).
CVO's evidence stack governs the parameters: review @4ade1cc08 · served scan @849552a5b · 8-month
backtest @67649304e · scope re-cut @6d4bc46a9 · peers backtest @df7e3cb98 · resolutions @b3c5088d6 ·
grain rule @4970f8a1d. Do not re-derive constants CVO measured — cite them.

## Scope (SHADOW ONLY — this TO blocks nothing, publishes nothing new)

Build `varflag-check` running post-generation in the Yang pipeline, computing + LOGGING flags on every
upload for the three in-scope artifacts (`model_portfolio_benchmarks.json`, `peer_performance.json`,
`model_portfolio_timeseries.json` via derived stats). NO staging re-route, NO waitForTaskToken pause,
NO UI — publication proceeds exactly as today. Output: a per-execution flag report (S3 + log line),
accumulating the false-flag-rate evidence that gates P2.

## Binding requirements (the ratified P1s ride the shadow, not the gate)

1. **Vintage = accepted-upload EVENT from execution metadata** — never raw S3 versions (CVO finding 2:
   same-day re-promotes + rollback restores poison version-stack deltas). Rollback executions and
   acknowledged-bad vintages excluded by execution disposition; one config drives this and the future
   FM-5 gate bypass.
2. **FM-6 registration invariant from day one**: every configured pattern matches ≥1 artifact cell-set
   AND every gated-prefix artifact matches ≥1 pattern; either miss = a loud structural flag in the
   report. A config miss must never be silence.
3. **Year-boundary YTD suppression** built in (measured: 153 spurious flags at the January boundary
   without it).
4. **Statistic constants as ratified**: benchmarks slow-cells 25% w/ max(|prior|,1pp) denominator floor;
   vol cells carried (the substitution killer); peers 1Y/SI @ ~50% monthly-calibrated + percentile-
   envelope + domain/universe structural; timeseries derived terminal stats + structural
   (count/length-monotonic/last-point==data_as_of). WTD-vol conditional-cells allowlist per @67649304e.

## Acceptance (exercised, both directions)

- Replay: corrupt `data_20260716_v1.pkl` vintage ⇒ flags fire on ST YTD+vol (positive); healthy 07-12
  transition ⇒ clean (negative). Separate invocations, mirroring `validate_data_pkl` discipline.
- The 49-vintage archive replay as calibration evidence: combined false-flag rate ≤2/upload on the
  ratified stack (CVO measured this achievable — your build must reproduce it, not assume it).
- Deploy per Terraform law; source map; deploy-completion ledger. Shadow runs on ≥3 real uploads
  before any P2 (gate) proposal comes back to my gate.
- Closure to me + CVO (they verify the instrument) + COO (ledger).
