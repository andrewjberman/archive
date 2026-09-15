# IRPT_FNTEND.TO-FE-s-49 -- Investor Reporting is Opal-admin only: result

Worker `0.9.0_WK_IRPT_FNTEND~2`. Workspace branch `wk-irpt_fntend-8-2-fe-s-49` (cut at 9a05002d39); portal branch of the same name, cut from portal DEV 1f3ce9f0. Portal commits (LOCAL, PORTAL FROZEN): `61f5c76b` (the three gate hunks + the test), `640379b8` (the entry-point census classifies each line). Every figure below is copied from a run log under `<WS>/.scratch/`.

## Verdicts

| criterion | status | deciding line |
|---|---|---|
| F49-AC1 | PASS | `rc=0` |
| F49-AC2 | PASS | `AN OPAL INTERNAL ADMIN REACHES BOTH ROUTES: 2 of 2` |
| F49-AC3 | PASS | `A PARTNER-FIRM ADMIN IS REFUSED ON BOTH ROUTES: 6 of 6` |
| F49-AC4 | PASS | `A NON-ADMIN IS REFUSED ON BOTH ROUTES: 8 of 8 (4 identities x 2 routes)` |
| F49-AC5 | PASS | `THE NAV SHOWS INVESTOR REPORTING ONLY TO THE OPAL INTERNAL ADMIN: yes (shown to 1 of 8 identities)` |
| F49-AC6 | PASS | `BEFORE (DEV 1f3ce9f0): A PARTNER-FIRM USER REACHED THE PAGE: yes (6 of 12 renders: 49financial user @ /investor-reporting; 49financial admin @ /investor-reporti` |
| F49-AC7 | PASS | `EVERY INVESTOR REPORTING ROUTE AND NAV ENTRY CARRIES THE OPAL-ADMIN PREDICATE: 3 of 3` |
| F49-AC8 | PASS | `THE THREE GATE HUNKS ARE BYTE-IDENTICAL TO 2.0.0_SA_COO~D'S c29a8b86: 3 of 3` |
| F49-AC9 | FAIL | `Ran 9 tests across 1 file. [5.20s]` |
| F49-AC10 | PASS | `EVERY ENDPOINT INVESTOR REPORTING CALLS HAS A PRINTED ADMIN-ONLY ANSWER: 12 of 12` |
| F49-AC11 | PASS | `0 fail` |
| F49-AC12 | UNVERIFIABLE-BY-INSTRUMENT | `RECORDED (no verdict): (1) route gate: partner-firm admins refused 6 of 6, non-admins 8 of 8, Opal admin reaches 2 of 2 (F49-AC2..AC4, portal 640379b8); nav sho` |

The order stays `pending`: F49-AC9 is REFUSED under the CTO's ruling, so not every mechanical criterion passes by output.

## The App.tsx diff (portal 1f3ce9f0 -> 640379b8): the three gate hunks and nothing else

```diff
diff --git a/src/App.tsx b/src/App.tsx
index 024fc714..0da43944 100644
--- a/src/App.tsx
+++ b/src/App.tsx
@@ -91,7 +91,9 @@ const NAV_SECTIONS: NavSection[] = [
       { path: '/market', label: 'Market Overview', icon: BarChart3 },
       { path: '/portfolios', label: 'Model Portfolios', icon: Briefcase },
       { path: '/advisor-intelligence', label: 'Advisor Intelligence', icon: Brain },
-      { path: '/investor-reporting', label: 'Investor Reporting', icon: FileText },
+      // Opal Admins only (Andrew-direct 2026-09-15 ~04:4xZ): an admin role AND the internal tier (opal-capital). The
+      // route below carries the same two requirements, so the page is gated where it lives, not only in this list.
+      { path: '/investor-reporting', label: 'Investor Reporting', icon: FileText, requiresAdmin: true, requiresTier: 'internal' },
     ],
   },
   {
@@ -418,7 +420,7 @@ function DashboardLayout() {
                   </ProtectedRoute>
                 }
               />
-              <Route path="/investor-reporting" element={<ProtectedRoute><InvestorReporting /></ProtectedRoute>} />
+              <Route path="/investor-reporting" element={<ProtectedRoute requireAdmin requireInternal><InvestorReporting /></ProtectedRoute>} />
               <Route path="/philosophy" element={<ProtectedRoute><CapitalMarketAssumptions /></ProtectedRoute>} />
               {/* OPAL_INVPHL.TO-2 R2: /cma REDIRECTS -- advisors bookmark pages and links
                   live in email, so a dead URL is a support ticket for no benefit.
@@ -570,7 +572,7 @@ function App() {
           }
         />
 
-        <Route path="/investor-reporting/print" element={<ProtectedRoute><InvestorReportingPrint /></ProtectedRoute>} />
+        <Route path="/investor-reporting/print" element={<ProtectedRoute requireAdmin requireInternal><InvestorReportingPrint /></ProtectedRoute>} />
         {/* Protected dashboard routes */}
         <Route
           path="/*"
```

