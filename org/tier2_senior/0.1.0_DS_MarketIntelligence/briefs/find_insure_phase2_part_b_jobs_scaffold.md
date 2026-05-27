# FIND_INSURE Phase 2 Part B — Job-postings channel scaffold

**Author:** 0.1.0_DS_MarketIntelligence~D
**Date:** 2026-05-27
**Trigger:** MSTR SPAWN-WITH-DIRECTION 2026-05-27T~16:49Z + ws COO `/allocation` #3 `org/tier1_exec/2.0.0_SA_COO/briefs/allocation_20260527T1647Z_find_insure_peak_priority.md`
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.2 / §3.6 / §4 Phase 2 Part B / §7 AC3b / §9 Q6
**Status:** **SCAFFOLD-COMPLETE / EXECUTE-PENDING.** Standing for Andrew HARs (PRD Q6) — until HARs land, Lambda implementations remain held; this brief is the design substrate that consumes the HAR endpoint manifest the moment it lands.
**Sister channel:** Phase 2 Part A (LinkedIn / LushaAI) — `0.1.0_DS_MarketIntelligence~C` parallel-prep brief.
**Pattern precedent:** SXPL_RESTIN HAR-first methodology — `docs/briefs/smartx-rest-integration-design-20260515.md` analogue.

---

## 1. Scope

Phase 2 Part B is the **job-posting channel** of FIND_INSURE — a per-IMO scrape of public job-board listings, scored on signals that an IMO is hiring into asset-management / investment-professional / corporate-finance / technology roles. The channel runs **in parallel** with Part A (LinkedIn current-state leadership); both feed Phase 3 consolidated scoring.

**What this brief produces:**

1. Stage Bα HAR-attack methodology — what Andrew captures, where it lands, how DS audits it.
2. Per-board target inventory + Bα-vs-Bβ disposition criteria.
3. Investment-keyword + Series-license + role-class taxonomies (v0.1 seed lists).
4. Union-schema across boards (silver tier).
5. `parse_job_posting_silver` Lambda design.
6. `score_job_posting_gold` Lambda design.
7. Open questions for Andrew at HAR-capture time.
8. Hand-off contract to AE 0.7 for Lambda + Bright Data wiring.

**What this brief does NOT produce (gated):**

- The per-board endpoint manifest itself (`docs/briefs/find-insure-job-board-endpoint-manifest.md`) — that lands AT Bα HAR-audit time, not now.
- Lambda code — pre-execution-trigger.
- Bright Data Bβ fallback configs — per-board decision deferred to Bα results.

---

## 2. Stage Bα HAR-attack methodology

Per PRD §4 Phase 2 Part B Stage Bα: Andrew supplies HAR captures from live browser sessions on each target job-board. DS audits the HAR for the JSON / GraphQL / REST endpoint each board uses behind its UI. The HAR-first-REST-second pattern is the same one that won SXPL_RESTIN — a HAR-confirmed REST endpoint replaces a fragile headless-browser scrape with a stateless HTTP call.

### 2.1 What Andrew captures (per board)

Per-board HAR drop = one `.har` file per board, covering a complete capture session:

1. **Landing page** — load `https://www.{board}.com/`. Establishes the cookie / session-token surface.
2. **Company-page navigation** — search for ONE seed IMO (e.g., "Advisors Excel" or any safemoneybroadcasting list company) and land on the company's "Jobs at X" page. This is the per-IMO entry point we'll programmatize.
3. **Job-listing iteration** — page through 2-3 pages of job listings for the seed company (Page 1 / Page 2 / Page 3). Captures pagination signature.
4. **Single job-detail page** — click into ONE specific listing. Captures the per-posting detail-fetch endpoint (URL + body + headers).
5. **Filter application** — apply ONE filter (e.g., "role = financial analyst") and re-page. Captures filter query-param signature.

### 2.2 HAR drop staging convention

Andrew drops HARs at: `data/find/imo/_har_capture/{board-slug}/{YYYY-MM-DD}/session.har` (or `s3://opal-data-imo/_har_drop/{board-slug}/{YYYY-MM-DD}/` if Andrew prefers S3-side delivery — single decision, both work).

