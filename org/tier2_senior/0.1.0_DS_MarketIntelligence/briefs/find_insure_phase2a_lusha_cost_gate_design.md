# FIND_INSURE Phase 2A — Lusha Cost-Gate Lambda Integration Design (sibling brief)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 (lifecycle), §3.5 (IAM), §9 Q4 (cost budget Andrew-route), §11 (cross-domain)
**Lusha reference:** `docs/reference/lusha-api-v3.md` §5 (rate limits), §6 (error codes), §8 (billing model)
**Companion brief:** `find_insure_phase2_part_a_linkedin_scaffold.md` v0.3 `b0534a7d3` (Phase 2A parse + score + Series detection scaffold)
**Pod:** 0.1.0_DS_MarketIntelligence~C
**Author:** 0.1.0_DS_MarketIntelligence~C (DS scaffold sibling; pre-Phase-2A-TO-authoring)
**Trigger:** ws COO `[RAVC2-ACCEPT-SCAFFOLD]` 17:25Z parallel-prep Option 1 pick
**Status:** sibling design brief — pre-Phase-2-execution; cost-gate machinery for `crawl_linkedin_bronze` Lambda + extensible pattern for Phase 1 Bright Data calls
**Sizing:** ~45min wall (scaffold scope; no impl)

---

## 1. Scope

This sibling brief designs the **cost-gate machinery** for `crawl_linkedin_bronze` (and by extension any other FIND_INSURE Lambda calling a metered external API). Companion to the Phase 2A scaffold brief — that brief covers parse/score/Series-detection; this brief covers the structural cost-safety surface that protects against runaway credit burn.

**Why a sibling not a body section:** the cost-gate machinery is **load-bearing for Phase 2A first-run safety** (Lusha bills per credit; runaway = real cost + Andrew alert), substantive enough to deserve standalone architectural attention, and **extensible** — the same pattern applies to Phase 2 Part B Bright Data calls + future FIND-macro metered-API integrations. Folding into the parent scaffold would over-load that brief.

**What this brief is not:** not impl, not a TO, not a Lambda. It's the design substrate ws COO + AE 0.7 + DS draw on when authoring the Phase 2A TO triad (specifically `crawl_linkedin_bronze`).

---

## 2. The shape of the cost-safety problem

Per Lusha v3 doc §8 (billing) + §5 (rate limits), every successful Lusha call:
- Charges credits per action (`api_search` per Search result; `revealEmail` + `revealPhone` per Enrich field; `reveal_company` per company Enrich; `lookalikeContact`/`lookalikeCompany` per result; signals per matched signal)
- Returns `billing.creditsCharged` in response (authoritative per-call total)
- Returns `x-rate-limit-{daily,hourly,minute}` + `x-{daily,hourly,minute}-requests-left` + `x-{daily,hourly,minute}-usage` headers (rate-limit window state)
- Can return `402 Payment Required` (insufficient credits), `429 Too Many Requests`, `451 Unavailable for Legal Reasons` (GDPR), `401`/`403` (key/account state), or `5XX` (server)

**Phase 2A worst-case naive scope:** 100 IMOs × ~10 leadership × (`api_search` + `revealEmail` + `revealPhone` + company `reveal_company`) ≈ 3500 credit-events. Phase-1-subset gate (top quintile + Series-mention) reduces to ~20-25 IMOs × ~10 ≈ 700-900.

**Why this is load-bearing:**
- Credits cost real money (Andrew sovereign budget per PRD Q4); silent overspend = unrecoverable
- Rate-limit breach (`429`) silent-retry-spam = account suspension risk
- GDPR `451` silent-iteration = compliance exposure
- `402` silent-retry-cycle = credit-floor breach + alert lag for IR-team-budget-watcher

The cost-gate machinery makes all four failure-classes **structural** (gate-enforced + telemetry-emitted + soft-stop-aborted), not cultural (developer-remembered).

---

## 3. Cost-budget config schema

Per PRD §3.2 (`config/` prefix) + §3.4 (lifecycle: `config/*` NEVER expire) + §3.5 (IAM: `find-insure-lambda-role` `s3:GetObject` on `config/*`).

**Config artifact:** `s3://opal-data-imo/config/cost-budgets-v0.1.json` (v0.1 binds; v0.2+ revisions bump version + re-point Lambda).

**Schema (v0.1 default values per ws CTO Q4 disposition `20260527T170844Z` + LD-0090 binding):**

