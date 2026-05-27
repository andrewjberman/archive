# FIND_INSURE Phase 2 Part A — LinkedIn Channel Scaffold (parse + score + Series-license detection)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §4 Phase 2 Part A; §3.2-3.5 (medallion + IAM + lifecycle); §3.3 slugify-util binding
**Lusha reference:** `docs/reference/lusha-api-v3.md` (workspace canonical; upstream <https://docs.lusha.com/apis/openapi/section/data-source-and-privacy>)
**Pod:** 0.1.0_DS_MarketIntelligence~C
**Author:** 0.1.0_DS_MarketIntelligence~C (DS scaffold; CTO arch-review + CVO arch-corroborate gated post-RAVC2)
**Spawn:** MSTR `[SPAWN-WITH-DIRECTION]` 2026-05-27T~16:49Z per Andrew sovereign 16:46Z peak-priority + ws COO `/allocation #3`
**Status:** scaffold draft — pre-Phase-2-execution (parallel to Phase 1 active execute); RAVC2 chain to ws COO on ship
**Sizing:** ~60min wall (scaffold scope; no impl)

---

## 1. Scope

This brief scaffolds Phase 2 Part A — the LinkedIn / LushaAI enrichment channel — **pre-execution**, parallel to Phase 1 active execute. Three deliverables per spawn directive:

1. **`parse_linkedin_silver`** design (bronze → silver: structure Lusha responses into one-row-per-employee silver records)
2. **`score_linkedin_gold`** design (silver → gold: per-employee relevance scoring + per-company rollup)
3. **Series-license regex/NLP draft** for Series 7 / 65 / 66 / 24 / 63 detection (the load-bearing signal-extraction sub-deliverable consumed by `score_linkedin_gold`)

`crawl_linkedin_bronze` (bronze emit; the upstream Lusha caller) is **out of scope of this scaffold** — its endpoint sequencing is already baked into PRD v0.3 §4 Phase 2 Part A table per "endpoint-by-endpoint capability mapping baked at PRD scope" doctrine (ws CTO v0.2 amendment). This brief consumes the bronze contract that PRD specifies and designs the downstream silver + gold stages.

**What this brief is not:** not Lambda implementation, not a TO. The downstream TO author (ws COO) decomposes this scaffold into per-Lambda TOs at Phase 2 Part A dispatch.

---

## 2. Bronze contract (consumed; not designed here)

Per PRD v0.3 §4 Phase 2 Part A, `crawl_linkedin_bronze` writes per-IMO Lusha responses to:

```
opal-data-imo/corp/{slug}/bronze/linkedin-scrape/{YYYY-MM-DD}/
  companies-search-response.json        # POST /v3/companies/search response (domain -> companyId resolution)
  companies-enrich-response.json        # POST /v3/companies/enrich response (firmographics)
  contacts-prospecting-response.json    # POST /v3/contacts/prospecting response (leadership candidate list)
  contacts-enrich-response.json         # POST /v3/contacts/enrich response (high-score subset reveal)
  run-metadata.json                     # {run_id, started_at, ended_at, credits_burned, x-rate-limit-* captured, error_log}
```

Silver consumes these five artifacts. The bronze contract preserves every field Lusha returns — see Lusha API v3 doc §7.2 (Enrich response shape) for the full firmographic + contact-profile payload.

**Cost-discipline note carried forward to bronze TO:** per Lusha v3 doc §8 + PRD Q4, Phase 2A worst-case credit burn = 100 IMOs × ~10 enriched contacts × (`api_search` + `revealEmail` + `revealPhone` + bio reveal) is materially expensive. Bronze TO must wire:
- Pre-run `GET /v3/account/usage` (call budget AND single 5/min hit at job start)
- `x-minute-requests-left` header capture + back-off on every Lusha call
- Per-IMO + global credit-budget gates from `config/cost-budgets-{version}.json` (PRD §3.4 lifecycle)
- Halt-on-`402` discipline (no silent credit burn) + alert chain to AE / IR-team-budget-watcher
- GDPR `451` skip + log discipline

---

## 3. `parse_linkedin_silver` — design

### 3.1 Inputs / outputs

**Reads:** `corp/{slug}/bronze/linkedin-scrape/{YYYY-MM-DD}/contacts-{prospecting,enrich}-response.json` + `companies-enrich-response.json` for the company-level join key.

**Writes:** `corp/{slug}/silver/linkedin-scrape/{YYYY-MM-DD}/employees.parquet` (one row per leadership-class employee; mirror JSON if parquet schema-tooling complications arise — Phase 0 precedent is JSON-first per source-list extractor).

### 3.2 Silver discipline — CLAUDE.md Rule 17 binding

**Silver tier performs ONLY deduplication + type standardization.** No field slimming, no `fillna()`, no `dropna()`, no business-row filtering. Per CLAUDE.md Rule 17 + Andrew direct 2026-05-13 ("agents that pare down available fields, they need to not fucking do that").

What silver IS permitted to do:
- Dedupe `(company_slug, lusha_contact_id)` exact-row duplicates (Lusha IDs are stable + canonical join key)
- Type standardization: `lusha_contact_id` + `lusha_company_id` → `Int64` (nullable per `coerce_silver_ids()` discipline per ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY); dates → ISO8601-Z strings; tenure → preserved verbatim from Lusha
- Unicode whitespace flatten on text fields (bio, headline, position-descriptions) — strip leading/trailing + collapse internal whitespace runs

What silver is NOT permitted to do:
- **NO** `output_cols` projection narrowing — every field Lusha returns flows through (firmographics: size, revenue, year-founded, SIC/NAICS, technologies, funding rounds; contact: full position-history, education, certifications, languages, locations)
- **NO** `fillna()` of missing emails/phones/tenure — null preserved, gold tier decides
- **NO** row drops by business semantic (e.g., "drop rows where seniority != C-suite" is a gold-tier projection)
- **NO** Series-license regex evaluation — Series detection is judgment-laden NLP and belongs in gold

### 3.3 Schema (silver employees parquet)

| Column | Type | Source | Notes |
|---|---|---|---|
| `schema_version` | str | constant `"v1.0"` (CTO Q-S1 disposition §12.1) | forward-compat detection across schema amendments |
| `company_slug` | str | derived via `data/find/imo/scripts/_util/slugify.py` from source-list `company_name` | join key to Phase 1 web-scrape gold + Phase 3 serving |
| `lusha_company_id` | Int64 | `companies-enrich-response.json` `companyId` | resolved at bronze stage |
| `lusha_contact_id` | Int64 | `contacts-enrich-response.json` per-contact `id` | dedupe key + Phase 3 join |
| `full_name` | str | enrich response | |
| `first_name` / `last_name` | str | enrich response | |
| `current_title` | str | enrich response | |
| `current_seniority` | str | prospecting + enrich `seniority` field | |
| `current_departments` | list[str] | enrich `departments` | preserved as list, not flattened |
| `tenure_start_date` | str (ISO8601-Z) | enrich `currentPosition.startDate` | null preserved |
| `tenure_end_date` | str (ISO8601-Z) | null for current role | |
| `prior_positions` | list[struct] | enrich `previousPositions` | full history preserved (not slimmed) |
| `linkedin_url` | str | enrich `linkedinUrl` | |
| `email_revealed` | str | enrich `emails[]` after reveal | null if not revealed |
| `phone_revealed` | str | enrich `phones[]` after reveal | null if not revealed |
| `bio_text` | str | enrich `summary` / `about` | verbatim — gold-tier scans this for Series regex |
| `headline_text` | str | enrich `headline` | verbatim |
| `experience_text` | str | concat of all position-description fields | verbatim — gold-tier scans this |
| `education` | list[struct] | enrich `education` | full preserved |
| `certifications` | list[struct] | enrich `certifications` | **load-bearing for Series-license detection** — explicit cert list often names licenses directly |
| `firmographic_industries` | list[str] | companies-enrich `industries` | company-level field denormalized to employee row for gold convenience |
| `firmographic_naics` | list[str] | companies-enrich `naics` | NAICS 524210 = canonical IMO match |
| `firmographic_size` | str | companies-enrich `size` | bucket label |
| `firmographic_revenue` | str | companies-enrich `revenue` | bucket label |
| `firmographic_year_founded` | Int64 | companies-enrich `yearFounded` | |
| `opt_out_at` | str (ISO8601-Z) | initially null; populated by Phase 2 mandatory opt-out webhook receiver (see §6) | |
| `bronze_run_id` | str | `run-metadata.json` `run_id` | lineage |
| `bronze_fetched_at` | str (ISO8601-Z) | `run-metadata.json` `started_at` | lineage |

`prior_positions` and `certifications` are kept as struct lists in parquet (not flattened to columns) so the entire LinkedIn profile is reconstructable from silver alone — gold-tier scans concat'd text but silver preserves structure for future re-scoring or NLP upgrades.

### 3.4 Dedupe + type-standardize logic

```python
# Pseudo-code (illustrative; not impl)
from __future__ import annotations  # CLAUDE.md Rule 15
import pandas as pd
from data.find.imo.scripts._util.slugify import slugify

def parse_linkedin_silver(slug: str, run_date: str) -> pd.DataFrame:
    bronze_dir = f"s3://opal-data-imo/corp/{slug}/bronze/linkedin-scrape/{run_date}/"
    contacts = read_json(bronze_dir + "contacts-enrich-response.json")
    company = read_json(bronze_dir + "companies-enrich-response.json")

    rows = []
    for contact in contacts["contacts"]:
        rows.append({
            "company_slug": slug,
            "lusha_company_id": company["companyId"],
            "lusha_contact_id": contact["id"],
            "full_name": contact.get("fullName"),
            # ... all fields per §3.3 schema ...
            "experience_text": "\n\n".join(
                p.get("description", "") for p in contact.get("previousPositions", [])
            ),
        })

    df = pd.DataFrame(rows)
    df = coerce_silver_ids(df, ["lusha_company_id", "lusha_contact_id"])  # ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY
    df = df.drop_duplicates(subset=["company_slug", "lusha_contact_id"])
    # NO fillna; NO output_cols projection; NO row-filter by business semantic
    return df
```

### 3.5 Open silver-design question routed to CTO

- **Q-S1:** parquet schema for `prior_positions` (list of structs) — pyarrow native supports nested but Phase 0 precedent is JSON. Recommend parquet for Phase 2A (efficiency at ~5-10k employee rows post-Part-A) with JSON fallback if pyarrow nested-struct support proves fragile in the Lambda runtime. CTO disposition pre-Phase-2-dispatch.

---

## 4. `score_linkedin_gold` — design

### 4.1 Inputs / outputs

**Reads:** `corp/{slug}/silver/linkedin-scrape/{YYYY-MM-DD}/employees.parquet`

**Writes:**
- `corp/{slug}/gold/linkedin-scrape/{YYYY-MM-DD}/employees-scored.parquet` (one row per employee + score axes + final employee_score)
- `corp/{slug}/gold/linkedin-scrape/{YYYY-MM-DD}/company-rollup.parquet` (one row per company: max employee score, series-licensed count, leadership count by class)

### 4.2 Per-employee scoring axes (PRD §4 Phase 2 Part A + §9 Q2)

| Axis | Weight (PRD Q2 default) | Computation |
|---|---|---|
| `years_at_company_score` | 0.25 | `(today - tenure_start_date).days / 365.25`, capped at 20yr, normalized to [0,1] = `min(years/10, 1.0)` — 10+ years saturates |
| `title_seniority_score` | 0.25 | enum map: `Owner/Founder/President/CEO`=1.0; `C-suite (CIO,CFO,CTO,COO,CMO,CCO)`=0.95; `MD/EVP`=0.85; `SVP/Head of`=0.75; `VP/Director`=0.6; `Senior Manager`=0.4; `Manager`=0.25; `IC`=0.1. Matched via case-insensitive title regex; uses `current_title` primarily, `current_seniority` as fallback |
| `series_license_count_weighted` | 0.30 | from §5 Series detection; per-license weights `{24: 0.40, 65: 0.30, 66: 0.30, 7: 0.20, 63: 0.10}` summed; cap at 1.0. **v0.3 weights per CVO Axis 2 CONCERN absorption + Andrew Q2 ratification gate (§13.2).** Series 24 highest (principal/managerial = asset-mgmt-organization OPERATOR); Series 65/66 (IAR — Uniform Investment Adviser Law + combined 63+65) = fee-based investment advisory = **the asset-management business model itself** (CVO insight: 65/66 are AM-business-model licenses, NOT Series 7); Series 7 (general securities representative = broker-dealer/commission) closer to insurance-sales-side; Series 63 most common blue-sky exam = weak standalone signal |
| `title_keyword_match_score` | 0.20 | regex over `current_title` for asset-mgmt-class terms: `wealth\|advisory\|investment\|asset\s+management\|portfolio\|fiduciary\|RIA\|IAR` — match = 1.0, no match = 0.0 |

**Final employee score** = sum of weighted axes ∈ [0, 1].

### 4.3 Per-company rollup axes (feeds Phase 3 company score)

| Field | Computation |
|---|---|
| `max_employee_score` | max of per-employee scores at this company |
| `mean_employee_score` | mean across leadership-class employees |
| `series_licensed_count` | count where any `series_N_match` = true |
| `series_24_count` | count where `series_24_match` = true (principal-class proxy) |
| `c_suite_count` | count where `title_seniority_score >= 0.85` |
| `asset_mgmt_title_keyword_count` | count where `title_keyword_match_score == 1.0` |
| `total_leadership_count` | row count |

Phase 3 `build_companies_serving` consumes these axes plus Phase 1 web-scrape gold to compute the **company-level relevance score** (PRD §4 Phase 3 deliverable 2: `Company score = aggregate of (Phase 1 web-signal score) + (max employee score in company) + (count of Series-licensed leadership)`).

### 4.4 Output schema (gold employees-scored)

Silver schema (preserved) +:
- `series_7_match` / `series_65_match` / `series_66_match` / `series_24_match` / `series_63_match` (bool)
- `series_*_evidence` (list[struct]: `{source_field, match_text, surrounding_context}`)
- `years_at_company` (float; years)
- `years_at_company_score` (float [0,1])
- `title_seniority_class` (str enum)
- `title_seniority_score` (float [0,1])
- `series_license_count_weighted` (float [0,1])
- `title_keyword_match_score` (float [0,1])
- `employee_score` (float [0,1]) — final weighted sum
- `scoring_methodology_version` (str; e.g. `v0.1`)

### 4.5 Methodology version pinning

`scoring_methodology_version` is the link to `s3://opal-data-imo/config/scoring-weights-{version}.json` (PRD §3.2). Default v0.1 weights are baked into the Lambda; loading from config enables tuning post-IR-team-review (PRD §9 Q2). Phase 3 `serving/_history/{date}/scoring.json` time-travel archive (PRD §3.2 + Q-B ruling) captures the methodology+weights at each ship — re-scoring under a new regime preserves the audit trail.

---

## 5. Series-license regex / NLP draft

### 5.1 Detection bar (Series 7 / 65 / 66 / 24 / 63)

Detection runs in `score_linkedin_gold` over three silver-column text surfaces (gold scans; silver preserves):

1. `bio_text` (LinkedIn summary / about — highest density of explicit cert mention)
2. `headline_text` (LinkedIn headline — high-density for active license-holders)
3. `experience_text` (concatenated position descriptions — broader; more false-positive risk)

Plus structured `certifications` list (silver preserves) — explicit cert names often disambiguate cleanly without regex.

### 5.2 Positive patterns (case-insensitive; per license)

Each pattern returns the first match's start index + surrounding ±50 chars as `surrounding_context` for evidence emission.

```python
SERIES_PATTERNS: dict[int, list[str]] = {
    7: [
        r"\bseries\s*7\b",
        r"\bs7\b",
        r"\bgeneral\s+securities\s+representative\b",
    ],
    65: [
        r"\bseries\s*65\b",
        r"\buniform\s+investment\s+adviser\s+law\s+examination\b",
        # IAR (Investment Adviser Rep) is the role-name; Series 65 is one path.
        # Pattern is BROAD — IAR alone is +1 evidence, not standalone confirmation.
        r"\bIAR\b",
    ],
    66: [
        r"\bseries\s*66\b",
        r"\buniform\s+combined\s+state\s+law\s+examination\b",
    ],
    24: [
        r"\bseries\s*24\b",
        r"\bgeneral\s+securities\s+principal\b",
    ],
    63: [
        r"\bseries\s*63\b",
        r"\buniform\s+securities\s+(agent|state)\s+(state\s+)?law\b",
    ],
}
```

### 5.3 Negative-context filters (FP suppression)

Within ±60 chars of a positive match, search for aspirational / lapsed / negation context. If ANY of these match, the positive hit is **suppressed** (recorded as a probe but not counted toward the license-count).

```python
NEGATIVE_CONTEXT: list[str] = [
    r"\bstud(y|ying|ied)\s+(for|towards)\b",
    r"\bpreparing\s+(to\s+take\s+|for\s+)\b",
    r"\bplan(ning|s)?\s+to\s+(take|sit|pursue)\b",
    r"\bexam\s+(scheduled|date|in|target)\b",
    r"\b(target|expected|anticipated)\s+(date|completion)\b",
    r"\bcandidate\s+for\b",
    r"\b(soon|upcoming|q[1-4])\b.*\b20\d{2}\b",  # "Q2 2026", "upcoming 2026"
    r"\bin\s+progress\b",
    r"\b(lapsed|expired|no\s+longer\s+active|formerly\s+held|previously\s+held)\b",
    r"\bnot\s+(currently\s+)?(active|registered|licensed)\b",
]
```

### 5.4 Confidence elevators + 4th detection path (CVO Axis 1 additive)

**Four detection paths** (all at gold tier per CLAUDE.md Rule 17 boundary; silver preserves all four source surfaces):
1. `bio_text` regex (LinkedIn summary / about)
2. `headline_text` regex (LinkedIn headline)
3. `experience_text` regex (concatenated position descriptions)
4. **`certifications[].name` struct-enum-match** — explicit Lusha-canonical cert names (e.g. `"Series 7"`, `"Series 65"`, `"Investment Adviser Representative"`). Per CVO Axis 1 disposition: cert-name canonicalization NOT documented stable forever; treating as text scan at gold (not silver-flag) protects against silent drift if Lusha renames `"Series 7"` → `"FINRA Series 7"` in a future API rev. Match implementation: case-insensitive substring against the `SERIES_PATTERNS` keys + license-name alternates.

If ANY of the following are present alongside a positive match, evidence quality flag = `HIGH`:
- Match in `certifications` structured field (path 4) — most reliable signal
- A FINRA CRD# is also surfaced in profile (`r"\bCRD\s*#?\s*(\d{6,7})\b"`) — Lusha may or may not expose this; capture if present
- **Multiple positive paths match for the same license** within the profile — e.g. text-regex on bio_text + struct-enum-match on certifications[] for the same Series N; OR text-regex on bio_text + text-regex on experience_text for the same Series N + `general securities representative` co-occurrence

Otherwise evidence quality flag = `STANDARD`.

### 5.5 Evidence-emission schema

Per employee, per detected license:

```json
{
  "license": 7,
  "matched": true,
  "evidence": [
    {
      "source_field": "bio_text",
      "match_text": "Series 7",
      "match_start": 142,
      "surrounding_context": "...holds Series 7, 63 and 65 licenses; CFP designation...",
      "negative_context_hit": null,
      "confidence": "HIGH"
    }
  ],
  "crd_number": "1234567"
}
```

If `matched: false` AND a positive pattern hit was suppressed by negative-context, surface the suppression as a probe (audit trail):

```json
{
  "license": 7,
  "matched": false,
  "evidence": [
    {
      "source_field": "experience_text",
      "match_text": "Series 7",
      "surrounding_context": "...currently studying for Series 7 exam...",
      "negative_context_hit": "studying for",
      "confidence": "SUPPRESSED"
    }
  ]
}
```

### 5.6 FINRA BrokerCheck cross-reference path (v0.2 candidate — not Phase 2A)

If a CRD# is captured (§5.4), a v0.2 sub-pipeline can hit `https://brokercheck.finra.org/individual/summary/{crd}` for authoritative license-status confirmation. Out of v0.1 scope:
- Throttle / scrape-discipline against FINRA (rate-limited public surface)
- HAR-analysis path or Bright Data middleman (mirror Phase 2 Part B Stage Bα/Bβ pattern)
- Cost-vs-value: probably not worth it for v0.1 — regex evidence on the LinkedIn-side is already strong; FINRA validates rather than discovers

**Phase 2A discipline:** capture CRD# in `score_linkedin_gold` evidence emission; flag in the v0.1 RAVC2 as the v0.2 candidate sub-deliverable.

### 5.7 Empirical-tightening protocol (CVO Axis 3 additives absorbed)

Phase 2A first run produces sample evidence on the Phase-1-selected IMO subset (~20 IMOs, ~200 employees). Pre-RAVC2 discipline:

1. **STRATIFIED positive sample (CVO Axis 3 ADDITIVE-1):** 5 Series 7 + 5 Series 65/66 + 5 Series 24 + 5 Series 63 = 20 total. Stratification keeps per-license CI roughly equal; uniform random would cluster on Series 63 (most common) and starve Series 24 (sparsest). Adjust per-class proportions if empirical per-license-rate diverges materially.
2. **CROSS-IMO sample (CVO Axis 3 ADDITIVE-2):** cap at **max 3 samples per IMO** across the 20 positives. Otherwise a single firm's text-style biases the FP/FN read (e.g. one firm's bio templates that name licenses inline drive false signal of detector quality).
3. 20 randomly-sampled negative-result rows (no license matched) — stratify too (4 per license-class) to estimate FN rate per-license. Particularly important for Series 24 (highest weight) and Series 65/66 (highest signal per v0.3 weight ordering).
4. **STRUCTURED-JSON evidence (CVO Axis 3 ADDITIVE-3):** spot-check output lands at `qa/phase-2-spot-checks-{YYYY-MM-DD}/spotcheck.json` in structured shape — `{employee_lusha_id, license, regex_path_matched, manual_verdict, classification (FP/FN/TP/TN), evidence_text, surrounding_context, sample_strata (positive/negative + license-class), imo_slug}` — NOT free-text narrative. Programmatic re-evaluation at v0.2 FINRA BrokerCheck cross-ref ship: compare v0.1 manual verdicts against v0.2 BrokerCheck-authoritative results without re-spot-checking. Saves a re-spot-check cycle.
5. Tighten patterns from the FP/FN analysis — typical adjustments are negative-context expansions, not positive-pattern additions.
6. Spot-check repeated post-tightening until FP ≤ 5% AND FN ≤ 10% per-license (gold-validate-style thresholds; numeric AC at TO-authoring).

