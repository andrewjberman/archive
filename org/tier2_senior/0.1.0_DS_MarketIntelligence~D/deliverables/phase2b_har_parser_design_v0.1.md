# FIND_INSURE.025 — Phase 2B HAR Parser Design (v0.1 pre-gate)

| | |
|---|---|
| **Author** | 0.1.0_DS_MarketIntelligence~D |
| **Date** | 2026-05-27 |
| **TO** | FIND_INSURE.025 §Sequencing — Pre-gate step 2 (~1h: design brief authoring) |
| **Status** | v0.1 pre-gate — Andrew HAR supply gate not yet fired; this brief locks per-board parser pattern + bronze schema + silver passthrough rules + gold scoring formula NOW so post-HAR ship cycle is mechanical (~3h wall per Andrew-HAR-supply-moment) |
| **Parent TO** | `org/tier2_senior/0.1.0_DS_MarketIntelligence~D/task_orders/FIND_INSURE.025.dsd-phase2b-stage-ba-har-parser.md` |
| **Sister artifacts (FIND_INSURE.028)** | `docs/reference/job-board-channel-architecture-matrix.md` (AC1) · `docs/briefs/find-insure-phase2b-multi-board-design-v0.1.md` (AC2) · `docs/reference/find-insure-phase2b-stage-routing-matrix.md` (AC3) · `docs/briefs/find-insure-phase2b-cross-board-analytics-v0.1.md` (AC4) |
| **Substrate** | `data/find/imo/scripts/_util/har_parser_base.py` (this TO sister AC5; canonical HAR ABC) · `data/find/imo/scripts/_util/job_board_parser_base.py` (DS~D `97c32ffa4`; canonical JobBoardParser ABC) |

---

## 0. Posture

This brief is the FIND_INSURE.025 §Sequencing pre-gate output: design-locked NOW so Andrew-HAR-supply-moment to ship is ~3h wall. Post-gate execution flow:

1. ~30min: HAR sanity-check + sample extraction (validates HAR format + URL_PATTERNS match)
2. ~2h: per-board HAR parser + silver Lambda + gold Lambda + ~5 unit tests
3. ~30min: empirical run against Andrew HAR + spot-check (extracted job count + sample fields)
4. ~15min: commit + RAVC2-Request

Per-board ship parallelizable: if Andrew supplies HAR for boards A + B + C simultaneously, ws COO can spawn additional tilde-lanes for parallel ship if capacity warrants; single DS~D lane is the recommended posture for cross-board consistency review at first-board ship.

---

## 1. Per-board parser pattern (locked v0.1)

**Two parser classes per board** — `HarParser` subclass + `JobBoardParser` subclass — per AC2 §1 two-tier abstraction. Same per-board data uniform downstream regardless of source mode (HAR-extracted vs live-fetch).

### 1.1 `HarParser` subclass — extracts postings from HAR file

**Path:** `data/find/imo/scripts/_util/har_parser_{board}.py`

**Template:**

```python
"""{Board} HAR parser -- extracts job postings from Andrew-supplied HAR.

Per FIND_INSURE.025 + .028 AC5 canonical pattern. Subclasses HarParser
(data/find/imo/scripts/_util/har_parser_base.py) which provides load_har +
iter_matching_entries + parse_har; this class implements extract_postings
for {board}'s specific response shape.
"""
from __future__ import annotations

import json
import re
from typing import Iterable

# Stable import path: when shipped, har_parser_base resolves via package
# relative import OR Lambda layer namespace. For local execution + tests,
# the script is co-located with har_parser_base.py in the _util/ tree.
from har_parser_base import ExtractedPosting, HarEntry, HarParser


class {Board}HarParser(HarParser):
    """{Board} HAR parser.

    Targets:
      - {Search-endpoint URL pattern + response class}
      - {Detail-endpoint URL pattern + response class}
      - {Optional: company-page or filter endpoints}

    Reference: docs/reference/job-board-channel-architecture-matrix.md §{section}
    """

    BOARD_SLUG = "{board-slug}"
    URL_PATTERNS = (
        re.compile(r"^https://{board}\\.com/api/{endpoint}"),
        # additional patterns per board
    )

    def extract_postings(self, entry: HarEntry) -> Iterable[ExtractedPosting]:
        # Per-board extraction:
        # 1. Distinguish response class by entry.url + entry.mime_type
        # 2. Parse JSON or HTML or JSON-LD per response class
        # 3. Yield ExtractedPosting per visible posting
        # 4. Tolerate malformed/partial payload (yield empty rather than raise)
        if entry.mime_type.startswith("application/json"):
            yield from self._parse_json_response(entry)
        elif "/jobs/view/" in entry.url or "/job-listing/" in entry.url:
            yield from self._parse_detail_html(entry)
        else:
            yield from self._parse_search_html(entry)

    def _parse_json_response(self, entry: HarEntry) -> Iterable[ExtractedPosting]:
        try:
            data = json.loads(entry.response_text)
        except (json.JSONDecodeError, ValueError):
            return
        # board-specific JSON shape extraction
        ...

    def _parse_detail_html(self, entry: HarEntry) -> Iterable[ExtractedPosting]:
        # JSON-LD <script type="application/ld+json"> extraction OR
        # board-specific HTML parsing
        ...

    def _parse_search_html(self, entry: HarEntry) -> Iterable[ExtractedPosting]:
        # search-page HTML fragment parsing
        ...
```

