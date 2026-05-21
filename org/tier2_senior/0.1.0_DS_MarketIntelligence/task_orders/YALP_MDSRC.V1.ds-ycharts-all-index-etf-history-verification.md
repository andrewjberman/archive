<task_order>
  <metadata>
    <id>YALP_MDSRC.V1</id>
    <slug>ds-ycharts-all-index-etf-history-verification</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>ALREADY GO'd — live verification dispatched 2026-05-21 (Andrew "first order of business" re-scope). V1 is the FORMAL TO OF RECORD for work 0.1.0_DS is already running; no new start. WS-A of YALP_MDSRC PRD v0.4 (docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md, 6543894ce).</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew's "first order of business." WS-A; gates the SA-series sourcing verdicts (every YCharts-replaceable verdict cites V1's measured depth/granularity).</priority>
    <sla>~1 effort-day — a serialized 76-entity live sweep on a single session.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md (v0.4, 6543894ce) §3 WS-A, §6 TO-V1.</prd>
    <a4>docs/briefs/mdsrc-a4-granularity-depth-matrix-20260521.csv — the 76-entity universe + partial verdicts V1 completes.</a4>
    <a5>docs/briefs/mdsrc-a5-ycharts-har-endpoint-assessment-20260521.md — the HAR-derived full quote-page param form (clears the MSCI/GSCI/bond 400s) + the /search/suggest/main endpoint.</a5>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md.</standard>
  </references>

  <context>
    A4 swept 76 entities but only 29 had confirmed depth; 36 MSCI/Bloomberg-bond entities returned documented-400 (the prior Alyssa-session evictions — A5 proved these are reachable via the full quote-page fund_data.json param form) and 9 were symbol-unresolved. V1 completes the verification LIVE on the stable mchm login: a real measured per-entity depth/granularity matrix for all 76.

    R4 — VERIFICATION != PRODUCTION. V1 runs verification probes on the mchm login. The production pipeline (automated YCharts pull cron, the C1 capture-Lambda live-invoke, D1 cutover) stays gated on the dedicated YCharts seat + an explicit Andrew go-live. V1 is verification only.
  </context>

  <scope>
    <in_scope>
      - Update the A4 capture runner to the A5/HAR-derived full quote-page fund_data.json param form + add a /search/suggest/main mode.
      - Live-capture, on the mchm login, full history depth + granularity for every index, ETF, bond index, and commodity in the A4 76-entity universe — including the 36 MSCI/Bloomberg-bond entities A4 only documented-400.
      - Resolve the 9 symbol-unresolved entities via /search/suggest/main.
      - Output: a complete per-entity matrix — first date, point count, cadence, isFullRange — for all 76, replacing A4's partial verdicts. RAVC2 to COO + CC CTO.
      - Single-session discipline: one mchm session, serialized probes (~2s spacing), freshness + 403-eviction detection — fail safe if the seat is disturbed.
    </in_scope>
    <out_of_scope>
      - Production YCharts execution — no cron, no C1 live-invoke, no D1. R4.
      - The page-by-page sourcing verdicts — that is SA1/SA2/SA3; V1 supplies the depth/granularity evidence those verdicts cite.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
  Phase 1: confirm the entity universe against the A4 matrix (docs/briefs/mdsrc-a4-granularity-depth-matrix-20260521.csv); no entity dropped.
  Phase 2: per-entity integrity check — raw_data length == point_count == first/last endpoints (the A4 verification method).
  Phase 3: verify-channel discipline — the matrix verdict is "history confirmed" only when an actual series was pulled and measured, never inventory-inferred.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - F1 single YCharts session seat — mchm login, single session, no dedicated seat yet. Hold the session for the run; coordinate 0.7.0_AE_CloudOps off YCharts during it. C1's capture Lambda is dormant — no contention there.
    - V1's matrix is the evidence base for SA1/SA2/SA3 — land it before those TOs' YCharts-replaceability verdicts finalize.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — all 76 entities probed live; none dropped (Phase-1 check vs the A4 matrix).
    - AC2 — per entity: first date, point count, cadence, isFullRange — measured from an actual pulled series (Phase-2 integrity check), never inventory-inferred (Phase-3).
    - AC3 — the 36 MSCI/Bloomberg-bond entities live-captured; the 9 symbol-unresolved entities resolved (or explicitly documented unresolvable).
    - AC4 — committed complete depth/granularity matrix superseding the A4 partial verdicts; session log Compiler Tools section; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