Per-board sub-dirs prevent same-day cross-board commingling. Date-partitioned because HAR signatures rot (cookies expire, bot-defense headers mutate); a re-capture in 60 days is normal cadence.

**Privacy hygiene:** HARs carry session cookies + Authorization headers. The drop directory MUST be gitignored AND S3-side encrypted-at-rest (already SSE-S3 default per PRD §3.1). DS never commits the raw `.har` to git — only the **derived endpoint manifest** (which strips the cookie / token values to placeholder).

### 2.3 DS HAR-audit output (per board)

For each board's HAR, DS produces a row in `docs/briefs/find-insure-job-board-endpoint-manifest.md`:

```yaml
board: linkedin-jobs
Bα-feasibility-verdict: GO | GO-WITH-COOKIE | NO-GO  # NO-GO routes to Bβ Bright Data
endpoints:
  company-jobs-search:
    method: GET | POST
    url: https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
    pagination: query-param "start" + page-size 25
    auth: anonymous | session-cookie | bearer
  job-detail:
    method: GET
    url-pattern: https://www.linkedin.com/jobs/view/{job_id}
    extract: HTML parse vs embedded-JSON-blob (per-board choice)
auth-mechanism: anonymous | cookie:{cookie_names_required} | bearer:{header_name}
request-shape: ...
response-shape: html-render | json | graphql
rate-limit-signals: 429 after ~N reqs/min, Retry-After header, etc.
freshness-cadence: real-time | hourly | daily index
bot-defense: none | cloudflare | datadome | perimeterx | captcha-on-N-reqs
Bβ-fallback-config-if-needed: bright-data-collector-id-XYZ + scrape-config-snippet
cost-comparison: Bα ~$0/IMO via direct REST | Bβ ~$0.0X/IMO via Bright Data
```

**Verdict criteria (per board):**

- **GO (Bα-direct):** endpoint is reachable anonymous OR with a renewable session cookie; response is structured (JSON / GraphQL / parseable HTML); rate-limit ≥ 50 req/min sustainable; no aggressive bot-defense that demands per-request rotation infra.
- **GO-WITH-COOKIE:** as above but requires a Lusha-style cookie refresh layer (DS implements; same pattern as SmartX session refresh).
- **NO-GO (route to Bβ):** auth is OAuth-tied to a user account we don't have, OR bot-defense is captcha-on-page-load, OR rate-limit < 10 req/min. Route through Bright Data Bβ.

### 2.4 Per-board sign-off gate

Per PRD: "Andrew + AE 0.7 + DS sign-off on the per-board approach before Bβ engagement (Bright Data calls cost money; we route through it only where Bα can't deliver)." DS issues the endpoint manifest as a brief amendment; AE 0.7 ratifies Bβ-class boards before secrets-namespace provision; ws COO RAVC2-closes the Bα/Bβ matrix per board.

---

## 3. Per-board target inventory + initial Bα-vs-Bβ priors

Boards in priority order (capture-likelihood × IMO-coverage):

| # | Board | Why | Initial Bα prior |
|---|---|---|---|
| 1 | **LinkedIn Jobs** | Highest signal for investment-professional + Series-license-required postings; IMOs over-index here for credentialed roles | GO-WITH-COOKIE expected (LinkedIn requires `li_at` cookie for paginated company-jobs listings); reverse-engineerable per `jobs-guest/jobs/api/seeMoreJobPostings` known pattern |
| 2 | **Indeed** | Broadest US-job-board coverage; aggregates many ATS feeds; high probability every IMO has at least some Indeed presence | GO expected; Indeed has a documented public search endpoint (`/jobs`-route HTML + structured `script type="application/ld+json"` `JobPosting` block); HAR will confirm whether the SPA hydration endpoint is anonymous |
| 3 | **Glassdoor** | Company-jobs view + salary data; some IMOs only post here | GO-WITH-COOKIE expected; Glassdoor is aggressive on bot-defense (DataDome); HAR will surface the bot-class |
| 4 | **ZipRecruiter** | Smaller-firm coverage where Indeed misses | GO expected; lighter bot-defense than Glassdoor historically |
| 5 | **Wellfound (ex AngelList)** | Captures the asset-management-tech-startup wing of the universe (RIA software, model-portfolio platforms) — IMOs hiring tech leads often cross-post here | GO expected; Wellfound has lighter defense and structured listing pages |
| 6 | **Built In** | Tech-role-heavy; captures CTO / Head of Eng hires that signal IMO platform-buildout activity | GO expected; minimal bot-defense |
| 7 | **Career-builder / SimplyHired / Lensa** (long-tail) | Coverage marginal; capture only if priority-1-6 leave coverage gaps | DEFERRED until v0.2; not in v0.1 HAR-capture set |

