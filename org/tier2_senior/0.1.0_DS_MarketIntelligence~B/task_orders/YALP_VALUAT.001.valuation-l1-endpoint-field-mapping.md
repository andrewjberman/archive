<task_order>
<metadata>
  <to_id>YALP_VALUAT.001</to_id>
  <project>YALP_VALUAT</project>
  <title>Valuation endpoint + field mapping (Level 1; 2 components)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatch this cycle</status>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~16:15Z YALP per-page parallelization mandate; ~17:00Z countermand on 16:45Z lane-correction; AS-SPAWNED tilde-lanes proceed)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_VALUAT.md v0.1 canonical (1.0.0_SA_CTO ws-charter cycle #32). Full scope + methodology + compiler mandates in PRD §1 + §2 + §3 + §6.</ref>
    <ref type="methodology_template">YALP_MKTOVR.001 (COMPLETE 2026-05-26 cc4a3d575; 50min wall GO→ship; 8/8 ACs; 0 DRIFT) — mirror verbatim.</ref>
    <ref type="sister">YALP_MACROS.001 (this same /drive #101 cycle; 4-component scope; PRD v0.2 amendment absorbed VolatilityTab via self-correction-upstream 4th-fire).</ref>
    <ref type="countermand">Andrew sovereign 2026-05-26T~17:00Z: "no dont kill let it go, doesn tmatter its fine" — countermands his 16:45Z lane-correction; operational momentum > lane discipline per MSTR ACK.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT (read-only verification scope). MSTR /allocation #10 P1 spawn-then-respawn fulfilled per Andrew countermand.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD §1 + YALP_MKTOVR Level-1 methodology: enumerate every field rendered by each of the 2 Valuation page components; trace endpoint → S3 key → producer Lambda → upstream → YCharts equivalent (or `n/a` with reason). Populate Level-1 table inline in `docs/briefs/yalp_valuat_valuation_field_comparison_<T*>.md`. Level-2 placeholder for TO-004.

**2 components in scope:**
1. **Valuation main view** (`useValuationData.ts`) — equity/bond valuation series; `valuation_data.json` (`yang-generate-valuation` Lambda; rubric `dc_index` from `data.pkl`).
2. **RiskPremiumTab** — IG + HY OAS spreads + Yang monthly ERP; `risk_premium_data.json` (`yang-generate-risk-premium` Lambda; FRED `BAMLC0A0CM` IG + `BAMLH0A0HYM2` HY + Yang monthly ERP fallback from `data.pkl`).

**Out of scope:** none flagged in PRD §1. Yang ERP is GAP-class (no YCharts equivalent expected; document via `sourcing/methodology` column).

**This is mapping work, NOT cutover.** DRIFT-routing rule from YALP_MKTOVR carries forward.

**T* placeholder:** T*=2026-05-22 likely inherited from YALP_MKTOVR; DS 0.2.0 TO-003 consult confirms.
</scope>

<acceptance_criteria>
- AC1: Every rendered field on both 2 components has a Level-1 row populated in the brief doc.
- AC2: YCharts-equivalent column is either a real endpoint+field OR an explicit `n/a — <reason>` (no blanks).
- AC3: Per-component sub-section in the brief documents the methodology evidence per field (which compiler tool surfaced it).
- AC4: Brief doc Level-2 table is an empty placeholder (no value comparison this TO — that's TO-004).
- AC5: Yang ERP row tagged GAP-class with explicit `sourcing/methodology` documentation (Yang-derived from `data.pkl` per yang-generate-risk-premium Lambda); ICE BofA OAS rows verify-mapped against YCharts FRED-proxy OR direct ICE coverage.
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before brief write):**
- `comp-platinum page Valuation` — surface every S3 key the page consumes.
- `comp-routes trace /api/general/valuation/...` — full CF → auth → S3 path per endpoint.
- `comp-platinum reverse json/valuation/valuation_data.json` + `json/valuation/risk_premium_data.json` — per-S3-key consumer surfacing.
- `comp-blast` on `yang-generate-valuation` + `yang-generate-risk-premium` — Lambda producer surface area.
- `comp-pipescript io` on each producer Lambda — column gaps + portal consumers sanity check.

**Phase 2 (before brief commit):** `comp-transform fields Valuation` (+ RiskPremiumTab) — confirm field-rendering surface area matches brief enumeration.

**Phase 3 (after brief commit):** Session log with Compiler Tools section per `org/ref/SESSION_LOG_STANDARD.md`.
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MDSRC predecessor:** D2/D3 lineage map baseline. Re-use heavily.
- **DRIFT-routing rule:** material DRIFT findings → close-MCP to CTO + COO + Andrew (future-project scope, not absorbed).
- **Lane: 0.2.0_DS_PortfolioAnalytics consult on TO-003** (shared-date `T*` determination ~30min).
- **AE 0.7.0 on-call** — likely zero touch; flag if `yang-generate-valuation` / `yang-generate-risk-premium` surfaces IAM gaps.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the brief doc creation
- Brief doc path: `docs/briefs/yalp_valuat_valuation_field_comparison_<T*>.md`
- Level-1 table populated for 2 components
- Compiler-tools section in session log
- Identification of any cross-pipeline dependencies surfaced by `comp-blast` (TO-002 / TO-003 input)
</expected_evidence>

<notes>
This TO dispatched per Andrew direct sovereign countermand 2026-05-26T~17:00Z reversing his 16:45Z lane-correction. AS-SPAWNED DS 0.1.0~B is canonical for YALP_VALUAT; do NOT route to DS 0.2.0~A. MSTR spawn auth ~17:05Z reaffirms post-countermand.

**TO sequence per PRD §4:** TO-001 (THIS) → TO-002 YCharts pulls → TO-003 shared-date → TO-004 Level-2 verdicts → TO-005 spreadsheet → TO-VAL consolidated.

YCharts shared cookie: per Andrew direct, use most-recent successful pulls from corpus if needed. Session-eviction tolerance per `project_ycharts_dedicated_seat_403_session_eviction.md`.

**Fast-lane regime applies:** YALP_MKTOVR ~50min wall GO→ship. Sister-page YALP_MACROS.001 in parallel-execution.

Scope ambiguity in PRD §1 / §2 / §3 → ws CTO (PRD author). Dispatch / RAVC2 / status questions → me.
</notes>
</task_order>
