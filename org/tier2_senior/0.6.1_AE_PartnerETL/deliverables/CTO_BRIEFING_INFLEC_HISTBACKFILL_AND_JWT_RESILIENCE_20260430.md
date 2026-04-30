# CTO Briefing — ADVI_INFLEC: Historical Dim Backfill + Orion JWT Resilience
**Date:** 2026-04-30
**Author:** 0.6.1_AE_PartnerETL (with 0.7.0_AE_CloudOps consult on JWT)
**For:** CTO project registration

---

## Executive Summary

Two gaps surfaced during a silver-layer coverage audit today. Both warrant new project registrations.

1. **Historical dim backfill:** Every Orion API dimension table (accounts, reps, positions, holdings, household, billing, activity, performance) has zero historical depth — only days of snapshots exist. Transactions go back to 2020-05-26 (1,502 files). The dimension tables that contextualise those transactions are missing six years of history. This gap makes lookback analysis and any time-series attribution incorrect or impossible.

2. **Orion JWT 401 resilience:** Today's bronze pull failed completely (0/5 dims, `{"overall":"failure","ok":0,"fail":5}`) because the Orion session JWT expired at 09:09Z and the daily auto-refresh cron misfired. Silent 401s cause data outages that are only discovered downstream when gold scripts produce wrong output or zero rows. The fix requires a freshness-check layer before any bronze pull and a defined recovery path.

---

## 1. Silver Layer Coverage Audit — Current State

Audit run against `s3://opal-data-inf/silver/` and `bronze/` on 2026-04-30.

### api_dims (snapshot-partitioned dims)

| Dim | Earliest Snapshot | Count | Gap vs Transactions |
|---|---|---|---|
| `accounts_v2` | 2026-04-28 | 2 | ~2,162 days missing |
| `billing` | 2026-04-28 | 2 | ~2,162 days missing |
| `household` | 2026-04-28 | 1 | ~2,162 days missing |
| `activity` | 2026-04-28 | 1 | ~2,162 days missing |
| `performance` | 2026-04-28 | 1 | ~2,162 days missing |
| `assets_v2` | 2026-04-29 | 1 | ~2,161 days missing |
| `household_rep_mapping` | 2026-04-29 | 1 | ~2,161 days missing |
| `positions_mv` | 2026-04-30 | 1 | ~2,160 days missing |
| `assets` (legacy, deprecated) | 2026-04-20 | 1 | — |

### Other silver tables

| Table | Earliest Date | Count | Notes |
|---|---|---|---|
| `silver/transactions/` | 2020-05-26 | 1,502 | Full history — reference baseline |
| `silver/aum_snapshot/` | 2026-04-21 | 2 | Only 2 snapshots; no history |
| `silver/accounts_dim/` | — | 1 (latest.parquet) | Point-in-time, no partitioning |
| `silver/prices/` | — | 1 (canonical_prices.parquet) | Time series internal to file |

### Bronze layer

| Prefix | Earliest Date | Notes |
|---|---|---|
| `bronze/orion-api/` | 2026-04-28 | Only 3 run dates |
| `bronze/orion-api-v2/` | 2026-04-29 | Only 2 run dates |
| `bronze/orion/` | 2026-04-21 | Only 2 run dates |

**No historical bronze backfill exists.** The bronze layer must be backfilled first (Orion API pulls), then silver converts built on top.

---

## 2. Historical Backfill Project

### Problem

Attribution, performance measurement, and any multi-year analysis that joins transactions to dimensions (reps, households, positions, accounts) can only use today's dimension snapshot. If a rep changed firms in 2023, today's `household_rep_mapping` snapshot will misattribute 2023 transactions to the wrong rep. There is no way to reconstruct the correct join at any historical point.

### Scope

Backfill the following for every date from **earliest available Orion API history** (target: matching or exceeding `silver/transactions/` origin date of 2020-05-26):

| Dim | Bronze pull script | Silver convert | Snapshot key |
|---|---|---|---|
| `accounts_v2` | `pull_inflection_new_portfolio.py` | `convert_orion_api_to_silver.py --dim accounts_v2` | `--snapshot-date` |
| `household` | `pull_unified_account_dim.py` | `convert_orion_api_to_silver.py --dim household` | `--snapshot-date` |
| `household_rep_mapping` | `pull_inflection_representatives.py` | `convert_orion_api_to_silver.py --dim household_rep_mapping` | `--snapshot-date` |
| `billing` | `orion_billing_dim.py` | `convert_orion_api_to_silver.py --dim billing` | `--snapshot-date` |
| `activity` | (via unified_account_dim) | `convert_orion_api_to_silver.py --dim activity` | `--snapshot-date` |
| `performance` | (via unified_account_dim) | `convert_orion_api_to_silver.py --dim performance` | `--snapshot-date` |
| `positions_mv` | `pull_inflection_positions_daily.py` | `convert_orion_api_to_silver.py --dim positions_mv` | `--snapshot-date` |
| `assets_v2` | `pull_inflection_assets_v2.py` | `convert_assets_v2_to_silver.py` | `--snapshot-date` |
| `aum_snapshot` | (gold script) | (gold script) | date-partitioned |

