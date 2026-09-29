# EQUALITY_MX-t-10 -- the ETF tool's figure against the served object, side by side

Measured 2026-09-29 by 0.9.0_WK_NFRA_MCPINDEX~15, worktree wk-mcpindex-r4-15 at a6c17f4bcf plus this cell's edits.
Graded live at MX-r-5's r5.J1; this is the pre-release read.

## The served object

- bucket `opal-data-portal-v2`, the key of the catalog row `etfs.01.positioning-data` (`platinum/etfs/positioning_data.json`)
- **VersionId `yBqGKuVXd0Fc3LLZDBV8ojJ_ONfgTbUY`**, LastModified 2026-09-28T13:01:32+00:00, ETag `19c502963991633b7b67b81b24088c82`, 146041 bytes
- read by `.tools/aws s3api get-object --version-id` (read-only); `head-object` before and after the tool call returned the same VersionId, so the tool read this version.

## The two sides

The headline figure: fund PFDE (Pathfinder Disciplined US Equity ETF), its AUM, holdings count and equity allocation.

| side | top-level as-of (`data_as_of`) | PFDE fund as-of | PFDE aum | PFDE num_holdings | PFDE equity allocation | funds |
|---|---|---|---|---|---|---|
| tool `etfs_get_positioning` (in-process, real S3 reader, Opal-internal principal, 1 GetObject) | 2026-09-25 | 2026-09-25 | 167895344.0 | 90 | 99.45 | DIVZ, IDVZ, PFDE, PFOE |
| served object by VersionId | 2026-09-25 | 2026-09-25 | 167895344.0 | 90 | 99.45 | DIVZ, IDVZ, PFDE, PFOE |

- The tool's whole `data` equals the served object's whole parsed JSON: `True`.
- The tool's `as_of_field` is `data_as_of`, from the catalog entry `portal_etfs_positioning` (`freshness_field: FIELD:data_as_of`), not the call time.
- The answer's `caveat` is the catalog row's own `serve_verdict_with_caveats`, read at call time: widened on Andrew's word (@dc75ddbe32), Opal-internal, never sum or blend funds, per-fund as-of, holdings_status is load-bearing, null is never zero.

## The call

`pi.answer("etfs_get_positioning", <recording s3_getter>, (catalog_gate.OPAL_INTERNAL, ""), loaded=<the real catalog>)`,
one recorded call: `('opal-data-portal-v2', 'platinum/etfs/positioning_data.json')`. No write. The script is in the
worker's scratch and is not committed.

## Routing (MX-d-5 AC2, for the issuer's grade)

`discover_probe.py first "ETF holdings and fund flows"` in this worktree: `catalogued=True first=platinum/etfs/positioning_data.json`
(before this row landed the same probe read `first=json/positioning/holdings_attribution_data.json`).
This worktree does not carry MX-d-5's weak-match rule; the ETF row's channel keywords are `ETF`, `ETF holdings`,
`ETF positioning`, the four tickers and other multi-word or upper-case forms, none a plain lower-case single word.
