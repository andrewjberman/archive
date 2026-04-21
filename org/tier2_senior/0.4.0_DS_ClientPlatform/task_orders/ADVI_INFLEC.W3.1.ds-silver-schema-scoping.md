<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w3.1-silver-scoping</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <co_owner>1.0.0_SA_CTO</co_owner>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Define the canonical silver-layer schema for Inflection's Orion CSV exports: column names, dedup rules, date parsing convention, and how ambiguous Orion fields map to silver. Output is a written schema spec DS uses to author `convert_orion_to_silver.py` (W3.2). CTO + DS joint — DS proposes from DS investigation brief; CTO validates against serving-layer requirements.
  </objective>

  <context>
    PRD §5.1-§5.2. Inflection source: Orion Portfolio Solutions CSVs (TRN, AUM snapshots, Slickgrid accounts). DS investigation brief at `docs/briefs/cto-brief-inflection-partner-data-investigation.md` has the raw column inventory. Silver target mirrors BD silver layout where structurally applicable: `silver/transactions/{date}.parquet`, `silver/accounts_dim/{date}.parquet`, `silver/aum_snapshot/{date}.parquet`.

    Known design decisions needed:
    - Rep ID + Rep Name → `advisor_key` slug derivation (snake_case, match gold-layer advisor slug)
    - "Firm" rep bucket handling (287 HH / $193.6M — exclude from individual attribution or map to a firm-bucket key)
    - "New Accounts Rep" (51,670 rows) — PRD §10 Q9: exclude from individual advisor attribution convention
    - Q2 2024 gap (Apr-Jun 2024) — flag all rows from that window in silver with `data_gap=True`? Or leave as-is with documented absence?
    - Date parsing: Orion TRN date column format (ISO? MM/DD/YYYY?)
    - NaT guard: any outer-merge that can produce NaT date must coerce (lessons from d87377a5 C_01 incident)

    **Parallelizable with W1:** does not require infrastructure to exist. DS can start immediately upon receiving this TO's GO; CTO review is async (MCP back-and-forth, not synchronous session).
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-pipescript io convert_orion_to_silver (once script exists — not yet, skip)</run>
    (N/A in this scoping TO. Runs in W3.2.)

    <run>cat docs/briefs/cto-brief-inflection-partner-data-investigation.md</run>
    <expect>Full column inventory from DS~D investigation. Use this as the source-of-truth for Orion field names.</expect>

    Phase 3:
    (N/A — document-only TO.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Schema spec doc committed at `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/advi_inflec_silver_schema_spec.md`.
    2. For every Orion source column: silver column name, dtype, nullable flag, derivation rule.
    3. Table-level decisions documented: dedup key, sort order, partition strategy.
    4. Orion → silver field mapping for TRN, AUM snapshot, accounts_dim.
    5. Rep ID → advisor_key slug derivation rule specified.
    6. Firm-rep bucket and "New Accounts Rep" conventions specified.
    7. Q2 2024 gap handling documented (gap flag vs absent-only vs other).
    8. NaT guard requirement noted for any outer-merge join.
    9. CTO sign-off comment in the doc (or separate MCP ack noting sign-off).
    10. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/advi_inflec_silver_schema_spec.md</file>
      <file action="reference">docs/briefs/cto-brief-inflection-partner-data-investigation.md</file>
      <file action="reference">data/black_diamond/scripts/gold/ (BD precedents for silver column naming)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">DS proposes; CTO must acknowledge before DS starts W3.2 implementation.</requirement>
    <requirement id="2">NaT guard on any outer-merge join — explicit note per d87377a5 incident.</requirement>
    <requirement id="3">Q2 2024 gap must have a stated handling convention — not silently absent.</requirement>
    <requirement id="4">DS drafts from investigation brief; CTO validates serving-layer alignment.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Silver schema spec with CTO sign-off.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start W3.2 implementation before CTO acknowledges the spec.</rule>
    <rule>Do NOT invent column names without tracing to Orion source field.</rule>
  </do_not>
</task_order>
