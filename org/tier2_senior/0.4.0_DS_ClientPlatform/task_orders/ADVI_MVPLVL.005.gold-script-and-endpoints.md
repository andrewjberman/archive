<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-16-005-ds-gold-endpoints</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-16</date>
    <status>complete</status>
    <thread_serial>ADVI_MVPLVL-005</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment/</thread_ref>
  </metadata>

  <objective>
    Write the 06b gold script that produces historical Mix and Concentration timeseries
    artifacts, then add two Lambda endpoints to opal-partners-data that serve the data
    to the portal. This is Addendum A of the ADVI_MVPLVL PRD.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create `06b_build_client_mix_timeseries.py`. Same join pattern as 05b: positions_cube x
      canonical_prices x accounts_dimension, ThreadPoolExecutor parallelism. Two output artifacts
      in a single pass per date partition:
        - `gold/client_mix_timeseries.parquet`: (date, relationship_id, asset_class, market_value, pct)
        - `gold/client_concentration_timeseries.parquet`: (date, relationship_id, asset_name, ticker, asset_class, market_value)
      Asset classes: equity, fixed_income, structured_notes, cash, other.
      Classification via `_classify_holding()` logic (copy the classification dicts into 06b — self-contained, no cross-boundary imports).
    </requirement>
    <requirement id="2">
      AP active gate: exclude account_ids not present in `account_performance` within 45 days
      of the snapshot date. Prevents $371M stale-holdings inflation.
    </requirement>
    <requirement id="3">
      Support `--incremental` flag from day one. Watermark-based: read max(date) in existing
      parquet, process only positions_cube partitions newer than that. First run (no existing
      parquet) falls back to full rebuild automatically.
      CLI: `python3 06b_... --upload` (full) / `python3 06b_... --upload --incremental` (incremental).
    </requirement>
    <requirement id="4">
      Concentration artifact stores ALL holdings per relationship per date (unbounded).
      Top-N filtering happens at Lambda layer, not at gold write time. Ticker column is nullable.
    </requirement>
    <requirement id="5">
      Mix pct values MUST sum to 1.0 (±0.001) per (date, relationship_id). Exclude dates
      where partial coverage prevents this. This is a hard gate — AE will validate before
      Lambda deployment proceeds (Gate 2 in thread receipt).
    </requirement>
    <requirement id="6">
      Add mix-timeseries endpoint to opal-partners-data Lambda:
      `GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx&window=1Y`
      Returns wide-format array: [{date, equity, fixed_income, structured_notes, cash, other}]
      as pct values (0-1). Pre-filter to window (1Y/3Y/Max). Exclude partial-coverage dates.
    </requirement>
    <requirement id="7">
      Add concentration-timeseries endpoint to opal-partners-data Lambda:
      `GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx&window=1Y`
      Returns {relationship_id, top_n, data: [{date, asset_name, ticker, asset_class, market_value, pct}]}.
      Top-10 per date at Lambda layer. Ticker nullable (write null, not empty string or synthetic value).
    </requirement>
    <requirement id="8">
      S3 output keys: `s3://opal-data-bd/gold/client_mix_timeseries.parquet` and
      `s3://opal-data-bd/gold/client_concentration_timeseries.parquet`. Single-file parquet,
      NOT Hive-partitioned.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">06b runs locally without error on at least 1 positions_cube date</criterion>
    <criterion id="2">Both output artifacts have correct schema per requirement 1</criterion>
    <criterion id="3">pct sum validation passes (±0.001) for all (date, relationship_id) rows</criterion>
    <criterion id="4">--incremental mode processes only new dates (verified by comparing output before/after)</criterion>
    <criterion id="5">Both Lambda endpoints return correct response shapes per requirements 6-7</criterion>
    <criterion id="6">Lambda endpoints respect window param (1Y/3Y/Max date filtering)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT add account_id column to either artifact — L4 is out of scope for Addendum A</constraint>
    <constraint>Copy classification dicts into 06b (option 1 from PRD) — no cross-boundary imports from Lambda shared code</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
    <constraint>Do NOT deploy — AE deploys 06b to EC2, DT deploys Lambda. DS writes code only.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="complete">
      Classification pipeline (_classify_holding) already built by DS (commit eea3297a).
      Composition endpoints already committed. No upstream blocker.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">06b gold script committed to CLOUD</deliverable>
    <deliverable type="commit">Lambda endpoint code committed to CLOUD</deliverable>
  </deliverables>
</task_order>
