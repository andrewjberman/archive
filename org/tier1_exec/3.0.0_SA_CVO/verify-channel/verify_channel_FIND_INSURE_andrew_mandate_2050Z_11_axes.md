---
cycle: /verify-channel Mode B comprehensive — Andrew sovereign 2050Z mandate (11 axes), Class-1 immediate-fire #3 [VERIFY-CHANNEL-NOW]-equivalent via ws CTO routing brief
verdict: MISALIGNED (axis-aggregate; C1 mechanical-untruth + W3/P2/W1-threshold + Rule 17 gaps surfaced)
project: FIND_INSURE
trigger_brief: docs/briefs/find-insure-cvo-validation-mandate-andrew-20260527T2050Z.md
window_baseline: Phase 1 in-flight; 3/99 IMO universe-run; first project-level comprehensive empirical-read
constitution_axis: NULL — drift-review subscan deferred (mandate is axis-empirical not constitution-drift; will re-fire at next regular comprehensive Mode B trigger)
---

**archetype:** VALIDATE

# /verify-channel FIND_INSURE — Andrew sovereign 11-axis validation mandate

CVO-independent empirical verification per Andrew sovereign 2026-05-27T~20:50Z dispatch via ws CTO. Each axis cites concrete S3 paths / file paths / counts / samples / verbatim config. No narrative-only assertions. Lift grades per [[feedback_lift_grading_framework_cvo_judgment]].

## TL;DR

**Aggregate verdict: MISALIGNED.** Phase 1 pipeline is methodologically substantive on the 2-IMO discriminating sample (Avantax POSITIVE / 1st-Atlantic NEGATIVE) — NOT noise. The mechanical failure is COVERAGE: only **3/99 = 3% of the IMO universe has been scraped**, and there is **no consolidated serving/scoring table** to rank against. Per Andrew's anti-pattern guard, the methodology is not "throwing noise around" — but Phase 1 cannot honestly claim RAVC2-Accept until the 99-IMO universe-run + serving table land.

Two REPAIR-AMENDMENT-AUTHORIZED triggers fired this cycle (see §REPAIR-AMENDMENT).

Per-axis grade summary:

| Axis | Grade | Headline |
|---|---|---|
| C1 — 99/99 attestation | **F** | 3/99 in S3 (3% coverage); 96 IMOs never crawled |
| C2 — Crawl outcome distribution | **D** | 3-IMO sample: 2 SUCCESS + 1 EMPTY-BODY (Bright Data TLS cert mismatch on carlostenson.com); 33% empty-body class on n=3 FAR exceeds 5-10% AC-T2 PRD threshold but n too small to fire |
| B1 — Bronze field inventory | **B** | Dual-file pattern (`.html` + `.meta.json` sidecar); meta schema 14 fields; readable + populated |
| S1 — Silver field inventory + Rule-17 check | **C** | 16-field success schema rich; **Rule 17 violation: 5 bronze meta fields dropped in silver** (http_headers, crawl_depth, robots_txt_compliance, scheme_fallback, tls_fail_original) |
| G1 — Gold structured layout | **B+** | 12-field gold schema; rich per-match evidence trails with context_snippet + location_class; decision-useful |
| P1 — Parsing yield | **B+** | Silver extraction rich on SUCCESS pages (Avantax sample body_text=6508 chars, 6-level headings, link_graph, structured_blocks, structured_data) |
| P2 — Empirical TP/FP discrimination | **INCOMPLETE** | n=2 valid sample (Avantax 100 TP / Atlantic 0 TN); CANNOT deliver 10-IMO discrimination without C1 universe-run; **CONDITIONAL on C1** |
| W1 — Term taxonomy criterion | **C+** | Keyword + class-weighted + log-dampened + location-weighted; **threshold semantics for has-WM-program vs adjacent vs absent NOT stated** in config or PRD |
| W2 — Scoring weights traceability | **C** | Term-class weights have rationale ([0.55-1.0] range, class-tiered); employee/company score weights lack explicit Andrew-direction provenance |
| W3 — Ranking output | **INCOMPLETE** | **NO consolidated `serving/scoring.json`** exists; 3 per-IMO `gold/score.json` files only; **CONDITIONAL on C1 + Phase 1 close + consolidation TO** |
| M1 — Noise vs signal aggregate | **CONDITIONAL — METHODOLOGICALLY-MEANINGFUL / EMPIRICALLY-INCOMPLETE** | NOT noise; methodology substantive on valid 2-IMO sample. Cannot answer "IR analyst agrees with top-20" because top-20 does not yet exist. Re-grade post-C1-resolution. |

