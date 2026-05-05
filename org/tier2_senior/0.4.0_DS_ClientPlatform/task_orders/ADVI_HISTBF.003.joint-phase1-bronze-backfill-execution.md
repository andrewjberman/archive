<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_HISTBF.003</id>
    <project>ADVI_HISTBF</project>
    <title>Phase 1 — Bronze backfill execution per eligible dim using adaptive rate-limiter (sized post-Phase-0)</title>
    <issued_to>0.4.0_DS_ClientPlatform + 0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>complete</status><!-- Flipped 2026-05-05 by 2.0.0_SA_COO during session 57 GT-recon. Evidence: ADVI_HISTBF.json status=complete (2026-05-04 ship) + Phase 1b BRONZE Wave B v5 + Phase 2 SILVER (DS~D `5fef9a910` ThreadPoolExecutor(32), 537s wall, ok=1618 skip=2714 err=0 zero gaps) + Phase 3 GOLD (AE 0.6.1 cumulative-batch 16min wall) + 3-step close commit `def351cb4`. CTO amendment 2026-04-30: AE 0.6.1 owns EC2 dispatch + run monitoring (not DS BASE); DS writes scripts + uploads to S3; chain reg gate: DS comp-pipescript deployed MATCH on all scripts → AE updates chain reg → AE EC2 dispatch. SSM RunCommand 60-min cap incompatible with 6hr run — must use persistent process on inf-bronze-runner. -->
    <priority>high</priority>
    <estimated_effort>TBD by Phase 0 results (~3-7 days; depends on dim count × calls per dim × observed sustained rate)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_HISTBF.md §2 Phase 1 + §5 rate-limiter design</ref>
    <ref type="gates">ADVI_HISTBF.001 RAVC4 (eligibility matrix + tunables); ADVI_HISTBF.002 RAVC4 (rate_limiter.py + telemetry harness shipped)</ref>
    <ref type="andrew_directive">2026-04-30 PM: "large scale backfill, whereby we slowly increase chunking size/calls linearly to see how much data we can pull before hitting a 401"</ref>
    <ref type="reference_pattern">data/orion/manual_api/pull_inflection_positions_daily.py (already supports --backfill-days N + --start/--end + chunked output)</ref>
    <ref type="canonical_pattern">docs/architecture/ADVI_ORIAPI.md §270/273/424/428/494 — Authorization: Session &lt;JWT&gt;</ref>
    <ref type="jwt_resilience">ADVI_JWTRES.001 freshness gate (parallel TO; soft-prereq for multi-day backfill)</ref>
  </references>

  <context>
    Phase 0 (.001) returns dim eligibility matrix + adaptive rate-limiter starting tunables. Phase 1a (.002) ships the shared `rate_limiter.py` module + telemetry harness + CW dashboard.

    Phase 1b (.003) is the actual backfill execution. For each dim where Phase 0 confirms historical-date support:
    - Run bronze pulls date-by-date (or in chunks if endpoint supports range queries)
    - Apply adaptive rate-limiter throttle
    - Emit telemetry per batch to CW
    - On 401/429/5xx, capture exact rate snapshot + persist + back off per STEP_DOWN
    - On clean batches, accelerate per STEP_UP
    - Backfill target: silver/transactions origin (2020-05-26) for SUPPORTED dims; per-dim earliest-available-date noted by Phase 0 for PARTIAL/CURRENT-ONLY dims

    Total scope sized off Phase 0 results. Estimated 16,000 calls minimum (2,000 dates × 8 dims) to ~2M+ for full 6yr if positions_daily's ~8,820 calls/30days extrapolates.

    Phase 1 is multi-day. JWT refresh cadence is the constraint — JWT Lasts 10h; multi-day runs cycle through ~3 refreshes/day. ADVI_JWTRES.001 (Option A freshness check) is the soft-prereq; if shipped, mid-backfill JWT-stale failures are caught early. If not yet shipped, .003 relies on rate-limiter's 401-handling to back off (graceful degradation).
  </context>

  <scope>
    1. **Per-dim pull script extensions**. For each Phase-0-eligible dim, extend `data/orion/manual_api/pull_inflection_<dim>.py` to support:
       - `--backfill-start YYYY-MM-DD` and `--backfill-end YYYY-MM-DD` flags (positions_daily already has this; reference)
       - `--cycle-id` UUID for telemetry attribution
       - Integration with `rate_limiter.AdaptiveRateLimiter` from .002a
       - Per-call telemetry capture from .002a helper
       - Resume-from-state on restart (if interrupted)

    2. **Per-dim execution wave**. Sequence dims per Phase 0 ops-convenience recommendation (Andrew §4 ruling: priority order irrelevant; ops convenience drives sequencing). Suggested ops-convenience: dim with fewest expected calls first to validate rate-limiting strategy at low cost.

    3. **JWT freshness during backfill**. Multi-day runs cycle through JWT refresh windows:
       - If ADVI_JWTRES.001 is live: rely on freshness gate to fail-fast on near-expiry; coordinate restart post-refresh
       - If not yet live: rely on rate_limiter's 401 handling — observe 401, back off, retry after JWT refresh signal (manual or via watchdog)

    4. **Real-time monitoring during execution**. Andrew direct quote: "act quickly at failure":
       - CW dashboard (.002b) live throughout
       - On `RateLimiter.FailureRate.*` metric spike: dispatcher (DS or AE on watch) reviews, decides to pause/resume
       - SNS alarm `Inflection-HistBackfill-FailureSpike` routes to inf-otp-alert → operator notification

    5. **Backfill output**. Per-dim, per-date partition: `s3://opal-data-inf/bronze/orion-api-v2/<date>/<dim>.parquet`.
       Compatible with existing chain reg in orion-gold-dispatch.sh.

    6. **Silver propagation**. Phase 2 silver backfill is OUT OF SCOPE for .003 — covered by separate TO post-Phase-1 ship. .003 focuses on bronze layer only.

    7. **Failure-recovery decision matrix**. Document at `docs/data/inflec_histbf_recovery_protocol.md`:
       - Per failure class (401 vendor IP-ban, 429 rate-limit, 503 transient, 504 timeout, 5xx unknown), what to do
       - When to pause vs auto-back-off vs escalate to Andrew
       - Per Andrew PRD §5.5: if vendor IP-bans during a run, pause + document + escalate (no Orion support fallback). Hard-stop event, not auto-recovery.

    8. **Persistent state across runs**. Per-dim state files `s3://opal-data-inf/orion/rate_limit_state_{dim_name}.json` survive across multi-day runs. Resume from prior observed-stable rate (not SAFE_FLOOR every restart). (CTO amendment 2026-04-30: per-dim paths required; single shared file causes write contention + cross-dim rate conflation.)

    8a. **Global-pause on systemic-rate-failure** (CTO amendment 2026-04-30). Orchestration-layer coordinator on top of per-dim rate_limiter.py:
       - Trigger: >= 3 dims fail within a 2-minute window with 401/429 AND JWTRES.001 reports JWT is fresh
       - Action: ALL dims pause for a configurable backoff window (recommended: 2x current STEP_DOWN interval)
       - Rationale: if JWT is confirmed fresh and 401s arrive on multiple dims simultaneously, that is a rate-class event — backing off only one dim doesn't help. Per-dim isolation handles single-dim blips; global-pause handles systemic rate exhaustion.
       - Implementation: add this coordinator to .003 multi-dim orchestration layer (not to .002 rate_limiter.py which stays per-dim)

    9. **Daily progress report**. AE 0.6.1 (or DS) emits daily summary post-EOD:
       - Dims completed today
       - Calls executed
       - Date ranges covered
       - Failure events (if any) with rate snapshots
       - Projected ETA to full Phase 1 completion
       - Save to `org/tier2_senior/0.6.1_AE_PartnerETL/logs/<date>/histbf_phase1_progress.md`

    10. **Phase 1 close criteria**:
       - All eligible dims (per Phase 0 matrix) backfilled to their earliest-available-date OR silver/transactions origin (2020-05-26), whichever applies
       - CURRENT-ONLY dims: documented as "current snapshot is earliest available"
       - UNSUPPORTED dims: documented as "vendor does not support historical retrieval; ongoing daily dispatch is the only data source"
       - State file final state captured
       - Phase 2 (silver backfill) authored as next TO

  </scope>

  <acceptance_criteria>
    1. Per-dim pull scripts extended with --backfill-start/--backfill-end + --cycle-id + rate_limiter integration + telemetry capture.
    2. Phase 0 eligibility matrix consumed (each SUPPORTED dim backfilled; CURRENT-ONLY dims skipped with documentation; UNSUPPORTED dims skipped with documentation).
    3. Backfill output present in s3://opal-data-inf/bronze/orion-api-v2/&lt;date&gt;/&lt;dim&gt;.parquet for all expected (date, dim) tuples.
    4. CW telemetry continuously emitted; dashboard shows per-dim progress.
    5. Failure-recovery protocol documented + executed cleanly (any 401/429/5xx events surfaced with rate snapshots).
    6. State file persisted + survived restarts (verified via at least one resumption cycle).
    7. Daily progress reports for each day of Phase 1 execution.
    8. Phase 1 close report: eligible dims complete; failure events catalogued; rate-limiter empirical findings updated to docs/data/inflec_histbf_rate_limiter_constants.md.
    9. Compiler tools mandate satisfied.
    10. Pre-commit gate (CLAUDE.md Rule 14) PASS on all .py edits.
    11. RAVC4 to COO + CTO at Phase 1 close with ETA for Phase 2 (silver backfill) authoring.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-pipescript io [each pull_inflection_&lt;dim&gt;.py being extended]</check>
      <check>comp-pipescript postdeps [each script] before any ad-hoc runs (CLAUDE.md table row 3)</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh on all .py edits</check>
      <check>from __future__ import annotations on bronze/silver scripts (CLAUDE.md Rule 15)</check>
    </before_commit>
    <after_commit>
      <check>S3 upload + comp-pipescript deployed MATCH (CLAUDE.md Rule 13 — DS owns upload)</check>
      <check>AE 0.6.1 chain reg update if new CATALOG entries needed (per .002 + .003 surface)</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_artifacts>
      <artifact>data/orion/manual_api/pull_inflection_*.py (authored by DS; uploaded to S3 by DS; executed by AE)</artifact>
      <artifact>s3://opal-data-inf/bronze/orion-api-v2/* (NEW partitions per dim per date; backfill output)</artifact>
      <artifact>s3://opal-data-inf/orion/rate_limit_state_{dim_name}.json (per-dim; AE pre-created; read+write throughout backfill)</artifact>
      <artifact>data/orion/scripts/gold/orion-gold-dispatch.sh (AE updates chain reg AFTER DS comp-pipescript deployed MATCH gate)</artifact>
    </shared_artifacts>
    <coordination_protocol>
      CTO ruling 2026-04-30: AE 0.6.1 owns EC2 dispatch + run monitoring. DS BASE does NOT dispatch EC2.
      Handoff gate: DS commits all pull scripts + uploads to s3://opal-data-inf/code/bronze/ + confirms comp-pipescript deployed MATCH on all scripts → MCP AE 0.6.1 → AE updates chain reg → AE dispatches inf-bronze-runner persistent process (NOT SSM RunCommand — 60-min cap incompatible with 6hr run).
      Run order: positions_mv → assets_v2 → transactions → performance (highest-confidence first; positions_mv proven by DIAGFIX.012).
      DS BASE monitors CW dashboard (Inflection-HistBackfill-RateLimiter) throughout; acts on FailureSpike alerts.
      Daily MCP between DS + AE 0.6.1 (progress + failure events). COO standby for cross-day blockers.
    </coordination_protocol>
  </cross_domain_coordination>
</task_order>