### 1.2 `JobBoardParser` subclass — payload-to-silver transform

**Path:** `data/find/imo/scripts/silver/job_posting/parsers/{board}.py`

**Pattern** (already-shipped substrate per `97c32ffa4`):

```python
from data.find.imo.scripts._util.job_board_parser_base import (
    JobBoardParser, ParsedPosting,
)


class {Board}Parser(JobBoardParser):
    BOARD_SLUG = "{board-slug}"

    def parse_payload(self, payload, source_url):
        # Identical extraction logic as {Board}HarParser.extract_postings,
        # but for live-fetch payload bytes (search-page HTML or JSON response).
        # OR: refactor to share extraction logic between the two tiers via a
        # shared private helper to avoid duplication.
        ...
```

**Shared-extraction-logic refactor pattern** (recommended once 2+ boards ship):

Extract the per-board response-shape extraction into a free function shared between HarParser + JobBoardParser:

```python
# data/find/imo/scripts/_util/_extract_{board}.py
"""Shared {board} response-shape extraction; consumed by both HarParser
+ JobBoardParser tiers."""

def extract_postings_from_search_response(payload, source_url):
    """Yield ExtractedPosting / ParsedPosting from a search-endpoint payload."""
    ...

def extract_postings_from_detail_response(payload, source_url):
    """Yield ExtractedPosting / ParsedPosting from a detail-page payload."""
    ...
```

Both `{Board}HarParser.extract_postings()` and `{Board}Parser.parse_payload()` then call into the shared helpers. v0.1 ships per-board parsers without the shared helper; v0.2 refactors at first-empirical-run if duplication grows painful.

---

## 2. Bronze schema (canonical; per AC2 §4)

**Path:** `s3://opal-data-imo/corp/{slug}/bronze/job-postings/{board}/{run-date}/{posting_id}.json`

**One-record-per-posting:**

```json
{
  "posting_id": "{board-slug}:{board-native-id}",
  "board": "{board-slug}",
  "imo_slug": "advisors-excel",
  "imo_canonical_name": "Advisors Excel",
  "fetched_at": "2026-05-27T18:30:00Z",
  "source_url": "https://...",
  "har_endpoint_class": "B-alpha-direct",
  "har_capture_id": "{board}-{capture-date}.har",
  "raw_payload": {
    "_format": "html|json|json-ld",
    "_excerpt": "...first ~50KB of response body...",
    "_full_path": "s3://.../bronze/job-postings/{board}/{run-date}/raw/{posting_id}.{ext}"
  },
  "extracted_fields": {
    "job_title": "...",
    "full_description": "...",
    "posted_date_relative_raw": "...",
    "location_raw": "...",
    "salary_min": null,
    "salary_max": null,
    "salary_currency": "USD"
  },
  "board_specific_metadata": {
    "_format": "per-board JSON blob; Rule 17 passthrough -- preserved at silver",
    "...": "per-board fields per AC2 §4 Per-board metadata extension table"
  }
}
```

---

## 3. Silver passthrough rules (Rule 17 binding)

Silver schema produced by `JobBoardParser.parse_to_silver()` per already-shipped `job_board_parser_base.py` (`97c32ffa4`); schema canonical at AC2 §5.

**Rule 17 strict binding:**

- `board_specific_metadata` field carries the bronze per-board extension AS-IS at silver
- NO silver-side projection / slimming / null-handling / business-logic-row-filtering
- Silver is permitted ONLY: dedup of exact-row duplicates + dtype standardization (e.g., `coerce_silver_ids()` Int64 enforcement) + string→numeric coercion on unambiguously-numeric columns + whitespace/encoding flattening
- All gold-tier field-pruning + null-handling + business-row-filtering lives at gold

