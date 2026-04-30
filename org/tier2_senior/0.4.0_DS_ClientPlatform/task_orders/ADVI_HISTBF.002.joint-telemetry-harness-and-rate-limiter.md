<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_HISTBF.002</id>
    <project>ADVI_HISTBF</project>
    <title>Phase 1a — Telemetry harness + adaptive rate-limiter shared module (`rate_limiter.py`)</title>
    <issued_to>0.4.0_DS_ClientPlatform + 0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>complete</status>
    <priority>critical</priority>
    <estimated_effort>1-2d (DS + AE in parallel)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_HISTBF.md §5 (Andrew rate-limiter design — linear accel/linear fallback)</ref>
    <ref type="andrew_directive">2026-04-30 PM: "we need real-time telemetry or close polling because the moment we hit the 401, we want to mark what number of requests were were making per second/minute, records per second/minute, amount downloaded per second/minute. It is important that the telemetry is solid for this so that we can act quickly at failure and then set limits for future ETL."</ref>
    <ref type="andrew_design">PRD §5.1 algorithm pseudocode + §5.2 properties + §5.3 implementation surface</ref>
    <ref type="phase0_input">ADVI_HISTBF.001 deliverables (rate-limiter starting tunables + eligibility matrix); .002 may proceed in PARALLEL to .001 since rate_limiter.py is dim-agnostic infrastructure</ref>
    <ref type="cw_pattern">infra/aws/lambda/inf-pipeline/inf-ec2-launch-monitor/* (existing CW metric emission pattern)</ref>
  </references>

  <context>
    Andrew direction 2026-04-30 PM: telemetry is critical. The moment a 401 hits during backfill, we need to know exactly:
    - Requests per second / per minute at the failure point
    - Records per second / per minute at the failure point
    - Megabytes downloaded per second / per minute at the failure point

    This data drives:
    1. Adaptive rate-limiter fallback (back off from observed-failure rate)
    2. Future ETL limit setting (what's safe vs what's not)
    3. Real-time ops visibility (CW dashboards + alarms)
    4. Persistent state (resume backfill from prior observed-stable rate, not from SAFE_FLOOR every restart)

    Rate-limiter design per Andrew PRD §5: linear acceleration / linear fallback. SAFE_FLOOR ~0.5 req/sec start; STEP_DOWN > STEP_UP for oscillation damping; persistent observed-stable rate; CW metrics. The shared `rate_limiter.py` module is consumed by every per-dim pull script during Phase 1.

    Phase 1 backfill is multi-day. Cycles through JWT refresh windows. Mid-run failures must be captured and surfaced quickly enough to act.
  </context>

  <scope>

  ## DS sub-tasks (.002a — `0.4.0_DS_ClientPlatform`)

    1. **`rate_limiter.py` module** at `data/orion/scripts/bronze/rate_limiter.py` (new directory if needed).
       - Implements the algorithm in PRD §5.1 (pseudocode authoritative)
       - Class `AdaptiveRateLimiter` with constructor accepting SAFE_FLOOR, STEP_UP, STEP_DOWN, OBSERVED_CEILING (optional), BATCH_SIZE, state_file_path
       - Methods: `observe_batch(batch_results)`, `current_rps()`, `throttle()` (sleeps to enforce current rate), `persist_state()`, `load_state()`
       - State file: `s3://opal-data-inf/orion/rate_limit_state_{dim_name}.json` (production; **per-dim — CTO amendment 2026-04-30: single shared file causes write contention + cross-dim rate conflation**) OR local fallback (dev)
       - State schema: `{rate_rps, observed_ceiling, batches_at_current_rate, last_failure_rate, last_failure_at, total_observed_batches}`
       - Status code categorization: failure = {401, 429, 503, 504}; success = {200, 206}; ambiguous = {404} (treat as success for rate purposes — endpoint missing != rate issue).

    2. **Per-call telemetry capture**. Helper class or context manager that wraps each ORIAPI call:
       - Capture: timestamp_start, timestamp_end, elapsed_ms, status_code, payload_bytes, record_count (if parseable)
       - Emit: structured JSON event to local log + optionally to CW Logs (AE wires CW)
       - Aggregate: per-batch rollup (req/sec, records/sec, MB/sec) emitted at batch close

    3. **Per-dim pull script integration pattern**. Document in `data/orion/scripts/bronze/RATE_LIMITER_USAGE.md`:
       - How to instantiate AdaptiveRateLimiter in a pull script
       - How to wrap calls with telemetry
       - How to emit per-batch metrics
       - State file path conventions per dim (separate state per dim OR shared global state — DS judgment)

    4. **Pre-failure rate snapshot**. When a failure batch occurs, the rate-limiter MUST capture and persist the EXACT rate at the moment of failure:
       - rate_rps_at_failure
       - records_per_sec_at_failure
       - mb_per_sec_at_failure
       - batches_at_that_rate_pre_failure
       - failure_status_code(s)
       - timestamp
       Write to state file + emit as CW metric. This is the data Andrew explicitly called out.

    5. **Resume-from-stable-rate semantics**. On restart:
       - Load state file
       - If `last_failure_at` is more recent than (now - 24h), start at `max(SAFE_FLOOR, last_failure_rate * 0.5)` (defensive)
       - Else start at `last_observed_stable_rate * 0.8` (slightly defensive ramp)
       - Document the resume logic in module docstring.

    6. **Unit tests** at `tests/test_rate_limiter.py` (or wherever DS tests live):
       - SAFE_FLOOR floor enforcement (rate cannot go below)
       - STEP_UP linear acceleration on clean batches
       - STEP_DOWN linear fallback on failure
       - STEP_DOWN > STEP_UP property assertion
       - Persistence + load round-trip
       - Resume-from-stable semantics

    7. **Pre-commit gate + future annotations** per CLAUDE.md Rules 14 + 15.

  ## AE sub-tasks (.002b — `0.6.1_AE_PartnerETL`)

    8. **CW metrics emission**. Wire `rate_limiter.py` to CloudWatch via boto3:
       - Custom namespace: `Inflection/HistBackfill/RateLimiter`
       - Metrics emitted per batch (every BATCH_SIZE requests, default 100):
         - `RequestsPerSecond` (gauge)
         - `RecordsPerSecond` (gauge)
         - `BytesPerSecond` (gauge)
         - `RequestsThisBatch` (counter)
         - `FailureCountThisBatch` (counter)
         - `CurrentRateRps` (gauge — what the limiter is currently throttling to)
       - Metrics emitted on failure event:
         - `RateLimiter.FailureRate.Rps` (gauge — exact rate at moment of failure)
         - `RateLimiter.FailureRate.RecordsPerSec` (gauge)
         - `RateLimiter.FailureRate.MbPerSec` (gauge)
         - `RateLimiter.FailureCount` (counter)
       - All metrics dimensioned by `dim_name` (which Orion dim is being pulled) + `cycle_id` (each backfill run gets a UUID).

    9. **CloudWatch dashboard** at `infra/aws/cloudwatch/inflec-histbf-dashboard.tf` (or equivalent module):
       - Real-time visualization of RequestsPerSecond / RecordsPerSecond / BytesPerSecond per dim
       - Failure rate annotations
       - CurrentRateRps trend line
       - Alarm: `Inflection-HistBackfill-FailureSpike` triggers when FailureCount > 5 in 5min window → SNS to inf-otp-alert (existing topic).

    10. **IAM grants**. inf-bronze-runner EC2 role + any local-dev role need:
        - `cloudwatch:PutMetricData` on `Inflection/HistBackfill/*`
        - Existing S3 perms for state file (s3://opal-data-inf/orion/rate_limit_state.json) — verify or grant.

    11. **Terraform shipped + 0-diff verified**. Tag inf-pipeline-v1.7.6 (or whatever's next). Record deploy.

    12. **Coordinate with DS on per-dim state file paths**. AE confirms `s3://opal-data-inf/orion/rate_limit_state_{dim_name}.json` pattern doesn't conflict with existing keys. Pre-create with empty initial state per dim if needed. (CTO amendment 2026-04-30: single file dropped; per-dim required.)

  </scope>

  <acceptance_criteria>
    1. `data/orion/scripts/bronze/rate_limiter.py` shipped + unit tests pass.
    2. AdaptiveRateLimiter class implements PRD §5.1 algorithm verbatim (linear accel/linear fallback; STEP_DOWN > STEP_UP enforced; persistent state).
    3. Per-call telemetry capture context manager / helper shipped + documented.
    4. Pre-failure rate snapshot captured to state file + emitted as CW metric (rate_rps + records_per_sec + mb_per_sec at moment of failure).
    5. Resume-from-stable-rate semantics implemented + documented.
    6. CW metrics emitted to `Inflection/HistBackfill/RateLimiter` namespace with correct dimensions.
    7. CW dashboard live + alarm configured + SNS routing to inf-otp-alert.
    8. IAM grants verified (PutMetricData + S3 state file access).
    9. Terraform 0-diff verified; tag pushed; deploy recorded.
    10. RAVC4 to COO + CTO with: rate_limiter.py path, CW dashboard URL, sample telemetry event JSON, sample failure-rate snapshot JSON, unit test exit codes.

    DS side blocks AE side at: rate_limiter.py module shape (AE wires CW around it). AE side blocks DS at: state file path confirmation + CW namespace. DS+AE coordinate via direct MCP; not COO routing.
  </acceptance_criteria>

  <data_reprocess_scope>
    <no_reprocess_needed>rate_limiter.py is new infrastructure (not a patch to existing scripts); bronze S3 write paths unchanged; telemetry emission adds CW side-channel only; no historical data is semantically altered by this TO's changes; downstream consumers read bronze partitions unchanged</no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-blast on existing telemetry / CW patterns (e.g. inf-ec2-launch-monitor metrics)</check>
      <check>comp-iam service [inf-bronze-runner role] before adding CloudWatch permissions</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh on all .py edits (DS + AE)</check>
      <check>from __future__ import annotations on rate_limiter.py</check>
      <check>terraform plan + 0-diff verify (AE)</check>
    </before_commit>
    <after_commit>
      <check>comp-iam gaps (AE; verify no IAM regressions)</check>
      <check>S3 upload + comp-pipescript deployed MATCH (DS, if rate_limiter.py distributed via standard chain artifact path)</check>
      <check>Tag + push + record-terraform-deploy.sh (AE)</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_artifacts>
      <artifact>s3://opal-data-inf/orion/rate_limit_state_{dim_name}.json (NEW per-dim; DS writes via rate_limiter.py; AE pre-creates paths + IAM grants — CTO amendment 2026-04-30)</artifact>
      <artifact>CloudWatch namespace Inflection/HistBackfill/RateLimiter (NEW; AE wires; DS emits)</artifact>
      <artifact>data/orion/scripts/bronze/rate_limiter.py (NEW DS module; AE references for IAM grant scope)</artifact>
    </shared_artifacts>
    <coordination_protocol>
      DS authors rate_limiter.py first (interface stable); AE wires CW + IAM around it. Both ship in same wave. Direct MCP between DS + AE 0.6.1 for handoff; COO routes only if blocked.
    </coordination_protocol>
  </cross_domain_coordination>
</task_order>
