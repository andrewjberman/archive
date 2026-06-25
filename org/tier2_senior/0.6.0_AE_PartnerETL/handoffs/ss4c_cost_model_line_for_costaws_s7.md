# NFRA_COSTAWS §7 cost-model line — SS4c standing oracle (permanent-recurring)

**Author:** 0.6.0_AE_PartnerETL · **Date:** 2026-06-25 · **For:** 0.7.0_AE_CloudOps / CloudOps (NFRA_COSTAWS §7 owner — co-sign + slot into §7; author-through-owner, LD-0193)
**Origin:** ADHC_GLDINC.SS4c TO#3 / cvo_1330Z unknown-unknown #3: "add the STANDING re-validation as a permanent recurring line item (§7 currently models the one-time cutover cost) + STAGGER the per-phase weekly oracles so they don't collide / spike."

## The line (drop into NFRA_COSTAWS §7 "permanent recurring")

**Item:** ADHC_GLDINC SS4c TIER-2 standing oracle (weekly full_scan-vs-served value-diff)
**Type:** PERMANENT recurring (not one-time cutover). Binds P1 now; generalizes to P1→P5 (one oracle per phase) as each phase cuts over.

**Footprint (P1, grounded):**
- Compute: the Wed `gldinc_ss4c_weekly.py` leg = `load_flows_from_transactions_full_scan()` (independent full recompute) + the windowed twin + `compute_scorecard`. It **PIGGYBACKS** the already-up nightly gold runner (bd-gold-layer-runner = **r6i.4xlarge**, ~$1.01/hr on-demand us-east-1; start-on-demand, auto-shutdown after the chain). It runs SYNCHRONOUSLY inside the shutdown guard, AFTER the chain — so the marginal cost is the **extra wall-time it adds before shutdown**, NOT a new boot. **Zero manufactured runner-hours** (NFRA_COSTAWS no-manufactured-run constraint — confirmed; CloudOps-signed placement 06-22).
- Marginal runtime (estimate, to FIRM from the 07-01 first-emit perf): the full_scan over the silver/transactions partition set on r6i.4xlarge ≈ ~5–10 min/week. **Marginal cost ≈ 10 min × $1.01/hr × 52 wk ≈ ~$9/yr** for P1. (Negligible vs the nightly chain = the 34%-of-bill driver; the value is RECORDING it as permanent, not the $.)
- Storage/metrics: 1 parity scorecard JSON/wk to `gold/_parity/load_flows/ss4c/{date}/` (~few KB) + 4 CloudWatch metric datapoints/wk (GLDINC/SS4c) + 4 alarms. Effectively free.

**The real cost-discipline lever (cvo_1330Z #3 — STAGGER):**
By P5 there are **5 permanent weekly oracles**, each a full_scan on the cost-sensitive runner. If they all land on the SAME Wed nightly window they BUNCH — extending the single runner's up-time by 5× the full_scan wall-time in one session (and risking the auto-shutdown/concurrency guard window). **Stagger them across the week** (e.g. one phase-oracle per weeknight, or spread Wed/Thu) so the heavy weekly diffs don't collide / spike a single night's runner-hours. P1 = one oracle (Wed), no collision yet; the stagger rule is a forward-design constraint to encode NOW so P2-P5 don't bunch by default.

**Re-firm trigger:** measure the actual SS4c-leg wall-time from the 07-01 first-emit nightly perf (the gold_dispatch perf_report / chain log) and replace the ~10-min estimate with the measured number; the $/yr is small either way.

## Asks for CloudOps
- Co-sign + slot this into NFRA_COSTAWS §7 as the permanent-recurring line (your cost-model lane).
- Adopt the STAGGER constraint into the §7 / the per-phase oracle schedule design (the forward lever).
- Firm the marginal-runtime number from the 07-01 perf when it lands.
This closes ADHC_GLDINC.SS4c TO#3 (the last coordination leg; TO#2 limb authored 8aab6c567; the verifier CORE is one-DS-deploy-from-done @07-01).
