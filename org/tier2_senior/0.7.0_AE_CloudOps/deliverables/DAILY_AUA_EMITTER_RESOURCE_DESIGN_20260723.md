# daily-aua emitter re-source -- integration design (four-channel, per the 1600Z contracts)
**Author:** 0.7.0_AE_CloudOps | 2026-07-23 ~16:10Z | Status: DESIGN-COMMITTED, implementation next
**Contracts:** 49F @DS 160023Z + item-9 @160312Z | INF/COT/GLOBAL @DS 160530Z | CTO gate mechanism @160240Z
**Picks pending (built as named constants, defaults = recommendations):** FRONTIER_SEMANTICS=T1_SETTLED |
GLOBAL_PARTIAL=LABELED_PARTIAL_IN_TABLE (CTO binds both at the deploy gate)

## Module layout (BUILD_MANIFEST discipline)
- `lambda_function.py` (existing, 1,262 lines): keeps orchestration, state machinery (_stamp_state /
  coverage / staleness), the ETF ownership limb (UNTOUCHED, contract boundary), write_rows, AC7 gate.
- NEW `channel_sources.py` (vendored beside, flat): the four contract derivations as pure functions,
  each returning {cohort_id: {value, as_of, provenance, labels...}} for a run_date:
  * `c2_custody(run_date)` -- fact_rps_s2 per-date, to_numeric coercion (LOAD-BEARING, object dtype),
    round(sum,2). Tag c2_net_mv_plus_cash.
  * `smartx_models(run_date)` -- LATEST fact_model_aum_daily partition, intra-day series (F1 law:
    never accumulate run_dates), F5 rmid bridge (VENDORED reference reader, not reimplemented),
    per-model closing_equity; 5-core aggregate = sum(CORE_MODEL_KEYS) (SMA-exclusive, unbridged
    8th rmid DROPS). Tag smartx_closing_equity / _5core + definition field. FRONTIER_SEMANTICS
    constant governs the emitted frontier day.
  * `inf_total(run_date)` -- orion fact_assets currentValue sum (spine _orion_custody_sum semantics);
    `inf_models(run_date)` -- eclipse fact_portfolios_full totalValue, Opal-scoped via eclipse_id
    crosswalk + KNOWN_EXCLUDED_ECLIPSE_IDS (vendored). Pre-2026-05-15 = STRUCTURAL ZERO with the
    launch-seam label (known-zero), NOT honest-absent; inside-range gap = honest-absent.
  * `cot_total(run_date)` / `cot_models(run_date)` -- depth DISCOVERED by listing at every call
    (NO literal, NO config floor -- any channel); holdings-domain total (HOLDINGS_COMPLETENESS_FLOOR
    governs valued dates; unpriced = honest-absent never $0); model = rebalancer assignments JOIN
    DataMining values on externalId==AccountID as STRING (z09-preserving, never int-coerced); basis
    label VERBATIM "bd-rebalancer-models + bd-datamining-values"; provenance channel
    measured|interpolated_estimate|absent per the CRO-signed schema.
  * `global_rows(channel_rows)` -- derived FROM THE TABLE ROWS just built (one derivation, no shadow
    silver read): total + model lines, legs_present + completeness labels load-bearing
    (sum-of-3 vs sum-of-2 readable without external context). GLOBAL_PARTIAL constant governs
    partial-date emission (table carries labeled partial; the SERVE keeps the spine's
    all-present-or-absent composition gate -- the split the estate already runs).
- Vendored reference readers (from the spine @9bd23d904 per BUILD_MANIFEST vendored_modules law):
  load_aum_daily + build_rmid_bridge + CORE_MODEL_KEYS; the eclipse crosswalk + exclusions;
  _orion_custody_sum. Vendor, don't reimplement -- the bridges/exclusions ARE the semantics.

## Cohort mapping (DS-confirmed 160312Z + expansion)
RE-SOURCE: 49f_schwab_custody (C2) | 7x partner_model_detail 49f_* | 49f_smartx_platform (5-core) |
inflection_models (eclipse contract -- the earlier stay-as-is is SUPERSEDED) | [NEW under expansion:
inf total + cot total/model + global rows per CTO's bound spec] | _total__partner_aua derived.
UNTOUCHED: 5x etf_fund + 12x etf_ownership rows (per-date etfs files, incl honest roll-forward).

## Shape laws folded in
Trading-day axis (no weekend fabrication / flat-carries -- the DDB's legacy weekend carries are NOT
reproduced); per-row provenance (source key + partition date + derivation tag); idempotent upsert
(PK run_date / SK cohort_id, proven); honest-absent never carried/interpolated (YANG_SITTW).

## Acceptance battery (committed with the change)
1. Per-channel tie controls to the cent: 49F 7-value table (2024-05-24=$637,049,561.72 ..
   07-22=$1,689,302,889.53); INF orion $202,258,677.80 @07-22 + eclipse $137,997,265.16 @07-22;
   COT vs blackdiamond as-far-as-reached. Full-span programmatic sweep primary, spot-grid excerpt.
2. LITERAL-GREP over the built artifact's BYTES (not repo): no series-start date literal any channel.
3. DISCOVERY MUTANT both directions: staged older BD partition in a test prefix (env-override for the
   mutant run only) -> series extends backward zero-change; removal -> floor returns to source min.
4. Import-health probe on the deployed function (the package's banked lesson).
5. 21-row supersession event in the walk ledger (per-row pinned delta; restoration @d15c83489).
6. Denominators per channel vs source depth at run time; honest-absent enumerated.

## Sequence
implement -> commit-gate -> artifact swap at CTO gate (picks bound there) -> walk per channel under
own ledger -> COO per-date byte-verify -> co-sign. Serve stays HELD for the full backfill (Andrew).
