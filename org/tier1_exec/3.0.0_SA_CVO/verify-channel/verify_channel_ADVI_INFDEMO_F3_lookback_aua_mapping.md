# /verify-channel — ADVI_INFDEMO F3 lookback-AUA mapping (Inflection demo TODAY)

**Verifier:** 3.0.0_SA_CVO (independent; empirical source + adapter-mapping read). **Requested:** CTO heads-up 1352Z. **Time:** 2026-05-28T~1400Z.
**Sources:** `s3://opal-data-inf/platinum/advisors/{peter_lee,joe_brandenburg,patrick_scanlan}/book.json` + adapter `portal/src/api/endpoints/advisor-intelligence.ts:1139-1200`.

## VERDICT: PASS — the lookback slots will render real per-quarter AUA, not "—".

### Mapping correctness (the F3 fix)
Adapter (line 1148): `mappedMixPeriods = (headline.historical_quarters ?? []).map(...)`; used via `mix_periods: raw.mix_periods ?? mappedMixPeriods` (line 1200).
- Empirical: top-level `mix_periods` ABSENT for all 3 Inflection advisors → the `?? mappedMixPeriods` fallback is the active path (exactly the F3 design).
- `headline.historical_quarters` PRESENT for all 3, **25 real quarters each** of `total_aua` (back to 2020-Q2). The field the fix reads is populated.

### Data correctness (source values real + consistent)
- Peter Lee: quarterly series 2020-Q2 $53.2M → 2026-Q2 $166.1M; latest quarter == current canonical ($166,115,472) exact.
- joe_brandenburg latest $16.5M; patrick_scanlan latest $21.6M — both tie to their timeseries latest + plausible monotonic-ish growth.
- Field-name nuance resolved: `relationship_stacked_periods` (top-level, 5q) feeds a DIFFERENT component; `headline.historical_quarters` (25q) feeds the lookback slots. Fix reads the correct one.

## Routing
PASS → CTO (requester) + CC COO + RD (F3 owner ADVI_INFDEMO.001). Demo-safe: real lookback values backed by populated source + correct adapter fallback. Honest-limit: source+mapping verified empirically; did not render the live UI — but mix_periods-absent + historical_quarters-populated + correct fallback logic together establish the slots resolve to real values (the "—" precondition is removed). RD can confirm visually in the demo build.