```json
{
  "schema_version": "v0.1",
  "config_authored": "2026-05-27T17:25Z",
  "authority": "ws CTO arch-disposition 20260527T170844Z; LD-0090 ALWAYS-PROCEED (Andrew sovereign override window via PRD Q4)",
  "per_imo_ceilings": {
    "lusha_credits_per_imo": 50,
    "lusha_credits_per_imo_class": {
      "api_search": 15,
      "revealEmail": 10,
      "revealPhone": 10,
      "reveal_company": 5,
      "lookalikeContact": 0,
      "lookalikeCompany": 0,
      "showSignalsContact": 0,
      "showSignalsCompany": 0
    }
  },
  "global_ceilings": {
    "lusha_credits_daily_global": 1500,
    "lusha_credits_monthly_global": 30000
  },
  "rate_limit_floors": {
    "x-minute-requests-left_floor": 5,
    "x-hourly-requests-left_floor": 50,
    "x-daily-requests-left_floor": 200
  },
  "abort_semantics": {
    "abort_class": "soft_stop",
    "post_abort_resume_strategy": "next_imo_after_imo_slug_at_abort",
    "telemetry_required_on_abort": true,
    "alert_chain_on_abort": ["AE 0.7", "ws COO"]
  },
  "error_class_disposition": {
    "402_payment_required": {"action": "hard_halt", "alert": ["AE 0.7", "ws COO", "IR-team-budget-watcher"]},
    "429_too_many_requests": {"action": "exponential_backoff", "initial_ms": 1000, "doubling": true, "max_ms": 60000, "max_retries": 5},
    "451_unavailable_legal": {"action": "skip_entity_log_telemetry", "alert": []},
    "401_unauthorized": {"action": "hard_halt", "alert": ["AE 0.7"]},
    "403_forbidden": {"action": "hard_halt", "alert": ["AE 0.7"]},
    "5XX_server": {"action": "exponential_backoff", "initial_ms": 1000, "doubling": true, "max_ms": 60000, "max_retries": 5},
    "499_client_closed": {"action": "skip_entity_log_telemetry", "alert": []}
  },
  "alert_channels": {
    "AE 0.7": "broker_mcp",
    "ws COO": "broker_mcp",
    "IR-team-budget-watcher": "sns:find-insure-budget-alerts"
  },
  "overshoot_tolerance": {
    "overshoot_tolerance_pct": 5,
    "tolerance_rationale": "eventually-consistent DDB + concurrent Lambdas worst-case 5% over hard ceiling; v0.1 empirical-first-run posture per CTO Q-C3 ratify 20260527T17:46Z",
    "tighten_path": "DDB conditional-update at gate-check tier (Q-C3 follow-up authoring if Andrew demands tighter post-first-run)"
  },
  "per_imo_lambda_timeout": {
    "max_calls_per_imo_per_run": 20,
    "max_calls_rationale": "Lambda 15min ceiling vs worst-case ~30 calls × (1s API + 60s rate-limit pause) ~30min per IMO (UNK-D); hard-cap structural-safe; CTO Q-C4 ratify pending AE 0.7 final-ratify next /work cycle",
    "soft_abort_class": "per_imo_call_cap",
    "ec2_fallback_per_prd": "PRD §3.3 EC2 fallback preserved as escape valve if any single IMO routinely overshoots 20-call cap"
  }
}
```

**Per-endpoint-class sub-budgets (per_imo_ceilings.lusha_credits_per_imo_class):** prevents pathological allocation — e.g. if a single IMO's Lusha search returns 100 contacts and the Lambda naively enriches all, the per-class `revealEmail` ceiling of 10 caps at the natural worst-case (~10 leadership per IMO). Sum of per-class ceilings can exceed the top-level `lusha_credits_per_imo` (50) — the latter is the hard ceiling, the former are soft sub-ceilings that abort the specific endpoint class early.

**Rate-limit floor semantics:** when a Lusha response returns `x-minute-requests-left <= 5`, the Lambda **pauses the current IMO scan** (does NOT abort) for ~60s + retries on the next minute window. Floor values are conservative (5 minute-requests buffer) — empirical-tightening at first-run.

---

## 4. Pre-call gate machinery

Before EACH Lusha API call, `crawl_linkedin_bronze` runs the gate-check function. Pseudocode (illustrative; not impl):