**HAR-capture priority for Andrew (v0.1):** boards 1-6. Board 7 deferred.

**Direct-ATS bypass note (out of v0.1):** large IMOs sometimes operate their own ATS (Greenhouse, Lever, Workday). v0.2 candidate: when the company-website crawl (Phase 1 web-scrape) discovers a `careers.{imo-domain}` page powered by Greenhouse/Lever, prefer the direct ATS API (Greenhouse + Lever have documented public job-board JSON endpoints with no bot-defense). Out of v0.1 scope — captured for follow-on.

---

## 4. Taxonomies (v0.1 seed lists)

### 4.1 Investment-keyword taxonomy

Per PRD §4 Phase 2 Part B deliverable 3. v0.1 seed list — refined at HAR-time once we see real listings:

**Title-class hits** (high-signal — these in a job TITLE = strong signal):

```
portfolio manager
investment advisor | investment adviser
financial advisor | financial planner
wealth advisor | wealth manager
asset management associate | asset management director
investment analyst | investment associate
research analyst | equity research analyst | fixed-income analyst
chief investment officer | CIO
director of investments
head of asset management | head of wealth | head of advisory
RIA principal | RIA chief compliance officer
TAMP advisor | TAMP director
model portfolio strategist
relationship manager (when paired with "advisor" / "wealth" / "investment")
```

**Description-class hits** (medium-signal — these in BODY but not title):

```
asset management | asset under management | AUM
investment advisory | investment advice | investment management
wealth management | wealth planning
portfolio construction | portfolio modeling
model portfolio | SMA | separately managed account
RIA | Registered Investment Advisor
fiduciary | suitability | best interest
Form ADV | Reg BI | Regulation Best Interest
TAMP | turnkey asset management platform
alternatives | alternative investments
fixed income | equity | structured products
financial planning | retirement planning | tax-advantaged investing
```

**Anti-signal terms** (REDUCE score when present without investment-class):

```
insurance only | insurance sales | annuity sales | life insurance agent
producer | downline | recruit producers
captive agent | independent agent (when standalone, not paired with advisory)
```

The anti-signal exists because most IMOs ARE insurance-distribution houses by default — we want to surface the ones differentiating into investment / advisory work, not flag every insurance-sales-rep listing.

### 4.2 Series-license taxonomy

Per Andrew SPAWN-WITH-DIRECTION: **Series 63/65/66/7** are the priority detection set, expanded per PRD §4 Phase 2 Part B deliverable 3 to the full FINRA/NASAA license codes.

| License | Class | What it signals |
|---|---|---|
| Series 7 | FINRA general securities | Broker-dealer rep — sells investment products |
| Series 63 | NASAA Uniform Securities Agent state law | Required to sell securities across states (companion to 7) |
| Series 65 | NASAA Investment Adviser Representative | RIA-side license — fee-based advisory (the asset-management transition tell) |
| Series 66 | NASAA combined 63+65 | Combined broker + adviser (very common at IMO advisory-transition firms) |
| Series 24 | FINRA general principal | Supervises Series 7 reps (compliance leadership) |
| Series 6 | FINRA limited products | Mutual funds + variable annuities only (lower-signal) |
| Series 79 | FINRA investment-banking rep | M&A activity signal (corporate-finance class) |
| Series 82 | FINRA private-securities-offerings rep | Private-placement signal |
| Series 51, 52, 53 | MSRB municipal-securities | Muni-bond business signal |
| Series 22, 26 | FINRA direct-participation-programs, investment-company principal | Niche-product principal signals |
| CFA, CFP, ChFC | Credentialing | Investment-credentialed talent — boost score even when not Series-numbered |

**Detection regex (v0.1 seed):**

