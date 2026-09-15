# IRPT_FNTEND.TO-FE-s-49 -- Investor Reporting is Opal-admin only: result (AMENDMENT 1)

Worker `0.9.0_WK_IRPT_FNTEND~2`. Workspace branch `wk-irpt_fntend-8-2-fe-s-49` (amendment commit 20718af324); portal branch of the same name at `0f674aa9`. Portal commits, all LOCAL (PORTAL FROZEN): `61f5c76b` and `640379b8` (the first run: the three gate hunks and the test, unchanged), `58033070` (2.0.0_SA_COO~F's sync of portal DEV 90d71d9e), `975656e3` (the allowlist removal and the fe-s-14 re-point), `0f674aa9` (the census timeout, the cost record, the AC13 bar). Every figure below is copied from a run log under `<WS>/.scratch/`, taken on the committed HEAD with a clean tree and port 5267 measured closed (PORT 5267 CLOSED ECONNREFUSED 3ms).

## Verdicts

| criterion | status | deciding line |
|---|---|---|
| F49-AC1 | PASS | `rc=0` |
| F49-AC2 | PASS | `AN OPAL INTERNAL ADMIN REACHES BOTH ROUTES: 2 of 2` |
| F49-AC3 | PASS | `A PARTNER-FIRM ADMIN IS REFUSED ON BOTH ROUTES: 6 of 6` |
| F49-AC4 | PASS | `A NON-ADMIN IS REFUSED ON BOTH ROUTES: 8 of 8 (4 identities x 2 routes)` |
| F49-AC5 | PASS | `THE NAV SHOWS INVESTOR REPORTING ONLY TO THE OPAL INTERNAL ADMIN: yes (shown to 1 of 8 identities)` |
| F49-AC6 | PASS | `BEFORE (DEV 1f3ce9f0): A PARTNER-FIRM USER REACHED THE PAGE: yes (6 of 12 renders: 49financial user @ /investor-reporting; 49financial admin @ /invest` |
| F49-AC7 | PASS | `EVERY INVESTOR REPORTING ROUTE AND NAV ENTRY CARRIES THE OPAL-ADMIN PREDICATE: 3 of 3` |
| F49-AC8 | PASS | `THE THREE GATE HUNKS ARE BYTE-IDENTICAL TO 2.0.0_SA_COO~D'S c29a8b86: 3 of 3` |
| F49-AC9 | PASS | `PARTNER ALLOWLIST ENTRIES GRANTING /investor-reporting: 0 of 3 REMAIN` |
| F49-AC10 | PASS | `EVERY ENDPOINT INVESTOR REPORTING CALLS HAS A PRINTED ADMIN-ONLY ANSWER: 12 of 12` |
| F49-AC11 | PASS | `PARTNER FIRMS REFUSED: 3 of 3` |
| F49-AC12 | PASS | `FIRMACCESS DIFF: +0 -3` |
| F49-AC13 | PASS | `THE CENSUS TEST'S TIMEOUT IS 3 TIMES ITS HIGHEST RECORDED COST: yes` |
| F49-AC14 | PASS | `0 fail` |
| F49-AC15 | RECORDED (judgment) | graded by 3.0.0_SA_CVO at L9 |

Every mechanical criterion passes by output; the order is flipped to `complete` in the same commit as this file.

## App.tsx (portal 1f3ce9f0 -> 0f674aa9): the three gate hunks and nothing else. Amendment 1 did not touch it: `git diff 58033070 0f674aa9 -- src/App.tsx` is empty.

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

## firmAccess.ts (portal 1f3ce9f0 -> 0f674aa9): three lines removed, nothing else (F49-AC9, F49-AC12)

```diff
diff --git a/src/lib/firmAccess.ts b/src/lib/firmAccess.ts
index 9d99a596..73cf302f 100644
--- a/src/lib/firmAccess.ts
+++ b/src/lib/firmAccess.ts
@@ -51,7 +51,6 @@ export const FIRM_ALLOWED_PATHS: Record<string, ReadonlySet<string>> = {
     '/valuations',
     '/macro',
     '/trade-submission',
-    '/investor-reporting',
   ]),
   'inflection': new Set([
     '/market',
@@ -65,7 +64,6 @@ export const FIRM_ALLOWED_PATHS: Record<string, ReadonlySet<string>> = {
     // section at this time (Andrew direct 2026-05-28). It is the only Tools-section
     // item in the inflection allowlist, so the section auto-hides (App.tsx:309-312)
     // and isPathAllowedForFirm gates the /trade-submission route → redirect to /market.
-    '/investor-reporting',
   ]),
   'cottonwood': new Set([
     '/market',
@@ -89,7 +87,6 @@ export const FIRM_ALLOWED_PATHS: Record<string, ReadonlySet<string>> = {
     '/valuations',
     '/macro',
     '/trade-submission',
-    '/investor-reporting',
   ]),
   // ADVI_DEMOV1.008 — demo tenant gets the full canonical Opal experience
   // (same path set as 49financial / inflection); opal-data-demo is a
```

## fe-s-14/allowlist.test.ts (58033070 -> 975656e3): the re-point (F49-AC11, F49-AC12)

F14-AC2 now asserts the three firms are refused and absent from their sets, with the internal short-circuit printed beside it. F14-AC3 measures `+0 -3` between `1f3ce9f0` and HEAD (committed trees). The header records the retirement and by whom (96903, 96961). The `demo` / unknown-id test and the positive control are byte-unchanged. Row W2-S35: that control still refuses only the retired `3<TAB>0` value.

```diff
diff --git a/src/pages/InvestorReporting/__tests__/fe-s-14/allowlist.test.ts b/src/pages/InvestorReporting/__tests__/fe-s-14/allowlist.test.ts
index 3ef19e91..0bf3a41e 100644
--- a/src/pages/InvestorReporting/__tests__/fe-s-14/allowlist.test.ts
+++ b/src/pages/InvestorReporting/__tests__/fe-s-14/allowlist.test.ts
@@ -1,23 +1,32 @@
 /**
- * F14-AC2 / F14-AC3 -- NO PARTNER FIRM COULD REACH /investor-reporting.
+ * F14-AC2 / F14-AC3 -- NO PARTNER FIRM REACHES /investor-reporting.
+ * (Re-pointed by FE-s-49 amendment 1: criteria F49-AC11 and F49-AC12.)
  *
- * `src/lib/firmAccess.ts`'s `FIRM_ALLOWED_PATHS` is the ONLY switch on this
- * route: `App.tsx` wraps it in a plain `<ProtectedRoute>`, whose firm-matrix
- * guard bounces any firm whose set does not name the path to
- * `FIRM_DEFAULT_LANDING` (`/market`). The page shipped through eleven cells and
- * eleven proofs while every partner session landed on /market -- because every
- * one of those proofs ran as the INTERNAL user, for whom `isPathAllowedForFirm`
- * short-circuits to true and the matrix is never consulted.
+ * THE GRANT THIS FILE USED TO ASSERT IS RETIRED. FE-s-14 wrote it to prove a
+ * grant: 1.0.0_SA_CTO's earlier ruling added '/investor-reporting' to the
+ * 49financial, inflection and cottonwood sets of `FIRM_ALLOWED_PATHS` (+3 -0
+ * against `edab15b5`). Andrew's word, relayed by 0.0.0_AB_MSTR in msg 96903 --
+ * "Investor Reporting must remain Opal Admin gated, no clients are allowed to
+ * see that" -- superseded it, and 1.0.0_SA_CTO's ruling 96961 retired the grant:
+ * FE-s-49 removed the three entries. The page is gated in App.tsx by
+ * `<ProtectedRoute requireAdmin requireInternal>` (FE-s-49), and no allowlist
+ * may grant what that gate refuses.
  *
- * THREE CLAIMS, and the third is the one that makes the first two safe:
- *   1. `ALLOWED: 3 of 3`  -- 49financial, inflection and cottonwood now reach it;
- *   2. `REFUSED: 2 of 2`  -- `demo` (not onboarded) and an unknown id still do
- *                            not, so the grant is a grant and not a hole;
- *   3. `FIRMACCESS DIFF: +3 -0` -- the file gained exactly three lines against
- *      `edab15b5` and lost none. Read by GIT, not by counting occurrences: a
- *      count of `'/investor-reporting'` would be just as green if this cell had
- *      also rewritten a neighbouring firm's set, which is the blast radius the
- *      criterion is actually about.
+ * THREE CLAIMS:
+ *   1. `PARTNER FIRMS REFUSED: 3 of 3` -- the three firms the retired grant
+ *      named are refused by `isPathAllowedForFirm`, and none of their sets
+ *      lists the path. The internal short-circuit still returns true for every
+ *      path, so a refusal here is the matrix speaking, not the short-circuit;
+ *   2. `REFUSED: 2 of 2`  -- `demo` and an unknown id are refused (unchanged);
+ *   3. `FIRMACCESS DIFF: +0 -3` -- the retirement, read by GIT between DEV
+ *      `1f3ce9f0` (the last DEV before FE-s-49) and the committed HEAD: the
+ *      three entry lines removed and none added. A count of occurrences would
+ *      be just as green if a neighbouring firm's set had also been rewritten.
+ *
+ * WHAT IS READ: `isPathAllowedForFirm` and `FIRM_ALLOWED_PATHS` are imported
+ * from the checkout's module, because that module is what the app runs; the
+ * diff reads committed trees only (`1f3ce9f0` against HEAD). The positive
+ * control and the `demo` / unknown-id arm are FE-s-14's, unchanged.
  */
 
 import { describe, expect, test } from 'bun:test'
@@ -32,36 +41,42 @@ import {
 
 const ROUTE = '/investor-reporting'
 const PORTAL_ROOT = fileURLToPath(new URL('../../../../../', import.meta.url)).replace(/[\\/]+$/, '')
-/** The commit this cell's diff is measured against -- the FE-s-11 drain. */
+/** FE-s-14's baseline, the FE-s-11 drain; the positive control below still reads against it. */
 const BASELINE = 'edab15b5'
+/** The last portal DEV before FE-s-49: the retirement of the grant is measured from here to HEAD. */
+const RETIREMENT_BASE = '1f3ce9f0'
 
-/** The three firms the CTO's ruling names. `demo` is deliberately not one. */
-const GRANTED: readonly string[] = ['49financial', 'inflection', 'cottonwood']
+/** The three firms the RETIRED grant named (96903, 96961); each is now REFUSED. `demo` was never one. */
+const RETIRED: readonly string[] = ['49financial', 'inflection', 'cottonwood']
 /** Not onboarded, and an id no firm has. */
 const REFUSED: readonly string[] = ['demo', 'not-a-firm-zz']
 
-describe('F14-AC2 -- the three registry firms reach the route', () => {
-  test('ALLOWED -- isPathAllowedForFirm is true for each granted firm', () => {
-    let allowed = 0
-    for (const firm of GRANTED) {
+describe('F14-AC2 (re-pointed, F49-AC11) -- the three partner firms are refused the route', () => {
+  test('REFUSED -- isPathAllowedForFirm is false for each firm whose grant was retired', () => {
+    let refused = 0
+    for (const firm of RETIRED) {
       const ok = isPathAllowedForFirm(firm, ROUTE)
-      console.log(`  ${firm} -> ${ROUTE}: ${ok ? 'ALLOWED' : 'REFUSED'}`)
-      if (ok) allowed += 1
+      console.log(`  ${firm} -> ${ROUTE}: ${ok ? 'ALLOWED' : `REFUSED (lands on ${FIRM_DEFAULT_LANDING})`}`)
+      if (!ok) refused += 1
     }
-    console.log(`ALLOWED: ${allowed} of ${GRANTED.length}`)
-    expect(allowed).toBe(3)
+    console.log(`PARTNER FIRMS REFUSED: ${refused} of ${RETIRED.length}`)
+    expect(refused).toBe(3)
   })
 
-  test('the grant is in the MATRIX, not in some other branch of the guard', () => {
+  test('the refusal is the MATRIX, not some other branch of the guard', () => {
     // DISCRIMINATION: the internal short-circuit returns true for every path,
     // so a test that only ever asked about the internal user could not tell a
     // granted route from an ungranted one. Both are printed.
-    expect(isPathAllowedForFirm(INTERNAL_FIRM_ID, ROUTE)).toBe(true)
-    expect(isPathAllowedForFirm(INTERNAL_FIRM_ID, '/a-route-that-does-not-exist')).toBe(true)
-    for (const firm of GRANTED) {
-      expect(FIRM_ALLOWED_PATHS[firm].has(ROUTE)).toBe(true)
+    const internalRoute = isPathAllowedForFirm(INTERNAL_FIRM_ID, ROUTE)
+    const internalAny = isPathAllowedForFirm(INTERNAL_FIRM_ID, '/a-route-that-does-not-exist')
+    console.log(`  INTERNAL SHORT-CIRCUIT (${INTERNAL_FIRM_ID}): ${ROUTE} ${internalRoute}; an unknown path ${internalAny}`)
+    expect(internalRoute).toBe(true)
+    expect(internalAny).toBe(true)
+    for (const firm of RETIRED) {
+      expect(FIRM_ALLOWED_PATHS[firm]).toBeDefined()
+      expect(FIRM_ALLOWED_PATHS[firm].has(ROUTE)).toBe(false)
     }
-    console.log(`MATRIX MEMBERSHIP: ${GRANTED.filter((f) => FIRM_ALLOWED_PATHS[f].has(ROUTE)).length} of ${GRANTED.length}`)
+    console.log(`MATRIX MEMBERSHIP: ${RETIRED.filter((f) => FIRM_ALLOWED_PATHS[f].has(ROUTE)).length} of ${RETIRED.length} list ${ROUTE}`)
   })
 })
 
@@ -82,8 +97,9 @@ describe('F14-AC3 -- the refusals still refuse, and the edit is three lines', ()
     expect(FIRM_ALLOWED_PATHS['not-a-firm-zz']).toBeUndefined()
   })
 
-  test('FIRMACCESS DIFF -- exactly three added lines, none removed, since the baseline', () => {
-    const raw = execSync(`git diff --numstat ${BASELINE} -- src/lib/firmAccess.ts`, {
+  test('FIRMACCESS DIFF -- the retirement: exactly three lines removed, none added, since DEV 1f3ce9f0', () => {
+    // Committed trees on both sides (RETIREMENT_BASE against HEAD), never the working copy.
+    const raw = execSync(`git diff --numstat ${RETIREMENT_BASE} HEAD -- src/lib/firmAccess.ts`, {
       cwd: PORTAL_ROOT,
       encoding: 'utf8',
     })
@@ -91,10 +107,10 @@ describe('F14-AC3 -- the refusals still refuse, and the edit is three lines', ()
     const parts = line.split('\t')
     const added = Number(parts[0])
     const removed = Number(parts[1])
-    console.log(`GIT NUMSTAT (${BASELINE}): ${line}`)
+    console.log(`GIT NUMSTAT (${RETIREMENT_BASE}..HEAD): ${line}`)
     console.log(`FIRMACCESS DIFF: +${added} -${removed}`)
-    expect(added).toBe(3)
-    expect(removed).toBe(0)
+    expect(added).toBe(0)
+    expect(removed).toBe(3)
   })
 
   test('POSITIVE CONTROL: the numstat reader is not a constant', () => {
```

## F49-AC10 timeout and the cost record (F49-AC13, row S67)

F49-AC10's test call now ends `}, 20109)`: 3 x 6703 ms, the highest cost in the committed `fe-s-49/recorded-costs.json` (the issuer's, row IRPT_FNTEND-S67 at `INVESTIGATION_v2.md@ca53c9d094`). The worker's own costs, from junit reports taken with a provisional 60000 ms timeout before the commit: 4907, 5187 and 6343 ms alone, 6188 ms inside the whole suite. The bar reads the third argument and the record from committed blobs only, and times nothing.

