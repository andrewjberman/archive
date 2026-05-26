<task_order>
<metadata>
  <to_id>YALP_MKTOVR.001</to_id>
  <project>YALP_MKTOVR</project>
  <title>Market Overview endpoint + field mapping (Level 1; 6 components)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completed>2026-05-26</completed>
  <closure_ship>cc4a3d575 -- brief `docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md` (389 lines) + session log + auto-appended comp-tools-log. RAVC2-ACCEPT from 2.0.0_SA_COO 2026-05-26 ~14:55Z banking as 2nd fast-lane empirical (~50min wall GO->ship; STANDBY-PREP/parallel-consult tier accelerated). AC1+AC2+AC3+AC4 all met. PRD v0.3 `42cbf164c` DDB-intermediate integration. TO-002/TO-004 next.</closure_ship>
  <priority>HIGH (Andrew sovereign direct priority elevation 2026-05-26 ~14:30Z: "highest priority for Opal as a whole at this stage")</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MKTOVR.md v0.1 canonical commit `63439b288` 2026-05-26 (1.0.0_SA_CTO). Full scope + methodology + compiler mandates in PRD §3.1 + §5 + §6 (TO-001 section).</ref>
    <ref type="predecessor">YALP_MDSRC L1 lineage map `docs/reference/yang-pipeline-lineage-map.md` — yang-side upstream resolution baseline (D2/D3 surface-confirmation). This TO adds value-level confidence onto that baseline.</ref>
    <ref type="andrew_quote">"I don't fully trust that we actually have all endpoints mapped and processed to be able to do a cutover. I need some kind of empirical side by side comparison for each data pull by page, what we get from Bloomberg/Yang-Pipeline versus what we get from YCharts."</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT (read-only verification scope per PRD §0). MSTR /allocation #3 P1 spawn fulfilled 2026-05-26T14:18Z.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD §3.1 Level-1 methodology: enumerate every field rendered by each of the 6 Market Overview components; trace endpoint → S3 key → market-overview pipeline producer → yang-pipeline upstream → YCharts equivalent (or `n/a` with reason). Populate Level-1 table inline in `docs/briefs/yalp_mktovr_market_overview_field_comparison_<T*>.md` (draft state — Level-2 table left as empty placeholder for TO-004).

**6 components in scope:**
1. ExecutiveSummary (Top/Bottom Performers)
2. SentimentGauge — 5 sub-fields: Global RSI + U.S. Regime + Yield Curve + News Sentiment + Fear & Greed
3-6. PerformanceHeatMap × 4 tabs: Equities / FixedIncome / MultiAsset / Commodities

**This is mapping work, NOT cutover.** Output is a deliverable doc; no portal / pipeline edits. Per Andrew explicit direction: empirical side-by-side comparison probe; cutover decisions are future-project scope downstream of this deliverable.

**T* placeholder:** TO-001 may leave `<T*>` symbolic in filename until TO-003 resolves the actual shared-date. Use a working-date placeholder (e.g., `T_TBD` or recent yang-pipeline data.pkl date) until TO-003.

**YCharts equivalents:** if a field has no direct YCharts equivalent (e.g., News Sentiment is gold-chain output from news-pipeline, not Bloomberg/yang-pipeline), populate the YCharts-equivalent column with explicit `n/a — <reason>`. Don't leave blank.
</scope>

<acceptance_criteria>
- AC1: Every rendered field on all 6 components has a Level-1 row populated in the brief doc.
- AC2: YCharts-equivalent column is either a real endpoint+field OR an explicit `n/a — <reason>` (no blanks).
- AC3: Per-component sub-section in the brief documents the methodology evidence per field (which compiler tool surfaced it).
- AC4: Brief doc Level-2 table is an empty placeholder (no value comparison this TO — that's TO-004).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before brief write) — PRD §5 explicit:**
- `comp-platinum page MarketPerformance` — surface every S3 key the page consumes
- `comp-routes trace /api/general/json-tiered/market-overview/...` — full CF → auth → S3 path per endpoint
- `comp-platinum reverse json-tiered/market-overview/*.json` — per-S3-key consumer surfacing
- `comp-blast` on each market-overview pipeline Lambda + yang-pipeline producer Lambda touching affected fields
- `comp-pipescript io` on each market-overview pipeline Lambda — column gaps + portal consumers sanity check

**Phase 2 (before brief commit):**
- `comp-transform fields MarketPerformance` (+ subcomponents) — confirm field-rendering surface area matches brief enumeration

**Phase 3 (after brief commit):**
- Session log with Compiler Tools section per `org/ref/SESSION_LOG_STANDARD.md`
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MDSRC predecessor:** D2/D3 lineage map (`docs/reference/yang-pipeline-lineage-map.md`) is baseline. Re-use heavily; don't re-derive what's already mapped.
- **DRIFT-routing rule (carry into TO-004 dependencies):** if downstream TO-004 surfaces material DRIFT findings (cutover-blocker class), route via RAVC2 close-MCP to CTO + COO + Andrew for future-project scoping. Do NOT absorb DRIFT findings into THIS project's scope. PRD §6 + §7 + §9 explicit.
- **Lane: 0.2.0_DS_PortfolioAnalytics consult on TO-003** (yang-pipeline publication-timing) — flag any TO-001 fields whose `T*` depends on yang-pipeline-side publication cadence so TO-003 can resolve.
- **AE 0.7.0 on-call** — likely zero touch from this TO; flag if any market-overview-pipeline Lambda surfaces IAM / invocation gaps unexpectedly.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the brief doc creation
- Brief doc path: `docs/briefs/yalp_mktovr_market_overview_field_comparison_<T*>.md`
- Level-1 table populated for all 6 components
- Compiler-tools section in session log
- Identification of any cross-pipeline dependencies surfaced by `comp-blast` (TO-002 / TO-003 input)
</expected_evidence>

<notes>
This TO is dispatched per MSTR /mstr-spawn fulfillment of ws COO /allocation v0.1 P1 ask 2026-05-26T14:16Z (event-triggered on YALP_MKTOVR PRD v0.1 ship `63439b288` + Andrew sovereign priority elevation). MSTR's spawn-message hint cites COO as dispatch authority + ws CTO as architectural-questions chain.

**TO sequence per PRD §6 (for situational awareness; only TO-001 is GO this cycle):**
- TO-001 (THIS): Level 1 endpoint+field mapping (~3-5h)
- TO-002: YCharts test-pulls on TO-001 endpoints (~2-3h; gated on TO-001 completion + cookie usability)
- TO-003: Shared-date `T*` determination (~30min-1h; parallel; DS 0.2.0 consult)
- TO-004: Level 2 value comparison + per-field verdicts (~4-6h; gated on TO-001 + TO-002 + TO-003)
- TO-VAL: Consolidated deliverable RAVC2 + CVO surface-pass (~1-2h)

I'll author TO-002 / TO-003 just-in-time after TO-001 RAVC2-Request to avoid stale-narrative risk (banked discipline per `feedback_drive_read_json_not_registry.md`).

If you find scope ambiguity in PRD §3.1 / §5 / §6, route to ws CTO (1.0.0_SA_CTO) — they authored the PRD this cycle. Dispatch / RAVC2 / status questions → me.

YCharts shared cookie: per Andrew direct, use existing menachem-bundled cookie via dormant C2 module pull paths. Session-eviction tolerance per `project_ycharts_dedicated_seat_403_session_eviction.md` — 403 = session eviction, not entitlement gap; recoverable with retry.
</notes>
</task_order>
