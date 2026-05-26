<task_order>
<metadata>
  <to_id>YALP_MACROS.013</to_id>
  <project>YALP_MACROS</project>
  <title>T002-VALIDATE: re-pull all YALP_MACROS YCharts test endpoints with FRESH cookie before colleague re-takes seat tomorrow AM ET</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — URGENT GO dispatched this cycle</status>
  <priority>URGENT (Andrew sovereign direct ~21:54Z via ws CTO; time-pressure window NOW → tomorrow AM ET before colleague re-takes single-session seat per [[project_ycharts_dedicated_seat_403_session_eviction]])</priority>
  <references>
    <ref type="cookie_refresh">AWS Secrets Manager `ycharts/credentials` REFRESHED ~21:55Z; all 6 key cookies PRESENT + structurally valid; source Andrew HAR `ycharts.com(mchm).har` 24.9MB</ref>
    <ref type="phase1_substrate">YALP_MACROS Phase 1 TO-002 results appendix `e6321011b` brief §11 (3-class structural findings: column-validity gap + Alyssa-concurrent-login session-eviction + macro-class symbol-resolution gap)</ref>
    <ref type="parallel_dispatch">5 YALP T002-VALIDATE TOs fired this cycle 114 — sibling lanes ~B (VALUAT) + ~C SPAWN-NEEDED (CORREL) + ~D (POSITN) + ~E (FACTOR); PARALLEL execution authorized by Andrew direct "no queue/sequencing"</ref>
  </references>
  <dependencies>
    <dependency>None — fresh cookie is in AWS Secrets Manager `ycharts/credentials` ready for pull</dependency>
    <dependency>Does NOT block YALP_MACROS.008 multi-source RE harness build (parallel sub-thread; T002-VALIDATE is lightweight sweep)</dependency>
  </dependencies>
</metadata>

<scope>
**Re-pull all YALP_MACROS YCharts test endpoints from Phase 1 with FRESH cookie** to validate that:
1. Previously-403'd endpoints now succeed (cookie session-eviction class resolved)
2. Previously-200 endpoints still succeed (no endpoint-class drift)
3. macro-class symbol-resolution gaps documented in Phase 1 §11 still GAP (not cookie-related)

**Endpoint scope:** all Phase 1 TO-002 test endpoints from your brief `e6321011b` §11 — YieldCurveTab + MacroHeatmap + MacroTimeSeriesModal + VolatilityTab YCharts surface, T*+4d freshness probe class. Use Phase 1 endpoint map verbatim; do NOT re-discover endpoints this turn.

**Output:** brief at `docs/briefs/yalp_macros_t002_validate_fresh_cookie_20260526.md` (~50-150 lines):
- §1 cookie-bundle source verification (cite AWS Secrets Manager `ycharts/credentials` retrieval timestamp)
- §2 per-endpoint validation table (endpoint + HTTP status + parseable Y/N + latency-class)
- §3 failure categorization (session-eviction-RETRY vs endpoint-class-issue vs symbol-resolution-gap-confirmed)
- §4 disposition for Phase 2 TO-008 harness build (does YCharts macro-class surface remain usable for cross-check, or is it deprecated-by-RE-multi-source path per Phase 2 architecture?)

**Coordinate with TO-008 lifecycle:** this TO-013 light-touch sweep can fire IN PARALLEL with TO-008 Wave 1 (FREDAdapter/YahooFinanceAdapter authoring) — read-only test-pulls don't conflict with adapter authoring. Fold into your /work tick OR run as standalone sub-task.

**Per CLAUDE.md Rule 14a:** `.tools/safe-commit.sh --only -- <paths>` for any committed artifacts.
</scope>

<acceptance_criteria>
- AC1: All Phase 1 YALP_MACROS YCharts test endpoints re-pulled with fresh `ycharts/credentials` bundle within the window (NOW → tomorrow AM ET).
- AC2: Per-endpoint HTTP status + parseable check documented.
- AC3: Failures categorized into 3 classes (session-eviction-RETRY / endpoint-class-issue / symbol-resolution-gap-confirmed).
- AC4: Disposition for Phase 2 TO-008 cross-check use documented.

**Pass requires all 4 ACs MET. Light-touch scope — sub-30min plausible.**
</acceptance_criteria>

<compiler_tools_mandate>
N/A — test-pull validation scope (no portal/Lambda code edits).
</compiler_tools_mandate>

<cross_domain_coordination>
- **Sibling YALP T002-VALIDATE lanes parallel:** ~B (VALUAT) + ~C (CORREL SPAWN-NEEDED) + ~D (POSITN) + ~E (FACTOR) per ws CTO Andrew-direct decomposition. Same cookie bundle; same window.
- **Andrew side-thread HARs (parallel substrate-arrival):** Andrew recording HARs for YALP_MACROS Phase 2b HAR-RE candidate list (AAII×2 + Conference Board×2 + NAHB + NAR + UMich + NFIB + TIC = 9 captures). Feeds TO-008 Wave 2; ws CTO will MCP separately when HARs land. NOT in this T002-VALIDATE scope.
- **TO-008 parallel execution:** continue TO-008 Wave 1+3+4 authoring; TO-013 is lightweight side-task NOT preempting TO-008.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing:
- Brief commit hash + path
- AC1-AC4 evidence inline
- TO-008 status (this TO is parallel; TO-008 not blocked)

**Target wall-time ETA:** ~20-30min light-touch sweep. Substantially compressible per cascade-compression pattern (your Phase 1 endpoint map is the substrate; fresh cookie is the only delta).

**Post-RAVC2-ACCEPT:** continue TO-008 multi-source RE harness build.
</deliverable_disposition>

<notes>
- This is a TIME-PRESSURED Andrew-direct validation sweep. Fresh cookie window is rare ([[project_ycharts_dedicated_seat_403_session_eviction]] single-session constraint F1); maximize validation coverage before colleague re-takes seat tomorrow AM ET.
- If any session-eviction-RETRY class fires DURING your pulls, cookie may be evicted mid-window (colleague re-took the seat earlier than expected). Document timestamp + escalate to ws COO immediately for state-check.
- If YCharts macro-class symbol-resolution gaps confirmed (27 variant attempts all 404 per Phase 1 §11), no action — those gaps are the architectural justification for the multi-source RE pivot in Phase 2.
</notes>
</task_order>
