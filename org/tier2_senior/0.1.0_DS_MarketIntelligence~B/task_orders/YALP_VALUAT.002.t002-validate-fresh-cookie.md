<task_order>
<metadata>
  <to_id>YALP_VALUAT.002</to_id>
  <project>YALP_VALUAT</project>
  <title>T002-VALIDATE: re-pull all YALP_VALUAT YCharts test endpoints with FRESH cookie before colleague re-takes seat tomorrow AM ET</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — URGENT GO dispatched this cycle</status>
  <priority>URGENT (Andrew sovereign direct ~21:54Z via ws CTO; time-pressure window NOW → tomorrow AM ET before colleague re-takes single-session seat)</priority>
  <references>
    <ref type="cookie_refresh">AWS Secrets Manager `ycharts/credentials` REFRESHED ~21:55Z; all 6 key cookies PRESENT + structurally valid</ref>
    <ref type="phase1_substrate">YALP_VALUAT Phase 1 brief `789bebc4d` (40 atomic field rows: 22 Valuation main + 18 RiskPremiumTab); cascade ship `68b0e67ce` (3 MATCH + 2 REPRESENTATIVE + 2 DRIFT + 252 GAP + ~1300 n/a-derived)</ref>
    <ref type="parallel_dispatch">5 YALP T002-VALIDATE TOs fired this cycle — sibling lanes ~A (MACROS) + ~C SPAWN-NEEDED (CORREL) + ~D (POSITN) + ~E (FACTOR); PARALLEL execution</ref>
  </references>
  <dependencies>
    <dependency>None — fresh cookie ready in AWS Secrets Manager</dependency>
  </dependencies>
</metadata>

<scope>
**Re-pull all YALP_VALUAT YCharts test endpoints from Phase 1 with FRESH cookie** to validate session continuity:
1. Previously-pulled endpoints (Valuation main view 22 fields + RiskPremiumTab 18 fields) re-fetch with fresh cookie
2. Cross-check against cascade ship `68b0e67ce` baseline (3 MATCH + 2 REPR + 2 DRIFT + 252 GAP + ~1300 n/a-derived)
3. Flag any session-eviction (403 class) vs endpoint-class drift (404 / data-shape changes) vs structural-baseline matches

**Endpoint scope:** all Phase 1 TO-002 test endpoints from your brief `789bebc4d` + `68b0e67ce` cascade. Use Phase 1 endpoint map verbatim.

**Output:** brief at `docs/briefs/yalp_valuat_t002_validate_fresh_cookie_20260526.md` (~50-150 lines):
- §1 cookie-bundle source verification + timestamp
- §2 per-endpoint validation table (40 atomic field rows + HTTP status + parseable Y/N)
- §3 failure categorization (session-eviction-RETRY / endpoint-class-drift / structural-baseline-match)
- §4 Phase 2 dispatch readiness: any blockers for VALUAT Phase 2 dispatch surfaced

**Per CLAUDE.md Rule 14a:** safe-commit.sh --only for commits.
</scope>

<acceptance_criteria>
- AC1: All Phase 1 YALP_VALUAT YCharts test endpoints re-pulled with fresh cookie within window.
- AC2: Per-endpoint HTTP status + parseable check documented.
- AC3: Failures categorized into 3 classes.
- AC4: Phase 2 dispatch readiness disposition documented.

**Pass requires all 4 ACs MET. Sub-30min plausible.**
</acceptance_criteria>

<cross_domain_coordination>
- **Sibling lanes parallel:** ~A (MACROS) + ~C (CORREL SPAWN-NEEDED) + ~D (POSITN) + ~E (FACTOR). Same cookie bundle; same window.
- **TO-007 co-author scope (separate):** you remain KEEP-EPHEMERAL for any TO-008 sub-task; T002-VALIDATE is parallel side-task.
- **F1 fallback verdict in Phase 1:** previously refined REPRESENTATIVE → MATCH-CANDIDATE; T002-VALIDATE re-pull confirms cookie-stale-was-not-the-issue.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing brief commit hash + AC1-AC4 evidence inline.

**Target ETA:** ~20-30min light-touch sweep per cascade-compression.

**Post-RAVC2-ACCEPT:** KEEP-EPHEMERAL pending YALP_VALUAT Phase 2 dispatch (separate decomposition).
</deliverable_disposition>

<notes>
- Light-touch validation; Phase 1 brief content stands — T002-VALIDATE confirms cookie-stale class resolved.
- If session-eviction-RETRY fires mid-pull, document timestamp + escalate to ws COO.
- 9th-fire of self-correction-upstream-of-verify-channel pattern banked in Phase 1; T002-VALIDATE is the verify-side completion.
</notes>
</task_order>
