# Task Order: Security Scanner Data Contract — SSCN_PORTAL-001

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-05-sscn-data-contract</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-05</date>
    <project>SSCN_PORTAL</project>
    <thread>SSCN_PORTAL-001</thread>
    <status>complete</status>
  </metadata>

  <references>
    <ref type="thread">org/threads/SSCN_PORTAL-001-pattern-0-security-scanner-data-architec/</ref>
    <ref type="thread-receipt">org/tier2_senior/0.3.0_DE_TradingOperations/threads/SSCN_PORTAL-001-pattern-0-security-scanner-data-architec_0.3.0_DS_TradingOperations+0.5.0_AE_OpalETL.md</ref>
    <ref type="prd">docs/architecture/SECURITY_SCANNER_PRD.md</ref>
    <ref type="ds-data-contract">org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml</ref>
  </references>

  <objective>
    Produce the standalone SSCN_PORTAL data contract that the COO requested as DE's
    final thread deliverable in SSCN_PORTAL-001 (turn 000, line 65-100). The thread
    converged (DS turn 7, AE turn 8) but DE's third turn never fired. This task order
    fulfills that gap.

    The data contract is the authoritative interface specification that DS uses to build
    the processing Lambda output, AE uses to provision S3 keys and API routes, and RD
    (0.3.4_RD_SecurityScanner) uses to wire TypeScript fetch calls and type definitions.
  </objective>

  <scope>
    <files>
      <file action="create">docs/architecture/SSCN_DATA_CONTRACT.md</file>
      <file action="modify">org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read your thread receipt:
        org/tier2_senior/0.3.0_DE_TradingOperations/threads/SSCN_PORTAL-001-pattern-0-security-scanner-data-architec_0.3.0_DS_TradingOperations+0.5.0_AE_OpalETL.md

      This contains all 9 turns (COO opening + 8 agent turns). The converged decisions
      are summarized in AE turn 8 (lines 952-1061 of the receipt). Your own turn 3
      (lines 462-633) proposed the JSON shapes that DS and AE accepted.
    </requirement>

    <requirement id="2">
      Create docs/architecture/SSCN_DATA_CONTRACT.md with the following sections.
      Every field, key, and path must be anchored to the thread turn that agreed it.

      Section 1: Header
        - Project: SSCN_PORTAL
        - Thread: SSCN_PORTAL-001
        - Participants: DS (0.3.0), AE (0.5.0), DE (0.3.0)
        - Date: 2026-03-05
        - Status: Contracted

      Section 2: Architecture Summary (one paragraph)
        - Monthly precompute: processing Lambda reads FactSet Excel, computes per-factor
          percentiles server-side using V0 canonical logic (calculate_percentiles_with_sign),
          writes static JSON to S3.
        - Client computes composite score + rank from percentiles and user weights.
        - Portal reads JSON via portal-proxy (no bespoke read Lambda, Phase 0).

      Section 3: S3 Key Structure
        Bucket: opal-data-portal-v2

        Upload (input):
          security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx

        Processed outputs:
          json/security_scanner/{asOf}/factor_metadata.json
          json/security_scanner/{asOf}/universes/{universeId}/universe_data.json
          json/security_scanner/{asOf}/universes/{universeId}/scanner_data.json

        Latest pointers (portal default reads):
          json/security_scanner/latest/factor_metadata.json
          json/security_scanner/latest/universes/{universeId}/universe_data.json
          json/security_scanner/latest/universes/{universeId}/scanner_data.json

        Source: AE turn 2 (002.md) + AE turn 8 (008.md)

      Section 4: API Endpoints (3 routes)

        Endpoint 1: GET /api/scoped/security-scanner/factors
          Auth: scoped (dev-gated, JWT Dev claim)
          S3 read: .../latest/factor_metadata.json
          Response shape: { asOf: string, factors: FactorDefinition[] }

        Endpoint 2: GET /api/scoped/security-scanner/universe/{universeId}/data
          Auth: scoped
          S3 read: .../latest/universes/{universeId}/universe_data.json
          Response shape: { asOf: string, universeId: string, sourceUniverseColumn: string, securities: UniverseDataRow[] }

        Endpoint 3: GET /api/scoped/security-scanner/universe/{universeId}/scanner
          Auth: scoped
          S3 read: .../latest/universes/{universeId}/scanner_data.json
          Response shape: { asOf: string, universeId: string, sourceUniverseColumn: string, rows: ScannerRow[] }

        Source: DE turn 3 (003.md) + AE turn 8 (008.md)

      Section 5: TypeScript Interfaces
        Define these interfaces with exact field names matching the JSON keys agreed
        in the thread. Place them in portal/src/pages/SecurityScanner/types.ts when
        RD implements.

        FactorDefinition:
          code: string
          name: string
          category: string
          relationship: 'Positive' | 'Inverse'
          ic: number
          coveragePct: number
          autocorrelationPct: number
          assetClass: string
          systematic: 'Yes' | 'No'
          Source: DS turn 1 (001.md) + DE turn 3 (003.md)

        UniverseDataRow:
          ticker: string
          name: string
          mktVal: number
          country: string | null      (null for US-only universes)
          sector: string
          industryGroup: string
          universeWeight: number
          values: Record&lt;string, number | null&gt;
          Source: DE turn 3 (003.md)

        ScannerRow:
          ticker: string
          name: string
          mktVal: number
          country: string | null
          sector: string
          industryGroup: string
          values: Record&lt;string, number | null&gt;
          pctls: Record&lt;string, number | null&gt;
          Source: DE turn 3 (003.md), confirmed DS turn 7 (007.md)

        Client-computed (not in JSON):
          compositeScore: number | null   (sum(pctls[code] * weight[code]) / 100, skip nulls)
          rank: number                    (sort order by compositeScore desc, nulls bottom)

      Section 6: Universe ID Mapping

        | Portal ID | Source Column | Universe Name |
        |-----------|-------------- |---------------|
        | sp500     | wt_ivv        | S&amp;P 500           |
        | r1000     | wt_iwb        | Russell 1000       |
        | r1000v    | wt_iwd        | Russell 1000 Value |
        | acwx      | wt_acwx       | MSCI ACWI ex-US    |
        | eafe      | wt_efa        | MSCI EAFE          |
        | eafev     | wt_efv        | MSCI EAFE Value    |

        Source: DE turn 3 (003.md), anchored to UNIVERSE_OPTIONS in quick_update_weights.py

      Section 7: Null Semantics
        - Missing raw value: values[code] = null
        - Missing percentile: pctls[code] = null
        - Composite: skip null pctls; if all selected factors are null, composite = null, sorts bottom
        Source: DS turn 4 (004.md), confirmed DS turn 7 (007.md)

      Section 8: Compute Split
        Server-side (processing Lambda, monthly):
          - Per-factor percentiles using rank(pct=True, method='average') * 100
          - Sign inversion for Inverse-relationship factors (negate before ranking)
          - Source: calculate_percentiles_with_sign() in quick_update_weights.py

        Client-side (browser, on every weight change):
          - compositeScore = sum(pctls[code] * weight[code]) / 100
          - rank = sort order by compositeScore descending
          - Source: mirrors XLSM Tab 4 formula D30 + VBA Worksheet_Calculate auto-sort

      Section 9: Refresh + Upload
        - Manual upload via presigned PUT URL (DataRefresh-style, scoped endpoint)
        - S3 event triggers processing Lambda
        - Presign endpoint: extend existing opal-data-refresh-api (preferred) or new Lambda
        - Source: AE turn 5 (005.md), DE turn 6 (006.md)

      Section 10: Open Items
        - "Exact Excel header names" -- V0 script references ticker, mkt_val, country_name,
          sector_name, indgrp_name; 255 factor codes from XLSM Tab 3 are column names in the
          data sheet. Processor normalizes to canonical JSON keys regardless. Resolution:
          provide repo path to FactSet export or check in a header snapshot artifact.
          Source: DS turn 7 (007.md), AE turn 8 (008.md)
        - Phase 0: no gzip, no CloudFront invalidation. Versioned {asOf} paths for cache-busting.
          Source: AE turn 8 (008.md)
    </requirement>

    <requirement id="3">
      Update org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml
      to add a Security Scanner section referencing the new contract document:
        - Source: SSCN_PORTAL-001 thread
        - Contract path: docs/architecture/SSCN_DATA_CONTRACT.md
        - Status: contracted
    </requirement>

    <requirement id="4">
      The contract document must be self-contained. A reader who has never seen the thread
      must be able to understand every API endpoint, JSON shape, S3 key, and TypeScript
      interface from this document alone. Do not use phrases like "as discussed" or
      "per the thread" without also stating the actual value.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">docs/architecture/SSCN_DATA_CONTRACT.md exists with all 10 sections.</criterion>
    <criterion id="2">Every S3 key, API route, and JSON field name in the contract matches what was agreed in the thread (cross-check against AE turn 8 and DE turn 3).</criterion>
    <criterion id="3">TypeScript interface definitions include exact field names and types (not pseudocode).</criterion>
    <criterion id="4">Universe ID mapping table has all 6 entries with portal ID, source column, and display name.</criterion>
    <criterion id="5">Null semantics section is explicit about composite behavior when all selected factors are null.</criterion>
    <criterion id="6">Open items section documents the Excel headers gap with the two resolution paths DS proposed.</criterion>
    <criterion id="7">DS data_contract.xml updated with SSCN reference.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not invent fields, routes, or shapes that were not agreed in the thread. If something is ambiguous, note it in Open Items rather than guessing.</constraint>
    <constraint>Do not write any portal code. This task order produces documentation only.</constraint>
    <constraint>Use camelCase for JSON field names (mktVal, coveragePct, industryGroup) -- this was the convention DE established in turn 3.</constraint>
    <constraint>Thread turn citations are required for traceability. Each section must name the turn(s) that established the decision.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">docs/architecture/SSCN_DATA_CONTRACT.md -- standalone data contract</deliverable>
    <deliverable type="document">Updated DS data_contract.xml with SSCN reference</deliverable>
    <deliverable type="log">Session log at org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-05/</deliverable>
  </deliverables>
</task_order>
```
