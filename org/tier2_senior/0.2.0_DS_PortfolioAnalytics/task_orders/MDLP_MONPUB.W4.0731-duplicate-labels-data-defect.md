<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w4</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-08-03</date>
    <status>pending</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    Root-cause and fix the 2026-07-31 data.pkl duplicate-labels defect (duplicate (tenor, date)
    rows in price_monthly) that loudly failed all four 07-31 executions, then land the corrected
    07-31 upload so the served frontier advances to true T-1.
  </objective>

  <context>
    Spec: docs/architecture/MDLP_MONPUB_MANIFEST_REGRESSION_FIX.md @d59fc15920 section 3 W4.
    Crash: ValueError "cannot reindex on an axis with duplicate labels" -- lambda_function.py:324 ->
    build_rfr_daily -> reindex on the date index filtered by index_name == tenor. Determine one-off
    upload artifact vs producer defect. HARD SEQUENCING: the corrected re-upload runs ONLY after
    W2's guard is LIVE (the guard protects the recovery path).
    DOCTRINE (comp-blast surfaced): memory/reference_yang_datapkl_return_daily_total_return_basis_custom_indices.md
    -- return==price_return on custom .X_BMK indices is NOT price-only; do not "fix" that as a
    duplicate/defect.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before touching data):
      <run>load the 2026-07-31 data.pkl; census the duplicates: which tenor(s), how many dup (tenor,date) rows, print the DENOMINATOR (total price_monthly rows scanned)</run>
      <expect>A concrete census -- e.g. "tenor X: N duplicate date rows of M total". A scan without its denominator is not evidence.</expect>
      <if_mismatch>Zero duplicates found = the 07-31 upload on hand differs from the one that crashed; STOP and reconcile which artifact the executions actually read</if_mismatch>
    Phase 3 (after re-upload):
      <run>verify the reprocess execution SUCCEEDED and serve advanced (head-object + body data_as_of)</run>
      <expect>data_as_of == expected_last_trading_day per lib/trading_calendar.py (the ONE frontier definition -- trading days, never wall-clock)</expect>
      <if_mismatch>Escalate with the execution history; do not hand-edit outputs</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: the yang data.pkl upload path + opal-data-portal-v2/json/benchmarks/*
    also_in_to: MDLP_MONPUB.W2 (guard must be LIVE before this TO's re-upload step)
    required_action: obtain W2-live confirmation before firing the reprocess.
  </cross_domain_coordination>

  <acceptance_criteria>
    0. CONTENT GATE (CTO-added 2026-08-03T1535Z on MSTR~Z's source-confirmed root cause -- BINDING
       regardless of fix path): before ANY corrected 0731 pkl is uploaded, verify its .ST Index
       series reads: inception 2023-12-29, ~676 rows over the request window, price level ~112.5.
       A wrong-instrument re-pull (the 0730 mechanism: terminal-side custom-index resolution
       returning a DIFFERENT instrument's 1449-row history at price ~1.88) BUILDS SUCCESSFULLY and
       PASSES W2's monotonic guard -- the guard cannot see content. ALSO: return_monthly dedup must
       keep the FIELD-BEARING row (168 non-value-identical dups: monthly rows carry valuation
       fields, appended daily rows carry NaNs -- a naive groupby().last() destroys field data);
       price_monthly's 60 dups are value-identical (lossless). Root cause: Yang's
       market_indices_data_pull.ipynb cell 16 double-append on month-end as-of; his OneDrive copy
       gained a guard 2026-08-03T13:08Z but that does NOT heal the uploaded 0731 pkl.
    1. ROOT CAUSE with grounding: producer-defect vs one-off classified, cited file:line @ commit
       (producer case) or a data-level census with denominator (one-off case). INFERRED is
       non-actionable -- "probably a double-append" without a citation fails this criterion.
    2. CORRECTNESS: the corrected 07-31 reprocess completes without the ValueError AND served
       data_as_of advances to the trading-day frontier (not merely "newer than 07-30").
    3. SEQUENCING: evidence W2 was live before the re-upload (guard deploy timestamp vs reprocess
       execution start).
    4. THIRD STATE: if the original crashing 07-31 artifact cannot be retrieved for the census, that
       is CANNOT-VERIFY (a finding, reported), not a silent skip to re-generation.
  </acceptance_criteria>
</task_order>
