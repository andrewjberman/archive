<task_order>
  <metadata>
    <id>YALP_MDSRC.SA1</id>
    <slug>ds-market-intelligence-correlation-surface-assessment</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — WS-B of YALP_MDSRC PRD v0.4 (6543894ce). PRD §6 candidate "TO-S1"; COO renamed to SA1 (the v0.4 surface-assessment series — S1/S2 task codes were already used by the YALP_MDSRC SmartX TOs). Authors in parallel with SA2/SA3/M1. Per-component YCharts-replaceability verdicts cite V1's verified entity matrix — sequence the verdict-finalization behind V1 delivery.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — WS-B page-by-page assessment, 2 of the 8 market-data pages.</priority>
    <sla>~1-2 effort-days — a component-by-component assessment of 2 pages.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md (v0.4, 6543894ce) §2 (current-state architecture table), §6 TO-S1.</prd>
    <yang_docs>infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md + LAMBDA_REGISTRY.md + FILE_SPECIFIC_METADATA.md — the structural guide (PRD §5: the comp graph is thin on yang pages; trace via these + comp-platinum reverse, not page-level comp-trace).</yang_docs>
    <v1>YALP_MDSRC.V1 — the verified 76-entity depth/granularity matrix; every YCharts-replaceable verdict cites it.</v1>
  </references>

  <context>
    WS-B assesses, component by component, every surface of the 8 market-data pages. SA1 covers TWO: Market Intelligence (= Market Overview / MarketPerformance — yang Lambdas market-overview-tiered-generator, market-rsi-tiered-generator, market-regime-classifier; artifacts json-tiered/market-overview/**, json/market/market-regime*.json; Bloomberg input data_pkl) and Correlation (yang-generate-correlation; json/correlations/correlation_data.json; data_pkl). Per component: what it renders -> which json/** artifact + yang Lambda feeds it -> which Bloomberg data_pkl key -> end-state sourcing verdict (YCharts-replaceable / hybrid / stays-Bloomberg) with granularity + depth + fidelity evidence.

    NOTE: Market Overview's sentiment / trending / fear-greed components are fed by separate, already-automated pipelines — flag them out-of-Bloomberg-scope; do NOT migrate them.
  </context>

  <scope>
    <in_scope>
      - Component-by-component, tab-by-tab assessment of the Market Intelligence and Correlation pages.
      - Per component: rendered content -> json/** artifact + yang Lambda -> Bloomberg data_pkl key -> sourcing verdict (YCharts-replaceable / hybrid / stays-Bloomberg), each verdict carrying granularity + depth + fidelity evidence from the V1 matrix.
      - Flag the sentiment/trending/fear-greed components as out-of-Bloomberg-scope (separate automated pipelines) — assessed-and-excluded, not migrated.
      - Deliverable: a committed per-component sourcing assessment for the 2 pages; RAVC2 to COO + CC CTO.
    </in_scope>
    <out_of_scope>
      - Implementing any migration — SA1 is assessment only; migration TOs follow from the v0.4 verdicts.
      - The other 6 pages (SA2/SA3 cover them).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
  Phase 1: comp-platinum reverse on each page's json/** artifact key -> consumer components; cross-ref yang PORTAL_DATA_FLOW.md + LAMBDA_REGISTRY.md + FILE_SPECIFIC_METADATA.md.
  Phase 2: per component, cite the yang Lambda + the data_pkl key read; map each to a YCharts endpoint (or not) using the TO-V1 verified entity matrix.
  Phase 3: every "YCharts-replaceable" verdict carries granularity/depth evidence from TO-V1 — no verdict on assumption.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Consumes V1's verified entity matrix — finalize YCharts-replaceable verdicts only against V1's measured depth/granularity (R3-adjacent: no verdict on assumption).
    - Same owner as V1 (0.1.0_DS) — sequence V1 first, then SA1's verdict-finalization; the assessment scaffolding can proceed in parallel.
    - Assessment-only — no artifact swap, so the R3 consumer-enumeration gate applies to the downstream migration TOs, not SA1.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — every component/tab of the Market Intelligence + Correlation pages assessed; none skipped.
    - AC2 — per component: artifact + yang Lambda + data_pkl key named; sourcing verdict assigned.
    - AC3 — every YCharts-replaceable verdict carries V1 granularity/depth evidence; no verdict on assumption.
    - AC4 — sentiment/trending/fear-greed components explicitly flagged out-of-Bloomberg-scope.
    - AC5 — committed per-component assessment; session log Compiler Tools section; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
