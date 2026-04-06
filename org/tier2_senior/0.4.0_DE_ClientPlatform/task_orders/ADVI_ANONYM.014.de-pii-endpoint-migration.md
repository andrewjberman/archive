# ADVI_ANONYM.014 — DE: Migrate PII Endpoints from S3-Direct to Lambda

<task_order>
  <issuer>2.0.0_SA_COO</issuer>
  <issued>2026-04-02</issued>
  <agent>0.4.0_DE_ClientPlatform</agent>
  <status>complete</status>
  <!-- COO 2026-04-06: DE re-executed with crossref validation. Portal DEV d552234. Awaiting DT push + PROD merge. -->
  <priority>high</priority>
  <project>ADVI_ANONYM</project>
</task_order>

## Context

The Advisor Intelligence frontend currently routes several PII-bearing data
fetches through the S3-direct path (shared-advisor-router), which serves raw
gold JSON with no pseudonymization. After .012 (DS adds Lambda handlers) and
.013 (DT fixes advisorId passthrough), the Lambda path will have full
pseudonymization coverage. This TO migrates the frontend to use it.

Additionally, the Books tab has an `isFirmAdmin` gate that blocks ALL data
fetching for partner users. This must be removed (while keeping the advisor
selector dropdown internal-only per Andrew's direction).

## Files

Primary: `portal/src/api/endpoints/advisor-intelligence.ts`
Secondary: `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`

## Deliverables

### 1. Migrate PII endpoint calls to Lambda path

In `advisor-intelligence.ts`, change these functions from S3-direct to Lambda:

| Function | Current Path (S3-direct) | New Path (Lambda) |
|---|---|---|
| `getClientsTab` | `/api/scoped/advisor-intelligence/clients_tab.json` | `/api/shared/advisor-intelligence/clients-tab?firmId={firmId}` |
| `getClientDetail` | `/api/scoped/advisor-intelligence/clients/{key}.json` | `/api/shared/advisor-intelligence/clients/{key}/detail?firmId={firmId}` |
| `getBooksClientDetail` | `/api/scoped/advisor-intelligence/clients/{key}.json` | Same as above |
| `getAdvisorBook` | `/api/scoped/advisor-intelligence/advisors/{id}/book.json` | `/api/shared/advisor-intelligence/advisors/{id}/book?firmId={firmId}` |
| `getBooksAdvisorComposition` | `/api/scoped/advisor-intelligence/advisors/{id}/composition.json` | `/api/scoped/partners/books/advisor/{id}/composition?firmId={firmId}` |

Each migrated function must:
- Accept `firmId` as a parameter (or derive it from the current firm context)
- Use `LAMBDA_FIRM_ID` mapping to translate bucket suffix to DynamoDB firm key
- Append `?firmId={firmId}` to the URL

**Existing Lambda-routed functions** (`getTimeSeries`, `getSnapshot`,
`getClientGrowth`, etc.) already follow this pattern — use them as reference.

### 2. Keep S3-direct for non-PII endpoints

These endpoints contain advisor names (employee data, not client PII) or
aggregate metrics. They stay on S3-direct:

- `getHeaderSummary`, `getHeaderMetrics` — firm-level aggregates
- `getArchitectLeaderboard`, `getImplementorLeaderboard` — employee names only
- `getAdvisorRollingFlows` — advisor-level flows (no client PII)
- `getCumulativeChart` — timeseries (no client PII in adv/geo/aua dimensions)

### 3. Remove isFirmAdmin gate on Books tab data fetching

In `ClientsTab.tsx` line 266:
```typescript
// REMOVE: if (!firmId || !isFirmAdmin) { setIsLoading(false); return }
// REPLACE WITH:
if (!firmId) { setIsLoading(false); return }
```

Line 280: Remove `isFirmAdmin` from the dependency array of the useEffect.

**KEEP** the advisor selector dropdown gate at line 642:
```typescript
{isFirmAdmin && (  // <-- KEEP THIS
```
The dropdown stays internal-only. Partner users navigate via the
AdvisorSummaryTable row click handler (`onSelectAdvisor`).

### 4. Verify type safety

Run `bunx tsc -b` to confirm no type errors after the migration. The Lambda
endpoints return the same JSON shape as S3-direct (same gold files), so
TypeScript interfaces should not change.

## Dependencies

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform"
              task="ADVI_ANONYM.012.ds-lambda-pii-handlers"
              status="complete"/>
  <dependency agent="0.4.0_DT_ClientPlatform"
              task="ADVI_ANONYM.013.dt-authorizer-advisorid-passthrough"
              status="complete"/>
</dependencies>

**DO NOT start until both .012 and .013 are complete.** The Lambda handlers
must exist and the advisorId must flow through the authorizer before the
frontend can use the Lambda path for PII data.

## Acceptance Criteria

- [ ] 5 PII endpoint functions migrated from S3-direct to Lambda path
- [ ] Each uses `?firmId=` parameter with `LAMBDA_FIRM_ID` mapping
- [ ] `isFirmAdmin` gate removed from Books tab data fetch (kept on advisor dropdown)
- [ ] `bunx tsc -b` passes
- [ ] Non-PII endpoints confirmed still on S3-direct
- [ ] Code committed on portal DEV branch
