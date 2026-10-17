# MDPF_CANON round 11, CN-s-6 -- D4 verdict: D4-PASS (2.0.0_SA_COO~D1)

Graded 2026-10-17 15:5xZ by the issuer, on CloudOps's saved responses (outside the repo, client-scale): `C:/dev/_deploy_artifacts/canon_s6/d4_ref_response.json` (sha256 `37420c085551382d89ce6cf59438560080a5bb759f9787469febba2709059cb0`, taken BEFORE the deploy) and `d4_new_response.json` (sha256 `2b56d4b7e0215fa004f2e08c272ddddbd25f4e736dcca7d649b1ca44b51c247e`, taken after). Grader: `round11/checks/r11_cn_s_6_d4.py` (counts and flags only). Pair: `round11/NEVER_WIDEN_PAIR_R11_CN_S_6.md` @f39392914a, section 3; CTO conditions @78082bd6b6.

| gate | reads | verdict |
|---|---|---|
| (i) / G1 | new: status green, `errors` [], `a4_objects_built` 16, 16 bodies (ref: non-green, `errors` ['global'], 12 bodies, as the pair expected) | PASS |
| (ii) / G2 | Global `as_of_last` 2026-10-15 = 49financial's = inflection's in the same response; 498 dates, no 2026-10-16; Global aggregate key `2026-10-15.json` | PASS |
| (iii) / G3 | last-row `model_aua`, `opal_aggregate_aua`, `non_model_aua` present; `aum-metrics` `total.aum` present | PASS |
| (iv) / G4 | the five core models: 0 None `model_value` cells from 2026-07-21 to `as_of_last`, 5 of 5 keys present | PASS |
| (v) / G5 | 12 non-Global bodies compared, 0 differ from D4-ref (volatile paths removed) | PASS |
| (vi) | no gold object written between the deploy and the dry runs: a listing of `portal/gold/mdpf/` for LastModified after 13:35Z shows only the package zip (15:37:16Z, the D2 upload) and `cottonwood/account-units/2026-10-16.json` (13:40:48Z, before the deploy); CloudOps reports the 16 served, staged, control and store objects at the same VersionId | PASS |

Live function after D2 (read by the issuer, 15:5xZ): `CodeSha256` `whMJ8Ei9g0ZUDFEUxSaEQAViS0kokkxt9CS+vlD7SGI=`, `MDPF_GOLD_COMMIT` `128fce3524a820c3c912a5f1e28ab149a68c5024`, last modified 15:40:33Z. Rollback target (unchanged, pair section 3): `fAXZ4gdLPspZepxmR9J8l3BfJROkppYOyf3qC2dAd40=` and `d2f734fbac`.

**Informational (not a gate), MEASURED on the D4-new bodies against the 2026-10-17 fire-served Global objects (aggregate and aum-metrics, both dated 2026-10-15):** `model_aua` +63,473,980.96, `opal_aggregate_aua` +63,473,980.96, `non_model_aua` +0.00, `tax_additive_aua` and `sma_additive_aua` +0.00, and `aum-metrics` `total.aum` 2,237,501,378.84 (+63,473,980.96): the Muni account's value on 2026-10-15 (CN-s-1's V2 leaf X), exactly the V2 pair's priced headline. (The OFFLINE build's +34.21M `opal_aggregate_aua` was the missing overlay, as the pair said; the deployed function carries it.) This is what Global would serve if it writes a new key; it is not a claim about what the 10-18 fire writes.

**What this does not show:** which branch the 2026-10-18 13:30Z fire takes (pair section 2: Global writes a new key only if 49financial and inflection carry a date after 2026-10-15; otherwise the 10-15 key write is `conflict`, no error). The fire read is the acceptance; no ad-hoc run is read as evidence (C-3).
