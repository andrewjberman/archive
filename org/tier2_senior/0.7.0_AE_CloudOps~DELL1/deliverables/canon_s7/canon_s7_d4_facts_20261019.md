# CN-s-7 D4 facts (0.7.0_AE_CloudOps~DELL1, 2026-10-19 16:0xZ) -- measured, ungraded; the grade is 2.0.0_SA_COO~D1's

Responses (outside the repo): D4-ref `C:/dev/_deploy_artifacts/canon_s7/d4_ref_response.json` 2,035,501 B sha256
`cfbdd21d6f9e0b9fd76e7e21e649a1fb1b802186083c74635fe798ed929c3161`; D4-new `.../d4_new_response.json` 2,037,198 B sha256
`46dff5f11886e938e4cd786d8ee3cac2944f529571d37a26d3f30e39910db1fb`. Both: StatusCode 200, no FunctionError, status green,
errors [], a4_objects_built 16, 16 bodies. Function under test: CodeSha256 `L4G9dhABUkZZ9+oZJf1mMdM1w4i2/NYSSNTc5ZFO1AM=`,
MDPF_GOLD_COMMIT `3d3d5ed5b91069a68b77d2d26b1ca37ae6a8fd8a`.

Pair section 2 gate inputs (values only):
- (i) D4-new status green, errors [], a4_objects_built 16.
- (ii) as_of_last D4-new: 49financial 2026-10-16, inflection 2026-10-16, cottonwood 2026-10-16, global 2026-10-16; Global 499 dates
  (2024-11-01 .. 2026-10-16). D4-ref Global as_of_last was 2026-10-15.
- (iii) Global last row: model_aua 1893063702.96, opal_aggregate_aua 2223898160.84, non_model_aua 301950138.87; aum-metrics
  total.aum 2223898160.84. (Row 2026-10-15: model_aua 1895313666.28, opal_aggregate_aua 2237501378.84, non_model_aua 312923402.67.)
- (iv) None model_value counts, Global by_model, 2026-07-21 .. 2026-10-16 (63 dates): opal_div_sma 0, opal_growth_sma 0,
  opal_intermediate 0, opal_long_term_aggressive 0, opal_long_term_conservative 0, opal_short_term 0, opal_ultra_short_term 0;
  divz 60, other_models 12, pfde 33, tax 50. Which five are "core" is the issuer's list.
- (v) bodies D4-ref vs D4-new after stripping the pair's volatile paths: the 12 non-Global bodies EQUAL; Global account-distribution
  (key 2026-10-19) EQUAL; Global aggregate-aua-timeseries, aum-metrics and category-views are REF-ONLY at key 2026-10-15 and
  NEW-ONLY at key 2026-10-16 (a new dated key each). Differing paths across the 13 common bodies: `_provenance.process_time` 13,
  `_provenance.source_vintage_age_hours` 3, `generated_at` 4, `last_updated` 3, `meta.generated_at` 2 (canon_s7_d4_pathdiff_20261019.txt).
- (vi) After print 16:01:48Z vs D4-ref after print: 16 served objects, 517 staged keys, 4 tax stores, control key: all unchanged
  (version + etag + sha256); emitter `GLQf6kv4...` and schedule input equal; workbook listing 35 -> 36 bronze and silver (the dry run's
  own inert pair). Versus the pre-D4-ref print: also unchanged.
