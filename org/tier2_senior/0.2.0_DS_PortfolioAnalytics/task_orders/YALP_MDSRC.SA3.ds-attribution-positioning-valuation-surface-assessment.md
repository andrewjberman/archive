<task_order>
  <metadata>
    <id>YALP_MDSRC.SA3</id>
    <slug>ds-attribution-positioning-valuation-surface-assessment</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — WS-B of YALP_MDSRC PRD v0.4 (6543894ce). PRD §6 candidate "TO-S3"; COO renamed to SA3 (surface-assessment series; S1/S2 codes already used by the YALP_MDSRC SmartX TOs). Authors in parallel with SA1/SA2/M1. Same owner as SA2 — SA2 (the headline dual-source deliverable) sequences first; SA3 follows.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — WS-B, 3 of the 8 market-data pages.</priority>
    <sla>~1-2 effort-days — component-by-component assessment of 3 pages.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md (v0.4, 6543894ce) §2, §6 TO-S3.</prd>
    <yang_docs>infra/aws/lambda/v2_portal/yang_pipeline/PORTAL_DATA_FLOW.md + LAMBDA_REGISTRY.md + FILE_SPECIFIC_METADATA.md.</yang_docs>
    <v1>YALP_MDSRC.V1 — the verified YCharts entity matrix (for YCharts-replaceability evidence).</v1>
    <cma_precedent>v0.3 CMA ruling — Capital Market Assumptions stays manual/Bloomberg (Opal proprietary model IP). The precedent for the SA3 proprietary-vs-vendor-replaceable classification.</cma_precedent>
  </references>

  <context>
    SA3 covers THREE pages: Attribution (yang-generate-holdings-attribution; json/positioning/holdings_attribution_data.json; input attribution_excel), Positioning (yang-generate-positioning, yang-generate-allocation-summary; json/positioning/{positioning_data,allocation_summary}.json; data_pkl + model_pkl) and Valuation (yang-generate-valuation, yang-generate-risk-premium; json/valuation/{valuation_data,risk_premium_data}.json; data_pkl).

    These pages MIX inputs — data_pkl, model_pkl, and attribution_excel. The verdict per component must name WHICH input it depends on and whether YCharts (or another source) can replace THAT input. Holdings attribution (attribution_excel) is a manual Excel workbook — SA3 must assess whether that is a Bloomberg dependency (vendor-replaceable) or an Opal-proprietary one (stays manual, per the CMA precedent).
  </context>

  <scope>
    <in_scope>
      - Component-by-component assessment of Attribution, Positioning, and Valuation: rendered content -> json/** artifact + yang Lambda -> Bloomberg input -> sourcing verdict.
      - Per component, NAME the specific Bloomberg input (data_pkl key / model_pkl key / attribution_excel) and the replaceability verdict against it.
      - Classify each verdict: vendor-replaceable (YCharts/another source) vs Opal-proprietary (stays manual, per the CMA precedent). Holdings attribution's attribution_excel gets this classification explicitly.
      - Deliverable: a committed per-component sourcing assessment for the 3 pages; RAVC2 to COO + CC CTO.
    </in_scope>
    <out_of_scope>
      - Implementing any migration — SA3 is assessment only.
      - The other 5 pages (V1/SA1/SA2 cover them).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
  Phase 1: comp-platinum reverse on json/positioning/** + json/valuation/** -> consumer components; cross-ref the yang docs.
  Phase 2: per component, name the Bloomberg input (data_pkl key / model_pkl key / attribution_excel) + the replaceability verdict.
  Phase 3: classify each verdict — vendor-replaceable vs Opal-proprietary (proprietary stays manual, per the CMA precedent).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Consumes V1's verified YCharts entity matrix for YCharts-replaceability verdicts — no verdict on assumption.
    - Same owner as SA2 (0.2.0_DS) — SA2 sequences first (it carries the headline dual-source deliverable); SA3 follows.
    - Assessment-only — the R3 consumer-enumeration / no-regression gate applies to the downstream migration TOs the verdicts spawn, not SA3.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — every component of Attribution + Positioning + Valuation assessed; none skipped.
    - AC2 — per component: the specific Bloomberg input named (data_pkl key / model_pkl key / attribution_excel) + the replaceability verdict.
    - AC3 — each verdict classified vendor-replaceable vs Opal-proprietary; attribution_excel explicitly classified.
    - AC4 — YCharts-replaceable verdicts carry V1 evidence; no verdict on assumption.
    - AC5 — committed per-component assessment; session log Compiler Tools section; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
