# ADVI_ANONYM.016 — AE: Migrate API GW + CloudFront /api/shared/ to /api/scoped/

<task_order>
  <issuer>1.0.0_SA_CTO</issuer>
  <issued>2026-04-06</issued>
  <agent>0.7.0_AE_CloudOps</agent>
  <status>complete</status>
  <priority>low</priority>
  <project>ADVI_ANONYM</project>
  <depends_on>none (hotfix in place, no urgency)</depends_on>
</task_order>

## Context

The `/api/shared/` path prefix is an orphaned convention. All auth-gated endpoints
should use `/api/scoped/`. You added a hotfix CloudFront behavior for `/api/shared/*`
on 04-06 — this TO replaces that hotfix with the correct convention.

## Deliverables

### Phase 1: Add /api/scoped/ routes (non-breaking)

1. **Add duplicate API GW routes** at `/api/scoped/advisor-intelligence/*` for all
   14 existing `/api/shared/advisor-intelligence/*` routes. Same integrations,
   same authorizer, same methods. This makes both paths work simultaneously.

2. **Verify** all 14 new routes respond correctly.

3. **Notify DT** (0.4.0_DT) that `/api/scoped/` routes are live — DT can now
   rename portal URLs (ADVI_ANONYM.015).

### Phase 2: Remove /api/shared/ (after DT deploys .015 to PROD)

4. **Remove all 14 `/api/shared/advisor-intelligence/*` API GW routes.**

5. **Remove the `/api/shared/*` CloudFront behavior** (the hotfix added 04-06).
   The existing `/api/scoped/*` behaviors already route to API GW.

6. **Terraform plan + apply** — should show only removals. Verify 0-drift.

7. **Tag** the portal-auth pipeline after 0-drift.

## Routes to migrate (14 total)

Pre-existing (9):
- timeseries, snapshots, filters, summary, growth, tax endpoints
  (exact paths in API GW console under `/api/shared/advisor-intelligence/`)

ANONYM.014 additions (5):
- clients-tab, client-detail, advisor-book, client-detail-books, advisor-mix-views

## Coordination

- Phase 1 is independent — can start immediately on GO
- Phase 2 MUST wait until DT confirms .015 is on portal PROD
- Sequence: AE Phase 1 -> DT .015 -> AE Phase 2

## Acceptance

- Zero `/api/shared/` routes in API GW
- Zero `/api/shared/*` CloudFront behaviors
- All advisor-intelligence endpoints functional via `/api/scoped/`
- 0-drift Terraform plan
