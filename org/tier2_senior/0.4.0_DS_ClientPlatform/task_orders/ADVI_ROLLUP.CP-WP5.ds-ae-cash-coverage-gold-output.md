<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-WP5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date><!-- RESCOPED 2026-04-22 per Andrew directive (see <decision_authority>); original 2026-04-17 cash-aggregator scope superseded -->
    <status>complete</status><!-- RAVC4-closed 2026-04-22 by 2.0.0_SA_COO. Evidence: commit 296b778e (D_04 + lib/s3_layout.py + gold_validate_config.yaml), S3 3 files MATCH via comp-pipescript deployed, comp-validate exit 0 (5 PASS / 0 ERROR / 2 WARN scalar-path type-mismatch benign), firm_cash_aggregate $34,323,539.33 matches silver/allocations headline within $0.33 (AC #2), per_account row count 6,543 = silver row count (AC #3), cash_bearing_account_count 5,922, comp-platinum reverse cash_coverage_summary → 0 consumers (AC #5 Phase 1+3 stable), zero changes to B_01/B_01b/C_02-C_08/D_02 (AC #6 confirmed), 8 emitted fields exceed 4-min (AC #1). AC #7 session log Compiler Tools reproduction pending — DS will ship as end-of-day log (documentation lag, not gate). -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P1 — D-tier emit, independent of CP-VETO-AUTH (which closed as superseded)</priority>
    <decision_authority>Andrew 2026-04-22 verbatim: "I don't think we have a reliable way to track excess cash, all we can do for that is get it in summary metrics in aggregate and per account via silver/allocations/ and have D_04 prepare that info in a table output and then we can choose what we do from that downstream in the portal."</decision_authority>
    <supersedes_prior_scope>Original CP-WP5 scope (2026-04-17) was cash aggregator script with two adjudicated options (a) cash rows in B_01.holdings_lots vs (b) separate cash aggregator script. Both options assumed lot-level cash tracking. CTO 20260422T193424Z called Option (b) with (a') middle-path. ALL OF THAT IS SUPERSEDED 2026-04-22 by Andrew's "no reliable lot-level cash tracking" call. New scope is D-tier summary emission only.</supersedes_prior_scope>
  </metadata>

  <references>
    <ref type="andrew_directive">2026-04-22 chat verbatim above (decision_authority field)</ref>
    <ref type="superseded_cto_adjudication">CTO MCP 20260422T193424Z (Option b cash aggregator) — moot post-Andrew rescope; CTO FYI'd 20260422T193825Z</ref>
    <ref type="related_complete">ADVI_ROLLUP.CP-VETO-AUTH (closed as superseded by CP-DS1 PIVOT 2 + PIVOT 5 + silver-cap absorption; today's gap -0.004%)</ref>
    <ref type="downstream_decision_pending">Portal display of cash table — deferred to a future DE TO; out of scope here</ref>
  </references>

  <objective>
    D-tier emit a cash-coverage summary table sourced from `silver/allocations/{date}.parquet`. Per-account cash dollar amounts + firm-level aggregate. Output as a JSON artifact under `gold/platinum/firm/` (DS picks final key in Phase 0). Portal consumption is deferred — this TO ships the data only.

    EXPLICIT SCOPE LOCK:
    - NO B_01 changes (no cash rows in holdings_lots, no two-artifact split)
    - NO new cash aggregator script
    - NO lot-level cash representation anywhere in the gold chain
    - NO portal display work (future DE TO)
    - Source authority: silver/allocations/ cash field ONLY (the same field that contributes the $34.3M headline cash on the 2026-04-15 partition)
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — add cash-coverage summary computation + emit (DS may instead pick D_00 or D_00b at Phase 0 if better fit; document choice)</file>
      <file action="modify">data/black_diamond/scripts/gold/lib/s3_layout.py — register the new artifact key</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add validator block (field presence + non-zero firm aggregate + per-account count matches silver/allocations cash row count)</file>
      <file action="read-only">data/black_diamond/scripts/silver/*.py (for understanding cash field provenance in silver/allocations)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="emission-design">
      DS picks the D-tier script (D_04 / D_00 / D_00b — your call, document at Phase 0). Read silver/allocations/{date}.parquet, extract per-account cash dollar amount + firm aggregate. Emit as JSON to `gold/platinum/firm/cash_coverage_summary.json` (or alternate key — your call).
    </deliverable>
    <deliverable id="schema-shape">
      Output shape (minimum):
      - `firm_cash_aggregate` (float): sum of cash across all 6,543 accounts (target: ~$34.3M for 2026-04-15)
      - `per_account` (array of `{account_id, cash}`): one row per account in silver/allocations
      - `source_date` (date): silver/allocations partition date used
      - `account_count` (int): row count for sanity check
      DS may extend; minimum is non-negotiable.
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml block:
      - field-presence checks on the 4 minimum fields
      - firm_cash_aggregate > $0 + within reasonable range ($10M-$100M sanity band)
      - account_count matches silver/allocations cash-bearing row count (or flagged as expected delta)
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">`gold/platinum/firm/cash_coverage_summary.json` (or DS-chosen key) emitted nightly with the 4 minimum fields.</ac>
    <ac id="2">`firm_cash_aggregate` matches silver/allocations cash sum within $10K (rounding/timing tolerance).</ac>
    <ac id="3">`per_account` row count = silver/allocations cash-bearing account count, OR documented delta with explanation.</ac>
    <ac id="4">`comp-validate D_04 --artifact /tmp/cash_coverage_summary.json` exits 0.</ac>
    <ac id="5">`comp-platinum reverse cash_coverage_summary` (or chosen field) at Phase 1 — enumerate any portal consumer that would break on null/new value (currently expected 0).</ac>
    <ac id="6">Zero changes to B_01, B_01b, C_02-C_08, or D_02 outputs (no upstream / sibling regression).</ac>
    <ac id="7">Session log Compiler Tools section reproduces each `<run>` + observed + pass/fail vs. `<expect>`.</ac>
    <ac id="8">MCP COMPLETE to COO with commit hash + firm aggregate figure + account count.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_04.client_portal_summary</run>
        <expect>Confirm silver/allocations is already a read source for D_04 (or document if a new read needs adding).</expect>
        <if_mismatch>If silver/allocations is not a current D_04 read, add the read in this TO with explicit comp-pipescript io re-run post-edit confirming the new source is registered.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse cash_coverage_summary</run>
        <expect>0 portal consumers (this is a new emit; no existing readers).</expect>
        <if_mismatch>If any consumer surfaces, that means the key already exists upstream — pick a different key name or coordinate with that consumer before emitting.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_04.client_portal_summary</run>
        <expect>Enumerate downstream consumers — any reader that schema-checks D_04 output needs awareness of the new key.</expect>
        <if_mismatch>If any reader has a strict schema validator that would reject the new key, coordinate before ship.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate D_04 --artifact /tmp/cash_coverage_summary.json</run>
        <expect>Exit 0; new validator block (added in this TO) passes.</expect>
        <if_mismatch>Iterate validator config or fix data shape until exit 0.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>No errors — required by CLAUDE.md Rule 14 ds-commit-gate.</expect>
        <if_mismatch>Fix syntax errors before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/lib/s3_layout.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0 — py_compile + AST undefined-name scan clean.</expect>
        <if_mismatch>Fix flagged issues before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed D_04.client_portal_summary</run>
        <expect>MATCH (after S3 upload).</expect>
        <if_mismatch>STALE = upload didn't propagate; re-upload + verify.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse cash_coverage_summary</run>
        <expect>Same result as Phase 1 (still 0 consumers); confirms emit didn't accidentally activate a portal path.</expect>
        <if_mismatch>If consumers appear post-emit, that's a portal-side change you didn't make — flag to COO/CTO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/D_04.client_portal_summary.py">
      Last-write owner: 0.4.0_DS_ClientPlatform (multiple). STAUDT.COHORT-A (DS data artifact already shipped 3cf43c26 — `cohort_a_summary.json` emit). Coordinate so CP-WP5 emit doesn't conflict with COHORT-A's emission block. Both are independent emits; should be additive.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/gold/lib/s3_layout.py">
      Centralized key registry — single-line addition. Low conflict risk.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/gold/gold_validate_config.yaml">
      Centralized validator config — additive block. Low conflict risk.
    </shared_resource>
    <downstream_pending>Portal display of cash table — future DE TO, NOT in this scope. Andrew explicitly: "we can choose what we do from that downstream in the portal."</downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT modify B_01.holdings_lots.py, B_01b, or any C-tier script. This is D-tier only.</rule>
    <rule>Do NOT introduce a lot-level cash representation anywhere. Per Andrew: no reliable lot-level cash tracking.</rule>
    <rule>Do NOT author portal display code in this TO. Future DE TO scope.</rule>
    <rule>Do NOT use any cash source other than silver/allocations/{date}.parquet. Schwab cash, FIFO-derived cash, RPS cash are all OUT.</rule>
    <rule>Do NOT block on CP-VETO-AUTH (now closed as superseded) — this TO is independent.</rule>
  </do_not>
</task_order>
