<task_order>
  <metadata>
    <id>YALP_MDSRC.001</id>
    <slug>ds-ws1-external-market-data-domain-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO FIRED 2026-05-20 — Andrew GO received; COO dispatched. Original gate: STAGED — Phase 0 audit, unblocked on Andrew GO (PRD v0.2 §9/§11: the four Phase-0 audits dispatch in parallel on Andrew GO). No inter-TO dependency — TO-1..4 are fully parallel. On GO: COO flips status->pending + dispatch_held=false + fires the GO message.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct (CEO interview 2026-05-20). WS-1 is the "can YCharts replace the Bloomberg data_pkl market feed" core of the audit. DS 0.1.0 is already engaged on the HAR per Andrew.</priority>
    <sla>~2-4 effort-days (PRD §9). Investigation TO; parallel with TO-2/3/4.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2 (1.0.0_SA_CTO). This TO = WS-1 / §8 TO-1. v0.2 re-cut the audit into three DS domain audits — read the §16 Amendment history, §3 (CTO HAR findings), §3.3 (endpoint inventory), and §4 (domain-seam declarations) before scoping.</prd>
    <recon_doc>docs/briefs/ycharts-bloomberg-portal-data-sourcing-audit-20260520.md (commit 3987616d8) — DS 0.1.0's own independent Phase-0 recon brief; the recon doc-of-record.</recon_doc>
    <har>C:\Users\AndrewBerman\Downloads\ycharts.com.har — 92 MB, 1,894 entries. Primary evidence base. Several HAR response bodies were NOT saved — fill those schemas by live-probe capture.</har>
    <pipeline_docs>infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md + data/yang_pkl/docs/CLOUD_PIPELINE_ARCHITECTURE.md — the yang manifest -> Step Functions -> ~18 Lambdas -> portal-JSON flow (the yang->portal map; PRD §5 confirms this is NOT in the comp-graph).</pipeline_docs>
  </references>

  <context>
    YALP_MDSRC determines, surface by surface, which portal market-data surfaces (today fed by the manual Bloomberg-pkl yang-pipeline) could move to a daily automated YCharts pull. PRD v0.2 (Andrew-direct, pre-dispatch) split the audit into THREE parallel DS domain audits — too large for one DS. WS-1 owns the EXTERNAL MARKET DATA domain end-to-end: (a) the YCharts backend capability for market-data classes, (b) the portal surfaces in that domain, (c) the per-surface source classification. v0.2 authorizes NO code/Terraform/portal change — this is an audit deliverable (committed brief + matrix slice).
  </context>

  <scope>
    <in_scope>
      End-to-end audit of the EXTERNAL MARKET DATA domain:
      - (a) YCharts capability — deep-parse the HAR for the market-data endpoints (`/indices/table_data`, `/indices/asset_class/root/index_list`, `/indices/families/{Family}` incl. Bloomberg, `/indices/{^TICKER}`, `/charts/general_data.json`, `/charts/fund_data.json`, `/dashboard/fund_chart_module_data/{id}`, `/classifications/sectors.json` for sectors, macro/VIX). Live-probe to fill response schemas the HAR did not save. Cross-reference the `static.ycharts.com/calculations/all_calc_menu.json` 3 MB catalog for market-data metrics (Q5, WS-1 slice). Evaluate the official YCharts API product for these data classes — coverage, pricing, rate limits, ToS (Q1/Q7 input).
      - (b) Portal surfaces — inventory Market Overview, Valuation (risk-premium = WS-1 primary; flag any portfolio-analytics dependency to WS-2 per the §4 seam, do NOT re-scope), Correlation, Macroeconomics, plus the DynamoDB `opal-portal-market-data` daily price series (entity types INDEX/ETF/BOND_INDEX/CREDIT/YIELD/COMMODITY/VOLATILITY). Each to the component / JSON-artifact / rendered-field level, with source artifact + refresh cadence.
      - (c) Per-surface source classification — YCharts-replaceable / Bloomberg-pkl-only / hybrid, with endpoint evidence. This is the WS-1 slice of the migration-candidate matrix; use the common matrix-slice schema (coordinate the schema with WS-2/WS-3 so the three slices compose at WS-5).
    </in_scope>
    <out_of_scope>
      - NO code, Terraform, Lambda, or portal change (v0.2 is audit-only).
      - Portfolio-analytics surfaces (Factor Tilts, Positioning, CMA, Model-Portfolios analytics) — WS-2 (TO-2).
      - Model-portfolio performance sourcing + SmartX + client-facing data — WS-3 (TO-3).
      - The operational/credential pattern — WS-4 (TO-4).
      - Finalized migration verdicts across domains — WS-5 (TO-5) synthesizes.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the audit">
      <step>
        <run>comp-routes behaviors</run>
        <expect>Confirms the serving path for the WS-1 pages: `/api/public/json*` + `/json-tiered/*` -> S3 `opal-data-portal-v2` via the `public-data-router` Lambda@Edge (PRD §5). Anchor the per-surface serving-path column to this.</expect>
        <if_mismatch>If the observed path differs from PRD §5, document the delta as an audit finding + RAVC1 to COO.</if_mismatch>
      </step>
      <step>
        <run>(yang->portal mapping) map via infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md + a portal/src fetch-path grep — DO NOT use comp-blast.</run>
        <expect>PRD §5 confirmed the yang generator Lambdas have NO comp-graph downstream edges (the path is S3-file-mediated). PORTAL_DATA_FLOW.md + the portal fetch grep is the authoritative map.</expect>
        <if_mismatch>If PORTAL_DATA_FLOW.md is stale vs the live Lambda set, record the staleness as a finding; reconcile against `infra/aws/lambda/v2_portal/yang_pipeline/`.</if_mismatch>
      </step>
      <step>
        <run>(YCharts side) none — YCharts is an EXTERNAL system, not in the comp-graph.</run>
        <expect>Documented-none per PRD §5 honest-scope note: the YCharts evidence base is the HAR (jq parse) + live-probe capture, not a comp-* tool.</expect>
        <if_mismatch>N/A — no compiler surface exists for an external system.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>(none) — audit deliverable is a committed brief + matrix slice; no code.</run>
        <expect>No py_compile / ruff / ds-precommit gate applies — no .py authored.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>(none) — the WS-1 matrix slice IS the deliverable's self-validation.</run>
        <expect>Matrix-slice completeness is checked by the acceptance criteria, not a compiler tool.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - If WS-1 is the FIRST domain audit to reach the YCharts auth/WAF layer while probing, record the empirical auth/WAF finding (Q3 — does the WAF defeat headless capture) and SHARE it with WS-2 / WS-3 / WS-4 via MCP. Do not let the auth probe be triplicated (PRD §4 / §7).
    - Share the `all_calc_menu` 3 MB catalog parse with WS-2 (YALP_MDSRC.002) — both filter it to their own data classes.
    - Agree the common migration-matrix-slice schema with WS-2 + WS-3 so the three slices compose cleanly at WS-5.
    - Valuation risk-premium: WS-1 primary; if a portfolio-analytics dependency surfaces, FLAG to WS-2 — do not re-scope into WS-1.
    No shared files written (audit-only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Every YCharts market-data endpoint in scope inventoried with method, query/POST params, response schema, response size, data class. HAR bodies not saved are filled by live-probe capture (method + date documented).</ac>
    <ac id="AC2">Market Overview / Valuation / Correlation / Macroeconomics enumerated to component + JSON-artifact + rendered-field level, each with source artifact + refresh cadence; the DynamoDB `opal-portal-market-data` price series characterized (entity types, grain, cadence).</ac>
    <ac id="AC3">Each WS-1 surface classified — YCharts-replaceable / Bloomberg-pkl-only / hybrid — with endpoint evidence. Delivered as the WS-1 slice of the migration-candidate matrix in the common slice schema.</ac>
    <ac id="AC4">Official YCharts API coverage for the market-data data classes evaluated (coverage vs scrape, pricing, rate limits, ToS) — Q1/Q7 input for the WS-5 consolidation; NOT pre-decided.</ac>
    <ac id="AC5">Q5 (WS-1 slice): the `all_calc_menu` catalog cross-referenced against the WS-1 per-surface field list; market-data metric-coverage gaps quantified.</ac>
    <ac id="AC6">If WS-1 reached the auth layer first, the shared auth/WAF finding (Q3) is recorded + MCP'd to WS-2/3/4. The matrix slice uses the schema agreed with WS-2/WS-3.</ac>
    <ac id="AC7">Deliverable is a committed brief `docs/briefs/mdsrc-ws1-external-market-data-audit-20260520.md` + the WS-1 matrix slice. Session log under `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/` (run date) with a Compiler Tools section reproducing each Phase-1 `<run>` + observed result + pass/fail vs `<expect>`, and the documented-none rationale for the YCharts side + Phases 2/3. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - `docs/briefs/mdsrc-ws1-external-market-data-audit-20260520.md` — the WS-1 domain audit brief.
    - The WS-1 slice of the migration-candidate matrix (common slice schema).
    - The shared auth/WAF finding + `all_calc_menu` parse, if WS-1 produced them first (MCP'd to peers).
    - Session log with a Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT author or change any code, Terraform, Lambda, or portal file — v0.2 is audit-only.</rule>
    <rule>Do NOT pre-decide official-API vs session-scrape (Q1) or the ToS question (Q7) — surface evidence; the decision is Andrew + CTO at v0.3.</rule>
    <rule>Do NOT rely on comp-blast for the yang->portal mapping — PRD §5; use PORTAL_DATA_FLOW.md + a portal/src fetch grep.</rule>
    <rule>Do NOT re-scope portfolio-analytics surfaces into WS-1 — flag the §4 seam to WS-2.</rule>
    <rule>No emojis in the brief, the matrix, the session log, or any CLI transcript (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
