<task_order>
<metadata>
  <to_id>YALP_MACROS.001</to_id>
  <project>YALP_MACROS</project>
  <title>Macroeconomics endpoint + field mapping (Level 1; 4 components)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <closure_ship>3effd8667 (brief shipped 2026-05-26 ~17:50Z; 5/5 ACs met; ws COO RAVC2-ACCEPT ~18:30Z)</closure_ship>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~16:15Z YALP per-page parallelization mandate; Wave-1 Pod-1)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.2 (SELF-CORRECTION-UPSTREAM amendment ~17:05Z per DS 0.1.0~A pre-scaffold structural finding — VolatilityTab added as 4th component). Full scope + methodology + compiler mandates in PRD §1 + §2 + §3 + §6.</ref>
    <ref type="methodology_template">YALP_MKTOVR.001 (COMPLETE 2026-05-26 cc4a3d575; 50min wall GO→ship; 8/8 ACs; 0 DRIFT) — mirror verbatim for this per-page probe.</ref>
    <ref type="predecessor">YALP_MDSRC L1 lineage map `docs/reference/yang-pipeline-lineage-map.md` §5a/§6 — Macroeconomics page yang-side upstream resolution baseline.</ref>
    <ref type="andrew_quote">"this process [YALP_MKTOVR], exactly how we did it for MKTOVR, has to be done the exact same way for each of the Portal UI pages... parallelize... DS tilde-serializing ~A ~B etc as needed".</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT (read-only verification scope per PRD §0 + YALP class). MSTR /allocation #10 P1 spawn fulfilled 2026-05-26T16:30Z; lane-correction `02519793e` confirms ~A canonical (Pod-1 unchanged).</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD §1 + YALP_MKTOVR Level-1 methodology: enumerate every field rendered by each of the 4 Macroeconomics page components; trace endpoint → S3 key → pipeline producer → upstream source → YCharts equivalent (or `n/a` with reason). Populate Level-1 table inline in `docs/briefs/yalp_macros_macroeconomics_field_comparison_<T*>.md` (draft state; STANDBY-PREP scaffold may already exist per parallel-consult discipline). Level-2 placeholder for TO-004.

**4 components in scope (PRD v0.2):**
1. **YieldCurveTab** — UST 2Y/5Y/10Y/30Y yields + 2Y-10Y spread; `macro_data.json` Treasury fields (yang-pipeline).
2. **MacroHeatmap** — macro indicator grid (CPI, Core CPI, unemployment, housing starts, PMI, etc.); `macro_data.json` macro series block (yang-pipeline).
3. **MacroTimeSeriesModal** — per-indicator historical chart on click; `macro/timeseries/{slug}.json` dynamic per-series files (yang-pipeline).
4. **VolatilityTab** — VIX + MOVE with toggle/speedometer/AI summary/historical chart; `json/macro/volatility_data.json` produced by `opal-portal-volatility-fetcher` (**market-overview pipeline; NOT yang**); VIX from FRED `VIXCLS` + MOVE from Yahoo Finance external.

**Out of scope** (per PRD §1): `json/macro/vix_data.json` (yang orphan, no active consumer); `json/yang/volatility_data.json` (yang orphan, no active consumer).

**This is mapping work, NOT cutover.** Deliverable is brief doc; no portal/pipeline edits. DRIFT-routing rule from YALP_MKTOVR carries forward — material DRIFT findings route via close-MCP to CTO + COO + Andrew for future-project scoping; do NOT absorb into THIS project scope.

**T* placeholder:** TO-001 may leave `<T*>` symbolic until TO-003 resolves. T*=2026-05-22 likely inherited from YALP_MKTOVR per Andrew shared-date guidance; DS 0.2.0 TO-003 consult confirms.

**YCharts equivalents:** if a field has no direct YCharts equivalent, populate with explicit `n/a — <reason>`. No blanks.
</scope>

<acceptance_criteria>
- AC1: Every rendered field on all 4 components has a Level-1 row populated in the brief doc.
- AC2: YCharts-equivalent column is either a real endpoint+field OR an explicit `n/a — <reason>` (no blanks).
- AC3: Per-component sub-section in the brief documents the methodology evidence per field (which compiler tool surfaced it).
- AC4: Brief doc Level-2 table is an empty placeholder (no value comparison this TO — that's TO-004).
- AC5: VolatilityTab row notes market-overview-pipeline upstream (NOT yang); upstream provenance via FRED `VIXCLS` (VIX) + Yahoo Finance (MOVE) external sources distinguished from yang-pipeline producer chain.
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before brief write) — PRD §6 explicit (mirrors YALP_MKTOVR.001 §5):**
- `comp-platinum page Macroeconomics` — surface every S3 key the page consumes (includes VolatilityTab market-overview key).
- `comp-routes trace /api/general/macro/...` — full CF → auth → S3 path per endpoint (macro_data, timeseries/{slug}, volatility_data).
- `comp-platinum reverse json/macro/macro_data.json` + `json/macro/timeseries/{slug}.json` + `json/macro/volatility_data.json` — per-S3-key consumer surfacing; confirm 4-component active-consumer set.
- `comp-blast` on `yang-generate-macro` + `yang-generate-macro-timeseries` + `opal-portal-volatility-fetcher` — Lambda producer surface area.
- `comp-pipescript io` on each producer Lambda — column gaps + portal consumers sanity check.

