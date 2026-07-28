# Cottonwood pair identity-(i) tolerance recalibration — divergence record

**Date:** 2026-07-28 ~22:50Z · **Author:** 0.7.0_AE_CloudOps · **Ruling:** CTO 20260728T224741Z (option a)
**Under:** MDPF_RESET_DIRECTIVE_20260728T2220Z / Andrew ~2157Z "run it right now… maximally updated data for every single channel."

## What happened
Run `mdpf_daily_20260728_222927` — the first run after the Stage-6 IAM grant — got through
`:523` (`build_dim_model_portfolio` WROTE+VERIFIED the dim parquet; grant accepted end-to-end)
and failed at `:524` `build_cottonwood_mdpf_pair.assert_identities` identity (i) by ONE CENT:
`decomposed 126,377,399.73 != dim 126,377,399.72`. The gate was `abs(delta) > 0.01` on a sum of
TWO independently-rounded components (models + income residual); the float representation of the
one-cent delta (0.010000005…) exceeds the exact 0.01 literal.

## What changed (S3-STAGED COPY ONLY)
`s3://opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_pair.py` — one block
(see `tolerance.diff`): tolerance 0.01 → **0.02** (compounding bound of two rounded components;
house precedent mdpf AC7 $0.011), and the ACTUAL delta is now **logged on every run** — the log
line is what proves the tolerance is not hiding drift. The gate stays a gate: a real
decomposition defect is dollars, not cents.

## The recorded divergence
**The S3-staged copy now diverges from the repo copy
(`data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` class of tree — the held G7
976-line generation swap, coupled to DS's read-preference) by exactly this block.**
The repo script is deliberately NOT edited. Reconciled when G7 lands, toward whichever
generation wins, tolerance carried.

## Files
- `build_cottonwood_mdpf_pair.py.staged` — the 07-23 S3 copy as found (pre-patch)
- `build_cottonwood_mdpf_pair.py.patched` — as uploaded (byte-roundtrip verified,
  ETag e0ef77832f123e6aa71307cb3671873b, 24228B, LM 2026-07-28T22:50:07Z)
- `tolerance.diff` — the exact divergence
- Ledger: `org/critical_paths/.open_deploys/cot-pair-tolerance-recal.json`
