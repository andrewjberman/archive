# FIND_INSURE.024 — Phase 2A LIVE-DISPATCH Design Brief v0.1

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.7+ §4 Phase 2A
**TO:** [FIND_INSURE.024](../task_orders/FIND_INSURE.024.dsc-phase2a-live-dispatch-lushaai.md) — `<status>staged</status>` `<dispatch_held>true</dispatch_held>`
**Author:** 0.1.0_DS_MarketIntelligence~C 2026-05-28T00:14Z
**Authority anchor:** TO .024 Sequencing step 2 (pre-gate authoring) + MSTR-DIRECT SPAWN-WITH-DIRECTION 23:35Z + Andrew goal-set 22:49Z drive-through-Phase-3-close
**Sister-artifact dependencies (.027 4-artifact ship commit `91a721862`):**
- [lusha-endpoint-architecture-map.md](../../../../docs/reference/lusha-endpoint-architecture-map.md) (AC1) — endpoint coverage classes + cost model
- [find-insure-bucket-structuring-implications-DSC-brief-20260527.md](../../../../docs/briefs/find-insure-bucket-structuring-implications-DSC-brief-20260527.md) (AC2) — silver/gold prefix + DDB cost-state
- [find-insure-downstream-analytics-shape-options-DSC-brief-20260527.md](../../../../docs/briefs/find-insure-downstream-analytics-shape-options-DSC-brief-20260527.md) (AC3) — Phase 3 serving hybrid Option C
- [find-insure-phase2a-endpoint-decision-matrix.md](../../../../docs/reference/find-insure-phase2a-endpoint-decision-matrix.md) (AC4) — 8-step per-IMO execution chain

## Purpose

Pre-gate design brief per .024 Sequencing step 2 — compress post-gate turnaround by landing the subset-selection algorithm pseudocode + per-IMO Lusha-invocation pattern + cost-budget model NOW so LIVE-DISPATCH fires immediately when both gates clear (.011 RAVC2-Accept + Andrew Q1 sovereign ratify). Per memory `feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch`.