---

## C1 — 99/99 crawl attestation

**Verdict: F (3/99 = 3.0% coverage)**

S3 evidence:
```
aws s3 ls s3://opal-data-imo/corp/
  PRE 1st-atlantic-insurance-group/
  PRE avantax-wealth-management/
  PRE carl-ostenson/
  .keep (0 bytes)
```

Source-list universe size: `aws s3 cp s3://opal-data-imo/serving/_meta/source-list-2026-05-27.json -` confirms 99 IMOs (`imo_count: 99`; first entry `{'company_name': '1st Atlantic Insurance Group', 'website_url': 'https://1statlantic.com', 'source_position': 1}`).

**Mechanical-untruth-to-reality:** PRD docs/architecture/FIND_INSURE.md §1 mandate text declares "Phase 1 web-scrape end-to-end across full 100-IMO universe with asset-management indicator-term scoring." Current state at 2026-05-27T~20:55Z = 3 IMOs scraped + 96 IMOs never crawled. AC2 (project-level) NOT empirically satisfied.

The 3 IMOs present are the same 3-IMO test set that prior cycle 4 + cycle 5 spot-checks + 1d28ffcc9 META-VERIFY operated on (Avantax + 1st-Atlantic + Carl-Ostenson). No additional IMOs scraped in the 90min post-respawn window.

96 IMOs awaiting first crawl. This is the C1 finding. REPAIR-AMENDMENT-AUTHORIZED (a) trigger (see §REPAIR-AMENDMENT).

---

## C2 — Crawl outcome distribution

**Verdict: D (n=3 sample too small; preliminary signal: 33% EMPTY-BODY exceeds AC-T2 PRD threshold)**

Per-IMO outcome from S3 evidence:

| IMO | bronze HTML pages | bronze meta_json | silver records | silver blocked_reason | outcome class |
|---|---|---|---|---|---|
| avantax-wealth-management | 5 (~30KB each) | 5 | 5 SUCCESS | null | **SUCCESS** |
| 1st-atlantic-insurance-group | 5 (~25KB each) | 5 | 5 SUCCESS (true-negative on AM terms) | null | **SUCCESS** |
| carl-ostenson | 0 .html | 1 (.meta.json only) | 1 BLOCKED | "empty-body" | **EMPTY-BODY** |

Carl-Ostenson bronze meta inspect (`aws s3 cp s3://opal-data-imo/corp/carl-ostenson/bronze/web-scrape/2026-05-27/7fe8d70daaa829f2.meta.json -`):
```json
{"url": "https://carlostenson.com",
 "http_status": 200,
 "http_headers": {"x-brd-error": "Navigation failed: The SSL/TLS certificate presented by the server doesn't match the domain name being accessed",
                  "x-brd-error-code": "net_err_cert_common_name_invalid",
                  "x-brd-status-code": "502"},
 "blocked_reason": "empty-body"}
```

Bright Data crawler hit a TLS cert common-name mismatch on carlostenson.com → HTTP 502 → body_text=null → silver `blocked_reason: empty-body`.

Distribution: 2 SUCCESS / 1 EMPTY-BODY / 0 BLOCKED-anti-bot / 0 TIMEOUT / 0 ERROR on n=3. Empty-body rate = 33%.

**PRD v0.6 AC-T2 threshold:** if EMPTY-BODY class > 5-10% across the 99-IMO universe → ship v0.3.0 scraping_browser1 escape-valve Lambda. **Cannot fire AC-T2 on n=3** — not statistically valid. AC-T2 trigger evaluation gates on C1 universe-run.