```python
# Case-insensitive, word-bounded
SERIES_LICENSE_RE = re.compile(
    r"\b(?:series\s+(?P<num>7|63|65|66|24|6|79|82|51|52|53|22|26))\b"
    r"|\b(?P<cred>CFA|CFP|ChFC|CPWA|CIMA|AIF)\b",
    re.IGNORECASE,
)
```

**Required-vs-preferred distinction:** the score-side cares about REQUIRED Series-licensure (binding signal) vs PREFERRED (soft signal). Detection looks for proximity markers — `required`, `must have`, `mandatory` boost vs `preferred`, `nice to have`, `plus`. Per-posting output carries `series_licenses_required: list[str]` + `series_licenses_preferred: list[str]` separately; the score aggregates both with different weights.

### 4.3 Role-class enum (per PRD)

```python
ROLE_CLASS_ENUM = Literal[
    "investment-professional",   # advisor / portfolio mgr / analyst / strategist
    "corporate-finance",         # CFO / FP&A / controller / treasurer / M&A
    "technology",                # CTO / engineering / data / platform / IT
    "operations",                # back-office / trade-ops / fund-admin / compliance-ops
    "compliance",                # CCO / compliance officer / regulatory affairs
    "sales",                     # insurance-sales / annuity-sales / producer-recruit
    "legal",                     # GC / corp-counsel / regulatory-counsel
    "other",                     # everything that doesn't fit
]
```

**Forward-signal-class roles** (per PRD §4 Phase 2 Part B deliverable 3 + Andrew rationale "begets m&a/growth activity"): `corporate-finance` + `technology` postings are NOT direct investment-management signals but they're forward signals — an IMO building a CFO function or a CTO function is investing in the infrastructure that begets the transition. Score weights these MEDIUM (vs HIGH for `investment-professional`, LOW for `sales`).

### 4.4 Title-keyword classification rules (silver-side `role_class` assignment)

Silver tier classifies role_class **deterministically from title + description keywords** — no LLM, no judgment. Disambiguation rules:

1. Title contains any from §4.1 title-class hits → `investment-professional`.
2. Title contains `CFO | Chief Financial Officer | VP Finance | Controller | Treasurer | FP&A | Director of Finance | M&A | Mergers and Acquisitions` → `corporate-finance`.
3. Title contains `CTO | Chief Technology | VP Engineering | Director of Engineering | Head of Engineering | Software Engineer | Data Engineer | Platform | DevOps | Site Reliability` → `technology`.
4. Title contains `CCO | Chief Compliance | Compliance Officer | Regulatory | AML | KYC` → `compliance`.
5. Title contains `General Counsel | Corporate Counsel | Attorney | Paralegal` → `legal`.
6. Title contains `Insurance | Annuity | Life Sales | Producer | Recruiter` (without investment-class title-hit) → `sales`.
7. Title contains `Operations | Back Office | Trade Support | Settlement | Fund Admin` → `operations`.
8. Else → `other`.

Order matters — first match wins. The order is deliberate: investment-professional tested first so a "Director of Investment Operations" lands as investment-professional, not operations.

---

## 5. Union-schema across boards (silver tier)

Per PRD: "structures each posting record — `{job_title, full_description, posted_date, location, source_board, source_url, role_class, requirements_text, salary_range_if_visible}`." Expanded:

### 5.1 Silver schema (`silver/job-posting-scrape/{slug}/{run-date}/postings.parquet`)

