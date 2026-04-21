<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.8-partner-schema-doc</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Create `infra/aws/users/partner-schemas/inflection.md` per ONBOARDING.md §5 Step 6 — documents Inflection's partner-specific schema extensions (even if identical to 49F at go-live) for future divergence tracking. Document-only TO; no code, no infra.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.2 row 7 + ONBOARDING.md §5 Step 6: "Create `infra/aws/users/partner-schemas/{firmId}.md` describing any partner-specific schema extensions. Even if the schema is identical to 49financial today, write the file so future divergence is tracked."

    Source content for the doc — draw from `docs/briefs/cto-brief-inflection-partner-data-investigation.md`:
    - Data source: Orion Portfolio Solutions (vs BD for 49F)
    - Custodian concentration: 99.4% Fidelity (vs 49F's mixed Fidelity + Schwab)
    - Rep attribution: per-transaction Rep ID + Rep Name (natively per-day gated — no CHART-ALIGN needed)
    - "Firm" rep bucket: 287 HH / $193.6M / 29% firm AUM
    - Date coverage: 2019-09-17 → 2026-04-20 (Q2 2024 gap pending re-download)
    - Transaction volume: 4.29M unique
    - AUM: $667M / 979 HH / 1,476 active accounts / 2,851 historical

    Schema identicality check vs 49F partner table: both use `opal-partner-{firmId}` with email PK, advisorKey/advisorName/advisorRole/firmRole attributes, GSI ByAdvisorRole. Inflection partners get the module-instantiated table (W1.4) — no attribute-level divergence today.

    Planned divergence items to note (forward-looking, so future agents know):
    - Potential `investment_model` dimension (Lighthouse / IWM / Core — Orion-specific split)
    - Potential per-advisor role set differences (Inflection-specific rep roles vs 49F's architect/implementor/consultant)
    - OTP-gated ingestion requires operational notes distinct from 49F's direct BD export path
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>cat infra/aws/users/partner-schemas/49financial.md</run>
    <expect>Reference doc structure. If file doesn't exist, note that 49F predated §5 Step 6 — write Inflection doc as the canonical template and flag to CTO so 49F doc can backfill.</expect>

    <run>cat docs/briefs/cto-brief-inflection-partner-data-investigation.md</run>
    <expect>DS investigation brief — source of partner-specific facts.</expect>

    Phase 2: (N/A — doc-only, no tool invocation.)

    Phase 3 (after writing):
    <run>ls infra/aws/users/partner-schemas/</run>
    <expect>{49financial.md if exists, inflection.md}. Both partners represented.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `infra/aws/users/partner-schemas/` directory.
    last_write_owner: 0.4.0_DT_ClientPlatform.
    required_action: "No concurrent TOs touching this path. If 49financial.md doesn't exist, create alongside as a backfill (flag to CTO)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `infra/aws/users/partner-schemas/inflection.md` committed.
    2. Doc covers: (a) data source + custodian + rep attribution baseline, (b) schema identicality vs 49F, (c) forward-looking divergence watch list.
    3. Doc references the DS investigation brief as source of truth.
    4. If `49financial.md` doesn't exist, either create it concurrently as a symmetry backfill OR explicitly flag in the Inflection doc that "49F doc TBD; Inflection is the first partner-schema doc".
    5. Session log at `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-{NN}/advi_inflec_w1_8_partner_schema_doc.md` with references + doc outline rationale.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">infra/aws/users/partner-schemas/inflection.md</file>
      <file action="reference">infra/aws/users/ONBOARDING.md §5 Step 6</file>
      <file action="reference">docs/briefs/cto-brief-inflection-partner-data-investigation.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Doc lives under `infra/aws/users/partner-schemas/` — exact path per ONBOARDING.md §5 Step 6.</requirement>
    <requirement id="2">Cite the DS investigation brief as primary source.</requirement>
    <requirement id="3">Do NOT duplicate PRD content verbatim — summarize schema-relevant facts only.</requirement>
    <requirement id="4">No emojis in doc body. ASCII only.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">`infra/aws/users/partner-schemas/inflection.md` + session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT conflate with the PRD — this is a schema-specific reference doc, not a project plan.</rule>
    <rule>Do NOT include operational runbook content (that's ONBOARDING.md's job).</rule>
  </do_not>
</task_order>