**Per-board metadata extension fields (Rule 17 preserved at silver):**

| Board | board_specific_metadata fields |
|---|---|
| LinkedIn Jobs | linkedin_company_id, seniority_level, employment_type, industries[], applicant_count_visible |
| Indeed | jobkey, sponsored_flag, expired_flag, formatted_relative_time, source_employer_name_match |
| Glassdoor | employer.id, employer.rating, employer.review_count, salaryRange.{min,max}, currency |
| eFinancialCareers | specialism, specialism_subcategory, keyword_tags[], seniority_level |
| InsuranceJobs.com | **required_licenses[] (STRUCTURED)**, specialty, jobType |
| WealthManagementJobs.com | **AUM_band (UNIQUE STRUCTURED)**, required_credentials[], jobFunction |
| ZipRecruiter | category, salary_min_annual, salary_max_annual, salary_interval, posted_time_iso |
| Built In | tech_stack[], industry_tags[], salary_range, equity_range, remote_flag |
| Wellfound | company.{valuation, funding_stage, employee_count, industries[]}, equity_range, skills[], experience_level |

---

## 4. Gold scoring formula (canonical v0.1; per AC2 §7)

**Path:** `data/find/imo/scripts/gold/score_jobs_gold.py` (per .025 AC6)

**Per-posting rollup_score formula v0.1:**

```python
def compute_posting_score(silver_row, run_date):
    # Read inputs from already-derived silver fields
    investment_title_hits  = len(silver_row["investment_title_hits"])
    investment_desc_hits   = len(silver_row["investment_description_hits"])
    anti_signal_hits       = len(silver_row["anti_signal_hits"])
    series_required        = len(silver_row["series_licenses_required"])
    series_preferred       = len(silver_row["series_licenses_preferred"])
    credentials_required   = len(silver_row["credentials_required"])
    credentials_preferred  = len(silver_row["credentials_preferred"])
    role_class             = silver_row["role_class"]
    cross_board_visibility = silver_row.get("cross_board_visibility_score", 0.0)
    posted_date            = silver_row["posted_date"]

    # v0.1 weights -- empirical-first-run calibration; tunable post-IR-review
    weights = {
        "w_investment_title":     5.0,
        "w_investment_desc":      2.0,
        "w_series_required":      4.0,
        "w_series_preferred":     2.0,
        "w_credentials_required": 3.0,
        "w_credentials_preferred":1.5,
        "w_cross_board":          3.0,
        "w_recency":              2.0,
        "w_anti_signal":          3.0,
    }
    role_class_weights = {
        "investment-professional": 5.0,
        "corporate-finance":       3.0,   # CVO ADDITIVE-1 forward-signal
        "technology":              2.0,   # CVO ADDITIVE-1 forward-signal
        "compliance":              2.0,
        "operations":              1.0,
        "legal":                   1.0,
        "sales":                   -1.0,  # insurance-only producer = negative signal
        "other":                   0.0,
    }
    recency_damping = compute_recency_damping(posted_date, run_date)  # 1.0 if <=30d, decays to 0.3 at 360d

    score = (
        weights["w_investment_title"]      * investment_title_hits
      + weights["w_investment_desc"]       * investment_desc_hits
      + weights["w_series_required"]       * series_required
      + weights["w_series_preferred"]      * series_preferred * 0.5
      + weights["w_credentials_required"]  * credentials_required
      + weights["w_credentials_preferred"] * credentials_preferred * 0.5
      + role_class_weights.get(role_class, 0.0)
      + weights["w_cross_board"]           * cross_board_visibility
      + weights["w_recency"]               * recency_damping
      - weights["w_anti_signal"]           * anti_signal_hits
    )
    return max(0.0, score)  # floor at 0 to avoid negative-aggregate weirdness


def compute_recency_damping(posted_date, run_date):
    if posted_date is None:
        return 0.5  # missing-date default; halfway weighting
    days_old = (run_date - posted_date).days
    if days_old <= 30:
        return 1.0
    if days_old <= 90:
        return 0.8
    if days_old <= 180:
        return 0.6
    if days_old <= 360:
        return 0.3
    return 0.1
```

**Per-IMO aggregate** (per .025 AC7 — schema canonical at AC2 §7 + AC4 §6):