```
 .../__tests__/fe-s-49/admin-gate.test.ts           | 51 ++++++++++++++++++----
 .../__tests__/fe-s-49/recorded-costs.json          | 14 ++++++
 2 files changed, 57 insertions(+), 8 deletions(-)
```

## The backend census (F49-AC10), read-only

**For Andrew: the portal gate is the only ADMIN wall.** All 12 routes the page calls run the shared `served.Entry` boundary. It refuses only an absent verified firm (`served.py:575`) and principal class UNKNOWN (`enforce.py:272`). A partner firm's admin resolves FIRM_OPERATIONS (`resolve.py:186`) and a partner advisor FIRM_ADVISOR (`resolve.py:193`), and both are served their OWN firm's scope (`resolve.py:345`). Neither the edge validator, its tier policy nor the portal authorizer has a rule naming investor-reporting. So the backend is a FIRM wall, not an admin wall.

## The whole-suite census of record (F49-AC14)

```
[shell precondition, not part of the command: IRPT_FE_DEV_PORT=5267 exported; port 5267 measured CLOSED (PORT 5267 CLOSED ECONNREFUSED 3ms) in the same shell before the run; portal HEAD 0f674aa9, clean tree]
 587 pass
 21 skip
 0 fail
 2494 expect() calls
Ran 608 tests across 106 files. [99.01s]
failing-case lines ((fail) / x-mark) in the run: 0
```