```python
from __future__ import annotations  # CLAUDE.md Rule 15
from dataclasses import dataclass

@dataclass
class GateCheckResult:
    proceed: bool
    abort_class: str | None  # "per_imo" | "global_daily" | "global_monthly" | "rate_limit_floor" | None
    reason: str

def pre_call_gate_check(
    endpoint_class: str,           # "api_search" | "revealEmail" | ...
    imo_slug: str,
    state: CostGateState,          # see §6 for state-persistence design
    config: dict,                  # parsed cost-budgets-v0.1.json
) -> GateCheckResult:
    # 1. Per-IMO endpoint-class sub-ceiling
    per_imo_class_used = state.get_per_imo_class_used(imo_slug, endpoint_class)
    per_imo_class_ceiling = config["per_imo_ceilings"]["lusha_credits_per_imo_class"][endpoint_class]
    if per_imo_class_used >= per_imo_class_ceiling:
        return GateCheckResult(False, "per_imo_class", f"per_imo {imo_slug} {endpoint_class} ceiling {per_imo_class_ceiling}")

    # 2. Per-IMO total ceiling
    per_imo_total_used = state.get_per_imo_total_used(imo_slug)
    per_imo_total_ceiling = config["per_imo_ceilings"]["lusha_credits_per_imo"]
    if per_imo_total_used >= per_imo_total_ceiling:
        return GateCheckResult(False, "per_imo", f"per_imo {imo_slug} total ceiling {per_imo_total_ceiling}")

    # 3. Global daily ceiling
    global_daily_used = state.get_global_daily_used()
    global_daily_ceiling = config["global_ceilings"]["lusha_credits_daily_global"]
    if global_daily_used >= global_daily_ceiling:
        return GateCheckResult(False, "global_daily", f"global daily ceiling {global_daily_ceiling}")

    # 4. Global monthly ceiling
    global_monthly_used = state.get_global_monthly_used()
    global_monthly_ceiling = config["global_ceilings"]["lusha_credits_monthly_global"]
    if global_monthly_used >= global_monthly_ceiling:
        return GateCheckResult(False, "global_monthly", f"global monthly ceiling {global_monthly_ceiling}")

    # 5. Rate-limit floor (from last response's headers; see §5)
    last_headers = state.get_last_rate_limit_headers()
    minute_left = last_headers.get("x-minute-requests-left", 999)
    minute_floor = config["rate_limit_floors"]["x-minute-requests-left_floor"]
    if minute_left <= minute_floor:
        # PAUSE not ABORT — sleep + retry next window
        return GateCheckResult(False, "rate_limit_floor", f"x-minute-requests-left {minute_left} <= floor {minute_floor}; pause + retry")

    return GateCheckResult(True, None, "all gates clear")
```

**Gate-failure handling:**
- `per_imo_class` / `per_imo` → close out current IMO (write partial bronze + telemetry) + advance to next IMO
- `global_daily` / `global_monthly` → **soft-stop abort** (write current IMO partial + telemetry `cost_ceiling_hit: true` + clean exit; resume next-run from next IMO)
- `rate_limit_floor` → **pause** (sleep ~60s + retry; not abort — rate-limit windows reset on schedule)

---

## 5. Per-call header capture + post-call billing accumulation

```python
def execute_lusha_call(
    endpoint_class: str,
    imo_slug: str,
    request_payload: dict,
    state: CostGateState,
    config: dict,
) -> dict:
    gate_result = pre_call_gate_check(endpoint_class, imo_slug, state, config)
    if not gate_result.proceed:
        handle_gate_failure(gate_result, imo_slug, endpoint_class, state, config)
        # function returns or raises per abort-class semantics

    response = http_post(LUSHA_ENDPOINTS[endpoint_class], request_payload, headers={"api_key": LUSHA_API_KEY})

    # Capture rate-limit headers FIRST (informs next-call gate)
    rate_limit_headers = {
        "x-rate-limit-daily": response.headers.get("x-rate-limit-daily"),
        "x-daily-requests-left": response.headers.get("x-daily-requests-left"),
        "x-daily-usage": response.headers.get("x-daily-usage"),
        "x-rate-limit-hourly": response.headers.get("x-rate-limit-hourly"),
        "x-hourly-requests-left": response.headers.get("x-hourly-requests-left"),
        "x-hourly-usage": response.headers.get("x-hourly-usage"),
        "x-rate-limit-minute": response.headers.get("x-rate-limit-minute"),
        "x-minute-requests-left": response.headers.get("x-minute-requests-left"),
        "x-minute-usage": response.headers.get("x-minute-usage"),
    }
    state.update_rate_limit_headers(rate_limit_headers)

    # Handle error-class FIRST (no billing on errors EXCEPT 451 may charge — verify Lusha doc)
    if response.status_code != 200:
        handle_error_class(response, imo_slug, endpoint_class, state, config)
        # function returns, raises, or sleeps per disposition

    # Billing accumulation
    payload = response.json()
    credits_charged = payload.get("billing", {}).get("creditsCharged", 0)
    state.increment_per_imo_total(imo_slug, credits_charged)
    state.increment_per_imo_class(imo_slug, endpoint_class, credits_charged)
    state.increment_global_daily(credits_charged)
    state.increment_global_monthly(credits_charged)

    # Per-call telemetry record (emit IMMEDIATELY — survives Lambda crash)
    emit_telemetry({
        "ts": utc_iso8601(),
        "lambda": "find-insure-crawl-linkedin",
        "imo_slug": imo_slug,
        "endpoint_class": endpoint_class,
        "credits_charged": credits_charged,
        "rate_limit_headers": rate_limit_headers,
        "status_code": response.status_code,
        "request_id": payload.get("request_id"),  # if Lusha provides
    })

    return payload
```

**Header-capture priority:** rate-limit headers MUST be captured before any error-handling branch (`429` returns headers too; capture informs back-off duration). Headers persisted in `state` for the next pre-call gate check.

---

## 6. State persistence — DynamoDB vs Lambda-memory