```python
SILVER_SCHEMA = {
    # Identity
    "posting_id": str,                    # board-namespaced ID, e.g. "linkedin:3987654321"
    "imo_slug": str,                      # FROM Phase 0 source-list slug — the join key
    "imo_canonical_name": str,            # company name as Phase 0 extracted it
    "source_board": str,                  # enum: linkedin-jobs | indeed | glassdoor | ziprecruiter | wellfound | builtin
    "source_url": str,                    # canonical board URL for this posting

    # Posting metadata
    "job_title": str,                     # raw title as posted
    "job_title_normalized": str,          # lowercased, whitespace-collapsed (downstream consistency)
    "full_description": str,              # plain-text description (HTML stripped at silver)
    "description_word_count": int,        # for low-content posting filtering downstream

    # Posted-date + freshness
    "posted_date": "date",                # board's posted date (often relative "3 days ago" — resolved at silver)
    "posted_date_relative_raw": str,      # the raw board string ("3d ago") for audit
    "fetched_at": "timestamp",            # when our crawl saw it (UTC)

    # Location
    "location_raw": str,                  # as posted
    "location_city": "str?",              # parsed
    "location_state": "str?",             # parsed (2-letter US state where resolvable)
    "location_remote_flag": bool,         # true if posting indicates remote / hybrid

    # Classification (silver-deterministic, NOT business-logic; rule-based per §4.4)
    "role_class": str,                    # enum per §4.3 — silver-side rule-based (allowed; not judgment)

    # Detection signals (raw lists; score interprets at gold)
    "series_licenses_required": "list[str]",     # ["65", "66"] etc
    "series_licenses_preferred": "list[str]",
    "credentials_required": "list[str]",         # ["CFA", "CFP"]
    "credentials_preferred": "list[str]",
    "investment_title_hits": "list[str]",        # title-class terms matched
    "investment_description_hits": "list[str]",  # description-class terms matched
    "anti_signal_hits": "list[str]",             # anti-signal terms matched

    # Salary (where visible — most boards do NOT publish; nullable)
    "salary_min": "float?",
    "salary_max": "float?",
    "salary_currency": "str?",            # "USD" default
    "salary_period": "str?",              # enum: year | hour | month | week

    # Lineage
    "har_endpoint_class": str,            # Bα-direct | Bβ-brightdata — tracks which lane the row came from
    "bronze_path": str,                   # back-reference for re-parse
}
```

### 5.2 Silver-tier discipline (CLAUDE.md Rule 17 compliance)

This silver schema **respects Rule 17** explicitly:

- ✅ Deduplication: silver dedups on `(source_board, posting_id)` composite key — exact-row duplicates from re-crawls collapse.
- ✅ Type standardization: relative-date strings (`"3 days ago"`) parsed to absolute `posted_date`; raw retained as `posted_date_relative_raw` for audit.
- ✅ Whitespace/encoding normalization: `job_title_normalized` lowercased + collapsed; `full_description` HTML-stripped.
- ✅ Rule-based classification (`role_class` via §4.4 deterministic regex) — NOT judgment; deterministic enum population per CLAUDE.md Rule 17 ("standardize dtypes" + "flatten obvious encoding artifacts").
- ❌ NO field-slimming: bronze HTML retains EVERY field the board returns; silver writes ALL of them.
- ❌ NO `fillna(0)` or `dropna()` — salary nulls stay null, location nulls stay null. Business decisions about "what null means here" happen at gold.
- ❌ NO row filtering by business semantic — silver KEEPS every posting bronze returned (including expired / dead / clearly-off-topic). Gold filters per the score's own logic.

The detection-signal lists (`series_licenses_required`, `investment_title_hits`, etc) are extracted at silver because they're DETERMINISTIC regex output, not business-logic interpretations. Gold WEIGHTS them — that's where judgment lives.

### 5.3 `coerce_silver_ids()` enforcement (CLAUDE.md Rule 14)

The silver Lambda MUST import + call `coerce_silver_ids()` per ds-precommit-check.py enforcement. `posting_id` is an Int64-eligible field (most boards use numeric IDs); composite-key columns enter the coercer.

---

## 6. `parse_job_posting_silver` Lambda design

Per PRD §3.6 (the `parse_job_posting_silver` row). One Lambda, fan-out per IMO + per board.

### 6.1 Invocation contract

```python
# Event shape (one Lambda invocation = one (IMO, board, run-date) tuple)
{
    "imo_slug": "advisors-excel",
    "source_board": "linkedin-jobs",
    "run_date": "2026-06-15",  # YYYY-MM-DD UTC
    "bronze_prefix": "s3://opal-data-imo/corp/advisors-excel/bronze/job-posting-scrape/2026-06-15/linkedin-jobs/",
}
```

### 6.2 Logic