F41-AC5's control did not time out. The one `timed out` line in the log is fe-s-46's seeded 1 ms control arm, printed by a passing test.

## Rows

- IRPT_FNTEND-W2-S34 (first run; BLOCKING, INERT): answered by amendment 1. The row is not edited.
- IRPT_FNTEND-W2-S35 (this run; OBSERVATION, INERT): fe-s-14's unchanged positive control no longer bounds the re-pointed diff test.

## Appendix: the deciding runs

`<WS>/.scratch/ag.log`:

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
OTHER ENTRY POINTS: 26 committed src/ line(s) quote the path; 25 are App.tsx or tests; 1 other, each classified:
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
  49financial: DEV 1f3ce9f0 LISTS /investor-reporting; HEAD does not list it
  inflection: DEV 1f3ce9f0 LISTS /investor-reporting; HEAD does not list it
  cottonwood: DEV 1f3ce9f0 LISTS /investor-reporting; HEAD does not list it
  HEAD, every firm in FIRM_ALLOWED_PATHS: 0 of 4 list /investor-reporting (49financial, inflection, cottonwood, demo)
PARTNER ALLOWLIST ENTRIES GRANTING /investor-reporting: 0 of 3 REMAIN
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
HEAD src/pages/InvestorReporting/__tests__/fe-s-49/admin-gate.test.ts:606 "F49-AC10 -- every endpoint Investor Reporting calls has a printed admin-only answer (READ-ONLY census)" third argument: 20109
HEAD src/pages/InvestorReporting/__tests__/fe-s-49/recorded-costs.json: 6 recorded cost(s), 6 usable
  6703 ms -- the issuer, 2.0.0_SA_COO~F: admin-gate.test.ts alone on an untouched pair (workspace d0a5ad368d, portal 640379b8); timed out at bun's default 5000 ms [row IRPT_FNTEND-S67, org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md@ca53c9d094]
  5938 ms -- the issuer, 2.0.0_SA_COO~F: inside the whole InvestorReporting suite on the same pair (567 pass / 18 skip / 2 fail of 587); timed out at bun's default 5000 ms [row IRPT_FNTEND-S67, org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md@ca53c9d094]
  4907 ms -- 0.9.0_WK_IRPT_FNTEND~2: admin-gate.test.ts alone, run 1 of 3, junit reporter, portal 58033070 plus this amendment's uncommitted edits, provisional timeout 60000 [worker junit report <WS>/.scratch/cost_alone_1.xml, testcase time 4.907]
  5187 ms -- 0.9.0_WK_IRPT_FNTEND~2: admin-gate.test.ts alone, run 2 of 3, same checkout [worker junit report <WS>/.scratch/cost_alone_2.xml, testcase time 5.187]
  6343 ms -- 0.9.0_WK_IRPT_FNTEND~2: admin-gate.test.ts alone, run 3 of 3, same checkout [worker junit report <WS>/.scratch/cost_alone_3.xml, testcase time 6.343]
  6188 ms -- 0.9.0_WK_IRPT_FNTEND~2: inside the whole InvestorReporting suite (608 tests across 106 files, one bun test process), same checkout [worker junit report <WS>/.scratch/cost_suite_1.xml, testcase time 6.188]
  the issuer's two costs from row S67 (6703, 5938) in the record: 2 of 2
  TIMEOUT 20109 ms / HIGHEST RECORDED COST 6703 ms = 3.0000 (rule: 3 x, at most 60000 ms)
