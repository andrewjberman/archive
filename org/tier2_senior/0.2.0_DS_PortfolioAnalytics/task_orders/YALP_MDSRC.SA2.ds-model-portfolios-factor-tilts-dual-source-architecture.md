<task_order>
  <metadata>
    <id>YALP_MDSRC.SA2</id>
    <slug>ds-model-portfolios-factor-tilts-dual-source-architecture</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — WS-B of YALP_MDSRC PRD v0.4 (6543894ce). PRD §6 candidate "TO-S2"; COO renamed to SA2 (S1/S2 task codes were already used by the YALP_MDSRC SmartX TOs). Authors in parallel with SA1/SA3/M1.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — WS-B. HEADLINE v0.4 architecture deliverable: the dual-source model-data abstraction (CTO ruling R2 — Andrew's vendor-lock-avoidance directive).</priority>
    <sla>~2 effort-days — 2-page assessment + the dual-source architecture design.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md (v0.4, 6543894ce) §2, §4 R1/R2/R3, §6 TO-S2.</prd>
    <yang_docs>infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md + LAMBDA_REGISTRY.md + FILE_SPECIFIC_METADATA.md.</yang_docs>
    <b3>YALP_MDSRC.B3 (the SmartX-direct daily-performance upgrade, being reworked to R3-additive) + the SmartX inventory S2 (e2bd44014). SA2 builds on these.</b3>
    <v1>YALP_MDSRC.V1 — the verified YCharts entity matrix (for the YCharts-leg replaceability evidence).</v1>
  </references>

  <context>
    SA2 covers Model Portfolios (yang Lambdas yang-model-portfolio-benchmarks, yang-generate-benchmark-returns, yang-generate-etf-returns, yang-generate-peer-performance; artifacts json/benchmarks/{model_portfolio_benchmarks,model_portfolio_timeseries,benchmark_returns,etf_returns}.json + json/peers/peer_performance.json; inputs data_pkl + model_pkl + peer_excel) and Factor Tilts (yang-generate-factor-tilts; json/factor-tilts/*.json; model_pkl).

    HEADLINE DELIVERABLE (R2): the dual-source model-data architecture. Andrew directive — model data/performance must be sourceable from BOTH YCharts and SmartX (YCharts-preferred, SmartX-alternate) through a source-abstraction layer so neither vendor is a single point of failure. Not "pick one" — build the switch. Both sources feed the same model_portfolio_timeseries.json / model_portfolio_benchmarks.json contract, config-switchable, each independently validated.

    R1 — Q8 revised: SmartX daily-direct (/api/3.1/models/{id}/performance?grouping=daily) is the authoritative realized-performance source; model.pkl is retained as the proprietary design-return view. R3 — model_portfolio_timeseries.json is additive (design-return series full-history retained + SmartX-realized series added); SA2's design must honor that additive contract.
  </context>

  <scope>
    <in_scope>
      - Component-by-component assessment of Model Portfolios + Factor Tilts: rendered content -> json/** artifact + yang Lambda -> Bloomberg input (data_pkl / model_pkl / peer_excel) -> sourcing verdict.
      - HEADLINE — design the dual-source model-data abstraction: a source-abstraction layer where model data/performance is sourceable from YCharts OR SmartX, YCharts-preferred, both feeding the same model_portfolio_timeseries.json / model_portfolio_benchmarks.json contract, config-switchable, each independently validated. Builds on the B3 SmartX-direct work + the R3 additive artifact.
      - Assess whether YCharts can serve the model-performance and factor-tilt series model_pkl currently supplies (cite V1 evidence).
      - Specify dual-source PARITY — how a YCharts-sourced and a SmartX-sourced series are validated equivalent before either serves.
      - Deliverable: the 2-page component assessment + the dual-source architecture design doc; RAVC2 to COO + CC CTO.
    </in_scope>
    <out_of_scope>
      - Implementing the abstraction layer — SA2 is assessment + architecture design; implementation is a follow-on TO.
      - The B3/B4 additive rework itself (0.4.0_DS owns it) — SA2 designs on top of the additive contract, does not redo it.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
  Phase 1: comp-platinum reverse on json/benchmarks/** + json/factor-tilts/** -> consumer components; enumerate every consumer of model_portfolio_timeseries.json (R3 — MDLP_RVVALT + any sibling).
  Phase 2: design the source-abstraction layer; confirm no new React Query cache-key collisions (comp-cache collisions) if the model-data fetch shape changes.
  Phase 3: dual-source parity — the design specifies how a YCharts-sourced and a SmartX-sourced series are validated equivalent before either serves.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - R3 — the model_portfolio_timeseries.json consumer enumeration (comp-platinum reverse) is shared ground with the B3/B4 additive rework (0.4.0_DS). Coordinate directly with 0.4.0_DS so SA2's architecture design and B3's additive artifact agree on the contract shape.
    - Builds on the SmartX inventory (S2, 0.2.0_DS, e2bd44014) + the verified YCharts matrix (V1, 0.1.0_DS) — both inputs to the dual-source replaceability assessment.
    - Same owner as SA3 (0.2.0_DS); SA2 is the headline — sequence it first if capacity forces a choice.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — every component of Model Portfolios + Factor Tilts assessed; per component artifact + yang Lambda + Bloomberg input named; sourcing verdict assigned.
    - AC2 — the dual-source model-data abstraction designed: source-abstraction layer, YCharts-preferred / SmartX-alternate, config-switchable, same artifact contract, R3-additive-compatible.
    - AC3 — dual-source parity method specified — how YCharts-sourced vs SmartX-sourced series are validated equivalent before serving.
    - AC4 — every consumer of model_portfolio_timeseries.json enumerated (comp-platinum reverse); comp-cache collisions clean for any new fetch shape.
    - AC5 — committed assessment + architecture design; session log Compiler Tools section; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
