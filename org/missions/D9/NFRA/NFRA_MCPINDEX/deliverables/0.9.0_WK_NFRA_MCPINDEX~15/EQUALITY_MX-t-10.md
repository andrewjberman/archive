# EQUALITY_MX-t-10 -- the ETF tool's figure against the served object, side by side

Re-measured live 2026-09-30 (~21:0xZ) by 0.9.0_WK_NFRA_MCPINDEX~15 in worktree wk-mcpindex-r5-15 (branch wk-nfra_mcpindex-5-15, cut from CLOUD @7aba7bcc4d) with the frozen candidate applied on top.
The 2026-09-29 read (VersionId `yBqGKuVXd0Fc3LLZDBV8ojJ_ONfgTbUY`, PFDE aum 167895344.0, as-of 2026-09-25) is superseded: the producer refreshed the object on 2026-09-30 13:01Z, so this record is the new version. Graded live at MX-r-5's r5.J1; this is the pre-release read.

## The served object

- bucket `opal-data-portal-v2`, the key of the catalog row `etfs.01.positioning-data` (`platinum/etfs/positioning_data.json`)
- **VersionId `YAsEJRNn8j_3Mu.nmkr_hwALppMRQFCB`**, LastModified 2026-09-30T13:01:30+00:00, ETag `14cbf50267380b9924ab1df591f0f2c2`, 147553 bytes
- read by `.tools/aws s3api get-object --version-id` (read-only); `head-object` before and after the tool call returned the same VersionId, so the tool read this version.

## The two sides

The headline figure: fund PFDE (Pathfinder Disciplined US Equity ETF), its AUM, holdings count and equity allocation.

| side | top-level as-of (`data_as_of`) | PFDE fund as-of | PFDE aum | PFDE num_holdings | PFDE equity allocation | funds |
|---|---|---|---|---|---|---|
| tool `etfs_get_positioning` (in-process, real S3 reader via boto3, Opal-internal principal, 1 GetObject) | 2026-09-29 | 2026-09-29 | 167398064.0 | 90 | 99.66 | DIVZ, IDVZ, PFDE, PFOE |
| served object by VersionId | 2026-09-29 | 2026-09-29 | 167398064.0 | 90 | 99.66 | DIVZ, IDVZ, PFDE, PFOE |

- The tool's whole `data` equals the served object's whole parsed JSON: `True`. `data_as_of_spread` on the object: `['2026-09-29']`.
- The tool's `as_of_field` is `data_as_of`, from the catalog entry `portal_etfs_positioning` (`freshness_field: FIELD:data_as_of`), not the call time.
- The answer's `caveat` is the catalog row's own `serve_verdict_with_caveats`, read at call time: widened on Andrew's word (@dc75ddbe32), Opal-internal, never sum or blend funds, per-fund as-of, holdings_status is load-bearing, null is never zero.

## The call

`pi.answer("etfs_get_positioning", <recording boto3 getter>, (catalog_gate.OPAL_INTERNAL, ""), loaded=pi.runtime_catalog())`,
one recorded call: `('opal-data-portal-v2', 'platinum/etfs/positioning_data.json')`. No write. The script is in the
worker's scratch and is not committed.