## firmAccess.ts: the removal that was MEASURED, and reverted

The CTO's ruling (96924) lands the removal only if the whole suite stays green. It was applied in the working copy over the committed gate (portal 61f5c76b) and measured, and it did NOT stay green:

```diff
--- a/src/lib/firmAccess.ts
+++ b/src/lib/firmAccess.ts (measured, NOT committed)
@@ -52,5 +52,4 @@
     '/macro',
     '/trade-submission',
-    '/investor-reporting',
   ]),
   'inflection': new Set([
@@ -66,5 +65,4 @@
     // item in the inflection allowlist, so the section auto-hides (App.tsx:309-312)
     // and isPathAllowedForFirm gates the /trade-submission route → redirect to /market.
-    '/investor-reporting',
   ]),
   'cottonwood': new Set([
@@ -90,5 +88,4 @@
     '/macro',
     '/trade-submission',
-    '/investor-reporting',
   ]),
   // ADVI_DEMOV1.008 — demo tenant gets the full canonical Opal experience
```

Whole suite with the removal (`<WS>/.scratch/suite_removed.log`):

```
✗ F14-AC2 -- the three registry firms reach the route > ALLOWED -- isPathAllowedForFirm is true for each granted firm
✗ F14-AC2 -- the three registry firms reach the route > the grant is in the MATRIX, not in some other branch of the guard
✗ F14-AC3 -- the refusals still refuse, and the edit is three lines > FIRMACCESS DIFF -- exactly three added lines, none removed, since the baseline [516.00ms]
 566 pass
 18 skip
 3 fail
Ran 587 tests across 103 files. [57.81s]
```

fe-s-14 alone with the removal (`<WS>/.scratch/fe14_removed.log`) printed `ALLOWED: 0 of 3` and `FIRMACCESS DIFF: +0 -0`. Its assertions at portal 1f3ce9f0 `src/pages/InvestorReporting/__tests__/fe-s-14/allowlist.test.ts:52`, `:62` and `:96` require the three entries. That file is outside this order's grant, so the entries were restored (`git diff --quiet HEAD -- src/lib/firmAccess.ts` rc 0, never committed removed), row IRPT_FNTEND-W2-S34 is filed BLOCKING/INERT, and F49-AC9 is REFUSED with that measurement. No product line of firmAccess.ts changes on this branch.

## The whole-suite census of record (F49-AC11)

```
PORT 5267 CLOSED ECONNREFUSED 3ms
 569 pass
 18 skip
 0 fail
 2445 expect() calls
Ran 587 tests across 103 files. [58.19s]
failing-case lines ((fail) / x-mark) in the run: 0
```

## The backend census (F49-AC10), read-only

