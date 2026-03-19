```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-13-p4-books-backend</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-13</date>
    <status>complete</status>
    <thread_serial>ADVI_MVPLVL-004</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</thread_ref>
  </metadata>

  <objective>
    Implement 4 new dynamic parquet-slice endpoints in the opal-partners-data Lambda
    for Books Tab L3/L4 views: 2 timeseries (relationship + account AUA/NNA) and
    2 composition (relationship + account Mix + Concentration). These endpoints serve
    drill-scoped data that does not exist in any current publisher output.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="4g-timeseries">
      Two timeseries endpoints returning daily AUA/NNA for a single entity.

      Routes (via portal-proxy under scoped namespace):
      - GET /api/scoped/partners/books/relationship/{relationship_id}/timeseries
      - GET /api/scoped/partners/books/account/{account_id}/timeseries

      Data sources:
      - Relationship: s3://opal-data-bd/gold/client_performance.parquet
        Filter: relationship_id == param. Columns: date, total_aua, cum_inflows,
        cum_outflows, nna. Optionally include aua_taxable, aua_tax_deferred,
        aua_tax_exempt if cheap.
      - Account: s3://opal-data-bd/gold/account_performance.parquet
        Filter: account_id == param. Same columns. Optionally include num_positions,
        pct_priced.

      Response shape:
      {
        "generated_at": "ISO",
        "data_as_of": "YYYY-MM-DD",   // max(date) in parquet
        "relationship_id": "...",       // or account_id
        "data": [
          {"date":"YYYY-MM-DD","total_aua":0,"cum_inflows":0,"cum_outflows":0,"nna":0}
        ]
      }

      Guarantees:
      - data_as_of = max(date) in parquet
      - data sorted ascending by date
      - Daily granularity only for MVP (frontend aggregates client-side)
    </requirement>

    <requirement id="4ef-composition">
      Two composition endpoints returning Mix (asset class) + Concentration (security)
      for a single entity, as-of latest holdings snapshot.

      Routes:
      - GET /api/scoped/partners/books/relationship/{relationship_id}/composition
      - GET /api/scoped/partners/books/account/{account_id}/composition

      Data source:
      - Latest holdings_lots snapshot: s3://opal-data-bd/gold/holdings_lots/YYYY-MM-DD.parquet
        (latest key under prefix, skip backfill_*)
      - Filter: is_open == True, then filter by relationship_id or account_id
      - Column prune: account_id, relationship_id, ticker, asset_name, market_value, is_open

      Classification logic:
      1. If ticker present AND in canonical ETF classification
         (infra/aws/lambda/v2_portal/_shared/etf_classification.py) -> use ETF_CLASSIFICATIONS
      2. Else fallback to name-pattern classifier (publisher-style _classify_asset) -> "other"

      Aggregation:
      - Mix: group by asset_class, sum market_value, compute pct. Emit all classes.
      - Concentration: group by ticker (or deterministic asset_name fallback when ticker
        missing), sum market_value, compute pct. Top 10 + Other bucket.

      Response shape:
      {
        "generated_at": "ISO",
        "data_as_of": "YYYY-MM-DD",
        "scope": {"relationship_id":"...","account_id":"..."},
        "mix": [
          {"asset_class":"equity","label":"Equities","market_value":0,"pct":0}
        ],
        "concentration": {
          "top_n": 10,
          "items": [
            {"key":"SPY","label":"SPY","asset_class":"equity","market_value":0,"pct":0}
          ],
          "other": {"market_value":0,"pct":0}
        },
        "unclassified": {"count":0,"market_value":0}
      }

      Key stability requirements (from RD):
      - mix[].asset_class must be stable enum key (equity|fixed_income|hedge|cash|other)
      - concentration.items[].key must be unique (ticker when available, else deterministic
        fallback from asset_name)
    </requirement>

    <requirement id="etf-import">
      Import canonical ETF classification from infra/aws/lambda/v2_portal/_shared/etf_classification.py.
      Use ETF_CLASSIFICATIONS dict for ticker -> asset_class mapping. This is the primary
      classification source; name-pattern fallback is secondary.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Timeseries endpoint returns correct daily AUA/NNA for a known relationship_id</criterion>
    <criterion id="2">Timeseries endpoint returns correct daily AUA/NNA for a known account_id</criterion>
    <criterion id="3">Composition endpoint returns Mix + Concentration with ETF classification for a known relationship_id</criterion>
    <criterion id="4">Composition endpoint returns Mix + Concentration for a known account_id</criterion>
    <criterion id="5">mix[].asset_class uses stable enum keys; concentration.items[].key is unique per item</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Code changes only — do not deploy. DT deploys after DS commits.</constraint>
    <constraint>Do not modify existing opal-partners-data endpoints — add new routes only</constraint>
    <constraint>ETF classification is primary; name-pattern is fallback only</constraint>
    <constraint>L2 (advisor-level) composition is deferred — implement L3/L4 only</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="deploy" status="pending">
      DT deploys updated opal-partners-data Lambda after DS commits
    </dependency>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_MVPLVL_PRD.md (Part 4, items 4e/4f/4g)</ref>
    <ref type="thread">org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</ref>
  </references>

  <deliverables>
    <deliverable type="commit">opal-partners-data Lambda with 4 new routes (timeseries x2 + composition x2)</deliverable>
  </deliverables>
</task_order>
```
