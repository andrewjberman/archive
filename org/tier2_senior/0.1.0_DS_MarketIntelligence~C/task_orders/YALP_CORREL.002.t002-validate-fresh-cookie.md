<task_order>
<metadata>
  <to_id>YALP_CORREL.002</to_id>
  <project>YALP_CORREL</project>
  <title>T002-VALIDATE: re-pull all YALP_CORREL YCharts test endpoints with FRESH cookie before colleague re-takes seat tomorrow AM ET</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~C</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — brief shipped 80d9bed66 22:25Z (~25min wall spawn→ship); 4/4 ACs MET; cookie validated via model_portfolios 403→200 flip + indices_table_data CORREL-universe 8/15 records; charts/fund_data 400 persisting (Option A vs B disposition deferred to COO); YALP_CORREL.006-EMPIRICAL follow-on readiness MET. RAVC2-Request 20260526T222531Z filesystem+broker+channel-push to ws COO. KEEP-EPHEMERAL pending YALP_CORREL Phase 2 dispatch per deliverable_disposition.</status>
  <priority>URGENT (Andrew sovereign direct ~21:54Z via ws CTO; time-pressure window NOW → tomorrow AM ET)</priority>
  <references>
    <ref type="cookie_refresh">AWS Secrets Manager `ycharts/credentials` REFRESHED ~21:55Z</ref>
    <ref type="phase1_substrate">YALP_CORREL Phase 1 brief `f386e9370` (Level-1 endpoint+field mapping) + cascade ship `2d7cf02ae` (105-row spreadsheet); RAVC2-accepted `8c946166c`</ref>
    <ref type="parallel_dispatch">5 YALP T002-VALIDATE TOs fired this cycle — sibling lanes ~A (MACROS) + ~B (VALUAT) + ~D (POSITN) + ~E (FACTOR)</ref>
  </references>
  <dependencies>
    <dependency>~C SPAWN-NEEDED via MSTR /allocation (not currently LIVE; per LD-0105 Fix-3 precheck + SPAWN-WITH-DIRECTION substrate)</dependency>
  </dependencies>
</metadata>

<scope>
**Re-pull all YALP_CORREL YCharts test endpoints from Phase 1 with FRESH cookie** to validate session continuity.

**Endpoint scope:** all Phase 1 TO-001/TO-002 test endpoints from `f386e9370` + `2d7cf02ae` cascade (105-row spreadsheet). Use Phase 1 endpoint map verbatim.

**Output:** brief at `docs/briefs/yalp_correl_t002_validate_fresh_cookie_20260526.md` (~50-150 lines):
- §1 cookie-bundle source verification + timestamp
- §2 per-endpoint validation table (105 rows + HTTP status + parseable Y/N)
- §3 failure categorization (session-eviction-RETRY / endpoint-class-drift / structural-baseline-match)
- §4 YALP_CORREL.006-EMPIRICAL follow-on readiness (per project JSON cutover-trust NEEDS-INVESTIGATION disposition)

**Per CLAUDE.md Rule 14a:** safe-commit.sh --only.
</scope>

<acceptance_criteria>
- AC1: All Phase 1 YALP_CORREL YCharts test endpoints re-pulled with fresh cookie.
- AC2: Per-endpoint HTTP status + parseable check documented.
- AC3: Failures categorized.
- AC4: YALP_CORREL.006-EMPIRICAL follow-on readiness documented.

**Pass requires all 4 ACs MET. Sub-30min plausible.**
</acceptance_criteria>

<cross_domain_coordination>
- **Sibling lanes parallel:** ~A + ~B + ~D + ~E. Same cookie bundle; same window.
- **SPAWN-with-DIRECTION substrate:** MSTR spawn-with-direction MCP this cycle will inline this TO file pointer + cookie-state context + Phase 1 substrate cites.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing brief commit hash + AC1-AC4 evidence inline.

**Target ETA:** ~20-30min light-touch + spawn-orient overhead.

**Post-RAVC2-ACCEPT:** KEEP-EPHEMERAL pending YALP_CORREL Phase 2 dispatch.
</deliverable_disposition>

<notes>
- Light-touch validation; spawn-with-direction substrate enables fast-orient pattern.
- 0.1.0_DS_MarketIntelligence~C is one of 5 YALP-page lanes; T002-VALIDATE is the cookie-sanity-class sweep.
</notes>
</task_order>
