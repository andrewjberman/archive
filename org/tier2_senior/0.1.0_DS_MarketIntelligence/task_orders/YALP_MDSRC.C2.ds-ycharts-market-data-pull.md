<task_order>
  <metadata>
    <id>YALP_MDSRC.C2</id>
    <slug>ds-ycharts-market-data-pull</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <co_owner>0.2.0_DS_PortfolioAnalytics — owns the WS-2 hybrid-input legs (see scope). COO finalizes at dispatch whether C2 ships as one TO with a co-owner or is split C2a (0.1.0_DS / WS-1 surfaces) + C2b (0.2.0_DS / WS-2 inputs).</co_owner>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- RAVC2-ACCEPTED + COMPLETE 2026-05-22 by 2.0.0_SA_COO (joint RAVC2 from 0.1.0_DS + 0.2.0_DS). C2 build-complete + structurally validated (handler runs 7/7 module self-tests) + Andrew-directed live-validated on the Menachem YCharts session (WS-1 71/71 ticker-map symbols resolve; WS-2 per-symbol fidelity PASS). Module infra/aws/lambda/ycharts-market-data-pull/ -- 8 files verified on origin/CLOUD. AC1/AC2/AC4 MET. AC3 (model_portfolio_*/TO-B1 dual-source seam) RE-SCOPED: C2's WS-2 MP module correctly emits only the YCharts benchmark leg -- the model leg is B1/SmartX's domain -- so the dual-source reconciliation is a cross-TO INTEGRATION item, not a C2-build deficiency; folded into D1 (the cutover TO, where the portal consumes the dual source). CARRIED to D1: the AE infra deploy of the C2 Lambda (lambda-source-map.json entry + ycharts-pipeline terraform, deploy dormant per the C1 pattern) + the Crude Oil generator-list alignment (MARKET_OVERVIEW_INDICES bare 'Crude Oil' -> 'Crude Oil WTI'). CARRIED follow-on: VAL-01 valuation-multiple indicator-ID pinning (0.1.0_DS, bounded, Menachem session; ERP-pattern indicator-entity resolution path identified). C2 is the last YALP build TO; D1 is the live cutover, gated on the dedicated YCharts seat. -->
    <!-- GO 2026-05-22 (COO /loop drive). Gates cleared: TO-C1 RAVC2-complete (ycharts-pipeline-v1.1.0, terraform 0-diff, record-deploy 48da66b7c; capture Lambda deployed dormant). Andrew Q1 resolved by the 2026-05-20 reverse-engineer-the-provider-API directive -- the A3 reverse-engineered internal API + the C1 session-capture pipeline IS the chosen path; the official Data API was not pursued. COO finalized the split decision: ONE TO, co-owner model (0.1.0_DS lead = WS-1 surfaces; 0.2.0_DS co-owner = WS-2 hybrid-input legs) -- NOT split into C2a/C2b. FREEZE-AWARE SCOPE: C2 BUILDS + structurally validates the pull module now; it does NOT run live against YCharts -- the YCharts execution freeze holds until the dedicated seat lands (Andrew procurement). Same dormant-build pattern as C1. Sequence per the C3 spec: MP-01/02/03 first (build-ready), FT-02/03 last. Build against the V1B-completed C2 pull-spec (76/76 rows). -->
    <dispatch_unblock_condition>GO ON PICKUP — gates cleared 2026-05-22 (see GO comment above). Build proceeds FREEZE-AWARE: write + structurally validate the pull module, NO live YCharts execution until the dedicated seat lands + the freeze lifts.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2C. The market-data pull that feeds the 7 YCharts-replaceable + the YCharts-input legs of the 10 hybrid surfaces.</priority>
    <sla>~5-8 days (PRD §7).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. This TO = §7 Phase 2C TO-C2. Read §5.2 (the 32-surface matrix — the 7 replaceable + 10 hybrid rows), §5.3 (the WS-2/WS-3 column seam).</prd>
    <ws1_brief>docs/briefs/mdsrc-ws1-external-market-data-audit-20260520.md + matrix slice — WS-1 surfaces + the YCharts endpoint inventory.</ws1_brief>
    <ws2_brief>docs/briefs/mdsrc-ws2-portfolio-analytics-audit-20260520.md + matrix slice — the WS-2 hybrid-input legs.</ws2_brief>
    <ticker_map>docs/briefs/mdsrc-ycharts-ticker-map-and-fidelity-20260520.{md,csv} (commit dc01d4b8a, origin/CLOUD) — the 71-row portal-entity -> Bloomberg-ticker -> YCharts-symbol crosswalk + per-ticker portal_1Y-vs-ycharts_1Y fidelity. UNLOCK (DS 0.1.0 overnight recon): the variant-pinning question is RESOLVED at source — Yang's data_pkl (`s3://opal-data-portal-v2/benchmarks/data_20260519_v1.pkl`) carries a `bbg_ticker` column giving all 71 entities their exact Bloomberg ticker; the "ask Yang / AE 0.5.0 consult" dependency is REMOVED. The C2 ticker-map work is now a DETERMINISTIC per-ticker identity crosswalk (44 fidelity-verified, ~27 to pin) — not a research problem. data_pkl also carries `return`+`price_return` (TR-vs-PR basis resolved at source) and the Valuation `return_monthly` fields. NOTE: YCharts has no Bloomberg-ticker crosswalk (MXKR -> 404; YCharts namespace is ^-symbols) — the crosswalk is per-ticker identity mapping.</ticker_map>
    <c3_input_spec>docs/briefs/mdsrc-ws2-c2-input-spec-20260520.{md,tsv} (commit 3d2d7792e, origin/CLOUD) — YALP_MDSRC.C3, the WS-2 hybrid-surface input-series spec; THIS IS THE C2 BUILD-INPUT for the WS-2 hybrid legs. §4 carries three findings C2 MUST account for: (1) Correlation has 3 GENUINE crosswalk gaps — Bloomberg US Treasury / 1-3 Year Treasury / 7-10 Year Treasury are not in the dc01d4b8a crosswalk + 1-3 Year Treasury must NOT be silently mapped to the crosswalk's "1-3 Year Gov/Credit" row (different index); plus a Crude Oil Brent-vs-WTI variant ambiguity. (2) FT-02/03 — the 6 factor-pair NAMES are documented (FACTOR_NAMES in infra/aws/lambda/v2_portal/yang_pipeline/factor_tilts/yang-generate-factor-tilts/lambda_function.py:32-35 — "Equity vs FI", "Growth vs Value", "US vs Foreign", "Large vs Small", "Agg vs Short", "HY vs Agg"), but the constituent index tickers per leg are NOT in the repo (model.pkl/factor_spread is pre-computed in Yang's manual build). C2 Phase-0 prerequisite (NARROWED per CTO 2026-05-20): not "discover the 6 pairs" but "ratify the exact constituent index ticker for each leg of the 6 named pairs" — most are semantically standard (US vs Foreign ~ S&P 500 vs MSCI EAFE; Large vs Small ~ S&P 500 vs Russell 2000; Growth vs Value ~ the S&P 500 Growth/Value pair), so likely a small ratify-6-picks methodology item (a Yang-consult or an Andrew/methodology ratify), NOT a hard blocker. SEQUENCE FT-02/03 LAST in C2 regardless. (3) MP-01/02/03 is the cleanest, build-ready C2 target (9 public series + documented re-blend weights) — sequence it first.</c3_input_spec>
    <a3_build_spec>docs/briefs/mdsrc-ycharts-internal-api-20260520.md + docs/briefs/mdsrc-ycharts-internal-api-mapping-20260520.tsv (YALP_MDSRC.A3, COMPLETE — commits af5102dd3 / 93721a207 / cff92278c, origin/CLOUD) — THE CANONICAL C2 BUILD SPEC, supersedes the page-level A2 spec. The P3 35-row TSV gives, per requirement: the internal endpoint + method + exact params + the JSON-path-to-value (so C2 reads each datum deterministically). Core structure: the 17 YCharts-served surfaces collapse to ~6 generic entity-agnostic internal JSON endpoints (4 carry the served surfaces — /indices/table_data, /charts/general_data.json, /charts/fund_data.json, /charts/scatter_plot_data.json POST). P4 RESIDUE C2 MUST CLOSE: A3 re-tested the 27 imperfect cases against the internal API — ~16 resolved, but ~10 remain (the ~5 still-wide GSCI-basis + 4 maturity-band bonds, and ~5 genuinely-unmapped 4 commodities + MSCI USA Size). A3's verdict: the residue is NOT missing data — YCharts HAS it — it is a bounded SYMBOL-DISCOVERY + return-basis-pinning task; C2 closes it via the YCharts securities-search UI + a per-symbol fidelity check. Build the C2 pull against the P3 TSV; treat the ~10-case symbol discovery as a defined C2 sub-task, not an open question.</a3_build_spec>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 §7 Phase 2C — build the YCharts pull that feeds: the 7 YCharts-replaceable surfaces (WS1-DDB-01, WS1-MO-01..05, WS1-VAL-01, WS2-MP-04) AND the YCharts-input legs of the 10 hybrid surfaces (the inputs migrate to YCharts; the Opal computation stays). Q1-gated — the pull authenticates via the TO-C1 credential pipeline, whose shape depends on Q1.
  </context>

  <scope>
    <in_scope>
      - Build the YCharts pull feeding the 7 YCharts-replaceable surfaces + the YCharts-input legs of the 10 hybrid surfaces (PRD §5.2 matrix).
      - WS-1 surfaces (0.1.0_DS): incl. the 71-entity ticker -> YCharts-symbol map (WS1-DDB-01). SCOPE TRIM 2026-05-20 (CTO): WS1-MAC-01 (Macroeconomics) is REMOVED from TO-C2 — the macro page + its Bloomberg->FRED mapping is now owned end-to-end by YALP_MDSRC.F1 (the dedicated Macroeconomics/FRED audit, 0.2.0_DS_PortfolioAnalytics~A). C2 does NOT pull macro indicators. If F1 surfaces a macro indicator best sourced from YCharts, F1 flags it back to C2.
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
    <ac id="AC2">The 71-entity ticker->YCharts-symbol map (WS1-DDB-01) delivered. (WS1-MAC-01 macro mapping trimmed to YALP_MDSRC.F1 — not a C2 deliverable.)</ac>
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