Telemetry-AC AC-T1 (crawl-coverage telemetry) is also not yet implemented at the silver-pipeline level — there's no aggregated 99-IMO crawl-outcome distribution table in S3, only per-IMO sample.

---

## B1 — Bronze field inventory

**Verdict: B**

Bronze object pair pattern (per `data/find/imo/scripts/bronze/crawl_web_bronze.py` design):
- `corp/{slug}/web-scrape/bronze/{YYYY-MM-DD}/{url_hash}.html` — raw HTML body
- `corp/{slug}/web-scrape/bronze/{YYYY-MM-DD}/{url_hash}.meta.json` — crawler metadata sidecar

Bronze meta.json sample (carl-ostenson, 723 bytes; same schema also seen in Avantax samples):

| Field | dtype | Sample value | Null-rate (n=3 IMOs sampled) |
|---|---|---|---|
| url | str | https://carlostenson.com | 0% |
| url_hash | str | 7fe8d70daaa829f2 (16 hex) | 0% |
| content_hash | str/null | null (empty-body) or 16-hex (success) | 33% (empty-body) |
| fetched_at | str ISO8601 UTC | 2026-05-27T18:24:17Z | 0% |
| http_status | int | 200 | 0% |
| content_type | str/null | null (empty-body) or "text/html..." (success) | 33% |
| etag | str/null | null in sampled records | 100% in sample |
| last_modified | str/null | null in sampled records | 100% in sample |
| http_headers | dict | {Server, Date, Transfer-Encoding, ..., x-brd-error*} | 0% |
| crawl_depth | int | 0 | 0% |
| robots_txt_compliance | bool | true | 0% |
| blocked_reason | str/null | "empty-body" (carl) or null (success) | 33% non-null |
| scheme_fallback | str/null | null | 100% null in sample |
| tls_fail_original | bool | false | 0% |

No "intent-stated-but-not-populated" column-gap class observed in bronze meta schema. Bronze HTML body is the primary content; bronze meta is the crawler-process metadata.

---

## S1 — Silver field inventory + Rule 17 preserve-all check

**Verdict: C** (16-field rich success schema; Rule 17 sub-finding fired)

Silver SUCCESS schema (from `/tmp/avantax_silver.json` sample, `data/find/imo/scripts/silver/parse_web_silver.py:291` build_silver_record):

| Field | dtype | Sample shape |
|---|---|---|
| url | str | 74 chars |
| url_hash | str | 16 hex |
| fetched_at | str | ISO8601 |
| http_status | int | 200 |
| content_type | str | "text/html; charset=..." |
| etag | str/null | null in sample |
| last_modified | str/null | null in sample |
| bronze_key | str | 81 chars S3 key |
| content_hash | str | 16 hex |
| title | str | 55 chars |
| meta_tags | dict | 8 keys (description, robots, og:type, og:url, og:title, og:image, Generator, MobileOptimized) |
| headings | dict | h1-h6 lists |
| body_text | str | 6508 chars (Avantax sample) |
| link_graph | dict | internal_links + external_links |
| structured_blocks | dict | addresses + emails + phones |
| structured_data | dict | json_ld list |

Silver BLOCKED schema (from `/tmp/ostenson_silver_sample.json`, `parse_web_silver.py:344` build_blocked_record):

| Field | dtype | Sample |
|---|---|---|
| url | str | https://carlostenson.com |
| url_hash | str | 7fe8d70daaa829f2 |
| fetched_at | str | 2026-05-27T18:24:17Z |
| http_status | int | 200 |
| content_type | null | null |
| bronze_key | null | null |
| blocked_reason | str | "empty-body" |
| page_text | null | null |
| body_text | null | null |

**RULE 17 SUB-FINDING (CLAUDE.md Rule 17 violation, alignment-substance class):**

Silver schema (success path) DOES NOT preserve the following 5 bronze meta fields:
- `http_headers` — Bright Data crawler response headers (diagnostic + anti-bot debug)
- `crawl_depth` — crawler tree depth at fetch (audit)
- `robots_txt_compliance` — bool (audit)
- `scheme_fallback` — null/str (https→http fallback flag)
- `tls_fail_original` — bool (TLS error flag)