```json
{
  "imo_slug": "advisors-excel",
  "imo_canonical_name": "Advisors Excel",
  "run_date": "2026-05-28",
  "job_postings_count": 17,
  "job_postings_count_deduped": 12,
  "boards_observed_on": ["linkedin-jobs", "indeed", "efinancialcareers", "insurancejobs-com"],
  "total_score": 487.3,
  "role_class_distribution": {...},
  "series_licenses_required_aggregate": {...},
  "credentials_required_aggregate": {...},
  "investment_keyword_density": 0.42,
  "AUM_band_observed": "$500M-$1B AUM",
  "top_job_signals": [...],
  "aggregated_hiring_signal_class": "high-conviction-buildout",
  "hiring_velocity_30d": 4,
  "hiring_velocity_90d": 11,
  "hiring_velocity_180d": 14,
  "tech_hire_forward_signal_count": 1,
  "corp_finance_forward_signal_count": 2
}
```

---

## 5. Per-board test pattern (~5 unit tests per board per .025 AC sizing)

**Per-board minimum test coverage:**

1. `test_{board}_har_url_patterns_match` — synthetic HAR with matching + non-matching entries; verify only target endpoints surface
2. `test_{board}_har_extract_postings_canonical` — canonical fixture HAR; verify N postings extracted with expected `posting_id` + `job_title` + `full_description` for ≥1 sample
3. `test_{board}_silver_transform_canonical` — `JobBoardParser.parse_to_silver()` against canonical payload; verify silver row matches expected JSON including taxonomy-derived `role_class` + `series_licenses_required` + `investment_title_hits`
4. `test_{board}_malformed_payload_graceful_degradation` — malformed HAR + malformed payload return empty iterators / lists (no exceptions)
5. `test_{board}_board_specific_metadata_passthrough` — Rule 17 verification: board-specific extension fields preserved at silver intact

**Per-board fixtures path:** `data/find/imo/tests/fixtures/phase2b/{board}/` per AC2 §8

**Optional 6th test (cross-board dedup at first 2nd-board ship):** `test_cross_board_dedup_composite_key` — synthetic posting visible on 2 boards; verify gold-tier dedup collapses to single row with `cross_board_observation_count = 2` + `seen_on_boards = [board_1, board_2]`

---

## 6. Lambda dispatch pattern (per .025 AC8)

**v0.1 mode:** standalone Python local invocation (NOT Lambda EventBridge fan-out) per .025 AC8 — HAR is one-shot per Andrew-supplied capture session, not recurring:

```bash
python data/find/imo/scripts/_util/har_parser_{board}.py \
  --input data/find/imo/config/har/{board}-{capture-date}.har \
  --output-prefix corp/ \
  --imo-slugs-file data/find/imo/config/source-list-{date}.json
```

The standalone script:
1. Loads HAR + extracts ExtractedPosting list
2. For each posting, determines which IMO it belongs to (matches `hiring_company.name` / `companyName` field against `imo_canonical_name` set from source-list)
3. Writes per-posting bronze JSON to `corp/{slug}/bronze/job-postings/{board}/{run-date}/{posting_id}.json`
4. Emits `parse_errors_{board}.json` log on malformed payload
5. Returns per-IMO posting count + total extraction summary

**Future v0.2 mode** (deferred per .025 AC8 OUT OF v0.1 SCOPE): EventBridge-fired Lambda for recurring per-IMO live-fetch using HAR-discovered internal endpoint URLs (no HAR re-supply needed for the recurring fetch; HAR-supply only at endpoint-discovery + endpoint-drift-recovery moments).

---

## 7. HAR validation + defensive parsing (per .025 AC9)

**Tolerant load behavior** (already-shipped in `har_parser_base.py` `load_har()`):

- Missing file → returns `{"log": {"entries": []}, "_parse_error": "HAR not found: ..."}`
- Malformed JSON → returns `{"log": {"entries": []}, "_parse_error": "JSONDecodeError: ..."}`
- Per-entry malformation (missing request/response/url) → skip silently in `iter_matching_entries`
- Response-body parse failure → per-board `extract_postings` returns empty iterator (no raise)

**Telemetry on tolerant degradation:**

```python
def emit_parse_errors_log(har, output_prefix):
    if "_parse_error" in har:
        log = {
            "har_parse_error": har["_parse_error"],
            "har_path": "...",
            "entries_yielded": 0,
            "fired_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(f"{output_prefix}/parse_errors_{BOARD}.json", "w") as f:
            json.dump(log, f, indent=2)
```