Empirical-tightening evidence appears in the Phase 2A RAVC2 — `qa/phase-2-spot-checks-{YYYY-MM-DD}/` (PRD §3.2 `qa/` prefix).

---

## 6. GDPR opt-out integration (MANDATORY pre-Phase-2A scale)

Per Lusha v3 doc §9.6 + PRD §11 (Lusha integration mapping row 5: "GDPR opt-out compliance — mandatory before scale"):

- Phase 2A ships with the `opt_out_at` column wired into silver schema (§3.3), defaulted null.
- Phase 2A bronze TO authors the **opt-out webhook receiver** Lambda (API Gateway → Lambda → SQS → silver writer): verifies `X-Lusha-Signature` HMAC-SHA256, writes the opt-out record to silver with `opt_out_at` ISO8601-Z timestamp, propagates to `serving/employees.parquet` to mark the row suppressed.
- **Pre-search opt-out check (CVO Axis 4 ADDITIVE-1):** `crawl_linkedin_bronze` queries the locally-maintained opt-out cache (or Lusha's `GET /v3/contacts/opt-outs` if available per Lusha v3 catalog — confirm pre-Phase-2A-dispatch) BEFORE issuing `POST /v3/contacts/enrich` for any contact. Skips already-opted-out contacts at the source. **Double-win:** cost-discipline (no credits burned on opted-out enrichment) + GDPR alignment (no enrich call against an opted-out individual). Local opt-out cache populated from inbound webhook fires + persisted in `config/opt-outs-current.json` or a DynamoDB table — TO-authoring picks (DynamoDB recommended for atomic single-write opt-out webhook → cache update path).
- **Phase 3 serving-tier filter explicit AC (CVO Axis 4 ADDITIVE-2):** Phase 3 `build_employees_serving` MUST include explicit AC: "`serving/employees.parquet` excludes rows where `opt_out_at IS NOT NULL`; `serving/companies.parquet` excludes companies where all leadership opted out OR adjusts the company score to exclude opted-out employees from the rollup." Defensive specification — implied-but-not-written is the gap-class that causes serving to silently include opted-out rows. Route to ws COO at Phase 3 TO authoring.
- `score_linkedin_gold` filters out rows with `opt_out_at IS NOT NULL` from the scoring pass — opted-out contacts neither appear in gold output nor in Phase 3 serving (PRD AC4).

Open question routed to ws CTO + Andrew (Lusha doc §12 Q-L3):

- **Q-L3 carried:** opt-out webhook receiver in scope for Phase 2A or v0.3 deferral? IR-team is US-focused; safemoneybroadcasting universe may include cross-border / EU-located individuals — recommend Phase 2A scope (legal + structural safer than v0.3 catch-up).

---

## 7. Cost-discipline cross-reference (PRD §9 Q4)

Forwarded to bronze TO author (`crawl_linkedin_bronze`):

- Pre-run `GET /v3/account/usage` (singleton per IMO-batch run; respect 5/min limit)
- `x-minute-requests-left` + `x-hourly-requests-left` + `x-daily-requests-left` header capture per call → `bronze/.../run-metadata.json` + `telemetry/{lambda}/{date}/{run-id}.ndjson` (PRD §3.2 telemetry prefix)
- Per-IMO + global credit-budget gates from `config/cost-budgets-{version}.json` — abort the per-IMO scan if either gate violates
- Halt-on-`402` (no silent credit burn) + alert chain to AE + IR-team-budget-watcher
- Action-class telemetry: per call, capture `billing.creditsCharged` for accurate aggregation against budget
- Lusha v3 §6 error-handling discipline: `429` exponential back-off (initial 1s, doubling, max 60s, max 5 retries); `5XX` exponential back-off (same params); `451` log + skip; `401`/`403` halt + alert

Phase 2A worst-case naive scope-bound: 100 IMOs × ~10 leadership × (1 `api_search` + 1 `revealEmail` + 1 `revealPhone` + 1 company `api_search` + 1 `reveal_company`) ≈ 3500 credit-events. Phase-1-subset gate (top quintile + Series-mention) reduces to ~20-25 IMOs × ~10 = ~700-900 credit-events. Hard budget number routes to Andrew at Q4 disposition.

---

## 8. Compiler-tools mandate (per CLAUDE.md / TO discipline)

**Before-write (per Lambda):**
- `comp-pipescript io data/find/imo/scripts/silver/parse_linkedin_silver.py` (column gaps + S3-dynamic reads + portal consumers)
- `comp-pipescript io data/find/imo/scripts/gold/score_linkedin_gold.py`
- `comp-iam service find-insure-parse-linkedin-silver` + `comp-iam service find-insure-score-linkedin-gold` (boto3 S3 read/write surface area against PRD §3.5 IAM)

**Before-commit:**
- `comp-pipescript deployed [script]` for any in-flight deploy
- `comp-validate score_linkedin_gold.py --artifact /tmp/score_linkedin_gold-sample.parquet` (per `gold_validate_config.yaml` once gold-validate config covers FIND_INSURE)
- `.tools/ds-commit-gate.sh` (py_compile + ds-precommit-check + ruff)
- `from __future__ import annotations` first import (CLAUDE.md Rule 15)

**After-commit:**
- `comp-blast score_linkedin_gold` (blast radius against Phase 3 `build_employees_serving` + Phase 3 `build_companies_serving`)
- `comp-iam gaps` (if iam.tf changed)

**Slug discipline:**
- Both Lambdas import `from data.find.imo.scripts._util.slugify import slugify` (PRD v0.3 §3.3 binding; single source of slug-truth)
- Slug-stability spot-check appears in Phase 2A RAVC2 (matches FIND_INSURE.002 AC7 pattern)

---

## 9. Acceptance criteria for Phase 2A scaffold (this brief)

This brief is the scaffold; Phase 2A TO acceptance criteria are authored by ws COO at TO-decomposition. The scaffold itself is accepted when:

- **AC-S1.** Brief lands at `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase2_part_a_linkedin_scaffold.md` (this path).
- **AC-S2.** Three sub-designs present: parse_linkedin_silver (§3), score_linkedin_gold (§4), Series-license regex/NLP draft (§5).
- **AC-S3.** Silver design honors CLAUDE.md Rule 17 (no field slimming, no fillna, no dropna; dedupe + type-standardize only).
- **AC-S4.** Series detection covers 7 / 65 / 66 / 24 / 63 with positive patterns + negative-context FP suppression + evidence-emission schema.
- **AC-S5.** Compiler-tools mandate per CLAUDE.md + slug discipline per PRD v0.3 §3.3 explicit.
- **AC-S6.** Open questions routed to ws CTO (Q-S1 parquet nested-struct) + Andrew (Q-L3 GDPR opt-out scope, Q4 cost cap) — explicit, not implicit.
- **AC-S7.** Cost-discipline cross-reference + GDPR opt-out integration baked at scaffold scope (not deferred to TO time).

---

## 10. RAVC2 chain

**To:** 2.0.0_SA_COO (ws COO)
**CC:** 1.0.0_SA_CTO (PRD architect) + 3.0.0_SA_CVO (arch-corroborate per LD-0022 priority architectural-corroborator) + 0.0.0_AB_MSTR (spawn dispatcher)
**Subject:** `[RAVC2-Request] FIND_INSURE Phase 2 Part A scaffold — parse + score + Series-license detection`

Payload:
- Brief commit hash (this file)
- Three sub-designs landed per AC-S2
- CLAUDE.md Rule 17 honored per AC-S3
- Open questions Q-S1 / Q-L3 / Q4 explicit per AC-S6
- Recommended ws COO decomposition: Phase 2A into 3-4 TOs (`crawl_linkedin_bronze` + `parse_linkedin_silver` + `score_linkedin_gold` + opt-out-webhook-receiver if Phase-2A-scope per Q-L3) post-Phase-1-RAVC2-Accept (subset decision gates 2A dispatch per PRD §4)

---

## 11. Cross-references

- **PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3.2-§3.5 (medallion + IAM + lifecycle), §4 Phase 2 Part A (Lusha endpoint mapping table)
- **Lusha API v3:** `docs/reference/lusha-api-v3.md` §7.1-§7.6 (endpoints), §8 (billing), §9 (webhooks + opt-out)
- **Slugify-util:** `data/find/imo/scripts/_util/slugify.py` (PRD v0.3 §3.3 binding)
- **Phase 0 precedent:** FIND_INSURE.002 source-list extractor TO + work log `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-27/work_1602Z_find_insure_002_source_list_extractor_ship.md`
- **Silver-discipline doctrine:** CLAUDE.md Rule 17 + `memory/feedback_silver_no_field_slimming.md`
- **CVO architectural authority:** LD-0022 priority architectural-corroborator + LD-0025 CORROBORATE-with-additive-META materializes-immediately
- **Operating-mode doctrine:** LD-0090 ALWAYS-PROCEED + Andrew-non-response-1tick-route-to-CVO

---

## 12. Architectural ratifications (v0.2 amendment — ws CTO arch-disposition 2026-05-27T~17:08Z)

ws CTO landed disposition `20260527T170844Z` (~3min spawn-to-disposition after RAVC2-Request) on all three open questions. Absorbed wholesale:

### 12.1 Q-S1 (parquet nested-struct) — APPROVED

- **Primary:** parquet via pyarrow native nested-struct support for `prior_positions` + `certifications` (standard fabric pattern; yang-pipeline + other parquet artifacts have nested already)
- **Fallback:** JSON if Lambda-runtime pyarrow nested-struct support proves fragile at scale-test (mirrors Phase 0 .002 extract_source_list JSON emit)
- **Schema versioning:** add `schema_version: "v1.0"` field to silver records (forward-compat detection)
- **Compression:** parquet snappy default

§3.3 silver schema amended: insert `schema_version str "v1.0"` row at the top of the column table; carry forward to all downstream Lambdas.

### 12.2 Q-L3 (opt-out webhook receiver Phase 2A scope) — PULL-FORWARD

CTO disposition: pull-forward unless Andrew overrides (LD-0090 ALWAYS-PROCEED: Andrew silent ≥1 cycle = pull-forward binds; Andrew CC'd for sovereign-window visibility on scope expansion).

Reasoning confirmed:
- GDPR opt-out structurally mandatory if any EU-located individual surfaces
- safemoneybroadcasting US-focused not US-exclusive
- v0.3 catch-up cost > Phase 2A upfront (retrofit into populated silver = data hygiene nightmare)
- Receiver design (API GW → Lambda HMAC-SHA256 verify per Lusha v3 §9.3 → SQS → silver writer) canonical
- `find-insure/lusha-ai/webhook-secret` sub-namespace under existing §3.5 IAM = zero IAM amend

**Phase 2A receiver discipline (CTO directive):** stub endpoint at Phase 2A but DO NOT subscribe-to-Lusha until Phase 2A execution gate fires — avoids credit overhead on delivered-but-unused webhook events. Subscription via `POST /api/subscriptions/opt-out` (Lusha v3 §9 endpoint catalog) deferred to Phase 2A execute.

§6 GDPR section amended: subscription deferred; receiver-stub mandatory at Phase 2A scaffold-impl.

### 12.3 Q4 (Lusha credit budget) — Andrew sovereign; CTO proposed defaults bind per LD-0090

| Tier | Default (LD-0090: Andrew silent ≥1 cycle = binds) | Rationale |
|---|---|---|
| **Per-IMO ceiling Phase 2A** | 50 credits | ~10 leadership × (Search + Enrich-email + Enrich-phone + company-reveal) + headroom; soft-abort cleanly if ceiling trips |
| **Global daily ceiling Phase 2A** | 1500 credits | ~2x headroom over post-Phase-1-subset worst-case (~700-900); ~3x headroom over conservative subset |
| **Abort behavior** | soft-stop | Lambda completes current IMO + telemetry record with `cost_ceiling_hit: true` + clean exit; next-run resumes from next IMO |
| **Config path** | `config/cost-budgets-v1.json` | PRD v0.3 §3.2 + §3.5 (Lambda-init load, in-memory increment) |

§7 cost-discipline section amended: defaults baked + soft-stop abort semantics added to bronze TO scope.

### 12.4 Hard constraint (CTO) — Phase 1 / Phase 2A sequencing

**No Lusha API endpoint calls until Phase 1 ships + Andrew confirms subset cut.** Scaffold + impl unit-test-clean against fixture JSON; live API calls Phase-1-RAVC2-Accept-gated. STANDBY-PREP class discipline (sister to ~A parse-web scaffold today).

### 12.5 Disposition summary

All three open questions cleared at scaffold layer; no architectural blockers remain. Phase 2A TO decomposition (ws COO) now has explicit:
- Schema version pin (Q-S1)
- Receiver-stub-at-2A + subscription-defer-to-2A-execute (Q-L3)
- Per-IMO + global cost ceilings + soft-stop abort semantics + config path (Q4)
- STANDBY-PREP discipline (CTO hard constraint)

— 0.1.0_DS_MarketIntelligence~C 2026-05-27T~17:0?Z (v0.1 scaffold)
— 0.1.0_DS_MarketIntelligence~C 2026-05-27T~17:11Z (v0.2 amendment — CTO Q-S1/Q-L3/Q4 dispositions absorbed)

---

## 13. CVO ARCH-CORROBORATE absorption (v0.3 amendment — 2026-05-27T~17:15Z)

ws CVO landed 4-axis ARCH-CORROBORATE response `20260527T1705Z_to_0.1.0_DS_MarketIntelligence_C_phase2a_linkedin_scaffold_arch_corroborate.md` per LD-0022 priority architectural-corroborator + LD-0094 framing-lean→explicit-verdict-on-invite. Headline: structurally sound; 1 P1 + 3 P2 + 4 mandatory unknown-unknowns.

### 13.1 Axis 1 (silver vs gold boundary) — CORROBORATE-with-additive

**Verdict: CORROBORATE** the "all detection in gold" framing per CLAUDE.md Rule 17. **ADDITIVE absorbed in §5.4:** `certifications[].name` struct-enum-match becomes a 4th gold detection path (alongside bio_text + headline_text + experience_text regex). Multi-path matches elevate confidence to HIGH per §5.4. Reasoning: Lusha cert-name canonicalization NOT documented strictly stable forever — gold-text-scan path protects against silent rename drift.

### 13.2 Axis 2 (Series-license weights) — **CORROBORATE-with-CONCERN — P1 — Andrew route**

**Verdict: CONCERN on Series 7 (.35) vs Series 65/66 (.30) ordering** — reads BACKWARDS for FIND_INSURE objective:
- Series 65 (Uniform Investment Adviser Law) + Series 66 (combined 63+65) ARE the IAR licenses = fee-based investment advisory = **the asset-management business model itself**
- Series 7 (general securities representative) = broker-dealer/commission-based = closer to insurance-sales-side
- For FIND_INSURE specifically (not generic securities-licensed detection), 65/66 should weight HIGHER than 7

**Weights revised (provisional default) per §4.2:** `{24: 0.40, 65: 0.30, 66: 0.30, 7: 0.20, 63: 0.10}` — Series 24 anchor (.40) preserved; Series 7 dropped from .35 → .20 (smallest correction matching CONCERN); Series 65/66 unchanged at .30; Series 63 unchanged at .10. **Andrew Q2 ratification gate fires pre-Phase-2A-first-run** — alternative defensible orderings:
- `{24: 0.35, 65: 0.35, 66: 0.35, 7: 0.20, 63: 0.10}` (IAR-as-equal-with-24)
- `{65: 0.40, 66: 0.40, 24: 0.35, 7: 0.25, 63: 0.10}` (IAR-as-most-specific)

**Why P1 not P0:** soft-fix path exists via config-bump (`config/scoring-weights-{version}.json` per PRD §3.2 + §4.5); doesn't block Phase 0/1. Specifically gates Phase 2A first-run **initial-list quality** — IR-team reviews against wrong signal-priority bias their judgment of which IMOs to pursue (AC5 ratification load-bearing).

**Routing:** Andrew direct ask via separate message thread (1min Andrew effort). LD-0090 ALWAYS-PROCEED: Andrew silent ≥1 cycle = v0.3 provisional weights bind.

### 13.3 Axis 3 (empirical-tightening 20+20 protocol) — CORROBORATE-with-additives

**Verdict: CORROBORATE** the 20+20 sample size for Phase 2A first-ship. **3 ADDITIVES absorbed in §5.7:**
- Stratified positive sample: 5 Series 7 + 5 Series 65/66 + 5 Series 24 + 5 Series 63 (Axis 3 ADDITIVE-1) — keeps per-license CI roughly equal
- Cross-IMO sample cap (max 3 samples per IMO) (Axis 3 ADDITIVE-2) — prevents single-firm text-style bias
- Structured-JSON evidence (not free-text narrative) at `qa/phase-2-spot-checks-{date}/spotcheck.json` (Axis 3 ADDITIVE-3) — enables v0.2 FINRA BrokerCheck programmatic cross-ref reuse

### 13.4 Axis 4 (GDPR opt-out Phase-2A scope) — CORROBORATE-with-additives

**Verdict: CORROBORATE** Phase 2A scope. **2 ADDITIVES absorbed in §6:**
- Pre-search opt-out check (Axis 4 ADDITIVE-1) — `crawl_linkedin_bronze` queries local opt-out cache (or Lusha `GET /v3/contacts/opt-outs` if available) BEFORE enriching; cost-discipline + GDPR double-win
- Explicit Phase 3 serving-tier opt_out_at filter AC (Axis 4 ADDITIVE-2) — `serving/employees.parquet` excludes opt-out rows; `serving/companies.parquet` excludes companies where all leadership opted out (or adjusts company score). Route to ws COO at Phase 3 TO authoring (defensive spec — implied-but-not-written is gap-class).

### 13.5 Unknown-unknowns (CVO Operating Doctrine §7 mandatory surfacing)

**UNK-1 (PII payload risk on silver employees.parquet):** silver schema (§3.3) at `email_revealed + phone_revealed + linkedin_url + full_name + bio_text + employer-context` = high-PII payload. PRD §3.5 SSE-S3 is account-boundary; not per-field PII. **Route ws CTO** PRD §3.6 KMS-upgrade-path candidate (CVO arch-brief §6.1 already documents upgrade-path; UNK-1 = empirical reason to invoke SOON not maybe). Disposition: separate CC to ws CTO for v0.4 PRD amendment consideration.

**UNK-2 (Lusha companyId drift at Phase 3 join):** silver captures both `company_slug` + `lusha_company_id` (§3.3) — good. **Route ws COO at Phase 3 TO authoring** to specify join-strategy precedence (slug-primary fallback to lusha_company_id?; or vice versa?) + drift-detection telemetry (e.g. log when slug + companyId resolve to different companies between runs).

**UNK-3 (tenure-as-decision-power may INVERT for transition signal):** `years_at_company_score` (§4.2 weight 0.25) heavily weighted assumes longer = more power. For FIND_INSURE specifically, AM build-out is often DRIVEN BY RECENT HIRES (new CFO + new VP Investments + new RIA-licensed advisor). Counter-intuitive: **low tenure + high seniority + recent Series-65 = STRONGEST transition signal.** **Action:** Phase 2A spot-check protocol (§5.7) extended to capture FN-rate for this class — specifically sample 5 employees with `years_at_company < 2yr` + `title_seniority >= 0.85` + `series_65_match OR series_66_match` and verify against rendered LinkedIn. If FN-rate elevated on this strata, re-weight `years_at_company_score` (potentially flip sign — bonus for low-tenure-high-seniority-license combo) at v0.1.1 config-bump.

**UNK-4 (cross-IMO exec overlap v0.2 enablement):** PRD §8 out-of-scope lists this v0.2. Phase 2A silver capture of `lusha_contact_id` as **globally unique** (not per-company scoped) makes v0.2 cross-IMO graph analysis trivial (`GROUP BY contact_id HAVING COUNT(DISTINCT company_id) > 1`). **Action:** confirm at bronze TO authoring that `lusha_contact_id` is preserved globally-unique (Lusha v3 IDs are stable per §7.1; verify nothing in bronze→silver pipeline de-dups across IMOs or re-scopes the ID). Cheap forward-compat win.

### 13.6 P1/P2 routing summary

| Item | Priority | Route |
|---|---|---|
| Axis 2 weight CONCERN | P1 | Andrew (Q2 ratification ask) |
| Axis 1 ADDITIVE (cert-struct-enum 4th path) | P2 | Self-absorbed §5.4; bronze + gold TO impl |
| Axis 3 ADDITIVES (stratify + cross-IMO cap + structured-JSON) | P2 | Self-absorbed §5.7; gold TO impl |
| Axis 4 ADDITIVE-1 (pre-search opt-out check) | P2 | Self-absorbed §6; bronze TO authoring |
| Axis 4 ADDITIVE-2 (Phase 3 serving-tier explicit filter AC) | P2 | ws COO at Phase 3 TO authoring |
| UNK-1 (PII / KMS upgrade) | UNK | ws CTO PRD §3.6 v0.4 candidate |
| UNK-2 (Lusha companyId drift) | UNK | ws COO at Phase 3 TO authoring |
| UNK-3 (tenure inversion for transition signal) | UNK | Self-absorbed §5.7 extension; v0.1.1 config-bump path |
| UNK-4 (lusha_contact_id global-unique) | UNK | bronze TO authoring confirmation |

### 13.7 No subsequent CVO consult required

Per LD-0094: explicit 4-shape rendered; no further CVO action expected unless DS~C or ws COO surfaces a new arch-fork. Next CVO Mode B fire on FIND_INSURE = Phase 1 RAVC2-Accept OR Phase 2A RAVC2-Accept (whichever first per cascade).

— 0.1.0_DS_MarketIntelligence~C 2026-05-27T~17:15Z (v0.3 amendment — CVO 4-axis ARCH-CORROBORATE absorbed; P1 Axis 2 routed Andrew; 3 P2 additives self-absorbed; 4 UNKs routed)
