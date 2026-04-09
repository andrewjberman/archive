# ADVI_GLDRST.021 — DE: Migrate Portal Frontend Reads to New S3 Structured Paths

<task_order>
  <issuer>1.0.0_SA_CTO</issuer>
  <issued>2026-04-06</issued>
  <agent>0.4.0_DE_ClientPlatform</agent>
  <status>complete</status>
  <priority>high</priority>
  <project>ADVI_GLDRST</project>
  <depends_on>GLDRST.020 (DS writes new EC2 scripts that output to new paths)</depends_on>
</task_order>

## Context

The portal frontend still reads advisor-intelligence data from old flat S3 paths.
Until these reads are migrated, dual-write (old + new paths) cannot be dropped from
the gold scripts. Dual-write doubles S3 put volume and directly caused the publisher
Lambda 900s timeout.

GLDRST.003 (COMPLETE) migrated pre-computed quarterly views. This TO migrates
the remaining client detail, advisor book, and aggregate reads.

## Old Paths Still in Use (portal reads)

From `portal/src/api/endpoints/advisor-intelligence.ts`:
- `gold/client_timeseries/{id}_views.json`
- `gold/client_timeseries/{id}_composition.json`
- `gold/advisors/{id}/mix.json`
- `gold/timeseries_chart.json`
- `gold/clients_tab.json`
- `gold/header_metrics.json`
- `gold/filters.json`

CloudFront behaviors rewrite `/api/scoped/advisor-intelligence/*` to `/gold/*`
(old flat structure).

## New Structured Paths (target)

Defined in `data/black_diamond/scripts/gold/lib/s3_layout.py`:
- `gold/entities/clients/{id}/views.json`
- `gold/entities/clients/{id}/composition.json`
- `gold/entities/advisors/{id}/mix.json`
- `gold/artifacts/timeseries_chart.json`
- `gold/artifacts/clients_tab.json`
- `gold/artifacts/header_metrics.json`
- `gold/artifacts/filters.json`

## Deliverables

1. **Update all S3 read paths** in `advisor-intelligence.ts` to new structured paths.

2. **Update CloudFront origin path mappings** (shared-advisor-router) to route
   `/api/scoped/advisor-intelligence/*` to the new structured paths. Coordinate
   with AE CloudOps if CF behavior changes are needed.

3. **Grep for any other old-path references:**
   ```
   grep -r "gold/client_timeseries\|gold/advisors\|gold/timeseries_chart\|gold/clients_tab\|gold/header_metrics\|gold/filters" portal/src/
   ```

4. **Test locally** that all advisor-intelligence pages load correctly with new paths.

## Acceptance

- Zero references to old flat S3 paths in portal source
- All advisor-intelligence pages functional with new structured paths
- Portal DEV commit pushed, PROD merge after verification
- This unblocks GLDRST.010 (old key cleanup / dual-write removal)
