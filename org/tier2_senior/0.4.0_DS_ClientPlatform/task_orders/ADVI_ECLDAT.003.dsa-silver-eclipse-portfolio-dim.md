<task_order>
  <metadata>
    <id>ADVI_ECLDAT.003</id>
    <slug>dsa-silver-eclipse-portfolio-dim</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>Cascade unblock post ADVI_ECLDAT.002 (Phase 2 bronze puller) RAVC2. Phase 3 silver consumes Phase 2 bronze outputs; gates on bronze artifacts materializing on S3 + sentinel manifest empirically valid.</dispatch_unblock_condition>
    <project_code>ADVI_ECLDAT</project_code>
    <priority>P1 — Andrew dashboard tomorrow gate; silver layer enables future gold script (Phase 4 deferred per Andrew "gold layers can wait")</priority>
    <sla>~2h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="feasibility_brief">docs/briefs/data-scientist-eclipse-ingestion-feasibility-20260514.md (DS~A `23d2e2c54`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~21:0XZ: "set up the same jwt refresher that we did for orion for eclipse as well as figuring out bronze and silver ingestion, gold layers can wait for now"</ref>
    <ref type="rule17_strict">CLAUDE.md Rule 17 — silver tier = dedupe + type standardization ONLY; no field slimming; no fillna defaults; no business-logic derivations</ref>
    <ref type="phase2_dependency">ADVI_ECLDAT.002 bronze puller (RAVC2 gates this Phase 3 dispatch)</ref>
    <ref type="type_coercion_spec">Eclipse accountId STRING ↔ Orion id INT type-coerced join per CTO feasibility brief §Schema-mechanics</ref>
  </references>

  <context>
    Eclipse silver tier consumes Phase 2 bronze artifacts (`bronze/eclipse/{date}/`) emitting silver-tier portfolio dim + model composition records. Per CLAUDE.md Rule 17 strict:
    - Dedupe exact-row duplicates
    - Standardize dtypes: Eclipse accountId STRING → STRING preserved; Eclipse internal IDs INT preserved
    - **Type-coerced join key:** Eclipse `accountId` (STRING) ↔ Orion `id` (INT) — Cast Eclipse accountId to INT64 for join column; PRESERVE original STRING as `eclipse_account_id_raw` for audit trail
    - NO field slimming (preserve all bronze columns)
    - NO fillna defaults (preserve null semantics)
    - NO business-logic derivations (those belong in gold; Phase 4 deferred)

    Silver tier emits cleaned + type-standardized + join-ready dim tables. Gold tier (Phase 4 deferred) will derive `opal_account_overlay.json` from this silver dim + Orion canonical dims.

    Per CLAUDE.md Rule 14+15: ds-commit-gate.sh + `from __future__ import annotations` first import + silver `coerce_silver_ids()` enforcement.
  </context>

  <objective>
    Author new silver script consuming Phase 2 bronze Eclipse artifacts; emit cleaned + type-coerced dim tables to silver-tier S3 path. Type-coerced join key handled (Eclipse accountId STRING → INT64 with raw STRING preserved). Strict Rule 17 compliance.
  </objective>

  <scope>
    <files>
      <file action="create">data/orion/scripts/silver/convert_eclipse_portfolios_to_silver.py — new silver script (~100 LOC)</file>
      <file action="readonly_reference">data/orion/scripts/silver/{existing Orion silver scripts} — pattern source for structure + Rule 17 compliance pattern</file>
      <file action="readonly_reference">ADVI_ECLDAT.002 bronze output schema — input contract</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io {existing Orion silver script with type-coerced join} — pattern source for type coercion + ID preservation</run>
      <expect>Pattern source for STRING→INT64 coercion with raw STRING preservation conventions.</expect>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/bronze/eclipse/{today}/ — verify Phase 2 bronze artifacts materialized + sentinel manifest pull_complete.json present</run>
      <expect>Bronze artifacts present; sentinel manifest valid. If missing, Phase 2 RAVC2 gates this dispatch.</expect>
    </step>
    <step>
      <run>Inspect bronze artifact schemas: `aws s3 cp s3://opal-data-inf/bronze/eclipse/{today}/portfolios.csv - | head -3` + per-model composition shape</run>
      <expect>Empirical schema understanding for silver type-coercion mapping.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Author convert_eclipse_portfolios_to_silver.py:
        - `from __future__ import annotations` first import per Rule 15
        - Read bronze artifacts from `s3://opal-data-inf/bronze/eclipse/{date}/`
        - Dedupe exact-row duplicates (Rule 17)
        - Standardize dtypes: Eclipse internal INT fields preserved; STRING fields preserved
        - **Type-coerce accountId STRING → INT64**: `silver_df['eclipse_account_id_int'] = pd.to_numeric(silver_df['accountId'], errors='coerce').astype('Int64')` — PRESERVE `eclipse_account_id_raw = silver_df['accountId']` (original STRING) for audit trail
        - `coerce_silver_ids()` enforcement per ds-precommit-check.py (Rule 14)
        - NO field slimming; NO fillna defaults; NO business-logic derivation
        - Write silver artifacts to `s3://opal-data-inf/silver/eclipse/{date}/`
        - Sentinel manifest `_meta/silver_complete.json` with rows + dedupe_dropped + type_coercion_errors + started_at + completed_at
        - No emoji per CLAUDE.md</run>
      <expect>Silver script ~100 LOC; Rule 17 strict compliance; type-coerced join column emitted with raw preserved.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh: py_compile + ds-precommit-check.py (AST + coerce_silver_ids enforcement) + ruff py39 0.15.11</run>
      <expect>All 3 PASS.</expect>
    </step>
    <step>
      <run>Local dry-run: invoke script against today's bronze artifacts; verify silver outputs land at silver/eclipse/{today}/</run>
      <expect>Silver artifacts populated; type-coercion clean; sentinel manifest written.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + deploy">
    <step>
      <run>safe-commit.sh per Rule 13: commit → push → S3 upload → comp-pipescript deployed MATCH</run>
      <expect>All gates PASS. Author identity DS~A.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 (Phase 1 JWT extension) + DE 0.4 (Phase 5 FE consumer of opal_account_overlay; gated on Phase 4 gold which is deferred)</run>
      <expect>Evidence-bearing close: commit SHA + safe-deploy log + silver S3 sentinel verification.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `convert_eclipse_portfolios_to_silver.py` created with `from __future__ import annotations` first import
    AC2: Bronze artifacts consumed from `bronze/eclipse/{date}/`; silver artifacts written to `silver/eclipse/{date}/`
    AC3: Dedupe applied (exact-row duplicates removed)
    AC4: Type-coercion: `eclipse_account_id_int` (Int64) + `eclipse_account_id_raw` (STRING) both emitted
    AC5: `coerce_silver_ids()` enforcement per Rule 14
    AC6: Rule 17 strict: NO field slimming + NO fillna defaults + NO business-logic derivations
    AC7: Sentinel manifest `_meta/silver_complete.json` emitted with rows + dedupe stats + coercion error count + timestamps
    AC8: ds-commit-gate.sh PASS
    AC9: safe-deploy.sh PASS + S3 upload + comp-pipescript deployed MATCH
    AC10: No emoji per CLAUDE.md
    AC11: RAVC2 to COO + CC CTO + AE 0.6.1 + DE 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-pipescript io reference + bronze artifact verify; Phase 2 ds-commit-gate.sh; Phase 3 safe-deploy.sh + comp-pipescript deployed MATCH.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: ADVI_ECLDAT.002 (Phase 2 bronze puller) RAVC2 — silver consumes bronze artifacts.
    PARALLEL-OK: ADVI_ECLDAT.001 AE 0.6.1 (Phase 1 JWT extension; independent of silver tier).
    NO PORTAL CHANGES.
    PHASE 4 GOLD DEFERRED: per Andrew 2026-05-14 ~21:0XZ "gold layers can wait for now". Phase 4 INF_D_XX.opal_account_overlay.py NOT in current scope.
    PHASE 5 FE DEFERRED: DE 0.4 PRD against dashboard product spec (gated on Phase 4 gold which is deferred).
    DS SUB-AGENT ROUTING: DS~A primary per CTO route.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure new silver layer; no historical backfill. Day-of ship + daily emit cadence cascades from bronze.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. convert_eclipse_portfolios_to_silver.py (~100 LOC)
    2. Silver artifacts under silver/eclipse/{date}/
    3. Type-coerced join columns (Int64 + STRING raw preserved)
    4. Sentinel manifest silver_complete.json
    5. ds-commit-gate + safe-deploy + S3 SHA-MATCH
    6. RAVC2 with deploy + dry-run evidence
  </deliverables>

  <ravc>DS~A RAVC2 to COO + CC CTO + AE 0.6.1 + DE 0.4 on AC1-11 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~A <0.4.0_DS_ClientPlatform~A@opal.agent>"`.

    **Rule 17 strict reminder:** silver does ONLY dedupe + type standardization. NO field slimming. NO fillna. NO business-logic. If tempted, escalate to COO for Phase 4 gold scope expansion (Phase 4 currently deferred per Andrew).

    **Type-coercion accountId pattern:** PRESERVE both `eclipse_account_id_raw` (STRING source-of-truth) + `eclipse_account_id_int` (Int64 join-ready) for audit trail + Orion join. NEVER lose the raw STRING — gold tier may need it for Eclipse audit log reconciliation.

    **Coercion error handling:** `pd.to_numeric(errors='coerce')` produces NaN on un-coercible STRING values. Sentinel manifest tracks coercion error count; if >0, surface to COO for investigation TO (un-coercible accountId would indicate Eclipse schema drift OR data quality issue).

    **Phase 4 gold deferral:** opal_account_overlay.json (firm-level gold) is the eventual consumer. Andrew "gold can wait" framing: silver is enough for now (bronze + silver gets ingestion pipeline running; gold derivation happens when dashboard FE wiring catches up). Worth banking as banking-discipline observation: "ingestion-first, derivation-later" sequencing.

    **No emoji per CLAUDE.md.** Plain ASCII log prefixes.
  </notes>
</task_order>
