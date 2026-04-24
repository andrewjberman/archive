<task_order>
  <metadata>
    <id>ADVI_ROLLUP.TOPPOSOPAL</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <status>staged</status><!-- GO gated on 49EXEC TO 1+5+ORPHRELID completion OR explicit COO/Andrew override; DE follow-on TO authored separately -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P2 — Top Positions portal widget cost_basis quality gate; not portal-breaking but visibly degraded today</priority>
    <origin>
      ADVI_ROLLUP dashboard blocking item (3): "Top Positions 'Opal models only' filter TO authoring (31.74% cost_basis coverage)". 68% of current BD positions lack cost_basis — Top Positions widget currently shows gain/loss data that is unreliable for the non-Opal-model cohort. Decision: emit an `is_opal_model` flag at gold layer so DE can filter the widget to the cohort with reliable cost_basis. Cleaner than retroactive cost_basis recovery (which is infeasible for some account types).
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Top Positions widget discussion; cost_basis coverage)</ref>
    <ref type="follow-on">DE TO (to be authored separately when this ships): portal filter consumption of `is_opal_model` in Top Positions widget</ref>
    <ref type="data_source">silver/bd_assets_dim or silver/accounts_dimension — source of "is Opal model portfolio account" distinction (Phase 0 confirms authoritative source)</ref>
  </references>

  <objective>
    Emit an `is_opal_model` boolean flag per-account (or per-position, depending on Phase 0 finding) at D-tier (D_04 or D_02 — your call in Phase 0), so the portal Top Positions widget can filter to the 31.74% cohort with reliable cost_basis.

    Phase 0 question to resolve: is "Opal model" a per-account classification (account is in an Opal-managed model portfolio) or per-position (this specific holding came through an Opal model trade)? Authoritative source likely `silver/accounts_dimension` (managed-account flag) or a naming convention in the account_type field. If the distinction is ambiguous, surface to Andrew — we cannot guess.

    Output: new field `is_opal_model` in the chosen D-tier artifact. DE follow-on TO wires the portal filter.

    **EXPLICIT SCOPE LOCK:**
    - NO portal work (DE follow-on TO)
    - NO backfill (forward-deploy; portal will show filtered counts from day one)
    - NO changes to existing Top Positions emit content (additive flag only)
  </objective>

  <scope>
    <files>
      <file action="investigate">silver/accounts_dimension + silver/allocations latest partitions — find the field/pattern that distinguishes Opal-model accounts</file>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py OR D_02.advisor_client_detail.py — add is_opal_model emit (Phase 0 picks D-tier script)</file>
      <file action="modify">data/black_diamond/scripts/gold/lib/s3_layout.py — if new key needed (likely additive field to existing artifact, not new key)</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add validator for is_opal_model field presence + coverage ratio check (non-null ≥ 95%)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="phase-0-source-decision">
      Session log documents: authoritative source of is_opal_model distinction (e.g., `silver/accounts_dimension.account_type == 'Opal_Model'` or similar). If ambiguous, Phase 0 MCP to Andrew via COO for field-definition ruling BEFORE code-write.
    </deliverable>
    <deliverable id="is-opal-model-emit">
      is_opal_model boolean field emitted per-account (or per-position — Phase 0 call) in chosen D-tier artifact. Additive — no existing field changes.
    </deliverable>
    <deliverable id="coverage-metric">
      Expected coverage ratio: ~31.74% of accounts True (per current cost_basis coverage observation). Document actual ratio post-emit.
    </deliverable>
    <deliverable id="de-follow-on-spec">
      Short spec snippet (not a TO) in session log describing what DE needs to do to wire the filter: query key, field path, filter semantic ("show Top Positions only for accounts where is_opal_model=True"). COO authors DE TO from this.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Phase 0 authoritative source confirmed with Andrew if ambiguous; documented in session log.</ac>
    <ac id="2">is_opal_model field emitted in chosen D-tier artifact — additive to existing schema, non-null for all rows.</ac>
    <ac id="3">Coverage ratio (is_opal_model=True / total) logged + within sanity band (25%-40% given current 31.74% cost_basis observation).</ac>
    <ac id="4">gold_validate_config.yaml validator block added; `comp-validate <D-script> --artifact <artifact>` exits 0.</ac>
    <ac id="5">Zero changes to existing Top Positions emit content (schema-additive only).</ac>
    <ac id="6">`comp-blast <D-script>` post-change: no new downstream consumers appeared; no regression on existing Top Positions consumers.</ac>
    <ac id="7">py_compile + ds-commit-gate exit 0.</ac>
    <ac id="8">Session log Compiler Tools section + MCP COMPLETE with commit hash + coverage ratio + DE follow-on spec snippet.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>python3 -c "import pyarrow.parquet as pq; df = pq.read_table('s3://opal-data-bd/silver/accounts_dimension/<latest>.parquet').to_pandas(); print(df.columns.tolist()); print(df['account_type'].value_counts() if 'account_type' in df.columns else 'no account_type')"</run>
        <expect>Surface the field(s) that distinguish Opal-model accounts. Candidate: account_type, managed_by, model_portfolio_flag, or similar.</expect>
        <if_mismatch>If no clear field, MCP Andrew via COO for ruling BEFORE code-write. Do not guess.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse cost_basis</run>
        <expect>Enumerate portal consumers of cost_basis. Confirms that Top Positions is the primary consumer + any other widgets affected by is_opal_model filter.</expect>
        <if_mismatch>If other widgets also want this filter, expand DE follow-on TO scope.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_04.client_portal_summary</run>
        <expect>D_04 READS include silver/accounts_dimension (or identify if new read needed).</expect>
        <if_mismatch>If D_04 doesn't read accounts_dim, consider D_02 instead OR add the read in this TO.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_04.client_portal_summary</run>
        <expect>Consumer list; confirms Top Positions widget dependency path.</expect>
        <if_mismatch>Unexpected consumers = coordinate before writing.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix flagged issues.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/client_portal_summary_sample.json</run>
        <expect>Exit 0; is_opal_model validator passes.</expect>
        <if_mismatch>Iterate validator.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/D_04.client_portal_summary.py">
      Active TO history: CP-WP5 (2026-04-22 close), COHORT-A (2026-04-22 close). Additive field only — low collision risk.
    </shared_resource>
    <downstream_pending>DE follow-on TO for portal filter wiring — COO authors from Phase-0 spec snippet post-completion.</downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT guess the Opal-model distinction. Phase 0 MCP Andrew if ambiguous.</rule>
    <rule>Do NOT add the portal filter in this TO — DE follow-on.</rule>
    <rule>Do NOT change existing Top Positions content — additive flag only.</rule>
    <rule>Do NOT retroactively backfill is_opal_model to historical partitions.</rule>
  </do_not>
</task_order>
