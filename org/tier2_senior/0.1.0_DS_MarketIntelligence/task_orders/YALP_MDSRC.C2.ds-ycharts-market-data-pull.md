<task_order>
  <metadata>
    <id>YALP_MDSRC.C2</id>
    <slug>ds-ycharts-market-data-pull</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <co_owner>0.2.0_DS_PortfolioAnalytics — owns the WS-2 hybrid-input legs (see scope). COO finalizes at dispatch whether C2 ships as one TO with a co-owner or is split C2a (0.1.0_DS / WS-1 surfaces) + C2b (0.2.0_DS / WS-2 inputs).</co_owner>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED — Phase 2C. GATED on the Andrew Q1 decision (PRD v0.3 §8) AND on TO-C1 (the credential pipeline this pull authenticates through). On Q1 + TO-C1 RAVC-complete: COO finalizes the one-TO-vs-C2a/C2b split, flips status->pending + fires the GO. Requires PRD v0.3 on origin/CLOUD.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2C. The market-data pull that feeds the 7 YCharts-replaceable + the YCharts-input legs of the 10 hybrid surfaces.</priority>
    <sla>~5-8 days (PRD §7).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. This TO = §7 Phase 2C TO-C2. Read §5.2 (the 32-surface matrix — the 7 replaceable + 10 hybrid rows), §5.3 (the WS-2/WS-3 column seam).</prd>
    <ws1_brief>docs/briefs/mdsrc-ws1-external-market-data-audit-20260520.md + matrix slice — WS-1 surfaces + the YCharts endpoint inventory.</ws1_brief>
    <ws2_brief>docs/briefs/mdsrc-ws2-portfolio-analytics-audit-20260520.md + matrix slice — the WS-2 hybrid-input legs.</ws2_brief>
    <ticker_map>docs/briefs/mdsrc-ycharts-ticker-map-and-fidelity-20260520.{md,csv} (commit dc01d4b8a, origin/CLOUD) — the 71-row portal-entity -> Bloomberg-ticker -> YCharts-symbol crosswalk + per-ticker portal_1Y-vs-ycharts_1Y fidelity. UNLOCK (DS 0.1.0 overnight recon): the variant-pinning question is RESOLVED at source — Yang's data_pkl (`s3://opal-data-portal-v2/benchmarks/data_20260519_v1.pkl`) carries a `bbg_ticker` column giving all 71 entities their exact Bloomberg ticker; the "ask Yang / AE 0.5.0 consult" dependency is REMOVED. The C2 ticker-map work is now a DETERMINISTIC per-ticker identity crosswalk (44 fidelity-verified, ~27 to pin) — not a research problem. data_pkl also carries `return`+`price_return` (TR-vs-PR basis resolved at source) and the Valuation `return_monthly` fields. NOTE: YCharts has no Bloomberg-ticker crosswalk (MXKR -> 404; YCharts namespace is ^-symbols) — the crosswalk is per-ticker identity mapping.</ticker_map>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 §7 Phase 2C — build the YCharts pull that feeds: the 7 YCharts-replaceable surfaces (WS1-DDB-01, WS1-MO-01..05, WS1-VAL-01, WS2-MP-04) AND the YCharts-input legs of the 10 hybrid surfaces (the inputs migrate to YCharts; the Opal computation stays). Q1-gated — the pull authenticates via the TO-C1 credential pipeline, whose shape depends on Q1.
  </context>

  <scope>
    <in_scope>
      - Build the YCharts pull feeding the 7 YCharts-replaceable surfaces + the YCharts-input legs of the 10 hybrid surfaces (PRD §5.2 matrix).
      - WS-1 surfaces (0.1.0_DS): incl. the 71-entity ticker -> YCharts-symbol map (WS1-DDB-01) and the per-indicator Bloomberg-ticker -> FRED/YCharts macro mapping (WS1-MAC-01).
      - WS-2 hybrid-input legs (0.2.0_DS co-owner): the YCharts-input side of the regime/correlation/ERP/factor-spread/benchmark-blend/peer surfaces — Opal computation unchanged.
      - The pull authenticates via the TO-C1 credential pipeline (do not build a parallel auth).
      - Per PRD §5.3: the model_portfolio_benchmarks/timeseries benchmark columns are C2's; the model columns are TO-B1's (SmartX) — coordinate the dual-sourced-producer shape with TO-B1.
    </in_scope>
    <out_of_scope>
      - The credential pipeline — TO-C1.
      - The model-portfolio performance columns — TO-B1 (SmartX).
      - The yang-pipeline cutover — TO-D1.
      - The Opal-side computation of the hybrid surfaces — unchanged; this TO only re-sources the inputs.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the build">
      <step>
        <run>comp-routes behaviors  +  comp-routes trace for each in-scope serving path</run>
        <expect>The serving paths for the WS-1/WS-2 surfaces confirmed (PRD §10: WS-1 corrected the path to /api/general/* — PORTAL_DATA_FLOW.md is stale).</expect>
        <if_mismatch>Document any serving-path delta; RAVC1 COO.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io &lt;each gold/generator script touched&gt;</run>
        <expect>Load list + COLUMN GAPS + portal consumers for each producer the pull feeds.</expect>
        <if_mismatch>Fall back to source read for any non-node script + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>CLAUDE.md Rule 14 pre-commit gate (.tools/ds-commit-gate.sh) on every .py</run>
        <expect>py_compile + ds-precommit-check + ruff py39 all exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast &lt;each changed producer function&gt;</run>
        <expect>No unexpected new downstream node from the re-sourcing.</expect>
        <if_mismatch>Flag a new downstream node to COO before signalling done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    TO-C1 (credential pipeline — auth dependency). TO-B1 (the model_portfolio_* dual-sourced-producer seam, PRD §5.3 — coordinate the artifact shape). 0.2.0_DS_PortfolioAnalytics co-owns the WS-2 hybrid-input legs. Portal DE/RD (Pods 1+2): if a migrated artifact's shape changes, that is a per-page coordination — enumerate it. COO finalizes the one-TO-vs-split at dispatch.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The YCharts pull feeds all 7 YCharts-replaceable surfaces + the YCharts-input legs of the 10 hybrid surfaces, authenticating via the TO-C1 pipeline.</ac>
    <ac id="AC2">The 71-entity ticker->YCharts-symbol map (WS1-DDB-01) + the per-indicator Bloomberg->FRED/YCharts macro mapping (WS1-MAC-01) delivered.</ac>
    <ac id="AC3">The model_portfolio_* benchmark-column shape coordinated with TO-B1 per the §5.3 dual-sourced-producer reconciliation.</ac>
    <ac id="AC4">Compiler mandate runs reproduced in the session log. Deliverable committed + push-confirmed on origin/CLOUD. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The YCharts market-data pull (WS-1 + WS-2 hybrid-input legs); the two ticker/indicator maps.
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT start before Andrew rules Q1 + TO-C1 is RAVC-complete — the pull authenticates through TO-C1.</rule>
    <rule>Do NOT change the Opal-side computation of the hybrid surfaces — re-source the inputs only.</rule>
    <rule>Do NOT cut any surface over to YCharts in this TO — the cutover is TO-D1 (behind a parallel-run diff gate). This TO builds the pull; D1 switches surfaces.</rule>
    <rule>No emojis in code, briefs, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
