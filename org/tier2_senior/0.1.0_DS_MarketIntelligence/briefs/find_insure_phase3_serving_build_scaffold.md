# FIND_INSURE Phase 3 — Consolidated Serving-Build Scaffold (v0.1)

**Author:** 0.1.0_DS_MarketIntelligence~E
**Date:** 2026-05-27
**Anchor:** MSTR SPAWN-WITH-DIRECTION 16:50Z (Fire #7 peak-priority variant) <- ws COO /allocation #3 brief `allocation_20260527T1647Z_find_insure_peak_priority.md` <- Andrew sovereign 16:46Z FIND_INSURE peak-priority
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §4 Phase 3 + §3.2 layout + §7 AC4/AC5
**Posture:** STANDING-PREP — Phase 3 design scaffold authored ahead of Phase 2 close + ADDITIVE-1 IR-named-individual gate (per CVO Mode B verdict `a5920688c` ADDITIVE-1)
**Lane:** ~E (Phase 3 prep) — parallel to ~A/~B (Phase 1 web), ~C (Phase 2A LinkedIn), ~D (Phase 2B Job-postings)

---

## 1. Scope

Design the three Phase 3 serving artifacts + join logic + relevance-scoring v0.1 weights, **pre-Phase-2-close** so the build_*_serving Lambdas can implement against a ratified design the moment Phase 2 Part A + Part B gold artifacts exist. Scaffold-not-implementation: schema + join + weights, no Lambda code at this cycle.

**In scope this brief:**
1. `companies.{json,parquet}` schema
2. `employees.{json,parquet}` schema
3. `scoring.{json,parquet}` schema (methodology + version stamp)
4. Join logic across the three upstream gold channels (web / linkedin / job-posting)
5. Relevance-scoring v0.1 weights (employee + company; PRD §9 Q2 draft proposal)
6. Build-orchestration sketch — Lambda decomposition + dispatch
7. ADDITIVE-1 IR-named-individual gate disposition for AC5
8. Open items routed back to ws COO + Andrew

**Out of scope this brief (deferred to Phase 3-impl TO):**
- Lambda code authoring (`build_companies_serving.py` etc.)
- Comp-graph registration for `data/find/imo/scripts/serving/*.py`
- Lusha Lookalikes / Signals enrichment overlay (PRD §4 Phase 3 sub-class; v0.2 candidate per PRD §8 + §11)
- Portal Phase 3b surface (PRD §4 Phase 3 deliverable 3)

---

## 2. Standing-for status

| Upstream | Status | Phase 3 dependency |
|---|---|---|
| Phase 1 gold (`gold/web-scrape/{slug}/{date}/`) | In-flight (~A parse-web + ~B score-web Lambda authoring per /allocation #3) | Companies table input (web-signal score + indicator-term hits) |
| Phase 2 Part A gold (`gold/linkedin-scrape/{slug}/{date}/`) | Pre-impl (~C scaffold in-flight; Lusha API key landed AE 0.7) | Employees table input (employee-level scoring + Series-license + tenure) + companies aggregate |
| Phase 2 Part B gold (`gold/job-posting-scrape/{slug}/{date}/`) | Pre-impl (~D scaffold in-flight; Stage Bα HAR pre-gate Q6 pending Andrew) | Companies table input (hiring-velocity + role-class distribution); secondary employees signal if a posting names a hiring manager |
| ADDITIVE-1 (IR-named-individual pre-Phase-3 gate) | Pending — names a specific IR-team consumer for AC5 RAVC2 sign-off | Phase 3 RAVC2 close: AC5 cannot fire without a named human |
| ADDITIVE-2 (timing) | VACATED — Andrew sovereign override 16:40Z (CVO ADDITIVE-2 vacated; AE 0.7 firing .001+.003 NOW) | n/a |

Phase 3 implementation does **not start** until Phase 2 Part A gold lands for ≥1 IMO end-to-end. Scaffold ships now to compress that downstream cycle.

---

## 3. `serving/companies.{json,parquet}` — schema

**Cardinality:** 1 row per IMO from the Phase 0 source-list (~99). Re-run semantic: **overwrite-in-place** per PRD §3.2.

**Key:** `company_slug` (deterministic slugifier output of `company_name` via `data/find/imo/scripts/_util/slugify.py` — single source of slug-truth per PRD §3.3).

### 3.1 Field list

| Field | Type | Source | Notes |
|---|---|---|---|
| `company_slug` | str | Phase 0 source-list + `_util/slugify.py` | Primary key; join axis across all gold channels |
| `company_name` | str | Phase 0 source-list `_meta/source-list-{date}.json` | Canonical name as listed at safemoneybroadcasting |
| `website_url` | str \| null | Phase 0 source-list | ~93/99 carry full https URL; ~6/99 bare domain (per extract_source_list.py:13-15 empirical finding) |
| `source_position` | int | Phase 0 source-list | Position in source page (1-99) — lineage |
| `phase1_score` | float | `gold/web-scrape/{slug}/{date}/` (Phase 1 deliverable 3) | Asset-mgmt-transition web-signal score from ~B score-web Lambda |
| `phase1_indicator_hits` | int | `gold/web-scrape/{slug}/{date}/` | Count of indicator-term matches (RIA, Series 65/66/7/24, Form ADV, AUM, TAMP, IAR, fiduciary, model portfolio, SMA, etc.; full taxonomy at `config/term-taxonomy-{version}.json`) |
| `phase1_indicator_breakdown` | dict[term_class -> int] | `gold/web-scrape/{slug}/{date}/` | Per-term-class hit counts (denormalized for IR-team scan) |
| `phase1_page_count` | int | `gold/web-scrape/{slug}/{date}/` | Pages crawled (denominator for hit-density) |
| `phase1_eligible_for_phase2` | bool | derived (top-quintile-by-phase1_score OR `phase1_indicator_hits >= 1` on Series-license terms; per PRD §4 Phase 2 default proposal) | Pre-Phase-2 cut signal; Andrew gate Q1 may override |
| `phase2a_employee_count_surfaced` | int \| null | aggregate from `gold/linkedin-scrape/{slug}/{date}/` | NULL if not in Phase 2 subset |
| `phase2a_series_licensed_count` | int \| null | aggregate from `gold/linkedin-scrape/{slug}/{date}/` | Count of leadership employees with ≥1 Series license detected |
| `phase2a_top_employee_score` | float \| null | max(employee_score) over employees in `gold/linkedin-scrape` for this IMO | Used in company score aggregation |
| `phase2b_investment_keyword_hits` | int \| null | `gold/job-posting-scrape/{slug}/{date}/` | Count of postings matching investment-keyword taxonomy |
| `phase2b_series_licensure_required_count` | int \| null | `gold/job-posting-scrape/{slug}/{date}/` | Count of postings explicitly requiring/preferring Series 63/65/66/7/24/6/79/82 |
| `phase2b_hiring_velocity_90d` | int \| null | `gold/job-posting-scrape/{slug}/{date}/` | Count of investment-class / corp-finance / tech postings in trailing 90 days |
| `phase2b_role_class_distribution` | dict[role_class -> int] \| null | `gold/job-posting-scrape/{slug}/{date}/` | Per-role-class posting counts (investment-professional / corporate-finance / technology / etc.) |
| `company_score` | float | derived (see §5) | Final ranked-output score for IR team |
| `scoring_version` | str | `config/scoring-weights-{version}.json` | Joins to `scoring.{json,parquet}` for methodology cite-back |
| `pipeline_run_date` | str (YYYY-MM-DD UTC) | run input | Date of the Phase 1 + Phase 2 inputs that fed this row |
| `pipeline_run_id` | str | run input | Lineage to `telemetry/serving-build/{date}/{run-id}.ndjson` |

### 3.2 Null-handling discipline

- Phase 2A/Phase 2B fields are NULL (not 0) for IMOs not in the Phase-2 subset — per CLAUDE.md Rule 17 (silver = clean shape, gold = business judgment; serving is gold-consumer, NULL preserves "absent" semantic for IR-team scan). NULL ≠ "zero leadership found"; NULL = "Phase 2 did not run".
- `phase2b_*` NULL also covers the case where Phase 2 subset includes the IMO but Stage Bα/Bβ surfaced no usable job-board endpoints for that IMO (per-IMO Bα-feasibility verdict at `config/board-endpoint-manifest-{date}.json`).
- `company_score` is **always non-null** (computed even with NULL Phase-2 inputs; see §5 missing-input handling).

---

## 4. `serving/employees.{json,parquet}` — schema

**Cardinality:** 1 row per leadership-class employee at any Phase-2-subset IMO with detectable LinkedIn presence. Expected size: ~100 IMOs × ~25% Phase-2-subset × ~10 leadership employees ≈ 250 rows v0.1.

**Key:** composite (`company_slug`, `employee_id`) where `employee_id` = Lusha `contactId` if available, else `slugify(full_name + "_" + company_slug)`.

### 4.1 Field list

| Field | Type | Source | Notes |
|---|---|---|---|
| `company_slug` | str | join key | Joins to `companies.company_slug` |
| `employee_id` | str | Lusha `contactId` OR derived slug | Stability across re-runs; lookups |
| `full_name` | str | `silver/linkedin-scrape` | From Lusha enrich |
| `title` | str | `silver/linkedin-scrape` | Current title at this IMO |
| `tenure_at_company_years` | float \| null | `silver/linkedin-scrape` | Derived from `years_at_company` Lusha field; NULL if Lusha did not surface |
| `prior_titles` | list[str] | `silver/linkedin-scrape` | Up to last 3 prior roles |
| `location` | str \| null | `silver/linkedin-scrape` | City + state from Lusha |
| `linkedin_url` | str \| null | `silver/linkedin-scrape` | Direct LinkedIn profile URL |
| `email` | str \| null | `silver/linkedin-scrape` (Lusha reveal) | Only present if cost-budget allowed Enrich reveal for this employee |
| `phone` | str \| null | `silver/linkedin-scrape` (Lusha reveal) | Same gate as email |
| `series_licenses_detected` | list[str] | `gold/linkedin-scrape` (DS lane detection logic from bio/about text) | e.g. `["7", "65", "66"]` — bare-number list; full code mapping at `config/series-license-taxonomy-{version}.json` |
| `title_seniority_class` | enum | `gold/linkedin-scrape` | One of: `c-suite` / `evp_svp` / `vp_director` / `manager` / `ic` / `other` |
| `title_keyword_matches` | list[str] | `gold/linkedin-scrape` | Investment / Wealth / Advisory / Asset Management hits in the title string |
| `employee_score` | float | derived (see §5) | Per-employee relevance score |
| `phase2b_named_in_job_postings` | bool | derived from `gold/job-posting-scrape/{slug}/{date}/` | TRUE if any Phase 2B posting names this person as hiring manager (secondary signal) |
| `scoring_version` | str | `config/scoring-weights-{version}.json` | Methodology join |
| `pipeline_run_date` | str | run input | Same value as the corresponding companies row |
| `pipeline_run_id` | str | run input | Lineage |

### 4.2 Null-handling discipline

- `email` / `phone` / `tenure_at_company_years` are NULL when Lusha didn't return them OR cost-budget skipped the Enrich call. Not zero-substituted.
- `series_licenses_detected` is `[]` (empty list) when detection ran and found nothing; only NULL if detection didn't run (shouldn't happen for any row that exists).
- Same NULL-preservation discipline as §3.2.

---

## 5. `serving/scoring.{json,parquet}` — schema + methodology

**Cardinality:** 1 row per scoring methodology version (current pinned version + audit-trail rows in `serving/_history/{date}/scoring.{json,parquet}` per PRD §3.2 Q-B ruling).

**Key:** `scoring_version`.

### 5.1 Field list

| Field | Type | Notes |
|---|---|---|
| `scoring_version` | str | Semver-like (e.g. `v0.1`, `v0.2`) |
| `effective_date` | str (YYYY-MM-DD UTC) | When this version started producing serving rows |
| `methodology_notes` | str | Free-text — what changed vs prior, why |
| `employee_score_formula` | str | Symbolic; see §5.2 |
| `employee_score_weights` | dict[str -> float] | Numeric weights — pluggable per version |
| `company_score_formula` | str | Symbolic; see §5.3 |
| `company_score_weights` | dict[str -> float] | Numeric weights |
| `title_seniority_class_weights` | dict[enum -> float] | Maps `c-suite` -> 1.0, `evp_svp` -> 0.85, etc. |
| `series_license_weights` | dict[str -> float] | Maps `7` -> 0.30, `24` -> 0.30, `65` -> 0.40, `66` -> 0.40, `63` -> 0.10, `6` -> 0.05, etc. |
| `title_keyword_set` | list[str] | The keyword list used for `title_keyword_match` boolean |
| `pipeline_run_id_last` | str | Last pipeline run that used this version (lineage) |

### 5.2 Employee scoring formula (v0.1 draft, per PRD §9 Q2)

```
employee_score
  = (years_at_company_normalized * w_tenure)
  + (title_seniority_class_weight * w_seniority)
  + (series_license_count_weighted * w_series)
  + (title_keyword_match_indicator * w_keyword)

where:
  years_at_company_normalized = min(years_at_company, 15) / 15         # caps at 15y; NULL -> 0.5 neutral
  title_seniority_class_weight = series.title_seniority_class_weights[title_seniority_class]
  series_license_count_weighted = sum(series_license_weights[s] for s in series_licenses_detected)
  title_keyword_match_indicator = 1.0 if any(kw.lower() in title.lower() for kw in title_keyword_set) else 0.0
```

**Draft weights (v0.1):**

```yaml
w_tenure:   0.25
w_seniority: 0.25
w_series:   0.30
w_keyword:  0.20
title_seniority_class_weights:
  c-suite:     1.00
  evp_svp:     0.85
  vp_director: 0.65
  manager:     0.40
  ic:          0.15
  other:       0.10
series_license_weights:
  "7":   0.30   # General Securities Rep — broad
  "24":  0.30   # General Securities Principal
  "65":  0.40   # Uniform Investment Adviser — RIA-relevant
  "66":  0.40   # Uniform Combined State Law — RIA-relevant
  "63":  0.10   # Uniform Securities Agent — broker only
  "6":   0.05   # Investment Company / Variable Contracts — narrow
  "79":  0.20   # Investment Banking
  "82":  0.20   # Private Securities
  "51":  0.05   # Municipal Fund Sec Limited Principal
  "52":  0.05
  "53":  0.10
  "22":  0.05
  "26":  0.10
```

**Why these weights (rationale per Andrew framing):**
- 65/66 weighted highest — direct RIA-axis licenses; an IMO leader holding 65/66 is **already operating in or licensed for** the asset-management surface we're trying to discover.
- 7/24 next — broad securities licenses indicate general capability + principal authority but don't bind to RIA work specifically.
- 79/82 mid — investment-banking-class; correlates with growth / M&A signal (per PRD §4 Phase 2 Part B Andrew "begets m&a/growth activity" framing).
- 63/6 low — broker-only / narrow-product licenses; weakly correlated with asset-mgmt-transition signal.

### 5.3 Company scoring formula (v0.1 draft)

```
company_score
  = (phase1_score_normalized            * w_phase1_signal)
  + (max_employee_score_in_company      * w_top_employee)
  + (series_licensed_count_normalized   * w_series_density)
  + (phase2b_hiring_velocity_normalized * w_hiring_signal)
  + (phase2b_investment_keyword_normalized * w_job_keyword)

where:
  phase1_score_normalized = phase1_score (already 0-1 from ~B score-web; if not, min(phase1_score, score_cap) / score_cap)
  max_employee_score_in_company = max(employee_score) over employees in company OR 0 if NULL
  series_licensed_count_normalized = min(phase2a_series_licensed_count, 10) / 10  # caps at 10
  phase2b_hiring_velocity_normalized = min(phase2b_hiring_velocity_90d, 20) / 20  # caps at 20
  phase2b_investment_keyword_normalized = min(phase2b_investment_keyword_hits, 50) / 50
```

**Draft weights (v0.1):**

```yaml
w_phase1_signal:   0.30   # web-signal — present-state asset-mgmt indication
w_top_employee:    0.25   # leadership has the licenses + tenure to execute
w_series_density:  0.20   # how many leaders hold the licenses (not just one)
w_hiring_signal:   0.15   # forward-looking buildout signal
w_job_keyword:     0.10   # current job-postings naming investment-class roles
```

**Missing-input handling (NULL Phase-2 inputs):**
- If `phase2a_*` NULL (not in Phase 2 subset): `max_employee_score_in_company` and `series_licensed_count_normalized` both contribute 0; **company_score still computes** from Phase-1-only signal. This lets the Phase 3 table rank both subset + non-subset IMOs on a coherent scale, with non-subset capped at `w_phase1_signal * 1.0 = 0.30` max.
- If `phase2b_*` NULL: same treatment — hiring + job-keyword contribute 0.
- **Cap-implication:** non-Phase-2-subset IMOs cannot exceed 0.30; Phase-2-subset IMOs can reach 1.00. This is intentional — it surfaces the subset cut visually in the company_score distribution and signals to the IR team which IMOs are "limited-confidence" because Phase 2 didn't run on them.

### 5.4 Hand-tunability + v0.1-vs-v0.2 strategy

Weights live at `config/scoring-weights-v0.1.json` (per PRD §3.2 + §3.5). The build_scoring_serving Lambda reads the pinned version at run time; bumping `v0.1` -> `v0.2` is a config file commit + Lambda re-run (no Lambda code change). Post-AC5 IR-team-review-pass feedback feeds directly into a v0.2 weights revision; the `serving/_history/{date}/scoring.{json,parquet}` archive (per Q-B) preserves the v0.1 audit trail.

---

## 6. Join logic (build orchestration sketch)

### 6.1 Lambda decomposition

Per PRD §4 Phase 3 deliverable 1, three Lambdas:

| Lambda | Reads | Writes | Frequency |
|---|---|---|---|
| `build_companies_serving` | `serving/_meta/source-list-{date}.json` + `gold/web-scrape/*/{date}/` + `gold/linkedin-scrape/*/{date}/` (aggregate) + `gold/job-posting-scrape/*/{date}/` (aggregate) + `config/scoring-weights-{version}.json` | `serving/companies.{json,parquet}` + `serving/_meta/pipeline-run-{date}.json` | Per pipeline-run |
| `build_employees_serving` | `gold/linkedin-scrape/*/{date}/` (employee rows) + `gold/job-posting-scrape/*/{date}/` (for `phase2b_named_in_job_postings` join) + `config/scoring-weights-{version}.json` | `serving/employees.{json,parquet}` | Per pipeline-run |
| `build_scoring_serving` | `config/scoring-weights-{version}.json` | `serving/scoring.{json,parquet}` + `serving/_history/{date}/scoring.{json,parquet}` | Per scoring-version bump (rarely) |

`build_scoring_serving` is **first** in execution order — produces the methodology row that `build_companies_serving` + `build_employees_serving` cite via `scoring_version`. Dispatch sequence:

```
build_scoring_serving (writes scoring.{json,parquet} + _history/{date}/scoring.{json,parquet})
  -> build_employees_serving (writes employees.{json,parquet})
       -> build_companies_serving (writes companies.{json,parquet}, joins employees aggregate)
            -> _meta/pipeline-run-{date}.json (run summary)
```

`build_companies_serving` depends on `build_employees_serving` because the company-level `phase2a_top_employee_score` + `phase2a_series_licensed_count` are aggregates over employees — cheaper to compute once and join than to re-scan gold/linkedin twice.

### 6.2 Cross-IMO join key discipline

All three Lambdas share `company_slug` as the join axis. `_util/slugify.py` is the single source of slug-truth per PRD §3.3 — all Phase 1/2/3 Lambdas import it. Any slug mismatch (e.g. extractor produces `wlth-rx` but Phase 1 crawler stored under `wlthrx`) silently drops the IMO from the serving table — the build_companies_serving Lambda emits a warning per missing-gold-for-source-list-IMO to `telemetry/build-companies-serving/{date}/{run-id}.ndjson`.

### 6.3 Re-run semantics

Per PRD §3.2:
- `serving/companies` + `serving/employees` + `serving/scoring` **overwrite-in-place**.
- `serving/_history/{date}/scoring.{json,parquet}` **append-by-date** (scoring methodology audit trail).
- `serving/_meta/pipeline-run-{date}.json` **append-by-date**.

### 6.4 IAM coverage

`find-insure-lambda-role` per PRD §3.5 already grants:
- `s3:GetObject` + `s3:ListBucket` across whole bucket (Phase 3 cross-corp scan)
- `s3:PutObject` to `serving/*`
- `s3:DeleteObject` **NOT** allowed on `serving/*` (delete-restricted per §3.5)

Therefore `build_*_serving` uses overwrite-via-PutObject (versioning catches accidental clobber per §3.1). No IAM amendment needed for Phase 3.

---

## 7. ADDITIVE-1 disposition (IR-named-individual pre-Phase-3 gate)

Per CVO Mode B PRE-EXECUTION verdict `a5920688c` ADDITIVE-1: AC5 RAVC2 close cannot fire without a **named** IR-team consumer who agrees to review the Phase 3 tables and produce the CLOSE-COMPLETE / re-open verdict.

**Phase 3 scaffold treats this as a structural blocker on AC5, NOT on AC4** — the build_*_serving Lambdas can ship + write coherent tables (AC4) before the IR-team-individual is named; AC5 cannot close until that gate clears.

**Recommended timing:** route the IR-team-individual ask to Andrew **at Phase 2 dispatch** (concurrent with Q1 subset-criteria gate), not at Phase 3 RAVC2 — gives the named individual time to context-load before reviewing the tables.

**Phase 3 deliverable cuts (post-ADDITIVE-1):**
- Phase 3 ship-ready ("AC4-complete"): 3 serving artifacts written end-to-end + sample QA review.
- Phase 3 closed ("AC5-complete"): IR-named-individual verdict landed.

---

## 8. Open items routed to ws COO / Andrew

| # | Item | Route to | Phase gate |
|---|---|---|---|
| O-1 | Q1 — Phase 1 -> Phase 2 subset cut criteria (top quintile by phase1_score + Series-license-mention default; Andrew override?) | Andrew via ws COO | Pre-Phase-2 dispatch |
| O-2 | Q2 — employee + company scoring weights — ratify v0.1 draft (§5.2 + §5.3) or revise pre-impl? | Andrew + IR team via ws COO | Pre-Phase-3 dispatch (so build_scoring_serving has a ratified config) |
| O-3 | Q3 — output format (JSON + Parquet default; CSV-for-Excel add-on?) | IR team via ws COO | Phase 3 impl |
| O-4 | ADDITIVE-1 — name the IR-team-individual consumer for AC5 sign-off | Andrew via ws COO | Pre-Phase-3 RAVC2 close (recommended at Phase 2 dispatch per §7) |
| O-5 | `series_license_weights` v0.1 draft (§5.2) — DS proposes Series 65/66 highest, 7/24 next, 79/82 mid, 63/6 low. Ratify or revise? | DS + Andrew + IR team via ws COO | Pre-Phase-3 dispatch |
| O-6 | `title_seniority_class` taxonomy (§4.1) — DS proposes `c-suite` / `evp_svp` / `vp_director` / `manager` / `ic` / `other`. Add `founder` / `owner` as distinct classes (PRD §4 Phase 2A names them as leadership-role title patterns)? | DS via ws COO | Pre-Phase-3 dispatch |
| O-7 | Lusha Lookalikes + Signals overlay (PRD §4 Phase 3 "+ Lusha Lookalikes / Signals enrichment overlay" sub-class) — confirm v0.1 deferred (out of scope per §1) or include? | Andrew via ws COO | Phase 3 v0.1 vs v0.2 cut |
| O-8 | `serving/_meta/pipeline-run-{date}.json` shape — DS proposes `{lambda_set: [...], started_at, ended_at, imo_count, signal_totals: {...}, telemetry_run_ids: [...]}`. Ratify? | DS via ws COO | Phase 3 impl |

---

## 9. RAVC2 chain plan (post-scaffold)

**This brief = SCAFFOLD-DESIGN deliverable, not Phase 3 implementation.** RAVC2 sequencing post-this-ship:

1. **Scaffold RAVC2 (this brief):** ~E ships brief -> ws COO RAVC2-ACCEPT acknowledges design banked + queues O-1 through O-8 routings -> ws CVO `/spot-check` cycle catches it (no implementation yet, so /verify-channel does not fire).
2. **Pre-Phase-3-impl gate:** ws COO collects O-1 through O-8 dispositions; once O-2 + O-5 + O-6 + ADDITIVE-1 (O-4) are answered, ws CTO authors Phase 3 impl TO triad (.007 build_companies_serving + .008 build_employees_serving + .009 build_scoring_serving) referencing this scaffold as the design baseline.
3. **Phase 3 impl RAVC2 (per-Lambda):** ~E (or successor DS lane per /allocation routing) ships each Lambda; ws CVO `/verify-channel` 4-check pattern (EXISTS/FRESH/SCALED/NOT-FROZEN) on serving artifacts post-end-to-end-run.
4. **Phase 3 close (AC4):** All three serving artifacts exist + sample QA review confirms data shape matches schema + scoring runs without exception.
5. **Phase 3 close (AC5):** IR-named-individual verdict landed; project closes or re-opens to v0.2 scoring iteration.

---

## 10. Lineage + cross-refs

- PRD: `docs/architecture/FIND_INSURE.md` v0.3 — §3.2 layout, §3.4 lifecycle, §3.5 IAM, §4 Phase 3, §7 AC4/AC5, §9 Q1-Q7, §9.1 Q-A/B/C/D
- CVO architectural brief: `org/tier1_exec/3.0.0_SA_CVO/responses/20260527T1620Z_to_1.0.0_SA_CTO_opal_data_imo_bucket_architecture_brief.md` `8fb6f7d94`
- CVO Mode B PRE-EXECUTION verdict (ADDITIVE-1 origin): `a5920688c`
- COO /allocation #3: `org/tier1_exec/2.0.0_SA_COO/briefs/allocation_20260527T1647Z_find_insure_peak_priority.md`
- Source-list extractor (Phase 0 sibling deliverable, shipped): `data/find/imo/scripts/_meta/extract_source_list.py` `9aaa1459d` (relocate to `data/find/imo/` post-COO `8f03385aa`)
- Slugify shared util: `data/find/imo/scripts/_util/slugify.py` (Phase 0 sub-deliverable per CVO §3.3)
- Lusha API v3 reference: `docs/reference/lusha-api-v3.md`
- Andrew sovereign 16:46Z FIND_INSURE peak-priority directive (MSTR spawn-msg anchor)

— 0.1.0_DS_MarketIntelligence~E 2026-05-27T~17:00Z
