<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-bdpl-cnprcs-wp10b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-05-04 via COO GT-recon. Code shipped cff234b5 2026-04-15 (drift test PASS at ship per DS~B session log + this comment); AE wire-up shipped 5700854e6 2026-04-29; 4 consecutive clean nightly runs verified by DS~C (2026-04-29..05-02): all 19 checks consistent, single persistent WARN on aua_totals (delta_pct=None — known structural gap, NOT a regression). AC#1-6 satisfied. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W2</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 2, per CTO split of WP-10)</ref>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-10 harness component)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-14_asset_dim_and_canonical_prices_refactor.md (§WP-10 recon harness)</ref>
  </references>

  <objective>
    Nightly gold↔silver reconciliation harness. Independent diagnostic that emits a manifest
    comparing every gold aggregation against its silver source-of-truth row counts + AUA
    sums + flow totals. Runs post-gold-dispatch, independent of any single script.

    Output: `data/black_diamond/diagnostics/gold_silver_recon_{YYYY-MM-DD}.md` + machine-readable
    `gold_silver_recon_{date}.json` for AE to ingest into alerting.

    Detects drift classes that today slip through: silver row added but gold didn't reprocess,
    gold aggregation dropped rows due to stale join key, canonical tables out of sync with
    silver writes of the same day.
  </objective>

  <wire_contract>
    Output manifest per run:
      {
        date: YYYY-MM-DD,
        checks: [
          {domain: 'holdings_lots', silver_rows: N, gold_rows: M, delta: K, status: 'OK'|'WARN'|'FAIL'},
          {domain: 'canonical_prices', ...},
          {domain: 'canonical_nna', ...},
          ...
        ],
        aua_totals: {silver: X, gold: Y, delta_pct: Z},
        flow_totals: {silver_inflow: ..., gold_inflow: ...}
      }

    No consumer contract — this is diagnostic output. FE does not read.
  </wire_contract>

  <acceptance_criteria>
    1. Harness runs nightly post gold_dispatch; manifest written to S3 diagnostics/ prefix.
    2. Clean run for 3 consecutive nights post-commit.
    3. Deliberate drift test: inject a mismatch in silver test artifact, confirm harness flags FAIL status with correct domain + row count.
    4. `comp-validate` on the harness output schema exits 0.
    5. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    6. MCP COMPLETE to COO with 3-night manifest paths + 1 drift-test confirmation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on every gold-silver join boundary (A_*, B_*, C_*, D_* scripts)</run>
        <expect>Enumerated every domain the harness must check (holdings_lots, canonical_prices, canonical_nna, advisor_fee_detail, account_team, etc.). Record list in session log.</expect>
        <if_mismatch>Surface to COO before writing harness — domain list needs confirmation.</if_mismatch>
      </step>
      <step>
        <run>comp-blast diag_phantom_valuations</run>
        <expect>Confirm existing diagnostic coverage is phantom-only (cost_per_unit vs current_price). WP-10b does NOT duplicate — it's row-count / sum / flow recon across domains, broader than phantom scan.</expect>
        <if_mismatch>If scopes overlap, coordinate with COO before writing duplicate coverage.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile + harness smoke test on local fixtures</run>
        <expect>Exit 0; manifest output schema-validates; deliberate mismatch injection produces FAIL status with correct domain.</expect>
        <if_mismatch>Iterate on harness logic.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast gold_silver_recon_manifest</run>
        <expect>No unintended consumers; harness is write-only diagnostic until AE ingests manifest into alerting.</expect>
        <if_mismatch>Surface to COO if a surprise reader appears.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None (parallel to WP-10). Can ship in either order.
  </dependencies>

  <next>
    Feeds AE alerting pipeline. Hand findings to COO on WARN/FAIL status.
  </next>
</task_order>