```
1. List all bronze objects under bronze_prefix (HTML files for HTML boards; JSON files for JSON boards)
2. For each object:
   a. Read + decode
   b. Parse to a normalized intermediate (HTMLBoardParser vs JSONBoardParser strategy class)
   c. Build the SILVER_SCHEMA row (§5.1)
   d. Apply role_class classification rules (§4.4)
   e. Extract detection-signal lists via regex (§4.1 + §4.2)
3. Coerce IDs (coerce_silver_ids)
4. Dedup on (source_board, posting_id)
5. Write to silver/job-posting-scrape/{imo_slug}/{run-date}/postings.parquet
6. Emit telemetry to telemetry/parse_job_posting_silver/{run-date}/{run-id}.ndjson
```

### 6.3 Per-board parser strategy

```python
# data/find/imo/scripts/silver/job_posting/parsers/
BOARD_PARSERS: dict[str, type[BoardParser]] = {
    "linkedin-jobs": LinkedInJobsParser,
    "indeed": IndeedParser,
    "glassdoor": GlassdoorParser,
    "ziprecruiter": ZipRecruiterParser,
    "wellfound": WellfoundParser,
    "builtin": BuiltInParser,
}
```

Each parser is a small class with one method `parse(bronze_payload: bytes, source_url: str) -> dict[str, Any]`. The strategy lives per-board because the HTML/JSON shape differs; the **post-parse silver-row construction is shared** (regex + role-class + ID-coerce + dedup all live in a common module).

### 6.4 Failure modes the silver Lambda MUST handle