```
[shell precondition, not part of the command: IRPT_FE_DEV_PORT=5267 exported; port 5267 measured CLOSED (node net.connect -> ECONNREFUSED 3ms) in the same shell before the run]
ENDPOINTS (committed src/api/endpoints/investor-reporting.ts IR_ROUTE_TABLE, the LiveClient's only table): 12
SHARED BOUNDARY (every entry below runs it):
  infra/aws/lambda/investor-reporting/_authz/served.py:575 -- the ONLY principal refusal before the guard is an absent verified firm (NOT_AUTHORIZED): found; lines naming x-user-role / 'admin' / opal-capital: 0
  infra/aws/lambda/investor-reporting/_authz/enforce.py:272 -- resolve_now refuses principal_class UNKNOWN (NO_PRINCIPAL): found
  infra/aws/lambda/investor-reporting/_scope/resolve.py:186 -- a role=admin caller with ANY verified firm is FIRM_OPERATIONS: found; the condition names opal: no
  infra/aws/lambda/investor-reporting/_scope/resolve.py:193 -- an advisorId caller (not admin) is FIRM_ADVISOR: found
  infra/aws/lambda/investor-reporting/_scope/resolve.py:345 -- FIRM_OPERATIONS is served its verified firm's population: found
  EDGE infra/aws/lambda-edge/auth-validator-edge/index.mjs: 0 line(s) name investor-reporting (no path rule of its own when 0)
  EDGE infra/aws/lambda-edge/auth-validator-edge/tier_policy.mjs: 0 line(s) name investor-reporting (no path rule of its own when 0)
  EDGE infra/aws/users/lambda/portal-authorizer/index.mjs: 0 line(s) name investor-reporting (no path rule of its own when 0)
  GET /api/scoped/investor-reporting/directory/search [directory-search, investor-reporting.ts:179] -> docs/contracts/investor-reporting/v1/routes.json:19 handler irpt-directory-search -> admin-only: no -- infra/aws/lambda/investor-reporting/directory/entry.py:152 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  POST /api/scoped/investor-reporting/directory/resolve [resolve-scope, investor-reporting.ts:180] -> docs/contracts/investor-reporting/v1/routes.json:29 handler irpt-directory-search -> admin-only: no -- infra/aws/lambda/investor-reporting/directory/entry.py:152 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/performance/{accountSetId} [performance-report, investor-reporting.ts:181] -> docs/contracts/investor-reporting/v1/routes.json:39 handler irpt-performance-adapter -> admin-only: no -- infra/aws/lambda/investor-reporting/performance/entry.py:107 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  POST /api/scoped/investor-reporting/analysis [analysis-requests, investor-reporting.ts:182] -> docs/contracts/investor-reporting/v1/routes.json:49 handler irpt-ycharts-generate -> admin-only: no -- infra/aws/lambda/investor-reporting/ycharts/generate/entry.py:178 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/analysis/{jobId}/sections [analysis-report, investor-reporting.ts:183] -> docs/contracts/investor-reporting/v1/routes.json:59 handler irpt-status -> admin-only: no -- infra/aws/lambda/investor-reporting/ops/entry.py:92 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/narrative/{reportId} [narrative-packet, investor-reporting.ts:184] -> docs/contracts/investor-reporting/v1/routes.json:69 handler irpt-narrative -> admin-only: no -- infra/aws/lambda/investor-reporting/narrative/entry.py:121 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/status [status-summary, investor-reporting.ts:185] -> docs/contracts/investor-reporting/v1/routes.json:79 handler irpt-status -> admin-only: no -- infra/aws/lambda/investor-reporting/ops/entry.py:92 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/status/{jobId} [status-job, investor-reporting.ts:186] -> docs/contracts/investor-reporting/v1/routes.json:90 handler irpt-status -> admin-only: no -- infra/aws/lambda/investor-reporting/ops/entry.py:92 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  POST /api/scoped/investor-reporting/export [submit-export, investor-reporting.ts:187] -> docs/contracts/investor-reporting/v1/routes.json:101 handler irpt-export-render -> admin-only: no -- infra/aws/lambda/investor-reporting/export/entry.py:190 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/export/{exportId} [export-receipt, investor-reporting.ts:188] -> docs/contracts/investor-reporting/v1/routes.json:111 handler irpt-export-render -> admin-only: no -- infra/aws/lambda/investor-reporting/export/entry.py:190 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/export/{exportId}/download [export-download, investor-reporting.ts:189] -> docs/contracts/investor-reporting/v1/routes.json:121 handler irpt-export-render -> admin-only: no -- infra/aws/lambda/investor-reporting/export/entry.py:190 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/holdings/{accountSetId} [holdings-snapshot, investor-reporting.ts:190] -> docs/contracts/investor-reporting/v1/routes.json:132 handler irpt-holdings -> admin-only: no -- infra/aws/lambda/investor-reporting/holdings/entry.py:159 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
ADMIN-ONLY ANSWERS: yes 0, no 12, UNKNOWN 0 of 12 -- THE PORTAL GATE IS THE ONLY ADMIN WALL; the backend is a FIRM wall
EVERY ENDPOINT INVESTOR REPORTING CALLS HAS A PRINTED ADMIN-ONLY ANSWER: 12 of 12
 9 pass
 0 fail
Ran 9 tests across 1 file. [5.20s]
```

