<task_order>
  <metadata>
    <id>YALP_MDSRC.F1</id>
    <slug>dsa-macro-page-input-audit-and-fred-exploration</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics~A</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON BOOT — Andrew-direct. 0.2.0_DS_PortfolioAnalytics~A is a new Andrew-spawned agent; this TO is in its task_orders/ folder to be picked up on the startup protocol. No gate — begin on boot. Q1-INDEPENDENT (FRED is a separate source from the YCharts Q1 decision).</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct. The definitive FRED-sourcing answer for the Macroeconomics portal page; feeds the v0.4 amendment + upgrades the v0.3 WS1-MAC-01 verdict.</priority>
    <sla>Substantial structured audit — comparable in depth to a WS-domain audit (~2-4 effort-days), NOT a quick mapping. Comprehensive + structured is Andrew's explicit ask. Interim partials welcome.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. §5.2 surface WS1-MAC-01 (Macroeconomics — macro indicators, 12 groups, currently "Bloomberg-leaning hybrid"); WS1-MAC-02 (VIX, already FRED VIXCLS); WS1-MAC-03 (Treasury yield curve, already FRED). This TO is the dedicated Macroeconomics/FRED workstream — it elevates the WS1-MAC-01 macro mapping OUT of TO-C2's sub-task list into its own audit.</prd>
    <pipeline_docs>infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md — the yang manifest -> portal-JSON flow; the Macroeconomics page's artifacts + their generators.</pipeline_docs>
    <fred_baseline>The EXISTING FRED integration already shipped in this pipeline — VIX (vix_data.json, FRED series VIXCLS) and the Treasury yield curve (yield_curve_fred.json). This is the proven extension baseline: study how the FRED API key is wired + how the pull works today.</fred_baseline>
  </references>

  <context>
    Andrew-direct, 2026-05-20: "comprehensive, structured audit of all inputs for the Macroeconomics portal page, and then comprehensive exploration of the FRED API." The portal's Macroeconomics page is today fed largely by the manual Bloomberg-pkl yang-pipeline, EXCEPT VIX + the yield curve which are already on FRED. This TO determines, definitively, how much of the Macroeconomics page can move to FRED — a free, official, public-data API — and what genuine residue must stay manual Bloomberg or need another source. It is structured as TWO comprehensive phases. v0.2 authorizes NO code/Terraform/portal change — this is an audit; the implementation is a later TO.
  </context>

  <scope>
    <in_scope>
      PHASE 1 — Comprehensive structured audit of ALL Macroeconomics portal-page inputs.
      Not just macro_data.json's 12 indicator groups — the WHOLE page. Enumerate every portal component on the Macroeconomics page, every JSON artifact it consumes (macro_data.json, vix_data.json, macro_timeseries.json, yield_curve_fred.json, and ANY other artifact the page resolves), and every underlying data input/indicator behind each artifact. Deliver a STRUCTURED INVENTORY — per input: name; current source (Bloomberg ticker / FRED series / other); what it feeds on the page; refresh cadence; units + any transform applied. The output is a complete, authoritative "what does the Macroeconomics page actually consume" input map.

      PHASE 2 — Comprehensive exploration of the FRED API.
      A real capability exploration, not a series-ID lookup: obtain/confirm the FRED API key + how it authenticates; the full FRED API surface (series search, observations, categories, releases, tags); rate limits; data coverage + timeliness. Study how the existing VIX / yield-curve FRED integration is wired as the extension baseline (can that mechanism extend to all inputs, or does it need new pull code; how the key is stored). Then map every Phase-1 input onto FRED: the FRED series ID per indicator; a fidelity check of the FRED series VALUES vs the portal's current Bloomberg-pkl values (same method as the YCharts-vs-Bloomberg exhaustion); and the genuine non-FRED residue — any international macro series FRED does not carry at adequate timeliness, any licensed private index (e.g. FRED carries the public ISM PMI but not the licensed S&P Global/Markit PMI) — each named with the alternative source it would need.
    </in_scope>
    <out_of_scope>
      - NO code / Terraform / portal change — this is an audit; the FRED-integration build is a later implementation TO.
      - Correlation + market-data surfaces — out of the Macroeconomics page; not this TO.
      - The YCharts side — the three DS YCharts audits + TO-C2 own that; F1 is FRED + the Macroeconomics page only.
      - The official-API-vs-scrape Q1 decision — irrelevant here; FRED is its own official free API.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the audit">
      <step>
        <run>comp-routes behaviors</run>
        <expect>Confirms the serving paths for the Macroeconomics page artifacts (the /api/general/json/macro/* family) — anchor the Phase-1 per-artifact serving-path column to compiler-confirmed fact.</expect>
        <if_mismatch>Document any serving-path delta as an audit finding + RAVC1 to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io yang-generate-macro  +  comp-pipescript io yang-generate-macro-timeseries</run>
        <expect>The load list + COLUMN GAPS + portal consumers for the macro generators — use this to enumerate the macro inputs accurately rather than reading the scripts blind.</expect>
        <if_mismatch>If a generator is not a comp-pipescript node, fall back to a direct source read of `infra/aws/lambda/v2_portal/yang_pipeline/` + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>(none) — audit deliverable is a committed brief + the mapping table; no code authored.</run>
        <expect>No py_compile / ruff gate applies.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>(none) — the input map + the FRED mapping table are the deliverable's self-validation (per-input fidelity column).</run>
        <expect>Checked by the acceptance criteria.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    The WS1-MAC-01 per-indicator macro mapping is being TRIMMED out of TO-C2's scope (COO edit, same dispatch) so the macro/FRED work is not double-owned — TO-C2 stays the YCharts market-data pull (WS-1 indices/securities + WS-2 hybrid inputs); F1 owns macro/FRED. If the audit surfaces a macro indicator best sourced from YCharts rather than FRED, flag it to TO-C2 — do not silently re-scope. No shared files written (audit-only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 1: a complete structured input map of the Macroeconomics page — every component, every consumed JSON artifact, every underlying indicator; per input: name / current source / what it feeds / cadence / units+transform. Nothing on the page omitted.</ac>
    <ac id="AC2">Phase 2: the FRED API explored as a capability — key + auth confirmed; the API surface (search/observations/categories/releases/tags), rate limits, coverage, timeliness documented; the existing VIX/yield-curve FRED integration characterized as the extension baseline (mechanism + key storage + whether it extends or needs new pull code).</ac>
    <ac id="AC3">Every Phase-1 input mapped onto FRED: the FRED series ID per indicator, with a fidelity check of FRED values vs the portal's current Bloomberg-pkl values. The committed mapping table is machine-readable.</ac>
    <ac id="AC4">The genuine non-FRED residue named explicitly — each international/licensed series FRED cannot serve at adequate timeliness, with the alternative source it would need. This quantifies the v0.3 WS1-MAC-01 verdict upgrade ("Bloomberg-leaning hybrid" -> the exact FRED-replaceable fraction + the residue).</ac>
    <ac id="AC5">Deliverable: a committed FRED macro-sourcing brief + the Bloomberg-ticker -> FRED-series-ID mapping table, pushed + push-confirmed on origin/CLOUD. Session log with a Compiler Tools section reproducing the Phase-1 comp-routes + comp-pipescript runs. RAVC2 to 1.0.0_SA_CTO (feeds the v0.4 amendment).</ac>
  </acceptance_criteria>

  <deliverables>
    - The Phase-1 structured Macroeconomics-page input map.
    - The Phase-2 FRED API capability exploration + the Bloomberg->FRED mapping table + the non-FRED residue list.
    - A committed brief (e.g. docs/briefs/mdsrc-fred-macro-sourcing-audit-20260520.md).
    - Session log with Compiler Tools section. RAVC2 to 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT treat this as a quick series-ID mapping — Andrew's explicit ask is a comprehensive, structured, two-phase audit. Size it accordingly.</rule>
    <rule>Do NOT author code / Terraform / portal changes — this is an audit; implementation is a later TO.</rule>
    <rule>Do NOT handle the FRED API key in chat / MCP / git / logs — if it must be stored, that is an implementation-TO concern; for the audit, confirm how it authenticates without exposing the key value.</rule>
    <rule>No emojis in the brief, the mapping table, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