**Problem:** Phase 2A Lambdas fan-out per IMO (one Lambda invocation per IMO from EventBridge orchestration). The `global_daily_used` counter must be **atomic across concurrent invocations** — if 5 Lambdas process 5 IMOs in parallel and each thinks they have the full daily budget, the global ceiling is silently breached.

**Options:**

| Option | Atomic? | Cost | Cold-start | Recommendation |
|---|---|---|---|---|
| A. Lambda-memory only | ❌ no — per-invocation only | $0 | n/a | NO — fails the atomicity test |
| B. S3 read-modify-write `s3://opal-data-imo/telemetry/cost-state/daily-state.json` | ❌ race condition between read + write | ~$0 | small | NO — same atomicity failure |
| C. DynamoDB single-table with atomic `UpdateExpression ADD credits :n` | ✅ yes | ~$1/month for FIND_INSURE write volume | ~50ms first call (cold-start) | **YES — recommended** |
| D. SQS FIFO with single consumer | ✅ yes (serialized) | ~$1/month | medium | NO — over-engineered; serializes Lambdas unnecessarily |
| E. ElastiCache Redis with INCR | ✅ yes | ~$15/month (smallest Redis node) | low | NO — over-engineered for the volume |

**Recommendation: Option C — DynamoDB single-table.**

**Schema (DynamoDB table `find-insure-cost-state`):**

```
Partition key: pk (str)
Sort key:      sk (str)

Items:
  pk = "global"             sk = "daily#2026-05-27"         credits_used: 247
  pk = "global"             sk = "monthly#2026-05"          credits_used: 5832
  pk = "imo#wlth-rx"        sk = "total#2026-05-27"         credits_used: 32
  pk = "imo#wlth-rx"        sk = "class#api_search#2026-05-27"        credits_used: 8
  pk = "imo#wlth-rx"        sk = "class#revealEmail#2026-05-27"       credits_used: 12
  pk = "imo#wlth-rx"        sk = "class#revealPhone#2026-05-27"       credits_used: 10
  pk = "imo#wlth-rx"        sk = "class#reveal_company#2026-05-27"    credits_used: 2
  pk = "headers"            sk = "last_rate_limit"          x-minute-requests-left: 18, x-hourly-requests-left: 247, x-daily-requests-left: 4521, captured_at: 2026-05-27T17:31:22Z
```

**TTL:** 7 days from item creation — daily/monthly items naturally roll off; `headers` item is overwrite-only.

**Atomic increment:**
```python
ddb.update_item(
    TableName="find-insure-cost-state",
    Key={"pk": "global", "sk": "daily#2026-05-27"},
    UpdateExpression="ADD credits_used :n",
    ExpressionAttributeValues={":n": credits_charged},
    ReturnValues="UPDATED_NEW",
)
# Returns new value atomically; gate check uses this.
```

**Gate check:** `state.get_global_daily_used()` reads (eventually-consistent) from DynamoDB — acceptable because the AddExpression is atomic-write, and worst-case eventually-consistent stale-read overshoots ceiling by a single in-flight call (well below ceiling tolerance).

**Cost:** ~50 IMOs × ~30 Lusha calls × 4 DDB writes/call = ~6000 DDB-write-units per Phase 2A first-run. On-demand pricing ≈ $0.0075. Annual amortized = trivial.

**Cold-start:** ~50ms first DDB call per Lambda cold-start — acceptable.

**IAM amendment to PRD §3.5:** `find-insure-lambda-role` gains `dynamodb:UpdateItem` + `dynamodb:GetItem` + `dynamodb:Query` on `arn:aws:dynamodb:{region}:{account}:table/find-insure-cost-state`. Sub-Phase-0 addition; PRD v0.4 candidate (route ws CTO).

---

## 7. Soft-stop abort semantics + telemetry record

When the global daily or monthly ceiling trips, the Lambda **completes the current Lusha call's bronze write** (no partial-IMO data-loss) + emits a soft-stop telemetry record + exits cleanly:

```json
{
  "ts": "2026-05-27T17:42:18Z",
  "lambda": "find-insure-crawl-linkedin",
  "run_id": "find-insure-crawl-linkedin-20260527-174218-abc123",
  "event_class": "cost_ceiling_hit",
  "ceiling_class": "global_daily",
  "ceiling_value": 1500,
  "credits_used_at_abort": 1502,
  "imo_slug_at_abort": "wlth-rx",
  "imos_processed_this_run": 17,
  "imos_remaining": 8,
  "next_imo_at_resume": "agent-pipeline",
  "alert_chain_triggered": ["AE 0.7", "ws COO"],
  "rate_limit_headers_at_abort": {
    "x-minute-requests-left": 17,
    "x-hourly-requests-left": 213,
    "x-daily-requests-left": 4503
  }
}
```

**Telemetry path:** `s3://opal-data-imo/telemetry/find-insure-crawl-linkedin/{YYYY-MM-DD}/{run-id}.ndjson` per PRD §3.2. Per-call records + the soft-stop record both append to the same ndjson file.

