```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-13-p4-books-proxy-wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-13</date>
    <status>complete</status><!-- Books proxy routes delivered under BKSCMP (partners-api-v1.5.0+). Project closed 2026-03-20. -->
    <thread_serial>ADVI_MVPLVL-004</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</thread_ref>
  </metadata>

  <objective>
    Wire portal proxy routes and TypeScript types for 4 new Books Tab endpoints
    (timeseries x2 + composition x2) that DS is implementing in opal-partners-data.
    Also implement item 4h (advisor listing UI consistency with leaderboard design
    from 3d) once RD's P3 leaderboard commit is available.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="proxy-routes">
      Add 4 proxy route functions in portal/src/api/endpoints/advisor-intelligence.ts:

      1. getBooksRelationshipTimeseries(relationshipId: string)
         -> GET /api/scoped/partners/books/relationship/{id}/timeseries
      2. getBooksAccountTimeseries(accountId: string)
         -> GET /api/scoped/partners/books/account/{id}/timeseries
      3. getBooksRelationshipComposition(relationshipId: string)
         -> GET /api/scoped/partners/books/relationship/{id}/composition
      4. getBooksAccountComposition(accountId: string)
         -> GET /api/scoped/partners/books/account/{id}/composition
    </requirement>

    <requirement id="types">
      Add TypeScript types in portal/src/pages/AdvisorIntelligence/types.ts:

      BooksTimeseriesResponse:
      - generated_at: string
      - data_as_of: string
      - relationship_id?: string
      - account_id?: string
      - data: BooksTimeseriesPoint[]

      BooksTimeseriesPoint:
      - date: string
      - total_aua: number
      - cum_inflows: number
      - cum_outflows: number
      - nna: number

      BooksCompositionResponse:
      - generated_at: string
      - data_as_of: string
      - scope: { relationship_id?: string, account_id?: string }
      - mix: MixItem[]
      - concentration: { top_n: number, items: ConcentrationItem[], other: { market_value: number, pct: number } }
      - unclassified: { count: number, market_value: number }

      MixItem:
      - asset_class: string  (enum: equity|fixed_income|hedge|cash|other)
      - label: string
      - market_value: number
      - pct: number

      ConcentrationItem:
      - key: string
      - label: string
      - asset_class: string
      - market_value: number
      - pct: number
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 4 proxy functions exist and compile (bunx tsc -b passes)</criterion>
    <criterion id="2">TypeScript types match the DS endpoint contract from thread ADVI_MVPLVL-004</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Commit on portal DEV branch</constraint>
    <constraint>Do not implement UI — RD owns component rendering</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.004.p4-books-backend-endpoints" status="pending">
      Proxy routes point to endpoints DS is implementing
    </dependency>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_MVPLVL_PRD.md (Part 4)</ref>
    <ref type="thread">org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with proxy routes + types</deliverable>
  </deliverables>
</task_order>
```