---

## 8. Cost-gate compliance (per .025 AC10)

**$0 LushaAI cost** — HAR-based parser does not call any external API; all data comes from Andrew-supplied HAR. Bronze writes are S3 PutObject only (negligible cost at 99-IMO × 10-50 postings per IMO scale).

**Cost-budget integration** (per DS~E `cost-budgets-v0.1.json`): standalone Python script can OPTIONALLY read `cost-budgets-v0.1.json` for per-IMO posting cap enforcement at extract time (default cap 100 postings/IMO/board per DS~E `6ee4c7eb2`). v0.1 skip if not needed; defer to v0.2 if first-empirical reveals over-cap extraction risk.

---

## 9. Compiler-tools mandate (per .025 AC11)

**Before-commit gates:**

- `.tools/ds-commit-gate.sh data/find/imo/scripts/_util/har_parser_{board}.py` — PASS (already verified for `har_parser_base.py` this turn)
- `.tools/ds-commit-gate.sh data/find/imo/scripts/silver/job_posting/parsers/{board}.py` — PASS
- `.tools/ds-commit-gate.sh data/find/imo/scripts/silver/parse_jobs_silver.py` — PASS (Lambda entrypoint)
- `.tools/ds-commit-gate.sh data/find/imo/scripts/gold/score_jobs_gold.py` — PASS

**After comp-graph registration (AE 0.7 task):**

- `comp-pipescript io data/find/imo/scripts/silver/parse_jobs_silver.py` — IO clean
- `comp-iam service find-insure-crawl-job-posting-{board}` — confirms s3:PutObject scope (per CLAUDE.md Rule 13 + 14)
- `comp-pipescript deployed data/find/imo/scripts/silver/parse_jobs_silver.py` — MATCH at deploy

---

## 10. RAVC2-Request deliverable (per .025 §RAVC2 deliverable section)

**Format:** `[RAVC2-Request] FIND_INSURE.025 — Phase 2B Stage Bα HAR parser ({board})` to ws COO. CC ws CTO + ws CVO.

**Body sections:**

- Code commit hash (per-board parser + silver + gold + tests)
- Per-board HAR parse evidence: extracted posting count + sample job_keywords (3-5 sample extracted titles + description excerpts) + corp_finance_or_tech_hire classification spot-check
- Cost-gate compliance: $0 expected (confirmed via SSM Lambda execution cost emission OR local-run resource usage)
- `comp-pipescript io` + `comp-iam service` outputs
- Self-attestation: all 11 ACs (AC1-AC11) PASS

---

## 11. Cross-references

- **Parent TO:** `org/tier2_senior/0.1.0_DS_MarketIntelligence~D/task_orders/FIND_INSURE.025.dsd-phase2b-stage-ba-har-parser.md`
- **Sister TO (this brief's TO):** `org/tier2_senior/0.1.0_DS_MarketIntelligence~D/task_orders/FIND_INSURE.028.dsd-phase2b-multi-board-architecture-survey.md`
- **AC1 board architecture matrix (.028 sister):** `docs/reference/job-board-channel-architecture-matrix.md`
- **AC2 multi-board parser system design (.028 sister):** `docs/briefs/find-insure-phase2b-multi-board-design-v0.1.md`
- **AC3 Stage Bα/Bβ routing matrix (.028 sister):** `docs/reference/find-insure-phase2b-stage-routing-matrix.md`
- **AC4 cross-board analytics framework (.028 sister):** `docs/briefs/find-insure-phase2b-cross-board-analytics-v0.1.md`
- **AC5 HarParser ABC (.028 sister AC5):** `data/find/imo/scripts/_util/har_parser_base.py` (this TO sister ship)
- **JobBoardParser ABC (already shipped):** `data/find/imo/scripts/_util/job_board_parser_base.py` (DS~D `97c32ffa4`)
- **Parent PRD:** `docs/architecture/FIND_INSURE.md` v0.7 §4 Phase 2 Part B + §3.7-§3.8 cost-budget infra

---

## 12. Authoring lineage

- **v0.1** 2026-05-27 — initial pre-gate design brief per FIND_INSURE.025 §Sequencing pre-gate authorization. Locks per-board parser pattern + bronze schema + silver passthrough + gold scoring formula + test pattern + dispatch mode + defensive parsing + cost-gate + compiler-tools mandate + RAVC2 format. Post-gate ship cycle compresses to ~3h wall per Andrew-HAR-supply-moment per board.
