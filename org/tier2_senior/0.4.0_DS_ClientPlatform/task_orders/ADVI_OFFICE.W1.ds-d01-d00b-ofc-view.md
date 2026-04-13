<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-13-office-w1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>pending</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_OFFICE_PRD.md</ref>
    <ref type="source_dim">data/black_diamond/config/office_mapping/advisor_registry_lusha_office_bridge_clean.csv</ref>
    <ref type="dim_readme">data/black_diamond/config/office_mapping/README.md</ref>
  </references>

  <objective>
    Add OFC (Office) cohort to two gold artifacts:
    1. `partner_analytics_{gran}.json` — gains `views.ofc[period_key]` (Snapshot AUA + L1 advisors)
       and `views.nna[period_key].ofc` (NNA by office). Implemented in D_01.
    2. `timeseries_chart.json` — gains top-level `ofc` (daily stacked AUA by office) and
       `nna_ofc` keys. Implemented in D_00b.
    D_04 is a pure pass-through for both artifacts — no changes needed there.
  </objective>

  <context>
    PRD §1-§5 and §7 (Wave 1) are authoritative. Key decisions (all resolved by Andrew 2026-04-13):
    - Unresolved advisors fold into "Other" bucket (key="other", label="Other",
      CHART_OTHER_COLOR gray). All accounts must be included to preserve canonical firm AUA.
    - Continuous AUA by OFC (D_00b) is in-scope for V1. No placeholder or deferral.
    - ADV toggle stays — OFC is added as a third toggle alongside GEO and ADV.

    Dim source: `data/black_diamond/config/office_mapping/advisor_registry_lusha_office_bridge_clean.csv`
    10 resolved offices (Arkansas, Atlanta, Austin, Charlotte, Dallas, Houston, Jacksonville,
    Kansas City, Los Angeles, Minnesota). 13 unresolved non-architect names — all fold into Other.
    Zero unresolved architects.

    At EC2 runtime, scripts read dim from:
      s3://opal-data-bd/gold/dimensions/dim_advisor_office.csv
    AE uploads this file in W2 (before triggering the gold run). For local dry-run,
    use the local CSV path directly (no S3 call required for validation step).

    Schema for `views.ofc` and `views.nna[period].ofc`: see PRD §4.1 and §4.2.
    Schema for timeseries `ofc` + `nna_ofc` keys: mirror `adv` / `nna_adv` structures exactly.
    Cross-domain note: `types.ts` will also be touched by ADVI_REBORN.W6-004 (DE).
    W6-003 DS must ship before DE touches types.ts for both projects. DS ships W6-003 first.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-pipescript io D_01` — confirm reads/writes. Note: dim_advisor_office.csv is a
      dynamic S3 read not tracked in graph; this is expected. Reads/writes confirmed by CTO PRD.
    - `comp-pipescript io D_00b` — confirm reads/writes. TIMESERIES_CHART write confirmed.
    - Read `build_adv_view` and `build_nna_adv_view` in D_01 for structural parity reference.
    - Read `_build_advisor_view` in D_00b for structural parity reference.

    Phase 2 (before committing):
    - Local dry-run using local CSV path override for dim load:
      * Verify `views.ofc.current.donut.segments` has >= 5 office keys + "other".
      * Verify `sum(seg.aua for seg in views.ofc.current.donut.segments)` == firm_total_aua
        within $0.01 (Other bucket ensures exact match).
      * Verify Austin segment present; Travis Penfield in Austin advisors list with AUA > $300M QTD.
      * Verify `views.nna.current.ofc` present with >= 3 office segment keys.
      * Verify `timeseries_chart.json` contains top-level `ofc` key with `categories` + `data`.
      * Verify `nna_ofc` present with >= 3 office keys.
    - Check `sum(ofc.donut.segments.aua)` == `sum(geo.donut.segments.aua)` (same canonical AUA).

    Phase 3 (after AE triggers gold run — MCP-message AE after W1 commit):
    - AE will verify platinum artifacts and send MCP confirmation.
    - DS appends to `org/compiler-tools-log.md` after gold run verified.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>gold/artifacts/partner_analytics/header_metrics_{gran}.json</shared_resource>
    <shared_resource>gold/artifacts/timeseries_chart.json</shared_resource>
    <shared_resource>data/black_diamond/scripts/gold/D_01.partner_analytics.py</shared_resource>
    <shared_resource>data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</shared_resource>
    <also_in_to>ADVI_OFFICE.W2 (AE — dim upload + gold run trigger)</also_in_to>
    <also_in_to>ADVI_OFFICE.W3 (DE — frontend consumes ofc views from same endpoints)</also_in_to>
    <also_in_to>ADVI_REBORN.W6-003 (DS — currently pending, touches D_00c only, not D_01/D_00b)</also_in_to>
    <required_action>
      Complete W6-003 FIRST before starting this task order (different scripts, but
      ship W6-003 so the gold artifact is clean before adding OFC changes on top).
      After committing D_01 + D_00b to CLOUD and uploading to S3, MCP-message
      0.6.0_AE_PartnerETL with: commit hash, S3 code upload confirmation, and
      "ADVI_OFFICE W1 ready — please proceed with W2 dim upload + gold run."
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `partner_analytics_quarterly.json` contains top-level key `views.ofc` with >= 5 office segments.
    2. For `current` period: `sum(ofc.donut.segments.aua)` within 5% of `views.geo.current.metrics.aua`.
    3. Austin segment present; Travis Penfield in Austin's `advisors` list with AUA > $300M QTD.
    4. `views.nna.current.ofc` present with >= 3 office segment keys.
    5. "other" segment always present; `sum(all segments.aua)` == `firm_total_aua` exactly.
    6. `timeseries_chart.json` contains top-level `ofc` key with >= 5 named office categories + `other`.
    7. All 3 granularities (quarterly, monthly, annual) updated for both artifacts.
    8. Session log includes dim audit table: account count per office + Other count + AUA per office.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_01.partner_analytics.py</file>
      <file action="modify">data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</file>
    </files>
    <out_of_scope>
      D_04 (pure pass-through, no changes needed).
      Frontend (DE W3). AE gold run trigger (AE W2).
      Rerunning Lusha enrichment for new advisor names (rerun policy: append only).
    </out_of_scope>
  </scope>

  <schema>
    See PRD §4.1 for `views.ofc[period_key]` structure.
    See PRD §4.2 for `views.nna[period_key].ofc` structure.
    See PRD §5.3 for D_00b `ofc` + `nna_ofc` timeseries structure.

    Key invariant: `sum(seg.aua for seg in views.ofc[p].donut.segments)` == `firm_total_aua`
    (the "other" bucket makes this exact — all unresolved accounts are counted there).
    Segment key format: lowercase office name, spaces → underscores (e.g., `los_angeles`, `kansas_city`).
    OFC donut center override: apply same cert override as ADV and GEO (`views.ofc[period]['donut']['total'] = round(certified, 2)`).
  </schema>

  <deliverables>
    - Commit D_01 + D_00b to CLOUD with DS author (`--author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"`).
    - S3 upload both scripts to `s3://opal-data-bd/code/gold/` (build-and-upload.sh or direct cp).
    - MCP message to 0.6.0_AE_PartnerETL: commit hash + S3 upload confirmation + GO for W2.
    - Session log with compiler tools section + dim audit table.
  </deliverables>
</task_order>
