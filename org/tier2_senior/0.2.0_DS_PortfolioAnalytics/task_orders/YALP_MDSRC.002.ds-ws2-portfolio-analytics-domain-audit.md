<task_order>
  <metadata>
    <id>YALP_MDSRC.002</id>
    <slug>ds-ws2-portfolio-analytics-domain-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED — Phase 0 audit. Unblocks on Andrew GO (PRD v0.2 §9/§11: the four Phase-0 audits dispatch in parallel on Andrew GO). No inter-TO dependency — TO-1..4 are fully parallel. On GO: COO flips status->pending + dispatch_held=false + fires the GO message.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct (CEO interview 2026-05-20). WS-2 is the "Opal-proprietary analytics vs YCharts-computable" cut — the domain that decides how much of the portal stays permanently Bloomberg-pkl.</priority>
    <sla>~2-4 effort-days (PRD §9). Investigation TO; parallel with TO-1/3/4.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2 (1.0.0_SA_CTO). This TO = WS-2 / §8 TO-2. v0.2 re-cut the audit into three DS domain audits — read §16 Amendment history, §3 (CTO HAR findings), §3.3 (endpoint inventory), §4 (domain-seam declarations) before scoping.</prd>
    <recon_doc>docs/briefs/ycharts-bloomberg-portal-data-sourcing-audit-20260520.md (commit 3987616d8) — DS 0.1.0's Phase-0 recon brief; the recon doc-of-record.</recon_doc>
    <har>C:\Users\AndrewBerman\Downloads\ycharts.com.har — 92 MB, 1,894 entries. Primary evidence base. HAR bodies not saved -> fill by live-probe capture.</har>
    <pipeline_docs>infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md + data/yang_pkl/docs/CLOUD_PIPELINE_ARCHITECTURE.md — the yang->portal map (PRD §5: NOT in the comp-graph).</pipeline_docs>
  </references>

  <context>
    YALP_MDSRC determines, surface by surface, which portal market-data surfaces (today fed by the manual Bloomberg-pkl yang-pipeline) could move to a daily automated YCharts pull. PRD v0.2 (Andrew-direct, pre-dispatch) split the audit into THREE parallel DS domain audits. WS-2 owns the PORTFOLIO ANALYTICS domain end-to-end: performance/risk-return metrics, factor data, attribution, classifications, benchmark/peer analytics, CMA. This domain holds the hardest classification calls — `model_pkl` is Opal-proprietary model output and `cma_excel` is Opal's own assumptions; WS-2 must explicitly separate Opal-proprietary analytics from YCharts-computable metrics. v0.2 authorizes NO code/Terraform/portal change — audit deliverable only (committed brief + matrix slice).
  </context>

  <scope>
    <in_scope>
      End-to-end audit of the PORTFOLIO ANALYTICS domain:
      - (a) YCharts capability — deep-parse the HAR for the analytics endpoints (`/charts/scatter_plot_data.json` POST risk/return metrics, `/calculations/calc_info`, `/calculations/metric_sets`, `/securities/attribution_contributors_detractors/{ticker}`, `/classifications/sectors.json`, the model-portfolio benchmark/analytics endpoints). Live-probe to fill response schemas. Cross-reference the `all_calc_menu` 3 MB catalog for analytics/risk metrics (Q5, WS-2 slice — consume WS-1's catalog parse). Evaluate the official YCharts API for these data classes (Q1/Q7 input).
      - (b) Portal surfaces — inventory Factor Tilts, Positioning (positioning data, allocation summary, holdings attribution), CMA, and the Model Portfolios *benchmark / model-portfolio-benchmark / ETF-returns / peer-performance* surfaces. Each to the component / JSON-artifact / rendered-field level, with source artifact + refresh cadence.
      - (c) Per-surface source classification — with EXPLICIT attention to what is Opal-proprietary analytics (`model_pkl` model output, `cma_excel` assumptions) vs. YCharts-computable. Name the proprietary surfaces as Bloomberg-pkl-only/proprietary (Q6). This is the WS-2 slice of the migration-candidate matrix in the common slice schema (agree the schema with WS-1/WS-3).
    </in_scope>
    <out_of_scope>
      - NO code, Terraform, Lambda, or portal change (v0.2 is audit-only).
      - External-market-data surfaces (Market Overview, Valuation, Correlation, Macroeconomics, the DynamoDB price series) — WS-1 (TO-1).
      - Model-portfolio PERFORMANCE sourcing + SmartX + client-facing data — WS-3 (TO-3). WS-2 owns the Model Portfolios *analytics/benchmark* surfaces only (the §4 seam).
      - The operational/credential pattern — WS-4 (TO-4).
      - Finalized cross-domain migration verdicts — WS-5 (TO-5).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the audit">
      <step>
        <run>comp-routes behaviors</run>
        <expect>Confirms the serving path for the WS-2 pages: `/api/public/json*` + `/json-tiered/*` -> S3 `opal-data-portal-v2` via the `public-data-router` Lambda@Edge (PRD §5). Anchor the per-surface serving-path column to this.</expect>
        <if_mismatch>If the observed path differs from PRD §5, document the delta as an audit finding + RAVC1 to COO.</if_mismatch>
      </step>
      <step>
        <run>(yang->portal mapping) map via PORTAL_DATA_FLOW.md + a portal/src fetch-path grep — DO NOT use comp-blast.</run>
        <expect>PRD §5 confirmed the yang generator Lambdas have NO comp-graph downstream edges. PORTAL_DATA_FLOW.md + the portal fetch grep is the authoritative map.</expect>
        <if_mismatch>If PORTAL_DATA_FLOW.md is stale vs the live Lambda set, record the staleness as a finding; reconcile against `infra/aws/lambda/v2_portal/yang_pipeline/`.</if_mismatch>
      </step>
      <step>
        <run>(YCharts side) none — YCharts is an EXTERNAL system, not in the comp-graph.</run>
        <expect>Documented-none per PRD §5: the YCharts evidence base is the HAR (jq parse) + live-probe capture.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>(none) — audit deliverable is a committed brief + matrix slice; no code.</run>
        <expect>No py_compile / ruff / ds-precommit gate applies.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>(none) — the WS-2 matrix slice IS the deliverable's self-validation.</run>
        <expect>Matrix-slice completeness is checked by the acceptance criteria.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Coordinate with WS-3 (YALP_MDSRC.003, 0.4.0_DS_ClientPlatform) on the Model Portfolios page SEAM (PRD §4): WS-2 owns the benchmark / model-portfolio-benchmark / ETF-returns / peer-performance analytics surfaces; WS-3 owns model-portfolio PERFORMANCE sourcing. MCP-coordinate so the page is neither double-audited nor dropped; WS-5 reconciles.
    - Consume WS-1's `all_calc_menu` catalog parse + the shared YCharts auth/WAF finding (do not re-probe the auth layer if WS-1 already recorded it).
    - Agree the common migration-matrix-slice schema with WS-1 + WS-3.
    No shared files written (audit-only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Every YCharts analytics / metric / attribution / classification endpoint in scope inventoried with method, params, response schema, data class.</ac>
    <ac id="AC2">Factor Tilts / Positioning / CMA / the Model-Portfolios analytics surfaces enumerated to component + JSON-artifact + rendered-field level, each with source artifact + refresh cadence.</ac>
    <ac id="AC3">Each WS-2 surface classified — YCharts-replaceable / Bloomberg-pkl-only / proprietary / hybrid. Opal-proprietary analytics (`model_pkl` model output, `cma_excel` assumptions) explicitly named Bloomberg-pkl-only/proprietary. Delivered as the WS-2 matrix slice in the common slice schema.</ac>
    <ac id="AC4">Q5 (WS-2 slice): the `all_calc_menu` catalog cross-referenced against the WS-2 per-surface field list; analytics/risk metric-coverage gaps quantified. Q6 answered: `peer_excel` / `attribution_excel` / `cma_excel` surfaces classified YCharts-sourceable or permanently-manual, with evidence.</ac>
    <ac id="AC5">Official YCharts API coverage for the analytics data classes evaluated (Q1/Q7 input); NOT pre-decided.</ac>
    <ac id="AC6">Evidence of the WS-2 ↔ WS-3 Model Portfolios seam coordination (MCP thread or cited brief section).</ac>
    <ac id="AC7">Deliverable is a committed brief `docs/briefs/mdsrc-ws2-portfolio-analytics-audit-20260520.md` + the WS-2 matrix slice. Session log under `org/tier2_senior/0.2.0_DS_PortfolioAnalytics/logs/` (run date) with a Compiler Tools section reproducing each Phase-1 `<run>` + observed result + pass/fail vs `<expect>`, and the documented-none rationale for the YCharts side + Phases 2/3. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - `docs/briefs/mdsrc-ws2-portfolio-analytics-audit-20260520.md` — the WS-2 domain audit brief.
    - The WS-2 slice of the migration-candidate matrix (common slice schema).
    - Session log with a Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT author or change any code, Terraform, Lambda, or portal file — v0.2 is audit-only.</rule>
    <rule>Do NOT pre-decide official-API vs session-scrape (Q1) or the ToS question (Q7).</rule>
    <rule>Do NOT rely on comp-blast for the yang->portal mapping — PRD §5; use PORTAL_DATA_FLOW.md + a portal/src fetch grep.</rule>
    <rule>Do NOT audit model-portfolio PERFORMANCE sourcing or SmartX — that is WS-3; coordinate the Model Portfolios seam, do not cross it.</rule>
    <rule>No emojis in the brief, the matrix, the session log, or any CLI transcript (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
