# MDPF_REVAMP -- A4 `non_model_assets` deliverable + named-delta ledger (TO-4)

**Author:** 0.4.0_DS_ClientPlatform~A · **Date:** 2026-07-21 · **Gate:** 1.0.0_SA_CTO
**Artifact:** `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py` (commits `80d30852c` + `f8667aab1`)
**Staging key (build-alongside, pure add):** `gold/mdpf_revamp/portfolios/global/non_model_assets.json`

Companion to the base named-delta ledger (`MDPF_REVAMP_named_delta_ledger_20260720.md`); the A4 section.

---

## 1. What A4 is (source-confirmed, Rule 22)

A4 `non_model_assets` (the `/model-portfolios` "Non-Model" bar) is a **THIN DERIVATION off the serve-real
aggregate spine**, NOT an independent enterprise producer. Grounded 2026-07-21 against the served producer
`data/mdpf/scripts/backfill/build_legacy_compat_emit.py:615-653` (the sole SoT for the served
`non_model_assets.json`), the served artifact, and the base aggregate `dim_mdpf_aggregate_aua_timeseries.py`:

- **`build_legacy_compat_emit` derives every post-cutover A4 row FROM the platinum aggregate** -- so the
  revamp equivalent reads the **base global aggregate**. A4 consumes the aggregate; it does not re-source
  enterprise from the monolith (that would duplicate the base's custody-envelope / inflection-onset /
  holiday logic and risk divergence). CTO + base confirmed this direction (144157Z / 144428Z).

## 2. Methodology (v0_9 = schwab_confirmed_only_plus_inflection_from_first_appearance)

```
enterprise_total[i] = base GLOBAL opal_aggregate_aua[i]     # = 49F custody(model+non_model) + inflection model
model_aum[i]        = base GLOBAL model_aua[i]              # = 49F 5-core + inflection all-7
non_model_aum[i]    = enterprise_total[i] - model_aum[i]    # 2-TERM
non_model_pct[i]    = 100 * non_model_aum / enterprise_total
etf_public_residual[i], inflection_non_model_aua[i]        # AUDIT-ONLY, out of the headline math
```

**2-term is Andrew-direct (verbatim, to DS~A, 2026-07-21):** *"let's not deal with the SMAs at this point
for this. just say non_model is enterprise_total - model."* SMAs fold INTO the residual (drops the v0_9
feeder's 3-term custody-model-sma form). **A4-SCOPED** -- the A5 spine is untouched (A5 already folds SMAs
into its residual; no SMA term to drop; CTO F3-close). The 2-term reproduces the served A4 to the dollar.

**Pre-cutover (< 2025-12-23):** verbatim passthrough from the served legacy `non_model_assets.json` (frozen
49F-CSV history; NOT monolith-derivable -- parity REQUIRES the frozen values, per the served
`meta.pre_cutover = verbatim_passthrough_from_legacy`). Do NOT recompute pre-cutover from the aggregate.

## 3. The trap A4 does NOT step in (baseline #2 / CVO F3)

A4 non_model (**$247,692,229.36**, enterprise-basis) is a DIFFERENT quantity from the base GLOBAL
`non_model_aua[]` (**$312,170,328.70**, firm-summed custody-basis). A4 computes `opal_aggregate_aua - model_aua`
and **NEVER reads the base global `non_model_aua[]` field.** The ~$64.48M gap = inflection non_model
(custody-vs-enterprise basis), **NOT an error** -- same never-substitute discipline as 0824/0833. Enforced by
a `validate()` guard that fails the build if any row equals the $312.17M spine number.

## 4. A4 named deltas vs the served `non_model_assets` (all NAMED, none silent)

| # | Delta | Basis |
|---|---|---|
| A4-D1 | **AXIS.** A4 post-cutover emits on the base ONE canonical NYSE trading-day axis; the served carries weekend/holiday ffill rows (455 served vs ~N trading-day rows). | Serve-real omits fabricated fill rows; the portal FE rolls forward on render (`getNonModelAumForDate` lookback) -- no spike-to-zero. Same class as the base aggregate's 21 holiday-fills. |
| A4-D2 | **LATEST-DATE.** served latest = 2026-07-18 (Sat, an ffill row); A4 latest = the trading-day frontier (e.g. 07-17 Fri). | A weekend ffill is not a serve-real datapoint. |
| A4-D3 | **PRE/POST-CUTOVER BOUNDARY (2025-12-22/23).** pre = verbatim legacy passthrough (calendar-day rows); post = trading-day-axis derivation (mixed axis at the boundary). | Parity REQUIRES the frozen legacy pre-cutover verbatim (served meta). DT date-joins; the boundary is explained, not smoothed. |
| A4-D4 | **REAL-vs-REDERIVED.** A4 propagates the base aggregate's D-1 (real aum_daily) / D-2 (real fact_rps_s2) named deltas through `opal_aggregate_aua - model_aua`. | A4 adds no independent recompute; its enterprise-minus-model identity is exact. A4's parity IS the aggregate's parity + the exact identity. |

## 5. Test evidence (committed)

- **Derivation self-test** (`--self-test`): `1,782,163,983.16 - 1,534,471,753.80 = 247,692,229.36 / 13.898397%`
  -- ties the 2026-07-18 baseline (`docs/briefs/mdpf-preswap-baseline-20260720.md`) to the cent; asserts
  `!= $312.17M`, gap `== $64,478,099.34` (inflection non_model).
- **E2E dry-run** (synthetic global fixture + REAL served legacy): 297 legacy passthrough rows
  (2024-11-01..2025-12-22) + derived post-cutover; validation PASS (identity exact, residual sane, NO
  trap-#2 substitution -- it ignored a planted $312.17M in the fixture's `non_model_aua`). Post-cutover
  trading-day axis WARN fired correctly on the fixture's Saturday row.
- **commit-gate** clean (py_compile + AST + ruff py39).

## 6. Calendar tie-in (Andrew-direct 2026-07-21)

A4 imports the mdpf-local `_trading_day_calendar` per CTO ARCH-GATE (runtime-consistent with the gold runner
+ the base aggregate). DS converges that module to canonical-faithful (add 2027 + frontier fns) under a
DRIFT-GUARD (vs `lib/trading_calendar`); A4 transparently gets canonical post-convergence. The convergence is
HELD pending CTO's word (Andrew elevated the calendar to a UNIVERSAL initiative, PRD-seed `30bef2f85`). A4
also carries a `validate()` post-cutover axis check (`is_trading_day`) as an aggregate-axis-leak guard.

## 7. Build-order dependency + co-verify plan

- **DEP:** A4's full dry-run + verify is gated on the base staging the GLOBAL + INFLECTION serve-real HISTORY
  (still latest-only skeleton at authoring). Base pings at stage-time.
- **Two asks to base before it stages:** (1) ADD `etf_public_residual_total[]` to the global aggregate
  contract (single-source the audit field off the aggregate); (2) confirm the exact staged S3 URIs.
- **Co-verify (CTO 144157Z):** A4 verifies IMMEDIATELY after the base global-aggregate S3 re-verify (co-verify,
  not race). A4's N=3 = the aggregate global N=3 + the enterprise-minus-model derivation-identity check on the
  staged global. The headline ties BY CONSTRUCTION once the global aggregate is staged + verified.
