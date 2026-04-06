<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-02-gldrst-018-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-02</date>
    <status>staged</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Wire the new `market_growth` and `synthetic_correction` fields from
    `client_performance.parquet` into the portal's advisor intelligence
    pages. Display the AUA decomposition (NNA vs market growth vs synthetic
    correction) wherever AUA changes are shown.
  </objective>

  <context>
    DS .017 adds two new columns to `client_performance.parquet`:
    - `market_growth`: day-over-day market appreciation (ex-NNA, ex-synthetic)
    - `synthetic_correction`: day-over-day change in synthetic injection AUA

    The decomposition identity: `delta(total_aua) = nna + market_growth + synthetic_correction`

    These fields need to flow through the publisher Lambda to the portal.
    The exact portal surfaces and component layout depend on what .017 delivers.
    This TO is intentionally held until .017 is complete so the wiring matches
    the actual schema.

    PRD: docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md (Work Stream C)
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/types.ts (add market_growth, synthetic_correction to relevant interfaces)</file>
      <file action="modify">Publisher Lambda query/S3 read path (if schema mapping needed)</file>
      <file action="modify">Portal components displaying AUA/NNA (Books tab, advisor drill, firm overview)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add `market_growth` and `synthetic_correction` to the TypeScript interface
      used by the client performance data. Use `number | null` typing (null when
      synthetic_positions_index.parquet was absent during the gold run).
    </requirement>

    <requirement id="2">
      Update the publisher Lambda (or S3 artifact generation) to include the
      new fields in the JSON output consumed by the portal. Coordinate with
      DT for deploy if Lambda changes are needed.
    </requirement>

    <requirement id="3">
      Display the decomposition in portal surfaces where AUA delta is shown.
      The synthetic_correction line should be labeled "AUA Reconciliation"
      (not "Synthetic Correction") per Andrew's approved naming.
    </requirement>

    <requirement id="4">
      Handle null/missing gracefully -- if market_growth is null (older data
      before .017 ran), hide the decomposition row rather than showing 0.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">TypeScript interfaces include market_growth and synthetic_correction</criterion>
    <criterion id="2">Portal renders AUA decomposition breakdown on at least one surface</criterion>
    <criterion id="3">Null handling: decomposition hidden when fields are absent</criterion>
    <criterion id="4">`bunx tsc -b` passes with no type errors</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start until .017 is COMPLETE and the output schema is confirmed</constraint>
    <constraint>Label "AUA Reconciliation" not "Synthetic Correction" in the UI</constraint>
    <constraint>This is a portal-only change -- do not modify gold scripts</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_GLDRST.017"
                status="staged">
      .017 must deliver the new schema before DE can wire it.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">TypeScript interface updates + component wiring</deliverable>
    <deliverable type="log">Session log with screenshots or test evidence</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md</ref>
    <ref type="depends-on">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_GLDRST.017.ds-nna-market-growth-rearchitecture.md</ref>
  </references>
</task_order>