Per CLAUDE.md Rule 17: "Silver tier conversions perform ONLY deduplication + type standardization. NEVER slim fields. Anything requiring judgment about *what fields matter* belongs in gold tier." The silver script's `build_silver_record` makes such a judgment by NOT carrying these 5 fields forward. The fields are crawler-process diagnostic — they would be load-bearing for debugging "why did silver land in BLOCKED class" (carl-ostenson empty-body root-cause needed bronze meta.json `x-brd-error*` field inspection — exactly the fields silver drops). This is the diagnostic-loss class Rule 17 exists to prevent.

REPAIR-AMENDMENT-AUTHORIZED (b) trigger (see §REPAIR-AMENDMENT).

---

## G1 — Gold structured layout

**Verdict: B+**

Gold schema (from all 3 `/gold/web-scrape/2026-05-27/score.json` files):

```
company_slug: str (the IMO slug)
run_date: str (YYYY-MM-DD)
taxonomy_version: str ("v1")
term_matches: list[dict] — per-match record
  {term, class, page_url, context_snippet (~80 chars), position (int), location_class}
term_match_count: int
term_class_distribution: dict[class_name → int]
page_count_scanned: int
page_count_with_matches: int
rollup_raw: float
class_diversity_multiplier: float (1.0 to 1.5)
rollup_score: int (0 to 100, capped)
scored_at: str (ISO8601 UTC)
```

Decision-usefulness: each match carries `context_snippet` (80-char window around the term hit) + `position` (char offset) + `location_class` (title / og_title / h1 / h2 / body / etc.). This IS decision-useful — an IR analyst inspecting the top-N can read the snippets and validate the rank. NOT just a black-box score.

Avantax full evidence (`/tmp/avantax_gold.json`):
- `term_match_count: 171`
- `term_class_distribution: {business-model: 110, regulatory-license: 50, product: 3, org-structure: 4, certification: 4}`
- `page_count_scanned: 5`, `page_count_with_matches: 5`
- `class_diversity_multiplier: 1.4` (5 classes with matches → 1 + 0.1*4, capped at 1.5)
- `rollup_raw: 28.1349`
- `rollup_score: 100` (capped from `min(100, round(28.1349 * 1.4 * 4))` = `min(100, round(157.555))` = 100)

Top match samples (term + class + context_snippet excerpt):
1. `wealth management` (business-model) — `"Licensed Tax Professionals - Avantax Wealth Management"` — location_class=title
2. `FINRA` (regulatory-license) — `"members FINRA / SIPC ; Cetera Advisors LLC, Cetera Wealth Services..."` — location_class=body
3. `broker-dealer` (regulatory-license) — `"Affiliation Models Independent Broker-Dealer Elevate your business..."` — location_class=body
4. `RIA` (business-model) — `"Registered Investment Advisers (RIA) Choose a turnkey program..."` — location_class=body
5. `Registered Investment Adviser` (business-model) — `"Avantax Planning Partners, Inc. is an SEC registered investment adviser..."` — location_class=body

These are LEGITIMATE asset-mgmt-transition signals on a target that IS structurally an RIA + tax-professional platform. Not superficial. Decision-useful.