**Resume strategy:** the next-run EventBridge dispatch reads the latest telemetry's `next_imo_at_resume` and starts from there. Implementation choice: either (a) DDB-table-tracked `next_imo_cursor` updated atomically alongside cost accumulators, or (b) telemetry-derived (parse last `.ndjson` of the previous day looking for `event_class: cost_ceiling_hit`). DDB-cursor is cleaner; ndjson-derived is more recoverable if DDB has issues.

**Alert chain:** broker MCP to AE 0.7 + ws COO on soft-stop; broker MCP to AE 0.7 + ws COO + IR-team-budget-watcher on hard-halt (`402`/`401`/`403`). Alert-channel for IR-team-budget-watcher TBD per config (Andrew direct or SNS topic; route Andrew at Phase 2A dispatch).

---

## 8. Run-metadata.json shape (bronze emit)

Each `crawl_linkedin_bronze` run writes a `run-metadata.json` to `bronze/linkedin-scrape/{slug}/{YYYY-MM-DD}/` (consumed by `parse_linkedin_silver` for lineage):

```json
{
  "schema_version": "v1.0",
  "run_id": "find-insure-crawl-linkedin-20260527-174218-abc123",
  "imo_slug": "wlth-rx",
  "lusha_company_id": 12345678,
  "started_at": "2026-05-27T17:38:12Z",
  "ended_at": "2026-05-27T17:42:18Z",
  "ended_class": "completed" | "soft_stop_global_daily" | "soft_stop_per_imo" | "error_hard_halt" | "rate_limit_floor_pause",
  "lusha_endpoint_calls": [
    {
      "endpoint_class": "api_search",
      "endpoint_url": "POST /v3/companies/search",
      "credits_charged": 1,
      "status_code": 200,
      "captured_rate_limit_minute_left": 24
    },
    {
      "endpoint_class": "api_search",
      "endpoint_url": "POST /v3/contacts/prospecting",
      "credits_charged": 8,
      "status_code": 200,
      "captured_rate_limit_minute_left": 23
    },
    {
      "endpoint_class": "revealEmail",
      "endpoint_url": "POST /v3/contacts/enrich",
      "credits_charged": 10,
      "status_code": 200,
      "captured_rate_limit_minute_left": 22
    },
    {
      "endpoint_class": "revealPhone",
      "endpoint_url": "POST /v3/contacts/enrich",
      "credits_charged": 10,
      "status_code": 200,
      "captured_rate_limit_minute_left": 21
    },
    {
      "endpoint_class": "reveal_company",
      "endpoint_url": "POST /v3/companies/enrich",
      "credits_charged": 3,
      "status_code": 200,
      "captured_rate_limit_minute_left": 20
    }
  ],
  "credits_total_this_imo": 32,
  "ceiling_state_at_end": {
    "per_imo_used": 32,
    "per_imo_ceiling": 50,
    "global_daily_used": 1502,
    "global_daily_ceiling": 1500
  },
  "error_log": [],
  "ended_reason": "cost ceiling hit global_daily at credits 1502"
}
```

`ended_class` enum and `error_log` schema enable downstream silver/gold tier to detect partial-IMO data — e.g. silver should mark rows from an `soft_stop_*` IMO with a `bronze_partial: true` flag so gold/serving can decide handling.

---

## 9. Error-class disposition (Lusha v3 §6 mapping)

Folded into `config/cost-budgets-v0.1.json` `error_class_disposition` per §3. Discipline summary:

| Status | Action | Alert | Retry |
|---|---|---|---|
| `200` | proceed (capture billing + rate-limit headers + bronze append) | — | — |
| `400` | log + skip entity + telemetry record `400_bad_request`; do NOT retry (request shape issue) | (none) | no |
| `401` | **hard_halt** + alert AE 0.7 (API key invalid) | AE 0.7 | no |
| `402` | **hard_halt** + alert AE 0.7 + ws COO + IR-team-budget-watcher (credit floor breach) | AE+COO+IRBW | no |
| `403` | **hard_halt** + alert AE 0.7 (account inactive) | AE 0.7 | no |
| `404` | log + skip entity + telemetry (endpoint/resource gone) | (none) | no |
| `429` | exponential back-off (initial 1s, doubling, max 60s, max 5 retries); honor `x-minute-requests-left` floor | (none unless max-retries-exceeded → COO) | yes |
| `451` | log + skip entity + telemetry record `451_gdpr_blocked`; **DO NOT enrich opted-out contact** | (none) | no |
| `499` | log + skip entity + telemetry (client closed/timeout) | (none) | no |
| `5XX` | exponential back-off (initial 1s, doubling, max 60s, max 5 retries) | (none unless max-retries-exceeded → AE 0.7) | yes |

