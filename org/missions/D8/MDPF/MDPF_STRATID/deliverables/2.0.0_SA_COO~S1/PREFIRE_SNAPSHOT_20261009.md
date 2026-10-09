# MDPF_STRATID R1 -- pre-fire snapshot for the ledger L4 read

Taken by `2.0.0_SA_COO~S1` 2026-10-09 ~03:4xZ, before the first scheduled `mdpf-gold-lambda` fire after D2
(`mdpf-scheduled-floor`, `cron(30 13 * * ? *)` UTC, 2026-10-09 13:30Z). Bucket `opal-data-assets` has versioning
Enabled, so each object below is recoverable by its version id. Run date 2026-10-07, written 2026-10-08 13:31:29-30Z by
the pre-D2 code (lambda last log event 13:31:29Z).

| key (`portal/gold/mdpf/<scope>/<view>/2026-10-07.json`) | VersionId | ETag |
|---|---|---|
| global/aggregate-aua-timeseries | `sTdxmYs3_xERKZ54i6bOMdV0HGrFlHOF` | `c73576e53655f4372d669feda1657cc2` |
| global/category-views | `Ef.VrDmPoP01rXKsVzq7L1jxpwmIgCcH` | `73d93c49eb941998b41de998c272d922` |
| global/aum-metrics | `_vO0SDIyJWvntRU6.R5KLWHHNQbj9V4I` | `f6a50278be01c39dbeacab55107e50a2` |
| 49financial/aggregate-aua-timeseries | `4.9IZdu8ccHIjB5iIA.WHALiKzj2Yiz_` | `9131e029157edbf4171567dc13bcdfc3` |
| 49financial/category-views | `mkNB2JXmUimILqgll1e0Ri9FpZ3tFQLv` | `3e24791bcfb259c0a0ad4d2b1be8ec10` |
| 49financial/aum-metrics | `7tDboC8Z8q1S2e2g2vcILJdz64I02x_G` | `6b5df9a64ee028855e96c4e964db3f26` |
| inflection/aggregate-aua-timeseries | `E_FbB00MXY0iqGJoirSqlsMzCjfxa4dy` | `9030d7544638b0e5912f20fb020e6103` |
| inflection/category-views | `3XZIGiTlzTwmCNUR4AUv1zYRVC2QogLE` | `49e7a92000ecaab635e2a994d63650e6` |
| inflection/aum-metrics | `NklaPdlaGYJeasRW7emsCM8kpchWCYez` | `a55e098a0e8d2c65ea38fd6e9dfd6a2d` |
| cottonwood/aggregate-aua-timeseries | `65dkDPX9cjPMhwo9EJ.8PJVxxEg4d3wL` | `b7f684647c07901d50d9da64ac2e1a6f` |
| cottonwood/category-views | `DFuAwUtya_X2aShycONduG.IXF.dbnGu` | `948d4a44a60830eac576c8c697243afd` |
| cottonwood/aum-metrics | `X21oFiai_KCRPLyjbdQxaltzutcvrwYK` | `02b2b0ed670117e93cfcf47deea949c2` |

## The read, and its control

`python l4_read.py <pre_dir> <post_dir>` (this folder). After the fire: download these 12 objects by version id into
`<pre_dir>`, and the fire's run-date objects into `<post_dir>`, both named `<scope>__<view>.json`.

Control, pre vs pre (2026-10-09 ~03:4xZ): A history 0 moved figures for 3 of 3 firms; B FAIL x3 (the admitted keys
are absent before the fold); C FAIL (no PFDE member under SMA > ETF Strategies; Cottonwood PFDE 412,892.63); D1 OK
(delta 0.00 with no fold: `opal_aggregate_aua = base_excluding_tax_aua + tax_additive_aua` on 483 of 483 dated
points); D2 OK; `L4-VERDICT FAIL`. So B and C discriminate the fold, and A, D1 and D2 pass on unchanged bytes.

D2 is a PROXY, labelled in the script's output: it shows the sleeve does not land under Client. A counterfactual
Client figure would need the pre-D2 pin run on the same inputs.