THE CENSUS TEST'S TIMEOUT IS 3 TIMES ITS HIGHEST RECORDED COST: yes

 10 pass
 0 fail
 20 expect() calls
Ran 10 tests across 1 file. [10.76s]

```

`<WS>/.scratch/f14.log`:

```
bun test v1.3.9 (cf6cdbbb)

src\pages\InvestorReporting\__tests__\fe-s-14\allowlist.test.ts:
  49financial -> /investor-reporting: REFUSED (lands on /market)
  inflection -> /investor-reporting: REFUSED (lands on /market)
  cottonwood -> /investor-reporting: REFUSED (lands on /market)
PARTNER FIRMS REFUSED: 3 of 3
  INTERNAL SHORT-CIRCUIT (opal-capital): /investor-reporting true; an unknown path true
MATRIX MEMBERSHIP: 0 of 3 list /investor-reporting
  demo -> /investor-reporting: REFUSED (lands on /market)
  not-a-firm-zz -> /investor-reporting: REFUSED (lands on /market)
REFUSED: 2 of 2
GIT NUMSTAT (1f3ce9f0..HEAD): 0	3	src/lib/firmAccess.ts
FIRMACCESS DIFF: +0 -3
CONTROL (index.tsx, untouched by this cell): 1	1	src/pages/InvestorReporting/index.tsx

 5 pass
 0 fail
 16 expect() calls
Ran 5 tests across 1 file. [822.00ms]

```
