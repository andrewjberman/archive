<task_order>
<metadata>
  <to_id>YALP_MKTOVR.002</to_id>
  <project>YALP_MKTOVR</project>
  <title>YCharts test-pulls on Level-1 endpoints (T*=2026-05-22; ~2-3h)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending</status>
  <priority>HIGH (Andrew sovereign direct priority elevation)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MKTOVR.md v0.3 `42cbf164c` (1.0.0_SA_CTO; DDB-intermediate canonicalized). Full scope + AC details in PRD §6 (TO-002 section).</ref>
    <ref type="predecessor">TO-001 SHIPPED `cc4a3d575` 2026-05-26 ~14:47Z (RAVC2-ACCEPT ws COO ~14:55Z). Brief at `docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md` (Level-1 table populated 6 components / 9 endpoints).</ref>
    <ref type="t_star">T*=2026-05-22 (Friday) yang-side binding constraint per DS 0.2.0 consult `8d1d6fcad`.</ref>
  </references>
  <dependencies>
    <dependency>TO-001 RAVC2-Accepted ✓.</dependency>
    <dependency>Menachem-bundled shared cookie usable (Andrew direct; session-eviction tolerance per `project_ycharts_dedicated_seat_403_session_eviction.md`).</dependency>
    <dependency>C2 dormant module IAM/invocation reachability — **PRE-CHECK REQUIRED before first pull** per CVO unknown-unknown from pre-propagate gate `d12028652`. If C2 module Lambda not invocable in current dormant state, surface to ws COO immediately — may need AE 0.7 on-call to enable (AE 0.7 currently AC9-gated; if needed, that's a STUCK-RESOLVABLE escalation to MSTR).</dependency>
  </dependencies>
</metadata>

<scope>
For every YCharts endpoint surfaced in TO-001's Level-1 table (`docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md`), execute a test pull on T*=2026-05-22 using the menachem-bundled shared cookie via C2 dormant module pull paths (or equivalent ycharts pull harness).

**Endpoint surface (from TO-001 brief §2):** Tier-1 page-mount + Tier-2 on-demand + Tier-3 sampled (per §9.4 plan: 15 tickers × 2 endpoints = 30 Tier-3 pulls).

**Per pull, capture:**
- HTTP response status
- Response shape (non-empty payload, JSON structure matches expected field schema)
- Pull timestamp (for 403-session-eviction-vs-stale-cookie disambiguation)
- Any 403/429/timeout classification: session-eviction (Andrew known) vs entitlement-gap (real permission issue) vs rate-limit (back-off + retry)

**Output:** appendix or sub-section in the same TO-001 brief (`docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md`) documenting test-pull results per endpoint. Keep Level-2 table empty (TO-004 scope).

**Skipped fields (carry forward from TO-001 §11 lean):** Daily Cloud (news-pipeline) + Fear & Greed (CNN) + Trending Topics — no YCharts pull needed (YCharts=n/a per Level-1).
</scope>

<acceptance_criteria>
- AC1: Every Level-1 YCharts endpoint has a confirmed non-empty test-pull on T*=2026-05-22 (or explicit failure classification).
- AC2: Tier-3 sampled tickers (15 tickers × 2 endpoints) match the §9.4 selection rubric (2 D2-clean + 2 D2-divergent + 1 random per asset class).
- AC3: Any 403/429/timeout classified per retry-class taxonomy (session-eviction / entitlement-gap / rate-limit) with retry-with-backoff evidence captured.
- AC4: C2 dormant module IAM/invocation reachability pre-check executed BEFORE first pull; result documented (PASS = proceed; FAIL = surface to COO immediately).
- AC5: Test-pull results appendix added to existing TO-001 brief (single-doc continuity).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before first pull):**
- C2 dormant module pre-check: `aws lambda get-function --function-name ycharts-market-data-pull` (or equivalent C2 module name); confirm function exists + IAM role attached + status=Active
- Verify menachem cookie staging path (likely SSM Parameter Store or S3 — per existing harness convention)

**Phase 2 (during pulls):**
- Compiler tools NOT applicable to YCharts pulls (external API; no comp-* coverage). Document session log with non-blank methodology.

**Phase 3 (after appendix commit):**
- Session log with Compiler Tools section noting the external-API non-applicability + retry-class observations
</compiler_tools_mandate>

<cross_domain_coordination>
- **AE 0.7 on-call** — flag immediately if C2 dormant module needs Lambda enable/permission grant. AE 0.7 AC9-gated; this becomes a STUCK-RESOLVABLE escalation to ws COO → MSTR.
- **Menachem cookie staging** — confirm cookie freshness before pulls; if stale, surface (no Andrew dedicated-seat yet per `project_ycharts_dedicated_seat_403_session_eviction`).
- **TO-001 brief continuity** — appendix lands in same doc; preserve §1-§11 + §12 (open items) + add §13 (test-pull results) section.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for test-pull appendix
- Per-endpoint pull-result table (status + response-shape + retry-class as applicable)
- C2 module pre-check evidence (`aws lambda get-function` output snippet OR equivalent)
- Session log
</expected_evidence>

<notes>
Sequential per PRD §6: TO-001 → TO-002 → TO-004. TO-003 closed via DS 0.2.0 consult `8d1d6fcad` (formal retrospective ACK in separate TO-003 file). TO-VAL fires after TO-004 closes.

**REPRESENTATIVE-class preventive note (carries into TO-004 GO, not this TO):** when TO-004 ships, the GO MCP will include CVO's sharp-boundary sentence — "for any REPRESENTATIVE verdict, include YCharts methodology citation OR delta-magnitude bound" — to prevent laundering-channel risk per CVO pre-propagate gate flag.

**Throughput target:** ~2-3h estimate per PRD §6. RAVC2-Request when all endpoints have a result (success OR explicit-failure classification). If C2 module pre-check FAILS, that's a STUCK-RESOLVABLE surface — don't wait, surface immediately so I can route to AE 0.7 (with AC9 escalation if needed).

Architectural / scope ambiguity → ws CTO. Dispatch / RAVC2 / blockers → me.
</notes>
</task_order>