**Phase 2 (before brief commit):**
- `comp-transform fields Macroeconomics` (+ subcomponents YieldCurveTab + MacroHeatmap + MacroTimeSeriesModal + VolatilityTab) — confirm field-rendering surface area matches brief enumeration.

**Phase 3 (after brief commit):**
- Session log with Compiler Tools section per `org/ref/SESSION_LOG_STANDARD.md`.
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MDSRC predecessor:** D2/D3 lineage map (`docs/reference/yang-pipeline-lineage-map.md` §5a/§6) is baseline. Re-use heavily; macro surface depth well-mapped.
- **DRIFT-routing rule (carry into TO-004 dependencies):** if downstream TO-004 surfaces material DRIFT findings (cutover-blocker class), route via RAVC2 close-MCP to CTO + COO + Andrew for future-project scoping. Do NOT absorb into this project's scope.
- **Lane: 0.2.0_DS_PortfolioAnalytics consult on TO-003** (yang-pipeline + market-overview-pipeline publication-timing; shared-date `T*` determination ~30min).
- **AE 0.7.0 on-call** — likely zero touch; flag if `opal-portal-volatility-fetcher` Lambda surfaces IAM / invocation gaps unexpectedly.
- **VolatilityTab provenance flag:** v0.2 amendment routed from self-correction-upstream (DS 0.1.0~A pre-scaffold catch); brief §11 documents the source-pipeline distinction for completeness.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the brief doc creation
- Brief doc path: `docs/briefs/yalp_macros_macroeconomics_field_comparison_<T*>.md` (STANDBY-PREP scaffold may pre-exist per `[[standby-prep-compress-to-delivery-when-context-sufficient]]`)
- Level-1 table populated for all 4 components
- Compiler-tools section in session log
- Identification of any cross-pipeline dependencies surfaced by `comp-blast` (TO-002 / TO-003 input)
</expected_evidence>

<notes>
This TO is dispatched per MSTR /mstr-spawn fulfillment of ws COO /allocation #10 BATCHED-MULTI-SPAWN P1 ask 2026-05-26T16:26Z (Andrew direct sovereign ~16:15Z YALP per-page Wave-1 charter). MSTR's spawn-message hint cites COO as dispatch authority + ws CTO as architectural-questions chain. Lane-correction `02519793e` 16:24Z confirms ~A canonical (Pod-1 unchanged); sibling ~B/~C/~D/~E reverted to DS 0.2.0~A-D per Andrew Pod 2 routing.

**TO sequence per PRD §4 (for situational awareness; only TO-001 is GO this cycle):**
- TO-001 (THIS): Level 1 endpoint + field mapping (~2-3h)
- TO-002: YCharts test-pulls on TO-001 endpoints (~1-2h; cookie stale → use most-recent corpus pulls)
- TO-003: Shared-date `T*` determination (~30min; parallel; DS 0.2.0 consult)
- TO-004: Level 2 value comparison + per-field verdicts MATCH/REPRESENTATIVE/DRIFT/GAP (~3-5h)
- TO-005: Side-by-side spreadsheet finalize (CSV + markdown; ~1-2h)
- TO-VAL: Consolidated deliverable RAVC2 + CVO surface-pass (~1-2h)

I'll author TO-002 / TO-003 just-in-time after TO-001 RAVC2-Request to avoid stale-narrative risk per `feedback_drive_read_json_not_registry.md`.

If scope ambiguity in PRD §1 / §2 / §3, route to ws CTO (1.0.0_SA_CTO; PRD author). Dispatch / RAVC2 / status questions → me.

**YCharts shared cookie:** per Andrew direct, use existing menachem-bundled cookie via dormant C2 module pull paths or use most-recent successful pulls from corpus. Session-eviction tolerance per `project_ycharts_dedicated_seat_403_session_eviction.md` — 403 = session eviction, not entitlement gap.

**STANDBY-PREP compression eligible:** DS 0.1.0~A authored YALP_MKTOVR methodology personally (predecessor-as-ground-truth); per `[[standby-prep-compress-to-delivery-when-context-sufficient]]` may compress to delivery same window. Scaffold-then-execute flow accepted; ETA may compress from PRD-estimated upper-bound.

**Fast-lane regime applies:** YALP_MKTOVR achieved ~50min wall GO→ship via STANDBY-PREP/parallel-consult tier. Methodology-author advantage compresses authoring overhead; per-page L1 mapping is mechanical given baseline.
</notes>
</task_order>
