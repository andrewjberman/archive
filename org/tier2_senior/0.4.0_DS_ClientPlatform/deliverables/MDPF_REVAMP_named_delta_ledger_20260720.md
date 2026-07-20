# MDPF_REVAMP -- NAMED-DELTA LEDGER (the never-widen evidence)

**Author:** 0.4.0_DS_ClientPlatform | **Date:** 2026-07-20 | **Gate:** 1.0.0_SA_CTO
**Basis:** Andrew D1 ruling (via CTO 20260720T220141Z) = **SERVE REAL/COMPLETE DATA**. The revamp
CORRECTS the 3 legacy served artifacts to the real monolith data; each correction is an EXPECTED,
NAMED delta recorded here. This ledger is the never-widen streak evidence: at cutover the value-parity
streak = shape-clean (done, 3/3 TO-3) + ONLY these named deltas + no unexplained delta, N=3 same-cycle,
then Andrew+CTO co-sign the SPECIFIC corrected numbers. Everything NOT listed here must still tie.

All magnitudes grounded live 2026-07-20 (opal-data-assets silver + served opal-data-portal-v2).

---

## D-1 -- 49F model_aua HISTORY: real measured vs interpolated backfill
- **Field:** `aggregate_aua_timeseries` 49F (+global) `model_aua[]` + `by_model.*.model_value[]`.
- **Corrected source:** `fact_model_aum_daily.closing_equity` by `day` (latest partition day-col, F1).
- **Legacy served:** the interpolated/rederived backfill (meta.basis_provenance: schwab_canonical_rederived,
  interpolated_1c, .031 2024depth).
- **Delta (measured 5-core vs served, sampled):** 2024-11-01 +$83.0M/+23.5% . 2025-01-16 +$178.8M/+39.3% .
  2025-07-01 +$83.5M/+11.3% . 2026-01-15 +$2.4M/+0.2% . 2026-07-17 -$1.3M/-0.1%. Mean gap over 408
  overlap days +$65.7M. **Shape: CONVERGES to a tie by 2026** (the measured series is correct; the
  legacy backfill understated 2024-25). **Reason:** real-vs-interpolated.
- **UST later-start:** measured UST starts 2025-01-16; zero-pad 2024-11-01..2025-01-15 (D4, shape parity).

## D-2 -- 49F CUSTODY: full-envelope vs partial-cash
- **Field:** `aggregate_aua_timeseries` 49F `partner_custody_total[]` (+ the non_model residual off it).
- **Corrected source:** `fact_rps_s2.net_mv_plus_cash` (the full account custody envelope).
- **Corrected latest:** **$1,665,338,126.76**. **Legacy served:** $1,644,993,954.34 (coverage=incomplete,
  ~40% of the $33.76M cash leg). **Delta: +$20,344,172.42 / +1.24%.** **Reason:** full-vs-partial-cash
  (the revamp includes the full cash leg). Positions-only cross-check: fact_rps assets-only $1,631.66M /
  fact_rps_s2 net_mv_positions $1,631.58M (the legacy sits between positions-only and full-envelope).
- **Custody HISTORY:** rps/rps_s2 snapshots where they exist (real back-depth TBD -- enumerating) +
  NAME any pre-coverage gap; NO interpolation (D1).

## D-3 -- 49F model-AUA LATEST: RESOLVED = NOT A REAL DELTA (monolith ties served, +$0)
- **GROUNDED 2026-07-20 (FLAG-1, CTO priority):** roster `Sigma value` (open) and aum_daily
  `closing_equity` are the SAME measure -- per-model EXACT tie for 4/5 core (INT/LTA/UST exact,
  ST -0.011M); ONLY LTC differs -1.866M = pure date-drift (aum_daily last day 07-17 vs roster 07-20).
  Both TIE the served $1,397.3M. Recently-opened-after-07-17 core = only $1.35M.
- **Conclusion:** there is NO $4.1M systematic under-enumeration. The spec's "roster 07-18 $1,401.3M vs
  DDB $1,397.2M" was the roster's DAY-TO-DAY VOLATILITY (my 07-20 roster = $1,395.4M, LOWER than the DDB),
  NOT an enumeration gap. The served 5-core is FULLY enumerated in BOTH roster and aum_daily.
- **=> NO D-3 delta.** The monolith model-AUA latest ties served (+$0, modulo daily drift). Andrew's D-3
  "legacy 11-of->=14 enumeration gap" framing does NOT apply to the served 5-core (any un-enumerated
  models are OUTSIDE the served 7, not on the page). CTO to correct Andrew's D-3. The D-1 history + D-2
  custody deltas STAND.

## TIES (NOT deltas -- must remain exact/named-drift-only)
- **Inflection model_aua** = eclipse `fact_portfolios_full.totalValue` (Opal-filtered) = **$137,170,028.82
  = served EXACT** (7/7 by_model to the cent). No delta.
- **Inflection custody** = orion `fact_assets.currentValue` = **$201,648,128.16 = served EXACT ($0.00)**.
  No delta. (Confirms the custody question is 49F-specific.)
- **Inflection non_model** = custody - model = **$64,478,099.34 = served EXACT.**
- **TO-3 distribution (all 3 firms):** shape-clean end-to-end; inflection EXACT (534=534), 49F+global
  F2 date-drift only. (First decision-independent green, published live, DT-parity-confirmed.)

## FRONTIER / STRUCTURAL (named, not value deltas)
- **Date axis:** measured 427 trading days (2024-11-01..2026-07-17) vs served 429 (..07-18) -- T-1 frontier
  alignment; align at authoring.
- **Cohort depths (as-is, do NOT extend):** core 429; SMA + blend + inflection 38-day depth (Andrew:
  do not extend the shallow cohorts). Serve real VALUES within each existing depth.
- **eclipse_id 30** ("90/10 Opal LT/UST" blend): excluded for parity (served omits it); post-swap co-sign
  candidate (KNOWN_EXCLUDED_ECLIPSE_IDS).
- **account_count[] history:** monolith has no daily count source -- disposition pending CTO (reconstruct
  from roster opened_ts, basis-named / vs serve-latest+name-gap). [sub-question surfaced 220311Z]

---
**STATUS:** shape-parity done (3/3 TO-3). Value-parity streak pending the history builds (this ledger's
D-1..D-3 are the whitelist) -> DT harness widens to history arrays -> N=3 same-cycle -> co-sign. Updated
as each corrected number lands with its measured magnitude.