1st-Atlantic gold: empty term_matches + 0 score (pages scanned, no AM-indicator hits) — true-negative.
Carl-Ostenson gold: empty term_matches + 0 score (page_count_scanned=1, but page was BLOCKED at silver — gold mechanically computes 0 over no content; this is NOT a discriminating zero, it's a no-data zero).

**G1 observation:** gold zero-score is currently overloaded — distinguishes "no AM signal in scanned content" from "no content was scanned". Carl-Ostenson's `rollup_score=0` is from EMPTY-BODY upstream, not from "we read your site and saw no AM language." An IR analyst handed the 0-score ranking would not know the difference. Recommend gold add field `score_class: {SCORED, BLOCKED_UPSTREAM, NO_PAGES}` or similar to distinguish. Not critical-block but worth banking as v2 candidate.

---

## P1 — Parsing yield

**Verdict: B+**

For bronze records with body_text populated (SUCCESS class, n=10 in sample = 5 Avantax + 5 Atlantic), silver yields rich non-trivial extraction:

| Field | Avantax sample | 1st-Atlantic sample (expected from schema) |
|---|---|---|
| title | 55 chars | populated |
| meta_tags | 8 fields | populated |
| headings (h1-h6) | 6-level dict, lists per level | populated |
| body_text | 6508 chars | populated |
| link_graph | internal_links + external_links | populated |
| structured_blocks | addresses + emails + phones | populated |
| structured_data | json_ld | populated |

Parser is extracting decision-useful structural signal, not just text dumps. Each silver record gives gold (a) where-on-page-the-match-fell (via `location_class` from headings/meta_tags/body), (b) page metadata to disambiguate (title + og:* tags), (c) link graph for crawl-extension topology, (d) structured contact data for downstream IR-team enrichment.

For BLOCKED records (n=1 Carl-Ostenson sample, ~30% rate on n=3): silver yields the BLOCKED schema correctly (mechanically tracks the empty-body class for AC-T2 telemetry).

Parsing yield grade B+ on the success-class sample. Honest-limit: P1 only validates the 2 IMOs that actually delivered bronze HTML (Avantax + Atlantic, 10 page samples); cannot generalize to 99-IMO universe yield without C1 resolution.

---

## P2 — Empirical TP/FP discrimination

**Verdict: INCOMPLETE — CONDITIONAL on C1 universe-run**

Valid empirical sample (n=2):
- **Avantax** — known publicly to be an RIA + tax-professional asset-mgmt platform → gold rollup_score=100 — **TRUE POSITIVE**
- **1st-Atlantic** — known to be insurance-only IMO → gold rollup_score=0 — **TRUE NEGATIVE**

Discrimination on n=2 = clean (1 TP + 1 TN, no FP, no FN). This was the prior 1d28ffcc9 META-VERIFY 7-items finding (discrimination axis EMPIRICALLY VALIDATED).

Andrew mandated test: 5 known-AM IMOs + 5 known-absent IMOs. **Cannot deliver** — only 3 IMOs in S3, one of which (Carl-Ostenson) is BLOCKED-class (gold score=0 but for EMPTY-BODY reason, not discriminating-negative reason).

P2 fires when C1 resolves OR when COO dispatches a 10-IMO subset-scrape ahead of the full 99-IMO universe-run (a "TP/FP-validation subset" pre-flight). Recommended: have ws CTO + COO scope the 10-IMO P2 validation sample explicitly in the next /ws-charter cycle so P2 can fire without waiting for full universe-run.

---

## W1 — Term taxonomy criterion

**Verdict: C+**

Criterion (from `data/find/imo/config/term-taxonomy-v1.json`):

- **Match mechanism:** keyword-presence via regex/word-boundary (NOT co-occurrence, NOT contextual NLP). Three match-type variants: `exact_or_word_boundary` (case-sensitive `\bTERM\b`), `case_insensitive` (case-insensitive `\bTERM\b`), `regex` (explicit pattern for variants like `Series\s*65`).
- **Weighting structure:** 6 classes with per-class weight tier:
  - `regulatory-license` weight=1.0 (FINRA, NASAA, Series 7/24/63/65/66/79, IAR, broker-dealer, Form ADV, fiduciary, Reg BI) — strongest signal
  - `business-model` weight=0.85 (RIA, asset management, wealth management, investment advisory, hybrid RIA, dually-registered) — load-bearing transition indicator
  - `certification` weight=0.85 (CFP, CFA, ChFC, CIMA, AIF, CPWA, RICP)
  - `product` weight=0.7 (AUM, SMA, UMA, TAMP, model portfolio, asset allocation)
  - `org-structure` weight=0.7 (CIO, portfolio manager, investment committee, wealth advisor)
  - `platform-partnership` weight=0.55 (Envestnet, AssetMark, Schwab Advisor Services, Fidelity Institutional, Pershing, SEI)
- **Location-multiplier:** title=3.0 / og_title=2.5 / h1=2.5 / h2=2.0 / og_description=2.0 / structured_data=2.0 / h3=1.75 / h4-h6=1.5 / address_block=1.5 / meta_keywords=1.5 / anchor_text=1.25 / body=1.0
- **Damping:** per-term `log(1+n)` over count of occurrences — prevents single-term-spam
- **Class diversity:** multiplier `1 + 0.1 * (num_classes_with_matches - 1)` capped at 1.5
- **Scale:** raw rollup * class_diversity * 4, capped at 100

**W1 CONCERN — threshold semantics for has-WM-program vs adjacent vs absent NOT stated.** Andrew's mandate verbatim asks "how we're ranking entities that appear to have wealth-management programs or may be adjacent to it" — implies 3 classes (present / adjacent / absent). The taxonomy config produces a continuous 0-100 score, not a 3-class label. **No threshold mapping** documented in the config, the design brief, or PRD §4. (PRD mentions "top quintile + explicit Series-license mention" as Phase 2 subset cut — which implies threshold ~80th percentile + a sub-filter — but that's project-level subset selection, not per-IMO classification.)

This is the W1 finding: methodology is defensible at the scoring layer; the classification layer (continuous score → discrete label) is not defined. REPAIR-AMENDMENT-AUTHORIZED (b) trigger (see §REPAIR-AMENDMENT).

---

## W2 — Scoring weights traceability

**Verdict: C**

Per-class term weights (term-taxonomy-v1.json):
- regulatory-license = 1.0 (rationale: "strongest signal class — these don't appear on insurance-only websites without an asset-mgmt-transition tie")
- business-model = 0.85 (rationale: "load-bearing transition indicator")
- certification = 0.85 (rationale: "tied to investment-management qualification, not insurance-marketing")
- product = 0.7 (rationale: "some leak from annuity-vocabulary")
- org-structure = 0.7 (rationale: "absent on many transitioning IMOs")
- platform-partnership = 0.55 (rationale: "partner-mention correlates with asset-mgmt-platform integration but doesn't directly indicate IMO-owned asset-mgmt")

**Term-class weight provenance: heuristic-with-rationale.** Documented in `term-taxonomy-v1.json` `class_taxonomy` section. Reasonable; aligned with the discrimination signal hypothesis (regulatory-license + business-model > product + org-structure > platform-partnership). NOT empirically fit yet (config explicitly marked `ratify_class: DRAFT` pending Phase 1 empirical run + IR-team spot-review).

Scoring formula scale-factor (4): rationale = "position the typical mid-signal IMO score in the 30-60 band; high-signal IMO approaches 100; pure-insurance IMOs score < 10." **Empirical-by-eyeball, not Andrew-direction.**

Employee-score weights (scoring-weights-v0.1.json):
- w_tenure=0.25, w_seniority=0.25, w_series=0.30, w_keyword=0.20 (sum=1.00) — **NO explicit provenance** in config; presented as the formula without per-weight rationale
- series_license_weights (7/24=0.30, 65/66=0.40, etc.) — has detailed `series_license_weights_rationale` section
- title_seniority_class_weights (c-suite=1.00, founder=1.00, owner=1.00, evp_svp=0.85, vp_director=0.65, manager=0.40, ic=0.15) — has note "founder + owner added per COO O-6 ratification 2026-05-27T17:08Z"

Company-score weights (scoring-weights-v0.1.json):
- w_phase1_signal=0.30, w_top_employee=0.25, w_series_density=0.20, w_hiring_signal=0.15, w_job_keyword=0.10 (sum=1.00) — **NO explicit provenance** in config

**W2 finding:** the 4 main employee-score weights + 5 main company-score weights are presented as the formula without Andrew-direction OR empirical-fit citation in the config. These ARE weight-allocations the IR-team-facing ranking turns on; they need explicit ratification cycle (per the `open_items_pending_empirical_ratify` block which lists "O-2-final" — Employee + company weights final ratify post-Phase-3-impl IR-team review).

Until O-2-final fires, these are placeholder weights of unstated provenance. Per Andrew's mandate question "how we're ranking entities" — the ranking turns on placeholder weights. NOT a noise verdict, but a "honest about your provenance" verdict.

---

## W3 — Ranking output

**Verdict: INCOMPLETE — CONDITIONAL**

`aws s3 ls s3://opal-data-imo/serving/` returns:
- `serving/.keep` (0 bytes)
- `serving/_meta/source-list-2026-05-27.json` (14 KB; the 99-IMO universe input list)

**NO consolidated `serving/companies.{json,parquet}` / `serving/scoring.{json,parquet}` / `serving/employees.{json,parquet}` exists.**

The 3 per-IMO `gold/score.json` files exist but are NOT consolidated. No top-quintile ranking, no IR-team-facing target table, no decision artifact.

W3 cannot fire empirically without:
1. C1 resolution (99-IMO universe scraped → 99 gold/score.json files)
2. A Phase 1 consolidation TO (likely DS~B or DS~E lane) that reads all gold/score.json + emits `serving/scoring.json` with a ranked list per company
3. Optional: a serving-layer view that joins phase1 gold with phase2 LinkedIn enrichment (gated to top-quintile subset per PRD)

W3 CONDITIONAL. Until consolidation lands, "ranking output" is a per-IMO score-file enumeration only.

---

## M1 — Noise vs signal aggregate (CVO meta-judgment)

**Verdict: CONDITIONAL — METHODOLOGICALLY-MEANINGFUL / EMPIRICALLY-INCOMPLETE**

Andrew's binary question: "is this pipeline producing IR-team-actionable output, or is it throwing noise around?"

CVO independent judgment:

**Methodologically:** NOT noise. The taxonomy is substantive (6 classes, 60+ terms, class-weighted, location-weighted, log-dampened, class-diversity-multiplied). The 2-IMO valid empirical sample discriminates correctly (Avantax 100 TP / Atlantic 0 TN). The gold output includes inspectable evidence trails. An IR analyst handed Avantax's `term_matches` would agree the score is well-founded.

**Empirically:** INCOMPLETE. Only 3/99 = 3% of the universe scraped. No consolidated ranking. No 5-on-5 TP/TN discrimination test. No top-20 to evaluate. **Cannot answer "would an IR analyst agree with the top-20 ranking after 30min of independent verification" because the top-20 does not exist yet.**

**Structurally:** the Phase 1 RAVC2-Accept gate per PRD v0.6 has correctly absorbed CVO's prior META-VERIFY 7-items + Andrew's spirit+business-usefulness directive into AC-T1 (crawl-coverage telemetry) and AC-T2 (empty-body escape-valve conditional). The gate logic is sound; what's missing is the empirical run that the gate evaluates.

**Anti-pattern check (Andrew's verbatim):** "not just mechanically doing a bunch of bullshit throwing noise around." Per CVO independent assessment: NO, the methodology is not bullshit-noise. The TAXONOMY is empirically defensible on the discriminating sample. The COVERAGE GAP is mechanical-untruth (Phase 1 is not what its self-report claims, see C1).

**M1 grade:** WITHHELD until C1 + W3 + P2 close. The pipeline is not noise; it's incomplete. Re-grade at next /verify-channel comprehensive Mode B fire post-99-IMO-universe-run.

---

## REPAIR-AMENDMENT-AUTHORIZED triggers

Per LD-0066 + LD-0065 — /verify-channel verdicts authorize ws CTO REPAIR-AMENDMENT authority on two structural classes. This cycle fires TWO triggers:

### Trigger 1: REPAIR-AMENDMENT-AUTHORIZED (a) — Mechanical-untruth to reality

**Class (a):** PRD docs/architecture/FIND_INSURE.md §1 mandate text + §4 Phase 1 narrative declare "Phase 1 web-scrape end-to-end across full 100-IMO universe." Empirical state at 2026-05-27T~20:55Z = **3/99 = 3.0% coverage**. PRD self-report and S3 reality are inconsistent.

**Finding-summary:** Phase 1 PRD §4 claims universe-scoped delivery; bucket inventory shows 3/99 IMOs scraped. PRD amend should either (i) clarify Phase 1 is delivered via subset-then-universe staged scope-cut (and AC2 fires on subset, not universe) OR (ii) keep universe scope but mark current state as "Phase 1 in-flight, 3/99 = 3% complete; 99-IMO fan-out scheduled for {date}" so the document doesn't claim what it hasn't done.

**MCP routing:** ws CTO via inbox subject `[RECOMMEND_REPAIR_AMENDMENT: (a) FIND_INSURE Phase 1 universe-scope vs 3/99 mechanical-untruth]`.

### Trigger 2: REPAIR-AMENDMENT-AUTHORIZED (b) — Inadequate solution-coverage

**Class (b):** Two coverage gaps surfaced:

**(b)(i) W1 threshold semantics gap.** Andrew mandate verbatim: "ranking entities that appear to have wealth-management programs **or may be adjacent to it**" — implies a 3-class label (present / adjacent / absent). Taxonomy + scoring formula produces continuous 0-100 score; no threshold mapping documented. Per Step 3.5 meaning-axis: the consumer (IR team) reads a label, not a continuous score. The classification layer is missing.

**(b)(ii) Rule 17 silver field-drop.** `data/find/imo/scripts/silver/parse_web_silver.py:291` `build_silver_record` drops 5 bronze meta fields (http_headers, crawl_depth, robots_txt_compliance, scheme_fallback, tls_fail_original). These fields are diagnostic — load-bearing for debugging empty-body / blocked-class root-causes (which is exactly the AC-T2 class). Rule 17 mandates silver passes through bronze content. The drops are a structural violation.

**Finding-summary:** PRD §4 needs (i) WM-present / adjacent / absent classification rule + threshold mapping AND silver needs to pass-through the 5 dropped bronze meta fields. Both are coverage gaps the current PRD doesn't address.

**MCP routing:** ws CTO via inbox subject `[RECOMMEND_REPAIR_AMENDMENT: (b) FIND_INSURE W1 threshold semantics + Rule 17 silver field-drop]`.

---

## §5.6 Input 0 emission

Verdict: `MISALIGNED`
- `axis_mechanical: YELLOW` (mechanical pipeline delivers on 3-IMO sample; 96-IMO coverage gap is structural-incomplete not mechanical-broken)
- `axis_intent_coverage: RED` (PRD claims universe; reality 3%; AC-T2 threshold cannot fire on n=3; W1 threshold-mapping missing)
- `axis_decision_useful: YELLOW` (methodology decision-useful on sample; consolidated serving table not yet exists for end-to-end consumer probe)
- `axis_constitution_coherence: NULL` (drift-review subscan deferred — this fire is empirical-axis-focused per Andrew mandate, not constitution-drift cadence)
- `mode: comprehensive`
- `source: verify-channel-ws`

Record emission deferred to next cycle (concurrent-index churn risk during multi-MCP turn; will land at next regular /verify-channel scan).

---

## Routing summary

- **Primary verdict to:** ws CTO (REPAIR-AMENDMENT triggers a + b) + CC ws COO (drive prioritization on C1 universe-run + W3 consolidation)
- **MSTR + Andrew:** awareness via this artifact on origin + COO MCP CC (LD-0116 — T1 to T1 chain; Andrew is implicit recipient via session focus declaration in the trigger brief)
- **Per axis evidence:** this artifact serves as the §5.6 substrate record for Andrew's mandate; each axis answer cites S3 / file / count / sample

---

## Self-validation surface declaration

CVO did NOT author any FIND_INSURE pipeline component. Discrimination on Avantax/1st-Atlantic was prior CVO verdict (1d28ffcc9 META-VERIFY 7-items) — this cycle re-confirms via independent S3 read, not self-validation. CVO authored AC-T1/AC-T2 recommendations absorbed into PRD v0.6 bb31769cc — but this cycle's C1/C2 findings are not validating CVO's own AC authorship; they're validating Phase 1 substance which CVO never authored.

Per [[feedback_cvo_self_validation_mitigation_pattern]]: surface area documented; (a) accurate report of own actions, (b) chartered-not-escape-hatch acceptance path, (c) Andrew override is operative via the 2050Z mandate itself.

---

— 3.0.0_SA_CVO 2026-05-27T~21:00Z
