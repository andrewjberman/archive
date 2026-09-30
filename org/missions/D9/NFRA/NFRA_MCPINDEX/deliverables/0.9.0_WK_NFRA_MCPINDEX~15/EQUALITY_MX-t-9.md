# EQUALITY_MX-t-9 -- the tool's figure against the served object, side by side

Measured 2026-09-29 by 0.9.0_WK_NFRA_MCPINDEX~15, worktree wk-mcpindex-r4-15 at 120ff9b27f plus this cell's edits.
Graded live at MX-r-5's r5.J1; this is the pre-release read.

## The served object

- bucket `opal-data-portal-v2`, key from catalog row `mp.05.model-portfolio-benchmarks` (`json/benchmarks/model_portfolio_benchmarks.json`)
- **VersionId `Pxy6ATX1Eah8up3d9.iauhexhaxPMkxX`**, LastModified 2026-09-26T11:06:31+00:00, ETag `8e60a85a46a693f0fe9edf659e0a40f4`, 19225 bytes
- read by `.tools/aws s3api get-object --version-id` (read-only); `head-object` before and after the tool call returned the same VersionId, so the tool read this version.

## The two sides

The headline figure: model UST (Ultra-Short Term), period "Since Inception", the model return and its two benchmark bases.

| side | as-of (`data_as_of`) | UST Since Inception model | index_benchmark | etf_benchmark |
|---|---|---|---|---|
| tool `mdpf_get_model_benchmarks` (in-process, real S3 reader, Opal-internal principal, 1 GetObject) | 2026-09-25 | 4.21 | 4.13 | 3.99 |
| served object by VersionId | 2026-09-25 | 4.21 | 4.13 | 3.99 |

- The tool's whole `data` equals the served object's whole parsed JSON: `True`.
- The tool's `as_of_field` is `data_as_of`, read from the catalog entry `portal_mdpf_model_benchmarks` (`freshness_field: FIELD:data_as_of`), not the call time.
- The answer carries `caveat`: "MODEL-DESIGN returns (Yang model-derived), never a client's realized return: quote them as the model's design performance only."
- The answer carries `benchmark_basis`: two bases (index_benchmark, etf_benchmark), and "a quoted figure must name which basis it used".

## The call

`pi.answer("mdpf_get_model_benchmarks", <recording s3_getter>, (catalog_gate.OPAL_INTERNAL, ""), loaded=<the real catalog>)`,
one recorded call: `('opal-data-portal-v2', 'json/benchmarks/model_portfolio_benchmarks.json')`. No write. The script is
in the worker's scratch and is not committed.
