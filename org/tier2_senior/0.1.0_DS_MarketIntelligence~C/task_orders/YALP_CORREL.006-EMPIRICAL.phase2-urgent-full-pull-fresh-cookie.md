<task_order>
<metadata>
  <to_id>YALP_CORREL.006-EMPIRICAL</to_id>
  <project>YALP_CORREL</project>
  <title>URGENT Phase 2 / .006-EMPIRICAL — symbol canonicalization + per-ticker bulk pull + pair-correlation derivation; window NOW → tomorrow AM ET</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~C</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — URGENT GO dispatched this cycle</status>
  <priority>URGENT (Andrew sovereign direct 2026-05-26T~22:38Z + ~22:40Z: "we have YCharts cookie we need DS agents who are not doing anything working on CORREL VALUAT FACTOR POSITN ATTRB" + "we only have until tomorrow morning so NOW is the time to assess what we need for everything")</priority>
  <references>
    <ref type="phase1_substrate">YALP_CORREL Phase 1 brief `f386e9370` + cascade `2d7cf02ae` (105-row spreadsheet); RAVC2-accepted `8c946166c`</ref>
    <ref type="t002_validate">YALP_CORREL.002 RAVC2-ACCEPTED `80d9bed66` cookie validated; charts/fund_data 400 endpoint-divergent; YALP_CORREL.006-EMPIRICAL follow-on readiness MET cycle 115</ref>
    <ref type="substitute_doctrine">Andrew sovereign substitute-security ruling [[feedback_persistent_ticker_failure_try_alternative_security]] binding for any persistent-ticker-failures</ref>
    <ref type="cookie_window">AWS Secrets `ycharts/credentials` REFRESHED ~21:55Z; window NOW → tomorrow AM ET</ref>
  </references>
</metadata>

<scope>
**URGENT Phase 2 / YALP_CORREL.006-EMPIRICAL** — execute your 4-phase scope outlined in T002-VALIDATE brief §4 NOW while cookie is fresh:

**Phase A — Symbol canonicalization** (your T002-VALIDATE found 7 hand-curated symbols silent-dropped; needs catalog look-up per LD-31)
**Phase B — Per-ticker price-history bulk pull** (all 59 names from Phase 1 + canonicalized symbol set)
**Phase C — Pair-correlation derivation** (Framing A primary)
**Phase D — 105 INFERRED-MATCH verdict upgrade** + project-close 3-step atomic OR Phase 3 dispatch

**Deliverable:** brief at `docs/briefs/yalp_correl_phase2_empirical_20260526.md`:
- §1 Phase A symbol canonicalization results + LD-31 catalog-verified IDs
- §2 Phase B bulk-pull execution (per-ticker freshness + parseable check; 7-shape verdict per row)
- §3 Phase C pair-correlation derivation (Framing A)
- §4 Phase D 105 INFERRED-MATCH upgrade
- §5 charts/fund_data 400 substitute-security disposition (endpoint-divergent finding from T002-VALIDATE; substitute via different endpoint OR sister-class metric)
- §6 RAVC2 packet

**Apply Andrew sovereign substitute-security ruling** for charts/fund_data 400 + any other persistent failures: substitute-endpoint-search OR substitute-ticker-formulation per closest-to-underlying-first rubric.

**Per CLAUDE.md Rule 14a:** safe-commit.sh --only.
</scope>

<acceptance_criteria>
- AC1: Symbol canonicalization complete with LD-31 catalog-verified IDs.
- AC2: Per-ticker bulk pull (Phase 1 59 names + canonicalized set) executed with fresh cookie.
- AC3: Pair-correlation derivation (Framing A) shipped.
- AC4: 105 INFERRED-MATCH verdicts upgraded per 7-shape taxonomy.
- AC5: charts/fund_data 400 + any other persistent failures → substitute-security-search applied.

**Target ETA: 3-5h wall** per your T002-VALIDATE §4 estimate; sub-3h plausible per cascade-compression.
</acceptance_criteria>

<cross_domain_coordination>
- **Sibling parallel Phase 2 dispatches:** ~B (VALUAT) + ~D (POSITN) + ~E (FACTOR) all firing this cycle URGENT
- **TO-007 cross-source consideration:** YALP_CORREL is correlation-derivation lane; if you need price-history substrate beyond YCharts, FREDAdapter from TO-008 `30bd38cf0` available
- **No formal sub-RAVC2 required** — single integrated commit + RAVC2-Request
</cross_domain_coordination>

<deliverable_disposition>
**RAVC2-Request to ws COO** at completion. Window closes tomorrow AM ET. Sub-3h plausible per cascade-compression.

**Post-RAVC2-ACCEPT:** YALP_CORREL project-close 3-step atomic OR Phase 3 dispatch per recommendation.
</deliverable_disposition>
</task_order>