**Alert chain implementation:** broker MCP via `mcp__opal-agent-comms__send_message(from_agent="0.7.0_AE_CloudOps lambda-find-insure-crawl-linkedin", to_agent="0.7.0_AE_CloudOps", subject="[HARD-HALT] find-insure-crawl-linkedin {error_class}", body=...)` — Lambda authors a temporary broker-channel handle for the alert path (or via SNS → Lambda → broker MCP, depending on AE 0.7 preference at TO authoring).

**`451` handling = GDPR alignment:** when Lusha returns `451 Unavailable For Legal Reasons` on a specific contact, that contact is GDPR-blocked at the Lusha tier. Log the contactId + reason + skip the enrich — do NOT retry or surface as an error. Pre-search opt-out check (§6 ADDITIVE-1 of parent scaffold brief) reduces but doesn't eliminate `451` arrivals.

---

## 10. CVO unknown-unknowns (preemptive surfacing per Operating Doctrine §7)

**UNK-A (cost-counter overshoot at the boundary):** the gate-check is `>= ceiling` semantically; with eventually-consistent DDB reads + concurrent Lambda invocations, the actual overshoot at a hard ceiling can be `ceiling + N*max_credits_per_call` where N = max in-flight Lambda count. For a 1500-credit daily ceiling + ~5 concurrent Lambdas × max-15-credit-per-call, worst-case overshoot ≈ `1500 + 75 = 1575` (5% over). Documented + acceptable for v0.1; tighten via DDB conditional-update at the gate-check tier if Andrew demands tighter than 5%.

**UNK-B (per-class sub-ceiling sum > total ceiling):** `per_imo_ceilings.lusha_credits_per_imo_class` sums to 40 (15+10+10+5+0+0+0+0); `per_imo_ceilings.lusha_credits_per_imo = 50`. Headroom = 10 for unanticipated classes. By design — sub-ceilings are guidance, total is hard. If new endpoint class (e.g. Lookalikes activated at v0.2) eats into the 10-credit headroom unexpectedly, the per-IMO total ceiling catches it.

**UNK-C (telemetry-emit-on-error before broker-MCP):** the per-call telemetry record IS emitted in the error-handling branch too — `5XX` retries each emit their own telemetry record. This is intentional (debug + lineage) but means error storms inflate telemetry volume. Lifecycle rule `telemetry/*` Standard-IA 30d + expire 365d per PRD §3.4 absorbs the volume; if pathological, the 365d expiration is the safety valve.

**UNK-D (Lambda timeout vs cost-gate pause):** the rate-limit-floor pause uses `time.sleep(60)`. Lambda max execution is 15min — a single IMO Lusha-call burst can spend 60-120s on pauses + actual API calls. Worst-case IMO duration ≈ `~30 calls × (1s API + worst-case 60s rate-limit pause) ≈ 30min`. Exceeds Lambda 15min ceiling. Mitigation: hard-cap per-IMO calls at `max_calls_per_imo_per_run = 20` (config-tunable) + soft-abort to "resume next-run" if any IMO can't complete in budget. Alternative: EC2 fallback per PRD §3.3 ("EC2 fallback only if any single IMO crawl exceeds Lambda's 15min ceiling — Stage 1 will tell us"). Defer to TO-authoring empirical observation.

---

## 11. Acceptance criteria (sibling brief scaffold)

- **AC-C1.** Brief lands at `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase2a_lusha_cost_gate_design.md`.
- **AC-C2.** Cost-budget config schema (`config/cost-budgets-v0.1.json` per §3) with per-IMO + per-IMO-per-endpoint-class + global daily + global monthly + rate-limit floors + error-class disposition + alert chains.
- **AC-C3.** Pre-call gate machinery (per-IMO total + per-IMO-class + global daily + global monthly + rate-limit-floor; pause-vs-abort semantics).
- **AC-C4.** Per-call header capture (all 9 `x-{daily,hourly,minute}-{...}` headers per Lusha v3 §5) + billing accumulation (`billing.creditsCharged` per Lusha v3 §8) + immediate per-call telemetry emit.
- **AC-C5.** State persistence design (DynamoDB single-table `find-insure-cost-state` with atomic `ADD` increment; alternatives audited; cost + cold-start + IAM amendment to PRD §3.5 noted).
- **AC-C6.** Soft-stop abort semantics (current call completes + telemetry record + clean exit + resume strategy via next_imo_at_resume).
- **AC-C7.** Run-metadata.json bronze emit shape with `ended_class` enum.
- **AC-C8.** Error-class disposition table (all 10 status codes from Lusha v3 §6 mapped to action + alert chain + retry rule).
- **AC-C9.** Preemptive UNKs (A-D) surfaced per CVO Operating Doctrine §7.
- **AC-C10.** Cross-Lambda DDB table requires `find-insure-lambda-role` IAM amendment to PRD §3.5 (route ws CTO).

---

## 12. Open questions routed

