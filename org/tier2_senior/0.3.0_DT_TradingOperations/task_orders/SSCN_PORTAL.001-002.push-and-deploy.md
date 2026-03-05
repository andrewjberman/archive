# Task Order: SSCN — Push and Deploy Coordination

```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-05-sscn-push-and-deploy</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-03-05</date>
    <status>pending</status>
    <thread_serial>SSCN_PORTAL-001</thread_serial>
  </metadata>

  <objective>
    DT is the QA gate and push authority for all SSCN portal work. Three push events are
    expected across the SSCN build-out: (1) DE's shared utils extraction + API endpoint file,
    (2) RD's SecurityScanner page implementation, and (3) coordination with AE on Terraform
    deploy timing so portal routes and backend Lambda are live together.
  </objective>

  <scope>
    <files>
      <!-- Push wave 1 (DE extraction) -->
      <file action="review">portal/src/utils/colorUtils.ts</file>
      <file action="review">portal/src/utils/factorOrder.ts</file>
      <file action="review">portal/src/api/endpoints/security-scanner.ts</file>
      <file action="review">portal/src/pages/PortfolioManagement/**/*.tsx (import path updates)</file>
      <!-- Push wave 2 (RD implementation) -->
      <file action="review">portal/src/pages/SecurityScanner/**</file>
      <!-- Update deployment_map.xml after deploy -->
      <file action="modify">org/tier2_senior/0.3.0_DT_TradingOperations/deliverables/deployment_map.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      READ BEFORE STARTING:
      - docs/architecture/SSCN_DESIGN_CONTRACT.md — this is the SoT for what correct SSCN
        frontend implementation looks like. Use it as your QA checklist when reviewing DE
        and RD commits before push. Sections to focus on:
          Section 3A: verify SSCN only imports from shared paths (not PM-local)
          Section 3B: verify PM-local util files are deleted after extraction
          Section 4: verify AG Grid in Tabs 2+4, HTML tables in Tabs 1+3
          Section 5: verify gradient formula (p - 50, -50, 50) in Tab 4
          Section 6: verify Tab 4 default column order and raw-value toggle placement
          Section 8: verify page shell composition order matches the contracted JSX tree
          Section 10: verify DESIGN_SPEC.md committed before any .tsx (gate)
      - docs/architecture/SSCN_DATA_CONTRACT.md — data shapes and API paths; use to verify
        endpoint function signatures in security-scanner.ts match the contracted paths
      - org/ref/LAMBDA_DEPLOYMENT_PROTOCOL.md
      - org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-05/ (DE session log)
      - org/tier3_junior/0.3.4_RD_SecurityScanner/logs/ (latest RD session log — signals readiness)
      - org/tier2_senior/0.5.0_AE_OpalETL/logs/ (latest AE session log — Terraform status)
    </requirement>
    <requirement id="2">
      PUSH WAVE 1 — DE extraction (unblocks RD; execute as soon as DE signals complete):
      Review commits:
        1. Extraction commit: portal/src/utils/colorUtils.ts + factorOrder.ts created;
           portal/src/pages/PortfolioManagement/utils/colorUtils.ts + factorOrder.ts deleted;
           all PM import paths updated.
        2. Endpoint commit: portal/src/api/endpoints/security-scanner.ts created.

      QA checks before push:
        - Grep: confirm no remaining import from 'PortfolioManagement/utils/colorUtils'
          or 'PortfolioManagement/utils/factorOrder' anywhere in the portal source.
        - Run bunx tsc -b from portal/ — must pass.
        - Spot-check ModelTab.tsx and PortfolioGrid.tsx to confirm gradient imports resolve.

      Push: git push on portal submodule DEV branch.
      DT is responsible for this push; DE cannot push (AGENT_START_HERE.md abilities table).
    </requirement>
    <requirement id="3">
      PUSH WAVE 2 — RD implementation (after RD signals complete):
      Review commits from 0.3.4_RD_SecurityScanner covering:
        portal/src/pages/SecurityScanner/ (all files)

      QA checks before push (use SSCN_DESIGN_CONTRACT.md as the review checklist):
        - Run bunx tsc -b from portal/ — must pass.
        - Section 3A: SSCN imports PageHeaderCleanBadge, TabNavigation, Panel etc. from shared paths.
        - Section 3B: no imports from portal/src/pages/PortfolioManagement/utils/ anywhere.
        - Section 4: AG Grid in UniverseDataTab + UniverseScannerTab. HTML tables in FactorBankTab + FactorDataTab.
        - Section 5: gradient formula in UniverseScannerTab uses getGradientBackground(p - 50, -50, 50, false).
        - Section 6: Tab 4 raw-value columns at far right (not interleaved with percentile columns).
        - Section 8: SecurityScanner.tsx composition order matches contracted JSX tree (ScanLine icon, Dev badge).
        - Section 10: DESIGN_SPEC.md committed and approved by DE before any .tsx file was written.
        - Verify ScannerHeaderPanel renders without crashing when no factors are selected.
        - Verify page renders gracefully in loading/error state (data may not yet exist in S3).

      Push: git push on portal submodule DEV branch after QA passes.
    </requirement>
    <requirement id="4">
      DEPLOYMENT COORDINATION WITH AE:
      Monitor org/tier2_senior/0.5.0_AE_OpalETL/logs/ for AE's session log confirming:
        - opal-security-scanner-processor Lambda is live
        - S3 event notification is active on opal-data-portal-v2/security_scanner/uploads/
        - Presign route is deployed in opal-data-refresh-api (or new opal-security-scanner-api)

      Once AE signals Terraform complete, verify end-to-end:
        - The presign upload route responds (test with a curl or portal dev flow)
        - Uploading a test Excel to the S3 prefix triggers the Lambda (check CloudWatch logs)
        - JSON artifacts appear in opal-data-portal-v2/json/security_scanner/latest/

      DT does not own AE's deployment steps; DT's role here is validation and signaling to DE.
    </requirement>
    <requirement id="5">
      UPDATE DEPLOYMENT MAP:
      After both push waves are complete and AE has deployed:
      Update org/tier2_senior/0.3.0_DT_TradingOperations/deliverables/deployment_map.xml
      to add the SSCN portal page entry:
        Page: SecurityScanner
        DEV commit range: [first RD commit]..[last RD commit]
        Portal path: portal/src/pages/SecurityScanner/
        Shared utils: portal/src/utils/colorUtils.ts, portal/src/utils/factorOrder.ts
        API endpoint file: portal/src/api/endpoints/security-scanner.ts
        Backend Lambda: opal-security-scanner-processor (owned by AE)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Wave 1 pushed: portal DEV contains portal/src/utils/colorUtils.ts + factorOrder.ts + security-scanner.ts, and PM-local util files are deleted. bunx tsc -b passes on pushed state.</criterion>
    <criterion id="2">Wave 2 pushed: portal DEV contains portal/src/pages/SecurityScanner/** complete. bunx tsc -b passes.</criterion>
    <criterion id="3">No imports from PortfolioManagement/utils/ anywhere in the portal source (grep confirmed before push).</criterion>
    <criterion id="4">deployment_map.xml updated with SSCN page entry.</criterion>
    <criterion id="5">DT session log documents both push events with commit hashes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not push until bunx tsc -b passes. TypeScript errors are a hard blocker for push.</constraint>
    <constraint>Push wave 1 first (DE extraction) before wave 2 (RD). RD's implementation depends on the shared utils being in portal/src/utils/ on the remote branch.</constraint>
    <constraint>DT does not deploy AWS resources — that is AE's scope. DT validates that the portal side is correct and signals DE if AE deployment reveals a contract mismatch.</constraint>
    <constraint>Do not merge portal DEV to PROD until both waves are pushed, AE Lambda is live, and DE has confirmed the end-to-end data flow with real data.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.0_DE_TradingOperations" task="SSCN_PORTAL.001-002.shared-utils-extraction-proxy-routes.md" status="pending">
      Wave 1 push requires DE extraction commits to be ready.
    </dependency>
    <dependency agent="0.3.4_RD_SecurityScanner" task="SSCN_PORTAL.001-002.page-implementation.md" status="pending">
      Wave 2 push requires RD implementation commits to be ready.
    </dependency>
    <dependency agent="0.5.0_AE_OpalETL" task="SSCN_PORTAL.001-002.terraform-infra.md" status="pending">
      End-to-end validation requires AE's Lambda + S3 trigger + presign route to be deployed.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">portal DEV push — wave 1 (DE extraction)</deliverable>
    <deliverable type="commit">portal DEV push — wave 2 (RD implementation)</deliverable>
    <deliverable type="document">deployment_map.xml updated with SSCN entry</deliverable>
    <deliverable type="log">Session log with both push event commit hashes at org/tier2_senior/0.3.0_DT_TradingOperations/logs/</deliverable>
  </deliverables>
</task_order>
```
