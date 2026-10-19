# MDPF_CANON round 11, CN-s-7 -- D4 verdict: D4-PASS (2.0.0_SA_COO~D1)

Graded 2026-10-19 16:0xZ by the issuer, on CloudOps's saved responses (outside the repo, client-scale): `C:/dev/_deploy_artifacts/canon_s7/d4_ref_response.json` (sha256 `cfbdd21d6f9e0b9fd76e7e21e649a1fb1b802186083c74635fe798ed929c3161`, taken BEFORE the deploy) and `d4_new_response.json` (sha256 `46dff5f11886e938e4cd786d8ee3cac2944f529571d37a26d3f30e39910db1fb`, taken after). Grader: `round11/checks/r11_cn_s_7_d4.py` (counts, paths and flags only), with `--stored` the four stored Global objects read from `s3://opal-data-assets/portal/gold/mdpf/global/`. Pair `round11/NEVER_WIDEN_PAIR_R11_CN_S_7.md` (sha256 `bb0120bb...c3af`) section 2 and addendum 1; CTO half @2fe324e11e.

| gate | reads | verdict |
|---|---|---|
| (i) / G1 | new: status green, `errors` [], `a4_objects_built` 16, 16 bodies (ref: also green, 16 bodies, Global at the 2026-10-15 key, as the pair expected) | PASS |
| (ii) / G2 | Global `as_of_last` 2026-10-16 = 49financial's = inflection's in the same response; 499 dates; Global aggregate key `2026-10-16.json` | PASS |
| (iii) / G3 | last-row `model_aua`, `opal_aggregate_aua`, `non_model_aua` present; `aum-metrics` `total.aum` present | PASS |
| (iv) / G4 | the five core models: 0 None `model_value` cells from 2026-07-21 to `as_of_last`, 5 of 5 keys present | PASS |
| (v) / G5 | 12 non-Global bodies compared, 0 differ from D4-ref (volatile paths removed) | PASS |
| (vi) | no gold object written during the dry runs: a listing of `portal/gold/mdpf/` for LastModified after 2026-10-19T13:35Z shows only the package zip (15:51:52Z, the D2 upload); CloudOps reports the served objects, stores and control key at the same VersionId and the emitter unchanged | PASS |

Live function after D2 (read by the issuer, 16:0xZ): `CodeSha256` `L4G9dhABUkZZ9+oZJf1mMdM1w4i2/NYSSNTc5ZFO1AM=`, `MDPF_GOLD_COMMIT` `3d3d5ed5b91069a68b77d2d26b1ca37ae6a8fd8a`, last modified 2026-10-19T15:58:14Z. Rollback target (unchanged, pair section 2): `whMJ8Ei9g0ZUDFEUxSaEQAViS0kokkxt9CS+vlD7SGI=` and `128fce3524`.

**LISTED, not graded (the CTO's request): the per-artifact Global business diffs of D4-new**
- `aggregate-aua-timeseries` (new key 2026-10-16): 68 diff paths against the reference's 2026-10-15 body (the added 2026-10-16 row in every array, `as_of_last`, `_provenance.data_as_of`) and 148 against the STORED 2026-10-15 object (those 68 plus the feeder catch-up's restated cells, `account_count_total[491..497]` among them).
- `aum-metrics` (2026-10-16): 65 diff paths against both; `category-views` (2026-10-16): 32 against the reference and 35 against the stored object (the stored one lacks the Custom member 12 `Opal Municipal Bonds` that CN-s-1 adds: members 13 -> 14); `account-distribution`: 0 paths against both.
- **Headline, MEASURED on the D4-new body against the stored 2026-10-15 aggregate:** `model_aua` and `opal_aggregate_aua` each differ on exactly 7 of 498 stored dates, 2026-10-07 .. 2026-10-15, and on 2026-10-15 by +63,473,980.96 (the Muni account's value, CN-s-1's V2 leaf X, exactly the V2 pair's priced headline); `non_model_aua` differs on 0 of 498. `aum-metrics` `total.aum` as of 2026-10-16: 2,223,898,160.84.

**What this does not show:** which branch the 2026-10-20 13:30Z fire takes (pair section 1: Branch A writes NEW write-once Global 2026-10-16 keys; Branch B, a leg losing the date, is refused by gate (v)). The fire read is the acceptance; no ad-hoc run is read as evidence (C-3). The new Global 2026-10-16 keys are permanent once written, which is why D4 was the whole gate.