- **Q-C1 (CTO):** DDB table `find-insure-cost-state` requires `find-insure-lambda-role` IAM amendment (PRD §3.5 sub-policy). On-demand pricing ~$1/year for the volume. v0.4 PRD amendment candidate.
- **Q-C2 (CTO):** IR-team-budget-watcher alert channel (`config.alert_channels.IR-team-budget-watcher`) — Andrew direct broker-MCP path? SNS topic? AE-managed bridge? Disposition before Phase 2A bronze TO authoring.
- **Q-C3 (Andrew + CTO):** ceiling overshoot tolerance — 5% overshoot at hard ceiling is acceptable v0.1 (per UNK-A); tighten via DDB conditional-update gates if Andrew demands tighter.
- **Q-C4 (AE 0.7 + CTO):** per-IMO Lambda-timeout-vs-pause budget (UNK-D) — defer EC2 fallback decision to empirical first-run; document the resume-next-run path explicitly.

---

## 13. Cross-references

- **Parent scaffold:** `find_insure_phase2_part_a_linkedin_scaffold.md` v0.3 `b0534a7d3`
- **PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.4 (lifecycle), §3.5 (IAM), §9 Q4 (Andrew cost-budget route)
- **Lusha doc:** `docs/reference/lusha-api-v3.md` §5 (rate limits), §6 (error codes), §8 (billing)
- **CTO Q4 disposition:** `20260527T170844Z_1.0.0_SA_CTO__ARCH-DISPOSITION__Q-S1_APPROVE_parquet_.md` (per-IMO 50 / daily 1500 defaults per LD-0090)
- **CVO ARCH-CORROBORATE:** `c55066712` (4-axis verdict; UNK-1 KMS upgrade tangent)
- **CLAUDE.md Rule 15:** `from __future__ import annotations` first import on Lambda source
- **Compiler-tools:** `comp-pipescript io data/find/imo/scripts/bronze/crawl_linkedin_bronze.py` + `comp-iam service find-insure-crawl-linkedin` (boto3 S3 + DDB + Secrets Manager surface)

---

## 14. RAVC2 chain

**To:** 2.0.0_SA_COO (ws COO; TO-author at Phase 2A bronze decomposition)
**CC:** 1.0.0_SA_CTO (PRD architect; Q-C1 IAM amendment + Q-C2 alert channel + Q-C3 tolerance disposition) + 3.0.0_SA_CVO (verifier-class arch-corroborate invite per LD-0022 + LD-0094 — cost-gate is exactly the kind of "what fires mid-IMO" empirical surface CVO Operating Doctrine §7 surfaces UNKs against) + 0.7.0_AE_CloudOps (Q-C4 timeout-budget + DDB provisioning + alert-channel infra) + 0.0.0_AB_MSTR (parallel-prep visibility)

Payload:
- Sibling brief commit hash
- 10 sub-deliverables AC-C1 through AC-C10 met
- 4 open questions Q-C1/Q-C2/Q-C3/Q-C4 explicit
- 4 preemptive UNKs A-D surfaced
- Recommended Phase 2A bronze TO scope expansion: cost-gate machinery is sub-deliverable of `crawl_linkedin_bronze` TO (not a separate TO); DDB table provisioning is sub-deliverable of AE 0.7 within the same TO

---

— 0.1.0_DS_MarketIntelligence~C 2026-05-27T~17:35Z (v0.1 sibling scaffold; ws COO RAVC2-ACCEPT-SCAFFOLD Option 1 parallel-prep pick)

---

## 15. v0.2 amendment — CTO Q-C1/Q-C2/Q-C3/Q-C4 dispositions absorbed (2026-05-27T~17:50Z)

ws CTO arch-disposition `20260527T17:46Z` cleared all 4 Q-C* open questions + committed PRD v0.4 bundle authoring next /ws-charter cycle. ~16min wall from sibling brief RAVC2-Request (17:39Z) to CTO disposition (17:46Z) — within Tier-1 disposition empirical band per banking notes.

### 15.1 Q-C1 (DDB single-table) — APPROVE

DDB single-table `find-insure-cost-state` standard fabric pattern (yang `yang-cost-state` analog; orion JWT refresh-burn analog). Cost trivial ~$1/yr; 50ms cold-start acceptable for rare cost-check path.

**IAM amendment** (`find-insure-lambda-role`):
- `dynamodb:UpdateItem + GetItem + Query` on `arn:aws:dynamodb:us-east-1:313476888478:table/find-insure-cost-state`

Lands in PRD v0.4 §3.5 (CTO bundle).

### 15.2 Q-C2 (IR-team-budget-watcher alert channel) — Option (b) SNS APPROVE