- Empty bronze prefix (no postings — return empty silver, NOT an error).
- One malformed payload (skip + log + continue, don't fail the whole IMO).
- Posted-date unparseable (write `posted_date=null` + retain raw string).
- Board-side schema drift (e.g., LinkedIn changes a field name) — fail-loudly + emit a sentinel to telemetry so we re-cut the parser.

### 6.5 Path

`data/find/imo/scripts/silver/job_posting/parse_job_posting_silver.py` (per PRD §3.2 medallion + channel layout).

Mandatory first line per CLAUDE.md Rule 15: `from __future__ import annotations`.

---

## 7. `score_job_posting_gold` Lambda design

Per PRD §3.6 + §4 Phase 2 Part B deliverable 3. Consumes silver, produces per-IMO hiring-pattern analytics.

### 7.1 Invocation contract

```python
# Event shape — one Lambda invocation = one (IMO, run-date) tuple (cross-board within IMO)
{
    "imo_slug": "advisors-excel",
    "run_date": "2026-06-15",
    "silver_prefix": "s3://opal-data-imo/corp/advisors-excel/silver/job-posting-scrape/2026-06-15/",
}
```

### 7.2 Logic + per-IMO gold output

```
1. Read silver across ALL boards for the IMO+date
2. Per posting:
   a. Compute posting_score (axes per §7.3)
3. Per IMO+date aggregate:
   a. Role-class distribution: {role_class: count, %}
   b. Series-license-required-or-preferred posting count (any of priority-set 63/65/66/7 + others)
   c. Investment-keyword hit count (title-class + description-class)
   d. Hiring velocity: postings in trailing 30/90/180 days
   e. Anti-signal-share: % of postings flagged anti-signal-only
   f. Highest-signal-posting list: top-N postings by posting_score
4. Write gold/job-posting-scrape/{imo_slug}/{run-date}/hiring_pattern.parquet
5. Write gold/job-posting-scrape/{imo_slug}/{run-date}/postings_scored.parquet (per-posting score detail)
6. Emit telemetry
```

### 7.3 `posting_score` axes (v0.1 seed weights — tunable post-Phase-3-feedback)

```python
posting_score = (
    role_class_weight[role_class]                  # 0.0 - 1.0 per §7.3.1
    + 0.10 * len(investment_title_hits) > 0        # title-hit is binary boost
    + 0.05 * min(len(investment_description_hits), 4) / 4  # capped description-hit count
    + 0.20 * len(series_licenses_required) > 0     # required-Series-license is strong signal
    + 0.10 * len(series_licenses_preferred) > 0    # preferred-Series-license is weaker
    + 0.10 * len(credentials_required) > 0         # CFA/CFP-required
    - 0.30 * (len(anti_signal_hits) > 0 and len(investment_title_hits) == 0)  # anti-signal penalty
)
# Clamp to [0, 1]
```

#### 7.3.1 `role_class_weight`

```python
role_class_weight = {
    "investment-professional": 0.50,    # HIGH — direct signal
    "corporate-finance": 0.30,          # MED — forward signal
    "technology": 0.25,                 # MED — forward signal (platform-buildout)
    "compliance": 0.20,                 # MED-LOW — compliance hires support advisory but not direct
    "operations": 0.15,                 # LOW
    "legal": 0.15,                      # LOW
    "sales": 0.05,                      # ANTI-LOW — most IMO sales hires are insurance/annuity
    "other": 0.05,
}
```

These weights are **DELIBERATELY HAND-TUNABLE** — they live in `config/job_posting_score_weights-v1.json` per PRD §3.4 (config/ root prefix, version-pinned filename). Andrew + IR-team can tune them after the v0.1 ranking pass without redeploying the Lambda.

### 7.4 IMO-rollup `hiring_pattern.parquet` schema

```python
HIRING_PATTERN_SCHEMA = {
    "imo_slug": str,
    "run_date": "date",
    "total_postings": int,
    "postings_by_role_class": "dict[str, int]",     # {role_class: count}
    "pct_by_role_class": "dict[str, float]",
    "series_license_required_count": int,
    "series_license_preferred_count": int,
    "investment_keyword_hit_count": int,
    "hiring_velocity_30d": int,
    "hiring_velocity_90d": int,
    "hiring_velocity_180d": int,
    "anti_signal_only_count": int,
    "anti_signal_only_pct": float,
    "top_n_postings": "list[dict]",                  # top 10 by posting_score; each is {posting_id, job_title, posting_score, source_url}
    "company_hiring_pattern_score": float,           # the IMO-level company score this channel contributes to Phase 3
}
```

### 7.5 `company_hiring_pattern_score` formula (the Phase-3 feeder)

This is what Phase 3 consolidated scoring consumes per IMO from this channel:

```python
company_hiring_pattern_score = (
    0.40 * avg(posting_score for posting in postings if role_class == "investment-professional")
    + 0.25 * normalize(series_license_required_count, 0..10)  # cap at 10 for normalization
    + 0.20 * normalize(hiring_velocity_90d, 0..50)            # cap at 50
    + 0.15 * (pct_corp_finance_role_class + pct_technology_role_class)  # forward-signal weight
    - 0.10 * anti_signal_only_pct                             # penalize sales-heavy hiring
)
# Clamp to [0, 1]
```

Phase 3 takes this score and aggregates it with the Phase-1 web-signal score + Phase-2-Part-A LinkedIn-current-state score. Phase 3 brief (`~E` lane) will define the cross-channel join formula.

### 7.6 Path

`data/find/imo/scripts/gold/job_posting/score_job_posting_gold.py`. Mandatory `from __future__ import annotations`.

---

## 8. Hand-off contract to AE 0.7

What AE 0.7 needs to wire (NOT in this brief; this brief produces the DS-side substrate AE consumes):

1. **Bright Data Bβ collectors** — per board that lands NO-GO on Bα. Each board needs its own Bright Data Web Scraper collector configured. Cost-budget per PRD Q7.
2. **`find-insure/job-board/*` Secrets Manager entries** — per-board API keys / cookies / OAuth tokens. PRD §3.5 reserved the namespace at Phase 0; AE populates at Bα HAR-audit time.
3. **`crawl_job_posting_bronze` Lambda** — fans out per (IMO, board, run-date); calls Bα-direct endpoint OR Bright Data collector per the manifest disposition; writes raw to `corp/{slug}/bronze/job-posting-scrape/{run-date}/{board}/`.
4. **IAM policy delta on `find-insure-lambda-role`** — `secretsmanager:GetSecretValue` on `find-insure/job-board/*` (already reserved per PRD §3.5).
5. **EventBridge rule** — Phase 2 Part B fans out per IMO in the Phase-1-selected subset.
6. **Cost-budget guard** in the bronze Lambda — pre-call check vs `config/cost-budgets-{version}.json` (Q4/Q7).

DS owns silver + gold + the manifest brief. AE owns bronze crawl-infra + IAM + secrets + orchestration.

---

## 9. Open questions for Andrew (at HAR-capture time)

Non-blocking on this scaffold; surface at Bα HAR-audit time:

- **Q6.1:** Capture set — confirm boards 1-6 (LinkedIn / Indeed / Glassdoor / ZipRecruiter / Wellfound / Built In) are the v0.1 set. Add or remove any.
- **Q6.2:** Cookie-renewal-class boards (LinkedIn very likely; Glassdoor possibly) — Andrew's HAR captures should include the cookie state at capture time AND a description of "how I logged in" (anonymous / personal / dedicated-burner account). Burner-account is canonical for this kind of scrape but Andrew picks the auth class.
- **Q6.3:** Direct-ATS bypass — if Andrew's Phase 1 web-scrape surfaces meaningful Greenhouse / Lever / Workday usage among IMOs, ratify whether v0.1 expands or whether direct-ATS waits for v0.2.
- **Q6.4:** Per-IMO query budget for Bβ (PRD Q7) — DS suggests $0.10 / IMO / board / scan for Bright Data Bβ-class (placeholder; AE 0.7 will source the actual Bright Data pricing). Andrew confirms the ceiling.
- **Q6.5:** Investment-keyword taxonomy v0.1 (§4.1) — confirm seed list adequate; flag any IMO-specific terminology Andrew has seen that we should add.
- **Q6.6:** Role-class-weight v0.1 (§7.3.1) — confirm `investment-professional` weighted 0.50 dominant; confirm `technology` weighted 0.25 (some IR-team intuitions might prefer 0.30+ given Andrew's "begets m&a/growth activity" framing).

---

## 10. Standing posture (until HARs land)

This scaffold is the deliverable. The Lambda implementations + per-board endpoint manifest cannot proceed without Andrew's HAR drop (PRD Q6 gate). Standing-prep continues:

- DS~D monitors inbox for HAR drop signal from Andrew (filesystem path or S3 prefix per §2.2).
- On HAR drop: DS~D fires Bα HAR-audit (~30-60min for 6 boards), produces `docs/briefs/find-insure-job-board-endpoint-manifest.md`, MCPs ws COO with RAVC2-Request on the manifest.
- ws COO + AE 0.7 ratify per-board Bα/Bβ disposition; AE 0.7 begins infra wiring per §8; DS~D begins silver+gold Lambda authoring per §6+§7.
- Sister-coordinate with `~C` (LinkedIn Part A) — Part A + Part B share the Phase-1-selected subset decision (PRD §4 Phase 2 subset gating); both run in parallel; DS~D pings ~C when Andrew's Part B HARs land in case ~C wants to chain-request Lusha-side validation HARs.

---

## 11. Cross-references

- PRD: `docs/architecture/FIND_INSURE.md` v0.3 §3.2 / §3.6 / §4 Phase 2 Part B / §7 AC3b / §9 Q6
- Sister brief (Part A LinkedIn): `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase2_part_a_linkedin_scaffold.md` (`~C` authoring)
- Sister brief (Phase 3 serving): `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase3_serving_scaffold.md` (`~E` authoring)
- Pattern precedent: `docs/briefs/smartx-rest-integration-design-20260515.md` (HAR-first REST methodology)
- Slugify-util (path-join key): `data/find/imo/scripts/_util/slugify.py` (DS 0.1.0 base shipped FIND_INSURE.002b)
- Source-list extractor (Phase 0 anchor): `data/find/imo/scripts/_meta/extract_source_list.py` (DS 0.1.0 base shipped FIND_INSURE.002 `9aaa1459d`)
- Lusha API v3 reference (Part A sister): `docs/reference/lusha-api-v3.md`
- Allocation brief: `org/tier1_exec/2.0.0_SA_COO/briefs/allocation_20260527T1647Z_find_insure_peak_priority.md`

---

## Authoring lineage

- v0.1 2026-05-27 — initial scaffold per MSTR SPAWN-WITH-DIRECTION 16:49Z + ws COO /allocation #3 16:47Z. Standing for Andrew HARs (PRD Q6 pre-gate). Per [[feedback_standby_prep_compress_to_delivery_when_context_sufficient]] — STANDBY-PREP compressed to delivery (full scaffold shipped in-session rather than literal prep).