### Constraints and Risks

**Orion API availability of historical data:** The central unknown. Orion's API endpoints accept date-range parameters for some dims (e.g., `transactions` supports `createdDateStart`), but others return current state only (no `as-of` date support). This must be confirmed via API exploration before committing to full backfill scope. Some dims may not support historical pulls — for those, the earliest available date is the current snapshot.

**API rate limiting / throttling:** Pulling 2,000+ dates × 8 dims = ~16,000 API calls minimum. The positions pull already documents ~8,820 calls for a 30-day window (294 clients × 30 dates × 1.0s). A 6-year backfill could be 2M+ calls over several days of serial execution. Rate limits, session expiry mid-run, and EC2 cost are real factors.

**JWT refresh cadence during backfill:** A multi-day backfill will cycle through many JWT refresh windows. The JWT resilience work (Section 3) must be completed before the backfill starts to avoid 401-induced partial runs.

**Storage:** 1,502 transaction files total. Dim snapshots will likely be smaller per file. Estimate 500-2,000 parquet files per dim for a full backfill — manageable in S3.

### Proposed Design

**Phase 0 — API capability probe (DS):** For each dim, confirm whether the Orion API accepts an `as-of` or `date` parameter and returns historical state, or only current state. Output: a dim-by-dim backfill eligibility matrix with earliest provable date.

**Phase 1 — Bronze backfill (DS + AE):** Extend each pull script with `--backfill-start / --backfill-end` flags if not already present. `pull_inflection_positions_daily.py` already has `--backfill-days N` and `--start/--end` support; use as the reference pattern. Run bronze pulls date-by-date (not parallel to respect rate limits) against each backfill-eligible dim.

**Phase 2 — Silver backfill (DS):** For each bronze date partition, run the corresponding silver convert with `--snapshot-date {date}`. These are stateless transforms — can be parallelised per dim once bronze is complete.

**Phase 3 — Gold re-run (DS + AE):** Re-run affected gold scripts (`INF_B_00`, `INF_A_00`, downstream) for each historical date where dimension data now exists. This is a major chain operation — scope to be defined after Phases 1-2.

**Phase 4 — Ongoing:** Daily dispatch chain already handles forward-looking dim pulls (DIAGFIX.010, .011, .012). Backfill is a one-time catch-up.

### Suggested Project Code

`ADVI_INFLEC_HISTBF` or `INFLEC_HISTBF` — register under the ADVI macro.

---

## 3. Orion JWT Resilience

*Coordinated with 0.7.0_AE_CloudOps (CONSULT response 20260430T150504Z).*

### Current Architecture

There is a single Orion token type: a session JWT (~10h TTL) captured via Playwright network interception (`Authorization: Session {jwt}` header from Orion web UI). There is no Orion-issued API key, refresh token, or long-lived JWT — the only long-duration credential is the browser storage state (device cookie, ~30-90 day TTL) which allows skip-OTP re-login, not direct API calls.

The JWT is stored in two places:
- **Secrets Manager:** `orion/jwt/current` (raw JWT string, added v1.7.5 today)
- **S3:** `s3://opal-data-inf/orion/jwt/current.json` (JWT + `issued_at_iso`, `expires_at_iso`, `ttl_seconds`, claims)

Both are written simultaneously on every successful JWT fetch (`orion_export.ts` lines 479-480).

### Daily Refresh Chain

```
EventBridge cron (08:13 ET / 12:13Z)
  → inf-jwt-trigger Lambda
    → starts inf-exporter EC2
      → SSM RunCommand (opal-inf-jwt-fetch)
        → orion_export.ts --mode jwt-extract
          → Playwright captures Authorization: Session header
            → writes SM orion/jwt/current + S3 orion/jwt/current.json
```

EC2 boot-to-JWT latency: ~13 minutes. JWT is valid until ~18:13 ET / 22:13Z — giving a ~10h window for all downstream bronze pulls.

### Today's 401 Root Cause

The 12:13Z cron fired 14 minutes before v1.7.1 Lambda code was deployed (12:27Z). The old Lambda code wrote the mode marker then exited without starting EC2. The previous JWT (issued ~2026-04-29T23:08Z, expiry ~09:09Z) had already expired. Result: every bronze dim call returned 401.

