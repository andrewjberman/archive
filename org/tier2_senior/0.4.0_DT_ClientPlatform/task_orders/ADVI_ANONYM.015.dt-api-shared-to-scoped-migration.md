# ADVI_ANONYM.015 — DT: Migrate Portal /api/shared/ Endpoints to /api/scoped/

<task_order>
  <issuer>1.0.0_SA_CTO</issuer>
  <issued>2026-04-06</issued>
  <agent>0.4.0_DT_ClientPlatform</agent>
  <status>complete</status>
  <priority>low</priority>
  <project>ADVI_ANONYM</project>
  <depends_on>none (hotfix in place, no urgency)</depends_on>
</task_order>

## Context

The `/api/shared/` path prefix is an orphaned convention from the original advisor
intelligence implementation. It predates the `api/general/` + `api/scoped/` taxonomy
established in the architecture decisions log. All auth-gated, firm-scoped endpoints
should use `/api/scoped/`. The `/api/shared/` prefix had no CloudFront behavior
until AE CloudOps added a hotfix (04-06) — these endpoints may never have worked
through CloudFront in production before that.

ANONYM.014 (d552234) expanded the problem by migrating 5 more endpoints to
`/api/shared/` instead of `/api/scoped/`.

## Deliverables

1. **Rename all portal endpoint URLs** from `/api/shared/` to `/api/scoped/` in:
   - `portal/src/api/endpoints/advisor-intelligence.ts`
   - Any other files that reference `/api/shared/` paths

2. **Verify no other frontend code references `/api/shared/`:**
   ```
   grep -r "api/shared" portal/src/
   ```
   All hits must be migrated or removed.

3. **Test locally** that all advisor-intelligence endpoints resolve correctly
   through the `/api/scoped/` path after the rename.

## Coordination

- **Must deploy WITH or AFTER** ADVI_ANONYM.016 (AE CloudOps API GW route rename).
  The API GW routes must exist at `/api/scoped/` before the portal calls them there.
- AE CloudOps will add the new `/api/scoped/` API GW routes first, then you rename
  the portal URLs, then AE removes the old `/api/shared/` routes + CF behavior.

## Files

Primary: `portal/src/api/endpoints/advisor-intelligence.ts`
Search: `grep -r "api/shared" portal/src/`

## Acceptance

- Zero references to `/api/shared/` in portal source
- All advisor-intelligence endpoints functional via `/api/scoped/` path
- Portal DEV commit pushed, PROD merge after AE confirms API GW routes live
