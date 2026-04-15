<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-ra-p0</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P0 (schema + tests)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #7)</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md (authoritative scope)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_post_presentation_master_summary.md (§7)</ref>
    <ref type="cross_domain">ADVI_ROLLUP.CN-P0 + CN-P1 — paired structural convergence (ROLEAUA + CANNNA co-ship shadow artifacts in single D_02 pre-pass commit at P1)</ref>
  </references>

  <objective>
    Phase 0 of 6. Schema design + invariant tests for the canonical `gold/canonical/role_aua/{date}.parquet`
    table that will supersede 6 independent per-advisor/per-role AUA aggregation sites:

      1. D_00c — `_build_at_role_slice` + `tagged_aua_counts` → leaderboard.json
      2. D_02 — `build_advisor_books` role_breakdown L1269 → summary.json + book.json
      3. D_02 — `build_advisor_timeseries` role_ts_lookup L1619 → timeseries.json
      4. D_01 — `build_adv_view` → partner_analytics views.adv
      5. D_00b — `_build_advisor_view` + adv_drill → timeseries_chart.json + cumulative_chart.json
      6. C_08 — scorecard builder → advisor_fee_efficiency.json

    Current state: 3 filter stacks × 3 cutoff conventions × 6 sites = ~0.5% drift visible in
    Travis's architect AUA across consumers. Architect three-way schism generalized.

    Scope of THIS TO (P0 only):
    - Freeze the table schema: one row per `(date, advisor, role)`.
    - Columns: `aua` (equal-split), `aua_tagged_total` (pre-dedup), `aua_fee_paying`, `aua_no_fee`,
      `nna_txn`, `daily_inflow`, `daily_outflow`, plus reconciliation metadata (source_filter_stack,
      ghost_flag, ap_gate, excluded_names_applied).
    - Write the invariant test suite (6 invariants from plan doc) as a standalone validator script
      that `comp-validate role_aua --artifact /tmp/*.parquet` will call.
    - Enumerate all 6 consumer aggregation sites with file:line citations + record in P0 deliverable memo.
    - NO production code change. NO shadow write yet. Zero reader impact.

    P1 (shadow write in D_02 pre-pass, co-ships with CN-P1 in single commit) comes next.
  </objective>

  <wire_contract>
    gold/canonical/role_aua/{date}.parquet (P0 produces schema spec + validator only, no data yet):

    | Column | Type | Notes |
    |---|---|---|
    | date | DATE | partition key |
    | advisor | STRING | pseudonymized slug |
    | role | STRING enum | architect / implementor / consultant / local_ops / additional_advisor |
    | aua | FLOAT | equal-split across roles on multi-role accounts |
    | aua_tagged_total | FLOAT | pre-dedup across roles |
    | aua_fee_paying | FLOAT | fee-bucket split |
    | aua_no_fee | FLOAT | fee-bucket split |
    | nna_txn | FLOAT | from canonical nna_atomic (CN-P1 dependency) |
    | daily_inflow | FLOAT | from canonical nna_atomic |
    | daily_outflow | FLOAT | from canonical nna_atomic |
    | source_filter_stack | STRING | metadata: which filters applied |
    | ghost_flag | BOOL | reconciliation metadata |

    Final column list confirmed by CTO at P0 review; may adjust before P1 shadow write.
  </wire_contract>

  <acceptance_criteria>
    1. Schema spec committed as `docs/data/role_aua_schema.md` (grep-able canonical reference for all 6 consumer owners).
    2. Invariant validator script at `data/black_diamond/scripts/validators/validate_role_aua.py` implementing the 6 invariants from the DS plan doc.
    3. Consumer enumeration memo committed: file:line citations for each of the 6 current aggregation sites plus the per-site filter/cutoff delta analysis.
    4. Cross-domain coordination block acknowledges CN-P1 as co-ship partner (same D_02 pre-pass commit, not this phase).
    5. `comp-validate role_aua --schema` exits 0 (validator wires correctly).
    6. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. **Column list RATIFIED at P0.** No further column additions permitted without a `RA-P0a` addendum TO (CTO lock 2026-04-15). This prevents P1 shadow-write moving-target and protects consumer-reverse work.
    8. MCP COMPLETE to COO with commit hash + memo path + pointer to validator.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast D_00c; comp-blast D_02; comp-blast D_01; comp-blast D_00b; comp-blast C_08</run>
        <expect>All 5 scripts return downstream graphs; confirm 6 aggregation sites still match plan doc. Record blast output per site in P0 memo.</expect>
        <if_mismatch>If a site has moved (function rename, file split), update plan doc reference in P0 memo before writing schema.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse role_aua</run>
        <expect>Empty — role_aua is a NEW platinum field (CTO auto-rule Phase 1 hit). No existing producer or consumer. Matches plan doc expectation.</expect>
        <if_mismatch>If any existing reference found, investigate and reconcile with plan doc — likely a rogue earlier prototype.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate role_aua --schema</run>
        <expect>Validator script syntax clean; invariant count matches plan doc (6 invariants).</expect>
        <if_mismatch>Fix validator wiring before commit.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile data/black_diamond/scripts/validators/validate_role_aua.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast role_aua_schema_doc</run>
        <expect>No consumers yet — schema doc is reference only until P1 produces data.</expect>
        <if_mismatch>If an agent is already importing the schema, coordinate before they ship on un-validated data.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None for P0. P1 will depend on CN-P0 schema stability for the shared `nna_atomic` columns.
  </dependencies>

  <cross_domain_coordination>
    CN-P1 co-ships with RA-P1 in a single DS commit (CTO directive 2026-04-15). Both produce
    shadow artifacts in the D_02 pre-pass. Do not commit RA-P1 alone. RA-P0 and CN-P0 can commit
    independently; they feed the shared P1.
  </cross_domain_coordination>

  <next>
    On P0 complete: ~C signals COO. COO issues RA-P1 TO for shadow write, paired with CN-P1
    authored simultaneously.
  </next>
</task_order>