**Answer for Andrew: the portal gate is the only ADMIN wall.** Every one of the 12 routes the page calls runs the shared `served.Entry` boundary, which refuses only an absent verified firm (`served.py:575`) and principal class UNKNOWN (`enforce.py:272`). A partner firm's admin resolves FIRM_OPERATIONS (`resolve.py:186`) and a partner advisor FIRM_ADVISOR (`resolve.py:193`), and both are served their OWN firm's scope (`resolve.py:345`). Neither the edge validator, its tier policy nor the portal authorizer carries a rule naming investor-reporting. So the backend is a FIRM wall, not an admin wall.

## How the test exercises the gate (RULING AC)

- Every inspected file is read as a committed blob (`git cat-file blob <rev>:<path>`), at HEAD and at 1f3ce9f0.
- ProtectedRoute.tsx and firmAccess.ts at each revision are written into `fe-s-49/.materialized/<run>/<rev>/` and imported from there, then removed. Exactly two import specifiers are re-pointed (`../hooks/useAuth`, `./LoadingSpinner`) to the checkout's modules, because they carry the auth context the test provides. The test refuses to run if either, or AuthContext.context.ts, differs from HEAD in the checkout.
- The outcome is the element the real ProtectedRoute returns: REDIRECT when it is react-router's `Navigate` (its `to` printed), CHILDREN when the probe child renders.
- The nav filter (a closure inside DashboardLayout) and `hasAccess` (inside AuthProvider) are lifted out of the committed sources by the TypeScript parser and evaluated unchanged. The lifted source is printed.

## Notes

- At 1f3ce9f0, partner users reached `/investor-reporting` but were redirected from `/investor-reporting/print`, because the allowlist never listed the print path (F49-AC6: 6 of 12 renders reached the page).
- The dashboard routes also sit inside the outer `<Route path="/*">` wrapped in a plain `<ProtectedRoute>` (App.tsx:577), which applies the firm allowlist again. The route's own `requireAdmin requireInternal` is the gate graded.
- No link or navigation into the page exists outside App.tsx (F49-AC7: 0 links among 4 non-App, non-test lines).
- F41-AC5 did not time out in either whole-suite run.

## Appendix: the deciding admin-gate run (`<WS>/.scratch/ag_final.log`)

