<task_order>
  <metadata>
    <id>YALP_MDSRC.003</id>
    <slug>ds-ws3-client-facing-data-domain-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <completed>2026-05-20</completed>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO FIRED 2026-05-20 — Andrew GO received; COO dispatched. Original gate: STAGED — Phase 0 audit, unblocked on Andrew GO (PRD v0.2 §9/§11: the four Phase-0 audits dispatch in parallel on Andrew GO). No inter-TO dependency — TO-1..4 are fully parallel. On GO: COO flips status->pending + dispatch_held=false + fires the GO message. NOTE: this is a BASE-LANE TO (YALP_MDSRC is a base-lane project); it MCP-coordinates with the ~B MDPF lane but is itself base-lane — base agent 0.4.0_DS_ClientPlatform owns it.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct (CEO interview 2026-05-20). WS-3 resolves where model-portfolio performance is canonically sourced (YCharts vs SmartX vs model.pkl) — a triple-sourcing reconciliation risk if left unaudited.</priority>
    <sla>~2-4 effort-days (PRD §9). Investigation TO; parallel with TO-1/2/4. Includes the mandatory MDPF coordination wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2 (1.0.0_SA_CTO). This TO = WS-3 / §8 TO-3. v0.2 re-cut the audit into three DS domain audits — read §16 Amendment history, §3 (CTO HAR findings), §3.3 (endpoint inventory), §4 (domain-seam declarations), §7 (cross-domain coordination) before scoping.</prd>
    <recon_doc>docs/briefs/ycharts-bloomberg-portal-data-sourcing-audit-20260520.md (commit 3987616d8) — DS 0.1.0's Phase-0 recon brief; the recon doc-of-record.</recon_doc>
    <har>C:\Users\AndrewBerman\Downloads\ycharts.com.har — 92 MB. The YCharts `/model_portfolios/*` endpoints are the YCharts side of the model-portfolio-sourcing question.</har>
    <smartx>data/smartx/ — `SMARTX_API_DOCUMENTATION.md`, the SmartX ingestion scripts, `lambda_smartx_query.py`. The SmartX backend audit target.</smartx>
    <mdpf>MDPF_ASSETS (active, ~B-lane) — SmartX is already a live MDPF data source (`MACRO_CODES.md`: MDPF = "smartx + inf-pipeline + etfs"; `data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py`). WS-3 consumes MDPF's existing SmartX knowledge — see &lt;cross_domain_coordination&gt;.</mdpf>
  </references>

  <context>
    YALP_MDSRC determines, surface by surface, which portal market-data surfaces could move to a daily automated YCharts pull. PRD v0.2 (Andrew-direct, pre-dispatch) split the audit into THREE parallel DS domain audits. WS-3 owns the CLIENT-BASED / CLIENT-FACING DATA domain end-to-end: model-portfolio PERFORMANCE sourcing (the question of where the delivered model-portfolio performance numbers come from — YCharts `/model_portfolios/*`, the SmartX backend, or the yang `model.pkl`), the SmartX backend audit, and any client-tied / per-account portal data surface. SmartX is a CLIENT-ACCOUNT backend and is already a live MDPF_ASSETS data source — so WS-3 MUST consume MDPF's existing SmartX integration knowledge rather than re-derive it, and reconcile any sourcing recommendation with MDPF's model-AUA architecture. v0.2 authorizes NO code/Terraform/portal change — audit deliverable only.
  </context>

  <scope>
    <in_scope>
      End-to-end audit of the CLIENT-BASED / CLIENT-FACING DATA domain:
      - (a) Model-portfolio PERFORMANCE sourcing — characterize what YCharts `/model_portfolios/` `/model_portfolios/list/` `/model_portfolios/collection_status` `/model_portfolios/transition_analysis/list` expose (deep-parse the HAR + live-probe); characterize what the SmartX backend exposes for model-portfolio performance; characterize what the yang `model.pkl` provides. Recommend the CANONICAL source for the portal's model-portfolio performance surfaces (Q4).
      - (b) The SmartX backend audit — grain, cadence, coverage, the API surface (`data/smartx/SMARTX_API_DOCUMENTATION.md`, the ingestion scripts, `lambda_smartx_query.py`).
      - (c) Any client-tied / per-account portal data surface — inventory + classify.
      - This is the WS-3 slice of the migration-candidate matrix in the common slice schema (agree the schema with WS-1/WS-2).
    </in_scope>
    <out_of_scope>
      - NO code, Terraform, Lambda, or portal change (v0.2 is audit-only).
      - External-market-data surfaces — WS-1 (TO-1).
      - Portfolio-analytics surfaces including the Model Portfolios *benchmark / ETF / peer* analytics — WS-2 (TO-2). WS-3 owns model-portfolio PERFORMANCE sourcing only (the §4 seam).
      - The operational/credential pattern — WS-4 (TO-4).
      - Re-deriving the MDPF SmartX integration — CONSUME MDPF's knowledge (see coordination block).
      - Finalized cross-domain migration verdicts — WS-5 (TO-5).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the audit">
      <step>
        <run>comp-pipescript io &lt;script&gt; — for any data/smartx gold-tier script the audit touches.</run>
        <expect>The script's load list + COLUMN GAPS + portal consumers. Use it to characterize the SmartX gold-tier I/O accurately rather than reading the script blind.</expect>
        <if_mismatch>If the script is not a recognized comp-pipescript node, fall back to a direct source read + note it.</if_mismatch>
      </step>
      <step>
        <run>comp-blast &lt;SmartX Lambda node&gt; — e.g. the SmartX query Lambda.</run>
        <expect>Downstream consumers of the SmartX backend. NOTE PRD §5: comp-graph edge coverage may be sparse for this pipeline — if "No nodes" / "No downstream", fall back to a source read of `data/smartx/` + the MDPF feeder.</expect>
        <if_mismatch>Sparse/absent edges -> fall back to source read; record the gap as a finding.</if_mismatch>
      </step>
      <step>
        <run>comp-routes behaviors — for any client-facing portal serving path the audit examines.</run>
        <expect>Confirms the serving path for any client-tied portal surface in scope.</expect>
        <if_mismatch>Document any serving-path delta as an audit finding.</if_mismatch>
      </step>
      <step>
        <run>(YCharts side) none — YCharts is an EXTERNAL system, not in the comp-graph.</run>
        <expect>Documented-none per PRD §5: the YCharts evidence base is the HAR + live-probe capture.</expect>
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
        <run>(none) — the WS-3 matrix slice + sourcing recommendation IS the deliverable's self-validation.</run>
        <expect>Checked by the acceptance criteria.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    MANDATORY — MDPF_ASSETS coordination: SmartX is a live MDPF_ASSETS data source. WS-3 MUST MCP-coordinate with the MDPF lane BEFORE finalizing the model-portfolio sourcing recommendation — consume MDPF's existing SmartX integration knowledge, do NOT re-derive it; reconcile any sourcing call with MDPF's model-AUA architecture. MDPF_ASSETS is a ~B-lane project — this is a base-lane <-> ~B-lane coordination. COO (2.0.0_SA_COO) is threading the handoff: 2.0.0_SA_COO has notified 2.0.0_SA_COO~B so the MDPF lane (DS~B) expects your coordination request. Route the coordination MCP to 0.4.0_DS_ClientPlatform~B (the MDPF SmartX lane) and/or 2.0.0_SA_COO~B; cite the MDPF SmartX feeder `data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py`. Capture the coordination as an MCP thread or a cited brief section (AC requirement).
    Also coordinate with WS-2 (YALP_MDSRC.002) on the Model Portfolios page SEAM (PRD §4): WS-2 owns the benchmark/ETF/peer analytics surfaces; WS-3 owns model-portfolio performance sourcing.
    Consume the shared YCharts auth/WAF finding (do not re-probe the auth layer if a peer audit already recorded it). Agree the common matrix-slice schema with WS-1 + WS-2.
    No shared files written (audit-only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">YCharts `/model_portfolios/*` characterized (what it exposes, grain, schema); the SmartX backend characterized (grain, cadence, coverage, API surface); the yang `model.pkl` model-portfolio content characterized.</ac>
    <ac id="AC2">A concrete CANONICAL-source recommendation for the portal's model-portfolio performance surfaces (YCharts vs SmartX vs model.pkl), reconciled with MDPF_ASSETS's model-AUA architecture — Q4 answered with evidence.</ac>
    <ac id="AC3">Any client-tied / per-account portal data surface inventoried + classified into the WS-3 matrix slice (common slice schema).</ac>
    <ac id="AC4">Evidence of the MANDATORY MDPF_ASSETS coordination — the MCP thread with the MDPF ~B lane, or a cited section of the committed brief documenting what MDPF SmartX knowledge was consumed and how the recommendation reconciles with MDPF's model-AUA architecture.</ac>
    <ac id="AC5">Evidence of the WS-2 ↔ WS-3 Model Portfolios seam coordination (MCP thread or cited brief section).</ac>
    <ac id="AC6">Deliverable is a committed brief `docs/briefs/mdsrc-ws3-client-facing-data-audit-20260520.md` + the WS-3 matrix slice + the model-portfolio-performance sourcing recommendation. Session log under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/` (run date) with a Compiler Tools section reproducing each Phase-1 `<run>` + observed result + pass/fail vs `<expect>`, and the documented-none rationale for the YCharts side + Phases 2/3. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - `docs/briefs/mdsrc-ws3-client-facing-data-audit-20260520.md` — the WS-3 domain audit brief.
    - The WS-3 slice of the migration-candidate matrix (common slice schema).
    - The model-portfolio-performance canonical-source recommendation (Q4).
    - Session log with a Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT author or change any code, Terraform, Lambda, or portal file — v0.2 is audit-only.</rule>
    <rule>Do NOT finalize the model-portfolio sourcing recommendation before the MDPF_ASSETS coordination — it is MANDATORY (PRD §7).</rule>
    <rule>Do NOT re-derive the MDPF SmartX integration — consume MDPF's existing knowledge.</rule>
    <rule>Do NOT cross the Model Portfolios seam into WS-2's analytics surfaces — coordinate it.</rule>
    <rule>Do NOT pre-decide official-API vs session-scrape (Q1) or the ToS question (Q7).</rule>
    <rule>No emojis in the brief, the matrix, the session log, or any CLI transcript (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
