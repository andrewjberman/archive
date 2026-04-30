<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_HISTBF.001</id>
    <project>ADVI_HISTBF</project>
    <title>Phase 0 — ORIAPI shape validation + historical-date capability probe across 8 dims</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>complete</status><!-- RAVC4 received 2026-04-30 from 0.4.0_DS_ClientPlatform_B (7a4d66c00). 8 probe scripts + eligibility matrix + rate constants delivered. positions_mv/assets_v2 SUPPORTED; accounts_v2/household_rep_mapping/household CURRENT-ONLY; billing/activity/performance PARTIAL. Scale: ~450K REST calls ~125h. Phase 1 gate: JWTRES.001 soft-prereq. -->
    <priority>high</priority>
    <estimated_effort>1-2d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_HISTBF.md (Phase 0 + Andrew rulings §4 + adaptive rate-limiter §5)</ref>
    <ref type="source_brief">org/tier2_senior/0.6.1_AE_PartnerETL/deliverables/CTO_BRIEFING_INFLEC_HISTBACKFILL_AND_JWT_RESILIENCE_20260430.md §1+§2</ref>
    <ref type="andrew_directive">2026-04-30 PM: "comprehensive validation of the ORIAPI file shapes (does the call work reliably? can we get historical dates for this shape through the ORIAPI?)"</ref>
    <ref type="reference_pattern">data/orion/manual_api/pull_inflection_positions_daily.py (already supports --backfill-days N + --start/--end; reference for new probe scripts)</ref>
    <ref type="parent_dispatch">data/orion/scripts/gold/orion-gold-dispatch.sh (8 dim CATALOG entries; INF_API_PULL_* + INF_API_SILVER_* prefixes; chain reg shipped via 3f762ba79 + c2062b709)</ref>
    <ref type="canonical_pattern">docs/architecture/ADVI_ORIAPI.md §270/273/424/428/494 — Authorization: Session &lt;JWT&gt; (NOT Bearer)</ref>
  </references>

  <context>
    Andrew direction 2026-04-30 PM: comprehensive ORIAPI shape validation precedes backfill. Must answer two questions PER DIM before committing to bulk backfill:
    1. Does the call work reliably? (call success rate, response shape consistency, latency profile)
    2. Can we get historical dates for this shape through ORIAPI? (does the endpoint accept date parameters; does it return historical state vs current state)

    8 dims in scope per AE silver-coverage audit: accounts_v2, household, household_rep_mapping, billing, activity, performance, positions_mv, assets_v2.

    Per-dim eligibility is unknown. Some dims may be current-state-only (vendor returns today's snapshot regardless of date param); for those, current snapshot is the earliest available date and the eligibility matrix records that explicitly.

    Off-the-books posture (no Orion support contact): probe is purely empirical. No vendor-confirmed answers; infer support from response shape (HTTP status codes, payload variance, response times, payload size variance).
  </context>

  <scope>
    1. **Per-dim probe scripts**. For each of the 8 dims, author a probe script in `data/orion/manual_api/probe_inflec_<dim>.py`. Pattern: take a small client sample (5-10 representatives across rep_id range {3,6,7,8,10,11,12} per DIAGFIX.011 representatives), test multiple historical dates: today, -7d, -30d, -90d, -180d, -365d, -730d, -1825d (5y), and silver/transactions origin (2020-05-26).

    2. **Per-call observation**. For each call, capture:
       - HTTP status code (200 / 401 / 404 / 429 / 5xx / etc.)
       - Response time in ms (start-to-finish wall clock)
       - Payload size in bytes (Content-Length OR len(response.content))
       - Top-level payload shape (key set; row count if list; record count for structured responses)
       - Error message body if non-200
       - Request timestamp (UTC, ms precision)

    3. **Reliability fingerprint per dim**. Aggregate per-dim metrics from probe runs:
       - Call success rate (200 / total)
       - p50 / p95 / p99 response time
       - Payload size variance (consistency check — sudden shape changes indicate vendor-side schema drift or unexpected behavior)
       - Failure modes encountered (with count + sample messages)

    4. **Historical-date support classification per dim**. Compare returned data across dates:
       - **SUPPORTED:** responses for past dates differ from today's snapshot in expected ways (different account counts, MV, activity volumes, etc.)
       - **CURRENT-ONLY:** responses for past dates equal today's snapshot regardless of date param (vendor ignores date)
       - **PARTIAL:** date param accepted but only for limited window (e.g. last 30/90 days)
       - **UNSUPPORTED:** 4xx errors / empty payloads / undocumented behavior

    5. **Earliest available date per dim**. Find the deepest historical date that returns 200 + non-empty payload differing from today's snapshot. Document explicitly. If silver/transactions origin (2020-05-26) returns equivalent shape, eligibility goes to that date.

    6. **Dim-by-dim eligibility matrix output**. Structured doc at `docs/data/inflec_histbf_eligibility_matrix.md` with:
       | dim_name | support_class | earliest_available_date | call_success_rate | p50_ms | p95_ms | payload_var | failure_modes | notes |

    7. **Adaptive rate-limiter starting tunables (Phase 0 deliverable per Andrew §5)**. During probe runs, observe at what request rates 401s/429s/5xx start appearing. Output recommendation:
       - SAFE_FLOOR (recommended starting req/sec; default 0.5 unless probe shows lower needed)
       - STEP_UP (linear acceleration constant)
       - STEP_DOWN (linear fallback constant; STEP_DOWN > STEP_UP per Andrew)
       - OBSERVED_CEILING (if discoverable; otherwise leave as runtime-discovered in Phase 1)
       - BATCH_SIZE (observation window; default 100)
       Document in `docs/data/inflec_histbf_rate_limiter_constants.md` with empirical justification (probe data citations).

    8. **Probe runtime budget**. Total probe should be ≤ 1,500 calls (8 dims × 5-10 clients × ~10 dates + retries). Stay polite by default — start at SAFE_FLOOR ~0.5 req/sec; if no failures observed, ramp gradually within probe scope. Don't burst.

    9. **JWT freshness during probe**. Probe runs require fresh JWT; coordinate with current Cycle 2 cron OR manual JWT refresh if needed. JWT live until 2026-05-01 00:27:47Z per AE 0.7 manual dispatch (SSM cmd `f4b04116`). If probe extends past JWT expiry, surface to AE 0.7 for refresh; do NOT silent-fail.

    10. **Authorization header**: use `Authorization: Session <JWT>` per canonical pattern (NOT Bearer). JWT in SM `orion/jwt/current` (raw token; consumer prepends `Session ` prefix) OR S3 `s3://opal-data-inf/orion/jwt/current.json` (JSON wrapper; both paths active per v1.7.5 dual-path).

    11. **Session log**. Capture findings + inferences + Phase 1 sequencing recommendation. Save to `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/<date>/histbf_phase0_probe.md` (mark with `~B` lane attribution).
  </scope>

  <acceptance_criteria>
    1. Per-dim probe scripts shipped to `data/orion/manual_api/probe_inflec_<dim>.py` for all 8 dims (accounts_v2, household, household_rep_mapping, billing, activity, performance, positions_mv, assets_v2).
    2. Probe runs executed against fresh JWT; per-call observation log saved (CSV or JSON in `data/orion/manual_api/pulls/<date>_histbf_probe.json`).
    3. Reliability fingerprint per dim documented: success rate, response-time p50/p95/p99, payload size variance, failure modes with counts.
    4. Eligibility matrix at `docs/data/inflec_histbf_eligibility_matrix.md`: 8 rows × {support_class, earliest_available_date, reliability metrics, notes}.
    5. Adaptive rate-limiter starting tunables documented at `docs/data/inflec_histbf_rate_limiter_constants.md` with empirical justification.
    6. Probe stayed under 1,500 calls total budget (verifiable from log).
    7. Compiler tools mandate satisfied (see block).
    8. Pre-commit gate (CLAUDE.md Rule 14) PASS on all `.py` edits.
    9. RAVC4 to COO + CTO with eligibility matrix link + tunables doc link + Phase 1 sizing recommendation (estimated calls per dim × eligible dim count + projected backfill duration).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      <check>Read pull_inflection_positions_daily.py — reference pattern for backfill flags + rate-limiting</check>
      <check>comp-pipescript io [for any existing pull script you extend]</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh on all new/modified .py files</check>
      <check>from __future__ import annotations as first import (CLAUDE.md Rule 15)</check>
    </before_commit>
    <after_commit>
      <check>S3 upload of probe scripts NOT required for Phase 0 (probe runs locally / from EC2 with JWT access; not part of nightly chain)</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    Phase 0 is pure exploration; no shared S3 keys with active TOs. Phase 1 will require coordination with AE 0.6.1 chain reg (post-Phase 0 ship).
  </cross_domain_coordination>
</task_order>