**Current gate state (2026-05-28T00:14Z):**
- **Gate 1 (.011 RAVC2-Accept):** OPEN. AC1 shipped `55449fc5a` (~C) + AC3 shipped `6457f6861` (~B parallel) + AC4 `79d202af0`; AC2 + AC5 + AC6 + AC7 (config/cost-budgets) status uncertain — bundle not yet at RAVC2-Request shape. My next-tick .011 work picks up AC2+AC5 (skip AC3 = DS~B's).
- **Gate 2 (Andrew Q1 sovereign ratify):** OPEN. 4-option menu shipped `5a00ced3b` 22:49Z; Andrew choice pending.

This brief is independent of either gate; reads only ratified PRD v0.7 + AC1-AC4 artifacts.

---

## §1. Subset-selection algorithm pseudocode

### §1.1 Inputs

| Input | Source | Format |
|---|---|---|
| Phase 1 ranked output | `s3://opal-data-imo/serving/scoring.json` (DS~E `.023` ship) OR fallback `corp/{slug}/gold/web-scrape/{date}/score.json` per-IMO | List of `{slug, rollup_score, term_matches[], wealth_management_axis_score?, ...}` |
| Andrew Q1 ratified rule | `5a00ced3b` 4-option menu → Andrew choice (one of A/B/C/D) | Enum + (optional) numeric parameter (threshold / N) |
| W1 threshold semantics | ws CTO REPAIR-AMENDMENT (b)(i) scribe (in flight) | Rank-based (NTILE) OR continuous-threshold |

### §1.2 Algorithm (Q1 dispatch on option choice)

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

Q1Option = Literal["A", "B", "C", "D"]

def select_phase_2a_subset(
    scoring_path: str,                          # s3://opal-data-imo/serving/scoring.json OR fallback
    q1_option: Q1Option,                        # "A" / "B" / "C" / "D" per Andrew ratify
    q1_param: float | int | None = None,        # B: adjacent-threshold (default 50); C: continuous-cutoff; D: top-N-absolute
    fallback_per_imo: bool = False,             # True if reading per-IMO gold/score.json instead of serving/scoring.json
) -> list[dict]:
    """
    Apply the Andrew-Q1-ratified subset-cut rule to Phase 1 ranked output.

    Returns: list of {slug, rollup_score, rationale: str, q1_tier: 1|2}
    """
    ranked = _load_ranked(scoring_path, fallback_per_imo=fallback_per_imo)
    ranked.sort(key=lambda x: x["rollup_score"], reverse=True)
    n = len(ranked)

    if q1_option == "A":
        # Top-quintile-only (top 20%; ceiling at top 25 IMOs for safety per AC7 hard-cap)
        cutoff_n = min(int(n * 0.20), 25)
        subset = [
            {**imo, "rationale": "top-quintile", "q1_tier": 1}
            for imo in ranked[:cutoff_n]
        ]

    elif q1_option == "B":
        # Top-quintile + adjacent-Series-license mention (RECOMMENDED)
        threshold = float(q1_param) if q1_param is not None else 50.0
        cutoff_n = min(int(n * 0.20), 25)
        tier1 = [
            {**imo, "rationale": "top-quintile", "q1_tier": 1}
            for imo in ranked[:cutoff_n]
        ]
        # Tier 2: above threshold AND Series-license term match in term_matches[]
        SERIES_TOKENS = {"Series 7", "Series 24", "Series 63", "Series 65", "Series 66", "Series 79"}
        seen_slugs = {imo["slug"] for imo in tier1}
        tier2 = [
            {**imo, "rationale": "adjacent-Series-license-mention", "q1_tier": 2}
            for imo in ranked[cutoff_n:]
            if imo["slug"] not in seen_slugs
            and imo["rollup_score"] >= threshold
            and any(tok in (imo.get("term_matches") or []) for tok in SERIES_TOKENS)
        ]
        subset = tier1 + tier2

    elif q1_option == "C":
        # Continuous-threshold (everyone above cutoff)
        threshold = float(q1_param) if q1_param is not None else 60.0
        subset = [
            {**imo, "rationale": f"above-threshold-{threshold}", "q1_tier": 1}
            for imo in ranked
            if imo["rollup_score"] >= threshold
        ]

    elif q1_option == "D":
        # Top-N-absolute (e.g., top 30 by rollup_score)
        n_abs = int(q1_param) if q1_param is not None else 30
        subset = [
            {**imo, "rationale": f"top-{n_abs}-absolute", "q1_tier": 1}
            for imo in ranked[:n_abs]
        ]

    else:
        raise ValueError(f"Unknown Q1 option: {q1_option}")

    # AC8 edge-case: empty / under-5 subset
    if len(subset) < 5:
        # Escalate to ws CTO + ws COO; do NOT dispatch
        raise EmptySubsetError(
            f"Phase 2A subset under 5 IMOs ({len(subset)}); Q1 option {q1_option} produces "
            f"insufficient coverage. Escalate to ws CTO for Q1 rule re-evaluation; "
            f"surface to ws COO with [PHASE2A-EMPTY-SUBSET] finding (likely Phase 1 calibration miss; "
            f"route to W1/W2 taxonomy refinement)."
        )

    return subset


def _load_ranked(scoring_path: str, fallback_per_imo: bool = False) -> list[dict]:
    """
    Read Phase 1 ranked output.
    Primary path: serving/scoring.json (DS~E .023 RAVC2-Accept'd; recommended).
    Fallback path: per-IMO corp/{slug}/gold/web-scrape/{date}/score.json + compose rollup-rank inline.
    """
    if not fallback_per_imo:
        # serving/scoring.json shape per DS~E .023 spec
        return _read_s3_json(scoring_path)
    # Fallback: scan corp/*/gold/web-scrape/latest/score.json + compose ranking
    return _compose_ranking_from_per_imo_gold()


class EmptySubsetError(Exception):
    """Phase 2A subset rule produced <5 IMOs; needs Q1 rule re-evaluation."""
```

### §1.3 Output artifact (.024 AC3)

Emit `s3://opal-data-imo/config/phase2a-subset-{run-date}.json` per AC3:

```json
{
  "run_date": "2026-05-28",
  "q1_option_ratified": "B",
  "q1_param": 50,
  "scoring_path": "s3://opal-data-imo/serving/scoring.json",
  "scoring_path_committed": "<git_hash_of_serving_scoring_at_read_time>",
  "w1_threshold_semantic": "rank-based",
  "subset": [
    {"slug": "wlth-rx", "rollup_score": 87, "rationale": "top-quintile", "q1_tier": 1},
    {"slug": "blue-bird-advisors", "rollup_score": 82, "rationale": "top-quintile", "q1_tier": 1},
    ...
    {"slug": "stevens-financial", "rollup_score": 52, "rationale": "adjacent-Series-license-mention", "q1_tier": 2}
  ],
  "subset_count": 25,
  "tier1_count": 20,
  "tier2_count": 5,
  "andrew_q1_ratify_text": "<verbatim Andrew Q1 ratify quote per AC2>"
}
```

**Lifecycle:** append-by-date per CVO §3.2; never overwrite. Re-runs on later dates produce new file.

---

## §2. Per-IMO Lusha-invocation pattern

**Canonical:** `find-insure-phase2a-endpoint-decision-matrix.md` §1 — 8-step per-IMO Lambda execution chain. Reproduced here in skeletal form for self-contained reference:

```python
from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import boto3
import requests

LUSHA_BASE = "https://api.lusha.com/v3"
LUSHA_API_KEY_SECRET = "find-insure/lusha-ai/api-key"
COST_STATE_TABLE = "find-insure-cost-state"
OPT_OUT_TABLE = "find_insure_opt_out"
BUCKET = "opal-data-imo"
PER_IMO_CEILING_CREDITS = 50   # per CVO §9 + AC4 §3.4
GLOBAL_DAILY_CEILING = 500     # per CVO §9
HARD_CAP_CALLS_PER_IMO = 20    # per PRD §3.8 + .024 AC7

# Filter spec per AC4 §4.2 (DS~E re-coord in flight for v0.2 ratify)
PROSPECTING_FILTER = {
    "contacts": {
        "seniority": ["C-Level", "VP", "Director"],
        "departments": ["Finance", "Sales", "Executive"],  # resolve to enum IDs via Filters discovery cached
        "existingDataPoints": ["email"],
    },
}


def lambda_handler(event: dict, context: Any) -> dict:
    """
    Per-IMO Phase 2A LushaAI enrichment Lambda.
    event: {slug: str, domain: str, rollup_score: int, run_date: str, run_id?: str}
    """
    slug = event["slug"]
    domain = event["domain"]
    run_id = event.get("run_id") or str(uuid.uuid4())
    run_date = event["run_date"]

    telemetry = _telemetry_init(slug, run_id, run_date)
    budget = LushaCallBudget(hard_cap=HARD_CAP_CALLS_PER_IMO, slug=slug)
    api_key = _get_secret(LUSHA_API_KEY_SECRET)

    try:
        # Step 0: pre-flight cost-state gate
        if _check_cost_gate_abort(slug, run_date):
            telemetry["aborted_at_step"] = 0
            telemetry["abort_reason"] = "cost_ceiling_hit"
            return _finalize(telemetry, budget)

        # Step 1: companies/search → lusha_company_id
        budget.consume()
        company_search = _lusha_call(
            method="POST",
            path="/v3/companies/search",
            body={"companies": [{"domain": domain}]},
            api_key=api_key,
            telemetry=telemetry,
        )
        if not company_search.get("data"):
            telemetry["aborted_at_step"] = 1
            telemetry["abort_reason"] = "company_not_found"
            return _finalize(telemetry, budget)
        lusha_company_id = company_search["data"][0]["id"]
        telemetry["lusha_company_id"] = lusha_company_id
        _land_bronze("companies_search", run_id, run_date, slug, company_search)

        # Step 2: contacts/prospecting → contactIds
        budget.consume()
        prospecting = _lusha_call(
            method="POST",
            path="/v3/contacts/prospecting",
            body={
                "filters": {
                    **PROSPECTING_FILTER,
                    "companies": {"companyIds": [lusha_company_id]},
                },
                "pages": {"page": 1, "size": 50},
            },
            api_key=api_key,
            telemetry=telemetry,
        )
        contacts_raw = (prospecting.get("data") or [])[:HARD_CAP_CALLS_PER_IMO]
        if not contacts_raw:
            telemetry["aborted_at_step"] = 2
            telemetry["abort_reason"] = "no_contacts_matched_filter"
            return _finalize(telemetry, budget)
        _land_bronze("contacts_prospecting", run_id, run_date, slug, prospecting)
        contact_ids = [c["id"] for c in contacts_raw]

        # Step 3: opt-out DDB pre-flight
        opted_out = _check_opt_out(contact_ids)
        keep_ids = [cid for cid in contact_ids if cid not in opted_out]
        telemetry["contacts_filtered_opt_out"] = len(opted_out)
        if not keep_ids:
            telemetry["aborted_at_step"] = 3
            telemetry["abort_reason"] = "all_contacts_opted_out"
            return _finalize(telemetry, budget)

        # Step 4: contacts/enrich (reveal: emails + phones)
        budget.consume()
        enriched = _lusha_call(
            method="POST",
            path="/v3/contacts/enrich",
            body={"contactIds": keep_ids, "reveal": "emails,phones"},
            api_key=api_key,
            telemetry=telemetry,
        )
        _land_bronze("contacts_enrich", run_id, run_date, slug, enriched)

        # Step 5: (CONDITIONAL — v0.1 default SKIP per AC1 §2.2 + AC4 §4.4)
        company_enriched = None
        if _config_company_enrich_enabled():
            budget.consume()
            company_enriched = _lusha_call(
                method="POST",
                path="/v3/companies/enrich",
                body={"companyIds": [lusha_company_id]},
                api_key=api_key,
                telemetry=telemetry,
            )
            _land_bronze("companies_enrich", run_id, run_date, slug, company_enriched)

        # Silver passthrough (per AC2 §1.X Rule 17 binding)
        _compose_silver_all_endpoints(slug, run_date, run_id, company_search, prospecting,
                                      enriched, opted_out_subset=opted_out,
                                      company_enriched=company_enriched)

        # Step 6: gold compose employees.json (per .024 AC6)
        gold_employees = _compose_gold_employees(
            slug=slug, run_date=run_date,
            company_search=company_search,
            prospecting_data=contacts_raw,
            enrich_data=enriched.get("data", []),
            opted_out=opted_out,
        )
        _land_gold("employees", run_date, slug, gold_employees)
        telemetry["gold_employees_row_count"] = len(gold_employees["employees"])

        # Step 7: (CONDITIONAL) gold compose companies.json
        if company_enriched is not None:
            gold_companies = _compose_gold_companies(slug, run_date, company_search, company_enriched)
            _land_gold("companies", run_date, slug, gold_companies)

        # Step 8: telemetry + cost-state finalize
        return _finalize(telemetry, budget)

    except PhaseAbortError as e:
        telemetry["aborted_at_step"] = e.step
        telemetry["abort_reason"] = e.error_class
        return _finalize(telemetry, budget)
    except Exception as e:
        telemetry["abort_reason"] = f"unexpected_error: {type(e).__name__}: {e}"
        return _finalize(telemetry, budget)
```

### §2.1 Helper-function contracts (skeleton)

- `_lusha_call` — wraps `requests.post/get`; captures rate-limit headers into telemetry; applies §3.3 backoff (sleep on x-minute-requests-left ≤ 5); handles HTTP error codes per AC4 §3.1 table; returns parsed JSON OR raises `PhaseAbortError(step=N, error_class="<>")`
- `_land_bronze` — writes raw response JSON to `corp/{slug}/bronze/linkedin/{endpoint}/{date}/{run_id}.json` (SSE-KMS per CVO §6.1)
- `_compose_silver_all_endpoints` — Rule 17 strict passthrough per AC2 §1.X schemas; writes parquet to `corp/{slug}/silver/linkedin/{endpoint}/{date}/{run_id}.parquet`
- `_compose_gold_employees` — joins silver/companies_search + silver/contacts_prospecting + silver/contacts_enrich on `lusha_contact_id` + `lusha_company_id` per AC2 §2.1 join graph; filters opted-out; derives per-employee fields (title_seniority_class, series_licenses[], tenure_years, employee_score, keyword_matches); aggregates (employee_count, top_employee_score, series_density)
- `_check_cost_gate_abort` — DDB GetItem per-IMO + global per AC4 Step 0
- `_check_opt_out` — DDB BatchGetItem on `find_insure_opt_out` per AC9; soft-fail on DDB error
- `_finalize` — UpdateItem cost-state (per-IMO + global ADD operations atomic); writes telemetry ndjson to `telemetry/find-insure-crawl-linkedin/{date}/{run_id}.ndjson`; returns Lambda response summary

### §2.2 Class scaffold

```python
class LushaCallBudget:
    def __init__(self, hard_cap: int, slug: str) -> None:
        self.hard_cap = hard_cap
        self.slug = slug
        self.calls = 0

    def consume(self) -> None:
        self.calls += 1
        if self.calls > self.hard_cap:
            raise PhaseAbortError(
                step=-1,
                error_class="hard_cap_exceeded",
                detail=f"slug={self.slug} calls={self.calls} cap={self.hard_cap}",
            )


class PhaseAbortError(Exception):
    def __init__(self, step: int, error_class: str, detail: str = "") -> None:
        self.step = step
        self.error_class = error_class
        self.detail = detail
        super().__init__(f"step={step} class={error_class} {detail}")
```

---

## §3. Cost-budget model

### §3.1 Per-Q1-option projected cost

Per AC4 §2.1 (reproduced for self-contained reference):

| Q1 option | Avg IMOs in subset | Avg credits per IMO | Total Lusha credits | $ at $0.05/credit |
|---|---|---|---|---|
| A (top-quintile-only) | 20 | ~35 | ~700 | ~$35 |
| B (top-quintile+adjacent-Series RECOMMENDED) | 25 | ~35 | ~875 | ~$44 |
| C (continuous-threshold) | varies (avg 25) | ~35 | ~875 | ~$44 |
| D (top-N-absolute=30) | 30 | ~35 | ~1050 | ~$53 |

**All within `.024` AC7 cost-gate ceiling** (recommended $30 + buffer per PRD §3.7; tighten on empirical-first-run per PRD §3.8 5% overshoot tolerance).

### §3.2 Credits-per-IMO breakdown

Per-IMO ~35-credit composition:
- 1 × `api_search` (companies/search) — 1 credit
- 10-15 × `api_search` (contacts/prospecting per-result; HARD-CAP 20) — typical 10 credits
- 10-15 × `revealEmail` + 10-15 × `revealPhone` (contacts/enrich) — typical 12 + 12 = 24 credits
- 0 × `reveal_company` (companies/enrich SKIPPED v0.1 default) — 0 credits
- 0 × `lookalike*` (NOT USED v0.1) — 0 credits
- 0 × `showSignals*` (NOT USED v0.1) — 0 credits

Total per IMO: ~35 credits (range 15-50 depending on prospecting yield).

### §3.3 Real-time enforcement (per AC2 §5.4 + AC4 §3.4)

```python
# Per Lambda invocation start
def _check_cost_gate_abort(slug: str, run_date: str) -> bool:
    """Returns True if cost ceiling already hit; abort this IMO."""
    ddb = boto3.client("dynamodb")

    per_imo = ddb.get_item(
        TableName=COST_STATE_TABLE,
        Key={"PK": {"S": f"imo#{slug}"}, "SK": {"S": f"lusha#{run_date}"}},
    ).get("Item", {})
    per_imo_burn = int(per_imo.get("credits_burned", {}).get("N", "0"))

    global_state = ddb.get_item(
        TableName=COST_STATE_TABLE,
        Key={"PK": {"S": "GLOBAL"}, "SK": {"S": f"lusha#{run_date}"}},
    ).get("Item", {})
    global_burn = int(global_state.get("total_credits_burned", {}).get("N", "0"))

    if per_imo_burn >= PER_IMO_CEILING_CREDITS:
        _emit_telemetry({"abort_class": "per_imo_ceiling", "slug": slug, "burn": per_imo_burn})
        return True
    if global_burn >= GLOBAL_DAILY_CEILING:
        _emit_telemetry({"abort_class": "global_ceiling", "burn": global_burn})
        _sns_publish_alert(f"find-insure global daily ceiling hit: {global_burn}/{GLOBAL_DAILY_CEILING}")
        return True
    return False
```

End-of-run atomic update (single DDB write per Lambda; avoids write amplification per AC2 §5.4):
```python
ddb.update_item(
    TableName=COST_STATE_TABLE,
    Key={"PK": {"S": f"imo#{slug}"}, "SK": {"S": f"lusha#{run_date}"}},
    UpdateExpression="ADD credits_burned :total, api_search_credits :search, reveal_email_credits :email, reveal_phone_credits :phone, call_count :calls SET last_run_ts_utc = :ts, last_run_id = :rid",
    ExpressionAttributeValues={...},
)
```

### §3.4 SNS alerting

Per CVO §8 staged monitoring + PRD §3.7 cost-gate substrate:
- `find-insure-budget-alert` topic — fires on global ceiling-hit + per-IMO ceiling-hit + 402 Payment Required from Lusha
- `find-insure-credentials-alert` topic — fires on 401/403 from Lusha (key/account state changed)
- `find-insure-lusha-credit-burn-alarm` (CloudWatch metric-filter on telemetry) — pre-fires at 80% of daily ceiling per CVO §8

---

## §4. Failure-mode handling (full reference: AC4 §3)

Skeleton table reproduced for self-contained reference:

| HTTP code | Action |
|---|---|
| 200 | Capture billing.creditsCharged to telemetry; advance |
| 400 | Log + SKIP result row; continue batch |
| 401 / 403 | HALT entire Phase 2A; SNS find-insure-credentials-alert |
| 402 | HALT entire Phase 2A; SNS find-insure-budget-alert |
| 429 | Capture x-minute-requests-left; sleep computed-backoff (1s→60s, 5 retries) |
| 451 | Skip entity (GDPR-blocked); persist to opt-out store |
| 499 | Retry once; else skip step |
| 5XX | Exponential back-off (1s→60s, 5 retries); skip on exhaust |

**EC2 escape hatch (per AC4 §3.5):** if same IMO triggers `hard_cap_exceeded` 3 consecutive runs → route to AE 0.7 for one-off EC2 enrichment. v0.1 likelihood LOW.

---

## §5. Pre-flight checklist (run when both gates clear)

When `.011 RAVC2-Accept` AND Andrew Q1 ratify both fire:

| Step | Action | Owner | Estimated wall |
|---|---|---|---|
| 1 | Read Andrew Q1 ratify text verbatim from MCP / commit / log | ~C | <5min |
| 2 | Confirm `serving/scoring.json` exists at expected hash (cross-ref DS~E `.023` close commit) | ~C | <5min |
| 3 | Run `select_phase_2a_subset()` against ratified Q1 option + Phase 1 ranked output | ~C | <5min |
| 4 | Validate subset count ≥ 5 (else escalate AC8) | ~C | <1min |
| 5 | Emit `config/phase2a-subset-{run-date}.json` to S3 + commit subset config to CLOUD | ~C | <10min |
| 6 | Confirm AE 0.7 deployed `find-insure-crawl-linkedin` Lambda + tag bump per `.011` RAVC2-Accept | ~C verify | <5min |
| 7 | Confirm `find-insure-cost-state` DDB table + `find_insure_opt_out` DDB table + KMS key + SNS topics provisioned per `.001` RAVC2-Accept | ~C verify | <5min |
| 8 | Confirm `comp-iam service find-insure-crawl-linkedin` no MISSING + `comp-pipescript deployed` MATCH per AC10 | ~C verify | <5min |
| 9 | Read `config/phase2a-subset-{run-date}.json` + fan-out Lambda invocations (one per IMO) via SQS OR direct invoke loop | ~C | 5min dispatch |
| 10 | Monitor per-IMO Lambda completions via SNS topic `find-insure-phase2a-progress` | ~C | concurrent with execution |
| 11 | Aggregate run summary post-completion (per AC4 §5.4 `serving/_meta/phase_2a_run_{date}.json`) | ~C | <10min |
| 12 | Spot-check per AC6: top-5 employee scores match expected title classes (visual inspect) | ~C | <15min |
| 13 | Confirm AC7 cost-gate compliance (post-run cost-state DDB read; estimated $ vs ceiling) | ~C | <5min |
| 14 | Commit subset config + run summary + close .024 status pending→complete | ~C | <5min |
| 15 | RAVC2-Request to ws COO with evidence per .024 RAVC2 spec | ~C | <5min |

**Total post-gate wall:** ~30-60min pre-execution + ~2-3h Lambda execution (concurrent across ~25 IMOs at reserved-concurrency=5 per AC4 §5.2) + ~30min post-execution = **~3-4h end-to-end**.

---

## §6. Open questions (route to ws COO if material)

- **Q-LD1 (operational):** Confirm AE 0.7 `find-insure-crawl-linkedin` Lambda name (vs `find-insure-phase2a-lusha-enrich` or other). Lambda name pins comp-pipescript MATCH check + comp-iam audit + telemetry path. **Default-recommendation:** match COO TO .011 spec exactly; flag at .011 RAVC2-Accept moment.
- **Q-LD2 (architectural):** DS~E `.023` `serving/scoring.json` schema — confirm `term_matches[]` field present (drives AC4 Q1 option B Series-license token check). **Default-recommendation:** if absent, fallback Q1 to option A (top-quintile-only); flag DS~E for v0.2 amend.
- **Q-LD3 (operational):** Reserved-concurrency = 5 per AC4 §5.2. Confirm via AE 0.7 at .011 deploy. **Default-recommendation:** 5 OK for v0.1 Q1 options A/B (~25 IMOs at ~10min each = ~50min wall); tune up to 10 for Q1 option D (top-30) if SLA-pressure.
- **Q-LD4 (architectural):** `config/phase2a-subset-{run-date}.json` schema — proposed shape per §1.3 above. Confirm with ws COO at pre-flight step 5.
- **Q-LD5 (operational):** Fan-out mechanism — SQS queue (concurrent + retry semantics) vs direct invoke loop (simpler, less retry-friendly). **Default-recommendation:** direct invoke loop for v0.1 (~25 IMOs is small batch); SQS upgrade-path for v0.2 if subset grows.

---

## §7. Sister-coord with AC4 §4.2 filter spec ownership clarification

Per DS~B ACK 0002Z + my MCP to DS~E 0011Z: the hardcoded `PROSPECTING_FILTER` at §2 (`seniority: [C-Level, VP, Director]` + `departments: [Finance, Sales, Executive]`) is **subject to DS~E ratification**. If DS~E flags divergence with `scoring-weights-v0.1.json title_seniority_class_weights` design intent, this design brief gets v0.2 amendment + AC4 §4.2 update.

Currently: filter spec is COO-author-best-estimate from .024 AC4 language; DS~E ACK pending at next /work cycle.

---

## §8. Forward-staging notes

Per `feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch`: this design brief compresses post-gate turnaround by surfacing the algorithm + Lambda chain + cost model NOW. When both gates clear (likely within 1-2 /drive cycles), execution can fire immediately at step 9 above without authoring overhead.

**My .011 remaining bundle (AC1+AC2+AC4+AC5 per DS~B parallel-AC3 ship `6457f6861`)** is the next-tick substantive work after this brief lands; .011 RAVC2-Accept is gate 1 of 2 — the work that progresses .024 toward LIVE-DISPATCH.

---

— 0.1.0_DS_MarketIntelligence~C 2026-05-28T00:14Z (FIND_INSURE.024 Sequencing step 2 pre-gate design brief; work-cycle:2 archetype DESIGN-SUBSTRATE)