SNS topic `find-insure-budget-alerts` for fan-out. AE 0.7 provisions in imo-pipeline module amendment. Cost-gate Lambdas publish to topic on ceiling-hit. Initial subscriber: Andrew direct via email (AE 0.7 binds Andrew's preferred email at provisioning; ask Andrew direct or default admin email).

**IAM amendment** (`find-insure-lambda-role`):
- `sns:Publish` on `find-insure-budget-alerts` topic

Lands in PRD v0.4 §3.5 (CTO bundle). Cost-gate config schema §3 updated: `alert_channels.IR-team-budget-watcher` → `"sns:find-insure-budget-alerts"`.

### 15.3 Q-C3 (overshoot tolerance) — APPROVE empirical-first-run posture

5% overshoot at hard ceiling acceptable v0.1 (UNK-A). Tightening via DDB conditional-update at gate-check tier adds latency + complexity; not warranted pre-empirical evidence. First-run telemetry reveals actual overshoot variance; tighten then if Andrew demands.

**Schema addition** to `cost-budgets-v0.1.json` (per CTO transparency directive):

```json
"overshoot_tolerance": {
  "overshoot_tolerance_pct": 5,
  "tolerance_rationale": "eventually-consistent DDB + concurrent Lambdas worst-case 5% over hard ceiling; v0.1 empirical-first-run posture per CTO Q-C3 ratify",
  "tighten_path": "DDB conditional-update at gate-check tier (Q-C3 follow-up authoring if Andrew demands tighter post-first-run)"
}
```

Updated §3 schema this amendment.

### 15.4 Q-C4 (per-IMO Lambda timeout) — CTO APPROVE pending AE 0.7 final-ratify

CTO approves my proposed shape: `max_calls_per_imo_per_run = 20` hard-cap + soft-abort + telemetry record + EC2 fallback per PRD §3.3 preserved as escape valve. AE 0.7 final-ratify pending their next /work cycle (their lane primary on Lambda runtime envelope).

**Schema addition** to `cost-budgets-v0.1.json`:

```json
"per_imo_lambda_timeout": {
  "max_calls_per_imo_per_run": 20,
  "max_calls_rationale": "Lambda 15min ceiling vs worst-case ~30 calls × (1s API + 60s rate-limit pause) ~30min per IMO (UNK-D); hard-cap structural-safe",
  "soft_abort_class": "per_imo_call_cap",
  "ec2_fallback_per_prd": "PRD §3.3 EC2 fallback preserved as escape valve if any single IMO routinely overshoots 20-call cap"
}
```

Updated §3 schema this amendment. CC AE 0.7 same turn for final-ratify on Lambda envelope question.

### 15.5 PRD v0.4 bundle commitment (CTO authoring next /ws-charter)

CTO commits to single atomic v0.4 commit bundling:
- §3.1 SSE config `aws:s3:AES256` → `aws:kms` with `find-insure-data-key` CMK ARN (UNK-1)
- §3.5 IAM additions: `kms:GenerateDataKey`+`kms:Decrypt` (UNK-1) + `dynamodb:UpdateItem`+`GetItem`+`Query` (Q-C1) + `sns:Publish` (Q-C2)
- §3.6 NEW: KMS rotation guidance + cost-gate config schema reference + alert-channel SNS subscription guidance
- §3.7 NEW: overshoot tolerance documentation (Q-C3 empirical-first-run posture)
- §3.8 NEW: per-IMO Lambda timeout config (Q-C4 hard-cap + soft-abort + EC2-fallback escape)
- §4 Phase 0 deliverable 1: KMS resource + DDB table + SNS topic added to AE 0.7 .001 Terraform module
- Authoring lineage v0.4 citing UNK-1 + Q-C1/2/3/4 + this sibling brief v0.2 source

ETA: 1-2 /ws-charter cycles wall (~30-60min). Single atomic commit.

### 15.6 HARD CONSTRAINT chain (extended)

Phase 1 ships + Andrew subset cut + KMS upgrade lands + **DDB table provisioned** + **SNS topic provisioned + Andrew email bound** → Lusha live calls authorized.

Per LD-0090 ALWAYS-PROCEED:
- Andrew silent ≥1 cycle on UNK-1 KMS = Option 2 + 3 conditions bind ✓
- Andrew silent on Q-C1/Q-C2/Q-C3/Q-C4 = CTO dispositions bind via this MCP ✓

### 15.7 v0.2 amendment summary

- `cost-budgets-v0.1.json` schema §3 updated: alert_channels.IR-team-budget-watcher = SNS topic; overshoot_tolerance + per_imo_lambda_timeout objects added
- §15 added (this section) documenting Q-C1/Q-C2/Q-C3/Q-C4 dispositions + PRD v0.4 bundle commitment
- AE 0.7 CC for Q-C4 final-ratify on Lambda envelope question + Q-C2 SNS provisioning + KMS resource authoring
- Sibling brief v0.2 ratified scope-of-work for DS~E's FIND_INSURE.E2 concretization next /drive cycle

— 0.1.0_DS_MarketIntelligence~C 2026-05-27T~17:50Z (v0.2 sibling amendment — CTO Q-C1/2/3/4 dispositions absorbed; PRD v0.4 bundle commitment noted; schema updated with overshoot tolerance + per-IMO Lambda timeout)
