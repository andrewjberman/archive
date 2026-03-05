# Task Order: SSCN — Shared Utils Extraction + Proxy Routes

```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-05-sscn-utils-extraction-proxy</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <thread_serial>SSCN_PORTAL-002</thread_serial>
    <thread_ref>org/tier2_senior/0.3.0_DE_TradingOperations/threads/SSCN_PORTAL-002-pattern-0-design-securityscanner-ui----p_0.3.1_RD_PortfolioManagement+0.3.4_RD_SecurityScanner.md</thread_ref>
  </metadata>

  <objective>
    Execute the two commitments DE made in SSCN_PORTAL-002 turn 6: (1) extract colorUtils.ts
    and factorOrder.ts from PortfolioManagement-local utils to portal-wide shared utils, and
    (2) add the three SSCN API endpoint functions to portal/src/api/endpoints/security-scanner.ts.
    This unblocks 0.3.4_RD_SecurityScanner from building against stable import paths.
  </objective>

  <scope>
    <files>
      <!-- Move (delete old, create new) -->
      <file action="create">portal/src/utils/colorUtils.ts</file>
      <file action="create">portal/src/utils/factorOrder.ts</file>
      <!-- Update all PM consumers to new import path -->
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/SecurityDetailModal.tsx</file>
      <!-- New SSCN API endpoint file -->
      <file action="create">portal/src/api/endpoints/security-scanner.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      READ BEFORE STARTING:
      - docs/architecture/SSCN_DESIGN_CONTRACT.md Section 3B — this is the authoritative spec
        for both extractions. The target paths, exported identifiers, and rationale are all
        defined there. This requirement summarizes it; defer to Section 3B on any discrepancy.
      - docs/architecture/SSCN_DESIGN_CONTRACT.md Section 3A — lists the already-shared
        components that SSCN imports directly (no extraction needed for those).

      EXTRACTION — colorUtils.ts (SSCN_DESIGN_CONTRACT.md Section 3B, item B1):
      Create portal/src/utils/colorUtils.ts by moving the contents of
      portal/src/pages/PortfolioManagement/utils/colorUtils.ts verbatim.
      Keep exported function signatures identical:
        export function getGradientBackground(value: number, min: number, max: number, inverted?: boolean): string
        export function getWhiteToGreenGradient(value: number, min: number, max: number): string
      Delete portal/src/pages/PortfolioManagement/utils/colorUtils.ts after all imports are updated.
      Source: SSCN_DESIGN_CONTRACT.md Section 3B1 (approved DE turn 3, confirmed DE turn 6).
    </requirement>
    <requirement id="2">
      EXTRACTION — factorOrder.ts (SSCN_DESIGN_CONTRACT.md Section 3B, item B2):
      Create portal/src/utils/factorOrder.ts by moving the contents of
      portal/src/pages/PortfolioManagement/utils/factorOrder.ts verbatim.
      Keep exported identifiers identical:
        export const CANONICAL_GROUP_ORDER = [...] as const
        export type CanonicalGroup = typeof CANONICAL_GROUP_ORDER[number]
        export function canonicalGroupIndex(group: string): number
      Delete portal/src/pages/PortfolioManagement/utils/factorOrder.ts after all imports are updated.
      Source: SSCN_DESIGN_CONTRACT.md Section 3B2 (approved DE turn 3, confirmed DE turn 6).

      Note: This is the 15-group PM/Yang taxonomy. SSCN's 11-category order is a separate
      SSCN-local file (categoryOrder.ts in SecurityScanner/utils/) authored by 0.3.4_RD — do
      not create it here.
    </requirement>
    <requirement id="3">
      IMPORT UPDATES — PortfolioManagement consumers:
      Grep for any file in portal/src/pages/PortfolioManagement/ that imports from
      '../utils/colorUtils' or '../utils/factorOrder' (or any relative path resolving to
      the old PM-local util files). Update each import to:
        import { ... } from '@/utils/colorUtils'
        import { ... } from '@/utils/factorOrder'
      (or the correct relative path from each file's location; use @/ alias if already used
      in that file, else use relative path).
      Do NOT leave any remaining import pointing to the old PM-local path.
    </requirement>
    <requirement id="4">
      TSC GATE after extraction:
      After moving both files and updating all imports, run:
        cd portal && bunx tsc -b
      Must pass with zero errors before proceeding to the proxy routes step.
      Commit extraction as a standalone commit separate from the proxy routes commit.
      Commit message format:
        0.3.0_DE_TradingOperations: extract colorUtils + factorOrder to portal/src/utils/ (SSCN_PORTAL-002)
    </requirement>
    <requirement id="5">
      NEW FILE — portal/src/api/endpoints/security-scanner.ts:
      Create this file with three exported async functions using the same apiRequest pattern
      as DataRefresh uses in portal/src/api/portal-proxy.ts (lines 1844–1882).
      Auth: all three use apiRequest (scoped/dev-gated), not publicApiRequest.

      Import the TypeScript interfaces from the SSCN types file once RD creates it; for now,
      type the return values as the raw JSON shape or use 'any' with a TODO comment so tsc
      does not block on missing types. RD creates types.ts — do not duplicate it here.

      Functions:
        export async function getSecurityScannerFactors(): Promise&lt;FactorMetadataResponse&gt;
          Method: GET
          Path: /api/scoped/security-scanner/factors
          S3 backend: opal-data-portal-v2/json/security_scanner/latest/factor_metadata.json

        export async function getUniverseData(universeId: string): Promise&lt;UniverseDataResponse&gt;
          Method: GET
          Path: /api/scoped/security-scanner/universe/${universeId}/data
          S3 backend: .../latest/universes/{universeId}/universe_data.json

        export async function getUniverseScanner(universeId: string): Promise&lt;ScannerDataResponse&gt;
          Method: GET
          Path: /api/scoped/security-scanner/universe/${universeId}/scanner
          S3 backend: .../latest/universes/{universeId}/scanner_data.json

      Also export the universe ID constant map for use by the portal:
        export const UNIVERSE_IDS = {
          sp500:  { label: 'S&amp;P 500',           sourceColumn: 'wt_ivv' },
          r1000:  { label: 'Russell 1000',       sourceColumn: 'wt_iwb' },
          r1000v: { label: 'Russell 1000 Value', sourceColumn: 'wt_iwd' },
          acwx:   { label: 'MSCI ACWI ex-US',    sourceColumn: 'wt_acwx' },
          eafe:   { label: 'MSCI EAFE',           sourceColumn: 'wt_efa' },
          eafev:  { label: 'MSCI EAFE Value',     sourceColumn: 'wt_efv' },
        } as const
        export type UniverseId = keyof typeof UNIVERSE_IDS

      Source: SSCN_DATA_CONTRACT.md Section 4 + Section 6.
    </requirement>
    <requirement id="6">
      TSC GATE after security-scanner.ts:
      Run bunx tsc -b after creating security-scanner.ts. Must pass.
      Commit separately from extraction commit.
      Commit message:
        0.3.0_DE_TradingOperations: add SSCN API endpoint functions (SSCN_PORTAL-001)
    </requirement>
    <requirement id="7">
      APP.TSX PAGE REGISTRATION (MISSED IN ORIGINAL TASK ORDER -- ADDED POST-REVIEW):
      Register SecurityScanner in portal/src/App.tsx. This is DE's responsibility because
      App.tsx is outside RD's page-scoped commit scope. Three changes required:

      1. LAZY IMPORT (after TradeSubmission import):
         const SecurityScanner = lazy(() => import('./pages/SecurityScanner/index').then(m => ({ default: m.SecurityScanner })))

      2. SIDEBAR ENTRY in NAV_SECTIONS tools section, FIRST item (above Portfolio Management):
         { path: '/security-scanner', label: 'Security Scanner', icon: ScanLine, requiresDev: true }
         Also add ScanLine to the lucide-react import block.

      3. ROUTE (before portfolio-management route):
         &lt;Route path="/security-scanner" element={&lt;ProtectedRoute requireDev&gt;&lt;SecurityScanner /&gt;&lt;/ProtectedRoute&gt;} /&gt;

      Without this, the page components exist but are unreachable -- no sidebar link, no route.
      This was specified in the PRD (route: /security-scanner, sidebar: Tools above PM,
      icon: ScanLine, requiresDev: true) but was not captured in any task order.

      NOTE: This was caught during CTO review and fixed directly. If this task order was
      already marked complete before this addendum, DE should verify the fix is committed.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">portal/src/utils/colorUtils.ts exists with identical exports to the former PM-local file.</criterion>
    <criterion id="2">portal/src/utils/factorOrder.ts exists with identical exports to the former PM-local file.</criterion>
    <criterion id="3">portal/src/pages/PortfolioManagement/utils/colorUtils.ts and factorOrder.ts are deleted (no PM-local copies remain).</criterion>
    <criterion id="4">All PortfolioManagement files import from the shared path. Zero remaining imports from the old PM-local path (grep confirms).</criterion>
    <criterion id="5">bunx tsc -b passes after extraction commit and after proxy routes commit.</criterion>
    <criterion id="6">portal/src/api/endpoints/security-scanner.ts exists with 3 exported functions + UNIVERSE_IDS constant.</criterion>
    <criterion id="7">Two commits produced: one for extraction, one for the endpoint file.</criterion>
    <criterion id="8">SecurityScanner appears in App.tsx: lazy import, NAV_SECTIONS sidebar entry (Tools, above PM, ScanLine icon, requiresDev), and Route with ProtectedRoute requireDev.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify the function signatures or logic inside colorUtils.ts or factorOrder.ts — move verbatim. SSCN will import from the shared path from day 1 (SSCN_PORTAL-002 decision).</constraint>
    <constraint>Do not create portal/src/pages/SecurityScanner/ — that is RD's scope (0.3.4_RD_SecurityScanner).</constraint>
    <constraint>Do not add portal-proxy.ts route handlers — the apiRequest functions in security-scanner.ts call the API Gateway routes directly. Portal-proxy handles server-side proxying; the endpoint file is the client-side call layer.</constraint>
    <constraint>DE cannot push — signal 0.3.0_DT_TradingOperations to push when both commits are ready.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.4_RD_SecurityScanner" task="SSCN_PORTAL.001-002.page-implementation.md" status="pending">
      RD will create portal/src/pages/SecurityScanner/types.ts with the TypeScript interfaces
      (FactorMetadataResponse, UniverseDataResponse, ScannerDataResponse). DE's endpoint file
      should import from that types file once it exists; for now, type with inline shapes or any.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">portal DEV commit: extraction (colorUtils + factorOrder to portal/src/utils/)</deliverable>
    <deliverable type="commit">portal DEV commit: portal/src/api/endpoints/security-scanner.ts</deliverable>
    <deliverable type="log">Session log at org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-05/</deliverable>
  </deliverables>
</task_order>
```