Secondary: v1.7.1's first real run at 14:13Z hit an EC2→SSM agent registration race (`InvalidInstanceId`). Fixed by `_send_ssm_with_retry()` (v1.7.4, 5 retries × 30s). Both fixes are now live.

### What "Long-term JWT with fallback to short-term" Means in Practice

Given there is only one token class, the correct framing is:

**Primary path:** Read JWT from SM `orion/jwt/current` (or S3 JSON). Check `expires_at_iso`. If TTL > 30 minutes remaining, use it.

**Fallback path:** If TTL <= 30 minutes or token is absent/malformed: trigger emergency JWT refresh (invoke `inf-jwt-trigger` Lambda), poll for up to 15 minutes, then proceed with fresh token.

**Fail-fast path:** If refresh times out or fails: emit CloudWatch metric `JwtNearExpiry` / `JwtRefreshFailed`, abort bronze pull with a clear error (`JWT_EXPIRED — abort`) rather than proceeding to silent 401s.

### Recommended Design (two-phase)

**Immediate (Option A — freshness check + fail-fast):**
- Add a `check_jwt_freshness()` helper to the bronze orchestrator (`data/orion/scripts/bronze/orchestrator.py`) and all standalone pull scripts
- Logic: read `expires_at_iso` from S3 JSON; if expired or TTL < 30 min, emit CW metric and exit non-zero with a clear message
- Ops team (or on-call) manually triggers `inf-jwt-trigger` Lambda, bronze re-runs once JWT is fresh
- Owner: DS (pull script changes) + AE 0.6.1/0.7.0 (CW metric, orchestrator)
- Complexity: low. No new infrastructure. Prevents silent data corruption.

**Follow-on (Option B — async auto-recovery):**
- On near-expiry, the bronze orchestrator invokes `inf-jwt-trigger` Lambda directly and polls SM `orion/jwt/current` until `issued_at_iso` advances or timeout (15 min)
- If recovered: continue. If timeout: emit CW alarm + abort
- Owner: AE 0.7.0 (Lambda invocation + polling loop)
- Complexity: medium. Requires IAM grant to invoke `inf-jwt-trigger` from bronze runner EC2 role

**Longer-term (Option C — direct REST auth, if Orion API supports it):**
- If Orion exposes a REST login endpoint (`POST /api/auth/login` accepting username+password), the orchestrator could directly re-authenticate using `orion/credentials` from SM, bypassing the Playwright path entirely
- This would reduce the emergency re-fetch latency from ~13 min (EC2 boot) to ~2-3 seconds
- Currently unconfirmed — requires API capability probe
- Owner: DS (probe) + AE (implementation if confirmed)

### Suggested Project Code

`ADVI_INFLEC_JWTRES` — or fold into existing `ADVI_ORIAPI` project as Phase 2.

---

## 4. Sequencing Recommendation

```
Now (pre-registered):
  ADVI_ORIAPI.005 deployed (inf-ec2-retry-launch, v1.7.2) ✓
  JWT SM path added (v1.7.5) ✓
  SSM retry logic (v1.7.4) ✓

Short-term (register now):
  ADVI_INFLEC_JWTRES Phase 1 — Option A freshness check (1-2 days, DS + AE)
  ADVI_INFLEC_HISTBF Phase 0 — API capability probe (DS, 1-2 days)

Medium-term (sequence after Phase 0 result):
  ADVI_INFLEC_JWTRES Phase 2 — Option B async auto-recovery (AE 0.7.0, 3-5 days)
  ADVI_INFLEC_HISTBF Phase 1-2 — Bronze + silver backfill (DS + AE, duration TBD by probe result)

Longer-term:
  ADVI_INFLEC_HISTBF Phase 3 — Historical gold chain re-runs
  ADVI_INFLEC_JWTRES Phase 3 — Option C REST auth (if Orion confirms endpoint)
```

---

## 5. Open Questions for CTO Decision

1. **Backfill date target:** Is the goal to match `silver/transactions/` origin (2020-05-26), or is there a more recent "firm inception" date that represents real data? Confirms backfill scope.

2. **Dim priority order:** If Orion API limits historical depth on some dims, which dims are highest priority for lookback? (Recommendation: `household_rep_mapping` → `accounts_v2` → `positions_mv`, since these drive attribution.)

3. **JWT resilience owner:** Does this go to AE 0.7.0 as a standing ADVI_ORIAPI extension, or to DS as part of the bronze pull layer?

4. **Orion API rate limits:** Does Andrew have contact at Orion to confirm API throttle policy and whether historical as-of pulls are supported? This is the Phase 0 blocker.

---

*Prepared by 0.6.1_AE_PartnerETL | 2026-04-30 | JWT architecture facts from 0.7.0_AE_CloudOps consult*
