<task_order>
<metadata>
  <to_id>YALP_POSITN.002</to_id>
  <project>YALP_POSITN</project>
  <title>T002-VALIDATE: re-pull all YALP_POSITN YCharts test endpoints with FRESH cookie before colleague re-takes seat tomorrow AM ET</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~D</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — brief e43c93e3c shipped 2026-05-26 ~22:16Z; 4/4 ACs MET; zero deltas vs Phase 1 baseline; IBTF persistence under fresh cookie = doctrine edge-case for sovereign ratification</status>
  <priority>URGENT (Andrew sovereign direct ~21:54Z via ws CTO; time-pressure window NOW → tomorrow AM ET)</priority>
  <references>
    <ref type="cookie_refresh">AWS Secrets Manager `ycharts/credentials` REFRESHED ~21:55Z</ref>
    <ref type="phase1_substrate">YALP_POSITN Phase 1 brief `292218f1f` (Level-1) + .002 `873b36313` (dual-T* YCharts test-pulls 83/84 OK; finding 13a IBTF HTTP 400 + 13b style_ticker H32 GAP) + cascade ship `a52a7ca18` (4943-row spreadsheet)</ref>
    <ref type="parallel_dispatch">5 YALP T002-VALIDATE TOs fired this cycle — sibling lanes ~A (MACROS) + ~B (VALUAT) + ~C SPAWN-NEEDED (CORREL) + ~E (FACTOR)</ref>
  </references>
  <dependencies>
    <dependency>None — fresh cookie ready in AWS Secrets Manager + you LIVE on broker (LD-0107 batch)</dependency>
  </dependencies>
</metadata>

<scope>
**Re-pull all YALP_POSITN YCharts test endpoints from Phase 1 with FRESH cookie** to validate session continuity.

**Endpoint scope:** all Phase 1 TO-001/TO-002 test endpoints from `292218f1f` + `873b36313` + `a52a7ca18` cascade (84 dual-T* pulls + 4943-row spreadsheet). Use Phase 1 endpoint map verbatim.

**Output:** brief at `docs/briefs/yalp_positn_t002_validate_fresh_cookie_20260526.md` (~50-150 lines):
- §1 cookie-bundle source verification + timestamp
- §2 per-endpoint validation table (per-pull HTTP status)
- §3 failure categorization (session-eviction-RETRY / endpoint-class-drift / structural-baseline-match)
- §4 Phase 2 dispatch readiness; specifically re-test finding 13a IBTF HTTP 400 (was style_ticker H32 GAP refinement — cookie-stale-class vs symbol-stale-class per [[feedback_ycharts_http_400_is_cookie_stale_class]] Andrew sovereign 2026-05-26 doctrine)

**Per CLAUDE.md Rule 14a:** safe-commit.sh --only.

**Special focus per [[feedback_ycharts_http_400_is_cookie_stale_class]]:** ws Andrew sovereign 2026-05-26 ruling — YCharts HTTP 400 is cookie-stale class NEVER symbol-stale class. Finding 13a IBTF HTTP 400 from your Phase 1 must re-test under fresh cookie; expected status either 200 (cookie-stale resolved) or persistent 400 with operational refresh+retry sufficient (NOT a symbol-class issue per doctrine).
</scope>

<acceptance_criteria>
- AC1: All Phase 1 YALP_POSITN YCharts test endpoints re-pulled with fresh cookie within window.
- AC2: Per-endpoint HTTP status + parseable check documented.
- AC3: Failures categorized.
- AC4: Phase 1 finding 13a IBTF HTTP 400 specifically re-tested + disposition vs doctrine [[feedback_ycharts_http_400_is_cookie_stale_class]].

**Pass requires all 4 ACs MET. Sub-30min plausible.**
</acceptance_criteria>

<cross_domain_coordination>
- **Sibling lanes parallel:** ~A + ~B + ~C + ~E.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing brief commit + AC1-AC4 evidence.

**Target ETA:** ~20-30min light-touch sweep.

**Post-RAVC2-ACCEPT:** KEEP-EPHEMERAL pending YALP_POSITN Phase 2 dispatch.
</deliverable_disposition>

<notes>
- Per Andrew's doctrine — HTTP 400 in YCharts is cookie-stale class only. T002-VALIDATE confirms 13a IBTF.
- Phase 1's 83/84 OK + 1 13a finding is the baseline; fresh-cookie sweep updates count.
</notes>
</task_order>