```
bun test v1.3.9 (cf6cdbbb)

src\pages\InvestorReporting\__tests__\fe-s-49\admin-gate.test.ts:
MATERIALIZED: HEAD and 1f3ce9f0 ProtectedRoute.tsx + firmAccess.ts from committed blobs; re-pointed specifiers (each counted once):
  from '../hooks/useAuth'  ->  from '../../../../../../../../hooks/useAuth'
  from './LoadingSpinner'  ->  from '../../../../../../../../components/LoadingSpinner'
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as opal-capital admin: CHILDREN
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as opal-capital admin: CHILDREN
AN OPAL INTERNAL ADMIN REACHES BOTH ROUTES: 2 of 2
FIRMS WHOSE ALLOWLIST LISTED /investor-reporting AT DEV 1f3ce9f0 (firmAccess.ts blob): 3 -- 49financial, inflection, cottonwood
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as 49financial admin: REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as 49financial admin: REDIRECT -> /market
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as inflection admin: REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as inflection admin: REDIRECT -> /market
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as cottonwood admin: REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as cottonwood admin: REDIRECT -> /market
A PARTNER-FIRM ADMIN IS REFUSED ON BOTH ROUTES: 6 of 6
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as opal-capital user (role user): REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as opal-capital user (role user): REDIRECT -> /market
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as 49financial user (role user): REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as 49financial user (role user): REDIRECT -> /market
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as inflection user (role user): REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as inflection user (role user): REDIRECT -> /market
  HEAD App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal> as cottonwood user (role user): REDIRECT -> /market
  HEAD App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal> as cottonwood user (role user): REDIRECT -> /market
A NON-ADMIN IS REFUSED ON BOTH ROUTES: 8 of 8 (4 identities x 2 routes)
LIFTED FROM HEAD App.tsx:305 (the nav filter, evaluated unchanged):
item => {
                // Firm-level page-access matrix (opal-capital sees all,
                // partner firms see only paths in their FIRM_ALLOWED_PATHS).
                if (!isPathAllowedForFirm(claims?.firmId, item.path)) {
                  return false
                }
                // Check dev requirement
                if (item.requiresDev && claims?.userType !== 'Dev') {
                  return false
                }
                // Check admin requirement
                if (item.requiresAdmin && user?.role !== 'admin') {
                  return false
                }
                // Check tier requirement
                if (item.requiresTier && !hasAccess(item.requiresTier)) {
                  return false
                }
                return true
              }
LIFTED FROM HEAD AuthContext.tsx:758 (hasAccess, evaluated unchanged):
(requiredTier: string) => {
    if (!state.claims) return false
    if (requiredTier === 'internal') return state.claims.firmId === 'opal-capital'
    return true
  }
  HEAD nav item in section 'insights' (section requiresDev=false): {"path":"/investor-reporting","label":"Investor Reporting","icon":"icon:FileText","requiresAdmin":true,"requiresTier":"internal"}
  NAV (HEAD) for opal-capital admin: SHOWN (1 investor-reporting nav item(s))
  NAV (HEAD) for 49financial admin: HIDDEN (1 investor-reporting nav item(s))
  NAV (HEAD) for inflection admin: HIDDEN (1 investor-reporting nav item(s))
  NAV (HEAD) for cottonwood admin: HIDDEN (1 investor-reporting nav item(s))
  NAV (HEAD) for opal-capital user (role user): HIDDEN (1 investor-reporting nav item(s))
  NAV (HEAD) for 49financial user (role user): HIDDEN (1 investor-reporting nav item(s))
  NAV (HEAD) for inflection user (role user): HIDDEN (1 investor-reporting nav item(s))
  NAV (HEAD) for cottonwood user (role user): HIDDEN (1 investor-reporting nav item(s))
  CONTROL (DEV 1f3ce9f0 nav item + allowlist, same lifted filter): shown to 3 of 3 partner users (49financial, inflection, cottonwood)
THE NAV SHOWS INVESTOR REPORTING ONLY TO THE OPAL INTERNAL ADMIN: yes (shown to 1 of 8 identities)
  1f3ce9f0 App.tsx:421 /investor-reporting <ProtectedRoute> as 49financial user: CHILDREN
  1f3ce9f0 App.tsx:573 /investor-reporting/print <ProtectedRoute> as 49financial user: REDIRECT -> /market
  1f3ce9f0 App.tsx:421 /investor-reporting <ProtectedRoute> as 49financial admin: CHILDREN
  1f3ce9f0 App.tsx:573 /investor-reporting/print <ProtectedRoute> as 49financial admin: REDIRECT -> /market
  1f3ce9f0 App.tsx:421 /investor-reporting <ProtectedRoute> as inflection user: CHILDREN
  1f3ce9f0 App.tsx:573 /investor-reporting/print <ProtectedRoute> as inflection user: REDIRECT -> /market
  1f3ce9f0 App.tsx:421 /investor-reporting <ProtectedRoute> as inflection admin: CHILDREN
  1f3ce9f0 App.tsx:573 /investor-reporting/print <ProtectedRoute> as inflection admin: REDIRECT -> /market
  1f3ce9f0 App.tsx:421 /investor-reporting <ProtectedRoute> as cottonwood user: CHILDREN
  1f3ce9f0 App.tsx:573 /investor-reporting/print <ProtectedRoute> as cottonwood user: REDIRECT -> /market
  1f3ce9f0 App.tsx:421 /investor-reporting <ProtectedRoute> as cottonwood admin: CHILDREN
  1f3ce9f0 App.tsx:573 /investor-reporting/print <ProtectedRoute> as cottonwood admin: REDIRECT -> /market
BEFORE (DEV 1f3ce9f0): A PARTNER-FIRM USER REACHED THE PAGE: yes (6 of 12 renders: 49financial user @ /investor-reporting; 49financial admin @ /investor-reporting; inflection user @ /investor-reporting; inflection admin @ /investor-reporting; cottonwood user @ /investor-reporting; cottonwood admin @ /investor-reporting)
HEAD App.tsx: 26 <Route> elements, 16 nav entries; minus those not under /investor-reporting: 2 route(s) + 1 nav entr(ies)
  ROUTE App.tsx:423 /investor-reporting <ProtectedRoute requireAdmin requireInternal>: CARRIES requireAdmin + requireInternal
  ROUTE App.tsx:575 /investor-reporting/print <ProtectedRoute requireAdmin requireInternal>: CARRIES requireAdmin + requireInternal
  NAV /investor-reporting requiresAdmin=true requiresTier=internal: CARRIES the predicate
  ENCLOSING ROUTE App.tsx:577 /* <ProtectedRoute> (wraps DashboardLayout, where /investor-reporting lives)
OTHER ENTRY POINTS: 29 committed src/ line(s) quote the path; 25 are App.tsx or tests; 4 other, each classified:
  src/lib/firmAccess.ts:54: '/investor-reporting',
    -> ALLOWLIST ENTRY -- not a link; it grants nothing the route gate refuses to pass (see F49-AC9)
  src/lib/firmAccess.ts:68: '/investor-reporting',
    -> ALLOWLIST ENTRY -- not a link; it grants nothing the route gate refuses to pass (see F49-AC9)
  src/lib/firmAccess.ts:92: '/investor-reporting',
    -> ALLOWLIST ENTRY -- not a link; it grants nothing the route gate refuses to pass (see F49-AC9)
  src/pages/InvestorReporting/render/PrintEntry.tsx:2: * FE-s-4 -- THE PRINT ENTRY POINT: route `/investor-reporting/print`.
    -> COMMENT -- not an entry point
  LINKS/NAVIGATIONS INTO THE PAGE OUTSIDE App.tsx: 0 (each lands on a route element enumerated above)
EVERY INVESTOR REPORTING ROUTE AND NAV ENTRY CARRIES THE OPAL-ADMIN PREDICATE: 3 of 3
c29a8b86 src/App.tsx: 5 hunks; 3 gate hunk(s) (a + line names /investor-reporting), 2 unrelated
  GATE HUNK 1: found at HEAD App.tsx:94; its removed line(s) absent from HEAD: yes
    c29a8b86 +|      // Opal Admins only (Andrew-direct 2026-09-15 ~04:4xZ): an admin role AND the internal tier (opal-capital). The
    HEAD:94     |      // Opal Admins only (Andrew-direct 2026-09-15 ~04:4xZ): an admin role AND the internal tier (opal-capital). The
    c29a8b86 +|      // route below carries the same two requirements, so the page is gated where it lives, not only in this list.
    HEAD:95     |      // route below carries the same two requirements, so the page is gated where it lives, not only in this list.
    c29a8b86 +|      { path: '/investor-reporting', label: 'Investor Reporting', icon: FileText, requiresAdmin: true, requiresTier: 'internal' },
    HEAD:96     |      { path: '/investor-reporting', label: 'Investor Reporting', icon: FileText, requiresAdmin: true, requiresTier: 'internal' },
  GATE HUNK 2: found at HEAD App.tsx:423; its removed line(s) absent from HEAD: yes
    c29a8b86 +|              <Route path="/investor-reporting" element={<ProtectedRoute requireAdmin requireInternal><InvestorReporting /></ProtectedRoute>} />
    HEAD:423    |              <Route path="/investor-reporting" element={<ProtectedRoute requireAdmin requireInternal><InvestorReporting /></ProtectedRoute>} />
  GATE HUNK 3: found at HEAD App.tsx:575; its removed line(s) absent from HEAD: yes
    c29a8b86 +|        <Route path="/investor-reporting/print" element={<ProtectedRoute requireAdmin requireInternal><InvestorReportingPrint /></ProtectedRoute>} />
    HEAD:575    |        <Route path="/investor-reporting/print" element={<ProtectedRoute requireAdmin requireInternal><InvestorReportingPrint /></ProtectedRoute>} />
  UNRELATED HUNKS CARRIED INTO HEAD: 0 of 2 (expected 0: they are not this order's)
    not ours: +|  ArrowLeftRight,
    not ours: +|      // Its own mark (Andrew-direct ~04:4xZ): the paper icon belongs to Investor Reporting. /       { path: '/trade-submission', label: 'Trade Submission', icon: ArrowLeftRight },
THE THREE GATE HUNKS ARE BYTE-IDENTICAL TO 2.0.0_SA_COO~D'S c29a8b86: 3 of 3
  49financial: DEV 1f3ce9f0 LISTS /investor-reporting; HEAD LISTS it
  inflection: DEV 1f3ce9f0 LISTS /investor-reporting; HEAD LISTS it
  cottonwood: DEV 1f3ce9f0 LISTS /investor-reporting; HEAD LISTS it
  HEAD, every firm in FIRM_ALLOWED_PATHS: 3 of 4 list /investor-reporting (49financial, inflection, cottonwood, demo)
PARTNER ALLOWLIST ENTRIES GRANTING /investor-reporting: 3 of 3 REMAIN (49financial, inflection, cottonwood)
ENDPOINTS (committed src/api/endpoints/investor-reporting.ts IR_ROUTE_TABLE, the LiveClient's only table): 12
SHARED BOUNDARY (every entry below runs it):
  infra/aws/lambda/investor-reporting/_authz/served.py:575 -- the ONLY principal refusal before the guard is an absent verified firm (NOT_AUTHORIZED): found; lines naming x-user-role / 'admin' / opal-capital: 0
  infra/aws/lambda/investor-reporting/_authz/enforce.py:272 -- resolve_now refuses principal_class UNKNOWN (NO_PRINCIPAL): found
  infra/aws/lambda/investor-reporting/_scope/resolve.py:186 -- a role=admin caller with ANY verified firm is FIRM_OPERATIONS: found; the condition names opal: no
  infra/aws/lambda/investor-reporting/_scope/resolve.py:193 -- an advisorId caller (not admin) is FIRM_ADVISOR: found
  infra/aws/lambda/investor-reporting/_scope/resolve.py:345 -- FIRM_OPERATIONS is served its verified firm's population: found
  EDGE infra/aws/lambda-edge/auth-validator-edge/index.mjs: 0 line(s) name investor-reporting (no path rule of its own when 0)
  EDGE infra/aws/lambda-edge/auth-validator-edge/tier_policy.mjs: 0 line(s) name investor-reporting (no path rule of its own when 0)
  EDGE infra/aws/users/lambda/portal-authorizer/index.mjs: 0 line(s) name investor-reporting (no path rule of its own when 0)
  GET /api/scoped/investor-reporting/directory/search [directory-search, investor-reporting.ts:179] -> docs/contracts/investor-reporting/v1/routes.json:19 handler irpt-directory-search -> admin-only: no -- infra/aws/lambda/investor-reporting/directory/entry.py:152 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  POST /api/scoped/investor-reporting/directory/resolve [resolve-scope, investor-reporting.ts:180] -> docs/contracts/investor-reporting/v1/routes.json:29 handler irpt-directory-search -> admin-only: no -- infra/aws/lambda/investor-reporting/directory/entry.py:152 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/performance/{accountSetId} [performance-report, investor-reporting.ts:181] -> docs/contracts/investor-reporting/v1/routes.json:39 handler irpt-performance-adapter -> admin-only: no -- infra/aws/lambda/investor-reporting/performance/entry.py:107 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  POST /api/scoped/investor-reporting/analysis [analysis-requests, investor-reporting.ts:182] -> docs/contracts/investor-reporting/v1/routes.json:49 handler irpt-ycharts-generate -> admin-only: no -- infra/aws/lambda/investor-reporting/ycharts/generate/entry.py:178 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/analysis/{jobId}/sections [analysis-report, investor-reporting.ts:183] -> docs/contracts/investor-reporting/v1/routes.json:59 handler irpt-status -> admin-only: no -- infra/aws/lambda/investor-reporting/ops/entry.py:92 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/narrative/{reportId} [narrative-packet, investor-reporting.ts:184] -> docs/contracts/investor-reporting/v1/routes.json:69 handler irpt-narrative -> admin-only: no -- infra/aws/lambda/investor-reporting/narrative/entry.py:121 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/status [status-summary, investor-reporting.ts:185] -> docs/contracts/investor-reporting/v1/routes.json:79 handler irpt-status -> admin-only: no -- infra/aws/lambda/investor-reporting/ops/entry.py:92 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/status/{jobId} [status-job, investor-reporting.ts:186] -> docs/contracts/investor-reporting/v1/routes.json:90 handler irpt-status -> admin-only: no -- infra/aws/lambda/investor-reporting/ops/entry.py:92 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  POST /api/scoped/investor-reporting/export [submit-export, investor-reporting.ts:187] -> docs/contracts/investor-reporting/v1/routes.json:101 handler irpt-export-render -> admin-only: no -- infra/aws/lambda/investor-reporting/export/entry.py:190 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/export/{exportId} [export-receipt, investor-reporting.ts:188] -> docs/contracts/investor-reporting/v1/routes.json:111 handler irpt-export-render -> admin-only: no -- infra/aws/lambda/investor-reporting/export/entry.py:190 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/export/{exportId}/download [export-download, investor-reporting.ts:189] -> docs/contracts/investor-reporting/v1/routes.json:121 handler irpt-export-render -> admin-only: no -- infra/aws/lambda/investor-reporting/export/entry.py:190 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
  GET /api/scoped/investor-reporting/holdings/{accountSetId} [holdings-snapshot, investor-reporting.ts:190] -> docs/contracts/investor-reporting/v1/routes.json:132 handler irpt-holdings -> admin-only: no -- infra/aws/lambda/investor-reporting/holdings/entry.py:159 (served.Entry) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:186 (partner-firm admin = FIRM_OPERATIONS) + infra/aws/lambda/investor-reporting/_scope/resolve.py:193 (partner advisor = FIRM_ADVISOR) -> infra/aws/lambda/investor-reporting/_scope/resolve.py:345 (served its firm) ; refusals only at infra/aws/lambda/investor-reporting/_authz/served.py:575 and infra/aws/lambda/investor-reporting/_authz/enforce.py:272
ADMIN-ONLY ANSWERS: yes 0, no 12, UNKNOWN 0 of 12 -- THE PORTAL GATE IS THE ONLY ADMIN WALL; the backend is a FIRM wall
EVERY ENDPOINT INVESTOR REPORTING CALLS HAS A PRINTED ADMIN-ONLY ANSWER: 12 of 12

 9 pass
 0 fail
 18 expect() calls
Ran 9 tests across 1 file. [5.20s]
```
