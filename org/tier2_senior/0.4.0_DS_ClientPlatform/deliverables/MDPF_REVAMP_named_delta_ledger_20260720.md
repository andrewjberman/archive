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

## D-2 -- 49F CUSTODY: full-envelope real-daily vs rederived-estimate  [BUILT 2026-07-21 @6eb54c186]
- **Field:** `aggregate_aua_timeseries` 49F `partner_custody_total[]` + `non_model_aua[]` (the residual off it).
- **Corrected source:** `fact_rps_s2.net_mv_plus_cash` (the full account custody envelope), REAL daily snapshots.
- **Corrected latest:** **$1,665,338,126.76**. **Legacy served (07-17 common):** $1,644,993,954.34. **Delta
  +$20,344,172.42 / +1.24%** = full-vs-partial-cash at the live tail (legacy ~40% of the $33.76M cash leg).
  **[AMENDED 2026-07-23, C2 arc]** The "legacy ~40% of the cash leg" read above is **RETRACTED** — a
  date-axis artifact (07-17 envelope vs a 07-15-valued legacy number). Grounded: legacy = positions-only
  assets-ex-CASH (`build_mdpf_wse_49f_non_model_aua.py:564-597`), ZERO cash; the legacy silver rps stalled
  at date=20260715, so its "@07-17/07-18" labels roll the 07-15 valuation forward. Same-date tie to the cent
  on canonical `dim_position/date=2026-07-15`. C2 spec (Andrew-ruled, COO 151257Z: net_mv_plus_cash) is the
  recorded definition — see `MODELPORTFOLIOS_GLOBAL_VIEW_BASIS_DEFINITIONS_20260723.md` §49financial.
- **Custody HISTORY -- GROUNDED (Rule 22), NOT a flat +1.24%:** the legacy served custody[] is the v0.9
  schwab_canonical **REDERIVED estimate** (per the served meta.backfill_methods: `.031` 2024depth pre-2026-01-16
  + `.029` rps_calibrated 2026-01-16..05-17 + real daily-forward 2026-05-18+). So D-2 is the SAME FAMILY as D-1
  (real-vs-rederived): the per-date delta is **date-VARYING**. Date-joined per-quarter (partner_custody_total,
  obs range +/-0.4 buffer -> ledger.json `custody_history_windows`): 2024Q4 [+2.46,+6.67] . 2025Q1 [+2.25,+6.58] .
  2025Q2 [+2.27,+4.32] . 2025Q3 [+1.62,+2.79] . 2025Q4 [+1.85,+6.27] . 2026Q1 [-0.58,+1.64] . 2026Q2pre
  [-1.47,-0.37] . live2605 [-3.23,+2.03]. **Coverage: 427/427 axis dates have an rps_s2 partition, ZERO gaps,
  NO interpolation (D1).**
- **non_model_aua[]:** the derived residual (`non_model[i] = custody[i] - model_aua[i]`); windows are WIDE
  ([-38%,+21%]) BY CONSTRUCTION (carries both D-1 model + D-2 custody corrections). Rigor = the internal identity
  `non_model==custody-model` (0 mismatches, enforced in-build) + the tighter custody + model windows -- not the
  wide non_model band alone.

## D-2b -- AXIS CALENDAR: DATE-JOIN REQUIRED (harness finding 2026-07-21)  [STRUCTURAL, named]
- The **published axis = real aum_daily trading days (427)**; the **served axis = the rederived business-day
  calendar (429) that FILLS market holidays**. Symmetric diff: **21 served-only** (Thanksgiving/Christmas/MLK/
  Juneteenth/Good Friday/... + the 07-18 frontier) + **19 published-only** (real trading days the rederive
  omitted); **408 common**.
- **=> DT's parity harness MUST DATE-JOIN, not index-join.** Index-join compares MISMATCHED dates from i=19
  onward (pub 2024-11-29 vs serv 2024-11-28). All windows above are DATE-JOINED on the 408 common dates; the
  symmetric-diff dates are the named structural delta (real-trading-days vs rederived-filled-business-days).
  Flagged to DT + CTO; ledger.json carries `_meta.harness_requirement` + `._calendar_note`.

## D-2c -- account_count[] PRESERVE PLACEHOLDER (co-sign-gated, NAMED)  [CTO 131345Z + DT 132025Z]
- 49F/global `by_model.*.account_count[]` = None history + latest (placeholder) while served is 429/429
  populated. NAMED via ledger.json `account_count_placeholder` **null_ok=true** (DT's consumer now DETECTS the
  null mismatch @5b097cbf3 -> classified NAMED, not UNEXPLAINED/SHAPE_FAIL). Disposition: import served-real
  count arrays as historical seed + roster-daily forward; ties EXACTLY (imported==served) at CUTOVER, when the
  null_ok entry is REMOVED and the count held to an exact tie. Serve-real-CONSISTENT (real data the monolith
  didn't itself capture). SEAM-CONTINUITY check at wire-time (roster-daily vs legacy boundary). cohort_provenance[]
  = None (revamp uniformly real-measured; legacy 82-date estimate labels retired) -- co-sign item, not FE-consumed.

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
- **account_count[] history -- PRESERVE (co-sign note, CTO-approved 225137Z):** the served count[] is
  REAL daily-snapshots (all-integer, irregular day-over-day steps -- INT 269 distinct/311 changes, LTC
  388/391; NOT interpolated, unlike model_value[]). None would be a REGRESSION on a feature Andrew asked
  about (Count toggle). Disposition = import the served count arrays ONCE as the real historical backfill
  + roster-daily forward (distinct allocation_id per model per daily roster partition). Serve-real-CONSISTENT
  (real data the monolith didn't itself capture; NOT replicating an interpolated artifact). Imported==served
  => count arrays TIE exactly in parity (no gap). SEAM-CONTINUITY check at wire-time: verify roster-daily
  count method matches the legacy trend at the boundary (funded/unfunded, model-membership, allocation_id
  vs account_id) -- name any discontinuity, do NOT smooth. Wired at cutover on the co-sign; folded into the
  cutover co-sign package, not a separate Andrew interrupt.

---
**STATUS:** shape-parity done (3/3 TO-3). Value-parity streak pending the history builds (this ledger's
D-1..D-3 are the whitelist) -> DT harness widens to history arrays -> N=3 same-cycle -> co-sign. Updated
as each corrected number lands with its measured magnitude.
