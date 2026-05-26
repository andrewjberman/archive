<task_order>
<metadata>
  <to_id>YALP_FACTOR.002</to_id>
  <project>YALP_FACTOR</project>
  <title>T002-VALIDATE: re-pull all YALP_FACTOR YCharts test endpoints with FRESH cookie before colleague re-takes seat tomorrow AM ET</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~E</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completion>
    <brief>docs/briefs/yalp_factor_t002_validate_fresh_cookie_20260526.md</brief>
    <completed_at>2026-05-26T~22:09Z</completed_at>
    <wall_time>~14min spawn-to-RAVC2-Request (well under sub-30min target)</wall_time>
    <ac_status>4/4 ACs MET — 10/10 constituents + 6/6 spreads pulled OK in 11.6s; freshness HTTP 200; ZERO failures; Phase 2 dispatch READY; ^MSACWI HTTP 400 from Phase 1 §13.1 empirically CONFIRMED cookie-stale class (Andrew sovereign [[feedback_ycharts_http_400_is_cookie_stale_class]] validated)</ac_status>
  </completion>
  <priority>URGENT (Andrew sovereign direct ~21:54Z via ws CTO; time-pressure window NOW → tomorrow AM ET)</priority>
  <references>
    <ref type="cookie_refresh">AWS Secrets Manager `ycharts/credentials` REFRESHED ~21:55Z</ref>
    <ref type="phase1_substrate">YALP_FACTOR Phase 1 cascade ship `115ad2d40` (TO-002+004+005+VAL bundled; Level-2 per-spread verdicts; 4 MATCH + 2 REPRESENTATIVE) + status flip `506063e7b` + housekeeping `f69ddec92`</ref>
    <ref type="parallel_dispatch">5 YALP T002-VALIDATE TOs fired this cycle — sibling lanes ~A (MACROS) + ~B (VALUAT) + ~C SPAWN-NEEDED (CORREL) + ~D (POSITN)</ref>
  </references>
  <dependencies>
    <dependency>None — fresh cookie ready in AWS Secrets Manager + you LIVE on broker (LD-0107 batch)</dependency>
  </dependencies>
</metadata>

<scope>
**Re-pull all YALP_FACTOR YCharts test endpoints from Phase 1 with FRESH cookie** to validate session continuity.

**Endpoint scope:** all Phase 1 TO-002 test endpoints from `115ad2d40` cascade + spreadsheet rows. Use Phase 1 endpoint map verbatim.

**Output:** brief at `docs/briefs/yalp_factor_t002_validate_fresh_cookie_20260526.md` (~50-150 lines):
- §1 cookie-bundle source verification + timestamp
- §2 per-endpoint validation table (per-pull HTTP status)
- §3 failure categorization (session-eviction-RETRY / endpoint-class-drift / structural-baseline-match)
- §4 Phase 2 dispatch readiness for YALP_FACTOR

**Per CLAUDE.md Rule 14a:** safe-commit.sh --only.
</scope>

<acceptance_criteria>
- AC1: All Phase 1 YALP_FACTOR YCharts test endpoints re-pulled with fresh cookie within window.
- AC2: Per-endpoint HTTP status + parseable check documented.
- AC3: Failures categorized.
- AC4: Phase 2 dispatch readiness disposition documented.

**Pass requires all 4 ACs MET. Sub-30min plausible.**
</acceptance_criteria>

<cross_domain_coordination>
- **Sibling lanes parallel:** ~A + ~B + ~C + ~D.
- **Aggregate-orphan substrate (YALP_MACROS.006e):** you remain primary on that 24-FRED-GAP class; T002-VALIDATE is parallel side-task on different project.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing brief commit + AC1-AC4 evidence.

**Target ETA:** ~20-30min light-touch sweep.

**Post-RAVC2-ACCEPT:** KEEP-EPHEMERAL pending YALP_FACTOR Phase 2 dispatch.
</deliverable_disposition>

<notes>
- Phase 1 cascade was 4 MATCH + 2 REPRESENTATIVE per-spread; T002-VALIDATE confirms session continuity for that baseline.
- Light-touch; Phase 1 substrate stands.
</notes>
</task_order>
